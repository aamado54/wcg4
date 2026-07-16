"""Reporte de cobertura / administración (solo .md)."""

from __future__ import annotations

from collections import defaultdict

from django.db.models import Count
from django.utils import timezone

from core.models import MetricDefinition, UNE
from imports.models import (
    CrossSaleImportRow,
    FileUpload,
    NewClientImportRow,
)
from pgc.models import (
    ManualRequirementsCompliance,
    MonthlyExchangeRate,
    MonthlyMetricResult,
    MonthlyModeScorecard,
    MonthlyTarget,
    PGCPlan,
)
from pgo.models import PgoResultadoPeriodo, Ticket
from reports.md_utils import ai_closing, bullets, h1, h2, h3, join_sections, md_table, p
from reports.models import ReportConfig
from reports.naming import report_stamp
from reports.services.common import period_label, ym_key
from risk.models import EstadoFinanciero, RiskOperationSnapshot


def build_admin_coverage_md(cfg: ReportConfig | None = None) -> str:
    cfg = cfg or ReportConfig.get_active()
    now = timezone.localtime()
    stamp = report_stamp(now).strip()

    sections = [
        h1("Reporte de administración / cobertura de datos"),
        p(f"**Generado:** {now.strftime('%Y-%m-%d %H:%M')} ({timezone.get_current_timezone_name()}) · marca `{stamp}`"),
        p(
            "Enfoque: disponibilidad y cobertura (no cifras de negocio). "
            "Áreas: **PGC**, **PGO**, **B. Riesgo**."
        ),
        p(f"**Config:** `{cfg.name}` · compact={cfg.compact_mode}"),
    ]

    # --- Global uploads ---
    uploads = FileUpload.objects.all().order_by("-created_at")
    up_rows = []
    for u in uploads[:40]:
        up_rows.append(
            [
                u.original_filename[:48],
                u.file_type_detected,
                u.status,
                f"{u.detected_year or '—'}-{int(u.detected_month or 0):02d}"
                if u.detected_month
                else "—",
                u.created_at.strftime("%Y-%m-%d") if u.created_at else "—",
            ]
        )
    sections += [
        h2("Archivos importados (recientes)"),
        md_table(
            ["Archivo", "Tipo", "Estado", "Período det.", "Creado"],
            up_rows
            or [["—", "—", "—", "—", "Sin uploads"]],
        ),
        p(f"Total FileUpload: **{uploads.count()}**"),
    ]

    # --- PGC coverage ---
    sections += _pgc_coverage()
    sections += _pgo_coverage()
    sections += _risk_coverage()

    hechos = [
        f"Uploads registrados: {uploads.count()}",
        f"Planes PGC: {PGCPlan.objects.count()}",
        f"Tickets PGO: {Ticket.objects.count()}",
        f"Snapshots riesgo: {RiskOperationSnapshot.objects.count()}",
    ]
    cambios = [
        "Este reporte es de cobertura; los cambios de negocio están en reportes PGC/PGO/B. Riesgo."
    ]
    vacios = _global_gaps()
    sections.append(ai_closing(hechos, cambios, vacios))
    return join_sections(*sections)


def _pgc_coverage() -> list[str]:
    out = [h2("PGC — cobertura por tema y período")]
    plans = list(PGCPlan.objects.order_by("year"))
    unes = list(UNE.objects.filter(is_active=True).order_by("sort_order"))
    metrics = list(MetricDefinition.objects.order_by("code"))

    out.append(h3("Disponible"))
    out.append(
        bullets(
            [
                f"Planes: {', '.join(str(p.year) for p in plans) or 'ninguno'}",
                f"UNEs activas: {', '.join(u.code for u in unes) or 'ninguna'}",
                f"Métricas: {', '.join(m.code for m in metrics) or 'ninguna'}",
                f"Filas clientes nuevos: {NewClientImportRow.objects.count()}",
                f"Filas venta cruzada: {CrossSaleImportRow.objects.count()}",
                f"Tipos de cambio: {MonthlyExchangeRate.objects.count()}",
                f"Metas (MonthlyTarget): {MonthlyTarget.objects.count()}",
                f"Resultados métrica: {MonthlyMetricResult.objects.count()}",
                f"Scorecards modo: {MonthlyModeScorecard.objects.count()}",
                f"Cumplimiento reqs: {ManualRequirementsCompliance.objects.count()}",
            ]
        )
    )

    by_period: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for y, m in MonthlyMetricResult.objects.values_list("year", "month").distinct():
        by_period[ym_key(y, m)]["resultados"] += 1
    for y, m in NewClientImportRow.objects.values_list("year", "month").distinct():
        by_period[ym_key(y, m)]["clientes"] += NewClientImportRow.objects.filter(
            year=y, month=m
        ).count()
    for y, m in CrossSaleImportRow.objects.values_list("year", "month").distinct():
        by_period[ym_key(y, m)]["venta_cruzada"] += CrossSaleImportRow.objects.filter(
            year=y, month=m
        ).count()
    for y, m in MonthlyModeScorecard.objects.values_list("year", "month").distinct():
        by_period[ym_key(y, m)]["scorecards"] += MonthlyModeScorecard.objects.filter(
            year=y, month=m
        ).count()
    for y, m in MonthlyExchangeRate.objects.values_list("year", "month"):
        by_period[ym_key(y, m)]["fx"] = 1
    for y, m in ManualRequirementsCompliance.objects.values_list("year", "month").distinct():
        by_period[ym_key(y, m)]["reqs"] += ManualRequirementsCompliance.objects.filter(
            year=y, month=m
        ).count()

    rows = []
    for key in sorted(by_period.keys()):
        d = by_period[key]
        rows.append(
            [
                key,
                d.get("resultados", 0),
                d.get("clientes", 0),
                d.get("venta_cruzada", 0),
                d.get("reqs", 0),
                d.get("scorecards", 0),
                "sí" if d.get("fx") else "no",
            ]
        )
    out.append(h3("Cobertura por período"))
    out.append(
        md_table(
            ["Período", "Resultados", "Clientes", "Vta cruzada", "Reqs", "Scores", "FX"],
            rows or [["—", 0, 0, 0, 0, 0, "no"]],
        )
    )

    missing = []
    if plans:
        year = plans[-1].year
        for month in range(1, 13):
            key = ym_key(year, month)
            d = by_period.get(key, {})
            gaps = []
            if not d.get("fx"):
                gaps.append("FX")
            if not d.get("scorecards"):
                gaps.append("score")
            if not d.get("resultados"):
                gaps.append("resultados")
            if gaps:
                missing.append(f"{period_label(year, month)}: falta {', '.join(gaps)}")
    out.append(h3("Faltante / pendiente (PGC)"))
    out.append(bullets(missing[:18] or ["Sin huecos evidentes en el último plan."]))
    return out


