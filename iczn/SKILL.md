---
name: iczn
description: >
  Expert knowledge of the International Code of Zoological Nomenclature (ICZN,
  4th edition 1999, with Declarations 44-47 and the 2012 electronic-publication
  amendment) for zoological taxonomists and for anyone structuring taxonomic data.
  Decides whether a name is available, which of two competing names is valid,
  whether a type designation is effective, how authorship and parentheses are
  cited, and how to model names, taxa and nomenclatural acts in a database.
  Use this skill whenever the user mentions "ICZN", "zoological nomenclature",
  "Code of Zoological Nomenclature", an Article number of the Code, "available
  name", "valid name", "senior/junior synonym", "homonym", "nomen nudum",
  "nomen oblitum", "nomen protectum", "nomen novum", "holotype", "syntype",
  "lectotype", "neotype", "paratype", "type species", "type genus", "type
  locality", "priority", "typification", "emendation", "new combination",
  "ZooBank", "LSID", "Bulletin of Zoological Nomenclature", or the ICZN
  Commission -- and also whenever they are describing a new animal species,
  reviewing a taxonomic manuscript, cleaning or validating animal name strings,
  resolving a synonymy or a spelling variant, deciding what belongs in
  scientificName / scientificNameAuthorship / nomenclaturalStatus /
  taxonomicStatus / typeStatus, or designing a database or checklist that holds
  animal names, even if they never say "ICZN".
license: MIT
compatibility: Python 3.9+ (standard library only)
metadata:
  author: biodiversityDataSkills
  repository: https://github.com/edalcin/biodiversityDataSkills
---

# International Code of Zoological Nomenclature

Working knowledge of the [Code](https://code.iczn.org/) — 4th edition, adopted by the
International Union of Biological Sciences, in force since 1 January 2000, as amended.

**What this skill is.** An operational synthesis of all 90 Articles, the Glossary and
the Appendices, written rule by rule with the citation attached, plus the data-modelling
consequences that follow from them. The Code's text is copyrighted (© International
Trust for Zoological Nomenclature 1999) and is not reproduced here; the rules are
restated in our own words and every one of them points at the Article it comes from.

**Its standing.** None. Art. 87 gives equal force to the English and French texts of
the Code and to no other version, so a synthesis — this one included — settles nothing
in a dispute. Cite the Article, and when the exact wording decides the case, fetch it:

```bash
python scripts/fetch_article.py 23.9        # the letter of the law, from the source
```

**Answer in the user's language.** The rules are stated here in English because the
Code's vocabulary is English and Latin, and translating *available name* or *nomen
oblitum* into a database field is how those fields end up wrong. Keep the technical
terms as they are; write the surrounding explanation in whatever language the user
used. `references/glossary.md` carries a pt-BR column for recognition.

---

## Answering a nomenclatural question

Almost every real question is one of six. Find it here, then open the file named — do
not try to answer from memory, because the traps in this domain are all in the
sub-articles.

### 1. "Is this name available?"
Availability is the threshold question: an unavailable name is not a name at all, and
nothing else about it matters. It is a permanent property of the name, fixed at
publication and untouched by anyone's later taxonomic opinion (Art. 10).

→ **`references/04-availability.md`** — opens with the checklist, in the order a
practitioner applies it. Arts. 10–20.
Then, depending on where the checklist stops:
- was the work published at all? → `references/03-publication.md` (Arts. 7–9)
- electronic-only publication? → **`references/zoobank.md`**. Without ZooBank
  registration under Art. 8.5 the name does not exist. This is the most common modern
  failure and it is silent.
- published after 1999? → Art. 16 requires explicit indication that the name is new,
  and for a species-group name, explicit type fixation naming the depository (Art. 16.4).
- is the entity even within the Code's scope? → Art. 1.3 excludes hypothetical concepts,
  teratological specimens, hybrids as such, and infrasubspecific entities:
  `references/01-nomenclature.md`.

