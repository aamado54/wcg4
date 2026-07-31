"""Fachada del motor gerencial — única entrada para vistas."""

from __future__ import annotations

from typing import Any

from risk.financiero.reader import load_combined

from .comando import build_comando
from .indices import build_indices_catalog
from .intermediacion import _build_slices, build_intermediacion
from .liquidez import build_estructura_board, build_liquidez_board
from .utils import rates_from_meta
from .whatif import DEFAULT_DRIVERS, drivers_as_pct_display, format_pct, parse_pct, run_whatif


def load_finance() -> dict[str, Any]:
    data = load_combined()
    if data.get("kpis") and not data.get("status"):
        data["status"] = "ok"
    return data


def board_intermediacion(**kwargs) -> dict[str, Any]:
    return build_intermediacion(load_finance(), **kwargs)


def board_liquidez(**kwargs) -> dict[str, Any]:
    return build_liquidez_board(load_finance(), **kwargs)


def board_estructura(**kwargs) -> dict[str, Any]:
    return build_estructura_board(load_finance(), **kwargs)


def board_indices(**kwargs) -> dict[str, Any]:
    return build_indices_catalog(load_finance(), **kwargs)


def board_comando() -> dict[str, Any]:
    return build_comando(load_finance())


def board_whatif(**kwargs) -> dict[str, Any]:
    return run_whatif(load_finance(), **kwargs)


def board_trimestral(bu: str = "T", mode: str = "gerencial") -> dict[str, Any]:
    data = load_finance()
    periods = list(data.get("periods") or [])
    if not periods:
        return {"status": "empty", "rows": []}

    rates = rates_from_meta(data)
    slices = _build_slices(data, bu, periods, rates, mode)
    buckets: dict[str, list] = {}
    for s in slices:
        y, m = s["period"].split("-")[0], int(s["period"].split("-")[1])
        key = f"{y}-Q{(m - 1) // 3 + 1}"
        buckets.setdefault(key, []).append(s)

    rows = []
    for qkey in list(buckets.keys())[-10:]:
        ps = buckets[qkey]
        rows.append(
            {
                "quarter": qkey,
                "end_period": ps[-1]["period"],
                "colocaciones": ps[-1]["colocaciones"],
                "margen_bruto": sum(x["margen_bruto"] for x in ps),
                "utilidad": sum(x["utilidad"] for x in ps),
                "months_in_q": len(ps),
            }
        )
    return {"status": "ok", "bu": bu, "mode": mode, "rows": rows}


__all__ = [
    "DEFAULT_DRIVERS",
    "drivers_as_pct_display",
    "format_pct",
    "parse_pct",
    "load_finance",
    "board_intermediacion",
    "board_liquidez",
    "board_estructura",
    "board_indices",
    "board_comando",
    "board_whatif",
    "board_trimestral",
]
