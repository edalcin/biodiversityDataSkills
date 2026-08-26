# Chapter 9 — Genus-Group Nominal Taxa and their Names (Articles 42–44)

Source: https://code.iczn.org/genus-group-nominal-taxa-and-their-names/ · 4th edition 1999

Land here for anything about genera and subgenera: what ranks the genus group covers, how a genus name and its nominotypical subgenus relate, and how coordination between genus and subgenus works. This chapter is the shortest of the three rank-group chapters (only 3 Articles) because most genus-group substance — type-species fixation, homonymy — lives in Chapters 15 (types) and 12 (homonymy).

## Article 42 — The genus group
Defines the rank range and the type-species-based application rule.

- **42.1** — The genus group sits between the family group and the species group and encompasses exactly two ranks: genus and subgenus [see also Arts. 10.3, 10.4]. [Art. 42.1](https://code.iczn.org/genus-group-nominal-taxa-and-their-names/article-42-the-genus-group/#art-42-1)
- **42.2** — Genus and subgenus names are governed by identical rules except where an Article explicitly names only one rank.
  - **42.2.1** — Names for "collective groups" (taxonomic-convenience assemblages) and for genus-group-level ichnotaxa (trace fossils) count as genus-group names under the Code [Art. 10.3] unless a specific Article says otherwise (exceptions listed: Arts. 13.3.2, 13.3.3, 23.7, 42.3.1, 66, 67.14); each keeps its own original author and date. [Art. 42.2.1](https://code.iczn.org/genus-group-nominal-taxa-and-their-names/article-42-the-genus-group/#art-42-2-1)
- **42.3** — A genus-group name's application is fixed by its type species [Arts. 61, 66–70], not by later content or usage.
  - **42.3.1** — Collective groups have no type species at all — do not attempt to assign one. [Art. 42.3.1](https://code.iczn.org/genus-group-nominal-taxa-and-their-names/article-42-the-genus-group/#art-42-3-1)
  - **42.3.2** — Genus-group taxa established before 1931 (before 2000 for ichnotaxa [Art. 13.3.3]) may never have had a type species originally fixed; Art. 69 (subsequent type fixation) governs those cases. [Art. 42.3.2](https://code.iczn.org/genus-group-nominal-taxa-and-their-names/article-42-the-genus-group/#art-42-3-2)
- **42.4** — Formation/treatment follows Arts. 10.3, 10.4, 11.8, and the relevant parts of Arts. 25–33. [Art. 42.4](https://code.iczn.org/genus-group-nominal-taxa-and-their-names/article-42-the-genus-group/#art-42-4)

**Database relevance:** the genus group has exactly two ranks (genus, subgenus) — do not extend a genus-group taxon table to accept arbitrary "infrageneric" rank strings beyond subgenus; anything finer is not regulated as a separate genus-group rank by the Code. Collective-group and ichnotaxon genus-group names need a `has_type_species = false` allowance (42.3.1) that ordinary genera and subgenera do not get.

## Article 43 — Principle of Coordination
- **43.1** — A name established at either rank in the genus group (genus OR subgenus) is deemed simultaneously established by the same author, on the same date, for a nominal taxon at the OTHER rank in the group; both the genus-rank and subgenus-rank taxa share the same type species, regardless of whether that type species was fixed originally or only later. Practical effect: naming a genus also automatically names its (as yet possibly unnamed) nominotypical subgenus, and vice versa for a subgenus named first. [Art. 43.1](https://code.iczn.org/genus-group-nominal-taxa-and-their-names/article-43-principle-of-coordination/#art-43-1)
- **43.2** — Raising a subgenus to genus rank, or lowering a genus to subgenus rank, never changes its type species [Art. 61.2.2], regardless of whether that type species was fixed originally or subsequently. [Art. 43.2](https://code.iczn.org/genus-group-nominal-taxa-and-their-names/article-43-principle-of-coordination/#art-43-2)

**Database relevance:** exactly as with the family group (`references/08-family-group.md` Art. 36) and the species group (`references/10-species-group.md` Art. 46), one authorship event produces a coordinate PAIR of names (genus + subgenus), same author, same date, same type species. A genus record and its nominotypical-subgenus record are not independent rows with independently entered authorship — the subgenus row's author/date/type_species must be derived from (or validated against) the genus row's, not entered separately by a data-entry operator transcribing a different citation.

## Article 44 — Nominotypical taxa
- **44.1** — When a genus is treated as containing subgenera, the subgenus that contains the genus's own type species is denoted by the SAME name as the genus (not a different subgeneric epithet), with the same author and date [Art. 43.1]. This is the "nominotypical subgenus" — e.g. genus *Mus* Linnaeus, 1758 has nominotypical subgenus *Mus* (*Mus*) Linnaeus, 1758. [Art. 44.1](https://code.iczn.org/genus-group-nominal-taxa-and-their-names/article-44-nominotypical-taxa/#art-44-1)
- **44.2** — If the genus name in use (and hence its nominotypical subgenus name) has to be replaced under Art. 23.3.5 because it is unavailable or invalid, the subgenus that contains the type species of the newly valid genus name becomes the new nominotypical subgenus — nominotypical status follows the type species, not the old label. [Art. 44.2](https://code.iczn.org/genus-group-nominal-taxa-and-their-names/article-44-nominotypical-taxa/#art-44-2)

**Database relevance:** never store the nominotypical subgenus as a manually authored name distinct from the genus — it is definitionally the genus's own name repeated at subgenus rank, and its identity must be recomputed if the genus's valid name changes (44.2), not left pointing at a stale label.
