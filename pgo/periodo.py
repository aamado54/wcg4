"""Cálculo de agregados PGO por período y unidad."""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from core.wcg_models import UnidadNegocio
from pgo.models import PgoResultadoPeriodo, Ticket


def _periodo_from_dt(dt) -> str:
    if not dt:
        return timezone.now().strftime("%Y-%m")
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt)
    local = timezone.localtime(dt)
    return local.strftime("%Y-%m")


def _horas_entre(inicio, fin) -> Decimal:
    if not inicio or not fin:
        return Decimal("0")
    if timezone.is_naive(inicio):
        inicio = timezone.make_aware(inicio)
    if timezone.is_naive(fin):
        fin = timezone.make_aware(fin)
    delta = fin - inicio
    return Decimal(str(round(delta.total_seconds() / 3600, 2)))


@transaction.atomic
def recalculate_pgo_periodos(periodo: str | None = None) -> list[PgoResultadoPeriodo]:
    """
    Recalcula PgoResultadoPeriodo desde tickets.
    Métricas: recibidos, cerrados, abiertos, tiempo promedio horas, % SLA cumplido.
    """
    tickets = Ticket.objects.select_related("unidad_negocio").all()
    buckets: dict[tuple[str, int | None], dict] = defaultdict(
        lambda: {
            "cerrados": 0,
            "abiertos": 0,
            "horas_total": Decimal("0"),
            "sla_ok": 0,
            "sla_total": 0,
        }
    )

    for t in tickets:
        p = _periodo_from_dt(t.fecha_apertura)
        if periodo and p != periodo:
            continue
        un_id = t.unidad_negocio_id
        key = (p, un_id)
        if t.estado == Ticket.ESTADO_CERRADO:
            buckets[key]["cerrados"] += 1
            if t.fecha_cierre:
                horas = _horas_entre(t.fecha_apertura, t.fecha_cierre)
                buckets[key]["horas_total"] += horas
                buckets[key]["sla_total"] += 1
                if horas <= Decimal(t.sla_horas):
                    buckets[key]["sla_ok"] += 1
        else:
            buckets[key]["abiertos"] += 1

    resultados: list[PgoResultadoPeriodo] = []
    default_un = UnidadNegocio.objects.filter(code="TI").first()

    for (p, un_id), data in buckets.items():
        unidad = UnidadNegocio.objects.filter(pk=un_id).first() if un_id else default_un
        if not unidad:
            continue
        cerrados = data["cerrados"]
        tiempo_prom = (data["horas_total"] / Decimal(cerrados)) if cerrados else Decimal("0")
        sla_pct = (
            (Decimal(data["sla_ok"]) / Decimal(data["sla_total"]) * Decimal("100"))
            if data["sla_total"]
            else Decimal("0")
        )
        obj, _ = PgoResultadoPeriodo.objects.update_or_create(
            periodo=p,
            unidad_negocio=unidad,
            defaults={
                "tickets_cerrados": cerrados,
                "tickets_abiertos": data["abiertos"],
                "tiempo_promedio_horas": tiempo_prom,
                "cumplimiento_sla_pct": sla_pct.quantize(Decimal("0.01")),
            },
        )
        resultados.append(obj)
    return resultados
