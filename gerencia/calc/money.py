"""Moneda de presentación Centro Gerencial (000 QTZ ↔ 000 USD)."""

from __future__ import annotations

from typing import Any

from .utils import fmt, n


def fx_factor(ccy: str, fx: float | None) -> float:
    if (ccy or "GTQ").upper() == "USD" and fx and float(fx) > 0:
        return 1.0 / float(fx)
    return 1.0


def scale(v: Any, factor: float) -> float | None:
    if v is None or v == "":
        return None
    try:
        return float(v) * factor
    except (TypeError, ValueError):
        return None


def fmt_money(v: Any, ccy: str = "GTQ", fx: float | None = None, digits: int = 0) -> str:
    return fmt(scale(v, fx_factor(ccy, fx)), digits)


def unit_label(ccy: str) -> str:
    return "000 USD" if (ccy or "GTQ").upper() == "USD" else "000 QTZ"


def scale_chart(chart: dict | None, factor: float) -> dict:
    if not chart:
        return {}
    out = dict(chart)
    datasets = []
    for ds in chart.get("datasets") or []:
        nd = dict(ds)
        nd["data"] = [scale(x, factor) if x is not None else None for x in (ds.get("data") or [])]
        datasets.append(nd)
    out["datasets"] = datasets
    return out


def latest_usd_gtq(period: str | None = None) -> float | None:
    try:
        from pgc.models import MonthlyExchangeRate
    except Exception:
        return None
    qs = MonthlyExchangeRate.objects.all()
    if period and "-" in period:
        try:
            y, m = int(period[:4]), int(period.split("-")[1])
            row = qs.filter(year=y, month=m).first()
            if row:
                return n(row.usd_to_gtq) or None
        except (TypeError, ValueError):
            pass
    row = qs.order_by("-year", "-month").first()
    if row:
        return n(row.usd_to_gtq) or None
    return 7.75
