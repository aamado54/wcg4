"""Peers de referencia para liquidez / apalancamiento."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


@lru_cache(maxsize=1)
def load_peers() -> dict[str, Any]:
    path = Path(__file__).resolve().parent.parent / "data" / "peers.json"
    return json.loads(path.read_text(encoding="utf-8"))


def peers_with_self(liquidez: float | None, apalancamiento: float | None, period: str) -> list[dict]:
    raw = load_peers()
    out: list[dict] = []
    for p in raw.get("peers") or []:
        row = dict(p)
        if row.get("kind") == "self":
            row["liquidez"] = liquidez
            row["apalancamiento"] = apalancamiento
            row["period"] = period
        out.append(row)
    return out
