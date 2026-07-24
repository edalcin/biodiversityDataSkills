# PROV Primer

Source: [PROV-DM Primer (W3C Note, 2013-04-30)](https://www.w3.org/TR/2013/NOTE-prov-primer-20130430/)

This document is a practical, example-driven walkthrough of the PROV data model. It provides an intuitive introduction and guide to PROV for building representations of the entities, people, and processes involved in producing a piece of data or thing in the world, and is intended as a **starting point** before consulting the more formal PROV-DM, PROV-O, and PROV-N specifications — read this first to build intuition, then use the other reference files in this skill for precise definitions, constraints, and syntax. The Primer builds its explanation around a single running scenario: a blogger (Betty) investigating the provenance of a newspaper article (`exn:article`) containing a chart (`exc:chart1`) generated from a government dataset (`exg:dataset1`), tracing an error back through the people, activities, and data involved. Examples use namespace prefixes `prov` (the PROV vocabulary), `exc`/`exn`/`exb`/`exg` (chart generator, newspaper, blogger, and government sources respectively), plus `foaf` and `dcterms` for non-PROV metadata.

## Intuitive overview

### Entities

An **entity** is a physical, digital, conceptual, or other kind of thing — examples include a web page, a chart, or a spellchecker. Provenance records describe the provenance of entities, and an entity's provenance may refer to many other entities (e.g. a document's provenance refers to a chart inserted into it, and the dataset used to create that chart). Entities may be described from different perspectives with different attributes: a document as stored in a file system, a specific version of the document, and the document as an evolving whole are three distinct entities.

The running example declares the article, dataset, region list, composed data, and chart as entities, with an attribute (`dcterms:title`) on the article:

```turtle
exn:article a prov:Entity ;
  dcterms:title "Crime rises in cities" .
exg:dataset1 a prov:Entity .
exc:regionList a prov:Entity .
exc:composition1 a prov:Entity .
exc:chart1 a prov:Entity .
```

```text
entity(exn:article, [dcterms:title="Crime rises in cities"])
entity(exg:dataset1)
entity(exc:regionList)
entity(exc:composition1)
entity(exc:chart1)
```

In visualizations, entities are conventionally drawn as **ovals**.

### Activities

**Activities** are how entities come into existence and how their attributes change to become new entities, often making use of previously existing entities. They are the dynamic aspects of the world — actions, processes, etc. For example, if a second version of a document is produced by translating the first version, the translation is an activity.

The example declares a top-level compilation activity and its two constituent steps — composing data by region, then generating the chart graphic:

```turtle
exc:compile1 a prov:Activity .
exc:compose1 a prov:Activity .
exc:illustrate1 a prov:Activity .
```

```text
activity(exc:compile1)
activity(exc:compose1)
activity(exc:illustrate1)
```

In visualizations, activities are drawn as **rectangles**.

### Usage and Generation

Activities **generate** new entities (e.g. writing a document brings it into existence; revising it brings a new version into existence) and **use** existing entities (e.g. revising a document uses the original version plus a list of corrections). Generation does not always occur at the end of an activity, nor usage always at the beginning — both may occur part-way through.

```turtle
exc:compose1 prov:used exg:dataset1 ;
  prov:used exc:regionList1 .
exc:composition1 prov:wasGeneratedBy exc:compose1 .

exc:illustrate1 prov:used exc:composition1 .
exc:chart1 prov:wasGeneratedBy exc:illustrate1 .
```

```text
used(exc:compose1, exg:dataset1, -)
used(exc:compose1, exc:regionList1, -)
wasGeneratedBy(exc:composition1, exc:compose1, -)

used(exc:illustrate1, exc:composition1, -)
wasGeneratedBy(exc:chart1, exc:illustrate1, -)
```

The `-` argument denotes unspecified optional information (e.g. time); see [PROV_N.md](PROV_N.md) for the full statement grammar. In visualizations, usage and generation are drawn as connections between entities and activities, with arrows pointing from the future to the past.

### Agents and Responsibility

