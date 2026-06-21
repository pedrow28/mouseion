"""QA estrutural (determinístico) — valida a edição antes de publicar.

Não avalia estética (CLAUDE.md, regra 4); só estrutura: tokens resolvidos, nenhuma
editoria do dia vazia, e link presente nas matérias de Saúde (regra de ouro).
"""
from __future__ import annotations

import re


def lint(html: str, editorias_esperadas: list[str]) -> tuple[bool, list[str]]:
    erros: list[str] = []

    if re.search(r"\{\{.*?\}\}", html):
        erros.append("token {{...}} não resolvido")
    if re.search(r"<!--\s*/?SLOT", html):
        erros.append("marcador SLOT remanescente")

    for eid in editorias_esperadas:
        m = re.search(
            r'<section class="editoria[^"]*" id="%s">(.*?)</section>' % re.escape(eid),
            html, re.S,
        )
        if not m:
            erros.append(f"editoria ausente: {eid}")
            continue
        texto = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if len(texto) < 20:
            erros.append(f"editoria vazia: {eid}")

    return (len(erros) == 0, erros)


def checar_links_saude(html: str) -> list[str]:
    """Aviso se a seção Saúde não tiver nenhum link de fonte."""
    avisos: list[str] = []
    m = re.search(r'id="saude">(.*?)</section>', html, re.S)
    if m and "href=" not in m.group(1):
        avisos.append("Saúde sem link de fonte (regra de ouro)")
    return avisos
