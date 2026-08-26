# Chapter 7 — Formation and treatment of names (Articles 25–34)

Source: https://code.iczn.org/formation-and-treatment-of-names/ · 4th edition 1999

This chapter is the mechanical layer of the Code: given an available name, how must it be *spelled, capitalized, and inflected*, and which of two or more spellings encountered in the literature is the one that counts. A reader lands here to resolve a spelling discrepancy, to determine whether a variant is a synonym-generating emendation or a non-name typo, to fix the gender ending of an adjectival epithet after a generic transfer, or to build the validation rules for a names database. It does not decide availability (Chapter 4, `references/04-availability.md`) or priority between competing names (Chapter 6, `references/06-validity-priority.md`) — only the correct *form* of a name whose availability is already settled.

## Article 25 — Formation and treatment of names
Umbrella article: every scientific name must be formed and treated per Art. 11 and Arts. 26–34; Appendix B carries non-mandatory general recommendations on the same subject.

- **25** — No independent rule; it is a pointer to Arts. 26–34 (below) and to Art. 11. [Art. 25](https://code.iczn.org/formation-and-treatment-of-names/article-25-formation-and-treatment-of-names/)

**Recommendations:** Rec. 25A (spell a name in full on first use in a work, abbreviate unambiguously thereafter with a full stop); Rec. 25B (state the derivation of a new name); Rec. 25C (choose new names with future users in mind: appropriate, compact, pronounceable, non-offensive). All advisory, not requirements for availability.

## Article 26 — Assumption of Greek or Latin in scientific names
Governs how a name's *linguistic origin* is determined, which feeds directly into Arts. 27–32.

- **26** — If a name, or the final component of a compound name (per Art. 31.1), is spelled identically to a Greek or Latin word, the Code treats it as a word of that language for all grammatical purposes (gender, declension, correction rules) — unless the describing author explicitly states otherwise when publishing it. [Art. 26](https://code.iczn.org/formation-and-treatment-of-names/article-26-assumption-of-greek-or-latin-in-scientific-names/)

**Database relevance:** the "is this name Latin/Greek?" flag cannot be inferred purely from spelling coincidence — it must record the author's explicit disclaimer, if any, from the original publication. Absent a disclaimer, coincidence of spelling controls.

## Article 27 — Diacritic and other marks
Fixes the permitted character set of a zoological name.

- **27** — A scientific name must contain no diacritic mark (e.g. ñ, ø, ü), no apostrophe, and no ligature (æ, œ). A hyphen is barred except in the single case specified at Art. 32.5.2.4.3 (a name whose first element is a Latin letter denoting descriptively a character of the taxon, e.g. a "c"-shaped mark). [Art. 27](https://code.iczn.org/formation-and-treatment-of-names/article-27-diacritic-and-other-marks/)

This Article states the *prohibition*; Art. 32.5.2 (below, under Art. 32) states the *correction mechanics* when a published name violates it — i.e. Art. 27 says what is forbidden, Art. 32.5.2 says what the forbidden character is replaced with and which Article (32, spelling correction, not 27 itself) governs the resulting spelling's status. Per Art. 32.5.2.1: a diacritic/other mark is simply deleted, except that in a name published before 1985 and based on a German word, an umlaut is deleted from its vowel and an "e" is inserted after that vowel (ä→ae, ö→oe, ü→ue); a name published in or after 1985 with a German umlaut is corrected by plain deletion, not e-insertion. An apostrophe or hyphen joining a compound species-group name is corrected by removing the mark and closing up the words (Art. 32.5.2.3), subject to the Art. 32.5.2.4 sub-rules for abbreviation-plus-word compounds.

## Article 28 — Initial letters
Mechanically checkable capitalisation rule.

- **28** — A family-group name, a genus-group name, or the name of any taxon above the family group must always begin with an upper-case letter; a species-group name must always begin with a lower-case letter — regardless of how the author originally capitalized it. [Art. 28](https://code.iczn.org/formation-and-treatment-of-names/article-28-initial-letters/)

**Recommendations:** Rec. 28A — avoid opening a sentence with a species-group name, to prevent the appearance of an upper-case initial. Advisory only; the mandatory floor is Art. 28 itself, enforced regardless of sentence position.

**Machine-checkable:** trivially — regex on the first character against the name's rank.

## Article 29 — Family-group names
Governs how a family-group name (superfamily to subtribe) is built from its type genus.

- **29.1** — A family-group name = stem of the type genus's name (Art. 29.3) + rank suffix (29.2), or in some cases the type genus's entire name (see 29.6) + suffix. [Art. 29.1](https://code.iczn.org/formation-and-treatment-of-names/article-29-family-group-names/#art-29-1)
- **29.2** — Mandatory rank suffixes: superfamily `-OIDEA`, family `-IDAE`, subfamily `-INAE`, tribe `-INI`, subtribe `-INA`. These five suffixes are reserved to exactly these ranks; no other family-group rank suffix is regulated by the Code. [Art. 29.2](https://code.iczn.org/formation-and-treatment-of-names/article-29-family-group-names/#art-29-2)
  - **29.2.1** — A genus- or species-group name that happens to end in one of these same letter sequences (e.g. a genus ending in `-oidea`) is not a family-group name and is unaffected by Art. 29.
- **29.3** — Stem-determination rule, in order:
  - **29.3.1** — If the generic name is, or ends in, a Greek/Latin word or a Greek/Latin suffix, the stem = the genitive singular of that word with the case ending deleted (e.g. *Culex*, genitive *Culicis* → stem *Culic-* → CULICIDAE).
    - **29.3.1.1** — If the resulting stem ends in `-id`, those letters may be elided before the suffix is added, *unless* the un-elided form is already the prevailing-usage spelling, in which case the prevailing form is kept regardless of originality.
  - **29.3.2** — If the generic name is a Greek word latinized with a changed ending, the stem is taken from the *latinized* form, not the original Greek root.
  - **29.3.3** — If the generic name is neither Greek nor Latin (or is an arbitrary letter string), the stem is whatever the family-group-name-establishing author adopted: the whole generic name, the whole name with the ending elided, or the whole name plus linking letters for euphony.
- **29.4** — For a family-group name coined after 1999 from a Greek/Latin-origin genus but *not* following the 29.3.1/29.3.2 grammar, the as-published spelling is nonetheless the correct original spelling provided it (29.4.1) has a correctly formed rank suffix and (29.4.2) treats the stem as if the genus name were an arbitrary letter string (29.3.3). This is a narrow post-1999 safe-harbor, not a general license to skip the genitive-stem rule.
- **29.5** — If a family-group name's stem was **not** properly derived under 29.3, but the resulting spelling is in prevailing usage, that spelling is preserved regardless of originality or grammatical correctness. [Art. 29.5](https://code.iczn.org/formation-and-treatment-of-names/article-29-family-group-names/#art-29-5)
- **29.6** — A family-group-name-establishing author must choose a stem that avoids homonymy with any existing family-group name; Rec. 29A (below) is the standard technique.

**Recommendations:** Rec. 29A — to dodge homonymy from two type genera sharing a stem, use the *entire* generic name as the family-group stem rather than the abbreviated genitive stem. Advisory technique, not a requirement — Art. 29.6 is the mandatory obligation to avoid homonymy; Rec. 29A only suggests one way to do it.

**Database relevance:** store (a) the type genus, (b) its genitive stem, (c) the applied rank suffix, and (d) whether the name's stem is a 29.3-derived stem, a 29.4 safe-harbor spelling, or a 29.5 prevailing-usage exception — these have different correction obligations if the family-group name is later reassessed.

**Machine-checkable:** suffix-to-rank mapping (29.2) is a pure lookup. Stem derivation (29.3) requires a Latin/Greek genitive dictionary and is not mechanically derivable from the nominative form alone without such a lookup table.

## Article 30 — Gender of genus-group names
Determines which Latin gender (masculine/feminine/neuter) a genus-group name carries, which in turn drives the mandatory ending changes of Art. 34.2 whenever the genus is combined with an adjectival species-group name.

- **30.1** — For a name that is, or ends in, a Latin or Greek word (subject to the 30.1.4 exceptions):
  - **30.1.1** — A Latin-origin name takes the gender given in standard Latin dictionaries; a compound Latin name takes the gender of its final component.
  - **30.1.2** — A Greek word transliterated into Latin unchanged takes the gender given in standard Greek dictionaries.
  - **30.1.3** — A Greek word latinized with a changed ending, or bearing a Latin/latinized suffix, takes the gender normally associated with that ending/suffix (e.g. endings in `-us` from Greek `-os`/`-e`/`-a`/`-on` are masculine).
  - **30.1.4 (default/exception ladder)**:
    - **30.1.4.1** — If the author states the name is *not* to be treated as Latin/Greek (Art. 26), gender is instead determined as for an arbitrary combination of letters (Art. 30.2.2 onward).
    - **30.1.4.2** — A name of common/variable Latin gender is masculine by default unless the author stated or treated it as feminine (via combination with an adjectival epithet) when establishing it.
    - **30.1.4.3** — A compound name ending in `-ops` is always masculine, regardless of derivation or authorial treatment.
    - **30.1.4.4** — A compound name ending in `-ites`, `-oides`, `-ides`, `-odes`, or `-istes` is masculine by default unless the author stated or demonstrated another gender at establishment.
    - **30.1.4.5** — A Latin-origin name whose ending was altered takes the gender fitting the new ending; if the new ending indicates no particular gender, it defaults to masculine.
- **30.2** — For a name that is *not* Latin or Greek in origin:
  - **30.2.1** — If it exactly reproduces a gendered noun of a modern European language, it takes that noun's gender.
  - **30.2.2** — Otherwise, it takes the gender the author expressly specified at establishment.
  - **30.2.3** — If unspecified, gender is inferred from the adjectival species-group names originally combined with it (Art. 67.2).
  - **30.2.4** — If neither specified nor inferable, the default is masculine, *except* names ending in `-a` (feminine) and names ending in `-um`, `-on`, or `-u` (neuter). [Art. 30.2.4](https://code.iczn.org/formation-and-treatment-of-names/article-30-gender-of-genus-group-names/#art-30-2-4)

**Recommendations:** Rec. 30A (state gender and derivation explicitly when coining a genus-group name); Rec. 30B (when the name is not Latin/Greek, choose an ending whose gender is self-evident). Both advisory; the binding fallback ladder is 30.2.1–30.2.4 regardless of whether an author complied.

**Database relevance:** gender is a *property of the genus-group name*, not of any one combination — store it once per genus-group name (with its determination path: 30.1.x classical rule, or 30.2.x default/specified/inferred) and derive every species epithet's expected ending from it, rather than storing gender per binomen.

**Machine-checkable:** the 30.1.4.2–30.1.4.5 ending-based defaults and the 30.2.4 fallback are pure suffix lookups. Classical gender under 30.1.1–30.1.3 requires a Latin/Greek lexicon (an external dictionary lookup), not derivable from the string alone. Whether an author "expressly stated" or "treated" a gender (30.1.4.x, 30.2.2, 30.2.3) requires reading the original publication — a human/literature judgement.

## Article 31 — Species-group names
Governs two independent things: how a personal-name-derived epithet is inflected (31.1), and whether an epithet must change its ending when the genus changes (31.2). These interact but must not be conflated.

- **31.1** — A species-group name built from a personal name may be a genitive noun, a noun in apposition (nominative), or an adjective/participle (cf. Art. 11.9.1).
  - **31.1.1** — A genitive formed from a Latin, or latinized, personal name follows ordinary Latin declension (e.g. *Victor* → *victoris*; *Cuvier* latinized to *Cuvierius* → *cuvierii*).
  - **31.1.2** — A genitive formed directly from an unlatinized modern personal name is built by adding to the name's stem: `-i` (one man), `-orum` (men, or men+women together), `-ae` (one woman), `-arum` (women). The stem itself is whatever the original author took it to be. [Art. 31.1.2](https://code.iczn.org/formation-and-treatment-of-names/article-31-species-group-names/#art-31-1-2)
  - **31.1.3** — Whichever genitive form (31.1.1 single-i or 31.1.2 double-i, etc.) was actually published is the original spelling and is preserved as such if available — the two rules can legitimately produce different-looking, equally correct genitives from the same surname (e.g. *cuvierii* vs. *cuvieri*), and they are treated as distinct correct original spellings, not as variants of one another.
- **31.2 — Agreement in gender.** A species-group name that is, or ends in, a Latin/latinized **adjective or participle** in the nominative singular must always agree in gender with whatever genus-group name it is currently combined with — this obligation travels with the name through every generic transfer, not just at original publication. [Art. 31.2](https://code.iczn.org/formation-and-treatment-of-names/article-31-species-group-names/#art-31-2)
  - **31.2.1** — A species-group name that is a **noun (or noun phrase) in apposition** is exempt: it need not, and per Art. 34.2.1 must not, be changed to agree with the genus's gender, regardless of subsequent generic reassignment.
  - **31.2.2** — Where the original author left it ambiguous whether the epithet was intended as a noun or an adjective, and usage evidence does not resolve it, the Code's tie-break is to treat it as a noun in apposition — i.e. the ending is frozen, not gender-agreeing.
  - **31.2.3** — A species-group name (or the final component of a compound one) that is not a Latin/latinized word at all (Arts. 11.2, 26) is treated as grammatically indeclinable: it never changes ending on generic transfer, regardless of the genus's gender.

**This is the crux distinction the skill must state without hedging: the noun/adjective status of an epithet is a fact about Latin grammar and the original author's intent, not something derivable from the spelling of the ending alone.** Endings such as `-fer`, `-ger`, `-us`, `-a`, `-um` are ambiguous between adjectival and appositional-noun readings (see the *phobifer* example under 31.2.2); resolving the case requires either an explicit authorial statement, decisive usage evidence, or — failing both — the mandatory noun-in-apposition default of 31.2.2. A database or a validator cannot correctly compute "does this epithet need re-gendering after generic transfer?" from string pattern-matching on the ending; it needs a stored grammatical-category flag per name, sourced from taxonomic literature/expert review, not inferred.

Art. 34.2 (Chapter 7, below) is the corollary: agreement is not merely descriptive, it is a *mandatory change* — the ending **must** be corrected on transfer to a genus of different gender if, and only if, 31.2 classifies the epithet as adjectival/participial; nouns in apposition are frozen by 34.2.1.

**Recommendations:** Rec. 31A — avoid forming a new personal-name species epithet as a noun in apposition sharing the exact spelling of the genus's authorship citation, to prevent visual confusion (e.g. avoid a combination that reads like "*Genus* Person" rather than a binomen).

**Database relevance:** store, per species-group name, a `grammatical_category` field (`genitive-noun` | `noun-in-apposition` | `adjective/participle` | `indeclinable-non-Latin`) sourced from the original description and subsequent taxonomic opinion — this field, not the ending string, is what a UI or validator must consult before proposing a re-gendered spelling after a generic transfer.

**Machine-checkable:** given the grammatical-category flag and the genus's stored gender (Art. 30), the *correct ending* for an adjectival epithet is computable. Determining the grammatical-category flag itself in the first place is not machine-checkable from the string — it requires the human/literature judgement described above.

## Article 32 — Original spellings
Defines what "the original spelling" means and the narrow conditions under which it may be overridden as incorrect.

- **32.1** — The original spelling is whatever spelling was actually used in the work that established the name.
- **32.2** — The original spelling is the "correct original spelling" by default, unless 32.5 requires correction.
  - **32.2.1** — If the establishing work itself uses more than one spelling, the correct original spelling is whichever the First Reviser selected (Art. 24.2.3; or an original co-author acting as First Reviser, Art. 24.2.4).
  - **32.2.2** — A justified emendation (Art. 33.2.2, below) is treated as if it were the correct original spelling, and it keeps the *original* publication's authorship and date (Art. 19.2) — it does not get the emender's name.
- **32.3** — Once fixed, the correct original spelling must be preserved unaltered except where Art. 34 mandates a suffix or gender-ending change.
- **32.4** — An "incorrect original spelling" (one that Art. 32.5 requires correcting) has no independent availability: it cannot be homonymous with anything and cannot serve as a replacement/substitute name.
- **32.5 — the inadvertent-error test.** A spelling must be corrected only where the case falls into one of these enumerated categories — this is an exhaustive list, not open-ended editorial discretion:
  - **32.5.1** — Correction applies only where the *original publication itself* (no external evidence) shows clear proof of an inadvertent slip — a lapsus calami, or a copyist's/printer's error. Incorrect transliteration, incorrect latinization, or a merely inapt connecting vowel are explicitly **excluded** — those are not inadvertent errors and the as-published spelling stands.
    - **32.5.1.1** — A same-volume publisher's/author's corrigendum (or an inserted errata slip) counts as clear internal evidence of inadvertent error.
  - **32.5.2** — A name published with a diacritic, ligature, apostrophe, or hyphen, or a species-group name wrongly split into abbreviation-containing separate words, must be corrected per the sub-rules 32.5.2.1–32.5.2.7 (diacritic deletion / German umlaut-to-`e` insertion pre-1985 as under Art. 27 above; joining of separated compound words; removal of apostrophe/hyphen except the Art. 32.5.2.4.3 descriptive-letter hyphen; spelling out honorific/place abbreviations in full at 32.5.2.4.1, dropping titles at 32.5.2.4.2; case correction at 32.5.2.5 mirroring Art. 28; spelling out numerals at 32.5.2.6; and grammatical-case correction to the nominative singular for names distorted by Latin sentence grammar at 32.5.2.7).
  - **32.5.3** — A family-group name is an incorrect original spelling requiring correction if it has a misformed rank suffix (32.5.3.1), derives from an unjustified emendation of the type genus's name (32.5.3.2, unless that emendation itself became a substitute name), derives from an incorrect subsequent spelling of the type genus's name (32.5.3.3), or derives from a type-genus spelling that the First Reviser did not select among multiple original spellings (32.5.3.4).

**The critical distinction:** 32.5.1 requires evidence *internal to the original work* of an unintentional slip. A First Reviser's opinion that a spelling is "probably a mistake," without such internal evidence, does not meet the 32.5.1 threshold — the as-published spelling then stands as the correct original spelling under 32.2, however implausible it looks in hindsight.

**Database relevance:** record, per name, whether its spelling is (a) the correct original spelling unmodified, (b) a correct original spelling as fixed by a First Reviser among original variants (32.2.1), or (c) a corrected incorrect-original-spelling under a specific 32.5.x sub-clause — each has a different evidentiary basis that a later reviewer will need to re-examine.

**Machine-checkable:** the *character-set* triggers of 32.5.2 (diacritics, ligatures, apostrophes, disallowed hyphens, wrong-case initial) are fully mechanical — a validator can flag the violation and even propose the mechanical replacement (umlaut/date rule, case flip, mark deletion). The *inadvertent-error* determination of 32.5.1 is not mechanical: it requires reading the original publication for internal evidence and cannot be inferred from the spelling alone.

## Article 33 — Subsequent spellings
The trichotomy that decides authorship and nomenclatural status whenever a name's spelling changes *after* original publication. Confusing the three categories is one of the most consequential errors a taxonomic database can make, because each carries a different author/date and a different homonymy status.

- **33.1** — Any subsequent spelling different from the original one is exactly one of: an emendation (33.2), an incorrect subsequent spelling (33.3), or a mandatory change (Art. 34).
- **33.2 — Emendation** = a demonstrably *intentional* respelling that is not a mandatory change.
  - **33.2.1** — "Demonstrably intentional" requires one of: an explicit statement of intent in the work or its corrigenda; both spellings cited with the new one substituted for the old; or a consistent pattern applied to two or more names in the same work. Silent, unexplained respelling does **not** qualify as demonstrably intentional (see 33.5 below).
  - **33.2.2 — Justified emendation**: an intentional correction that fixes an incorrect original spelling per Art. 32.5. **Authorship/date consequence: it takes the *original* author and date** (Art. 19.2) — the emender receives no nomenclatural credit; it is legally the same name, correctly spelled.
  - **33.2.3 — Unjustified emendation**: any *other* intentional respelling (i.e. one not correcting a genuine 32.5 defect). **Authorship/date consequence: it is a new, separately available name with its own author and date, and it is automatically a junior objective synonym of the name in its original spelling** — it can be a homonym of something else, and it can itself be pressed into service as a replacement/substitute name. [Art. 33.2.3](https://code.iczn.org/formation-and-treatment-of-names/article-33-subsequent-spellings/#art-33-2-3)
    - **33.2.3.1** — Exception: if an unjustified emendation is itself in prevailing usage and is (mis)attributed in that usage to the *original* author/date, it is deemed a justified emendation after all, and the *original* spelling+authorship is what is maintained — prevailing usage overrides the mechanical 33.2.3 default.
- **33.3 — Incorrect subsequent spelling**: any subsequent-spelling difference from the correct original spelling that is *neither* a mandatory change nor a (justified or unjustified) emendation — i.e. an unintentional slip made after original publication. **Consequence: it is not an available name at all** — no author, no date, no homonymy status, cannot be used as a substitute name. It is, in effect, a typo with no nomenclatural existence of its own.
  - **33.3.1** — Exception mirroring 33.2.3.1: if an incorrect subsequent spelling is in prevailing usage and is attributed to the original publication, that spelling+attribution is preserved and is deemed the correct original spelling going forward (see the *brucei*/*brucii* example on site).
- **33.4** — A special, narrow instance of 33.3: switching a personal-name genitive between `-i`/`-ii`, `-ae`/`-iae`, `-orum`/`-iorum`, or `-arum`/`-iarum` relative to the correct original spelling is **always** deemed an incorrect subsequent spelling — even where the change was demonstrably deliberate. This overrides the general 33.2.1 "demonstrable intent ⇒ emendation" test specifically for this class of ending swap. [Art. 33.4](https://code.iczn.org/formation-and-treatment-of-names/article-33-subsequent-spellings/#art-33-4)
- **33.5 — Default rule for doubt**: whenever it is unclear whether a differing subsequent spelling is an emendation or an incorrect subsequent spelling, the Code requires treating it as an **incorrect subsequent spelling** (i.e. unavailable) — doubt resolves against emendation status, not toward it.

**Summary table (authorship/status consequence is the operative distinction):**

| Category | Article | Intentional? | Available as its own name? | Author/date | Enters homonymy / usable as substitute name? |
|---|---|---|---|---|---|
| Justified emendation | 33.2.2 | Yes, correcting a genuine 32.5 defect | No — same name, corrected | Original author/date | Same as original name |
| Unjustified emendation | 33.2.3 | Yes, not correcting a genuine defect | Yes — separate available name | Emender's own author/date | Yes — junior objective synonym; can be a homonym or substitute name |
| Incorrect subsequent spelling | 33.3 | No (or unintentional/doubtful, 33.5) | No | None | No |

**Database relevance:** never silently normalise or merge spelling variants of the same name. Store every encountered string verbatim with a `spelling_status` field (`correct-original` / `justified-emendation` / `unjustified-emendation` / `incorrect-subsequent`), because literature citations must resolve to the string actually printed even when that string is nomenclaturally a non-name (33.3) — a search index must still find it. See `references/data-modeling.md` for the schema pattern (name-string table separate from nomenclatural-act table).

**Machine-checkable:** none of 33.2/33.3/33.4/33.5 classification is mechanical in the general case — it requires reading the publishing work for a statement of intent (33.2.1) or establishing prevailing usage (33.2.3.1, 33.3.1), both literature-research tasks. The one exception is 33.4: given two candidate genitive endings and knowledge that both derive from the same personal name, the `-i`/`-ii` (etc.) swap-detection itself is a mechanical string check, though it only fires once a human has already confirmed the two strings are meant to be the same underlying name.

## Article 34 — Mandatory changes in spelling consequent upon changes in rank or combination
The two cases where a spelling change is **required**, not optional, and does not disturb authorship/date.

- **34.1 — Family-group names.** When a family-group taxon's rank changes (e.g. subfamily raised to family), its name's suffix must change to match the new rank's Art. 29.2 suffix; author and date are unaffected (cf. Arts. 23.3.1, 29.2, 50.3.1). [Art. 34.1](https://code.iczn.org/formation-and-treatment-of-names/article-34-mandatory-changes-in-spelling-consequent-upon-changes-in-rank-or-combination/#art-34-1)
- **34.2 — Species-group names.** When a Latin/latinized adjectival or participial species-group name (per Art. 31.2) is combined with a genus of different gender than its current ending expresses, the ending **must** be changed to the grammatically correct gender ending for the new genus; author and date are unaffected (cf. Art. 50.3.2). [Art. 34.2](https://code.iczn.org/formation-and-treatment-of-names/article-34-mandatory-changes-in-spelling-consequent-upon-changes-in-rank-or-combination/#art-34-2)
  - **34.2.1** — Converse rule: if the species-group name is a noun in apposition (Art. 31.2.1), its ending must **not** be changed on generic transfer, regardless of the new genus's gender.

**Database relevance:** 34.1/34.2 changes are *display-form* recomputations, not new nomenclatural acts — the stored author/date of the name must not change when the suffix/ending is mechanically updated for a rank or combination change; only the currently-valid combination's rendered string changes.

**Machine-checkable:** fully mechanical *given* the two prerequisite facts established under Arts. 29–31 by human/literature judgement: (a) the family-group name's target rank (34.1, then a suffix lookup) and (b) the species epithet's grammatical category plus the genus's gender (34.2, then an ending lookup). The lookups themselves are trivial; supplying their inputs is not.

## Machine-checkable rules — summary for `scripts/validate_name.py`

**Fully deterministic (character/string-level; no external judgement needed given the name's rank and declared category):**
- Character set: no diacritics, ligatures, apostrophes, or hyphens outside the single Art. 32.5.2.4.3 exception (Art. 27, Art. 32.5.2).
- Initial letter case vs. rank (Art. 28).
- Family-group suffix vs. declared rank, and validity of the suffix-to-rank mapping itself (Art. 29.2).
- Given a stored genus gender and a stored epithet grammatical-category flag, whether the rendered ending is the grammatically correct one (Arts. 30, 31.2, 34) — a pure suffix lookup.
- The `-i`/`-ii`, `-ae`/`-iae`, `-orum`/`-iorum`, `-arum`/`-iarum` swap-detection between two strings already known to represent the same base name (Art. 33.4).
- Genitive-ending well-formedness against the 31.1.2 morphology (`-i`, `-orum`, `-ae`, `-arum`) once the personal name's stem is supplied.

**Requires human/literature/morphological judgement (not derivable from the string alone):**
- Whether a name is "of Greek or Latin origin" absent an authorial disclaimer (Art. 26) — a lexical-origin call.
- Classical gender under Art. 30.1.1–30.1.3 — needs a Latin/Greek dictionary lookup, and whether the author "expressly stated or treated" a gender under 30.1.4.x/30.2.2/30.2.3.
- The grammatical category of a species epithet — genitive noun, noun in apposition, or adjective/participle (Art. 31.1/31.2) — this is the single most consequential judgement call in the chapter and cannot be inferred from the ending's letters.
- Whether a spelling discrepancy in the original work reflects "clear evidence of an inadvertent error" (Art. 32.5.1) vs. a defensible original choice — requires reading the original publication, not just comparing strings.
- Determining prevailing usage for the Art. 29.5, 33.2.3.1, and 33.3.1 exceptions — a literature-survey task.
- Distinguishing justified emendation / unjustified emendation / incorrect subsequent spelling (Art. 33.2–33.3) in the first instance — requires establishing authorial intent from the publishing work; only once that classification exists do the mechanical consequences (author/date, homonymy eligibility) follow automatically.

A validator can therefore *flag* every character-set and case/suffix/ending violation automatically, and can *propagate* a gender/category decision once a human has recorded it, but it cannot *originate* a gender, grammatical-category, or emendation-class determination from the bare name string.
