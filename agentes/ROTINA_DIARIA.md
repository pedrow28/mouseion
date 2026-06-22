# Rotina diária — a revista no piloto automático

> Como deixar a Mouseion saindo **sozinha, todo dia, publicada direto na `main`**
> (e, por consequência, no GitHub Pages). Usa o recurso **Routines** do Claude Code on
> the web. Esta config é versionada aqui para não se perder e para ser reusada.

## O que é

Uma **Rotina** é uma sessão do Claude Code que roda na nuvem da Anthropic num horário fixo,
sem ninguém abrir o navegador. Ela clona o repo, executa o `agentes/RUNBOOK_DIARIO.md`,
monta a edição do dia e **dá commit + push direto na `main`**. O Pages reconstrói e a edição
aparece no site.

Docs: <https://code.claude.com/docs/en/routines>

## Ligar a rotina (uma vez, ~2 min) — em claude.ai/code/routines

1. Abra <https://claude.ai/code/routines> → **New routine**.
2. **Nome:** `Mouseion — edição diária`.
3. **Prompt:** cole o bloco da seção [Prompt da rotina](#prompt-da-rotina) abaixo. Escolha o
   modelo (recomendado: o mais capaz disponível).
4. **Repositories:** adicione `pedrow28/mouseion`.
5. **Environment:** selecione o ambiente que tem o que a coleta precisa (ver
   [Ambiente](#ambiente-rede-e-segredos)). Network access **Trusted** já basta para o conector
   Apify (o tráfego de conector passa pela Anthropic) e para o GitHub.
6. **Connectors:** mantenha **Apify** ligado (é como a coleta de notícia funciona). Remova
   conectores que a revista não usa.
7. **Trigger → Schedule:** escolha **Daily** e a hora (no seu fuso; ex.: 06:00). A conversão de
   fuso é automática. (Intervalo mínimo: 1h.)
8. **Permissions:** ligue **Allow unrestricted branch pushes** para `pedrow28/mouseion`. **Esse
   passo é o que permite publicar direto na `main`** — sem ele, a rotina só empurra para
   branches `claude/…` e nada chega ao Pages.
9. **Create.** Use **Run now** na página da rotina para testar a primeira execução agora.

> Pausar/retomar: toggle em **Repeats**. Editar prompt/horário: ícone de lápis.
> Do CLI local (não de dentro de uma sessão web) dá para usar `/schedule`, `/schedule list`,
> `/schedule update`.

## Prompt da rotina

Cole exatamente isto no campo de prompt da rotina:

```
Você é a redação automática da revista Mouseion. Use a data atual no fuso America/Sao_Paulo
como HOJE (AAAA-MM-DD).

Execute integralmente o runbook diário em agentes/RUNBOOK_DIARIO.md, que orquestra os papéis
em agentes/ e o motor em motor/. Em resumo: leia o estado em estado/ e editorias/editorias.yaml;
para cada editoria cuja cadência inclui hoje, gere a matéria (currículo = a aula do cursor,
seguindo docs/MOLDE_AULA.md e editorias/redatores/curriculo.md, sem escolher a aula — é a do
cursor; notícia = só o que for efetivamente recuperado via o conector Apify, sempre com link).
Colete também 2–3 artigos de 'Para aprofundar' por editoria. Avance os cursores e registre nos
ledgers o que saiu. Monte a edição em edicoes/AAAA-MM-DD.html; adicione a edição no topo da
lista em index.html; rode o QA (motor/qa.py) e só publique se passar.

Publicação: trabalhe e publique DIRETO NA BRANCH main. Ao final, com o QA aprovado:
  git add -A && git commit -m "Edição AAAA-MM-DD" && git push origin HEAD:main
Não abra pull request. Se o QA reprovar, NÃO publique: registre o motivo e pare.

Regras de ouro inegociáveis (CLAUDE.md): no editorial Saúde a acurácia é absoluta — só resuma
texto efetivamente recuperado, sempre com o link da fonte, nunca invente nem extrapole; se a
fonte não foi recuperada, não existe. Não repita pauta (dedup pelo ledger) nem aula (cursor).
O peso editorial está nos artigos de aprofundamento. Tudo em PT-BR. Não toque no visual
(template/). Se algum cursor estiver atrasado em relação ao que já foi publicado em edicoes/,
reconcilie antes de gerar para não repetir.
```

## Ambiente, rede e segredos

- **Coleta de notícia:** feita pelo **conector Apify** (MCP). Em **Trusted** o tráfego do
  conector já passa — não precisa liberar domínio. Garanta que o conector Apify está conectado
  na sua conta (claude.ai → Settings → Connectors) e incluído na rotina.
- **`fontes/apify.py` (REST, opcional):** se um dia quiser usar o coletor REST em vez do
  conector, defina `APIFY_TOKEN` como variável de ambiente do environment (formato `.env`,
  sem aspas). Hoje a revista funciona bem só com o conector.
- **Dependências do motor:** o motor usa `pyyaml`. Se o ambiente reclamar, adicione
  `pip install pyyaml` ao **Setup script** do environment (o resultado fica em cache).
- **GitHub:** as ferramentas de GitHub e o push já funcionam pela identidade conectada; o
  **Allow unrestricted branch pushes** é o que destrava a `main`.

## Por que publicar na main funciona com o Pages

O GitHub Pages do repo serve a partir da `main`. Com a rotina empurrando direto para a `main`,
cada edição entra no ar sozinha. Sem o passo 8 (unrestricted branch pushes), a rotina pararia
numa branch `claude/…` e o site não mudaria.
