from __future__ import annotations

import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from reports.models import ReportConfig
from reports.services import (
    AREA_ADMIN,
    AREA_PGC,
    AREA_PGO,
    AREA_RISK,
    generate_report_package,
)


@login_required
@require_GET
def report_defaults(request):
    cfg = ReportConfig.get_active()
    return JsonResponse(
        {
            "ok": True,
            "defaults": {
                AREA_ADMIN: cfg.include_admin_by_default,
                AREA_PGC: cfg.include_pgc_by_default,
                AREA_PGO: cfg.include_pgo_by_default,
                AREA_RISK: cfg.include_risk_by_default,
            },
            "labels": {
                AREA_ADMIN: "Administración",
                AREA_PGC: "PGC",
                AREA_PGO: "PGO",
                AREA_RISK: "B. Riesgo",
            },
        }
    )


@login_required
@require_POST
def generate_reports(request):
    """
    Acepta application/json {areas:[...]} o form areas=admin&areas=pgc
    """
    areas: list[str] = []
    content_type = (request.content_type or "").lower()
    if "application/json" in content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return HttpResponseBadRequest("JSON inválido.")
        raw = payload.get("areas") or []
        if isinstance(raw, str):
            areas = [raw]
        else:
            areas = [str(a) for a in raw]
    else:
        areas = request.POST.getlist("areas")

    areas = [a.strip().lower() for a in areas if str(a).strip()]
    if not areas:
        return JsonResponse(
            {"ok": False, "error": "Seleccione al menos un área (Administración, PGC, PGO o B. Riesgo)."},
            status=400,
        )

    try:
        filename, content, ctype = generate_report_package(areas)
    except ValueError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=400)
    except Exception as exc:
        return JsonResponse(
            {"ok": False, "error": f"Error al generar reportes: {exc}"},
            status=500,
        )

    response = HttpResponse(content, content_type=ctype)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    response["X-Report-Filename"] = filename
    return response
