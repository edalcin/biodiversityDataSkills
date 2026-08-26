# Darwin Core Mapping — Nomenclatural Fields

Field-by-field guide to the Darwin Core terms that carry nomenclatural information, what the Code means by the value, the rule for filling it, and how it typically breaks. Definitions of the DwC terms themselves are drawn from `../darwin-core/references/term_versions.csv`; the *filling rule* and *failure mode* columns are this skill's own operational guidance, not part of the DwC standard. See `references/data-modeling.md` for the underlying Name/TaxonConcept/Act model these fields are projections of.

## Name string and publication fields

| DwC term | What the Code says the value means | Filling rule | Failure mode |
|---|---|---|---|
| `scientificName` | DwC defines this as the name "with authorship and date information if known" — but the Code itself treats author citation as optional and customary, never part of the name proper ([Art. 51.1](https://code.iczn.org/authorship/article-51-citation-of-names-of-authors/#art-51-1)). Following DwC's own recommendation literally makes `scientificName` ambiguous to parse back into atomic fields, especially when the authorship is parenthesized and itself contains a comma and a year (§ below). | Pick one convention and hold it across the whole dataset: put the **canonical name only** (genus + epithet(s), no authorship) in `scientificName`, and always populate `scientificNameAuthorship` as a separate field. Reassemble the DwC-recommended "full" form only for display, by concatenation. | Mixing conventions row-to-row (`"Cus bus"` in one record, `"Cus bus (Smith, 1850)"` in another) breaks every downstream exact-match join on `scientificName`, and re-parsing authorship out of an embedded string mis-splits on the comma inside `(Smith, 1850)`. |
| `scientificNameAuthorship` | The authorship string "formatted according to the conventions of the applicable nomenclaturalCode." For zoology that means: no parentheses if the name is still in its original combination; parentheses around author+date if the species-group name has been recombined into a different genus ([Art. 51.3](https://code.iczn.org/authorship/article-51-citation-of-names-of-authors/#art-51-3)), except when the original combination itself used an incorrect spelling or emendation of the genus name, in which case no parentheses are used even after correction ([Art. 51.3.1](https://code.iczn.org/authorship/article-51-citation-of-names-of-authors/#art-51-3-1)). | Populate separately from `scientificName` (above). Derive the parenthesization at the moment of filling — do not hand-copy it from a source that may have gotten it wrong. | Parenthesizing a name-above-species-group rank (family/genus group names never take parentheses — Art. 51.3 applies only to species-group names); or failing to re-derive parentheses after a later new-combination act, leaving a stale unparenthesized (or wrongly parenthesized) string. |
| `namePublishedIn` | The bibliographic citation of the work that made the name available under [Arts. 10–20](https://code.iczn.org/chapter-4-criteria-of-availability/article-10-provisions-conferring-availability/). | Cite the **original description**, not a later revision, redescription, or the work that made a new combination. A species transferred to a new genus keeps its original `namePublishedIn` unchanged — only `acceptedNameUsage`/`parentNameUsage` change (below). | Citing the most recent revision because it is the most convenient reference at hand — this silently destroys the ability to verify availability, authorship, and the fixed type against Arts. 10–20. |
| `namePublishedInYear` | The year component of the date fixed under [Art. 21](https://code.iczn.org/date-of-publication/article-21-determination-of-date/#art-21-1). | Use the year the Code would adopt under Art. 21's precision rules (specified date if given; otherwise the fallback to end-of-month or end-of-year, [Art. 21.3](https://code.iczn.org/date-of-publication/article-21-determination-of-date/#art-21-3)), not simply the copyright year on the title page if evidence shows the work actually appeared later ([Art. 21.4](https://code.iczn.org/date-of-publication/article-21-determination-of-date/#art-21-4)). | Trusting a printed date without checking against known evidence of actual availability (parts issued serially, Art. 21.5; advance separates before 2000, Art. 21.8) produces a wrong priority calculation downstream. |
| `namePublishedInID` | A resolvable identifier (DOI, handle, ZooBank publication LSID) for the same work as `namePublishedIn`. | Prefer a ZooBank-registered publication identifier where one exists — see `references/zoobank.md`. | Pointing the ID at a different edition/reprint than the one `namePublishedIn` and `namePublishedInYear` actually cite. |
| `nomenclaturalCode` | Which code's rules govern the construction of this `scientificName`. For zoology the controlled value is `ICZN`. | Populate on **every** record in any dataset that mixes kingdoms or ranks governed by different codes, even if the whole dataset happens to be animals — homonymy across codes is explicitly legal (an animal genus and a plant genus may legitimately share a spelling), so a consumer cannot safely assume a code from taxonomic rank alone. Cross-reference `references/other-codes.md` for how the other codes' homonymy rules differ. | Omitting `nomenclaturalCode` in a mixed-kingdom dataset, then having a name-matching pipeline collide an animal genus with a botanical or bacteriological homonym because nothing on the record disambiguated them. |

## `nomenclaturalStatus` vs. `taxonomicStatus` — the central confusion

DwC's own definitions already draw the line correctly, but the two fields are routinely swapped by data entry because both sound like "is this name okay to use." **`nomenclaturalStatus`**: "the status related to the original publication of the name and its conformance to the relevant rules of nomenclature... based essentially on an algorithm... requires no taxonomic opinion." **`taxonomicStatus`**: "the status of the use of the scientificName as a label for a taxon. Requires taxonomic opinion to define the scope of a taxon... must be linked to a specific taxonomic reference that defines the concept." (Definitions per `../darwin-core/references/term_versions.csv`.) In this skill's terms: `nomenclaturalStatus` is a fact about the **Name**; `taxonomicStatus` is an opinion about a **TaxonConcept** (`references/data-modeling.md` §1).

| Value | Field it belongs in | Why | Justifying Article |
|---|---|---|---|
| nomen nudum | `nomenclaturalStatus` | The name never satisfied the availability requirements (no qualifying description/definition/indication) — it is unavailable from that publication regardless of anyone's taxonomic opinion. | [Art. 12](https://code.iczn.org/chapter-4-criteria-of-availability/article-12-names-published-before-1931/) (pre-1931), [Art. 13](https://code.iczn.org/chapter-4-criteria-of-availability/article-13-names-published-after-1930/) (post-1930) |
| unavailable | `nomenclaturalStatus` | General failure of Arts. 10–20 (not published in an available work, not binominal, infrasubspecific rank, etc.). | Arts. 10–20 |
| junior homonym | `nomenclaturalStatus` | Homonymy is a mechanical spelling/combination collision, determined without reference to any taxonomic circumscription; a junior primary homonym is permanently invalid regardless of opinion (barring the listed exceptions). | [Art. 57.2](https://code.iczn.org/homonymy/article-57-species-group-names/#art-57-2) |
| unjustified emendation | `nomenclaturalStatus` | An algorithmic classification of a spelling change (demonstrably intentional, not required by Art. 34) — available, but the classification itself requires no opinion about the taxon. | [Art. 33.2.3](https://code.iczn.org/formation-and-treatment-of-names/article-33-subsequent-spellings/#art-33-2-3) |
| justified emendation | `nomenclaturalStatus` | Correction of an incorrect original spelling; likewise algorithmic. | [Art. 33.2.2](https://code.iczn.org/formation-and-treatment-of-names/article-33-subsequent-spellings/#art-33-2-2) |
| incorrect subsequent spelling | `nomenclaturalStatus` | Not an available name at all; tracked only for literature-matching. | [Art. 33.3](https://code.iczn.org/formation-and-treatment-of-names/article-33-subsequent-spellings/#art-33-3) |
| nomen oblitum | `nomenclaturalStatus` | The outcome of a specific published reversal-of-precedence act with cited, checkable conditions (`references/data-modeling.md` §3.6) — a fact about that act, not a live taxonomic opinion. | [Art. 23.9.2](https://code.iczn.org/validity-of-names-and-nomenclatural-acts/article-23-principle-of-priority/#art-23-9-2) |
| nomen protectum | `nomenclaturalStatus` | The companion label from the same act. | Art. 23.9.2 |
| conserved / suppressed | `nomenclaturalStatus` | A Commission ruling under the plenary power; the ruling itself is the fact, independent of any one taxonomist's current circumscription. | [Art. 81](https://code.iczn.org/the-international-commission-on-zoological-nomenclature/article-81-use-of-the-plenary-power/) |
| replacement name (nomen novum) | `nomenclaturalStatus` | A structural fact about how the name was proposed (expressly to replace a junior homonym or unusable name). | [Art. 60](https://code.iczn.org/homonymy/article-60-replacement-of-junior-homonyms/) |
| accepted | `taxonomicStatus` | Which name an author currently applies as valid for a circumscription is a taxonomic judgment, even though the *rule* used to pick it (priority) is mechanical — the judgment is in deciding what falls inside the circumscription. | [Art. 23.1](https://code.iczn.org/validity-of-names-and-nomenclatural-acts/article-23-principle-of-priority/#art-23-1) |
| synonym / junior synonym / senior synonym | `taxonomicStatus` | Synonymy exists only relative to a stated circumscription uniting two or more nominal taxa — an opinion, reversible without any nomenclatural act at all. | [Art. 23.3](https://code.iczn.org/validity-of-names-and-nomenclatural-acts/article-23-principle-of-priority/#art-23-3) |
| misapplied | `taxonomicStatus` | A name used for the wrong taxon through misidentification; the defect is in the *application*, not in the name's own standing — the name itself is perfectly available and may be valid elsewhere. | [Art. 49](https://code.iczn.org/species-group-nominal-taxa-and-their-names/article-49-use-of-species-group-names-wrongly-applied-through-misidentification/) |

**Why a *nomen nudum* is not a synonym:** synonymy (per the glossary) is a relationship between two or more *names*; a nomen nudum never became a name in the Code's sense — it failed [Art. 12](https://code.iczn.org/chapter-4-criteria-of-availability/article-12-names-published-before-1931/)/[13](https://code.iczn.org/chapter-4-criteria-of-availability/article-13-names-published-after-1930/) and so was never available to compete for priority under [Art. 23.1](https://code.iczn.org/validity-of-names-and-nomenclatural-acts/article-23-principle-of-priority/#art-23-1) ("the oldest *available* name"). It is absent from nomenclature, not junior to anything in it. **Why a junior synonym is not a nomenclatural defect:** an available name does not stop being available because it is currently treated as a synonym — [Art. 10.6](https://code.iczn.org/chapter-4-criteria-of-availability/article-10-provisions-conferring-availability/#art-10-6) says invalidity as a junior synonym does not affect availability, and Art. 23.3.6 lets a later author revive the very same name as valid the moment the synonymy judgment is reversed, with no new nomenclatural act required. If reclassification alone can flip the value, the value belongs in `taxonomicStatus`.

## Original vs. current usage

| DwC term | What it captures | Filling rule |
|---|---|---|
| `originalNameUsage` / `originalNameUsageID` | The name and combination exactly as first published — the Name-layer fact (`references/data-modeling.md` §3.2). | Populate with the original genus-species combination even when it differs from the currently accepted one; this is what lets a reader recover the basionym-equivalent original combination Art. 48 requires the model to track. |
| `acceptedNameUsage` / `acceptedNameUsageID` | The name a specific TaxonConcept currently treats as valid. | On a record that documents the accepted usage itself, this is self-referential (points to the record's own name/ID). On a synonym record, it points to the accepted usage's ID. |
| `parentNameUsage` | The next-higher taxon in the classification the current TaxonConcept places this name under (typically the genus, for a species-group name). | Reflects the *current* combination (post new-combination acts), not the original one — this is exactly the field that changes when Art. 48 fires, while `originalNameUsage` does not. |

## Rank, status, and remarks

| DwC term | Note |
|---|---|
| `taxonRank` | The rank as currently applied by the cited TaxonConcept. Because rank-within-group can be raised or lowered without a new nomenclatural act ([Art. 23.3.1](https://code.iczn.org/validity-of-names-and-nomenclatural-acts/article-23-principle-of-priority/#art-23-3-1)), this is a TaxonConcept-layer value, not fixed on the Name. |
| `verbatimTaxonRank` | The rank exactly as given in the source record before normalization — keep it distinct from `taxonRank` whenever the source uses non-standard rank terms (e.g. "natio", "aberration" — see [Art. 45.6](https://code.iczn.org/species-group-nominal-taxa-and-their-names/article-45-the-species-group/#art-45-6) on how such terms determine infrasubspecific vs. subspecific rank). |
| `taxonomicStatus` | See the worked table above. |
| `taxonRemarks` | Free text — the right place for anything that does not fit a controlled field: which Opinion resolved a case, that a spelling is a misspelling in common use, that a reversal-of-precedence act is pending Commission review. |

## Type specimen fields

| DwC term | Note |
|---|---|
| `typeStatus` | A concatenated list of "type status of typified name, publication" (e.g. `holotype of Aus bus Smith, 1850`). Cite the type status against the name **as originally established**, per [Art. 61.1](https://code.iczn.org/the-type-concept-in-nomenclature/article-61-principle-of-typification/#art-61-1) — the name-bearing type belongs to the nominal taxon fixed at establishment, not to whichever combination happens to be current. For the categories themselves (holotype, syntype, lectotype, paralectotype, neotype) and how one converts into another over time, see `references/16-species-group-types.md` and `references/data-modeling.md` §3.8 (type category is a function of the latest valid type-fixation act, never a static specimen attribute). |
| `typifiedName` | The scientific name the specimen is the type of — again the original-combination name, for the same reason. |

## Atomized name fields and the Art. 51.3 reassembly problem

`genus`, `subgenus`, `specificEpithet`, `infraspecificEpithet` decompose a name into parts convenient for filtering and reporting. Reassembling `scientificName` from these parts is lossy for exactly the case this skill exists to flag: the parenthesization of `scientificNameAuthorship` depends on whether `genus` differs from the name's *original* combination genus ([Art. 51.3](https://code.iczn.org/authorship/article-51-citation-of-names-of-authors/#art-51-3)) — a fact that is not present anywhere in the atomized fields themselves unless `originalNameUsage` is also populated and compared. A pipeline that concatenates `genus + " " + specificEpithet + " " + scientificNameAuthorship` and always wraps the authorship in parentheses (or never does) will get roughly half of any dataset with transferred species wrong. Store (or derive at read time) a same-as-original-combination boolean alongside the atomized fields if `scientificNameAuthorship` is generated rather than curated.

## GBIF practical notes

GBIF's Backbone Taxonomy normalizes the free-text `taxonomicStatus` values found in source datasets into a fixed internal enumeration (`org.gbif.api.vocabulary.TaxonomicStatus`): `ACCEPTED`, `DOUBTFUL`, `SYNONYM`, `HOMOTYPIC_SYNONYM`, `HETEROTYPIC_SYNONYM`, `PROPARTE_SYNONYM`, `MISAPPLIED`, `AMBIGUOUS_SYNONYM`, `PROVISIONALLY_ACCEPTED`. Note `HOMOTYPIC_SYNONYM`/`HETEROTYPIC_SYNONYM` are GBIF's own labels for what this skill calls objective/subjective synonymy (`references/data-modeling.md` §3.3) — the botanical terms "homotypic"/"heterotypic" are being reused across codes by GBIF's tooling, not by the ICZN Code itself, which uses "objective"/"subjective". GBIF's `NomenclaturalStatus` enumeration (`org.gbif.api.vocabulary.NomenclaturalStatus`) is explicitly cross-code (zoology and botany share one vocabulary in GBIF's tooling) and includes zoology-specific values such as `NUDUM` (nomen nudum), `FORGOTTEN` (nomen oblitum), `PROTECTED` (nomen protectum), `CONSERVED`, `REJECTED`, and `REPLACEMENT` alongside purely botanical values (`ILLEGITIMATE`, `SUPERFLUOUS`) that have no ICZN meaning — do not assume every value in a GBIF-derived `nomenclaturalStatus` column is applicable to, or was correctly assigned under, the zoological Code. These are properties of GBIF's own backbone processing, not part of the Darwin Core standard itself; verify against a specific GBIF dataset export before relying on exact token spelling in a new pipeline.

## Worked example

Illustrative only — fictional taxon names in the Code's own `Aus`/`Bus` convention, not a real species, chosen to show every field interacting.

**History:** *Aus bus* Smith, 1850 was described in genus *Aus*. Jones (1900) transferred it to genus *Cus*, giving *Cus bus* (Smith, 1850) — a new combination ([Art. 48](https://code.iczn.org/species-group-nominal-taxa-and-their-names/article-48-change-of-generic-assignment/)), parenthesized because the genus changed ([Art. 51.3](https://code.iczn.org/authorship/article-51-citation-of-names-of-authors/#art-51-3)). In 1975, Taylor judged the older, previously unused name *Cus wus* Miller, 1820 (different name-bearing type; described directly in *Cus*) to be a **subjective senior synonym** of *Cus bus* (Art. 61.3.1) — under strict priority *Cus wus* would displace *Cus bus* as the valid name. Because *Cus bus* was in prevailing use but the mechanical 25-works/10-authors/50-year test of [Art. 23.9.1](https://code.iczn.org/validity-of-names-and-nomenclatural-acts/article-23-principle-of-priority/#art-23-9-1) was not clearly met, Taylor referred the case to the Commission ([Art. 23.9.3](https://code.iczn.org/validity-of-names-and-nomenclatural-acts/article-23-principle-of-priority/#art-23-9-3)) rather than self-applying a reversal of precedence. The Commission's Opinion 2000 (1980) conditionally suppressed *Cus wus* Miller, 1820 under the plenary power ([Art. 81.2.3](https://code.iczn.org/the-international-commission-on-zoological-nomenclature/article-81-use-of-the-plenary-power/#art-81-2-3)), giving *Cus bus* (Smith, 1850) precedence; the ruling took effect on publication ([Art. 80.3](https://code.iczn.org/the-international-commission-on-zoological-nomenclature/article-80-status-of-actions-of-the-commission/#art-80-3)).

**Accepted-usage record:**

| Field | Value |
|---|---|
| `scientificName` | Cus bus |
| `scientificNameAuthorship` | (Smith, 1850) |
| `genus` | Cus |
| `specificEpithet` | bus |
| `taxonRank` | species |
| `namePublishedIn` | Smith, 1850 [original description, in genus *Aus*] |
| `namePublishedInYear` | 1850 |
| `nomenclaturalCode` | ICZN |
| `originalNameUsage` / `originalNameUsageID` | Aus bus Smith, 1850 |
| `acceptedNameUsage` / `acceptedNameUsageID` | Cus bus (Smith, 1850) [self] |
| `parentNameUsage` | Cus |
| `taxonomicStatus` | accepted |
| `nomenclaturalStatus` | conserved (precedence given by ICZN Opinion 2000, Art. 81.2.3) |
| `taxonRemarks` | Transferred from *Aus* to *Cus* by Jones (1900); given precedence over senior subjective synonym *Cus wus* Miller, 1820 by ICZN Opinion 2000 (1980) |

**Suppressed senior-synonym record:**

| Field | Value |
|---|---|
| `scientificName` | Cus wus |
| `scientificNameAuthorship` | Miller, 1820 |
| `genus` | Cus |
| `specificEpithet` | wus |
| `taxonRank` | species |
| `namePublishedInYear` | 1820 |
| `nomenclaturalCode` | ICZN |
| `originalNameUsage` / `originalNameUsageID` | Cus wus Miller, 1820 [never transferred — original combination] |
| `acceptedNameUsage` / `acceptedNameUsageID` | Cus bus (Smith, 1850) |
| `taxonomicStatus` | synonym (subjective senior synonym per Taylor, 1975) |
| `nomenclaturalStatus` | conditionally suppressed (ICZN Opinion 2000, Art. 81.2.3) |
| `taxonRemarks` | Remains an available name (Art. 10.6) despite suppression; suppression is conditional — usable again as valid if the taxa are later regarded as distinct (Art. 81.2.3.1) |

**Type-specimen record (attached to Smith's original material, not to the current combination):**

| Field | Value |
|---|---|
| `typeStatus` | holotype of Aus bus Smith, 1850 |
| `typifiedName` | Aus bus Smith, 1850 |

Note every occurrence of the type fields cites the **original** combination (*Aus bus*), never the current one (*Cus bus*) — exactly the Art. 61.1/Art. 51.3 distinction this whole file exists to keep straight.
