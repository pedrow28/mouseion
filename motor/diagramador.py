"""Diagramador (determinístico) — encaixa as matérias do dia no template fixo.

Sem LLM e sem decisão estética (CLAUDE.md, regra 4): preenche os slots de
template/base.html, regenera o sumário com as editorias presentes e remove as
seções das editorias que não saem hoje.
"""
from __future__ import annotations

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def _nome_da_secao(html: str, eid: str) -> str:
    m = re.search(
        r'id="%s">.*?<h2 class="editoria-nome">(.*?)</h2>' % re.escape(eid),
        html, re.S,
    )
    return m.group(1).strip() if m else eid


def _slot_sub(html: str, eid: str, conteudo: str) -> str:
    padrao = re.compile(r"(<!-- SLOT:%s -->).*?(<!-- /SLOT -->)" % re.escape(eid), re.S)
    return padrao.sub(lambda m: m.group(1) + conteudo + m.group(2), html)


def renderizar(materias: dict, meta: dict, base=None, saida=None) -> str:
    """materias: {editoria_id: html}. meta: titulo_revista, tagline, edicao_n, data_extenso.

    Devolve o HTML final; grava em `saida` se informado.
    """
    base = Path(base) if base else RAIZ / "template" / "base.html"
    html = base.read_text(encoding="utf-8")

    # 0) descarta o comentário de documentação do template (não vai para a edição)
    html = re.sub(r"<!DOCTYPE html>\s*<!--.*?-->", "<!DOCTYPE html>", html, count=1, flags=re.S)

    # 1) tokens do masthead/rodapé
    for k, v in {
        "{{TITULO_REVISTA}}": meta["titulo_revista"],
        "{{TAGLINE}}": meta["tagline"],
        "{{EDICAO_N}}": meta["edicao_n"],
        "{{DATA_EXTENSO}}": meta["data_extenso"],
    }.items():
        html = html.replace(k, v)

    # 2) editorias presentes, na ordem em que aparecem no template
    ids_template = re.findall(r'<section class="editoria[^"]*" id="([^"]+)">', html)
    presentes = [eid for eid in ids_template if eid in materias]

    # 3) regenera o sumário só com as editorias do dia
    lis = "".join(
        f'<li class="e-{eid}"><span class="ponto"></span>'
        f'<a href="#{eid}">{_nome_da_secao(html, eid)}</a></li>'
        for eid in presentes
    )
    html = re.sub(
        r'(<nav class="sumario">.*?<ol>).*?(</ol>)',
        lambda m: m.group(1) + lis + m.group(2),
        html, flags=re.S,
    )

    # 4) preenche slots / remove seções que não saem hoje
    for eid in ids_template:
        if eid in materias:
            html = _slot_sub(html, eid, materias[eid])
        else:
            html = re.sub(
                r'\s*<section class="editoria[^"]*" id="%s">.*?</section>' % re.escape(eid),
                "", html, flags=re.S,
            )

    # 5) limpeza defensiva de marcadores/tokens remanescentes
    html = re.sub(r"<!-- /?SLOT[^>]*-->", "", html)
    html = re.sub(r"\{\{SLOT_[^}]*\}\}", "", html)

    if saida:
        Path(saida).write_text(html, encoding="utf-8")
    return html
