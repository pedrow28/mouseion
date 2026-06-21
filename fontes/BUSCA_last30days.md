# Busca de notícias e artigos — `last30days`

Pesquisador das editorias **IA** e **Ideias de Negócio** (e da *Coletânea* do Saúde, se
quiser). Varre os últimos 30 dias em Reddit, X, YouTube, TikTok, Hacker News, Polymarket,
GitHub e web, e devolve material bruto com as fontes. **Não é usada no Pulso oficial do
Saúde** — lá vale só DOU/IOF (regra de ouro).

> Requisito: **Python 3.12+**. (O sandbox do Cowork tem 3.10 e não roda a skill; na sua
> máquina, com 3.12+, roda normalmente.)

## 1. Instalar (uma vez)

Cowork / Claude Code — recomendado, atualiza sozinho pelo marketplace:

```
/plugin marketplace add mvanhorn/last30days-skill
/plugin install last30days
```

Alternativa (qualquer host de skills):

```
npx skills add mvanhorn/last30days-skill -g
```

## 2. Rodar o setup wizard (liga tudo)

```
python3 <skill>/scripts/last30days.py setup
```

- Liga na hora, **sem chave**: Reddit, Hacker News, Polymarket, GitHub, web.
- Guia o **X** (extrai os cookies do navegador logado) e o **ScrapeCreators** (opt-in).

## 3. Chaves (`.env`)

A skill procura, nesta ordem:

1. `.claude/last30days.env` — **neste projeto** (tem precedência).
2. `~/.config/last30days/.env` — global do usuário.

Copie o template e preencha só o que for usar:

```
cp fontes/last30days.env.example .claude/last30days.env
chmod 600 .claude/last30days.env
```

| Quero buscar em… | Preciso de | Custo |
|---|---|---|
| Reddit, HN, Polymarket, GitHub, web | nada | grátis |
| **X / Twitter** | `AUTH_TOKEN`+`CT0` (cookies do browser) **ou** `XAI_API_KEY` | grátis / pago |
| TikTok, Instagram, comentários do YouTube | `SCRAPECREATORS_API_KEY` | 100 grátis, depois ~US$10/5k |

### X no Chrome, Brave ou Edge

A extração automática silenciosa é de Firefox/Safari. No Chromium, faça um dos dois:

- **Automático:** adicione `FROM_BROWSER=chrome` (ou `brave`/`edge`) no `.env` e rode o wizard — ele tenta ler os cookies (o sistema pode pedir permissão).
- **Manual (garantido):** em `x.com` logado → **F12** → aba **Application** → **Cookies** → `https://x.com` → copie os valores de `auth_token` e `ct0` para o `.env`:

  ```
  AUTH_TOKEN=<valor do auth_token>
  CT0=<valor do ct0>
  ```

Os cookies do X expiram de tempos em tempos; quando o X parar de retornar, é só recopiar.

## 4. Testar

```
python3 <skill>/scripts/last30days.py "Claude Code skills" --quick --agent --emit=compact
```

Com tudo keyless, já volta Reddit + HN + web. Conforme você adiciona X/ScrapeCreators, mais
fontes entram.

## 5. Como entra na revista

`editorias/editorias.yaml` já aponta a `last30days` como fonte de **IA** e **Ideias**
(modo `--agent`, não interativo). No ciclo diário: o Pesquisador roda a skill, o engine salva
o raw em `LAST30DAYS_MEMORY_DIR`, o `fontes/comum.py` deduplica pelo ledger da editoria, e o
Redator escreve a matéria **com os links** a partir do material — nunca colando a síntese da
própria skill (preservamos a voz da revista e a regra do link).
