#!/usr/bin/env python3
"""
sync.py - Downloads SKOS and SKOS-XL schema files from W3C.

Downloads:
  - SKOS Core schema (RDF/OWL) from W3C
  - SKOS-XL schema (RDF/OWL) from W3C
  - TDWG TAG SKOS-XL examples (NameThing, Person patterns)

Usage:
    python scripts/sync.py
"""

import sys
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REF_DIR = Path(__file__).resolve().parent.parent / "references"

FILES = [
    {
        "url": "https://www.w3.org/2004/02/skos/core.rdf",
        "dest": "skos_core.rdf",
        "desc": "SKOS Core schema (RDF/OWL)",
        "headers": {"Accept": "application/rdf+xml"},
    },
    {
        "url": "https://www.w3.org/2008/05/skos-xl.rdf",
        "dest": "skos_xl.rdf",
        "desc": "SKOS-XL schema (RDF/OWL)",
        "headers": {"Accept": "application/rdf+xml"},
    },
    {
        "url": "https://raw.githubusercontent.com/tdwg/tag/master/skos-xl/skosxl-name.ttl",
        "dest": "tdwg_skosxl_name.ttl",
        "desc": "TDWG TAG NameThing pattern (Turtle)",
        "headers": {},
    },
    {
        "url": "https://raw.githubusercontent.com/tdwg/tag/master/skos-xl/skosxl-person.ttl",
        "dest": "tdwg_skosxl_person.ttl",
        "desc": "TDWG TAG Person label pattern (Turtle)",
        "headers": {},
    },
]


def download_file(url, dest_path, extra_headers=None):
    try:
        headers = {"User-Agent": "skos-xl-skill/1.0"}
        if extra_headers:
            headers.update(extra_headers)
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status != 200:
                return False, "HTTP %d" % response.status
            content = response.read()
            with open(dest_path, "wb") as f:
                f.write(content)
            return True, len(content)
    except Exception as e:
        return False, str(e)


def main():
    print("[sync] Syncing references for skos-xl skill")
    print("=" * 60)
    print("   Directory: %s" % REF_DIR)
    print()

    REF_DIR.mkdir(parents=True, exist_ok=True)
    successes = 0
    failures = 0

    for f in FILES:
        print("[download] %s..." % f["desc"])
        print("   %s" % f["url"])
        ok, result = download_file(f["url"], REF_DIR / f["dest"], f.get("headers"))
        if ok:
            print("   [OK] (%s bytes)" % "{:,}".format(result))
            successes += 1
        else:
            print("   [FAIL] %s" % result)
            failures += 1
        print()

    print("=" * 60)
    print("[OK] %d file(s) downloaded" % successes)
    if failures:
        print("[WARN] %d download(s) failed" % failures)
        print("   The skill will continue using built-in references.")
    print()


if __name__ == "__main__":
    main()
