# Darwin Core Conceptual Model (DwC-CM)

**Status:** Ratified TDWG Standard  
**Date ratified:** 2026-05-26  
**URL:** https://dwc.tdwg.org/cm/  
**Versioned URL:** http://rs.tdwg.org/dwc/doc/cm/2026-05-26  
**Citation:** Darwin Core Maintenance Group. 2026. Darwin Core conceptual model. Biodiversity Information Standards (TDWG). http://rs.tdwg.org/dwc/doc/cm/2026-05-26

## Purpose

DwC-CM provides the **semantics of relationships between Darwin Core classes**. It fills the gap that existed since Darwin Core's inception: formal DwC defined terms grouped by class, but never specified how classes relate to each other.

DwC-CM is technology-agnostic (not a blueprint):
- Relational DB → joins across normalized tables
- Document DB → embedded nested objects
- Graph DB → explicit links between nodes

## Classes in the Model

| Class | Definition |
|---|---|
| **Event** | An action, process, or set of circumstances at some place during some time interval |
| **Occurrence** | A type of Event; establishes the state of an Organism at a place and time |
| **Survey** | A type of Event; biotic survey/inventory supporting presence, absence, and abundance inferences |
| **OrganismInteraction** | A type of Event; non-permanent interaction between two Organisms |
| **Organism** | A particular organism or defined group considered taxonomically homogeneous |
| **OrganismRelationship** | Permanent relationships between Organisms (e.g., mother of, sibling of) |
| **SurveyTarget** | Declares what was being sought in a Survey (taxa, traits, environmental conditions) |
| **MaterialEntity** | An entity identifiable, existing for some period, consisting in whole or in part of physical matter |
| **Identification** | A classification of a resource (typically: taxonomic determination assigning a Taxon to an Organism) |
| **Taxon** | A group of organisms considered to be taxonomically homogeneous; can occupy a rank in a hierarchy |
| **Location** | A spatial region or named place |
| **GeologicalContext** | Information enabling the assignment of an entity to a stratigraphic horizon |
| **ChronometricAge** | Age determination based on a dating method (e.g., radiocarbon) |
| **Agent** | A resource that acts or has the power to act (person, organization, group, device, software) |
| **Protocol** | A method used during an action |
| **MediaEntity** | A recorded entity (Still Image, Moving Image, Sound, Text) |
| **NucleotideAnalysis** | Analysis of a MaterialEntity following a MolecularProtocol |
| **NucleotideSequence** | A nucleotide sequence produced by a NucleotideAnalysis |
| **MolecularProtocol** | A Protocol for nucleotide analysis (records primers, target regions, etc.) |

> Note: `MaterialSample` is omitted from DwC-CM; treated as a MaterialEntity derived from another MaterialEntity.

## Key Relationships

### Event hierarchy
- Events nest: child Event contained spatially and temporally within parent Event (one parent only)
- Occurrence, OrganismInteraction, and Survey are specializations of Event (not combinable)
- Events must have a Location (even if unknown/not shared)
- Events may be conducted by Agents

### Occurrence
- Represents: (1) direct observation of an Organism, (2) indirect inference, or (3) absence of detection
- One Organism → many Occurrences (different ephemeral states each time)
- Permanent Organism traits = properties of Organism class, not Occurrence

### OrganismInteraction
- Has TWO relationships to Occurrence: `by` (actor/subject) and `with` (target/object)
- Typically requires two Occurrence instances (one per Organism)
- Self-directed behavior: one Occurrence, pointed to by both `by` and `with`

### Survey
- Follows Protocols
- Can have SurveyTargets (a priori or post facto filters)
- Occurrences reported by Survey may be incidental ("bycatch") or match SurveyTarget
- Supports inference of absence, abundance estimation

### MaterialEntity
- Gathered or sampled during an Event at a Location
- Can be `derived from` another MaterialEntity (skeleton from body, DNA extract from tissue)
- Can be `part of` a containing MaterialEntity (fossil in rock)
- Evidence for Identifications; gathering Event provides evidence for Occurrences

### Identification
- Made by an Agent
- Can be based on: Occurrence observation, MediaEntity, MaterialEntity, NucleotideAnalysis
- Multiple Identifications per Organism/MaterialEntity allowed (historical, differing opinions)

### NucleotideAnalysis (eDNA / metabarcoding / barcoding)
- MaterialEntity → NucleotideAnalysis (follows MolecularProtocol)
- Produces zero or more NucleotideSequences
- Evidence for Identifications → inferred Occurrence
- Supports: metabarcoding, metagenomics, qPCR, barcoding
- Note: inferred Occurrences should carry data quality/confidence measures

### Agent
- Related to any class via dedicated properties (e.g., `identifiedByID`, `recordedByID`)
- Agents relate to each other (person belongs to crew, crew deploys device)
- AgentRole pattern: joins Agent to another class with a declared relationship type

### MediaEntity
- Subject matter: Agents, Events, MaterialEntities, Occurrences
- Used as evidence for Identifications
- Can be a "region of interest" (part of parent MediaEntity)
- MaterialEntity can be created FROM a MediaEntity (e.g., 3D print from 3D model)

## Implementation Notes

**eventCategory `context`:** When one Event serves as spatio-temporal context for multiple activities (Occurrence + OrganismInteraction + MaterialEntity gathering), use `eventCategory = "context"` to flag it.

**Embedding shortcuts:** Implementations may subsume:
- Location info within Events
- Organism info within Occurrences
- Taxon info within Identifications

**Reference implementations:**
- [Darwin Core Data Package (DwC-DP)](https://dwc.tdwg.org/dp/) — tabular CSV format; canonical DwC-CM implementation
- openDS — JSON Schema for extended digital specimens

## Associated Tools
- [DwC-DP Quick Reference Guide](https://gbif.github.io/dwc-dp/qrg/) — contextual term definitions per table/field
- [DwC-DP Designer](https://gbif.github.io/dwc-dp/designer/) — explore relationships, build descriptors
