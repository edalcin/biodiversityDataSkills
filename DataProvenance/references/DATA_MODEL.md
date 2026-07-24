# PROV-DM: The PROV Data Model

Source: [PROV-DM: The PROV Data Model (W3C Recommendation, 2013-04-30)](https://www.w3.org/TR/2013/REC-prov-dm-20130430/)

## 1. What PROV-DM is

PROV-DM is the conceptual data model that forms the basis for the W3C PROV family
of specifications. Provenance is "a record that describes the people, institutions,
entities, and activities involved in producing, influencing, or delivering a piece
of data or a thing" (§1). PROV-DM defines a **domain-agnostic** generic data model
for provenance so that heterogeneous systems can export their native provenance
into a common model, and consumers can import, process, and reason over it,
without being tied to any particular application domain — while still providing
extensibility points for domain-specific detail (§1).

### Core vs. extended structures

PROV-DM distinguishes:

- **Core structures** — the essence of provenance information, commonly found
  across domain-specific provenance vocabularies: `Entity`, `Activity`, `Agent`,
  and the seven binary relations `Generation`, `Usage`, `Communication`,
  `Derivation`, `Attribution`, `Association`, `Delegation` (§2.1, Table 2).
- **Extended structures** — enhancements/refinements of core structures for
  more advanced uses, built via four mechanisms (§2.2.1):
  - **Subtyping** — e.g. `SoftwareAgent` is a subtype of `Agent`; `Revision`
    is a subtype of `Derivation`.
  - **Expanded relations** — binary core relations are shorthands that can be
    "opened up" into richer n-ary relations with more arguments (e.g. plain
    `Association` between activity/agent expanded to also carry a `plan`).
  - **Optional identification** — an n-ary relation instance can be given its
    own identifier so it can be referred to elsewhere.
  - **Further relations** — wholly new relations not a subtype/expansion of an
    existing one (e.g. `specializationOf`, `alternateOf`).

A companion document, PROV-CONSTRAINTS, defines formal constraints on how
provenance descriptions must relate to be valid (§7); PROV-N is the human-oriented
notation used for every example in PROV-DM and throughout this reference
(reproduced in [PROV_N.md](PROV_N.md)); PROV-O is the OWL2 ontology mapping of
this model to RDF (reproduced in [PROV_O.md](PROV_O.md)).

### The six components

PROV-DM has a modular design, organized into six components (§2.3, Table 3).
Only components 1–3 contain core structures; all six contain extended structures.

| # | Component | Has core structures | About |
|---|---|---|---|
| 1 | Entities and Activities | ✔ | entities and activities, and their interrelations (the only component with time-related concepts) |
| 2 | Derivation | ✔ | derivation and its subtypes (Revision, Quotation, Primary Source) |
| 3 | Agent and Responsibility | ✔ | agents and concepts ascribing responsibility to them, plus the generic Influence relation |
| 4 | Bundles | | bundles — a mechanism to support provenance of provenance |
| 5 | Alternate | | relations linking entities that refer to the same thing |
| 6 | Collections | | collections and their membership |

Component dependencies run downward: e.g. component 5 (alternate) depends on
concepts from component 4 (bundles), itself dependent on component 1
(entity/activity) (§5, Figure 4).

---

## 2. Core types

### Entity (§5.1.1)

An **entity** is a physical, digital, conceptual, or other kind of thing with
some fixed aspects; entities may be real or imaginary.

`entity(id, [attr1=val1, ...])` in PROV-N, has:

- **id** — an identifier for an entity (mandatory).
- **attributes** — an OPTIONAL set of attribute-value pairs representing
  additional information about the fixed aspects of this entity.

Two entities are equal if they have the same identifier (§5.7.1).

```text
entity(tr:WD-prov-dm-20111215, [ prov:type="document", ex:version="2" ])
```

### Activity (§5.1.2)

An **activity** is something that occurs over a period of time and acts upon
or with entities; it may include consuming, processing, transforming,
modifying, relocating, using, or generating entities.

`activity(id, st, et, [attr1=val1, ...])` in PROV-N, has:

- **id** — an identifier for an activity (mandatory).
- **startTime** — an OPTIONAL time (`st`) for the start of the activity.
- **endTime** — an OPTIONAL time (`et`) for the end of the activity.
- **attributes** — an OPTIONAL set of attribute-value pairs about this activity.

An activity is *not* an entity — the distinction mirrors 'continuant' vs.
'occurrent' in logic.

```text
activity(a1, 2011-11-16T16:05:00, 2011-11-16T16:06:00,
  [ ex:host="server.example.org", prov:type='ex:edit' ])
```

### Agent (§5.3.1)

An **agent** is something that bears some form of responsibility for an
activity taking place, for the existence of an entity, or for another agent's
activity. An agent may itself be a particular kind of entity or activity —
i.e. the provenance of agents can itself be expressed in PROV.

`agent(id, [attr1=val1, ...])` in PROV-N, has:

- **id** — an identifier for an agent (mandatory).
- **attributes** — a set of attribute-value pairs about this agent.

```text
agent(e1, [ ex:employee="1234", ex:name="Alice", prov:type='prov:Person' ])
```

#### Agent sub-kinds (extended structures, §5.3.1)

PROV-DM defines three basic agent categories "common across most anticipated
domains of use", acknowledging they do not cover every kind of agent. All three
are expressed by subtyping (a `prov:type` attribute on `agent(...)`); **PROV
defines no attributes specific to any of them**:

| Sub-kind | Definition | `prov:type` value |
|---|---|---|
| Software Agent | Running software. | `prov:SoftwareAgent` |
| Organization | A social or legal institution such as a company, society, etc. | `prov:Organization` |
| Person | People. | `prov:Person` |

---

## 3. Core relations (Components 1–3)

The table below covers every relation defined across components 1, 2, and 3
(§5.1–§5.3). Relation names in **bold** are the seven relations explicitly
identified as core structures in §2.1/Table 2 (`Generation`, `Usage`,
`Communication`, `Derivation`, `Attribution`, `Association`, `Delegation`);
plain-text names (`Start`, `End`, `Invalidation`, `Influence`, and the
derivation subtypes) are extended structures still defined within these three
components. Unless noted otherwise, `id` and `attrs` are OPTIONAL on every row.

| Relation | PROV-N form (arguments) | Definition |
|---|---|---|
| **Generation** | `wasGeneratedBy(id; e, a, t, attrs)` — e: generated entity; a: OPTIONAL activity that created it; t: OPTIONAL generation time; attrs: OPTIONAL attribute-value pairs. At least one of id/a/t/attrs MUST be present. | The completion of production of a new entity by an activity. The entity did not exist before generation and becomes available for usage after it. Instantaneous. |
| **Usage** | `used(id; a, e, t, attrs)` — a: activity that used the entity (mandatory); e: OPTIONAL entity used; t: OPTIONAL usage time; attrs: OPTIONAL. At least one of id/e/t/attrs MUST be present. | The beginning of utilizing an entity by an activity. Before usage, the activity had not begun to utilize the entity and could not have been affected by it. Instantaneous. |
| **Communication** | `wasInformedBy(id; a2, a1, attrs)` — a2: informed activity; a1: informant activity; attrs: OPTIONAL. | The exchange of some unspecified entity by two activities, one using an entity generated by the other. Implies activity a2 depends on a1 via some unspecified entity generated by a1 and used by a2. |
| Start | `wasStartedBy(id; a2, e, a1, t, attrs)` — a2: started activity (mandatory); e: OPTIONAL trigger entity that set off the activity; a1: OPTIONAL "starter" activity that generated the trigger; t: OPTIONAL start time; attrs: OPTIONAL. At least one of id/e/a1/t/attrs MUST be present. | When an activity is deemed to have been started by an entity (the "trigger"). The activity did not exist before its start; any usage/generation/invalidation involving it follows the start. Instantaneous. |
| End | `wasEndedBy(id; a2, e, a1, t, attrs)` — a2: ended activity (mandatory); e: OPTIONAL trigger entity that terminated the activity; a1: OPTIONAL "ender" activity that generated the trigger; t: OPTIONAL end time; attrs: OPTIONAL. At least one of id/e/a1/t/attrs MUST be present. | When an activity is deemed to have been ended by an entity (the "trigger"). The activity no longer exists after its end; any usage/generation/invalidation involving it precedes the end. Instantaneous. |
| Invalidation | `wasInvalidatedBy(id; e, a, t, attrs)` — e: invalidated entity (mandatory); a: OPTIONAL activity that invalidated it; t: OPTIONAL invalidation time; attrs: OPTIONAL. At least one of id/a/t/attrs MUST be present. | The start of destruction, cessation, or expiry of an existing entity by an activity. The entity is no longer available for use (or further invalidation) afterward; any generation/usage of the entity precedes it. Instantaneous. |
| **Derivation** | `wasDerivedFrom(id; e2, e1, a, g2, u1, attrs)` — e2: generated entity; e1: used entity; a: OPTIONAL activity that used e1 and generated e2; g2: OPTIONAL generation id (for e2/a); u1: OPTIONAL usage id (for e1/a); attrs: OPTIONAL. | A transformation of an entity into another, an update of an entity resulting in a new one, or the construction of a new entity based on a pre-existing one. A chain of usage+generation is necessary but not sufficient for a derivation — some further influence during the intervening activity is also implied; PROV does not specify what determines a derivation. |
| ↳ Revision | Same form as Derivation, tagged `[ prov:type='prov:Revision' ]`. | A derivation whose resulting entity is a revised version of some original, i.e. contains substantial content from the original. No revision-specific attributes. |
| ↳ Quotation | Same form as Derivation, tagged `[ prov:type='prov:Quotation' ]`. | A derivation for which an entity was derived from a preceding entity by copying ("quoting") some or all of it — the repeat of some/all of an entity (text, image, etc.) by someone who may or may not be its original author. No quotation-specific attributes. |
| ↳ Primary Source | Same form as Derivation, tagged `[ prov:type='prov:PrimarySource' ]`. | A derivation from secondary materials to their primary source(s) — something produced by an agent with direct experience/knowledge of a topic at the time of study, without benefit of hindsight. Determination of what counts as primary is domain-convention-dependent. No primary-source-specific attributes. |
| **Attribution** | `wasAttributedTo(id; e, ag, attrs)` — e: entity (mandatory); ag: agent the entity is ascribed to (mandatory); attrs: OPTIONAL. | The ascribing of an entity to an agent. Implies entity `e` was generated by some unspecified activity that was in turn associated with agent `ag` — useful when the activity is unknown or irrelevant. |
| **Association** | `wasAssociatedWith(id; a, ag, pl, attrs)` — a: activity (mandatory); ag: OPTIONAL agent associated with the activity; pl: OPTIONAL plan (an Entity, `prov:Plan`) the agent relied on; attrs: OPTIONAL. At least one of id/ag/pl/attrs MUST be present. | An assignment of responsibility to an agent for an activity, indicating the agent had a role in it; optionally names the plan (set of actions/steps intended to achieve some goal) the agent relied on. |
| **Delegation** | `actedOnBehalfOf(id; ag2, ag1, a, attrs)` — ag2: delegate agent (mandatory); ag1: responsible agent on whose behalf ag2 acted (mandatory); a: OPTIONAL activity for which the delegation holds; attrs: OPTIONAL. | Assignment of authority/responsibility to an agent (by itself or another agent) to carry out a specific activity as delegate/representative, while the responsible agent retains some responsibility for the outcome. Broad in scope — covers contractual relations as well as altruistic initiative. |
| Influence | `wasInfluencedBy(id; o2, o1, attrs)` — o2: influencee (entity, activity, or agent); o1: influencer (an ancestor entity, activity, or agent o2 depends on); attrs: OPTIONAL. | A generic dependency of o2 on o1 signifying some form of influence of o1 on o2. Usage, Start, End, Generation, Invalidation, Communication, Derivation, Attribution, Association, and Delegation are all also instances of Influence; it is RECOMMENDED to use the more specific relation when possible. Influence is intended mainly to support querying over provenance. |

### Mapping specific relations onto Influence's influencee/influencer (Table 7, §5.3.5)

| Relation | influencee | influencer |
|---|---|---|
| Generation | entity | activity |
| Usage | activity | entity |
| Communication | informed | informant |
| Start | activity | trigger |
| End | activity | trigger |
| Invalidation | entity | activity |
| Derivation | generatedEntity | usedEntity |
| Attribution | entity | agent |
| Association | activity | agent |
| Delegation | delegate | responsible |

### Plan (§5.3.3)

A **plan** is an entity representing a set of actions or steps intended by one
or more agents to achieve some goals — it is the optional third argument of an
expanded `Association`. It is a subtype of Entity, denoted by `prov:Plan`.
PROV defines no plan-specific attributes. Since plans may evolve, their own
provenance can be tracked like any other entity.

```text
wasAssociatedWith(ex:a, ex:ag2, ex:wf, [ prov:role="designer" ])
entity(ex:wf, [ prov:type='prov:Plan', ex:label="Workflow 1",
  prov:location="http://example.org/workflow1.bpel" %% xsd:anyURI ])
```

---

## 4. Component 4: Bundles (§5.4)

A **bundle** is a named set of provenance descriptions, and is itself an
entity — this is the mechanism by which **provenance of provenance** is
expressed: to decide how much to trust a provenance description, a consumer
may need to know who asserted it, and when.

### Bundle constructor (§5.4.1)

A **bundle constructor** specifies the content and name of a bundle:

```text
bundle id
  description_1
  ...
  description_n
endBundle
```

- **id** — an identifier for the bundle; a bundle's identifier identifies a
  unique set of descriptions.
- **descriptions** — the set of provenance descriptions the bundle contains.

Other kinds of bundles not directly expressible by this constructor may
exist (e.g. provenance handwritten on a letter or whiteboard) — whatever the
means of expression, all bundles can be described via the Bundle type below.

### Bundle type (§5.4.2)

PROV defines one reserved type for bundles: **`prov:Bundle`** denotes Bundle
entities. PROV defines no bundle-specific attributes. A bundle's own
provenance is described the same way any entity's provenance is, e.g.:

```text
entity(bob:bundle1, [ prov:type='prov:Bundle' ])
wasGeneratedBy(bob:bundle1, -, 2012-05-24T10:30:00)
wasAttributedTo(bob:bundle1, ex:Bob)
```

Because a bundle is an entity, it can also participate in `wasDerivedFrom`
(e.g. a bundle produced by merging two other bundles is `wasDerivedFrom` each
of them), `wasGeneratedBy`, `wasAttributedTo`, etc. — the full core/extended
vocabulary applies recursively to provenance-about-provenance.

---

## 5. Component 5: Alternate entities (§5.5)

Two descriptions about the same underlying thing may emphasize different
aspects of it (e.g. a date-specific version of an article vs. the article "in
general"). PROV-DM defines two relations to link such entities. **Neither
relation is, as defined here, also an Influence — consequently neither has an
`id` nor `attrs` argument.**

### Specialization (§5.5.1)

An entity that is a **specialization** of another shares *all* aspects of the
latter, and additionally presents more specific aspects of the same thing.
The lifetime of the general (specialized) entity contains that of any of its
specializations. Aspects include things like a time period, an abstraction,
or a context associated with the entity.

`specializationOf(infra, supra)` in PROV-N, has:

- **specificEntity** (`infra`) — the entity that is a specialization of the general entity.
- **generalEntity** (`supra`) — the entity being specialized.

```text
specializationOf(ex:bbcNews2012-03-23, bbc:news/)
```

### Alternate (§5.5.2)

Two **alternate** entities present aspects of the same thing. These aspects
may be the same or different, and the alternate entities may or may not
overlap in time — this is a deliberately weak relationship: it only asserts
that both entities fix some aspect of some common thing, without further
inference (subtypes of `alternateOf` may support stronger inference in a
specific application).

`alternateOf(e1, e2)` in PROV-N, has:

- **alternate1** (`e1`) — identifier of the first entity.
- **alternate2** (`e2`) — identifier of the second entity.

```text
alternateOf(bbc:news/science-environment-17526723,
            bbc:news/mobile/science-environment-17526723)
```

**Distinguishing the two:** `specializationOf` is asymmetric and implies
strict containment — the specialization has *every* aspect of the general
entity plus more (and a shorter-or-equal lifetime). `alternateOf` is
symmetric and much weaker — it only says two entities are "about" the same
underlying thing without one being a refinement of the other. Two entities
can be both alternates of each other *and* each a specialization of some
common, more general entity (e.g. two dated versions of the same document
are alternates of each other, and both are specializations of the document's
generic, undated IRI).

---

## 6. Component 6: Collections (§5.6)

A **collection** is an entity that provides structure to some constituents,
which must themselves be entities; the constituents are said to be
**members** of the collection. This lets an application express the
provenance of the collection itself (who maintains it, how it was
assembled, which members it held at a given point) in addition to that of
its members. Many kinds of collections exist (sets, dictionaries, lists,
etc.) — PROV-DM only standardizes the generic notion and its emptiness.

### Collection and EmptyCollection (§5.6.1)

An **empty collection** is a collection without members. PROV-DM defines two
reserved types (no collection-specific attributes are defined for either):

| Type | Denotes |
|---|---|
| `prov:Collection` | An entity of type Collection, i.e. one that can participate in relations amongst collections. |
| `prov:EmptyCollection` | An empty collection. |

```text
entity(c0, [ prov:type='prov:EmptyCollection' ])  // c0 is an empty collection
entity(c1, [ prov:type='prov:Collection' ])       // c1 is a collection, unknown content
```

### Membership (§5.6.2)

**Membership** is the belonging of an entity to a collection. Like
`specializationOf`/`alternateOf`, it is **not defined as an Influence**, so it
has no `id` and no `attrs`.

`hadMember(c, e)` in PROV-N, has:

- **collection** (`c`) — identifier of the collection whose member is asserted.
- **entity** (`e`) — identifier of the entity that is a member of the collection.

```text
entity(c, [ prov:type='prov:Collection' ])  // c is known to have (at least) e0, e1, e2
hadMember(c, e0)
hadMember(c, e1)
hadMember(c, e2)
```

A collection can also be `wasInvalidatedBy`'d and re-`wasGeneratedBy`'d over
time (e.g. a Web page's membership of news items changing from one day to
the next), letting evolving collections be modeled with the same
generation/invalidation vocabulary as any other entity.

---

## 7. Further elements of PROV-DM (§5.7)

### Identifier (§5.7.1)

An **identifier** is a qualified name. `Entity`, `Activity`, and `Agent` have
a **mandatory** identifier — two of these are equal iff they share an
identifier. `Generation`, `Usage`, `Communication`, `Start`, `End`,
`Invalidation`, `Derivation`, `Attribution`, `Association`, `Delegation`, and
`Influence` have an **optional** identifier — two instances of the same
relation kind are equal iff they share an identifier.

### Attribute (§5.7.2)

An **attribute** is a qualified name. PROV-DM pre-defines five reserved
attributes in the PROV namespace (Table 8); this specification gives no
interpretation to attributes declared in any other namespace.

| Attribute | Allowed in | Value | §  |
|---|---|---|---|
| `prov:label` | Any construct | An `xsd:string` | 5.7.2.1 |
| `prov:location` | Entity, Activity, Agent, Usage, Generation, Invalidation, Start, End | A Value | 5.7.2.2 |
| `prov:role` | Usage, Generation, Invalidation, Association, Start, End | A Value | 5.7.2.3 |
| `prov:type` | Any construct | A Value | 5.7.2.4 |
| `prov:value` | Entity | A Value | 5.7.2.5 |

- **`prov:label`** — a human-readable representation of a PROV-DM type/relation
  instance. Value MUST be a string; may occur multiple times (e.g. per
  language: `prov:label="Voiture 01"@fr, prov:label="Car 01"@en`).
- **`prov:location`** — an identifiable geographic place (ISO 19112) or a
  non-geographic place (directory, row, column, etc.). PROV does not
  standardize how a location is concretely expressed; value MUST be a
  PROV-DM Value expected to denote a location.
- **`prov:role`** — the function of an entity or agent w.r.t. an activity, in
  the context of a usage, generation, invalidation, association, start, or
  end. May occur multiple times in one attribute list; value MUST be a
  PROV-DM Value.
- **`prov:type`** — further typing information for any construct. PROV-DM is
  agnostic about type representation; value MUST be a PROV-DM Value; may
  occur multiple times.
- **`prov:value`** — a direct representation of an entity as a PROV-DM Value.
  OPTIONAL on Entity only; MUST be a PROV-DM Value; MAY occur at most once.
  Two different entities MAY share the same `prov:value` (e.g. two
  entities computed differently that happen to both equal `4`).

#### PROV-DM predefined types (Table 9, §5.7.2.4)

| Type | Defined in | Applies to (core concept) |
|---|---|---|
| `prov:Bundle` | §5.4.1 | Entity |
| `prov:Collection` | §5.6.1 | Entity |
| `prov:EmptyCollection` | §5.6.1 | Entity |
| `prov:Organization` | §5.3.1 | Agent |
| `prov:Person` | §5.3.1 | Agent |
| `prov:Plan` | §5.3.3 | Entity |
| `prov:PrimarySource` | §5.2.4 | Derivation |
| `prov:Quotation` | §5.2.3 | Derivation |
| `prov:Revision` | §5.2.2 | Derivation |
| `prov:SoftwareAgent` | §5.3.1 | Agent |

### Value (§5.7.3)

A **value** is a constant — a string, number, time, qualified name, IRI, or
encoded binary data — whose interpretation is outside PROV's scope. Each kind
of value is a *datatype*; use of RDF-compatible types (including XML Schema
Datatypes) and of qualified names introduced by this spec is RECOMMENDED.
PROV time instants are defined according to `xsd:dateTime`.

```text
"abc"
"1" %% xsd:integer
"http://example.org/foo" %% xsd:anyURI
"ex:value" %% prov:QUALIFIED_NAME   // or, as convenience sugar: 'ex:value'
```

### Namespace Declaration (§5.7.4)

A **namespace** is identified by an IRI. A **namespace declaration** binds a
prefix to a namespace; every qualified name using that prefix, in scope,
refers to that namespace. A **default namespace declaration** binds an
unprefixed namespace; every un-prefixed qualified name refers to it. The
**PROV namespace** itself is `http://www.w3.org/ns/prov#`.

### Qualified Name (§5.7.5)

A **qualified name** is a name subject to namespace interpretation: a
namespace (denoted by an OPTIONAL prefix) plus a local name. A qualified
name maps to an IRI by concatenating the prefix's IRI and the local part. A
prefix-less qualified name refers to the default namespace.

### Extensibility points (§6, non-normative summary)

The PROV namespace reserves `prov:type`, `prov:role`, and `prov:location`
specifically to support extension without new relations:

- Sub-types and sub-relations are expressed via `prov:type` (e.g.
  `wasDerivedFrom(e2, e1, [ prov:type='ex:Translation' ])`,
  `entity(e, [ prov:type='ex:Car' ])`).
- Application/domain-specific roles are expressed via `prov:role` (e.g.
  `used(ex:work, ex:laptop4, [ prov:role="day-to-day machine" ])`).
- Arbitrary further attributes are introduced freely by declaring a new
  namespace/prefix and qualifying attribute names with it.

Specializations of PROV-DM that use these extensibility points MUST preserve
the semantics defined in PROV-DM and in PROV-CONSTRAINTS (§7) to remain
interoperable.

---

## 8. Cross-reference to PROV-N and PROV-O (Appendix A)

PROV-DM is a conceptual model serializable in multiple concrete notations.
Appendix A (Table 10, normative) maps every PROV-DM concept to its PROV-O
class/property and PROV-N production. Full grammar/production details live in
[PROV_N.md](PROV_N.md); full class/property definitions live in
[PROV_O.md](PROV_O.md).

| PROV-DM | PROV-O | PROV-N | Component |
|---|---|---|---|
| Entity | `Entity` | `entityExpression` | 1: Entities/Activities |
| Activity | `Activity` | `activityExpression` | |
| Generation | `wasGeneratedBy`, `Generation` | `generationExpression` | |
| Usage | `used`, `Usage` | `usageExpression` | |
| Communication | `wasInformedBy`, `Communication` | `communicationExpression` | |
| Start | `wasStartedBy`, `Start` | `startExpression` | |
| End | `wasEndedBy`, `End` | `endExpression` | |
| Invalidation | `wasInvalidatedBy`, `Invalidation` | `invalidationExpression` | |
| Derivation | `wasDerivedFrom`, `Derivation` | `derivationExpression` | 2: Derivations |
| Revision | `wasRevisionOf`, `Revision` | type `Revision` | |
| Quotation | `wasQuotedFrom`, `Quotation` | type `Quotation` | |
| Primary Source | `hadPrimarySource`, `PrimarySource` | type `PrimarySource` | |
| Agent | `Agent` | `agentExpression` | 3: Agents, Responsibility, Influence |
| Attribution | `wasAttributedTo`, `Attribution` | `attributionExpression` | |
| Association | `wasAssociatedWith`, `Association` | `associationExpression` | |
| Delegation | `actedOnBehalfOf`, `Delegation` | `delegationExpression` | |
| Plan | `Plan` | type `Plan` | |
| Person | `Person` | type `Person` | |
| Organization | `Organization` | type `Organization` | |
| SoftwareAgent | `SoftwareAgent` | type `SoftwareAgent` | |
| Influence | `wasInfluencedBy`, `Influence` | `influenceExpression` | |
| Bundle constructor | `bundle description` | `bundle` | 4: Bundles |
| Bundle type | `Bundle` | type `Bundle` | |
| Alternate | `alternateOf` | `alternateExpression` | 5: Alternate |
| Specialization | `specializationOf` | `specializationExpression` | |
| Collection | `Collection` | type `Collection` | 6: Collections |
| EmptyCollection | `EmptyCollection` | type `EmptyCollection` | |
| Membership | `hadMember` | `membershipExpression` | |

Note the DM-level `Derivation` relation covers `Revision`/`Quotation`/`Primary
Source` via a `prov:type` attribute in PROV-N (there is no separate PROV-N
production for them), but PROV-O exposes each as its own named property
(`wasRevisionOf`, `wasQuotedFrom`, `hadPrimarySource`) — see
[PROV_O.md](PROV_O.md) for full class/property definitions.
