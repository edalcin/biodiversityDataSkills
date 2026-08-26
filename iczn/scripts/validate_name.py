#!/usr/bin/env python3
"""Check zoological names against the mechanically checkable provisions of the Code.

The point of this script is the boundary it draws. Some of the Code's requirements are
decidable from the characters in a string -- initial letters (Art. 28), the Latin
alphabet (Art. 11.2), family-group suffixes (Art. 29.2), the 1758 starting point
(Art. 3). Others look decidable and are not: whether a species-group epithet is an
adjective that must agree in gender with its genus (Art. 31.2) or a noun in apposition
that must not change (Art. 11.9.1.2) is a question about Latin grammar, not about
spelling. A validator that guesses at the second kind produces confident nonsense and
gets switched off, so this one reports three levels and never blurs them:

  violation  the Code is demonstrably breached by the string as given
  warning    the string is suspect and a human must look; the script cannot decide
  info       worth knowing, no defect implied

Read the level names literally. A `violation` is safe to act on in bulk; a `warning`
is a worklist, never an edit.

    python scripts/validate_name.py "Panthera onca (Linnaeus, 1758)"
    python scripts/validate_name.py --rank family "Felidae"
    python scripts/validate_name.py --csv names.csv --name-column scientificName
    python scripts/validate_name.py --csv names.csv --json > report.json

Homonym detection across a whole file needs the file, so it runs only in --csv mode.
"""

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict

# --- what the Code says, as data ---------------------------------------------------

# Art. 29.2. These suffixes are reserved to the ranks listed and must not be used at
# other family-group ranks. Art. 29.2.1 exempts genus- and species-group names that
# merely happen to end this way (the genus Ranoidea is not a superfamily).
FAMILY_SUFFIXES = {
    "oidea": "superfamily",
    "idae": "family",
    "inae": "subfamily",
    "ini": "tribe",
    "ina": "subtribe",
}

# Art. 58. Spellings deemed identical for homonymy -- but only for names "of the same
# derivation and meaning", which is why matches here can only ever be warnings
# (Art. 58's own Example: calidus "warm" and callidus "clever" are not homonyms).
ART_58_CLASSES = [
    (r"ae|oe", "e"),        # 58.1
    (r"ei|y", "i"),         # 58.2, 58.13
    (r"j", "i"),            # 58.3
    (r"v", "u"),            # 58.4
    (r"k", "c"),            # 58.5
    (r"ph", "f"),           # 58.9
    (r"ch", "c"),           # 58.6, 58.10
    (r"th", "t"),           # 58.11
    (r"ct", "t"),           # 58.8
    (r"ii", "i"),           # 58.14
    (r"(.)\1", r"\1"),      # 58.7 double consonant
]

LATIN_GENDER_ENDINGS = {"us": "masculine", "a": "feminine", "um": "neuter",
                        "is": "masculine or feminine", "e": "neuter",
                        "er": "masculine", "os": "masculine", "on": "neuter"}

# Endings that are grammatically genitive or otherwise invariant, so gender agreement
# does not apply (Art. 11.9.1.3, 31.1.2). Checking these first is what keeps the
# gender heuristic from firing on every eponym.
INVARIANT_ENDINGS = ("i", "ii", "ae", "iae", "orum", "iorum", "arum", "iarum",
                     "ensis", "iensis", "icus", "ianus")


class Finding:
    __slots__ = ("level", "article", "message", "subject")

    def __init__(self, level, article, message, subject=""):
        self.level, self.article, self.message, self.subject = level, article, message, subject

    def as_dict(self):
        return {"level": self.level, "article": self.article,
                "message": self.message, "subject": self.subject}

    def __str__(self):
        head = {"violation": "VIOLATION", "warning": "warning ", "info": "info    "}[self.level]
        where = f" [{self.subject}]" if self.subject else ""
        return f"  {head}  {self.article:<14} {self.message}{where}"


# --- parsing -----------------------------------------------------------------------

