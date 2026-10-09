"""
Matriz anual de cumplimiento: 12 meses × UNEs (respuesta a requerimientos).
"""

from __future__ import annotations

from datetime import date

from django.db import transaction

from pgc.admin_manual import (
    REQUIREMENTS_MONTH_LABELS_SHORT,
    _get_plan,
    _unes,
    build_requirements_matrix,
    save_requirements,
)


def through_month_for_year(year: int, now: date | None = None) -> int:
    """Último mes editable «hasta la fecha» para el año seleccionado."""
    today = now or date.today()
    if year < today.year:
        return 12
    if year > today.year:
        return 0
    return today.month


def get_requirements_year_context(year: int, now: date | None = None) -> dict:
    plan = _get_plan(year)
    unes = _unes()
    headers, matrix, months = build_requirements_matrix(plan, year, 1, 12, unes=unes)
    through = through_month_for_year(year, now=now)
    through_label = REQUIREMENTS_MONTH_LABELS_SHORT.get(through, str(through)) if through else ""
    return {
        "year": year,
        "plan": plan,
        "unes": unes,
        "requirements_month_headers": headers,
        "requirements_matrix": matrix,
        "requirements_months": months,
        "through_month": through,
        "through_month_label": through_label,
        "label": str(year),
    }


@transaction.atomic
def save_requirements_year(user, year: int, post_data, reason: str = "") -> int:
    """Persiste la matriz enero–diciembre vía save_requirements."""
    return save_requirements(
        user,
        year,
        12,
        post_data,
        reason,
        month_from=1,
    )
