---
name: skos-xl
description: >
  Helps users build, validate, convert, and explore controlled vocabularies
  using SKOS (Simple Knowledge Organization System) and SKOS-XL (the W3C
  extension for annotatable labels). Supports Darwin Core integration for
  biodiversity vocabularies (basisOfRecord, habitat types, taxonomic names)
  and Traditional Knowledge (CTA/EtnoTermos) vocabularies with CARE principles,
  Nagoya Protocol compliance, per-label access control, and indigenous language
  attribution (PROV-O).
  Use when the user mentions "SKOS", "SKOS-XL", "thesaurus", "controlled
  vocabulary", "concept scheme", "RDF vocabulary", "taxonomic names vocabulary",
  "Darwin Core vocabulary", "conhecimento tradicional", "etnotermos",
  "CTA", "CARE principles", "Nagoya Protocol", "indigenous knowledge",
  "skos:Concept", "prefLabel", or "broadMatch".
license: MIT
compatibility: Python 3.9+
metadata:
  author: biodiversityDataSkills
  repository: https://github.com/edalcin/biodiversityDataSkills
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

### 1. Explain SKOS, SKOS-XL, and CTA properties

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

Traditional Knowledge (CTA) properties overview:

```bash
python scripts/explain.py --cta
python scripts/explain.py --cta --list
python scripts/explain.py --cta --term accessLevel
python scripts/explain.py --cta --term sourcePeople
python scripts/explain.py --cta --term nagoyaStatus
```

---

### 2. Validate a SKOS vocabulary file

Validates Turtle, RDF/XML, JSON-LD, N-Triples, or N3 files.

**Standard checks** (always run):
1. File parses as valid RDF
2. Contains at least one `skos:ConceptScheme`
3. All `skos:Concept` instances linked via `skos:inScheme`
4. Each concept has `skos:prefLabel` (or `skosxl:prefLabel`)
5. No duplicate `prefLabel` in the same language within a scheme (S14)
6. No disjointness violations (`Concept` / `ConceptScheme` / `Collection`)
7. `skos:related` not used between broader/narrower concepts (S27)
8. SKOS-XL: each `skosxl:Label` has exactly one `skosxl:literalForm`

**CTA checks** (`--cta` flag, Traditional Knowledge / CARE / Nagoya):
9. `ConceptScheme` has `dct:rightsHolder` (CARE Authority)
10. `ConceptScheme` has `dct:license` (TK Label recommended)
11. Each `skosxl:Label` has `etno:accessLevel`
12. Labels in non-standard languages have `prov:wasAttributedTo` or `etno:sourcePeople`
13. Labels with `accessLevel = restricted/sacred` have `etno:validatedBy` or `prov:wasAttributedTo`

```bash
python scripts/validate.py vocab.ttl
python scripts/validate.py vocab.ttl --verbose
python scripts/validate.py vocab.ttl --cta
python scripts/validate.py vocab.ttl --cta --verbose
python scripts/validate.py vocab.rdf --format xml
```

Exit code `0` on success, `1` if errors are found (suitable for CI pipelines).

---

### 3. Generate a SKOS vocabulary template

Four templates are available:

| Template | Use case |
|---|---|
| `basic` (default) | Generic concept hierarchy with optional SKOS-XL labels |
| `dwc-vocab` | Darwin Core controlled vocabulary (basisOfRecord, occurrenceStatus, etc.) |
| `dwc-names` | Taxonomic name vocabulary using the TDWG TAG NameThing pattern (SKOS-XL) |
| `etno-tk` | Traditional Knowledge vocabulary with CARE/PROV-O metadata (SKOS-XL) |

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

**Traditional Knowledge vocabulary** (CTA / EtnoTermos pattern, CARE + Nagoya, SKOS-XL):

```bash
python scripts/generate.py etnotermos --template etno-tk
python scripts/generate.py etnotermos --template etno-tk --lang pt --dir ./output
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

## Traditional Knowledge (CTA) Vocabularies

### Overview

Traditional Knowledge Associated with Biodiversity (CTA — Conhecimento Tradicional
Associado à Biodiversidade) requires a vocabulary architecture that is:

- **Polyglot** — multiple indigenous languages, each with individual metadata
- **Governed** — per-label access control (`public` / `restricted` / `community-only` / `sacred`)
- **Attributed** — provenance traceable to the originating people (CARE principles)
- **Compliant** — aligned with the Nagoya Protocol on Access and Benefit-Sharing

SKOS-XL is the correct choice because access restrictions live at the *label* level,
not at the concept level. The scientific name of a plant may be public while the sacred
ritual name is restricted — granularity impossible with `skos:prefLabel` literals.

### CARE Principles

| Principle | Property | Description |
|---|---|---|
| Collective | `prov:wasAttributedTo`, `etno:sourcePeople` | Attribute knowledge to originating people |
| Authority | `dct:rightsHolder`, `etno:accessLevel`, `etno:validatedBy` | Community controls its own data |
| Responsibility | `dct:source`, `etno:nagoyaStatus`, `prov:hadPrimarySource` | Traceable provenance |
| Ethics | `etno:languageStatus`, `etno:consentType`, `dct:license` | Do no harm; respect restrictions |

### Access levels (`etno:accessLevel`)

| Value | Meaning |
|---|---|
| `public` | Available to anyone |
| `restricted` | Researchers only, requires FPIC under Nagoya |
| `community-only` | Members of the originating community only |
| `sacred` | Sacred knowledge; never publish without explicit consent |

### Generate the template

```bash
python scripts/generate.py etnotermos --template etno-tk --lang pt
```

This creates a Turtle file with:
- `skos:ConceptScheme` with `dct:rightsHolder` and `dct:license` (TK Label)
- Ethnotaxonomic top-level categories (not western-science categories)
- **Jatobá** (*Hymenaea courbaril*) concept with labels in Portuguese, Guarani Mbya (`@gnm`), and Latin — each with full CARE metadata
- **Ayahuasca** concept with a `sacred` label in Huni Kuĩ (`@hux`) alongside a public Spanish label — demonstrating per-label access control
- `prov:Agent` resources for each indigenous people
- Darwin Core `dwc:vernacularName` bridge on each Concept

### Validate CTA compliance

```bash
python scripts/validate.py etnotermos.ttl --cta --verbose
```

### Explain CTA properties

```bash
python scripts/explain.py --cta
python scripts/explain.py --cta --term accessLevel
python scripts/explain.py --cta --term sourcePeople
python scripts/explain.py --cta --term nagoyaStatus
python scripts/explain.py --cta --list
```

### Key references

- [CARE Principles for Indigenous Data Governance](https://www.gida-global.org/care)
- [Nagoya Protocol — CBD](https://www.cbd.int/abs/)
- [Local Contexts TK Labels](https://localcontexts.org/labels/traditional-knowledge-labels/)
- [ISO 639-3 (indigenous language codes)](https://iso639-3.sil.org/)
- [VocBench 3 — SKOS-XL editor used by FAO/Agrovoc](https://vocbench.uniroma2.it/)
- [EtnoTermos — JBRJ](https://etnotermos.jbrj.gov.br/)

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
- [Traditional Knowledge properties](references/traditional_knowledge_properties.csv) — CTA/CARE metadata properties

---

## Related Skills

**[darwin-core](../darwin-core/)** — Use alongside this skill to package and validate occurrence data. Darwin Core defines the fields; SKOS defines the controlled vocabularies for the values. The `dwc-vocab` template generates SKOS representations of any Darwin Core controlled term.