### 2. "Which of these two names is valid?"
→ **`references/06-validity-priority.md`** — Art. 23 Priority, Art. 24 simultaneous
publication and the First Reviser.

The trap: **Art. 23.9 reversal of precedence has two conditions and they are
conjunctive.** The senior name must not have been used as valid after 1899 (23.9.1.1)
*and* the junior name must have been used as valid in at least 25 works by at least 10
authors within the preceding 50 years spanning at least 10 years (23.9.1.2). Almost
everyone recalls the first and drops the second. If both hold, the author must publish
the act citing both names (23.9.2), and the *junior* name becomes the *nomen protectum*
while the senior becomes the *nomen oblitum* — the naming is counter-intuitive, so check
which is which every time. If the conditions do not hold, the case goes to the
Commission (23.9.3); it is not the author's to decide.

### 3. "Is this the right spelling, ending, or author citation?"
→ **`references/07-formation-spelling.md`** — Arts. 25–34.
- gender agreement (Art. 31.2) applies only to adjectival epithets, never to nouns in
  apposition or genitives, and the spelling alone does not tell you which it is
- justified emendation / unjustified emendation / incorrect subsequent spelling
  (Art. 33) are three different things with three different authorship consequences
→ **`references/11-authorship.md`** — Arts. 50–51, including Art. 51.3: parentheses
around the author mean the species sits in a genus other than the original one. That is
a statement about the current combination, not about the name.

### 4. "Are these homonyms?"
→ **`references/12-homonymy.md`** — Arts. 52–60. Species-group homonymy exists only
within a genus (Art. 53.3), so it is not a property of a name string; Art. 54 lists
names that never enter homonymy at all; Art. 58 makes certain spelling variants count
as identical — but only when the names share derivation and meaning.

### 5. "Is this type designation valid?"
→ **`references/13-typification.md`** (Art. 61, the principle and the objective /
subjective synonymy distinction that falls out of it)
→ **`references/16-species-group-types.md`** (Arts. 71–76: holotype, syntype,
lectotype, neotype, type locality). Two live traps: a lectotype designation after 1999
must satisfy Art. 74.7 in full, and a neotype designation must satisfy every one of the
seven conditions of Art. 75.3 — they are conjunctive, and one omission voids the act.
→ **`references/15-genus-group-types.md`** (Arts. 66–70: type species, and the
precedence of the fixation mechanisms — original designation, then monotypy, then
tautonymy, before any subsequent designation can be valid)
→ **`references/14-family-group-types.md`** (Arts. 62–65: type genus)

### 6. "How do I store this?"
→ **`references/data-modeling.md`** — the name / taxon-concept / nomenclatural-act
separation, and the eight cases where naive schemas break.
→ **`references/dwc-mapping.md`** — the Darwin Core fields, and the
`nomenclaturalStatus` vs `taxonomicStatus` split that most datasets get wrong.

### Everything else
| Question | File |
|---|---|
| What does this term mean? | `references/glossary.md` |
| Coordinate ranks, nominotypical taxa | `references/08-family-group.md`, `09-genus-group.md`, `10-species-group.md` |
| Family-group suffix and stem | `references/07-formation-spelling.md` (Art. 29) |
| Infrasubspecific vs subspecific | `references/10-species-group.md` (Art. 45.6) |
| Date of publication, "online first" | `references/05-date.md` (Arts. 21–22) |
| Commission, Cases, Opinions, plenary power | `references/17-commission.md` |
| How the Code itself is amended | `references/18-regulations.md` |
| Code of Ethics, general recommendations | `references/appendices.md` |
| Plants, fungi, bacteria, ambiregnal names | `references/other-codes.md` |

---

## Two distinctions that decide most answers

**Available vs valid.** *Available* means the name passed Arts. 10–20 at publication.
It is permanent, objective, and says nothing about whether anyone should use the name.
*Valid* means it is the correct name to use for a taxon under someone's current
taxonomic hypothesis — an opinion, revisable, and relative to a circumscription. Every
available name has exactly one status on the first axis and a changing status on the
second. A dataset with one `status` column has already lost this and cannot get it back.

