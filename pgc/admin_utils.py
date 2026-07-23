"""Utilidades compartidas del área de Administración."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from urllib.parse import urlencode

from django.db.models import Q, QuerySet
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone


@dataclass(frozen=True)
class AdminPeriod:
    """Período admin: rango de meses en un mismo año.

    Las pantallas de un solo mes usan ``month`` (= fin del rango).
    Las de datos/browse usan ``month_from``..``month_to``.
    """

    year: int
    month_from: int
    month_to: int

    @property
    def month(self) -> int:
        """Mes operativo (último del rango) para pantallas de un solo mes."""
        return self.month_to

    @property
    def is_range(self) -> bool:
        return self.month_from != self.month_to

    def months(self) -> list[int]:
        return list(range(self.month_from, self.month_to + 1))

    @property
    def label(self) -> str:
        if self.is_range:
            return f"{self.year}-{self.month_from:02d} → {self.year}-{self.month_to:02d}"
        return f"{self.year}-{self.month_to:02d}"

    @property
    def focus_label(self) -> str:
        return f"{self.year}-{self.month_to:02d}"

    def query_dict(self, **extra) -> dict:
        data = {
            "year": str(self.year),
            "month": str(self.month_to),
            "month_from": str(self.month_from),
            "month_to": str(self.month_to),
        }
        for key, value in extra.items():
            if value is None or value == "":
                continue
            data[key] = str(value)
        return data

    def querystring(self, **extra) -> str:
        return urlencode(self.query_dict(**extra))


def _clamp_month(value: int) -> int:
    return max(1, min(12, value))


def default_admin_period(now=None) -> AdminPeriod:
    """Rango maestro por defecto: año actual, mes 01 → mes anterior al actual.

    En enero (no hay mes anterior en el mismo año) queda 01→01.
    """
    now = now or timezone.now()
    year = now.year
    if now.month <= 1:
        return AdminPeriod(year=year, month_from=1, month_to=1)
    return AdminPeriod(year=year, month_from=1, month_to=now.month - 1)


def parse_admin_period(
    request,
    default_year: int | None = None,
    default_month: int | None = None,
) -> AdminPeriod:
    defaults = default_admin_period()
    if default_year is None:
        default_year = defaults.year
    if default_month is None:
        default_month = defaults.month_to

    get = request.GET
    post = request.POST

    def _raw(*keys: str) -> str | None:
        for key in keys:
            value = get.get(key) or post.get(key)
            if value not in (None, ""):
                return value
        return None

    year_raw = _raw("year")
    # month / month_to = fin del rango (compat + pantallas single-month)
    month_to_raw = _raw("month_to", "month")
    month_from_raw = _raw("month_from")

    # Sin parámetros de período → año actual, 01 hasta el mes anterior al actual.
    if year_raw is None and month_to_raw is None and month_from_raw is None:
        return AdminPeriod(
            year=default_year,
            month_from=1,
            month_to=_clamp_month(default_month),
        )

    year_raw = year_raw or str(default_year)
    month_to_raw = month_to_raw or str(default_month)
    # Si viene mes fin pero no "desde", interpretar como un solo mes (compat).
    month_from_raw = month_from_raw or month_to_raw

    try:
        year = int(str(year_raw).replace(",", "").replace(" ", "").replace("\u00a0", ""))
        month_to = _clamp_month(int(str(month_to_raw).replace(",", "").replace(" ", "").replace("\u00a0", "")))
        month_from = _clamp_month(int(str(month_from_raw).replace(",", "").replace(" ", "").replace("\u00a0", "")))
    except (TypeError, ValueError):
        return AdminPeriod(
            year=default_year,
            month_from=1,
            month_to=_clamp_month(default_month),
        )

    if month_from > month_to:
        month_from, month_to = month_to, month_from

    return AdminPeriod(year=year, month_from=month_from, month_to=month_to)


def parse_period(
    request,
    default_year: int | None = None,
    default_month: int | None = None,
) -> tuple[int, int]:
    """Compat: (year, month_to). Preferir parse_admin_period."""
    period = parse_admin_period(request, default_year=default_year, default_month=default_month)
    return period.year, period.month


def period_filter(period: AdminPeriod, year_field: str = "year", month_field: str = "month") -> Q:
    return Q(**{year_field: period.year}) & Q(
        **{f"{month_field}__gte": period.month_from, f"{month_field}__lte": period.month_to}
    )


def apply_period_range(
    qs: QuerySet,
    period: AdminPeriod,
    *,
    year_field: str = "year",
    month_field: str = "month",
) -> QuerySet:
    return qs.filter(period_filter(period, year_field=year_field, month_field=month_field))


def admin_period_context(period: AdminPeriod) -> dict:
    from pgc.admin_recalc import get_global_recalc_status

    return {
        "period": period,
        "year": period.year,
        "month": period.month,
        "month_from": period.month_from,
        "month_to": period.month_to,
        "period_label": period.label,
        "period_focus_label": period.focus_label,
        "period_is_range": period.is_range,
        "period_qs": period.querystring(),
        "month_choices": list(range(1, 13)),
        "year_choices": list(range(2024, 2031)),
        "recalc_status": get_global_recalc_status(),
    }


def redirect_admin_monthly(
    year: int | AdminPeriod | None = None,
    month: int | None = None,
    block: str | None = None,
    *,
    period: AdminPeriod | None = None,
) -> redirect:
    p = _as_period(year, month, period)
    url = f"{reverse('pgc:admin_monthly')}?{p.querystring(block=block)}"
    return redirect(url)


def redirect_admin_manual(
    year: int | AdminPeriod | None = None,
    month: int | None = None,
    tab: str | None = None,
    *,
    period: AdminPeriod | None = None,
) -> redirect:
    p = _as_period(year, month, period)
    url = f"{reverse('pgc:admin_manual_edit')}?{p.querystring(tab=tab)}"
    return redirect(url)


def redirect_admin_new_clients_browse(
    year: int | AdminPeriod | None = None,
    month: int | None = None,
    *,
    period: AdminPeriod | None = None,
) -> redirect:
    p = _as_period(year, month, period)
    return redirect(f"{reverse('pgc:admin_new_clients_browse')}?{p.querystring()}")


def redirect_admin_new_clients_une(
    year: int | AdminPeriod | None = None,
    month: int | None = None,
    *,
    period: AdminPeriod | None = None,
) -> redirect:
    p = _as_period(year, month, period)
    return redirect(f"{reverse('pgc:admin_new_clients_une')}?{p.querystring()}")


def redirect_admin_ingresos_year(
    year: int | AdminPeriod | None = None,
    month: int | None = None,
    *,
    period: AdminPeriod | None = None,
    curr: str | None = None,
) -> redirect:
    p = _as_period(year, month, period)
    qs = p.querystring()
    if curr:
        qs = f"{qs}&curr={curr}"
    return redirect(f"{reverse('pgc:admin_ingresos_year')}?{qs}")


def _as_period(
    year: int | AdminPeriod | None,
    month: int | None,
    period: AdminPeriod | None,
) -> AdminPeriod:
    if isinstance(year, AdminPeriod):
        return year
    if period is not None:
        return period
    if year is None or month is None:
        raise TypeError("Debe indicar AdminPeriod o year/month")
    return AdminPeriod(year=year, month_from=month, month_to=month)


def parse_decimal_or_none(raw_value) -> Decimal | None:
    if raw_value is None:
        return None

    text = str(raw_value).strip()
    if text == "":
        return None

    text = text.replace(" ", "")
    if "," in text and "." in text:
        text = text.replace(",", "")
    elif "," in text:
        text = text.replace(",", ".")

    try:
        return Decimal(text)
    except (InvalidOperation, ValueError):
        return None


def format_value(value) -> str:
    if value is None:
        return ""
    return str(value)
