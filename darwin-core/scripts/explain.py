#!/usr/bin/env python3
"""
explain.py - Explains the Darwin Core standard and its terms.

Usage:
    python scripts/explain.py                      # Overview
    python scripts/explain.py --term <term>        # Explain a specific term
    python scripts/explain.py --list               # List all available terms
"""

import argparse
import csv
import os
import sys
from pathlib import Path

# Ensure UTF-8 output (Windows fix)
if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REF_DIR = Path(__file__).resolve().parent.parent / "references"
TERMS_CSV = REF_DIR / "all_dwc_vertical.csv"
TERMS_DETAILED_CSV = REF_DIR / "term_versions.csv"


def load_term_names():
    """Load term names from the simple CSV list (all_dwc_vertical.csv)."""
    names = []
    if TERMS_CSV.exists():
        with open(TERMS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                t = row.get("type", "").strip()
                if t:
                    names.append(t)
    return names


def load_detailed_terms():
    """Load all terms with full metadata (term_versions.csv), deduplicated."""
    terms = []
    seen = set()
    if not TERMS_DETAILED_CSV.exists():
        print("[WARN] term_versions.csv not found. Run sync.py first.")
        return terms
    with open(TERMS_DETAILED_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("term_localName", "").strip()
            if name and name not in seen:
                seen.add(name)
                terms.append(row)
    return terms


def show_overview(terms):
    """Display a general overview of the Darwin Core standard."""
    print("=" * 70)
    print("  DARWIN CORE - Standard for Biodiversity Data")
    print("=" * 70)
    print()
    print("Darwin Core (DwC) is a standard maintained by TDWG (Biodiversity")
    print("Information Standards) for sharing information about biological")
    print("diversity.")
    print()
    print("[DwC-A] Darwin Core Archive")
    print("   A packaging format that combines:")
    print("   . meta.xml  -- description of the data structure")
    print("   . data.csv  -- table with records (occurrences, events, taxa)")
    print("   . extensions -- additional files with complementary info")
    print()
    print("[Cores] Main record types:")
    print("   . Occurrence  -- occurrence of an organism in nature")
    print("   . Event       -- sampling/collection event")
    print("   . Taxon       -- taxonomic classification")
    print()
    print("[Common extensions]:")
    print("   . MeasurementOrFact  -- measurements and attributes")
    print("   . Multimedia         -- images, audio, video")
    print("   . Identification     -- identification history")
    print("   . ResourceRelationship -- relationships between resources")
    print("   . DNADerivedData     -- DNA-derived data")
    print()

    total = len(terms)
    recommended = sum(1 for t in terms if t.get("status") == "recommended")
    print("[Stats] %d terms total, %d recommended" % (total, recommended))
    print()

    print("[Key terms]:")
    examples = [
        "occurrenceID", "scientificName", "decimalLatitude",
        "decimalLongitude", "eventDate", "basisOfRecord",
        "locality", "individualCount", "kingdom", "family"
    ]
    for name in examples:
        for t in terms:
            if t.get("term_localName") == name:
                print("   . %s: %s" % (name, t.get("label", "")))
                break
    print()
    print("Use --term <name> to see details for a specific term.")
    print("Use --list to see all available terms.")


def show_term_detail(terms, term_name):
    """Show detailed information for a specific term."""
    found = []
    for t in terms:
        if (t.get("term_localName", "").lower() == term_name.lower() or
            t.get("label", "").lower() == term_name.lower()):
            found.append(t)

    if not found:
        print("[ERROR] Term '%s' not found." % term_name)
        print("   Use --list to see all available terms.")
        return

    for t in found:
        print("[%s] (%s)" % (t.get("term_localName", ""), t.get("label", "")))
        print("   IRI: %s" % t.get("iri", ""))
        print("   Definition: %s" % t.get("definition", ""))
        if t.get("comments"):
            print("   Comments: %s" % t["comments"])
        if t.get("examples"):
            print("   Examples: %s" % t["examples"])
        print("   Organized in: %s" % t.get("organized_in", ""))
        print("   Version: %s" % t.get("issued", ""))
        print("   Status: %s" % t.get("status", ""))


def list_terms(names):
    """List all available terms in columns."""
    print("[List] All %d Darwin Core terms:" % len(names))
    print()
    col_width = 30
    cols = 3
    for i, name in enumerate(names):
        print("  %-*s" % (col_width, name), end="")
        if (i + 1) % cols == 0:
            print()
    if len(names) % cols != 0:
        print()
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Explains the Darwin Core standard and its terms"
    )
    parser.add_argument(
        "--term", "-t",
        help="Term name to explain (e.g. occurrenceID, decimalLatitude)"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available terms"
    )
    args = parser.parse_args()

    terms = load_detailed_terms()
    names = load_term_names()

    if args.term:
        show_term_detail(terms, args.term)
    elif args.list:
        list_terms(names)
    else:
        show_overview(terms)


if __name__ == "__main__":
    main()