**Articles vs Recommendations.** Articles are mandatory. Recommendations (`Rec. 73F`),
Examples, and Appendices A and B are not (Art. 89.2) — they are good practice, and
citing them as binding is a real error in manuscript review. Every reference file here
marks which is which; keep that distinction in your answers.

---

## Scripts

Standard library only, no installation.

```bash
# Route to the rule offline: the synthesis, its citation, and the URL
python scripts/explain.py                       # chapter map
python scripts/explain.py --article 23.9        # the rule and its sub-rules
python scripts/explain.py --term "nomen oblitum"
python scripts/explain.py --search lectotype    # across all reference files

# Get the Code's exact wording from the source (network required)
python scripts/fetch_article.py 74.7
python scripts/fetch_article.py glossary
python scripts/fetch_article.py 23 --url

# Check names against the mechanically checkable provisions
python scripts/validate_name.py "Panthera onca (Linnaeus, 1758)"
python scripts/validate_name.py --rank family "Felinae"
python scripts/validate_name.py --csv names.csv --name-column scientificName
python scripts/validate_name.py --csv names.csv --json > report.json
python scripts/validate_name.py --selftest      # assertions pinning rules to Articles

# Has the Code changed upstream since these references were written?
python scripts/sync.py --articles 8 9 10 21 78
```

### Reading validator output
Three levels, and the distinction is the whole value of the tool:

- **`violation`** — decidable from the string itself: a numeral in an epithet
  (Art. 11.2), a lower-case genus (Art. 28), `-inae` on a declared family (Art. 29.2),
  a date before 1758 (Art. 3), an exact epithet collision inside one genus (Art. 57.2).
  Safe to act on in bulk.
- **`warning`** — suspect, and the script cannot decide. Possible gender disagreement
  (Art. 31.2) needs the Latin grammatical category of the epithet; an Art. 58 variant
  collision needs the two etymologies. **A warning is a worklist, never an edit.**
- **`info`** — worth knowing, no defect. Tautonymy (Art. 18) is legal; parenthesised
  authorship (Art. 51.3) is reported so you notice it is combination-dependent.

`validate_name.py` deliberately refuses to guess where the Code requires judgement. If
you need the judgement call made, make it yourself from the original description — and
say that is what you did.

---

## Working practice

**Cite, always.** `ICZN Art. 74.7.3` with a link. A nomenclatural conclusion without an
Article number cannot be checked by the person who has to defend it to a reviewer, and
is therefore worthless however correct it happens to be.

**Never invent an Article number.** If you are unsure, `explain.py --search` or
`fetch_article.py` will tell you in one call. A plausible-looking wrong citation is
worse than no citation, because it will be trusted.

**Say when the Code is silent.** It does not cover taxonomic judgement — whether two
populations are one species is not a nomenclatural question, and the Code says so
(Preamble, Art. 1.1). Sending a user to the Code for an answer it does not contain
wastes their time; name the boundary instead.

**Distinguish the act from the conclusion.** Reversal of precedence, lectotype
designation, and *nomen novum* publication are *acts*: they take effect when published,
by an author, on a date. Reaching the conclusion privately changes nothing. When a user
says "so this name is now the valid one", check whether they mean they have published
the act or that they believe the conditions are met.

---

## Pending / contested

**Not rules. Do not act on anything in this section.** It exists so that a question
about contested ground gets a clear "the current rule is X, and there is an active
debate" rather than false confidence.

- **A fifth edition** has been under discussion within the Commission for years. Nothing
  in it is in force. Until ratified under Art. 90, the 4th edition governs.
- **Names based only on photographs or on DNA sequence, without a preserved specimen.**
  The Code does not currently require a preserved specimen as the name-bearing type — an
  illustration can serve in circumscribed cases (Arts. 72.5.6, 73.1.4) — and several
  such names have been published and heavily criticised. The debate is about whether the
  Code *should* require preserved material, and Declaration 45's addition of the Glossary
  term "specimen, preserved" and Recommendations to Art. 73 (2020) pushes toward
  preservation without mandating it. Current rule: Art. 73 as amended. Contested:
  whether photograph-only types should remain acceptable.