An **agent** takes a role in an activity such that it can be assigned some degree of responsibility for the activity taking place. An agent can be a person, a piece of software, an inanimate object, an organization, or other entity that may be ascribed responsibility. When an agent has responsibility for an activity, PROV says the agent **was associated with** the activity (several agents may be associated with one activity and vice versa). An agent may act **on behalf of** another (e.g. an employee on behalf of their organization), forming chains of responsibility. An entity may also be **attributed to** an agent, expressing the agent's responsibility for the entity — shorthand for saying the agent was responsible for the activity that generated it. To make provenance assertions *about* an agent (e.g. an organization's own history), the agent must be declared explicitly both as an agent and as an entity.

Derek (a person) is associated with both activities, acts on behalf of his employer (an organization), and the chart is attributed to him:

```turtle
exc:compose1 prov:wasAssociatedWith exc:derek .
exc:illustrate1 prov:wasAssociatedWith exc:derek .

exc:derek a prov:Agent ;
  a prov:Person ;
  foaf:givenName "Derek"^^xsd:string ;
  foaf:mbox <mailto:derek@example.org> .

exc:derek prov:actedOnBehalfOf exc:chartgen .
exc:chartgen a prov:Agent ;
  a prov:Organization ;
  foaf:name "Chart Generators Inc" .

exc:chart1 prov:wasAttributedTo exc:derek .
```

```text
wasAssociatedWith(exc:compose1, exc:derek, -)
wasAssociatedWith(exc:illustrate1, exc:derek, -)

agent(exc:derek,
  [prov:type='prov:Person', foaf:givenName="Derek",
   foaf:mbox="<mailto:derek@example.org>"])

agent(exc:chartgen,
  [prov:type='prov:Organization', foaf:name="Chart Generators Inc"])
actedOnBehalfOf(exc:derek, exc:chartgen)

wasAttributedTo(exc:chart1, exc:derek)
```

It is also possible to state that an agent acted on another's behalf for a *specific* activity rather than in general (activity-specific delegation) — see PROV-DM/PROV-N for details.

### Roles

A **role** describes the function or part that an entity played in an activity, or how an agent was involved in and responsible for an activity. Roles specify the relationship between an entity/agent and an activity — e.g. an agent may play "editor" while an activity uses one entity as "document to be edited" and another as "addition to be made", generating a further entity in the role "edited document". Roles are application-specific; PROV does not predefine any.

Simple usage/generation/association facts (e.g. `exc:compose1 prov:used exg:dataset1`) can be enriched with roles via PROV-O's **qualified** forms (`qualifiedUsage`, `qualifiedGeneration`, `qualifiedAssociation`, ...) — auxiliary structures bundling several statements about how a usage/generation/association took place (role, time, plan, etc.):

```turtle
exc:compose1 prov:qualifiedUsage [
  a prov:Usage ;
  prov:entity exg:dataset1 ;
  prov:hadRole exc:dataToCompose
] .

exc:compose1 prov:qualifiedUsage [
  a prov:Usage ;
  prov:entity exc:regionList1 ;
  prov:hadRole exc:regionsToAggregateBy
] .

exc:compose1 prov:qualifiedAssociation [
  a prov:Association ;
  prov:agent exc:derek ;
  prov:hadRole exc:analyst
] .
exc:composition1 prov:qualifiedGeneration [
  a prov:Generation ;
  prov:activity exc:compose1 ;
  prov:hadRole exc:composedData
] .
```

In PROV-N, a role is expressed as an attribute (`prov:role`) in the statement's attribute list rather than as a separate qualified structure:

```text
used(exc:compose1, exg:dataset1, -, [prov:role='exc:dataToCompose'])
used(exc:compose1, exc:regionList1, -, [prov:role='exc:regionsToAggregateBy'])
wasAssociatedWith(exc:compose1, exc:derek, -, [prov:role='exc:analyst'])
wasGeneratedBy(exc:composition1, exc:compose1, -, [prov:role='exc:composedData'])
```

### Derivation and Revision

When one entity's existence, content, or characteristics are at least partly due to another entity, the former is said to be **derived from** the latter (e.g. a document containing material copied from another, or a chart derived from the data it illustrates). PROV allows some specialized kinds of derivation:

