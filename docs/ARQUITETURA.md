# Arquitetura

## 1. Princípio que organiza tudo

**Código para o determinístico; LLM para julgamento e linguagem.**
(Antes era "minimizar token". Com Claude Code na assinatura, o custo deixa de ser o ponto — o
ponto é *confiabilidade e reprodutibilidade*.) Coletar, deduplicar, agendar, renderizar e
checar = código repetível. LLM só onde só ele resolve: redigir, triar material bruto, dar
coerência à edição.

## 2. Papéis vs. implementação

Os "agentes" são papéis. Nem todo papel é um LLM.

| Papel | O que faz | Implementação | LLM? |
|---|---|---|---|
| **Pesquisador** | Traz matéria-prima (DOU/IOF, artigos, papers) | Scripts Python, MCP/Apify, RSS, APIs | ❌ |
| **Editor-chefe — planejamento** | Define a pauta lendo o estado | Lógica determinística | ❌ |
| **Editor-chefe — curadoria** | Tria o material bruto (o que entra, o que é ruído); coerência da edição | LLM, escopo cravado | ✅ |
| **Redator** | Escreve cada matéria | LLM, 1× por matéria | ✅ |
| **Diagramador** | Monta a edição no template | Template fixo | ❌ |
| **QA** | Lint estrutural (editoria vazia? link quebrado?) | Checagem determinística | ❌ |

Os prompts dos papéis com LLM ficam em `agentes/`.

## 3. Fluxo diário

```
Routine (ex.: 6h, fuso America/Sao_Paulo)
  └─ para cada editoria habilitada na config:
       1. Editor-chefe (planejamento) lê o estado → define a pauta do dia
       2. Pesquisador coleta matéria-prima (só editorias com fonte externa)
       3. Editor-chefe (curadoria) tria o material bruto coletado
       4. Redator escreve cada matéria (LLM), seguindo o molde quando for currículo
       5. Editor-chefe grava no estado o que saiu (dedup / avança cursor)
  └─ Diagramador renderiza a edição com o template fixo
  └─ QA roda o lint estrutural
  └─ Commit no repo → publica no GitHub Pages
```

## 4. Camada de execução (Claude Code)

Três caminhos reais (verificado, jun/2026):

- **Routine (recomendado).** Roda na infraestrutura da Anthropic, sem servidor, usa a
  assinatura (Pro+). Agenda diária. **Validar na Fase 1** se a Routine consegue escrever no
  repo no setup do Pedro.
- **GitHub Actions headless (`claude -p`).** Cron + repo + Pages tudo no GitHub, version-
  controlado e portável. Normalmente pede API key (custo à parte da assinatura). Bom fallback.
- **Desktop scheduled task (Mac/Windows).** Persistente, usa a assinatura, roda local e dá
  push fácil pro GitHub. Fallback se a Routine não escrever no repo.

### O que a Routine (nuvem) consegue — e o que não (verificado jun/2026)

A Routine roda em ambiente **efêmero na nuvem da Anthropic**: clona o repo, tem Bash + `gh`, e
**faz `git commit`/`push`** (publica no Pages) com um PAT no *Cloud Environment*. Mas **não vê
nada local** — nem `.env`, nem o navegador, nem cookies. Consequências para esta revista:

- **Currículo** (Gestão, Imersão, Mente, Família): roda sem atrito — é só LLM.
- **IA / Ideias (Apify)**: X, Reddit e Google News vêm de atores do Apify, que rodam **na nuvem
  do Apify** — então **funcionam na Routine** com só o `APIFY_TOKEN` (sem navegador, sem cookies,
  sem Python local). Único cuidado: liberar `api.apify.com` na rede "lista branca" do Cloud
  Environment. Coletor em `fontes/apify.py`. (A `last30days` foi avaliada e descartada do
  pipeline — fica como ferramenta interativa opcional.)
- **Saúde (DOU/IOF)**: scrapers com Playwright + sites `.gov.br` → exigem allowlist de rede e
  navegador headless; rodam com menos atrito num **agendamento local**.

