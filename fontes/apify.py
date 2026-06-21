"""Coletor Apify (determinístico) — Pesquisador das editorias de notícia/síntese.

Roda atores do Apify Store via REST (`run-sync-get-dataset-items`) usando `APIFY_TOKEN`
e normaliza cada item no contrato de material bruto (docs/ARQUITETURA.md §6):
{editoria, tipo, fonte, url, titulo, texto_recuperado, data, _meta}.

Sem LLM. A triagem (o que presta vs. ruído) é do Editor-chefe; a redação, do Redator.
O X funciona aqui SEM navegador/cookies — o ator roda na nuvem do Apify; basta o token.
Por isso esta é a fonte ideal também para a Routine na nuvem.

Config: defina `APIFY_TOKEN` no ambiente (ou no `.env` do projeto). Token em apify.com → Settings → API.
Uso rápido:  python3 fontes/apify.py "AI agents"
"""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

APIFY_BASE = "https://api.apify.com/v2"

# Atores escolhidos (jun/2026). Trocar aqui é trocar a fonte — sem mexer no resto.
ATOR_X = "apidojo/tweet-scraper"            # X/Twitter · US$0,40/1k tweets · 99,9%
ATOR_REDDIT = "automation-lab/reddit-scraper"   # Reddit · ~US$0,001/post · sem API key
ATOR_NEWS = "automation-lab/google-news-scraper"  # Google News · ~US$0,002/artigo
ATOR_WEB = "apify/rag-web-browser"          # Google + scrape → Markdown (oficial Apify)


RAIZ = Path(__file__).resolve().parents[1]


def _carregar_env() -> None:
    """Popula os.environ a partir do .env do projeto (só chaves ainda não definidas)."""
    env = RAIZ / ".env"
    if not env.exists():
        return
    for linha in env.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        k, _, v = linha.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _token() -> str:
    _carregar_env()
    t = os.environ.get("APIFY_TOKEN", "").strip()
    if not t:
        raise RuntimeError("APIFY_TOKEN ausente. Defina no ambiente ou no .env do projeto.")
    return t


def rodar_ator(ator: str, entrada: dict, fields: list[str] | None = None,
               max_charge_usd: float = 0.25, timeout: int = 120) -> list[dict]:
    """Roda um ator de forma síncrona e devolve os itens do dataset.

    `max_charge_usd` é a rede de segurança de custo (cap pay-per-event).
    """
    params = {"token": _token(), "maxTotalChargeUsd": max_charge_usd}
    if fields:
        params["fields"] = ",".join(fields)
    url = f"{APIFY_BASE}/acts/{ator.replace('/', '~')}/run-sync-get-dataset-items?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url, data=json.dumps(entrada).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _g(item: dict, *paths, default=""):
    """Primeiro caminho (dot-notation) presente e não-vazio."""
    for p in paths:
        cur, ok = item, True
        for k in p.split("."):
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                ok = False
                break
        if ok and cur not in (None, ""):
            return cur
    return default


