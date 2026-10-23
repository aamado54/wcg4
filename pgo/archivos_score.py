"""Puntaje mensual desde expedientes Archivos (100% en plazo = puntos máximos)."""

from __future__ import annotations

from pgo.archivos_sla import CONCEPT_SLA, cumple_plazo
from pgo.models import PgoExpediente
from pgo.scorecard_engine import CellScore


def score_concept_month_from_expedientes(
    concept_id: str,
    year: int,
    month: int,
    une: str,
    max_pts: float,
) -> CellScore | None:
    if concept_id not in CONCEPT_SLA:
        return None
    rule = CONCEPT_SLA[concept_id]
    qs = PgoExpediente.objects.filter(
        concept_id=concept_id,
        une=une,
        fecha_inicio__year=year,
        fecha_inicio__month=month,
    )
    total = qs.count()
    if total == 0:
        return None

    cerrados = qs.exclude(fecha_entrega__isnull=True)
    if cerrados.count() < total:
        return CellScore(
            points=0.0,
            max_points=max_pts,
            confidence="high",
            note=f"{cerrados.count()}/{total} expedientes con fecha de entrega",
        )

    on_time = 0
    for ex in cerrados:
        ok = ex.cumple_plazo
        if ok is None and ex.fecha_entrega:
            ok = cumple_plazo(ex.fecha_inicio, ex.fecha_entrega, rule)
        if ok:
            on_time += 1

    if on_time == total:
        return CellScore(
            points=max_pts,
            max_points=max_pts,
            confidence="high",
            note=f"100% ({total}) expedientes en plazo ({rule.kind.value})",
        )
    return CellScore(
        points=0.0,
        max_points=max_pts,
        confidence="high",
        note=f"{on_time}/{total} expedientes en plazo; se requiere 100%",
    )
