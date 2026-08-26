# Graph Report - biodiversityDataSkills  (2026-07-01)

## Corpus Check
- 29 files · ~26,612 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 217 nodes · 276 edges · 20 communities (18 shown, 2 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b3d487b1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]

## God Nodes (most connected - your core abstractions)
1. `biodiversityDataSkills` - 10 edges
2. `detect_operations()` - 9 edges
3. `main()` - 9 edges
4. `Darwin Core Skill` - 8 edges
5. `SKOS-XL Skill` - 8 edges
6. `Traditional Knowledge (CTA) Vocabularies` - 8 edges
7. `main()` - 7 edges
8. `main()` - 7 edges
9. `Scripts` - 6 edges
10. `Scripts` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Darwin Core Data Package (DwC-DP)` --implements--> `Darwin Core Conceptual Model (DwC-CM)`  [EXTRACTED]
  darwin-core/references/DATA_PACKAGE_GUIDE.md → darwin-core/references/CONCEPTUAL_MODEL.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **TDWG Standards Ratified 2026-05-26** — dwc_cm, dwc_dp [EXTRACTED 1.00]
- **Traditional Knowledge (CTA) Workflow** — skos_generate, skos_validate, cta_vocab [EXTRACTED 1.00]
- **Darwin Core Data Workflow** — dwc_sync, dwc_explain, dwc_validate [EXTRACTED 1.00]

## Communities (20 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.21
Nodes (13): main(), extract_meta_xml(), load_valid_terms(), Check if all files referenced in meta.xml exist inside the ZIP., Check if all terms used are valid Darwin Core terms., Load the set of valid Darwin Core term names., Check if the file is a valid ZIP archive., Extract and parse meta.xml from the ZIP. (+5 more)

### Community 1 - "Community 1"
Cohesion: 0.24
Nodes (11): list_terms(), main(), show_term_detail(), load_detailed_terms(), load_term_names(), Show detailed information for a specific term., List all available terms in columns., Load term names from the simple CSV list (all_dwc_vertical.csv). (+3 more)

### Community 2 - "Community 2"
Cohesion: 0.35
Nodes (10): list_cta_terms(), load_terms(), normalize_term(), show_cta_overview(), show_cta_term(), show_skos_overview(), show_skosxl_overview(), list_terms() (+2 more)

### Community 3 - "Community 3"
Cohesion: 0.12
Nodes (15): Darwin Core Archive (DwC-A), Darwin Core Conceptual Model (DwC-CM), Darwin Core Data Package (DwC-DP), 1. `analyze.py` — Analyze a spreadsheet and propose a structure, 2. `apply.py` — Write the corrected spreadsheet, biodiversityDataSkills, biohousekeeper, Installation (+7 more)

### Community 4 - "Community 4"
Cohesion: 0.38
Nodes (9): bind_common(), build_basic(), build_dwc_names(), build_dwc_vocab(), build_etno_tk(), main(), Template for a DwC controlled vocabulary (e.g. basisOfRecord values)., Template: TDWG TAG NameThing pattern for taxonomic names (SKOS-XL).     Referenc (+1 more)

### Community 5 - "Community 5"
Cohesion: 0.29
Nodes (9): convert_csv(), load_dwc_terms(), main(), normalize_column_name(), Load Darwin Core term names from the reference CSV., Normalize column name for dictionary lookup., Suggest DwC term mapping for each CSV column., Generate a new CSV with Darwin Core headers. (+1 more)

### Community 6 - "Community 6"
Cohesion: 0.43
Nodes (6): detect_format(), downgrade_from_xl(), main(), Upgrade plain SKOS labels to SKOS-XL Label resources., Downgrade SKOS-XL labels to plain SKOS literal labels., upgrade_to_xl()

### Community 7 - "Community 7"
Cohesion: 0.52
Nodes (6): detect_format(), label_of(), Additional checks for Traditional Knowledge (CTA) vocabularies.     Based on CAR, run_cta_checks(), run_standard_checks(), main()

### Community 8 - "Community 8"
Cohesion: 0.47
Nodes (5): generate_example_csv(), generate_meta_xml(), main(), Generate example CSV content with DwC headers., Generate the content of meta.xml.

### Community 9 - "Community 9"
Cohesion: 0.67
Nodes (3): download_file(), main(), Download a file from URL to destination path.

### Community 11 - "Community 11"
Cohesion: 0.08
Nodes (25): 1. Explain SKOS, SKOS-XL, and CTA properties, 1. Install Python 3.9+, 2. Install dependencies, 2. Validate a SKOS vocabulary file, 3. Generate a SKOS vocabulary template, 3. (Optional) Sync W3C schema files, 4. Convert vocabulary format or label style, 5. Sync reference files (+17 more)

### Community 13 - "Community 13"
Cohesion: 0.09
Nodes (22): 1. Explain the Darwin Core standard, 1. Install Python 3.9+, 2. Install dependencies, 2. Validate a Darwin Core Archive, 3. Generate a DwC-A template, 3. (Optional) Sync references, 4. Map CSV columns to DwC terms, 5. Sync references (+14 more)

### Community 16 - "Community 16"
Cohesion: 0.19
Nodes (21): analyze_columns(), build_report_md(), columns_similarity(), detect_binomial(), detect_coordinate_pair(), detect_locality_delimiter(), detect_operations(), _in_range() (+13 more)

### Community 17 - "Community 17"
Cohesion: 0.14
Nodes (14): 1. `sync.py` — Download reference schemas, 2. `explain.py` — Explore the standard, 3. `generate.py` — Generate a vocabulary template, 4. `validate.py` — Validate a SKOS file, 5. `convert.py` — Convert format or label style, Access levels (`etno:accessLevel`), CARE Principles, Key references (+6 more)

### Community 18 - "Community 18"
Cohesion: 0.20
Nodes (9): `apply.py` - write the corrected spreadsheet, `/biohousekeeper analyze <spreadsheet>`, BioHousekeeper Skill, Detection heuristics (what `analyze.py` looks for), References, Related Skills, Setup, Usage (+1 more)

### Community 19 - "Community 19"
Cohesion: 0.20
Nodes (10): 1. `sync.py` — Update reference data, 2. `explain.py` — Explore the standard, 3. `map_columns.py` — Map existing CSV data to DwC terms, 4. `generate_template.py` — Generate a DwC-A template, 5. `validate.py` — Validate a Darwin Core Archive, darwin-core, DwC-A Extensions, Reference files (+2 more)

### Community 20 - "Community 20"
Cohesion: 0.36
Nodes (8): apply_derive_taxon_epithets(), apply_merge_date_parts(), apply_split_coordinates(), apply_split_locality(), main(), read_spreadsheet(), unique_name(), write_spreadsheet()

## Knowledge Gaps
- **74 isolated node(s):** `Installation`, `Skills`, `Skills Interoperability`, `What is SKOS?`, `Setup` (+69 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `biodiversityDataSkills` connect `Community 3` to `Community 17`, `Community 19`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Why does `SKOS-XL Skill` connect `Community 11` to `Community 3`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `Darwin Core Skill` connect `Community 13` to `Community 3`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **What connects `Installation`, `Skills`, `Skills Interoperability` to the rest of the system?**
  _101 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.12418300653594772 - nodes in this community are weakly interconnected._
- **Should `Community 11` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 13` be split into smaller, more focused modules?**
  _Cohesion score 0.09090909090909091 - nodes in this community are weakly interconnected._