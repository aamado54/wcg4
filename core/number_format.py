"""Formato numérico WCG: coma miles, punto decimal, hasta N decimales sin ceros finales."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def _to_decimal(value) -> Decimal | None:
    if value is None or value == "":
        return None
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(str(value).replace(",", ""))
    except (InvalidOperation, ValueError, TypeError):
        return None


def format_wcg_amount(value, max_decimal_places: int = 3) -> str:
    if value is None:
        return ""
    num = _to_decimal(value)
    if num is None:
        return ""
    places = max(0, int(max_decimal_places))
    q = Decimal(10) ** -places if places else Decimal("1")
    normalized = num.quantize(q, rounding=ROUND_HALF_UP)
    text = f"{normalized:,.{places}f}" if places else f"{normalized:,.0f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text
