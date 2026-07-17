from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from .models import PgoResultadoPeriodo, Ticket
from .periodo import recalculate_pgo_periodos
from .selectors import ticket_dashboard_summary, ticket_list_queryset


@login_required
def dashboard(request):
    recalculate_pgo_periodos()
    summary = ticket_dashboard_summary()
    por_unidad = (
        Ticket.objects.values("unidad_negocio__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")[:10]
    )
    return render(
        request,
        "pgo/pgodashboard.html",
        {
            **summary,
            "abiertos": summary["tickets_abiertos"],
            "cerrados": summary["tickets_cerrados"],
            "recibidos": summary["total_tickets"],
            "por_unidad": por_unidad,
            "breadcrumbs": [
                {"label": "Panel principal", "url": "/panel/"},
                {"label": "PGO — Operación"},
            ],
        },
    )


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "pgo/pgoticketlist.html"
    context_object_name = "tickets"
    paginate_by = 50

    def get_queryset(self):
        return ticket_list_queryset(self.request)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["estados"] = Ticket.ESTADO_CHOICES
        ctx["prioridades"] = Ticket.PRIORIDAD_CHOICES
        return ctx


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "pgo/pgoticketdetail.html"
    context_object_name = "ticket"
    slug_field = "codigo"
    slug_url_kwarg = "codigo"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["eventos"] = self.object.eventos.select_related("usuario")
        return ctx


@login_required
def importar(request):
    return redirect("imports:import_hub")


@login_required
def resumen_usuario(request):
    data = (
        Ticket.objects.values("asignado_a__username")
        .annotate(total=Count("id"), abiertos=Count("id", filter=Q(estado=Ticket.ESTADO_ABIERTO)))
        .order_by("-total")
    )
    return render(request, "pgo/pgoresumenusuario.html", {"data": data})


@login_required
def resumen_unidad(request):
    data = (
        Ticket.objects.values("unidad_negocio__code", "unidad_negocio__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    return render(request, "pgo/pgoresumenunidad.html", {"data": data})


@login_required
def resultados(request):
    recalculate_pgo_periodos()
    rows = PgoResultadoPeriodo.objects.select_related("unidad_negocio").order_by("-periodo")
    return render(request, "pgo/pgoresultados.html", {"resultados": rows})


@login_required
def export_tickets(request):
    import csv

    qs = ticket_list_queryset(request)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="pgo_tickets.csv"'
    writer = csv.writer(response)
    writer.writerow(["codigo", "titulo", "estado", "prioridad", "unidad", "apertura", "cierre"])
    for t in qs:
        writer.writerow(
            [
                t.codigo,
                t.titulo,
                t.estado,
                t.prioridad,
                t.unidad_negocio.code if t.unidad_negocio else "",
                t.fecha_apertura,
                t.fecha_cierre or "",
            ]
        )
    return response
