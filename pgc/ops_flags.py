"""Banderas operativas PGC: sincronía Objetivos, score modo2 y recálculo."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from django.db.models import Max, Q
from django.utils import timezone

from core.models import MetricDefinition
from imports.models import CrossSaleImportHeader
from pgc.admin_utils import AdminPeriod
from pgc.models import (
    ManualRequirementsCompliance,
    MonthlyMetricResult,
    MonthlyMetricScore,
    MonthlyTarget,
    PGCMode,
    PGCPlan,
)

OBJETIVOS_IMPORT_NOTE = Q(calculation_note__icontains="Importado desde") & Q(
    calculation_note__icontains="Objetivos"
)

DOCS_CIERRE_MENSUAL = "docs/pgc-cierre-mensual-operacion.md"
VALIDATE_CLI = (
    "python tools/pgc/validate_ejecucion_excel.py <archivo.xlsx> --year AÑO"
)


@dataclass(frozen=True)
class OpsFlag:
    code: str
    level: str
    title: str
    message: str
    fix: str
    year: int | None = None
    month: int | None = None

    def as_dict(self) -> dict[str, Any]:
        label = None
        if self.year is not None and self.month is not None:
            label = f"{self.year}-{self.month:02d}"
        return {
            "code": self.code,
            "level": self.level,
            "title": self.title,
            "message": self.message,
            "fix": self.fix,
            "year": self.year,
            "month": self.month,
            "label": label,
        }


def plan_for_year(year: int) -> PGCPlan | None:
    return PGCPlan.objects.filter(year=year).first()


def _ingresos_metric_id() -> int | None:
    row = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
    return row.id if row else None


def _venta_cruzada_metric_id() -> int | None:
    row = MetricDefinition.objects.filter(
        code=MetricDefinition.CODE_VENTA_CRUZADA
    ).first()
    return row.id if row else None


def _aware(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


def objetivos_import_updated_at(
    plan: PGCPlan, year: int, month: int
) -> datetime | None:
    agg = (
        MonthlyMetricResult.objects.filter(
            plan=plan, year=year, month=month
        )
        .filter(OBJETIVOS_IMPORT_NOTE)
        .aggregate(latest=Max("updated_at"))
    )
    return agg.get("latest")


def has_objetivos_import(plan: PGCPlan, year: int, month: int) -> bool:
    return objetivos_import_updated_at(plan, year, month) is not None


def ingresos_targets_missing_presupuesto_gtq(
    plan: PGCPlan, year: int, month: int, metric_id: int
) -> list[str]:
    rows = MonthlyTarget.objects.filter(
        plan=plan,
        metric_id=metric_id,
        year=year,
        month=month,
    ).select_related("une")
    missing = [t.une.code for t in rows if t.presupuesto_gtq is None]
    return missing


def modo2_score_updated_at(plan: PGCPlan, year: int, month: int) -> datetime | None:
    agg = MonthlyMetricScore.objects.filter(
        plan=plan,
        year=year,
        month=month,
        mode=PGCMode.MODO2,
    ).aggregate(latest=Max("updated_at"))
    return agg.get("latest")


def collect_ops_flags(
    year: int,
    month: int,
    *,
    plan: PGCPlan | None = None,
    recalc_status: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    flags: list[OpsFlag] = []
    plan = plan or plan_for_year(year)
    metric_id = _ingresos_metric_id()

    if plan and metric_id:
        targets_exist = MonthlyTarget.objects.filter(
            plan=plan, metric_id=metric_id, year=year, month=month
        ).exists()
        if targets_exist:
            missing_une = ingresos_targets_missing_presupuesto_gtq(
                plan, year, month, metric_id
            )
            imported = has_objetivos_import(plan, year, month)
            if not imported or missing_une:
                parts = []
                if not imported:
                    parts.append(
                        "no hay resultados con nota «Importado desde … Objetivos»"
                    )
                if missing_une:
                    parts.append(
                        "falta presupuesto GTQ (presupuesto_gtq) en ingresos para: "
                        + ", ".join(missing_une)
                    )
                flags.append(
                    OpsFlag(
                        code="objetivos_sync",
                        level="warn",
                        title="Mes sin sincronía completa con Objetivos",
                        message=" ".join(parts).capitalize() + ".",
                        fix=(
                            "Ejecute `python manage.py import_pgc_objetivos <archivo.xlsx> "
                            f"--year {year} --month {month:02d}` (o import_pgc_objetivos_tsv) "
                            "y confirme presupuesto GTQ en metas de ingresos. "
                            f"Luego recalcule el período. Guía: {DOCS_CIERRE_MENSUAL}."
                        ),
                        year=year,
                        month=month,
                    )
                )

            import_ts = _aware(objetivos_import_updated_at(plan, year, month))
            modo2_ts = _aware(modo2_score_updated_at(plan, year, month))
            if import_ts and modo2_ts and modo2_ts < import_ts:
                flags.append(
                    OpsFlag(
                        code="modo2_stale_objetivos",
                        level="warn",
                        title="Score modo2 anterior al último import Objetivos",
                        message=(
                            "Los puntos 2.Proporción (modo2) no se han recalculado "
                            "después del último import desde la hoja Objetivos."
                        ),
                        fix=(
                            "En el tablero mensual use «Recalcular período» o el recálculo "
                            "inteligente global. Valide con "
                            f"`{VALIDATE_CLI}`. Ver {DOCS_CIERRE_MENSUAL}#validacion-excel."
                        ),
                        year=year,
                        month=month,
                    )
                )
            elif import_ts and modo2_ts is None:
                flags.append(
                    OpsFlag(
                        code="modo2_stale_objetivos",
                        level="warn",
                        title="Sin score modo2 tras import Objetivos",
                        message=(
                            "Hay datos importados desde Objetivos pero no hay filas de "
                            "score modo2 para este mes."
                        ),
                        fix=(
                            "Recalcule el período desde el tablero mensual (bloque revisión). "
                            f"Documentación: {DOCS_CIERRE_MENSUAL}."
                        ),
                        year=year,
                        month=month,
                    )
                )

    if plan:
        vc_metric_id = _venta_cruzada_metric_id()
        if vc_metric_id:
            vc_positive = MonthlyMetricResult.objects.filter(
                plan=plan,
                metric_id=vc_metric_id,
                year=year,
                month=month,
                measured_value__gt=0,
            ).exists()
            has_cross_sale = CrossSaleImportHeader.objects.filter(
                year=year, month=month
            ).exists()
            if vc_positive and not has_cross_sale:
                flags.append(
                    OpsFlag(
                        code="vc_without_operational_import",
                        level="warn",
                        title="Venta cruzada sin carga operativa",
                        message=(
                            "Hay ejecución VENTA_CRUZADA > 0 pero no existe "
                            "CrossSaleImportHeader para este mes (política: VC=0 "
                            "sin ventas cruzadas reales)."
                        ),
                        fix=(
                            "Revise MonthlyMetricResult de VC o ejecute "
                            "`clear_operational_fiction_from_objetivos` si son "
                            "datos heredados de Excel Objetivos. Cargas reales: "
                            "tablero mensual / import_venta_cruzada."
                        ),
                        year=year,
                        month=month,
                    )
                )

        excel_reqs = ManualRequirementsCompliance.objects.filter(
            plan=plan,
            year=year,
            month=month,
            incident_note__icontains="Excel Objetivos",
        )
        if excel_reqs.exists():
            flags.append(
                OpsFlag(
                    code="reqs_from_excel_objetivos",
                    level="warn",
                    title="Requerimientos sincronizados desde Excel",
                    message=(
                        "Existen registros ManualRequirementsCompliance con nota "
                        "«Excel Objetivos»; los reqs no se reportan vía Objetivos."
                    ),
                    fix=(
                        "Elimine esos MRC o use la matriz anual de requerimientos. "
                        "Limpieza masiva: "
                        "`python manage.py clear_operational_fiction_from_objetivos "
                        f"--year {year} --months {month}`."
                    ),
                    year=year,
                    month=month,
                )
            )

    if recalc_status and recalc_status.get("is_pending"):
        label = f"{year}-{month:02d}"
        pending = recalc_status.get("pending_periods") or []
        match = next((p for p in pending if p.get("label") == label), None)
        if match:
            reasons = "; ".join(match.get("reasons") or [])
            flags.append(
                OpsFlag(
                    code="recalc_pending",
                    level="warn",
                    title="Recálculo pendiente en este período",
                    message=reasons or "Hay cálculos desactualizados o incompletos.",
                    fix=(
                        "Corrija la causa (TC, ingresos STALE, cargas, etc.) y ejecute "
                        "recálculo desde el tablero mensual. Detalle en "
                        f"{DOCS_CIERRE_MENSUAL}#recalculo."
                    ),
                    year=year,
                    month=month,
                )
            )

    return [f.as_dict() for f in flags]


def collect_ops_flags_for_period(
    period: AdminPeriod,
    *,
    recalc_status: dict[str, Any] | None = None,
    include_validate_hint: bool = True,
) -> list[dict[str, Any]]:
    plan = plan_for_year(period.year)
    seen: set[tuple[str, str | None]] = set()
    out: list[dict[str, Any]] = []
    months = period.months()
    for month in months:
        month_flags = collect_ops_flags(
            period.year,
            month,
            plan=plan,
            recalc_status=recalc_status,
        )
        for item in month_flags:
            key = (item["code"], item.get("label"))
            if key in seen:
                continue
            seen.add(key)
            out.append(item)

    if include_validate_hint:
        out.append(
            OpsFlag(
                code="validate_hint",
                level="info",
                title="Validación contra Excel Objetivos (CLI)",
                message=(
                    "Antes del cierre puede cuadrar modo2 con la hoja Objetivos "
                    "(columnas S–X) usando el validador en línea de comandos."
                ),
                fix=f"`{VALIDATE_CLI}`. Pasos: {DOCS_CIERRE_MENSUAL}#validacion-excel.",
            ).as_dict()
        )

    return out
