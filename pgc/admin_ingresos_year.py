"""
Matriz anual de ingresos reales: 12 meses × 4 UNEs + TC editable.
"""

from __future__ import annotations

from decimal import Decimal

from django.db import transaction

from core.models import MetricDefinition, UNE
from imports.models import BankLoanMonthSnapshot, InvestmentGrowthRow
from pgc.admin_manual import log_manual_edit, save_fx
from pgc.admin_utils import parse_decimal_or_none
from pgc.income_conversion import (
    apply_result_achievement,
    format_currency_display,
    format_usd_3,
    get_fx_rate,
    gtq_to_usd,
)
from pgc.investment_ingresos import (
    MILES_DIVISOR,
    _ap_pg_total_usd,
    _previous_period,
    get_investment_une,
    investment_gross_usd,
    investment_net_growth_usd,
)
from pgc.models import (
    AdminManualEditLog,
    MonthlyExchangeRate,
    MonthlyMetricResult,
    PGCPlan,
)

MONTH_LABELS = (
    (1, "Enero"),
    (2, "Febrero"),
    (3, "Marzo"),
    (4, "Abril"),
    (5, "Mayo"),
    (6, "Junio"),
    (7, "Julio"),
    (8, "Agosto"),
    (9, "Septiembre"),
    (10, "Octubre"),
    (11, "Noviembre"),
    (12, "Diciembre"),
)


def _unes() -> list[UNE]:
    return list(UNE.objects.filter(is_active=True).order_by("sort_order", "code"))


def _ingresos_metric() -> MetricDefinition | None:
    return MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()


def _display_pgc_miles(
    miles_usd: Decimal | None,
    *,
    fx: Decimal | None,
    currency: str,
    usd_full_for_gtq: Decimal | None = None,
) -> tuple[str | None, str | None]:
    """
    PGC matriz: cifras en miles USD (misma dimensión que measured_value / tablero).
    En modo Q, el principal sigue en miles USD; subtexto con referencia en Q si hay TC.
    """
    if miles_usd is None:
        return None, None
    miles_label = format_currency_display(miles_usd)
    if currency == MonthlyMetricResult.CURRENCY_GTQ:
        if fx and fx > 0 and usd_full_for_gtq is not None:
            gtq_ref = usd_full_for_gtq * fx
            return miles_label, f"Q ref: {format_currency_display(gtq_ref)}"
        return miles_label, None
    return miles_label, None


def _usd_full_to_miles(usd: Decimal | None) -> Decimal | None:
    if usd is None:
        return None
    return usd / MILES_DIVISOR


def _build_investment_audit(
    year: int,
    month: int,
    *,
    fx: Decimal | None,
    currency: str,
    result_obj: MonthlyMetricResult | None,
) -> dict:
    gross = investment_gross_usd(year, month)
    prev_y, prev_m = _previous_period(year, month)
    prev_gross = investment_gross_usd(prev_y, prev_m)

    inv_usd = _ap_pg_total_usd(gross)
    loans_usd = gross.get("banks_usd") if gross.get("has_data") else None
    cap_usd = gross.get("total_usd")

    prev_cap_usd = (
        prev_gross.get("total_usd") if prev_gross.get("has_data") else None
    )
    growth_usd = investment_net_growth_usd(year, month)
    growth_miles = (
        growth_usd / MILES_DIVISOR if growth_usd is not None else None
    )

    stored_miles = (
        getattr(result_obj, "measured_value", None) if result_obj else None
    )
    stored_growth_usd = (
        stored_miles * MILES_DIVISOR if stored_miles is not None else None
    )

    delta_from_levels = None
    if cap_usd is not None and prev_cap_usd is not None:
        delta_from_levels = cap_usd - prev_cap_usd

    growth_matches_levels = (
        growth_usd is not None
        and delta_from_levels is not None
        and growth_usd == delta_from_levels
    )
    stored_matches_growth = False
    if growth_miles is not None and stored_miles is not None:
        stored_matches_growth = (
            growth_miles.quantize(Decimal("0.001"))
            == stored_miles.quantize(Decimal("0.001"))
        )

    inv_miles = _usd_full_to_miles(inv_usd)
    loans_miles = _usd_full_to_miles(loans_usd)
    inv_disp, inv_sub = _display_pgc_miles(
        inv_miles, fx=fx, currency=currency, usd_full_for_gtq=inv_usd
    )
    loans_disp, loans_sub = _display_pgc_miles(
        loans_miles, fx=fx, currency=currency, usd_full_for_gtq=loans_usd
    )
    growth_disp, growth_sub = _display_pgc_miles(
        growth_miles, fx=fx, currency=currency, usd_full_for_gtq=growth_usd
    )

    return {
        "has_ap_pg": bool(
            gross.get("has_data")
            and InvestmentGrowthRow.objects.filter(year=year, month=month).exists()
        ),
        "has_bank": BankLoanMonthSnapshot.objects.filter(year=year, month=month).exists(),
        "inversiones_display": inv_disp,
        "inversiones_sub": inv_sub,
        "prestamos_display": loans_disp,
        "prestamos_sub": loans_sub,
        "growth_display": growth_disp,
        "growth_sub": growth_sub,
        "growth_miles": growth_miles,
        "stored_miles": stored_miles,
        "growth_usd": growth_usd,
        "captaciones_usd": cap_usd,
        "prev_captaciones_usd": prev_cap_usd,
        "growth_matches_levels": growth_matches_levels,
        "stored_matches_growth": stored_matches_growth,
        "partial_bank_month": (
            gross.get("has_data")
            and prev_gross.get("has_data")
            and BankLoanMonthSnapshot.objects.filter(year=year, month=month).exists()
            != BankLoanMonthSnapshot.objects.filter(year=prev_y, month=prev_m).exists()
        ),
        "note": (
            "Δ con solo AP+PG (un mes tiene bancos y el otro no)."
            if growth_usd is not None
            and delta_from_levels is not None
            and growth_usd != delta_from_levels
            else ""
        ),
    }


