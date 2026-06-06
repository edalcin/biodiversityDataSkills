---
name: skos-xl
description: >
  Helps users build, validate, convert, and explore controlled vocabularies
  using SKOS (Simple Knowledge Organization System) and SKOS-XL (the W3C
  extension for annotatable labels). Supports Darwin Core integration for
  biodiversity vocabularies (basisOfRecord, habitat types, taxonomic names).
  Use when the user mentions "SKOS", "SKOS-XL", "thesaurus", "controlled
  vocabulary", "concept scheme", "RDF vocabulary", "taxonomic names vocabulary",
  "Darwin Core vocabulary", "skos:Concept", "prefLabel", or "broadMatch".
license: MIT
compatibility: Python 3.9+
metadata:
  author: biodiversityDataSkills
  repository: https://github.com/<your-username>/biodiversityDataSkills
---

# SKOS-XL Skill

Skill for building and working with [SKOS](https://www.w3.org/TR/skos-reference/) (Simple Knowledge Organization System) and [SKOS-XL](https://www.w3.org/TR/skos-reference/skos-xl.html) vocabularies, with first-class support for Darwin Core integration following the [TDWG TAG SKOS-XL patterns](https://github.com/tdwg/tag/tree/master/skos-xl).

---

## Setup

### 1. Install Python 3.9+

```bash
python --version
```

### 2. Install dependencies

```bash
cd /path/to/skos-xl
pip install -r requirements.txt
```

One dependency: [`rdflib`](https://rdflib.readthedocs.io/) — handles all RDF formats (Turtle, RDF/XML, JSON-LD, N-Triples) and the SKOS namespace natively.

### 3. (Optional) Sync W3C schema files

Downloads the official SKOS/SKOS-XL RDF/OWL schemas and TDWG TAG examples:

```bash
python scripts/sync.py
```

---

## Usage

### 1. Explain SKOS and SKOS-XL

General SKOS overview:

```bash
python scripts/explain.py
```

Explain a specific SKOS term:

```bash
python scripts/explain.py --term broader
python scripts/explain.py --term prefLabel
python scripts/explain.py --term exactMatch
```

List all SKOS terms:

```bash
python scripts/explain.py --list
```

SKOS-XL overview (when to use XL vs plain SKOS):

```bash
python scripts/explain.py --xl
```

Explain a specific SKOS-XL term:

```bash
python scripts/explain.py --xl --term Label
python scripts/explain.py --xl --term literalForm
python scripts/explain.py --xl --list
```

---

### 2. Validate a SKOS vocabulary file

Validates Turtle, RDF/XML, JSON-LD, N-Triples, or N3 files.

Checks run:
1. File parses as valid RDF
2. Contains at least one `skos:ConceptScheme`
3. All `skos:Concept` instances linked via `skos:inScheme`
4. Each concept has `skos:prefLabel` (or `skosxl:prefLabel`)
5. No duplicate `prefLabel` in the same language within a scheme (S14)
6. No disjointness violations (`Concept` / `ConceptScheme` / `Collection`)
7. `skos:related` not used between broader/narrower concepts (S27)
8. SKOS-XL: each `skosxl:Label` has exactly one `skosxl:literalForm`

```bash
python scripts/validate.py vocab.ttl
python scripts/validate.py vocab.ttl --verbose
python scripts/validate.py vocab.rdf --format xml
python scripts/validate.py vocab.jsonld --format json-ld
```

Exit code `0` on success, `1` if errors are found (suitable for CI pipelines).

---

### 3. Generate a SKOS vocabulary template

Three templates are available:

| Template | Use case |
|---|---|
| `basic` (default) | Generic concept hierarchy with optional SKOS-XL labels |
| `dwc-vocab` | Darwin Core controlled vocabulary (basisOfRecord, occurrenceStatus, etc.) |
| `dwc-names` | Taxonomic name vocabulary using the TDWG TAG NameThing pattern (SKOS-XL) |

**Basic vocabulary** (plain SKOS):

```bash
python scripts/generate.py my_vocab
```

**Basic vocabulary** with SKOS-XL labels:

```bash
python scripts/generate.py my_vocab --xl
```

**Darwin Core controlled vocabulary** (e.g. for `basisOfRecord`):

```bash
python scripts/generate.py basisOfRecord --template dwc-vocab
```

**Taxonomic name vocabulary** (TDWG TAG NameThing pattern, SKOS-XL):

```bash
python scripts/generate.py my_names --template dwc-names
```

**Change output format and language**:

```bash
python scripts/generate.py my_vocab --format jsonld --lang pt
python scripts/generate.py my_vocab --format rdfxml --dir ./output
python scripts/generate.py my_vocab --base http://vocab.example.org/myVocab
```

Supported formats: `turtle` (default), `rdfxml`, `jsonld`, `nt`, `n3`

---

### 4. Convert vocabulary format or label style

**Convert RDF serialization format**:

```bash
python scripts/convert.py vocab.rdf --to-format turtle
python scripts/convert.py vocab.ttl --to-format jsonld --output vocab.jsonld
```

**Upgrade plain SKOS labels to SKOS-XL** (adds URI resources for each label):

```bash
python scripts/convert.py vocab.ttl --to-xl
```

**Downgrade SKOS-XL labels to plain SKOS** (extracts `literalForm` literals back to `skos:prefLabel`):

```bash
python scripts/convert.py vocab_xl.ttl --from-xl
```

**Combine operations** (upgrade labels + change format):

```bash
python scripts/convert.py vocab.ttl --to-xl --to-format jsonld
```

---

### 5. Sync reference files

Downloads W3C SKOS/SKOS-XL schemas and TDWG TAG Turtle examples:

```bash
python scripts/sync.py
```

---

## Darwin Core Integration

SKOS is the recommended representation for Darwin Core controlled vocabularies.
Two patterns are supported by this skill:

### Pattern 1 — Controlled vocabulary for DwC term values

Used for terms like `basisOfRecord`, `occurrenceStatus`, `sex`, `lifeStage`,
`establishmentMeans`, `degreeOfEstablishment`, `habitat`:

```bash
python scripts/generate.py basisOfRecord --template dwc-vocab
```

Each concept maps to the authoritative TDWG IRI via `skos:exactMatch`.

### Pattern 2 — Taxonomic name vocabulary (TDWG TAG NameThing)

Reference: [tdwg/tag/skos-xl](https://github.com/tdwg/tag/tree/master/skos-xl)

Used for scientific names. Labels become `skosxl:Label` resources carrying
parsed nomenclatural components:
- `skosxl:literalForm` — full name string (e.g. `"Dicranum braunii Müll. Hal."@la`)
- `tnc:canonicalName` — genus + epithet without authorship
- `tnc:genus`, `tnc:specificEpithet`, `tnc:authorship`
- `skosxl:labelRelation` subproperties for basionyms and orthographic variants

This resolves the `dwc:` / `dwciri:` namespace split: SKOS-XL Labels provide
a single IRI-addressable resource that bridges both.

```bash
python scripts/generate.py bryophytes --template dwc-names
```

---

## Key DwC Terms That Benefit from SKOS Vocabularies

| DwC Term | Template | Notes |
|---|---|---|
| `basisOfRecord` | `dwc-vocab` | 6 standard values |
| `occurrenceStatus` | `dwc-vocab` | `present` / `absent` |
| `sex` | `dwc-vocab` | Multilingual labels |
| `lifeStage` | `dwc-vocab` | Hierarchical stages |
| `establishmentMeans` | `dwc-vocab` | IUCN pathway-aligned |
| `degreeOfEstablishment` | `dwc-vocab` | Ordered progression |
| `typeStatus` | `dwc-vocab` | Type specimen designations |
| `habitat` | `dwc-vocab` | EUNIS / IUCN hierarchy |
| `scientificName` | `dwc-names` | NameThing with parsed components |
| `recordedBy` / `identifiedBy` | `dwc-names` | Person labels with provenance |

---

## References

- [SKOS terms reference](references/skos_terms.csv) — 4 classes, 28 properties
- [SKOS-XL terms reference](references/skos_xl_terms.csv) — 1 class, 5 properties
- [SKOS & SKOS-XL Quick Reference Guide](references/SKOS_GUIDE.md) — patterns, examples, DwC integration
- [SKOS Core schema](references/skos_core.rdf) — official W3C RDF/OWL (after `sync.py`)
- [SKOS-XL schema](references/skos_xl.rdf) — official W3C RDF/OWL (after `sync.py`)
- [TDWG TAG NameThing](references/tdwg_skosxl_name.ttl) — Turtle example (after `sync.py`)

---

## Related Skills

**[darwin-core](../darwin-core/)** — Use alongside this skill to package and validate occurrence data. Darwin Core defines the fields; SKOS defines the controlled vocabularies for the values. The `dwc-vocab` template generates SKOS representations of any Darwin Core controlled term.
