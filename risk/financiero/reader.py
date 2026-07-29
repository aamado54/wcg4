"""Carga segura del dataset financiero combinado."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from django.conf import settings

logger = logging.getLogger(__name__)

DEFAULT_REL = Path("risk/financiero/seed/combined_series.json")
# Legacy/local rebuild path (gitignored under data/)
LEGACY_REL = Path("data/wcg/financiero/combined_series.json")


def _default_path() -> Path:
    custom = getattr(settings, "WCG_FINANCIERO_COMBINED", None)
    if custom:
        return Path(custom)
    base = Path(settings.BASE_DIR)
    seed = base / DEFAULT_REL
    if seed.exists():
        return seed
    return base / LEGACY_REL


def load_combined(path: str | Path | None = None) -> dict[str, Any]:
    """Always returns a dict. On failure: empty payload + errors list."""
    p = Path(path) if path else _default_path()
    empty: dict[str, Any] = {
        "unit": "000 quetzales",
        "periods": [],
        "recent_periods": [],
        "business_units": {"F": "Factoraje", "L": "Leasing", "I": "Insurance", "S": "Services", "T": "Total"},
        "kpis": {},
        "accounts_sample": [],
        "qf_extract_meta": {},
        "errors": [],
        "source_path": str(p),
        "status": "empty",
    }
    try:
        if not p.exists():
            empty["errors"].append(f"No se encontró {p}")
            return empty
        data = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            empty["errors"].append("JSON inválido (no es objeto)")
            return empty
        data.setdefault("errors", [])
        data["source_path"] = str(p)
        data["status"] = "ok" if data.get("kpis") else "empty"
        return data
    except Exception as exc:  # noqa: BLE001
        logger.exception("financiero load_combined failed")
        empty["errors"].append(str(exc))
        empty["status"] = "error"
        return empty
