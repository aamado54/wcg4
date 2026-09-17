"""Stress test Noviembre 2026 — Midterms EUA · base agosto 2026."""

from __future__ import annotations

from typing import Any

from ..accounts import div_pref_ytd, preferentes_stock
from ..bands import evaluate_ratio
from ..indices import derived_metrics
from ..intermediacion import _intermediation_slice
from ..money import fmt_money
from ..utils import kpi_row, n, rates_from_meta

BASE_PERIOD = "2026-08"
FX_REF = 7.622
PROJECTION_MONTHS = ("2026-09", "2026-10", "2026-11", "2026-12")
USD_PASIVA_SHARE = 0.42  # fracción del pasivo sensible a depreciación (AP/PG USD)

DEFAULT_SHOCKS: dict[str, float] = {
    "fx_pct": 0.0,
    "rates_bp": 0.0,
    "mora_pct": 0.0,
    "withdrawals_pct": 0.0,
    "remittances_pct": 0.0,
    "recovery_pct": 0.0,
    "factoraje_mom_pct": -0.5,
}

PRESETS: dict[str, dict[str, Any]] = {
    "base": {
        "label": "Base",
        "hint": "Continuidad desde agosto; sin shock adicional.",
        **DEFAULT_SHOCKS,
    },
    "moderado": {
        "label": "Moderado",
        "hint": "Volatilidad electoral; presión cambiaria y fondeo contenidos.",
        "fx_pct": 5.0,
        "rates_bp": 150.0,
        "mora_pct": 25.0,
        "withdrawals_pct": 10.0,
        "remittances_pct": 5.0,
        "recovery_pct": 10.0,
        "factoraje_mom_pct": -1.0,
    },
    "severo": {
        "label": "Severo",
        "hint": "Crisis de confianza en bonos USA; liquidez bajo presión.",
        "fx_pct": 10.0,
        "rates_bp": 300.0,
        "mora_pct": 50.0,
        "withdrawals_pct": 20.0,
        "remittances_pct": 15.0,
        "recovery_pct": 20.0,
        "factoraje_mom_pct": -2.5,
    },
    "extremo": {
        "label": "Extremo",
        "hint": "Disrupción constitucional; retiros y tipo de cambio agresivos.",
        "fx_pct": 20.0,
        "rates_bp": 500.0,
        "mora_pct": 100.0,
        "withdrawals_pct": 35.0,
        "remittances_pct": 25.0,
        "recovery_pct": 35.0,
        "factoraje_mom_pct": -5.0,
    },
}


def parse_shock(raw: str | float | None, fallback: float) -> float:
    if raw is None or raw == "":
        return fallback
    try:
        return float(str(raw).strip().replace(",", ".").replace("%", ""))
    except (TypeError, ValueError):
        return fallback


def default_shocks() -> dict[str, float]:
    return dict(DEFAULT_SHOCKS)


def _prev_period(data: dict, period: str) -> str | None:
    periods = list(data.get("periods") or [])
    if period not in periods:
        return None
    idx = periods.index(period)
    return periods[idx - 1] if idx else None


def _base_slice(data: dict, bu: str = "T") -> dict[str, Any]:
    periods = list(data.get("periods") or [])
    if BASE_PERIOD not in periods:
        return {"status": "empty"}
    rates = rates_from_meta(data)
    prev = _prev_period(data, BASE_PERIOD)
    prev_row = kpi_row(data, bu, prev) if prev else {}
    prev_util_g = n(prev_row.get("utilidades")) - div_pref_ytd(data, bu, prev) if prev else None
    prev_util_c = n(prev_row.get("utilidades")) if prev else None
    sl = _intermediation_slice(
        data,
        bu,
        BASE_PERIOD,
        rates,
        "gerencial",
        prev_period=prev,
        prev_util_c=prev_util_c,
        prev_util_g=prev_util_g,
    )
    row = kpi_row(data, bu, BASE_PERIOD)
    pref = preferentes_stock(data, bu, BASE_PERIOD)
    div_y = div_pref_ytd(data, bu, BASE_PERIOD)
    m = derived_metrics(
        row, bu, BASE_PERIOD, rates, vista="gerencial", inv_proxy=pref, div_ytd=div_y
    )
    return {
        "status": "ok",
        "period": BASE_PERIOD,
        "slice": sl,
        "metrics": m,
        "rates": rates,
        "fx_ref": FX_REF,
    }


