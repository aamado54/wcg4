"""Resultados PGC extensos: tablero, charts, métricas, clientes browse, venta cruzada."""

from __future__ import annotations

from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from core.models import MetricDefinition, UNE
from imports.models import CrossSaleImportRow, NewClientImportRow
from pgc.models import (
    ManualRequirementsCompliance,
    MonthlyMetricResult,
    MonthlyMetricScore,
    MonthlyModeScorecard,
    MonthlyTarget,
)
from reports.md_utils import ai_closing, bullets, h1, h2, h3, join_sections, md_table, p
from reports.models import ReportConfig
from reports.naming import report_stamp
from reports.services.common import (
    fmt_num,
    pct_change,
    period_label,
    previous_month,
    ym_key,
)

SCORE_EXPLAIN = """
El **tablero principal PGC** consolida, por UNE y mes, los puntos de las métricas
scored (Ingresos, Clientes nuevos, Venta cruzada, Respuesta a requerimientos)
bajo una modalidad (`modo1` o `modo2`).

- Cada métrica tiene **meta** (`MonthlyTarget.target_value`) y **real**
  (`MonthlyMetricResult.measured_value`).
- El comando `recalc_pgc` asigna `points_awarded` en `MonthlyMetricScore`
  según la modalidad (cumplimiento meta vs real, con reglas adicionales en modo2).
- La suma es `MonthlyModeScorecard.total_points`.
- **Clasifica = Sí** si `total_points >= qualified_threshold` (default **80**).

Los charts del tablero grafican, por período y UNE, el **real vs meta** de
Ingresos (cifras en miles de US$), Clientes nuevos y Venta cruzada — no los
puntos del scorecard, sino las cifras de medición subyacentes.
""".strip()


def _all_score_periods() -> list[tuple[int, int]]:
    qs = (
        MonthlyModeScorecard.objects.order_by("year", "month")
        .values_list("year", "month")
        .distinct()
    )
    return [(int(y), int(m)) for y, m in qs]


def _sheet(name: str, title: str, headers: list, rows: list) -> dict:
    return {"name": name[:31], "title": title, "headers": headers, "rows": rows}