- **Revision** — a given entity (e.g. a document) may go through multiple revisions over time; the result of each revision is a new entity, related to the prior one via `wasRevisionOf` (PROV-O) / a `wasDerivedFrom` with `prov:type='prov:Revision'` (PROV-N).
- **Quotation** — one entity (a quotation) is quoted from another (commonly a document); see [Alternate Entities and Specialization](#alternate-entities-and-specialization) below for the worked example.

```turtle
exg:dataset2 a prov:Entity ;
  prov:wasRevisionOf exg:dataset1 .

exc:chart2 a prov:Entity ;
  prov:wasDerivedFrom exg:dataset2 .

exc:chart2 a prov:Entity ;
  prov:wasRevisionOf exc:chart1 .
```

```text
entity(exg:dataset2)
wasDerivedFrom(exg:dataset2, exg:dataset1, [prov:type='prov:Revision'])

wasDerivedFrom(exc:chart2, exg:dataset2)

entity(exc:chart2)
wasDerivedFrom(exc:chart2, exc:chart1, [prov:type='prov:Revision'])
```

Derivation and revision are visualized as connections (arrows) between entities.

### Plans

Activities may follow pre-defined procedures — recipes, tutorials, instructions, or workflows. PROV refers to these generically as **plans**, and allows describing that a plan was followed by an agent in performing an activity. The plan is expressed via `prov:hadPlan` inside a qualified association (PROV-O), or as an optional third argument to `wasAssociatedWith` (PROV-N):

```turtle
exg:correct1 a prov:Activity .
exg:edith a prov:Agent, prov:Person .
exg:instructions a prov:Plan .

exg:correct1 prov:qualifiedAssociation [
  a prov:Association ;
  prov:agent exg:edith ;
  prov:hadPlan exg:instructions
] .
exg:dataset2 prov:wasGeneratedBy exg:correct1 .
```

```text
activity(exg:correct1)
agent(exg:edith, [prov:type='prov:Person'])
entity(exg:instructions)

wasAssociatedWith(exg:correct1, exg:edith, exg:instructions)
wasGeneratedBy(exg:dataset2, exg:correct1, -)
```

Plans are additional information attached to the connection from an activity to an agent, and so are visualized attached to that link.

### Time

PROV allows the timing of significant events to be described: when an entity was **generated** or **used**, and when an activity **started** and **finished**. This lets consumers compare, for example, when two revisions of a chart were produced, or how long a correction activity took.

```turtle
exc:chart1 prov:generatedAtTime "2012-03-02T10:30:00"^^xsd:dateTime .
exc:chart2 prov:generatedAtTime "2012-04-01T15:21:00"^^xsd:dateTime .

exg:correct1 prov:startedAtTime "2012-03-31T09:21:00"^^xsd:dateTime ;
  prov:endedAtTime "2012-04-01T15:21:00"^^xsd:dateTime .
```

```text
wasGeneratedBy(exc:chart1, exc:compile1, 2012-03-02T10:30:00)
wasGeneratedBy(exc:chart2, exc:compile2, 2012-04-01T15:21:00)

activity(exg:correct1, 2012-03-31T09:21:00, 2012-04-01T15:21:00)
```

Time is visualized as additional information on activities or on the links between activities and entities/agents.

### Alternate Entities and Specialization

There is often more than one way to describe the same thing in provenance. Each perspective is a separately identified entity, and PROV links these descriptions together via two mechanisms:

- **Specialization** (`specializationOf`) — entity A is a specialization of entity B if A shares the same fixed attributes as B, possibly with further fixed attributes added. Example: a webpage `W` edited over time is one entity, but each version `W1`, `W2`, ... is also an entity and a specialization of `W`.
- **Alternate** (`alternateOf`) — a more general connection between two descriptions of the same thing, even when not at different specialization levels (e.g. two versions `W1`/`W2` of a webpage are alternates of each other because they describe the same webpage; a file copied to a backup directory is an alternate of the original because the copies differ only in context/location, not content).

A blog quote is derived from the article via a quotation-typed derivation:

```turtle
exb:quoteInBlogEntry-20130326 a prov:Entity ;
  prov:value "Smaller cities have more crime than larger ones" ;
  prov:wasQuotedFrom exn:article .
```

```text
entity(exb:quoteInBlogEntry-20130326, prov:value="Smaller cities have more crime than larger ones")
wasDerivedFrom(exb:quoteInBlogEntry-20130326, exn:article, [prov:type='prov:Quotation'])
```

The newspaper distinguishes the general article from its first published version via specialization, and later relates a second version to both the general article (specialization) and the first version (alternate):

```turtle
exn:articleV1 a prov:Entity ;
  prov:specializationOf exn:article .

exn:articleV2 prov:specializationOf exn:article .
exn:articleV2 prov:alternateOf exn:articleV1 .
```

```text
entity(exn:articleV1)
specializationOf(exn:articleV1, exn:article)

specializationOf(exn:articleV2, exn:article)
alternateOf(exn:articleV2, exn:articleV1)
```

Note that `exn:articleV2` could instead (or additionally) have been declared `wasRevisionOf` `exn:articleV1`, which would state more concretely how the two alternates relate. Specialization and alternate relations are visualized as links between entities.

## Summary

Section 4 of the Primer highlights the capabilities the running example demonstrates:

- Representing diverse entities from **object-centered** (newspaper: what was derived from what), **agent-centered** (Betty: entities linked to people/orgs), and **process-centered** (Derek: activities plus object- and agent-centered detail) perspectives.
- Stating **partial or incomplete** provenance (the newspaper omitted editorial process detail; the chart generator omitted software agents).
- **Integrating** other vocabularies — FOAF for Derek/his company, Dublin Core for the article title.
- **Combining distributed** provenance records from multiple parties (government, newspaper, company, blogger) via URIs and namespaces.
- Describing **commonalities in derivation** — both chart versions were produced by a similar compile activity.
- **Relating versions over time** via revision (`exg:dataset2` as a revision of `exg:dataset1`).
- **Provenance of provenance** — a provenance record can itself be grouped as a `bundle` (a type of entity) and have its own provenance asserted (e.g. Betty stating she personally checked her sources) — not covered in worked examples here; see PROV-DM.
- **Alternative accounts** for the same entity's provenance (e.g. the blog post could carry a provenance account from Betty and another from the newspaper it quotes).
- **Queries at different granularity** — the composition activity was described in finer detail than the other steps.
- **Reasoning and inference** — e.g. because Derek created the chart on behalf of Chart Generators, PROV inference can conclude the chart is also attributable to Chart Generators.

PROV also supports **collections** (an entity with other entities as members, e.g. Derek grouping several charts derived from `dataset2`) — not detailed in this Primer; see PROV-DM.

### PROV-N relations used in the worked example

| Statement / relation | One-line description (as used in the Primer) |
|---|---|
| `entity(id, [attrs])` | Declares something (physical, digital, or conceptual) as a PROV entity, optionally with attributes. |
| `activity(id, [start, end, attrs])` | Declares a dynamic process/action as a PROV activity, optionally with start/end time. |
| `agent(id, [attrs])` | Declares a person, organization, or software as a PROV agent, optionally with a type/attributes. |
| `used(activity, entity, time, [attrs])` | States that an activity made use of an entity (optionally in a given role, at a given time). |
| `wasGeneratedBy(entity, activity, time, [attrs])` | States that an entity was produced by an activity (optionally in a given role, at a given time). |
| `wasAssociatedWith(activity, agent, plan, [attrs])` | States that an agent had some responsibility for an activity, optionally naming the plan it followed and its role. |
| `actedOnBehalfOf(delegate, responsible, [activity])` | States that one agent acted for another (e.g. an employee for their organization), forming a responsibility chain. |
| `wasAttributedTo(entity, agent)` | States that an entity is attributed to (i.e. is the responsibility of) an agent. |
| `wasDerivedFrom(generatedEntity, usedEntity, [attrs])` | States that one entity was derived from another; `prov:type='prov:Revision'` specializes it to revision, `prov:type='prov:Quotation'` to quotation. |
| `specializationOf(specificEntity, generalEntity)` | States that a specific entity shares all fixed attributes of a more general entity (possibly with more). |
| `alternateOf(entity1, entity2)` | States that two entities describe the same thing without one specializing the other. |
| `prov:role` attribute (in `used`/`wasGeneratedBy`/`wasAssociatedWith`) | Qualifies the function an entity/agent played in an activity (application-specific; not predefined by PROV). |
| `prov:hadPlan` (via `wasAssociatedWith`'s third argument) | Names the recipe/workflow/instructions an agent followed while carrying out an activity. |
