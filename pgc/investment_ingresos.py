"""
Ingresos Investment para PGC.

Fuente PGC (ingresos vs meta / tablero):
- Crecimiento neto mensual en miles de US$ dolarizado de AP + PG + préstamos bancarios.
- Se calcula como delta del total dolarizado respecto al mes anterior con datos.

Fuente histórica (clientes nuevos):
- sum_investment_ingresos_usd sigue disponible para detalle/browse de clientes nuevos.
"""

from __future__ import annotations

from decimal import Decimal

from django.db.models import Q, Sum

from core.models import UNE
from imports.models import BankLoanMonthSnapshot, InvestmentGrowthRow, NewClientImportRow
from pgc.models import MonthlyExchangeRate

INVESTMENT_UNE_CODES = ("INVESTMENT", "INVESTMENTS", "INVERSIONES")
MILES_DIVISOR = Decimal("1000")


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
        if (not fx or fx == 0) and fx_map:
            prior = [k for k in fx_map if k <= (row_year or 0, row_month or 0)]
            if prior:
                fx = fx_map[max(prior)]
        if fx and fx != 0:
            return amount / fx

    return Decimal("0")


def has_investment_growth_data() -> bool:
    return InvestmentGrowthRow.objects.exists() or BankLoanMonthSnapshot.objects.exists()


def investment_periods_with_data() -> list[tuple[int, int]]:
    inv_periods = set(
        InvestmentGrowthRow.objects.values_list("year", "month").distinct()
    )
    bank_periods = set(
        BankLoanMonthSnapshot.objects.values_list("year", "month").distinct()
    )
    return sorted(inv_periods | bank_periods)


def investment_gross_usd(year: int, month: int) -> dict[str, Decimal | None]:
    """
    Totales brutos dolarizados al cierre del mes (USD completos, no miles).
    """
    inv = (
        InvestmentGrowthRow.objects.filter(year=year, month=month)
        .values("instrument")
        .annotate(total=Sum("amount_usd"))
    )
    ap_usd = Decimal("0")
    pg_usd = Decimal("0")
    for row in inv:
        if row["instrument"] == "AP":
            ap_usd = row["total"] or Decimal("0")
        elif row["instrument"] == "PG":
            pg_usd = row["total"] or Decimal("0")

    bank = BankLoanMonthSnapshot.objects.filter(year=year, month=month).first()
    banks_usd = bank.total_usd if bank else Decimal("0")

    has_inv = InvestmentGrowthRow.objects.filter(year=year, month=month).exists()
    has_bank = bank is not None
    if not has_inv and not has_bank:
        return {
            "ap_usd": None,
            "pg_usd": None,
            "banks_usd": None,
            "total_usd": None,
            "has_data": False,
        }

    total_usd = ap_usd + pg_usd + banks_usd
    return {
        "ap_usd": ap_usd,
        "pg_usd": pg_usd,
        "banks_usd": banks_usd,
        "total_usd": total_usd,
        "has_data": True,
    }


def _previous_period(year: int, month: int) -> tuple[int, int]:
    if month > 1:
        return year, month - 1
    return year - 1, 12


def _banks_snapshot_exists(year: int, month: int) -> bool:
    return BankLoanMonthSnapshot.objects.filter(year=year, month=month).exists()


def _ap_pg_total_usd(gross: dict[str, Decimal | None]) -> Decimal | None:
    if not gross.get("has_data"):
        return None
    ap = gross.get("ap_usd")
    pg = gross.get("pg_usd")
    if ap is None and pg is None:
        return None
    return (ap or Decimal("0")) + (pg or Decimal("0"))


def investment_net_growth_usd(year: int, month: int) -> Decimal | None:
    """Incremento mensual del total dolarizado (USD completos). None si no hay mes previo."""
    current = investment_gross_usd(year, month)
    if not current["has_data"] or current["total_usd"] is None:
        return None

    prev_year, prev_month = _previous_period(year, month)
    previous = investment_gross_usd(prev_year, prev_month)
    if not previous["has_data"] or previous["total_usd"] is None:
        return None

    cur_banks = _banks_snapshot_exists(year, month)
    prev_banks = _banks_snapshot_exists(prev_year, prev_month)
    # Evita deltas falsos cuando un mes trae bancos y el otro no (p. ej. ago sin Bancos_Fin_de_mes).
    if cur_banks != prev_banks:
        cur_ap_pg = _ap_pg_total_usd(current)
        prev_ap_pg = _ap_pg_total_usd(previous)
        if cur_ap_pg is None or prev_ap_pg is None:
            return None
        return cur_ap_pg - prev_ap_pg

    return current["total_usd"] - previous["total_usd"]


