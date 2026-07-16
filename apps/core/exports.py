"""Exportaciones CSV simples vía HttpResponse."""

from __future__ import annotations

import csv
from io import StringIO

from django.http import HttpResponse


def csv_response(filename: str, headers: list[str], rows: list[list]) -> HttpResponse:
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    response = HttpResponse("\ufeff" + buffer.getvalue(), content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
