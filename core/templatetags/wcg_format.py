"""Filtros de formato numérico WCG: miles con coma, decimales con punto."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django import template

register = template.Library()


def _to_decimal(value) -> Decimal | None:
    if value is None or value == "":
        return None
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(str(value).replace(",", ""))
    except (InvalidOperation, ValueError, TypeError):
        return None


def _format(value, decimals: int) -> str:
    num = _to_decimal(value)
    if num is None:
        return ""
    q = Decimal("1") if decimals <= 0 else Decimal("0." + ("0" * (decimals - 1)) + "1")
    quantized = num.quantize(q, rounding=ROUND_HALF_UP)
    # Python format: coma miles, punto decimal (regla WCG).
    return f"{quantized:,.{decimals}f}"


@register.filter(name="wcg_num")
def wcg_num(value, decimals=2):
    """Cifras simples (p. ej. dólares / Balón): separador de miles + N decimales."""
    try:
        d = int(decimals)
    except (TypeError, ValueError):
        d = 2
    return _format(value, max(0, d))


@register.filter(name="wcg_miles")
def wcg_miles(value, decimals=1):
    """Cifras en miles: separador de miles y 1 (o 0) decimal — evita 2 decimales."""
    try:
        d = int(decimals)
    except (TypeError, ValueError):
        d = 1
    return _format(value, max(0, min(d, 1)))
