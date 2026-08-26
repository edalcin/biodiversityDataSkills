# ZooBank, Electronic Publication, and LSIDs

Source: https://code.iczn.org/criteria-of-publication/article-8-what-constitutes-published-work/ · https://code.iczn.org/criteria-of-publication/article-9-what-does-not-constitute-published-work/ · https://code.iczn.org/date-of-publication/article-21-determination-of-date/ · https://code.iczn.org/the-international-commission-on-zoological-nomenclature/article-78-powers-and-duties-of-the-commission/ · 4th edition 1999, as amended 2012

A name published only in an electronic work that fails to satisfy Art. 8.5 is not merely "informal" — it is **unavailable**: it does not exist as a zoological name at all, and every downstream act (combinations, synonymies, type designations) built on it is void. This is the single most consequential trap in modern zoological nomenclature and it is fallen into every year by authors who register after acceptance instead of before publication, or who assume a DOI substitutes for a ZooBank record. This file exists to make the trap visible to both authors and data managers.

## The 2012 amendment

The Commission adopted "Amendment of Articles 8, 9, 10, 21 and 78 ... to expand and refine methods of publication," formally published 4 September 2012 with an effective date of **1 January 2012**. It applies to works issued from that date forward; works issued before 2012 are judged under the pre-2012 text of these Articles. It:

- rewrote **Art. 8.1.3** and **Art. 8.5** to define, for the first time, the conditions under which a work distributed only in electronic form is "published" within the meaning of the Code, and created the Official Register of Zoological Nomenclature (**ZooBank**) as the mechanism for it;
- rewrote **Art. 9** to add exclusions specific to electronic and hybrid distribution (advance online versions, raw web-signal distribution not meeting Art. 8);
- rewrote **Art. 10** (Recommendation 10B) to encourage — not require — registration of names from conventional print works;
- rewrote **Art. 21** to state how the date of an electronic work is fixed, including the "online first" problem;
- rewrote **Art. 78.2.4** to give the Commission the power to establish and maintain ZooBank.

Two further Declarations amended these same Articles' neighborhood after 2012 — see `references/glossary.md` for Declaration 44 (Art. 74.7.3) and Declaration 46 (Art. 8.8 + Glossary "retraction"), which are adjacent but not part of the 2012 amendment itself.

## Art. 8.1 — the general conditions (apply to every work, print or electronic)

Before Art. 8.5 is even reached, a work must meet the general Art. 8.1 criteria: issued for a public and permanent scientific record (Art. 8.1.1), obtainable free or by purchase when first issued (Art. 8.1.2), and produced in an edition of simultaneously obtainable copies by a method assuring EITHER:

