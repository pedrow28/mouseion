# Runbook diário — a edição de hoje

> Roteiro que a automação (Routine / Actions / local) executa **todo dia**. Amarra os papéis de
> `agentes/` na ordem certa. Tudo determinístico é código; só a **redação** é LLM.

`HOJE = AAAA-MM-DD` (fuso `America/Sao_Paulo`).

## 1. Ler o estado
- `editorias/editorias.yaml` → as editorias cujo `cadencia` inclui o dia da semana de hoje.
- Para cada uma, os ponteiros em `estado/` (cursor de currículo / ledger de notícia).

## 2. Por editoria do dia

**Currículo (Gestão, Marketing & Vendas, Imersão, Mente, Família):**
- Pegue a aula do `cursor` (`motor/curriculo.py`). Em Mente, o fio do dia vem de `rotacao.json`.
- Escreva a aula seguindo `docs/MOLDE_AULA.md` (os 7 beats) e `editorias/redatores/curriculo.md`.
  **Não escolha a aula — é a do cursor.**
- Depois de publicar, **avance o cursor** (`motor/curriculo.py: avancar`).

**Notícia / síntese (Saúde, IA, Ideias):**
- Colete: `fontes/apify.py: coletar_editoria(<id>, <termos do dia>)` (já deduplica pelo ledger).
- Triagem (Editor-chefe) → redação (Redator) **com o link da fonte**, conforme o redator da
  editoria. **Saúde: só o recuperado, zero invenção.** O Pulso oficial usa os scrapers DOU/IOF.
- Registre no ledger o que saiu.

**Todas as editorias:**
- `fontes/apify.py: coletar_aprofundamento(<id>)` → 2–3 artigos para a seção **"Para aprofundar"**.

## 3. Montar e publicar
- O Diagramador (motor) encaixa tudo no template → `edicoes/AAAA-MM-DD.html`.
- Atualize `index.html` (adicione a edição no topo da lista).
- **QA** (`motor/qa.py`): editoria vazia? link quebrado? cursor avançou? Se reprovar, **não
  publica** — registra o motivo.
- **Publica direto na `main`** (é de lá que o GitHub Pages serve):
  `git add -A && git commit -m "Edição AAAA-MM-DD" && git push origin HEAD:main`. Sem PR.
- Roda sozinho todo dia pela **Rotina** (ver `agentes/ROTINA_DIARIA.md`).

## 4. Regras de ouro (inegociáveis)
- **Saúde:** só resume texto efetivamente recuperado, sempre com link. Nunca inventa.
- **Sem repetir** pauta (ledger) nem aula (cursor).
- **Aprofundamento > notícia:** o peso editorial está nos artigos de desenvolvimento.
- Tudo em **PT-BR**.
