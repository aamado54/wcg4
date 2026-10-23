"""Vista tablero por puntos PGO con filtros."""

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import render
from django.templatetags.static import static

from pgo.scorecard_catalog import (
    PGO_TABLES,
    UNE_CODES,
    UNE_LABELS,
    all_concepts,
    concept_short_label,
    table_by_id,
)
from pgo.scorecard_engine import (
    CellScore,
    build_score_grid,
    chunk_rows,
    month_average,
    table_total,
)
from pgo.scorecard_explain import (
    concept_by_id,
    explain_concept_row,
    explain_total_row,
)

MONTH_LABELS = [
    "Ene",
    "Feb",
    "Mar",
    "Abr",
    "May",
    "Jun",
    "Jul",
    "Ago",
    "Sep",
    "Oct",
    "Nov",
    "Dic",
]


def _concept_choices():
    choices = []
    for table in PGO_TABLES:
        choices.append(
            {
                "id": f"total:{table.id}",
                "label": f"TOTAL — {table.title}",
                "table_id": table.id,
                "is_total": True,
            }
        )
        for c in table.concepts:
            choices.append(
                {
                    "id": c.id,
                    "label": c.label,
                    "table_id": table.id,
                    "category": c.category,
                    "is_total": False,
                }
            )
    return choices


@login_required
def tablero_puntos(request):
    grid = build_score_grid()
    years = sorted(y for y in grid.cells.keys() if y >= 2026) or [2026]
    year = int(request.GET.get("year") or years[-1])
    if year not in years:
        year = years[-1]

    selected_unes = request.GET.getlist("une") or list(UNE_CODES)
    selected_unes = [u for u in selected_unes if u in UNE_CODES]
    if not selected_unes:
        selected_unes = list(UNE_CODES)

    all_choices = _concept_choices()
    selected_concepts = request.GET.getlist("concept")
    if not selected_concepts:
        selected_concepts = [c["id"] for c in all_choices if c["is_total"]]

    group_by = request.GET.get("group_by", "concept")
    if group_by not in ("concept", "une"):
        group_by = "concept"

    show_help = request.GET.get("help") == "1"

    # Build display rows: each row has label, une (optional), concept_id, table_id, months[1..12], avg
    display_rows: list[dict] = []

    def add_row(label: str, une: str, concept_key: str, table_id: str, getter, label_short: str | None = None):
        months_vals = []
        row_cells = []
        for m in range(1, 13):
            cell: CellScore = getter(m)
            months_vals.append(cell.points)
            row_cells.append(cell)
        avg = month_average(months_vals)
        row_info = _row_info_for_key(concept_key, une, year, grid)
        display_rows.append(
            {
                "label": label,
                "label_short": label_short or label[:40],
                "une": une,
                "une_label": UNE_LABELS.get(une, une),
                "concept_key": concept_key,
                "table_id": table_id,
                "months": row_cells,
                "average": avg,
                "row_info": row_info,
            }
        )

    for concept_sel in selected_concepts:
        if concept_sel.startswith("total:"):
            table_id = concept_sel.split(":", 1)[1]
            table = table_by_id(table_id)
            if not table:
                continue
            if group_by == "concept":
                for une in selected_unes:
                    add_row(
                        f"TOTAL — {table.title}",
                        une,
                        concept_sel,
                        table_id,
                        lambda m, u=une, tid=table_id: table_total(grid, tid, year, m, u),
                        label_short=f"TOTAL {table.title}",
                    )
            else:
                for une in selected_unes:
                    add_row(
                        f"TOTAL — {table.title}",
                        une,
                        concept_sel,
                        table_id,
                        lambda m, u=une, tid=table_id: table_total(grid, tid, year, m, u),
                        label_short=f"TOTAL {table.title}",
                    )
        else:
            concept = next((c for c in all_concepts() if c.id == concept_sel), None)
            if not concept:
                continue
            if group_by == "concept":
                for une in selected_unes:
                    if une not in concept.max_points:
                        continue
                    add_row(
                        concept.label,
                        une,
                        concept.id,
                        concept.table_id,
                        lambda m, u=une, c=concept: grid.get(year, m, u, c.id),
                        label_short=concept_short_label(concept),
                    )
            else:
                for une in selected_unes:
                    if une not in concept.max_points:
                        continue
                    add_row(
                        concept.label,
                        une,
                        concept.id,
                        concept.table_id,
                        lambda m, u=une, c=concept: grid.get(year, m, u, c.id),
                        label_short=concept_short_label(concept),
                    )

    if group_by == "une":
        display_rows.sort(key=lambda r: (r["une"], r["table_id"], r["label"]))
    else:
        display_rows.sort(key=lambda r: (r["table_id"], r["concept_key"], r["une"]))

    table_chunks = chunk_rows(display_rows, 10)

    matrix_tables = [_build_table_matrix(grid, table, year) for table in PGO_TABLES]
    detail_month_totals = _detail_month_column_totals(grid, year, selected_unes)
    detail_month_avg = month_average(detail_month_totals)

    # Resumen calculable vs no
    summary_notes = _build_data_summary(grid, year)

    return render(
        request,
        "pgo/pgotableropuntos.html",
        {
            "years": years,
            "year": year,
            "show_year_picker": len(years) > 1,
            "une_codes": UNE_CODES,
            "une_labels": UNE_LABELS,
            "une_options": [(c, UNE_LABELS[c]) for c in UNE_CODES],
            "selected_unes": selected_unes,
            "concept_choices": all_choices,
            "selected_concepts": selected_concepts,
            "group_by": group_by,
            "month_labels": MONTH_LABELS,
            "table_chunks": table_chunks,
            "matrix_tables": matrix_tables,
            "detail_month_totals": detail_month_totals,
            "detail_month_avg": detail_month_avg,
            "summary_notes": summary_notes,
            "show_help": show_help,
            "help_pdf_url": request.build_absolute_uri(static("pgo/PGO-referencia.pdf")),
            "breadcrumbs": [
                {"label": "Panel principal", "url": "/panel/"},
                {"label": "PGO", "url": "/pgo/"},
                {"label": "Tablero por puntos"},
            ],
        },
    )


