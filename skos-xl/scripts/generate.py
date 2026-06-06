#!/usr/bin/env python3
"""
generate.py - Generates a SKOS vocabulary template.

Templates:
  basic      -- Simple ConceptScheme with hierarchy and related concepts
  dwc-vocab  -- Darwin Core controlled vocabulary (e.g. basisOfRecord values)
  dwc-names  -- TDWG TAG NameThing pattern for taxonomic names (SKOS-XL)

Usage:
    python scripts/generate.py my_vocab
    python scripts/generate.py my_vocab --template dwc-vocab
    python scripts/generate.py my_vocab --template dwc-names
    python scripts/generate.py my_vocab --format jsonld
    python scripts/generate.py my_vocab --xl
    python scripts/generate.py my_vocab --lang pt
    python scripts/generate.py my_vocab --dir ./output
"""

import argparse
import sys
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    from rdflib import Graph, Literal, Namespace, RDF, URIRef
    from rdflib.namespace import SKOS, XSD
    DC = Namespace("http://purl.org/dc/elements/1.1/")
    DCT = Namespace("http://purl.org/dc/terms/")
except ImportError:
    print("[ERROR] rdflib not installed. Run: pip install rdflib")
    sys.exit(1)

SKOSXL = Namespace("http://www.w3.org/2008/05/skos-xl#")
DWC = Namespace("http://rs.tdwg.org/dwc/terms/")
DWCTYPE = Namespace("http://rs.tdwg.org/dwc/dwctype/")
TNC = Namespace("http://example.org/tnc/")

FORMAT_EXT = {
    "turtle": ".ttl",
    "xml": ".rdf",
    "json-ld": ".jsonld",
    "nt": ".nt",
    "n3": ".n3",
}

FORMAT_ALIASES = {
    "ttl": "turtle", "turtle": "turtle",
    "rdfxml": "xml", "rdf": "xml", "xml": "xml",
    "jsonld": "json-ld", "json-ld": "json-ld", "json": "json-ld",
    "nt": "nt", "n3": "n3",
}


def bind_common(g, vocab_ns):
    g.bind("skos", SKOS)
    g.bind("skosxl", SKOSXL)
    g.bind("dc", DC)
    g.bind("dct", DCT)
    g.bind("vocab", vocab_ns)


def build_basic(name, lang, use_xl, base_uri):
    g = Graph()
    V = Namespace(base_uri + "#")
    bind_common(g, V)

    scheme = V["scheme"]
    g.add((scheme, RDF.type, SKOS.ConceptScheme))
    g.add((scheme, SKOS.prefLabel, Literal(name, lang=lang)))
    g.add((scheme, DC.description,
           Literal("SKOS vocabulary generated with skos-xl skill.", lang="en")))

    top = V["concept_01"]
    g.add((top, RDF.type, SKOS.Concept))
    g.add((top, SKOS.inScheme, scheme))
    g.add((top, SKOS.topConceptOf, scheme))
    g.add((scheme, SKOS.hasTopConcept, top))
    g.add((top, SKOS.notation, Literal("01")))
    g.add((top, SKOS.definition, Literal("Definition of concept 01.", lang="en")))
    g.add((top, SKOS.scopeNote, Literal("Scope note for concept 01.", lang="en")))

    narrow = V["concept_01_01"]
    g.add((narrow, RDF.type, SKOS.Concept))
    g.add((narrow, SKOS.inScheme, scheme))
    g.add((narrow, SKOS.broader, top))
    g.add((top, SKOS.narrower, narrow))
    g.add((narrow, SKOS.notation, Literal("01.01")))
    g.add((narrow, SKOS.definition, Literal("Definition of concept 01.01.", lang="en")))

    rel = V["concept_02"]
    g.add((rel, RDF.type, SKOS.Concept))
    g.add((rel, SKOS.inScheme, scheme))
    g.add((rel, SKOS.topConceptOf, scheme))
    g.add((scheme, SKOS.hasTopConcept, rel))
    g.add((rel, SKOS.notation, Literal("02")))
    g.add((rel, SKOS.related, top))
    g.add((top, SKOS.related, rel))

    # External mapping example
    g.add((top, SKOS.exactMatch,
           URIRef("http://example.org/external#concept_A")))

    entries = [(top, "01", "Concept 01", "C01"),
               (narrow, "01.01", "Concept 01.01", "C01.01"),
               (rel, "02", "Concept 02", "C02")]

    if use_xl:
        g.bind("skosxl", SKOSXL)
        for concept, code, pref_text, alt_text in entries:
            lid_pref = V["label_%s_pref" % code.replace(".", "_")]
            g.add((lid_pref, RDF.type, SKOSXL.Label))
            g.add((lid_pref, SKOSXL.literalForm, Literal(pref_text, lang=lang)))
            g.add((concept, SKOSXL.prefLabel, lid_pref))
            lid_alt = V["label_%s_alt" % code.replace(".", "_")]
            g.add((lid_alt, RDF.type, SKOSXL.Label))
            g.add((lid_alt, SKOSXL.literalForm, Literal(alt_text, lang=lang)))
            g.add((concept, SKOSXL.altLabel, lid_alt))
    else:
        for concept, _, pref_text, alt_text in entries:
            g.add((concept, SKOS.prefLabel, Literal(pref_text, lang=lang)))
            g.add((concept, SKOS.altLabel, Literal(alt_text, lang=lang)))

    return g


