"""Mapeo de columnas reales (CSV/XLSX) a nombres canónicos de importación."""

from __future__ import annotations

import re
import unicodedata

import pandas as pd

from .import_base import cell_str


def _norm_header(name: str) -> str:
    s = unicodedata.normalize("NFKD", str(name))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("\ufeff", "").strip()
    # NombreCliente / Client Name → snake_case usable por aliases
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    s = s.lower()
    s = re.sub(r"[^\w]+", "_", s)
    return s.strip("_")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [_norm_header(c) for c in df.columns]
    return df


def pick(row: pd.Series, *aliases: str) -> str:
    """Primer alias presente en la fila (columnas ya normalizadas)."""
    for alias in aliases:
        key = _norm_header(alias)
        if key in row.index:
            val = cell_str(row.get(key))
            if val:
                return val
    return ""


def pick_decimal(row: pd.Series, *aliases: str, default: str = "0"):
    from decimal import Decimal, InvalidOperation

    raw = pick(row, *aliases) or default
    try:
        return Decimal(raw.replace(",", "").replace("Q", "").replace("$", "").strip())
    except (InvalidOperation, AttributeError):
        return Decimal(default)


def pick_int(row: pd.Series, *aliases: str, default: int = 0) -> int:
    try:
        return int(pick_decimal(row, *aliases, default=str(default)))
    except (ValueError, TypeError):
        return default


def require_any(df: pd.DataFrame, groups: list[list[str]]) -> None:
    """Cada grupo es OR de columnas; todos los grupos deben resolverse."""
    cols = set(df.columns)
    missing_groups = []
    for group in groups:
        keys = {_norm_header(g) for g in group}
        if not keys.intersection(cols):
            missing_groups.append(" o ".join(group))
    if missing_groups:
        from .import_base import ImportValidationError

        raise ImportValidationError(
            "Faltan columnas (al menos una por grupo): " + "; ".join(missing_groups)
        )