def _apply_shocks(
    base: dict[str, Any],
    shocks: dict[str, float],
) -> dict[str, float]:
    """Traduce drivers a impactos mensuales sobre margen, pasivo y activo."""
    sl = base["slice"]
    m = base["metrics"]
    fx = shocks["fx_pct"] / 100.0
    mora = shocks["mora_pct"] / 100.0
    rem = shocks["remittances_pct"] / 100.0
    wd = shocks["withdrawals_pct"] / 100.0
    rec = shocks["recovery_pct"] / 100.0
    rate_add = shocks["rates_bp"] / 10000.0

    cartera = n(sl.get("colocaciones"))
    captacion = n(sl.get("captaciones"))
    margen = n(sl.get("margen_bruto"))
    overhead = n(sl.get("overhead_neto"))
    ac = n(m.get("activo_corriente"))
    pc = n(m.get("pasivo_corriente_books") or m.get("pasivo_corriente"))
    pasivo = n(m.get("pasivo_books") or m.get("pasivo_total"))
    pat = n(m.get("patrimonio_books") or m.get("patrimonio"))

    # Costo de fondeo: tasa extra + repricing USD pasivas
    cost_up = captacion * rate_add / 12.0
    fx_pasivo_q = pasivo * USD_PASIVA_SHARE * fx
    fx_cost_month = fx_pasivo_q * 0.0025  # carry mensual aproximado del descalce

    # Ingreso: mora + remesas reducen yield efectivo (~60% factoraje expuesto)
    yield_loss = cartera * sl["tasa_activa"] / 12.0 * (mora * 0.45 + rem * 0.25)
    recovery_loss = cartera * 0.015 / 12.0 * rec  # 1.5% anual recuperación base

    margen_stress = margen - cost_up - fx_cost_month - yield_loss - recovery_loss

    # Retiros: sube PC, baja AC proporcionalmente
    wd_amt = captacion * wd
    ac1 = max(ac - wd_amt * 0.85, 1.0)
    pc1 = pc + wd_amt + fx_pasivo_q * 0.15
    liq1 = ac1 / pc1 if pc1 else None

    util_stress = margen_stress - overhead

    return {
        "margen_stress": margen_stress,
        "util_stress": util_stress,
        "liquidez_stress": liq1,
        "ac_stress": ac1,
        "pc_stress": pc1,
        "pasivo_fx_delta": fx_pasivo_q,
        "cost_rate_delta": cost_up,
        "yield_loss": yield_loss,
        "recovery_loss": recovery_loss,
        "withdrawal_amt": wd_amt,
        "patrimonio": pat,
        "apalancamiento_stress": (pasivo + fx_pasivo_q + wd_amt) / pat if pat else None,
    }


def _project_horizon(
    base: dict[str, Any],
    shocks: dict[str, float],
    stressed: dict[str, float],
) -> dict[str, Any]:
    sl = base["slice"]
    mom = shocks.get("factoraje_mom_pct", 0.0) / 100.0
    cartera = n(sl.get("colocaciones"))
    liq = stressed.get("liquidez_stress") or n(base["metrics"].get("liquidez"))
    util_m = stressed.get("util_stress") or 0.0
    margen_m = stressed.get("margen_stress") or 0.0

    labels = list(PROJECTION_MONTHS)
    util_series = []
    liq_series = []
    cartera_series = []
    cum_util = 0.0
    for i, lab in enumerate(labels):
        cartera *= 1 + mom
        # Noviembre: shock electoral adicional leve
        bump = 1.08 if lab == "2026-11" and shocks.get("fx_pct", 0) >= 5 else 1.0
        u = util_m * bump
        cum_util += u
        liq *= 0.995 if u < 0 else 1.002
        if shocks.get("withdrawals_pct", 0) > 15 and lab in ("2026-11", "2026-12"):
            liq *= 0.97
        util_series.append(round(u, 2))
        liq_series.append(round(liq, 3) if liq else None)
        cartera_series.append(round(cartera, 2))

    return {
        "labels": labels,
        "utilidad_mes": util_series,
        "utilidad_acum_q4": round(cum_util, 2),
        "liquidez": liq_series,
        "cartera": cartera_series,
        "midterm_month": "2026-11",
    }