def build_dwc_vocab(name, lang, base_uri):
    """Template for a DwC controlled vocabulary (e.g. basisOfRecord values)."""
    g = Graph()
    V = Namespace(base_uri + "#")
    bind_common(g, V)
    g.bind("dwc", DWC)
    g.bind("dwctype", DWCTYPE)

    scheme = V["scheme"]
    g.add((scheme, RDF.type, SKOS.ConceptScheme))
    g.add((scheme, SKOS.prefLabel,
           Literal("%s Vocabulary" % name, lang=lang)))
    g.add((scheme, DC.description,
           Literal("Controlled vocabulary for Darwin Core term %s." % name, lang="en")))
    g.add((scheme, DCT.conformsTo,
           URIRef("https://dwc.tdwg.org/terms/")))

    values = [
        ("PreservedSpecimen",
         "A specimen that has been preserved.",
         URIRef("http://rs.tdwg.org/dwc/dwctype/PreservedSpecimen")),
        ("HumanObservation",
         "An output of a human observation process.",
         URIRef("http://rs.tdwg.org/dwc/dwctype/HumanObservation")),
        ("MachineObservation",
         "An output of a machine observation process.",
         URIRef("http://rs.tdwg.org/dwc/dwctype/MachineObservation")),
        ("MaterialSample",
         "A physical result of a sampling (or sub-sampling) event.",
         URIRef("http://rs.tdwg.org/dwc/dwctype/MaterialSample")),
        ("LivingSpecimen",
         "A specimen that is alive.",
         URIRef("http://rs.tdwg.org/dwc/dwctype/LivingSpecimen")),
        ("FossilSpecimen",
         "A preserved specimen that is a fossil.",
         URIRef("http://rs.tdwg.org/dwc/dwctype/FossilSpecimen")),
    ]

    for val_name, defn, exact_uri in values:
        concept = V[val_name]
        g.add((concept, RDF.type, SKOS.Concept))
        g.add((concept, SKOS.inScheme, scheme))
        g.add((concept, SKOS.topConceptOf, scheme))
        g.add((scheme, SKOS.hasTopConcept, concept))
        g.add((concept, SKOS.prefLabel, Literal(val_name, lang=lang)))
        g.add((concept, SKOS.notation, Literal(val_name)))
        g.add((concept, SKOS.definition, Literal(defn, lang="en")))
        g.add((concept, SKOS.exactMatch, exact_uri))

    return g


