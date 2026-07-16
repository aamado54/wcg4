from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.models import DataImportBatch, Entidad
from apps.crm.models import Tarea
from apps.pgo.models import PgoTicket
from apps.risk.models import RiskOperacion, RiskOperationSnapshot


class SplashView(TemplateView):
    template_name = "portal/splash_wcgone.html"


class PanelView(LoginRequiredMixin, TemplateView):
    template_name = "portal/home_wcgone.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cerrados = ["cerrado", "closed", "cerrada"]
        context["stats"] = {
            "entidades_total": Entidad.objects.count(),
            "entidades_activas": Entidad.objects.filter(activo=True).count(),
            "operaciones_riesgo": RiskOperacion.objects.count(),
            "snapshots": RiskOperationSnapshot.objects.count(),
            "tickets_total": PgoTicket.objects.count(),
            "tickets_abiertos": PgoTicket.objects.exclude(
                estado_normalizado__in=cerrados
            ).count(),
            "tareas_pendientes": Tarea.objects.filter(completada=False).count(),
            "lotes_importacion": DataImportBatch.objects.count(),
            "importaciones_recientes": DataImportBatch.objects.order_by("-fecha_carga")[:5],
        }
        context["breadcrumbs"] = [{"label": "Panel principal"}]
        return context


class AyudaView(LoginRequiredMixin, TemplateView):
    template_name = "portal/ayuda.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "Guía de uso"},
        ]
        return context
