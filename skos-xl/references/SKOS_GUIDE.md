# SKOS & SKOS-XL Quick Reference Guide

> W3C Recommendations:
> - SKOS: https://www.w3.org/TR/skos-reference/
> - SKOS-XL: https://www.w3.org/TR/skos-reference/skos-xl.html

---

## Namespaces

```turtle
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .
@prefix skosxl: <http://www.w3.org/2008/05/skos-xl#> .
@prefix dc:     <http://purl.org/dc/elements/1.1/> .
@prefix dct:    <http://purl.org/dc/terms/> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
```

---

## Core SKOS Pattern (Turtle)

```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix :     <http://example.org/vocab#> .

:MyVocabulary a skos:ConceptScheme ;
    skos:prefLabel "My Vocabulary"@en ;
    skos:hasTopConcept :TopConcept .

:TopConcept a skos:Concept ;
    skos:inScheme :MyVocabulary ;
    skos:topConceptOf :MyVocabulary ;
    skos:prefLabel "Top Concept"@en ;
    skos:altLabel "TC"@en ;
    skos:definition "The broadest concept in this vocabulary."@en ;
    skos:notation "01" ;
    skos:narrower :ChildConcept .

:ChildConcept a skos:Concept ;
    skos:inScheme :MyVocabulary ;
    skos:broader :TopConcept ;
    skos:prefLabel "Child Concept"@en ;
    skos:definition "A more specific concept."@en ;
    skos:notation "01.01" .
```

---

## SKOS-XL Pattern (Extended Labels)

```turtle
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .
@prefix skosxl: <http://www.w3.org/2008/05/skos-xl#> .
@prefix dc:     <http://purl.org/dc/elements/1.1/> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix :       <http://example.org/vocab#> .

:MammalConcept a skos:Concept ;
    skos:inScheme :MyVocabulary ;
    skosxl:prefLabel :label_mammal_en ;
    skosxl:altLabel  :label_mammalia .

:label_mammal_en a skosxl:Label ;
    skosxl:literalForm "mammal"@en ;
    dc:source <https://example.org/source> ;
    dc:created "2024-01-15"^^xsd:date .

:label_mammalia a skosxl:Label ;
    skosxl:literalForm "Mammalia"@la ;
    dc:description "Scientific Latin name"@en .
```

---

## When to Choose SKOS-XL over Plain SKOS

| Need | Plain SKOS | SKOS-XL |
|------|-----------|---------|
| Simple labels with language tags | ✓ | |
| Label provenance (source, date) | | ✓ |
| Label metadata (status, morphology) | | ✓ |
| Label-to-label relationships | | ✓ |
| Multilingual thesaurus with rich annotation | | ✓ |
| Interoperability with OntoLex/lemon | | ✓ |
| Minimal, lightweight vocabulary | ✓ | |

---

## SKOS Integrity Conditions (key rules)

1. **S9** — `skos:prefLabel`, `skos:altLabel`, `skos:hiddenLabel` are pairwise disjoint for a given resource and language tag.
2. **S13** — A resource cannot have more than one `skos:prefLabel` per language tag.
3. **S14** — Two concepts in the same ConceptScheme cannot share the same `skos:prefLabel` in the same language.
4. **S23** — `skos:broader` and `skos:narrower` are inverse properties.
5. **S27** — `skos:related` must not be used to link a concept to its ancestor or descendant in the broader/narrower hierarchy.
6. **S37** — `skos:exactMatch` is transitive; `skos:closeMatch` is not.

---

## Mapping Relations (cross-vocabulary alignment)

```turtle
# Concepts from different schemes
:BirdConcept skos:exactMatch   <http://vocab.getty.edu/aat/300249660> .
:BirdConcept skos:broadMatch   <http://example.org/otherVocab#Animal> .
:BirdConcept skos:closeMatch   <http://dbpedia.org/resource/Bird> .
:BirdConcept skos:relatedMatch <http://example.org/otherVocab#Wings> .
```

---

## Collections

```turtle
# Unordered collection (no hierarchy implied)
:HabitatTypes a skos:Collection ;
    skos:prefLabel "Habitat Types"@en ;
    skos:member :Forest, :Wetland, :Grassland .

# Ordered collection
:PreferredOrder a skos:OrderedCollection ;
    skos:prefLabel "Preferred display order"@en ;
    skos:memberList ( :Forest :Grassland :Wetland ) .
```

---

## SKOS-XL Label Relations

```turtle
# Linking two labels (e.g., abbreviation derived from full form)
:label_full a skosxl:Label ;
    skosxl:literalForm "Deoxyribonucleic acid"@en ;
    skosxl:labelRelation :label_abbrev .

:label_abbrev a skosxl:Label ;
    skosxl:literalForm "DNA"@en ;
    skosxl:labelRelation :label_full .
```

