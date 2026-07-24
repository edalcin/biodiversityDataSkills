# PROV-N: The Provenance Notation

Source: [PROV-N: The Provenance Notation (W3C Recommendation, 2013-04-30)](https://www.w3.org/TR/2013/REC-prov-n-20130430/)

PROV-N is the human-readable, functional-style notation used throughout the PROV family of documents (PROV-DM, PROV-CONSTRAINTS) to write examples of provenance descriptions. It is not the interchange format used by applications (that role is filled by PROV-XML / PROV-O / RDF); PROV-N exists for illustration, teaching, and as the basis for the formal semantics of the PROV data model (PROV-SEM). Design goals: technology independence (a simple syntax mappable to several technologies), human readability (functional syntax style), and formality (a grammar amenable to parser generators).

Every PROV-N expression corresponds to one PROV-DM concept (Entity, Activity, Generation, Usage, ...). This file lists the exact syntax of every production; see [DATA_MODEL.md](DATA_MODEL.md) for the underlying conceptual definitions.

## 1. Grammar basics

### 1.1 Functional-style syntax

PROV-N adopts a functional-style syntax: a predicate name followed by an ordered list of terms in parentheses.

```text
entity(e1)
activity(a2, 2011-11-16T16:00:00, 2011-11-16T16:00:01)
```

reads as "entity e1" and "activity a2, which occurred between 2011-11-16T16:00:00 and 2011-11-16T16:00:01".

All PROV-DM **relations** involve two primary elements, the *subject* and the *object*, in that order, plus optional further elements:

```text
wasDerivedFrom(e2, e1)                    // e2 was derived from e1 (e2 = subject, e1 = object)
wasDerivedFrom(e2, e1, a, g2, u1)         // expanded with optional activity a, generation g2, usage u1
```

### 1.2 EBNF grammar conventions

The grammar is written in a subset of XML 1.1's EBNF notation. Symbols start with an initial capital letter if they are the start symbol of a regular language (terminals, e.g. `QUALIFIED_NAME`), otherwise lowercase (nonterminals, e.g. `expression`). Term syntax used in productions:

| Form | Meaning |
|---|---|
| `expr` | matches production for nonterminal symbol `expr` |
| `TERMINAL` | matches production for terminal symbol `TERMINAL` |
| `"abc"` | matches the literal string `abc` |
| `(term)?` | optional: matches term or nothing |
| `(term)+` | one or more occurrences of term |
| `(term)*` | zero or more occurrences of term |
| `(term \| term)` | matches one of the two terms |

Where suitable, PROV-N reuses production/terminal names from the SPARQL grammar [RDF-SPARQL-QUERY].

Two productions are entry points to the grammar:
- `expression` [2] — the core expressions of PROV-N (one alternative per PROV-DM concept: `entityExpression`, `activityExpression`, `generationExpression`, `usageExpression`, `startExpression`, `endExpression`, `invalidationExpression`, `communicationExpression`, `agentExpression`, `associationExpression`, `attributionExpression`, `delegationExpression`, `derivationExpression`, `influenceExpression`, `alternateExpression`, `specializationExpression`, `membershipExpression`, `extensibilityExpression`).
- `document` [1] — the wrapper for a set of expressions plus namespace declarations (see §4).

### 1.3 Optional terms and the `-` marker

Some terms in an expression are optional. If **none** of the optional terms in an expression are used, they are simply omitted (a shorter form):

```text
wasDerivedFrom(e2, e1, a, g2, u1)
wasDerivedFrom(e2, e1)                    // activity, generation, usage all omitted

activity(a2, 2011-11-16T16:00:00, 2011-11-16T16:00:01)
activity(a1)                              // start/end times omitted
```

But because term **position** matters, if only *some* optional terms are omitted, the missing ones must be marked with `-` so position is preserved:

```text
wasDerivedFrom(e2, e1, a, g2, u1)
wasDerivedFrom(e2, e1, -, -, u1)          // activity and generation omitted, usage present
wasDerivedFrom(e2, e1, a, -, -)           // activity present, generation and usage omitted
```

The succinct form is shorthand for the complete expression with all markers spelled out — `activity(a1)` ≡ `activity(a1, -, -)`.

### 1.4 Identifiers and attributes

Almost all expressions include an identifier (§1.5). Most also admit a set of attribute-value pairs delimited by square brackets. Rules:

- Identifiers are **required** (not optional) only for Entity, Activity, and Agent expressions; elsewhere they are optional.
- The identifier, when present, is always the **first** term in an expression.
- An **optional** identifier MUST be separated from the rest of the term list with a semicolon `;`. A **required** identifier uses a regular comma `,`. This lets an optional identifier be omitted entirely with no ambiguity.
- The attribute-value pair list, if present, is always the **last** term in an expression.

```text
wasDerivedFrom(e2, e1)                    // optional id omitted
wasDerivedFrom(d; e2, e1)                 // optional id 'd' given, separated by ';'
wasDerivedFrom(-; e2, e1)                 // optional id explicitly marked absent — equivalent to the first form

activity(ex:a1)                           // no attributes
activity(ex:a1, [])                       // empty attribute list — equivalent to no attributes
activity(ex:a1, [ex:param1="a", ex:param2="b"])   // two attributes
```

### 1.5 Qualified names / namespaces

An **identifier** (`identifier ::= QUALIFIED_NAME`) is a *qualified name*: a name subject to namespace interpretation, consisting of an optional prefix and a local name (`PN_PREFIX ":" PN_LOCAL`, or `PN_LOCAL` alone using the default namespace). A qualified name maps to an IRI by concatenating the IRI bound to the prefix with the local part. PROV-N's `QUALIFIED_NAME` is more permissive than XML `QName` / SPARQL `PrefixedName`: local parts allow extra IRI characters, `%`-escapes, and `\`-escapes for delimiter characters (`= ' ( ) , : ; " [ ]`, plus `. : -`) that would otherwise collide with PROV-N's own delimiters. See §3.7.1 details reproduced in the table below.

```text
document
prefix ex <http://example.org/1/>
default <http://example.org/2/>

entity(ex:a)     // IRI http://example.org/1/a
entity(b)        // IRI http://example.org/2/b   (default namespace, no prefix)
entity(ex:foo\?a\=1)  // \-escaped delimiter characters
endDocument
```

### 1.6 Comments

PROV-N supports two comment forms, treated as whitespace:
- `//` outside an `IRI_REF` or `STRING_LITERAL` — runs to end of line (or end of file).
- `/* ... */` outside an `IRI_REF` or `STRING_LITERAL`.

## 2. Expressions per component

Each table below lists the exact PROV-N production for every expression in a PROV-DM component, in the source's argument order. `optionalIdentifier` = `(identifierOrMarker ";")?`; `identifierOrMarker` = `identifier | "-"`; `timeOrMarker` = `time | "-"`; an `xIdentifierOrMarker` (e.g. `aIdentifierOrMarker`, `eIdentifierOrMarker`) = that identifier kind or `"-"`. `optionalAttributeValuePairs` = `("," "[" attributeValuePairs "]")?`.

### 2.1 Component 1: Entities and Activities

| Production | Syntax | Meaning |
|---|---|---|
| Entity | `entity(identifier, optionalAttributeValuePairs)` | Declares an Entity with required `id` and optional attributes. Example: `entity(tr:WD-prov-dm-20111215, [ prov:type="document" ])`. |
| Activity | `activity(identifier, (timeOrMarker, timeOrMarker)?, optionalAttributeValuePairs)` | Declares an Activity with required `id`, optional `startTime`, optional `endTime` (both times required together or both markers), and optional attributes. Example: `activity(ex:a10, 2011-11-16T16:00:00, 2011-11-16T16:00:01, [prov:type="createFile"])`. |
| Generation (unqualified/qualified) | `wasGeneratedBy(optionalIdentifier eIdentifier, (aIdentifierOrMarker, timeOrMarker)?, optionalAttributeValuePairs)` | An entity `eIdentifier` was generated, optionally by activity `aIdentifierOrMarker`, at `timeOrMarker`, with optional `id` and attributes. Example: `wasGeneratedBy(ex:g1; tr:WD-prov-dm-20111215, ex:edit1, 2011-11-16T16:00:00, [ex:fct="save"])`. At least one of id, activity, time, attributes MUST be present. |
| Usage (unqualified/qualified) | `used(optionalIdentifier aIdentifier, (eIdentifierOrMarker, timeOrMarker)?, optionalAttributeValuePairs)` | Activity `aIdentifier` used entity `eIdentifierOrMarker` at `timeOrMarker`, with optional `id` and attributes. Example: `used(ex:u1; ex:act2, ar3:0111, 2011-11-16T16:00:00, [ex:fct="load"])`. At least one of id, entity, time, attributes MUST be present. |
| Communication | `wasInformedBy(optionalIdentifier aIdentifier, aIdentifier, optionalAttributeValuePairs)` | The first activity (`informed`) was informed by the second activity (`informant`), with optional `id` and attributes. Example: `wasInformedBy(ex:inf1; ex:a1, ex:a2, [ex:param1="a", ex:param2="b"])`. |
| Start (unqualified/qualified) | `wasStartedBy(optionalIdentifier aIdentifier, (eIdentifierOrMarker, aIdentifierOrMarker, timeOrMarker)?, optionalAttributeValuePairs)` | Activity `aIdentifier` was started, optionally triggered by entity `eIdentifierOrMarker`, optionally caused by starting activity `aIdentifierOrMarker` (the `starter`), at `timeOrMarker`, with optional `id` and attributes. Example: `wasStartedBy(ex:start; ex:act2, ex:trigger, ex:act1, 2011-11-16T16:00:00, [ex:param="a"])`. At least one of id, trigger, starter, time, attributes MUST be present. |
| End (unqualified/qualified) | `wasEndedBy(optionalIdentifier aIdentifier, (eIdentifierOrMarker, aIdentifierOrMarker, timeOrMarker)?, optionalAttributeValuePairs)` | Activity `aIdentifier` was ended, optionally triggered by entity `eIdentifierOrMarker`, optionally caused by ending activity `aIdentifierOrMarker` (the `ender`), at `timeOrMarker`, with optional `id` and attributes. Example: `wasEndedBy(ex:end; ex:act2, ex:trigger, ex:act3, 2011-11-16T16:00:00, [ex:param="a"])`. At least one of id, trigger, ender, time, attributes MUST be present. |
| Invalidation (unqualified/qualified) | `wasInvalidatedBy(optionalIdentifier eIdentifier, (aIdentifierOrMarker, timeOrMarker)?, optionalAttributeValuePairs)` | Entity `eIdentifier` was invalidated, optionally by activity `aIdentifierOrMarker`, at `timeOrMarker`, with optional `id` and attributes. Example: `wasInvalidatedBy(ex:inv; tr:WD-prov-dm-20111215, ex:edit1, 2011-11-16T16:00:00, [ex:fct="save"])`. At least one of id, activity, time, attributes MUST be present. |

`generationExpression`/`usageExpression`/`startExpression`/`endExpression`/`invalidationExpression` each carry BOTH the qualified form (optional `id`, extra qualifying terms) and the unqualified two-term form (just subject and object) — PROV-N has one production per relation covering both, distinguished only by which optional terms are supplied.

### 2.2 Component 2: Derivations

| Production | Syntax | Meaning |
|---|---|---|
| Derivation | `wasDerivedFrom(optionalIdentifier eIdentifier, eIdentifier, (aIdentifierOrMarker, gIdentifierOrMarker, uIdentifierOrMarker)?, optionalAttributeValuePairs)` | The first entity (`generatedEntity`) was derived from the second (`usedEntity`), optionally via activity, generation, and usage identifiers, with optional `id` and attributes. Example: `wasDerivedFrom(ex:d; e2, e1, a, g2, u1, [ex:comment="a righteous derivation"])`. |
| Revision | *No dedicated production.* Expressed as `wasDerivedFrom(...)` with attribute `prov:type='prov:Revision'`. | A Revision is a Derivation whose subject is a revised version of the object. Example: `wasDerivedFrom(ex:d; e2, e1, a, g2, u1, [prov:type='prov:Revision', ex:comment="a righteous derivation"])`. |
| Quotation | *No dedicated production.* Expressed as `wasDerivedFrom(...)` with attribute `prov:type='prov:Quotation'`. | A Quotation is a Derivation where the subject is quoted from the object. Example: `wasDerivedFrom(ex:quoteId1; ex:blockQuote, ex:blog, ex:act1, ex:g, ex:u, [ prov:type='prov:Quotation' ])`. |
| Primary Source | *No dedicated production.* Expressed as `wasDerivedFrom(...)` with attribute `prov:type='prov:PrimarySource'`. | A PrimarySource is a Derivation where the object is a primary source for the subject. Example: `wasDerivedFrom(ex:sourceId1; ex:e1, ex:e2, ex:act, ex:g, ex:u, [ prov:type='prov:PrimarySource' ])` (source text notes the literal is written `prov:Primary-Source` in the normative rule statement but `prov:PrimarySource` in the worked example). |

### 2.3 Component 3: Agents, Responsibility, and Influence

| Production | Syntax | Meaning |
|---|---|---|
| Agent | `agent(identifier, optionalAttributeValuePairs)` | Declares an Agent with required `id` and optional attributes. Example: `agent(ex:ag4, [ prov:type='prov:Person', ex:name="David" ])`. Person/Organization/SoftwareAgent have no dedicated syntax — expressed as `agent(...)` with `prov:type='prov:Person'`, `'prov:Organization'`, or `'prov:SoftwareAgent'` respectively. |
| Attribution | `wasAttributedTo(optionalIdentifier eIdentifier, agIdentifier, optionalAttributeValuePairs)` | Entity `eIdentifier` is ascribed to agent `agIdentifier`, with optional `id` and attributes. Example: `wasAttributedTo(ex:attr; e, ag, [ex:license='cc:attributionURL' ])`. |
| Association | `wasAssociatedWith(optionalIdentifier aIdentifier, (agIdentifierOrMarker, eIdentifierOrMarker)?, optionalAttributeValuePairs)` | Activity `aIdentifier` was associated with agent `agIdentifierOrMarker`, optionally per plan `eIdentifierOrMarker`, with optional `id` and attributes. Example: `wasAssociatedWith(ex:assoc; ex:a1, ex:ag1, ex:e1, [ex:param1="a", ex:param2="b"])`. At least one of id, agent, plan, attributes MUST be present. Plan has no dedicated syntax — expressed as `entity(...)` with `prov:type='prov:Plan'`. |
| Delegation | `actedOnBehalfOf(optionalIdentifier agIdentifier, agIdentifier, (aIdentifierOrMarker)?, optionalAttributeValuePairs)` | The first agent (`delegate`) acted on behalf of the second (`responsible`), optionally for activity `aIdentifierOrMarker`, with optional `id` and attributes. Example: `actedOnBehalfOf(ex:del1; ex:ag2, ex:ag1, ex:a, [prov:type="contract"])`. |
| Influence | `wasInfluencedBy(optionalIdentifier eIdentifier, eIdentifier, optionalAttributeValuePairs)` | The first thing (`influencee`) was influenced by the second (`influencer`), with optional `id` and attributes. This is the generic superproperty of Generation, Usage, Communication, Start, End, Invalidation, Derivation, Attribution, Association, and Delegation. Example: `wasInfluencedBy(ex:infl1; e2, e1, [ex:param="a"])`. |

### 2.4 Component 4: Bundles

| Production | Syntax | Meaning |
|---|---|---|
| Bundle constructor | `bundle identifier (namespaceDeclarations)? (expression)* endBundle` | Names a named group of descriptions (`identifier`) with its own optional namespace declarations and a sequence of expressions. Bundles cannot nest — `bundle` is not itself an `expression`, so it cannot occur inside another `bundle`. Example: `bundle ex:author-view` / `prefix ex <http://example.org/>` / `agent(ex:Paolo, [ prov:type='prov:Person' ])` / ... / `endBundle`. |
| Bundle type | *No dedicated production.* Expressed as `entity(...)` with attribute `prov:type='prov:Bundle'`. | Describes a bundle's own provenance by referring to it as an entity. Example: `entity(ex:author-view, [ prov:type='prov:Bundle' ])`. |

Each identifier occurring in a bundle (including the bundle's own identifier) is interpreted against that bundle's namespace declarations, falling back to the enclosing document's declarations if the prefix is undeclared locally.

### 2.5 Component 5: Alternate Entities

| Production | Syntax | Meaning |
|---|---|---|
| Alternate | `alternateOf(eIdentifier, eIdentifier)` | The two entity identifiers (`alternate1`, `alternate2`) refer to aspects of the same thing. Example: `alternateOf(tr:WD-prov-dm-20111215, ex:alternate-20111215)`. |
| Specialization | `specializationOf(eIdentifier, eIdentifier)` | The first entity (`specificEntity`) is a specialization of the second (`generalEntity`) — narrower and more specific. Example: `specializationOf(tr:WD-prov-dm-20111215, tr:prov-dm)`. |

### 2.6 Component 6: Collections

| Production | Syntax | Meaning |
|---|---|---|
| Collection / EmptyCollection | *No dedicated production.* Expressed as `entity(...)` with attribute `prov:type='prov:Collection'` or `prov:type='prov:EmptyCollection'`. | A Collection is an entity that groups other entities; an EmptyCollection has no members. Example: `entity(ex:col1, [ prov:type='prov:Collection' ])` / `entity(ex:col2, [ prov:type='prov:EmptyCollection' ])`. |
| Membership | `hadMember(cIdentifier, eIdentifier)` | Collection `cIdentifier` has member entity `eIdentifier`. Example: `hadMember(ex:c, ex:e1) // ex:c contained ex:e1`. |

### 2.7 Extensibility expressions

| Production | Syntax | Meaning |
|---|---|---|
| Extensibility expression | `QUALIFIED_NAME "(" optionalIdentifier extensibilityArgument ("," extensibilityArgument)* optionalAttributeValuePairs ")"` | A general functional-style expression whose predicate is a qualified name with a non-empty prefix, for notions beyond core PROV-N. PROV-N parsers MUST be able to parse it syntactically; PROV gives it no semantics, so implementations MAY ignore it. Extensions MAY define more specific productions/interpretations. Example (a dictionary extension): `dictExt:hadMembers(mId; d, {("k1",e1), ("k2",e2), ("k3",e3)}, [])`. |
| Extensibility argument | `extensibilityArgument ::= identifierOrMarker \| literal \| time \| extensibilityExpression \| extensibilityTuple` | The allowed term kinds inside an extensibility expression's argument list. |
| Extensibility tuple | `extensibilityTuple ::= "{" extensibilityArgument ("," extensibilityArgument)* "}" \| "(" extensibilityArgument ("," extensibilityArgument)* ")"` | A parenthesized or braced group of extensibility arguments, e.g. a key-entity pair `("k1", e1)`. |

## 3. Shared building blocks

### 3.1 Identifier kinds

All of `eIdentifier`, `aIdentifier`, `agIdentifier`, `gIdentifier`, `uIdentifier`, `cIdentifier` reduce to the same production `identifier ::= QUALIFIED_NAME` — the different names only document which PROV-DM role (entity, activity, agent, generation, usage, collection) the identifier fills at that argument position. Each has a `...OrMarker` counterpart (`eIdentifierOrMarker`, etc.) meaning "that identifier kind, or `-`".

### 3.2 Attribute

`attribute ::= QUALIFIED_NAME`. Reserved attributes in the `prov:` namespace (meaning defined in [PROV-DM] §5.7.2): `prov:label`, `prov:location`, `prov:role`, `prov:type`, `prov:value`.

### 3.3 Literal

`literal ::= typedLiteral | convenienceNotation`.

- `typedLiteral ::= STRING_LITERAL "%%" datatype`, `datatype ::= QUALIFIED_NAME` — an explicitly typed value, e.g. `"1.01" %% xsd:float`.
- `convenienceNotation ::= STRING_LITERAL (LANGTAG)? | INT_LITERAL | QUALIFIED_NAME_LITERAL` — syntactic sugar: a bare string defaults to datatype `xsd:string` (optionally with a language tag, e.g. `"bonjour"@fr`); a bare (optionally signed) integer defaults to `xsd:integer`, e.g. `1234` or `-1234`; a single-quoted qualified name (`'ex:value'`) defaults to datatype `prov:QUALIFIED_NAME`.

```text
"abc" %% xsd:string        // same value as:
"abc"

"1234" %% xsd:integer      // same value as:
1234

"ex:value" %% prov:QUALIFIED_NAME   // same value as:
'ex:value'
```

**Reserved type values** (`prov:type`, meaning defined in [PROV-DM] §5.7.2.4): `prov:Bundle`, `prov:Collection`, `prov:EmptyCollection`, `prov:Organization`, `prov:Person`, `prov:Plan`, `prov:PrimarySource`, `prov:Quotation`, `prov:Revision`, `prov:SoftwareAgent`.

**Time values**: `time ::= DATETIME`, per `xsd:dateTime` [XMLSCHEMA11-2], e.g. `2011-11-16T16:00:00`.

### 3.4 Namespace declaration

```
namespaceDeclarations       ::= (defaultNamespaceDeclaration | namespaceDeclaration) (namespaceDeclaration)*
namespaceDeclaration        ::= "prefix" PN_PREFIX namespace
defaultNamespaceDeclaration ::= "default" IRI_REF
namespace                   ::= IRI_REF
```

A `namespaceDeclaration` binds a prefix to a namespace IRI; every qualified name using that prefix within scope belongs to that namespace. A `defaultNamespaceDeclaration` binds the *unprefixed* namespace. Scoping rules:

- A prefix-namespace declaration directly inside a `bundle` scopes to that bundle only.
- A prefix-namespace declaration directly inside a `document` scopes to the whole document, including nested bundles, *except* bundles that re-declare the same prefix.
- `namespaceDeclarations` MUST NOT re-declare the same prefix twice within one scope; a bundle MAY re-declare a prefix already declared in its enclosing document (shadowing it for that bundle).
- A `namespaceDeclaration` MUST NOT declare the reserved prefixes `prov` or `xsd` (see Table 1: `prov` = `http://www.w3.org/ns/prov#`, `xsd` = `http://www.w3.org/2000/10/XMLSchema#`).

```text
document
default <http://example.org/1/>
entity(e001)                 // IRI: http://example.org/1/e001

bundle e001                  // IRI: http://example.org/2/e001
default <http://example.org/2/>
entity(e001)                 // IRI: http://example.org/2/e001
endBundle
endDocument
```

## 4. Documents and namespaces

A `document` is the house-keeping construct that packages up PROV-N expressions and namespace declarations into a self-contained, exchangeable unit (e.g. the response to a provenance query, [PROV-AQ]). Because of this role, `document` is *not* itself a PROV-N `expression`.

```
document ::= "document" (namespaceDeclarations)? (expression)* (bundle)* "endDocument"
```

A document contains, in order: optional namespace declarations, zero or more `expression`s, and zero or more `bundle`s. Bundles MAY occur inside a document but never inside another bundle.

```text
document
default <http://anotherexample.org/>
prefix ex <http://example.org/>

entity(e2, [ prov:type="File", ex:path="/shared/crime.txt", ex:creator="Alice",
ex:content="There was a lot of crime in London last month."])
activity(a1, 2011-11-16T16:05:00, -, [prov:type="edit"])
wasGeneratedBy(e2, a1, -, [ex:fct="save"])
wasAssociatedWith(a1, ag2, -, [prov:role="author"])
agent(ag2, [ prov:type='prov:Person', ex:name="Bob" ])

endDocument
```

## 5. Extensibility

The PROV data model is already extensible through `prov:type` and `prov:role` attributes for subtyping expressions. Where that is not enough, PROV-N additionally allows novel predicate syntax via `extensibilityExpression` (§2.7):

- PROV-N compliant parsers MUST be able to parse expressions matching `extensibilityExpression`.
- Since PROV defines no semantics for these expressions, compliant implementations MAY ignore them.
- Extensions to PROV/PROV-N MAY define more specific productions and interpretations for these expressions, which applications MAY choose to follow.

The predicate of an `extensibilityExpression` MUST be a qualified name with a non-empty prefix (distinguishing it from the fixed, unprefixed core predicates like `entity`, `wasGeneratedBy`, etc.).

## 6. Media type

The Internet Media Type of PROV-N is **`text/provenance-notation`**, always UTF-8 encoded. The recommended file extension is `.provn` (lowercase); on Macintosh HFS file systems the recommended file type is `TEXT`. Required parameter: `charset` — MUST always be UTF-8. No optional parameters. Encoding considerations: 8bit; code points may also be expressed with `\uXXXX` (U+0–U+FFFF) or `\UXXXXXXXX` (U+10000 onward) escapes. Magic number: documents typically contain the string `document` near the start. No known interoperability issues. Intended usage: COMMON.
