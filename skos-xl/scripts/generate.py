#!/usr/bin/env python3
"""
generate.py - Generates a SKOS vocabulary template.

Templates:
  basic      -- Simple ConceptScheme with hierarchy and related concepts
  dwc-vocab  -- Darwin Core controlled vocabulary (e.g. basisOfRecord values)
  dwc-names  -- TDWG TAG NameThing pattern for taxonomic names (SKOS-XL)
  etno-tk    -- Traditional Knowledge (CTA) vocabulary with CARE/PROV-O metadata

Usage:
    python scripts/generate.py my_vocab
    python scripts/generate.py my_vocab --template dwc-vocab
    python scripts/generate.py my_vocab --template dwc-names
    python scripts/generate.py my_vocab --template etno-tk
    python scripts/generate.py my_vocab --template etno-tk --lang pt
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
DWC    = Namespace("http://rs.tdwg.org/dwc/terms/")
DWCTYPE = Namespace("http://rs.tdwg.org/dwc/dwctype/")
TNC    = Namespace("http://example.org/tnc/")
PROV   = Namespace("http://www.w3.org/ns/prov#")
ETNO   = Namespace("http://example.org/etno/")

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

    thing1 = V["name_001"]
    g.add((thing1, RDF.type, SKOS.Concept))
    g.add((thing1, RDF.type, TNC.NameThing))
    g.add((thing1, SKOS.inScheme, scheme))
    g.add((thing1, SKOS.topConceptOf, scheme))
    g.add((scheme, SKOS.hasTopConcept, thing1))

    lbl1_pref = V["label_name_001_pref"]
    g.add((lbl1_pref, RDF.type, SKOSXL.Label))
    g.add((lbl1_pref, SKOSXL.literalForm, Literal("Dicranum braunii Mull. Hal.", lang="la")))
    g.add((lbl1_pref, TNC.canonicalName, Literal("Dicranum braunii", lang="la")))
    g.add((lbl1_pref, TNC.genus, Literal("Dicranum", lang="la")))
    g.add((lbl1_pref, TNC.specificEpithet, Literal("braunii", lang="la")))
    g.add((lbl1_pref, TNC.authorship, Literal("Mull. Hal.", lang="la")))
    g.add((thing1, SKOSXL.prefLabel, lbl1_pref))

    lbl1_alt = V["label_name_001_orthvar"]
    g.add((lbl1_alt, RDF.type, SKOSXL.Label))
    g.add((lbl1_alt, SKOSXL.literalForm, Literal("Dicranum brownii Mull. Hal.", lang="la")))
    g.add((lbl1_alt, TNC.canonicalName, Literal("Dicranum brownii", lang="la")))
    g.add((thing1, SKOSXL.altLabel, lbl1_alt))
    g.add((lbl1_alt, SKOSXL.labelRelation, lbl1_pref))
    g.add((lbl1_pref, SKOSXL.labelRelation, lbl1_alt))

    thing2 = V["name_002"]
    g.add((thing2, RDF.type, SKOS.Concept))
    g.add((thing2, RDF.type, TNC.NameThing))
    g.add((thing2, SKOS.inScheme, scheme))
    g.add((thing2, SKOS.topConceptOf, scheme))
    g.add((scheme, SKOS.hasTopConcept, thing2))

    lbl2_pref = V["label_name_002_pref"]
    g.add((lbl2_pref, RDF.type, SKOSXL.Label))
    g.add((lbl2_pref, SKOSXL.literalForm, Literal("Fissidens braunii Mull. Hal.", lang="la")))
    g.add((lbl2_pref, TNC.canonicalName, Literal("Fissidens braunii", lang="la")))
    g.add((lbl2_pref, TNC.genus, Literal("Fissidens", lang="la")))
    g.add((lbl2_pref, TNC.specificEpithet, Literal("braunii", lang="la")))
    g.add((lbl2_pref, TNC.authorship, Literal("Mull. Hal.", lang="la")))
    g.add((thing2, SKOSXL.prefLabel, lbl2_pref))

    g.add((thing1, TNC.hasBasionym, thing2))
    g.add((thing1, SKOS.related, thing2))
    g.add((thing2, SKOS.related, thing1))
    g.add((thing1, SKOS.altLabel, Literal("Example moss species", lang="en")))

    return g


def build_etno_tk(name, lang, base_uri):
    """Template: Traditional Knowledge (CTA) vocabulary.

    Pattern: EtnoTermos / JBRJ — SKOS-XL labels with CARE metadata.
    Each label carries:
      - etno:sourcePeople  -- indigenous people attribution
      - etno:sourceRegion  -- geographic origin
      - etno:accessLevel   -- public / restricted / community-only / sacred
      - etno:validatedBy   -- validating community organization
      - prov:wasAttributedTo -- CARE Collective principle (PROV-O)
      - dct:source         -- bibliographic or consultation reference
      - dct:language       -- ISO 639-3 language code

    References:
      - CARE Principles: https://www.gida-global.org/care
      - Nagoya Protocol: https://www.cbd.int/abs/
      - Local Contexts TK Labels: https://localcontexts.org/labels/traditional-knowledge-labels/
      - ISO 639-3 (indigenous languages): https://iso639-3.sil.org/
    """
    g = Graph()
    V = Namespace(base_uri + "#")
    bind_common(g, V)
    g.bind("etno", ETNO)
    g.bind("prov", PROV)
    g.bind("xsd", XSD)
    g.bind("dwc", DWC)

    # ── ConceptScheme ─────────────────────────────────────────────
    scheme = V["scheme"]
    g.add((scheme, RDF.type, SKOS.ConceptScheme))
    g.add((scheme, SKOS.prefLabel,
           Literal("%s - Vocabulario de Conhecimento Tradicional" % name, lang="pt")))
    g.add((scheme, SKOS.prefLabel,
           Literal("%s - Traditional Knowledge Vocabulary" % name, lang="en")))
    g.add((scheme, DC.description,
           Literal(
               "Vocabulario de conhecimento tradicional associado a biodiversidade. "
               "Segue o padrao EtnoTermos/SKOS-XL com metadados CARE e Protocolo de Nagoya.",
               lang="pt")))
    # CARE — Authority: rights holder
    g.add((scheme, DCT.rightsHolder,
           Literal("[Nome do povo/comunidade detentora do saber]")))
    # CARE — Authority: license (TK Label recommended)
    g.add((scheme, DCT.license,
           URIRef("https://localcontexts.org/labels/traditional-knowledge-labels/")))
    g.add((scheme, ETNO.nagoyaStatus, Literal("compliant")))

    # ── Top-level categories (etnotaxonomia) ─────────────────────
    cat_medicinais = V["categoria/plantas-medicinais"]
    g.add((cat_medicinais, RDF.type, SKOS.Concept))
    g.add((cat_medicinais, SKOS.inScheme, scheme))
    g.add((cat_medicinais, SKOS.topConceptOf, scheme))
    g.add((scheme, SKOS.hasTopConcept, cat_medicinais))
    g.add((cat_medicinais, SKOS.prefLabel, Literal("Plantas medicinais", lang="pt")))
    g.add((cat_medicinais, SKOS.prefLabel, Literal("Medicinal plants", lang="en")))
    g.add((cat_medicinais, SKOS.definition,
           Literal("Plantas utilizadas para fins terapeuticos e de cura pela comunidade.", lang="pt")))
    g.add((cat_medicinais, SKOS.scopeNote,
           Literal("Categoria etnotaxonomica; nao corresponde necessariamente a uma categoria "
                   "da taxonomia cientifica ocidental.", lang="pt")))
    g.add((cat_medicinais, SKOS.notation, Literal("PM")))

    cat_rituais = V["categoria/plantas-rituais"]
    g.add((cat_rituais, RDF.type, SKOS.Concept))
    g.add((cat_rituais, SKOS.inScheme, scheme))
    g.add((cat_rituais, SKOS.topConceptOf, scheme))
    g.add((scheme, SKOS.hasTopConcept, cat_rituais))
    g.add((cat_rituais, SKOS.prefLabel, Literal("Plantas rituais", lang="pt")))
    g.add((cat_rituais, SKOS.prefLabel, Literal("Ritual plants", lang="en")))
    g.add((cat_rituais, SKOS.definition,
           Literal("Plantas com uso cerimonial, espiritual ou sagrado.", lang="pt")))
    g.add((cat_rituais, SKOS.notation, Literal("PR")))

    # ── Conceito 1: Jatoba ────────────────────────────────────────
    # (Hymenaea courbaril) — planta medicinal, acesso publico
    jatoba = V["conceito/jatoba"]
    g.add((jatoba, RDF.type, SKOS.Concept))
    g.add((jatoba, SKOS.inScheme, scheme))
    g.add((jatoba, SKOS.broader, cat_medicinais))
    g.add((cat_medicinais, SKOS.narrower, jatoba))
    g.add((jatoba, SKOS.definition,
           Literal("Arvore da familia Fabaceae, usada na medicina tradicional para afeccoes "
                   "respiratorias e como anti-inflamatorio.", lang="pt")))
    g.add((jatoba, SKOS.notation, Literal("PM.001")))
    # Bridge to Darwin Core
    g.add((jatoba, DWC.vernacularName, Literal("Jatoba")))

    # Label 1: nome em portugues (publico)
    lbl_jatoba_pt = V["label/jatoba-pt"]
    g.add((lbl_jatoba_pt, RDF.type, SKOSXL.Label))
    g.add((lbl_jatoba_pt, SKOSXL.literalForm, Literal("Jatoba", lang="pt")))
    g.add((lbl_jatoba_pt, DCT.language, Literal("pt")))
    g.add((lbl_jatoba_pt, ETNO.accessLevel, Literal("public")))
    g.add((jatoba, SKOSXL.prefLabel, lbl_jatoba_pt))

    # Label 2: nome em Guarani Mbya (ISO 639-3: gnm) — publico, validado
    lbl_jatoba_guarani = V["label/jatoba-guarani"]
    g.add((lbl_jatoba_guarani, RDF.type, SKOSXL.Label))
    g.add((lbl_jatoba_guarani, SKOSXL.literalForm, Literal("Jutai", lang="gnm")))
    g.add((lbl_jatoba_guarani, DCT.language, Literal("gnm")))  # ISO 639-3: Guarani Mbya
    g.add((lbl_jatoba_guarani, ETNO.sourcePeople, Literal("Guarani Mbya")))
    g.add((lbl_jatoba_guarani, ETNO.sourceRegion, Literal("Mata Atlantica meridional")))
    g.add((lbl_jatoba_guarani, ETNO.accessLevel, Literal("public")))
    g.add((lbl_jatoba_guarani, ETNO.validatedBy, Literal("Conselho Aty Guasu")))
    g.add((lbl_jatoba_guarani, PROV.wasAttributedTo, V["povo/guarani-mbya"]))
    g.add((lbl_jatoba_guarani, DCT.source,
           URIRef("https://doi.org/10.XXXX/etno2019")))
    g.add((lbl_jatoba_guarani, ETNO.nagoyaStatus, Literal("compliant")))
    g.add((jatoba, SKOSXL.altLabel, lbl_jatoba_guarani))

    # Label 3: nome cientifico como label alternativo (publico)
    lbl_jatoba_sci = V["label/jatoba-cientifico"]
    g.add((lbl_jatoba_sci, RDF.type, SKOSXL.Label))
    g.add((lbl_jatoba_sci, SKOSXL.literalForm, Literal("Hymenaea courbaril L.", lang="la")))
    g.add((lbl_jatoba_sci, DCT.language, Literal("la")))
    g.add((lbl_jatoba_sci, DCT.type, Literal("scientificName")))
    g.add((lbl_jatoba_sci, ETNO.accessLevel, Literal("public")))
    g.add((lbl_jatoba_sci, DCT.source,
           URIRef("https://floradobrasil.jbrj.gov.br/FB23011")))
    g.add((jatoba, SKOSXL.altLabel, lbl_jatoba_sci))

    # Mapping to Flora do Brasil / external vocabulary
    g.add((jatoba, SKOS.exactMatch,
           URIRef("https://floradobrasil.jbrj.gov.br/FB23011")))

    # ── Conceito 2: Ayahuasca ─────────────────────────────────────
    # Varios nomes em linguas indigenas — um deles sagrado/restrito
    ayahuasca = V["conceito/ayahuasca"]
    g.add((ayahuasca, RDF.type, SKOS.Concept))
    g.add((ayahuasca, SKOS.inScheme, scheme))
    g.add((ayahuasca, SKOS.broader, cat_rituais))
    g.add((cat_rituais, SKOS.narrower, ayahuasca))
    g.add((ayahuasca, SKOS.definition,
           Literal("Bebida ritual preparada a partir do cipo Banisteriopsis caapi e folhas de "
                   "Psychotria viridis. Uso cerimonial por povos indigenas da Amazonia.", lang="pt")))
    g.add((ayahuasca, SKOS.notation, Literal("PR.001")))
    g.add((ayahuasca, SKOS.scopeNote,
           Literal("Alguns nomes e conhecimentos associados a esta planta sao sagrados e de "
                   "acesso restrito. Ver etno:accessLevel em cada Label.", lang="pt")))

    # Label 1: nome espanhol/generico (publico)
    lbl_aya_es = V["label/ayahuasca-es"]
    g.add((lbl_aya_es, RDF.type, SKOSXL.Label))
    g.add((lbl_aya_es, SKOSXL.literalForm, Literal("Ayahuasca", lang="es")))
    g.add((lbl_aya_es, DCT.language, Literal("es")))
    g.add((lbl_aya_es, ETNO.accessLevel, Literal("public")))
    g.add((ayahuasca, SKOSXL.prefLabel, lbl_aya_es))

    # Label 2: nome Huni Kui (ISO 639-3: hux) — RESTRITO / sagrado
    lbl_nixi = V["label/nixi-pae"]
    g.add((lbl_nixi, RDF.type, SKOSXL.Label))
    g.add((lbl_nixi, SKOSXL.literalForm, Literal("Nixi Pae", lang="hux")))
    g.add((lbl_nixi, DCT.language, Literal("hux")))  # ISO 639-3: Huni Kui (Kaxinawa)
    g.add((lbl_nixi, ETNO.sourcePeople, Literal("Huni Kui (Kaxinawa)")))
    g.add((lbl_nixi, ETNO.sourceRegion, Literal("Alto Jurua, Acre")))
    g.add((lbl_nixi, ETNO.accessLevel, Literal("sacred")))
    g.add((lbl_nixi, ETNO.consentType, Literal("fpic")))
    g.add((lbl_nixi, PROV.wasAttributedTo, V["povo/huni-kui"]))
    g.add((lbl_nixi, ETNO.validatedBy, Literal("ASKARJ")))
    g.add((lbl_nixi, ETNO.validatedBy, Literal("Organizacao dos Agricultores e Indios do Alto Jurua")))
    g.add((lbl_nixi, ETNO.nagoyaStatus, Literal("restricted")))
    g.add((lbl_nixi, ETNO.languageStatus, Literal("vulnerable")))
    g.add((ayahuasca, SKOSXL.altLabel, lbl_nixi))

    # Label 3: nome em portugues (publico)
    lbl_aya_pt = V["label/cipo-mariri"]
    g.add((lbl_aya_pt, RDF.type, SKOSXL.Label))
    g.add((lbl_aya_pt, SKOSXL.literalForm, Literal("Cipo-mariri", lang="pt")))
    g.add((lbl_aya_pt, DCT.language, Literal("pt")))
    g.add((lbl_aya_pt, ETNO.accessLevel, Literal("public")))
    g.add((ayahuasca, SKOSXL.altLabel, lbl_aya_pt))

    # labelRelation: os dois nomes indigenas sao cognatos de origem diferente
    g.add((lbl_nixi, SKOSXL.labelRelation, lbl_aya_es))

    # ── Povo como recurso (PROV entity) ───────────────────────────
    guarani = V["povo/guarani-mbya"]
    g.add((guarani, RDF.type, PROV.Agent))
    g.add((guarani, RDF.type, URIRef("http://www.w3.org/ns/org#Organization")))
    g.add((guarani, SKOS.prefLabel, Literal("Guarani Mbya", lang="pt")))

    huni_kui = V["povo/huni-kui"]
    g.add((huni_kui, RDF.type, PROV.Agent))
    g.add((huni_kui, RDF.type, URIRef("http://www.w3.org/ns/org#Organization")))
    g.add((huni_kui, SKOS.prefLabel, Literal("Huni Kui (Kaxinawa)", lang="pt")))

    # ── Relacao entre conceitos (etnotaxonomia x taxonomia) ───────
    g.add((jatoba, SKOS.related, ayahuasca))
    g.add((ayahuasca, SKOS.related, jatoba))

    return g


def main():
    parser = argparse.ArgumentParser(description="Generates a SKOS vocabulary template")
    parser.add_argument("name", help="Vocabulary name (used as filename and label)")
    parser.add_argument(
        "--template", "-t", default="basic",
        choices=["basic", "dwc-vocab", "dwc-names", "etno-tk"],
        help="Template: basic (default), dwc-vocab, dwc-names, etno-tk"
    )
    parser.add_argument(
        "--format", "-f", default="turtle",
        help="Output format: turtle (default), rdfxml, jsonld, nt, n3"
    )
    parser.add_argument("--xl", action="store_true",
                        help="Use SKOS-XL labels (only for 'basic'; other templates use XL by design)")
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

    use_xl = args.xl or args.template in ("dwc-names", "etno-tk")

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
    elif args.template == "etno-tk":
        g = build_etno_tk(args.name, args.lang, base_uri)
    else:
        g = build_basic(args.name, args.lang, use_xl, base_uri)

    try:
        g.serialize(destination=str(out_file), format=fmt)
        print("[OK] Vocabulary written to: %s" % out_file)
        print("[Info] %d triples generated" % len(g))
        print()
        print("[Next steps]")
        print("   1. Edit %s with your own concepts and community data" % out_file)
        if args.template == "etno-tk":
            print("   2. Update dct:rightsHolder with the actual indigenous community name")
            print("   3. Replace etno:accessLevel placeholders with correct values")
            print("      Valid: public / restricted / community-only / sacred")
            print("   4. Add etno:pronunciationAudio URIs for indigenous labels")
            print("   5. Validate: python scripts/validate.py %s --cta" % out_file)
            print("   6. Explain CTA properties: python scripts/explain.py --cta")
        else:
            print("   2. Validate: python scripts/validate.py %s" % out_file)
        if use_xl:
            print("   . Convert to plain SKOS if needed:")
            print("         python scripts/convert.py %s --from-xl" % out_file)
    except Exception as e:
        print("[ERROR] Failed to write: %s" % e)
        sys.exit(1)


if __name__ == "__main__":
    main()
