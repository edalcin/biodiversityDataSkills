---
name: darwin-core
description: >
  Helps users work with Darwin Core (DwC), Darwin Core Archive (DwC-A),
  Darwin Core Conceptual Model (DwC-CM), and Darwin Core Data Package (DwC-DP),
  the biodiversity data standards maintained by TDWG. Validates DwC-A files,
  generates templates, maps CSV columns to DwC terms, explains the standard,
  explains class relationships via DwC-CM, and helps create DwC-DP packages.
  Use when the user mentions "Darwin Core", "DwC", "DwC-A", "DwC-DP", "DwC-CM",
  "GBIF", "biodiversity data", "occurrence", "taxon", "biodiversity",
  "conceptual model", "data package", "frictionless data", or "datapackage.json".
license: MIT
compatibility: Python 3.9+
metadata:
  author: biodiversityDataSkills
  repository: https://github.com/<your-username>/biodiversityDataSkills
---

# Darwin Core Skill

Skill for working with [Darwin Core](https://dwc.tdwg.org/) and its related standards maintained by [TDWG](https://www.tdwg.org/):
- **DwC-A** — Darwin Core Archive (star-schema ZIP format; existing tooling)
- **DwC-CM** — Darwin Core Conceptual Model (ratified 2026-05-26; semantics of class relationships)
- **DwC-DP** — Darwin Core Data Package (ratified 2026-05-26; relational tabular format extending Frictionless Data)

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
- [Darwin Core Conceptual Model](references/CONCEPTUAL_MODEL.md) — DwC-CM classes and relationships (ratified 2026-05-26)
- [Darwin Core Data Package Guide](references/DATA_PACKAGE_GUIDE.md) — DwC-DP spec, descriptor format, table schemas (ratified 2026-05-26)

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

## Darwin Core Conceptual Model (DwC-CM)

Ratified 2026-05-26. Provides semantics of relationships between DwC classes — the missing piece since Darwin Core's inception. Technology-agnostic (relational DB, document DB, graph DB all valid).

**Full reference:** [references/CONCEPTUAL_MODEL.md](references/CONCEPTUAL_MODEL.md)

### DwC-CM Classes (quick reference)

| Class | Role |
|---|---|
| Event | Action/process at a place+time; 4 specializations below |
| Occurrence | Event establishing state of an Organism at place+time |
| Survey | Event supporting presence/absence/abundance inferences |
| OrganismInteraction | Event expressing non-permanent interaction between 2 Organisms |
| Organism | Particular organism or taxonomically homogeneous group |
| OrganismRelationship | Permanent Organism-to-Organism relationships |
| SurveyTarget | What a Survey was seeking |
| MaterialEntity | Physical matter; gathered or sampled during an Event |
| Identification | Taxonomic (or other) determination by an Agent |
| Taxon | Taxonomically homogeneous group; occupies a rank in hierarchy |
| Location | Spatial region or named place |
| GeologicalContext | Stratigraphic assignment context |
| ChronometricAge | Age from a dating method (radiocarbon, etc.) |
| Agent | Person, org, group, device, software that can act |
| Protocol | Method used during an action |
| MediaEntity | Recorded entity (image, sound, video, text) |
| NucleotideAnalysis | Molecular analysis following a MolecularProtocol |
| NucleotideSequence | Sequence produced by NucleotideAnalysis |
| MolecularProtocol | Protocol for nucleotide analysis |

**Key design points:**
- Occurrence, Survey, OrganismInteraction are specializations of Event — not combinable in one Event
- Events nest (parent/child); one child has only one parent
- MaterialSample omitted from DwC-CM; use MaterialEntity (derived from another MaterialEntity)
- OrganismInteraction has `by` (actor) and `with` (target) links to Occurrence
- NucleotideAnalysis → Identification → inferred Occurrence (for eDNA/metabarcoding)

---

## Darwin Core Data Package (DwC-DP)

Ratified 2026-05-26. Extends [Frictionless Data Package spec](https://specs.frictionlessdata.io/) as the reference implementation of DwC-CM. Replaces DwC-A's star-schema constraint with arbitrary relational FK graphs.

**Full reference:** [references/DATA_PACKAGE_GUIDE.md](references/DATA_PACKAGE_GUIDE.md)

### File structure
```
datapackage.json   # Required descriptor
eml.xml            # Optional EML metadata
event.csv          # One or more DwC-DP table CSV files
occurrence.csv
...
```

### Descriptor (`datapackage.json`) required fields
```json
{
  "profile": "http://rs.tdwg.org/dwc-dp/1.0/dwc-dp-profile.json",
  "resources": [
    {
      "name": "event",
      "path": "event.csv",
      "profile": "tabular-data-resource",
      "mediatype": "text/csv",
      "schema": {
        "fields": [...],
        "primaryKey": ["eventID"],
        "foreignKeys": [
          {
            "fields": "parentEventID",
            "predicate": "happened during",
            "reference": { "resource": "", "fields": "eventID" }
          }
        ]
      }
    }
  ]
}
```

### Rules
- Table `name` MUST be a reserved name from the profile (`event`, `occurrence`, `agent`, etc.)
- Field descriptors MUST include `name`, `title`, `description`, `type`, `dcterms:isVersionOf`
- `foreignKeys.predicate` documents relationship semantics (e.g., `"happened during"`, `"conducted by"`)
- Self-referencing FK: `"resource": ""`
- Compression: gzip only (`.gz`); `datapackage.json` always at root, never individually compressed
- Copy field descriptors from `http://rs.tdwg.org/dwc-dp/1.0/table-schemas` for guaranteed compliance

### Key URLs
- Profile: `http://rs.tdwg.org/dwc-dp/1.0/dwc-dp-profile.json`
- Table schemas: `http://rs.tdwg.org/dwc-dp/1.0/table-schemas`
- Designer: https://gbif.github.io/dwc-dp/designer/
- QRG: https://gbif.github.io/dwc-dp/qrg/

### DwC-DP vs DwC-A

| | DwC-A | DwC-DP |
|---|---|---|
| Container | ZIP | gzip |
| Descriptor | meta.xml | datapackage.json |
| Schema | Star schema only | Arbitrary FK graph |
| Relationship labels | Implicit | Explicit `predicate` |
| Status | Operational | Ratified 2026-05-26; GBIF adoption in progress |

---

## Related Skills

**[skos-xl](../skos-xl/)** — Use alongside this skill to define the controlled vocabularies for Darwin Core term values (e.g. `basisOfRecord`, `occurrenceStatus`, `habitat`) as SKOS RDF. Also supports the TDWG TAG NameThing pattern for representing taxonomic names with full nomenclatural provenance.
