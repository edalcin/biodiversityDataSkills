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
    python scripts/explain.py --cta                  # Traditional Knowledge (CARE) overview
    python scripts/explain.py --cta --term accessLevel  # Explain a CTA property
    python scripts/explain.py --cta --list           # List all CTA properties
"""

import argparse
import csv
import sys
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REF_DIR = Path(__file__).resolve().parent.parent / "references"
SKOS_CSV   = REF_DIR / "skos_terms.csv"
SKOSXL_CSV = REF_DIR / "skos_xl_terms.csv"
CTA_CSV    = REF_DIR / "traditional_knowledge_properties.csv"


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


def show_cta_overview(terms):
    print("=" * 70)
    print("  CTA - Conhecimento Tradicional Associado a Biodiversidade")
    print("  Traditional Knowledge (SKOS-XL + CARE + Nagoya Protocol)")
    print("=" * 70)
    print()
    print("Para vocabularios de Conhecimento Tradicional Associado (CTA),")
    print("SKOS-XL e a escolha correta: permite anotar cada rotulo indigena")
    print("com povo de origem, nivel de acesso, validacao comunitaria e")
    print("proveniencia — impossivel com skos:prefLabel literal.")
    print()
    print("[CARE Principles] https://www.gida-global.org/care")
    print("   C - Coletividade (Collective)   -- atribuicao ao povo detentor")
    print("   A - Autoridade (Authority)       -- controle comunitario sobre os dados")
    print("   R - Responsabilidade (Responsibility) -- proveniencia rastreavel")
    print("   E - Etica (Ethics)               -- nao causar dano; respeitar restricoes")
    print()
    print("[Protocolo de Nagoya] https://www.cbd.int/abs/")
    print("   Exige Consentimento Previo Informado (FPIC) para acesso a CTA.")
    print("   etno:nagoyaStatus e etno:consentType codificam conformidade.")
    print()
    print("[Niveis de Acesso] (etno:accessLevel)")
    print("   public         -- disponivel a qualquer usuario")
    print("   restricted     -- somente pesquisadores com FPIC")
    print("   community-only -- somente membros da comunidade")
    print("   sacred         -- sagrado; nunca publicar sem autorizacao explicita")
    print()
    print("[TK Labels] https://localcontexts.org/labels/traditional-knowledge-labels/")
    print("   Licencas controladas por comunidades indigenas para CTA.")
    print("   Use dct:license para associar ao ConceptScheme.")
    print()
    print("[ISO 639-3 para linguas indigenas] https://iso639-3.sil.org/")
    print("   Exemplos: hux = Huni Kui (Kaxinawa)  |  gnm = Guarani Mbya")
    print("             tup = Tupi                  |  yor = Yoruba")
    print()
    print("[Propriedades recomendadas em skosxl:Label]")
    print("   etno:sourcePeople     -- povo de origem do rotulo")
    print("   etno:sourceRegion     -- territorio/regiao geografica")
    print("   etno:accessLevel      -- public / restricted / community-only / sacred")
    print("   etno:validatedBy      -- organizacao representativa que validou")
    print("   etno:pronunciationAudio -- URI para audio com pronuncia")
    print("   prov:wasAttributedTo  -- entidade PROV (CARE Coletividade)")
    print("   dct:source            -- referencia bibliografica ou consulta")
    print("   etno:nagoyaStatus     -- conformidade com Protocolo de Nagoya")
    print("   etno:consentType      -- none-required / fpic / restricted")
    print("   etno:languageStatus   -- vitalidade da lingua (UNESCO)")
    print()
    print("[Namespace etno:]")
    print("   @prefix etno: <http://example.org/etno/> .")
    print("   (substitua pelo URI definitivo do seu projeto)")
    print()
    print("[Ferramentas que suportam SKOS-XL bem]")
    print("   VocBench 3  -- open-source, usado por FAO/Agrovoc")
    print("   PoolParty   -- enterprise")
    print("   Skosmos     -- publicacao/consulta de vocabularios")
    print()
    props = sum(1 for t in terms if t)
    print("[Stats] %d propriedades/classes CTA documentadas" % props)
    print()
    print("Use --term <nome> para detalhes. Use --list para listar.")
    print("Gere um vocabulario CTA: python scripts/generate.py meu_vocab --template etno-tk")
    print("Valide com CARE checks: python scripts/validate.py vocab.ttl --cta")


def show_cta_term(terms, term_name):
    norm = term_name.lower().replace("etno:", "").replace("prov:", "").replace("dct:", "")
    found = [t for t in terms if t.get("property", "").lower() == norm]
    if not found:
        print("[ERROR] Propriedade '%s' nao encontrada." % term_name)
        print("   Use --list para ver todas as propriedades CTA.")
        return
    for t in found:
        ns = t.get("namespace", "etno")
        print("[%s:%s]" % (ns, t["property"]))
        print("   URI: %s" % t.get("uri", ""))
        print("   Principio CARE: %s" % t.get("care_principle", ""))
        print("   Definicao: %s" % t.get("definition", ""))
        if t.get("notes"):
            print("   Notas: %s" % t["notes"])
        print()


def list_cta_terms(terms):
    print("[Lista] Propriedades CTA para vocabularios de Conhecimento Tradicional")
    print()
    etno_props = [t for t in terms if t.get("namespace") == "etno"]
    other_props = [t for t in terms if t.get("namespace") != "etno"]
    if etno_props:
        print("  Propriedades etno: (namespace: http://example.org/etno/)")
        for t in etno_props:
            care = t.get("care_principle", "")
            print("    %-30s [%s]" % (t["property"], care))
        print()
    if other_props:
        print("  Propriedades de vocabularios padrao (PROV-O, Dublin Core, DwC):")
        for t in other_props:
            print("    %s:%-24s %s" % (
                t.get("namespace", "?"), t["property"],
                t.get("definition", "")[:45]))
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Explains SKOS, SKOS-XL, and Traditional Knowledge (CTA) terms"
    )
    parser.add_argument("--term", "-t",
                        help="Term name to explain (e.g. broader, prefLabel, Label, accessLevel)")
    parser.add_argument("--list", "-l",
                        action="store_true", help="List all terms")
    parser.add_argument("--xl",
                        action="store_true", help="Target SKOS-XL namespace")
    parser.add_argument("--cta",
                        action="store_true",
                        help="Traditional Knowledge / Conhecimento Tradicional properties")
    args = parser.parse_args()

    if args.cta:
        terms = load_terms(CTA_CSV)
        if args.term:
            show_cta_term(terms, args.term)
        elif args.list:
            list_cta_terms(terms)
        else:
            show_cta_overview(terms)
    elif args.xl:
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
