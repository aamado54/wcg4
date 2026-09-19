"""Filtros de formato numérico WCG: miles con coma, decimales con punto."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

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


@register.filter(name="methodology_lead")
def methodology_lead(value: str) -> str:
    """Primera cláusula antes de ': ' en semibold (texto metodología escenario)."""
    text = str(value or "")
    if ": " not in text:
        return conditional_escape(text)
    topic, body = text.split(": ", 1)
    return mark_safe(
        f'<span class="esc-method-topic">{conditional_escape(topic)}</span>: '
        f"{conditional_escape(body)}"
    )
