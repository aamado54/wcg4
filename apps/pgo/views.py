from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, ListView

from apps.core.exports import csv_response
from apps.core.forms import ImportFileForm

from .models import PgoMonthlyAgg, PgoPeriodScore, PgoTicket
from .selectors import ticket_dashboard_summary, ticket_list_queryset


@login_required
def dashboard(request):
    summary = ticket_dashboard_summary()
    context = {
        **summary,
        "breadcrumbs": [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "PGO — Operación"},
        ],
    }
    return render(request, "wcgone/pgo/dashboard.html", context)


class TicketListView(LoginRequiredMixin, ListView):
    model = PgoTicket
    template_name = "wcgone/pgo/ticket_list.html"
    context_object_name = "tickets"
    paginate_by = 25

    def get_queryset(self):
        return ticket_list_queryset(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "PGO — Operación", "url": "/wcgone/pgo/"},
            {"label": "Tickets"},
        ]
        context["export_query"] = self.request.GET.urlencode()
        return context


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = PgoTicket
    template_name = "wcgone/pgo/ticket_detail.html"
    context_object_name = "ticket"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = self.object
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "PGO — Operación", "url": "/wcgone/pgo/"},
            {"label": "Tickets", "url": "/wcgone/pgo/tickets/"},
            {"label": ticket.ticket_externo_id or f"#{ticket.pk}"},
        ]
        return context


@login_required
def resultados(request):
    periodo = request.GET.get("periodo", "").strip()
    scores = PgoPeriodScore.objects.select_related("unidad_negocio", "usuario").order_by(
        "-periodo", "area"
    )
    aggs = PgoMonthlyAgg.objects.select_related("unidad_negocio").order_by("-periodo")
    if periodo:
        scores = scores.filter(periodo=periodo)
        aggs = aggs.filter(periodo=periodo)
    context = {
        "scores": scores[:50],
        "aggs": aggs[:50],
        "breadcrumbs": [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "PGO — Operación", "url": "/wcgone/pgo/"},
            {"label": "Resultados por período"},
        ],
    }
    return render(request, "wcgone/pgo/resultados.html", context)


from django.contrib import messages  # noqa: E402
from django.shortcuts import redirect  # noqa: E402

from .imports.tickets import import_tickets  # noqa: E402


@login_required
def export_tickets_csv(request):
    qs = ticket_list_queryset(request)
    rows = []
    for t in qs:
        rows.append([
            t.ticket_externo_id or t.pk,
            t.titulo,
            t.estado_normalizado or t.estado_raw or "",
            t.prioridad or "",
            t.departamento or "",
            t.sistema or "",
            t.anio_mes or "",
            "Sí" if t.sla_cumplido else "No",
            t.fecha_apertura.strftime("%Y-%m-%d %H:%M") if t.fecha_apertura else "",
            t.fecha_cierre.strftime("%Y-%m-%d %H:%M") if t.fecha_cierre else "",
            t.duracion_horas or "",
        ])
    filename = f"pgo_tickets_{timezone.localdate().isoformat()}.csv"
    return csv_response(
        filename,
        [
            "ID ticket",
            "Título",
            "Estado",
            "Prioridad",
            "Departamento",
            "Sistema",
            "Período",
            "SLA cumplido",
            "Fecha apertura",
            "Fecha cierre",
            "Duración (h)",
        ],
        rows,
    )


@login_required
def importar_tickets(request):
    if request.method == "POST":
        form = ImportFileForm(request.POST, request.FILES)
        if form.is_valid():
            batch = import_tickets(request.user, form.cleaned_data["archivo"])
            messages.success(
                request,
                f"Importación PGO finalizada ({batch.get_estado_display()}): "
                f"{batch.filas_validas} filas válidas, {batch.filas_error} con error.",
            )
            return redirect("core:import_batch_detail", pk=batch.pk)
    else:
        form = ImportFileForm()
    return render(
        request,
        "imports/upload.html",
        {
            "form": form,
            "titulo": "Importar tickets PGO",
            "descripcion": "Carga CSV o XLSX con tickets operativos de helpdesk.",
            "columnas_ejemplo": "ID Ticket, Título, Estado, Prioridad, Fecha apertura, Fecha cierre, Departamento",
            "breadcrumbs": [
                {"label": "Panel principal", "url": "/panel/"},
                {"label": "PGO — Operación", "url": "/wcgone/pgo/"},
                {"label": "Importar tickets"},
            ],
        },
    )
