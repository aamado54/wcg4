"""Cálculo de índices estratégicos a partir de KPIs institucionales."""

from __future__ import annotations

from typing import Any

from .bands import evaluate_ratio
from .utils import BU_LABEL, delta, kpi_row, month_of, n, rates_from_meta

# Porción del patrimonio tratada como preferentes / pagarés a inversionistas (deuda gerencial).
INV_SHARE = {"T": 0.45, "F": 0.45, "L": 0.25, "I": 0.15, "S": 0.15}


def derived_metrics(
    row: dict,
    bu: str,
    period: str,
    rates: dict[str, float],
    vista: str = "contable",
) -> dict[str, float | None]:
    """vista: 'contable' (preferentes en patrimonio) | 'gerencial' (preferentes = deuda)."""
    vista = "gerencial" if vista == "gerencial" else "contable"

    ac = n(row.get("activo_corriente"))
    pc = n(row.get("pasivo_corriente"))
    pnc = n(row.get("pasivo_no_corriente"))
    pat_books = n(row.get("patrimonio"))
    act = n(row.get("activo")) or (ac + n(row.get("activo_no_corriente")))
    util = n(row.get("utilidades"))
    cartera = n(row.get("cartera"))

    inv_share = INV_SHARE.get(bu, 0.35)
    inv_proxy = pat_books * inv_share
    pas_i = rates["pasiva_inv_f"] if bu != "L" else rates["pasiva_inv_l"]
    m = month_of(period)
    div_ytd = inv_proxy * pas_i * (m / 12.0)
    util_g = util - div_ytd

    pasivo_books = pc + pnc
    if vista == "gerencial":
        # Preferentes / pagarés a inversionistas salen del patrimonio y entran a deuda.
        patrimonio = max(pat_books - inv_proxy, 1.0)
        pasivo_total = pasivo_books + inv_proxy
        util_view = util_g
    else:
        patrimonio = pat_books if pat_books else 1.0
        pasivo_total = pasivo_books
        util_view = util

    liq = row.get("liquidez")
    if liq is None and pc:
        liq = ac / pc
    # En vista gerencial el pasivo corriente no crece automáticamente (preferentes suelen
    # ser no corrientes / capital contable). El apalancamiento sí cambia.
    apa = (pasivo_total / patrimonio) if patrimonio else None
    acida = (ac * 0.85 / pc) if pc else None
    kt = ac - pc
    deuda_pat = (pasivo_total / patrimonio) if patrimonio else None

    bank_share = 0.55
    fondeo_bancos = pasivo_books * bank_share
    # En gerencial el costo a inversionistas también es "interés" económico
    pas_b = rates["pasiva_bancos_f"] if bu != "L" else rates["pasiva_bancos_l"]
    interes_bancos = fondeo_bancos * pas_b * (m / 12.0)
    interes_inv = div_ytd if vista == "gerencial" else 0.0
    interes_est = interes_bancos + interes_inv
    cobertura = (util_view / interes_est) if interes_est else None

    # Z-score con patrimonio / pasivo según la vista
    z = None
    if act > 0 and pasivo_total > 0:
        roe = (util_view / patrimonio) if patrimonio else 0.0
        z = (
            1.2 * (kt / act)
            + 1.4 * (util_view / act)
            + 0.8 * roe
            + 0.6 * (patrimonio / pasivo_total)
            + 0.9 * ((cartera / act) if cartera else 0.35)
        )

    roa = (util_view / act) if act else row.get("roa")
    roe_v = (util_view / patrimonio) if patrimonio else row.get("roe")

    return {
        "vista": vista,
        "activo": act,
        "activo_corriente": ac,
        "pasivo_corriente": pc,
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
        "roa": roa,
        "roe": roe_v,
        "inv_proxy": inv_proxy,
        "div_pref_ytd": div_ytd,
        "interes_est_ytd": interes_est,
    }


def build_indices_catalog(
    data: dict,
    bu: str = "T",
    periods: int = 14,
    vista: str = "contable",
) -> dict[str, Any]:
    all_periods = list(data.get("periods") or [])
    if not all_periods:
        return {"status": "empty", "rows": [], "series": {}, "period": None}

    vista = "gerencial" if vista == "gerencial" else "contable"
    focus = all_periods[-periods:] if len(all_periods) > periods else all_periods
    latest = focus[-1]
    prev = focus[-2] if len(focus) >= 2 else None
    rates = rates_from_meta(data)
    cur = derived_metrics(kpi_row(data, bu, latest), bu, latest, rates, vista=vista)
    prv = derived_metrics(kpi_row(data, bu, prev), bu, prev, rates, vista=vista) if prev else {}

    apa_note = (
        "Pasivo contable / Patrimonio contable."
        if vista == "contable"
        else "Pasivo + preferentes/pagarés est. / Patrimonio neto de esas obligaciones."
    )
    catalog_keys = [
        ("liquidez", "Liquidez (AC/PC)", "Relación circulante. Para factoraje/leasing corto, 1.3–1.85× suele ser razonable."),
        ("acida", "Prueba ácida adaptada", "85% del activo corriente / PC. Sin inventario industrial; la cartera es el activo líquido principal."),
        ("capital_trabajo", "Capital de trabajo", "AC − PC (000 QTZ). Buffer operativo de corto plazo."),
        ("apalancamiento", "Apalancamiento", apa_note),
        (
            "deuda_patrimonio",
            "Deuda / Patrimonio",
            "Misma base que apalancamiento en esta vista.",
        ),
        ("cobertura_intereses", "Cobertura de intereses (est.)", "Utilidad de la vista / costo financiero estimado (bancos ± inversionistas)."),
        ("z_score", "Calificador Z NBFI", "Score interno WCG recalculado con patrimonio y deuda de la vista elegida."),
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

    def series_of(metric: str) -> list:
        return [
            derived_metrics(kpi_row(data, bu, p), bu, p, rates, vista=vista).get(metric)
            for p in focus
        ]

    series = {
        "labels": focus,
        "liquidez": series_of("liquidez"),
        "apalancamiento": series_of("apalancamiento"),
        "acida": series_of("acida"),
        "z_score": series_of("z_score"),
        "deuda_gerencial_patrimonio": series_of("deuda_patrimonio"),
    }

    return {
        "status": "ok",
        "bu": bu,
        "bu_label": BU_LABEL.get(bu, bu),
        "vista": vista,
        "period": latest,
        "prev_period": prev,
        "unit": data.get("unit") or "000 quetzales",
        "metrics": cur,
        "rows": rows,
        "series": series,
        "rates": rates,
    }
