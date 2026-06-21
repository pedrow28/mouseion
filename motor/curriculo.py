"""Motor de currículo (determinístico).

Lê o cursor, extrai a aula do dia do syllabus e avança o cursor. Resolve o fio do
dia (Mente) pela rotação. O Redator nunca escolhe a aula — ela vem daqui.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DIAS = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]

# Casa "- [ ] **Aula 1 — Título.** Ideia central: ... (ref: ...)" e as variantes
# Pílula (Imersão) e Lição (Família).
# Aceita uma faceta opcional entre o número e o travessão, ex.: "Lição 1 (P/M) — ..."
PADRAO = re.compile(r"\*\*(Aula|Pílula|Lição)\s+(\d+)\s*(?:\([^)]*\))?\s*[—-]\s+(.+?)\.?\*\*\s*(.*)")


def _abs(p) -> Path:
    p = Path(p)
    return p if p.is_absolute() else RAIZ / p


def ler_json(p) -> dict:
    return json.loads(_abs(p).read_text(encoding="utf-8"))


def escrever_json(p, obj) -> None:
    _abs(p).write_text(json.dumps(obj, ensure_ascii=False) + "\n", encoding="utf-8")


def _limpar_semente(texto: str) -> str:
    texto = re.sub(r"\(ref:[^)]*\)", "", texto)
    texto = re.sub(r"^Ideia central:\s*", "", texto.strip())
    texto = re.split(r"Micro-prática:", texto)[0]
    return texto.strip()


def parsear_syllabus(caminho) -> list[dict]:
    """Lista de aulas do syllabus: {posicao, tipo, titulo, semente}."""
    aulas = []
    for linha in _abs(caminho).read_text(encoding="utf-8").splitlines():
        m = PADRAO.search(linha)
        if m:
            aulas.append({
                "posicao": int(m.group(2)),
                "tipo": m.group(1),
                "titulo": m.group(3).strip(),
                "semente": _limpar_semente(m.group(4)),
            })
    aulas.sort(key=lambda a: a["posicao"])
    return aulas


def aula_do_dia(syllabus, cursor: dict) -> dict | None:
    """A aula na posição `cursor['proxima_aula']`, anotada com total e eh_revisao."""
    aulas = parsear_syllabus(syllabus)
    pos = cursor.get("proxima_aula", 1)
    for a in aulas:
        if a["posicao"] == pos:
            return {
                **a,
                "total": cursor.get("total", len(aulas)),
                "eh_revisao": "revis" in a["titulo"].lower(),
            }
    return None


def fio_do_dia_mente(data) -> str | None:
    """Resolve qual fio de Mente sai hoje (psicologia/filosofia/teologia ou None)."""
    rot = ler_json("estado/mente/rotacao.json")
    return rot["dias"].get(DIAS[data.weekday()])


def avancar(cursor_path) -> dict:
    """Incrementa o cursor (respeitando o total) e grava. Chamar após publicar."""
    c = ler_json(cursor_path)
    total = c.get("total")
    if total is None or c.get("proxima_aula", 1) < total:
        c["proxima_aula"] = c.get("proxima_aula", 1) + 1
    escrever_json(cursor_path, c)
    return c
