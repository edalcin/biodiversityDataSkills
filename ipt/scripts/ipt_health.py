#!/usr/bin/env python3
"""ipt_health.py - check, report on and (optionally) fix the health of a GBIF IPT instance.

Python 3.9+, standard library only.  Sub-commands:

  check     <base_url> [--resource SHORTNAME] [--json] [--no-gbif] [--stale-days N]
  resources <base_url> [--json]
  report    <base_url> --resource SHORTNAME            (login required)
  publish   <base_url> --resource SHORTNAME --yes      (login required; the ONLY write action)
  selftest                                             (offline parser self-check)

Credentials come from the environment only (never from argv, never stored):
  IPT_URL       base URL when <base_url> is omitted (e.g. https://ipt.example.org/ipt)
  IPT_USER      IPT account e-mail          IPT_PASSWORD   IPT account password
Without IPT_USER/IPT_PASSWORD only the public checks run.  Session cookies live in memory only.

Exit code: 0 = no ERROR finding / success, 1 = at least one ERROR finding / failure.
Catalogue of check IDs and fixes: references/health-checks.md (one `## <ID>` section per check).
"""
import argparse
import concurrent.futures as cf
import html
import json
import os
import re
import socket
import ssl
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone

UA = "biodiversityDataSkills-ipt-health"
DOC = "references/health-checks.md"
OK_CRAWL = ("NORMAL", "NOT_MODIFIED")  # CrawlerFinishReason values that mean "nothing wrong"
MONTHS = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
SEV_ORDER = {"ERROR": 0, "WARN": 1, "INFO": 2}

# Short fix hints; every finding also points to `references/health-checks.md#<id>`.
FIX = {
    "IPT-REACH": "Check Tomcat/Docker container, reverse proxy and firewall; read catalina.out and the IPT admin.log.",
    "IPT-REDIRECT": "Set the IPT base URL (Admin > Configuration) to the final public URL so GBIF crawls the right host.",
    "IPT-SETUP": "Finish the setup wizard (data directory, admin user, mode, base URL).",
    "IPT-VERSION": "Informational.",
    "IPT-OUTDATED": "Upgrade the IPT (manual: 'Upgrading'); take a backup of the data directory first.",
    "IPT-TLS": "Renew the certificate on the web server/proxy in front of the IPT.",
    "IPT-BASEURL": "Admin > Configuration > Base URL must equal the public URL (then republish).",
    "IPT-MODE": "Test-mode IPTs register in the GBIF UAT registry; data never reaches gbif.org. Production needs a fresh install/registration.",
    "IPT-INVENTORY": "Open /inventory/v2/dataset in a browser; look for errors in admin.log.",
    "IPT-HEALTH-NET": "IPT cannot reach the registry / rs.gbif.org / its own public URL: check outbound firewall, proxy, base URL.",
    "IPT-HEALTH-DISK": "Free disk space in the data directory (old versions: Manage > resource > delete versions).",
    "IPT-HEALTH-PERMS": "Fix ownership/permissions of the data directory for the Tomcat user.",
    "IPT-HEALTH-SYSTEM": "Informational (OS/Java/Tomcat/mode).",
    "RES-NOT-FOUND": "Check the shortname (case-sensitive) or use `resources` to list them.",
    "RES-NEVER-PUBLISHED": "Complete metadata/mappings and click Publish, or delete the draft resource.",
    "RES-ZERO-RECORDS": "Check source file/SQL and the occurrence/core mapping; use mappingPeek and the publication log.",
    "RES-STALE": "Publish again or enable auto-publishing (Manage > resource > Auto-publishing).",
    "RES-NO-GBIFKEY": "Register the resource with GBIF (Manage > resource > Visibility > Register) if it should be on GBIF.",
    "RES-OVERDUE": "Auto-publication did not run: see the publication report/log, publish manually once (clears the 3-failure lock), fix the root cause.",
    "RES-ARCHIVE": "Republish; if the file is really missing restore from backup (resources/<name>/dwca-<ver>.zip).",
    "RES-EML": "Republish; check resources/<name>/eml-<ver>.xml in the data directory.",
    "RES-BLOCKED": "Open Manage > resource and fix the metadata/organisation/licence reported in the publication warning.",
    "RES-PUBLISH-FAILED": "Read the publication log (`report` sub-command), fix the cause, publish again.",
    "RES-PUBLISHING": "Wait; if it hangs for hours restart Tomcat or use Cancel on the resource page.",
    "RES-NO-REPORT": "Informational: the report is kept in memory and is empty after an IPT restart.",
    "GBIF-API": "GBIF API unreachable from here; retry later or use --no-gbif.",
    "GBIF-DATASET-MISSING": "The registry key is unknown to GBIF: re-register the resource or contact helpdesk@gbif.org.",
    "GBIF-DATASET-DELETED": "Dataset deleted at GBIF: contact helpdesk@gbif.org to restore, or re-register.",
    "GBIF-ENDPOINT": "GBIF crawls a URL that is not this IPT: base URL changed? Ask helpdesk@gbif.org to update the endpoint.",
    "GBIF-NEVER-CRAWLED": "Wait for the crawler or ask helpdesk@gbif.org to trigger a crawl; make sure archive.do is public.",
    "GBIF-CRAWL-FAILED": "Open the crawl details at gbif.org/dataset/<key>; fix archive/EML and republish.",
    "GBIF-NOT-RECRAWLED": "GBIF has not re-crawled since the last publication; wait or ask helpdesk@gbif.org.",
    "GBIF-COUNT-MISMATCH": "Check the dataset's ingestion history on gbif.org; compare IPT records with GBIF processing issues.",
    "GBIF-INSTALLATION": "Installation endpoint (rss.do) differs from this IPT: ask helpdesk@gbif.org to fix the installation.",
    "GBIF-ORPHANS": "Datasets hosted by this installation but not in the public inventory (private/unpublished/removed here).",
    "AUTH-SKIPPED": "Set IPT_USER and IPT_PASSWORD to run authenticated checks.",
    "AUTH-LOGIN": "Verify account/password; the account needs the Manager (or Admin) role.",
    "AUTH-PRIVATE": "Informational: resources only visible to logged-in managers.",
    "LOG-ERRORS": "Open /admin/logfile.do?log=admin (or debug) and investigate the top messages.",
    "LOG-ACCESS": "Admin role is needed to read the logs.",
}


