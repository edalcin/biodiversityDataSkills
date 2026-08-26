# Chapter 1 — Zoological Nomenclature (Articles 1–3)

Source: https://code.iczn.org/zoological-nomenclature/ · 4th edition 1999

This chapter is the entry gate: it says what zoological nomenclature *is*, which names it governs and which it deliberately ignores, and when the clock starts (1758). Land here first when deciding whether a name-like string belongs in a zoological-nomenclature dataset at all, or when resolving an 18th-century priority dispute.

## Preamble (not an Article, but binding)
The Code's own purpose statement, cited as "Preamble" rather than an Article number.

- **Preamble** — The Code exists to promote stability and universality of animal scientific names and to keep each taxon's name unique; every Article and Recommendation serves that end, and none constrains taxonomic *opinion* (only the *names* used to express it). [Preamble](https://code.iczn.org/preamble/)
- **Preamble** — Priority of publication is the basic organizing principle, but the Code itself provides mechanisms to override strict priority for stability (see `references/06-validity-priority.md`), and the Commission may suspend the Code case-by-case using its plenary power [Art. 81]. [Preamble](https://code.iczn.org/preamble/)
- **Preamble** — Terms used in the Code carry the meaning fixed in the Glossary; the Preamble and Glossary are both binding parts of the Code, not just front matter (see `references/glossary.md`). [Preamble](https://code.iczn.org/preamble/)
- **Preamble** — The International Commission on Zoological Nomenclature (ICZN, "the Commission") is the Code's author and the body with authority to rule on its application (see `references/17-commission.md`). [Preamble](https://code.iczn.org/preamble/)

**Explanatory note (front matter, not itself binding):** the Code comprises the Preamble, 90 Articles in 18 Chapters, and the Glossary; official texts in any language authorized by the Commission are equally authoritative [Art. 87]; only the Commission — never an individual author — may waive or modify a provision for a particular case, using its plenary power [Arts. 78, 81]. Source: https://code.iczn.org/explanatory-note-on-the-code/

## Article 1 — Definition and scope
What counts as an "animal" for nomenclature, which taxonomic ranks the Code regulates, and the categories of names it excludes outright.

- **1.1** — Zoological nomenclature is the naming system for taxa of extant or extinct animals. [Art. 1.1](https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/#art-1-1)
  - **1.1.1** — "Animals" means the Metazoa, plus protistan taxa where the relevant workers themselves treat them as animals for naming purposes — i.e. animal status here is nomenclatural convention, not strict phylogeny. [Art. 1.1.1](https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/#art-1-1-1)
- **1.2.1** — The names the Code covers include names based on domesticated animals, names based on fossil substitutions for animal remains (replacements, impressions, moulds, casts), names for the fossilized *work* of organisms (ichnotaxa — trace fossils), names for collective groups, and pre-1931 names based on the work of extant animals. [Art. 1.2.1](https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/#art-1-2-1)
- **1.2.2** — The Code fully regulates names at family-group, genus-group and species-group rank. Above the family group, only a limited subset of Articles applies: 1–4, 7–10, 11.1–11.3, 14, 27, 28, and 32.5.2.5. A database field for "order" or "class" name governance therefore cannot assume the same rule machinery (priority competition, typification, etc.) that applies below the family group. [Art. 1.2.2](https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/#art-1-2-2)
- **1.3 — Exclusions.** The following are never governed by the Code, regardless of how name-like they look — this is the first filter to apply to any incoming taxonomic-name record:
  - **1.3.1** — names for hypothetical concepts. [Art. 1.3.1](https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/#art-1-3-1)
  - **1.3.2** — names for teratological (malformed/monstrous) specimens as such. [Art. 1.3.2](https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/#art-1-3-2)
  - **1.3.3** — names for hybrid specimens as such — but a taxon that itself originated by hybridization can still be named normally [Art. 17.2]. [Art. 1.3.3](https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/#art-1-3-3)
  - **1.3.4** — names for infrasubspecific entities (below subspecies), unless later deemed available under the specific escape hatch of Art. 45.6.4.1. [Art. 1.3.4](https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/#art-1-3-4)
  - **1.3.5** — names used only as temporary reference tags, never proposed as formal scientific names. [Art. 1.3.5](https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/#art-1-3-5)
  - **1.3.6** — names proposed after 1930 for the work of extant animals (e.g. a nest or burrow of a living species) — contrast with 1.2.1's inclusion of ichnotaxa (fossil work) and pre-1931 work-based names. [Art. 1.3.6](https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/#art-1-3-6)
  - **1.3.7** — mechanical group-wide modifications of existing available names by a standard prefix/suffix meant only to flag group membership (e.g. prefixing every insect genus name with "Ins-"); these "formulae" never entered zoological nomenclature (Opinion 72). [Art. 1.3.7](https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/#art-1-3-7)
- **1.4** — Zoological names are governed independently of botanical/bacteriological codes: a name is not rejected merely because an identical name exists for a non-animal taxon. [Art. 1.4](https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/#art-1-4)

**Recommendations:** Rec. 1A — advisory only: before publishing a new genus-group name, authors are urged to check the botanical (Index Nominum Genericorum) and bacteriological approved-names lists and avoid duplicating an existing non-animal name, even though the Code would not block it.

**Database relevance:** a `kingdom`/`taxonSource` or equivalent field is not sufficient to admit a name into a zoological-nomenclature system — apply the Art. 1.3 exclusion list as a hard validation gate before treating any string as a governed scientific name.

## Article 2 — Admissibility of certain names in zoological nomenclature
Cross-kingdom edge cases: taxa reclassified into or out of the animal kingdom.

- **2.1** — A name for a taxon not originally classified as an animal can still enter zoological nomenclature later, but only under the specific conditions of Article 11.5 (see `references/11-authorship.md`, which covers Art. 11 generally). [Art. 2.1](https://code.iczn.org/zoological-nomenclature/article-2-admissibility-of-certain-names-in-zoological-nomenclature/#art-2-1)
- **2.2** — Once a name has been available while its taxon was classified as an animal, it permanently keeps competing in zoological homonymy even if the taxon is later reclassified out of Animalia (e.g. moved to Protista or another kingdom). [Art. 2.2](https://code.iczn.org/zoological-nomenclature/article-2-admissibility-of-certain-names-in-zoological-nomenclature/#art-2-2)

**Database relevance:** homonymy checks (see `references/12-homonymy.md`) must not be scoped to "currently classified as Animalia" — a name's homonymy history persists across reclassification events per Art. 2.2.

## Article 3 — Starting point
Fixes the date before which no zoological name exists, and resolves the one same-day priority tie the Code had to legislate explicitly.

- **3** — 1 January 1758 is the fixed (arbitrary, not evidentiary) starting point of zoological nomenclature; nothing published before it is governed. [Art. 3](https://code.iczn.org/zoological-nomenclature/article-3-starting-point/#art-3)
- **3.1** — Two works are both deemed published exactly on 1 January 1758: Linnaeus's *Systema Naturae*, 10th edition, and Clerck's *Aranei Svecici*. Because they share a nominal publication date, the Code breaks the tie by rule rather than evidence: names in Clerck's work take priority over names in Linnaeus's 10th edition; every other 1758 work is deemed published *after* the 10th edition (so loses priority to both). [Art. 3.1](https://code.iczn.org/zoological-nomenclature/article-3-starting-point/#art-3-1)
- **3.2** — No name or nomenclatural act from before 1758 is available, but pre-1758 descriptions/illustrations may still be cited as supporting *information* (e.g. to interpret a post-1758 name). For the status of names/acts in works later suppressed by the Commission, see Art. 8.7.1 (`references/03-publication.md`). [Art. 3.2](https://code.iczn.org/zoological-nomenclature/article-3-starting-point/#art-3-2)

**Database relevance:** a `protonymDate` field pre-1758 is invalid for an available zoological name; the priority-comparison routine must special-case the 1758-01-01 tie so that "Clerck" always outranks "Linnaeus, 1758" (10th ed.) rather than being treated as an unresolvable same-date collision.
