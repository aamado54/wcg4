"""Mapeo de filas Archivos → concepto PGO y UNE."""

from __future__ import annotations

import re

from pgo.scorecard_catalog import UNE_CODES

_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"garant", re.I), "legal_tiempos_garantias_3d"),
    (re.compile(r"comit[eé]", re.I), "legal_actas_comite"),
    (re.compile(r"t[ií]tulo|inversi[oó]n|pr[eé]stamo", re.I), "legal_titulos_inversion"),
    (re.compile(r"an[aá]lisis|caso|cr[eé]dito|planner", re.I), "fr_analisis_10d"),
    (re.compile(r"registro.*garant|garant.*100", re.I), "legal_garantias_100"),
]

_UNE_ALIASES = {
    "factoring": "FACTORING",
    "factoraje": "FACTORING",
    "f": "FACTORING",
    "leasing": "LEASING",
    "l": "LEASING",
    "investment": "INVESTMENT",
    "inversion": "INVESTMENT",
    "i": "INVESTMENT",
    "insurance": "INSURANCE",
    "seguros": "INSURANCE",
    "s": "INSURANCE",
}


def infer_concept_id(*texts: str | None) -> str | None:
    blob = " ".join(t for t in texts if t).strip()
    if not blob:
        return None
    for pat, cid in _PATTERNS:
        if pat.search(blob):
            return cid
    return None


def infer_une(*texts: str | None) -> str | None:
    blob = " ".join(t for t in texts if t).lower()
    for key, code in _UNE_ALIASES.items():
        if key in blob:
            return code
    for code in UNE_CODES:
        if code.lower() in blob:
            return code
    return None
