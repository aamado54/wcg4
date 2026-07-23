# CONCATENATED .PY FILES

PART_NUMBER=10
TOTAL_PARTS=10

DOCUMENT_MODE=LITERAL_CODE_ARCHIVE
PARSING_PRIORITY=PATH_LITERAL->CONTENT_NUMBERED_BEGIN->CONTENT_BASE64_BEGIN->CONTENT_BEGIN
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
RECORD_SEPARATOR=BEGIN_LITERAL_FILE_RECORD|END_LITERAL_FILE_RECORD
RECORD_BOUNDARY=========== RECORD_BOUNDARY ==========
CONTENT_POLICY=PRESERVE_EXACT_TEXT_WITH_METADATA_AND_NUMBERED_FALLBACK
READING_HINT=Prefer PATH_LITERAL first for file identity. Prefer CONTENT_NUMBERED_BEGIN for faithful line-by-line reading. Use CONTENT_BASE64_BEGIN for exact reconstruction when available. Use CONTENT_BEGIN only as a convenience view. If CONTENT_BEGIN looks compacted, flattened, or visually altered, do not use it to infer exact identifiers, variable names, paths, punctuation grouping, or spacing.
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/services/risk_results.py
PATH_JSON="reports/services/risk_results.py"
FILENAME=risk_results.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=839
SIZE_BYTES_UTF8=31158
CONTENT_SHA256=82945c8634ab954aa6a328bbea46a1d07f5d9c5bb1c7bccffb54ac9359a66643
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Resultados Balón de Riesgo extensos: comando balón + detalle + WCG One."""

from __future__ import annotations

from decimal import Decimal

from django.db.models import Count, Max, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from reports.md_utils import ai_closing, bullets, h1, h2, h3, join_sections, md_table, p
from reports.models import ReportConfig
from reports.naming import report_stamp
from reports.services.common import fmt_num, pct_change
from risk.models import (
    ContactoCobranza,
    EstadoFinanciero,
    PagoRealizado,
    ProgramacionPago,
    RiskOperationSnapshot,
)

RISK_EXPLAIN = """
El **Balón de Riesgo** productivo (`/risk/`) concentra:

- `RiskOperationSnapshot` — snapshot por operación (nivel, mora, saldo, exigible, alerta)
- Vista **Comando Balón**: último snapshot por (entidad, referencia_operacion)
- `EstadoFinanciero` — saldo/exposición/mora por entidad y período `YYYY-MM`
- `ProgramacionPago` / `PagoRealizado` — agenda y pagos
- `ContactoCobranza` — directorio de contactos

El stack WCG One (`apps.risk`) puede coexistir con snapshots leasing ricos,
estados financieros contables, alertas estructuradas y pagos desglosados.

Este reporte incluye **tablero comando balón**, listados operativos, histórico
completo y el detalle WCG One cuando existen datos.
""".strip()


def _sheet(name, title, headers, rows):
    return {"name": name[:31], "title": title, "headers": headers, "rows": rows}


def _ym(dt) -> str:
    if not dt:
        return ""
    if hasattr(dt, "strftime"):
        return dt.strftime("%Y-%m")
    return str(dt)[:7]


def _wcg_risk_block() -> tuple[list[str], list[dict], list[str], list[str]]:
    md: list[str] = []
    sheets: list[dict] = []
    hechos: list[str] = []
    vacios: list[str] = []
    try:
        from apps.risk.models import (
            ContactoCobranza as WcgContacto,
        )
        from apps.risk.models import (
            EstadoFinanciero as WcgEF,
        )
        from apps.risk.models import (
            RiskAlerta,
            RiskOperacion,
            RiskOperationSnapshot as WcgSnap,
            RiskPagoProgramado,
            RiskPagoRealizado,
        )
        from apps.risk.selectors import snapshot_summary
    except Exception as exc:
        md.append(h2("Stack WCG One Risk (`apps.risk`)"))
        md.append(p(f"_No disponible: {exc}_"))
        vacios.append(f"Stack apps.risk no importable: {exc}")
        return md, sheets, hechos, vacios

    qs = WcgSnap.objects.select_related(
        "operacion", "entidad", "operacion__unidad_negocio", "operacion__producto"
    )
    summary = snapshot_summary(qs)
    kpi_headers = ["KPI Comando Balón WCG One", "Valor"]
    kpi_rows = [
        ["Snapshots", summary["total_snapshots"]],
        ["Clientes (distintos)", summary["clientes"]],
        ["Operaciones (distintas)", summary["operaciones"]],
        ["Con mora (due_days>0)", summary["con_mora"]],
        ["Suma past_due_balance", fmt_num(summary["suma_vencido"], 2)],
    ]
    hechos.append(f"WCG One snapshots: {summary['total_snapshots']}")
    hechos.append(f"WCG One operaciones master: {RiskOperacion.objects.count()}")

    md.extend(
        [
            h2("Stack WCG One — Comando Balón KPIs (`apps.risk`)"),
            p("Equivalente a `/wcgone/risk/comando-balon/`."),
            md_table(kpi_headers, kpi_rows),
        ]
    )
    sheets.append(_sheet("WCG KPI", "KPIs WCG Risk", kpi_headers, kpi_rows))

    op_headers = [
        "Código",
        "Cliente",
        "Producto",
        "UN",
        "Contrato",
        "Asesor",
        "Moneda",
        "Inicio",
        "Monto original",
        "Estado",
        "Notas",
    ]
    op_rows = []
    for o in RiskOperacion.objects.select_related(
        "entidad", "producto", "unidad_negocio"
    ).order_by("entidad__nombre", "codigo_operacion"):
        op_rows.append(
            [
                o.codigo_operacion,
                getattr(o.entidad, "nombre", None) or getattr(o.entidad, "codigo", "") or "—",
                getattr(o.producto, "nombre", None) or getattr(o.producto, "codigo", "") or "—",
                str(o.unidad_negocio) if o.unidad_negocio else "—",
                o.contrato_numero or "",
                o.asesor or "",
                o.moneda or "",
                o.fecha_inicio.isoformat() if o.fecha_inicio else "",
                fmt_num(o.monto_original, 2) if o.monto_original is not None else "",
                o.estado or "",
                (o.notas or "")[:160],
            ]
        )
    md.extend(
        [
            h2("WCG One — maestro de operaciones"),
            p(f"Registros: **{len(op_rows)}**."),
            md_table(op_headers, op_rows) if op_rows else p("_Sin RiskOperacion._"),
        ]
    )
    sheets.append(_sheet("WCG Operaciones", "RiskOperacion", op_headers, op_rows))
    if not op_rows:
        vacios.append("Sin RiskOperacion en apps.risk.")

    snap_headers = [
        "Fecha",
        "Cliente",
        "Operación",
        "Estado op.",
        "Producto raw",
        "Capital",
        "Vencido",
        "Días atraso",
        "Renta mensual",
        "Cuotas pend.",
        "Interés",
        "Seguro",
        "Otros",
        "Opción compra",
        "Renta inicial",
        "Renta total",
        "Archivo",
    ]
    snap_rows = []
    for s in qs.order_by("-fecha_snapshot", "-due_days", "entidad__nombre"):
        snap_rows.append(
            [
                s.fecha_snapshot.isoformat() if s.fecha_snapshot else "",
                getattr(s.entidad, "nombre", None) or "—",
                s.operacion.codigo_operacion if s.operacion else "—",
                s.estado_operacion or "",
                s.producto_nombre_raw or "",
                fmt_num(s.capital_balance, 2) if s.capital_balance is not None else "",
                fmt_num(s.past_due_balance, 2) if s.past_due_balance is not None else "",
                s.due_days if s.due_days is not None else "",
                fmt_num(s.monthly_rent, 2) if s.monthly_rent is not None else "",
                fmt_num(s.outstanding_installments, 2)
                if s.outstanding_installments is not None
                else "",
                fmt_num(s.interest_balance, 2) if s.interest_balance is not None else "",
                fmt_num(s.insurance_balance, 2) if s.insurance_balance is not None else "",
                fmt_num(s.other_charges_balance, 2)
                if s.other_charges_balance is not None
                else "",
                fmt_num(s.purchase_option_value, 2)
                if s.purchase_option_value is not None
                else "",
                fmt_num(s.initial_rent_value, 2) if s.initial_rent_value is not None else "",
                fmt_num(s.total_rent_value, 2) if s.total_rent_value is not None else "",
                s.archivo_origen or "",
            ]
        )
    md.extend(
        [
            h2("WCG One — detalle completo de snapshots (browse)"),
            p(f"Registros: **{len(snap_rows)}**."),
            md_table(snap_headers, snap_rows) if snap_rows else p("_Sin snapshots WCG._"),
        ]
    )
    sheets.append(_sheet("WCG Snapshots", "apps.risk snapshots", snap_headers, snap_rows))
    if not snap_rows:
        vacios.append("Sin RiskOperationSnapshot en apps.risk.")

    ef_headers = [
        "Fecha corte",
        "Entidad",
        "Ventas",
        "Utilidad neta",
        "Activo corr.",
        "Activo no corr.",
        "Pasivo corr.",
        "Pasivo no corr.",
        "Patrimonio",
        "EBITDA",
        "Auditor",
        "Observaciones",
    ]
    ef_rows = []
    for e in WcgEF.objects.select_related("entidad").order_by(
        "-fecha_corte", "entidad__nombre"
    ):
        ef_rows.append(
            [
                e.fecha_corte.isoformat() if e.fecha_corte else "",
                getattr(e.entidad, "nombre", None) or "—",
                fmt_num(e.ventas, 2) if e.ventas is not None else "",
                fmt_num(e.utilidad_neta, 2) if e.utilidad_neta is not None else "",
                fmt_num(e.activo_corriente, 2) if e.activo_corriente is not None else "",
                fmt_num(e.activo_no_corriente, 2)
                if e.activo_no_corriente is not None
                else "",
                fmt_num(e.pasivo_corriente, 2) if e.pasivo_corriente is not None else "",
                fmt_num(e.pasivo_no_corriente, 2)
                if e.pasivo_no_corriente is not None
                else "",
                fmt_num(e.patrimonio, 2) if e.patrimonio is not None else "",
                fmt_num(e.ebitda, 2) if e.ebitda is not None else "",
                e.auditor_contador or "",
                (e.observaciones or "")[:200],
            ]
        )
    md.extend(
        [
            h2("WCG One — estados financieros (EEFF)"),
            md_table(ef_headers, ef_rows) if ef_rows else p("_Sin EEFF WCG._"),
        ]
    )
    sheets.append(_sheet("WCG EEFF", "EstadoFinanciero WCG", ef_headers, ef_rows))

    alerta_headers = [
        "Fecha",
        "Entidad",
        "Operación",
        "Tipo",
        "Severidad",
        "Activa",
        "Origen",
        "Mensaje",
    ]
    alerta_rows = []
    for a in RiskAlerta.objects.select_related("entidad", "operacion").order_by(
        "-fecha_alerta", "-id"
    ):
        alerta_rows.append(
            [
                a.fecha_alerta.isoformat() if a.fecha_alerta else "",
                getattr(a.entidad, "nombre", None) or "—",
                a.operacion.codigo_operacion if a.operacion else "—",
                a.tipo_alerta,
                a.severidad,
                "Sí" if a.activa else "No",
                a.origen or "",
                (a.mensaje or "")[:300],
            ]
        )
    md.extend(
        [
            h2("WCG One — alertas de riesgo"),
            md_table(alerta_headers, alerta_rows)
            if alerta_rows
            else p("_Sin RiskAlerta._"),
        ]
    )
    sheets.append(_sheet("WCG Alertas", "RiskAlerta", alerta_headers, alerta_rows))
    hechos.append(f"WCG One alertas: {len(alerta_rows)}")

    prog_headers = [
        "Operación",
        "Entidad",
        "Fecha prog.",
        "Capital",
        "Interés",
        "Mora",
        "Otros",
        "Moneda",
        "Estado",
    ]
    prog_rows = []
    for r in RiskPagoProgramado.objects.select_related("operacion", "entidad").order_by(
        "fecha_programada"
    ):
        prog_rows.append(
            [
                r.operacion.codigo_operacion if r.operacion else "—",
                getattr(r.entidad, "nombre", None) or "—",
                r.fecha_programada.isoformat() if r.fecha_programada else "",
                fmt_num(r.monto_capital, 2) if r.monto_capital is not None else "",
                fmt_num(r.monto_interes, 2) if r.monto_interes is not None else "",
                fmt_num(r.monto_mora, 2) if r.monto_mora is not None else "",
                fmt_num(r.monto_otros, 2) if r.monto_otros is not None else "",
                r.moneda or "",
                r.estado or "",
            ]
        )
    pago_headers = [
        "Operación",
        "Entidad",
        "Fecha pago",
        "Capital",
        "Interés",
        "Mora",
        "Otros",
        "Moneda",
        "Referencia",
    ]
    pago_rows = []
    for r in RiskPagoRealizado.objects.select_related("operacion", "entidad").order_by(
        "-fecha_pago"
    ):
        pago_rows.append(
            [
                r.operacion.codigo_operacion if r.operacion else "—",
                getattr(r.entidad, "nombre", None) or "—",
                r.fecha_pago.isoformat() if r.fecha_pago else "",
                fmt_num(r.monto_capital, 2) if r.monto_capital is not None else "",
                fmt_num(r.monto_interes, 2) if r.monto_interes is not None else "",
                fmt_num(r.monto_mora, 2) if r.monto_mora is not None else "",
                fmt_num(r.monto_otros, 2) if r.monto_otros is not None else "",
                r.moneda or "",
                r.referencia or "",
            ]
        )
    contact_headers = [
        "Fecha",
        "Entidad",
        "Operación",
        "Tipo",
        "Resultado",
        "Acuerdo",
        "Compromiso",
        "Notas",
    ]
    contact_rows = []
    for c in WcgContacto.objects.select_related("entidad", "operacion").order_by(
        "-fecha", "entidad__nombre"
    ):
        contact_rows.append(
            [
                c.fecha.isoformat() if c.fecha else "",
                getattr(c.entidad, "nombre", None) or "—",
                c.operacion.codigo_operacion if c.operacion else "—",
                c.tipo_contacto,
                c.resultado or "",
                (c.acuerdo or "")[:200],
                c.fecha_compromiso.isoformat() if c.fecha_compromiso else "",
                (c.notas or "")[:160],
            ]
        )
    md.extend(
        [
            h2("WCG One — pagos programados"),
            md_table(prog_headers, prog_rows) if prog_rows else p("_Sin pagos programados WCG._"),
            h2("WCG One — pagos realizados"),
            md_table(pago_headers, pago_rows) if pago_rows else p("_Sin pagos realizados WCG._"),
            h2("WCG One — bitácora de contactos de cobranza"),
            md_table(contact_headers, contact_rows)
            if contact_rows
            else p("_Sin contactos WCG._"),
        ]
    )
    sheets.extend(
        [
            _sheet("WCG Prog pagos", "RiskPagoProgramado", prog_headers, prog_rows),
            _sheet("WCG Pagos", "RiskPagoRealizado", pago_headers, pago_rows),
            _sheet("WCG Contactos", "ContactoCobranza WCG", contact_headers, contact_rows),
        ]
    )
    return md, sheets, hechos, vacios


def build_risk_results(cfg: ReportConfig | None = None) -> dict:
    cfg = cfg or ReportConfig.get_active()
    now = timezone.localtime()
    stamp = report_stamp(now)
    stamp_label = (
        f"Generado {now.strftime('%Y-%m-%d %H:%M')} "
        f"({timezone.get_current_timezone_name()}) ·{stamp}"
    )
    today = now.date()

    months = [
        m
        for m in (
            RiskOperationSnapshot.objects.annotate(m=TruncMonth("fecha_snapshot"))
            .values_list("m", flat=True)
            .distinct()
            .order_by("-m")
        )
        if m
    ]
    curr_p = months[0].strftime("%Y-%m") if months else None
    prev_p = months[1].strftime("%Y-%m") if len(months) > 1 else None

    def _filter_month(qs, ym: str | None):
        if not ym:
            return qs.none()
        y, m = ym.split("-")
        return qs.filter(fecha_snapshot__year=int(y), fecha_snapshot__month=int(m))

    def _kpi(ym: str | None) -> dict:
        empty = {
            "ops": 0,
            "alertas": 0,
            "saldo": Decimal("0"),
            "exigible": Decimal("0"),
            "criticos": 0,
            "altos": 0,
            "mora_prom": Decimal("0"),
        }
        if not ym:
            return empty
        qs = _filter_month(RiskOperationSnapshot.objects.all(), ym)
        n = qs.count()
        if not n:
            return empty
        agg = qs.aggregate(
            saldo=Sum("saldo"), exigible=Sum("monto_exigible"), mora=Sum("dias_mora")
        )
        return {
            "ops": n,
            "alertas": qs.filter(alerta=True).count(),
            "saldo": agg["saldo"] or Decimal("0"),
            "exigible": agg["exigible"] or Decimal("0"),
            "criticos": qs.filter(nivel_riesgo=RiskOperationSnapshot.NIVEL_CRITICO).count(),
            "altos": qs.filter(nivel_riesgo=RiskOperationSnapshot.NIVEL_ALTO).count(),
            "mora_prom": (Decimal(agg["mora"] or 0) / Decimal(n)),
        }

    curr = _kpi(curr_p)
    prev = _kpi(prev_p)
    kpi_headers = ["KPI", "Último período", "Anterior", "% Δ"]
    kpi_rows = [
        ["Operaciones", curr["ops"], prev["ops"] if prev_p else "—", pct_change(curr["ops"], prev["ops"]) if prev_p else "—"],
        ["Alertas", curr["alertas"], prev["alertas"] if prev_p else "—", pct_change(curr["alertas"], prev["alertas"]) if prev_p else "—"],
        ["Saldo", fmt_num(curr["saldo"], 2), fmt_num(prev["saldo"], 2) if prev_p else "—", pct_change(curr["saldo"], prev["saldo"]) if prev_p else "—"],
        ["Exigible", fmt_num(curr["exigible"], 2), fmt_num(prev["exigible"], 2) if prev_p else "—", pct_change(curr["exigible"], prev["exigible"]) if prev_p else "—"],
        ["Críticos", curr["criticos"], prev["criticos"] if prev_p else "—", pct_change(curr["criticos"], prev["criticos"]) if prev_p else "—"],
        ["Altos", curr["altos"], prev["altos"] if prev_p else "—", pct_change(curr["altos"], prev["altos"]) if prev_p else "—"],
        ["Mora prom. días", fmt_num(curr["mora_prom"], 1), fmt_num(prev["mora_prom"], 1) if prev_p else "—", pct_change(curr["mora_prom"], prev["mora_prom"]) if prev_p else "—"],
    ]

    # Serie mensual completa (cifras base tipo chart)
    serie_headers = [
        "Periodo",
        "Ops",
        "Alertas",
        "Saldo",
        "Exigible",
        "Críticos",
        "Altos",
        "Mora prom.",
    ]
    serie_rows = []
    for m in sorted(months):
        ym = m.strftime("%Y-%m")
        k = _kpi(ym)
        serie_rows.append(
            [
                ym,
                k["ops"],
                k["alertas"],
                fmt_num(k["saldo"], 2),
                fmt_num(k["exigible"], 2),
                k["criticos"],
                k["altos"],
                fmt_num(k["mora_prom"], 1),
            ]
        )

    # Comando Balón: último snapshot por operación
    balon_headers = [
        "Cliente",
        "Código cliente",
        "Operación",
        "UN",
        "Producto",
        "Fecha snapshot",
        "Saldo",
        "Días mora",
        "Exigible",
        "Nivel",
        "Alerta",
        "Detalle",
    ]
    balon_rows = []
    latest_dates = RiskOperationSnapshot.objects.values(
        "entidad_id", "referencia_operacion"
    ).annotate(ultima=Max("fecha_snapshot"))
    operaciones_latest = []
    for row in latest_dates.order_by("-ultima"):
        snap = (
            RiskOperationSnapshot.objects.filter(
                entidad_id=row["entidad_id"],
                referencia_operacion=row["referencia_operacion"],
                fecha_snapshot=row["ultima"],
            )
            .select_related("entidad", "entidad__unidad_negocio", "producto")
            .first()
        )
        if snap:
            operaciones_latest.append(snap)
    for s in operaciones_latest:
        un = ""
        if s.entidad and getattr(s.entidad, "unidad_negocio", None):
            un = getattr(s.entidad.unidad_negocio, "code", None) or str(
                s.entidad.unidad_negocio
            )
        elif s.producto and getattr(s.producto, "unidad_negocio", None):
            un = getattr(s.producto.unidad_negocio, "code", None) or str(
                s.producto.unidad_negocio
            )
        balon_rows.append(
            [
                getattr(s.entidad, "nombre", None) or "—",
                getattr(s.entidad, "codigo", None) or "—",
                s.referencia_operacion,
                un or "—",
                getattr(s.producto, "codigo", None)
                or getattr(s.producto, "nombre", None)
                or "—",
                s.fecha_snapshot.isoformat() if s.fecha_snapshot else "",
                fmt_num(s.saldo, 2),
                s.dias_mora,
                fmt_num(s.monto_exigible, 2),
                s.nivel_riesgo,
                "Sí" if s.alerta else "No",
                (s.detalle or "")[:200],
            ]
        )

    alertas_rows = [r for r in balon_rows if r[10] == "Sí"]
    mora_alta_rows = sorted(
        [r for r in balon_rows if isinstance(r[7], int) and r[7] >= 30],
        key=lambda x: x[7],
        reverse=True,
    )

    pagos_vencidos_headers = [
        "Entidad",
        "Referencia",
        "Fecha prog.",
        "Monto",
        "Moneda",
        "Producto",
        "Días vencido",
    ]
    pagos_vencidos_rows = []
    for r in (
        ProgramacionPago.objects.filter(fecha_programada__lt=today)
        .select_related("entidad", "producto")
        .order_by("fecha_programada")
    ):
        dias = (today - r.fecha_programada).days if r.fecha_programada else ""
        pagos_vencidos_rows.append(
            [
                getattr(r.entidad, "codigo", None) or "—",
                r.referencia,
                r.fecha_programada.isoformat() if r.fecha_programada else "",
                fmt_num(r.monto, 2),
                r.moneda,
                getattr(r.producto, "codigo", None) or "—",
                dias,
            ]
        )

    snap_headers = [
        "Fecha",
        "Periodo",
        "Entidad",
        "Producto",
        "Operación",
        "Nivel",
        "Días mora",
        "Saldo",
        "Exigible",
        "Alerta",
        "Detalle",
    ]
    snap_rows = []
    for s in (
        RiskOperationSnapshot.objects.select_related("entidad", "producto")
        .order_by("-fecha_snapshot", "entidad__codigo", "referencia_operacion")
    ):
        snap_rows.append(
            [
                s.fecha_snapshot.isoformat() if s.fecha_snapshot else "",
                _ym(s.fecha_snapshot),
                getattr(s.entidad, "codigo", None)
                or getattr(s.entidad, "nombre", "")
                or "—",
                getattr(s.producto, "codigo", None)
                or getattr(s.producto, "nombre", "")
                or "—",
                s.referencia_operacion,
                s.nivel_riesgo,
                s.dias_mora,
                fmt_num(s.saldo, 2),
                fmt_num(s.monto_exigible, 2),
                "Sí" if s.alerta else "No",
                s.detalle or "",
            ]
        )

    nivel_rows = list(
        RiskOperationSnapshot.objects.values("nivel_riesgo")
        .annotate(n=Count("id"), saldo=Sum("saldo"))
        .order_by("nivel_riesgo")
    )

    ef_headers = ["Periodo", "Entidad", "Saldo total", "Mora días", "Exposición", "Notas"]
    ef_rows = []
    for e in EstadoFinanciero.objects.select_related("entidad").order_by(
        "-periodo", "entidad__codigo"
    ):
        ef_rows.append(
            [
                e.periodo,
                getattr(e.entidad, "codigo", None) or "—",
                fmt_num(e.saldo_total, 2),
                e.mora_dias,
                fmt_num(e.exposicion, 2),
                e.notas or "",
            ]
        )

    prog_headers = ["Entidad", "Referencia", "Fecha prog.", "Monto", "Moneda", "Producto"]
    prog_rows = []
    for r in ProgramacionPago.objects.select_related("entidad", "producto").order_by(
        "fecha_programada"
    ):
        prog_rows.append(
            [
                getattr(r.entidad, "codigo", None) or "—",
                r.referencia,
                r.fecha_programada.isoformat() if r.fecha_programada else "",
                fmt_num(r.monto, 2),
                r.moneda,
                getattr(r.producto, "codigo", None) or "—",
            ]
        )

    pago_headers = ["Entidad", "Referencia", "Fecha pago", "Monto", "Moneda"]
    pago_rows = []
    for r in PagoRealizado.objects.select_related("entidad").order_by("-fecha_pago"):
        pago_rows.append(
            [
                getattr(r.entidad, "codigo", None) or "—",
                r.referencia,
                r.fecha_pago.isoformat() if r.fecha_pago else "",
                fmt_num(r.monto, 2),
                r.moneda,
            ]
        )

    contact_headers = ["Entidad", "Nombre", "Teléfono", "Email", "Activo"]
    contact_rows = []
    for c in ContactoCobranza.objects.select_related("entidad").order_by(
        "entidad__codigo", "nombre"
    ):
        contact_rows.append(
            [
                getattr(c.entidad, "codigo", None) or "—",
                c.nombre,
                c.telefono,
                c.email,
                "Sí" if c.activo else "No",
            ]
        )

    cambios = []
    if prev_p:
        for label, a, b in [
            ("Alertas", curr["alertas"], prev["alertas"]),
            ("Saldo", curr["saldo"], prev["saldo"]),
            ("Exigible", curr["exigible"], prev["exigible"]),
            ("Críticos", curr["criticos"], prev["criticos"]),
        ]:
            cambios.append(
                f"{label}: {fmt_num(b, 2) if not isinstance(b, int) else b} → "
                f"{fmt_num(a, 2) if not isinstance(a, int) else a} ({pct_change(a, b)})"
            )

    wcg_md, wcg_sheets, wcg_hechos, wcg_vacios = _wcg_risk_block()

    hechos = [
        f"Snapshots histórico: {len(snap_rows)}",
        f"Ops en Comando Balón (últimas): {len(balon_rows)}",
        f"Alertas activas (última foto): {len(alertas_rows)}",
        f"Mora ≥30 días (última foto): {len(mora_alta_rows)}",
        f"Pagos programados vencidos: {len(pagos_vencidos_rows)}",
        f"Estados financieros: {len(ef_rows)}",
        f"Programaciones pago: {len(prog_rows)}",
        f"Pagos realizados: {len(pago_rows)}",
        f"Contactos cobranza: {len(contact_rows)}",
        f"Último mes snapshot: {curr_p or 'n/d'}",
        f"Mes anterior: {prev_p or 'n/d'}",
        *wcg_hechos,
    ]
    vacios = list(wcg_vacios)
    if not snap_rows:
        vacios.append("Sin RiskOperationSnapshot productivo.")
    if not ef_rows:
        vacios.append("Sin EstadoFinanciero productivo.")
    if not prev_p:
        vacios.append("Sin mes anterior de snapshots para comparar.")

    md_parts = [
        h1("Reporte de resultados B. Riesgo (extenso)"),
        p(stamp_label),
        p(
            "Propósito: inventario detallado de riesgo para IA estratégica y Excel. "
            "CRM no se incluye."
        ),
        h2("Información usada y proceso"),
        p(RISK_EXPLAIN),
        h2("KPIs último mes vs anterior"),
        p(f"Último: **{curr_p or 'n/d'}** · Anterior: **{prev_p or 'n/d'}**"),
        md_table(kpi_headers, kpi_rows),
        h2("Serie mensual de cifras base (para tendencia / gráficos)"),
        p(
            "Agregados por mes de snapshot — equivalentes a la base numérica que "
            "soportaría charts de saldo, exigible, alertas y concentración de riesgo."
        ),
        md_table(serie_headers, serie_rows) if serie_rows else p("_Sin serie mensual._"),
        h2("Cambios relevantes"),
        bullets(cambios or ["Sin comparación de meses."]),
        h2("Comando Balón — último snapshot por operación"),
        p(
            "Misma lógica que `/risk/`: un renglón por (cliente, operación) con la "
            f"fecha de snapshot más reciente. Filas: **{len(balon_rows)}**."
        ),
        md_table(balon_headers, balon_rows) if balon_rows else p("_Sin operaciones._"),
        h2("Panel de alertas (última foto)"),
        p(f"Operaciones con `alerta=Sí`: **{len(alertas_rows)}**."),
        md_table(balon_headers, alertas_rows) if alertas_rows else p("_Sin alertas._"),
        h2("Mora alta (≥ 30 días, última foto)"),
        md_table(balon_headers, mora_alta_rows)
        if mora_alta_rows
        else p("_Sin mora ≥30 días._"),
        h2("Pagos programados vencidos"),
        md_table(pagos_vencidos_headers, pagos_vencidos_rows)
        if pagos_vencidos_rows
        else p("_Sin pagos vencidos._"),
        h2("Concentración por nivel (histórico de snapshots)"),
        md_table(
            ["Nivel", "Ops", "Saldo"],
            [[r["nivel_riesgo"], r["n"], fmt_num(r["saldo"] or 0, 2)] for r in nivel_rows],
        )
        if nivel_rows
        else p("_Sin datos._"),
        h2("Detalle completo histórico de snapshots"),
        p(f"Registros: **{len(snap_rows)}** (todas las fechas, no solo la última)."),
        md_table(snap_headers, snap_rows) if snap_rows else p("_Sin snapshots._"),
        h2("Estados financieros (productivo)"),
        p(f"Registros: **{len(ef_rows)}**."),
        md_table(ef_headers, ef_rows) if ef_rows else p("_Sin estados financieros._"),
        h2("Programación de pagos (productivo)"),
        md_table(prog_headers, prog_rows) if prog_rows else p("_Sin programaciones._"),
        h2("Pagos realizados (productivo)"),
        md_table(pago_headers, pago_rows) if pago_rows else p("_Sin pagos._"),
        h2("Contactos de cobranza (directorio productivo)"),
        md_table(contact_headers, contact_rows) if contact_rows else p("_Sin contactos._"),
        *wcg_md,
        h2("Inventario"),
        bullets(hechos),
        h2("Guía de análisis estratégico (IA)"),
        p(
            "Construye un diagnóstico de riesgo crediticio/operativo: "
            "(1) ¿mejora o empeora la mora, el saldo exigible y las alertas mes a mes?; "
            "(2) ¿dónde se concentra el riesgo (niveles ALTO/CRITICO, clientes)?; "
            "(3) ¿hay pagos vencidos o clientes sin contacto de cobranza?; "
            "(4) recomendaciones de seguimiento (priorizar críticos, regularizar "
            "programaciones, reforzar cobranza). Cita cifras. No inventes umbrales "
            "ni clasificaciones ausentes en los datos."
        ),
    ]
    if cfg.include_ai_section:
        md_parts.append(
            ai_closing(
                hechos,
                cambios[:20] if cfg.include_period_comparison else ["Comparación desactivada."],
                vacios or ["Sin vacíos críticos adicionales."],
            )
        )

    sheets = [
        _sheet("KPIs", f"KPIs {curr_p} vs {prev_p}", kpi_headers, kpi_rows),
        _sheet("Serie mensual", "Cifras base tendencia", serie_headers, serie_rows),
        _sheet("Comando Balon", "Último snapshot por op", balon_headers, balon_rows),
        _sheet("Alertas", "Ops con alerta", balon_headers, alertas_rows),
        _sheet("Mora alta", "Mora >= 30", balon_headers, mora_alta_rows),
        _sheet(
            "Pagos vencidos",
            "ProgramacionPago vencida",
            pagos_vencidos_headers,
            pagos_vencidos_rows,
        ),
        _sheet("Snapshots hist", "RiskOperationSnapshot", snap_headers, snap_rows),
        _sheet(
            "Por nivel",
            "Concentración",
            ["Nivel", "Ops", "Saldo"],
            [[r["nivel_riesgo"], r["n"], float(r["saldo"] or 0)] for r in nivel_rows],
        ),
        _sheet("Estados financieros", "EstadoFinanciero", ef_headers, ef_rows),
        _sheet("Programacion pagos", "ProgramacionPago", prog_headers, prog_rows),
        _sheet("Pagos", "PagoRealizado", pago_headers, pago_rows),
        _sheet("Contactos", "ContactoCobranza", contact_headers, contact_rows),
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

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Resultados Balón de Riesgo extensos: comando balón + detalle + WCG One."""
00002|
00003|from __future__ import annotations
00004|
00005|from decimal import Decimal
00006|
00007|from django.db.models import Count, Max, Sum
00008|from django.db.models.functions import TruncMonth
00009|from django.utils import timezone
00010|
00011|from reports.md_utils import ai_closing, bullets, h1, h2, h3, join_sections, md_table, p
00012|from reports.models import ReportConfig
00013|from reports.naming import report_stamp
00014|from reports.services.common import fmt_num, pct_change
00015|from risk.models import (
00016|    ContactoCobranza,
00017|    EstadoFinanciero,
00018|    PagoRealizado,
00019|    ProgramacionPago,
00020|    RiskOperationSnapshot,
00021|)
00022|
00023|RISK_EXPLAIN = """
00024|El **Balón de Riesgo** productivo (`/risk/`) concentra:
00025|
00026|- `RiskOperationSnapshot` — snapshot por operación (nivel, mora, saldo, exigible, alerta)
00027|- Vista **Comando Balón**: último snapshot por (entidad, referencia_operacion)
00028|- `EstadoFinanciero` — saldo/exposición/mora por entidad y período `YYYY-MM`
00029|- `ProgramacionPago` / `PagoRealizado` — agenda y pagos
00030|- `ContactoCobranza` — directorio de contactos
00031|
00032|El stack WCG One (`apps.risk`) puede coexistir con snapshots leasing ricos,
00033|estados financieros contables, alertas estructuradas y pagos desglosados.
00034|
00035|Este reporte incluye **tablero comando balón**, listados operativos, histórico
00036|completo y el detalle WCG One cuando existen datos.
00037|""".strip()
00038|
00039|
00040|def _sheet(name, title, headers, rows):
00041|    return {"name": name[:31], "title": title, "headers": headers, "rows": rows}
00042|
00043|
00044|def _ym(dt) -> str:
00045|    if not dt:
00046|        return ""
00047|    if hasattr(dt, "strftime"):
00048|        return dt.strftime("%Y-%m")
00049|    return str(dt)[:7]
00050|
00051|
00052|def _wcg_risk_block() -> tuple[list[str], list[dict], list[str], list[str]]:
00053|    md: list[str] = []
00054|    sheets: list[dict] = []
00055|    hechos: list[str] = []
00056|    vacios: list[str] = []
00057|    try:
00058|        from apps.risk.models import (
00059|            ContactoCobranza as WcgContacto,
00060|        )
00061|        from apps.risk.models import (
00062|            EstadoFinanciero as WcgEF,
00063|        )
00064|        from apps.risk.models import (
00065|            RiskAlerta,
00066|            RiskOperacion,
00067|            RiskOperationSnapshot as WcgSnap,
00068|            RiskPagoProgramado,
00069|            RiskPagoRealizado,
00070|        )
00071|        from apps.risk.selectors import snapshot_summary
00072|    except Exception as exc:
00073|        md.append(h2("Stack WCG One Risk (`apps.risk`)"))
00074|        md.append(p(f"_No disponible: {exc}_"))
00075|        vacios.append(f"Stack apps.risk no importable: {exc}")
00076|        return md, sheets, hechos, vacios
00077|
00078|    qs = WcgSnap.objects.select_related(
00079|        "operacion", "entidad", "operacion__unidad_negocio", "operacion__producto"
00080|    )
00081|    summary = snapshot_summary(qs)
00082|    kpi_headers = ["KPI Comando Balón WCG One", "Valor"]
00083|    kpi_rows = [
00084|        ["Snapshots", summary["total_snapshots"]],
00085|        ["Clientes (distintos)", summary["clientes"]],
00086|        ["Operaciones (distintas)", summary["operaciones"]],
00087|        ["Con mora (due_days>0)", summary["con_mora"]],
00088|        ["Suma past_due_balance", fmt_num(summary["suma_vencido"], 2)],
00089|    ]
00090|    hechos.append(f"WCG One snapshots: {summary['total_snapshots']}")
00091|    hechos.append(f"WCG One operaciones master: {RiskOperacion.objects.count()}")
00092|
00093|    md.extend(
00094|        [
00095|            h2("Stack WCG One — Comando Balón KPIs (`apps.risk`)"),
00096|            p("Equivalente a `/wcgone/risk/comando-balon/`."),
00097|            md_table(kpi_headers, kpi_rows),
00098|        ]
00099|    )
00100|    sheets.append(_sheet("WCG KPI", "KPIs WCG Risk", kpi_headers, kpi_rows))
00101|
00102|    op_headers = [
00103|        "Código",
00104|        "Cliente",
00105|        "Producto",
00106|        "UN",
00107|        "Contrato",
00108|        "Asesor",
00109|        "Moneda",
00110|        "Inicio",
00111|        "Monto original",
00112|        "Estado",
00113|        "Notas",
00114|    ]
00115|    op_rows = []
00116|    for o in RiskOperacion.objects.select_related(
00117|        "entidad", "producto", "unidad_negocio"
00118|    ).order_by("entidad__nombre", "codigo_operacion"):
00119|        op_rows.append(
00120|            [
00121|                o.codigo_operacion,
00122|                getattr(o.entidad, "nombre", None) or getattr(o.entidad, "codigo", "") or "—",
00123|                getattr(o.producto, "nombre", None) or getattr(o.producto, "codigo", "") or "—",
00124|                str(o.unidad_negocio) if o.unidad_negocio else "—",
00125|                o.contrato_numero or "",
00126|                o.asesor or "",
00127|                o.moneda or "",
00128|                o.fecha_inicio.isoformat() if o.fecha_inicio else "",
00129|                fmt_num(o.monto_original, 2) if o.monto_original is not None else "",
00130|                o.estado or "",
00131|                (o.notas or "")[:160],
00132|            ]
00133|        )
00134|    md.extend(
00135|        [
00136|            h2("WCG One — maestro de operaciones"),
00137|            p(f"Registros: **{len(op_rows)}**."),
00138|            md_table(op_headers, op_rows) if op_rows else p("_Sin RiskOperacion._"),
00139|        ]
00140|    )
00141|    sheets.append(_sheet("WCG Operaciones", "RiskOperacion", op_headers, op_rows))
00142|    if not op_rows:
00143|        vacios.append("Sin RiskOperacion en apps.risk.")
00144|
00145|    snap_headers = [
00146|        "Fecha",
00147|        "Cliente",
00148|        "Operación",
00149|        "Estado op.",
00150|        "Producto raw",
00151|        "Capital",
00152|        "Vencido",
00153|        "Días atraso",
00154|        "Renta mensual",
00155|        "Cuotas pend.",
00156|        "Interés",
00157|        "Seguro",
00158|        "Otros",
00159|        "Opción compra",
00160|        "Renta inicial",
00161|        "Renta total",
00162|        "Archivo",
00163|    ]
00164|    snap_rows = []
00165|    for s in qs.order_by("-fecha_snapshot", "-due_days", "entidad__nombre"):
00166|        snap_rows.append(
00167|            [
00168|                s.fecha_snapshot.isoformat() if s.fecha_snapshot else "",
00169|                getattr(s.entidad, "nombre", None) or "—",
00170|                s.operacion.codigo_operacion if s.operacion else "—",
00171|                s.estado_operacion or "",
00172|                s.producto_nombre_raw or "",
00173|                fmt_num(s.capital_balance, 2) if s.capital_balance is not None else "",
00174|                fmt_num(s.past_due_balance, 2) if s.past_due_balance is not None else "",
00175|                s.due_days if s.due_days is not None else "",
00176|                fmt_num(s.monthly_rent, 2) if s.monthly_rent is not None else "",
00177|                fmt_num(s.outstanding_installments, 2)
00178|                if s.outstanding_installments is not None
00179|                else "",
00180|                fmt_num(s.interest_balance, 2) if s.interest_balance is not None else "",
00181|                fmt_num(s.insurance_balance, 2) if s.insurance_balance is not None else "",
00182|                fmt_num(s.other_charges_balance, 2)
00183|                if s.other_charges_balance is not None
00184|                else "",
00185|                fmt_num(s.purchase_option_value, 2)
00186|                if s.purchase_option_value is not None
00187|                else "",
00188|                fmt_num(s.initial_rent_value, 2) if s.initial_rent_value is not None else "",
00189|                fmt_num(s.total_rent_value, 2) if s.total_rent_value is not None else "",
00190|                s.archivo_origen or "",
00191|            ]
00192|        )
00193|    md.extend(
00194|        [
00195|            h2("WCG One — detalle completo de snapshots (browse)"),
00196|            p(f"Registros: **{len(snap_rows)}**."),
00197|            md_table(snap_headers, snap_rows) if snap_rows else p("_Sin snapshots WCG._"),
00198|        ]
00199|    )
00200|    sheets.append(_sheet("WCG Snapshots", "apps.risk snapshots", snap_headers, snap_rows))
00201|    if not snap_rows:
00202|        vacios.append("Sin RiskOperationSnapshot en apps.risk.")
00203|
00204|    ef_headers = [
00205|        "Fecha corte",
00206|        "Entidad",
00207|        "Ventas",
00208|        "Utilidad neta",
00209|        "Activo corr.",
00210|        "Activo no corr.",
00211|        "Pasivo corr.",
00212|        "Pasivo no corr.",
00213|        "Patrimonio",
00214|        "EBITDA",
00215|        "Auditor",
00216|        "Observaciones",
00217|    ]
00218|    ef_rows = []
00219|    for e in WcgEF.objects.select_related("entidad").order_by(
00220|        "-fecha_corte", "entidad__nombre"
00221|    ):
00222|        ef_rows.append(
00223|            [
00224|                e.fecha_corte.isoformat() if e.fecha_corte else "",
00225|                getattr(e.entidad, "nombre", None) or "—",
00226|                fmt_num(e.ventas, 2) if e.ventas is not None else "",
00227|                fmt_num(e.utilidad_neta, 2) if e.utilidad_neta is not None else "",
00228|                fmt_num(e.activo_corriente, 2) if e.activo_corriente is not None else "",
00229|                fmt_num(e.activo_no_corriente, 2)
00230|                if e.activo_no_corriente is not None
00231|                else "",
00232|                fmt_num(e.pasivo_corriente, 2) if e.pasivo_corriente is not None else "",
00233|                fmt_num(e.pasivo_no_corriente, 2)
00234|                if e.pasivo_no_corriente is not None
00235|                else "",
00236|                fmt_num(e.patrimonio, 2) if e.patrimonio is not None else "",
00237|                fmt_num(e.ebitda, 2) if e.ebitda is not None else "",
00238|                e.auditor_contador or "",
00239|                (e.observaciones or "")[:200],
00240|            ]
00241|        )
00242|    md.extend(
00243|        [
00244|            h2("WCG One — estados financieros (EEFF)"),
00245|            md_table(ef_headers, ef_rows) if ef_rows else p("_Sin EEFF WCG._"),
00246|        ]
00247|    )
00248|    sheets.append(_sheet("WCG EEFF", "EstadoFinanciero WCG", ef_headers, ef_rows))
00249|
00250|    alerta_headers = [
00251|        "Fecha",
00252|        "Entidad",
00253|        "Operación",
00254|        "Tipo",
00255|        "Severidad",
00256|        "Activa",
00257|        "Origen",
00258|        "Mensaje",
00259|    ]
00260|    alerta_rows = []
00261|    for a in RiskAlerta.objects.select_related("entidad", "operacion").order_by(
00262|        "-fecha_alerta", "-id"
00263|    ):
00264|        alerta_rows.append(
00265|            [
00266|                a.fecha_alerta.isoformat() if a.fecha_alerta else "",
00267|                getattr(a.entidad, "nombre", None) or "—",
00268|                a.operacion.codigo_operacion if a.operacion else "—",
00269|                a.tipo_alerta,
00270|                a.severidad,
00271|                "Sí" if a.activa else "No",
00272|                a.origen or "",
00273|                (a.mensaje or "")[:300],
00274|            ]
00275|        )
00276|    md.extend(
00277|        [
00278|            h2("WCG One — alertas de riesgo"),
00279|            md_table(alerta_headers, alerta_rows)
00280|            if alerta_rows
00281|            else p("_Sin RiskAlerta._"),
00282|        ]
00283|    )
00284|    sheets.append(_sheet("WCG Alertas", "RiskAlerta", alerta_headers, alerta_rows))
00285|    hechos.append(f"WCG One alertas: {len(alerta_rows)}")
00286|
00287|    prog_headers = [
00288|        "Operación",
00289|        "Entidad",
00290|        "Fecha prog.",
00291|        "Capital",
00292|        "Interés",
00293|        "Mora",
00294|        "Otros",
00295|        "Moneda",
00296|        "Estado",
00297|    ]
00298|    prog_rows = []
00299|    for r in RiskPagoProgramado.objects.select_related("operacion", "entidad").order_by(
00300|        "fecha_programada"
00301|    ):
00302|        prog_rows.append(
00303|            [
00304|                r.operacion.codigo_operacion if r.operacion else "—",
00305|                getattr(r.entidad, "nombre", None) or "—",
00306|                r.fecha_programada.isoformat() if r.fecha_programada else "",
00307|                fmt_num(r.monto_capital, 2) if r.monto_capital is not None else "",
00308|                fmt_num(r.monto_interes, 2) if r.monto_interes is not None else "",
00309|                fmt_num(r.monto_mora, 2) if r.monto_mora is not None else "",
00310|                fmt_num(r.monto_otros, 2) if r.monto_otros is not None else "",
00311|                r.moneda or "",
00312|                r.estado or "",
00313|            ]
00314|        )
00315|    pago_headers = [
00316|        "Operación",
00317|        "Entidad",
00318|        "Fecha pago",
00319|        "Capital",
00320|        "Interés",
00321|        "Mora",
00322|        "Otros",
00323|        "Moneda",
00324|        "Referencia",
00325|    ]
00326|    pago_rows = []
00327|    for r in RiskPagoRealizado.objects.select_related("operacion", "entidad").order_by(
00328|        "-fecha_pago"
00329|    ):
00330|        pago_rows.append(
00331|            [
00332|                r.operacion.codigo_operacion if r.operacion else "—",
00333|                getattr(r.entidad, "nombre", None) or "—",
00334|                r.fecha_pago.isoformat() if r.fecha_pago else "",
00335|                fmt_num(r.monto_capital, 2) if r.monto_capital is not None else "",
00336|                fmt_num(r.monto_interes, 2) if r.monto_interes is not None else "",
00337|                fmt_num(r.monto_mora, 2) if r.monto_mora is not None else "",
00338|                fmt_num(r.monto_otros, 2) if r.monto_otros is not None else "",
00339|                r.moneda or "",
00340|                r.referencia or "",
00341|            ]
00342|        )
00343|    contact_headers = [
00344|        "Fecha",
00345|        "Entidad",
00346|        "Operación",
00347|        "Tipo",
00348|        "Resultado",
00349|        "Acuerdo",
00350|        "Compromiso",
00351|        "Notas",
00352|    ]
00353|    contact_rows = []
00354|    for c in WcgContacto.objects.select_related("entidad", "operacion").order_by(
00355|        "-fecha", "entidad__nombre"
00356|    ):
00357|        contact_rows.append(
00358|            [
00359|                c.fecha.isoformat() if c.fecha else "",
00360|                getattr(c.entidad, "nombre", None) or "—",
00361|                c.operacion.codigo_operacion if c.operacion else "—",
00362|                c.tipo_contacto,
00363|                c.resultado or "",
00364|                (c.acuerdo or "")[:200],
00365|                c.fecha_compromiso.isoformat() if c.fecha_compromiso else "",
00366|                (c.notas or "")[:160],
00367|            ]
00368|        )
00369|    md.extend(
00370|        [
00371|            h2("WCG One — pagos programados"),
00372|            md_table(prog_headers, prog_rows) if prog_rows else p("_Sin pagos programados WCG._"),
00373|            h2("WCG One — pagos realizados"),
00374|            md_table(pago_headers, pago_rows) if pago_rows else p("_Sin pagos realizados WCG._"),
00375|            h2("WCG One — bitácora de contactos de cobranza"),
00376|            md_table(contact_headers, contact_rows)
00377|            if contact_rows
00378|            else p("_Sin contactos WCG._"),
00379|        ]
00380|    )
00381|    sheets.extend(
00382|        [
00383|            _sheet("WCG Prog pagos", "RiskPagoProgramado", prog_headers, prog_rows),
00384|            _sheet("WCG Pagos", "RiskPagoRealizado", pago_headers, pago_rows),
00385|            _sheet("WCG Contactos", "ContactoCobranza WCG", contact_headers, contact_rows),
00386|        ]
00387|    )
00388|    return md, sheets, hechos, vacios
00389|
00390|
00391|def build_risk_results(cfg: ReportConfig | None = None) -> dict:
00392|    cfg = cfg or ReportConfig.get_active()
00393|    now = timezone.localtime()
00394|    stamp = report_stamp(now)
00395|    stamp_label = (
00396|        f"Generado {now.strftime('%Y-%m-%d %H:%M')} "
00397|        f"({timezone.get_current_timezone_name()}) ·{stamp}"
00398|    )
00399|    today = now.date()
00400|
00401|    months = [
00402|        m
00403|        for m in (
00404|            RiskOperationSnapshot.objects.annotate(m=TruncMonth("fecha_snapshot"))
00405|            .values_list("m", flat=True)
00406|            .distinct()
00407|            .order_by("-m")
00408|        )
00409|        if m
00410|    ]
00411|    curr_p = months[0].strftime("%Y-%m") if months else None
00412|    prev_p = months[1].strftime("%Y-%m") if len(months) > 1 else None
00413|
00414|    def _filter_month(qs, ym: str | None):
00415|        if not ym:
00416|            return qs.none()
00417|        y, m = ym.split("-")
00418|        return qs.filter(fecha_snapshot__year=int(y), fecha_snapshot__month=int(m))
00419|
00420|    def _kpi(ym: str | None) -> dict:
00421|        empty = {
00422|            "ops": 0,
00423|            "alertas": 0,
00424|            "saldo": Decimal("0"),
00425|            "exigible": Decimal("0"),
00426|            "criticos": 0,
00427|            "altos": 0,
00428|            "mora_prom": Decimal("0"),
00429|        }
00430|        if not ym:
00431|            return empty
00432|        qs = _filter_month(RiskOperationSnapshot.objects.all(), ym)
00433|        n = qs.count()
00434|        if not n:
00435|            return empty
00436|        agg = qs.aggregate(
00437|            saldo=Sum("saldo"), exigible=Sum("monto_exigible"), mora=Sum("dias_mora")
00438|        )
00439|        return {
00440|            "ops": n,
00441|            "alertas": qs.filter(alerta=True).count(),
00442|            "saldo": agg["saldo"] or Decimal("0"),
00443|            "exigible": agg["exigible"] or Decimal("0"),
00444|            "criticos": qs.filter(nivel_riesgo=RiskOperationSnapshot.NIVEL_CRITICO).count(),
00445|            "altos": qs.filter(nivel_riesgo=RiskOperationSnapshot.NIVEL_ALTO).count(),
00446|            "mora_prom": (Decimal(agg["mora"] or 0) / Decimal(n)),
00447|        }
00448|
00449|    curr = _kpi(curr_p)
00450|    prev = _kpi(prev_p)
00451|    kpi_headers = ["KPI", "Último período", "Anterior", "% Δ"]
00452|    kpi_rows = [
00453|        ["Operaciones", curr["ops"], prev["ops"] if prev_p else "—", pct_change(curr["ops"], prev["ops"]) if prev_p else "—"],
00454|        ["Alertas", curr["alertas"], prev["alertas"] if prev_p else "—", pct_change(curr["alertas"], prev["alertas"]) if prev_p else "—"],
00455|        ["Saldo", fmt_num(curr["saldo"], 2), fmt_num(prev["saldo"], 2) if prev_p else "—", pct_change(curr["saldo"], prev["saldo"]) if prev_p else "—"],
00456|        ["Exigible", fmt_num(curr["exigible"], 2), fmt_num(prev["exigible"], 2) if prev_p else "—", pct_change(curr["exigible"], prev["exigible"]) if prev_p else "—"],
00457|        ["Críticos", curr["criticos"], prev["criticos"] if prev_p else "—", pct_change(curr["criticos"], prev["criticos"]) if prev_p else "—"],
00458|        ["Altos", curr["altos"], prev["altos"] if prev_p else "—", pct_change(curr["altos"], prev["altos"]) if prev_p else "—"],
00459|        ["Mora prom. días", fmt_num(curr["mora_prom"], 1), fmt_num(prev["mora_prom"], 1) if prev_p else "—", pct_change(curr["mora_prom"], prev["mora_prom"]) if prev_p else "—"],
00460|    ]
00461|
00462|    # Serie mensual completa (cifras base tipo chart)
00463|    serie_headers = [
00464|        "Periodo",
00465|        "Ops",
00466|        "Alertas",
00467|        "Saldo",
00468|        "Exigible",
00469|        "Críticos",
00470|        "Altos",
00471|        "Mora prom.",
00472|    ]
00473|    serie_rows = []
00474|    for m in sorted(months):
00475|        ym = m.strftime("%Y-%m")
00476|        k = _kpi(ym)
00477|        serie_rows.append(
00478|            [
00479|                ym,
00480|                k["ops"],
00481|                k["alertas"],
00482|                fmt_num(k["saldo"], 2),
00483|                fmt_num(k["exigible"], 2),
00484|                k["criticos"],
00485|                k["altos"],
00486|                fmt_num(k["mora_prom"], 1),
00487|            ]
00488|        )
00489|
00490|    # Comando Balón: último snapshot por operación
00491|    balon_headers = [
00492|        "Cliente",
00493|        "Código cliente",
00494|        "Operación",
00495|        "UN",
00496|        "Producto",
00497|        "Fecha snapshot",
00498|        "Saldo",
00499|        "Días mora",
00500|        "Exigible",
00501|        "Nivel",
00502|        "Alerta",
00503|        "Detalle",
00504|    ]
00505|    balon_rows = []
00506|    latest_dates = RiskOperationSnapshot.objects.values(
00507|        "entidad_id", "referencia_operacion"
00508|    ).annotate(ultima=Max("fecha_snapshot"))
00509|    operaciones_latest = []
00510|    for row in latest_dates.order_by("-ultima"):
00511|        snap = (
00512|            RiskOperationSnapshot.objects.filter(
00513|                entidad_id=row["entidad_id"],
00514|                referencia_operacion=row["referencia_operacion"],
00515|                fecha_snapshot=row["ultima"],
00516|            )
00517|            .select_related("entidad", "entidad__unidad_negocio", "producto")
00518|            .first()
00519|        )
00520|        if snap:
00521|            operaciones_latest.append(snap)
00522|    for s in operaciones_latest:
00523|        un = ""
00524|        if s.entidad and getattr(s.entidad, "unidad_negocio", None):
00525|            un = getattr(s.entidad.unidad_negocio, "code", None) or str(
00526|                s.entidad.unidad_negocio
00527|            )
00528|        elif s.producto and getattr(s.producto, "unidad_negocio", None):
00529|            un = getattr(s.producto.unidad_negocio, "code", None) or str(
00530|                s.producto.unidad_negocio
00531|            )
00532|        balon_rows.append(
00533|            [
00534|                getattr(s.entidad, "nombre", None) or "—",
00535|                getattr(s.entidad, "codigo", None) or "—",
00536|                s.referencia_operacion,
00537|                un or "—",
00538|                getattr(s.producto, "codigo", None)
00539|                or getattr(s.producto, "nombre", None)
00540|                or "—",
00541|                s.fecha_snapshot.isoformat() if s.fecha_snapshot else "",
00542|                fmt_num(s.saldo, 2),
00543|                s.dias_mora,
00544|                fmt_num(s.monto_exigible, 2),
00545|                s.nivel_riesgo,
00546|                "Sí" if s.alerta else "No",
00547|                (s.detalle or "")[:200],
00548|            ]
00549|        )
00550|
00551|    alertas_rows = [r for r in balon_rows if r[10] == "Sí"]
00552|    mora_alta_rows = sorted(
00553|        [r for r in balon_rows if isinstance(r[7], int) and r[7] >= 30],
00554|        key=lambda x: x[7],
00555|        reverse=True,
00556|    )
00557|
00558|    pagos_vencidos_headers = [
00559|        "Entidad",
00560|        "Referencia",
00561|        "Fecha prog.",
00562|        "Monto",
00563|        "Moneda",
00564|        "Producto",
00565|        "Días vencido",
00566|    ]
00567|    pagos_vencidos_rows = []
00568|    for r in (
00569|        ProgramacionPago.objects.filter(fecha_programada__lt=today)
00570|        .select_related("entidad", "producto")
00571|        .order_by("fecha_programada")
00572|    ):
00573|        dias = (today - r.fecha_programada).days if r.fecha_programada else ""
00574|        pagos_vencidos_rows.append(
00575|            [
00576|                getattr(r.entidad, "codigo", None) or "—",
00577|                r.referencia,
00578|                r.fecha_programada.isoformat() if r.fecha_programada else "",
00579|                fmt_num(r.monto, 2),
00580|                r.moneda,
00581|                getattr(r.producto, "codigo", None) or "—",
00582|                dias,
00583|            ]
00584|        )
00585|
00586|    snap_headers = [
00587|        "Fecha",
00588|        "Periodo",
00589|        "Entidad",
00590|        "Producto",
00591|        "Operación",
00592|        "Nivel",
00593|        "Días mora",
00594|        "Saldo",
00595|        "Exigible",
00596|        "Alerta",
00597|        "Detalle",
00598|    ]
00599|    snap_rows = []
00600|    for s in (
00601|        RiskOperationSnapshot.objects.select_related("entidad", "producto")
00602|        .order_by("-fecha_snapshot", "entidad__codigo", "referencia_operacion")
00603|    ):
00604|        snap_rows.append(
00605|            [
00606|                s.fecha_snapshot.isoformat() if s.fecha_snapshot else "",
00607|                _ym(s.fecha_snapshot),
00608|                getattr(s.entidad, "codigo", None)
00609|                or getattr(s.entidad, "nombre", "")
00610|                or "—",
00611|                getattr(s.producto, "codigo", None)
00612|                or getattr(s.producto, "nombre", "")
00613|                or "—",
00614|                s.referencia_operacion,
00615|                s.nivel_riesgo,
00616|                s.dias_mora,
00617|                fmt_num(s.saldo, 2),
00618|                fmt_num(s.monto_exigible, 2),
00619|                "Sí" if s.alerta else "No",
00620|                s.detalle or "",
00621|            ]
00622|        )
00623|
00624|    nivel_rows = list(
00625|        RiskOperationSnapshot.objects.values("nivel_riesgo")
00626|        .annotate(n=Count("id"), saldo=Sum("saldo"))
00627|        .order_by("nivel_riesgo")
00628|    )
00629|
00630|    ef_headers = ["Periodo", "Entidad", "Saldo total", "Mora días", "Exposición", "Notas"]
00631|    ef_rows = []
00632|    for e in EstadoFinanciero.objects.select_related("entidad").order_by(
00633|        "-periodo", "entidad__codigo"
00634|    ):
00635|        ef_rows.append(
00636|            [
00637|                e.periodo,
00638|                getattr(e.entidad, "codigo", None) or "—",
00639|                fmt_num(e.saldo_total, 2),
00640|                e.mora_dias,
00641|                fmt_num(e.exposicion, 2),
00642|                e.notas or "",
00643|            ]
00644|        )
00645|
00646|    prog_headers = ["Entidad", "Referencia", "Fecha prog.", "Monto", "Moneda", "Producto"]
00647|    prog_rows = []
00648|    for r in ProgramacionPago.objects.select_related("entidad", "producto").order_by(
00649|        "fecha_programada"
00650|    ):
00651|        prog_rows.append(
00652|            [
00653|                getattr(r.entidad, "codigo", None) or "—",
00654|                r.referencia,
00655|                r.fecha_programada.isoformat() if r.fecha_programada else "",
00656|                fmt_num(r.monto, 2),
00657|                r.moneda,
00658|                getattr(r.producto, "codigo", None) or "—",
00659|            ]
00660|        )
00661|
00662|    pago_headers = ["Entidad", "Referencia", "Fecha pago", "Monto", "Moneda"]
00663|    pago_rows = []
00664|    for r in PagoRealizado.objects.select_related("entidad").order_by("-fecha_pago"):
00665|        pago_rows.append(
00666|            [
00667|                getattr(r.entidad, "codigo", None) or "—",
00668|                r.referencia,
00669|                r.fecha_pago.isoformat() if r.fecha_pago else "",
00670|                fmt_num(r.monto, 2),
00671|                r.moneda,
00672|            ]
00673|        )
00674|
00675|    contact_headers = ["Entidad", "Nombre", "Teléfono", "Email", "Activo"]
00676|    contact_rows = []
00677|    for c in ContactoCobranza.objects.select_related("entidad").order_by(
00678|        "entidad__codigo", "nombre"
00679|    ):
00680|        contact_rows.append(
00681|            [
00682|                getattr(c.entidad, "codigo", None) or "—",
00683|                c.nombre,
00684|                c.telefono,
00685|                c.email,
00686|                "Sí" if c.activo else "No",
00687|            ]
00688|        )
00689|
00690|    cambios = []
00691|    if prev_p:
00692|        for label, a, b in [
00693|            ("Alertas", curr["alertas"], prev["alertas"]),
00694|            ("Saldo", curr["saldo"], prev["saldo"]),
00695|            ("Exigible", curr["exigible"], prev["exigible"]),
00696|            ("Críticos", curr["criticos"], prev["criticos"]),
00697|        ]:
00698|            cambios.append(
00699|                f"{label}: {fmt_num(b, 2) if not isinstance(b, int) else b} → "
00700|                f"{fmt_num(a, 2) if not isinstance(a, int) else a} ({pct_change(a, b)})"
00701|            )
00702|
00703|    wcg_md, wcg_sheets, wcg_hechos, wcg_vacios = _wcg_risk_block()
00704|
00705|    hechos = [
00706|        f"Snapshots histórico: {len(snap_rows)}",
00707|        f"Ops en Comando Balón (últimas): {len(balon_rows)}",
00708|        f"Alertas activas (última foto): {len(alertas_rows)}",
00709|        f"Mora ≥30 días (última foto): {len(mora_alta_rows)}",
00710|        f"Pagos programados vencidos: {len(pagos_vencidos_rows)}",
00711|        f"Estados financieros: {len(ef_rows)}",
00712|        f"Programaciones pago: {len(prog_rows)}",
00713|        f"Pagos realizados: {len(pago_rows)}",
00714|        f"Contactos cobranza: {len(contact_rows)}",
00715|        f"Último mes snapshot: {curr_p or 'n/d'}",
00716|        f"Mes anterior: {prev_p or 'n/d'}",
00717|        *wcg_hechos,
00718|    ]
00719|    vacios = list(wcg_vacios)
00720|    if not snap_rows:
00721|        vacios.append("Sin RiskOperationSnapshot productivo.")
00722|    if not ef_rows:
00723|        vacios.append("Sin EstadoFinanciero productivo.")
00724|    if not prev_p:
00725|        vacios.append("Sin mes anterior de snapshots para comparar.")
00726|
00727|    md_parts = [
00728|        h1("Reporte de resultados B. Riesgo (extenso)"),
00729|        p(stamp_label),
00730|        p(
00731|            "Propósito: inventario detallado de riesgo para IA estratégica y Excel. "
00732|            "CRM no se incluye."
00733|        ),
00734|        h2("Información usada y proceso"),
00735|        p(RISK_EXPLAIN),
00736|        h2("KPIs último mes vs anterior"),
00737|        p(f"Último: **{curr_p or 'n/d'}** · Anterior: **{prev_p or 'n/d'}**"),
00738|        md_table(kpi_headers, kpi_rows),
00739|        h2("Serie mensual de cifras base (para tendencia / gráficos)"),
00740|        p(
00741|            "Agregados por mes de snapshot — equivalentes a la base numérica que "
00742|            "soportaría charts de saldo, exigible, alertas y concentración de riesgo."
00743|        ),
00744|        md_table(serie_headers, serie_rows) if serie_rows else p("_Sin serie mensual._"),
00745|        h2("Cambios relevantes"),
00746|        bullets(cambios or ["Sin comparación de meses."]),
00747|        h2("Comando Balón — último snapshot por operación"),
00748|        p(
00749|            "Misma lógica que `/risk/`: un renglón por (cliente, operación) con la "
00750|            f"fecha de snapshot más reciente. Filas: **{len(balon_rows)}**."
00751|        ),
00752|        md_table(balon_headers, balon_rows) if balon_rows else p("_Sin operaciones._"),
00753|        h2("Panel de alertas (última foto)"),
00754|        p(f"Operaciones con `alerta=Sí`: **{len(alertas_rows)}**."),
00755|        md_table(balon_headers, alertas_rows) if alertas_rows else p("_Sin alertas._"),
00756|        h2("Mora alta (≥ 30 días, última foto)"),
00757|        md_table(balon_headers, mora_alta_rows)
00758|        if mora_alta_rows
00759|        else p("_Sin mora ≥30 días._"),
00760|        h2("Pagos programados vencidos"),
00761|        md_table(pagos_vencidos_headers, pagos_vencidos_rows)
00762|        if pagos_vencidos_rows
00763|        else p("_Sin pagos vencidos._"),
00764|        h2("Concentración por nivel (histórico de snapshots)"),
00765|        md_table(
00766|            ["Nivel", "Ops", "Saldo"],
00767|            [[r["nivel_riesgo"], r["n"], fmt_num(r["saldo"] or 0, 2)] for r in nivel_rows],
00768|        )
00769|        if nivel_rows
00770|        else p("_Sin datos._"),
00771|        h2("Detalle completo histórico de snapshots"),
00772|        p(f"Registros: **{len(snap_rows)}** (todas las fechas, no solo la última)."),
00773|        md_table(snap_headers, snap_rows) if snap_rows else p("_Sin snapshots._"),
00774|        h2("Estados financieros (productivo)"),
00775|        p(f"Registros: **{len(ef_rows)}**."),
00776|        md_table(ef_headers, ef_rows) if ef_rows else p("_Sin estados financieros._"),
00777|        h2("Programación de pagos (productivo)"),
00778|        md_table(prog_headers, prog_rows) if prog_rows else p("_Sin programaciones._"),
00779|        h2("Pagos realizados (productivo)"),
00780|        md_table(pago_headers, pago_rows) if pago_rows else p("_Sin pagos._"),
00781|        h2("Contactos de cobranza (directorio productivo)"),
00782|        md_table(contact_headers, contact_rows) if contact_rows else p("_Sin contactos._"),
00783|        *wcg_md,
00784|        h2("Inventario"),
00785|        bullets(hechos),
00786|        h2("Guía de análisis estratégico (IA)"),
00787|        p(
00788|            "Construye un diagnóstico de riesgo crediticio/operativo: "
00789|            "(1) ¿mejora o empeora la mora, el saldo exigible y las alertas mes a mes?; "
00790|            "(2) ¿dónde se concentra el riesgo (niveles ALTO/CRITICO, clientes)?; "
00791|            "(3) ¿hay pagos vencidos o clientes sin contacto de cobranza?; "
00792|            "(4) recomendaciones de seguimiento (priorizar críticos, regularizar "
00793|            "programaciones, reforzar cobranza). Cita cifras. No inventes umbrales "
00794|            "ni clasificaciones ausentes en los datos."
00795|        ),
00796|    ]
00797|    if cfg.include_ai_section:
00798|        md_parts.append(
00799|            ai_closing(
00800|                hechos,
00801|                cambios[:20] if cfg.include_period_comparison else ["Comparación desactivada."],
00802|                vacios or ["Sin vacíos críticos adicionales."],
00803|            )
00804|        )
00805|
00806|    sheets = [
00807|        _sheet("KPIs", f"KPIs {curr_p} vs {prev_p}", kpi_headers, kpi_rows),
00808|        _sheet("Serie mensual", "Cifras base tendencia", serie_headers, serie_rows),
00809|        _sheet("Comando Balon", "Último snapshot por op", balon_headers, balon_rows),
00810|        _sheet("Alertas", "Ops con alerta", balon_headers, alertas_rows),
00811|        _sheet("Mora alta", "Mora >= 30", balon_headers, mora_alta_rows),
00812|        _sheet(
00813|            "Pagos vencidos",
00814|            "ProgramacionPago vencida",
00815|            pagos_vencidos_headers,
00816|            pagos_vencidos_rows,
00817|        ),
00818|        _sheet("Snapshots hist", "RiskOperationSnapshot", snap_headers, snap_rows),
00819|        _sheet(
00820|            "Por nivel",
00821|            "Concentración",
00822|            ["Nivel", "Ops", "Saldo"],
00823|            [[r["nivel_riesgo"], r["n"], float(r["saldo"] or 0)] for r in nivel_rows],
00824|        ),
00825|        _sheet("Estados financieros", "EstadoFinanciero", ef_headers, ef_rows),
00826|        _sheet("Programacion pagos", "ProgramacionPago", prog_headers, prog_rows),
00827|        _sheet("Pagos", "PagoRealizado", pago_headers, pago_rows),
00828|        _sheet("Contactos", "ContactoCobranza", contact_headers, contact_rows),
00829|        *wcg_sheets,
00830|    ]
00831|
00832|    return {
00833|        "md": join_sections(*md_parts),
00834|        "sheets": sheets,
00835|        "stamp": stamp,
00836|        "stamp_label": stamp_label,
00837|        "period": curr_p,
00838|        "prev_period": prev_p,
00839|    }

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiUmVzdWx0YWRvcyBCYWzDs24gZGUgUmllc2dvIGV4dGVuc29zOiBjb21hbmRvIGJhbMOzbiArIGRldGFsbGUgKyBXQ0cgT25lLiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsCgpmcm9tIGRqYW5nby5kYi5tb2RlbHMgaW1wb3J0IENvdW50LCBNYXgsIFN1bQpmcm9tIGRqYW5nby5kYi5tb2RlbHMuZnVuY3Rpb25zIGltcG9ydCBUcnVuY01vbnRoCmZyb20gZGphbmdvLnV0aWxzIGltcG9ydCB0aW1lem9uZQoKZnJvbSByZXBvcnRzLm1kX3V0aWxzIGltcG9ydCBhaV9jbG9zaW5nLCBidWxsZXRzLCBoMSwgaDIsIGgzLCBqb2luX3NlY3Rpb25zLCBtZF90YWJsZSwgcApmcm9tIHJlcG9ydHMubW9kZWxzIGltcG9ydCBSZXBvcnRDb25maWcKZnJvbSByZXBvcnRzLm5hbWluZyBpbXBvcnQgcmVwb3J0X3N0YW1wCmZyb20gcmVwb3J0cy5zZXJ2aWNlcy5jb21tb24gaW1wb3J0IGZtdF9udW0sIHBjdF9jaGFuZ2UKZnJvbSByaXNrLm1vZGVscyBpbXBvcnQgKAogICAgQ29udGFjdG9Db2JyYW56YSwKICAgIEVzdGFkb0ZpbmFuY2llcm8sCiAgICBQYWdvUmVhbGl6YWRvLAogICAgUHJvZ3JhbWFjaW9uUGFnbywKICAgIFJpc2tPcGVyYXRpb25TbmFwc2hvdCwKKQoKUklTS19FWFBMQUlOID0gIiIiCkVsICoqQmFsw7NuIGRlIFJpZXNnbyoqIHByb2R1Y3Rpdm8gKGAvcmlzay9gKSBjb25jZW50cmE6CgotIGBSaXNrT3BlcmF0aW9uU25hcHNob3RgIOKAlCBzbmFwc2hvdCBwb3Igb3BlcmFjacOzbiAobml2ZWwsIG1vcmEsIHNhbGRvLCBleGlnaWJsZSwgYWxlcnRhKQotIFZpc3RhICoqQ29tYW5kbyBCYWzDs24qKjogw7psdGltbyBzbmFwc2hvdCBwb3IgKGVudGlkYWQsIHJlZmVyZW5jaWFfb3BlcmFjaW9uKQotIGBFc3RhZG9GaW5hbmNpZXJvYCDigJQgc2FsZG8vZXhwb3NpY2nDs24vbW9yYSBwb3IgZW50aWRhZCB5IHBlcsOtb2RvIGBZWVlZLU1NYAotIGBQcm9ncmFtYWNpb25QYWdvYCAvIGBQYWdvUmVhbGl6YWRvYCDigJQgYWdlbmRhIHkgcGFnb3MKLSBgQ29udGFjdG9Db2JyYW56YWAg4oCUIGRpcmVjdG9yaW8gZGUgY29udGFjdG9zCgpFbCBzdGFjayBXQ0cgT25lIChgYXBwcy5yaXNrYCkgcHVlZGUgY29leGlzdGlyIGNvbiBzbmFwc2hvdHMgbGVhc2luZyByaWNvcywKZXN0YWRvcyBmaW5hbmNpZXJvcyBjb250YWJsZXMsIGFsZXJ0YXMgZXN0cnVjdHVyYWRhcyB5IHBhZ29zIGRlc2dsb3NhZG9zLgoKRXN0ZSByZXBvcnRlIGluY2x1eWUgKip0YWJsZXJvIGNvbWFuZG8gYmFsw7NuKiosIGxpc3RhZG9zIG9wZXJhdGl2b3MsIGhpc3TDs3JpY28KY29tcGxldG8geSBlbCBkZXRhbGxlIFdDRyBPbmUgY3VhbmRvIGV4aXN0ZW4gZGF0b3MuCiIiIi5zdHJpcCgpCgoKZGVmIF9zaGVldChuYW1lLCB0aXRsZSwgaGVhZGVycywgcm93cyk6CiAgICByZXR1cm4geyJuYW1lIjogbmFtZVs6MzFdLCAidGl0bGUiOiB0aXRsZSwgImhlYWRlcnMiOiBoZWFkZXJzLCAicm93cyI6IHJvd3N9CgoKZGVmIF95bShkdCkgLT4gc3RyOgogICAgaWYgbm90IGR0OgogICAgICAgIHJldHVybiAiIgogICAgaWYgaGFzYXR0cihkdCwgInN0cmZ0aW1lIik6CiAgICAgICAgcmV0dXJuIGR0LnN0cmZ0aW1lKCIlWS0lbSIpCiAgICByZXR1cm4gc3RyKGR0KVs6N10KCgpkZWYgX3djZ19yaXNrX2Jsb2NrKCkgLT4gdHVwbGVbbGlzdFtzdHJdLCBsaXN0W2RpY3RdLCBsaXN0W3N0cl0sIGxpc3Rbc3RyXV06CiAgICBtZDogbGlzdFtzdHJdID0gW10KICAgIHNoZWV0czogbGlzdFtkaWN0XSA9IFtdCiAgICBoZWNob3M6IGxpc3Rbc3RyXSA9IFtdCiAgICB2YWNpb3M6IGxpc3Rbc3RyXSA9IFtdCiAgICB0cnk6CiAgICAgICAgZnJvbSBhcHBzLnJpc2subW9kZWxzIGltcG9ydCAoCiAgICAgICAgICAgIENvbnRhY3RvQ29icmFuemEgYXMgV2NnQ29udGFjdG8sCiAgICAgICAgKQogICAgICAgIGZyb20gYXBwcy5yaXNrLm1vZGVscyBpbXBvcnQgKAogICAgICAgICAgICBFc3RhZG9GaW5hbmNpZXJvIGFzIFdjZ0VGLAogICAgICAgICkKICAgICAgICBmcm9tIGFwcHMucmlzay5tb2RlbHMgaW1wb3J0ICgKICAgICAgICAgICAgUmlza0FsZXJ0YSwKICAgICAgICAgICAgUmlza09wZXJhY2lvbiwKICAgICAgICAgICAgUmlza09wZXJhdGlvblNuYXBzaG90IGFzIFdjZ1NuYXAsCiAgICAgICAgICAgIFJpc2tQYWdvUHJvZ3JhbWFkbywKICAgICAgICAgICAgUmlza1BhZ29SZWFsaXphZG8sCiAgICAgICAgKQogICAgICAgIGZyb20gYXBwcy5yaXNrLnNlbGVjdG9ycyBpbXBvcnQgc25hcHNob3Rfc3VtbWFyeQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBleGM6CiAgICAgICAgbWQuYXBwZW5kKGgyKCJTdGFjayBXQ0cgT25lIFJpc2sgKGBhcHBzLnJpc2tgKSIpKQogICAgICAgIG1kLmFwcGVuZChwKGYiX05vIGRpc3BvbmlibGU6IHtleGN9XyIpKQogICAgICAgIHZhY2lvcy5hcHBlbmQoZiJTdGFjayBhcHBzLnJpc2sgbm8gaW1wb3J0YWJsZToge2V4Y30iKQogICAgICAgIHJldHVybiBtZCwgc2hlZXRzLCBoZWNob3MsIHZhY2lvcwoKICAgIHFzID0gV2NnU25hcC5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKAogICAgICAgICJvcGVyYWNpb24iLCAiZW50aWRhZCIsICJvcGVyYWNpb25fX3VuaWRhZF9uZWdvY2lvIiwgIm9wZXJhY2lvbl9fcHJvZHVjdG8iCiAgICApCiAgICBzdW1tYXJ5ID0gc25hcHNob3Rfc3VtbWFyeShxcykKICAgIGtwaV9oZWFkZXJzID0gWyJLUEkgQ29tYW5kbyBCYWzDs24gV0NHIE9uZSIsICJWYWxvciJdCiAgICBrcGlfcm93cyA9IFsKICAgICAgICBbIlNuYXBzaG90cyIsIHN1bW1hcnlbInRvdGFsX3NuYXBzaG90cyJdXSwKICAgICAgICBbIkNsaWVudGVzIChkaXN0aW50b3MpIiwgc3VtbWFyeVsiY2xpZW50ZXMiXV0sCiAgICAgICAgWyJPcGVyYWNpb25lcyAoZGlzdGludGFzKSIsIHN1bW1hcnlbIm9wZXJhY2lvbmVzIl1dLAogICAgICAgIFsiQ29uIG1vcmEgKGR1ZV9kYXlzPjApIiwgc3VtbWFyeVsiY29uX21vcmEiXV0sCiAgICAgICAgWyJTdW1hIHBhc3RfZHVlX2JhbGFuY2UiLCBmbXRfbnVtKHN1bW1hcnlbInN1bWFfdmVuY2lkbyJdLCAyKV0sCiAgICBdCiAgICBoZWNob3MuYXBwZW5kKGYiV0NHIE9uZSBzbmFwc2hvdHM6IHtzdW1tYXJ5Wyd0b3RhbF9zbmFwc2hvdHMnXX0iKQogICAgaGVjaG9zLmFwcGVuZChmIldDRyBPbmUgb3BlcmFjaW9uZXMgbWFzdGVyOiB7Umlza09wZXJhY2lvbi5vYmplY3RzLmNvdW50KCl9IikKCiAgICBtZC5leHRlbmQoCiAgICAgICAgWwogICAgICAgICAgICBoMigiU3RhY2sgV0NHIE9uZSDigJQgQ29tYW5kbyBCYWzDs24gS1BJcyAoYGFwcHMucmlza2ApIiksCiAgICAgICAgICAgIHAoIkVxdWl2YWxlbnRlIGEgYC93Y2dvbmUvcmlzay9jb21hbmRvLWJhbG9uL2AuIiksCiAgICAgICAgICAgIG1kX3RhYmxlKGtwaV9oZWFkZXJzLCBrcGlfcm93cyksCiAgICAgICAgXQogICAgKQogICAgc2hlZXRzLmFwcGVuZChfc2hlZXQoIldDRyBLUEkiLCAiS1BJcyBXQ0cgUmlzayIsIGtwaV9oZWFkZXJzLCBrcGlfcm93cykpCgogICAgb3BfaGVhZGVycyA9IFsKICAgICAgICAiQ8OzZGlnbyIsCiAgICAgICAgIkNsaWVudGUiLAogICAgICAgICJQcm9kdWN0byIsCiAgICAgICAgIlVOIiwKICAgICAgICAiQ29udHJhdG8iLAogICAgICAgICJBc2Vzb3IiLAogICAgICAgICJNb25lZGEiLAogICAgICAgICJJbmljaW8iLAogICAgICAgICJNb250byBvcmlnaW5hbCIsCiAgICAgICAgIkVzdGFkbyIsCiAgICAgICAgIk5vdGFzIiwKICAgIF0KICAgIG9wX3Jvd3MgPSBbXQogICAgZm9yIG8gaW4gUmlza09wZXJhY2lvbi5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKAogICAgICAgICJlbnRpZGFkIiwgInByb2R1Y3RvIiwgInVuaWRhZF9uZWdvY2lvIgogICAgKS5vcmRlcl9ieSgiZW50aWRhZF9fbm9tYnJlIiwgImNvZGlnb19vcGVyYWNpb24iKToKICAgICAgICBvcF9yb3dzLmFwcGVuZCgKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgby5jb2RpZ29fb3BlcmFjaW9uLAogICAgICAgICAgICAgICAgZ2V0YXR0cihvLmVudGlkYWQsICJub21icmUiLCBOb25lKSBvciBnZXRhdHRyKG8uZW50aWRhZCwgImNvZGlnbyIsICIiKSBvciAi4oCUIiwKICAgICAgICAgICAgICAgIGdldGF0dHIoby5wcm9kdWN0bywgIm5vbWJyZSIsIE5vbmUpIG9yIGdldGF0dHIoby5wcm9kdWN0bywgImNvZGlnbyIsICIiKSBvciAi4oCUIiwKICAgICAgICAgICAgICAgIHN0cihvLnVuaWRhZF9uZWdvY2lvKSBpZiBvLnVuaWRhZF9uZWdvY2lvIGVsc2UgIuKAlCIsCiAgICAgICAgICAgICAgICBvLmNvbnRyYXRvX251bWVybyBvciAiIiwKICAgICAgICAgICAgICAgIG8uYXNlc29yIG9yICIiLAogICAgICAgICAgICAgICAgby5tb25lZGEgb3IgIiIsCiAgICAgICAgICAgICAgICBvLmZlY2hhX2luaWNpby5pc29mb3JtYXQoKSBpZiBvLmZlY2hhX2luaWNpbyBlbHNlICIiLAogICAgICAgICAgICAgICAgZm10X251bShvLm1vbnRvX29yaWdpbmFsLCAyKSBpZiBvLm1vbnRvX29yaWdpbmFsIGlzIG5vdCBOb25lIGVsc2UgIiIsCiAgICAgICAgICAgICAgICBvLmVzdGFkbyBvciAiIiwKICAgICAgICAgICAgICAgIChvLm5vdGFzIG9yICIiKVs6MTYwXSwKICAgICAgICAgICAgXQogICAgICAgICkKICAgIG1kLmV4dGVuZCgKICAgICAgICBbCiAgICAgICAgICAgIGgyKCJXQ0cgT25lIOKAlCBtYWVzdHJvIGRlIG9wZXJhY2lvbmVzIiksCiAgICAgICAgICAgIHAoZiJSZWdpc3Ryb3M6ICoqe2xlbihvcF9yb3dzKX0qKi4iKSwKICAgICAgICAgICAgbWRfdGFibGUob3BfaGVhZGVycywgb3Bfcm93cykgaWYgb3Bfcm93cyBlbHNlIHAoIl9TaW4gUmlza09wZXJhY2lvbi5fIiksCiAgICAgICAgXQogICAgKQogICAgc2hlZXRzLmFwcGVuZChfc2hlZXQoIldDRyBPcGVyYWNpb25lcyIsICJSaXNrT3BlcmFjaW9uIiwgb3BfaGVhZGVycywgb3Bfcm93cykpCiAgICBpZiBub3Qgb3Bfcm93czoKICAgICAgICB2YWNpb3MuYXBwZW5kKCJTaW4gUmlza09wZXJhY2lvbiBlbiBhcHBzLnJpc2suIikKCiAgICBzbmFwX2hlYWRlcnMgPSBbCiAgICAgICAgIkZlY2hhIiwKICAgICAgICAiQ2xpZW50ZSIsCiAgICAgICAgIk9wZXJhY2nDs24iLAogICAgICAgICJFc3RhZG8gb3AuIiwKICAgICAgICAiUHJvZHVjdG8gcmF3IiwKICAgICAgICAiQ2FwaXRhbCIsCiAgICAgICAgIlZlbmNpZG8iLAogICAgICAgICJEw61hcyBhdHJhc28iLAogICAgICAgICJSZW50YSBtZW5zdWFsIiwKICAgICAgICAiQ3VvdGFzIHBlbmQuIiwKICAgICAgICAiSW50ZXLDqXMiLAogICAgICAgICJTZWd1cm8iLAogICAgICAgICJPdHJvcyIsCiAgICAgICAgIk9wY2nDs24gY29tcHJhIiwKICAgICAgICAiUmVudGEgaW5pY2lhbCIsCiAgICAgICAgIlJlbnRhIHRvdGFsIiwKICAgICAgICAiQXJjaGl2byIsCiAgICBdCiAgICBzbmFwX3Jvd3MgPSBbXQogICAgZm9yIHMgaW4gcXMub3JkZXJfYnkoIi1mZWNoYV9zbmFwc2hvdCIsICItZHVlX2RheXMiLCAiZW50aWRhZF9fbm9tYnJlIik6CiAgICAgICAgc25hcF9yb3dzLmFwcGVuZCgKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgcy5mZWNoYV9zbmFwc2hvdC5pc29mb3JtYXQoKSBpZiBzLmZlY2hhX3NuYXBzaG90IGVsc2UgIiIsCiAgICAgICAgICAgICAgICBnZXRhdHRyKHMuZW50aWRhZCwgIm5vbWJyZSIsIE5vbmUpIG9yICLigJQiLAogICAgICAgICAgICAgICAgcy5vcGVyYWNpb24uY29kaWdvX29wZXJhY2lvbiBpZiBzLm9wZXJhY2lvbiBlbHNlICLigJQiLAogICAgICAgICAgICAgICAgcy5lc3RhZG9fb3BlcmFjaW9uIG9yICIiLAogICAgICAgICAgICAgICAgcy5wcm9kdWN0b19ub21icmVfcmF3IG9yICIiLAogICAgICAgICAgICAgICAgZm10X251bShzLmNhcGl0YWxfYmFsYW5jZSwgMikgaWYgcy5jYXBpdGFsX2JhbGFuY2UgaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0ocy5wYXN0X2R1ZV9iYWxhbmNlLCAyKSBpZiBzLnBhc3RfZHVlX2JhbGFuY2UgaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICAgICAgICAgIHMuZHVlX2RheXMgaWYgcy5kdWVfZGF5cyBpcyBub3QgTm9uZSBlbHNlICIiLAogICAgICAgICAgICAgICAgZm10X251bShzLm1vbnRobHlfcmVudCwgMikgaWYgcy5tb250aGx5X3JlbnQgaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0ocy5vdXRzdGFuZGluZ19pbnN0YWxsbWVudHMsIDIpCiAgICAgICAgICAgICAgICBpZiBzLm91dHN0YW5kaW5nX2luc3RhbGxtZW50cyBpcyBub3QgTm9uZQogICAgICAgICAgICAgICAgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0ocy5pbnRlcmVzdF9iYWxhbmNlLCAyKSBpZiBzLmludGVyZXN0X2JhbGFuY2UgaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0ocy5pbnN1cmFuY2VfYmFsYW5jZSwgMikgaWYgcy5pbnN1cmFuY2VfYmFsYW5jZSBpcyBub3QgTm9uZSBlbHNlICIiLAogICAgICAgICAgICAgICAgZm10X251bShzLm90aGVyX2NoYXJnZXNfYmFsYW5jZSwgMikKICAgICAgICAgICAgICAgIGlmIHMub3RoZXJfY2hhcmdlc19iYWxhbmNlIGlzIG5vdCBOb25lCiAgICAgICAgICAgICAgICBlbHNlICIiLAogICAgICAgICAgICAgICAgZm10X251bShzLnB1cmNoYXNlX29wdGlvbl92YWx1ZSwgMikKICAgICAgICAgICAgICAgIGlmIHMucHVyY2hhc2Vfb3B0aW9uX3ZhbHVlIGlzIG5vdCBOb25lCiAgICAgICAgICAgICAgICBlbHNlICIiLAogICAgICAgICAgICAgICAgZm10X251bShzLmluaXRpYWxfcmVudF92YWx1ZSwgMikgaWYgcy5pbml0aWFsX3JlbnRfdmFsdWUgaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0ocy50b3RhbF9yZW50X3ZhbHVlLCAyKSBpZiBzLnRvdGFsX3JlbnRfdmFsdWUgaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICAgICAgICAgIHMuYXJjaGl2b19vcmlnZW4gb3IgIiIsCiAgICAgICAgICAgIF0KICAgICAgICApCiAgICBtZC5leHRlbmQoCiAgICAgICAgWwogICAgICAgICAgICBoMigiV0NHIE9uZSDigJQgZGV0YWxsZSBjb21wbGV0byBkZSBzbmFwc2hvdHMgKGJyb3dzZSkiKSwKICAgICAgICAgICAgcChmIlJlZ2lzdHJvczogKip7bGVuKHNuYXBfcm93cyl9KiouIiksCiAgICAgICAgICAgIG1kX3RhYmxlKHNuYXBfaGVhZGVycywgc25hcF9yb3dzKSBpZiBzbmFwX3Jvd3MgZWxzZSBwKCJfU2luIHNuYXBzaG90cyBXQ0cuXyIpLAogICAgICAgIF0KICAgICkKICAgIHNoZWV0cy5hcHBlbmQoX3NoZWV0KCJXQ0cgU25hcHNob3RzIiwgImFwcHMucmlzayBzbmFwc2hvdHMiLCBzbmFwX2hlYWRlcnMsIHNuYXBfcm93cykpCiAgICBpZiBub3Qgc25hcF9yb3dzOgogICAgICAgIHZhY2lvcy5hcHBlbmQoIlNpbiBSaXNrT3BlcmF0aW9uU25hcHNob3QgZW4gYXBwcy5yaXNrLiIpCgogICAgZWZfaGVhZGVycyA9IFsKICAgICAgICAiRmVjaGEgY29ydGUiLAogICAgICAgICJFbnRpZGFkIiwKICAgICAgICAiVmVudGFzIiwKICAgICAgICAiVXRpbGlkYWQgbmV0YSIsCiAgICAgICAgIkFjdGl2byBjb3JyLiIsCiAgICAgICAgIkFjdGl2byBubyBjb3JyLiIsCiAgICAgICAgIlBhc2l2byBjb3JyLiIsCiAgICAgICAgIlBhc2l2byBubyBjb3JyLiIsCiAgICAgICAgIlBhdHJpbW9uaW8iLAogICAgICAgICJFQklUREEiLAogICAgICAgICJBdWRpdG9yIiwKICAgICAgICAiT2JzZXJ2YWNpb25lcyIsCiAgICBdCiAgICBlZl9yb3dzID0gW10KICAgIGZvciBlIGluIFdjZ0VGLm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoImVudGlkYWQiKS5vcmRlcl9ieSgKICAgICAgICAiLWZlY2hhX2NvcnRlIiwgImVudGlkYWRfX25vbWJyZSIKICAgICk6CiAgICAgICAgZWZfcm93cy5hcHBlbmQoCiAgICAgICAgICAgIFsKICAgICAgICAgICAgICAgIGUuZmVjaGFfY29ydGUuaXNvZm9ybWF0KCkgaWYgZS5mZWNoYV9jb3J0ZSBlbHNlICIiLAogICAgICAgICAgICAgICAgZ2V0YXR0cihlLmVudGlkYWQsICJub21icmUiLCBOb25lKSBvciAi4oCUIiwKICAgICAgICAgICAgICAgIGZtdF9udW0oZS52ZW50YXMsIDIpIGlmIGUudmVudGFzIGlzIG5vdCBOb25lIGVsc2UgIiIsCiAgICAgICAgICAgICAgICBmbXRfbnVtKGUudXRpbGlkYWRfbmV0YSwgMikgaWYgZS51dGlsaWRhZF9uZXRhIGlzIG5vdCBOb25lIGVsc2UgIiIsCiAgICAgICAgICAgICAgICBmbXRfbnVtKGUuYWN0aXZvX2NvcnJpZW50ZSwgMikgaWYgZS5hY3Rpdm9fY29ycmllbnRlIGlzIG5vdCBOb25lIGVsc2UgIiIsCiAgICAgICAgICAgICAgICBmbXRfbnVtKGUuYWN0aXZvX25vX2NvcnJpZW50ZSwgMikKICAgICAgICAgICAgICAgIGlmIGUuYWN0aXZvX25vX2NvcnJpZW50ZSBpcyBub3QgTm9uZQogICAgICAgICAgICAgICAgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0oZS5wYXNpdm9fY29ycmllbnRlLCAyKSBpZiBlLnBhc2l2b19jb3JyaWVudGUgaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0oZS5wYXNpdm9fbm9fY29ycmllbnRlLCAyKQogICAgICAgICAgICAgICAgaWYgZS5wYXNpdm9fbm9fY29ycmllbnRlIGlzIG5vdCBOb25lCiAgICAgICAgICAgICAgICBlbHNlICIiLAogICAgICAgICAgICAgICAgZm10X251bShlLnBhdHJpbW9uaW8sIDIpIGlmIGUucGF0cmltb25pbyBpcyBub3QgTm9uZSBlbHNlICIiLAogICAgICAgICAgICAgICAgZm10X251bShlLmViaXRkYSwgMikgaWYgZS5lYml0ZGEgaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGUuYXVkaXRvcl9jb250YWRvciBvciAiIiwKICAgICAgICAgICAgICAgIChlLm9ic2VydmFjaW9uZXMgb3IgIiIpWzoyMDBdLAogICAgICAgICAgICBdCiAgICAgICAgKQogICAgbWQuZXh0ZW5kKAogICAgICAgIFsKICAgICAgICAgICAgaDIoIldDRyBPbmUg4oCUIGVzdGFkb3MgZmluYW5jaWVyb3MgKEVFRkYpIiksCiAgICAgICAgICAgIG1kX3RhYmxlKGVmX2hlYWRlcnMsIGVmX3Jvd3MpIGlmIGVmX3Jvd3MgZWxzZSBwKCJfU2luIEVFRkYgV0NHLl8iKSwKICAgICAgICBdCiAgICApCiAgICBzaGVldHMuYXBwZW5kKF9zaGVldCgiV0NHIEVFRkYiLCAiRXN0YWRvRmluYW5jaWVybyBXQ0ciLCBlZl9oZWFkZXJzLCBlZl9yb3dzKSkKCiAgICBhbGVydGFfaGVhZGVycyA9IFsKICAgICAgICAiRmVjaGEiLAogICAgICAgICJFbnRpZGFkIiwKICAgICAgICAiT3BlcmFjacOzbiIsCiAgICAgICAgIlRpcG8iLAogICAgICAgICJTZXZlcmlkYWQiLAogICAgICAgICJBY3RpdmEiLAogICAgICAgICJPcmlnZW4iLAogICAgICAgICJNZW5zYWplIiwKICAgIF0KICAgIGFsZXJ0YV9yb3dzID0gW10KICAgIGZvciBhIGluIFJpc2tBbGVydGEub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgiZW50aWRhZCIsICJvcGVyYWNpb24iKS5vcmRlcl9ieSgKICAgICAgICAiLWZlY2hhX2FsZXJ0YSIsICItaWQiCiAgICApOgogICAgICAgIGFsZXJ0YV9yb3dzLmFwcGVuZCgKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgYS5mZWNoYV9hbGVydGEuaXNvZm9ybWF0KCkgaWYgYS5mZWNoYV9hbGVydGEgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGdldGF0dHIoYS5lbnRpZGFkLCAibm9tYnJlIiwgTm9uZSkgb3IgIuKAlCIsCiAgICAgICAgICAgICAgICBhLm9wZXJhY2lvbi5jb2RpZ29fb3BlcmFjaW9uIGlmIGEub3BlcmFjaW9uIGVsc2UgIuKAlCIsCiAgICAgICAgICAgICAgICBhLnRpcG9fYWxlcnRhLAogICAgICAgICAgICAgICAgYS5zZXZlcmlkYWQsCiAgICAgICAgICAgICAgICAiU8OtIiBpZiBhLmFjdGl2YSBlbHNlICJObyIsCiAgICAgICAgICAgICAgICBhLm9yaWdlbiBvciAiIiwKICAgICAgICAgICAgICAgIChhLm1lbnNhamUgb3IgIiIpWzozMDBdLAogICAgICAgICAgICBdCiAgICAgICAgKQogICAgbWQuZXh0ZW5kKAogICAgICAgIFsKICAgICAgICAgICAgaDIoIldDRyBPbmUg4oCUIGFsZXJ0YXMgZGUgcmllc2dvIiksCiAgICAgICAgICAgIG1kX3RhYmxlKGFsZXJ0YV9oZWFkZXJzLCBhbGVydGFfcm93cykKICAgICAgICAgICAgaWYgYWxlcnRhX3Jvd3MKICAgICAgICAgICAgZWxzZSBwKCJfU2luIFJpc2tBbGVydGEuXyIpLAogICAgICAgIF0KICAgICkKICAgIHNoZWV0cy5hcHBlbmQoX3NoZWV0KCJXQ0cgQWxlcnRhcyIsICJSaXNrQWxlcnRhIiwgYWxlcnRhX2hlYWRlcnMsIGFsZXJ0YV9yb3dzKSkKICAgIGhlY2hvcy5hcHBlbmQoZiJXQ0cgT25lIGFsZXJ0YXM6IHtsZW4oYWxlcnRhX3Jvd3MpfSIpCgogICAgcHJvZ19oZWFkZXJzID0gWwogICAgICAgICJPcGVyYWNpw7NuIiwKICAgICAgICAiRW50aWRhZCIsCiAgICAgICAgIkZlY2hhIHByb2cuIiwKICAgICAgICAiQ2FwaXRhbCIsCiAgICAgICAgIkludGVyw6lzIiwKICAgICAgICAiTW9yYSIsCiAgICAgICAgIk90cm9zIiwKICAgICAgICAiTW9uZWRhIiwKICAgICAgICAiRXN0YWRvIiwKICAgIF0KICAgIHByb2dfcm93cyA9IFtdCiAgICBmb3IgciBpbiBSaXNrUGFnb1Byb2dyYW1hZG8ub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgib3BlcmFjaW9uIiwgImVudGlkYWQiKS5vcmRlcl9ieSgKICAgICAgICAiZmVjaGFfcHJvZ3JhbWFkYSIKICAgICk6CiAgICAgICAgcHJvZ19yb3dzLmFwcGVuZCgKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgci5vcGVyYWNpb24uY29kaWdvX29wZXJhY2lvbiBpZiByLm9wZXJhY2lvbiBlbHNlICLigJQiLAogICAgICAgICAgICAgICAgZ2V0YXR0cihyLmVudGlkYWQsICJub21icmUiLCBOb25lKSBvciAi4oCUIiwKICAgICAgICAgICAgICAgIHIuZmVjaGFfcHJvZ3JhbWFkYS5pc29mb3JtYXQoKSBpZiByLmZlY2hhX3Byb2dyYW1hZGEgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0oci5tb250b19jYXBpdGFsLCAyKSBpZiByLm1vbnRvX2NhcGl0YWwgaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0oci5tb250b19pbnRlcmVzLCAyKSBpZiByLm1vbnRvX2ludGVyZXMgaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0oci5tb250b19tb3JhLCAyKSBpZiByLm1vbnRvX21vcmEgaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0oci5tb250b19vdHJvcywgMikgaWYgci5tb250b19vdHJvcyBpcyBub3QgTm9uZSBlbHNlICIiLAogICAgICAgICAgICAgICAgci5tb25lZGEgb3IgIiIsCiAgICAgICAgICAgICAgICByLmVzdGFkbyBvciAiIiwKICAgICAgICAgICAgXQogICAgICAgICkKICAgIHBhZ29faGVhZGVycyA9IFsKICAgICAgICAiT3BlcmFjacOzbiIsCiAgICAgICAgIkVudGlkYWQiLAogICAgICAgICJGZWNoYSBwYWdvIiwKICAgICAgICAiQ2FwaXRhbCIsCiAgICAgICAgIkludGVyw6lzIiwKICAgICAgICAiTW9yYSIsCiAgICAgICAgIk90cm9zIiwKICAgICAgICAiTW9uZWRhIiwKICAgICAgICAiUmVmZXJlbmNpYSIsCiAgICBdCiAgICBwYWdvX3Jvd3MgPSBbXQogICAgZm9yIHIgaW4gUmlza1BhZ29SZWFsaXphZG8ub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgib3BlcmFjaW9uIiwgImVudGlkYWQiKS5vcmRlcl9ieSgKICAgICAgICAiLWZlY2hhX3BhZ28iCiAgICApOgogICAgICAgIHBhZ29fcm93cy5hcHBlbmQoCiAgICAgICAgICAgIFsKICAgICAgICAgICAgICAgIHIub3BlcmFjaW9uLmNvZGlnb19vcGVyYWNpb24gaWYgci5vcGVyYWNpb24gZWxzZSAi4oCUIiwKICAgICAgICAgICAgICAgIGdldGF0dHIoci5lbnRpZGFkLCAibm9tYnJlIiwgTm9uZSkgb3IgIuKAlCIsCiAgICAgICAgICAgICAgICByLmZlY2hhX3BhZ28uaXNvZm9ybWF0KCkgaWYgci5mZWNoYV9wYWdvIGVsc2UgIiIsCiAgICAgICAgICAgICAgICBmbXRfbnVtKHIubW9udG9fY2FwaXRhbCwgMikgaWYgci5tb250b19jYXBpdGFsIGlzIG5vdCBOb25lIGVsc2UgIiIsCiAgICAgICAgICAgICAgICBmbXRfbnVtKHIubW9udG9faW50ZXJlcywgMikgaWYgci5tb250b19pbnRlcmVzIGlzIG5vdCBOb25lIGVsc2UgIiIsCiAgICAgICAgICAgICAgICBmbXRfbnVtKHIubW9udG9fbW9yYSwgMikgaWYgci5tb250b19tb3JhIGlzIG5vdCBOb25lIGVsc2UgIiIsCiAgICAgICAgICAgICAgICBmbXRfbnVtKHIubW9udG9fb3Ryb3MsIDIpIGlmIHIubW9udG9fb3Ryb3MgaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICAgICAgICAgIHIubW9uZWRhIG9yICIiLAogICAgICAgICAgICAgICAgci5yZWZlcmVuY2lhIG9yICIiLAogICAgICAgICAgICBdCiAgICAgICAgKQogICAgY29udGFjdF9oZWFkZXJzID0gWwogICAgICAgICJGZWNoYSIsCiAgICAgICAgIkVudGlkYWQiLAogICAgICAgICJPcGVyYWNpw7NuIiwKICAgICAgICAiVGlwbyIsCiAgICAgICAgIlJlc3VsdGFkbyIsCiAgICAgICAgIkFjdWVyZG8iLAogICAgICAgICJDb21wcm9taXNvIiwKICAgICAgICAiTm90YXMiLAogICAgXQogICAgY29udGFjdF9yb3dzID0gW10KICAgIGZvciBjIGluIFdjZ0NvbnRhY3RvLm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoImVudGlkYWQiLCAib3BlcmFjaW9uIikub3JkZXJfYnkoCiAgICAgICAgIi1mZWNoYSIsICJlbnRpZGFkX19ub21icmUiCiAgICApOgogICAgICAgIGNvbnRhY3Rfcm93cy5hcHBlbmQoCiAgICAgICAgICAgIFsKICAgICAgICAgICAgICAgIGMuZmVjaGEuaXNvZm9ybWF0KCkgaWYgYy5mZWNoYSBlbHNlICIiLAogICAgICAgICAgICAgICAgZ2V0YXR0cihjLmVudGlkYWQsICJub21icmUiLCBOb25lKSBvciAi4oCUIiwKICAgICAgICAgICAgICAgIGMub3BlcmFjaW9uLmNvZGlnb19vcGVyYWNpb24gaWYgYy5vcGVyYWNpb24gZWxzZSAi4oCUIiwKICAgICAgICAgICAgICAgIGMudGlwb19jb250YWN0bywKICAgICAgICAgICAgICAgIGMucmVzdWx0YWRvIG9yICIiLAogICAgICAgICAgICAgICAgKGMuYWN1ZXJkbyBvciAiIilbOjIwMF0sCiAgICAgICAgICAgICAgICBjLmZlY2hhX2NvbXByb21pc28uaXNvZm9ybWF0KCkgaWYgYy5mZWNoYV9jb21wcm9taXNvIGVsc2UgIiIsCiAgICAgICAgICAgICAgICAoYy5ub3RhcyBvciAiIilbOjE2MF0sCiAgICAgICAgICAgIF0KICAgICAgICApCiAgICBtZC5leHRlbmQoCiAgICAgICAgWwogICAgICAgICAgICBoMigiV0NHIE9uZSDigJQgcGFnb3MgcHJvZ3JhbWFkb3MiKSwKICAgICAgICAgICAgbWRfdGFibGUocHJvZ19oZWFkZXJzLCBwcm9nX3Jvd3MpIGlmIHByb2dfcm93cyBlbHNlIHAoIl9TaW4gcGFnb3MgcHJvZ3JhbWFkb3MgV0NHLl8iKSwKICAgICAgICAgICAgaDIoIldDRyBPbmUg4oCUIHBhZ29zIHJlYWxpemFkb3MiKSwKICAgICAgICAgICAgbWRfdGFibGUocGFnb19oZWFkZXJzLCBwYWdvX3Jvd3MpIGlmIHBhZ29fcm93cyBlbHNlIHAoIl9TaW4gcGFnb3MgcmVhbGl6YWRvcyBXQ0cuXyIpLAogICAgICAgICAgICBoMigiV0NHIE9uZSDigJQgYml0w6Fjb3JhIGRlIGNvbnRhY3RvcyBkZSBjb2JyYW56YSIpLAogICAgICAgICAgICBtZF90YWJsZShjb250YWN0X2hlYWRlcnMsIGNvbnRhY3Rfcm93cykKICAgICAgICAgICAgaWYgY29udGFjdF9yb3dzCiAgICAgICAgICAgIGVsc2UgcCgiX1NpbiBjb250YWN0b3MgV0NHLl8iKSwKICAgICAgICBdCiAgICApCiAgICBzaGVldHMuZXh0ZW5kKAogICAgICAgIFsKICAgICAgICAgICAgX3NoZWV0KCJXQ0cgUHJvZyBwYWdvcyIsICJSaXNrUGFnb1Byb2dyYW1hZG8iLCBwcm9nX2hlYWRlcnMsIHByb2dfcm93cyksCiAgICAgICAgICAgIF9zaGVldCgiV0NHIFBhZ29zIiwgIlJpc2tQYWdvUmVhbGl6YWRvIiwgcGFnb19oZWFkZXJzLCBwYWdvX3Jvd3MpLAogICAgICAgICAgICBfc2hlZXQoIldDRyBDb250YWN0b3MiLCAiQ29udGFjdG9Db2JyYW56YSBXQ0ciLCBjb250YWN0X2hlYWRlcnMsIGNvbnRhY3Rfcm93cyksCiAgICAgICAgXQogICAgKQogICAgcmV0dXJuIG1kLCBzaGVldHMsIGhlY2hvcywgdmFjaW9zCgoKZGVmIGJ1aWxkX3Jpc2tfcmVzdWx0cyhjZmc6IFJlcG9ydENvbmZpZyB8IE5vbmUgPSBOb25lKSAtPiBkaWN0OgogICAgY2ZnID0gY2ZnIG9yIFJlcG9ydENvbmZpZy5nZXRfYWN0aXZlKCkKICAgIG5vdyA9IHRpbWV6b25lLmxvY2FsdGltZSgpCiAgICBzdGFtcCA9IHJlcG9ydF9zdGFtcChub3cpCiAgICBzdGFtcF9sYWJlbCA9ICgKICAgICAgICBmIkdlbmVyYWRvIHtub3cuc3RyZnRpbWUoJyVZLSVtLSVkICVIOiVNJyl9ICIKICAgICAgICBmIih7dGltZXpvbmUuZ2V0X2N1cnJlbnRfdGltZXpvbmVfbmFtZSgpfSkgwrd7c3RhbXB9IgogICAgKQogICAgdG9kYXkgPSBub3cuZGF0ZSgpCgogICAgbW9udGhzID0gWwogICAgICAgIG0KICAgICAgICBmb3IgbSBpbiAoCiAgICAgICAgICAgIFJpc2tPcGVyYXRpb25TbmFwc2hvdC5vYmplY3RzLmFubm90YXRlKG09VHJ1bmNNb250aCgiZmVjaGFfc25hcHNob3QiKSkKICAgICAgICAgICAgLnZhbHVlc19saXN0KCJtIiwgZmxhdD1UcnVlKQogICAgICAgICAgICAuZGlzdGluY3QoKQogICAgICAgICAgICAub3JkZXJfYnkoIi1tIikKICAgICAgICApCiAgICAgICAgaWYgbQogICAgXQogICAgY3Vycl9wID0gbW9udGhzWzBdLnN0cmZ0aW1lKCIlWS0lbSIpIGlmIG1vbnRocyBlbHNlIE5vbmUKICAgIHByZXZfcCA9IG1vbnRoc1sxXS5zdHJmdGltZSgiJVktJW0iKSBpZiBsZW4obW9udGhzKSA+IDEgZWxzZSBOb25lCgogICAgZGVmIF9maWx0ZXJfbW9udGgocXMsIHltOiBzdHIgfCBOb25lKToKICAgICAgICBpZiBub3QgeW06CiAgICAgICAgICAgIHJldHVybiBxcy5ub25lKCkKICAgICAgICB5LCBtID0geW0uc3BsaXQoIi0iKQogICAgICAgIHJldHVybiBxcy5maWx0ZXIoZmVjaGFfc25hcHNob3RfX3llYXI9aW50KHkpLCBmZWNoYV9zbmFwc2hvdF9fbW9udGg9aW50KG0pKQoKICAgIGRlZiBfa3BpKHltOiBzdHIgfCBOb25lKSAtPiBkaWN0OgogICAgICAgIGVtcHR5ID0gewogICAgICAgICAgICAib3BzIjogMCwKICAgICAgICAgICAgImFsZXJ0YXMiOiAwLAogICAgICAgICAgICAic2FsZG8iOiBEZWNpbWFsKCIwIiksCiAgICAgICAgICAgICJleGlnaWJsZSI6IERlY2ltYWwoIjAiKSwKICAgICAgICAgICAgImNyaXRpY29zIjogMCwKICAgICAgICAgICAgImFsdG9zIjogMCwKICAgICAgICAgICAgIm1vcmFfcHJvbSI6IERlY2ltYWwoIjAiKSwKICAgICAgICB9CiAgICAgICAgaWYgbm90IHltOgogICAgICAgICAgICByZXR1cm4gZW1wdHkKICAgICAgICBxcyA9IF9maWx0ZXJfbW9udGgoUmlza09wZXJhdGlvblNuYXBzaG90Lm9iamVjdHMuYWxsKCksIHltKQogICAgICAgIG4gPSBxcy5jb3VudCgpCiAgICAgICAgaWYgbm90IG46CiAgICAgICAgICAgIHJldHVybiBlbXB0eQogICAgICAgIGFnZyA9IHFzLmFnZ3JlZ2F0ZSgKICAgICAgICAgICAgc2FsZG89U3VtKCJzYWxkbyIpLCBleGlnaWJsZT1TdW0oIm1vbnRvX2V4aWdpYmxlIiksIG1vcmE9U3VtKCJkaWFzX21vcmEiKQogICAgICAgICkKICAgICAgICByZXR1cm4gewogICAgICAgICAgICAib3BzIjogbiwKICAgICAgICAgICAgImFsZXJ0YXMiOiBxcy5maWx0ZXIoYWxlcnRhPVRydWUpLmNvdW50KCksCiAgICAgICAgICAgICJzYWxkbyI6IGFnZ1sic2FsZG8iXSBvciBEZWNpbWFsKCIwIiksCiAgICAgICAgICAgICJleGlnaWJsZSI6IGFnZ1siZXhpZ2libGUiXSBvciBEZWNpbWFsKCIwIiksCiAgICAgICAgICAgICJjcml0aWNvcyI6IHFzLmZpbHRlcihuaXZlbF9yaWVzZ289Umlza09wZXJhdGlvblNuYXBzaG90Lk5JVkVMX0NSSVRJQ08pLmNvdW50KCksCiAgICAgICAgICAgICJhbHRvcyI6IHFzLmZpbHRlcihuaXZlbF9yaWVzZ289Umlza09wZXJhdGlvblNuYXBzaG90Lk5JVkVMX0FMVE8pLmNvdW50KCksCiAgICAgICAgICAgICJtb3JhX3Byb20iOiAoRGVjaW1hbChhZ2dbIm1vcmEiXSBvciAwKSAvIERlY2ltYWwobikpLAogICAgICAgIH0KCiAgICBjdXJyID0gX2twaShjdXJyX3ApCiAgICBwcmV2ID0gX2twaShwcmV2X3ApCiAgICBrcGlfaGVhZGVycyA9IFsiS1BJIiwgIsOabHRpbW8gcGVyw61vZG8iLCAiQW50ZXJpb3IiLCAiJSDOlCJdCiAgICBrcGlfcm93cyA9IFsKICAgICAgICBbIk9wZXJhY2lvbmVzIiwgY3Vyclsib3BzIl0sIHByZXZbIm9wcyJdIGlmIHByZXZfcCBlbHNlICLigJQiLCBwY3RfY2hhbmdlKGN1cnJbIm9wcyJdLCBwcmV2WyJvcHMiXSkgaWYgcHJldl9wIGVsc2UgIuKAlCJdLAogICAgICAgIFsiQWxlcnRhcyIsIGN1cnJbImFsZXJ0YXMiXSwgcHJldlsiYWxlcnRhcyJdIGlmIHByZXZfcCBlbHNlICLigJQiLCBwY3RfY2hhbmdlKGN1cnJbImFsZXJ0YXMiXSwgcHJldlsiYWxlcnRhcyJdKSBpZiBwcmV2X3AgZWxzZSAi4oCUIl0sCiAgICAgICAgWyJTYWxkbyIsIGZtdF9udW0oY3Vyclsic2FsZG8iXSwgMiksIGZtdF9udW0ocHJldlsic2FsZG8iXSwgMikgaWYgcHJldl9wIGVsc2UgIuKAlCIsIHBjdF9jaGFuZ2UoY3Vyclsic2FsZG8iXSwgcHJldlsic2FsZG8iXSkgaWYgcHJldl9wIGVsc2UgIuKAlCJdLAogICAgICAgIFsiRXhpZ2libGUiLCBmbXRfbnVtKGN1cnJbImV4aWdpYmxlIl0sIDIpLCBmbXRfbnVtKHByZXZbImV4aWdpYmxlIl0sIDIpIGlmIHByZXZfcCBlbHNlICLigJQiLCBwY3RfY2hhbmdlKGN1cnJbImV4aWdpYmxlIl0sIHByZXZbImV4aWdpYmxlIl0pIGlmIHByZXZfcCBlbHNlICLigJQiXSwKICAgICAgICBbIkNyw610aWNvcyIsIGN1cnJbImNyaXRpY29zIl0sIHByZXZbImNyaXRpY29zIl0gaWYgcHJldl9wIGVsc2UgIuKAlCIsIHBjdF9jaGFuZ2UoY3VyclsiY3JpdGljb3MiXSwgcHJldlsiY3JpdGljb3MiXSkgaWYgcHJldl9wIGVsc2UgIuKAlCJdLAogICAgICAgIFsiQWx0b3MiLCBjdXJyWyJhbHRvcyJdLCBwcmV2WyJhbHRvcyJdIGlmIHByZXZfcCBlbHNlICLigJQiLCBwY3RfY2hhbmdlKGN1cnJbImFsdG9zIl0sIHByZXZbImFsdG9zIl0pIGlmIHByZXZfcCBlbHNlICLigJQiXSwKICAgICAgICBbIk1vcmEgcHJvbS4gZMOtYXMiLCBmbXRfbnVtKGN1cnJbIm1vcmFfcHJvbSJdLCAxKSwgZm10X251bShwcmV2WyJtb3JhX3Byb20iXSwgMSkgaWYgcHJldl9wIGVsc2UgIuKAlCIsIHBjdF9jaGFuZ2UoY3VyclsibW9yYV9wcm9tIl0sIHByZXZbIm1vcmFfcHJvbSJdKSBpZiBwcmV2X3AgZWxzZSAi4oCUIl0sCiAgICBdCgogICAgIyBTZXJpZSBtZW5zdWFsIGNvbXBsZXRhIChjaWZyYXMgYmFzZSB0aXBvIGNoYXJ0KQogICAgc2VyaWVfaGVhZGVycyA9IFsKICAgICAgICAiUGVyaW9kbyIsCiAgICAgICAgIk9wcyIsCiAgICAgICAgIkFsZXJ0YXMiLAogICAgICAgICJTYWxkbyIsCiAgICAgICAgIkV4aWdpYmxlIiwKICAgICAgICAiQ3LDrXRpY29zIiwKICAgICAgICAiQWx0b3MiLAogICAgICAgICJNb3JhIHByb20uIiwKICAgIF0KICAgIHNlcmllX3Jvd3MgPSBbXQogICAgZm9yIG0gaW4gc29ydGVkKG1vbnRocyk6CiAgICAgICAgeW0gPSBtLnN0cmZ0aW1lKCIlWS0lbSIpCiAgICAgICAgayA9IF9rcGkoeW0pCiAgICAgICAgc2VyaWVfcm93cy5hcHBlbmQoCiAgICAgICAgICAgIFsKICAgICAgICAgICAgICAgIHltLAogICAgICAgICAgICAgICAga1sib3BzIl0sCiAgICAgICAgICAgICAgICBrWyJhbGVydGFzIl0sCiAgICAgICAgICAgICAgICBmbXRfbnVtKGtbInNhbGRvIl0sIDIpLAogICAgICAgICAgICAgICAgZm10X251bShrWyJleGlnaWJsZSJdLCAyKSwKICAgICAgICAgICAgICAgIGtbImNyaXRpY29zIl0sCiAgICAgICAgICAgICAgICBrWyJhbHRvcyJdLAogICAgICAgICAgICAgICAgZm10X251bShrWyJtb3JhX3Byb20iXSwgMSksCiAgICAgICAgICAgIF0KICAgICAgICApCgogICAgIyBDb21hbmRvIEJhbMOzbjogw7psdGltbyBzbmFwc2hvdCBwb3Igb3BlcmFjacOzbgogICAgYmFsb25faGVhZGVycyA9IFsKICAgICAgICAiQ2xpZW50ZSIsCiAgICAgICAgIkPDs2RpZ28gY2xpZW50ZSIsCiAgICAgICAgIk9wZXJhY2nDs24iLAogICAgICAgICJVTiIsCiAgICAgICAgIlByb2R1Y3RvIiwKICAgICAgICAiRmVjaGEgc25hcHNob3QiLAogICAgICAgICJTYWxkbyIsCiAgICAgICAgIkTDrWFzIG1vcmEiLAogICAgICAgICJFeGlnaWJsZSIsCiAgICAgICAgIk5pdmVsIiwKICAgICAgICAiQWxlcnRhIiwKICAgICAgICAiRGV0YWxsZSIsCiAgICBdCiAgICBiYWxvbl9yb3dzID0gW10KICAgIGxhdGVzdF9kYXRlcyA9IFJpc2tPcGVyYXRpb25TbmFwc2hvdC5vYmplY3RzLnZhbHVlcygKICAgICAgICAiZW50aWRhZF9pZCIsICJyZWZlcmVuY2lhX29wZXJhY2lvbiIKICAgICkuYW5ub3RhdGUodWx0aW1hPU1heCgiZmVjaGFfc25hcHNob3QiKSkKICAgIG9wZXJhY2lvbmVzX2xhdGVzdCA9IFtdCiAgICBmb3Igcm93IGluIGxhdGVzdF9kYXRlcy5vcmRlcl9ieSgiLXVsdGltYSIpOgogICAgICAgIHNuYXAgPSAoCiAgICAgICAgICAgIFJpc2tPcGVyYXRpb25TbmFwc2hvdC5vYmplY3RzLmZpbHRlcigKICAgICAgICAgICAgICAgIGVudGlkYWRfaWQ9cm93WyJlbnRpZGFkX2lkIl0sCiAgICAgICAgICAgICAgICByZWZlcmVuY2lhX29wZXJhY2lvbj1yb3dbInJlZmVyZW5jaWFfb3BlcmFjaW9uIl0sCiAgICAgICAgICAgICAgICBmZWNoYV9zbmFwc2hvdD1yb3dbInVsdGltYSJdLAogICAgICAgICAgICApCiAgICAgICAgICAgIC5zZWxlY3RfcmVsYXRlZCgiZW50aWRhZCIsICJlbnRpZGFkX191bmlkYWRfbmVnb2NpbyIsICJwcm9kdWN0byIpCiAgICAgICAgICAgIC5maXJzdCgpCiAgICAgICAgKQogICAgICAgIGlmIHNuYXA6CiAgICAgICAgICAgIG9wZXJhY2lvbmVzX2xhdGVzdC5hcHBlbmQoc25hcCkKICAgIGZvciBzIGluIG9wZXJhY2lvbmVzX2xhdGVzdDoKICAgICAgICB1biA9ICIiCiAgICAgICAgaWYgcy5lbnRpZGFkIGFuZCBnZXRhdHRyKHMuZW50aWRhZCwgInVuaWRhZF9uZWdvY2lvIiwgTm9uZSk6CiAgICAgICAgICAgIHVuID0gZ2V0YXR0cihzLmVudGlkYWQudW5pZGFkX25lZ29jaW8sICJjb2RlIiwgTm9uZSkgb3Igc3RyKAogICAgICAgICAgICAgICAgcy5lbnRpZGFkLnVuaWRhZF9uZWdvY2lvCiAgICAgICAgICAgICkKICAgICAgICBlbGlmIHMucHJvZHVjdG8gYW5kIGdldGF0dHIocy5wcm9kdWN0bywgInVuaWRhZF9uZWdvY2lvIiwgTm9uZSk6CiAgICAgICAgICAgIHVuID0gZ2V0YXR0cihzLnByb2R1Y3RvLnVuaWRhZF9uZWdvY2lvLCAiY29kZSIsIE5vbmUpIG9yIHN0cigKICAgICAgICAgICAgICAgIHMucHJvZHVjdG8udW5pZGFkX25lZ29jaW8KICAgICAgICAgICAgKQogICAgICAgIGJhbG9uX3Jvd3MuYXBwZW5kKAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICBnZXRhdHRyKHMuZW50aWRhZCwgIm5vbWJyZSIsIE5vbmUpIG9yICLigJQiLAogICAgICAgICAgICAgICAgZ2V0YXR0cihzLmVudGlkYWQsICJjb2RpZ28iLCBOb25lKSBvciAi4oCUIiwKICAgICAgICAgICAgICAgIHMucmVmZXJlbmNpYV9vcGVyYWNpb24sCiAgICAgICAgICAgICAgICB1biBvciAi4oCUIiwKICAgICAgICAgICAgICAgIGdldGF0dHIocy5wcm9kdWN0bywgImNvZGlnbyIsIE5vbmUpCiAgICAgICAgICAgICAgICBvciBnZXRhdHRyKHMucHJvZHVjdG8sICJub21icmUiLCBOb25lKQogICAgICAgICAgICAgICAgb3IgIuKAlCIsCiAgICAgICAgICAgICAgICBzLmZlY2hhX3NuYXBzaG90Lmlzb2Zvcm1hdCgpIGlmIHMuZmVjaGFfc25hcHNob3QgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0ocy5zYWxkbywgMiksCiAgICAgICAgICAgICAgICBzLmRpYXNfbW9yYSwKICAgICAgICAgICAgICAgIGZtdF9udW0ocy5tb250b19leGlnaWJsZSwgMiksCiAgICAgICAgICAgICAgICBzLm5pdmVsX3JpZXNnbywKICAgICAgICAgICAgICAgICJTw60iIGlmIHMuYWxlcnRhIGVsc2UgIk5vIiwKICAgICAgICAgICAgICAgIChzLmRldGFsbGUgb3IgIiIpWzoyMDBdLAogICAgICAgICAgICBdCiAgICAgICAgKQoKICAgIGFsZXJ0YXNfcm93cyA9IFtyIGZvciByIGluIGJhbG9uX3Jvd3MgaWYgclsxMF0gPT0gIlPDrSJdCiAgICBtb3JhX2FsdGFfcm93cyA9IHNvcnRlZCgKICAgICAgICBbciBmb3IgciBpbiBiYWxvbl9yb3dzIGlmIGlzaW5zdGFuY2Uocls3XSwgaW50KSBhbmQgcls3XSA+PSAzMF0sCiAgICAgICAga2V5PWxhbWJkYSB4OiB4WzddLAogICAgICAgIHJldmVyc2U9VHJ1ZSwKICAgICkKCiAgICBwYWdvc192ZW5jaWRvc19oZWFkZXJzID0gWwogICAgICAgICJFbnRpZGFkIiwKICAgICAgICAiUmVmZXJlbmNpYSIsCiAgICAgICAgIkZlY2hhIHByb2cuIiwKICAgICAgICAiTW9udG8iLAogICAgICAgICJNb25lZGEiLAogICAgICAgICJQcm9kdWN0byIsCiAgICAgICAgIkTDrWFzIHZlbmNpZG8iLAogICAgXQogICAgcGFnb3NfdmVuY2lkb3Nfcm93cyA9IFtdCiAgICBmb3IgciBpbiAoCiAgICAgICAgUHJvZ3JhbWFjaW9uUGFnby5vYmplY3RzLmZpbHRlcihmZWNoYV9wcm9ncmFtYWRhX19sdD10b2RheSkKICAgICAgICAuc2VsZWN0X3JlbGF0ZWQoImVudGlkYWQiLCAicHJvZHVjdG8iKQogICAgICAgIC5vcmRlcl9ieSgiZmVjaGFfcHJvZ3JhbWFkYSIpCiAgICApOgogICAgICAgIGRpYXMgPSAodG9kYXkgLSByLmZlY2hhX3Byb2dyYW1hZGEpLmRheXMgaWYgci5mZWNoYV9wcm9ncmFtYWRhIGVsc2UgIiIKICAgICAgICBwYWdvc192ZW5jaWRvc19yb3dzLmFwcGVuZCgKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgZ2V0YXR0cihyLmVudGlkYWQsICJjb2RpZ28iLCBOb25lKSBvciAi4oCUIiwKICAgICAgICAgICAgICAgIHIucmVmZXJlbmNpYSwKICAgICAgICAgICAgICAgIHIuZmVjaGFfcHJvZ3JhbWFkYS5pc29mb3JtYXQoKSBpZiByLmZlY2hhX3Byb2dyYW1hZGEgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0oci5tb250bywgMiksCiAgICAgICAgICAgICAgICByLm1vbmVkYSwKICAgICAgICAgICAgICAgIGdldGF0dHIoci5wcm9kdWN0bywgImNvZGlnbyIsIE5vbmUpIG9yICLigJQiLAogICAgICAgICAgICAgICAgZGlhcywKICAgICAgICAgICAgXQogICAgICAgICkKCiAgICBzbmFwX2hlYWRlcnMgPSBbCiAgICAgICAgIkZlY2hhIiwKICAgICAgICAiUGVyaW9kbyIsCiAgICAgICAgIkVudGlkYWQiLAogICAgICAgICJQcm9kdWN0byIsCiAgICAgICAgIk9wZXJhY2nDs24iLAogICAgICAgICJOaXZlbCIsCiAgICAgICAgIkTDrWFzIG1vcmEiLAogICAgICAgICJTYWxkbyIsCiAgICAgICAgIkV4aWdpYmxlIiwKICAgICAgICAiQWxlcnRhIiwKICAgICAgICAiRGV0YWxsZSIsCiAgICBdCiAgICBzbmFwX3Jvd3MgPSBbXQogICAgZm9yIHMgaW4gKAogICAgICAgIFJpc2tPcGVyYXRpb25TbmFwc2hvdC5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJlbnRpZGFkIiwgInByb2R1Y3RvIikKICAgICAgICAub3JkZXJfYnkoIi1mZWNoYV9zbmFwc2hvdCIsICJlbnRpZGFkX19jb2RpZ28iLCAicmVmZXJlbmNpYV9vcGVyYWNpb24iKQogICAgKToKICAgICAgICBzbmFwX3Jvd3MuYXBwZW5kKAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICBzLmZlY2hhX3NuYXBzaG90Lmlzb2Zvcm1hdCgpIGlmIHMuZmVjaGFfc25hcHNob3QgZWxzZSAiIiwKICAgICAgICAgICAgICAgIF95bShzLmZlY2hhX3NuYXBzaG90KSwKICAgICAgICAgICAgICAgIGdldGF0dHIocy5lbnRpZGFkLCAiY29kaWdvIiwgTm9uZSkKICAgICAgICAgICAgICAgIG9yIGdldGF0dHIocy5lbnRpZGFkLCAibm9tYnJlIiwgIiIpCiAgICAgICAgICAgICAgICBvciAi4oCUIiwKICAgICAgICAgICAgICAgIGdldGF0dHIocy5wcm9kdWN0bywgImNvZGlnbyIsIE5vbmUpCiAgICAgICAgICAgICAgICBvciBnZXRhdHRyKHMucHJvZHVjdG8sICJub21icmUiLCAiIikKICAgICAgICAgICAgICAgIG9yICLigJQiLAogICAgICAgICAgICAgICAgcy5yZWZlcmVuY2lhX29wZXJhY2lvbiwKICAgICAgICAgICAgICAgIHMubml2ZWxfcmllc2dvLAogICAgICAgICAgICAgICAgcy5kaWFzX21vcmEsCiAgICAgICAgICAgICAgICBmbXRfbnVtKHMuc2FsZG8sIDIpLAogICAgICAgICAgICAgICAgZm10X251bShzLm1vbnRvX2V4aWdpYmxlLCAyKSwKICAgICAgICAgICAgICAgICJTw60iIGlmIHMuYWxlcnRhIGVsc2UgIk5vIiwKICAgICAgICAgICAgICAgIHMuZGV0YWxsZSBvciAiIiwKICAgICAgICAgICAgXQogICAgICAgICkKCiAgICBuaXZlbF9yb3dzID0gbGlzdCgKICAgICAgICBSaXNrT3BlcmF0aW9uU25hcHNob3Qub2JqZWN0cy52YWx1ZXMoIm5pdmVsX3JpZXNnbyIpCiAgICAgICAgLmFubm90YXRlKG49Q291bnQoImlkIiksIHNhbGRvPVN1bSgic2FsZG8iKSkKICAgICAgICAub3JkZXJfYnkoIm5pdmVsX3JpZXNnbyIpCiAgICApCgogICAgZWZfaGVhZGVycyA9IFsiUGVyaW9kbyIsICJFbnRpZGFkIiwgIlNhbGRvIHRvdGFsIiwgIk1vcmEgZMOtYXMiLCAiRXhwb3NpY2nDs24iLCAiTm90YXMiXQogICAgZWZfcm93cyA9IFtdCiAgICBmb3IgZSBpbiBFc3RhZG9GaW5hbmNpZXJvLm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoImVudGlkYWQiKS5vcmRlcl9ieSgKICAgICAgICAiLXBlcmlvZG8iLCAiZW50aWRhZF9fY29kaWdvIgogICAgKToKICAgICAgICBlZl9yb3dzLmFwcGVuZCgKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgZS5wZXJpb2RvLAogICAgICAgICAgICAgICAgZ2V0YXR0cihlLmVudGlkYWQsICJjb2RpZ28iLCBOb25lKSBvciAi4oCUIiwKICAgICAgICAgICAgICAgIGZtdF9udW0oZS5zYWxkb190b3RhbCwgMiksCiAgICAgICAgICAgICAgICBlLm1vcmFfZGlhcywKICAgICAgICAgICAgICAgIGZtdF9udW0oZS5leHBvc2ljaW9uLCAyKSwKICAgICAgICAgICAgICAgIGUubm90YXMgb3IgIiIsCiAgICAgICAgICAgIF0KICAgICAgICApCgogICAgcHJvZ19oZWFkZXJzID0gWyJFbnRpZGFkIiwgIlJlZmVyZW5jaWEiLCAiRmVjaGEgcHJvZy4iLCAiTW9udG8iLCAiTW9uZWRhIiwgIlByb2R1Y3RvIl0KICAgIHByb2dfcm93cyA9IFtdCiAgICBmb3IgciBpbiBQcm9ncmFtYWNpb25QYWdvLm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoImVudGlkYWQiLCAicHJvZHVjdG8iKS5vcmRlcl9ieSgKICAgICAgICAiZmVjaGFfcHJvZ3JhbWFkYSIKICAgICk6CiAgICAgICAgcHJvZ19yb3dzLmFwcGVuZCgKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgZ2V0YXR0cihyLmVudGlkYWQsICJjb2RpZ28iLCBOb25lKSBvciAi4oCUIiwKICAgICAgICAgICAgICAgIHIucmVmZXJlbmNpYSwKICAgICAgICAgICAgICAgIHIuZmVjaGFfcHJvZ3JhbWFkYS5pc29mb3JtYXQoKSBpZiByLmZlY2hhX3Byb2dyYW1hZGEgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0oci5tb250bywgMiksCiAgICAgICAgICAgICAgICByLm1vbmVkYSwKICAgICAgICAgICAgICAgIGdldGF0dHIoci5wcm9kdWN0bywgImNvZGlnbyIsIE5vbmUpIG9yICLigJQiLAogICAgICAgICAgICBdCiAgICAgICAgKQoKICAgIHBhZ29faGVhZGVycyA9IFsiRW50aWRhZCIsICJSZWZlcmVuY2lhIiwgIkZlY2hhIHBhZ28iLCAiTW9udG8iLCAiTW9uZWRhIl0KICAgIHBhZ29fcm93cyA9IFtdCiAgICBmb3IgciBpbiBQYWdvUmVhbGl6YWRvLm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoImVudGlkYWQiKS5vcmRlcl9ieSgiLWZlY2hhX3BhZ28iKToKICAgICAgICBwYWdvX3Jvd3MuYXBwZW5kKAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICBnZXRhdHRyKHIuZW50aWRhZCwgImNvZGlnbyIsIE5vbmUpIG9yICLigJQiLAogICAgICAgICAgICAgICAgci5yZWZlcmVuY2lhLAogICAgICAgICAgICAgICAgci5mZWNoYV9wYWdvLmlzb2Zvcm1hdCgpIGlmIHIuZmVjaGFfcGFnbyBlbHNlICIiLAogICAgICAgICAgICAgICAgZm10X251bShyLm1vbnRvLCAyKSwKICAgICAgICAgICAgICAgIHIubW9uZWRhLAogICAgICAgICAgICBdCiAgICAgICAgKQoKICAgIGNvbnRhY3RfaGVhZGVycyA9IFsiRW50aWRhZCIsICJOb21icmUiLCAiVGVsw6lmb25vIiwgIkVtYWlsIiwgIkFjdGl2byJdCiAgICBjb250YWN0X3Jvd3MgPSBbXQogICAgZm9yIGMgaW4gQ29udGFjdG9Db2JyYW56YS5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJlbnRpZGFkIikub3JkZXJfYnkoCiAgICAgICAgImVudGlkYWRfX2NvZGlnbyIsICJub21icmUiCiAgICApOgogICAgICAgIGNvbnRhY3Rfcm93cy5hcHBlbmQoCiAgICAgICAgICAgIFsKICAgICAgICAgICAgICAgIGdldGF0dHIoYy5lbnRpZGFkLCAiY29kaWdvIiwgTm9uZSkgb3IgIuKAlCIsCiAgICAgICAgICAgICAgICBjLm5vbWJyZSwKICAgICAgICAgICAgICAgIGMudGVsZWZvbm8sCiAgICAgICAgICAgICAgICBjLmVtYWlsLAogICAgICAgICAgICAgICAgIlPDrSIgaWYgYy5hY3Rpdm8gZWxzZSAiTm8iLAogICAgICAgICAgICBdCiAgICAgICAgKQoKICAgIGNhbWJpb3MgPSBbXQogICAgaWYgcHJldl9wOgogICAgICAgIGZvciBsYWJlbCwgYSwgYiBpbiBbCiAgICAgICAgICAgICgiQWxlcnRhcyIsIGN1cnJbImFsZXJ0YXMiXSwgcHJldlsiYWxlcnRhcyJdKSwKICAgICAgICAgICAgKCJTYWxkbyIsIGN1cnJbInNhbGRvIl0sIHByZXZbInNhbGRvIl0pLAogICAgICAgICAgICAoIkV4aWdpYmxlIiwgY3VyclsiZXhpZ2libGUiXSwgcHJldlsiZXhpZ2libGUiXSksCiAgICAgICAgICAgICgiQ3LDrXRpY29zIiwgY3VyclsiY3JpdGljb3MiXSwgcHJldlsiY3JpdGljb3MiXSksCiAgICAgICAgXToKICAgICAgICAgICAgY2FtYmlvcy5hcHBlbmQoCiAgICAgICAgICAgICAgICBmIntsYWJlbH06IHtmbXRfbnVtKGIsIDIpIGlmIG5vdCBpc2luc3RhbmNlKGIsIGludCkgZWxzZSBifSDihpIgIgogICAgICAgICAgICAgICAgZiJ7Zm10X251bShhLCAyKSBpZiBub3QgaXNpbnN0YW5jZShhLCBpbnQpIGVsc2UgYX0gKHtwY3RfY2hhbmdlKGEsIGIpfSkiCiAgICAgICAgICAgICkKCiAgICB3Y2dfbWQsIHdjZ19zaGVldHMsIHdjZ19oZWNob3MsIHdjZ192YWNpb3MgPSBfd2NnX3Jpc2tfYmxvY2soKQoKICAgIGhlY2hvcyA9IFsKICAgICAgICBmIlNuYXBzaG90cyBoaXN0w7NyaWNvOiB7bGVuKHNuYXBfcm93cyl9IiwKICAgICAgICBmIk9wcyBlbiBDb21hbmRvIEJhbMOzbiAow7psdGltYXMpOiB7bGVuKGJhbG9uX3Jvd3MpfSIsCiAgICAgICAgZiJBbGVydGFzIGFjdGl2YXMgKMO6bHRpbWEgZm90byk6IHtsZW4oYWxlcnRhc19yb3dzKX0iLAogICAgICAgIGYiTW9yYSDiiaUzMCBkw61hcyAow7psdGltYSBmb3RvKToge2xlbihtb3JhX2FsdGFfcm93cyl9IiwKICAgICAgICBmIlBhZ29zIHByb2dyYW1hZG9zIHZlbmNpZG9zOiB7bGVuKHBhZ29zX3ZlbmNpZG9zX3Jvd3MpfSIsCiAgICAgICAgZiJFc3RhZG9zIGZpbmFuY2llcm9zOiB7bGVuKGVmX3Jvd3MpfSIsCiAgICAgICAgZiJQcm9ncmFtYWNpb25lcyBwYWdvOiB7bGVuKHByb2dfcm93cyl9IiwKICAgICAgICBmIlBhZ29zIHJlYWxpemFkb3M6IHtsZW4ocGFnb19yb3dzKX0iLAogICAgICAgIGYiQ29udGFjdG9zIGNvYnJhbnphOiB7bGVuKGNvbnRhY3Rfcm93cyl9IiwKICAgICAgICBmIsOabHRpbW8gbWVzIHNuYXBzaG90OiB7Y3Vycl9wIG9yICduL2QnfSIsCiAgICAgICAgZiJNZXMgYW50ZXJpb3I6IHtwcmV2X3Agb3IgJ24vZCd9IiwKICAgICAgICAqd2NnX2hlY2hvcywKICAgIF0KICAgIHZhY2lvcyA9IGxpc3Qod2NnX3ZhY2lvcykKICAgIGlmIG5vdCBzbmFwX3Jvd3M6CiAgICAgICAgdmFjaW9zLmFwcGVuZCgiU2luIFJpc2tPcGVyYXRpb25TbmFwc2hvdCBwcm9kdWN0aXZvLiIpCiAgICBpZiBub3QgZWZfcm93czoKICAgICAgICB2YWNpb3MuYXBwZW5kKCJTaW4gRXN0YWRvRmluYW5jaWVybyBwcm9kdWN0aXZvLiIpCiAgICBpZiBub3QgcHJldl9wOgogICAgICAgIHZhY2lvcy5hcHBlbmQoIlNpbiBtZXMgYW50ZXJpb3IgZGUgc25hcHNob3RzIHBhcmEgY29tcGFyYXIuIikKCiAgICBtZF9wYXJ0cyA9IFsKICAgICAgICBoMSgiUmVwb3J0ZSBkZSByZXN1bHRhZG9zIEIuIFJpZXNnbyAoZXh0ZW5zbykiKSwKICAgICAgICBwKHN0YW1wX2xhYmVsKSwKICAgICAgICBwKAogICAgICAgICAgICAiUHJvcMOzc2l0bzogaW52ZW50YXJpbyBkZXRhbGxhZG8gZGUgcmllc2dvIHBhcmEgSUEgZXN0cmF0w6lnaWNhIHkgRXhjZWwuICIKICAgICAgICAgICAgIkNSTSBubyBzZSBpbmNsdXllLiIKICAgICAgICApLAogICAgICAgIGgyKCJJbmZvcm1hY2nDs24gdXNhZGEgeSBwcm9jZXNvIiksCiAgICAgICAgcChSSVNLX0VYUExBSU4pLAogICAgICAgIGgyKCJLUElzIMO6bHRpbW8gbWVzIHZzIGFudGVyaW9yIiksCiAgICAgICAgcChmIsOabHRpbW86ICoqe2N1cnJfcCBvciAnbi9kJ30qKiDCtyBBbnRlcmlvcjogKip7cHJldl9wIG9yICduL2QnfSoqIiksCiAgICAgICAgbWRfdGFibGUoa3BpX2hlYWRlcnMsIGtwaV9yb3dzKSwKICAgICAgICBoMigiU2VyaWUgbWVuc3VhbCBkZSBjaWZyYXMgYmFzZSAocGFyYSB0ZW5kZW5jaWEgLyBncsOhZmljb3MpIiksCiAgICAgICAgcCgKICAgICAgICAgICAgIkFncmVnYWRvcyBwb3IgbWVzIGRlIHNuYXBzaG90IOKAlCBlcXVpdmFsZW50ZXMgYSBsYSBiYXNlIG51bcOpcmljYSBxdWUgIgogICAgICAgICAgICAic29wb3J0YXLDrWEgY2hhcnRzIGRlIHNhbGRvLCBleGlnaWJsZSwgYWxlcnRhcyB5IGNvbmNlbnRyYWNpw7NuIGRlIHJpZXNnby4iCiAgICAgICAgKSwKICAgICAgICBtZF90YWJsZShzZXJpZV9oZWFkZXJzLCBzZXJpZV9yb3dzKSBpZiBzZXJpZV9yb3dzIGVsc2UgcCgiX1NpbiBzZXJpZSBtZW5zdWFsLl8iKSwKICAgICAgICBoMigiQ2FtYmlvcyByZWxldmFudGVzIiksCiAgICAgICAgYnVsbGV0cyhjYW1iaW9zIG9yIFsiU2luIGNvbXBhcmFjacOzbiBkZSBtZXNlcy4iXSksCiAgICAgICAgaDIoIkNvbWFuZG8gQmFsw7NuIOKAlCDDumx0aW1vIHNuYXBzaG90IHBvciBvcGVyYWNpw7NuIiksCiAgICAgICAgcCgKICAgICAgICAgICAgIk1pc21hIGzDs2dpY2EgcXVlIGAvcmlzay9gOiB1biByZW5nbMOzbiBwb3IgKGNsaWVudGUsIG9wZXJhY2nDs24pIGNvbiBsYSAiCiAgICAgICAgICAgIGYiZmVjaGEgZGUgc25hcHNob3QgbcOhcyByZWNpZW50ZS4gRmlsYXM6ICoqe2xlbihiYWxvbl9yb3dzKX0qKi4iCiAgICAgICAgKSwKICAgICAgICBtZF90YWJsZShiYWxvbl9oZWFkZXJzLCBiYWxvbl9yb3dzKSBpZiBiYWxvbl9yb3dzIGVsc2UgcCgiX1NpbiBvcGVyYWNpb25lcy5fIiksCiAgICAgICAgaDIoIlBhbmVsIGRlIGFsZXJ0YXMgKMO6bHRpbWEgZm90bykiKSwKICAgICAgICBwKGYiT3BlcmFjaW9uZXMgY29uIGBhbGVydGE9U8OtYDogKip7bGVuKGFsZXJ0YXNfcm93cyl9KiouIiksCiAgICAgICAgbWRfdGFibGUoYmFsb25faGVhZGVycywgYWxlcnRhc19yb3dzKSBpZiBhbGVydGFzX3Jvd3MgZWxzZSBwKCJfU2luIGFsZXJ0YXMuXyIpLAogICAgICAgIGgyKCJNb3JhIGFsdGEgKOKJpSAzMCBkw61hcywgw7psdGltYSBmb3RvKSIpLAogICAgICAgIG1kX3RhYmxlKGJhbG9uX2hlYWRlcnMsIG1vcmFfYWx0YV9yb3dzKQogICAgICAgIGlmIG1vcmFfYWx0YV9yb3dzCiAgICAgICAgZWxzZSBwKCJfU2luIG1vcmEg4omlMzAgZMOtYXMuXyIpLAogICAgICAgIGgyKCJQYWdvcyBwcm9ncmFtYWRvcyB2ZW5jaWRvcyIpLAogICAgICAgIG1kX3RhYmxlKHBhZ29zX3ZlbmNpZG9zX2hlYWRlcnMsIHBhZ29zX3ZlbmNpZG9zX3Jvd3MpCiAgICAgICAgaWYgcGFnb3NfdmVuY2lkb3Nfcm93cwogICAgICAgIGVsc2UgcCgiX1NpbiBwYWdvcyB2ZW5jaWRvcy5fIiksCiAgICAgICAgaDIoIkNvbmNlbnRyYWNpw7NuIHBvciBuaXZlbCAoaGlzdMOzcmljbyBkZSBzbmFwc2hvdHMpIiksCiAgICAgICAgbWRfdGFibGUoCiAgICAgICAgICAgIFsiTml2ZWwiLCAiT3BzIiwgIlNhbGRvIl0sCiAgICAgICAgICAgIFtbclsibml2ZWxfcmllc2dvIl0sIHJbIm4iXSwgZm10X251bShyWyJzYWxkbyJdIG9yIDAsIDIpXSBmb3IgciBpbiBuaXZlbF9yb3dzXSwKICAgICAgICApCiAgICAgICAgaWYgbml2ZWxfcm93cwogICAgICAgIGVsc2UgcCgiX1NpbiBkYXRvcy5fIiksCiAgICAgICAgaDIoIkRldGFsbGUgY29tcGxldG8gaGlzdMOzcmljbyBkZSBzbmFwc2hvdHMiKSwKICAgICAgICBwKGYiUmVnaXN0cm9zOiAqKntsZW4oc25hcF9yb3dzKX0qKiAodG9kYXMgbGFzIGZlY2hhcywgbm8gc29sbyBsYSDDumx0aW1hKS4iKSwKICAgICAgICBtZF90YWJsZShzbmFwX2hlYWRlcnMsIHNuYXBfcm93cykgaWYgc25hcF9yb3dzIGVsc2UgcCgiX1NpbiBzbmFwc2hvdHMuXyIpLAogICAgICAgIGgyKCJFc3RhZG9zIGZpbmFuY2llcm9zIChwcm9kdWN0aXZvKSIpLAogICAgICAgIHAoZiJSZWdpc3Ryb3M6ICoqe2xlbihlZl9yb3dzKX0qKi4iKSwKICAgICAgICBtZF90YWJsZShlZl9oZWFkZXJzLCBlZl9yb3dzKSBpZiBlZl9yb3dzIGVsc2UgcCgiX1NpbiBlc3RhZG9zIGZpbmFuY2llcm9zLl8iKSwKICAgICAgICBoMigiUHJvZ3JhbWFjacOzbiBkZSBwYWdvcyAocHJvZHVjdGl2bykiKSwKICAgICAgICBtZF90YWJsZShwcm9nX2hlYWRlcnMsIHByb2dfcm93cykgaWYgcHJvZ19yb3dzIGVsc2UgcCgiX1NpbiBwcm9ncmFtYWNpb25lcy5fIiksCiAgICAgICAgaDIoIlBhZ29zIHJlYWxpemFkb3MgKHByb2R1Y3Rpdm8pIiksCiAgICAgICAgbWRfdGFibGUocGFnb19oZWFkZXJzLCBwYWdvX3Jvd3MpIGlmIHBhZ29fcm93cyBlbHNlIHAoIl9TaW4gcGFnb3MuXyIpLAogICAgICAgIGgyKCJDb250YWN0b3MgZGUgY29icmFuemEgKGRpcmVjdG9yaW8gcHJvZHVjdGl2bykiKSwKICAgICAgICBtZF90YWJsZShjb250YWN0X2hlYWRlcnMsIGNvbnRhY3Rfcm93cykgaWYgY29udGFjdF9yb3dzIGVsc2UgcCgiX1NpbiBjb250YWN0b3MuXyIpLAogICAgICAgICp3Y2dfbWQsCiAgICAgICAgaDIoIkludmVudGFyaW8iKSwKICAgICAgICBidWxsZXRzKGhlY2hvcyksCiAgICAgICAgaDIoIkd1w61hIGRlIGFuw6FsaXNpcyBlc3RyYXTDqWdpY28gKElBKSIpLAogICAgICAgIHAoCiAgICAgICAgICAgICJDb25zdHJ1eWUgdW4gZGlhZ27Ds3N0aWNvIGRlIHJpZXNnbyBjcmVkaXRpY2lvL29wZXJhdGl2bzogIgogICAgICAgICAgICAiKDEpIMK/bWVqb3JhIG8gZW1wZW9yYSBsYSBtb3JhLCBlbCBzYWxkbyBleGlnaWJsZSB5IGxhcyBhbGVydGFzIG1lcyBhIG1lcz87ICIKICAgICAgICAgICAgIigyKSDCv2TDs25kZSBzZSBjb25jZW50cmEgZWwgcmllc2dvIChuaXZlbGVzIEFMVE8vQ1JJVElDTywgY2xpZW50ZXMpPzsgIgogICAgICAgICAgICAiKDMpIMK/aGF5IHBhZ29zIHZlbmNpZG9zIG8gY2xpZW50ZXMgc2luIGNvbnRhY3RvIGRlIGNvYnJhbnphPzsgIgogICAgICAgICAgICAiKDQpIHJlY29tZW5kYWNpb25lcyBkZSBzZWd1aW1pZW50byAocHJpb3JpemFyIGNyw610aWNvcywgcmVndWxhcml6YXIgIgogICAgICAgICAgICAicHJvZ3JhbWFjaW9uZXMsIHJlZm9yemFyIGNvYnJhbnphKS4gQ2l0YSBjaWZyYXMuIE5vIGludmVudGVzIHVtYnJhbGVzICIKICAgICAgICAgICAgIm5pIGNsYXNpZmljYWNpb25lcyBhdXNlbnRlcyBlbiBsb3MgZGF0b3MuIgogICAgICAgICksCiAgICBdCiAgICBpZiBjZmcuaW5jbHVkZV9haV9zZWN0aW9uOgogICAgICAgIG1kX3BhcnRzLmFwcGVuZCgKICAgICAgICAgICAgYWlfY2xvc2luZygKICAgICAgICAgICAgICAgIGhlY2hvcywKICAgICAgICAgICAgICAgIGNhbWJpb3NbOjIwXSBpZiBjZmcuaW5jbHVkZV9wZXJpb2RfY29tcGFyaXNvbiBlbHNlIFsiQ29tcGFyYWNpw7NuIGRlc2FjdGl2YWRhLiJdLAogICAgICAgICAgICAgICAgdmFjaW9zIG9yIFsiU2luIHZhY8Otb3MgY3LDrXRpY29zIGFkaWNpb25hbGVzLiJdLAogICAgICAgICAgICApCiAgICAgICAgKQoKICAgIHNoZWV0cyA9IFsKICAgICAgICBfc2hlZXQoIktQSXMiLCBmIktQSXMge2N1cnJfcH0gdnMge3ByZXZfcH0iLCBrcGlfaGVhZGVycywga3BpX3Jvd3MpLAogICAgICAgIF9zaGVldCgiU2VyaWUgbWVuc3VhbCIsICJDaWZyYXMgYmFzZSB0ZW5kZW5jaWEiLCBzZXJpZV9oZWFkZXJzLCBzZXJpZV9yb3dzKSwKICAgICAgICBfc2hlZXQoIkNvbWFuZG8gQmFsb24iLCAiw5psdGltbyBzbmFwc2hvdCBwb3Igb3AiLCBiYWxvbl9oZWFkZXJzLCBiYWxvbl9yb3dzKSwKICAgICAgICBfc2hlZXQoIkFsZXJ0YXMiLCAiT3BzIGNvbiBhbGVydGEiLCBiYWxvbl9oZWFkZXJzLCBhbGVydGFzX3Jvd3MpLAogICAgICAgIF9zaGVldCgiTW9yYSBhbHRhIiwgIk1vcmEgPj0gMzAiLCBiYWxvbl9oZWFkZXJzLCBtb3JhX2FsdGFfcm93cyksCiAgICAgICAgX3NoZWV0KAogICAgICAgICAgICAiUGFnb3MgdmVuY2lkb3MiLAogICAgICAgICAgICAiUHJvZ3JhbWFjaW9uUGFnbyB2ZW5jaWRhIiwKICAgICAgICAgICAgcGFnb3NfdmVuY2lkb3NfaGVhZGVycywKICAgICAgICAgICAgcGFnb3NfdmVuY2lkb3Nfcm93cywKICAgICAgICApLAogICAgICAgIF9zaGVldCgiU25hcHNob3RzIGhpc3QiLCAiUmlza09wZXJhdGlvblNuYXBzaG90Iiwgc25hcF9oZWFkZXJzLCBzbmFwX3Jvd3MpLAogICAgICAgIF9zaGVldCgKICAgICAgICAgICAgIlBvciBuaXZlbCIsCiAgICAgICAgICAgICJDb25jZW50cmFjacOzbiIsCiAgICAgICAgICAgIFsiTml2ZWwiLCAiT3BzIiwgIlNhbGRvIl0sCiAgICAgICAgICAgIFtbclsibml2ZWxfcmllc2dvIl0sIHJbIm4iXSwgZmxvYXQoclsic2FsZG8iXSBvciAwKV0gZm9yIHIgaW4gbml2ZWxfcm93c10sCiAgICAgICAgKSwKICAgICAgICBfc2hlZXQoIkVzdGFkb3MgZmluYW5jaWVyb3MiLCAiRXN0YWRvRmluYW5jaWVybyIsIGVmX2hlYWRlcnMsIGVmX3Jvd3MpLAogICAgICAgIF9zaGVldCgiUHJvZ3JhbWFjaW9uIHBhZ29zIiwgIlByb2dyYW1hY2lvblBhZ28iLCBwcm9nX2hlYWRlcnMsIHByb2dfcm93cyksCiAgICAgICAgX3NoZWV0KCJQYWdvcyIsICJQYWdvUmVhbGl6YWRvIiwgcGFnb19oZWFkZXJzLCBwYWdvX3Jvd3MpLAogICAgICAgIF9zaGVldCgiQ29udGFjdG9zIiwgIkNvbnRhY3RvQ29icmFuemEiLCBjb250YWN0X2hlYWRlcnMsIGNvbnRhY3Rfcm93cyksCiAgICAgICAgKndjZ19zaGVldHMsCiAgICBdCgogICAgcmV0dXJuIHsKICAgICAgICAibWQiOiBqb2luX3NlY3Rpb25zKCptZF9wYXJ0cyksCiAgICAgICAgInNoZWV0cyI6IHNoZWV0cywKICAgICAgICAic3RhbXAiOiBzdGFtcCwKICAgICAgICAic3RhbXBfbGFiZWwiOiBzdGFtcF9sYWJlbCwKICAgICAgICAicGVyaW9kIjogY3Vycl9wLAogICAgICAgICJwcmV2X3BlcmlvZCI6IHByZXZfcCwKICAgIH0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/tests.py
PATH_JSON="reports/tests.py"
FILENAME=tests.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=88
SIZE_BYTES_UTF8=3331
CONTENT_SHA256=f97b6a02e4cbb6db1f8e2fae055ef73e7484db037600b9d9b7de8dbe59b64bdb
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from reports.md_utils import h2, join_sections, md_table, normalize_markdown, p
from reports.naming import stamp_filename, report_stamp
from reports.services import generate_report_package


class ReportNamingTests(TestCase):
    def test_stamp_pattern(self):
        name = stamp_filename("reporte_pgc", "md")
        # e.g. reporte_pgc 26-07 16-05.md
        self.assertRegex(name, r"^reporte_pgc \d{2}-\d{2} \d{2}-\d{2}\.md$")
        self.assertTrue(report_stamp().startswith(" "))


class MarkdownFormatTests(TestCase):
    def test_blank_line_before_table(self):
        md = join_sections(
            h2("Clientes nuevos — detalle completo (browse)"),
            p("Equivalente al detalle visto en Administración. Registros: **40**."),
            md_table(
                ["Periodo", "UNE", "Cliente"],
                [["2026-01", "INVESTMENT", "EDGAR ESTUARDO ORTIZ FUENTES"]],
            ),
        )
        self.assertIn(
            "Registros: **40**.\n\n| Periodo | UNE | Cliente |",
            md,
        )
        self.assertIn("## Clientes nuevos — detalle completo (browse)\n\n", md)
        self.assertNotIn("\r", md)

    def test_normalize_inserts_blank_before_heading_and_table(self):
        broken = (
            "Intro sin blank.\n"
            "## Título pegado\n"
            "Párrafo.\n"
            "| A | B |\n"
            "| --- | --- |\n"
            "| 1 | 2 |\n"
            "### Otro título\n"
            "Fin."
        )
        fixed = normalize_markdown(broken)
        self.assertIn("Intro sin blank.\n\n## Título pegado\n\n", fixed)
        self.assertIn("Párrafo.\n\n| A | B |", fixed)
        self.assertIn("| 1 | 2 |\n\n### Otro título\n\nFin.", fixed)

    def test_pipe_and_newline_escaped_in_cells(self):
        table = md_table(["A"], [["x|y\nz"]])
        body_line = table.splitlines()[2]
        self.assertIn("x\\|y z", body_line)
        self.assertEqual(body_line, "| x\\|y z |")


class ReportGenerateTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="rep_tester", password="x", is_staff=True
        )

    def test_package_pgc_zip_or_files(self):
        name, content, ctype = generate_report_package(["pgc"])
        self.assertTrue(name.endswith(".zip") or name.endswith(".md") or name.endswith(".xlsx"))
        # pgc produces md+xlsx → zip
        self.assertTrue(name.endswith(".zip"))
        self.assertEqual(ctype, "application/zip")
        self.assertGreater(len(content), 50)

    def test_endpoint_requires_areas(self):
        self.client.force_login(self.user)
        url = reverse("reports:generate")
        resp = self.client.post(
            url, data='{"areas":[]}', content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

    def test_endpoint_generate_admin(self):
        self.client.force_login(self.user)
        url = reverse("reports:generate")
        resp = self.client.post(
            url, data='{"areas":["admin"]}', content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("attachment", resp.get("Content-Disposition", ""))

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.test import TestCase
00002|from django.contrib.auth import get_user_model
00003|from django.urls import reverse
00004|
00005|from reports.md_utils import h2, join_sections, md_table, normalize_markdown, p
00006|from reports.naming import stamp_filename, report_stamp
00007|from reports.services import generate_report_package
00008|
00009|
00010|class ReportNamingTests(TestCase):
00011|    def test_stamp_pattern(self):
00012|        name = stamp_filename("reporte_pgc", "md")
00013|        # e.g. reporte_pgc 26-07 16-05.md
00014|        self.assertRegex(name, r"^reporte_pgc \d{2}-\d{2} \d{2}-\d{2}\.md$")
00015|        self.assertTrue(report_stamp().startswith(" "))
00016|
00017|
00018|class MarkdownFormatTests(TestCase):
00019|    def test_blank_line_before_table(self):
00020|        md = join_sections(
00021|            h2("Clientes nuevos — detalle completo (browse)"),
00022|            p("Equivalente al detalle visto en Administración. Registros: **40**."),
00023|            md_table(
00024|                ["Periodo", "UNE", "Cliente"],
00025|                [["2026-01", "INVESTMENT", "EDGAR ESTUARDO ORTIZ FUENTES"]],
00026|            ),
00027|        )
00028|        self.assertIn(
00029|            "Registros: **40**.\n\n| Periodo | UNE | Cliente |",
00030|            md,
00031|        )
00032|        self.assertIn("## Clientes nuevos — detalle completo (browse)\n\n", md)
00033|        self.assertNotIn("\r", md)
00034|
00035|    def test_normalize_inserts_blank_before_heading_and_table(self):
00036|        broken = (
00037|            "Intro sin blank.\n"
00038|            "## Título pegado\n"
00039|            "Párrafo.\n"
00040|            "| A | B |\n"
00041|            "| --- | --- |\n"
00042|            "| 1 | 2 |\n"
00043|            "### Otro título\n"
00044|            "Fin."
00045|        )
00046|        fixed = normalize_markdown(broken)
00047|        self.assertIn("Intro sin blank.\n\n## Título pegado\n\n", fixed)
00048|        self.assertIn("Párrafo.\n\n| A | B |", fixed)
00049|        self.assertIn("| 1 | 2 |\n\n### Otro título\n\nFin.", fixed)
00050|
00051|    def test_pipe_and_newline_escaped_in_cells(self):
00052|        table = md_table(["A"], [["x|y\nz"]])
00053|        body_line = table.splitlines()[2]
00054|        self.assertIn("x\\|y z", body_line)
00055|        self.assertEqual(body_line, "| x\\|y z |")
00056|
00057|
00058|class ReportGenerateTests(TestCase):
00059|    def setUp(self):
00060|        User = get_user_model()
00061|        self.user = User.objects.create_user(
00062|            username="rep_tester", password="x", is_staff=True
00063|        )
00064|
00065|    def test_package_pgc_zip_or_files(self):
00066|        name, content, ctype = generate_report_package(["pgc"])
00067|        self.assertTrue(name.endswith(".zip") or name.endswith(".md") or name.endswith(".xlsx"))
00068|        # pgc produces md+xlsx → zip
00069|        self.assertTrue(name.endswith(".zip"))
00070|        self.assertEqual(ctype, "application/zip")
00071|        self.assertGreater(len(content), 50)
00072|
00073|    def test_endpoint_requires_areas(self):
00074|        self.client.force_login(self.user)
00075|        url = reverse("reports:generate")
00076|        resp = self.client.post(
00077|            url, data='{"areas":[]}', content_type="application/json"
00078|        )
00079|        self.assertEqual(resp.status_code, 400)
00080|
00081|    def test_endpoint_generate_admin(self):
00082|        self.client.force_login(self.user)
00083|        url = reverse("reports:generate")
00084|        resp = self.client.post(
00085|            url, data='{"areas":["admin"]}', content_type="application/json"
00086|        )
00087|        self.assertEqual(resp.status_code, 200)
00088|        self.assertIn("attachment", resp.get("Content-Disposition", ""))

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udGVzdCBpbXBvcnQgVGVzdENhc2UKZnJvbSBkamFuZ28uY29udHJpYi5hdXRoIGltcG9ydCBnZXRfdXNlcl9tb2RlbApmcm9tIGRqYW5nby51cmxzIGltcG9ydCByZXZlcnNlCgpmcm9tIHJlcG9ydHMubWRfdXRpbHMgaW1wb3J0IGgyLCBqb2luX3NlY3Rpb25zLCBtZF90YWJsZSwgbm9ybWFsaXplX21hcmtkb3duLCBwCmZyb20gcmVwb3J0cy5uYW1pbmcgaW1wb3J0IHN0YW1wX2ZpbGVuYW1lLCByZXBvcnRfc3RhbXAKZnJvbSByZXBvcnRzLnNlcnZpY2VzIGltcG9ydCBnZW5lcmF0ZV9yZXBvcnRfcGFja2FnZQoKCmNsYXNzIFJlcG9ydE5hbWluZ1Rlc3RzKFRlc3RDYXNlKToKICAgIGRlZiB0ZXN0X3N0YW1wX3BhdHRlcm4oc2VsZik6CiAgICAgICAgbmFtZSA9IHN0YW1wX2ZpbGVuYW1lKCJyZXBvcnRlX3BnYyIsICJtZCIpCiAgICAgICAgIyBlLmcuIHJlcG9ydGVfcGdjIDI2LTA3IDE2LTA1Lm1kCiAgICAgICAgc2VsZi5hc3NlcnRSZWdleChuYW1lLCByIl5yZXBvcnRlX3BnYyBcZHsyfS1cZHsyfSBcZHsyfS1cZHsyfVwubWQkIikKICAgICAgICBzZWxmLmFzc2VydFRydWUocmVwb3J0X3N0YW1wKCkuc3RhcnRzd2l0aCgiICIpKQoKCmNsYXNzIE1hcmtkb3duRm9ybWF0VGVzdHMoVGVzdENhc2UpOgogICAgZGVmIHRlc3RfYmxhbmtfbGluZV9iZWZvcmVfdGFibGUoc2VsZik6CiAgICAgICAgbWQgPSBqb2luX3NlY3Rpb25zKAogICAgICAgICAgICBoMigiQ2xpZW50ZXMgbnVldm9zIOKAlCBkZXRhbGxlIGNvbXBsZXRvIChicm93c2UpIiksCiAgICAgICAgICAgIHAoIkVxdWl2YWxlbnRlIGFsIGRldGFsbGUgdmlzdG8gZW4gQWRtaW5pc3RyYWNpw7NuLiBSZWdpc3Ryb3M6ICoqNDAqKi4iKSwKICAgICAgICAgICAgbWRfdGFibGUoCiAgICAgICAgICAgICAgICBbIlBlcmlvZG8iLCAiVU5FIiwgIkNsaWVudGUiXSwKICAgICAgICAgICAgICAgIFtbIjIwMjYtMDEiLCAiSU5WRVNUTUVOVCIsICJFREdBUiBFU1RVQVJETyBPUlRJWiBGVUVOVEVTIl1dLAogICAgICAgICAgICApLAogICAgICAgICkKICAgICAgICBzZWxmLmFzc2VydEluKAogICAgICAgICAgICAiUmVnaXN0cm9zOiAqKjQwKiouXG5cbnwgUGVyaW9kbyB8IFVORSB8IENsaWVudGUgfCIsCiAgICAgICAgICAgIG1kLAogICAgICAgICkKICAgICAgICBzZWxmLmFzc2VydEluKCIjIyBDbGllbnRlcyBudWV2b3Mg4oCUIGRldGFsbGUgY29tcGxldG8gKGJyb3dzZSlcblxuIiwgbWQpCiAgICAgICAgc2VsZi5hc3NlcnROb3RJbigiXHIiLCBtZCkKCiAgICBkZWYgdGVzdF9ub3JtYWxpemVfaW5zZXJ0c19ibGFua19iZWZvcmVfaGVhZGluZ19hbmRfdGFibGUoc2VsZik6CiAgICAgICAgYnJva2VuID0gKAogICAgICAgICAgICAiSW50cm8gc2luIGJsYW5rLlxuIgogICAgICAgICAgICAiIyMgVMOtdHVsbyBwZWdhZG9cbiIKICAgICAgICAgICAgIlDDoXJyYWZvLlxuIgogICAgICAgICAgICAifCBBIHwgQiB8XG4iCiAgICAgICAgICAgICJ8IC0tLSB8IC0tLSB8XG4iCiAgICAgICAgICAgICJ8IDEgfCAyIHxcbiIKICAgICAgICAgICAgIiMjIyBPdHJvIHTDrXR1bG9cbiIKICAgICAgICAgICAgIkZpbi4iCiAgICAgICAgKQogICAgICAgIGZpeGVkID0gbm9ybWFsaXplX21hcmtkb3duKGJyb2tlbikKICAgICAgICBzZWxmLmFzc2VydEluKCJJbnRybyBzaW4gYmxhbmsuXG5cbiMjIFTDrXR1bG8gcGVnYWRvXG5cbiIsIGZpeGVkKQogICAgICAgIHNlbGYuYXNzZXJ0SW4oIlDDoXJyYWZvLlxuXG58IEEgfCBCIHwiLCBmaXhlZCkKICAgICAgICBzZWxmLmFzc2VydEluKCJ8IDEgfCAyIHxcblxuIyMjIE90cm8gdMOtdHVsb1xuXG5GaW4uIiwgZml4ZWQpCgogICAgZGVmIHRlc3RfcGlwZV9hbmRfbmV3bGluZV9lc2NhcGVkX2luX2NlbGxzKHNlbGYpOgogICAgICAgIHRhYmxlID0gbWRfdGFibGUoWyJBIl0sIFtbInh8eVxueiJdXSkKICAgICAgICBib2R5X2xpbmUgPSB0YWJsZS5zcGxpdGxpbmVzKClbMl0KICAgICAgICBzZWxmLmFzc2VydEluKCJ4XFx8eSB6IiwgYm9keV9saW5lKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwoYm9keV9saW5lLCAifCB4XFx8eSB6IHwiKQoKCmNsYXNzIFJlcG9ydEdlbmVyYXRlVGVzdHMoVGVzdENhc2UpOgogICAgZGVmIHNldFVwKHNlbGYpOgogICAgICAgIFVzZXIgPSBnZXRfdXNlcl9tb2RlbCgpCiAgICAgICAgc2VsZi51c2VyID0gVXNlci5vYmplY3RzLmNyZWF0ZV91c2VyKAogICAgICAgICAgICB1c2VybmFtZT0icmVwX3Rlc3RlciIsIHBhc3N3b3JkPSJ4IiwgaXNfc3RhZmY9VHJ1ZQogICAgICAgICkKCiAgICBkZWYgdGVzdF9wYWNrYWdlX3BnY196aXBfb3JfZmlsZXMoc2VsZik6CiAgICAgICAgbmFtZSwgY29udGVudCwgY3R5cGUgPSBnZW5lcmF0ZV9yZXBvcnRfcGFja2FnZShbInBnYyJdKQogICAgICAgIHNlbGYuYXNzZXJ0VHJ1ZShuYW1lLmVuZHN3aXRoKCIuemlwIikgb3IgbmFtZS5lbmRzd2l0aCgiLm1kIikgb3IgbmFtZS5lbmRzd2l0aCgiLnhsc3giKSkKICAgICAgICAjIHBnYyBwcm9kdWNlcyBtZCt4bHN4IOKGkiB6aXAKICAgICAgICBzZWxmLmFzc2VydFRydWUobmFtZS5lbmRzd2l0aCgiLnppcCIpKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwoY3R5cGUsICJhcHBsaWNhdGlvbi96aXAiKQogICAgICAgIHNlbGYuYXNzZXJ0R3JlYXRlcihsZW4oY29udGVudCksIDUwKQoKICAgIGRlZiB0ZXN0X2VuZHBvaW50X3JlcXVpcmVzX2FyZWFzKHNlbGYpOgogICAgICAgIHNlbGYuY2xpZW50LmZvcmNlX2xvZ2luKHNlbGYudXNlcikKICAgICAgICB1cmwgPSByZXZlcnNlKCJyZXBvcnRzOmdlbmVyYXRlIikKICAgICAgICByZXNwID0gc2VsZi5jbGllbnQucG9zdCgKICAgICAgICAgICAgdXJsLCBkYXRhPSd7ImFyZWFzIjpbXX0nLCBjb250ZW50X3R5cGU9ImFwcGxpY2F0aW9uL2pzb24iCiAgICAgICAgKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwocmVzcC5zdGF0dXNfY29kZSwgNDAwKQoKICAgIGRlZiB0ZXN0X2VuZHBvaW50X2dlbmVyYXRlX2FkbWluKHNlbGYpOgogICAgICAgIHNlbGYuY2xpZW50LmZvcmNlX2xvZ2luKHNlbGYudXNlcikKICAgICAgICB1cmwgPSByZXZlcnNlKCJyZXBvcnRzOmdlbmVyYXRlIikKICAgICAgICByZXNwID0gc2VsZi5jbGllbnQucG9zdCgKICAgICAgICAgICAgdXJsLCBkYXRhPSd7ImFyZWFzIjpbImFkbWluIl19JywgY29udGVudF90eXBlPSJhcHBsaWNhdGlvbi9qc29uIgogICAgICAgICkKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKHJlc3Auc3RhdHVzX2NvZGUsIDIwMCkKICAgICAgICBzZWxmLmFzc2VydEluKCJhdHRhY2htZW50IiwgcmVzcC5nZXQoIkNvbnRlbnQtRGlzcG9zaXRpb24iLCAiIikpCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/urls.py
PATH_JSON="reports/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=10
SIZE_BYTES_UTF8=218
CONTENT_SHA256=a65b6696065aba3f8ca6d4f23a15890714427d375442fabc4a0b7986eb846e0c
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("defaults/", views.report_defaults, name="defaults"),
    path("generate/", views.generate_reports, name="generate"),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.urls import path
00002|
00003|from . import views
00004|
00005|app_name = "reports"
00006|
00007|urlpatterns = [
00008|    path("defaults/", views.report_defaults, name="defaults"),
00009|    path("generate/", views.generate_reports, name="generate"),
00010|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aAoKZnJvbSAuIGltcG9ydCB2aWV3cwoKYXBwX25hbWUgPSAicmVwb3J0cyIKCnVybHBhdHRlcm5zID0gWwogICAgcGF0aCgiZGVmYXVsdHMvIiwgdmlld3MucmVwb3J0X2RlZmF1bHRzLCBuYW1lPSJkZWZhdWx0cyIpLAogICAgcGF0aCgiZ2VuZXJhdGUvIiwgdmlld3MuZ2VuZXJhdGVfcmVwb3J0cywgbmFtZT0iZ2VuZXJhdGUiKSwKXQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/views.py
PATH_JSON="reports/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=83
SIZE_BYTES_UTF8=2506
CONTENT_SHA256=b32cc8a5e0460601aaf34b44f0c0567a313f2ea290f0bb9589a4b1af2df1e652
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from __future__ import annotations

import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from reports.models import ReportConfig
from reports.services import (
    AREA_ADMIN,
    AREA_PGC,
    AREA_PGO,
    AREA_RISK,
    generate_report_package,
)


@login_required
@require_GET
def report_defaults(request):
    cfg = ReportConfig.get_active()
    return JsonResponse(
        {
            "ok": True,
            "defaults": {
                AREA_ADMIN: cfg.include_admin_by_default,
                AREA_PGC: cfg.include_pgc_by_default,
                AREA_PGO: cfg.include_pgo_by_default,
                AREA_RISK: cfg.include_risk_by_default,
            },
            "labels": {
                AREA_ADMIN: "Administración",
                AREA_PGC: "PGC",
                AREA_PGO: "PGO",
                AREA_RISK: "B. Riesgo",
            },
        }
    )


@login_required
@require_POST
def generate_reports(request):
    """
    Acepta application/json {areas:[...]} o form areas=admin&areas=pgc
    """
    areas: list[str] = []
    content_type = (request.content_type or "").lower()
    if "application/json" in content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return HttpResponseBadRequest("JSON inválido.")
        raw = payload.get("areas") or []
        if isinstance(raw, str):
            areas = [raw]
        else:
            areas = [str(a) for a in raw]
    else:
        areas = request.POST.getlist("areas")

    areas = [a.strip().lower() for a in areas if str(a).strip()]
    if not areas:
        return JsonResponse(
            {"ok": False, "error": "Seleccione al menos un área (Administración, PGC, PGO o B. Riesgo)."},
            status=400,
        )

    try:
        filename, content, ctype = generate_report_package(areas)
    except ValueError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=400)
    except Exception as exc:
        return JsonResponse(
            {"ok": False, "error": f"Error al generar reportes: {exc}"},
            status=500,
        )

    response = HttpResponse(content, content_type=ctype)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    response["X-Report-Filename"] = filename
    return response

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from __future__ import annotations
00002|
00003|import json
00004|
00005|from django.contrib.auth.decorators import login_required
00006|from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
00007|from django.views.decorators.http import require_GET, require_POST
00008|
00009|from reports.models import ReportConfig
00010|from reports.services import (
00011|    AREA_ADMIN,
00012|    AREA_PGC,
00013|    AREA_PGO,
00014|    AREA_RISK,
00015|    generate_report_package,
00016|)
00017|
00018|
00019|@login_required
00020|@require_GET
00021|def report_defaults(request):
00022|    cfg = ReportConfig.get_active()
00023|    return JsonResponse(
00024|        {
00025|            "ok": True,
00026|            "defaults": {
00027|                AREA_ADMIN: cfg.include_admin_by_default,
00028|                AREA_PGC: cfg.include_pgc_by_default,
00029|                AREA_PGO: cfg.include_pgo_by_default,
00030|                AREA_RISK: cfg.include_risk_by_default,
00031|            },
00032|            "labels": {
00033|                AREA_ADMIN: "Administración",
00034|                AREA_PGC: "PGC",
00035|                AREA_PGO: "PGO",
00036|                AREA_RISK: "B. Riesgo",
00037|            },
00038|        }
00039|    )
00040|
00041|
00042|@login_required
00043|@require_POST
00044|def generate_reports(request):
00045|    """
00046|    Acepta application/json {areas:[...]} o form areas=admin&areas=pgc
00047|    """
00048|    areas: list[str] = []
00049|    content_type = (request.content_type or "").lower()
00050|    if "application/json" in content_type:
00051|        try:
00052|            payload = json.loads(request.body.decode("utf-8") or "{}")
00053|        except json.JSONDecodeError:
00054|            return HttpResponseBadRequest("JSON inválido.")
00055|        raw = payload.get("areas") or []
00056|        if isinstance(raw, str):
00057|            areas = [raw]
00058|        else:
00059|            areas = [str(a) for a in raw]
00060|    else:
00061|        areas = request.POST.getlist("areas")
00062|
00063|    areas = [a.strip().lower() for a in areas if str(a).strip()]
00064|    if not areas:
00065|        return JsonResponse(
00066|            {"ok": False, "error": "Seleccione al menos un área (Administración, PGC, PGO o B. Riesgo)."},
00067|            status=400,
00068|        )
00069|
00070|    try:
00071|        filename, content, ctype = generate_report_package(areas)
00072|    except ValueError as exc:
00073|        return JsonResponse({"ok": False, "error": str(exc)}, status=400)
00074|    except Exception as exc:
00075|        return JsonResponse(
00076|            {"ok": False, "error": f"Error al generar reportes: {exc}"},
00077|            status=500,
00078|        )
00079|
00080|    response = HttpResponse(content, content_type=ctype)
00081|    response["Content-Disposition"] = f'attachment; filename="{filename}"'
00082|    response["X-Report-Filename"] = filename
00083|    return response

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKaW1wb3J0IGpzb24KCmZyb20gZGphbmdvLmNvbnRyaWIuYXV0aC5kZWNvcmF0b3JzIGltcG9ydCBsb2dpbl9yZXF1aXJlZApmcm9tIGRqYW5nby5odHRwIGltcG9ydCBIdHRwUmVzcG9uc2UsIEh0dHBSZXNwb25zZUJhZFJlcXVlc3QsIEpzb25SZXNwb25zZQpmcm9tIGRqYW5nby52aWV3cy5kZWNvcmF0b3JzLmh0dHAgaW1wb3J0IHJlcXVpcmVfR0VULCByZXF1aXJlX1BPU1QKCmZyb20gcmVwb3J0cy5tb2RlbHMgaW1wb3J0IFJlcG9ydENvbmZpZwpmcm9tIHJlcG9ydHMuc2VydmljZXMgaW1wb3J0ICgKICAgIEFSRUFfQURNSU4sCiAgICBBUkVBX1BHQywKICAgIEFSRUFfUEdPLAogICAgQVJFQV9SSVNLLAogICAgZ2VuZXJhdGVfcmVwb3J0X3BhY2thZ2UsCikKCgpAbG9naW5fcmVxdWlyZWQKQHJlcXVpcmVfR0VUCmRlZiByZXBvcnRfZGVmYXVsdHMocmVxdWVzdCk6CiAgICBjZmcgPSBSZXBvcnRDb25maWcuZ2V0X2FjdGl2ZSgpCiAgICByZXR1cm4gSnNvblJlc3BvbnNlKAogICAgICAgIHsKICAgICAgICAgICAgIm9rIjogVHJ1ZSwKICAgICAgICAgICAgImRlZmF1bHRzIjogewogICAgICAgICAgICAgICAgQVJFQV9BRE1JTjogY2ZnLmluY2x1ZGVfYWRtaW5fYnlfZGVmYXVsdCwKICAgICAgICAgICAgICAgIEFSRUFfUEdDOiBjZmcuaW5jbHVkZV9wZ2NfYnlfZGVmYXVsdCwKICAgICAgICAgICAgICAgIEFSRUFfUEdPOiBjZmcuaW5jbHVkZV9wZ29fYnlfZGVmYXVsdCwKICAgICAgICAgICAgICAgIEFSRUFfUklTSzogY2ZnLmluY2x1ZGVfcmlza19ieV9kZWZhdWx0LAogICAgICAgICAgICB9LAogICAgICAgICAgICAibGFiZWxzIjogewogICAgICAgICAgICAgICAgQVJFQV9BRE1JTjogIkFkbWluaXN0cmFjacOzbiIsCiAgICAgICAgICAgICAgICBBUkVBX1BHQzogIlBHQyIsCiAgICAgICAgICAgICAgICBBUkVBX1BHTzogIlBHTyIsCiAgICAgICAgICAgICAgICBBUkVBX1JJU0s6ICJCLiBSaWVzZ28iLAogICAgICAgICAgICB9LAogICAgICAgIH0KICAgICkKCgpAbG9naW5fcmVxdWlyZWQKQHJlcXVpcmVfUE9TVApkZWYgZ2VuZXJhdGVfcmVwb3J0cyhyZXF1ZXN0KToKICAgICIiIgogICAgQWNlcHRhIGFwcGxpY2F0aW9uL2pzb24ge2FyZWFzOlsuLi5dfSBvIGZvcm0gYXJlYXM9YWRtaW4mYXJlYXM9cGdjCiAgICAiIiIKICAgIGFyZWFzOiBsaXN0W3N0cl0gPSBbXQogICAgY29udGVudF90eXBlID0gKHJlcXVlc3QuY29udGVudF90eXBlIG9yICIiKS5sb3dlcigpCiAgICBpZiAiYXBwbGljYXRpb24vanNvbiIgaW4gY29udGVudF90eXBlOgogICAgICAgIHRyeToKICAgICAgICAgICAgcGF5bG9hZCA9IGpzb24ubG9hZHMocmVxdWVzdC5ib2R5LmRlY29kZSgidXRmLTgiKSBvciAie30iKQogICAgICAgIGV4Y2VwdCBqc29uLkpTT05EZWNvZGVFcnJvcjoKICAgICAgICAgICAgcmV0dXJuIEh0dHBSZXNwb25zZUJhZFJlcXVlc3QoIkpTT04gaW52w6FsaWRvLiIpCiAgICAgICAgcmF3ID0gcGF5bG9hZC5nZXQoImFyZWFzIikgb3IgW10KICAgICAgICBpZiBpc2luc3RhbmNlKHJhdywgc3RyKToKICAgICAgICAgICAgYXJlYXMgPSBbcmF3XQogICAgICAgIGVsc2U6CiAgICAgICAgICAgIGFyZWFzID0gW3N0cihhKSBmb3IgYSBpbiByYXddCiAgICBlbHNlOgogICAgICAgIGFyZWFzID0gcmVxdWVzdC5QT1NULmdldGxpc3QoImFyZWFzIikKCiAgICBhcmVhcyA9IFthLnN0cmlwKCkubG93ZXIoKSBmb3IgYSBpbiBhcmVhcyBpZiBzdHIoYSkuc3RyaXAoKV0KICAgIGlmIG5vdCBhcmVhczoKICAgICAgICByZXR1cm4gSnNvblJlc3BvbnNlKAogICAgICAgICAgICB7Im9rIjogRmFsc2UsICJlcnJvciI6ICJTZWxlY2Npb25lIGFsIG1lbm9zIHVuIMOhcmVhIChBZG1pbmlzdHJhY2nDs24sIFBHQywgUEdPIG8gQi4gUmllc2dvKS4ifSwKICAgICAgICAgICAgc3RhdHVzPTQwMCwKICAgICAgICApCgogICAgdHJ5OgogICAgICAgIGZpbGVuYW1lLCBjb250ZW50LCBjdHlwZSA9IGdlbmVyYXRlX3JlcG9ydF9wYWNrYWdlKGFyZWFzKQogICAgZXhjZXB0IFZhbHVlRXJyb3IgYXMgZXhjOgogICAgICAgIHJldHVybiBKc29uUmVzcG9uc2UoeyJvayI6IEZhbHNlLCAiZXJyb3IiOiBzdHIoZXhjKX0sIHN0YXR1cz00MDApCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGV4YzoKICAgICAgICByZXR1cm4gSnNvblJlc3BvbnNlKAogICAgICAgICAgICB7Im9rIjogRmFsc2UsICJlcnJvciI6IGYiRXJyb3IgYWwgZ2VuZXJhciByZXBvcnRlczoge2V4Y30ifSwKICAgICAgICAgICAgc3RhdHVzPTUwMCwKICAgICAgICApCgogICAgcmVzcG9uc2UgPSBIdHRwUmVzcG9uc2UoY29udGVudCwgY29udGVudF90eXBlPWN0eXBlKQogICAgcmVzcG9uc2VbIkNvbnRlbnQtRGlzcG9zaXRpb24iXSA9IGYnYXR0YWNobWVudDsgZmlsZW5hbWU9IntmaWxlbmFtZX0iJwogICAgcmVzcG9uc2VbIlgtUmVwb3J0LUZpbGVuYW1lIl0gPSBmaWxlbmFtZQogICAgcmV0dXJuIHJlc3BvbnNlCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/xlsx_utils.py
PATH_JSON="reports/xlsx_utils.py"
FILENAME=xlsx_utils.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=70
SIZE_BYTES_UTF8=2383
CONTENT_SHA256=18fe576d0ed481b6c9aa15595a56641109d798df8ae80aa62a8b31e7c938415c
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Builders Excel compactos con openpyxl."""

from __future__ import annotations

from io import BytesIO
from typing import Any, Sequence

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter


def build_workbook(
    sheets: Sequence[dict[str, Any]],
    *,
    report_title: str,
    stamp_label: str,
) -> bytes:
    """
    sheets: list of {name, title, headers, rows}
    """
    wb = Workbook()
    # remove default if we create sheets
    default = wb.active
    wb.remove(default)

    if not sheets:
        ws = wb.create_sheet("Sin datos")
        ws["A1"] = report_title
        ws["A1"].font = Font(bold=True, size=14)
        ws["A2"] = stamp_label
        ws["A2"].font = Font(bold=True)
        ws["A4"] = "No hay tablas para exportar."
    else:
        for idx, sheet in enumerate(sheets):
            name = (sheet.get("name") or f"Hoja{idx+1}")[:31]
            ws = wb.create_sheet(name)
            title = sheet.get("title") or name
            headers = list(sheet.get("headers") or [])
            rows = list(sheet.get("rows") or [])

            ws["A1"] = report_title
            ws["A1"].font = Font(bold=True, size=14)
            ws["A2"] = stamp_label
            ws["A2"].font = Font(bold=True)
            ws["A4"] = title
            ws["A4"].font = Font(bold=True, size=12)

            start_row = 6
            for col, header in enumerate(headers, start=1):
                cell = ws.cell(row=start_row, column=col, value=header)
                cell.font = Font(bold=True)
            for r_i, row in enumerate(rows, start=start_row + 1):
                for c_i, value in enumerate(row, start=1):
                    ws.cell(row=r_i, column=c_i, value=value)

            for col in range(1, max(len(headers), 1) + 1):
                letter = get_column_letter(col)
                maxlen = len(str(headers[col - 1])) if headers and col <= len(headers) else 10
                for row in rows:
                    if col - 1 < len(row) and col <= 40:
                        maxlen = max(
                            maxlen,
                            min(len(str(row[col - 1] if row[col - 1] is not None else "")), 60),
                        )
                ws.column_dimensions[letter].width = min(maxlen + 2, 42)

    bio = BytesIO()
    wb.save(bio)
    return bio.getvalue()

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Builders Excel compactos con openpyxl."""
00002|
00003|from __future__ import annotations
00004|
00005|from io import BytesIO
00006|from typing import Any, Sequence
00007|
00008|from openpyxl import Workbook
00009|from openpyxl.styles import Font
00010|from openpyxl.utils import get_column_letter
00011|
00012|
00013|def build_workbook(
00014|    sheets: Sequence[dict[str, Any]],
00015|    *,
00016|    report_title: str,
00017|    stamp_label: str,
00018|) -> bytes:
00019|    """
00020|    sheets: list of {name, title, headers, rows}
00021|    """
00022|    wb = Workbook()
00023|    # remove default if we create sheets
00024|    default = wb.active
00025|    wb.remove(default)
00026|
00027|    if not sheets:
00028|        ws = wb.create_sheet("Sin datos")
00029|        ws["A1"] = report_title
00030|        ws["A1"].font = Font(bold=True, size=14)
00031|        ws["A2"] = stamp_label
00032|        ws["A2"].font = Font(bold=True)
00033|        ws["A4"] = "No hay tablas para exportar."
00034|    else:
00035|        for idx, sheet in enumerate(sheets):
00036|            name = (sheet.get("name") or f"Hoja{idx+1}")[:31]
00037|            ws = wb.create_sheet(name)
00038|            title = sheet.get("title") or name
00039|            headers = list(sheet.get("headers") or [])
00040|            rows = list(sheet.get("rows") or [])
00041|
00042|            ws["A1"] = report_title
00043|            ws["A1"].font = Font(bold=True, size=14)
00044|            ws["A2"] = stamp_label
00045|            ws["A2"].font = Font(bold=True)
00046|            ws["A4"] = title
00047|            ws["A4"].font = Font(bold=True, size=12)
00048|
00049|            start_row = 6
00050|            for col, header in enumerate(headers, start=1):
00051|                cell = ws.cell(row=start_row, column=col, value=header)
00052|                cell.font = Font(bold=True)
00053|            for r_i, row in enumerate(rows, start=start_row + 1):
00054|                for c_i, value in enumerate(row, start=1):
00055|                    ws.cell(row=r_i, column=c_i, value=value)
00056|
00057|            for col in range(1, max(len(headers), 1) + 1):
00058|                letter = get_column_letter(col)
00059|                maxlen = len(str(headers[col - 1])) if headers and col <= len(headers) else 10
00060|                for row in rows:
00061|                    if col - 1 < len(row) and col <= 40:
00062|                        maxlen = max(
00063|                            maxlen,
00064|                            min(len(str(row[col - 1] if row[col - 1] is not None else "")), 60),
00065|                        )
00066|                ws.column_dimensions[letter].width = min(maxlen + 2, 42)
00067|
00068|    bio = BytesIO()
00069|    wb.save(bio)
00070|    return bio.getvalue()

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiQnVpbGRlcnMgRXhjZWwgY29tcGFjdG9zIGNvbiBvcGVucHl4bC4iIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmZyb20gaW8gaW1wb3J0IEJ5dGVzSU8KZnJvbSB0eXBpbmcgaW1wb3J0IEFueSwgU2VxdWVuY2UKCmZyb20gb3BlbnB5eGwgaW1wb3J0IFdvcmtib29rCmZyb20gb3BlbnB5eGwuc3R5bGVzIGltcG9ydCBGb250CmZyb20gb3BlbnB5eGwudXRpbHMgaW1wb3J0IGdldF9jb2x1bW5fbGV0dGVyCgoKZGVmIGJ1aWxkX3dvcmtib29rKAogICAgc2hlZXRzOiBTZXF1ZW5jZVtkaWN0W3N0ciwgQW55XV0sCiAgICAqLAogICAgcmVwb3J0X3RpdGxlOiBzdHIsCiAgICBzdGFtcF9sYWJlbDogc3RyLAopIC0+IGJ5dGVzOgogICAgIiIiCiAgICBzaGVldHM6IGxpc3Qgb2Yge25hbWUsIHRpdGxlLCBoZWFkZXJzLCByb3dzfQogICAgIiIiCiAgICB3YiA9IFdvcmtib29rKCkKICAgICMgcmVtb3ZlIGRlZmF1bHQgaWYgd2UgY3JlYXRlIHNoZWV0cwogICAgZGVmYXVsdCA9IHdiLmFjdGl2ZQogICAgd2IucmVtb3ZlKGRlZmF1bHQpCgogICAgaWYgbm90IHNoZWV0czoKICAgICAgICB3cyA9IHdiLmNyZWF0ZV9zaGVldCgiU2luIGRhdG9zIikKICAgICAgICB3c1siQTEiXSA9IHJlcG9ydF90aXRsZQogICAgICAgIHdzWyJBMSJdLmZvbnQgPSBGb250KGJvbGQ9VHJ1ZSwgc2l6ZT0xNCkKICAgICAgICB3c1siQTIiXSA9IHN0YW1wX2xhYmVsCiAgICAgICAgd3NbIkEyIl0uZm9udCA9IEZvbnQoYm9sZD1UcnVlKQogICAgICAgIHdzWyJBNCJdID0gIk5vIGhheSB0YWJsYXMgcGFyYSBleHBvcnRhci4iCiAgICBlbHNlOgogICAgICAgIGZvciBpZHgsIHNoZWV0IGluIGVudW1lcmF0ZShzaGVldHMpOgogICAgICAgICAgICBuYW1lID0gKHNoZWV0LmdldCgibmFtZSIpIG9yIGYiSG9qYXtpZHgrMX0iKVs6MzFdCiAgICAgICAgICAgIHdzID0gd2IuY3JlYXRlX3NoZWV0KG5hbWUpCiAgICAgICAgICAgIHRpdGxlID0gc2hlZXQuZ2V0KCJ0aXRsZSIpIG9yIG5hbWUKICAgICAgICAgICAgaGVhZGVycyA9IGxpc3Qoc2hlZXQuZ2V0KCJoZWFkZXJzIikgb3IgW10pCiAgICAgICAgICAgIHJvd3MgPSBsaXN0KHNoZWV0LmdldCgicm93cyIpIG9yIFtdKQoKICAgICAgICAgICAgd3NbIkExIl0gPSByZXBvcnRfdGl0bGUKICAgICAgICAgICAgd3NbIkExIl0uZm9udCA9IEZvbnQoYm9sZD1UcnVlLCBzaXplPTE0KQogICAgICAgICAgICB3c1siQTIiXSA9IHN0YW1wX2xhYmVsCiAgICAgICAgICAgIHdzWyJBMiJdLmZvbnQgPSBGb250KGJvbGQ9VHJ1ZSkKICAgICAgICAgICAgd3NbIkE0Il0gPSB0aXRsZQogICAgICAgICAgICB3c1siQTQiXS5mb250ID0gRm9udChib2xkPVRydWUsIHNpemU9MTIpCgogICAgICAgICAgICBzdGFydF9yb3cgPSA2CiAgICAgICAgICAgIGZvciBjb2wsIGhlYWRlciBpbiBlbnVtZXJhdGUoaGVhZGVycywgc3RhcnQ9MSk6CiAgICAgICAgICAgICAgICBjZWxsID0gd3MuY2VsbChyb3c9c3RhcnRfcm93LCBjb2x1bW49Y29sLCB2YWx1ZT1oZWFkZXIpCiAgICAgICAgICAgICAgICBjZWxsLmZvbnQgPSBGb250KGJvbGQ9VHJ1ZSkKICAgICAgICAgICAgZm9yIHJfaSwgcm93IGluIGVudW1lcmF0ZShyb3dzLCBzdGFydD1zdGFydF9yb3cgKyAxKToKICAgICAgICAgICAgICAgIGZvciBjX2ksIHZhbHVlIGluIGVudW1lcmF0ZShyb3csIHN0YXJ0PTEpOgogICAgICAgICAgICAgICAgICAgIHdzLmNlbGwocm93PXJfaSwgY29sdW1uPWNfaSwgdmFsdWU9dmFsdWUpCgogICAgICAgICAgICBmb3IgY29sIGluIHJhbmdlKDEsIG1heChsZW4oaGVhZGVycyksIDEpICsgMSk6CiAgICAgICAgICAgICAgICBsZXR0ZXIgPSBnZXRfY29sdW1uX2xldHRlcihjb2wpCiAgICAgICAgICAgICAgICBtYXhsZW4gPSBsZW4oc3RyKGhlYWRlcnNbY29sIC0gMV0pKSBpZiBoZWFkZXJzIGFuZCBjb2wgPD0gbGVuKGhlYWRlcnMpIGVsc2UgMTAKICAgICAgICAgICAgICAgIGZvciByb3cgaW4gcm93czoKICAgICAgICAgICAgICAgICAgICBpZiBjb2wgLSAxIDwgbGVuKHJvdykgYW5kIGNvbCA8PSA0MDoKICAgICAgICAgICAgICAgICAgICAgICAgbWF4bGVuID0gbWF4KAogICAgICAgICAgICAgICAgICAgICAgICAgICAgbWF4bGVuLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgbWluKGxlbihzdHIocm93W2NvbCAtIDFdIGlmIHJvd1tjb2wgLSAxXSBpcyBub3QgTm9uZSBlbHNlICIiKSksIDYwKSwKICAgICAgICAgICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgd3MuY29sdW1uX2RpbWVuc2lvbnNbbGV0dGVyXS53aWR0aCA9IG1pbihtYXhsZW4gKyAyLCA0MikKCiAgICBiaW8gPSBCeXRlc0lPKCkKICAgIHdiLnNhdmUoYmlvKQogICAgcmV0dXJuIGJpby5nZXR2YWx1ZSgpCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=risk/__init__.py
PATH_JSON="risk/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=risk/admin.py
PATH_JSON="risk/admin.py"
FILENAME=admin.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=58
SIZE_BYTES_UTF8=1872
CONTENT_SHA256=9ca696b157d286d7db43b859cac6629ba5ff2714971bf0d99973195c1cc6fc37
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.contrib import admin

from .models import (
    ContactoCobranza,
    EstadoFinanciero,
    PagoRealizado,
    ProgramacionPago,
    RiskOperationSnapshot,
)


@admin.register(EstadoFinanciero)
class EstadoFinancieroAdmin(admin.ModelAdmin):
    list_display = ("entidad", "periodo", "saldo_total", "mora_dias", "exposicion")
    list_filter = ("periodo",)
    search_fields = ("entidad__codigo", "entidad__nombre")
    ordering = ("-periodo",)


@admin.register(ProgramacionPago)
class ProgramacionPagoAdmin(admin.ModelAdmin):
    list_display = ("entidad", "referencia", "fecha_programada", "monto", "moneda", "producto")
    list_filter = ("fecha_programada", "moneda")
    search_fields = ("referencia", "entidad__codigo", "entidad__nombre")
    ordering = ("fecha_programada",)


@admin.register(PagoRealizado)
class PagoRealizadoAdmin(admin.ModelAdmin):
    list_display = ("entidad", "referencia", "fecha_pago", "monto", "moneda")
    list_filter = ("fecha_pago", "moneda")
    search_fields = ("referencia", "entidad__codigo", "entidad__nombre")
    ordering = ("-fecha_pago",)


@admin.register(ContactoCobranza)
class ContactoCobranzaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "entidad", "telefono", "email", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre", "entidad__codigo", "entidad__nombre")
    ordering = ("entidad__nombre",)


@admin.register(RiskOperationSnapshot)
class RiskOperationSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_snapshot",
        "entidad",
        "referencia_operacion",
        "nivel_riesgo",
        "dias_mora",
        "saldo",
        "monto_exigible",
        "alerta",
    )
    list_filter = ("nivel_riesgo", "alerta", "fecha_snapshot")
    search_fields = ("referencia_operacion", "entidad__codigo", "entidad__nombre")
    ordering = ("-fecha_snapshot",)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib import admin
00002|
00003|from .models import (
00004|    ContactoCobranza,
00005|    EstadoFinanciero,
00006|    PagoRealizado,
00007|    ProgramacionPago,
00008|    RiskOperationSnapshot,
00009|)
00010|
00011|
00012|@admin.register(EstadoFinanciero)
00013|class EstadoFinancieroAdmin(admin.ModelAdmin):
00014|    list_display = ("entidad", "periodo", "saldo_total", "mora_dias", "exposicion")
00015|    list_filter = ("periodo",)
00016|    search_fields = ("entidad__codigo", "entidad__nombre")
00017|    ordering = ("-periodo",)
00018|
00019|
00020|@admin.register(ProgramacionPago)
00021|class ProgramacionPagoAdmin(admin.ModelAdmin):
00022|    list_display = ("entidad", "referencia", "fecha_programada", "monto", "moneda", "producto")
00023|    list_filter = ("fecha_programada", "moneda")
00024|    search_fields = ("referencia", "entidad__codigo", "entidad__nombre")
00025|    ordering = ("fecha_programada",)
00026|
00027|
00028|@admin.register(PagoRealizado)
00029|class PagoRealizadoAdmin(admin.ModelAdmin):
00030|    list_display = ("entidad", "referencia", "fecha_pago", "monto", "moneda")
00031|    list_filter = ("fecha_pago", "moneda")
00032|    search_fields = ("referencia", "entidad__codigo", "entidad__nombre")
00033|    ordering = ("-fecha_pago",)
00034|
00035|
00036|@admin.register(ContactoCobranza)
00037|class ContactoCobranzaAdmin(admin.ModelAdmin):
00038|    list_display = ("nombre", "entidad", "telefono", "email", "activo")
00039|    list_filter = ("activo",)
00040|    search_fields = ("nombre", "entidad__codigo", "entidad__nombre")
00041|    ordering = ("entidad__nombre",)
00042|
00043|
00044|@admin.register(RiskOperationSnapshot)
00045|class RiskOperationSnapshotAdmin(admin.ModelAdmin):
00046|    list_display = (
00047|        "fecha_snapshot",
00048|        "entidad",
00049|        "referencia_operacion",
00050|        "nivel_riesgo",
00051|        "dias_mora",
00052|        "saldo",
00053|        "monto_exigible",
00054|        "alerta",
00055|    )
00056|    list_filter = ("nivel_riesgo", "alerta", "fecha_snapshot")
00057|    search_fields = ("referencia_operacion", "entidad__codigo", "entidad__nombre")
00058|    ordering = ("-fecha_snapshot",)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgYWRtaW4KCmZyb20gLm1vZGVscyBpbXBvcnQgKAogICAgQ29udGFjdG9Db2JyYW56YSwKICAgIEVzdGFkb0ZpbmFuY2llcm8sCiAgICBQYWdvUmVhbGl6YWRvLAogICAgUHJvZ3JhbWFjaW9uUGFnbywKICAgIFJpc2tPcGVyYXRpb25TbmFwc2hvdCwKKQoKCkBhZG1pbi5yZWdpc3RlcihFc3RhZG9GaW5hbmNpZXJvKQpjbGFzcyBFc3RhZG9GaW5hbmNpZXJvQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoImVudGlkYWQiLCAicGVyaW9kbyIsICJzYWxkb190b3RhbCIsICJtb3JhX2RpYXMiLCAiZXhwb3NpY2lvbiIpCiAgICBsaXN0X2ZpbHRlciA9ICgicGVyaW9kbyIsKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgiZW50aWRhZF9fY29kaWdvIiwgImVudGlkYWRfX25vbWJyZSIpCiAgICBvcmRlcmluZyA9ICgiLXBlcmlvZG8iLCkKCgpAYWRtaW4ucmVnaXN0ZXIoUHJvZ3JhbWFjaW9uUGFnbykKY2xhc3MgUHJvZ3JhbWFjaW9uUGFnb0FkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKCJlbnRpZGFkIiwgInJlZmVyZW5jaWEiLCAiZmVjaGFfcHJvZ3JhbWFkYSIsICJtb250byIsICJtb25lZGEiLCAicHJvZHVjdG8iKQogICAgbGlzdF9maWx0ZXIgPSAoImZlY2hhX3Byb2dyYW1hZGEiLCAibW9uZWRhIikKICAgIHNlYXJjaF9maWVsZHMgPSAoInJlZmVyZW5jaWEiLCAiZW50aWRhZF9fY29kaWdvIiwgImVudGlkYWRfX25vbWJyZSIpCiAgICBvcmRlcmluZyA9ICgiZmVjaGFfcHJvZ3JhbWFkYSIsKQoKCkBhZG1pbi5yZWdpc3RlcihQYWdvUmVhbGl6YWRvKQpjbGFzcyBQYWdvUmVhbGl6YWRvQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoImVudGlkYWQiLCAicmVmZXJlbmNpYSIsICJmZWNoYV9wYWdvIiwgIm1vbnRvIiwgIm1vbmVkYSIpCiAgICBsaXN0X2ZpbHRlciA9ICgiZmVjaGFfcGFnbyIsICJtb25lZGEiKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgicmVmZXJlbmNpYSIsICJlbnRpZGFkX19jb2RpZ28iLCAiZW50aWRhZF9fbm9tYnJlIikKICAgIG9yZGVyaW5nID0gKCItZmVjaGFfcGFnbyIsKQoKCkBhZG1pbi5yZWdpc3RlcihDb250YWN0b0NvYnJhbnphKQpjbGFzcyBDb250YWN0b0NvYnJhbnphQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoIm5vbWJyZSIsICJlbnRpZGFkIiwgInRlbGVmb25vIiwgImVtYWlsIiwgImFjdGl2byIpCiAgICBsaXN0X2ZpbHRlciA9ICgiYWN0aXZvIiwpCiAgICBzZWFyY2hfZmllbGRzID0gKCJub21icmUiLCAiZW50aWRhZF9fY29kaWdvIiwgImVudGlkYWRfX25vbWJyZSIpCiAgICBvcmRlcmluZyA9ICgiZW50aWRhZF9fbm9tYnJlIiwpCgoKQGFkbWluLnJlZ2lzdGVyKFJpc2tPcGVyYXRpb25TbmFwc2hvdCkKY2xhc3MgUmlza09wZXJhdGlvblNuYXBzaG90QWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoCiAgICAgICAgImZlY2hhX3NuYXBzaG90IiwKICAgICAgICAiZW50aWRhZCIsCiAgICAgICAgInJlZmVyZW5jaWFfb3BlcmFjaW9uIiwKICAgICAgICAibml2ZWxfcmllc2dvIiwKICAgICAgICAiZGlhc19tb3JhIiwKICAgICAgICAic2FsZG8iLAogICAgICAgICJtb250b19leGlnaWJsZSIsCiAgICAgICAgImFsZXJ0YSIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgibml2ZWxfcmllc2dvIiwgImFsZXJ0YSIsICJmZWNoYV9zbmFwc2hvdCIpCiAgICBzZWFyY2hfZmllbGRzID0gKCJyZWZlcmVuY2lhX29wZXJhY2lvbiIsICJlbnRpZGFkX19jb2RpZ28iLCAiZW50aWRhZF9fbm9tYnJlIikKICAgIG9yZGVyaW5nID0gKCItZmVjaGFfc25hcHNob3QiLCkK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=risk/apps.py
PATH_JSON="risk/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=6
SIZE_BYTES_UTF8=140
CONTENT_SHA256=f81f96d52cf6a78dcde874f63f951ad87f105e642529cf31906c9c22d6673450
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.apps import AppConfig


class RiskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'risk'

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class RiskConfig(AppConfig):
00005|    default_auto_field = 'django.db.models.BigAutoField'
00006|    name = 'risk'

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgUmlza0NvbmZpZyhBcHBDb25maWcpOgogICAgZGVmYXVsdF9hdXRvX2ZpZWxkID0gJ2RqYW5nby5kYi5tb2RlbHMuQmlnQXV0b0ZpZWxkJwogICAgbmFtZSA9ICdyaXNrJwo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=risk/forms.py
PATH_JSON="risk/forms.py"
FILENAME=forms.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=16
SIZE_BYTES_UTF8=578
CONTENT_SHA256=8fdee2743b17eac79e8221f402aea9564bdade3db69e441dc8bf5f099ab5244f
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django import forms


class ImportFileForm(forms.Form):
    archivo = forms.FileField(label="Archivo CSV o XLSX")
    tipo = forms.ChoiceField(
        choices=[
            ("leasing_database", "Base de datos Leasing (CSV/XLSX)"),
            ("leasing_rentas", "Rentas / cuotas leasing"),
            ("estados_financieros", "Estados financieros"),
            ("programacion_pagos", "Programación de pagos"),
            ("pagos_realizados", "Pagos realizados"),
            ("snapshots", "Snapshots operativos"),
        ],
        label="Tipo de importación",
    )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django import forms
00002|
00003|
00004|class ImportFileForm(forms.Form):
00005|    archivo = forms.FileField(label="Archivo CSV o XLSX")
00006|    tipo = forms.ChoiceField(
00007|        choices=[
00008|            ("leasing_database", "Base de datos Leasing (CSV/XLSX)"),
00009|            ("leasing_rentas", "Rentas / cuotas leasing"),
00010|            ("estados_financieros", "Estados financieros"),
00011|            ("programacion_pagos", "Programación de pagos"),
00012|            ("pagos_realizados", "Pagos realizados"),
00013|            ("snapshots", "Snapshots operativos"),
00014|        ],
00015|        label="Tipo de importación",
00016|    )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28gaW1wb3J0IGZvcm1zCgoKY2xhc3MgSW1wb3J0RmlsZUZvcm0oZm9ybXMuRm9ybSk6CiAgICBhcmNoaXZvID0gZm9ybXMuRmlsZUZpZWxkKGxhYmVsPSJBcmNoaXZvIENTViBvIFhMU1giKQogICAgdGlwbyA9IGZvcm1zLkNob2ljZUZpZWxkKAogICAgICAgIGNob2ljZXM9WwogICAgICAgICAgICAoImxlYXNpbmdfZGF0YWJhc2UiLCAiQmFzZSBkZSBkYXRvcyBMZWFzaW5nIChDU1YvWExTWCkiKSwKICAgICAgICAgICAgKCJsZWFzaW5nX3JlbnRhcyIsICJSZW50YXMgLyBjdW90YXMgbGVhc2luZyIpLAogICAgICAgICAgICAoImVzdGFkb3NfZmluYW5jaWVyb3MiLCAiRXN0YWRvcyBmaW5hbmNpZXJvcyIpLAogICAgICAgICAgICAoInByb2dyYW1hY2lvbl9wYWdvcyIsICJQcm9ncmFtYWNpw7NuIGRlIHBhZ29zIiksCiAgICAgICAgICAgICgicGFnb3NfcmVhbGl6YWRvcyIsICJQYWdvcyByZWFsaXphZG9zIiksCiAgICAgICAgICAgICgic25hcHNob3RzIiwgIlNuYXBzaG90cyBvcGVyYXRpdm9zIiksCiAgICAgICAgXSwKICAgICAgICBsYWJlbD0iVGlwbyBkZSBpbXBvcnRhY2nDs24iLAogICAgKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=risk/models.py
PATH_JSON="risk/models.py"
FILENAME=models.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=127
SIZE_BYTES_UTF8=4627
CONTENT_SHA256=e8d8b4bf819af00944b5c12074d7667cbf06909825f407d74abedc7553599a97
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.db import models

from core.models import TimeStampedModel
from core.wcg_models import Entidad, Producto


class EstadoFinanciero(TimeStampedModel):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="estados_financieros")
    periodo = models.CharField(max_length=7, help_text="YYYY-MM")
    saldo_total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    mora_dias = models.PositiveIntegerField(default=0)
    exposicion = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    notas = models.TextField(blank=True)

    class Meta:
        unique_together = ("entidad", "periodo")
        ordering = ["-periodo", "entidad__nombre"]
        verbose_name = "Estado financiero"
        verbose_name_plural = "Estados financieros"

    def __str__(self):
        return f"{self.entidad.codigo} {self.periodo}"


class ProgramacionPago(TimeStampedModel):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="programaciones_pago")
    referencia = models.CharField(max_length=80)
    fecha_programada = models.DateField()
    monto = models.DecimalField(max_digits=16, decimal_places=2)
    moneda = models.CharField(max_length=3, default="GTQ")
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="programaciones_pago",
    )

    class Meta:
        unique_together = ("entidad", "referencia")
        ordering = ["fecha_programada"]
        verbose_name = "Programación de pago"
        verbose_name_plural = "Programaciones de pago"

    def __str__(self):
        return f"{self.entidad.codigo} — {self.referencia}"


class PagoRealizado(TimeStampedModel):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="pagos_realizados")
    referencia = models.CharField(max_length=80)
    fecha_pago = models.DateField()
    monto = models.DecimalField(max_digits=16, decimal_places=2)
    moneda = models.CharField(max_length=3, default="GTQ")

    class Meta:
        unique_together = ("entidad", "referencia")
        ordering = ["-fecha_pago"]
        verbose_name = "Pago realizado"
        verbose_name_plural = "Pagos realizados"

    def __str__(self):
        return f"{self.entidad.codigo} — {self.referencia}"


class ContactoCobranza(TimeStampedModel):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="contactos_cobranza")
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["entidad__nombre", "nombre"]
        verbose_name = "Contacto de cobranza"
        verbose_name_plural = "Contactos de cobranza"

    def __str__(self):
        return f"{self.nombre} ({self.entidad.codigo})"


class RiskOperationSnapshot(TimeStampedModel):
    """
    Snapshot operativo de riesgo (Balón).
    Clave natural: (`entidad`, `referencia_operacion`, `fecha_snapshot`).
    """
    NIVEL_BAJO = "BAJO"
    NIVEL_MEDIO = "MEDIO"
    NIVEL_ALTO = "ALTO"
    NIVEL_CRITICO = "CRITICO"
    NIVEL_CHOICES = [
        (NIVEL_BAJO, "Bajo"),
        (NIVEL_MEDIO, "Medio"),
        (NIVEL_ALTO, "Alto"),
        (NIVEL_CRITICO, "Crítico"),
    ]

    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="risk_snapshots")
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="risk_snapshots",
    )
    referencia_operacion = models.CharField(max_length=80, db_index=True)
    fecha_snapshot = models.DateField()
    nivel_riesgo = models.CharField(max_length=20, choices=NIVEL_CHOICES, default=NIVEL_MEDIO)
    dias_mora = models.PositiveIntegerField(default=0)
    saldo = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    monto_exigible = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        help_text="Monto vencido/exigible al momento del snapshot.",
    )
    alerta = models.BooleanField(default=False)
    detalle = models.TextField(blank=True)

    class Meta:
        unique_together = ("entidad", "referencia_operacion", "fecha_snapshot")
        ordering = ["-fecha_snapshot", "entidad__nombre"]
        verbose_name = "Snapshot operativo de riesgo"
        verbose_name_plural = "Snapshots operativos de riesgo"

    def __str__(self):
        return f"{self.referencia_operacion} — {self.fecha_snapshot}"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.db import models
00002|
00003|from core.models import TimeStampedModel
00004|from core.wcg_models import Entidad, Producto
00005|
00006|
00007|class EstadoFinanciero(TimeStampedModel):
00008|    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="estados_financieros")
00009|    periodo = models.CharField(max_length=7, help_text="YYYY-MM")
00010|    saldo_total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
00011|    mora_dias = models.PositiveIntegerField(default=0)
00012|    exposicion = models.DecimalField(max_digits=16, decimal_places=2, default=0)
00013|    notas = models.TextField(blank=True)
00014|
00015|    class Meta:
00016|        unique_together = ("entidad", "periodo")
00017|        ordering = ["-periodo", "entidad__nombre"]
00018|        verbose_name = "Estado financiero"
00019|        verbose_name_plural = "Estados financieros"
00020|
00021|    def __str__(self):
00022|        return f"{self.entidad.codigo} {self.periodo}"
00023|
00024|
00025|class ProgramacionPago(TimeStampedModel):
00026|    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="programaciones_pago")
00027|    referencia = models.CharField(max_length=80)
00028|    fecha_programada = models.DateField()
00029|    monto = models.DecimalField(max_digits=16, decimal_places=2)
00030|    moneda = models.CharField(max_length=3, default="GTQ")
00031|    producto = models.ForeignKey(
00032|        Producto,
00033|        on_delete=models.SET_NULL,
00034|        null=True,
00035|        blank=True,
00036|        related_name="programaciones_pago",
00037|    )
00038|
00039|    class Meta:
00040|        unique_together = ("entidad", "referencia")
00041|        ordering = ["fecha_programada"]
00042|        verbose_name = "Programación de pago"
00043|        verbose_name_plural = "Programaciones de pago"
00044|
00045|    def __str__(self):
00046|        return f"{self.entidad.codigo} — {self.referencia}"
00047|
00048|
00049|class PagoRealizado(TimeStampedModel):
00050|    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="pagos_realizados")
00051|    referencia = models.CharField(max_length=80)
00052|    fecha_pago = models.DateField()
00053|    monto = models.DecimalField(max_digits=16, decimal_places=2)
00054|    moneda = models.CharField(max_length=3, default="GTQ")
00055|
00056|    class Meta:
00057|        unique_together = ("entidad", "referencia")
00058|        ordering = ["-fecha_pago"]
00059|        verbose_name = "Pago realizado"
00060|        verbose_name_plural = "Pagos realizados"
00061|
00062|    def __str__(self):
00063|        return f"{self.entidad.codigo} — {self.referencia}"
00064|
00065|
00066|class ContactoCobranza(TimeStampedModel):
00067|    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="contactos_cobranza")
00068|    nombre = models.CharField(max_length=120)
00069|    telefono = models.CharField(max_length=40, blank=True)
00070|    email = models.EmailField(blank=True)
00071|    activo = models.BooleanField(default=True)
00072|
00073|    class Meta:
00074|        ordering = ["entidad__nombre", "nombre"]
00075|        verbose_name = "Contacto de cobranza"
00076|        verbose_name_plural = "Contactos de cobranza"
00077|
00078|    def __str__(self):
00079|        return f"{self.nombre} ({self.entidad.codigo})"
00080|
00081|
00082|class RiskOperationSnapshot(TimeStampedModel):
00083|    """
00084|    Snapshot operativo de riesgo (Balón).
00085|    Clave natural: (`entidad`, `referencia_operacion`, `fecha_snapshot`).
00086|    """
00087|    NIVEL_BAJO = "BAJO"
00088|    NIVEL_MEDIO = "MEDIO"
00089|    NIVEL_ALTO = "ALTO"
00090|    NIVEL_CRITICO = "CRITICO"
00091|    NIVEL_CHOICES = [
00092|        (NIVEL_BAJO, "Bajo"),
00093|        (NIVEL_MEDIO, "Medio"),
00094|        (NIVEL_ALTO, "Alto"),
00095|        (NIVEL_CRITICO, "Crítico"),
00096|    ]
00097|
00098|    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="risk_snapshots")
00099|    producto = models.ForeignKey(
00100|        Producto,
00101|        on_delete=models.SET_NULL,
00102|        null=True,
00103|        blank=True,
00104|        related_name="risk_snapshots",
00105|    )
00106|    referencia_operacion = models.CharField(max_length=80, db_index=True)
00107|    fecha_snapshot = models.DateField()
00108|    nivel_riesgo = models.CharField(max_length=20, choices=NIVEL_CHOICES, default=NIVEL_MEDIO)
00109|    dias_mora = models.PositiveIntegerField(default=0)
00110|    saldo = models.DecimalField(max_digits=16, decimal_places=2, default=0)
00111|    monto_exigible = models.DecimalField(
00112|        max_digits=16,
00113|        decimal_places=2,
00114|        default=0,
00115|        help_text="Monto vencido/exigible al momento del snapshot.",
00116|    )
00117|    alerta = models.BooleanField(default=False)
00118|    detalle = models.TextField(blank=True)
00119|
00120|    class Meta:
00121|        unique_together = ("entidad", "referencia_operacion", "fecha_snapshot")
00122|        ordering = ["-fecha_snapshot", "entidad__nombre"]
00123|        verbose_name = "Snapshot operativo de riesgo"
00124|        verbose_name_plural = "Snapshots operativos de riesgo"
00125|
00126|    def __str__(self):
00127|        return f"{self.referencia_operacion} — {self.fecha_snapshot}"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uZGIgaW1wb3J0IG1vZGVscwoKZnJvbSBjb3JlLm1vZGVscyBpbXBvcnQgVGltZVN0YW1wZWRNb2RlbApmcm9tIGNvcmUud2NnX21vZGVscyBpbXBvcnQgRW50aWRhZCwgUHJvZHVjdG8KCgpjbGFzcyBFc3RhZG9GaW5hbmNpZXJvKFRpbWVTdGFtcGVkTW9kZWwpOgogICAgZW50aWRhZCA9IG1vZGVscy5Gb3JlaWduS2V5KEVudGlkYWQsIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSwgcmVsYXRlZF9uYW1lPSJlc3RhZG9zX2ZpbmFuY2llcm9zIikKICAgIHBlcmlvZG8gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9NywgaGVscF90ZXh0PSJZWVlZLU1NIikKICAgIHNhbGRvX3RvdGFsID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTE2LCBkZWNpbWFsX3BsYWNlcz0yLCBkZWZhdWx0PTApCiAgICBtb3JhX2RpYXMgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoZGVmYXVsdD0wKQogICAgZXhwb3NpY2lvbiA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xNiwgZGVjaW1hbF9wbGFjZXM9MiwgZGVmYXVsdD0wKQogICAgbm90YXMgPSBtb2RlbHMuVGV4dEZpZWxkKGJsYW5rPVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICB1bmlxdWVfdG9nZXRoZXIgPSAoImVudGlkYWQiLCAicGVyaW9kbyIpCiAgICAgICAgb3JkZXJpbmcgPSBbIi1wZXJpb2RvIiwgImVudGlkYWRfX25vbWJyZSJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIkVzdGFkbyBmaW5hbmNpZXJvIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiRXN0YWRvcyBmaW5hbmNpZXJvcyIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi5lbnRpZGFkLmNvZGlnb30ge3NlbGYucGVyaW9kb30iCgoKY2xhc3MgUHJvZ3JhbWFjaW9uUGFnbyhUaW1lU3RhbXBlZE1vZGVsKToKICAgIGVudGlkYWQgPSBtb2RlbHMuRm9yZWlnbktleShFbnRpZGFkLCBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsIHJlbGF0ZWRfbmFtZT0icHJvZ3JhbWFjaW9uZXNfcGFnbyIpCiAgICByZWZlcmVuY2lhID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTgwKQogICAgZmVjaGFfcHJvZ3JhbWFkYSA9IG1vZGVscy5EYXRlRmllbGQoKQogICAgbW9udG8gPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTYsIGRlY2ltYWxfcGxhY2VzPTIpCiAgICBtb25lZGEgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MywgZGVmYXVsdD0iR1RRIikKICAgIHByb2R1Y3RvID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgUHJvZHVjdG8sCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5TRVRfTlVMTCwKICAgICAgICBudWxsPVRydWUsCiAgICAgICAgYmxhbms9VHJ1ZSwKICAgICAgICByZWxhdGVkX25hbWU9InByb2dyYW1hY2lvbmVzX3BhZ28iLAogICAgKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgdW5pcXVlX3RvZ2V0aGVyID0gKCJlbnRpZGFkIiwgInJlZmVyZW5jaWEiKQogICAgICAgIG9yZGVyaW5nID0gWyJmZWNoYV9wcm9ncmFtYWRhIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiUHJvZ3JhbWFjacOzbiBkZSBwYWdvIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiUHJvZ3JhbWFjaW9uZXMgZGUgcGFnbyIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi5lbnRpZGFkLmNvZGlnb30g4oCUIHtzZWxmLnJlZmVyZW5jaWF9IgoKCmNsYXNzIFBhZ29SZWFsaXphZG8oVGltZVN0YW1wZWRNb2RlbCk6CiAgICBlbnRpZGFkID0gbW9kZWxzLkZvcmVpZ25LZXkoRW50aWRhZCwgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLCByZWxhdGVkX25hbWU9InBhZ29zX3JlYWxpemFkb3MiKQogICAgcmVmZXJlbmNpYSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD04MCkKICAgIGZlY2hhX3BhZ28gPSBtb2RlbHMuRGF0ZUZpZWxkKCkKICAgIG1vbnRvID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTE2LCBkZWNpbWFsX3BsYWNlcz0yKQogICAgbW9uZWRhID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTMsIGRlZmF1bHQ9IkdUUSIpCgogICAgY2xhc3MgTWV0YToKICAgICAgICB1bmlxdWVfdG9nZXRoZXIgPSAoImVudGlkYWQiLCAicmVmZXJlbmNpYSIpCiAgICAgICAgb3JkZXJpbmcgPSBbIi1mZWNoYV9wYWdvIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiUGFnbyByZWFsaXphZG8iCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJQYWdvcyByZWFsaXphZG9zIgoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLmVudGlkYWQuY29kaWdvfSDigJQge3NlbGYucmVmZXJlbmNpYX0iCgoKY2xhc3MgQ29udGFjdG9Db2JyYW56YShUaW1lU3RhbXBlZE1vZGVsKToKICAgIGVudGlkYWQgPSBtb2RlbHMuRm9yZWlnbktleShFbnRpZGFkLCBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsIHJlbGF0ZWRfbmFtZT0iY29udGFjdG9zX2NvYnJhbnphIikKICAgIG5vbWJyZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMjApCiAgICB0ZWxlZm9ubyA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD00MCwgYmxhbms9VHJ1ZSkKICAgIGVtYWlsID0gbW9kZWxzLkVtYWlsRmllbGQoYmxhbms9VHJ1ZSkKICAgIGFjdGl2byA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbImVudGlkYWRfX25vbWJyZSIsICJub21icmUiXQogICAgICAgIHZlcmJvc2VfbmFtZSA9ICJDb250YWN0byBkZSBjb2JyYW56YSIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIkNvbnRhY3RvcyBkZSBjb2JyYW56YSIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi5ub21icmV9ICh7c2VsZi5lbnRpZGFkLmNvZGlnb30pIgoKCmNsYXNzIFJpc2tPcGVyYXRpb25TbmFwc2hvdChUaW1lU3RhbXBlZE1vZGVsKToKICAgICIiIgogICAgU25hcHNob3Qgb3BlcmF0aXZvIGRlIHJpZXNnbyAoQmFsw7NuKS4KICAgIENsYXZlIG5hdHVyYWw6IChgZW50aWRhZGAsIGByZWZlcmVuY2lhX29wZXJhY2lvbmAsIGBmZWNoYV9zbmFwc2hvdGApLgogICAgIiIiCiAgICBOSVZFTF9CQUpPID0gIkJBSk8iCiAgICBOSVZFTF9NRURJTyA9ICJNRURJTyIKICAgIE5JVkVMX0FMVE8gPSAiQUxUTyIKICAgIE5JVkVMX0NSSVRJQ08gPSAiQ1JJVElDTyIKICAgIE5JVkVMX0NIT0lDRVMgPSBbCiAgICAgICAgKE5JVkVMX0JBSk8sICJCYWpvIiksCiAgICAgICAgKE5JVkVMX01FRElPLCAiTWVkaW8iKSwKICAgICAgICAoTklWRUxfQUxUTywgIkFsdG8iKSwKICAgICAgICAoTklWRUxfQ1JJVElDTywgIkNyw610aWNvIiksCiAgICBdCgogICAgZW50aWRhZCA9IG1vZGVscy5Gb3JlaWduS2V5KEVudGlkYWQsIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSwgcmVsYXRlZF9uYW1lPSJyaXNrX3NuYXBzaG90cyIpCiAgICBwcm9kdWN0byA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIFByb2R1Y3RvLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJyaXNrX3NuYXBzaG90cyIsCiAgICApCiAgICByZWZlcmVuY2lhX29wZXJhY2lvbiA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD04MCwgZGJfaW5kZXg9VHJ1ZSkKICAgIGZlY2hhX3NuYXBzaG90ID0gbW9kZWxzLkRhdGVGaWVsZCgpCiAgICBuaXZlbF9yaWVzZ28gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MjAsIGNob2ljZXM9TklWRUxfQ0hPSUNFUywgZGVmYXVsdD1OSVZFTF9NRURJTykKICAgIGRpYXNfbW9yYSA9IG1vZGVscy5Qb3NpdGl2ZUludGVnZXJGaWVsZChkZWZhdWx0PTApCiAgICBzYWxkbyA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xNiwgZGVjaW1hbF9wbGFjZXM9MiwgZGVmYXVsdD0wKQogICAgbW9udG9fZXhpZ2libGUgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKAogICAgICAgIG1heF9kaWdpdHM9MTYsCiAgICAgICAgZGVjaW1hbF9wbGFjZXM9MiwKICAgICAgICBkZWZhdWx0PTAsCiAgICAgICAgaGVscF90ZXh0PSJNb250byB2ZW5jaWRvL2V4aWdpYmxlIGFsIG1vbWVudG8gZGVsIHNuYXBzaG90LiIsCiAgICApCiAgICBhbGVydGEgPSBtb2RlbHMuQm9vbGVhbkZpZWxkKGRlZmF1bHQ9RmFsc2UpCiAgICBkZXRhbGxlID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgdW5pcXVlX3RvZ2V0aGVyID0gKCJlbnRpZGFkIiwgInJlZmVyZW5jaWFfb3BlcmFjaW9uIiwgImZlY2hhX3NuYXBzaG90IikKICAgICAgICBvcmRlcmluZyA9IFsiLWZlY2hhX3NuYXBzaG90IiwgImVudGlkYWRfX25vbWJyZSJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIlNuYXBzaG90IG9wZXJhdGl2byBkZSByaWVzZ28iCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJTbmFwc2hvdHMgb3BlcmF0aXZvcyBkZSByaWVzZ28iCgogICAgZGVmIF9fc3RyX18oc2VsZik6CiAgICAgICAgcmV0dXJuIGYie3NlbGYucmVmZXJlbmNpYV9vcGVyYWNpb259IOKAlCB7c2VsZi5mZWNoYV9zbmFwc2hvdH0iCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=risk/selectors.py
PATH_JSON="risk/selectors.py"
FILENAME=selectors.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=61
SIZE_BYTES_UTF8=2137
CONTENT_SHA256=2c38b2a649226d6e502660d9b58894602814b881a5d7c1930d5c8fa4d638c60f
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Consultas reutilizables Risk / Comando Balón (modelos productivos)."""

from __future__ import annotations

from django.db.models import Count, Max, Sum

from risk.models import RiskOperationSnapshot


def latest_snapshots_queryset(request=None):
    """Último snapshot por (entidad, referencia_operacion)."""
    latest = (
        RiskOperationSnapshot.objects.values("entidad_id", "referencia_operacion")
        .annotate(ultima=Max("fecha_snapshot"))
    )
    ids = []
    for row in latest:
        snap = (
            RiskOperationSnapshot.objects.filter(
                entidad_id=row["entidad_id"],
                referencia_operacion=row["referencia_operacion"],
                fecha_snapshot=row["ultima"],
            )
            .values_list("id", flat=True)
            .first()
        )
        if snap:
            ids.append(snap)
    qs = RiskOperationSnapshot.objects.filter(id__in=ids).select_related(
        "entidad", "entidad__unidad_negocio", "producto"
    ).order_by("-dias_mora", "-fecha_snapshot", "entidad__nombre")

    if request is not None:
        cliente = request.GET.get("cliente", "").strip()
        if cliente:
            qs = qs.filter(entidad__nombre__icontains=cliente)
        nivel = request.GET.get("nivel", "").strip()
        if nivel:
            qs = qs.filter(nivel_riesgo=nivel)
        alerta = request.GET.get("alerta", "").strip()
        if alerta == "1":
            qs = qs.filter(alerta=True)
        elif alerta == "0":
            qs = qs.filter(alerta=False)
    return qs


def snapshot_summary(queryset):
    clientes = queryset.values("entidad_id").distinct().count()
    con_mora = queryset.filter(dias_mora__gt=0).count()
    sum_vencido = queryset.aggregate(total=Sum("monto_exigible"))["total"] or 0
    operaciones = queryset.values("referencia_operacion").distinct().count()
    alertas = queryset.filter(alerta=True).count()
    return {
        "total_snapshots": queryset.count(),
        "clientes": clientes,
        "operaciones": operaciones,
        "con_mora": con_mora,
        "suma_vencido": sum_vencido,
        "alertas": alertas,
    }

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Consultas reutilizables Risk / Comando Balón (modelos productivos)."""
00002|
00003|from __future__ import annotations
00004|
00005|from django.db.models import Count, Max, Sum
00006|
00007|from risk.models import RiskOperationSnapshot
00008|
00009|
00010|def latest_snapshots_queryset(request=None):
00011|    """Último snapshot por (entidad, referencia_operacion)."""
00012|    latest = (
00013|        RiskOperationSnapshot.objects.values("entidad_id", "referencia_operacion")
00014|        .annotate(ultima=Max("fecha_snapshot"))
00015|    )
00016|    ids = []
00017|    for row in latest:
00018|        snap = (
00019|            RiskOperationSnapshot.objects.filter(
00020|                entidad_id=row["entidad_id"],
00021|                referencia_operacion=row["referencia_operacion"],
00022|                fecha_snapshot=row["ultima"],
00023|            )
00024|            .values_list("id", flat=True)
00025|            .first()
00026|        )
00027|        if snap:
00028|            ids.append(snap)
00029|    qs = RiskOperationSnapshot.objects.filter(id__in=ids).select_related(
00030|        "entidad", "entidad__unidad_negocio", "producto"
00031|    ).order_by("-dias_mora", "-fecha_snapshot", "entidad__nombre")
00032|
00033|    if request is not None:
00034|        cliente = request.GET.get("cliente", "").strip()
00035|        if cliente:
00036|            qs = qs.filter(entidad__nombre__icontains=cliente)
00037|        nivel = request.GET.get("nivel", "").strip()
00038|        if nivel:
00039|            qs = qs.filter(nivel_riesgo=nivel)
00040|        alerta = request.GET.get("alerta", "").strip()
00041|        if alerta == "1":
00042|            qs = qs.filter(alerta=True)
00043|        elif alerta == "0":
00044|            qs = qs.filter(alerta=False)
00045|    return qs
00046|
00047|
00048|def snapshot_summary(queryset):
00049|    clientes = queryset.values("entidad_id").distinct().count()
00050|    con_mora = queryset.filter(dias_mora__gt=0).count()
00051|    sum_vencido = queryset.aggregate(total=Sum("monto_exigible"))["total"] or 0
00052|    operaciones = queryset.values("referencia_operacion").distinct().count()
00053|    alertas = queryset.filter(alerta=True).count()
00054|    return {
00055|        "total_snapshots": queryset.count(),
00056|        "clientes": clientes,
00057|        "operaciones": operaciones,
00058|        "con_mora": con_mora,
00059|        "suma_vencido": sum_vencido,
00060|        "alertas": alertas,
00061|    }

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiQ29uc3VsdGFzIHJldXRpbGl6YWJsZXMgUmlzayAvIENvbWFuZG8gQmFsw7NuIChtb2RlbG9zIHByb2R1Y3Rpdm9zKS4iIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmZyb20gZGphbmdvLmRiLm1vZGVscyBpbXBvcnQgQ291bnQsIE1heCwgU3VtCgpmcm9tIHJpc2subW9kZWxzIGltcG9ydCBSaXNrT3BlcmF0aW9uU25hcHNob3QKCgpkZWYgbGF0ZXN0X3NuYXBzaG90c19xdWVyeXNldChyZXF1ZXN0PU5vbmUpOgogICAgIiIiw5psdGltbyBzbmFwc2hvdCBwb3IgKGVudGlkYWQsIHJlZmVyZW5jaWFfb3BlcmFjaW9uKS4iIiIKICAgIGxhdGVzdCA9ICgKICAgICAgICBSaXNrT3BlcmF0aW9uU25hcHNob3Qub2JqZWN0cy52YWx1ZXMoImVudGlkYWRfaWQiLCAicmVmZXJlbmNpYV9vcGVyYWNpb24iKQogICAgICAgIC5hbm5vdGF0ZSh1bHRpbWE9TWF4KCJmZWNoYV9zbmFwc2hvdCIpKQogICAgKQogICAgaWRzID0gW10KICAgIGZvciByb3cgaW4gbGF0ZXN0OgogICAgICAgIHNuYXAgPSAoCiAgICAgICAgICAgIFJpc2tPcGVyYXRpb25TbmFwc2hvdC5vYmplY3RzLmZpbHRlcigKICAgICAgICAgICAgICAgIGVudGlkYWRfaWQ9cm93WyJlbnRpZGFkX2lkIl0sCiAgICAgICAgICAgICAgICByZWZlcmVuY2lhX29wZXJhY2lvbj1yb3dbInJlZmVyZW5jaWFfb3BlcmFjaW9uIl0sCiAgICAgICAgICAgICAgICBmZWNoYV9zbmFwc2hvdD1yb3dbInVsdGltYSJdLAogICAgICAgICAgICApCiAgICAgICAgICAgIC52YWx1ZXNfbGlzdCgiaWQiLCBmbGF0PVRydWUpCiAgICAgICAgICAgIC5maXJzdCgpCiAgICAgICAgKQogICAgICAgIGlmIHNuYXA6CiAgICAgICAgICAgIGlkcy5hcHBlbmQoc25hcCkKICAgIHFzID0gUmlza09wZXJhdGlvblNuYXBzaG90Lm9iamVjdHMuZmlsdGVyKGlkX19pbj1pZHMpLnNlbGVjdF9yZWxhdGVkKAogICAgICAgICJlbnRpZGFkIiwgImVudGlkYWRfX3VuaWRhZF9uZWdvY2lvIiwgInByb2R1Y3RvIgogICAgKS5vcmRlcl9ieSgiLWRpYXNfbW9yYSIsICItZmVjaGFfc25hcHNob3QiLCAiZW50aWRhZF9fbm9tYnJlIikKCiAgICBpZiByZXF1ZXN0IGlzIG5vdCBOb25lOgogICAgICAgIGNsaWVudGUgPSByZXF1ZXN0LkdFVC5nZXQoImNsaWVudGUiLCAiIikuc3RyaXAoKQogICAgICAgIGlmIGNsaWVudGU6CiAgICAgICAgICAgIHFzID0gcXMuZmlsdGVyKGVudGlkYWRfX25vbWJyZV9faWNvbnRhaW5zPWNsaWVudGUpCiAgICAgICAgbml2ZWwgPSByZXF1ZXN0LkdFVC5nZXQoIm5pdmVsIiwgIiIpLnN0cmlwKCkKICAgICAgICBpZiBuaXZlbDoKICAgICAgICAgICAgcXMgPSBxcy5maWx0ZXIobml2ZWxfcmllc2dvPW5pdmVsKQogICAgICAgIGFsZXJ0YSA9IHJlcXVlc3QuR0VULmdldCgiYWxlcnRhIiwgIiIpLnN0cmlwKCkKICAgICAgICBpZiBhbGVydGEgPT0gIjEiOgogICAgICAgICAgICBxcyA9IHFzLmZpbHRlcihhbGVydGE9VHJ1ZSkKICAgICAgICBlbGlmIGFsZXJ0YSA9PSAiMCI6CiAgICAgICAgICAgIHFzID0gcXMuZmlsdGVyKGFsZXJ0YT1GYWxzZSkKICAgIHJldHVybiBxcwoKCmRlZiBzbmFwc2hvdF9zdW1tYXJ5KHF1ZXJ5c2V0KToKICAgIGNsaWVudGVzID0gcXVlcnlzZXQudmFsdWVzKCJlbnRpZGFkX2lkIikuZGlzdGluY3QoKS5jb3VudCgpCiAgICBjb25fbW9yYSA9IHF1ZXJ5c2V0LmZpbHRlcihkaWFzX21vcmFfX2d0PTApLmNvdW50KCkKICAgIHN1bV92ZW5jaWRvID0gcXVlcnlzZXQuYWdncmVnYXRlKHRvdGFsPVN1bSgibW9udG9fZXhpZ2libGUiKSlbInRvdGFsIl0gb3IgMAogICAgb3BlcmFjaW9uZXMgPSBxdWVyeXNldC52YWx1ZXMoInJlZmVyZW5jaWFfb3BlcmFjaW9uIikuZGlzdGluY3QoKS5jb3VudCgpCiAgICBhbGVydGFzID0gcXVlcnlzZXQuZmlsdGVyKGFsZXJ0YT1UcnVlKS5jb3VudCgpCiAgICByZXR1cm4gewogICAgICAgICJ0b3RhbF9zbmFwc2hvdHMiOiBxdWVyeXNldC5jb3VudCgpLAogICAgICAgICJjbGllbnRlcyI6IGNsaWVudGVzLAogICAgICAgICJvcGVyYWNpb25lcyI6IG9wZXJhY2lvbmVzLAogICAgICAgICJjb25fbW9yYSI6IGNvbl9tb3JhLAogICAgICAgICJzdW1hX3ZlbmNpZG8iOiBzdW1fdmVuY2lkbywKICAgICAgICAiYWxlcnRhcyI6IGFsZXJ0YXMsCiAgICB9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=risk/services.py
PATH_JSON="risk/services.py"
FILENAME=services.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=419
SIZE_BYTES_UTF8=14445
CONTENT_SHA256=6a247ba040630f7c6b6751f48772c29150c14fb30de1ff033183fed5c28afc17
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""
Importadores Risk / Balón.

Archivo referencia leasing:
  `balon datos - Ejemplo de datos Riesgo al 31-mayo para una operacion - Base de datos Leasing.xlsx`

Columnas mínimas (alias):
  - cliente / nombre + nit (crea Entidad si no existe)
  - operacion / referencia_operacion / contrato
  - fecha_snapshot / fecha_corte / al_31_mayo
  - saldo, dias_mora / dias_atraso, monto_exigible / exigible

Clave natural snapshot: (entidad, referencia_operacion, fecha_snapshot)
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

import pandas as pd

from core.services.column_map import normalize_columns, pick, pick_decimal, pick_int, require_any
from core.services.import_base import read_dataframe, run_import_batch
from core.wcg_models import DataImportBatch, Entidad, Producto, UnidadNegocio
from crm.services import _entidad_codigo_from_row, _resolve_unidad, _slug_codigo
from risk.models import (
    EstadoFinanciero,
    PagoRealizado,
    ProgramacionPago,
    RiskOperationSnapshot,
)


def _parse_date(value: str) -> date | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(value[:19], fmt).date()
        except ValueError:
            continue
    try:
        return pd.to_datetime(value).date()
    except Exception:
        return None


def _ensure_entidad_from_row(row: pd.Series, errors: list[str]) -> Entidad | None:
    nombre = pick(
        row,
        "cliente",
        "nombre",
        "razon_social",
        "nombre_cliente",
        "client_name",
    )
    nit = pick(row, "nit", "nit_cliente")
    client_id = pick(row, "client_id", "cliente_id")
    codigo = (
        pick(row, "entidad_codigo", "codigo_cliente")
        or (f"CLI{client_id}" if client_id else "")
        or _entidad_codigo_from_row(row)
    )
    if not nombre and not codigo:
        errors.append("falta cliente o identificador")
        return None
    if not nombre:
        nombre = codigo
    if not codigo:
        codigo = _slug_codigo(nombre[:20])
    unidad = _resolve_unidad(
        pick(row, "unidad", "une", "unidad_negocio", "owning_business_unit", "financial_entity")
        or "LEASING"
    )
    if unidad is None:
        unidad = UnidadNegocio.objects.filter(code="LEASING").first()
    entidad, _ = Entidad.objects.update_or_create(
        codigo=codigo,
        defaults={"nombre": nombre, "nit": nit, "unidad_negocio": unidad, "activa": True},
    )
    return entidad


def _nivel_from_mora(dias: int) -> str:
    if dias >= 90:
        return RiskOperationSnapshot.NIVEL_CRITICO
    if dias >= 60:
        return RiskOperationSnapshot.NIVEL_ALTO
    if dias >= 30:
        return RiskOperationSnapshot.NIVEL_MEDIO
    return RiskOperationSnapshot.NIVEL_BAJO


def import_leasing_database(user, uploaded_file) -> DataImportBatch:
    from core.services.import_base import read_dataframe

    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(
        df,
        [
            ["cliente", "nombre", "razon_social", "client_name", "nombre_cliente"],
            [
                "operacion",
                "referencia_operacion",
                "contrato",
                "no_operacion",
                "contract_number",
                "no_contrato",
            ],
        ],
    )
    uploaded_file.seek(0)

    def handler(row: pd.Series, errors: list[str]):
        entidad = _ensure_entidad_from_row(row, errors)
        if not entidad:
            return None
        referencia = pick(
            row,
            "operacion",
            "referencia_operacion",
            "contrato",
            "no_operacion",
            "no_contrato",
            "contract_number",
        )
        if not referencia:
            errors.append("falta referencia de operación")
            return None
        fecha_raw = pick(
            row,
            "fecha_snapshot",
            "fecha_corte",
            "al_31_mayo",
            "fecha",
            "corte",
            "balance_until",
            "final_validity",
        )
        fecha = _parse_date(fecha_raw) or date(2026, 6, 30)
        dias = pick_int(
            row,
            "dias_mora",
            "dias_atraso",
            "dias_de_mora",
            "mora_dias",
            "duedays",
            "due_days",
        )
        saldo = pick_decimal(
            row,
            "saldo",
            "saldo_total",
            "saldo_operacion",
            "capital_balance",
            "total_capital",
        )
        exigible = pick_decimal(
            row,
            "monto_exigible",
            "exigible",
            "monto_vencido",
            "vencido",
            "past_due_balance",
        )
        if exigible == 0 and saldo > 0 and dias > 0:
            exigible = saldo
        nivel = pick(row, "nivel_riesgo", "categoria_riesgo").upper() or _nivel_from_mora(dias)
        if nivel not in dict(RiskOperationSnapshot.NIVEL_CHOICES):
            nivel = _nivel_from_mora(dias)
        alerta_raw = pick(row, "alerta", "en_alerta", "status")
        alerta = dias >= 30 or alerta_raw.lower() in ("1", "si", "sí", "true", "yes", "vencido", "mora")
        prod_raw = pick(row, "producto", "producto_codigo") or "LEASING"
        prod_code = _slug_codigo(prod_raw)[:50] or "LEASING"
        producto, _ = Producto.objects.get_or_create(
            codigo=prod_code,
            defaults={"nombre": prod_raw[:200] or "Leasing", "activo": True},
        )
        detalle_parts = [
            pick(row, "detalle", "observaciones", "notas"),
            f"Status={pick(row, 'status')}" if pick(row, "status") else "",
            f"Advisor={pick(row, 'advisor_name')}" if pick(row, "advisor_name") else "",
            f"Cuotas pend.={pick(row, 'outstanding_installments')}"
            if pick(row, "outstanding_installments")
            else "",
        ]
        detalle = " | ".join(p for p in detalle_parts if p)
        _, created = RiskOperationSnapshot.objects.update_or_create(
            entidad=entidad,
            referencia_operacion=referencia,
            fecha_snapshot=fecha,
            defaults={
                "producto": producto,
                "nivel_riesgo": nivel,
                "dias_mora": dias,
                "saldo": saldo,
                "monto_exigible": exigible,
                "alerta": alerta,
                "detalle": detalle,
            },
        )
        periodo = fecha.strftime("%Y-%m")
        EstadoFinanciero.objects.update_or_create(
            entidad=entidad,
            periodo=periodo,
            defaults={
                "saldo_total": saldo,
                "mora_dias": dias,
                "exposicion": saldo,
            },
        )
        return created, not created

    uploaded_file.seek(0)
    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_RISK,
        tipo_importacion="leasing_database",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_leasing_rentas(user, uploaded_file) -> DataImportBatch:
    """
    Enriquecimiento Balón: cuotas/rentas por contrato.
    Archivo: LeasingRentasYYYY-MM-DD.csv
    Matching: NoContrato → Entidad vía RiskOperationSnapshot.referencia_operacion
              o creación de ProgramacionPago / PagoRealizado.
    """
    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(
        df,
        [
            ["no_contrato", "contrato", "contract_number", "referencia"],
            ["vencimiento", "fecha_programada", "fecha_vencimiento"],
        ],
    )
    uploaded_file.seek(0)

    def handler(row: pd.Series, errors: list[str]):
        contrato = pick(row, "no_contrato", "contrato", "contract_number", "referencia", "operacion")
        if not contrato:
            errors.append("falta NoContrato")
            return None
        snap = (
            RiskOperationSnapshot.objects.filter(referencia_operacion__iexact=contrato)
            .select_related("entidad")
            .order_by("-fecha_snapshot")
            .first()
        )
        if snap:
            entidad = snap.entidad
        else:
            # Crear entidad mínima si el contrato aún no está en snapshots
            entidad, _ = Entidad.objects.get_or_create(
                codigo=_slug_codigo(contrato),
                defaults={
                    "nombre": f"Contrato {contrato}",
                    "unidad_negocio": UnidadNegocio.objects.filter(code="LEASING").first(),
                    "activa": True,
                    "tipo": Entidad.TIPO_CLIENTE,
                },
            )
        nro = pick(row, "no", "numero", "cuota", "nro") or "0"
        referencia = f"{contrato}-C{nro}"
        fecha = _parse_date(pick(row, "vencimiento", "fecha_programada", "fecha_vencimiento"))
        if not fecha:
            errors.append("falta fecha vencimiento")
            return None
        monto = pick_decimal(row, "renta_total", "valor_renta_con_mora", "valor_renta", "monto")
        estado = pick(row, "estado", "status").lower()
        _, created_prog = ProgramacionPago.objects.update_or_create(
            entidad=entidad,
            referencia=referencia,
            defaults={
                "fecha_programada": fecha,
                "monto": monto,
                "moneda": "GTQ",
            },
        )
        created = created_prog
        updated = not created_prog
        fecha_pago = _parse_date(pick(row, "fecha_pago"))
        if fecha_pago or estado in ("pagada", "pagado", "paid"):
            _, created_pago = PagoRealizado.objects.update_or_create(
                entidad=entidad,
                referencia=referencia,
                defaults={
                    "fecha_pago": fecha_pago or fecha,
                    "monto": monto,
                    "moneda": "GTQ",
                },
            )
            created = created or created_pago
            updated = updated or (not created_pago)
        return created, updated and not created

    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_RISK,
        tipo_importacion="leasing_rentas",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_estados_financieros(user, uploaded_file) -> DataImportBatch:
    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(df, [["entidad_codigo", "nit", "cliente"], ["periodo"]])

    def handler(row: pd.Series, errors: list[str]):
        entidad = _ensure_entidad_from_row(row, errors)
        if not entidad:
            return None
        periodo = pick(row, "periodo", "anio_mes", "mes")
        if not periodo:
            errors.append("periodo obligatorio")
            return None
        periodo = periodo.replace("/", "-")[:7]
        _, created = EstadoFinanciero.objects.update_or_create(
            entidad=entidad,
            periodo=periodo,
            defaults={
                "saldo_total": pick_decimal(row, "saldo_total", "saldo"),
                "mora_dias": pick_int(row, "mora_dias", "dias_mora"),
                "exposicion": pick_decimal(row, "exposicion"),
                "notas": pick(row, "notas"),
            },
        )
        return created, not created

    uploaded_file.seek(0)
    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_RISK,
        tipo_importacion="estados_financieros",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_programacion_pagos(user, uploaded_file) -> DataImportBatch:
    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(df, [["referencia", "operacion"], ["fecha_programada", "fecha_pago_programada"], ["monto"]])

    def handler(row: pd.Series, errors: list[str]):
        entidad = _ensure_entidad_from_row(row, errors)
        if not entidad:
            return None
        referencia = pick(row, "referencia", "operacion", "cuota")
        fecha = _parse_date(pick(row, "fecha_programada", "fecha_vencimiento"))
        if not referencia or not fecha:
            errors.append("referencia y fecha_programada obligatorias")
            return None
        _, created = ProgramacionPago.objects.update_or_create(
            entidad=entidad,
            referencia=referencia,
            defaults={
                "fecha_programada": fecha,
                "monto": pick_decimal(row, "monto"),
                "moneda": pick(row, "moneda") or "GTQ",
            },
        )
        return created, not created

    uploaded_file.seek(0)
    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_RISK,
        tipo_importacion="programacion_pagos",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_pagos_realizados(user, uploaded_file) -> DataImportBatch:
    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(df, [["referencia", "operacion"], ["fecha_pago"], ["monto"]])

    def handler(row: pd.Series, errors: list[str]):
        entidad = _ensure_entidad_from_row(row, errors)
        if not entidad:
            return None
        referencia = pick(row, "referencia", "operacion", "cuota")
        fecha = _parse_date(pick(row, "fecha_pago"))
        if not referencia or not fecha:
            errors.append("referencia y fecha_pago obligatorias")
            return None
        _, created = PagoRealizado.objects.update_or_create(
            entidad=entidad,
            referencia=referencia,
            defaults={
                "fecha_pago": fecha,
                "monto": pick_decimal(row, "monto"),
                "moneda": pick(row, "moneda") or "GTQ",
            },
        )
        return created, not created

    uploaded_file.seek(0)
    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_RISK,
        tipo_importacion="pagos_realizados",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_snapshots(user, uploaded_file) -> DataImportBatch:
    """CSV genérico de snapshots — mismo mapeo que leasing en formato plano."""
    return import_leasing_database(user, uploaded_file)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Importadores Risk / Balón.
00003|
00004|Archivo referencia leasing:
00005|  `balon datos - Ejemplo de datos Riesgo al 31-mayo para una operacion - Base de datos Leasing.xlsx`
00006|
00007|Columnas mínimas (alias):
00008|  - cliente / nombre + nit (crea Entidad si no existe)
00009|  - operacion / referencia_operacion / contrato
00010|  - fecha_snapshot / fecha_corte / al_31_mayo
00011|  - saldo, dias_mora / dias_atraso, monto_exigible / exigible
00012|
00013|Clave natural snapshot: (entidad, referencia_operacion, fecha_snapshot)
00014|"""
00015|
00016|from __future__ import annotations
00017|
00018|from datetime import date, datetime
00019|from decimal import Decimal
00020|
00021|import pandas as pd
00022|
00023|from core.services.column_map import normalize_columns, pick, pick_decimal, pick_int, require_any
00024|from core.services.import_base import read_dataframe, run_import_batch
00025|from core.wcg_models import DataImportBatch, Entidad, Producto, UnidadNegocio
00026|from crm.services import _entidad_codigo_from_row, _resolve_unidad, _slug_codigo
00027|from risk.models import (
00028|    EstadoFinanciero,
00029|    PagoRealizado,
00030|    ProgramacionPago,
00031|    RiskOperationSnapshot,
00032|)
00033|
00034|
00035|def _parse_date(value: str) -> date | None:
00036|    if not value:
00037|        return None
00038|    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S"):
00039|        try:
00040|            return datetime.strptime(value[:19], fmt).date()
00041|        except ValueError:
00042|            continue
00043|    try:
00044|        return pd.to_datetime(value).date()
00045|    except Exception:
00046|        return None
00047|
00048|
00049|def _ensure_entidad_from_row(row: pd.Series, errors: list[str]) -> Entidad | None:
00050|    nombre = pick(
00051|        row,
00052|        "cliente",
00053|        "nombre",
00054|        "razon_social",
00055|        "nombre_cliente",
00056|        "client_name",
00057|    )
00058|    nit = pick(row, "nit", "nit_cliente")
00059|    client_id = pick(row, "client_id", "cliente_id")
00060|    codigo = (
00061|        pick(row, "entidad_codigo", "codigo_cliente")
00062|        or (f"CLI{client_id}" if client_id else "")
00063|        or _entidad_codigo_from_row(row)
00064|    )
00065|    if not nombre and not codigo:
00066|        errors.append("falta cliente o identificador")
00067|        return None
00068|    if not nombre:
00069|        nombre = codigo
00070|    if not codigo:
00071|        codigo = _slug_codigo(nombre[:20])
00072|    unidad = _resolve_unidad(
00073|        pick(row, "unidad", "une", "unidad_negocio", "owning_business_unit", "financial_entity")
00074|        or "LEASING"
00075|    )
00076|    if unidad is None:
00077|        unidad = UnidadNegocio.objects.filter(code="LEASING").first()
00078|    entidad, _ = Entidad.objects.update_or_create(
00079|        codigo=codigo,
00080|        defaults={"nombre": nombre, "nit": nit, "unidad_negocio": unidad, "activa": True},
00081|    )
00082|    return entidad
00083|
00084|
00085|def _nivel_from_mora(dias: int) -> str:
00086|    if dias >= 90:
00087|        return RiskOperationSnapshot.NIVEL_CRITICO
00088|    if dias >= 60:
00089|        return RiskOperationSnapshot.NIVEL_ALTO
00090|    if dias >= 30:
00091|        return RiskOperationSnapshot.NIVEL_MEDIO
00092|    return RiskOperationSnapshot.NIVEL_BAJO
00093|
00094|
00095|def import_leasing_database(user, uploaded_file) -> DataImportBatch:
00096|    from core.services.import_base import read_dataframe
00097|
00098|    df = normalize_columns(read_dataframe(uploaded_file))
00099|    require_any(
00100|        df,
00101|        [
00102|            ["cliente", "nombre", "razon_social", "client_name", "nombre_cliente"],
00103|            [
00104|                "operacion",
00105|                "referencia_operacion",
00106|                "contrato",
00107|                "no_operacion",
00108|                "contract_number",
00109|                "no_contrato",
00110|            ],
00111|        ],
00112|    )
00113|    uploaded_file.seek(0)
00114|
00115|    def handler(row: pd.Series, errors: list[str]):
00116|        entidad = _ensure_entidad_from_row(row, errors)
00117|        if not entidad:
00118|            return None
00119|        referencia = pick(
00120|            row,
00121|            "operacion",
00122|            "referencia_operacion",
00123|            "contrato",
00124|            "no_operacion",
00125|            "no_contrato",
00126|            "contract_number",
00127|        )
00128|        if not referencia:
00129|            errors.append("falta referencia de operación")
00130|            return None
00131|        fecha_raw = pick(
00132|            row,
00133|            "fecha_snapshot",
00134|            "fecha_corte",
00135|            "al_31_mayo",
00136|            "fecha",
00137|            "corte",
00138|            "balance_until",
00139|            "final_validity",
00140|        )
00141|        fecha = _parse_date(fecha_raw) or date(2026, 6, 30)
00142|        dias = pick_int(
00143|            row,
00144|            "dias_mora",
00145|            "dias_atraso",
00146|            "dias_de_mora",
00147|            "mora_dias",
00148|            "duedays",
00149|            "due_days",
00150|        )
00151|        saldo = pick_decimal(
00152|            row,
00153|            "saldo",
00154|            "saldo_total",
00155|            "saldo_operacion",
00156|            "capital_balance",
00157|            "total_capital",
00158|        )
00159|        exigible = pick_decimal(
00160|            row,
00161|            "monto_exigible",
00162|            "exigible",
00163|            "monto_vencido",
00164|            "vencido",
00165|            "past_due_balance",
00166|        )
00167|        if exigible == 0 and saldo > 0 and dias > 0:
00168|            exigible = saldo
00169|        nivel = pick(row, "nivel_riesgo", "categoria_riesgo").upper() or _nivel_from_mora(dias)
00170|        if nivel not in dict(RiskOperationSnapshot.NIVEL_CHOICES):
00171|            nivel = _nivel_from_mora(dias)
00172|        alerta_raw = pick(row, "alerta", "en_alerta", "status")
00173|        alerta = dias >= 30 or alerta_raw.lower() in ("1", "si", "sí", "true", "yes", "vencido", "mora")
00174|        prod_raw = pick(row, "producto", "producto_codigo") or "LEASING"
00175|        prod_code = _slug_codigo(prod_raw)[:50] or "LEASING"
00176|        producto, _ = Producto.objects.get_or_create(
00177|            codigo=prod_code,
00178|            defaults={"nombre": prod_raw[:200] or "Leasing", "activo": True},
00179|        )
00180|        detalle_parts = [
00181|            pick(row, "detalle", "observaciones", "notas"),
00182|            f"Status={pick(row, 'status')}" if pick(row, "status") else "",
00183|            f"Advisor={pick(row, 'advisor_name')}" if pick(row, "advisor_name") else "",
00184|            f"Cuotas pend.={pick(row, 'outstanding_installments')}"
00185|            if pick(row, "outstanding_installments")
00186|            else "",
00187|        ]
00188|        detalle = " | ".join(p for p in detalle_parts if p)
00189|        _, created = RiskOperationSnapshot.objects.update_or_create(
00190|            entidad=entidad,
00191|            referencia_operacion=referencia,
00192|            fecha_snapshot=fecha,
00193|            defaults={
00194|                "producto": producto,
00195|                "nivel_riesgo": nivel,
00196|                "dias_mora": dias,
00197|                "saldo": saldo,
00198|                "monto_exigible": exigible,
00199|                "alerta": alerta,
00200|                "detalle": detalle,
00201|            },
00202|        )
00203|        periodo = fecha.strftime("%Y-%m")
00204|        EstadoFinanciero.objects.update_or_create(
00205|            entidad=entidad,
00206|            periodo=periodo,
00207|            defaults={
00208|                "saldo_total": saldo,
00209|                "mora_dias": dias,
00210|                "exposicion": saldo,
00211|            },
00212|        )
00213|        return created, not created
00214|
00215|    uploaded_file.seek(0)
00216|    return run_import_batch(
00217|        user=user,
00218|        modulo=DataImportBatch.MODULO_RISK,
00219|        tipo_importacion="leasing_database",
00220|        uploaded_file=uploaded_file,
00221|        required_columns=[],
00222|        row_handler=handler,
00223|    )
00224|
00225|
00226|def import_leasing_rentas(user, uploaded_file) -> DataImportBatch:
00227|    """
00228|    Enriquecimiento Balón: cuotas/rentas por contrato.
00229|    Archivo: LeasingRentasYYYY-MM-DD.csv
00230|    Matching: NoContrato → Entidad vía RiskOperationSnapshot.referencia_operacion
00231|              o creación de ProgramacionPago / PagoRealizado.
00232|    """
00233|    df = normalize_columns(read_dataframe(uploaded_file))
00234|    require_any(
00235|        df,
00236|        [
00237|            ["no_contrato", "contrato", "contract_number", "referencia"],
00238|            ["vencimiento", "fecha_programada", "fecha_vencimiento"],
00239|        ],
00240|    )
00241|    uploaded_file.seek(0)
00242|
00243|    def handler(row: pd.Series, errors: list[str]):
00244|        contrato = pick(row, "no_contrato", "contrato", "contract_number", "referencia", "operacion")
00245|        if not contrato:
00246|            errors.append("falta NoContrato")
00247|            return None
00248|        snap = (
00249|            RiskOperationSnapshot.objects.filter(referencia_operacion__iexact=contrato)
00250|            .select_related("entidad")
00251|            .order_by("-fecha_snapshot")
00252|            .first()
00253|        )
00254|        if snap:
00255|            entidad = snap.entidad
00256|        else:
00257|            # Crear entidad mínima si el contrato aún no está en snapshots
00258|            entidad, _ = Entidad.objects.get_or_create(
00259|                codigo=_slug_codigo(contrato),
00260|                defaults={
00261|                    "nombre": f"Contrato {contrato}",
00262|                    "unidad_negocio": UnidadNegocio.objects.filter(code="LEASING").first(),
00263|                    "activa": True,
00264|                    "tipo": Entidad.TIPO_CLIENTE,
00265|                },
00266|            )
00267|        nro = pick(row, "no", "numero", "cuota", "nro") or "0"
00268|        referencia = f"{contrato}-C{nro}"
00269|        fecha = _parse_date(pick(row, "vencimiento", "fecha_programada", "fecha_vencimiento"))
00270|        if not fecha:
00271|            errors.append("falta fecha vencimiento")
00272|            return None
00273|        monto = pick_decimal(row, "renta_total", "valor_renta_con_mora", "valor_renta", "monto")
00274|        estado = pick(row, "estado", "status").lower()
00275|        _, created_prog = ProgramacionPago.objects.update_or_create(
00276|            entidad=entidad,
00277|            referencia=referencia,
00278|            defaults={
00279|                "fecha_programada": fecha,
00280|                "monto": monto,
00281|                "moneda": "GTQ",
00282|            },
00283|        )
00284|        created = created_prog
00285|        updated = not created_prog
00286|        fecha_pago = _parse_date(pick(row, "fecha_pago"))
00287|        if fecha_pago or estado in ("pagada", "pagado", "paid"):
00288|            _, created_pago = PagoRealizado.objects.update_or_create(
00289|                entidad=entidad,
00290|                referencia=referencia,
00291|                defaults={
00292|                    "fecha_pago": fecha_pago or fecha,
00293|                    "monto": monto,
00294|                    "moneda": "GTQ",
00295|                },
00296|            )
00297|            created = created or created_pago
00298|            updated = updated or (not created_pago)
00299|        return created, updated and not created
00300|
00301|    return run_import_batch(
00302|        user=user,
00303|        modulo=DataImportBatch.MODULO_RISK,
00304|        tipo_importacion="leasing_rentas",
00305|        uploaded_file=uploaded_file,
00306|        required_columns=[],
00307|        row_handler=handler,
00308|    )
00309|
00310|
00311|def import_estados_financieros(user, uploaded_file) -> DataImportBatch:
00312|    df = normalize_columns(read_dataframe(uploaded_file))
00313|    require_any(df, [["entidad_codigo", "nit", "cliente"], ["periodo"]])
00314|
00315|    def handler(row: pd.Series, errors: list[str]):
00316|        entidad = _ensure_entidad_from_row(row, errors)
00317|        if not entidad:
00318|            return None
00319|        periodo = pick(row, "periodo", "anio_mes", "mes")
00320|        if not periodo:
00321|            errors.append("periodo obligatorio")
00322|            return None
00323|        periodo = periodo.replace("/", "-")[:7]
00324|        _, created = EstadoFinanciero.objects.update_or_create(
00325|            entidad=entidad,
00326|            periodo=periodo,
00327|            defaults={
00328|                "saldo_total": pick_decimal(row, "saldo_total", "saldo"),
00329|                "mora_dias": pick_int(row, "mora_dias", "dias_mora"),
00330|                "exposicion": pick_decimal(row, "exposicion"),
00331|                "notas": pick(row, "notas"),
00332|            },
00333|        )
00334|        return created, not created
00335|
00336|    uploaded_file.seek(0)
00337|    return run_import_batch(
00338|        user=user,
00339|        modulo=DataImportBatch.MODULO_RISK,
00340|        tipo_importacion="estados_financieros",
00341|        uploaded_file=uploaded_file,
00342|        required_columns=[],
00343|        row_handler=handler,
00344|    )
00345|
00346|
00347|def import_programacion_pagos(user, uploaded_file) -> DataImportBatch:
00348|    df = normalize_columns(read_dataframe(uploaded_file))
00349|    require_any(df, [["referencia", "operacion"], ["fecha_programada", "fecha_pago_programada"], ["monto"]])
00350|
00351|    def handler(row: pd.Series, errors: list[str]):
00352|        entidad = _ensure_entidad_from_row(row, errors)
00353|        if not entidad:
00354|            return None
00355|        referencia = pick(row, "referencia", "operacion", "cuota")
00356|        fecha = _parse_date(pick(row, "fecha_programada", "fecha_vencimiento"))
00357|        if not referencia or not fecha:
00358|            errors.append("referencia y fecha_programada obligatorias")
00359|            return None
00360|        _, created = ProgramacionPago.objects.update_or_create(
00361|            entidad=entidad,
00362|            referencia=referencia,
00363|            defaults={
00364|                "fecha_programada": fecha,
00365|                "monto": pick_decimal(row, "monto"),
00366|                "moneda": pick(row, "moneda") or "GTQ",
00367|            },
00368|        )
00369|        return created, not created
00370|
00371|    uploaded_file.seek(0)
00372|    return run_import_batch(
00373|        user=user,
00374|        modulo=DataImportBatch.MODULO_RISK,
00375|        tipo_importacion="programacion_pagos",
00376|        uploaded_file=uploaded_file,
00377|        required_columns=[],
00378|        row_handler=handler,
00379|    )
00380|
00381|
00382|def import_pagos_realizados(user, uploaded_file) -> DataImportBatch:
00383|    df = normalize_columns(read_dataframe(uploaded_file))
00384|    require_any(df, [["referencia", "operacion"], ["fecha_pago"], ["monto"]])
00385|
00386|    def handler(row: pd.Series, errors: list[str]):
00387|        entidad = _ensure_entidad_from_row(row, errors)
00388|        if not entidad:
00389|            return None
00390|        referencia = pick(row, "referencia", "operacion", "cuota")
00391|        fecha = _parse_date(pick(row, "fecha_pago"))
00392|        if not referencia or not fecha:
00393|            errors.append("referencia y fecha_pago obligatorias")
00394|            return None
00395|        _, created = PagoRealizado.objects.update_or_create(
00396|            entidad=entidad,
00397|            referencia=referencia,
00398|            defaults={
00399|                "fecha_pago": fecha,
00400|                "monto": pick_decimal(row, "monto"),
00401|                "moneda": pick(row, "moneda") or "GTQ",
00402|            },
00403|        )
00404|        return created, not created
00405|
00406|    uploaded_file.seek(0)
00407|    return run_import_batch(
00408|        user=user,
00409|        modulo=DataImportBatch.MODULO_RISK,
00410|        tipo_importacion="pagos_realizados",
00411|        uploaded_file=uploaded_file,
00412|        required_columns=[],
00413|        row_handler=handler,
00414|    )
00415|
00416|
00417|def import_snapshots(user, uploaded_file) -> DataImportBatch:
00418|    """CSV genérico de snapshots — mismo mapeo que leasing en formato plano."""
00419|    return import_leasing_database(user, uploaded_file)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiCkltcG9ydGFkb3JlcyBSaXNrIC8gQmFsw7NuLgoKQXJjaGl2byByZWZlcmVuY2lhIGxlYXNpbmc6CiAgYGJhbG9uIGRhdG9zIC0gRWplbXBsbyBkZSBkYXRvcyBSaWVzZ28gYWwgMzEtbWF5byBwYXJhIHVuYSBvcGVyYWNpb24gLSBCYXNlIGRlIGRhdG9zIExlYXNpbmcueGxzeGAKCkNvbHVtbmFzIG3DrW5pbWFzIChhbGlhcyk6CiAgLSBjbGllbnRlIC8gbm9tYnJlICsgbml0IChjcmVhIEVudGlkYWQgc2kgbm8gZXhpc3RlKQogIC0gb3BlcmFjaW9uIC8gcmVmZXJlbmNpYV9vcGVyYWNpb24gLyBjb250cmF0bwogIC0gZmVjaGFfc25hcHNob3QgLyBmZWNoYV9jb3J0ZSAvIGFsXzMxX21heW8KICAtIHNhbGRvLCBkaWFzX21vcmEgLyBkaWFzX2F0cmFzbywgbW9udG9fZXhpZ2libGUgLyBleGlnaWJsZQoKQ2xhdmUgbmF0dXJhbCBzbmFwc2hvdDogKGVudGlkYWQsIHJlZmVyZW5jaWFfb3BlcmFjaW9uLCBmZWNoYV9zbmFwc2hvdCkKIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgpmcm9tIGRhdGV0aW1lIGltcG9ydCBkYXRlLCBkYXRldGltZQpmcm9tIGRlY2ltYWwgaW1wb3J0IERlY2ltYWwKCmltcG9ydCBwYW5kYXMgYXMgcGQKCmZyb20gY29yZS5zZXJ2aWNlcy5jb2x1bW5fbWFwIGltcG9ydCBub3JtYWxpemVfY29sdW1ucywgcGljaywgcGlja19kZWNpbWFsLCBwaWNrX2ludCwgcmVxdWlyZV9hbnkKZnJvbSBjb3JlLnNlcnZpY2VzLmltcG9ydF9iYXNlIGltcG9ydCByZWFkX2RhdGFmcmFtZSwgcnVuX2ltcG9ydF9iYXRjaApmcm9tIGNvcmUud2NnX21vZGVscyBpbXBvcnQgRGF0YUltcG9ydEJhdGNoLCBFbnRpZGFkLCBQcm9kdWN0bywgVW5pZGFkTmVnb2Npbwpmcm9tIGNybS5zZXJ2aWNlcyBpbXBvcnQgX2VudGlkYWRfY29kaWdvX2Zyb21fcm93LCBfcmVzb2x2ZV91bmlkYWQsIF9zbHVnX2NvZGlnbwpmcm9tIHJpc2subW9kZWxzIGltcG9ydCAoCiAgICBFc3RhZG9GaW5hbmNpZXJvLAogICAgUGFnb1JlYWxpemFkbywKICAgIFByb2dyYW1hY2lvblBhZ28sCiAgICBSaXNrT3BlcmF0aW9uU25hcHNob3QsCikKCgpkZWYgX3BhcnNlX2RhdGUodmFsdWU6IHN0cikgLT4gZGF0ZSB8IE5vbmU6CiAgICBpZiBub3QgdmFsdWU6CiAgICAgICAgcmV0dXJuIE5vbmUKICAgIGZvciBmbXQgaW4gKCIlWS0lbS0lZCIsICIlZC8lbS8lWSIsICIlbS8lZC8lWSIsICIlWS0lbS0lZCAlSDolTTolUyIpOgogICAgICAgIHRyeToKICAgICAgICAgICAgcmV0dXJuIGRhdGV0aW1lLnN0cnB0aW1lKHZhbHVlWzoxOV0sIGZtdCkuZGF0ZSgpCiAgICAgICAgZXhjZXB0IFZhbHVlRXJyb3I6CiAgICAgICAgICAgIGNvbnRpbnVlCiAgICB0cnk6CiAgICAgICAgcmV0dXJuIHBkLnRvX2RhdGV0aW1lKHZhbHVlKS5kYXRlKCkKICAgIGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgcmV0dXJuIE5vbmUKCgpkZWYgX2Vuc3VyZV9lbnRpZGFkX2Zyb21fcm93KHJvdzogcGQuU2VyaWVzLCBlcnJvcnM6IGxpc3Rbc3RyXSkgLT4gRW50aWRhZCB8IE5vbmU6CiAgICBub21icmUgPSBwaWNrKAogICAgICAgIHJvdywKICAgICAgICAiY2xpZW50ZSIsCiAgICAgICAgIm5vbWJyZSIsCiAgICAgICAgInJhem9uX3NvY2lhbCIsCiAgICAgICAgIm5vbWJyZV9jbGllbnRlIiwKICAgICAgICAiY2xpZW50X25hbWUiLAogICAgKQogICAgbml0ID0gcGljayhyb3csICJuaXQiLCAibml0X2NsaWVudGUiKQogICAgY2xpZW50X2lkID0gcGljayhyb3csICJjbGllbnRfaWQiLCAiY2xpZW50ZV9pZCIpCiAgICBjb2RpZ28gPSAoCiAgICAgICAgcGljayhyb3csICJlbnRpZGFkX2NvZGlnbyIsICJjb2RpZ29fY2xpZW50ZSIpCiAgICAgICAgb3IgKGYiQ0xJe2NsaWVudF9pZH0iIGlmIGNsaWVudF9pZCBlbHNlICIiKQogICAgICAgIG9yIF9lbnRpZGFkX2NvZGlnb19mcm9tX3Jvdyhyb3cpCiAgICApCiAgICBpZiBub3Qgbm9tYnJlIGFuZCBub3QgY29kaWdvOgogICAgICAgIGVycm9ycy5hcHBlbmQoImZhbHRhIGNsaWVudGUgbyBpZGVudGlmaWNhZG9yIikKICAgICAgICByZXR1cm4gTm9uZQogICAgaWYgbm90IG5vbWJyZToKICAgICAgICBub21icmUgPSBjb2RpZ28KICAgIGlmIG5vdCBjb2RpZ286CiAgICAgICAgY29kaWdvID0gX3NsdWdfY29kaWdvKG5vbWJyZVs6MjBdKQogICAgdW5pZGFkID0gX3Jlc29sdmVfdW5pZGFkKAogICAgICAgIHBpY2socm93LCAidW5pZGFkIiwgInVuZSIsICJ1bmlkYWRfbmVnb2NpbyIsICJvd25pbmdfYnVzaW5lc3NfdW5pdCIsICJmaW5hbmNpYWxfZW50aXR5IikKICAgICAgICBvciAiTEVBU0lORyIKICAgICkKICAgIGlmIHVuaWRhZCBpcyBOb25lOgogICAgICAgIHVuaWRhZCA9IFVuaWRhZE5lZ29jaW8ub2JqZWN0cy5maWx0ZXIoY29kZT0iTEVBU0lORyIpLmZpcnN0KCkKICAgIGVudGlkYWQsIF8gPSBFbnRpZGFkLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICBjb2RpZ289Y29kaWdvLAogICAgICAgIGRlZmF1bHRzPXsibm9tYnJlIjogbm9tYnJlLCAibml0Ijogbml0LCAidW5pZGFkX25lZ29jaW8iOiB1bmlkYWQsICJhY3RpdmEiOiBUcnVlfSwKICAgICkKICAgIHJldHVybiBlbnRpZGFkCgoKZGVmIF9uaXZlbF9mcm9tX21vcmEoZGlhczogaW50KSAtPiBzdHI6CiAgICBpZiBkaWFzID49IDkwOgogICAgICAgIHJldHVybiBSaXNrT3BlcmF0aW9uU25hcHNob3QuTklWRUxfQ1JJVElDTwogICAgaWYgZGlhcyA+PSA2MDoKICAgICAgICByZXR1cm4gUmlza09wZXJhdGlvblNuYXBzaG90Lk5JVkVMX0FMVE8KICAgIGlmIGRpYXMgPj0gMzA6CiAgICAgICAgcmV0dXJuIFJpc2tPcGVyYXRpb25TbmFwc2hvdC5OSVZFTF9NRURJTwogICAgcmV0dXJuIFJpc2tPcGVyYXRpb25TbmFwc2hvdC5OSVZFTF9CQUpPCgoKZGVmIGltcG9ydF9sZWFzaW5nX2RhdGFiYXNlKHVzZXIsIHVwbG9hZGVkX2ZpbGUpIC0+IERhdGFJbXBvcnRCYXRjaDoKICAgIGZyb20gY29yZS5zZXJ2aWNlcy5pbXBvcnRfYmFzZSBpbXBvcnQgcmVhZF9kYXRhZnJhbWUKCiAgICBkZiA9IG5vcm1hbGl6ZV9jb2x1bW5zKHJlYWRfZGF0YWZyYW1lKHVwbG9hZGVkX2ZpbGUpKQogICAgcmVxdWlyZV9hbnkoCiAgICAgICAgZGYsCiAgICAgICAgWwogICAgICAgICAgICBbImNsaWVudGUiLCAibm9tYnJlIiwgInJhem9uX3NvY2lhbCIsICJjbGllbnRfbmFtZSIsICJub21icmVfY2xpZW50ZSJdLAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICAib3BlcmFjaW9uIiwKICAgICAgICAgICAgICAgICJyZWZlcmVuY2lhX29wZXJhY2lvbiIsCiAgICAgICAgICAgICAgICAiY29udHJhdG8iLAogICAgICAgICAgICAgICAgIm5vX29wZXJhY2lvbiIsCiAgICAgICAgICAgICAgICAiY29udHJhY3RfbnVtYmVyIiwKICAgICAgICAgICAgICAgICJub19jb250cmF0byIsCiAgICAgICAgICAgIF0sCiAgICAgICAgXSwKICAgICkKICAgIHVwbG9hZGVkX2ZpbGUuc2VlaygwKQoKICAgIGRlZiBoYW5kbGVyKHJvdzogcGQuU2VyaWVzLCBlcnJvcnM6IGxpc3Rbc3RyXSk6CiAgICAgICAgZW50aWRhZCA9IF9lbnN1cmVfZW50aWRhZF9mcm9tX3Jvdyhyb3csIGVycm9ycykKICAgICAgICBpZiBub3QgZW50aWRhZDoKICAgICAgICAgICAgcmV0dXJuIE5vbmUKICAgICAgICByZWZlcmVuY2lhID0gcGljaygKICAgICAgICAgICAgcm93LAogICAgICAgICAgICAib3BlcmFjaW9uIiwKICAgICAgICAgICAgInJlZmVyZW5jaWFfb3BlcmFjaW9uIiwKICAgICAgICAgICAgImNvbnRyYXRvIiwKICAgICAgICAgICAgIm5vX29wZXJhY2lvbiIsCiAgICAgICAgICAgICJub19jb250cmF0byIsCiAgICAgICAgICAgICJjb250cmFjdF9udW1iZXIiLAogICAgICAgICkKICAgICAgICBpZiBub3QgcmVmZXJlbmNpYToKICAgICAgICAgICAgZXJyb3JzLmFwcGVuZCgiZmFsdGEgcmVmZXJlbmNpYSBkZSBvcGVyYWNpw7NuIikKICAgICAgICAgICAgcmV0dXJuIE5vbmUKICAgICAgICBmZWNoYV9yYXcgPSBwaWNrKAogICAgICAgICAgICByb3csCiAgICAgICAgICAgICJmZWNoYV9zbmFwc2hvdCIsCiAgICAgICAgICAgICJmZWNoYV9jb3J0ZSIsCiAgICAgICAgICAgICJhbF8zMV9tYXlvIiwKICAgICAgICAgICAgImZlY2hhIiwKICAgICAgICAgICAgImNvcnRlIiwKICAgICAgICAgICAgImJhbGFuY2VfdW50aWwiLAogICAgICAgICAgICAiZmluYWxfdmFsaWRpdHkiLAogICAgICAgICkKICAgICAgICBmZWNoYSA9IF9wYXJzZV9kYXRlKGZlY2hhX3Jhdykgb3IgZGF0ZSgyMDI2LCA2LCAzMCkKICAgICAgICBkaWFzID0gcGlja19pbnQoCiAgICAgICAgICAgIHJvdywKICAgICAgICAgICAgImRpYXNfbW9yYSIsCiAgICAgICAgICAgICJkaWFzX2F0cmFzbyIsCiAgICAgICAgICAgICJkaWFzX2RlX21vcmEiLAogICAgICAgICAgICAibW9yYV9kaWFzIiwKICAgICAgICAgICAgImR1ZWRheXMiLAogICAgICAgICAgICAiZHVlX2RheXMiLAogICAgICAgICkKICAgICAgICBzYWxkbyA9IHBpY2tfZGVjaW1hbCgKICAgICAgICAgICAgcm93LAogICAgICAgICAgICAic2FsZG8iLAogICAgICAgICAgICAic2FsZG9fdG90YWwiLAogICAgICAgICAgICAic2FsZG9fb3BlcmFjaW9uIiwKICAgICAgICAgICAgImNhcGl0YWxfYmFsYW5jZSIsCiAgICAgICAgICAgICJ0b3RhbF9jYXBpdGFsIiwKICAgICAgICApCiAgICAgICAgZXhpZ2libGUgPSBwaWNrX2RlY2ltYWwoCiAgICAgICAgICAgIHJvdywKICAgICAgICAgICAgIm1vbnRvX2V4aWdpYmxlIiwKICAgICAgICAgICAgImV4aWdpYmxlIiwKICAgICAgICAgICAgIm1vbnRvX3ZlbmNpZG8iLAogICAgICAgICAgICAidmVuY2lkbyIsCiAgICAgICAgICAgICJwYXN0X2R1ZV9iYWxhbmNlIiwKICAgICAgICApCiAgICAgICAgaWYgZXhpZ2libGUgPT0gMCBhbmQgc2FsZG8gPiAwIGFuZCBkaWFzID4gMDoKICAgICAgICAgICAgZXhpZ2libGUgPSBzYWxkbwogICAgICAgIG5pdmVsID0gcGljayhyb3csICJuaXZlbF9yaWVzZ28iLCAiY2F0ZWdvcmlhX3JpZXNnbyIpLnVwcGVyKCkgb3IgX25pdmVsX2Zyb21fbW9yYShkaWFzKQogICAgICAgIGlmIG5pdmVsIG5vdCBpbiBkaWN0KFJpc2tPcGVyYXRpb25TbmFwc2hvdC5OSVZFTF9DSE9JQ0VTKToKICAgICAgICAgICAgbml2ZWwgPSBfbml2ZWxfZnJvbV9tb3JhKGRpYXMpCiAgICAgICAgYWxlcnRhX3JhdyA9IHBpY2socm93LCAiYWxlcnRhIiwgImVuX2FsZXJ0YSIsICJzdGF0dXMiKQogICAgICAgIGFsZXJ0YSA9IGRpYXMgPj0gMzAgb3IgYWxlcnRhX3Jhdy5sb3dlcigpIGluICgiMSIsICJzaSIsICJzw60iLCAidHJ1ZSIsICJ5ZXMiLCAidmVuY2lkbyIsICJtb3JhIikKICAgICAgICBwcm9kX3JhdyA9IHBpY2socm93LCAicHJvZHVjdG8iLCAicHJvZHVjdG9fY29kaWdvIikgb3IgIkxFQVNJTkciCiAgICAgICAgcHJvZF9jb2RlID0gX3NsdWdfY29kaWdvKHByb2RfcmF3KVs6NTBdIG9yICJMRUFTSU5HIgogICAgICAgIHByb2R1Y3RvLCBfID0gUHJvZHVjdG8ub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICBjb2RpZ289cHJvZF9jb2RlLAogICAgICAgICAgICBkZWZhdWx0cz17Im5vbWJyZSI6IHByb2RfcmF3WzoyMDBdIG9yICJMZWFzaW5nIiwgImFjdGl2byI6IFRydWV9LAogICAgICAgICkKICAgICAgICBkZXRhbGxlX3BhcnRzID0gWwogICAgICAgICAgICBwaWNrKHJvdywgImRldGFsbGUiLCAib2JzZXJ2YWNpb25lcyIsICJub3RhcyIpLAogICAgICAgICAgICBmIlN0YXR1cz17cGljayhyb3csICdzdGF0dXMnKX0iIGlmIHBpY2socm93LCAic3RhdHVzIikgZWxzZSAiIiwKICAgICAgICAgICAgZiJBZHZpc29yPXtwaWNrKHJvdywgJ2Fkdmlzb3JfbmFtZScpfSIgaWYgcGljayhyb3csICJhZHZpc29yX25hbWUiKSBlbHNlICIiLAogICAgICAgICAgICBmIkN1b3RhcyBwZW5kLj17cGljayhyb3csICdvdXRzdGFuZGluZ19pbnN0YWxsbWVudHMnKX0iCiAgICAgICAgICAgIGlmIHBpY2socm93LCAib3V0c3RhbmRpbmdfaW5zdGFsbG1lbnRzIikKICAgICAgICAgICAgZWxzZSAiIiwKICAgICAgICBdCiAgICAgICAgZGV0YWxsZSA9ICIgfCAiLmpvaW4ocCBmb3IgcCBpbiBkZXRhbGxlX3BhcnRzIGlmIHApCiAgICAgICAgXywgY3JlYXRlZCA9IFJpc2tPcGVyYXRpb25TbmFwc2hvdC5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgIGVudGlkYWQ9ZW50aWRhZCwKICAgICAgICAgICAgcmVmZXJlbmNpYV9vcGVyYWNpb249cmVmZXJlbmNpYSwKICAgICAgICAgICAgZmVjaGFfc25hcHNob3Q9ZmVjaGEsCiAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICJwcm9kdWN0byI6IHByb2R1Y3RvLAogICAgICAgICAgICAgICAgIm5pdmVsX3JpZXNnbyI6IG5pdmVsLAogICAgICAgICAgICAgICAgImRpYXNfbW9yYSI6IGRpYXMsCiAgICAgICAgICAgICAgICAic2FsZG8iOiBzYWxkbywKICAgICAgICAgICAgICAgICJtb250b19leGlnaWJsZSI6IGV4aWdpYmxlLAogICAgICAgICAgICAgICAgImFsZXJ0YSI6IGFsZXJ0YSwKICAgICAgICAgICAgICAgICJkZXRhbGxlIjogZGV0YWxsZSwKICAgICAgICAgICAgfSwKICAgICAgICApCiAgICAgICAgcGVyaW9kbyA9IGZlY2hhLnN0cmZ0aW1lKCIlWS0lbSIpCiAgICAgICAgRXN0YWRvRmluYW5jaWVyby5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgIGVudGlkYWQ9ZW50aWRhZCwKICAgICAgICAgICAgcGVyaW9kbz1wZXJpb2RvLAogICAgICAgICAgICBkZWZhdWx0cz17CiAgICAgICAgICAgICAgICAic2FsZG9fdG90YWwiOiBzYWxkbywKICAgICAgICAgICAgICAgICJtb3JhX2RpYXMiOiBkaWFzLAogICAgICAgICAgICAgICAgImV4cG9zaWNpb24iOiBzYWxkbywKICAgICAgICAgICAgfSwKICAgICAgICApCiAgICAgICAgcmV0dXJuIGNyZWF0ZWQsIG5vdCBjcmVhdGVkCgogICAgdXBsb2FkZWRfZmlsZS5zZWVrKDApCiAgICByZXR1cm4gcnVuX2ltcG9ydF9iYXRjaCgKICAgICAgICB1c2VyPXVzZXIsCiAgICAgICAgbW9kdWxvPURhdGFJbXBvcnRCYXRjaC5NT0RVTE9fUklTSywKICAgICAgICB0aXBvX2ltcG9ydGFjaW9uPSJsZWFzaW5nX2RhdGFiYXNlIiwKICAgICAgICB1cGxvYWRlZF9maWxlPXVwbG9hZGVkX2ZpbGUsCiAgICAgICAgcmVxdWlyZWRfY29sdW1ucz1bXSwKICAgICAgICByb3dfaGFuZGxlcj1oYW5kbGVyLAogICAgKQoKCmRlZiBpbXBvcnRfbGVhc2luZ19yZW50YXModXNlciwgdXBsb2FkZWRfZmlsZSkgLT4gRGF0YUltcG9ydEJhdGNoOgogICAgIiIiCiAgICBFbnJpcXVlY2ltaWVudG8gQmFsw7NuOiBjdW90YXMvcmVudGFzIHBvciBjb250cmF0by4KICAgIEFyY2hpdm86IExlYXNpbmdSZW50YXNZWVlZLU1NLURELmNzdgogICAgTWF0Y2hpbmc6IE5vQ29udHJhdG8g4oaSIEVudGlkYWQgdsOtYSBSaXNrT3BlcmF0aW9uU25hcHNob3QucmVmZXJlbmNpYV9vcGVyYWNpb24KICAgICAgICAgICAgICBvIGNyZWFjacOzbiBkZSBQcm9ncmFtYWNpb25QYWdvIC8gUGFnb1JlYWxpemFkby4KICAgICIiIgogICAgZGYgPSBub3JtYWxpemVfY29sdW1ucyhyZWFkX2RhdGFmcmFtZSh1cGxvYWRlZF9maWxlKSkKICAgIHJlcXVpcmVfYW55KAogICAgICAgIGRmLAogICAgICAgIFsKICAgICAgICAgICAgWyJub19jb250cmF0byIsICJjb250cmF0byIsICJjb250cmFjdF9udW1iZXIiLCAicmVmZXJlbmNpYSJdLAogICAgICAgICAgICBbInZlbmNpbWllbnRvIiwgImZlY2hhX3Byb2dyYW1hZGEiLCAiZmVjaGFfdmVuY2ltaWVudG8iXSwKICAgICAgICBdLAogICAgKQogICAgdXBsb2FkZWRfZmlsZS5zZWVrKDApCgogICAgZGVmIGhhbmRsZXIocm93OiBwZC5TZXJpZXMsIGVycm9yczogbGlzdFtzdHJdKToKICAgICAgICBjb250cmF0byA9IHBpY2socm93LCAibm9fY29udHJhdG8iLCAiY29udHJhdG8iLCAiY29udHJhY3RfbnVtYmVyIiwgInJlZmVyZW5jaWEiLCAib3BlcmFjaW9uIikKICAgICAgICBpZiBub3QgY29udHJhdG86CiAgICAgICAgICAgIGVycm9ycy5hcHBlbmQoImZhbHRhIE5vQ29udHJhdG8iKQogICAgICAgICAgICByZXR1cm4gTm9uZQogICAgICAgIHNuYXAgPSAoCiAgICAgICAgICAgIFJpc2tPcGVyYXRpb25TbmFwc2hvdC5vYmplY3RzLmZpbHRlcihyZWZlcmVuY2lhX29wZXJhY2lvbl9faWV4YWN0PWNvbnRyYXRvKQogICAgICAgICAgICAuc2VsZWN0X3JlbGF0ZWQoImVudGlkYWQiKQogICAgICAgICAgICAub3JkZXJfYnkoIi1mZWNoYV9zbmFwc2hvdCIpCiAgICAgICAgICAgIC5maXJzdCgpCiAgICAgICAgKQogICAgICAgIGlmIHNuYXA6CiAgICAgICAgICAgIGVudGlkYWQgPSBzbmFwLmVudGlkYWQKICAgICAgICBlbHNlOgogICAgICAgICAgICAjIENyZWFyIGVudGlkYWQgbcOtbmltYSBzaSBlbCBjb250cmF0byBhw7puIG5vIGVzdMOhIGVuIHNuYXBzaG90cwogICAgICAgICAgICBlbnRpZGFkLCBfID0gRW50aWRhZC5vYmplY3RzLmdldF9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICBjb2RpZ289X3NsdWdfY29kaWdvKGNvbnRyYXRvKSwKICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICAgICAibm9tYnJlIjogZiJDb250cmF0byB7Y29udHJhdG99IiwKICAgICAgICAgICAgICAgICAgICAidW5pZGFkX25lZ29jaW8iOiBVbmlkYWROZWdvY2lvLm9iamVjdHMuZmlsdGVyKGNvZGU9IkxFQVNJTkciKS5maXJzdCgpLAogICAgICAgICAgICAgICAgICAgICJhY3RpdmEiOiBUcnVlLAogICAgICAgICAgICAgICAgICAgICJ0aXBvIjogRW50aWRhZC5USVBPX0NMSUVOVEUsCiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICApCiAgICAgICAgbnJvID0gcGljayhyb3csICJubyIsICJudW1lcm8iLCAiY3VvdGEiLCAibnJvIikgb3IgIjAiCiAgICAgICAgcmVmZXJlbmNpYSA9IGYie2NvbnRyYXRvfS1De25yb30iCiAgICAgICAgZmVjaGEgPSBfcGFyc2VfZGF0ZShwaWNrKHJvdywgInZlbmNpbWllbnRvIiwgImZlY2hhX3Byb2dyYW1hZGEiLCAiZmVjaGFfdmVuY2ltaWVudG8iKSkKICAgICAgICBpZiBub3QgZmVjaGE6CiAgICAgICAgICAgIGVycm9ycy5hcHBlbmQoImZhbHRhIGZlY2hhIHZlbmNpbWllbnRvIikKICAgICAgICAgICAgcmV0dXJuIE5vbmUKICAgICAgICBtb250byA9IHBpY2tfZGVjaW1hbChyb3csICJyZW50YV90b3RhbCIsICJ2YWxvcl9yZW50YV9jb25fbW9yYSIsICJ2YWxvcl9yZW50YSIsICJtb250byIpCiAgICAgICAgZXN0YWRvID0gcGljayhyb3csICJlc3RhZG8iLCAic3RhdHVzIikubG93ZXIoKQogICAgICAgIF8sIGNyZWF0ZWRfcHJvZyA9IFByb2dyYW1hY2lvblBhZ28ub2JqZWN0cy51cGRhdGVfb3JfY3JlYXRlKAogICAgICAgICAgICBlbnRpZGFkPWVudGlkYWQsCiAgICAgICAgICAgIHJlZmVyZW5jaWE9cmVmZXJlbmNpYSwKICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgImZlY2hhX3Byb2dyYW1hZGEiOiBmZWNoYSwKICAgICAgICAgICAgICAgICJtb250byI6IG1vbnRvLAogICAgICAgICAgICAgICAgIm1vbmVkYSI6ICJHVFEiLAogICAgICAgICAgICB9LAogICAgICAgICkKICAgICAgICBjcmVhdGVkID0gY3JlYXRlZF9wcm9nCiAgICAgICAgdXBkYXRlZCA9IG5vdCBjcmVhdGVkX3Byb2cKICAgICAgICBmZWNoYV9wYWdvID0gX3BhcnNlX2RhdGUocGljayhyb3csICJmZWNoYV9wYWdvIikpCiAgICAgICAgaWYgZmVjaGFfcGFnbyBvciBlc3RhZG8gaW4gKCJwYWdhZGEiLCAicGFnYWRvIiwgInBhaWQiKToKICAgICAgICAgICAgXywgY3JlYXRlZF9wYWdvID0gUGFnb1JlYWxpemFkby5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICBlbnRpZGFkPWVudGlkYWQsCiAgICAgICAgICAgICAgICByZWZlcmVuY2lhPXJlZmVyZW5jaWEsCiAgICAgICAgICAgICAgICBkZWZhdWx0cz17CiAgICAgICAgICAgICAgICAgICAgImZlY2hhX3BhZ28iOiBmZWNoYV9wYWdvIG9yIGZlY2hhLAogICAgICAgICAgICAgICAgICAgICJtb250byI6IG1vbnRvLAogICAgICAgICAgICAgICAgICAgICJtb25lZGEiOiAiR1RRIiwKICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICkKICAgICAgICAgICAgY3JlYXRlZCA9IGNyZWF0ZWQgb3IgY3JlYXRlZF9wYWdvCiAgICAgICAgICAgIHVwZGF0ZWQgPSB1cGRhdGVkIG9yIChub3QgY3JlYXRlZF9wYWdvKQogICAgICAgIHJldHVybiBjcmVhdGVkLCB1cGRhdGVkIGFuZCBub3QgY3JlYXRlZAoKICAgIHJldHVybiBydW5faW1wb3J0X2JhdGNoKAogICAgICAgIHVzZXI9dXNlciwKICAgICAgICBtb2R1bG89RGF0YUltcG9ydEJhdGNoLk1PRFVMT19SSVNLLAogICAgICAgIHRpcG9faW1wb3J0YWNpb249ImxlYXNpbmdfcmVudGFzIiwKICAgICAgICB1cGxvYWRlZF9maWxlPXVwbG9hZGVkX2ZpbGUsCiAgICAgICAgcmVxdWlyZWRfY29sdW1ucz1bXSwKICAgICAgICByb3dfaGFuZGxlcj1oYW5kbGVyLAogICAgKQoKCmRlZiBpbXBvcnRfZXN0YWRvc19maW5hbmNpZXJvcyh1c2VyLCB1cGxvYWRlZF9maWxlKSAtPiBEYXRhSW1wb3J0QmF0Y2g6CiAgICBkZiA9IG5vcm1hbGl6ZV9jb2x1bW5zKHJlYWRfZGF0YWZyYW1lKHVwbG9hZGVkX2ZpbGUpKQogICAgcmVxdWlyZV9hbnkoZGYsIFtbImVudGlkYWRfY29kaWdvIiwgIm5pdCIsICJjbGllbnRlIl0sIFsicGVyaW9kbyJdXSkKCiAgICBkZWYgaGFuZGxlcihyb3c6IHBkLlNlcmllcywgZXJyb3JzOiBsaXN0W3N0cl0pOgogICAgICAgIGVudGlkYWQgPSBfZW5zdXJlX2VudGlkYWRfZnJvbV9yb3cocm93LCBlcnJvcnMpCiAgICAgICAgaWYgbm90IGVudGlkYWQ6CiAgICAgICAgICAgIHJldHVybiBOb25lCiAgICAgICAgcGVyaW9kbyA9IHBpY2socm93LCAicGVyaW9kbyIsICJhbmlvX21lcyIsICJtZXMiKQogICAgICAgIGlmIG5vdCBwZXJpb2RvOgogICAgICAgICAgICBlcnJvcnMuYXBwZW5kKCJwZXJpb2RvIG9ibGlnYXRvcmlvIikKICAgICAgICAgICAgcmV0dXJuIE5vbmUKICAgICAgICBwZXJpb2RvID0gcGVyaW9kby5yZXBsYWNlKCIvIiwgIi0iKVs6N10KICAgICAgICBfLCBjcmVhdGVkID0gRXN0YWRvRmluYW5jaWVyby5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgIGVudGlkYWQ9ZW50aWRhZCwKICAgICAgICAgICAgcGVyaW9kbz1wZXJpb2RvLAogICAgICAgICAgICBkZWZhdWx0cz17CiAgICAgICAgICAgICAgICAic2FsZG9fdG90YWwiOiBwaWNrX2RlY2ltYWwocm93LCAic2FsZG9fdG90YWwiLCAic2FsZG8iKSwKICAgICAgICAgICAgICAgICJtb3JhX2RpYXMiOiBwaWNrX2ludChyb3csICJtb3JhX2RpYXMiLCAiZGlhc19tb3JhIiksCiAgICAgICAgICAgICAgICAiZXhwb3NpY2lvbiI6IHBpY2tfZGVjaW1hbChyb3csICJleHBvc2ljaW9uIiksCiAgICAgICAgICAgICAgICAibm90YXMiOiBwaWNrKHJvdywgIm5vdGFzIiksCiAgICAgICAgICAgIH0sCiAgICAgICAgKQogICAgICAgIHJldHVybiBjcmVhdGVkLCBub3QgY3JlYXRlZAoKICAgIHVwbG9hZGVkX2ZpbGUuc2VlaygwKQogICAgcmV0dXJuIHJ1bl9pbXBvcnRfYmF0Y2goCiAgICAgICAgdXNlcj11c2VyLAogICAgICAgIG1vZHVsbz1EYXRhSW1wb3J0QmF0Y2guTU9EVUxPX1JJU0ssCiAgICAgICAgdGlwb19pbXBvcnRhY2lvbj0iZXN0YWRvc19maW5hbmNpZXJvcyIsCiAgICAgICAgdXBsb2FkZWRfZmlsZT11cGxvYWRlZF9maWxlLAogICAgICAgIHJlcXVpcmVkX2NvbHVtbnM9W10sCiAgICAgICAgcm93X2hhbmRsZXI9aGFuZGxlciwKICAgICkKCgpkZWYgaW1wb3J0X3Byb2dyYW1hY2lvbl9wYWdvcyh1c2VyLCB1cGxvYWRlZF9maWxlKSAtPiBEYXRhSW1wb3J0QmF0Y2g6CiAgICBkZiA9IG5vcm1hbGl6ZV9jb2x1bW5zKHJlYWRfZGF0YWZyYW1lKHVwbG9hZGVkX2ZpbGUpKQogICAgcmVxdWlyZV9hbnkoZGYsIFtbInJlZmVyZW5jaWEiLCAib3BlcmFjaW9uIl0sIFsiZmVjaGFfcHJvZ3JhbWFkYSIsICJmZWNoYV9wYWdvX3Byb2dyYW1hZGEiXSwgWyJtb250byJdXSkKCiAgICBkZWYgaGFuZGxlcihyb3c6IHBkLlNlcmllcywgZXJyb3JzOiBsaXN0W3N0cl0pOgogICAgICAgIGVudGlkYWQgPSBfZW5zdXJlX2VudGlkYWRfZnJvbV9yb3cocm93LCBlcnJvcnMpCiAgICAgICAgaWYgbm90IGVudGlkYWQ6CiAgICAgICAgICAgIHJldHVybiBOb25lCiAgICAgICAgcmVmZXJlbmNpYSA9IHBpY2socm93LCAicmVmZXJlbmNpYSIsICJvcGVyYWNpb24iLCAiY3VvdGEiKQogICAgICAgIGZlY2hhID0gX3BhcnNlX2RhdGUocGljayhyb3csICJmZWNoYV9wcm9ncmFtYWRhIiwgImZlY2hhX3ZlbmNpbWllbnRvIikpCiAgICAgICAgaWYgbm90IHJlZmVyZW5jaWEgb3Igbm90IGZlY2hhOgogICAgICAgICAgICBlcnJvcnMuYXBwZW5kKCJyZWZlcmVuY2lhIHkgZmVjaGFfcHJvZ3JhbWFkYSBvYmxpZ2F0b3JpYXMiKQogICAgICAgICAgICByZXR1cm4gTm9uZQogICAgICAgIF8sIGNyZWF0ZWQgPSBQcm9ncmFtYWNpb25QYWdvLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgZW50aWRhZD1lbnRpZGFkLAogICAgICAgICAgICByZWZlcmVuY2lhPXJlZmVyZW5jaWEsCiAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICJmZWNoYV9wcm9ncmFtYWRhIjogZmVjaGEsCiAgICAgICAgICAgICAgICAibW9udG8iOiBwaWNrX2RlY2ltYWwocm93LCAibW9udG8iKSwKICAgICAgICAgICAgICAgICJtb25lZGEiOiBwaWNrKHJvdywgIm1vbmVkYSIpIG9yICJHVFEiLAogICAgICAgICAgICB9LAogICAgICAgICkKICAgICAgICByZXR1cm4gY3JlYXRlZCwgbm90IGNyZWF0ZWQKCiAgICB1cGxvYWRlZF9maWxlLnNlZWsoMCkKICAgIHJldHVybiBydW5faW1wb3J0X2JhdGNoKAogICAgICAgIHVzZXI9dXNlciwKICAgICAgICBtb2R1bG89RGF0YUltcG9ydEJhdGNoLk1PRFVMT19SSVNLLAogICAgICAgIHRpcG9faW1wb3J0YWNpb249InByb2dyYW1hY2lvbl9wYWdvcyIsCiAgICAgICAgdXBsb2FkZWRfZmlsZT11cGxvYWRlZF9maWxlLAogICAgICAgIHJlcXVpcmVkX2NvbHVtbnM9W10sCiAgICAgICAgcm93X2hhbmRsZXI9aGFuZGxlciwKICAgICkKCgpkZWYgaW1wb3J0X3BhZ29zX3JlYWxpemFkb3ModXNlciwgdXBsb2FkZWRfZmlsZSkgLT4gRGF0YUltcG9ydEJhdGNoOgogICAgZGYgPSBub3JtYWxpemVfY29sdW1ucyhyZWFkX2RhdGFmcmFtZSh1cGxvYWRlZF9maWxlKSkKICAgIHJlcXVpcmVfYW55KGRmLCBbWyJyZWZlcmVuY2lhIiwgIm9wZXJhY2lvbiJdLCBbImZlY2hhX3BhZ28iXSwgWyJtb250byJdXSkKCiAgICBkZWYgaGFuZGxlcihyb3c6IHBkLlNlcmllcywgZXJyb3JzOiBsaXN0W3N0cl0pOgogICAgICAgIGVudGlkYWQgPSBfZW5zdXJlX2VudGlkYWRfZnJvbV9yb3cocm93LCBlcnJvcnMpCiAgICAgICAgaWYgbm90IGVudGlkYWQ6CiAgICAgICAgICAgIHJldHVybiBOb25lCiAgICAgICAgcmVmZXJlbmNpYSA9IHBpY2socm93LCAicmVmZXJlbmNpYSIsICJvcGVyYWNpb24iLCAiY3VvdGEiKQogICAgICAgIGZlY2hhID0gX3BhcnNlX2RhdGUocGljayhyb3csICJmZWNoYV9wYWdvIikpCiAgICAgICAgaWYgbm90IHJlZmVyZW5jaWEgb3Igbm90IGZlY2hhOgogICAgICAgICAgICBlcnJvcnMuYXBwZW5kKCJyZWZlcmVuY2lhIHkgZmVjaGFfcGFnbyBvYmxpZ2F0b3JpYXMiKQogICAgICAgICAgICByZXR1cm4gTm9uZQogICAgICAgIF8sIGNyZWF0ZWQgPSBQYWdvUmVhbGl6YWRvLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgZW50aWRhZD1lbnRpZGFkLAogICAgICAgICAgICByZWZlcmVuY2lhPXJlZmVyZW5jaWEsCiAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICJmZWNoYV9wYWdvIjogZmVjaGEsCiAgICAgICAgICAgICAgICAibW9udG8iOiBwaWNrX2RlY2ltYWwocm93LCAibW9udG8iKSwKICAgICAgICAgICAgICAgICJtb25lZGEiOiBwaWNrKHJvdywgIm1vbmVkYSIpIG9yICJHVFEiLAogICAgICAgICAgICB9LAogICAgICAgICkKICAgICAgICByZXR1cm4gY3JlYXRlZCwgbm90IGNyZWF0ZWQKCiAgICB1cGxvYWRlZF9maWxlLnNlZWsoMCkKICAgIHJldHVybiBydW5faW1wb3J0X2JhdGNoKAogICAgICAgIHVzZXI9dXNlciwKICAgICAgICBtb2R1bG89RGF0YUltcG9ydEJhdGNoLk1PRFVMT19SSVNLLAogICAgICAgIHRpcG9faW1wb3J0YWNpb249InBhZ29zX3JlYWxpemFkb3MiLAogICAgICAgIHVwbG9hZGVkX2ZpbGU9dXBsb2FkZWRfZmlsZSwKICAgICAgICByZXF1aXJlZF9jb2x1bW5zPVtdLAogICAgICAgIHJvd19oYW5kbGVyPWhhbmRsZXIsCiAgICApCgoKZGVmIGltcG9ydF9zbmFwc2hvdHModXNlciwgdXBsb2FkZWRfZmlsZSkgLT4gRGF0YUltcG9ydEJhdGNoOgogICAgIiIiQ1NWIGdlbsOpcmljbyBkZSBzbmFwc2hvdHMg4oCUIG1pc21vIG1hcGVvIHF1ZSBsZWFzaW5nIGVuIGZvcm1hdG8gcGxhbm8uIiIiCiAgICByZXR1cm4gaW1wb3J0X2xlYXNpbmdfZGF0YWJhc2UodXNlciwgdXBsb2FkZWRfZmlsZSkK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=risk/tests.py
PATH_JSON="risk/tests.py"
FILENAME=tests.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=3
SIZE_BYTES_UTF8=60
CONTENT_SHA256=9ab6c6191360e63c1b4c9b5659aef348a743c9e078be68190917369e4e9563e8
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.test import TestCase

# Create your tests here.

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.test import TestCase
00002|
00003|# Create your tests here.

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udGVzdCBpbXBvcnQgVGVzdENhc2UKCiMgQ3JlYXRlIHlvdXIgdGVzdHMgaGVyZS4K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=risk/urls.py
PATH_JSON="risk/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=14
SIZE_BYTES_UTF8=546
CONTENT_SHA256=c4205ec248f398c41a12482f68c6e889c7305ce634a66b0df7ecc4878787dce5
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.urls import path

from . import views

app_name = "risk"

urlpatterns = [
    path("", views.comando_balon, name="comando_balon"),
    path("clientes/", views.ClienteListView.as_view(), name="cliente_list"),
    path("cliente/<str:codigo>/", views.ClienteDetailView.as_view(), name="cliente_detail"),
    path("operacion/<int:pk>/", views.OperacionDetailView.as_view(), name="operacion_detail"),
    path("exportar/", views.export_comando_balon, name="export_comando_balon"),
    path("importar/", views.importar, name="importar"),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.urls import path
00002|
00003|from . import views
00004|
00005|app_name = "risk"
00006|
00007|urlpatterns = [
00008|    path("", views.comando_balon, name="comando_balon"),
00009|    path("clientes/", views.ClienteListView.as_view(), name="cliente_list"),
00010|    path("cliente/<str:codigo>/", views.ClienteDetailView.as_view(), name="cliente_detail"),
00011|    path("operacion/<int:pk>/", views.OperacionDetailView.as_view(), name="operacion_detail"),
00012|    path("exportar/", views.export_comando_balon, name="export_comando_balon"),
00013|    path("importar/", views.importar, name="importar"),
00014|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aAoKZnJvbSAuIGltcG9ydCB2aWV3cwoKYXBwX25hbWUgPSAicmlzayIKCnVybHBhdHRlcm5zID0gWwogICAgcGF0aCgiIiwgdmlld3MuY29tYW5kb19iYWxvbiwgbmFtZT0iY29tYW5kb19iYWxvbiIpLAogICAgcGF0aCgiY2xpZW50ZXMvIiwgdmlld3MuQ2xpZW50ZUxpc3RWaWV3LmFzX3ZpZXcoKSwgbmFtZT0iY2xpZW50ZV9saXN0IiksCiAgICBwYXRoKCJjbGllbnRlLzxzdHI6Y29kaWdvPi8iLCB2aWV3cy5DbGllbnRlRGV0YWlsVmlldy5hc192aWV3KCksIG5hbWU9ImNsaWVudGVfZGV0YWlsIiksCiAgICBwYXRoKCJvcGVyYWNpb24vPGludDpwaz4vIiwgdmlld3MuT3BlcmFjaW9uRGV0YWlsVmlldy5hc192aWV3KCksIG5hbWU9Im9wZXJhY2lvbl9kZXRhaWwiKSwKICAgIHBhdGgoImV4cG9ydGFyLyIsIHZpZXdzLmV4cG9ydF9jb21hbmRvX2JhbG9uLCBuYW1lPSJleHBvcnRfY29tYW5kb19iYWxvbiIpLAogICAgcGF0aCgiaW1wb3J0YXIvIiwgdmlld3MuaW1wb3J0YXIsIG5hbWU9ImltcG9ydGFyIiksCl0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=risk/views.py
PATH_JSON="risk/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=157
SIZE_BYTES_UTF8=5214
CONTENT_SHA256=dc2a95087b47401b8ae889a06d746f050db48b088215f31b15e69c3397a97f57
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView

from core.wcg_models import Entidad

from .models import ProgramacionPago, RiskOperationSnapshot
from .selectors import latest_snapshots_queryset, snapshot_summary


@login_required
def comando_balon(request):
    qs = latest_snapshots_queryset(request)
    summary = snapshot_summary(qs)
    operaciones = list(qs[:100])
    alertas = [s for s in operaciones if s.alerta]
    mora_alta = sorted(
        [s for s in operaciones if s.dias_mora >= 30],
        key=lambda s: s.dias_mora,
        reverse=True,
    )[:50]
    pagos_vencidos = (
        ProgramacionPago.objects.filter(fecha_programada__lt=timezone.now().date())
        .select_related("entidad")
        .order_by("fecha_programada")[:40]
    )
    return render(
        request,
        "risk/riskcommandobalon.html",
        {
            "operaciones": operaciones,
            "snapshots": operaciones,
            "summary": summary,
            "alertas": alertas,
            "mora_alta": mora_alta,
            "pagos_vencidos": pagos_vencidos,
            "niveles": RiskOperationSnapshot.NIVEL_CHOICES,
            "breadcrumbs": [
                {"label": "Panel principal", "url": "/panel/"},
                {"label": "Riesgo — Comando Balón"},
            ],
        },
    )


class ClienteListView(LoginRequiredMixin, ListView):
    model = Entidad
    template_name = "risk/riskclientlist.html"
    context_object_name = "clientes"
    paginate_by = 50

    def get_queryset(self):
        ids = (
            RiskOperationSnapshot.objects.values_list("entidad_id", flat=True).distinct()
        )
        return Entidad.objects.filter(id__in=ids).order_by("nombre")


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Entidad
    template_name = "risk/riskclientdetail.html"
    context_object_name = "entidad"
    slug_field = "codigo"
    slug_url_kwarg = "codigo"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        entidad = self.object
        ctx["estados"] = entidad.estados_financieros.order_by("-periodo")[:12]
        ctx["programaciones"] = entidad.programaciones_pago.order_by("-fecha_programada")[:20]
        ctx["pagos"] = entidad.pagos_realizados.order_by("-fecha_pago")[:20]
        ctx["snapshots"] = entidad.risk_snapshots.select_related("producto").order_by(
            "-fecha_snapshot"
        )[:20]
        ctx["contactos_cobranza"] = entidad.contactos_cobranza.filter(activo=True)
        return ctx


class OperacionDetailView(LoginRequiredMixin, DetailView):
    model = RiskOperationSnapshot
    template_name = "risk/riskoperationdetail.html"
    context_object_name = "snapshot"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        snap = self.object
        ref = snap.referencia_operacion
        ctx["historial"] = RiskOperationSnapshot.objects.filter(
            entidad=snap.entidad,
            referencia_operacion=ref,
        ).order_by("-fecha_snapshot")
        # Rentas/cuotas del contrato: referencia empieza con el código de operación
        ctx["pagos_programados"] = ProgramacionPago.objects.filter(
            entidad=snap.entidad,
            referencia__startswith=ref,
        ).order_by("-fecha_programada")[:30]
        from risk.models import PagoRealizado

        ctx["pagos_realizados"] = PagoRealizado.objects.filter(
            entidad=snap.entidad,
            referencia__startswith=ref,
        ).order_by("-fecha_pago")[:30]
        ctx["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "Balón de Riesgo", "url": "/risk/"},
            {"label": "Clientes", "url": "/risk/clientes/"},
            {"label": snap.entidad.nombre, "url": f"/risk/cliente/{snap.entidad.codigo}/"},
            {"label": ref},
        ]
        return ctx


@login_required
def importar(request):
    return redirect("imports:import_hub")


@login_required
def export_comando_balon(request):
    import csv

    qs = latest_snapshots_queryset(request)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="comando_balon.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [
            "fecha",
            "cliente",
            "operacion",
            "producto",
            "saldo",
            "exigible",
            "dias_mora",
            "nivel",
            "alerta",
        ]
    )
    for s in qs:
        writer.writerow(
            [
                s.fecha_snapshot,
                s.entidad.nombre,
                s.referencia_operacion,
                s.producto.nombre if s.producto else "",
                s.saldo,
                s.monto_exigible,
                s.dias_mora,
                s.nivel_riesgo,
                "1" if s.alerta else "0",
            ]
        )
    return response

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib.auth.decorators import login_required
00002|from django.contrib.auth.mixins import LoginRequiredMixin
00003|from django.http import HttpResponse
00004|from django.shortcuts import redirect, render
00005|from django.utils import timezone
00006|from django.views.generic import DetailView, ListView
00007|
00008|from core.wcg_models import Entidad
00009|
00010|from .models import ProgramacionPago, RiskOperationSnapshot
00011|from .selectors import latest_snapshots_queryset, snapshot_summary
00012|
00013|
00014|@login_required
00015|def comando_balon(request):
00016|    qs = latest_snapshots_queryset(request)
00017|    summary = snapshot_summary(qs)
00018|    operaciones = list(qs[:100])
00019|    alertas = [s for s in operaciones if s.alerta]
00020|    mora_alta = sorted(
00021|        [s for s in operaciones if s.dias_mora >= 30],
00022|        key=lambda s: s.dias_mora,
00023|        reverse=True,
00024|    )[:50]
00025|    pagos_vencidos = (
00026|        ProgramacionPago.objects.filter(fecha_programada__lt=timezone.now().date())
00027|        .select_related("entidad")
00028|        .order_by("fecha_programada")[:40]
00029|    )
00030|    return render(
00031|        request,
00032|        "risk/riskcommandobalon.html",
00033|        {
00034|            "operaciones": operaciones,
00035|            "snapshots": operaciones,
00036|            "summary": summary,
00037|            "alertas": alertas,
00038|            "mora_alta": mora_alta,
00039|            "pagos_vencidos": pagos_vencidos,
00040|            "niveles": RiskOperationSnapshot.NIVEL_CHOICES,
00041|            "breadcrumbs": [
00042|                {"label": "Panel principal", "url": "/panel/"},
00043|                {"label": "Riesgo — Comando Balón"},
00044|            ],
00045|        },
00046|    )
00047|
00048|
00049|class ClienteListView(LoginRequiredMixin, ListView):
00050|    model = Entidad
00051|    template_name = "risk/riskclientlist.html"
00052|    context_object_name = "clientes"
00053|    paginate_by = 50
00054|
00055|    def get_queryset(self):
00056|        ids = (
00057|            RiskOperationSnapshot.objects.values_list("entidad_id", flat=True).distinct()
00058|        )
00059|        return Entidad.objects.filter(id__in=ids).order_by("nombre")
00060|
00061|
00062|class ClienteDetailView(LoginRequiredMixin, DetailView):
00063|    model = Entidad
00064|    template_name = "risk/riskclientdetail.html"
00065|    context_object_name = "entidad"
00066|    slug_field = "codigo"
00067|    slug_url_kwarg = "codigo"
00068|
00069|    def get_context_data(self, **kwargs):
00070|        ctx = super().get_context_data(**kwargs)
00071|        entidad = self.object
00072|        ctx["estados"] = entidad.estados_financieros.order_by("-periodo")[:12]
00073|        ctx["programaciones"] = entidad.programaciones_pago.order_by("-fecha_programada")[:20]
00074|        ctx["pagos"] = entidad.pagos_realizados.order_by("-fecha_pago")[:20]
00075|        ctx["snapshots"] = entidad.risk_snapshots.select_related("producto").order_by(
00076|            "-fecha_snapshot"
00077|        )[:20]
00078|        ctx["contactos_cobranza"] = entidad.contactos_cobranza.filter(activo=True)
00079|        return ctx
00080|
00081|
00082|class OperacionDetailView(LoginRequiredMixin, DetailView):
00083|    model = RiskOperationSnapshot
00084|    template_name = "risk/riskoperationdetail.html"
00085|    context_object_name = "snapshot"
00086|    pk_url_kwarg = "pk"
00087|
00088|    def get_context_data(self, **kwargs):
00089|        ctx = super().get_context_data(**kwargs)
00090|        snap = self.object
00091|        ref = snap.referencia_operacion
00092|        ctx["historial"] = RiskOperationSnapshot.objects.filter(
00093|            entidad=snap.entidad,
00094|            referencia_operacion=ref,
00095|        ).order_by("-fecha_snapshot")
00096|        # Rentas/cuotas del contrato: referencia empieza con el código de operación
00097|        ctx["pagos_programados"] = ProgramacionPago.objects.filter(
00098|            entidad=snap.entidad,
00099|            referencia__startswith=ref,
00100|        ).order_by("-fecha_programada")[:30]
00101|        from risk.models import PagoRealizado
00102|
00103|        ctx["pagos_realizados"] = PagoRealizado.objects.filter(
00104|            entidad=snap.entidad,
00105|            referencia__startswith=ref,
00106|        ).order_by("-fecha_pago")[:30]
00107|        ctx["breadcrumbs"] = [
00108|            {"label": "Panel principal", "url": "/panel/"},
00109|            {"label": "Balón de Riesgo", "url": "/risk/"},
00110|            {"label": "Clientes", "url": "/risk/clientes/"},
00111|            {"label": snap.entidad.nombre, "url": f"/risk/cliente/{snap.entidad.codigo}/"},
00112|            {"label": ref},
00113|        ]
00114|        return ctx
00115|
00116|
00117|@login_required
00118|def importar(request):
00119|    return redirect("imports:import_hub")
00120|
00121|
00122|@login_required
00123|def export_comando_balon(request):
00124|    import csv
00125|
00126|    qs = latest_snapshots_queryset(request)
00127|    response = HttpResponse(content_type="text/csv")
00128|    response["Content-Disposition"] = 'attachment; filename="comando_balon.csv"'
00129|    writer = csv.writer(response)
00130|    writer.writerow(
00131|        [
00132|            "fecha",
00133|            "cliente",
00134|            "operacion",
00135|            "producto",
00136|            "saldo",
00137|            "exigible",
00138|            "dias_mora",
00139|            "nivel",
00140|            "alerta",
00141|        ]
00142|    )
00143|    for s in qs:
00144|        writer.writerow(
00145|            [
00146|                s.fecha_snapshot,
00147|                s.entidad.nombre,
00148|                s.referencia_operacion,
00149|                s.producto.nombre if s.producto else "",
00150|                s.saldo,
00151|                s.monto_exigible,
00152|                s.dias_mora,
00153|                s.nivel_riesgo,
00154|                "1" if s.alerta else "0",
00155|            ]
00156|        )
00157|    return response

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYi5hdXRoLmRlY29yYXRvcnMgaW1wb3J0IGxvZ2luX3JlcXVpcmVkCmZyb20gZGphbmdvLmNvbnRyaWIuYXV0aC5taXhpbnMgaW1wb3J0IExvZ2luUmVxdWlyZWRNaXhpbgpmcm9tIGRqYW5nby5odHRwIGltcG9ydCBIdHRwUmVzcG9uc2UKZnJvbSBkamFuZ28uc2hvcnRjdXRzIGltcG9ydCByZWRpcmVjdCwgcmVuZGVyCmZyb20gZGphbmdvLnV0aWxzIGltcG9ydCB0aW1lem9uZQpmcm9tIGRqYW5nby52aWV3cy5nZW5lcmljIGltcG9ydCBEZXRhaWxWaWV3LCBMaXN0VmlldwoKZnJvbSBjb3JlLndjZ19tb2RlbHMgaW1wb3J0IEVudGlkYWQKCmZyb20gLm1vZGVscyBpbXBvcnQgUHJvZ3JhbWFjaW9uUGFnbywgUmlza09wZXJhdGlvblNuYXBzaG90CmZyb20gLnNlbGVjdG9ycyBpbXBvcnQgbGF0ZXN0X3NuYXBzaG90c19xdWVyeXNldCwgc25hcHNob3Rfc3VtbWFyeQoKCkBsb2dpbl9yZXF1aXJlZApkZWYgY29tYW5kb19iYWxvbihyZXF1ZXN0KToKICAgIHFzID0gbGF0ZXN0X3NuYXBzaG90c19xdWVyeXNldChyZXF1ZXN0KQogICAgc3VtbWFyeSA9IHNuYXBzaG90X3N1bW1hcnkocXMpCiAgICBvcGVyYWNpb25lcyA9IGxpc3QocXNbOjEwMF0pCiAgICBhbGVydGFzID0gW3MgZm9yIHMgaW4gb3BlcmFjaW9uZXMgaWYgcy5hbGVydGFdCiAgICBtb3JhX2FsdGEgPSBzb3J0ZWQoCiAgICAgICAgW3MgZm9yIHMgaW4gb3BlcmFjaW9uZXMgaWYgcy5kaWFzX21vcmEgPj0gMzBdLAogICAgICAgIGtleT1sYW1iZGEgczogcy5kaWFzX21vcmEsCiAgICAgICAgcmV2ZXJzZT1UcnVlLAogICAgKVs6NTBdCiAgICBwYWdvc192ZW5jaWRvcyA9ICgKICAgICAgICBQcm9ncmFtYWNpb25QYWdvLm9iamVjdHMuZmlsdGVyKGZlY2hhX3Byb2dyYW1hZGFfX2x0PXRpbWV6b25lLm5vdygpLmRhdGUoKSkKICAgICAgICAuc2VsZWN0X3JlbGF0ZWQoImVudGlkYWQiKQogICAgICAgIC5vcmRlcl9ieSgiZmVjaGFfcHJvZ3JhbWFkYSIpWzo0MF0KICAgICkKICAgIHJldHVybiByZW5kZXIoCiAgICAgICAgcmVxdWVzdCwKICAgICAgICAicmlzay9yaXNrY29tbWFuZG9iYWxvbi5odG1sIiwKICAgICAgICB7CiAgICAgICAgICAgICJvcGVyYWNpb25lcyI6IG9wZXJhY2lvbmVzLAogICAgICAgICAgICAic25hcHNob3RzIjogb3BlcmFjaW9uZXMsCiAgICAgICAgICAgICJzdW1tYXJ5Ijogc3VtbWFyeSwKICAgICAgICAgICAgImFsZXJ0YXMiOiBhbGVydGFzLAogICAgICAgICAgICAibW9yYV9hbHRhIjogbW9yYV9hbHRhLAogICAgICAgICAgICAicGFnb3NfdmVuY2lkb3MiOiBwYWdvc192ZW5jaWRvcywKICAgICAgICAgICAgIm5pdmVsZXMiOiBSaXNrT3BlcmF0aW9uU25hcHNob3QuTklWRUxfQ0hPSUNFUywKICAgICAgICAgICAgImJyZWFkY3J1bWJzIjogWwogICAgICAgICAgICAgICAgeyJsYWJlbCI6ICJQYW5lbCBwcmluY2lwYWwiLCAidXJsIjogIi9wYW5lbC8ifSwKICAgICAgICAgICAgICAgIHsibGFiZWwiOiAiUmllc2dvIOKAlCBDb21hbmRvIEJhbMOzbiJ9LAogICAgICAgICAgICBdLAogICAgICAgIH0sCiAgICApCgoKY2xhc3MgQ2xpZW50ZUxpc3RWaWV3KExvZ2luUmVxdWlyZWRNaXhpbiwgTGlzdFZpZXcpOgogICAgbW9kZWwgPSBFbnRpZGFkCiAgICB0ZW1wbGF0ZV9uYW1lID0gInJpc2svcmlza2NsaWVudGxpc3QuaHRtbCIKICAgIGNvbnRleHRfb2JqZWN0X25hbWUgPSAiY2xpZW50ZXMiCiAgICBwYWdpbmF0ZV9ieSA9IDUwCgogICAgZGVmIGdldF9xdWVyeXNldChzZWxmKToKICAgICAgICBpZHMgPSAoCiAgICAgICAgICAgIFJpc2tPcGVyYXRpb25TbmFwc2hvdC5vYmplY3RzLnZhbHVlc19saXN0KCJlbnRpZGFkX2lkIiwgZmxhdD1UcnVlKS5kaXN0aW5jdCgpCiAgICAgICAgKQogICAgICAgIHJldHVybiBFbnRpZGFkLm9iamVjdHMuZmlsdGVyKGlkX19pbj1pZHMpLm9yZGVyX2J5KCJub21icmUiKQoKCmNsYXNzIENsaWVudGVEZXRhaWxWaWV3KExvZ2luUmVxdWlyZWRNaXhpbiwgRGV0YWlsVmlldyk6CiAgICBtb2RlbCA9IEVudGlkYWQKICAgIHRlbXBsYXRlX25hbWUgPSAicmlzay9yaXNrY2xpZW50ZGV0YWlsLmh0bWwiCiAgICBjb250ZXh0X29iamVjdF9uYW1lID0gImVudGlkYWQiCiAgICBzbHVnX2ZpZWxkID0gImNvZGlnbyIKICAgIHNsdWdfdXJsX2t3YXJnID0gImNvZGlnbyIKCiAgICBkZWYgZ2V0X2NvbnRleHRfZGF0YShzZWxmLCAqKmt3YXJncyk6CiAgICAgICAgY3R4ID0gc3VwZXIoKS5nZXRfY29udGV4dF9kYXRhKCoqa3dhcmdzKQogICAgICAgIGVudGlkYWQgPSBzZWxmLm9iamVjdAogICAgICAgIGN0eFsiZXN0YWRvcyJdID0gZW50aWRhZC5lc3RhZG9zX2ZpbmFuY2llcm9zLm9yZGVyX2J5KCItcGVyaW9kbyIpWzoxMl0KICAgICAgICBjdHhbInByb2dyYW1hY2lvbmVzIl0gPSBlbnRpZGFkLnByb2dyYW1hY2lvbmVzX3BhZ28ub3JkZXJfYnkoIi1mZWNoYV9wcm9ncmFtYWRhIilbOjIwXQogICAgICAgIGN0eFsicGFnb3MiXSA9IGVudGlkYWQucGFnb3NfcmVhbGl6YWRvcy5vcmRlcl9ieSgiLWZlY2hhX3BhZ28iKVs6MjBdCiAgICAgICAgY3R4WyJzbmFwc2hvdHMiXSA9IGVudGlkYWQucmlza19zbmFwc2hvdHMuc2VsZWN0X3JlbGF0ZWQoInByb2R1Y3RvIikub3JkZXJfYnkoCiAgICAgICAgICAgICItZmVjaGFfc25hcHNob3QiCiAgICAgICAgKVs6MjBdCiAgICAgICAgY3R4WyJjb250YWN0b3NfY29icmFuemEiXSA9IGVudGlkYWQuY29udGFjdG9zX2NvYnJhbnphLmZpbHRlcihhY3Rpdm89VHJ1ZSkKICAgICAgICByZXR1cm4gY3R4CgoKY2xhc3MgT3BlcmFjaW9uRGV0YWlsVmlldyhMb2dpblJlcXVpcmVkTWl4aW4sIERldGFpbFZpZXcpOgogICAgbW9kZWwgPSBSaXNrT3BlcmF0aW9uU25hcHNob3QKICAgIHRlbXBsYXRlX25hbWUgPSAicmlzay9yaXNrb3BlcmF0aW9uZGV0YWlsLmh0bWwiCiAgICBjb250ZXh0X29iamVjdF9uYW1lID0gInNuYXBzaG90IgogICAgcGtfdXJsX2t3YXJnID0gInBrIgoKICAgIGRlZiBnZXRfY29udGV4dF9kYXRhKHNlbGYsICoqa3dhcmdzKToKICAgICAgICBjdHggPSBzdXBlcigpLmdldF9jb250ZXh0X2RhdGEoKiprd2FyZ3MpCiAgICAgICAgc25hcCA9IHNlbGYub2JqZWN0CiAgICAgICAgcmVmID0gc25hcC5yZWZlcmVuY2lhX29wZXJhY2lvbgogICAgICAgIGN0eFsiaGlzdG9yaWFsIl0gPSBSaXNrT3BlcmF0aW9uU25hcHNob3Qub2JqZWN0cy5maWx0ZXIoCiAgICAgICAgICAgIGVudGlkYWQ9c25hcC5lbnRpZGFkLAogICAgICAgICAgICByZWZlcmVuY2lhX29wZXJhY2lvbj1yZWYsCiAgICAgICAgKS5vcmRlcl9ieSgiLWZlY2hhX3NuYXBzaG90IikKICAgICAgICAjIFJlbnRhcy9jdW90YXMgZGVsIGNvbnRyYXRvOiByZWZlcmVuY2lhIGVtcGllemEgY29uIGVsIGPDs2RpZ28gZGUgb3BlcmFjacOzbgogICAgICAgIGN0eFsicGFnb3NfcHJvZ3JhbWFkb3MiXSA9IFByb2dyYW1hY2lvblBhZ28ub2JqZWN0cy5maWx0ZXIoCiAgICAgICAgICAgIGVudGlkYWQ9c25hcC5lbnRpZGFkLAogICAgICAgICAgICByZWZlcmVuY2lhX19zdGFydHN3aXRoPXJlZiwKICAgICAgICApLm9yZGVyX2J5KCItZmVjaGFfcHJvZ3JhbWFkYSIpWzozMF0KICAgICAgICBmcm9tIHJpc2subW9kZWxzIGltcG9ydCBQYWdvUmVhbGl6YWRvCgogICAgICAgIGN0eFsicGFnb3NfcmVhbGl6YWRvcyJdID0gUGFnb1JlYWxpemFkby5vYmplY3RzLmZpbHRlcigKICAgICAgICAgICAgZW50aWRhZD1zbmFwLmVudGlkYWQsCiAgICAgICAgICAgIHJlZmVyZW5jaWFfX3N0YXJ0c3dpdGg9cmVmLAogICAgICAgICkub3JkZXJfYnkoIi1mZWNoYV9wYWdvIilbOjMwXQogICAgICAgIGN0eFsiYnJlYWRjcnVtYnMiXSA9IFsKICAgICAgICAgICAgeyJsYWJlbCI6ICJQYW5lbCBwcmluY2lwYWwiLCAidXJsIjogIi9wYW5lbC8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJCYWzDs24gZGUgUmllc2dvIiwgInVybCI6ICIvcmlzay8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJDbGllbnRlcyIsICJ1cmwiOiAiL3Jpc2svY2xpZW50ZXMvIn0sCiAgICAgICAgICAgIHsibGFiZWwiOiBzbmFwLmVudGlkYWQubm9tYnJlLCAidXJsIjogZiIvcmlzay9jbGllbnRlL3tzbmFwLmVudGlkYWQuY29kaWdvfS8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6IHJlZn0sCiAgICAgICAgXQogICAgICAgIHJldHVybiBjdHgKCgpAbG9naW5fcmVxdWlyZWQKZGVmIGltcG9ydGFyKHJlcXVlc3QpOgogICAgcmV0dXJuIHJlZGlyZWN0KCJpbXBvcnRzOmltcG9ydF9odWIiKQoKCkBsb2dpbl9yZXF1aXJlZApkZWYgZXhwb3J0X2NvbWFuZG9fYmFsb24ocmVxdWVzdCk6CiAgICBpbXBvcnQgY3N2CgogICAgcXMgPSBsYXRlc3Rfc25hcHNob3RzX3F1ZXJ5c2V0KHJlcXVlc3QpCiAgICByZXNwb25zZSA9IEh0dHBSZXNwb25zZShjb250ZW50X3R5cGU9InRleHQvY3N2IikKICAgIHJlc3BvbnNlWyJDb250ZW50LURpc3Bvc2l0aW9uIl0gPSAnYXR0YWNobWVudDsgZmlsZW5hbWU9ImNvbWFuZG9fYmFsb24uY3N2IicKICAgIHdyaXRlciA9IGNzdi53cml0ZXIocmVzcG9uc2UpCiAgICB3cml0ZXIud3JpdGVyb3coCiAgICAgICAgWwogICAgICAgICAgICAiZmVjaGEiLAogICAgICAgICAgICAiY2xpZW50ZSIsCiAgICAgICAgICAgICJvcGVyYWNpb24iLAogICAgICAgICAgICAicHJvZHVjdG8iLAogICAgICAgICAgICAic2FsZG8iLAogICAgICAgICAgICAiZXhpZ2libGUiLAogICAgICAgICAgICAiZGlhc19tb3JhIiwKICAgICAgICAgICAgIm5pdmVsIiwKICAgICAgICAgICAgImFsZXJ0YSIsCiAgICAgICAgXQogICAgKQogICAgZm9yIHMgaW4gcXM6CiAgICAgICAgd3JpdGVyLndyaXRlcm93KAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICBzLmZlY2hhX3NuYXBzaG90LAogICAgICAgICAgICAgICAgcy5lbnRpZGFkLm5vbWJyZSwKICAgICAgICAgICAgICAgIHMucmVmZXJlbmNpYV9vcGVyYWNpb24sCiAgICAgICAgICAgICAgICBzLnByb2R1Y3RvLm5vbWJyZSBpZiBzLnByb2R1Y3RvIGVsc2UgIiIsCiAgICAgICAgICAgICAgICBzLnNhbGRvLAogICAgICAgICAgICAgICAgcy5tb250b19leGlnaWJsZSwKICAgICAgICAgICAgICAgIHMuZGlhc19tb3JhLAogICAgICAgICAgICAgICAgcy5uaXZlbF9yaWVzZ28sCiAgICAgICAgICAgICAgICAiMSIgaWYgcy5hbGVydGEgZWxzZSAiMCIsCiAgICAgICAgICAgIF0KICAgICAgICApCiAgICByZXR1cm4gcmVzcG9uc2UK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
