
# biodiversityDataSkills

A collection of AI skills for biodiversity data, designed for the [skills.sh](https://www.skills.sh/) ecosystem. Each skill provides scripts, reference data, and documentation to help researchers, data managers, and biodiversity informaticians work with standards-compliant data.

## Installation

Each skill installs independently via the [skills.sh](https://www.skills.sh/) CLI — no need to clone this repo:

```bash
npx skills add https://github.com/edalcin/biodiversityDataSkills --skill darwin-core
npx skills add https://github.com/edalcin/biodiversityDataSkills --skill skos-xl
npx skills add https://github.com/edalcin/biodiversityDataSkills --skill biohousekeeper
```

Or install every skill in the repo at once:

```bash
npx skills add https://github.com/edalcin/biodiversityDataSkills
```

Each skill has its own Python dependencies — see that skill's **Setup** section below for the `pip install` command to run after installing.

## Skills

| Skill | Description | Key dependency |
|---|---|---|
| [darwin-core](./darwin-core/) | Work with Darwin Core (DwC), Darwin Core Archive (DwC-A), **Darwin Core Conceptual Model (DwC-CM)**, and **Darwin Core Data Package (DwC-DP)** | `pandas`, `python-dwca-reader` |
| [skos-xl](./skos-xl/) | Build and validate SKOS / SKOS-XL controlled vocabularies — generic, Darwin Core, and Traditional Knowledge (CTA/CARE/Nagoya) | `rdflib` |
| [biohousekeeper](./biohousekeeper/) | Analyze a biodiversity spreadsheet (CSV/XLSX) and propose a Darwin Core-aligned column structure, asking the user about ambiguous splits/merges before restructuring | `pandas`, `openpyxl` |

## Skills Interoperability

The two skills complement each other. Darwin Core defines **what fields** a biodiversity dataset uses; SKOS defines the **controlled vocabularies** (the valid values) for those fields as Linked Data.

| Use case | Skills |
|---|---|
| Publish occurrence data with standardized term values | darwin-core + skos-xl |
| Define a controlled vocabulary for `basisOfRecord` as RDF | skos-xl (`dwc-vocab` template) |
| Represent taxonomic names with nomenclatural provenance | skos-xl (`dwc-names` template) |
| Build a Traditional Knowledge vocabulary (CTA/EtnoTermos) | skos-xl (`etno-tk` template) |
| Map a legacy CSV to Darwin Core terms | darwin-core (`map_columns.py`) |
| Validate a DwC-A archive | darwin-core (`validate.py`) |
| Align an institutional vocabulary to GBIF/TDWG terms | skos-xl (`skos:exactMatch`) |
| Understand DwC class relationships (Event, Occurrence, Survey…) | darwin-core (DwC-CM reference) |
| Create a relational DwC-DP data package (replaces DwC-A star schema) | darwin-core (DwC-DP guide) |
| Restructure a legacy spreadsheet's columns to match Darwin Core, with composite-field splitting | biohousekeeper (`analyze.py` + `apply.py`) |

---

## skos-xl

This skill helps researchers, data managers, and biodiversity informaticians build and maintain [SKOS](https://www.w3.org/TR/skos-reference/) (Simple Knowledge Organization System) and [SKOS-XL](https://www.w3.org/TR/skos-reference/skos-xl.html) controlled vocabularies as Linked Data (RDF). It covers three domains:

1. **Generic vocabularies** — thesauri, classification schemes, concept hierarchies
2. **Darwin Core integration** — controlled vocabularies for DwC terms; taxonomic name vocabularies using the [TDWG TAG SKOS-XL patterns](https://github.com/tdwg/tag/tree/master/skos-xl)
3. **Traditional Knowledge (CTA)** — vocabularies for *Conhecimento Tradicional Associado à Biodiversidade*, with per-label access control, multilingual indigenous labels, [CARE principles](https://www.gida-global.org/care), and [Nagoya Protocol](https://www.cbd.int/abs/) compliance metadata

### What is SKOS?

SKOS is a W3C standard for representing thesauri, classification schemes, subject heading lists, and taxonomies in RDF. A **SKOS vocabulary** is an RDF file that contains:
- `skos:ConceptScheme` — the vocabulary container
- `skos:Concept` instances — individual controlled terms
- `skos:broader` / `skos:narrower` — hierarchical relationships
- `skos:prefLabel` / `skos:altLabel` — labels with language tags
- `skos:exactMatch` / `skos:closeMatch` — cross-vocabulary alignment links

**SKOS-XL** extends SKOS by making labels first-class RDF resources (`skosxl:Label`), enabling provenance, metadata, and relationships to be attached to individual labels — not just to concepts. This is essential for Traditional Knowledge vocabularies: the scientific name of a species may be public while the sacred ritual name in an indigenous language is restricted — granularity that is impossible with `skos:prefLabel` literals.

### Setup

Requires Python 3.9+ and `rdflib`:

```bash
pip install -r skos-xl/requirements.txt
```

### Scripts

```
sync.py → explain.py → generate.py → validate.py → convert.py
```

---

#### 1. `sync.py` — Download reference schemas

Downloads the official W3C SKOS/SKOS-XL RDF/OWL schemas and TDWG TAG Turtle examples.

```bash
python skos-xl/scripts/sync.py
```

---

#### 2. `explain.py` — Explore the standard

Reference guide for SKOS and SKOS-XL terms with definitions and usage notes.

```bash
python skos-xl/scripts/explain.py                  # SKOS overview
python skos-xl/scripts/explain.py --term broader   # Explain a specific term
python skos-xl/scripts/explain.py --list           # List all SKOS terms
python skos-xl/scripts/explain.py --xl             # SKOS-XL overview
python skos-xl/scripts/explain.py --xl --term Label
```

---

#### 3. `generate.py` — Generate a vocabulary template

Three templates cover the most common biodiversity use cases:

| Template | Use case |
|---|---|
| `basic` (default) | Generic SKOS vocabulary with hierarchy |
| `dwc-vocab` | DwC controlled vocabulary (basisOfRecord, sex, habitat, …) |
| `dwc-names` | Taxonomic name vocabulary (TDWG TAG NameThing, SKOS-XL) |
| `etno-tk` | Traditional Knowledge (CTA/EtnoTermos) with CARE + Nagoya metadata |

```bash
python skos-xl/scripts/generate.py my_vocab
python skos-xl/scripts/generate.py basisOfRecord --template dwc-vocab
python skos-xl/scripts/generate.py bryophytes --template dwc-names
python skos-xl/scripts/generate.py etnotermos --template etno-tk --lang pt
python skos-xl/scripts/generate.py my_vocab --xl --format jsonld --lang pt
```

---

#### 4. `validate.py` — Validate a SKOS file

Validates Turtle, RDF/XML, JSON-LD, N-Triples, or N3 files. Standard (8 checks) + optional CTA checks (`--cta`):
- Parse integrity, ConceptScheme presence, `inScheme` links
- `prefLabel` presence, duplicate prefLabel detection (S14)
- Disjointness constraints, S27 relation integrity
- SKOS-XL `literalForm` cardinality
- CTA: `dct:rightsHolder`, `dct:license`, `etno:accessLevel`, attribution, sacred-label validation

```bash
python skos-xl/scripts/validate.py vocab.ttl
python skos-xl/scripts/validate.py vocab.ttl --verbose
python skos-xl/scripts/validate.py etnotermos.ttl --cta --verbose
```

---

#### 5. `convert.py` — Convert format or label style

```bash
python skos-xl/scripts/convert.py vocab.rdf --to-format turtle
python skos-xl/scripts/convert.py vocab.ttl --to-xl            # plain → SKOS-XL
python skos-xl/scripts/convert.py vocab_xl.ttl --from-xl       # SKOS-XL → plain
python skos-xl/scripts/convert.py vocab.ttl --to-xl --to-format jsonld
```

---

### Traditional Knowledge (CTA)

**CTA** (*Conhecimento Tradicional Associado à Biodiversidade*) vocabularies encode indigenous knowledge about plants, animals, and ecosystems together with the governance metadata that ethical use requires.

**Why SKOS-XL?** Access restrictions exist at the *label* level, not the concept level. The scientific name of a plant can be public while the sacred ritual name in an indigenous language is restricted — granularity that is impossible with plain `skos:prefLabel` literals. SKOS-XL makes each label a first-class RDF resource that can carry provenance, community attribution, and access control independently.

#### Access levels (`etno:accessLevel`)

| Value | Meaning |
|---|---|
| `public` | Available to anyone |
| `restricted` | Researchers only; requires FPIC under Nagoya Protocol |
| `community-only` | Members of the originating community only |
| `sacred` | Never publish without explicit community consent |

#### CARE Principles

| Principle | Key properties |
|---|---|
| **C**ollective | `prov:wasAttributedTo`, `etno:sourcePeople` — attribute knowledge to originating people |
| **A**uthority | `dct:rightsHolder`, `etno:accessLevel`, `etno:validatedBy` — community controls its own data |
| **R**esponsibility | `dct:source`, `etno:nagoyaStatus`, `prov:hadPrimarySource` — traceable provenance |
| **E**thics | `etno:consentType`, `etno:languageStatus`, `dct:license` — respect restrictions; do no harm |

#### Workflow

**1. Generate a CTA vocabulary template:**

```bash
python skos-xl/scripts/generate.py etnotermos --template etno-tk --lang pt
```

Creates a Turtle file with:
- `skos:ConceptScheme` with `dct:rightsHolder` and `dct:license` (TK Label)
- Labels in Portuguese, Guarani Mbya (`@gnm`), and Latin for a plant concept
- A `sacred` label in Huni Kuĩ (`@hux`) with `etno:accessLevel sacred` alongside a public Spanish label — demonstrating per-label access control
- `prov:Agent` resources for each indigenous people
- `dwc:vernacularName` bridge for Darwin Core interoperability

**2. Explore CTA properties:**

```bash
python skos-xl/scripts/explain.py --cta                       # overview: CARE, Nagoya, access levels
python skos-xl/scripts/explain.py --cta --list                # all 17 CTA properties
python skos-xl/scripts/explain.py --cta --term accessLevel    # specific property
python skos-xl/scripts/explain.py --cta --term nagoyaStatus
```

**3. Validate CARE / Nagoya compliance:**

```bash
python skos-xl/scripts/validate.py etnotermos.ttl --cta --verbose
```

Runs 5 CTA checks on top of the 8 standard SKOS checks:
- `dct:rightsHolder` present on `ConceptScheme` (CARE Authority)
- `dct:license` present (TK Label recommended)
- `etno:accessLevel` on every `skosxl:Label`
- Attribution (`prov:wasAttributedTo` or `etno:sourcePeople`) for labels in indigenous languages
- Validation record (`etno:validatedBy`) for `restricted`, `community-only`, and `sacred` labels

#### Key references

- [CARE Principles for Indigenous Data Governance](https://www.gida-global.org/care)
- [Nagoya Protocol — CBD](https://www.cbd.int/abs/)
- [Local Contexts TK Labels](https://localcontexts.org/labels/traditional-knowledge-labels/)
- [EtnoTermos — JBRJ](https://etnotermos.jbrj.gov.br/)
- [ISO 639-3 (indigenous language codes)](https://iso639-3.sil.org/)

---

## darwin-core

> **Updated 2026-05-26:** The TDWG Executive Committee ratified two new normative additions to Darwin Core: the **Conceptual Model (DwC-CM)** and the **Data Package Guide (DwC-DP)**. This skill now covers all three formats: DwC-A (existing archives), DwC-CM (class relationship semantics), and DwC-DP (next-generation relational packages).

This skill helps researchers, data managers, and biodiversity informaticians work with [Darwin Core](https://dwc.tdwg.org/) (DwC) — the international standard for sharing biological occurrence data — and its packaging formats:

- **Darwin Core Archive (DwC-A)** — ZIP file with `meta.xml` + CSVs; star-schema; used by GBIF, iDigBio, and IPT today
- **Darwin Core Data Package (DwC-DP)** — gzip with `datapackage.json` + CSVs; arbitrary FK relationships; ratified 2026-05-26; GBIF adoption in progress
- **Darwin Core Conceptual Model (DwC-CM)** — semantics of relationships between DwC classes; technology-agnostic reference; ratified 2026-05-26

### Setup

Requires Python 3.9+:

```bash
pip install -r darwin-core/requirements.txt
```

### Scripts

The skill provides five Python scripts. The recommended workflow runs them in this order:

```
sync.py → explain.py → map_columns.py → generate_template.py → validate.py
```

---

#### 1. `sync.py` — Update reference data

Downloads the latest Darwin Core term definitions from the official [TDWG GitHub repository](https://github.com/tdwg/dwc). This is optional but recommended before first use, since the bundled references may become outdated as the standard evolves.

What it downloads:
- `all_dwc_vertical.csv` — the flat list of all 216+ current DwC terms
- `term_versions.csv` — full version history with definitions, comments, and examples for each term
- `TEXT_GUIDE.md` — the official Darwin Core Text Guide (the spec that defines the DwC-A format)

```bash
python darwin-core/scripts/sync.py
```

---

#### 2. `explain.py` — Explore the standard

Provides a human-readable reference for the Darwin Core standard and its individual terms. Useful for understanding what a term means before mapping data to it.

**Show a general overview** of the standard, its core types, and key terms:

```bash
python darwin-core/scripts/explain.py
```

**Explain a specific term** — shows the IRI (unique identifier), full definition, usage comments, and examples:

```bash
python darwin-core/scripts/explain.py --term occurrenceID
python darwin-core/scripts/explain.py --term decimalLatitude
python darwin-core/scripts/explain.py --term basisOfRecord
```

**List all available terms** in a compact columnar display:

```bash
python darwin-core/scripts/explain.py --list
```

The script reads from `term_versions.csv` (the detailed reference). If that file is missing, run `sync.py` first.

---

#### 3. `map_columns.py` — Map existing CSV data to DwC terms

Analyzes an existing CSV file and suggests how to rename each column to the correct Darwin Core term. This is the typical entry point when you have legacy data (field notebooks, collection databases, spreadsheets) that you want to publish in DwC format.

The script uses a multilingual synonym dictionary covering common column names in English, Portuguese, and Spanish (e.g., `lat` → `decimalLatitude`, `coletor` → `recordedBy`, `especie` → `scientificName`). It also performs partial-match fallback against all 216 DwC terms.

**Suggest mappings** (display only, no file written):

```bash
python darwin-core/scripts/map_columns.py data.csv
```

**Write a new CSV** with Darwin Core column headers and the original data:

```bash
python darwin-core/scripts/map_columns.py data.csv --output mapped.csv
```

**Interactive mode** — confirm or override each mapping one by one:

```bash
python darwin-core/scripts/map_columns.py data.csv --interactive
```

In interactive mode, for each column you can press Enter to accept the suggestion, `n` to skip it (keep the original name), or `m` to manually type any DwC term.

---

#### 4. `generate_template.py` — Generate a DwC-A template

Creates a ready-to-use Darwin Core Archive directory with a valid `meta.xml` and an example CSV pre-populated with all recommended fields for the chosen core type. Use this as a starting point when building a new dataset from scratch.

Three **core types** are supported:

| Core | Use case | Key fields |
|---|---|---|
| `occurrence` (default) | Specimen records, field observations | `occurrenceID`, `scientificName`, `decimalLatitude`, `eventDate`, … |
| `event` | Sampling campaigns, surveys | `eventID`, `parentEventID`, `samplingProtocol`, `habitat`, … |
| `taxon` | Checklists, taxonomic databases | `taxonID`, `scientificName`, `taxonRank`, `kingdom`, … |

**Generate an Occurrence core archive** in `./output/my_project/`:

```bash
python darwin-core/scripts/generate_template.py my_project --dir ./output
```

**Generate an Event core archive:**

```bash
python darwin-core/scripts/generate_template.py my_project --core event --dir ./output
```

**Generate a Taxon core archive:**

```bash
python darwin-core/scripts/generate_template.py my_project --core taxon --dir ./output
```

The output is a directory (not yet zipped) containing `meta.xml` and the CSV. Fill in the CSV with your data, then ZIP the folder and validate it with `validate.py`.

---

#### 5. `validate.py` — Validate a Darwin Core Archive

Validates a DwC-A `.zip` file against the standard. Runs five sequential checks and reports errors and warnings:

| Step | What is checked |
|---|---|
| 1 | File is a valid ZIP archive |
| 2 | `meta.xml` is present and can be parsed |
| 3 | `meta.xml` has valid structure (`<archive>`, `<core>`, `<files>`, `<field>` elements) |
| 4 | All files referenced in `meta.xml` actually exist inside the ZIP |
| 5 | All terms used in `meta.xml` are valid Darwin Core terms |

**Validate an archive:**

```bash
python darwin-core/scripts/validate.py occurrences.zip
```

**Verbose output** (show warnings in addition to errors):

```bash
python darwin-core/scripts/validate.py occurrences.zip --verbose
```

The script exits with code `0` on success and `1` if any errors are found, making it suitable for use in CI pipelines.

---

### DwC-A Extensions

Beyond the core file, a DwC-A can include extension files that link additional data rows to core records. This skill knows all GBIF-registered extensions:

| Extension | Use case |
|---|---|
| MeasurementOrFact | Measurements, traits, attributes |
| Multimedia | Images, audio, video |
| Identification History | Past identifications of a specimen |
| ResourceRelationship | Host–parasite, part–whole, etc. |
| DNADerivedData | eDNA, barcoding, metabarcoding |
| ChronometricAge | Radiocarbon and other age data |
| Vernacular Names | Common names per language |
| Species Distribution | Range polygons for checklists |
| ExtendedMeasurementOrFact | OBIS/EMODnet event-based measurements |

See [`darwin-core/references/EXTENSIONS.md`](darwin-core/references/EXTENSIONS.md) for the full list with row types and compatible cores.

---

### Reference files

| File | Content |
|---|---|
| `references/all_dwc_vertical.csv` | Flat list of 216 current DwC terms |
| `references/term_versions.csv` | 457 term versions with full definitions, comments, and examples |
| `references/EXTENSIONS.md` | All GBIF-registered DwC-A extensions |
| `references/TEXT_GUIDE.md` | Official Darwin Core Text Guide (DwC-A `meta.xml` spec) |
| `references/CONCEPTUAL_MODEL.md` | **DwC-CM** — classes, relationships, eDNA/molecular, Agent, Media (ratified 2026-05-26) |
| `references/DATA_PACKAGE_GUIDE.md` | **DwC-DP** — descriptor, table schemas, FK graph, field descriptors (ratified 2026-05-26) |

---

## biohousekeeper

This skill helps researchers and data managers turn a legacy biodiversity spreadsheet (field notebook exports, museum collection databases, survey data) into a Darwin Core-aligned structure. Unlike `darwin-core`'s `map_columns.py` — which only renames CSV headers — `biohousekeeper` also reads sample cell values to detect **composite columns that need splitting** (packed coordinates, binomial scientific names, delimited locality hierarchies), **redundant duplicate columns**, and **missing recommended fields**, asking the user about anything ambiguous before proposing a final structure.

### Setup

Requires Python 3.9+:

```bash
pip install -r biohousekeeper/requirements.txt
```

### Scripts

```
analyze.py → (resolve open questions) → apply.py
```

---

#### 1. `analyze.py` — Analyze a spreadsheet and propose a structure

Reads a `.csv` or `.xlsx` file, inspects column names and sample values, and writes a Markdown report plus a JSON plan — the original file is never modified.

```bash
python biohousekeeper/scripts/analyze.py my_spreadsheet.xlsx
python biohousekeeper/scripts/analyze.py my_spreadsheet.xlsx --sheet "Occurrences"
python biohousekeeper/scripts/analyze.py data.csv --out-dir ./report
```

What it detects:

| Finding | Example | Confidence |
|---|---|---|
| Column name/synonym maps to a DwC term (EN/PT/ES) | `coletor` → `recordedBy` | high — auto-applies |
| Packed coordinate pair | `"-23.55,-46.63"` → `decimalLatitude` + `decimalLongitude` | high — auto-applies |
| Binomial scientific name | `"Panthera onca"` → `genus` + `specificEpithet` (derived; `scientificName` kept) | medium — asks first |
| Delimited locality hierarchy | `"Brazil/SP/Campinas"` → `country`/`stateProvince`/`municipality` | low — asks which term per part |
| Separate year/month/day columns | merged into ISO 8601 `eventDate` | high — auto-applies |
| Duplicate columns (≥95% matching values) | `coletor` and `observador` holding the same names | medium — asks which to drop |
| Missing recommended field | no column maps to `occurrenceID`, `basisOfRecord`, etc. | advisory note |

---

#### 2. `apply.py` — Write the corrected spreadsheet

After reviewing the report and resolving its open questions (by editing the plan JSON's `apply`/`targets` fields), generate the corrected file:

```bash
python biohousekeeper/scripts/apply.py my_spreadsheet.xlsx --plan my_spreadsheet_biohousekeeper_report.json --output my_spreadsheet_corrected.xlsx
```

`--output` must be a different path from the input — the original spreadsheet is always preserved.

### Scope

`biohousekeeper` handles column-level renaming and single-column split/merge/drop operations on one sheet. It does not perform full DwC-DP multi-table normalization (splitting a flat sheet into separate event/occurrence/taxon tables) — use `darwin-core`'s DwC-DP guide for that once the column-level cleanup is done.

---

## License

MIT
