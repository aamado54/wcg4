"""Consultas reutilizables Risk / Comando Balón (modelos productivos)."""

from __future__ import annotations

from django.db.models import Count, Max, Sum

from risk.models import RiskOperationSnapshot


def latest_snapshots_queryset(request=None):
    """Último snapshot por (entidad, referencia_operacion)."""
    latest = (
        RiskOperationSnapshot.objects.values("entidad_id", "referencia_operacion")
        .annotate(ultima=Max("fecha_snapshot"))
    )
    ids = []
    for row in latest:
        snap = (
            RiskOperationSnapshot.objects.filter(
                entidad_id=row["entidad_id"],
                referencia_operacion=row["referencia_operacion"],
                fecha_snapshot=row["ultima"],
            )
            .values_list("id", flat=True)
            .first()
        )
        if snap:
            ids.append(snap)
    qs = RiskOperationSnapshot.objects.filter(id__in=ids).select_related(
        "entidad", "entidad__unidad_negocio", "producto"
    ).order_by("-dias_mora", "-fecha_snapshot", "entidad__nombre")

    if request is not None:
        cliente = request.GET.get("cliente", "").strip()
        if cliente:
            qs = qs.filter(entidad__nombre__icontains=cliente)
        nivel = request.GET.get("nivel", "").strip()
        if nivel:
            qs = qs.filter(nivel_riesgo=nivel)
        alerta = request.GET.get("alerta", "").strip()
        if alerta == "1":
            qs = qs.filter(alerta=True)
        elif alerta == "0":
            qs = qs.filter(alerta=False)
    return qs


def snapshot_summary(queryset):
    clientes = queryset.values("entidad_id").distinct().count()
    con_mora = queryset.filter(dias_mora__gt=0).count()
    sum_vencido = queryset.aggregate(total=Sum("monto_exigible"))["total"] or 0
    operaciones = queryset.values("referencia_operacion").distinct().count()
    alertas = queryset.filter(alerta=True).count()
    return {
        "total_snapshots": queryset.count(),
        "clientes": clientes,
        "operaciones": operaciones,
        "con_mora": con_mora,
        "suma_vencido": sum_vencido,
        "alertas": alertas,
    }
