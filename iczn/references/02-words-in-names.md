# Chapter 2 — The Number of Words in the Scientific Names of Animals (Articles 4–6)

Source: https://code.iczn.org/chapter-2-the-number-of-words-in-the-scientific-names-of-animals/ · 4th edition 1999

This chapter fixes how many name-tokens a taxon's scientific name has at each rank, and what may (and may not) be inserted between those tokens. Land here when validating that a stored name string has the right word count and capitalization for its rank, or when deciding whether a bracketed interpolation is a real name component.

## Article 4 — Names of taxa at ranks above the species group
Uninominal naming above the species group, and the one restriction on using a subgeneric name alone.

- **4.1** — A name for any taxon ranked above the species group (genus and up) is a single word (uninominal) and must start with an upper-case letter [Art. 28]. [Art. 4.1](https://code.iczn.org/chapter-2-the-number-of-words-in-the-scientific-names-of-animals/article-4-names-of-taxa-at-ranks-above-the-species-group/#art-4-1)
- **4.2** — A subgeneric name may stand alone as the first element of a binomen/trinomen only when it is actually being used *as* the genus name (i.e., promoted to genus rank in that usage); otherwise it must appear only as the parenthetical interpolation described in Art. 6.1. [Art. 4.2](https://code.iczn.org/chapter-2-the-number-of-words-in-the-scientific-names-of-animals/article-4-names-of-taxa-at-ranks-above-the-species-group/#art-4-2)

**Database relevance:** `scientificName` fields above species rank should validate as exactly one capitalized token; a genus/subgenus rank flag distinguishes "used as genus" from "used as subgenus" for the same word.

## Article 5 — Principle of Binominal Nomenclature
The defining rule of zoological names: species names are two-part, subspecies names three-part. Note the Code's own term is **binominal** ("two-name"), not the more common English word "binomial" ("two-number/term") — keep the Code's spelling when citing the Principle itself.

- **5.1** — The scientific name of a species — and only a species, no other rank — is a binomen: generic name (upper-case initial) + specific name (lower-case initial) [Art. 28]. In a database, `species` is therefore never a single token; it is always `genus + specificEpithet`, and no other taxonomic rank stores a two-token name under this Article. [Art. 5.1](https://code.iczn.org/chapter-2-the-number-of-words-in-the-scientific-names-of-animals/article-5-principle-of-binominal-nomenclature/#art-5-1)
  - **5.1.1** — Availability of a genus-group name published without an associated nominal species, and of a subspecific name published only inside a trinomen, is governed instead by Art. 11.4 (`references/11-authorship.md`) — Art. 5 states the *form* of the name, Art. 11.4 states when such a name counts as *available*. [Art. 5.1.1](https://code.iczn.org/chapter-2-the-number-of-words-in-the-scientific-names-of-animals/article-5-principle-of-binominal-nomenclature/#art-5-1-1)
  - **5.1.2** — How subgeneric names and species/subspecies-aggregate names interact with the Principle is deferred to Art. 6, immediately below. [Art. 5.1.2](https://code.iczn.org/chapter-2-the-number-of-words-in-the-scientific-names-of-animals/article-5-principle-of-binominal-nomenclature/#art-5-1-2)
- **5.2** — The scientific name of a subspecies is a trinomen: binomen + subspecific name (lower-case initial) [Art. 11.4.2, `references/11-authorship.md`]. There is no valid rank between species and subspecies that gets its own name component under this Article. [Art. 5.2](https://code.iczn.org/chapter-2-the-number-of-words-in-the-scientific-names-of-animals/article-5-principle-of-binominal-nomenclature/#art-5-2)
- **5.3** — Qualifying marks such as `?`, `aff.`, `cf.`, `prox.` are never part of the scientific name, even when written between its components (e.g. `Genus cf. species`); a parser must strip these before treating the remainder as the name proper. [Art. 5.3](https://code.iczn.org/chapter-2-the-number-of-words-in-the-scientific-names-of-animals/article-5-principle-of-binominal-nomenclature/#art-5-3)

**Database relevance:** `scientificName` word-count validation: genus rank = 1 token; species = 2 tokens; subspecies = 3 tokens (see Art. 6 below for the *non-counted* interpolations that may legitimately appear between them). Open-nomenclature qualifiers (`cf.`, `aff.`, `?`) belong in an `identificationQualifier`-style field, never concatenated into `scientificName` (see also `references/dwc-mapping.md`).

## Article 6 — Interpolated names
Parenthetical material that may sit between the counted words of a binomen/trinomen without itself counting as one of those words.

- **6.1** — A subgeneric name used alongside a binomen/trinomen must be interpolated in parentheses between the generic and specific names (e.g. `Genus (Subgenus) species`), begins with an upper-case letter, and is *not* one of the counted words of the binomen/trinomen. [Art. 6.1](https://code.iczn.org/chapter-2-the-number-of-words-in-the-scientific-names-of-animals/article-6-interpolated-names/#art-6-1)
- **6.2** — A parenthetical species-group name may likewise be interpolated (after the genus-group name, or between genus-group and specific name, or between specific and subspecific name) to denote an informal aggregate — e.g. a superspecies grouping of related species. Such interpolated names always start lower-case, are written in full (not abbreviated), are not counted as words of the binomen/trinomen, but do compete under the Principle of Priority [Art. 23.3.3, `references/06-validity-priority.md`]; their availability is governed by Art. 11.9.3.5 (`references/11-authorship.md`). [Art. 6.2](https://code.iczn.org/chapter-2-the-number-of-words-in-the-scientific-names-of-animals/article-6-interpolated-names/#art-6-2)

**Recommendations:** Rec. 6A (advisory) — do not interpolate any genus-group name other than a valid subgenus between generic and specific name, even in brackets; write a former-combination cross-reference in explicit prose instead. Rec. 6B (advisory) — when using an Art. 6.2 aggregate notation, state its taxonomic meaning (e.g. "superspecies") in the same parentheses the first time it is used in a work.

**Database relevance:** a `scientificName` parser must recognize `(Subgenus)` and lower-case `(aggregateName)` interpolations as structurally distinct, non-counted tokens — store the subgenus in its own field (e.g. Darwin Core `subgenus`) and never let either interpolation shift the computed word-count validation from Art. 5.

**Common errors:** treating an interpolated subgenus as part of the specific epithet token count, or capitalizing a species/subspecies-aggregate interpolation as if it were a subgenus — the Code fixes case (upper vs. lower) specifically to distinguish the two.
