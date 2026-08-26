# Chapter 12 — Homonymy (Articles 52–60)

Source: https://code.iczn.org/homonymy/ · 4th edition 1999

This chapter decides which of two identically-spelled names for different taxa wins the name, and what happens to the loser. Land here when validating whether a "duplicate name" flag is nomenclaturally real, when deciding whether a junior homonym needs a *nomen novum*, or when modelling the rank-specific definitions of "identical spelling" that Art. 58 forces on any string-matching validator.

## Article 52 — Principle of Homonymy
States and scopes the core rule that identical names for different taxa cannot both stand.

- **52.1** — Distinct taxa must not carry the same name. [Art. 52.1](https://code.iczn.org/homonymy/article-52-principle-of-homonymy/#art-52-1)
- **52.2 — operation:** among homonyms, only the *senior* (by [Art. 23 Priority](06-validity-priority.md)) may be used as valid. Exceptions: unused senior homonyms superseded by long-accepted junior ones ([Arts. 23.2, 23.9](06-validity-priority.md)), and secondary species-group homonyms under [Art. 59](#article-59-validity-of-secondary-homonyms) below. [Art. 52.2](https://code.iczn.org/homonymy/article-52-principle-of-homonymy/#art-52-2)
- **52.3** — Relative precedence among homonyms (including primary vs. secondary species-group homonyms, see Art. 57 below) is decided by [Art. 23 Priority](06-validity-priority.md) and [Art. 24 First Reviser](06-validity-priority.md). [Art. 52.3](https://code.iczn.org/homonymy/article-52-principle-of-homonymy/#art-52-3)
- **52.4** — Replacement of junior homonyms: see [Arts. 23.3.5, 23.9.5](06-validity-priority.md), [39](08-family-group.md), [55](#article-55-family-group-names), [60](#article-60-replacement-of-junior-homonyms) below.
- **52.5 — junior homonym invalidity is the default outcome**, but senior homonyms can be *suppressed* by a Commission ruling under [Arts. 54.4, 81.2.1](17-commission.md) — i.e. Commission action can reverse which name of a homonymous pair survives; absent such action the junior stays permanently invalid (subject to the Art. 23.9/59 exceptions). [Art. 52.5](https://code.iczn.org/homonymy/article-52-principle-of-homonymy/#art-52-5)
- **52.6** — A *corrected* original spelling can enter homonymy; an *incorrect* original spelling cannot, since it is not itself available ([Art. 32.4](07-formation-spelling.md)). [Art. 52.6](https://code.iczn.org/homonymy/article-52-principle-of-homonymy/#art-52-6)
- **52.7 — secondary homonymy defined generally at Art. 52.2/53.3** below is not to be confused with cross-kingdom name clashes: an animal name identical to a name that has never been treated as an animal name is not a homonym under this Code ([Arts. 1.4, 2.2](01-nomenclature.md)). [Art. 52.7](https://code.iczn.org/homonymy/article-52-principle-of-homonymy/#art-52-7)

## Article 53 — Definitions of homonymy in the family group, genus group and species group
Fixes what "identical spelling" means at each nomenclatural rank — the three definitions are not interchangeable.

- **53.1 — family group:** two available names with the same spelling, or differing only in the rank-suffix ([Art. 29.2](08-family-group.md)), that denote *different* nominal taxa are homonyms — **regardless of whether their type genera are the same or different.** [Art. 53.1](https://code.iczn.org/homonymy/article-53-definitions-of-homonymy-in-the-family-group-genus-group-and-species-group/#art-53-1)
- **53.2 — genus group:** two available names established with the same spelling are homonyms, **full stop — no qualification by taxon, rank of use, or type species.** [Art. 53.2](https://code.iczn.org/homonymy/article-53-definitions-of-homonymy-in-the-family-group-genus-group-and-species-group/#art-53-2)
- **53.3 — species group:** two available species-group names with the same spelling are homonyms **only if combined with the same generic name** — either originally (primary homonymy) or subsequently (secondary homonymy, see Art. 57 below); an exception for names combined with homonymous *generic* names is at [Art. 57.8.1](#article-57-species-group-names). [Art. 53.3](https://code.iczn.org/homonymy/article-53-definitions-of-homonymy-in-the-family-group-genus-group-and-species-group/#art-53-3) **This is the pivotal asymmetry: family- and genus-group homonymy is absolute (spelling alone), species-group homonymy is relative to the current generic combination — the identical specific epithet `variegata` in two different genera is simply not a homonymy case at all.**
  - **53.3.1** — the Art. 58 variant-spelling list (below) counts as "identical spelling" for this test.

## Article 54 — Names that do not enter into homonymy
Carves out categories that never trigger the Principle of Homonymy, regardless of identical spelling.

- **54.1** — names excluded from the Code's scope ([Arts. 1.3, 8.3](01-nomenclature.md); cf. [Arts. 1.4, 52.7](#article-52-principle-of-homonymy)).
- **54.2** — unavailable names ([Art. 10.1](04-availability.md)), except as [Art. 20](04-availability.md) provides.
- **54.3** — incorrect spellings, original or subsequent, since an uncorrected incorrect spelling is not itself available ([Arts. 32.4, 32.5, 33.3](07-formation-spelling.md)).
- **54.4** — a name suppressed for homonymy purposes by Commission ruling ([Art. 81.2.1](17-commission.md)).

[Art. 54](https://code.iczn.org/homonymy/article-54-names-that-do-not-enter-into-homonymy/) **A validator that flags every string-identical name pair as a homonym is wrong on all four counts above — unavailable names, uncorrected incorrect spellings, and Commission-suppressed names must be excluded from the comparison set before the Art. 58 spelling-variant test is even applied.** Note also that infrasubspecific names and (per Arts. 55.1/56.1 below) collective-group and family/genus-level ichnotaxon names are explicitly *included* in homonymy at the ranks stated — do not over-generalize an infrasubspecific exclusion the Code does not state generally in Art. 54; the relevant exclusion for infrasubspecific names runs instead through Art. 54.2 (unavailability) via [Art. 1.2/10.1](04-availability.md).

## Article 55 — Family-group names
Applies and extends the Principle of Homonymy at the family-group rank.

- **55.1** — applies to all family-group names, including ichnotaxa. [Art. 55.1](https://code.iczn.org/homonymy/article-55-family-group-names/#art-55-1)
- **55.2** — homonymy from identical type-genus names: see [Art. 39](08-family-group.md).
- **55.3 — homonymy from *similar but non-identical* type-genus names:**
  - **55.3.1** — such a case must go to the Commission for a ruling, unless the senior homonym is a *nomen oblitum*.
  - **55.3.1.1** — if the senior name is a confirmed *nomen oblitum* ([Art. 23.9.2](06-validity-priority.md)), a new family-group *nomen novum* on the same type genus may be coined, choosing a stem that avoids the homonymy ([Arts. 29.1, 29.4, 29.6](08-family-group.md)).
- **55.4** — a *one-letter* difference is sufficient to avoid family-group homonymy (e.g. LARIDAE vs. LARRIDAE are not homonyms). [Art. 55.4](https://code.iczn.org/homonymy/article-55-family-group-names/#art-55-4)
- **55.5** — of two identically-dated family-group homonyms established at different ranks, the one at the *higher* rank is senior ([Art. 24.1](06-validity-priority.md)). [Art. 55.5](https://code.iczn.org/homonymy/article-55-family-group-names/#art-55-5)

## Article 56 — Genus-group names
Applies and extends the Principle of Homonymy at the genus-group rank.

- **56.1** — applies to all genus-group names, including collective groups and genus-level ichnotaxa ([Arts. 1.2, 23.7, 42.2](06-validity-priority.md)). [Art. 56.1](https://code.iczn.org/homonymy/article-56-genus-group-names/#art-56-1)
- **56.2** — a one-letter difference avoids genus-group homonymy (e.g. *Microchaetina* vs. *Microchaetona*). [Art. 56.2](https://code.iczn.org/homonymy/article-56-genus-group-names/#art-56-2)
- **56.3** — of two identically-dated homonyms, one established for a genus and one for a subgenus, the genus-rank name is senior ([Art. 24.1](06-validity-priority.md)). [Art. 56.3](https://code.iczn.org/homonymy/article-56-genus-group-names/#art-56-3)

## Article 57 — Species-group names
Fixes the mechanics of species-group homonymy and the primary/secondary distinction that carries different consequences.

- **57.1** — applies to species-group names identical (or deemed identical under Art. 58) *and* combined, originally or subsequently, with the same generic name ([Art. 53.3](#article-53-definitions-of-homonymy-in-the-family-group-genus-group-and-species-group)); includes collective-group and genus-level ichnotaxon names. [Art. 57.1](https://code.iczn.org/homonymy/article-57-species-group-names/#art-57-1)
- **57.2 — primary homonyms:** identical species-group names established for *different* taxa when *originally* combined with the same generic name. The junior primary homonym is **permanently invalid**, except when: (57.2.1) it survives as a protected *nomen protectum* under [Art. 23.9](06-validity-priority.md); (57.2.2) the Commission conserves it under [Art. 81](17-commission.md); or (57.2.3) it — but not its senior homonym — is on an adopted Part of the List of Available Names in Zoology ([Art. 79.4.3](17-commission.md)). [Art. 57.2](https://code.iczn.org/homonymy/article-57-species-group-names/#art-57-2)
- **57.3 — secondary homonyms:**
  - **57.3.1** — identical species-group names for different taxa *subsequently* brought into the same genus are secondary homonyms; the junior one is invalid, but may be reinstated under conditions in [Art. 59.2–59.4](#article-59-validity-of-secondary-homonyms) below (subject to the [Art. 57.8.1](#57-8-exceptions) exception).
  - **57.3.2** — a special case: one name originally combined with a junior *generic* homonym, the other originally combined with the *nomen novum* that replaced that generic homonym ([Art. 60.1](#article-60-replacement-of-junior-homonyms)) — these are secondary homonyms of each other once the replacement genus is in use.
- **57.4** — a parenthetical subgeneric name interposed between genus and species epithet is irrelevant to the homonymy test; comparison runs on the genus name alone. [Art. 57.4](https://code.iczn.org/homonymy/article-57-species-group-names/#art-57-4)
- **57.5** — homonymy still applies even if one of the two generic combinations uses an incorrect spelling or emendation of the genus name ([Art. 11.9.3.2](04-availability.md)). [Art. 57.5](https://code.iczn.org/homonymy/article-57-species-group-names/#art-57-5)
- **57.6** — outside the Art. 58 variant list, a one-letter difference between species-group names in the same genus is sufficient to avoid homonymy. [Art. 57.6](https://code.iczn.org/homonymy/article-57-species-group-names/#art-57-6)
- **57.7** — of two identically-dated species-group homonyms, one at species rank and one at subspecies rank (or deemed subspecific per [Art. 45.6](10-species-group.md)), the species-rank name is senior ([Art. 24.1](06-validity-priority.md)). [Art. 57.7](https://code.iczn.org/homonymy/article-57-species-group-names/#art-57-7)
- **57.8 Exceptions:**
  - **57.8.1** — species epithets combined (originally or subsequently) with genus names that are themselves homonyms of each other (same spelling, different type genera, [Art. 53.2](#article-53-definitions-of-homonymy-in-the-family-group-genus-group-and-species-group)) are *not* treated as homonyms of each other — the generic-level homonymy does not propagate down. [Art. 57.8.1](https://code.iczn.org/homonymy/article-57-species-group-names/#art-57-8-1)
  - **57.8.2** — cross-refers to [Art. 59.2–59.4](#article-59-validity-of-secondary-homonyms) for reinstatement of junior secondary homonyms.

**Database relevance:** the primary/secondary distinction (57.2 vs. 57.3) is not a static property of a name pair — it depends on whether the *original* combination already put both names in the same genus (primary) or a later transfer did (secondary). This must be computed from the protonym-combination history, not hand-tagged once. It also determines the consequence: primary junior homonyms are (near-)permanently invalid; secondary junior homonyms have a conditional reinstatement path (Art. 59, next).

## Article 58 — Variant spellings of species-group names deemed to be identical
A closed, enumerated list of spelling differences that count as "identical" for homonymy — implementable directly as a validator ruleset, provided the names are of the same derivation/meaning and the taxa are currently in the same genus or collective group.

| # | Variant category | Example pair |
|---|---|---|
| 58.1 | *ae* / *oe* / *e* | caeruleus / coeruleus / ceruleus |
| 58.2 | *ei* / *i* / *y* | cheiropus / chiropus / chyropus |
| 58.3 | *i* / *j* for the same letter | iavanus / javanus; maior / major |
| 58.4 | *u* / *v* for the same letter | neura / nevra; miluina / milvina |
| 58.5 | *c* / *k* | microdon / mikrodon |
| 58.6 | aspirated / unaspirated consonant | oxyrhynchus / oxyrynchus |
| 58.7 | single / double consonant | litoralis / littoralis |
| 58.8 | presence/absence of *c* before *t* | auctumnalis / autumnalis |
| 58.9 | *f* / *ph* | sulfureus / sulphureus |
| 58.10 | *ch* / *c* | chloropterus / cloropterus |
| 58.11 | *th* / *t* | thiara / tiara; clathratus / clatratus |
| 58.12 | differing connecting vowel in compounds | nigricinctus / nigrocinctus |
| 58.13 | semivowel *i* as *y*/*ei*/*ej*/*ij* | guianensis / guyanensis |
| 58.14 | genitive endings *-i*/*-ii*, *-ae*/*-iae*, *-orum*/*-iorum*, *-arum*/*-iarum* | smithi / smithii; patchae / patchiae |
| 58.15 | presence/absence of *-i* before a suffix | timorensis / timoriensis; comstockana / comstockiana |

[Art. 58](https://code.iczn.org/homonymy/article-58-variant-spellings-of-species-group-names-deemed-to-be-identical/) — critically, the list applies **only** when the two names are also "of the same derivation and meaning": `calidus` (warm) and `callidus` (clever), though differing only by the 58.7 single/double-consonant pattern, are *not* deemed identical because their etymology differs (worked example in the Article). A mechanical regex pass over these 15 categories will over-match without an etymology check the Code leaves to taxonomic judgment; flag matches from this table as *candidates* for review, not automatic homonym determinations.

**Recommendation:** Rec. 58A — authors should avoid coining a new species-group name from a personal/geographic name if a name from the same root (even differently formed) is already in use in the same or an allied genus. Advisory guidance for future naming, not a validation rule for existing names.

## Article 59 — Validity of secondary homonyms
Governs when a junior secondary homonym (Art. 57.3) stays invalid versus is reinstated, hinging on current congenericity. *(Confirmed against cache page `homonymy/new-page-2/`, which carries Article 59 despite its placeholder URL slug.)*

- **59.1 — general rule while congeneric:** a junior secondary homonym must be treated as invalid by any author who considers the two species-group taxa congeneric. [Art. 59.1](https://code.iczn.org/homonymy/new-page-2/#art-59-1)
- **59.2 — not replaced, and no longer congeneric:** if the junior secondary homonym was *never* replaced by a substitute name ([Art. 60](#article-60-replacement-of-junior-homonyms)) and the two taxa are no longer considered congeneric, the junior name is **not** to be rejected — even though it once shared a genus with the senior name. [Art. 59.2](https://code.iczn.org/homonymy/new-page-2/#art-59-2)
- **59.3 — replaced before 1961, and no longer congeneric:** a junior secondary homonym that *was* replaced before 1961 is permanently invalid **unless both** (a) the substitute name is not in use, **and** (b) the taxa are no longer considered congeneric — in which case the junior homonym is not to be rejected on the strength of that old replacement. [Art. 59.3](https://code.iczn.org/homonymy/new-page-2/#art-59-3) **Note the exact condition is conjunctive on the substitute name's disuse, not merely on the loss of congenericity** — do not implement this as "no longer congeneric ⇒ automatically reinstated" without also checking whether the substitute name is currently in use.
  - **59.3.1** — if applying 59.3 would itself cause confusion, refer the case to the Commission (using the plenary power if needed, [Art. 81](17-commission.md)) to rule on whichever name best serves stability.
- **59.4 — reinstatement after 1960:** a species-group name rejected *after* 1960 on secondary-homonymy grounds must be reinstated as valid by any author who considers the two taxa no longer congeneric — unless it is invalid for some unrelated reason. [Art. 59.4](https://code.iczn.org/homonymy/new-page-2/#art-59-4)

**Database relevance:** Article 59 makes species-group name validity a function that must be *re-evaluated whenever the current generic classification changes*, not a value fixed at the time a homonymy conflict was first detected. A `status = invalid_homonym` flag persisted on the name row will silently go wrong the moment a subsequent revision splits the two taxa into different genera (59.2/59.4) — status needs to be derivable from `(replaced_before_1961?, substitute_in_use?, currently_congeneric?)`, not stored as a frozen boolean.

## Article 60 — Replacement of junior homonyms
Governs what happens once a junior homonym is confirmed rejected: reuse an existing synonym, or coin a new one.

- **60.1** — a junior homonym ([Art. 53](#article-53-definitions-of-homonymy-in-the-family-group-genus-group-and-species-group)) must be rejected and replaced, either by (a) an available and potentially valid synonym ([Art. 23.3.5](06-validity-priority.md)) or (b) a new substitute name (60.3) if no such synonym exists. Cross-refs: unused senior homonyms ([Art. 23.9](06-validity-priority.md)); family-group homonym replacement ([Arts. 39](08-family-group.md), 55.3); secondary species-group homonyms ([Art. 59](#article-59-validity-of-secondary-homonyms) above). [Art. 60.1](https://code.iczn.org/homonymy/article-60-replacement-of-junior-homonyms/#art-60-1)
- **60.2 — synonym exists:** the oldest available, potentially-valid synonym of the rejected junior homonym becomes the valid name, under **its own** authorship and date (not the rejected homonym's). [Art. 60.2](https://code.iczn.org/homonymy/article-60-replacement-of-junior-homonyms/#art-60-2)
  - **60.2.1** — that promoted synonym remains valid *only for as long as* it is still regarded as a synonym of the rejected homonym — if taxonomic opinion later separates them, this fallback lapses.
- **60.3 — no synonym exists:** a *new substitute name* (a **nomen novum**) must be published, with its own author and date; this new name then competes for priority against any synonym that might later be recognized. **The nomen novum takes over the name-bearing type of the name it replaces** (per Rec. 60A's objective-replacement guidance and the general type-fixation mechanism) — it does not get a fresh type. [Art. 60.3](https://code.iczn.org/homonymy/article-60-replacement-of-junior-homonyms/#art-60-3)

**Recommendation:** Rec. 60A — unless the rejected homonym's name-bearing type is taxonomically inadequate (e.g. per [Art. 75.5](13-typification.md), or a poorly-defined type species at genus rank), authors are advised to use that same type when coining the *nomen novum*, making it an *objective* replacement ([Arts. 67.8, 72.7](15-genus-group-types.md)). Advisory, not mandatory — a *subjective* replacement (new type) is permitted but not recommended.

**Database relevance:** a *nomen novum* under Art. 60.3 is not an independent name row — it must be modelled with an explicit relationship to the replaced homonym: same name-bearing type (when objective, per Rec. 60A), its own author/date/availability record, and a `replaces` link back to the rejected homonym. Treating the *nomen novum* as unrelated to the name it replaces loses the type-sharing fact required to trace synonymy. See [`references/13-typification.md`](13-typification.md) for name-bearing type mechanics and [`references/data-modeling.md`](data-modeling.md) for the protonym/replacement-name relationship pattern, and [`references/06-validity-priority.md`](06-validity-priority.md) for how a *nomen novum*'s own date enters priority competition per 60.3.

**Common errors:** (1) coining a substitute name when an available senior synonym already exists — 60.1 requires exhausting 60.2 before 60.3; (2) treating the *nomen novum*'s type as newly designated rather than inherited from the replaced name when the replacement is objective; (3) applying the Art. 60 replacement logic to a *secondary* species-group homonym without first checking the Art. 59 conditions under which it need not be replaced at all.
