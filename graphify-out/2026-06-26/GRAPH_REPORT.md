# Graph Report - D:\git\biodiversityDataSkills  (2026-06-26)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 99 nodes · 129 edges · 16 communities (11 shown, 5 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `effdfa8d`
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
- [[_COMMUNITY_Community 14|Community 14]]

## God Nodes (most connected - your core abstractions)
1. `main()` - 9 edges
2. `main()` - 7 edges
3. `main()` - 6 edges
4. `bind_common()` - 5 edges
5. `main()` - 5 edges
6. `Darwin Core Skill` - 5 edges
7. `suggest_mapping()` - 4 edges
8. `main()` - 4 edges
9. `main()` - 4 edges
10. `build_dwc_vocab()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `biodiversityDataSkills` --references--> `Darwin Core Skill`  [EXTRACTED]
  README.md → darwin-core/SKILL.md
- `biodiversityDataSkills` --references--> `SKOS-XL Skill`  [EXTRACTED]
  README.md → skos-xl/SKILL.md
- `SKOS-XL Skill` --conceptually_related_to--> `Darwin Core Skill`  [EXTRACTED]
  skos-xl/SKILL.md → darwin-core/SKILL.md
- `Darwin Core Skill` --references--> `Darwin Core Archive (DwC-A)`  [EXTRACTED]
  darwin-core/SKILL.md → darwin-core/references/TEXT_GUIDE.md
- `Darwin Core Skill` --references--> `Darwin Core Conceptual Model (DwC-CM)`  [EXTRACTED]
  darwin-core/SKILL.md → darwin-core/references/CONCEPTUAL_MODEL.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **TDWG Standards Ratified 2026-05-26** — dwc_cm, dwc_dp [EXTRACTED 1.00]
- **Traditional Knowledge (CTA) Workflow** — skos_generate, skos_validate, cta_vocab [EXTRACTED 1.00]
- **Darwin Core Data Workflow** — dwc_sync, dwc_explain, dwc_validate [EXTRACTED 1.00]

## Communities (16 total, 5 thin omitted)

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
Cohesion: 0.24
Nodes (10): Traditional Knowledge (CTA) Vocabularies, Darwin Core Skill, Darwin Core Archive (DwC-A), Darwin Core Conceptual Model (DwC-CM), Darwin Core Data Package (DwC-DP), darwin-core/scripts/validate.py, biodiversityDataSkills, skos-xl/scripts/generate.py (+2 more)

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

## Knowledge Gaps
- **7 isolated node(s):** `SKOS & SKOS-XL Quick Reference Guide`, `Darwin Core Extensions`, `darwin-core/scripts/sync.py`, `darwin-core/scripts/explain.py`, `darwin-core/scripts/validate.py` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Load term names from the simple CSV list (all_dwc_vertical.csv).`, `Load all terms with full metadata (term_versions.csv), deduplicated.`, `Display a general overview of the Darwin Core standard.` to the rest of the system?**
  _31 weakly-connected nodes found - possible documentation gaps or missing edges._