# Graph Report - biodiversityDataSkills  (2026-07-23)

## Corpus Check
- 34 files · ~35,362 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 337 nodes · 408 edges · 26 communities (24 shown, 2 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3258f1ae`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- CLAUDE.md
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Grist Formulas & Functions
- Grist Access Rules
- Grist Column Types & References
- Available tools
- Grist REST API Reference

## God Nodes (most connected - your core abstractions)
1. `Grist Column Types & References` - 13 edges
2. `Grist Access Rules` - 12 edges
3. `Self-Hosted Grist` - 11 edges
4. `Operations` - 11 edges
5. `biodiversityDataSkills` - 10 edges
6. `Grist Formulas & Functions` - 9 edges
7. `detect_operations()` - 9 edges
8. `main()` - 9 edges
9. `Darwin Core Skill` - 8 edges
10. `SKOS-XL Skill` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Darwin Core Data Package (DwC-DP)` --implements--> `Darwin Core Conceptual Model (DwC-CM)`  [EXTRACTED]
  darwin-core/references/DATA_PACKAGE_GUIDE.md → darwin-core/references/CONCEPTUAL_MODEL.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **TDWG Standards Ratified 2026-05-26** — dwc_cm, dwc_dp [EXTRACTED 1.00]

## Communities (26 total, 2 thin omitted)

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
Cohesion: 0.08
Nodes (25): Darwin Core Archive (DwC-A), Darwin Core Conceptual Model (DwC-CM), Darwin Core Data Package (DwC-DP), 1. `analyze.py` — Analyze a spreadsheet and propose a structure, 1. `sync.py` — Update reference data, 2. `apply.py` — Write the corrected spreadsheet, 2. `explain.py` — Explore the standard, 3. `map_columns.py` — Map existing CSV data to DwC terms (+17 more)

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

### Community 14 - "CLAUDE.md"
Cohesion: 0.11
Nodes (18): Accounts, Documents and data, Grist and your website/app, Grist FAQ, Plans, Sharing, Grist Glossary, Custom widgets (Plugin API) (+10 more)

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
Cohesion: 0.10
Nodes (21): Administrator account, Authentication, Automatic version checks, Customization, Editions, Hardware, High availability, Install (Docker) (+13 more)

### Community 20 - "Community 20"
Cohesion: 0.36
Nodes (8): apply_derive_taxon_epithets(), apply_merge_date_parts(), apply_split_coordinates(), apply_split_locality(), main(), read_spreadsheet(), unique_name(), write_spreadsheet()

### Community 21 - "Grist Formulas & Functions"
Cohesion: 0.11
Nodes (19): Aggregating without hand-written "totals rows", `class Record` (`rec`), `class RecordSet`, `class UserTable`, Code viewer, Column behavior (3 states), Cumulative functions, Formula basics (+11 more)

### Community 22 - "Grist Access Rules"
Cohesion: 0.11
Nodes (18): Access rule memos, Basic conditions, Column restriction, Enabling / disabling, Grist Access Rules, Link keys, Permissions, Private table (+10 more)

### Community 23 - "Grist Column Types & References"
Cohesion: 0.15
Nodes (13): Attachment columns, Choice / Choice List columns, Date / DateTime columns, Four relationship shapes (design guidance), Grist Column Types & References, Managing columns, Numeric / Integer columns, Reference columns (+5 more)

### Community 24 - "Available tools"
Cohesion: 0.17
Nodes (12): Attachments, Auth & consent, Available tools, Discovery, Grist MCP Server, Managing documents and schema, Pages and widgets, Reading data (+4 more)

### Community 25 - "Grist REST API Reference"
Cohesion: 0.22
Nodes (9): API client libraries, API keys (script/personal use), Authentication, Grist REST API Reference, OAuth apps (third-party tools, AI agents, partner apps), REST endpoint groups, Scopes, SQL endpoint (+1 more)

## Knowledge Gaps
- **166 isolated node(s):** `Installation`, `Skills`, `Skills Interoperability`, `What is SKOS?`, `Setup` (+161 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `biodiversityDataSkills` connect `Community 3` to `Community 17`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `Self-Hosted Grist` connect `Community 19` to `CLAUDE.md`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `Grist Formulas & Functions` connect `Grist Formulas & Functions` to `CLAUDE.md`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **What connects `Installation`, `Skills`, `Skills Interoperability` to the rest of the system?**
  _166 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.07671957671957672 - nodes in this community are weakly interconnected._
- **Should `Community 11` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Community 13` be split into smaller, more focused modules?**
  _Cohesion score 0.09090909090909091 - nodes in this community are weakly interconnected._