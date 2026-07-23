from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, ListView

from apps.core.exports import csv_response
from apps.core.forms import ImportFileForm

from .models import PgoMonthlyAgg, PgoPeriodScore, PgoTicket
from .selectors import ticket_dashboard_summary, ticket_list_queryset
from .services import brief_detalle, period_scores_for_dashboard, recalculate_pgo_scores


@login_required
def dashboard(request):
    # Recalc liviano para que la tabla de resultados tenga datos al abrir.
    try:
        recalculate_pgo_scores()
    except Exception:
        pass
    summary = ticket_dashboard_summary()
    scores = list(period_scores_for_dashboard(40))
    for s in scores:
        s.detalle_breve = brief_detalle(s)
    context = {
        **summary,
        "period_scores": scores,
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
    try:
        recalculate_pgo_scores(periodo=request.GET.get("periodo", "").strip() or None)
    except Exception:
        pass
    periodo = request.GET.get("periodo", "").strip()
    scores = PgoPeriodScore.objects.select_related("unidad_negocio", "usuario").order_by(
        "-periodo", "area"
    )
    aggs = PgoMonthlyAgg.objects.select_related("unidad_negocio").order_by("-periodo")
    if periodo:
        scores = scores.filter(periodo=periodo)
        aggs = aggs.filter(periodo=periodo)
    score_list = list(scores[:50])
    for s in score_list:
        s.detalle_breve = brief_detalle(s)
    context = {
        "scores": score_list,
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
    return redirect("imports:import_hub")
