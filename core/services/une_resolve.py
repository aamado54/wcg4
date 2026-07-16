"""Resolución de UNE a partir de texto crudo de importaciones."""

from __future__ import annotations


def _mentions_investment(raw_lower: str) -> bool:
    return (
        "investment" in raw_lower
        or "investments" in raw_lower
        or "invest" in raw_lower
        or "inversiones" in raw_lower
        or "inversion" in raw_lower
        or "inversión" in raw_lower
    )


def resolve_une_from_text(raw_value, aliases: dict, unes_by_code: dict):
    """
    Regla de negocio: si el valor crudo menciona Investment/Inversiones,
    SIEMPRE es UNE Inversiones — aunque también diga Factoring/Leasing
    y aunque exista un alias incorrecto.
    """
    if not raw_value:
        return None

    raw_clean = str(raw_value).strip()
    if not raw_clean:
        return None

    raw_upper = raw_clean.upper()
    raw_lower = raw_clean.lower()

    if _mentions_investment(raw_lower):
        return unes_by_code.get("INVESTMENT")

    if raw_upper in aliases:
        return aliases[raw_upper]

    if "factoring" in raw_lower or "factoraje" in raw_lower or "factor" in raw_lower:
        return unes_by_code.get("FACTORING")

    if "leasing" in raw_lower:
        return unes_by_code.get("LEASING")

    if (
        "insurance" in raw_lower
        or "seguros" in raw_lower
        or "seguro" in raw_lower
    ):
        return unes_by_code.get("INSURANCE")

    return unes_by_code.get(raw_upper)
