"""Cálculo de índices estratégicos a partir de KPIs institucionales."""

from __future__ import annotations

from typing import Any

from .bands import evaluate_ratio
from .utils import BU_LABEL, delta, kpi_row, month_of, n, rates_from_meta


def derived_metrics(row: dict, bu: str, period: str, rates: dict[str, float]) -> dict[str, float | None]:
    ac = n(row.get("activo_corriente"))
    pc = n(row.get("pasivo_corriente"))
    pnc = n(row.get("pasivo_no_corriente"))
    pat = n(row.get("patrimonio"))
    act = n(row.get("activo")) or (ac + n(row.get("activo_no_corriente")))
    util = n(row.get("utilidades"))
    cartera = n(row.get("cartera"))
    liq = row.get("liquidez")
    if liq is None and pc:
        liq = ac / pc
    apa = row.get("apalancamiento")
    if apa is None and pat:
        apa = (pc + pnc) / pat

    # Ácida adaptada NBFI: ~85% del AC se trata como realizable en ciclo corto (cartera dominante).
    acida = (ac * 0.85 / pc) if pc else None
    kt = ac - pc
    deuda_pat = ((pc + pnc) / pat) if pat else None

    # Preferentes / inversionistas: proxy sobre patrimonio (disciplina qf / financiero board).
    inv_share = 0.45 if bu in ("T", "F") else 0.25
    inv_proxy = pat * inv_share
    pas_i = rates["pasiva_inv_f"] if bu != "L" else rates["pasiva_inv_l"]
    m = month_of(period)
    div_ytd = inv_proxy * pas_i * (m / 12.0)
    util_g = util - div_ytd

    # Deuda gerencial = pasivo + preferentes estimados
    deuda_ger = (pc + pnc + inv_proxy)
    deuda_ger_pat = (deuda_ger / pat) if pat else None

    # Cobertura intereses proxy: utilidad / (fondeo bancario * tasa)
    bank_share = 0.55
    fondeo_bancos = (pc + pnc) * bank_share
    pas_b = rates["pasiva_bancos_f"] if bu != "L" else rates["pasiva_bancos_l"]
    interes_est = fondeo_bancos * pas_b * (m / 12.0)
    cobertura = (util / interes_est) if interes_est else None

    # Z-score NBFI WCG (calibración interna, no Altman manufacturero)
    # Z = 1.2*KT/A + 1.4*Util/A + 0.8*ROE + 0.6*Pat/Pasivo + 0.9*Cartera/A
    z = None
    if act > 0 and (pc + pnc) > 0:
        roe = (util / pat) if pat else 0.0
        z = (
            1.2 * (kt / act)
            + 1.4 * (util / act)
            + 0.8 * roe
            + 0.6 * (pat / (pc + pnc))
            + 0.9 * ((cartera / act) if cartera else 0.35)
        )

    return {
        "activo": act,
        "activo_corriente": ac,
        "pasivo_corriente": pc,
        "pasivo_no_corriente": pnc,
        "pasivo_total": pc + pnc,
        "patrimonio": pat,
        "utilidades": util,
        "util_gerencial": util_g,
        "cartera": cartera,
        "liquidez": float(liq) if liq is not None else None,
        "acida": acida,
        "capital_trabajo": kt,
        "apalancamiento": float(apa) if apa is not None else None,
        "deuda_patrimonio": deuda_pat,
        "deuda_gerencial_patrimonio": deuda_ger_pat,
        "cobertura_intereses": cobertura,
        "z_score": z,
        "roa": row.get("roa"),
        "roe": row.get("roe"),
        "inv_proxy": inv_proxy,
        "div_pref_ytd": div_ytd,
        "interes_est_ytd": interes_est,
    }