AUTHORSHIP_RE = re.compile(
    r"^\(?\s*(?P<authors>[^,()]+?)\s*,\s*(?P<year>\d{3,4})\s*\)?\.?$")


def parse(name):
    """Split a name string into its parts. Returns a dict; `authorship` may be None.

    The split is done on token shape rather than by matching an authorship pattern
    against the tail of the string, because a pattern match is ambiguous: in
    "Aus bus Smith, 1900" nothing in the characters distinguishes the genus from the
    author. What does distinguish them is the Code's own structure -- a name is a
    genus-group name optionally followed by lower-case species-group names (Art. 5),
    with an interpolated subgenus in parentheses not counted among the words
    (Art. 6.1). So: the name runs up to the last unparenthesised lower-case token,
    and authorship is whatever follows it.

    Deliberately permissive: the job is to report what is wrong with the input, so a
    malformed string must survive parsing long enough to be reported on.
    """
    raw = " ".join(name.split())
    out = {"input": raw, "authorship": None, "author_parenthesised": None,
           "authors": None, "year": None, "words": [], "subgenus": None}
    tokens = raw.split()
    if not tokens:
        return out

    # Without a year there is nothing to mark authorship, so treat it all as the name.
    # This keeps "Panthera Onca" (a capitalisation error, Art. 28) from being misread
    # as a genus plus an author.
    has_year = re.search(r"\d{3,4}\)?\.?$", raw) is not None
    cut = len(tokens)
    if has_year:
        lower_idx = [i for i, t in enumerate(tokens)
                     if t[:1].islower() and not t.startswith("(")]
        cut = (lower_idx[-1] + 1) if lower_idx else 1

    name_tokens = tokens[:cut]
    tail = " ".join(tokens[cut:]).strip()

    # Art. 6.1: an interpolated subgenus is not one of the words of the name.
    kept = []
    for t in name_tokens:
        if t.startswith("(") and t.endswith(")") and len(t) > 2:
            out["subgenus"] = t[1:-1]
        else:
            kept.append(t)
    out["words"] = kept

    if tail:
        out["authorship"] = tail
        out["author_parenthesised"] = tail.startswith("(")
        m = AUTHORSHIP_RE.match(tail)
        if m:
            out["authors"] = m.group("authors").strip()
            out["year"] = int(m.group("year"))
        else:
            y = re.search(r"(\d{3,4})\)?\.?$", tail)
            if y:
                out["year"] = int(y.group(1))
            authors = re.sub(r"[(),.]|\d", " ", tail).strip()
            out["authors"] = authors or None
    return out


def norm_58(word):
    """Collapse a species-group name to its Art. 58 equivalence class."""
    w = word.lower()
    for pat, rep in ART_58_CLASSES:
        w = re.sub(pat, rep, w)
    return w


# --- individual checks -------------------------------------------------------------

def check_charset(word, findings, subject):
    """Art. 11.2 / Art. 27. Note carefully: diacritics do NOT make a name unavailable
    (Art. 11.2 says so explicitly); they make the spelling incorrect and mandate a
    correction under Arts. 27 and 32.5.2. Conflating the two is exactly the error this
    script must not make, so the message says which is which."""
    for ch in word:
        if ch in "-":
            continue
        if not ("a" <= ch.lower() <= "z"):
            decomposed = unicodedata.decomposition(ch)
            if decomposed or ch in "æœ'\u2019":
                findings.append(Finding(
                    "violation", "Art. 27",
                    f"contains {ch!r}: diacritics, apostrophes and the ae/oe ligatures "
                    f"are not to be used and must be corrected per Art. 32.5.2 "
                    f"(availability itself is unaffected, Art. 11.2)", subject))
            elif ch.isdigit():
                findings.append(Finding(
                    "violation", "Art. 11.2",
                    f"contains the numeral {ch!r}; a numeral must be spelled out "
                    f"(Art. 32.5.2.4)", subject))
            else:
                findings.append(Finding(
                    "violation", "Art. 11.2",
                    f"contains {ch!r}, which is outside the 26 letters of the Latin "
                    f"alphabet", subject))
    if "-" in word:
        findings.append(Finding(
            "violation", "Art. 27",
            "contains a hyphen; permitted only in the narrow case of Art. 32.5.2.4.3, "
            "otherwise the hyphen is removed", subject))