---

## Integration with Darwin Core

### Pattern 1 — SKOS vocabulary for DwC controlled values

SKOS is the recommended way to formally define the controlled vocabularies
behind Darwin Core terms like `basisOfRecord`, `occurrenceStatus`, etc.

```turtle
@prefix skos:  <http://www.w3.org/2004/02/skos/core#> .
@prefix dwc:   <http://rs.tdwg.org/dwc/terms/> .
@prefix :      <http://example.org/basisOfRecord#> .

:BasisOfRecordVocab a skos:ConceptScheme ;
    skos:prefLabel "Darwin Core Basis of Record Vocabulary"@en ;
    skos:hasTopConcept :PreservedSpecimen, :HumanObservation,
                       :MachineObservation, :MaterialSample,
                       :LivingSpecimen, :FossilSpecimen .

:PreservedSpecimen a skos:Concept ;
    skos:inScheme :BasisOfRecordVocab ;
    skos:topConceptOf :BasisOfRecordVocab ;
    skos:prefLabel "PreservedSpecimen"@en ;
    skos:definition "A specimen that has been preserved."@en ;
    skos:notation "PreservedSpecimen" ;
    skos:exactMatch <http://rs.tdwg.org/dwc/dwctype/PreservedSpecimen> .

:HumanObservation a skos:Concept ;
    skos:inScheme :BasisOfRecordVocab ;
    skos:topConceptOf :BasisOfRecordVocab ;
    skos:prefLabel "HumanObservation"@en ;
    skos:definition "An output of a human observation process."@en ;
    skos:notation "HumanObservation" .
```

### Pattern 2 — SKOS-XL for taxonomic names (TDWG TAG NameThing pattern)

The TDWG Technical Architecture Group (TAG) uses SKOS-XL to model taxonomic
names as `tnc:NameThing` resources — separating label metadata (parsed name
components, authorship, orthographic variants) from the abstract concept identity.

This solves the DwC `dwc:` / `dwciri:` namespace split: `dwc:scientificName`
holds a plain literal, `dwciri:scientificName` holds an IRI — SKOS-XL unifies
both as an annotatable label resource.

Reference: https://github.com/tdwg/tag/tree/master/skos-xl

```turtle
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .
@prefix skosxl: <http://www.w3.org/2008/05/skos-xl#> .
@prefix tnc:    <http://example.org/tnc/> .
@prefix :       <http://example.org/names#> .

# Abstract name concept (the taxonomic identity)
:Dicranum_braunii a skos:Concept, tnc:NameThing ;
    skos:inScheme :BryophyteNames ;
    skosxl:prefLabel :label_dicranum_braunii_accepted ;
    skosxl:altLabel  :label_dicranum_braunii_orthvar .

# Accepted name label — with full nomenclatural metadata
:label_dicranum_braunii_accepted a skosxl:Label ;
    skosxl:literalForm   "Dicranum braunii Müll. Hal."@la ;
    tnc:canonicalName    "Dicranum braunii"@la ;
    tnc:genus            "Dicranum"@la ;
    tnc:specificEpithet  "braunii"@la ;
    tnc:authorship       "Müll. Hal."@la ;
    skosxl:labelRelation :label_dicranum_braunii_orthvar .

# Orthographic variant label
:label_dicranum_braunii_orthvar a skosxl:Label ;
    skosxl:literalForm "Dicranum brownii Müll. Hal."@la ;
    tnc:canonicalName  "Dicranum brownii"@la ;
    skosxl:labelRelation :label_dicranum_braunii_accepted .

# Basionym relationship between NameThings
:Dicranum_braunii tnc:hasBasionym :Fissidens_braunii .
```

### Key DwC terms that benefit from SKOS vocabularies

| DwC Term | SKOS Use | Pattern |
|----------|----------|---------|
| `basisOfRecord` | Controlled vocabulary with definitions | Pattern 1 |
| `occurrenceStatus` | `present` / `absent` concepts | Pattern 1 |
| `sex` | Multilingual labels | Pattern 1 |
| `lifeStage` | Hierarchical lifecycle stages | Pattern 1 |
| `establishmentMeans` | `native` / `introduced` / `invasive` | Pattern 1 |
| `degreeOfEstablishment` | Ordered progression | Pattern 1 |
| `pathway` | IUCN pathway hierarchy | Pattern 1 |
| `habitat` | EUNIS / IUCN habitat classification | Pattern 1 |
| `typeStatus` | Type specimen designations | Pattern 1 |
| `scientificName` | Taxonomic name with parsed components | Pattern 2 (NameThing) |
| `recordedBy` / `identifiedBy` | Person labels with provenance | Pattern 2 (skosxl:Label) |

