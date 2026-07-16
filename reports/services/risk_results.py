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
