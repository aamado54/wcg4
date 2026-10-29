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


def gtq_comisiones_to_usd_miles(gtq: Decimal, usd_to_gtq: Decimal) -> Decimal:
    """Comisiones en GTQ → miles USD (convención PGC tablero / metas TSV)."""
    if not gtq or not usd_to_gtq or usd_to_gtq <= 0:
        return Decimal("0")
    return ((gtq / Decimal("1000")) / usd_to_gtq).quantize(
        USD_STORE_PLACES, rounding=ROUND_HALF_UP
    )


LEGACY_INGRESOS_MILES_TOLERANCE = Decimal("0.05")


def _source_stored_as_gtq_over_fx(
    source_stored: Decimal, measured_miles: Decimal | None, fx: Decimal
) -> bool:
    """True si source_value parece GTQ/FX (no GTQ canónico mensual completo)."""
    if measured_miles is None or not source_stored or not fx or fx <= 0:
        return False
    semi_legacy_miles = (source_stored / Decimal("1000")).quantize(
        USD_STORE_PLACES, rounding=ROUND_HALF_UP
    )
    canonical_gtq = (source_stored * fx).quantize(
        USD_STORE_PLACES, rounding=ROUND_HALF_UP
    )
    expected = gtq_comisiones_to_usd_miles(canonical_gtq, fx)
    if abs(expected - semi_legacy_miles) > LEGACY_INGRESOS_MILES_TOLERANCE:
        return False
    # GTQ canónico mensual (factoraje) en source_value supera esto; no es GTQ/FX.
    if source_stored >= Decimal("250000"):
        return False
    return True


def ingresos_has_extra_fx_on_gtq_over_fx_source(
    source_stored: Decimal,
    measured_miles: Decimal | None,
    fx: Decimal,
) -> bool:
    """Repair previo dejó source=GTQ/FX y measured=(GTQ/FX)/1000/FX (÷FX de más)."""
    if measured_miles is None or not source_stored or not fx or fx <= 0:
        return False
    if not _source_stored_as_gtq_over_fx(source_stored, measured_miles, fx):
        return False
    wrong_miles = gtq_comisiones_to_usd_miles(source_stored, fx)
    if abs(measured_miles - wrong_miles) > LEGACY_INGRESOS_MILES_TOLERANCE:
        return False
    semi_legacy_miles = (source_stored / Decimal("1000")).quantize(
        USD_STORE_PLACES, rounding=ROUND_HALF_UP
    )
    return abs(measured_miles - semi_legacy_miles) > LEGACY_INGRESOS_MILES_TOLERANCE


def ingresos_has_legacy_double_fx_bug(
    source_gtq: Decimal,
    measured_miles: Decimal | None,
    fx: Decimal,
) -> bool:
    """
    Import PGA antiguo guardaba source≈GTQ/FX y measured con un ÷FX de más.

    En ese caso el GTQ real = source × FX y miles correctos = (GTQ/1000)/FX = source/1000.
    """
    if measured_miles is None or not source_gtq or not fx or fx <= 0:
        return False
    legacy_miles = (source_gtq / Decimal("1000")) / (fx * fx)
    return abs(measured_miles - legacy_miles) <= LEGACY_INGRESOS_MILES_TOLERANCE


def measured_matches_gtq_comisiones(
    source_gtq: Decimal,
    measured_miles: Decimal | None,
    fx: Decimal,
) -> bool:
    if measured_miles is None or not source_gtq or not fx or fx <= 0:
        return False
    expected = gtq_comisiones_to_usd_miles(source_gtq, fx)
    return abs(measured_miles - expected) <= LEGACY_INGRESOS_MILES_TOLERANCE


def ingresos_has_gtq_over_fx_source_with_correct_miles(
    source_stored: Decimal,
    measured_miles: Decimal | None,
    fx: Decimal,
) -> bool:
    """
    Convención intermedia PGA: source_value = GTQ/FX, measured_value = source/1000 (miles USD).

    Es correcto en pantalla pero el GTQ canónico falta en source. No debe recalcularse
    measured como (GTQ/FX)/1000/FX (un ÷FX de más → totales ~670 vs ~11000).
    """
    if measured_miles is None or not source_stored or not fx or fx <= 0:
        return False
    miles_from_stored_source = (source_stored / Decimal("1000")).quantize(
        USD_STORE_PLACES, rounding=ROUND_HALF_UP
    )
    if abs(measured_miles - miles_from_stored_source) > LEGACY_INGRESOS_MILES_TOLERANCE:
        return False
    if measured_matches_gtq_comisiones(source_stored, measured_miles, fx):
        return False
    return True


