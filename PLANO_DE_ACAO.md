# Plano de Ação (tracker)

> Marque o check ao concluir. Mantenha sincronizado com o estado real do projeto.

## Onde paramos (log de sessão)

### 2026-06-21 — "Para aprofundar" em todos os campos
- **Nova linha editorial:** privilegiar **aprofundamento** (artigos técnicos/de desenvolvimento) sobre notícia. Toda editoria fecha com **"Para aprofundar"** — 2–3 artigos com link.
- Coletados ao vivo via Apify (`rag-web-browser`) para as 9 editorias e já na edição (até PDF da USP em Teoria dos Jogos e artigo da USP em modelos de negócio com IA).
- **Estrutura:** `editorias/aprofundamento.yaml` (query por editoria) + `coletar_aprofundamento` em `fontes/apify.py`; registrado em `docs/LINHA_EDITORIAL.md`.

### 2026-06-21 — Editoria de Vendas + mais leituras
- **Nova editoria Marketing & Vendas** (currículo, foco vender serviço B2B consultivo): syllabus de **37 aulas** (`estado/vendas/`), entrada no `editorias.yaml` (ordem 4, após Gestão), cor `.e-vendas`, slot no `base.html` e Aula 1 na edição. A revista agora tem **9 editorias**.
- **"Mais para ler"** em IA, Saúde e Ideias: lista de links curados (artigos/posts coletados que não viraram matéria), estilo `.leituras`. Atende o pedido de mais materiais para ler.

### 2026-06-21 — Busca via Apify
- **Decidido:** o buscador da revista (IA, Ideias, Coletânea do Saúde) é o **Apify**, não a `last30days`. Motivo: já configurado, roda na nuvem (funciona na Routine só com `APIFY_TOKEN`, sem cookies/navegador) e entrega dado bruto (encaixa na arquitetura).
- **Testado ao vivo:** o ator `apidojo/tweet-scraper` buscou 12 tweets de "AI agents" em 4 s, < 1 centavo, com autor/data/engajamento/link.
- **Feito:** `fontes/apify.py` com os **4 coletores calibrados e testados ao vivo** (X, Reddit, Google News PT-BR, Web); lê o `.env`, despacha pela config e deduplica via `coletar_editoria`. `editorias.yaml` aponta os atores; `APIFY_TOKEN` colado no `.env`.
- **Atores:** X `apidojo/tweet-scraper` · Reddit `automation-lab/reddit-scraper` · News `automation-lab/google-news-scraper` · Web `apify/rag-web-browser`.
- **Edição real montada ponta a ponta:** `edicoes/2026-06-20.html` agora traz IA, Ideias e a Coletânea do Saúde com **notícia real** (coletada via Apify, triada e redigida com links, lente Thauma/Fhemig) ao lado das aulas do currículo. Prova do pipeline completo coleta→triagem→redação→render.
- **Falta:** ligar `coletar_editoria` no **pipeline diário** (coleta → Editor-chefe tria → Redator escreve → motor renderiza); **decidir a execução** (Routine na nuvem só com `APIFY_TOKEN`, ou agendamento local) e agendar. Obs.: News vem com URL do Google News RSS (redireciona pro artigo); trocável por ator com `decodeUrls` se quiser link limpo.

### 2026-06-20
**Feito:**
- **Currículo 100% desenhado** (syllabus + amostra cada): Gestão (64), Imersão/Teoria dos Jogos (34), Família (33), Mente — Psicologia (24) / Filosofia (23) / Teologia (22) + rotação.
- **Bloco de notícia estruturado**: Saúde, IA, Ideias e Fitness com seções, fontes, prompt do Redator e amostra na vitrine.
- **Editorias como dados**: `editorias/editorias.yaml` (config das 8) + `editorias/redatores/*.md` (prompts). Cadência proposta embutida.
- **Template + blog**: `template/` (base + css), home `index.html`, vitrine `edicoes/2026-06-20.html` com as **8 editorias** preenchidas (4 aulas + 3 gabaritos rotulados + 1 dose real).
- **Motor determinístico (código, sem API), testado**: `fontes/comum.py` (dedup/ledger), `motor/curriculo.py` (cursor + rotação), `motor/config.py` (cadência), `motor/diagramador.py` (render), `motor/qa.py` (lint), `motor/montar_edicao.py` (orquestra). Teste: monta a edição de sábado com as 6 editorias certas e o QA passa.
- **Stack de pesquisa decidida**: scrapers DOU/IOF p/ Saúde; `last30days` p/ IA e Ideias; sem Brave MCP.