- **8.1.3.1** — numerous identical and durable copies (the traditional print criterion, detailed in Art. 8.4), OR
- **8.1.3.2** — widely accessible electronic copies with fixed content and layout (the Code's own Example names PDF/A, ISO 19005-1:2005, as a format that qualifies; an editable web page or a PDF that can be silently altered does not).

[Art. 8.1](https://code.iczn.org/criteria-of-publication/article-8-what-constitutes-published-work/#art-8-1)

## Article 8.5 — conditions for a work "issued and distributed electronically" to be published

This is the operative Article and its three conditions are **conjunctive** — all three must be met, on top of Art. 8.1, for an electronic-only work to be published within the meaning of the Code:

- **8.5.1** — the work must have been issued after 2011 (i.e., from 2012 onward; an electronic-only work from before 2012 cannot be validated under this route at all). [Art. 8.5.1](https://code.iczn.org/criteria-of-publication/article-8-what-constitutes-published-work/#art-8-5)
- **8.5.2** — the work must state its date of publication in the work itself.
- **8.5.3** — the work must be registered in ZooBank (Art. 78.2.4) **before** it is published, and must contain evidence in the work itself that this registration occurred (e.g., the registration number, or an embedded hyperlink to the ZooBank record — even one invisible in normal viewing/printing counts, per the Code's own Example).
  - **8.5.3.1** — the ZooBank entry itself (not the work) must name an archiving organization, other than the publisher, and its Internet address, capable of permanently preserving the work's content and layout.
  - **8.5.3.2** — the ZooBank entry itself (not the work) must carry an ISBN for the work or an ISSN for the journal.
  - **8.5.3.3** — a stated error in the evidence of registration does not by itself make the work unavailable, provided the work can be unambiguously matched to a ZooBank record that was created *before* the work was published. Registering only *after* the fact is fatal even if the author intended to register earlier — the Code's own Example is exactly this case: date-stamped for same-day registration, actually registered later, held unavailable.

[Art. 8.5](https://code.iczn.org/criteria-of-publication/article-8-what-constitutes-published-work/#art-8-5)

**What goes where, precisely:** the *work* must carry the date of publication (8.5.2) and some form of evidence that registration happened (8.5.3) — typically the registration number or LSID. The *ZooBank record* (not the work) is where the archive name/URL (8.5.3.1) and the ISBN/ISSN (8.5.3.2) live. Confusing these two — e.g., assuming the ISSN must appear printed in the paper — is a common misreading.

**Recommendation 8C** (advisory, not mandatory): electronic works should be structured for automated indexing/data extraction and should carry actionable hyperlinks to the ZooBank record. **Recommendation 8H** (advisory): authors are encouraged to archive with more than one organization.

## Article 9 — what electronic material never counts as published, even after the amendment

Independently of Art. 8.5, Art. 9 excludes several classes of electronic material outright:

- **9.9** — preliminary versions of a work accessible electronically in advance of the final publication (see Art. 21.8.3 below) — an "online first"/"in press" proof is not published.
- **9.11** — text or illustrations distributed by electronic signals (e.g. via the Internet) generally, **except** those that fulfil Arts. 8.1 and 8.5 — i.e., a bare web page, blog post, or PDF that doesn't meet the Art. 8.5 conditions is unpublished no matter how widely it circulates.
- **9.12** — facsimiles or reproductions obtained on demand of an unpublished work remain unpublished (this rule predates 2012 but is routinely relevant to digitized theses and reports offered print-on-demand).

[Art. 9](https://code.iczn.org/criteria-of-publication/article-9-what-does-not-constitute-published-work/)

## Article 21.8–21.9 — dating an electronic work, and the "online first" trap

- **21.7.2** — an electronic work is *required* to state a date of publication (this is the same obligation as Art. 8.5.2, cross-referenced).
- **21.8.3** — advance electronic access to a preliminary version does **not** advance the date of publication, because such a preliminary version is itself unpublished under Art. 9.9. The date is fixed only when the final version meeting Art. 8/Art. 9 appears.
- **21.9** — when a work is issued in both print and electronic editions, the date of publication is that of whichever edition *first* satisfies Art. 8 and is not excluded by Art. 9. In practice: if the electronic edition is registered in ZooBank and dated before the print run ships, the electronic date wins, and vice versa — the two editions are not assumed to share a date just because they share content.

[Art. 21.8](https://code.iczn.org/date-of-publication/article-21-determination-of-date/#art-21-8) · [Art. 21.9](https://code.iczn.org/date-of-publication/article-21-determination-of-date/#art-21-9)

**Practical warning:** a manuscript's "Accepted" date, "Online first"/"Early view" date, and final issue/DOI-minting date are frequently three different dates. Under Art. 21.8.3 only the version that actually satisfies Art. 8.5 in full (dated, registered before publication, evidence present) fixes the nomenclatural date — an early-view PDF lacking a ZooBank registration number is not yet a published work at all, regardless of what date is printed on it.

## LSIDs — what they are and how to record them

ZooBank identifies its records with Life Science Identifiers (LSIDs), a URN scheme. The two namespaces that matter for nomenclatural citation are:

- `urn:lsid:zoobank.org:pub:<UUID>` — identifies the **publication** (the work as a whole).
- `urn:lsid:zoobank.org:act:<UUID>` — identifies a **nomenclatural act** within that work (e.g., the original description that establishes a new name, or another act such as a lectotype designation). This is the record that actually carries the established name and its type information.

ZooBank also assigns LSIDs to **author** records (`urn:lsid:zoobank.org:author:<UUID>`) and to provisionally-registered **type specimen** records (`urn:lsid:zoobank.org:specimen:<UUID>`), but these are not required by Art. 8.5 and are not treated further here. There is no separate top-level LSID for "a scientific name" as a bare string — the name is carried as an attribute of the `act` record that established it.

LSIDs resolve through ZooBank, typically presented as `https://zoobank.org/` followed by the bare LSID (e.g. `https://zoobank.org/urn:lsid:zoobank.org:pub:<UUID>` — some tools also render this as `zoobank.org/References/<UUID>` for a publication). A resolvable LSID is a machine-checkable claim; a free-text citation is not.

**Database use:** record the `act` LSID (or, if the act was not separately registered, the `pub` LSID) as the value of Darwin Core `namePublishedInID` and/or `nameAccordingToID`; some implementations also populate `scientificNameID` with it. See `references/dwc-mapping.md` for the full field mapping and the rationale for preferring a resolvable identifier over a citation string.

## Checklist — an author about to publish a new name electronically

1. **Before** submitting the final version for publication, register the work in ZooBank and obtain its `pub` LSID/registration number. Registration must occur before the work is published, not after (Art. 8.5.3, and see the inadmissible-error Example under 8.5.3.3).
2. Register the nomenclatural act(s) within the work (the new name(s), any other acts) to obtain `act` LSIDs.
3. In the ZooBank record, supply the ISBN/ISSN (Art. 8.5.3.2) and the name and URL of an archiving organization other than the publisher (Art. 8.5.3.1).
4. In the manuscript itself, state the intended date of publication (Art. 8.5.2) and print or embed the registration evidence — the registration number, and/or an embedded hyperlink to the ZooBank record (Art. 8.5.3).
5. Confirm the file format assures fixed content and layout (e.g., PDF/A) so it satisfies Art. 8.1.3.2, and confirm the work is not a preliminary/advance version excluded by Art. 9.9.
6. If the work will also appear in print, decide (or determine) which edition satisfies Art. 8/Art. 9 first — that edition fixes the date under Art. 21.9.
7. Advisory (Rec. 8A, 8C, 8H, not mandatory): notify the Zoological Record, structure the electronic file for automated indexing, and consider a second archiving organization for redundancy.

## Checklist — a data manager receiving a recently published name

1. Determine whether the original description is print or electronic-only. If print (and satisfies Art. 8.1/8.4), ZooBank registration was never legally required — skip to normal availability checks (`references/04-availability.md`).
2. If electronic and dated 2012 or later, look in the work for a stated ZooBank registration number or LSID.
3. If found, resolve it at zoobank.org and confirm (a) the record exists, (b) it predates the work's stated publication date, and (c) it corresponds to this work/act.
4. If no registration evidence is stated in the work, or the LSID does not resolve, or the ZooBank record postdates publication — the name's availability under Art. 8.5.3 is in doubt. Flag the record rather than silently accepting it; check whether Art. 8.5.3.3's error-tolerance clause plausibly applies (an unambiguous pre-publication record exists despite a stated error) before concluding the name is unavailable.
5. Registration alone does not establish availability: the name must still independently satisfy the substantive requirements of Arts. 11–20 (`references/11-authorship.md` onward). Do not treat "has a ZooBank number" as sufficient.
6. Store the resolved `pub`/`act` LSID(s) as the identifier for the publication/act, per `references/dwc-mapping.md`.

## What is NOT required

- Conventional print works satisfying Art. 8.1 and Art. 8.4.1 have never needed ZooBank registration to be available — Art. 8.5's registration requirement applies only to works "issued and distributed electronically." Registering a print work's names is encouraged (**Rec. 10B**, advisory) but not a condition of availability.
- ZooBank registration does not, by itself, confer availability on an otherwise deficient name. Availability is governed by Art. 10.1 together with Arts. 11–20; registration is one necessary condition among several for electronic works specifically, not a substitute for the rest.