class Net(Exception):
    """Network-level failure (DNS, TLS, timeout, reset)."""


class Resp:
    def __init__(self, status, headers, body, url, elapsed):
        self.status, self.headers, self.body, self.url, self.elapsed = status, headers, body, url, elapsed

    @property
    def text(self):
        return self.body.decode("utf-8", "replace")

    def json(self):
        return json.loads(self.body.decode("utf-8", "replace"))


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):  # we follow redirects ourselves to keep cookies exact
        return None


class Client:
    """Tiny HTTP client: manual redirects, in-memory cookie dict (single host), per-call read limit."""

    def __init__(self, timeout=30, verify=True, cookies=True):
        self.timeout, self.use_cookies, self.cookies = timeout, cookies, {}
        ctx = ssl.create_default_context() if verify else ssl._create_unverified_context()  # noqa: SLF001
        self.opener = urllib.request.build_opener(_NoRedirect, urllib.request.HTTPSHandler(context=ctx))

    def _store(self, headers):
        if not self.use_cookies:
            return
        for sc in headers.get_all("Set-Cookie") or []:
            parts = [p.strip() for p in sc.split(";")]
            name, _, val = parts[0].partition("=")
            attrs = {p.split("=")[0].lower(): p.partition("=")[2] for p in parts[1:]}
            if val == "" or attrs.get("max-age") == "0":
                self.cookies.pop(name, None)
            else:
                self.cookies[name] = val

    def request(self, url, method="GET", data=None, headers=None, limit=None, follow=True):
        t0 = time.time()
        for _ in range(8):
            h = {"User-Agent": UA, "Accept-Language": "en", "Accept": "*/*"}
            h.update(headers or {})
            if self.use_cookies and self.cookies:
                h["Cookie"] = "; ".join(f"{k}={v}" for k, v in self.cookies.items())
            body = data.encode() if isinstance(data, str) else data
            if body is not None:
                h.setdefault("Content-Type", "application/x-www-form-urlencoded")
            req = urllib.request.Request(url, data=body, headers=h, method=method)
            try:
                try:
                    r = self.opener.open(req, timeout=self.timeout)
                except urllib.error.HTTPError as e:  # 3xx/4xx/5xx are responses for us
                    r = e
                status, hdrs = r.getcode(), r.headers
                raw = r.read(limit) if limit else r.read()
                r.close()
            except (urllib.error.URLError, socket.timeout, ssl.SSLError, OSError, ValueError) as e:
                raise Net(str(getattr(e, "reason", e))) from e
            except Exception as e:  # http.client.HTTPException etc.
                raise Net(f"{type(e).__name__}: {e}") from e
            self._store(hdrs)
            loc = hdrs.get("Location")
            if follow and status in (301, 302, 303, 307, 308) and loc:
                url = re.sub(r"\s+", "", urllib.parse.urljoin(url, loc.split(",")[0]))  # IPT may echo `r=a, a` for duplicated params
                if status in (301, 302, 303):
                    method, data = "GET", None
                continue
            return Resp(status, hdrs, raw, url, time.time() - t0)
        raise Net("too many redirects")


