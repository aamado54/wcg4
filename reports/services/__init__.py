"""Orquestación: genera archivos y empaqueta ZIP cuando corresponde."""

from __future__ import annotations

import zipfile
from io import BytesIO
from typing import Iterable

from django.utils import timezone

from reports.models import ReportConfig
from reports.naming import stamp_filename
from reports.services.coverage import build_admin_coverage_md
from reports.services.pgc_results import build_pgc_results
from reports.services.pgo_results import build_pgo_results
from reports.services.risk_results import build_risk_results
from reports.xlsx_utils import build_workbook

AREA_ADMIN = "admin"
AREA_PGC = "pgc"
AREA_PGO = "pgo"
AREA_RISK = "risk"

VALID_AREAS = {AREA_ADMIN, AREA_PGC, AREA_PGO, AREA_RISK}


def generate_report_package(areas: Iterable[str]) -> tuple[str, bytes, str]:
    """
    Returns (filename, content_bytes, content_type).
    ZIP if more than one file; otherwise single file.
    """
    selected = [a for a in areas if a in VALID_AREAS]
    if not selected:
        raise ValueError("Debe seleccionar al menos un área de reporte.")

    cfg = ReportConfig.get_active()
    now = timezone.localtime()
    files: list[tuple[str, bytes]] = []

    if AREA_ADMIN in selected:
        md = build_admin_coverage_md(cfg)
        files.append(
            (
                stamp_filename("reporte_administracion", "md", now),
                md.encode("utf-8"),
            )
        )

    if AREA_PGC in selected:
        data = build_pgc_results(cfg)
        files.append(
            (stamp_filename("reporte_pgc", "md", now), data["md"].encode("utf-8"))
        )
        xlsx = build_workbook(
            data["sheets"],
            report_title="Reporte PGC — tablas",
            stamp_label=data.get("stamp_label") or stamp_filename("reporte_pgc", "xlsx", now),
        )
        files.append((stamp_filename("reporte_pgc_tablas", "xlsx", now), xlsx))

    if AREA_PGO in selected:
        data = build_pgo_results(cfg)
        files.append(
            (stamp_filename("reporte_pgo", "md", now), data["md"].encode("utf-8"))
        )
        xlsx = build_workbook(
            data["sheets"],
            report_title="Reporte PGO — tablas",
            stamp_label=data.get("stamp_label") or stamp_filename("reporte_pgo", "xlsx", now),
        )
        files.append((stamp_filename("reporte_pgo_tablas", "xlsx", now), xlsx))

    if AREA_RISK in selected:
        data = build_risk_results(cfg)
        files.append(
            (stamp_filename("reporte_briesgo", "md", now), data["md"].encode("utf-8"))
        )
        xlsx = build_workbook(
            data["sheets"],
            report_title="Reporte B. Riesgo — tablas",
            stamp_label=data.get("stamp_label") or stamp_filename("reporte_briesgo", "xlsx", now),
        )
        files.append((stamp_filename("reporte_briesgo_tablas", "xlsx", now), xlsx))

    if len(files) == 1:
        name, content = files[0]
        if name.endswith(".md"):
            ctype = "text/markdown; charset=utf-8"
        else:
            ctype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return name, content, ctype

    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, content in files:
            zf.writestr(name, content)
    zip_name = stamp_filename("reportes_wcg", "zip", now)
    return zip_name, buf.getvalue(), "application/zip"