def format_currency_display(
    value: Decimal | None, *, max_decimal_places: int = 3
) -> str:
    """Coma miles, punto decimal, hasta N decimales sin ceros finales (matriz admin)."""
    from core.number_format import format_wcg_amount

    if value is None:
        return ""
    return format_wcg_amount(value, max_decimal_places=max_decimal_places)


def format_usd_3(value: Decimal | None) -> str:
    return format_currency_display(value, max_decimal_places=3)


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
        new_usd = gtq_comisiones_to_usd_miles(row.source_value, fx)
        row.measured_value = new_usd
        row.exchange_rate_used = fx
        row.conversion_status = MonthlyMetricResult.CONVERSION_CONVERTED
        row.calculation_note = (
            (row.calculation_note or "")
            + f" [Recalc GTQ→USD miles: {row.source_value} GTQ / {fx} → {new_usd} miles; "
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


@transaction.atomic
def repair_ingresos_gtq_and_usd_miles(
    *,
    year: int | None = None,
    month: int | None = None,
    dry_run: bool = False,
) -> dict:
    """
    Normaliza INGRESOS GTQ en BD (comisiones en Q) y recalcula measured_value (miles USD).

    - GTQ canónico en ``source_value`` (no se divide por TC al guardar).
    - Miles USD = (GTQ/1000)/FX usando TC del mes (``exchange_rate_used`` o tabla FX).
    - Filas con bug histórico (source guardado como GTQ/FX): restaura GTQ = source×FX.
    """
    from pgc.models import MonthlyMetricResult

    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
    if not metric:
        raise ValueError("No existe métrica INGRESOS.")

    qs = MonthlyMetricResult.objects.filter(metric=metric).select_related("une", "plan")
    if year is not None:
        qs = qs.filter(year=year)
    if month is not None:
        qs = qs.filter(month=month)

    stats = {
        "scanned": 0,
        "skipped_usd": 0,
        "skipped_ok": 0,
        "skipped_no_fx": 0,
        "repaired_legacy": 0,
        "repaired_measured": 0,
        "dry_run": dry_run,
    }

    for row in qs.iterator():
        stats["scanned"] += 1
        if row.source_currency == MonthlyMetricResult.CURRENCY_USD:
            stats["skipped_usd"] += 1
            continue
        if row.source_currency != MonthlyMetricResult.CURRENCY_GTQ or row.source_value is None:
            stats["skipped_ok"] += 1
            continue

        fx = row.exchange_rate_used or get_fx_rate(row.year, row.month)
        if fx is None or fx <= 0:
            stats["skipped_no_fx"] += 1
            continue

        source_gtq = Decimal(str(row.source_value))
        legacy = ingresos_has_legacy_double_fx_bug(
            source_gtq, row.measured_value, fx
        )
        semi_legacy_source = ingresos_has_gtq_over_fx_source_with_correct_miles(
            source_gtq, row.measured_value, fx
        )
        extra_fx_source = ingresos_has_extra_fx_on_gtq_over_fx_source(
            source_gtq, row.measured_value, fx
        )
        if legacy:
            source_gtq = (source_gtq * fx).quantize(
                USD_STORE_PLACES, rounding=ROUND_HALF_UP
            )
        elif semi_legacy_source or extra_fx_source:
            source_gtq = (source_gtq * fx).quantize(
                USD_STORE_PLACES, rounding=ROUND_HALF_UP
            )
        elif measured_matches_gtq_comisiones(source_gtq, row.measured_value, fx):
            stats["skipped_ok"] += 1
            continue

        if semi_legacy_source:
            new_measured = row.measured_value
        else:
            new_measured = gtq_comisiones_to_usd_miles(source_gtq, fx)
        if dry_run:
            if legacy or semi_legacy_source or extra_fx_source:
                stats["repaired_legacy"] += 1
            else:
                stats["repaired_measured"] += 1
            continue

        old_source = row.source_value
        old_measured = row.measured_value
        row.source_value = source_gtq
        row.measured_value = new_measured
        row.exchange_rate_used = fx
        row.conversion_status = MonthlyMetricResult.CONVERSION_CONVERTED
        if legacy:
            tag = "legacy GTQ/FX→GTQ"
        elif semi_legacy_source:
            tag = "GTQ/FX source→GTQ canónico (miles OK)"
        elif extra_fx_source:
            tag = "GTQ/FX source→GTQ; miles ÷FX extra corregidos"
        else:
            tag = "miles desde GTQ"
        row.calculation_note = (
            (row.calculation_note or "").strip()
            + f" [Repair {tag}: GTQ {old_source}→{source_gtq}, "
            f"miles {old_measured}→{new_measured}, FX={fx}]"
        ).strip()
        achievement_fields = apply_result_achievement(row)
        row.save(
            update_fields=[
                "source_value",
                "measured_value",
                "exchange_rate_used",
                "conversion_status",
                "calculation_note",
                *achievement_fields,
                "updated_at",
            ]
        )
        if legacy or semi_legacy_source or extra_fx_source:
            stats["repaired_legacy"] += 1
        else:
            stats["repaired_measured"] += 1

    return stats


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


def audit_ingresos_fx_findings(
    *,
    year: int | None = None,
    month: int | None = None,
    sample_limit: int = 15,
) -> dict:
    """
    Detecta filas INGRESOS GTQ con doble FX, miles incoherentes o TC STALE.

    Usar en cierre mensual / certificación (exit code ≠ 0 si ``pass`` es False).
    """
    from pgc.models import MonthlyMetricResult

    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
    if not metric:
        return {
            "pass": True,
            "counts": {},
            "samples": [],
            "repair_dry_run": {},
            "message": "Sin métrica INGRESOS.",
        }

    qs = MonthlyMetricResult.objects.filter(metric=metric).select_related("une", "plan")
    if year is not None:
        qs = qs.filter(year=year)
    if month is not None:
        qs = qs.filter(month=month)

    counts = {
        "scanned": 0,
        "ok": 0,
        "usd_native": 0,
        "no_fx": 0,
        "stale_fx": 0,
        "legacy_double_fx": 0,
        "extra_fx_division": 0,
        "semi_legacy_source": 0,
        "measured_mismatch": 0,
    }
    samples: list[dict] = []

    def _sample(issue: str, row, **extra):
        if len(samples) >= sample_limit:
            return
        samples.append(
            {
                "issue": issue,
                "period": f"{row.year}-{row.month:02d}",
                "une": row.une.code,
                "measured": row.measured_value,
                "source": row.source_value,
                "fx": row.exchange_rate_used,
                **extra,
            }
        )

    for row in qs.iterator():
        counts["scanned"] += 1
        if row.conversion_status == MonthlyMetricResult.CONVERSION_STALE_FX:
            counts["stale_fx"] += 1
            _sample("stale_fx", row)

        if row.source_currency == MonthlyMetricResult.CURRENCY_USD:
            counts["usd_native"] += 1
            continue
        if row.source_currency != MonthlyMetricResult.CURRENCY_GTQ or row.source_value is None:
            counts["ok"] += 1
            continue

        fx = row.exchange_rate_used or get_fx_rate(row.year, row.month)
        if fx is None or fx <= 0:
            counts["no_fx"] += 1
            _sample("no_fx", row)
            continue

        source_stored = Decimal(str(row.source_value))
        measured = row.measured_value

        if ingresos_has_legacy_double_fx_bug(source_stored, measured, fx):
            counts["legacy_double_fx"] += 1
            _sample("legacy_double_fx", row)
            continue
        if ingresos_has_extra_fx_on_gtq_over_fx_source(source_stored, measured, fx):
            counts["extra_fx_division"] += 1
            _sample("extra_fx_division", row)
            continue
        if ingresos_has_gtq_over_fx_source_with_correct_miles(source_stored, measured, fx):
            counts["semi_legacy_source"] += 1
            _sample("semi_legacy_source", row)
            continue

        source_gtq = source_stored
        if measured_matches_gtq_comisiones(source_gtq, measured, fx):
            counts["ok"] += 1
            continue

        counts["measured_mismatch"] += 1
        expected = gtq_comisiones_to_usd_miles(source_gtq, fx)
        _sample("measured_mismatch", row, expected=expected)

    repair_dry = repair_ingresos_gtq_and_usd_miles(
        year=year, month=month, dry_run=True
    )
    fail_count = (
        counts["legacy_double_fx"]
        + counts["extra_fx_division"]
        + counts["measured_mismatch"]
        + counts["semi_legacy_source"]
        + counts["stale_fx"]
        + counts["no_fx"]
    )
    needs_repair = (repair_dry.get("repaired_legacy") or 0) + (
        repair_dry.get("repaired_measured") or 0
    )
    passed = fail_count == 0 and needs_repair == 0

    return {
        "pass": passed,
        "counts": counts,
        "samples": samples,
        "repair_dry_run": repair_dry,
        "needs_repair": needs_repair,
        "fail_count": fail_count,
    }
