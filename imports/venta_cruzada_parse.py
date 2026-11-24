from __future__ import annotations

import csv
from datetime import date, datetime
from pathlib import Path

SPANISH_MONTH_INDEX = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "septeimbre": 9,
    "setiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}


def parse_cross_sale_period(periodo, *, default_year: int = 2026) -> tuple[int, int] | None:
    if periodo is None or str(periodo).strip() == "":
        return None
    raw = str(periodo).strip()
    try:
        year_str, month_str = raw.replace("-", "/").split("/")[:2]
        return int(year_str), int(month_str)
    except Exception:
        pass
    key = raw.casefold().strip()
    month = SPANISH_MONTH_INDEX.get(key)
    if month:
        return default_year, month
    return None


def parse_cross_sale_date(value) -> date | None:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    fecha_raw = str(value).strip()
    if not fecha_raw:
        return None
    try:
        return datetime.fromisoformat(fecha_raw.replace("Z", "+00:00")).date()
    except Exception:
        pass
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(fecha_raw[:10], fmt).date()
        except Exception:
            continue
    return None


def _normalize_header(h: object) -> str:
    return str(h or "").strip()


def iter_cross_sale_rows(path: Path):
    suffix = path.suffix.lower()
    if suffix in (".xlsx", ".xls"):
        import openpyxl

        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        sheet = wb["Datos"] if "Datos" in wb.sheetnames else wb.active
        headers: list[str] | None = None
        for row in sheet.iter_rows(values_only=True):
            if not any(c is not None and str(c).strip() for c in row):
                continue
            if headers is None:
                headers = [_normalize_header(c) for c in row]
                continue
            cells = list(row)
            if len(cells) < len(headers):
                cells.extend([None] * (len(headers) - len(cells)))
            yield dict(zip(headers, cells))
        return

    with path.open("r", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=[",", "\t", ";"])
        except csv.Error:
            delimiter = "\t" if "\t" in sample else ","
            dialect = csv.excel_tab if delimiter == "\t" else csv.excel
        reader = csv.DictReader(f, dialect=dialect)
        for row in reader:
            yield row


def cross_sale_row_exists(
    *,
    year: int,
    month: int,
    client_name: str,
    operation_code: str,
    row_date: date | None,
    currency_id: int | None,
    une_destination_id: int | None,
    une_origin_id: int | None,
) -> bool:
    from imports.models import CrossSaleImportRow

    return CrossSaleImportRow.objects.filter(
        year=year,
        month=month,
        client_name=client_name,
        operation_code=operation_code,
        date=row_date,
        currency_id=currency_id,
        une_destination_id=une_destination_id,
        une_origin_id=une_origin_id,
    ).exists()