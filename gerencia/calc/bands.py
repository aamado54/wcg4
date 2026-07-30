"""Bandas de referencia y evaluación de tono para ratios gerenciales."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


@lru_cache(maxsize=1)
def load_bands() -> dict[str, Any]:
    path = Path(__file__).resolve().parent.parent / "data" / "bands.json"
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_ratio(key: str, value: float | None) -> dict[str, Any]:
    bands = load_bands()
    cfg = (bands.get("ratios") or {}).get(key) or {}
    if value is None or not cfg:
        return {
            "key": key,
            "value": value,
            "tone": "neutral",
            "zone": "n/d",
            "label": cfg.get("label") or key,
            "meaning": "Sin dato.",
            "bands": cfg,
        }

    lc = float(cfg["low_critical"])
    lw = float(cfg["low_warn"])
    ol = float(cfg["optimal_low"])
    oh = float(cfg["optimal_high"])
    hw = float(cfg["high_warn"])
    hc = float(cfg["high_critical"])

    if value < lc:
        tone, zone, meaning = "risk", "muy bajo", cfg.get("meaning_low")
    elif value < lw:
        tone, zone, meaning = "warn", "bajo", cfg.get("meaning_low")
    elif value > hc:
        tone, zone, meaning = "risk", "muy alto", cfg.get("meaning_high")
    elif value > hw:
        tone, zone, meaning = "warn", "alto", cfg.get("meaning_high")
    elif ol <= value <= oh:
        tone, zone, meaning = "ok", "óptimo", cfg.get("meaning_ok")
    else:
        tone, zone, meaning = "ok", "aceptable", cfg.get("meaning_ok")

    return {
        "key": key,
        "value": value,
        "tone": tone,
        "zone": zone,
        "label": cfg.get("label") or key,
        "unit": cfg.get("unit") or "×",
        "meaning": meaning or "",
        "bands": {
            "optimal_low": ol,
            "optimal_high": oh,
            "low_warn": lw,
            "high_warn": hw,
            "low_critical": lc,
            "high_critical": hc,
        },
    }


def band_chart_guides(key: str) -> list[dict[str, Any]]:
    """Horizontal guide lines for Chart.js (optimal band edges)."""
    bands = load_bands()
    cfg = (bands.get("ratios") or {}).get(key) or {}
    if not cfg:
        return []
    return [
        {"label": f"Óptimo ↓ {cfg['optimal_low']}", "value": float(cfg["optimal_low"]), "color": "#2f5c4e55"},
        {"label": f"Óptimo ↑ {cfg['optimal_high']}", "value": float(cfg["optimal_high"]), "color": "#2f5c4e55"},
        {"label": f"Alerta baja {cfg['low_warn']}", "value": float(cfg["low_warn"]), "color": "#a67c2a44"},
        {"label": f"Alerta alta {cfg['high_warn']}", "value": float(cfg["high_warn"]), "color": "#a67c2a44"},
    ]
