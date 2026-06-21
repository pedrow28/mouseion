"""Carrega a configuração das editorias (editorias/editorias.yaml).

'Editorias são dados, não código' (CLAUDE.md, regra 5): o motor descobre as
editorias, a ordem, as fontes e a cadência LENDO este arquivo — nada é cravado aqui.
"""
from __future__ import annotations

from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
DIAS = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]


def carregar(caminho=None) -> dict:
    caminho = Path(caminho) if caminho else RAIZ / "editorias" / "editorias.yaml"
    return yaml.safe_load(Path(caminho).read_text(encoding="utf-8"))


def dia_semana(data) -> str:
    """datetime.date → 'seg'..'dom'."""
    return DIAS[data.weekday()]


def editorias_do_dia(cfg: dict, data) -> list:
    """As editorias cuja cadência inclui o dia de `data`, em ordem de edição."""
    dia = dia_semana(data)
    eds = [e for e in cfg["editorias"] if dia in (e.get("cadencia") or [])]
    return sorted(eds, key=lambda e: e.get("ordem", 99))
