
# biodiversityDataSkills

A collection of AI skills for biodiversity data, designed for the [pi](https://pi.dev) / [skills.sh](https://www.skills.sh/) ecosystem.

## Skills

| Skill | Description |
|---|---|
| [darwin-core](./darwin-core/) | Work with Darwin Core and Darwin Core Archive (DwC-A) |
| [skos-xl](./skos-xl/) | Build and validate SKOS / SKOS-XL controlled vocabularies, with Darwin Core integration |

---

## skos-xl

This skill helps researchers, data managers, and biodiversity informaticians build and maintain [SKOS](https://www.w3.org/TR/skos-reference/) (Simple Knowledge Organization System) and [SKOS-XL](https://www.w3.org/TR/skos-reference/skos-xl.html) controlled vocabularies as Linked Data (RDF). It is particularly focused on Darwin Core vocabulary integration, following the [TDWG TAG SKOS-XL patterns](https://github.com/tdwg/tag/tree/master/skos-xl).

### What is SKOS?

SKOS is a W3C standard for representing thesauri, classification schemes, subject heading lists, and taxonomies in RDF. A **SKOS vocabulary** is an RDF file that contains:
- `skos:ConceptScheme` — the vocabulary container
- `skos:Concept` instances — individual controlled terms
- `skos:broader` / `skos:narrower` — hierarchical relationships
- `skos:prefLabel` / `skos:altLabel` — labels with language tags
- `skos:exactMatch` / `skos:closeMatch` — cross-vocabulary alignment links

**SKOS-XL** extends SKOS by making labels first-class RDF resources (`skosxl:Label`), enabling provenance, metadata, and relationships to be attached to individual labels — not just to concepts. The TDWG TAG uses this to model taxonomic names with parsed components (genus, epithet, authorship, basionym links).

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

```bash
python skos-xl/scripts/generate.py my_vocab
python skos-xl/scripts/generate.py basisOfRecord --template dwc-vocab
python skos-xl/scripts/generate.py bryophytes --template dwc-names
python skos-xl/scripts/generate.py my_vocab --xl --format jsonld --lang pt
```

---

#### 4. `validate.py` — Validate a SKOS file

Validates Turtle, RDF/XML, JSON-LD, N-Triples, or N3 files against 8 checks:
- Parse integrity, ConceptScheme presence, `inScheme` links
- `prefLabel` presence, duplicate prefLabel detection (S14)
- Disjointness constraints, S27 relation integrity
- SKOS-XL `literalForm` cardinality

```bash
python skos-xl/scripts/validate.py vocab.ttl
python skos-xl/scripts/validate.py vocab.ttl --verbose
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

## darwin-core

This skill helps researchers, data managers, and biodiversity informaticians work with [Darwin Core](https://dwc.tdwg.org/) (DwC) — the international standard for sharing biological occurrence data — and the [Darwin Core Archive](https://rs.gbif.org/core/) (DwC-A) packaging format used by platforms like [GBIF](https://www.gbif.org/) and [iDigBio](https://www.idigbio.org/).

### What is Darwin Core?

Darwin Core is a vocabulary standard maintained by [TDWG](https://www.tdwg.org/) (Biodiversity Information Standards). It defines a fixed set of terms (fields) for describing biological observations, specimens, and taxa, making data interoperable across institutions worldwide.

A **Darwin Core Archive** (DwC-A) is a ZIP file containing:
- `meta.xml` — machine-readable descriptor of the archive structure (which files exist, which terms each column maps to, and how files relate to each other)
- One or more CSV data files (occurrences, events, taxa, or extension data)

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
| `references/TEXT_GUIDE.md` | Official Darwin Core Text Guide specification |

---

## License

MIT
