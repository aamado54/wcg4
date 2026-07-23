# CONCATENATED .PY FILES

PART_NUMBER=7
TOTAL_PARTS=10

DOCUMENT_MODE=LITERAL_CODE_ARCHIVE
PARSING_PRIORITY=PATH_LITERAL->CONTENT_NUMBERED_BEGIN->CONTENT_BASE64_BEGIN->CONTENT_BEGIN
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
RECORD_SEPARATOR=BEGIN_LITERAL_FILE_RECORD|END_LITERAL_FILE_RECORD
RECORD_BOUNDARY=========== RECORD_BOUNDARY ==========
CONTENT_POLICY=PRESERVE_EXACT_TEXT_WITH_METADATA_AND_NUMBERED_FALLBACK
READING_HINT=Prefer PATH_LITERAL first for file identity. Prefer CONTENT_NUMBERED_BEGIN for faithful line-by-line reading. Use CONTENT_BASE64_BEGIN for exact reconstruction when available. Use CONTENT_BEGIN only as a convenience view. If CONTENT_BEGIN looks compacted, flattened, or visually altered, do not use it to infer exact identifiers, variable names, paths, punctuation grouping, or spacing.
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/investment_ingresos.py
PATH_JSON="pgc/investment_ingresos.py"
FILENAME=investment_ingresos.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=138
SIZE_BYTES_UTF8=4302
CONTENT_SHA256=6db792f6ea30518b551b2db51817129f7930bb586c0d1364bbdb5cd28aec5cd5
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""
Ingresos Investment desde NewClientImportRow.

Fuente única para vista/reporte y para persistir en MonthlyMetricResult.
Regla (alineada con /pgc/ingresos/):
- suma TODOS los registros del mes de la UNE Investment (no solo counts_as_new)
- USD se toma tal cual; GTQ se convierte con MonthlyExchangeRate del mes de la fila
- NewClientImportRow.amount ya viene en miles (Monto del archivo ÷ 1000 al importar)
"""

from __future__ import annotations

from decimal import Decimal

from django.db.models import Q

from core.models import UNE
from imports.models import NewClientImportRow
from pgc.models import MonthlyExchangeRate

INVESTMENT_UNE_CODES = ("INVESTMENT", "INVESTMENTS", "INVERSIONES")


def get_investment_une() -> UNE | None:
    return (
        UNE.objects.filter(code__in=INVESTMENT_UNE_CODES)
        .order_by("sort_order", "id")
        .first()
    )


def build_fx_map() -> dict[tuple[int, int], Decimal]:
    return {
        (item.year, item.month): item.usd_to_gtq
        for item in MonthlyExchangeRate.objects.all()
    }


def row_period(row) -> tuple[int | None, int | None]:
    year = row.year or (row.header.year if getattr(row, "header_id", None) and row.header else None)
    month = row.month or (
        row.header.month if getattr(row, "header_id", None) and row.header else None
    )
    return year, month


def convert_row_amount_to_usd(row, fx_map: dict[tuple[int, int], Decimal]) -> Decimal:
    """Misma semántica que la vista de ingresos (USD tal cual, GTQ/FX, resto 0)."""
    amount = row.amount if row.amount is not None else Decimal("0")
    currency_code = ((row.currency.code if row.currency else "") or "").upper()

    if amount == 0:
        return Decimal("0")

    if currency_code in ("USD", "US$", "$"):
        return amount

    if currency_code in ("GTQ", "Q", "QUETZALES", "QUETZAL"):
        row_year, row_month = row_period(row)
        fx = fx_map.get((row_year, row_month))
        if fx and fx != 0:
            return amount / fx

    return Decimal("0")


def sum_investment_ingresos_usd(
    year: int,
    month: int,
    *,
    une: UNE | None = None,
    fx_map: dict[tuple[int, int], Decimal] | None = None,
) -> dict:
    """
    Totales Investment para un mes (misma lógica que /pgc/ingresos/).

    Returns:
        une, total_usd, used_rows, fx (TC del year/month pedido)
    """
    une = une or get_investment_une()
    fx_map = fx_map if fx_map is not None else build_fx_map()
    fx = fx_map.get((year, month))

    if not une:
        return {"une": None, "total_usd": Decimal("0"), "used_rows": 0, "fx": fx}

    period_q = Q(year=year, month=month) | Q(header__year=year, header__month=month)
    rows = (
        NewClientImportRow.objects.select_related("header", "currency", "une")
        .filter(une=une)
        .filter(period_q)
    )

    total = Decimal("0")
    used = 0
    for row in rows:
        row_year, row_month = row_period(row)
        if (row_year, row_month) != (year, month):
            continue
        total += convert_row_amount_to_usd(row, fx_map)
        used += 1

    return {"une": une, "total_usd": total, "used_rows": used, "fx": fx}


def investment_real_map_for_periods(
    periods: list[tuple[int, int]] | None = None,
    *,
    une: UNE | None = None,
    fx_map: dict[tuple[int, int], Decimal] | None = None,
) -> dict[tuple[int, int, int], Decimal]:
    """
    Mapa (year, month, une_id) -> total USD.
    Si periods es None, usa todas las filas Investment.
    """
    une = une or get_investment_une()
    fx_map = fx_map if fx_map is not None else build_fx_map()
    out: dict[tuple[int, int, int], Decimal] = {}
    if not une:
        return out

    qs = NewClientImportRow.objects.select_related("header", "currency", "une").filter(
        une=une
    )
    if periods:
        detail_period_q = Q()
        for y, m in periods:
            detail_period_q |= Q(year=y, month=m)
            detail_period_q |= Q(header__year=y, header__month=m)
        qs = qs.filter(detail_period_q)

    for row in qs:
        row_year, row_month = row_period(row)
        if not row_year or not row_month:
            continue
        key = (row_year, row_month, une.id)
        out[key] = out.get(key, Decimal("0")) + convert_row_amount_to_usd(row, fx_map)
    return out

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Ingresos Investment desde NewClientImportRow.
00003|
00004|Fuente única para vista/reporte y para persistir en MonthlyMetricResult.
00005|Regla (alineada con /pgc/ingresos/):
00006|- suma TODOS los registros del mes de la UNE Investment (no solo counts_as_new)
00007|- USD se toma tal cual; GTQ se convierte con MonthlyExchangeRate del mes de la fila
00008|- NewClientImportRow.amount ya viene en miles (Monto del archivo ÷ 1000 al importar)
00009|"""
00010|
00011|from __future__ import annotations
00012|
00013|from decimal import Decimal
00014|
00015|from django.db.models import Q
00016|
00017|from core.models import UNE
00018|from imports.models import NewClientImportRow
00019|from pgc.models import MonthlyExchangeRate
00020|
00021|INVESTMENT_UNE_CODES = ("INVESTMENT", "INVESTMENTS", "INVERSIONES")
00022|
00023|
00024|def get_investment_une() -> UNE | None:
00025|    return (
00026|        UNE.objects.filter(code__in=INVESTMENT_UNE_CODES)
00027|        .order_by("sort_order", "id")
00028|        .first()
00029|    )
00030|
00031|
00032|def build_fx_map() -> dict[tuple[int, int], Decimal]:
00033|    return {
00034|        (item.year, item.month): item.usd_to_gtq
00035|        for item in MonthlyExchangeRate.objects.all()
00036|    }
00037|
00038|
00039|def row_period(row) -> tuple[int | None, int | None]:
00040|    year = row.year or (row.header.year if getattr(row, "header_id", None) and row.header else None)
00041|    month = row.month or (
00042|        row.header.month if getattr(row, "header_id", None) and row.header else None
00043|    )
00044|    return year, month
00045|
00046|
00047|def convert_row_amount_to_usd(row, fx_map: dict[tuple[int, int], Decimal]) -> Decimal:
00048|    """Misma semántica que la vista de ingresos (USD tal cual, GTQ/FX, resto 0)."""
00049|    amount = row.amount if row.amount is not None else Decimal("0")
00050|    currency_code = ((row.currency.code if row.currency else "") or "").upper()
00051|
00052|    if amount == 0:
00053|        return Decimal("0")
00054|
00055|    if currency_code in ("USD", "US$", "$"):
00056|        return amount
00057|
00058|    if currency_code in ("GTQ", "Q", "QUETZALES", "QUETZAL"):
00059|        row_year, row_month = row_period(row)
00060|        fx = fx_map.get((row_year, row_month))
00061|        if fx and fx != 0:
00062|            return amount / fx
00063|
00064|    return Decimal("0")
00065|
00066|
00067|def sum_investment_ingresos_usd(
00068|    year: int,
00069|    month: int,
00070|    *,
00071|    une: UNE | None = None,
00072|    fx_map: dict[tuple[int, int], Decimal] | None = None,
00073|) -> dict:
00074|    """
00075|    Totales Investment para un mes (misma lógica que /pgc/ingresos/).
00076|
00077|    Returns:
00078|        une, total_usd, used_rows, fx (TC del year/month pedido)
00079|    """
00080|    une = une or get_investment_une()
00081|    fx_map = fx_map if fx_map is not None else build_fx_map()
00082|    fx = fx_map.get((year, month))
00083|
00084|    if not une:
00085|        return {"une": None, "total_usd": Decimal("0"), "used_rows": 0, "fx": fx}
00086|
00087|    period_q = Q(year=year, month=month) | Q(header__year=year, header__month=month)
00088|    rows = (
00089|        NewClientImportRow.objects.select_related("header", "currency", "une")
00090|        .filter(une=une)
00091|        .filter(period_q)
00092|    )
00093|
00094|    total = Decimal("0")
00095|    used = 0
00096|    for row in rows:
00097|        row_year, row_month = row_period(row)
00098|        if (row_year, row_month) != (year, month):
00099|            continue
00100|        total += convert_row_amount_to_usd(row, fx_map)
00101|        used += 1
00102|
00103|    return {"une": une, "total_usd": total, "used_rows": used, "fx": fx}
00104|
00105|
00106|def investment_real_map_for_periods(
00107|    periods: list[tuple[int, int]] | None = None,
00108|    *,
00109|    une: UNE | None = None,
00110|    fx_map: dict[tuple[int, int], Decimal] | None = None,
00111|) -> dict[tuple[int, int, int], Decimal]:
00112|    """
00113|    Mapa (year, month, une_id) -> total USD.
00114|    Si periods es None, usa todas las filas Investment.
00115|    """
00116|    une = une or get_investment_une()
00117|    fx_map = fx_map if fx_map is not None else build_fx_map()
00118|    out: dict[tuple[int, int, int], Decimal] = {}
00119|    if not une:
00120|        return out
00121|
00122|    qs = NewClientImportRow.objects.select_related("header", "currency", "une").filter(
00123|        une=une
00124|    )
00125|    if periods:
00126|        detail_period_q = Q()
00127|        for y, m in periods:
00128|            detail_period_q |= Q(year=y, month=m)
00129|            detail_period_q |= Q(header__year=y, header__month=m)
00130|        qs = qs.filter(detail_period_q)
00131|
00132|    for row in qs:
00133|        row_year, row_month = row_period(row)
00134|        if not row_year or not row_month:
00135|            continue
00136|        key = (row_year, row_month, une.id)
00137|        out[key] = out.get(key, Decimal("0")) + convert_row_amount_to_usd(row, fx_map)
00138|    return out

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiCkluZ3Jlc29zIEludmVzdG1lbnQgZGVzZGUgTmV3Q2xpZW50SW1wb3J0Um93LgoKRnVlbnRlIMO6bmljYSBwYXJhIHZpc3RhL3JlcG9ydGUgeSBwYXJhIHBlcnNpc3RpciBlbiBNb250aGx5TWV0cmljUmVzdWx0LgpSZWdsYSAoYWxpbmVhZGEgY29uIC9wZ2MvaW5ncmVzb3MvKToKLSBzdW1hIFRPRE9TIGxvcyByZWdpc3Ryb3MgZGVsIG1lcyBkZSBsYSBVTkUgSW52ZXN0bWVudCAobm8gc29sbyBjb3VudHNfYXNfbmV3KQotIFVTRCBzZSB0b21hIHRhbCBjdWFsOyBHVFEgc2UgY29udmllcnRlIGNvbiBNb250aGx5RXhjaGFuZ2VSYXRlIGRlbCBtZXMgZGUgbGEgZmlsYQotIE5ld0NsaWVudEltcG9ydFJvdy5hbW91bnQgeWEgdmllbmUgZW4gbWlsZXMgKE1vbnRvIGRlbCBhcmNoaXZvIMO3IDEwMDAgYWwgaW1wb3J0YXIpCiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsCgpmcm9tIGRqYW5nby5kYi5tb2RlbHMgaW1wb3J0IFEKCmZyb20gY29yZS5tb2RlbHMgaW1wb3J0IFVORQpmcm9tIGltcG9ydHMubW9kZWxzIGltcG9ydCBOZXdDbGllbnRJbXBvcnRSb3cKZnJvbSBwZ2MubW9kZWxzIGltcG9ydCBNb250aGx5RXhjaGFuZ2VSYXRlCgpJTlZFU1RNRU5UX1VORV9DT0RFUyA9ICgiSU5WRVNUTUVOVCIsICJJTlZFU1RNRU5UUyIsICJJTlZFUlNJT05FUyIpCgoKZGVmIGdldF9pbnZlc3RtZW50X3VuZSgpIC0+IFVORSB8IE5vbmU6CiAgICByZXR1cm4gKAogICAgICAgIFVORS5vYmplY3RzLmZpbHRlcihjb2RlX19pbj1JTlZFU1RNRU5UX1VORV9DT0RFUykKICAgICAgICAub3JkZXJfYnkoInNvcnRfb3JkZXIiLCAiaWQiKQogICAgICAgIC5maXJzdCgpCiAgICApCgoKZGVmIGJ1aWxkX2Z4X21hcCgpIC0+IGRpY3RbdHVwbGVbaW50LCBpbnRdLCBEZWNpbWFsXToKICAgIHJldHVybiB7CiAgICAgICAgKGl0ZW0ueWVhciwgaXRlbS5tb250aCk6IGl0ZW0udXNkX3RvX2d0cQogICAgICAgIGZvciBpdGVtIGluIE1vbnRobHlFeGNoYW5nZVJhdGUub2JqZWN0cy5hbGwoKQogICAgfQoKCmRlZiByb3dfcGVyaW9kKHJvdykgLT4gdHVwbGVbaW50IHwgTm9uZSwgaW50IHwgTm9uZV06CiAgICB5ZWFyID0gcm93LnllYXIgb3IgKHJvdy5oZWFkZXIueWVhciBpZiBnZXRhdHRyKHJvdywgImhlYWRlcl9pZCIsIE5vbmUpIGFuZCByb3cuaGVhZGVyIGVsc2UgTm9uZSkKICAgIG1vbnRoID0gcm93Lm1vbnRoIG9yICgKICAgICAgICByb3cuaGVhZGVyLm1vbnRoIGlmIGdldGF0dHIocm93LCAiaGVhZGVyX2lkIiwgTm9uZSkgYW5kIHJvdy5oZWFkZXIgZWxzZSBOb25lCiAgICApCiAgICByZXR1cm4geWVhciwgbW9udGgKCgpkZWYgY29udmVydF9yb3dfYW1vdW50X3RvX3VzZChyb3csIGZ4X21hcDogZGljdFt0dXBsZVtpbnQsIGludF0sIERlY2ltYWxdKSAtPiBEZWNpbWFsOgogICAgIiIiTWlzbWEgc2Vtw6FudGljYSBxdWUgbGEgdmlzdGEgZGUgaW5ncmVzb3MgKFVTRCB0YWwgY3VhbCwgR1RRL0ZYLCByZXN0byAwKS4iIiIKICAgIGFtb3VudCA9IHJvdy5hbW91bnQgaWYgcm93LmFtb3VudCBpcyBub3QgTm9uZSBlbHNlIERlY2ltYWwoIjAiKQogICAgY3VycmVuY3lfY29kZSA9ICgocm93LmN1cnJlbmN5LmNvZGUgaWYgcm93LmN1cnJlbmN5IGVsc2UgIiIpIG9yICIiKS51cHBlcigpCgogICAgaWYgYW1vdW50ID09IDA6CiAgICAgICAgcmV0dXJuIERlY2ltYWwoIjAiKQoKICAgIGlmIGN1cnJlbmN5X2NvZGUgaW4gKCJVU0QiLCAiVVMkIiwgIiQiKToKICAgICAgICByZXR1cm4gYW1vdW50CgogICAgaWYgY3VycmVuY3lfY29kZSBpbiAoIkdUUSIsICJRIiwgIlFVRVRaQUxFUyIsICJRVUVUWkFMIik6CiAgICAgICAgcm93X3llYXIsIHJvd19tb250aCA9IHJvd19wZXJpb2Qocm93KQogICAgICAgIGZ4ID0gZnhfbWFwLmdldCgocm93X3llYXIsIHJvd19tb250aCkpCiAgICAgICAgaWYgZnggYW5kIGZ4ICE9IDA6CiAgICAgICAgICAgIHJldHVybiBhbW91bnQgLyBmeAoKICAgIHJldHVybiBEZWNpbWFsKCIwIikKCgpkZWYgc3VtX2ludmVzdG1lbnRfaW5ncmVzb3NfdXNkKAogICAgeWVhcjogaW50LAogICAgbW9udGg6IGludCwKICAgICosCiAgICB1bmU6IFVORSB8IE5vbmUgPSBOb25lLAogICAgZnhfbWFwOiBkaWN0W3R1cGxlW2ludCwgaW50XSwgRGVjaW1hbF0gfCBOb25lID0gTm9uZSwKKSAtPiBkaWN0OgogICAgIiIiCiAgICBUb3RhbGVzIEludmVzdG1lbnQgcGFyYSB1biBtZXMgKG1pc21hIGzDs2dpY2EgcXVlIC9wZ2MvaW5ncmVzb3MvKS4KCiAgICBSZXR1cm5zOgogICAgICAgIHVuZSwgdG90YWxfdXNkLCB1c2VkX3Jvd3MsIGZ4IChUQyBkZWwgeWVhci9tb250aCBwZWRpZG8pCiAgICAiIiIKICAgIHVuZSA9IHVuZSBvciBnZXRfaW52ZXN0bWVudF91bmUoKQogICAgZnhfbWFwID0gZnhfbWFwIGlmIGZ4X21hcCBpcyBub3QgTm9uZSBlbHNlIGJ1aWxkX2Z4X21hcCgpCiAgICBmeCA9IGZ4X21hcC5nZXQoKHllYXIsIG1vbnRoKSkKCiAgICBpZiBub3QgdW5lOgogICAgICAgIHJldHVybiB7InVuZSI6IE5vbmUsICJ0b3RhbF91c2QiOiBEZWNpbWFsKCIwIiksICJ1c2VkX3Jvd3MiOiAwLCAiZngiOiBmeH0KCiAgICBwZXJpb2RfcSA9IFEoeWVhcj15ZWFyLCBtb250aD1tb250aCkgfCBRKGhlYWRlcl9feWVhcj15ZWFyLCBoZWFkZXJfX21vbnRoPW1vbnRoKQogICAgcm93cyA9ICgKICAgICAgICBOZXdDbGllbnRJbXBvcnRSb3cub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgiaGVhZGVyIiwgImN1cnJlbmN5IiwgInVuZSIpCiAgICAgICAgLmZpbHRlcih1bmU9dW5lKQogICAgICAgIC5maWx0ZXIocGVyaW9kX3EpCiAgICApCgogICAgdG90YWwgPSBEZWNpbWFsKCIwIikKICAgIHVzZWQgPSAwCiAgICBmb3Igcm93IGluIHJvd3M6CiAgICAgICAgcm93X3llYXIsIHJvd19tb250aCA9IHJvd19wZXJpb2Qocm93KQogICAgICAgIGlmIChyb3dfeWVhciwgcm93X21vbnRoKSAhPSAoeWVhciwgbW9udGgpOgogICAgICAgICAgICBjb250aW51ZQogICAgICAgIHRvdGFsICs9IGNvbnZlcnRfcm93X2Ftb3VudF90b191c2Qocm93LCBmeF9tYXApCiAgICAgICAgdXNlZCArPSAxCgogICAgcmV0dXJuIHsidW5lIjogdW5lLCAidG90YWxfdXNkIjogdG90YWwsICJ1c2VkX3Jvd3MiOiB1c2VkLCAiZngiOiBmeH0KCgpkZWYgaW52ZXN0bWVudF9yZWFsX21hcF9mb3JfcGVyaW9kcygKICAgIHBlcmlvZHM6IGxpc3RbdHVwbGVbaW50LCBpbnRdXSB8IE5vbmUgPSBOb25lLAogICAgKiwKICAgIHVuZTogVU5FIHwgTm9uZSA9IE5vbmUsCiAgICBmeF9tYXA6IGRpY3RbdHVwbGVbaW50LCBpbnRdLCBEZWNpbWFsXSB8IE5vbmUgPSBOb25lLAopIC0+IGRpY3RbdHVwbGVbaW50LCBpbnQsIGludF0sIERlY2ltYWxdOgogICAgIiIiCiAgICBNYXBhICh5ZWFyLCBtb250aCwgdW5lX2lkKSAtPiB0b3RhbCBVU0QuCiAgICBTaSBwZXJpb2RzIGVzIE5vbmUsIHVzYSB0b2RhcyBsYXMgZmlsYXMgSW52ZXN0bWVudC4KICAgICIiIgogICAgdW5lID0gdW5lIG9yIGdldF9pbnZlc3RtZW50X3VuZSgpCiAgICBmeF9tYXAgPSBmeF9tYXAgaWYgZnhfbWFwIGlzIG5vdCBOb25lIGVsc2UgYnVpbGRfZnhfbWFwKCkKICAgIG91dDogZGljdFt0dXBsZVtpbnQsIGludCwgaW50XSwgRGVjaW1hbF0gPSB7fQogICAgaWYgbm90IHVuZToKICAgICAgICByZXR1cm4gb3V0CgogICAgcXMgPSBOZXdDbGllbnRJbXBvcnRSb3cub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgiaGVhZGVyIiwgImN1cnJlbmN5IiwgInVuZSIpLmZpbHRlcigKICAgICAgICB1bmU9dW5lCiAgICApCiAgICBpZiBwZXJpb2RzOgogICAgICAgIGRldGFpbF9wZXJpb2RfcSA9IFEoKQogICAgICAgIGZvciB5LCBtIGluIHBlcmlvZHM6CiAgICAgICAgICAgIGRldGFpbF9wZXJpb2RfcSB8PSBRKHllYXI9eSwgbW9udGg9bSkKICAgICAgICAgICAgZGV0YWlsX3BlcmlvZF9xIHw9IFEoaGVhZGVyX195ZWFyPXksIGhlYWRlcl9fbW9udGg9bSkKICAgICAgICBxcyA9IHFzLmZpbHRlcihkZXRhaWxfcGVyaW9kX3EpCgogICAgZm9yIHJvdyBpbiBxczoKICAgICAgICByb3dfeWVhciwgcm93X21vbnRoID0gcm93X3BlcmlvZChyb3cpCiAgICAgICAgaWYgbm90IHJvd195ZWFyIG9yIG5vdCByb3dfbW9udGg6CiAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAga2V5ID0gKHJvd195ZWFyLCByb3dfbW9udGgsIHVuZS5pZCkKICAgICAgICBvdXRba2V5XSA9IG91dC5nZXQoa2V5LCBEZWNpbWFsKCIwIikpICsgY29udmVydF9yb3dfYW1vdW50X3RvX3VzZChyb3csIGZ4X21hcCkKICAgIHJldHVybiBvdXQK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/management/__init__.py
PATH_JSON="pgc/management/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/management/commands/__init__.py
PATH_JSON="pgc/management/commands/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/management/commands/recalc_stale_ingresos.py
PATH_JSON="pgc/management/commands/recalc_stale_ingresos.py"
FILENAME=recalc_stale_ingresos.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=29
SIZE_BYTES_UTF8=958
CONTENT_SHA256=32ed593992bebc483158ad315ad1086072553bbcbcf81a7e7a8f4fe674c6d6ff
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.core.management.base import BaseCommand, CommandError

from pgc.income_conversion import recalc_stale_ingresos


class Command(BaseCommand):
    help = (
        "Recalcula INGRESOS con conversion_status=STALE_FX "
        "desde source_value GTQ usando el TC actual del mes."
    )

    def add_arguments(self, parser):
        parser.add_argument("--year", type=int, required=True)
        parser.add_argument("--month", type=int, required=True)

    def handle(self, *args, **options):
        year = options["year"]
        month = options["month"]
        try:
            result = recalc_stale_ingresos(year=year, month=month, only_stale=True)
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"{year}-{month:02d}: {result['updated']} ingreso(s) recalculado(s) "
                f"con TC={result['fx']}."
            )
        )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.core.management.base import BaseCommand, CommandError
