# Graph Report - D:\git\biodiversityDataSkills  (2026-08-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 290 nodes · 348 edges · 26 communities (21 shown, 5 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `821ef035`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- PROV-DM: The PROV Data Model
- 2. Expressions per component
- analyze.py
- 3. XML elements per component (source §3)
- PROV_N.md
- Grist Access Rules
- Grist Column Types & References
- darwin-core/scripts/validate.py
- Intuitive overview
- darwin-core/scripts/explain.py
- skos-xl/scripts/explain.py
- biodiversityDataSkills
- apply.py
- Grist Formulas & Functions
- Grist REST API Reference
- generate.py
- map_columns.py
- convert.py
- skos-xl/scripts/validate.py
- generate_template.py
- download_file
- skos-xl/scripts/sync.py
- Darwin Core Conceptual Model (DwC-CM)
- Darwin Core Archive (DwC-A)
- Darwin Core Extensions
- SKOS & SKOS-XL Quick Reference Guide

## God Nodes (most connected - your core abstractions)
1. `Grist Column Types & References` - 13 edges
2. `Grist Access Rules` - 12 edges
3. `Intuitive overview` - 10 edges
4. `PROV-DM: The PROV Data Model` - 9 edges
5. `main()` - 9 edges
6. `detect_operations()` - 9 edges
7. `2. Expressions per component` - 8 edges
8. `3. XML elements per component (source §3)` - 8 edges
9. `7. Further elements of PROV-DM (§5.7)` - 7 edges
10. `PROV-N: The Provenance Notation` - 7 edges

## Surprising Connections (you probably didn't know these)
- `biodiversityDataSkills` --references--> `BioHousekeeper Skill`  [EXTRACTED]
  README.md → biohousekeeper/SKILL.md
- `biodiversityDataSkills` --references--> `Darwin Core Skill`  [EXTRACTED]
  README.md → darwin-core/SKILL.md
- `biodiversityDataSkills` --references--> `DataProvenance Skill`  [EXTRACTED]
  README.md → DataProvenance/SKILL.md
- `biodiversityDataSkills` --references--> `Grist Master Skill`  [EXTRACTED]
  README.md → grist-master/SKILL.md
- `biodiversityDataSkills` --references--> `SKOS-XL Skill`  [EXTRACTED]
  README.md → skos-xl/SKILL.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Biodiversity Data Standardization Flow** — biohousekeeper_skill, darwin_core_skill, skos_xl_skill [EXTRACTED 0.95]
- **Data Lineage and Provenance Integration** — dataprovenance_skill, darwin_core_skill, skos_xl_skill [EXTRACTED 0.90]
- **Grist Core Documentation** — grist_faq, grist_formulas_and_functions, grist_glossary, grist_integrations, grist_self_hosted [EXTRACTED 0.90]
- **SKOS-XL Vocabulary Patterns** — skos_xl_cta, skos_xl_dwc, skos_xl_skill [EXTRACTED 0.95]

## Communities (26 total, 5 thin omitted)

### Community 0 - "PROV-DM: The PROV Data Model"
Cohesion: 0.07
Nodes (30): 1. What PROV-DM is, 2. Core types, 3. Core relations (Components 1–3), 4. Component 4: Bundles (§5.4), 5. Component 5: Alternate entities (§5.5), 6. Component 6: Collections (§5.6), 7. Further elements of PROV-DM (§5.7), 8. Cross-reference to PROV-N and PROV-O (Appendix A) (+22 more)

### Community 1 - "2. Expressions per component"
Cohesion: 0.08
Nodes (24): 1.1 Functional-style syntax, 1.2 EBNF grammar conventions, 1.3 Optional terms and the `-` marker, 1.4 Identifiers and attributes, 1.5 Qualified names / namespaces, 1.6 Comments, 1. Grammar basics, 2.1 Component 1: Entities and Activities (+16 more)

### Community 2 - "analyze.py"
Cohesion: 0.19
Nodes (21): analyze_columns(), build_report_md(), columns_similarity(), detect_binomial(), detect_coordinate_pair(), detect_locality_delimiter(), detect_operations(), _in_range() (+13 more)

### Community 3 - "3. XML elements per component (source §3)"
Cohesion: 0.10
Nodes (20): 1. PROV namespace, 2.1 Schema modularization, 2.2 Salami slice design pattern, 2.3 Elements vs. attributes, 2.4 Type conventions, 2.5 Identifier conventions, 2.6 Naming conventions, 2. XML schema design conventions (source §2) (+12 more)

### Community 4 - "PROV_N.md"
Cohesion: 0.14
Nodes (13): PROV Glossary, Classes, Expanded Terms, Properties, PROV-O: The PROV Ontology, Qualifiable relations, Qualified and supporting properties, Qualified classes (+5 more)

### Community 5 - "Grist Access Rules"
Cohesion: 0.11
Nodes (18): Access rule memos, Basic conditions, Column restriction, Enabling / disabling, Grist Access Rules, Link keys, Permissions, Private table (+10 more)

### Community 6 - "Grist Column Types & References"
Cohesion: 0.13
Nodes (13): Attachment columns, Choice / Choice List columns, Date / DateTime columns, Four relationship shapes (design guidance), Grist Column Types & References, Managing columns, Numeric / Integer columns, Reference columns (+5 more)