def _row_info_for_key(concept_key: str, une: str, year: int, grid: ScoreGrid):
    if concept_key.startswith("total:"):
        return explain_total_row(concept_key.split(":", 1)[1], year, grid, une)
    concept = concept_by_id(concept_key)
    if not concept:
        from pgo.scorecard_explain import RowInfo

        return RowInfo("red", "Concepto desconocido.")
    return explain_concept_row(concept, year, grid, une=une)


def _row_total_footnote_text(year: int, total: float | None) -> str:
    if total is None:
        return "Sin total calculable (ningún promedio mensual con dato en UNE aplicables)."
    return (
        f"Total fila {total:.1f} pts — suma de los promedios mensuales {year} "
        "en cada UNE donde aplica el concepto. Se recalcula al cambiar cualquier celda del concepto."
    )


def _build_table_matrix(grid, table, year: int) -> dict:
    """Matriz completa concepto × UNE; total columna = suma exacta de la columna."""
    rows = []
    une_order = list(UNE_CODES)
    footnotes: list[dict] = []
    note_idx = 0

    for concept in table.concepts:
        row_cells = []
        row_vals = []
        for une in une_order:
            if une not in concept.max_points:
                row_cells.append(None)
                continue
            monthly = [grid.get(year, m, une, concept.id).points for m in range(1, 13)]
            avg = month_average(monthly)
            row_cells.append(avg)
            if avg is not None:
                row_vals.append(avg)
        row_total = sum(row_vals) if row_vals else None
        note_idx += 1
        footnotes.append(
            {
                "num": note_idx,
                "text": _row_total_footnote_text(year, row_total),
            }
        )
        rows.append(
            {
                "label": concept.label,
                "label_short": concept_short_label(concept),
                "concept_id": concept.id,
                "cells": row_cells,
                "row_total": row_total,
                "note_ref": f"n.{note_idx}",
                "row_info": explain_concept_row(concept, year, grid, une=None),
            }
        )

    footer = []
    for col_i, _une in enumerate(une_order):
        col_sum = 0.0
        any_val = False
        for row in rows:
            val = row["cells"][col_i]
            if val is not None:
                col_sum += val
                any_val = True
        footer.append(col_sum if any_val else None)

    corner_sum = sum(v for v in footer if v is not None)
    corner = corner_sum if any(v is not None for v in footer) else None

    weights = [table.area_weights.get(u, "") for u in une_order]

    return {
        "title": table.title,
        "table_id": table.id,
        "rows": rows,
        "footnotes": footnotes,
        "footer": footer,
        "corner": corner,
        "weights": weights,
        "is_full_table": True,
    }


def _detail_month_column_totals(grid: ScoreGrid, year: int, unes: list[str]) -> list[float | None]:
    """Totales por mes (todas las filas PGO × UNE seleccionadas); fijos al filtrar conceptos."""
    totals: list[float | None] = []
    for month in range(1, 13):
        col_sum = 0.0
        any_val = False
        for concept in all_concepts():
            for une in unes:
                if une not in concept.max_points:
                    continue
                pts = grid.get(year, month, une, concept.id).points
                if pts is not None:
                    col_sum += pts
                    any_val = True
        totals.append(col_sum if any_val else None)
    return totals


def _build_data_summary(grid, year: int) -> list[dict]:
    """Notas para el usuario sobre qué se puede calcular hoy."""
    from pgo.scorecard_catalog import all_concepts

    lines = []
    for c in all_concepts():
        sample = None
        for m in range(1, 13):
            for une in UNE_CODES:
                if une not in c.max_points:
                    continue
                cell = grid.get(year, m, une, c.id)
                if cell.points is not None:
                    sample = cell
                    break
            if sample:
                break
        if sample and sample.confidence in ("high", "low"):
            lines.append(
                {
                    "concept": c.label,
                    "status": "parcial" if sample.confidence == "low" else "calculable",
                    "note": sample.note,
                }
            )
        else:
            lines.append(
                {
                    "concept": c.label,
                    "status": "sin_dato",
                    "note": sample.note if sample else "Sin fuente en sistema",
                }
            )
    return lines


@login_required
def ayuda_pgo_pdf(request):
    static_pdf = Path(settings.BASE_DIR) / "static" / "pgo" / "PGO-referencia.pdf"
    pdf = static_pdf if static_pdf.is_file() else Path(settings.BASE_DIR).parent / "data" / "ref" / "PGO-.pdf"
    if not pdf.is_file():
        raise Http404("PGO-.pdf no encontrado")
    return FileResponse(pdf.open("rb"), content_type="application/pdf", filename="PGO-referencia.pdf")
