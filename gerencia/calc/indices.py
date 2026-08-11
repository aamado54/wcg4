"""Cálculo de índices estratégicos a partir de KPIs institucionales."""

from __future__ import annotations

from typing import Any

from .accounts import div_pref_ytd, preferentes_stock
from .bands import evaluate_ratio
from .utils import BU_LABEL, delta, kpi_row, month_of, n, rates_from_meta


def build_preferentes_stock(data: dict, bu: str, periods: list[str]) -> dict[str, float]:
    """Stock real 301010106 (Inversionistas Factoraje / Leasing)."""
    return {p: preferentes_stock(data, bu, p) for p in periods}


def derived_metrics(
    row: dict,
    bu: str,
    period: str,
    rates: dict[str, float],
    vista: str = "contable",
    inv_proxy: float | None = None,
    div_ytd: float | None = None,
    strict: bool = False,
) -> dict[str, float | None]:
    """vista: 'contable' | 'gerencial'.

    Gerencial normal: solo resta dividendos preferentes (102020301 Δ≥0) de la 302.
    Gerencial estricta: además reclasifica 301010106 de patrimonio a pasivo a 1 año.
    """
    vista = "gerencial" if vista == "gerencial" else "contable"

    ac = n(row.get("activo_corriente"))
    pc_books = n(row.get("pasivo_corriente"))
    pnc = n(row.get("pasivo_no_corriente"))
    pat_books = n(row.get("patrimonio"))
    act = n(row.get("activo")) or (ac + n(row.get("activo_no_corriente")))
    util = n(row.get("utilidades"))
    cartera = n(row.get("cartera"))

    pref = float(inv_proxy) if inv_proxy is not None else 0.0
    if div_ytd is None:
        div_ytd = 0.0
    util_g = util - float(div_ytd)

    pasivo_books = pc_books + pnc
    reclasifica = vista == "gerencial" and strict
    if reclasifica:
        patrimonio = max(pat_books - pref, 1.0)
        pc = pc_books + pref
        pasivo_total = pasivo_books + pref
        util_view = util_g
    elif vista == "gerencial":
        patrimonio = pat_books if pat_books else 1.0
        pc = pc_books
        pasivo_total = pasivo_books
        util_view = util_g
    else:
        patrimonio = pat_books if pat_books else 1.0
        pc = pc_books
        pasivo_total = pasivo_books
        util_view = util

    liq = (ac / pc) if pc else row.get("liquidez")
    apa = (pasivo_total / patrimonio) if patrimonio else None
    acida = (ac * 0.85 / pc) if pc else None
    kt = ac - pc
    deuda_pat = (pasivo_total / patrimonio) if patrimonio else None

    bank_share = 0.55
    fondeo_bancos = pasivo_books * bank_share
    pas_b = rates["pasiva_bancos_f"] if bu != "L" else rates["pasiva_bancos_l"]
    mes = month_of(period)
    interes_bancos = fondeo_bancos * pas_b * (mes / 12.0)
    interes_inv = float(div_ytd) if vista == "gerencial" else 0.0
    interes_est = interes_bancos + interes_inv
    cobertura = (util_view / interes_est) if interes_est else None

    z_parts = {
        "kt_a": 1.2 * (kt / act) if act else 0.0,
        "u_a": 1.4 * (util_view / act) if act else 0.0,
        "roe": 0.8 * ((util_view / patrimonio) if patrimonio else 0.0),
        "pat_pas": 0.6 * ((patrimonio / pasivo_total) if pasivo_total else 0.0),
        "cart_a": 0.9 * ((cartera / act) if act else 0.0),
    }
    z = sum(z_parts.values()) if act > 0 and pasivo_total > 0 else None

    roa = (util_view / act) if act else row.get("roa")
    roe_v = (util_view / patrimonio) if patrimonio else row.get("roe")

    return {
        "vista": vista,
        "activo": act,
        "activo_corriente": ac,
        "pasivo_corriente": pc,
        "pasivo_corriente_books": pc_books,
        "pasivo_no_corriente": pnc,
        "pasivo_total": pasivo_total,
        "pasivo_books": pasivo_books,
        "patrimonio": patrimonio,
        "patrimonio_books": pat_books,
        "utilidades": util,
        "util_gerencial": util_g,
        "util_vista": util_view,
        "cartera": cartera,
        "liquidez": float(liq) if liq is not None else None,
        "acida": acida,
        "capital_trabajo": kt,
        "apalancamiento": float(apa) if apa is not None else None,
        "deuda_patrimonio": deuda_pat,
        "deuda_gerencial_patrimonio": deuda_pat,
        "cobertura_intereses": cobertura,
        "z_score": z,
        "z_parts": z_parts,
        "roa": roa,
        "roe": roe_v,
        "inv_proxy": pref,
        "div_pref_ytd": float(div_ytd),
        "interes_est_ytd": interes_est,
    }


