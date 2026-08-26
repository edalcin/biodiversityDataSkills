# Glossary of the Code

Source: https://code.iczn.org/glossary-2/ · definitions rewritten, not transcribed

The Glossary is part of the Code itself (**Art. 89.1**: in interpreting the Code, a word's Glossary meaning *is* its meaning for Code purposes, with any doubt referable to the Commission), so its terms are legally operative — not casual explanation, but text you can cite the same way you cite an Article. The definitions below are an original compressed paraphrase of the Code's own Glossary entries (International Trust for Zoological Nomenclature, 1999, all rights reserved); consult the source URL above for the Code's exact wording when precision to the letter matters. The **pt-BR** column gives the customary rendering used in Brazilian zoological practice purely as a recognition aid — the **English term is always the canonical one to cite**; most Latin terms (*nomen nudum*, *sensu lato*, etc.) are used untranslated in Portuguese practice and are left blank rather than have a term invented for them.

## Core distinctions (read these first)

Nearly every database and manuscript-review error traces back to conflating one of these pairs.

- **Available vs. valid.** *Available* is a mechanical pass/fail test (Arts. 10–20): did the name meet the formal publication/description/type requirements when proposed? *Valid* is a further, taxon-specific judgment: is this the one name a taxonomist should currently use for a given taxon (Art. 23, the Principle of Priority, plus any Commission ruling)? A name can be available and still not valid (e.g. it lost out to a senior synonym) — it can never be valid without first being available. **Database rule: `available` is a boolean per name; `valid` is a boolean per name *in a given taxonomic opinion*, and can flip when opinion changes without any nomenclatural act happening.**
- **Valid vs. correct (spelling).** "Valid name" is about which taxon-name wins under Priority/homonymy. "Correct spelling" is a wholly separate axis — the accepted spelling of whichever name is valid (Arts. 32–33: original spelling unless demonstrably incorrect, or a justified emendation). Don't let "correct" leak from one axis to the other.
- **Objective vs. subjective synonym.** *Objective* synonyms share the same name-bearing type — a fact, not an opinion, and it never changes. *Subjective* synonyms are taxonomically judged to apply to the same taxon despite different types — an opinion, and it can change when someone's taxonomy changes. Never store a subjective-synonymy call as if it were a permanent fact.
- **Senior vs. junior.** Pure priority ranking by date of establishment (older = senior), used identically for synonyms and for homonyms. Senior/junior says nothing about which one is currently valid — a junior synonym can become the valid name (nomen protectum reversal, Art. 23.9) and a senior synonym can be permanently displaced (nomen oblitum).
- **Nominal taxon vs. taxon.** A *nominal taxon* is a name-anchored bookkeeping unit: one available name plus (actually or potentially) one name-bearing type. A *taxon* (or "taxonomic taxon") is what a working scientist actually recognizes in nature, and it may lump several nominal taxa together as synonyms. Confusing the two is why databases end up with "one row per name" schemas that can't represent synonymy — you need both entities, linked, not merged.
- **Name-bearing type vs. other type material.** The *name-bearing type* (holotype/lectotype/syntype series/neotype/type species/type genus) is the single objective anchor a name is permanently pinned to (Principle of Typification, Art. 61). Paratypes, paralectotypes, and topotypes are useful reference specimens but carry **no** nomenclatural weight — losing or reidentifying them never changes what the name means.
- **Homonym vs. synonym.** These are opposite failure modes, not variants of the same thing: a *homonym* is one spelling shared by two different taxa (a naming collision — Principle of Homonymy, Art. 52, forces one out); a *synonym* is two-or-more different spellings applied to the same taxon (a naming surplus — Principle of Priority picks the winner).
- **Nomenclatural act vs. taxonomic act.** A nomenclatural act (designating a type, proposing a name, synonymizing under the Code) is governed by the Code and is largely mechanical once the facts are settled. A taxonomic act (deciding two populations are "the same species") is a judgment call the Code deliberately does not regulate. Many Glossary terms exist specifically to mark this boundary (compare "valid", "reject", "synonym" — all partly taxonomic — against "available", "priority", "type fixation" — all purely nomenclatural).

## Latin status-terms and abbreviations (frequently cited, easy to confuse)

These recur constantly in synonymy lists and manuscript comments; several are *not* Code-defined and carry no nomenclatural force even though they look like technical terms.

| Term | Meaning | Code-defined? |
|---|---|---|
| *nomen nudum* | Fails the availability bar (Art. 12/13) — not usable, and a later, compliant use of the same word starts its own authorship/date. | Yes — Glossary + Arts. 12, 13 |
| *nomen novum* | A name coined solely to replace an existing (usually preoccupied) one; same type as the name it replaces. | Yes — Glossary + Arts. 67.8, 72.7 |
| *nomen oblitum* | A long-unused (since before 1900) senior synonym/homonym stripped of precedence by an Art. 23.9.2 case. | Yes — Glossary + Art. 23.9 |
| *nomen protectum* | The junior name that wins precedence over a *nomen oblitum*. | Yes — Glossary + Art. 23.9.2 |
| *nomen dubium* | Taxonomic-judgment label: application to a real taxon can't be confidently pinned down. | Yes — Glossary (no Article; it is a judgment, not a status) |
| *nomen inquirendum* | Informal name-level analogue of *nomen dubium* / "species inquirenda". | **No** — not a Glossary headword |
| *incertae sedis* | "Of uncertain position" — a classification flag, not a name status. | Yes — Glossary (no Article) |
| *sensu lato* / *sensu stricto* | Broad sense / narrow sense of a taxon concept as used by a cited author. | Yes — Glossary (no Article) |
| *sic* | Marks a quoted spelling as reproduced verbatim, error included. | **No** — general scholarly convention, not in the Glossary |

**Glossary abbreviations:** a. = adjective · Art., Arts. = Article(s) of the Code · e.g. = *exempli gratia*, "for example" · f. = feminine · i.e. = *id est*, "that is" · m. = masculine · n. = noun · neut. = neuter · pl. = plural · q.v. = *quod vide*, "which see" · sing. = singular · v. = verb.

## Terms

| Term | Definition | Governing Article | pt-BR |
|---|---|---|---|
| abbreviation | Shortened form of a word or name; genus-group names may be abbreviated after first full use, always followed by a full stop. |  | abreviatura |
| aberration (ab.) | Informal term for a variant individual within a species; a name coined solely to denote an aberration is not available. |  |  |
| absolute tautonymy | Identical spelling between a generic/subgeneric name and the specific/subspecific name of a species/subspecies it originally included. | Arts. 18, 68.4 |  |
| act, nomenclatural | Any published act that changes a name's nomenclatural status or a nominal taxon's typification (e.g. a designation, synonymy, or emendation). |  | ato nomenclatural |
| adopt (v.) | To take up a previously unavailable name and use it as if newly proposing it, thereby giving it fresh authorship and date. | Arts. 11.6, 45.5.1, 45.6.4.1 |  |
| adoption | Formal acceptance by the Commission of a Part of the List of Available Names in Zoology. | Art. 79 |  |
| aggregate | An informal grouping of species (or subspecies) within a genus/subgenus/species, optionally shown as a parenthetical species-group name. | Art. 6.2 |  |
| agreement, gender | Requirement that a Latin/latinized adjectival species-group name change its ending to match the grammatical gender of the genus it is combined with. | Art. 31.2 | concordância de gênero |
| allotype | A designated specimen of the sex opposite the holotype; not a Code-regulated category. | Rec. 72A (advisory only) | alótipo |
| anagram | A name built by rearranging the letters of an existing word. |  |  |
| animal | For the Code, covers the Metazoa plus any protistan taxon that has been or is treated as an animal for nomenclatural purposes. | Art. 1.1 | animal |
| animals, domesticated | Animals differing from their wild ancestors through human selective breeding (e.g. Canis familiaris). |  | animais domesticados |
| anonymous | Of a work, name/act, or author: one whose author cannot be identified from the work itself; special availability rules apply. | Art. 14; see also Art. 50.1 | anônimo |
| anonymous work | A published work whose author(s) cannot be determined from its own contents. | Art. 14 |  |
| archive | n. A repository intended to permanently preserve a work; v. to deposit a work there so it survives. |  |  |
| Articles | The Code's mandatory (as opposed to advisory) provisions. |  | Artigos |
| as such | Fixed phrase meaning 'strictly in the cited form' (e.g. a photograph 'as such' is the print, not a later reproduction). |  |  |
| auctorum (auct., auctt.) | Latin tag meaning 'of authors', flagging that a name is being used in a later, collective sense rather than its original one. |  |  |
| author | The person(s) legally credited with a work, name, or nomenclatural act; if credited to an office or body, only the individual(s) actually responsible count. | Arts. 50, 51 | autor |
| availability | Formal, threshold compliance test applied to works, names, and acts (met/not met) — a precondition for any name to be usable at all, distinct from validity. | Arts. 10–20 (names); Arts. 8–9 (works); Art. 11 (acts) | disponibilidade |
| available name | A name proposed for an animal that clears the Article 10–20 formation/publication tests and isn't one of the categories Art. 1.3 rules out from the start — the baseline pass/fail every name must clear before validity is even asked. | Arts. 10–20 | nome disponível |
| available nomenclatural act | A nomenclatural act published in an available work. |  |  |
| available work | A published work that clears the bar for establishing names/acts in it, whether by satisfying the Code directly or by a Commission ruling. | Arts. 8–9 |  |
| binomen / binominal name | The two-word combination (genus name + species name) forming a species' scientific name; interpolated names are not counted as part of it. | Art. 5.1 | binômio |
| binominal nomenclature | The naming system in which only the species rank (not other ranks) is denoted by a two-part name. |  | nomenclatura binominal |
| Binominal Nomenclature, Principle of | The rule that species alone get two-part names, subspecies get three-part names, and higher taxa get one-word names. | Arts. 5, 11.4 |  |
| Bulletin of Zoological Nomenclature | The Commission's official journal, where cases, Declarations, and Opinions are published. |  |  |
| case | (1) A nomenclatural problem submitted to the Commission for a ruling; (2) a grammatical inflection (nominative, genitive) relevant to Latin name-forms. |  | caso (1); caso gramatical (2) |
| caste | In social insects, a morphologically/functionally distinct group within one species or subspecies (e.g. worker, drone, queen). |  | casta |
| change, mandatory | A spelling change the Code itself compels: to a family-group suffix, or to a species/subspecies name's gender ending. | Art. 34 |  |
| Chapter | A top-level division of the Code's text. |  | capítulo |
| character | Any observable trait of organisms used to recognize, differentiate, or classify taxa. |  | caráter |
| Code | Short title for the International Code of Zoological Nomenclature; also used generically for the sister codes governing bacterial and botanical names. |  | Código |
| collection | An assembled, maintained set of specimens kept for study or display. |  | coleção |
| collective group | An assemblage of species (or of developmental stages, e.g. eggs/larvae) that cannot confidently be placed in a nominal genus; its name is treated as genus-group but under special rules. | Art. 42.2.1 | grupo coletivo |
| collective-group name | What a collective group is called — a genus-group-style name under special rules (see 'group'). | Art. 42.2.1 |  |
| combination | Pairing of a generic name with a species(-and-subspecies) name to build a species' or subspecies' full scientific name. |  | combinação |
| combination of letters, arbitrary | A coined name that its author did not base on any existing word. |  |  |
| Commission | Short title for the International Commission on Zoological Nomenclature, the body empowered to rule on nomenclatural cases. | Art. 77.1 | Comissão |
| compound (name/word) | A name/word built from two or more root components (excluding prefixes/suffixes), normally written as a single word. | Art. 32.5.2.4 |  |
| concept, hypothetical | A published taxonomic concept that, at the time of publication, matched no real known animal — pure invention or prediction. | Art. 1.3.1 |  |
| conditional | (1) A name or type fixation proposed with an explicit reservation; (2) inclusion of a taxon in a higher taxon subject to a stated proviso. | Arts. 15.1, 51.3.3 |  |
| conserve (v.) | Commission action, via plenary power, that removes a specific obstacle blocking a name's use or that certifies a work as available, done to protect stability. | Arts. 78, 81 | conservar |
| conserved name | A name the Commission has made usable as valid by removing what would otherwise block it. |  | nome conservado |
| conserved work | A work the Commission has ruled to be available despite not meeting the ordinary criteria. |  |  |
| Constitution | Short title for the Constitution of the International Commission on Zoological Nomenclature (governs the Commission itself, not nomenclature) — see references/17-commission.md. |  |  |
| Coordination, Principle of | Within one of the three name-groups, a name established at one rank is automatically treated as simultaneously established, with the same author/date, at the other ranks of that group sharing the same name-bearing type. | Arts. 36, 43, 46 | Princípio da Coordenação |
| copyist's error | A misspelling introduced while copying a name. |  |  |
| correct original spelling | An available name's spelling exactly as first published, unless Art. 32.5 shows it was demonstrably wrong at the time. | Art. 32.5 |  |
| corrigendum | A published note by an author/editor/publisher citing and correcting an error in that same work. |  |  |
| cotype | Obsolete, Code-disfavoured term formerly meaning syntype or paratype; avoid using it. | Rec. 73E |  |
| date of publication | The date copies of a work first become available by sale or free distribution; if unknown, fixed by the Article 21 default rules. | Art. 21 | data de publicação |
| Declaration | A provisional Code amendment issued by the Commission, later folded into the next edition. | Arts. 78.3.2, 80.1 | Declaração |
| deem | To treat/rule something as being a certain way for Code purposes, regardless of other facts. |  |  |
| definition | A prose statement of the characters that, together, uniquely mark a taxon. | Arts. 12, 13 | definição |
| description | A prose statement of a specimen's or taxon's taxonomic characters. | Arts. 12, 13 | descrição |
| designation | The formal step, taken by an author or the Commission, that pins down a nominal taxon's name-bearing type via an explicit statement. |  | designação |
| diagnosis | A statement of the characters that separate a taxon from those it could be confused with (contrast 'description', which need not be comparative). |  | diagnose |
| differentiate (v.) | To distinguish one taxon from others by its characters. | Art. 13 |  |
| Direction | Obsolete term (pre-1999 editions) for a Commission statement completing/correcting an Opinion; superseded by Official Corrections. |  |  |
| Disclaimer | An author/editor/publisher's stated exclusion of a work, or of specific names/acts in it, from zoological nomenclature. | Arts. 8.2, 8.3 |  |
| division | A subgeneric-level rank used to subdivide a genus/subgenus (or a taxon so ranked) — nomenclaturally treated exactly like a subgenus. | Art. 10.4 |  |
| electronic publication | A work issued and distributed by electronic signals; became independently eligible as available only from 2012 onward, and only if it meets the 2012 amendment's registration/archiving conditions. | Arts. 8.5, 8.6, 9.8, 9.9, 21.8, 78.3.4 (2012 amendment) | publicação eletrônica |
| elide (v.) | To deliberately drop one or more letters from within a word when forming a name. | Art. 29.3.1.1 |  |
| emendation | An intentional change to an available name's original spelling (or the resulting respelled name). | Art. 33.2 | emenda |
| ending, gender | The terminal letters of a genus-group name that mark its grammatical gender, controlling how adjectival species names combined with it must be spelled. | Art. 30.2 |  |
| ending, genitive | The terminal letters marking a species-group name as a genitive-case noun (e.g. -i, -ae, -orum, -arum), reflecting the gender/number of the person, place, or thing it honours. | Art. 31.1.2 |  |
| error | An incorrect spelling. |  | erro |
| establish (v.) | For a nominal taxon/name: to satisfy the Code's requirements so that the name becomes available. |  | estabelecer |
| excluded | (1) Barred from nomenclature altogether, whether by a Code provision or by a disclaimer; (2) of a specimen: expressly cut out of a type series or dropped from a name-bearing type. | Arts. 8.2, 8.3, 72.4.1, 73.1.5 |  |
| excluded name | A name that Article 1.3 bars from ever being available, or one that has been disclaimed. | Arts. 1.3, 8.2, 8.3 |  |
| extant | (1) Of a taxon: has living representatives; (2) of a specimen: still exists physically. |  |  |
| extinct | Of a taxon: no living representatives remain. |  | extinto |
| family | Sits between superfamily and subfamily in the family-group hierarchy; also denotes a taxon at that level. | Art. 35.1 | família |
| family group | The block of ranks, from superfamily down to (and including) subtribe, whose names the Code fully regulates. | Art. 35.1 | grupo-família |
| family name | A scientific name at the rank of family; suffix -IDAE. |  | nome de família |
| family-group name | A scientific name at any rank of the family group. | Art. 35 | nome de grupo-família |
| field, taxonomic | A named taxon or set of taxa used to scope a discussion (e.g. 'Crustacea: Amphipoda'). |  |  |
| fixation | General term for how a name-bearing type gets determined — by designation, by monotypy, or by tautonymy. | Arts. 68–75 | fixação |
| fixation by elimination | The (invalid) idea that a type species is fixed merely by later removing all but one originally included species from a genus — not itself a recognized method. | Art. 69.4 (but see 69.1.1) |  |
| form | (1) Post-1960 usage: automatically denotes infrasubspecific rank; (2) pre-1961 usage: governed by separate transitional rules; also loosely, any recognizable variant within a species (larval/adult, sexual, seasonal). | Art. 45.6.3-4 |  |
| formulae, zoological | Standardized prefixes/suffixes attached across a taxonomic group's names to flag common membership; not regulated by the Code (family-group rank suffixes are not formulae). | Art. 1.3.7 |  |
| gender | A genus-group name's grammatical property (masculine/feminine/neuter), which forces matching endings on Latin/latinized adjectival species names combined with it. | Arts. 30, 31.2 | gênero gramatical |
| generic name | Either a genus-rank scientific name, or, functionally, whichever word opens a binomen/trinomen. | Art. 5 | nome genérico |
| genotype | Obsolete, Code-disfavoured term formerly meaning type species; avoid using it (note: unrelated to the genetics sense of 'genotype'). | Rec. 67A |  |
| genus | The genus-group tier immediately under the family group, one step up from subgenus; also denotes a taxon at that level. |  | gênero |
| genus group | The two-rank tier — genus plus subgenus — that sits above species-group ranks and below the family group; collective-group and genus-level ichnotaxon names count as genus-group names too. | Art. 42.1, 42.2.1 | grupo-gênero |
| genus-group name | Covers genus and subgenus names alike, plus names for collective groups and genus-level ichnotaxa. | Art. 42 | nome de grupo-gênero |
| group | A general term for an assemblage of taxa; see family group, genus group, species group. |  | grupo |
| hapantotype | A set of preparations of directly related life-cycle stages that jointly serve as the name-bearing type of an extant protistan species; treated as a holotype and immune to lectotype-style splitting except to exclude contaminant taxa. | Arts. 72.5.4, 73.3 | hapantótipo |
| hectographing | An obsolete gelatine-transfer copying method; relevant to whether pre-electronic works count as 'printed'. |  |  |
| hierarchy, taxonomic | The nested system of ranks (species → genus → family → ...) ordered by increasing inclusiveness. |  | hierarquia taxonômica |
| holotype | The single specimen fixed as a species/subspecies' name-bearing type when the taxon is established (unless it is a hapantotype). |  | holótipo |
| homonym | One of two-or-more available names that are identically (or, for family-group names, near-identically) spelled and were established for different nominal taxa in the same name-group. | Art. 53 | homônimo |
| homonymy | The relationship of being homonyms, or the state of having a homonym. |  | homonímia |
| Homonymy, Principle of | Every taxon's name must be unique; a junior homonym may never stand as a valid name. | Art. 52 | Princípio da Homonímia |
| hybrid | The offspring of two individuals of different taxa; naming hybrids and hybrid-origin taxa follows special rules. | Arts. 1.3.3, 17, 23.8 | híbrido |
| hyphen | The punctuation mark '-', used in compound species names with a single-letter first element, or joining words used adjectivally. | Art. 32.5.2.4.3 |  |
| ichnotaxon | A taxon founded on a fossilized trace of animal activity (trail, track, burrow) rather than the animal's body. |  |  |
| inadvertent error | An unintended misspelling (slip of the pen, copying or printing error) not deliberately made by the original author. | Art. 32.5.1 |  |
| inappropriate name | A name suggesting a character, quality, or origin the taxon does not actually have — not by itself a bar to availability or validity. |  |  |
| incertae sedis | Latin: 'of uncertain [taxonomic] position' — flags unresolved placement, not a nomenclatural status. |  |  |
| incorrect original spelling | An originally-published spelling that Arts. 32.4–32.5 flag as wrong from the outset (e.g. an internal inconsistency in the original work itself). | Arts. 32.4, 32.5 |  |
| incorrect subsequent spelling | Any later respelling of an available name that is neither a mandatory change nor an emendation — i.e. a plain error introduced after establishment. | Art. 33.3 |  |
| index | An ordered (usually alphabetical) list of names/subjects in a work with page references. |  |  |
| indication | For pre-1931 names only: a reference to already-published information (rather than an original definition/description) that can satisfy the availability requirement. | Art. 12.2; see also 13.6.1 |  |
| information, taxonomic | Descriptive/illustrative material about taxa; unlike names/acts, it may validly be drawn from an otherwise-unavailable earlier work (e.g. pre-1758, non-binominal, or suppressed). |  |  |
| infraspecific name | Umbrella term for any name below species rank, covering both subspecific and infrasubspecific names. |  |  |
| infrasubspecific | Of a rank/taxon/name: below the rank of subspecies; such names fall outside the Code's regulation. | Art. 1.3.4 |  |
| infrasubspecific entity | A taxon, or intra-population variant (sex, caste, age/seasonal form, aberration, generation), below subspecies rank. |  |  |
| infrasubspecific name | Names something at infrasubspecific rank; falls outside Code regulation. | Art. 1.3.4 |  |
| infrasubspecific taxon | A taxon ranked below subspecies; its name is outside Code regulation. | Art. 1.3.4 |  |
| interpolated name | A name in parentheses inserted after a generic name (subgenus), after a genus-group name (species aggregate), or after a specific name (subspecies aggregate); not counted as one of the binomen/trinomen's own name-elements. | Art. 6 |  |
| invalid | Of an available name/act: fails the Code's test for acceptance (contrast 'unavailable', a more basic failure). |  | inválido |
| invalid name | An available name that is objectively invalid (junior homonym, junior objective synonym, Code-barred, or suppressed) or subjectively invalid (judged a junior synonym, or inapplicable, by taxonomic opinion). |  | nome inválido |
| invalid nomenclatural act | An available nomenclatural act that fails to comply with the Code's provisions. |  |  |
| junior homonym | Of two homonyms, the one established later (or not given First Reviser precedence when simultaneous). | Art. 24 | homônimo júnior |
| junior synonym | Of two synonyms, the one established later (or not given First Reviser precedence when simultaneous); see also the reversal-of-precedence rule for long-unused senior synonyms. | Arts. 23.9, 24 | sinônimo júnior |
| justified emendation | A correction of a demonstrably incorrect original spelling; keeps the original name's authorship and date. | Art. 33.2.2 | emenda justificada |
| kingdom | The highest formal rank in the taxonomic hierarchy (the Code no longer endorses a single taxon 'Animalia' at this rank). |  | reino |
| lapsus calami | Latin: 'slip of the pen' — an author's own inadvertent writing error, as distinct from a copyist's or printer's error. | Art. 32.5.1 |  |
| latinize (v.) | To give a non-Latin word Latin form (ending/suffix) so it can serve as a scientific name. |  | latinizar |
| lectotype | A single specimen selected from a syntype series, after the taxon's establishment, to serve as its sole name-bearing type. | Art. 74 | lectótipo |
| Linnaean tautonymy | A pre-1931 genus/subgenus name that happens to duplicate an even older (pre-1758) name once listed as a synonym under just one of its founding species. | Art. 68.5 |  |
| List of Available Names in Zoology | The cumulative, Commission-adopted register of names in a taxonomic field, built up from adopted Parts. | Art. 79 |  |
| mark, diacritic | An accent, cedilla, tilde, umlaut, etc. marking pronunciation; generally must be dropped/transliterated when latinizing. |  |  |
| Metazoa | Multicellular organisms treated as animals for nomenclatural purposes. |  | Metazoa |
| mimeographing | An obsolete stencil-based duplication method, relevant to historical publication status. |  |  |
| misapply (v.) | To use a name in a sense inconsistent with the Code (e.g. not matching its name-bearing type), whether deliberately or by mistake. |  |  |
| misidentify (v.) | To wrongly attribute a specimen to a taxon it does not belong to. |  |  |
| monotypy | Automatic type fixation: (1) a genus/subgenus established for a single included species is that species' type by monotypy; (2) a species-group taxon based on one specimen, without an explicit holotype statement, has that specimen as holotype by monotypy. | Arts. 68.3, 73.1.2 | monotipia |
| multiple original spellings | Two or more different spellings of the same name all published as original at establishment. | Art. 32.2.1 |  |
| name-bearing type | The specimen(s) or nominal taxon (type genus/species, holotype, lectotype, syntype series, or neotype) that objectively anchors what a name applies to — contrast with other, non-type-bearing material in a collection. | Art. 61 | tipo portador do nome |
| neotype | A single specimen the Commission (plenary power) or an author designates as name-bearing type when none of the original type material is believed to survive and stability requires one. |  | neótipo |
| new combination | The first-ever pairing of an existing species-group name with a particular generic name. |  | combinação nova |
| new replacement name (nomen novum) | A substitute word deliberately coined for a name that is already unusable (most often a junior homonym); it inherits the exact type of the taxon whose name it stands in for. | Arts. 67.8, 72.7 |  |
| new scientific name | Any name — available or not — the first time it is proposed for a taxon. |  |  |
| nomen dubium (pl. nomina dubia) | Latin 'name of doubtful/uncertain application' — a taxonomic-judgment label for a name whose type material or original account cannot be tied with confidence to a recognizable taxon. Remains available; the label is not itself a nomenclatural status. |  |  |
| nomen inquirendum | **Not a term defined in the Code's Glossary.** Common taxonomic shorthand for 'a name of doubtful application needing investigation' — the name-level analogue of the Code's own 'species inquirenda'. Use with the same caution as any undefined term: it carries no independent nomenclatural status under the Code. |  |  |
| nomen novum (pl. nomina nova) | Latin equivalent of 'new replacement name' (see above). | Arts. 67.8, 72.7 |  |
| nomen nudum (pl. nomina nuda) | Latin 'naked name' — a name that fails the Article 12 (pre-1931) or Article 13 (post-1930) availability tests; not an available name, so the same word can later be validly (re-)established, taking its authorship and date from that later act, not from the nomen nudum publication. | Arts. 12, 13 |  |
| nomen oblitum (pl. nomina oblita) | Latin 'forgotten name' — a senior synonym/homonym unused since 1899 which, once an Art. 23.9.2 case is decided, loses precedence over the junior name in prevailing use (a nomen protectum); remains available and citable, just not usable as valid absent a fresh reversal. A differently-scoped, now-closed sense of the term applied to names rejected between 1961 and 1973 under the prior Code's Art. 23b. | Art. 23.9; historical use under Art. 23.12 |  |
| nomen protectum (pl. nomina protecta) | Latin 'protected name' — the junior synonym/homonym given precedence over a nomen oblitum under Art. 23.9.2. | Art. 23.9.2 |  |
| nomenclatural (adj.) | Relating to the naming system, as opposed to taxonomic judgment. |  | nomenclatural |
| nomenclatural status | A name/act/work's overall standing: availability, and (for a name) its spelling, its taxon's typification, and its precedence relative to competing names. |  |  |
| nomenclature | A system of names plus the rules for forming and using them. |  | nomenclatura |
| nominal taxon | A taxon-concept anchored to a specific available name, carrying a name-bearing type whether or not that type has been physically fixed yet — distinct from 'taxon', which is the biological entity a scientist recognizes and may embrace several nominal taxa as synonyms. |  | táxon nominal |
| nominate (adj.) | Older editions' term for what the current Code calls 'nominotypical'. |  |  |
| nominotypical taxon | The subordinate taxon within a family-, genus-, or species-group taxon that itself contains the name-bearing type (e.g. the nominotypical subspecies). | Arts. 37, 44, 47 | táxon nominotípico |
| noun phrase | A compound species-group name built from noun+noun (or noun+adjective) used in apposition; a trailing adjective's gender ending follows the noun it modifies, not the combined genus. | Art. 31.2.1 |  |
| objective | Demonstrably fixed by fact, not a matter of taxonomic opinion — contrast 'subjective'. |  | objetivo |
| objective synonym | Synonyms whose nominal taxa share the same name-bearing type (or, for family-/genus-group names, whose types are themselves objective synonyms) — a factual, not opinion-based, relationship. |  | sinônimo objetivo |
| Official Correction | The Commission's mechanism for fixing a mistake it made in an earlier Opinion. | Art. 80.4 |  |
| Official Index | One of four Commission-maintained lists of works/names rejected/ruled invalid (works, family-, genus-, species-group names). | Art. 80.7 |  |
| Official List | One of four Commission-maintained lists of works/names formally ruled upon and accepted (works, family-, genus-, species-group names). | Art. 80.6 |  |
| Official Register | The Commission's central record of works, names, and acts submitted for registration; its online form is ZooBank. | Art. 78.2.4 |  |
| offprint | Older term for what the Code calls a separate (see 'separate'). |  |  |
| Opinion | A formal Commission publication ruling on how the Code applies to a specific case. | Art. 80.2-5 | Opinião |
| optical disc | CD-ROM/DVD-ROM media; could carry an available work only between 1985 and 2012 (superseded by the 2012 e-publication amendment). | Art. 8.4.2 |  |
| original description | The description published when a nominal taxon is first established. |  |  |
| original designation | A type designation made at the moment the nominal taxon is established. | Arts. 68.1, 73.1.1 |  |
| original publication | (1) The work first publishing a name/act; (2) the fact of a name/act's first publication. |  |  |
| original spelling | However a name was actually spelled at the moment it was established (there may be more than one — see multiple original spellings). | Arts. 32.1, 32.2.1 |  |
| originally included nominal species | The species deemed part of a nominal genus-group taxon at its establishment, for the purpose of fixing a type by monotypy. | Art. 67.2 |  |
| paralectotype | Each former syntype left over once a lectotype has been selected from the series. | Art. 72.1.3; Rec. 74F (advisory) | paralectótipo |
| paratype | Every member of a species-group type series except whichever one is the holotype. | Rec. 73D (advisory) | parátipo |
| Part of the List of Available Names in Zoology | A Commission-adopted list of available names covering one major taxonomic field. | Art. 79 |  |
| plenary power | The Commission's authority to override or modify Articles 1–76 in a specific case to protect nomenclatural stability. | Arts. 78, 81 | poder plenário |
| potentially valid name | An available name that is not objectively invalid (it may still be subjectively invalid in a given author's opinion). |  |  |
| precedence | The seniority ranking of names/acts: by Priority (Art. 23), by First Reviser choice among simultaneous ones (Art. 24), or by a plenary-power Commission ruling. | Arts. 23, 24 | precedência |
| prefix | Letters attached before a word's root, used only to build derived words, not as a stand-alone word. |  | prefixo |
| preprint | A work issued, with its own imprint date, ahead of its later reissue inside a larger collective work; can count as separately published. |  |  |
| primary homonym | Two identical species-group names given to different taxa while both were already combined with the same generic name. | Art. 57.2 | homônimo primário |
| Principle of Binominal Nomenclature | See binominal nomenclature. | Arts. 5, 11.4 |  |
| Principle of Coordination | See under Coordination, Principle of. | Arts. 36, 43, 46 |  |
| Principle of Homonymy | See under Homonymy, Principle of. | Art. 52 |  |
| Principle of Priority | The oldest available name for a taxon is its valid name, subject to the Code's other Article 23 provisions and any Commission ruling. | Art. 23 | Princípio da Prioridade |
| Principle of the First Reviser | See under Reviser, First. | Art. 24.2 |  |
| Principle of Typification | Every nominal taxon in the three lower name-groups is anchored to an objective reference point — its name-bearing type — whether or not that type is yet on record. | Art. 61 | Princípio da Tipificação |
| printer's error | A misspelling introduced during typesetting. |  |  |
| printing on paper | Producing multiple identical paper copies of text/images; photographic prints do not count as 'printing' for the Code. | Art. 9.2 |  |
| priority, of a name or act | Seniority as measured purely by date of availability. |  | prioridade |
| proposal | (1) Any attempt, successful or not, to establish a name/taxon or perform a nomenclatural act; (2) a formal application to adopt a Part of the List of Available Names. | Art. 79 |  |
| protistan | An organism classified in the Protista; those historically treated as Protozoa are usually deemed animals for Code purposes. | Art. 1.1.1 |  |
| provisions | Synonym for 'rules' — i.e. the Code's Articles. |  |  |
| publication | (1) Any published work; (2) the act of issuing a work that meets Articles 8–9. | Arts. 8, 9 | publicação |
| publish (v.) | To issue a work meeting Article 8, not excluded under Article 9, thereby making public any names/acts/information it contains. | Arts. 8, 9 | publicar |
| published work | See publish. | Arts. 8, 9 |  |
| rank | A name's hierarchical level (e.g. all families sit at the same rank, between superfamily and subfamily). | Arts. 10.3, 10.4, 35.1, 42.1, 45.1 | categoria/posição taxonômica |
| Recommendation | An advisory note attached to an Article, numbered as the Article plus a letter (e.g. Rec. 40A); never mandatory. |  | Recomendação |
| reference, bibliographic | A published citation pointing to a work. |  |  |
| register (v.) | To enter a work/name/author/act into the Official Register. |  |  |
| registration number | A unique code the Official Register assigns to a registered item. |  |  |
| reinstate (v.) | To restore a name previously rejected as a junior secondary homonym to valid status, once the Article 59.4 conditions are met. | Art. 59.4 |  |
| reject (v.) | To set a work aside from nomenclature entirely, or to pick one name over a competing one, per Code rules plus (for names) taxonomic judgment. |  | rejeitar |
| rejected name | (1) A name the Code bars from valid use, set aside for another; (2) a name a taxonomist's own judgment treats as a junior subjective synonym or as inapplicable. |  | nome rejeitado |
| rejected work | A work the Commission has placed on the Official Index of Rejected and Invalid Works. |  |  |
| replacement name | Umbrella term covering both a new replacement name (nomen novum) and any other substitute name. |  |  |
| reprint | For Code purposes, treated the same as a separate. |  |  |
| retraction | Formal removal of a published work, in whole or part, from the permanent public scientific record. Added to the Glossary and Code by **Declaration 46** (Art. 8.8): a retracted electronic work is treated as unpublished from the retraction date on, closing a loophole the 2012 e-publication rules had left open. | Art. 8.8 | retratação |
| Reviser, First | The first author to notice names/spellings/acts published on the very same date and to choose which gets precedence. | Art. 24.2 | Primeiro Revisor |
| rules | The Code's Articles (not titles, Recommendations, or Examples); mandatory, synonym of 'provisions'. |  | regras |
| ruling by the Commission | A Commission decision issued as an Opinion, a Declaration, or (historically) a Direction. | Arts. 80.1, 80.2 |  |
| scientific name | A Code-conforming name (Art. 1) as opposed to a vernacular name; one word above the species group, two (binomen) for species, three (trinomen) for subspecies. Not automatically available. | Arts. 1, 4, 5 | nome científico |
| secondary homonym | Two identical species-group names, originally combined with different genera, that later end up combined with the same genus. | Art. 57.3 | homônimo secundário |
| section | A subgeneric-level rank used to subdivide a genus/subgenus (or a taxon so ranked) — nomenclaturally treated exactly like a subgenus. | Art. 10.4 |  |
| senior homonym | Of two homonyms, the one established earlier (or given First Reviser precedence when simultaneous). | Art. 24 | homônimo sênior |
| senior synonym | Of two synonyms, the one established earlier (or given First Reviser precedence when simultaneous). | Arts. 23.9, 24 | sinônimo sênior |
| sensu | Latin 'in the sense of' — flags that a name is being used the way a specific (cited) author understood it, not necessarily the original author's sense. |  |  |
| sensu lato (s.l.) | Latin 'in the broad sense' — the wider circumscription of a taxon; opposite of sensu stricto. |  |  |
| sensu stricto (s.s., s.str.) | Latin 'in the strict sense' — the narrow circumscription, typically the nominotypical subordinate taxon; opposite of sensu lato. |  |  |
| separate | A privately distributed copy of one contribution from a larger periodical/book, lacking its own imprint date; post-1999 advance distribution of separates does not count as publication. |  | separata |
| sic | **Not a term defined in the Code's Glossary.** General scholarly convention (Latin 'thus') marking that a quoted spelling is reproduced exactly from the source, including an apparent error — used to show the error is the original author's, not introduced by whoever is now citing it. Distinguish from the Code's own defined 'inadvertent error', 'lapsus calami', 'copyist's error' and 'printer's error', which classify *whose* error it is for spelling-correction purposes. | cf. Art. 32.5.1 (classifies error origin) |  |
| species | The basic classificatory rank, sitting directly below the genus group; also denotes a taxon at that level. |  | espécie |
| species group | The lowest Code-regulated rank-group, comprising species and subspecies. | Art. 45.1 | grupo-espécie |
| species inquirenda | Latin 'species of doubtful identity requiring investigation' — a taxonomic-status flag, not a nomenclatural one (contrast the informal, non-Code term 'nomen inquirendum' used for a name in the same situation). |  |  |
| species name | A binomen: the genus name + specific name combination denoting a species. |  | nome de espécie |
| species-group name | Umbrella term covering both tiers below genus: specific names and subspecific names. | Art. 45 | nome de grupo-espécie |
| specific name | The second element of a binomen/trinomen. | Art. 5 | nome específico |
| specimen | A physical example (or part) of an animal, or of a fossil or trace of one; Article 72.5 lists what kinds of specimen may serve as a species-group name-bearing type. | Art. 72.5 | espécime |
| specimen, preserved | **Not present as a distinct headword in the current cached Glossary text** — the Code's own front matter states this term was added to the Glossary by **Declaration 45** together with four new Recommendations under Article 73 (on preserving/illustrating type material). Verify current wording directly at the Glossary and Art. 73 Recommendations before citing a definition; do not infer one. | Art. 73 Recommendations |  |
| specimen, teratological | An abnormal specimen or monstrosity. | Art. 1.3.2 |  |
| spelling | How a name's letters are chosen and arranged. |  | grafia |
| stem (of a name) | (1) The part of a type genus's name that a family-group suffix is added to; (2) the part of a name that a genitive ending is added to when building a species-group name. | Art. 29 (family-group); Art. 31.1.2 (species-group) | radical |
| subfamily | Sits below family in the family-group hierarchy; also denotes a taxon at that level; suffix -INAE. |  | subfamília |
| subfamily name | A scientific name at the rank of subfamily; suffix -INAE. |  | nome de subfamília |
| subgeneric name | A scientific name at the rank of subgenus. |  | nome subgenérico |
| subgenus | Sits below genus in the genus-group hierarchy; also denotes a taxon at that level. |  | subgênero |
| subjective | Depends on individual taxonomic judgment rather than demonstrable fact — contrast 'objective'. |  | subjetivo |
| subjective synonym | Synonyms whose equivalence rests on taxonomic opinion, not a shared name-bearing type. | Art. 61.3.1 | sinônimo subjetivo |
| subordinate taxon | A lower-ranked taxon judged against a same-group taxon it sits inside. |  |  |
| subsequent designation | A type designation made in a later publication than the one that established the taxon. | Arts. 69.1, 74, 75 |  |
| subsequent monotypy | For genera/subgenera established before 1931 with no included species at first: fixation of the type species when exactly one species is later referred to it. | Art. 69.3 |  |
| subsequent spelling | Any spelling of a name other than one used when it was first established. | Art. 33 |  |
| subspecies | The lowest rank the Code regulates, sitting below species; also denotes a taxon at that level. |  | subespécie |
| subspecies name | A trinomen: genus + specific + subspecific name combination denoting a subspecies. |  | nome de subespécie |
| subspecific name | The third element of a trinomen. | Art. 5.2 | nome subespecífico |
| substitute name | Any available name, new or pre-existing, used in place of an older available name (covers both replacement names and some synonym usages). |  |  |
| subtribe | Sits below tribe in the family-group hierarchy; also denotes a taxon at that level; suffix -INA. |  | subtribo |
| subtribe name | A scientific name at the rank of subtribe; suffix -INA. |  |  |
| suffix | Letters added after a word's stem, e.g. -IDAE (family), -INAE (subfamily), or a Latin word-forming suffix in some generic names. | Arts. 29.2, 30 | sufixo |
| superfamily | Sits above family — the topmost fully-regulated rank in the family-group hierarchy; also denotes a taxon at that level; suffix -OIDEA. |  | superfamília |
| superfamily name | A scientific name at the rank of superfamily; suffix -OIDEA. |  | nome de superfamília |
| suppressed name | See suppression. | Art. 81.2.1 |  |
| suppressed work | A work the Commission has ruled unpublished or unavailable. |  |  |
| suppression | A plenary-power Commission ruling that a work is deemed unpublished/unavailable, or that an otherwise-available name is never (or only conditionally) to be used as valid, whether for homonymy purposes ('partial') or for both priority and homonymy ('total'). | Art. 81.2.1 | supressão |
| suprageneric | Of a taxon: ranked above genus. |  | supragenérico |
| synonym | Two or more differently-spelled names, sharing a rank, that all get applied to one taxon. |  | sinônimo |
| synonymy | (1) The relation between synonyms; (2) a list of a taxon's synonyms. |  | sinonímia |
| syntype | Any one specimen out of a type series still awaiting a holotype/lectotype pick; until that pick happens, the whole set jointly stands as the name's anchor. | Arts. 72.1.2, 73.2, 74 | sintipo |
| tautonymous name | A name that repeats the same word at genus- and species-group rank (see tautonymy). | Arts. 18, 68.4, 68.5 |  |
| tautonymy | Reusing one identical word both as a genus/subgenus name and as the species- or subspecies-rank name of a taxon that genus/subgenus originally contained. |  | tautonimia |
| taxon | A named or unnamed taxonomic unit (population(s) inferred as related, sharing distinguishing characters) at any rank; the Code fully regulates names only from superfamily down to subspecies. Contrast 'nominal taxon' (a name-anchored concept) and 'taxonomic taxon' (a working scientist's concept, which may subsume several nominal taxa). |  | táxon |
| taxonomic group | A taxon or set of taxa treated as a unit for discussion. |  |  |
| taxonomic taxon | A working taxonomic unit as a zoologist currently circumscribes it, potentially combining several nominal taxa and individuals; denoted by whichever available name is valid for it. |  |  |
| taxonomy | Classifying organisms as a discipline: building and defending the groupings themselves — sharply distinct from nomenclature, which only names groupings someone else has already drawn. |  | taxonomia |
| text, official | Any language version of the Code text that the Commission has formally authorized; all official texts carry equal authority. | Art. 87 | texto oficial |
| topotype | A specimen collected from a species/subspecies' type locality and thought to belong to it; not a Code-regulated type category and not necessarily part of the type series. |  |  |
| transliteration | Rewriting a word's letters in a different alphabet; required for non-Latin-alphabet source words used as scientific names. |  | transliteração |
| tribe | Sits below subfamily in the family-group hierarchy; also denotes a taxon at that level; suffix -INI. |  | tribo |
| tribe name | A scientific name at the rank of tribe; suffix -INI. |  | nome de tribo |
| trinomen / trinominal name | The three-word combination (genus + species + subspecies names) forming a subspecies' scientific name. | Art. 5.2 | trinômio |
| type (general) | A word denoting a particular kind of type specimen or type taxon; always qualify it (holotype, type species, etc.) — 'type' alone is not a defined status. |  | tipo |
| type fixation | See fixation. | Arts. 68–75 |  |
| type genus | The nominal genus that is a family-group taxon's name-bearing type. |  | gênero-tipo |
| type horizon | The geological stratum a fossil name-bearing type was collected from. |  |  |
| type host | The host species associated with a parasite's name-bearing type. | Rec. 76A.1 (advisory) |  |
| type locality | The place (and, where relevant, stratum) where a species/subspecies' name-bearing type was collected/observed. | Art. 76.1 | localidade-tipo |
| type series | All specimens an author had before them and used to establish a new species-group taxon; absent a holotype designation, every one of them is a syntype eligible for later lectotype selection, and specimens the author expressly excluded are not part of it. | Arts. 72.4, 73.2 | série-tipo |
| type species | The nominal species that is a genus/subgenus's name-bearing type. |  | espécie-tipo |
| type specimen | Older, now-imprecise umbrella term (previous Code editions) for a holotype/lectotype/neotype or any syntype. |  |  |
| typification | Fixing a nominal taxon's name-bearing type so the name has an objective point of reference. |  | tipificação |
| unavailability | The state of failing the Code's availability test — see 'available name', 'unavailable name', 'unavailable work', 'unavailable nomenclatural act'. |  | indisponibilidade |
| unavailable name | A name that fails Articles 10–20, or that Article 1.3 excludes outright. | Arts. 1.3, 10–20 | nome indisponível |
| unavailable nomenclatural act | A nomenclatural act published in a work that is itself unavailable. |  |  |
| unavailable work | A published work in which names/acts cannot be established: e.g. pre-1758, non-binominal, anonymous after 1950, disclaimed, or Commission-ruled unavailable. | Arts. 3, 11.4, 14; see also 12.2.1, 12.2.7, 13.1.2 |  |
| uninominal (name) | A single-word scientific name, used for taxa above the species group. | Art. 4 | uninominal |
| unjustified emendation | Any other intentional respelling; itself becomes an available name with its own author/date, and is a junior objective synonym of the name it changed. | Art. 33.2.3 | emenda injustificada |
| unpublished work | A work that Articles 8–9's publication test does not recognize as issued — including one the Commission has separately decided to treat that way despite appearing to be issued. | Arts. 8, 9 |  |
| usage, prevailing | Whatever reading of a name most of its currently-active users have settled on, no matter how old their publications are. |  | uso corrente |
| valid | Of an available name/act: accepted under the Code and, for a name, judged by the author to be the taxon's correct name — contrast 'available' (a lower bar) and note validity is separate from correct spelling. |  | válido |
| valid name | The single correct name for a taxonomic taxon: the oldest potentially valid name whose name-bearing type falls within the author's concept of that taxon, subject to the Principle of Priority's own exceptions. | Art. 23 | nome válido |
| valid nomenclatural act | The single earliest available act, for a given name/taxon, that does not conflict with the Code — the one to be followed. |  |  |
| validated | Older term meaning what the Code now calls 'conserved'. |  |  |
| variant spellings | Two renderings of a species/subspecies name that Art. 58's rules treat as one and the same for homonymy purposes, even though the letters differ. | Art. 58 |  |
| variety | Pre-1961: interpreted under the transitional Art. 45.6.3-4 rules; post-1960: automatically infrasubspecific and outside Code regulation. | Art. 45.6.3-4 | variedade |
| vernacular name | A common-language name for an animal, as opposed to one proposed for zoological nomenclature; never Code-regulated. |  | nome vernacular/nome popular |
| virtual tautonymy | Near-identical spelling or shared origin/meaning between a genus-group and a species-group name in the same combination; not itself Code-regulated. | Rec. 69A.2 (advisory only) |  |
| vowel, connecting | A vowel joining two word-elements into one compound word; omitted when the second element already starts with a vowel. | Art. 58.12 (relevant to spelling comparison) |  |
| work | Any text or illustration — published, unpublished, or disclaimed. |  | obra |
| work of an animal | The physical product of an animal's activity (burrow, nest, web, track) rather than the animal's body; underlies ichnotaxa but excludes fossil moulds/impressions/replacements. | Arts. 1.2.1, 1.3.6, 10.3, 12.2.8 |  |
| ZooBank | The online implementation of the Official Register of Zoological Nomenclature — see also references/17-commission.md and references/zoobank.md. | Art. 78.2.4 | ZooBank |
| zoological name | A scientific name of an animal taxon under binominal nomenclature. |  |  |
| zoological nomenclature | The Code-governed system of scientific animal names and the rules for forming, treating, and using them. |  | nomenclatura zoológica |
| zoological taxon | A real (natural) taxon of animals, whether or not it currently has a name. |  |  |
| zoologist | Anyone who studies animals, regardless of professional status. |  | zoólogo |

---

**Declaration-added terms flagged in this file:** *retraction* (Declaration 46, Art. 8.8) and *specimen, preserved* (Declaration 45, Art. 73 Recommendations) — see their rows above.

**Cross-references:** Family-group, genus-group, and species-group name mechanics → `references/08-family-group.md`, `09-genus-group.md`, `10-species-group.md`. Type-related terms in depth → `13-typification.md`, `14-family-group-types.md`, `15-genus-group-types.md`, `16-species-group-types.md`. Availability → `04-availability.md`. Priority/validity/synonymy → `06-validity-priority.md`. Homonymy → `12-homonymy.md`. Commission, Opinions, plenary power, ZooBank → `17-commission.md`, `zoobank.md`.
