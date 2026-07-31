"""Intermediación gerencial — estructura A–E estilo RIntGer (wc-mod5c)."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .indices import derived_metrics
from .utils import BU_LABEL, fmt, kpi_row, last_n, n, rates_from_meta


def _rates_for_bu(data: dict, bu: str, period: str, rates: dict) -> tuple[float, float]:
    if bu == "L":
        activa = rates["activa_l"]
        pasiva = 0.55 * rates["pasiva_bancos_l"] + 0.45 * rates["pasiva_inv_l"]
    elif bu == "F":
        activa = rates["activa_f"]
        pasiva = 0.55 * rates["pasiva_bancos_f"] + 0.45 * rates["pasiva_inv_f"]
    else:
        cf = n(kpi_row(data, "F", period).get("cartera"))
        cl = n(kpi_row(data, "L", period).get("cartera"))
        tot = cf + cl or 1.0
        activa = rates["activa_f"] * (cf / tot) + rates["activa_l"] * (cl / tot)
        pasiva = (
            (0.55 * rates["pasiva_bancos_f"] + 0.45 * rates["pasiva_inv_f"]) * (cf / tot)
            + (0.55 * rates["pasiva_bancos_l"] + 0.45 * rates["pasiva_inv_l"]) * (cl / tot)
        )
    return activa, pasiva


def _util_flow(prev_period: str | None, prev_util: float | None, period: str, util: float) -> float:
    """Flujo de utilidad del mes a partir de saldos mensuales (pueden bajar)."""
    if prev_period is None or prev_util is None:
        return util
    if prev_period[:4] == period[:4]:
        return util - prev_util
    return util


def _intermediation_slice(
    data: dict,
    bu: str,
    period: str,
    rates: dict,
    mode: str,
    prev_period: str | None = None,
    prev_util_c: float | None = None,
    prev_util_g: float | None = None,
) -> dict[str, Any]:
    row = kpi_row(data, bu, period)
    m = derived_metrics(row, bu, period, rates, vista="contable")
    cartera = n(m.get("cartera"))
    pasivo = n(m.get("pasivo_books"))
    pat = n(m.get("patrimonio_books"))
    inv = n(m.get("inv_proxy"))
    captacion = pasivo + inv

    activa, pasiva = _rates_for_bu(data, bu, period, rates)

    # Flujo del mes (no YTD): cartera × tasa / 12
    productos_mes = cartera * activa / 12.0
    costos_mes = captacion * pasiva / 12.0
    margen_mes = productos_mes - costos_mes

    util_c = n(m.get("utilidades"))
    util_g = n(m.get("util_gerencial"))
    util_flow_c = _util_flow(prev_period, prev_util_c, period, util_c)
    util_flow_g = _util_flow(prev_period, prev_util_g, period, util_g)
    util_flow = util_flow_g if mode == "gerencial" else util_flow_c
    overhead_mes = margen_mes - util_flow

    return {
        "period": period,
        "colocaciones": cartera,
        "captaciones": captacion,
        "productos": productos_mes,
        "costos": costos_mes,
        "margen_bruto": margen_mes,
        "overhead_neto": overhead_mes,
        "utilidad": util_flow,
        "util_contable": util_c,
        "util_gerencial": util_g,
        "util_flow_c": util_flow_c,
        "util_flow_g": util_flow_g,
        "util_saldo": util_g if mode == "gerencial" else util_c,
        "tasa_activa": activa,
        "tasa_pasiva": pasiva,
        "patrimonio": pat,
        "spread": activa - pasiva,
    }


def _build_slices(data: dict, bu: str, periods: list[str], rates: dict, mode: str) -> list[dict]:
    out: list[dict] = []
    prev_p = None
    prev_uc = prev_ug = None
    # Need util before window start for correct first-month flow
    all_p = list(data.get("periods") or [])
    if periods:
        idx0 = all_p.index(periods[0]) if periods[0] in all_p else 0
        if idx0 > 0:
            warm = _intermediation_slice(data, bu, all_p[idx0 - 1], rates, mode)
            prev_p = warm["period"]
            prev_uc = warm["util_contable"]
            prev_ug = warm["util_gerencial"]
    for p in periods:
        sl = _intermediation_slice(
            data, bu, p, rates, mode,
            prev_period=prev_p, prev_util_c=prev_uc, prev_util_g=prev_ug,
        )
        out.append(sl)
        prev_p = p
        prev_uc = sl["util_contable"]
        prev_ug = sl["util_gerencial"]
    return out


def _aggregate(slices: list[dict]) -> dict[str, float]:
    return {
        "productos": sum(s["productos"] for s in slices),
        "costos": sum(s["costos"] for s in slices),
        "margen_bruto": sum(s["margen_bruto"] for s in slices),
        "overhead_neto": sum(s["overhead_neto"] for s in slices),
        "utilidad": sum(s["utilidad"] for s in slices),
        "util_flow_c": sum(s["util_flow_c"] for s in slices),
        "util_flow_g": sum(s["util_flow_g"] for s in slices),
    }


def _quarter_key(period: str) -> str:
    y, m = period.split("-")[0], int(period.split("-")[1])
    return f"{y}-Q{(m - 1) // 3 + 1}"


def _chart_from_buckets(buckets: list[tuple[str, list[dict]]]) -> dict:
    labels = [k for k, _ in buckets]
    return {
        "labels": labels,
        "datasets": [
            {
                "label": "Colocaciones (fin)",
                "data": [b[-1]["colocaciones"] for _, b in buckets],
                "borderColor": "#1e4d3a",
                "yAxisID": "y",
                "tension": 0.25,
            },
            {
                "label": "Captaciones (fin)",
                "data": [b[-1]["captaciones"] for _, b in buckets],
                "borderColor": "#2f6f9f",
                "yAxisID": "y",
                "tension": 0.25,
            },
            {
                "label": "Margen del período",
                "data": [sum(x["margen_bruto"] for x in b) for _, b in buckets],
                "borderColor": "#8a6d3b",
                "yAxisID": "y1",
                "tension": 0.25,
            },
            {
                "label": "Utilidad del período",
                "data": [sum(x["utilidad"] for x in b) for _, b in buckets],
                "borderColor": "#8a3a34",
                "yAxisID": "y1",
                "tension": 0.25,
            },
        ],
    }


def build_intermediacion(
    data: dict,
    bu: str = "T",
    months: int = 12,
    end_period: str | None = None,
    mode: str = "gerencial",
) -> dict[str, Any]:
    periods = list(data.get("periods") or [])
    if not periods:
        return {"status": "empty", "sections": [], "chart": {}}

    if end_period and end_period in periods:
        end_idx = periods.index(end_period)
    else:
        end_idx = len(periods) - 1
        end_period = periods[end_idx]

    months = max(1, min(36, int(months)))
    start_idx = max(0, end_idx - months + 1)
    window = periods[start_idx : end_idx + 1]

    rates = rates_from_meta(data)
    mode = "gerencial" if mode == "gerencial" else "contable"

    # Series completa hasta end (para trim/anual)
    hist = periods[: end_idx + 1]
    all_slices = _build_slices(data, bu, hist, rates, mode)
    by_period = {s["period"]: s for s in all_slices}
    slices = [by_period[p] for p in window]
    latest = slices[-1]
    first = slices[0]
    agg = _aggregate(slices)

    def dlt(a: float, b: float) -> float | None:
        if b == 0:
            return None
        return (a - b) / abs(b)

    n_m = len(slices)
    sections = [
        {
            "id": "A",
            "title": "Colocaciones",
            "subtitle": f"Saldo al cierre · {latest['period']}",
            "metrics": [
                {"label": "Saldo cartera", "value": fmt(latest["colocaciones"]), "hint": "000 QTZ · stock"},
                {"label": "Tasa activa (est.)", "value": f"{latest['tasa_activa']*100:.1f}%", "hint": "Control qf"},
                {
                    "label": "Δ saldo en el período",
                    "value": f"{dlt(latest['colocaciones'], first['colocaciones'])*100:+.1f}%"
                    if dlt(latest["colocaciones"], first["colocaciones"]) is not None
                    else "—",
                    "hint": f"{first['period']} → {latest['period']}",
                },
            ],
        },
        {
            "id": "B",
            "title": "Captaciones",
            "subtitle": "Fondeo gerencial al cierre (pasivo + preferentes est.)",
            "metrics": [
                {"label": "Fondeo total", "value": fmt(latest["captaciones"]), "hint": "000 QTZ · stock"},
                {"label": "Tasa pasiva (est.)", "value": f"{latest['tasa_pasiva']*100:.1f}%", "hint": "Bancos+inv."},
                {"label": "Spread", "value": f"{latest['spread']*100:.1f} pp", "hint": "Activa − pasiva"},
            ],
        },
        {
            "id": "C",
            "title": "Margen bruto",
            "subtitle": f"Suma de {n_m} mes(es) terminando en {latest['period']}",
            "metrics": [
                {"label": "Productos del período", "value": fmt(agg["productos"]), "hint": f"{n_m} meses acum."},
                {"label": "Costos fondeo del período", "value": fmt(agg["costos"]), "hint": "est. acum."},
                {"label": "Margen bruto del período", "value": fmt(agg["margen_bruto"]), "hint": "Intermediación"},
            ],
        },
        {
            "id": "D",
            "title": "Overhead neto",
            "subtitle": f"Residuo acum. {n_m} mes(es) (margen − utilidad del período)",
            "metrics": [
                {"label": "Overhead del período", "value": fmt(agg["overhead_neto"]), "hint": "000 QTZ"},
                {
                    "label": "% del margen",
                    "value": f"{(agg['overhead_neto']/agg['margen_bruto']*100):.0f}%"
                    if agg["margen_bruto"]
                    else "—",
                    "hint": "eficiencia",
                },
            ],
        },
        {
            "id": "E",
            "title": "Utilidad del período",
            "subtitle": (
                f"{'Gerencial' if mode == 'gerencial' else 'Contable'} · "
                f"suma de flujos mensuales ({n_m} meses)"
            ),
            "metrics": [
                {"label": "Utilidad del período", "value": fmt(agg["utilidad"]), "hint": mode},
                {"label": "Flujo contable acum.", "value": fmt(agg["util_flow_c"]), "hint": "MoM"},
                {"label": "Flujo gerencial acum.", "value": fmt(agg["util_flow_g"]), "hint": "post inv."},
            ],
        },
    ]

    chart = {
        "labels": [s["period"] for s in slices],
        "datasets": [
            {
                "label": "Colocaciones",
                "data": [s["colocaciones"] for s in slices],
                "borderColor": "#1e4d3a",
                "yAxisID": "y",
                "tension": 0.25,
            },
            {
                "label": "Captaciones",
                "data": [s["captaciones"] for s in slices],
                "borderColor": "#2f6f9f",
                "yAxisID": "y",
                "tension": 0.25,
            },
            {
                "label": "Margen del mes",
                "data": [s["margen_bruto"] for s in slices],
                "borderColor": "#8a6d3b",
                "yAxisID": "y1",
                "tension": 0.25,
            },
            {
                "label": "Utilidad del mes",
                "data": [s["utilidad"] for s in slices],
                "borderColor": "#8a3a34",
                "yAxisID": "y1",
                "tension": 0.25,
            },
        ],
    }

    # Trimestral: últimos 10 trimestres hasta end
    qmap: dict[str, list[dict]] = defaultdict(list)
    for s in all_slices:
        qmap[_quarter_key(s["period"])].append(s)
    q_keys = sorted(qmap.keys())[-10:]
    chart_quarterly = _chart_from_buckets([(k, qmap[k]) for k in q_keys])

    # Anual: 2023, 2024, 2025 y 2026 (porción)
    ymap: dict[str, list[dict]] = defaultdict(list)
    for s in all_slices:
        ymap[s["period"][:4]].append(s)
    y_keys = [y for y in ("2023", "2024", "2025", "2026") if y in ymap]
    chart_annual = _chart_from_buckets([(k, ymap[k]) for k in y_keys])

    story = (
        f"{BU_LABEL.get(bu, bu)} · período {window[0]} → {window[-1]} ({n_m} meses) · modo {mode}. "
        f"Productos, costos, margen, overhead y utilidad de los cuadros C–E son "
        f"acumulados de ese período. Colocaciones y captaciones son saldos al cierre. "
        f"Margen acum. {fmt(agg['margen_bruto'])}; utilidad acum. {fmt(agg['utilidad'])} (000 QTZ)."
    )

    return {
        "status": "ok",
        "bu": bu,
        "bu_label": BU_LABEL.get(bu, bu),
        "mode": mode,
        "months": n_m,
        "months_requested": months,
        "end_period": window[-1],
        "start_period": window[0],
        "periods_available": periods,
        "unit": data.get("unit") or "000 quetzales",
        "sections": sections,
        "latest": latest,
        "aggregated": agg,
        "series": slices,
        "chart": chart,
        "chart_quarterly": chart_quarterly,
        "chart_annual": chart_annual,
        "story": story,
    }