00002|
00003|from pgc.income_conversion import recalc_stale_ingresos
00004|
00005|
00006|class Command(BaseCommand):
00007|    help = (
00008|        "Recalcula INGRESOS con conversion_status=STALE_FX "
00009|        "desde source_value GTQ usando el TC actual del mes."
00010|    )
00011|
00012|    def add_arguments(self, parser):
00013|        parser.add_argument("--year", type=int, required=True)
00014|        parser.add_argument("--month", type=int, required=True)
00015|
00016|    def handle(self, *args, **options):
00017|        year = options["year"]
00018|        month = options["month"]
00019|        try:
00020|            result = recalc_stale_ingresos(year=year, month=month, only_stale=True)
00021|        except ValueError as exc:
00022|            raise CommandError(str(exc)) from exc
00023|
00024|        self.stdout.write(
00025|            self.style.SUCCESS(
00026|                f"{year}-{month:02d}: {result['updated']} ingreso(s) recalculado(s) "
00027|                f"con TC={result['fx']}."
00028|            )
00029|        )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29yZS5tYW5hZ2VtZW50LmJhc2UgaW1wb3J0IEJhc2VDb21tYW5kLCBDb21tYW5kRXJyb3IKCmZyb20gcGdjLmluY29tZV9jb252ZXJzaW9uIGltcG9ydCByZWNhbGNfc3RhbGVfaW5ncmVzb3MKCgpjbGFzcyBDb21tYW5kKEJhc2VDb21tYW5kKToKICAgIGhlbHAgPSAoCiAgICAgICAgIlJlY2FsY3VsYSBJTkdSRVNPUyBjb24gY29udmVyc2lvbl9zdGF0dXM9U1RBTEVfRlggIgogICAgICAgICJkZXNkZSBzb3VyY2VfdmFsdWUgR1RRIHVzYW5kbyBlbCBUQyBhY3R1YWwgZGVsIG1lcy4iCiAgICApCgogICAgZGVmIGFkZF9hcmd1bWVudHMoc2VsZiwgcGFyc2VyKToKICAgICAgICBwYXJzZXIuYWRkX2FyZ3VtZW50KCItLXllYXIiLCB0eXBlPWludCwgcmVxdWlyZWQ9VHJ1ZSkKICAgICAgICBwYXJzZXIuYWRkX2FyZ3VtZW50KCItLW1vbnRoIiwgdHlwZT1pbnQsIHJlcXVpcmVkPVRydWUpCgogICAgZGVmIGhhbmRsZShzZWxmLCAqYXJncywgKipvcHRpb25zKToKICAgICAgICB5ZWFyID0gb3B0aW9uc1sieWVhciJdCiAgICAgICAgbW9udGggPSBvcHRpb25zWyJtb250aCJdCiAgICAgICAgdHJ5OgogICAgICAgICAgICByZXN1bHQgPSByZWNhbGNfc3RhbGVfaW5ncmVzb3MoeWVhcj15ZWFyLCBtb250aD1tb250aCwgb25seV9zdGFsZT1UcnVlKQogICAgICAgIGV4Y2VwdCBWYWx1ZUVycm9yIGFzIGV4YzoKICAgICAgICAgICAgcmFpc2UgQ29tbWFuZEVycm9yKHN0cihleGMpKSBmcm9tIGV4YwoKICAgICAgICBzZWxmLnN0ZG91dC53cml0ZSgKICAgICAgICAgICAgc2VsZi5zdHlsZS5TVUNDRVNTKAogICAgICAgICAgICAgICAgZiJ7eWVhcn0te21vbnRoOjAyZH06IHtyZXN1bHRbJ3VwZGF0ZWQnXX0gaW5ncmVzbyhzKSByZWNhbGN1bGFkbyhzKSAiCiAgICAgICAgICAgICAgICBmImNvbiBUQz17cmVzdWx0WydmeCddfS4iCiAgICAgICAgICAgICkKICAgICAgICApCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/models.py
PATH_JSON="pgc/models.py"
FILENAME=models.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=313
SIZE_BYTES_UTF8=11541
CONTENT_SHA256=fe83c72a2c44d569cd19b35b9221156ec810c806e932282cb0218641e597c728
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
# pgc/models.py

from django.conf import settings
from django.db import models
from core.models import TimeStampedModel, UNE, MetricDefinition


class PGCMode(models.TextChoices):
    MODO1 = "modo1", "Modo 1"
    MODO2 = "modo2", "Modo 2"


class MonthlyMetricScore(TimeStampedModel):
    plan = models.ForeignKey("PGCPlan", on_delete=models.CASCADE, related_name="metric_scores")
    une = models.ForeignKey(UNE, on_delete=models.CASCADE, related_name="metric_scores")
    metric = models.ForeignKey(MetricDefinition, on_delete=models.CASCADE, related_name="metric_scores")
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    mode = models.CharField(max_length=10, choices=PGCMode.choices, default=PGCMode.MODO1)

    measured_value = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    target_value = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)

    is_achieved = models.BooleanField(default=False)
    points_awarded = models.DecimalField(max_digits=18, decimal_places=4, default=0)

    carry_in = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    carry_used = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    carry_generated = models.DecimalField(max_digits=18, decimal_places=4, default=0)

    calculation_note = models.TextField(blank=True)

    class Meta:
        unique_together = ("plan", "une", "metric", "year", "month", "mode")
        ordering = ["year", "month", "une__sort_order", "metric__code", "mode"]

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.une.code} {self.metric.code} {self.mode}"


class MonthlyModeScorecard(TimeStampedModel):
    plan = models.ForeignKey("PGCPlan", on_delete=models.CASCADE, related_name="mode_scorecards")
    une = models.ForeignKey(UNE, on_delete=models.CASCADE, related_name="mode_scorecards")
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    mode = models.CharField(max_length=10, choices=PGCMode.choices, default=PGCMode.MODO1)

    total_points = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    qualified_threshold = models.DecimalField(max_digits=18, decimal_places=4, default=80)
    is_month_qualified = models.BooleanField(default=False)
    summary_note = models.TextField(blank=True)

    class Meta:
        unique_together = ("plan", "une", "year", "month", "mode")
        ordering = ["year", "month", "une__sort_order", "mode"]

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.une.code} {self.mode} ({self.total_points} pts)"


class MetricReserve(TimeStampedModel):
    plan = models.ForeignKey("PGCPlan", on_delete=models.CASCADE, related_name="metric_reserves")
    une = models.ForeignKey(UNE, on_delete=models.CASCADE, related_name="metric_reserves")
    metric = models.ForeignKey(MetricDefinition, on_delete=models.CASCADE, related_name="metric_reserves")

    mode = models.CharField(max_length=10, choices=PGCMode.choices, default=PGCMode.MODO2)

    source_year = models.PositiveIntegerField()
    source_month = models.PositiveIntegerField()

    amount = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    remaining = models.DecimalField(max_digits=18, decimal_places=4, default=0)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["source_year", "source_month", "une__sort_order", "metric__code"]

    def __str__(self):
        return f"{self.source_year}-{self.source_month:02d} {self.une.code} {self.metric.code} rem={self.remaining}"


class MonthlyExchangeRate(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    usd_to_gtq = models.DecimalField(max_digits=10, decimal_places=5)

    class Meta:
        unique_together = ("year", "month")
        ordering = ["year", "month"]

    def __str__(self):
        return f"{self.year}-{self.month:02d}: 1 USD = {self.usd_to_gtq} GTQ"


class PGCPlan(TimeStampedModel):
    year = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100, default="Plan PGC")
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-year"]
        verbose_name = "Plan PGC"
        verbose_name_plural = "Planes PGC"

    def __str__(self):
        return f"{self.name} {self.year}"


class MonthlyTarget(TimeStampedModel):
    plan = models.ForeignKey(
        PGCPlan,
        on_delete=models.CASCADE,
        related_name="monthly_targets",
    )
    une = models.ForeignKey(
        UNE,
        on_delete=models.CASCADE,
        related_name="monthly_targets",
    )
    metric = models.ForeignKey(
        MetricDefinition,
        on_delete=models.CASCADE,
        related_name="monthly_targets",
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    target_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    points_if_achieved = models.PositiveIntegerField(default=0)
    reference_annual_value = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Solo referencia; no asigna puntos por sí misma.",
    )
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("plan", "une", "metric", "year", "month")
        ordering = ["year", "month", "une__sort_order", "metric__code"]
        verbose_name = "Meta mensual"
        verbose_name_plural = "Metas mensuales"

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.une.code} {self.metric.code}"


class MonthlyMetricResult(TimeStampedModel):
    # conversion_status for manual/auto income capture
    CONVERSION_NATIVE_USD = "NATIVE_USD"
    CONVERSION_CONVERTED = "CONVERTED"
    CONVERSION_MISSING_FX = "MISSING_FX"
    CONVERSION_STALE_FX = "STALE_FX"
    CONVERSION_CHOICES = [
        (CONVERSION_NATIVE_USD, "USD nativo / legado"),
        (CONVERSION_CONVERTED, "Convertido GTQ→USD"),
        (CONVERSION_MISSING_FX, "Sin tipo de cambio"),
        (CONVERSION_STALE_FX, "TC desactualizado"),
    ]

    CURRENCY_GTQ = "GTQ"
    CURRENCY_USD = "USD"

    plan = models.ForeignKey(
        PGCPlan,
        on_delete=models.CASCADE,
        related_name="metric_results",
    )
    une = models.ForeignKey(
        UNE,
        on_delete=models.CASCADE,
        related_name="metric_results",
    )
    metric = models.ForeignKey(
        MetricDefinition,
        on_delete=models.CASCADE,
        related_name="metric_results",
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    # Canonical value for scoring/reporting: always USD for INGRESOS.
    measured_value = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    target_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    is_achieved = models.BooleanField(default=False)
    points_awarded = models.PositiveIntegerField(default=0)
    calculation_note = models.TextField(blank=True)

    # Financial capture trail (mainly for manual/auto INGRESOS).
    source_currency = models.CharField(max_length=3, blank=True, default="")
    source_value = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    exchange_rate_used = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    conversion_status = models.CharField(
        max_length=20,
        choices=CONVERSION_CHOICES,
        blank=True,
        default="",
    )

    class Meta:
        unique_together = ("plan", "une", "metric", "year", "month")
        ordering = ["year", "month", "une__sort_order", "metric__code"]
        verbose_name = "Resultado mensual de métrica"
        verbose_name_plural = "Resultados mensuales de métricas"

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.une.code} {self.metric.code}"


class MonthlyScorecard(TimeStampedModel):
    plan = models.ForeignKey(
        PGCPlan,
        on_delete=models.CASCADE,
        related_name="scorecards",
    )
    une = models.ForeignKey(
        UNE,
        on_delete=models.CASCADE,
        related_name="scorecards",
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    total_points = models.PositiveIntegerField(default=0)
    qualified_threshold = models.PositiveIntegerField(default=80)
    is_month_qualified = models.BooleanField(default=False)
    summary_note = models.TextField(blank=True)

    class Meta:
        unique_together = ("plan", "une", "year", "month")
        ordering = ["year", "month", "une__sort_order"]
        verbose_name = "Score mensual"
        verbose_name_plural = "Scores mensuales"

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.une.code} ({self.total_points} pts)"


class ManualRequirementsCompliance(TimeStampedModel):
    plan = models.ForeignKey(
        PGCPlan,
        on_delete=models.CASCADE,
        related_name="manual_requirements",
    )
    une = models.ForeignKey(
        UNE,
        on_delete=models.CASCADE,
        related_name="manual_requirements",
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    is_compliant = models.BooleanField(default=True)
    incident_note = models.TextField(blank=True)

    class Meta:
        unique_together = ("plan", "une", "year", "month")
        ordering = ["year", "month", "une__sort_order"]
        verbose_name = "Cumplimiento manual de requerimientos"
        verbose_name_plural = "Cumplimientos manuales de requerimientos"

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.une.code} cumplimiento={self.is_compliant}"


