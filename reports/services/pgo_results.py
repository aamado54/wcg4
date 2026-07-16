"""Resultados PGO extensos: dashboard productivo + browse + stack WCG One."""

from __future__ import annotations

from django.db.models import Count, Q
from django.utils import timezone

from pgo.models import PgoResultadoPeriodo, Ticket, TicketEvento
from reports.md_utils import ai_closing, bullets, h1, h2, h3, join_sections, md_table, p
from reports.models import ReportConfig
from reports.naming import report_stamp
from reports.services.common import fmt_num, pct_change

PGO_EXPLAIN = """
El **dashboard PGO productivo** (`/pgo/`) se alimenta de tickets (`pgo.Ticket`).
Tras la importación (o al abrir el dashboard) se ejecuta
`pgo.periodo.recalculate_pgo_periodos`, que llena `PgoResultadoPeriodo` por
período (`YYYY-MM` de apertura) y unidad de negocio con:

- tickets cerrados / abiertos
- tiempo promedio de cierre (horas)
- % cumplimiento SLA: cerrados cuyo tiempo ≤ `sla_horas` del ticket

**No** hay en el pipeline productivo un campo `Clasifica` calculado.
El stack WCG One (`apps.pgo`) puede coexistir con tickets, agregados mensuales
y `PgoPeriodScore.clasifica` si existen filas; el motor de score no está
garantizado en código.

Este reporte incluye **ambas fuentes** cuando hay datos: tablas del tablero,
resúmenes por usuario/unidad, detalle browse de tickets y el detalle WCG One.
""".strip()


def _sheet(name, title, headers, rows):
    return {"name": name[:31], "title": title, "headers": headers, "rows": rows}


