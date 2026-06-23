# Darwin Core Data Package Guide (DwC-DP)

**Status:** Ratified TDWG Standard  
**Date ratified:** 2026-05-26  
**URL:** https://dwc.tdwg.org/dp/  
**Versioned URL:** http://rs.tdwg.org/dwc/doc/dp/2026-05-26  
**Citation:** Darwin Core Maintenance Group. 2026. Darwin Core Data Package guide. Biodiversity Information Standards (TDWG). http://rs.tdwg.org/dwc/doc/dp/2026-05-26

## What is DwC-DP?

Darwin Core Data Package (DwC-DP) is a community container format for exchanging biodiversity data. It:
- Extends the [Frictionless Data Package specification](https://specs.frictionlessdata.io/)
- Implements the [Darwin Core Conceptual Model (DwC-CM)](https://dwc.tdwg.org/cm/)
- Supersedes the "star schema" constraint of Darwin Core Archives (DwC-A)
- Enables complex relational datasets with explicit inter-table relationships
- Is normative (all non-exempted sections define requirements for compliance)

## File Structure

```
datapackage.json     # Required: descriptor (structure + relationships)
eml.xml              # Optional: dataset metadata (EML format)
event.csv            # One or more CSV table files
occurrence.csv
...
```

Compression: gzip only (`.gz`). If zipped: `datapackage.json` and `eml.xml` MUST be at root level, MUST NOT be individually compressed. Individual CSV files MAY be compressed as `filename.csv.gz`.

## Descriptor (`datapackage.json`)

```json
{
  "profile": "http://rs.tdwg.org/dwc-dp/1.0/dwc-dp-profile.json",
  "id": "https://doi.org/10.xxxx/...",
  "created": "2025-09-08T09:52:03-03:00",
  "version": "1.0",
  "resources": [ ... ]
}
```

| Property | Requirement | Notes |
|---|---|---|
| `profile` | MUST | URL to DwC-DP profile at `rs.tdwg.org`; MUST include version |
| `id` | SHOULD | Preferably a DOI |
| `created` | SHOULD | ISO 8601 timestamp |
| `version` | SHOULD | Dataset version string |
| `resources` | MUST | Array with at least one resource |

Profile URL: `http://rs.tdwg.org/dwc-dp/1.0/dwc-dp-profile.json`  
A valid DwC-DP is also a valid Frictionless Data Package.

## Resources (Tables)

Each CSV file is a resource. DwC-DP table resources have additional requirements:

| Property | Requirement | Value |
|---|---|---|
| `name` | MUST | One of the reserved table names from DwC-DP profile |
| `path` | MUST | Path to the CSV file |
| `profile` | MUST | `"tabular-data-resource"` |
| `format` | SHOULD | `"csv"` or `"tsv"` |
| `mediatype` | MUST | `"text/csv"` |
| `schema` | MUST | Inline schema object (not a reference URL) |
| `encoding` | Conditional | Required if not UTF-8 |
| `dialect` | Conditional | Required if deviating from RFC 4180 defaults |

**Reserved table names:** see `enum` for `dwc-dp-resource-names` in the profile JSON at  
`http://rs.tdwg.org/dwc-dp/1.0/dwc-dp-profile.json`

Known tables include: `event`, `occurrence`, `agent`, and others defined in the profile.

**Table schemas** (all fields, PKs, FKs per table):  
`http://rs.tdwg.org/dwc-dp/1.0/table-schemas`

## Schema: Primary Keys and Foreign Keys

```json
{
  "fields": [...],
  "primaryKey": ["eventID"],
  "foreignKeys": [
    {
      "fields": "eventID",
      "predicate": "happened during",
      "reference": {
        "resource": "event",
        "fields": "eventID"
      }
    }
  ]
}
```

- `primaryKey`: REQUIRED if the field is referenced by another table. Values MUST match those defined in `rs.tdwg.org` schemas.
- `foreignKeys`: REQUIRED if the table has any FK relationships. All relationships MUST be expressed. Values MUST match those defined in `rs.tdwg.org` schemas.
- `predicate`: Optional string on foreignKey to declare relationship semantics (e.g., `"happened during"`, `"conducted by"`).
- Self-referencing FK: `"resource": ""` (empty string) references the same table.
- `missingValues`: Optional; follows Table Schema spec.

## Field Descriptors

Each field in a table schema:

| Property | Requirement | Example |
|---|---|---|
| `name` | MUST | `"eventID"` |
| `title` | MUST | `"Event ID"` |
| `description` | MUST | Human-readable definition (may differ from canonical term def) |
| `type` | MUST | `"string"`, `"number"`, etc. |
| `format` | SHOULD | `"default"`, `"uri"`, etc. |
| `dcterms:isVersionOf` | MUST | `"http://rs.tdwg.org/dwc/terms/eventID"` |
| `dcterms:references` | MAY | Versioned term URL |
| `rdfs:comment` | MAY | Canonical definition from the versioned term |
| `namespace` | MAY | `"dwc"`, `"dcterms"` |
| `comments` | MAY | Context-specific usage notes |
| `examples` | MAY | Context-specific examples |
| `constraints` | MAY | Validation constraints (Table Schema spec) |

**Shortcut:** Copy field descriptors directly from `rs.tdwg.org` table schemas to guarantee compliance.

## Minimal Example

**event.csv**
```
eventID,eventDate,locationID
S229876476,2025-04-26T20:57:00+02:00,https://ebird.org/hotspot/L43523233
```

**occurrence.csv**
```
occurrenceID,eventID,scientificName,organismQuantity,organismQuantityType
1,S229876476,Apus apus,3,individuals
2,S229876476,Troglodytes troglodytes,1,individuals
```

**datapackage.json** (abbreviated):
```json
{
  "profile": "http://rs.tdwg.org/dwc-dp/1.0/dwc-dp-profile.json",
  "resources": [
    {
      "name": "event",
      "path": "event.csv",
      "profile": "tabular-data-resource",
      "mediatype": "text/csv",
      "schema": {
        "fields": [
          {
            "name": "eventID",
            "title": "Event ID",
            "description": "An identifier for a dwc:Event.",
            "type": "string",
            "format": "default",
            "dcterms:isVersionOf": "http://rs.tdwg.org/dwc/terms/eventID"
          }
        ],
        "primaryKey": ["eventID"]
      }
    },
    {
      "name": "occurrence",
      "path": "occurrence.csv",
      "profile": "tabular-data-resource",
      "mediatype": "text/csv",
      "schema": {
        "fields": [
          {
            "name": "occurrenceID",
            "title": "Occurrence ID",
            "description": "An identifier for a dwc:Occurrence.",
            "type": "string",
            "format": "default",
            "dcterms:isVersionOf": "http://rs.tdwg.org/dwc/terms/occurrenceID"
          },
          {
            "name": "eventID",
            "title": "Event ID",
            "description": "An identifier for a dwc:Event.",
            "type": "string",
            "format": "default",
            "dcterms:isVersionOf": "http://rs.tdwg.org/dwc/terms/eventID"
          }
        ],
        "primaryKey": ["occurrenceID"],
        "foreignKeys": [
          {
            "fields": "eventID",
            "predicate": "happened during",
            "reference": {
              "resource": "event",
              "fields": "eventID"
            }
          }
        ]
      }
    }
  ]
}
```

## DwC-DP vs DwC-A (Darwin Core Archive)

| Feature | DwC-A (star schema) | DwC-DP |
|---|---|---|
| Format | ZIP (meta.xml + CSVs) | gzip (datapackage.json + CSVs) |
| Relationships | Star schema only (one core, many extensions) | Arbitrary relational (FK graph) |
| Relationship semantics | Implicit | Explicit `predicate` on foreignKeys |
| Standard | Older, operational | Ratified 2026-05-26, GBIF adoption pending |
| Schema source | meta.xml + GBIF registry | `rs.tdwg.org` table schemas |
| Validation | GBIF tools | Frictionless Data tools + DwC-DP profile |

## External Links
- Profile JSON: http://rs.tdwg.org/dwc-dp/1.0/dwc-dp-profile.json
- Table schemas: http://rs.tdwg.org/dwc-dp/1.0/table-schemas
- QRG: https://gbif.github.io/dwc-dp/qrg/
- Designer tool: https://gbif.github.io/dwc-dp/designer/
- Frictionless Data Package spec: https://specs.frictionlessdata.io/
