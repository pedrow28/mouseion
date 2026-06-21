# editorias/ — as editorias como dados

> "Editorias são dados, não código" (CLAUDE.md, regra 5). Esta pasta é a configuração que
> separa **o que** a revista publica do **motor** que a monta. Mudou editoria? Edita aqui —
> nunca o motor.

## Arquivos

- `editorias.yaml` — a config canônica das 8 editorias (id, motor, seções, fontes, cadência,
  regra, acento, ponteiros de estado). O **motor lê este arquivo**: o diagramador para saber a
  ordem e os slots; o de currículo para achar syllabus/cursor; o de dedup para achar o ledger.
- `redatores/` — o prompt do Redator (LLM) por editoria. Cada `editorias.yaml › redator` aponta
  para um arquivo aqui. São especializações do papel genérico `agentes/redator.md`.

## Os cinco motores

| motor | editorias | o que o Pesquisador traz | o que o Redator faz |
|---|---|---|---|
| `noticia`   | (parte de Saúde/IA) | texto recuperado + link | resume o recuperado, com link |
| `curriculo` | Gestão, Imersão, Mente, Família | nada (cursor decide a aula) | escreve a aula do syllabus no molde |
| `hibrido`   | Saúde, IA | recuperado + currículo | as duas coisas, por seção |
| `sintese`   | Ideias de Negócio | coleta de IA/Saúde + web | 1–3 ângulos acionáveis (lente Thauma) |
| `curadoria` | Fitness | 1 dose da web | dose curta, sem virar curso |

## Para aprofundar & Mais para ler

**Toda** editoria fecha com **"Para aprofundar"**: 2–3 artigos de desenvolvimento (com link),
coletados por `coletar_aprofundamento` usando a query de `editorias/aprofundamento.yaml`. É o
peso de aprofundamento da revista — vale mais que a notícia efêmera.

Além disso, as editorias de notícia (Saúde, IA, Ideias) trazem **"Mais para ler"**: os
artigos/posts que o coletor de notícia trouxe e que **não** viraram matéria redigida, como
links curados. Ambas as listas usam o estilo `.leituras` no template.

## Cadência

As cadências em `editorias.yaml` são **propostas** (decisão em aberto #2). O motor respeita o
campo `cadencia` (lista de dias da semana) para decidir o que entra na edição de cada dia.

## Como o motor usa isto (resumo)

1. Lê `editorias.yaml`, filtra as editorias cuja `cadencia` inclui o dia de hoje.
2. Para `curriculo`: lê o `cursor`, pega a aula do `syllabus`, manda ao Redator; depois avança o cursor.
3. Para `noticia`/`hibrido`/`sintese`/`curadoria`: roda as `fontes`, deduplica pelo `ledger`,
   manda o material ao Redator.
4. Encaixa as matérias nos slots de `template/base.html` na `ordem` definida.
5. QA estrutural; se passar, publica.
