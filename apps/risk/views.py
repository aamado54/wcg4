from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max, Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView

from apps.core.exports import csv_response
from apps.core.models import Entidad

from .models import RiskOperacion, RiskOperationSnapshot
from .selectors import snapshot_queryset, snapshot_summary


@login_required
def comando_balon(request):
    qs = snapshot_queryset(request)
    context = {
        "snapshots": qs[:100],
        "summary": snapshot_summary(qs),
        "export_query": request.GET.urlencode(),
        "breadcrumbs": [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "Riesgo — Comando Balón"},
        ],
    }
    return render(request, "wcgone/risk/comando_balon.html", context)


@login_required
def export_comando_balon_csv(request):
    qs = snapshot_queryset(request)
    rows = []
    for snap in qs:
        rows.append([
            snap.fecha_snapshot.isoformat() if snap.fecha_snapshot else "",
            snap.entidad.nombre,
            snap.entidad.nit or "",
            snap.operacion.codigo_operacion,
            snap.producto_nombre_raw or "",
            snap.estado_operacion or "",
            snap.capital_balance or "",
            snap.past_due_balance or "",
            snap.due_days if snap.due_days is not None else "",
        ])
    filename = f"risk_comando_balon_{timezone.localdate().isoformat()}.csv"
    return csv_response(
        filename,
        [
            "Fecha snapshot",
            "Cliente",
            "NIT",
            "Operación",
            "Producto",
            "Estado",
            "Saldo capital",
            "Saldo vencido",
            "Días atraso",
        ],
        rows,
    )


class ClienteListView(LoginRequiredMixin, ListView):
    model = Entidad
    template_name = "wcgone/risk/cliente_list.html"
    context_object_name = "clientes"
    paginate_by = 25

    def get_queryset(self):
        qs = (
            Entidad.objects.filter(operaciones_riesgo__isnull=False)
            .annotate(
                num_operaciones=Count("operaciones_riesgo", distinct=True),
                ultimo_snapshot=Max("risk_snapshots__fecha_snapshot"),
            )
            .distinct()
            .order_by("nombre")
        )
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(nit__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "Balón de Riesgo"},
            {"label": "Clientes"},
        ]
        return context


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Entidad
    template_name = "wcgone/risk/cliente_detail.html"
    context_object_name = "cliente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.object
        context["operaciones"] = cliente.operaciones_riesgo.select_related(
            "producto", "unidad_negocio"
        ).order_by("codigo_operacion")
        context["snapshots_recientes"] = (
            cliente.risk_snapshots.select_related("operacion")
            .order_by("-fecha_snapshot")[:10]
        )
        context["alertas"] = cliente.alertas_riesgo.filter(activa=True).order_by(
            "-fecha_alerta"
        )[:10]
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "Balón de Riesgo"},
            {"label": "Clientes", "url": "/wcgone/risk/clientes/"},
            {"label": cliente.nombre},
        ]
        return context


class OperacionDetailView(LoginRequiredMixin, DetailView):
    model = RiskOperacion
    template_name = "wcgone/risk/operacion_detail.html"
    context_object_name = "operacion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        operacion = self.object
        context["snapshots"] = operacion.snapshots.order_by("-fecha_snapshot")
        context["pagos_programados"] = operacion.pagos_programados.order_by("fecha_programada")
        context["pagos_realizados"] = operacion.pagos_realizados.order_by("-fecha_pago")
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "Balón de Riesgo"},
            {"label": "Clientes", "url": "/wcgone/risk/clientes/"},
            {
                "label": operacion.entidad.nombre,
                "url": f"/wcgone/risk/clientes/{operacion.entidad_id}/",
            },
            {"label": operacion.codigo_operacion},
        ]
        return context


from django.contrib import messages  # noqa: E402
from django.shortcuts import redirect, render  # noqa: E402

@login_required
def importar_snapshots(request):
    return redirect("imports:import_hub")


@login_required
def importar_eeff(request):
    return redirect("imports:import_hub")
