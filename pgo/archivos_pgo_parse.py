"""Parseo ArchivosPGO: fecha en nombre (dd.mm.yyyy) y CreadoEn (yyyy-mm-dd hh:mm:ss)."""

from __future__ import annotations

import re
from datetime import date, datetime, time

from pgo.archivos_dates import parse_entrega

_DD_MM_YYYY = re.compile(
    r"(?<!\d)(\d{1,2})\.(\d{1,2})\.(\d{4})(?!\d)"
)
_DD_MM_YY = re.compile(
    r"(?<!\d)(\d{1,2})\.(\d{1,2})\.(\d{2})(?!\d)"
)
_DDMMYY = re.compile(r"(?<!\d)(\d{2})(\d{2})(\d{2})(?!\d)")


def _to_date(d: int, m: int, y: int) -> date | None:
    if y < 100:
        y = 2000 + y if y < 70 else 1900 + y
    try:
        return date(y, m, d)
    except ValueError:
        return None


def parse_event_date_from_archivo(archivo: str) -> date | None:
    """Fecha del hecho en el nombre de archivo (prioridad dd.mm.yyyy)."""
    if not archivo:
        return None
    text = str(archivo).strip()
    for pat in (_DD_MM_YYYY, _DD_MM_YY):
        m = pat.search(text)
        if m:
            d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
            got = _to_date(d, mo, y)
            if got:
                return got
    for m in _DDMMYY.finditer(text):
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if d > 31 or mo > 12:
            continue
        got = _to_date(d, mo, y)
        if got:
            return got
    return None


def parse_creado_en(value) -> datetime | None:
    """Columna CreadoEn: yyyy-mm-dd hh:mm:ss (ISO / Excel)."""
    return parse_entrega(value)


def elapsed_seconds(event_day: date, creado_en: datetime) -> float:
    """Resta siempre positiva entre CreadoEn y la fecha del archivo (medianoche local)."""
    start = datetime.combine(event_day, time.min)
    end = creado_en.replace(tzinfo=None) if creado_en.tzinfo else creado_en
    return abs((end - start).total_seconds())
