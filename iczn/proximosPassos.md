# Skill `iczn` — estado e próximos passos

Última atualização: 2026-08-26. A skill está **construída, commitada e no `main`**.
Este documento cobre só o que falta: a fase de avaliação.

---

## 0. Estado atual (confirmado no repositório)

Commits no `main`, já com `git push` feito:

```
efb6d04  docs: list iczn skill in README
877af4e  feat(iczn): add ICZN skill (zoological nomenclature)
```

Conteúdo em `iczn/` na raiz do repositório:

```
iczn/
├── SKILL.md                17 KB, roteiro de decisão em 6 perguntas
├── .gitignore               .cache/
├── promptInicial.txt        prompt original do usuário que originou a skill
├── references/              24 arquivos, ~2.285 linhas
│   ├── 01-nomenclature.md … 18-regulations.md   (Arts. 1-90, um arquivo por capítulo)
│   ├── glossary.md          296 termos, colunas Governing Article + pt-BR
│   ├── appendices.md        Apêndices A/B, marcados advisory
│   ├── zoobank.md           Art. 8.5, emenda de 2012, LSIDs
│   ├── data-modeling.md     nome/táxon/ato, 8 casos difíceis, anti-padrões
│   ├── dwc-mapping.md       campos Darwin Core + exemplo trabalhado
│   └── other-codes.md       fronteira com ICNafp/ICNP
└── scripts/                 só biblioteca padrão, sem requirements.txt
    ├── code_index.json      90 Artigos → URL, capítulo, arquivo, hash
    ├── explain.py           consulta offline (Artigo, termo, busca livre)
    ├── validate_name.py     violation/warning/info, --selftest com 21 asserções
    ├── fetch_article.py     texto exato da fonte (código.iczn.org)
    └── sync.py               detecta emenda upstream, nunca reescreve sozinho
```

`README.md` já lista a skill na tabela **Skills** e em dois casos de uso da tabela
**Skills Interoperability**.

`python3 iczn/scripts/validate_name.py --selftest` passa a partir da raiz do repositório.

**O que NÃO está no repositório, de propósito:** `iczn/.cache/` (as 101 páginas
raspadas de `code.iczn.org`, matéria-prima da escrita). Fica fora do git pelo
`.gitignore` — é cópia de obra protegida (© International Trust for Zoological
Nomenclature 1999), não deve ser redistribuída. Está preservada localmente em
`~/iczn-build/iczn-cache.tar.gz` nesta máquina; se precisar recriar em outra
máquina, o procedimento está na seção 4 abaixo.

---

## 1. O que falta: avaliação da skill

Nenhuma corrida de teste foi feita ainda. É a única fase pendente do ciclo do
`skill-creator`. Os três prompts de teste e a planilha suja já foram redigidos
numa sessão anterior — estão prontos para uso, só faltou executar.

### Passo 1 — criar `iczn/evals/`

Dois arquivos: `iczn/evals/evals.json` e `iczn/evals/nomes_colecao.csv`.

**`nomes_colecao.csv`** — planilha de coleção zoológica, suja de propósito; cada
linha aciona uma regra específica da skill:

```csv
catalogNumber,scientificName,taxonRank,author,year,status,typeStatus,notes
MZ-1001,Aus mülleri,species,"Müller",1899,valid,holotype,coletado no Pará
MZ-1002,aus muelleri,species,"Muller",1899,synonym,,grafia alternativa na etiqueta
MZ-1003,Aus bus,species,"Smith",1900,valid,syntype,3 exemplares
MZ-1004,Aus bus,species,"Jones",1955,valid,holotype,descrito de Minas Gerais
MZ-1005,Ausidae,family,"Smith",1900,valid,,
MZ-1006,Ausinae,family,"Smith",1900,valid,,
MZ-1007,Panthera onca,species,"(Linnaeus)",1758,valid,,
MZ-1008,Felis onca,species,"Linnaeus",1758,synonym,,combinação original
MZ-1009,Xus rubrum,species,"Costa",2021,valid,paratype,publicado só em PDF online
MZ-1010,Xus2 flavus,species,"Costa",2021,valid,,erro de digitação?
MZ-1011,Bison bison,species,"(Linnaeus)",1758,valid,,
MZ-1012,Aus caeruleus,species,"Reis",1930,valid,,
MZ-1013,Aus ceruleus,species,"Lima",1962,valid,,
MZ-1014,Yus smithi,species,"Alves",1988,valid,neotype,neótipo designado 2019
```

