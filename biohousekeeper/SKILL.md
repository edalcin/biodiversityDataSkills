---
name: biohousekeeper
description: >
  Analyzes biodiversity spreadsheets (CSV/XLSX) and proposes a restructured
  column layout aligned with Darwin Core (DwC), asking the user clarifying
  questions about anything ambiguous before finalizing the report. Detects
  columns that should be renamed to DwC terms, composite columns that should
  be split (e.g. packed "lat,long" pairs, "Genus species" binomials,
  delimited locality hierarchies), redundant duplicate columns, and missing
  recommended fields (occurrenceID, basisOfRecord, eventDate, coordinates).
  Use when the user mentions "biohousekeeper", "clean up my spreadsheet",
  "restructure my biodiversity data", "map my spreadsheet to Darwin Core",
  or asks to analyze/tidy/fix columns in an occurrence/species/collection
  spreadsheet.
license: MIT
compatibility: Python 3.9+
metadata:
  author: biodiversityDataSkills
  repository: https://github.com/edalcin/biodiversityDataSkills
---

# BioHousekeeper Skill

Turns a messy biodiversity spreadsheet into a Darwin Core-aligned structure through analysis plus a short, targeted conversation - never a silent bulk rewrite.

## Setup

```bash
cd /path/to/biohousekeeper
pip install -r requirements.txt
```

## Usage

### `/biohousekeeper analyze <spreadsheet>`

```bash
python scripts/analyze.py my_spreadsheet.xlsx
python scripts/analyze.py my_spreadsheet.xlsx --sheet "Occurrences"
python scripts/analyze.py data.csv --out-dir ./report
```

Reads the file (first sheet by default for `.xlsx`; other sheets are listed but not analyzed - pass `--sheet` to pick one), inspects both column names and sample cell values, and writes two files next to `--out-dir` (default: current directory):

- `<name>_biohousekeeper_report.md` - human-readable report: column mapping table, proposed transformations, missing recommended fields, open questions
- `<name>_biohousekeeper_report.json` - the same findings as a plan, with an `apply`/`auto_apply` flag per suggestion, consumed by `apply.py`

The original spreadsheet is never modified by either script.

### What you (the agent) do after running `analyze.py`

1. Read the generated Markdown report and present the column mapping table and proposed transformations to the user.
2. Walk through the `questions` array in the JSON one at a time (not all at once) - these are the cases the heuristics could not resolve alone:
   - a "coordinates split" needs no question (deterministic, `auto_apply: true`)
   - a binomial `scientificName` split into `genus`/`specificEpithet` always asks for confirmation - regex-based epithet extraction can be wrong on cultivars, hybrids, or "sp." records
   - a delimited locality column asks the user to name each part left-to-right (e.g. `country,stateProvince,municipality`) - order is dataset-specific and cannot be inferred
   - a suspected duplicate column asks which one to drop
3. Record the user's answers by editing the plan JSON directly:
   - set `"apply": true` (or `false`) on the relevant column entry or operation
   - for `split_locality`, fill in `"targets"` with the DwC term list the user gave you, in order (use `"skip"` for a part that maps to nothing)
4. Ask whether the user wants a corrected file. If yes, run `apply.py`; if no, the report alone stands as the deliverable.

### `apply.py` - write the corrected spreadsheet

```bash
python scripts/apply.py my_spreadsheet.xlsx --plan my_spreadsheet_biohousekeeper_report.json --output my_spreadsheet_corrected.xlsx
```

Executes, in order: date-parts merges, coordinate splits, taxon epithet derivation, locality splits, redundant-column drops, then column header renames. Only operations/columns with `apply: true` (or their heuristic `auto_apply: true` default, if untouched) run. `--output` must differ from the input path - the original file is always preserved.

## Detection heuristics (what `analyze.py` looks for)

| Finding | Signal | Confidence |
|---|---|---|
| Column already named or synonym of a DwC term | Name match against `references/dwc_terms.csv` + a EN/PT/ES synonym dictionary | high -> auto-applies |
| Partial name match only | Substring match against DwC term list | low -> asks for confirmation |
| Packed coordinate pair (`"−23.5,−46.6"`) | Column name hints at coordinates + delimited values both numeric and in valid lat/lon range | high -> auto-applies, original kept as `verbatimCoordinates` |
| Binomial scientific name (`"Panthera onca"`) | Column maps to `scientificName` (or name hints at species) + values match a `Genus species` pattern | medium -> always asks |
| Delimited locality hierarchy (`"Brazil / SP / Campinas"`) | Column name hints at locality + a consistent delimiter splits most rows into 2-5 parts | low -> always asks which DwC term each part represents |
| Separate year/month/day columns | Three columns with valid year/month/day ranges | high -> auto-applies, merges into ISO 8601 `eventDate` |
| Redundant duplicate columns | Two columns match in ≥95% of overlapping non-null rows | medium -> always asks which to drop |
| Missing recommended field | `occurrenceID`, `basisOfRecord`, `scientificName`, `eventDate`, `decimalLatitude`/`decimalLongitude`, `recordedBy`, `country` absent from the mapped terms | advisory note only, not a blocking error |

Only column-level renaming and single-column split/merge/drop operations are in scope. BioHousekeeper does not attempt full DwC-DP multi-table normalization (splitting a flat sheet into separate event/occurrence/taxon tables) - use the [darwin-core](../darwin-core/) skill's DwC-DP guide for that.

## References

- [`references/dwc_terms.csv`](references/dwc_terms.csv) - flat list of 216 current Darwin Core terms, vendored from the [TDWG `dwc` repository](https://github.com/tdwg/dwc)

## Related Skills

**[darwin-core](../darwin-core/)** - once BioHousekeeper's report and corrected spreadsheet exist, use darwin-core to validate the result, generate a full DwC-A/DwC-DP package, or look up the precise definition of any DwC term the report suggested.
