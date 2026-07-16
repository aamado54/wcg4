"""Consultas reutilizables para PGO y KPIs."""

from __future__ import annotations

from django.db.models import Avg, Count, Q

from apps.pgo.models import PgoTicket

CERRADOS = Q(estado_normalizado__in=["cerrado", "closed", "cerrada"])


def ticket_list_queryset(request):
    qs = PgoTicket.objects.select_related("unidad_negocio", "responsable").order_by(
        "-fecha_apertura"
    )
    estado = request.GET.get("estado", "").strip()
    if estado:
        qs = qs.filter(estado_normalizado__icontains=estado)
    periodo = request.GET.get("periodo", "").strip()
    if periodo:
        qs = qs.filter(anio_mes=periodo)
    prioridad = request.GET.get("prioridad", "").strip()
    if prioridad:
        qs = qs.filter(prioridad__icontains=prioridad)
    return qs


def ticket_dashboard_summary():
    tickets = PgoTicket.objects.all()
    abiertos = tickets.exclude(CERRADOS)
    por_estado = list(
        tickets.values("estado_normalizado")
        .annotate(total=Count("id"))
        .order_by("-total")[:8]
    )
    por_prioridad = list(
        tickets.exclude(prioridad="")
        .values("prioridad")
        .annotate(total=Count("id"))
        .order_by("-total")[:8]
    )
    return {
        "total_tickets": tickets.count(),
        "tickets_cerrados": tickets.filter(CERRADOS).count(),
        "tickets_abiertos": abiertos.count(),
        "tickets_vencidos": abiertos.filter(sla_cumplido=False).count(),
        "sla_cumplidos": tickets.filter(sla_cumplido=True).count(),
        "sla_incumplidos": tickets.filter(sla_cumplido=False).exclude(CERRADOS).count(),
        "tiempo_promedio": tickets.filter(duracion_horas__isnull=False).aggregate(
            avg=Avg("duracion_horas")
        )["avg"],
        "por_estado": por_estado,
        "por_prioridad": por_prioridad,
        "tickets_recientes": tickets.order_by("-fecha_apertura")[:10],
    }
