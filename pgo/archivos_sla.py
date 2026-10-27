"""Plazos PGO sobre expedientes (100% de casos dentro del tiempo)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import Enum


class SlaKind(str, Enum):
    SAME_CALENDAR_DAY = "same_day"
    NEXT_BUSINESS_DAY = "next_business_day"
    BUSINESS_DAYS = "business_days"
    CALENDAR_DAYS = "calendar_days"


@dataclass(frozen=True)
class SlaRule:
    kind: SlaKind
    days: int = 0


# concept_id → plazo (PGO-.md / reglas operativas)
CONCEPT_SLA: dict[str, SlaRule] = {
    "legal_garantias_100": SlaRule(SlaKind.SAME_CALENDAR_DAY),
    "legal_tiempos_garantias_3d": SlaRule(SlaKind.BUSINESS_DAYS, 3),
    "legal_titulos_inversion": SlaRule(SlaKind.BUSINESS_DAYS, 2),
    "legal_actas_comite": SlaRule(SlaKind.NEXT_BUSINESS_DAY),
    "fr_analisis_10d": SlaRule(SlaKind.BUSINESS_DAYS, 10),
}


def _is_weekend(d: date) -> bool:
    return d.weekday() >= 5


def add_business_days(start: date, n: int) -> date:
    if n <= 0:
        return start
    d = start
    added = 0
    while added < n:
        d += timedelta(days=1)
        if not _is_weekend(d):
            added += 1
    return d


def next_business_day(start: date) -> date:
    d = start + timedelta(days=1)
    while _is_weekend(d):
        d += timedelta(days=1)
    return d


def deadline(inicio: datetime, rule: SlaRule) -> datetime:
    d0 = inicio.date()
    if rule.kind == SlaKind.SAME_CALENDAR_DAY:
        return datetime.combine(d0, datetime.max.time()).replace(microsecond=0)
    if rule.kind == SlaKind.NEXT_BUSINESS_DAY:
        end = next_business_day(d0)
        return datetime.combine(end, datetime.max.time()).replace(microsecond=0)
    if rule.kind == SlaKind.BUSINESS_DAYS:
        end = add_business_days(d0, rule.days)
        return datetime.combine(end, datetime.max.time()).replace(microsecond=0)
    end = d0 + timedelta(days=rule.days)
    return datetime.combine(end, datetime.max.time()).replace(microsecond=0)


def cumple_plazo(inicio: datetime, entrega: datetime, rule: SlaRule) -> bool:
    """Entrega a tiempo: cualquier hora del día límite cuenta (día siguiente hábil, etc.)."""
    if inicio.tzinfo is not None:
        inicio = inicio.replace(tzinfo=None)
    if entrega.tzinfo is not None:
        entrega = entrega.replace(tzinfo=None)
    lim = deadline(inicio, rule)
    return entrega <= lim
