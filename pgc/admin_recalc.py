"""
Recálculo inteligente global: detecta pendientes en todos los períodos
y ejecuta la cadena en orden estricto.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from django.core.management import call_command
from django.db.models import Max
from django.utils import timezone

from core.models import MetricDefinition, UNE
from imports.models import CrossSaleImportRow, FileUpload, NewClientImportRow
from pgc.income_conversion import count_stale_ingresos, recalc_stale_ingresos
from pgc.models import (
    ManualRequirementsCompliance,
    MonthlyMetricResult,
    MonthlyModeScorecard,
    MonthlyTarget,
    PGCPlan,
)

MODES = ("modo1", "modo2")
INVESTMENT_CODES = ("INVESTMENT", "INVESTMENTS", "INVERSIONES")


def _aware(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


def _max_ts(*values: datetime | None) -> datetime | None:
    aware = [_aware(v) for v in values if v is not None]
    return max(aware) if aware else None


def iter_known_periods() -> list[tuple[int, int]]:
    """Todos los (año, mes) con presencia de datos PGC / imports."""
    periods: set[tuple[int, int]] = set()

    for year, month in MonthlyTarget.objects.values_list("year", "month").distinct():
        periods.add((year, month))
    for year, month in MonthlyMetricResult.objects.values_list("year", "month").distinct():
        periods.add((year, month))
    for year, month in NewClientImportRow.objects.values_list("year", "month").distinct():
        periods.add((year, month))
    for year, month in CrossSaleImportRow.objects.values_list("year", "month").distinct():
        periods.add((year, month))
    for year, month in ManualRequirementsCompliance.objects.values_list(
        "year", "month"
    ).distinct():
        periods.add((year, month))
    for year, month in MonthlyModeScorecard.objects.values_list("year", "month").distinct():
        periods.add((year, month))
    for year, month in (
        FileUpload.objects.exclude(detected_year__isnull=True)
        .exclude(detected_month__isnull=True)
        .values_list("detected_year", "detected_month")
        .distinct()
    ):
        periods.add((int(year), int(month)))

    # Años con plan: al menos asegurar meses donde haya plan, aunque vacíos
    # (no los agregamos vacíos — solo datos reales).
    return sorted(periods)


def _investment_une() -> UNE | None:
    return (
        UNE.objects.filter(code__in=INVESTMENT_CODES)
        .order_by("sort_order", "id")
        .first()
    )


def _ingresos_metric() -> MetricDefinition | None:
    return MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()


def _data_timestamp(year: int, month: int) -> datetime | None:
    """Última modificación de insumos que alimentan el score."""
    stamps: list[datetime | None] = []
    for model in (
        MonthlyTarget,
        MonthlyMetricResult,
        NewClientImportRow,
        CrossSaleImportRow,
        ManualRequirementsCompliance,
    ):
        stamps.append(
            model.objects.filter(year=year, month=month).aggregate(m=Max("updated_at"))["m"]
        )
    stamps.append(
        FileUpload.objects.filter(detected_year=year, detected_month=month).aggregate(
            m=Max("created_at")
        )["m"]
    )
    return _max_ts(*stamps)


def _score_timestamp(plan: PGCPlan | None, year: int, month: int) -> datetime | None:
    if not plan:
        return None
    stamps = []
    qs = MonthlyModeScorecard.objects.filter(plan=plan, year=year, month=month)
    for mode in MODES:
        stamps.append(qs.filter(mode=mode).aggregate(m=Max("updated_at"))["m"])
    return _max_ts(*stamps)


def _has_scoreable_data(year: int, month: int) -> bool:
    return (
        MonthlyTarget.objects.filter(year=year, month=month).exists()
        or MonthlyMetricResult.objects.filter(year=year, month=month).exists()
        or NewClientImportRow.objects.filter(year=year, month=month).exists()
        or CrossSaleImportRow.objects.filter(year=year, month=month).exists()
        or ManualRequirementsCompliance.objects.filter(year=year, month=month).exists()
    )


def _score_complete(plan: PGCPlan | None, year: int, month: int) -> bool:
    if not plan:
        return False
    une_count = UNE.objects.filter(is_active=True).count()
    if une_count == 0:
        return False
    for mode in MODES:
        n = MonthlyModeScorecard.objects.filter(
            plan=plan, year=year, month=month, mode=mode
        ).count()
        if n < une_count:
            return False
    return True


def period_pending_reasons(year: int, month: int) -> list[str]:
    """Razones por las que el período necesita la cadena de recálculo."""
    reasons: list[str] = []
    plan = PGCPlan.objects.filter(year=year).first()
    label = f"{year}-{month:02d}"

    stale = count_stale_ingresos(year, month)
    if stale:
        reasons.append(f"{stale} ingreso(s) con TC desactualizado (STALE)")

    inv_une = _investment_une()
    metric = _ingresos_metric()
    if inv_une and NewClientImportRow.objects.filter(
        year=year, month=month, une=inv_une
    ).exists():
        latest_row_ts = NewClientImportRow.objects.filter(
            year=year, month=month, une=inv_une
        ).aggregate(m=Max("updated_at"))["m"]
        result = None
        if plan and metric:
            result = MonthlyMetricResult.objects.filter(
                plan=plan,
                metric=metric,
                une=inv_une,
                year=year,
                month=month,
            ).first()
        if result is None or result.measured_value is None:
            reasons.append("Ingresos Investment sin calcular desde clientes")
        elif latest_row_ts and result.updated_at and _aware(result.updated_at) < _aware(
            latest_row_ts
        ):
            reasons.append("Ingresos Investment desactualizados vs clientes")

    if _has_scoreable_data(year, month):
        if not plan:
            reasons.append(f"Sin plan PGC para {year} (no se puede scorear)")
        elif not _score_complete(plan, year, month):
            reasons.append("Score PGC incompleto (modo1/modo2)")
        else:
            data_ts = _data_timestamp(year, month)
            score_ts = _score_timestamp(plan, year, month)
            if data_ts and score_ts and score_ts < data_ts:
                reasons.append("Score desactualizado respecto a los datos")
            elif data_ts and not score_ts:
                reasons.append(f"Sin score para {label}")

    return reasons


def get_global_recalc_status() -> dict[str, Any]:
    pending_periods: list[dict[str, Any]] = []
    for year, month in iter_known_periods():
        reasons = period_pending_reasons(year, month)
        if reasons:
            pending_periods.append(
                {
                    "year": year,
                    "month": month,
                    "label": f"{year}-{month:02d}",
                    "reasons": reasons,
                }
            )

    pending_count = len(pending_periods)
    is_pending = pending_count > 0
    return {
        "is_pending": is_pending,
        "is_ready": not is_pending,
        "pending_count": pending_count,
        "pending_periods": pending_periods,
        "state": "pending" if is_pending else "ready",
        "state_label": (
            f"Pendiente · {pending_count} período(s)"
            if is_pending
            else "Al día · sin pendientes"
        ),
        "button_label": (
            f"△ Recalcular pendientes ({pending_count})"
            if is_pending
            else "✓ Recalcular (todo al día)"
        ),
        "button_hint": (
            "Hay cálculos faltantes o desactualizados en uno o más períodos."
            if is_pending
            else "No hay pendientes. Puede ejecutar de todos modos si quiere forzar revisión."
        ),
    }


def run_period_recalc_chain(
    year: int,
    month: int,
    *,
    user=None,
    force: bool = False,
) -> list[str]:
    """
    Orden estricto por período:
    1) Ingresos STALE GTQ→USD
    2) Ingresos Investment desde clientes nuevos
    3) Score PGC modo1 + modo2
    """
    messages_out: list[str] = []
    label = f"{year}-{month:02d}"

    try:
        stale_result = recalc_stale_ingresos(
            year=year,
            month=month,
            user=user,
            reason=f"Recálculo inteligente {label}",
            only_stale=True,
        )
        if stale_result["updated"]:
            messages_out.append(
                f"{label}: {stale_result['updated']} ingreso(s) STALE → USD "
                f"(TC={stale_result['fx']})."
            )
    except ValueError as exc:
        # Sin TC: no bloquear el resto; avisar.
        if count_stale_ingresos(year, month):
            messages_out.append(f"{label}: STALE no convertido — {exc}")

    has_clients = NewClientImportRow.objects.filter(year=year, month=month).exists()
    if has_clients or force:
        call_command(
            "recalc_investment_ingresos_from_new_clients", year=year, month=month
        )
        messages_out.append(f"{label}: ingresos Investment recalculados.")

    if _has_scoreable_data(year, month) or force or has_clients:
        for mode in MODES:
            call_command("recalc_pgc", year=year, month=month, mode=mode)
        messages_out.append(f"{label}: score PGC (modo1 y modo2) recalculado.")

    if not messages_out:
        messages_out.append(f"{label}: sin operaciones aplicables.")
    return messages_out


def run_smart_recalc_all(*, user=None, force_all: bool = False) -> dict[str, Any]:
    """
    Si hay pendientes: recalcula solo esos períodos (en orden cronológico).
    Si no hay pendientes y force_all=False: no-op informativo.
    Si force_all=True: corre la cadena en todos los períodos conocidos.
    """
    status_before = get_global_recalc_status()
    if force_all:
        targets = [
            {"year": y, "month": m, "label": f"{y}-{m:02d}", "reasons": ["forzado"]}
            for y, m in iter_known_periods()
        ]
    else:
        targets = list(status_before["pending_periods"])

    if not targets:
        return {
            "ran": False,
            "periods_processed": 0,
            "messages": ["Nada pendiente de calcular. Todo al día."],
            "status_before": status_before,
            "status_after": status_before,
        }

    messages: list[str] = []
    for item in targets:
        year, month = item["year"], item["month"]
        try:
            messages.extend(
                run_period_recalc_chain(year, month, user=user, force=force_all)
            )
        except Exception as exc:  # keep going across periods
            messages.append(f"{item['label']}: error — {exc}")

    status_after = get_global_recalc_status()
    return {
        "ran": True,
        "periods_processed": len(targets),
        "messages": messages,
        "status_before": status_before,
        "status_after": status_after,
    }
