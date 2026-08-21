"""Conversión y recálculo de ingresos (GTQ → USD canónico)."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction

from core.models import MetricDefinition
from pgc.models import AdminManualEditLog, MonthlyExchangeRate, MonthlyMetricResult


USD_DISPLAY_PLACES = Decimal("0.001")
USD_STORE_PLACES = Decimal("0.000001")


def get_fx_rate(year: int, month: int) -> Decimal | None:
    fx = MonthlyExchangeRate.objects.filter(year=year, month=month).first()
    if not fx or fx.usd_to_gtq in (None, Decimal("0")):
        return None
    return fx.usd_to_gtq


def gtq_to_usd(gtq: Decimal, usd_to_gtq: Decimal) -> Decimal:
    """1 USD = usd_to_gtq GTQ ⇒ USD = GTQ / usd_to_gtq."""
    if usd_to_gtq <= 0:
        raise ValueError("Tipo de cambio inválido.")
    return (gtq / usd_to_gtq).quantize(USD_STORE_PLACES, rounding=ROUND_HALF_UP)


def format_usd_3(value: Decimal | None) -> str:
    if value is None:
        return ""
    return str(value.quantize(USD_DISPLAY_PLACES, rounding=ROUND_HALF_UP))


def evaluate_result_achievement(
    measured_value,
    target_value,
    *,
    points_if_achieved: int = 0,
) -> tuple[bool, int]:
    """Regla PGC modo1 para Cumple: real >= meta → Sí + puntos; si no, No + 0."""
    if measured_value is None or target_value is None:
        return False, 0
    try:
        measured = Decimal(str(measured_value))
        target = Decimal(str(target_value))
    except Exception:
        return False, 0
    achieved = measured >= target
    points = int(points_if_achieved or 0) if achieved else 0
    return achieved, points


def apply_result_achievement(result: MonthlyMetricResult, target=None) -> list[str]:
    """
    Sincroniza is_achieved / points_awarded / target_value en MonthlyMetricResult.

    Returns:
        Lista de campos modificados (para update_fields).
    """
    from pgc.models import MonthlyTarget

    if target is None:
        target = (
            MonthlyTarget.objects.filter(
                plan_id=result.plan_id,
                une_id=result.une_id,
                metric_id=result.metric_id,
                year=result.year,
                month=result.month,
            ).first()
        )

    meta = None
    points_if = 0
    if target is not None:
        meta = target.target_value
        points_if = int(target.points_if_achieved or 0)
    elif result.target_value is not None:
        meta = result.target_value

    achieved, points = evaluate_result_achievement(
        result.measured_value,
        meta,
        points_if_achieved=points_if,
    )

    changed: list[str] = []
    if meta is not None and result.target_value != meta:
        result.target_value = meta
        changed.append("target_value")
    if bool(result.is_achieved) != achieved:
        result.is_achieved = achieved
        changed.append("is_achieved")
    if int(result.points_awarded or 0) != points:
        result.points_awarded = points
        changed.append("points_awarded")
    return changed


def sync_ingresos_achievements(*, year: int | None = None) -> dict:
    """Repara Cumple/puntos de todos los MonthlyMetricResult de INGRESOS."""
    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
    if not metric:
        return {"updated": 0, "checked": 0}

    qs = MonthlyMetricResult.objects.filter(metric=metric).select_related("une")
    if year is not None:
        qs = qs.filter(year=year)

    checked = 0
    updated = 0
    mismatches = []
    for row in qs.iterator():
        checked += 1
        before = (row.is_achieved, int(row.points_awarded or 0), row.target_value)
        fields = apply_result_achievement(row)
        if not fields:
            continue
        row.save(update_fields=fields + ["updated_at"])
        updated += 1
        mismatches.append(
            {
                "une": row.une.code if row.une_id else "?",
                "period": f"{row.year}-{row.month:02d}",
                "measured": row.measured_value,
                "before": before,
                "after": (row.is_achieved, int(row.points_awarded or 0), row.target_value),
            }
        )
    return {"updated": updated, "checked": checked, "mismatches": mismatches}


def _log_edit(*, user, year, month, entity_id, field_name, old_value, new_value, reason):
    if user is None:
        return
    from pgc.admin_utils import format_value

    AdminManualEditLog.objects.create(
        year=year,
        month=month,
        entity_type=AdminManualEditLog.ENTITY_RESULT,
        entity_id=entity_id,
        field_name=field_name,
        old_value=format_value(old_value),
        new_value=format_value(new_value),
        reason=reason or "",
        edited_by=user,
    )


def mark_ingresos_stale_for_fx_change(
    *,
    year: int,
    month: int,
    old_fx,
    new_fx,
    user=None,
    reason: str = "",
) -> int:
    """Marca INGRESOS convertidos del mes como STALE_FX (no recalcula USD)."""
    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
    if not metric:
        return 0

    qs = MonthlyMetricResult.objects.filter(
        year=year,
        month=month,
        metric=metric,
        source_currency=MonthlyMetricResult.CURRENCY_GTQ,
        source_value__isnull=False,
    ).exclude(conversion_status=MonthlyMetricResult.CONVERSION_STALE_FX)

    marked = 0
    for row in qs:
        old_status = row.conversion_status
        row.conversion_status = MonthlyMetricResult.CONVERSION_STALE_FX
        note = (
            f"[TC cambió {old_fx} → {new_fx}; USD previo={row.measured_value}; "
            f"GTQ origen={row.source_value}]"
        )
        row.calculation_note = ((row.calculation_note or "") + " " + note).strip()
        row.save(update_fields=["conversion_status", "calculation_note", "updated_at"])
        _log_edit(
            user=user,
            year=year,
            month=month,
            entity_id=row.id,
            field_name="conversion_status",
            old_value=old_status or "",
            new_value=MonthlyMetricResult.CONVERSION_STALE_FX,
            reason=reason
            or f"TC actualizado {old_fx} → {new_fx}; ingresos pendientes de recálculo",
        )
        marked += 1
    return marked


@transaction.atomic
def recalc_stale_ingresos(
    *,
    year: int,
    month: int,
    user=None,
    reason: str = "",
    only_stale: bool = True,
) -> dict:
    """
    Recalcula USD desde source_value GTQ usando el FX actual del mes.
    Por defecto solo filas con conversion_status=STALE_FX.
    """
    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
    if not metric:
        raise ValueError("No existe métrica INGRESOS.")

    fx = get_fx_rate(year, month)
    if fx is None:
        raise ValueError(
            f"Falta tipo de cambio para {year}-{month:02d}. "
            "Defínalo antes de recalcular ingresos."
        )

    qs = MonthlyMetricResult.objects.filter(
        year=year,
        month=month,
        metric=metric,
        source_currency=MonthlyMetricResult.CURRENCY_GTQ,
        source_value__isnull=False,
    )
    if only_stale:
        qs = qs.filter(conversion_status=MonthlyMetricResult.CONVERSION_STALE_FX)

    updated = 0
    for row in qs:
        old_usd = row.measured_value
        old_fx = row.exchange_rate_used
        new_usd = gtq_to_usd(row.source_value, fx)
        row.measured_value = new_usd
        row.exchange_rate_used = fx
        row.conversion_status = MonthlyMetricResult.CONVERSION_CONVERTED
        row.calculation_note = (
            (row.calculation_note or "")
            + f" [Recalc GTQ→USD: {row.source_value} GTQ / {fx} = {new_usd} USD; "
            f"prev USD={old_usd}, prev FX={old_fx}]"
        ).strip()
        achievement_fields = apply_result_achievement(row)
        row.save(
            update_fields=[
                "measured_value",
                "exchange_rate_used",
                "conversion_status",
                "calculation_note",
                *achievement_fields,
                "updated_at",
            ]
        )
        _log_edit(
            user=user,
            year=year,
            month=month,
            entity_id=row.id,
            field_name="measured_value/exchange_rate_used",
            old_value=f"USD={old_usd}; FX={old_fx}",
            new_value=f"USD={new_usd}; FX={fx}; GTQ={row.source_value}",
            reason=reason or "Recálculo de ingresos tras cambio de TC",
        )
        updated += 1

    return {"updated": updated, "fx": fx}


def count_stale_ingresos(year: int, month: int) -> int:
    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
    if not metric:
        return 0
    return MonthlyMetricResult.objects.filter(
        year=year,
        month=month,
        metric=metric,
        conversion_status=MonthlyMetricResult.CONVERSION_STALE_FX,
    ).count()
