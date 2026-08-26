#!/usr/bin/env python3
"""Look up an Article or a Glossary term in this skill's local reference files.

This is the offline path: it reads the synthesised rules in references/ rather than
the Code website, so it works with no network and returns the operational statement
of the rule plus its citation. When you need the Code's exact wording instead, use
fetch_article.py.

    python scripts/explain.py                        # overview + chapter map
    python scripts/explain.py --article 23.9         # the rule and its sub-rules
    python scripts/explain.py --term "nomen oblitum"
    python scripts/explain.py --search homonym       # free-text across all references
    python scripts/explain.py --list                 # every Article with its chapter
"""

import argparse
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REFS = HERE.parent / "references"
INDEX = HERE / "code_index.json"


def load():
    if not INDEX.exists():
        sys.exit(f"missing {INDEX}; the skill is incomplete")
    return json.loads(INDEX.read_text(encoding="utf-8"))


def overview(index):
    print("International Code of Zoological Nomenclature -- 4th edition (1999)")
    print("In force with Declarations 44-47 and the 2012 electronic-publication amendment.")
    print(f"Source: {index['source']}   Articles: 1-90 in 18 chapters\n")
    seen = {}
    for a in index["articles"]:
        seen.setdefault(a["chapter"], (a["chapter_title"], a["reference"], []))[2].append(a["article"])
    for ch in sorted(seen):
        title, ref, nums = seen[ch]
        print(f"  Ch {ch:>2}  Arts. {nums[0]:>2}-{nums[-1]:<2}  {title}")
        print(f"          -> references/{ref}")
    print("\n  Also: references/glossary.md, appendices.md, zoobank.md,")
    print("        data-modeling.md, dwc-mapping.md, other-codes.md")
    print("\nAuthoritative texts are the English and French texts of the Code (Art. 87);")
    print("this skill is a synthesis and has no standing in a dispute.")


def list_articles(index):
    for a in index["articles"]:
        print(f"Art. {a['article']:>2}  {a['title']:<70}  ch{a['chapter']:>2}  {a['reference']}")


def article(index, ref):
    m = re.match(r"^(\d+)", ref.strip())
    if not m:
        sys.exit(f"not an Article number: {ref!r}")
    n = int(m.group(1))
    entry = next((a for a in index["articles"] if a["article"] == n), None)
    if entry is None:
        sys.exit(f"no Article {n} (the Code has Articles 1-90)")
    path = REFS / entry["reference"]
    print(f"Article {n}. {entry['title']}   (Chapter {entry['chapter']}: {entry['chapter_title']})")
    print(f"Code text: {entry['url']}")
    print(f"Synthesis: references/{entry['reference']}\n")
    if not path.exists():
        sys.exit(f"reference file {path} not found")
    lines = path.read_text(encoding="utf-8").splitlines()

    # Locate the "## Article N" heading and stop at the next Article heading. The
    # negative lookahead matters: reference files sometimes give a long sub-Article its
    # own "### Article 23.9" heading, and without it that heading would be mistaken for
    # the start of the next Article, truncating the block just before the part asked for.
    start = next((i for i, l in enumerate(lines)
                  if re.match(rf"^#+\s*Article\s+{n}(?![\d.])", l)), None)
    if start is None:
        sys.exit(f"references/{entry['reference']} has no section for Article {n}")
    end = next((i for i in range(start + 1, len(lines))
                if re.match(r"^#+\s*Article\s+\d+(?![\d.])", lines[i])), len(lines))
    block = lines[start:end]

    if "." in ref:  # a specific sub-Article: keep it and anything nested under it
        want = ref.strip()
        # Preferred case: the sub-Article has its own heading, so take that section.
        head = next((i for i, l in enumerate(block)
                     if re.match(rf"^#+\s*Article\s+{re.escape(want)}(?![\d.])", l)), None)
        if head is not None:
            depth = len(block[head]) - len(block[head].lstrip("#"))
            tail = next((j for j in range(head + 1, len(block))
                         if re.match(r"^#+", block[j])
                         and len(block[j]) - len(block[j].lstrip("#")) <= depth), len(block))
            block = block[head:tail]
        else:
            kept, capturing = [], False
            for line in block:
                # The number may carry trailing text inside the bold ("**8.5 (2012 text)**"),
                # and if that is not matched the scan never sees the next sibling and
                # keeps capturing past the end of what was asked for.
                hit = re.search(r"\*\*(\d+(?:\.\d+)+)\b[^*]*\*\*", line)
                if hit:
                    num = hit.group(1)
                    capturing = num == want or num.startswith(want + ".")
                if capturing:
                    kept.append(line)
            if kept:
                block = kept
            else:
                print(f"[Art. {want} is not called out separately; "
                      f"showing all of Article {n}]\n")
    print("\n".join(block).strip())


def term(index, needle):
    path = REFS / "glossary.md"
    if not path.exists():
        sys.exit("references/glossary.md not found")
    needle_l = needle.lower()
    rows = [l for l in path.read_text(encoding="utf-8").splitlines()
            if l.startswith("|") and needle_l in l.split("|")[1].lower()]
    if not rows:
        print(f"'{needle}' not found in the Glossary. Try --search {needle}")
        return
    for r in rows:
        cells = [c.strip() for c in r.strip("|").split("|")]
        print(f"{cells[0]}")
        for label, cell in zip(("definition", "governing Article", "pt-BR"), cells[1:]):
            if cell:
                print(f"  {label}: {cell}")
        print()


def search(needle):
    needle_l = needle.lower()
    hits = 0
    for path in sorted(REFS.glob("*.md")):
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if needle_l in line.lower():
                print(f"{path.name}:{i}: {line.strip()[:200]}")
                hits += 1
    if not hits:
        print(f"no match for {needle!r} in references/")


def main():
    # Piping into head/less closes the stream early; that is the caller's choice, not
    # an error, so let the default SIGPIPE behaviour apply instead of raising.
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--article", help="Article or sub-Article, e.g. 23 or 23.9.1")
    ap.add_argument("--term", help="Glossary term")
    ap.add_argument("--search", help="free-text search across all reference files")
    ap.add_argument("--list", action="store_true", help="list all 90 Articles")
    args = ap.parse_args()

    index = load()
    if args.article:
        article(index, args.article)
    elif args.term:
        term(index, args.term)
    elif args.search:
        search(args.search)
    elif args.list:
        list_articles(index)
    else:
        overview(index)


if __name__ == "__main__":
    main()