def check_length(word, findings, subject, kind):
    art = "Art. 11.8" if kind == "genus" else "Art. 11.9.1"
    if len(re.sub(r"[^A-Za-z]", "", word)) < 2:
        findings.append(Finding("violation", art,
                                f"a {kind}-group name must be a word of two or more letters",
                                subject))


def check_initial(word, findings, subject, upper):
    """Art. 28, and it applies regardless of how the name was originally published."""
    letter = next((c for c in word if c.isalpha()), "")
    if not letter:
        return
    if upper and not letter.isupper():
        findings.append(Finding("violation", "Art. 28",
                                "must begin with an upper-case initial letter", subject))
    if not upper and not letter.islower():
        findings.append(Finding("violation", "Art. 28",
                                "a species-group name always begins with a lower-case "
                                "initial letter", subject))
    if upper and word[1:] != word[1:].lower() and word.upper() != word:
        findings.append(Finding("info", "Art. 28",
                                "internal capitals are unusual; check the original spelling",
                                subject))


def check_year(year, findings, subject):
    if year is None:
        return
    if year < 1758:
        findings.append(Finding(
            "violation", "Art. 3",
            f"dated {year}: 1 January 1758 is the starting point of zoological "
            f"nomenclature, so a name of this date is unavailable", subject))
    elif year > 2100:
        findings.append(Finding("violation", "Art. 21", f"implausible year {year}", subject))


def check_family(word, rank, findings, subject):
    """Art. 29.2, with the Art. 29.2.1 exemption respected: we only judge a suffix
    against a rank when the caller told us the rank."""
    low = word.lower()
    matched = next((s for s in sorted(FAMILY_SUFFIXES, key=len, reverse=True)
                    if low.endswith(s)), None)
    if rank is None:
        if matched:
            findings.append(Finding(
                "info", "Art. 29.2",
                f"ends in -{matched}, the suffix reserved for a {FAMILY_SUFFIXES[matched]}; "
                f"pass --rank to have this checked (a genus or species name may end this "
                f"way legitimately, Art. 29.2.1)", subject))
        return
    rank = rank.lower()
    if rank not in FAMILY_SUFFIXES.values():
        return
    expected = [s for s, r in FAMILY_SUFFIXES.items() if r == rank]
    if matched is None:
        findings.append(Finding(
            "violation", "Art. 29.2",
            f"declared rank {rank} requires the suffix -{expected[0]}", subject))
    elif FAMILY_SUFFIXES[matched] != rank:
        findings.append(Finding(
            "violation", "Art. 29.2",
            f"declared rank {rank} requires -{expected[0]} but the name ends in "
            f"-{matched}, which is reserved for a {FAMILY_SUFFIXES[matched]}", subject))


