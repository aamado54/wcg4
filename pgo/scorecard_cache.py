"""Persistencia del tablero PGO por puntos (snapshot en BD + huella de fuentes)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from imports.models import FileUpload, InvestmentGrowthRow
from pgc.models import MonthlyMetricResult
from pgo.models import PgoArchivoRegistro, PgoExpediente, PgoScorecardCacheMeta, PgoScorecardCell, Ticket
from pgo.scorecard_engine import CellScore, ScoreGrid, build_score_grid, months_processed_for_pgo


META_PK = 1


def _financiero_seed_stat() -> str:
    seed = Path(settings.BASE_DIR) / "risk" / "financiero" / "seed" / "combined_full.json"
    if not seed.is_file():
        return "seed:missing"
    st = seed.stat()
    return f"seed:{st.st_mtime_ns}:{st.st_size}"


def _agg_stamp(model, field: str = "updated_at") -> str:
    agg = model.objects.aggregate(m=Max(field))
    m = agg["m"]
    n = model.objects.count()
    return f"{model._meta.label_lower}:{n}:{m!s}"


def compute_data_fingerprint() -> str:
    """Huella de todas las fuentes que alimentan el scorecard."""
    parts = [
        _financiero_seed_stat(),
        _agg_stamp(PgoArchivoRegistro),
        _agg_stamp(PgoExpediente),
        _agg_stamp(Ticket, "fecha_apertura"),
        _agg_stamp(Ticket, "fecha_cierre"),
        _agg_stamp(InvestmentGrowthRow),
        _agg_stamp(FileUpload),
        _agg_stamp(MonthlyMetricResult),
    ]
    digest = hashlib.sha256("|".join(parts).encode()).hexdigest()
    return digest[:40]


def get_cache_meta() -> PgoScorecardCacheMeta | None:
    return PgoScorecardCacheMeta.objects.filter(pk=META_PK).first()


def processed_months_for_display(year: int) -> frozenset[int]:
    meta = get_cache_meta()
    if meta and meta.processed_months:
        raw = meta.processed_months.get(str(year))
        if raw is not None:
            return frozenset(int(m) for m in raw)
    return months_processed_for_pgo(year)


def _grid_from_cells(cells_qs) -> ScoreGrid:
    grid = ScoreGrid()
    for row in cells_qs.iterator(chunk_size=2000):
        cell = CellScore(
            points=row.points,
            max_points=float(row.max_points),
            confidence=row.confidence,
            note=row.note or "",
        )
        grid.cells.setdefault(row.year, {}).setdefault(row.month, {}).setdefault(row.une, {})[
            row.concept_id
        ] = cell
    return grid


@transaction.atomic
def rebuild_scorecard_cache(years: list[int] | None = None) -> PgoScorecardCacheMeta:
    grid = build_score_grid(years=years)
    years_built = sorted(grid.cells.keys())
    processed: dict[str, list[int]] = {
        str(y): sorted(months_processed_for_pgo(y)) for y in years_built
    }
    fingerprint = compute_data_fingerprint()
    now = timezone.now()

    PgoScorecardCell.objects.all().delete()
    bulk: list[PgoScorecardCell] = []
    for year, by_month in grid.cells.items():
        for month, by_une in by_month.items():
            for une, by_concept in by_une.items():
                for concept_id, cell in by_concept.items():
                    bulk.append(
                        PgoScorecardCell(
                            year=year,
                            month=month,
                            une=une,
                            concept_id=concept_id,
                            points=cell.points,
                            max_points=cell.max_points,
                            confidence=cell.confidence,
                            note=(cell.note or "")[:2000],
                        )
                    )
    PgoScorecardCell.objects.bulk_create(bulk, batch_size=500)

    meta, _created = PgoScorecardCacheMeta.objects.update_or_create(
        pk=META_PK,
        defaults={
            "fingerprint": fingerprint,
            "computed_at": now,
            "years": years_built,
            "processed_months": processed,
        },
    )
    return meta


@dataclass
class LoadedScorecard:
    grid: ScoreGrid
    meta: PgoScorecardCacheMeta
    from_cache: bool


def load_scorecard(years: list[int] | None = None) -> LoadedScorecard:
    """
    Devuelve la cuadrícula persistida si la huella coincide; si no, recalcula y guarda.
    """
    fingerprint = compute_data_fingerprint()
    meta = get_cache_meta()
    if years is None:
        years = meta.years if meta and meta.years else None

    if meta and meta.fingerprint == fingerprint:
        qs = PgoScorecardCell.objects.all()
        if years:
            qs = qs.filter(year__in=years)
        if qs.exists():
            return LoadedScorecard(grid=_grid_from_cells(qs), meta=meta, from_cache=True)

    meta = rebuild_scorecard_cache(years=years)
    qs = PgoScorecardCell.objects.all()
    if years:
        qs = qs.filter(year__in=years)
    return LoadedScorecard(grid=_grid_from_cells(qs), meta=meta, from_cache=False)