O que cada linha testa: `mülleri` diacrítico (Art. 27); `aus muelleri` inicial
minúscula (Art. 28); `Aus bus` Smith 1900 vs Jones 1955 homonímia primária
(Art. 57.2); `Ausinae` declarado family mas `-inae` é subfamily (Art. 29.2);
`Panthera onca` com parênteses (Art. 51.3) e sua combinação original na linha
seguinte; `Xus rubrum` só em PDF online (Art. 8.5, ZooBank); `Xus2` dígito
(Art. 11.2); `Bison bison` tautonímia lícita (Art. 18); `caeruleus`/`ceruleus`
variantes do Art. 58; `Yus smithi` com neótipo (Art. 75.3). A coluna `status`
mistura de propósito status nomenclatural e taxonômico.

**Três prompts de teste**, em português (testa também a regra de responder no
idioma do usuário, já que o conteúdo da skill é em inglês):

**Eval 0 — `electronic-publication-zoobank`**
> Estou finalizando a descrição de uma espécie nova de Chrysomelidae. A revista onde vou
> publicar é só online, em PDF, tem ISSN, e o artigo sai com DOI. Meu orientador disse
> que basta o DOI e que ZooBank é opcional. Eu já tenho holótipo depositado no MZUSP com
> número de tombo. Está tudo certo para submeter? O que exatamente preciso fazer para o
> nome não ter problema depois?

Esperado: identificar que o Art. 8.5 exige ISSN/ISBN **e** registro prévio da obra no
ZooBank com a evidência declarada na própria obra, e que sem isso o nome é
**indisponível** — não meramente irregular. Corrigir o orientador: DOI não substitui,
ZooBank não é opcional em publicação eletrônica. Sinalizar também Art. 16.1 (indicação
expressa de que o nome é novo) e Art. 16.4 (fixação explícita de tipo com o depositário).
Citar Artigo em tudo.

**Eval 1 — `forgotten-senior-synonym-art-23-9`**
> Trabalho com Cerambycidae neotropicais. Descobri que o nome que todo mundo usa desde
> os anos 1950 para uma praga florestal importante, *Aus xus* Schmidt, 1952, é sinônimo
> júnior de *Aus wus* Pereira, 1889 — o nome do Pereira nunca mais foi usado depois da
> descrição original, achei só a publicação de 1889 e nada mais. O *Aus xus* aparece em
> dezenas de trabalhos, é nome consagrado. Posso simplesmente declarar o *Aus wus* como
> *nomen oblitum* no meu artigo de revisão e manter o *Aus xus*? Como faço isso
> corretamente?

Esperado: dizer que o Art. 23.9.1 tem **duas** condições **conjuntivas** — 23.9.1.1
(sênior não usado como válido depois de 1899, satisfeita aqui) **e** 23.9.1.2 (júnior
usado como válido em pelo menos 25 obras, por pelo menos 10 autores, nos 50 anos
imediatamente anteriores, abrangendo pelo menos 10 anos). Dizer que "dezenas de
trabalhos" não é evidência do limiar 25/10 e que o autor precisa documentá-lo. Se não
der para documentar, o caso **tem** de ir à Comissão pelo Art. 23.9.3 (plenary power,
Art. 81), mantendo o uso corrente enquanto pende (Art. 82). Acertar a terminologia:
júnior = *nomen protectum*, sênior = *nomen oblitum*, e é **ato publicado** (Art. 23.9.2),
não conclusão privada.

Este é o caso que mata o baseline: um modelo sem a skill lembra a primeira condição e
esquece a segunda, com toda a confiança do mundo.

**Eval 2 — `collection-spreadsheet-triage`** (com `nomes_colecao.csv` anexo)
> Segue a planilha da nossa coleção zoológica (nomes_colecao.csv). Antes de publicar
> isso no GBIF eu preciso saber o que está errado do ponto de vista nomenclatural e como
> eu deveria reestruturar as colunas. A coluna 'status' foi preenchida por três
> estagiários diferentes ao longo dos anos e eu desconfio dela. Me diz o que consertar,
> o que é erro de verdade e o que só precisa de conferência.

Esperado: achar os defeitos concretos listados acima; diagnosticar a coluna `status`
como mistura de `nomenclaturalStatus` com `taxonomicStatus` e recomendar a separação;
separar `scientificName` de `scientificNameAuthorship`; tratar os parênteses de
*Panthera onca* como derivados da combinação (Art. 51.3); sinalizar MZ-1009 para
verificação de ZooBank; e **distinguir violação de item que precisa de conferência
humana**.

