from __future__ import annotations

from decimal import Decimal
from typing import Any


def dec(value) -> Decimal:
    if value is None:
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


def pct_change(curr, prev) -> str:
    c, p = dec(curr), dec(prev)
    if p == 0:
        if c == 0:
            return "0%"
        return "n/d (base 0)"
    change = ((c - p) / abs(p)) * Decimal("100")
    sign = "+" if change > 0 else ""
    return f"{sign}{change.quantize(Decimal('0.1'))}%"


def delta(curr, prev) -> Decimal:
    return dec(curr) - dec(prev)


def fmt_num(value, places: int = 1) -> str:
    d = dec(value)
    q = Decimal("1").scaleb(-places)
    return str(d.quantize(q))


def period_label(year: int, month: int) -> str:
    months = [
        "",
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ]
    return f"{months[month]} {year}"


def ym_key(year: int, month: int) -> str:
    return f"{year}-{month:02d}"


def previous_month(year: int, month: int) -> tuple[int, int]:
    if month <= 1:
        return year - 1, 12
    return year, month - 1


def sorted_unique_periods(pairs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return sorted(set(pairs))


def limit_rows(rows: list[Any], n: int) -> list[Any]:
    if n <= 0:
        return rows
    return rows[:n]
