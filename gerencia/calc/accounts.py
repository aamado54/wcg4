"""Cuentas reales EE.FF. para costos financieros y preferentes."""

from __future__ import annotations

from typing import Any

from .utils import n

# Costo de preferentes (balance): max(0, Δ) por mes.
DIV_PREF = "102020301"
# Stock de acciones preferentes (Inversionistas F / L).
PREF_STOCK = "301010106"
# Pagarés = intereses a inversionistas (P&L del mes).
PAGARES = "501010101"
# Bancos (P&L del mes).
BANK_F = ("701010106", "701010108", "701010104")
BANK_L = ("701010108", "701010104")

LABELS = {
    DIV_PREF: "Anticipos de dividendos (costo preferentes)",
    PREF_STOCK: "Inversionistas — acciones preferentes",
    PAGARES: "Intereses pagados a inversionistas (pagarés)",
    "701010106": "Intereses pagados a instituciones financieras",
    "701010108": "Intereses pagados a bancos del país",
    "701010104": "Gastos y comisiones bancarias",
}


def _index(data: dict) -> dict[tuple[str, str], dict]:
    cached = data.get("_account_index")
    if isinstance(cached, dict) and cached:
        return cached
    out: dict[tuple[str, str], dict] = {}
    for acc in data.get("accounts") or []:
        bu = str(acc.get("bu") or "").upper()
        code = str(acc.get("code") or "").strip()
        if bu and code:
            out[(bu, code)] = acc
    data["_account_index"] = out
    return out


def line(data: dict, bu: str, code: str, period: str) -> float:
    acc = _index(data).get((bu.upper(), str(code)))
    if not acc:
        return 0.0
    return n((acc.get("values") or {}).get(period))


def _prev_period(data: dict, period: str) -> str | None:
    periods = list(data.get("periods") or [])
    if period not in periods:
        return None
    i = periods.index(period)
    return periods[i - 1] if i > 0 else None


def max0_inc(data: dict, bu: str, code: str, period: str) -> float:
    cur = line(data, bu, code, period)
    prev_p = _prev_period(data, period)
    if prev_p is None:
        return max(0.0, cur)
    return max(0.0, cur - line(data, bu, code, prev_p))


def _bus(bu: str) -> tuple[str, ...]:
    bu = (bu or "T").upper()
    if bu == "T":
        return ("F", "L")
    if bu in ("F", "L"):
        return (bu,)
    return ()


def preferentes_stock(data: dict, bu: str, period: str) -> float:
    return sum(line(data, b, PREF_STOCK, period) for b in _bus(bu))


def div_pref_month(data: dict, bu: str, period: str) -> float:
    return sum(max0_inc(data, b, DIV_PREF, period) for b in _bus(bu))


def div_pref_ytd(data: dict, bu: str, period: str) -> float:
    year = (period or "")[:4]
    total = 0.0
    for p in data.get("periods") or []:
        if str(p).startswith(year) and str(p) <= period:
            total += div_pref_month(data, bu, p)
    return total


def p_and_l_month(data: dict, bu: str, code: str, period: str) -> float:
    return sum(line(data, b, code, period) for b in _bus(bu))


def bank_codes(bu: str) -> tuple[str, ...]:
    bu = (bu or "T").upper()
    if bu == "L":
        return BANK_L
    if bu == "F":
        return BANK_F
    # Total: union, applied per BU with that BU's set.
    return BANK_F


def bancos_month(data: dict, bu: str, period: str) -> float:
    total = 0.0
    for b in _bus(bu):
        codes = BANK_F if b == "F" else BANK_L
        total += sum(line(data, b, c, period) for c in codes)
    return total


def pagares_month(data: dict, bu: str, period: str) -> float:
    return p_and_l_month(data, bu, PAGARES, period)


def funding_detail(
    data: dict, bu: str, periods: list[str]
) -> dict[str, Any]:
    """Desglose real de costos financieros en un período (no estima)."""
    rows_pref = []
    rows_pag = []
    rows_bank = []
    tot_pref = tot_pag = tot_bank = 0.0
    by_bu: dict[str, dict[str, float]] = {}

    for b in _bus(bu):
        pref = sum(max0_inc(data, b, DIV_PREF, p) for p in periods)
        pag = sum(line(data, b, PAGARES, p) for p in periods)
        codes = BANK_F if b == "F" else BANK_L
        bank_parts = []
        bank_sum = 0.0
        for c in codes:
            amt = sum(line(data, b, c, p) for p in periods)
            bank_parts.append(
                {
                    "code": c,
                    "label": LABELS.get(c, c),
                    "amount": amt,
                    "bu": b,
                }
            )
            bank_sum += amt
        name = "Factoraje" if b == "F" else "Leasing"
        rows_pref.append(
            {
                "bu": b,
                "bu_label": name,
                "code": DIV_PREF,
                "label": f"{LABELS[DIV_PREF]} · {name}",
                "amount": pref,
                "rule": "max(0, Δ saldo) · 102020301",
            }
        )
        rows_pag.append(
            {
                "bu": b,
                "bu_label": name,
                "code": PAGARES,
                "label": f"{LABELS[PAGARES]} · {name}",
                "amount": pag,
            }
        )
        rows_bank.extend(bank_parts)
        tot_pref += pref
        tot_pag += pag
        tot_bank += bank_sum
        by_bu[b] = {"preferentes": pref, "pagares": pag, "bancos": bank_sum}

    return {
        "periods": periods,
        "preferentes": rows_pref,
        "pagares": rows_pag,
        "bancos": rows_bank,
        "totals": {
            "preferentes": tot_pref,
            "pagares": tot_pag,
            "bancos": tot_bank,
            "all": tot_pref + tot_pag + tot_bank,
        },
        "by_bu": by_bu,
        "note": (
            "Pagarés = intereses a inversionistas (501010101). "
            "Preferentes = incrementos de anticipo de dividendos (102020301), "
            "max(0, Δ). Bancos = intereses y comisiones (701010106 / 108 / 104). "
            "El cuadro de margen sigue usando costos estimados (tasa × stock)."
        ),
    }
