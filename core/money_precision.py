"""Constantes y utilidades de precisión para montos PGC / imports (almacenamiento vs display)."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

MONEY_DECIMAL_PLACES = 6
MONEY_STORE_PLACES = Decimal("0.000001")
FX_STORE_PLACES = Decimal("0.000001")
INGRESOS_MILES_STORE_PLACES = MONEY_STORE_PLACES

# Tolerancia legada ingresos GTQ (miles USD); no usar en investment AP/PG.
LEGACY_INGRESOS_MILES_TOLERANCE = Decimal("0.05")


def quantize_store(value: Decimal | None, *, places: Decimal | None = None) -> Decimal | None:
    if value is None:
        return None
    q = places or MONEY_STORE_PLACES
    return Decimal(str(value)).quantize(q, rounding=ROUND_HALF_UP)


def money_equal(
    left,
    right,
    *,
    places: Decimal | None = None,
) -> bool:
    """Comparación en precisión de almacenamiento (evita falsos negativos por 2 dec)."""
    if left is None or right is None:
        return left is right
    q = places or MONEY_STORE_PLACES
    a = Decimal(str(left)).quantize(q, rounding=ROUND_HALF_UP)
    b = Decimal(str(right)).quantize(q, rounding=ROUND_HALF_UP)
    return a == b