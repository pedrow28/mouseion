"""Orquestrador determinístico — monta a edição do dia a partir da config + cursores.

SEM LLM: para currículo, gera o esqueleto da aula (trilha + ideia central do
syllabus + os beats vazios) direto do cursor; para notícia, marca "aguardando
coleta". Prova o pipeline ponta a ponta. Na operação real, os beats/resumos vazios
são preenchidos pelo Redator (LLM) antes da diagramação.

Uso:  python3 motor/montar_edicao.py [AAAA-MM-DD]
"""
from __future__ import annotations

import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from motor import config, curriculo, diagramador, qa  # noqa: E402

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
         "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
DIAS_EXT = {"seg": "Segunda", "ter": "Terça", "qua": "Quarta", "qui": "Quinta",
            "sex": "Sexta", "sab": "Sábado", "dom": "Domingo"}
BEATS = ["Onde estamos", "Desenvolvimento", "Exemplo / aplicação",
         "Conexão", "Recordação", "Para guardar"]


def data_extenso(d: datetime.date) -> str:
    return f"{DIAS_EXT[config.DIAS[d.weekday()]]}, {d.day} de {MESES[d.month - 1]} de {d.year}"


def _render_aula(rotulo: str, aula: dict) -> str:
    beats = "".join(
        f'<div class="beat"><p class="beat-label">{b}</p>'
        f'<div class="beat-corpo"><p>[a redigir pelo Redator]</p></div></div>'
        for b in BEATS
    )
    ideia = aula["semente"] or aula["titulo"]
    return (
        f'<article class="aula"><span class="aula-trilha">'
        f'{rotulo} · {aula["tipo"]} {aula["posicao"]} de {aula["total"]}</span>'
        f'<div class="beat beat-ideia"><p class="beat-label">A ideia central</p>'
        f'<div class="beat-corpo"><p>{ideia}</p></div></div>{beats}</article>'
    )


def _materia_curriculo(ed: dict, data: datetime.date):
    est = ed.get("estado", {})
    if ed["id"] == "mente":
        fio = curriculo.fio_do_dia_mente(data)
        if not fio:
            return None
        syl = est["fios"][fio]["syllabus"]
        cursor = curriculo.ler_json(est["fios"][fio]["cursor"])
        rotulo = f'Mente · {fio}'
    elif ed["id"] == "imersao":
        # o cursor da Imersão (slot rotativo) vive dentro de tema_atual.json
        tema = curriculo.ler_json(est["tema"])
        syl = est["syllabus"]
        cursor = {"proxima_aula": tema.get("cursor", 1), "total": tema.get("total")}
        rotulo = f'Imersão · {tema.get("tema", "")}'
    else:
        syl = est["syllabus"]
        cursor = curriculo.ler_json(est["cursor"])
        rotulo = ed["nome"]
    aula = curriculo.aula_do_dia(syl, cursor)
    return _render_aula(rotulo, aula) if aula else None


def _materia_noticia(ed: dict) -> str:
    return (
        '<div class="placeholder"><span class="selo">Aguardando coleta</span>'
        '<p>O Pesquisador roda as fontes e o Redator escreve a partir do que for '
        'recuperado — com link, sem inventar.</p></div>'
    )


def montar(data: datetime.date, saida: str):
    cfg = config.carregar()
    eds = config.editorias_do_dia(cfg, data)
    materias: dict[str, str] = {}
    for ed in eds:
        html = _materia_curriculo(ed, data) if ed["motor"] == "curriculo" else _materia_noticia(ed)
        if html:
            materias[ed["id"]] = html
    meta = {
        "titulo_revista": "Mouseion",
        "tagline": "Metade notícia, metade formação.",
        "edicao_n": "Edição automática (motor)",
        "data_extenso": data_extenso(data),
    }
    html = diagramador.renderizar(materias, meta, saida=saida)
    ok, erros = qa.lint(html, list(materias.keys()))
    return html, ok, erros, list(materias.keys())


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "2026-06-20"
    d = datetime.date.fromisoformat(arg)
    out = Path(__file__).resolve().parents[1] / "edicoes" / "exemplo-motor.html"
    _, ok, erros, ids = montar(d, str(out))
    print("Data:", arg, "(" + config.dia_semana(d) + ")")
    print("Editorias do dia:", ", ".join(ids))
    print("QA:", "PASSOU" if ok else "FALHOU", erros or "")
    print("Saída:", out)
