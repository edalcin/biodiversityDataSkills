#!/usr/bin/env python3
"""
explain.py - Explains SKOS and SKOS-XL terms and vocabulary concepts.

Usage:
    python scripts/explain.py                        # SKOS overview
    python scripts/explain.py --term prefLabel       # Explain a specific term
    python scripts/explain.py --term skos:broader    # Explain with prefix
    python scripts/explain.py --list                 # List all SKOS terms
    python scripts/explain.py --xl                   # SKOS-XL overview
    python scripts/explain.py --xl --term Label      # Explain a SKOS-XL term
    python scripts/explain.py --xl --list            # List all SKOS-XL terms
"""

import argparse
import csv
import sys
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REF_DIR = Path(__file__).resolve().parent.parent / "references"
SKOS_CSV = REF_DIR / "skos_terms.csv"
SKOSXL_CSV = REF_DIR / "skos_xl_terms.csv"


def load_terms(csv_path):
    terms = []
    if not csv_path.exists():
        print("[WARN] %s not found." % csv_path.name)
        return terms
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            terms.append(row)
    return terms


def show_skos_overview(terms):
    print("=" * 70)
    print("  SKOS - Simple Knowledge Organization System")
    print("  W3C Recommendation | https://www.w3.org/TR/skos-reference/")
    print("=" * 70)
    print()
    print("SKOS is a W3C standard for representing thesauri, classification")
    print("schemes, subject heading systems, and taxonomies as Linked Data (RDF).")
    print()
    print("[Core Classes]")
    print("   skos:Concept           -- A unit of thought (idea, notion, term)")
    print("   skos:ConceptScheme     -- A vocabulary/container holding concepts")
    print("   skos:Collection        -- A labeled group of concepts (no hierarchy)")
    print("   skos:OrderedCollection -- A sequenced group of concepts")
    print()
    print("[Label Properties]")
    print("   skos:prefLabel    -- Preferred label (one per language per concept)")
    print("   skos:altLabel     -- Synonyms, acronyms, spelling variants")
    print("   skos:hiddenLabel  -- Hidden search terms (not displayed in UI)")
    print()
    print("[Documentation Properties]")
    print("   skos:definition   -- Formal definition of a concept")
    print("   skos:scopeNote    -- Guidance on how/when to use the concept")
    print("   skos:example      -- Example of the concept in use")
    print("   skos:note         -- General note (parent of all doc properties)")
    print("   skos:changeNote   -- Record of modification")
    print("   skos:historyNote  -- Historical usage note")
    print("   skos:editorialNote -- Internal editorial comment (not for end-users)")
    print()
    print("[Semantic Relations]")
    print("   skos:broader  -- Parent concept (more general)")
    print("   skos:narrower -- Child concept (more specific)")
    print("   skos:related  -- Associative, non-hierarchical link (symmetric)")
    print()
    print("[Mapping Relations] (cross-vocabulary alignment)")
    print("   skos:exactMatch   -- Interchangeable concepts (transitive)")
    print("   skos:closeMatch   -- Near-equivalent (not transitive)")
    print("   skos:broadMatch   -- External concept is broader")
    print("   skos:narrowMatch  -- External concept is narrower")
    print("   skos:relatedMatch -- Cross-vocabulary associative link")
    print()
    print("[Notation]")
    print("   skos:notation     -- Classification code (e.g. DDC '004.6', '01.03')")
    print()
    classes = sum(1 for t in terms if t.get("type") == "Class")
    props = sum(1 for t in terms if t.get("type") == "Property")
    print("[Stats] %d classes, %d properties" % (classes, props))
    print()
    print("[Namespaces]")
    print("   @prefix skos: <http://www.w3.org/2004/02/skos/core#> .")
    print("   @prefix skosxl: <http://www.w3.org/2008/05/skos-xl#> .")
    print()
    print("Use --term <name> for details on any term.")
    print("Use --list to see all terms.")
    print("Use --xl for SKOS-XL (extended label support).")


