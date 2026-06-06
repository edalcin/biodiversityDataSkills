---
name: darwin-core
description: >
  Helps users work with Darwin Core and Darwin Core Archive (DwC-A),
  the biodiversity data standards. Validates DwC-A files, generates
  templates, maps CSV columns to DwC terms, and explains the standard.
  Use when the user mentions "Darwin Core", "DwC", "DwC-A", "GBIF",
  "biodiversity data", "occurrence", "taxon", or "biodiversity".
license: MIT
compatibility: Python 3.9+
metadata:
  author: biodiversityDataSkills
  repository: https://github.com/<your-username>/biodiversityDataSkills
---

# Darwin Core Skill

Skill for working with [Darwin Core](https://dwc.tdwg.org/) and [Darwin Core Archive](https://rs.gbif.org/core/) (DwC-A) data, the biodiversity data standards maintained by [TDWG](https://www.tdwg.org/).

## Setup

### 1. Install Python 3.9+

Make sure Python 3.9 or later is installed:

```bash
python --version
```

### 2. Install dependencies

```bash
cd /path/to/darwin-core
pip install -r requirements.txt
```

### 3. (Optional) Sync references

To download the latest Darwin Core term definitions:

```bash
python scripts/sync.py
```

---

## Usage

### 1. Explain the Darwin Core standard

General overview:

```bash
python scripts/explain.py
```

Explain a specific term:

```bash
python scripts/explain.py --term occurrenceID
python scripts/explain.py --term decimalLatitude
```

List all available terms:

```bash
python scripts/explain.py --list
```

### 2. Validate a Darwin Core Archive

Validates a DwC-A (.zip) checking structure, terms, and data:

```bash
python scripts/validate.py occurrences.zip
```

Detailed validation:

```bash
python scripts/validate.py occurrences.zip --verbose
```

### 3. Generate a DwC-A template

Creates a basic Darwin Core Archive structure:

```bash
python scripts/generate_template.py my_project --dir ./output
```

Generate with Event core (default: Occurrence):

```bash
python scripts/generate_template.py my_project --core event --dir ./output
```

Generate with Taxon core:

```bash
python scripts/generate_template.py my_project --core taxon --dir ./output
```

### 4. Map CSV columns to DwC terms

Analyzes a CSV and suggests mappings to Darwin Core terms:

```bash
python scripts/map_columns.py data.csv
```

Generate a new CSV with DwC headers:

```bash
python scripts/map_columns.py data.csv --output mapped.csv
```

Interactive mode (confirm each suggestion):

```bash
python scripts/map_columns.py data.csv --interactive
```

### 5. Sync references

Updates term definitions and extensions from official sources:

```bash
python scripts/sync.py
```

---

## References

- [Complete Darwin Core term list](references/all_dwc_vertical.csv) — 216 terms
- [Detailed term metadata](references/term_versions.csv) — 457 unique terms with full definitions
- [DwC Extensions guide](references/EXTENSIONS.md) — All GBIF-registered extensions
- [Darwin Core Text Guide](references/TEXT_GUIDE.md) — Official DwC-A spec (meta.xml format)

## Known Darwin Core Extensions

This skill knows about all GBIF-registered extensions ([https://rs.gbif.org/extensions.html](https://rs.gbif.org/extensions.html)), including:

| Extension | RowType | Core |
|---|---|---|
| Audiovisual Media | `ac/terms/Multimedia` | Occurrence, Taxon |
| Types and Specimen | `gbif/1.0/TypesAndSpecimen` | Taxon |
| DNA derived data | `gbif/1.0/DNADerivedData` | Occurrence, Event |
| Species Distribution | `gbif/1.0/Distribution` | Taxon |
| Species Profile | `gbif/1.0/SpeciesProfile` | Taxon |
| MeasurementOrFacts | `dwc/terms/MeasurementOrFact` | Occurrence, Event, Taxon |
| Identification History | `dwc/terms/Identification` | Occurrence |
| Resource Relationship | `dwc/terms/ResourceRelationship` | Occurrence, Event, Taxon |
| ChronometricAge | `chrono/terms/ChronometricAge` | Occurrence |
| Humboldt Ecological Inventory | `eco/terms/Event` | Event |
| ExtendedMeasurementOrFact | `obis/terms/ExtendedMeasurementOrFact` | Event |
| GGBN Permits / Loans | `ggbn/terms/...` | MaterialSample |
| Germplasm | `germplasm/germplasmTerm#...` | Occurrence |
| Vernacular Names | `gbif/1.0/VernacularName` | Taxon |
| Literature References | `gbif/1.0/Reference` | Taxon, Occurrence |
| Taxon Description | `gbif/1.0/Description` | Taxon |

See [references/EXTENSIONS.md](references/EXTENSIONS.md) for full details.

---

## Related Skills

**[skos-xl](../skos-xl/)** — Use alongside this skill to define the controlled vocabularies for Darwin Core term values (e.g. `basisOfRecord`, `occurrenceStatus`, `habitat`) as SKOS RDF. Also supports the TDWG TAG NameThing pattern for representing taxonomic names with full nomenclatural provenance.
