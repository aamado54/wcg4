"""Normalización de códigos de moneda en importaciones."""

from __future__ import annotations

from core.models import Currency

# Alias de archivo → código canónico en catálogo.
CURRENCY_ALIASES: dict[str, str] = {
    "Q": "GTQ",
    "QUETZAL": "GTQ",
    "QUETZALES": "GTQ",
    "$": "USD",
    "US$": "USD",
}


def normalize_currency_code(raw: str | None) -> tuple[str, str | None]:
    """
    Devuelve (código_canónico, warning_o_None).

    Si el archivo trae ``Q``, se trata como ``GTQ`` y se genera un warning
    para corregir la fuente (no se ignora el dato).
    """
    code = (raw or "").strip().upper()
    if not code:
        return "", None
    if code in CURRENCY_ALIASES:
        canon = CURRENCY_ALIASES[code]
        warning = (
            f"Moneda '{raw.strip()}' interpretada como {canon}. "
            f"Corrija el archivo fuente para usar {canon}."
        )
        return canon, warning
    return code, None


def resolve_currency(
    raw: str | None,
    currencies_by_code: dict[str, Currency] | None = None,
) -> tuple[Currency | None, str | None]:
    """Resuelve Currency FK + warning de alias."""
    code, warning = normalize_currency_code(raw)
    if not code:
        return None, warning
    if currencies_by_code is not None:
        return currencies_by_code.get(code), warning
    return Currency.objects.filter(code__iexact=code).first(), warning
