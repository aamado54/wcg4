"""Vistas capturas manuales PGO."""

from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from pgo.capturas_catalog import (
    PENDING_FOOTNOTES,
    captura_type_or_404,
    concept_labels_for,
    index_by_area,
)
from pgo.capturas_forms import (
    LegalContratosAcreedoresForm,
    LegalGarantiasRegistroForm,
    OpCronogramaProyectosForm,
    OpReportesPgcPgo7Form,
    TiBackupNasForm,
    TiCronogramaProyectosForm,
)
from pgo.capturas_services import (
    business_hours_message,
    default_period,
    is_out_of_period,
    is_within_business_hours,
    latest_version,
    period_from_request,
    permission_denied_message,
    suggested_report_dates,
    user_can_capture,
    version_history,
)
from pgo.models import PgoManualCaptureVersion

FORM_BY_SLUG = {
    "legal_garantias_registro": LegalGarantiasRegistroForm,
    "legal_contratos_acreedores_15d": LegalContratosAcreedoresForm,
    "op_cronograma_proyectos": OpCronogramaProyectosForm,
    "op_reportes_pgc_pgo_7": OpReportesPgcPgo7Form,
    "ti_cronograma_proyectos": TiCronogramaProyectosForm,
    "ti_backup_nas": TiBackupNasForm,
}

BREADCRUMB_ROOT = [
    {"label": "Panel principal", "url": "/panel/"},
    {"label": "PGO", "url": "/pgo/"},
    {"label": "Capturas manuales", "url": "/pgo/capturas/"},
]


def _period_initial(year: int, month: int) -> dict:
    return {"period_year": year, "period_month": month}


def _hydrate_form_from_payload(form_cls, payload: dict, year: int, month: int):
    initial = _period_initial(year, month)
    if form_cls is OpCronogramaProyectosForm:
        for code, val in (payload.get("entries") or {}).items():
            initial[f"cumple_{code}"] = val
    elif form_cls is TiCronogramaProyectosForm:
        for k, v in payload.items():
            if k.startswith("pct_"):
                initial[k] = v
    elif form_cls is TiBackupNasForm:
        for k in ("quarter", "areas_implemented", "backup_nas_done", "notes"):
            if k in payload:
                initial[k] = payload[k]
    elif form_cls is LegalGarantiasRegistroForm:
        for k, v in payload.items():
            if k in form_cls.base_fields:
                initial[k] = v
    elif form_cls is LegalContratosAcreedoresForm:
        lines = payload.get("lines") or []
        if lines:
            line = lines[0]
            initial.update(
                {
                    "creditor_name": line.get("creditor_name"),
                    "due_date": line.get("due_date"),
                    "formalized": line.get("formalized"),
                    "date_done": line.get("date_done"),
                    "notes": line.get("notes"),
                }
            )
    return initial


@login_required
def capturas_index(request):
    cy, cm = default_period()
    areas = []
    for area_id, area_label, items in index_by_area():
        rows = [(c, concept_labels_for(c)) for c in items]
        areas.append((area_id, area_label, rows))
    return render(
        request,
        "pgo/capturas/index.html",
        {
            "areas": areas,
            "pending_footnotes": PENDING_FOOTNOTES,
            "default_year": cy,
            "default_month": cm,
            "breadcrumbs": BREADCRUMB_ROOT,
        },
    )


@login_required
def capturas_page(request, slug: str):
    """Entrada única por tipo: formulario, stub o pendiente."""
    ctype = captura_type_or_404(slug)
    if not ctype:
        raise Http404
    if ctype.implemented and slug in FORM_BY_SLUG:
        return capturas_capture(request, slug)
    if slug == "legal_titulos_inversion":
        return capturas_stub(request, slug)
    if not ctype.implemented:
        return capturas_stub(request, slug)
    raise Http404


@login_required
def capturas_stub(request, slug: str):
    ctype = captura_type_or_404(slug)
    if not ctype:
        raise Http404
    year, month = period_from_request(request)
    latest = latest_version(slug, year, month)
    ctx = {
        "ctype": ctype,
        "concept_labels": concept_labels_for(ctype),
        "year": year,
        "month": month,
        "latest": latest,
        "breadcrumbs": BREADCRUMB_ROOT + [{"label": ctype.title}],
    }
    if slug == "legal_titulos_inversion":
        return render(request, "pgo/capturas/legal_titulos_inversion.html", ctx)
    if not ctype.implemented:
        return render(request, "pgo/capturas/pending.html", ctx)
    raise Http404


