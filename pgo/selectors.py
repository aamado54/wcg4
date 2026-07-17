"""Consultas reutilizables PGO (modelos productivos)."""

from __future__ import annotations

from decimal import Decimal

from django.db.models import Avg, Count, Q
from django.utils import timezone

from pgo.models import Ticket

CERRADOS = Q(estado=Ticket.ESTADO_CERRADO)


def _horas_entre(inicio, fin) -> float | None:
    if not inicio or not fin:
        return None
    if timezone.is_naive(inicio):
        inicio = timezone.make_aware(inicio)
    if timezone.is_naive(fin):
        fin = timezone.make_aware(fin)
    return (fin - inicio).total_seconds() / 3600


def ticket_list_queryset(request):
    qs = Ticket.objects.select_related("unidad_negocio", "asignado_a", "entidad").order_by(
        "-fecha_apertura"
    )
    estado = request.GET.get("estado", "").strip()
    if estado:
        qs = qs.filter(estado=estado)
    prioridad = request.GET.get("prioridad", "").strip()
    if prioridad:
        qs = qs.filter(prioridad=prioridad)
    unidad = request.GET.get("unidad", "").strip()
    if unidad:
        qs = qs.filter(unidad_negocio_id=unidad)
    return qs


def ticket_dashboard_summary():
    tickets = Ticket.objects.select_related("unidad_negocio", "asignado_a")
    abiertos = tickets.exclude(CERRADOS)
    cerrados = tickets.filter(CERRADOS)

    # SLA: cerrado dentro de sla_horas, o abierto ya excedido
    vencidos = 0
    horas_list = []
    for t in tickets.filter(fecha_cierre__isnull=False):
        h = _horas_entre(t.fecha_apertura, t.fecha_cierre)
        if h is not None:
            horas_list.append(h)
    now = timezone.now()
    for t in abiertos:
        h = _horas_entre(t.fecha_apertura, now)
        if h is not None and h > t.sla_horas:
            vencidos += 1

    por_estado = list(
        tickets.values("estado").annotate(total=Count("id")).order_by("-total")
    )
    por_prioridad = list(
        tickets.values("prioridad").annotate(total=Count("id")).order_by("-total")
    )
    avg_h = sum(horas_list) / len(horas_list) if horas_list else None

    return {
        "total_tickets": tickets.count(),
        "tickets_cerrados": cerrados.count(),
        "tickets_abiertos": abiertos.count(),
        "tickets_vencidos": vencidos,
        "tiempo_promedio": avg_h,
        "por_estado": por_estado,
        "por_prioridad": por_prioridad,
        "tickets_recientes": list(tickets.order_by("-fecha_apertura")[:12]),
        "resultados": list(
            __import__("pgo.models", fromlist=["PgoResultadoPeriodo"])
            .PgoResultadoPeriodo.objects.select_related("unidad_negocio")
            .order_by("-periodo")[:12]
        ),
    }
