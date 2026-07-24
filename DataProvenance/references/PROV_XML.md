# PROV-XML: The PROV XML Schema

Source: [PROV-XML: The PROV XML Schema (W3C Note, 2013-04-30)](https://www.w3.org/TR/2013/NOTE-prov-xml-20130430/)

PROV-XML defines an XML Schema (XSD) that serializes instances of the PROV data model (see [DATA_MODEL.md](DATA_MODEL.md)) as XML documents. PROV-XML is a **W3C Working Group Note**, not a Recommendation — unlike PROV-DM, PROV-N, PROV-O, and PROV-CONSTRAINTS, which are Recommendations. All references from PROV-XML to those documents are therefore informative, not normative.

## 1. PROV namespace

The PROV namespace is `http://www.w3.org/ns/prov#`. All concepts, reserved names, and attributes introduced by PROV belong to this namespace, and the conventional prefix is `prov`. All schemas developed by the PROV Working Group (core and extensions) use this same namespace.

## 2. XML schema design conventions (source §2)

### 2.1 Schema modularization

xml-elements denoting terms defined by **PROV-DM** (the Recommendation) live in the core schema; xml-elements denoting terms defined by **PROV Working Group Notes** (e.g. PROV-Dictionary, PROV-Links) live in separate **extension schemas**. This keeps the normative core distinct from note-level extensions while still letting every PROV element be reached from one default schema:

| Schema | Location | Role |
|---|---|---|
| Main schema | `http://www.w3.org/ns/prov.xsd` | Aggregates (`xs:include`) the core schema and every extension schema, so all PROV xml-elements — core and extension — are reachable from one default schema. |
| Core schema | `http://www.w3.org/ns/prov-core.xsd` | Defines the XML representation of PROV-DM itself (all elements in the component tables below). |
| PROV-Dictionary extension | `http://www.w3.org/ns/prov-dictionary.xsd` | Defines elements for the key-entity-pair collection extension from [PROV-DICTIONARY]. |
| PROV-Links extension | `http://www.w3.org/ns/prov-links.xsd` | Defines `prov:mentionOf` (complexType `prov:Mention`, with `specificEntity`, `generalEntity`, `bundle` children, each `prov:IDRef`) from [PROV-LINKS]. |

Extension schemas `xs:include` the core schema and add their new elements to the substitution group of the abstract element `prov:internalElement`, which is how an extension-defined element becomes a valid member of a bundle or document alongside the core elements.

The default schema:

```xml
<?xml version="1.0" encoding="utf-8"?>
<xs:schema targetNamespace="http://www.w3.org/ns/prov#"
xmlns:xs="http://www.w3.org/2001/XMLSchema"
xmlns:prov="http://www.w3.org/ns/prov#"
elementFormDefault="qualified"
attributeFormDefault="unqualified">

<xs:include schemaLocation="prov-core.xsd"/>
<xs:include schemaLocation="prov-dictionary.xsd"/>
<xs:include schemaLocation="prov-links.xsd"/>

</xs:schema>
```

The PROV-Links extension schema, illustrating the substitution-group pattern:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
targetNamespace="http://www.w3.org/ns/prov#" xmlns:prov="http://www.w3.org/ns/prov#"
elementFormDefault="qualified">

<xs:include schemaLocation="prov-core.xsd" />

<xs:complexType name="Mention">
<xs:sequence>
<xs:element name="specificEntity" type="prov:IDRef" />
<xs:element name="generalEntity" type="prov:IDRef" />
<xs:element name="bundle" type="prov:IDRef" />
</xs:sequence>
</xs:complexType>

<xs:element name="mentionOf" type="prov:Mention" substitutionGroup="prov:internalElement" />

</xs:schema>
```

> Note (source): this substitution-group design on an abstract element can produce sub-optimal binding classes from Object-to-XML frameworks such as JAXB or JiBX; see the PROV FAQ for JAXB-specific guidance.

### 2.2 Salami slice design pattern

Each PROV concept is defined at the **top level** as a separate xml-element with its own distinct xml-type ("Salami Slice Design"), rather than nested inside one monolithic type. This makes every xml-type independently reusable for domain-specific extensions. `prov:document` exists as a convenient root element for a whole PROV-XML document, but using it as the root is **not required** — the salami-slice layout lets PROV elements be embedded inside mixed-schema XML documents that need a different root.

### 2.3 Elements vs. attributes

PROV-N (see [PROV_N.md](PROV_N.md)) uses two general syntactic patterns:

```text
thing(id, elem1, elem2, ..., [attr1=val1, attr2=val2])
concept(id; elem1, elem2, ... [attr1=val2, attr2=val2])
```

PROV-XML maps this onto XML as follows:

- The PROV-N `id` becomes the xml-attribute `prov:id`.
- PROV-N "elements" (`elem1, elem2, ...`) become xml-elements, always emitted in the **same fixed order** given by the PROV-DM/PROV-N description.
- PROV-N "attributes" (`attr1=val1, ...`) also become xml-elements, but are placed **after** all element-derived xml-elements, in **fixed alphabetical order**; unlike PROV-N, this fixed order applies even though PROV-N attributes may repeat.
- XML elements from namespaces other than PROV may follow the prov-"attribute" elements.
- Wherever an id is referenced from a later concept, it is carried as a `prov:ref` xml-attribute on an element inside that concept.

General XML pattern that results:

```xml
<prov:thing prov:id="id">
<prov:elem1 />
<prov:elem2 />
...
<ex:attr1>val1</ex:attr1>
<ex:attr2>val2</ex:attr2>
...
</prov:thing>
```

### 2.4 Type conventions

**2.4.1 PROV type attribute.** PROV-DM's `prov:type` prov-"attribute" (may occur multiple times on an entity, activity, agent, or relation) is represented by the repeatable xml-element `<prov:type>`, which can hold both PROV and non-PROV type values, e.g. `<prov:type xsi:type="xsd:QName">prov:Plan</prov:type>`.

**2.4.2 Extension types.** PROV-XML also defines complexTypes matching PROV-DM's prov-"type" values (e.g. `prov:Plan`), giving a more native XML representation. Any complexType denoting a prov-"type" that is a PROV-DM subclass of another prov-"type" is defined as an XSD extension of the parent type's complexType — e.g. `prov:Plan` extends complexType `prov:Entity`, so a Plan may be referenced by either a `<prov:plan>` or a `<prov:entity xsi:type="prov:Plan">` element. Using the dedicated element (e.g. `<prov:plan>`) lets a prov-"type" be *inferred* without an explicit `<prov:type>` child; the explicit `<prov:type>` element is nonetheless "highly encouraged" because it is easier for transformation tooling (e.g. XSLT) to process.

**2.4.3 XSI type.** The standard XSD `xsi:type` attribute is a third equivalent way to convey the same type information, e.g. `<prov:entity prov:id="..." xsi:type="prov:Plan">`; its value must be a complexType derived from the element's default xml-type, in a schema reachable via `xsi:schemaLocation`. A prov-"type" may likewise be inferred from `xsi:type` alone.

Other type conventions used throughout the schema (see the element tables below): `prov:InternationalizedString` for `prov:label` (supports `xml:lang`), `xs:anySimpleType` for `prov:location`, `prov:role`, `prov:type`, and `prov:value`, and `xs:dateTime` for all time values (`startTime`, `endTime`, `time`).

### 2.5 Identifier conventions

PROV-DM defines a PROV identifier as a **qualified name**: a name subject to namespace interpretation, consisting of a namespace (denoted by an optional prefix) and a local name, always mappable to a URI by concatenating the namespace URI with the local name.

- `prov:id` — the xml-attribute denoting a PROV identifier.
- `prov:ref` — the xml-attribute denoting a reference-by-id to an instance of a prov-"type" or prov-"relation" with a matching PROV identifier; there is no requirement that a matching `prov:id` actually exist anywhere in the document.

Both `prov:id` and `prov:ref` are typed `xsd:QName` in the schema, as the closest XSD datatype to PROV-DM's qualified name. `xsd:QName` is **more restrictive** than PROV-N's `QualifiedName` (e.g. PROV-N allows local names to start with a digit, `xsd:QName` does not) — so some valid PROV-N identifiers are not valid PROV-XML identifiers. Users should choose identifier schemes that map cleanly to both valid `xsd:QName`s and URIs.

### 2.6 Naming conventions

- **XML element names** are aligned with PROV-N record names (e.g. `prov:wasGeneratedBy`, `prov:actedOnBehalfOf`) and record parameter roles (e.g. `prov:delegate`, `prov:responsible` on a Delegation), and are written in **camelCase**, matching PROV-N conventions.
- **ComplexType names** are aligned with PROV-DM prov-"type" names (e.g. `prov:Generation`, `prov:Delegation`) and are written in **PascalCase**, which both matches PROV-DM conventions and visually differentiates complexTypes from xml-elements in the schema.

## 3. XML elements per component (source §3)

PROV-DM's six components (see [DATA_MODEL.md](DATA_MODEL.md)) map directly onto XML elements. In the tables below, an "IDRef" child is an xml-element typed `prov:IDRef` that carries a `prov:ref` attribute pointing at another element's `prov:id` (e.g. `<prov:entity prov:ref="ex:e1"/>`); `label*`/`location*`/`role*`/`type*` denote the repeatable prov-"attribute" elements `prov:label`, `prov:location`, `prov:role`, `prov:type`; `any*` denotes an optional, unbounded `xs:any namespace="##other"` extension point for non-PROV elements. All complexTypes below also accept a `prov:id` xml-attribute unless noted otherwise.

### Component 1: Entities and Activities

| Element | Key attributes/children | Meaning |
|---|---|---|
| `<prov:entity>` | `prov:id`; children: `label*`, `location*`, `type*`, `value?`, `any*` | Denotes a `prov:Entity`: a physical, digital, conceptual, or other kind of thing with some fixed aspects; entities may be real or imaginary. |
| `<prov:activity>` | `prov:id`; children: `startTime?` (`xsd:dateTime`), `endTime?` (`xsd:dateTime`), `label*`, `location*`, `type*`, `any*` | Denotes a `prov:Activity`: something that occurs over a period of time and acts upon or with entities — consuming, processing, transforming, modifying, relocating, using, or generating them. |
| `<prov:wasGeneratedBy>` | `prov:id`; children: `entity` (IDRef), `activity?` (IDRef), `time?` (`xsd:dateTime`), `label*`, `location*`, `role*`, `type*`, `any*` | Denotes a `prov:Generation`: completion of production of a new entity by an activity; the entity did not exist before generation and becomes available for usage after it. |
| `<prov:used>` | `prov:id`; children: `activity` (IDRef), `entity?` (IDRef), `time?`, `label*`, `location*`, `role*`, `type*`, `any*` | Denotes a `prov:Usage`: the beginning of an activity's utilization of an entity; before usage, the activity could not have been affected by the entity. |
| `<prov:wasInformedBy>` | `prov:id`; children: `informed` (IDRef), `informant` (IDRef), `label*`, `type*`, `any*` | Denotes a `prov:Communication`: the exchange of some unspecified entity by two activities, one using an entity generated by the other. |
| `<prov:wasStartedBy>` | `prov:id`; children: `activity` (IDRef), `trigger?` (IDRef), `starter?` (IDRef), `time?`, `label*`, `location*`, `role*`, `type*`, `any*` | Denotes a `prov:Start`: when an activity is deemed started by a `trigger` entity; the activity did not exist before its start. `starter` optionally names the activity that generated the trigger. |
| `<prov:wasEndedBy>` | `prov:id`; children: `activity` (IDRef), `trigger?` (IDRef), `ender?` (IDRef), `time?`, `label*`, `location*`, `role*`, `type*`, `any*` | Denotes a `prov:End`: when an activity is deemed ended by a `trigger` entity; the activity no longer exists after its end. `ender` optionally names the activity that generated the trigger. |
| `<prov:wasInvalidatedBy>` | `prov:id`; children: `entity` (IDRef), `activity?` (IDRef), `time?`, `label*`, `location*`, `role*`, `type*`, `any*` | Denotes a `prov:Invalidation`: the start of the destruction, cessation, or expiry of an existing entity by an activity; the entity is no longer available for use afterward. |

### Component 2: Derivations

| Element | Key attributes/children | Meaning |
|---|---|---|
| `<prov:wasDerivedFrom>` | `prov:id`; children: `generatedEntity` (IDRef), `usedEntity` (IDRef), `activity?` (IDRef), `generation?` (IDRef), `usage?` (IDRef), `label*`, `type*`, `any*` | Denotes a `prov:Derivation`: a transformation of an entity into another, an update of an entity resulting in a new one, or construction of a new entity based on a pre-existing one. |
| `<prov:wasRevisionOf>` | Same structure as `prov:wasDerivedFrom` — complexType `prov:Revision` is an empty XSD extension of `prov:Derivation` | Denotes a `prov:Revision`: a derivation for which the resulting entity is a revised version of some original. |
| `<prov:wasQuotedFrom>` | Same structure as `prov:wasDerivedFrom` — complexType `prov:Quotation` extends `prov:Derivation` | Denotes a `prov:Quotation`: the repeat of (some or all of) an entity, such as text or image, by someone who may or may not be its original author. |
| `<prov:hadPrimarySource>` | Same structure as `prov:wasDerivedFrom` — complexType `prov:PrimarySource` extends `prov:Derivation` | Denotes a `prov:PrimarySource`: something produced by an agent with direct experience and knowledge of a topic, at the time of the topic's study, without benefit of hindsight. |

### Component 3: Agents, Responsibility, and Influence

| Element | Key attributes/children | Meaning |
|---|---|---|
| `<prov:agent>` | `prov:id`; children: `label*`, `location*`, `type*`, `any*` | Denotes a `prov:Agent`: something that bears some form of responsibility for an activity taking place, for an entity's existence, or for another agent's activity. |
| `<prov:person>` | Same structure as `prov:agent` — `prov:Person` extends `prov:Agent` | Denotes a `prov:Person`: people. |
| `<prov:organization>` | Same structure as `prov:agent` — `prov:Organization` extends `prov:Agent` | Denotes a `prov:Organization`: a social or legal institution such as a company or society. |
| `<prov:softwareAgent>` | Same structure as `prov:agent` — `prov:SoftwareAgent` extends `prov:Agent` | Denotes a `prov:SoftwareAgent`: running software. |
| `<prov:wasAttributedTo>` | `prov:id`; children: `entity` (IDRef), `agent` (IDRef), `label*`, `type*`, `any*` | Denotes a `prov:Attribution`: the ascribing of an entity to an agent. |
| `<prov:wasAssociatedWith>` | `prov:id`; children: `activity` (IDRef), `agent?` (IDRef), `plan?` (IDRef), `label*`, `role*`, `type*`, `any*` | Denotes a `prov:Association`: assignment of responsibility to an agent for an activity, indicating the agent had a role in it; optionally names a `plan` the agent intended to follow. |
| `<prov:plan>` | Same structure as `prov:entity` — `prov:Plan` extends `prov:Entity` | Denotes a `prov:Plan`: an entity representing a set of actions or steps intended by one or more agents to achieve some goals. |
| `<prov:actedOnBehalfOf>` | `prov:id`; children: `delegate` (IDRef), `responsible` (IDRef), `activity?` (IDRef), `label*`, `type*`, `any*` | Denotes a `prov:Delegation`: assignment of authority and responsibility to an agent (by itself or by another agent) to act as a delegate carrying out a specific activity, while the responsible agent retains some responsibility for the outcome. |
| `<prov:wasInfluencedBy>` | `prov:id`; children: `influencee` (IDRef), `influencer` (IDRef), `label*`, `type*`, `any*` | Denotes a `prov:Influence`: the capacity of an entity, activity, or agent to affect the character, development, or behavior of another, generalizing usage, start, end, generation, invalidation, communication, derivation, attribution, association, and delegation. |

### Component 4: Bundles

| Element | Key attributes/children | Meaning |
|---|---|---|
| `<prov:bundle>` | Same structure as `prov:entity` — `prov:Bundle` extends `prov:Entity`; its `prov:id` must equal the corresponding `<prov:bundleContent>`'s `prov:id` | Denotes a `prov:Bundle`: a named set of provenance descriptions, itself an entity, enabling provenance of provenance to be expressed. |
| `<prov:bundleContent>` | `prov:id`; content: unbounded `xs:choice` of standard PROV elements (complexType `prov:BundleConstructor`) | Holds the nested provenance statements that make up a bundle's content. May appear only directly inside `prov:document` (never nested inside another `prov:bundleContent`); the associated `prov:bundle` entity may be declared at the `prov:document` level or inside any `prov:bundleContent`. |

### Component 5: Alternate Entities

| Element | Key attributes/children | Meaning |
|---|---|---|
| `<prov:specializationOf>` | No `prov:id`; children: `specificEntity` (IDRef), `generalEntity` (IDRef) | Denotes a `prov:Specialization`: an entity that specializes another shares all aspects of it while presenting more specific aspects of the same thing; the general entity's lifetime contains that of the specialization. |
| `<prov:alternateOf>` | No `prov:id`; children: `alternate1` (IDRef), `alternate2` (IDRef) | Denotes a `prov:Alternate`: two alternate entities present aspects of the same thing; the aspects may be the same or different, and the entities may or may not overlap in time. |

### Component 6: Collections

| Element | Key attributes/children | Meaning |
|---|---|---|
| `<prov:collection>` | Same structure as `prov:entity` — `prov:Collection` extends `prov:Entity` | Denotes a `prov:Collection`: an entity that provides a structure to some constituents, themselves entities, called members of the collection. |
| `<prov:emptyCollection>` | Same structure as `prov:collection` — `prov:EmptyCollection` extends `prov:Collection` | Denotes a `prov:EmptyCollection`: a collection without members. |
| `<prov:hadMember>` | No `prov:id`; children: `collection` (IDRef), `entity+` (IDRef, `maxOccurs="unbounded"`) | Denotes a `prov:Membership`: the belonging of an entity to a collection. |

### Further elements of PROV (source §3.7) and structural elements (source §3.8)

| Element/attribute | Key attributes/children | Meaning |
|---|---|---|
| `prov:id` (xml-attribute) | type `xsd:QName` | Identifies an instance of a prov-"type" or prov-"relation" (§2.5). |
| `prov:ref` (xml-attribute) | type `xsd:QName`, required where used | References, by id, an instance of a prov-"type" or prov-"relation" defined elsewhere (§2.5); no requirement that a matching `prov:id` exist. |
| `<prov:label>` | type `prov:InternationalizedString`; repeatable; supports `xml:lang` | Represents the `prov:label` prov-"attribute": a human-readable representation of an instance of a PROV-DM type or relation. |
| `<prov:location>` | type `xs:anySimpleType`; repeatable | Represents the `prov:location` prov-"attribute": an identifiable geographic place (ISO 19112) or a non-geographic place such as a directory, row, or column. |
| `<prov:role>` | type `xs:anySimpleType`; repeatable | Represents the `prov:role` prov-"attribute": the function of an entity or agent with respect to an activity, in the context of a usage, generation, invalidation, association, start, or end. |
| `<prov:type>` | type `xs:anySimpleType`; repeatable | Represents the `prov:type` prov-"attribute": further typing information for any construct, as an optional set of attribute-value pairs (§2.4). |
| `<prov:value>` | type `xs:anySimpleType`; at most one | Represents the `prov:value` prov-"attribute": a value that is a direct representation of an entity as a PROV-DM Value — a constant such as a string, number, time, qualified name, IRI, or encoded binary data, whose interpretation is outside PROV's scope. Relations with prov-"type" Value default to XSD type `xs:anySimpleType` unless otherwise specified. |
| `<prov:document>` | No `prov:id`; content: unbounded `xs:choice` of standard PROV elements plus an optional `bundleContent` (complexType `prov:Document`) | The root xml-element of a PROV-XML document. Unlike `prov:BundleConstructor`, may contain `prov:bundle` elements (but not nested `prov:document` elements) and carries no `prov:id`. May be used only as the document root. |
| `<prov:other>` | content: unbounded, `xs:any namespace="##other"` (complexType `prov:Other`) | Placeholder for including non-PROV xml-elements inside a `prov:document` or `prov:bundleContent`; may not be used inside a prov-"relation", entity, or activity element. |
| `prov:internalElement` (abstract element) | substitution-group head | Abstract element to whose substitution group every standard PROV element belongs; extension schemas (e.g. PROV-Links' `prov:mentionOf`) add elements to the valid-PROV-element set by joining this group (§2.1). |

## 4. Worked example

A complete, well-formed `<prov:document>` combining entities, an activity, an agent, and several relations (assembled from the schema's per-element examples in source §3):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<prov:document
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:prov="http://www.w3.org/ns/prov#"
    xmlns:ex="http://example.com/ns/ex#">

  <prov:entity prov:id="ex:e1">
    <prov:type xsi:type="xsd:QName">ex:dataset</prov:type>
  </prov:entity>

  <prov:entity prov:id="ex:e2">
    <prov:type xsi:type="xsd:QName">ex:report</prov:type>
  </prov:entity>

  <prov:activity prov:id="ex:a1">
    <prov:startTime>2011-11-16T16:05:00</prov:startTime>
    <prov:endTime>2011-11-16T16:06:00</prov:endTime>
    <prov:type xsi:type="xsd:QName">ex:analyse</prov:type>
  </prov:activity>

  <prov:agent prov:id="ex:ag1">
    <prov:type xsi:type="xsd:QName">prov:Person</prov:type>
  </prov:agent>

  <prov:used>
    <prov:activity prov:ref="ex:a1"/>
    <prov:entity prov:ref="ex:e1"/>
    <prov:time>2011-11-16T16:05:00</prov:time>
  </prov:used>

  <prov:wasGeneratedBy>
    <prov:entity prov:ref="ex:e2"/>
    <prov:activity prov:ref="ex:a1"/>
    <prov:time>2011-11-16T16:06:00</prov:time>
  </prov:wasGeneratedBy>

  <prov:wasAssociatedWith>
    <prov:activity prov:ref="ex:a1"/>
    <prov:agent prov:ref="ex:ag1"/>
    <prov:role xsi:type="xsd:QName">analyst</prov:role>
  </prov:wasAssociatedWith>

  <prov:wasDerivedFrom>
    <prov:generatedEntity prov:ref="ex:e2"/>
    <prov:usedEntity prov:ref="ex:e1"/>
    <prov:activity prov:ref="ex:a1"/>
  </prov:wasDerivedFrom>

  <prov:wasAttributedTo>
    <prov:entity prov:ref="ex:e2"/>
    <prov:agent prov:ref="ex:ag1"/>
  </prov:wasAttributedTo>

</prov:document>
```

This mirrors the element-ordering convention from §2.3: on each relation element, `prov:ref`-bearing children come first in schema-defined order, followed by any prov-"attribute" elements (`prov:time`, `prov:role`, `prov:type`, ...).

## 5. Media type (source §4)

| Field | Value |
|---|---|
| Internet Media Type | `application/provenance+xml` |
| Recommended file extension | `.provx` (all lowercase, all platforms) |
| Macintosh HFS file type | `TEXT` |
| Required parameters | none |
| Optional parameters | same as the `charset` parameter of `application/xml` per [RFC3023] §3.2 |
| Encoding considerations | same as `application/xml` per [RFC3023] §3.2 |
| Interoperability considerations | none known |
| Fragment identifier considerations | N/A |
| Magic number(s) | none beyond those of XML documents generally |
| Intended usage | COMMON |
| Restrictions on usage | none |
| Published specification | *PROV-XML: The PROV XML Schema*, Hua, Tilmes, Zednik (eds), Moreau — `http://www.w3.org/TR/prov-xml/`, 2013 |
| Applications using this type | any application publishing provenance information; PROV-XML is designed as an XML form of provenance |
| Author | The PROV-XML specification is a product of the W3C Provenance Working Group |
| Change controller | The W3C and the W3C Provenance Working Group |
| Contact | Ivan Herman, `ivan@w3.org` |

**Security considerations (source-registered, condensed):**

- Applications may dereference URIs found in PROV-XML data; this invokes the security considerations of the URI's scheme, and RFC3023 §10's privacy issues apply to HTTP URIs. Data from an inaccurate or malicious source can lead to inaccurate conclusions or dereferencing of unintended URIs — trust in consulted resources should be aligned with the sensitivity of the intended use.
- PROV-XML can present strings to users (e.g. via `prov:label`); applications rendering strings from untrusted PROV-XML documents must guard against misleading or malignant strings, per the XML media-type security guidance in [RFC3023] §10.
- Because a PROV-XML document is itself metadata about other resources, an untrusted PROV-XML document can mislead consumers about a third party resource's lineage; provenance of the PROV-XML document itself should be sought where relevant.
- PROV-XML uses QNames mappable to IRIs as term identifiers, so [RFC3987] §8 (IRIs) and [RFC3986] §7 (URI generic syntax) security issues apply, including confusable/look-alike characters across scripts or via combining characters — see the Unicode Security Considerations [UNISEC] and [RFC3987] §8 for guidance on matching similar-looking characters correctly.

## Schema documents (source Appendix A)

| Schema | Location | Contents |
|---|---|---|
| Main | `http://www.w3.org/ns/prov.xsd` | Aggregation of the core schema and every PROV-defined extension schema. |
| Core | `http://www.w3.org/ns/prov-core.xsd` | XML representation of PROV-DM. |
| PROV-Dictionary extension | `http://www.w3.org/ns/prov-dictionary.xsd` | Extension elements from [PROV-DICTIONARY]. |
| PROV-Links extension | `http://www.w3.org/ns/prov-links.xsd` | Extension elements from [PROV-LINKS] (`prov:mentionOf`). |