class AdminManualEditLog(TimeStampedModel):
    """Trazabilidad básica de cambios manuales desde Administración."""

    ENTITY_TARGET = "target"
    ENTITY_RESULT = "result"
    ENTITY_REQUIREMENT = "requirement"
    ENTITY_FX = "fx"
    ENTITY_ALIAS = "alias"
    ENTITY_NEW_CLIENT_ROW = "new_client_row"
    ENTITY_CROSS_SALE_ROW = "cross_sale_row"
    ENTITY_PERIOD_NOTE = "period_note"

    ENTITY_CHOICES = [
        (ENTITY_TARGET, "Meta mensual"),
        (ENTITY_RESULT, "Resultado mensual"),
        (ENTITY_REQUIREMENT, "Requerimiento manual"),
        (ENTITY_FX, "Tipo de cambio"),
        (ENTITY_ALIAS, "Alias UNE"),
        (ENTITY_NEW_CLIENT_ROW, "Fila cliente nuevo"),
        (ENTITY_CROSS_SALE_ROW, "Fila venta cruzada"),
        (ENTITY_PERIOD_NOTE, "Nota del período"),
    ]

    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    entity_type = models.CharField(max_length=30, choices=ENTITY_CHOICES)
    entity_id = models.PositiveIntegerField(null=True, blank=True)
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    reason = models.TextField(blank=True)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admin_manual_edits",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Bitácora de edición manual"
        verbose_name_plural = "Bitácora de ediciones manuales"

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.entity_type}.{self.field_name}"
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|# pgc/models.py
00002|
00003|from django.conf import settings
00004|from django.db import models
00005|from core.models import TimeStampedModel, UNE, MetricDefinition
00006|
00007|
00008|class PGCMode(models.TextChoices):
00009|    MODO1 = "modo1", "Modo 1"
00010|    MODO2 = "modo2", "Modo 2"
00011|
00012|
00013|class MonthlyMetricScore(TimeStampedModel):
00014|    plan = models.ForeignKey("PGCPlan", on_delete=models.CASCADE, related_name="metric_scores")
00015|    une = models.ForeignKey(UNE, on_delete=models.CASCADE, related_name="metric_scores")
00016|    metric = models.ForeignKey(MetricDefinition, on_delete=models.CASCADE, related_name="metric_scores")
00017|    year = models.PositiveIntegerField()
00018|    month = models.PositiveIntegerField()
00019|
00020|    mode = models.CharField(max_length=10, choices=PGCMode.choices, default=PGCMode.MODO1)
00021|
00022|    measured_value = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
00023|    target_value = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
00024|
00025|    is_achieved = models.BooleanField(default=False)
00026|    points_awarded = models.DecimalField(max_digits=18, decimal_places=4, default=0)
00027|
00028|    carry_in = models.DecimalField(max_digits=18, decimal_places=4, default=0)
00029|    carry_used = models.DecimalField(max_digits=18, decimal_places=4, default=0)
00030|    carry_generated = models.DecimalField(max_digits=18, decimal_places=4, default=0)
00031|
00032|    calculation_note = models.TextField(blank=True)
00033|
00034|    class Meta:
00035|        unique_together = ("plan", "une", "metric", "year", "month", "mode")
00036|        ordering = ["year", "month", "une__sort_order", "metric__code", "mode"]
00037|
00038|    def __str__(self):
00039|        return f"{self.year}-{self.month:02d} {self.une.code} {self.metric.code} {self.mode}"
00040|
00041|
00042|class MonthlyModeScorecard(TimeStampedModel):
00043|    plan = models.ForeignKey("PGCPlan", on_delete=models.CASCADE, related_name="mode_scorecards")
00044|    une = models.ForeignKey(UNE, on_delete=models.CASCADE, related_name="mode_scorecards")
00045|    year = models.PositiveIntegerField()
00046|    month = models.PositiveIntegerField()
00047|
00048|    mode = models.CharField(max_length=10, choices=PGCMode.choices, default=PGCMode.MODO1)
00049|
00050|    total_points = models.DecimalField(max_digits=18, decimal_places=4, default=0)
00051|    qualified_threshold = models.DecimalField(max_digits=18, decimal_places=4, default=80)
00052|    is_month_qualified = models.BooleanField(default=False)
00053|    summary_note = models.TextField(blank=True)
00054|
00055|    class Meta:
00056|        unique_together = ("plan", "une", "year", "month", "mode")
00057|        ordering = ["year", "month", "une__sort_order", "mode"]
00058|
00059|    def __str__(self):
00060|        return f"{self.year}-{self.month:02d} {self.une.code} {self.mode} ({self.total_points} pts)"
00061|
00062|
00063|class MetricReserve(TimeStampedModel):
00064|    plan = models.ForeignKey("PGCPlan", on_delete=models.CASCADE, related_name="metric_reserves")
00065|    une = models.ForeignKey(UNE, on_delete=models.CASCADE, related_name="metric_reserves")
00066|    metric = models.ForeignKey(MetricDefinition, on_delete=models.CASCADE, related_name="metric_reserves")
00067|
00068|    mode = models.CharField(max_length=10, choices=PGCMode.choices, default=PGCMode.MODO2)
00069|
00070|    source_year = models.PositiveIntegerField()
00071|    source_month = models.PositiveIntegerField()
00072|
00073|    amount = models.DecimalField(max_digits=18, decimal_places=4, default=0)
00074|    remaining = models.DecimalField(max_digits=18, decimal_places=4, default=0)
00075|
00076|    notes = models.TextField(blank=True)
00077|
00078|    class Meta:
00079|        ordering = ["source_year", "source_month", "une__sort_order", "metric__code"]
00080|
00081|    def __str__(self):
00082|        return f"{self.source_year}-{self.source_month:02d} {self.une.code} {self.metric.code} rem={self.remaining}"
00083|
00084|
00085|class MonthlyExchangeRate(models.Model):
00086|    year = models.PositiveIntegerField()
00087|    month = models.PositiveIntegerField()
00088|    usd_to_gtq = models.DecimalField(max_digits=10, decimal_places=5)
00089|
00090|    class Meta:
00091|        unique_together = ("year", "month")
00092|        ordering = ["year", "month"]
00093|
00094|    def __str__(self):
00095|        return f"{self.year}-{self.month:02d}: 1 USD = {self.usd_to_gtq} GTQ"
00096|
00097|
00098|class PGCPlan(TimeStampedModel):
00099|    year = models.PositiveIntegerField(unique=True)
00100|    name = models.CharField(max_length=100, default="Plan PGC")
00101|    is_active = models.BooleanField(default=True)
00102|    notes = models.TextField(blank=True)
00103|
00104|    class Meta:
00105|        ordering = ["-year"]
00106|        verbose_name = "Plan PGC"
00107|        verbose_name_plural = "Planes PGC"
00108|
00109|    def __str__(self):
00110|        return f"{self.name} {self.year}"
00111|
00112|
00113|class MonthlyTarget(TimeStampedModel):
00114|    plan = models.ForeignKey(
00115|        PGCPlan,
00116|        on_delete=models.CASCADE,
00117|        related_name="monthly_targets",
00118|    )
00119|    une = models.ForeignKey(
00120|        UNE,
00121|        on_delete=models.CASCADE,
00122|        related_name="monthly_targets",
00123|    )
00124|    metric = models.ForeignKey(
00125|        MetricDefinition,
00126|        on_delete=models.CASCADE,
00127|        related_name="monthly_targets",
00128|    )
00129|    year = models.PositiveIntegerField()
00130|    month = models.PositiveIntegerField()
00131|    target_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00132|    points_if_achieved = models.PositiveIntegerField(default=0)
00133|    reference_annual_value = models.DecimalField(
00134|        max_digits=18,
00135|        decimal_places=2,
00136|        null=True,
00137|        blank=True,
00138|        help_text="Solo referencia; no asigna puntos por sí misma.",
00139|    )
00140|    notes = models.TextField(blank=True)
00141|
00142|    class Meta:
00143|        unique_together = ("plan", "une", "metric", "year", "month")
00144|        ordering = ["year", "month", "une__sort_order", "metric__code"]
00145|        verbose_name = "Meta mensual"
00146|        verbose_name_plural = "Metas mensuales"
00147|
00148|    def __str__(self):
00149|        return f"{self.year}-{self.month:02d} {self.une.code} {self.metric.code}"
00150|
00151|
00152|class MonthlyMetricResult(TimeStampedModel):
00153|    # conversion_status for manual/auto income capture
00154|    CONVERSION_NATIVE_USD = "NATIVE_USD"
00155|    CONVERSION_CONVERTED = "CONVERTED"
00156|    CONVERSION_MISSING_FX = "MISSING_FX"
00157|    CONVERSION_STALE_FX = "STALE_FX"
00158|    CONVERSION_CHOICES = [
00159|        (CONVERSION_NATIVE_USD, "USD nativo / legado"),
00160|        (CONVERSION_CONVERTED, "Convertido GTQ→USD"),
00161|        (CONVERSION_MISSING_FX, "Sin tipo de cambio"),
00162|        (CONVERSION_STALE_FX, "TC desactualizado"),
00163|    ]
00164|
00165|    CURRENCY_GTQ = "GTQ"
00166|    CURRENCY_USD = "USD"
00167|
00168|    plan = models.ForeignKey(
00169|        PGCPlan,
00170|        on_delete=models.CASCADE,
00171|        related_name="metric_results",
00172|    )
00173|    une = models.ForeignKey(
00174|        UNE,
00175|        on_delete=models.CASCADE,
00176|        related_name="metric_results",
00177|    )
00178|    metric = models.ForeignKey(
00179|        MetricDefinition,
00180|        on_delete=models.CASCADE,
00181|        related_name="metric_results",
00182|    )
00183|    year = models.PositiveIntegerField()
00184|    month = models.PositiveIntegerField()
00185|    # Canonical value for scoring/reporting: always USD for INGRESOS.
00186|    measured_value = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
00187|    target_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00188|    is_achieved = models.BooleanField(default=False)
00189|    points_awarded = models.PositiveIntegerField(default=0)
00190|    calculation_note = models.TextField(blank=True)
00191|
00192|    # Financial capture trail (mainly for manual/auto INGRESOS).
00193|    source_currency = models.CharField(max_length=3, blank=True, default="")
00194|    source_value = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
00195|    exchange_rate_used = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
00196|    conversion_status = models.CharField(
00197|        max_length=20,
00198|        choices=CONVERSION_CHOICES,
00199|        blank=True,
00200|        default="",
00201|    )
00202|
00203|    class Meta:
00204|        unique_together = ("plan", "une", "metric", "year", "month")
00205|        ordering = ["year", "month", "une__sort_order", "metric__code"]
00206|        verbose_name = "Resultado mensual de métrica"
00207|        verbose_name_plural = "Resultados mensuales de métricas"
00208|
00209|    def __str__(self):
00210|        return f"{self.year}-{self.month:02d} {self.une.code} {self.metric.code}"
00211|
00212|
00213|class MonthlyScorecard(TimeStampedModel):
00214|    plan = models.ForeignKey(
00215|        PGCPlan,
00216|        on_delete=models.CASCADE,
00217|        related_name="scorecards",
00218|    )
00219|    une = models.ForeignKey(
00220|        UNE,
00221|        on_delete=models.CASCADE,
00222|        related_name="scorecards",
00223|    )
00224|    year = models.PositiveIntegerField()
00225|    month = models.PositiveIntegerField()
00226|    total_points = models.PositiveIntegerField(default=0)
00227|    qualified_threshold = models.PositiveIntegerField(default=80)
00228|    is_month_qualified = models.BooleanField(default=False)
00229|    summary_note = models.TextField(blank=True)
00230|
00231|    class Meta:
00232|        unique_together = ("plan", "une", "year", "month")
00233|        ordering = ["year", "month", "une__sort_order"]
00234|        verbose_name = "Score mensual"
00235|        verbose_name_plural = "Scores mensuales"
00236|
00237|    def __str__(self):
00238|        return f"{self.year}-{self.month:02d} {self.une.code} ({self.total_points} pts)"
00239|
00240|
00241|class ManualRequirementsCompliance(TimeStampedModel):
00242|    plan = models.ForeignKey(
00243|        PGCPlan,
00244|        on_delete=models.CASCADE,
00245|        related_name="manual_requirements",
00246|    )
00247|    une = models.ForeignKey(
00248|        UNE,
00249|        on_delete=models.CASCADE,
00250|        related_name="manual_requirements",
00251|    )
00252|    year = models.PositiveIntegerField()
00253|    month = models.PositiveIntegerField()
00254|    is_compliant = models.BooleanField(default=True)
00255|    incident_note = models.TextField(blank=True)
00256|
00257|    class Meta:
00258|        unique_together = ("plan", "une", "year", "month")
00259|        ordering = ["year", "month", "une__sort_order"]
00260|        verbose_name = "Cumplimiento manual de requerimientos"
00261|        verbose_name_plural = "Cumplimientos manuales de requerimientos"
00262|
00263|    def __str__(self):
00264|        return f"{self.year}-{self.month:02d} {self.une.code} cumplimiento={self.is_compliant}"
00265|
00266|
00267|class AdminManualEditLog(TimeStampedModel):
00268|    """Trazabilidad básica de cambios manuales desde Administración."""
00269|
00270|    ENTITY_TARGET = "target"
00271|    ENTITY_RESULT = "result"
00272|    ENTITY_REQUIREMENT = "requirement"
00273|    ENTITY_FX = "fx"
00274|    ENTITY_ALIAS = "alias"
00275|    ENTITY_NEW_CLIENT_ROW = "new_client_row"
00276|    ENTITY_CROSS_SALE_ROW = "cross_sale_row"
00277|    ENTITY_PERIOD_NOTE = "period_note"
00278|
00279|    ENTITY_CHOICES = [
00280|        (ENTITY_TARGET, "Meta mensual"),
00281|        (ENTITY_RESULT, "Resultado mensual"),
00282|        (ENTITY_REQUIREMENT, "Requerimiento manual"),
00283|        (ENTITY_FX, "Tipo de cambio"),
00284|        (ENTITY_ALIAS, "Alias UNE"),
00285|        (ENTITY_NEW_CLIENT_ROW, "Fila cliente nuevo"),
00286|        (ENTITY_CROSS_SALE_ROW, "Fila venta cruzada"),
00287|        (ENTITY_PERIOD_NOTE, "Nota del período"),
00288|    ]
00289|
00290|    year = models.PositiveIntegerField()
00291|    month = models.PositiveIntegerField()
00292|    entity_type = models.CharField(max_length=30, choices=ENTITY_CHOICES)
00293|    entity_id = models.PositiveIntegerField(null=True, blank=True)
00294|    field_name = models.CharField(max_length=100)
00295|    old_value = models.TextField(blank=True)
00296|    new_value = models.TextField(blank=True)
00297|    reason = models.TextField(blank=True)
00298|    edited_by = models.ForeignKey(
00299|        settings.AUTH_USER_MODEL,
00300|        on_delete=models.SET_NULL,
00301|        null=True,
00302|        blank=True,
00303|        related_name="admin_manual_edits",
00304|    )
00305|
00306|    class Meta:
00307|        ordering = ["-created_at"]
00308|        verbose_name = "Bitácora de edición manual"
00309|        verbose_name_plural = "Bitácora de ediciones manuales"
00310|
00311|    def __str__(self):
00312|        return f"{self.year}-{self.month:02d} {self.entity_type}.{self.field_name}"
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IyBwZ2MvbW9kZWxzLnB5Cgpmcm9tIGRqYW5nby5jb25mIGltcG9ydCBzZXR0aW5ncwpmcm9tIGRqYW5nby5kYiBpbXBvcnQgbW9kZWxzCmZyb20gY29yZS5tb2RlbHMgaW1wb3J0IFRpbWVTdGFtcGVkTW9kZWwsIFVORSwgTWV0cmljRGVmaW5pdGlvbgoKCmNsYXNzIFBHQ01vZGUobW9kZWxzLlRleHRDaG9pY2VzKToKICAgIE1PRE8xID0gIm1vZG8xIiwgIk1vZG8gMSIKICAgIE1PRE8yID0gIm1vZG8yIiwgIk1vZG8gMiIKCgpjbGFzcyBNb250aGx5TWV0cmljU2NvcmUoVGltZVN0YW1wZWRNb2RlbCk6CiAgICBwbGFuID0gbW9kZWxzLkZvcmVpZ25LZXkoIlBHQ1BsYW4iLCBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsIHJlbGF0ZWRfbmFtZT0ibWV0cmljX3Njb3JlcyIpCiAgICB1bmUgPSBtb2RlbHMuRm9yZWlnbktleShVTkUsIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSwgcmVsYXRlZF9uYW1lPSJtZXRyaWNfc2NvcmVzIikKICAgIG1ldHJpYyA9IG1vZGVscy5Gb3JlaWduS2V5KE1ldHJpY0RlZmluaXRpb24sIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSwgcmVsYXRlZF9uYW1lPSJtZXRyaWNfc2NvcmVzIikKICAgIHllYXIgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoKQogICAgbW9udGggPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoKQoKICAgIG1vZGUgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAsIGNob2ljZXM9UEdDTW9kZS5jaG9pY2VzLCBkZWZhdWx0PVBHQ01vZGUuTU9ETzEpCgogICAgbWVhc3VyZWRfdmFsdWUgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTQsIG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIHRhcmdldF92YWx1ZSA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9NCwgbnVsbD1UcnVlLCBibGFuaz1UcnVlKQoKICAgIGlzX2FjaGlldmVkID0gbW9kZWxzLkJvb2xlYW5GaWVsZChkZWZhdWx0PUZhbHNlKQogICAgcG9pbnRzX2F3YXJkZWQgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTQsIGRlZmF1bHQ9MCkKCiAgICBjYXJyeV9pbiA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9NCwgZGVmYXVsdD0wKQogICAgY2FycnlfdXNlZCA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9NCwgZGVmYXVsdD0wKQogICAgY2FycnlfZ2VuZXJhdGVkID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTE4LCBkZWNpbWFsX3BsYWNlcz00LCBkZWZhdWx0PTApCgogICAgY2FsY3VsYXRpb25fbm90ZSA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIHVuaXF1ZV90b2dldGhlciA9ICgicGxhbiIsICJ1bmUiLCAibWV0cmljIiwgInllYXIiLCAibW9udGgiLCAibW9kZSIpCiAgICAgICAgb3JkZXJpbmcgPSBbInllYXIiLCAibW9udGgiLCAidW5lX19zb3J0X29yZGVyIiwgIm1ldHJpY19fY29kZSIsICJtb2RlIl0KCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi55ZWFyfS17c2VsZi5tb250aDowMmR9IHtzZWxmLnVuZS5jb2RlfSB7c2VsZi5tZXRyaWMuY29kZX0ge3NlbGYubW9kZX0iCgoKY2xhc3MgTW9udGhseU1vZGVTY29yZWNhcmQoVGltZVN0YW1wZWRNb2RlbCk6CiAgICBwbGFuID0gbW9kZWxzLkZvcmVpZ25LZXkoIlBHQ1BsYW4iLCBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsIHJlbGF0ZWRfbmFtZT0ibW9kZV9zY29yZWNhcmRzIikKICAgIHVuZSA9IG1vZGVscy5Gb3JlaWduS2V5KFVORSwgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLCByZWxhdGVkX25hbWU9Im1vZGVfc2NvcmVjYXJkcyIpCiAgICB5ZWFyID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKCkKICAgIG1vbnRoID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKCkKCiAgICBtb2RlID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwLCBjaG9pY2VzPVBHQ01vZGUuY2hvaWNlcywgZGVmYXVsdD1QR0NNb2RlLk1PRE8xKQoKICAgIHRvdGFsX3BvaW50cyA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9NCwgZGVmYXVsdD0wKQogICAgcXVhbGlmaWVkX3RocmVzaG9sZCA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9NCwgZGVmYXVsdD04MCkKICAgIGlzX21vbnRoX3F1YWxpZmllZCA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1GYWxzZSkKICAgIHN1bW1hcnlfbm90ZSA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIHVuaXF1ZV90b2dldGhlciA9ICgicGxhbiIsICJ1bmUiLCAieWVhciIsICJtb250aCIsICJtb2RlIikKICAgICAgICBvcmRlcmluZyA9IFsieWVhciIsICJtb250aCIsICJ1bmVfX3NvcnRfb3JkZXIiLCAibW9kZSJdCgogICAgZGVmIF9fc3RyX18oc2VsZik6CiAgICAgICAgcmV0dXJuIGYie3NlbGYueWVhcn0te3NlbGYubW9udGg6MDJkfSB7c2VsZi51bmUuY29kZX0ge3NlbGYubW9kZX0gKHtzZWxmLnRvdGFsX3BvaW50c30gcHRzKSIKCgpjbGFzcyBNZXRyaWNSZXNlcnZlKFRpbWVTdGFtcGVkTW9kZWwpOgogICAgcGxhbiA9IG1vZGVscy5Gb3JlaWduS2V5KCJQR0NQbGFuIiwgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLCByZWxhdGVkX25hbWU9Im1ldHJpY19yZXNlcnZlcyIpCiAgICB1bmUgPSBtb2RlbHMuRm9yZWlnbktleShVTkUsIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSwgcmVsYXRlZF9uYW1lPSJtZXRyaWNfcmVzZXJ2ZXMiKQogICAgbWV0cmljID0gbW9kZWxzLkZvcmVpZ25LZXkoTWV0cmljRGVmaW5pdGlvbiwgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLCByZWxhdGVkX25hbWU9Im1ldHJpY19yZXNlcnZlcyIpCgogICAgbW9kZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMCwgY2hvaWNlcz1QR0NNb2RlLmNob2ljZXMsIGRlZmF1bHQ9UEdDTW9kZS5NT0RPMikKCiAgICBzb3VyY2VfeWVhciA9IG1vZGVscy5Qb3NpdGl2ZUludGVnZXJGaWVsZCgpCiAgICBzb3VyY2VfbW9udGggPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoKQoKICAgIGFtb3VudCA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9NCwgZGVmYXVsdD0wKQogICAgcmVtYWluaW5nID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTE4LCBkZWNpbWFsX3BsYWNlcz00LCBkZWZhdWx0PTApCgogICAgbm90ZXMgPSBtb2RlbHMuVGV4dEZpZWxkKGJsYW5rPVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICBvcmRlcmluZyA9IFsic291cmNlX3llYXIiLCAic291cmNlX21vbnRoIiwgInVuZV9fc29ydF9vcmRlciIsICJtZXRyaWNfX2NvZGUiXQoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLnNvdXJjZV95ZWFyfS17c2VsZi5zb3VyY2VfbW9udGg6MDJkfSB7c2VsZi51bmUuY29kZX0ge3NlbGYubWV0cmljLmNvZGV9IHJlbT17c2VsZi5yZW1haW5pbmd9IgoKCmNsYXNzIE1vbnRobHlFeGNoYW5nZVJhdGUobW9kZWxzLk1vZGVsKToKICAgIHllYXIgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoKQogICAgbW9udGggPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoKQogICAgdXNkX3RvX2d0cSA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xMCwgZGVjaW1hbF9wbGFjZXM9NSkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIHVuaXF1ZV90b2dldGhlciA9ICgieWVhciIsICJtb250aCIpCiAgICAgICAgb3JkZXJpbmcgPSBbInllYXIiLCAibW9udGgiXQoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLnllYXJ9LXtzZWxmLm1vbnRoOjAyZH06IDEgVVNEID0ge3NlbGYudXNkX3RvX2d0cX0gR1RRIgoKCmNsYXNzIFBHQ1BsYW4oVGltZVN0YW1wZWRNb2RlbCk6CiAgICB5ZWFyID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKHVuaXF1ZT1UcnVlKQogICAgbmFtZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMDAsIGRlZmF1bHQ9IlBsYW4gUEdDIikKICAgIGlzX2FjdGl2ZSA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1UcnVlKQogICAgbm90ZXMgPSBtb2RlbHMuVGV4dEZpZWxkKGJsYW5rPVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICBvcmRlcmluZyA9IFsiLXllYXIiXQogICAgICAgIHZlcmJvc2VfbmFtZSA9ICJQbGFuIFBHQyIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIlBsYW5lcyBQR0MiCgogICAgZGVmIF9fc3RyX18oc2VsZik6CiAgICAgICAgcmV0dXJuIGYie3NlbGYubmFtZX0ge3NlbGYueWVhcn0iCgoKY2xhc3MgTW9udGhseVRhcmdldChUaW1lU3RhbXBlZE1vZGVsKToKICAgIHBsYW4gPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICBQR0NQbGFuLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSwKICAgICAgICByZWxhdGVkX25hbWU9Im1vbnRobHlfdGFyZ2V0cyIsCiAgICApCiAgICB1bmUgPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICBVTkUsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLAogICAgICAgIHJlbGF0ZWRfbmFtZT0ibW9udGhseV90YXJnZXRzIiwKICAgICkKICAgIG1ldHJpYyA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIE1ldHJpY0RlZmluaXRpb24sCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLAogICAgICAgIHJlbGF0ZWRfbmFtZT0ibW9udGhseV90YXJnZXRzIiwKICAgICkKICAgIHllYXIgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoKQogICAgbW9udGggPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoKQogICAgdGFyZ2V0X3ZhbHVlID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTE4LCBkZWNpbWFsX3BsYWNlcz0yLCBudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBwb2ludHNfaWZfYWNoaWV2ZWQgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoZGVmYXVsdD0wKQogICAgcmVmZXJlbmNlX2FubnVhbF92YWx1ZSA9IG1vZGVscy5EZWNpbWFsRmllbGQoCiAgICAgICAgbWF4X2RpZ2l0cz0xOCwKICAgICAgICBkZWNpbWFsX3BsYWNlcz0yLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIGhlbHBfdGV4dD0iU29sbyByZWZlcmVuY2lhOyBubyBhc2lnbmEgcHVudG9zIHBvciBzw60gbWlzbWEuIiwKICAgICkKICAgIG5vdGVzID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgdW5pcXVlX3RvZ2V0aGVyID0gKCJwbGFuIiwgInVuZSIsICJtZXRyaWMiLCAieWVhciIsICJtb250aCIpCiAgICAgICAgb3JkZXJpbmcgPSBbInllYXIiLCAibW9udGgiLCAidW5lX19zb3J0X29yZGVyIiwgIm1ldHJpY19fY29kZSJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIk1ldGEgbWVuc3VhbCIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIk1ldGFzIG1lbnN1YWxlcyIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi55ZWFyfS17c2VsZi5tb250aDowMmR9IHtzZWxmLnVuZS5jb2RlfSB7c2VsZi5tZXRyaWMuY29kZX0iCgoKY2xhc3MgTW9udGhseU1ldHJpY1Jlc3VsdChUaW1lU3RhbXBlZE1vZGVsKToKICAgICMgY29udmVyc2lvbl9zdGF0dXMgZm9yIG1hbnVhbC9hdXRvIGluY29tZSBjYXB0dXJlCiAgICBDT05WRVJTSU9OX05BVElWRV9VU0QgPSAiTkFUSVZFX1VTRCIKICAgIENPTlZFUlNJT05fQ09OVkVSVEVEID0gIkNPTlZFUlRFRCIKICAgIENPTlZFUlNJT05fTUlTU0lOR19GWCA9ICJNSVNTSU5HX0ZYIgogICAgQ09OVkVSU0lPTl9TVEFMRV9GWCA9ICJTVEFMRV9GWCIKICAgIENPTlZFUlNJT05fQ0hPSUNFUyA9IFsKICAgICAgICAoQ09OVkVSU0lPTl9OQVRJVkVfVVNELCAiVVNEIG5hdGl2byAvIGxlZ2FkbyIpLAogICAgICAgIChDT05WRVJTSU9OX0NPTlZFUlRFRCwgIkNvbnZlcnRpZG8gR1RR4oaSVVNEIiksCiAgICAgICAgKENPTlZFUlNJT05fTUlTU0lOR19GWCwgIlNpbiB0aXBvIGRlIGNhbWJpbyIpLAogICAgICAgIChDT05WRVJTSU9OX1NUQUxFX0ZYLCAiVEMgZGVzYWN0dWFsaXphZG8iKSwKICAgIF0KCiAgICBDVVJSRU5DWV9HVFEgPSAiR1RRIgogICAgQ1VSUkVOQ1lfVVNEID0gIlVTRCIKCiAgICBwbGFuID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgUEdDUGxhbiwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJtZXRyaWNfcmVzdWx0cyIsCiAgICApCiAgICB1bmUgPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICBVTkUsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLAogICAgICAgIHJlbGF0ZWRfbmFtZT0ibWV0cmljX3Jlc3VsdHMiLAogICAgKQogICAgbWV0cmljID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgTWV0cmljRGVmaW5pdGlvbiwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJtZXRyaWNfcmVzdWx0cyIsCiAgICApCiAgICB5ZWFyID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKCkKICAgIG1vbnRoID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKCkKICAgICMgQ2Fub25pY2FsIHZhbHVlIGZvciBzY29yaW5nL3JlcG9ydGluZzogYWx3YXlzIFVTRCBmb3IgSU5HUkVTT1MuCiAgICBtZWFzdXJlZF92YWx1ZSA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0yMCwgZGVjaW1hbF9wbGFjZXM9NiwgbnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgdGFyZ2V0X3ZhbHVlID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTE4LCBkZWNpbWFsX3BsYWNlcz0yLCBudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBpc19hY2hpZXZlZCA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1GYWxzZSkKICAgIHBvaW50c19hd2FyZGVkID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKGRlZmF1bHQ9MCkKICAgIGNhbGN1bGF0aW9uX25vdGUgPSBtb2RlbHMuVGV4dEZpZWxkKGJsYW5rPVRydWUpCgogICAgIyBGaW5hbmNpYWwgY2FwdHVyZSB0cmFpbCAobWFpbmx5IGZvciBtYW51YWwvYXV0byBJTkdSRVNPUykuCiAgICBzb3VyY2VfY3VycmVuY3kgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MywgYmxhbms9VHJ1ZSwgZGVmYXVsdD0iIikKICAgIHNvdXJjZV92YWx1ZSA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0yMCwgZGVjaW1hbF9wbGFjZXM9OCwgbnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgZXhjaGFuZ2VfcmF0ZV91c2VkID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTEyLCBkZWNpbWFsX3BsYWNlcz02LCBudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBjb252ZXJzaW9uX3N0YXR1cyA9IG1vZGVscy5DaGFyRmllbGQoCiAgICAgICAgbWF4X2xlbmd0aD0yMCwKICAgICAgICBjaG9pY2VzPUNPTlZFUlNJT05fQ0hPSUNFUywKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIGRlZmF1bHQ9IiIsCiAgICApCgogICAgY2xhc3MgTWV0YToKICAgICAgICB1bmlxdWVfdG9nZXRoZXIgPSAoInBsYW4iLCAidW5lIiwgIm1ldHJpYyIsICJ5ZWFyIiwgIm1vbnRoIikKICAgICAgICBvcmRlcmluZyA9IFsieWVhciIsICJtb250aCIsICJ1bmVfX3NvcnRfb3JkZXIiLCAibWV0cmljX19jb2RlIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiUmVzdWx0YWRvIG1lbnN1YWwgZGUgbcOpdHJpY2EiCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJSZXN1bHRhZG9zIG1lbnN1YWxlcyBkZSBtw6l0cmljYXMiCgogICAgZGVmIF9fc3RyX18oc2VsZik6CiAgICAgICAgcmV0dXJuIGYie3NlbGYueWVhcn0te3NlbGYubW9udGg6MDJkfSB7c2VsZi51bmUuY29kZX0ge3NlbGYubWV0cmljLmNvZGV9IgoKCmNsYXNzIE1vbnRobHlTY29yZWNhcmQoVGltZVN0YW1wZWRNb2RlbCk6CiAgICBwbGFuID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgUEdDUGxhbiwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJzY29yZWNhcmRzIiwKICAgICkKICAgIHVuZSA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIFVORSwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJzY29yZWNhcmRzIiwKICAgICkKICAgIHllYXIgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoKQogICAgbW9udGggPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoKQogICAgdG90YWxfcG9pbnRzID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKGRlZmF1bHQ9MCkKICAgIHF1YWxpZmllZF90aHJlc2hvbGQgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoZGVmYXVsdD04MCkKICAgIGlzX21vbnRoX3F1YWxpZmllZCA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1GYWxzZSkKICAgIHN1bW1hcnlfbm90ZSA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIHVuaXF1ZV90b2dldGhlciA9ICgicGxhbiIsICJ1bmUiLCAieWVhciIsICJtb250aCIpCiAgICAgICAgb3JkZXJpbmcgPSBbInllYXIiLCAibW9udGgiLCAidW5lX19zb3J0X29yZGVyIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiU2NvcmUgbWVuc3VhbCIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIlNjb3JlcyBtZW5zdWFsZXMiCgogICAgZGVmIF9fc3RyX18oc2VsZik6CiAgICAgICAgcmV0dXJuIGYie3NlbGYueWVhcn0te3NlbGYubW9udGg6MDJkfSB7c2VsZi51bmUuY29kZX0gKHtzZWxmLnRvdGFsX3BvaW50c30gcHRzKSIKCgpjbGFzcyBNYW51YWxSZXF1aXJlbWVudHNDb21wbGlhbmNlKFRpbWVTdGFtcGVkTW9kZWwpOgogICAgcGxhbiA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIFBHQ1BsYW4sCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLAogICAgICAgIHJlbGF0ZWRfbmFtZT0ibWFudWFsX3JlcXVpcmVtZW50cyIsCiAgICApCiAgICB1bmUgPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICBVTkUsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLAogICAgICAgIHJlbGF0ZWRfbmFtZT0ibWFudWFsX3JlcXVpcmVtZW50cyIsCiAgICApCiAgICB5ZWFyID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKCkKICAgIG1vbnRoID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKCkKICAgIGlzX2NvbXBsaWFudCA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1UcnVlKQogICAgaW5jaWRlbnRfbm90ZSA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIHVuaXF1ZV90b2dldGhlciA9ICgicGxhbiIsICJ1bmUiLCAieWVhciIsICJtb250aCIpCiAgICAgICAgb3JkZXJpbmcgPSBbInllYXIiLCAibW9udGgiLCAidW5lX19zb3J0X29yZGVyIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiQ3VtcGxpbWllbnRvIG1hbnVhbCBkZSByZXF1ZXJpbWllbnRvcyIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIkN1bXBsaW1pZW50b3MgbWFudWFsZXMgZGUgcmVxdWVyaW1pZW50b3MiCgogICAgZGVmIF9fc3RyX18oc2VsZik6CiAgICAgICAgcmV0dXJuIGYie3NlbGYueWVhcn0te3NlbGYubW9udGg6MDJkfSB7c2VsZi51bmUuY29kZX0gY3VtcGxpbWllbnRvPXtzZWxmLmlzX2NvbXBsaWFudH0iCgoKY2xhc3MgQWRtaW5NYW51YWxFZGl0TG9nKFRpbWVTdGFtcGVkTW9kZWwpOgogICAgIiIiVHJhemFiaWxpZGFkIGLDoXNpY2EgZGUgY2FtYmlvcyBtYW51YWxlcyBkZXNkZSBBZG1pbmlzdHJhY2nDs24uIiIiCgogICAgRU5USVRZX1RBUkdFVCA9ICJ0YXJnZXQiCiAgICBFTlRJVFlfUkVTVUxUID0gInJlc3VsdCIKICAgIEVOVElUWV9SRVFVSVJFTUVOVCA9ICJyZXF1aXJlbWVudCIKICAgIEVOVElUWV9GWCA9ICJmeCIKICAgIEVOVElUWV9BTElBUyA9ICJhbGlhcyIKICAgIEVOVElUWV9ORVdfQ0xJRU5UX1JPVyA9ICJuZXdfY2xpZW50X3JvdyIKICAgIEVOVElUWV9DUk9TU19TQUxFX1JPVyA9ICJjcm9zc19zYWxlX3JvdyIKICAgIEVOVElUWV9QRVJJT0RfTk9URSA9ICJwZXJpb2Rfbm90ZSIKCiAgICBFTlRJVFlfQ0hPSUNFUyA9IFsKICAgICAgICAoRU5USVRZX1RBUkdFVCwgIk1ldGEgbWVuc3VhbCIpLAogICAgICAgIChFTlRJVFlfUkVTVUxULCAiUmVzdWx0YWRvIG1lbnN1YWwiKSwKICAgICAgICAoRU5USVRZX1JFUVVJUkVNRU5ULCAiUmVxdWVyaW1pZW50byBtYW51YWwiKSwKICAgICAgICAoRU5USVRZX0ZYLCAiVGlwbyBkZSBjYW1iaW8iKSwKICAgICAgICAoRU5USVRZX0FMSUFTLCAiQWxpYXMgVU5FIiksCiAgICAgICAgKEVOVElUWV9ORVdfQ0xJRU5UX1JPVywgIkZpbGEgY2xpZW50ZSBudWV2byIpLAogICAgICAgIChFTlRJVFlfQ1JPU1NfU0FMRV9ST1csICJGaWxhIHZlbnRhIGNydXphZGEiKSwKICAgICAgICAoRU5USVRZX1BFUklPRF9OT1RFLCAiTm90YSBkZWwgcGVyw61vZG8iKSwKICAgIF0KCiAgICB5ZWFyID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKCkKICAgIG1vbnRoID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKCkKICAgIGVudGl0eV90eXBlID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTMwLCBjaG9pY2VzPUVOVElUWV9DSE9JQ0VTKQogICAgZW50aXR5X2lkID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIGZpZWxkX25hbWUgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAwKQogICAgb2xkX3ZhbHVlID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQogICAgbmV3X3ZhbHVlID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQogICAgcmVhc29uID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQogICAgZWRpdGVkX2J5ID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgc2V0dGluZ3MuQVVUSF9VU0VSX01PREVMLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJhZG1pbl9tYW51YWxfZWRpdHMiLAogICAgKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbIi1jcmVhdGVkX2F0Il0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiQml0w6Fjb3JhIGRlIGVkaWNpw7NuIG1hbnVhbCIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIkJpdMOhY29yYSBkZSBlZGljaW9uZXMgbWFudWFsZXMiCgogICAgZGVmIF9fc3RyX18oc2VsZik6CiAgICAgICAgcmV0dXJuIGYie3NlbGYueWVhcn0te3NlbGYubW9udGg6MDJkfSB7c2VsZi5lbnRpdHlfdHlwZX0ue3NlbGYuZmllbGRfbmFtZX0i
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/tests.py
PATH_JSON="pgc/tests.py"
FILENAME=tests.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=311
SIZE_BYTES_UTF8=11343
CONTENT_SHA256=8ce0f4eb430bfab315082f3cf86a2cd4af3248c4f90810b83d3b8cb8d7b60e51
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import MetricDefinition, UNE
from pgc.admin_manual import save_fx, save_results
from pgc.income_conversion import gtq_to_usd, recalc_stale_ingresos
from pgc.models import (
    MonthlyExchangeRate,
    MonthlyMetricResult,
    PGCPlan,
)


class IngresosConversionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            username="ingresos_test",
            email="t@example.com",
            password="pass",
        )
        self.year = 2026
        self.month = 5
        self.plan = PGCPlan.objects.create(year=self.year, name="Plan test")
        self.une = UNE.objects.create(
            code=UNE.CODE_FACTORING,
            name="Factoring",
            name_es="Factoraje",
            sort_order=1,
        )
        self.metric, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_INGRESOS,
            defaults={"name": "Ingresos", "is_scored": True},
        )
        for code, name in (
            (MetricDefinition.CODE_CLIENTES_NUEVOS, "Clientes"),
            (MetricDefinition.CODE_VENTA_CRUZADA, "Venta cruzada"),
            (MetricDefinition.CODE_RESPUESTA_REQS, "Reqs"),
        ):
            MetricDefinition.objects.get_or_create(
                code=code, defaults={"name": name, "is_scored": True}
            )

    def test_gtq_to_usd_math(self):
        usd = gtq_to_usd(Decimal("7850"), Decimal("7.85"))
        self.assertEqual(usd, Decimal("1000.000000"))

    def test_save_ingresos_requires_fx(self):
        with self.assertRaises(ValueError) as ctx:
            save_results(
                self.user,
                self.year,
                self.month,
                {
                    f"result_{self.une.id}_{self.metric.id}": "1000.5",
                },
                reason="prueba sin FX",
            )
        self.assertIn("Falta tipo de cambio", str(ctx.exception))
        self.assertFalse(
            MonthlyMetricResult.objects.filter(
                plan=self.plan, une=self.une, metric=self.metric
            ).exists()
        )

    def test_save_ingresos_converts_and_logs(self):
        MonthlyExchangeRate.objects.create(
            year=self.year, month=self.month, usd_to_gtq=Decimal("7.85000")
        )
        changes = save_results(
            self.user,
            self.year,
            self.month,
            {f"result_{self.une.id}_{self.metric.id}": "7850.12345678"},
            reason="captura GTQ",
        )
        self.assertEqual(changes, 1)
        row = MonthlyMetricResult.objects.get(
            plan=self.plan, une=self.une, metric=self.metric, year=self.year, month=self.month
        )
        self.assertEqual(row.source_currency, "GTQ")
        self.assertEqual(row.source_value, Decimal("7850.12345678"))
        self.assertEqual(row.exchange_rate_used, Decimal("7.85000"))
        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_CONVERTED)
        self.assertEqual(row.measured_value, gtq_to_usd(Decimal("7850.12345678"), Decimal("7.85")))

    def test_fx_change_marks_stale_and_recalc(self):
        MonthlyExchangeRate.objects.create(
            year=self.year, month=self.month, usd_to_gtq=Decimal("7.85")
        )
        save_results(
            self.user,
            self.year,
            self.month,
            {f"result_{self.une.id}_{self.metric.id}": "7850"},
            reason="inicial",
        )
        save_fx(
            self.user,
            self.year,
            self.month,
            {"fx_value": "8.00"},
            reason="ajuste TC",
        )
        row = MonthlyMetricResult.objects.get(
            plan=self.plan, une=self.une, metric=self.metric
        )
        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_STALE_FX)
        old_usd = row.measured_value

        result = recalc_stale_ingresos(
            year=self.year, month=self.month, user=self.user, reason="recalc test"
        )
        self.assertEqual(result["updated"], 1)
        row.refresh_from_db()
        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_CONVERTED)
        self.assertEqual(row.exchange_rate_used, Decimal("8.00"))
        self.assertEqual(row.measured_value, gtq_to_usd(Decimal("7850"), Decimal("8.00")))
        self.assertNotEqual(row.measured_value, old_usd)

    def test_save_ingresos_usd_native_without_fx(self):
        changes = save_results(
            self.user,
            self.year,
            self.month,
            {
                f"result_{self.une.id}_{self.metric.id}": "1500.5",
                f"ingresos_curr_{self.une.id}": "USD",
            },
            reason="captura USD",
        )
        self.assertEqual(changes, 1)
        row = MonthlyMetricResult.objects.get(
            plan=self.plan, une=self.une, metric=self.metric, year=self.year, month=self.month
        )
        self.assertEqual(row.source_currency, "USD")
        self.assertEqual(row.measured_value, Decimal("1500.5"))
        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_NATIVE_USD)
        self.assertIsNone(row.exchange_rate_used)

    def test_save_fx_range_months(self):
        changes = save_fx(
            self.user,
            self.year,
            6,
            {"fx_value_5": "7.80", "fx_value_6": "7.85"},
            reason="rango 05-06",
            month_from=5,
        )
        self.assertEqual(changes, 2)
        self.assertEqual(
            MonthlyExchangeRate.objects.get(year=self.year, month=5).usd_to_gtq,
            Decimal("7.80"),
        )
        self.assertEqual(
            MonthlyExchangeRate.objects.get(year=self.year, month=6).usd_to_gtq,
            Decimal("7.85"),
        )


class IngresosYearGridTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            username="year_grid_test",
            email="y@example.com",
            password="pass",
        )
        self.year = 2026
        self.plan = PGCPlan.objects.create(year=self.year, name="Plan year")
        self.unes = []
        for i, (code, name, name_es) in enumerate(
            (
                (UNE.CODE_FACTORING, "Factoring", "Factoraje"),
                (UNE.CODE_LEASING, "Leasing", "Leasing"),
                (UNE.CODE_INSURANCE, "Insurance", "Insurance"),
                (UNE.CODE_INVESTMENT, "Investment", "Inversiones"),
            )
        ):
            self.unes.append(
                UNE.objects.create(
                    code=code, name=name, name_es=name_es, sort_order=i + 1
                )
            )
        self.metric, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_INGRESOS,
            defaults={"name": "Ingresos", "is_scored": True},
        )

    def test_year_grid_gtq_uses_month_fx(self):
        from pgc.admin_ingresos_year import save_ingresos_year

        post = {
            "capture_currency": "GTQ",
            "fx_3": "7.85",
            f"ing_3_{self.unes[0].id}": "7850",
        }
        result = save_ingresos_year(self.user, self.year, post, reason="matriz Q")
        self.assertEqual(result["income_changes"], 1)
        self.assertEqual(result["fx_changes"], 1)
        row = MonthlyMetricResult.objects.get(
            plan=self.plan,
            une=self.unes[0],
            metric=self.metric,
            year=self.year,
            month=3,
        )
        self.assertEqual(row.source_currency, "GTQ")
        self.assertEqual(row.measured_value, gtq_to_usd(Decimal("7850"), Decimal("7.85")))

    def test_year_grid_requires_fx_for_gtq(self):
        from pgc.admin_ingresos_year import save_ingresos_year

        with self.assertRaises(ValueError) as ctx:
            save_ingresos_year(
                self.user,
                self.year,
                {
                    "capture_currency": "GTQ",
                    f"ing_4_{self.unes[1].id}": "1000",
                },
                reason="sin tc",
            )
        self.assertIn("Falta tipo de cambio", str(ctx.exception))

    def test_year_grid_usd_without_fx(self):
        from pgc.admin_ingresos_year import save_ingresos_year

        result = save_ingresos_year(
            self.user,
            self.year,
            {
                "capture_currency": "USD",
                f"ing_1_{self.unes[2].id}": "2500",
            },
            reason="matriz $",
        )
        self.assertEqual(result["income_changes"], 1)
        row = MonthlyMetricResult.objects.get(
            plan=self.plan,
            une=self.unes[2],
            metric=self.metric,
            year=self.year,
            month=1,
        )
        self.assertEqual(row.measured_value, Decimal("2500"))
        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_NATIVE_USD)


class SmartRecalcTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            username="smart_recalc",
            email="s@example.com",
            password="pass",
        )
        self.year = 2026
        self.month = 3
        self.plan = PGCPlan.objects.create(year=self.year, name="Plan smart")
        self.une = UNE.objects.create(
            code=UNE.CODE_FACTORING,
            name="Factoring",
            name_es="Factoraje",
            sort_order=1,
        )
        self.metric, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_INGRESOS,
            defaults={"name": "Ingresos", "is_scored": True},
        )
        for code, name in (
            (MetricDefinition.CODE_CLIENTES_NUEVOS, "Clientes"),
            (MetricDefinition.CODE_VENTA_CRUZADA, "VC"),
            (MetricDefinition.CODE_RESPUESTA_REQS, "Reqs"),
        ):
            MetricDefinition.objects.get_or_create(
                code=code, defaults={"name": name, "is_scored": True}
            )

    def test_stale_marks_period_pending(self):
        from pgc.admin_recalc import get_global_recalc_status, period_pending_reasons

        MonthlyExchangeRate.objects.create(
            year=self.year, month=self.month, usd_to_gtq=Decimal("7.85")
        )
        MonthlyMetricResult.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric,
            year=self.year,
            month=self.month,
            measured_value=Decimal("1000"),
            source_currency="GTQ",
            source_value=Decimal("7850"),
            exchange_rate_used=Decimal("7.85"),
            conversion_status=MonthlyMetricResult.CONVERSION_STALE_FX,
        )
        reasons = period_pending_reasons(self.year, self.month)
        self.assertTrue(any("STALE" in r for r in reasons))
        status = get_global_recalc_status()
        self.assertTrue(status["is_pending"])
        self.assertEqual(status["state"], "pending")

    def test_empty_known_periods_ready(self):
        from pgc.admin_recalc import get_global_recalc_status

        status = get_global_recalc_status()
        self.assertEqual(status["pending_count"], 0)
        self.assertTrue(status["is_ready"])

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from decimal import Decimal
00002|
00003|from django.contrib.auth import get_user_model
00004|from django.test import TestCase
00005|
00006|from core.models import MetricDefinition, UNE
00007|from pgc.admin_manual import save_fx, save_results
00008|from pgc.income_conversion import gtq_to_usd, recalc_stale_ingresos
00009|from pgc.models import (
00010|    MonthlyExchangeRate,
00011|    MonthlyMetricResult,
00012|    PGCPlan,
00013|)
00014|
00015|
00016|class IngresosConversionTests(TestCase):
00017|    def setUp(self):
00018|        User = get_user_model()
00019|        self.user = User.objects.create_superuser(
00020|            username="ingresos_test",
00021|            email="t@example.com",
00022|            password="pass",
00023|        )
00024|        self.year = 2026
00025|        self.month = 5
00026|        self.plan = PGCPlan.objects.create(year=self.year, name="Plan test")
00027|        self.une = UNE.objects.create(
00028|            code=UNE.CODE_FACTORING,
00029|            name="Factoring",
00030|            name_es="Factoraje",
00031|            sort_order=1,
00032|        )
00033|        self.metric, _ = MetricDefinition.objects.get_or_create(
00034|            code=MetricDefinition.CODE_INGRESOS,
00035|            defaults={"name": "Ingresos", "is_scored": True},
00036|        )
00037|        for code, name in (
00038|            (MetricDefinition.CODE_CLIENTES_NUEVOS, "Clientes"),
00039|            (MetricDefinition.CODE_VENTA_CRUZADA, "Venta cruzada"),
00040|            (MetricDefinition.CODE_RESPUESTA_REQS, "Reqs"),
00041|        ):
00042|            MetricDefinition.objects.get_or_create(
00043|                code=code, defaults={"name": name, "is_scored": True}
00044|            )
00045|
00046|    def test_gtq_to_usd_math(self):
00047|        usd = gtq_to_usd(Decimal("7850"), Decimal("7.85"))
00048|        self.assertEqual(usd, Decimal("1000.000000"))
00049|
00050|    def test_save_ingresos_requires_fx(self):
00051|        with self.assertRaises(ValueError) as ctx:
00052|            save_results(
00053|                self.user,
00054|                self.year,
00055|                self.month,
00056|                {
00057|                    f"result_{self.une.id}_{self.metric.id}": "1000.5",
00058|                },
00059|                reason="prueba sin FX",
00060|            )
00061|        self.assertIn("Falta tipo de cambio", str(ctx.exception))
00062|        self.assertFalse(
00063|            MonthlyMetricResult.objects.filter(
00064|                plan=self.plan, une=self.une, metric=self.metric
00065|            ).exists()
00066|        )
00067|
00068|    def test_save_ingresos_converts_and_logs(self):
00069|        MonthlyExchangeRate.objects.create(
00070|            year=self.year, month=self.month, usd_to_gtq=Decimal("7.85000")
00071|        )
00072|        changes = save_results(
00073|            self.user,
00074|            self.year,
00075|            self.month,
00076|            {f"result_{self.une.id}_{self.metric.id}": "7850.12345678"},
00077|            reason="captura GTQ",
00078|        )
00079|        self.assertEqual(changes, 1)
00080|        row = MonthlyMetricResult.objects.get(
00081|            plan=self.plan, une=self.une, metric=self.metric, year=self.year, month=self.month
00082|        )
00083|        self.assertEqual(row.source_currency, "GTQ")
00084|        self.assertEqual(row.source_value, Decimal("7850.12345678"))
00085|        self.assertEqual(row.exchange_rate_used, Decimal("7.85000"))
00086|        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_CONVERTED)
00087|        self.assertEqual(row.measured_value, gtq_to_usd(Decimal("7850.12345678"), Decimal("7.85")))
00088|
00089|    def test_fx_change_marks_stale_and_recalc(self):
00090|        MonthlyExchangeRate.objects.create(
00091|            year=self.year, month=self.month, usd_to_gtq=Decimal("7.85")
00092|        )
00093|        save_results(
00094|            self.user,
00095|            self.year,
00096|            self.month,
00097|            {f"result_{self.une.id}_{self.metric.id}": "7850"},
00098|            reason="inicial",
00099|        )
00100|        save_fx(
00101|            self.user,
00102|            self.year,
00103|            self.month,
00104|            {"fx_value": "8.00"},
00105|            reason="ajuste TC",
00106|        )
00107|        row = MonthlyMetricResult.objects.get(
00108|            plan=self.plan, une=self.une, metric=self.metric
00109|        )
00110|        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_STALE_FX)
00111|        old_usd = row.measured_value
00112|
00113|        result = recalc_stale_ingresos(
00114|            year=self.year, month=self.month, user=self.user, reason="recalc test"
00115|        )
00116|        self.assertEqual(result["updated"], 1)
00117|        row.refresh_from_db()
00118|        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_CONVERTED)
00119|        self.assertEqual(row.exchange_rate_used, Decimal("8.00"))
00120|        self.assertEqual(row.measured_value, gtq_to_usd(Decimal("7850"), Decimal("8.00")))
00121|        self.assertNotEqual(row.measured_value, old_usd)
00122|
00123|    def test_save_ingresos_usd_native_without_fx(self):
00124|        changes = save_results(
00125|            self.user,
00126|            self.year,
00127|            self.month,
00128|            {
00129|                f"result_{self.une.id}_{self.metric.id}": "1500.5",
00130|                f"ingresos_curr_{self.une.id}": "USD",
00131|            },
00132|            reason="captura USD",
00133|        )
00134|        self.assertEqual(changes, 1)
00135|        row = MonthlyMetricResult.objects.get(
00136|            plan=self.plan, une=self.une, metric=self.metric, year=self.year, month=self.month
00137|        )
00138|        self.assertEqual(row.source_currency, "USD")
00139|        self.assertEqual(row.measured_value, Decimal("1500.5"))
00140|        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_NATIVE_USD)
00141|        self.assertIsNone(row.exchange_rate_used)
00142|
00143|    def test_save_fx_range_months(self):
00144|        changes = save_fx(
00145|            self.user,
00146|            self.year,
00147|            6,
00148|            {"fx_value_5": "7.80", "fx_value_6": "7.85"},
00149|            reason="rango 05-06",
00150|            month_from=5,
00151|        )
00152|        self.assertEqual(changes, 2)
00153|        self.assertEqual(
00154|            MonthlyExchangeRate.objects.get(year=self.year, month=5).usd_to_gtq,
00155|            Decimal("7.80"),
00156|        )
00157|        self.assertEqual(
00158|            MonthlyExchangeRate.objects.get(year=self.year, month=6).usd_to_gtq,
00159|            Decimal("7.85"),
00160|        )
00161|
00162|
00163|class IngresosYearGridTests(TestCase):
00164|    def setUp(self):
00165|        User = get_user_model()
00166|        self.user = User.objects.create_superuser(
00167|            username="year_grid_test",
00168|            email="y@example.com",
00169|            password="pass",
00170|        )
00171|        self.year = 2026
00172|        self.plan = PGCPlan.objects.create(year=self.year, name="Plan year")
00173|        self.unes = []
00174|        for i, (code, name, name_es) in enumerate(
00175|            (
00176|                (UNE.CODE_FACTORING, "Factoring", "Factoraje"),
00177|                (UNE.CODE_LEASING, "Leasing", "Leasing"),
00178|                (UNE.CODE_INSURANCE, "Insurance", "Insurance"),
00179|                (UNE.CODE_INVESTMENT, "Investment", "Inversiones"),
00180|            )
00181|        ):
00182|            self.unes.append(
00183|                UNE.objects.create(
00184|                    code=code, name=name, name_es=name_es, sort_order=i + 1
00185|                )
00186|            )
00187|        self.metric, _ = MetricDefinition.objects.get_or_create(
00188|            code=MetricDefinition.CODE_INGRESOS,
00189|            defaults={"name": "Ingresos", "is_scored": True},
00190|        )
00191|
00192|    def test_year_grid_gtq_uses_month_fx(self):
00193|        from pgc.admin_ingresos_year import save_ingresos_year
00194|
00195|        post = {
00196|            "capture_currency": "GTQ",
00197|            "fx_3": "7.85",
00198|            f"ing_3_{self.unes[0].id}": "7850",
00199|        }
00200|        result = save_ingresos_year(self.user, self.year, post, reason="matriz Q")
00201|        self.assertEqual(result["income_changes"], 1)
00202|        self.assertEqual(result["fx_changes"], 1)
00203|        row = MonthlyMetricResult.objects.get(
00204|            plan=self.plan,
00205|            une=self.unes[0],
00206|            metric=self.metric,
00207|            year=self.year,
00208|            month=3,
00209|        )
00210|        self.assertEqual(row.source_currency, "GTQ")
00211|        self.assertEqual(row.measured_value, gtq_to_usd(Decimal("7850"), Decimal("7.85")))
00212|
00213|    def test_year_grid_requires_fx_for_gtq(self):
00214|        from pgc.admin_ingresos_year import save_ingresos_year
00215|
00216|        with self.assertRaises(ValueError) as ctx:
00217|            save_ingresos_year(
00218|                self.user,
00219|                self.year,
00220|                {
00221|                    "capture_currency": "GTQ",
00222|                    f"ing_4_{self.unes[1].id}": "1000",
00223|                },
00224|                reason="sin tc",
00225|            )
00226|        self.assertIn("Falta tipo de cambio", str(ctx.exception))
00227|
00228|    def test_year_grid_usd_without_fx(self):
00229|        from pgc.admin_ingresos_year import save_ingresos_year
00230|
00231|        result = save_ingresos_year(
00232|            self.user,
00233|            self.year,
00234|            {
00235|                "capture_currency": "USD",
00236|                f"ing_1_{self.unes[2].id}": "2500",
00237|            },
00238|            reason="matriz $",
00239|        )
00240|        self.assertEqual(result["income_changes"], 1)
00241|        row = MonthlyMetricResult.objects.get(
00242|            plan=self.plan,
00243|            une=self.unes[2],
00244|            metric=self.metric,
00245|            year=self.year,
00246|            month=1,
00247|        )
00248|        self.assertEqual(row.measured_value, Decimal("2500"))
00249|        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_NATIVE_USD)
00250|
00251|
00252|class SmartRecalcTests(TestCase):
00253|    def setUp(self):
00254|        User = get_user_model()
00255|        self.user = User.objects.create_superuser(
00256|            username="smart_recalc",
00257|            email="s@example.com",
00258|            password="pass",
00259|        )
00260|        self.year = 2026
00261|        self.month = 3
00262|        self.plan = PGCPlan.objects.create(year=self.year, name="Plan smart")
00263|        self.une = UNE.objects.create(
00264|            code=UNE.CODE_FACTORING,
00265|            name="Factoring",
00266|            name_es="Factoraje",
00267|            sort_order=1,
00268|        )
00269|        self.metric, _ = MetricDefinition.objects.get_or_create(
00270|            code=MetricDefinition.CODE_INGRESOS,
00271|            defaults={"name": "Ingresos", "is_scored": True},
00272|        )
00273|        for code, name in (
00274|            (MetricDefinition.CODE_CLIENTES_NUEVOS, "Clientes"),
00275|            (MetricDefinition.CODE_VENTA_CRUZADA, "VC"),
00276|            (MetricDefinition.CODE_RESPUESTA_REQS, "Reqs"),
00277|        ):
00278|            MetricDefinition.objects.get_or_create(
00279|                code=code, defaults={"name": name, "is_scored": True}
00280|            )
00281|
00282|    def test_stale_marks_period_pending(self):
00283|        from pgc.admin_recalc import get_global_recalc_status, period_pending_reasons
00284|
00285|        MonthlyExchangeRate.objects.create(
00286|            year=self.year, month=self.month, usd_to_gtq=Decimal("7.85")
00287|        )
00288|        MonthlyMetricResult.objects.create(
00289|            plan=self.plan,
00290|            une=self.une,
00291|            metric=self.metric,
00292|            year=self.year,
00293|            month=self.month,
00294|            measured_value=Decimal("1000"),
00295|            source_currency="GTQ",
00296|            source_value=Decimal("7850"),
00297|            exchange_rate_used=Decimal("7.85"),
00298|            conversion_status=MonthlyMetricResult.CONVERSION_STALE_FX,
00299|        )
00300|        reasons = period_pending_reasons(self.year, self.month)
00301|        self.assertTrue(any("STALE" in r for r in reasons))
00302|        status = get_global_recalc_status()
00303|        self.assertTrue(status["is_pending"])
00304|        self.assertEqual(status["state"], "pending")
00305|
00306|    def test_empty_known_periods_ready(self):
00307|        from pgc.admin_recalc import get_global_recalc_status
00308|
00309|        status = get_global_recalc_status()
00310|        self.assertEqual(status["pending_count"], 0)
00311|        self.assertTrue(status["is_ready"])

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsCgpmcm9tIGRqYW5nby5jb250cmliLmF1dGggaW1wb3J0IGdldF91c2VyX21vZGVsCmZyb20gZGphbmdvLnRlc3QgaW1wb3J0IFRlc3RDYXNlCgpmcm9tIGNvcmUubW9kZWxzIGltcG9ydCBNZXRyaWNEZWZpbml0aW9uLCBVTkUKZnJvbSBwZ2MuYWRtaW5fbWFudWFsIGltcG9ydCBzYXZlX2Z4LCBzYXZlX3Jlc3VsdHMKZnJvbSBwZ2MuaW5jb21lX2NvbnZlcnNpb24gaW1wb3J0IGd0cV90b191c2QsIHJlY2FsY19zdGFsZV9pbmdyZXNvcwpmcm9tIHBnYy5tb2RlbHMgaW1wb3J0ICgKICAgIE1vbnRobHlFeGNoYW5nZVJhdGUsCiAgICBNb250aGx5TWV0cmljUmVzdWx0LAogICAgUEdDUGxhbiwKKQoKCmNsYXNzIEluZ3Jlc29zQ29udmVyc2lvblRlc3RzKFRlc3RDYXNlKToKICAgIGRlZiBzZXRVcChzZWxmKToKICAgICAgICBVc2VyID0gZ2V0X3VzZXJfbW9kZWwoKQogICAgICAgIHNlbGYudXNlciA9IFVzZXIub2JqZWN0cy5jcmVhdGVfc3VwZXJ1c2VyKAogICAgICAgICAgICB1c2VybmFtZT0iaW5ncmVzb3NfdGVzdCIsCiAgICAgICAgICAgIGVtYWlsPSJ0QGV4YW1wbGUuY29tIiwKICAgICAgICAgICAgcGFzc3dvcmQ9InBhc3MiLAogICAgICAgICkKICAgICAgICBzZWxmLnllYXIgPSAyMDI2CiAgICAgICAgc2VsZi5tb250aCA9IDUKICAgICAgICBzZWxmLnBsYW4gPSBQR0NQbGFuLm9iamVjdHMuY3JlYXRlKHllYXI9c2VsZi55ZWFyLCBuYW1lPSJQbGFuIHRlc3QiKQogICAgICAgIHNlbGYudW5lID0gVU5FLm9iamVjdHMuY3JlYXRlKAogICAgICAgICAgICBjb2RlPVVORS5DT0RFX0ZBQ1RPUklORywKICAgICAgICAgICAgbmFtZT0iRmFjdG9yaW5nIiwKICAgICAgICAgICAgbmFtZV9lcz0iRmFjdG9yYWplIiwKICAgICAgICAgICAgc29ydF9vcmRlcj0xLAogICAgICAgICkKICAgICAgICBzZWxmLm1ldHJpYywgXyA9IE1ldHJpY0RlZmluaXRpb24ub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICBjb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9JTkdSRVNPUywKICAgICAgICAgICAgZGVmYXVsdHM9eyJuYW1lIjogIkluZ3Jlc29zIiwgImlzX3Njb3JlZCI6IFRydWV9LAogICAgICAgICkKICAgICAgICBmb3IgY29kZSwgbmFtZSBpbiAoCiAgICAgICAgICAgIChNZXRyaWNEZWZpbml0aW9uLkNPREVfQ0xJRU5URVNfTlVFVk9TLCAiQ2xpZW50ZXMiKSwKICAgICAgICAgICAgKE1ldHJpY0RlZmluaXRpb24uQ09ERV9WRU5UQV9DUlVaQURBLCAiVmVudGEgY3J1emFkYSIpLAogICAgICAgICAgICAoTWV0cmljRGVmaW5pdGlvbi5DT0RFX1JFU1BVRVNUQV9SRVFTLCAiUmVxcyIpLAogICAgICAgICk6CiAgICAgICAgICAgIE1ldHJpY0RlZmluaXRpb24ub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgY29kZT1jb2RlLCBkZWZhdWx0cz17Im5hbWUiOiBuYW1lLCAiaXNfc2NvcmVkIjogVHJ1ZX0KICAgICAgICAgICAgKQoKICAgIGRlZiB0ZXN0X2d0cV90b191c2RfbWF0aChzZWxmKToKICAgICAgICB1c2QgPSBndHFfdG9fdXNkKERlY2ltYWwoIjc4NTAiKSwgRGVjaW1hbCgiNy44NSIpKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwodXNkLCBEZWNpbWFsKCIxMDAwLjAwMDAwMCIpKQoKICAgIGRlZiB0ZXN0X3NhdmVfaW5ncmVzb3NfcmVxdWlyZXNfZngoc2VsZik6CiAgICAgICAgd2l0aCBzZWxmLmFzc2VydFJhaXNlcyhWYWx1ZUVycm9yKSBhcyBjdHg6CiAgICAgICAgICAgIHNhdmVfcmVzdWx0cygKICAgICAgICAgICAgICAgIHNlbGYudXNlciwKICAgICAgICAgICAgICAgIHNlbGYueWVhciwKICAgICAgICAgICAgICAgIHNlbGYubW9udGgsCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgZiJyZXN1bHRfe3NlbGYudW5lLmlkfV97c2VsZi5tZXRyaWMuaWR9IjogIjEwMDAuNSIsCiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgcmVhc29uPSJwcnVlYmEgc2luIEZYIiwKICAgICAgICAgICAgKQogICAgICAgIHNlbGYuYXNzZXJ0SW4oIkZhbHRhIHRpcG8gZGUgY2FtYmlvIiwgc3RyKGN0eC5leGNlcHRpb24pKQogICAgICAgIHNlbGYuYXNzZXJ0RmFsc2UoCiAgICAgICAgICAgIE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5maWx0ZXIoCiAgICAgICAgICAgICAgICBwbGFuPXNlbGYucGxhbiwgdW5lPXNlbGYudW5lLCBtZXRyaWM9c2VsZi5tZXRyaWMKICAgICAgICAgICAgKS5leGlzdHMoKQogICAgICAgICkKCiAgICBkZWYgdGVzdF9zYXZlX2luZ3Jlc29zX2NvbnZlcnRzX2FuZF9sb2dzKHNlbGYpOgogICAgICAgIE1vbnRobHlFeGNoYW5nZVJhdGUub2JqZWN0cy5jcmVhdGUoCiAgICAgICAgICAgIHllYXI9c2VsZi55ZWFyLCBtb250aD1zZWxmLm1vbnRoLCB1c2RfdG9fZ3RxPURlY2ltYWwoIjcuODUwMDAiKQogICAgICAgICkKICAgICAgICBjaGFuZ2VzID0gc2F2ZV9yZXN1bHRzKAogICAgICAgICAgICBzZWxmLnVzZXIsCiAgICAgICAgICAgIHNlbGYueWVhciwKICAgICAgICAgICAgc2VsZi5tb250aCwKICAgICAgICAgICAge2YicmVzdWx0X3tzZWxmLnVuZS5pZH1fe3NlbGYubWV0cmljLmlkfSI6ICI3ODUwLjEyMzQ1Njc4In0sCiAgICAgICAgICAgIHJlYXNvbj0iY2FwdHVyYSBHVFEiLAogICAgICAgICkKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKGNoYW5nZXMsIDEpCiAgICAgICAgcm93ID0gTW9udGhseU1ldHJpY1Jlc3VsdC5vYmplY3RzLmdldCgKICAgICAgICAgICAgcGxhbj1zZWxmLnBsYW4sIHVuZT1zZWxmLnVuZSwgbWV0cmljPXNlbGYubWV0cmljLCB5ZWFyPXNlbGYueWVhciwgbW9udGg9c2VsZi5tb250aAogICAgICAgICkKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKHJvdy5zb3VyY2VfY3VycmVuY3ksICJHVFEiKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwocm93LnNvdXJjZV92YWx1ZSwgRGVjaW1hbCgiNzg1MC4xMjM0NTY3OCIpKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwocm93LmV4Y2hhbmdlX3JhdGVfdXNlZCwgRGVjaW1hbCgiNy44NTAwMCIpKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwocm93LmNvbnZlcnNpb25fc3RhdHVzLCBNb250aGx5TWV0cmljUmVzdWx0LkNPTlZFUlNJT05fQ09OVkVSVEVEKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwocm93Lm1lYXN1cmVkX3ZhbHVlLCBndHFfdG9fdXNkKERlY2ltYWwoIjc4NTAuMTIzNDU2NzgiKSwgRGVjaW1hbCgiNy44NSIpKSkKCiAgICBkZWYgdGVzdF9meF9jaGFuZ2VfbWFya3Nfc3RhbGVfYW5kX3JlY2FsYyhzZWxmKToKICAgICAgICBNb250aGx5RXhjaGFuZ2VSYXRlLm9iamVjdHMuY3JlYXRlKAogICAgICAgICAgICB5ZWFyPXNlbGYueWVhciwgbW9udGg9c2VsZi5tb250aCwgdXNkX3RvX2d0cT1EZWNpbWFsKCI3Ljg1IikKICAgICAgICApCiAgICAgICAgc2F2ZV9yZXN1bHRzKAogICAgICAgICAgICBzZWxmLnVzZXIsCiAgICAgICAgICAgIHNlbGYueWVhciwKICAgICAgICAgICAgc2VsZi5tb250aCwKICAgICAgICAgICAge2YicmVzdWx0X3tzZWxmLnVuZS5pZH1fe3NlbGYubWV0cmljLmlkfSI6ICI3ODUwIn0sCiAgICAgICAgICAgIHJlYXNvbj0iaW5pY2lhbCIsCiAgICAgICAgKQogICAgICAgIHNhdmVfZngoCiAgICAgICAgICAgIHNlbGYudXNlciwKICAgICAgICAgICAgc2VsZi55ZWFyLAogICAgICAgICAgICBzZWxmLm1vbnRoLAogICAgICAgICAgICB7ImZ4X3ZhbHVlIjogIjguMDAifSwKICAgICAgICAgICAgcmVhc29uPSJhanVzdGUgVEMiLAogICAgICAgICkKICAgICAgICByb3cgPSBNb250aGx5TWV0cmljUmVzdWx0Lm9iamVjdHMuZ2V0KAogICAgICAgICAgICBwbGFuPXNlbGYucGxhbiwgdW5lPXNlbGYudW5lLCBtZXRyaWM9c2VsZi5tZXRyaWMKICAgICAgICApCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChyb3cuY29udmVyc2lvbl9zdGF0dXMsIE1vbnRobHlNZXRyaWNSZXN1bHQuQ09OVkVSU0lPTl9TVEFMRV9GWCkKICAgICAgICBvbGRfdXNkID0gcm93Lm1lYXN1cmVkX3ZhbHVlCgogICAgICAgIHJlc3VsdCA9IHJlY2FsY19zdGFsZV9pbmdyZXNvcygKICAgICAgICAgICAgeWVhcj1zZWxmLnllYXIsIG1vbnRoPXNlbGYubW9udGgsIHVzZXI9c2VsZi51c2VyLCByZWFzb249InJlY2FsYyB0ZXN0IgogICAgICAgICkKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKHJlc3VsdFsidXBkYXRlZCJdLCAxKQogICAgICAgIHJvdy5yZWZyZXNoX2Zyb21fZGIoKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwocm93LmNvbnZlcnNpb25fc3RhdHVzLCBNb250aGx5TWV0cmljUmVzdWx0LkNPTlZFUlNJT05fQ09OVkVSVEVEKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwocm93LmV4Y2hhbmdlX3JhdGVfdXNlZCwgRGVjaW1hbCgiOC4wMCIpKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwocm93Lm1lYXN1cmVkX3ZhbHVlLCBndHFfdG9fdXNkKERlY2ltYWwoIjc4NTAiKSwgRGVjaW1hbCgiOC4wMCIpKSkKICAgICAgICBzZWxmLmFzc2VydE5vdEVxdWFsKHJvdy5tZWFzdXJlZF92YWx1ZSwgb2xkX3VzZCkKCiAgICBkZWYgdGVzdF9zYXZlX2luZ3Jlc29zX3VzZF9uYXRpdmVfd2l0aG91dF9meChzZWxmKToKICAgICAgICBjaGFuZ2VzID0gc2F2ZV9yZXN1bHRzKAogICAgICAgICAgICBzZWxmLnVzZXIsCiAgICAgICAgICAgIHNlbGYueWVhciwKICAgICAgICAgICAgc2VsZi5tb250aCwKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgZiJyZXN1bHRfe3NlbGYudW5lLmlkfV97c2VsZi5tZXRyaWMuaWR9IjogIjE1MDAuNSIsCiAgICAgICAgICAgICAgICBmImluZ3Jlc29zX2N1cnJfe3NlbGYudW5lLmlkfSI6ICJVU0QiLAogICAgICAgICAgICB9LAogICAgICAgICAgICByZWFzb249ImNhcHR1cmEgVVNEIiwKICAgICAgICApCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChjaGFuZ2VzLCAxKQogICAgICAgIHJvdyA9IE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5nZXQoCiAgICAgICAgICAgIHBsYW49c2VsZi5wbGFuLCB1bmU9c2VsZi51bmUsIG1ldHJpYz1zZWxmLm1ldHJpYywgeWVhcj1zZWxmLnllYXIsIG1vbnRoPXNlbGYubW9udGgKICAgICAgICApCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChyb3cuc291cmNlX2N1cnJlbmN5LCAiVVNEIikKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKHJvdy5tZWFzdXJlZF92YWx1ZSwgRGVjaW1hbCgiMTUwMC41IikpCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChyb3cuY29udmVyc2lvbl9zdGF0dXMsIE1vbnRobHlNZXRyaWNSZXN1bHQuQ09OVkVSU0lPTl9OQVRJVkVfVVNEKQogICAgICAgIHNlbGYuYXNzZXJ0SXNOb25lKHJvdy5leGNoYW5nZV9yYXRlX3VzZWQpCgogICAgZGVmIHRlc3Rfc2F2ZV9meF9yYW5nZV9tb250aHMoc2VsZik6CiAgICAgICAgY2hhbmdlcyA9IHNhdmVfZngoCiAgICAgICAgICAgIHNlbGYudXNlciwKICAgICAgICAgICAgc2VsZi55ZWFyLAogICAgICAgICAgICA2LAogICAgICAgICAgICB7ImZ4X3ZhbHVlXzUiOiAiNy44MCIsICJmeF92YWx1ZV82IjogIjcuODUifSwKICAgICAgICAgICAgcmVhc29uPSJyYW5nbyAwNS0wNiIsCiAgICAgICAgICAgIG1vbnRoX2Zyb209NSwKICAgICAgICApCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChjaGFuZ2VzLCAyKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwoCiAgICAgICAgICAgIE1vbnRobHlFeGNoYW5nZVJhdGUub2JqZWN0cy5nZXQoeWVhcj1zZWxmLnllYXIsIG1vbnRoPTUpLnVzZF90b19ndHEsCiAgICAgICAgICAgIERlY2ltYWwoIjcuODAiKSwKICAgICAgICApCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbCgKICAgICAgICAgICAgTW9udGhseUV4Y2hhbmdlUmF0ZS5vYmplY3RzLmdldCh5ZWFyPXNlbGYueWVhciwgbW9udGg9NikudXNkX3RvX2d0cSwKICAgICAgICAgICAgRGVjaW1hbCgiNy44NSIpLAogICAgICAgICkKCgpjbGFzcyBJbmdyZXNvc1llYXJHcmlkVGVzdHMoVGVzdENhc2UpOgogICAgZGVmIHNldFVwKHNlbGYpOgogICAgICAgIFVzZXIgPSBnZXRfdXNlcl9tb2RlbCgpCiAgICAgICAgc2VsZi51c2VyID0gVXNlci5vYmplY3RzLmNyZWF0ZV9zdXBlcnVzZXIoCiAgICAgICAgICAgIHVzZXJuYW1lPSJ5ZWFyX2dyaWRfdGVzdCIsCiAgICAgICAgICAgIGVtYWlsPSJ5QGV4YW1wbGUuY29tIiwKICAgICAgICAgICAgcGFzc3dvcmQ9InBhc3MiLAogICAgICAgICkKICAgICAgICBzZWxmLnllYXIgPSAyMDI2CiAgICAgICAgc2VsZi5wbGFuID0gUEdDUGxhbi5vYmplY3RzLmNyZWF0ZSh5ZWFyPXNlbGYueWVhciwgbmFtZT0iUGxhbiB5ZWFyIikKICAgICAgICBzZWxmLnVuZXMgPSBbXQogICAgICAgIGZvciBpLCAoY29kZSwgbmFtZSwgbmFtZV9lcykgaW4gZW51bWVyYXRlKAogICAgICAgICAgICAoCiAgICAgICAgICAgICAgICAoVU5FLkNPREVfRkFDVE9SSU5HLCAiRmFjdG9yaW5nIiwgIkZhY3RvcmFqZSIpLAogICAgICAgICAgICAgICAgKFVORS5DT0RFX0xFQVNJTkcsICJMZWFzaW5nIiwgIkxlYXNpbmciKSwKICAgICAgICAgICAgICAgIChVTkUuQ09ERV9JTlNVUkFOQ0UsICJJbnN1cmFuY2UiLCAiSW5zdXJhbmNlIiksCiAgICAgICAgICAgICAgICAoVU5FLkNPREVfSU5WRVNUTUVOVCwgIkludmVzdG1lbnQiLCAiSW52ZXJzaW9uZXMiKSwKICAgICAgICAgICAgKQogICAgICAgICk6CiAgICAgICAgICAgIHNlbGYudW5lcy5hcHBlbmQoCiAgICAgICAgICAgICAgICBVTkUub2JqZWN0cy5jcmVhdGUoCiAgICAgICAgICAgICAgICAgICAgY29kZT1jb2RlLCBuYW1lPW5hbWUsIG5hbWVfZXM9bmFtZV9lcywgc29ydF9vcmRlcj1pICsgMQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICApCiAgICAgICAgc2VsZi5tZXRyaWMsIF8gPSBNZXRyaWNEZWZpbml0aW9uLm9iamVjdHMuZ2V0X29yX2NyZWF0ZSgKICAgICAgICAgICAgY29kZT1NZXRyaWNEZWZpbml0aW9uLkNPREVfSU5HUkVTT1MsCiAgICAgICAgICAgIGRlZmF1bHRzPXsibmFtZSI6ICJJbmdyZXNvcyIsICJpc19zY29yZWQiOiBUcnVlfSwKICAgICAgICApCgogICAgZGVmIHRlc3RfeWVhcl9ncmlkX2d0cV91c2VzX21vbnRoX2Z4KHNlbGYpOgogICAgICAgIGZyb20gcGdjLmFkbWluX2luZ3Jlc29zX3llYXIgaW1wb3J0IHNhdmVfaW5ncmVzb3NfeWVhcgoKICAgICAgICBwb3N0ID0gewogICAgICAgICAgICAiY2FwdHVyZV9jdXJyZW5jeSI6ICJHVFEiLAogICAgICAgICAgICAiZnhfMyI6ICI3Ljg1IiwKICAgICAgICAgICAgZiJpbmdfM197c2VsZi51bmVzWzBdLmlkfSI6ICI3ODUwIiwKICAgICAgICB9CiAgICAgICAgcmVzdWx0ID0gc2F2ZV9pbmdyZXNvc195ZWFyKHNlbGYudXNlciwgc2VsZi55ZWFyLCBwb3N0LCByZWFzb249Im1hdHJpeiBRIikKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKHJlc3VsdFsiaW5jb21lX2NoYW5nZXMiXSwgMSkKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKHJlc3VsdFsiZnhfY2hhbmdlcyJdLCAxKQogICAgICAgIHJvdyA9IE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5nZXQoCiAgICAgICAgICAgIHBsYW49c2VsZi5wbGFuLAogICAgICAgICAgICB1bmU9c2VsZi51bmVzWzBdLAogICAgICAgICAgICBtZXRyaWM9c2VsZi5tZXRyaWMsCiAgICAgICAgICAgIHllYXI9c2VsZi55ZWFyLAogICAgICAgICAgICBtb250aD0zLAogICAgICAgICkKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKHJvdy5zb3VyY2VfY3VycmVuY3ksICJHVFEiKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwocm93Lm1lYXN1cmVkX3ZhbHVlLCBndHFfdG9fdXNkKERlY2ltYWwoIjc4NTAiKSwgRGVjaW1hbCgiNy44NSIpKSkKCiAgICBkZWYgdGVzdF95ZWFyX2dyaWRfcmVxdWlyZXNfZnhfZm9yX2d0cShzZWxmKToKICAgICAgICBmcm9tIHBnYy5hZG1pbl9pbmdyZXNvc195ZWFyIGltcG9ydCBzYXZlX2luZ3Jlc29zX3llYXIKCiAgICAgICAgd2l0aCBzZWxmLmFzc2VydFJhaXNlcyhWYWx1ZUVycm9yKSBhcyBjdHg6CiAgICAgICAgICAgIHNhdmVfaW5ncmVzb3NfeWVhcigKICAgICAgICAgICAgICAgIHNlbGYudXNlciwKICAgICAgICAgICAgICAgIHNlbGYueWVhciwKICAgICAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICAgICAiY2FwdHVyZV9jdXJyZW5jeSI6ICJHVFEiLAogICAgICAgICAgICAgICAgICAgIGYiaW5nXzRfe3NlbGYudW5lc1sxXS5pZH0iOiAiMTAwMCIsCiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgcmVhc29uPSJzaW4gdGMiLAogICAgICAgICAgICApCiAgICAgICAgc2VsZi5hc3NlcnRJbigiRmFsdGEgdGlwbyBkZSBjYW1iaW8iLCBzdHIoY3R4LmV4Y2VwdGlvbikpCgogICAgZGVmIHRlc3RfeWVhcl9ncmlkX3VzZF93aXRob3V0X2Z4KHNlbGYpOgogICAgICAgIGZyb20gcGdjLmFkbWluX2luZ3Jlc29zX3llYXIgaW1wb3J0IHNhdmVfaW5ncmVzb3NfeWVhcgoKICAgICAgICByZXN1bHQgPSBzYXZlX2luZ3Jlc29zX3llYXIoCiAgICAgICAgICAgIHNlbGYudXNlciwKICAgICAgICAgICAgc2VsZi55ZWFyLAogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAiY2FwdHVyZV9jdXJyZW5jeSI6ICJVU0QiLAogICAgICAgICAgICAgICAgZiJpbmdfMV97c2VsZi51bmVzWzJdLmlkfSI6ICIyNTAwIiwKICAgICAgICAgICAgfSwKICAgICAgICAgICAgcmVhc29uPSJtYXRyaXogJCIsCiAgICAgICAgKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwocmVzdWx0WyJpbmNvbWVfY2hhbmdlcyJdLCAxKQogICAgICAgIHJvdyA9IE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5nZXQoCiAgICAgICAgICAgIHBsYW49c2VsZi5wbGFuLAogICAgICAgICAgICB1bmU9c2VsZi51bmVzWzJdLAogICAgICAgICAgICBtZXRyaWM9c2VsZi5tZXRyaWMsCiAgICAgICAgICAgIHllYXI9c2VsZi55ZWFyLAogICAgICAgICAgICBtb250aD0xLAogICAgICAgICkKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKHJvdy5tZWFzdXJlZF92YWx1ZSwgRGVjaW1hbCgiMjUwMCIpKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwocm93LmNvbnZlcnNpb25fc3RhdHVzLCBNb250aGx5TWV0cmljUmVzdWx0LkNPTlZFUlNJT05fTkFUSVZFX1VTRCkKCgpjbGFzcyBTbWFydFJlY2FsY1Rlc3RzKFRlc3RDYXNlKToKICAgIGRlZiBzZXRVcChzZWxmKToKICAgICAgICBVc2VyID0gZ2V0X3VzZXJfbW9kZWwoKQogICAgICAgIHNlbGYudXNlciA9IFVzZXIub2JqZWN0cy5jcmVhdGVfc3VwZXJ1c2VyKAogICAgICAgICAgICB1c2VybmFtZT0ic21hcnRfcmVjYWxjIiwKICAgICAgICAgICAgZW1haWw9InNAZXhhbXBsZS5jb20iLAogICAgICAgICAgICBwYXNzd29yZD0icGFzcyIsCiAgICAgICAgKQogICAgICAgIHNlbGYueWVhciA9IDIwMjYKICAgICAgICBzZWxmLm1vbnRoID0gMwogICAgICAgIHNlbGYucGxhbiA9IFBHQ1BsYW4ub2JqZWN0cy5jcmVhdGUoeWVhcj1zZWxmLnllYXIsIG5hbWU9IlBsYW4gc21hcnQiKQogICAgICAgIHNlbGYudW5lID0gVU5FLm9iamVjdHMuY3JlYXRlKAogICAgICAgICAgICBjb2RlPVVORS5DT0RFX0ZBQ1RPUklORywKICAgICAgICAgICAgbmFtZT0iRmFjdG9yaW5nIiwKICAgICAgICAgICAgbmFtZV9lcz0iRmFjdG9yYWplIiwKICAgICAgICAgICAgc29ydF9vcmRlcj0xLAogICAgICAgICkKICAgICAgICBzZWxmLm1ldHJpYywgXyA9IE1ldHJpY0RlZmluaXRpb24ub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICBjb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9JTkdSRVNPUywKICAgICAgICAgICAgZGVmYXVsdHM9eyJuYW1lIjogIkluZ3Jlc29zIiwgImlzX3Njb3JlZCI6IFRydWV9LAogICAgICAgICkKICAgICAgICBmb3IgY29kZSwgbmFtZSBpbiAoCiAgICAgICAgICAgIChNZXRyaWNEZWZpbml0aW9uLkNPREVfQ0xJRU5URVNfTlVFVk9TLCAiQ2xpZW50ZXMiKSwKICAgICAgICAgICAgKE1ldHJpY0RlZmluaXRpb24uQ09ERV9WRU5UQV9DUlVaQURBLCAiVkMiKSwKICAgICAgICAgICAgKE1ldHJpY0RlZmluaXRpb24uQ09ERV9SRVNQVUVTVEFfUkVRUywgIlJlcXMiKSwKICAgICAgICApOgogICAgICAgICAgICBNZXRyaWNEZWZpbml0aW9uLm9iamVjdHMuZ2V0X29yX2NyZWF0ZSgKICAgICAgICAgICAgICAgIGNvZGU9Y29kZSwgZGVmYXVsdHM9eyJuYW1lIjogbmFtZSwgImlzX3Njb3JlZCI6IFRydWV9CiAgICAgICAgICAgICkKCiAgICBkZWYgdGVzdF9zdGFsZV9tYXJrc19wZXJpb2RfcGVuZGluZyhzZWxmKToKICAgICAgICBmcm9tIHBnYy5hZG1pbl9yZWNhbGMgaW1wb3J0IGdldF9nbG9iYWxfcmVjYWxjX3N0YXR1cywgcGVyaW9kX3BlbmRpbmdfcmVhc29ucwoKICAgICAgICBNb250aGx5RXhjaGFuZ2VSYXRlLm9iamVjdHMuY3JlYXRlKAogICAgICAgICAgICB5ZWFyPXNlbGYueWVhciwgbW9udGg9c2VsZi5tb250aCwgdXNkX3RvX2d0cT1EZWNpbWFsKCI3Ljg1IikKICAgICAgICApCiAgICAgICAgTW9udGhseU1ldHJpY1Jlc3VsdC5vYmplY3RzLmNyZWF0ZSgKICAgICAgICAgICAgcGxhbj1zZWxmLnBsYW4sCiAgICAgICAgICAgIHVuZT1zZWxmLnVuZSwKICAgICAgICAgICAgbWV0cmljPXNlbGYubWV0cmljLAogICAgICAgICAgICB5ZWFyPXNlbGYueWVhciwKICAgICAgICAgICAgbW9udGg9c2VsZi5tb250aCwKICAgICAgICAgICAgbWVhc3VyZWRfdmFsdWU9RGVjaW1hbCgiMTAwMCIpLAogICAgICAgICAgICBzb3VyY2VfY3VycmVuY3k9IkdUUSIsCiAgICAgICAgICAgIHNvdXJjZV92YWx1ZT1EZWNpbWFsKCI3ODUwIiksCiAgICAgICAgICAgIGV4Y2hhbmdlX3JhdGVfdXNlZD1EZWNpbWFsKCI3Ljg1IiksCiAgICAgICAgICAgIGNvbnZlcnNpb25fc3RhdHVzPU1vbnRobHlNZXRyaWNSZXN1bHQuQ09OVkVSU0lPTl9TVEFMRV9GWCwKICAgICAgICApCiAgICAgICAgcmVhc29ucyA9IHBlcmlvZF9wZW5kaW5nX3JlYXNvbnMoc2VsZi55ZWFyLCBzZWxmLm1vbnRoKQogICAgICAgIHNlbGYuYXNzZXJ0VHJ1ZShhbnkoIlNUQUxFIiBpbiByIGZvciByIGluIHJlYXNvbnMpKQogICAgICAgIHN0YXR1cyA9IGdldF9nbG9iYWxfcmVjYWxjX3N0YXR1cygpCiAgICAgICAgc2VsZi5hc3NlcnRUcnVlKHN0YXR1c1siaXNfcGVuZGluZyJdKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwoc3RhdHVzWyJzdGF0ZSJdLCAicGVuZGluZyIpCgogICAgZGVmIHRlc3RfZW1wdHlfa25vd25fcGVyaW9kc19yZWFkeShzZWxmKToKICAgICAgICBmcm9tIHBnYy5hZG1pbl9yZWNhbGMgaW1wb3J0IGdldF9nbG9iYWxfcmVjYWxjX3N0YXR1cwoKICAgICAgICBzdGF0dXMgPSBnZXRfZ2xvYmFsX3JlY2FsY19zdGF0dXMoKQogICAgICAgIHNlbGYuYXNzZXJ0RXF1YWwoc3RhdHVzWyJwZW5kaW5nX2NvdW50Il0sIDApCiAgICAgICAgc2VsZi5hc3NlcnRUcnVlKHN0YXR1c1siaXNfcmVhZHkiXSkK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/tv_charts.py
PATH_JSON="pgc/tv_charts.py"
FILENAME=tv_charts.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=357
SIZE_BYTES_UTF8=11537
CONTENT_SHA256=3bd7c16efb548942d1bc0124e5fd6d6fdcaf4a4e91e384debd2b3b619ea3caf3
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""
Charts TV: archivo archivados con sello + copias vivas wcg-g1..g4.png.

