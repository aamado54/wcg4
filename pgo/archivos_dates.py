"""Fechas en exports «Archivos» (Planner / WCG Créditos).

- Inicio: suele venir como texto con día primero (DD-MM-YY).
- Entrega / resultado: suele venir como fecha Excel o texto con mes primero (MM-DD-YY).
"""

from __future__ import annotations

import re
from datetime import date, datetime, time

import pandas as pd

_INICIO_HINTS = frozenset(
    {
        "fecha_inicio",
        "fechainicio",
        "fecha_de_inicio",
        "inicio",
        "fecha_ingreso",
        "fecha_registro",
    }
)
_ENTREGA_HINTS = frozenset(
    {
        "fecha_entrega",
        "fechaentrega",
        "fecha_de_entrega",
        "fecha_entrega_resultado",
        "fecha_resultado",
        "entrega",
        "resultado",
        "fecha_cierre",
    }
)


def column_role(normalized_name: str) -> str | None:
    n = normalized_name.strip().lower()
    if n in _INICIO_HINTS or "inicio" in n and "entrega" not in n:
        return "inicio"
    if n in _ENTREGA_HINTS or "entrega" in n or n.endswith("_resultado"):
        return "entrega"
    return None


def _expand_year(y: int) -> int:
    if y < 100:
        return 2000 + y if y < 70 else 1900 + y
    return y


def _from_parts(d: int, m: int, y: int) -> date | None:
    try:
        return date(_expand_year(y), m, d)
    except ValueError:
        return None


def _parse_text_with_order(text: str, day_first: bool) -> date | None:
    text = text.strip()
    if not text or text.lower() in ("nan", "nat", "none", ""):
        return None
    m = re.match(r"^(\d{1,2})[./\-](\d{1,2})[./\-](\d{2,4})(?:\s+\d{1,2}:\d{2})?", text)
    if not m:
        return None
    a, b, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if day_first:
        return _from_parts(a, b, y)
    return _from_parts(b, a, y)


def parse_inicio(value) -> datetime | None:
    """Campo texto: prioridad DD-MM-YY."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, datetime):
        return value.replace(tzinfo=None) if value.tzinfo else value
    if isinstance(value, date):
        return datetime.combine(value, time.min)
    if hasattr(value, "to_pydatetime"):
        try:
            dt = value.to_pydatetime()
            return dt.replace(tzinfo=None) if getattr(dt, "tzinfo", None) else dt
        except Exception:
            pass
    text = str(value).strip()
    d = _parse_text_with_order(text, day_first=True)
    if d:
        return datetime.combine(d, time.min)
    d = _parse_text_with_order(text, day_first=False)
    if d:
        return datetime.combine(d, time.min)
    try:
        dt = pd.to_datetime(text, dayfirst=True).to_pydatetime()
        return dt.replace(tzinfo=None) if getattr(dt, "tzinfo", None) else dt
    except Exception:
        return None


def parse_entrega(value) -> datetime | None:
    """Campo fecha/resultado: prioridad MM-DD-YY; desempate si parte1 > 12."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, datetime):
        return value.replace(tzinfo=None) if value.tzinfo else value
    if isinstance(value, date):
        return datetime.combine(value, time.min)
    if hasattr(value, "to_pydatetime"):
        try:
            dt = value.to_pydatetime()
            return dt.replace(tzinfo=None) if getattr(dt, "tzinfo", None) else dt
        except Exception:
            pass
    text = str(value).strip()
    m = re.match(r"^(\d{1,2})[./\-](\d{1,2})[./\-](\d{2,4})", text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        y = int(m.group(3))
        if a > 12 and b <= 12:
            d = _from_parts(a, b, y)
        elif b > 12 and a <= 12:
            d = _from_parts(b, a, y)
        else:
            d = _parse_text_with_order(text, day_first=False) or _parse_text_with_order(
                text, day_first=True
            )
        if d:
            return datetime.combine(d, time.min)
    try:
        dt = pd.to_datetime(text, dayfirst=False).to_pydatetime()
        return dt.replace(tzinfo=None) if getattr(dt, "tzinfo", None) else dt
    except Exception:
        try:
            dt = pd.to_datetime(text, dayfirst=True).to_pydatetime()
            return dt.replace(tzinfo=None) if getattr(dt, "tzinfo", None) else dt
        except Exception:
            return None
