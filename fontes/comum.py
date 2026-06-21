"""Utilidades determinísticas de coleta — hash, normalização e ledger de dedup.

Sem LLM. Usado pelo Pesquisador das editorias de notícia para garantir a regra
"sem repetir pauta" (CLAUDE.md, regra 3): cada item recebe um hash; o que já está
no ledger é descartado.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path


def normalizar_texto(s: str) -> str:
    """Minúsculas, acentuação normalizada e espaços colapsados — base estável para o hash."""
    s = unicodedata.normalize("NFKC", s or "")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def hash_item(*partes: str) -> str:
    """SHA-1 de uma ou mais partes normalizadas (ex.: url + título + texto)."""
    base = "␟".join(normalizar_texto(p) for p in partes if p)
    return hashlib.sha1(base.encode("utf-8")).hexdigest()


def carregar_ledger(caminho) -> set[str]:
    """Lê o ledger .jsonl e devolve o conjunto de hashes já publicados."""
    p = Path(caminho)
    hashes: set[str] = set()
    if p.exists():
        for linha in p.read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if not linha:
                continue
            try:
                hashes.add(json.loads(linha)["hash"])
            except Exception:
                pass
    return hashes


def registrar(caminho, h: str, url: str, titulo: str, data: str) -> None:
    """Anexa um item ao ledger (uma linha JSON por publicação)."""
    p = Path(caminho)
    p.parent.mkdir(parents=True, exist_ok=True)
    reg = {"hash": h, "url": url, "titulo": titulo, "data_saida": data}
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")


def deduplicar(itens, caminho_ledger):
    """Filtra `itens` (dicts com url/titulo/texto_recuperado) mantendo só os inéditos.

    Cada item devolvido ganha o campo `_hash`. Não grava no ledger — isso é feito
    depois da publicação, via `registrar`.
    """
    vistos = carregar_ledger(caminho_ledger)
    novos = []
    for it in itens:
        h = hash_item(it.get("url", ""), it.get("titulo", ""), it.get("texto_recuperado", ""))
        if h in vistos:
            continue
        vistos.add(h)
        novos.append({**it, "_hash": h})
    return novos
