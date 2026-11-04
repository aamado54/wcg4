#!/usr/bin/env python3
"""Genera workbook WCG 0 BOLAS (gerencia · datos reales · Google Sheets friendly)."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from copy import copy
from pathlib import Path

import openpyxl
from openpyxl.chart import LineChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SRC = Path.home() / "download/eeff/other/estados_financieros_tabla formatted.xlsx"
DEFAULT_ORIG = Path.home() / "download/eeff/other/estados_financieros_tabla original.xlsx"
OUT_DIR = Path.home() / "download/eeff/other"

NAVY = "1A365D"
BLUE = "2B6CB0"
GRAY_BG = "EDF2F7"
WHITE = "FFFFFF"
ACCENT = "2C5282"
WARN = "C05621"

HEADER_FILL = PatternFill("solid", fgColor=NAVY)
SECTION_FILL = PatternFill("solid", fgColor=GRAY_BG)
ACCENT_FILL = PatternFill("solid", fgColor=BLUE)
THIN = Side(style="thin", color="CBD5E0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

BU_LABELS = {
    "T": "Total WCG",
    "F": "Factoraje",
    "L": "Leasing",
    "I": "Insurance",
    "S": "Services",
}
KPI_GERENCIA = [
    ("activo", "Activo (Q)"),
    ("utilidades", "Utilidad del periodo"),
    ("cartera", "Cartera"),
    ("liquidez", "Liquidez (AC / PC)"),
    ("apalancamiento", "Apalancamiento"),
    ("roe", "ROE"),
]
CHART_SERIES = [
    ("Total WCG · Activo", "Total", "activo"),
    ("Total WCG · Utilidades", "Total", "utilidades"),
    ("Total WCG · Cartera", "Total", "cartera"),
    ("Factoraje · Activo", "Factor", "activo"),
    ("Factoraje · Cartera", "Factor", "cartera"),
    ("Factoraje · Utilidades", "Factor", "utilidades"),
    ("Leasing · Activo", "Leasing", "activo"),
    ("Leasing · Utilidades", "Leasing", "utilidades"),
    ("Insurance · Activo", "Insurance", "activo"),
    ("Services · Activo", "Services", "activo"),
]
BALANCE_CODES = [
    ("101", "Activo corriente"),
    ("102", "Activo no corriente"),
    ("201", "Pasivo corriente"),
    ("202", "Pasivo no corriente"),
    ("301", "Patrimonio"),
    ("302", "Utilidades"),
]
ER_LINES = [
    ("4", "Ingresos (grupo 4)"),
    ("5", "Costos (grupo 5)"),
    ("6", "Gastos operativos (grupo 6)"),
    ("7", "Otros (grupo 7)"),
    ("302", "Utilidad del ejercicio"),
]


def _style_header_row(ws, row: int, ncol: int) -> None:
    for c in range(1, ncol + 1):
        cell = ws.cell(row, c)
        cell.fill = HEADER_FILL
        cell.font = Font(color=WHITE, bold=True, size=10)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER


def _copy_sheet(src, dest_wb, name: str):
    if name in dest_wb.sheetnames:
        del dest_wb[name]
    dest = dest_wb.create_sheet(name)
    for row in src.iter_rows():
        for cell in row:
            d = dest.cell(row=cell.row, column=cell.column, value=cell.value)
            if cell.has_style:
                d._style = copy(cell._style)
    for col, dim in src.column_dimensions.items():
        dest.column_dimensions[col].width = dim.width
    for rng in src.merged_cells.ranges:
        dest.merge_cells(str(rng))
    dest.freeze_panes = src.freeze_panes
    return dest


def _period_cols(ws) -> list[tuple[int, str]]:
    out = []
    for c in range(3, ws.max_column + 1):
        h = ws.cell(1, c).value
        if h and re.match(r"\d{4}-\d{2}", str(h)):
            out.append((c, str(h)))
    return out


def _add_kpi_key_column(ws) -> int:
    key_col = ws.max_column + 1
    letter = get_column_letter(key_col)
    ws.cell(1, key_col, "_key")
    for r in range(2, ws.max_row + 1):
        a, b = ws.cell(r, 1).value, ws.cell(r, 2).value
        if a and b:
            ws.cell(r, key_col, f"{a}|{b}")
    ws.column_dimensions[letter].hidden = True
    return key_col


def _meta_map(ws) -> dict[str, str]:
    m = {}
    for r in range(2, ws.max_row + 1):
        k, v = ws.cell(r, 1).value, ws.cell(r, 2).value
        if k:
            m[str(k)] = "" if v is None else str(v)
    return m


def _build_inicio(wb, meta: dict) -> None:
    ws = wb.create_sheet("Inicio", 0)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 28
    ws.column_dimensions["C"].width = 36
    ws.column_dimensions["D"].width = 36

    ws.merge_cells("B2:D2")
    t = ws["B2"]
    t.value = "WCG · 0 BOLAS"
    t.font = Font(size=22, bold=True, color=NAVY)
    ws.merge_cells("B3:D3")
    ws["B3"].value = "Fuente oficial · estados financieros REALES (no proyecciones)"
    ws["B3"].font = Font(size=11, color=ACCENT)

    ws["B5"] = "Corte de datos"
    ws["C5"] = meta.get("generated", "")[:10]
    ws["B6"] = "Unidades"
    ws["C6"] = meta.get("unit", "000 quetzales")
    ws["B7"] = "Períodos"
    ws["C7"] = meta.get("periods_count", "")

    ws.merge_cells("B9:D9")
    ws["B9"] = "Ir a…"
    ws["B9"].font = Font(bold=True, size=12, color=NAVY)

    nav = [
        ("Gerencia", "Resumen ejecutivo (12 meses)"),
        ("Gráficos", "Tendencias · elija serie y cree/actualice gráfico"),
        ("Balance", "Balance resumido por empresa"),
        ("Resultados", "Estado de resultados (niveles clave)"),
        ("Datos", "Detalle contable completo"),
        ("KPIs", "Indicadores calculados (backend)"),
        ("Advertencias", "Calidad de datos"),
        ("Meta", "Trazabilidad de la integración"),
    ]
    r = 10
    for sheet, desc in nav:
        c = ws.cell(r, 2, sheet)
        c.font = Font(bold=True, color=BLUE, underline="single")
        c.hyperlink = f"#'{sheet}'!A1"
        ws.cell(r, 3, desc)
        r += 1

    ws.merge_cells(f"B{r+1}:D{r+3}")
    note = ws.cell(r + 1, 2)
    note.value = (
        "Google Sheets: abra este archivo y use las pestañas de arriba. "
        "En «Gráficos», seleccione la serie en el menú; la tabla Periodo/Valor "
        "alimenta un gráfico de líneas (Insertar → Gráfico). "
        "Tras actualizar datos en «KPIs»/«Datos», recargue fórmulas si hace falta."
    )
    note.alignment = Alignment(wrap_text=True, vertical="top")
    note.font = Font(size=10, color="4A5568")

    ws.merge_cells("B4:D4")
    badge = ws["B4"]
    badge.value = " 0 BOLAS · cero relleno · solo real  "
    badge.fill = ACCENT_FILL
    badge.font = Font(bold=True, color=WHITE, size=10)


BU_CHOOSE = (
    'CHOOSE(MATCH($B$2,{"Total WCG","Factoraje","Leasing","Insurance","Services"},0),'
    '"Total","Factor","Leasing","Insurance","Services")'
)


def _build_datos_map(wb) -> None:
    datos = wb["Datos"]
    mp = wb.create_sheet("_Map")
    mp.sheet_state = "hidden"
    mp.cell(1, 1, "key")
    mp.cell(1, 2, "row")
    r = 2
    for dr in range(2, datos.max_row + 1):
        bu = datos.cell(dr, 1).value
        code = datos.cell(dr, 2).value
        if bu is None or code is None:
            continue
        mp.cell(r, 1, f"{bu}|{code}")
        mp.cell(r, 2, dr)
        r += 1


def _build_gerencia(wb, kpi_ws_name: str = "KPIs") -> None:
    ws = wb.create_sheet("Gerencia", 1)
    kpi = wb[kpi_ws_name]
    periods = _period_cols(kpi)[-12:]
    key_col = kpi.max_column

    ws.merge_cells("A1:O1")
    ws["A1"] = "Resumen gerencia · Working Capital Group"
    ws["A1"].font = Font(size=14, bold=True, color=NAVY)
    ws["A2"] = "Unidad de negocio"
    ws["B2"] = "Total WCG"
    dv = DataValidation(
        type="list",
        formula1='"Total WCG,Factoraje,Leasing,Insurance,Services"',
        allow_blank=False,
    )
    dv.add(ws["B2"])
    ws.add_data_validation(dv)
    ws["A3"] = "Unidades monetarias"
    ws["B3"] = "000 quetzales · datos reales EEFF"

    hdr_row = 5
    ws.cell(hdr_row, 1, "Indicador")
    for i, (_, p) in enumerate(periods, start=2):
        ws.cell(hdr_row, i, p)
    _style_header_row(ws, hdr_row, 1 + len(periods))

    key_letter = get_column_letter(key_col)
    first_p_col = get_column_letter(periods[0][0])
    last_p_col = get_column_letter(periods[-1][0])

    r = hdr_row + 1
    for metric, label in KPI_GERENCIA:
        ws.cell(r, 1, label)
        for i, (pcol, _) in enumerate(periods, start=2):
            plet = get_column_letter(pcol)
            ws.cell(
                r,
                i,
                f'=IFERROR(INDEX({kpi_ws_name}!${first_p_col}$2:${last_p_col}${kpi.max_row},'
                f'MATCH({BU_CHOOSE}&"|"&"{metric}",'
                f'{kpi_ws_name}!${key_letter}$2:${key_letter}${kpi.max_row}, 0),'
                f'COLUMN({kpi_ws_name}!{plet}$1)-COLUMN({kpi_ws_name}!${first_p_col}$1)+1), "")',
            )
        r += 1

    ws.column_dimensions["A"].width = 26
    for c in range(2, 2 + len(periods)):
        ws.column_dimensions[get_column_letter(c)].width = 11
    ws.freeze_panes = "B6"


def _build_graficos(wb, kpi_ws_name: str = "KPIs") -> None:
    ws = wb.create_sheet("Gráficos", 2)
    cat = wb.create_sheet("_Catalogo")
    cat.sheet_state = "hidden"

    kpi = wb[kpi_ws_name]
    periods = _period_cols(kpi)
    key_col = kpi.max_column
    key_letter = get_column_letter(key_col)
    first_p_col = get_column_letter(periods[0][0])
    last_p_col = get_column_letter(periods[-1][0])

    cat.cell(1, 1, "label")
    cat.cell(1, 2, "bu")
    cat.cell(1, 3, "metric")
    for i, (label, bu, metric) in enumerate(CHART_SERIES, start=2):
        cat.cell(i, 1, label)
        cat.cell(i, 2, bu)
        cat.cell(i, 3, metric)
        cat.cell(i, 4, f"{bu}|{metric}")

    ws.merge_cells("A1:F1")
    ws["A1"] = "Tendencias · 0 BOLAS (datos reales)"
    ws["A1"].font = Font(size=14, bold=True, color=NAVY)
    ws["A3"] = "Serie a graficar"
    ws["B3"] = CHART_SERIES[0][0]
    last_cat = len(CHART_SERIES) + 1
    dv = DataValidation(type="list", formula1=f"=_Catalogo!$A$2:$A${last_cat}", allow_blank=False)
    dv.add(ws["B3"])
    ws.add_data_validation(dv)
    ws["A4"] = "Unidades"
    ws["B4"] = "000 quetzales (ver KPIs)"
    ws["A6"] = "Periodo"
    ws["B6"] = "Valor"
    _style_header_row(ws, 6, 2)

    bu_cell = "D3"
    ws["C3"] = "Clave lookup"
    ws[bu_cell] = f'=INDEX(_Catalogo!D:D, MATCH(B3, _Catalogo!A:A, 0))'

    data_start = 7
    for idx, (_, p) in enumerate(periods):
        row = data_start + idx
        ws.cell(row, 1, p)
        plet = get_column_letter(periods[idx][0])
        ws.cell(
            row,
            2,
            f'=IFERROR(INDEX({kpi_ws_name}!${first_p_col}$2:${last_p_col}${kpi.max_row},'
            f'MATCH(${bu_cell}, {kpi_ws_name}!${key_letter}$2:${key_letter}${kpi.max_row}, 0),'
            f'COLUMN({kpi_ws_name}!{plet}$1)-COLUMN({kpi_ws_name}!${first_p_col}$1)+1), "")',
        )

    chart = LineChart()
    chart.title = "Serie seleccionada (actualice título en Sheets si desea)"
    chart.y_axis.title = "000 Q"
    chart.x_axis.title = "Mes"
    data = Reference(ws, min_col=2, min_row=6, max_row=data_start + len(periods) - 1)
    cats = Reference(ws, min_col=1, min_row=7, max_row=data_start + len(periods) - 1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.height = 12
    chart.width = 22
    ws.add_chart(chart, "D6")

    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["D"].width = 3


def _datos_value_formula(code: str, plet: str, datos_max: int) -> str:
    bu = (
        'CHOOSE(MATCH($B$2,{"Factoraje","Leasing","Insurance","Services"},0),'
        '"Factor","Leasing","Insurance","Services")'
    )
    return (
        f'=IFERROR(INDEX(Datos!{plet}$2:{plet}${datos_max},'
        f'INDEX(_Map!$B$2:$B$3000, MATCH({bu}&"|"&"{code}", _Map!$A$2:$A$3000, 0))-1), "")'
    )


def _build_balance(wb) -> None:
    ws = wb.create_sheet("Balance", 3)
    datos = wb["Datos"]
    periods = _period_cols(datos)[-6:]

    ws["A1"] = "Balance resumido · últimos 6 meses"
    ws["A1"].font = Font(size=14, bold=True, color=NAVY)
    ws["A2"] = "Empresa"
    ws["B2"] = "Factoraje"
    dv_bu = DataValidation(type="list", formula1='"Factoraje,Leasing,Insurance,Services"', allow_blank=False)
    dv_bu.add(ws["B2"])
    ws.add_data_validation(dv_bu)

    hdr = 4
    ws.cell(hdr, 1, "Cuenta")
    for i, (_, p) in enumerate(periods, start=2):
        ws.cell(hdr, i, p)
    _style_header_row(ws, hdr, 1 + len(periods))

    r = hdr + 1
    for code, label in BALANCE_CODES:
        ws.cell(r, 1, label)
        for j, (pcol, _) in enumerate(periods, start=2):
            plet = get_column_letter(pcol)
            ws.cell(r, j, _datos_value_formula(code, plet, datos.max_row))
        r += 1

    ws.column_dimensions["A"].width = 24
    ws.freeze_panes = "C5"


def _build_resultados(wb) -> None:
    ws = wb.create_sheet("Resultados", 4)
    datos = wb["Datos"]
    periods = _period_cols(datos)[-6:]
    ws["A1"] = "Resultados · líneas clave (000 quetzales · reales)"
    ws["A1"].font = Font(size=14, bold=True, color=NAVY)
    ws["A2"] = "Empresa"
    ws["B2"] = "Factoraje"
    dv = DataValidation(type="list", formula1='"Factoraje,Leasing,Insurance,Services"', allow_blank=False)
    dv.add(ws["B2"])
    ws.add_data_validation(dv)

    hdr = 4
    ws.cell(hdr, 1, "Código")
    ws.cell(hdr, 2, "Concepto")
    for i, (_, p) in enumerate(periods, start=3):
        ws.cell(hdr, i, p)
    _style_header_row(ws, hdr, 2 + len(periods))

    r0 = hdr + 1
    for code, label in ER_LINES:
        ws.cell(r0, 1, code)
        ws.cell(r0, 2, label)
        for j, (pcol, _) in enumerate(periods, start=3):
            plet = get_column_letter(pcol)
            ws.cell(r0, j, _datos_value_formula(code, plet, datos.max_row))
        r0 += 1

    ws.column_dimensions["B"].width = 32
    ws.freeze_panes = "C5"


def _touch_datos_kpis(wb) -> None:
    if "Datos" in wb.sheetnames:
        ws = wb["Datos"]
        ws.sheet_properties.tabColor = "718096"
        if not ws.freeze_panes:
            ws.freeze_panes = "E2"
        _style_header_row(ws, 1, min(10, ws.max_column))
    if "KPIs" in wb.sheetnames:
        ws = wb["KPIs"]
        ws.sheet_properties.tabColor = "718096"
        if not ws.freeze_panes:
            ws.freeze_panes = "C2"
        _add_kpi_key_column(ws)
        _style_header_row(ws, 1, min(10, ws.max_column))
    if "Advertencias" in wb.sheetnames:
        wb["Advertencias"].sheet_properties.tabColor = WARN


def build(source: Path, outputs: list[Path]) -> None:
    src_wb = openpyxl.load_workbook(source)
    meta = _meta_map(src_wb["Meta"]) if "Meta" in src_wb.sheetnames else {}

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    for name in ("Datos", "KPIs", "Meta", "Advertencias"):
        if name in src_wb.sheetnames:
            _copy_sheet(src_wb[name], wb, name)

    _touch_datos_kpis(wb)
    _build_datos_map(wb)
    _build_inicio(wb, meta)
    _build_gerencia(wb)
    _build_graficos(wb)
    _build_balance(wb)
    _build_resultados(wb)

    # Tab colors gerencia-facing
    for sn, color in (
        ("Inicio", NAVY),
        ("Gerencia", BLUE),
        ("Gráficos", "38A169"),
        ("Balance", "805AD5"),
        ("Resultados", "DD6B20"),
    ):
        if sn in wb.sheetnames:
            wb[sn].sheet_properties.tabColor = color

    tmp = outputs[0]
    tmp.parent.mkdir(parents=True, exist_ok=True)
    wb.save(tmp)
    for out in outputs[1:]:
        shutil.copy2(tmp, out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Build WCG 0 BOLAS workbook")
    ap.add_argument("--source", type=Path, default=DEFAULT_SRC)
    ap.add_argument(
        "--output",
        type=Path,
        action="append",
        default=[],
        help="Output xlsx (default: wcg-0bolas + formatted copy)",
    )
    args = ap.parse_args()
    outs = args.output or [
        OUT_DIR / "wcg-0bolas.xlsx",
        OUT_DIR / "estados_financieros_tabla formatted.xlsx",
    ]
    if not args.source.is_file():
        args.source = DEFAULT_ORIG
    build(args.source, outs)
    print("OK →", ", ".join(str(p) for p in outs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
