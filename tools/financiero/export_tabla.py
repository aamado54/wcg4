"""Exporta combined_full.json a Excel plano (vaciado) o tabla de revisión (Datos/KPIs/Advertencias)."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

SUMMARY_CODES = {
    "activo": ["1"],
    "activo_corriente": ["101"],
    "activo_no_corriente": ["102"],
    "pasivo_corriente": ["201"],
    "pasivo_no_corriente": ["202"],
    "patrimonio": ["301"],
    "utilidades": ["302"],
    "cartera": ["1010301", "10103"],
}


def _norm_code(v) -> str:
    if v is None:
        return ""
    s = str(v).strip()
    return re.sub(r"\.0$", "", s)


def audit_data_warnings(data: dict) -> dict:
    """Genera advertencias de calidad al estilo data_warnings.json (Jul 2026)."""
    periods = list(data.get("periods") or [])
    kpis = data.get("kpis") or {}
    by_key = {
        (a.get("bu", ""), a.get("code", "")): a
        for a in (data.get("accounts") or [])
    }
    warnings: list[dict] = []

    recent = set(data.get("recent_periods") or [])
    for bu in ("T", "F", "L", "I", "S"):
        for p in periods:
            row = (kpis.get(bu) or {}).get(p) or {}
            if row.get("activo") is None and (
                row.get("activo_corriente") is not None
                or row.get("activo_no_corriente") is not None
            ):
                warnings.append(
                    {
                        "severity": "kpi_gap",
                        "bu": bu,
                        "period": p,
                        "metric": "activo",
                        "detail": "KPI activo (cuenta 1) ausente; sí hay 101/102 — el gráfico muestra 0",
                    }
                )
            if (
                bu in ("L", "I", "S")
                and p in recent
                and "cartera" not in row
            ):
                warnings.append(
                    {
                        "severity": "kpi_map",
                        "bu": bu,
                        "period": p,
                        "metric": "cartera",
                        "detail": "Sin mapeo de cartera para esta BU (códigos F-only 10103*)",
                    }
                )

    for bu in "FLIS":
        for code in ("1", "202"):
            acc = by_key.get((bu, code))
            if not acc:
                continue
            vals = acc.get("values") or {}
            missing = [p for p in periods if p not in vals or vals[p] is None]
            if len(missing) >= 3 and missing[0] >= "2025-06":
                label = acc.get("label") or code
                warnings.append(
                    {
                        "severity": "missing_periods",
                        "bu": bu,
                        "period": ",".join(missing[:12]),
                        "metric": code,
                        "detail": f"{label} — faltan {len(missing)} períodos desde {missing[0][:7]}",
                    }
                )

    return {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "count": len(warnings),
        "warnings": warnings,
    }


def export_financiero_tabla(
    combined_full_path: Path,
    output_path: Path,
    *,
    include_kpis: bool = True,
) -> dict:
    data = json.loads(combined_full_path.read_text(encoding="utf-8"))
    accounts = data.get("accounts") or []
    periods = sorted(data.get("periods") or [])
    kpis = data.get("kpis") or {}

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "EEFF consolidado"

    headers = ["BU", "Código", "Cuenta", "Fuente"] + periods
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for acc in sorted(accounts, key=lambda a: (a.get("bu", ""), a.get("code", ""))):
        vals = acc.get("values") or {}
        row = [
            acc.get("bu", ""),
            acc.get("code", ""),
            acc.get("label", ""),
            acc.get("source", ""),
        ]
        row.extend(vals.get(p) for p in periods)
        ws.append(row)

    if include_kpis:
        ws2 = wb.create_sheet("KPIs")
        kpi_names = sorted(
            {k for bu in kpis.values() for per in bu.values() for k in per}
        )
        ws2.append(["BU", "KPI"] + periods)
        for cell in ws2[1]:
            cell.font = Font(bold=True)
        for bu, bu_data in sorted(kpis.items()):
            for kpi in kpi_names:
                row = [bu, kpi]
                row.extend((bu_data.get(p) or {}).get(kpi) for p in periods)
                if any(v is not None for v in row[2:]):
                    ws2.append(row)

    meta = wb.create_sheet("meta", 0)
    meta.append(["campo", "valor"])
    meta.append(["source_json", str(combined_full_path)])
    meta.append(["generated", data.get("generated", "")])
    meta.append(["unit", data.get("unit", "")])
    meta.append(["accounts", len(accounts)])
    meta.append(["periods", ", ".join(periods)])
    meta.append(["recent_periods", ", ".join(data.get("recent_periods") or [])])

    for i, _ in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(i)].width = 14
    ws.column_dimensions["C"].width = 42

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    return {
        "accounts": len(accounts),
        "periods": len(periods),
        "output": str(output_path),
    }


def _structure_account_rows(structure_path: Path) -> list[tuple[str, str, str]]:
    wb = openpyxl.load_workbook(structure_path, data_only=True, read_only=True)
    ws = wb.active
    rows: list[tuple[str, str, str]] = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        cells = list(row) + [None] * 4
        bu = str(cells[1]).strip() if cells[1] is not None else ""
        code = _norm_code(cells[2])
        if bu not in ("F", "L", "I", "S") or not code:
            continue
        name = str(cells[3]).strip() if cells[3] is not None else ""
        rows.append((bu, code, name))
    wb.close()
    return rows


def _wcout_dynamic_rows(wcout_path: Path) -> list[tuple[str, str, str]]:
    wb = openpyxl.load_workbook(wcout_path, data_only=True, read_only=True)
    ws = wb["consolidado"]
    out: list[tuple[str, str, str]] = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or len(row) < 5:
            continue
        if row[4] != 1:
            continue
        bu = str(row[1]).strip().upper() if row[1] else ""
        code = _norm_code(row[2])
        if bu not in ("F", "L", "I", "S") or not code:
            continue
        name = str(row[3]).strip() if row[3] else ""
        out.append((bu, code, name))
    wb.close()
    return out


def export_financiero_tabla_revision(
    combined_full_path: Path,
    output_path: Path,
    *,
    structure_path: Path,
    wcout_path: Path,
    warnings: dict | None = None,
) -> dict:
    """Excel de revisión: hojas Datos, KPIs, Advertencias, Meta (orden según estructura wcup)."""
    data = json.loads(combined_full_path.read_text(encoding="utf-8"))
    periods = sorted(data.get("periods") or [])
    kpis = data.get("kpis") or {}
    acct_map = {
        (a.get("bu", ""), a.get("code", "")): a for a in (data.get("accounts") or [])
    }
    warn = warnings or audit_data_warnings(data)

    struct_keys = _structure_account_rows(structure_path)
    struct_set = set(struct_keys)
    dynamic = [r for r in _wcout_dynamic_rows(wcout_path) if r not in struct_set]
    business_order = {"F": 0, "L": 1, "I": 2, "S": 3}
    dynamic = sorted(dynamic, key=lambda r: (business_order.get(r[0], 9), r[1]))
    all_rows = struct_keys + dynamic

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Datos"
    headers = ["businessid", "acode", "aname", "source"] + periods
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for bu, code, name in all_rows:
        acc = acct_map.get((bu, code), {})
        vals = acc.get("values") or {}
        label = acc.get("label") or name
        source = acc.get("source") or "import_reciente"
        row = [bu, code, label, source]
        row.extend(vals.get(p) for p in periods)
        ws.append(row)

    ws2 = wb.create_sheet("KPIs")
    kpi_names = sorted({k for bu in kpis.values() for per in bu.values() for k in per})
    ws2.append(["bu", "metric"] + periods)
    for cell in ws2[1]:
        cell.font = Font(bold=True)
    for bu, bu_data in sorted(kpis.items()):
        for metric in kpi_names:
            row = [bu, metric]
            row.extend((bu_data.get(p) or {}).get(metric) for p in periods)
            if any(v is not None for v in row[2:]):
                ws2.append(row)

    ws3 = wb.create_sheet("Advertencias")
    ws3.append(["severity", "bu", "period", "metric", "detail"])
    for w in warn.get("warnings") or []:
        ws3.append(
            [
                w.get("severity"),
                w.get("bu"),
                w.get("period"),
                w.get("metric"),
                w.get("detail"),
            ]
        )

    meta = wb.create_sheet("Meta", 0)
    meta.append(["campo", "valor"])
    meta.append(["unit", data.get("unit", "")])
    meta.append(["generated", data.get("generated", "")])
    meta.append(["history_source", data.get("history_source", "")])
    meta.append(["recent_source", data.get("recent_source", "")])
    meta.append(["accounts_count", len(all_rows)])
    meta.append(["periods_count", len(periods)])
    meta.append(["periods", ", ".join(periods)])
    meta.append(["warnings_count", warn.get("count", 0)])
    meta.append(["note", "Unidades: 000 quetzales. Filas=cuentas; columnas=períodos."])

    for i, _ in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(i)].width = 14
    ws.column_dimensions["C"].width = 42

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    return {
        "accounts": len(all_rows),
        "periods": len(periods),
        "warnings": warn.get("count", 0),
        "output": str(output_path),
    }
