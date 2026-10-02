# IPT endpoints reference

Every URL an IPT instance exposes, how to authenticate to it, what it returns, and which calls change state. Companion files: `health-checks.md` (what to check), `administration.md`, `resources-publishing.md`, `releases.md`, `known-issues.md`.

Evidence tags used below:
- **[SRC]** read in the IPT source (`gbif/ipt` main, commit 62097149, version 3.3.7-SNAPSHOT).
- **[OBSERVED]** verified against a throw-away local Docker `gbif/ipt:latest` container, **IPT 3.3.6**, on 2026-10-02 (container removed afterwards), or against the live GBIF API/registry.
- **[INFERENCE]** deduced from code, not run.

⚠️ = the call **mutates state** (publishes, deletes, registers, changes visibility/config, cancels a job, …). Never call a ⚠️ endpoint during a read-only health check.

## Table of contents
1. [Conventions and path legend](#1-conventions-and-path-legend)
2. [Public portal (anonymous)](#2-public-portal-anonymous)
3. [Machine APIs in depth](#3-machine-apis-in-depth)
   - 3.1 [`/inventory/dataset` (v1)](#31-inventorydataset-v1)
   - 3.2 [`/inventory/v2/dataset`](#32-inventoryv2dataset)
   - 3.3 [`/api/resources` and `/manager-api/resources` (DataTables)](#33-apiresources-and-manager-apiresources-datatables)
   - 3.4 [`/admin-api/publication-report(s)` (publishing status API)](#34-admin-apipublication-reports-publishing-status-api)
   - 3.5 [`/api/health` and `/health.do`](#35-apihealth-and-healthdo)
   - 3.6 [RSS `/rss.do`](#36-rss-rssdo)
   - 3.7 [Files: `archive.do`, `eml.do`, `metadata.do`, `rtf.do`, logs, `dcat`](#37-files-archivedo-emldo-metadatado-rtfdo-logs-dcat)
   - 3.8 [Resource page `/resource`](#38-resource-page-resource)
4. [Login, session, CSRF (scripted access)](#4-login-session-csrf-scripted-access)
5. [Manage section (manager role)](#5-manage-section-manager-role)
6. [Admin section (admin role)](#6-admin-section-admin-role)
7. [GBIF registry and API endpoints](#7-gbif-registry-and-api-endpoints)
8. [Data directory layout](#8-data-directory-layout)
9. [Runbook verification (corrections)](#9-runbook-verification-corrections)
10. [Security and safety observations](#10-security-and-safety-observations)

---

## 1. Conventions and path legend

- **Base URL** = `$IPT_URL` (e.g. `https://ipt.example.org/ipt`, no trailing slash). Credentials only from env: `IPT_USER` (login e-mail), `IPT_PASSWORD`.
- **Action extension**: `struts.action.extension=do,,` → `/resource`, `/resource.do` are identical; `/inventory/dataset` has no `.do`. [SRC `S/struts.properties`]
- **Unknown path** falls back to the namespace's default action (`/foo` → portal `home`, `/manage/foo` → manage `home`, `/admin/foo` → admin `home`). [SRC `default-action-ref` in struts-portal/manage/admin.xml]
- **HTTP methods are not restricted** by Struts config. Only flags/parameters guard mutations (see §10). "GET" below means "read-only, safe"; ⚠️ rows should be called with POST.
- **Paths in "Source" columns**: `S/` = `src/main/resources/`, `J/` = `src/main/java/org/gbif/ipt/`, `W/` = `src/main/webapp/WEB-INF/pages/`.
- **Auth levels** (derived from interceptor stacks in `S/struts.xml`):

| Level | Meaning | Enforced by |
|---|---|---|
| **anon** | no login | `portalStack` (default of namespace `/`) or `json-default` packages (no interceptors at all) |
| **anon + visibility** | anonymous, but PRIVATE/DELETED resources are refused | `portalStack` → `PrivateDeletedResourceInterceptor` (401 for private, 410 for deleted, 404 unknown; managers/admin of the resource pass). `J/struts2/PrivateDeletedResourceInterceptor.java` |
| **mgr** | logged-in user with role `Manager`, `Publisher` or `Admin` (anything except `User`); if `r=` given, must be creator/co-manager of that resource or Admin; 404 if resource unknown, 401 page if not authorised, redirect to `/manage/locked.do` if the resource is being published | `managerStack` → `RequireManagerInterceptor`. `J/struts2/RequireManagerInterceptor.java`, `J/model/User.java` (`hasManagerRights() = role != User`) |
| **publisher** | `Publisher` or `Admin` (registration / DOI rights) | checked inside actions (`User.hasRegistrationRights()`) |
| **admin** | role `Admin` | `adminStack` → `RequireAdminInterceptor` (non-logged-in → redirect `/login.do`; logged-in non-admin → 401) |
| **none-enforced** ⚠️ | action declares `ajaxStack` only, which **replaces** the namespace default stack → no login check | see §10 |

- **Not logged in on a mgr/admin URL**: HTTP 302 → `${baseURL}/login.do` (referer is stored in session and replayed after login). [SRC both interceptors; OBSERVED]
- **Common request parameters** (`J/config/Constants.java`): `r` = resource shortname, `v` = published version (decimal, e.g. `1.3`; invalid → 404), `id` = generic id (source name, rowType URI, user e-mail, org key …), `mid` = mapping index within a rowType, `s` = source name (logs), `request_locale` = UI language.
- **Resource status values** (`J/model/voc/PublicationStatus.java`): `PRIVATE`, `PUBLIC`, `REGISTERED` (registered with GBIF), `DELETED`. **Identifier status**: `UNRESERVED`, `PUBLIC_PENDING_PUBLICATION`, `PUBLIC` (DOI).
- **User roles** (`J/model/User.java`): `User`, `Manager`, `Publisher`, `Admin`.
- **Errors**: 404 (`/WEB-INF/pages/error/404.ftl`), 401, 410, 500 `error.ftl` with HTTP status set. Tomcat answers **400** if query strings contain raw `[` `]` (see §3.3). [SRC `S/struts.xml` global-results; OBSERVED]
- **CORS / cache headers**: `CorsFilter` and `ResponseHeaderFilter` exist but are **not registered** in `web.xml` (only `characterEncodingFilter`, `sanitizeHtmlFilter`, `struts2`). No CORS header is sent by default. [SRC `webapp/WEB-INF/web.xml`; OBSERVED]

---

## 2. Public portal (anonymous)

Namespace `/`, package `portal` (`S/struts-portal.xml`) and the generic actions in `S/struts.xml`. Default stack `portalStack` = resourceSession → setupAndCancel → protectPrivateResource → iptStackWithoutSetup. Before first-run setup is complete, `setupAndCancel` redirects everything to `/setupDataDirectory.do`.

| Path | Method | Auth | Params | Response | Purpose | Mut | Source |
|---|---|---|---|---|---|---|---|
| `/home.do` (also `/`, any unknown path) | GET | anon | `request_locale` | HTML | Public resource table (data loaded by `POST /api/resources`, §3.3) | – | `portal/HomeAction`, `W/portal/home.ftl` |
| `/resource` | GET | anon + visibility | `r`, `v` | HTML (404/401/410 by state) | Resource landing page for a published version (§3.8) | – | `portal/ResourceAction.detail` |
| `/resource/preview.do` | GET | **mgr** | `r` | HTML | Preview of the *next* publication from unpublished `eml.xml` | – | struts-portal.xml (`managerStack` override), `ResourceAction.preview` |
| `/eml.do` | GET | anon + visibility | `r`, `v` | XML `eml-<shortname>[-v<ver>].xml` (`text/xml`) | Published EML (latest version if no `v`) | – | `portal/ResourceFileAction.metadata` |
| `/metadata.do` | GET | anon + visibility | `r`, `v` | same action as `eml.do`; for data packages returns `datapackage-*.json` (`application/json`) or `metadata-*.yaml` (ColDP, `text/yaml`) | Published metadata | – | same |
| `/archive.do` | GET | anon + visibility | `r`, `v` | ZIP `dwca-<shortname>[-v<ver>].zip` (`datapackage-…` for data packages) | Download published archive; 404 if never published; honours `If-Modified-Since` → 304 | – | `ResourceFileAction.archive` |
| `/rtf.do` | GET | anon + visibility | `r`, `v` | `application/rtf` `rtf-<shortname>[-v<ver>].rtf` | Human-readable metadata export | – | `ResourceFileAction.rtf` |
| `/logo.do` | GET | anon + visibility | `r` | image (`jpeg`/`gif`/`png`) | Resource logo | – | `ResourceFileAction.logo` |
| `/appLogo.do` | GET | anon | – | image | Custom IPT logo | – | `portal/AppFileAction` |
| `/publicationlog.do` | GET | anon + visibility | `r` | `text/log` `publication.log` | Log of the **last publication run** — readable anonymously for public resources | – | `ResourceFileAction.publicationLog` |
| `/sourcelog.do` | GET | anon + visibility | `r`, `s` (source name; omitting `s` → NPE/500 [INFERENCE]) | `text/log` `<source>.log` | Per-source log (SQL/file read issues) | – | `ResourceFileAction.sourceLog` |
| `/rss.do` | GET | anon | `r` (optional) | RSS 2.0 XML | Feed of latest published public resources (§3.6) | – | `S/struts.xml` `rss`, `W/portal/rss.ftl` |
| `/dcat.do` (`/dcat`) | GET | anon | – | `text/turtle` | DCAT catalogue of published resources (cached; interval from DCAT settings) | – | `portal/DCATAction`, `task/GenerateDCAT.java`; manual `faq.adoc` |
| `/fallback.do` | GET | anon | – | HTML | Fallback page | – | `portal/FallbackAction` |
| `/about.do` | GET | anon | – | HTML | Version, mode, links | – | `action/AboutAction` |
| `/health.do` | GET | anon (+login for system block) | – | HTML | Health page (§3.5) | – | `S/struts.xml` `health`, `HealthAction` |
| `/login.do` | GET / POST | anon | see §4 | HTML / 302 | Login | ⚠️ (creates session, writes `users.xml` last-login) | `action/LoginAction` |
| `/logout.do` | GET | session | – | 302 → `${baseURL}/` | Clears session | ⚠️ (session only) | `LoginAction.logout` |
| `/account.do`, `/change-password.do` | GET / POST | logged-in user | form fields | HTML / 302 | Own account / password | ⚠️ (POST) | `action/AccountAction` |
| `/setupDataDirectory.do` → `/setupDefaultAdministrator.do` → `/setupMode.do` → `/setupPublicUrl.do` → `/setupInstallationComplete.do` | GET / POST | anon, **only until each wizard step is done** (each step returns SUCCESS/skips once its state exists) | `dataDirPath`; `user.firstname/lastname/email/password`, `password2`, hidden `setupDefaultAdministrator=true`; `modeSelected=Test|Production`; hidden `setupPublicUrl=true`, `baseURL`, `proxy`, `ignoreUserValidation` | HTML / 302 | First-run wizard | ⚠️ (one-shot) | `config/SetupAction` |

Visibility rule for every `anon + visibility` row, with `r` present and no `v`: DELETED resource → 410 unless authorised; latest history entry PRIVATE → 401 unless authorised; with `v`: that version's history entry PRIVATE → 401, DELETED → 410. Authorised = Admin, resource creator, or co-manager with manager role. [SRC `PrivateDeletedResourceInterceptor`; OBSERVED: anonymous `GET /resource?r=<private>` → 401]

Caching: file actions set `Last-Modified` and answer `If-Modified-Since` with the global `304` result. [SRC `ResourceFileAction.execute`]

---

## 3. Machine APIs in depth

All JSON responses use `noCache=true`. None of the four JSON packages below applies `setupAndCancel`/CSRF logic.

### 3.1 `/inventory/dataset` (v1)

- **Auth**: anon. **Method**: GET. **Params**: none. **Source**: `S/struts.xml` package `default` namespace `/inventory`; `J/action/portal/InventoryAction.java`; manual `home.adoc` ("GBIF uses this inventory to monitor … comparing target and indexed record counts").
- **Scope**: only resources with status **REGISTERED** (`resourceManager.list(REGISTERED)`), skipping never-published resources and **data packages** (use v2 for those). Values come from the *reconstructed last published version* (its `eml-<ver>.xml` + version history), not from live edits.
- **Shape** [SRC, confirmed empty shape OBSERVED `{"registeredResources":[]}`]:

```json
{"registeredResources":[
  {"title":"…", "type":"OCCURRENCE", "records":12345, "lastPublished":"2026-03-14",
   "gbifKey":"<uuid>", "eml":"<IPT_URL>/eml.do?r=<shortname>", "dwca":"<IPT_URL>/archive.do?r=<shortname>",
   "version":1.7, "recordsByExtension":{"http://rs.gbif.org/terms/1.0/Multimedia":120}}
]}
```
  `lastPublished` is `yyyy-MM-dd` only; `type` = core type (`OCCURRENCE`, `CHECKLIST`, `SAMPLINGEVENT`, `METADATA`…); `version` is a decimal number; `recordsByExtension` = rowType → count (empty map if none). Null properties are **not** excluded in v1 (title can be `null`).
- **Not included**: next publication date, public-but-unregistered resources, private resources.

### 3.2 `/inventory/v2/dataset`

- **Auth**: anon. **Method**: GET. **Source**: `S/struts.xml` package `inventory-v2`; `J/action/portal/InventoryV2Action.java`. `excludeNullProperties=true`.
- **Query params** (both optional, all case-insensitive):
  - `status` = `private|public|registered|deleted` → `resourceManager.list(status)` (**live status**, so `status=private` lists private resources that were published before — it is anonymous!). Unknown value → ignored (falls back to default).
  - default (no/invalid `status`) = `listPublishedPublicVersions()`: resources whose latest version history entry is not DELETED/PRIVATE and has a release date (plus pre-2.2 registered ones).
  - `type` = `dwca` | `camtrap` (`camtrapdp`, `camtrap-dp`) | `coldp` | `datapackage` (camtrap-dp or coldp).
- Resources never published are skipped.
- **Shape**:

```json
{"resources":[
 {"id":"<shortname>", "gbifKey":"<uuid, omitted if unregistered>", "title":"…",
  "format":"DWCA|METADATA|CAMTRAP_DP|COLDP", "version":1.7, "lastPublished":"2026-03-14", "records":12345,
  "archive":[{"type":"DWCA|CAMTRAP_DP|COLDP","url":"<IPT_URL>/archive.do?r=<shortname>"}],
  "metadata":[{"type":"EML|FRICTIONLESS","url":"<IPT_URL>/eml.do?r=<shortname>"}],
  "additionalProperties":{"recordsByExtension":{"<rowType>":N},"core":"occurrence"}}
]}
```
  - `METADATA` resources have `archive: []` (no archive). Data packages: `additionalProperties` = `{"recordsByTable":{…}}` and `metadata[].url` points to `metadata.do?r=…` (`getResourceDataPackageMetadataUrl`).
  - `records` = `recordsPublished` of the last published version; `lastPublished` is `yyyy-MM-dd`.
- OBSERVED (empty IPT): `{"resources":[]}`.
- **Does not contain**: next publication date (use §3.3), overdue flag, publication failures.

### 3.3 `/api/resources` and `/manager-api/resources` (DataTables)

| | `/api/resources` | `/manager-api/resources` |
|---|---|---|
| Auth | anon | **mgr** (OBSERVED: anonymous → 302 `/login.do`) |
| Rows | resources whose latest version is not PRIVATE/DELETED **and** was released (`publishedPublicVersionsSimplified`); values reconstructed from **last published version** (title, status, records, org, logo, subject) but **live** `modified`, `nextPublished`, `coreType`, `subtype`, `creatorName` | **all** resources the user may manage (Admin = all; Manager = created or co-managed), from **live** state, includes PRIVATE, DELETED, never-published; `pendingStatus` overrides the status badge |
| Source | `portal/HomeAction` → `ResourceManagerImpl.listPublishedPublicVersionsSimplified` | `manage/HomeAction` → `ResourceManagerImpl.list(User, DatatableRequest)` |

Both: package `ipt-api` / `ipt-manager-api`, JSON `root=resources`. The UI posts `type: 'POST'` (`W/macros/resourcesTable.ftl`), but GET with the same parameters also works [OBSERVED].

**Request parameters** (`J/config/Constants.java` `DATATABLE_*`; `J/model/datatable/DatatableRequest.java` defaults):

| Param | Default if absent | Meaning |
|---|---|---|
| `start` | 0 | offset |
| `length` | **10** | page size → send `10000` to get everything |
| `search[value]` | "" | case-insensitive substring over shortname, title, organisation alias/name, core type, subtype, creator name, subject |
| `order[0][column]` | 1 | sort column index (see below) |
| `order[0][dir]` | `asc` | `asc`/`desc` |
| `draw` | – | ignored by the server (not echoed back) |

⚠️ **Gotcha [OBSERVED]**: with GET, unencoded brackets (`order[0][column]`) are rejected by Tomcat with **400**; URL-encode as `order%5B0%5D%5Bcolumn%5D=11`. With a form-encoded POST body no problem.

Sorting maps: 1 title, 2 organisation, 3 core type, 4 subtype, 5 records (tie-break last published), 6 modified, 7 last published, 8 next published, 9 status, 10 creator; any other index (0, 11, 12) sorts by **shortname**. [SRC `ResourceManagerImpl.resourceComparator`]

**Response shape** [SRC `DatatableResult`; OBSERVED]:

```json
{"aaData":[[ "<13 strings>" ]], "iTotalDisplayRecords": <filtered count>, "iTotalRecords": <total count>}
```
`iTotalRecords` ignores the search; `iTotalDisplayRecords` respects it. Every cell is a **string, many contain HTML** (strip tags). `ResourceManagerImpl.toDatatableResourcePortalView / toDatatableResourceManageView` ("BEWARE! Order is crucial"):

| Idx | Content (public view) | Manage view differences / parsing hint |
|---|---|---|
| 0 | `<img class="resourceminilogo" src="…"/>` or `<span>--</span>` | same |
| 1 | `<a class="resource-table-link" href='<IPT_URL>/resource?r=<shortname>'>Title (HTML-escaped)</a>`; title falls back to shortname | href is `<IPT_URL>/manage/resource?r=<shortname>`; title is the **live** title |
| 2 | organisation alias or name (HTML-escaped) or `--` (also for "No organisation") | same |
| 3 | `<span class="… type-<coretype>">Localised type</span>` or `<span>--</span>` | same |
| 4 | subtype badge or `<span>--</span>` | same |
| 5 | `<a class="resource-table-link" href='…/resource?r=<sn>#anchor-dataRecords'>1,234</a>` (locale-formatted) or `<span>--</span>` when never published and 0 records | strip non-digits to get the number |
| 6 | **modified** `yyyy-MM-dd HH:mm:ss` (server JVM timezone) | same |
| 7 | **last published** `yyyy-MM-dd HH:mm:ss` or `<span>--</span>` | same |
| 8 | **next publication** `yyyy-MM-dd HH:mm:ss`, `<span>--</span>` if none; **overdue** (date before server "now") is wrapped `<span class="text-gbif-danger">yyyy-MM-dd HH:mm:ss</span>` | same. Overdue ⇒ auto-publication failed/suspended. |
| 9 | status badge `<span class="text-nowrap status-pill … status-<private\|public\|registered\|deleted>">…<span>Localised label</span></span>` | `pendingStatus` (visibility change scheduled for next publication) replaces status |
| 10 | creator name (HTML-escaped) | same |
| 11 | **shortname** (plain text, not escaped) | same |
| 12 | subject/keywords (escaped) or "" | same |

Parsing recipes: shortname = `row[11]`; status = regex `status-(\w+)`; overdue = `'text-gbif-danger' in row[8]`; dates = `re.search(r'\d{4}-\d\d-\d\d \d\d:\d\d:\d\d', cell)`.

Related `/manager-api` actions (mgr, GET, JSON): `suggest-resources` (root `suggestedResources`), `suggest-agents?r=<shortname>&type=<agentType>` (root `suggestedAgents`) — metadata-form helpers, not needed for health checks. [SRC `S/struts-manage.xml`, `manage/MetadataAgentSuggesterAction`]

### 3.4 `/admin-api/publication-report(s)` (publishing status API)

- **Auth**: **admin** (`adminStack`, OBSERVED: anonymous → 302 login). **Method**: GET. **Source**: `S/struts-admin.xml` package `ipt-admin-api`; `J/action/admin/PublishingStatusApiAction.java`. Not in the runbook; this is the only JSON view of running/finished publication jobs. Reports are the in-memory `ResourceManager.getProcessReports()` — **lost on IPT restart**, cleared by `admin/bulk-publication.do`/`publishAll.do`.
- `GET /admin-api/publication-report?r=<shortname>` → JSON root `report` = one `StatusReport` or `null` (OBSERVED `null` when none).
- `GET /admin-api/publication-reports[?status=running|completed][&since=<epoch-ms>]` → JSON root `reports` = map `shortname → StatusReport` (OBSERVED `{}` when none). `status=running` → not completed; `status=completed` → completed **and** `timestamp > since`; no `status` → all.
- **`StatusReport`** (`J/task/StatusReport.java`, Lombok `@Getter` → JSON getters) [SRC; field list, exact serialisation of `exception` not run → INFERENCE]:

| Field | Type | Meaning |
|---|---|---|
| `completed` | bool | job finished (success **or** failure) |
| `state` | string | human status text (HTML possible; e.g. cancelled state message) |
| `timestamp` | long (epoch ms) | creation time of this report object |
| `messages` | list of `{level, message, timestamp, date}` | log4j2 level (`INFO`/`WARN`/`ERROR`…) per step |
| `exceptionMessage` | string/null | failure message (non-null ⇒ failed) |
| `exceptionStacktrace` | list of strings | stack trace lines (empty if OK) |
| `exception` | object/null | serialised throwable (may be bulky) |

  Failed = `completed && exceptionMessage != null`. Running = `!completed`.
- HTML twin for managers (own jobs): `/manage/report.do?r=` (§5). Admin HTML twin: `/admin/bulkReport.do`.

### 3.5 `/api/health` and `/health.do`

| | `/api/health` | `/health.do` |
|---|---|---|
| Auth | **anon** [OBSERVED] | anon for network/disk/permissions; **OS, Java, app-server, IPT mode block needs login** (`loggedIn` flag in `W/health.ftl`: shows "Please log in for more details") [SRC+OBSERVED] |
| Response | JSON `{"status":{…}}` | HTML tables |
| Source | `S/struts.xml` package `ipt-api`, `J/action/HealthAction.java` | `S/struts.xml` `health` (`healthAction` prototype bean), `W/health.ftl` |

JSON keys (all of them; the system block is **not** in the JSON) — OBSERVED output on 3.3.6:
`networkRegistry` (bool: HTTP 200 from `cfg.getRegistryUrl()` — `https://gbrds.gbif.org` production / `https://gbrds.gbif-uat.org` test), `networkRegistryURL`, `networkRepository` (bool: HTTP 200 from `http://rs.gbif.org`), `networkRepositoryURL`, `networkPublicAccess` (bool: base URL is reachable from the Internet **as judged by `https://tools.gbif.org/ws-validurl/?url=<baseURL>`** → `{"success":true}`), `networkPublicAccessURL`, `diskTotal`, `diskUsed`, `diskFree` (bytes of the data-dir volume), `diskUsedRatio` (int %; page turns red above **80**), `readConfigDir`, `readLogDir`, `writeLogDir`, `readTmpDir`, `writeTmpDir`, `readResourcesDir`, `writeResourcesDir`, `readSubResourcesDir`, `writeSubResourcesDir` (bools, tested on `config/`, `logs/`, `tmp/`, `resources/` and every `resources/<shortname>/`).

Interpretation notes: `networkPublicAccess=false` is expected for localhost/private base URLs, and also appears when `tools.gbif.org` is unreachable or when the volume is full ([issue #2390](https://github.com/gbif/ipt/issues/2390): all checks Failed because the disk was 100 % full). Each call performs 3 outbound HTTP requests (slow, ~1–5 s) — do not poll it.

### 3.6 RSS `/rss.do`

- **Auth**: anon. **Params**: `r=<shortname>` optional (one item; empty if that resource is not PUBLIC/REGISTERED; unknown shortname → NPE/500 [INFERENCE `ResourceAction.rss`]). Without `r`: all resources whose last published version is not PRIVATE/DELETED, newest `modified` first (the code requests page size 25 but `latest()` returns the whole sorted list — [INFERENCE]). **Source**: `S/struts.xml` `rss`, `ResourceAction.rss`, `service/manage/impl/ResourceManagerImpl.latest`, `W/portal/rss.ftl`.
- **Shape** [SRC `rss.ftl`; OBSERVED 523 B on empty IPT]: `<rss version="2.0" xmlns:ipt="http://ipt.gbif.org/" xmlns:atom=… xmlns:geo=…><channel>` with `title`, `link`, `atom:link rel=self`, `pubDate` (IPT creation), `lastBuildDate` (modified of first resource), `ipt:identifier` (IPT UUID = GBIF installation key), `generator` ("GBIF IPT <version>"), `webMaster`, `ttl 15`, optional `geo:Point`; per resource `<item>` with `title`, `link` (`/resource?r=`), `description` (change summary or description), `author`, `pubDate` (last published), `ipt:eml`/`ipt:dwca` (or `ipt:metadata`/`ipt:archive` for data packages), `guid`.
- The GBIF registry stores this URL as the installation's `FEED` endpoint, e.g. `https://<ipt>/rss.do` [OBSERVED on live GBIF installation].

### 3.7 Files: `archive.do`, `eml.do`, `metadata.do`, `rtf.do`, logs, `dcat`

See §2 table for exact names. Practical points:
- Without `v` the **latest published** version is served; `v=` selects archived versions that still exist on disk (`dwca-<ver>.zip`, `eml-<ver>.xml`, `<shortname>-<ver>.rtf`; see §8). ⚠️ `deleteVersion.do` removes them.
- A file missing on disk although version history lists it → **404** (`Data dir file not found` in the debug log) even for a public resource: a typical "published but broken" symptom. [SRC `ResourceFileAction.execute`]
- `eml.do?r=` / `archive.do?r=` are precisely the URLs the GBIF registry stores as dataset endpoints (`EML`, `DWC_ARCHIVE`) [OBSERVED live dataset endpoints; SRC `RegistryManagerImpl.serviceURLs` built from `cfg.getResourceEmlUrl` / `getResourceArchiveUrl`], so `HEAD`/`GET` on them reproduces what GBIF's crawler sees.
- `/publicationlog.do?r=` is the quickest anonymous way to read the last publication log (equivalent file: `resources/<shortname>/publication.log`).
- `/dcat` output is cached for the interval in DCAT settings (`GenerateDCAT.getFeed`).

### 3.8 Resource page `/resource`

`/resource?r=<shortname>[&v=<version>]`. HTML. For anonymous users: shows `v` or the latest **public** version; if none → 401 (`NOT_ALLOWED`); private/deleted requested versions → 401/410; an unknown `r` → 404; metadata file missing on disk → 404; EML unparsable → 500. Managers see the latest version regardless of visibility (with a warning banner). When `v` is not the latest, a "not latest" warning is added. [SRC `ResourceAction.detail`; OBSERVED 401 for private resource]. Version history, download links (`archive.do`, `eml.do`, `rtf.do`, `publicationlog.do`), GBIF key and DOI are in the rendered HTML (`W/portal/resource.ftl`).

---

## 4. Login, session, CSRF (scripted access)

**Flow** (`J/action/LoginAction.java`, `J/struts2/CsrfLoginInterceptor.java`, `W/login.ftl`; all steps [OBSERVED] on 3.3.6):

1. `GET <IPT_URL>/login.do` → `200`, `Set-Cookie: JSESSIONID=…; Path=/; HttpOnly` and `Set-Cookie: CSRFtoken=<32 alnum chars>; HttpOnly` (Max-Age **900 s**; `Path` = path of configured base URL, `Domain` = host of **configured** base URL, `Secure` if base URL is https). The body contains `<input type="hidden" name="csrfToken" value="<same token>">`.
2. `POST <IPT_URL>/login.do`, `Content-Type: application/x-www-form-urlencoded`, **same cookies**, fields:

| Field | Value |
|---|---|
| `csrfToken` | token from the form (must equal the `CSRFtoken` cookie) |
| `email` | `$IPT_USER` (the user's e-mail; trimmed) |
| `password` | `$IPT_PASSWORD` (trimmed) |
| `login` | optional submit button value |

3. **Success** → `302`, `Location: <baseURL>/` (or the originally requested manage/admin page, remembered in session). Keep `JSESSIONID`; the same id stays valid (not rotated). Session lifetime: `req.getSession().setMaxInactiveInterval(cfg.getSessionTimeout())`, where `AppConfig.getSessionTimeout()` = `session.timeout` (from `config/ipt.properties`) **× 60**; default file ships `session.timeout=3600` with the comment "in seconds" — code multiplies by 60 (i.e. treats it as minutes) [SRC `AppConfig.java:276-283`, `S/configDefault/ipt.properties:26-27`; effective value not measured].
4. **Failure detection**:
   - wrong e-mail/password → `200` + login page containing the action error *"The email – password combination does not exist."* (i18n `admin.user.wrong.email.password.combination`; language follows `request_locale`) — **no 302**.
   - missing/mismatched CSRF token or missing `CSRFtoken` cookie → `200` login page **without** any message (only `WARN CSRF login token wrong!` in `logs/debug.log`/`admin.log`).
   - login after success always needs `userManager.save()` (writes `config/users.xml` with last-login) → a full disk makes login fail with a 500 ([issue #2391](https://github.com/gbif/ipt/issues/2391), stack trace in `XStream … QuickWriter.flush`).
   - Simplest robust test: `status == 302` and `Location` not ending in `login.do`; then `GET /manage/home.do` must return 200 (not 302 → login).
5. **Cookie-domain trap**: the CSRF cookie is created with `Domain=<host of the *configured* ipt.baseURL>`. Calling the IPT through a different host name (internal IP, container port mapping, reverse-proxy alias) can make strict cookie jars drop it → login silently returns 200. Send `Cookie:` headers manually or call the configured public URL. [SRC + OBSERVED with Python `http.cookiejar`, which rejected the cookie once base URL was `http://localhost:8080` but the call went to `localhost:18080`.]
6. **Logout**: `GET /logout.do` → `302 Location: <baseURL>/`, session cleared. Afterwards `/manage/home.do` → 302 `/login.do`. [OBSERVED]

**CSRF for other POSTs**: **none**. The interceptor stacks (`iptStackWithoutSetup`: keepRedirectMessages, defaultLocale, i18n, defaultStack, xssFieldError, validation, csrfLoginInterceptor, workflow) contain no Struts `token`/`tokenSession` interceptor and no `X-CSRF` header handling; `CsrfLoginInterceptor` only guards the login form (it re-issues a fresh `CSRFtoken` cookie on **every** request while not logged in). So manage/admin POSTs need only the `JSESSIONID` cookie. [SRC `S/struts.xml`, `J/struts2/*`; OBSERVED: a `GET` with `deleteFlag=Delete` deleted a resource, §10.] Consequences: (a) scripted writes are simple; (b) the IPT is CSRF-able — hence "state transition" parameters (`publish`, `unpublish`, `deleteFlag`, …) are the only guard.

**Minimal stdlib login (Python ≥3.9, placeholders only)**

```python
import os, re, urllib.parse, urllib.request

BASE = os.environ["IPT_URL"].rstrip("/")
cookies = {}

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None  # keep 302s visible

_opener = urllib.request.build_opener(_NoRedirect)

def call(path, form=None):
    data = urllib.parse.urlencode(form).encode() if form is not None else None
    req = urllib.request.Request(BASE + path, data=data)
    if cookies:
        req.add_header("Cookie", "; ".join(f"{k}={v}" for k, v in cookies.items()))
    try:
        resp = _opener.open(req, timeout=60)
    except urllib.error.HTTPError as e:  # 3xx/4xx/5xx arrive here
        resp = e
    for sc in resp.headers.get_all("Set-Cookie") or []:
        name, _, rest = sc.partition("=")
        cookies[name] = rest.split(";")[0]
    return resp.status, resp.headers, resp.read().decode("utf-8", "replace")

def login():
    _, _, html = call("/login.do")
    token = re.search(r'name="csrfToken" value="([^"]*)"', html).group(1)
    st, hdr, _ = call("/login.do", {"csrfToken": token, "email": os.environ["IPT_USER"],
                                    "password": os.environ["IPT_PASSWORD"], "login": "Login"})
    return st == 302 and not (hdr.get("Location") or "").endswith("login.do")
```

---

## 5. Manage section (manager role)

Namespace `/manage` (`S/struts-manage.xml`), default stack `managerStack` = resourceSession (stores `r` in session) → setupAndCancel → iptStackWithoutSetup → requireManager. Common to all rows: **mgr**; with `r=` a 404/401/redirect-to-locked can occur as described in §1. After a successful mutation most actions redirect (302) to `/manage/resource.do?r=<shortname>`.

A resource being published is **locked**: any `managerStack` URL with that `r` redirects to `/manage/locked.do` (page that polls `report.do` every second and offers cancel). Use `report.do` (below), not `resource.do`, to follow a running job. [SRC `RequireManagerInterceptor` + `W/manage/locked.ftl`]

### 5.1 Read-only (safe for monitoring)

| Path | Method | Params | Response | Purpose | Source |
|---|---|---|---|---|---|
| `/manage/` , `/manage/home.do` | GET | – | HTML | Manager home (resource table fed by `POST /manager-api/resources`) | `manage/HomeAction` |
| `/manage/resource.do` | GET | `r` | HTML (141 KB) | **Overview page**: metadata/mapping/source status, publish button, version history, auto-publish state, DOI/registration state, manager list | `manage/OverviewAction`, `W/manage/overview.ftl` |
| `/manage/report.do` | GET | `r` | HTML fragment (≈0.3 KB) "Publishing Status" | **Last/current publication status**: `In Progress` (spinner, with cancel hint) / `Completed` (green) / `Failed` (red) + `report.state` + link to `publicationlog.do`; empty if the IPT has no report in memory (after restart) — OBSERVED fragment with "Finished" and `resource overview` link for a never-published resource. i18n keys: `admin.config.publish.inProgress/failed/completed` | struts-manage.xml (`ajaxStack`), `W/manage/report.ftl` |
| `/manage/locked.do` | GET | `r` | HTML | Shown while resource is locked | `OverviewAction.locked` |
| `/manage/mappingPeek.do` | GET | `r`, `id` (rowType **URI**, e.g. `http://rs.tdwg.org/dwc/terms/Occurrence`), `mid` (0-based mapping index) | HTML table (`peek.ftl`) of the first **100 rows** (`PEEK_ROWS`) as the DwC-A generator would write them; errors in `report.messages` | Tests the SQL/file source + mapping **without publishing** (does run the SQL against the source DB, writes a temp file under `tmp/`) | `OverviewAction.peek`, `W/manage/peek.ftl`. OBSERVED: for a non-existent mapping → HTTP 500 error page |
| `/manage/peek.do` | GET | `r`, `id` (source name) | HTML table | Preview of a **source** (first rows) | `SourceAction.peek`; OBSERVED 404 "source cannot be loaded" for unknown source |
| `/manage/source.do` | GET | `r`, `id` (source name) | HTML form | Shows source type, and for SQL sources `rdbms`, `sqlSource.host`, `sqlSource.database`, `sqlSource.username`, `sqlSource.sql` (password field present but not echoed unless cached); for files: delimiter, encoding, header lines, date format | `SourceAction`, `W/manage/source.ftl` |
| `/manage/raw-source.do` | GET | `r`, `id` (source name) | file download (`application/octet-stream`, `<id><suffix>`) | Original uploaded file of a file source (404 for SQL/URL sources) | `portal/ResourceFileAction.rawsource` |
| `/manage/mapping.do` | GET | `r`, `id` (rowType), `mid`, `source` | HTML | Mapping editor (view) | `MappingAction` |
| `/manage/translation.do` | GET | `r`, `mid`, `rowType`, `term` | HTML | Value-translation table of a mapped term | `TranslationAction` |
| `/manage/metadata-<section>.do` | GET | `r` | HTML form | EML section view. Sections (template names): `basic`, `contacts`, `geocoverage`, `taxcoverage`, `tempcoverage`, `keywords`, `project`, `methods`, `citations`, `collections`, `physical`, `additional`, `acknowledgements`, `additionalDescription` | `manage/MetadataAction`, `W/manage/eml/*.ftl` |
| `/manage/camtrap-metadata-<section>.do`, `/manage/datapackage-metadata-<section>.do` | GET | `r` | HTML form | Data-package metadata sections (camtrap: basic, citation, geographic, keywords, other, project, taxonomic, temporal; frictionless: basic) | `CamtrapMetadataAction`, `DataPackageMetadataAction` |
| `/manage/auto-publish.do` | GET | `r` | HTML form | Auto-publication configuration (view) | `AutoPublishAction` |
| `/manage/publication-settings.do` | GET | `r` | HTML form | Publishing organisation, etc. (view) | `PublicationSettingsAction` |
| `/manage/history.do` | GET | `r`, `v` | HTML | Version history / change summary editor (view) | `VersionHistoryAction` |
| `/manage/detail.do` | GET | `r`, `v` | HTML | Manager view of a published version (data-package aware) | `portal/ResourceAction.detail` (OBSERVED 500 for never-published resource) |
| `/manage/eml.do` | GET | `r`, `v` | XML | Same file as public `eml.do` (no visibility filter) | `manage/ResourceFileAction` |
| `/manage/vocabulary.do` | GET | `id` | HTML | Vocabulary term list | `admin/VocabulariesAction` |
| `/manage/urlMetadata.do` | GET | `url` | JSON `{"status","contentType","contentLength","lastModified","acceptRanges"}` (400 if `url` missing) | Server-side HEAD of a URL (used by URL-source form). Causes outbound request from the IPT host | `manage/UrlMetadataAction` |

### 5.2 Mutating (⚠️) — use POST, never in health checks

All use `managerStack` unless noted; they only act when the state-transition parameter is present (the flag value is irrelevant, just non-blank). Success → 302 to `/manage/resource.do?r=<shortname>`.

| Path | Params (besides `r`) | Effect | Source |
|---|---|---|---|
| ⚠️ `/manage/publish.do` | `publish=Publish` (flag), optional `summary` (change summary) | **Starts publication** (new version, writes DwC-A/EML/RTF, registry update, DOI ops if configured). Refused/INPUT if: registered resource without GBIF-supported licence; DOI operations without DOI account; invalid metadata. Clears auto-publish failure counter. Redirects to `locked.ftl` while running | `OverviewAction.publish`; button forms in `W/macros/manage/publish.ftl` |
| ⚠️ `/manage/cancel.do` | – (GET link in the locked page) | **Cancels the running publication** and rolls the version back. **No login enforced** (§10) | `OverviewAction.cancel`, struts-manage.xml (`ajaxStack`) |
| ⚠️ `/manage/create.do` | `shortname`, `resourceType` (core/type id), optional `importDwca`, `file` (multipart) | Create resource (or import archive) | `CreateResourceAction` |
| ⚠️ `/manage/resource-delete.do` | `r`, `deleteFlag` | Delete resource from IPT **and deregister from GBIF** (`DELETE …/registry/ipt/resource/<key>`) | `OverviewAction.delete` |
| ⚠️ `/manage/resource-deleteFromIpt.do` | `r`, `deleteFlag` | Delete from IPT only. **OBSERVED: works with GET** | `OverviewAction.deleteFromIpt` |
| ⚠️ `/manage/resource-undelete.do` | `r`, `undelete` | Undelete | `OverviewAction.undelete` |
| ⚠️ `/manage/resource-makePrivate.do` | `r`, `unpublish` | PUBLIC → PRIVATE (refused if DOI assigned or registered) | `OverviewAction.makePrivate` |
| ⚠️ `/manage/resource-makePublic.do` | `r`, optional `makePublicDateTime` | PRIVATE → PUBLIC (immediately or scheduled) | `OverviewAction.makePublic` |
| ⚠️ `/manage/resource-cancelVisibilityChange.do` | `r` | Cancel pending visibility change | `OverviewAction.cancelVisibilityChange` |
| ⚠️ `/manage/resource-registerResource.do` | `r` | **Register resource with GBIF** (publisher role; resource must be PUBLIC, published once, valid org) → `POST …/registry/ipt/resource` | `OverviewAction.registerResource` |
| ⚠️ `/manage/resource-reserveDoi.do`, `resource-deleteDoi.do` | `r`, `reserveDoi` / `deleteDoi` | Reserve / delete a DOI at the DOI agency | `OverviewAction` |
| ⚠️ `/manage/resource-addManager.do`, `resource-deleteManager.do` | `r`, `id` (user e-mail) | Add/remove co-manager | `OverviewAction` |
| ⚠️ `/manage/resource-addNetwork.do`, `resource-deleteNetwork.do` | `r`, `id` (network UUID) | Add/remove GBIF network membership (`POST/DELETE …/registry/resource/<key>/network/<net>`) | `OverviewAction` |
| ⚠️ `/manage/resource-changePublishingOrganization.do` | `r`, `id` (organisation key) | Move registered resource to another organisation | `OverviewAction` |
| ⚠️ `/manage/replace-eml.do`, `replace-datapackage-metadata.do` | `r`, multipart file | Replace metadata file | `OverviewAction.replaceEml` |
| ⚠️ `/manage/publication-settings.do` (POST) | `r`, `id` (org key), `save` | Save publication settings | `PublicationSettingsAction` |
| ⚠️ `/manage/auto-publish.do` (POST) | `r`, `updateFrequency`, `updateFrequencyMonth`, `updateFrequencyBiMonth`, `updateFrequencyDay`, `updateFrequencyDayOfWeek`, `updateFrequencyTime`, `skipUnchanged`, `skipDrop`, `recordsDropThreshold`, `notifyPublicationFailure`, `failureEmails` | Set auto-publication schedule/guards (changes `nextPublished`) | `AutoPublishAction`, `Constants.REQ_PARAM_AUTO_PUBLISH_*` |
| ⚠️ `/manage/metadata-<section>.do` (POST) | form fields `eml.*`, `r` | Save EML section; `reinferMetadata` param re-infers | `MetadataAction` |
| ⚠️ `/manage/history.do` (POST) | `r`, `v`, `summary` | Edit change summary of a version | `VersionHistoryAction` |
| ⚠️ `/manage/addsource.do` | `r`, `sourceType`, `url`/`file`/SQL fields, `sourceName` | Add source (file upload, URL, SQL) | `SourceAction.add` |
| ⚠️ `/manage/source.do` (POST) | `r`, `id`, `source.*`, `sqlSource.*`, `sqlSourcePassword`, `rdbms`, `analyze`, `deleteFlag` | Edit/re-analyze/delete a source | `SourceAction` |
| ⚠️ `/manage/delete-source.do` | `r`, `id` | Delete source | `SourceAction.delete` |
| ⚠️ `/manage/canceloverwrite.do` | `r` | Cancel a pending source overwrite | `SourceAction.cancelOverwrite` |
| ⚠️ `/manage/mapping.do` (POST), `dataPackageMapping.do`, `dataPackageMappingSourceNew/Create.do` | `r`, `id`, `mid`, `source`, `fields[*]` | Create/save mappings | `MappingAction`, `DataPackageMappingAction` |
| ⚠️ `/manage/delete-mapping.do`, `deleteDataPackageMapping.do` | `r`, `id`, `mid` | Delete mapping | same |
| ⚠️ `/manage/translation.do` (POST), `translationReload.do`, `translationAutomap.do`, `dataPackageFieldTranslation*.do` | `r`, `mid`, `rowType`, `term`, `tmap` | Save/reload/auto-map value translations | `TranslationAction`, `DataPackageFieldTranslationAction` |
| ⚠️ `/manage/uploadlogo.do` | `r`, file, `removeLogo` | Resource logo | `MetadataAction.uploadLogo` |

---

## 6. Admin section (admin role)

Namespace `/admin` and `/admin-api` (`S/struts-admin.xml`), stack `adminStack` (setupAndCancel → iptStackWithoutSetup → requireAdmin). Not logged in → 302 login; logged-in non-admin → 401.

### 6.1 Read-only

| Path | Method | Params | Response | Purpose | Source |
|---|---|---|---|---|---|
| `/admin/`, `/admin/home.do` | GET | – | HTML | Admin dashboard (registration status, counts) | `admin/HomeAction` |
| `/admin/logs.do` | GET | – | HTML | Log viewer page (loads `logfile.do?log=admin` via AJAX, links the debug log) | `LogsAction`, `W/admin/logs.ftl` |
| `/admin/logfile.do` | GET | `log` = `admin` or `debug` | `text/plain` UTF-8 | **Full log file**: `<datadir>/logs/<log>.log`. `admin` = WARN+ of `org.gbif`; `debug` = everything (root DEBUG). Only these two live files — rolled files `*.log.N` cannot be fetched. File must be a direct child of `logs/` (path traversal blocked) → else 404 | `LogsAction.logfile`, `config/LoggingConfiguration.java` (10 MB size rollover + roll on startup) |
| `/admin/config.do` | GET | – | HTML | Server config (base URL, proxy, SMTP, archival, debug flag, session…) | `ConfigAction` |
| `/admin/users.do` | GET | – | HTML | User list | `UserAccountsAction.list` |
| `/admin/user.do` | GET | `id` (e-mail) | HTML | User form | `UserAccountsAction` |
| `/admin/extensions.do`, `/admin/extension.do` | GET | `id` (rowType) | HTML | Installed extensions, details, whether updates exist | `ExtensionsAction` |
| `/admin/vocabulary.do` | GET | `id` | HTML | Vocabulary details | `VocabulariesAction` |
| `/admin/dataPackages.do`, `/admin/dataPackage.do` | GET | `id` | HTML | Installed data package schemas | `DataPackageSchemaAction` |
| `/admin/organisations.do`, `/admin/organisation.do` | GET | `id` (org UUID) | HTML | Organisations associated to this IPT | `OrganisationsAction` |
| `/admin/registration.do` | GET | – | HTML | GBIF registration form/state | `RegistrationAction` |
| `/admin/uiManagement.do` | GET | – | HTML | UI customisation | `UIManagementAction` |
| `/admin/bulk-publication.do` | GET | – | HTML | Bulk publication page; **clears the in-memory process reports** | `BulkPublicationAction` |
| `/admin/bulkReport.do` | GET | – | HTML fragment (running/completed publications) | Poll target of bulk publication (`ajaxStack`, no auth, §10) | `PublishingStatusAction` |
| `/admin-api/publication-report`, `/admin-api/publication-reports` | GET | see §3.4 | JSON | Publishing status API | `PublishingStatusApiAction` |

### 6.2 Mutating (⚠️)

| Path | Params | Effect | Source |
|---|---|---|---|
| ⚠️ `/admin/publishAll.do` | `publishMode` (`SELECTED`/`EXCLUDED`/`CHANGED`/else all), `selectedResources`, `excludedResources` (shortnames) | **Publishes every resource** (first updates the IPT's own registry entry and all registered resources' metadata at GBIF). Runs on **GET** too (no POST check; OBSERVED 200 on test container) | `PublishAllResourcesAction` |
| ⚠️ `/admin/deleteVersion.do` | `r`, `v` | Removes one archived version (files + history). `execute()` overrides `POSTAction` and runs on GET; redirects to `${baseURL}/resource` | `DeleteVersionAction` |
| ⚠️ `/admin/config.do` (POST) | `baseUrl`, `proxy`, `logoRedirectUrl`, `latitude`, `longitude`, `adminEmail`, `mailSmtp*`, `analyticsKey`, `archivalMode`, `archivalLimit`, `debug`, `defaultLocale` | Save `config/ipt.properties`. OBSERVED: success → 302 to **`<new baseUrl>/home.do`** | `ConfigAction` |
| ⚠️ `/admin/user.do` (POST), delete via `deleteFlag` | `user.*`, `resetPassword`, `password` | Create/edit/delete user, roles | `UserAccountsAction` |
| ⚠️ `/admin/updateExtension.do`, `/admin/extension.do` (POST), `extensions.do` | `id`, `url`, `synchronise` | Install/update/delete extension | `ExtensionsAction` |
| ⚠️ `/admin/updateDataPackage.do`, `/admin/dataPackage.do` (POST) | `id` | Install/update/delete schema | `DataPackageSchemaAction` |
| ⚠️ `/admin/registration.do`, `updateRegistration.do`, `changeTokens.do`, `associateWithNetwork.do` | `registeredIptPassword`, `hostingOrganisationToken`, `tokenChange`, `networkKey`, `applyToExistingResources`, org fields | **Register this IPT with GBIF**, update its registry record, rotate tokens | `RegistrationAction` (→ `POST …/registry/ipt/register`, `…/ipt/update/<iptKey>`) |
| ⚠️ `/admin/organisation.do` (POST), `organisationsSynchronize.do` | `id`, org key, password/token | Add/delete organisation; re-sync names from registry | `OrganisationsAction` |
| ⚠️ `/admin/uiManagement.do` (POST), `appLogoUpload.do` | file, `removeLogo` | UI customisation | `UIManagementAction` |

---

## 7. GBIF registry and API endpoints

### 7.1 What the IPT itself calls (legacy "GBRDS" registry API)

Base = `cfg.getRegistryUrl()`: **production `https://gbrds.gbif.org`**, **test `https://gbrds.gbif-uat.org`**. Which one is used is fixed per data dir by `config/.gbifreg` (content `PRODUCTION` or `DEVELOPMENT`, written when the mode is chosen; IPT refuses to switch afterwards — `AppConfig.setRegistryType`). Registry writes use HTTP Basic with the organisation key + organisation token/password (IPT: `ipt key` + its own password) — **never put these in notes or logs**. [SRC `J/service/registry/impl/RegistryManagerImpl.java`, `J/config/AppConfig.java`, `S/application.properties`]

| Registry URL (under base) | Verb | IPT use | Mut | Verified |
|---|---|---|---|---|
| `/registry/organisation.json` | GET | List registrable organisations | – | [OBSERVED 200 JSON `[{key,name}]`] |
| `/registry/organisation/<orgKey>.json` | GET | One organisation | – | [OBSERVED] |
| `/registry/organisation/<orgKey>?op=login` | GET + Basic(orgKey, token) | Validate organisation credentials | – (auth check) | [SRC] |
| `/registry/resource.json?organisationKey=<orgKey>` | GET (code marks it `@Deprecated`) | Datasets of an organisation | – | [OBSERVED 200] |
| `/registry/resource/<datasetKey>/belongs/organisation/<orgKey>` | GET | Ownership check | – | [SRC] |
| `/registry/network.json`, `/registry/resource/<key>/networks` | GET | Networks | – | [OBSERVED 200] |
| `/registry/extensions.json`, `/registry/extensions/`, `/registry/thesauri.json`, `/registry/thesauri/`, `/registry/dataPackages.json`, `/registry/dataPackages/<name>/<ver>[/version.json]` | GET | Extension/vocabulary/schema catalogues (used by admin updates) | – | [OBSERVED 200 for the `.json` ones] |
| `/registry/ipt/register` | POST | Register the IPT installation (returns installation key) | ⚠️ | [SRC `registerIPT`] |
| `/registry/ipt/update/<iptKey>` | POST | Update the IPT's record (incl. RSS feed URL `<IPT_URL>/rss.do`) | ⚠️ | [SRC `updateIpt`] |
| `/registry/ipt/resource` | POST | Register a dataset (sends title, description, contacts, `serviceUrls` = `eml.do?r=…\|archive.do?r=…`) | ⚠️ | [SRC `register`] |
| `/registry/ipt/resource/<datasetKey>` | POST | Update dataset record | ⚠️ | [SRC `updateResource`] |
| `/registry/ipt/resource/<datasetKey>` | DELETE | Deregister dataset (done by `resource-delete.do`) | ⚠️ | [SRC `deregister`] |
| `/registry/resource/<datasetKey>/network/<netKey>` | POST / DELETE | Add/remove network | ⚠️ | [SRC] |

The admin registration page also calls `GET https://api.gbif.org/v1/organization/<orgKey>/installation` (UAT: `https://api.gbif-uat.org/v1/…`) from the browser. [SRC `W/admin/registration.ftl:93-97`]

### 7.2 Public GBIF API v1 for IPT health checks

Base `https://api.gbif.org/v1/` (production) / `https://api.gbif-uat.org/v1/` (test). Anonymous GET, JSON, paged with `limit`/`offset`, rate-limited (HTTP 429 → slow down; set a descriptive `User-Agent`). Reference: <https://techdocs.gbif.org/en/openapi/> ("Registry", "Occurrence" sections; the per-endpoint pages are rendered client-side, so the table below was **verified by live calls on 2026-10-02**). Endpoints not documented there "may be changed or removed without warning".

| Endpoint | Returns | Use for IPT health |
|---|---|---|
| `GET /dataset/<gbifKey>` | Dataset: `key`, `installationKey`, `publishingOrganizationKey`, `type`, `subtype`, `title`, `doi`, `modified`, `pubDate`, `created`, `endpoints` (usually empty here), `machineTags`, … | Is the dataset registered; which installation/org owns it; GBIF-side `modified` vs IPT `lastPublished`. 404 = not (or no longer) registered |
| `GET /dataset/<gbifKey>/endpoint` | `[ {key,type:"DWC_ARCHIVE"\|"EML"\|…,url,created,modified} ]` | **URLs GBIF crawls** — compare with the IPT public URL (`<IPT_URL>/archive.do?r=<shortname>`, `…/eml.do?r=…`). A stale host/shortname here explains "GBIF can't crawl" |
| `GET /dataset/<gbifKey>/process?limit=N` | Paged crawl history, newest first: `crawlJob{endpointType,targetUrl,attempt}`, `startedCrawling`, `finishedCrawling`, `finishReason` (OBSERVED `NORMAL`; other values per GBIF docs), `processStateOccurrence` (OBSERVED `FINISHED`), `processStateChecklist` (OBSERVED `EMPTY`), `pagesCrawled`, `rawOccurrencesPersisted{New,Updated,Unchanged,Error}`, `fragmentsEmitted/Received/Processed`, `verbatim…`, `interpreted…Persisted{Successful,Error}` | Runbook row (✅ verified): last crawl time/outcome; `finishReason` ≠ `NORMAL` or any `…Error` counter > 0 → investigate the archive (`validator`) |
| `GET /dataset/<gbifKey>/document` | EML as stored by GBIF (XML) | Compare `packageId`, `pubDate`, version with `eml.do` of the IPT |
| `GET /dataset/<gbifKey>/machineTag` | e.g. `crawler.gbif.org / crawl_attempt` | Failed-crawl counters |
| `GET /occurrence/search?datasetKey=<gbifKey>&limit=0` | `{count:N,…}` | **Indexed record count** vs IPT `records` (inventory/`recordsPublished`). Note: count = occurrences only (checklist/sampling-event datasets differ) |
| `GET /installation/<installationKey>` | `type:"IPT_INSTALLATION"`, `organizationKey`, `title`, `disabled`, `endpoints:[{type:"FEED",url:"<IPT_URL>/rss.do"}]`, `machineTags` | Installation known to GBIF? `disabled`? Feed URL equals the IPT's current base URL? (mismatch after a domain change = crawl failures) |
| `GET /installation/<installationKey>/dataset?limit=N` | `{count, results:[dataset…]}` | All datasets GBIF has for this IPT → diff against `GET /inventory/v2/dataset` |
| `GET /organization/<orgKey>` | Organisation: `endorsementStatus`, `endorsementApproved`, `endorsingNodeKey`, `title` | Publisher endorsed? (unendorsed publishers' data is not indexed) |
| `GET /organization/<orgKey>/installation` | Installations of the org (used by IPT registration page) | Find the IPT's installation key from the org |
| `GET /organization/<orgKey>/publishedDataset?limit=N` | Datasets published by the org | Dataset inventory per org |
| `GET /dataset?type=…&limit=N`, `GET /dataset/search?q=` | Dataset lists | Discovery (not needed if keys are known) |

Where the keys come from: **GBIF dataset key** = `gbifKey` in `/inventory/v2/dataset` (or `<key>` in `resource.xml`); **installation key** = `ipt:identifier` in `rss.do` (= IPT UUID, `registration2.xml`); **organisation key** = `resource.xml`/`registration2.xml`. GBIF's crawl is **pull-based**: it re-crawls when the dataset `modified`/endpoint changes or on its schedule; manual re-crawl is only possible with GBIF registry rights ([faq.adoc](https://ipt.gbif.org/manual/en/ipt/latest/faq): "5–60 minutes … to start indexing"; crawl monitor <https://registry.gbif.org/monitoring/running-crawls>).

---

## 8. Data directory layout

Location resolution, in order (`J/config/IPTModule.java:provideDataDir`): servlet-context parameter `IPT_DATA_DIR` → env var `IPT_DATA_DIR` (Docker image: `ENV IPT_DATA_DIR=/srv/ipt`, `VOLUME /srv/ipt`, `package/docker/Dockerfile`) → file `WEB-INF/datadir.location` inside the webapp (text file holding the path). `<datadir>/tmp` is **wiped at every startup** (`DataDir.clearTmp`).

```
<datadir>/
├── config/
│   ├── ipt.properties            # main settings (ipt.baseURL, proxy, debug, archivalMode/Limit, mail.smtp.*, session.timeout, location.lat/lon, defaultLocale, admin.email, analytics.key)  [AppConfig keys]
│   ├── .gbifreg                  # registry lock: PRODUCTION | DEVELOPMENT  (AppConfig.PRODUCTION_TYPE_LOCKFILE)
│   ├── users.xml                 # all accounts incl. role, last login, BCrypt password hash   (UserAccountManagerImpl.PERSISTENCE_FILE)
│   ├── registration2.xml         # IPT registration: ipt key/password, associated organisations (+ tokens, DOI accounts)  (RegistrationManagerImpl; registration.xml = legacy v1)
│   ├── .extensions/              # installed extension definitions (*.xml) (ExtensionManagerImpl)
│   ├── .vocabularies/            # *.vocab files (VocabulariesManagerImpl)
│   ├── .dataPackages/<schema>/   # data package schemas (DataPackageSchemaManagerImpl)
│   └── .uiSettings/              # ipt-color-scheme.properties, logos/logo.<ext>
├── resources/
│   └── <shortname>/
│       ├── resource.xml          # THE resource record: coreType, status, key (GBIF UUID), organisation, doi, versionHistory, sources (incl. SQL host/db/user/sql; password encrypted via PasswordEncrypter), mappings, managers, auto-publish fields, nextPublished, recordsPublished …   (DataDir.PERSISTENCE_FILENAME)
│       ├── eml.xml               # working (unpublished) metadata
│       ├── inferredMetadata.xml  # inferred metadata draft
│       ├── eml-<ver>.xml         # published EML per version, e.g. eml-1.2.xml
│       ├── dwca.zip              # working archive being built / last generated
│       ├── dwca-<ver>.zip        # published DwC-A per version  (Constants DWC_ARCHIVE_NAME "dwca" + ".zip")
│       ├── datapackage-<ver>.zip, datapackage.json / datapackage-<ver>.json, metadata.yaml / metadata-<ver>.yaml   # data packages (camtrap-dp: .json, coldp: .yaml)
│       ├── <shortname>-<ver>.rtf # RTF export per version
│       ├── logo.<jpeg|gif|png>   # resource logo
│       ├── publication.log       # log of the LAST publication run (also at /publicationlog.do)
│       └── sources/
│           ├── <source><suffix>  # uploaded file sources (csv/tsv/xls/xlsx/…)
│           └── <source>.log      # per-source read log (also /sourcelog.do)
├── logs/
│   ├── admin.log                 # WARN+ of org.gbif; rolls at 10 MB and on startup  (→ /admin/logfile.do?log=admin)
│   └── debug.log                 # everything; same rolling                             (→ /admin/logfile.do?log=debug)
└── tmp/                          # scratch (uploads, peek output, archive builds); cleared on start
```
[SRC `J/config/DataDir.java`, `AppConfig.java`, `LoggingConfiguration.java`, `J/service/*/impl/*ManagerImpl.java`; **OBSERVED** in the 3.3.6 container: `config/{.dataPackages,.gbifreg,.uiSettings,.vocabularies,ipt.properties,registration2.xml,users.xml}`, `logs/{admin.log,debug.log}`, `resources/<sn>/resource.xml`, `tmp/`. `.extensions/` was absent only because the sandbox could not install extensions.]

File-level triage hints:
- Published but 404 on `archive.do`/`eml.do` → `resources/<sn>/dwca-<ver>.zip` / `eml-<ver>.xml` missing while `resource.xml` `<versionHistory>` still lists the version.
- Stuck "publishing" after a crash: in-memory only; restart clears locks/reports; `publication.log` shows the last step reached.
- `resource.xml` is read once at startup (IPT keeps the model in memory) — edit only with the IPT stopped, keep a backup.
- Free space: `HealthAction` uses the volume of the data dir; a full disk breaks login (`users.xml` rewrite), publication, and registry sync ([#2390](https://github.com/gbif/ipt/issues/2390), [#2391](https://github.com/gbif/ipt/issues/2391)).

---

## 9. Runbook verification (corrections)

Each runbook row was checked against the source and, where marked, against a live container.

| Runbook row | Verdict | Details |
|---|---|---|
| `/inventory/v2/dataset` GET, no login: `records`, `lastPublished`, `version`, `gbifKey`, records per extension; no next publication | ✅ **Correct** [SRC+OBSERVED] | Records per extension live in `additionalProperties.recordsByExtension` (DwC-A) / `recordsByTable` (data packages); `lastPublished` has date only. Extra: `status`/`type` query filters; **default** list = latest published public versions (includes PUBLIC and REGISTERED), `gbifKey` omitted if unregistered. (v1 `/inventory/dataset` = REGISTERED only.) |
| `/api/resources` POST DataTables, no login; next publication in column 8; overdue in `<span class="text-gbif-danger">`; column 11 = shortname | ✅ **Correct** [SRC+OBSERVED shape] | 13 columns (0–12). Add: default `length` is **10**; `draw` ignored; GET works but needs URL-encoded brackets (raw brackets → Tomcat 400). Public rows exclude PRIVATE/DELETED/never-released resources. Next-publication shown is the live value. |
| `/manager-api/resources` POST, login; includes hidden/private | ✅ **Correct** [OBSERVED: anonymous → 302 login] | Scope depends on role: Admin = all; Manager = only resources created/co-managed. Shows live (not last-published) title/status, plus `pendingStatus`. |
| `/manage/resource.do?r=<id>`: button `id="publish-button-show-warning"` = publication blocked (invalid metadata); button in `<form action="publish.do?r=<id>">` = can publish | ⚠️ **Partly correct — must be broadened** [SRC `W/macros/manage/publish.ftl`; OBSERVED on a fresh resource: `publish-button-show-warning` present, no `publish.do` form] | `publish-button-show-warning` is rendered not only for invalid metadata but also when: status is DELETED; data-package mappings missing; resource is REGISTERED without a GBIF-supported licence; no publishing organisation (DwC-A); the user lacks registration (Publisher/Admin) rights for a DOI-reserved/registered/REGISTERED resource; no DOI agency account activated. If **neither** marker is present (unmatched branch) publication is deliberately not offered. Also: the form posts `publish=Publish` (button `name="publish"`), `summary`, hidden `r`. And **while a publish is running** `resource.do?r=` redirects to `locked.do` (use `report.do`). |
| `/manage/report.do?r=<id>`: `In Progress` / `Completed` / failure + log | ✅ **Correct text**, ❌ **"Login: yes" is not enforced** | Status words come from i18n (`In Progress`, `Completed`, `Failed`; language follows `request_locale`/session). Log = link to `/publicationlog.do?r=` (public). The action uses `ajaxStack` only, so **no authentication** is applied: [OBSERVED] anonymous `GET /manage/report.do?r=x` → 200 (even for unknown `r`). Always log in anyway (not guaranteed in other versions). A report only exists in memory (empty after restart). |
| `/manage/mappingPeek.do?r=&id=<rowType>&mid=0`: read-only 100-row preview | ✅ **Correct** (`PEEK_ROWS`=100 per `OverviewAction`) [SRC] | `id` must be the full rowType **URI**; `mid` is the 0-based index among mappings of that rowType. Same missing-auth caveat as `report.do` (anonymous reached the action: HTTP 500 for a non-existent mapping) [OBSERVED]. Executes the source SQL against the source DB. |
| `/manage/source.do?r=&id=`: host, DB, user and SQL | ✅ **Correct** [SRC `W/manage/source.ftl`] | Fields `rdbms`, `sqlSource.host`, `sqlSource.database`, `sqlSource.username`, `sqlSource.sql`. Password stored encrypted in `resource.xml`, not echoed (`sqlSourcePassword`). |
| `/manage/auto-publish.do?r=` GET/POST | ✅ **Correct**; POST fields in §5.2; `updateFrequencyDay` is parsed with `Integer.parseInt` (a missing value → 500) [SRC] |
| `/manage/metadata-contacts.do?r=` GET/POST | ✅ **Correct**; one of 14 `metadata-<section>` pages (§5.1) |
| `/admin/logfile.do?log=admin` / `?log=debug` (admin = WARN+, debug = all) | ✅ **Correct** [SRC+OBSERVED 200 `text/plain`] | Login must be **admin** role (not just manager). Only the live `admin.log` / `debug.log`; rolled files unreachable via HTTP. |
| `/health.do` partial login; system section only with login | ✅ **Correct** [SRC+OBSERVED] | Plus **undocumented** `GET /api/health` (JSON, anonymous, no system block) — §3.5. |
| `api.gbif.org/v1/dataset/<gbifKey>/process` GET no login | ✅ **Correct** [OBSERVED] | Newest-first paged list; `limit` supported; see §7.2 for fields. |

New endpoints not in the runbook that are useful: `/admin-api/publication-report(s)` (§3.4), `/api/health` (§3.5), `/publicationlog.do`, `/sourcelog.do`, `/rss.do`, `/dcat`, `/inventory/dataset`, `/manage/peek.do`, `/manage/history.do`.

---

## 10. Security and safety observations

Verified on IPT 3.3.6 (local, disposable container) unless marked otherwise; they matter because a health-check agent must not trigger side effects by accident.

1. **State changes work with HTTP GET.** `GET /manage/resource-deleteFromIpt.do?r=<sn>&deleteFlag=Delete` deleted a resource [OBSERVED]. The actions only test the flag parameter (`publish`, `unpublish`, `undelete`, `deleteFlag`, `reserveDoi`, `deleteDoi`), not `isHttpPost()`; comment in code: "so the same request triggered purely by a URL will not work" — which is true for hand-typed URLs without the flag, not for CSRF. `GET /admin/publishAll.do` (starts publication of all resources) and `GET /admin/deleteVersion.do?r=&v=` also execute without POST [SRC `PublishAllResourcesAction.execute`, `DeleteVersionAction.execute`; OBSERVED 200 for publishAll]. ⇒ A monitoring script must only issue GETs from the "safe" tables, never follow redirects blindly into ⚠️ URLs, and never crawl `/manage/*` links.
2. **Only the login form has CSRF protection** (§4). No Struts token on any other form.
3. **Actions that skip authentication** (their `<action>` declares `ajaxStack` = `i18nStack`, which replaces the package default `managerStack`/`adminStack`) [SRC `S/struts-manage.xml`, `S/struts-admin.xml`; OBSERVED anonymous requests reaching action code]:
   - `GET /manage/report.do?r=` (200), `GET /manage/peek.do?r=&id=` (404 "source cannot be loaded" = action code reached), `GET /manage/mappingPeek.do?r=&id=&mid=` (500 = action code reached; for an existing mapping it would return the first 100 data rows), `GET /admin/bulkReport.do` (200),
   - ⚠️ `GET /manage/cancel.do?r=<sn>` (200 page "Failed to stop publishing!" when nothing runs; with a running job it **cancels that publication**).
   Treat as a vulnerability to report upstream; for the skill: always authenticate, and do not rely on these being open.
4. **`/inventory/v2/dataset?status=private` is anonymous** and lists previously-published private resources (title, version, file URLs; the files themselves still 401) [SRC `InventoryV2Action.execute` → `resourceManager.list(status)`; INFERENCE for live behaviour].
5. **`/manage/urlMetadata.do?url=`** makes the IPT server fetch an arbitrary URL (manager login required) [SRC] – not to be used by the skill.
6. **Process state is volatile**: publication reports/locks live in memory (`ResourceManager`); restart ends running jobs. Auto-publish suspends itself after repeated failures; a manual `publish.do` resets the failure counter (comment block in `OverviewAction.publish`).
7. **Never log or store**: `config/users.xml`, `config/registration2.xml` (registry/organisation tokens, DOI passwords), SQL source passwords, `IPT_PASSWORD`.

Docker note (this skill's tests): containers were run only on local Docker with `gbif/ipt:latest` (3.3.6), reached on `localhost`, and removed afterwards (`docker rm -f -v`). First-run setup was scripted through the wizard POSTs of §2; in an offline sandbox extension/schema installation fails with `NoSuchFileException … tmp/_http_rs_gbif_org_…` (harmless for endpoint tests).