def _pgo_coverage() -> list[str]:
    out = [h2("PGO — cobertura")]
    tickets = Ticket.objects.count()
    periodos = list(
        PgoResultadoPeriodo.objects.values_list("periodo", flat=True).distinct().order_by("periodo")
    )
    by_estado = list(
        Ticket.objects.values("estado").annotate(n=Count("id")).order_by("estado")
    )
    out.append(h3("Disponible"))
    out.append(
        bullets(
            [
                f"Tickets: {tickets}",
                f"Resultados período: {PgoResultadoPeriodo.objects.count()}",
                f"Períodos con resultado: {', '.join(periodos) or 'ninguno'}",
            ]
            + [f"Estado {r['estado']}: {r['n']}" for r in by_estado]
        )
    )
    gaps = []
    if tickets == 0:
        gaps.append("Sin tickets cargados.")
    if not periodos:
        gaps.append("Sin PgoResultadoPeriodo calculados.")
    out.append(h3("Faltante / pendiente (PGO)"))
    out.append(bullets(gaps or ["Cobertura PGO presente."]))
    return out


def _risk_coverage() -> list[str]:
    out = [h2("B. Riesgo — cobertura")]
    snaps = RiskOperationSnapshot.objects.count()
    estados = EstadoFinanciero.objects.count()
    periods = sorted(
        {
            s.strftime("%Y-%m")
            for s in RiskOperationSnapshot.objects.values_list("fecha_snapshot", flat=True)
            if s
        }
    )
    ef_periods = sorted(set(EstadoFinanciero.objects.values_list("periodo", flat=True)))
    out.append(h3("Disponible"))
    out.append(
        bullets(
            [
                f"Snapshots operación: {snaps}",
                f"Estados financieros: {estados}",
                f"Períodos snapshot: {', '.join(periods[-12:]) or 'ninguno'}",
                f"Períodos EF: {', '.join(ef_periods[-12:]) or 'ninguno'}",
                f"Con alerta: {RiskOperationSnapshot.objects.filter(alerta=True).count()}",
            ]
        )
    )
    gaps = []
    if snaps == 0:
        gaps.append("Sin RiskOperationSnapshot.")
    if estados == 0:
        gaps.append("Sin EstadoFinanciero.")
    out.append(h3("Faltante / pendiente (B. Riesgo)"))
    out.append(bullets(gaps or ["Cobertura de riesgo presente."]))
    return out


def _global_gaps() -> list[str]:
    gaps = []
    if FileUpload.objects.filter(status=FileUpload.STATUS_UPLOADED).exists():
        gaps.append("Hay archivos UPLOADED pendientes de procesar.")
    if FileUpload.objects.filter(status=FileUpload.STATUS_PARSED_ERROR).exists():
        gaps.append("Hay archivos con PARSED_ERROR.")
    if not MonthlyExchangeRate.objects.exists():
        gaps.append("No hay tipos de cambio PGC.")
    if Ticket.objects.count() == 0:
        gaps.append("PGO sin tickets.")
    if RiskOperationSnapshot.objects.count() == 0:
        gaps.append("B. Riesgo sin snapshots.")
    return gaps or ["Sin vacíos globales críticos detectados."]
