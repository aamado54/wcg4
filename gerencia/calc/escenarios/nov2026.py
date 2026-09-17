"""Stress test Noviembre 2026 — Midterms EUA · base agosto 2026."""

from __future__ import annotations

from typing import Any

from ..accounts import div_pref_ytd, line, preferentes_stock
from ..bands import evaluate_ratio
from ..indices import derived_metrics
from ..intermediacion import _intermediation_slice
from ..money import fmt_money
from ..utils import kpi_row, n, rates_from_meta

BASE_PERIOD = "2026-08"
ELECTION_DATE = "2026-11-03"
FX_REF = 7.622
USD_PASIVA_SHARE = 0.42
BANK_PASIVO_CODES = ("202010104", "202010106", "202010108", "202010111", "202010112")
PAGARES_CODE = "201010106"

DEFAULT_SHOCKS: dict[str, float] = {
    "fx_pct": 0.0,
    "rates_bp": 0.0,
    "mora_pct": 0.0,
    "withdrawals_pct": 0.0,
    "remittances_pct": 0.0,
    "recovery_pct": 0.0,
    "factoraje_mom_pct": 0.0,
}

# Sep–oct preparación; nov apertura tardía; dic–ene crisis; feb–jul secuela (~6 meses).
TIMELINE: list[tuple[str, str, float, str]] = [
    ("2026-09", "prep", 0.0, "Preparación"),
    ("2026-10", "prep", 0.0, "Preparación"),
    ("2026-11", "apertura", 0.35, "Midterms 3 nov · shock tardío"),
    ("2026-12", "crisis", 1.0, "Crisis"),
    ("2027-01", "crisis", 1.0, "Crisis"),
    ("2027-02", "secuela", 0.85, "Secuela"),
    ("2027-03", "secuela", 0.75, "Secuela"),
    ("2027-04", "secuela", 0.65, "Secuela"),
    ("2027-05", "secuela", 0.58, "Secuela"),
    ("2027-06", "secuela", 0.52, "Secuela"),
    ("2027-07", "secuela", 0.48, "Secuela"),
]

