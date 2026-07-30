"""Dashboards de liquidez / estructura con bandas y peers."""

from __future__ import annotations

from typing import Any

from .bands import band_chart_guides, evaluate_ratio
from .indices import build_indices_catalog, derived_metrics
from .peers import peers_with_self
from .utils import BU_LABEL, fmt, kpi_row, last_n, n, rates_from_meta


def _structural_break_note(labels: list[str], liq: list, apa: list) -> str | None:
    """Detecta el mayor salto absoluto de liquidez en la ventana."""
    if len(labels) < 3:
        return None
    best_i, best_abs = None, 0.0
    for i in range(1, len(labels)):
        if liq[i] is None or liq[i - 1] is None:
            continue
        jump = abs(float(liq[i]) - float(liq[i - 1]))
        if jump > best_abs:
            best_abs, best_i = jump, i
    if best_i is None or best_abs < 0.25:
        return None
    a, b = labels[best_i - 1], labels[best_i]
    dl = float(liq[best_i]) - float(liq[best_i - 1])
    da = 0.0
    if apa[best_i] is not None and apa[best_i - 1] is not None:
        da = float(apa[best_i]) - float(apa[best_i - 1])
    return (
        f"Cambio estructural {a}→{b}: liquidez {dl:+.2f}× "
        f"(de {float(liq[best_i-1]):.2f} a {float(liq[best_i]):.2f}); "
        f"apalancamiento {da:+.2f}×. "
        "Interpretar el salto con las bandas óptimas, no solo la serie."
    )


def build_liquidez_board(data: dict, bu: str = "T", months: int = 14) -> dict[str, Any]:
    catalog = build_indices_catalog(data, bu=bu, periods=months)
    if catalog.get("status") != "ok":
        return {"status": "empty"}

    m = catalog["metrics"]
    liq_ev = evaluate_ratio("liquidez", m.get("liquidez"))
    apa_ev = evaluate_ratio("apalancamiento", m.get("apalancamiento"))
    acida_ev = evaluate_ratio("acida", m.get("acida"))
    z_ev = evaluate_ratio("z_score", m.get("z_score"))

    series = catalog["series"]
    labels = series["labels"]
    break_note = _structural_break_note(labels, series["liquidez"], series["apalancamiento"])

    peers = peers_with_self(m.get("liquidez"), m.get("apalancamiento"), catalog["period"])

    chart = {
        "labels": labels,
        "datasets": [
            {
                "label": "Liquidez",
                "data": series["liquidez"],
                "borderColor": "#2f5c4e",
                "yAxisID": "y",
                "tension": 0.25,
            },
            {
                "label": "Ácida adaptada",
                "data": series["acida"],
                "borderColor": "#2f6f9f",
                "yAxisID": "y",
                "borderDash": [5, 4],
                "tension": 0.25,
            },
            {
                "label": "Apalancamiento",
                "data": series["apalancamiento"],
                "borderColor": "#8a3a34",
                "yAxisID": "y1",
                "tension": 0.25,
            },
        ],
        "guides_liq": band_chart_guides("liquidez"),
        "guides_apa": band_chart_guides("apalancamiento"),
    }

    cards = [
        {
            "label": liq_ev["label"],
            "display": f"{m['liquidez']:.2f}×" if m.get("liquidez") is not None else "—",
            "tone": liq_ev["tone"],
            "zone": liq_ev["zone"],
            "meaning": liq_ev["meaning"],
            "band": f"{liq_ev['bands'].get('optimal_low', '—')}–{liq_ev['bands'].get('optimal_high', '—')}× óptimo",
        },
        {
            "label": acida_ev["label"],
            "display": f"{m['acida']:.2f}×" if m.get("acida") is not None else "—",
            "tone": acida_ev["tone"],
            "zone": acida_ev["zone"],
            "meaning": acida_ev["meaning"],
            "band": f"{acida_ev['bands'].get('optimal_low', '—')}–{acida_ev['bands'].get('optimal_high', '—')}× óptimo",
        },
        {
            "label": "Capital de trabajo",
            "display": fmt(m.get("capital_trabajo")),
            "tone": "ok" if n(m.get("capital_trabajo")) > 0 else "risk",
            "zone": "positivo" if n(m.get("capital_trabajo")) > 0 else "negativo",
            "meaning": "AC − PC. Buffer de corto plazo (000 QTZ).",
            "band": "—",
        },
        {
            "label": apa_ev["label"],
            "display": f"{m['apalancamiento']:.2f}×" if m.get("apalancamiento") is not None else "—",
            "tone": apa_ev["tone"],
            "zone": apa_ev["zone"],
            "meaning": apa_ev["meaning"],
            "band": f"{apa_ev['bands'].get('optimal_low', '—')}–{apa_ev['bands'].get('optimal_high', '—')}× óptimo",
        },
        {
            "label": z_ev["label"],
            "display": f"{m['z_score']:.2f}" if m.get("z_score") is not None else "—",
            "tone": z_ev["tone"],
            "zone": z_ev["zone"],
            "meaning": z_ev["meaning"],
            "band": f"{z_ev['bands'].get('optimal_low', '—')}–{z_ev['bands'].get('optimal_high', '—')} óptimo",
        },
    ]

    return {
        "status": "ok",
        "bu": bu,
        "bu_label": BU_LABEL.get(bu, bu),
        "period": catalog["period"],
        "unit": catalog["unit"],
        "cards": cards,
        "peers": peers,
        "chart": chart,
        "break_note": break_note,
        "z_series": {"labels": labels, "data": series["z_score"]},
        "story": (
            f"Liquidez y solvencia · {BU_LABEL.get(bu, bu)} · {catalog['period']}. "
            "Cada indicador se interpreta contra bandas NBFI factoraje/leasing, no solo contra sí mismo."
        ),
    }