def _normalize_currency(raw: str | None) -> str:
    curr = (raw or "GTQ").strip().upper()
    if curr in ("Q", "GTQ"):
        return MonthlyMetricResult.CURRENCY_GTQ
    if curr in ("$", "USD", "US$"):
        return MonthlyMetricResult.CURRENCY_USD
    return MonthlyMetricResult.CURRENCY_GTQ


def get_ingresos_year_context(year: int, capture_currency: str = "GTQ") -> dict:
    currency = _normalize_currency(capture_currency)
    plan = PGCPlan.objects.filter(year=year).first()
    unes = _unes()
    metric = _ingresos_metric()
    investment_une = get_investment_une()

    fx_by_month = {
        r.month: r
        for r in MonthlyExchangeRate.objects.filter(year=year)
    }
    results_map: dict[tuple[int, int], MonthlyMetricResult] = {}
    if plan and metric:
        for row in MonthlyMetricResult.objects.filter(
            plan=plan, metric=metric, year=year
        ).select_related("une"):
            results_map[(row.month, row.une_id)] = row

    month_rows = []
    missing_fx_for_gtq = []
    for month, label in MONTH_LABELS:
        fx_obj = fx_by_month.get(month)
        fx_value = fx_obj.usd_to_gtq if fx_obj else None
        has_fx = fx_value not in (None, Decimal("0"), 0)
        if currency == MonthlyMetricResult.CURRENCY_GTQ and not has_fx:
            missing_fx_for_gtq.append(f"{year}-{month:02d}")

        cells = []
        for une in unes:
            obj = results_map.get((month, une.id))
            measured_usd = getattr(obj, "measured_value", None) if obj else None
            source_curr = (getattr(obj, "source_currency", "") or "") if obj else ""
            source_value = getattr(obj, "source_value", None) if obj else None

            if currency == MonthlyMetricResult.CURRENCY_GTQ:
                if source_curr == MonthlyMetricResult.CURRENCY_GTQ:
                    input_value = source_value
                else:
                    input_value = None
            else:
                input_value = measured_usd

            is_investment = (
                investment_une is not None and une.id == investment_une.id
            )
            cell = {
                "une": une,
                "obj": obj,
                "is_investment": is_investment,
                "value": (
                    format_currency_display(input_value)
                    if input_value is not None
                    else None
                ),
                "measured_usd": measured_usd,
                "measured_usd_display": format_usd_3(measured_usd) if measured_usd is not None else None,
                "source_currency": source_curr,
                "conversion_status": getattr(obj, "conversion_status", "") if obj else "",
                "input_disabled": (
                    currency == MonthlyMetricResult.CURRENCY_GTQ and not has_fx
                ),
            }
            if is_investment:
                cell["investment_audit"] = _build_investment_audit(
                    year,
                    month,
                    fx=fx_value,
                    currency=currency,
                    result_obj=obj,
                )
            cells.append(cell)

        month_rows.append({
            "month": month,
            "label": label,
            "fx_value": (
                format_currency_display(fx_value) if fx_value is not None else None
            ),
            "has_fx": has_fx,
            "cells": cells,
        })

    return {
        "year": year,
        "plan": plan,
        "unes": unes,
        "investment_une": investment_une,
        "month_rows": month_rows,
        "capture_currency": currency,
        "missing_fx_months": missing_fx_for_gtq,
        "label": str(year),
    }


