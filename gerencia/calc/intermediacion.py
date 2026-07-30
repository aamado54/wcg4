"""Intermediación gerencial — estructura A–E estilo RIntGer (wc-mod5c)."""

from __future__ import annotations

from typing import Any

from .indices import derived_metrics
from .utils import BU_LABEL, fmt, kpi_row, last_n, month_of, n, rates_from_meta


def _intermediation_slice(data: dict, bu: str, period: str, rates: dict, mode: str) -> dict[str, Any]:
    row = kpi_row(data, bu, period)
    m = derived_metrics(row, bu, period, rates)
    cartera = n(m.get("cartera"))
    pasivo = n(m.get("pasivo_total"))
    pat = n(m.get("patrimonio"))
    inv = n(m.get("inv_proxy"))
    captacion = pasivo + inv  # fondeo gerencial

    if bu == "L":
        activa = rates["activa_l"]
        pasiva = 0.55 * rates["pasiva_bancos_l"] + 0.45 * rates["pasiva_inv_l"]
    elif bu == "F":
        activa = rates["activa_f"]
        pasiva = 0.55 * rates["pasiva_bancos_f"] + 0.45 * rates["pasiva_inv_f"]
    else:
        # Total: ponderar por cartera F vs L si disponible
        cf = n(kpi_row(data, "F", period).get("cartera"))
        cl = n(kpi_row(data, "L", period).get("cartera"))
        tot = cf + cl or 1.0
        activa = rates["activa_f"] * (cf / tot) + rates["activa_l"] * (cl / tot)
        pasiva = (
            (0.55 * rates["pasiva_bancos_f"] + 0.45 * rates["pasiva_inv_f"]) * (cf / tot)
            + (0.55 * rates["pasiva_bancos_l"] + 0.45 * rates["pasiva_inv_l"]) * (cl / tot)
        )

    months = month_of(period)
    productos = cartera * activa * (months / 12.0)
    costos = captacion * pasiva * (months / 12.0)
    margen = productos - costos
    util_c = n(m.get("utilidades"))
    util_g = n(m.get("util_gerencial"))
    utilidad = util_g if mode == "gerencial" else util_c
    # Overhead neto ≈ margen − utilidad (residuo de operación / admin / otros)
    overhead = margen - utilidad

    return {
        "period": period,
        "colocaciones": cartera,
        "captaciones": captacion,
        "productos": productos,
        "costos": costos,
        "margen_bruto": margen,
        "overhead_neto": overhead,
        "utilidad": utilidad,
        "util_contable": util_c,
        "util_gerencial": util_g,
        "tasa_activa": activa,
        "tasa_pasiva": pasiva,
        "patrimonio": pat,
        "spread": activa - pasiva,
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
        window = periods[max(0, end_idx - months + 1) : end_idx + 1]
    else:
        window = last_n(periods, months)

    rates = rates_from_meta(data)
    mode = "gerencial" if mode == "gerencial" else "contable"
    slices = [_intermediation_slice(data, bu, p, rates, mode) for p in window]
    latest = slices[-1]
    first = slices[0]

    def dlt(a: float, b: float) -> float | None:
        if b == 0:
            return None
        return (a - b) / abs(b)

    sections = [
        {
            "id": "A",
            "title": "Colocaciones",
            "subtitle": "Cartera de intermediación",
            "metrics": [
                {"label": "Saldo cartera", "value": fmt(latest["colocaciones"]), "hint": "000 QTZ"},
                {"label": "Tasa activa (est.)", "value": f"{latest['tasa_activa']*100:.1f}%", "hint": "Control qf"},
                {
                    "label": "Δ período",
                    "value": f"{dlt(latest['colocaciones'], first['colocaciones'])*100:+.1f}%"
                    if dlt(latest["colocaciones"], first["colocaciones"]) is not None
                    else "—",
                    "hint": f"vs {first['period']}",
                },
            ],
        },
        {
            "id": "B",
            "title": "Captaciones",
            "subtitle": "Fondeo gerencial (pasivo + preferentes est.)",
            "metrics": [
                {"label": "Fondeo total", "value": fmt(latest["captaciones"]), "hint": "000 QTZ"},
                {"label": "Tasa pasiva (est.)", "value": f"{latest['tasa_pasiva']*100:.1f}%", "hint": "Bancos+inv."},
                {"label": "Spread", "value": f"{latest['spread']*100:.1f} pp", "hint": "Activa − pasiva"},
            ],
        },
        {
            "id": "C",
            "title": "Margen bruto",
            "subtitle": "Productos de colocación − costos de captación",
            "metrics": [
                {"label": "Productos", "value": fmt(latest["productos"]), "hint": f"YTD {latest['period']}"},
                {"label": "Costos fondeo", "value": fmt(latest["costos"]), "hint": "est."},
                {"label": "Margen bruto", "value": fmt(latest["margen_bruto"]), "hint": "Intermediación pura"},
            ],
        },
        {
            "id": "D",
            "title": "Overhead neto",
            "subtitle": "Residuo operación / admin / otros (margen − utilidad)",
            "metrics": [
                {"label": "Overhead neto", "value": fmt(latest["overhead_neto"]), "hint": "000 QTZ"},
                {
                    "label": "% del margen",
                    "value": f"{(latest['overhead_neto']/latest['margen_bruto']*100):.0f}%"
                    if latest["margen_bruto"]
                    else "—",
                    "hint": "eficiencia",
                },
            ],
        },
        {
            "id": "E",
            "title": "Utilidad neta",
            "subtitle": "Contable" if mode == "contable" else "Gerencial (después de dividendos / inv.)",
            "metrics": [
                {"label": "Utilidad reportada", "value": fmt(latest["utilidad"]), "hint": mode},
                {"label": "Utilidad contable", "value": fmt(latest["util_contable"]), "hint": "cta 302"},
                {"label": "Utilidad gerencial", "value": fmt(latest["util_gerencial"]), "hint": "post inv."},
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
                "label": "Margen bruto",
                "data": [s["margen_bruto"] for s in slices],
                "borderColor": "#8a6d3b",
                "yAxisID": "y1",
                "tension": 0.25,
            },
            {
                "label": "Utilidad",
                "data": [s["utilidad"] for s in slices],
                "borderColor": "#8a3a34",
                "yAxisID": "y1",
                "tension": 0.25,
            },
        ],
    }

    story = (
        f"{BU_LABEL.get(bu, bu)} · {window[0]} → {window[-1]} · modo {mode}. "
        f"Margen de intermediación {fmt(latest['margen_bruto'])} (000 QTZ); "
        f"utilidad {fmt(latest['utilidad'])}. "
        "Las tasas provienen del control qf/wc-mod5c; el overhead es residual."
    )

    return {
        "status": "ok",
        "bu": bu,
        "bu_label": BU_LABEL.get(bu, bu),
        "mode": mode,
        "months": len(window),
        "end_period": window[-1],
        "periods_available": periods,
        "unit": data.get("unit") or "000 quetzales",
        "sections": sections,
        "latest": latest,
        "series": slices,
        "chart": chart,
        "story": story,
    }