Formato de `evals/evals.json` (ver `skill://skill-creator` → `references/schemas.md`
para o schema completo — campo `assertions` fica vazio nesta etapa, é preenchido no
passo 3):

```json
{
  "skill_name": "iczn",
  "evals": [
    {"id": 0, "name": "electronic-publication-zoobank", "prompt": "...", "expected_output": "...", "files": []},
    {"id": 1, "name": "forgotten-senior-synonym-art-23-9", "prompt": "...", "expected_output": "...", "files": ["nomes_colecao.csv"]},
    {"id": 2, "name": "collection-spreadsheet-triage", "prompt": "...", "expected_output": "...", "files": ["nomes_colecao.csv"]}
  ]
}
```

### Passo 2 — rodar os seis subagentes de uma vez

Três com a skill, três sem (baseline = sem skill nenhuma, porque a skill é nova).
Workspace fora do repositório, por exemplo `../iczn-workspace/iteration-1/` (não
versionar resultados de avaliação junto com a skill).

```
iczn-workspace/iteration-1/eval-<id>-<nome>/
  ├── with_skill/outputs/
  ├── without_skill/outputs/
  └── eval_metadata.json
```

Cada subagente recebe: caminho da skill (`iczn/`, para as corridas "with_skill"),
o prompt, os arquivos de entrada (`nomes_colecao.csv` quando aplicável), e onde
salvar a saída. Instruir explicitamente a **não** rodar formatters/linters/testes
do projeto.

Gravar `eval_metadata.json` por caso (`eval_id`, `eval_name`, `prompt`,
`assertions: []`) e `timing.json` (`total_tokens`, `duration_ms`) assim que cada
notificação de subagente chegar — é a única oportunidade de capturar isso.

### Passo 3 — escrever as asserções (pode ser feito enquanto as corridas rodam)

Objetivamente verificáveis, nome descritivo para aparecer bem no visualizador:

- **Eval 0:** cita Art. 8.5; diz explicitamente que o nome seria indisponível sem
  ZooBank; corrige a afirmação de que DOI basta; cita Art. 16.4 (fixação de tipo);
  não inventa número de Artigo.
- **Eval 1:** enuncia as duas condições do Art. 23.9.1; dá os números 25 obras / 10
  autores / 50 anos / 10 anos; marca as condições como conjuntivas; atribui *nomen
  protectum* ao júnior e *nomen oblitum* ao sênior; encaminha à Comissão pelo
  Art. 23.9.3 quando 23.9.1.2 não é comprovável; trata como ato publicado (Art. 23.9.2).
- **Eval 2:** identifica a homonímia primária de *Aus bus*; identifica
  `Ausinae`/`-inae` contra o rank family; identifica o dígito em `Xus2`; recomenda
  separar `nomenclaturalStatus` de `taxonomicStatus`; sinaliza `caeruleus`/`ceruleus`
  como conferência e não como correção automática; sinaliza MZ-1009 para ZooBank.

Atualizar `evals/evals.json` e os `eval_metadata.json` com elas.

### Passo 4 — corrigir, agregar, abrir o visualizador

Graduar cada corrida (`grading.json`, campos exatamente `text`/`passed`/`evidence` —
o visualizador depende desses nomes). Agregar com, rodado de dentro do diretório do
skill-creator (não deste repositório):

```bash
python -m scripts.aggregate_benchmark <workspace>/iteration-1 --skill-name iczn
```

Depois:

```bash
nohup python /home/edalcin/.agents/skills/skill-creator/eval-viewer/generate_review.py \
  <workspace>/iteration-1 --skill-name "iczn" \
  --benchmark <workspace>/iteration-1/benchmark.json > /dev/null 2>&1 &
```

**Abrir o visualizador antes de julgar as saídas por conta própria** — o humano vê
primeiro.

### Passo 5 — iterar

Ler `feedback.json`, revisar a skill conforme o feedback, rodar `iteration-2` com
`--previous-workspace`, repetir até o usuário se dar por satisfeito. A cada
iteração que alterar `iczn/`, commitar e sincronizar como nas duas rodadas
já feitas.

### Passo 6 — otimizar a descrição do frontmatter (só no fim, com a skill estável)

