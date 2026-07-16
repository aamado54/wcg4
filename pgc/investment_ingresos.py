"""
Ingresos Investment desde NewClientImportRow.

Fuente única para vista/reporte y para persistir en MonthlyMetricResult.
Regla (alineada con /pgc/ingresos/):
- suma TODOS los registros del mes de la UNE Investment (no solo counts_as_new)
- USD se toma tal cual; GTQ se convierte con MonthlyExchangeRate del mes de la fila
- NewClientImportRow.amount ya viene en miles (Monto del archivo ÷ 1000 al importar)
"""

from __future__ import annotations

from decimal import Decimal

from django.db.models import Q

from core.models import UNE
from imports.models import NewClientImportRow
from pgc.models import MonthlyExchangeRate

INVESTMENT_UNE_CODES = ("INVESTMENT", "INVESTMENTS", "INVERSIONES")


def get_investment_une() -> UNE | None:
    return (
        UNE.objects.filter(code__in=INVESTMENT_UNE_CODES)
        .order_by("sort_order", "id")
        .first()
    )


def build_fx_map() -> dict[tuple[int, int], Decimal]:
    return {
        (item.year, item.month): item.usd_to_gtq
        for item in MonthlyExchangeRate.objects.all()
    }


def row_period(row) -> tuple[int | None, int | None]:
    year = row.year or (row.header.year if getattr(row, "header_id", None) and row.header else None)
    month = row.month or (
        row.header.month if getattr(row, "header_id", None) and row.header else None
    )
    return year, month


def convert_row_amount_to_usd(row, fx_map: dict[tuple[int, int], Decimal]) -> Decimal:
    """Misma semántica que la vista de ingresos (USD tal cual, GTQ/FX, resto 0)."""
    amount = row.amount if row.amount is not None else Decimal("0")
    currency_code = ((row.currency.code if row.currency else "") or "").upper()

    if amount == 0:
        return Decimal("0")

    if currency_code in ("USD", "US$", "$"):
        return amount

    if currency_code in ("GTQ", "Q", "QUETZALES", "QUETZAL"):
        row_year, row_month = row_period(row)
        fx = fx_map.get((row_year, row_month))
        if fx and fx != 0:
            return amount / fx

    return Decimal("0")


def sum_investment_ingresos_usd(
    year: int,
    month: int,
    *,
    une: UNE | None = None,
    fx_map: dict[tuple[int, int], Decimal] | None = None,
) -> dict:
    """
    Totales Investment para un mes (misma lógica que /pgc/ingresos/).

    Returns:
        une, total_usd, used_rows, fx (TC del year/month pedido)
    """
    une = une or get_investment_une()
    fx_map = fx_map if fx_map is not None else build_fx_map()
    fx = fx_map.get((year, month))

    if not une:
        return {"une": None, "total_usd": Decimal("0"), "used_rows": 0, "fx": fx}

    period_q = Q(year=year, month=month) | Q(header__year=year, header__month=month)
    rows = (
        NewClientImportRow.objects.select_related("header", "currency", "une")
        .filter(une=une)
        .filter(period_q)
    )

    total = Decimal("0")
    used = 0
    for row in rows:
        row_year, row_month = row_period(row)
        if (row_year, row_month) != (year, month):
            continue
        total += convert_row_amount_to_usd(row, fx_map)
        used += 1

    return {"une": une, "total_usd": total, "used_rows": used, "fx": fx}


def investment_real_map_for_periods(
    periods: list[tuple[int, int]] | None = None,
    *,
    une: UNE | None = None,
    fx_map: dict[tuple[int, int], Decimal] | None = None,
) -> dict[tuple[int, int, int], Decimal]:
    """
    Mapa (year, month, une_id) -> total USD.
    Si periods es None, usa todas las filas Investment.
    """
    une = une or get_investment_une()
    fx_map = fx_map if fx_map is not None else build_fx_map()
    out: dict[tuple[int, int, int], Decimal] = {}
    if not une:
        return out

    qs = NewClientImportRow.objects.select_related("header", "currency", "une").filter(
        une=une
    )
    if periods:
        detail_period_q = Q()
        for y, m in periods:
            detail_period_q |= Q(year=y, month=m)
            detail_period_q |= Q(header__year=y, header__month=m)
        qs = qs.filter(detail_period_q)

    for row in qs:
        row_year, row_month = row_period(row)
        if not row_year or not row_month:
            continue
        key = (row_year, row_month, une.id)
        out[key] = out.get(key, Decimal("0")) + convert_row_amount_to_usd(row, fx_map)
    return out
