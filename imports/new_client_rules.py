"""Reglas PGC para conteo de clientes nuevos e inversiones intercompañía del grupo WC."""

from __future__ import annotations

import re
from collections import defaultdict

from core.models import UNE

# Categorías de clientes nuevos que sí suman a la meta INVESTMENT (filas con ContratosPrevios=0).
INVESTMENT_CLIENT_CATEGORIES = (
    "INVESTMENT - WC LEASING",
    "INVESTMENT - WORKING CAPITAL HOLDING GROUP",
)

WC_GROUP_NAME_MARKERS = (
    "WORKING CAPITAL LEASING",
    "WORKING CAPITAL INSURANCE",
    "WORKING CAPITAL HOLDING GROUP",
    "WORKING CAPITAL FACTORING",
    "WORKING CAPITAL SERVICES",
    "WORKING CAPITAL GROUP",
)

WC_GROUP_NIT_PREFIXES = (
    "11339813",  # WCL
    "11512835",  # WCI corredores (variantes 115128352)
    "155753996",  # WCHG
)


def normalize_nit(raw: str | None) -> str:
    if not raw:
        return ""
    text = str(raw).strip().upper()
    text = re.sub(r"\s+", "", text)
    return "".join(ch for ch in text if ch.isdigit())


def normalize_operation_code(raw: str | None) -> str:
    return re.sub(r"\s+", "", (raw or "").strip()).upper()


def is_wc_group_entity(nit: str | None, client_name: str | None) -> bool:
    """True si el cliente es una entidad del grupo WC (WCF/WCL/WCI/WCS/WCHG)."""
    nit_digits = normalize_nit(nit)
    if nit_digits and any(nit_digits.startswith(prefix) for prefix in WC_GROUP_NIT_PREFIXES):
        return True
    name = (client_name or "").strip().upper()
    if not name:
        return False
    return any(marker in name for marker in WC_GROUP_NAME_MARKERS)


def raw_une_is_external_investment_category(raw_une: str | None) -> bool:
    """Solo inversiones captadas vía Leasing Investment o WCHG cuentan como clientes nuevos."""
    text = (raw_une or "").strip().upper()
    if not text:
        return False
    return any(marker in text for marker in INVESTMENT_CLIENT_CATEGORIES)


def counts_toward_clientes_nuevos_metric(
    *,
    une_code: str | None,
    raw_une: str | None,
    nit: str | None,
    client_name: str | None,
    counts_as_new: bool,
) -> bool:
    """
    Define si una fila importada incrementa CLIENTES_NUEVOS en PGC.

    - Insurance: nunca (clientes propios del grupo).
    - Investment: solo categorías externas Leasing Investment + WCHG; excluye intercompañía.
    - Resto de UNE: ContratosPrevios=0 y no entidad del grupo.
    """
    if not counts_as_new:
        return False

    code = (une_code or "").upper()
    if code == UNE.CODE_INSURANCE:
        return False

    if code == UNE.CODE_INVESTMENT:
        if not raw_une_is_external_investment_category(raw_une):
            return False
        if is_wc_group_entity(nit, client_name):
            return False
        return True

    if is_wc_group_entity(nit, client_name):
        return False
    return True


def client_identity_key(
    nit: str | None,
    client_name: str | None,
    operation_code: str | None,
) -> str:
    """Clave para contar clientes únicos por NIT (o nombre / operación si falta NIT)."""
    nit_key = normalize_nit(nit)
    if nit_key:
        return f"nit:{nit_key}"
    name = re.sub(r"\s+", " ", (client_name or "").strip().upper())
    if name:
        return f"name:{name}"
    op = normalize_operation_code(operation_code)
    return f"op:{op or 'unknown'}"


def aggregate_clientes_nuevos_counts(rows) -> dict[tuple[int, int, int], int]:
    """
    Agrega conteos por (year, month, une_id).

    Todas las UNE: clientes únicos por NIT (o nombre / operación si no hay NIT).
    Varias filas del mismo cliente no incrementan la métrica.
    """
    unique_keys: dict[tuple[int, int, int], set[str]] = defaultdict(set)

    for row in rows:
        une = getattr(row, "une", None)
        if not une:
            continue
        year = row.year
        month = row.month
        if not year or not month:
            header = getattr(row, "header", None)
            if header:
                year = year or header.year
                month = month or header.month
        if not year or not month:
            continue

        raw_une = getattr(row, "raw_une_value", None) or ""
        if not counts_toward_clientes_nuevos_metric(
            une_code=une.code,
            raw_une=raw_une,
            nit=getattr(row, "nit", None),
            client_name=getattr(row, "client_name", None),
            counts_as_new=bool(getattr(row, "counts_as_new", False)),
        ):
            continue

        key = (year, month, une.id)
        identity = client_identity_key(
            getattr(row, "nit", None),
            getattr(row, "client_name", None),
            getattr(row, "operation_code", None),
        )
        unique_keys[key].add(identity)

    return {key: len(identities) for key, identities in unique_keys.items()}


def intercompany_investment_operation_codes(rows) -> set[str]:
    """Códigos de operación de inversiones entre entidades del grupo (no importar en AP/PG)."""
    codes: set[str] = set()
    for row in rows:
        raw_une = (getattr(row, "raw_une_value", None) or getattr(row, "company", None) or "")
        if "INVEST" not in str(raw_une).upper():
            continue
        nit = getattr(row, "nit", None)
        client_name = getattr(row, "client_name", None)
        if not is_wc_group_entity(nit, client_name):
            continue
        op = normalize_operation_code(getattr(row, "operation_code", None))
        if op:
            codes.add(op)
    return codes


def is_intercompany_investment_growth_row(
    company: str | None,
    operation_code: str | None,
    *,
    intercompany_ops: set[str] | None = None,
) -> bool:
    """
    Excluye saldos AP/PG que son préstamos/inversiones entre divisiones WC.

    Se identifican por código de operación vinculado a un NIT/nombre de grupo
    en el archivo de clientes nuevos.
    """
    op = normalize_operation_code(operation_code)
    if not op:
        return False
    if intercompany_ops and op in intercompany_ops:
        return True
    return False