Layout en disco (MEDIA_ROOT/tv):
  media/tv/archive/wcg-g1 YY-MM HH-MM.png
  media/tv/live/wcg-g1.png … wcg-g4.png

URL pública (televisor):
  /tv/wcg-g1.png … /tv/wcg-g4.png
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from pgc.admin_utils import admin_period_context, parse_admin_period

LIVE_SLOT_COUNT = 4
LIVE_NAMES = {n: f"wcg-g{n}.png" for n in range(1, LIVE_SLOT_COUNT + 1)}
# Soporta sello nuevo YY-MM-DD HH-MM y legado YY-MM HH-MM
ARCHIVE_NAME_RE = re.compile(
    r"^wcg-g([1-4]) (\d{2}-\d{2}(?:-\d{2})? \d{2}-\d{2})\.png$"
)


def tv_root() -> Path:
    root = Path(settings.MEDIA_ROOT) / "tv"
    (root / "archive").mkdir(parents=True, exist_ok=True)
    (root / "live").mkdir(parents=True, exist_ok=True)
    return root


def archive_dir() -> Path:
    return tv_root() / "archive"


def live_dir() -> Path:
    return tv_root() / "live"


def live_path(slot: int) -> Path:
    if slot not in LIVE_NAMES:
        raise ValueError(f"slot inválido: {slot}")
    return live_dir() / LIVE_NAMES[slot]


def parse_archive_name(name: str) -> tuple[int, str] | None:
    match = ARCHIVE_NAME_RE.match(name)
    if not match:
        return None
    return int(match.group(1)), match.group(2)


def is_safe_archive_name(name: str) -> bool:
    return parse_archive_name(name) is not None


@dataclass
class ArchiveFile:
    name: str
    slot: int
    stamp: str
    size: int
    mtime: float


@dataclass
class ArchiveSet:
    stamp: str
    files: dict[int, ArchiveFile]

    @property
    def complete(self) -> bool:
        return all(n in self.files for n in range(1, LIVE_SLOT_COUNT + 1))

    @property
    def slots_present(self) -> list[int]:
        return sorted(self.files)


def list_archive_files() -> list[ArchiveFile]:
    items: list[ArchiveFile] = []
    for path in sorted(archive_dir().glob("wcg-g*.png"), key=lambda p: p.stat().st_mtime, reverse=True):
        parsed = parse_archive_name(path.name)
        if not parsed:
            continue
        slot, stamp = parsed
        st = path.stat()
        items.append(
            ArchiveFile(
                name=path.name,
                slot=slot,
                stamp=stamp,
                size=st.st_size,
                mtime=st.st_mtime,
            )
        )
    return items


def group_archive_sets(files: list[ArchiveFile] | None = None) -> list[ArchiveSet]:
    files = files if files is not None else list_archive_files()
    by_stamp: dict[str, dict[int, ArchiveFile]] = {}
    order: list[str] = []
    for item in files:
        if item.stamp not in by_stamp:
            by_stamp[item.stamp] = {}
            order.append(item.stamp)
        by_stamp[item.stamp][item.slot] = item
    return [ArchiveSet(stamp=stamp, files=by_stamp[stamp]) for stamp in order]


def live_status() -> list[dict]:
    rows = []
    for slot, name in LIVE_NAMES.items():
        path = live_path(slot)
        rows.append(
            {
                "slot": slot,
                "name": name,
                "exists": path.is_file(),
                "size": path.stat().st_size if path.is_file() else 0,
                "url": f"/tv/{name}",
            }
        )
    return rows


def save_archive_upload(filename: str, raw: bytes, *, activate_live: bool = True) -> dict:
    """
    Guarda PNG con sello en archive/.
    Si activate_live=True, también copia/actualiza media/tv/live/wcg-gN.png.
    """
    parsed = parse_archive_name(filename)
    if not parsed:
        raise ValueError(
            "Nombre inválido. Use: wcg-gN YY-MM HH-MM.png (N=1..4; también acepta YY-MM-DD)."
        )
    slot, stamp = parsed
    dest = archive_dir() / filename
    dest.write_bytes(raw)
    live_name = None
    if activate_live:
        live_dest = live_path(slot)
        live_dest.write_bytes(raw)
        live_name = LIVE_NAMES[slot]
    return {
        "filename": filename,
        "slot": slot,
        "stamp": stamp,
        "live": live_name,
    }


def promote_latest_complete_set() -> list[str] | None:
    """Si hay un set g1–g4 completo, copia el más reciente a live. None si no hay."""
    for aset in group_archive_sets():
        if aset.complete:
            names = [aset.files[n].name for n in range(1, LIVE_SLOT_COUNT + 1)]
            return copy_archives_to_live(names)
    return None


def copy_archives_to_live(filenames: list[str]) -> list[str]:
    """Copia archivos de archive → live (sobrescribe). No borra el archivo con sello."""
    copied: list[str] = []
    seen_slots: set[int] = set()
    for name in filenames:
        parsed = parse_archive_name(name)
        if not parsed:
            raise ValueError(f"Nombre no permitido: {name}")
        slot, _stamp = parsed
        src = archive_dir() / name
        if not src.is_file():
            raise FileNotFoundError(f"No existe en archivo: {name}")
        if slot in seen_slots:
            raise ValueError(f"Seleccionó más de un archivo para wcg-g{slot}.")
        seen_slots.add(slot)
        dest = live_path(slot)
        shutil.copy2(src, dest)
        copied.append(LIVE_NAMES[slot])
    return copied


def delete_archives(filenames: list[str]) -> list[str]:
    deleted: list[str] = []
    for name in filenames:
        if not is_safe_archive_name(name):
            raise ValueError(f"Nombre no permitido: {name}")
        path = archive_dir() / name
        if path.is_file():
            path.unlink()
            deleted.append(name)
    return deleted


def _superuser(user) -> bool:
    return bool(user.is_superuser)


@require_GET
def tv_live_png(request, name: str):
    """Sirve wcg-g1.png … wcg-g4.png sin autenticación (TV)."""
    if name not in LIVE_NAMES.values():
        raise Http404("Archivo TV no encontrado.")
    path = live_dir() / name
    if not path.is_file():
        raise Http404("Aún no hay chart vivo para ese slot.")
    response = FileResponse(path.open("rb"), content_type="image/png")
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    return response


@login_required
@user_passes_test(_superuser)
@require_GET
def tv_archive_png(request, name: str):
    if not is_safe_archive_name(name):
        raise Http404("Nombre inválido.")
    path = archive_dir() / name
    if not path.is_file():
        raise Http404("Archivo no encontrado.")
    return FileResponse(path.open("rb"), content_type="image/png")


@login_required
@require_POST
def tv_charts_upload(request):
    """Recibe PNG desde Exportación 4 charts → archive/ + live/."""
    uploaded = request.FILES.get("file") or request.FILES.get("png")
    if not uploaded:
        return JsonResponse({"ok": False, "error": "Falta archivo."}, status=400)
    filename = (uploaded.name or "").strip()
    # Algunos navegadores envían solo el basename; normalizar espacios.
    filename = Path(filename).name
    activate = (request.POST.get("activate") or "1").strip() != "0"
    try:
        result = save_archive_upload(filename, uploaded.read(), activate_live=activate)
    except ValueError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=400)
    except OSError as exc:
        return JsonResponse(
            {"ok": False, "error": f"No se pudo escribir en media/tv/: {exc}"},
            status=500,
        )
    return JsonResponse({"ok": True, **result})


@login_required
@user_passes_test(_superuser)
def admin_tv_charts(request):
    period = parse_admin_period(request)

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()
        selected = [n.strip() for n in request.POST.getlist("files") if n.strip()]

        if action == "promote":
            if not selected:
                messages.error(request, "Seleccione al menos un archivo con sello.")
            else:
                try:
                    copied = copy_archives_to_live(selected)
                    messages.success(
                        request,
                        "Copiado a TV (vivos): " + ", ".join(copied) + ".",
                    )
                except (ValueError, FileNotFoundError) as exc:
                    messages.error(request, str(exc))
            return redirect("pgc:admin_tv_charts")

        if action == "delete":
            if not selected:
                messages.error(request, "Seleccione archivos archivados para borrar.")
            else:
                try:
                    deleted = delete_archives(selected)
                    if deleted:
                        messages.success(
                            request,
                            f"Borrados {len(deleted)} archivo(s) archivado(s).",
                        )
                    else:
                        messages.info(request, "Nada que borrar.")
                except ValueError as exc:
                    messages.error(request, str(exc))
            return redirect("pgc:admin_tv_charts")

        if action == "promote_stamp":
            stamp = (request.POST.get("stamp") or "").strip()
            sets = {s.stamp: s for s in group_archive_sets()}
            aset = sets.get(stamp)
            if not aset or not aset.complete:
                messages.error(
                    request,
                    "Ese sello no tiene los 4 PNG (g1–g4). Seleccione un set completo.",
                )
            else:
                names = [aset.files[n].name for n in range(1, LIVE_SLOT_COUNT + 1)]
                try:
                    copied = copy_archives_to_live(names)
                    messages.success(
                        request,
                        f"Set «{stamp}» copiado a TV: " + ", ".join(copied) + ".",
                    )
                except (ValueError, FileNotFoundError) as exc:
                    messages.error(request, str(exc))
            return redirect("pgc:admin_tv_charts")

        messages.error(request, "Acción no reconocida.")
        return redirect("pgc:admin_tv_charts")

    archive_sets = []
    for aset in group_archive_sets():
        slots = []
        for n in range(1, LIVE_SLOT_COUNT + 1):
            f = aset.files.get(n)
            slots.append(
                {
                    "slot": n,
                    "file": f,
                    "name": f.name if f else None,
                    "preview_url": (
                        reverse("pgc:tv_archive_png", kwargs={"name": f.name})
                        if f
                        else None
                    ),
                }
            )
        archive_sets.append(
            {
                "stamp": aset.stamp,
                "complete": aset.complete,
                "slots": slots,
            }
        )

    context = {
        **admin_period_context(period),
        "live_slots": live_status(),
        "live_all_empty": not any(s["exists"] for s in live_status()),
        "archive_sets": archive_sets,
        "supports_month_range": False,
    }
    return render(request, "pgc/admin_tv_charts.html", context)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Charts TV: archivo archivados con sello + copias vivas wcg-g1..g4.png.
