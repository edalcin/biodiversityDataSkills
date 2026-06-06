#!/usr/bin/env python3
"""
validate.py - Validates a SKOS vocabulary file.

Supports: Turtle (.ttl), RDF/XML (.rdf .owl .xml), JSON-LD (.jsonld), N-Triples (.nt), N3 (.n3)

Checks:
  1. File parses as valid RDF
  2. Contains at least one skos:ConceptScheme
  3. All skos:Concept instances linked via skos:inScheme
  4. Each concept has at least one skos:prefLabel (or skosxl:prefLabel)
  5. No duplicate prefLabels in the same language within a scheme
  6. No disjointness violations (Concept / ConceptScheme / Collection)
  7. skos:related not used between directly broader/narrower concepts (S27)
  8. SKOS-XL: each skosxl:Label has exactly one skosxl:literalForm

Usage:
    python scripts/validate.py vocab.ttl
    python scripts/validate.py vocab.ttl --verbose
    python scripts/validate.py vocab.rdf --format xml
"""

import argparse
import sys
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    from rdflib import Graph, Namespace, RDF, RDFS
    from rdflib.namespace import SKOS
except ImportError:
    print("[ERROR] rdflib not installed. Run: pip install rdflib")
    sys.exit(1)

SKOSXL = Namespace("http://www.w3.org/2008/05/skos-xl#")


def detect_format(path):
    return {
        ".ttl": "turtle",
        ".n3": "n3",
        ".nt": "nt",
        ".rdf": "xml",
        ".owl": "xml",
        ".xml": "xml",
        ".jsonld": "json-ld",
        ".json": "json-ld",
    }.get(Path(path).suffix.lower(), "turtle")


def label_of(g, uri):
    val = (g.value(uri, SKOS.prefLabel)
           or g.value(uri, RDFS.label)
           or uri)
    return str(val)


