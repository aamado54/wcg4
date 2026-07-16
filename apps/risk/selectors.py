"""Consultas reutilizables para Risk y KPIs del Comando Balón."""

from __future__ import annotations

from django.db.models import Count, Sum

from apps.risk.models import RiskOperationSnapshot


def snapshot_queryset(request):
    qs = RiskOperationSnapshot.objects.select_related(
        "operacion",
        "entidad",
        "operacion__unidad_negocio",
        "operacion__producto",
    ).order_by("-fecha_snapshot", "-due_days", "entidad__nombre")
    cliente = request.GET.get("cliente", "").strip()
    if cliente:
        qs = qs.filter(entidad__nombre__icontains=cliente)
    estado = request.GET.get("estado", "").strip()
    if estado:
        qs = qs.filter(estado_operacion__icontains=estado)
    return qs


def snapshot_summary(queryset):
    clientes = queryset.values("entidad_id").distinct().count()
    con_mora = queryset.filter(due_days__gt=0).count()
    sum_vencido = queryset.aggregate(total=Sum("past_due_balance"))["total"] or 0
    operaciones = queryset.values("operacion_id").distinct().count()
    return {
        "total_snapshots": queryset.count(),
        "clientes": clientes,
        "operaciones": operaciones,
        "con_mora": con_mora,
        "suma_vencido": sum_vencido,
    }