---

## RDF Serialization Formats

| Format | Extension | Mime Type | Notes |
|--------|-----------|-----------|-------|
| Turtle | `.ttl` | `text/turtle` | Most readable, preferred for editing |
| RDF/XML | `.rdf` | `application/rdf+xml` | Legacy; required by some tools |
| JSON-LD | `.jsonld` | `application/ld+json` | Best for web APIs |
| N-Triples | `.nt` | `application/n-triples` | Line-based; good for diff/version control |
| N3 | `.n3` | `text/n3` | Turtle superset with rules |

---

---

## Traditional Knowledge (CTA) Pattern — EtnoTermos

### Context

Traditional Knowledge Associated with Biodiversity (CTA / Conhecimento Tradicional Associado)
requires a vocabulary architecture that is:
- **Polyglot**: multiple indigenous languages, each with its own metadata
- **Polyphonic**: multiple communities may name the same species differently
- **Governed**: per-label access control (public / restricted / sacred)
- **Attributed**: provenance traceable to the originating people (CARE principles)
- **Compliant**: Nagoya Protocol on Access and Benefit-Sharing

SKOS-XL is the correct choice because access restrictions live at the *label* level,
not the concept level. The scientific name of a plant may be public while the sacred
ritual name is restricted — impossible to model with `skos:prefLabel` literals.

### Namespaces

```turtle
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .
@prefix skosxl: <http://www.w3.org/2008/05/skos-xl#> .
@prefix etno:   <http://example.org/etno/> .
@prefix prov:   <http://www.w3.org/ns/prov#> .
@prefix dct:    <http://purl.org/dc/terms/> .
@prefix dwc:    <http://rs.tdwg.org/dwc/terms/> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
```

### Full EtnoTermos Pattern (Turtle)

```turtle
# ── ConceptScheme (CARE Authority) ──────────────────────────────
:EtnoTermos a skos:ConceptScheme ;
    skos:prefLabel "EtnoTermos - Vocabulario de Conhecimento Tradicional"@pt ;
    dct:rightsHolder "Conselho Aty Guasu"^^xsd:string ;
    dct:license <https://localcontexts.org/labels/traditional-knowledge-labels/> ;
    etno:nagoyaStatus "compliant" .

# ── Ethnotaxonomic category (NOT a western-science category) ────
:plantas-medicinais a skos:Concept ;
    skos:inScheme :EtnoTermos ;
    skos:topConceptOf :EtnoTermos ;
    skos:prefLabel "Plantas medicinais"@pt ;
    skos:scopeNote "Categoria etnotaxonomica; nao mapeada 1:1 para taxonomia ocidental."@pt .

# ── Concept with multilingual labels ───────────────────────────
:jatoba a skos:Concept ;
    skos:inScheme :EtnoTermos ;
    skos:broader :plantas-medicinais ;
    dwc:vernacularName "Jatoba" .

# Portuguese label (public)
:label/jatoba-pt a skosxl:Label ;
    skosxl:literalForm "Jatoba"@pt ;
    dct:language "pt" ;
    etno:accessLevel "public" .
:jatoba skosxl:prefLabel :label/jatoba-pt .

# Guarani Mbya label (ISO 639-3: gnm) — public, community-validated
:label/jatoba-guarani a skosxl:Label ;
    skosxl:literalForm "Jutai"@gnm ;
    dct:language "gnm" ;
    etno:sourcePeople "Guarani Mbya" ;
    etno:sourceRegion "Mata Atlantica meridional" ;
    etno:accessLevel "public" ;
    etno:validatedBy "Conselho Aty Guasu" ;
    prov:wasAttributedTo :povo/guarani-mbya ;
    dct:source <https://doi.org/10.XXXX/etno2019> ;
    etno:nagoyaStatus "compliant" .
:jatoba skosxl:altLabel :label/jatoba-guarani .

# Scientific name as alternative label (public)
:label/jatoba-sci a skosxl:Label ;
    skosxl:literalForm "Hymenaea courbaril L."@la ;
    dct:type "scientificName" ;
    etno:accessLevel "public" ;
    dct:source <https://floradobrasil.jbrj.gov.br/FB23011> .
:jatoba skosxl:altLabel :label/jatoba-sci .
:jatoba skos:exactMatch <https://floradobrasil.jbrj.gov.br/FB23011> .

# ── Concept with RESTRICTED/SACRED label ───────────────────────
:ayahuasca a skos:Concept ;
    skos:inScheme :EtnoTermos ;
    skos:broader :plantas-rituais ;
    skos:scopeNote "Alguns nomes sao sagrados. Ver etno:accessLevel por rotulo."@pt .

# Public generic label
:label/ayahuasca-es a skosxl:Label ;
    skosxl:literalForm "Ayahuasca"@es ;
    etno:accessLevel "public" .
:ayahuasca skosxl:prefLabel :label/ayahuasca-es .

# SACRED label — Huni Kui name (ISO 639-3: hux)
:label/nixi-pae a skosxl:Label ;
    skosxl:literalForm "Nixi Pae"@hux ;
    dct:language "hux" ;
    etno:sourcePeople "Huni Kui (Kaxinawa)" ;
    etno:sourceRegion "Alto Jurua, Acre" ;
    etno:accessLevel "sacred" ;
    etno:consentType "fpic" ;
    etno:validatedBy "ASKARJ" ;
    prov:wasAttributedTo :povo/huni-kui ;
    etno:nagoyaStatus "restricted" ;
    etno:languageStatus "vulnerable" .
:ayahuasca skosxl:altLabel :label/nixi-pae .

# ── Indigenous people as PROV Agent ────────────────────────────
:povo/guarani-mbya a prov:Agent ;
    skos:prefLabel "Guarani Mbya"@pt .

:povo/huni-kui a prov:Agent ;
    skos:prefLabel "Huni Kui (Kaxinawa)"@pt .
```