def build_dwc_names(name, lang, base_uri):
    """Template: TDWG TAG NameThing pattern for taxonomic names (SKOS-XL).
    Reference: https://github.com/tdwg/tag/tree/master/skos-xl
    """
    g = Graph()
    V = Namespace(base_uri + "#")
    bind_common(g, V)
    g.bind("tnc", TNC)

    scheme = V["scheme"]
    g.add((scheme, RDF.type, SKOS.ConceptScheme))
    g.add((scheme, SKOS.prefLabel,
           Literal("%s Name Vocabulary" % name, lang=lang)))
    g.add((scheme, DC.description,
           Literal("Taxonomic name vocabulary using TDWG TAG SKOS-XL NameThing pattern.", lang="en")))

    # NameThing 1 — accepted name
    thing1 = V["name_001"]
    g.add((thing1, RDF.type, SKOS.Concept))
    g.add((thing1, RDF.type, TNC.NameThing))
    g.add((thing1, SKOS.inScheme, scheme))
    g.add((thing1, SKOS.topConceptOf, scheme))
    g.add((scheme, SKOS.hasTopConcept, thing1))

    lbl1_pref = V["label_name_001_pref"]
    g.add((lbl1_pref, RDF.type, SKOSXL.Label))
    g.add((lbl1_pref, SKOSXL.literalForm,
           Literal("Dicranum braunii Mull. Hal.", lang="la")))
    g.add((lbl1_pref, TNC.canonicalName,
           Literal("Dicranum braunii", lang="la")))
    g.add((lbl1_pref, TNC.genus, Literal("Dicranum", lang="la")))
    g.add((lbl1_pref, TNC.specificEpithet, Literal("braunii", lang="la")))
    g.add((lbl1_pref, TNC.authorship, Literal("Mull. Hal.", lang="la")))
    g.add((thing1, SKOSXL.prefLabel, lbl1_pref))

    lbl1_alt = V["label_name_001_orthvar"]
    g.add((lbl1_alt, RDF.type, SKOSXL.Label))
    g.add((lbl1_alt, SKOSXL.literalForm,
           Literal("Dicranum brownii Mull. Hal.", lang="la")))
    g.add((lbl1_alt, TNC.canonicalName,
           Literal("Dicranum brownii", lang="la")))
    g.add((thing1, SKOSXL.altLabel, lbl1_alt))

    # labelRelation: orthographic variant correction
    g.add((lbl1_alt, SKOSXL.labelRelation, lbl1_pref))
    g.add((lbl1_pref, SKOSXL.labelRelation, lbl1_alt))

    # NameThing 2 — basionym
    thing2 = V["name_002"]
    g.add((thing2, RDF.type, SKOS.Concept))
    g.add((thing2, RDF.type, TNC.NameThing))
    g.add((thing2, SKOS.inScheme, scheme))
    g.add((thing2, SKOS.topConceptOf, scheme))
    g.add((scheme, SKOS.hasTopConcept, thing2))

    lbl2_pref = V["label_name_002_pref"]
    g.add((lbl2_pref, RDF.type, SKOSXL.Label))
    g.add((lbl2_pref, SKOSXL.literalForm,
           Literal("Fissidens braunii Mull. Hal.", lang="la")))
    g.add((lbl2_pref, TNC.canonicalName,
           Literal("Fissidens braunii", lang="la")))
    g.add((lbl2_pref, TNC.genus, Literal("Fissidens", lang="la")))
    g.add((lbl2_pref, TNC.specificEpithet, Literal("braunii", lang="la")))
    g.add((lbl2_pref, TNC.authorship, Literal("Mull. Hal.", lang="la")))
    g.add((thing2, SKOSXL.prefLabel, lbl2_pref))

    # Nomenclatural relationship
    g.add((thing1, TNC.hasBasionym, thing2))
    g.add((thing1, SKOS.related, thing2))
    g.add((thing2, SKOS.related, thing1))

    # Common name label (plain SKOS on the concept)
    g.add((thing1, SKOS.altLabel, Literal("Example moss species", lang="en")))

    return g


def main():
    parser = argparse.ArgumentParser(description="Generates a SKOS vocabulary template")
    parser.add_argument("name", help="Vocabulary name (used as filename and label)")
    parser.add_argument(
        "--template", "-t", default="basic",
        choices=["basic", "dwc-vocab", "dwc-names"],
        help="Template: basic (default), dwc-vocab, dwc-names"
    )
    parser.add_argument(
        "--format", "-f", default="turtle",
        help="Output format: turtle (default), rdfxml, jsonld, nt, n3"
    )
    parser.add_argument("--xl", action="store_true",
                        help="Use SKOS-XL labels (only for 'basic' template; dwc-names uses XL by design)")
    parser.add_argument("--lang", "-l", default="en",
                        help="Language tag for labels (default: en)")
    parser.add_argument("--dir", "-d", default=".",
                        help="Output directory (default: current)")
    parser.add_argument("--base", "-b",
                        help="Base URI (default: http://example.org/<name>)")
    args = parser.parse_args()

    fmt = FORMAT_ALIASES.get(args.format.lower(), args.format)
    ext = FORMAT_EXT.get(fmt, ".ttl")
    base_uri = args.base or ("http://example.org/%s" % args.name)

    out_dir = Path(args.dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / ("%s%s" % (args.name, ext))

    use_xl = args.xl or (args.template == "dwc-names")

    print()
    print("[Generate] SKOS vocabulary: %s" % args.name)
    print("   Template: %s" % args.template)
    print("   Format  : %s" % fmt)
    print("   Labels  : %s" % ("SKOS-XL" if use_xl else "Plain SKOS"))
    print("   Language: %s" % args.lang)
    print("   Base URI: %s" % base_uri)
    print("   Output  : %s" % out_file)
    print()

    if args.template == "dwc-vocab":
        g = build_dwc_vocab(args.name, args.lang, base_uri)
    elif args.template == "dwc-names":
        g = build_dwc_names(args.name, args.lang, base_uri)
    else:
        g = build_basic(args.name, args.lang, use_xl, base_uri)

    try:
        g.serialize(destination=str(out_file), format=fmt)
        print("[OK] Vocabulary written to: %s" % out_file)
        print("[Info] %d triples generated" % len(g))
        print()
        print("[Next steps]")
        print("   1. Edit %s with your own concepts" % out_file)
        print("   2. Validate: python scripts/validate.py %s" % out_file)
        if use_xl:
            print("   3. Convert to plain SKOS if needed:")
            print("         python scripts/convert.py %s --from-xl" % out_file)
        print("   4. Explain terms: python scripts/explain.py --term broader")
    except Exception as e:
        print("[ERROR] Failed to write: %s" % e)
        sys.exit(1)


if __name__ == "__main__":
    main()
