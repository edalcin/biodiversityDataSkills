# The Boundary with the Other Nomenclatural Codes

Source: https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/ · https://code.iczn.org/zoological-nomenclature/article-2-admissibility-of-certain-names-in-zoological-nomenclature/ · 4th edition 1999

This file is deliberately short. Its job is not to teach botanical, prokaryote, or viral nomenclature — it is to let a reader recognise the moment a question has left ICZN territory, and to prevent ICZN vocabulary or homonymy logic from being silently applied where it does not hold. For anything past the pointers below, defer to the other code's own authority; do not extrapolate from the ICZN.

## Scope: which code governs what

- **ICZN** — extant and extinct animals (Metazoa), plus protistan taxa when workers themselves treat them as animals for nomenclatural purposes. [Art. 1.1, 1.1.1](https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/#art-1-1)
- **ICNafp** (International Code of Nomenclature for algae, fungi, and plants) — algae, fungi, and plants, including many protist lineages when workers treat them as plants/algae/fungi. Maintained by the International Association for Plant Taxonomy (IAPT).
- **ICNP** (International Code of Nomenclature of Prokaryotes, formerly the Bacteriological Code) — bacteria and archaea.
- **ICVCN** (International Code of Virus Classification and Nomenclature) — viruses, viroids, and related agents; maintained by the ICTV.
- **ICNCP** (International Code of Nomenclature for Cultivated Plants) — cultivar and cultivar-group names for plants under cultivation, layered on top of whichever botanical name the cultivar belongs to.

None of these codes has authority to determine availability, validity, priority, or homonymy of a name governed by one of the others.

## Independence of the codes, and its homonymy consequence

**Art. 1.4** states that zoological nomenclature is independent of other nomenclatural systems: an animal name is not rejected merely because it is identical to the name of a non-animal taxon. [Art. 1.4](https://code.iczn.org/zoological-nomenclature/article-1-definition-and-scope/#art-1-4)

This is reinforced on the homonymy side: **Art. 52.7** states that the name of an animal taxon identical to the name of a taxon that has never been treated as an animal is *not a homonym* for zoological purposes (see `references/12-homonymy.md` for the full Art. 52 Principle of Homonymy). Homonymy under the ICZN (Art. 52) is defined and adjudicated entirely within zoological nomenclature; the ICNafp defines its own homonymy entirely within botanical nomenclature. The two are separate competitions.

The practical upshot, sometimes called a **hemihomonym**: the same string can be a legitimate name in zoology and a legitimate name in botany simultaneously, with no conflict and no priority contest between them, because they were never competing under the same code. Documented cases include *Prunella* (a bird genus, Vieillot 1816, and a plant genus, Linnaeus), *Oenanthe* (a bird genus, Vieillot 1816, and a plant genus, Linnaeus), and *Erica* (a spider genus, Peckham & Peckham 1892, and a plant genus, Linnaeus 1753).

**Consequence for databases:** any dataset spanning more than one kingdom is nomenclaturally meaningless without a populated `nomenclaturalCode` (or equivalent) field on every scientific name record. A homonym-detection routine that compares bare name strings across kingdoms without partitioning by code will generate false positives on exactly these cases. See `references/dwc-mapping.md` for the field, and `references/12-homonymy.md` for how ICZN homonymy itself is scoped and resolved.

## Ambiregnal organisms

Certain groups — most persistently fossil and living protists such as dinoflagellates, and some fungus-like organisms — have historically been worked on by researchers applying different codes to the same lineage (zoologists under the ICZN, phycologists/mycologists under the ICNafp), because the group's affinities were disputed or because fossil and living material were treated separately. The result: the same biological entity can legitimately carry two independently-established names, one available under each code, neither a synonym of the other in the ordinary priority sense — because they were never in nomenclatural competition to begin with.

**How to record this without asserting false synonymy:** do not merge the two names into one taxon record with one marked as a junior synonym unless a taxonomic decision (not a nomenclatural one) has actually been published saying so. Instead, record both names as valid under their own `nomenclaturalCode`, and if a relationship between them is asserted by a source, record it as a documented taxonomic opinion (e.g., via a `taxonRemarks` note or a Darwin Core `ResourceRelationship` of type "is taxonomically equivalent to"), not as an ICZN `taxonomicStatus: synonym` — that status presumes both names compete for validity under the same code, which ambiregnal pairs do not.

## Article 2 of the ICZN — names crossing the animal boundary

- **Art. 2.1** — for a name of a taxon that was *not at first* classified as an animal but later is (e.g., a protist moved into Animalia), the conditions of admissibility into zoological nomenclature are given in **Art. 10.5**, not in Art. 2 itself: the name is available from its original publication provided it satisfies the relevant Chapter 4 availability provisions, is not excluded under Arts. 1.3/3, and — crucially — was a *potentially valid* name under the other code (ICNafp or, per the Code's own text, the Bacteriological Code) at the time. It does not need to be re-described under the ICZN. See `references/04-availability.md` for Art. 10.5 detail.
- **Art. 2.2** — for a name of a taxon that was *at one time* classified as an animal but is later moved out of Animalia, the name continues to compete in zoological homonymy indefinitely, even though its taxon is no longer treated as an animal. Moving a taxon out of the animal kingdom does not retroactively free up its old name for reuse in zoology.

[Art. 2](https://code.iczn.org/zoological-nomenclature/article-2-admissibility-of-certain-names-in-zoological-nomenclature/)

## Terminology that does not transfer

Botanical/ICNafp vocabulary is frequently imported into zoological contexts by habit (especially by database designers who built their schema against a botanical dataset first). The mapping is not 1:1 — use ICZN vocabulary in ICZN contexts:

| ICNafp concept | ICZN equivalent | Note |
|---|---|---|
| *basionym* | no equivalent term | ICZN cites the original name and original author, with the current combination's author following Art. 51.3's parenthesis rule when genus placement changes — there is no separate named concept for "the name this one was based on." |
| *combinatio nova* (comb. nov.) | "new combination" | Same underlying act (moving a species-group name to a different genus); ICZN does not use the Latin term as a formal status label the way ICNafp does. |
| *typus conservandus* / conserved type under Art. 14 | Commission-conserved type under the **plenary power** (Art. 81) | ICNafp conservation runs through published Appendices voted on by nomenclature sections; ICZN conservation is a case-by-case Commission ruling (an Opinion) using the plenary power, not a standing conserved-names list of comparable scope. |
| *nomen illegitimum* | no direct ICZN status; closest are **unavailable** (fails Arts. 10–20) and **invalid** (available but not the name to use, e.g. junior synonym/homonym) | ICZN does not have a single "illegitimate" category comparable to ICNafp's; the reasons ICNafp bundles into "illegitimate" are split across ICZN's separate availability and validity tracks. |
| Latin (historically) / English diagnosis requirement | no language requirement | The ICZN imposes no requirement that a description or diagnosis be in Latin or any particular language. |

Only the rows above are asserted with confidence; if a term is not in this table, do not assume it exists in the ICZN by analogy — check `references/glossary.md` or ask rather than guess.

## Where to go next

For handling names across kingdoms in a single dataset (field mapping, `nomenclaturalCode`, cross-kingdom homonym flags), see the sibling skill `../darwin-core/`. For building or reconciling a controlled vocabulary that needs to span multiple nomenclatural codes without collapsing their distinctions, see `../skos-xl/`.