def _wcg_pgo_block(stamp_label: str) -> tuple[list[str], list[dict], list[str], list[str]]:
    """Secciones MD + sheets + hechos + vacíos del stack apps.pgo."""
    md: list[str] = []
    sheets: list[dict] = []
    hechos: list[str] = []
    vacios: list[str] = []
    try:
        from apps.pgo.models import (
            PgoMetricRule,
            PgoMonthlyAgg,
            PgoPeriodScore,
            PgoTicket,
        )
        from apps.pgo.selectors import ticket_dashboard_summary
    except Exception as exc:
        md.append(h2("Stack WCG One PGO (`apps.pgo`)"))
        md.append(p(f"_No disponible: {exc}_"))
        vacios.append(f"Stack apps.pgo no importable: {exc}")
        return md, sheets, hechos, vacios

    summary = ticket_dashboard_summary()
    kpi_headers = ["KPI", "Valor"]
    kpi_rows = [
        ["Total tickets", summary["total_tickets"]],
        ["Abiertos", summary["tickets_abiertos"]],
        ["Cerrados", summary["tickets_cerrados"]],
        ["Vencidos (abiertos SLA no)", summary["tickets_vencidos"]],
        ["SLA cumplidos", summary["sla_cumplidos"]],
        ["SLA incumplidos (abiertos)", summary["sla_incumplidos"]],
        ["Tiempo promedio (h)", fmt_num(summary["tiempo_promedio"], 2) if summary["tiempo_promedio"] is not None else "—"],
    ]
    hechos.append(f"WCG One PgoTicket: {summary['total_tickets']}")

    md.extend(
        [
            h2("Stack WCG One — dashboard KPIs (`apps.pgo`)"),
            p(
                "Equivalente a `/wcgone/pgo/`: KPIs, desglose por estado/prioridad "
                "y detalle completo de tickets importados al schema WCG One."
            ),
            md_table(kpi_headers, kpi_rows),
            h3("Por estado normalizado"),
            md_table(
                ["Estado", "Total"],
                [[r["estado_normalizado"] or "—", r["total"]] for r in summary["por_estado"]],
            )
            if summary["por_estado"]
            else p("_Sin desglose por estado._"),
            h3("Por prioridad"),
            md_table(
                ["Prioridad", "Total"],
                [[r["prioridad"] or "—", r["total"]] for r in summary["por_prioridad"]],
            )
            if summary["por_prioridad"]
            else p("_Sin desglose por prioridad._"),
        ]
    )
    sheets.append(_sheet("WCG KPI", "KPIs WCG One PGO", kpi_headers, kpi_rows))
    sheets.append(
        _sheet(
            "WCG por estado",
            "PgoTicket por estado",
            ["Estado", "Total"],
            [[r["estado_normalizado"] or "", r["total"]] for r in summary["por_estado"]],
        )
    )
    sheets.append(
        _sheet(
            "WCG por prioridad",
            "PgoTicket por prioridad",
            ["Prioridad", "Total"],
            [[r["prioridad"] or "", r["total"]] for r in summary["por_prioridad"]],
        )
    )

    ticket_headers = [
        "ID externo",
        "Título",
        "Estado raw",
        "Estado norm.",
        "Prioridad",
        "Departamento",
        "Sistema",
        "Periodo",
        "UN",
        "Responsable",
        "Solicita",
        "Correo",
        "Tipo",
        "Tipo servicio",
        "Elemento",
        "Ruta",
        "Apertura",
        "Cierre",
        "Duración h",
        "SLA h",
        "SLA ok",
        "Solución",
        "Razón cierre",
    ]
    ticket_rows = []
    for t in PgoTicket.objects.select_related("unidad_negocio", "responsable").order_by(
        "-fecha_apertura", "ticket_externo_id"
    ):
        ticket_rows.append(
            [
                t.ticket_externo_id,
                t.titulo or "",
                t.estado_raw or "",
                t.estado_normalizado or "",
                t.prioridad or "",
                t.departamento or "",
                t.sistema or "",
                t.anio_mes or "",
                t.unidad_negocio.code if t.unidad_negocio else "—",
                getattr(t.responsable, "username", None) or "—",
                t.usuario_solicita or "",
                t.correo_solicita or "",
                t.tipo or "",
                t.tipo_servicio or "",
                t.elemento or "",
                t.ruta or "",
                t.fecha_apertura.isoformat() if t.fecha_apertura else "",
                t.fecha_cierre.isoformat() if t.fecha_cierre else "",
                fmt_num(t.duracion_horas, 2) if t.duracion_horas is not None else "",
                t.sla_horas if t.sla_horas is not None else "",
                "Sí" if t.sla_cumplido else ("No" if t.sla_cumplido is False else "—"),
                (t.solucion or "")[:300],
                (t.razon_cierre or "")[:160],
            ]
        )
    md.extend(
        [
            h2("WCG One — detalle completo de tickets (browse)"),
            p(f"Registros: **{len(ticket_rows)}**. Exportables también en Excel."),
            md_table(ticket_headers, ticket_rows) if ticket_rows else p("_Sin PgoTicket._"),
        ]
    )
    sheets.append(_sheet("WCG Tickets", "PgoTicket detalle", ticket_headers, ticket_rows))
    if not ticket_rows:
        vacios.append("Sin PgoTicket en apps.pgo (importar tickets WCG One).")

    score_headers = [
        "Periodo",
        "Área",
        "UN",
        "Usuario",
        "Puntaje",
        "Clasifica",
        "Fecha cálculo",
        "Detalle JSON",
    ]
    score_rows = []
    for s in PgoPeriodScore.objects.select_related("unidad_negocio", "usuario").order_by(
        "-periodo", "area"
    ):
        score_rows.append(
            [
                s.periodo,
                s.area or "",
                str(s.unidad_negocio) if s.unidad_negocio else "—",
                str(s.usuario) if s.usuario else "—",
                fmt_num(s.puntaje_total, 2),
                "Sí" if s.clasifica else "No",
                s.fecha_calculo.isoformat() if getattr(s, "fecha_calculo", None) else "",
                str(s.detalle_json or "")[:400],
            ]
        )
    md.extend(
        [
            h2("WCG One — resultados / PgoPeriodScore"),
            p(
                "Tabla de `/wcgone/pgo/resultados/`. **Clasifica** solo si hay filas; "
                "no inventar umbrales si el puntaje no está calculado en código."
            ),
            md_table(score_headers, score_rows)
            if score_rows
            else p("_Sin PgoPeriodScore._"),
        ]
    )
    sheets.append(_sheet("WCG Scores", "PgoPeriodScore", score_headers, score_rows))
    hechos.append(f"WCG One PgoPeriodScore: {len(score_rows)}")
    if not score_rows:
        vacios.append("Sin PgoPeriodScore (scoring WCG One vacío o no calculado).")

    agg_headers = [
        "Periodo",
        "UN",
        "Departamento",
        "Recibidos",
        "Cerrados",
        "Abiertos fin mes",
        "Tiempo prom. h",
        "SLA ok",
        "SLA no",
    ]
    agg_rows = []
    for a in PgoMonthlyAgg.objects.select_related("unidad_negocio").order_by(
        "-periodo", "unidad_negocio__nombre"
    ):
        agg_rows.append(
            [
                a.periodo,
                str(a.unidad_negocio) if a.unidad_negocio else "—",
                a.departamento or "",
                a.tickets_recibidos,
                a.tickets_cerrados,
                a.tickets_abiertos_fin_mes,
                fmt_num(a.tiempo_promedio_horas, 2) if a.tiempo_promedio_horas is not None else "",
                a.sla_cumplidos,
                a.sla_incumplidos,
            ]
        )
    md.extend(
        [
            h2("WCG One — agregados mensuales (PgoMonthlyAgg)"),
            md_table(agg_headers, agg_rows) if agg_rows else p("_Sin PgoMonthlyAgg._"),
        ]
    )
    sheets.append(_sheet("WCG Agg mensual", "PgoMonthlyAgg", agg_headers, agg_rows))

    rule_headers = [
        "Código",
        "Área",
        "Variable",
        "Puntos",
        "Peso",
        "Tipo regla",
        "Activo",
        "Fórmula",
        "Notas",
    ]
    rule_rows = []
    for r in PgoMetricRule.objects.order_by("area", "codigo"):
        rule_rows.append(
            [
                r.codigo,
                r.area or "",
                r.variable or "",
                fmt_num(r.puntos, 2) if r.puntos is not None else "",
                fmt_num(r.peso, 2) if r.peso is not None else "",
                r.tipo_regla or "",
                "Sí" if r.activo else "No",
                (r.formula_texto or "")[:200],
                (r.notas or "")[:160],
            ]
        )
    md.extend(
        [
            h2("WCG One — catálogo de reglas de métrica"),
            md_table(rule_headers, rule_rows)
            if rule_rows
            else p("_Sin PgoMetricRule._"),
        ]
    )
    sheets.append(_sheet("WCG Reglas", "PgoMetricRule", rule_headers, rule_rows))
    return md, sheets, hechos, vacios