00003|
00004|Layout en disco (MEDIA_ROOT/tv):
00005|  media/tv/archive/wcg-g1 YY-MM HH-MM.png
00006|  media/tv/live/wcg-g1.png … wcg-g4.png
00007|
00008|URL pública (televisor):
00009|  /tv/wcg-g1.png … /tv/wcg-g4.png
00010|"""
00011|
00012|from __future__ import annotations
00013|
00014|import re
00015|import shutil
00016|from dataclasses import dataclass
00017|from pathlib import Path
00018|
00019|from django.conf import settings
00020|from django.contrib import messages
00021|from django.contrib.auth.decorators import login_required, user_passes_test
00022|from django.http import FileResponse, Http404, JsonResponse
00023|from django.shortcuts import redirect, render
00024|from django.urls import reverse
00025|from django.views.decorators.http import require_GET, require_POST
00026|
00027|from pgc.admin_utils import admin_period_context, parse_admin_period
00028|
00029|LIVE_SLOT_COUNT = 4
00030|LIVE_NAMES = {n: f"wcg-g{n}.png" for n in range(1, LIVE_SLOT_COUNT + 1)}
00031|# Soporta sello nuevo YY-MM-DD HH-MM y legado YY-MM HH-MM
00032|ARCHIVE_NAME_RE = re.compile(
00033|    r"^wcg-g([1-4]) (\d{2}-\d{2}(?:-\d{2})? \d{2}-\d{2})\.png$"
00034|)
00035|
00036|
00037|def tv_root() -> Path:
00038|    root = Path(settings.MEDIA_ROOT) / "tv"
00039|    (root / "archive").mkdir(parents=True, exist_ok=True)
00040|    (root / "live").mkdir(parents=True, exist_ok=True)
00041|    return root
00042|
00043|
00044|def archive_dir() -> Path:
00045|    return tv_root() / "archive"
00046|
00047|
00048|def live_dir() -> Path:
00049|    return tv_root() / "live"
00050|
00051|
00052|def live_path(slot: int) -> Path:
00053|    if slot not in LIVE_NAMES:
00054|        raise ValueError(f"slot inválido: {slot}")
00055|    return live_dir() / LIVE_NAMES[slot]
00056|
00057|
00058|def parse_archive_name(name: str) -> tuple[int, str] | None:
00059|    match = ARCHIVE_NAME_RE.match(name)
00060|    if not match:
00061|        return None
00062|    return int(match.group(1)), match.group(2)
00063|
00064|
00065|def is_safe_archive_name(name: str) -> bool:
00066|    return parse_archive_name(name) is not None
00067|
00068|
00069|@dataclass
00070|class ArchiveFile:
00071|    name: str
00072|    slot: int
00073|    stamp: str
00074|    size: int
00075|    mtime: float
00076|
00077|
00078|@dataclass
00079|class ArchiveSet:
00080|    stamp: str
00081|    files: dict[int, ArchiveFile]
00082|
00083|    @property
00084|    def complete(self) -> bool:
00085|        return all(n in self.files for n in range(1, LIVE_SLOT_COUNT + 1))
00086|
00087|    @property
00088|    def slots_present(self) -> list[int]:
00089|        return sorted(self.files)
00090|
00091|
00092|def list_archive_files() -> list[ArchiveFile]:
00093|    items: list[ArchiveFile] = []
00094|    for path in sorted(archive_dir().glob("wcg-g*.png"), key=lambda p: p.stat().st_mtime, reverse=True):
00095|        parsed = parse_archive_name(path.name)
00096|        if not parsed:
00097|            continue
00098|        slot, stamp = parsed
00099|        st = path.stat()
00100|        items.append(
00101|            ArchiveFile(
00102|                name=path.name,
00103|                slot=slot,
00104|                stamp=stamp,
00105|                size=st.st_size,
00106|                mtime=st.st_mtime,
00107|            )
00108|        )
00109|    return items
00110|
00111|
00112|def group_archive_sets(files: list[ArchiveFile] | None = None) -> list[ArchiveSet]:
00113|    files = files if files is not None else list_archive_files()
00114|    by_stamp: dict[str, dict[int, ArchiveFile]] = {}
00115|    order: list[str] = []
00116|    for item in files:
00117|        if item.stamp not in by_stamp:
00118|            by_stamp[item.stamp] = {}
00119|            order.append(item.stamp)
00120|        by_stamp[item.stamp][item.slot] = item
00121|    return [ArchiveSet(stamp=stamp, files=by_stamp[stamp]) for stamp in order]
00122|
00123|
00124|def live_status() -> list[dict]:
00125|    rows = []
00126|    for slot, name in LIVE_NAMES.items():
00127|        path = live_path(slot)
00128|        rows.append(
00129|            {
00130|                "slot": slot,
00131|                "name": name,
00132|                "exists": path.is_file(),
00133|                "size": path.stat().st_size if path.is_file() else 0,
00134|                "url": f"/tv/{name}",
00135|            }
00136|        )
00137|    return rows
00138|
00139|
00140|def save_archive_upload(filename: str, raw: bytes, *, activate_live: bool = True) -> dict:
00141|    """
00142|    Guarda PNG con sello en archive/.
00143|    Si activate_live=True, también copia/actualiza media/tv/live/wcg-gN.png.
00144|    """
00145|    parsed = parse_archive_name(filename)
00146|    if not parsed:
00147|        raise ValueError(
00148|            "Nombre inválido. Use: wcg-gN YY-MM HH-MM.png (N=1..4; también acepta YY-MM-DD)."
00149|        )
00150|    slot, stamp = parsed
00151|    dest = archive_dir() / filename
00152|    dest.write_bytes(raw)
00153|    live_name = None
00154|    if activate_live:
00155|        live_dest = live_path(slot)
00156|        live_dest.write_bytes(raw)
00157|        live_name = LIVE_NAMES[slot]
00158|    return {
00159|        "filename": filename,
00160|        "slot": slot,
00161|        "stamp": stamp,
00162|        "live": live_name,
00163|    }
00164|
00165|
00166|def promote_latest_complete_set() -> list[str] | None:
00167|    """Si hay un set g1–g4 completo, copia el más reciente a live. None si no hay."""
00168|    for aset in group_archive_sets():
00169|        if aset.complete:
00170|            names = [aset.files[n].name for n in range(1, LIVE_SLOT_COUNT + 1)]
00171|            return copy_archives_to_live(names)
00172|    return None
00173|
00174|
00175|def copy_archives_to_live(filenames: list[str]) -> list[str]:
00176|    """Copia archivos de archive → live (sobrescribe). No borra el archivo con sello."""
00177|    copied: list[str] = []
00178|    seen_slots: set[int] = set()
00179|    for name in filenames:
00180|        parsed = parse_archive_name(name)
00181|        if not parsed:
00182|            raise ValueError(f"Nombre no permitido: {name}")
00183|        slot, _stamp = parsed
00184|        src = archive_dir() / name
00185|        if not src.is_file():
00186|            raise FileNotFoundError(f"No existe en archivo: {name}")
00187|        if slot in seen_slots:
00188|            raise ValueError(f"Seleccionó más de un archivo para wcg-g{slot}.")
00189|        seen_slots.add(slot)
00190|        dest = live_path(slot)
00191|        shutil.copy2(src, dest)
00192|        copied.append(LIVE_NAMES[slot])
00193|    return copied
00194|
00195|
00196|def delete_archives(filenames: list[str]) -> list[str]:
00197|    deleted: list[str] = []
00198|    for name in filenames:
00199|        if not is_safe_archive_name(name):
00200|            raise ValueError(f"Nombre no permitido: {name}")
00201|        path = archive_dir() / name
00202|        if path.is_file():
00203|            path.unlink()
00204|            deleted.append(name)
00205|    return deleted
00206|
00207|
00208|def _superuser(user) -> bool:
00209|    return bool(user.is_superuser)
00210|
00211|
00212|@require_GET
00213|def tv_live_png(request, name: str):
00214|    """Sirve wcg-g1.png … wcg-g4.png sin autenticación (TV)."""
00215|    if name not in LIVE_NAMES.values():
00216|        raise Http404("Archivo TV no encontrado.")
00217|    path = live_dir() / name
00218|    if not path.is_file():
00219|        raise Http404("Aún no hay chart vivo para ese slot.")
00220|    response = FileResponse(path.open("rb"), content_type="image/png")
00221|    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
00222|    response["Pragma"] = "no-cache"
00223|    return response
00224|
00225|
00226|@login_required
00227|@user_passes_test(_superuser)
00228|@require_GET
00229|def tv_archive_png(request, name: str):
00230|    if not is_safe_archive_name(name):
00231|        raise Http404("Nombre inválido.")
00232|    path = archive_dir() / name
00233|    if not path.is_file():
00234|        raise Http404("Archivo no encontrado.")
00235|    return FileResponse(path.open("rb"), content_type="image/png")
00236|
00237|
00238|@login_required
00239|@require_POST
00240|def tv_charts_upload(request):
00241|    """Recibe PNG desde Exportación 4 charts → archive/ + live/."""
00242|    uploaded = request.FILES.get("file") or request.FILES.get("png")
00243|    if not uploaded:
00244|        return JsonResponse({"ok": False, "error": "Falta archivo."}, status=400)
00245|    filename = (uploaded.name or "").strip()
00246|    # Algunos navegadores envían solo el basename; normalizar espacios.
00247|    filename = Path(filename).name
00248|    activate = (request.POST.get("activate") or "1").strip() != "0"
00249|    try:
00250|        result = save_archive_upload(filename, uploaded.read(), activate_live=activate)
00251|    except ValueError as exc:
00252|        return JsonResponse({"ok": False, "error": str(exc)}, status=400)
00253|    except OSError as exc:
00254|        return JsonResponse(
00255|            {"ok": False, "error": f"No se pudo escribir en media/tv/: {exc}"},
00256|            status=500,
00257|        )
00258|    return JsonResponse({"ok": True, **result})
00259|
00260|
00261|@login_required
00262|@user_passes_test(_superuser)
00263|def admin_tv_charts(request):
00264|    period = parse_admin_period(request)
00265|
00266|    if request.method == "POST":
00267|        action = (request.POST.get("action") or "").strip()
00268|        selected = [n.strip() for n in request.POST.getlist("files") if n.strip()]
00269|
00270|        if action == "promote":
00271|            if not selected:
00272|                messages.error(request, "Seleccione al menos un archivo con sello.")
00273|            else:
00274|                try:
00275|                    copied = copy_archives_to_live(selected)
00276|                    messages.success(
00277|                        request,
00278|                        "Copiado a TV (vivos): " + ", ".join(copied) + ".",
00279|                    )
00280|                except (ValueError, FileNotFoundError) as exc:
00281|                    messages.error(request, str(exc))
00282|            return redirect("pgc:admin_tv_charts")
00283|
00284|        if action == "delete":
00285|            if not selected:
00286|                messages.error(request, "Seleccione archivos archivados para borrar.")
00287|            else:
00288|                try:
00289|                    deleted = delete_archives(selected)
00290|                    if deleted:
00291|                        messages.success(
00292|                            request,
00293|                            f"Borrados {len(deleted)} archivo(s) archivado(s).",
00294|                        )
00295|                    else:
00296|                        messages.info(request, "Nada que borrar.")
00297|                except ValueError as exc:
00298|                    messages.error(request, str(exc))
00299|            return redirect("pgc:admin_tv_charts")
00300|
00301|        if action == "promote_stamp":
00302|            stamp = (request.POST.get("stamp") or "").strip()
00303|            sets = {s.stamp: s for s in group_archive_sets()}
00304|            aset = sets.get(stamp)
00305|            if not aset or not aset.complete:
00306|                messages.error(
00307|                    request,
00308|                    "Ese sello no tiene los 4 PNG (g1–g4). Seleccione un set completo.",
00309|                )
00310|            else:
00311|                names = [aset.files[n].name for n in range(1, LIVE_SLOT_COUNT + 1)]
00312|                try:
00313|                    copied = copy_archives_to_live(names)
00314|                    messages.success(
00315|                        request,
00316|                        f"Set «{stamp}» copiado a TV: " + ", ".join(copied) + ".",
00317|                    )
00318|                except (ValueError, FileNotFoundError) as exc:
00319|                    messages.error(request, str(exc))
00320|            return redirect("pgc:admin_tv_charts")
00321|
00322|        messages.error(request, "Acción no reconocida.")
00323|        return redirect("pgc:admin_tv_charts")
00324|
00325|    archive_sets = []
00326|    for aset in group_archive_sets():
00327|        slots = []
00328|        for n in range(1, LIVE_SLOT_COUNT + 1):
00329|            f = aset.files.get(n)
00330|            slots.append(
00331|                {
00332|                    "slot": n,
00333|                    "file": f,
00334|                    "name": f.name if f else None,
00335|                    "preview_url": (
00336|                        reverse("pgc:tv_archive_png", kwargs={"name": f.name})
00337|                        if f
00338|                        else None
00339|                    ),
00340|                }
00341|            )
00342|        archive_sets.append(
00343|            {
00344|                "stamp": aset.stamp,
00345|                "complete": aset.complete,
00346|                "slots": slots,
00347|            }
00348|        )
00349|
00350|    context = {
00351|        **admin_period_context(period),
00352|        "live_slots": live_status(),
00353|        "live_all_empty": not any(s["exists"] for s in live_status()),
00354|        "archive_sets": archive_sets,
00355|        "supports_month_range": False,
00356|    }
00357|    return render(request, "pgc/admin_tv_charts.html", context)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiCkNoYXJ0cyBUVjogYXJjaGl2byBhcmNoaXZhZG9zIGNvbiBzZWxsbyArIGNvcGlhcyB2aXZhcyB3Y2ctZzEuLmc0LnBuZy4KCkxheW91dCBlbiBkaXNjbyAoTUVESUFfUk9PVC90dik6CiAgbWVkaWEvdHYvYXJjaGl2ZS93Y2ctZzEgWVktTU0gSEgtTU0ucG5nCiAgbWVkaWEvdHYvbGl2ZS93Y2ctZzEucG5nIOKApiB3Y2ctZzQucG5nCgpVUkwgcMO6YmxpY2EgKHRlbGV2aXNvcik6CiAgL3R2L3djZy1nMS5wbmcg4oCmIC90di93Y2ctZzQucG5nCiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKaW1wb3J0IHJlCmltcG9ydCBzaHV0aWwKZnJvbSBkYXRhY2xhc3NlcyBpbXBvcnQgZGF0YWNsYXNzCmZyb20gcGF0aGxpYiBpbXBvcnQgUGF0aAoKZnJvbSBkamFuZ28uY29uZiBpbXBvcnQgc2V0dGluZ3MKZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgbWVzc2FnZXMKZnJvbSBkamFuZ28uY29udHJpYi5hdXRoLmRlY29yYXRvcnMgaW1wb3J0IGxvZ2luX3JlcXVpcmVkLCB1c2VyX3Bhc3Nlc190ZXN0CmZyb20gZGphbmdvLmh0dHAgaW1wb3J0IEZpbGVSZXNwb25zZSwgSHR0cDQwNCwgSnNvblJlc3BvbnNlCmZyb20gZGphbmdvLnNob3J0Y3V0cyBpbXBvcnQgcmVkaXJlY3QsIHJlbmRlcgpmcm9tIGRqYW5nby51cmxzIGltcG9ydCByZXZlcnNlCmZyb20gZGphbmdvLnZpZXdzLmRlY29yYXRvcnMuaHR0cCBpbXBvcnQgcmVxdWlyZV9HRVQsIHJlcXVpcmVfUE9TVAoKZnJvbSBwZ2MuYWRtaW5fdXRpbHMgaW1wb3J0IGFkbWluX3BlcmlvZF9jb250ZXh0LCBwYXJzZV9hZG1pbl9wZXJpb2QKCkxJVkVfU0xPVF9DT1VOVCA9IDQKTElWRV9OQU1FUyA9IHtuOiBmIndjZy1ne259LnBuZyIgZm9yIG4gaW4gcmFuZ2UoMSwgTElWRV9TTE9UX0NPVU5UICsgMSl9CiMgU29wb3J0YSBzZWxsbyBudWV2byBZWS1NTS1ERCBISC1NTSB5IGxlZ2FkbyBZWS1NTSBISC1NTQpBUkNISVZFX05BTUVfUkUgPSByZS5jb21waWxlKAogICAgciJed2NnLWcoWzEtNF0pIChcZHsyfS1cZHsyfSg/Oi1cZHsyfSk/IFxkezJ9LVxkezJ9KVwucG5nJCIKKQoKCmRlZiB0dl9yb290KCkgLT4gUGF0aDoKICAgIHJvb3QgPSBQYXRoKHNldHRpbmdzLk1FRElBX1JPT1QpIC8gInR2IgogICAgKHJvb3QgLyAiYXJjaGl2ZSIpLm1rZGlyKHBhcmVudHM9VHJ1ZSwgZXhpc3Rfb2s9VHJ1ZSkKICAgIChyb290IC8gImxpdmUiKS5ta2RpcihwYXJlbnRzPVRydWUsIGV4aXN0X29rPVRydWUpCiAgICByZXR1cm4gcm9vdAoKCmRlZiBhcmNoaXZlX2RpcigpIC0+IFBhdGg6CiAgICByZXR1cm4gdHZfcm9vdCgpIC8gImFyY2hpdmUiCgoKZGVmIGxpdmVfZGlyKCkgLT4gUGF0aDoKICAgIHJldHVybiB0dl9yb290KCkgLyAibGl2ZSIKCgpkZWYgbGl2ZV9wYXRoKHNsb3Q6IGludCkgLT4gUGF0aDoKICAgIGlmIHNsb3Qgbm90IGluIExJVkVfTkFNRVM6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmInNsb3QgaW52w6FsaWRvOiB7c2xvdH0iKQogICAgcmV0dXJuIGxpdmVfZGlyKCkgLyBMSVZFX05BTUVTW3Nsb3RdCgoKZGVmIHBhcnNlX2FyY2hpdmVfbmFtZShuYW1lOiBzdHIpIC0+IHR1cGxlW2ludCwgc3RyXSB8IE5vbmU6CiAgICBtYXRjaCA9IEFSQ0hJVkVfTkFNRV9SRS5tYXRjaChuYW1lKQogICAgaWYgbm90IG1hdGNoOgogICAgICAgIHJldHVybiBOb25lCiAgICByZXR1cm4gaW50KG1hdGNoLmdyb3VwKDEpKSwgbWF0Y2guZ3JvdXAoMikKCgpkZWYgaXNfc2FmZV9hcmNoaXZlX25hbWUobmFtZTogc3RyKSAtPiBib29sOgogICAgcmV0dXJuIHBhcnNlX2FyY2hpdmVfbmFtZShuYW1lKSBpcyBub3QgTm9uZQoKCkBkYXRhY2xhc3MKY2xhc3MgQXJjaGl2ZUZpbGU6CiAgICBuYW1lOiBzdHIKICAgIHNsb3Q6IGludAogICAgc3RhbXA6IHN0cgogICAgc2l6ZTogaW50CiAgICBtdGltZTogZmxvYXQKCgpAZGF0YWNsYXNzCmNsYXNzIEFyY2hpdmVTZXQ6CiAgICBzdGFtcDogc3RyCiAgICBmaWxlczogZGljdFtpbnQsIEFyY2hpdmVGaWxlXQoKICAgIEBwcm9wZXJ0eQogICAgZGVmIGNvbXBsZXRlKHNlbGYpIC0+IGJvb2w6CiAgICAgICAgcmV0dXJuIGFsbChuIGluIHNlbGYuZmlsZXMgZm9yIG4gaW4gcmFuZ2UoMSwgTElWRV9TTE9UX0NPVU5UICsgMSkpCgogICAgQHByb3BlcnR5CiAgICBkZWYgc2xvdHNfcHJlc2VudChzZWxmKSAtPiBsaXN0W2ludF06CiAgICAgICAgcmV0dXJuIHNvcnRlZChzZWxmLmZpbGVzKQoKCmRlZiBsaXN0X2FyY2hpdmVfZmlsZXMoKSAtPiBsaXN0W0FyY2hpdmVGaWxlXToKICAgIGl0ZW1zOiBsaXN0W0FyY2hpdmVGaWxlXSA9IFtdCiAgICBmb3IgcGF0aCBpbiBzb3J0ZWQoYXJjaGl2ZV9kaXIoKS5nbG9iKCJ3Y2ctZyoucG5nIiksIGtleT1sYW1iZGEgcDogcC5zdGF0KCkuc3RfbXRpbWUsIHJldmVyc2U9VHJ1ZSk6CiAgICAgICAgcGFyc2VkID0gcGFyc2VfYXJjaGl2ZV9uYW1lKHBhdGgubmFtZSkKICAgICAgICBpZiBub3QgcGFyc2VkOgogICAgICAgICAgICBjb250aW51ZQogICAgICAgIHNsb3QsIHN0YW1wID0gcGFyc2VkCiAgICAgICAgc3QgPSBwYXRoLnN0YXQoKQogICAgICAgIGl0ZW1zLmFwcGVuZCgKICAgICAgICAgICAgQXJjaGl2ZUZpbGUoCiAgICAgICAgICAgICAgICBuYW1lPXBhdGgubmFtZSwKICAgICAgICAgICAgICAgIHNsb3Q9c2xvdCwKICAgICAgICAgICAgICAgIHN0YW1wPXN0YW1wLAogICAgICAgICAgICAgICAgc2l6ZT1zdC5zdF9zaXplLAogICAgICAgICAgICAgICAgbXRpbWU9c3Quc3RfbXRpbWUsCiAgICAgICAgICAgICkKICAgICAgICApCiAgICByZXR1cm4gaXRlbXMKCgpkZWYgZ3JvdXBfYXJjaGl2ZV9zZXRzKGZpbGVzOiBsaXN0W0FyY2hpdmVGaWxlXSB8IE5vbmUgPSBOb25lKSAtPiBsaXN0W0FyY2hpdmVTZXRdOgogICAgZmlsZXMgPSBmaWxlcyBpZiBmaWxlcyBpcyBub3QgTm9uZSBlbHNlIGxpc3RfYXJjaGl2ZV9maWxlcygpCiAgICBieV9zdGFtcDogZGljdFtzdHIsIGRpY3RbaW50LCBBcmNoaXZlRmlsZV1dID0ge30KICAgIG9yZGVyOiBsaXN0W3N0cl0gPSBbXQogICAgZm9yIGl0ZW0gaW4gZmlsZXM6CiAgICAgICAgaWYgaXRlbS5zdGFtcCBub3QgaW4gYnlfc3RhbXA6CiAgICAgICAgICAgIGJ5X3N0YW1wW2l0ZW0uc3RhbXBdID0ge30KICAgICAgICAgICAgb3JkZXIuYXBwZW5kKGl0ZW0uc3RhbXApCiAgICAgICAgYnlfc3RhbXBbaXRlbS5zdGFtcF1baXRlbS5zbG90XSA9IGl0ZW0KICAgIHJldHVybiBbQXJjaGl2ZVNldChzdGFtcD1zdGFtcCwgZmlsZXM9Ynlfc3RhbXBbc3RhbXBdKSBmb3Igc3RhbXAgaW4gb3JkZXJdCgoKZGVmIGxpdmVfc3RhdHVzKCkgLT4gbGlzdFtkaWN0XToKICAgIHJvd3MgPSBbXQogICAgZm9yIHNsb3QsIG5hbWUgaW4gTElWRV9OQU1FUy5pdGVtcygpOgogICAgICAgIHBhdGggPSBsaXZlX3BhdGgoc2xvdCkKICAgICAgICByb3dzLmFwcGVuZCgKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgInNsb3QiOiBzbG90LAogICAgICAgICAgICAgICAgIm5hbWUiOiBuYW1lLAogICAgICAgICAgICAgICAgImV4aXN0cyI6IHBhdGguaXNfZmlsZSgpLAogICAgICAgICAgICAgICAgInNpemUiOiBwYXRoLnN0YXQoKS5zdF9zaXplIGlmIHBhdGguaXNfZmlsZSgpIGVsc2UgMCwKICAgICAgICAgICAgICAgICJ1cmwiOiBmIi90di97bmFtZX0iLAogICAgICAgICAgICB9CiAgICAgICAgKQogICAgcmV0dXJuIHJvd3MKCgpkZWYgc2F2ZV9hcmNoaXZlX3VwbG9hZChmaWxlbmFtZTogc3RyLCByYXc6IGJ5dGVzLCAqLCBhY3RpdmF0ZV9saXZlOiBib29sID0gVHJ1ZSkgLT4gZGljdDoKICAgICIiIgogICAgR3VhcmRhIFBORyBjb24gc2VsbG8gZW4gYXJjaGl2ZS8uCiAgICBTaSBhY3RpdmF0ZV9saXZlPVRydWUsIHRhbWJpw6luIGNvcGlhL2FjdHVhbGl6YSBtZWRpYS90di9saXZlL3djZy1nTi5wbmcuCiAgICAiIiIKICAgIHBhcnNlZCA9IHBhcnNlX2FyY2hpdmVfbmFtZShmaWxlbmFtZSkKICAgIGlmIG5vdCBwYXJzZWQ6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcigKICAgICAgICAgICAgIk5vbWJyZSBpbnbDoWxpZG8uIFVzZTogd2NnLWdOIFlZLU1NIEhILU1NLnBuZyAoTj0xLi40OyB0YW1iacOpbiBhY2VwdGEgWVktTU0tREQpLiIKICAgICAgICApCiAgICBzbG90LCBzdGFtcCA9IHBhcnNlZAogICAgZGVzdCA9IGFyY2hpdmVfZGlyKCkgLyBmaWxlbmFtZQogICAgZGVzdC53cml0ZV9ieXRlcyhyYXcpCiAgICBsaXZlX25hbWUgPSBOb25lCiAgICBpZiBhY3RpdmF0ZV9saXZlOgogICAgICAgIGxpdmVfZGVzdCA9IGxpdmVfcGF0aChzbG90KQogICAgICAgIGxpdmVfZGVzdC53cml0ZV9ieXRlcyhyYXcpCiAgICAgICAgbGl2ZV9uYW1lID0gTElWRV9OQU1FU1tzbG90XQogICAgcmV0dXJuIHsKICAgICAgICAiZmlsZW5hbWUiOiBmaWxlbmFtZSwKICAgICAgICAic2xvdCI6IHNsb3QsCiAgICAgICAgInN0YW1wIjogc3RhbXAsCiAgICAgICAgImxpdmUiOiBsaXZlX25hbWUsCiAgICB9CgoKZGVmIHByb21vdGVfbGF0ZXN0X2NvbXBsZXRlX3NldCgpIC0+IGxpc3Rbc3RyXSB8IE5vbmU6CiAgICAiIiJTaSBoYXkgdW4gc2V0IGcx4oCTZzQgY29tcGxldG8sIGNvcGlhIGVsIG3DoXMgcmVjaWVudGUgYSBsaXZlLiBOb25lIHNpIG5vIGhheS4iIiIKICAgIGZvciBhc2V0IGluIGdyb3VwX2FyY2hpdmVfc2V0cygpOgogICAgICAgIGlmIGFzZXQuY29tcGxldGU6CiAgICAgICAgICAgIG5hbWVzID0gW2FzZXQuZmlsZXNbbl0ubmFtZSBmb3IgbiBpbiByYW5nZSgxLCBMSVZFX1NMT1RfQ09VTlQgKyAxKV0KICAgICAgICAgICAgcmV0dXJuIGNvcHlfYXJjaGl2ZXNfdG9fbGl2ZShuYW1lcykKICAgIHJldHVybiBOb25lCgoKZGVmIGNvcHlfYXJjaGl2ZXNfdG9fbGl2ZShmaWxlbmFtZXM6IGxpc3Rbc3RyXSkgLT4gbGlzdFtzdHJdOgogICAgIiIiQ29waWEgYXJjaGl2b3MgZGUgYXJjaGl2ZSDihpIgbGl2ZSAoc29icmVzY3JpYmUpLiBObyBib3JyYSBlbCBhcmNoaXZvIGNvbiBzZWxsby4iIiIKICAgIGNvcGllZDogbGlzdFtzdHJdID0gW10KICAgIHNlZW5fc2xvdHM6IHNldFtpbnRdID0gc2V0KCkKICAgIGZvciBuYW1lIGluIGZpbGVuYW1lczoKICAgICAgICBwYXJzZWQgPSBwYXJzZV9hcmNoaXZlX25hbWUobmFtZSkKICAgICAgICBpZiBub3QgcGFyc2VkOgogICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKGYiTm9tYnJlIG5vIHBlcm1pdGlkbzoge25hbWV9IikKICAgICAgICBzbG90LCBfc3RhbXAgPSBwYXJzZWQKICAgICAgICBzcmMgPSBhcmNoaXZlX2RpcigpIC8gbmFtZQogICAgICAgIGlmIG5vdCBzcmMuaXNfZmlsZSgpOgogICAgICAgICAgICByYWlzZSBGaWxlTm90Rm91bmRFcnJvcihmIk5vIGV4aXN0ZSBlbiBhcmNoaXZvOiB7bmFtZX0iKQogICAgICAgIGlmIHNsb3QgaW4gc2Vlbl9zbG90czoKICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIlNlbGVjY2lvbsOzIG3DoXMgZGUgdW4gYXJjaGl2byBwYXJhIHdjZy1ne3Nsb3R9LiIpCiAgICAgICAgc2Vlbl9zbG90cy5hZGQoc2xvdCkKICAgICAgICBkZXN0ID0gbGl2ZV9wYXRoKHNsb3QpCiAgICAgICAgc2h1dGlsLmNvcHkyKHNyYywgZGVzdCkKICAgICAgICBjb3BpZWQuYXBwZW5kKExJVkVfTkFNRVNbc2xvdF0pCiAgICByZXR1cm4gY29waWVkCgoKZGVmIGRlbGV0ZV9hcmNoaXZlcyhmaWxlbmFtZXM6IGxpc3Rbc3RyXSkgLT4gbGlzdFtzdHJdOgogICAgZGVsZXRlZDogbGlzdFtzdHJdID0gW10KICAgIGZvciBuYW1lIGluIGZpbGVuYW1lczoKICAgICAgICBpZiBub3QgaXNfc2FmZV9hcmNoaXZlX25hbWUobmFtZSk6CiAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJOb21icmUgbm8gcGVybWl0aWRvOiB7bmFtZX0iKQogICAgICAgIHBhdGggPSBhcmNoaXZlX2RpcigpIC8gbmFtZQogICAgICAgIGlmIHBhdGguaXNfZmlsZSgpOgogICAgICAgICAgICBwYXRoLnVubGluaygpCiAgICAgICAgICAgIGRlbGV0ZWQuYXBwZW5kKG5hbWUpCiAgICByZXR1cm4gZGVsZXRlZAoKCmRlZiBfc3VwZXJ1c2VyKHVzZXIpIC0+IGJvb2w6CiAgICByZXR1cm4gYm9vbCh1c2VyLmlzX3N1cGVydXNlcikKCgpAcmVxdWlyZV9HRVQKZGVmIHR2X2xpdmVfcG5nKHJlcXVlc3QsIG5hbWU6IHN0cik6CiAgICAiIiJTaXJ2ZSB3Y2ctZzEucG5nIOKApiB3Y2ctZzQucG5nIHNpbiBhdXRlbnRpY2FjacOzbiAoVFYpLiIiIgogICAgaWYgbmFtZSBub3QgaW4gTElWRV9OQU1FUy52YWx1ZXMoKToKICAgICAgICByYWlzZSBIdHRwNDA0KCJBcmNoaXZvIFRWIG5vIGVuY29udHJhZG8uIikKICAgIHBhdGggPSBsaXZlX2RpcigpIC8gbmFtZQogICAgaWYgbm90IHBhdGguaXNfZmlsZSgpOgogICAgICAgIHJhaXNlIEh0dHA0MDQoIkHDum4gbm8gaGF5IGNoYXJ0IHZpdm8gcGFyYSBlc2Ugc2xvdC4iKQogICAgcmVzcG9uc2UgPSBGaWxlUmVzcG9uc2UocGF0aC5vcGVuKCJyYiIpLCBjb250ZW50X3R5cGU9ImltYWdlL3BuZyIpCiAgICByZXNwb25zZVsiQ2FjaGUtQ29udHJvbCJdID0gIm5vLWNhY2hlLCBuby1zdG9yZSwgbXVzdC1yZXZhbGlkYXRlIgogICAgcmVzcG9uc2VbIlByYWdtYSJdID0gIm5vLWNhY2hlIgogICAgcmV0dXJuIHJlc3BvbnNlCgoKQGxvZ2luX3JlcXVpcmVkCkB1c2VyX3Bhc3Nlc190ZXN0KF9zdXBlcnVzZXIpCkByZXF1aXJlX0dFVApkZWYgdHZfYXJjaGl2ZV9wbmcocmVxdWVzdCwgbmFtZTogc3RyKToKICAgIGlmIG5vdCBpc19zYWZlX2FyY2hpdmVfbmFtZShuYW1lKToKICAgICAgICByYWlzZSBIdHRwNDA0KCJOb21icmUgaW52w6FsaWRvLiIpCiAgICBwYXRoID0gYXJjaGl2ZV9kaXIoKSAvIG5hbWUKICAgIGlmIG5vdCBwYXRoLmlzX2ZpbGUoKToKICAgICAgICByYWlzZSBIdHRwNDA0KCJBcmNoaXZvIG5vIGVuY29udHJhZG8uIikKICAgIHJldHVybiBGaWxlUmVzcG9uc2UocGF0aC5vcGVuKCJyYiIpLCBjb250ZW50X3R5cGU9ImltYWdlL3BuZyIpCgoKQGxvZ2luX3JlcXVpcmVkCkByZXF1aXJlX1BPU1QKZGVmIHR2X2NoYXJ0c191cGxvYWQocmVxdWVzdCk6CiAgICAiIiJSZWNpYmUgUE5HIGRlc2RlIEV4cG9ydGFjacOzbiA0IGNoYXJ0cyDihpIgYXJjaGl2ZS8gKyBsaXZlLy4iIiIKICAgIHVwbG9hZGVkID0gcmVxdWVzdC5GSUxFUy5nZXQoImZpbGUiKSBvciByZXF1ZXN0LkZJTEVTLmdldCgicG5nIikKICAgIGlmIG5vdCB1cGxvYWRlZDoKICAgICAgICByZXR1cm4gSnNvblJlc3BvbnNlKHsib2siOiBGYWxzZSwgImVycm9yIjogIkZhbHRhIGFyY2hpdm8uIn0sIHN0YXR1cz00MDApCiAgICBmaWxlbmFtZSA9ICh1cGxvYWRlZC5uYW1lIG9yICIiKS5zdHJpcCgpCiAgICAjIEFsZ3Vub3MgbmF2ZWdhZG9yZXMgZW52w61hbiBzb2xvIGVsIGJhc2VuYW1lOyBub3JtYWxpemFyIGVzcGFjaW9zLgogICAgZmlsZW5hbWUgPSBQYXRoKGZpbGVuYW1lKS5uYW1lCiAgICBhY3RpdmF0ZSA9IChyZXF1ZXN0LlBPU1QuZ2V0KCJhY3RpdmF0ZSIpIG9yICIxIikuc3RyaXAoKSAhPSAiMCIKICAgIHRyeToKICAgICAgICByZXN1bHQgPSBzYXZlX2FyY2hpdmVfdXBsb2FkKGZpbGVuYW1lLCB1cGxvYWRlZC5yZWFkKCksIGFjdGl2YXRlX2xpdmU9YWN0aXZhdGUpCiAgICBleGNlcHQgVmFsdWVFcnJvciBhcyBleGM6CiAgICAgICAgcmV0dXJuIEpzb25SZXNwb25zZSh7Im9rIjogRmFsc2UsICJlcnJvciI6IHN0cihleGMpfSwgc3RhdHVzPTQwMCkKICAgIGV4Y2VwdCBPU0Vycm9yIGFzIGV4YzoKICAgICAgICByZXR1cm4gSnNvblJlc3BvbnNlKAogICAgICAgICAgICB7Im9rIjogRmFsc2UsICJlcnJvciI6IGYiTm8gc2UgcHVkbyBlc2NyaWJpciBlbiBtZWRpYS90di86IHtleGN9In0sCiAgICAgICAgICAgIHN0YXR1cz01MDAsCiAgICAgICAgKQogICAgcmV0dXJuIEpzb25SZXNwb25zZSh7Im9rIjogVHJ1ZSwgKipyZXN1bHR9KQoKCkBsb2dpbl9yZXF1aXJlZApAdXNlcl9wYXNzZXNfdGVzdChfc3VwZXJ1c2VyKQpkZWYgYWRtaW5fdHZfY2hhcnRzKHJlcXVlc3QpOgogICAgcGVyaW9kID0gcGFyc2VfYWRtaW5fcGVyaW9kKHJlcXVlc3QpCgogICAgaWYgcmVxdWVzdC5tZXRob2QgPT0gIlBPU1QiOgogICAgICAgIGFjdGlvbiA9IChyZXF1ZXN0LlBPU1QuZ2V0KCJhY3Rpb24iKSBvciAiIikuc3RyaXAoKQogICAgICAgIHNlbGVjdGVkID0gW24uc3RyaXAoKSBmb3IgbiBpbiByZXF1ZXN0LlBPU1QuZ2V0bGlzdCgiZmlsZXMiKSBpZiBuLnN0cmlwKCldCgogICAgICAgIGlmIGFjdGlvbiA9PSAicHJvbW90ZSI6CiAgICAgICAgICAgIGlmIG5vdCBzZWxlY3RlZDoKICAgICAgICAgICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsICJTZWxlY2Npb25lIGFsIG1lbm9zIHVuIGFyY2hpdm8gY29uIHNlbGxvLiIpCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgY29waWVkID0gY29weV9hcmNoaXZlc190b19saXZlKHNlbGVjdGVkKQogICAgICAgICAgICAgICAgICAgIG1lc3NhZ2VzLnN1Y2Nlc3MoCiAgICAgICAgICAgICAgICAgICAgICAgIHJlcXVlc3QsCiAgICAgICAgICAgICAgICAgICAgICAgICJDb3BpYWRvIGEgVFYgKHZpdm9zKTogIiArICIsICIuam9pbihjb3BpZWQpICsgIi4iLAogICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIGV4Y2VwdCAoVmFsdWVFcnJvciwgRmlsZU5vdEZvdW5kRXJyb3IpIGFzIGV4YzoKICAgICAgICAgICAgICAgICAgICBtZXNzYWdlcy5lcnJvcihyZXF1ZXN0LCBzdHIoZXhjKSkKICAgICAgICAgICAgcmV0dXJuIHJlZGlyZWN0KCJwZ2M6YWRtaW5fdHZfY2hhcnRzIikKCiAgICAgICAgaWYgYWN0aW9uID09ICJkZWxldGUiOgogICAgICAgICAgICBpZiBub3Qgc2VsZWN0ZWQ6CiAgICAgICAgICAgICAgICBtZXNzYWdlcy5lcnJvcihyZXF1ZXN0LCAiU2VsZWNjaW9uZSBhcmNoaXZvcyBhcmNoaXZhZG9zIHBhcmEgYm9ycmFyLiIpCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgZGVsZXRlZCA9IGRlbGV0ZV9hcmNoaXZlcyhzZWxlY3RlZCkKICAgICAgICAgICAgICAgICAgICBpZiBkZWxldGVkOgogICAgICAgICAgICAgICAgICAgICAgICBtZXNzYWdlcy5zdWNjZXNzKAogICAgICAgICAgICAgICAgICAgICAgICAgICAgcmVxdWVzdCwKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGYiQm9ycmFkb3Mge2xlbihkZWxldGVkKX0gYXJjaGl2byhzKSBhcmNoaXZhZG8ocykuIiwKICAgICAgICAgICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICAgICAgICAgIG1lc3NhZ2VzLmluZm8ocmVxdWVzdCwgIk5hZGEgcXVlIGJvcnJhci4iKQogICAgICAgICAgICAgICAgZXhjZXB0IFZhbHVlRXJyb3IgYXMgZXhjOgogICAgICAgICAgICAgICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsIHN0cihleGMpKQogICAgICAgICAgICByZXR1cm4gcmVkaXJlY3QoInBnYzphZG1pbl90dl9jaGFydHMiKQoKICAgICAgICBpZiBhY3Rpb24gPT0gInByb21vdGVfc3RhbXAiOgogICAgICAgICAgICBzdGFtcCA9IChyZXF1ZXN0LlBPU1QuZ2V0KCJzdGFtcCIpIG9yICIiKS5zdHJpcCgpCiAgICAgICAgICAgIHNldHMgPSB7cy5zdGFtcDogcyBmb3IgcyBpbiBncm91cF9hcmNoaXZlX3NldHMoKX0KICAgICAgICAgICAgYXNldCA9IHNldHMuZ2V0KHN0YW1wKQogICAgICAgICAgICBpZiBub3QgYXNldCBvciBub3QgYXNldC5jb21wbGV0ZToKICAgICAgICAgICAgICAgIG1lc3NhZ2VzLmVycm9yKAogICAgICAgICAgICAgICAgICAgIHJlcXVlc3QsCiAgICAgICAgICAgICAgICAgICAgIkVzZSBzZWxsbyBubyB0aWVuZSBsb3MgNCBQTkcgKGcx4oCTZzQpLiBTZWxlY2Npb25lIHVuIHNldCBjb21wbGV0by4iLAogICAgICAgICAgICAgICAgKQogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgbmFtZXMgPSBbYXNldC5maWxlc1tuXS5uYW1lIGZvciBuIGluIHJhbmdlKDEsIExJVkVfU0xPVF9DT1VOVCArIDEpXQogICAgICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgICAgIGNvcGllZCA9IGNvcHlfYXJjaGl2ZXNfdG9fbGl2ZShuYW1lcykKICAgICAgICAgICAgICAgICAgICBtZXNzYWdlcy5zdWNjZXNzKAogICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0LAogICAgICAgICAgICAgICAgICAgICAgICBmIlNldCDCq3tzdGFtcH3CuyBjb3BpYWRvIGEgVFY6ICIgKyAiLCAiLmpvaW4oY29waWVkKSArICIuIiwKICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICBleGNlcHQgKFZhbHVlRXJyb3IsIEZpbGVOb3RGb3VuZEVycm9yKSBhcyBleGM6CiAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMuZXJyb3IocmVxdWVzdCwgc3RyKGV4YykpCiAgICAgICAgICAgIHJldHVybiByZWRpcmVjdCgicGdjOmFkbWluX3R2X2NoYXJ0cyIpCgogICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsICJBY2Npw7NuIG5vIHJlY29ub2NpZGEuIikKICAgICAgICByZXR1cm4gcmVkaXJlY3QoInBnYzphZG1pbl90dl9jaGFydHMiKQoKICAgIGFyY2hpdmVfc2V0cyA9IFtdCiAgICBmb3IgYXNldCBpbiBncm91cF9hcmNoaXZlX3NldHMoKToKICAgICAgICBzbG90cyA9IFtdCiAgICAgICAgZm9yIG4gaW4gcmFuZ2UoMSwgTElWRV9TTE9UX0NPVU5UICsgMSk6CiAgICAgICAgICAgIGYgPSBhc2V0LmZpbGVzLmdldChuKQogICAgICAgICAgICBzbG90cy5hcHBlbmQoCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgInNsb3QiOiBuLAogICAgICAgICAgICAgICAgICAgICJmaWxlIjogZiwKICAgICAgICAgICAgICAgICAgICAibmFtZSI6IGYubmFtZSBpZiBmIGVsc2UgTm9uZSwKICAgICAgICAgICAgICAgICAgICAicHJldmlld191cmwiOiAoCiAgICAgICAgICAgICAgICAgICAgICAgIHJldmVyc2UoInBnYzp0dl9hcmNoaXZlX3BuZyIsIGt3YXJncz17Im5hbWUiOiBmLm5hbWV9KQogICAgICAgICAgICAgICAgICAgICAgICBpZiBmCiAgICAgICAgICAgICAgICAgICAgICAgIGVsc2UgTm9uZQogICAgICAgICAgICAgICAgICAgICksCiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICkKICAgICAgICBhcmNoaXZlX3NldHMuYXBwZW5kKAogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAic3RhbXAiOiBhc2V0LnN0YW1wLAogICAgICAgICAgICAgICAgImNvbXBsZXRlIjogYXNldC5jb21wbGV0ZSwKICAgICAgICAgICAgICAgICJzbG90cyI6IHNsb3RzLAogICAgICAgICAgICB9CiAgICAgICAgKQoKICAgIGNvbnRleHQgPSB7CiAgICAgICAgKiphZG1pbl9wZXJpb2RfY29udGV4dChwZXJpb2QpLAogICAgICAgICJsaXZlX3Nsb3RzIjogbGl2ZV9zdGF0dXMoKSwKICAgICAgICAibGl2ZV9hbGxfZW1wdHkiOiBub3QgYW55KHNbImV4aXN0cyJdIGZvciBzIGluIGxpdmVfc3RhdHVzKCkpLAogICAgICAgICJhcmNoaXZlX3NldHMiOiBhcmNoaXZlX3NldHMsCiAgICAgICAgInN1cHBvcnRzX21vbnRoX3JhbmdlIjogRmFsc2UsCiAgICB9CiAgICByZXR1cm4gcmVuZGVyKHJlcXVlc3QsICJwZ2MvYWRtaW5fdHZfY2hhcnRzLmh0bWwiLCBjb250ZXh0KQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/urls.py
PATH_JSON="pgc/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=86
SIZE_BYTES_UTF8=3158
CONTENT_SHA256=d76231e87dd8ae4b765c5bd36fcf59313eccaec7d6387c60a8d51ad01f8246c6
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
# pgc/urls.py

from django.urls import path
from . import admin_views, tv_charts, views

app_name = "pgc"

urlpatterns = [
    path("tablero/", views.pgc_dashboard, name="dashboard"),
    path("pgc/", views.pgc_home, name="module_home"),
    path("clientes-nuevos/", views.clientes_nuevos_report, name="clientes_nuevos"),
    path("export/dashboard.md", views.pgc_dashboard_export_md, name="dashboard_export_md"),
    path("venta-cruzada/", views.venta_cruzada_report, name="venta_cruzada"),
    path("export/venta-cruzada.md", views.venta_cruzada_export_md, name="venta_cruzada_export_md"),
    path("respuesta-reqs/", views.respuesta_reqs_report, name="respuesta_reqs"),
    path("export/respuesta-reqs.md", views.respuesta_reqs_export_md, name="respuesta_reqs_export_md"),
    path("admin-hub/", admin_views.admin_hub, name="admin_hub"),
    path("admin-hub/mensual/", admin_views.admin_monthly, name="admin_monthly"),
    path(
        "admin-hub/recalcular/",
        admin_views.admin_smart_recalc,
        name="admin_smart_recalc",
    ),
    path("admin-hub/mensual/edicion/", admin_views.admin_manual_edit, name="admin_manual_edit"),
    path(
        "admin-hub/mensual/ingresos/",
        admin_views.admin_ingresos_year,
        name="admin_ingresos_year",
    ),
    path("admin-hub/mensual/bitacora/", admin_views.admin_monthly_log, name="admin_monthly_log"),
    path(
        "admin-hub/mensual/clientes-nuevos/",
        admin_views.admin_new_clients_browse,
        name="admin_new_clients_browse",
    ),
    path(
        "admin-hub/mensual/clientes-nuevos/une/",
        admin_views.admin_new_clients_une,
        name="admin_new_clients_une",
    ),
    path("admin-hub/tv-charts/", tv_charts.admin_tv_charts, name="admin_tv_charts"),
    path(
        "admin-hub/tv-charts/upload/",
        tv_charts.tv_charts_upload,
        name="tv_charts_upload",
    ),
    path(
        "admin-hub/tv-charts/archivo/<path:name>",
        tv_charts.tv_archive_png,
        name="tv_archive_png",
    ),
    path("tv/<str:name>", tv_charts.tv_live_png, name="tv_live_png"),
    path(
        "admin-hub/run-recalc-pgc",
        admin_views.legacy_run_recalc_pgc,
        name="run_recalc_pgc",
    ),

    path(
        "admin-hub/run-recalc-investment-ingresos/",
        admin_views.legacy_run_recalc_investment,
        name="run_recalc_investment_ingresos",
    ),
  
    path(
        "admin-hub/ingresos-manual-capture",
        admin_views.redirect_manual_results,
        name="ingresos_manual_capture",
    ),

    path(
        "admin-hub/exchange-rates/",
        admin_views.redirect_manual_fx,
        name="exchange_rates_manual_capture",
    ),
  
    path("ingresos/", views.ingresos_report, name="ingresos"),
    path("export/ingresos.md", views.ingresos_export_md, name="ingresos_export_md"),
    path("export/clientes-nuevos.md", views.clientes_nuevos_export_md, name="clientes_nuevos_export_md"),
    path("clientes-nuevos/detalle/", views.clientes_nuevos_detail, name="clientes_nuevos_detail"),
    path(
        "venta-cruzada/detalle/",
        views.venta_cruzada_detail,
        name="venta_cruzada_detail",
        ),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|# pgc/urls.py
00002|
00003|from django.urls import path
00004|from . import admin_views, tv_charts, views
00005|
00006|app_name = "pgc"
00007|
00008|urlpatterns = [
00009|    path("tablero/", views.pgc_dashboard, name="dashboard"),
00010|    path("pgc/", views.pgc_home, name="module_home"),
00011|    path("clientes-nuevos/", views.clientes_nuevos_report, name="clientes_nuevos"),
00012|    path("export/dashboard.md", views.pgc_dashboard_export_md, name="dashboard_export_md"),
00013|    path("venta-cruzada/", views.venta_cruzada_report, name="venta_cruzada"),
00014|    path("export/venta-cruzada.md", views.venta_cruzada_export_md, name="venta_cruzada_export_md"),
00015|    path("respuesta-reqs/", views.respuesta_reqs_report, name="respuesta_reqs"),
00016|    path("export/respuesta-reqs.md", views.respuesta_reqs_export_md, name="respuesta_reqs_export_md"),
00017|    path("admin-hub/", admin_views.admin_hub, name="admin_hub"),
00018|    path("admin-hub/mensual/", admin_views.admin_monthly, name="admin_monthly"),
00019|    path(
00020|        "admin-hub/recalcular/",
00021|        admin_views.admin_smart_recalc,
00022|        name="admin_smart_recalc",
00023|    ),
00024|    path("admin-hub/mensual/edicion/", admin_views.admin_manual_edit, name="admin_manual_edit"),
00025|    path(
00026|        "admin-hub/mensual/ingresos/",
00027|        admin_views.admin_ingresos_year,
00028|        name="admin_ingresos_year",
00029|    ),
00030|    path("admin-hub/mensual/bitacora/", admin_views.admin_monthly_log, name="admin_monthly_log"),
00031|    path(
00032|        "admin-hub/mensual/clientes-nuevos/",
00033|        admin_views.admin_new_clients_browse,
00034|        name="admin_new_clients_browse",
00035|    ),
00036|    path(
00037|        "admin-hub/mensual/clientes-nuevos/une/",
00038|        admin_views.admin_new_clients_une,
00039|        name="admin_new_clients_une",
00040|    ),
00041|    path("admin-hub/tv-charts/", tv_charts.admin_tv_charts, name="admin_tv_charts"),
00042|    path(
00043|        "admin-hub/tv-charts/upload/",
00044|        tv_charts.tv_charts_upload,
00045|        name="tv_charts_upload",
00046|    ),
00047|    path(
00048|        "admin-hub/tv-charts/archivo/<path:name>",
00049|        tv_charts.tv_archive_png,
00050|        name="tv_archive_png",
00051|    ),
00052|    path("tv/<str:name>", tv_charts.tv_live_png, name="tv_live_png"),
00053|    path(
00054|        "admin-hub/run-recalc-pgc",
00055|        admin_views.legacy_run_recalc_pgc,
00056|        name="run_recalc_pgc",
00057|    ),
00058|
00059|    path(
00060|        "admin-hub/run-recalc-investment-ingresos/",
00061|        admin_views.legacy_run_recalc_investment,
00062|        name="run_recalc_investment_ingresos",
00063|    ),
00064|  
00065|    path(
00066|        "admin-hub/ingresos-manual-capture",
00067|        admin_views.redirect_manual_results,
00068|        name="ingresos_manual_capture",
00069|    ),
00070|
00071|    path(
00072|        "admin-hub/exchange-rates/",
00073|        admin_views.redirect_manual_fx,
00074|        name="exchange_rates_manual_capture",
00075|    ),
00076|  
00077|    path("ingresos/", views.ingresos_report, name="ingresos"),
00078|    path("export/ingresos.md", views.ingresos_export_md, name="ingresos_export_md"),
00079|    path("export/clientes-nuevos.md", views.clientes_nuevos_export_md, name="clientes_nuevos_export_md"),
00080|    path("clientes-nuevos/detalle/", views.clientes_nuevos_detail, name="clientes_nuevos_detail"),
00081|    path(
00082|        "venta-cruzada/detalle/",
00083|        views.venta_cruzada_detail,
00084|        name="venta_cruzada_detail",
00085|        ),
00086|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IyBwZ2MvdXJscy5weQoKZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aApmcm9tIC4gaW1wb3J0IGFkbWluX3ZpZXdzLCB0dl9jaGFydHMsIHZpZXdzCgphcHBfbmFtZSA9ICJwZ2MiCgp1cmxwYXR0ZXJucyA9IFsKICAgIHBhdGgoInRhYmxlcm8vIiwgdmlld3MucGdjX2Rhc2hib2FyZCwgbmFtZT0iZGFzaGJvYXJkIiksCiAgICBwYXRoKCJwZ2MvIiwgdmlld3MucGdjX2hvbWUsIG5hbWU9Im1vZHVsZV9ob21lIiksCiAgICBwYXRoKCJjbGllbnRlcy1udWV2b3MvIiwgdmlld3MuY2xpZW50ZXNfbnVldm9zX3JlcG9ydCwgbmFtZT0iY2xpZW50ZXNfbnVldm9zIiksCiAgICBwYXRoKCJleHBvcnQvZGFzaGJvYXJkLm1kIiwgdmlld3MucGdjX2Rhc2hib2FyZF9leHBvcnRfbWQsIG5hbWU9ImRhc2hib2FyZF9leHBvcnRfbWQiKSwKICAgIHBhdGgoInZlbnRhLWNydXphZGEvIiwgdmlld3MudmVudGFfY3J1emFkYV9yZXBvcnQsIG5hbWU9InZlbnRhX2NydXphZGEiKSwKICAgIHBhdGgoImV4cG9ydC92ZW50YS1jcnV6YWRhLm1kIiwgdmlld3MudmVudGFfY3J1emFkYV9leHBvcnRfbWQsIG5hbWU9InZlbnRhX2NydXphZGFfZXhwb3J0X21kIiksCiAgICBwYXRoKCJyZXNwdWVzdGEtcmVxcy8iLCB2aWV3cy5yZXNwdWVzdGFfcmVxc19yZXBvcnQsIG5hbWU9InJlc3B1ZXN0YV9yZXFzIiksCiAgICBwYXRoKCJleHBvcnQvcmVzcHVlc3RhLXJlcXMubWQiLCB2aWV3cy5yZXNwdWVzdGFfcmVxc19leHBvcnRfbWQsIG5hbWU9InJlc3B1ZXN0YV9yZXFzX2V4cG9ydF9tZCIpLAogICAgcGF0aCgiYWRtaW4taHViLyIsIGFkbWluX3ZpZXdzLmFkbWluX2h1YiwgbmFtZT0iYWRtaW5faHViIiksCiAgICBwYXRoKCJhZG1pbi1odWIvbWVuc3VhbC8iLCBhZG1pbl92aWV3cy5hZG1pbl9tb250aGx5LCBuYW1lPSJhZG1pbl9tb250aGx5IiksCiAgICBwYXRoKAogICAgICAgICJhZG1pbi1odWIvcmVjYWxjdWxhci8iLAogICAgICAgIGFkbWluX3ZpZXdzLmFkbWluX3NtYXJ0X3JlY2FsYywKICAgICAgICBuYW1lPSJhZG1pbl9zbWFydF9yZWNhbGMiLAogICAgKSwKICAgIHBhdGgoImFkbWluLWh1Yi9tZW5zdWFsL2VkaWNpb24vIiwgYWRtaW5fdmlld3MuYWRtaW5fbWFudWFsX2VkaXQsIG5hbWU9ImFkbWluX21hbnVhbF9lZGl0IiksCiAgICBwYXRoKAogICAgICAgICJhZG1pbi1odWIvbWVuc3VhbC9pbmdyZXNvcy8iLAogICAgICAgIGFkbWluX3ZpZXdzLmFkbWluX2luZ3Jlc29zX3llYXIsCiAgICAgICAgbmFtZT0iYWRtaW5faW5ncmVzb3NfeWVhciIsCiAgICApLAogICAgcGF0aCgiYWRtaW4taHViL21lbnN1YWwvYml0YWNvcmEvIiwgYWRtaW5fdmlld3MuYWRtaW5fbW9udGhseV9sb2csIG5hbWU9ImFkbWluX21vbnRobHlfbG9nIiksCiAgICBwYXRoKAogICAgICAgICJhZG1pbi1odWIvbWVuc3VhbC9jbGllbnRlcy1udWV2b3MvIiwKICAgICAgICBhZG1pbl92aWV3cy5hZG1pbl9uZXdfY2xpZW50c19icm93c2UsCiAgICAgICAgbmFtZT0iYWRtaW5fbmV3X2NsaWVudHNfYnJvd3NlIiwKICAgICksCiAgICBwYXRoKAogICAgICAgICJhZG1pbi1odWIvbWVuc3VhbC9jbGllbnRlcy1udWV2b3MvdW5lLyIsCiAgICAgICAgYWRtaW5fdmlld3MuYWRtaW5fbmV3X2NsaWVudHNfdW5lLAogICAgICAgIG5hbWU9ImFkbWluX25ld19jbGllbnRzX3VuZSIsCiAgICApLAogICAgcGF0aCgiYWRtaW4taHViL3R2LWNoYXJ0cy8iLCB0dl9jaGFydHMuYWRtaW5fdHZfY2hhcnRzLCBuYW1lPSJhZG1pbl90dl9jaGFydHMiKSwKICAgIHBhdGgoCiAgICAgICAgImFkbWluLWh1Yi90di1jaGFydHMvdXBsb2FkLyIsCiAgICAgICAgdHZfY2hhcnRzLnR2X2NoYXJ0c191cGxvYWQsCiAgICAgICAgbmFtZT0idHZfY2hhcnRzX3VwbG9hZCIsCiAgICApLAogICAgcGF0aCgKICAgICAgICAiYWRtaW4taHViL3R2LWNoYXJ0cy9hcmNoaXZvLzxwYXRoOm5hbWU+IiwKICAgICAgICB0dl9jaGFydHMudHZfYXJjaGl2ZV9wbmcsCiAgICAgICAgbmFtZT0idHZfYXJjaGl2ZV9wbmciLAogICAgKSwKICAgIHBhdGgoInR2LzxzdHI6bmFtZT4iLCB0dl9jaGFydHMudHZfbGl2ZV9wbmcsIG5hbWU9InR2X2xpdmVfcG5nIiksCiAgICBwYXRoKAogICAgICAgICJhZG1pbi1odWIvcnVuLXJlY2FsYy1wZ2MiLAogICAgICAgIGFkbWluX3ZpZXdzLmxlZ2FjeV9ydW5fcmVjYWxjX3BnYywKICAgICAgICBuYW1lPSJydW5fcmVjYWxjX3BnYyIsCiAgICApLAoKICAgIHBhdGgoCiAgICAgICAgImFkbWluLWh1Yi9ydW4tcmVjYWxjLWludmVzdG1lbnQtaW5ncmVzb3MvIiwKICAgICAgICBhZG1pbl92aWV3cy5sZWdhY3lfcnVuX3JlY2FsY19pbnZlc3RtZW50LAogICAgICAgIG5hbWU9InJ1bl9yZWNhbGNfaW52ZXN0bWVudF9pbmdyZXNvcyIsCiAgICApLAogIAogICAgcGF0aCgKICAgICAgICAiYWRtaW4taHViL2luZ3Jlc29zLW1hbnVhbC1jYXB0dXJlIiwKICAgICAgICBhZG1pbl92aWV3cy5yZWRpcmVjdF9tYW51YWxfcmVzdWx0cywKICAgICAgICBuYW1lPSJpbmdyZXNvc19tYW51YWxfY2FwdHVyZSIsCiAgICApLAoKICAgIHBhdGgoCiAgICAgICAgImFkbWluLWh1Yi9leGNoYW5nZS1yYXRlcy8iLAogICAgICAgIGFkbWluX3ZpZXdzLnJlZGlyZWN0X21hbnVhbF9meCwKICAgICAgICBuYW1lPSJleGNoYW5nZV9yYXRlc19tYW51YWxfY2FwdHVyZSIsCiAgICApLAogIAogICAgcGF0aCgiaW5ncmVzb3MvIiwgdmlld3MuaW5ncmVzb3NfcmVwb3J0LCBuYW1lPSJpbmdyZXNvcyIpLAogICAgcGF0aCgiZXhwb3J0L2luZ3Jlc29zLm1kIiwgdmlld3MuaW5ncmVzb3NfZXhwb3J0X21kLCBuYW1lPSJpbmdyZXNvc19leHBvcnRfbWQiKSwKICAgIHBhdGgoImV4cG9ydC9jbGllbnRlcy1udWV2b3MubWQiLCB2aWV3cy5jbGllbnRlc19udWV2b3NfZXhwb3J0X21kLCBuYW1lPSJjbGllbnRlc19udWV2b3NfZXhwb3J0X21kIiksCiAgICBwYXRoKCJjbGllbnRlcy1udWV2b3MvZGV0YWxsZS8iLCB2aWV3cy5jbGllbnRlc19udWV2b3NfZGV0YWlsLCBuYW1lPSJjbGllbnRlc19udWV2b3NfZGV0YWlsIiksCiAgICBwYXRoKAogICAgICAgICJ2ZW50YS1jcnV6YWRhL2RldGFsbGUvIiwKICAgICAgICB2aWV3cy52ZW50YV9jcnV6YWRhX2RldGFpbCwKICAgICAgICBuYW1lPSJ2ZW50YV9jcnV6YWRhX2RldGFpbCIsCiAgICAgICAgKSwKXQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
