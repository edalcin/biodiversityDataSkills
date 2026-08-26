# Chapter 14 — Types in the Family Group (Articles 62–65)

Source: https://code.iczn.org/types-in-the-family-group/ · 4th edition 1999

This short chapter governs the type genus: how it is chosen when a family-group name is established, and how disputes over its identity get resolved. Land here when validating or recording the name-bearing type of a superfamily, family, subfamily, tribe, or any family-group rank.

## Article 62 — Application
The chapter's rules apply uniformly to every family-group rank.

- **62.1** — Superfamily, family, subfamily, tribe, subtribe, and any other rank below superfamily and above genus are all governed identically by this chapter (Art. 35.1, `references/08-family-group.md`). [Art. 62](https://code.iczn.org/types-in-the-family-group/article-62-application/)

## Article 63 — Name-bearing types
The name-bearing type of a family-group taxon is a nominal genus, the "type genus," and the family-group name's stem is built from it.

- **63.1** — The name-bearing type of a nominal family-group taxon is a nominal genus, called the type genus; the family-group name is formed on that genus's name (Art. 29, `references/07-formation-spelling.md`; see also Arts. 11.7, 35, 39, 40). [Art. 63](https://code.iczn.org/types-in-the-family-group/article-63-name-bearing-types/#art-63)
  - **63.1 (coordinate taxa)** — Coordinate family-group taxa (e.g. a family and the subfamily formed on the same genus stem) share the same type genus by construction (Arts. 36, 37, 61.2 — `references/13-typification.md`). [Art. 63.1](https://code.iczn.org/types-in-the-family-group/article-63-name-bearing-types/#art-63-1)

## Article 64 — Choice of type genus
An author establishing a new family-group taxon picks the type genus freely from among the included genera.

- **64.1** — When establishing a new family-group taxon, the author may choose as type genus any included nominal genus whose name they regard as valid (Art. 11.7.1) — it need not be the oldest-named genus in the group. The chosen genus determines the stem of the new family-group name (Art. 29.1). [Art. 64](https://code.iczn.org/types-in-the-family-group/article-64-choice-of-type-genus/#art-64)

**Recommendations:** Rec. 64A (advisory) — prefer a type genus that is well known and representative of the taxon, not merely convenient.

## Article 65 — Identification of the type genus
Correct identification of the type genus is presumed; genuine disputes route through fixed procedures, sometimes to the Commission.

- **65.1** — Absent clear contrary evidence, assume the establishing author correctly identified the type genus. [Art. 65.1](https://code.iczn.org/types-in-the-family-group/article-65-identification-of-the-type-genus/#art-65-1)
- **65.2** — When stability/universality is threatened or confusion would result, three distinct problem cases are resolved differently:
  - **65.2.1** — Type genus was *misidentified* (i.e., interpreted in a sense other than that defined by its own type species) when the family name was established → refer to the Commission for a ruling. No self-help fix available here.
  - **65.2.2** — An *overlooked* type-species fixation for the type genus (or an overlooked name-bearing type for that type species) surfaces later → refer to the Commission (see Art. 70.2, `references/15-genus-group-types.md`).
  - **65.2.3** — The type genus was, when established, based on a type species that was *itself misidentified* → the author may fix a replacement type species under Art. 70.3 (`references/15-genus-group-types.md`); only if that cannot resolve the threat does the case go to the Commission.

**Database relevance:** Record the type genus per family-group name as a direct reference, and treat "correctly identified" as the default state (flag = true) unless a specific 65.2.x correction or Commission ruling is on file. Coordinate family-group taxa should share one type-genus foreign key, not duplicate copies, so the constraint in Art. 63.1 is structural rather than merely asserted.

**Common errors:** Assuming a family-group name can freely swap its type genus by ordinary revision — it cannot; only 65.2.1–65.2.3 provide any route, and 65.2.1/65.2.2 require Commission action, not unilateral author decision.