def _fx_matrix(base: dict[str, Any], shocks: dict[str, float]) -> list[dict[str, Any]]:
    rows = []
    for fx in (0, 5, 10, 15, 20):
        s = {**shocks, "fx_pct": float(fx)}
        st = _apply_shocks(base, s)
        liq_ev = evaluate_ratio("liquidez", st.get("liquidez_stress"))
        spread_need = max(0.0, 2.0 + fx * 0.08 + shocks.get("rates_bp", 0) / 100.0)
        rows.append(
            {
                "fx_pct": fx,
                "usd_gtq": round(FX_REF * (1 + fx / 100.0), 4),
                "liquidez": st.get("liquidez_stress"),
                "liquidez_display": f"{st['liquidez_stress']:.2f}×" if st.get("liquidez_stress") else "—",
                "liquidez_tone": liq_ev.get("tone"),
                "min_spread_pp": round(spread_need, 2),
                "liquidity_buffer_000": round(max(0, 1.25 - (st.get("liquidez_stress") or 0)) * n(base["metrics"].get("pasivo_corriente_books")) * 0.1, 0),
                "util_mes": round(st.get("util_stress") or 0, 0),
            }
        )
    return rows


def _precautions(stressed: dict[str, float], shocks: dict[str, float]) -> list[str]:
    out: list[str] = []
    liq = stressed.get("liquidez_stress")
    if liq is not None and liq < 1.25:
        out.append(
            f"Mantener colchón de liquidez: liquidez estresada {liq:.2f}× "
            f"(banda de alerta 1.20×). Activar calendario diario de vencimientos."
        )
    if shocks.get("withdrawals_pct", 0) >= 15:
        out.append(
            "Confirmar líneas back-to-back bancarias y cupos prenegociados antes de midterms; "
            "no contar líneas no probadas operacionalmente."
        )
    if shocks.get("fx_pct", 0) >= 10:
        out.append(
            "Reducir descalce: limitar créditos en USD a clientes sin ingreso en dólares; "
            f"repricing pasivo USD (~{USD_PASIVA_SHARE:.0%} del pasivo sensible)."
        )
    if shocks.get("factoraje_mom_pct", 0) < -1:
        out.append(
            "Pivot factoraje: tratar rampa con anclas como fase de inversión — "
            "presupuestar utilidad negativa 2–3 trimestres mientras sale cartera legacy."
        )
    if (stressed.get("util_stress") or 0) < 0:
        out.append(
            "Utilidad mensual estresada negativa: congelar crecimiento especulativo en bonos largos "
            "y priorizar cobranza sobre originación."
        )
    if not out:
        out.append(
            "Postura defensiva prudente: monitoreo semanal de FX, mora y retiros; "
            "sin señales de stress extremo en este escenario."
        )
    return out


