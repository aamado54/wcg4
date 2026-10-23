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
from pgo.scorecard_explain import explain_concept_row
from pgo.scorecard_footnotes import FootnoteRegistry, weighted_column_total

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

    footnote_registry = FootnoteRegistry()
    matrix_tables = [
        _build_table_matrix(grid, table, year, footnote_registry) for table in PGO_TABLES
    ]
    footnote_registry.ref("weighted_corner")
    global_footnotes = footnote_registry.as_list()
    detail_month_totals = _detail_month_column_totals(grid, year, selected_unes)
    detail_month_avg = month_average(detail_month_totals)

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
            "global_footnotes": global_footnotes,
            "detail_month_totals": detail_month_totals,
            "detail_month_avg": detail_month_avg,
            "show_help": show_help,
            "help_pdf_url": request.build_absolute_uri(static("pgo/PGO-referencia.pdf")),
            "breadcrumbs": [
                {"label": "Panel principal", "url": "/panel/"},
                {"label": "PGO", "url": "/pgo/"},
                {"label": "Tablero por puntos"},
            ],
        },
    )


def _une_concept_points_sum(table, une: str) -> float:
    return float(
        sum(c.max_points[une] for c in table.concepts if une in c.max_points)
    )


def _scale_matrix_to_une_totals(table, rows: list[dict], footer: list, une_order: list[str]) -> None:
    """Escala columnas al TOTAL oficial PGO por UNE (p. ej. Operaciones 90→100)."""
    if not table.une_total_points:
        return
    for col_i, une in enumerate(une_order):
        cap = table.une_total_points.get(une)
        if not cap:
            continue
        raw_sum = _une_concept_points_sum(table, une)
        if raw_sum <= 0 or raw_sum == cap:
            continue
        factor = cap / raw_sum
        for row in rows:
            val = row["cells"][col_i]
            if val is not None:
                row["cells"][col_i] = val * factor
        if footer[col_i] is not None:
            footer[col_i] = footer[col_i] * factor
    for row in rows:
        row_vals = [v for v in row["cells"] if v is not None]
        row["row_total"] = sum(row_vals) if row_vals else None


def _build_table_matrix(
    grid, table, year: int, footnote_registry: FootnoteRegistry
) -> dict:
    """Matriz completa concepto × UNE; total columna = suma; esquina = suma ponderada."""
    rows = []
    une_order = list(UNE_CODES)

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
        note_key = "row_no_total" if row_total is None else "row_has_total"
        note_ref = footnote_registry.ref(note_key)
        detail = explain_concept_row(concept, year, grid, une=None)
        rows.append(
            {
                "label": concept.label,
                "label_short": concept_short_label(concept),
                "concept_id": concept.id,
                "cells": row_cells,
                "row_total": row_total,
                "note_ref": note_ref,
                "detail_title": concept.label,
                "detail_body": detail.body,
                "detail_clickable": bool((detail.body or "").strip()),
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

    _scale_matrix_to_une_totals(table, rows, footer, une_order)

    weights = [table.area_weights.get(u, "") for u in une_order]
    corner = weighted_column_total(footer, weights)

    return {
        "title": table.title,
        "table_id": table.id,
        "rows": rows,
        "footer": footer,
        "corner": corner,
        "weights": weights,
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


@login_required
def ayuda_pgo_pdf(request):
    static_pdf = Path(settings.BASE_DIR) / "static" / "pgo" / "PGO-referencia.pdf"
    pdf = static_pdf if static_pdf.is_file() else Path(settings.BASE_DIR).parent / "data" / "ref" / "PGO-.pdf"
    if not pdf.is_file():
        raise Http404("PGO-.pdf no encontrado")
    return FileResponse(pdf.open("rb"), content_type="application/pdf", filename="PGO-referencia.pdf")
