# Mouseion — a casa das Musas

Uma redação de agentes de IA que monta, todos os dias, uma revista pessoal — metade *notícia*
(o que mudou no mundo que importa), metade *formação* (conhecimento estruturado e retido em
vários campos). O objetivo não é informar: é desenvolver. Virar um *deep generalist* e
alimentar um segundo cérebro.

## Como funciona, em uma imagem

```
Routine diária (Claude Code)
   │
   ├─ lê o estado (o que já saiu / qual a próxima aula)
   ├─ coleta matéria-prima (scripts, MCP, RSS, APIs)   ← sem LLM
   ├─ tria + redige cada matéria                        ← LLM
   ├─ grava o estado (dedup / avança cursor)
   ├─ renderiza no template fixo                        ← sem LLM
   └─ commit no repo → publica no GitHub Pages
```

A divisão central: **código faz o determinístico, LLM faz julgamento e linguagem.** Ver
`CLAUDE.md` para as regras inegociáveis.

## As 8 editorias

Saúde · Inteligência Artificial · Gestão · Imersão (slot rotativo) · Mente · Fitness ·
Ideias de Negócio · Família. Detalhe de cada uma em `docs/LINHA_EDITORIAL.md`.

## Estrutura

- `CLAUDE.md` — briefing operacional (lido pelo Claude em toda sessão).
- `docs/` — arquitetura, linha editorial, molde de aula.
- `agentes/` — os prompts dos papéis da redação.
- `estado/` — a memória editorial (dedup + syllabi). Fonte da verdade.
- `fontes/` — scripts de coleta.
- `template/` — o visual fixo da revista.
- `edicoes/` — as edições publicadas.
- `PLANO_DE_ACAO.md` — o checklist do projeto.

## Começando

1. `git init` neste diretório e suba para um repositório no GitHub.
2. Abra o diretório no **Claude Code** (ou **Claude Cowork**). O `CLAUDE.md` é carregado
   automaticamente.
3. Siga o `PLANO_DE_ACAO.md`. O primeiro marco é o piloto de **Saúde ponta a ponta**.
4. Execução agendada: configurar uma **Routine** diária do Claude Code (usa a assinatura,
   sem servidor). Fallback: GitHub Actions headless ou Desktop scheduled task. Decisão
   detalhada em `docs/ARQUITETURA.md`.

## Status

Concepção (Fase 0) concluída. Em construção.