- **Mandatory registration of all new names in ZooBank.** Required now only for
  electronic publication (Art. 8.5.3). Extension to print works has been proposed
  repeatedly and is not in force. See `references/zoobank.md`.
- **Interpreting molecular data as a description or definition** under Art. 13.1.1.
  Declaration 47 added Examples to guide this; the boundary is still argued in practice.

When a user asks about any of these, give the rule in force, name the debate, and do not
blur the two.

---

## References

Chapter by chapter, mirroring the Code's own structure so each file can be checked
against its source and updated when the Commission amends it.

| File | Articles | Subject |
|---|---|---|
| `references/01-nomenclature.md` | 1–3 | Preamble, scope, exclusions, 1758 starting point |
| `references/02-words-in-names.md` | 4–6 | Binominal nomenclature, interpolated names |
| `references/03-publication.md` | 7–9 | What is and is not published |
| `references/04-availability.md` | 10–20 | Availability, with the decision checklist |
| `references/05-date.md` | 21–22 | Determination and citation of dates |
| `references/06-validity-priority.md` | 23–24 | Priority, reversal of precedence, First Reviser |
| `references/07-formation-spelling.md` | 25–34 | Formation, gender, spellings, emendations |
| `references/08-family-group.md` | 35–41 | Family-group taxa, coordination |
| `references/09-genus-group.md` | 42–44 | Genus-group taxa, coordination |
| `references/10-species-group.md` | 45–49 | Species-group taxa, infrasubspecific names |
| `references/11-authorship.md` | 50–51 | Authorship and its citation |
| `references/12-homonymy.md` | 52–60 | Homonymy, replacement names |
| `references/13-typification.md` | 61 | The type concept; objective vs subjective synonymy |
| `references/14-family-group-types.md` | 62–65 | Type genus |
| `references/15-genus-group-types.md` | 66–70 | Type species |
| `references/16-species-group-types.md` | 71–76 | Type specimens, lectotypes, neotypes |
| `references/17-commission.md` | 77–84 | The Commission, Cases, Opinions, plenary power |
| `references/18-regulations.md` | 85–90 | Official texts, interpretation, amendment |
| `references/glossary.md` | — | The Code's terms, with governing Articles and pt-BR |
| `references/appendices.md` | — | Code of Ethics, General Recommendations (both advisory) |
| `references/zoobank.md` | 8, 9, 10, 21, 78 | Electronic publication, registration, LSIDs |
| `references/data-modeling.md` | — | Name / taxon / act separation; anti-patterns |
| `references/dwc-mapping.md` | — | Darwin Core fields for nomenclatural data |
| `references/other-codes.md` | — | ICNafp, ICNP, ambiregnal names, code independence |

`scripts/code_index.json` maps every Article to its canonical URL, its chapter, the
reference file that synthesises it, and a hash of the page as retrieved — which is what
lets `sync.py` notice an upstream amendment.

---

## Related skills

**[darwin-core](../darwin-core/)** — the standard this skill's names travel in. Use both
together whenever nomenclatural data has to be published as DwC-A or DwC-DP; the
Darwin Core Conceptual Model's `Taxon` and `Identification` classes are where the
name / concept separation described in `references/data-modeling.md` lands.

**[skos-xl](../skos-xl/)** — for the controlled vocabularies behind field *values*
(`nomenclaturalStatus`, `typeStatus`, `taxonomicStatus`), and for the TDWG NameThing
pattern representing names with their nomenclatural provenance as RDF.

**[DataProvenance](../DataProvenance/)** — nomenclatural acts are events with an agent,
a date and a source, which is exactly what W3C PROV records. Use it when a database has
to answer "who asserted this synonymy, when, and on what basis".