def show_skosxl_overview(terms):
    print("=" * 70)
    print("  SKOS-XL - SKOS eXtension for Labels")
    print("  W3C Recommendation | https://www.w3.org/TR/skos-reference/skos-xl.html")
    print("=" * 70)
    print()
    print("SKOS-XL extends SKOS to treat labels as first-class RDF resources,")
    print("allowing metadata, provenance, and relationships to be attached to")
    print("labels themselves -- not just to concepts.")
    print()
    print("[When to use SKOS-XL instead of plain SKOS]")
    print("   . Store metadata per label (source, date, status, morphology)")
    print("   . Create label-to-label relationships (derivation, etymology)")
    print("   . Manage multilingual labels with rich annotation")
    print("   . Interoperability with linguistic linked data (lemon, OntoLex)")
    print("   . Model taxonomic names with parsed components (TDWG TAG pattern)")
    print()
    print("[SKOS-XL Class]")
    print("   skosxl:Label        -- An RDF resource representing one label")
    print("     REQUIRED: exactly one skosxl:literalForm per Label instance")
    print()
    print("[SKOS-XL Properties]")
    print("   skosxl:prefLabel    -- Links concept to its preferred Label resource")
    print("   skosxl:altLabel     -- Links concept to an alternative Label resource")
    print("   skosxl:hiddenLabel  -- Links concept to a hidden Label resource")
    print("   skosxl:literalForm  -- The actual text of a Label (on Label itself)")
    print("   skosxl:labelRelation -- Links two Label resources (symmetric)")
    print()
    print("[Namespace]")
    print("   @prefix skosxl: <http://www.w3.org/2008/05/skos-xl#> .")
    print()
    print("[Plain SKOS vs SKOS-XL]")
    print()
    print("   Plain SKOS:")
    print('   :mammal skos:prefLabel "mammal"@en ;')
    print('           skos:altLabel  "Mammalia"@la .')
    print()
    print("   SKOS-XL (with label metadata):")
    print('   :mammal skosxl:prefLabel :label_mammal_en .')
    print('   :label_mammal_en a skosxl:Label ;')
    print('       skosxl:literalForm "mammal"@en ;')
    print('       dc:source <https://example.org/source> ;')
    print('       dc:created "2024-01-01"^^xsd:date .')
    print()
    print("[TDWG TAG NameThing pattern]")
    print("   TDWG uses SKOS-XL to model taxonomic names as annotatable labels:")
    print("   - skosxl:literalForm  = full name string")
    print("   - tnc:canonicalName   = genus + epithet without authorship")
    print("   - tnc:genus / tnc:specificEpithet / tnc:authorship = parsed parts")
    print("   - skosxl:labelRelation subproperties = basionym, orthographic variant")
    print("   See: https://github.com/tdwg/tag/tree/master/skos-xl")
    print()
    print("Use --term <name> for details. Use --list for all SKOS-XL terms.")


def normalize_term(name):
    if ":" in name:
        return name.split(":")[-1].lower()
    return name.lower()


def show_term_detail(terms, term_name, vocab="SKOS"):
    norm = normalize_term(term_name)
    found = [t for t in terms if t.get("term", "").lower() == norm]
    if not found:
        print("[ERROR] Term '%s' not found in %s." % (term_name, vocab))
        print("   Use --list to see all available terms.")
        return
    for t in found:
        print("[%s:%s] (%s)" % (vocab.lower().replace("-", ""), t["term"], t["type"]))
        print("   URI: %s" % t.get("uri", ""))
        print("   Definition: %s" % t.get("definition", ""))
        if t.get("notes"):
            print("   Notes: %s" % t["notes"])
        print()


def list_terms(terms, vocab="SKOS"):
    classes = [t for t in terms if t.get("type") == "Class"]
    props = [t for t in terms if t.get("type") == "Property"]
    print("[List] %s terms (%d total)" % (vocab, len(terms)))
    print()
    if classes:
        print("  Classes:")
        for t in classes:
            defn = t.get("definition", "")
            short = defn[:55] + "..." if len(defn) > 55 else defn
            print("    %-28s %s" % (t["term"], short))
        print()
    if props:
        print("  Properties:")
        col_width = 28
        cols = 3
        names = [t["term"] for t in props]
        for i, name in enumerate(names):
            print("  %-*s" % (col_width, name), end="")
            if (i + 1) % cols == 0:
                print()
        if len(names) % cols != 0:
            print()
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Explains SKOS and SKOS-XL terms"
    )
    parser.add_argument("--term", "-t",
                        help="Term name to explain (e.g. broader, prefLabel, Label)")
    parser.add_argument("--list", "-l",
                        action="store_true", help="List all terms")
    parser.add_argument("--xl",
                        action="store_true", help="Target SKOS-XL namespace")
    args = parser.parse_args()

    if args.xl:
        terms = load_terms(SKOSXL_CSV)
        vocab = "SKOS-XL"
        if args.term:
            show_term_detail(terms, args.term, vocab)
        elif args.list:
            list_terms(terms, vocab)
        else:
            show_skosxl_overview(terms)
    else:
        terms = load_terms(SKOS_CSV)
        vocab = "SKOS"
        if args.term:
            show_term_detail(terms, args.term, vocab)
        elif args.list:
            list_terms(terms, vocab)
        else:
            show_skos_overview(terms)


if __name__ == "__main__":
    main()