**Regra de bolso:** quer "laptop pode fechar" → Routine na nuvem, com `XAI_API_KEY` e allowlist.
Quer os cookies grátis do navegador e os scrapers como estão → **Desktop scheduled task** na
máquina do Pedro (custo: máquina ligada na hora).

Evitar o `/loop` da CLI para isto: é session-scoped e expira — serve pra tarefas curtas, não
pra uma revista que roda por meses.

## 5. Estado (a memória editorial — fonte da verdade)

### 5.1 Ledger de notícia (dedup)
`estado/<editoria>/ledger.jsonl` — uma linha por item já publicado:
```json
{"hash":"sha1-do-conteudo","url":"https://...","titulo":"...","data_saida":"2026-06-20"}
```
O Pesquisador descarta qualquer item cujo hash já esteja no ledger.

### 5.2 Syllabus + cursor (currículo)
O curso existe **antes** da automação — é entregável de design, não invenção diária.
```
estado/<editoria>/syllabus.md   → ementa completa (N aulas, em ordem)
estado/<editoria>/cursor.json   → {"proxima_aula": 14, "total": 65}
```

### 5.3 Slot rotativo (editoria Imersão)
```
estado/imersao/tema_atual.json  → {"tema":"Teoria dos Jogos","syllabus":"...","cursor":5,"total":40}
estado/imersao/arquivo/         → trilhas concluídas (arquivadas)
```
Cursor chegou ao fim → arquiva a trilha, troca o tema (config), começa a próxima.

## 6. Contratos de dados entre etapas

Para as etapas conversarem sem ambiguidade, padronizar o objeto que passa de uma para a outra.
**A definir na Fase 1** — esboço inicial:

```json
// material bruto (Pesquisador → Editor-chefe/curadoria)
{"editoria":"saude","tipo":"noticia","url":"...","titulo":"...","texto_recuperado":"...","fonte":"DOU","data":"2026-06-20"}

// matéria pronta (Redator → Diagramador)
{"editoria":"saude","secao":"pulso_oficial","titulo":"...","corpo_md":"...","fontes":["url1"],"data":"2026-06-20"}
```

Regra do Saúde reforçada no contrato: `texto_recuperado` é obrigatório e o Redator não pode
produzir afirmação que não se sustente nele.

## 7. Convenções

- Idioma: PT-BR.
- Agentes em Markdown, versionados.
- Estado é sempre lido antes e gravado depois — nunca pulado.
- Documentação acompanha o código: mudou arquitetura/linha editorial, atualiza o doc.

## 8. Implementação (o que já é código)

A espinha determinística existe e roda **sem LLM e sem chaves**. As editorias são lidas de
`editorias/editorias.yaml` (regra 5: editoria é dado).

| Papel | Implementação | Arquivo |
|---|---|---|
| Config das editorias | dados (YAML) | `editorias/editorias.yaml` + `editorias/redatores/*.md` |
| Pesquisador — dedup | hash + ledger | `fontes/comum.py` |
| Coletores Saúde | scrapers (Playwright/API) | `fontes/dou_complete_scraper.py`, `fontes/iof_mg_scraper.py` |
| Coletor IA/Ideias/Coletânea | atores do Apify via REST (`APIFY_TOKEN`) | `fontes/apify.py` |
| Editor-chefe — planejamento | editorias do dia por cadência | `motor/config.py` |
| Currículo | aula do dia + avança cursor; rotação Mente | `motor/curriculo.py` |
| Diagramador | template → edição, sumário dinâmico | `motor/diagramador.py` |
| QA | lint estrutural | `motor/qa.py` |
| Orquestrador | monta a edição do dia | `motor/montar_edicao.py` |

Teste do pipeline (sem LLM): `python3 motor/montar_edicao.py 2026-06-20` monta a edição do dia
só com o determinístico — filtra editorias pela cadência, puxa a aula de cada cursor, encaixa no
template e roda o QA.

**O que ainda depende de fora:** a redação (LLM em runtime, via Routine) preenche os
beats/resumos; a coleta web (`last30days` + chave) alimenta IA/Ideias; o agendamento
(Routine/Actions) dispara o ciclo; o GitHub Pages publica.
