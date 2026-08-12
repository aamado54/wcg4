"""Tasa de interés en clientes nuevos: Investment anual; Factoraje/Leasing mensual."""

from __future__ import annotations

import csv
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

RATE_ANNUAL = "annual"
RATE_MONTHLY = "monthly"


def _norm_header(name: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", "", (name or "").strip().lower())


def clean_cell(raw) -> str:
    s = "" if raw is None else str(raw).strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        s = s[1:-1].strip()
    return s


def row_get(row: dict, *aliases: str) -> str:
    wanted = {_norm_header(a) for a in aliases}
    for key, val in row.items():
        if _norm_header(key) in wanted:
            return clean_cell(val)
    return ""


def parse_rate(raw: str) -> Decimal | None:
    text = clean_cell(raw)
    if not text:
        return None
    try:
        return Decimal(text.replace("%", "").replace(",", "").strip())
    except (InvalidOperation, ValueError):
        return None


def mentions_investment(text: str) -> bool:
    blob = (text or "").lower()
    return any(
        x in blob
        for x in (
            "investment",
            "investments",
            "invest",
            "inversiones",
            "inversion",
            "inversión",
        )
    )


def mentions_lending(text: str) -> bool:
    blob = (text or "").lower()
    return any(
        x in blob
        for x in ("leasing", "factoraje", "factoring", "factor")
    )


def rate_basis_for(une=None, raw_une: str = "") -> str:
    """Investment / inversiones → anual. Leasing / Factoraje → mensual."""
    une_code = str(getattr(une, "code", "") or "")
    blob = f"{une_code} {raw_une or ''}"
    if mentions_investment(blob) or une_code.upper() == "INVESTMENT":
        return RATE_ANNUAL
    if mentions_lending(blob) or une_code.upper() in ("LEASING", "FACTORING"):
        return RATE_MONTHLY
    return ""


def apply_rate_basis(row) -> str:
    une = getattr(row, "une", None)
    une_id = getattr(row, "une_id", None)
    if une is not None and une_id and getattr(une, "pk", None) != une_id:
        une = None
    basis = rate_basis_for(une, getattr(row, "raw_une_value", "") or "")
    if not basis and une_id and une is None:
        code = ""
        try:
            from core.models import UNE

            code = UNE.objects.filter(pk=une_id).values_list("code", flat=True).first() or ""
        except Exception:
            code = ""
        basis = rate_basis_for(type("U", (), {"code": code})(), getattr(row, "raw_une_value", "") or "")
    row.rate_basis = basis
    return basis


def match_key(nit: str, operation: str, year: int, month: int) -> tuple[str, str, int, int]:
    return (" ".join((nit or "").split()), " ".join((operation or "").split()), year, month)


def sniff_open(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=[",", "\t", ";"])
    except csv.Error:
        dialect = csv.excel
    return csv.DictReader(text.splitlines(), dialect=dialect)


def source_row_index(path: Path) -> dict[tuple[str, str, int, int], dict]:
    """(nit, operacion, year, month) → campos recuperables del archivo fuente."""
    out: dict[tuple[str, str, int, int], dict] = {}
    try:
        reader = sniff_open(path)
    except Exception:
        return out
    for row in reader:
        anio_mes = row_get(row, "AnioMes", "anio_mes", "periodo")
        if not anio_mes:
            continue
        try:
            year_s, month_s = anio_mes.replace("-", "/").split("/")
            year, month = int(year_s), int(month_s)
        except Exception:
            continue
        amount = None
        amount_raw = row_get(row, "Monto", "MONTO")
        if amount_raw:
            try:
                amount = Decimal(amount_raw.replace(",", "")) / Decimal("1000")
            except (InvalidOperation, ValueError):
                amount = None
        payload = {
            "interest_rate": parse_rate(row_get(row, "Porcentaje", "Tasa", "Rate")),
            "amount": amount,
            "currency": row_get(row, "Moneda", "MONEDA"),
            "client_name": row_get(row, "Cliente", "CLIENTE", "nombre"),
            "nit": row_get(row, "NIT", "Nit"),
            "operation_code": row_get(row, "Operacion", "Operación", "OPERACION"),
            "raw_une": row_get(row, "UNE", "une"),
        }
        if payload["interest_rate"] is None and payload["amount"] is None:
            continue
        out[
            match_key(payload["nit"], payload["operation_code"], year, month)
        ] = payload
    return out