20 queries de disparo (8–10 que devem disparar, 8–10 near-misses que não devem —
as difíceis são as vizinhas: pergunta sobre nomenclatura botânica, pergunta sobre
identificação taxonômica que não é nomenclatura, pergunta de Darwin Core que é da
outra skill). Revisar com o usuário via `assets/eval_review.html` do skill-creator,
depois:

```bash
python -m scripts.run_loop --eval-set <path> --skill-path <repo>/iczn \
  --model <modelo desta sessão> --max-iterations 5 --verbose
```

Aplicar o `best_description` resultante ao frontmatter de `iczn/SKILL.md`, commitar
e sincronizar.

---

## 2. Coisas que não devem se perder ao iterar

1. **Nunca transcrever o Code.** É a decisão de origem e a razão da arquitetura
   inteira — o Code é "All rights reserved" © International Trust for Zoological
   Nomenclature 1999. Toda regra em `references/` é redigida por nós, com citação
   de Artigo obrigatória. Se precisar da letra exata, usa `fetch_article.py`.
2. **Nunca inventar número de Artigo.** Foi o pior modo de falha identificado na
   construção — vários subagentes corrigiram números que eu havia passado errado,
   conferindo contra o cache em vez de confiar no que estava escrito.
3. **Artigo é obrigatório, Recommendation não é** (Art. 89.2). Vale para os
   Apêndices A e B também.
4. **`violation` e `warning` não se misturam** no `validate_name.py`. Concordância
   de gênero (Art. 31.2) é sempre `warning`, nunca `violation` — promover isso a
   violação seria regressão, e o `--selftest` falha de propósito se isso acontecer.
5. **Disponibilidade é permanente e do nome; validade é opinião e do conceito.**
   É o eixo de `data-modeling.md` e `04-availability.md`.
6. **A skill não tem autoridade** (Art. 87: só os textos inglês e francês têm).
   Está escrito no `SKILL.md` e precisa continuar escrito.
7. **`.cache/` nunca entra no git.** Está no `.gitignore` por decisão de copyright,
   não por descuido.

---

## 3. Decisões de design já fechadas (para não reabrir sem necessidade)

Nove rodadas de grilling resultaram nestas decisões, todas já implementadas:

| # | Decisão |
|---|---|
| 1 | Síntese autoral com citação obrigatória, não transcrição |
| 2 | Code + processo da Comissão + ZooBank dentro; outros códigos só como fronteira |
| 3 | `references/` por capítulo + roteiro de decisão no `SKILL.md` |
| 4 | Quatro scripts: `explain.py`, `validate_name.py`, `fetch_article.py`, `sync.py` |
| 5 | Mapeamento DwC + modelo conceitual nome-vs-táxon, sem DDL versionado |
| 6 | Conteúdo em inglês, resposta no idioma do usuário, glossário com coluna pt-BR |
| 7 | Cache local fora do git, `sync.py` alerta mas não reescreve |
| 8 | Seção `## Pending / contested` isolada no fim do `SKILL.md` |
| 9 | Avaliação com casos de teste e baseline comparativo |

---

## 4. Como regenerar o cache local, se precisar reescrever alguma referência

O cache (~292 KB) não está no git. Está preservado em
`~/iczn-build/iczn-cache.tar.gz` nesta máquina. Para recriar do zero em outra
máquina ou se o arquivo se perder:

```python
# 1. Enumerar: baixar https://code.iczn.org/menus/sidemenu com UA de navegador,
#    extrair href, descartar assets e âncoras, deduplicar -> 101 páginas.
# 2. Baixar cada uma com ~0,4 s de pausa entre requisições, gravar em
#    iczn/.cache/<slug>.html onde <slug> = caminho do site com '/' trocado por '__'.
# 3. Converter para texto em iczn/.cache/text/<slug>.txt removendo script/style/head,
#    trocando <br>/</p>/</div>/</li>/</h*>/</tr> por \n e apagando as demais tags.
# 4. Reconstruir a URL a partir do slug: trocar '__' por '/' e envolver em
#    https://code.iczn.org/.../
```

O site devolve **HTTP 403** a clientes não-navegador — é preciso
`curl -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"`.
Não existe sitemap, robots.txt, API, JSON, XML nem repositório GitHub por trás do
site. `iczn/scripts/code_index.json` traz o sha256 de cada página como estava na
raspagem original, então dá para verificar se a regeneração trouxe o mesmo conteúdo.
