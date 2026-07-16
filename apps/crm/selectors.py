"""Consultas reutilizables para listados CRM y KPIs."""

from __future__ import annotations

from django.db.models import Count, Q

from apps.core.models import Entidad


def entidad_list_queryset(request):
    qs = Entidad.objects.annotate(
        num_contactos=Count("contactos", distinct=True),
        num_productos=Count("relaciones_producto", distinct=True),
    ).order_by("nombre")
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(nombre__icontains=q) | Q(nit__icontains=q))
    tipo = request.GET.get("tipo", "").strip()
    if tipo:
        qs = qs.filter(tipo_entidad=tipo)
    activo = request.GET.get("activo", "").strip()
    if activo == "1":
        qs = qs.filter(activo=True)
    elif activo == "0":
        qs = qs.filter(activo=False)
    return qs


def entidad_summary(queryset=None):
    base = queryset if queryset is not None else Entidad.objects.all()
    por_ciudad = list(
        base.exclude(ciudad="")
        .values("ciudad")
        .annotate(total=Count("id"))
        .order_by("-total", "ciudad")[:5]
    )
    por_riesgo = list(
        base.exclude(categoria_riesgo="")
        .values("categoria_riesgo")
        .annotate(total=Count("id"))
        .order_by("-total", "categoria_riesgo")[:5]
    )
    return {
        "total": base.count(),
        "activas": base.filter(activo=True).count(),
        "inactivas": base.filter(activo=False).count(),
        "por_ciudad": por_ciudad,
        "por_riesgo": por_riesgo,
    }
