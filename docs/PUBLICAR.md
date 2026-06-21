# Publicar e automatizar a revista

Guia para **(1)** subir no GitHub, **(2)** ligar o GitHub Pages e **(3)** automatizar a edição
diária. Os passos com `<...>` você troca pelos seus valores.

> ⚠️ **Antes de tudo:** confirme que o `.env` (com o `APIFY_TOKEN`) **não** vai para o GitHub.
> Ele já está no `.gitignore` — segredo nunca entra no repositório. Na automação, o token vai
> como **variável de ambiente** (Parte 3), não no código.

---

## Parte 1 — Subir no GitHub (uma vez)

1. Crie um repositório **vazio** em https://github.com/new. Pode ser **público** (o Pages é
   grátis em repositório público). Use o nome da revista. **Não** marque "Add a README".
2. No terminal, dentro da pasta `revista-diaria`:
   ```bash
   git init
   git add .
   git commit -m "Revista — primeira edição"
   git branch -M main
   git remote add origin https://github.com/<SEU_USUARIO>/<REPO>.git
   git push -u origin main
   ```
3. No GitHub, confirme que o arquivo `.env` **não** apareceu na lista. Se aparecer, **pare** e
   me chame (não dê push de segredo).

## Parte 2 — Ligar o GitHub Pages (uma vez)

1. No repositório: **Settings → Pages**.
2. Em **Build and deployment → Source**, escolha **Deploy from a branch**.
3. Branch **main**, pasta **/ (root)** → **Save**.
4. Aguarde ~1 minuto. A revista fica no ar em:
   `https://<SEU_USUARIO>.github.io/<REPO>/`
   - A capa é o `index.html`; cada edição em `/edicoes/AAAA-MM-DD.html`.

Pronto — a edição de hoje já está pública. Falta a de **amanhã** nascer sozinha.

## Parte 3 — A edição diária automática

Todo dia o ciclo é: **motor monta o esqueleto → coleta (Apify) → o Redator (LLM) escreve →
renderiza a edição → commit/push** (o Pages publica). Esse roteiro está em
`agentes/RUNBOOK_DIARIO.md`. Falta só escolher **quem dispara** o ciclo. Três caminhos:

### Opção A — Routine do Claude Code (recomendada)
Roda na nuvem da Anthropic, usa a sua assinatura (sem API key extra) e **o laptop pode estar
fechado**.
1. No Claude Code, crie uma **Routine** agendada (ex.: todo dia 6h, fuso `America/Sao_Paulo`).
2. Aponte o **repositório** para o seu repo da revista.
3. No **Cloud Environment** da Routine, adicione:
   - `APIFY_TOKEN` = seu token do Apify
   - um **GitHub PAT** (token com permissão de escrita no repo), para o `git push`.
4. Libere `api.apify.com` na rede (allowlist / "Trusted network" do Cloud Environment).
5. **Prompt da Routine:** `Execute o runbook diário em agentes/RUNBOOK_DIARIO.md.`
6. Salve. Amanhã, no horário, ela monta, escreve, publica e commita sozinha.

### Opção B — GitHub Actions (tudo no GitHub)
Cron no próprio GitHub rodando `claude -p`. Precisa de uma **API key da Anthropic** (custo à
parte da assinatura). Secrets do repo: `ANTHROPIC_API_KEY`, `APIFY_TOKEN`. Bom se você prefere
não depender do app. *(Posso te gerar o arquivo de workflow quando quiser.)*

### Opção C — Agendamento local (sua máquina)
O **Task Scheduler** (Windows) dispara o Claude Code local todo dia + `git push`. Simples, mas
exige a máquina ligada na hora do disparo.

## Parte 4 — Conferir amanhã
- A Routine/Action **rodou**? (veja o histórico de execução)
- Surgiu um **commit novo** com `edicoes/AAAA-MM-DD.html`?
- A edição abre em `https://<SEU_USUARIO>.github.io/<REPO>/edicoes/<data>.html`?

Se falhar, o **QA** (lint) barra a publicação e registra o motivo — me mostre o log que a gente
ajusta.
