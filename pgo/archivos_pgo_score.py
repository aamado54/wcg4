"""Puntaje desde exports ArchivosPGO (Carpeta / Archivo / CreadoEn)."""

from __future__ import annotations

from datetime import datetime, time

from pgo.archivos_pgo_parse import parse_event_date_from_archivo
from pgo.archivos_sla import CONCEPT_SLA, cumple_plazo
from pgo.models import PgoArchivoRegistro
from pgo.scorecard_engine import CellScore

# Carpeta (normalizada) → concept_id PGO
_CARPETA_CONCEPT: list[tuple[str, str]] = [
    ("legal/memoria comite", "legal_actas_comite"),
]


def _concept_for_carpeta(carpeta: str) -> str | None:
    c = (carpeta or "").lower().replace("\\", "/")
    for needle, cid in _CARPETA_CONCEPT:
        if needle in c:
            return cid
    return None


def _cumple_evento_creado(event_day, creado_en: datetime, concept_id: str) -> bool:
    rule = CONCEPT_SLA.get(concept_id)
    if not rule:
        return False
    inicio = datetime.combine(event_day, time.min)
    return cumple_plazo(inicio, creado_en, rule)


def score_concept_month_from_archivos_pgo(
    concept_id: str,
    year: int,
    month: int,
    une: str,
    max_pts: float,
) -> CellScore | None:
    if concept_id == "legal_actas_comite" and une not in ("FACTORING", "LEASING"):
        return None
    if concept_id not in CONCEPT_SLA:
        return None

    rows = [
        r
        for r in PgoArchivoRegistro.objects.all().only(
            "carpeta", "archivo", "creado_en", "event_date"
        )
        if _concept_for_carpeta(r.carpeta) == concept_id
    ]
    month_rows = [
        r
        for r in rows
        if r.event_date and r.event_date.year == year and r.event_date.month == month
    ]
    if not month_rows:
        return None

    failures: list[str] = []
    for r in month_rows:
        if not r.creado_en:
            failures.append(r.archivo[:60])
            continue
        if not _cumple_evento_creado(r.event_date, r.creado_en, concept_id):
            failures.append(r.archivo[:60])

    rule = CONCEPT_SLA[concept_id]
    label = rule.kind.value
    total = len(month_rows)
    if failures:
        return CellScore(
            points=0.0,
            max_points=max_pts,
            confidence="high",
            note=f"0/{total} cumplen ({label}); falló p. ej. {failures[0]}",
        )
    return CellScore(
        points=max_pts,
        max_points=max_pts,
        confidence="high",
        note=f"100% ({total}) memos/actas en plazo ({label})",
    )
