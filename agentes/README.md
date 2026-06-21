# Agentes

Os prompts dos papéis da redação. Cada arquivo é o "system prompt" de um papel.
Apenas os papéis com LLM têm prompt aqui; Pesquisador, Diagramador e QA são código
(ver `docs/ARQUITETURA.md`) e ficam em `fontes/`, `template/` e na rotina de build.

São **rascunhos v0** — refine conforme o piloto de Saúde roda. Mantenha as regras
inegociáveis do `CLAUDE.md` sempre presentes no topo de cada prompt.

| Arquivo | Papel | Tem LLM? |
|---|---|---|
| `pesquisador.md` | Especificação da coleta (implementada em código) | ❌ (spec) |
| `editor-chefe.md` | Triagem do material bruto + coerência da edição | ✅ |
| `redator.md` | Redação de cada matéria | ✅ |
| `diagramador.md` | Especificação da renderização (template fixo) | ❌ (spec) |
| `qa.md` | Especificação do lint estrutural | ❌ (spec) |