def build_indices_catalog(
    data: dict,
    bu: str = "T",
    periods: int = 14,
    vista: str = "contable",
    strict: bool = False,
) -> dict[str, Any]:
    all_periods = list(data.get("periods") or [])
    if not all_periods:
        return {"status": "empty", "rows": [], "series": {}, "period": None}

    vista = "gerencial" if vista == "gerencial" else "contable"
    pref_stock = build_preferentes_stock(data, bu, all_periods)

    focus = all_periods[-periods:] if len(all_periods) > periods else all_periods
    latest = focus[-1]
    prev = focus[-2] if len(focus) >= 2 else None
    rates = rates_from_meta(data)

    def metrics_at(p: str) -> dict:
        return derived_metrics(
            kpi_row(data, bu, p),
            bu,
            p,
            rates,
            vista=vista,
            inv_proxy=pref_stock.get(p, 0.0),
            div_ytd=div_pref_ytd(data, bu, p),
            strict=strict,
        )

    cur = metrics_at(latest)
    prv = metrics_at(prev) if prev else {}

    apa_note = (
        "Pasivo contable / Patrimonio contable."
        if vista == "contable"
        else (
            "Pasivo + 301010106 (preferentes) / Patrimonio neto. Vista gerencial estricta."
            if strict
            else "Mismos saldos de libros; la utilidad resta dividendos preferentes (102020301)."
        )
    )
    catalog_keys = [
        ("liquidez", "Liquidez (AC/PC)", "Relación circulante. Para factoraje/leasing corto, 1.3–1.85× suele ser razonable."),
        ("acida", "Prueba ácida adaptada", "85% del activo corriente / PC."),
        ("capital_trabajo", "Capital de trabajo", "AC − PC (000 QTZ)."),
        ("apalancamiento", "Apalancamiento", apa_note),
        ("deuda_patrimonio", "Deuda / Patrimonio", "Misma base que apalancamiento en esta vista."),
        ("cobertura_intereses", "Cobertura de intereses (est.)", "Utilidad de la vista / costo financiero estimado."),
        ("z_score", "Calificador Z NBFI", "Score interno WCG con patrimonio y deuda de la vista."),
        ("roe", "ROE", "Utilidad de la vista / Patrimonio de la vista."),
        ("roa", "ROA", "Utilidad de la vista / Activo."),
    ]

    rows = []
    for key, label, note in catalog_keys:
        val = cur.get(key)
        if key in ("roe", "roa") and val is not None:
            display = f"{float(val) * 100:.1f}%"
            ev = {"tone": "neutral", "zone": "—", "meaning": note, "bands": {}}
        elif key == "capital_trabajo":
            display = f"{val:,.0f}" if val is not None else "—"
            ev = {
                "tone": "ok" if (val or 0) > 0 else "risk",
                "zone": "positivo" if (val or 0) > 0 else "negativo",
                "meaning": note,
                "bands": {},
            }
        elif key == "cobertura_intereses":
            display = f"{val:.2f}×" if val is not None else "—"
            tone = "ok" if (val or 0) >= 1.5 else ("warn" if (val or 0) >= 1.0 else "risk")
            ev = {"tone": tone, "zone": "—", "meaning": note, "bands": {}}
        else:
            band_key = {
                "liquidez": "liquidez",
                "acida": "acida",
                "apalancamiento": "apalancamiento",
                "deuda_patrimonio": "deuda_patrimonio",
                "z_score": "z_score",
            }.get(key)
            ev = (
                evaluate_ratio(band_key, float(val) if val is not None else None)
                if band_key
                else {"tone": "neutral", "zone": "—", "meaning": note, "bands": {}}
            )
            display = f"{val:.2f}" if key == "z_score" and val is not None else (
                f"{val:.2f}×" if val is not None else "—"
            )

        d = delta(
            float(val) if val is not None else None,
            float(prv[key]) if prv.get(key) is not None else None,
        )
        rows.append(
            {
                "key": key,
                "label": label,
                "value": val,
                "display": display,
                "delta": (d * 100.0) if d is not None else None,
                "tone": ev.get("tone"),
                "zone": ev.get("zone"),
                "meaning": ev.get("meaning") or note,
                "note": note,
                "bands": ev.get("bands") or {},
            }
        )

    focus_metrics = [metrics_at(p) for p in focus]
    series = {
        "labels": focus,
        "liquidez": [m.get("liquidez") for m in focus_metrics],
        "apalancamiento": [m.get("apalancamiento") for m in focus_metrics],
        "acida": [m.get("acida") for m in focus_metrics],
        "z_score": [m.get("z_score") for m in focus_metrics],
        "deuda_gerencial_patrimonio": [m.get("deuda_patrimonio") for m in focus_metrics],
        "z_kt_a": [((m.get("z_parts") or {}).get("kt_a")) for m in focus_metrics],
        "z_u_a": [((m.get("z_parts") or {}).get("u_a")) for m in focus_metrics],
        "z_roe": [((m.get("z_parts") or {}).get("roe")) for m in focus_metrics],
        "z_pat_pas": [((m.get("z_parts") or {}).get("pat_pas")) for m in focus_metrics],
        "z_cart_a": [((m.get("z_parts") or {}).get("cart_a")) for m in focus_metrics],
    }

    return {
        "status": "ok",
        "bu": bu,
        "bu_label": BU_LABEL.get(bu, bu),
        "vista": vista,
        "strict": strict,
        "period": latest,
        "prev_period": prev,
        "unit": data.get("unit") or "000 quetzales",
        "metrics": cur,
        "rows": rows,
        "series": series,
        "rates": rates,
    }