def build_nov2026_board(
    data: dict,
    shocks: dict[str, float] | None = None,
    bu: str = "T",
    ccy: str = "GTQ",
    fx: float | None = None,
) -> dict[str, Any]:
    base = _base_slice(data, bu=bu)
    if base.get("status") != "ok":
        return {"status": "empty"}

    s = {**DEFAULT_SHOCKS, **(shocks or {})}
    stressed = _apply_shocks(base, s)
    projection = _project_horizon(base, s, stressed)
    fx_matrix = _fx_matrix(base, s)

    fm = lambda v, d=0: fmt_money(v, ccy, fx, d)
    sl = base["slice"]
    m = base["metrics"]
    liq_base = evaluate_ratio("liquidez", m.get("liquidez"))
    liq_st = evaluate_ratio("liquidez", stressed.get("liquidez_stress"))
    apa_base = evaluate_ratio("apalancamiento", m.get("apalancamiento"))
    apa_st = evaluate_ratio("apalancamiento", stressed.get("apalancamiento_stress"))
    z_ev = evaluate_ratio("z_score", m.get("z_score"))

    preset_rows = []
    for key, preset in PRESETS.items():
        ps = {**DEFAULT_SHOCKS, **{k: v for k, v in preset.items() if k in DEFAULT_SHOCKS}}
        pst = _apply_shocks(base, ps)
        proj = _project_horizon(base, ps, pst)
        preset_rows.append(
            {
                "id": key,
                "label": preset["label"],
                "hint": preset.get("hint", ""),
                "util_q4": proj["utilidad_acum_q4"],
                "util_q4_display": fm(proj["utilidad_acum_q4"]),
                "liquidez_nov": proj["liquidez"][2] if len(proj["liquidez"]) > 2 else None,
                "liquidez_nov_display": (
                    f"{proj['liquidez'][2]:.2f}×" if proj.get("liquidez") and proj["liquidez"][2] else "—"
                ),
                "util_mes": pst.get("util_stress"),
                "util_mes_display": fm(pst.get("util_stress")),
            }
        )

    return {
        "status": "ok",
        "bu": bu,
        "base_period": BASE_PERIOD,
        "fx_ref": FX_REF,
        "usd_pasiva_share": USD_PASIVA_SHARE,
        "drivers": s,
        "base_cards": [
            {"label": "Cartera", "value": fm(sl["colocaciones"]), "hint": "Factoraje + leasing · ago-26"},
            {"label": "Liquidez AC/PC", "value": f"{m['liquidez']:.2f}×", "tone": liq_base["tone"], "hint": liq_base["zone"]},
            {"label": "Apalancamiento", "value": f"{m['apalancamiento']:.2f}×", "tone": apa_base["tone"], "hint": apa_base["zone"]},
            {"label": "Util. ger. mes", "value": fm(sl["utilidad"]), "hint": "Flujo agosto post div. pref."},
            {"label": "Margen bruto mes", "value": fm(sl["margen_bruto"]), "hint": f"Spread {sl['spread']*100:.1f} pp"},
            {"label": "Z NBFI", "value": f"{m['z_score']:.2f}", "tone": z_ev["tone"], "hint": z_ev["zone"]},
        ],
        "strategy_flags": [
            {
                "title": "Factoraje en transición",
                "body": "Cartera F ~388M (000) con utilidad mensual volátil; salida de Faktorlab e "
                "inicio de anclas implica fase tipo startup — riesgo de utilidad negativa en rampa.",
                "tone": "warn",
            },
            {
                "title": "Inversiones sostienen cash flow",
                "body": "Pasivas AP/PG ~USD 64M (jul-26) con crecimiento neto positivo; "
                "endeudamiento y apalancamiento requieren back-to-back bancario para pagar cupones.",
                "tone": "warn",
            },
            {
                "title": "Posición agosto",
                "body": f"Liquidez {m['liquidez']:.2f}× y Z {m['z_score']:.2f} — holgura moderada, "
                "no holgura para shock prolongado sin medidas.",
                "tone": "ok" if (m.get("liquidez") or 0) >= 1.5 else "warn",
            },
        ],
        "stressed": {
            **stressed,
            "util_display": fm(stressed.get("util_stress")),
            "margen_display": fm(stressed.get("margen_stress")),
            "liquidez_display": (
                f"{stressed['liquidez_stress']:.2f}×" if stressed.get("liquidez_stress") else "—"
            ),
            "liquidez_tone": liq_st["tone"],
            "apalancamiento_display": (
                f"{stressed['apalancamiento_stress']:.2f}×"
                if stressed.get("apalancamiento_stress")
                else "—"
            ),
            "apalancamiento_tone": apa_st["tone"],
        },
        "impact_rows": [
            {"label": "↑ costo fondeo (tasas)", "value": fm(stressed["cost_rate_delta"])},
            {"label": "↑ carry FX pasivo USD", "value": fm(stressed["pasivo_fx_delta"] * 0.0025)},
            {"label": "↓ yield (mora + remesas)", "value": fm(-stressed["yield_loss"])},
            {"label": "↓ recuperación cartera", "value": fm(-stressed["recovery_loss"])},
            {"label": "Retiros simulados", "value": fm(stressed["withdrawal_amt"])},
        ],
        "projection": projection,
        "chart_projection": {
            "labels": projection["labels"],
            "datasets": [
                {
                    "label": "Utilidad mensual estresada",
                    "data": projection["utilidad_mes"],
                    "borderColor": "#1e4d3a",
                    "backgroundColor": "#1e4d3a33",
                    "yAxisID": "y",
                    "tension": 0.25,
                },
                {
                    "label": "Liquidez",
                    "data": projection["liquidez"],
                    "borderColor": "#2f6f9f",
                    "borderDash": [6, 4],
                    "yAxisID": "y1",
                    "tension": 0.25,
                },
            ],
        },
        "fx_matrix": fx_matrix,
        "preset_rows": preset_rows,
        "precautions": _precautions(stressed, s),
        "presets": PRESETS,
    }
