from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView

from core.wcg_models import Entidad

from .models import ProgramacionPago, RiskOperationSnapshot
from .selectors import latest_snapshots_queryset, snapshot_summary


@login_required
def comando_balon(request):
    qs = latest_snapshots_queryset(request)
    summary = snapshot_summary(qs)
    operaciones = list(qs[:100])
    alertas = [s for s in operaciones if s.alerta]
    mora_alta = sorted(
        [s for s in operaciones if s.dias_mora >= 30],
        key=lambda s: s.dias_mora,
        reverse=True,
    )[:50]
    pagos_vencidos = (
        ProgramacionPago.objects.filter(fecha_programada__lt=timezone.now().date())
        .select_related("entidad")
        .order_by("fecha_programada")[:40]
    )
    return render(
        request,
        "risk/riskcommandobalon.html",
        {
            "operaciones": operaciones,
            "snapshots": operaciones,
            "summary": summary,
            "alertas": alertas,
            "mora_alta": mora_alta,
            "pagos_vencidos": pagos_vencidos,
            "niveles": RiskOperationSnapshot.NIVEL_CHOICES,
            "breadcrumbs": [
                {"label": "Panel principal", "url": "/panel/"},
                {"label": "Riesgo — Comando Balón"},
            ],
        },
    )


class ClienteListView(LoginRequiredMixin, ListView):
    model = Entidad
    template_name = "risk/riskclientlist.html"
    context_object_name = "clientes"
    paginate_by = 50

    def get_queryset(self):
        ids = (
            RiskOperationSnapshot.objects.values_list("entidad_id", flat=True).distinct()
        )
        return Entidad.objects.filter(id__in=ids).order_by("nombre")


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Entidad
    template_name = "risk/riskclientdetail.html"
    context_object_name = "entidad"
    slug_field = "codigo"
    slug_url_kwarg = "codigo"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        entidad = self.object
        ctx["estados"] = entidad.estados_financieros.order_by("-periodo")[:12]
        ctx["programaciones"] = entidad.programaciones_pago.order_by("-fecha_programada")[:20]
        ctx["pagos"] = entidad.pagos_realizados.order_by("-fecha_pago")[:20]
        ctx["snapshots"] = entidad.risk_snapshots.select_related("producto").order_by(
            "-fecha_snapshot"
        )[:20]
        ctx["contactos_cobranza"] = entidad.contactos_cobranza.filter(activo=True)
        return ctx


class OperacionDetailView(LoginRequiredMixin, DetailView):
    model = RiskOperationSnapshot
    template_name = "risk/riskoperationdetail.html"
    context_object_name = "snapshot"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        snap = self.object
        ref = snap.referencia_operacion
        ctx["historial"] = RiskOperationSnapshot.objects.filter(
            entidad=snap.entidad,
            referencia_operacion=ref,
        ).order_by("-fecha_snapshot")
        # Rentas/cuotas del contrato: referencia empieza con el código de operación
        ctx["pagos_programados"] = ProgramacionPago.objects.filter(
            entidad=snap.entidad,
            referencia__startswith=ref,
        ).order_by("-fecha_programada")[:30]
        from risk.models import PagoRealizado

        ctx["pagos_realizados"] = PagoRealizado.objects.filter(
            entidad=snap.entidad,
            referencia__startswith=ref,
        ).order_by("-fecha_pago")[:30]
        ctx["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "Balón de Riesgo", "url": "/risk/"},
            {"label": "Clientes", "url": "/risk/clientes/"},
            {"label": snap.entidad.nombre, "url": f"/risk/cliente/{snap.entidad.codigo}/"},
            {"label": ref},
        ]
        return ctx


@login_required
def importar(request):
    return redirect("imports:import_hub")


@login_required
def export_comando_balon(request):
    import csv

    qs = latest_snapshots_queryset(request)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="comando_balon.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [
            "fecha",
            "cliente",
            "operacion",
            "producto",
            "saldo",
            "exigible",
            "dias_mora",
            "nivel",
            "alerta",
        ]
    )
    for s in qs:
        writer.writerow(
            [
                s.fecha_snapshot,
                s.entidad.nombre,
                s.referencia_operacion,
                s.producto.nombre if s.producto else "",
                s.saldo,
                s.monto_exigible,
                s.dias_mora,
                s.nivel_riesgo,
                "1" if s.alerta else "0",
            ]
        )
    return response