def check_gender(genus, epithet, findings, subject):
    """Art. 31.2 / 34.2 -- and this is the check that must stay a warning.

    Agreement is required only of an adjectival or participial epithet. A noun in
    apposition (Art. 11.9.1.2, e.g. Struthio camelus) and a genitive (Art. 11.9.1.3,
    e.g. smithi) do not change. Whether a given epithet is an adjective is a fact
    about Latin, not about its ending, so all this can honestly do is notice a
    possible mismatch and hand it to a human.
    """
    low = epithet.lower()
    if any(low.endswith(e) for e in sorted(INVARIANT_ENDINGS, key=len, reverse=True)):
        return  # genitive or toponymic: no agreement required
    ep_gender = next((g for e, g in sorted(LATIN_GENDER_ENDINGS.items(),
                                           key=lambda kv: -len(kv[0]))
                      if low.endswith(e)), None)
    gen_gender = next((g for e, g in sorted(LATIN_GENDER_ENDINGS.items(),
                                            key=lambda kv: -len(kv[0]))
                       if genus.lower().endswith(e)), None)
    if not ep_gender or not gen_gender or ep_gender == gen_gender:
        return
    if "or" in ep_gender or "or" in gen_gender:
        return
    findings.append(Finding(
        "warning", "Art. 31.2",
        f"if {epithet!r} is adjectival it must agree in gender with {genus!r} "
        f"(the genus ending suggests {gen_gender}, the epithet {ep_gender}); no change "
        f"is due if the epithet is a noun in apposition (Art. 11.9.1.2) or a genitive "
        f"(Art. 11.9.1.3). Determining which requires the Latin grammar of the word, "
        f"which this script cannot do -- check the original description. Gender is "
        f"itself governed by Art. 30, and any change is mandatory under Art. 34.2",
        subject))


def check_authorship(parsed, findings, subject):
    if parsed["authorship"] is None:
        if len(parsed["words"]) >= 2:
            findings.append(Finding(
                "info", "Art. 51.1",
                "no authorship cited; citation is recommended, not required", subject))
        return
    if parsed["author_parenthesised"]:
        findings.append(Finding(
            "info", "Art. 51.3",
            "the parentheses assert that this species-group name is combined with a "
            "genus other than the original one. That is a claim about the current "
            "combination, not a property of the name, so it must be re-derived whenever "
            "the generic assignment changes", subject))
    elif len(parsed["words"]) >= 2:
        findings.append(Finding(
            "info", "Art. 51.3",
            "authorship is unparenthesised, asserting the name is still in its original "
            "genus; if the species has been transferred, the parentheses are required",
            subject))
    if parsed["authors"] and re.search(r"\d", parsed["authors"]):
        findings.append(Finding("warning", "Art. 51.2",
                                f"author string {parsed['authors']!r} contains digits; "
                                f"the year should be separated by a comma", subject))


def check_binominal(parsed, findings, subject):
    n = len(parsed["words"])
    if n == 0:
        findings.append(Finding("violation", "Art. 11", "empty name", subject))
    elif n == 1:
        findings.append(Finding("info", "Art. 5",
                                "single word: read as a genus-group or higher name", subject))
    elif n == 2:
        pass  # a binomen, Art. 5.1
    elif n == 3:
        findings.append(Finding("info", "Art. 5.2",
                                "three words: read as a trinomen (subspecies)", subject))
    else:
        findings.append(Finding(
            "warning", "Art. 5",
            f"{n} words: not a binomen or trinomen. Subgenera in parentheses and "
            f"connecting terms such as 'var.' or 'subsp.' are not part of the name "
            f"(Art. 6, Art. 45.6) -- check what was intended", subject))


def check_tautonymy(parsed, findings, subject):
    w = parsed["words"]
    if len(w) >= 2 and w[0].lower() == w[1].lower():
        findings.append(Finding(
            "info", "Art. 18",
            "tautonym: identical genus and species-group names are permitted and the "
            "name is available (and see Art. 68.4 on absolute tautonymy fixing a type "
            "species)", subject))


# --- driver ------------------------------------------------------------------------

