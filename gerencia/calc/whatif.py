"""What-if simplificado (inspirado en hoja Control de wc-mod5c)."""

from __future__ import annotations

from typing import Any

from .accounts import div_pref_ytd, preferentes_stock
from .indices import derived_metrics
from .intermediacion import _intermediation_slice
from .money import fmt_money
from .utils import BU_LABEL, kpi_row, rates_from_meta


DEFAULT_DRIVERS = {
    "growth_cartera_f": 0.10,
    "growth_cartera_l": 0.08,
    "rate_activa_f": 0.18,
    "rate_activa_l": 0.14,
    "rate_pasiva_inv": 0.09,
    "rate_pasiva_bancos": 0.08,
    "growth_overhead": 0.05,
}


def format_pct(fraction: float) -> str:
    """10% → '10'; 5.3% → '5.3'; sin ceros de relleno."""
    pct = float(fraction) * 100.0
    text = f"{pct:.10f}".rstrip("0").rstrip(".")
    return text if text else "0"


def parse_pct(raw: str | float | None, fallback: float) -> float:
    """Acepta '10' o '10%' o 0.10; interpreta números ≥1 (y ≠ fracción típica) como %."""
    if raw is None or raw == "":
        return fallback
    try:
        s = str(raw).strip().replace("%", "").replace(",", ".")
        v = float(s)
    except (TypeError, ValueError):
        return fallback
    # Si el usuario escribe 10 → 10%; si escribe 0.18 → puede ser 0.18% o 18%?
    # Convención UI: siempre porcentaje (10 = 10%).
    return v / 100.0


def drivers_as_pct_display(drivers: dict[str, float]) -> dict[str, str]:
    return {k: format_pct(v) for k, v in drivers.items()}


def run_whatif(
    data: dict,
    drivers: dict[str, float] | None = None,
    bu: str = "T",
    ccy: str = "GTQ",
    fx: float | None = None,
) -> dict[str, Any]:
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

    all_p = periods
    prev = all_p[-2] if len(all_p) >= 2 else None
    prev_m = (
        derived_metrics(
            kpi_row(data, bu, prev),
            bu,
            prev,
            base_rates,
            inv_proxy=preferentes_stock(data, bu, prev),
            div_ytd=div_pref_ytd(data, bu, prev),
        )
        if prev
        else {}
    )
    base = _intermediation_slice(
        data,
        bu,
        latest,
        base_rates,
        "gerencial",
        prev_period=prev,
        prev_util_c=prev_m.get("utilidades"),
        prev_util_g=prev_m.get("util_gerencial"),
    )

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

    m = derived_metrics(
        kpi_row(data, bu, latest),
        bu,
        latest,
        rates,
        vista="gerencial",
        inv_proxy=preferentes_stock(data, bu, latest),
        div_ytd=div_pref_ytd(data, bu, latest),
    )
    fm = lambda v: fmt_money(v, ccy, fx)
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
        "drivers_pct": drivers_as_pct_display(d),
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
        "raw_rows": [
            {"key": "cartera", "label": "Cartera", "base": base["colocaciones"], "proj": proj_cartera, "money": True},
            {"key": "margen", "label": "Margen intermediación", "base": base["margen_bruto"], "proj": margen, "money": True},
            {"key": "utilidad", "label": "Utilidad gerencial", "base": base["utilidad"], "proj": util, "money": True},
            {"key": "liquidez", "label": "Liquidez", "base": m.get("liquidez"), "proj": liq_proj, "money": False},
        ],
        "summary_rows": [
            {"label": "Cartera", "base": fm(base["colocaciones"]), "proj": fm(proj_cartera)},
            {"label": "Margen intermediación", "base": fm(base["margen_bruto"]), "proj": fm(margen)},
            {"label": "Utilidad gerencial", "base": fm(base["utilidad"]), "proj": fm(util)},
            {
                "label": "Liquidez",
                "base": f"{m['liquidez']:.2f}×" if m.get("liquidez") is not None else "—",
                "proj": f"{liq_proj:.2f}×" if liq_proj is not None else "—",
            },
        ],
    }
