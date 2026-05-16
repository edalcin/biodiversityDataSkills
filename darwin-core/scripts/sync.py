#!/usr/bin/env python3
"""
sync.py - Syncs skill references from official sources.

Downloads:
  - all_dwc_vertical.csv (simple Darwin Core term list)
  - term_versions.csv (full term version history)
  - Text Guide (DwC-A specification)

Usage:
    python scripts/sync.py
"""

import os
import sys
import urllib.request
from pathlib import Path

# Ensure UTF-8 output (Windows fix)
if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REF_DIR = Path(__file__).resolve().parent.parent / "references"

FILES = [
    {
        "url": "https://raw.githubusercontent.com/tdwg/dwc/master/dist/all_dwc_vertical.csv",
        "dest": "all_dwc_vertical.csv",
        "desc": "Darwin Core terms (CSV)",
    },
    {
        "url": "https://raw.githubusercontent.com/tdwg/dwc/master/vocabulary/term_versions.csv",
        "dest": "term_versions.csv",
        "desc": "Term version history",
    },
    {
        "url": "https://raw.githubusercontent.com/tdwg/dwc/master/docs/text/index.md",
        "dest": "TEXT_GUIDE.md",
        "desc": "Darwin Core Text Guide specification",
    },
]


def download_file(url, dest_path):
    """Download a file from URL to destination path."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "darwin-core-skill/1.0"}
        )
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
    print("[sync] Syncing references for darwin-core skill")
    print("=" * 60)
    print("   Directory: %s" % REF_DIR)
    print()

    REF_DIR.mkdir(parents=True, exist_ok=True)

    successes = 0
    failures = 0

    for f in FILES:
        print("[download] %s..." % f["desc"])
        print("   %s" % f["url"])
        ok, result = download_file(f["url"], REF_DIR / f["dest"])
        if ok:
            print("   [OK] (%s bytes)" % "{:,}".format(result))
            successes += 1
        else:
            print("   [FAIL] %s" % result)
            failures += 1
        print()

    print("=" * 60)
    print("[OK] %s file(s) downloaded successfully" % successes)
    if failures:
        print("[WARN] %s download(s) failed" % failures)
        print("   The skill will continue using existing references.")
    print()


if __name__ == "__main__":
    main()
