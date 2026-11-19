"""Vistas staff: auditoría de importaciones (quién / cuándo / éxito)."""

from __future__ import annotations

import json
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from core.access import can_access_ops
from imports.audit import audit_summary_counts
from imports.detection import TYPE_LABELS
from imports.models import FileUpload, ImportAuditEvent


def _parse_date_param(value: str, *, end_of_day: bool = False):
    value = (value or "").strip()
    if not value:
        return None
    try:
        dt = datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
    if end_of_day:
        dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    return dt


def _filter_events(request):
    qs = ImportAuditEvent.objects.select_related("user", "file_upload").order_by("-loaded_at")

    import_tipo = (request.GET.get("tipo") or "").strip()
    if import_tipo:
        qs = qs.filter(import_tipo=import_tipo)

    source = (request.GET.get("source") or "").strip()
    if source:
        qs = qs.filter(source=source)

    success_raw = (request.GET.get("success") or "").strip().lower()
    if success_raw in ("ok", "1", "true", "yes"):
        qs = qs.filter(success=True)
    elif success_raw in ("fail", "0", "false", "no"):
        qs = qs.filter(success=False)

    user_id = (request.GET.get("user") or "").strip()
    if user_id.isdigit():
        qs = qs.filter(user_id=int(user_id))

    username = (request.GET.get("username") or "").strip()
    if username:
        qs = qs.filter(Q(user__username__icontains=username))

    date_from = _parse_date_param(request.GET.get("from") or "")
    if date_from:
        qs = qs.filter(loaded_at__gte=date_from)

    date_to = _parse_date_param(request.GET.get("to") or "", end_of_day=True)
    if date_to:
        qs = qs.filter(loaded_at__lte=date_to)

    q = (request.GET.get("q") or "").strip()
    if q:
        qs = qs.filter(
            Q(file_path_key__icontains=q)
            | Q(error_message__icontains=q)
            | Q(import_tipo__icontains=q)
        )

    return qs


def _tipo_choices():
    rows = (
        ImportAuditEvent.objects.exclude(import_tipo="")
        .values("import_tipo")
        .annotate(n=Count("id"))
        .order_by("-n")[:40]
    )
    labels = []
    for row in rows:
        tipo = row["import_tipo"]
        lab = TYPE_LABELS.get(tipo, tipo)
        labels.append((tipo, f"{lab} ({row['n']})"))
    return labels


def _upload_health():
    return {
        "parsed_errors": FileUpload.objects.filter(
            status=FileUpload.STATUS_PARSED_ERROR
        ).count(),
        "pending": FileUpload.objects.filter(status=FileUpload.STATUS_UPLOADED).count(),
    }


@login_required
@user_passes_test(can_access_ops)
def import_audit_list(request):
    """Listado filtrable + resumen tipo checklist."""
    filtered = _filter_events(request)
    summary = audit_summary_counts()
    filtered_total = filtered.count()
    filtered_fail = filtered.filter(success=False).count()
    by_tipo_filtered = list(
        filtered.exclude(import_tipo="")
        .values("import_tipo")
        .annotate(n=Count("id"), fails=Count("id", filter=Q(success=False)))
        .order_by("-n")[:20]
    )
    upload_health = _upload_health()

    paginator = Paginator(filtered, 40)
    page = paginator.get_page(request.GET.get("page"))

    User = get_user_model()
    recent_users = (
        User.objects.filter(import_audit_events__isnull=False)
        .distinct()
        .order_by("username")[:30]
    )

    tipo_labels = {t: TYPE_LABELS.get(t, t) for t in TYPE_LABELS}
    for row in by_tipo_filtered:
        row["label"] = tipo_labels.get(row["import_tipo"], row["import_tipo"])

    return render(
        request,
        "imports/audit_list.html",
        {
            "page": page,
            "summary": summary,
            "filtered_total": filtered_total,
            "filtered_ok": filtered_total - filtered_fail,
            "filtered_fail": filtered_fail,
            "by_tipo": by_tipo_filtered,
            "upload_health": upload_health,
            "tipo_choices": _tipo_choices(),
            "source_choices": ImportAuditEvent.SOURCE_CHOICES,
            "recent_users": recent_users,
            "filters": {
                "tipo": request.GET.get("tipo", ""),
                "source": request.GET.get("source", ""),
                "success": request.GET.get("success", ""),
                "user": request.GET.get("user", ""),
                "username": request.GET.get("username", ""),
                "from": request.GET.get("from", ""),
                "to": request.GET.get("to", ""),
                "q": request.GET.get("q", ""),
            },
            "breadcrumbs": [
                {"label": "Inicio", "url": reverse("portal:home")},
                {"label": "Administración", "url": reverse("imports:import_hub")},
                {"label": "Auditoría de importaciones"},
            ],
        },
    )


@login_required
@user_passes_test(can_access_ops)
def import_audit_detail(request, event_id: int):
    event = get_object_or_404(
        ImportAuditEvent.objects.select_related("user", "file_upload"),
        pk=event_id,
    )
    related = ImportAuditEvent.objects.filter(
        file_path_key=event.file_path_key
    ).exclude(pk=event.pk).select_related("user")[:15]

    tipo_label = TYPE_LABELS.get(event.import_tipo, event.import_tipo or "—")
    detail_json_pretty = json.dumps(event.detail_json or {}, indent=2, ensure_ascii=False)

    return render(
        request,
        "imports/audit_detail.html",
        {
            "event": event,
            "tipo_label": tipo_label,
            "detail_json_pretty": detail_json_pretty,
            "related": related,
            "breadcrumbs": [
                {"label": "Inicio", "url": reverse("portal:home")},
                {"label": "Importación", "url": reverse("imports:import_hub")},
                {
                    "label": "Auditoría",
                    "url": reverse("imports:import_audit_list"),
                },
                {"label": f"Evento #{event.pk}"},
            ],
        },
    )