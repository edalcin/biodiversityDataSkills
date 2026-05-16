# Relações Parasito-Hospedeiro entre Espécies no Padrão Darwin Core

## Contexto

Este guia aborda a modelagem de relações **parasito-hospedeiro entre espécies** (conceitos taxonômicos) no padrão [Darwin Core](https://dwc.tdwg.org/) (DwC), utilizando o **Taxon Core** como base.

> ⚠️ **Importante:** A relação é entre **espécies**, não entre organismos/ocorrências individuais. Portanto, o core adequado é **Taxon**, não Occurrence.

---

## Abordagem 1: Taxon Core + ResourceRelationship Extension (Recomendada)

Esta é a abordagem **mais alinhada ao padrão TDWG** e **totalmente interoperável com o GBIF**. Cada espécie é um registro no Taxon Core, e a relação parasito-hospedeiro é modelada na extensão **ResourceRelationship**, conectada via `taxonID`.

### Estrutura do DwC-A

```
meu_arquivo.zip/
├── meta.xml                    ← Metadados descritivos
├── taxon.csv                   ← Core (registros de espécies)
└── resource_relationship.csv   ← Extension (relações entre espécies)
```

### taxon.csv (core)

| taxonID | scientificName | taxonomicStatus | kingdom | phylum | class | order | family | genus |
|---|---|---|---|---|---|---|---|---|
| TX-P-001 | *Toxoplasma gondii* | accepted | Animalia | Apicomplexa | Conoidasida | Eucoccidiorida | Sarcocystidae | *Toxoplasma* |
| TX-H-001 | *Felis catus* | accepted | Animalia | Chordata | Mammalia | Carnivora | Felidae | *Felis* |
| TX-H-002 | *Homo sapiens* | accepted | Animalia | Chordata | Mammalia | Primates | Hominidae | *Homo* |

### resource_relationship.csv (extension)

| taxonID (coreid) | resourceRelationshipID | relationshipOfResource | relatedResourceID | relationshipAccordingTo | relationshipEstablishedDate | relationshipRemarks |
|---|---|---|---|---|---|---|
| TX-P-001 | RR-001 | parasiteOf | TX-H-001 | Dubey, 2010 | — | Hospedeiro definitivo primário |
| TX-P-001 | RR-002 | parasiteOf | TX-H-002 | Dubey, 2010 | — | Hospedeiro intermediário |
| TX-H-001 | RR-003 | hostOf | TX-P-001 | Dubey, 2010 | — | — |
| TX-H-002 | RR-004 | hostOf | TX-P-001 | Dubey, 2010 | — | Pode causar toxoplasmose |

### Termos da extensão ResourceRelationship

| Termo | Descrição | Obrigatório |
|---|---|---|
| `resourceRelationshipID` | Identificador único da relação | Sim |
| `relationshipOfResource` | Tipo de relação (vocabulário controlado) | Sim |
| `relatedResourceID` | ID do recurso relacionado (taxonID) | Sim |
| `relationshipAccordingTo` | Fonte bibliográfica da relação | Não |
| `relationshipEstablishedDate` | Data de estabelecimento da relação | Não |
| `relationshipRemarks` | Observações sobre a relação | Não |

> 💡 **Nota:** O campo `taxonID` (primeira coluna da extensão) é o **coreid** — ele referencia o `taxonID` do registro no Taxon Core que é o **sujeito** da relação.

---

## Vocabulário Controlado para `relationshipOfResource`

| Termo | Sentido (sujeito → recurso relacionado) |
|---|---|
| `parasiteOf` | A espécie A é parasita da espécie B |
| `hostOf` | A espécie A é hospedeira da espécie B |
| `definitiveHostOf` | Hospedeiro definitivo |
| `intermediateHostOf` | Hospedeiro intermediário |
| `reservoirOf` | Reservatório |
| `vectorOf` | Vetor |
| `pathogenOf` | Patógeno |
| `ectoparasiteOf` | Parasita externo |
| `endoparasiteOf` | Parasita interno |
| `parasitoidOf` | Parasitóide (mata o hospedeiro) |

### Relação bidirecional

A relação parasito-hospedeiro é **inerentemente bidirecional**:

- Se `TX-P-001` é `parasiteOf` `TX-H-001`
- Então `TX-H-001` é `hostOf` `TX-P-001`

**Recomenda-se** incluir ambas as direções no arquivo `resource_relationship.csv` para maximizar a interoperabilidade e facilitar consultas em qualquer direção.

---

### meta.xml — Exemplo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<archive xmlns="http://rs.tdwg.org/dwc/text/">
  <core encoding="UTF-8" fieldsTerminatedBy="," fieldsEnclosedBy='"' rowsTerminatedBy="\n" ignoreHeaderLines="1">
    <files>
      <location>taxon.csv</location>
    </files>
    <coreRowType>http://rs.tdwg.org/dwc/terms/Taxon</coreRowType>
    <field index="0" term="http://rs.tdwg.org/dwc/terms/taxonID"/>
    <field index="1" term="http://rs.tdwg.org/dwc/terms/scientificName"/>
    <field index="2" term="http://rs.tdwg.org/dwc/terms/taxonomicStatus"/>
    <field index="3" term="http://rs.tdwg.org/dwc/terms/kingdom"/>
    <field index="4" term="http://rs.tdwg.org/dwc/terms/phylum"/>
    <field index="5" term="http://rs.tdwg.org/dwc/terms/class"/>
    <field index="6" term="http://rs.tdwg.org/dwc/terms/order"/>
    <field index="7" term="http://rs.tdwg.org/dwc/terms/family"/>
    <field index="8" term="http://rs.tdwg.org/dwc/terms/genus"/>
  </core>
  <extension encoding="UTF-8" fieldsTerminatedBy="," fieldsEnclosedBy='"' rowsTerminatedBy="\n" ignoreHeaderLines="1">
    <files>
      <location>resource_relationship.csv</location>
    </files>
    <coreRowType>http://rs.tdwg.org/dwc/terms/ResourceRelationship</coreRowType>
    <coreid index="0"/>
    <field index="1" term="http://rs.tdwg.org/dwc/terms/resourceRelationshipID"/>
    <field index="2" term="http://rs.tdwg.org/dwc/terms/relationshipOfResource"/>
    <field index="3" term="http://rs.tdwg.org/dwc/terms/relatedResourceID"/>
    <field index="4" term="http://rs.tdwg.org/dwc/terms/relationshipAccordingTo"/>
    <field index="5" term="http://rs.tdwg.org/dwc/terms/relationshipEstablishedDate"/>
    <field index="6" term="http://rs.tdwg.org/dwc/terms/relationshipRemarks"/>
  </extension>
</archive>
```

---

## Abordagem 2: SpeciesProfile Extension (simplificada)

A extensão **SpeciesProfile** (`gbif/1.0/SpeciesProfile`), associada ao Taxon Core, possui campos que podem expressar a natureza parasitária de uma espécie:

| Termo | Descrição |
|---|---|
| `isParasitic` | A espécie é parasita? (booleano) |
| `isHost` | A espécie é hospedeira? (booleano) |
| `host` | Nome do hospedeiro (texto livre) |

### Exemplo

| taxonID (coreid) | isParasitic | host |
|---|---|---|
| TX-P-001 | true | *Felis catus* |
| TX-H-001 | false | — |

> ⚠️ **Limitação:** Os campos `host` e `parasite` são **texto livre**, sem referência cruzada a IDs de taxa. Isso impossibilita consultas relacionais precisas do tipo *"quais parasitas afetam Felis catus?"*.

---

## Abordagem 3: dynamicProperties (simplificada / protótipo)

Usando o campo `dynamicProperties` (JSON) diretamente no Taxon Core:

| taxonID | scientificName | dynamicProperties |
|---|---|---|
| TX-P-001 | *Toxoplasma gondii* | `{"hostAssociations": [{"host": "Felis catus", "type": "definitiveHost"}, {"host": "Homo sapiens", "type": "intermediateHost"}]}` |

> ⚠️ **Problema:** `dynamicProperties` é um campo JSON opaco, **não pesquisável**, **não validável** por ferramentas padrão (GBIF, IPT). Use apenas para protótipos ou dados internos.

---

## Comparação das Abordagens

| Abordagem | Estrutura | Consultável por máquina | Publicável no GBIF | Complexidade |
|---|---|---|---|---|
| 🟢 **Taxon Core + ResourceRelationship** | Relacional com IDs | ✅ Sim | ✅ Sim | Média |
| 🟡 Taxon Core + SpeciesProfile | Texto livre | ⚠️ Parcial | ✅ Sim | Baixa |
| 🔴 Taxon Core + dynamicProperties | JSON opaco | ❌ Não | ✅ Aceito, mas desencorajado | Mínima |

---

## Recomendação Final

> ✅ **Use Taxon Core + ResourceRelationship Extension** para modelar relações parasito-hospedeiro entre espécies. Esta abordagem:
>
> - É **totalmente alinhada ao padrão TDWG/Darwin Core**
> - Permite **consultas programáticas** (ex.: *"quais hospedeiros de Toxoplasma gondii?"*)
> - É **compatível com publicação no GBIF** via IPT
> - Suporta **metadados associados** (fonte bibliográfica, data, observações)
> - Permite **relações N:N** (um parasita com múltiplos hospedeiros e vice-versa)

---

## Referências

- [Darwin Core (TDWG)](https://dwc.tdwg.org/)
- [ResourceRelationship Extension (GBIF)](https://rs.gbif.org/extension/dwc/resource_relationship_2025-07-10.xml)
- [Taxon Core (GBIF)](https://rs.gbif.org/core/dwc/taxon_2025-07-10.xml)
- [SpeciesProfile Extension (GBIF)](https://rs.gbif.org/extension/gbif/1.0/species_profile_2022-02-02.xml)
- [DwC-A Text Guide (meta.xml)](https://dwc.tdwg.org/text/)
- [GBIF IPT — Guia de publicação](https://ipt.gbif.org/manual/en/ipt/latest/)
