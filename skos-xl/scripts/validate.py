#!/usr/bin/env python3
"""
validate.py - Validates a SKOS vocabulary file.

Supports: Turtle (.ttl), RDF/XML (.rdf .owl .xml), JSON-LD (.jsonld), N-Triples (.nt), N3 (.n3)

Standard checks (always run):
  1. File parses as valid RDF
  2. Contains at least one skos:ConceptScheme
  3. All skos:Concept instances linked via skos:inScheme
  4. Each concept has at least one skos:prefLabel (or skosxl:prefLabel)
  5. No duplicate prefLabels in the same language within a scheme (S14)
  6. No disjointness violations (Concept / ConceptScheme / Collection)
  7. skos:related not used between directly broader/narrower concepts (S27)
  8. SKOS-XL: each skosxl:Label has exactly one skosxl:literalForm

CTA checks (--cta flag, Traditional Knowledge / Conhecimento Tradicional):
  9.  ConceptScheme has dct:rightsHolder
  10. ConceptScheme has dct:license (TK Label or equivalent)
  11. Each SKOS-XL Label has etno:accessLevel
  12. SKOS-XL Labels with non-standard language tags have prov:wasAttributedTo
      or etno:sourcePeople (CARE Collective principle)
  13. Labels marked as 'restricted', 'community-only', or 'sacred' have
      etno:validatedBy or prov:wasAttributedTo

Usage:
    python scripts/validate.py vocab.ttl
    python scripts/validate.py vocab.ttl --verbose
    python scripts/validate.py vocab.ttl --cta
    python scripts/validate.py vocab.ttl --cta --verbose
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
DCT    = Namespace("http://purl.org/dc/terms/")
PROV   = Namespace("http://www.w3.org/ns/prov#")
ETNO   = Namespace("http://example.org/etno/")

# Standard BCP 47 / ISO 639-1 codes; tags NOT in this set are treated as
# potentially indigenous and checked for community attribution.
STANDARD_LANG_TAGS = {
    "en", "pt", "es", "fr", "de", "it", "nl", "ru", "zh", "ja", "ko",
    "ar", "la", "el", "pl", "cs", "sv", "da", "fi", "no", "hu", "ro",
    "bg", "hr", "sk", "sl", "lt", "lv", "et", "ca", "gl", "eu",
}


def detect_format(path):
    return {
        ".ttl": "turtle", ".n3": "n3", ".nt": "nt",
        ".rdf": "xml", ".owl": "xml", ".xml": "xml",
        ".jsonld": "json-ld", ".json": "json-ld",
    }.get(Path(path).suffix.lower(), "turtle")


def label_of(g, uri):
    val = g.value(uri, SKOS.prefLabel) or g.value(uri, RDFS.label) or uri
    return str(val)


def run_standard_checks(g, errors, warnings):
    concepts = set(g.subjects(RDF.type, SKOS.Concept))
    schemes = set(g.subjects(RDF.type, SKOS.ConceptScheme))
    collections = set(g.subjects(RDF.type, SKOS.Collection))
    xl_labels = set(g.subjects(RDF.type, SKOSXL.Label))

    print("   [Info] %d concept(s), %d scheme(s), %d collection(s)" % (
        len(concepts), len(schemes), len(collections)))
    if xl_labels:
        print("   [Info] %d SKOS-XL Label(s) detected" % len(xl_labels))

    # 2. ConceptScheme
    print("[2/8] Checking ConceptScheme...")
    if not schemes:
        errors.append("No skos:ConceptScheme found.")
        print("   [ERROR] No ConceptScheme found")
    else:
        for s in schemes:
            print("   [OK] %s" % label_of(g, s))

    # 3. inScheme
    print("[3/8] Checking skos:inScheme links...")
    no_scheme = [c for c in concepts if not list(g.objects(c, SKOS.inScheme))]
    if no_scheme:
        for c in no_scheme[:5]:
            warnings.append("Concept not linked via inScheme: %s" % c)
        if len(no_scheme) > 5:
            warnings.append("... and %d more without inScheme" % (len(no_scheme) - 5))
        print("   [WARN] %d concept(s) without skos:inScheme" % len(no_scheme))
    else:
        print("   [OK] All %d concept(s) linked to a ConceptScheme" % len(concepts))

    # 4. prefLabel
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
            errors.append("... and %d more without prefLabel" % (len(no_pref) - 5))
        print("   [ERROR] %d concept(s) without prefLabel" % len(no_pref))
    else:
        print("   [OK] All concepts have prefLabel")

    # 5. Duplicate prefLabels (S14)
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
                                lbl, lbl.language, label_of(g, scheme)))
                    else:
                        seen[key] = c
    if dup_errors:
        for e in dup_errors[:5]:
            errors.append(e)
            print("   [ERROR] %s" % e)
    else:
        print("   [OK] No duplicate prefLabels found")

    # 6. Disjointness
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

    # 7. S27 (related + broader/narrower)
    print("[7/8] Checking semantic relation integrity (S27)...")
    s27 = []
    for c in concepts:
        related = set(g.objects(c, SKOS.related))
        broader = set(g.objects(c, SKOS.broader))
        narrower = set(g.objects(c, SKOS.narrower))
        for r in related:
            if r in broader or r in narrower:
                s27.append("skos:related used with hierarchically linked concept: %s <-> %s" % (c, r))
    if s27:
        for w in s27[:5]:
            warnings.append(w)
            print("   [WARN] %s" % w)
    else:
        print("   [OK] No S27 violations found")

    # 8. SKOS-XL literalForm
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

    return schemes, xl_labels


def run_cta_checks(g, schemes, xl_labels, errors, warnings):
    """Additional checks for Traditional Knowledge (CTA) vocabularies.
    Based on CARE Principles and Nagoya Protocol requirements.
    """
    print()
    print("[CTA] Traditional Knowledge (CARE / Nagoya) checks")
    print("-" * 60)

    # 9. rightsHolder on ConceptScheme
    print("[CTA-1/5] Checking dct:rightsHolder on ConceptScheme...")
    no_rights = []
    for s in schemes:
        if not g.value(s, DCT.rightsHolder):
            no_rights.append(s)
    if no_rights:
        for s in no_rights:
            warnings.append("ConceptScheme missing dct:rightsHolder (CARE Authority): %s" % s)
            print("   [WARN] No dct:rightsHolder: %s" % label_of(g, s))
        print("   [Tip] Add: <scheme> dct:rightsHolder \"[Community name]\" .")
    else:
        print("   [OK] All schemes have dct:rightsHolder")

    # 10. license on ConceptScheme
    print("[CTA-2/5] Checking dct:license on ConceptScheme...")
    no_license = []
    for s in schemes:
        if not g.value(s, DCT.license):
            no_license.append(s)
    if no_license:
        for s in no_license:
            warnings.append("ConceptScheme missing dct:license (CARE Authority): %s" % s)
            print("   [WARN] No dct:license: %s" % label_of(g, s))
        print("   [Tip] Consider TK Labels: https://localcontexts.org/labels/traditional-knowledge-labels/")
    else:
        print("   [OK] All schemes have dct:license")

    # 11. accessLevel on XL Labels
    print("[CTA-3/5] Checking etno:accessLevel on SKOS-XL Labels...")
    no_access = []
    if xl_labels:
        for lbl in xl_labels:
            if not g.value(lbl, ETNO.accessLevel):
                no_access.append(lbl)
        if no_access:
            for lbl in no_access[:5]:
                warnings.append("SKOS-XL Label missing etno:accessLevel: %s" % lbl)
                print("   [WARN] No accessLevel: %s" % lbl)
            if len(no_access) > 5:
                print("   [WARN] ... and %d more without accessLevel" % (len(no_access) - 5))
            print("   [Tip] Valid values: public / restricted / community-only / sacred")
        else:
            print("   [OK] All %d SKOS-XL Labels have etno:accessLevel" % len(xl_labels))
    else:
        print("   [SKIP] No SKOS-XL labels detected (consider using etno-tk template)")

    # 12. Attribution for non-standard language labels (CARE Collective)
    print("[CTA-4/5] Checking attribution for indigenous language labels...")
    unattributed = []
    if xl_labels:
        for lbl in xl_labels:
            form = g.value(lbl, SKOSXL.literalForm)
            if form is None:
                continue
            lang_tag = str(form.language) if form.language else ""
            if lang_tag.lower() not in STANDARD_LANG_TAGS and lang_tag != "":
                has_attrib = (
                    g.value(lbl, PROV.wasAttributedTo) is not None
                    or g.value(lbl, ETNO.sourcePeople) is not None
                )
                if not has_attrib:
                    unattributed.append((lbl, lang_tag))
        if unattributed:
            for lbl, lang in unattributed[:5]:
                warnings.append(
                    "Label in language '%s' has no attribution "
                    "(prov:wasAttributedTo / etno:sourcePeople): %s" % (lang, lbl))
                print("   [WARN] No attribution for @%s label: %s" % (lang, lbl))
            if len(unattributed) > 5:
                print("   [WARN] ... and %d more without attribution" % (len(unattributed) - 5))
        else:
            print("   [OK] All non-standard language labels have attribution")
    else:
        print("   [SKIP] No SKOS-XL labels to check")

    # 13. Restricted/sacred labels require validation record
    print("[CTA-5/5] Checking sensitive labels have validatedBy/attribution...")
    sensitive_levels = {"restricted", "community-only", "sacred"}
    no_validation = []
    if xl_labels:
        for lbl in xl_labels:
            access = g.value(lbl, ETNO.accessLevel)
            if access and str(access).lower() in sensitive_levels:
                has_validated = g.value(lbl, ETNO.validatedBy) is not None
                has_prov = g.value(lbl, PROV.wasAttributedTo) is not None
                if not has_validated and not has_prov:
                    no_validation.append((lbl, str(access)))
        if no_validation:
            for lbl, lvl in no_validation[:5]:
                warnings.append(
                    "Label with accessLevel='%s' has no etno:validatedBy or "
                    "prov:wasAttributedTo: %s" % (lvl, lbl))
                print("   [WARN] '%s' label without validation record: %s" % (lvl, lbl))
        else:
            print("   [OK] All sensitive labels have validation records")
    else:
        print("   [SKIP] No SKOS-XL labels to check")


def main():
    parser = argparse.ArgumentParser(description="Validates a SKOS vocabulary file")
    parser.add_argument("file", help="Path to SKOS vocabulary file")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show warnings in addition to errors")
    parser.add_argument("--cta", action="store_true",
                        help="Run additional CTA (Traditional Knowledge / CARE) checks")
    parser.add_argument("--format", "-f",
                        help="RDF format override: turtle, xml, json-ld, nt, n3")
    args = parser.parse_args()

    errors = []
    warnings = []

    print()
    print("[Validate] %s" % args.file)
    if args.cta:
        print("[Mode] Standard + CTA (Traditional Knowledge / CARE / Nagoya)")
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

    schemes, xl_labels = run_standard_checks(g, errors, warnings)

    if args.cta:
        run_cta_checks(g, schemes, xl_labels, errors, warnings)

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
        print("[Info] %d warning(s) (use --verbose to see)" % len(warnings))

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
