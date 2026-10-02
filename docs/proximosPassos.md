# biodiversityDataSkills — status e próximos passos

## Status (2026-10-02)

| Skill | Estado | Pendências |
|---|---|---|
| darwin-core | Pronta (DwC-A, DwC-CM, DwC-DP) | — |
| skos-xl | Pronta | — |
| biohousekeeper | Pronta | — |
| grist-master | Pronta (referência) | — |
| DataProvenance | Pronta (referência) | — |
| iczn | Pronta | Ver [`iczn/proximosPassos.md`](../iczn/proximosPassos.md) |
| ipt | Pronta (v1): 7 referências, `ipt_health.py`, `sync_issues.py` | Ver [`ipt/proximosPassos.md`](../ipt/proximosPassos.md) |

## Próximos passos

1. **ipt**: rodar `check` com credenciais em uma instância de produção (JBRJ/SiBBr) e ajustar limites de `GBIF-COUNT-MISMATCH`, `GBIF-NOT-RECRAWLED`, `GBIF-NEVER-CRAWLED`.
2. **ipt**: reportar ao gbif/ipt as falhas de auth (`manage/report.do`, `mappingPeek.do`, `cancel.do` anônimos; mutações via GET) — `ipt/references/endpoints.md` §10.
3. **ipt**: reexecutar `python ipt/scripts/sync_issues.py` a cada release do IPT.
4. Rodar evals (skill-creator) nas skills novas: ipt e iczn.
