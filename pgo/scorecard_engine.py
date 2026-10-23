"""Cálculo de puntajes PGO por año/mes/UNE (heurísticas sobre datos existentes)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Literal

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from core.models import MetricDefinition, UNE
from pgc.models import MonthlyMetricResult
from imports.models import FileUpload, InvestmentGrowthRow
from pgo.models import Ticket
from pgo.scorecard_catalog import PGO_TABLES, PgoConcept, UNE_CODES, all_concepts, table_by_id

Confidence = Literal["high", "low", "none"]


@dataclass
class CellScore:
    points: float | None
    max_points: float
    confidence: Confidence = "none"
    note: str = ""

    @property
    def display(self) -> str:
        if self.points is None:
            return "—"
        return f"{self.points:g}"


@dataclass
class ScoreGrid:
    """year -> month (1-12) -> une -> concept_id -> CellScore"""

    cells: dict[int, dict[int, dict[str, dict[str, CellScore]]]] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def get(self, year: int, month: int, une: str, concept_id: str) -> CellScore:
        return (
            self.cells.get(year, {})
            .get(month, {})
            .get(une, {})
            .get(
                concept_id,
                CellScore(points=None, max_points=0, confidence="none", note="Sin cálculo"),
            )
        )


def _financiero_periods() -> set[str]:
    seed = Path(settings.BASE_DIR) / "risk" / "financiero" / "seed" / "combined_full.json"
    if not seed.is_file():
        return set()
    data = json.loads(seed.read_text(encoding="utf-8"))
    return set(data.get("periods") or [])


def months_processed_for_pgo(year: int) -> frozenset[int]:
    """Meses con cierre operativo cargado (p. ej. EEFF en seed); el resto queda en blanco en tablero."""
    months: set[int] = set()
    prefix = f"{year}-"
    for period in _financiero_periods():
        if not period.startswith(prefix) or len(period) < 7:
            continue
        try:
            months.add(int(period[5:7]))
        except ValueError:
            continue
    return frozenset(months)


def _financiero_kpi_month(period: str, bu: str) -> bool:
    """bu: F,L,I,S en seed."""
    seed = Path(settings.BASE_DIR) / "risk" / "financiero" / "seed" / "combined_full.json"
    if not seed.is_file():
        return False
    data = json.loads(seed.read_text(encoding="utf-8"))
    if period not in data.get("periods", []):
        return False
    kpis = data.get("kpis", {}).get(bu, {}).get(period, {})
    return bool(kpis.get("activo_corriente") or kpis.get("utilidades"))


_BU_MAP = {
    "FACTORING": "F",
    "LEASING": "L",
    "INVESTMENT": "I",
    "INSURANCE": "S",
}


def _ingresos_imported(year: int, month: int, une_code: str) -> bool:
    une = UNE.objects.filter(code=une_code).first()
    if not une:
        return False
    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
    if not metric:
        return False
    return MonthlyMetricResult.objects.filter(
        year=year, month=month, une=une, metric=metric
    ).exists()


def _inversiones_month(year: int, month: int) -> bool:
    return InvestmentGrowthRow.objects.filter(year=year, month=month).exists()


def _file_upload_in_month(year: int, month: int, types: tuple[str, ...]) -> bool:
    start = timezone.make_aware(datetime(year, month, 1))
    if month == 12:
        end = timezone.make_aware(datetime(year + 1, 1, 1))
    else:
        end = timezone.make_aware(datetime(year, month + 1, 1))
    return FileUpload.objects.filter(
        file_type_detected__in=types,
        created_at__gte=start,
        created_at__lt=end,
    ).exists()


def _open_tickets_at_month_end(year: int, month: int) -> int:
    """Tickets no cerrados con apertura hasta fin de mes (aprox.)."""
    if month == 12:
        end = timezone.make_aware(datetime(year, 12, 31, 23, 59, 59))
    else:
        from calendar import monthrange

        last = monthrange(year, month)[1]
        end = timezone.make_aware(datetime(year, month, last, 23, 59, 59))
    qs = Ticket.objects.filter(fecha_apertura__lte=end).filter(
        Q(fecha_cierre__isnull=True) | Q(fecha_cierre__gt=end)
    )
    return qs.count()


def _set_cell(grid: ScoreGrid, year: int, month: int, une: str, concept: PgoConcept, cell: CellScore):
    grid.cells.setdefault(year, {}).setdefault(month, {}).setdefault(une, {})[concept.id] = cell


def _full_or_zero(ok: bool, max_pts: float, note_ok: str, note_fail: str, confidence: Confidence):
    if ok:
        return CellScore(points=max_pts, max_points=max_pts, confidence=confidence, note=note_ok)
    return CellScore(points=0.0, max_points=max_pts, confidence=confidence, note=note_fail)


def compute_concept_month(
    concept: PgoConcept, year: int, month: int, une: str, grid: ScoreGrid
) -> CellScore:
    max_pts = float(concept.max_points.get(une, 0))
    if max_pts <= 0:
        return CellScore(points=None, max_points=0, confidence="none", note="N/A en plantilla")

    period = f"{year}-{month:02d}"
    cid = concept.id

    if cid in ("fr_eeff_integraciones", "fr_carga_analitica"):
        bu = _BU_MAP.get(une)
        has_eeff = _financiero_kpi_month(period, bu) if bu else False
        has_ing = _ingresos_imported(year, month, une)
        if cid == "fr_eeff_integraciones":
            return _full_or_zero(
                has_eeff,
                max_pts,
                f"EEFF gerencial {period} con KPI {bu}",
                f"Sin EEFF consolidado para {period} / {une}",
                "high" if has_eeff else "low",
            )
        ok = has_eeff and (has_ing or une in ("INVESTMENT", "INSURANCE"))
        if une in ("INVESTMENT", "INSURANCE"):
            ok = has_eeff or _inversiones_month(year, month)
        return _full_or_zero(
            ok,
            max_pts,
            "Carga analítica inferida (EEFF ± ingresos/inversiones)",
            "Faltan EEFF o ingresos operativos del mes",
            "low",
        )

    if cid == "op_reportes_pgc_pgo_7":
        has_fin = period in _financiero_periods()
        has_clients = FileUpload.objects.filter(
            file_type_detected=FileUpload.TYPE_NEW_CLIENTS,
            created_at__year=year,
            created_at__month=month,
        ).exists()
        ok = has_fin and (has_clients or month <= 6)
        return _full_or_zero(
            ok,
            max_pts,
            "Proxy: EEFF seed + actividad imports del mes",
            "Sin evidencia de cierre PGC/PGO en imports",
            "low",
        )

    if cid == "ti_reportes_7":
        ok = _file_upload_in_month(
            year,
            month,
            (FileUpload.TYPE_FINANCIAL, FileUpload.TYPE_INVESTMENT_GROWTH, FileUpload.TYPE_NEW_CLIENTS),
        )
        return _full_or_zero(
            ok,
            max_pts,
            "Proxy: al menos un archivo operativo importado en el mes",
            "Sin imports detectados en el mes",
            "low",
        )

    if cid == "ti_max_5_tickets":
        n = _open_tickets_at_month_end(year, month)
        if not Ticket.objects.exists():
            return CellScore(
                points=None,
                max_points=max_pts,
                confidence="none",
                note="Sin tickets en BD (importar helpdesk)",
            )
        ok = n <= 5
        pts = max_pts if ok else 0.0
        return CellScore(
            points=pts,
            max_points=max_pts,
            confidence="low",
            note=(
                f"{n} tickets abiertos al cierre (mismo conteo replicado en las 4 UNE; "
                "helpdesk no discrimina UNE PGO)"
            ),
        )

    if cid == "ti_backup_nas":
        ok = month in (3, 6, 9, 12)
        return _full_or_zero(
            ok,
            max_pts,
            "Trimestre natural: asumido cumplido sin evidencia NAS",
            "Mes fuera de trimestre MAR/JUN/SEP/DIC",
            "low",
        )

    return CellScore(
        points=None,
        max_points=max_pts,
        confidence="none",
        note="Sin fuente automatizada (Planner, SharePoint, cronograma CEO, etc.)",
    )


def build_score_grid(years: list[int] | None = None) -> ScoreGrid:
    grid = ScoreGrid()
    if years is None:
        years = _detect_years()
    for year in years:
        for month in range(1, 13):
            for concept in all_concepts():
                for une in UNE_CODES:
                    if une not in concept.max_points:
                        continue
                    cell = compute_concept_month(concept, year, month, une, grid)
                    _set_cell(grid, year, month, une, concept, cell)
    return grid


def _detect_years() -> list[int]:
    years = set()
    for p in _financiero_periods():
        if len(p) >= 7 and p[4] == "-":
            try:
                years.add(int(p[:4]))
            except ValueError:
                pass
    for t in Ticket.objects.dates("fecha_apertura", "year"):
        years.add(t.year)
    if not years:
        years.add(timezone.localdate().year)
    return sorted(y for y in years if y >= 2026)


def table_total(
    grid: ScoreGrid, table_id: str, year: int, month: int, une: str
) -> CellScore:
    table = table_by_id(table_id)
    if not table:
        return CellScore(points=None, max_points=0)
    pts = 0.0
    mx = 0.0
    any_val = False
    for c in table.concepts:
        if une not in c.max_points:
            continue
        cell = grid.get(year, month, une, c.id)
        if cell.points is not None:
            pts += cell.points
            any_val = True
        mx += cell.max_points
    if not any_val and mx == 0:
        return CellScore(points=None, max_points=0, note="N/A")
    return CellScore(
        points=pts if any_val else None,
        max_points=mx,
        confidence="low",
        note="Suma de conceptos con dato en el mes",
    )


def month_average(values: list[float | None]) -> float | None:
    nums = [v for v in values if v is not None]
    if not nums:
        return None
    return sum(nums) / len(nums)


def average_scored_months(points: list[float]) -> float | None:
    """Promedio solo sobre meses con puntaje (lista ya filtrada)."""
    if not points:
        return None
    return sum(points) / len(points)


def chunk_rows(rows: list, size: int = 10) -> list[list]:
    return [rows[i : i + size] for i in range(0, len(rows), size)] or [[]]
