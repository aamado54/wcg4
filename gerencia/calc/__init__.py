"""Fachada del motor gerencial — única entrada para vistas."""

from __future__ import annotations

from typing import Any

from risk.financiero.reader import load_combined

from .comando import build_comando
from .indices import build_indices_catalog
from .intermediacion import build_intermediacion
from .liquidez import build_estructura_board, build_liquidez_board
from .whatif import DEFAULT_DRIVERS, run_whatif


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
    """Agrega intermediación a trimestres calendario (pasivo / lectura)."""
    data = load_finance()
    periods = list(data.get("periods") or [])
    if not periods:
        return {"status": "empty", "rows": []}

    from .intermediacion import _intermediation_slice
    from .utils import rates_from_meta

    rates = rates_from_meta(data)
    # group YYYY-Qn
    buckets: dict[str, list[str]] = {}
    for p in periods:
        y, m = p.split("-")[0], int(p.split("-")[1])
        q = (m - 1) // 3 + 1
        key = f"{y}-Q{q}"
        buckets.setdefault(key, []).append(p)

    rows = []
    for qkey, ps in list(buckets.items())[-8:]:
        end = ps[-1]
        sl = _intermediation_slice(data, bu, end, rates, mode)
        rows.append(
            {
                "quarter": qkey,
                "end_period": end,
                "colocaciones": sl["colocaciones"],
                "margen_bruto": sl["margen_bruto"],
                "utilidad": sl["utilidad"],
                "months_in_q": len(ps),
            }
        )
    return {"status": "ok", "bu": bu, "mode": mode, "rows": rows}


__all__ = [
    "DEFAULT_DRIVERS",
    "load_finance",
    "board_intermediacion",
    "board_liquidez",
    "board_estructura",
    "board_indices",
    "board_comando",
    "board_whatif",
    "board_trimestral",
]