### etno: Property Reference

| Property | CARE | Description |
|---|---|---|
| `etno:sourcePeople` | Collective | Indigenous people attribution (use endonym) |
| `etno:sourceRegion` | Collective | Geographic territory or biome |
| `etno:accessLevel` | Authority | `public` / `restricted` / `community-only` / `sacred` |
| `etno:validatedBy` | Responsibility | Community organization that validated |
| `etno:pronunciationAudio` | Collective | URI to audio recording |
| `etno:dialectVariant` | Collective | Dialectal variation note |
| `etno:languageStatus` | Ethics | UNESCO vitality: safe/vulnerable/endangered/extinct |
| `etno:consentType` | Authority | `none-required` / `fpic` / `restricted` |
| `etno:nagoyaStatus` | Responsibility | `compliant` / `pending` / `restricted` / `not-applicable` |
| `etno:tkLabel` | Authority/Ethics | Local Contexts TK Label applied |

Standard properties also used on labels:
- `prov:wasAttributedTo` — links label to PROV Agent (people/community)
- `dct:source` — bibliographic or consultation reference
- `dct:rightsHolder` — community/org holding rights (on ConceptScheme)
- `dct:license` — TK Label or license (on ConceptScheme)
- `dct:language` — ISO 639-3 code
- `dwc:vernacularName` — Darwin Core bridge on the Concept

### ISO 639-3 Codes for Brazilian Indigenous Languages (examples)

| Code | Language | People |
|---|---|---|
| `hux` | Huni Kuĩ | Kaxinawá |
| `gnm` | Guarani Mbya | Guarani Mbya |
| `tup` | Tupí | Tupí |
| `xav` | Xavánte | Xavánte |
| `kyr` | Kuruáya | Kuruáya |
| `jab` | Jabuti | Jabuti |
| `ore` | Orejón | Orejón/Maijuna |
| `yon` | Yawanapi | Yawanapi |

Full list: https://iso639-3.sil.org/

### Key References

- CARE Principles: https://www.gida-global.org/care
- Nagoya Protocol: https://www.cbd.int/abs/
- Local Contexts TK Labels: https://localcontexts.org/labels/traditional-knowledge-labels/
- PROV-O: https://www.w3.org/TR/prov-o/
- EtnoTermos / JBRJ: https://etnotermos.jbrj.gov.br/
- VocBench 3 (best SKOS-XL editor): https://vocbench.uniroma2.it/

---

## Common Biodiversity SKOS Vocabularies

| Vocabulary | URI | Description |
|-----------|-----|-------------|
| GBIF Vocabulary Bank | https://rs.gbif.org/vocabulary/ | DwC controlled vocabularies |
| IUCN Habitat Classification | https://www.iucnredlist.org/resources/habitat-classification-scheme | Hierarchical habitat types |
| IUCN Threats Classification | https://www.iucnredlist.org/resources/threat-classification-scheme | Threat categories |
| EUNIS Habitat Types | https://eunis.eea.europa.eu/habitats.jsp | European habitat classification |
| SWEET Ontology | https://sweetontology.net | Earth and environmental science terms |
| ENVO | http://www.obofoundry.org/ontology/envo.html | Environment Ontology |