**Falta só o que depende de fora (deixado para o final, como combinado):**
1. **API/chaves**: `SCRAPECREATORS_API_KEY` (núcleo da `last30days`). *(a perguntar quando chegarmos lá)*
2. **Configs de MCP**: confirmar a skill `last30days` instalada + ligar os scrapers (desacoplar resumo/email `~/.hermes`).
3. **GitHub Pages** (deploy from root) + **execução agendada** (Routine/Actions).
4. **Decisões**: nome da revista; confirmar a cadência proposta em `editorias.yaml`.

## Fase 0 — Linha editorial & DNA
- [x] Definir propósito (deep generalist + segundo cérebro)
- [x] Definir os dois motores
- [x] Definir lineup de editorias (8)
- [x] Definir papel do LLM no Editor-chefe (curadoria/coerência sim; layout não)
- [x] Definir camada de execução (Routine do Claude Code)
- [x] Desenhar o molde de aula (docs/MOLDE_AULA.md)
- [x] Estruturar o repositório
- [x] Fechar nome da revista — **Mouseion** (a casa das Musas)
- [ ] Fechar cadência por editoria (quais diárias, quais X/semana)

## Fase 1 — Arquitetura & decisões técnicas
- [ ] Validar no setup do Pedro se a Routine consegue escrever no repo (senão, fallback)
- [x] Confirmar a estrutura do repo e os contratos de dados (docs/ARQUITETURA.md §6) — usados pelo motor
- [x] Construir o template visual da revista (resolve layout de uma vez)
- [ ] Configurar GitHub Pages

## Fase 2 — Estado & syllabi
- [x] Implementar ledger de notícia (dedup) para Saúde — `fontes/comum.py`
- [x] Implementar modelo genérico syllabus + cursor — `motor/curriculo.py`
- [x] Desenhar o syllabus de Gestão completo (protótipo do molde) — 64 aulas
- [x] Mecanismo do slot rotativo (Imersão) — motor lê `tema_atual.json` (troca de tema ao fim: manual por ora)

## Fase 3 — Piloto: Saúde ponta a ponta
- [ ] Ligar os scripts DOU/IOF como Pesquisador (já colados em `fontes/`; falta desacoplar coleta de resumo/email)
- [x] Finalizar o prompt do Redator de Saúde — `editorias/redatores/saude.md`
- [ ] Finalizar o prompt do Editor-chefe (triagem + coerência)
- [x] Renderizar 1 edição no template (piloto: 2026-06-20, Gestão Aula 1)
- [ ] Publicar no Pages e ler
- [ ] Rodar 3 dias seguidos sem repetir pauta (teste do dedup)

## Fase 4 — Replicar
- Conteúdo fechado (syllabus/estrutura + amostra): [x] Gestão · [x] Marketing & Vendas · [x] Imersão (Teoria dos Jogos) · [x] Família · [x] Mente (3 fios) · [x] Saúde · [x] IA · [x] Ideias de Negócio · [x] Fitness
- [ ] Feature de síntese cross-editorial (retenção) — opcional

## Decisões em aberto
1. ✓ Nome: **Mouseion** (a casa das Musas). *(decidido 2026-06-21)*
2. Cadência por editoria. *(proposta pronta em `editorias/editorias.yaml` — confirmar)*
3. ✓ Fontes do Saúde — scrapers DOU/IOF (oficial) + busca web na Coletânea. *(decidido 2026-06-20)*
4. ✓ Fontes de IA / Ideias — **Apify** (atores X/Reddit/News) como Pesquisador; `last30days` descartada do pipeline. *(decidido 2026-06-21)*
5. ✓ Desenhar syllabi (Gestão, Teoria dos Jogos, Mente×3, Família) — **concluído** 2026-06-20.
6. ✓ Rotação do Mente — definida (`estado/mente/rotacao.json`). Pendente: cadência do Fitness.
7. ✓ Buscador: **Apify** (já configurado). Falta só pôr o `APIFY_TOKEN` no `.env`. *(decidido 2026-06-21)*
