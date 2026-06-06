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

## Common Biodiversity SKOS Vocabularies

| Vocabulary | URI | Description |
|-----------|-----|-------------|
| GBIF Vocabulary Bank | https://rs.gbif.org/vocabulary/ | DwC controlled vocabularies |
| IUCN Habitat Classification | https://www.iucnredlist.org/resources/habitat-classification-scheme | Hierarchical habitat types |
| IUCN Threats Classification | https://www.iucnredlist.org/resources/threat-classification-scheme | Threat categories |
| EUNIS Habitat Types | https://eunis.eea.europa.eu/habitats.jsp | European habitat classification |
| SWEET Ontology | https://sweetontology.net | Earth and environmental science terms |
| ENVO | http://www.obofoundry.org/ontology/envo.html | Environment Ontology |
