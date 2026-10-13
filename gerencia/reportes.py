"""Reportes asociados a stress tests (PDF + MD en disco)."""

from __future__ import annotations

from pathlib import Path

from django.conf import settings


def stress_reportes_dir() -> Path:
    raw = getattr(
        settings,
        "WCG_STRESS_REPORTES_DIR",
        settings.BASE_DIR.parent / "data" / "now" / "reportes",
    )
    return Path(raw)


def resolve_report_file(filename: str) -> Path:
    base = stress_reportes_dir().resolve()
    path = (base / filename).resolve()
    if not str(path).startswith(str(base)):
        raise ValueError("invalid path")
    return path
