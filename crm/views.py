from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from core.wcg_models import Entidad, UnidadNegocio

from .forms import ImportFileForm, InteraccionForm, TareaForm
from .models import Interaccion, Tarea
from . import services


class EntidadListView(LoginRequiredMixin, ListView):
    model = Entidad
    template_name = "crm/crmentitylist.html"
    context_object_name = "entidades"
    paginate_by = 50

    def get_queryset(self):
        qs = Entidad.objects.select_related("unidad_negocio").filter(activa=True)
        q = self.request.GET.get("q", "").strip()
        tipo = self.request.GET.get("tipo", "").strip()
        unidad = self.request.GET.get("unidad", "").strip()
        if q:
            qs = qs.filter(nombre__icontains=q) | qs.filter(codigo__icontains=q) | qs.filter(nit__icontains=q)
        if tipo:
            qs = qs.filter(tipo=tipo)
        if unidad:
            qs = qs.filter(unidad_negocio_id=unidad)
        return qs.order_by("nombre")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["unidades"] = UnidadNegocio.objects.filter(activa=True).order_by("nombre")
        ctx["tipos"] = Entidad.TIPO_CHOICES
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
        ctx["interacciones"] = entidad.interacciones.select_related("usuario")[:20]
        ctx["tareas"] = entidad.tareas.select_related("asignado_a")[:20]
        ctx["contactos"] = entidad.contactos.filter(activo=True)
        ctx["productos"] = entidad.productos_relacionados.select_related("producto")
        return ctx


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
def importar(request, tipo):
    tipos = {
        "entidades": ("Importar entidades", services.import_entidades),
        "contactos": ("Importar contactos", services.import_contactos),
    }
    if tipo not in tipos:
        return redirect("crm:entidad_list")
    titulo, importer = tipos[tipo]
    batch = None
    if request.method == "POST":
        form = ImportFileForm(request.POST, request.FILES)
        if form.is_valid():
            batch = importer(request.user, form.cleaned_data["archivo"])
            messages.info(
                request,
                f"Importación finalizada: {batch.creados} creados, "
                f"{batch.actualizados} actualizados, {batch.errores} errores.",
            )
    else:
        form = ImportFileForm()
    return render(
        request,
        "crm/crmimportform.html",
        {"form": form, "titulo": titulo, "tipo": tipo, "batch": batch},
    )
