"""Normalización de columnas y lectura de celdas."""

from __future__ import annotations

import re
import unicodedata
from decimal import Decimal, InvalidOperation

import pandas as pd

from .base import ImportValidationError, cell_str


def _norm_header(name: str) -> str:
    s = unicodedata.normalize("NFKD", str(name))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.strip().lower()
    s = re.sub(r"[^\w]+", "_", s)
    return s.strip("_")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [_norm_header(c) for c in out.columns]
    return out


def pick(row: pd.Series, *aliases: str) -> str:
    for alias in aliases:
        key = _norm_header(alias)
        if key in row.index:
            val = cell_str(row.get(key))
            if val:
                return val
    return ""


def pick_decimal(row: pd.Series, *aliases: str, default: str = "0") -> Decimal:
    raw = pick(row, *aliases) or default
    try:
        cleaned = raw.replace(",", "").replace("Q", "").replace("$", "").strip()
        if cleaned in ("", "-", "nan"):
            return Decimal(default)
        return Decimal(cleaned)
    except (InvalidOperation, AttributeError):
        return Decimal(default)


def pick_int(row: pd.Series, *aliases: str, default: int = 0) -> int:
    try:
        return int(pick_decimal(row, *aliases, default=str(default)))
    except (ValueError, TypeError):
        return default


def require_any(df: pd.DataFrame, groups: list[list[str]]) -> None:
    cols = set(df.columns)
    missing_groups = []
    for group in groups:
        keys = {_norm_header(g) for g in group}
        if not keys.intersection(cols):
            missing_groups.append(" o ".join(group))
    if missing_groups:
        raise ImportValidationError(
            "Faltan columnas (al menos una por grupo): " + "; ".join(missing_groups)
        )
