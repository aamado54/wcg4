"""Extrae bloques Carátula/Balance/Resultados de cada plantilla individual."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import openpyxl

from .io_utils import (
    column_has_numbers,
    column_is_percentage,
    find_sheet,
    identify_version,
    is_hidden,
    safe_cell,
)


@dataclass
class TemplateBlock:
    filename: str
    version: int
    caratula: list[list] = field(default_factory=list)
    balance: list[list] = field(default_factory=list)
    resultados: list[list] = field(default_factory=list)
    alerts: list[str] = field(default_factory=list)


def _read_caratula(ws, version: int) -> list[list]:
    max_rows = 80
    desc_col = 2 if version == 1 else 8
    data_start_col = 3 if version == 1 else 9
    max_data_cols = 12 if version == 1 else 6

    data_cols: list[int] = []
    for col in range(data_start_col, data_start_col + max_data_cols):
        if is_hidden(ws, col=col):
            continue
        if version == 1 and column_is_percentage(ws, col, 1, max_rows):
            continue
        if not column_has_numbers(ws, col, 1, max_rows, min_numbers=3):
            continue
        data_cols.append(col)

    data: list[list] = []
    for row in range(1, max_rows + 1):
        if is_hidden(ws, row=row):
            continue
        desc_cell = safe_cell(ws, row, desc_col)
        desc_val = desc_cell.value if desc_cell else None
        row_vals = [desc_val]
        for col in data_cols:
            cell = safe_cell(ws, row, col)
            row_vals.append(cell.value if cell else None)
        data.append(row_vals)
    while data and all(
        x is None or (isinstance(x, str) and not x.strip()) for x in data[-1]
    ):
        data.pop()
    return data


def _read_balance_or_resultados(ws, version: int, kind: str) -> list[list]:
    max_rows = 120 if kind == "balance" else 80
    if version == 1:
        desc_num_col, desc_text_col = 2, 3
        data_start_col, max_data_cols = (7, 18) if kind == "balance" else (6, 18)
        min_nums = 10 if kind == "balance" else 5
    else:
        desc_num_col, desc_text_col = 4, 5
        data_start_col, max_data_cols = 9, 6
        min_nums = 10 if kind == "balance" else 5

    data_cols: list[int] = []
    for col in range(data_start_col, data_start_col + max_data_cols):
        if is_hidden(ws, col=col):
            continue
        if version == 1 and column_is_percentage(ws, col, 1, max_rows):
            continue
        if not column_has_numbers(ws, col, 1, max_rows, min_numbers=min_nums):
            continue
        data_cols.append(col)

    data: list[list] = []
    for row in range(1, max_rows + 1):
        if is_hidden(ws, row=row):
            continue
        num_cell = safe_cell(ws, row, desc_num_col)
        text_cell = safe_cell(ws, row, desc_text_col)
        row_vals = [
            num_cell.value if num_cell else None,
            text_cell.value if text_cell else None,
        ]
        for col in data_cols:
            cell = safe_cell(ws, row, col)
            row_vals.append(cell.value if cell else None)
        data.append(row_vals)
    while data and all(
        x is None or (isinstance(x, str) and not x.strip()) for x in data[-1]
    ):
        data.pop()
    return data


def extract_template(path: Path) -> TemplateBlock:
    block = TemplateBlock(filename=path.name, version=0)
    try:
        wb = openpyxl.load_workbook(path, data_only=True)
    except Exception as exc:
        block.alerts.append(f"ERROR: no se pudo abrir {path.name}: {exc}")
        return block

    ws_first = wb.worksheets[0]
    version = identify_version(ws_first)
    if version not in (1, 2):
        block.alerts.append(f"{path.name}: no se identificó versión de plantilla (1/2)")
        wb.close()
        return block
    block.version = version

    ws_c = find_sheet(wb, ["caratula"])
    if ws_c:
        try:
            block.caratula = _read_caratula(ws_c, version)
        except Exception as exc:
            block.alerts.append(f"{path.name}: error leyendo Carátula: {exc}")
    else:
        block.alerts.append(f"{path.name}: falta hoja Carátula")

    ws_b = find_sheet(wb, ["balan"])
    if ws_b:
        try:
            block.balance = _read_balance_or_resultados(ws_b, version, "balance")
        except Exception as exc:
            block.alerts.append(f"{path.name}: error leyendo Balance: {exc}")

    ws_r = find_sheet(wb, ["est", "result"])
    if ws_r:
        try:
            block.resultados = _read_balance_or_resultados(ws_r, version, "resultados")
        except Exception as exc:
            block.alerts.append(f"{path.name}: error leyendo Resultados: {exc}")

    wb.close()
    return block


def extract_directory(source_dir: Path) -> tuple[list[TemplateBlock], list[str]]:
    blocks: list[TemplateBlock] = []
    alerts: list[str] = []
    files = sorted(
        p
        for p in source_dir.iterdir()
        if p.is_file() and p.suffix.lower() in (".xlsx", ".xlsm")
    )
    if not files:
        alerts.append(f"Sin archivos .xlsx/.xlsm en {source_dir}")
    for path in files:
        block = extract_template(path)
        blocks.append(block)
        alerts.extend(block.alerts)
    return blocks, alerts