def build_pgo_results(cfg: ReportConfig | None = None) -> dict:
    cfg = cfg or ReportConfig.get_active()
    now = timezone.localtime()
    stamp = report_stamp(now)
    stamp_label = (
        f"Generado {now.strftime('%Y-%m-%d %H:%M')} "
        f"({timezone.get_current_timezone_name()}) ·{stamp}"
    )

    # ----- KPI tablero productivo -----
    recibidos = Ticket.objects.count()
    abiertos = Ticket.objects.filter(
        estado__in=["ABIERTO", "EN_PROCESO"]
    ).count()
    cerrados = Ticket.objects.filter(estado="CERRADO").count()
    kpi_headers = ["KPI dashboard /pgo/", "Valor"]
    kpi_rows = [
        ["Recibidos (total)", recibidos],
        ["Abiertos (ABIERTO+EN_PROCESO)", abiertos],
        ["Cerrados", cerrados],
    ]

    resultados = list(
        PgoResultadoPeriodo.objects.select_related("unidad_negocio").order_by(
            "periodo", "unidad_negocio__nombre"
        )
    )
    res_headers = [
        "Periodo",
        "Unidad",
        "Código UN",
        "Cerrados",
        "Abiertos",
        "Tiempo prom. h",
        "SLA %",
    ]
    res_rows = []
    for r in resultados:
        res_rows.append(
            [
                r.periodo,
                r.unidad_negocio.nombre if r.unidad_negocio else "—",
                r.unidad_negocio.code if r.unidad_negocio else "—",
                r.tickets_cerrados,
                r.tickets_abiertos,
                fmt_num(r.tiempo_promedio_horas, 2),
                fmt_num(r.cumplimiento_sla_pct, 2),
            ]
        )

    # Serie de cifras base (equivalente a “charts”): por período totales
    serie_headers = [
        "Periodo",
        "Cerrados",
        "Abiertos",
        "SLA % ponderado (promedio simple UN)",
        "Tiempo prom. h (promedio simple UN)",
    ]
    serie_rows = []
    by_period: dict[str, list] = {}
    for r in resultados:
        by_period.setdefault(r.periodo, []).append(r)
    for periodo in sorted(by_period):
        rows_p = by_period[periodo]
        n = len(rows_p) or 1
        serie_rows.append(
            [
                periodo,
                sum(x.tickets_cerrados for x in rows_p),
                sum(x.tickets_abiertos for x in rows_p),
                fmt_num(sum(float(x.cumplimiento_sla_pct or 0) for x in rows_p) / n, 2),
                fmt_num(sum(float(x.tiempo_promedio_horas or 0) for x in rows_p) / n, 2),
            ]
        )

    periodos = sorted({r.periodo for r in resultados})
    curr_p = periodos[-1] if periodos else None
    prev_p = periodos[-2] if len(periodos) > 1 else None
    cambios = []
    if curr_p and prev_p:
        prev_map = {r.unidad_negocio_id: r for r in resultados if r.periodo == prev_p}
        for r in [x for x in resultados if x.periodo == curr_p]:
            prv = prev_map.get(r.unidad_negocio_id)
            if not prv:
                continue
            cambios.append(
                f"{r.unidad_negocio.code if r.unidad_negocio else '?'}: "
                f"SLA {fmt_num(prv.cumplimiento_sla_pct, 2)}%→{fmt_num(r.cumplimiento_sla_pct, 2)}% "
                f"({pct_change(r.cumplimiento_sla_pct, prv.cumplimiento_sla_pct)}); "
                f"cerrados {prv.tickets_cerrados}→{r.tickets_cerrados}; "
                f"abiertos {prv.tickets_abiertos}→{r.tickets_abiertos}"
            )

    # Resumen por usuario (como /pgo/resumen/usuario/)
    user_headers = ["Usuario asignado", "Total tickets", "Abiertos"]
    user_rows = []
    for row in (
        Ticket.objects.values("asignado_a__username")
        .annotate(
            total=Count("id"),
            abiertos_n=Count("id", filter=Q(estado="ABIERTO")),
        )
        .order_by("-total")
    ):
        user_rows.append(
            [
                row["asignado_a__username"] or "(sin asignar)",
                row["total"],
                row["abiertos_n"],
            ]
        )

    # Resumen por unidad
    un_headers = ["Código UN", "Nombre", "Total tickets"]
    un_rows = []
    for row in (
        Ticket.objects.values("unidad_negocio__code", "unidad_negocio__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")
    ):
        un_rows.append(
            [
                row["unidad_negocio__code"] or "—",
                row["unidad_negocio__nombre"] or "—",
                row["total"],
            ]
        )

    by_estado = list(
        Ticket.objects.values("estado").annotate(n=Count("id")).order_by("estado")
    )
    by_prio = list(
        Ticket.objects.values("prioridad").annotate(n=Count("id")).order_by("prioridad")
    )

    ticket_headers = [
        "Código",
        "Título",
        "Descripción",
        "Estado",
        "Prioridad",
        "UN",
        "Entidad",
        "Asignado",
        "Apertura",
        "Cierre",
        "SLA horas",
        "Horas ciclo",
        "SLA ok",
        "Creado",
        "Actualizado",
    ]
    ticket_rows = []
    for t in Ticket.objects.select_related(
        "unidad_negocio", "entidad", "asignado_a"
    ).order_by("-fecha_apertura", "codigo"):
        horas = ""
        sla_ok = ""
        if t.fecha_apertura and t.fecha_cierre:
            try:
                delta = t.fecha_cierre - t.fecha_apertura
                horas_val = round(delta.total_seconds() / 3600, so=2)
                horas = horas_val
                sla_ok = "Sí" if horas_val <= float(t.sla_horas or 0) else "No"
            except Exception:
                pass
        ticket_rows.append(
            [
                t.codigo,
                t.titulo or "",
                t.descripcion or "",
                t.estado,
                t.prioridad,
                t.unidad_negocio.code if t.unidad_negocio else "—",
                getattr(t.entidad, "codigo", None)
                or getattr(t.entidad, "nombre", None)
                or "—",
                getattr(t.asignado_a, "username", None) or "—",
                t.fecha_apertura.isoformat() if t.fecha_apertura else "",
                t.fecha_cierre.isoformat() if t.fecha_cierre else "",
                t.sla_horas,
                horas,
                sla_ok,
                t.created_at.isoformat() if t.created_at else "",
                t.updated_at.isoformat() if t.updated_at else "",
            ]
        )

    evento_headers = ["Ticket", "Tipo", "Fecha", "Usuario", "Descripción"]
    evento_rows = []
    evento_cap = 5000
    for e in (
        TicketEvento.objects.select_related("ticket", "usuario")
        .order_by("-fecha")[:evento_cap]
    ):
        evento_rows.append(
            [
                e.ticket.codigo if e.ticket else "—",
                e.tipo,
                e.fecha.isoformat() if e.fecha else "",
                getattr(e.usuario, "username", None) or "—",
                e.descripcion or "",
            ]
        )
    evento_total = TicketEvento.objects.count()

    wcg_md, wcg_sheets, wcg_hechos, wcg_vacios = _wcg_pgo_block(stamp_label)

    hechos = [
        f"Tickets productivo: {recibidos}",
        f"Abiertos: {abiertos} · Cerrados: {cerrados}",
        f"Filas PgoResultadoPeriodo: {len(res_rows)}",
        f"Período último resultados: {curr_p or 'n/d'}",
        f"Período anterior: {prev_p or 'n/d'}",
        f"Eventos listados: {len(evento_rows)} de {evento_total}",
        *wcg_hechos,
    ]
    vacios = list(wcg_vacios)
    if not ticket_rows:
        vacios.append("Sin tickets en pgo.Ticket.")
    if not res_rows:
        vacios.append("Sin PgoResultadoPeriodo (importar tickets / recalcular períodos).")
    if evento_total > evento_cap:
        vacios.append(
            f"TicketEvento truncado a {evento_cap} filas más recientes (hay {evento_total})."
        )

    md_parts = [
        h1("Reporte de resultados PGO (extenso)"),
        p(stamp_label),
        p(
            "Propósito: datos operativos completos de PGO para análisis estratégico "
            "por IA y exportación Excel humana. CRM no se incluye."
        ),
        h2("Cómo se procesa PGO"),
        p(PGO_EXPLAIN),
        h2("Dashboard productivo — KPIs"),
        md_table(kpi_headers, kpi_rows),
        h2("Dashboard — resultados por período y unidad"),
        p(
            "Tabla del tablero `/pgo/` (`PgoResultadoPeriodo`). Sentido: medir "
            "carga y cumplimiento SLA por UN y mes de apertura del ticket."
        ),
        p(f"Filas: **{len(res_rows)}**."),
        md_table(res_headers, res_rows) if res_rows else p("_Sin resultados de período._"),
        h2("Cifras base por período (serie para análisis / gráficos)"),
        p(
            "Agregados por período a partir de la tabla de resultados — útiles para "
            "construir tendencias de volumen y SLA en Excel o por IA."
        ),
        md_table(serie_headers, serie_rows) if serie_rows else p("_Sin serie._"),
        h2("Cambios último vs período anterior"),
        bullets(cambios[:80] or ["Sin pares de períodos comparables."]),
        h2("Resumen de tickets por estado"),
        md_table(
            ["Estado", "Cantidad"],
            [[r["estado"], r["n"]] for r in by_estado],
        )
        if by_estado
        else p("_Sin tickets._"),
        h2("Resumen de tickets por prioridad"),
        md_table(
            ["Prioridad", "Cantidad"],
            [[r["prioridad"], r["n"]] for r in by_prio],
        )
        if by_prio
        else p("_Sin desglose._"),
        h2("Resumen por unidad de negocio (browse tablero)"),
        md_table(un_headers, un_rows) if un_rows else p("_Sin desglose._"),
        h2("Resumen por usuario asignado"),
        p("Equivalente a `/pgo/resumen/usuario/`."),
        md_table(user_headers, user_rows) if user_rows else p("_Sin asignación._"),
        h2("Detalle completo de tickets (browse administración)"),
        p(
            f"Registros: **{len(ticket_rows)}**. Incluye descripción completa "
            "como en el detalle del ticket."
        ),
        md_table(ticket_headers, ticket_rows) if ticket_rows else p("_Sin tickets._"),
        h2("Eventos de tickets"),
        p(
            f"Filas incluidas: **{len(evento_rows)}**"
            + (f" (tope {evento_cap}; total BD {evento_total})." if evento_total else ".")
        ),
        md_table(evento_headers, evento_rows) if evento_rows else p("_Sin eventos._"),
        *wcg_md,
        h2("Inventario"),
        bullets(hechos),
        h2("Guía de análisis estratégico (IA)"),
        p(
            "Con las tablas anteriores, construye un diagnóstico de operación PGO: "
            "(1) ¿el SLA mejora o empeora por UN y período?; "
            "(2) ¿hay sobrecarga en usuarios o unidades concretas?; "
            "(3) ¿cuántos tickets abiertos críticos/alta prioridad hay y desde cuándo?; "
            "(4) recomendaciones accionables (redistribuir, revisar SLA, priorizar backlog). "
            "Cita cifras explícitas. No inventes Clasifica ni umbrales ausentes en los datos."
        ),
    ]
    if cfg.include_ai_section:
        md_parts.append(
            ai_closing(
                hechos,
                cambios[:40] if cfg.include_period_comparison else ["Comparación desactivada."],
                vacios or ["Sin vacíos críticos adicionales."],
            )
        )

    sheets = [
        _sheet("KPI dashboard", "KPIs /pgo/", kpi_headers, kpi_rows),
        _sheet("Resultados periodo", "PgoResultadoPeriodo", res_headers, res_rows),
        _sheet("Serie por periodo", "Cifras base tendencia", serie_headers, serie_rows),
        _sheet("Por estado", "Conteo tickets", ["Estado", "N"], [[r["estado"], r["n"]] for r in by_estado]),
        _sheet(
            "Por prioridad",
            "Conteo prioridad",
            ["Prioridad", "N"],
            [[r["prioridad"], r["n"]] for r in by_prio],
        ),
        _sheet("Por UN", "Resumen unidad", un_headers, un_rows),
        _sheet("Por usuario", "Resumen asignado", user_headers, user_rows),
        _sheet("Tickets", "Detalle tickets PGO", ticket_headers, ticket_rows),
        _sheet("Eventos", f"TicketEvento (hasta {evento_cap})", evento_headers, evento_rows),
        _sheet(
            "Explicacion",
            "Proceso PGO",
            ["Tema", "Detalle"],
            [
                ["Fuente productiva", "pgo.Ticket + recalculate_pgo_periodos"],
                ["SLA", "horas ciclo <= sla_horas"],
                ["Clasifica PGO productivo", "No implementada"],
                ["Fuente WCG One", "apps.pgo.* si hay datos"],
            ],
        ),
        *wcg_sheets,
    ]

    return {
        "md": join_sections(*md_parts),
        "sheets": sheets,
        "stamp": stamp,
        "stamp_label": stamp_label,
        "period": curr_p,
        "prev_period": prev_p,
    }
