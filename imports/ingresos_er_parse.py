"""Lectura de comisiones mensuales (GTQ) desde ER operativos y PGA mensuales."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import openpyxl
from django.core.management.base import CommandError

PGA_SHEET_BY_UNE = {
    "FACTORING": "FACTORING",
    "LEASING": "LEASING",
    "INSURANCE": "INSURANCE",
}

PGA_MONTH_ABBR = {
    1: "Ene",
    2: "Feb",
    3: "Mzo",
    4: "Abr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dic",
}


from pgc.income_conversion import gtq_comisiones_to_usd_miles


def objetivos_style_ingresos_values(
    ingreso_mensual_gtq: Decimal, fx: Decimal
) -> tuple[Decimal, Decimal]:
    """
    Par source/measured alineado a import Objetivos y PGA.

    source_value = comisiones GTQ; measured_value = miles USD = (GTQ/1000)/FX.
    """
    if not fx or fx <= 0:
        raise ValueError("Tipo de cambio inválido para comisiones.")
    source_value = ingreso_mensual_gtq
    measured_value = gtq_comisiones_to_usd_miles(ingreso_mensual_gtq, fx)
    return source_value, measured_value


def is_pga_mensuales_workbook(path: Path) -> bool:
    try:
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        names = set(wb.sheetnames)
        wb.close()
    except Exception:
        return False
    return bool(names & set(PGA_SHEET_BY_UNE.values())) and "Datos" not in names


def read_pga_mensuales_comisiones_gtq(
    path: Path, une_code: str, month: int
) -> Decimal:
    sheet = PGA_SHEET_BY_UNE.get(une_code.upper())
    if not sheet:
        raise CommandError(f"PGA mensuales no define hoja para UNE {une_code}.")
    abbr = PGA_MONTH_ABBR.get(month)
    if not abbr:
        raise CommandError(f"Mes inválido para PGA: {month}")

    try:
        wb = openpyxl.load_workbook(path, data_only=True)
    except Exception as e:
        raise CommandError(f"No se pudo abrir {path.name}: {e}")

    if sheet not in wb.sheetnames:
        wb.close()
        raise CommandError(f"{path.name}: falta hoja {sheet}.")

    ws = wb[sheet]
    month_col = None
    for row in ws.iter_rows(min_row=1, max_row=12, values_only=True):
        if not row:
            continue
        for idx, cell in enumerate(row):
            if cell is not None and str(cell).strip() == abbr:
                month_col = idx
                break
        if month_col is not None:
            break

    if month_col is None:
        wb.close()
        raise CommandError(
            f"{path.name} hoja {sheet}: no se encontró columna del mes {abbr}."
        )

    comisiones_row = None
    for row in ws.iter_rows(min_row=1, max_row=30, values_only=True):
        if not row or len(row) <= 2:
            continue
        label = row[2]
        if label is not None and str(label).strip().lower() == "comisiones":
            comisiones_row = row
            break

    wb.close()
    if comisiones_row is None:
        raise CommandError(f"{path.name} hoja {sheet}: falta fila «Comisiones».")

    if month_col >= len(comisiones_row):
        raise CommandError(f"{path.name}: columna {abbr} fuera de rango en Comisiones.")

    raw = comisiones_row[month_col]
    if raw in (None, ""):
        raise CommandError(
            f"{path.name} hoja {sheet}: sin comisión en {abbr}."
        )
    try:
        return Decimal(str(raw).replace(",", ""))
    except Exception:
        raise CommandError(
            f"{path.name}: comisión no numérica en {abbr}: {raw!r}"
        )
