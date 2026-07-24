---
name: DataProvenance
description: >
  Provides comprehensive technical knowledge about the W3C PROV standard for
  documenting data provenance: the PROV-DM conceptual model (Entity,
  Activity, Agent and their relations), PROV-O (the RDF/OWL2 ontology),
  PROV-N (the human-readable notation), PROV-XML (the XML serialization),
  and the PROV-DM Primer's worked examples. Use when the user mentions
  "PROV", "W3C PROV", "provenance", "data provenance", "PROV-O", "PROV-DM",
  "PROV-N", "PROV-XML", "wasGeneratedBy", "wasDerivedFrom",
  "wasAttributedTo", "wasAssociatedWith", needs to document the lineage of a
  dataset/entity, model who/what produced or transformed a piece of data, or
  serialize provenance metadata as RDF/Turtle/XML.
license: MIT
metadata:
  author: biodiversityDataSkills
  repository: https://github.com/edalcin/biodiversityDataSkills
  source: https://www.w3.org/TR/prov-overview/
---

# DataProvenance

Reference knowledge base for the [W3C PROV](https://www.w3.org/TR/prov-overview/)
family of specifications — the standard model for documenting **data
provenance**: which entities, activities, and agents produced, used,
transformed, or are responsible for a piece of data or thing, so its
quality, reliability, and trustworthiness can be assessed. Built from the
official W3C Recommendations and Notes (2013-04-30).

This is a pure reference skill — no scripts, no dependencies. Read the
relevant file(s) below before answering non-trivial PROV questions or
producing provenance records for a dataset.

## What PROV is

PROV models provenance with three core types — **Entity** (a thing:
document, dataset, chart, ...), **Activity** (something that occurs over
time and acts on/with entities: computing, transforming, publishing, ...),
and **Agent** (something responsible: a person, organization, or software)
— connected by relations such as `wasGeneratedBy`, `used`, `wasDerivedFrom`,
`wasAttributedTo`, and `wasAssociatedWith`. Every PROV term, regardless of
which document defines it or which serialization you use, lives in the
**same namespace**: `http://www.w3.org/ns/prov#` (prefix `prov:`).

## Quick reference — where to look

| Topic | File |
|---|---|
| Roadmap of the whole PROV family, which document to read for what, namespace | [references/OVERVIEW.md](references/OVERVIEW.md) |
| **Start here for a new provenance scenario** — intuitive, example-driven walkthrough (entities, activities, usage/generation, agents/responsibility, roles, derivation/revision, plans, time, alternate/specialization) with worked PROV-N + Turtle snippets | [references/PRIMER.md](references/PRIMER.md) |
| **Normative core model** — exact definitions, optional arguments, and cardinality for every PROV-DM type and relation (Entity/Activity/Agent, Generation, Usage, Communication, Start, End, Invalidation, Derivation + Revision/Quotation/PrimarySource, Attribution, Association, Delegation, Influence, Bundles, Alternate/Specialization, Collections, attributes, extensibility) | [references/DATA_MODEL.md](references/DATA_MODEL.md) |
| **RDF/OWL2 ontology** — for serializing provenance as Turtle/RDF/JSON-LD: Starting Point / Expanded / Qualified term tiers, every `prov:` class and property, the qualification pattern (attaching time/role/plan to a relation) | [references/PROV_O.md](references/PROV_O.md) |
| **Human-readable notation** — exact functional-style syntax (`entity(id, [...])`, `wasGeneratedBy(id; e, a, t, attrs)`) used in every PROV example, incl. the `-`/`;` optional-argument conventions | [references/PROV_N.md](references/PROV_N.md) |
| **XML serialization** — XSD element/attribute mapping for XML-native pipelines, worked `<prov:document>` example | [references/PROV_XML.md](references/PROV_XML.md) |
| Glossary of PROV terms | [references/GLOSSARY.md](references/GLOSSARY.md) |

## Core concepts an agent must get right

- **Three core types, one namespace.** `Entity`, `Activity`, `Agent` are the
  whole model's anchor; every relation connects two of them. Don't invent a
  fourth top-level type — model anything else (a Plan, a Collection, a
  Bundle) as a typed Entity via `prov:type`.
- **Relations are directional and named for the *effect*, not the actor.**
  `wasGeneratedBy(entity, activity)`, not the other way round; `used(activity,
  entity)`. Read the exact argument order in [DATA_MODEL.md](references/DATA_MODEL.md)
  or [PROV_N.md](references/PROV_N.md) before writing a relation — getting
  subject/object backwards is the most common modeling error.
- **`wasDerivedFrom` has three named specializations**: `wasRevisionOf` (new
  version, substantial original content retained), `wasQuotedFrom` (copied
  part/all of the original), `hadPrimarySource` (secondary material citing
  its firsthand origin). Prefer the specific one when it applies; in
  PROV-DM/PROV-N these are expressed via `prov:type` on a `wasDerivedFrom`,
  in PROV-O they are distinct sub-properties.
- **Attribution is a shortcut, not a substitute for Association.** `entity
  wasAttributedTo agent` says "some activity associated with this agent
  generated this entity" without naming the activity. If the activity is
  known, prefer `activity wasAssociatedWith agent` + `entity wasGeneratedBy
  activity` — more precise and queryable.
- **Qualification adds attributes to a relation, not to an entity/activity.**
  Plain `prov:wasGeneratedBy` is a bare RDF triple — it cannot carry a
  `role` or exact `time`. To say *when* or *in what role*, use the
  `prov:qualifiedGeneration` / `prov:Generation` pattern (or the
  richer PROV-N argument list — PROV-N's `wasGeneratedBy(id; e, a, t,
  attrs)` already carries time/attrs without needing qualification). See
  [PROV_O.md#qualified-terms](references/PROV_O.md#qualified-terms).
- **Specialization ≠ Alternate.** `specializationOf` is asymmetric and
  implies strict containment (all aspects of the general entity, plus
  more, plus a shorter-or-equal lifetime — e.g. a dated version of a page
  vs. the page's generic URI). `alternateOf` is symmetric and deliberately
  weak (two entities are "about" the same thing, no refinement implied).
  Don't conflate them.
- **Provenance of provenance uses Bundles**, not a special relation. A
  `prov:Bundle` is itself an `Entity`, so its own `wasGeneratedBy`,
  `wasAttributedTo`, etc. describe who asserted a set of provenance
  records and when — the same vocabulary, applied recursively.
- **Pick the serialization to match the target system**, not personal
  preference: RDF triple store / SPARQL / Linked Data catalog → PROV-O
  (Turtle/RDF/JSON-LD); XML-native pipeline / XSD-validated exchange →
  PROV-XML; documentation, examples, or a quick sketch for a human reader →
  PROV-N. All three losslessly round-trip through the same PROV-DM model.

## When answering PROV questions

1. New scenario, unsure where to start → read [PRIMER.md](references/PRIMER.md)
   first to build intuition from its worked example, then confirm exact
   argument/cardinality rules in [DATA_MODEL.md](references/DATA_MODEL.md).
2. "What's the precise definition/optional arguments of relation X?" →
   [DATA_MODEL.md](references/DATA_MODEL.md) — don't guess; PROV relations
   have specific optional-argument sets (e.g. `wasAssociatedWith` accepts
   an optional `plan`, `wasDerivedFrom` accepts optional `activity`,
   `generation`, and `usage` references).
3. "Write this as RDF/Turtle/JSON-LD" → [PROV_O.md](references/PROV_O.md);
   check whether the relation needs qualification before reaching for a
   qualified form (only needed when an attribute must attach to the
   relation itself, e.g. a role or precise time not already covered by a
   direct datatype property like `prov:generatedAtTime`).
4. "Write this as PROV-N" (for documentation, a spec example, or a quick
   human-readable sketch) → [PROV_N.md](references/PROV_N.md) for exact
   functional syntax, including the `-`/`;` conventions for omitted
   optional arguments.
5. "Write this as XML" → [PROV_XML.md](references/PROV_XML.md) for the
   element/attribute mapping and a full worked `<prov:document>` example.
6. Term-only lookup → [GLOSSARY.md](references/GLOSSARY.md).

## Interoperability with other skills in this repo

- **darwin-core** — document the lineage of a Darwin Core Archive or
  Darwin Core Data Package: which `Activity` (an import, a georeferencing
  pass, a QC step) generated/transformed which occurrence records, and
  which `Agent` (collector, data manager, institution) is responsible. Model
  the dataset/record as a `prov:Entity` and reuse `dwc:` terms as PROV-O
  attributes alongside `prov:` properties in the same Turtle graph.
- **skos-xl** — the Traditional Knowledge (CTA) vocabulary template already
  uses `prov:wasAttributedTo` / `prov:Agent` for per-label attribution and
  CARE-principle provenance; this skill is the normative reference for that
  usage (roles, qualification, `prov:hadPrimarySource` for citing an
  originating knowledge holder) if a deeper provenance trail is needed than
  the template covers.
