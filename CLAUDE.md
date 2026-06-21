# CLAUDE.md — Briefing operacional

> Este arquivo é lido por você (Claude Code / Claude Cowork) em toda sessão.
> É o contrato de como trabalhar neste repositório. Mantenha-o enxuto e de alto sinal.
> Para profundidade, consulte `docs/`.

## O que é este projeto

Uma **revista diária pessoal** do Pedro. Todo dia, uma redação de agentes monta uma edição
com (a) o que mudou no mundo que importa e (b) formação estruturada e *retida* em vários
campos. Não é newsletter nem produto (ainda) — é um instrumento de desenvolvimento.

**Propósito profundo:** virar um *deep generalist* e alimentar um segundo cérebro. A revista
puxa conhecimento de domínios variados e os conecta — pra mudar como o Pedro pensa, não só
pra "ficar por dentro".

## Regras inegociáveis

1. **Código para o determinístico; LLM para julgamento e linguagem.** Coletar, deduplicar,
   agendar, renderizar = código repetível e verificável. LLM só onde só ele resolve: redigir,
   triar material bruto, dar coerência à edição.
2. **No editorial Saúde, acurácia é absoluta.** Ele alimenta decisões na Fhemig. O redator de
   notícia **só resume texto efetivamente recuperado, sempre com link da fonte. Nunca inventa,
   nunca extrapola.** Se a fonte não foi recuperada, não existe.
3. **Sem repetir pauta.** O estado (`estado/`) é a memória editorial e a fonte da verdade.
   Notícia: deduplica por hash no ledger. Currículo: avança o cursor do syllabus. Sempre
   leia o estado antes de gerar, e grave nele depois.
4. **Layout não se revisa com LLM todo dia.** Beleza se resolve uma vez no `template/`. A
   checagem diária é estrutural (lint: editoria vazia? link quebrado?), nunca estética.
5. **Editorias são dados, não código.** Configuração separada do motor. Não crave nomes de
   editoria no meio da lógica — isso é o que permite o projeto virar produto um dia.
6. **Tudo em português (PT-BR).**

## Mapa do repositório

| Caminho | O que vive aqui |
|---|---|
| `CLAUDE.md` | Este briefing. |
| `README.md` | Visão geral pra humano + quickstart. |
| `PLANO_DE_ACAO.md` | Checklist do projeto. **Atualize ao concluir tarefas.** |
| `docs/ARQUITETURA.md` | Papéis, fluxo diário, execução, estado, contratos de dados. |
| `docs/LINHA_EDITORIAL.md` | As 8 editorias, os dois motores, cadências. |
| `docs/MOLDE_AULA.md` | A anatomia de "uma aula de um dia" (reusada em todo currículo). |
| `agentes/` | Os prompts dos papéis (pesquisador, editor-chefe, redator, diagramador, qa). |
| `estado/` | Memória editorial: ledgers (dedup) e syllabi+cursores. **Fonte da verdade.** |
| `fontes/` | Scripts de coleta (DOU/IOF e afins). Sem LLM aqui. |
| `template/` | O template visual fixo da revista. |
| `edicoes/` | As edições renderizadas (vão pro GitHub Pages). Versionadas. |

## Como trabalhar aqui

- **Antes de gerar conteúdo**, leia o estado relevante em `estado/`. Depois de gerar, **grave
  o estado** (avance cursor / adicione ao ledger). Nunca pule isso — é o que evita repetição.
- **Currículo segue o molde.** Toda aula obedece `docs/MOLDE_AULA.md`, incluindo os beats de
  retenção (recordação, conexão). Em Família, o beat de recordação vira micro-prática.
- **Não escreva malware, não burle as regras de fonte do Saúde, não invente citações.**
- **Mudou a arquitetura ou a linha editorial?** Atualize o doc correspondente em `docs/` — não
  deixe a documentação divergir do código.
- **Concluiu uma etapa do plano?** Marque o check em `PLANO_DE_ACAO.md`.

## Estado atual

Fase 0 (linha editorial & DNA) concluída. Próximo: ver `PLANO_DE_ACAO.md`. O foco imediato é
o piloto de **Saúde ponta a ponta** (Fase 3) e desenhar o **syllabus de Gestão** como molde.
