from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import DetailView, ListView

from apps.core.models import Contacto, Entidad

from .models import Tarea
from .selectors import entidad_list_queryset, entidad_summary


class EntidadListView(LoginRequiredMixin, ListView):
    model = Entidad
    template_name = "wcgone/crm/entidad_list.html"
    context_object_name = "entidades"
    paginate_by = 25

    def get_queryset(self):
        return entidad_list_queryset(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = entidad_list_queryset(self.request)
        context["summary"] = entidad_summary(qs)
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "CRM — Clientes"},
        ]
        context["tipo_choices"] = Entidad.TIPO_CHOICES
        context["export_query"] = self.request.GET.urlencode()
        return context


class EntidadDetailView(LoginRequiredMixin, DetailView):
    model = Entidad
    template_name = "wcgone/crm/entidad_detail.html"
    context_object_name = "entidad"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entidad = self.object
        context["contactos"] = entidad.contactos.filter(activo=True).order_by("nombre")
        context["relaciones_producto"] = entidad.relaciones_producto.select_related(
            "producto", "unidad_negocio"
        )
        context["interacciones"] = entidad.interacciones.select_related("usuario").order_by(
            "-fecha"
        )[:10]
        context["tareas"] = entidad.tareas.filter(completada=False).order_by("fecha_limite")[:10]
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "CRM — Clientes", "url": "/wcgone/crm/entidades/"},
            {"label": entidad.nombre},
        ]
        return context


class ContactoListView(LoginRequiredMixin, ListView):
    model = Contacto
    template_name = "wcgone/crm/contacto_list.html"
    context_object_name = "contactos"
    paginate_by = 25

    def get_queryset(self):
        qs = Contacto.objects.select_related("entidad").order_by("entidad__nombre", "nombre")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(email__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "CRM — Clientes", "url": "/wcgone/crm/entidades/"},
            {"label": "Contactos"},
        ]
        return context


class TareaListView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = "wcgone/crm/tarea_list.html"
    context_object_name = "tareas"
    paginate_by = 25

    def get_queryset(self):
        qs = Tarea.objects.select_related("entidad", "asignado_a").order_by(
            "completada", "fecha_limite"
        )
        estado = self.request.GET.get("estado", "").strip()
        if estado:
            qs = qs.filter(estado=estado)
        if self.request.GET.get("pendientes") == "1":
            qs = qs.filter(completada=False)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "CRM — Clientes", "url": "/wcgone/crm/entidades/"},
            {"label": "Tareas"},
        ]
        return context


from django.contrib import messages  # noqa: E402
from django.contrib.auth.decorators import login_required  # noqa: E402
from django.shortcuts import redirect, render  # noqa: E402
from django.utils import timezone  # noqa: E402

from apps.core.exports import csv_response  # noqa: E402
from apps.core.forms import ImportFileForm  # noqa: E402

from .imports.entidades import import_entidades_clientes  # noqa: E402
from .selectors import entidad_list_queryset  # noqa: E402


@login_required
def export_entidades_csv(request):
    qs = entidad_list_queryset(request)
    rows = []
    for e in qs:
        rows.append([
            e.nombre,
            e.nit or "",
            e.get_tipo_entidad_display(),
            e.ciudad or "",
            e.categoria_riesgo or "",
            "Activo" if e.activo else "Inactivo",
            e.num_contactos,
            e.num_productos,
            e.email or "",
            e.telefono or "",
        ])
    filename = f"crm_entidades_{timezone.localdate().isoformat()}.csv"
    return csv_response(
        filename,
        [
            "Nombre",
            "NIT",
            "Tipo",
            "Ciudad",
            "Categoría riesgo",
            "Estado",
            "Contactos",
            "Productos",
            "Email",
            "Teléfono",
        ],
        rows,
    )


@login_required
def importar_entidades(request):
    if request.method == "POST":
        form = ImportFileForm(request.POST, request.FILES)
        if form.is_valid():
            batch = import_entidades_clientes(request.user, form.cleaned_data["archivo"])
            messages.success(
                request,
                f"Importación CRM finalizada ({batch.get_estado_display()}): "
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
            "titulo": "Importar entidades / clientes CRM",
            "descripcion": "Carga CSV o XLSX con columnas mínimas: NIT o Nombre.",
            "columnas_ejemplo": "NIT, Nombre, UNE, Tipo, Teléfono, Email, Contacto, Cargo",
            "breadcrumbs": [
                {"label": "Panel principal", "url": "/panel/"},
                {"label": "CRM — Clientes", "url": "/wcgone/crm/entidades/"},
                {"label": "Importar entidades"},
            ],
        },
    )
