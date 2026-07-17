from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from core.wcg_models import DataImportBatch, Entidad
from crm.models import Tarea
from pgo.models import Ticket
from risk.models import RiskOperationSnapshot
from risk.selectors import latest_snapshots_queryset


def splash(request):
    """Landing visual productiva (pgc1); al entrar va al menú principal."""
    return render(request, "splash.html")


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboardhome.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(_panel_stats())
        return ctx


def _panel_stats():
    snaps = latest_snapshots_queryset()
    return {
        "stats": {
            "entidades_total": Entidad.objects.count(),
            "entidades_activas": Entidad.objects.filter(activa=True).count(),
            "operaciones_riesgo": snaps.values("referencia_operacion").distinct().count(),
            "snapshots": RiskOperationSnapshot.objects.count(),
            "tickets_total": Ticket.objects.count(),
            "tickets_abiertos": Ticket.objects.exclude(estado=Ticket.ESTADO_CERRADO).count(),
            "tareas_pendientes": Tarea.objects.filter(estado=Tarea.ESTADO_PENDIENTE).count()
            if hasattr(Tarea, "ESTADO_PENDIENTE")
            else Tarea.objects.filter(estado="PENDIENTE").count(),
            "lotes_importacion": DataImportBatch.objects.count(),
            "importaciones_recientes": DataImportBatch.objects.order_by("-created_at")[:8],
            "alertas_riesgo": snaps.filter(alerta=True).count(),
        }
    }


@login_required
def dashboard_home(request):
    return render(request, "dashboard/dashboardhome.html", _panel_stats())


@login_required
def ayuda(request):
    return render(request, "portal/ayuda.html")