@transaction.atomic
def save_ingresos_year(user, year: int, post_data, reason: str = "") -> dict:
    if not reason.strip():
        raise ValueError("Debe indicar un motivo para guardar ingresos del año.")

    plan = PGCPlan.objects.filter(year=year).first()
    if not plan:
        raise ValueError(f"No existe plan PGC para {year}.")

    metric = _ingresos_metric()
    if not metric:
        raise ValueError("No existe la métrica INGRESOS.")

    currency = _normalize_currency(post_data.get("capture_currency"))
    unes = _unes()

    # 1) Guardar TC de todos los meses primero (afecta conversión GTQ).
    fx_post = {f"fx_value_{m}": (post_data.get(f"fx_{m}") or "") for m in range(1, 13)}
    fx_changes = save_fx(
        user,
        year,
        12,
        fx_post,
        reason=reason or "TC desde matriz anual de ingresos",
        month_from=1,
    )

    income_changes = 0
    for month, _label in MONTH_LABELS:
        fx_rate = get_fx_rate(year, month)
        for une in unes:
            key = f"ing_{month}_{une.id}"
            raw = (post_data.get(key) or "").strip()
            if raw == "":
                continue
            parsed = parse_decimal_or_none(raw)
            if parsed is None:
                raise ValueError(
                    f"Valor inválido en {year}-{month:02d} / {une.name_es}."
                )

            if currency == MonthlyMetricResult.CURRENCY_USD:
                usd_value = parsed
                obj, created = MonthlyMetricResult.objects.get_or_create(
                    plan=plan,
                    une=une,
                    metric=metric,
                    year=year,
                    month=month,
                    defaults={
                        "measured_value": usd_value,
                        "source_currency": MonthlyMetricResult.CURRENCY_USD,
                        "source_value": usd_value,
                        "exchange_rate_used": None,
                        "conversion_status": MonthlyMetricResult.CONVERSION_NATIVE_USD,
                    },
                )
                old_usd = None if created else obj.measured_value
                old_curr = "" if created else (obj.source_currency or "")
                changed = (
                    created
                    or old_usd != usd_value
                    or old_curr != MonthlyMetricResult.CURRENCY_USD
                )
                if not changed:
                    continue
                obj.measured_value = usd_value
                obj.source_currency = MonthlyMetricResult.CURRENCY_USD
                obj.source_value = usd_value
                obj.exchange_rate_used = None
                obj.conversion_status = MonthlyMetricResult.CONVERSION_NATIVE_USD
                obj.calculation_note = (
                    f"Matriz anual USD: {usd_value} USD [{year}-{month:02d}]"
                )
                achievement_fields = apply_result_achievement(obj)
                obj.save(
                    update_fields=[
                        "measured_value",
                        "source_currency",
                        "source_value",
                        "exchange_rate_used",
                        "conversion_status",
                        "calculation_note",
                        *achievement_fields,
                        "updated_at",
                    ]
                )
                log_manual_edit(
                    user=user,
                    year=year,
                    month=month,
                    entity_type=AdminManualEditLog.ENTITY_RESULT,
                    entity_id=obj.id,
                    field_name="ingresos_year_usd",
                    old_value=f"USD={old_usd}; curr={old_curr}",
                    new_value=f"USD={usd_value}",
                    reason=reason,
                )
                income_changes += 1
                continue

            # GTQ → USD
            if fx_rate is None:
                raise ValueError(
                    f"Falta tipo de cambio para {year}-{month:02d}. "
                    f"No se puede convertir ingresos de {une.name_es} en Q. "
                    "Complete la columna TC de ese mes."
                )
            usd_value = gtq_to_usd(parsed, fx_rate)
            obj, created = MonthlyMetricResult.objects.get_or_create(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
                defaults={
                    "measured_value": usd_value,
                    "source_currency": MonthlyMetricResult.CURRENCY_GTQ,
                    "source_value": parsed,
                    "exchange_rate_used": fx_rate,
                    "conversion_status": MonthlyMetricResult.CONVERSION_CONVERTED,
                },
            )
            old_usd = None if created else obj.measured_value
            old_gtq = None if created else obj.source_value
            changed = (
                created
                or old_usd != usd_value
                or old_gtq != parsed
                or obj.source_currency != MonthlyMetricResult.CURRENCY_GTQ
                or obj.exchange_rate_used != fx_rate
            )
            if not changed:
                continue
            obj.measured_value = usd_value
            obj.source_currency = MonthlyMetricResult.CURRENCY_GTQ
            obj.source_value = parsed
            obj.exchange_rate_used = fx_rate
            obj.conversion_status = MonthlyMetricResult.CONVERSION_CONVERTED
            obj.calculation_note = (
                f"Matriz anual GTQ→USD: {parsed} GTQ / {fx_rate} = {usd_value} USD "
                f"[{year}-{month:02d}]"
            )
            achievement_fields = apply_result_achievement(obj)
            obj.save(
                update_fields=[
                    "measured_value",
                    "source_currency",
                    "source_value",
                    "exchange_rate_used",
                    "conversion_status",
                    "calculation_note",
                    *achievement_fields,
                    "updated_at",
                ]
            )
            log_manual_edit(
                user=user,
                year=year,
                month=month,
                entity_type=AdminManualEditLog.ENTITY_RESULT,
                entity_id=obj.id,
                field_name="ingresos_year_gtq",
                old_value=f"GTQ={old_gtq}; USD={old_usd}",
                new_value=f"GTQ={parsed}; FX={fx_rate}; USD={usd_value}",
                reason=reason,
            )
            income_changes += 1

    return {
        "fx_changes": fx_changes,
        "income_changes": income_changes,
        "changes": fx_changes + income_changes,
        "currency": currency,
    }
