from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from core.wcg_models import Contacto, Entidad, UnidadNegocio
from crm.models import Tarea
from crm.selectors import entidad_list_queryset, entidad_summary

from .forms import InteraccionForm, TareaForm


class EntidadListView(LoginRequiredMixin, ListView):
    model = Entidad
    template_name = "crm/crmentitylist.html"
    context_object_name = "entidades"
    paginate_by = 50

    def get_queryset(self):
        return entidad_list_queryset(self.request)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["unidades"] = UnidadNegocio.objects.filter(activa=True).order_by("nombre")
        ctx["tipos"] = Entidad.TIPO_CHOICES
        ctx["summary"] = entidad_summary(Entidad.objects.all())
        ctx["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "CRM — Clientes"},
        ]
        return ctx


class EntidadDetailView(LoginRequiredMixin, DetailView):
    model = Entidad
    template_name = "crm/crmentitydetail.html"
    context_object_name = "entidad"
    slug_field = "codigo"
    slug_url_kwarg = "codigo"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        entidad = self.object
        contactos = list(entidad.contactos.filter(activo=True))
        ctx["interacciones"] = entidad.interacciones.select_related("usuario")[:20]
        ctx["tareas"] = entidad.tareas.exclude(estado=Tarea.ESTADO_HECHA).exclude(
            estado=Tarea.ESTADO_CANCELADA
        ).select_related("asignado_a")[:20]
        ctx["contactos"] = contactos
        ctx["productos"] = entidad.productos_relacionados.select_related(
            "producto", "producto__unidad_negocio"
        )
        ctx["contacto_principal"] = next(
            (c for c in contactos if c.es_principal),
            contactos[0] if contactos else None,
        )
        ctx["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "CRM — Clientes", "url": "/crm/"},
            {"label": entidad.nombre},
        ]
        return ctx


class ContactoListView(LoginRequiredMixin, ListView):
    model = Contacto
    template_name = "crm/crmcontactolist.html"
    context_object_name = "contactos"
    paginate_by = 50

    def get_queryset(self):
        qs = Contacto.objects.select_related("entidad").filter(activo=True).order_by(
            "entidad__nombre", "nombre"
        )
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q)
                | Q(email__icontains=q)
                | Q(entidad__nombre__icontains=q)
            )
        return qs


class TareaListView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = "crm/crmtarealist.html"
    context_object_name = "tareas"
    paginate_by = 50

    def get_queryset(self):
        return Tarea.objects.select_related("entidad", "asignado_a").order_by(
            "-fecha_vencimiento"
        )


@login_required
def nueva_interaccion(request, codigo):
    entidad = get_object_or_404(Entidad, codigo=codigo)
    if request.method == "POST":
        form = InteraccionForm(request.POST)
        if form.is_valid():
            inter = form.save(commit=False)
            inter.entidad = entidad
            inter.usuario = request.user
            inter.save()
            messages.success(request, "Interacción registrada.")
            return redirect("crm:entidad_detail", codigo=entidad.codigo)
    else:
        form = InteraccionForm()
    return render(request, "crm/crminteractionform.html", {"form": form, "entidad": entidad})


@login_required
def nueva_tarea(request, codigo):
    entidad = get_object_or_404(Entidad, codigo=codigo)
    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.entidad = entidad
            if not tarea.asignado_a:
                tarea.asignado_a = request.user
            tarea.save()
            messages.success(request, "Tarea creada.")
            return redirect("crm:entidad_detail", codigo=entidad.codigo)
    else:
        form = TareaForm(initial={"asignado_a": request.user.pk})
    return render(request, "crm/crmtaskform.html", {"form": form, "entidad": entidad})


@login_required
def importar(request, tipo=None):
    return redirect("imports:import_hub")


@login_required
def export_entidades(request):
    import csv

    qs = entidad_list_queryset(request)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="crm_entidades.csv"'
    writer = csv.writer(response)
    writer.writerow(["codigo", "nombre", "nit", "tipo", "unidad", "activa"])
    for e in qs:
        writer.writerow(
            [
                e.codigo,
                e.nombre,
                e.nit,
                e.tipo,
                e.unidad_negocio.code if e.unidad_negocio else "",
                "1" if e.activa else "0",
            ]
        )
    return response
