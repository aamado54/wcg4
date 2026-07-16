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
        row.save(
            update_fields=[
                "measured_value",
                "exchange_rate_used",
                "conversion_status",
                "calculation_note",
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