# --------------------------------------------------------------------------- helpers
def txt(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def norm_base(u):
    u = (u or "").strip().rstrip("/")
    u = re.sub(r"/(home|admin/home|manage/home)(\.do)?$", "", u)
    if u and "://" not in u:
        u = "https://" + u
    return u


def q(s):
    return urllib.parse.quote(s, safe="")


def parse_dt(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return None


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def dt_row(row):
    """One DataTables row of /api/resources or /manager-api/resources (column order: ResourceManagerImpl)."""
    if len(row) < 12:
        raise ValueError(f"unexpected row with {len(row)} columns (IPT older than 3.x?)")
    return dict(shortname=row[11], title=txt(row[1]), type=txt(row[3]), records=txt(row[5]),
                modified=txt(row[6]), last_published=txt(row[7]), next_published=txt(row[8]),
                overdue="text-gbif-danger" in row[8], status=txt(row[9]))


DT_FORM = urllib.parse.urlencode({"draw": 1, "start": 0, "length": 10000, "search[value]": "",
                                  "order[0][column]": 1, "order[0][dir]": "asc"})


class Run:
    """State shared by all checks of one invocation."""

    def __init__(self, args, base):
        self.args, self.base = args, base
        self.http = Client(args.timeout, not args.insecure)
        self.gbif = Client(args.timeout, True, cookies=False)
        self.findings, self.lock = [], threading.Lock()
        self.res = {}  # shortname -> merged resource dict
        self.version = None
        ga = getattr(args, "gbif_api", None)
        self.gbif_api = ga.rstrip("/") if ga else "https://api.gbif.org/v1"
        self.authed = False
        self.installations = Counter()

    def add(self, cid, sev, msg, resource=None, evidence=None):
        f = {"id": cid, "severity": sev, "resource": resource, "message": msg, "evidence": evidence,
             "fix": (f"{FIX.get(cid, '')} -> " if sev != "INFO" else "") + f"{DOC}#{cid.lower()}"}
        with self.lock:
            self.findings.append(f)

    def guard(self, cid, fn, *a):
        """Run one check; an exception becomes a finding and never aborts the run."""
        try:
            return fn(*a)
        except Net as e:
            self.add(cid, "ERROR" if cid == "IPT-REACH" else "WARN", f"check could not run (network): {e}", evidence=self.base)
        except Exception as e:  # noqa: BLE001 - a broken check must not kill the report
            self.add(cid, "WARN", f"check crashed: {type(e).__name__}: {e}")

    def url(self, path):
        return self.base + path


# --------------------------------------------------------------------------- public checks
def check_reach(run):
    r = run.http.request(run.url("/"))
    if "setupDataDirectory" in r.url:
        run.add("IPT-SETUP", "ERROR", "IPT redirects to the setup wizard (setup incomplete)", evidence=r.url)
        return False
    if r.status >= 400 or "Integrated Publishing Toolkit" not in r.text:
        run.add("IPT-REACH", "ERROR", f"HTTP {r.status}; does not look like an IPT home page", evidence=r.url)
        return False
    sev = "WARN" if r.elapsed > 5 else "INFO"
    run.add("IPT-REACH", sev, f"reachable, HTTP {r.status}, home page in {r.elapsed:.2f}s", evidence=r.url)
    fin = urllib.parse.urlsplit(r.url)
    cur = urllib.parse.urlsplit(run.base)
    if (fin.scheme, fin.netloc) != (cur.scheme, cur.netloc):
        new = norm_base(f"{fin.scheme}://{fin.netloc}{fin.path.rsplit('/', 1)[0] if fin.path.count('/') > 1 else ''}")
        run.add("IPT-REDIRECT", "INFO", f"{run.base} redirects to {new}; using the latter", evidence=r.url)
        run.base = new
    m = re.search(r'title="IPT ([^"]+)"', r.text) or re.search(r"\(IPT\)\s*(?:Version|Vers\S+)\s*([0-9][^<\s]*)", r.text)
    run.version = m.group(1) if m else None
    run.add("IPT-VERSION", "INFO", f"IPT version {run.version or 'not found in footer'}", evidence=run.url("/"))
    return True


def check_outdated(run):
    r = run.gbif.request("https://api.github.com/repos/gbif/ipt/releases/latest")
    tag = r.json().get("tag_name", "")
    nums = lambda s: tuple(int(x) for x in re.findall(r"\d+", s)[:3])  # noqa: E731
    cur, lat = nums(run.version or ""), nums(tag)
    if cur and lat and cur < lat:
        sev = "WARN" if cur[:2] < lat[:2] else "INFO"
        run.add("IPT-OUTDATED", sev, f"running {run.version}, latest release is {tag}",
                evidence="https://github.com/gbif/ipt/releases/latest")


def check_tls(run):
    u = urllib.parse.urlsplit(run.base)
    if u.scheme != "https":
        run.add("IPT-TLS", "INFO" if u.hostname in ("localhost", "127.0.0.1") else "WARN", "base URL is plain http (no TLS)", evidence=run.base)
        return
    host, port = u.hostname, u.port or 443
    try:
        ctx = ssl.create_default_context() if not run.args.insecure else ssl._create_unverified_context()  # noqa: SLF001
        with socket.create_connection((host, port), timeout=run.args.timeout) as s:
            with ctx.wrap_socket(s, server_hostname=host) as t:
                cert = t.getpeercert()
    except ssl.SSLError as e:
        run.add("IPT-TLS", "ERROR", f"certificate not valid: {e}", evidence=f"{host}:{port}")
        return
    if not cert:  # --insecure: no parsed cert available
        run.add("IPT-TLS", "INFO", "certificate not inspected (--insecure)", evidence=f"{host}:{port}")
        return
    left = (ssl.cert_time_to_seconds(cert["notAfter"]) - time.time()) / 86400
    sev = "ERROR" if left < 0 else "WARN" if left < 21 else "INFO"
    run.add("IPT-TLS", sev, f"certificate expires {cert['notAfter']} ({left:.0f} days)", evidence=f"{host}:{port}")


def check_health(run):
    r = run.http.request(run.url("/api/health"))
    if r.status != 200 or "json" not in r.headers.get("Content-Type", ""):
        h = run.http.request(run.url("/health.do"))
        bad = h.text.count("text-gbif-danger")
        run.add("IPT-HEALTH-NET", "WARN" if bad else "INFO",
                f"/api/health not available; health.do shows {bad} failing item(s)", evidence=h.url)
        return
    s = r.json().get("status", {})
    ev = run.url("/api/health")
    reg = s.get("networkRegistryURL", "")
    for key, label in (("networkRegistry", f"GBIF registry {reg}"), ("networkRepository", "rs.gbif.org vocabulary repository"),
                       ("networkPublicAccess", f"public access to {s.get('networkPublicAccessURL')} (tools.gbif.org check)")):
        if not s.get(key, False):
            run.add("IPT-HEALTH-NET", "WARN", f"{label} failed", evidence=ev)
    ratio = s.get("diskUsedRatio", 0)
    gb = lambda b: f"{b / 2**30:.1f} GiB"  # noqa: E731
    run.add("IPT-HEALTH-DISK", "ERROR" if ratio >= 95 else "WARN" if ratio >= 80 else "INFO",
            f"data directory disk {ratio}% used (free {gb(s.get('diskFree', 0))} of {gb(s.get('diskTotal', 0))})", evidence=ev)
    bad = [k for k in ("readConfigDir", "readLogDir", "writeLogDir", "readTmpDir", "writeTmpDir", "readResourcesDir",
                       "writeResourcesDir", "readSubResourcesDir", "writeSubResourcesDir") if not s.get(k, False)]
    if bad:
        run.add("IPT-HEALTH-PERMS", "ERROR", "file permission problems: " + ", ".join(bad), evidence=ev)
    if re.search(r"gbif-uat", reg):
        run.add("IPT-MODE", "WARN", f"TEST mode: registry is {reg}; datasets are NOT on gbif.org", evidence=ev)
        if not getattr(run.args, "gbif_api", None):
            run.gbif_api = "https://api.gbif-uat.org/v1"
    elif reg:
        run.add("IPT-MODE", "INFO", f"PRODUCTION registry {reg}", evidence=ev)


def load_inventory(run):
    r = run.http.request(run.url("/inventory/v2/dataset"))
    if r.status != 200:
        run.add("IPT-INVENTORY", "ERROR", f"/inventory/v2/dataset returned HTTP {r.status}", evidence=r.url)
        return
    items = r.json().get("resources", [])
    run.add("IPT-INVENTORY", "INFO", f"{len(items)} published public resource(s) in inventory", evidence=r.url)
    for it in items:
        d = run.res.setdefault(it["id"], {"shortname": it["id"]})
        add = it.get("additionalProperties") or {}
        d.update(title=it.get("title"), records=it.get("records"), version=it.get("version"), gbif_key=it.get("gbifKey"),
                 last_published=it.get("lastPublished"), fmt=it.get("format"), core=add.get("core"),
                 by_ext=add.get("recordsByExtension") or add.get("recordsByTable") or {}, public=True,
                 archive_url=(it.get("archive") or [{}])[0].get("url"), eml_url=(it.get("metadata") or [{}])[0].get("url"))


def load_datatable(run, path, private):
    r = run.http.request(run.url(path), "POST", DT_FORM)
    if "json" not in r.headers.get("Content-Type", ""):
        return False
    for row in r.json().get("aaData", []):
        x = dt_row(row)
        d = run.res.setdefault(x["shortname"], {"shortname": x["shortname"]})
        d.update(next_published=x["next_published"], overdue=x["overdue"], status=x["status"])
        if private:
            d["managed"] = True
            d.setdefault("title", x["title"])
            d.setdefault("manage_last_published", x["last_published"])
            if x["last_published"] == "--":
                d["never_published"] = True
            if not d.get("public"):
                d["records"] = d.get("records") or x["records"]
        else:
            d.setdefault("title", x["title"])
    return True


def check_public_datatable(run):
    if not load_datatable(run, "/api/resources", False):
        run.add("IPT-INVENTORY", "WARN", "/api/resources did not return JSON; next-publication checks skipped",
                evidence=run.url("/api/resources"))


def res_public(run, d):
    sn = d["shortname"]
    ev = run.url(f"/resource?r={q(sn)}")
    if d.get("public"):
        fmt = d.get("fmt")
        if not d.get("records") and fmt != "METADATA":
            run.add("RES-ZERO-RECORDS", "WARN", "last published version has 0 records", sn, ev)
        lp = d.get("last_published")
        if lp:
            age = (utcnow().date() - datetime.strptime(lp, "%Y-%m-%d").date()).days
            if age > run.args.stale_days:
                future = bool(d.get("next_published")) and d["next_published"] != "--" and not d.get("overdue")
                run.add("RES-STALE", "INFO" if future else "WARN",
                        f"last published {lp} ({age} days ago, limit {run.args.stale_days})"
                        + ("; auto-publication is scheduled" if future else ""), sn, ev)
        if not d.get("gbif_key"):
            run.add("RES-NO-GBIFKEY", "INFO", "not registered with GBIF (no gbifKey in inventory)", sn, ev)
        for u in (d.get("archive_url"), d.get("eml_url")):  # base URL is what GBIF crawls
            if u and urllib.parse.urlsplit(u).netloc.lower() != urllib.parse.urlsplit(run.base).netloc.lower():
                run.add("IPT-BASEURL", "WARN", f"inventory advertises {u} but instance was queried at {run.base}", sn, u)
                break
        for kind, key, cid in (("archive", "archive_url", "RES-ARCHIVE"), ("metadata", "eml_url", "RES-EML")):
            u = d.get(key)
            if not u:
                continue
            target = run.url("/" + u.rsplit("/", 1)[-1])
            try:
                r = run.http.request(target, limit=65536 if kind == "metadata" else 4)
            except Net as e:
                run.add(cid, "ERROR", f"{kind} not reachable: {e}", sn, target)
                continue
            if r.status != 200:
                run.add(cid, "ERROR", f"{kind} returned HTTP {r.status}", sn, target)
            elif kind == "archive" and r.body[:2] != b"PK":
                run.add(cid, "ERROR", "archive does not start with a ZIP signature", sn, target)
            elif kind == "metadata" and not re.search(rb"[<{]", r.body[:200]):  # EML is XML, data-package metadata is JSON
                run.add(cid, "ERROR", "metadata is neither XML nor JSON", sn, target)
    if d.get("overdue"):
        nxt = parse_dt(d.get("next_published"))
        days = (utcnow() - nxt).total_seconds() / 86400 if nxt else 0
        run.add("RES-OVERDUE", "ERROR" if days > 2 else "WARN",
                f"next publication {d['next_published']} is in the past (~{days:.1f} days); auto-publication is not running for it",
                sn, run.url("/api/resources"))
    if d.get("public") and not run.authed:  # report.do is anonymous on IPT 3.3.x (ajaxStack skips requireManager)
        report_check(run, sn, quiet=True)


# --------------------------------------------------------------------------- GBIF cross-checks
def gbif_get(run, path):
    r = run.gbif.request(run.gbif_api + path)
    return r.status, (r.json() if r.status == 200 else None)


def endpoint_matches(run, ep_url, sn):
    u, b = urllib.parse.urlsplit(ep_url), urllib.parse.urlsplit(run.base)
    return (u.netloc.lower() == b.netloc.lower() and u.path.startswith(b.path.rstrip("/") + "/")
            and urllib.parse.parse_qs(u.query).get("r") == [sn])


def res_gbif(run, d):
    sn, key = d["shortname"], d.get("gbif_key")
    if not key:
        return
    ev = f"{run.gbif_api}/dataset/{key}"
    st, ds = gbif_get(run, f"/dataset/{key}")
    if st == 404:
        run.add("GBIF-DATASET-MISSING", "ERROR", f"registry key {key} unknown to GBIF", sn, ev)
        return
    if ds is None:
        run.add("GBIF-API", "WARN", f"GBIF API returned HTTP {st} for the dataset", sn, ev)
        return
    if ds.get("deleted"):
        run.add("GBIF-DATASET-DELETED", "ERROR", f"dataset deleted at GBIF on {ds['deleted']}", sn, ev)
        return
    if ds.get("installationKey"):
        run.installations[ds["installationKey"]] += 1
    eps = [e.get("url", "") for e in ds.get("endpoints", [])]
    if not any(endpoint_matches(run, e, sn) for e in eps):
        run.add("GBIF-ENDPOINT", "ERROR", f"no GBIF endpoint points to this IPT/resource; endpoints: {eps or 'none'}", sn, ev)
    _, pr = gbif_get(run, f"/dataset/{key}/process?limit=3")
    ev_p = f"{ev}/process"
    runs = (pr or {}).get("results", [])
    lp = d.get("last_published")
    lp_dt = datetime.strptime(lp, "%Y-%m-%d") if lp else None
    if not runs:
        if lp_dt and (utcnow() - lp_dt).days > 3:
            run.add("GBIF-NEVER-CRAWLED", "WARN", "GBIF has no crawl history for this dataset", sn, ev_p)
    else:
        last = runs[0]
        reason = last.get("finishReason")
        errs = sum(last.get(k) or 0 for k in ("pagesFragmentedError", "rawOccurrencesPersistedError",
                                              "verbatimOccurrencesPersistedError", "interpretedOccurrencesPersistedError"))
        if last.get("finishedCrawling") and reason not in OK_CRAWL:
            run.add("GBIF-CRAWL-FAILED", "ERROR", f"last crawl #{last['crawlJob'].get('attempt')} ended {reason} "
                    f"at {last['finishedCrawling']}", sn, ev_p)
        elif errs:
            run.add("GBIF-CRAWL-FAILED", "WARN", f"last crawl finished with {errs} persistence/fragment error(s)", sn, ev_p)
        fin = last.get("finishedCrawling") or last.get("startedCrawling")
        if fin and lp_dt and (utcnow() - lp_dt).days > 3 and fin[:10] < lp:
            run.add("GBIF-NOT-RECRAWLED", "WARN", f"last GBIF crawl {fin[:10]} is older than last publication {lp}", sn, ev_p)
    exp = next((v for k, v in (d.get("by_ext") or {}).items() if k.lower().endswith("/occurrence")), None)
    if exp is not None and d.get("fmt") == "DWCA":
        st, oc = gbif_get(run, f"/occurrence/search?datasetKey={key}&limit=0")
        if oc is not None:
            n = oc.get("count", 0)
            tol = max(10, run.args.count_tolerance * exp)
            if abs(n - exp) > tol:
                run.add("GBIF-COUNT-MISMATCH", "INFO" if "-uat." in run.gbif_api else "WARN",
                        f"IPT published {exp} occurrence rows, GBIF indexes {n}" + (" (UAT does not guarantee indexing)" if "-uat." in run.gbif_api else ""), sn,
                        f"{run.gbif_api}/occurrence/search?datasetKey={key}&limit=0")


def gbif_installation(run):
    if not run.installations:
        run.add("GBIF-INSTALLATION", "INFO", "no dataset with a gbifKey: installation could not be located")
        return
    ik = run.installations.most_common(1)[0][0]
    ev = f"{run.gbif_api}/installation/{ik}"
    st, inst = gbif_get(run, f"/installation/{ik}")
    if inst is None:
        run.add("GBIF-INSTALLATION", "WARN", f"installation {ik} returned HTTP {st}", evidence=ev)
        return
    feeds = [e.get("url", "") for e in inst.get("endpoints", [])]
    b = urllib.parse.urlsplit(run.base)
    if inst.get("deleted") or not any(urllib.parse.urlsplit(u).netloc.lower() == b.netloc.lower() for u in feeds):
        run.add("GBIF-INSTALLATION", "ERROR", f"installation {ik} ('{inst.get('title')}') deleted or its endpoints {feeds} "
                f"do not match {run.base}", evidence=ev)
        return
    known, orphans, off = {d.get("gbif_key") for d in run.res.values()}, [], 0
    while off < 2000:
        st, page = gbif_get(run, f"/installation/{ik}/dataset?limit=100&offset={off}")
        if not page:
            break
        orphans += [f"{x['key']} ({x.get('title', '')[:50]})" for x in page["results"]
                    if x["key"] not in known and not x.get("deleted")]
        if page.get("endOfRecords", True):
            break
        off += 100
    run.add("GBIF-INSTALLATION", "INFO", f"installation {ik} '{inst.get('title')}' matches this IPT", evidence=ev)
    if orphans:
        run.add("GBIF-ORPHANS", "INFO", f"{len(orphans)} dataset(s) of this installation are not in the inventory: "
                + "; ".join(orphans[:8]) + (" ..." if len(orphans) > 8 else ""), evidence=ev + "/dataset")


# --------------------------------------------------------------------------- authenticated part
def login(c, base, user, pw):
    """Returns None on success or an error message.  Flow: LoginAction + CsrfLoginInterceptor (csrfToken form field == CSRFtoken cookie)."""
    r = c.request(base + "/login.do")
    m = re.search(r'name="csrfToken"\s+value="([^"]*)"', r.text)
    if not m:
        return "login form not found" if "logout.do" not in r.text else None
    r = c.request(base + "/login.do", "POST", urllib.parse.urlencode(
        {"csrfToken": m.group(1), "email": user, "password": pw, "login": "Login"}))
    if "logout.do" in r.text:
        return None
    err = re.search(r'alert-danger.*?<span>(.*?)</span>', r.text, re.S)
    return txt(err.group(1)) if err else f"login failed (HTTP {r.status})"


def creds():
    return os.environ.get("IPT_USER", ""), os.environ.get("IPT_PASSWORD", "")


def parse_report(h):
    m = re.search(r'<div class="alert alert-(success|danger|warning)" role="alert">\s*(.*?)\s*</div>', h, re.S)
    state = {"success": "completed", "danger": "failed", "warning": "in_progress"}.get(m.group(1)) if m else "none"
    msgs = [(lv, txt(t), txt(x)) for lv, t, x in re.findall(r'<li class="(\w+)"><span class="small">(.*?)</span>(.*?)</li>', h, re.S)]
    return {"state": state, "text": txt(m.group(2)) if m else "", "messages": msgs}


def parse_manage(h):
    blocked = bool(re.search(r'<(?:a|button)\s[^>]*id="publish-button-show-warning"', h))
    reason = ""
    m = re.search(r'id="publication-modal-title".*?</h5>(.*?)</div>', h, re.S)
    if blocked and m:
        reason = txt(m.group(1))
    return {"blocked": blocked, "reason": reason, "can_publish": bool(re.search(r'<form action="publish\.do\?r=', h)),
            "autopublish": "autopublish-enabled" in h}


def report_check(run, sn, quiet=False):
    ev = run.url(f"/manage/report.do?r={q(sn)}")
    r = run.http.request(ev)
    if "login.do" in r.url:  # newer IPTs may protect report.do
        return
    rp = parse_report(r.text)
    if rp["state"] == "failed":
        tail = [m for lv, _, m in rp["messages"] if lv.lower() in ("error", "warn", "warning")][-2:]
        run.add("RES-PUBLISH-FAILED", "ERROR", f"last publication failed: {rp['text']} {' | '.join(tail)}"[:400], sn, ev)
    elif rp["state"] == "in_progress":
        run.add("RES-PUBLISHING", "INFO", "publication in progress: " + rp["text"][:200], sn, ev)
    elif rp["state"] == "none" and not quiet:
        run.add("RES-NO-REPORT", "INFO", "no publication report in memory (IPT restarted since last publication?)", sn, ev)


def res_auth(run, d):
    sn = d["shortname"]
    ev = run.url(f"/manage/resource.do?r={q(sn)}")
    r = run.http.request(ev)
    if r.status == 200 and "logout.do" in r.text:
        p = parse_manage(r.text)
        if p["blocked"]:
            run.add("RES-BLOCKED", "ERROR" if d.get("overdue") else "WARN",
                    "publication blocked: " + (p["reason"] or "see Manage page warning"), sn, ev)
    else:
        run.add("AUTH-LOGIN", "WARN", f"cannot open manage page (HTTP {r.status}); account may not manage this resource", sn, ev)
        return
    report_check(run, sn)


def check_logs(run):
    ev = run.url("/admin/logfile.do?log=admin")
    r = run.http.request(ev, limit=run.args.max_log_mb * 2**20)
    if r.status != 200 or "text/plain" not in r.headers.get("Content-Type", ""):
        run.add("LOG-ACCESS", "INFO", f"admin.log not readable (HTTP {r.status}); needs Admin role", evidence=ev)
        return
    rows = []
    for ln in r.text.splitlines():
        m = re.match(r"ERROR (\d\d)-(\w{3})-(\d{4}) (\d\d:\d\d:\d\d) \[([^\]]+)\] - (.*)", ln)
        if m:
            try:
                ts = datetime.strptime(f"{m.group(3)}-{MONTHS[m.group(2)]:02d}-{m.group(1)} {m.group(4)}", "%Y-%m-%d %H:%M:%S")
            except (KeyError, ValueError):
                ts = None
            rows.append((ts, m.group(5).rsplit(".", 1)[-1], m.group(6)))
    stamps = [t for t, _, _ in rows if t]
    if stamps:  # window is relative to the newest log line: server time zone is unknown
        lim = max(stamps) - timedelta(hours=24)
        rows = [x for x in rows if x[0] and x[0] >= lim]
    if not rows:
        run.add("LOG-ERRORS", "INFO", "no ERROR lines in the last 24h of admin.log", evidence=ev)
        return
    top = Counter((c, re.sub(r"\d+", "N", m)[:110]) for _, c, m in rows).most_common(5)
    run.add("LOG-ERRORS", "WARN", f"{len(rows)} ERROR line(s) in last 24h of admin.log; top: "
            + " || ".join(f"{n}x [{c}] {m}" for (c, m), n in top), evidence=ev)


def check_system(run):
    h = run.http.request(run.url("/health.do")).text
    cells = re.findall(r'<td>([^<]*)</td>\s*<td class="text-end">\s*(.*?)\s*</td>', h, re.S)
    sysv = {txt(k): txt(v) for k, v in cells if k.strip().lower().split(" ")[0] in ("os", "java", "application", "ipt")}
    run.add("IPT-HEALTH-SYSTEM", "INFO", "; ".join(f"{k}: {v}" for k, v in sysv.items()) or "system section empty",
            evidence=run.url("/health.do"))


def do_auth(run):
    user, pw = creds()
    if not (user and pw) or run.args.no_auth:
        run.add("AUTH-SKIPPED", "INFO", "authenticated checks skipped (IPT_USER/IPT_PASSWORD not set)" if not run.args.no_auth
                else "authenticated checks skipped (--no-auth)")
        return
    err = login(run.http, run.base, user, pw)
    if err:
        run.add("AUTH-LOGIN", "ERROR", f"login failed for {user}: {err}", evidence=run.url("/login.do"))
        return
    if not load_datatable(run, "/manager-api/resources", True):
        run.add("AUTH-LOGIN", "ERROR", f"logged in as {user} but /manager-api/resources is denied (needs Manager role)",
                evidence=run.url("/manager-api/resources"))
        return
    run.authed = True
    priv = [d for d in run.res.values() if d.get("managed") and not d.get("public")]
    run.add("AUTH-PRIVATE", "INFO", f"logged in as {user}; {len(priv)} resource(s) not publicly listed (private/never published)",
            evidence=run.url("/manager-api/resources"))
    for d in run.res.values():
        if d.get("never_published"):
            run.add("RES-NEVER-PUBLISHED", "WARN", "resource exists but was never published", d["shortname"],
                    run.url(f"/manage/resource.do?r={q(d['shortname'])}"))


def run_per_resource(run, only_auth=False):
    pool = [d for d in run.res.values() if (not run.args.resource or d["shortname"] == run.args.resource)]
    if not only_auth:
        with cf.ThreadPoolExecutor(max_workers=max(1, run.args.workers)) as ex:
            futs = []
            for d in pool:
                futs.append(ex.submit(run.guard, "RES-ARCHIVE", res_public, run, d))
                if not run.args.no_gbif and d.get("gbif_key"):
                    futs.append(ex.submit(run.guard, "GBIF-API", res_gbif, run, d))
            cf.wait(futs)
    else:
        for d in pool:  # sequential: the IPT keeps the "current resource" in the shared session
            if d.get("managed"):
                run.guard("RES-BLOCKED", res_auth, run, d)


# --------------------------------------------------------------------------- commands
def render_md(run, secs):
    c = Counter(f["severity"] for f in run.findings)
    out = [f"# IPT health report: {run.base}", "",
           f"- generated: {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}; IPT version: {run.version or 'unknown'}; "
           f"resources: {len(run.res)}; authenticated: {'yes' if run.authed else 'no'}; duration: {secs:.1f}s",
           f"- **summary: {c['ERROR']} ERROR, {c['WARN']} WARN, {c['INFO']} INFO**", ""]
    esc = lambda s: (s or "").replace("|", "\\|").replace("\n", " ")  # noqa: E731
    for title, sevs in (("Problems", ("ERROR", "WARN")), ("Informational", ("INFO",))):
        rows = [f for f in run.findings if f["severity"] in sevs]
        out += [f"## {title}", ""]
        if not rows:
            out += ["_none_", ""]
            continue
        out += ["| Severity | Check | Resource | Message | Evidence | Fix |", "|---|---|---|---|---|---|"]
        out += [f"| {f['severity']} | `{f['id']}` | {esc(f['resource'])} | {esc(f['message'])} | {esc(f['evidence'])} | {esc(f['fix'])} |"
                for f in rows]
        out.append("")
    return "\n".join(out)


def gather(run, with_gbif_data=False):
    run.guard("IPT-INVENTORY", load_inventory, run)
    run.guard("IPT-INVENTORY", check_public_datatable, run)


def need_base(args):
    base = norm_base(args.base_url or os.environ.get("IPT_URL", ""))
    if not base:
        sys.exit("error: give <base_url> or set IPT_URL")
    return base


def cmd_check(args):
    t0, run = time.time(), Run(args, need_base(args))
    if run.guard("IPT-REACH", check_reach, run):
        run.guard("IPT-TLS", check_tls, run)
        run.guard("IPT-HEALTH-NET", check_health, run)
        if not args.no_gbif:
            run.guard("IPT-OUTDATED", check_outdated, run)
        gather(run)
        run.guard("AUTH-LOGIN", do_auth, run)
        if args.resource and args.resource not in run.res:
            run.add("RES-NOT-FOUND", "ERROR", f"resource '{args.resource}' not found in inventory" +
                    ("" if run.authed else " (private/unpublished resources need IPT_USER/IPT_PASSWORD)"))
        run_per_resource(run)
        if run.authed:
            run_per_resource(run, only_auth=True)
            if not args.resource:
                run.guard("LOG-ERRORS", check_logs, run)
            run.guard("IPT-HEALTH-SYSTEM", check_system, run)
        if not args.no_gbif and not args.resource:
            run.guard("GBIF-INSTALLATION", gbif_installation, run)
    run.findings.sort(key=lambda f: (SEV_ORDER[f["severity"]], f["id"], f["resource"] or ""))
    if args.json:
        c = Counter(f["severity"] for f in run.findings)
        print(json.dumps({"base_url": run.base, "ipt_version": run.version, "authenticated": run.authed,
                          "summary": dict(c), "findings": run.findings, "resources": list(run.res.values())}, indent=2))
    else:
        print(render_md(run, time.time() - t0))
    return 1 if any(f["severity"] == "ERROR" for f in run.findings) else 0


def cmd_resources(args):
    run = Run(args, need_base(args))
    run.guard("IPT-REACH", check_reach, run)
    gather(run)
    user, pw = creds()
    if user and pw and not args.no_auth:
        err = login(run.http, run.base, user, pw)
        if err:
            print(f"warning: login failed ({err}); listing public resources only", file=sys.stderr)
        else:
            run.guard("AUTH-LOGIN", load_datatable, run, "/manager-api/resources", True)
    rows = sorted(run.res.values(), key=lambda d: d["shortname"])
    if args.json:
        print(json.dumps(rows, indent=2))
        return 0
    print("| Shortname | Title | Records | Last published | Version | Next publication | Status | GBIF key |")
    print("|---|---|---|---|---|---|---|---|")
    for d in rows:
        nxt = d.get("next_published") or "--"
        nxt += " **OVERDUE**" if d.get("overdue") else ""
        lp = d.get("last_published") or d.get("manage_last_published") or "--"
        print(f"| {d['shortname']} | {(d.get('title') or '')[:60].replace('|', '/')} | {d.get('records', '--')} | {lp} | "
              f"{d.get('version', '--')} | {nxt} | {d.get('status', '--')} | {d.get('gbif_key') or '--'} |")
    return 0


def logged_run(args):
    user, pw = creds()
    if not (user and pw):
        sys.exit("error: set IPT_USER and IPT_PASSWORD in the environment")
    run = Run(args, need_base(args))
    err = login(run.http, run.base, user, pw)
    if err:
        sys.exit(f"error: login failed: {err}")
    return run


def print_report(run, sn, lines):
    rp = parse_report(run.http.request(run.url(f"/manage/report.do?r={q(sn)}")).text)
    print(f"## Publication report for {sn}: {rp['state'].upper()}\n{rp['text']}\n")
    for lv, t, m in rp["messages"][-lines:]:
        print(f"{lv.upper():6} {t} {m}")
    log = run.http.request(run.url(f"/publicationlog.do?r={q(sn)}"), limit=2**20)
    if log.status == 200:
        print(f"\n## publicationlog.do (last {lines} lines)")
        print("\n".join(log.text.splitlines()[-lines:]))
    return rp


def cmd_report(args):
    run = logged_run(args)
    rp = print_report(run, args.resource, args.lines)
    return 1 if rp["state"] == "failed" else 0


def cmd_publish(args):
    if not args.yes:
        print("refusing to publish without --yes (publishing creates a new resource version and may notify GBIF).", file=sys.stderr)
        return 1
    run, sn = logged_run(args), args.resource
    page = run.http.request(run.url(f"/manage/resource.do?r={q(sn)}"))
    if page.status != 200:
        print(f"error: cannot open resource '{sn}' (HTTP {page.status})", file=sys.stderr)
        return 1
    mp = parse_manage(page.text)
    if mp["blocked"] or not mp["can_publish"]:
        print(f"error: publication is blocked for '{sn}': {mp['reason'] or 'no publish form on the manage page'}", file=sys.stderr)
        return 1
    if parse_report(run.http.request(run.url(f"/manage/report.do?r={q(sn)}")).text)["state"] == "in_progress":
        print(f"error: '{sn}' is already being published", file=sys.stderr)
        return 1
    r = run.http.request(run.url(f"/manage/publish.do?r={q(sn)}"), "POST",
                         urllib.parse.urlencode({"publish": "Publish", "summary": "published by ipt_health.py"}))
    errs = [txt(e) for e in re.findall(r'alert alert-danger.*?<span>(.*?)</span>', r.text, re.S)]
    if r.status >= 400 or errs:
        print(f"error: publish rejected (HTTP {r.status}): {' | '.join(errs) or 'see IPT UI'}", file=sys.stderr)
        return 1
    print(f"publication of '{sn}' started; polling {run.url('/manage/report.do?r=' + q(sn))}")
    end, rp = time.time() + args.wait, {"state": "none"}
    while time.time() < end:
        time.sleep(2)
        rp = parse_report(run.http.request(run.url(f"/manage/report.do?r={q(sn)}")).text)
        if rp["state"] in ("completed", "failed"):
            break
    if rp["state"] == "in_progress" or rp["state"] == "none":
        print(f"timeout after {args.wait}s: state={rp['state']} (publication may still be running; use `report`)", file=sys.stderr)
        return 1
    print_report(run, sn, args.lines)
    if rp["state"] == "completed":
        inv = run.http.request(run.url("/inventory/v2/dataset")).json().get("resources", [])
        cur = next((x for x in inv if x["id"] == sn), None)
        if cur:
            print(f"\ninventory now lists {sn} version {cur['version']}, {cur['records']} records, lastPublished {cur['lastPublished']}")
    return 0 if rp["state"] == "completed" else 1


def build_parser():
    ap = argparse.ArgumentParser(prog="ipt_health.py", description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog="Credentials: env IPT_USER / IPT_PASSWORD (login), IPT_URL (default base URL). Never passed on argv.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, resource=False):
        p.add_argument("base_url", nargs="?", help="IPT base URL, e.g. https://ipt.example.org/ipt (default: $IPT_URL)")
        p.add_argument("--timeout", type=float, default=30, help="per-request timeout in seconds (default 30)")
        p.add_argument("--insecure", action="store_true", help="do not verify TLS certificates of the IPT")
        p.add_argument("--no-auth", action="store_true", help="ignore IPT_USER/IPT_PASSWORD")
        if resource:
            p.add_argument("--resource", required=True, metavar="SHORTNAME")

    c = sub.add_parser("check", help="run the health check and print a Markdown (or JSON) report")
    common(c)
    c.add_argument("--resource", metavar="SHORTNAME", help="only check this resource")
    c.add_argument("--json", action="store_true")
    c.add_argument("--no-gbif", action="store_true", help="skip GBIF API / GitHub cross-checks")
    c.add_argument("--stale-days", type=int, default=365, help="RES-STALE threshold (default 365)")
    c.add_argument("--count-tolerance", type=float, default=0.05, help="GBIF-COUNT-MISMATCH relative tolerance (default 0.05)")
    c.add_argument("--gbif-api", help="GBIF API base (default: derived from the IPT registry: api.gbif.org or api.gbif-uat.org)")
    c.add_argument("--workers", type=int, default=4, help="parallel per-resource checks (default 4)")
    c.add_argument("--max-log-mb", type=int, default=10, help="max MB of admin.log to read (default 10)")
    c.set_defaults(fn=cmd_check)

    r = sub.add_parser("resources", help="list resources (inventory + next publication)")
    common(r)
    r.add_argument("--json", action="store_true")
    r.set_defaults(fn=cmd_resources, gbif_api=None)

    p = sub.add_parser("report", help="show last publication report and log (login)")
    common(p, True)
    p.add_argument("--lines", type=int, default=60, help="lines of log to show (default 60)")
    p.set_defaults(fn=cmd_report)

    u = sub.add_parser("publish", help="FIX action: publish a resource now (login). Requires --yes")
    common(u, True)
    u.add_argument("--yes", action="store_true", help="confirm that you really want to publish")
    u.add_argument("--wait", type=int, default=600, help="seconds to wait for completion (default 600)")
    u.add_argument("--lines", type=int, default=40)
    u.set_defaults(fn=cmd_publish)
    sub.add_parser("selftest", help="offline parser self-check (no network)").set_defaults(fn=cmd_selftest)
    return ap


def cmd_selftest(_args):
    row = ["", "<a>T</a>", "", "", "", "<a>1,234</a>", "2026-01-01 10:00:00", "2026-01-02 10:00:00",
           '<span class="text-gbif-danger">2026-01-03 10:00:00</span>', "<span>Public</span>", "x", "my-res", ""]
    d = dt_row(row)
    assert d["shortname"] == "my-res" and d["overdue"] and d["next_published"] == "2026-01-03 10:00:00" and d["records"] == "1,234"
    rep = parse_report('<div class="alert alert-danger" role="alert">boom</div><li class="ERROR"><span class="small">10:00:00</span> bad</li>')
    assert rep["state"] == "failed" and rep["text"] == "boom" and rep["messages"][0][2] == "bad"
    assert parse_report("<h5>Finished</h5>")["state"] == "none"
    assert parse_manage('<a id="publish-button-show-warning" href="#">')["blocked"]
    assert not parse_manage('$("#publish-button-show-warning").on(')["blocked"]
    assert parse_manage('<form action="publish.do?r=x" method="post">')["can_publish"]
    assert norm_base("ipt.example.org/ipt/") == "https://ipt.example.org/ipt"
    print("selftest ok")
    return 0


def main(argv=None):
    for s in (sys.stdout, sys.stderr):  # IPT logs contain non-ASCII (e.g. check marks); Windows consoles choke
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    try:
        return args.fn(args)
    except Net as e:
        print(f"network error: {e}", file=sys.stderr)
        return 1
    except (BrokenPipeError, KeyboardInterrupt):
        return 130


if __name__ == "__main__":
    sys.exit(main())
