# Darwin Core Extensions Registered with GBIF

Source: [https://rs.gbif.org/extensions.html](https://rs.gbif.org/extensions.html)
Last updated: 2026-05-16

---

## Core Types

Cores are the main record types in a Darwin Core Archive.

| Core | Namespace | RowType | Description |
|---|---|---|---|
| **Occurrence** | `http://rs.tdwg.org/dwc/terms/` | `dwc/terms/Occurrence` | Occurrence of an organism in nature |
| **Event** | `http://rs.tdwg.org/dwc/terms/` | `dwc/terms/Event` | Sampling or collection event |
| **Taxon** | `http://rs.tdwg.org/dwc/terms/` | `dwc/terms/Taxon` | Taxonomic classification |

---

## Extensions by Category

### 📸 Audiovisual / Media

#### Audiovisual Media Description (Audubon Core)
- **Name:** Multimedia
- **Namespace:** `http://rs.tdwg.org/ac/terms/`
- **RowType:** `ac/terms/Multimedia`
- **Latest version:** 2026-02-24
- **Description:** Metadata for biodiversity multimedia resources (images, audio, video). Based on the Audubon Core standard.
- **Associated core:** Occurrence, Taxon

#### Simple Multimedia (GBIF)
- **Name:** Multimedia
- **Namespace:** `http://rs.gbif.org/terms/1.0`
- **RowType:** `gbif/1.0/Multimedia`
- **Description:** Simple extension for exchanging metadata about multimedia resources.
- ⚠️ **Deprecated in favor of Audiovisual Media Description (Audubon Core)**

#### Simple Images (deprecated)
- **RowType:** `gbif/1.0/Image`
- ⚠️ **DEPRECATED** — Use Audiovisual Media Description instead

---

### 🧬 DNA / Genetics

#### DNA derived data
- **Name:** dnaDerivedData
- **Namespace:** `http://rs.gbif.org/terms/1.0/`
- **RowType:** `gbif/1.0/DNADerivedData`
- **Latest version:** 2024-07-11
- **Description:** DNA-derived data based on MIxS, GGBN and MIQE standards.
- **Associated core:** Occurrence, Event

---

### 📏 Measurements

#### Measurement or Facts (DwC)
- **Name:** MeasurementOrFacts
- **Namespace:** `http://rs.tdwg.org/dwc/terms/`
- **RowType:** `dwc/terms/MeasurementOrFact`
- **Latest version:** 2025-07-10
- **Description:** Measurements or facts associated with Occurrence, Event, or Taxon.
- **Associated core:** Occurrence, Event, Taxon

#### Extended Measurement Or Facts (OBIS/eMoF)
- **Name:** ExtendedMeasurementOrFact
- **Namespace:** `http://rs.iobis.org/obis/terms/`
- **RowType:** `obis/terms/ExtendedMeasurementOrFact`
- **Latest version:** 2023-08-28
- **Description:** Extended version of MeasurementOrFact with controlled vocabulary support.
- **Associated core:** Event (compatible with other cores)

---

### 🔗 Relationships

#### Resource Relationship (DwC)
- **Name:** ResourceRelationship
- **Namespace:** `http://rs.tdwg.org/dwc/terms/`
- **RowType:** `dwc/terms/ResourceRelationship`
- **Latest version:** 2025-07-10
- **Description:** Relationships between resources (e.g., related occurrences).
- **Associated core:** Occurrence, Event, Taxon

---

### 🔬 Identification

#### Identification History (DwC)
- **Name:** Identification
- **Namespace:** `http://rs.tdwg.org/dwc/terms/`
- **RowType:** `dwc/terms/Identification`
- **Latest version:** 2025-07-10
- **Description:** Species identification history (determinations).
- **Associated core:** Occurrence

---

### 🏛️ Types and Specimens

#### Types and Specimen (GBIF)
- **Name:** TypesAndSpecimen
- **Namespace:** `http://rs.gbif.org/terms/1.0`
- **RowType:** `gbif/1.0/TypesAndSpecimen`
- **Latest version:** 2026-05-05
- **Description:** Specimens and types (type specimens, type species, type genera).
- **Associated core:** Taxon

---

### ⏳ Chronometry

#### ChronometricAge (TDWG Chrono)
- **Name:** ChronometricAge
- **Namespace:** `http://rs.tdwg.org/chrono/terms/`
- **RowType:** `chrono/terms/ChronometricAge`
- **Latest version:** 2024-03-11
- **Description:** Chronometric age for non-contemporaneous records.
- **Associated core:** Occurrence

---

### 🌿 Ecology

#### Humboldt Ecological Inventory
- **Name:** HumboldtEcologicalInventory
- **Namespace:** `http://rs.tdwg.org/eco/terms/`
- **RowType:** `eco/terms/Event`
- **Latest version:** 2025-07-10
- **Description:** Ecological inventory data (extended events).
- **Associated core:** Event

#### GBIF Relevé
- **Name:** Releve
- **Namespace:** `http://rs.gbif.org/terms/1.0/`
- **RowType:** `gbif/1.0/Releve`
- **Description:** Vegetation plot survey (relevé) data with percentage coverage measurements.
- **Associated core:** Event

---

### 🌍 Distribution

#### Species Distribution (GBIF)
- **Name:** Distribution
- **Namespace:** `http://rs.gbif.org/terms/1.0`
- **RowType:** `gbif/1.0/Distribution`
- **Latest version:** 2022-02-02
- **Description:** Geographic distribution of a taxon.
- **Associated core:** Taxon

#### Species Profile (GBIF)
- **Name:** SpeciesProfile
- **Namespace:** `http://rs.gbif.org/terms/1.0`
- **RowType:** `gbif/1.0/SpeciesProfile`
- **Description:** Basic species profile with characteristics.
- **Associated core:** Taxon

---

### 📝 Descriptions

#### Taxon Description (GBIF)
- **Name:** Description
- **Namespace:** `http://rs.gbif.org/terms/1.0`
- **RowType:** `gbif/1.0/Description`
- **Description:** Textual taxon descriptions (useful for species pages).
- **Associated core:** Taxon

#### Vernacular Names (GBIF)
- **Name:** VernacularName
- **Namespace:** `http://rs.gbif.org/terms/1.0`
- **RowType:** `gbif/1.0/VernacularName`
- **Description:** Common/vernacular names for taxa.
- **Associated core:** Taxon

---

### 📚 References

#### Alternative Identifiers (GBIF)
- **Name:** Identifier
- **Namespace:** `http://rs.gbif.org/terms/1.0`
- **RowType:** `gbif/1.0/Identifier`
- **Description:** Alternative identifiers for records.

#### Literature References (GBIF)
- **Name:** Reference
- **Namespace:** `http://rs.gbif.org/terms/1.0`
- **RowType:** `gbif/1.0/Reference`
- **Description:** Bibliographic references.

---

### 🧪 GGBN (Global Genome Biodiversity Network)

Extensions for biological material samples (tissues, DNA, RNA).

| Extension | RowType | Description |
|---|---|---|
| **Material Sample** | `ggbn/terms/MaterialSample` | Material samples (tissues, DNA, RNA) |
| **Permit** | `ggbn/terms/Permit` | Permits and licenses |
| **Amplification** | `ggbn/terms/Amplification` | DNA amplifications |
| **DNA Cloning** | `ggbn/terms/Cloning` | DNA cloning |
| **Gel Image** | `ggbn/terms/GelImage` | Gel images |
| **Loan** | `ggbn/terms/Loan` | Material loans |
| **Preparation** | `ggbn/terms/Preparation` | Sample preparations |
| **Preservation** | `ggbn/terms/Preservation` | Sample preservations |

**Associated core:** MaterialSample

---

### 🌾 Germplasm (Genetic Resources)

Extensions for plant genetic resources (genebank accessions).

| Extension | RowType | Description |
|---|---|---|
| **GermplasmAccession** | `purl.org/germplasm/germplasmTerm#GermplasmAccession` | Genebank accessions |
| **MeasurementScore** | `purl.org/germplasm/germplasmTerm#MeasurementScore` | Trait characterization measurements |
| **MeasurementTrait** | `purl.org/germplasm/germplasmTerm#MeasurementTrait` | Trait descriptors |
| **MeasurementTrial** | `purl.org/germplasm/germplasmTerm#MeasurementTrial` | Field/greenhouse trials |

---

### 🌐 EOL (Encyclopedia of Life)

| Extension | RowType | Description |
|---|---|---|
| **EOL Media Extension** | `eol.org/schema/media/Document` | Media for EOL |
| **EOL References Extension** | `eol.org/schema/reference/Reference` | Bibliographic references for EOL |

---

## Deprecated Extensions

| Extension | Replaced by |
|---|---|
| Simple Images (`gbif/1.0/Image`) | Audiovisual Media (Audubon Core) |
| ChronometricAge (zooarchnet) | ChronometricAge (TDWG Chrono) |
| ChronometricDate (zooarchnet) | ChronometricAge (TDWG Chrono) |
| Germplasm (0.1, nordgen) | GermplasmAccession (purl.org) |

## Darwin Core Archive Structure with Extensions

```
my_archive.zip/
├── meta.xml                    ← Required: describes all files
├── occurrences.csv             ← Core (e.g. Occurrence)
├── multimedia.csv              ← Extension: images/media
└── identifications.csv         ← Extension: identification history
```

The `meta.xml` references both the core and extensions:

```xml
<archive>
    <core rowType="http://rs.tdwg.org/dwc/terms/Occurrence" ...>
        <files><location>occurrences.csv</location></files>
        <field ... />
    </core>
    <extension rowType="http://rs.tdwg.org/ac/terms/Multimedia">
        <files><location>multimedia.csv</location></files>
        <coreid index="0" />
        <field ... />
    </extension>
</archive>
```
