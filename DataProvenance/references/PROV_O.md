# PROV-O: The PROV Ontology

Source: [PROV-O: The PROV Ontology (W3C Recommendation, 2013-04-30)](https://www.w3.org/TR/2013/REC-prov-o-20130430/)

PROV-O expresses the [PROV Data Model](DATA_MODEL.md) (PROV-DM) using the OWL2 Web Ontology Language. It defines the set of RDF classes, properties, and restrictions needed to represent and interchange provenance information in RDF/OWL2 — Turtle, RDF/XML, JSON-LD, etc. PROV-O is the file an AI agent reaches for when it needs to actually *serialize* provenance, as opposed to reasoning about the abstract model ([DATA_MODEL.md](DATA_MODEL.md)) or the human-readable notation ([PROV_N.md](PROV_N.md)).

The namespace for all PROV-O terms is `http://www.w3.org/ns/prov#`, conventionally bound to the prefix `prov:`. PROV-O is a lightweight ontology: with the exception of five axioms (documented in Appendix A of the source), it conforms to the OWL 2 RL profile.

PROV-O terms are organized into three tiers, of increasing expressiveness and verbosity:

1. **Starting Point Terms** — a minimal set of 3 classes and 9 properties sufficient for simple provenance chains (`prov:Entity`, `prov:Activity`, `prov:Agent` and the direct binary relations connecting them).
2. **Expanded Terms** — additional classes/subclasses and properties/subproperties (agent kinds, collections, bundles, timestamps, more specific derivations) that refine or extend the Starting Point vocabulary.
3. **Qualified Terms** — a structural pattern (`prov:qualifiedX` / `prov:XClass`) that restates any binary Starting Point or Expanded relation as an intermediate resource, so extra attributes (time, role, plan, etc.) can be attached to the relation itself, not just to its endpoints.

Superscripts in the tables below follow the source convention: **op** = OWL object property, **dp** = OWL datatype property.

## Starting Point Terms

The Starting Point category is a small set of classes and properties sufficient to create simple, initial provenance descriptions. Three classes anchor the whole ontology; the rest are properties relating them.

| Term | Type | Domain → Range | Definition |
|---|---|---|---|
| `prov:Entity` | Class | — | A physical, digital, conceptual, or other kind of thing with some fixed aspects; entities may be real or imaginary. |
| `prov:Activity` | Class | — | Something that occurs over a period of time and acts upon or with entities; it may include consuming, processing, transforming, modifying, relocating, using, or generating entities. |
| `prov:Agent` | Class | — | Something that bears some form of responsibility for an activity taking place, for the existence of an entity, or for another agent's activity. |
| `prov:wasGeneratedBy` | Property (op) | Entity → Activity | Generation is the completion of production of a new entity by an activity. The entity did not exist before generation and becomes available for usage after it. Qualifiable with `prov:Generation`. |
| `prov:used` | Property (op) | Activity → Entity | Usage is the beginning of utilizing an entity by an activity. Before usage, the activity had not begun to utilize the entity and could not have been affected by it. Qualifiable with `prov:Usage`. |
| `prov:wasInformedBy` | Property (op) | Activity → Activity | An activity a2 is dependent on / informed by another activity a1, by way of some unspecified entity that a1 generated and a2 used. Communication is the exchange of an entity by two activities. Qualifiable with `prov:Communication`. |
| `prov:wasAssociatedWith` | Property (op) | Activity → Agent | An activity association is an assignment of responsibility to an agent for an activity, indicating the agent had a role in it, and optionally the plan it followed. Qualifiable with `prov:Association`. |
| `prov:actedOnBehalfOf` | Property (op) | Agent → Agent | Delegation: the assignment of authority and responsibility to an agent (by itself or another agent) to carry out a specific activity as a delegate, while the agent it acts on behalf of retains some responsibility for the outcome. Qualifiable with `prov:Delegation`. |
| `prov:wasAttributedTo` | Property (op) | Entity → Agent | Attribution is the ascribing of an entity to an agent. Qualifiable with `prov:Attribution`. |
| `prov:wasDerivedFrom` | Property (op) | Entity → Entity | A derivation is a transformation of an entity into another, an update of an entity resulting in a new one, or construction of a new entity based on a pre-existing one. Superproperty of `wasQuotedFrom`, `wasRevisionOf`, `hadPrimarySource`. Qualifiable with `prov:Derivation`. |
| `prov:startedAtTime` | Property (dp) | Activity → `xsd:dateTime` | The time at which an activity started. See also `prov:endedAtTime`. Qualifiable with `prov:Start`. |
| `prov:endedAtTime` | Property (dp) | Activity → `xsd:dateTime` | The time at which an activity ended. See also `prov:startedAtTime`. Qualifiable with `prov:End`. |

All Starting Point properties are (directly or transitively) subproperties of `prov:wasInfluencedBy` (see [Qualified Terms](#qualified-terms)). `rdf:type` and `rdfs:label` are used to express PROV-DM's `prov:type` and `prov:label` respectively — they are not separate PROV-O terms.

The source's running example (a data journalist aggregating crime statistics into a chart) uses only Starting Point terms:

```turtle
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix : <http://example.org#> .

:bar_chart
    a prov:Entity;
    prov:wasGeneratedBy :illustrationActivity;
    prov:wasDerivedFrom :aggregatedByRegions;
    prov:wasAttributedTo :derek;
    .

:derek
    a foaf:Person, prov:Agent;
    foaf:givenName "Derek";
    foaf:mbox <mailto:derek@example.org>;
    prov:actedOnBehalfOf :natonal_newspaper_inc;
    .

:national_newspaper_inc
    a foaf:Organization, prov:Agent;
    foaf:name "National Newspaper, Inc.";
    .

:illustrationActivity
    a prov:Activity;
    prov:used :aggregatedByRegions;
    prov:wasAssociatedWith :derek;
    prov:wasInformedBy :aggregationActivity;
    .

:aggregatedByRegions
    a prov:Entity;
    prov:wasGeneratedBy :aggregationActivity;
    prov:wasAttributedTo :derek;
    .

:aggregationActivity
    a prov:Activity;
    prov:startedAtTime "2011-07-14T01:01:01Z"^^xsd:dateTime;
    prov:wasAssociatedWith :derek;
    prov:used :crimeData;
    prov:used :nationalRegionsList;
    prov:endedAtTime "2011-07-14T02:02:02Z"^^xsd:dateTime;
    .

:crimeData a prov:Entity; prov:wasAttributedTo :government .
:government a foaf:Organization, prov:Agent .

:nationalRegionsList a prov:Entity; prov:wasAttributedTo :civil_action_group .
:civil_action_group a foaf:Organization, prov:Agent .
```

`:derek` was associated with two activities (`:aggregationActivity`, `:illustrationActivity`); the first used `:crimeData` and `:nationalRegionsList` to generate `:aggregatedByRegions`, which the second used to generate `:bar_chart`. `:illustrationActivity` `prov:wasInformedBy` `:aggregationActivity` because it used an entity the latter generated.

## Expanded Terms

The Expanded tier refines the Starting Point terms along five lines: (1) subclasses of `Agent`/`Entity` and a superproperty (`wasInfluencedBy`) plus more specific derivation subproperties; (2) entity abstraction levels (`specializationOf`/`alternateOf`); (3) further description via `value`/`atLocation`; (4) entity lifetime bounds (`generatedAtTime`/`invalidatedAtTime`); (5) activity lifetime via entity triggers (`wasStartedBy`/`wasEndedBy`).

### Classes

| Term | Type | Subclass of | Definition |
|---|---|---|---|
| `prov:Collection` | Class | `prov:Entity` | An entity that provides a structure (e.g. set, list) to some constituents, which are themselves entities and are said to be members of the collection. Described with `prov:hadMember`. |
| `prov:EmptyCollection` | Class | `prov:Collection` | A collection without members. |
| `prov:Bundle` | Class | `prov:Entity` | A named set of provenance descriptions, itself an Entity — allowing provenance of provenance to be expressed. Because a bundle is a kind of entity, all entity assertions can also be made about bundles. |
| `prov:Person` | Class | `prov:Agent` | Person agents are people. |
| `prov:Organization` | Class | `prov:Agent` | A social or legal institution such as a company, society, etc. |
| `prov:SoftwareAgent` | Class | `prov:Agent` | A software agent is running software. |
| `prov:Location` | Class | — | An identifiable geographic place (ISO 19112), or a non-geographic place such as a directory, row, or column; expressible by coordinate, address, landmark, etc. Properties describing `Location` instances are out of scope for PROV-O. |

### Properties

| Term | Type | Domain → Range | Definition |
|---|---|---|---|
| `prov:alternateOf` | Property (op) | Entity → Entity | Two alternate entities present aspects of the same thing; these aspects may be the same or different, and the entities may or may not overlap in time. Has subproperty `specializationOf`. |
| `prov:specializationOf` | Property (op), subproperty of `alternateOf` | Entity → Entity | A specialization of another entity shares all its aspects and additionally presents more specific aspects of the same thing; the lifetime of the general entity contains that of any specialization. |
| `prov:generatedAtTime` | Property (dp) | Entity → `xsd:dateTime` | The time at which an entity was completely created and became available for use. Qualifiable with `prov:Generation`/`prov:atTime`. |
| `prov:hadPrimarySource` | Property (op), subproperty of `wasDerivedFrom` | Entity → Entity | Cites a preceding entity produced by some agent with direct experience and knowledge about the topic, at the time of its study, without benefit of hindsight — e.g. a sensor reading. A particular case of derivation. Qualifiable with `prov:PrimarySource`. |
| `prov:value` | Property (dp) | Entity → literal | Provides a value that is a direct representation of an entity, e.g. the string of a quote, or the `xsd:integer` result of a calculation. |
| `prov:wasQuotedFrom` | Property (op), subproperty of `wasDerivedFrom` | Entity → Entity | An entity is derived from an original entity by copying, or "quoting", some or all of it — a particular case of derivation. Qualifiable with `prov:Quotation`. |
| `prov:wasRevisionOf` | Property (op), subproperty of `wasDerivedFrom` | Entity → Entity | A derivation for which the resulting entity is a revised version of some original, containing substantial content from it — a particular case of derivation. Qualifiable with `prov:Revision`. |
| `prov:invalidatedAtTime` | Property (dp) | Entity → `xsd:dateTime` | The time at which an entity was invalidated (no longer usable). Qualifiable with `prov:Invalidation`/`prov:atTime`. |
| `prov:wasInvalidatedBy` | Property (op) | Entity → Activity | Invalidation is the start of the destruction, cessation, or expiry of an existing entity by an activity; the entity is no longer available for use afterward. Any generation or usage of the entity precedes its invalidation. Qualifiable with `prov:Invalidation`. |
| `prov:hadMember` | Property (op) | Collection → Entity | Asserts membership of an Entity in a Collection. |
| `prov:wasStartedBy` | Property (op) | Activity → Entity | Start is when an activity is deemed to have been started by an entity, known as trigger; the activity did not exist before its start. Qualifiable with `prov:Start`. |
| `prov:wasEndedBy` | Property (op) | Activity → Entity | End is when an activity is deemed to have been ended by an entity, known as trigger; the activity no longer exists after its end. Qualifiable with `prov:End`. |
| `prov:invalidated` | Property (op), subproperty of `influenced` | Activity → Entity | Inverse of `prov:wasInvalidatedBy`, provided to facilitate Activity-as-subject descriptions. |
| `prov:influenced` | Property (op) | — | Inverse of `prov:wasInfluencedBy`. Superproperty of `prov:generated` and `prov:invalidated`. |
| `prov:atLocation` | Property (op) | Activity ∪ Agent ∪ Entity ∪ InstantaneousEvent → Location | The Location of any resource. Has multiple RDFS domains (a non-OWL-RL-conformant axiom — see the source's Appendix A). |
| `prov:generated` | Property (op), subproperty of `influenced` | Activity → Entity | Inverse of `prov:wasGeneratedBy`, provided to facilitate Activity-as-subject descriptions. |

`prov:Plan` and `prov:Role` are also introduced conceptually in this tier but are cross-referenced under [Qualified Terms](#qualified-terms) in the source, since they are only usable via the qualification pattern (`prov:hadPlan`, `prov:hadRole`).

A `prov:Collection` example, showing membership and a `prov:wasQuotedFrom` derivation:

```turtle
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix ex: <http://example.com/ontology#> .
@prefix : <http://example.com/> .

:todays-us-supreme-court
    a prov:Collection, :RobertsCourt;
    prov:hadMember
        <http://dbpedia.org/resource/John_Glover_Roberts,_Jr.>,
        <http://dbpedia.org/resource/Antonin_Scalia>,
        <http://dbpedia.org/resource/Ruth_Bader_Ginsburg>;
    prov:wasDerivedFrom :the-first-us-supreme-court;
    dcterms:description :copied-string;
    .

:copied-string
    a prov:Entity;
    prov:value """2010-present: A. Scalia ... R.B. Ginsburg ...""";
    prov:wasQuotedFrom :page-by-composition;
    .

:page-by-composition
    a prov:Entity, ex:WikipediaPage;
    prov:specializationOf <http://purl.org/twc/page/wikipedia/us-supreme-court-by-composition>;
    prov:generatedAtTime "2012-05-16T14:33:00"^^xsd:dateTime;
    .
```

A revision/alternate example (Derek edits a typo in his blog post):

```turtle
:post9821v2
    a sioc:Post, prov:Entity;
    prov:specializationOf :more-crime-happens-in-cities;
    prov:value "I was curious...";
    prov:generatedAtTime "2011-07-16T02:02:02Z"^^xsd:dateTime;
    prov:wasRevisionOf :post9821v1;
    prov:alternateOf :post9821v1;
    .
```

## Qualified Terms

### Why qualification exists

Starting Point and Expanded properties (`prov:used`, `prov:wasGeneratedBy`, `prov:wasAssociatedWith`, etc.) are direct, binary RDF triples: they connect two resources but cannot themselves carry attributes — RDF triples have no place to hang a "the activity used this entity *in role X, at time T*" annotation. The Qualification Pattern (from [LD-Patterns-QR]) solves this by restating the binary relation through an intermediate class instance (e.g. `prov:Usage`) that represents the *influence itself* as a first-class resource. Additional properties (time, role, plan, location, etc.) are then attached to that intermediate instance instead of to either endpoint.

Every qualifiable relation follows the same shape: the influenced resource keeps its `prov:qualifiedX` property pointing at a new blank node or IRI typed `prov:X` (a subclass of `prov:Influence`), and that new resource cites the influencing resource via an `influencer`-style property (`prov:entity`, `prov:activity`, or `prov:agent`, depending on whether the influencer is an Entity, Activity, or Agent). It is correct to use either the unqualified or the qualified form (or both); when additional attributes aren't needed, the unqualified form should be favored for brevity. When qualification is used, including the equivalent unqualified triple is encouraged to aid consumers that don't process the qualified form.

All qualifiable-influence subclasses derive from `prov:Influence`, and specifically from one of `prov:EntityInfluence`, `prov:ActivityInfluence`, or `prov:AgentInfluence`, which fix which citing property (`prov:entity`, `prov:activity`, `prov:agent` respectively) is used.

### Qualifiable relations

Seven Starting Point relations and seven Expanded relations can be qualified (source Tables 2 and 3):

| Influenced Class | Unqualified Property | Influencing Class | Qualification Property | Qualified Class | Influencer Property |
|---|---|---|---|---|---|
| Entity | `wasGeneratedBy` | Activity | `qualifiedGeneration` | `Generation` | `activity` |
| Entity | `wasDerivedFrom` | Entity | `qualifiedDerivation` | `Derivation` | `entity` |
| Entity | `wasAttributedTo` | Agent | `qualifiedAttribution` | `Attribution` | `agent` |
| Activity | `used` | Entity | `qualifiedUsage` | `Usage` | `entity` |
| Activity | `wasInformedBy` | Activity | `qualifiedCommunication` | `Communication` | `activity` |
| Activity | `wasAssociatedWith` | Agent | `qualifiedAssociation` | `Association` | `agent` |
| Agent | `actedOnBehalfOf` | Agent | `qualifiedDelegation` | `Delegation` | `agent` |
| Entity ∪ Activity ∪ Agent | `wasInfluencedBy` | Entity ∪ Activity ∪ Agent | `qualifiedInfluence` | `Influence` | `influencer` |
| Entity | `hadPrimarySource` | Entity | `qualifiedPrimarySource` | `PrimarySource` | `entity` |
| Entity | `wasQuotedFrom` | Entity | `qualifiedQuotation` | `Quotation` | `entity` |
| Entity | `wasRevisionOf` | Entity | `qualifiedRevision` | `Revision` | `entity` |
| Entity | `wasInvalidatedBy` | Activity | `qualifiedInvalidation` | `Invalidation` | `activity` |
| Activity | `wasStartedBy` | Entity | `qualifiedStart` | `Start` | `entity` |
| Activity | `wasEndedBy` | Entity | `qualifiedEnd` | `End` | `entity` |

### Qualified classes

| Term | Subclass of | Qualifies | Definition |
|---|---|---|---|
| `prov:Influence` | — | `wasInfluencedBy` | The capacity of an entity, activity, or agent to have an effect on the character, development, or behavior of another, by means of usage, start, end, generation, invalidation, communication, derivation, attribution, association, or delegation. Because it is broad, more specific subclasses should be used when applicable. |
| `prov:EntityInfluence` | `Influence` | — | An Entity's binary influence upon any other resource; cites the influencing Entity via `prov:entity`. Subclasses: `End`, `Start`, `Usage`, `Derivation`. |
| `prov:ActivityInfluence` | `Influence` | — | An Activity's binary influence upon any other resource; cites the influencing Activity via `prov:activity`. Subclasses: `Generation`, `Invalidation`, `Communication`. |
| `prov:AgentInfluence` | `Influence` | — | An Agent's binary influence upon any other resource; cites the influencing Agent via `prov:agent`. Subclasses: `Delegation`, `Association`, `Attribution`. |
| `prov:Usage` | `InstantaneousEvent`, `EntityInfluence` | `used` | Additional description of the binary `used` relation from an Activity to the Entity it used. |
| `prov:Start` | `InstantaneousEvent`, `EntityInfluence` | `wasStartedBy` | Additional description of the binary `wasStartedBy` relation from a started Activity to its triggering Entity. |
| `prov:End` | `InstantaneousEvent`, `EntityInfluence` | `wasEndedBy` | Additional description of the binary `wasEndedBy` relation from an ended Activity to its triggering Entity. |
| `prov:Derivation` | `EntityInfluence` | `wasDerivedFrom` | Additional description of the binary `wasDerivedFrom` relation from a derived Entity to the Entity it was derived from. More specific forms (`Revision`, `Quotation`, `PrimarySource`) should be used when applicable. |
| `prov:PrimarySource` | `Derivation` | `hadPrimarySource` | Additional description of the binary `hadPrimarySource` relation from a secondary Entity to an earlier, primary Entity. |
| `prov:Quotation` | `Derivation` | `wasQuotedFrom` | Additional description of the binary `wasQuotedFrom` relation from a taken Entity to an earlier, larger Entity. |
| `prov:Revision` | `Derivation` | `wasRevisionOf` | Additional description of the binary `wasRevisionOf` relation from a newer Entity to an earlier one. |
| `prov:Generation` | `InstantaneousEvent`, `ActivityInfluence` | `wasGeneratedBy` | Additional description of the binary `wasGeneratedBy` relation from a generated Entity to the Activity that generated it. |
| `prov:Communication` | `ActivityInfluence` | `wasInformedBy` | Additional description of the binary `wasInformedBy` relation from an informed Activity to the Activity that informed it. |
| `prov:Invalidation` | `InstantaneousEvent`, `ActivityInfluence` | `wasInvalidatedBy` | Additional description of the binary `wasInvalidatedBy` relation from an invalidated Entity to the Activity that invalidated it. |
| `prov:Attribution` | `AgentInfluence` | `wasAttributedTo` | Additional description of the binary `wasAttributedTo` relation from an Entity to the Agent responsible for it. |
| `prov:Association` | `AgentInfluence` | `wasAssociatedWith` | Additional description of the binary `wasAssociatedWith` relation from an Activity to a responsible Agent; can further cite a `prov:hadPlan`. |
| `prov:Plan` | `Entity` | (range of `hadPlan`) | An entity representing a set of actions or steps intended by one or more agents to achieve some goals. No prescriptive requirement on plan representation; left to applications to extend. |
| `prov:Delegation` | `AgentInfluence` | `actedOnBehalfOf` | Additional description of the binary `actedOnBehalfOf` relation from a performing Agent to the Agent on whose behalf it acted. |
| `prov:InstantaneousEvent` | — | — | A transition point in the world — generation, usage, invalidation of entities, or the starting/ending of activities. Not first-class in PROV-DM, but useful for explaining PROV-O's semantics. Subclasses: `Generation`, `Start`, `Invalidation`, `End`, `Usage`. |
| `prov:Role` | — | (range of `hadRole`) | The function of an entity or agent with respect to an activity, in the context of a usage, generation, invalidation, association, start, or end. Left to applications to extend. |

### Qualified and supporting properties

| Term | Type | Domain → Range | Qualifies / Purpose |
|---|---|---|---|
| `prov:wasInfluencedBy` | Property (op) | Entity ∪ Activity ∪ Agent → Entity ∪ Activity ∪ Agent | Superproperty of `hadMember`, `wasAttributedTo`, `wasAssociatedWith`, `wasGeneratedBy`, `wasDerivedFrom`, `wasInvalidatedBy`, `used`, `actedOnBehalfOf`, `wasInformedBy`, `wasStartedBy`, `wasEndedBy`. |
| `prov:qualifiedInfluence` | Property (op) | Entity ∪ Activity ∪ Agent → `Influence` | Qualifies `wasInfluencedBy`; superproperty of all other `qualifiedX` properties. |
| `prov:qualifiedGeneration` | Property (op) | Entity → `Generation` | Qualifies `wasGeneratedBy`. |
| `prov:qualifiedDerivation` | Property (op) | Entity → `Derivation` | Qualifies `wasDerivedFrom`. |
| `prov:qualifiedPrimarySource` | Property (op) | Entity → `PrimarySource` | Qualifies `hadPrimarySource`. |
| `prov:qualifiedQuotation` | Property (op) | Entity → `Quotation` | Qualifies `wasQuotedFrom`. |
| `prov:qualifiedRevision` | Property (op) | Entity → `Revision` | Qualifies `wasRevisionOf`. |
| `prov:qualifiedAttribution` | Property (op) | Entity → `Attribution` | Qualifies `wasAttributedTo`. |
| `prov:qualifiedInvalidation` | Property (op) | Entity → `Invalidation` | Qualifies `wasInvalidatedBy`. |
| `prov:qualifiedStart` | Property (op) | Activity → `Start` | Qualifies `wasStartedBy`. |
| `prov:qualifiedUsage` | Property (op) | Activity → `Usage` | Qualifies `used`. |
| `prov:qualifiedCommunication` | Property (op) | Activity → `Communication` | Qualifies `wasInformedBy`. |
| `prov:qualifiedAssociation` | Property (op) | Activity → `Association` | Qualifies `wasAssociatedWith`. |
| `prov:qualifiedEnd` | Property (op) | Activity → `End` | Qualifies `wasEndedBy`. |
| `prov:qualifiedDelegation` | Property (op) | Agent → `Delegation` | Qualifies `actedOnBehalfOf`. |
| `prov:influencer` | Property (op) | `Influence` → (unspecified) | Cites the object of an unqualified triple whose predicate is a subproperty of `wasInfluencedBy`; superproperty of `entity`, `activity`, `agent` — used much like `rdf:object`. |
| `prov:entity` | Property (op), subproperty of `influencer` | `EntityInfluence` → Entity | Cites the influencing Entity. |
| `prov:activity` | Property (op), subproperty of `influencer` | `ActivityInfluence` → Activity | Cites the influencing Activity. |
| `prov:agent` | Property (op), subproperty of `influencer` | `AgentInfluence` → Agent | Cites the influencing Agent. |
| `prov:hadUsage` | Property (op) | `Derivation` → `Usage` | The optional Usage involved in an Entity's Derivation. |
| `prov:hadGeneration` | Property (op) | `Derivation` → `Generation` | The optional Generation involved in an Entity's Derivation. |
| `prov:hadPlan` | Property (op) | `Association` → `Plan` | The optional Plan adopted by an Agent in an Association with an Activity. |
| `prov:hadActivity` | Property (op) | `Delegation` ∪ `Derivation` ∪ `End` ∪ `Start` (∪ `Influence`) → Activity | The optional Activity of an Influence that used, generated, invalidated, or was responsible for an Entity. Not used by `ActivityInfluence` (use `prov:activity` there instead). |
| `prov:atTime` | Property (dp) | `InstantaneousEvent` → `xsd:dateTime` | The time at which an `InstantaneousEvent` occurred. |
| `prov:hadRole` | Property (op) | `Association` ∪ `InstantaneousEvent` (∪ `Influence`) → `Role` | The optional Role that an Entity or Agent assumed in the context of an Activity. |

### Worked example: unqualified → qualified

The source gives this exact before/after pair. First, the unqualified relation:

```turtle
:e1 a prov:Entity;
    prov:wasGeneratedBy :a1;
    .
:a1 a prov:Activity .
```

`prov:wasGeneratedBy` can be qualified using `prov:qualifiedGeneration`, the class `prov:Generation` (a subclass of `prov:ActivityInfluence`), and the property `prov:activity`. Restated with the qualification pattern, additional attributes (here an arbitrary `ex:foo`) can now be attached to the Generation event itself:

```turtle
:e1 a prov:Entity;
    prov:wasGeneratedBy :a1;
    prov:qualifiedGeneration :e1Gen;  # Add the qualification.
    .

:e1Gen a prov:Generation;
    prov:activity :a1;   # Cite the influencing Activity.
    ex:foo :bar;          # Describe the Activity :a1's influence upon the Entity :e1.
    .

:a1 a prov:Activity .
```

A second worked example — qualifying `used` with a role that has no direct property in the unqualified form:

```turtle
:sortActivity
    a prov:Activity;
    prov:startedAtTime "2011-07-16T01:52:02Z"^^xsd:dateTime;
    prov:qualifiedUsage [
        a prov:Usage;
        prov:entity :datasetA;       # The entity used by the prov:Usage
        prov:hadRole :inputToBeSorted; # the role of the entity in this prov:Usage
    ];
    prov:generated :datasetB;
    .

:datasetA a prov:Entity .
:datasetB a prov:Entity .
:inputToBeSorted a prov:Role .

## The role of :datasetA cannot be expressed using only starting-point terms:
:sortActivity
    a prov:Activity;
    prov:startedAtTime "2011-07-16T01:52:02Z"^^xsd:dateTime;
    prov:used :datasetA;
    prov:generated :datasetB;
    .
```

And qualifying `wasAssociatedWith` to attach a role and a plan:

```turtle
:illustrationActivity
    a prov:Activity;
    prov:wasAssociatedWith :derek;
    prov:qualifiedAssociation [
        a prov:Association;
        prov:agent :derek;
        prov:hadRole :illustrationist;
        prov:hadPlan :tutorial_blog;
    ];
    .

:derek a prov:Agent .
:tutorial_blog a prov:Plan, prov:Entity .
:illustrationist a prov:Role .
```

## See also

- [PROV_N.md](PROV_N.md) — the equivalent human-readable, non-RDF notation for the same PROV-DM concepts (record/identifier/attribute correspondences).
- [DATA_MODEL.md](DATA_MODEL.md) — the underlying conceptual definitions (PROV-DM) that PROV-O maps to RDF/OWL2; consult it for the abstract semantics behind any `prov:` term above.
