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
    average_scored_months,
    months_processed_for_pgo,
    table_total,
)
from pgo.scorecard_explain import explain_concept_row
from pgo.scorecard_footnotes import FootnoteRegistry, weighted_column_total

def _parse_year_param(raw: str | None, default: int) -> int:
    """GET year; tolerate localized forms like ``2,026`` from hidden inputs."""
    if not raw:
        return default
    cleaned = str(raw).strip().replace(",", "").replace(" ", "")
    try:
        return int(cleaned)
    except ValueError:
        digits = "".join(c for c in cleaned if c.isdigit())
        if len(digits) >= 4:
            return int(digits[:4])
        return default


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
    year = _parse_year_param(request.GET.get("year"), years[-1])
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
    processed_months = months_processed_for_pgo(year)

    # Build display rows: each row has label, une (optional), concept_id, table_id, months[1..12], avg
    display_rows: list[dict] = []

    def add_row(label: str, une: str, concept_key: str, table_id: str, getter, label_short: str | None = None):
        scored_months: list[float] = []
        row_cells = []
        for m in range(1, 13):
            cell: CellScore = getter(m)
            row_cells.append(cell)
            if m in processed_months and cell.points is not None:
                scored_months.append(cell.points)
        avg = average_scored_months(scored_months)
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

    _blank_repeated_detail_labels(display_rows)

    table_chunks = chunk_rows(display_rows, 10)

    footnote_registry = FootnoteRegistry()
    matrix_tables = [
        _build_table_matrix(grid, table, year, footnote_registry, processed_months)
        for table in PGO_TABLES
    ]
    footnote_registry.ref("weighted_corner")
    global_footnotes = footnote_registry.as_list()

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
            "processed_months": processed_months,
            "show_help": show_help,
            "help_pdf_url": request.build_absolute_uri(static("pgo/PGO-referencia.pdf")),
            "breadcrumbs": [
                {"label": "Panel principal", "url": "/panel/"},
                {"label": "PGO", "url": "/pgo/"},
                {"label": "Tablero por puntos"},
            ],
        },
    )


def _blank_repeated_detail_labels(rows: list[dict]) -> None:
    """Detalle filtrado: no repetir Concepto/UNE en filas consecutivas iguales."""
    prev_concept_key: str | None = None
    prev_une: str | None = None
    for row in rows:
        ck = row["concept_key"]
        une = row["une"]
        row["show_concept"] = ck != prev_concept_key
        row["show_une"] = une != prev_une
        prev_concept_key = ck
        prev_une = une


def _build_table_matrix(
    grid,
    table,
    year: int,
    footnote_registry: FootnoteRegistry,
    processed_months: frozenset[int],
) -> dict:
    """Matriz concepto × UNE; total fila y esquina = suma ponderada (fila Pesos); total columna = suma."""
    rows = []
    une_order = list(UNE_CODES)
    weights = [table.area_weights.get(u, "") for u in une_order]

    for concept in table.concepts:
        row_cells = []
        for une in une_order:
            if une not in concept.max_points:
                row_cells.append(None)
                continue
            scored: list[float] = []
            for m in range(1, 13):
                if m not in processed_months:
                    continue
                pts = grid.get(year, m, une, concept.id).points
                if pts is not None:
                    scored.append(pts)
            avg = average_scored_months(scored)
            row_cells.append(avg)
        row_total = weighted_column_total(row_cells, weights)
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

    corner = weighted_column_total(footer, weights)

    return {
        "title": table.title,
        "table_id": table.id,
        "rows": rows,
        "footer": footer,
        "corner": corner,
        "weights": weights,
    }


@login_required
def ayuda_pgo_pdf(request):
    static_pdf = Path(settings.BASE_DIR) / "static" / "pgo" / "PGO-referencia.pdf"
    pdf = static_pdf if static_pdf.is_file() else Path(settings.BASE_DIR).parent / "data" / "ref" / "PGO-.pdf"
    if not pdf.is_file():
        raise Http404("PGO-.pdf no encontrado")
    return FileResponse(pdf.open("rb"), content_type="application/pdf", filename="PGO-referencia.pdf")
