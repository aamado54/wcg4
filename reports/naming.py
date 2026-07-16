"""Utilidades de nombres y hora para archivos de reportes."""

from __future__ import annotations

from datetime import datetime

from django.utils import timezone


def report_stamp(now: datetime | None = None) -> str:
    """
    Sufijo obligatorio: ' yy-mm hh-mm' (espacio + yy-mm + espacio + hh-mm).
    Usa zona horaria Django (America/Guatemala).
    """
    now = now or timezone.localtime()
    return f" {now.strftime('%y-%m')} {now.strftime('%H-%M')}"


def stamp_filename(stem: str, ext: str, now: datetime | None = None) -> str:
    ext = ext.lstrip(".")
    return f"{stem}{report_stamp(now)}.{ext}"
