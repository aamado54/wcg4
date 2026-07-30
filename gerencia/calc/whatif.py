"""What-if simplificado (inspirado en hoja Control de wc-mod5c)."""

from __future__ import annotations

from typing import Any

from .indices import derived_metrics
from .intermediacion import _intermediation_slice
from .utils import BU_LABEL, fmt, kpi_row, rates_from_meta


DEFAULT_DRIVERS = {
    "growth_cartera_f": 0.10,
    "growth_cartera_l": 0.08,
    "rate_activa_f": 0.18,
    "rate_activa_l": 0.14,
    "rate_pasiva_inv": 0.09,
    "rate_pasiva_bancos": 0.08,
    "growth_overhead": 0.05,
}


def run_whatif(data: dict, drivers: dict[str, float] | None = None, bu: str = "T") -> dict[str, Any]:
    periods = list(data.get("periods") or [])
    if not periods:
        return {"status": "empty"}

    d = {**DEFAULT_DRIVERS, **(drivers or {})}
    latest = periods[-1]
    base_rates = rates_from_meta(data)
    rates = {
        "activa_f": float(d["rate_activa_f"]),
        "activa_l": float(d["rate_activa_l"]),
        "pasiva_inv_f": float(d["rate_pasiva_inv"]),
        "pasiva_inv_l": float(d["rate_pasiva_inv"]),
        "pasiva_bancos_f": float(d["rate_pasiva_bancos"]),
        "pasiva_bancos_l": float(d["rate_pasiva_bancos"]),
    }

    base = _intermediation_slice(data, bu, latest, base_rates, "gerencial")

    # Proyectar un "mes+12" simplificado: cartera crece, fondeo acompaña ~80% del crecimiento
    g = float(d["growth_cartera_f"]) if bu != "L" else float(d["growth_cartera_l"])
    if bu == "T":
        g = 0.6 * float(d["growth_cartera_f"]) + 0.4 * float(d["growth_cartera_l"])

    proj_cartera = base["colocaciones"] * (1 + g)
    proj_captacion = base["captaciones"] * (1 + g * 0.8)
    activa = rates["activa_f"] if bu != "L" else rates["activa_l"]
    if bu == "T":
        activa = 0.6 * rates["activa_f"] + 0.4 * rates["activa_l"]
    pasiva = 0.55 * rates["pasiva_bancos_f"] + 0.45 * rates["pasiva_inv_f"]

    productos = proj_cartera * activa
    costos = proj_captacion * pasiva
    margen = productos - costos
    overhead = base["overhead_neto"] * (1 + float(d["growth_overhead"]))
    util = margen - overhead

    m = derived_metrics(kpi_row(data, bu, latest), bu, latest, rates)
    # Liquidez proyectada naive: AC crece con cartera, PC con captación parcial
    ac0 = float(m.get("activo_corriente") or 0)
    pc0 = float(m.get("pasivo_corriente") or 1)
    ac1 = ac0 * (1 + g * 0.9)
    pc1 = pc0 * (1 + g * 0.75)
    liq_proj = ac1 / pc1 if pc1 else None

    return {
        "status": "ok",
        "bu": bu,
        "bu_label": BU_LABEL.get(bu, bu),
        "base_period": latest,
        "drivers": d,
        "base": {
            "cartera": base["colocaciones"],
            "margen": base["margen_bruto"],
            "utilidad": base["utilidad"],
            "liquidez": m.get("liquidez"),
        },
        "projected": {
            "horizon": "12 meses (simplificado)",
            "cartera": proj_cartera,
            "margen": margen,
            "utilidad": util,
            "liquidez": liq_proj,
            "productos": productos,
            "costos": costos,
            "overhead": overhead,
        },
        "deltas": {
            "cartera": (proj_cartera - base["colocaciones"]) / abs(base["colocaciones"] or 1),
            "margen": (margen - base["margen_bruto"]) / abs(base["margen_bruto"] or 1),
            "utilidad": (util - base["utilidad"]) / abs(base["utilidad"] or 1),
        },
        "summary_rows": [
            {"label": "Cartera", "base": fmt(base["colocaciones"]), "proj": fmt(proj_cartera)},
            {"label": "Margen intermediación", "base": fmt(base["margen_bruto"]), "proj": fmt(margen)},
            {"label": "Utilidad gerencial", "base": fmt(base["utilidad"]), "proj": fmt(util)},
            {
                "label": "Liquidez",
                "base": f"{m['liquidez']:.2f}×" if m.get("liquidez") is not None else "—",
                "proj": f"{liq_proj:.2f}×" if liq_proj is not None else "—",
            },
        ],
    }
