"""Stress test Noviembre 2026 — Midterms EUA · base agosto 2026."""

from __future__ import annotations

from typing import Any

from ..accounts import div_pref_ytd, line, preferentes_stock
from ..bands import evaluate_ratio
from ..indices import derived_metrics
from ..intermediacion import _aggregate, _build_slices, _intermediation_slice
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
            _line("Pagarés AP/PG", pagares),
            _line("Acciones preferentes", pref),
            _line("Préstamos bancos (pasivo)", bancos),
            _line("Pasivo total (libros)", pasivo_books),
            _line("Fondeo total (Pas.+Pref.)", pasivo_books + pref),
        ],
        "liquidez": liq,
        "liquidez_display": f"{liq:.2f}×" if liq is not None else "—",
    }


def _ytd_periods(data: dict, period: str) -> list[str]:
    year = (period or "")[:4]
    return [p for p in data.get("periods") or [] if str(p).startswith(year) and str(p) <= period]


def _mini_balance_triple_rows(
    real_mb: dict[str, Any],
    base_mb: dict[str, Any],
    vivo_mb: dict[str, Any],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    r_pas = real_mb["pasivos"]
    b_pas = base_mb["pasivos"]
    v_pas = vivo_mb["pasivos"]
    for i, r_act in enumerate(real_mb["activos"]):
        b_act = base_mb["activos"][i] if i < len(base_mb["activos"]) else {"label": "", "value": ""}
        v_act = vivo_mb["activos"][i] if i < len(vivo_mb["activos"]) else {"label": "", "value": ""}
        r_pas_row = r_pas[i] if i < len(r_pas) else {"label": "", "value": ""}
        b_pas_row = b_pas[i] if i < len(b_pas) else {"label": "", "value": ""}
        v_pas_row = v_pas[i] if i < len(v_pas) else {"label": "", "value": ""}
        rows.append(
            {
                "activo_label": r_act["label"],
                "activo_real": r_act["value"],
                "activo_base": b_act["value"],
                "activo_vivo": v_act["value"],
                "pasivo_label": r_pas_row.get("label", ""),
                "pasivo_real": r_pas_row.get("value", ""),
                "pasivo_base": b_pas_row.get("value", ""),
                "pasivo_vivo": v_pas_row.get("value", ""),
            }
        )
    for j in range(len(real_mb["activos"]), len(r_pas)):
        b_pas_row = b_pas[j] if j < len(b_pas) else {"label": "", "value": ""}
        v_pas_row = v_pas[j] if j < len(v_pas) else {"label": "", "value": ""}
        rows.append(
            {
                "activo_label": "",
                "activo_real": "",
                "activo_base": "",
                "activo_vivo": "",
                "pasivo_label": r_pas[j]["label"],
                "pasivo_real": r_pas[j]["value"],
                "pasivo_base": b_pas_row.get("value", ""),
                "pasivo_vivo": v_pas_row.get("value", ""),
            }
        )
    return rows


def _mini_results_triple(
    real_rows: list[dict[str, str]],
    sim_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for i in range(min(4, len(real_rows), len(sim_rows))):
        out.append(
            {
                "label": real_rows[i]["label"],
                "real": real_rows[i]["value"],
                "base": sim_rows[i]["base"],
                "vivo": sim_rows[i]["vivo"],
            }
        )
    if len(real_rows) >= 6 and len(sim_rows) >= 6:
        out.append(
            {
                "label": "Util. contable",
                "real": real_rows[4]["value"],
                "base": sim_rows[4]["base"],
                "vivo": sim_rows[4]["vivo"],
            }
        )
        out.append(
            {
                "label": "Util. gerencial",
                "real": real_rows[5]["value"],
                "base": sim_rows[5]["base"],
                "vivo": sim_rows[5]["vivo"],
            }
        )
    return out


def _mini_results_real(ctx: dict[str, Any], data: dict, bu: str, fm) -> list[dict[str, str]]:
    period = ctx["period"]
    rates = ctx["rates"]
    ytd_slices = _build_slices(data, bu, _ytd_periods(data, period), rates, "gerencial")
    agg = _aggregate(ytd_slices)
    mc = ctx["metrics_cont"]
    mg = ctx["metrics"]
    year = period[:4]
    return [
        {"label": "Productos financieros", "value": fm(agg["productos"])},
        {"label": "Gastos financieros", "value": fm(agg["costos"])},
        {"label": "Margen", "value": fm(agg["margen_bruto"])},
        {"label": "Otros gastos", "value": fm(agg["overhead_neto"])},
        {"label": f"Utilidad acum. contable ({year})", "value": fm(mc.get("utilidades"))},
        {"label": f"Utilidad acum. gerencial ({year})", "value": fm(mg.get("util_vista"))},
    ]


def _scenario_pnl_totals(ctx: dict[str, Any], shocks: dict[str, float]) -> dict[str, float]:
    sl = ctx["slice"]
    mom = shocks.get("factoraje_mom_pct", 0.0) / 100.0
    cartera = n(sl.get("colocaciones"))
    captacion = n(sl.get("captaciones"))
    base_cartera = cartera or 1.0
    t_act = sl["tasa_activa"]
    div_m = n(sl.get("div_pref_mes"))
    base_oh = n(sl.get("overhead_neto"))

    productos = costos = margen = overhead = util_c = util_g = 0.0
    for _, _, factor, _ in TIMELINE:
        cartera *= 1 + mom
        captacion *= 1 + mom
        scale = cartera / base_cartera
        eff = DEFAULT_SHOCKS if factor <= 0 else _scaled_shocks(shocks, factor)
        st = _monthly_stress(ctx, eff, cartera=cartera, captacion=captacion)
        prod_m = cartera * t_act / 12.0
        marg_m = st["margen_stress"]
        oh_m = base_oh * scale
        util_m = marg_m - oh_m
        productos += prod_m
        margen += marg_m
        costos += prod_m - marg_m
        overhead += oh_m
        util_g += util_m
        util_c += util_m + div_m
    return {
        "productos": productos,
        "costos": costos,
        "margen_bruto": margen,
        "overhead_neto": overhead,
        "util_cont": util_c,
        "util_ger": util_g,
    }


def _mini_results_compare(ctx: dict[str, Any], shocks_base: dict[str, float], shocks_vivo: dict[str, float], fm) -> list[dict[str, str]]:
    agg_b = _scenario_pnl_totals(ctx, shocks_base)
    agg_v = _scenario_pnl_totals(ctx, shocks_vivo)

    def _row(label: str, key: str) -> dict[str, str]:
        return {"label": label, "base": fm(agg_b[key]), "vivo": fm(agg_v[key])}

    return [
        _row("Productos financieros", "productos"),
        _row("Gastos financieros", "costos"),
        _row("Margen", "margen_bruto"),
        _row("Otros gastos", "overhead_neto"),
        _row(f"Utilidad sim. contable (sep–jul)", "util_cont"),
        _row(f"Utilidad sim. gerencial (sep–jul)", "util_ger"),
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
    overhead = n(sl.get("overhead_neto")) * scale
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


def _balance_end_rows(base_mb: dict, vivo_mb: dict, fm) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    b_items = {x["label"]: x for x in base_mb["activos"] + base_mb["pasivos"]}
    v_items = {x["label"]: x for x in vivo_mb["activos"] + vivo_mb["pasivos"]}
    seen: set[str] = set()
    for label in list(b_items.keys()) + [k for k in v_items if k not in b_items]:
        if label in seen:
            continue
        seen.add(label)
        b_raw = b_items.get(label, {}).get("raw")
        v_raw = v_items.get(label, {}).get("raw")
        diff = _diff_cell(b_raw, v_raw, fm=fm)
        rows.append(
            {
                "label": label,
                "base": b_items.get(label, {}).get("value", "—"),
                "vivo": v_items.get(label, {}).get("value", "—"),
                "abs": diff["abs"],
                "pct": diff["pct"],
            }
        )
    liq_diff = _diff_cell(base_mb.get("liquidez"), vivo_mb.get("liquidez"), fm=fm, pct_fmt=True)
    rows.append(
        {
            "label": "Liquidez simulada",
            "base": base_mb.get("liquidez_display", "—"),
            "vivo": vivo_mb.get("liquidez_display", "—"),
            "abs": liq_diff["abs"],
            "pct": liq_diff["pct"],
        }
    )
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


def methodology_sections() -> list[dict[str, Any]]:
    """Texto de metodología alineado con TIMELINE y _monthly_stress."""

    def _p(label: str, *parts: str) -> dict[str, Any]:
        return {"text": f"{label}: {' '.join(parts)}"}

    timeline_lines = []
    for period, phase, factor, phase_label in TIMELINE:
        if factor <= 0:
            eff = "sin shock (drivers de estrés en 0; colocaciones/mes aparte)"
        else:
            eff = f"intensidad ×{factor:g} sobre los valores del slider"
        timeline_lines.append(f"{period} ({phase_label}) — {eff}")

    base_label = BASE_PERIOD.replace("-", " ")
    mod = MODERADO_SHOCKS

    return [
        _p(
            "Punto de partida",
            f"El corte Real usa libros de {base_label} (agosto 2026): balance, margen y tasas del slice "
            "de intermediación gerencial.",
            "Base y Vivo son simulaciones independientes desde ese mismo corte, recorriendo once meses "
            "(sep-2026 → jul-2027); no se re-simula enero–agosto 2026.",
        ),
        _p(
            "Calendario de intensidad del shock",
            "Los sliders definen el shock pleno (100 % activo). Cada mes aplica un factor multiplicador "
            "solo a los drivers de estrés (tipo de cambio, tasas, mora, retiros, remesas, recuperación); "
            "colocaciones/mes no usa ese factor.",
            "Agosto es la ancla contable y no entra en la línea simulada.",
            "Septiembre y octubre tienen factor 0 (sin estrés), aunque la cartera puede moverse por colocaciones/mes.",
        ),
        {
            "text": "Detalle mes a mes:",
            "bullets": timeline_lines,
        },
        _p(
            "Presets cero, moderado, severo y extremo",
            "Base cero deja todos los drivers en 0.",
            "Base moderado y vivo moderado comparten el paquete numérico moderado; severo y extremo "
            "solo en el escenario vivo.",
            "Los valores corresponden al preset seleccionado en pantalla; la simulación los escala con el calendario.",
        ),
        {
            "text": (
                f"Referencia moderado: FX +{mod['fx_pct']:g} %, tasas +{mod['rates_bp']:.0f} pb, "
                f"mora +{mod['mora_pct']:.0f} %, retiros +{mod['withdrawals_pct']:.0f} %, "
                f"remesas +{mod['remittances_pct']:.0f} %, recuperación +{mod['recovery_pct']:.0f} %, "
                f"colocaciones {mod['factoraje_mom_pct']:+.1f} %/mes."
            ),
            "bullets": ["Severo y extremo elevan esos ejes (según sliders del preset vivo)."],
        },
        _p(
            "Colocaciones / mes (factoraje)",
            "Cada mes (incluidos sep–oct): cartera ← cartera × (1 + colocaciones/mes) y captaciones ← "
            "captaciones × (1 + colocaciones/mes), con el slider del escenario.",
            "Margen bruto, overhead y activo corriente escalan con cartera y captación respecto al corte de agosto.",
        ),
        _p(
            "Tipo de cambio (USD/GTQ +dep.)",
            f"Se asume {USD_PASIVA_SHARE:.0%} del pasivo sensible a depreciación.",
            f"Notional FX = pasivo × {USD_PASIVA_SHARE:.2f} × (fx_pct/100), escalado por captación.",
            "Costo mensual en resultados: notional FX × 0,25 %.",
            "En balance: pasivo corriente sube notional FX × 15 % (liquidez/contingencia simplificada).",
        ),
        _p(
            "Tasas de fondeo (+ pb)",
            "Costo mensual adicional = captaciones × (rates_bp / 10 000) / 12,",
            "interpretado como spread anual extra sobre el stock de captaciones del mes, repartido en doce.",
        ),
        _p(
            "Mora (+) y caída de remesas (+)",
            "Pérdida de rendimiento mensual: cartera × tasa activa/12 × (mora×0,45 + remesas×0,25).",
            "Coeficientes fijos sobre ingreso financiero bruto; no hay provisiones contables línea a línea.",
        ),
        _p(
            "Recuperación de cartera (−)",
            "Penaliza el margen: cartera × 1,5 % anual × (recovery_pct/100) / 12.",
            "Un recovery_pct mayor reduce margen en el mes estresado.",
        ),
        _p(
            "Retiros de pasivas (+)",
            "Salida mensual = captaciones × (withdrawals_pct/100).",
            "Activo corriente baja salida × 85 %; pasivo corriente sube la salida (más ajuste FX en PC).",
            "Liquidez del mes = activo corriente ajustado / pasivo corriente ajustado.",
        ),
        _p(
            "Utilidad y margen mensual",
            "Margen estresado = margen bruto escalado − costo tasas − costo FX − mora/remesas − recuperación.",
            "Utilidad gerencial = margen estresado − overhead neto escalado.",
            "Utilidad contable = utilidad gerencial + dividendos preferentes del mes (constante del corte).",
        ),
        _p(
            "Mini resultados (Base vs Vivo)",
            "Productos: suma mensual cartera × tasa activa / 12 (sep–jul).",
            "Gastos financieros: productos − margen estresado acumulado.",
            "Margen, overhead y utilidades: suma de los once meses simulados.",
            "La columna Real es ene–ago 2026 en libros; no mezcla la simulación.",
        ),
        _p(
            "Mini balance fin jul-2027",
            "Tras el último mes se usan activo corriente, pasivo corriente, cartera simulada y pasivo extra "
            "(retiros + FX) para reconstruir activo, pasivo, patrimonio y liquidez.",
            "El Δ compara vivo vs base al mismo cierre simulado.",
        ),
        _p(
            "Simplificaciones",
            f"Referencia FX {FX_REF} GTQ/USD; sin path diario del tipo de cambio.",
            "Noviembre intensidad 0,35 (apertura tardía post 3-nov), pico dic–ene ×1,0, secuela feb–jul hasta ×0,48.",
            "Stress test gerencial para comparar escenarios, no forecast auditado.",
        ),
        {
            "text": (
                "Primeros refinamientos (si más adelante se prefiere afinar el cálculo): "
                "El modelo actual se queda así: sensibilidad con pocas relaciones explícitas. "
                "Para acercarse a una simulación más completa, estos serían los primeros pasos razonables:"
            ),
            "bullets": [
                "Provisiones y castigos por tramos de mora (A–E), ligados a mora_pct y saldos reales.",
                "Pasivo desagregado: pagarés vs bancos, GTQ vs USD, con elasticidades distintas en FX y retiros.",
                "Colocaciones por producto (factoraje, hipotecario, consumo) con tasas y prepagos propias.",
                "Overhead con tramo fijo + variable y recortes diferidos en secuela.",
                "Liquidez con colchón regulatorio, líneas de respaldo y costo de oportunidad del efectivo.",
                "Correlaciones entre drivers en meses de crisis (FX, retiros, remesas).",
                "Calibración histórica de coeficientes (0,45 / 0,25 / 0,25 % FX) si hubiera meses de estrés.",
            ],
        },
        _p(
            "Qué tan impactantes serían esos refinamientos",
            "Ninguna simulación reproduce fielmente un caso real.",
            "Este MVP sirve sobre todo para comparar base vs vivo en la misma lógica: dirección y orden "
            "de magnitud suelen ser útiles; la cifra exacta de utilidad o liquidez mínima no es pronóstico contable.",
        ),
        _p(
            "Precisión orientativa",
            "Frente a un motor refinado (provisiones, pasivo desagregado, productos), en los totales agregados "
            "(utilidad acumulada sep–jul, margen, liquidez mínima) puede estimarse un ~10–20 % menos error "
            "relativo si esos refinamientos estuvieran bien calibrados: menos sesgo por simplificar mora, FX y retiros, "
            "no una «precisión absoluta».",
            "En partidas sueltas —un mes concreto, liquidez en ene-2027, Δ patrimonio al cierre— la brecha con "
            "un modelo fino puede seguir siendo amplia (±20–40 % o más en severo/extremo), porque aquí faltan "
            "correlaciones, colchones regulatorios y castigos explícitos.",
            "Los refinamientos anteriores atacan sobre todo ese segundo tipo de error; el juicio gerencial sigue siendo indispensable.",
        ),
    ]


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
    sim_base = _simulate_timeline(ctx, sb)
    sim_vivo = _simulate_timeline(ctx, sv)

    bg_base_crisis = _mini_balance(
        ctx,
        data,
        bu,
        fm,
        ac=sim_base["end_ac"],
        pc=sim_base["end_pc"],
        pasivo_extra=sim_base["end_pasivo_extra"],
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
    mini_balance_corte_rows = _mini_balance_triple_rows(mini_bg, bg_base_crisis, bg_vivo_crisis)
    mini_results_real = _mini_results_real(ctx, data, bu, fm)
    mini_results_sim = _mini_results_compare(ctx, sb, sv, fm)
    mini_results = _mini_results_triple(mini_results_real, mini_results_sim)
    balance_end_rows = _balance_end_rows(bg_base_crisis, bg_vivo_crisis, fm)

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
        "corte_note": (
            "Real = corte ago-2026 en libros (común). Base y Vivo = proyección al cierre de la simulación (jul-2027) según drivers."
        ),
        "results_note": (
            "Real = acumulado ene–ago 2026. Base y Vivo = simulación acumulada sep–jul según drivers."
        ),
        "sim_note": (
            "Comparación base vs vivo al cierre jul-2027 (Δ respecto al escenario base)."
        ),
        "shocks_base": sb,
        "shocks_vivo": sv,
        "mini_balance": mini_bg,
        "mini_balance_corte_rows": mini_balance_corte_rows,
        "liquidez_corte": mini_bg.get("liquidez_display", "—"),
        "liquidez_corte_base": bg_base_crisis.get("liquidez_display", "—"),
        "liquidez_corte_vivo": bg_vivo_crisis.get("liquidez_display", "—"),
        "mini_results": mini_results,
        "mini_results_real": mini_results_real,
        "mini_results_sim": mini_results_sim,
        "mini_balance_base_crisis": bg_base_crisis,
        "mini_balance_vivo_crisis": bg_vivo_crisis,
        "balance_end_rows": balance_end_rows,
        "compare_rows": compare_rows,
        "sim_base": sim_base,
        "sim_vivo": sim_vivo,
        "chart_timeline": chart,
        "base_presets": BASE_PRESETS,
        "vivo_presets": VIVO_PRESETS,
        "driver_fields": DRIVER_FIELDS,
        "precautions": _precautions(sv, sim_vivo),
        "methodology": methodology_sections(),
        "liq_vivo_tone": liq_vivo_ev.get("tone"),
        "liq_base_tone": liq_base_ev.get("tone"),
    }


# Compatibilidad con imports previos
PRESETS = {**BASE_PRESETS, **VIVO_PRESETS}
