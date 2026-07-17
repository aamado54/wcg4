"""Consultas reutilizables CRM (modelos productivos)."""

from __future__ import annotations

from django.db.models import Count, Q

from core.wcg_models import Entidad


def entidad_list_queryset(request):
    qs = Entidad.objects.select_related("unidad_negocio").annotate(
        num_contactos=Count("contactos", distinct=True),
        num_productos=Count("productos_relacionados", distinct=True),
    ).order_by("nombre")
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q) | Q(nit__icontains=q) | Q(codigo__icontains=q)
        )
    tipo = request.GET.get("tipo", "").strip()
    if tipo:
        qs = qs.filter(tipo=tipo)
    unidad = request.GET.get("unidad", "").strip()
    if unidad:
        qs = qs.filter(unidad_negocio_id=unidad)
    activo = request.GET.get("activo", "").strip()
    if activo == "1":
        qs = qs.filter(activa=True)
    elif activo == "0":
        qs = qs.filter(activa=False)
    return qs


def entidad_summary(queryset=None):
    base = queryset if queryset is not None else Entidad.objects.all()
    por_unidad = list(
        base.filter(unidad_negocio__isnull=False)
        .values("unidad_negocio__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )
    por_tipo = list(
        base.values("tipo").annotate(total=Count("id")).order_by("-total")
    )
    return {
        "total": base.count(),
        "activas": base.filter(activa=True).count(),
        "inactivas": base.filter(activa=False).count(),
        "por_unidad": por_unidad,
        "por_tipo": por_tipo,
    }