### Community 7 - "darwin-core/scripts/validate.py"
Cohesion: 0.21
Nodes (13): main(), extract_meta_xml(), load_valid_terms(), Check if all files referenced in meta.xml exist inside the ZIP., Check if all terms used are valid Darwin Core terms., Load the set of valid Darwin Core term names., Check if the file is a valid ZIP archive., Extract and parse meta.xml from the ZIP. (+5 more)

### Community 8 - "Intuitive overview"
Cohesion: 0.14
Nodes (13): Activities, Agents and Responsibility, Alternate Entities and Specialization, Derivation and Revision, Entities, Intuitive overview, Plans, PROV-N relations used in the worked example (+5 more)

### Community 9 - "darwin-core/scripts/explain.py"
Cohesion: 0.24
Nodes (11): list_terms(), main(), show_term_detail(), load_detailed_terms(), load_term_names(), Show detailed information for a specific term., List all available terms in columns., Load term names from the simple CSV list (all_dwc_vertical.csv). (+3 more)

### Community 10 - "skos-xl/scripts/explain.py"
Cohesion: 0.35
Nodes (10): list_cta_terms(), load_terms(), normalize_term(), show_cta_overview(), show_cta_term(), show_skos_overview(), show_skosxl_overview(), list_terms() (+2 more)

### Community 11 - "biodiversityDataSkills"
Cohesion: 0.22
Nodes (10): biodiversityDataSkills, BioHousekeeper Skill, Darwin Core Skill, DataProvenance Skill, Grist Master Skill, Traditional Knowledge (CTA) Vocabularies, Darwin Core Integration, SKOS-XL Requirements (+2 more)

### Community 12 - "apply.py"
Cohesion: 0.36
Nodes (8): apply_derive_taxon_epithets(), apply_merge_date_parts(), apply_split_coordinates(), apply_split_locality(), main(), read_spreadsheet(), unique_name(), write_spreadsheet()

### Community 13 - "Grist Formulas & Functions"
Cohesion: 0.20
Nodes (10): Grist FAQ, Grist Formulas & Functions, Python in Grist Formulas, Grist Glossary, Grist Integrations, Grist MCP Server, Grist Sandboxing (gVisor), Self-Hosted Grist (+2 more)

### Community 14 - "Grist REST API Reference"
Cohesion: 0.20
Nodes (9): API client libraries, API keys (script/personal use), Authentication, Grist REST API Reference, OAuth apps (third-party tools, AI agents, partner apps), REST endpoint groups, Scopes, SQL endpoint (+1 more)

### Community 15 - "generate.py"
Cohesion: 0.38
Nodes (9): bind_common(), build_basic(), build_dwc_names(), build_dwc_vocab(), build_etno_tk(), main(), Template for a DwC controlled vocabulary (e.g. basisOfRecord values)., Template: TDWG TAG NameThing pattern for taxonomic names (SKOS-XL).     Referenc (+1 more)

### Community 16 - "map_columns.py"
Cohesion: 0.29
Nodes (9): convert_csv(), load_dwc_terms(), main(), normalize_column_name(), Load Darwin Core term names from the reference CSV., Normalize column name for dictionary lookup., Suggest DwC term mapping for each CSV column., Generate a new CSV with Darwin Core headers. (+1 more)

### Community 17 - "convert.py"
Cohesion: 0.43
Nodes (6): detect_format(), downgrade_from_xl(), main(), Upgrade plain SKOS labels to SKOS-XL Label resources., Downgrade SKOS-XL labels to plain SKOS literal labels., upgrade_to_xl()

### Community 18 - "skos-xl/scripts/validate.py"
Cohesion: 0.52
Nodes (6): detect_format(), label_of(), Additional checks for Traditional Knowledge (CTA) vocabularies.     Based on CAR, run_cta_checks(), run_standard_checks(), main()

### Community 19 - "generate_template.py"
Cohesion: 0.47
Nodes (5): generate_example_csv(), generate_meta_xml(), main(), Generate example CSV content with DwC headers., Generate the content of meta.xml.

### Community 20 - "download_file"
Cohesion: 0.67
Nodes (3): download_file(), main(), Download a file from URL to destination path.

## Knowledge Gaps
- **126 isolated node(s):** `Core vs. extended structures`, `The six components`, `Entity (§5.1.1)`, `Activity (§5.1.2)`, `Agent sub-kinds (extended structures, §5.3.1)` (+121 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PROV-DM: The PROV Data Model` connect `PROV-DM: The PROV Data Model` to `PROV_N.md`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `PROV-N: The Provenance Notation` connect `2. Expressions per component` to `PROV_N.md`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `PROV-XML: The PROV XML Schema` connect `3. XML elements per component (source §3)` to `PROV_N.md`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **What connects `Core vs. extended structures`, `The six components`, `Entity (§5.1.1)` to the rest of the system?**
  _126 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `PROV-DM: The PROV Data Model` be split into smaller, more focused modules?**
  _Cohesion score 0.06666666666666667 - nodes in this community are weakly interconnected._
- **Should `2. Expressions per component` be split into smaller, more focused modules?**
  _Cohesion score 0.08333333333333333 - nodes in this community are weakly interconnected._
- **Should `3. XML elements per component (source §3)` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._