def build_indices_catalog(data: dict, bu: str = "T", periods: int = 14) -> dict[str, Any]:
    all_periods = list(data.get("periods") or [])
    if not all_periods:
        return {"status": "empty", "rows": [], "series": {}, "period": None}

    focus = all_periods[-periods:] if len(all_periods) > periods else all_periods
    latest = focus[-1]
    prev = focus[-2] if len(focus) >= 2 else None
    rates = rates_from_meta(data)
    cur = derived_metrics(kpi_row(data, bu, latest), bu, latest, rates)
    prv = derived_metrics(kpi_row(data, bu, prev), bu, prev, rates) if prev else {}

    catalog_keys = [
        ("liquidez", "Liquidez (AC/PC)", "Relación circulante. Para factoraje/leasing corto, 1.3–1.85× suele ser razonable."),
        ("acida", "Prueba ácida adaptada", "85% del activo corriente / PC. Sin inventario industrial; la cartera es el activo líquido principal."),
        ("capital_trabajo", "Capital de trabajo", "AC − PC (000 QTZ). Buffer operativo de corto plazo."),
        ("apalancamiento", "Apalancamiento", "Pasivo / Patrimonio contable."),
        ("deuda_gerencial_patrimonio", "Deuda gerencial / Patrimonio", "Pasivo + preferentes est. / Patrimonio. Más fiel a la intermediación real."),
        ("cobertura_intereses", "Cobertura de intereses (est.)", "Utilidad / interés estimado sobre fondeo bancario."),
        ("z_score", "Calificador Z NBFI", "Score interno WCG (no Altman industrial). Combina KT, utilidad, ROE, capital y cartera."),
        ("roe", "ROE", "Utilidad / Patrimonio."),
        ("roa", "ROA", "Utilidad / Activo."),
    ]

    rows = []
    for key, label, note in catalog_keys:
        val = cur.get(key)
        if key in ("roe", "roa") and val is not None:
            display = f"{float(val) * 100:.1f}%"
            band_key = None
            ev = {"tone": "neutral", "zone": "—", "meaning": note, "bands": {}}
        elif key == "capital_trabajo":
            display = f"{val:,.0f}" if val is not None else "—"
            band_key = None
            ev = {"tone": "ok" if (val or 0) > 0 else "risk", "zone": "positivo" if (val or 0) > 0 else "negativo", "meaning": note, "bands": {}}
        elif key == "cobertura_intereses":
            display = f"{val:.2f}×" if val is not None else "—"
            band_key = None
            tone = "ok" if (val or 0) >= 1.5 else ("warn" if (val or 0) >= 1.0 else "risk")
            ev = {"tone": tone, "zone": "—", "meaning": note, "bands": {}}
        else:
            band_key = {
                "liquidez": "liquidez",
                "acida": "acida",
                "apalancamiento": "apalancamiento",
                "deuda_gerencial_patrimonio": "deuda_patrimonio",
                "z_score": "z_score",
            }.get(key)
            ev = evaluate_ratio(band_key, float(val) if val is not None else None) if band_key else {
                "tone": "neutral",
                "zone": "—",
                "meaning": note,
                "bands": {},
            }
            if key == "z_score":
                display = f"{val:.2f}" if val is not None else "—"
            else:
                display = f"{val:.2f}×" if val is not None else "—"

        d = delta(float(val) if val is not None else None, float(prv[key]) if prv.get(key) is not None else None)
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

    series = {
        "labels": focus,
        "liquidez": [derived_metrics(kpi_row(data, bu, p), bu, p, rates).get("liquidez") for p in focus],
        "apalancamiento": [derived_metrics(kpi_row(data, bu, p), bu, p, rates).get("apalancamiento") for p in focus],
        "acida": [derived_metrics(kpi_row(data, bu, p), bu, p, rates).get("acida") for p in focus],
        "z_score": [derived_metrics(kpi_row(data, bu, p), bu, p, rates).get("z_score") for p in focus],
        "deuda_gerencial_patrimonio": [
            derived_metrics(kpi_row(data, bu, p), bu, p, rates).get("deuda_gerencial_patrimonio") for p in focus
        ],
    }

    return {
        "status": "ok",
        "bu": bu,
        "bu_label": BU_LABEL.get(bu, bu),
        "period": latest,
        "prev_period": prev,
        "unit": data.get("unit") or "000 quetzales",
        "metrics": cur,
        "rows": rows,
        "series": series,
        "rates": rates,
    }