def investment_net_growth_miles(year: int, month: int) -> Decimal | None:
    growth = investment_net_growth_usd(year, month)
    if growth is None:
        return None
    return growth / MILES_DIVISOR


def investment_growth_summary(
    year: int,
    month: int,
    *,
    une: UNE | None = None,
) -> dict:
    """
    Resumen para recálculo PGC / vistas.

    measured_value en miles USD = crecimiento neto mensual dolarizado.
    """
    une = une or get_investment_une()
    gross = investment_gross_usd(year, month)
    growth_usd = investment_net_growth_usd(year, month)
    growth_miles = (
        growth_usd / MILES_DIVISOR if growth_usd is not None else None
    )

    bank = BankLoanMonthSnapshot.objects.filter(year=year, month=month).first()
    fx = bank.exchange_rate if bank else build_fx_map().get((year, month))
    op_count = InvestmentGrowthRow.objects.filter(year=year, month=month).count()

    return {
        "une": une,
        "gross": gross,
        "growth_usd": growth_usd,
        "growth_miles": growth_miles,
        "total_miles": (
            gross["total_usd"] / MILES_DIVISOR
            if gross.get("total_usd") is not None
            else None
        ),
        "fx": fx,
        "operation_count": op_count,
        "has_growth_data": bool(gross.get("has_data")),
    }


def investment_real_map_for_periods(
    periods: list[tuple[int, int]] | None = None,
    *,
    une: UNE | None = None,
    fx_map: dict[tuple[int, int], Decimal] | None = None,
) -> dict[tuple[int, int, int], Decimal]:
    """
    Mapa (year, month, une_id) -> crecimiento neto mensual en miles USD.

    Si no hay datos de crecimiento, conserva el fallback histórico desde clientes nuevos.
    """
    une = une or get_investment_une()
    out: dict[tuple[int, int, int], Decimal] = {}
    if not une:
        return out

    if has_investment_growth_data():
        if periods is None:
            periods = investment_periods_with_data()
        for year, month in periods:
            growth = investment_net_growth_miles(year, month)
            if growth is not None:
                out[(year, month, une.id)] = growth
        return out

    # Fallback legado: suma bruta de clientes nuevos (miles).
    fx_map = fx_map if fx_map is not None else build_fx_map()
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


def sum_investment_ingresos_usd(
    year: int,
    month: int,
    *,
    une: UNE | None = None,
    fx_map: dict[tuple[int, int], Decimal] | None = None,
) -> dict:
    """
    Valor PGC de ingresos Investment para un mes.

    Prioridad: crecimiento neto mensual (miles USD) desde AP/PG + bancos.
    Fallback: suma bruta de clientes nuevos del mes.
    """
    une = une or get_investment_une()
    fx_map = fx_map if fx_map is not None else build_fx_map()
    fx = fx_map.get((year, month))

    if has_investment_growth_data():
        summary = investment_growth_summary(year, month, une=une)
        growth_miles = summary["growth_miles"]
        if growth_miles is None:
            return {
                "une": une,
                "total_usd": Decimal("0"),
                "used_rows": summary["operation_count"],
                "fx": summary["fx"] or fx,
                "growth_usd": None,
                "gross": summary["gross"],
                "source": "investment_growth",
                "note": "Sin mes anterior para calcular crecimiento neto.",
            }
        note = ""
        if (
            summary["growth_usd"] is not None
            and _banks_snapshot_exists(year, month)
            != _banks_snapshot_exists(*_previous_period(year, month))
        ):
            note = (
                "Crecimiento calculado solo AP+PG (un mes con bancos y el otro sin snapshot bancario)."
            )
        return {
            "une": une,
            "total_usd": growth_miles,
            "used_rows": summary["operation_count"],
            "fx": summary["fx"] or fx,
            "growth_usd": summary["growth_usd"],
            "gross": summary["gross"],
            "source": "investment_growth",
            "note": note,
        }

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

    return {
        "une": une,
        "total_usd": total,
        "used_rows": used,
        "fx": fx,
        "source": "new_clients",
        "note": "",
    }
