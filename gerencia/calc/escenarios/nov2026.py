"""Stress test Noviembre 2026 — Midterms EUA · base agosto 2026."""

from __future__ import annotations

from typing import Any

from ..accounts import div_pref_ytd, line, pagares_month, preferentes_stock
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

MODERADO_SHOCKS = {
    "fx_pct": 5.0,
    "rates_bp": 150.0,
    "mora_pct": 25.0,
    "withdrawals_pct": 10.0,
    "remittances_pct": 5.0,
    "recovery_pct": 10.0,
    "factoraje_mom_pct": -1.0,
}

BASE_PRESETS: dict[str, dict[str, Any]] = {
    "cero": {"label": "Base cero", **DEFAULT_SHOCKS},
    "moderado": {"label": "Base moderado", **MODERADO_SHOCKS},
}

VIVO_PRESETS: dict[str, dict[str, Any]] = {
    "moderado": {"label": "Vivo moderado", **MODERADO_SHOCKS},
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

DRIVER_FIELDS: list[dict[str, Any]] = [
    {"key": "fx_pct", "label": "USD/GTQ (+dep.)", "min": 0, "max": 25, "step": 0.5, "suffix": "%"},
    {"key": "rates_bp", "label": "Tasas fondeo (+pb)", "min": 0, "max": 600, "step": 25, "suffix": ""},
    {"key": "mora_pct", "label": "Mora (+)", "min": 0, "max": 100, "step": 5, "suffix": "%"},
    {"key": "withdrawals_pct", "label": "Retiros pasivas (+)", "min": 0, "max": 40, "step": 5, "suffix": "%"},
    {"key": "remittances_pct", "label": "Caída remesas (+)", "min": 0, "max": 30, "step": 5, "suffix": "%"},
    {"key": "recovery_pct", "label": "Recup. cartera (−)", "min": 0, "max": 40, "step": 5, "suffix": "%"},
    {"key": "factoraje_mom_pct", "label": "Colocaciones / mes", "min": -8, "max": 3, "step": 0.5, "suffix": "%"},
]


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


def _pagares_ytd(data: dict, bu: str, period: str) -> float:
    year = (period or "")[:4]
    total = 0.0
    for p in data.get("periods") or []:
        if str(p).startswith(year) and str(p) <= period:
            total += pagares_month(data, bu, p)
    return total


def _mini_balance(
    ctx: dict[str, Any],
    data: dict,
    bu: str,
    fm,
    *,
    ac: float | None = None,
    pc: float | None = None,
    pasivo_extra: float = 0.0,
    cartera_override: float | None = None,
) -> dict[str, Any]:
    period = ctx["period"]
    row = kpi_row(data, bu, period)
    m = ctx["metrics"]
    ac_v = ac if ac is not None else n(m.get("activo_corriente"))
    pc_v = pc if pc is not None else n(m.get("pasivo_corriente_books") or m.get("pasivo_corriente"))
    pasivo_books = n(m.get("pasivo_books") or m.get("pasivo_total")) + pasivo_extra
    activo = n(row.get("activo")) or (n(row.get("activo_corriente")) + n(row.get("activo_no_corriente")))
    base_cartera = n(m.get("cartera"))
    cartera = cartera_override if cartera_override is not None else base_cartera
    if cartera_override is not None and base_cartera:
        activo = activo * (cartera / base_cartera)
    pref = ctx["pref"]
    pagares = _pagares_stock(data, bu, period)
    bancos = _bancos_pasivo(data, bu, period)
    liq = ac_v / pc_v if pc_v else m.get("liquidez")

    def _line(label: str, raw: float) -> dict[str, Any]:
        return {"label": label, "value": fm(raw), "raw": raw}

    return {
        "activos": [
            _line("Colocaciones (cartera)", cartera),
            _line("Activo total", activo),
        ],
        "pasivos": [
            _line("Pagarés AP/PG (201010106)", pagares),
            _line("Acciones preferentes (301010106)", pref),
            _line("Préstamos bancos (pasivo)", bancos),
            _line("Pasivo total (libros)", pasivo_books),
            _line("Fondeo total (Pas.+Pref.)", pasivo_books + pref),
        ],
        "liquidez": liq,
        "liquidez_display": f"{liq:.2f}×" if liq is not None else "—",
    }


def _mini_results(ctx: dict[str, Any], data: dict, bu: str, fm) -> list[dict[str, str]]:
    mc = ctx["metrics_cont"]
    mg = ctx["metrics"]
    ms = ctx["metrics_strict"]
    div_y = ctx["div_ytd"]
    pag_y = _pagares_ytd(data, bu, BASE_PERIOD)
    year = BASE_PERIOD[:4]
    return [
        {
            "label": f"Utilidad acum. contable ({year})",
            "value": fm(mc.get("utilidades")),
            "hint": (
                f"Saldo YTD cuenta 302. Los intereses a pagarés ({fm(pag_y)}) ya están en libros; "
                f"los dividendos a preferentes no restan aquí."
            ),
        },
        {
            "label": f"Utilidad acum. gerencial ({year})",
            "value": fm(mg.get("util_vista")),
            "hint": (
                f"302 menos dividendos preferentes acumulados ({fm(div_y)}), pagados mes a mes. "
                f"Esa diferencia existe siempre, no espera la vista estricta."
            ),
        },
        {
            "label": f"Utilidad acum. ger. estricta ({year})",
            "value": fm(ms.get("util_vista")),
            "hint": (
                "Misma utilidad que la gerencial. Solo reclasifica preferentes (301010106) "
                "de patrimonio a pasivo a un año — ejercicio de balance, no de resultados."
            ),
        },
    ]


def _scaled_shocks(shocks: dict[str, float], factor: float) -> dict[str, float]:
    if factor <= 0:
        return dict(DEFAULT_SHOCKS)
    return {k: float(shocks.get(k, 0.0)) * factor for k in DEFAULT_SHOCKS}


def _monthly_stress(
    ctx: dict[str, Any],
    shocks: dict[str, float],
    *,
    cartera: float | None = None,
    captacion: float | None = None,
) -> dict[str, float]:
    sl = ctx["slice"]
    m = ctx["metrics"]
    fx = shocks["fx_pct"] / 100.0
    mora = shocks["mora_pct"] / 100.0
    rem = shocks["remittances_pct"] / 100.0
    wd = shocks["withdrawals_pct"] / 100.0
    rec = shocks["recovery_pct"] / 100.0
    rate_add = shocks["rates_bp"] / 10000.0

    base_cartera = n(sl.get("colocaciones")) or 1.0
    base_capt = n(sl.get("captaciones")) or 1.0
    cartera_v = base_cartera if cartera is None else cartera
    captacion_v = base_capt if captacion is None else captacion
    scale = cartera_v / base_cartera

    margen = n(sl.get("margen_bruto")) * scale
    overhead = n(sl.get("overhead_neto"))
    base_ac = n(m.get("activo_corriente")) * scale
    pc = n(m.get("pasivo_corriente_books") or m.get("pasivo_corriente"))
    pasivo = (n(m.get("pasivo_books") or m.get("pasivo_total"))) * (captacion_v / base_capt)

    cost_up = captacion_v * rate_add / 12.0
    fx_pasivo_q = pasivo * USD_PASIVA_SHARE * fx
    fx_cost_month = fx_pasivo_q * 0.0025
    yield_loss = cartera_v * sl["tasa_activa"] / 12.0 * (mora * 0.45 + rem * 0.25)
    recovery_loss = cartera_v * 0.015 / 12.0 * rec
    margen_stress = margen - cost_up - fx_cost_month - yield_loss - recovery_loss
    wd_amt = captacion_v * wd
    ac1 = max(base_ac - wd_amt * 0.85, 1.0)
    pc1 = pc + wd_amt + fx_pasivo_q * 0.15
    liq1 = ac1 / pc1 if pc1 else None
    util_stress = margen_stress - overhead
    base_util = n(sl.get("utilidad")) * scale

    return {
        "util_base": base_util,
        "util_stress": util_stress,
        "liquidez_base": n(m.get("liquidez")),
        "liquidez_stress": liq1,
        "ac": ac1,
        "pc": pc1,
        "pasivo_extra": fx_pasivo_q * 0.15 + wd_amt,
        "margen_stress": margen_stress,
        "cartera": cartera_v,
    }


def _simulate_timeline(ctx: dict[str, Any], shocks: dict[str, float]) -> dict[str, Any]:
    sl = ctx["slice"]
    mom = shocks.get("factoraje_mom_pct", 0.0) / 100.0

    ac = n(ctx["metrics"].get("activo_corriente"))
    pc = n(ctx["metrics"].get("pasivo_corriente_books") or ctx["metrics"].get("pasivo_corriente"))
    liq = n(ctx["metrics"].get("liquidez"))
    cartera = n(sl.get("colocaciones"))
    captacion = n(sl.get("captaciones"))

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
        captacion *= 1 + mom

        if factor <= 0:
            st = _monthly_stress(ctx, DEFAULT_SHOCKS, cartera=cartera, captacion=captacion)
            u = st["util_stress"]
            ac = st["ac"]
            pc = st["pc"]
            liq = st["liquidez_stress"]
        else:
            eff = _scaled_shocks(shocks, factor)
            st = _monthly_stress(ctx, eff, cartera=cartera, captacion=captacion)
            u = st["util_stress"]
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
        "end_cartera": cartera,
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


def _diff_cell(base_raw: float | None, vivo_raw: float | None, *, fm, pct_fmt=False) -> dict[str, str]:
    if base_raw is None or vivo_raw is None:
        return {"abs": "—", "pct": "—"}
    delta = vivo_raw - base_raw
    abs_disp = f"{delta:+.2f}" if pct_fmt else fm(delta)
    if base_raw:
        pct = (vivo_raw / base_raw - 1.0) * 100.0
        pct_disp = f"{pct:+.1f}%"
    elif vivo_raw:
        pct_disp = "—"
    else:
        pct_disp = "0.0%"
    return {"abs": abs_disp, "pct": pct_disp}


def _balance_diff_rows(base_mb: dict, vivo_mb: dict, fm) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    b_items = {x["label"]: x.get("raw", 0.0) for x in base_mb["activos"] + base_mb["pasivos"]}
    v_items = {x["label"]: x.get("raw", 0.0) for x in vivo_mb["activos"] + vivo_mb["pasivos"]}
    for label in list(b_items.keys()) + [k for k in v_items if k not in b_items]:
        diff = _diff_cell(b_items.get(label), v_items.get(label), fm=fm)
        rows.append({"label": label, "abs": diff["abs"], "pct": diff["pct"]})
    liq_diff = _diff_cell(base_mb.get("liquidez"), vivo_mb.get("liquidez"), fm=fm, pct_fmt=True)
    rows.append({"label": "Liquidez simulada", "abs": liq_diff["abs"], "pct": liq_diff["pct"]})
    return rows


def _precautions(vivo: dict[str, float], sim_vivo: dict[str, Any]) -> list[dict[str, str]]:
    from .precauciones import PRECAUTION_ARTICLES

    out: list[dict[str, str]] = []
    liq = sim_vivo.get("liquidez_min")
    if liq is not None and liq < 1.25:
        art = PRECAUTION_ARTICLES["liquidez-war-room"]
        out.append(
            {
                "slug": "liquidez-war-room",
                "title": art["title"],
                "summary": f"Liquidez mínima simulada {liq:.2f}× (nov–jul). {art['summary']}",
            }
        )
    if vivo.get("withdrawals_pct", 0) >= 10:
        art = PRECAUTION_ARTICLES["back-to-back-sep-oct"]
        out.append(
            {
                "slug": "back-to-back-sep-oct",
                "title": art["title"],
                "summary": art["summary"],
            }
        )
    if vivo.get("fx_pct", 0) >= 8:
        art = PRECAUTION_ARTICLES["descalce-fx"]
        out.append({"slug": "descalce-fx", "title": art["title"], "summary": art["summary"]})
    if sim_vivo.get("util_crisis_acum", 0) < 0:
        art = PRECAUTION_ARTICLES["utilidad-crisis-cobranza"]
        out.append(
            {
                "slug": "utilidad-crisis-cobranza",
                "title": art["title"],
                "summary": art["summary"],
            }
        )
    if not out:
        art = PRECAUTION_ARTICLES["preparacion-sep-oct"]
        out.append(
            {
                "slug": "preparacion-sep-oct",
                "title": art["title"],
                "summary": art["summary"],
            }
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
    mini_res = _mini_results(ctx, data, bu, fm)
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
        ctx,
        data,
        bu,
        fm,
        ac=sim_base["end_ac"],
        pc=sim_base["end_pc"],
        pasivo_extra=0,
        cartera_override=sim_base["end_cartera"],
    )
    bg_vivo_crisis = _mini_balance(
        ctx,
        data,
        bu,
        fm,
        ac=sim_vivo["end_ac"],
        pc=sim_vivo["end_pc"],
        pasivo_extra=sim_vivo["end_pasivo_extra"],
        cartera_override=sim_vivo["end_cartera"],
    )
    balance_diff_rows = _balance_diff_rows(bg_base_crisis, bg_vivo_crisis, fm)

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
        "balance_diff_rows": balance_diff_rows,
        "compare_rows": compare_rows,
        "sim_base": sim_base,
        "sim_vivo": sim_vivo,
        "chart_timeline": chart,
        "base_presets": BASE_PRESETS,
        "vivo_presets": VIVO_PRESETS,
        "driver_fields": DRIVER_FIELDS,
        "precautions": _precautions(sv, sim_vivo),
        "liq_vivo_tone": liq_vivo_ev.get("tone"),
        "liq_base_tone": liq_base_ev.get("tone"),
    }


# Compatibilidad con imports previos
PRESETS = {**BASE_PRESETS, **VIVO_PRESETS}
