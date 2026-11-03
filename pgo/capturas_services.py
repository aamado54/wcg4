"""Servicios capturas manuales PGO: período, horario, permisos, archivos sugeridos."""

from __future__ import annotations

import re
from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.contrib.auth.models import Group
from django.utils import timezone

from pgo.models import PgoArchivoRegistro, PgoManualCaptureVersion

TZ = ZoneInfo(getattr(settings, "PGO_CAPTURAS_TIMEZONE", settings.TIME_ZONE))


def now_local() -> datetime:
    return timezone.now().astimezone(TZ)


def default_period() -> tuple[int, int]:
    n = now_local()
    return n.year, n.month


def period_from_request(request) -> tuple[int, int]:
    try:
        y = int(request.GET.get("year") or request.POST.get("period_year"))
        m = int(request.GET.get("month") or request.POST.get("period_month"))
        if 1 <= m <= 12 and 2000 <= y <= 2100:
            return y, m
    except (TypeError, ValueError):
        pass
    return default_period()


def is_out_of_period(year: int, month: int) -> bool:
    cy, cm = default_period()
    return (year, month) != (cy, cm)


def business_hours_window() -> tuple[int, int]:
    start, end = getattr(settings, "PGO_CAPTURAS_BUSINESS_HOURS", (9, 18))
    return int(start), int(end)


def is_within_business_hours(when: datetime | None = None) -> bool:
    dt = (when or timezone.now()).astimezone(TZ)
    start_h, end_h = business_hours_window()
    return start_h <= dt.hour < end_h and dt.weekday() < 5


def business_hours_message() -> str:
    start_h, end_h = business_hours_window()
    return (
        f"Las capturas nuevas solo se permiten en horario hábil "
        f"({start_h:02d}:00–{end_h:02d}:00, {settings.TIME_ZONE}), lunes a viernes."
    )


def user_can_capture(slug: str, user) -> bool:
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    if slug == "legal_garantias_registro":
        allowed = getattr(settings, "PGO_CAPTURAS_LEGAL_GARANTIAS_USERNAMES", ())
        group_name = getattr(settings, "PGO_CAPTURAS_LEGAL_GARANTIAS_GROUP", "")
        if user.username in allowed:
            return True
        if group_name and user.groups.filter(name=group_name).exists():
            return True
        return False
    return True


def permission_denied_message(slug: str) -> str:
    if slug == "legal_garantias_registro":
        return "Solo usuarios autorizados (Legal — garantías mobiliarias) pueden capturar aquí."
    return "No tiene permiso para esta captura."


def latest_version(slug: str, year: int, month: int) -> PgoManualCaptureVersion | None:
    return (
        PgoManualCaptureVersion.objects.filter(
            capture_type=slug,
            period_year=year,
            period_month=month,
        )
        .select_related("user")
        .order_by("-created_at")
        .first()
    )


def version_history(slug: str, year: int | None = None, month: int | None = None):
    qs = PgoManualCaptureVersion.objects.filter(capture_type=slug).select_related("user")
    if year is not None:
        qs = qs.filter(period_year=year)
    if month is not None:
        qs = qs.filter(period_month=month)
    return qs.order_by("-created_at")


# Reportes esperados (Operaciones — día 7)
OP_REPORTES_PGO_7_ROWS: tuple[tuple[str, str], ...] = (
    ("reporte_cierre", "Reporte Cierre"),
    ("vobo_comisiones_investments", "VoBo Comisiones Investments"),
    ("vobo_comisiones_factoring", "VoBo Comisiones Factoring"),
    ("vobo_comisiones_leasing", "VoBo Comisiones Leasing"),
    ("eeff_integraciones", "EEFF con integraciones"),
    ("reporte_cartera", "Reporte Cartera / cierre operativo"),
)

_REPORTE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("reporte_cierre", re.compile(r"cierre", re.I)),
    ("vobo_comisiones_investments", re.compile(r"vobo.*comision.*invest|invest.*comision", re.I)),
    ("vobo_comisiones_factoring", re.compile(r"vobo.*comision.*fact|fact.*comision", re.I)),
    ("vobo_comisiones_leasing", re.compile(r"vobo.*comision.*leas|leas.*comision", re.I)),
    ("eeff_integraciones", re.compile(r"eeff.*integr|integr.*eeff", re.I)),
    ("reporte_cartera", re.compile(r"cartera|portfolio", re.I)),
]


def suggested_report_dates(year: int, month: int) -> dict[str, str | None]:
    """Fechas ISO sugeridas desde último import ArchivosPGO del mes (si hay match por nombre)."""
    start = datetime(year, month, 1, tzinfo=TZ)
    if month == 12:
        end = datetime(year + 1, 1, 1, tzinfo=TZ)
    else:
        end = datetime(year, month + 1, 1, tzinfo=TZ)
    qs = PgoArchivoRegistro.objects.filter(
        event_date__gte=start.date(),
        event_date__lt=end.date(),
    ).only("archivo", "event_date", "creado_en")
    by_key: dict[str, str | None] = {k: None for k, _ in OP_REPORTES_PGO_7_ROWS}
    for row in qs:
        name = row.archivo or ""
        d = row.event_date
        if not d:
            continue
        iso = d.isoformat()
        for key, pat in _REPORTE_PATTERNS:
            if pat.search(name):
                prev = by_key.get(key)
                if prev is None or iso > prev:
                    by_key[key] = iso
    return by_key


def validate_operation_id(op_id: str) -> str | None:
    op_id = (op_id or "").strip().upper()
    min_len = getattr(settings, "PGO_CAPTURAS_OPERATION_ID_MIN", 5)
    max_len = getattr(settings, "PGO_CAPTURAS_OPERATION_ID_MAX", 20)
    if len(op_id) < min_len or len(op_id) > max_len:
        return f"ID operación: entre {min_len} y {max_len} caracteres."
    if not re.fullmatch(r"[A-Z0-9_-]+", op_id):
        return "ID operación: solo A-Z, 0-9, _ y - (mayúsculas)."
    return None