def build_pgc_results(cfg: ReportConfig | None = None) -> dict:
    cfg = cfg or ReportConfig.get_active()
    now = timezone.localtime()
    stamp = report_stamp(now)
    stamp_label = f"Generado {now.strftime('%Y-%m-%d %H:%M')} ({timezone.get_current_timezone_name()}) ·{stamp}"

    periods = _all_score_periods()
    if not periods and not MonthlyMetricResult.objects.exists():
        md = join_sections(
            h1("Reporte de resultados PGC"),
            p(stamp_label),
            p("No hay scorecards ni resultados PGC en la base."),
            ai_closing(
                ["Sin datos PGC."],
                ["Sin período anterior."],
                ["Cargar datos y ejecutar recalc_pgc."],
            ),
        )
        return {
            "md": md,
            "sheets": [
                _sheet("Resumen", "Sin datos", ["Nota"], [["Sin datos PGC"]])
            ],
            "stamp": stamp,
            "stamp_label": stamp_label,
        }

    mode = "modo1"
    latest = periods[-1] if periods else None
    if latest:
        prev = previous_month(*latest)
    else:
        prev = None

    # ---------- Scoreboard (como tablero) ----------
    scorecards = list(
        MonthlyModeScorecard.objects.filter(mode=mode)
        .select_related("une", "plan")
        .order_by("year", "month", "une__sort_order", "une__code")
    )
    score_map = {(s.year, s.month, s.une_id): s for s in scorecards}
    metric_scores = list(
        MonthlyMetricScore.objects.filter(mode=mode)
        .select_related("metric", "une")
        .order_by("year", "month", "metric__code")
    )
    points_by_key: dict[tuple[int, int, int], dict[str, Decimal]] = {}
    for ms in metric_scores:
        key = (ms.year, ms.month, ms.une_id)
        bucket = points_by_key.setdefault(key, {})
        bucket[ms.metric.code] = ms.points_awarded or Decimal("0")

    tablero_headers = [
        "UNE",
        "Periodo",
        "Pts Ingresos",
        "Pts Clientes",
        "Pts Venta cruzada",
        "Pts Respuesta reqs",
        "Total",
        "Umbral",
        "Clasifica",
    ]
    tablero_rows = []
    for s in scorecards:
        pts = points_by_key.get((s.year, s.month, s.une_id), {})
        tablero_rows.append(
            [
                s.une.code if s.une else "—",
                ym_key(s.year, s.month),
                fmt_num(pts.get(MetricDefinition.CODE_INGRESOS, 0)),
                fmt_num(pts.get(MetricDefinition.CODE_CLIENTES_NUEVOS, 0)),
                fmt_num(pts.get(MetricDefinition.CODE_VENTA_CRUZADA, 0)),
                fmt_num(pts.get(MetricDefinition.CODE_RESPUESTA_REQS, 0)),
                fmt_num(s.total_points),
                fmt_num(s.qualified_threshold or 80),
                "Sí" if s.is_month_qualified else "No",
            ]
        )

    # ---------- Chart series: real vs meta ----------
    chart_codes = [
        MetricDefinition.CODE_INGRESOS,
        MetricDefinition.CODE_CLIENTES_NUEVOS,
        MetricDefinition.CODE_VENTA_CRUZADA,
    ]
    chart_headers = ["Métrica", "Periodo", "UNE", "Meta", "Real", "Δ", "% Δ"]
    chart_rows = []
    for code in chart_codes:
        targets = MonthlyTarget.objects.filter(metric__code=code).select_related(
            "une", "metric"
        )
        results = {
            (r.year, r.month, r.une_id): r.measured_value
            for r in MonthlyMetricResult.objects.filter(metric__code=code)
        }
        for t in targets.order_by("year", "month", "une__sort_order"):
            real = results.get((t.year, t.month, t.une_id))
            meta = t.target_value
            dlt = (real or Decimal("0")) - (meta or Decimal("0")) if real is not None and meta is not None else None
            chart_rows.append(
                [
                    code,
                    ym_key(t.year, t.month),
                    t.une.code if t.une else "—",
                    fmt_num(meta, 2) if meta is not None else "—",
                    fmt_num(real, 2) if real is not None else "—",
                    fmt_num(dlt, 2) if dlt is not None else "—",
                    pct_change(real, meta) if real is not None and meta is not None else "—",
                ]
            )

    # ---------- Ingresos / clientes / venta cruzada measured dump ----------
    metric_result_headers = [
        "Métrica",
        "Periodo",
        "UNE",
        "Meta",
        "Real",
        "Moneda fuente",
        "Estado conversión",
        "Nota",
    ]
    metric_result_rows = []
    for r in (
        MonthlyMetricResult.objects.select_related("metric", "une")
        .order_by("metric__code", "year", "month", "une__sort_order")
    ):
        tgt = (
            MonthlyTarget.objects.filter(
                plan_id=r.plan_id,
                metric_id=r.metric_id,
                une_id=r.une_id,
                year=r.year,
                month=r.month,
            )
            .values_list("target_value", flat=True)
            .first()
        )
        metric_result_rows.append(
            [
                r.metric.code if r.metric else "—",
                ym_key(r.year, r.month),
                r.une.code if r.une else "—",
                fmt_num(tgt, 2) if tgt is not None else "—",
                fmt_num(r.measured_value, 2) if r.measured_value is not None else "—",
                getattr(r, "source_currency", "") or "—",
                getattr(r, "conversion_status", "") or "—",
                (r.calculation_note or "")[:120],
            ]
        )

    # ---------- Clientes nuevos — detalle browse ----------
    client_headers = [
        "Periodo",
        "UNE",
        "Cliente",
        "NIT",
        "Operación",
        "Contratos previos",
        "Cuenta como nuevo",
        "Moneda",
        "Monto (miles si USD PGC)",
        "UNE cruda",
        "Observaciones",
        "Fila origen",
    ]
    client_rows = []
    for row in (
        NewClientImportRow.objects.select_related("une", "currency")
        .order_by("year", "month", "une__sort_order", "client_name", "id")
    ):
        client_rows.append(
            [
                ym_key(row.year, row.month),
                row.une.code if row.une else "—",
                row.client_name,
                row.nit,
                row.operation_code,
                row.previous_contracts,
                "Sí" if row.counts_as_new else "No",
                row.currency.code if row.currency else "—",
                fmt_num(row.amount, 2) if row.amount is not None else "—",
                row.raw_une_value,
                row.observations or "",
                row.source_row_number or "",
            ]
        )

    # ---------- Venta cruzada detalle ----------
    xc_headers = [
        "Periodo",
        "Cliente",
        "Operación",
        "Fecha",
        "Moneda",
        "UNE origen",
        "UNE destino",
        "UNE origen raw",
        "UNE destino raw",
    ]
    xc_rows = []
    for row in (
        CrossSaleImportRow.objects.select_related(
            "currency", "une_origin", "une_destination"
        ).order_by("year", "month", "client_name", "id")
    ):
        xc_rows.append(
            [
                ym_key(row.year, row.month),
                row.client_name,
                row.operation_code,
                row.date.isoformat() if row.date else "",
                row.currency.code if row.currency else "—",
                row.une_origin.code if row.une_origin else "—",
                row.une_destination.code if row.une_destination else "—",
                row.raw_une_origin,
                row.raw_une_destination,
            ]
        )

    # ---------- Requerimientos ----------
    req_headers = ["Periodo", "UNE", "Cumple", "Nota incidente"]
    req_rows = []
    for r in ManualRequirementsCompliance.objects.select_related("une").order_by(
        "year", "month", "une__sort_order"
    ):
        req_rows.append(
            [
                ym_key(r.year, r.month),
                r.une.code if r.une else "—",
                "Sí" if r.is_compliant else "No",
                (r.incident_note or "")[:200],
            ]
        )

    # ---------- Comparación último vs anterior ----------
    cambios = []
    hechos = [
        f"Modalidad de score reportada: {mode}",
        f"Filas tablero (scorecards): {len(tablero_rows)}",
        f"Series chart (meta/real): {len(chart_rows)}",
        f"Resultados métrica: {len(metric_result_rows)}",
        f"Detalle clientes: {len(client_rows)}",
        f"Detalle venta cruzada: {len(xc_rows)}",
        f"Cumplimiento reqs: {len(req_rows)}",
    ]
    if latest:
        hechos.append(f"Último período con score: {period_label(*latest)} ({ym_key(*latest)})")
        ly, lm = latest
        for une in UNE.objects.filter(is_active=True).order_by("sort_order"):
            cur = score_map.get((ly, lm, une.id))
            if not cur or not prev:
                continue
            prv = score_map.get((prev[0], prev[1], une.id))
            if not prv:
                continue
            cambios.append(
                f"{une.code} {ym_key(*prev)}→{ym_key(*latest)}: "
                f"{fmt_num(prv.total_points)} → {fmt_num(cur.total_points)} "
                f"({pct_change(cur.total_points, prv.total_points)}); "
                f"Clasifica {('Sí' if prv.is_month_qualified else 'No')}→"
                f"{('Sí' if cur.is_month_qualified else 'No')}"
            )

    vacios = []
    if not tablero_rows:
        vacios.append("Sin MonthlyModeScorecard (ejecutar recalc_pgc).")
    if not client_rows:
        vacios.append("Sin NewClientImportRow.")
    if not xc_rows:
        vacios.append("Sin CrossSaleImportRow.")
    if not chart_rows:
        vacios.append("Sin metas/reales para charts.")
    if latest and prev and not cambios:
        vacios.append(
            f"Hay último período {ym_key(*latest)} pero pocas comparaciones vs {ym_key(*prev)}."
        )

    # ---------- Markdown ----------
    md_parts = [
        h1("Reporte de resultados PGC (extenso)"),
        p(stamp_label),
        p(
            "Propósito: entregar a IA generativa y a usuarios humanos el **detalle operativo** "
            "del PGC (tablero, cifras de charts, clientes, venta cruzada) para análisis estratégico."
        ),
        h2("Cómo interpretar el tablero y el cálculo"),
        p(SCORE_EXPLAIN),
        h2("Tabla de puntos del tablero principal"),
        p(f"Modalidad: **{mode}**. Filas: **{len(tablero_rows)}**."),
        md_table(tablero_headers, tablero_rows)
        if tablero_rows
        else p("_Sin scorecards._"),
        h2("Cifras base de los charts (meta vs real)"),
        p(
            "Ingresos en miles de US$ según regla PGC; clientes y venta cruzada en unidades del sistema. "
            f"Filas: **{len(chart_rows)}**."
        ),
        md_table(chart_headers, chart_rows) if chart_rows else p("_Sin series chart._"),
        h2("Resultados de métricas (MonthlyMetricResult)"),
        md_table(metric_result_headers, metric_result_rows)
        if metric_result_rows
        else p("_Sin resultados._"),
        h2("Clientes nuevos — detalle completo (browse)"),
        p(
            "Equivalente al detalle visto en Administración → Clientes (browse). "
            f"Registros: **{len(client_rows)}**."
        ),
        md_table(client_headers, client_rows) if client_rows else p("_Sin clientes importados._"),
        h2("Venta cruzada — detalle"),
        p(f"Registros: **{len(xc_rows)}**."),
        md_table(xc_headers, xc_rows) if xc_rows else p("_Sin venta cruzada._"),
        h2("Respuesta a requerimientos"),
        md_table(req_headers, req_rows) if req_rows else p("_Sin registros de requerimientos._"),
        h2("Cambios último período vs anterior"),
        bullets(cambios[:40] or ["Sin pares comparables suficientes."]),
        h2("Inventario de cobertura en este reporte"),
        bullets(hechos),
    ]
    if cfg.include_ai_section:
        md_parts.append(
            ai_closing(
                hechos,
                cambios[:30] if cfg.include_period_comparison else ["Comparación desactivada en config."],
                vacios or ["Sin vacíos críticos detectados en PGC."],
            )
        )
    md_parts.append(
        p(
            "_Instrucción para IA:_ con las tablas anteriores, elabora un análisis estratégico "
            "(estado, tendencias, riesgos, oportunidades y recomendaciones accionables) "
            "sin inventar cifras que no aparezcan aquí."
        )
    )

    sheets = [
        _sheet("Tablero puntos", f"Tablero PGC {mode}", tablero_headers, tablero_rows),
        _sheet("Charts meta real", "Series charts PGC", chart_headers, chart_rows),
        _sheet("Metricas medidas", "MonthlyMetricResult", metric_result_headers, metric_result_rows),
        _sheet("Clientes detalle", "NewClientImportRow browse", client_headers, client_rows),
        _sheet("Venta cruzada", "CrossSaleImportRow", xc_headers, xc_rows),
        _sheet("Requerimientos", "ManualRequirementsCompliance", req_headers, req_rows),
        _sheet(
            "Explicacion",
            "Sentido del cálculo PGC",
            ["Tema", "Detalle"],
            [
                ["Modalidad", mode],
                ["Umbral clasifica default", "80 puntos (qualified_threshold)"],
                ["Clasifica", "total_points >= qualified_threshold"],
                ["Charts", "real vs meta INGRESOS / CLIENTES_NUEVOS / VENTA_CRUZADA"],
                ["Fuente clientes", "NewClientImportRow (browse admin)"],
            ],
        ),
    ]

    return {
        "md": join_sections(*md_parts),
        "sheets": sheets,
        "stamp": stamp,
        "stamp_label": stamp_label,
        "period": latest,
        "prev_period": prev,
    }