def build_estructura_board(data: dict, bu: str = "T", months: int = 14) -> dict[str, Any]:
    periods = list(data.get("periods") or [])
    if not periods:
        return {"status": "empty"}
    focus = last_n(periods, months)
    rates = rates_from_meta(data)
    latest = focus[-1]
    m = derived_metrics(kpi_row(data, bu, latest), bu, latest, rates)

    labels = focus
    pas_c = [n(derived_metrics(kpi_row(data, bu, p), bu, p, rates).get("pasivo_corriente")) for p in focus]
    pas_nc = [n(derived_metrics(kpi_row(data, bu, p), bu, p, rates).get("pasivo_no_corriente")) for p in focus]
    pat = [n(derived_metrics(kpi_row(data, bu, p), bu, p, rates).get("patrimonio")) for p in focus]
    ac = [n(derived_metrics(kpi_row(data, bu, p), bu, p, rates).get("activo_corriente")) for p in focus]
    act = [n(derived_metrics(kpi_row(data, bu, p), bu, p, rates).get("activo")) for p in focus]
    deuda_g = [
        derived_metrics(kpi_row(data, bu, p), bu, p, rates).get("deuda_gerencial_patrimonio") for p in focus
    ]

    deuda_ev = evaluate_ratio("deuda_patrimonio", m.get("deuda_gerencial_patrimonio"))
    short_share = (n(m.get("pasivo_corriente")) / n(m.get("pasivo_total"))) if n(m.get("pasivo_total")) else None

    chart_fondeo = {
        "labels": labels,
        "datasets": [
            {"label": "Pasivo corriente", "data": pas_c, "borderColor": "#8a3a34", "tension": 0.25},
            {"label": "Pasivo no corriente", "data": pas_nc, "borderColor": "#8a6d3b", "tension": 0.25},
            {"label": "Patrimonio", "data": pat, "borderColor": "#1e4d3a", "tension": 0.25},
        ],
    }
    chart_activos = {
        "labels": labels,
        "datasets": [
            {"label": "Activo corriente", "data": ac, "borderColor": "#2f6f9f", "tension": 0.25},
            {"label": "Activo total", "data": act, "borderColor": "#1e4d3a", "tension": 0.25},
        ],
    }
    chart_deuda = {
        "labels": labels,
        "datasets": [
            {
                "label": "Deuda gerencial / Patrimonio",
                "data": deuda_g,
                "borderColor": "#5b7c99",
                "tension": 0.25,
            }
        ],
        "guides": band_chart_guides("deuda_patrimonio"),
    }

    return {
        "status": "ok",
        "bu": bu,
        "bu_label": BU_LABEL.get(bu, bu),
        "period": latest,
        "unit": data.get("unit") or "000 quetzales",
        "cards": [
            {
                "label": "Financiamiento vs patrimonio",
                "display": f"{n(m.get('pasivo_total'))/n(m.get('patrimonio')):.2f}×"
                if n(m.get("patrimonio"))
                else "—",
                "hint": "Pasivo / Patrimonio",
            },
            {
                "label": "Deuda gerencial / Pat.",
                "display": f"{m['deuda_gerencial_patrimonio']:.2f}×"
                if m.get("deuda_gerencial_patrimonio") is not None
                else "—",
                "hint": deuda_ev["zone"],
                "tone": deuda_ev["tone"],
            },
            {
                "label": "% pasivo corto plazo",
                "display": f"{short_share*100:.0f}%" if short_share is not None else "—",
                "hint": "Perfil de endeudamiento",
            },
            {
                "label": "AC / Activo total",
                "display": f"{n(m.get('activo_corriente'))/n(m.get('activo'))*100:.0f}%"
                if n(m.get("activo"))
                else "—",
                "hint": "Composición de activos",
            },
            {
                "label": "Cobertura intereses (est.)",
                "display": f"{m['cobertura_intereses']:.2f}×"
                if m.get("cobertura_intereses") is not None
                else "—",
                "hint": "Utilidad / interés est.",
            },
        ],
        "chart_fondeo": chart_fondeo,
        "chart_activos": chart_activos,
        "chart_deuda": chart_deuda,
        "deuda_eval": deuda_ev,
        "story": (
            f"Estructura de fondeo y activos · {BU_LABEL.get(bu, bu)} · {latest}. "
            "Preferentes se tratan como deuda gerencial para el análisis de intermediación."
        ),
    }
