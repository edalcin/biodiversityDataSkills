#!/usr/bin/env python3
"""Detect whether code.iczn.org has changed since this skill's references were written.

It re-fetches each page and compares a hash of its content against the hash recorded
in code_index.json. What it deliberately does NOT do is rewrite the reference files:
a Code provision is a legal text, and turning a changed provision into a changed rule
is reading work, not a diff. So this reports, and a human (or an agent holding this
skill) does the rewriting.

The comparison hashes the page's extracted text, not its raw HTML, so a theme tweak
or a changed navigation link does not show up as a Code amendment.

    python scripts/sync.py                  # check everything (~101 requests, ~2 min)
    python scripts/sync.py --articles 8 9 10 21 78
    python scripts/sync.py --update-hashes  # accept current state as the new baseline
"""

import argparse
import hashlib
import html
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

INDEX = pathlib.Path(__file__).with_name("code_index.json")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
DELAY = 0.4  # the site is a small institutional server; do not hammer it


def text_of(raw):
    raw = re.sub(r"(?is)<(script|style|head).*?</\1>", " ", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw)).strip()


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--articles", nargs="*", type=int, help="check only these Articles")
    ap.add_argument("--update-hashes", action="store_true",
                    help="record the current pages as the baseline (do this only after "
                         "the reference files have actually been brought up to date)")
    args = ap.parse_args()

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    targets = []
    for a in index["articles"]:
        if args.articles and a["article"] not in args.articles:
            continue
        targets.append((f"Art. {a['article']}", a, a["reference"]))
    if not args.articles:
        for slug, s in index["sections"].items():
            targets.append((slug, s, "-"))

    changed, failed = [], []
    for i, (label, entry, ref) in enumerate(targets, 1):
        try:
            body = text_of(fetch(entry["url"]))
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            failed.append((label, str(e)))
            print(f"[{i}/{len(targets)}] {label}: UNREACHABLE ({e})", file=sys.stderr)
            continue
        digest = hashlib.sha256(body.encode()).hexdigest()
        old = entry.get("text_sha256")
        if old is None:
            entry["text_sha256"] = digest  # first run establishes the text baseline
            print(f"[{i}/{len(targets)}] {label}: baseline recorded")
        elif digest != old:
            entry["text_sha256"] = digest if args.update_hashes else old
            changed.append((label, entry["url"], ref))
            print(f"[{i}/{len(targets)}] {label}: CHANGED -> review references/{ref}")
        time.sleep(DELAY)

    if args.update_hashes or any(e.get("text_sha256") for _, e, _ in targets):
        INDEX.write_text(json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8")

    print()
    if failed:
        print(f"{len(failed)} page(s) unreachable; the check is incomplete.")
    if not changed:
        print("No content change detected against the recorded baseline.")
        return
    print(f"{len(changed)} page(s) changed upstream. Each needs a human re-reading, "
          f"not an automatic patch:\n")
    for label, url, ref in changed:
        print(f"  {label}\n    {url}\n    update: references/{ref}")
    print("\nAfter the reference files are corrected, re-run with --update-hashes to "
          "move the baseline forward.")
    sys.exit(1)


if __name__ == "__main__":
    main()
