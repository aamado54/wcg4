"""Utilidades compartidas del motor gerencial."""

from __future__ import annotations

from typing import Any


BU_ORDER = ("T", "F", "L")
BU_LABEL = {
    "T": "Total WCG",
    "F": "Factoraje",
    "L": "Leasing",
    "I": "Insurance",
    "S": "Services",
}


def n(v: Any, default: float = 0.0) -> float:
    try:
        if v is None or v == "":
            return default
        return float(v)
    except (TypeError, ValueError):
        return default


def fmt(v: float | None, digits: int = 0) -> str:
    if v is None:
        return "—"
    if digits == 0:
        return f"{v:,.0f}"
    return f"{v:,.{digits}f}"


def pct(v: float | None, digits: int = 1) -> str:
    if v is None:
        return "—"
    return f"{v * 100:.{digits}f}%"


def delta(cur: float | None, prev: float | None) -> float | None:
    if cur is None or prev is None or prev == 0:
        return None
    return (cur - prev) / abs(prev)


def kpi_row(data: dict, bu: str, period: str) -> dict:
    from risk.financiero.quality import enrich_kpi_row

    return enrich_kpi_row(((data.get("kpis") or {}).get(bu) or {}).get(period) or {})


def last_n(periods: list[str], n: int = 12) -> list[str]:
    return periods[-n:] if len(periods) > n else list(periods)


def month_of(period: str) -> int:
    if period and "-" in period:
        try:
            return int(period.split("-")[1])
        except ValueError:
            return 6
    return 6


def rates_from_meta(data: dict) -> dict[str, float]:
    qf = data.get("qf_extract_meta") or {}
    rates = ((qf.get("control_defaults") or {}).get("rates") or {})
    return {
        "activa_f": n((rates.get("activa_cartera") or {}).get("F"), 0.18),
        "activa_l": n((rates.get("activa_cartera") or {}).get("L"), 0.14),
        "pasiva_inv_f": n((rates.get("pasiva_inversionistas") or {}).get("F"), 0.09),
        "pasiva_inv_l": n((rates.get("pasiva_inversionistas") or {}).get("L"), 0.095),
        "pasiva_bancos_f": n((rates.get("pasiva_bancos") or {}).get("F"), 0.08),
        "pasiva_bancos_l": n((rates.get("pasiva_bancos") or {}).get("L"), 0.08),
    }