VIVO_PRESETS: dict[str, dict[str, Any]] = {
    "moderado": {
        "label": "Vivo moderado",
        "fx_pct": 5.0,
        "rates_bp": 150.0,
        "mora_pct": 25.0,
        "withdrawals_pct": 10.0,
        "remittances_pct": 5.0,
        "recovery_pct": 10.0,
        "factoraje_mom_pct": -1.0,
    },
    "severo": {
        "label": "Vivo severo",
        "fx_pct": 10.0,
        "rates_bp": 300.0,
        "mora_pct": 50.0,
        "withdrawals_pct": 20.0,
        "remittances_pct": 15.0,
        "recovery_pct": 20.0,
        "factoraje_mom_pct": -2.5,
    },
    "extremo": {
        "label": "Vivo extremo",
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


def _bus(bu: str) -> tuple[str, ...]:
    bu = (bu or "T").upper()
    return ("F", "L") if bu == "T" else (bu,)


def _prev_period(data: dict, period: str) -> str | None:
    periods = list(data.get("periods") or [])
    if period not in periods:
        return None
    idx = periods.index(period)
    return periods[idx - 1] if idx else None


def _pagares_stock(data: dict, bu: str, period: str) -> float:
    return sum(line(data, b, PAGARES_CODE, period) for b in _bus(bu))


def _bancos_pasivo(data: dict, bu: str, period: str) -> float:
    return sum(
        line(data, b, code, period) for b in _bus(bu) for code in BANK_PASIVO_CODES
    )


def _base_context(data: dict, bu: str = "T") -> dict[str, Any]:
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
    m_cont = derived_metrics(
        row, bu, BASE_PERIOD, rates, vista="contable", inv_proxy=pref, div_ytd=div_y
    )
    m_ger = derived_metrics(
        row, bu, BASE_PERIOD, rates, vista="gerencial", inv_proxy=pref, div_ytd=div_y
    )
    m_strict = derived_metrics(
        row, bu, BASE_PERIOD, rates, vista="gerencial", inv_proxy=pref, div_ytd=div_y, strict=True
    )
    return {
        "status": "ok",
        "period": BASE_PERIOD,
        "slice": sl,
        "metrics": m_ger,
        "metrics_cont": m_cont,
        "metrics_strict": m_strict,
        "rates": rates,
        "pref": pref,
        "div_ytd": div_y,
    }


def _mini_balance(
    ctx: dict[str, Any],
    data: dict,
    bu: str,
    fm,
    *,
    ac: float | None = None,
    pc: float | None = None,
    pasivo_extra: float = 0.0,
) -> dict[str, Any]:
    period = ctx["period"]
    row = kpi_row(data, bu, period)
    m = ctx["metrics"]
    ac_v = ac if ac is not None else n(m.get("activo_corriente"))
    pc_v = pc if pc is not None else n(m.get("pasivo_corriente_books") or m.get("pasivo_corriente"))
    pasivo_books = n(m.get("pasivo_books") or m.get("pasivo_total")) + pasivo_extra
    activo = n(row.get("activo")) or (n(row.get("activo_corriente")) + n(row.get("activo_no_corriente")))
    cartera = n(m.get("cartera"))
    pref = ctx["pref"]
    pagares = _pagares_stock(data, bu, period)
    bancos = _bancos_pasivo(data, bu, period)
    liq = ac_v / pc_v if pc_v else m.get("liquidez")
    return {
        "activos": [
            {"label": "Colocaciones (cartera)", "value": fm(cartera)},
            {"label": "Activo total", "value": fm(activo)},
        ],
        "pasivos": [
            {"label": "Pagarés AP/PG (201010106)", "value": fm(pagares)},
            {"label": "Acciones preferentes (301010106)", "value": fm(pref)},
            {"label": "Préstamos bancos (pasivo)", "value": fm(bancos)},
            {"label": "Pasivo total (libros)", "value": fm(pasivo_books)},
            {"label": "Fondeo total (Pas.+Pref.)", "value": fm(pasivo_books + pref)},
        ],
        "liquidez": liq,
        "liquidez_display": f"{liq:.2f}×" if liq is not None else "—",
    }


def _mini_results(ctx: dict[str, Any], fm) -> list[dict[str, str]]:
    mc = ctx["metrics_cont"]
    mg = ctx["metrics"]
    ms = ctx["metrics_strict"]
    year = BASE_PERIOD[:4]
    return [
        {
            "label": f"Utilidad acum. contable ({year})",
            "value": fm(mc.get("utilidades")),
            "hint": "Cuenta 302 · saldo YTD",
        },
        {
            "label": f"Utilidad acum. gerencial ({year})",
            "value": fm(mg.get("util_vista")),
            "hint": "302 − dividendos preferentes (102020301)",
        },
        {
            "label": f"Utilidad acum. ger. estricta ({year})",
            "value": fm(ms.get("util_vista")),
            "hint": "Igual util.; preferentes reclasificados a pasivo a 1 año",
        },
    ]


def _scaled_shocks(shocks: dict[str, float], factor: float) -> dict[str, float]:
    if factor <= 0:
        return dict(DEFAULT_SHOCKS)
    return {k: float(shocks.get(k, 0.0)) * factor for k in DEFAULT_SHOCKS}


def _monthly_stress(ctx: dict[str, Any], shocks: dict[str, float]) -> dict[str, float]:
    sl = ctx["slice"]
    m = ctx["metrics"]
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

    cost_up = captacion * rate_add / 12.0
    fx_pasivo_q = pasivo * USD_PASIVA_SHARE * fx
    fx_cost_month = fx_pasivo_q * 0.0025
    yield_loss = cartera * sl["tasa_activa"] / 12.0 * (mora * 0.45 + rem * 0.25)
    recovery_loss = cartera * 0.015 / 12.0 * rec
    margen_stress = margen - cost_up - fx_cost_month - yield_loss - recovery_loss
    wd_amt = captacion * wd
    ac1 = max(ac - wd_amt * 0.85, 1.0)
    pc1 = pc + wd_amt + fx_pasivo_q * 0.15
    liq1 = ac1 / pc1 if pc1 else None
    util_stress = margen_stress - overhead
    base_util = n(sl.get("utilidad"))

    return {
        "util_base": base_util,
        "util_stress": util_stress,
        "liquidez_base": n(m.get("liquidez")),
        "liquidez_stress": liq1,
        "ac": ac1,
        "pc": pc1,
        "pasivo_extra": fx_pasivo_q * 0.15 + wd_amt,
        "margen_stress": margen_stress,
    }


def _simulate_timeline(ctx: dict[str, Any], shocks: dict[str, float]) -> dict[str, Any]:
    sl = ctx["slice"]
    mom = shocks.get("factoraje_mom_pct", 0.0) / 100.0
    full = _monthly_stress(ctx, shocks)

    ac = n(ctx["metrics"].get("activo_corriente"))
    pc = n(ctx["metrics"].get("pasivo_corriente_books") or ctx["metrics"].get("pasivo_corriente"))
    liq = n(ctx["metrics"].get("liquidez"))
    cartera = n(sl.get("colocaciones"))
    util_base = n(sl.get("utilidad"))

    labels: list[str] = []
    phases: list[str] = []
    phase_labels: list[str] = []
    utils: list[float] = []
    liqs: list[float | None] = []
    pasivo_extra = 0.0

    for period, phase, factor, phase_label in TIMELINE:
        labels.append(period)
        phases.append(phase)
        phase_labels.append(phase_label)
        cartera *= 1 + mom

        if factor <= 0:
            u = util_base
        else:
            eff = _scaled_shocks(shocks, factor)
            st = _monthly_stress(ctx, eff)
            u = util_base + (st["util_stress"] - util_base)
            pasivo_extra = st["pasivo_extra"]
            ac = st["ac"]
            pc = st["pc"]
            liq = st["liquidez_stress"]

        utils.append(round(u, 2))
        liqs.append(round(liq, 3) if liq is not None else None)

    crisis_util = sum(
        u for (_, ph, f, _), u in zip(TIMELINE, utils) if ph in ("crisis", "apertura") and f > 0
    )
    peak_liq = min(x for x in liqs if x is not None) if liqs else None
    jan_idx = next(i for i, (p, _, _, _) in enumerate(TIMELINE) if p == "2027-01")

    return {
        "labels": labels,
        "phases": phases,
        "phase_labels": phase_labels,
        "utilidad": utils,
        "liquidez": liqs,
        "util_crisis_acum": round(crisis_util, 2),
        "liquidez_min": peak_liq,
        "liquidez_crisis": liqs[jan_idx] if jan_idx < len(liqs) else None,
        "end_ac": ac,
        "end_pc": pc,
        "end_pasivo_extra": pasivo_extra,
    }


def _compare_row(label: str, base_val, vivo_val, *, display_fn, lower_is_worse=False) -> dict:
    b = display_fn(base_val)
    v = display_fn(vivo_val)
    delta = None
    if isinstance(base_val, (int, float)) and isinstance(vivo_val, (int, float)):
        delta = vivo_val - base_val
    tone = "ok"
    if delta is not None:
        if lower_is_worse and delta < 0:
            tone = "risk"
        elif not lower_is_worse and delta < 0:
            tone = "warn"
    delta_display = "—"
    if delta is not None:
        if isinstance(base_val, (int, float)) and abs(base_val) < 20 and abs(vivo_val or 0) < 20:
            delta_display = f"{delta:+.2f}"
        else:
            delta_display = display_fn(delta) if delta else f"{delta:+.0f}"
    return {"label": label, "base": b, "vivo": v, "delta": delta, "delta_display": delta_display, "tone": tone}


def _precautions(vivo: dict[str, float], sim_vivo: dict[str, Any]) -> list[str]:
    out: list[str] = []
    liq = sim_vivo.get("liquidez_min")
    if liq is not None and liq < 1.25:
        out.append(
            f"Escenario vivo: liquidez mínima simulada {liq:.2f}× en la ventana nov–jul. "
            "Activar war room de liquidez y calendario diario de vencimientos."
        )
    if vivo.get("withdrawals_pct", 0) >= 10:
        out.append(
            "Sep–oct (ahora): confirmar back-to-backs y líneas bancarias antes del 3 nov; "
            "no contar cupos no probados."
        )
    if vivo.get("fx_pct", 0) >= 8:
        out.append(
            "Reducir descalce USD/GTQ en cartera y exigir cobertura a clientes importadores."
        )
    if sim_vivo.get("util_crisis_acum", 0) < 0:
        out.append(
            "Utilidad acumulada negativa en ventana de crisis: priorizar cobranza y congelar "
            "riesgo especulativo en bonos largos."
        )
    if not out:
        out.append(
            "Sep–oct: usar los dos meses de preparación para alinear tesorería; "
            "el escenario vivo no dispara alertas extremas con los drivers actuales."
        )
    return out


def build_nov2026_board(
    data: dict,
    shocks_base: dict[str, float] | None = None,
    shocks_vivo: dict[str, float] | None = None,
    bu: str = "T",
    ccy: str = "GTQ",
    fx: float | None = None,
) -> dict[str, Any]:
    ctx = _base_context(data, bu=bu)
    if ctx.get("status") != "ok":
        return {"status": "empty"}

    sb = {**DEFAULT_SHOCKS, **(shocks_base or {})}
    sv = {**DEFAULT_SHOCKS, **(shocks_vivo or {})}
    fm = lambda v, d=0: fmt_money(v, ccy, fx, d)

    mini_bg = _mini_balance(ctx, data, bu, fm)
    mini_res = _mini_results(ctx, fm)
    sim_base = _simulate_timeline(ctx, sb)
    sim_vivo = _simulate_timeline(ctx, sv)

    balance_rows = []
    pas = mini_bg["pasivos"]
    for i, act in enumerate(mini_bg["activos"]):
        pas_row = pas[i] if i < len(pas) else {"label": "", "value": ""}
        balance_rows.append(
            {
                "activo_label": act["label"],
                "activo_value": act["value"],
                "pasivo_label": pas_row["label"],
                "pasivo_value": pas_row["value"],
            }
        )
    for j in range(len(mini_bg["activos"]), len(pas)):
        balance_rows.append(
            {
                "activo_label": "",
                "activo_value": "",
                "pasivo_label": pas[j]["label"],
                "pasivo_value": pas[j]["value"],
            }
        )

    bg_base_crisis = _mini_balance(
        ctx, data, bu, fm, ac=sim_base["end_ac"], pc=sim_base["end_pc"], pasivo_extra=0
    )
    bg_vivo_crisis = _mini_balance(
        ctx,
        data,
        bu,
        fm,
        ac=sim_vivo["end_ac"],
        pc=sim_vivo["end_pc"],
        pasivo_extra=sim_vivo["end_pasivo_extra"],
    )

    liq_base_ev = evaluate_ratio("liquidez", sim_base.get("liquidez_min"))
    liq_vivo_ev = evaluate_ratio("liquidez", sim_vivo.get("liquidez_min"))

    compare_rows = [
        _compare_row(
            "Liquidez mínima (nov–jul)",
            sim_base.get("liquidez_min"),
            sim_vivo.get("liquidez_min"),
            display_fn=lambda x: f"{x:.2f}×" if x is not None else "—",
            lower_is_worse=True,
        ),
        _compare_row(
            "Liquidez ene-2027",
            sim_base.get("liquidez_crisis"),
            sim_vivo.get("liquidez_crisis"),
            display_fn=lambda x: f"{x:.2f}×" if x is not None else "—",
            lower_is_worse=True,
        ),
        _compare_row(
            "Util. acum. crisis (nov–ene)",
            sim_base.get("util_crisis_acum"),
            sim_vivo.get("util_crisis_acum"),
            display_fn=lambda x: fm(x),
        ),
        _compare_row(
            "Util. prom. mes estresado",
            _monthly_stress(ctx, sb).get("util_stress"),
            _monthly_stress(ctx, sv).get("util_stress"),
            display_fn=lambda x: fm(x),
        ),
    ]

    chart = {
        "labels": sim_vivo["labels"],
        "phases": sim_vivo["phases"],
        "datasets": [
            {
                "label": "Liquidez · escenario base",
                "data": sim_base["liquidez"],
                "borderColor": "#9aa8b5",
                "borderDash": [5, 5],
                "yAxisID": "y",
                "tension": 0.2,
            },
            {
                "label": "Liquidez · escenario vivo",
                "data": sim_vivo["liquidez"],
                "borderColor": "#2f6f9f",
                "borderWidth": 2,
                "yAxisID": "y",
                "tension": 0.2,
            },
            {
                "label": "Utilidad · escenario base",
                "data": sim_base["utilidad"],
                "borderColor": "#b8c4bc",
                "borderDash": [4, 4],
                "yAxisID": "y1",
                "tension": 0.2,
            },
            {
                "label": "Utilidad · escenario vivo",
                "data": sim_vivo["utilidad"],
                "borderColor": "#1e4d3a",
                "borderWidth": 2,
                "yAxisID": "y1",
                "tension": 0.2,
            },
        ],
    }

    return {
        "status": "ok",
        "bu": bu,
        "base_period": BASE_PERIOD,
        "election_date": ELECTION_DATE,
        "fx_ref": FX_REF,
        "timeline_note": (
            "Nada ocurre en sep–oct: son meses de preparación. El stress arranca en noviembre "
            "(midterms 3 nov; hipótesis de escalada tardía), pico dic–ene, y secuela ~6 meses."
        ),
        "shocks_base": sb,
        "shocks_vivo": sv,
        "mini_balance": mini_bg,
        "mini_balance_rows": balance_rows,
        "mini_results": mini_res,
        "mini_balance_base_crisis": bg_base_crisis,
        "mini_balance_vivo_crisis": bg_vivo_crisis,
        "compare_rows": compare_rows,
        "sim_base": sim_base,
        "sim_vivo": sim_vivo,
        "chart_timeline": chart,
        "vivo_presets": VIVO_PRESETS,
        "precautions": _precautions(sv, sim_vivo),
        "liq_vivo_tone": liq_vivo_ev.get("tone"),
        "liq_base_tone": liq_base_ev.get("tone"),
    }


# Compatibilidad con imports previos
PRESETS = {"base": {"label": "Base", **DEFAULT_SHOCKS}, **VIVO_PRESETS}
