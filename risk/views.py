from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import DetailView

from core.wcg_models import Entidad

from .forms import ImportFileForm
from .models import ProgramacionPago, RiskOperationSnapshot
from . import services


@login_required
def comando_balon(request):
    latest_dates = (
        RiskOperationSnapshot.objects.values("entidad_id", "referencia_operacion")
        .annotate(ultima=Max("fecha_snapshot"))
    )
    operaciones = []
    for row in latest_dates.order_by("-ultima")[:100]:
        snap = (
            RiskOperationSnapshot.objects.filter(
                entidad_id=row["entidad_id"],
                referencia_operacion=row["referencia_operacion"],
                fecha_snapshot=row["ultima"],
            )
            .select_related("entidad", "entidad__unidad_negocio", "producto")
            .first()
        )
        if snap:
            operaciones.append(snap)

    alertas = [s for s in operaciones if s.alerta]
    mora_alta = sorted(
        [s for s in operaciones if s.dias_mora >= 30],
        key=lambda s: s.dias_mora,
        reverse=True,
    )[:50]
    pagos_vencidos = (
        ProgramacionPago.objects.filter(fecha_programada__lt=timezone.now().date())
        .select_related("entidad")
        .order_by("fecha_programada")[:50]
    )
    return render(
        request,
        "risk/riskcommandobalon.html",
        {
            "operaciones": operaciones,
            "alertas": alertas,
            "mora_alta": mora_alta,
            "pagos_vencidos": pagos_vencidos,
        },
    )


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
        ctx["snapshots"] = entidad.risk_snapshots.select_related("producto").order_by("-fecha_snapshot")[:20]
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
        ctx["historial"] = RiskOperationSnapshot.objects.filter(
            entidad=snap.entidad,
            referencia_operacion=snap.referencia_operacion,
        ).order_by("-fecha_snapshot")
        return ctx


@login_required
def importar(request):
    batch = None
    importers = {
        "leasing_database": services.import_leasing_database,
        "estados_financieros": services.import_estados_financieros,
        "programacion_pagos": services.import_programacion_pagos,
        "pagos_realizados": services.import_pagos_realizados,
        "snapshots": services.import_snapshots,
    }
    if request.method == "POST":
        form = ImportFileForm(request.POST, request.FILES)
        if form.is_valid():
            tipo = form.cleaned_data["tipo"]
            batch = importers[tipo](request.user, form.cleaned_data["archivo"])
            messages.info(
                request,
                f"Importación {tipo}: {batch.creados} creados, "
                f"{batch.actualizados} actualizados, {batch.errores} errores.",
            )
    else:
        form = ImportFileForm()
    return render(request, "risk/riskimportform.html", {"form": form, "batch": batch})
