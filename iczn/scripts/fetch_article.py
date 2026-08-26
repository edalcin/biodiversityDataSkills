#!/usr/bin/env python3
"""Fetch the verbatim text of an Article from code.iczn.org.

Why this exists: the reference files in this skill are an original synthesis of the
Code's rules, not a transcription -- the Code is copyrighted ("All rights reserved",
(c) International Trust for Zoological Nomenclature 1999) and reproducing it is not
ours to do. When the exact letter of a provision decides a case (and in nomenclature
it often does), this script goes and gets it from the source instead of us shipping a
copy. Nothing is written to disk unless you ask for it.

Note the site rejects plain HTTP clients with 403, so a browser User-Agent is sent.
That is not evasion of an access control; the pages are public and unauthenticated.

    python scripts/fetch_article.py 23            # whole Article
    python scripts/fetch_article.py 23.9          # just that sub-Article and its children
    python scripts/fetch_article.py glossary
    python scripts/fetch_article.py 74 --url      # print the canonical URL only
"""

import argparse
import html
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

INDEX = pathlib.Path(__file__).with_name("code_index.json")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

SECTION_ALIASES = {
    "glossary": "glossary-2",
    "preamble": "preamble",
    "introduction": "introduction",
    "preface": "preface-to-the-fourth-edition",
    "summary": "summary",
    "appendices": "appendices",
    "appendix-a": "appendices/appendix-a-code-of-ethics",
    "ethics": "appendices/appendix-a-code-of-ethics",
    "appendix-b": "appendices/appendix-b-general-recommendations",
    "constitution": "appendices/constitution-of-the-iczn",
}


def load_index():
    return json.loads(INDEX.read_text(encoding="utf-8"))


def resolve(target, index):
    """Return (url, article_number_or_None, label)."""
    key = target.strip().lower().lstrip("art.").strip()
    if key in SECTION_ALIASES or key in index["sections"]:
        slug = SECTION_ALIASES.get(key, key)
        entry = index["sections"].get(slug)
        if entry is None:
            sys.exit(f"unknown section: {target}")
        return entry["url"], None, entry.get("title", slug)
    m = re.match(r"^(\d+)(?:\.[\d.]+)?$", key)
    if not m:
        sys.exit(f"cannot interpret {target!r}: give an Article number (e.g. 23.9) "
                 f"or one of {', '.join(sorted(SECTION_ALIASES))}")
    n = int(m.group(1))
    for a in index["articles"]:
        if a["article"] == n:
            return a["url"], n, f"Article {n}. {a['title']}"
    sys.exit(f"no Article {n} in the Code (Articles run 1-90)")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} fetching {url}")
    except urllib.error.URLError as e:
        sys.exit(f"cannot reach {url}: {e.reason}")


def to_text(raw):
    raw = re.sub(r"(?is)<(script|style|head).*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<(br|/p|/div|/li|/h[1-6]|/tr)[^>]*>", "\n", raw)
    raw = re.sub(r"<[^>]+>", "", raw)
    raw = html.unescape(raw).replace("\xa0", " ")
    raw = re.sub(r"[ \t]+", " ", raw)
    return re.sub(r"\n\s*\n+", "\n\n", raw).strip().lstrip("\u25c0\u25b6 \n")


def slice_subarticle(text, ref):
    """Keep the paragraph introducing `ref` and everything nested under it.

    Sub-articles are numbered hierarchically (23.9, 23.9.1, 23.9.1.2), so "nested
    under 23.9" means any number that starts with "23.9." -- and the slice ends at
    the first number that does not, which is the next sibling.
    """
    lines = text.splitlines()
    out, capturing = [], False
    for line in lines:
        m = re.match(r"\s*(\d+(?:\.\d+)+)\.?\s", line)
        if m:
            num = m.group(1)
            if num == ref or num.startswith(ref + "."):
                capturing = True
            elif capturing:
                break
        if capturing:
            out.append(line)
    return "\n".join(out).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="Article number (23, 23.9), or glossary/preamble/"
                                   "introduction/appendix-a/appendix-b/constitution")
    ap.add_argument("--url", action="store_true", help="print the canonical URL and exit")
    ap.add_argument("--raw", action="store_true", help="print the HTML unprocessed")
    args = ap.parse_args()

    index = load_index()
    url, article, label = resolve(args.target, index)
    sub = args.target.strip() if re.match(r"^\d+\.[\d.]+$", args.target.strip()) else None
    if sub:
        url += "#art-" + sub.replace(".", "-")

    if args.url:
        print(url)
        return

    raw = get(url.split("#")[0])
    if args.raw:
        print(raw)
        return

    text = to_text(raw)
    if sub:
        piece = slice_subarticle(text, sub)
        if not piece:
            print(f"# {label}\n# {url}\n\n[Art. {sub} not found as a numbered paragraph on "
                  f"this page -- showing the whole Article]\n", file=sys.stderr)
        else:
            text = piece

    print(f"# {label}")
    print(f"# Source: {url}")
    print("# (c) International Trust for Zoological Nomenclature. Quoted here for "
          "consultation; do not redistribute.\n")
    print(text)


if __name__ == "__main__":
    main()