@login_required
def capturas_capture(request, slug: str):
    ctype = captura_type_or_404(slug)
    form_cls = FORM_BY_SLUG.get(slug)
    if not ctype or not form_cls or not ctype.implemented:
        raise Http404

    if not user_can_capture(slug, request.user):
        return HttpResponseForbidden(permission_denied_message(slug))

    year, month = period_from_request(request)
    latest = latest_version(slug, year, month)
    suggested = suggested_report_dates(year, month) if slug == "op_reportes_pgc_pgo_7" else {}

    if request.method == "POST":
        if not is_within_business_hours():
            messages.error(request, business_hours_message())
            return redirect(request.path + f"?year={year}&month={month}")

        if slug == "op_reportes_pgc_pgo_7":
            initial_rows = {}
            if latest and latest.payload.get("reports"):
                initial_rows = {r["key"]: r for r in latest.payload["reports"]}
            form = OpReportesPgcPgo7Form(suggested, initial_rows, request.POST)
        elif slug == "legal_garantias_registro":
            form = LegalGarantiasRegistroForm(request.POST, request.FILES)
        else:
            form = form_cls(request.POST)

        if form.is_valid():
            py = int(form.cleaned_data["period_year"])
            pm = int(form.cleaned_data["period_month"])
            oop = is_out_of_period(py, pm)
            if slug == "op_reportes_pgc_pgo_7":
                payload = form.to_payload(suggested)
            else:
                payload = form.to_payload()
            version = PgoManualCaptureVersion(
                capture_type=slug,
                period_year=py,
                period_month=pm,
                user=request.user,
                payload=payload,
                change_note=form.cleaned_data.get("change_note") or "",
                is_out_of_period=oop,
            )
            if slug == "legal_garantias_registro":
                version.attachment = form.cleaned_data.get("attachment")
            version.save()
            if oop:
                messages.warning(
                    request,
                    "Guardado fuera del período calendario actual (marcado is_out_of_period).",
                )
            else:
                messages.success(request, "Captura guardada (nueva versión).")
            return redirect("pgo:capturas_history", slug=slug)
    else:
        initial = _period_initial(year, month)
        if latest:
            initial.update(_hydrate_form_from_payload(form_cls, latest.payload, year, month))
        if slug == "op_reportes_pgc_pgo_7":
            initial_rows = {}
            if latest and latest.payload.get("reports"):
                initial_rows = {r["key"]: r for r in latest.payload["reports"]}
            form = OpReportesPgcPgo7Form(suggested, initial_rows, initial=initial)
        else:
            form = form_cls(initial=initial)

    extra = {}
    if slug == "op_reportes_pgc_pgo_7" and hasattr(form, "report_rows"):
        extra["report_table"] = [
            {
                "key": key,
                "label": label,
                "suggested": suggested.get(key),
                "completion": form[f"completion_{key}"],
                "notes": form[f"notes_{key}"],
            }
            for key, label in form.report_rows
        ]

    return render(
        request,
        f"pgo/capturas/form_{slug}.html",
        {
            "ctype": ctype,
            "form": form,
            "year": year,
            "month": month,
            "latest": latest,
            "suggested": suggested,
            "concept_labels": concept_labels_for(ctype),
            "business_hours_ok": is_within_business_hours(),
            "business_hours_message": business_hours_message(),
            "breadcrumbs": BREADCRUMB_ROOT + [{"label": ctype.title}],
            **extra,
        },
    )


@login_required
def capturas_history(request, slug: str):
    ctype = captura_type_or_404(slug)
    if not ctype:
        raise Http404
    year_raw = request.GET.get("year")
    month_raw = request.GET.get("month")
    year = int(year_raw) if year_raw else None
    month = int(month_raw) if month_raw else None
    versions = version_history(slug, year, month)[:200]
    return render(
        request,
        "pgo/capturas/history.html",
        {
            "ctype": ctype,
            "versions": versions,
            "filter_year": year,
            "filter_month": month,
            "breadcrumbs": BREADCRUMB_ROOT
            + [{"label": ctype.title, "url": f"/pgo/capturas/{slug}/"}, {"label": "Historial"}],
        },
    )


@login_required
def capturas_version_detail(request, slug: str, version_id: int):
    ctype = captura_type_or_404(slug)
    if not ctype:
        raise Http404
    version = get_object_or_404(PgoManualCaptureVersion, pk=version_id, capture_type=slug)
    return render(
        request,
        "pgo/capturas/version_detail.html",
        {
            "ctype": ctype,
            "version": version,
            "breadcrumbs": BREADCRUMB_ROOT
            + [
                {"label": ctype.title, "url": f"/pgo/capturas/{slug}/"},
                {"label": f"Versión {version.created_at:%d/%m/%Y %H:%M}"},
            ],
        },
    )
