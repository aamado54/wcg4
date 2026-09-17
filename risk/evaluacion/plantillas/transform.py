"""Transforma bloques extraídos al layout Caratula/Altman que consume load_evaluacion."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from openpyxl.utils import get_column_letter

from .altman_compute import build_altman_row_defs
from .extract import TemplateBlock
from .io_utils import clean_company_name


def _is_year(value: Any) -> bool:
    if isinstance(value, datetime):
        return 1990 <= value.year <= 2100
    try:
        y = int(float(value))
        return 1990 <= y <= 2100
    except (TypeError, ValueError):
        return False


def _year_value(value: Any) -> int | str:
    if isinstance(value, datetime):
        return value.year
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return str(value).strip()


def _split_label_value(text: str) -> tuple[str, str | None]:
    if not text:
        return "", None
    s = str(text).strip()
    if ":" in s:
        label, rest = s.split(":", 1)
        return label.strip() + ":", rest.strip() or None
    return s, None


def _find_data_row(block_data: list[list], *needles: str) -> int | None:
    needles_l = [n.lower() for n in needles]
    for i, row in enumerate(block_data):
        if not row:
            continue
        label = str(row[0] or "").lower()
        if any(n in label for n in needles_l):
            return i
    return None


def _block_to_company_grid(block: TemplateBlock) -> dict[str, Any] | None:
    data = block.caratula
    if not data or len(data) < 3:
        return None

    company_name = clean_company_name(block.filename)

    # Fila de años: primera fila con >=2 años en columnas de datos
    years_row_idx = None
    years: list[Any] = []
    for i, row in enumerate(data):
        ys = [_year_value(v) for v in row[1:] if _is_year(v)]
        if len(ys) >= 2:
            years_row_idx = i
            years = [_year_value(v) for v in row[1:]]
            break
    if years_row_idx is None:
        return None

    status_row = data[years_row_idx + 1] if years_row_idx + 1 < len(data) else []
    statuses = list(status_row[1 : 1 + len(years)])

    # Métricas: filas con etiqueta textual en col 0 y números en cols de datos
    metric_rows: list[tuple[str, list]] = []
    for row in data[years_row_idx + 2 :]:
        if not row or not row[0]:
            continue
        label_raw = str(row[0]).strip()
        if not label_raw or label_raw.lower().startswith("estructuras"):
            break
        vals = list(row[1 : 1 + len(years)])
        if any(v is not None and str(v).strip() != "" for v in vals):
            metric_rows.append((label_raw, vals))

    # Metadatos desde filas NOMBRE/GIRO/MILES/AUDITOR
    meta: dict[str, str | None] = {}
    for key, needles in (
        ("nombre", ("nombre del cliente",)),
        ("giro", ("giro del negocio",)),
        ("miles", ("en miles de",)),
        ("auditor", ("auditor", "contador", "firma")),
    ):
        idx = _find_data_row(data, *needles)
        if idx is not None:
            label, val = _split_label_value(str(data[idx][0]))
            if not val and len(data[idx]) > 1:
                for v in data[idx][1:]:
                    if v and str(v).strip():
                        val = str(v).strip()
                        break
            meta[key] = val or company_name if key == "nombre" else val

    return {
        "filename": block.filename,
        "company_name": meta.get("nombre") or company_name,
        "giro": meta.get("giro"),
        "miles": meta.get("miles"),
        "auditor": meta.get("auditor"),
        "years": years,
        "statuses": statuses,
        "metric_rows": metric_rows,
    }


def build_wcg_caratula_sheet(blocks: list[TemplateBlock]) -> list[list[Any]]:
    """Genera grilla Caratula compatible con risk.evaluacion.reader._parse_caratula."""
    companies = []
    for block in blocks:
        grid = _block_to_company_grid(block)
        if grid:
            companies.append(grid)

    if not companies:
        return []

    # Determinar ancho máximo de años por empresa (puede variar)
    max_years = max(len(c["years"]) for c in companies)
    total_cols = 3 + sum(max_years + 1 for c in companies)  # A + gaps

    def empty_row() -> list[Any]:
        return [None] * total_cols

    out: list[list[Any]] = [empty_row(), empty_row(), empty_row()]

    col = 3  # primera empresa empieza en D (0-index col 3)
    label_col = 0

    for ci, comp in enumerate(companies):
        n = len(comp["years"])
        # Fila 0: nombre empresa
        out[0][col] = comp["company_name"]
        # Fila 1: años
        for j, y in enumerate(comp["years"]):
            out[1][col + j] = y
        # Fila 2: estatus
        for j, st in enumerate(comp["statuses"][:n]):
            out[2][col + j] = st

        # Filas de contenido (desde fila 4 en Excel = index 4)
        row_defs: list[tuple[str, list | None]] = [
            ("NOMBRE DEL CLIENTE:", [comp["company_name"]] + [None] * (n - 1)),
            ("GIRO DEL NEGOCIO:", [comp.get("giro")] + [None] * (n - 1)),
            ("EN MILES DE:", [comp.get("miles")] + [None] * (n - 1)),
            ("FIRMA DE AUDITORIA (O CONTADOR):", [comp.get("auditor")] + [None] * (n - 1)),
            ("", None),
        ]
        for label, vals in comp["metric_rows"]:
            row_defs.append((label, vals))

        altman_rows = build_altman_row_defs(comp["metric_rows"])
        # load_evaluacion distingue fila de etiquetas Z (Bien/Soso/Mal) solo si r_idx > 60.
        start_data_row = 4
        min_z_label_idx = 61  # índice 0-based; debe ser > 60
        pad_rows = max(
            0,
            (min_z_label_idx + 1) - start_data_row - len(row_defs) - len(altman_rows),
        )
        row_defs.extend([("", None)] * pad_rows)
        row_defs.extend(altman_rows)

        # Expandir out hasta tener filas suficientes
        needed = start_data_row + len(row_defs)
        while len(out) < needed:
            out.append(empty_row())

        for ri, (label, vals) in enumerate(row_defs):
            r = start_data_row + ri
            out[r][label_col] = label if label else None
            if vals:
                for j, v in enumerate(vals[:n]):
                    out[r][col + j] = v

        col += n + 1  # columna separadora

    return out


def write_sheet_from_grid(ws, grid: list[list[Any]]) -> None:
    for r_idx, row in enumerate(grid, start=1):
        for c_idx, val in enumerate(row, start=1):
            if val is not None:
                ws.cell(row=r_idx, column=c_idx, value=val)


def write_side_by_side(ws, blocks: dict[str, list[list]], desc_cols: int = 1) -> None:
    col_pos = 1
    for filename, data in blocks.items():
        if not data:
            continue
        data = [row for row in data if any(v is not None and str(v).strip() for v in row)]
        if not data:
            continue
        data[0][0] = filename
        for r_idx, row in enumerate(data, start=1):
            for c_idx, val in enumerate(row, start=col_pos):
                ws.cell(row=r_idx, column=c_idx, value=val)
        max_cols = max(len(row) for row in data)
        col_pos += max_cols + 1
