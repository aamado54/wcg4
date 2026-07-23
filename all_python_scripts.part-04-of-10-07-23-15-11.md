# CONCATENATED .PY FILES

PART_NUMBER=4
TOTAL_PARTS=10

DOCUMENT_MODE=LITERAL_CODE_ARCHIVE
PARSING_PRIORITY=PATH_LITERAL->CONTENT_NUMBERED_BEGIN->CONTENT_BASE64_BEGIN->CONTENT_BEGIN
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
RECORD_SEPARATOR=BEGIN_LITERAL_FILE_RECORD|END_LITERAL_FILE_RECORD
RECORD_BOUNDARY=========== RECORD_BOUNDARY ==========
CONTENT_POLICY=PRESERVE_EXACT_TEXT_WITH_METADATA_AND_NUMBERED_FALLBACK
READING_HINT=Prefer PATH_LITERAL first for file identity. Prefer CONTENT_NUMBERED_BEGIN for faithful line-by-line reading. Use CONTENT_BASE64_BEGIN for exact reconstruction when available. Use CONTENT_BEGIN only as a convenience view. If CONTENT_BEGIN looks compacted, flattened, or visually altered, do not use it to infer exact identifiers, variable names, paths, punctuation grouping, or spacing.
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=crm/views.py
PATH_JSON="crm/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=160
SIZE_BYTES_UTF8=5459
CONTENT_SHA256=2905260c11fc47ebfdd2b4045f9dab190271795dc47593c21dc88e1944c7597e
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
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

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib import messages
00002|from django.contrib.auth.decorators import login_required
00003|from django.contrib.auth.mixins import LoginRequiredMixin
00004|from django.db.models import Q
00005|from django.http import HttpResponse
00006|from django.shortcuts import get_object_or_404, redirect, render
00007|from django.views.generic import DetailView, ListView
00008|
00009|from core.wcg_models import Contacto, Entidad, UnidadNegocio
00010|from crm.models import Tarea
00011|from crm.selectors import entidad_list_queryset, entidad_summary
00012|
00013|from .forms import InteraccionForm, TareaForm
00014|
00015|
00016|class EntidadListView(LoginRequiredMixin, ListView):
00017|    model = Entidad
00018|    template_name = "crm/crmentitylist.html"
00019|    context_object_name = "entidades"
00020|    paginate_by = 50
00021|
00022|    def get_queryset(self):
00023|        return entidad_list_queryset(self.request)
00024|
00025|    def get_context_data(self, **kwargs):
00026|        ctx = super().get_context_data(**kwargs)
00027|        ctx["unidades"] = UnidadNegocio.objects.filter(activa=True).order_by("nombre")
00028|        ctx["tipos"] = Entidad.TIPO_CHOICES
00029|        ctx["summary"] = entidad_summary(Entidad.objects.all())
00030|        ctx["breadcrumbs"] = [
00031|            {"label": "Panel principal", "url": "/panel/"},
00032|            {"label": "CRM — Clientes"},
00033|        ]
00034|        return ctx
00035|
00036|
00037|class EntidadDetailView(LoginRequiredMixin, DetailView):
00038|    model = Entidad
00039|    template_name = "crm/crmentitydetail.html"
00040|    context_object_name = "entidad"
00041|    slug_field = "codigo"
00042|    slug_url_kwarg = "codigo"
00043|
00044|    def get_context_data(self, **kwargs):
00045|        ctx = super().get_context_data(**kwargs)
00046|        entidad = self.object
00047|        contactos = list(entidad.contactos.filter(activo=True))
00048|        ctx["interacciones"] = entidad.interacciones.select_related("usuario")[:20]
00049|        ctx["tareas"] = entidad.tareas.exclude(estado=Tarea.ESTADO_HECHA).exclude(
00050|            estado=Tarea.ESTADO_CANCELADA
00051|        ).select_related("asignado_a")[:20]
00052|        ctx["contactos"] = contactos
00053|        ctx["productos"] = entidad.productos_relacionados.select_related(
00054|            "producto", "producto__unidad_negocio"
00055|        )
00056|        ctx["contacto_principal"] = next(
00057|            (c for c in contactos if c.es_principal),
00058|            contactos[0] if contactos else None,
00059|        )
00060|        ctx["breadcrumbs"] = [
00061|            {"label": "Panel principal", "url": "/panel/"},
00062|            {"label": "CRM — Clientes", "url": "/crm/"},
00063|            {"label": entidad.nombre},
00064|        ]
00065|        return ctx
00066|
00067|
00068|class ContactoListView(LoginRequiredMixin, ListView):
00069|    model = Contacto
00070|    template_name = "crm/crmcontactolist.html"
00071|    context_object_name = "contactos"
00072|    paginate_by = 50
00073|
00074|    def get_queryset(self):
00075|        qs = Contacto.objects.select_related("entidad").filter(activo=True).order_by(
00076|            "entidad__nombre", "nombre"
00077|        )
00078|        q = self.request.GET.get("q", "").strip()
00079|        if q:
00080|            qs = qs.filter(
00081|                Q(nombre__icontains=q)
00082|                | Q(email__icontains=q)
00083|                | Q(entidad__nombre__icontains=q)
00084|            )
00085|        return qs
00086|
00087|
00088|class TareaListView(LoginRequiredMixin, ListView):
00089|    model = Tarea
00090|    template_name = "crm/crmtarealist.html"
00091|    context_object_name = "tareas"
00092|    paginate_by = 50
00093|
00094|    def get_queryset(self):
00095|        return Tarea.objects.select_related("entidad", "asignado_a").order_by(
00096|            "-fecha_vencimiento"
00097|        )
00098|
00099|
00100|@login_required
00101|def nueva_interaccion(request, codigo):
00102|    entidad = get_object_or_404(Entidad, codigo=codigo)
00103|    if request.method == "POST":
00104|        form = InteraccionForm(request.POST)
00105|        if form.is_valid():
00106|            inter = form.save(commit=False)
00107|            inter.entidad = entidad
00108|            inter.usuario = request.user
00109|            inter.save()
00110|            messages.success(request, "Interacción registrada.")
00111|            return redirect("crm:entidad_detail", codigo=entidad.codigo)
00112|    else:
00113|        form = InteraccionForm()
00114|    return render(request, "crm/crminteractionform.html", {"form": form, "entidad": entidad})
00115|
00116|
00117|@login_required
00118|def nueva_tarea(request, codigo):
00119|    entidad = get_object_or_404(Entidad, codigo=codigo)
00120|    if request.method == "POST":
00121|        form = TareaForm(request.POST)
00122|        if form.is_valid():
00123|            tarea = form.save(commit=False)
00124|            tarea.entidad = entidad
00125|            if not tarea.asignado_a:
00126|                tarea.asignado_a = request.user
00127|            tarea.save()
00128|            messages.success(request, "Tarea creada.")
00129|            return redirect("crm:entidad_detail", codigo=entidad.codigo)
00130|    else:
00131|        form = TareaForm(initial={"asignado_a": request.user.pk})
00132|    return render(request, "crm/crmtaskform.html", {"form": form, "entidad": entidad})
00133|
00134|
00135|@login_required
00136|def importar(request, tipo=None):
00137|    return redirect("imports:import_hub")
00138|
00139|
00140|@login_required
00141|def export_entidades(request):
00142|    import csv
00143|
00144|    qs = entidad_list_queryset(request)
00145|    response = HttpResponse(content_type="text/csv")
00146|    response["Content-Disposition"] = 'attachment; filename="crm_entidades.csv"'
00147|    writer = csv.writer(response)
00148|    writer.writerow(["codigo", "nombre", "nit", "tipo", "unidad", "activa"])
00149|    for e in qs:
00150|        writer.writerow(
00151|            [
00152|                e.codigo,
00153|                e.nombre,
00154|                e.nit,
00155|                e.tipo,
00156|                e.unidad_negocio.code if e.unidad_negocio else "",
00157|                "1" if e.activa else "0",
00158|            ]
00159|        )
00160|    return response

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgbWVzc2FnZXMKZnJvbSBkamFuZ28uY29udHJpYi5hdXRoLmRlY29yYXRvcnMgaW1wb3J0IGxvZ2luX3JlcXVpcmVkCmZyb20gZGphbmdvLmNvbnRyaWIuYXV0aC5taXhpbnMgaW1wb3J0IExvZ2luUmVxdWlyZWRNaXhpbgpmcm9tIGRqYW5nby5kYi5tb2RlbHMgaW1wb3J0IFEKZnJvbSBkamFuZ28uaHR0cCBpbXBvcnQgSHR0cFJlc3BvbnNlCmZyb20gZGphbmdvLnNob3J0Y3V0cyBpbXBvcnQgZ2V0X29iamVjdF9vcl80MDQsIHJlZGlyZWN0LCByZW5kZXIKZnJvbSBkamFuZ28udmlld3MuZ2VuZXJpYyBpbXBvcnQgRGV0YWlsVmlldywgTGlzdFZpZXcKCmZyb20gY29yZS53Y2dfbW9kZWxzIGltcG9ydCBDb250YWN0bywgRW50aWRhZCwgVW5pZGFkTmVnb2Npbwpmcm9tIGNybS5tb2RlbHMgaW1wb3J0IFRhcmVhCmZyb20gY3JtLnNlbGVjdG9ycyBpbXBvcnQgZW50aWRhZF9saXN0X3F1ZXJ5c2V0LCBlbnRpZGFkX3N1bW1hcnkKCmZyb20gLmZvcm1zIGltcG9ydCBJbnRlcmFjY2lvbkZvcm0sIFRhcmVhRm9ybQoKCmNsYXNzIEVudGlkYWRMaXN0VmlldyhMb2dpblJlcXVpcmVkTWl4aW4sIExpc3RWaWV3KToKICAgIG1vZGVsID0gRW50aWRhZAogICAgdGVtcGxhdGVfbmFtZSA9ICJjcm0vY3JtZW50aXR5bGlzdC5odG1sIgogICAgY29udGV4dF9vYmplY3RfbmFtZSA9ICJlbnRpZGFkZXMiCiAgICBwYWdpbmF0ZV9ieSA9IDUwCgogICAgZGVmIGdldF9xdWVyeXNldChzZWxmKToKICAgICAgICByZXR1cm4gZW50aWRhZF9saXN0X3F1ZXJ5c2V0KHNlbGYucmVxdWVzdCkKCiAgICBkZWYgZ2V0X2NvbnRleHRfZGF0YShzZWxmLCAqKmt3YXJncyk6CiAgICAgICAgY3R4ID0gc3VwZXIoKS5nZXRfY29udGV4dF9kYXRhKCoqa3dhcmdzKQogICAgICAgIGN0eFsidW5pZGFkZXMiXSA9IFVuaWRhZE5lZ29jaW8ub2JqZWN0cy5maWx0ZXIoYWN0aXZhPVRydWUpLm9yZGVyX2J5KCJub21icmUiKQogICAgICAgIGN0eFsidGlwb3MiXSA9IEVudGlkYWQuVElQT19DSE9JQ0VTCiAgICAgICAgY3R4WyJzdW1tYXJ5Il0gPSBlbnRpZGFkX3N1bW1hcnkoRW50aWRhZC5vYmplY3RzLmFsbCgpKQogICAgICAgIGN0eFsiYnJlYWRjcnVtYnMiXSA9IFsKICAgICAgICAgICAgeyJsYWJlbCI6ICJQYW5lbCBwcmluY2lwYWwiLCAidXJsIjogIi9wYW5lbC8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJDUk0g4oCUIENsaWVudGVzIn0sCiAgICAgICAgXQogICAgICAgIHJldHVybiBjdHgKCgpjbGFzcyBFbnRpZGFkRGV0YWlsVmlldyhMb2dpblJlcXVpcmVkTWl4aW4sIERldGFpbFZpZXcpOgogICAgbW9kZWwgPSBFbnRpZGFkCiAgICB0ZW1wbGF0ZV9uYW1lID0gImNybS9jcm1lbnRpdHlkZXRhaWwuaHRtbCIKICAgIGNvbnRleHRfb2JqZWN0X25hbWUgPSAiZW50aWRhZCIKICAgIHNsdWdfZmllbGQgPSAiY29kaWdvIgogICAgc2x1Z191cmxfa3dhcmcgPSAiY29kaWdvIgoKICAgIGRlZiBnZXRfY29udGV4dF9kYXRhKHNlbGYsICoqa3dhcmdzKToKICAgICAgICBjdHggPSBzdXBlcigpLmdldF9jb250ZXh0X2RhdGEoKiprd2FyZ3MpCiAgICAgICAgZW50aWRhZCA9IHNlbGYub2JqZWN0CiAgICAgICAgY29udGFjdG9zID0gbGlzdChlbnRpZGFkLmNvbnRhY3Rvcy5maWx0ZXIoYWN0aXZvPVRydWUpKQogICAgICAgIGN0eFsiaW50ZXJhY2Npb25lcyJdID0gZW50aWRhZC5pbnRlcmFjY2lvbmVzLnNlbGVjdF9yZWxhdGVkKCJ1c3VhcmlvIilbOjIwXQogICAgICAgIGN0eFsidGFyZWFzIl0gPSBlbnRpZGFkLnRhcmVhcy5leGNsdWRlKGVzdGFkbz1UYXJlYS5FU1RBRE9fSEVDSEEpLmV4Y2x1ZGUoCiAgICAgICAgICAgIGVzdGFkbz1UYXJlYS5FU1RBRE9fQ0FOQ0VMQURBCiAgICAgICAgKS5zZWxlY3RfcmVsYXRlZCgiYXNpZ25hZG9fYSIpWzoyMF0KICAgICAgICBjdHhbImNvbnRhY3RvcyJdID0gY29udGFjdG9zCiAgICAgICAgY3R4WyJwcm9kdWN0b3MiXSA9IGVudGlkYWQucHJvZHVjdG9zX3JlbGFjaW9uYWRvcy5zZWxlY3RfcmVsYXRlZCgKICAgICAgICAgICAgInByb2R1Y3RvIiwgInByb2R1Y3RvX191bmlkYWRfbmVnb2NpbyIKICAgICAgICApCiAgICAgICAgY3R4WyJjb250YWN0b19wcmluY2lwYWwiXSA9IG5leHQoCiAgICAgICAgICAgIChjIGZvciBjIGluIGNvbnRhY3RvcyBpZiBjLmVzX3ByaW5jaXBhbCksCiAgICAgICAgICAgIGNvbnRhY3Rvc1swXSBpZiBjb250YWN0b3MgZWxzZSBOb25lLAogICAgICAgICkKICAgICAgICBjdHhbImJyZWFkY3J1bWJzIl0gPSBbCiAgICAgICAgICAgIHsibGFiZWwiOiAiUGFuZWwgcHJpbmNpcGFsIiwgInVybCI6ICIvcGFuZWwvIn0sCiAgICAgICAgICAgIHsibGFiZWwiOiAiQ1JNIOKAlCBDbGllbnRlcyIsICJ1cmwiOiAiL2NybS8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6IGVudGlkYWQubm9tYnJlfSwKICAgICAgICBdCiAgICAgICAgcmV0dXJuIGN0eAoKCmNsYXNzIENvbnRhY3RvTGlzdFZpZXcoTG9naW5SZXF1aXJlZE1peGluLCBMaXN0Vmlldyk6CiAgICBtb2RlbCA9IENvbnRhY3RvCiAgICB0ZW1wbGF0ZV9uYW1lID0gImNybS9jcm1jb250YWN0b2xpc3QuaHRtbCIKICAgIGNvbnRleHRfb2JqZWN0X25hbWUgPSAiY29udGFjdG9zIgogICAgcGFnaW5hdGVfYnkgPSA1MAoKICAgIGRlZiBnZXRfcXVlcnlzZXQoc2VsZik6CiAgICAgICAgcXMgPSBDb250YWN0by5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJlbnRpZGFkIikuZmlsdGVyKGFjdGl2bz1UcnVlKS5vcmRlcl9ieSgKICAgICAgICAgICAgImVudGlkYWRfX25vbWJyZSIsICJub21icmUiCiAgICAgICAgKQogICAgICAgIHEgPSBzZWxmLnJlcXVlc3QuR0VULmdldCgicSIsICIiKS5zdHJpcCgpCiAgICAgICAgaWYgcToKICAgICAgICAgICAgcXMgPSBxcy5maWx0ZXIoCiAgICAgICAgICAgICAgICBRKG5vbWJyZV9faWNvbnRhaW5zPXEpCiAgICAgICAgICAgICAgICB8IFEoZW1haWxfX2ljb250YWlucz1xKQogICAgICAgICAgICAgICAgfCBRKGVudGlkYWRfX25vbWJyZV9faWNvbnRhaW5zPXEpCiAgICAgICAgICAgICkKICAgICAgICByZXR1cm4gcXMKCgpjbGFzcyBUYXJlYUxpc3RWaWV3KExvZ2luUmVxdWlyZWRNaXhpbiwgTGlzdFZpZXcpOgogICAgbW9kZWwgPSBUYXJlYQogICAgdGVtcGxhdGVfbmFtZSA9ICJjcm0vY3JtdGFyZWFsaXN0Lmh0bWwiCiAgICBjb250ZXh0X29iamVjdF9uYW1lID0gInRhcmVhcyIKICAgIHBhZ2luYXRlX2J5ID0gNTAKCiAgICBkZWYgZ2V0X3F1ZXJ5c2V0KHNlbGYpOgogICAgICAgIHJldHVybiBUYXJlYS5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJlbnRpZGFkIiwgImFzaWduYWRvX2EiKS5vcmRlcl9ieSgKICAgICAgICAgICAgIi1mZWNoYV92ZW5jaW1pZW50byIKICAgICAgICApCgoKQGxvZ2luX3JlcXVpcmVkCmRlZiBudWV2YV9pbnRlcmFjY2lvbihyZXF1ZXN0LCBjb2RpZ28pOgogICAgZW50aWRhZCA9IGdldF9vYmplY3Rfb3JfNDA0KEVudGlkYWQsIGNvZGlnbz1jb2RpZ28pCiAgICBpZiByZXF1ZXN0Lm1ldGhvZCA9PSAiUE9TVCI6CiAgICAgICAgZm9ybSA9IEludGVyYWNjaW9uRm9ybShyZXF1ZXN0LlBPU1QpCiAgICAgICAgaWYgZm9ybS5pc192YWxpZCgpOgogICAgICAgICAgICBpbnRlciA9IGZvcm0uc2F2ZShjb21taXQ9RmFsc2UpCiAgICAgICAgICAgIGludGVyLmVudGlkYWQgPSBlbnRpZGFkCiAgICAgICAgICAgIGludGVyLnVzdWFyaW8gPSByZXF1ZXN0LnVzZXIKICAgICAgICAgICAgaW50ZXIuc2F2ZSgpCiAgICAgICAgICAgIG1lc3NhZ2VzLnN1Y2Nlc3MocmVxdWVzdCwgIkludGVyYWNjacOzbiByZWdpc3RyYWRhLiIpCiAgICAgICAgICAgIHJldHVybiByZWRpcmVjdCgiY3JtOmVudGlkYWRfZGV0YWlsIiwgY29kaWdvPWVudGlkYWQuY29kaWdvKQogICAgZWxzZToKICAgICAgICBmb3JtID0gSW50ZXJhY2Npb25Gb3JtKCkKICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgImNybS9jcm1pbnRlcmFjdGlvbmZvcm0uaHRtbCIsIHsiZm9ybSI6IGZvcm0sICJlbnRpZGFkIjogZW50aWRhZH0pCgoKQGxvZ2luX3JlcXVpcmVkCmRlZiBudWV2YV90YXJlYShyZXF1ZXN0LCBjb2RpZ28pOgogICAgZW50aWRhZCA9IGdldF9vYmplY3Rfb3JfNDA0KEVudGlkYWQsIGNvZGlnbz1jb2RpZ28pCiAgICBpZiByZXF1ZXN0Lm1ldGhvZCA9PSAiUE9TVCI6CiAgICAgICAgZm9ybSA9IFRhcmVhRm9ybShyZXF1ZXN0LlBPU1QpCiAgICAgICAgaWYgZm9ybS5pc192YWxpZCgpOgogICAgICAgICAgICB0YXJlYSA9IGZvcm0uc2F2ZShjb21taXQ9RmFsc2UpCiAgICAgICAgICAgIHRhcmVhLmVudGlkYWQgPSBlbnRpZGFkCiAgICAgICAgICAgIGlmIG5vdCB0YXJlYS5hc2lnbmFkb19hOgogICAgICAgICAgICAgICAgdGFyZWEuYXNpZ25hZG9fYSA9IHJlcXVlc3QudXNlcgogICAgICAgICAgICB0YXJlYS5zYXZlKCkKICAgICAgICAgICAgbWVzc2FnZXMuc3VjY2VzcyhyZXF1ZXN0LCAiVGFyZWEgY3JlYWRhLiIpCiAgICAgICAgICAgIHJldHVybiByZWRpcmVjdCgiY3JtOmVudGlkYWRfZGV0YWlsIiwgY29kaWdvPWVudGlkYWQuY29kaWdvKQogICAgZWxzZToKICAgICAgICBmb3JtID0gVGFyZWFGb3JtKGluaXRpYWw9eyJhc2lnbmFkb19hIjogcmVxdWVzdC51c2VyLnBrfSkKICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgImNybS9jcm10YXNrZm9ybS5odG1sIiwgeyJmb3JtIjogZm9ybSwgImVudGlkYWQiOiBlbnRpZGFkfSkKCgpAbG9naW5fcmVxdWlyZWQKZGVmIGltcG9ydGFyKHJlcXVlc3QsIHRpcG89Tm9uZSk6CiAgICByZXR1cm4gcmVkaXJlY3QoImltcG9ydHM6aW1wb3J0X2h1YiIpCgoKQGxvZ2luX3JlcXVpcmVkCmRlZiBleHBvcnRfZW50aWRhZGVzKHJlcXVlc3QpOgogICAgaW1wb3J0IGNzdgoKICAgIHFzID0gZW50aWRhZF9saXN0X3F1ZXJ5c2V0KHJlcXVlc3QpCiAgICByZXNwb25zZSA9IEh0dHBSZXNwb25zZShjb250ZW50X3R5cGU9InRleHQvY3N2IikKICAgIHJlc3BvbnNlWyJDb250ZW50LURpc3Bvc2l0aW9uIl0gPSAnYXR0YWNobWVudDsgZmlsZW5hbWU9ImNybV9lbnRpZGFkZXMuY3N2IicKICAgIHdyaXRlciA9IGNzdi53cml0ZXIocmVzcG9uc2UpCiAgICB3cml0ZXIud3JpdGVyb3coWyJjb2RpZ28iLCAibm9tYnJlIiwgIm5pdCIsICJ0aXBvIiwgInVuaWRhZCIsICJhY3RpdmEiXSkKICAgIGZvciBlIGluIHFzOgogICAgICAgIHdyaXRlci53cml0ZXJvdygKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgZS5jb2RpZ28sCiAgICAgICAgICAgICAgICBlLm5vbWJyZSwKICAgICAgICAgICAgICAgIGUubml0LAogICAgICAgICAgICAgICAgZS50aXBvLAogICAgICAgICAgICAgICAgZS51bmlkYWRfbmVnb2Npby5jb2RlIGlmIGUudW5pZGFkX25lZ29jaW8gZWxzZSAiIiwKICAgICAgICAgICAgICAgICIxIiBpZiBlLmFjdGl2YSBlbHNlICIwIiwKICAgICAgICAgICAgXQogICAgICAgICkKICAgIHJldHVybiByZXNwb25zZQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=feedback/__init__.py
PATH_JSON="feedback/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=feedback/admin.py
PATH_JSON="feedback/admin.py"
FILENAME=admin.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=3
SIZE_BYTES_UTF8=63
CONTENT_SHA256=b2e328e31f08dc907100505521d13ee6a9ea67a240655d051120011ce49cfaf8
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.contrib import admin

# Register your models here.

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib import admin
00002|
00003|# Register your models here.

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgYWRtaW4KCiMgUmVnaXN0ZXIgeW91ciBtb2RlbHMgaGVyZS4K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=feedback/apps.py
PATH_JSON="feedback/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=6
SIZE_BYTES_UTF8=148
CONTENT_SHA256=dad47b767fd0c6d2af2a2a9c9e34aaae27332110c535605aac73e9780e1dd8f5
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "feedback"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class FeedbackConfig(AppConfig):
00005|    default_auto_field = "django.db.models.BigAutoField"
00006|    name = "feedback"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgRmVlZGJhY2tDb25maWcoQXBwQ29uZmlnKToKICAgIGRlZmF1bHRfYXV0b19maWVsZCA9ICJkamFuZ28uZGIubW9kZWxzLkJpZ0F1dG9GaWVsZCIKICAgIG5hbWUgPSAiZmVlZGJhY2siCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=feedback/models.py
PATH_JSON="feedback/models.py"
FILENAME=models.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=3
SIZE_BYTES_UTF8=57
CONTENT_SHA256=563734a765db00f804e87c9317abe597df00e1e0e103902f690aac738910f404
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.db import models

# Create your models here.

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.db import models
00002|
00003|# Create your models here.

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uZGIgaW1wb3J0IG1vZGVscwoKIyBDcmVhdGUgeW91ciBtb2RlbHMgaGVyZS4K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=feedback/tests.py
PATH_JSON="feedback/tests.py"
FILENAME=tests.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=3
SIZE_BYTES_UTF8=60
CONTENT_SHA256=9ab6c6191360e63c1b4c9b5659aef348a743c9e078be68190917369e4e9563e8
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.test import TestCase

# Create your tests here.

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.test import TestCase
00002|
00003|# Create your tests here.

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udGVzdCBpbXBvcnQgVGVzdENhc2UKCiMgQ3JlYXRlIHlvdXIgdGVzdHMgaGVyZS4K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=feedback/views.py
PATH_JSON="feedback/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=3
SIZE_BYTES_UTF8=63
CONTENT_SHA256=c5cd48407aec8a3ee3df74d46e8fbfa1ec32defb34de9c3f7ada4159a318265d
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.shortcuts import render

# Create your views here.

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.shortcuts import render
00002|
00003|# Create your views here.

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uc2hvcnRjdXRzIGltcG9ydCByZW5kZXIKCiMgQ3JlYXRlIHlvdXIgdmlld3MgaGVyZS4K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/__init__.py
PATH_JSON="imports/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/admin.py
PATH_JSON="imports/admin.py"
FILENAME=admin.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=167
SIZE_BYTES_UTF8=4374
CONTENT_SHA256=093b96a11072d054eea1f91b49c2e01902bcc8e14e02772131ae951fd5ccd0ff
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.contrib import admin
from .models import (
    FileUpload,
    FileImportLog,
    FinancialStatementImportHeader,
    NewClientImportHeader,
    CrossSaleImportHeader,
    StationTimeImportHeader,
    NewClientImportRow,
    CrossSaleImportRow,
)


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = (
        "original_filename",
        "file_type_detected",
        "file_format",
        "detected_year",
        "detected_month",
        "status",
        "uploaded_by",
        "created_at",
    )
    list_filter = (
        "file_type_detected",
        "file_format",
        "status",
        "detected_year",
        "detected_month",
    )
    search_fields = ("original_filename", "uploaded_by__username", "uploaded_by__email")
    readonly_fields = (
        "uploaded_by",
        "file_size_bytes",
        "sha256",
        "mime_type",
        "original_filename",
        "detected_year",
        "detected_month",
        "status",
        "error_summary",
        "parsing_notes",
        "created_at",
        "updated_at",
    )
    fields = (
        "stored_file",
        "uploaded_by",
        "original_filename",
        "file_type_detected",
        "file_format",
        "detected_year",
        "detected_month",
        "file_size_bytes",
        "status",
        "error_summary",
        "parsing_notes",
        "created_at",
        "updated_at",
    )

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(FileImportLog)
class FileImportLogAdmin(admin.ModelAdmin):
    list_display = ("file_upload", "level", "step_code", "line_number", "created_at")
    list_filter = ("level", "step_code")
    search_fields = ("file_upload__original_filename", "message")


@admin.register(FinancialStatementImportHeader)
class FinancialStatementImportHeaderAdmin(admin.ModelAdmin):
    list_display = ("file_upload", "une", "year", "month", "statement_type")
    list_filter = ("une", "year", "month", "statement_type")
    search_fields = ("file_upload__original_filename",)


@admin.register(NewClientImportHeader)
class NewClientImportHeaderAdmin(admin.ModelAdmin):
    list_display = ("file_upload", "year", "month")
    list_filter = ("year", "month")
    search_fields = ("file_upload__original_filename",)


@admin.register(CrossSaleImportHeader)
class CrossSaleImportHeaderAdmin(admin.ModelAdmin):
    list_display = ("file_upload", "year", "month")
    list_filter = ("year", "month")
    search_fields = ("file_upload__original_filename",)


@admin.register(StationTimeImportHeader)
class StationTimeImportHeaderAdmin(admin.ModelAdmin):
    list_display = ("file_upload", "year", "month")
    list_filter = ("year", "month")
    search_fields = ("file_upload__original_filename",)


@admin.register(NewClientImportRow)
class NewClientImportRowAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "month",
        "une",
        "client_name",
        "nit",
        "operation_code",
        "previous_contracts",
        "counts_as_new",
        "currency",
        "amount",
    )
    list_filter = (
        "year",
        "month",
        "une",
        "counts_as_new",
        "currency",
    )
    search_fields = (
        "client_name",
        "nit",
        "operation_code",
        "une__code",
        "une__name_es",
        "raw_une_value",
    )
    autocomplete_fields = ("une", "currency")
    list_select_related = ("header", "une", "currency")


@admin.register(CrossSaleImportRow)
class CrossSaleImportRowAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "month",
        "une_origin",
        "une_destination",
        "client_name",
        "operation_code",
        "date",
        "currency",
    )
    list_filter = (
        "year",
        "month",
        "une_origin",
        "une_destination",
        "currency",
    )
    search_fields = (
        "client_name",
        "operation_code",
        "raw_une_origin",
        "raw_une_destination",
        "une_origin__code",
        "une_destination__code",
    )
    autocomplete_fields = ("une_origin", "une_destination", "currency")
    list_select_related = ("header", "une_origin", "une_destination", "currency")
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib import admin
00002|from .models import (
00003|    FileUpload,
00004|    FileImportLog,
00005|    FinancialStatementImportHeader,
00006|    NewClientImportHeader,
00007|    CrossSaleImportHeader,
00008|    StationTimeImportHeader,
00009|    NewClientImportRow,
00010|    CrossSaleImportRow,
00011|)
00012|
00013|
00014|@admin.register(FileUpload)
00015|class FileUploadAdmin(admin.ModelAdmin):
00016|    list_display = (
00017|        "original_filename",
00018|        "file_type_detected",
00019|        "file_format",
00020|        "detected_year",
00021|        "detected_month",
00022|        "status",
00023|        "uploaded_by",
00024|        "created_at",
00025|    )
00026|    list_filter = (
00027|        "file_type_detected",
00028|        "file_format",
00029|        "status",
00030|        "detected_year",
00031|        "detected_month",
00032|    )
00033|    search_fields = ("original_filename", "uploaded_by__username", "uploaded_by__email")
00034|    readonly_fields = (
00035|        "uploaded_by",
00036|        "file_size_bytes",
00037|        "sha256",
00038|        "mime_type",
00039|        "original_filename",
00040|        "detected_year",
00041|        "detected_month",
00042|        "status",
00043|        "error_summary",
00044|        "parsing_notes",
00045|        "created_at",
00046|        "updated_at",
00047|    )
00048|    fields = (
00049|        "stored_file",
00050|        "uploaded_by",
00051|        "original_filename",
00052|        "file_type_detected",
00053|        "file_format",
00054|        "detected_year",
00055|        "detected_month",
00056|        "file_size_bytes",
00057|        "status",
00058|        "error_summary",
00059|        "parsing_notes",
00060|        "created_at",
00061|        "updated_at",
00062|    )
00063|
00064|    def save_model(self, request, obj, form, change):
00065|        if not obj.uploaded_by:
00066|            obj.uploaded_by = request.user
00067|        super().save_model(request, obj, form, change)
00068|
00069|
00070|@admin.register(FileImportLog)
00071|class FileImportLogAdmin(admin.ModelAdmin):
00072|    list_display = ("file_upload", "level", "step_code", "line_number", "created_at")
00073|    list_filter = ("level", "step_code")
00074|    search_fields = ("file_upload__original_filename", "message")
00075|
00076|
00077|@admin.register(FinancialStatementImportHeader)
00078|class FinancialStatementImportHeaderAdmin(admin.ModelAdmin):
00079|    list_display = ("file_upload", "une", "year", "month", "statement_type")
00080|    list_filter = ("une", "year", "month", "statement_type")
00081|    search_fields = ("file_upload__original_filename",)
00082|
00083|
00084|@admin.register(NewClientImportHeader)
00085|class NewClientImportHeaderAdmin(admin.ModelAdmin):
00086|    list_display = ("file_upload", "year", "month")
00087|    list_filter = ("year", "month")
00088|    search_fields = ("file_upload__original_filename",)
00089|
00090|
00091|@admin.register(CrossSaleImportHeader)
00092|class CrossSaleImportHeaderAdmin(admin.ModelAdmin):
00093|    list_display = ("file_upload", "year", "month")
00094|    list_filter = ("year", "month")
00095|    search_fields = ("file_upload__original_filename",)
00096|
00097|
00098|@admin.register(StationTimeImportHeader)
00099|class StationTimeImportHeaderAdmin(admin.ModelAdmin):
00100|    list_display = ("file_upload", "year", "month")
00101|    list_filter = ("year", "month")
00102|    search_fields = ("file_upload__original_filename",)
00103|
00104|
00105|@admin.register(NewClientImportRow)
00106|class NewClientImportRowAdmin(admin.ModelAdmin):
00107|    list_display = (
00108|        "year",
00109|        "month",
00110|        "une",
00111|        "client_name",
00112|        "nit",
00113|        "operation_code",
00114|        "previous_contracts",
00115|        "counts_as_new",
00116|        "currency",
00117|        "amount",
00118|    )
00119|    list_filter = (
00120|        "year",
00121|        "month",
00122|        "une",
00123|        "counts_as_new",
00124|        "currency",
00125|    )
00126|    search_fields = (
00127|        "client_name",
00128|        "nit",
00129|        "operation_code",
00130|        "une__code",
00131|        "une__name_es",
00132|        "raw_une_value",
00133|    )
00134|    autocomplete_fields = ("une", "currency")
00135|    list_select_related = ("header", "une", "currency")
00136|
00137|
00138|@admin.register(CrossSaleImportRow)
00139|class CrossSaleImportRowAdmin(admin.ModelAdmin):
00140|    list_display = (
00141|        "year",
00142|        "month",
00143|        "une_origin",
00144|        "une_destination",
00145|        "client_name",
00146|        "operation_code",
00147|        "date",
00148|        "currency",
00149|    )
00150|    list_filter = (
00151|        "year",
00152|        "month",
00153|        "une_origin",
00154|        "une_destination",
00155|        "currency",
00156|    )
00157|    search_fields = (
00158|        "client_name",
00159|        "operation_code",
00160|        "raw_une_origin",
00161|        "raw_une_destination",
00162|        "une_origin__code",
00163|        "une_destination__code",
00164|    )
00165|    autocomplete_fields = ("une_origin", "une_destination", "currency")
00166|    list_select_related = ("header", "une_origin", "une_destination", "currency")
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgYWRtaW4KZnJvbSAubW9kZWxzIGltcG9ydCAoCiAgICBGaWxlVXBsb2FkLAogICAgRmlsZUltcG9ydExvZywKICAgIEZpbmFuY2lhbFN0YXRlbWVudEltcG9ydEhlYWRlciwKICAgIE5ld0NsaWVudEltcG9ydEhlYWRlciwKICAgIENyb3NzU2FsZUltcG9ydEhlYWRlciwKICAgIFN0YXRpb25UaW1lSW1wb3J0SGVhZGVyLAogICAgTmV3Q2xpZW50SW1wb3J0Um93LAogICAgQ3Jvc3NTYWxlSW1wb3J0Um93LAopCgoKQGFkbWluLnJlZ2lzdGVyKEZpbGVVcGxvYWQpCmNsYXNzIEZpbGVVcGxvYWRBZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgKICAgICAgICAib3JpZ2luYWxfZmlsZW5hbWUiLAogICAgICAgICJmaWxlX3R5cGVfZGV0ZWN0ZWQiLAogICAgICAgICJmaWxlX2Zvcm1hdCIsCiAgICAgICAgImRldGVjdGVkX3llYXIiLAogICAgICAgICJkZXRlY3RlZF9tb250aCIsCiAgICAgICAgInN0YXR1cyIsCiAgICAgICAgInVwbG9hZGVkX2J5IiwKICAgICAgICAiY3JlYXRlZF9hdCIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgKICAgICAgICAiZmlsZV90eXBlX2RldGVjdGVkIiwKICAgICAgICAiZmlsZV9mb3JtYXQiLAogICAgICAgICJzdGF0dXMiLAogICAgICAgICJkZXRlY3RlZF95ZWFyIiwKICAgICAgICAiZGV0ZWN0ZWRfbW9udGgiLAogICAgKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgib3JpZ2luYWxfZmlsZW5hbWUiLCAidXBsb2FkZWRfYnlfX3VzZXJuYW1lIiwgInVwbG9hZGVkX2J5X19lbWFpbCIpCiAgICByZWFkb25seV9maWVsZHMgPSAoCiAgICAgICAgInVwbG9hZGVkX2J5IiwKICAgICAgICAiZmlsZV9zaXplX2J5dGVzIiwKICAgICAgICAic2hhMjU2IiwKICAgICAgICAibWltZV90eXBlIiwKICAgICAgICAib3JpZ2luYWxfZmlsZW5hbWUiLAogICAgICAgICJkZXRlY3RlZF95ZWFyIiwKICAgICAgICAiZGV0ZWN0ZWRfbW9udGgiLAogICAgICAgICJzdGF0dXMiLAogICAgICAgICJlcnJvcl9zdW1tYXJ5IiwKICAgICAgICAicGFyc2luZ19ub3RlcyIsCiAgICAgICAgImNyZWF0ZWRfYXQiLAogICAgICAgICJ1cGRhdGVkX2F0IiwKICAgICkKICAgIGZpZWxkcyA9ICgKICAgICAgICAic3RvcmVkX2ZpbGUiLAogICAgICAgICJ1cGxvYWRlZF9ieSIsCiAgICAgICAgIm9yaWdpbmFsX2ZpbGVuYW1lIiwKICAgICAgICAiZmlsZV90eXBlX2RldGVjdGVkIiwKICAgICAgICAiZmlsZV9mb3JtYXQiLAogICAgICAgICJkZXRlY3RlZF95ZWFyIiwKICAgICAgICAiZGV0ZWN0ZWRfbW9udGgiLAogICAgICAgICJmaWxlX3NpemVfYnl0ZXMiLAogICAgICAgICJzdGF0dXMiLAogICAgICAgICJlcnJvcl9zdW1tYXJ5IiwKICAgICAgICAicGFyc2luZ19ub3RlcyIsCiAgICAgICAgImNyZWF0ZWRfYXQiLAogICAgICAgICJ1cGRhdGVkX2F0IiwKICAgICkKCiAgICBkZWYgc2F2ZV9tb2RlbChzZWxmLCByZXF1ZXN0LCBvYmosIGZvcm0sIGNoYW5nZSk6CiAgICAgICAgaWYgbm90IG9iai51cGxvYWRlZF9ieToKICAgICAgICAgICAgb2JqLnVwbG9hZGVkX2J5ID0gcmVxdWVzdC51c2VyCiAgICAgICAgc3VwZXIoKS5zYXZlX21vZGVsKHJlcXVlc3QsIG9iaiwgZm9ybSwgY2hhbmdlKQoKCkBhZG1pbi5yZWdpc3RlcihGaWxlSW1wb3J0TG9nKQpjbGFzcyBGaWxlSW1wb3J0TG9nQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoImZpbGVfdXBsb2FkIiwgImxldmVsIiwgInN0ZXBfY29kZSIsICJsaW5lX251bWJlciIsICJjcmVhdGVkX2F0IikKICAgIGxpc3RfZmlsdGVyID0gKCJsZXZlbCIsICJzdGVwX2NvZGUiKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgiZmlsZV91cGxvYWRfX29yaWdpbmFsX2ZpbGVuYW1lIiwgIm1lc3NhZ2UiKQoKCkBhZG1pbi5yZWdpc3RlcihGaW5hbmNpYWxTdGF0ZW1lbnRJbXBvcnRIZWFkZXIpCmNsYXNzIEZpbmFuY2lhbFN0YXRlbWVudEltcG9ydEhlYWRlckFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKCJmaWxlX3VwbG9hZCIsICJ1bmUiLCAieWVhciIsICJtb250aCIsICJzdGF0ZW1lbnRfdHlwZSIpCiAgICBsaXN0X2ZpbHRlciA9ICgidW5lIiwgInllYXIiLCAibW9udGgiLCAic3RhdGVtZW50X3R5cGUiKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgiZmlsZV91cGxvYWRfX29yaWdpbmFsX2ZpbGVuYW1lIiwpCgoKQGFkbWluLnJlZ2lzdGVyKE5ld0NsaWVudEltcG9ydEhlYWRlcikKY2xhc3MgTmV3Q2xpZW50SW1wb3J0SGVhZGVyQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoImZpbGVfdXBsb2FkIiwgInllYXIiLCAibW9udGgiKQogICAgbGlzdF9maWx0ZXIgPSAoInllYXIiLCAibW9udGgiKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgiZmlsZV91cGxvYWRfX29yaWdpbmFsX2ZpbGVuYW1lIiwpCgoKQGFkbWluLnJlZ2lzdGVyKENyb3NzU2FsZUltcG9ydEhlYWRlcikKY2xhc3MgQ3Jvc3NTYWxlSW1wb3J0SGVhZGVyQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoImZpbGVfdXBsb2FkIiwgInllYXIiLCAibW9udGgiKQogICAgbGlzdF9maWx0ZXIgPSAoInllYXIiLCAibW9udGgiKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgiZmlsZV91cGxvYWRfX29yaWdpbmFsX2ZpbGVuYW1lIiwpCgoKQGFkbWluLnJlZ2lzdGVyKFN0YXRpb25UaW1lSW1wb3J0SGVhZGVyKQpjbGFzcyBTdGF0aW9uVGltZUltcG9ydEhlYWRlckFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKCJmaWxlX3VwbG9hZCIsICJ5ZWFyIiwgIm1vbnRoIikKICAgIGxpc3RfZmlsdGVyID0gKCJ5ZWFyIiwgIm1vbnRoIikKICAgIHNlYXJjaF9maWVsZHMgPSAoImZpbGVfdXBsb2FkX19vcmlnaW5hbF9maWxlbmFtZSIsKQoKCkBhZG1pbi5yZWdpc3RlcihOZXdDbGllbnRJbXBvcnRSb3cpCmNsYXNzIE5ld0NsaWVudEltcG9ydFJvd0FkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKAogICAgICAgICJ5ZWFyIiwKICAgICAgICAibW9udGgiLAogICAgICAgICJ1bmUiLAogICAgICAgICJjbGllbnRfbmFtZSIsCiAgICAgICAgIm5pdCIsCiAgICAgICAgIm9wZXJhdGlvbl9jb2RlIiwKICAgICAgICAicHJldmlvdXNfY29udHJhY3RzIiwKICAgICAgICAiY291bnRzX2FzX25ldyIsCiAgICAgICAgImN1cnJlbmN5IiwKICAgICAgICAiYW1vdW50IiwKICAgICkKICAgIGxpc3RfZmlsdGVyID0gKAogICAgICAgICJ5ZWFyIiwKICAgICAgICAibW9udGgiLAogICAgICAgICJ1bmUiLAogICAgICAgICJjb3VudHNfYXNfbmV3IiwKICAgICAgICAiY3VycmVuY3kiLAogICAgKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgKICAgICAgICAiY2xpZW50X25hbWUiLAogICAgICAgICJuaXQiLAogICAgICAgICJvcGVyYXRpb25fY29kZSIsCiAgICAgICAgInVuZV9fY29kZSIsCiAgICAgICAgInVuZV9fbmFtZV9lcyIsCiAgICAgICAgInJhd191bmVfdmFsdWUiLAogICAgKQogICAgYXV0b2NvbXBsZXRlX2ZpZWxkcyA9ICgidW5lIiwgImN1cnJlbmN5IikKICAgIGxpc3Rfc2VsZWN0X3JlbGF0ZWQgPSAoImhlYWRlciIsICJ1bmUiLCAiY3VycmVuY3kiKQoKCkBhZG1pbi5yZWdpc3RlcihDcm9zc1NhbGVJbXBvcnRSb3cpCmNsYXNzIENyb3NzU2FsZUltcG9ydFJvd0FkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKAogICAgICAgICJ5ZWFyIiwKICAgICAgICAibW9udGgiLAogICAgICAgICJ1bmVfb3JpZ2luIiwKICAgICAgICAidW5lX2Rlc3RpbmF0aW9uIiwKICAgICAgICAiY2xpZW50X25hbWUiLAogICAgICAgICJvcGVyYXRpb25fY29kZSIsCiAgICAgICAgImRhdGUiLAogICAgICAgICJjdXJyZW5jeSIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgKICAgICAgICAieWVhciIsCiAgICAgICAgIm1vbnRoIiwKICAgICAgICAidW5lX29yaWdpbiIsCiAgICAgICAgInVuZV9kZXN0aW5hdGlvbiIsCiAgICAgICAgImN1cnJlbmN5IiwKICAgICkKICAgIHNlYXJjaF9maWVsZHMgPSAoCiAgICAgICAgImNsaWVudF9uYW1lIiwKICAgICAgICAib3BlcmF0aW9uX2NvZGUiLAogICAgICAgICJyYXdfdW5lX29yaWdpbiIsCiAgICAgICAgInJhd191bmVfZGVzdGluYXRpb24iLAogICAgICAgICJ1bmVfb3JpZ2luX19jb2RlIiwKICAgICAgICAidW5lX2Rlc3RpbmF0aW9uX19jb2RlIiwKICAgICkKICAgIGF1dG9jb21wbGV0ZV9maWVsZHMgPSAoInVuZV9vcmlnaW4iLCAidW5lX2Rlc3RpbmF0aW9uIiwgImN1cnJlbmN5IikKICAgIGxpc3Rfc2VsZWN0X3JlbGF0ZWQgPSAoImhlYWRlciIsICJ1bmVfb3JpZ2luIiwgInVuZV9kZXN0aW5hdGlvbiIsICJjdXJyZW5jeSIp
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/apps.py
PATH_JSON="imports/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=6
SIZE_BYTES_UTF8=146
CONTENT_SHA256=e3bd24435a87330db778a6ed0c50ee0981d99aaf5f0436863c544264773e0ee4
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.apps import AppConfig


class ImportsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "imports"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class ImportsConfig(AppConfig):
00005|    default_auto_field = "django.db.models.BigAutoField"
00006|    name = "imports"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgSW1wb3J0c0NvbmZpZyhBcHBDb25maWcpOgogICAgZGVmYXVsdF9hdXRvX2ZpZWxkID0gImRqYW5nby5kYi5tb2RlbHMuQmlnQXV0b0ZpZWxkIgogICAgbmFtZSA9ICJpbXBvcnRzIgo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/detection.py
PATH_JSON="imports/detection.py"
FILENAME=detection.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=443
SIZE_BYTES_UTF8=16299
CONTENT_SHA256=085afb1f1231923f464022096a998f86afc3d5953e8837501436b543aa4604f7
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Autodetección de tipo de archivo para Importación General.

Capas (en orden de evaluación, luego fusión):
1. Nombre del archivo
2. Estructura (columnas / encabezados / hojas)
3. Contenido de muestra (valores que desambiguan tipos parecidos)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from core.services.column_map import _norm_header, normalize_columns
from core.services.import_base import ImportValidationError, read_dataframe

CONFIDENCE_AUTO = 0.80


@dataclass
class DetectionResult:
    tipo: str
    confidence: float
    label: str
    reasons: list[str] = field(default_factory=list)
    suggestions: list[tuple[str, str]] = field(default_factory=list)
    layer: str = ""
    ambiguous: bool = False
    candidates: list[tuple[str, float, str]] = field(default_factory=list)

    @property
    def can_auto_import(self) -> bool:
        return (
            self.tipo != TYPE_UNKNOWN
            and not self.ambiguous
            and self.confidence >= CONFIDENCE_AUTO
        )

    @property
    def rule_summary(self) -> str:
        """Texto corto para bitácora."""
        parts = [
            f"tipo={self.tipo}",
            f"capa={self.layer or 'n/a'}",
            f"confianza={self.confidence:.0%}",
            f"auto={'sí' if self.can_auto_import else 'no'}",
        ]
        if self.reasons:
            parts.append("reglas=[" + "; ".join(self.reasons[:6]) + "]")
        if self.ambiguous:
            parts.append("ambiguo=sí")
        return " | ".join(parts)


# Tipos canónicos del hub unificado
TYPE_CRM_CLIENTES = "crm_clientes"
TYPE_PGO_TICKETS = "pgo_tickets"
TYPE_PGO_CATALOGO = "pgo_catalogo"
TYPE_RISK_LEASING = "risk_leasing"
TYPE_RISK_RENTAS = "risk_rentas"
TYPE_NEW_CLIENTS = "new_clients"
TYPE_CROSS_SALE = "cross_sale"
TYPE_FINANCIAL = "financial"
TYPE_UNKNOWN = "unknown"

TYPE_LABELS = {
    TYPE_CRM_CLIENTES: "CRM — Clientes / entidades",
    TYPE_PGO_TICKETS: "PGO — Tickets helpdesk",
    TYPE_PGO_CATALOGO: "PGO — Catálogo de archivos (informativo)",
    TYPE_RISK_LEASING: "Balón de Riesgo — Base leasing / snapshots",
    TYPE_RISK_RENTAS: "Balón de Riesgo — Rentas / cuotas leasing",
    TYPE_NEW_CLIENTS: "PGC — Clientes nuevos",
    TYPE_CROSS_SALE: "PGC — Venta cruzada",
    TYPE_FINANCIAL: "PGC — Estado financiero (WC*)",
    TYPE_UNKNOWN: "Desconocido",
}

ALL_IMPORTABLE = [
    TYPE_CRM_CLIENTES,
    TYPE_PGO_TICKETS,
    TYPE_PGO_CATALOGO,
    TYPE_RISK_LEASING,
    TYPE_RISK_RENTAS,
    TYPE_NEW_CLIENTS,
    TYPE_CROSS_SALE,
]

IMPORTER_LABELS = {
    TYPE_CRM_CLIENTES: "crm.services.import_entidades",
    TYPE_PGO_TICKETS: "pgo.services.import_tickets",
    TYPE_PGO_CATALOGO: "pgo.services.import_archivos_catalogo",
    TYPE_RISK_LEASING: "risk.services.import_leasing_database",
    TYPE_RISK_RENTAS: "risk.services.import_leasing_rentas",
    TYPE_NEW_CLIENTS: "import_clientes_nuevos",
    TYPE_CROSS_SALE: "import_venta_cruzada",
    TYPE_FINANCIAL: "pgc.admin_monthly (manual)",
}


def _score_columns(cols: set[str], required_groups: list[list[str]]) -> int:
    score = 0
    for group in required_groups:
        if any(_norm_header(g) in cols for g in group):
            score += 1
    return score


def detect_from_name(filename: str) -> DetectionResult | None:
    name = (filename or "").lower()
    compact = re.sub(r"[\s_\-.]+", "", name)

    checks = [
        (TYPE_NEW_CLIENTS, "clientesnuevos" in compact or "clientes_nuevos" in name, "nombre: ClientesNuevos"),
        (TYPE_CROSS_SALE, "ventacruzada" in compact, "nombre: VentaCruzada"),
        (TYPE_FINANCIAL, name.startswith("wc") or "estado_resultados" in name or "er_" in name, "nombre: WC*/ER financiero"),
        (TYPE_PGO_TICKETS, "pgo" in name and ("ticket" in name or "control" in name), "nombre: PGO+tickets/control"),
        (TYPE_PGO_CATALOGO, "pgo" in name and "archivo" in name, "nombre: PGO+archivos"),
        (TYPE_CRM_CLIENTES, "crm" in name or "infoclientes" in compact, "nombre: CRM/InfoClientes"),
        (TYPE_RISK_RENTAS, "rentas" in name and "leasing" in name, "nombre: LeasingRentas"),
        (
            TYPE_RISK_LEASING,
            "baseleasing" in compact
            or ("balon" in name and "leasing" in name)
            or ("leasing" in name and "base" in name),
            "nombre: BaseLeasing/balón",
        ),
    ]
    for tipo, matched, reason in checks:
        if matched:
            return DetectionResult(
                tipo=tipo,
                confidence=0.85,
                label=TYPE_LABELS[tipo],
                reasons=[reason],
                layer="nombre",
            )
    return None


def detect_from_columns(cols: set[str]) -> DetectionResult | None:
    candidates: list[tuple[str, int, list[str]]] = []

    crm_score = _score_columns(
        cols,
        [["nit"], ["nombre", "nombre_cliente", "cliente", "razon_social"], ["wcf", "wcl", "wci"]],
    )
    if crm_score >= 2:
        candidates.append((TYPE_CRM_CLIENTES, crm_score, ["estructura: NIT/Nombre/WCF|WCL|WCI"]))

    pgo_score = _score_columns(
        cols,
        [["id", "codigo", "ticket"], ["titulo", "asunto"], ["estado"], ["fecha_apertura", "usuario_solicita"]],
    )
    if pgo_score >= 3:
        candidates.append((TYPE_PGO_TICKETS, pgo_score, ["estructura: ID/Titulo/Estado helpdesk"]))

    catalog_score = _score_columns(cols, [["carpeta", "archivo"], ["creado_por", "creado_en"]])
    if catalog_score >= 2:
        candidates.append((TYPE_PGO_CATALOGO, catalog_score, ["estructura: Carpeta/Archivo"]))

    leasing_score = _score_columns(
        cols,
        [
            ["contract_number", "contrato", "no_contrato"],
            ["client_name", "cliente", "nombre_cliente"],
            ["capital_balance", "saldo", "duedays", "due_days"],
        ],
    )
    if leasing_score >= 2:
        candidates.append((TYPE_RISK_LEASING, leasing_score, ["estructura: Contract/Client/Balance"]))

    rentas_score = _score_columns(
        cols,
        [["no_contrato", "contrato"], ["vencimiento"], ["valor_renta", "renta_total"], ["estado"]],
    )
    if rentas_score >= 3:
        candidates.append((TYPE_RISK_RENTAS, rentas_score, ["estructura: NoContrato/Vencimiento/ValorRenta"]))

    nc_score = _score_columns(cols, [["une"], ["cliente", "nombre"], ["fecha", "mes"], ["monto", "amount", "ingreso"]])
    if "une" in cols and nc_score >= 2:
        candidates.append((TYPE_NEW_CLIENTS, nc_score, ["estructura: UNE + cliente/periodo"]))

    xc_score = _score_columns(
        cols,
        [
            ["une", "unidad"],
            ["producto_origen", "origen", "producto"],
            ["producto_destino", "destino", "cruzado"],
            ["cliente", "nombre"],
        ],
    )
    if xc_score >= 3:
        candidates.append((TYPE_CROSS_SALE, xc_score, ["estructura: venta cruzada origen/destino"]))

    if not candidates:
        return None
    candidates.sort(key=lambda x: x[1], reverse=True)
    tipo, score, reasons = candidates[0]
    conf = min(0.95, 0.55 + 0.1 * score)
    suggestions = [(t, TYPE_LABELS[t]) for t, _, _ in candidates[1:3]]
    ambiguous = len(candidates) > 1 and candidates[0][1] == candidates[1][1]
    return DetectionResult(
        tipo=tipo,
        confidence=conf * (0.75 if ambiguous else 1.0),
        label=TYPE_LABELS[tipo],
        reasons=reasons,
        suggestions=suggestions,
        layer="estructura",
        ambiguous=ambiguous,
        candidates=[(t, float(s), "; ".join(r)) for t, s, r in candidates],
    )


def detect_from_content(df) -> DetectionResult | None:
    """Capa 3: patrones en valores de muestra (primeras filas)."""
    if df is None or df.empty:
        return None

    sample = df.head(40)
    cols = set(sample.columns)
    scores: dict[str, float] = {}
    reasons: dict[str, list[str]] = {}

    def bump(tipo: str, pts: float, reason: str) -> None:
        scores[tipo] = scores.get(tipo, 0.0) + pts
        reasons.setdefault(tipo, []).append(reason)

    # NIT / documento típico CRM
    for col in ("nit", "documento", "ruc", "identificacion"):
        if col in cols:
            series = sample[col].astype(str).str.replace(r"\s+", "", regex=True)
            nit_hits = series.str.match(r"^\d{6,14}(-\d)?$").sum()
            if nit_hits >= 3:
                bump(TYPE_CRM_CLIENTES, 1.5, f"contenido: {nit_hits} NITs en '{col}'")

    # Flags UNE en columnas WCF/WCL/WCI
    une_flag_cols = [c for c in ("wcf", "wcl", "wci") if c in cols]
    if une_flag_cols:
        bump(TYPE_CRM_CLIENTES, 1.0, f"contenido: columnas producto {', '.join(une_flag_cols)}")

    # Tickets PGO: estados / prioridades frecuentes
    if "estado" in cols:
        estados = " ".join(sample["estado"].astype(str).str.lower().unique()[:20])
        if any(k in estados for k in ("abierto", "cerrado", "pendiente", "en proceso", "resuelto")):
            bump(TYPE_PGO_TICKETS, 1.2, "contenido: estados tipo helpdesk")
        if any(k in estados for k in ("vigente", "vencid", "pagad", "mora")):
            bump(TYPE_RISK_RENTAS, 1.0, "contenido: estados tipo renta/cuota")

    if any(c in cols for c in ("titulo", "asunto")) and any(c in cols for c in ("id", "codigo", "ticket")):
        bump(TYPE_PGO_TICKETS, 0.8, "contenido: id+titulo ticket")

    # Leasing: días de mora / saldo
    for col in ("duedays", "due_days", "dias_mora", "diasmora"):
        if col in cols:
            numeric = sample[col].apply(lambda v: _is_number(v))
            if numeric.sum() >= 3:
                bump(TYPE_RISK_LEASING, 1.3, f"contenido: días mora en '{col}'")

    for col in ("capital_balance", "saldo", "saldo_capital", "outstanding"):
        if col in cols and sample[col].apply(_is_number).sum() >= 3:
            bump(TYPE_RISK_LEASING, 0.9, f"contenido: saldos en '{col}'")

    for col in ("valor_renta", "renta_total", "monto_renta"):
        if col in cols and sample[col].apply(_is_number).sum() >= 3:
            bump(TYPE_RISK_RENTAS, 1.2, f"contenido: montos renta en '{col}'")

    # Clientes nuevos: códigos UNE
    if "une" in cols:
        unes = " ".join(sample["une"].astype(str).str.upper().unique()[:30])
        if any(k in unes for k in ("WCF", "WCL", "WCI", "INVEST", "FACTOR")):
            bump(TYPE_NEW_CLIENTS, 1.4, "contenido: códigos UNE comerciales")

    # Venta cruzada: mención origen/destino en valores o columnas
    if any(c in cols for c in ("producto_origen", "producto_destino", "origen", "destino")):
        bump(TYPE_CROSS_SALE, 1.2, "contenido: columnas origen/destino producto")

    if not scores:
        return None

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_tipo, best_score = ranked[0]
    conf = min(0.92, 0.45 + 0.12 * best_score)
    ambiguous = len(ranked) > 1 and (ranked[0][1] - ranked[1][1]) < 0.6
    suggestions = [(t, TYPE_LABELS[t]) for t, _ in ranked[1:3] if t in TYPE_LABELS]
    return DetectionResult(
        tipo=best_tipo,
        confidence=conf * (0.7 if ambiguous else 1.0),
        label=TYPE_LABELS.get(best_tipo, best_tipo),
        reasons=reasons.get(best_tipo, [])[:4],
        suggestions=suggestions,
        layer="contenido",
        ambiguous=ambiguous,
        candidates=[(t, s, "; ".join(reasons.get(t, [])[:2])) for t, s in ranked],
    )


def _is_number(value) -> bool:
    try:
        if value is None:
            return False
        s = str(value).strip().replace(",", "")
        if not s or s.lower() in ("nan", "none", "-"):
            return False
        float(s)
        return True
    except (TypeError, ValueError):
        return False


def _merge_detections(
    by_name: DetectionResult | None,
    by_cols: DetectionResult | None,
    by_content: DetectionResult | None,
) -> DetectionResult:
    """Fusiona las tres capas con prioridad nombre → estructura → contenido."""
    votes: dict[str, float] = {}
    all_reasons: list[str] = []
    layers_used: list[str] = []

    def add_vote(det: DetectionResult | None, weight: float) -> None:
        if not det or det.tipo == TYPE_UNKNOWN:
            return
        votes[det.tipo] = votes.get(det.tipo, 0.0) + det.confidence * weight
        all_reasons.extend(det.reasons)
        if det.layer:
            layers_used.append(det.layer)

    # Pesos: nombre fuerte si coincide; estructura y contenido refuerzan
    add_vote(by_name, 1.0)
    add_vote(by_cols, 1.15)
    add_vote(by_content, 1.05)

    if not votes:
        return DetectionResult(
            tipo=TYPE_UNKNOWN,
            confidence=0.0,
            label=TYPE_LABELS[TYPE_UNKNOWN],
            reasons=["No se pudo identificar el tipo con ninguna capa"],
            suggestions=[(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE],
            layer="ninguna",
            ambiguous=True,
        )

    ranked = sorted(votes.items(), key=lambda x: x[1], reverse=True)
    best_tipo, best_vote = ranked[0]
    second_vote = ranked[1][1] if len(ranked) > 1 else 0.0

    # Acuerdo nombre + estructura → alta confianza
    name_tipo = by_name.tipo if by_name else None
    cols_tipo = by_cols.tipo if by_cols else None
    content_tipo = by_content.tipo if by_content else None

    agreement = sum(
        1
        for t in (name_tipo, cols_tipo, content_tipo)
        if t and t == best_tipo
    )

    confidence = min(0.99, best_vote / max(1.0, agreement + 0.5))
    if agreement >= 2:
        confidence = max(confidence, 0.88)
    if agreement >= 3:
        confidence = max(confidence, 0.95)

    conflict = False
    if name_tipo and cols_tipo and name_tipo != cols_tipo:
        conflict = True
        all_reasons.append(f"conflicto nombre({name_tipo}) vs estructura({cols_tipo})")
        confidence = min(confidence, 0.72)

    if content_tipo and cols_tipo and content_tipo != cols_tipo and agreement < 2:
        conflict = True
        all_reasons.append(f"contenido({content_tipo}) difiere de estructura({cols_tipo})")

    margin_tight = (best_vote - second_vote) < 0.25 and len(ranked) > 1
    ambiguous = conflict or margin_tight or confidence < CONFIDENCE_AUTO

    suggestions: list[tuple[str, str]] = []
    for t, _ in ranked[1:4]:
        if t in TYPE_LABELS:
            suggestions.append((t, TYPE_LABELS[t]))
    # Incluir capas discrepantes
    for t in (name_tipo, cols_tipo, content_tipo):
        if t and t != best_tipo and t in TYPE_LABELS:
            pair = (t, TYPE_LABELS[t])
            if pair not in suggestions:
                suggestions.append(pair)

    layer = "+".join(dict.fromkeys(layers_used)) or "combinada"
    if agreement >= 2:
        layer = f"combinada({agreement} capas)"

    return DetectionResult(
        tipo=best_tipo,
        confidence=confidence,
        label=TYPE_LABELS.get(best_tipo, best_tipo),
        reasons=list(dict.fromkeys(all_reasons))[:8],
        suggestions=suggestions[:4],
        layer=layer,
        ambiguous=ambiguous,
        candidates=[(t, v, "") for t, v in ranked],
    )


def detect_file(uploaded_file) -> DetectionResult:
    by_name = detect_from_name(getattr(uploaded_file, "name", "") or "")
    df = None
    by_cols = None
    by_content = None

    try:
        df = normalize_columns(read_dataframe(uploaded_file, sheet_name=None))
        uploaded_file.seek(0)
        cols = set(df.columns)
        by_cols = detect_from_columns(cols)
        by_content = detect_from_content(df)
    except Exception as exc:
        uploaded_file.seek(0)
        if by_name and by_name.confidence >= 0.8:
            by_name.reasons.append(f"columnas no leídas ({exc})")
            by_name.ambiguous = False
            return by_name
        return DetectionResult(
            tipo=TYPE_UNKNOWN,
            confidence=0.0,
            label=TYPE_LABELS[TYPE_UNKNOWN],
            reasons=[f"No se pudo leer el archivo: {exc}"],
            suggestions=[(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE[:5]],
            layer="error",
            ambiguous=True,
        )

    return _merge_detections(by_name, by_cols, by_content)


def detect_path(path: str) -> DetectionResult:
    from pathlib import Path

    from django.core.files.uploadedfile import SimpleUploadedFile

    p = Path(path)
    f = SimpleUploadedFile(p.name, p.read_bytes())
    return detect_file(f)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Autodetección de tipo de archivo para Importación General.
00002|
00003|Capas (en orden de evaluación, luego fusión):
00004|1. Nombre del archivo
00005|2. Estructura (columnas / encabezados / hojas)
00006|3. Contenido de muestra (valores que desambiguan tipos parecidos)
00007|"""
00008|
00009|from __future__ import annotations
00010|
00011|import re
00012|from dataclasses import dataclass, field
00013|
00014|from core.services.column_map import _norm_header, normalize_columns
00015|from core.services.import_base import ImportValidationError, read_dataframe
00016|
00017|CONFIDENCE_AUTO = 0.80
00018|
00019|
00020|@dataclass
00021|class DetectionResult:
00022|    tipo: str
00023|    confidence: float
00024|    label: str
00025|    reasons: list[str] = field(default_factory=list)
00026|    suggestions: list[tuple[str, str]] = field(default_factory=list)
00027|    layer: str = ""
00028|    ambiguous: bool = False
00029|    candidates: list[tuple[str, float, str]] = field(default_factory=list)
00030|
00031|    @property
00032|    def can_auto_import(self) -> bool:
00033|        return (
00034|            self.tipo != TYPE_UNKNOWN
00035|            and not self.ambiguous
00036|            and self.confidence >= CONFIDENCE_AUTO
00037|        )
00038|
00039|    @property
00040|    def rule_summary(self) -> str:
00041|        """Texto corto para bitácora."""
00042|        parts = [
00043|            f"tipo={self.tipo}",
00044|            f"capa={self.layer or 'n/a'}",
00045|            f"confianza={self.confidence:.0%}",
00046|            f"auto={'sí' if self.can_auto_import else 'no'}",
00047|        ]
00048|        if self.reasons:
00049|            parts.append("reglas=[" + "; ".join(self.reasons[:6]) + "]")
00050|        if self.ambiguous:
00051|            parts.append("ambiguo=sí")
00052|        return " | ".join(parts)
00053|
00054|
00055|# Tipos canónicos del hub unificado
00056|TYPE_CRM_CLIENTES = "crm_clientes"
00057|TYPE_PGO_TICKETS = "pgo_tickets"
00058|TYPE_PGO_CATALOGO = "pgo_catalogo"
00059|TYPE_RISK_LEASING = "risk_leasing"
00060|TYPE_RISK_RENTAS = "risk_rentas"
00061|TYPE_NEW_CLIENTS = "new_clients"
00062|TYPE_CROSS_SALE = "cross_sale"
00063|TYPE_FINANCIAL = "financial"
00064|TYPE_UNKNOWN = "unknown"
00065|
00066|TYPE_LABELS = {
00067|    TYPE_CRM_CLIENTES: "CRM — Clientes / entidades",
00068|    TYPE_PGO_TICKETS: "PGO — Tickets helpdesk",
00069|    TYPE_PGO_CATALOGO: "PGO — Catálogo de archivos (informativo)",
00070|    TYPE_RISK_LEASING: "Balón de Riesgo — Base leasing / snapshots",
00071|    TYPE_RISK_RENTAS: "Balón de Riesgo — Rentas / cuotas leasing",
00072|    TYPE_NEW_CLIENTS: "PGC — Clientes nuevos",
00073|    TYPE_CROSS_SALE: "PGC — Venta cruzada",
00074|    TYPE_FINANCIAL: "PGC — Estado financiero (WC*)",
00075|    TYPE_UNKNOWN: "Desconocido",
00076|}
00077|
00078|ALL_IMPORTABLE = [
00079|    TYPE_CRM_CLIENTES,
00080|    TYPE_PGO_TICKETS,
00081|    TYPE_PGO_CATALOGO,
00082|    TYPE_RISK_LEASING,
00083|    TYPE_RISK_RENTAS,
00084|    TYPE_NEW_CLIENTS,
00085|    TYPE_CROSS_SALE,
00086|]
00087|
00088|IMPORTER_LABELS = {
00089|    TYPE_CRM_CLIENTES: "crm.services.import_entidades",
00090|    TYPE_PGO_TICKETS: "pgo.services.import_tickets",
00091|    TYPE_PGO_CATALOGO: "pgo.services.import_archivos_catalogo",
00092|    TYPE_RISK_LEASING: "risk.services.import_leasing_database",
00093|    TYPE_RISK_RENTAS: "risk.services.import_leasing_rentas",
00094|    TYPE_NEW_CLIENTS: "import_clientes_nuevos",
00095|    TYPE_CROSS_SALE: "import_venta_cruzada",
00096|    TYPE_FINANCIAL: "pgc.admin_monthly (manual)",
00097|}
00098|
00099|
00100|def _score_columns(cols: set[str], required_groups: list[list[str]]) -> int:
00101|    score = 0
00102|    for group in required_groups:
00103|        if any(_norm_header(g) in cols for g in group):
00104|            score += 1
00105|    return score
00106|
00107|
00108|def detect_from_name(filename: str) -> DetectionResult | None:
00109|    name = (filename or "").lower()
00110|    compact = re.sub(r"[\s_\-.]+", "", name)
00111|
00112|    checks = [
00113|        (TYPE_NEW_CLIENTS, "clientesnuevos" in compact or "clientes_nuevos" in name, "nombre: ClientesNuevos"),
00114|        (TYPE_CROSS_SALE, "ventacruzada" in compact, "nombre: VentaCruzada"),
00115|        (TYPE_FINANCIAL, name.startswith("wc") or "estado_resultados" in name or "er_" in name, "nombre: WC*/ER financiero"),
00116|        (TYPE_PGO_TICKETS, "pgo" in name and ("ticket" in name or "control" in name), "nombre: PGO+tickets/control"),
00117|        (TYPE_PGO_CATALOGO, "pgo" in name and "archivo" in name, "nombre: PGO+archivos"),
00118|        (TYPE_CRM_CLIENTES, "crm" in name or "infoclientes" in compact, "nombre: CRM/InfoClientes"),
00119|        (TYPE_RISK_RENTAS, "rentas" in name and "leasing" in name, "nombre: LeasingRentas"),
00120|        (
00121|            TYPE_RISK_LEASING,
00122|            "baseleasing" in compact
00123|            or ("balon" in name and "leasing" in name)
00124|            or ("leasing" in name and "base" in name),
00125|            "nombre: BaseLeasing/balón",
00126|        ),
00127|    ]
00128|    for tipo, matched, reason in checks:
00129|        if matched:
00130|            return DetectionResult(
00131|                tipo=tipo,
00132|                confidence=0.85,
00133|                label=TYPE_LABELS[tipo],
00134|                reasons=[reason],
00135|                layer="nombre",
00136|            )
00137|    return None
00138|
00139|
00140|def detect_from_columns(cols: set[str]) -> DetectionResult | None:
00141|    candidates: list[tuple[str, int, list[str]]] = []
00142|
00143|    crm_score = _score_columns(
00144|        cols,
00145|        [["nit"], ["nombre", "nombre_cliente", "cliente", "razon_social"], ["wcf", "wcl", "wci"]],
00146|    )
00147|    if crm_score >= 2:
00148|        candidates.append((TYPE_CRM_CLIENTES, crm_score, ["estructura: NIT/Nombre/WCF|WCL|WCI"]))
00149|
00150|    pgo_score = _score_columns(
00151|        cols,
00152|        [["id", "codigo", "ticket"], ["titulo", "asunto"], ["estado"], ["fecha_apertura", "usuario_solicita"]],
00153|    )
00154|    if pgo_score >= 3:
00155|        candidates.append((TYPE_PGO_TICKETS, pgo_score, ["estructura: ID/Titulo/Estado helpdesk"]))
00156|
00157|    catalog_score = _score_columns(cols, [["carpeta", "archivo"], ["creado_por", "creado_en"]])
00158|    if catalog_score >= 2:
00159|        candidates.append((TYPE_PGO_CATALOGO, catalog_score, ["estructura: Carpeta/Archivo"]))
00160|
00161|    leasing_score = _score_columns(
00162|        cols,
00163|        [
00164|            ["contract_number", "contrato", "no_contrato"],
00165|            ["client_name", "cliente", "nombre_cliente"],
00166|            ["capital_balance", "saldo", "duedays", "due_days"],
00167|        ],
00168|    )
00169|    if leasing_score >= 2:
00170|        candidates.append((TYPE_RISK_LEASING, leasing_score, ["estructura: Contract/Client/Balance"]))
00171|
00172|    rentas_score = _score_columns(
00173|        cols,
00174|        [["no_contrato", "contrato"], ["vencimiento"], ["valor_renta", "renta_total"], ["estado"]],
00175|    )
00176|    if rentas_score >= 3:
00177|        candidates.append((TYPE_RISK_RENTAS, rentas_score, ["estructura: NoContrato/Vencimiento/ValorRenta"]))
00178|
00179|    nc_score = _score_columns(cols, [["une"], ["cliente", "nombre"], ["fecha", "mes"], ["monto", "amount", "ingreso"]])
00180|    if "une" in cols and nc_score >= 2:
00181|        candidates.append((TYPE_NEW_CLIENTS, nc_score, ["estructura: UNE + cliente/periodo"]))
00182|
00183|    xc_score = _score_columns(
00184|        cols,
00185|        [
00186|            ["une", "unidad"],
00187|            ["producto_origen", "origen", "producto"],
00188|            ["producto_destino", "destino", "cruzado"],
00189|            ["cliente", "nombre"],
00190|        ],
00191|    )
00192|    if xc_score >= 3:
00193|        candidates.append((TYPE_CROSS_SALE, xc_score, ["estructura: venta cruzada origen/destino"]))
00194|
00195|    if not candidates:
00196|        return None
00197|    candidates.sort(key=lambda x: x[1], reverse=True)
00198|    tipo, score, reasons = candidates[0]
00199|    conf = min(0.95, 0.55 + 0.1 * score)
00200|    suggestions = [(t, TYPE_LABELS[t]) for t, _, _ in candidates[1:3]]
00201|    ambiguous = len(candidates) > 1 and candidates[0][1] == candidates[1][1]
00202|    return DetectionResult(
00203|        tipo=tipo,
00204|        confidence=conf * (0.75 if ambiguous else 1.0),
00205|        label=TYPE_LABELS[tipo],
00206|        reasons=reasons,
00207|        suggestions=suggestions,
00208|        layer="estructura",
00209|        ambiguous=ambiguous,
00210|        candidates=[(t, float(s), "; ".join(r)) for t, s, r in candidates],
00211|    )
00212|
00213|
00214|def detect_from_content(df) -> DetectionResult | None:
00215|    """Capa 3: patrones en valores de muestra (primeras filas)."""
00216|    if df is None or df.empty:
00217|        return None
00218|
00219|    sample = df.head(40)
00220|    cols = set(sample.columns)
00221|    scores: dict[str, float] = {}
00222|    reasons: dict[str, list[str]] = {}
00223|
00224|    def bump(tipo: str, pts: float, reason: str) -> None:
00225|        scores[tipo] = scores.get(tipo, 0.0) + pts
00226|        reasons.setdefault(tipo, []).append(reason)
00227|
00228|    # NIT / documento típico CRM
00229|    for col in ("nit", "documento", "ruc", "identificacion"):
00230|        if col in cols:
00231|            series = sample[col].astype(str).str.replace(r"\s+", "", regex=True)
00232|            nit_hits = series.str.match(r"^\d{6,14}(-\d)?$").sum()
00233|            if nit_hits >= 3:
00234|                bump(TYPE_CRM_CLIENTES, 1.5, f"contenido: {nit_hits} NITs en '{col}'")
00235|
00236|    # Flags UNE en columnas WCF/WCL/WCI
00237|    une_flag_cols = [c for c in ("wcf", "wcl", "wci") if c in cols]
00238|    if une_flag_cols:
00239|        bump(TYPE_CRM_CLIENTES, 1.0, f"contenido: columnas producto {', '.join(une_flag_cols)}")
00240|
00241|    # Tickets PGO: estados / prioridades frecuentes
00242|    if "estado" in cols:
00243|        estados = " ".join(sample["estado"].astype(str).str.lower().unique()[:20])
00244|        if any(k in estados for k in ("abierto", "cerrado", "pendiente", "en proceso", "resuelto")):
00245|            bump(TYPE_PGO_TICKETS, 1.2, "contenido: estados tipo helpdesk")
00246|        if any(k in estados for k in ("vigente", "vencid", "pagad", "mora")):
00247|            bump(TYPE_RISK_RENTAS, 1.0, "contenido: estados tipo renta/cuota")
00248|
00249|    if any(c in cols for c in ("titulo", "asunto")) and any(c in cols for c in ("id", "codigo", "ticket")):
00250|        bump(TYPE_PGO_TICKETS, 0.8, "contenido: id+titulo ticket")
00251|
00252|    # Leasing: días de mora / saldo
00253|    for col in ("duedays", "due_days", "dias_mora", "diasmora"):
00254|        if col in cols:
00255|            numeric = sample[col].apply(lambda v: _is_number(v))
00256|            if numeric.sum() >= 3:
00257|                bump(TYPE_RISK_LEASING, 1.3, f"contenido: días mora en '{col}'")
00258|
00259|    for col in ("capital_balance", "saldo", "saldo_capital", "outstanding"):
00260|        if col in cols and sample[col].apply(_is_number).sum() >= 3:
00261|            bump(TYPE_RISK_LEASING, 0.9, f"contenido: saldos en '{col}'")
00262|
00263|    for col in ("valor_renta", "renta_total", "monto_renta"):
00264|        if col in cols and sample[col].apply(_is_number).sum() >= 3:
00265|            bump(TYPE_RISK_RENTAS, 1.2, f"contenido: montos renta en '{col}'")
00266|
00267|    # Clientes nuevos: códigos UNE
00268|    if "une" in cols:
00269|        unes = " ".join(sample["une"].astype(str).str.upper().unique()[:30])
00270|        if any(k in unes for k in ("WCF", "WCL", "WCI", "INVEST", "FACTOR")):
00271|            bump(TYPE_NEW_CLIENTS, 1.4, "contenido: códigos UNE comerciales")
00272|
00273|    # Venta cruzada: mención origen/destino en valores o columnas
00274|    if any(c in cols for c in ("producto_origen", "producto_destino", "origen", "destino")):
00275|        bump(TYPE_CROSS_SALE, 1.2, "contenido: columnas origen/destino producto")
00276|
00277|    if not scores:
00278|        return None
00279|
00280|    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
00281|    best_tipo, best_score = ranked[0]
00282|    conf = min(0.92, 0.45 + 0.12 * best_score)
00283|    ambiguous = len(ranked) > 1 and (ranked[0][1] - ranked[1][1]) < 0.6
00284|    suggestions = [(t, TYPE_LABELS[t]) for t, _ in ranked[1:3] if t in TYPE_LABELS]
00285|    return DetectionResult(
00286|        tipo=best_tipo,
00287|        confidence=conf * (0.7 if ambiguous else 1.0),
00288|        label=TYPE_LABELS.get(best_tipo, best_tipo),
00289|        reasons=reasons.get(best_tipo, [])[:4],
00290|        suggestions=suggestions,
00291|        layer="contenido",
00292|        ambiguous=ambiguous,
00293|        candidates=[(t, s, "; ".join(reasons.get(t, [])[:2])) for t, s in ranked],
00294|    )
00295|
00296|
00297|def _is_number(value) -> bool:
00298|    try:
00299|        if value is None:
00300|            return False
00301|        s = str(value).strip().replace(",", "")
00302|        if not s or s.lower() in ("nan", "none", "-"):
00303|            return False
00304|        float(s)
00305|        return True
00306|    except (TypeError, ValueError):
00307|        return False
00308|
00309|
00310|def _merge_detections(
00311|    by_name: DetectionResult | None,
00312|    by_cols: DetectionResult | None,
00313|    by_content: DetectionResult | None,
00314|) -> DetectionResult:
00315|    """Fusiona las tres capas con prioridad nombre → estructura → contenido."""
00316|    votes: dict[str, float] = {}
00317|    all_reasons: list[str] = []
00318|    layers_used: list[str] = []
00319|
00320|    def add_vote(det: DetectionResult | None, weight: float) -> None:
00321|        if not det or det.tipo == TYPE_UNKNOWN:
00322|            return
00323|        votes[det.tipo] = votes.get(det.tipo, 0.0) + det.confidence * weight
00324|        all_reasons.extend(det.reasons)
00325|        if det.layer:
00326|            layers_used.append(det.layer)
00327|
00328|    # Pesos: nombre fuerte si coincide; estructura y contenido refuerzan
00329|    add_vote(by_name, 1.0)
00330|    add_vote(by_cols, 1.15)
00331|    add_vote(by_content, 1.05)
00332|
00333|    if not votes:
00334|        return DetectionResult(
00335|            tipo=TYPE_UNKNOWN,
00336|            confidence=0.0,
00337|            label=TYPE_LABELS[TYPE_UNKNOWN],
00338|            reasons=["No se pudo identificar el tipo con ninguna capa"],
00339|            suggestions=[(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE],
00340|            layer="ninguna",
00341|            ambiguous=True,
00342|        )
00343|
00344|    ranked = sorted(votes.items(), key=lambda x: x[1], reverse=True)
00345|    best_tipo, best_vote = ranked[0]
00346|    second_vote = ranked[1][1] if len(ranked) > 1 else 0.0
00347|
00348|    # Acuerdo nombre + estructura → alta confianza
00349|    name_tipo = by_name.tipo if by_name else None
00350|    cols_tipo = by_cols.tipo if by_cols else None
00351|    content_tipo = by_content.tipo if by_content else None
00352|
00353|    agreement = sum(
00354|        1
00355|        for t in (name_tipo, cols_tipo, content_tipo)
00356|        if t and t == best_tipo
00357|    )
00358|
00359|    confidence = min(0.99, best_vote / max(1.0, agreement + 0.5))
00360|    if agreement >= 2:
00361|        confidence = max(confidence, 0.88)
00362|    if agreement >= 3:
00363|        confidence = max(confidence, 0.95)
00364|
00365|    conflict = False
00366|    if name_tipo and cols_tipo and name_tipo != cols_tipo:
00367|        conflict = True
00368|        all_reasons.append(f"conflicto nombre({name_tipo}) vs estructura({cols_tipo})")
00369|        confidence = min(confidence, 0.72)
00370|
00371|    if content_tipo and cols_tipo and content_tipo != cols_tipo and agreement < 2:
00372|        conflict = True
00373|        all_reasons.append(f"contenido({content_tipo}) difiere de estructura({cols_tipo})")
00374|
00375|    margin_tight = (best_vote - second_vote) < 0.25 and len(ranked) > 1
00376|    ambiguous = conflict or margin_tight or confidence < CONFIDENCE_AUTO
00377|
00378|    suggestions: list[tuple[str, str]] = []
00379|    for t, _ in ranked[1:4]:
00380|        if t in TYPE_LABELS:
00381|            suggestions.append((t, TYPE_LABELS[t]))
00382|    # Incluir capas discrepantes
00383|    for t in (name_tipo, cols_tipo, content_tipo):
00384|        if t and t != best_tipo and t in TYPE_LABELS:
00385|            pair = (t, TYPE_LABELS[t])
00386|            if pair not in suggestions:
00387|                suggestions.append(pair)
00388|
00389|    layer = "+".join(dict.fromkeys(layers_used)) or "combinada"
00390|    if agreement >= 2:
00391|        layer = f"combinada({agreement} capas)"
00392|
00393|    return DetectionResult(
00394|        tipo=best_tipo,
00395|        confidence=confidence,
00396|        label=TYPE_LABELS.get(best_tipo, best_tipo),
00397|        reasons=list(dict.fromkeys(all_reasons))[:8],
00398|        suggestions=suggestions[:4],
00399|        layer=layer,
00400|        ambiguous=ambiguous,
00401|        candidates=[(t, v, "") for t, v in ranked],
00402|    )
00403|
00404|
00405|def detect_file(uploaded_file) -> DetectionResult:
00406|    by_name = detect_from_name(getattr(uploaded_file, "name", "") or "")
00407|    df = None
00408|    by_cols = None
00409|    by_content = None
00410|
00411|    try:
00412|        df = normalize_columns(read_dataframe(uploaded_file, sheet_name=None))
00413|        uploaded_file.seek(0)
00414|        cols = set(df.columns)
00415|        by_cols = detect_from_columns(cols)
00416|        by_content = detect_from_content(df)
00417|    except Exception as exc:
00418|        uploaded_file.seek(0)
00419|        if by_name and by_name.confidence >= 0.8:
00420|            by_name.reasons.append(f"columnas no leídas ({exc})")
00421|            by_name.ambiguous = False
00422|            return by_name
00423|        return DetectionResult(
00424|            tipo=TYPE_UNKNOWN,
00425|            confidence=0.0,
00426|            label=TYPE_LABELS[TYPE_UNKNOWN],
00427|            reasons=[f"No se pudo leer el archivo: {exc}"],
00428|            suggestions=[(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE[:5]],
00429|            layer="error",
00430|            ambiguous=True,
00431|        )
00432|
00433|    return _merge_detections(by_name, by_cols, by_content)
00434|
00435|
00436|def detect_path(path: str) -> DetectionResult:
00437|    from pathlib import Path
00438|
00439|    from django.core.files.uploadedfile import SimpleUploadedFile
00440|
00441|    p = Path(path)
00442|    f = SimpleUploadedFile(p.name, p.read_bytes())
00443|    return detect_file(f)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiQXV0b2RldGVjY2nDs24gZGUgdGlwbyBkZSBhcmNoaXZvIHBhcmEgSW1wb3J0YWNpw7NuIEdlbmVyYWwuCgpDYXBhcyAoZW4gb3JkZW4gZGUgZXZhbHVhY2nDs24sIGx1ZWdvIGZ1c2nDs24pOgoxLiBOb21icmUgZGVsIGFyY2hpdm8KMi4gRXN0cnVjdHVyYSAoY29sdW1uYXMgLyBlbmNhYmV6YWRvcyAvIGhvamFzKQozLiBDb250ZW5pZG8gZGUgbXVlc3RyYSAodmFsb3JlcyBxdWUgZGVzYW1iaWd1YW4gdGlwb3MgcGFyZWNpZG9zKQoiIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmltcG9ydCByZQpmcm9tIGRhdGFjbGFzc2VzIGltcG9ydCBkYXRhY2xhc3MsIGZpZWxkCgpmcm9tIGNvcmUuc2VydmljZXMuY29sdW1uX21hcCBpbXBvcnQgX25vcm1faGVhZGVyLCBub3JtYWxpemVfY29sdW1ucwpmcm9tIGNvcmUuc2VydmljZXMuaW1wb3J0X2Jhc2UgaW1wb3J0IEltcG9ydFZhbGlkYXRpb25FcnJvciwgcmVhZF9kYXRhZnJhbWUKCkNPTkZJREVOQ0VfQVVUTyA9IDAuODAKCgpAZGF0YWNsYXNzCmNsYXNzIERldGVjdGlvblJlc3VsdDoKICAgIHRpcG86IHN0cgogICAgY29uZmlkZW5jZTogZmxvYXQKICAgIGxhYmVsOiBzdHIKICAgIHJlYXNvbnM6IGxpc3Rbc3RyXSA9IGZpZWxkKGRlZmF1bHRfZmFjdG9yeT1saXN0KQogICAgc3VnZ2VzdGlvbnM6IGxpc3RbdHVwbGVbc3RyLCBzdHJdXSA9IGZpZWxkKGRlZmF1bHRfZmFjdG9yeT1saXN0KQogICAgbGF5ZXI6IHN0ciA9ICIiCiAgICBhbWJpZ3VvdXM6IGJvb2wgPSBGYWxzZQogICAgY2FuZGlkYXRlczogbGlzdFt0dXBsZVtzdHIsIGZsb2F0LCBzdHJdXSA9IGZpZWxkKGRlZmF1bHRfZmFjdG9yeT1saXN0KQoKICAgIEBwcm9wZXJ0eQogICAgZGVmIGNhbl9hdXRvX2ltcG9ydChzZWxmKSAtPiBib29sOgogICAgICAgIHJldHVybiAoCiAgICAgICAgICAgIHNlbGYudGlwbyAhPSBUWVBFX1VOS05PV04KICAgICAgICAgICAgYW5kIG5vdCBzZWxmLmFtYmlndW91cwogICAgICAgICAgICBhbmQgc2VsZi5jb25maWRlbmNlID49IENPTkZJREVOQ0VfQVVUTwogICAgICAgICkKCiAgICBAcHJvcGVydHkKICAgIGRlZiBydWxlX3N1bW1hcnkoc2VsZikgLT4gc3RyOgogICAgICAgICIiIlRleHRvIGNvcnRvIHBhcmEgYml0w6Fjb3JhLiIiIgogICAgICAgIHBhcnRzID0gWwogICAgICAgICAgICBmInRpcG89e3NlbGYudGlwb30iLAogICAgICAgICAgICBmImNhcGE9e3NlbGYubGF5ZXIgb3IgJ24vYSd9IiwKICAgICAgICAgICAgZiJjb25maWFuemE9e3NlbGYuY29uZmlkZW5jZTouMCV9IiwKICAgICAgICAgICAgZiJhdXRvPXsnc8OtJyBpZiBzZWxmLmNhbl9hdXRvX2ltcG9ydCBlbHNlICdubyd9IiwKICAgICAgICBdCiAgICAgICAgaWYgc2VsZi5yZWFzb25zOgogICAgICAgICAgICBwYXJ0cy5hcHBlbmQoInJlZ2xhcz1bIiArICI7ICIuam9pbihzZWxmLnJlYXNvbnNbOjZdKSArICJdIikKICAgICAgICBpZiBzZWxmLmFtYmlndW91czoKICAgICAgICAgICAgcGFydHMuYXBwZW5kKCJhbWJpZ3VvPXPDrSIpCiAgICAgICAgcmV0dXJuICIgfCAiLmpvaW4ocGFydHMpCgoKIyBUaXBvcyBjYW7Ds25pY29zIGRlbCBodWIgdW5pZmljYWRvClRZUEVfQ1JNX0NMSUVOVEVTID0gImNybV9jbGllbnRlcyIKVFlQRV9QR09fVElDS0VUUyA9ICJwZ29fdGlja2V0cyIKVFlQRV9QR09fQ0FUQUxPR08gPSAicGdvX2NhdGFsb2dvIgpUWVBFX1JJU0tfTEVBU0lORyA9ICJyaXNrX2xlYXNpbmciClRZUEVfUklTS19SRU5UQVMgPSAicmlza19yZW50YXMiClRZUEVfTkVXX0NMSUVOVFMgPSAibmV3X2NsaWVudHMiClRZUEVfQ1JPU1NfU0FMRSA9ICJjcm9zc19zYWxlIgpUWVBFX0ZJTkFOQ0lBTCA9ICJmaW5hbmNpYWwiClRZUEVfVU5LTk9XTiA9ICJ1bmtub3duIgoKVFlQRV9MQUJFTFMgPSB7CiAgICBUWVBFX0NSTV9DTElFTlRFUzogIkNSTSDigJQgQ2xpZW50ZXMgLyBlbnRpZGFkZXMiLAogICAgVFlQRV9QR09fVElDS0VUUzogIlBHTyDigJQgVGlja2V0cyBoZWxwZGVzayIsCiAgICBUWVBFX1BHT19DQVRBTE9HTzogIlBHTyDigJQgQ2F0w6Fsb2dvIGRlIGFyY2hpdm9zIChpbmZvcm1hdGl2bykiLAogICAgVFlQRV9SSVNLX0xFQVNJTkc6ICJCYWzDs24gZGUgUmllc2dvIOKAlCBCYXNlIGxlYXNpbmcgLyBzbmFwc2hvdHMiLAogICAgVFlQRV9SSVNLX1JFTlRBUzogIkJhbMOzbiBkZSBSaWVzZ28g4oCUIFJlbnRhcyAvIGN1b3RhcyBsZWFzaW5nIiwKICAgIFRZUEVfTkVXX0NMSUVOVFM6ICJQR0Mg4oCUIENsaWVudGVzIG51ZXZvcyIsCiAgICBUWVBFX0NST1NTX1NBTEU6ICJQR0Mg4oCUIFZlbnRhIGNydXphZGEiLAogICAgVFlQRV9GSU5BTkNJQUw6ICJQR0Mg4oCUIEVzdGFkbyBmaW5hbmNpZXJvIChXQyopIiwKICAgIFRZUEVfVU5LTk9XTjogIkRlc2Nvbm9jaWRvIiwKfQoKQUxMX0lNUE9SVEFCTEUgPSBbCiAgICBUWVBFX0NSTV9DTElFTlRFUywKICAgIFRZUEVfUEdPX1RJQ0tFVFMsCiAgICBUWVBFX1BHT19DQVRBTE9HTywKICAgIFRZUEVfUklTS19MRUFTSU5HLAogICAgVFlQRV9SSVNLX1JFTlRBUywKICAgIFRZUEVfTkVXX0NMSUVOVFMsCiAgICBUWVBFX0NST1NTX1NBTEUsCl0KCklNUE9SVEVSX0xBQkVMUyA9IHsKICAgIFRZUEVfQ1JNX0NMSUVOVEVTOiAiY3JtLnNlcnZpY2VzLmltcG9ydF9lbnRpZGFkZXMiLAogICAgVFlQRV9QR09fVElDS0VUUzogInBnby5zZXJ2aWNlcy5pbXBvcnRfdGlja2V0cyIsCiAgICBUWVBFX1BHT19DQVRBTE9HTzogInBnby5zZXJ2aWNlcy5pbXBvcnRfYXJjaGl2b3NfY2F0YWxvZ28iLAogICAgVFlQRV9SSVNLX0xFQVNJTkc6ICJyaXNrLnNlcnZpY2VzLmltcG9ydF9sZWFzaW5nX2RhdGFiYXNlIiwKICAgIFRZUEVfUklTS19SRU5UQVM6ICJyaXNrLnNlcnZpY2VzLmltcG9ydF9sZWFzaW5nX3JlbnRhcyIsCiAgICBUWVBFX05FV19DTElFTlRTOiAiaW1wb3J0X2NsaWVudGVzX251ZXZvcyIsCiAgICBUWVBFX0NST1NTX1NBTEU6ICJpbXBvcnRfdmVudGFfY3J1emFkYSIsCiAgICBUWVBFX0ZJTkFOQ0lBTDogInBnYy5hZG1pbl9tb250aGx5IChtYW51YWwpIiwKfQoKCmRlZiBfc2NvcmVfY29sdW1ucyhjb2xzOiBzZXRbc3RyXSwgcmVxdWlyZWRfZ3JvdXBzOiBsaXN0W2xpc3Rbc3RyXV0pIC0+IGludDoKICAgIHNjb3JlID0gMAogICAgZm9yIGdyb3VwIGluIHJlcXVpcmVkX2dyb3VwczoKICAgICAgICBpZiBhbnkoX25vcm1faGVhZGVyKGcpIGluIGNvbHMgZm9yIGcgaW4gZ3JvdXApOgogICAgICAgICAgICBzY29yZSArPSAxCiAgICByZXR1cm4gc2NvcmUKCgpkZWYgZGV0ZWN0X2Zyb21fbmFtZShmaWxlbmFtZTogc3RyKSAtPiBEZXRlY3Rpb25SZXN1bHQgfCBOb25lOgogICAgbmFtZSA9IChmaWxlbmFtZSBvciAiIikubG93ZXIoKQogICAgY29tcGFjdCA9IHJlLnN1YihyIltcc19cLS5dKyIsICIiLCBuYW1lKQoKICAgIGNoZWNrcyA9IFsKICAgICAgICAoVFlQRV9ORVdfQ0xJRU5UUywgImNsaWVudGVzbnVldm9zIiBpbiBjb21wYWN0IG9yICJjbGllbnRlc19udWV2b3MiIGluIG5hbWUsICJub21icmU6IENsaWVudGVzTnVldm9zIiksCiAgICAgICAgKFRZUEVfQ1JPU1NfU0FMRSwgInZlbnRhY3J1emFkYSIgaW4gY29tcGFjdCwgIm5vbWJyZTogVmVudGFDcnV6YWRhIiksCiAgICAgICAgKFRZUEVfRklOQU5DSUFMLCBuYW1lLnN0YXJ0c3dpdGgoIndjIikgb3IgImVzdGFkb19yZXN1bHRhZG9zIiBpbiBuYW1lIG9yICJlcl8iIGluIG5hbWUsICJub21icmU6IFdDKi9FUiBmaW5hbmNpZXJvIiksCiAgICAgICAgKFRZUEVfUEdPX1RJQ0tFVFMsICJwZ28iIGluIG5hbWUgYW5kICgidGlja2V0IiBpbiBuYW1lIG9yICJjb250cm9sIiBpbiBuYW1lKSwgIm5vbWJyZTogUEdPK3RpY2tldHMvY29udHJvbCIpLAogICAgICAgIChUWVBFX1BHT19DQVRBTE9HTywgInBnbyIgaW4gbmFtZSBhbmQgImFyY2hpdm8iIGluIG5hbWUsICJub21icmU6IFBHTythcmNoaXZvcyIpLAogICAgICAgIChUWVBFX0NSTV9DTElFTlRFUywgImNybSIgaW4gbmFtZSBvciAiaW5mb2NsaWVudGVzIiBpbiBjb21wYWN0LCAibm9tYnJlOiBDUk0vSW5mb0NsaWVudGVzIiksCiAgICAgICAgKFRZUEVfUklTS19SRU5UQVMsICJyZW50YXMiIGluIG5hbWUgYW5kICJsZWFzaW5nIiBpbiBuYW1lLCAibm9tYnJlOiBMZWFzaW5nUmVudGFzIiksCiAgICAgICAgKAogICAgICAgICAgICBUWVBFX1JJU0tfTEVBU0lORywKICAgICAgICAgICAgImJhc2VsZWFzaW5nIiBpbiBjb21wYWN0CiAgICAgICAgICAgIG9yICgiYmFsb24iIGluIG5hbWUgYW5kICJsZWFzaW5nIiBpbiBuYW1lKQogICAgICAgICAgICBvciAoImxlYXNpbmciIGluIG5hbWUgYW5kICJiYXNlIiBpbiBuYW1lKSwKICAgICAgICAgICAgIm5vbWJyZTogQmFzZUxlYXNpbmcvYmFsw7NuIiwKICAgICAgICApLAogICAgXQogICAgZm9yIHRpcG8sIG1hdGNoZWQsIHJlYXNvbiBpbiBjaGVja3M6CiAgICAgICAgaWYgbWF0Y2hlZDoKICAgICAgICAgICAgcmV0dXJuIERldGVjdGlvblJlc3VsdCgKICAgICAgICAgICAgICAgIHRpcG89dGlwbywKICAgICAgICAgICAgICAgIGNvbmZpZGVuY2U9MC44NSwKICAgICAgICAgICAgICAgIGxhYmVsPVRZUEVfTEFCRUxTW3RpcG9dLAogICAgICAgICAgICAgICAgcmVhc29ucz1bcmVhc29uXSwKICAgICAgICAgICAgICAgIGxheWVyPSJub21icmUiLAogICAgICAgICAgICApCiAgICByZXR1cm4gTm9uZQoKCmRlZiBkZXRlY3RfZnJvbV9jb2x1bW5zKGNvbHM6IHNldFtzdHJdKSAtPiBEZXRlY3Rpb25SZXN1bHQgfCBOb25lOgogICAgY2FuZGlkYXRlczogbGlzdFt0dXBsZVtzdHIsIGludCwgbGlzdFtzdHJdXV0gPSBbXQoKICAgIGNybV9zY29yZSA9IF9zY29yZV9jb2x1bW5zKAogICAgICAgIGNvbHMsCiAgICAgICAgW1sibml0Il0sIFsibm9tYnJlIiwgIm5vbWJyZV9jbGllbnRlIiwgImNsaWVudGUiLCAicmF6b25fc29jaWFsIl0sIFsid2NmIiwgIndjbCIsICJ3Y2kiXV0sCiAgICApCiAgICBpZiBjcm1fc2NvcmUgPj0gMjoKICAgICAgICBjYW5kaWRhdGVzLmFwcGVuZCgoVFlQRV9DUk1fQ0xJRU5URVMsIGNybV9zY29yZSwgWyJlc3RydWN0dXJhOiBOSVQvTm9tYnJlL1dDRnxXQ0x8V0NJIl0pKQoKICAgIHBnb19zY29yZSA9IF9zY29yZV9jb2x1bW5zKAogICAgICAgIGNvbHMsCiAgICAgICAgW1siaWQiLCAiY29kaWdvIiwgInRpY2tldCJdLCBbInRpdHVsbyIsICJhc3VudG8iXSwgWyJlc3RhZG8iXSwgWyJmZWNoYV9hcGVydHVyYSIsICJ1c3VhcmlvX3NvbGljaXRhIl1dLAogICAgKQogICAgaWYgcGdvX3Njb3JlID49IDM6CiAgICAgICAgY2FuZGlkYXRlcy5hcHBlbmQoKFRZUEVfUEdPX1RJQ0tFVFMsIHBnb19zY29yZSwgWyJlc3RydWN0dXJhOiBJRC9UaXR1bG8vRXN0YWRvIGhlbHBkZXNrIl0pKQoKICAgIGNhdGFsb2dfc2NvcmUgPSBfc2NvcmVfY29sdW1ucyhjb2xzLCBbWyJjYXJwZXRhIiwgImFyY2hpdm8iXSwgWyJjcmVhZG9fcG9yIiwgImNyZWFkb19lbiJdXSkKICAgIGlmIGNhdGFsb2dfc2NvcmUgPj0gMjoKICAgICAgICBjYW5kaWRhdGVzLmFwcGVuZCgoVFlQRV9QR09fQ0FUQUxPR08sIGNhdGFsb2dfc2NvcmUsIFsiZXN0cnVjdHVyYTogQ2FycGV0YS9BcmNoaXZvIl0pKQoKICAgIGxlYXNpbmdfc2NvcmUgPSBfc2NvcmVfY29sdW1ucygKICAgICAgICBjb2xzLAogICAgICAgIFsKICAgICAgICAgICAgWyJjb250cmFjdF9udW1iZXIiLCAiY29udHJhdG8iLCAibm9fY29udHJhdG8iXSwKICAgICAgICAgICAgWyJjbGllbnRfbmFtZSIsICJjbGllbnRlIiwgIm5vbWJyZV9jbGllbnRlIl0sCiAgICAgICAgICAgIFsiY2FwaXRhbF9iYWxhbmNlIiwgInNhbGRvIiwgImR1ZWRheXMiLCAiZHVlX2RheXMiXSwKICAgICAgICBdLAogICAgKQogICAgaWYgbGVhc2luZ19zY29yZSA+PSAyOgogICAgICAgIGNhbmRpZGF0ZXMuYXBwZW5kKChUWVBFX1JJU0tfTEVBU0lORywgbGVhc2luZ19zY29yZSwgWyJlc3RydWN0dXJhOiBDb250cmFjdC9DbGllbnQvQmFsYW5jZSJdKSkKCiAgICByZW50YXNfc2NvcmUgPSBfc2NvcmVfY29sdW1ucygKICAgICAgICBjb2xzLAogICAgICAgIFtbIm5vX2NvbnRyYXRvIiwgImNvbnRyYXRvIl0sIFsidmVuY2ltaWVudG8iXSwgWyJ2YWxvcl9yZW50YSIsICJyZW50YV90b3RhbCJdLCBbImVzdGFkbyJdXSwKICAgICkKICAgIGlmIHJlbnRhc19zY29yZSA+PSAzOgogICAgICAgIGNhbmRpZGF0ZXMuYXBwZW5kKChUWVBFX1JJU0tfUkVOVEFTLCByZW50YXNfc2NvcmUsIFsiZXN0cnVjdHVyYTogTm9Db250cmF0by9WZW5jaW1pZW50by9WYWxvclJlbnRhIl0pKQoKICAgIG5jX3Njb3JlID0gX3Njb3JlX2NvbHVtbnMoY29scywgW1sidW5lIl0sIFsiY2xpZW50ZSIsICJub21icmUiXSwgWyJmZWNoYSIsICJtZXMiXSwgWyJtb250byIsICJhbW91bnQiLCAiaW5ncmVzbyJdXSkKICAgIGlmICJ1bmUiIGluIGNvbHMgYW5kIG5jX3Njb3JlID49IDI6CiAgICAgICAgY2FuZGlkYXRlcy5hcHBlbmQoKFRZUEVfTkVXX0NMSUVOVFMsIG5jX3Njb3JlLCBbImVzdHJ1Y3R1cmE6IFVORSArIGNsaWVudGUvcGVyaW9kbyJdKSkKCiAgICB4Y19zY29yZSA9IF9zY29yZV9jb2x1bW5zKAogICAgICAgIGNvbHMsCiAgICAgICAgWwogICAgICAgICAgICBbInVuZSIsICJ1bmlkYWQiXSwKICAgICAgICAgICAgWyJwcm9kdWN0b19vcmlnZW4iLCAib3JpZ2VuIiwgInByb2R1Y3RvIl0sCiAgICAgICAgICAgIFsicHJvZHVjdG9fZGVzdGlubyIsICJkZXN0aW5vIiwgImNydXphZG8iXSwKICAgICAgICAgICAgWyJjbGllbnRlIiwgIm5vbWJyZSJdLAogICAgICAgIF0sCiAgICApCiAgICBpZiB4Y19zY29yZSA+PSAzOgogICAgICAgIGNhbmRpZGF0ZXMuYXBwZW5kKChUWVBFX0NST1NTX1NBTEUsIHhjX3Njb3JlLCBbImVzdHJ1Y3R1cmE6IHZlbnRhIGNydXphZGEgb3JpZ2VuL2Rlc3Rpbm8iXSkpCgogICAgaWYgbm90IGNhbmRpZGF0ZXM6CiAgICAgICAgcmV0dXJuIE5vbmUKICAgIGNhbmRpZGF0ZXMuc29ydChrZXk9bGFtYmRhIHg6IHhbMV0sIHJldmVyc2U9VHJ1ZSkKICAgIHRpcG8sIHNjb3JlLCByZWFzb25zID0gY2FuZGlkYXRlc1swXQogICAgY29uZiA9IG1pbigwLjk1LCAwLjU1ICsgMC4xICogc2NvcmUpCiAgICBzdWdnZXN0aW9ucyA9IFsodCwgVFlQRV9MQUJFTFNbdF0pIGZvciB0LCBfLCBfIGluIGNhbmRpZGF0ZXNbMTozXV0KICAgIGFtYmlndW91cyA9IGxlbihjYW5kaWRhdGVzKSA+IDEgYW5kIGNhbmRpZGF0ZXNbMF1bMV0gPT0gY2FuZGlkYXRlc1sxXVsxXQogICAgcmV0dXJuIERldGVjdGlvblJlc3VsdCgKICAgICAgICB0aXBvPXRpcG8sCiAgICAgICAgY29uZmlkZW5jZT1jb25mICogKDAuNzUgaWYgYW1iaWd1b3VzIGVsc2UgMS4wKSwKICAgICAgICBsYWJlbD1UWVBFX0xBQkVMU1t0aXBvXSwKICAgICAgICByZWFzb25zPXJlYXNvbnMsCiAgICAgICAgc3VnZ2VzdGlvbnM9c3VnZ2VzdGlvbnMsCiAgICAgICAgbGF5ZXI9ImVzdHJ1Y3R1cmEiLAogICAgICAgIGFtYmlndW91cz1hbWJpZ3VvdXMsCiAgICAgICAgY2FuZGlkYXRlcz1bKHQsIGZsb2F0KHMpLCAiOyAiLmpvaW4ocikpIGZvciB0LCBzLCByIGluIGNhbmRpZGF0ZXNdLAogICAgKQoKCmRlZiBkZXRlY3RfZnJvbV9jb250ZW50KGRmKSAtPiBEZXRlY3Rpb25SZXN1bHQgfCBOb25lOgogICAgIiIiQ2FwYSAzOiBwYXRyb25lcyBlbiB2YWxvcmVzIGRlIG11ZXN0cmEgKHByaW1lcmFzIGZpbGFzKS4iIiIKICAgIGlmIGRmIGlzIE5vbmUgb3IgZGYuZW1wdHk6CiAgICAgICAgcmV0dXJuIE5vbmUKCiAgICBzYW1wbGUgPSBkZi5oZWFkKDQwKQogICAgY29scyA9IHNldChzYW1wbGUuY29sdW1ucykKICAgIHNjb3JlczogZGljdFtzdHIsIGZsb2F0XSA9IHt9CiAgICByZWFzb25zOiBkaWN0W3N0ciwgbGlzdFtzdHJdXSA9IHt9CgogICAgZGVmIGJ1bXAodGlwbzogc3RyLCBwdHM6IGZsb2F0LCByZWFzb246IHN0cikgLT4gTm9uZToKICAgICAgICBzY29yZXNbdGlwb10gPSBzY29yZXMuZ2V0KHRpcG8sIDAuMCkgKyBwdHMKICAgICAgICByZWFzb25zLnNldGRlZmF1bHQodGlwbywgW10pLmFwcGVuZChyZWFzb24pCgogICAgIyBOSVQgLyBkb2N1bWVudG8gdMOtcGljbyBDUk0KICAgIGZvciBjb2wgaW4gKCJuaXQiLCAiZG9jdW1lbnRvIiwgInJ1YyIsICJpZGVudGlmaWNhY2lvbiIpOgogICAgICAgIGlmIGNvbCBpbiBjb2xzOgogICAgICAgICAgICBzZXJpZXMgPSBzYW1wbGVbY29sXS5hc3R5cGUoc3RyKS5zdHIucmVwbGFjZShyIlxzKyIsICIiLCByZWdleD1UcnVlKQogICAgICAgICAgICBuaXRfaGl0cyA9IHNlcmllcy5zdHIubWF0Y2gociJeXGR7NiwxNH0oLVxkKT8kIikuc3VtKCkKICAgICAgICAgICAgaWYgbml0X2hpdHMgPj0gMzoKICAgICAgICAgICAgICAgIGJ1bXAoVFlQRV9DUk1fQ0xJRU5URVMsIDEuNSwgZiJjb250ZW5pZG86IHtuaXRfaGl0c30gTklUcyBlbiAne2NvbH0nIikKCiAgICAjIEZsYWdzIFVORSBlbiBjb2x1bW5hcyBXQ0YvV0NML1dDSQogICAgdW5lX2ZsYWdfY29scyA9IFtjIGZvciBjIGluICgid2NmIiwgIndjbCIsICJ3Y2kiKSBpZiBjIGluIGNvbHNdCiAgICBpZiB1bmVfZmxhZ19jb2xzOgogICAgICAgIGJ1bXAoVFlQRV9DUk1fQ0xJRU5URVMsIDEuMCwgZiJjb250ZW5pZG86IGNvbHVtbmFzIHByb2R1Y3RvIHsnLCAnLmpvaW4odW5lX2ZsYWdfY29scyl9IikKCiAgICAjIFRpY2tldHMgUEdPOiBlc3RhZG9zIC8gcHJpb3JpZGFkZXMgZnJlY3VlbnRlcwogICAgaWYgImVzdGFkbyIgaW4gY29sczoKICAgICAgICBlc3RhZG9zID0gIiAiLmpvaW4oc2FtcGxlWyJlc3RhZG8iXS5hc3R5cGUoc3RyKS5zdHIubG93ZXIoKS51bmlxdWUoKVs6MjBdKQogICAgICAgIGlmIGFueShrIGluIGVzdGFkb3MgZm9yIGsgaW4gKCJhYmllcnRvIiwgImNlcnJhZG8iLCAicGVuZGllbnRlIiwgImVuIHByb2Nlc28iLCAicmVzdWVsdG8iKSk6CiAgICAgICAgICAgIGJ1bXAoVFlQRV9QR09fVElDS0VUUywgMS4yLCAiY29udGVuaWRvOiBlc3RhZG9zIHRpcG8gaGVscGRlc2siKQogICAgICAgIGlmIGFueShrIGluIGVzdGFkb3MgZm9yIGsgaW4gKCJ2aWdlbnRlIiwgInZlbmNpZCIsICJwYWdhZCIsICJtb3JhIikpOgogICAgICAgICAgICBidW1wKFRZUEVfUklTS19SRU5UQVMsIDEuMCwgImNvbnRlbmlkbzogZXN0YWRvcyB0aXBvIHJlbnRhL2N1b3RhIikKCiAgICBpZiBhbnkoYyBpbiBjb2xzIGZvciBjIGluICgidGl0dWxvIiwgImFzdW50byIpKSBhbmQgYW55KGMgaW4gY29scyBmb3IgYyBpbiAoImlkIiwgImNvZGlnbyIsICJ0aWNrZXQiKSk6CiAgICAgICAgYnVtcChUWVBFX1BHT19USUNLRVRTLCAwLjgsICJjb250ZW5pZG86IGlkK3RpdHVsbyB0aWNrZXQiKQoKICAgICMgTGVhc2luZzogZMOtYXMgZGUgbW9yYSAvIHNhbGRvCiAgICBmb3IgY29sIGluICgiZHVlZGF5cyIsICJkdWVfZGF5cyIsICJkaWFzX21vcmEiLCAiZGlhc21vcmEiKToKICAgICAgICBpZiBjb2wgaW4gY29sczoKICAgICAgICAgICAgbnVtZXJpYyA9IHNhbXBsZVtjb2xdLmFwcGx5KGxhbWJkYSB2OiBfaXNfbnVtYmVyKHYpKQogICAgICAgICAgICBpZiBudW1lcmljLnN1bSgpID49IDM6CiAgICAgICAgICAgICAgICBidW1wKFRZUEVfUklTS19MRUFTSU5HLCAxLjMsIGYiY29udGVuaWRvOiBkw61hcyBtb3JhIGVuICd7Y29sfSciKQoKICAgIGZvciBjb2wgaW4gKCJjYXBpdGFsX2JhbGFuY2UiLCAic2FsZG8iLCAic2FsZG9fY2FwaXRhbCIsICJvdXRzdGFuZGluZyIpOgogICAgICAgIGlmIGNvbCBpbiBjb2xzIGFuZCBzYW1wbGVbY29sXS5hcHBseShfaXNfbnVtYmVyKS5zdW0oKSA+PSAzOgogICAgICAgICAgICBidW1wKFRZUEVfUklTS19MRUFTSU5HLCAwLjksIGYiY29udGVuaWRvOiBzYWxkb3MgZW4gJ3tjb2x9JyIpCgogICAgZm9yIGNvbCBpbiAoInZhbG9yX3JlbnRhIiwgInJlbnRhX3RvdGFsIiwgIm1vbnRvX3JlbnRhIik6CiAgICAgICAgaWYgY29sIGluIGNvbHMgYW5kIHNhbXBsZVtjb2xdLmFwcGx5KF9pc19udW1iZXIpLnN1bSgpID49IDM6CiAgICAgICAgICAgIGJ1bXAoVFlQRV9SSVNLX1JFTlRBUywgMS4yLCBmImNvbnRlbmlkbzogbW9udG9zIHJlbnRhIGVuICd7Y29sfSciKQoKICAgICMgQ2xpZW50ZXMgbnVldm9zOiBjw7NkaWdvcyBVTkUKICAgIGlmICJ1bmUiIGluIGNvbHM6CiAgICAgICAgdW5lcyA9ICIgIi5qb2luKHNhbXBsZVsidW5lIl0uYXN0eXBlKHN0cikuc3RyLnVwcGVyKCkudW5pcXVlKClbOjMwXSkKICAgICAgICBpZiBhbnkoayBpbiB1bmVzIGZvciBrIGluICgiV0NGIiwgIldDTCIsICJXQ0kiLCAiSU5WRVNUIiwgIkZBQ1RPUiIpKToKICAgICAgICAgICAgYnVtcChUWVBFX05FV19DTElFTlRTLCAxLjQsICJjb250ZW5pZG86IGPDs2RpZ29zIFVORSBjb21lcmNpYWxlcyIpCgogICAgIyBWZW50YSBjcnV6YWRhOiBtZW5jacOzbiBvcmlnZW4vZGVzdGlubyBlbiB2YWxvcmVzIG8gY29sdW1uYXMKICAgIGlmIGFueShjIGluIGNvbHMgZm9yIGMgaW4gKCJwcm9kdWN0b19vcmlnZW4iLCAicHJvZHVjdG9fZGVzdGlubyIsICJvcmlnZW4iLCAiZGVzdGlubyIpKToKICAgICAgICBidW1wKFRZUEVfQ1JPU1NfU0FMRSwgMS4yLCAiY29udGVuaWRvOiBjb2x1bW5hcyBvcmlnZW4vZGVzdGlubyBwcm9kdWN0byIpCgogICAgaWYgbm90IHNjb3JlczoKICAgICAgICByZXR1cm4gTm9uZQoKICAgIHJhbmtlZCA9IHNvcnRlZChzY29yZXMuaXRlbXMoKSwga2V5PWxhbWJkYSB4OiB4WzFdLCByZXZlcnNlPVRydWUpCiAgICBiZXN0X3RpcG8sIGJlc3Rfc2NvcmUgPSByYW5rZWRbMF0KICAgIGNvbmYgPSBtaW4oMC45MiwgMC40NSArIDAuMTIgKiBiZXN0X3Njb3JlKQogICAgYW1iaWd1b3VzID0gbGVuKHJhbmtlZCkgPiAxIGFuZCAocmFua2VkWzBdWzFdIC0gcmFua2VkWzFdWzFdKSA8IDAuNgogICAgc3VnZ2VzdGlvbnMgPSBbKHQsIFRZUEVfTEFCRUxTW3RdKSBmb3IgdCwgXyBpbiByYW5rZWRbMTozXSBpZiB0IGluIFRZUEVfTEFCRUxTXQogICAgcmV0dXJuIERldGVjdGlvblJlc3VsdCgKICAgICAgICB0aXBvPWJlc3RfdGlwbywKICAgICAgICBjb25maWRlbmNlPWNvbmYgKiAoMC43IGlmIGFtYmlndW91cyBlbHNlIDEuMCksCiAgICAgICAgbGFiZWw9VFlQRV9MQUJFTFMuZ2V0KGJlc3RfdGlwbywgYmVzdF90aXBvKSwKICAgICAgICByZWFzb25zPXJlYXNvbnMuZ2V0KGJlc3RfdGlwbywgW10pWzo0XSwKICAgICAgICBzdWdnZXN0aW9ucz1zdWdnZXN0aW9ucywKICAgICAgICBsYXllcj0iY29udGVuaWRvIiwKICAgICAgICBhbWJpZ3VvdXM9YW1iaWd1b3VzLAogICAgICAgIGNhbmRpZGF0ZXM9Wyh0LCBzLCAiOyAiLmpvaW4ocmVhc29ucy5nZXQodCwgW10pWzoyXSkpIGZvciB0LCBzIGluIHJhbmtlZF0sCiAgICApCgoKZGVmIF9pc19udW1iZXIodmFsdWUpIC0+IGJvb2w6CiAgICB0cnk6CiAgICAgICAgaWYgdmFsdWUgaXMgTm9uZToKICAgICAgICAgICAgcmV0dXJuIEZhbHNlCiAgICAgICAgcyA9IHN0cih2YWx1ZSkuc3RyaXAoKS5yZXBsYWNlKCIsIiwgIiIpCiAgICAgICAgaWYgbm90IHMgb3Igcy5sb3dlcigpIGluICgibmFuIiwgIm5vbmUiLCAiLSIpOgogICAgICAgICAgICByZXR1cm4gRmFsc2UKICAgICAgICBmbG9hdChzKQogICAgICAgIHJldHVybiBUcnVlCiAgICBleGNlcHQgKFR5cGVFcnJvciwgVmFsdWVFcnJvcik6CiAgICAgICAgcmV0dXJuIEZhbHNlCgoKZGVmIF9tZXJnZV9kZXRlY3Rpb25zKAogICAgYnlfbmFtZTogRGV0ZWN0aW9uUmVzdWx0IHwgTm9uZSwKICAgIGJ5X2NvbHM6IERldGVjdGlvblJlc3VsdCB8IE5vbmUsCiAgICBieV9jb250ZW50OiBEZXRlY3Rpb25SZXN1bHQgfCBOb25lLAopIC0+IERldGVjdGlvblJlc3VsdDoKICAgICIiIkZ1c2lvbmEgbGFzIHRyZXMgY2FwYXMgY29uIHByaW9yaWRhZCBub21icmUg4oaSIGVzdHJ1Y3R1cmEg4oaSIGNvbnRlbmlkby4iIiIKICAgIHZvdGVzOiBkaWN0W3N0ciwgZmxvYXRdID0ge30KICAgIGFsbF9yZWFzb25zOiBsaXN0W3N0cl0gPSBbXQogICAgbGF5ZXJzX3VzZWQ6IGxpc3Rbc3RyXSA9IFtdCgogICAgZGVmIGFkZF92b3RlKGRldDogRGV0ZWN0aW9uUmVzdWx0IHwgTm9uZSwgd2VpZ2h0OiBmbG9hdCkgLT4gTm9uZToKICAgICAgICBpZiBub3QgZGV0IG9yIGRldC50aXBvID09IFRZUEVfVU5LTk9XTjoKICAgICAgICAgICAgcmV0dXJuCiAgICAgICAgdm90ZXNbZGV0LnRpcG9dID0gdm90ZXMuZ2V0KGRldC50aXBvLCAwLjApICsgZGV0LmNvbmZpZGVuY2UgKiB3ZWlnaHQKICAgICAgICBhbGxfcmVhc29ucy5leHRlbmQoZGV0LnJlYXNvbnMpCiAgICAgICAgaWYgZGV0LmxheWVyOgogICAgICAgICAgICBsYXllcnNfdXNlZC5hcHBlbmQoZGV0LmxheWVyKQoKICAgICMgUGVzb3M6IG5vbWJyZSBmdWVydGUgc2kgY29pbmNpZGU7IGVzdHJ1Y3R1cmEgeSBjb250ZW5pZG8gcmVmdWVyemFuCiAgICBhZGRfdm90ZShieV9uYW1lLCAxLjApCiAgICBhZGRfdm90ZShieV9jb2xzLCAxLjE1KQogICAgYWRkX3ZvdGUoYnlfY29udGVudCwgMS4wNSkKCiAgICBpZiBub3Qgdm90ZXM6CiAgICAgICAgcmV0dXJuIERldGVjdGlvblJlc3VsdCgKICAgICAgICAgICAgdGlwbz1UWVBFX1VOS05PV04sCiAgICAgICAgICAgIGNvbmZpZGVuY2U9MC4wLAogICAgICAgICAgICBsYWJlbD1UWVBFX0xBQkVMU1tUWVBFX1VOS05PV05dLAogICAgICAgICAgICByZWFzb25zPVsiTm8gc2UgcHVkbyBpZGVudGlmaWNhciBlbCB0aXBvIGNvbiBuaW5ndW5hIGNhcGEiXSwKICAgICAgICAgICAgc3VnZ2VzdGlvbnM9Wyh0LCBUWVBFX0xBQkVMU1t0XSkgZm9yIHQgaW4gQUxMX0lNUE9SVEFCTEVdLAogICAgICAgICAgICBsYXllcj0ibmluZ3VuYSIsCiAgICAgICAgICAgIGFtYmlndW91cz1UcnVlLAogICAgICAgICkKCiAgICByYW5rZWQgPSBzb3J0ZWQodm90ZXMuaXRlbXMoKSwga2V5PWxhbWJkYSB4OiB4WzFdLCByZXZlcnNlPVRydWUpCiAgICBiZXN0X3RpcG8sIGJlc3Rfdm90ZSA9IHJhbmtlZFswXQogICAgc2Vjb25kX3ZvdGUgPSByYW5rZWRbMV1bMV0gaWYgbGVuKHJhbmtlZCkgPiAxIGVsc2UgMC4wCgogICAgIyBBY3VlcmRvIG5vbWJyZSArIGVzdHJ1Y3R1cmEg4oaSIGFsdGEgY29uZmlhbnphCiAgICBuYW1lX3RpcG8gPSBieV9uYW1lLnRpcG8gaWYgYnlfbmFtZSBlbHNlIE5vbmUKICAgIGNvbHNfdGlwbyA9IGJ5X2NvbHMudGlwbyBpZiBieV9jb2xzIGVsc2UgTm9uZQogICAgY29udGVudF90aXBvID0gYnlfY29udGVudC50aXBvIGlmIGJ5X2NvbnRlbnQgZWxzZSBOb25lCgogICAgYWdyZWVtZW50ID0gc3VtKAogICAgICAgIDEKICAgICAgICBmb3IgdCBpbiAobmFtZV90aXBvLCBjb2xzX3RpcG8sIGNvbnRlbnRfdGlwbykKICAgICAgICBpZiB0IGFuZCB0ID09IGJlc3RfdGlwbwogICAgKQoKICAgIGNvbmZpZGVuY2UgPSBtaW4oMC45OSwgYmVzdF92b3RlIC8gbWF4KDEuMCwgYWdyZWVtZW50ICsgMC41KSkKICAgIGlmIGFncmVlbWVudCA+PSAyOgogICAgICAgIGNvbmZpZGVuY2UgPSBtYXgoY29uZmlkZW5jZSwgMC44OCkKICAgIGlmIGFncmVlbWVudCA+PSAzOgogICAgICAgIGNvbmZpZGVuY2UgPSBtYXgoY29uZmlkZW5jZSwgMC45NSkKCiAgICBjb25mbGljdCA9IEZhbHNlCiAgICBpZiBuYW1lX3RpcG8gYW5kIGNvbHNfdGlwbyBhbmQgbmFtZV90aXBvICE9IGNvbHNfdGlwbzoKICAgICAgICBjb25mbGljdCA9IFRydWUKICAgICAgICBhbGxfcmVhc29ucy5hcHBlbmQoZiJjb25mbGljdG8gbm9tYnJlKHtuYW1lX3RpcG99KSB2cyBlc3RydWN0dXJhKHtjb2xzX3RpcG99KSIpCiAgICAgICAgY29uZmlkZW5jZSA9IG1pbihjb25maWRlbmNlLCAwLjcyKQoKICAgIGlmIGNvbnRlbnRfdGlwbyBhbmQgY29sc190aXBvIGFuZCBjb250ZW50X3RpcG8gIT0gY29sc190aXBvIGFuZCBhZ3JlZW1lbnQgPCAyOgogICAgICAgIGNvbmZsaWN0ID0gVHJ1ZQogICAgICAgIGFsbF9yZWFzb25zLmFwcGVuZChmImNvbnRlbmlkbyh7Y29udGVudF90aXBvfSkgZGlmaWVyZSBkZSBlc3RydWN0dXJhKHtjb2xzX3RpcG99KSIpCgogICAgbWFyZ2luX3RpZ2h0ID0gKGJlc3Rfdm90ZSAtIHNlY29uZF92b3RlKSA8IDAuMjUgYW5kIGxlbihyYW5rZWQpID4gMQogICAgYW1iaWd1b3VzID0gY29uZmxpY3Qgb3IgbWFyZ2luX3RpZ2h0IG9yIGNvbmZpZGVuY2UgPCBDT05GSURFTkNFX0FVVE8KCiAgICBzdWdnZXN0aW9uczogbGlzdFt0dXBsZVtzdHIsIHN0cl1dID0gW10KICAgIGZvciB0LCBfIGluIHJhbmtlZFsxOjRdOgogICAgICAgIGlmIHQgaW4gVFlQRV9MQUJFTFM6CiAgICAgICAgICAgIHN1Z2dlc3Rpb25zLmFwcGVuZCgodCwgVFlQRV9MQUJFTFNbdF0pKQogICAgIyBJbmNsdWlyIGNhcGFzIGRpc2NyZXBhbnRlcwogICAgZm9yIHQgaW4gKG5hbWVfdGlwbywgY29sc190aXBvLCBjb250ZW50X3RpcG8pOgogICAgICAgIGlmIHQgYW5kIHQgIT0gYmVzdF90aXBvIGFuZCB0IGluIFRZUEVfTEFCRUxTOgogICAgICAgICAgICBwYWlyID0gKHQsIFRZUEVfTEFCRUxTW3RdKQogICAgICAgICAgICBpZiBwYWlyIG5vdCBpbiBzdWdnZXN0aW9uczoKICAgICAgICAgICAgICAgIHN1Z2dlc3Rpb25zLmFwcGVuZChwYWlyKQoKICAgIGxheWVyID0gIisiLmpvaW4oZGljdC5mcm9ta2V5cyhsYXllcnNfdXNlZCkpIG9yICJjb21iaW5hZGEiCiAgICBpZiBhZ3JlZW1lbnQgPj0gMjoKICAgICAgICBsYXllciA9IGYiY29tYmluYWRhKHthZ3JlZW1lbnR9IGNhcGFzKSIKCiAgICByZXR1cm4gRGV0ZWN0aW9uUmVzdWx0KAogICAgICAgIHRpcG89YmVzdF90aXBvLAogICAgICAgIGNvbmZpZGVuY2U9Y29uZmlkZW5jZSwKICAgICAgICBsYWJlbD1UWVBFX0xBQkVMUy5nZXQoYmVzdF90aXBvLCBiZXN0X3RpcG8pLAogICAgICAgIHJlYXNvbnM9bGlzdChkaWN0LmZyb21rZXlzKGFsbF9yZWFzb25zKSlbOjhdLAogICAgICAgIHN1Z2dlc3Rpb25zPXN1Z2dlc3Rpb25zWzo0XSwKICAgICAgICBsYXllcj1sYXllciwKICAgICAgICBhbWJpZ3VvdXM9YW1iaWd1b3VzLAogICAgICAgIGNhbmRpZGF0ZXM9Wyh0LCB2LCAiIikgZm9yIHQsIHYgaW4gcmFua2VkXSwKICAgICkKCgpkZWYgZGV0ZWN0X2ZpbGUodXBsb2FkZWRfZmlsZSkgLT4gRGV0ZWN0aW9uUmVzdWx0OgogICAgYnlfbmFtZSA9IGRldGVjdF9mcm9tX25hbWUoZ2V0YXR0cih1cGxvYWRlZF9maWxlLCAibmFtZSIsICIiKSBvciAiIikKICAgIGRmID0gTm9uZQogICAgYnlfY29scyA9IE5vbmUKICAgIGJ5X2NvbnRlbnQgPSBOb25lCgogICAgdHJ5OgogICAgICAgIGRmID0gbm9ybWFsaXplX2NvbHVtbnMocmVhZF9kYXRhZnJhbWUodXBsb2FkZWRfZmlsZSwgc2hlZXRfbmFtZT1Ob25lKSkKICAgICAgICB1cGxvYWRlZF9maWxlLnNlZWsoMCkKICAgICAgICBjb2xzID0gc2V0KGRmLmNvbHVtbnMpCiAgICAgICAgYnlfY29scyA9IGRldGVjdF9mcm9tX2NvbHVtbnMoY29scykKICAgICAgICBieV9jb250ZW50ID0gZGV0ZWN0X2Zyb21fY29udGVudChkZikKICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZXhjOgogICAgICAgIHVwbG9hZGVkX2ZpbGUuc2VlaygwKQogICAgICAgIGlmIGJ5X25hbWUgYW5kIGJ5X25hbWUuY29uZmlkZW5jZSA+PSAwLjg6CiAgICAgICAgICAgIGJ5X25hbWUucmVhc29ucy5hcHBlbmQoZiJjb2x1bW5hcyBubyBsZcOtZGFzICh7ZXhjfSkiKQogICAgICAgICAgICBieV9uYW1lLmFtYmlndW91cyA9IEZhbHNlCiAgICAgICAgICAgIHJldHVybiBieV9uYW1lCiAgICAgICAgcmV0dXJuIERldGVjdGlvblJlc3VsdCgKICAgICAgICAgICAgdGlwbz1UWVBFX1VOS05PV04sCiAgICAgICAgICAgIGNvbmZpZGVuY2U9MC4wLAogICAgICAgICAgICBsYWJlbD1UWVBFX0xBQkVMU1tUWVBFX1VOS05PV05dLAogICAgICAgICAgICByZWFzb25zPVtmIk5vIHNlIHB1ZG8gbGVlciBlbCBhcmNoaXZvOiB7ZXhjfSJdLAogICAgICAgICAgICBzdWdnZXN0aW9ucz1bKHQsIFRZUEVfTEFCRUxTW3RdKSBmb3IgdCBpbiBBTExfSU1QT1JUQUJMRVs6NV1dLAogICAgICAgICAgICBsYXllcj0iZXJyb3IiLAogICAgICAgICAgICBhbWJpZ3VvdXM9VHJ1ZSwKICAgICAgICApCgogICAgcmV0dXJuIF9tZXJnZV9kZXRlY3Rpb25zKGJ5X25hbWUsIGJ5X2NvbHMsIGJ5X2NvbnRlbnQpCgoKZGVmIGRldGVjdF9wYXRoKHBhdGg6IHN0cikgLT4gRGV0ZWN0aW9uUmVzdWx0OgogICAgZnJvbSBwYXRobGliIGltcG9ydCBQYXRoCgogICAgZnJvbSBkamFuZ28uY29yZS5maWxlcy51cGxvYWRlZGZpbGUgaW1wb3J0IFNpbXBsZVVwbG9hZGVkRmlsZQoKICAgIHAgPSBQYXRoKHBhdGgpCiAgICBmID0gU2ltcGxlVXBsb2FkZWRGaWxlKHAubmFtZSwgcC5yZWFkX2J5dGVzKCkpCiAgICByZXR1cm4gZGV0ZWN0X2ZpbGUoZikK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/dispatch.py
PATH_JSON="imports/dispatch.py"
FILENAME=dispatch.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=291
SIZE_BYTES_UTF8=10337
CONTENT_SHA256=3b2e38694da9add80817a439c8d055f3b062ecf415963375355fa38ac85f1636
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Despacho unificado de importaciones WCG (CRM / PGO / Risk / PGC)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.core.management import call_command

from imports.detection import (
    IMPORTER_LABELS,
    TYPE_CRM_CLIENTES,
    TYPE_CROSS_SALE,
    TYPE_FINANCIAL,
    TYPE_LABELS,
    TYPE_NEW_CLIENTS,
    TYPE_PGO_CATALOGO,
    TYPE_PGO_TICKETS,
    TYPE_RISK_LEASING,
    TYPE_RISK_RENTAS,
    TYPE_UNKNOWN,
    DetectionResult,
    detect_file,
)


@dataclass
class DispatchResult:
    tipo: str
    label: str
    detection: DetectionResult
    batch: object | None = None
    message: str = ""
    ok: bool = False
    redirect_hint: str = ""
    needs_manual: bool = False
    forced: bool = False


def _batch_summary(batch) -> str:
    if batch is None:
        return ""
    if hasattr(batch, "creados"):
        return (
            f"{batch.creados} creados, {batch.actualizados} actualizados, "
            f"{batch.errores} errores (filas {getattr(batch, 'filas_leidas', '?')})"
        )
    return str(batch)


def _detection_log(detection: DetectionResult, tipo: str, forced: bool) -> str:
    importer = IMPORTER_LABELS.get(tipo, tipo)
    mode = "forzado" if forced else ("auto" if detection.can_auto_import else "manual")
    return (
        f"[detección] {detection.rule_summary} | importador={importer} | modo={mode}"
    )


def _annotate_batch(batch, detection: DetectionResult, tipo: str, forced: bool) -> None:
    if batch is None or not hasattr(batch, "log_texto"):
        return
    header = _detection_log(detection, tipo, forced)
    existing = (batch.log_texto or "").strip()
    batch.log_texto = (header + ("\n" + existing if existing else ""))[:8000]
    batch.save(update_fields=["log_texto"])


def run_import(user, uploaded_file: UploadedFile, tipo_forzado: str | None = None) -> DispatchResult:
    detection = detect_file(uploaded_file)
    uploaded_file.seek(0)
    forced = bool(tipo_forzado)
    tipo = tipo_forzado or detection.tipo

    if not forced and (detection.ambiguous or not detection.can_auto_import or tipo == TYPE_UNKNOWN):
        return DispatchResult(
            tipo=tipo if tipo != TYPE_UNKNOWN else TYPE_UNKNOWN,
            label=TYPE_LABELS.get(tipo, TYPE_LABELS[TYPE_UNKNOWN]),
            detection=detection,
            message=(
                "Ambigüedad en la detección. Seleccione el tipo de importación "
                "manualmente y vuelva a enviar el archivo."
                if detection.ambiguous or tipo == TYPE_UNKNOWN
                else "Confianza insuficiente para importar automáticamente. Confirme el tipo."
            ),
            ok=False,
            needs_manual=True,
        )

    if tipo == TYPE_UNKNOWN or not tipo:
        return DispatchResult(
            tipo=TYPE_UNKNOWN,
            label=TYPE_LABELS[TYPE_UNKNOWN],
            detection=detection,
            message="No se pudo identificar el tipo. Elija una opción sugerida.",
            ok=False,
            needs_manual=True,
        )

    label = TYPE_LABELS.get(tipo, tipo)

    if tipo == TYPE_CRM_CLIENTES:
        from crm import services as crm_services

        batch = crm_services.import_entidades(user, uploaded_file)
        _annotate_batch(batch, detection, tipo, forced)
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=f"CRM: {_batch_summary(batch)}",
            ok=batch.status in ("OK", "PARTIAL"),
            redirect_hint="crm:entidad_list",
            forced=forced,
        )

    if tipo == TYPE_PGO_TICKETS:
        from pgo import services as pgo_services
        from pgo.periodo import recalculate_pgo_periodos

        batch = pgo_services.import_tickets(user, uploaded_file)
        recalculate_pgo_periodos()
        _annotate_batch(batch, detection, tipo, forced)
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=f"PGO tickets: {_batch_summary(batch)}",
            ok=batch.status in ("OK", "PARTIAL"),
            redirect_hint="pgo:dashboard",
            forced=forced,
        )

    if tipo == TYPE_PGO_CATALOGO:
        from pgo import services as pgo_services

        batch = pgo_services.import_archivos_catalogo(user, uploaded_file)
        _annotate_batch(batch, detection, tipo, forced)
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=f"Catálogo PGO registrado ({batch.filas_leidas} filas).",
            ok=True,
            redirect_hint="pgo:dashboard",
            forced=forced,
        )

    if tipo == TYPE_RISK_LEASING:
        from risk import services as risk_services

        batch = risk_services.import_leasing_database(user, uploaded_file)
        _annotate_batch(batch, detection, tipo, forced)
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=f"Balón leasing: {_batch_summary(batch)}",
            ok=batch.status in ("OK", "PARTIAL"),
            redirect_hint="risk:comando_balon",
            forced=forced,
        )

    if tipo == TYPE_RISK_RENTAS:
        from risk import services as risk_services

        batch = risk_services.import_leasing_rentas(user, uploaded_file)
        _annotate_batch(batch, detection, tipo, forced)
        return DispatchResult(
            tipo=tipo,
            label=label,
            detection=detection,
            batch=batch,
            message=f"Rentas leasing: {_batch_summary(batch)}",
            ok=batch.status in ("OK", "PARTIAL"),
            redirect_hint="risk:comando_balon",
            forced=forced,
        )

    if tipo in (TYPE_NEW_CLIENTS, TYPE_CROSS_SALE, TYPE_FINANCIAL):
        from imports.models import FileImportLog, FileUpload, guess_file_format

        tmp = FileUpload(
            uploaded_by=user,
            original_filename=uploaded_file.name,
            file_format=guess_file_format(uploaded_file.name),
            file_type_detected={
                TYPE_NEW_CLIENTS: FileUpload.TYPE_NEW_CLIENTS,
                TYPE_CROSS_SALE: FileUpload.TYPE_CROSS_SALE,
                TYPE_FINANCIAL: FileUpload.TYPE_FINANCIAL,
            }[tipo],
            status=FileUpload.STATUS_UPLOADED,
            parsing_notes=_detection_log(detection, tipo, forced),
        )
        tmp.stored_file.save(uploaded_file.name, uploaded_file, save=True)
        FileImportLog.objects.create(
            file_upload=tmp,
            step_code="detect",
            level=FileImportLog.LEVEL_INFO,
            message=_detection_log(detection, tipo, forced),
            payload_json={
                "tipo": tipo,
                "layer": detection.layer,
                "confidence": detection.confidence,
                "reasons": detection.reasons,
                "forced": forced,
                "importer": IMPORTER_LABELS.get(tipo),
            },
        )
        path = Path(tmp.stored_file.path)
        try:
            if tipo == TYPE_NEW_CLIENTS:
                call_command("import_clientes_nuevos", path=str(path), file_upload_id=tmp.id)
            elif tipo == TYPE_CROSS_SALE:
                call_command("import_venta_cruzada", path=str(path))
            else:
                tmp.status = FileUpload.STATUS_UPLOADED
                tmp.parsing_notes = (
                    _detection_log(detection, tipo, forced)
                    + " | Subido vía Administración → Importación. "
                    "Procesar en Admin PGC mensual (requiere año/mes)."
                )
                tmp.save(update_fields=["status", "parsing_notes"])
                return DispatchResult(
                    tipo=tipo,
                    label=label,
                    detection=detection,
                    batch=tmp,
                    message=(
                        "Archivo financiero WC* guardado. "
                        "Complételo en Admin PGC → período mensual (requiere año/mes)."
                    ),
                    ok=True,
                    redirect_hint="pgc:admin_monthly",
                    forced=forced,
                )
            tmp.status = FileUpload.STATUS_PARSED_OK
            tmp.save(update_fields=["status"])
            FileImportLog.objects.create(
                file_upload=tmp,
                step_code="dispatch",
                level=FileImportLog.LEVEL_INFO,
                message=f"Procesado con {IMPORTER_LABELS.get(tipo, tipo)}",
            )
            return DispatchResult(
                tipo=tipo,
                label=label,
                detection=detection,
                batch=tmp,
                message=f"{label}: procesado correctamente.",
                ok=True,
                redirect_hint="pgc:admin_monthly" if tipo != TYPE_NEW_CLIENTS else "pgc:clientes_nuevos",
                forced=forced,
            )
        except Exception as exc:
            tmp.status = FileUpload.STATUS_PARSED_ERROR
            tmp.error_summary = str(exc)[:500]
            tmp.save(update_fields=["status", "error_summary"])
            FileImportLog.objects.create(
                file_upload=tmp,
                step_code="dispatch",
                level=FileImportLog.LEVEL_ERROR,
                message=str(exc)[:1000],
            )
            return DispatchResult(
                tipo=tipo,
                label=label,
                detection=detection,
                batch=tmp,
                message=f"Error al procesar: {exc}",
                ok=False,
                forced=forced,
            )

    return DispatchResult(
        tipo=tipo,
        label=label,
        detection=detection,
        message=f"Tipo '{tipo}' aún no tiene despacho automático.",
        ok=False,
    )


def run_import_path(user, path: str, tipo_forzado: str | None = None) -> DispatchResult:
    p = Path(path)
    f = SimpleUploadedFile(p.name, p.read_bytes())
    return run_import(user, f, tipo_forzado=tipo_forzado)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Despacho unificado de importaciones WCG (CRM / PGO / Risk / PGC)."""
00002|
00003|from __future__ import annotations
00004|
00005|from dataclasses import dataclass
00006|from pathlib import Path
00007|
00008|from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
00009|from django.core.management import call_command
00010|
00011|from imports.detection import (
00012|    IMPORTER_LABELS,
00013|    TYPE_CRM_CLIENTES,
00014|    TYPE_CROSS_SALE,
00015|    TYPE_FINANCIAL,
00016|    TYPE_LABELS,
00017|    TYPE_NEW_CLIENTS,
00018|    TYPE_PGO_CATALOGO,
00019|    TYPE_PGO_TICKETS,
00020|    TYPE_RISK_LEASING,
00021|    TYPE_RISK_RENTAS,
00022|    TYPE_UNKNOWN,
00023|    DetectionResult,
00024|    detect_file,
00025|)
00026|
00027|
00028|@dataclass
00029|class DispatchResult:
00030|    tipo: str
00031|    label: str
00032|    detection: DetectionResult
00033|    batch: object | None = None
00034|    message: str = ""
00035|    ok: bool = False
00036|    redirect_hint: str = ""
00037|    needs_manual: bool = False
00038|    forced: bool = False
00039|
00040|
00041|def _batch_summary(batch) -> str:
00042|    if batch is None:
00043|        return ""
00044|    if hasattr(batch, "creados"):
00045|        return (
00046|            f"{batch.creados} creados, {batch.actualizados} actualizados, "
00047|            f"{batch.errores} errores (filas {getattr(batch, 'filas_leidas', '?')})"
00048|        )
00049|    return str(batch)
00050|
00051|
00052|def _detection_log(detection: DetectionResult, tipo: str, forced: bool) -> str:
00053|    importer = IMPORTER_LABELS.get(tipo, tipo)
00054|    mode = "forzado" if forced else ("auto" if detection.can_auto_import else "manual")
00055|    return (
00056|        f"[detección] {detection.rule_summary} | importador={importer} | modo={mode}"
00057|    )
00058|
00059|
00060|def _annotate_batch(batch, detection: DetectionResult, tipo: str, forced: bool) -> None:
00061|    if batch is None or not hasattr(batch, "log_texto"):
00062|        return
00063|    header = _detection_log(detection, tipo, forced)
00064|    existing = (batch.log_texto or "").strip()
00065|    batch.log_texto = (header + ("\n" + existing if existing else ""))[:8000]
00066|    batch.save(update_fields=["log_texto"])
00067|
00068|
00069|def run_import(user, uploaded_file: UploadedFile, tipo_forzado: str | None = None) -> DispatchResult:
00070|    detection = detect_file(uploaded_file)
00071|    uploaded_file.seek(0)
00072|    forced = bool(tipo_forzado)
00073|    tipo = tipo_forzado or detection.tipo
00074|
00075|    if not forced and (detection.ambiguous or not detection.can_auto_import or tipo == TYPE_UNKNOWN):
00076|        return DispatchResult(
00077|            tipo=tipo if tipo != TYPE_UNKNOWN else TYPE_UNKNOWN,
00078|            label=TYPE_LABELS.get(tipo, TYPE_LABELS[TYPE_UNKNOWN]),
00079|            detection=detection,
00080|            message=(
00081|                "Ambigüedad en la detección. Seleccione el tipo de importación "
00082|                "manualmente y vuelva a enviar el archivo."
00083|                if detection.ambiguous or tipo == TYPE_UNKNOWN
00084|                else "Confianza insuficiente para importar automáticamente. Confirme el tipo."
00085|            ),
00086|            ok=False,
00087|            needs_manual=True,
00088|        )
00089|
00090|    if tipo == TYPE_UNKNOWN or not tipo:
00091|        return DispatchResult(
00092|            tipo=TYPE_UNKNOWN,
00093|            label=TYPE_LABELS[TYPE_UNKNOWN],
00094|            detection=detection,
00095|            message="No se pudo identificar el tipo. Elija una opción sugerida.",
00096|            ok=False,
00097|            needs_manual=True,
00098|        )
00099|
00100|    label = TYPE_LABELS.get(tipo, tipo)
00101|
00102|    if tipo == TYPE_CRM_CLIENTES:
00103|        from crm import services as crm_services
00104|
00105|        batch = crm_services.import_entidades(user, uploaded_file)
00106|        _annotate_batch(batch, detection, tipo, forced)
00107|        return DispatchResult(
00108|            tipo=tipo,
00109|            label=label,
00110|            detection=detection,
00111|            batch=batch,
00112|            message=f"CRM: {_batch_summary(batch)}",
00113|            ok=batch.status in ("OK", "PARTIAL"),
00114|            redirect_hint="crm:entidad_list",
00115|            forced=forced,
00116|        )
00117|
00118|    if tipo == TYPE_PGO_TICKETS:
00119|        from pgo import services as pgo_services
00120|        from pgo.periodo import recalculate_pgo_periodos
00121|
00122|        batch = pgo_services.import_tickets(user, uploaded_file)
00123|        recalculate_pgo_periodos()
00124|        _annotate_batch(batch, detection, tipo, forced)
00125|        return DispatchResult(
00126|            tipo=tipo,
00127|            label=label,
00128|            detection=detection,
00129|            batch=batch,
00130|            message=f"PGO tickets: {_batch_summary(batch)}",
00131|            ok=batch.status in ("OK", "PARTIAL"),
00132|            redirect_hint="pgo:dashboard",
00133|            forced=forced,
00134|        )
00135|
00136|    if tipo == TYPE_PGO_CATALOGO:
00137|        from pgo import services as pgo_services
00138|
00139|        batch = pgo_services.import_archivos_catalogo(user, uploaded_file)
00140|        _annotate_batch(batch, detection, tipo, forced)
00141|        return DispatchResult(
00142|            tipo=tipo,
00143|            label=label,
00144|            detection=detection,
00145|            batch=batch,
00146|            message=f"Catálogo PGO registrado ({batch.filas_leidas} filas).",
00147|            ok=True,
00148|            redirect_hint="pgo:dashboard",
00149|            forced=forced,
00150|        )
00151|
00152|    if tipo == TYPE_RISK_LEASING:
00153|        from risk import services as risk_services
00154|
00155|        batch = risk_services.import_leasing_database(user, uploaded_file)
00156|        _annotate_batch(batch, detection, tipo, forced)
00157|        return DispatchResult(
00158|            tipo=tipo,
00159|            label=label,
00160|            detection=detection,
00161|            batch=batch,
00162|            message=f"Balón leasing: {_batch_summary(batch)}",
00163|            ok=batch.status in ("OK", "PARTIAL"),
00164|            redirect_hint="risk:comando_balon",
00165|            forced=forced,
00166|        )
00167|
00168|    if tipo == TYPE_RISK_RENTAS:
00169|        from risk import services as risk_services
00170|
00171|        batch = risk_services.import_leasing_rentas(user, uploaded_file)
00172|        _annotate_batch(batch, detection, tipo, forced)
00173|        return DispatchResult(
00174|            tipo=tipo,
00175|            label=label,
00176|            detection=detection,
00177|            batch=batch,
00178|            message=f"Rentas leasing: {_batch_summary(batch)}",
00179|            ok=batch.status in ("OK", "PARTIAL"),
00180|            redirect_hint="risk:comando_balon",
00181|            forced=forced,
00182|        )
00183|
00184|    if tipo in (TYPE_NEW_CLIENTS, TYPE_CROSS_SALE, TYPE_FINANCIAL):
00185|        from imports.models import FileImportLog, FileUpload, guess_file_format
00186|
00187|        tmp = FileUpload(
00188|            uploaded_by=user,
00189|            original_filename=uploaded_file.name,
00190|            file_format=guess_file_format(uploaded_file.name),
00191|            file_type_detected={
00192|                TYPE_NEW_CLIENTS: FileUpload.TYPE_NEW_CLIENTS,
00193|                TYPE_CROSS_SALE: FileUpload.TYPE_CROSS_SALE,
00194|                TYPE_FINANCIAL: FileUpload.TYPE_FINANCIAL,
00195|            }[tipo],
00196|            status=FileUpload.STATUS_UPLOADED,
00197|            parsing_notes=_detection_log(detection, tipo, forced),
00198|        )
00199|        tmp.stored_file.save(uploaded_file.name, uploaded_file, save=True)
00200|        FileImportLog.objects.create(
00201|            file_upload=tmp,
00202|            step_code="detect",
00203|            level=FileImportLog.LEVEL_INFO,
00204|            message=_detection_log(detection, tipo, forced),
00205|            payload_json={
00206|                "tipo": tipo,
00207|                "layer": detection.layer,
00208|                "confidence": detection.confidence,
00209|                "reasons": detection.reasons,
00210|                "forced": forced,
00211|                "importer": IMPORTER_LABELS.get(tipo),
00212|            },
00213|        )
00214|        path = Path(tmp.stored_file.path)
00215|        try:
00216|            if tipo == TYPE_NEW_CLIENTS:
00217|                call_command("import_clientes_nuevos", path=str(path), file_upload_id=tmp.id)
00218|            elif tipo == TYPE_CROSS_SALE:
00219|                call_command("import_venta_cruzada", path=str(path))
00220|            else:
00221|                tmp.status = FileUpload.STATUS_UPLOADED
00222|                tmp.parsing_notes = (
00223|                    _detection_log(detection, tipo, forced)
00224|                    + " | Subido vía Administración → Importación. "
00225|                    "Procesar en Admin PGC mensual (requiere año/mes)."
00226|                )
00227|                tmp.save(update_fields=["status", "parsing_notes"])
00228|                return DispatchResult(
00229|                    tipo=tipo,
00230|                    label=label,
00231|                    detection=detection,
00232|                    batch=tmp,
00233|                    message=(
00234|                        "Archivo financiero WC* guardado. "
00235|                        "Complételo en Admin PGC → período mensual (requiere año/mes)."
00236|                    ),
00237|                    ok=True,
00238|                    redirect_hint="pgc:admin_monthly",
00239|                    forced=forced,
00240|                )
00241|            tmp.status = FileUpload.STATUS_PARSED_OK
00242|            tmp.save(update_fields=["status"])
00243|            FileImportLog.objects.create(
00244|                file_upload=tmp,
00245|                step_code="dispatch",
00246|                level=FileImportLog.LEVEL_INFO,
00247|                message=f"Procesado con {IMPORTER_LABELS.get(tipo, tipo)}",
00248|            )
00249|            return DispatchResult(
00250|                tipo=tipo,
00251|                label=label,
00252|                detection=detection,
00253|                batch=tmp,
00254|                message=f"{label}: procesado correctamente.",
00255|                ok=True,
00256|                redirect_hint="pgc:admin_monthly" if tipo != TYPE_NEW_CLIENTS else "pgc:clientes_nuevos",
00257|                forced=forced,
00258|            )
00259|        except Exception as exc:
00260|            tmp.status = FileUpload.STATUS_PARSED_ERROR
00261|            tmp.error_summary = str(exc)[:500]
00262|            tmp.save(update_fields=["status", "error_summary"])
00263|            FileImportLog.objects.create(
00264|                file_upload=tmp,
00265|                step_code="dispatch",
00266|                level=FileImportLog.LEVEL_ERROR,
00267|                message=str(exc)[:1000],
00268|            )
00269|            return DispatchResult(
00270|                tipo=tipo,
00271|                label=label,
00272|                detection=detection,
00273|                batch=tmp,
00274|                message=f"Error al procesar: {exc}",
00275|                ok=False,
00276|                forced=forced,
00277|            )
00278|
00279|    return DispatchResult(
00280|        tipo=tipo,
00281|        label=label,
00282|        detection=detection,
00283|        message=f"Tipo '{tipo}' aún no tiene despacho automático.",
00284|        ok=False,
00285|    )
00286|
00287|
00288|def run_import_path(user, path: str, tipo_forzado: str | None = None) -> DispatchResult:
00289|    p = Path(path)
00290|    f = SimpleUploadedFile(p.name, p.read_bytes())
00291|    return run_import(user, f, tipo_forzado=tipo_forzado)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiRGVzcGFjaG8gdW5pZmljYWRvIGRlIGltcG9ydGFjaW9uZXMgV0NHIChDUk0gLyBQR08gLyBSaXNrIC8gUEdDKS4iIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmZyb20gZGF0YWNsYXNzZXMgaW1wb3J0IGRhdGFjbGFzcwpmcm9tIHBhdGhsaWIgaW1wb3J0IFBhdGgKCmZyb20gZGphbmdvLmNvcmUuZmlsZXMudXBsb2FkZWRmaWxlIGltcG9ydCBTaW1wbGVVcGxvYWRlZEZpbGUsIFVwbG9hZGVkRmlsZQpmcm9tIGRqYW5nby5jb3JlLm1hbmFnZW1lbnQgaW1wb3J0IGNhbGxfY29tbWFuZAoKZnJvbSBpbXBvcnRzLmRldGVjdGlvbiBpbXBvcnQgKAogICAgSU1QT1JURVJfTEFCRUxTLAogICAgVFlQRV9DUk1fQ0xJRU5URVMsCiAgICBUWVBFX0NST1NTX1NBTEUsCiAgICBUWVBFX0ZJTkFOQ0lBTCwKICAgIFRZUEVfTEFCRUxTLAogICAgVFlQRV9ORVdfQ0xJRU5UUywKICAgIFRZUEVfUEdPX0NBVEFMT0dPLAogICAgVFlQRV9QR09fVElDS0VUUywKICAgIFRZUEVfUklTS19MRUFTSU5HLAogICAgVFlQRV9SSVNLX1JFTlRBUywKICAgIFRZUEVfVU5LTk9XTiwKICAgIERldGVjdGlvblJlc3VsdCwKICAgIGRldGVjdF9maWxlLAopCgoKQGRhdGFjbGFzcwpjbGFzcyBEaXNwYXRjaFJlc3VsdDoKICAgIHRpcG86IHN0cgogICAgbGFiZWw6IHN0cgogICAgZGV0ZWN0aW9uOiBEZXRlY3Rpb25SZXN1bHQKICAgIGJhdGNoOiBvYmplY3QgfCBOb25lID0gTm9uZQogICAgbWVzc2FnZTogc3RyID0gIiIKICAgIG9rOiBib29sID0gRmFsc2UKICAgIHJlZGlyZWN0X2hpbnQ6IHN0ciA9ICIiCiAgICBuZWVkc19tYW51YWw6IGJvb2wgPSBGYWxzZQogICAgZm9yY2VkOiBib29sID0gRmFsc2UKCgpkZWYgX2JhdGNoX3N1bW1hcnkoYmF0Y2gpIC0+IHN0cjoKICAgIGlmIGJhdGNoIGlzIE5vbmU6CiAgICAgICAgcmV0dXJuICIiCiAgICBpZiBoYXNhdHRyKGJhdGNoLCAiY3JlYWRvcyIpOgogICAgICAgIHJldHVybiAoCiAgICAgICAgICAgIGYie2JhdGNoLmNyZWFkb3N9IGNyZWFkb3MsIHtiYXRjaC5hY3R1YWxpemFkb3N9IGFjdHVhbGl6YWRvcywgIgogICAgICAgICAgICBmIntiYXRjaC5lcnJvcmVzfSBlcnJvcmVzIChmaWxhcyB7Z2V0YXR0cihiYXRjaCwgJ2ZpbGFzX2xlaWRhcycsICc/Jyl9KSIKICAgICAgICApCiAgICByZXR1cm4gc3RyKGJhdGNoKQoKCmRlZiBfZGV0ZWN0aW9uX2xvZyhkZXRlY3Rpb246IERldGVjdGlvblJlc3VsdCwgdGlwbzogc3RyLCBmb3JjZWQ6IGJvb2wpIC0+IHN0cjoKICAgIGltcG9ydGVyID0gSU1QT1JURVJfTEFCRUxTLmdldCh0aXBvLCB0aXBvKQogICAgbW9kZSA9ICJmb3J6YWRvIiBpZiBmb3JjZWQgZWxzZSAoImF1dG8iIGlmIGRldGVjdGlvbi5jYW5fYXV0b19pbXBvcnQgZWxzZSAibWFudWFsIikKICAgIHJldHVybiAoCiAgICAgICAgZiJbZGV0ZWNjacOzbl0ge2RldGVjdGlvbi5ydWxlX3N1bW1hcnl9IHwgaW1wb3J0YWRvcj17aW1wb3J0ZXJ9IHwgbW9kbz17bW9kZX0iCiAgICApCgoKZGVmIF9hbm5vdGF0ZV9iYXRjaChiYXRjaCwgZGV0ZWN0aW9uOiBEZXRlY3Rpb25SZXN1bHQsIHRpcG86IHN0ciwgZm9yY2VkOiBib29sKSAtPiBOb25lOgogICAgaWYgYmF0Y2ggaXMgTm9uZSBvciBub3QgaGFzYXR0cihiYXRjaCwgImxvZ190ZXh0byIpOgogICAgICAgIHJldHVybgogICAgaGVhZGVyID0gX2RldGVjdGlvbl9sb2coZGV0ZWN0aW9uLCB0aXBvLCBmb3JjZWQpCiAgICBleGlzdGluZyA9IChiYXRjaC5sb2dfdGV4dG8gb3IgIiIpLnN0cmlwKCkKICAgIGJhdGNoLmxvZ190ZXh0byA9IChoZWFkZXIgKyAoIlxuIiArIGV4aXN0aW5nIGlmIGV4aXN0aW5nIGVsc2UgIiIpKVs6ODAwMF0KICAgIGJhdGNoLnNhdmUodXBkYXRlX2ZpZWxkcz1bImxvZ190ZXh0byJdKQoKCmRlZiBydW5faW1wb3J0KHVzZXIsIHVwbG9hZGVkX2ZpbGU6IFVwbG9hZGVkRmlsZSwgdGlwb19mb3J6YWRvOiBzdHIgfCBOb25lID0gTm9uZSkgLT4gRGlzcGF0Y2hSZXN1bHQ6CiAgICBkZXRlY3Rpb24gPSBkZXRlY3RfZmlsZSh1cGxvYWRlZF9maWxlKQogICAgdXBsb2FkZWRfZmlsZS5zZWVrKDApCiAgICBmb3JjZWQgPSBib29sKHRpcG9fZm9yemFkbykKICAgIHRpcG8gPSB0aXBvX2ZvcnphZG8gb3IgZGV0ZWN0aW9uLnRpcG8KCiAgICBpZiBub3QgZm9yY2VkIGFuZCAoZGV0ZWN0aW9uLmFtYmlndW91cyBvciBub3QgZGV0ZWN0aW9uLmNhbl9hdXRvX2ltcG9ydCBvciB0aXBvID09IFRZUEVfVU5LTk9XTik6CiAgICAgICAgcmV0dXJuIERpc3BhdGNoUmVzdWx0KAogICAgICAgICAgICB0aXBvPXRpcG8gaWYgdGlwbyAhPSBUWVBFX1VOS05PV04gZWxzZSBUWVBFX1VOS05PV04sCiAgICAgICAgICAgIGxhYmVsPVRZUEVfTEFCRUxTLmdldCh0aXBvLCBUWVBFX0xBQkVMU1tUWVBFX1VOS05PV05dKSwKICAgICAgICAgICAgZGV0ZWN0aW9uPWRldGVjdGlvbiwKICAgICAgICAgICAgbWVzc2FnZT0oCiAgICAgICAgICAgICAgICAiQW1iaWfDvGVkYWQgZW4gbGEgZGV0ZWNjacOzbi4gU2VsZWNjaW9uZSBlbCB0aXBvIGRlIGltcG9ydGFjacOzbiAiCiAgICAgICAgICAgICAgICAibWFudWFsbWVudGUgeSB2dWVsdmEgYSBlbnZpYXIgZWwgYXJjaGl2by4iCiAgICAgICAgICAgICAgICBpZiBkZXRlY3Rpb24uYW1iaWd1b3VzIG9yIHRpcG8gPT0gVFlQRV9VTktOT1dOCiAgICAgICAgICAgICAgICBlbHNlICJDb25maWFuemEgaW5zdWZpY2llbnRlIHBhcmEgaW1wb3J0YXIgYXV0b23DoXRpY2FtZW50ZS4gQ29uZmlybWUgZWwgdGlwby4iCiAgICAgICAgICAgICksCiAgICAgICAgICAgIG9rPUZhbHNlLAogICAgICAgICAgICBuZWVkc19tYW51YWw9VHJ1ZSwKICAgICAgICApCgogICAgaWYgdGlwbyA9PSBUWVBFX1VOS05PV04gb3Igbm90IHRpcG86CiAgICAgICAgcmV0dXJuIERpc3BhdGNoUmVzdWx0KAogICAgICAgICAgICB0aXBvPVRZUEVfVU5LTk9XTiwKICAgICAgICAgICAgbGFiZWw9VFlQRV9MQUJFTFNbVFlQRV9VTktOT1dOXSwKICAgICAgICAgICAgZGV0ZWN0aW9uPWRldGVjdGlvbiwKICAgICAgICAgICAgbWVzc2FnZT0iTm8gc2UgcHVkbyBpZGVudGlmaWNhciBlbCB0aXBvLiBFbGlqYSB1bmEgb3BjacOzbiBzdWdlcmlkYS4iLAogICAgICAgICAgICBvaz1GYWxzZSwKICAgICAgICAgICAgbmVlZHNfbWFudWFsPVRydWUsCiAgICAgICAgKQoKICAgIGxhYmVsID0gVFlQRV9MQUJFTFMuZ2V0KHRpcG8sIHRpcG8pCgogICAgaWYgdGlwbyA9PSBUWVBFX0NSTV9DTElFTlRFUzoKICAgICAgICBmcm9tIGNybSBpbXBvcnQgc2VydmljZXMgYXMgY3JtX3NlcnZpY2VzCgogICAgICAgIGJhdGNoID0gY3JtX3NlcnZpY2VzLmltcG9ydF9lbnRpZGFkZXModXNlciwgdXBsb2FkZWRfZmlsZSkKICAgICAgICBfYW5ub3RhdGVfYmF0Y2goYmF0Y2gsIGRldGVjdGlvbiwgdGlwbywgZm9yY2VkKQogICAgICAgIHJldHVybiBEaXNwYXRjaFJlc3VsdCgKICAgICAgICAgICAgdGlwbz10aXBvLAogICAgICAgICAgICBsYWJlbD1sYWJlbCwKICAgICAgICAgICAgZGV0ZWN0aW9uPWRldGVjdGlvbiwKICAgICAgICAgICAgYmF0Y2g9YmF0Y2gsCiAgICAgICAgICAgIG1lc3NhZ2U9ZiJDUk06IHtfYmF0Y2hfc3VtbWFyeShiYXRjaCl9IiwKICAgICAgICAgICAgb2s9YmF0Y2guc3RhdHVzIGluICgiT0siLCAiUEFSVElBTCIpLAogICAgICAgICAgICByZWRpcmVjdF9oaW50PSJjcm06ZW50aWRhZF9saXN0IiwKICAgICAgICAgICAgZm9yY2VkPWZvcmNlZCwKICAgICAgICApCgogICAgaWYgdGlwbyA9PSBUWVBFX1BHT19USUNLRVRTOgogICAgICAgIGZyb20gcGdvIGltcG9ydCBzZXJ2aWNlcyBhcyBwZ29fc2VydmljZXMKICAgICAgICBmcm9tIHBnby5wZXJpb2RvIGltcG9ydCByZWNhbGN1bGF0ZV9wZ29fcGVyaW9kb3MKCiAgICAgICAgYmF0Y2ggPSBwZ29fc2VydmljZXMuaW1wb3J0X3RpY2tldHModXNlciwgdXBsb2FkZWRfZmlsZSkKICAgICAgICByZWNhbGN1bGF0ZV9wZ29fcGVyaW9kb3MoKQogICAgICAgIF9hbm5vdGF0ZV9iYXRjaChiYXRjaCwgZGV0ZWN0aW9uLCB0aXBvLCBmb3JjZWQpCiAgICAgICAgcmV0dXJuIERpc3BhdGNoUmVzdWx0KAogICAgICAgICAgICB0aXBvPXRpcG8sCiAgICAgICAgICAgIGxhYmVsPWxhYmVsLAogICAgICAgICAgICBkZXRlY3Rpb249ZGV0ZWN0aW9uLAogICAgICAgICAgICBiYXRjaD1iYXRjaCwKICAgICAgICAgICAgbWVzc2FnZT1mIlBHTyB0aWNrZXRzOiB7X2JhdGNoX3N1bW1hcnkoYmF0Y2gpfSIsCiAgICAgICAgICAgIG9rPWJhdGNoLnN0YXR1cyBpbiAoIk9LIiwgIlBBUlRJQUwiKSwKICAgICAgICAgICAgcmVkaXJlY3RfaGludD0icGdvOmRhc2hib2FyZCIsCiAgICAgICAgICAgIGZvcmNlZD1mb3JjZWQsCiAgICAgICAgKQoKICAgIGlmIHRpcG8gPT0gVFlQRV9QR09fQ0FUQUxPR086CiAgICAgICAgZnJvbSBwZ28gaW1wb3J0IHNlcnZpY2VzIGFzIHBnb19zZXJ2aWNlcwoKICAgICAgICBiYXRjaCA9IHBnb19zZXJ2aWNlcy5pbXBvcnRfYXJjaGl2b3NfY2F0YWxvZ28odXNlciwgdXBsb2FkZWRfZmlsZSkKICAgICAgICBfYW5ub3RhdGVfYmF0Y2goYmF0Y2gsIGRldGVjdGlvbiwgdGlwbywgZm9yY2VkKQogICAgICAgIHJldHVybiBEaXNwYXRjaFJlc3VsdCgKICAgICAgICAgICAgdGlwbz10aXBvLAogICAgICAgICAgICBsYWJlbD1sYWJlbCwKICAgICAgICAgICAgZGV0ZWN0aW9uPWRldGVjdGlvbiwKICAgICAgICAgICAgYmF0Y2g9YmF0Y2gsCiAgICAgICAgICAgIG1lc3NhZ2U9ZiJDYXTDoWxvZ28gUEdPIHJlZ2lzdHJhZG8gKHtiYXRjaC5maWxhc19sZWlkYXN9IGZpbGFzKS4iLAogICAgICAgICAgICBvaz1UcnVlLAogICAgICAgICAgICByZWRpcmVjdF9oaW50PSJwZ286ZGFzaGJvYXJkIiwKICAgICAgICAgICAgZm9yY2VkPWZvcmNlZCwKICAgICAgICApCgogICAgaWYgdGlwbyA9PSBUWVBFX1JJU0tfTEVBU0lORzoKICAgICAgICBmcm9tIHJpc2sgaW1wb3J0IHNlcnZpY2VzIGFzIHJpc2tfc2VydmljZXMKCiAgICAgICAgYmF0Y2ggPSByaXNrX3NlcnZpY2VzLmltcG9ydF9sZWFzaW5nX2RhdGFiYXNlKHVzZXIsIHVwbG9hZGVkX2ZpbGUpCiAgICAgICAgX2Fubm90YXRlX2JhdGNoKGJhdGNoLCBkZXRlY3Rpb24sIHRpcG8sIGZvcmNlZCkKICAgICAgICByZXR1cm4gRGlzcGF0Y2hSZXN1bHQoCiAgICAgICAgICAgIHRpcG89dGlwbywKICAgICAgICAgICAgbGFiZWw9bGFiZWwsCiAgICAgICAgICAgIGRldGVjdGlvbj1kZXRlY3Rpb24sCiAgICAgICAgICAgIGJhdGNoPWJhdGNoLAogICAgICAgICAgICBtZXNzYWdlPWYiQmFsw7NuIGxlYXNpbmc6IHtfYmF0Y2hfc3VtbWFyeShiYXRjaCl9IiwKICAgICAgICAgICAgb2s9YmF0Y2guc3RhdHVzIGluICgiT0siLCAiUEFSVElBTCIpLAogICAgICAgICAgICByZWRpcmVjdF9oaW50PSJyaXNrOmNvbWFuZG9fYmFsb24iLAogICAgICAgICAgICBmb3JjZWQ9Zm9yY2VkLAogICAgICAgICkKCiAgICBpZiB0aXBvID09IFRZUEVfUklTS19SRU5UQVM6CiAgICAgICAgZnJvbSByaXNrIGltcG9ydCBzZXJ2aWNlcyBhcyByaXNrX3NlcnZpY2VzCgogICAgICAgIGJhdGNoID0gcmlza19zZXJ2aWNlcy5pbXBvcnRfbGVhc2luZ19yZW50YXModXNlciwgdXBsb2FkZWRfZmlsZSkKICAgICAgICBfYW5ub3RhdGVfYmF0Y2goYmF0Y2gsIGRldGVjdGlvbiwgdGlwbywgZm9yY2VkKQogICAgICAgIHJldHVybiBEaXNwYXRjaFJlc3VsdCgKICAgICAgICAgICAgdGlwbz10aXBvLAogICAgICAgICAgICBsYWJlbD1sYWJlbCwKICAgICAgICAgICAgZGV0ZWN0aW9uPWRldGVjdGlvbiwKICAgICAgICAgICAgYmF0Y2g9YmF0Y2gsCiAgICAgICAgICAgIG1lc3NhZ2U9ZiJSZW50YXMgbGVhc2luZzoge19iYXRjaF9zdW1tYXJ5KGJhdGNoKX0iLAogICAgICAgICAgICBvaz1iYXRjaC5zdGF0dXMgaW4gKCJPSyIsICJQQVJUSUFMIiksCiAgICAgICAgICAgIHJlZGlyZWN0X2hpbnQ9InJpc2s6Y29tYW5kb19iYWxvbiIsCiAgICAgICAgICAgIGZvcmNlZD1mb3JjZWQsCiAgICAgICAgKQoKICAgIGlmIHRpcG8gaW4gKFRZUEVfTkVXX0NMSUVOVFMsIFRZUEVfQ1JPU1NfU0FMRSwgVFlQRV9GSU5BTkNJQUwpOgogICAgICAgIGZyb20gaW1wb3J0cy5tb2RlbHMgaW1wb3J0IEZpbGVJbXBvcnRMb2csIEZpbGVVcGxvYWQsIGd1ZXNzX2ZpbGVfZm9ybWF0CgogICAgICAgIHRtcCA9IEZpbGVVcGxvYWQoCiAgICAgICAgICAgIHVwbG9hZGVkX2J5PXVzZXIsCiAgICAgICAgICAgIG9yaWdpbmFsX2ZpbGVuYW1lPXVwbG9hZGVkX2ZpbGUubmFtZSwKICAgICAgICAgICAgZmlsZV9mb3JtYXQ9Z3Vlc3NfZmlsZV9mb3JtYXQodXBsb2FkZWRfZmlsZS5uYW1lKSwKICAgICAgICAgICAgZmlsZV90eXBlX2RldGVjdGVkPXsKICAgICAgICAgICAgICAgIFRZUEVfTkVXX0NMSUVOVFM6IEZpbGVVcGxvYWQuVFlQRV9ORVdfQ0xJRU5UUywKICAgICAgICAgICAgICAgIFRZUEVfQ1JPU1NfU0FMRTogRmlsZVVwbG9hZC5UWVBFX0NST1NTX1NBTEUsCiAgICAgICAgICAgICAgICBUWVBFX0ZJTkFOQ0lBTDogRmlsZVVwbG9hZC5UWVBFX0ZJTkFOQ0lBTCwKICAgICAgICAgICAgfVt0aXBvXSwKICAgICAgICAgICAgc3RhdHVzPUZpbGVVcGxvYWQuU1RBVFVTX1VQTE9BREVELAogICAgICAgICAgICBwYXJzaW5nX25vdGVzPV9kZXRlY3Rpb25fbG9nKGRldGVjdGlvbiwgdGlwbywgZm9yY2VkKSwKICAgICAgICApCiAgICAgICAgdG1wLnN0b3JlZF9maWxlLnNhdmUodXBsb2FkZWRfZmlsZS5uYW1lLCB1cGxvYWRlZF9maWxlLCBzYXZlPVRydWUpCiAgICAgICAgRmlsZUltcG9ydExvZy5vYmplY3RzLmNyZWF0ZSgKICAgICAgICAgICAgZmlsZV91cGxvYWQ9dG1wLAogICAgICAgICAgICBzdGVwX2NvZGU9ImRldGVjdCIsCiAgICAgICAgICAgIGxldmVsPUZpbGVJbXBvcnRMb2cuTEVWRUxfSU5GTywKICAgICAgICAgICAgbWVzc2FnZT1fZGV0ZWN0aW9uX2xvZyhkZXRlY3Rpb24sIHRpcG8sIGZvcmNlZCksCiAgICAgICAgICAgIHBheWxvYWRfanNvbj17CiAgICAgICAgICAgICAgICAidGlwbyI6IHRpcG8sCiAgICAgICAgICAgICAgICAibGF5ZXIiOiBkZXRlY3Rpb24ubGF5ZXIsCiAgICAgICAgICAgICAgICAiY29uZmlkZW5jZSI6IGRldGVjdGlvbi5jb25maWRlbmNlLAogICAgICAgICAgICAgICAgInJlYXNvbnMiOiBkZXRlY3Rpb24ucmVhc29ucywKICAgICAgICAgICAgICAgICJmb3JjZWQiOiBmb3JjZWQsCiAgICAgICAgICAgICAgICAiaW1wb3J0ZXIiOiBJTVBPUlRFUl9MQUJFTFMuZ2V0KHRpcG8pLAogICAgICAgICAgICB9LAogICAgICAgICkKICAgICAgICBwYXRoID0gUGF0aCh0bXAuc3RvcmVkX2ZpbGUucGF0aCkKICAgICAgICB0cnk6CiAgICAgICAgICAgIGlmIHRpcG8gPT0gVFlQRV9ORVdfQ0xJRU5UUzoKICAgICAgICAgICAgICAgIGNhbGxfY29tbWFuZCgiaW1wb3J0X2NsaWVudGVzX251ZXZvcyIsIHBhdGg9c3RyKHBhdGgpLCBmaWxlX3VwbG9hZF9pZD10bXAuaWQpCiAgICAgICAgICAgIGVsaWYgdGlwbyA9PSBUWVBFX0NST1NTX1NBTEU6CiAgICAgICAgICAgICAgICBjYWxsX2NvbW1hbmQoImltcG9ydF92ZW50YV9jcnV6YWRhIiwgcGF0aD1zdHIocGF0aCkpCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICB0bXAuc3RhdHVzID0gRmlsZVVwbG9hZC5TVEFUVVNfVVBMT0FERUQKICAgICAgICAgICAgICAgIHRtcC5wYXJzaW5nX25vdGVzID0gKAogICAgICAgICAgICAgICAgICAgIF9kZXRlY3Rpb25fbG9nKGRldGVjdGlvbiwgdGlwbywgZm9yY2VkKQogICAgICAgICAgICAgICAgICAgICsgIiB8IFN1YmlkbyB2w61hIEFkbWluaXN0cmFjacOzbiDihpIgSW1wb3J0YWNpw7NuLiAiCiAgICAgICAgICAgICAgICAgICAgIlByb2Nlc2FyIGVuIEFkbWluIFBHQyBtZW5zdWFsIChyZXF1aWVyZSBhw7FvL21lcykuIgogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgdG1wLnNhdmUodXBkYXRlX2ZpZWxkcz1bInN0YXR1cyIsICJwYXJzaW5nX25vdGVzIl0pCiAgICAgICAgICAgICAgICByZXR1cm4gRGlzcGF0Y2hSZXN1bHQoCiAgICAgICAgICAgICAgICAgICAgdGlwbz10aXBvLAogICAgICAgICAgICAgICAgICAgIGxhYmVsPWxhYmVsLAogICAgICAgICAgICAgICAgICAgIGRldGVjdGlvbj1kZXRlY3Rpb24sCiAgICAgICAgICAgICAgICAgICAgYmF0Y2g9dG1wLAogICAgICAgICAgICAgICAgICAgIG1lc3NhZ2U9KAogICAgICAgICAgICAgICAgICAgICAgICAiQXJjaGl2byBmaW5hbmNpZXJvIFdDKiBndWFyZGFkby4gIgogICAgICAgICAgICAgICAgICAgICAgICAiQ29tcGzDqXRlbG8gZW4gQWRtaW4gUEdDIOKGkiBwZXLDrW9kbyBtZW5zdWFsIChyZXF1aWVyZSBhw7FvL21lcykuIgogICAgICAgICAgICAgICAgICAgICksCiAgICAgICAgICAgICAgICAgICAgb2s9VHJ1ZSwKICAgICAgICAgICAgICAgICAgICByZWRpcmVjdF9oaW50PSJwZ2M6YWRtaW5fbW9udGhseSIsCiAgICAgICAgICAgICAgICAgICAgZm9yY2VkPWZvcmNlZCwKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgdG1wLnN0YXR1cyA9IEZpbGVVcGxvYWQuU1RBVFVTX1BBUlNFRF9PSwogICAgICAgICAgICB0bXAuc2F2ZSh1cGRhdGVfZmllbGRzPVsic3RhdHVzIl0pCiAgICAgICAgICAgIEZpbGVJbXBvcnRMb2cub2JqZWN0cy5jcmVhdGUoCiAgICAgICAgICAgICAgICBmaWxlX3VwbG9hZD10bXAsCiAgICAgICAgICAgICAgICBzdGVwX2NvZGU9ImRpc3BhdGNoIiwKICAgICAgICAgICAgICAgIGxldmVsPUZpbGVJbXBvcnRMb2cuTEVWRUxfSU5GTywKICAgICAgICAgICAgICAgIG1lc3NhZ2U9ZiJQcm9jZXNhZG8gY29uIHtJTVBPUlRFUl9MQUJFTFMuZ2V0KHRpcG8sIHRpcG8pfSIsCiAgICAgICAgICAgICkKICAgICAgICAgICAgcmV0dXJuIERpc3BhdGNoUmVzdWx0KAogICAgICAgICAgICAgICAgdGlwbz10aXBvLAogICAgICAgICAgICAgICAgbGFiZWw9bGFiZWwsCiAgICAgICAgICAgICAgICBkZXRlY3Rpb249ZGV0ZWN0aW9uLAogICAgICAgICAgICAgICAgYmF0Y2g9dG1wLAogICAgICAgICAgICAgICAgbWVzc2FnZT1mIntsYWJlbH06IHByb2Nlc2FkbyBjb3JyZWN0YW1lbnRlLiIsCiAgICAgICAgICAgICAgICBvaz1UcnVlLAogICAgICAgICAgICAgICAgcmVkaXJlY3RfaGludD0icGdjOmFkbWluX21vbnRobHkiIGlmIHRpcG8gIT0gVFlQRV9ORVdfQ0xJRU5UUyBlbHNlICJwZ2M6Y2xpZW50ZXNfbnVldm9zIiwKICAgICAgICAgICAgICAgIGZvcmNlZD1mb3JjZWQsCiAgICAgICAgICAgICkKICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGV4YzoKICAgICAgICAgICAgdG1wLnN0YXR1cyA9IEZpbGVVcGxvYWQuU1RBVFVTX1BBUlNFRF9FUlJPUgogICAgICAgICAgICB0bXAuZXJyb3Jfc3VtbWFyeSA9IHN0cihleGMpWzo1MDBdCiAgICAgICAgICAgIHRtcC5zYXZlKHVwZGF0ZV9maWVsZHM9WyJzdGF0dXMiLCAiZXJyb3Jfc3VtbWFyeSJdKQogICAgICAgICAgICBGaWxlSW1wb3J0TG9nLm9iamVjdHMuY3JlYXRlKAogICAgICAgICAgICAgICAgZmlsZV91cGxvYWQ9dG1wLAogICAgICAgICAgICAgICAgc3RlcF9jb2RlPSJkaXNwYXRjaCIsCiAgICAgICAgICAgICAgICBsZXZlbD1GaWxlSW1wb3J0TG9nLkxFVkVMX0VSUk9SLAogICAgICAgICAgICAgICAgbWVzc2FnZT1zdHIoZXhjKVs6MTAwMF0sCiAgICAgICAgICAgICkKICAgICAgICAgICAgcmV0dXJuIERpc3BhdGNoUmVzdWx0KAogICAgICAgICAgICAgICAgdGlwbz10aXBvLAogICAgICAgICAgICAgICAgbGFiZWw9bGFiZWwsCiAgICAgICAgICAgICAgICBkZXRlY3Rpb249ZGV0ZWN0aW9uLAogICAgICAgICAgICAgICAgYmF0Y2g9dG1wLAogICAgICAgICAgICAgICAgbWVzc2FnZT1mIkVycm9yIGFsIHByb2Nlc2FyOiB7ZXhjfSIsCiAgICAgICAgICAgICAgICBvaz1GYWxzZSwKICAgICAgICAgICAgICAgIGZvcmNlZD1mb3JjZWQsCiAgICAgICAgICAgICkKCiAgICByZXR1cm4gRGlzcGF0Y2hSZXN1bHQoCiAgICAgICAgdGlwbz10aXBvLAogICAgICAgIGxhYmVsPWxhYmVsLAogICAgICAgIGRldGVjdGlvbj1kZXRlY3Rpb24sCiAgICAgICAgbWVzc2FnZT1mIlRpcG8gJ3t0aXBvfScgYcO6biBubyB0aWVuZSBkZXNwYWNobyBhdXRvbcOhdGljby4iLAogICAgICAgIG9rPUZhbHNlLAogICAgKQoKCmRlZiBydW5faW1wb3J0X3BhdGgodXNlciwgcGF0aDogc3RyLCB0aXBvX2ZvcnphZG86IHN0ciB8IE5vbmUgPSBOb25lKSAtPiBEaXNwYXRjaFJlc3VsdDoKICAgIHAgPSBQYXRoKHBhdGgpCiAgICBmID0gU2ltcGxlVXBsb2FkZWRGaWxlKHAubmFtZSwgcC5yZWFkX2J5dGVzKCkpCiAgICByZXR1cm4gcnVuX2ltcG9ydCh1c2VyLCBmLCB0aXBvX2ZvcnphZG89dGlwb19mb3J6YWRvKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/forms.py
PATH_JSON="imports/forms.py"
FILENAME=forms.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=22
SIZE_BYTES_UTF8=796
CONTENT_SHA256=2c525f106bac4aef4dc88bf5b20b9e598655638515f6bb8846fcda6fe17fa724
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django import forms

from imports.detection import ALL_IMPORTABLE, TYPE_LABELS


class FileUploadForm(forms.Form):
    stored_file = forms.FileField(label="Archivo a importar")


class GeneralImportForm(forms.Form):
    archivo = forms.FileField(
        label="Archivo",
        help_text="CSV, TSV o Excel (.xlsx). Detección por nombre, estructura y contenido.",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )
    tipo_forzado = forms.ChoiceField(
        label="Tipo de importación",
        required=False,
        choices=[("", "— Autodetectar —")] + [(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE],
        help_text="Obligatorio si la detección es ambigua o de baja confianza.",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django import forms
00002|
00003|from imports.detection import ALL_IMPORTABLE, TYPE_LABELS
00004|
00005|
00006|class FileUploadForm(forms.Form):
00007|    stored_file = forms.FileField(label="Archivo a importar")
00008|
00009|
00010|class GeneralImportForm(forms.Form):
00011|    archivo = forms.FileField(
00012|        label="Archivo",
00013|        help_text="CSV, TSV o Excel (.xlsx). Detección por nombre, estructura y contenido.",
00014|        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
00015|    )
00016|    tipo_forzado = forms.ChoiceField(
00017|        label="Tipo de importación",
00018|        required=False,
00019|        choices=[("", "— Autodetectar —")] + [(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE],
00020|        help_text="Obligatorio si la detección es ambigua o de baja confianza.",
00021|        widget=forms.Select(attrs={"class": "form-select"}),
00022|    )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28gaW1wb3J0IGZvcm1zCgpmcm9tIGltcG9ydHMuZGV0ZWN0aW9uIGltcG9ydCBBTExfSU1QT1JUQUJMRSwgVFlQRV9MQUJFTFMKCgpjbGFzcyBGaWxlVXBsb2FkRm9ybShmb3Jtcy5Gb3JtKToKICAgIHN0b3JlZF9maWxlID0gZm9ybXMuRmlsZUZpZWxkKGxhYmVsPSJBcmNoaXZvIGEgaW1wb3J0YXIiKQoKCmNsYXNzIEdlbmVyYWxJbXBvcnRGb3JtKGZvcm1zLkZvcm0pOgogICAgYXJjaGl2byA9IGZvcm1zLkZpbGVGaWVsZCgKICAgICAgICBsYWJlbD0iQXJjaGl2byIsCiAgICAgICAgaGVscF90ZXh0PSJDU1YsIFRTViBvIEV4Y2VsICgueGxzeCkuIERldGVjY2nDs24gcG9yIG5vbWJyZSwgZXN0cnVjdHVyYSB5IGNvbnRlbmlkby4iLAogICAgICAgIHdpZGdldD1mb3Jtcy5DbGVhcmFibGVGaWxlSW5wdXQoYXR0cnM9eyJjbGFzcyI6ICJmb3JtLWNvbnRyb2wifSksCiAgICApCiAgICB0aXBvX2ZvcnphZG8gPSBmb3Jtcy5DaG9pY2VGaWVsZCgKICAgICAgICBsYWJlbD0iVGlwbyBkZSBpbXBvcnRhY2nDs24iLAogICAgICAgIHJlcXVpcmVkPUZhbHNlLAogICAgICAgIGNob2ljZXM9WygiIiwgIuKAlCBBdXRvZGV0ZWN0YXIg4oCUIildICsgWyh0LCBUWVBFX0xBQkVMU1t0XSkgZm9yIHQgaW4gQUxMX0lNUE9SVEFCTEVdLAogICAgICAgIGhlbHBfdGV4dD0iT2JsaWdhdG9yaW8gc2kgbGEgZGV0ZWNjacOzbiBlcyBhbWJpZ3VhIG8gZGUgYmFqYSBjb25maWFuemEuIiwKICAgICAgICB3aWRnZXQ9Zm9ybXMuU2VsZWN0KGF0dHJzPXsiY2xhc3MiOiAiZm9ybS1zZWxlY3QifSksCiAgICApCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/management/__init__.py
PATH_JSON="imports/management/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/management/commands/__init__.py
PATH_JSON="imports/management/commands/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/management/commands/import_clientes_nuevos.py
PATH_JSON="imports/management/commands/import_clientes_nuevos.py"
FILENAME=import_clientes_nuevos.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=326
SIZE_BYTES_UTF8=11690
CONTENT_SHA256=31a28599ef22bf5f8c5a1b275c6d1ce71188accaf50adc25875caf0dddbf0192
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
# File: import_clientes_nuevos.py

import csv

from core.models import UNE, UNEAlias, MetricDefinition, Currency
from core.services.une_resolve import resolve_une_from_text
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from imports.models import FileUpload, NewClientImportHeader, NewClientImportRow
from pathlib import Path
from pgc.models import PGCPlan, MonthlyTarget, MonthlyMetricResult


def _resolve_file_upload(path: Path, file_upload_id: int | None) -> FileUpload | None:
    if file_upload_id:
        upload = FileUpload.objects.filter(pk=file_upload_id).first()
        if not upload:
            raise CommandError(f"FileUpload id={file_upload_id} no encontrado.")
        return upload

    path = path.resolve()
    candidates = FileUpload.objects.filter(
        file_type_detected=FileUpload.TYPE_NEW_CLIENTS,
    ).order_by("-id")[:80]
    for upload in candidates:
        try:
            if upload.stored_file and Path(upload.stored_file.path).resolve() == path:
                return upload
        except Exception:
            continue

    by_name = (
        FileUpload.objects.filter(
            file_type_detected=FileUpload.TYPE_NEW_CLIENTS,
            original_filename=path.name,
        )
        .order_by("-id")
        .first()
    )
    return by_name


def _ensure_header(year: int, month: int, upload: FileUpload | None) -> NewClientImportHeader:
    header = NewClientImportHeader.objects.filter(year=year, month=month).first()
    if header:
        return header

    if not upload:
        raise CommandError(
            f"No existe NewClientImportHeader para {year}-{month:02d} y no hay "
            "FileUpload de origen para crearlo. Sube el archivo vía Administración."
        )

    header, _ = NewClientImportHeader.objects.get_or_create(
        year=year,
        month=month,
        defaults={"file_upload": upload},
    )
    return header


class Command(BaseCommand):
    help = (
        "Importa ClientesNuevos (csv/tsv). Cada fila se guarda en su AnioMes; "
        "un solo archivo puede contener varios meses."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            required=True,
            help="Ruta al archivo ClientesNuevos (csv/tsv)",
        )
        parser.add_argument(
            "--file-upload-id",
            type=int,
            default=None,
            help="Id de FileUpload origen (opcional; se infiere por ruta si falta)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.exists():
            raise CommandError(f"Archivo no encontrado: {path}")

        self.stdout.write(self.style.WARNING(f"Leyendo {path} ..."))

        imported_file_name = path.name
        source_upload = _resolve_file_upload(path, options.get("file_upload_id"))

        metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_CLIENTES_NUEVOS)
        currencies = {c.code.upper(): c for c in Currency.objects.all()}
        headers_cache: dict[tuple[int, int], NewClientImportHeader] = {}

        aliases = {
            a.raw_value.strip().upper(): a.une
            for a in UNEAlias.objects.select_related("une").filter(is_active=True)
        }
        unes_by_code = {u.code: u for u in UNE.objects.all()}

        # clave: (year, month, une_id) -> conteo clientes nuevos
        counts: dict[tuple[int, int, int], int] = {}
        rows_written = 0
        rows_skipped = 0
        months_touched: set[tuple[int, int]] = set()

        with path.open("r", encoding="utf-8-sig") as f:
            sample = f.read(4096)
            f.seek(0)
            dialect = csv.Sniffer().sniff(sample, delimiters=[",", "\t", ";"])
            reader = csv.DictReader(f, dialect=dialect)

            for line_no, row in enumerate(reader, start=2):
                anio_mes = row.get("AnioMes") or row.get("aniomes")
                contratos_previos = row.get("ContratosPrevios") or row.get("contratosprevios")
                une_raw = row.get("UNE") or row.get("une")

                if not anio_mes or not une_raw:
                    rows_skipped += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Fila {line_no}: omitida (falta AnioMes o UNE)."
                        )
                    )
                    continue

                try:
                    year_str, month_str = anio_mes.replace("-", "/").split("/")
                    year = int(year_str)
                    month = int(month_str)
                except Exception:
                    rows_skipped += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Fila {line_no}: AnioMes no válido ({anio_mes!r})."
                        )
                    )
                    continue

                if month < 1 or month > 12:
                    rows_skipped += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Fila {line_no}: mes inválido ({month})."
                        )
                    )
                    continue

                try:
                    prev = int(contratos_previos) if contratos_previos not in (None, "") else 0
                except ValueError:
                    prev = 0

                counts_as_new = prev == 0

                une = resolve_une_from_text(une_raw, aliases, unes_by_code)
                if not une:
                    rows_skipped += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Fila {line_no}: UNE no reconocida ({une_raw!r})."
                        )
                    )
                    continue

                header_key = (year, month)
                header = headers_cache.get(header_key)
                if header is None:
                    header = _ensure_header(year, month, source_upload)
                    headers_cache[header_key] = header
                months_touched.add(header_key)

                client_name = (
                    row.get("Cliente")
                    or row.get("CLIENTE")
                    or row.get("cliente")
                    or ""
                ).strip()

                nit = (
                    row.get("NIT")
                    or row.get("Nit")
                    or row.get("nit")
                    or ""
                ).strip()

                operation_code = (
                    row.get("Operacion")
                    or row.get("Operación")
                    or row.get("OPERACION")
                    or row.get("operation_code")
                    or ""
                ).strip()

                currency_code = (
                    row.get("Moneda")
                    or row.get("MONEDA")
                    or row.get("moneda")
                    or ""
                ).strip().upper()

                amount_raw = (
                    row.get("Monto")
                    or row.get("MONTO")
                    or row.get("monto")
                    or ""
                ).strip()

                amount = None
                if amount_raw:
                    try:
                        # PGC expresa montos de ingresos en miles de US$;
                        # el archivo trae unidades → guardar ya dividido entre 1000.
                        amount = Decimal(str(amount_raw).replace(",", "")) / Decimal(
                            "1000"
                        )
                    except Exception:
                        amount = None

                currency = currencies.get(currency_code)

                NewClientImportRow.objects.create(
                    header=header,
                    une=une,
                    year=year,
                    month=month,
                    client_name=client_name,
                    nit=nit,
                    operation_code=operation_code,
                    previous_contracts=prev,
                    counts_as_new=counts_as_new,
                    currency=currency,
                    amount=amount,
                    source_row_number=line_no,
                    raw_une_value=une_raw,
                    observations="",
                )
                rows_written += 1

                if counts_as_new:
                    key = (year, month, une.id)
                    counts[key] = counts.get(key, 0) + 1

        if months_touched:
            months_label = ", ".join(
                f"{y}-{m:02d}" for y, m in sorted(months_touched)
            )
            self.stdout.write(
                f"Meses del archivo: {months_label}. "
                f"Filas guardadas: {rows_written}. Omitidas: {rows_skipped}."
            )

        years_in_file = sorted({year for (year, _, _), _ in counts.items()})
        if not years_in_file:
            # Puede haber filas guardadas sin counts_as_new; no es error duro.
            if rows_written:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Import completado: {rows_written} fila(s) almacenada(s); "
                        "ninguna contó como cliente nuevo (ContratosPrevios≠0)."
                    )
                )
                return
            self.stdout.write(
                self.style.WARNING("No se encontraron filas importables en el archivo.")
            )
            return
        if len(years_in_file) > 1:
            raise CommandError(
                f"El archivo contiene múltiples años {years_in_file}. "
                "Por ahora se espera un año por archivo."
            )
        year_for_plan = years_in_file[0]
        try:
            plan = PGCPlan.objects.get(year=year_for_plan)
        except PGCPlan.DoesNotExist:
            raise CommandError(f"No existe PGCPlan para año {year_for_plan}.")

        total_updated = 0
        for (year, month, une_id), count in counts.items():
            une = UNE.objects.get(id=une_id)
            try:
                target = MonthlyTarget.objects.get(
                    plan=plan,
                    une=une,
                    metric=metric,
                    year=year,
                    month=month,
                )
            except MonthlyTarget.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Sin MonthlyTarget para {une.code} {year}-{month:02d}"
                    )
                )
                continue

            mmr, _ = MonthlyMetricResult.objects.get_or_create(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
                defaults={"target_value": target.target_value},
            )
            mmr.target_value = target.target_value
            mmr.measured_value = Decimal(str(count))
            mmr.calculation_note = (
                f"{count} clientes nuevos contados desde {imported_file_name}"
            )
            mmr.save()
            total_updated += 1
            self.stdout.write(
                f"Actualizado CLIENTES_NUEVOS {une.code} {year}-{month:02d}: {count}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Import CLIENTES_NUEVOS completado. "
                f"{rows_written} fila(s), {total_updated} métrica(s), "
                f"{len(months_touched)} mes(es)."
            )
        )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|# File: import_clientes_nuevos.py
00002|
00003|import csv
00004|
00005|from core.models import UNE, UNEAlias, MetricDefinition, Currency
00006|from core.services.une_resolve import resolve_une_from_text
00007|from decimal import Decimal
00008|from django.core.management.base import BaseCommand, CommandError
00009|from django.db import transaction
00010|from imports.models import FileUpload, NewClientImportHeader, NewClientImportRow
00011|from pathlib import Path
00012|from pgc.models import PGCPlan, MonthlyTarget, MonthlyMetricResult
00013|
00014|
00015|def _resolve_file_upload(path: Path, file_upload_id: int | None) -> FileUpload | None:
00016|    if file_upload_id:
00017|        upload = FileUpload.objects.filter(pk=file_upload_id).first()
00018|        if not upload:
00019|            raise CommandError(f"FileUpload id={file_upload_id} no encontrado.")
00020|        return upload
00021|
00022|    path = path.resolve()
00023|    candidates = FileUpload.objects.filter(
00024|        file_type_detected=FileUpload.TYPE_NEW_CLIENTS,
00025|    ).order_by("-id")[:80]
00026|    for upload in candidates:
00027|        try:
00028|            if upload.stored_file and Path(upload.stored_file.path).resolve() == path:
00029|                return upload
00030|        except Exception:
00031|            continue
00032|
00033|    by_name = (
00034|        FileUpload.objects.filter(
00035|            file_type_detected=FileUpload.TYPE_NEW_CLIENTS,
00036|            original_filename=path.name,
00037|        )
00038|        .order_by("-id")
00039|        .first()
00040|    )
00041|    return by_name
00042|
00043|
00044|def _ensure_header(year: int, month: int, upload: FileUpload | None) -> NewClientImportHeader:
00045|    header = NewClientImportHeader.objects.filter(year=year, month=month).first()
00046|    if header:
00047|        return header
00048|
00049|    if not upload:
00050|        raise CommandError(
00051|            f"No existe NewClientImportHeader para {year}-{month:02d} y no hay "
00052|            "FileUpload de origen para crearlo. Sube el archivo vía Administración."
00053|        )
00054|
00055|    header, _ = NewClientImportHeader.objects.get_or_create(
00056|        year=year,
00057|        month=month,
00058|        defaults={"file_upload": upload},
00059|    )
00060|    return header
00061|
00062|
00063|class Command(BaseCommand):
00064|    help = (
00065|        "Importa ClientesNuevos (csv/tsv). Cada fila se guarda en su AnioMes; "
00066|        "un solo archivo puede contener varios meses."
00067|    )
00068|
00069|    def add_arguments(self, parser):
00070|        parser.add_argument(
00071|            "--path",
00072|            type=str,
00073|            required=True,
00074|            help="Ruta al archivo ClientesNuevos (csv/tsv)",
00075|        )
00076|        parser.add_argument(
00077|            "--file-upload-id",
00078|            type=int,
00079|            default=None,
00080|            help="Id de FileUpload origen (opcional; se infiere por ruta si falta)",
00081|        )
00082|
00083|    @transaction.atomic
00084|    def handle(self, *args, **options):
00085|        path = Path(options["path"])
00086|        if not path.exists():
00087|            raise CommandError(f"Archivo no encontrado: {path}")
00088|
00089|        self.stdout.write(self.style.WARNING(f"Leyendo {path} ..."))
00090|
00091|        imported_file_name = path.name
00092|        source_upload = _resolve_file_upload(path, options.get("file_upload_id"))
00093|
00094|        metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_CLIENTES_NUEVOS)
00095|        currencies = {c.code.upper(): c for c in Currency.objects.all()}
00096|        headers_cache: dict[tuple[int, int], NewClientImportHeader] = {}
00097|
00098|        aliases = {
00099|            a.raw_value.strip().upper(): a.une
00100|            for a in UNEAlias.objects.select_related("une").filter(is_active=True)
00101|        }
00102|        unes_by_code = {u.code: u for u in UNE.objects.all()}
00103|
00104|        # clave: (year, month, une_id) -> conteo clientes nuevos
00105|        counts: dict[tuple[int, int, int], int] = {}
00106|        rows_written = 0
00107|        rows_skipped = 0
00108|        months_touched: set[tuple[int, int]] = set()
00109|
00110|        with path.open("r", encoding="utf-8-sig") as f:
00111|            sample = f.read(4096)
00112|            f.seek(0)
00113|            dialect = csv.Sniffer().sniff(sample, delimiters=[",", "\t", ";"])
00114|            reader = csv.DictReader(f, dialect=dialect)
00115|
00116|            for line_no, row in enumerate(reader, start=2):
00117|                anio_mes = row.get("AnioMes") or row.get("aniomes")
00118|                contratos_previos = row.get("ContratosPrevios") or row.get("contratosprevios")
00119|                une_raw = row.get("UNE") or row.get("une")
00120|
00121|                if not anio_mes or not une_raw:
00122|                    rows_skipped += 1
00123|                    self.stdout.write(
00124|                        self.style.WARNING(
00125|                            f"Fila {line_no}: omitida (falta AnioMes o UNE)."
00126|                        )
00127|                    )
00128|                    continue
00129|
00130|                try:
00131|                    year_str, month_str = anio_mes.replace("-", "/").split("/")
00132|                    year = int(year_str)
00133|                    month = int(month_str)
00134|                except Exception:
00135|                    rows_skipped += 1
00136|                    self.stdout.write(
00137|                        self.style.WARNING(
00138|                            f"Fila {line_no}: AnioMes no válido ({anio_mes!r})."
00139|                        )
00140|                    )
00141|                    continue
00142|
00143|                if month < 1 or month > 12:
00144|                    rows_skipped += 1
00145|                    self.stdout.write(
00146|                        self.style.WARNING(
00147|                            f"Fila {line_no}: mes inválido ({month})."
00148|                        )
00149|                    )
00150|                    continue
00151|
00152|                try:
00153|                    prev = int(contratos_previos) if contratos_previos not in (None, "") else 0
00154|                except ValueError:
00155|                    prev = 0
00156|
00157|                counts_as_new = prev == 0
00158|
00159|                une = resolve_une_from_text(une_raw, aliases, unes_by_code)
00160|                if not une:
00161|                    rows_skipped += 1
00162|                    self.stdout.write(
00163|                        self.style.WARNING(
00164|                            f"Fila {line_no}: UNE no reconocida ({une_raw!r})."
00165|                        )
00166|                    )
00167|                    continue
00168|
00169|                header_key = (year, month)
00170|                header = headers_cache.get(header_key)
00171|                if header is None:
00172|                    header = _ensure_header(year, month, source_upload)
00173|                    headers_cache[header_key] = header
00174|                months_touched.add(header_key)
00175|
00176|                client_name = (
00177|                    row.get("Cliente")
00178|                    or row.get("CLIENTE")
00179|                    or row.get("cliente")
00180|                    or ""
00181|                ).strip()
00182|
00183|                nit = (
00184|                    row.get("NIT")
00185|                    or row.get("Nit")
00186|                    or row.get("nit")
00187|                    or ""
00188|                ).strip()
00189|
00190|                operation_code = (
00191|                    row.get("Operacion")
00192|                    or row.get("Operación")
00193|                    or row.get("OPERACION")
00194|                    or row.get("operation_code")
00195|                    or ""
00196|                ).strip()
00197|
00198|                currency_code = (
00199|                    row.get("Moneda")
00200|                    or row.get("MONEDA")
00201|                    or row.get("moneda")
00202|                    or ""
00203|                ).strip().upper()
00204|
00205|                amount_raw = (
00206|                    row.get("Monto")
00207|                    or row.get("MONTO")
00208|                    or row.get("monto")
00209|                    or ""
00210|                ).strip()
00211|
00212|                amount = None
00213|                if amount_raw:
00214|                    try:
00215|                        # PGC expresa montos de ingresos en miles de US$;
00216|                        # el archivo trae unidades → guardar ya dividido entre 1000.
00217|                        amount = Decimal(str(amount_raw).replace(",", "")) / Decimal(
00218|                            "1000"
00219|                        )
00220|                    except Exception:
00221|                        amount = None
00222|
00223|                currency = currencies.get(currency_code)
00224|
00225|                NewClientImportRow.objects.create(
00226|                    header=header,
00227|                    une=une,
00228|                    year=year,
00229|                    month=month,
00230|                    client_name=client_name,
00231|                    nit=nit,
00232|                    operation_code=operation_code,
00233|                    previous_contracts=prev,
00234|                    counts_as_new=counts_as_new,
00235|                    currency=currency,
00236|                    amount=amount,
00237|                    source_row_number=line_no,
00238|                    raw_une_value=une_raw,
00239|                    observations="",
00240|                )
00241|                rows_written += 1
00242|
00243|                if counts_as_new:
00244|                    key = (year, month, une.id)
00245|                    counts[key] = counts.get(key, 0) + 1
00246|
00247|        if months_touched:
00248|            months_label = ", ".join(
00249|                f"{y}-{m:02d}" for y, m in sorted(months_touched)
00250|            )
00251|            self.stdout.write(
00252|                f"Meses del archivo: {months_label}. "
00253|                f"Filas guardadas: {rows_written}. Omitidas: {rows_skipped}."
00254|            )
00255|
00256|        years_in_file = sorted({year for (year, _, _), _ in counts.items()})
00257|        if not years_in_file:
00258|            # Puede haber filas guardadas sin counts_as_new; no es error duro.
00259|            if rows_written:
00260|                self.stdout.write(
00261|                    self.style.SUCCESS(
00262|                        f"Import completado: {rows_written} fila(s) almacenada(s); "
00263|                        "ninguna contó como cliente nuevo (ContratosPrevios≠0)."
00264|                    )
00265|                )
00266|                return
00267|            self.stdout.write(
00268|                self.style.WARNING("No se encontraron filas importables en el archivo.")
00269|            )
00270|            return
00271|        if len(years_in_file) > 1:
00272|            raise CommandError(
00273|                f"El archivo contiene múltiples años {years_in_file}. "
00274|                "Por ahora se espera un año por archivo."
00275|            )
00276|        year_for_plan = years_in_file[0]
00277|        try:
00278|            plan = PGCPlan.objects.get(year=year_for_plan)
00279|        except PGCPlan.DoesNotExist:
00280|            raise CommandError(f"No existe PGCPlan para año {year_for_plan}.")
00281|
00282|        total_updated = 0
00283|        for (year, month, une_id), count in counts.items():
00284|            une = UNE.objects.get(id=une_id)
00285|            try:
00286|                target = MonthlyTarget.objects.get(
00287|                    plan=plan,
00288|                    une=une,
00289|                    metric=metric,
00290|                    year=year,
00291|                    month=month,
00292|                )
00293|            except MonthlyTarget.DoesNotExist:
00294|                self.stdout.write(
00295|                    self.style.WARNING(
00296|                        f"Sin MonthlyTarget para {une.code} {year}-{month:02d}"
00297|                    )
00298|                )
00299|                continue
00300|
00301|            mmr, _ = MonthlyMetricResult.objects.get_or_create(
00302|                plan=plan,
00303|                une=une,
00304|                metric=metric,
00305|                year=year,
00306|                month=month,
00307|                defaults={"target_value": target.target_value},
00308|            )
00309|            mmr.target_value = target.target_value
00310|            mmr.measured_value = Decimal(str(count))
00311|            mmr.calculation_note = (
00312|                f"{count} clientes nuevos contados desde {imported_file_name}"
00313|            )
00314|            mmr.save()
00315|            total_updated += 1
00316|            self.stdout.write(
00317|                f"Actualizado CLIENTES_NUEVOS {une.code} {year}-{month:02d}: {count}"
00318|            )
00319|
00320|        self.stdout.write(
00321|            self.style.SUCCESS(
00322|                f"Import CLIENTES_NUEVOS completado. "
00323|                f"{rows_written} fila(s), {total_updated} métrica(s), "
00324|                f"{len(months_touched)} mes(es)."
00325|            )
00326|        )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IyBGaWxlOiBpbXBvcnRfY2xpZW50ZXNfbnVldm9zLnB5CgppbXBvcnQgY3N2Cgpmcm9tIGNvcmUubW9kZWxzIGltcG9ydCBVTkUsIFVORUFsaWFzLCBNZXRyaWNEZWZpbml0aW9uLCBDdXJyZW5jeQpmcm9tIGNvcmUuc2VydmljZXMudW5lX3Jlc29sdmUgaW1wb3J0IHJlc29sdmVfdW5lX2Zyb21fdGV4dApmcm9tIGRlY2ltYWwgaW1wb3J0IERlY2ltYWwKZnJvbSBkamFuZ28uY29yZS5tYW5hZ2VtZW50LmJhc2UgaW1wb3J0IEJhc2VDb21tYW5kLCBDb21tYW5kRXJyb3IKZnJvbSBkamFuZ28uZGIgaW1wb3J0IHRyYW5zYWN0aW9uCmZyb20gaW1wb3J0cy5tb2RlbHMgaW1wb3J0IEZpbGVVcGxvYWQsIE5ld0NsaWVudEltcG9ydEhlYWRlciwgTmV3Q2xpZW50SW1wb3J0Um93CmZyb20gcGF0aGxpYiBpbXBvcnQgUGF0aApmcm9tIHBnYy5tb2RlbHMgaW1wb3J0IFBHQ1BsYW4sIE1vbnRobHlUYXJnZXQsIE1vbnRobHlNZXRyaWNSZXN1bHQKCgpkZWYgX3Jlc29sdmVfZmlsZV91cGxvYWQocGF0aDogUGF0aCwgZmlsZV91cGxvYWRfaWQ6IGludCB8IE5vbmUpIC0+IEZpbGVVcGxvYWQgfCBOb25lOgogICAgaWYgZmlsZV91cGxvYWRfaWQ6CiAgICAgICAgdXBsb2FkID0gRmlsZVVwbG9hZC5vYmplY3RzLmZpbHRlcihwaz1maWxlX3VwbG9hZF9pZCkuZmlyc3QoKQogICAgICAgIGlmIG5vdCB1cGxvYWQ6CiAgICAgICAgICAgIHJhaXNlIENvbW1hbmRFcnJvcihmIkZpbGVVcGxvYWQgaWQ9e2ZpbGVfdXBsb2FkX2lkfSBubyBlbmNvbnRyYWRvLiIpCiAgICAgICAgcmV0dXJuIHVwbG9hZAoKICAgIHBhdGggPSBwYXRoLnJlc29sdmUoKQogICAgY2FuZGlkYXRlcyA9IEZpbGVVcGxvYWQub2JqZWN0cy5maWx0ZXIoCiAgICAgICAgZmlsZV90eXBlX2RldGVjdGVkPUZpbGVVcGxvYWQuVFlQRV9ORVdfQ0xJRU5UUywKICAgICkub3JkZXJfYnkoIi1pZCIpWzo4MF0KICAgIGZvciB1cGxvYWQgaW4gY2FuZGlkYXRlczoKICAgICAgICB0cnk6CiAgICAgICAgICAgIGlmIHVwbG9hZC5zdG9yZWRfZmlsZSBhbmQgUGF0aCh1cGxvYWQuc3RvcmVkX2ZpbGUucGF0aCkucmVzb2x2ZSgpID09IHBhdGg6CiAgICAgICAgICAgICAgICByZXR1cm4gdXBsb2FkCiAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICAgICAgY29udGludWUKCiAgICBieV9uYW1lID0gKAogICAgICAgIEZpbGVVcGxvYWQub2JqZWN0cy5maWx0ZXIoCiAgICAgICAgICAgIGZpbGVfdHlwZV9kZXRlY3RlZD1GaWxlVXBsb2FkLlRZUEVfTkVXX0NMSUVOVFMsCiAgICAgICAgICAgIG9yaWdpbmFsX2ZpbGVuYW1lPXBhdGgubmFtZSwKICAgICAgICApCiAgICAgICAgLm9yZGVyX2J5KCItaWQiKQogICAgICAgIC5maXJzdCgpCiAgICApCiAgICByZXR1cm4gYnlfbmFtZQoKCmRlZiBfZW5zdXJlX2hlYWRlcih5ZWFyOiBpbnQsIG1vbnRoOiBpbnQsIHVwbG9hZDogRmlsZVVwbG9hZCB8IE5vbmUpIC0+IE5ld0NsaWVudEltcG9ydEhlYWRlcjoKICAgIGhlYWRlciA9IE5ld0NsaWVudEltcG9ydEhlYWRlci5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKS5maXJzdCgpCiAgICBpZiBoZWFkZXI6CiAgICAgICAgcmV0dXJuIGhlYWRlcgoKICAgIGlmIG5vdCB1cGxvYWQ6CiAgICAgICAgcmFpc2UgQ29tbWFuZEVycm9yKAogICAgICAgICAgICBmIk5vIGV4aXN0ZSBOZXdDbGllbnRJbXBvcnRIZWFkZXIgcGFyYSB7eWVhcn0te21vbnRoOjAyZH0geSBubyBoYXkgIgogICAgICAgICAgICAiRmlsZVVwbG9hZCBkZSBvcmlnZW4gcGFyYSBjcmVhcmxvLiBTdWJlIGVsIGFyY2hpdm8gdsOtYSBBZG1pbmlzdHJhY2nDs24uIgogICAgICAgICkKCiAgICBoZWFkZXIsIF8gPSBOZXdDbGllbnRJbXBvcnRIZWFkZXIub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgIHllYXI9eWVhciwKICAgICAgICBtb250aD1tb250aCwKICAgICAgICBkZWZhdWx0cz17ImZpbGVfdXBsb2FkIjogdXBsb2FkfSwKICAgICkKICAgIHJldHVybiBoZWFkZXIKCgpjbGFzcyBDb21tYW5kKEJhc2VDb21tYW5kKToKICAgIGhlbHAgPSAoCiAgICAgICAgIkltcG9ydGEgQ2xpZW50ZXNOdWV2b3MgKGNzdi90c3YpLiBDYWRhIGZpbGEgc2UgZ3VhcmRhIGVuIHN1IEFuaW9NZXM7ICIKICAgICAgICAidW4gc29sbyBhcmNoaXZvIHB1ZWRlIGNvbnRlbmVyIHZhcmlvcyBtZXNlcy4iCiAgICApCgogICAgZGVmIGFkZF9hcmd1bWVudHMoc2VsZiwgcGFyc2VyKToKICAgICAgICBwYXJzZXIuYWRkX2FyZ3VtZW50KAogICAgICAgICAgICAiLS1wYXRoIiwKICAgICAgICAgICAgdHlwZT1zdHIsCiAgICAgICAgICAgIHJlcXVpcmVkPVRydWUsCiAgICAgICAgICAgIGhlbHA9IlJ1dGEgYWwgYXJjaGl2byBDbGllbnRlc051ZXZvcyAoY3N2L3RzdikiLAogICAgICAgICkKICAgICAgICBwYXJzZXIuYWRkX2FyZ3VtZW50KAogICAgICAgICAgICAiLS1maWxlLXVwbG9hZC1pZCIsCiAgICAgICAgICAgIHR5cGU9aW50LAogICAgICAgICAgICBkZWZhdWx0PU5vbmUsCiAgICAgICAgICAgIGhlbHA9IklkIGRlIEZpbGVVcGxvYWQgb3JpZ2VuIChvcGNpb25hbDsgc2UgaW5maWVyZSBwb3IgcnV0YSBzaSBmYWx0YSkiLAogICAgICAgICkKCiAgICBAdHJhbnNhY3Rpb24uYXRvbWljCiAgICBkZWYgaGFuZGxlKHNlbGYsICphcmdzLCAqKm9wdGlvbnMpOgogICAgICAgIHBhdGggPSBQYXRoKG9wdGlvbnNbInBhdGgiXSkKICAgICAgICBpZiBub3QgcGF0aC5leGlzdHMoKToKICAgICAgICAgICAgcmFpc2UgQ29tbWFuZEVycm9yKGYiQXJjaGl2byBubyBlbmNvbnRyYWRvOiB7cGF0aH0iKQoKICAgICAgICBzZWxmLnN0ZG91dC53cml0ZShzZWxmLnN0eWxlLldBUk5JTkcoZiJMZXllbmRvIHtwYXRofSAuLi4iKSkKCiAgICAgICAgaW1wb3J0ZWRfZmlsZV9uYW1lID0gcGF0aC5uYW1lCiAgICAgICAgc291cmNlX3VwbG9hZCA9IF9yZXNvbHZlX2ZpbGVfdXBsb2FkKHBhdGgsIG9wdGlvbnMuZ2V0KCJmaWxlX3VwbG9hZF9pZCIpKQoKICAgICAgICBtZXRyaWMgPSBNZXRyaWNEZWZpbml0aW9uLm9iamVjdHMuZ2V0KGNvZGU9TWV0cmljRGVmaW5pdGlvbi5DT0RFX0NMSUVOVEVTX05VRVZPUykKICAgICAgICBjdXJyZW5jaWVzID0ge2MuY29kZS51cHBlcigpOiBjIGZvciBjIGluIEN1cnJlbmN5Lm9iamVjdHMuYWxsKCl9CiAgICAgICAgaGVhZGVyc19jYWNoZTogZGljdFt0dXBsZVtpbnQsIGludF0sIE5ld0NsaWVudEltcG9ydEhlYWRlcl0gPSB7fQoKICAgICAgICBhbGlhc2VzID0gewogICAgICAgICAgICBhLnJhd192YWx1ZS5zdHJpcCgpLnVwcGVyKCk6IGEudW5lCiAgICAgICAgICAgIGZvciBhIGluIFVORUFsaWFzLm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoInVuZSIpLmZpbHRlcihpc19hY3RpdmU9VHJ1ZSkKICAgICAgICB9CiAgICAgICAgdW5lc19ieV9jb2RlID0ge3UuY29kZTogdSBmb3IgdSBpbiBVTkUub2JqZWN0cy5hbGwoKX0KCiAgICAgICAgIyBjbGF2ZTogKHllYXIsIG1vbnRoLCB1bmVfaWQpIC0+IGNvbnRlbyBjbGllbnRlcyBudWV2b3MKICAgICAgICBjb3VudHM6IGRpY3RbdHVwbGVbaW50LCBpbnQsIGludF0sIGludF0gPSB7fQogICAgICAgIHJvd3Nfd3JpdHRlbiA9IDAKICAgICAgICByb3dzX3NraXBwZWQgPSAwCiAgICAgICAgbW9udGhzX3RvdWNoZWQ6IHNldFt0dXBsZVtpbnQsIGludF1dID0gc2V0KCkKCiAgICAgICAgd2l0aCBwYXRoLm9wZW4oInIiLCBlbmNvZGluZz0idXRmLTgtc2lnIikgYXMgZjoKICAgICAgICAgICAgc2FtcGxlID0gZi5yZWFkKDQwOTYpCiAgICAgICAgICAgIGYuc2VlaygwKQogICAgICAgICAgICBkaWFsZWN0ID0gY3N2LlNuaWZmZXIoKS5zbmlmZihzYW1wbGUsIGRlbGltaXRlcnM9WyIsIiwgIlx0IiwgIjsiXSkKICAgICAgICAgICAgcmVhZGVyID0gY3N2LkRpY3RSZWFkZXIoZiwgZGlhbGVjdD1kaWFsZWN0KQoKICAgICAgICAgICAgZm9yIGxpbmVfbm8sIHJvdyBpbiBlbnVtZXJhdGUocmVhZGVyLCBzdGFydD0yKToKICAgICAgICAgICAgICAgIGFuaW9fbWVzID0gcm93LmdldCgiQW5pb01lcyIpIG9yIHJvdy5nZXQoImFuaW9tZXMiKQogICAgICAgICAgICAgICAgY29udHJhdG9zX3ByZXZpb3MgPSByb3cuZ2V0KCJDb250cmF0b3NQcmV2aW9zIikgb3Igcm93LmdldCgiY29udHJhdG9zcHJldmlvcyIpCiAgICAgICAgICAgICAgICB1bmVfcmF3ID0gcm93LmdldCgiVU5FIikgb3Igcm93LmdldCgidW5lIikKCiAgICAgICAgICAgICAgICBpZiBub3QgYW5pb19tZXMgb3Igbm90IHVuZV9yYXc6CiAgICAgICAgICAgICAgICAgICAgcm93c19za2lwcGVkICs9IDEKICAgICAgICAgICAgICAgICAgICBzZWxmLnN0ZG91dC53cml0ZSgKICAgICAgICAgICAgICAgICAgICAgICAgc2VsZi5zdHlsZS5XQVJOSU5HKAogICAgICAgICAgICAgICAgICAgICAgICAgICAgZiJGaWxhIHtsaW5lX25vfTogb21pdGlkYSAoZmFsdGEgQW5pb01lcyBvIFVORSkuIgogICAgICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgICAgIGNvbnRpbnVlCgogICAgICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgICAgIHllYXJfc3RyLCBtb250aF9zdHIgPSBhbmlvX21lcy5yZXBsYWNlKCItIiwgIi8iKS5zcGxpdCgiLyIpCiAgICAgICAgICAgICAgICAgICAgeWVhciA9IGludCh5ZWFyX3N0cikKICAgICAgICAgICAgICAgICAgICBtb250aCA9IGludChtb250aF9zdHIpCiAgICAgICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uOgogICAgICAgICAgICAgICAgICAgIHJvd3Nfc2tpcHBlZCArPSAxCiAgICAgICAgICAgICAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoCiAgICAgICAgICAgICAgICAgICAgICAgIHNlbGYuc3R5bGUuV0FSTklORygKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGYiRmlsYSB7bGluZV9ub306IEFuaW9NZXMgbm8gdsOhbGlkbyAoe2FuaW9fbWVzIXJ9KS4iCiAgICAgICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAgICAgY29udGludWUKCiAgICAgICAgICAgICAgICBpZiBtb250aCA8IDEgb3IgbW9udGggPiAxMjoKICAgICAgICAgICAgICAgICAgICByb3dzX3NraXBwZWQgKz0gMQogICAgICAgICAgICAgICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKAogICAgICAgICAgICAgICAgICAgICAgICBzZWxmLnN0eWxlLldBUk5JTkcoCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBmIkZpbGEge2xpbmVfbm99OiBtZXMgaW52w6FsaWRvICh7bW9udGh9KS4iCiAgICAgICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAgICAgY29udGludWUKCiAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgcHJldiA9IGludChjb250cmF0b3NfcHJldmlvcykgaWYgY29udHJhdG9zX3ByZXZpb3Mgbm90IGluIChOb25lLCAiIikgZWxzZSAwCiAgICAgICAgICAgICAgICBleGNlcHQgVmFsdWVFcnJvcjoKICAgICAgICAgICAgICAgICAgICBwcmV2ID0gMAoKICAgICAgICAgICAgICAgIGNvdW50c19hc19uZXcgPSBwcmV2ID09IDAKCiAgICAgICAgICAgICAgICB1bmUgPSByZXNvbHZlX3VuZV9mcm9tX3RleHQodW5lX3JhdywgYWxpYXNlcywgdW5lc19ieV9jb2RlKQogICAgICAgICAgICAgICAgaWYgbm90IHVuZToKICAgICAgICAgICAgICAgICAgICByb3dzX3NraXBwZWQgKz0gMQogICAgICAgICAgICAgICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKAogICAgICAgICAgICAgICAgICAgICAgICBzZWxmLnN0eWxlLldBUk5JTkcoCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBmIkZpbGEge2xpbmVfbm99OiBVTkUgbm8gcmVjb25vY2lkYSAoe3VuZV9yYXchcn0pLiIKICAgICAgICAgICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgICAgICBjb250aW51ZQoKICAgICAgICAgICAgICAgIGhlYWRlcl9rZXkgPSAoeWVhciwgbW9udGgpCiAgICAgICAgICAgICAgICBoZWFkZXIgPSBoZWFkZXJzX2NhY2hlLmdldChoZWFkZXJfa2V5KQogICAgICAgICAgICAgICAgaWYgaGVhZGVyIGlzIE5vbmU6CiAgICAgICAgICAgICAgICAgICAgaGVhZGVyID0gX2Vuc3VyZV9oZWFkZXIoeWVhciwgbW9udGgsIHNvdXJjZV91cGxvYWQpCiAgICAgICAgICAgICAgICAgICAgaGVhZGVyc19jYWNoZVtoZWFkZXJfa2V5XSA9IGhlYWRlcgogICAgICAgICAgICAgICAgbW9udGhzX3RvdWNoZWQuYWRkKGhlYWRlcl9rZXkpCgogICAgICAgICAgICAgICAgY2xpZW50X25hbWUgPSAoCiAgICAgICAgICAgICAgICAgICAgcm93LmdldCgiQ2xpZW50ZSIpCiAgICAgICAgICAgICAgICAgICAgb3Igcm93LmdldCgiQ0xJRU5URSIpCiAgICAgICAgICAgICAgICAgICAgb3Igcm93LmdldCgiY2xpZW50ZSIpCiAgICAgICAgICAgICAgICAgICAgb3IgIiIKICAgICAgICAgICAgICAgICkuc3RyaXAoKQoKICAgICAgICAgICAgICAgIG5pdCA9ICgKICAgICAgICAgICAgICAgICAgICByb3cuZ2V0KCJOSVQiKQogICAgICAgICAgICAgICAgICAgIG9yIHJvdy5nZXQoIk5pdCIpCiAgICAgICAgICAgICAgICAgICAgb3Igcm93LmdldCgibml0IikKICAgICAgICAgICAgICAgICAgICBvciAiIgogICAgICAgICAgICAgICAgKS5zdHJpcCgpCgogICAgICAgICAgICAgICAgb3BlcmF0aW9uX2NvZGUgPSAoCiAgICAgICAgICAgICAgICAgICAgcm93LmdldCgiT3BlcmFjaW9uIikKICAgICAgICAgICAgICAgICAgICBvciByb3cuZ2V0KCJPcGVyYWNpw7NuIikKICAgICAgICAgICAgICAgICAgICBvciByb3cuZ2V0KCJPUEVSQUNJT04iKQogICAgICAgICAgICAgICAgICAgIG9yIHJvdy5nZXQoIm9wZXJhdGlvbl9jb2RlIikKICAgICAgICAgICAgICAgICAgICBvciAiIgogICAgICAgICAgICAgICAgKS5zdHJpcCgpCgogICAgICAgICAgICAgICAgY3VycmVuY3lfY29kZSA9ICgKICAgICAgICAgICAgICAgICAgICByb3cuZ2V0KCJNb25lZGEiKQogICAgICAgICAgICAgICAgICAgIG9yIHJvdy5nZXQoIk1PTkVEQSIpCiAgICAgICAgICAgICAgICAgICAgb3Igcm93LmdldCgibW9uZWRhIikKICAgICAgICAgICAgICAgICAgICBvciAiIgogICAgICAgICAgICAgICAgKS5zdHJpcCgpLnVwcGVyKCkKCiAgICAgICAgICAgICAgICBhbW91bnRfcmF3ID0gKAogICAgICAgICAgICAgICAgICAgIHJvdy5nZXQoIk1vbnRvIikKICAgICAgICAgICAgICAgICAgICBvciByb3cuZ2V0KCJNT05UTyIpCiAgICAgICAgICAgICAgICAgICAgb3Igcm93LmdldCgibW9udG8iKQogICAgICAgICAgICAgICAgICAgIG9yICIiCiAgICAgICAgICAgICAgICApLnN0cmlwKCkKCiAgICAgICAgICAgICAgICBhbW91bnQgPSBOb25lCiAgICAgICAgICAgICAgICBpZiBhbW91bnRfcmF3OgogICAgICAgICAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgICAgICAgICAgIyBQR0MgZXhwcmVzYSBtb250b3MgZGUgaW5ncmVzb3MgZW4gbWlsZXMgZGUgVVMkOwogICAgICAgICAgICAgICAgICAgICAgICAjIGVsIGFyY2hpdm8gdHJhZSB1bmlkYWRlcyDihpIgZ3VhcmRhciB5YSBkaXZpZGlkbyBlbnRyZSAxMDAwLgogICAgICAgICAgICAgICAgICAgICAgICBhbW91bnQgPSBEZWNpbWFsKHN0cihhbW91bnRfcmF3KS5yZXBsYWNlKCIsIiwgIiIpKSAvIERlY2ltYWwoCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAiMTAwMCIKICAgICAgICAgICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgICAgICAgICAgICAgICAgIGFtb3VudCA9IE5vbmUKCiAgICAgICAgICAgICAgICBjdXJyZW5jeSA9IGN1cnJlbmNpZXMuZ2V0KGN1cnJlbmN5X2NvZGUpCgogICAgICAgICAgICAgICAgTmV3Q2xpZW50SW1wb3J0Um93Lm9iamVjdHMuY3JlYXRlKAogICAgICAgICAgICAgICAgICAgIGhlYWRlcj1oZWFkZXIsCiAgICAgICAgICAgICAgICAgICAgdW5lPXVuZSwKICAgICAgICAgICAgICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgICAgICAgICAgY2xpZW50X25hbWU9Y2xpZW50X25hbWUsCiAgICAgICAgICAgICAgICAgICAgbml0PW5pdCwKICAgICAgICAgICAgICAgICAgICBvcGVyYXRpb25fY29kZT1vcGVyYXRpb25fY29kZSwKICAgICAgICAgICAgICAgICAgICBwcmV2aW91c19jb250cmFjdHM9cHJldiwKICAgICAgICAgICAgICAgICAgICBjb3VudHNfYXNfbmV3PWNvdW50c19hc19uZXcsCiAgICAgICAgICAgICAgICAgICAgY3VycmVuY3k9Y3VycmVuY3ksCiAgICAgICAgICAgICAgICAgICAgYW1vdW50PWFtb3VudCwKICAgICAgICAgICAgICAgICAgICBzb3VyY2Vfcm93X251bWJlcj1saW5lX25vLAogICAgICAgICAgICAgICAgICAgIHJhd191bmVfdmFsdWU9dW5lX3JhdywKICAgICAgICAgICAgICAgICAgICBvYnNlcnZhdGlvbnM9IiIsCiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICByb3dzX3dyaXR0ZW4gKz0gMQoKICAgICAgICAgICAgICAgIGlmIGNvdW50c19hc19uZXc6CiAgICAgICAgICAgICAgICAgICAga2V5ID0gKHllYXIsIG1vbnRoLCB1bmUuaWQpCiAgICAgICAgICAgICAgICAgICAgY291bnRzW2tleV0gPSBjb3VudHMuZ2V0KGtleSwgMCkgKyAxCgogICAgICAgIGlmIG1vbnRoc190b3VjaGVkOgogICAgICAgICAgICBtb250aHNfbGFiZWwgPSAiLCAiLmpvaW4oCiAgICAgICAgICAgICAgICBmInt5fS17bTowMmR9IiBmb3IgeSwgbSBpbiBzb3J0ZWQobW9udGhzX3RvdWNoZWQpCiAgICAgICAgICAgICkKICAgICAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoCiAgICAgICAgICAgICAgICBmIk1lc2VzIGRlbCBhcmNoaXZvOiB7bW9udGhzX2xhYmVsfS4gIgogICAgICAgICAgICAgICAgZiJGaWxhcyBndWFyZGFkYXM6IHtyb3dzX3dyaXR0ZW59LiBPbWl0aWRhczoge3Jvd3Nfc2tpcHBlZH0uIgogICAgICAgICAgICApCgogICAgICAgIHllYXJzX2luX2ZpbGUgPSBzb3J0ZWQoe3llYXIgZm9yICh5ZWFyLCBfLCBfKSwgXyBpbiBjb3VudHMuaXRlbXMoKX0pCiAgICAgICAgaWYgbm90IHllYXJzX2luX2ZpbGU6CiAgICAgICAgICAgICMgUHVlZGUgaGFiZXIgZmlsYXMgZ3VhcmRhZGFzIHNpbiBjb3VudHNfYXNfbmV3OyBubyBlcyBlcnJvciBkdXJvLgogICAgICAgICAgICBpZiByb3dzX3dyaXR0ZW46CiAgICAgICAgICAgICAgICBzZWxmLnN0ZG91dC53cml0ZSgKICAgICAgICAgICAgICAgICAgICBzZWxmLnN0eWxlLlNVQ0NFU1MoCiAgICAgICAgICAgICAgICAgICAgICAgIGYiSW1wb3J0IGNvbXBsZXRhZG86IHtyb3dzX3dyaXR0ZW59IGZpbGEocykgYWxtYWNlbmFkYShzKTsgIgogICAgICAgICAgICAgICAgICAgICAgICAibmluZ3VuYSBjb250w7MgY29tbyBjbGllbnRlIG51ZXZvIChDb250cmF0b3NQcmV2aW9z4omgMCkuIgogICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIHJldHVybgogICAgICAgICAgICBzZWxmLnN0ZG91dC53cml0ZSgKICAgICAgICAgICAgICAgIHNlbGYuc3R5bGUuV0FSTklORygiTm8gc2UgZW5jb250cmFyb24gZmlsYXMgaW1wb3J0YWJsZXMgZW4gZWwgYXJjaGl2by4iKQogICAgICAgICAgICApCiAgICAgICAgICAgIHJldHVybgogICAgICAgIGlmIGxlbih5ZWFyc19pbl9maWxlKSA+IDE6CiAgICAgICAgICAgIHJhaXNlIENvbW1hbmRFcnJvcigKICAgICAgICAgICAgICAgIGYiRWwgYXJjaGl2byBjb250aWVuZSBtw7psdGlwbGVzIGHDsW9zIHt5ZWFyc19pbl9maWxlfS4gIgogICAgICAgICAgICAgICAgIlBvciBhaG9yYSBzZSBlc3BlcmEgdW4gYcOxbyBwb3IgYXJjaGl2by4iCiAgICAgICAgICAgICkKICAgICAgICB5ZWFyX2Zvcl9wbGFuID0geWVhcnNfaW5fZmlsZVswXQogICAgICAgIHRyeToKICAgICAgICAgICAgcGxhbiA9IFBHQ1BsYW4ub2JqZWN0cy5nZXQoeWVhcj15ZWFyX2Zvcl9wbGFuKQogICAgICAgIGV4Y2VwdCBQR0NQbGFuLkRvZXNOb3RFeGlzdDoKICAgICAgICAgICAgcmFpc2UgQ29tbWFuZEVycm9yKGYiTm8gZXhpc3RlIFBHQ1BsYW4gcGFyYSBhw7FvIHt5ZWFyX2Zvcl9wbGFufS4iKQoKICAgICAgICB0b3RhbF91cGRhdGVkID0gMAogICAgICAgIGZvciAoeWVhciwgbW9udGgsIHVuZV9pZCksIGNvdW50IGluIGNvdW50cy5pdGVtcygpOgogICAgICAgICAgICB1bmUgPSBVTkUub2JqZWN0cy5nZXQoaWQ9dW5lX2lkKQogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICB0YXJnZXQgPSBNb250aGx5VGFyZ2V0Lm9iamVjdHMuZ2V0KAogICAgICAgICAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgICAgICAgICB1bmU9dW5lLAogICAgICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgKQogICAgICAgICAgICBleGNlcHQgTW9udGhseVRhcmdldC5Eb2VzTm90RXhpc3Q6CiAgICAgICAgICAgICAgICBzZWxmLnN0ZG91dC53cml0ZSgKICAgICAgICAgICAgICAgICAgICBzZWxmLnN0eWxlLldBUk5JTkcoCiAgICAgICAgICAgICAgICAgICAgICAgIGYiU2luIE1vbnRobHlUYXJnZXQgcGFyYSB7dW5lLmNvZGV9IHt5ZWFyfS17bW9udGg6MDJkfSIKICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICBjb250aW51ZQoKICAgICAgICAgICAgbW1yLCBfID0gTW9udGhseU1ldHJpY1Jlc3VsdC5vYmplY3RzLmdldF9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICBwbGFuPXBsYW4sCiAgICAgICAgICAgICAgICB1bmU9dW5lLAogICAgICAgICAgICAgICAgbWV0cmljPW1ldHJpYywKICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgZGVmYXVsdHM9eyJ0YXJnZXRfdmFsdWUiOiB0YXJnZXQudGFyZ2V0X3ZhbHVlfSwKICAgICAgICAgICAgKQogICAgICAgICAgICBtbXIudGFyZ2V0X3ZhbHVlID0gdGFyZ2V0LnRhcmdldF92YWx1ZQogICAgICAgICAgICBtbXIubWVhc3VyZWRfdmFsdWUgPSBEZWNpbWFsKHN0cihjb3VudCkpCiAgICAgICAgICAgIG1tci5jYWxjdWxhdGlvbl9ub3RlID0gKAogICAgICAgICAgICAgICAgZiJ7Y291bnR9IGNsaWVudGVzIG51ZXZvcyBjb250YWRvcyBkZXNkZSB7aW1wb3J0ZWRfZmlsZV9uYW1lfSIKICAgICAgICAgICAgKQogICAgICAgICAgICBtbXIuc2F2ZSgpCiAgICAgICAgICAgIHRvdGFsX3VwZGF0ZWQgKz0gMQogICAgICAgICAgICBzZWxmLnN0ZG91dC53cml0ZSgKICAgICAgICAgICAgICAgIGYiQWN0dWFsaXphZG8gQ0xJRU5URVNfTlVFVk9TIHt1bmUuY29kZX0ge3llYXJ9LXttb250aDowMmR9OiB7Y291bnR9IgogICAgICAgICAgICApCgogICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKAogICAgICAgICAgICBzZWxmLnN0eWxlLlNVQ0NFU1MoCiAgICAgICAgICAgICAgICBmIkltcG9ydCBDTElFTlRFU19OVUVWT1MgY29tcGxldGFkby4gIgogICAgICAgICAgICAgICAgZiJ7cm93c193cml0dGVufSBmaWxhKHMpLCB7dG90YWxfdXBkYXRlZH0gbcOpdHJpY2EocyksICIKICAgICAgICAgICAgICAgIGYie2xlbihtb250aHNfdG91Y2hlZCl9IG1lcyhlcykuIgogICAgICAgICAgICApCiAgICAgICAgKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/management/commands/import_ingresos.py
PATH_JSON="imports/management/commands/import_ingresos.py"
FILENAME=import_ingresos.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=324
SIZE_BYTES_UTF8=10933
CONTENT_SHA256=cf84ef13a78fb0ecc5fe74dc59da4181cce11567f85c354f13939d40ac9ec360
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
# imports/management/commands/import_ingresos.py

from decimal import Decimal
from pathlib import Path

import openpyxl
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import UNE, MetricDefinition
from pgc.models import PGCPlan, MonthlyTarget, MonthlyMetricResult, MonthlyExchangeRate


class Command(BaseCommand):
    help = (
        "Importa ingresos mensuales desde archivo de estado de resultados "
        "(xlsx) y actualiza la métrica INGRESOS por UNE (no incluye INVESTMENT)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            required=True,
            help="Ruta al archivo de estado de resultados (xlsx).",
        )
        parser.add_argument(
            "--year",
            type=int,
            required=True,
            help="Año del período, por ejemplo 2026.",
        )
        parser.add_argument(
            "--month",
            type=int,
            required=True,
            help="Mes del período, 1-12.",
        )

    def _infer_une_from_filename(self, path: Path) -> UNE:
        name = path.name.upper().strip()

        if name.startswith("WCI"):
            code = "INSURANCE"
        elif name.startswith("WCL"):
            code = "LEASING"
        elif name.startswith("WCF"):
            code = "FACTORING"
        elif name.startswith("WC"):
            code = "FACTORING"
        else:
            raise CommandError(
                f"No se pudo inferir UNE desde el nombre de archivo: {path.name}. "
                "Esperaba prefijos WC / WCF / WCI / WCL."
            )

        try:
            return UNE.objects.get(code=code)
        except UNE.DoesNotExist:
            raise CommandError(f"UNE con code={code} no existe en la base de datos.")

    def _to_decimal(self, raw_value, context: str) -> Decimal:
        if raw_value in (None, ""):
            return Decimal("0")

        text = str(raw_value).strip().replace(",", "")
        try:
            return Decimal(text)
        except Exception:
            raise CommandError(
                f"No se pudo convertir a decimal ({context}). Valor bruto={raw_value!r}"
            )

    def _sum_accounts_starting_with(self, ws, month: int, prefix: str) -> Decimal:
        """
        Suma cuentas contables que empiezan con `prefix` (ej: '4' o '8').
        
        Lógica:
        1) Buscar primero si existe una fila con CUENTA == prefix.
           - Si existe, usar SALDOFIN y terminar.
        2) Solo si NO existe CUENTA == prefix, usar la lógica alterna:
           - sumar filas cuyo código empiece con prefix
           - y tenga exactamente 9 dígitos
           - tomando el valor de la columna del mes en español.
        """
        cuenta_col = 2  # B

        # ---- Paso 1: detectar si existe CUENTA == prefix ----
        row_with_prefix = None
        for row in ws.iter_rows(min_row=2):
            cuenta = row[cuenta_col - 1].value
            if cuenta is None:
                continue
            if str(cuenta).strip() == prefix:
                row_with_prefix = row
                break

        # ---- Si existe CUENTA == prefix, usar SOLO esa lógica ----
        if row_with_prefix is not None:
            saldo_fin_col = None
            for col_idx, cell in enumerate(ws[1], start=1):
                if cell.value is None:
                    continue
                if str(cell.value).strip().upper() == "SALDOFIN":
                    saldo_fin_col = col_idx
                    break

            if saldo_fin_col is None:
                # No hay columna SALDOFIN, retornar cero (sin error)
                return Decimal("0")

            saldo_value = row_with_prefix[saldo_fin_col - 1].value
            return self._to_decimal(
                saldo_value,
                f"hoja Datos fila CUENTA={prefix} SALDOFIN",
            )

        # ---- Paso 2: solo si NO existe CUENTA == prefix, usar lógica mensual ----
        month_names = {
            1: "ENERO",
            2: "FEBRERO",
            3: "MARZO",
            4: "ABRIL",
            5: "MAYO",
            6: "JUNIO",
            7: "JULIO",
            8: "AGOSTO",
            9: "SEPTIEMBRE",
            10: "OCTUBRE",
            11: "NOVIEMBRE",
            12: "DICIEMBRE",
        }

        month_name = month_names.get(month)
        if not month_name:
            raise CommandError(f"Mes inválido: {month}")

        month_col = None
        for col_idx, cell in enumerate(ws[1], start=1):
            if cell.value is None:
                continue
            if str(cell.value).strip().upper() == month_name:
                month_col = col_idx
                break

        if month_col is None:
            # No hay columna del mes, retornar cero (sin error)
            return Decimal("0")

        total = Decimal("0")
        for row in ws.iter_rows(min_row=2):
            cuenta = row[cuenta_col - 1].value
            if cuenta is None:
                continue

            cuenta_str = str(cuenta).strip()
            cuenta_digits = "".join(ch for ch in cuenta_str if ch.isdigit())

            if cuenta_digits.startswith(prefix) and len(cuenta_digits) == 9:
                month_value = row[month_col - 1].value
                if month_value in (None, ""):
                    continue

                total += self._to_decimal(
                    month_value,
                    f"cuenta {cuenta_str} columna {month_name}",
                )

        return total

    def _read_ingreso_from_excel(self, path: Path, month: int) -> Decimal:
        """
        Lee el ingreso bruto desde el estado de resultados.
        
        Regla fija: suma los ingresos de cuentas que empiezan con 4
        MÁS los ingresos de cuentas que empiezan con 8.
        """
        try:
            wb = openpyxl.load_workbook(path, data_only=True)
        except Exception as e:
            raise CommandError(f"No se pudo abrir el archivo Excel: {e}")

        if "Datos" not in wb.sheetnames:
            raise CommandError(
                f"El archivo {path.name} no contiene hoja 'Datos'. "
                f"Hojas disponibles: {', '.join(wb.sheetnames)}"
            )

        ws = wb["Datos"]

        # Suma cuentas que empiezan con 4
        suma_4 = self._sum_accounts_starting_with(ws, month, "4")
        
        # Suma cuentas que empiezan con 8
        suma_8 = self._sum_accounts_starting_with(ws, month, "8")

        # Total = 4 + 8
        total = suma_4 + suma_8

        self.stdout.write(
            self.style.WARNING(
                f"  Cuentas '4': {suma_4} | Cuentas '8': {suma_8} | Total: {total}"
            )
        )

        return total

    def _get_exchange_rate(self, year: int, month: int) -> Decimal:
        try:
            rate = MonthlyExchangeRate.objects.get(year=year, month=month)
        except MonthlyExchangeRate.DoesNotExist:
            raise CommandError(
                f"No existe tipo de cambio para {year}-{month:02d}. "
                "Debe registrar MonthlyExchangeRate antes de importar ingresos."
            )

        if rate.usd_to_gtq in (None, Decimal("0")):
            raise CommandError(
                f"Tipo de cambio inválido para {year}-{month:02d}: {rate.usd_to_gtq}"
            )

        return rate.usd_to_gtq

    @transaction.atomic
    def handle(self, *args, **options):
        path = Path(options["path"])
        year = options["year"]
        month = options["month"]

        if not path.exists():
            raise CommandError(f"Archivo no encontrado: {path}")

        self.stdout.write(
            self.style.WARNING(f"Leyendo estado de resultados desde {path} ...")
        )

        try:
            plan = PGCPlan.objects.get(year=year)
        except PGCPlan.DoesNotExist:
            raise CommandError(f"No existe PGCPlan para year={year}")

        try:
            metric = MetricDefinition.objects.get(
                code=MetricDefinition.CODE_INGRESOS
            )
        except MetricDefinition.DoesNotExist:
            raise CommandError("No existe MetricDefinition para CODE_INGRESOS")

        une = self._infer_une_from_filename(path)
        if une.code == "INVESTMENT":
            raise CommandError(
                "Este comando no debe usarse para INVESTMENT; "
                "para esa UNE use el recálculo desde NewClientImportRow."
            )

        self.stdout.write(self.style.WARNING(f"Archivo detectado para UNE={une.code}"))

        ingreso_bruto_gtq = self._read_ingreso_from_excel(path, month)
        
        if ingreso_bruto_gtq is None:
            raise CommandError(
                f"_read_ingreso_from_excel devolvió None para {path.name} "
                f"en {year}-{month:02d}."
            )

        # TERCERO del plan: Insurance también se divide entre mil
        if une.code in ("FACTORING", "LEASING", "INSURANCE"):
            ingreso_ajustado_gtq = ingreso_bruto_gtq / Decimal("1000")
        else:
            ingreso_ajustado_gtq = ingreso_bruto_gtq

        tipo_cambio = self._get_exchange_rate(year, month)
        ingreso_usd = ingreso_ajustado_gtq / tipo_cambio

        try:
            target = MonthlyTarget.objects.get(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
            )
        except MonthlyTarget.DoesNotExist:
            raise CommandError(
                f"No existe MonthlyTarget para INGRESOS {une.code} "
                f"{year}-{month:02d}."
            )

        mmr, _ = MonthlyMetricResult.objects.get_or_create(
            plan=plan,
            une=une,
            metric=metric,
            year=year,
            month=month,
            defaults={"target_value": target.target_value},
        )

        mmr.target_value = target.target_value
        mmr.measured_value = ingreso_usd

        measured = mmr.measured_value or Decimal("0")
        target_val = mmr.target_value or Decimal("0")
        achieved = measured >= target_val

        mmr.is_achieved = achieved
        mmr.points_awarded = target.points_if_achieved if achieved else 0
        mmr.calculation_note = (
            f"Ingreso importado desde {path.name}, hoja Datos. "
            f"BrutoGTQ(4+8)={ingreso_bruto_gtq}, "
            f"AjustadoGTQ={ingreso_ajustado_gtq}, "
            f"TipoCambioGTQxUSD={tipo_cambio}, "
            f"USD={ingreso_usd}, UNE={une.code}."
        )
        mmr.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Actualizado INGRESOS {une.code} {year}-{month:02d}: "
                f"real={measured} meta={target_val} "
                f"logrado={achieved} puntos={mmr.points_awarded}"
            )
        )
        self.stdout.write(self.style.SUCCESS("Import INGRESOS completado."))
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|# imports/management/commands/import_ingresos.py
00002|
00003|from decimal import Decimal
00004|from pathlib import Path
00005|
00006|import openpyxl
00007|from django.core.management.base import BaseCommand, CommandError
00008|from django.db import transaction
00009|
00010|from core.models import UNE, MetricDefinition
00011|from pgc.models import PGCPlan, MonthlyTarget, MonthlyMetricResult, MonthlyExchangeRate
00012|
00013|
00014|class Command(BaseCommand):
00015|    help = (
00016|        "Importa ingresos mensuales desde archivo de estado de resultados "
00017|        "(xlsx) y actualiza la métrica INGRESOS por UNE (no incluye INVESTMENT)."
00018|    )
00019|
00020|    def add_arguments(self, parser):
00021|        parser.add_argument(
00022|            "--path",
00023|            type=str,
00024|            required=True,
00025|            help="Ruta al archivo de estado de resultados (xlsx).",
00026|        )
00027|        parser.add_argument(
00028|            "--year",
00029|            type=int,
00030|            required=True,
00031|            help="Año del período, por ejemplo 2026.",
00032|        )
00033|        parser.add_argument(
00034|            "--month",
00035|            type=int,
00036|            required=True,
00037|            help="Mes del período, 1-12.",
00038|        )
00039|
00040|    def _infer_une_from_filename(self, path: Path) -> UNE:
00041|        name = path.name.upper().strip()
00042|
00043|        if name.startswith("WCI"):
00044|            code = "INSURANCE"
00045|        elif name.startswith("WCL"):
00046|            code = "LEASING"
00047|        elif name.startswith("WCF"):
00048|            code = "FACTORING"
00049|        elif name.startswith("WC"):
00050|            code = "FACTORING"
00051|        else:
00052|            raise CommandError(
00053|                f"No se pudo inferir UNE desde el nombre de archivo: {path.name}. "
00054|                "Esperaba prefijos WC / WCF / WCI / WCL."
00055|            )
00056|
00057|        try:
00058|            return UNE.objects.get(code=code)
00059|        except UNE.DoesNotExist:
00060|            raise CommandError(f"UNE con code={code} no existe en la base de datos.")
00061|
00062|    def _to_decimal(self, raw_value, context: str) -> Decimal:
00063|        if raw_value in (None, ""):
00064|            return Decimal("0")
00065|
00066|        text = str(raw_value).strip().replace(",", "")
00067|        try:
00068|            return Decimal(text)
00069|        except Exception:
00070|            raise CommandError(
00071|                f"No se pudo convertir a decimal ({context}). Valor bruto={raw_value!r}"
00072|            )
00073|
00074|    def _sum_accounts_starting_with(self, ws, month: int, prefix: str) -> Decimal:
00075|        """
00076|        Suma cuentas contables que empiezan con `prefix` (ej: '4' o '8').
00077|        
00078|        Lógica:
00079|        1) Buscar primero si existe una fila con CUENTA == prefix.
00080|           - Si existe, usar SALDOFIN y terminar.
00081|        2) Solo si NO existe CUENTA == prefix, usar la lógica alterna:
00082|           - sumar filas cuyo código empiece con prefix
00083|           - y tenga exactamente 9 dígitos
00084|           - tomando el valor de la columna del mes en español.
00085|        """
00086|        cuenta_col = 2  # B
00087|
00088|        # ---- Paso 1: detectar si existe CUENTA == prefix ----
00089|        row_with_prefix = None
00090|        for row in ws.iter_rows(min_row=2):
00091|            cuenta = row[cuenta_col - 1].value
00092|            if cuenta is None:
00093|                continue
00094|            if str(cuenta).strip() == prefix:
00095|                row_with_prefix = row
00096|                break
00097|
00098|        # ---- Si existe CUENTA == prefix, usar SOLO esa lógica ----
00099|        if row_with_prefix is not None:
00100|            saldo_fin_col = None
00101|            for col_idx, cell in enumerate(ws[1], start=1):
00102|                if cell.value is None:
00103|                    continue
00104|                if str(cell.value).strip().upper() == "SALDOFIN":
00105|                    saldo_fin_col = col_idx
00106|                    break
00107|
00108|            if saldo_fin_col is None:
00109|                # No hay columna SALDOFIN, retornar cero (sin error)
00110|                return Decimal("0")
00111|
00112|            saldo_value = row_with_prefix[saldo_fin_col - 1].value
00113|            return self._to_decimal(
00114|                saldo_value,
00115|                f"hoja Datos fila CUENTA={prefix} SALDOFIN",
00116|            )
00117|
00118|        # ---- Paso 2: solo si NO existe CUENTA == prefix, usar lógica mensual ----
00119|        month_names = {
00120|            1: "ENERO",
00121|            2: "FEBRERO",
00122|            3: "MARZO",
00123|            4: "ABRIL",
00124|            5: "MAYO",
00125|            6: "JUNIO",
00126|            7: "JULIO",
00127|            8: "AGOSTO",
00128|            9: "SEPTIEMBRE",
00129|            10: "OCTUBRE",
00130|            11: "NOVIEMBRE",
00131|            12: "DICIEMBRE",
00132|        }
00133|
00134|        month_name = month_names.get(month)
00135|        if not month_name:
00136|            raise CommandError(f"Mes inválido: {month}")
00137|
00138|        month_col = None
00139|        for col_idx, cell in enumerate(ws[1], start=1):
00140|            if cell.value is None:
00141|                continue
00142|            if str(cell.value).strip().upper() == month_name:
00143|                month_col = col_idx
00144|                break
00145|
00146|        if month_col is None:
00147|            # No hay columna del mes, retornar cero (sin error)
00148|            return Decimal("0")
00149|
00150|        total = Decimal("0")
00151|        for row in ws.iter_rows(min_row=2):
00152|            cuenta = row[cuenta_col - 1].value
00153|            if cuenta is None:
00154|                continue
00155|
00156|            cuenta_str = str(cuenta).strip()
00157|            cuenta_digits = "".join(ch for ch in cuenta_str if ch.isdigit())
00158|
00159|            if cuenta_digits.startswith(prefix) and len(cuenta_digits) == 9:
00160|                month_value = row[month_col - 1].value
00161|                if month_value in (None, ""):
00162|                    continue
00163|
00164|                total += self._to_decimal(
00165|                    month_value,
00166|                    f"cuenta {cuenta_str} columna {month_name}",
00167|                )
00168|
00169|        return total
00170|
00171|    def _read_ingreso_from_excel(self, path: Path, month: int) -> Decimal:
00172|        """
00173|        Lee el ingreso bruto desde el estado de resultados.
00174|        
00175|        Regla fija: suma los ingresos de cuentas que empiezan con 4
00176|        MÁS los ingresos de cuentas que empiezan con 8.
00177|        """
00178|        try:
00179|            wb = openpyxl.load_workbook(path, data_only=True)
00180|        except Exception as e:
00181|            raise CommandError(f"No se pudo abrir el archivo Excel: {e}")
00182|
00183|        if "Datos" not in wb.sheetnames:
00184|            raise CommandError(
00185|                f"El archivo {path.name} no contiene hoja 'Datos'. "
00186|                f"Hojas disponibles: {', '.join(wb.sheetnames)}"
00187|            )
00188|
00189|        ws = wb["Datos"]
00190|
00191|        # Suma cuentas que empiezan con 4
00192|        suma_4 = self._sum_accounts_starting_with(ws, month, "4")
00193|        
00194|        # Suma cuentas que empiezan con 8
00195|        suma_8 = self._sum_accounts_starting_with(ws, month, "8")
00196|
00197|        # Total = 4 + 8
00198|        total = suma_4 + suma_8
00199|
00200|        self.stdout.write(
00201|            self.style.WARNING(
00202|                f"  Cuentas '4': {suma_4} | Cuentas '8': {suma_8} | Total: {total}"
00203|            )
00204|        )
00205|
00206|        return total
00207|
00208|    def _get_exchange_rate(self, year: int, month: int) -> Decimal:
00209|        try:
00210|            rate = MonthlyExchangeRate.objects.get(year=year, month=month)
00211|        except MonthlyExchangeRate.DoesNotExist:
00212|            raise CommandError(
00213|                f"No existe tipo de cambio para {year}-{month:02d}. "
00214|                "Debe registrar MonthlyExchangeRate antes de importar ingresos."
00215|            )
00216|
00217|        if rate.usd_to_gtq in (None, Decimal("0")):
00218|            raise CommandError(
00219|                f"Tipo de cambio inválido para {year}-{month:02d}: {rate.usd_to_gtq}"
00220|            )
00221|
00222|        return rate.usd_to_gtq
00223|
00224|    @transaction.atomic
00225|    def handle(self, *args, **options):
00226|        path = Path(options["path"])
00227|        year = options["year"]
00228|        month = options["month"]
00229|
00230|        if not path.exists():
00231|            raise CommandError(f"Archivo no encontrado: {path}")
00232|
00233|        self.stdout.write(
00234|            self.style.WARNING(f"Leyendo estado de resultados desde {path} ...")
00235|        )
00236|
00237|        try:
00238|            plan = PGCPlan.objects.get(year=year)
00239|        except PGCPlan.DoesNotExist:
00240|            raise CommandError(f"No existe PGCPlan para year={year}")
00241|
00242|        try:
00243|            metric = MetricDefinition.objects.get(
00244|                code=MetricDefinition.CODE_INGRESOS
00245|            )
00246|        except MetricDefinition.DoesNotExist:
00247|            raise CommandError("No existe MetricDefinition para CODE_INGRESOS")
00248|
00249|        une = self._infer_une_from_filename(path)
00250|        if une.code == "INVESTMENT":
00251|            raise CommandError(
00252|                "Este comando no debe usarse para INVESTMENT; "
00253|                "para esa UNE use el recálculo desde NewClientImportRow."
00254|            )
00255|
00256|        self.stdout.write(self.style.WARNING(f"Archivo detectado para UNE={une.code}"))
00257|
00258|        ingreso_bruto_gtq = self._read_ingreso_from_excel(path, month)
00259|        
00260|        if ingreso_bruto_gtq is None:
00261|            raise CommandError(
00262|                f"_read_ingreso_from_excel devolvió None para {path.name} "
00263|                f"en {year}-{month:02d}."
00264|            )
00265|
00266|        # TERCERO del plan: Insurance también se divide entre mil
00267|        if une.code in ("FACTORING", "LEASING", "INSURANCE"):
00268|            ingreso_ajustado_gtq = ingreso_bruto_gtq / Decimal("1000")
00269|        else:
00270|            ingreso_ajustado_gtq = ingreso_bruto_gtq
00271|
00272|        tipo_cambio = self._get_exchange_rate(year, month)
00273|        ingreso_usd = ingreso_ajustado_gtq / tipo_cambio
00274|
00275|        try:
00276|            target = MonthlyTarget.objects.get(
00277|                plan=plan,
00278|                une=une,
00279|                metric=metric,
00280|                year=year,
00281|                month=month,
00282|            )
00283|        except MonthlyTarget.DoesNotExist:
00284|            raise CommandError(
00285|                f"No existe MonthlyTarget para INGRESOS {une.code} "
00286|                f"{year}-{month:02d}."
00287|            )
00288|
00289|        mmr, _ = MonthlyMetricResult.objects.get_or_create(
00290|            plan=plan,
00291|            une=une,
00292|            metric=metric,
00293|            year=year,
00294|            month=month,
00295|            defaults={"target_value": target.target_value},
00296|        )
00297|
00298|        mmr.target_value = target.target_value
00299|        mmr.measured_value = ingreso_usd
00300|
00301|        measured = mmr.measured_value or Decimal("0")
00302|        target_val = mmr.target_value or Decimal("0")
00303|        achieved = measured >= target_val
00304|
00305|        mmr.is_achieved = achieved
00306|        mmr.points_awarded = target.points_if_achieved if achieved else 0
00307|        mmr.calculation_note = (
00308|            f"Ingreso importado desde {path.name}, hoja Datos. "
00309|            f"BrutoGTQ(4+8)={ingreso_bruto_gtq}, "
00310|            f"AjustadoGTQ={ingreso_ajustado_gtq}, "
00311|            f"TipoCambioGTQxUSD={tipo_cambio}, "
00312|            f"USD={ingreso_usd}, UNE={une.code}."
00313|        )
00314|        mmr.save()
00315|
00316|        self.stdout.write(
00317|            self.style.SUCCESS(
00318|                f"Actualizado INGRESOS {une.code} {year}-{month:02d}: "
00319|                f"real={measured} meta={target_val} "
00320|                f"logrado={achieved} puntos={mmr.points_awarded}"
00321|            )
00322|        )
00323|        self.stdout.write(self.style.SUCCESS("Import INGRESOS completado."))
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IyBpbXBvcnRzL21hbmFnZW1lbnQvY29tbWFuZHMvaW1wb3J0X2luZ3Jlc29zLnB5Cgpmcm9tIGRlY2ltYWwgaW1wb3J0IERlY2ltYWwKZnJvbSBwYXRobGliIGltcG9ydCBQYXRoCgppbXBvcnQgb3BlbnB5eGwKZnJvbSBkamFuZ28uY29yZS5tYW5hZ2VtZW50LmJhc2UgaW1wb3J0IEJhc2VDb21tYW5kLCBDb21tYW5kRXJyb3IKZnJvbSBkamFuZ28uZGIgaW1wb3J0IHRyYW5zYWN0aW9uCgpmcm9tIGNvcmUubW9kZWxzIGltcG9ydCBVTkUsIE1ldHJpY0RlZmluaXRpb24KZnJvbSBwZ2MubW9kZWxzIGltcG9ydCBQR0NQbGFuLCBNb250aGx5VGFyZ2V0LCBNb250aGx5TWV0cmljUmVzdWx0LCBNb250aGx5RXhjaGFuZ2VSYXRlCgoKY2xhc3MgQ29tbWFuZChCYXNlQ29tbWFuZCk6CiAgICBoZWxwID0gKAogICAgICAgICJJbXBvcnRhIGluZ3Jlc29zIG1lbnN1YWxlcyBkZXNkZSBhcmNoaXZvIGRlIGVzdGFkbyBkZSByZXN1bHRhZG9zICIKICAgICAgICAiKHhsc3gpIHkgYWN0dWFsaXphIGxhIG3DqXRyaWNhIElOR1JFU09TIHBvciBVTkUgKG5vIGluY2x1eWUgSU5WRVNUTUVOVCkuIgogICAgKQoKICAgIGRlZiBhZGRfYXJndW1lbnRzKHNlbGYsIHBhcnNlcik6CiAgICAgICAgcGFyc2VyLmFkZF9hcmd1bWVudCgKICAgICAgICAgICAgIi0tcGF0aCIsCiAgICAgICAgICAgIHR5cGU9c3RyLAogICAgICAgICAgICByZXF1aXJlZD1UcnVlLAogICAgICAgICAgICBoZWxwPSJSdXRhIGFsIGFyY2hpdm8gZGUgZXN0YWRvIGRlIHJlc3VsdGFkb3MgKHhsc3gpLiIsCiAgICAgICAgKQogICAgICAgIHBhcnNlci5hZGRfYXJndW1lbnQoCiAgICAgICAgICAgICItLXllYXIiLAogICAgICAgICAgICB0eXBlPWludCwKICAgICAgICAgICAgcmVxdWlyZWQ9VHJ1ZSwKICAgICAgICAgICAgaGVscD0iQcOxbyBkZWwgcGVyw61vZG8sIHBvciBlamVtcGxvIDIwMjYuIiwKICAgICAgICApCiAgICAgICAgcGFyc2VyLmFkZF9hcmd1bWVudCgKICAgICAgICAgICAgIi0tbW9udGgiLAogICAgICAgICAgICB0eXBlPWludCwKICAgICAgICAgICAgcmVxdWlyZWQ9VHJ1ZSwKICAgICAgICAgICAgaGVscD0iTWVzIGRlbCBwZXLDrW9kbywgMS0xMi4iLAogICAgICAgICkKCiAgICBkZWYgX2luZmVyX3VuZV9mcm9tX2ZpbGVuYW1lKHNlbGYsIHBhdGg6IFBhdGgpIC0+IFVORToKICAgICAgICBuYW1lID0gcGF0aC5uYW1lLnVwcGVyKCkuc3RyaXAoKQoKICAgICAgICBpZiBuYW1lLnN0YXJ0c3dpdGgoIldDSSIpOgogICAgICAgICAgICBjb2RlID0gIklOU1VSQU5DRSIKICAgICAgICBlbGlmIG5hbWUuc3RhcnRzd2l0aCgiV0NMIik6CiAgICAgICAgICAgIGNvZGUgPSAiTEVBU0lORyIKICAgICAgICBlbGlmIG5hbWUuc3RhcnRzd2l0aCgiV0NGIik6CiAgICAgICAgICAgIGNvZGUgPSAiRkFDVE9SSU5HIgogICAgICAgIGVsaWYgbmFtZS5zdGFydHN3aXRoKCJXQyIpOgogICAgICAgICAgICBjb2RlID0gIkZBQ1RPUklORyIKICAgICAgICBlbHNlOgogICAgICAgICAgICByYWlzZSBDb21tYW5kRXJyb3IoCiAgICAgICAgICAgICAgICBmIk5vIHNlIHB1ZG8gaW5mZXJpciBVTkUgZGVzZGUgZWwgbm9tYnJlIGRlIGFyY2hpdm86IHtwYXRoLm5hbWV9LiAiCiAgICAgICAgICAgICAgICAiRXNwZXJhYmEgcHJlZmlqb3MgV0MgLyBXQ0YgLyBXQ0kgLyBXQ0wuIgogICAgICAgICAgICApCgogICAgICAgIHRyeToKICAgICAgICAgICAgcmV0dXJuIFVORS5vYmplY3RzLmdldChjb2RlPWNvZGUpCiAgICAgICAgZXhjZXB0IFVORS5Eb2VzTm90RXhpc3Q6CiAgICAgICAgICAgIHJhaXNlIENvbW1hbmRFcnJvcihmIlVORSBjb24gY29kZT17Y29kZX0gbm8gZXhpc3RlIGVuIGxhIGJhc2UgZGUgZGF0b3MuIikKCiAgICBkZWYgX3RvX2RlY2ltYWwoc2VsZiwgcmF3X3ZhbHVlLCBjb250ZXh0OiBzdHIpIC0+IERlY2ltYWw6CiAgICAgICAgaWYgcmF3X3ZhbHVlIGluIChOb25lLCAiIik6CiAgICAgICAgICAgIHJldHVybiBEZWNpbWFsKCIwIikKCiAgICAgICAgdGV4dCA9IHN0cihyYXdfdmFsdWUpLnN0cmlwKCkucmVwbGFjZSgiLCIsICIiKQogICAgICAgIHRyeToKICAgICAgICAgICAgcmV0dXJuIERlY2ltYWwodGV4dCkKICAgICAgICBleGNlcHQgRXhjZXB0aW9uOgogICAgICAgICAgICByYWlzZSBDb21tYW5kRXJyb3IoCiAgICAgICAgICAgICAgICBmIk5vIHNlIHB1ZG8gY29udmVydGlyIGEgZGVjaW1hbCAoe2NvbnRleHR9KS4gVmFsb3IgYnJ1dG89e3Jhd192YWx1ZSFyfSIKICAgICAgICAgICAgKQoKICAgIGRlZiBfc3VtX2FjY291bnRzX3N0YXJ0aW5nX3dpdGgoc2VsZiwgd3MsIG1vbnRoOiBpbnQsIHByZWZpeDogc3RyKSAtPiBEZWNpbWFsOgogICAgICAgICIiIgogICAgICAgIFN1bWEgY3VlbnRhcyBjb250YWJsZXMgcXVlIGVtcGllemFuIGNvbiBgcHJlZml4YCAoZWo6ICc0JyBvICc4JykuCiAgICAgICAgCiAgICAgICAgTMOzZ2ljYToKICAgICAgICAxKSBCdXNjYXIgcHJpbWVybyBzaSBleGlzdGUgdW5hIGZpbGEgY29uIENVRU5UQSA9PSBwcmVmaXguCiAgICAgICAgICAgLSBTaSBleGlzdGUsIHVzYXIgU0FMRE9GSU4geSB0ZXJtaW5hci4KICAgICAgICAyKSBTb2xvIHNpIE5PIGV4aXN0ZSBDVUVOVEEgPT0gcHJlZml4LCB1c2FyIGxhIGzDs2dpY2EgYWx0ZXJuYToKICAgICAgICAgICAtIHN1bWFyIGZpbGFzIGN1eW8gY8OzZGlnbyBlbXBpZWNlIGNvbiBwcmVmaXgKICAgICAgICAgICAtIHkgdGVuZ2EgZXhhY3RhbWVudGUgOSBkw61naXRvcwogICAgICAgICAgIC0gdG9tYW5kbyBlbCB2YWxvciBkZSBsYSBjb2x1bW5hIGRlbCBtZXMgZW4gZXNwYcOxb2wuCiAgICAgICAgIiIiCiAgICAgICAgY3VlbnRhX2NvbCA9IDIgICMgQgoKICAgICAgICAjIC0tLS0gUGFzbyAxOiBkZXRlY3RhciBzaSBleGlzdGUgQ1VFTlRBID09IHByZWZpeCAtLS0tCiAgICAgICAgcm93X3dpdGhfcHJlZml4ID0gTm9uZQogICAgICAgIGZvciByb3cgaW4gd3MuaXRlcl9yb3dzKG1pbl9yb3c9Mik6CiAgICAgICAgICAgIGN1ZW50YSA9IHJvd1tjdWVudGFfY29sIC0gMV0udmFsdWUKICAgICAgICAgICAgaWYgY3VlbnRhIGlzIE5vbmU6CiAgICAgICAgICAgICAgICBjb250aW51ZQogICAgICAgICAgICBpZiBzdHIoY3VlbnRhKS5zdHJpcCgpID09IHByZWZpeDoKICAgICAgICAgICAgICAgIHJvd193aXRoX3ByZWZpeCA9IHJvdwogICAgICAgICAgICAgICAgYnJlYWsKCiAgICAgICAgIyAtLS0tIFNpIGV4aXN0ZSBDVUVOVEEgPT0gcHJlZml4LCB1c2FyIFNPTE8gZXNhIGzDs2dpY2EgLS0tLQogICAgICAgIGlmIHJvd193aXRoX3ByZWZpeCBpcyBub3QgTm9uZToKICAgICAgICAgICAgc2FsZG9fZmluX2NvbCA9IE5vbmUKICAgICAgICAgICAgZm9yIGNvbF9pZHgsIGNlbGwgaW4gZW51bWVyYXRlKHdzWzFdLCBzdGFydD0xKToKICAgICAgICAgICAgICAgIGlmIGNlbGwudmFsdWUgaXMgTm9uZToKICAgICAgICAgICAgICAgICAgICBjb250aW51ZQogICAgICAgICAgICAgICAgaWYgc3RyKGNlbGwudmFsdWUpLnN0cmlwKCkudXBwZXIoKSA9PSAiU0FMRE9GSU4iOgogICAgICAgICAgICAgICAgICAgIHNhbGRvX2Zpbl9jb2wgPSBjb2xfaWR4CiAgICAgICAgICAgICAgICAgICAgYnJlYWsKCiAgICAgICAgICAgIGlmIHNhbGRvX2Zpbl9jb2wgaXMgTm9uZToKICAgICAgICAgICAgICAgICMgTm8gaGF5IGNvbHVtbmEgU0FMRE9GSU4sIHJldG9ybmFyIGNlcm8gKHNpbiBlcnJvcikKICAgICAgICAgICAgICAgIHJldHVybiBEZWNpbWFsKCIwIikKCiAgICAgICAgICAgIHNhbGRvX3ZhbHVlID0gcm93X3dpdGhfcHJlZml4W3NhbGRvX2Zpbl9jb2wgLSAxXS52YWx1ZQogICAgICAgICAgICByZXR1cm4gc2VsZi5fdG9fZGVjaW1hbCgKICAgICAgICAgICAgICAgIHNhbGRvX3ZhbHVlLAogICAgICAgICAgICAgICAgZiJob2phIERhdG9zIGZpbGEgQ1VFTlRBPXtwcmVmaXh9IFNBTERPRklOIiwKICAgICAgICAgICAgKQoKICAgICAgICAjIC0tLS0gUGFzbyAyOiBzb2xvIHNpIE5PIGV4aXN0ZSBDVUVOVEEgPT0gcHJlZml4LCB1c2FyIGzDs2dpY2EgbWVuc3VhbCAtLS0tCiAgICAgICAgbW9udGhfbmFtZXMgPSB7CiAgICAgICAgICAgIDE6ICJFTkVSTyIsCiAgICAgICAgICAgIDI6ICJGRUJSRVJPIiwKICAgICAgICAgICAgMzogIk1BUlpPIiwKICAgICAgICAgICAgNDogIkFCUklMIiwKICAgICAgICAgICAgNTogIk1BWU8iLAogICAgICAgICAgICA2OiAiSlVOSU8iLAogICAgICAgICAgICA3OiAiSlVMSU8iLAogICAgICAgICAgICA4OiAiQUdPU1RPIiwKICAgICAgICAgICAgOTogIlNFUFRJRU1CUkUiLAogICAgICAgICAgICAxMDogIk9DVFVCUkUiLAogICAgICAgICAgICAxMTogIk5PVklFTUJSRSIsCiAgICAgICAgICAgIDEyOiAiRElDSUVNQlJFIiwKICAgICAgICB9CgogICAgICAgIG1vbnRoX25hbWUgPSBtb250aF9uYW1lcy5nZXQobW9udGgpCiAgICAgICAgaWYgbm90IG1vbnRoX25hbWU6CiAgICAgICAgICAgIHJhaXNlIENvbW1hbmRFcnJvcihmIk1lcyBpbnbDoWxpZG86IHttb250aH0iKQoKICAgICAgICBtb250aF9jb2wgPSBOb25lCiAgICAgICAgZm9yIGNvbF9pZHgsIGNlbGwgaW4gZW51bWVyYXRlKHdzWzFdLCBzdGFydD0xKToKICAgICAgICAgICAgaWYgY2VsbC52YWx1ZSBpcyBOb25lOgogICAgICAgICAgICAgICAgY29udGludWUKICAgICAgICAgICAgaWYgc3RyKGNlbGwudmFsdWUpLnN0cmlwKCkudXBwZXIoKSA9PSBtb250aF9uYW1lOgogICAgICAgICAgICAgICAgbW9udGhfY29sID0gY29sX2lkeAogICAgICAgICAgICAgICAgYnJlYWsKCiAgICAgICAgaWYgbW9udGhfY29sIGlzIE5vbmU6CiAgICAgICAgICAgICMgTm8gaGF5IGNvbHVtbmEgZGVsIG1lcywgcmV0b3JuYXIgY2VybyAoc2luIGVycm9yKQogICAgICAgICAgICByZXR1cm4gRGVjaW1hbCgiMCIpCgogICAgICAgIHRvdGFsID0gRGVjaW1hbCgiMCIpCiAgICAgICAgZm9yIHJvdyBpbiB3cy5pdGVyX3Jvd3MobWluX3Jvdz0yKToKICAgICAgICAgICAgY3VlbnRhID0gcm93W2N1ZW50YV9jb2wgLSAxXS52YWx1ZQogICAgICAgICAgICBpZiBjdWVudGEgaXMgTm9uZToKICAgICAgICAgICAgICAgIGNvbnRpbnVlCgogICAgICAgICAgICBjdWVudGFfc3RyID0gc3RyKGN1ZW50YSkuc3RyaXAoKQogICAgICAgICAgICBjdWVudGFfZGlnaXRzID0gIiIuam9pbihjaCBmb3IgY2ggaW4gY3VlbnRhX3N0ciBpZiBjaC5pc2RpZ2l0KCkpCgogICAgICAgICAgICBpZiBjdWVudGFfZGlnaXRzLnN0YXJ0c3dpdGgocHJlZml4KSBhbmQgbGVuKGN1ZW50YV9kaWdpdHMpID09IDk6CiAgICAgICAgICAgICAgICBtb250aF92YWx1ZSA9IHJvd1ttb250aF9jb2wgLSAxXS52YWx1ZQogICAgICAgICAgICAgICAgaWYgbW9udGhfdmFsdWUgaW4gKE5vbmUsICIiKToKICAgICAgICAgICAgICAgICAgICBjb250aW51ZQoKICAgICAgICAgICAgICAgIHRvdGFsICs9IHNlbGYuX3RvX2RlY2ltYWwoCiAgICAgICAgICAgICAgICAgICAgbW9udGhfdmFsdWUsCiAgICAgICAgICAgICAgICAgICAgZiJjdWVudGEge2N1ZW50YV9zdHJ9IGNvbHVtbmEge21vbnRoX25hbWV9IiwKICAgICAgICAgICAgICAgICkKCiAgICAgICAgcmV0dXJuIHRvdGFsCgogICAgZGVmIF9yZWFkX2luZ3Jlc29fZnJvbV9leGNlbChzZWxmLCBwYXRoOiBQYXRoLCBtb250aDogaW50KSAtPiBEZWNpbWFsOgogICAgICAgICIiIgogICAgICAgIExlZSBlbCBpbmdyZXNvIGJydXRvIGRlc2RlIGVsIGVzdGFkbyBkZSByZXN1bHRhZG9zLgogICAgICAgIAogICAgICAgIFJlZ2xhIGZpamE6IHN1bWEgbG9zIGluZ3Jlc29zIGRlIGN1ZW50YXMgcXVlIGVtcGllemFuIGNvbiA0CiAgICAgICAgTcOBUyBsb3MgaW5ncmVzb3MgZGUgY3VlbnRhcyBxdWUgZW1waWV6YW4gY29uIDguCiAgICAgICAgIiIiCiAgICAgICAgdHJ5OgogICAgICAgICAgICB3YiA9IG9wZW5weXhsLmxvYWRfd29ya2Jvb2socGF0aCwgZGF0YV9vbmx5PVRydWUpCiAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICByYWlzZSBDb21tYW5kRXJyb3IoZiJObyBzZSBwdWRvIGFicmlyIGVsIGFyY2hpdm8gRXhjZWw6IHtlfSIpCgogICAgICAgIGlmICJEYXRvcyIgbm90IGluIHdiLnNoZWV0bmFtZXM6CiAgICAgICAgICAgIHJhaXNlIENvbW1hbmRFcnJvcigKICAgICAgICAgICAgICAgIGYiRWwgYXJjaGl2byB7cGF0aC5uYW1lfSBubyBjb250aWVuZSBob2phICdEYXRvcycuICIKICAgICAgICAgICAgICAgIGYiSG9qYXMgZGlzcG9uaWJsZXM6IHsnLCAnLmpvaW4od2Iuc2hlZXRuYW1lcyl9IgogICAgICAgICAgICApCgogICAgICAgIHdzID0gd2JbIkRhdG9zIl0KCiAgICAgICAgIyBTdW1hIGN1ZW50YXMgcXVlIGVtcGllemFuIGNvbiA0CiAgICAgICAgc3VtYV80ID0gc2VsZi5fc3VtX2FjY291bnRzX3N0YXJ0aW5nX3dpdGgod3MsIG1vbnRoLCAiNCIpCiAgICAgICAgCiAgICAgICAgIyBTdW1hIGN1ZW50YXMgcXVlIGVtcGllemFuIGNvbiA4CiAgICAgICAgc3VtYV84ID0gc2VsZi5fc3VtX2FjY291bnRzX3N0YXJ0aW5nX3dpdGgod3MsIG1vbnRoLCAiOCIpCgogICAgICAgICMgVG90YWwgPSA0ICsgOAogICAgICAgIHRvdGFsID0gc3VtYV80ICsgc3VtYV84CgogICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKAogICAgICAgICAgICBzZWxmLnN0eWxlLldBUk5JTkcoCiAgICAgICAgICAgICAgICBmIiAgQ3VlbnRhcyAnNCc6IHtzdW1hXzR9IHwgQ3VlbnRhcyAnOCc6IHtzdW1hXzh9IHwgVG90YWw6IHt0b3RhbH0iCiAgICAgICAgICAgICkKICAgICAgICApCgogICAgICAgIHJldHVybiB0b3RhbAoKICAgIGRlZiBfZ2V0X2V4Y2hhbmdlX3JhdGUoc2VsZiwgeWVhcjogaW50LCBtb250aDogaW50KSAtPiBEZWNpbWFsOgogICAgICAgIHRyeToKICAgICAgICAgICAgcmF0ZSA9IE1vbnRobHlFeGNoYW5nZVJhdGUub2JqZWN0cy5nZXQoeWVhcj15ZWFyLCBtb250aD1tb250aCkKICAgICAgICBleGNlcHQgTW9udGhseUV4Y2hhbmdlUmF0ZS5Eb2VzTm90RXhpc3Q6CiAgICAgICAgICAgIHJhaXNlIENvbW1hbmRFcnJvcigKICAgICAgICAgICAgICAgIGYiTm8gZXhpc3RlIHRpcG8gZGUgY2FtYmlvIHBhcmEge3llYXJ9LXttb250aDowMmR9LiAiCiAgICAgICAgICAgICAgICAiRGViZSByZWdpc3RyYXIgTW9udGhseUV4Y2hhbmdlUmF0ZSBhbnRlcyBkZSBpbXBvcnRhciBpbmdyZXNvcy4iCiAgICAgICAgICAgICkKCiAgICAgICAgaWYgcmF0ZS51c2RfdG9fZ3RxIGluIChOb25lLCBEZWNpbWFsKCIwIikpOgogICAgICAgICAgICByYWlzZSBDb21tYW5kRXJyb3IoCiAgICAgICAgICAgICAgICBmIlRpcG8gZGUgY2FtYmlvIGludsOhbGlkbyBwYXJhIHt5ZWFyfS17bW9udGg6MDJkfToge3JhdGUudXNkX3RvX2d0cX0iCiAgICAgICAgICAgICkKCiAgICAgICAgcmV0dXJuIHJhdGUudXNkX3RvX2d0cQoKICAgIEB0cmFuc2FjdGlvbi5hdG9taWMKICAgIGRlZiBoYW5kbGUoc2VsZiwgKmFyZ3MsICoqb3B0aW9ucyk6CiAgICAgICAgcGF0aCA9IFBhdGgob3B0aW9uc1sicGF0aCJdKQogICAgICAgIHllYXIgPSBvcHRpb25zWyJ5ZWFyIl0KICAgICAgICBtb250aCA9IG9wdGlvbnNbIm1vbnRoIl0KCiAgICAgICAgaWYgbm90IHBhdGguZXhpc3RzKCk6CiAgICAgICAgICAgIHJhaXNlIENvbW1hbmRFcnJvcihmIkFyY2hpdm8gbm8gZW5jb250cmFkbzoge3BhdGh9IikKCiAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoCiAgICAgICAgICAgIHNlbGYuc3R5bGUuV0FSTklORyhmIkxleWVuZG8gZXN0YWRvIGRlIHJlc3VsdGFkb3MgZGVzZGUge3BhdGh9IC4uLiIpCiAgICAgICAgKQoKICAgICAgICB0cnk6CiAgICAgICAgICAgIHBsYW4gPSBQR0NQbGFuLm9iamVjdHMuZ2V0KHllYXI9eWVhcikKICAgICAgICBleGNlcHQgUEdDUGxhbi5Eb2VzTm90RXhpc3Q6CiAgICAgICAgICAgIHJhaXNlIENvbW1hbmRFcnJvcihmIk5vIGV4aXN0ZSBQR0NQbGFuIHBhcmEgeWVhcj17eWVhcn0iKQoKICAgICAgICB0cnk6CiAgICAgICAgICAgIG1ldHJpYyA9IE1ldHJpY0RlZmluaXRpb24ub2JqZWN0cy5nZXQoCiAgICAgICAgICAgICAgICBjb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9JTkdSRVNPUwogICAgICAgICAgICApCiAgICAgICAgZXhjZXB0IE1ldHJpY0RlZmluaXRpb24uRG9lc05vdEV4aXN0OgogICAgICAgICAgICByYWlzZSBDb21tYW5kRXJyb3IoIk5vIGV4aXN0ZSBNZXRyaWNEZWZpbml0aW9uIHBhcmEgQ09ERV9JTkdSRVNPUyIpCgogICAgICAgIHVuZSA9IHNlbGYuX2luZmVyX3VuZV9mcm9tX2ZpbGVuYW1lKHBhdGgpCiAgICAgICAgaWYgdW5lLmNvZGUgPT0gIklOVkVTVE1FTlQiOgogICAgICAgICAgICByYWlzZSBDb21tYW5kRXJyb3IoCiAgICAgICAgICAgICAgICAiRXN0ZSBjb21hbmRvIG5vIGRlYmUgdXNhcnNlIHBhcmEgSU5WRVNUTUVOVDsgIgogICAgICAgICAgICAgICAgInBhcmEgZXNhIFVORSB1c2UgZWwgcmVjw6FsY3VsbyBkZXNkZSBOZXdDbGllbnRJbXBvcnRSb3cuIgogICAgICAgICAgICApCgogICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKHNlbGYuc3R5bGUuV0FSTklORyhmIkFyY2hpdm8gZGV0ZWN0YWRvIHBhcmEgVU5FPXt1bmUuY29kZX0iKSkKCiAgICAgICAgaW5ncmVzb19icnV0b19ndHEgPSBzZWxmLl9yZWFkX2luZ3Jlc29fZnJvbV9leGNlbChwYXRoLCBtb250aCkKICAgICAgICAKICAgICAgICBpZiBpbmdyZXNvX2JydXRvX2d0cSBpcyBOb25lOgogICAgICAgICAgICByYWlzZSBDb21tYW5kRXJyb3IoCiAgICAgICAgICAgICAgICBmIl9yZWFkX2luZ3Jlc29fZnJvbV9leGNlbCBkZXZvbHZpw7MgTm9uZSBwYXJhIHtwYXRoLm5hbWV9ICIKICAgICAgICAgICAgICAgIGYiZW4ge3llYXJ9LXttb250aDowMmR9LiIKICAgICAgICAgICAgKQoKICAgICAgICAjIFRFUkNFUk8gZGVsIHBsYW46IEluc3VyYW5jZSB0YW1iacOpbiBzZSBkaXZpZGUgZW50cmUgbWlsCiAgICAgICAgaWYgdW5lLmNvZGUgaW4gKCJGQUNUT1JJTkciLCAiTEVBU0lORyIsICJJTlNVUkFOQ0UiKToKICAgICAgICAgICAgaW5ncmVzb19hanVzdGFkb19ndHEgPSBpbmdyZXNvX2JydXRvX2d0cSAvIERlY2ltYWwoIjEwMDAiKQogICAgICAgIGVsc2U6CiAgICAgICAgICAgIGluZ3Jlc29fYWp1c3RhZG9fZ3RxID0gaW5ncmVzb19icnV0b19ndHEKCiAgICAgICAgdGlwb19jYW1iaW8gPSBzZWxmLl9nZXRfZXhjaGFuZ2VfcmF0ZSh5ZWFyLCBtb250aCkKICAgICAgICBpbmdyZXNvX3VzZCA9IGluZ3Jlc29fYWp1c3RhZG9fZ3RxIC8gdGlwb19jYW1iaW8KCiAgICAgICAgdHJ5OgogICAgICAgICAgICB0YXJnZXQgPSBNb250aGx5VGFyZ2V0Lm9iamVjdHMuZ2V0KAogICAgICAgICAgICAgICAgcGxhbj1wbGFuLAogICAgICAgICAgICAgICAgdW5lPXVuZSwKICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgICAgICAgICBtb250aD1tb250aCwKICAgICAgICAgICAgKQogICAgICAgIGV4Y2VwdCBNb250aGx5VGFyZ2V0LkRvZXNOb3RFeGlzdDoKICAgICAgICAgICAgcmFpc2UgQ29tbWFuZEVycm9yKAogICAgICAgICAgICAgICAgZiJObyBleGlzdGUgTW9udGhseVRhcmdldCBwYXJhIElOR1JFU09TIHt1bmUuY29kZX0gIgogICAgICAgICAgICAgICAgZiJ7eWVhcn0te21vbnRoOjAyZH0uIgogICAgICAgICAgICApCgogICAgICAgIG1tciwgXyA9IE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICBwbGFuPXBsYW4sCiAgICAgICAgICAgIHVuZT11bmUsCiAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgIGRlZmF1bHRzPXsidGFyZ2V0X3ZhbHVlIjogdGFyZ2V0LnRhcmdldF92YWx1ZX0sCiAgICAgICAgKQoKICAgICAgICBtbXIudGFyZ2V0X3ZhbHVlID0gdGFyZ2V0LnRhcmdldF92YWx1ZQogICAgICAgIG1tci5tZWFzdXJlZF92YWx1ZSA9IGluZ3Jlc29fdXNkCgogICAgICAgIG1lYXN1cmVkID0gbW1yLm1lYXN1cmVkX3ZhbHVlIG9yIERlY2ltYWwoIjAiKQogICAgICAgIHRhcmdldF92YWwgPSBtbXIudGFyZ2V0X3ZhbHVlIG9yIERlY2ltYWwoIjAiKQogICAgICAgIGFjaGlldmVkID0gbWVhc3VyZWQgPj0gdGFyZ2V0X3ZhbAoKICAgICAgICBtbXIuaXNfYWNoaWV2ZWQgPSBhY2hpZXZlZAogICAgICAgIG1tci5wb2ludHNfYXdhcmRlZCA9IHRhcmdldC5wb2ludHNfaWZfYWNoaWV2ZWQgaWYgYWNoaWV2ZWQgZWxzZSAwCiAgICAgICAgbW1yLmNhbGN1bGF0aW9uX25vdGUgPSAoCiAgICAgICAgICAgIGYiSW5ncmVzbyBpbXBvcnRhZG8gZGVzZGUge3BhdGgubmFtZX0sIGhvamEgRGF0b3MuICIKICAgICAgICAgICAgZiJCcnV0b0dUUSg0KzgpPXtpbmdyZXNvX2JydXRvX2d0cX0sICIKICAgICAgICAgICAgZiJBanVzdGFkb0dUUT17aW5ncmVzb19hanVzdGFkb19ndHF9LCAiCiAgICAgICAgICAgIGYiVGlwb0NhbWJpb0dUUXhVU0Q9e3RpcG9fY2FtYmlvfSwgIgogICAgICAgICAgICBmIlVTRD17aW5ncmVzb191c2R9LCBVTkU9e3VuZS5jb2RlfS4iCiAgICAgICAgKQogICAgICAgIG1tci5zYXZlKCkKCiAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoCiAgICAgICAgICAgIHNlbGYuc3R5bGUuU1VDQ0VTUygKICAgICAgICAgICAgICAgIGYiQWN0dWFsaXphZG8gSU5HUkVTT1Mge3VuZS5jb2RlfSB7eWVhcn0te21vbnRoOjAyZH06ICIKICAgICAgICAgICAgICAgIGYicmVhbD17bWVhc3VyZWR9IG1ldGE9e3RhcmdldF92YWx9ICIKICAgICAgICAgICAgICAgIGYibG9ncmFkbz17YWNoaWV2ZWR9IHB1bnRvcz17bW1yLnBvaW50c19hd2FyZGVkfSIKICAgICAgICAgICAgKQogICAgICAgICkKICAgICAgICBzZWxmLnN0ZG91dC53cml0ZShzZWxmLnN0eWxlLlNVQ0NFU1MoIkltcG9ydCBJTkdSRVNPUyBjb21wbGV0YWRvLiIpKQ==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/management/commands/import_venta_cruzada.py
PATH_JSON="imports/management/commands/import_venta_cruzada.py"
FILENAME=import_venta_cruzada.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=238
SIZE_BYTES_UTF8=8992
CONTENT_SHA256=999f35d69ead89f082fc9a6b284b23a4152676fede6d17e8495e7c139ddf3fe4
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from core.models import UNE, UNEAlias, MetricDefinition, Currency
from core.services.une_resolve import resolve_une_from_text
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from imports.models import CrossSaleImportHeader, CrossSaleImportRow
from pathlib import Path
from pgc.models import PGCPlan, MonthlyTarget, MonthlyMetricResult
import csv


class Command(BaseCommand):
    help = "Importa archivo de Venta Cruzada y actualiza métricas de VENTA_CRUZADA"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            required=True,
            help="Ruta al archivo de Venta Cruzada (csv/tsv/xlsx->tsv)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.exists():
            raise CommandError(f"Archivo no encontrado: {path}")

        self.stdout.write(self.style.WARNING(f"Leyendo Venta Cruzada desde {path} ..."))

        aliases = {
            a.raw_value.strip().upper(): a.une
            for a in UNEAlias.objects.select_related("une").all()
        }
        unes_by_code = {u.code: u for u in UNE.objects.all()}

        plan = PGCPlan.objects.get(year=2026)
        metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_VENTA_CRUZADA)

        headers_cache = {}
        counts_by_pair = {}
        counts_by_origin = {}  # (year, month, une_origin_id) -> int

        with path.open("r", encoding="utf-8-sig") as f:
            sample = f.read(4096)
            f.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=[",", "\t", ";"])
            except csv.Error:
                delimiter = "\t" if "\t" in sample else ","
                dialect = csv.excel_tab if delimiter == "\t" else csv.excel
          
            reader = csv.DictReader(f, dialect=dialect)

            for row in reader:
                periodo = (
                    row.get("Período")
                    or row.get("Periodo")
                    or row.get("PERIODO")
                    or row.get("periodo")
                )
                if not periodo:
                    continue

                try:
                    year_str, month_str = str(periodo).replace("-", "/").split("/")
                    year = int(year_str)
                    month = int(month_str)
                except Exception:
                    continue

                cliente = (
                    row.get("Cliente")
                    or row.get("CLIENTE")
                    or row.get("cliente")
                    or ""
                ).strip()

                operacion = (
                    row.get("Operación")
                    or row.get("Operacion")
                    or row.get("OPERACION")
                    or row.get("operacion")
                    or ""
                ).strip()

                fecha_raw = (
                    row.get("Fecha")
                    or row.get("FECHA")
                    or row.get("fecha")
                    or ""
                ).strip()

                moneda_raw = (
                    row.get("Moneda")
                    or row.get("MONEDA")
                    or row.get("moneda")
                    or ""
                ).strip().upper()

                une_dest_raw = (
                    row.get("UNE")
                    or row.get("une")
                    or ""
                ).strip()

                une_origin_raw = (
                    row.get("UNE que refiere")
                    or row.get("UNE QUE REFIERE")
                    or row.get("une que refiere")
                    or ""
                ).strip()

                if not une_dest_raw:
                    continue

                une_destination = resolve_une_from_text(
                    une_dest_raw,
                    aliases=aliases,
                    unes_by_code=unes_by_code,
                )

                une_origin = resolve_une_from_text(
                    une_origin_raw,
                    aliases=aliases,
                    unes_by_code=unes_by_code,
                )

                currency = None
                if moneda_raw:
                    currency = Currency.objects.filter(code__iexact=moneda_raw).first()

                header_key = (year, month)
                header = headers_cache.get(header_key)
                if header is None:
                    header = CrossSaleImportHeader.objects.filter(
                        year=year, month=month
                    ).first()
                    if header is None:
                        from imports.models import FileUpload, guess_file_format

                        upload = FileUpload.objects.filter(
                            file_type_detected=FileUpload.TYPE_CROSS_SALE,
                            detected_year=year,
                            detected_month=month,
                        ).order_by("-id").first()
                        if upload is None:
                            upload = FileUpload.objects.create(
                                original_filename=path.name,
                                file_format=guess_file_format(path.name),
                                file_type_detected=FileUpload.TYPE_CROSS_SALE,
                                detected_year=year,
                                detected_month=month,
                                status=FileUpload.STATUS_UPLOADED,
                            )
                            # Adjuntar archivo existente si la ruta es local
                            try:
                                from django.core.files import File as DjFile

                                with path.open("rb") as fh:
                                    upload.stored_file.save(path.name, DjFile(fh), save=True)
                            except Exception:
                                upload.save()
                        header = CrossSaleImportHeader.objects.create(
                            file_upload=upload,
                            year=year,
                            month=month,
                        )
                    headers_cache[header_key] = header

                parsed_date = None
                if fecha_raw:
                    try:
                        parsed_date = datetime.fromisoformat(
                            fecha_raw.replace("Z", "+00:00")
                        ).date()
                    except Exception:
                        try:
                            parsed_date = datetime.strptime(
                                fecha_raw[:10], "%Y-%m-%d"
                            ).date()
                        except Exception:
                            parsed_date = None

                CrossSaleImportRow.objects.create(
                    header=header,
                    year=year,
                    month=month,
                    client_name=cliente,
                    operation_code=operacion,
                    date=parsed_date,
                    currency=currency,
                    une_destination=une_destination,
                    une_origin=une_origin,
                    raw_une_destination=une_dest_raw,
                    raw_une_origin=une_origin_raw,
                )

                if une_origin and une_destination:
                    key_pair = (year, month, une_origin.id, une_destination.id)
                    counts_by_pair[key_pair] = counts_by_pair.get(key_pair, 0) + 1
                
                    key_origin = (year, month, une_origin.id)
                    counts_by_origin[key_origin] = counts_by_origin.get(key_origin, 0) + 1
  
        for (year, month, une_origin_id), count in counts_by_origin.items():
            une_origin = UNE.objects.get(id=une_origin_id)
        
            target = MonthlyTarget.objects.filter(
                plan=plan,
                une=une_origin,
                metric=metric,
                year=year,
                month=month,
            ).first()
        
            target_value = target.target_value if target else Decimal("1")
            is_achieved = Decimal(str(count)) >= target_value
        
            MonthlyMetricResult.objects.update_or_create(
                plan=plan,
                metric=metric,
                une=une_origin,
                year=year,
                month=month,
                defaults={
                    "measured_value": Decimal(str(count)),
                    "target_value": target_value,
                    "is_achieved": is_achieved,
                    "points_awarded": 0,
                    "calculation_note": f"{count} referencias válidas de venta cruzada en el mes",
                },
            )

        self.stdout.write(self.style.SUCCESS("Venta cruzada importada correctamente."))
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from core.models import UNE, UNEAlias, MetricDefinition, Currency
00002|from core.services.une_resolve import resolve_une_from_text
00003|from datetime import datetime
00004|from decimal import Decimal
00005|from django.core.management.base import BaseCommand, CommandError
00006|from django.db import transaction
00007|from imports.models import CrossSaleImportHeader, CrossSaleImportRow
00008|from pathlib import Path
00009|from pgc.models import PGCPlan, MonthlyTarget, MonthlyMetricResult
00010|import csv
00011|
00012|
00013|class Command(BaseCommand):
00014|    help = "Importa archivo de Venta Cruzada y actualiza métricas de VENTA_CRUZADA"
00015|
00016|    def add_arguments(self, parser):
00017|        parser.add_argument(
00018|            "--path",
00019|            type=str,
00020|            required=True,
00021|            help="Ruta al archivo de Venta Cruzada (csv/tsv/xlsx->tsv)",
00022|        )
00023|
00024|    @transaction.atomic
00025|    def handle(self, *args, **options):
00026|        path = Path(options["path"])
00027|        if not path.exists():
00028|            raise CommandError(f"Archivo no encontrado: {path}")
00029|
00030|        self.stdout.write(self.style.WARNING(f"Leyendo Venta Cruzada desde {path} ..."))
00031|
00032|        aliases = {
00033|            a.raw_value.strip().upper(): a.une
00034|            for a in UNEAlias.objects.select_related("une").all()
00035|        }
00036|        unes_by_code = {u.code: u for u in UNE.objects.all()}
00037|
00038|        plan = PGCPlan.objects.get(year=2026)
00039|        metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_VENTA_CRUZADA)
00040|
00041|        headers_cache = {}
00042|        counts_by_pair = {}
00043|        counts_by_origin = {}  # (year, month, une_origin_id) -> int
00044|
00045|        with path.open("r", encoding="utf-8-sig") as f:
00046|            sample = f.read(4096)
00047|            f.seek(0)
00048|
00049|            try:
00050|                dialect = csv.Sniffer().sniff(sample, delimiters=[",", "\t", ";"])
00051|            except csv.Error:
00052|                delimiter = "\t" if "\t" in sample else ","
00053|                dialect = csv.excel_tab if delimiter == "\t" else csv.excel
00054|          
00055|            reader = csv.DictReader(f, dialect=dialect)
00056|
00057|            for row in reader:
00058|                periodo = (
00059|                    row.get("Período")
00060|                    or row.get("Periodo")
00061|                    or row.get("PERIODO")
00062|                    or row.get("periodo")
00063|                )
00064|                if not periodo:
00065|                    continue
00066|
00067|                try:
00068|                    year_str, month_str = str(periodo).replace("-", "/").split("/")
00069|                    year = int(year_str)
00070|                    month = int(month_str)
00071|                except Exception:
00072|                    continue
00073|
00074|                cliente = (
00075|                    row.get("Cliente")
00076|                    or row.get("CLIENTE")
00077|                    or row.get("cliente")
00078|                    or ""
00079|                ).strip()
00080|
00081|                operacion = (
00082|                    row.get("Operación")
00083|                    or row.get("Operacion")
00084|                    or row.get("OPERACION")
00085|                    or row.get("operacion")
00086|                    or ""
00087|                ).strip()
00088|
00089|                fecha_raw = (
00090|                    row.get("Fecha")
00091|                    or row.get("FECHA")
00092|                    or row.get("fecha")
00093|                    or ""
00094|                ).strip()
00095|
00096|                moneda_raw = (
00097|                    row.get("Moneda")
00098|                    or row.get("MONEDA")
00099|                    or row.get("moneda")
00100|                    or ""
00101|                ).strip().upper()
00102|
00103|                une_dest_raw = (
00104|                    row.get("UNE")
00105|                    or row.get("une")
00106|                    or ""
00107|                ).strip()
00108|
00109|                une_origin_raw = (
00110|                    row.get("UNE que refiere")
00111|                    or row.get("UNE QUE REFIERE")
00112|                    or row.get("une que refiere")
00113|                    or ""
00114|                ).strip()
00115|
00116|                if not une_dest_raw:
00117|                    continue
00118|
00119|                une_destination = resolve_une_from_text(
00120|                    une_dest_raw,
00121|                    aliases=aliases,
00122|                    unes_by_code=unes_by_code,
00123|                )
00124|
00125|                une_origin = resolve_une_from_text(
00126|                    une_origin_raw,
00127|                    aliases=aliases,
00128|                    unes_by_code=unes_by_code,
00129|                )
00130|
00131|                currency = None
00132|                if moneda_raw:
00133|                    currency = Currency.objects.filter(code__iexact=moneda_raw).first()
00134|
00135|                header_key = (year, month)
00136|                header = headers_cache.get(header_key)
00137|                if header is None:
00138|                    header = CrossSaleImportHeader.objects.filter(
00139|                        year=year, month=month
00140|                    ).first()
00141|                    if header is None:
00142|                        from imports.models import FileUpload, guess_file_format
00143|
00144|                        upload = FileUpload.objects.filter(
00145|                            file_type_detected=FileUpload.TYPE_CROSS_SALE,
00146|                            detected_year=year,
00147|                            detected_month=month,
00148|                        ).order_by("-id").first()
00149|                        if upload is None:
00150|                            upload = FileUpload.objects.create(
00151|                                original_filename=path.name,
00152|                                file_format=guess_file_format(path.name),
00153|                                file_type_detected=FileUpload.TYPE_CROSS_SALE,
00154|                                detected_year=year,
00155|                                detected_month=month,
00156|                                status=FileUpload.STATUS_UPLOADED,
00157|                            )
00158|                            # Adjuntar archivo existente si la ruta es local
00159|                            try:
00160|                                from django.core.files import File as DjFile
00161|
00162|                                with path.open("rb") as fh:
00163|                                    upload.stored_file.save(path.name, DjFile(fh), save=True)
00164|                            except Exception:
00165|                                upload.save()
00166|                        header = CrossSaleImportHeader.objects.create(
00167|                            file_upload=upload,
00168|                            year=year,
00169|                            month=month,
00170|                        )
00171|                    headers_cache[header_key] = header
00172|
00173|                parsed_date = None
00174|                if fecha_raw:
00175|                    try:
00176|                        parsed_date = datetime.fromisoformat(
00177|                            fecha_raw.replace("Z", "+00:00")
00178|                        ).date()
00179|                    except Exception:
00180|                        try:
00181|                            parsed_date = datetime.strptime(
00182|                                fecha_raw[:10], "%Y-%m-%d"
00183|                            ).date()
00184|                        except Exception:
00185|                            parsed_date = None
00186|
00187|                CrossSaleImportRow.objects.create(
00188|                    header=header,
00189|                    year=year,
00190|                    month=month,
00191|                    client_name=cliente,
00192|                    operation_code=operacion,
00193|                    date=parsed_date,
00194|                    currency=currency,
00195|                    une_destination=une_destination,
00196|                    une_origin=une_origin,
00197|                    raw_une_destination=une_dest_raw,
00198|                    raw_une_origin=une_origin_raw,
00199|                )
00200|
00201|                if une_origin and une_destination:
00202|                    key_pair = (year, month, une_origin.id, une_destination.id)
00203|                    counts_by_pair[key_pair] = counts_by_pair.get(key_pair, 0) + 1
00204|                
00205|                    key_origin = (year, month, une_origin.id)
00206|                    counts_by_origin[key_origin] = counts_by_origin.get(key_origin, 0) + 1
00207|  
00208|        for (year, month, une_origin_id), count in counts_by_origin.items():
00209|            une_origin = UNE.objects.get(id=une_origin_id)
00210|        
00211|            target = MonthlyTarget.objects.filter(
00212|                plan=plan,
00213|                une=une_origin,
00214|                metric=metric,
00215|                year=year,
00216|                month=month,
00217|            ).first()
00218|        
00219|            target_value = target.target_value if target else Decimal("1")
00220|            is_achieved = Decimal(str(count)) >= target_value
00221|        
00222|            MonthlyMetricResult.objects.update_or_create(
00223|                plan=plan,
00224|                metric=metric,
00225|                une=une_origin,
00226|                year=year,
00227|                month=month,
00228|                defaults={
00229|                    "measured_value": Decimal(str(count)),
00230|                    "target_value": target_value,
00231|                    "is_achieved": is_achieved,
00232|                    "points_awarded": 0,
00233|                    "calculation_note": f"{count} referencias válidas de venta cruzada en el mes",
00234|                },
00235|            )
00236|
00237|        self.stdout.write(self.style.SUCCESS("Venta cruzada importada correctamente."))
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBjb3JlLm1vZGVscyBpbXBvcnQgVU5FLCBVTkVBbGlhcywgTWV0cmljRGVmaW5pdGlvbiwgQ3VycmVuY3kKZnJvbSBjb3JlLnNlcnZpY2VzLnVuZV9yZXNvbHZlIGltcG9ydCByZXNvbHZlX3VuZV9mcm9tX3RleHQKZnJvbSBkYXRldGltZSBpbXBvcnQgZGF0ZXRpbWUKZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsCmZyb20gZGphbmdvLmNvcmUubWFuYWdlbWVudC5iYXNlIGltcG9ydCBCYXNlQ29tbWFuZCwgQ29tbWFuZEVycm9yCmZyb20gZGphbmdvLmRiIGltcG9ydCB0cmFuc2FjdGlvbgpmcm9tIGltcG9ydHMubW9kZWxzIGltcG9ydCBDcm9zc1NhbGVJbXBvcnRIZWFkZXIsIENyb3NzU2FsZUltcG9ydFJvdwpmcm9tIHBhdGhsaWIgaW1wb3J0IFBhdGgKZnJvbSBwZ2MubW9kZWxzIGltcG9ydCBQR0NQbGFuLCBNb250aGx5VGFyZ2V0LCBNb250aGx5TWV0cmljUmVzdWx0CmltcG9ydCBjc3YKCgpjbGFzcyBDb21tYW5kKEJhc2VDb21tYW5kKToKICAgIGhlbHAgPSAiSW1wb3J0YSBhcmNoaXZvIGRlIFZlbnRhIENydXphZGEgeSBhY3R1YWxpemEgbcOpdHJpY2FzIGRlIFZFTlRBX0NSVVpBREEiCgogICAgZGVmIGFkZF9hcmd1bWVudHMoc2VsZiwgcGFyc2VyKToKICAgICAgICBwYXJzZXIuYWRkX2FyZ3VtZW50KAogICAgICAgICAgICAiLS1wYXRoIiwKICAgICAgICAgICAgdHlwZT1zdHIsCiAgICAgICAgICAgIHJlcXVpcmVkPVRydWUsCiAgICAgICAgICAgIGhlbHA9IlJ1dGEgYWwgYXJjaGl2byBkZSBWZW50YSBDcnV6YWRhIChjc3YvdHN2L3hsc3gtPnRzdikiLAogICAgICAgICkKCiAgICBAdHJhbnNhY3Rpb24uYXRvbWljCiAgICBkZWYgaGFuZGxlKHNlbGYsICphcmdzLCAqKm9wdGlvbnMpOgogICAgICAgIHBhdGggPSBQYXRoKG9wdGlvbnNbInBhdGgiXSkKICAgICAgICBpZiBub3QgcGF0aC5leGlzdHMoKToKICAgICAgICAgICAgcmFpc2UgQ29tbWFuZEVycm9yKGYiQXJjaGl2byBubyBlbmNvbnRyYWRvOiB7cGF0aH0iKQoKICAgICAgICBzZWxmLnN0ZG91dC53cml0ZShzZWxmLnN0eWxlLldBUk5JTkcoZiJMZXllbmRvIFZlbnRhIENydXphZGEgZGVzZGUge3BhdGh9IC4uLiIpKQoKICAgICAgICBhbGlhc2VzID0gewogICAgICAgICAgICBhLnJhd192YWx1ZS5zdHJpcCgpLnVwcGVyKCk6IGEudW5lCiAgICAgICAgICAgIGZvciBhIGluIFVORUFsaWFzLm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoInVuZSIpLmFsbCgpCiAgICAgICAgfQogICAgICAgIHVuZXNfYnlfY29kZSA9IHt1LmNvZGU6IHUgZm9yIHUgaW4gVU5FLm9iamVjdHMuYWxsKCl9CgogICAgICAgIHBsYW4gPSBQR0NQbGFuLm9iamVjdHMuZ2V0KHllYXI9MjAyNikKICAgICAgICBtZXRyaWMgPSBNZXRyaWNEZWZpbml0aW9uLm9iamVjdHMuZ2V0KGNvZGU9TWV0cmljRGVmaW5pdGlvbi5DT0RFX1ZFTlRBX0NSVVpBREEpCgogICAgICAgIGhlYWRlcnNfY2FjaGUgPSB7fQogICAgICAgIGNvdW50c19ieV9wYWlyID0ge30KICAgICAgICBjb3VudHNfYnlfb3JpZ2luID0ge30gICMgKHllYXIsIG1vbnRoLCB1bmVfb3JpZ2luX2lkKSAtPiBpbnQKCiAgICAgICAgd2l0aCBwYXRoLm9wZW4oInIiLCBlbmNvZGluZz0idXRmLTgtc2lnIikgYXMgZjoKICAgICAgICAgICAgc2FtcGxlID0gZi5yZWFkKDQwOTYpCiAgICAgICAgICAgIGYuc2VlaygwKQoKICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgZGlhbGVjdCA9IGNzdi5TbmlmZmVyKCkuc25pZmYoc2FtcGxlLCBkZWxpbWl0ZXJzPVsiLCIsICJcdCIsICI7Il0pCiAgICAgICAgICAgIGV4Y2VwdCBjc3YuRXJyb3I6CiAgICAgICAgICAgICAgICBkZWxpbWl0ZXIgPSAiXHQiIGlmICJcdCIgaW4gc2FtcGxlIGVsc2UgIiwiCiAgICAgICAgICAgICAgICBkaWFsZWN0ID0gY3N2LmV4Y2VsX3RhYiBpZiBkZWxpbWl0ZXIgPT0gIlx0IiBlbHNlIGNzdi5leGNlbAogICAgICAgICAgCiAgICAgICAgICAgIHJlYWRlciA9IGNzdi5EaWN0UmVhZGVyKGYsIGRpYWxlY3Q9ZGlhbGVjdCkKCiAgICAgICAgICAgIGZvciByb3cgaW4gcmVhZGVyOgogICAgICAgICAgICAgICAgcGVyaW9kbyA9ICgKICAgICAgICAgICAgICAgICAgICByb3cuZ2V0KCJQZXLDrW9kbyIpCiAgICAgICAgICAgICAgICAgICAgb3Igcm93LmdldCgiUGVyaW9kbyIpCiAgICAgICAgICAgICAgICAgICAgb3Igcm93LmdldCgiUEVSSU9ETyIpCiAgICAgICAgICAgICAgICAgICAgb3Igcm93LmdldCgicGVyaW9kbyIpCiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICBpZiBub3QgcGVyaW9kbzoKICAgICAgICAgICAgICAgICAgICBjb250aW51ZQoKICAgICAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgICAgICB5ZWFyX3N0ciwgbW9udGhfc3RyID0gc3RyKHBlcmlvZG8pLnJlcGxhY2UoIi0iLCAiLyIpLnNwbGl0KCIvIikKICAgICAgICAgICAgICAgICAgICB5ZWFyID0gaW50KHllYXJfc3RyKQogICAgICAgICAgICAgICAgICAgIG1vbnRoID0gaW50KG1vbnRoX3N0cikKICAgICAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgICAgICAgICAgICAgY29udGludWUKCiAgICAgICAgICAgICAgICBjbGllbnRlID0gKAogICAgICAgICAgICAgICAgICAgIHJvdy5nZXQoIkNsaWVudGUiKQogICAgICAgICAgICAgICAgICAgIG9yIHJvdy5nZXQoIkNMSUVOVEUiKQogICAgICAgICAgICAgICAgICAgIG9yIHJvdy5nZXQoImNsaWVudGUiKQogICAgICAgICAgICAgICAgICAgIG9yICIiCiAgICAgICAgICAgICAgICApLnN0cmlwKCkKCiAgICAgICAgICAgICAgICBvcGVyYWNpb24gPSAoCiAgICAgICAgICAgICAgICAgICAgcm93LmdldCgiT3BlcmFjacOzbiIpCiAgICAgICAgICAgICAgICAgICAgb3Igcm93LmdldCgiT3BlcmFjaW9uIikKICAgICAgICAgICAgICAgICAgICBvciByb3cuZ2V0KCJPUEVSQUNJT04iKQogICAgICAgICAgICAgICAgICAgIG9yIHJvdy5nZXQoIm9wZXJhY2lvbiIpCiAgICAgICAgICAgICAgICAgICAgb3IgIiIKICAgICAgICAgICAgICAgICkuc3RyaXAoKQoKICAgICAgICAgICAgICAgIGZlY2hhX3JhdyA9ICgKICAgICAgICAgICAgICAgICAgICByb3cuZ2V0KCJGZWNoYSIpCiAgICAgICAgICAgICAgICAgICAgb3Igcm93LmdldCgiRkVDSEEiKQogICAgICAgICAgICAgICAgICAgIG9yIHJvdy5nZXQoImZlY2hhIikKICAgICAgICAgICAgICAgICAgICBvciAiIgogICAgICAgICAgICAgICAgKS5zdHJpcCgpCgogICAgICAgICAgICAgICAgbW9uZWRhX3JhdyA9ICgKICAgICAgICAgICAgICAgICAgICByb3cuZ2V0KCJNb25lZGEiKQogICAgICAgICAgICAgICAgICAgIG9yIHJvdy5nZXQoIk1PTkVEQSIpCiAgICAgICAgICAgICAgICAgICAgb3Igcm93LmdldCgibW9uZWRhIikKICAgICAgICAgICAgICAgICAgICBvciAiIgogICAgICAgICAgICAgICAgKS5zdHJpcCgpLnVwcGVyKCkKCiAgICAgICAgICAgICAgICB1bmVfZGVzdF9yYXcgPSAoCiAgICAgICAgICAgICAgICAgICAgcm93LmdldCgiVU5FIikKICAgICAgICAgICAgICAgICAgICBvciByb3cuZ2V0KCJ1bmUiKQogICAgICAgICAgICAgICAgICAgIG9yICIiCiAgICAgICAgICAgICAgICApLnN0cmlwKCkKCiAgICAgICAgICAgICAgICB1bmVfb3JpZ2luX3JhdyA9ICgKICAgICAgICAgICAgICAgICAgICByb3cuZ2V0KCJVTkUgcXVlIHJlZmllcmUiKQogICAgICAgICAgICAgICAgICAgIG9yIHJvdy5nZXQoIlVORSBRVUUgUkVGSUVSRSIpCiAgICAgICAgICAgICAgICAgICAgb3Igcm93LmdldCgidW5lIHF1ZSByZWZpZXJlIikKICAgICAgICAgICAgICAgICAgICBvciAiIgogICAgICAgICAgICAgICAgKS5zdHJpcCgpCgogICAgICAgICAgICAgICAgaWYgbm90IHVuZV9kZXN0X3JhdzoKICAgICAgICAgICAgICAgICAgICBjb250aW51ZQoKICAgICAgICAgICAgICAgIHVuZV9kZXN0aW5hdGlvbiA9IHJlc29sdmVfdW5lX2Zyb21fdGV4dCgKICAgICAgICAgICAgICAgICAgICB1bmVfZGVzdF9yYXcsCiAgICAgICAgICAgICAgICAgICAgYWxpYXNlcz1hbGlhc2VzLAogICAgICAgICAgICAgICAgICAgIHVuZXNfYnlfY29kZT11bmVzX2J5X2NvZGUsCiAgICAgICAgICAgICAgICApCgogICAgICAgICAgICAgICAgdW5lX29yaWdpbiA9IHJlc29sdmVfdW5lX2Zyb21fdGV4dCgKICAgICAgICAgICAgICAgICAgICB1bmVfb3JpZ2luX3JhdywKICAgICAgICAgICAgICAgICAgICBhbGlhc2VzPWFsaWFzZXMsCiAgICAgICAgICAgICAgICAgICAgdW5lc19ieV9jb2RlPXVuZXNfYnlfY29kZSwKICAgICAgICAgICAgICAgICkKCiAgICAgICAgICAgICAgICBjdXJyZW5jeSA9IE5vbmUKICAgICAgICAgICAgICAgIGlmIG1vbmVkYV9yYXc6CiAgICAgICAgICAgICAgICAgICAgY3VycmVuY3kgPSBDdXJyZW5jeS5vYmplY3RzLmZpbHRlcihjb2RlX19pZXhhY3Q9bW9uZWRhX3JhdykuZmlyc3QoKQoKICAgICAgICAgICAgICAgIGhlYWRlcl9rZXkgPSAoeWVhciwgbW9udGgpCiAgICAgICAgICAgICAgICBoZWFkZXIgPSBoZWFkZXJzX2NhY2hlLmdldChoZWFkZXJfa2V5KQogICAgICAgICAgICAgICAgaWYgaGVhZGVyIGlzIE5vbmU6CiAgICAgICAgICAgICAgICAgICAgaGVhZGVyID0gQ3Jvc3NTYWxlSW1wb3J0SGVhZGVyLm9iamVjdHMuZmlsdGVyKAogICAgICAgICAgICAgICAgICAgICAgICB5ZWFyPXllYXIsIG1vbnRoPW1vbnRoCiAgICAgICAgICAgICAgICAgICAgKS5maXJzdCgpCiAgICAgICAgICAgICAgICAgICAgaWYgaGVhZGVyIGlzIE5vbmU6CiAgICAgICAgICAgICAgICAgICAgICAgIGZyb20gaW1wb3J0cy5tb2RlbHMgaW1wb3J0IEZpbGVVcGxvYWQsIGd1ZXNzX2ZpbGVfZm9ybWF0CgogICAgICAgICAgICAgICAgICAgICAgICB1cGxvYWQgPSBGaWxlVXBsb2FkLm9iamVjdHMuZmlsdGVyKAogICAgICAgICAgICAgICAgICAgICAgICAgICAgZmlsZV90eXBlX2RldGVjdGVkPUZpbGVVcGxvYWQuVFlQRV9DUk9TU19TQUxFLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgZGV0ZWN0ZWRfeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgZGV0ZWN0ZWRfbW9udGg9bW9udGgsCiAgICAgICAgICAgICAgICAgICAgICAgICkub3JkZXJfYnkoIi1pZCIpLmZpcnN0KCkKICAgICAgICAgICAgICAgICAgICAgICAgaWYgdXBsb2FkIGlzIE5vbmU6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB1cGxvYWQgPSBGaWxlVXBsb2FkLm9iamVjdHMuY3JlYXRlKAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG9yaWdpbmFsX2ZpbGVuYW1lPXBhdGgubmFtZSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBmaWxlX2Zvcm1hdD1ndWVzc19maWxlX2Zvcm1hdChwYXRoLm5hbWUpLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGZpbGVfdHlwZV9kZXRlY3RlZD1GaWxlVXBsb2FkLlRZUEVfQ1JPU1NfU0FMRSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkZXRlY3RlZF95ZWFyPXllYXIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZGV0ZWN0ZWRfbW9udGg9bW9udGgsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc3RhdHVzPUZpbGVVcGxvYWQuU1RBVFVTX1VQTE9BREVELAogICAgICAgICAgICAgICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgICAgICAgICAgICAgIyBBZGp1bnRhciBhcmNoaXZvIGV4aXN0ZW50ZSBzaSBsYSBydXRhIGVzIGxvY2FsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZnJvbSBkamFuZ28uY29yZS5maWxlcyBpbXBvcnQgRmlsZSBhcyBEakZpbGUKCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgd2l0aCBwYXRoLm9wZW4oInJiIikgYXMgZmg6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHVwbG9hZC5zdG9yZWRfZmlsZS5zYXZlKHBhdGgubmFtZSwgRGpGaWxlKGZoKSwgc2F2ZT1UcnVlKQogICAgICAgICAgICAgICAgICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB1cGxvYWQuc2F2ZSgpCiAgICAgICAgICAgICAgICAgICAgICAgIGhlYWRlciA9IENyb3NzU2FsZUltcG9ydEhlYWRlci5vYmplY3RzLmNyZWF0ZSgKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGZpbGVfdXBsb2FkPXVwbG9hZCwKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAgICAgaGVhZGVyc19jYWNoZVtoZWFkZXJfa2V5XSA9IGhlYWRlcgoKICAgICAgICAgICAgICAgIHBhcnNlZF9kYXRlID0gTm9uZQogICAgICAgICAgICAgICAgaWYgZmVjaGFfcmF3OgogICAgICAgICAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgICAgICAgICAgcGFyc2VkX2RhdGUgPSBkYXRldGltZS5mcm9taXNvZm9ybWF0KAogICAgICAgICAgICAgICAgICAgICAgICAgICAgZmVjaGFfcmF3LnJlcGxhY2UoIloiLCAiKzAwOjAwIikKICAgICAgICAgICAgICAgICAgICAgICAgKS5kYXRlKCkKICAgICAgICAgICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uOgogICAgICAgICAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBwYXJzZWRfZGF0ZSA9IGRhdGV0aW1lLnN0cnB0aW1lKAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGZlY2hhX3Jhd1s6MTBdLCAiJVktJW0tJWQiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICApLmRhdGUoKQogICAgICAgICAgICAgICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uOgogICAgICAgICAgICAgICAgICAgICAgICAgICAgcGFyc2VkX2RhdGUgPSBOb25lCgogICAgICAgICAgICAgICAgQ3Jvc3NTYWxlSW1wb3J0Um93Lm9iamVjdHMuY3JlYXRlKAogICAgICAgICAgICAgICAgICAgIGhlYWRlcj1oZWFkZXIsCiAgICAgICAgICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgICAgIGNsaWVudF9uYW1lPWNsaWVudGUsCiAgICAgICAgICAgICAgICAgICAgb3BlcmF0aW9uX2NvZGU9b3BlcmFjaW9uLAogICAgICAgICAgICAgICAgICAgIGRhdGU9cGFyc2VkX2RhdGUsCiAgICAgICAgICAgICAgICAgICAgY3VycmVuY3k9Y3VycmVuY3ksCiAgICAgICAgICAgICAgICAgICAgdW5lX2Rlc3RpbmF0aW9uPXVuZV9kZXN0aW5hdGlvbiwKICAgICAgICAgICAgICAgICAgICB1bmVfb3JpZ2luPXVuZV9vcmlnaW4sCiAgICAgICAgICAgICAgICAgICAgcmF3X3VuZV9kZXN0aW5hdGlvbj11bmVfZGVzdF9yYXcsCiAgICAgICAgICAgICAgICAgICAgcmF3X3VuZV9vcmlnaW49dW5lX29yaWdpbl9yYXcsCiAgICAgICAgICAgICAgICApCgogICAgICAgICAgICAgICAgaWYgdW5lX29yaWdpbiBhbmQgdW5lX2Rlc3RpbmF0aW9uOgogICAgICAgICAgICAgICAgICAgIGtleV9wYWlyID0gKHllYXIsIG1vbnRoLCB1bmVfb3JpZ2luLmlkLCB1bmVfZGVzdGluYXRpb24uaWQpCiAgICAgICAgICAgICAgICAgICAgY291bnRzX2J5X3BhaXJba2V5X3BhaXJdID0gY291bnRzX2J5X3BhaXIuZ2V0KGtleV9wYWlyLCAwKSArIDEKICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIGtleV9vcmlnaW4gPSAoeWVhciwgbW9udGgsIHVuZV9vcmlnaW4uaWQpCiAgICAgICAgICAgICAgICAgICAgY291bnRzX2J5X29yaWdpbltrZXlfb3JpZ2luXSA9IGNvdW50c19ieV9vcmlnaW4uZ2V0KGtleV9vcmlnaW4sIDApICsgMQogIAogICAgICAgIGZvciAoeWVhciwgbW9udGgsIHVuZV9vcmlnaW5faWQpLCBjb3VudCBpbiBjb3VudHNfYnlfb3JpZ2luLml0ZW1zKCk6CiAgICAgICAgICAgIHVuZV9vcmlnaW4gPSBVTkUub2JqZWN0cy5nZXQoaWQ9dW5lX29yaWdpbl9pZCkKICAgICAgICAKICAgICAgICAgICAgdGFyZ2V0ID0gTW9udGhseVRhcmdldC5vYmplY3RzLmZpbHRlcigKICAgICAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgICAgIHVuZT11bmVfb3JpZ2luLAogICAgICAgICAgICAgICAgbWV0cmljPW1ldHJpYywKICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICApLmZpcnN0KCkKICAgICAgICAKICAgICAgICAgICAgdGFyZ2V0X3ZhbHVlID0gdGFyZ2V0LnRhcmdldF92YWx1ZSBpZiB0YXJnZXQgZWxzZSBEZWNpbWFsKCIxIikKICAgICAgICAgICAgaXNfYWNoaWV2ZWQgPSBEZWNpbWFsKHN0cihjb3VudCkpID49IHRhcmdldF92YWx1ZQogICAgICAgIAogICAgICAgICAgICBNb250aGx5TWV0cmljUmVzdWx0Lm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICB1bmU9dW5lX29yaWdpbiwKICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgICAgICJtZWFzdXJlZF92YWx1ZSI6IERlY2ltYWwoc3RyKGNvdW50KSksCiAgICAgICAgICAgICAgICAgICAgInRhcmdldF92YWx1ZSI6IHRhcmdldF92YWx1ZSwKICAgICAgICAgICAgICAgICAgICAiaXNfYWNoaWV2ZWQiOiBpc19hY2hpZXZlZCwKICAgICAgICAgICAgICAgICAgICAicG9pbnRzX2F3YXJkZWQiOiAwLAogICAgICAgICAgICAgICAgICAgICJjYWxjdWxhdGlvbl9ub3RlIjogZiJ7Y291bnR9IHJlZmVyZW5jaWFzIHbDoWxpZGFzIGRlIHZlbnRhIGNydXphZGEgZW4gZWwgbWVzIiwKICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICkKCiAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoc2VsZi5zdHlsZS5TVUNDRVNTKCJWZW50YSBjcnV6YWRhIGltcG9ydGFkYSBjb3JyZWN0YW1lbnRlLiIpKQ==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/management/commands/load_wcg_data.py
PATH_JSON="imports/management/commands/load_wcg_data.py"
FILENAME=load_wcg_data.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=76
SIZE_BYTES_UTF8=2967
CONTENT_SHA256=1b8900812242f789ae94fd83e96b80d8ab480ca74d796661e3feb54be6c19067
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Carga los archivos de demo desde el directorio data/ hacia los módulos WCG."""

from __future__ import annotations

from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from imports.dispatch import run_import_path
from pgo.periodo import recalculate_pgo_periodos

User = get_user_model()

# Orden importa: CRM y leasing base antes de rentas
DEFAULT_FILES = [
    ("crm datos - InfoClientesWCG para CRM.csv", None),
    ("pgo datos - control de tickets marzo abril y mayo 2026 para PGO.xlsx", "pgo_tickets"),
    ("pgo datos - Archivos para PGO.csv", "pgo_catalogo"),
    ("BaseLeasing202606.csv", "risk_leasing"),
    ("balon datos - BaseLeasing202605.csv", "risk_leasing"),
    ("LeasingRentas2026-06-30.csv", "risk_rentas"),
]


class Command(BaseCommand):
    help = "Importa archivos de /wcg4/data o demo_data/ vía Importación General"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir",
            default="",
            help="Directorio de datos (default: demo_data/ o ../data)",
        )
        parser.add_argument("--user", default="", help="Username que registra los lotes")

    def handle(self, *args, **options):
        base = Path(options["dir"]) if options["dir"] else self._default_data_dir()
        if not base.exists():
            self.stderr.write(self.style.ERROR(f"No existe directorio: {base}"))
            return

        user = None
        if options["user"]:
            user = User.objects.filter(username=options["user"]).first()
        user = user or User.objects.filter(is_superuser=True).first() or User.objects.first()
        if not user:
            self.stderr.write(self.style.ERROR("No hay usuario para asociar lotes."))
            return

        self.stdout.write(f"Importando desde {base} como {user.username}")
        for filename, forced in DEFAULT_FILES:
            path = base / filename
            if not path.exists():
                self.stdout.write(self.style.WARNING(f"  skip (no encontrado): {filename}"))
                continue
            result = run_import_path(user, str(path), tipo_forzado=forced)
            style = self.style.SUCCESS if result.ok else self.style.WARNING
            self.stdout.write(style(f"  [{result.tipo}] {filename}: {result.message}"))

        recalculate_pgo_periodos()
        self.stdout.write(self.style.SUCCESS("Recálculo PGO OK. Importación general finalizada."))

    def _default_data_dir(self) -> Path:
        here = Path(__file__).resolve()
        candidates = [
            here.parents[3] / "demo_data",  # dashboard/demo_data (deploy)
            here.parents[4] / "data",  # /wc/wcg4/data
            here.parents[3] / "data" / "wcg",
            Path("/app/demo_data"),
            Path("/home/caa/wc/wcg4/data"),
        ]
        for c in candidates:
            if c.exists():
                return c
        return candidates[0]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Carga los archivos de demo desde el directorio data/ hacia los módulos WCG."""
00002|
00003|from __future__ import annotations
00004|
00005|from pathlib import Path
00006|
00007|from django.contrib.auth import get_user_model
00008|from django.core.management.base import BaseCommand
00009|
00010|from imports.dispatch import run_import_path
00011|from pgo.periodo import recalculate_pgo_periodos
00012|
00013|User = get_user_model()
00014|
00015|# Orden importa: CRM y leasing base antes de rentas
00016|DEFAULT_FILES = [
00017|    ("crm datos - InfoClientesWCG para CRM.csv", None),
00018|    ("pgo datos - control de tickets marzo abril y mayo 2026 para PGO.xlsx", "pgo_tickets"),
00019|    ("pgo datos - Archivos para PGO.csv", "pgo_catalogo"),
00020|    ("BaseLeasing202606.csv", "risk_leasing"),
00021|    ("balon datos - BaseLeasing202605.csv", "risk_leasing"),
00022|    ("LeasingRentas2026-06-30.csv", "risk_rentas"),
00023|]
00024|
00025|
00026|class Command(BaseCommand):
00027|    help = "Importa archivos de /wcg4/data o demo_data/ vía Importación General"
00028|
00029|    def add_arguments(self, parser):
00030|        parser.add_argument(
00031|            "--dir",
00032|            default="",
00033|            help="Directorio de datos (default: demo_data/ o ../data)",
00034|        )
00035|        parser.add_argument("--user", default="", help="Username que registra los lotes")
00036|
00037|    def handle(self, *args, **options):
00038|        base = Path(options["dir"]) if options["dir"] else self._default_data_dir()
00039|        if not base.exists():
00040|            self.stderr.write(self.style.ERROR(f"No existe directorio: {base}"))
00041|            return
00042|
00043|        user = None
00044|        if options["user"]:
00045|            user = User.objects.filter(username=options["user"]).first()
00046|        user = user or User.objects.filter(is_superuser=True).first() or User.objects.first()
00047|        if not user:
00048|            self.stderr.write(self.style.ERROR("No hay usuario para asociar lotes."))
00049|            return
00050|
00051|        self.stdout.write(f"Importando desde {base} como {user.username}")
00052|        for filename, forced in DEFAULT_FILES:
00053|            path = base / filename
00054|            if not path.exists():
00055|                self.stdout.write(self.style.WARNING(f"  skip (no encontrado): {filename}"))
00056|                continue
00057|            result = run_import_path(user, str(path), tipo_forzado=forced)
00058|            style = self.style.SUCCESS if result.ok else self.style.WARNING
00059|            self.stdout.write(style(f"  [{result.tipo}] {filename}: {result.message}"))
00060|
00061|        recalculate_pgo_periodos()
00062|        self.stdout.write(self.style.SUCCESS("Recálculo PGO OK. Importación general finalizada."))
00063|
00064|    def _default_data_dir(self) -> Path:
00065|        here = Path(__file__).resolve()
00066|        candidates = [
00067|            here.parents[3] / "demo_data",  # dashboard/demo_data (deploy)
00068|            here.parents[4] / "data",  # /wc/wcg4/data
00069|            here.parents[3] / "data" / "wcg",
00070|            Path("/app/demo_data"),
00071|            Path("/home/caa/wc/wcg4/data"),
00072|        ]
00073|        for c in candidates:
00074|            if c.exists():
00075|                return c
00076|        return candidates[0]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiQ2FyZ2EgbG9zIGFyY2hpdm9zIGRlIGRlbW8gZGVzZGUgZWwgZGlyZWN0b3JpbyBkYXRhLyBoYWNpYSBsb3MgbcOzZHVsb3MgV0NHLiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKZnJvbSBwYXRobGliIGltcG9ydCBQYXRoCgpmcm9tIGRqYW5nby5jb250cmliLmF1dGggaW1wb3J0IGdldF91c2VyX21vZGVsCmZyb20gZGphbmdvLmNvcmUubWFuYWdlbWVudC5iYXNlIGltcG9ydCBCYXNlQ29tbWFuZAoKZnJvbSBpbXBvcnRzLmRpc3BhdGNoIGltcG9ydCBydW5faW1wb3J0X3BhdGgKZnJvbSBwZ28ucGVyaW9kbyBpbXBvcnQgcmVjYWxjdWxhdGVfcGdvX3BlcmlvZG9zCgpVc2VyID0gZ2V0X3VzZXJfbW9kZWwoKQoKIyBPcmRlbiBpbXBvcnRhOiBDUk0geSBsZWFzaW5nIGJhc2UgYW50ZXMgZGUgcmVudGFzCkRFRkFVTFRfRklMRVMgPSBbCiAgICAoImNybSBkYXRvcyAtIEluZm9DbGllbnRlc1dDRyBwYXJhIENSTS5jc3YiLCBOb25lKSwKICAgICgicGdvIGRhdG9zIC0gY29udHJvbCBkZSB0aWNrZXRzIG1hcnpvIGFicmlsIHkgbWF5byAyMDI2IHBhcmEgUEdPLnhsc3giLCAicGdvX3RpY2tldHMiKSwKICAgICgicGdvIGRhdG9zIC0gQXJjaGl2b3MgcGFyYSBQR08uY3N2IiwgInBnb19jYXRhbG9nbyIpLAogICAgKCJCYXNlTGVhc2luZzIwMjYwNi5jc3YiLCAicmlza19sZWFzaW5nIiksCiAgICAoImJhbG9uIGRhdG9zIC0gQmFzZUxlYXNpbmcyMDI2MDUuY3N2IiwgInJpc2tfbGVhc2luZyIpLAogICAgKCJMZWFzaW5nUmVudGFzMjAyNi0wNi0zMC5jc3YiLCAicmlza19yZW50YXMiKSwKXQoKCmNsYXNzIENvbW1hbmQoQmFzZUNvbW1hbmQpOgogICAgaGVscCA9ICJJbXBvcnRhIGFyY2hpdm9zIGRlIC93Y2c0L2RhdGEgbyBkZW1vX2RhdGEvIHbDrWEgSW1wb3J0YWNpw7NuIEdlbmVyYWwiCgogICAgZGVmIGFkZF9hcmd1bWVudHMoc2VsZiwgcGFyc2VyKToKICAgICAgICBwYXJzZXIuYWRkX2FyZ3VtZW50KAogICAgICAgICAgICAiLS1kaXIiLAogICAgICAgICAgICBkZWZhdWx0PSIiLAogICAgICAgICAgICBoZWxwPSJEaXJlY3RvcmlvIGRlIGRhdG9zIChkZWZhdWx0OiBkZW1vX2RhdGEvIG8gLi4vZGF0YSkiLAogICAgICAgICkKICAgICAgICBwYXJzZXIuYWRkX2FyZ3VtZW50KCItLXVzZXIiLCBkZWZhdWx0PSIiLCBoZWxwPSJVc2VybmFtZSBxdWUgcmVnaXN0cmEgbG9zIGxvdGVzIikKCiAgICBkZWYgaGFuZGxlKHNlbGYsICphcmdzLCAqKm9wdGlvbnMpOgogICAgICAgIGJhc2UgPSBQYXRoKG9wdGlvbnNbImRpciJdKSBpZiBvcHRpb25zWyJkaXIiXSBlbHNlIHNlbGYuX2RlZmF1bHRfZGF0YV9kaXIoKQogICAgICAgIGlmIG5vdCBiYXNlLmV4aXN0cygpOgogICAgICAgICAgICBzZWxmLnN0ZGVyci53cml0ZShzZWxmLnN0eWxlLkVSUk9SKGYiTm8gZXhpc3RlIGRpcmVjdG9yaW86IHtiYXNlfSIpKQogICAgICAgICAgICByZXR1cm4KCiAgICAgICAgdXNlciA9IE5vbmUKICAgICAgICBpZiBvcHRpb25zWyJ1c2VyIl06CiAgICAgICAgICAgIHVzZXIgPSBVc2VyLm9iamVjdHMuZmlsdGVyKHVzZXJuYW1lPW9wdGlvbnNbInVzZXIiXSkuZmlyc3QoKQogICAgICAgIHVzZXIgPSB1c2VyIG9yIFVzZXIub2JqZWN0cy5maWx0ZXIoaXNfc3VwZXJ1c2VyPVRydWUpLmZpcnN0KCkgb3IgVXNlci5vYmplY3RzLmZpcnN0KCkKICAgICAgICBpZiBub3QgdXNlcjoKICAgICAgICAgICAgc2VsZi5zdGRlcnIud3JpdGUoc2VsZi5zdHlsZS5FUlJPUigiTm8gaGF5IHVzdWFyaW8gcGFyYSBhc29jaWFyIGxvdGVzLiIpKQogICAgICAgICAgICByZXR1cm4KCiAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoZiJJbXBvcnRhbmRvIGRlc2RlIHtiYXNlfSBjb21vIHt1c2VyLnVzZXJuYW1lfSIpCiAgICAgICAgZm9yIGZpbGVuYW1lLCBmb3JjZWQgaW4gREVGQVVMVF9GSUxFUzoKICAgICAgICAgICAgcGF0aCA9IGJhc2UgLyBmaWxlbmFtZQogICAgICAgICAgICBpZiBub3QgcGF0aC5leGlzdHMoKToKICAgICAgICAgICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKHNlbGYuc3R5bGUuV0FSTklORyhmIiAgc2tpcCAobm8gZW5jb250cmFkbyk6IHtmaWxlbmFtZX0iKSkKICAgICAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgICAgIHJlc3VsdCA9IHJ1bl9pbXBvcnRfcGF0aCh1c2VyLCBzdHIocGF0aCksIHRpcG9fZm9yemFkbz1mb3JjZWQpCiAgICAgICAgICAgIHN0eWxlID0gc2VsZi5zdHlsZS5TVUNDRVNTIGlmIHJlc3VsdC5vayBlbHNlIHNlbGYuc3R5bGUuV0FSTklORwogICAgICAgICAgICBzZWxmLnN0ZG91dC53cml0ZShzdHlsZShmIiAgW3tyZXN1bHQudGlwb31dIHtmaWxlbmFtZX06IHtyZXN1bHQubWVzc2FnZX0iKSkKCiAgICAgICAgcmVjYWxjdWxhdGVfcGdvX3BlcmlvZG9zKCkKICAgICAgICBzZWxmLnN0ZG91dC53cml0ZShzZWxmLnN0eWxlLlNVQ0NFU1MoIlJlY8OhbGN1bG8gUEdPIE9LLiBJbXBvcnRhY2nDs24gZ2VuZXJhbCBmaW5hbGl6YWRhLiIpKQoKICAgIGRlZiBfZGVmYXVsdF9kYXRhX2RpcihzZWxmKSAtPiBQYXRoOgogICAgICAgIGhlcmUgPSBQYXRoKF9fZmlsZV9fKS5yZXNvbHZlKCkKICAgICAgICBjYW5kaWRhdGVzID0gWwogICAgICAgICAgICBoZXJlLnBhcmVudHNbM10gLyAiZGVtb19kYXRhIiwgICMgZGFzaGJvYXJkL2RlbW9fZGF0YSAoZGVwbG95KQogICAgICAgICAgICBoZXJlLnBhcmVudHNbNF0gLyAiZGF0YSIsICAjIC93Yy93Y2c0L2RhdGEKICAgICAgICAgICAgaGVyZS5wYXJlbnRzWzNdIC8gImRhdGEiIC8gIndjZyIsCiAgICAgICAgICAgIFBhdGgoIi9hcHAvZGVtb19kYXRhIiksCiAgICAgICAgICAgIFBhdGgoIi9ob21lL2NhYS93Yy93Y2c0L2RhdGEiKSwKICAgICAgICBdCiAgICAgICAgZm9yIGMgaW4gY2FuZGlkYXRlczoKICAgICAgICAgICAgaWYgYy5leGlzdHMoKToKICAgICAgICAgICAgICAgIHJldHVybiBjCiAgICAgICAgcmV0dXJuIGNhbmRpZGF0ZXNbMF0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/management/commands/recalc_investment_ingresos_from_new_clients.py
PATH_JSON="imports/management/commands/recalc_investment_ingresos_from_new_clients.py"
FILENAME=recalc_investment_ingresos_from_new_clients.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=110
SIZE_BYTES_UTF8=3638
CONTENT_SHA256=bb2374a4ed7dd4989e425520faf4d17f65d8ead53ec0b75c6ef958d64974a5dc
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
# imports/management/commands/recalc_investment_ingresos_from_new_clients.py

from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import MetricDefinition
from pgc.investment_ingresos import get_investment_une, sum_investment_ingresos_usd
from pgc.models import (
    MonthlyMetricResult,
    MonthlyTarget,
    PGCPlan,
)


class Command(BaseCommand):
    help = (
        "Recalcula INGRESOS de INVESTMENT desde NewClientImportRow "
        "(misma lógica que /pgc/ingresos/: todos los registros del mes; "
        "amount ya está en miles, sin volver a dividir entre 1000)."
    )

    def add_arguments(self, parser):
        parser.add_argument("--year", type=int, required=True)
        parser.add_argument("--month", type=int, required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        year = options["year"]
        month = options["month"]

        try:
            plan = PGCPlan.objects.get(year=year)
        except PGCPlan.DoesNotExist:
            raise CommandError(f"No existe PGCPlan para {year}.")

        une = get_investment_une()
        if not une:
            raise CommandError("No existe UNE Investment.")

        try:
            metric = MetricDefinition.objects.get(
                code=MetricDefinition.CODE_INGRESOS
            )
        except MetricDefinition.DoesNotExist:
            raise CommandError("No existe MetricDefinition para CODE_INGRESOS.")

        try:
            target = MonthlyTarget.objects.get(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
            )
        except MonthlyTarget.DoesNotExist:
            raise CommandError(
                f"No existe MonthlyTarget para INGRESOS INVESTMENT "
                f"{year}-{month:02d}."
            )

        summary = sum_investment_ingresos_usd(year, month, une=une)
        fx = summary["fx"]
        if fx in (None, Decimal("0")):
            raise CommandError(
                f"No existe MonthlyExchangeRate válido para {year}-{month:02d}."
            )

        total_usd = summary["total_usd"]
        used_rows = summary["used_rows"]

        mmr, _ = MonthlyMetricResult.objects.get_or_create(
            plan=plan,
            une=une,
            metric=metric,
            year=year,
            month=month,
            defaults={"target_value": target.target_value},
        )

        mmr.target_value = target.target_value
        mmr.measured_value = total_usd
        mmr.source_currency = MonthlyMetricResult.CURRENCY_USD
        mmr.source_value = total_usd
        mmr.exchange_rate_used = fx
        mmr.conversion_status = MonthlyMetricResult.CONVERSION_NATIVE_USD
        mmr.is_achieved = (
            total_usd >= target.target_value
            if target.target_value is not None
            else False
        )
        mmr.points_awarded = (
            target.points_if_achieved if mmr.is_achieved else 0
        )
        mmr.calculation_note = (
            "INVESTMENT INGRESOS recalculado desde NewClientImportRow "
            f"(todos los registros del mes; alineado con /pgc/ingresos/). "
            f"Filas={used_rows}. "
            f"GTQ->USD usando TC={fx} del {year}-{month:02d}. "
            f"TotalUSD={total_usd}."
        )
        mmr.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Actualizado INGRESOS INVESTMENT {year}-{month:02d}: "
                f"USD {total_usd} con {used_rows} filas."
            )
        )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|# imports/management/commands/recalc_investment_ingresos_from_new_clients.py
00002|
00003|from decimal import Decimal
00004|
00005|from django.core.management.base import BaseCommand, CommandError
00006|from django.db import transaction
00007|
00008|from core.models import MetricDefinition
00009|from pgc.investment_ingresos import get_investment_une, sum_investment_ingresos_usd
00010|from pgc.models import (
00011|    MonthlyMetricResult,
00012|    MonthlyTarget,
00013|    PGCPlan,
00014|)
00015|
00016|
00017|class Command(BaseCommand):
00018|    help = (
00019|        "Recalcula INGRESOS de INVESTMENT desde NewClientImportRow "
00020|        "(misma lógica que /pgc/ingresos/: todos los registros del mes; "
00021|        "amount ya está en miles, sin volver a dividir entre 1000)."
00022|    )
00023|
00024|    def add_arguments(self, parser):
00025|        parser.add_argument("--year", type=int, required=True)
00026|        parser.add_argument("--month", type=int, required=True)
00027|
00028|    @transaction.atomic
00029|    def handle(self, *args, **options):
00030|        year = options["year"]
00031|        month = options["month"]
00032|
00033|        try:
00034|            plan = PGCPlan.objects.get(year=year)
00035|        except PGCPlan.DoesNotExist:
00036|            raise CommandError(f"No existe PGCPlan para {year}.")
00037|
00038|        une = get_investment_une()
00039|        if not une:
00040|            raise CommandError("No existe UNE Investment.")
00041|
00042|        try:
00043|            metric = MetricDefinition.objects.get(
00044|                code=MetricDefinition.CODE_INGRESOS
00045|            )
00046|        except MetricDefinition.DoesNotExist:
00047|            raise CommandError("No existe MetricDefinition para CODE_INGRESOS.")
00048|
00049|        try:
00050|            target = MonthlyTarget.objects.get(
00051|                plan=plan,
00052|                une=une,
00053|                metric=metric,
00054|                year=year,
00055|                month=month,
00056|            )
00057|        except MonthlyTarget.DoesNotExist:
00058|            raise CommandError(
00059|                f"No existe MonthlyTarget para INGRESOS INVESTMENT "
00060|                f"{year}-{month:02d}."
00061|            )
00062|
00063|        summary = sum_investment_ingresos_usd(year, month, une=une)
00064|        fx = summary["fx"]
00065|        if fx in (None, Decimal("0")):
00066|            raise CommandError(
00067|                f"No existe MonthlyExchangeRate válido para {year}-{month:02d}."
00068|            )
00069|
00070|        total_usd = summary["total_usd"]
00071|        used_rows = summary["used_rows"]
00072|
00073|        mmr, _ = MonthlyMetricResult.objects.get_or_create(
00074|            plan=plan,
00075|            une=une,
00076|            metric=metric,
00077|            year=year,
00078|            month=month,
00079|            defaults={"target_value": target.target_value},
00080|        )
00081|
00082|        mmr.target_value = target.target_value
00083|        mmr.measured_value = total_usd
00084|        mmr.source_currency = MonthlyMetricResult.CURRENCY_USD
00085|        mmr.source_value = total_usd
00086|        mmr.exchange_rate_used = fx
00087|        mmr.conversion_status = MonthlyMetricResult.CONVERSION_NATIVE_USD
00088|        mmr.is_achieved = (
00089|            total_usd >= target.target_value
00090|            if target.target_value is not None
00091|            else False
00092|        )
00093|        mmr.points_awarded = (
00094|            target.points_if_achieved if mmr.is_achieved else 0
00095|        )
00096|        mmr.calculation_note = (
00097|            "INVESTMENT INGRESOS recalculado desde NewClientImportRow "
00098|            f"(todos los registros del mes; alineado con /pgc/ingresos/). "
00099|            f"Filas={used_rows}. "
00100|            f"GTQ->USD usando TC={fx} del {year}-{month:02d}. "
00101|            f"TotalUSD={total_usd}."
00102|        )
00103|        mmr.save()
00104|
00105|        self.stdout.write(
00106|            self.style.SUCCESS(
00107|                f"Actualizado INGRESOS INVESTMENT {year}-{month:02d}: "
00108|                f"USD {total_usd} con {used_rows} filas."
00109|            )
00110|        )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IyBpbXBvcnRzL21hbmFnZW1lbnQvY29tbWFuZHMvcmVjYWxjX2ludmVzdG1lbnRfaW5ncmVzb3NfZnJvbV9uZXdfY2xpZW50cy5weQoKZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsCgpmcm9tIGRqYW5nby5jb3JlLm1hbmFnZW1lbnQuYmFzZSBpbXBvcnQgQmFzZUNvbW1hbmQsIENvbW1hbmRFcnJvcgpmcm9tIGRqYW5nby5kYiBpbXBvcnQgdHJhbnNhY3Rpb24KCmZyb20gY29yZS5tb2RlbHMgaW1wb3J0IE1ldHJpY0RlZmluaXRpb24KZnJvbSBwZ2MuaW52ZXN0bWVudF9pbmdyZXNvcyBpbXBvcnQgZ2V0X2ludmVzdG1lbnRfdW5lLCBzdW1faW52ZXN0bWVudF9pbmdyZXNvc191c2QKZnJvbSBwZ2MubW9kZWxzIGltcG9ydCAoCiAgICBNb250aGx5TWV0cmljUmVzdWx0LAogICAgTW9udGhseVRhcmdldCwKICAgIFBHQ1BsYW4sCikKCgpjbGFzcyBDb21tYW5kKEJhc2VDb21tYW5kKToKICAgIGhlbHAgPSAoCiAgICAgICAgIlJlY2FsY3VsYSBJTkdSRVNPUyBkZSBJTlZFU1RNRU5UIGRlc2RlIE5ld0NsaWVudEltcG9ydFJvdyAiCiAgICAgICAgIihtaXNtYSBsw7NnaWNhIHF1ZSAvcGdjL2luZ3Jlc29zLzogdG9kb3MgbG9zIHJlZ2lzdHJvcyBkZWwgbWVzOyAiCiAgICAgICAgImFtb3VudCB5YSBlc3TDoSBlbiBtaWxlcywgc2luIHZvbHZlciBhIGRpdmlkaXIgZW50cmUgMTAwMCkuIgogICAgKQoKICAgIGRlZiBhZGRfYXJndW1lbnRzKHNlbGYsIHBhcnNlcik6CiAgICAgICAgcGFyc2VyLmFkZF9hcmd1bWVudCgiLS15ZWFyIiwgdHlwZT1pbnQsIHJlcXVpcmVkPVRydWUpCiAgICAgICAgcGFyc2VyLmFkZF9hcmd1bWVudCgiLS1tb250aCIsIHR5cGU9aW50LCByZXF1aXJlZD1UcnVlKQoKICAgIEB0cmFuc2FjdGlvbi5hdG9taWMKICAgIGRlZiBoYW5kbGUoc2VsZiwgKmFyZ3MsICoqb3B0aW9ucyk6CiAgICAgICAgeWVhciA9IG9wdGlvbnNbInllYXIiXQogICAgICAgIG1vbnRoID0gb3B0aW9uc1sibW9udGgiXQoKICAgICAgICB0cnk6CiAgICAgICAgICAgIHBsYW4gPSBQR0NQbGFuLm9iamVjdHMuZ2V0KHllYXI9eWVhcikKICAgICAgICBleGNlcHQgUEdDUGxhbi5Eb2VzTm90RXhpc3Q6CiAgICAgICAgICAgIHJhaXNlIENvbW1hbmRFcnJvcihmIk5vIGV4aXN0ZSBQR0NQbGFuIHBhcmEge3llYXJ9LiIpCgogICAgICAgIHVuZSA9IGdldF9pbnZlc3RtZW50X3VuZSgpCiAgICAgICAgaWYgbm90IHVuZToKICAgICAgICAgICAgcmFpc2UgQ29tbWFuZEVycm9yKCJObyBleGlzdGUgVU5FIEludmVzdG1lbnQuIikKCiAgICAgICAgdHJ5OgogICAgICAgICAgICBtZXRyaWMgPSBNZXRyaWNEZWZpbml0aW9uLm9iamVjdHMuZ2V0KAogICAgICAgICAgICAgICAgY29kZT1NZXRyaWNEZWZpbml0aW9uLkNPREVfSU5HUkVTT1MKICAgICAgICAgICAgKQogICAgICAgIGV4Y2VwdCBNZXRyaWNEZWZpbml0aW9uLkRvZXNOb3RFeGlzdDoKICAgICAgICAgICAgcmFpc2UgQ29tbWFuZEVycm9yKCJObyBleGlzdGUgTWV0cmljRGVmaW5pdGlvbiBwYXJhIENPREVfSU5HUkVTT1MuIikKCiAgICAgICAgdHJ5OgogICAgICAgICAgICB0YXJnZXQgPSBNb250aGx5VGFyZ2V0Lm9iamVjdHMuZ2V0KAogICAgICAgICAgICAgICAgcGxhbj1wbGFuLAogICAgICAgICAgICAgICAgdW5lPXVuZSwKICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgICAgICAgICBtb250aD1tb250aCwKICAgICAgICAgICAgKQogICAgICAgIGV4Y2VwdCBNb250aGx5VGFyZ2V0LkRvZXNOb3RFeGlzdDoKICAgICAgICAgICAgcmFpc2UgQ29tbWFuZEVycm9yKAogICAgICAgICAgICAgICAgZiJObyBleGlzdGUgTW9udGhseVRhcmdldCBwYXJhIElOR1JFU09TIElOVkVTVE1FTlQgIgogICAgICAgICAgICAgICAgZiJ7eWVhcn0te21vbnRoOjAyZH0uIgogICAgICAgICAgICApCgogICAgICAgIHN1bW1hcnkgPSBzdW1faW52ZXN0bWVudF9pbmdyZXNvc191c2QoeWVhciwgbW9udGgsIHVuZT11bmUpCiAgICAgICAgZnggPSBzdW1tYXJ5WyJmeCJdCiAgICAgICAgaWYgZnggaW4gKE5vbmUsIERlY2ltYWwoIjAiKSk6CiAgICAgICAgICAgIHJhaXNlIENvbW1hbmRFcnJvcigKICAgICAgICAgICAgICAgIGYiTm8gZXhpc3RlIE1vbnRobHlFeGNoYW5nZVJhdGUgdsOhbGlkbyBwYXJhIHt5ZWFyfS17bW9udGg6MDJkfS4iCiAgICAgICAgICAgICkKCiAgICAgICAgdG90YWxfdXNkID0gc3VtbWFyeVsidG90YWxfdXNkIl0KICAgICAgICB1c2VkX3Jvd3MgPSBzdW1tYXJ5WyJ1c2VkX3Jvd3MiXQoKICAgICAgICBtbXIsIF8gPSBNb250aGx5TWV0cmljUmVzdWx0Lm9iamVjdHMuZ2V0X29yX2NyZWF0ZSgKICAgICAgICAgICAgcGxhbj1wbGFuLAogICAgICAgICAgICB1bmU9dW5lLAogICAgICAgICAgICBtZXRyaWM9bWV0cmljLAogICAgICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICBkZWZhdWx0cz17InRhcmdldF92YWx1ZSI6IHRhcmdldC50YXJnZXRfdmFsdWV9LAogICAgICAgICkKCiAgICAgICAgbW1yLnRhcmdldF92YWx1ZSA9IHRhcmdldC50YXJnZXRfdmFsdWUKICAgICAgICBtbXIubWVhc3VyZWRfdmFsdWUgPSB0b3RhbF91c2QKICAgICAgICBtbXIuc291cmNlX2N1cnJlbmN5ID0gTW9udGhseU1ldHJpY1Jlc3VsdC5DVVJSRU5DWV9VU0QKICAgICAgICBtbXIuc291cmNlX3ZhbHVlID0gdG90YWxfdXNkCiAgICAgICAgbW1yLmV4Y2hhbmdlX3JhdGVfdXNlZCA9IGZ4CiAgICAgICAgbW1yLmNvbnZlcnNpb25fc3RhdHVzID0gTW9udGhseU1ldHJpY1Jlc3VsdC5DT05WRVJTSU9OX05BVElWRV9VU0QKICAgICAgICBtbXIuaXNfYWNoaWV2ZWQgPSAoCiAgICAgICAgICAgIHRvdGFsX3VzZCA+PSB0YXJnZXQudGFyZ2V0X3ZhbHVlCiAgICAgICAgICAgIGlmIHRhcmdldC50YXJnZXRfdmFsdWUgaXMgbm90IE5vbmUKICAgICAgICAgICAgZWxzZSBGYWxzZQogICAgICAgICkKICAgICAgICBtbXIucG9pbnRzX2F3YXJkZWQgPSAoCiAgICAgICAgICAgIHRhcmdldC5wb2ludHNfaWZfYWNoaWV2ZWQgaWYgbW1yLmlzX2FjaGlldmVkIGVsc2UgMAogICAgICAgICkKICAgICAgICBtbXIuY2FsY3VsYXRpb25fbm90ZSA9ICgKICAgICAgICAgICAgIklOVkVTVE1FTlQgSU5HUkVTT1MgcmVjYWxjdWxhZG8gZGVzZGUgTmV3Q2xpZW50SW1wb3J0Um93ICIKICAgICAgICAgICAgZiIodG9kb3MgbG9zIHJlZ2lzdHJvcyBkZWwgbWVzOyBhbGluZWFkbyBjb24gL3BnYy9pbmdyZXNvcy8pLiAiCiAgICAgICAgICAgIGYiRmlsYXM9e3VzZWRfcm93c30uICIKICAgICAgICAgICAgZiJHVFEtPlVTRCB1c2FuZG8gVEM9e2Z4fSBkZWwge3llYXJ9LXttb250aDowMmR9LiAiCiAgICAgICAgICAgIGYiVG90YWxVU0Q9e3RvdGFsX3VzZH0uIgogICAgICAgICkKICAgICAgICBtbXIuc2F2ZSgpCgogICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKAogICAgICAgICAgICBzZWxmLnN0eWxlLlNVQ0NFU1MoCiAgICAgICAgICAgICAgICBmIkFjdHVhbGl6YWRvIElOR1JFU09TIElOVkVTVE1FTlQge3llYXJ9LXttb250aDowMmR9OiAiCiAgICAgICAgICAgICAgICBmIlVTRCB7dG90YWxfdXNkfSBjb24ge3VzZWRfcm93c30gZmlsYXMuIgogICAgICAgICAgICApCiAgICAgICAgKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
