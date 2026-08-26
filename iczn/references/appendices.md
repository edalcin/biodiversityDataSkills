# Appendices A & B — Code of Ethics and General Recommendations

Source: https://code.iczn.org/appendices/appendix-a-code-of-ethics/ · https://code.iczn.org/appendices/appendix-b-general-recommendations/ · 4th edition 1999

> **Both appendices are advisory, not mandatory — full stop.** Article 89.2 states this in the Code's own legislative text: "Recommendations, examples, and all titles and appendices do not form part of the legislative text of the Code." Appendix A and Appendix B are Appendices. Nothing in either one can be enforced as a rule, cited as grounds to reject a name, or used to override an Article. Their placement bound into the same volume as the Articles is exactly why they get mis-cited as rules — treat every numbered point below as a "should", never a "must". Where an Appendix point restates something an Article separately makes mandatory (e.g. Appendix B §3's mention of mandatory type-collection deposition), the *Article* is the mandatory source and is cited alongside; the Appendix text itself still is not.
>
> This file does **not** cover the Constitution of the ICZN (the Commission's own governing rules) — see `references/17-commission.md`.

## Appendix A — Code of Ethics (advisory)

Source: [Appendix A](https://code.iczn.org/appendices/appendix-a-code-of-ethics/) — a set of conduct norms for authors proposing names, addressed to professional courtesy and priority disputes rather than to the validity of names. **The Commission has no power to investigate or rule on breaches (A.7 below) — there is no enforcement mechanism.** A reviewer citing "Code of Ethics" in a manuscript report is making a collegial appeal, not a nomenclatural objection.

- **A.1** — The Code of Ethics is the set of principles in A.2–A.7, addressed to authors proposing new names.
- **A.2** — Before publishing a new name, first make a reasonable effort (communicate, wait at least a year) to check whether someone else already recognizes the same taxon and intends to name it — including a taxon awaiting a posthumous publication. [Appendix A](https://code.iczn.org/appendices/appendix-a-code-of-ethics/)
- **A.3** — Don't rush out a replacement name (*nomen novum*) for another living author's junior homonym; tell them and give them at least a year to propose their own substitute first.
- **A.4** — Don't propose a name you have reason to think would cause offence.
- **A.5** — Keep nomenclatural debate courteous; avoid intemperate language in print or discussion.
- **A.6** — Editors/publishers should decline to publish material that appears to breach A.2–A.5.
- **A.7** — Enforcement is a matter of individual conscience only: the Commission has **no authority** to investigate or rule on alleged breaches of the Code of Ethics.

**Database relevance:** none of A.1–A.7 map to a stored field or validation rule — they govern author conduct before publication, not the resulting name's nomenclatural status. Do not build a "meets Code of Ethics" flag; there is nothing for the Code to certify.

**Common errors:** citing an Ethics breach (e.g. "should have waited a year," A.2) as grounds to treat a name as unavailable or invalid — it is neither; ethical breach and nomenclatural availability are unrelated. Asking the Commission to rule on an Ethics complaint — A.7 forecloses this explicitly.

## Appendix B — General Recommendations (advisory)

Source: [Appendix B](https://code.iczn.org/appendices/appendix-b-general-recommendations/) — a non-exhaustive checklist of good practice in publishing nomenclatural work, additional to the Recommendations already appended to individual Articles. **This is the natural checklist for reviewing a manuscript that proposes new names**, but every point remains advisory: a manuscript that ignores one is not thereby non-compliant with the Code, only with good practice.

### Stability of nomenclature

- **B.1** — Don't shift a name's prevailing usage or sense without a genuine scientific (reclassification) reason; especially avoid moving a name to a different taxon than the one it is generally understood to denote.
- **B.2** — If following the Code's literal provisions in a specific case would threaten stability or cause confusion, refer the case to the Commission before acting rather than acting unilaterally.

### Establishing and forming new names

- **B.3** — When describing a new taxon, compare it explicitly with related taxa to aid later identification, and illustrate (or cite an illustration of) the name-bearing type material. *(Reminder, not itself the source of the rule: depositing preserved-specimen type material in a named, located collection is independently **mandatory** under [Art. 16.4](https://code.iczn.org/chapter-4-criteria-of-availability/article-16-names-published-after-1999/#art-16-4), not merely recommended.)*
- **B.4** — State clearly which higher taxa (family, order, class, etc.) a new taxon is assigned to.
- **B.5** — For a new genus- or species-group name: state its etymology, and (for genus-group names) its grammatical gender explicitly. Prefer Latin-form, euphonious, memorable names unlikely to be confused with other taxa or vernacular words; genus-group names should not duplicate an existing botanical or microbiological genus name. *(Citing the type genus for a new family-group name is independently **mandatory** under [Art. 16.2](https://code.iczn.org/chapter-4-criteria-of-availability/article-16-names-published-after-1999/#art-16-2); B.5 additionally recommends giving that genus's author and date.)*
- **B.6** — Print genus- and species-group names in a distinct type-face (conventionally italic, never used for higher-taxon names). Species-group names are always lower-case and, when cited, preceded by a generic name or its abbreviation; supraspecific names always start upper-case.
- **B.7** — If a paper proposing a new name is written in a language not widely used internationally for science, include an abstract in a widely understood language flagging the new name.
- **B.8** — Publish new names in paper-printed works with real circulation, in venues zoologists would expect to carry new names in that field — not buried in keys, tables, abstracts, or footnotes.
- **B.9** — Make sure new names reach Zoological Record (BIOSIS, U.K.) so the wider community sees them.

### Citing names

- **B.10** — Cite a name's author and date at least once when discussing a genus-, species-, or family-group taxon in a work; never cite a name as "new" before it is actually established, and never pre-announce a name ahead of its intended publication (see also Appendix A).
- **B.11** — After first mention, a genus-group name may be abbreviated in a binomen/trinomen provided the abbreviation (1) always ends in a full stop and (2) cannot be mistaken for an abbreviation of a different genus name in the same work (e.g. avoid "A." in a paper covering both *Aedes* and *Anopheles*). The same care applies to abbreviating the specific name inside a trinomen.
- **B.12** — Never abbreviate an author's surname. For a name published by more than three authors, the text may cite the first author's surname alone followed by "et al.", but the bibliography should still list every author.

**Database relevance:** B.3–B.5 are the direct source of common "type depository", "etymology", "gender", and "type-genus citation" metadata fields in a taxonomic database schema — even though advisory, they describe exactly the data curators expect a description to supply. B.6 explains why display layers italicize genus/species names. B.11–B.12 govern citation-string formatting (abbreviated combinations, "et al." author strings) that a database's name-citation renderer should reproduce.

**Common errors:** treating B.3's type-deposition language as the rule itself — the mandatory instrument is Art. 16.4, not B.3; citing B.5's type-genus-citation recommendation instead of the actually mandatory Art. 16.2 when checking whether a family-group name is available; assuming B.9 (Zoological Record submission) affects a name's availability — it does not, availability is governed solely by Arts. 10–20.