def main():
    parser = argparse.ArgumentParser(description="Validates a SKOS vocabulary file")
    parser.add_argument("file", help="Path to SKOS vocabulary file")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show warnings in addition to errors")
    parser.add_argument("--format", "-f",
                        help="RDF format override: turtle, xml, json-ld, nt, n3")
    args = parser.parse_args()

    errors = []
    warnings = []

    print()
    print("[Validate] %s" % args.file)
    print("=" * 60)

    # 1. Parse RDF
    print("[1/8] Parsing RDF...")
    fmt = args.format or detect_format(args.file)
    print("   Format: %s" % fmt)
    g = Graph()
    try:
        g.parse(args.file, format=fmt)
        print("   [OK] Parsed (%d triples)" % len(g))
    except Exception as e:
        print("   [ERROR] Parse failed: %s" % e)
        sys.exit(1)

    concepts = set(g.subjects(RDF.type, SKOS.Concept))
    schemes = set(g.subjects(RDF.type, SKOS.ConceptScheme))
    collections = set(g.subjects(RDF.type, SKOS.Collection))
    xl_labels = set(g.subjects(RDF.type, SKOSXL.Label))

    print("   [Info] %d concept(s), %d scheme(s), %d collection(s)" % (
        len(concepts), len(schemes), len(collections)))
    if xl_labels:
        print("   [Info] %d SKOS-XL Label(s) detected" % len(xl_labels))

    # 2. ConceptScheme present
    print("[2/8] Checking ConceptScheme...")
    if not schemes:
        errors.append("No skos:ConceptScheme found. Vocabulary must have at least one.")
        print("   [ERROR] No ConceptScheme found")
    else:
        for s in schemes:
            print("   [OK] %s" % label_of(g, s))

    # 3. inScheme links
    print("[3/8] Checking skos:inScheme links...")
    no_scheme = [c for c in concepts if not list(g.objects(c, SKOS.inScheme))]
    if no_scheme:
        for c in no_scheme[:5]:
            warnings.append("Concept not linked via inScheme: %s" % c)
        if len(no_scheme) > 5:
            warnings.append("... and %d more concept(s) without inScheme" % (len(no_scheme) - 5))
        print("   [WARN] %d concept(s) without skos:inScheme" % len(no_scheme))
    else:
        print("   [OK] All %d concept(s) linked to a ConceptScheme" % len(concepts))

    # 4. prefLabel present
    print("[4/8] Checking skos:prefLabel...")
    no_pref = []
    for c in concepts:
        has_plain = any(True for _ in g.objects(c, SKOS.prefLabel))
        has_xl = any(True for _ in g.objects(c, SKOSXL.prefLabel))
        if not has_plain and not has_xl:
            no_pref.append(c)
    if no_pref:
        for c in no_pref[:5]:
            errors.append("Concept without prefLabel: %s" % c)
        if len(no_pref) > 5:
            errors.append("... and %d more concept(s) without prefLabel" % (len(no_pref) - 5))
        print("   [ERROR] %d concept(s) without prefLabel" % len(no_pref))
    else:
        print("   [OK] All concepts have prefLabel")

    # 5. Duplicate prefLabels within scheme (integrity condition S14)
    print("[5/8] Checking for duplicate prefLabels within scheme...")
    dup_errors = []
    for scheme in schemes:
        seen = {}
        for c in concepts:
            if (c, SKOS.inScheme, scheme) in g:
                for lbl in g.objects(c, SKOS.prefLabel):
                    key = (str(lbl.language), str(lbl))
                    if key in seen and seen[key] != c:
                        dup_errors.append(
                            "Duplicate prefLabel '%s'@%s in %s" % (
                                lbl, lbl.language, label_of(g, scheme))
                        )
                    else:
                        seen[key] = c
    if dup_errors:
        for e in dup_errors[:5]:
            errors.append(e)
            print("   [ERROR] %s" % e)
    else:
        print("   [OK] No duplicate prefLabels found")

    # 6. Disjointness (Concept / ConceptScheme / Collection)
    print("[6/8] Checking disjointness constraints...")
    disj = []
    for c in concepts:
        if c in schemes:
            disj.append("Resource is both Concept and ConceptScheme: %s" % c)
        if c in collections:
            disj.append("Resource is both Concept and Collection: %s" % c)
    for s in schemes:
        if s in collections:
            disj.append("Resource is both ConceptScheme and Collection: %s" % s)
    if disj:
        for e in disj:
            errors.append(e)
            print("   [ERROR] %s" % e)
    else:
        print("   [OK] No disjointness violations")

    # 7. skos:related + broader/narrower conflict (S27 — direct only)
    print("[7/8] Checking semantic relation integrity (S27)...")
    s27_issues = []
    for c in concepts:
        related = set(g.objects(c, SKOS.related))
        broader = set(g.objects(c, SKOS.broader))
        narrower = set(g.objects(c, SKOS.narrower))
        for r in related:
            if r in broader or r in narrower:
                s27_issues.append(
                    "skos:related used between hierarchically linked concepts: %s <-> %s" % (c, r)
                )
    if s27_issues:
        for w in s27_issues[:5]:
            warnings.append(w)
            print("   [WARN] %s" % w)
    else:
        print("   [OK] No S27 violations found")

    # 8. SKOS-XL literalForm integrity
    print("[8/8] Checking SKOS-XL Label integrity...")
    if xl_labels:
        xl_errors = []
        for lbl in xl_labels:
            forms = list(g.objects(lbl, SKOSXL.literalForm))
            if len(forms) == 0:
                xl_errors.append("skosxl:Label with no literalForm: %s" % lbl)
            elif len(forms) > 1:
                xl_errors.append("skosxl:Label with multiple literalForms (%d): %s" % (len(forms), lbl))
        if xl_errors:
            for e in xl_errors:
                errors.append(e)
                print("   [ERROR] %s" % e)
        else:
            print("   [OK] All %d SKOS-XL Label(s) have exactly one literalForm" % len(xl_labels))
    else:
        print("   [OK] No SKOS-XL labels present (skipping XL checks)")

    # Summary
    print()
    print("=" * 60)
    if not errors:
        print("[RESULT] Validation complete -- No errors found!")
    else:
        print("[RESULT] %d error(s) found" % len(errors))
        for e in errors:
            print("   . %s" % e)

    if warnings and args.verbose:
        print()
        print("[WARNINGS] %d warning(s):" % len(warnings))
        for w in warnings:
            print("   . %s" % w)
    elif warnings:
        print("[Info] %d warning(s) found (use --verbose to see)" % len(warnings))

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
