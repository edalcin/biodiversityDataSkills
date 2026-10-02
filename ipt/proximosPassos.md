# ipt — status and next steps

## Status (2026-10-02)

- Skill created: `SKILL.md`, 7 reference files, `scripts/ipt_health.py`, `scripts/sync_issues.py`.
- Sources: gbif/ipt main at commit `62097149` (3.3.7-SNAPSHOT), IPT manual, 2608 GitHub issues (to 2026-10-02).
- `ipt_health.py` verified:
  - public checks on https://ipt.gbif.org/ (IPT 3.3.4, test mode, 497 resources, ~207 s) and https://cloud.gbif.org/eca (3.3.6, production);
  - authenticated checks, `report` and `publish --yes` on a local Docker `gbif/ipt:latest` (3.3.6) container (removed after the test).
- https://ipt.jbrj.gov.br/jbrj/ answered 403 (AWS ELB) to scripted requests — not tested.

## Next steps

1. Run `check` with real credentials on a production instance (JBRJ / SiBBr) and tune thresholds of `GBIF-COUNT-MISMATCH`, `GBIF-NOT-RECRAWLED`, `GBIF-NEVER-CRAWLED` (not exercised against production data).
2. Exercise `LOG-ERRORS` on a long-running instance log (only tested on a fresh container).
3. Run skill evals (skill-creator loop): 2–3 realistic prompts, with/without skill.
4. Consider reporting upstream (gbif/ipt) the auth gaps documented in `references/endpoints.md` §10: `manage/report.do`, `manage/mappingPeek.do`, `manage/cancel.do` reachable anonymously on 3.3.6; mutations accepted over GET.
5. Re-sync after each IPT release: `python scripts/sync_issues.py`; review `releases.md` and `known-issues.md` "Open issues affecting operators".