def validate(name, rank=None):
    parsed = parse(name)
    findings = []
    subject = ""
    check_binominal(parsed, findings, subject)
    words = parsed["words"]

    for word in words:
        check_charset(word, findings, word)
    if words:
        first = words[0]
        check_initial(first, findings, first, upper=True)
        check_length(first, findings, first, "genus")
        # A declared rank only governs a name of that rank. Applying --rank family to
        # the genus of a binomen would demand that Panthera end in -idae, which is
        # nonsense (and Art. 29.2.1 says so), so the suffix rule is judged only when
        # the name is a single word.
        if len(words) == 1:
            check_family(first, rank, findings, first)
        elif rank and rank.lower() in FAMILY_SUFFIXES.values():
            findings.append(Finding(
                "warning", "Art. 29.2",
                f"declared rank {rank.lower()} but the name has {len(words)} words; a "
                f"family-group name is a single word (Art. 4.1), so the rank and the "
                f"name disagree", first))
    for word in words[1:3]:
        check_initial(word, findings, word, upper=False)
        check_length(word, findings, word, "species")
    if len(words) >= 2:
        check_gender(words[0], words[1], findings, f"{words[0]} {words[1]}")
    if len(words) >= 3:
        check_gender(words[0], words[2], findings, f"{words[0]} ... {words[2]}")
    check_year(parsed["year"], findings, "")
    check_authorship(parsed, findings, "")
    check_tautonymy(parsed, findings, "")
    return parsed, findings


def homonym_scan(parsedlist):
    """Arts. 53.3 and 57: species-group homonymy exists only within a genus, so this
    groups by genus. Art. 58 makes certain spelling variants count as identical, but
    only for names of the same derivation and meaning -- which the script cannot judge,
    so variant collisions are warnings and exact collisions are violations."""
    findings = []
    by_genus = defaultdict(list)
    for parsed in parsedlist:
        w = parsed["words"]
        if len(w) >= 2:
            by_genus[w[0].lower()].append(parsed)
    for genus, members in by_genus.items():
        exact = defaultdict(list)
        variant = defaultdict(list)
        for p in members:
            ep = p["words"][1].lower()
            exact[ep].append(p)
            variant[norm_58(ep)].append(p)
        for ep, group in exact.items():
            years = {p["year"] for p in group}
            if len(group) > 1 and len(years) > 1:
                cites = "; ".join(sorted(p["input"] for p in group))
                findings.append(Finding(
                    "violation", "Art. 57.2",
                    f"primary homonyms in {genus.capitalize()}: same epithet {ep!r} "
                    f"published for different nominal taxa. The junior name is invalid "
                    f"(Art. 52.3) and needs a substitute (Art. 60): {cites}", genus))
        for key, group in variant.items():
            spellings = {p["words"][1].lower() for p in group}
            if len(spellings) > 1:
                findings.append(Finding(
                    "warning", "Art. 58",
                    f"in {genus.capitalize()}, {sorted(spellings)} differ only in a way "
                    f"Art. 58 deems identical, so they are homonyms IF they are of the "
                    f"same derivation and meaning. Art. 58's own Example (calidus "
                    f"'warm' vs callidus 'clever') shows they may not be -- check the "
                    f"etymologies before treating either as invalid", genus))
    return findings


