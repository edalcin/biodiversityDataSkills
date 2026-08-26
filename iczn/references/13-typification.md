# Chapter 13 — The Type Concept in Nomenclature (Article 61)

Source: https://code.iczn.org/the-type-concept-in-nomenclature/ · 4th edition 1999

This chapter states the single organizing idea underneath the whole Code: names are anchored to physical or nominal objects (types), not to taxonomic opinion. Land here to understand *why* a name-bearing type exists, how the anchoring chain runs from species up to family group, and — critically — how it produces the objective/subjective synonymy distinction that a database must encode correctly or it will silently merge facts with opinions.

## Article 61 — Principle of Typification
Every nominal taxon in the family, genus and species groups has (actually or potentially) a name-bearing type, fixed once and stable thereafter.

- **61.1** — Each nominal taxon in the three name-group ranks has a name-bearing type; fixing it creates the objective standard of reference for applying the name, independent of how later authors draw the taxon's boundaries. [Art. 61.1](https://code.iczn.org/the-type-concept-in-nomenclature/article-61-principle-of-typification/#art-61-1)
  - **61.1.1** — The taxon's boundaries may be redrawn at will by taxonomic opinion; the valid name nonetheless tracks whichever name-bearing type falls inside those boundaries (see Art. 23.3, `references/06-validity-priority.md`).
  - **61.1.2** — The anchoring is recursive across ranks: a species-group name-bearing type is a specimen or set of specimens (holotype, lectotype, neotype, or syntypes — Art. 72.1.2, `references/16-species-group-types.md`); a genus-group name-bearing type is a nominal species, itself defined by its own type; a family-group name-bearing type is the nominal genus the family name is built on. **This is the traversable chain a database should model explicitly**: family → type genus → type species → type specimen(s). Every family-group name, followed down this chain, ultimately rests on a physical specimen.
  - **61.1.3** — Once fixed under the Code, a name-bearing type is stable and does not change except: for genus-group taxa, under the misidentified-type-species provision (Art. 70.3.2, `references/15-genus-group-types.md`); for species-group taxa, under Arts. 74–75 (`references/16-species-group-types.md`); or by the Commission's plenary power (Art. 81, `references/17-commission.md`).
- **61.2** — A name-bearing type fixed for a nominal taxon is simultaneously fixed for its nominotypical subordinate/superordinate taxon (Arts. 37.1, 44.1, 47.1) — the two share one type by construction, not by separate act.
  - **61.2.1** — If different types are fixed simultaneously for a taxon and its nominotypical taxon, the fixation at the higher rank wins.
  - **61.2.2** — Raising, lowering, or simultaneous multi-rank use of a nominal taxon's name never changes its name-bearing type (Arts. 36.2, 43.1, 46.2).
- **61.3** — Name-bearing types are what make a synonymy either a **fact** or an **opinion**, and the Code's vocabulary keeps the two apart on purpose:
  - **61.3.1 — subjective synonymy.** When nominal taxa with *different* name-bearing types are judged by a taxonomist to belong to one taxonomic taxon, their names become subjective synonyms **at that rank only** — the judgment can be reversed by another taxonomist, and the names need not be synonyms at a subordinate rank. [Art. 61.3.1](https://code.iczn.org/the-type-concept-in-nomenclature/article-61-principle-of-typification/#art-61-3-1)
  - **61.3.2** — If two genus-group names are objective synonyms (same or objectively-synonymous type species), any family-group names built on those genera are automatically objective synonyms too.
  - **61.3.3 — objective synonymy (genus group).** Two genus-group names with the same type species, or with type species that are themselves objective synonyms, are objective synonyms of each other. This is a **derivable fact**, not a judgment call. [Art. 61.3.3](https://code.iczn.org/the-type-concept-in-nomenclature/article-61-principle-of-typification/#art-61-3-3)
  - **61.3.4 — objective synonymy (species group).** Two species-group names sharing the same name-bearing type specimen(s) are objective synonyms. Same logic, one rank down.
- **61.4** — If a nominal subgenus is fixed as the name-bearing type of a family-group taxon, it is treated as if first raised to genus rank; likewise a nominal subspecies fixed as the type of a genus-group taxon is treated as first raised to species rank.

**Database relevance:** This is the load-bearing distinction for any taxonomic data model:
- **Objective synonymy** (Arts. 61.3.2–61.3.4) follows mechanically from shared/linked type records. It should be a *computed* relationship (join on type identity), never hand-entered, and it carries no asserting-author field because it is not an opinion.
- **Subjective synonymy** (Art. 61.3.1) is an *asserted* relationship that must always carry: the asserting author, the publication, and the rank at which it was asserted (it may not hold at a subordinate rank). Treat it as a reviewable claim, not a fact.
- Model type fixation itself as a first-class record per name: which type, by what act (original designation / monotypy / tautonymy / subsequent designation — see `references/15-genus-group-types.md` and `references/16-species-group-types.md`), in which publication, by which author. Everything else (objective synonymy, the traversable family→genus→species→specimen chain) derives from that record.
- See `references/data-modeling.md` for the concrete schema treatment.

**Common errors:** Treating a subjective synonymy as if it were permanent or author-independent; conflating "same type species" (objective, factual) with "I think these are the same species" (subjective, opinion-bound); forgetting that a name-bearing type, once validly fixed, cannot be changed by ordinary taxonomic revision — only by the specific escape hatches in 61.1.3.
