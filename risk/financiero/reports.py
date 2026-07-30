"""Armado de tableros gerenciales / riesgo / estrategia a partir del combinado."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


BU_ORDER = ("T", "F", "L", "I", "S")
BU_LABEL = {
    "T": "Total WCG",
    "F": "Factoraje",
    "L": "Leasing",
    "I": "Insurance",
    "S": "Services",
}


def _n(v: Any, default: float = 0.0) -> float:
    try:
        if v is None or v == "":
            return default
        return float(v)
    except (TypeError, ValueError):
        return default


def _fmt(v: float | None, digits: int = 0) -> str | None:
    if v is None:
        return None
    if digits == 0:
        return f"{v:,.0f}"
    return f"{v:,.{digits}f}"


def _pct(v: float | None, digits: int = 1) -> str | None:
    if v is None:
        return None
    return f"{v * 100:.{digits}f}%"


def _delta(cur: float | None, prev: float | None) -> float | None:
    if cur is None or prev is None or prev == 0:
        return None
    return (cur - prev) / abs(prev)


@dataclass
class FinancieroBoard:
    status: str
    unit: str
    source_path: str
    headline: str
    story: str
    periods: list[str] = field(default_factory=list)
    recent_periods: list[str] = field(default_factory=list)
    focus_periods: list[str] = field(default_factory=list)
    summary_cards: list[dict] = field(default_factory=list)
    bu_table: list[dict] = field(default_factory=list)
    trend_activo: dict = field(default_factory=dict)
    trend_util: dict = field(default_factory=dict)
    util_compare: list[dict] = field(default_factory=list)
    risk_table: list[dict] = field(default_factory=list)
    strategy_notes: list[str] = field(default_factory=list)
    projection_note: str = ""
    qf_meta: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    chart_activo: dict = field(default_factory=dict)
    chart_util: dict = field(default_factory=dict)
    chart_riesgo: dict = field(default_factory=dict)
    data_warnings: list = field(default_factory=list)
    warnings_count: int = 0
    has_tabla_xlsx: bool = False


def _last_n(periods: list[str], n: int = 12) -> list[str]:
    return periods[-n:] if len(periods) > n else list(periods)


def _kpi(data: dict, bu: str, period: str) -> dict:
    from .quality import enrich_kpi_row

    return enrich_kpi_row(((data.get("kpis") or {}).get(bu) or {}).get(period) or {})


def build_financiero_board(data: dict[str, Any], bu: str = "T") -> FinancieroBoard:
    errors = list(data.get("errors") or [])
    periods = list(data.get("periods") or [])
    recent = list(data.get("recent_periods") or [])
    focus = _last_n(periods, 14)
    bu = (bu or "T").upper()
    if bu not in BU_LABEL:
        bu = "T"

    if data.get("status") != "ok" or not periods:
        return FinancieroBoard(
            status=data.get("status") or "empty",
            unit=data.get("unit") or "000 quetzales",
            source_path=data.get("source_path") or "",
            headline="Sin datos financieros institucionales",
            story="Ejecute la importación wcup2 y regenere combined_series.json.",
            errors=errors or ["Dataset vacío"],
            qf_meta=data.get("qf_extract_meta") or {},
        )

    latest = periods[-1]
    prev = periods[-2] if len(periods) >= 2 else None
    k_latest = _kpi(data, bu, latest)
    k_prev = _kpi(data, bu, prev) if prev else {}

    activo = _n(k_latest.get("activo"))
    util = _n(k_latest.get("utilidades"))
    cartera = _n(k_latest.get("cartera"))
    liq = k_latest.get("liquidez")
    apa = k_latest.get("apalancamiento")
    roe = k_latest.get("roe")

    d_act = _delta(activo, _n(k_prev.get("activo")) if k_prev else None)
    d_util = _delta(util, _n(k_prev.get("utilidades")) if k_prev else None)

    # Contable vs gerencial approximation (qf discipline):
    # Contable ≈ utilidades de balance (302). Gerencial resta costo a inversionistas
    # estimado como 9% anual sobre fondeo implícito (patrimonio * 0.35 proxy) / 12 * YTD months.
    # For board clarity we also surface qf extract control rates.
    qf = data.get("qf_extract_meta") or {}
    rates = ((qf.get("control_defaults") or {}).get("rates") or {})
    pas_i = _n((rates.get("pasiva_inversionistas") or {}).get("F", 0.09), 0.09)
    # Prefer preferentes ≈ portion of patrimonio funded by investors (Factoraje-heavy)
    inv_proxy = _n(k_latest.get("patrimonio")) * (0.45 if bu in ("T", "F") else 0.25)
    month = int(latest.split("-")[1]) if "-" in latest else 6
    # YTD preferred / investor cost in 000 QTZ
    div_pref_ytd = inv_proxy * pas_i * (month / 12.0)
    util_contable = util
    util_gerencial = util - div_pref_ytd

    summary_cards = [
        {
            "label": f"Activo — {BU_LABEL[bu]}",
            "value": _fmt(activo),
            "hint": f"{latest} · 000 QTZ",
            "delta": _pct(d_act),
            "tone": "ok" if (d_act or 0) >= 0 else "risk",
        },
        {
            "label": "Cartera (aprox.)",
            "value": _fmt(cartera) if cartera else "—",
            "hint": "F:10103 · L/I: ver advertencias",
            "delta": None,
            "tone": "warn" if not cartera else "neutral",
        },
        {
            "label": "Utilidad contable",
            "value": _fmt(util_contable),
            "hint": "Cuenta 302 · no resta div. pref.",
            "delta": _pct(d_util),
            "tone": "ok" if util_contable >= 0 else "risk",
        },
        {
            "label": "Utilidad gerencial",
            "value": _fmt(util_gerencial),
            "hint": "Después de costo a inversionistas",
            "delta": None,
            "tone": "warn" if util_gerencial < util_contable * 0.7 else "ok",
        },
        {
            "label": "Liquidez",
            "value": f"{_n(liq):.2f}×" if liq is not None else "—",
            "hint": "AC / PC",
            "delta": None,
            "tone": "ok" if _n(liq) >= 1.2 else "risk",
        },
        {
            "label": "Apalancamiento",
            "value": f"{_n(apa):.2f}×" if apa is not None else "—",
            "hint": "Pasivo / Patrimonio",
            "delta": None,
            "tone": "warn" if _n(apa) > 2 else "ok",
        },
    ]

    # BU comparison at latest
    bu_table = []
    for b in BU_ORDER:
        k = _kpi(data, b, latest)
        if not k:
            continue
        uc = _n(k.get("utilidades"))
        inv_b = _n(k.get("patrimonio")) * (0.45 if b in ("T", "F") else 0.25)
        ug = uc - inv_b * pas_i * (month / 12.0)
        roe_v = k.get("roe")
        bu_table.append(
            {
                "bu": b,
                "label": BU_LABEL[b],
                "activo": _n(k.get("activo")),
                "cartera": _n(k.get("cartera")),
                "util_c": uc,
                "util_g": ug,
                "liquidez": k.get("liquidez"),
                "apalancamiento": k.get("apalancamiento"),
                "roe_pct": (roe_v * 100.0) if roe_v is not None else None,
            }
        )

    # Trends for charts (focus window)
    labels = focus
    colors = {
        "T": "#1e4d3a",
        "F": "#2f6f9f",
        "L": "#8a6d3b",
        "I": "#5b7c99",
        "S": "#6b5b7a",
    }

    def series_metric(metric: str, bus: tuple[str, ...] = ("T", "F", "L")) -> dict:
        datasets = []
        for b in bus:
            datasets.append(
                {
                    "label": BU_LABEL[b],
                    "data": [_n(_kpi(data, b, p).get(metric)) for p in labels],
                    "borderColor": colors[b],
                    "backgroundColor": colors[b] + "33",
                    "tension": 0.25,
                    "fill": False,
                }
            )
        return {"labels": labels, "datasets": datasets}

    chart_activo = series_metric("activo")
    chart_util = series_metric("utilidades")
    chart_riesgo = {
        "labels": labels,
        "datasets": [
            {
                "label": "Liquidez T",
                "data": [_n(_kpi(data, "T", p).get("liquidez")) for p in labels],
                "borderColor": "#2f5c4e",
                "yAxisID": "y",
                "tension": 0.25,
            },
            {
                "label": "Apalancamiento T",
                "data": [_n(_kpi(data, "T", p).get("apalancamiento")) for p in labels],
                "borderColor": "#8a3a34",
                "yAxisID": "y1",
                "tension": 0.25,
            },
        ],
    }
    # Bandas óptimas desde Centro Gerencial (si el módulo está disponible)
    try:
        from gerencia.calc.bands import band_chart_guides, evaluate_ratio

        chart_riesgo["guides_liq"] = band_chart_guides("liquidez")
        chart_riesgo["guides_apa"] = band_chart_guides("apalancamiento")
        liq_ev = evaluate_ratio("liquidez", float(liq) if liq is not None else None)
        apa_ev = evaluate_ratio("apalancamiento", float(apa) if apa is not None else None)
        strategy_notes_band = [
            f"Liquidez {_n(liq):.2f}× → zona «{liq_ev.get('zone')}» "
            f"(óptimo {liq_ev['bands'].get('optimal_low')}–{liq_ev['bands'].get('optimal_high')}×). "
            f"{liq_ev.get('meaning')}",
            f"Apalancamiento {_n(apa):.2f}× → zona «{apa_ev.get('zone')}» "
            f"(óptimo {apa_ev['bands'].get('optimal_low')}–{apa_ev['bands'].get('optimal_high')}×). "
            f"{apa_ev.get('meaning')}",
        ]
    except Exception:  # noqa: BLE001
        strategy_notes_band = []
        chart_riesgo["guides_liq"] = []
        chart_riesgo["guides_apa"] = []

    # Risk table last 6 recent months for selected BU
    risk_periods = recent[-6:] if recent else focus[-6:]
    risk_table = []
    for p in risk_periods:
        k = _kpi(data, bu, p)
        if not k:
            continue
        roa_v, roe_v = k.get("roa"), k.get("roe")
        risk_table.append(
            {
                "period": p,
                "activo": _n(k.get("activo")),
                "cartera": _n(k.get("cartera")),
                "utilidades": _n(k.get("utilidades")),
                "liquidez": k.get("liquidez"),
                "apalancamiento": k.get("apalancamiento"),
                "roa_pct": (roa_v * 100.0) if roa_v is not None else None,
                "roe_pct": (roe_v * 100.0) if roe_v is not None else None,
            }
        )

    util_compare = [
        {
            "concept": "Utilidad contable (302)",
            "detail": "No resta dividendos de acciones preferentes / costo a inversionistas",
            "amount": util_contable,
            "amount_display": _fmt(util_contable),
        },
        {
            "concept": "(-) Costo inversionistas (est.)",
            "detail": f"Proxy patrimonio×tasa pasiva {pas_i:.0%} × {month}/12",
            "amount": -div_pref_ytd,
            "amount_display": f"−{_fmt(div_pref_ytd)}",
        },
        {
            "concept": "Utilidad gerencial",
            "detail": "Después de pagar dividendos / retribución a inversionistas",
            "amount": util_gerencial,
            "amount_display": _fmt(util_gerencial),
        },
    ]

    strategy_notes = [
        f"Período ancla: {latest}. Unidades en 000 quetzales (histórico Datos + importación ÷ 1000).",
        "Utilidad contable vs gerencial: misma disciplina que qf/wc_engine — la gerencial resta el costo a inversionistas.",
        "Importación reciente cubre ene–jun 2026 (BG+ER por F/L/I/S) vía wcup2 sobre wcsource.",
        "El extracto qf aporta tasas/crecimientos de control para contrastar trayectoria proyectada 2026.",
        *strategy_notes_band,
    ]
    if _n(liq) < 1.15:
        strategy_notes.append("Señal de riesgo: liquidez Total bajo 1.15× — revisar pasivo corriente vs activo líquido.")
    if _n(apa) > 2.0:
        strategy_notes.append("Señal de riesgo: apalancamiento elevado (>2×) — vigilar fondeo bancario vs patrimonio.")
    if util_gerencial < 0 < util_contable:
        strategy_notes.append("La utilidad contable es positiva pero la gerencial (post inversionistas) es negativa.")

    d_act_s = f"{_pct(d_act)} vs mes previo" if d_act is not None else "sin mes previo"
    headline = (
        f"{BU_LABEL[bu]} · activo {_fmt(activo)} · utilidad contable {_fmt(util_contable)} "
        f"· gerencial {_fmt(util_gerencial)} ({latest})"
    )
    story = (
        f"En {latest} el activo ({d_act_s}) y las utilidades de balance reflejan la lectura "
        f"combinada del histórico wc-mod5c y los estados financieros importados. "
        f"ROE {_pct(roe) or 'n/d'}; liquidez {_n(liq):.2f}×."
    )

    from .quality import load_warnings, summarize_warnings, tabla_xlsx_path

    warn_raw = load_warnings()
    warn_bullets = summarize_warnings(warn_raw)

    return FinancieroBoard(
        status="ok",
        unit=data.get("unit") or "000 quetzales",
        source_path=data.get("source_path") or "",
        headline=headline,
        story=story,
        periods=periods,
        recent_periods=recent,
        focus_periods=focus,
        summary_cards=summary_cards,
        bu_table=bu_table,
        trend_activo={},
        trend_util={},
        util_compare=util_compare,
        risk_table=risk_table,
        strategy_notes=strategy_notes,
        projection_note=(
            f"qf extract: {qf.get('accounts', '?')} cuentas · "
            f"historia {qf.get('history_periods')} · forecast {qf.get('forecast_periods')}"
        ),
        qf_meta=qf,
        errors=errors,
        chart_activo=chart_activo,
        chart_util=chart_util,
        chart_riesgo=chart_riesgo,
        data_warnings=warn_bullets,
        warnings_count=int(warn_raw.get("count") or 0),
        has_tabla_xlsx=tabla_xlsx_path() is not None,
    )
