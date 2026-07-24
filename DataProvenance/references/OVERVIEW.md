# PROV-Overview: An Overview of the PROV Family of Documents

Source: [PROV-Overview (W3C Working Group Note, 2013-04-30)](https://www.w3.org/TR/2013/NOTE-prov-overview-20130430/)

## What PROV is

**Provenance** is information about entities, activities, and people involved
in producing a piece of data or thing, which can be used to form assessments
about its quality, reliability, or trustworthiness. **PROV** is the W3C
family of specifications that enables the wide publication and interchange
of provenance on the Web and in other information systems, using formats
such as RDF and XML, plus definitions for accessing, validating, and mapping
provenance to Dublin Core. "PROV" always refers to the *entire family* of
documents below, not any single one.

PROV's design responds to 8 broad recommendations from the W3C Provenance
Incubator Group: support the core concepts of identifying an object,
attributing it to a person/entity, and representing processing steps;
accessing provenance expressed in other standards; accessing provenance;
provenance of provenance; reproducibility; versioning; representing
procedures; and representing derivation.

## Namespace

Every term defined anywhere in PROV lives in **one** namespace, regardless
of which document defines it:

```
http://www.w3.org/ns/prov#
```

Conventional prefix: **`prov`**. `prov:Entity`, `prov:wasGeneratedBy`, etc.
are the same terms whether you got there via PROV-O, PROV-N, or PROV-XML.

## Document roadmap

PROV consists of 12 documents. You do **not** need to read all of them —
each targets one of three audiences, and the family is designed so a
newcomer starts at Part 1 and only goes deeper as needed. This skill covers
the six most load-bearing ones (marked ✅); the rest are linked for
completeness.

| # | Audience | Type | Document | Purpose |
|---|---|---|---|---|
| 1 | Users | Note | ✅ [PRIMER.md](PRIMER.md) (PROV-PRIMER) | Entry point to PROV — an intuitive introduction to the data model. Start here; for many use cases it's the only document needed. |
| 2 | Developers | Rec | ✅ [PROV_O.md](PROV_O.md) (PROV-O) | Lightweight OWL2 ontology mapping PROV-DM to RDF. For Linked Data / Semantic Web / SPARQL use. |
| 3 | Developers | Note | ✅ [PROV_XML.md](PROV_XML.md) (PROV-XML) | XML Schema (XSD) serialization of PROV-DM, for XML-native pipelines. |
| 4 | Advanced | Rec | ✅ [DATA_MODEL.md](DATA_MODEL.md) (PROV-DM) | The conceptual data model itself (with UML diagrams in the original). PROV-O, PROV-XML, and PROV-N are all serializations *of* this model. |
| 5 | Advanced | Rec | ✅ [PROV_N.md](PROV_N.md) (PROV-N) | Human-readable functional-style notation for the model; used for examples throughout the other PROV documents. |
| 6 | Advanced | Rec | PROV-CONSTRAINTS | Constraints defining what counts as *valid* provenance; aimed at implementors of validators. Not bundled in this skill — consult [the spec](https://www.w3.org/TR/2013/REC-prov-constraints-20130430/) directly if you need to build a validator. |
| 7 | Developers | Note | PROV-AQ | Web-based mechanisms (HTTP headers/links, service description) to locate and retrieve provenance for a given resource. |
| 8 | Developers | Note | PROV-DC | Mapping between Dublin Core Terms and PROV-O. |
| 9 | Developers | Note | PROV-DICTIONARY | Constructs for the provenance of dictionary-style (key→entity) data structures — a specific kind of `prov:Collection`. |
| 10 | Advanced | Note | PROV-SEM | Declarative first-order-logic semantics of PROV-DM. |
| 11 | Advanced | Note | PROV-LINKS | Extensions for linking provenance across separate bundles. |
| 12 | — | Note | PROV-Overview (this document) | The roadmap you're reading. |

## How to use this roadmap when documenting provenance

1. **Modeling a new provenance scenario in prose/diagrams?** Read
   [PRIMER.md](PRIMER.md) — it walks a single running example through every
   core concept with PROV-N and Turtle snippets.
2. **Need the precise, load-bearing definition of a relation or type**
   (exact optional attributes, cardinality, what's a specialization of
   what)? Go straight to [DATA_MODEL.md](DATA_MODEL.md) — the normative
   source; PRIMER.md is intentionally looser.
3. **Serializing as RDF/Turtle/JSON-LD** (triple stores, SPARQL, Linked
   Data, most modern metadata catalogs) → [PROV_O.md](PROV_O.md).
4. **Serializing as XML** (legacy pipelines, XSD-validated exchange) →
   [PROV_XML.md](PROV_XML.md).
5. **Writing or reading the compact human-readable notation used in specs
   and examples** (not for storage — for documentation/debugging) →
   [PROV_N.md](PROV_N.md).
6. **Terminology check** → [GLOSSARY.md](GLOSSARY.md).

See also [SKILL.md](../SKILL.md) for the condensed cheat sheet and decision
guide.