def _iso(v) -> str:
    if not v:
        return datetime.now(timezone.utc).date().isoformat()
    for fmt in ("%a %b %d %H:%M:%S %z %Y", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            return datetime.strptime(str(v), fmt).date().isoformat()
        except Exception:
            pass
    return str(v)[:10]


# ─────────────────────────────────────────────────────────────────────────────
# Coletores por fonte. Cada um normaliza para o contrato de material bruto.
# O mapeamento do X está validado (jun/2026). Reddit/News/Web usam os campos
# prováveis do ator — confira no primeiro teste de cada e ajuste o mapa se preciso.
# ─────────────────────────────────────────────────────────────────────────────

def coletar_x(query: str, editoria: str, max_itens: int = 25, lang: str | None = None) -> list[dict]:
    entrada = {"searchTerms": [query], "maxItems": max_itens, "sort": "Latest"}
    if lang:
        entrada["tweetLanguage"] = lang
    fields = ["url", "text", "fullText", "createdAt", "likeCount", "retweetCount",
              "viewCount", "author.userName", "author.name", "author.followers"]
    out = []
    for it in rodar_ator(ATOR_X, entrada, fields):
        texto = _g(it, "fullText", "text")
        if not texto:
            continue
        autor = _g(it, "author.userName")
        out.append({
            "editoria": editoria, "tipo": "noticia", "fonte": f"X · @{autor}",
            "url": _g(it, "url"),
            "titulo": (texto[:90] + "…") if len(texto) > 90 else texto,
            "texto_recuperado": texto, "data": _iso(_g(it, "createdAt")),
            "_meta": {"likes": _g(it, "likeCount", default=0),
                      "rt": _g(it, "retweetCount", default=0),
                      "views": _g(it, "viewCount", default=0),
                      "seguidores_autor": _g(it, "author.followers", default=0)},
        })
    return out


def coletar_reddit(query: str, editoria: str, max_itens: int = 25,
                   periodo: str = "month") -> list[dict]:
    # "top" do período = o que teve mais engajamento (sinal), não só o mais novo.
    entrada = {"searchQuery": query, "sort": "top", "timeFilter": periodo,
               "maxPostsPerSource": max_itens, "includeComments": False}
    fields = ["title", "url", "permalink", "selfText", "score", "numComments",
              "subreddit", "author", "createdAt"]
    out = []
    for it in rodar_ator(ATOR_REDDIT, entrada, fields):
        out.append({
            "editoria": editoria, "tipo": "noticia",
            "fonte": f"Reddit · r/{_g(it, 'subreddit', default='?')}",
            "url": _g(it, "permalink", "url"), "titulo": _g(it, "title"),
            "texto_recuperado": _g(it, "selfText", "title"),
            "data": _iso(_g(it, "createdAt")),
            "_meta": {"score": _g(it, "score", default=0),
                      "comentarios": _g(it, "numComments", default=0)},
        })
    return out


def coletar_news(query: str, editoria: str, max_itens: int = 25,
                 lang: str = "pt", pais: str = "BR") -> list[dict]:
    entrada = {"queries": [query], "language": lang, "country": pais, "maxArticles": max_itens}
    fields = ["title", "url", "source", "publishedAt", "date", "snippet", "description"]
    out = []
    for it in rodar_ator(ATOR_NEWS, entrada, fields):
        out.append({
            "editoria": editoria, "tipo": "noticia",
            "fonte": f"Notícia · {_g(it, 'source', default='?')}",
            "url": _g(it, "url"), "titulo": _g(it, "title"),
            "texto_recuperado": _g(it, "snippet", "description", "title"),
            "data": _iso(_g(it, "publishedAt", "date")), "_meta": {},
        })
    return out


def coletar_web(query: str, editoria: str, max_resultados: int = 3) -> list[dict]:
    entrada = {"query": query, "maxResults": max_resultados, "outputFormats": ["markdown"]}
    out = []
    for it in rodar_ator(ATOR_WEB, entrada):
        out.append({
            "editoria": editoria, "tipo": "noticia",
            "fonte": f"Web · {_g(it, 'metadata.url', 'url')}",
            "url": _g(it, "metadata.url", "url"),
            "titulo": _g(it, "metadata.title", "title"),
            "texto_recuperado": str(_g(it, "markdown", "text"))[:4000],
            "data": _iso(""), "_meta": {},
        })
    return out


def coletar_aprofundamento(editoria: str, max_resultados: int = 3) -> list[dict]:
    """Artigos de DESENVOLVIMENTO ('Para aprofundar') via rag-web-browser.

    A query vem de editorias/aprofundamento.yaml (uma por editoria). É o que dá à
    revista peso de aprofundamento, não só de notícia — em todos os campos.
    """
    import yaml
    f = RAIZ / "editorias" / "aprofundamento.yaml"
    query = editoria
    if f.exists():
        query = (yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get(editoria, editoria)
    out = []
    for it in rodar_ator(ATOR_WEB, {"query": query, "maxResults": max_resultados,
                                    "outputFormats": ["markdown"]}):
        url = _g(it, "searchResult.url", "metadata.url")
        if not url:
            continue
        out.append({
            "editoria": editoria, "tipo": "aprofundamento", "fonte": "Para aprofundar",
            "url": url, "titulo": _g(it, "searchResult.title", "metadata.title"),
            "texto_recuperado": _g(it, "searchResult.description", default=""),
            "data": _iso(""), "_meta": {},
        })
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Fiação: lê a config das editorias, despacha para os coletores certos e deduplica.
# O pipeline diário chama coletar_editoria(); o resultado vai ao Editor-chefe/Redator.
# ─────────────────────────────────────────────────────────────────────────────

def _ler_editorias() -> dict:
    import yaml
    return yaml.safe_load((RAIZ / "editorias" / "editorias.yaml").read_text(encoding="utf-8"))


def coletar_editoria(editoria_id: str, termos: list[str], max_por_fonte: int = 20,
                     dedup: bool = True) -> list[dict]:
    """Roda todas as fontes Apify da editoria, para cada termo, e devolve o material
    bruto — deduplicado pelo ledger da editoria (se dedup=True). Sem LLM."""
    cfg = _ler_editorias()
    ed = next((e for e in cfg["editorias"] if e["id"] == editoria_id), None)
    if not ed:
        raise ValueError(f"editoria desconhecida: {editoria_id}")
    bruto: list[dict] = []
    for fonte in ed.get("fontes", []):
        if fonte.get("tipo") != "apify":
            continue
        func = globals().get(str(fonte.get("coletor", "")).split(":")[-1])
        if not callable(func):
            continue
        for termo in termos:
            try:
                bruto.extend(func(termo, editoria_id, max_por_fonte))
            except Exception as e:  # uma fonte falhar não derruba a coleta
                print(f"[apify] falha em {func.__name__}({termo!r}): {e}", file=sys.stderr)
    if dedup:
        sys.path.insert(0, str(RAIZ / "fontes"))
        import comum
        led = (ed.get("estado") or {}).get("ledger")
        if led:
            bruto = comum.deduplicar(bruto, RAIZ / led)
    return bruto


if __name__ == "__main__":
    termo = sys.argv[1] if len(sys.argv) > 1 else "AI agents"
    editoria = sys.argv[2] if len(sys.argv) > 2 else "ia"
    print(f"# coletar_editoria({editoria!r}, [{termo!r}])")
    for m in coletar_editoria(editoria, [termo], max_por_fonte=5, dedup=False):
        print("-", m["fonte"], "|", m["titulo"][:70], "|", m["url"])