def report_text(rows, out=sys.stdout):
    counts = defaultdict(int)
    for name, findings in rows:
        print(f"\n{name}", file=out)
        if not findings:
            print("  no findings", file=out)
        for f in findings:
            print(f, file=out)
            counts[f.level] += 1
    print(f"\n{'-' * 70}", file=out)
    print(f"{len(rows)} name(s) checked: "
          f"{counts['violation']} violation(s), {counts['warning']} warning(s), "
          f"{counts['info']} info", file=out)
    print("Violations are decidable from the string. Warnings need a human and the "
          "original description -- never bulk-edit on a warning.", file=out)
    return counts


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", help="one or more name strings")
    ap.add_argument("--csv", help="CSV file of names")
    ap.add_argument("--name-column", default="scientificName",
                    help="column holding the name (default: scientificName)")
    ap.add_argument("--rank-column", help="column holding the rank, for Art. 29.2 checks")
    ap.add_argument("--rank", help="rank of the name(s) given on the command line")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = ap.parse_args()

    rows, parsedlist = [], []
    if args.csv:
        with open(args.csv, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            if args.name_column not in (reader.fieldnames or []):
                sys.exit(f"column {args.name_column!r} not in {args.csv}; "
                         f"columns are {reader.fieldnames}")
            for row in reader:
                name = (row.get(args.name_column) or "").strip()
                if not name:
                    continue
                rank = (row.get(args.rank_column) or None) if args.rank_column else args.rank
                parsed, findings = validate(name, rank)
                rows.append((name, findings))
                parsedlist.append(parsed)
        cross = homonym_scan(parsedlist)
        if cross:
            rows.append((f"-- across {args.csv} --", cross))
    elif args.names:
        for name in args.names:
            parsed, findings = validate(name, args.rank)
            rows.append((name, findings))
            parsedlist.append(parsed)
    else:
        ap.error("give one or more names, or --csv")

    if args.json:
        json.dump({"names": [{"name": n, "findings": [f.as_dict() for f in fs]}
                             for n, fs in rows]}, sys.stdout, indent=1, ensure_ascii=False)
        print()
        violations = sum(1 for _, fs in rows for f in fs if f.level == "violation")
    else:
        violations = report_text(rows)["violation"]
    sys.exit(1 if violations else 0)


def _selftest():
    """Run with --selftest. Each assertion pins a rule to its Article, so a refactor
    that silently changes a level or drops a check fails here rather than in a user's
    50,000-row spreadsheet."""
    def levels(name, rank=None):
        _, fs = validate(name, rank)
        return {(f.level, f.article) for f in fs}

    # Art. 28: initial letters, both directions.
    assert ("violation", "Art. 28") in levels("panthera onca")
    assert ("violation", "Art. 28") in levels("Panthera Onca")
    assert ("violation", "Art. 28") not in levels("Panthera onca")
    # Art. 27 / 11.2: marks are a spelling defect, not an availability defect.
    assert ("violation", "Art. 27") in levels("Aus mülleri")
    assert ("violation", "Art. 11.2") in levels("Aus bus2")
    # Art. 3: the 1758 starting point.
    assert ("violation", "Art. 3") in levels("Aus bus Linnaeus, 1757")
    assert ("violation", "Art. 3") not in levels("Aus bus Linnaeus, 1758")
    # Art. 11.8 / 11.9.1: two-letter minimum.
    assert ("violation", "Art. 11.8") in levels("A bus")
    assert ("violation", "Art. 11.9.1") in levels("Aus b")
    # Art. 29.2: suffix must match the declared rank, and is only judged when known.
    assert ("violation", "Art. 29.2") in levels("Felinae", rank="family")
    assert ("violation", "Art. 29.2") not in levels("Felidae", rank="family")
    assert not any(l == "violation" for l, _ in levels("Ranoidea"))  # Art. 29.2.1
    # Art. 31.2 stays a warning, and must not fire on a genitive eponym (Art. 11.9.1.3).
    assert ("warning", "Art. 31.2") in levels("Aus rubrum")
    assert ("warning", "Art. 31.2") not in levels("Aus smithi")
    assert ("warning", "Art. 31.2") not in levels("Aus timorensis")
    # Art. 51.3: parentheses reported as combination-dependent, never as an error.
    assert ("info", "Art. 51.3") in levels("Panthera onca (Linnaeus, 1758)")
    assert not any(l == "violation" for l, _ in levels("Panthera onca (Linnaeus, 1758)"))
    # Art. 18: a tautonym is available.
    assert ("info", "Art. 18") in levels("Bison bison")
    # Arts. 57.2 and 58 in the cross-file scan.
    ps = [parse("Aus bus Smith, 1900"), parse("Aus bus Jones, 1950")]
    assert any(f.level == "violation" and f.article == "Art. 57.2"
               for f in homonym_scan(ps))
    ps = [parse("Aus caeruleus Smith, 1900"), parse("Aus ceruleus Jones, 1950")]
    assert any(f.level == "warning" and f.article == "Art. 58" for f in homonym_scan(ps))
    # A genus is not a homonym of a same-named species in another genus (Art. 53.3).
    ps = [parse("Aus bus Smith, 1900"), parse("Xus bus Jones, 1950")]
    assert not any(f.level == "violation" for f in homonym_scan(ps))
    print("selftest: all assertions passed")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        main()
