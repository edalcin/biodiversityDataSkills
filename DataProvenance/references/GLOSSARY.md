# PROV Glossary

Source: distilled from [DATA_MODEL.md](DATA_MODEL.md) (PROV-DM), [PROV_O.md](PROV_O.md), and [PROV_N.md](PROV_N.md) — see those files for full normative definitions.

- **Activity** — something that occurs over a period of time and acts upon or
  with entities; may consume, process, transform, modify, relocate, use, or
  generate entities. See [DATA_MODEL.md#2-core-types](DATA_MODEL.md#2-core-types).
- **Agent** — something that bears some form of responsibility for an
  activity taking place, for an entity's existence, or for another agent's
  activity. Sub-kinds: **Person**, **Organization**, **SoftwareAgent**.
- **Association** (`wasAssociatedWith`) — assignment of responsibility to an
  Agent for an Activity, optionally naming the **Plan** it followed.
- **Attribution** (`wasAttributedTo`) — ascribing an Entity to an Agent
  (shorthand for "some activity associated with this agent generated this
  entity").
- **Bundle** — a named set of provenance descriptions, itself an Entity — the
  mechanism for **provenance of provenance** (who asserted this provenance,
  and when). See [DATA_MODEL.md#4-component-4-bundles-54](DATA_MODEL.md#4-component-4-bundles-54).
- **Collection** — an Entity that structures other Entities (its
  **members**); membership is expressed with `hadMember`.
- **Communication** (`wasInformedBy`) — an Activity depends on another via
  some unspecified Entity the first generated and the second used.
- **Delegation** (`actedOnBehalfOf`) — an Agent (delegate) acts with
  authority granted by another Agent (responsible), who retains some
  responsibility for the outcome.
- **Derivation** (`wasDerivedFrom`) — an Entity transformed, updated, or
  constructed from a pre-existing one. Sub-kinds: **Revision** (substantial
  content preserved from the original), **Quotation** (copying part/all of
  an entity), **Primary Source** (secondary material citing its
  firsthand/primary origin).
- **Entity** — a physical, digital, conceptual, or other kind of thing with
  some fixed aspects; may be real or imaginary.
- **Generation** (`wasGeneratedBy`) — completion of production of a new
  Entity by an Activity; instantaneous, the entity did not exist before it.
- **Identifier** — a qualified name uniquely naming an Entity, Activity, or
  Agent (mandatory), or optionally naming a relation instance so it can be
  referenced/qualified elsewhere.
- **Influence** (`wasInfluencedBy`) — the generic dependency of one thing on
  another; every core relation (Generation, Usage, Derivation, Attribution,
  Association, Delegation, ...) is also an Influence. Prefer the specific
  relation; Influence exists mainly to support querying.
- **Invalidation** (`wasInvalidatedBy`) — start of destruction, cessation, or
  expiry of an existing Entity by an Activity; the entity is no longer
  usable afterward.
- **Plan** — an Entity representing a set of actions/steps intended by one or
  more Agents to achieve a goal; the optional third argument of Association.
- **PROV-DM** — the core, technology-agnostic conceptual data model for
  provenance. See [DATA_MODEL.md](DATA_MODEL.md).
- **PROV-N** — the human-readable functional-style notation (`entity(...)`,
  `wasGeneratedBy(...)`) used for examples throughout the PROV family. See
  [PROV_N.md](PROV_N.md).
- **PROV-O** — the OWL2 ontology mapping PROV-DM to RDF (namespace
  `http://www.w3.org/ns/prov#`, prefix `prov:`). See [PROV_O.md](PROV_O.md).
- **PROV-XML** — the XML Schema (XSD) serialization of PROV-DM. See
  [PROV_XML.md](PROV_XML.md).
- **Qualification / Qualified relation** — the PROV-O pattern (`prov:qualifiedX`
  / `prov:X` class) that restates a binary relation (e.g. `wasGeneratedBy`)
  as an intermediate resource so extra attributes (time, role, plan,
  location) can be attached to the relation itself, not just its endpoints.
  See [PROV_O.md#qualified-terms](PROV_O.md#qualified-terms).
- **Role** (`prov:role` / `prov:hadRole`) — the function an Entity or Agent
  assumed with respect to an Activity, in the context of a usage,
  generation, invalidation, association, start, or end.
- **Specialization** (`specializationOf`) vs. **Alternate** (`alternateOf`)
  — two ways of relating Entities about the same underlying thing.
  Specialization is asymmetric/strict containment (all aspects of the
  general entity, plus more, plus a shorter-or-equal lifetime); Alternate is
  symmetric and weak (both entities are "about" the same thing, no
  refinement implied). See [DATA_MODEL.md#5-component-5-alternate-entities-55](DATA_MODEL.md#5-component-5-alternate-entities-55).
- **Start** (`wasStartedBy`) / **End** (`wasEndedBy`) — an Activity is
  deemed started/ended by a triggering Entity.
- **Usage** (`used`) — the beginning of utilizing an Entity by an Activity;
  instantaneous, before which the activity could not have been affected by
  the entity.
- **Value** — a constant (string, number, time, qualified name, IRI, binary
  data) attached via an attribute (e.g. `prov:value`), whose interpretation
  is outside PROV's scope.
