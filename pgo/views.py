from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from core.wcg_models import UnidadNegocio

from .forms import ImportFileForm
from .models import PgoResultadoPeriodo, Ticket
from .periodo import recalculate_pgo_periodos
from . import services

User = get_user_model()


@login_required
def dashboard(request):
    recalculate_pgo_periodos()
    abiertos = Ticket.objects.filter(estado__in=[Ticket.ESTADO_ABIERTO, Ticket.ESTADO_EN_PROCESO]).count()
    cerrados = Ticket.objects.filter(estado=Ticket.ESTADO_CERRADO).count()
    recibidos = Ticket.objects.count()
    resultados = PgoResultadoPeriodo.objects.select_related("unidad_negocio").order_by("-periodo")[:12]
    por_unidad = (
        Ticket.objects.values("unidad_negocio__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")[:10]
    )
    return render(
        request,
        "pgo/pgodashboard.html",
        {
            "abiertos": abiertos,
            "cerrados": cerrados,
            "recibidos": recibidos,
            "resultados": resultados,
            "por_unidad": por_unidad,
        },
    )


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "pgo/pgoticketlist.html"
    context_object_name = "tickets"
    paginate_by = 50

    def get_queryset(self):
        qs = Ticket.objects.select_related("entidad", "unidad_negocio", "asignado_a")
        estado = self.request.GET.get("estado")
        if estado:
            qs = qs.filter(estado=estado)
        return qs.order_by("-fecha_apertura")


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
    batch = None
    if request.method == "POST":
        form = ImportFileForm(request.POST, request.FILES)
        if form.is_valid():
            batch = services.import_tickets(request.user, form.cleaned_data["archivo"])
            recalculate_pgo_periodos()
            messages.info(
                request,
                f"Importación: {batch.creados} creados, "
                f"{batch.actualizados} actualizados, {batch.errores} errores.",
            )
    else:
        form = ImportFileForm()
    return render(request, "pgo/pgoimportform.html", {"form": form, "batch": batch})


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
