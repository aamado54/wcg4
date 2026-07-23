# CONCATENATED .PY FILES

PART_NUMBER=9
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
PATH_LITERAL=pgo/urls.py
PATH_JSON="pgo/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=16
SIZE_BYTES_UTF8=638
CONTENT_SHA256=13abe36538807b2de359e151509844ef2c1e25a9973e611656fa5994c1745d39
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
from django.urls import path

from . import views

app_name = "pgo"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("tickets/", views.TicketListView.as_view(), name="ticket_list"),
    path("tickets/<str:codigo>/", views.TicketDetailView.as_view(), name="ticket_detail"),
    path("resultados/", views.resultados, name="resultados"),
    path("exportar/", views.export_tickets, name="export_tickets"),
    path("importar/", views.importar, name="importar"),
    path("resumen/usuario/", views.resumen_usuario, name="resumen_usuario"),
    path("resumen/unidad/", views.resumen_unidad, name="resumen_unidad"),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.urls import path
00002|
00003|from . import views
00004|
00005|app_name = "pgo"
00006|
00007|urlpatterns = [
00008|    path("", views.dashboard, name="dashboard"),
00009|    path("tickets/", views.TicketListView.as_view(), name="ticket_list"),
00010|    path("tickets/<str:codigo>/", views.TicketDetailView.as_view(), name="ticket_detail"),
00011|    path("resultados/", views.resultados, name="resultados"),
00012|    path("exportar/", views.export_tickets, name="export_tickets"),
00013|    path("importar/", views.importar, name="importar"),
00014|    path("resumen/usuario/", views.resumen_usuario, name="resumen_usuario"),
00015|    path("resumen/unidad/", views.resumen_unidad, name="resumen_unidad"),
00016|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aAoKZnJvbSAuIGltcG9ydCB2aWV3cwoKYXBwX25hbWUgPSAicGdvIgoKdXJscGF0dGVybnMgPSBbCiAgICBwYXRoKCIiLCB2aWV3cy5kYXNoYm9hcmQsIG5hbWU9ImRhc2hib2FyZCIpLAogICAgcGF0aCgidGlja2V0cy8iLCB2aWV3cy5UaWNrZXRMaXN0Vmlldy5hc192aWV3KCksIG5hbWU9InRpY2tldF9saXN0IiksCiAgICBwYXRoKCJ0aWNrZXRzLzxzdHI6Y29kaWdvPi8iLCB2aWV3cy5UaWNrZXREZXRhaWxWaWV3LmFzX3ZpZXcoKSwgbmFtZT0idGlja2V0X2RldGFpbCIpLAogICAgcGF0aCgicmVzdWx0YWRvcy8iLCB2aWV3cy5yZXN1bHRhZG9zLCBuYW1lPSJyZXN1bHRhZG9zIiksCiAgICBwYXRoKCJleHBvcnRhci8iLCB2aWV3cy5leHBvcnRfdGlja2V0cywgbmFtZT0iZXhwb3J0X3RpY2tldHMiKSwKICAgIHBhdGgoImltcG9ydGFyLyIsIHZpZXdzLmltcG9ydGFyLCBuYW1lPSJpbXBvcnRhciIpLAogICAgcGF0aCgicmVzdW1lbi91c3VhcmlvLyIsIHZpZXdzLnJlc3VtZW5fdXN1YXJpbywgbmFtZT0icmVzdW1lbl91c3VhcmlvIiksCiAgICBwYXRoKCJyZXN1bWVuL3VuaWRhZC8iLCB2aWV3cy5yZXN1bWVuX3VuaWRhZCwgbmFtZT0icmVzdW1lbl91bmlkYWQiKSwKXQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgo/views.py
PATH_JSON="pgo/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=121
SIZE_BYTES_UTF8=3695
CONTENT_SHA256=580ccb99ad5f9541fb9b39e75a7ab179a8af67707059efda7ac263c6765fb649
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

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib.auth.decorators import login_required
00002|from django.contrib.auth.mixins import LoginRequiredMixin
00003|from django.db.models import Count, Q
00004|from django.http import HttpResponse
00005|from django.shortcuts import redirect, render
00006|from django.views.generic import DetailView, ListView
00007|
00008|from .models import PgoResultadoPeriodo, Ticket
00009|from .periodo import recalculate_pgo_periodos
00010|from .selectors import ticket_dashboard_summary, ticket_list_queryset
00011|
00012|
00013|@login_required
00014|def dashboard(request):
00015|    recalculate_pgo_periodos()
00016|    summary = ticket_dashboard_summary()
00017|    por_unidad = (
00018|        Ticket.objects.values("unidad_negocio__nombre")
00019|        .annotate(total=Count("id"))
00020|        .order_by("-total")[:10]
00021|    )
00022|    return render(
00023|        request,
00024|        "pgo/pgodashboard.html",
00025|        {
00026|            **summary,
00027|            "abiertos": summary["tickets_abiertos"],
00028|            "cerrados": summary["tickets_cerrados"],
00029|            "recibidos": summary["total_tickets"],
00030|            "por_unidad": por_unidad,
00031|            "breadcrumbs": [
00032|                {"label": "Panel principal", "url": "/panel/"},
00033|                {"label": "PGO — Operación"},
00034|            ],
00035|        },
00036|    )
00037|
00038|
00039|class TicketListView(LoginRequiredMixin, ListView):
00040|    model = Ticket
00041|    template_name = "pgo/pgoticketlist.html"
00042|    context_object_name = "tickets"
00043|    paginate_by = 50
00044|
00045|    def get_queryset(self):
00046|        return ticket_list_queryset(self.request)
00047|
00048|    def get_context_data(self, **kwargs):
00049|        ctx = super().get_context_data(**kwargs)
00050|        ctx["estados"] = Ticket.ESTADO_CHOICES
00051|        ctx["prioridades"] = Ticket.PRIORIDAD_CHOICES
00052|        return ctx
00053|
00054|
00055|class TicketDetailView(LoginRequiredMixin, DetailView):
00056|    model = Ticket
00057|    template_name = "pgo/pgoticketdetail.html"
00058|    context_object_name = "ticket"
00059|    slug_field = "codigo"
00060|    slug_url_kwarg = "codigo"
00061|
00062|    def get_context_data(self, **kwargs):
00063|        ctx = super().get_context_data(**kwargs)
00064|        ctx["eventos"] = self.object.eventos.select_related("usuario")
00065|        return ctx
00066|
00067|
00068|@login_required
00069|def importar(request):
00070|    return redirect("imports:import_hub")
00071|
00072|
00073|@login_required
00074|def resumen_usuario(request):
00075|    data = (
00076|        Ticket.objects.values("asignado_a__username")
00077|        .annotate(total=Count("id"), abiertos=Count("id", filter=Q(estado=Ticket.ESTADO_ABIERTO)))
00078|        .order_by("-total")
00079|    )
00080|    return render(request, "pgo/pgoresumenusuario.html", {"data": data})
00081|
00082|
00083|@login_required
00084|def resumen_unidad(request):
00085|    data = (
00086|        Ticket.objects.values("unidad_negocio__code", "unidad_negocio__nombre")
00087|        .annotate(total=Count("id"))
00088|        .order_by("-total")
00089|    )
00090|    return render(request, "pgo/pgoresumenunidad.html", {"data": data})
00091|
00092|
00093|@login_required
00094|def resultados(request):
00095|    recalculate_pgo_periodos()
00096|    rows = PgoResultadoPeriodo.objects.select_related("unidad_negocio").order_by("-periodo")
00097|    return render(request, "pgo/pgoresultados.html", {"resultados": rows})
00098|
00099|
00100|@login_required
00101|def export_tickets(request):
00102|    import csv
00103|
00104|    qs = ticket_list_queryset(request)
00105|    response = HttpResponse(content_type="text/csv")
00106|    response["Content-Disposition"] = 'attachment; filename="pgo_tickets.csv"'
00107|    writer = csv.writer(response)
00108|    writer.writerow(["codigo", "titulo", "estado", "prioridad", "unidad", "apertura", "cierre"])
00109|    for t in qs:
00110|        writer.writerow(
00111|            [
00112|                t.codigo,
00113|                t.titulo,
00114|                t.estado,
00115|                t.prioridad,
00116|                t.unidad_negocio.code if t.unidad_negocio else "",
00117|                t.fecha_apertura,
00118|                t.fecha_cierre or "",
00119|            ]
00120|        )
00121|    return response

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYi5hdXRoLmRlY29yYXRvcnMgaW1wb3J0IGxvZ2luX3JlcXVpcmVkCmZyb20gZGphbmdvLmNvbnRyaWIuYXV0aC5taXhpbnMgaW1wb3J0IExvZ2luUmVxdWlyZWRNaXhpbgpmcm9tIGRqYW5nby5kYi5tb2RlbHMgaW1wb3J0IENvdW50LCBRCmZyb20gZGphbmdvLmh0dHAgaW1wb3J0IEh0dHBSZXNwb25zZQpmcm9tIGRqYW5nby5zaG9ydGN1dHMgaW1wb3J0IHJlZGlyZWN0LCByZW5kZXIKZnJvbSBkamFuZ28udmlld3MuZ2VuZXJpYyBpbXBvcnQgRGV0YWlsVmlldywgTGlzdFZpZXcKCmZyb20gLm1vZGVscyBpbXBvcnQgUGdvUmVzdWx0YWRvUGVyaW9kbywgVGlja2V0CmZyb20gLnBlcmlvZG8gaW1wb3J0IHJlY2FsY3VsYXRlX3Bnb19wZXJpb2Rvcwpmcm9tIC5zZWxlY3RvcnMgaW1wb3J0IHRpY2tldF9kYXNoYm9hcmRfc3VtbWFyeSwgdGlja2V0X2xpc3RfcXVlcnlzZXQKCgpAbG9naW5fcmVxdWlyZWQKZGVmIGRhc2hib2FyZChyZXF1ZXN0KToKICAgIHJlY2FsY3VsYXRlX3Bnb19wZXJpb2RvcygpCiAgICBzdW1tYXJ5ID0gdGlja2V0X2Rhc2hib2FyZF9zdW1tYXJ5KCkKICAgIHBvcl91bmlkYWQgPSAoCiAgICAgICAgVGlja2V0Lm9iamVjdHMudmFsdWVzKCJ1bmlkYWRfbmVnb2Npb19fbm9tYnJlIikKICAgICAgICAuYW5ub3RhdGUodG90YWw9Q291bnQoImlkIikpCiAgICAgICAgLm9yZGVyX2J5KCItdG90YWwiKVs6MTBdCiAgICApCiAgICByZXR1cm4gcmVuZGVyKAogICAgICAgIHJlcXVlc3QsCiAgICAgICAgInBnby9wZ29kYXNoYm9hcmQuaHRtbCIsCiAgICAgICAgewogICAgICAgICAgICAqKnN1bW1hcnksCiAgICAgICAgICAgICJhYmllcnRvcyI6IHN1bW1hcnlbInRpY2tldHNfYWJpZXJ0b3MiXSwKICAgICAgICAgICAgImNlcnJhZG9zIjogc3VtbWFyeVsidGlja2V0c19jZXJyYWRvcyJdLAogICAgICAgICAgICAicmVjaWJpZG9zIjogc3VtbWFyeVsidG90YWxfdGlja2V0cyJdLAogICAgICAgICAgICAicG9yX3VuaWRhZCI6IHBvcl91bmlkYWQsCiAgICAgICAgICAgICJicmVhZGNydW1icyI6IFsKICAgICAgICAgICAgICAgIHsibGFiZWwiOiAiUGFuZWwgcHJpbmNpcGFsIiwgInVybCI6ICIvcGFuZWwvIn0sCiAgICAgICAgICAgICAgICB7ImxhYmVsIjogIlBHTyDigJQgT3BlcmFjacOzbiJ9LAogICAgICAgICAgICBdLAogICAgICAgIH0sCiAgICApCgoKY2xhc3MgVGlja2V0TGlzdFZpZXcoTG9naW5SZXF1aXJlZE1peGluLCBMaXN0Vmlldyk6CiAgICBtb2RlbCA9IFRpY2tldAogICAgdGVtcGxhdGVfbmFtZSA9ICJwZ28vcGdvdGlja2V0bGlzdC5odG1sIgogICAgY29udGV4dF9vYmplY3RfbmFtZSA9ICJ0aWNrZXRzIgogICAgcGFnaW5hdGVfYnkgPSA1MAoKICAgIGRlZiBnZXRfcXVlcnlzZXQoc2VsZik6CiAgICAgICAgcmV0dXJuIHRpY2tldF9saXN0X3F1ZXJ5c2V0KHNlbGYucmVxdWVzdCkKCiAgICBkZWYgZ2V0X2NvbnRleHRfZGF0YShzZWxmLCAqKmt3YXJncyk6CiAgICAgICAgY3R4ID0gc3VwZXIoKS5nZXRfY29udGV4dF9kYXRhKCoqa3dhcmdzKQogICAgICAgIGN0eFsiZXN0YWRvcyJdID0gVGlja2V0LkVTVEFET19DSE9JQ0VTCiAgICAgICAgY3R4WyJwcmlvcmlkYWRlcyJdID0gVGlja2V0LlBSSU9SSURBRF9DSE9JQ0VTCiAgICAgICAgcmV0dXJuIGN0eAoKCmNsYXNzIFRpY2tldERldGFpbFZpZXcoTG9naW5SZXF1aXJlZE1peGluLCBEZXRhaWxWaWV3KToKICAgIG1vZGVsID0gVGlja2V0CiAgICB0ZW1wbGF0ZV9uYW1lID0gInBnby9wZ290aWNrZXRkZXRhaWwuaHRtbCIKICAgIGNvbnRleHRfb2JqZWN0X25hbWUgPSAidGlja2V0IgogICAgc2x1Z19maWVsZCA9ICJjb2RpZ28iCiAgICBzbHVnX3VybF9rd2FyZyA9ICJjb2RpZ28iCgogICAgZGVmIGdldF9jb250ZXh0X2RhdGEoc2VsZiwgKiprd2FyZ3MpOgogICAgICAgIGN0eCA9IHN1cGVyKCkuZ2V0X2NvbnRleHRfZGF0YSgqKmt3YXJncykKICAgICAgICBjdHhbImV2ZW50b3MiXSA9IHNlbGYub2JqZWN0LmV2ZW50b3Muc2VsZWN0X3JlbGF0ZWQoInVzdWFyaW8iKQogICAgICAgIHJldHVybiBjdHgKCgpAbG9naW5fcmVxdWlyZWQKZGVmIGltcG9ydGFyKHJlcXVlc3QpOgogICAgcmV0dXJuIHJlZGlyZWN0KCJpbXBvcnRzOmltcG9ydF9odWIiKQoKCkBsb2dpbl9yZXF1aXJlZApkZWYgcmVzdW1lbl91c3VhcmlvKHJlcXVlc3QpOgogICAgZGF0YSA9ICgKICAgICAgICBUaWNrZXQub2JqZWN0cy52YWx1ZXMoImFzaWduYWRvX2FfX3VzZXJuYW1lIikKICAgICAgICAuYW5ub3RhdGUodG90YWw9Q291bnQoImlkIiksIGFiaWVydG9zPUNvdW50KCJpZCIsIGZpbHRlcj1RKGVzdGFkbz1UaWNrZXQuRVNUQURPX0FCSUVSVE8pKSkKICAgICAgICAub3JkZXJfYnkoIi10b3RhbCIpCiAgICApCiAgICByZXR1cm4gcmVuZGVyKHJlcXVlc3QsICJwZ28vcGdvcmVzdW1lbnVzdWFyaW8uaHRtbCIsIHsiZGF0YSI6IGRhdGF9KQoKCkBsb2dpbl9yZXF1aXJlZApkZWYgcmVzdW1lbl91bmlkYWQocmVxdWVzdCk6CiAgICBkYXRhID0gKAogICAgICAgIFRpY2tldC5vYmplY3RzLnZhbHVlcygidW5pZGFkX25lZ29jaW9fX2NvZGUiLCAidW5pZGFkX25lZ29jaW9fX25vbWJyZSIpCiAgICAgICAgLmFubm90YXRlKHRvdGFsPUNvdW50KCJpZCIpKQogICAgICAgIC5vcmRlcl9ieSgiLXRvdGFsIikKICAgICkKICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgInBnby9wZ29yZXN1bWVudW5pZGFkLmh0bWwiLCB7ImRhdGEiOiBkYXRhfSkKCgpAbG9naW5fcmVxdWlyZWQKZGVmIHJlc3VsdGFkb3MocmVxdWVzdCk6CiAgICByZWNhbGN1bGF0ZV9wZ29fcGVyaW9kb3MoKQogICAgcm93cyA9IFBnb1Jlc3VsdGFkb1BlcmlvZG8ub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgidW5pZGFkX25lZ29jaW8iKS5vcmRlcl9ieSgiLXBlcmlvZG8iKQogICAgcmV0dXJuIHJlbmRlcihyZXF1ZXN0LCAicGdvL3Bnb3Jlc3VsdGFkb3MuaHRtbCIsIHsicmVzdWx0YWRvcyI6IHJvd3N9KQoKCkBsb2dpbl9yZXF1aXJlZApkZWYgZXhwb3J0X3RpY2tldHMocmVxdWVzdCk6CiAgICBpbXBvcnQgY3N2CgogICAgcXMgPSB0aWNrZXRfbGlzdF9xdWVyeXNldChyZXF1ZXN0KQogICAgcmVzcG9uc2UgPSBIdHRwUmVzcG9uc2UoY29udGVudF90eXBlPSJ0ZXh0L2NzdiIpCiAgICByZXNwb25zZVsiQ29udGVudC1EaXNwb3NpdGlvbiJdID0gJ2F0dGFjaG1lbnQ7IGZpbGVuYW1lPSJwZ29fdGlja2V0cy5jc3YiJwogICAgd3JpdGVyID0gY3N2LndyaXRlcihyZXNwb25zZSkKICAgIHdyaXRlci53cml0ZXJvdyhbImNvZGlnbyIsICJ0aXR1bG8iLCAiZXN0YWRvIiwgInByaW9yaWRhZCIsICJ1bmlkYWQiLCAiYXBlcnR1cmEiLCAiY2llcnJlIl0pCiAgICBmb3IgdCBpbiBxczoKICAgICAgICB3cml0ZXIud3JpdGVyb3coCiAgICAgICAgICAgIFsKICAgICAgICAgICAgICAgIHQuY29kaWdvLAogICAgICAgICAgICAgICAgdC50aXR1bG8sCiAgICAgICAgICAgICAgICB0LmVzdGFkbywKICAgICAgICAgICAgICAgIHQucHJpb3JpZGFkLAogICAgICAgICAgICAgICAgdC51bmlkYWRfbmVnb2Npby5jb2RlIGlmIHQudW5pZGFkX25lZ29jaW8gZWxzZSAiIiwKICAgICAgICAgICAgICAgIHQuZmVjaGFfYXBlcnR1cmEsCiAgICAgICAgICAgICAgICB0LmZlY2hhX2NpZXJyZSBvciAiIiwKICAgICAgICAgICAgXQogICAgICAgICkKICAgIHJldHVybiByZXNwb25zZQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=portal/__init__.py
PATH_JSON="portal/__init__.py"
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
PATH_LITERAL=portal/admin.py
PATH_JSON="portal/admin.py"
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
PATH_LITERAL=portal/apps.py
PATH_JSON="portal/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=6
SIZE_BYTES_UTF8=144
CONTENT_SHA256=16546b94213142c89b29ae24bbe01cbf2289b72312f90d62cdc3f468bf2a1f4e
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


class PortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portal'

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class PortalConfig(AppConfig):
00005|    default_auto_field = 'django.db.models.BigAutoField'
00006|    name = 'portal'

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgUG9ydGFsQ29uZmlnKEFwcENvbmZpZyk6CiAgICBkZWZhdWx0X2F1dG9fZmllbGQgPSAnZGphbmdvLmRiLm1vZGVscy5CaWdBdXRvRmllbGQnCiAgICBuYW1lID0gJ3BvcnRhbCcK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=portal/models.py
PATH_JSON="portal/models.py"
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
PATH_LITERAL=portal/tests.py
PATH_JSON="portal/tests.py"
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
PATH_LITERAL=portal/urls.py
PATH_JSON="portal/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=11
SIZE_BYTES_UTF8=236
CONTENT_SHA256=7a716aa69ece53dc079592fdde04ce56c7fc671ae4fca0b2286132f303c36789
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
from django.urls import path

from . import views

app_name = "portal"

urlpatterns = [
    path("", views.dashboard_home, name="home"),
    path("estado/", views.estado, name="estado"),
    path("ayuda/", views.ayuda, name="ayuda"),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.urls import path
00002|
00003|from . import views
00004|
00005|app_name = "portal"
00006|
00007|urlpatterns = [
00008|    path("", views.dashboard_home, name="home"),
00009|    path("estado/", views.estado, name="estado"),
00010|    path("ayuda/", views.ayuda, name="ayuda"),
00011|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aAoKZnJvbSAuIGltcG9ydCB2aWV3cwoKYXBwX25hbWUgPSAicG9ydGFsIgoKdXJscGF0dGVybnMgPSBbCiAgICBwYXRoKCIiLCB2aWV3cy5kYXNoYm9hcmRfaG9tZSwgbmFtZT0iaG9tZSIpLAogICAgcGF0aCgiZXN0YWRvLyIsIHZpZXdzLmVzdGFkbywgbmFtZT0iZXN0YWRvIiksCiAgICBwYXRoKCJheXVkYS8iLCB2aWV3cy5heXVkYSwgbmFtZT0iYXl1ZGEiKSwKXQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=portal/views.py
PATH_JSON="portal/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=60
SIZE_BYTES_UTF8=2164
CONTENT_SHA256=44e1110f789dda9aa0be45be6db686727997898a3eb7bc2b419f4890e4e2473f
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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from core.wcg_models import DataImportBatch, Entidad
from crm.models import Tarea
from pgo.models import Ticket
from risk.models import RiskOperationSnapshot
from risk.selectors import latest_snapshots_queryset


def splash(request):
    """Landing visual productiva (pgc1); al entrar va al menú principal."""
    return render(request, "splash.html")


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboardhome.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(_panel_stats())
        return ctx


def _panel_stats():
    snaps = latest_snapshots_queryset()
    return {
        "stats": {
            "entidades_total": Entidad.objects.count(),
            "entidades_activas": Entidad.objects.filter(activa=True).count(),
            "operaciones_riesgo": snaps.values("referencia_operacion").distinct().count(),
            "snapshots": RiskOperationSnapshot.objects.count(),
            "tickets_total": Ticket.objects.count(),
            "tickets_abiertos": Ticket.objects.exclude(estado=Ticket.ESTADO_CERRADO).count(),
            "tareas_pendientes": Tarea.objects.filter(estado=Tarea.ESTADO_PENDIENTE).count()
            if hasattr(Tarea, "ESTADO_PENDIENTE")
            else Tarea.objects.filter(estado="PENDIENTE").count(),
            "lotes_importacion": DataImportBatch.objects.count(),
            "importaciones_recientes": DataImportBatch.objects.order_by("-created_at")[:8],
            "alertas_riesgo": snaps.filter(alerta=True).count(),
        }
    }


@login_required
def dashboard_home(request):
    return render(request, "dashboard/dashboardhome.html")


@login_required
def estado(request):
    """KPIs e importaciones recientes — acceso secundario desde el menú."""
    return render(request, "portal/estado.html", _panel_stats())


@login_required
def ayuda(request):
    return render(request, "portal/ayuda.html")

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib.auth.decorators import login_required
00002|from django.contrib.auth.mixins import LoginRequiredMixin
00003|from django.shortcuts import render
00004|from django.views.generic import TemplateView
00005|
00006|from core.wcg_models import DataImportBatch, Entidad
00007|from crm.models import Tarea
00008|from pgo.models import Ticket
00009|from risk.models import RiskOperationSnapshot
00010|from risk.selectors import latest_snapshots_queryset
00011|
00012|
00013|def splash(request):
00014|    """Landing visual productiva (pgc1); al entrar va al menú principal."""
00015|    return render(request, "splash.html")
00016|
00017|
00018|class DashboardHomeView(LoginRequiredMixin, TemplateView):
00019|    template_name = "dashboard/dashboardhome.html"
00020|
00021|    def get_context_data(self, **kwargs):
00022|        ctx = super().get_context_data(**kwargs)
00023|        ctx.update(_panel_stats())
00024|        return ctx
00025|
00026|
00027|def _panel_stats():
00028|    snaps = latest_snapshots_queryset()
00029|    return {
00030|        "stats": {
00031|            "entidades_total": Entidad.objects.count(),
00032|            "entidades_activas": Entidad.objects.filter(activa=True).count(),
00033|            "operaciones_riesgo": snaps.values("referencia_operacion").distinct().count(),
00034|            "snapshots": RiskOperationSnapshot.objects.count(),
00035|            "tickets_total": Ticket.objects.count(),
00036|            "tickets_abiertos": Ticket.objects.exclude(estado=Ticket.ESTADO_CERRADO).count(),
00037|            "tareas_pendientes": Tarea.objects.filter(estado=Tarea.ESTADO_PENDIENTE).count()
00038|            if hasattr(Tarea, "ESTADO_PENDIENTE")
00039|            else Tarea.objects.filter(estado="PENDIENTE").count(),
00040|            "lotes_importacion": DataImportBatch.objects.count(),
00041|            "importaciones_recientes": DataImportBatch.objects.order_by("-created_at")[:8],
00042|            "alertas_riesgo": snaps.filter(alerta=True).count(),
00043|        }
00044|    }
00045|
00046|
00047|@login_required
00048|def dashboard_home(request):
00049|    return render(request, "dashboard/dashboardhome.html")
00050|
00051|
00052|@login_required
00053|def estado(request):
00054|    """KPIs e importaciones recientes — acceso secundario desde el menú."""
00055|    return render(request, "portal/estado.html", _panel_stats())
00056|
00057|
00058|@login_required
00059|def ayuda(request):
00060|    return render(request, "portal/ayuda.html")

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYi5hdXRoLmRlY29yYXRvcnMgaW1wb3J0IGxvZ2luX3JlcXVpcmVkCmZyb20gZGphbmdvLmNvbnRyaWIuYXV0aC5taXhpbnMgaW1wb3J0IExvZ2luUmVxdWlyZWRNaXhpbgpmcm9tIGRqYW5nby5zaG9ydGN1dHMgaW1wb3J0IHJlbmRlcgpmcm9tIGRqYW5nby52aWV3cy5nZW5lcmljIGltcG9ydCBUZW1wbGF0ZVZpZXcKCmZyb20gY29yZS53Y2dfbW9kZWxzIGltcG9ydCBEYXRhSW1wb3J0QmF0Y2gsIEVudGlkYWQKZnJvbSBjcm0ubW9kZWxzIGltcG9ydCBUYXJlYQpmcm9tIHBnby5tb2RlbHMgaW1wb3J0IFRpY2tldApmcm9tIHJpc2subW9kZWxzIGltcG9ydCBSaXNrT3BlcmF0aW9uU25hcHNob3QKZnJvbSByaXNrLnNlbGVjdG9ycyBpbXBvcnQgbGF0ZXN0X3NuYXBzaG90c19xdWVyeXNldAoKCmRlZiBzcGxhc2gocmVxdWVzdCk6CiAgICAiIiJMYW5kaW5nIHZpc3VhbCBwcm9kdWN0aXZhIChwZ2MxKTsgYWwgZW50cmFyIHZhIGFsIG1lbsO6IHByaW5jaXBhbC4iIiIKICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgInNwbGFzaC5odG1sIikKCgpjbGFzcyBEYXNoYm9hcmRIb21lVmlldyhMb2dpblJlcXVpcmVkTWl4aW4sIFRlbXBsYXRlVmlldyk6CiAgICB0ZW1wbGF0ZV9uYW1lID0gImRhc2hib2FyZC9kYXNoYm9hcmRob21lLmh0bWwiCgogICAgZGVmIGdldF9jb250ZXh0X2RhdGEoc2VsZiwgKiprd2FyZ3MpOgogICAgICAgIGN0eCA9IHN1cGVyKCkuZ2V0X2NvbnRleHRfZGF0YSgqKmt3YXJncykKICAgICAgICBjdHgudXBkYXRlKF9wYW5lbF9zdGF0cygpKQogICAgICAgIHJldHVybiBjdHgKCgpkZWYgX3BhbmVsX3N0YXRzKCk6CiAgICBzbmFwcyA9IGxhdGVzdF9zbmFwc2hvdHNfcXVlcnlzZXQoKQogICAgcmV0dXJuIHsKICAgICAgICAic3RhdHMiOiB7CiAgICAgICAgICAgICJlbnRpZGFkZXNfdG90YWwiOiBFbnRpZGFkLm9iamVjdHMuY291bnQoKSwKICAgICAgICAgICAgImVudGlkYWRlc19hY3RpdmFzIjogRW50aWRhZC5vYmplY3RzLmZpbHRlcihhY3RpdmE9VHJ1ZSkuY291bnQoKSwKICAgICAgICAgICAgIm9wZXJhY2lvbmVzX3JpZXNnbyI6IHNuYXBzLnZhbHVlcygicmVmZXJlbmNpYV9vcGVyYWNpb24iKS5kaXN0aW5jdCgpLmNvdW50KCksCiAgICAgICAgICAgICJzbmFwc2hvdHMiOiBSaXNrT3BlcmF0aW9uU25hcHNob3Qub2JqZWN0cy5jb3VudCgpLAogICAgICAgICAgICAidGlja2V0c190b3RhbCI6IFRpY2tldC5vYmplY3RzLmNvdW50KCksCiAgICAgICAgICAgICJ0aWNrZXRzX2FiaWVydG9zIjogVGlja2V0Lm9iamVjdHMuZXhjbHVkZShlc3RhZG89VGlja2V0LkVTVEFET19DRVJSQURPKS5jb3VudCgpLAogICAgICAgICAgICAidGFyZWFzX3BlbmRpZW50ZXMiOiBUYXJlYS5vYmplY3RzLmZpbHRlcihlc3RhZG89VGFyZWEuRVNUQURPX1BFTkRJRU5URSkuY291bnQoKQogICAgICAgICAgICBpZiBoYXNhdHRyKFRhcmVhLCAiRVNUQURPX1BFTkRJRU5URSIpCiAgICAgICAgICAgIGVsc2UgVGFyZWEub2JqZWN0cy5maWx0ZXIoZXN0YWRvPSJQRU5ESUVOVEUiKS5jb3VudCgpLAogICAgICAgICAgICAibG90ZXNfaW1wb3J0YWNpb24iOiBEYXRhSW1wb3J0QmF0Y2gub2JqZWN0cy5jb3VudCgpLAogICAgICAgICAgICAiaW1wb3J0YWNpb25lc19yZWNpZW50ZXMiOiBEYXRhSW1wb3J0QmF0Y2gub2JqZWN0cy5vcmRlcl9ieSgiLWNyZWF0ZWRfYXQiKVs6OF0sCiAgICAgICAgICAgICJhbGVydGFzX3JpZXNnbyI6IHNuYXBzLmZpbHRlcihhbGVydGE9VHJ1ZSkuY291bnQoKSwKICAgICAgICB9CiAgICB9CgoKQGxvZ2luX3JlcXVpcmVkCmRlZiBkYXNoYm9hcmRfaG9tZShyZXF1ZXN0KToKICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgImRhc2hib2FyZC9kYXNoYm9hcmRob21lLmh0bWwiKQoKCkBsb2dpbl9yZXF1aXJlZApkZWYgZXN0YWRvKHJlcXVlc3QpOgogICAgIiIiS1BJcyBlIGltcG9ydGFjaW9uZXMgcmVjaWVudGVzIOKAlCBhY2Nlc28gc2VjdW5kYXJpbyBkZXNkZSBlbCBtZW7Dui4iIiIKICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgInBvcnRhbC9lc3RhZG8uaHRtbCIsIF9wYW5lbF9zdGF0cygpKQoKCkBsb2dpbl9yZXF1aXJlZApkZWYgYXl1ZGEocmVxdWVzdCk6CiAgICByZXR1cm4gcmVuZGVyKHJlcXVlc3QsICJwb3J0YWwvYXl1ZGEuaHRtbCIpCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/__init__.py
PATH_JSON="reports/__init__.py"
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
PATH_LITERAL=reports/admin.py
PATH_JSON="reports/admin.py"
FILENAME=admin.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=44
SIZE_BYTES_UTF8=1202
CONTENT_SHA256=953fb09f4f38b9fd785246fba14daf3ea155f09850d895ca2ad07c863134d99f
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

from .models import ReportConfig


@admin.register(ReportConfig)
class ReportConfigAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "include_pgc_by_default",
        "include_pgo_by_default",
        "include_risk_by_default",
        "compact_mode",
        "updated_at",
    )
    list_filter = ("is_active", "compact_mode")
    search_fields = ("name", "intro_note")
    fieldsets = (
        (None, {"fields": ("name", "is_active", "intro_note")}),
        (
            "Defaults del checklist",
            {
                "fields": (
                    "include_admin_by_default",
                    "include_pgc_by_default",
                    "include_pgo_by_default",
                    "include_risk_by_default",
                )
            },
        ),
        (
            "Secciones y densidad",
            {
                "fields": (
                    "include_executive_summary",
                    "include_period_comparison",
                    "include_ai_section",
                    "compact_mode",
                    "max_table_rows",
                )
            },
        ),
    )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib import admin
00002|
00003|from .models import ReportConfig
00004|
00005|
00006|@admin.register(ReportConfig)
00007|class ReportConfigAdmin(admin.ModelAdmin):
00008|    list_display = (
00009|        "name",
00010|        "is_active",
00011|        "include_pgc_by_default",
00012|        "include_pgo_by_default",
00013|        "include_risk_by_default",
00014|        "compact_mode",
00015|        "updated_at",
00016|    )
00017|    list_filter = ("is_active", "compact_mode")
00018|    search_fields = ("name", "intro_note")
00019|    fieldsets = (
00020|        (None, {"fields": ("name", "is_active", "intro_note")}),
00021|        (
00022|            "Defaults del checklist",
00023|            {
00024|                "fields": (
00025|                    "include_admin_by_default",
00026|                    "include_pgc_by_default",
00027|                    "include_pgo_by_default",
00028|                    "include_risk_by_default",
00029|                )
00030|            },
00031|        ),
00032|        (
00033|            "Secciones y densidad",
00034|            {
00035|                "fields": (
00036|                    "include_executive_summary",
00037|                    "include_period_comparison",
00038|                    "include_ai_section",
00039|                    "compact_mode",
00040|                    "max_table_rows",
00041|                )
00042|            },
00043|        ),
00044|    )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgYWRtaW4KCmZyb20gLm1vZGVscyBpbXBvcnQgUmVwb3J0Q29uZmlnCgoKQGFkbWluLnJlZ2lzdGVyKFJlcG9ydENvbmZpZykKY2xhc3MgUmVwb3J0Q29uZmlnQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoCiAgICAgICAgIm5hbWUiLAogICAgICAgICJpc19hY3RpdmUiLAogICAgICAgICJpbmNsdWRlX3BnY19ieV9kZWZhdWx0IiwKICAgICAgICAiaW5jbHVkZV9wZ29fYnlfZGVmYXVsdCIsCiAgICAgICAgImluY2x1ZGVfcmlza19ieV9kZWZhdWx0IiwKICAgICAgICAiY29tcGFjdF9tb2RlIiwKICAgICAgICAidXBkYXRlZF9hdCIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgiaXNfYWN0aXZlIiwgImNvbXBhY3RfbW9kZSIpCiAgICBzZWFyY2hfZmllbGRzID0gKCJuYW1lIiwgImludHJvX25vdGUiKQogICAgZmllbGRzZXRzID0gKAogICAgICAgIChOb25lLCB7ImZpZWxkcyI6ICgibmFtZSIsICJpc19hY3RpdmUiLCAiaW50cm9fbm90ZSIpfSksCiAgICAgICAgKAogICAgICAgICAgICAiRGVmYXVsdHMgZGVsIGNoZWNrbGlzdCIsCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICJmaWVsZHMiOiAoCiAgICAgICAgICAgICAgICAgICAgImluY2x1ZGVfYWRtaW5fYnlfZGVmYXVsdCIsCiAgICAgICAgICAgICAgICAgICAgImluY2x1ZGVfcGdjX2J5X2RlZmF1bHQiLAogICAgICAgICAgICAgICAgICAgICJpbmNsdWRlX3Bnb19ieV9kZWZhdWx0IiwKICAgICAgICAgICAgICAgICAgICAiaW5jbHVkZV9yaXNrX2J5X2RlZmF1bHQiLAogICAgICAgICAgICAgICAgKQogICAgICAgICAgICB9LAogICAgICAgICksCiAgICAgICAgKAogICAgICAgICAgICAiU2VjY2lvbmVzIHkgZGVuc2lkYWQiLAogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAiZmllbGRzIjogKAogICAgICAgICAgICAgICAgICAgICJpbmNsdWRlX2V4ZWN1dGl2ZV9zdW1tYXJ5IiwKICAgICAgICAgICAgICAgICAgICAiaW5jbHVkZV9wZXJpb2RfY29tcGFyaXNvbiIsCiAgICAgICAgICAgICAgICAgICAgImluY2x1ZGVfYWlfc2VjdGlvbiIsCiAgICAgICAgICAgICAgICAgICAgImNvbXBhY3RfbW9kZSIsCiAgICAgICAgICAgICAgICAgICAgIm1heF90YWJsZV9yb3dzIiwKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgfSwKICAgICAgICApLAogICAgKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/apps.py
PATH_JSON="reports/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=7
SIZE_BYTES_UTF8=180
CONTENT_SHA256=7354a5c5ae1fa66cf16869b07ab8e3065bb6e5f8fda06ff2c89d18c6486f3a54
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


class ReportsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reports"
    verbose_name = "Reportes WCG"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class ReportsConfig(AppConfig):
00005|    default_auto_field = "django.db.models.BigAutoField"
00006|    name = "reports"
00007|    verbose_name = "Reportes WCG"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgUmVwb3J0c0NvbmZpZyhBcHBDb25maWcpOgogICAgZGVmYXVsdF9hdXRvX2ZpZWxkID0gImRqYW5nby5kYi5tb2RlbHMuQmlnQXV0b0ZpZWxkIgogICAgbmFtZSA9ICJyZXBvcnRzIgogICAgdmVyYm9zZV9uYW1lID0gIlJlcG9ydGVzIFdDRyIK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/md_utils.py
PATH_JSON="reports/md_utils.py"
FILENAME=md_utils.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=149
SIZE_BYTES_UTF8=4519
CONTENT_SHA256=135cdf39f098242695dc555869f697349fcab2640c54350ad01a617e355456d6
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
"""Helpers markdown compactos y seguros para lectores GFM/CommonMark."""

from __future__ import annotations

import re
from typing import Any, Iterable, Sequence

_HEADING_RE = re.compile(r"^#{1,6}\s+")
_TABLE_ROW_RE = re.compile(r"^\|")


def h1(text: str) -> str:
    return f"# {text}"


def h2(text: str) -> str:
    return f"## {text}"


def h3(text: str) -> str:
    return f"### {text}"


def p(text: str) -> str:
    """Bloque de texto. Conserva párrafos; normaliza CRLF → LF."""
    return str(text).replace("\r\n", "\n").replace("\r", "\n").strip()


def bullets(items: Iterable[str]) -> str:
    lines = []
    for item in items:
        if item is None:
            continue
        text = _inline(item)
        if text:
            lines.append(f"- {text}")
    return "\n".join(lines) if lines else "_Sin elementos._"


def _inline(value: Any) -> str:
    """Celda/texto inline: sin saltos de línea ni pipes crudos."""
    if value is None:
        return "—"
    text = str(value).replace("\r\n", "\n").replace("\r", "\n")
    text = " ".join(text.split())
    return text.replace("|", "\\|")


def md_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    """Tabla GFM (filas unidas por LF; blank lines externas las pone normalize_markdown)."""
    if not headers:
        return ""
    clean_headers = [_inline(h) for h in headers]
    head = "| " + " | ".join(clean_headers) + " |"
    sep = "| " + " | ".join("---" for _ in clean_headers) + " |"
    body = []
    n = len(clean_headers)
    for row in rows:
        cells = [_inline(c) for c in row]
        if len(cells) < n:
            cells.extend(["—"] * (n - len(cells)))
        body.append("| " + " | ".join(cells[:n]) + " |")
    return "\n".join([head, sep, *body])


def ai_closing(
    hechos: Sequence[str],
    cambios: Sequence[str],
    vacios: Sequence[str],
) -> str:
    return join_sections(
        h2("Hechos observables / Cambios relevantes / Vacíos de información"),
        h3("Hechos observables"),
        bullets(hechos or ["Sin hechos suficientes en los datos disponibles."]),
        h3("Cambios relevantes vs período anterior"),
        bullets(cambios or ["Sin período anterior comparable o sin cambios medibles."]),
        h3("Vacíos de información"),
        bullets(vacios or ["No se detectaron vacíos explícitos adicionales."]),
    )


def normalize_markdown(text: str) -> str:
    """
    Garantiza línea en blanco antes de:
    - títulos ATX (# … ######)
    - inicio de tabla GFM (| …)
    También línea en blanco después de títulos cuando sigue contenido.
    """
    text = str(text).replace("\r\n", "\n").replace("\r", "\n")
    raw_lines = text.split("\n")
    out: list[str] = []

    def ends_with_blank() -> bool:
        return not out or out[-1].strip() == ""

    i = 0
    while i < len(raw_lines):
        line = raw_lines[i]
        is_heading = bool(_HEADING_RE.match(line))
        is_table_start = bool(_TABLE_ROW_RE.match(line)) and (
            not out or not _TABLE_ROW_RE.match(out[-1] if out else "")
        )

        if is_heading or is_table_start:
            if out and not ends_with_blank():
                out.append("")

        out.append(line)

        if is_heading:
            # Blank line after heading if next non-empty line is not blank already.
            nxt = raw_lines[i + 1] if i + 1 < len(raw_lines) else None
            if nxt is not None and nxt.strip() != "":
                out.append("")

        i += 1

    # Collapse 3+ consecutive blanks → 1 blank (i.e. max one empty line between blocks).
    collapsed: list[str] = []
    blank_run = 0
    for line in out:
        if line.strip() == "":
            blank_run += 1
            if blank_run <= 1:
                collapsed.append("")
        else:
            blank_run = 0
            collapsed.append(line)

    # Trim leading blanks; ensure trailing single newline.
    while collapsed and collapsed[0] == "":
        collapsed.pop(0)
    while collapsed and collapsed[-1] == "":
        collapsed.pop()
    return "\n".join(collapsed) + "\n"


def join_sections(*sections: str) -> str:
    """
    Une bloques con línea en blanco entre ellos y normaliza el markdown final.
    """
    parts: list[str] = []
    for s in sections:
        if not s:
            continue
        cleaned = str(s).replace("\r\n", "\n").replace("\r", "\n").strip()
        if cleaned:
            parts.append(cleaned)
    return normalize_markdown("\n\n".join(parts))

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Helpers markdown compactos y seguros para lectores GFM/CommonMark."""
00002|
00003|from __future__ import annotations
00004|
00005|import re
00006|from typing import Any, Iterable, Sequence
00007|
00008|_HEADING_RE = re.compile(r"^#{1,6}\s+")
00009|_TABLE_ROW_RE = re.compile(r"^\|")
00010|
00011|
00012|def h1(text: str) -> str:
00013|    return f"# {text}"
00014|
00015|
00016|def h2(text: str) -> str:
00017|    return f"## {text}"
00018|
00019|
00020|def h3(text: str) -> str:
00021|    return f"### {text}"
00022|
00023|
00024|def p(text: str) -> str:
00025|    """Bloque de texto. Conserva párrafos; normaliza CRLF → LF."""
00026|    return str(text).replace("\r\n", "\n").replace("\r", "\n").strip()
00027|
00028|
00029|def bullets(items: Iterable[str]) -> str:
00030|    lines = []
00031|    for item in items:
00032|        if item is None:
00033|            continue
00034|        text = _inline(item)
00035|        if text:
00036|            lines.append(f"- {text}")
00037|    return "\n".join(lines) if lines else "_Sin elementos._"
00038|
00039|
00040|def _inline(value: Any) -> str:
00041|    """Celda/texto inline: sin saltos de línea ni pipes crudos."""
00042|    if value is None:
00043|        return "—"
00044|    text = str(value).replace("\r\n", "\n").replace("\r", "\n")
00045|    text = " ".join(text.split())
00046|    return text.replace("|", "\\|")
00047|
00048|
00049|def md_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
00050|    """Tabla GFM (filas unidas por LF; blank lines externas las pone normalize_markdown)."""
00051|    if not headers:
00052|        return ""
00053|    clean_headers = [_inline(h) for h in headers]
00054|    head = "| " + " | ".join(clean_headers) + " |"
00055|    sep = "| " + " | ".join("---" for _ in clean_headers) + " |"
00056|    body = []
00057|    n = len(clean_headers)
00058|    for row in rows:
00059|        cells = [_inline(c) for c in row]
00060|        if len(cells) < n:
00061|            cells.extend(["—"] * (n - len(cells)))
00062|        body.append("| " + " | ".join(cells[:n]) + " |")
00063|    return "\n".join([head, sep, *body])
00064|
00065|
00066|def ai_closing(
00067|    hechos: Sequence[str],
00068|    cambios: Sequence[str],
00069|    vacios: Sequence[str],
00070|) -> str:
00071|    return join_sections(
00072|        h2("Hechos observables / Cambios relevantes / Vacíos de información"),
00073|        h3("Hechos observables"),
00074|        bullets(hechos or ["Sin hechos suficientes en los datos disponibles."]),
00075|        h3("Cambios relevantes vs período anterior"),
00076|        bullets(cambios or ["Sin período anterior comparable o sin cambios medibles."]),
00077|        h3("Vacíos de información"),
00078|        bullets(vacios or ["No se detectaron vacíos explícitos adicionales."]),
00079|    )
00080|
00081|
00082|def normalize_markdown(text: str) -> str:
00083|    """
00084|    Garantiza línea en blanco antes de:
00085|    - títulos ATX (# … ######)
00086|    - inicio de tabla GFM (| …)
00087|    También línea en blanco después de títulos cuando sigue contenido.
00088|    """
00089|    text = str(text).replace("\r\n", "\n").replace("\r", "\n")
00090|    raw_lines = text.split("\n")
00091|    out: list[str] = []
00092|
00093|    def ends_with_blank() -> bool:
00094|        return not out or out[-1].strip() == ""
00095|
00096|    i = 0
00097|    while i < len(raw_lines):
00098|        line = raw_lines[i]
00099|        is_heading = bool(_HEADING_RE.match(line))
00100|        is_table_start = bool(_TABLE_ROW_RE.match(line)) and (
00101|            not out or not _TABLE_ROW_RE.match(out[-1] if out else "")
00102|        )
00103|
00104|        if is_heading or is_table_start:
00105|            if out and not ends_with_blank():
00106|                out.append("")
00107|
00108|        out.append(line)
00109|
00110|        if is_heading:
00111|            # Blank line after heading if next non-empty line is not blank already.
00112|            nxt = raw_lines[i + 1] if i + 1 < len(raw_lines) else None
00113|            if nxt is not None and nxt.strip() != "":
00114|                out.append("")
00115|
00116|        i += 1
00117|
00118|    # Collapse 3+ consecutive blanks → 1 blank (i.e. max one empty line between blocks).
00119|    collapsed: list[str] = []
00120|    blank_run = 0
00121|    for line in out:
00122|        if line.strip() == "":
00123|            blank_run += 1
00124|            if blank_run <= 1:
00125|                collapsed.append("")
00126|        else:
00127|            blank_run = 0
00128|            collapsed.append(line)
00129|
00130|    # Trim leading blanks; ensure trailing single newline.
00131|    while collapsed and collapsed[0] == "":
00132|        collapsed.pop(0)
00133|    while collapsed and collapsed[-1] == "":
00134|        collapsed.pop()
00135|    return "\n".join(collapsed) + "\n"
00136|
00137|
00138|def join_sections(*sections: str) -> str:
00139|    """
00140|    Une bloques con línea en blanco entre ellos y normaliza el markdown final.
00141|    """
00142|    parts: list[str] = []
00143|    for s in sections:
00144|        if not s:
00145|            continue
00146|        cleaned = str(s).replace("\r\n", "\n").replace("\r", "\n").strip()
00147|        if cleaned:
00148|            parts.append(cleaned)
00149|    return normalize_markdown("\n\n".join(parts))

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiSGVscGVycyBtYXJrZG93biBjb21wYWN0b3MgeSBzZWd1cm9zIHBhcmEgbGVjdG9yZXMgR0ZNL0NvbW1vbk1hcmsuIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgppbXBvcnQgcmUKZnJvbSB0eXBpbmcgaW1wb3J0IEFueSwgSXRlcmFibGUsIFNlcXVlbmNlCgpfSEVBRElOR19SRSA9IHJlLmNvbXBpbGUociJeI3sxLDZ9XHMrIikKX1RBQkxFX1JPV19SRSA9IHJlLmNvbXBpbGUociJeXHwiKQoKCmRlZiBoMSh0ZXh0OiBzdHIpIC0+IHN0cjoKICAgIHJldHVybiBmIiMge3RleHR9IgoKCmRlZiBoMih0ZXh0OiBzdHIpIC0+IHN0cjoKICAgIHJldHVybiBmIiMjIHt0ZXh0fSIKCgpkZWYgaDModGV4dDogc3RyKSAtPiBzdHI6CiAgICByZXR1cm4gZiIjIyMge3RleHR9IgoKCmRlZiBwKHRleHQ6IHN0cikgLT4gc3RyOgogICAgIiIiQmxvcXVlIGRlIHRleHRvLiBDb25zZXJ2YSBww6FycmFmb3M7IG5vcm1hbGl6YSBDUkxGIOKGkiBMRi4iIiIKICAgIHJldHVybiBzdHIodGV4dCkucmVwbGFjZSgiXHJcbiIsICJcbiIpLnJlcGxhY2UoIlxyIiwgIlxuIikuc3RyaXAoKQoKCmRlZiBidWxsZXRzKGl0ZW1zOiBJdGVyYWJsZVtzdHJdKSAtPiBzdHI6CiAgICBsaW5lcyA9IFtdCiAgICBmb3IgaXRlbSBpbiBpdGVtczoKICAgICAgICBpZiBpdGVtIGlzIE5vbmU6CiAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgdGV4dCA9IF9pbmxpbmUoaXRlbSkKICAgICAgICBpZiB0ZXh0OgogICAgICAgICAgICBsaW5lcy5hcHBlbmQoZiItIHt0ZXh0fSIpCiAgICByZXR1cm4gIlxuIi5qb2luKGxpbmVzKSBpZiBsaW5lcyBlbHNlICJfU2luIGVsZW1lbnRvcy5fIgoKCmRlZiBfaW5saW5lKHZhbHVlOiBBbnkpIC0+IHN0cjoKICAgICIiIkNlbGRhL3RleHRvIGlubGluZTogc2luIHNhbHRvcyBkZSBsw61uZWEgbmkgcGlwZXMgY3J1ZG9zLiIiIgogICAgaWYgdmFsdWUgaXMgTm9uZToKICAgICAgICByZXR1cm4gIuKAlCIKICAgIHRleHQgPSBzdHIodmFsdWUpLnJlcGxhY2UoIlxyXG4iLCAiXG4iKS5yZXBsYWNlKCJcciIsICJcbiIpCiAgICB0ZXh0ID0gIiAiLmpvaW4odGV4dC5zcGxpdCgpKQogICAgcmV0dXJuIHRleHQucmVwbGFjZSgifCIsICJcXHwiKQoKCmRlZiBtZF90YWJsZShoZWFkZXJzOiBTZXF1ZW5jZVtzdHJdLCByb3dzOiBTZXF1ZW5jZVtTZXF1ZW5jZVtBbnldXSkgLT4gc3RyOgogICAgIiIiVGFibGEgR0ZNIChmaWxhcyB1bmlkYXMgcG9yIExGOyBibGFuayBsaW5lcyBleHRlcm5hcyBsYXMgcG9uZSBub3JtYWxpemVfbWFya2Rvd24pLiIiIgogICAgaWYgbm90IGhlYWRlcnM6CiAgICAgICAgcmV0dXJuICIiCiAgICBjbGVhbl9oZWFkZXJzID0gW19pbmxpbmUoaCkgZm9yIGggaW4gaGVhZGVyc10KICAgIGhlYWQgPSAifCAiICsgIiB8ICIuam9pbihjbGVhbl9oZWFkZXJzKSArICIgfCIKICAgIHNlcCA9ICJ8ICIgKyAiIHwgIi5qb2luKCItLS0iIGZvciBfIGluIGNsZWFuX2hlYWRlcnMpICsgIiB8IgogICAgYm9keSA9IFtdCiAgICBuID0gbGVuKGNsZWFuX2hlYWRlcnMpCiAgICBmb3Igcm93IGluIHJvd3M6CiAgICAgICAgY2VsbHMgPSBbX2lubGluZShjKSBmb3IgYyBpbiByb3ddCiAgICAgICAgaWYgbGVuKGNlbGxzKSA8IG46CiAgICAgICAgICAgIGNlbGxzLmV4dGVuZChbIuKAlCJdICogKG4gLSBsZW4oY2VsbHMpKSkKICAgICAgICBib2R5LmFwcGVuZCgifCAiICsgIiB8ICIuam9pbihjZWxsc1s6bl0pICsgIiB8IikKICAgIHJldHVybiAiXG4iLmpvaW4oW2hlYWQsIHNlcCwgKmJvZHldKQoKCmRlZiBhaV9jbG9zaW5nKAogICAgaGVjaG9zOiBTZXF1ZW5jZVtzdHJdLAogICAgY2FtYmlvczogU2VxdWVuY2Vbc3RyXSwKICAgIHZhY2lvczogU2VxdWVuY2Vbc3RyXSwKKSAtPiBzdHI6CiAgICByZXR1cm4gam9pbl9zZWN0aW9ucygKICAgICAgICBoMigiSGVjaG9zIG9ic2VydmFibGVzIC8gQ2FtYmlvcyByZWxldmFudGVzIC8gVmFjw61vcyBkZSBpbmZvcm1hY2nDs24iKSwKICAgICAgICBoMygiSGVjaG9zIG9ic2VydmFibGVzIiksCiAgICAgICAgYnVsbGV0cyhoZWNob3Mgb3IgWyJTaW4gaGVjaG9zIHN1ZmljaWVudGVzIGVuIGxvcyBkYXRvcyBkaXNwb25pYmxlcy4iXSksCiAgICAgICAgaDMoIkNhbWJpb3MgcmVsZXZhbnRlcyB2cyBwZXLDrW9kbyBhbnRlcmlvciIpLAogICAgICAgIGJ1bGxldHMoY2FtYmlvcyBvciBbIlNpbiBwZXLDrW9kbyBhbnRlcmlvciBjb21wYXJhYmxlIG8gc2luIGNhbWJpb3MgbWVkaWJsZXMuIl0pLAogICAgICAgIGgzKCJWYWPDrW9zIGRlIGluZm9ybWFjacOzbiIpLAogICAgICAgIGJ1bGxldHModmFjaW9zIG9yIFsiTm8gc2UgZGV0ZWN0YXJvbiB2YWPDrW9zIGV4cGzDrWNpdG9zIGFkaWNpb25hbGVzLiJdKSwKICAgICkKCgpkZWYgbm9ybWFsaXplX21hcmtkb3duKHRleHQ6IHN0cikgLT4gc3RyOgogICAgIiIiCiAgICBHYXJhbnRpemEgbMOtbmVhIGVuIGJsYW5jbyBhbnRlcyBkZToKICAgIC0gdMOtdHVsb3MgQVRYICgjIOKApiAjIyMjIyMpCiAgICAtIGluaWNpbyBkZSB0YWJsYSBHRk0gKHwg4oCmKQogICAgVGFtYmnDqW4gbMOtbmVhIGVuIGJsYW5jbyBkZXNwdcOpcyBkZSB0w610dWxvcyBjdWFuZG8gc2lndWUgY29udGVuaWRvLgogICAgIiIiCiAgICB0ZXh0ID0gc3RyKHRleHQpLnJlcGxhY2UoIlxyXG4iLCAiXG4iKS5yZXBsYWNlKCJcciIsICJcbiIpCiAgICByYXdfbGluZXMgPSB0ZXh0LnNwbGl0KCJcbiIpCiAgICBvdXQ6IGxpc3Rbc3RyXSA9IFtdCgogICAgZGVmIGVuZHNfd2l0aF9ibGFuaygpIC0+IGJvb2w6CiAgICAgICAgcmV0dXJuIG5vdCBvdXQgb3Igb3V0Wy0xXS5zdHJpcCgpID09ICIiCgogICAgaSA9IDAKICAgIHdoaWxlIGkgPCBsZW4ocmF3X2xpbmVzKToKICAgICAgICBsaW5lID0gcmF3X2xpbmVzW2ldCiAgICAgICAgaXNfaGVhZGluZyA9IGJvb2woX0hFQURJTkdfUkUubWF0Y2gobGluZSkpCiAgICAgICAgaXNfdGFibGVfc3RhcnQgPSBib29sKF9UQUJMRV9ST1dfUkUubWF0Y2gobGluZSkpIGFuZCAoCiAgICAgICAgICAgIG5vdCBvdXQgb3Igbm90IF9UQUJMRV9ST1dfUkUubWF0Y2gob3V0Wy0xXSBpZiBvdXQgZWxzZSAiIikKICAgICAgICApCgogICAgICAgIGlmIGlzX2hlYWRpbmcgb3IgaXNfdGFibGVfc3RhcnQ6CiAgICAgICAgICAgIGlmIG91dCBhbmQgbm90IGVuZHNfd2l0aF9ibGFuaygpOgogICAgICAgICAgICAgICAgb3V0LmFwcGVuZCgiIikKCiAgICAgICAgb3V0LmFwcGVuZChsaW5lKQoKICAgICAgICBpZiBpc19oZWFkaW5nOgogICAgICAgICAgICAjIEJsYW5rIGxpbmUgYWZ0ZXIgaGVhZGluZyBpZiBuZXh0IG5vbi1lbXB0eSBsaW5lIGlzIG5vdCBibGFuayBhbHJlYWR5LgogICAgICAgICAgICBueHQgPSByYXdfbGluZXNbaSArIDFdIGlmIGkgKyAxIDwgbGVuKHJhd19saW5lcykgZWxzZSBOb25lCiAgICAgICAgICAgIGlmIG54dCBpcyBub3QgTm9uZSBhbmQgbnh0LnN0cmlwKCkgIT0gIiI6CiAgICAgICAgICAgICAgICBvdXQuYXBwZW5kKCIiKQoKICAgICAgICBpICs9IDEKCiAgICAjIENvbGxhcHNlIDMrIGNvbnNlY3V0aXZlIGJsYW5rcyDihpIgMSBibGFuayAoaS5lLiBtYXggb25lIGVtcHR5IGxpbmUgYmV0d2VlbiBibG9ja3MpLgogICAgY29sbGFwc2VkOiBsaXN0W3N0cl0gPSBbXQogICAgYmxhbmtfcnVuID0gMAogICAgZm9yIGxpbmUgaW4gb3V0OgogICAgICAgIGlmIGxpbmUuc3RyaXAoKSA9PSAiIjoKICAgICAgICAgICAgYmxhbmtfcnVuICs9IDEKICAgICAgICAgICAgaWYgYmxhbmtfcnVuIDw9IDE6CiAgICAgICAgICAgICAgICBjb2xsYXBzZWQuYXBwZW5kKCIiKQogICAgICAgIGVsc2U6CiAgICAgICAgICAgIGJsYW5rX3J1biA9IDAKICAgICAgICAgICAgY29sbGFwc2VkLmFwcGVuZChsaW5lKQoKICAgICMgVHJpbSBsZWFkaW5nIGJsYW5rczsgZW5zdXJlIHRyYWlsaW5nIHNpbmdsZSBuZXdsaW5lLgogICAgd2hpbGUgY29sbGFwc2VkIGFuZCBjb2xsYXBzZWRbMF0gPT0gIiI6CiAgICAgICAgY29sbGFwc2VkLnBvcCgwKQogICAgd2hpbGUgY29sbGFwc2VkIGFuZCBjb2xsYXBzZWRbLTFdID09ICIiOgogICAgICAgIGNvbGxhcHNlZC5wb3AoKQogICAgcmV0dXJuICJcbiIuam9pbihjb2xsYXBzZWQpICsgIlxuIgoKCmRlZiBqb2luX3NlY3Rpb25zKCpzZWN0aW9uczogc3RyKSAtPiBzdHI6CiAgICAiIiIKICAgIFVuZSBibG9xdWVzIGNvbiBsw61uZWEgZW4gYmxhbmNvIGVudHJlIGVsbG9zIHkgbm9ybWFsaXphIGVsIG1hcmtkb3duIGZpbmFsLgogICAgIiIiCiAgICBwYXJ0czogbGlzdFtzdHJdID0gW10KICAgIGZvciBzIGluIHNlY3Rpb25zOgogICAgICAgIGlmIG5vdCBzOgogICAgICAgICAgICBjb250aW51ZQogICAgICAgIGNsZWFuZWQgPSBzdHIocykucmVwbGFjZSgiXHJcbiIsICJcbiIpLnJlcGxhY2UoIlxyIiwgIlxuIikuc3RyaXAoKQogICAgICAgIGlmIGNsZWFuZWQ6CiAgICAgICAgICAgIHBhcnRzLmFwcGVuZChjbGVhbmVkKQogICAgcmV0dXJuIG5vcm1hbGl6ZV9tYXJrZG93bigiXG5cbiIuam9pbihwYXJ0cykpCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/models.py
PATH_JSON="reports/models.py"
FILENAME=models.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=42
SIZE_BYTES_UTF8=1537
CONTENT_SHA256=24d5c36da94ec9f94a8d6562e7fa9352ee3bcd25cae5010ee4af4c6bc3d0a13b
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

from core.models import TimeStampedModel


class ReportConfig(TimeStampedModel):
    """Configuración ampliable para generación de reportes desde PGC."""

    name = models.CharField(max_length=80, unique=True, default="default")
    is_active = models.BooleanField(default=True)

    include_admin_by_default = models.BooleanField(default=False)
    include_pgc_by_default = models.BooleanField(default=True)
    include_pgo_by_default = models.BooleanField(default=False)
    include_risk_by_default = models.BooleanField(default=False)

    include_executive_summary = models.BooleanField(default=True)
    include_period_comparison = models.BooleanField(default=True)
    include_ai_section = models.BooleanField(default=True)
    compact_mode = models.BooleanField(
        default=True,
        help_text="Limita tablas y listas a hallazgos de alta densidad.",
    )
    max_table_rows = models.PositiveIntegerField(default=25)
    intro_note = models.TextField(
        blank=True,
        help_text="Nota opcional al inicio de cada reporte de resultados.",
    )

    class Meta:
        verbose_name = "Configuración de reportes"
        verbose_name_plural = "Configuraciones de reportes"

    def __str__(self):
        return f"ReportConfig:{self.name}"

    @classmethod
    def get_active(cls) -> "ReportConfig":
        obj = cls.objects.filter(is_active=True).order_by("id").first()
        if obj:
            return obj
        return cls.objects.create(name="default", is_active=True)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.db import models
00002|
00003|from core.models import TimeStampedModel
00004|
00005|
00006|class ReportConfig(TimeStampedModel):
00007|    """Configuración ampliable para generación de reportes desde PGC."""
00008|
00009|    name = models.CharField(max_length=80, unique=True, default="default")
00010|    is_active = models.BooleanField(default=True)
00011|
00012|    include_admin_by_default = models.BooleanField(default=False)
00013|    include_pgc_by_default = models.BooleanField(default=True)
00014|    include_pgo_by_default = models.BooleanField(default=False)
00015|    include_risk_by_default = models.BooleanField(default=False)
00016|
00017|    include_executive_summary = models.BooleanField(default=True)
00018|    include_period_comparison = models.BooleanField(default=True)
00019|    include_ai_section = models.BooleanField(default=True)
00020|    compact_mode = models.BooleanField(
00021|        default=True,
00022|        help_text="Limita tablas y listas a hallazgos de alta densidad.",
00023|    )
00024|    max_table_rows = models.PositiveIntegerField(default=25)
00025|    intro_note = models.TextField(
00026|        blank=True,
00027|        help_text="Nota opcional al inicio de cada reporte de resultados.",
00028|    )
00029|
00030|    class Meta:
00031|        verbose_name = "Configuración de reportes"
00032|        verbose_name_plural = "Configuraciones de reportes"
00033|
00034|    def __str__(self):
00035|        return f"ReportConfig:{self.name}"
00036|
00037|    @classmethod
00038|    def get_active(cls) -> "ReportConfig":
00039|        obj = cls.objects.filter(is_active=True).order_by("id").first()
00040|        if obj:
00041|            return obj
00042|        return cls.objects.create(name="default", is_active=True)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uZGIgaW1wb3J0IG1vZGVscwoKZnJvbSBjb3JlLm1vZGVscyBpbXBvcnQgVGltZVN0YW1wZWRNb2RlbAoKCmNsYXNzIFJlcG9ydENvbmZpZyhUaW1lU3RhbXBlZE1vZGVsKToKICAgICIiIkNvbmZpZ3VyYWNpw7NuIGFtcGxpYWJsZSBwYXJhIGdlbmVyYWNpw7NuIGRlIHJlcG9ydGVzIGRlc2RlIFBHQy4iIiIKCiAgICBuYW1lID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTgwLCB1bmlxdWU9VHJ1ZSwgZGVmYXVsdD0iZGVmYXVsdCIpCiAgICBpc19hY3RpdmUgPSBtb2RlbHMuQm9vbGVhbkZpZWxkKGRlZmF1bHQ9VHJ1ZSkKCiAgICBpbmNsdWRlX2FkbWluX2J5X2RlZmF1bHQgPSBtb2RlbHMuQm9vbGVhbkZpZWxkKGRlZmF1bHQ9RmFsc2UpCiAgICBpbmNsdWRlX3BnY19ieV9kZWZhdWx0ID0gbW9kZWxzLkJvb2xlYW5GaWVsZChkZWZhdWx0PVRydWUpCiAgICBpbmNsdWRlX3Bnb19ieV9kZWZhdWx0ID0gbW9kZWxzLkJvb2xlYW5GaWVsZChkZWZhdWx0PUZhbHNlKQogICAgaW5jbHVkZV9yaXNrX2J5X2RlZmF1bHQgPSBtb2RlbHMuQm9vbGVhbkZpZWxkKGRlZmF1bHQ9RmFsc2UpCgogICAgaW5jbHVkZV9leGVjdXRpdmVfc3VtbWFyeSA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1UcnVlKQogICAgaW5jbHVkZV9wZXJpb2RfY29tcGFyaXNvbiA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1UcnVlKQogICAgaW5jbHVkZV9haV9zZWN0aW9uID0gbW9kZWxzLkJvb2xlYW5GaWVsZChkZWZhdWx0PVRydWUpCiAgICBjb21wYWN0X21vZGUgPSBtb2RlbHMuQm9vbGVhbkZpZWxkKAogICAgICAgIGRlZmF1bHQ9VHJ1ZSwKICAgICAgICBoZWxwX3RleHQ9IkxpbWl0YSB0YWJsYXMgeSBsaXN0YXMgYSBoYWxsYXpnb3MgZGUgYWx0YSBkZW5zaWRhZC4iLAogICAgKQogICAgbWF4X3RhYmxlX3Jvd3MgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoZGVmYXVsdD0yNSkKICAgIGludHJvX25vdGUgPSBtb2RlbHMuVGV4dEZpZWxkKAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgaGVscF90ZXh0PSJOb3RhIG9wY2lvbmFsIGFsIGluaWNpbyBkZSBjYWRhIHJlcG9ydGUgZGUgcmVzdWx0YWRvcy4iLAogICAgKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgdmVyYm9zZV9uYW1lID0gIkNvbmZpZ3VyYWNpw7NuIGRlIHJlcG9ydGVzIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiQ29uZmlndXJhY2lvbmVzIGRlIHJlcG9ydGVzIgoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIlJlcG9ydENvbmZpZzp7c2VsZi5uYW1lfSIKCiAgICBAY2xhc3NtZXRob2QKICAgIGRlZiBnZXRfYWN0aXZlKGNscykgLT4gIlJlcG9ydENvbmZpZyI6CiAgICAgICAgb2JqID0gY2xzLm9iamVjdHMuZmlsdGVyKGlzX2FjdGl2ZT1UcnVlKS5vcmRlcl9ieSgiaWQiKS5maXJzdCgpCiAgICAgICAgaWYgb2JqOgogICAgICAgICAgICByZXR1cm4gb2JqCiAgICAgICAgcmV0dXJuIGNscy5vYmplY3RzLmNyZWF0ZShuYW1lPSJkZWZhdWx0IiwgaXNfYWN0aXZlPVRydWUpCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/naming.py
PATH_JSON="reports/naming.py"
FILENAME=naming.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=21
SIZE_BYTES_UTF8=613
CONTENT_SHA256=0da657589da17a847dc56fe0eb6a41517b42f708160f55a2fc851db8c58d6635
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
"""Utilidades de nombres y hora para archivos de reportes."""

from __future__ import annotations

from datetime import datetime

from django.utils import timezone


def report_stamp(now: datetime | None = None) -> str:
    """
    Sufijo obligatorio: ' yy-mm hh-mm' (espacio + yy-mm + espacio + hh-mm).
    Usa zona horaria Django (America/Guatemala).
    """
    now = now or timezone.localtime()
    return f" {now.strftime('%y-%m')} {now.strftime('%H-%M')}"


def stamp_filename(stem: str, ext: str, now: datetime | None = None) -> str:
    ext = ext.lstrip(".")
    return f"{stem}{report_stamp(now)}.{ext}"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Utilidades de nombres y hora para archivos de reportes."""
00002|
00003|from __future__ import annotations
00004|
00005|from datetime import datetime
00006|
00007|from django.utils import timezone
00008|
00009|
00010|def report_stamp(now: datetime | None = None) -> str:
00011|    """
00012|    Sufijo obligatorio: ' yy-mm hh-mm' (espacio + yy-mm + espacio + hh-mm).
00013|    Usa zona horaria Django (America/Guatemala).
00014|    """
00015|    now = now or timezone.localtime()
00016|    return f" {now.strftime('%y-%m')} {now.strftime('%H-%M')}"
00017|
00018|
00019|def stamp_filename(stem: str, ext: str, now: datetime | None = None) -> str:
00020|    ext = ext.lstrip(".")
00021|    return f"{stem}{report_stamp(now)}.{ext}"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiVXRpbGlkYWRlcyBkZSBub21icmVzIHkgaG9yYSBwYXJhIGFyY2hpdm9zIGRlIHJlcG9ydGVzLiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKZnJvbSBkYXRldGltZSBpbXBvcnQgZGF0ZXRpbWUKCmZyb20gZGphbmdvLnV0aWxzIGltcG9ydCB0aW1lem9uZQoKCmRlZiByZXBvcnRfc3RhbXAobm93OiBkYXRldGltZSB8IE5vbmUgPSBOb25lKSAtPiBzdHI6CiAgICAiIiIKICAgIFN1ZmlqbyBvYmxpZ2F0b3JpbzogJyB5eS1tbSBoaC1tbScgKGVzcGFjaW8gKyB5eS1tbSArIGVzcGFjaW8gKyBoaC1tbSkuCiAgICBVc2Egem9uYSBob3JhcmlhIERqYW5nbyAoQW1lcmljYS9HdWF0ZW1hbGEpLgogICAgIiIiCiAgICBub3cgPSBub3cgb3IgdGltZXpvbmUubG9jYWx0aW1lKCkKICAgIHJldHVybiBmIiB7bm93LnN0cmZ0aW1lKCcleS0lbScpfSB7bm93LnN0cmZ0aW1lKCclSC0lTScpfSIKCgpkZWYgc3RhbXBfZmlsZW5hbWUoc3RlbTogc3RyLCBleHQ6IHN0ciwgbm93OiBkYXRldGltZSB8IE5vbmUgPSBOb25lKSAtPiBzdHI6CiAgICBleHQgPSBleHQubHN0cmlwKCIuIikKICAgIHJldHVybiBmIntzdGVtfXtyZXBvcnRfc3RhbXAobm93KX0ue2V4dH0iCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/services/__init__.py
PATH_JSON="reports/services/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=98
SIZE_BYTES_UTF8=3433
CONTENT_SHA256=56463ed4ee04a3220657eeeac155b40100d1700ff2e92bf6d6f904f9dd66c25e
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
"""Orquestación: genera archivos y empaqueta ZIP cuando corresponde."""

from __future__ import annotations

import zipfile
from io import BytesIO
from typing import Iterable

from django.utils import timezone

from reports.models import ReportConfig
from reports.naming import stamp_filename
from reports.services.coverage import build_admin_coverage_md
from reports.services.pgc_results import build_pgc_results
from reports.services.pgo_results import build_pgo_results
from reports.services.risk_results import build_risk_results
from reports.xlsx_utils import build_workbook

AREA_ADMIN = "admin"
AREA_PGC = "pgc"
AREA_PGO = "pgo"
AREA_RISK = "risk"

VALID_AREAS = {AREA_ADMIN, AREA_PGC, AREA_PGO, AREA_RISK}


def generate_report_package(areas: Iterable[str]) -> tuple[str, bytes, str]:
    """
    Returns (filename, content_bytes, content_type).
    ZIP if more than one file; otherwise single file.
    """
    selected = [a for a in areas if a in VALID_AREAS]
    if not selected:
        raise ValueError("Debe seleccionar al menos un área de reporte.")

    cfg = ReportConfig.get_active()
    now = timezone.localtime()
    files: list[tuple[str, bytes]] = []

    if AREA_ADMIN in selected:
        md = build_admin_coverage_md(cfg)
        files.append(
            (
                stamp_filename("reporte_administracion", "md", now),
                md.encode("utf-8"),
            )
        )

    if AREA_PGC in selected:
        data = build_pgc_results(cfg)
        files.append(
            (stamp_filename("reporte_pgc", "md", now), data["md"].encode("utf-8"))
        )
        xlsx = build_workbook(
            data["sheets"],
            report_title="Reporte PGC — tablas",
            stamp_label=data.get("stamp_label") or stamp_filename("reporte_pgc", "xlsx", now),
        )
        files.append((stamp_filename("reporte_pgc_tablas", "xlsx", now), xlsx))

    if AREA_PGO in selected:
        data = build_pgo_results(cfg)
        files.append(
            (stamp_filename("reporte_pgo", "md", now), data["md"].encode("utf-8"))
        )
        xlsx = build_workbook(
            data["sheets"],
            report_title="Reporte PGO — tablas",
            stamp_label=data.get("stamp_label") or stamp_filename("reporte_pgo", "xlsx", now),
        )
        files.append((stamp_filename("reporte_pgo_tablas", "xlsx", now), xlsx))

    if AREA_RISK in selected:
        data = build_risk_results(cfg)
        files.append(
            (stamp_filename("reporte_briesgo", "md", now), data["md"].encode("utf-8"))
        )
        xlsx = build_workbook(
            data["sheets"],
            report_title="Reporte B. Riesgo — tablas",
            stamp_label=data.get("stamp_label") or stamp_filename("reporte_briesgo", "xlsx", now),
        )
        files.append((stamp_filename("reporte_briesgo_tablas", "xlsx", now), xlsx))

    if len(files) == 1:
        name, content = files[0]
        if name.endswith(".md"):
            ctype = "text/markdown; charset=utf-8"
        else:
            ctype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return name, content, ctype

    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, content in files:
            zf.writestr(name, content)
    zip_name = stamp_filename("reportes_wcg", "zip", now)
    return zip_name, buf.getvalue(), "application/zip"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Orquestación: genera archivos y empaqueta ZIP cuando corresponde."""
00002|
00003|from __future__ import annotations
00004|
00005|import zipfile
00006|from io import BytesIO
00007|from typing import Iterable
00008|
00009|from django.utils import timezone
00010|
00011|from reports.models import ReportConfig
00012|from reports.naming import stamp_filename
00013|from reports.services.coverage import build_admin_coverage_md
00014|from reports.services.pgc_results import build_pgc_results
00015|from reports.services.pgo_results import build_pgo_results
00016|from reports.services.risk_results import build_risk_results
00017|from reports.xlsx_utils import build_workbook
00018|
00019|AREA_ADMIN = "admin"
00020|AREA_PGC = "pgc"
00021|AREA_PGO = "pgo"
00022|AREA_RISK = "risk"
00023|
00024|VALID_AREAS = {AREA_ADMIN, AREA_PGC, AREA_PGO, AREA_RISK}
00025|
00026|
00027|def generate_report_package(areas: Iterable[str]) -> tuple[str, bytes, str]:
00028|    """
00029|    Returns (filename, content_bytes, content_type).
00030|    ZIP if more than one file; otherwise single file.
00031|    """
00032|    selected = [a for a in areas if a in VALID_AREAS]
00033|    if not selected:
00034|        raise ValueError("Debe seleccionar al menos un área de reporte.")
00035|
00036|    cfg = ReportConfig.get_active()
00037|    now = timezone.localtime()
00038|    files: list[tuple[str, bytes]] = []
00039|
00040|    if AREA_ADMIN in selected:
00041|        md = build_admin_coverage_md(cfg)
00042|        files.append(
00043|            (
00044|                stamp_filename("reporte_administracion", "md", now),
00045|                md.encode("utf-8"),
00046|            )
00047|        )
00048|
00049|    if AREA_PGC in selected:
00050|        data = build_pgc_results(cfg)
00051|        files.append(
00052|            (stamp_filename("reporte_pgc", "md", now), data["md"].encode("utf-8"))
00053|        )
00054|        xlsx = build_workbook(
00055|            data["sheets"],
00056|            report_title="Reporte PGC — tablas",
00057|            stamp_label=data.get("stamp_label") or stamp_filename("reporte_pgc", "xlsx", now),
00058|        )
00059|        files.append((stamp_filename("reporte_pgc_tablas", "xlsx", now), xlsx))
00060|
00061|    if AREA_PGO in selected:
00062|        data = build_pgo_results(cfg)
00063|        files.append(
00064|            (stamp_filename("reporte_pgo", "md", now), data["md"].encode("utf-8"))
00065|        )
00066|        xlsx = build_workbook(
00067|            data["sheets"],
00068|            report_title="Reporte PGO — tablas",
00069|            stamp_label=data.get("stamp_label") or stamp_filename("reporte_pgo", "xlsx", now),
00070|        )
00071|        files.append((stamp_filename("reporte_pgo_tablas", "xlsx", now), xlsx))
00072|
00073|    if AREA_RISK in selected:
00074|        data = build_risk_results(cfg)
00075|        files.append(
00076|            (stamp_filename("reporte_briesgo", "md", now), data["md"].encode("utf-8"))
00077|        )
00078|        xlsx = build_workbook(
00079|            data["sheets"],
00080|            report_title="Reporte B. Riesgo — tablas",
00081|            stamp_label=data.get("stamp_label") or stamp_filename("reporte_briesgo", "xlsx", now),
00082|        )
00083|        files.append((stamp_filename("reporte_briesgo_tablas", "xlsx", now), xlsx))
00084|
00085|    if len(files) == 1:
00086|        name, content = files[0]
00087|        if name.endswith(".md"):
00088|            ctype = "text/markdown; charset=utf-8"
00089|        else:
00090|            ctype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
00091|        return name, content, ctype
00092|
00093|    buf = BytesIO()
00094|    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
00095|        for name, content in files:
00096|            zf.writestr(name, content)
00097|    zip_name = stamp_filename("reportes_wcg", "zip", now)
00098|    return zip_name, buf.getvalue(), "application/zip"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiT3JxdWVzdGFjacOzbjogZ2VuZXJhIGFyY2hpdm9zIHkgZW1wYXF1ZXRhIFpJUCBjdWFuZG8gY29ycmVzcG9uZGUuIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgppbXBvcnQgemlwZmlsZQpmcm9tIGlvIGltcG9ydCBCeXRlc0lPCmZyb20gdHlwaW5nIGltcG9ydCBJdGVyYWJsZQoKZnJvbSBkamFuZ28udXRpbHMgaW1wb3J0IHRpbWV6b25lCgpmcm9tIHJlcG9ydHMubW9kZWxzIGltcG9ydCBSZXBvcnRDb25maWcKZnJvbSByZXBvcnRzLm5hbWluZyBpbXBvcnQgc3RhbXBfZmlsZW5hbWUKZnJvbSByZXBvcnRzLnNlcnZpY2VzLmNvdmVyYWdlIGltcG9ydCBidWlsZF9hZG1pbl9jb3ZlcmFnZV9tZApmcm9tIHJlcG9ydHMuc2VydmljZXMucGdjX3Jlc3VsdHMgaW1wb3J0IGJ1aWxkX3BnY19yZXN1bHRzCmZyb20gcmVwb3J0cy5zZXJ2aWNlcy5wZ29fcmVzdWx0cyBpbXBvcnQgYnVpbGRfcGdvX3Jlc3VsdHMKZnJvbSByZXBvcnRzLnNlcnZpY2VzLnJpc2tfcmVzdWx0cyBpbXBvcnQgYnVpbGRfcmlza19yZXN1bHRzCmZyb20gcmVwb3J0cy54bHN4X3V0aWxzIGltcG9ydCBidWlsZF93b3JrYm9vawoKQVJFQV9BRE1JTiA9ICJhZG1pbiIKQVJFQV9QR0MgPSAicGdjIgpBUkVBX1BHTyA9ICJwZ28iCkFSRUFfUklTSyA9ICJyaXNrIgoKVkFMSURfQVJFQVMgPSB7QVJFQV9BRE1JTiwgQVJFQV9QR0MsIEFSRUFfUEdPLCBBUkVBX1JJU0t9CgoKZGVmIGdlbmVyYXRlX3JlcG9ydF9wYWNrYWdlKGFyZWFzOiBJdGVyYWJsZVtzdHJdKSAtPiB0dXBsZVtzdHIsIGJ5dGVzLCBzdHJdOgogICAgIiIiCiAgICBSZXR1cm5zIChmaWxlbmFtZSwgY29udGVudF9ieXRlcywgY29udGVudF90eXBlKS4KICAgIFpJUCBpZiBtb3JlIHRoYW4gb25lIGZpbGU7IG90aGVyd2lzZSBzaW5nbGUgZmlsZS4KICAgICIiIgogICAgc2VsZWN0ZWQgPSBbYSBmb3IgYSBpbiBhcmVhcyBpZiBhIGluIFZBTElEX0FSRUFTXQogICAgaWYgbm90IHNlbGVjdGVkOgogICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoIkRlYmUgc2VsZWNjaW9uYXIgYWwgbWVub3MgdW4gw6FyZWEgZGUgcmVwb3J0ZS4iKQoKICAgIGNmZyA9IFJlcG9ydENvbmZpZy5nZXRfYWN0aXZlKCkKICAgIG5vdyA9IHRpbWV6b25lLmxvY2FsdGltZSgpCiAgICBmaWxlczogbGlzdFt0dXBsZVtzdHIsIGJ5dGVzXV0gPSBbXQoKICAgIGlmIEFSRUFfQURNSU4gaW4gc2VsZWN0ZWQ6CiAgICAgICAgbWQgPSBidWlsZF9hZG1pbl9jb3ZlcmFnZV9tZChjZmcpCiAgICAgICAgZmlsZXMuYXBwZW5kKAogICAgICAgICAgICAoCiAgICAgICAgICAgICAgICBzdGFtcF9maWxlbmFtZSgicmVwb3J0ZV9hZG1pbmlzdHJhY2lvbiIsICJtZCIsIG5vdyksCiAgICAgICAgICAgICAgICBtZC5lbmNvZGUoInV0Zi04IiksCiAgICAgICAgICAgICkKICAgICAgICApCgogICAgaWYgQVJFQV9QR0MgaW4gc2VsZWN0ZWQ6CiAgICAgICAgZGF0YSA9IGJ1aWxkX3BnY19yZXN1bHRzKGNmZykKICAgICAgICBmaWxlcy5hcHBlbmQoCiAgICAgICAgICAgIChzdGFtcF9maWxlbmFtZSgicmVwb3J0ZV9wZ2MiLCAibWQiLCBub3cpLCBkYXRhWyJtZCJdLmVuY29kZSgidXRmLTgiKSkKICAgICAgICApCiAgICAgICAgeGxzeCA9IGJ1aWxkX3dvcmtib29rKAogICAgICAgICAgICBkYXRhWyJzaGVldHMiXSwKICAgICAgICAgICAgcmVwb3J0X3RpdGxlPSJSZXBvcnRlIFBHQyDigJQgdGFibGFzIiwKICAgICAgICAgICAgc3RhbXBfbGFiZWw9ZGF0YS5nZXQoInN0YW1wX2xhYmVsIikgb3Igc3RhbXBfZmlsZW5hbWUoInJlcG9ydGVfcGdjIiwgInhsc3giLCBub3cpLAogICAgICAgICkKICAgICAgICBmaWxlcy5hcHBlbmQoKHN0YW1wX2ZpbGVuYW1lKCJyZXBvcnRlX3BnY190YWJsYXMiLCAieGxzeCIsIG5vdyksIHhsc3gpKQoKICAgIGlmIEFSRUFfUEdPIGluIHNlbGVjdGVkOgogICAgICAgIGRhdGEgPSBidWlsZF9wZ29fcmVzdWx0cyhjZmcpCiAgICAgICAgZmlsZXMuYXBwZW5kKAogICAgICAgICAgICAoc3RhbXBfZmlsZW5hbWUoInJlcG9ydGVfcGdvIiwgIm1kIiwgbm93KSwgZGF0YVsibWQiXS5lbmNvZGUoInV0Zi04IikpCiAgICAgICAgKQogICAgICAgIHhsc3ggPSBidWlsZF93b3JrYm9vaygKICAgICAgICAgICAgZGF0YVsic2hlZXRzIl0sCiAgICAgICAgICAgIHJlcG9ydF90aXRsZT0iUmVwb3J0ZSBQR08g4oCUIHRhYmxhcyIsCiAgICAgICAgICAgIHN0YW1wX2xhYmVsPWRhdGEuZ2V0KCJzdGFtcF9sYWJlbCIpIG9yIHN0YW1wX2ZpbGVuYW1lKCJyZXBvcnRlX3BnbyIsICJ4bHN4Iiwgbm93KSwKICAgICAgICApCiAgICAgICAgZmlsZXMuYXBwZW5kKChzdGFtcF9maWxlbmFtZSgicmVwb3J0ZV9wZ29fdGFibGFzIiwgInhsc3giLCBub3cpLCB4bHN4KSkKCiAgICBpZiBBUkVBX1JJU0sgaW4gc2VsZWN0ZWQ6CiAgICAgICAgZGF0YSA9IGJ1aWxkX3Jpc2tfcmVzdWx0cyhjZmcpCiAgICAgICAgZmlsZXMuYXBwZW5kKAogICAgICAgICAgICAoc3RhbXBfZmlsZW5hbWUoInJlcG9ydGVfYnJpZXNnbyIsICJtZCIsIG5vdyksIGRhdGFbIm1kIl0uZW5jb2RlKCJ1dGYtOCIpKQogICAgICAgICkKICAgICAgICB4bHN4ID0gYnVpbGRfd29ya2Jvb2soCiAgICAgICAgICAgIGRhdGFbInNoZWV0cyJdLAogICAgICAgICAgICByZXBvcnRfdGl0bGU9IlJlcG9ydGUgQi4gUmllc2dvIOKAlCB0YWJsYXMiLAogICAgICAgICAgICBzdGFtcF9sYWJlbD1kYXRhLmdldCgic3RhbXBfbGFiZWwiKSBvciBzdGFtcF9maWxlbmFtZSgicmVwb3J0ZV9icmllc2dvIiwgInhsc3giLCBub3cpLAogICAgICAgICkKICAgICAgICBmaWxlcy5hcHBlbmQoKHN0YW1wX2ZpbGVuYW1lKCJyZXBvcnRlX2JyaWVzZ29fdGFibGFzIiwgInhsc3giLCBub3cpLCB4bHN4KSkKCiAgICBpZiBsZW4oZmlsZXMpID09IDE6CiAgICAgICAgbmFtZSwgY29udGVudCA9IGZpbGVzWzBdCiAgICAgICAgaWYgbmFtZS5lbmRzd2l0aCgiLm1kIik6CiAgICAgICAgICAgIGN0eXBlID0gInRleHQvbWFya2Rvd247IGNoYXJzZXQ9dXRmLTgiCiAgICAgICAgZWxzZToKICAgICAgICAgICAgY3R5cGUgPSAiYXBwbGljYXRpb24vdm5kLm9wZW54bWxmb3JtYXRzLW9mZmljZWRvY3VtZW50LnNwcmVhZHNoZWV0bWwuc2hlZXQiCiAgICAgICAgcmV0dXJuIG5hbWUsIGNvbnRlbnQsIGN0eXBlCgogICAgYnVmID0gQnl0ZXNJTygpCiAgICB3aXRoIHppcGZpbGUuWmlwRmlsZShidWYsICJ3IiwgY29tcHJlc3Npb249emlwZmlsZS5aSVBfREVGTEFURUQpIGFzIHpmOgogICAgICAgIGZvciBuYW1lLCBjb250ZW50IGluIGZpbGVzOgogICAgICAgICAgICB6Zi53cml0ZXN0cihuYW1lLCBjb250ZW50KQogICAgemlwX25hbWUgPSBzdGFtcF9maWxlbmFtZSgicmVwb3J0ZXNfd2NnIiwgInppcCIsIG5vdykKICAgIHJldHVybiB6aXBfbmFtZSwgYnVmLmdldHZhbHVlKCksICJhcHBsaWNhdGlvbi96aXAiCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/services/common.py
PATH_JSON="reports/services/common.py"
FILENAME=common.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=75
SIZE_BYTES_UTF8=1596
CONTENT_SHA256=9c0b384ef6fe8a5e55f3265d31625b1282d9fc1336f2421032e5d2b0fa118cd2
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
from __future__ import annotations

from decimal import Decimal
from typing import Any


def dec(value) -> Decimal:
    if value is None:
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


def pct_change(curr, prev) -> str:
    c, p = dec(curr), dec(prev)
    if p == 0:
        if c == 0:
            return "0%"
        return "n/d (base 0)"
    change = ((c - p) / abs(p)) * Decimal("100")
    sign = "+" if change > 0 else ""
    return f"{sign}{change.quantize(Decimal('0.1'))}%"


def delta(curr, prev) -> Decimal:
    return dec(curr) - dec(prev)


def fmt_num(value, places: int = 1) -> str:
    d = dec(value)
    q = Decimal("1").scaleb(-places)
    return str(d.quantize(q))


def period_label(year: int, month: int) -> str:
    months = [
        "",
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ]
    return f"{months[month]} {year}"


def ym_key(year: int, month: int) -> str:
    return f"{year}-{month:02d}"


def previous_month(year: int, month: int) -> tuple[int, int]:
    if month <= 1:
        return year - 1, 12
    return year, month - 1


def sorted_unique_periods(pairs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return sorted(set(pairs))


def limit_rows(rows: list[Any], n: int) -> list[Any]:
    if n <= 0:
        return rows
    return rows[:n]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from __future__ import annotations
00002|
00003|from decimal import Decimal
00004|from typing import Any
00005|
00006|
00007|def dec(value) -> Decimal:
00008|    if value is None:
00009|        return Decimal("0")
00010|    if isinstance(value, Decimal):
00011|        return value
00012|    try:
00013|        return Decimal(str(value))
00014|    except Exception:
00015|        return Decimal("0")
00016|
00017|
00018|def pct_change(curr, prev) -> str:
00019|    c, p = dec(curr), dec(prev)
00020|    if p == 0:
00021|        if c == 0:
00022|            return "0%"
00023|        return "n/d (base 0)"
00024|    change = ((c - p) / abs(p)) * Decimal("100")
00025|    sign = "+" if change > 0 else ""
00026|    return f"{sign}{change.quantize(Decimal('0.1'))}%"
00027|
00028|
00029|def delta(curr, prev) -> Decimal:
00030|    return dec(curr) - dec(prev)
00031|
00032|
00033|def fmt_num(value, places: int = 1) -> str:
00034|    d = dec(value)
00035|    q = Decimal("1").scaleb(-places)
00036|    return str(d.quantize(q))
00037|
00038|
00039|def period_label(year: int, month: int) -> str:
00040|    months = [
00041|        "",
00042|        "enero",
00043|        "febrero",
00044|        "marzo",
00045|        "abril",
00046|        "mayo",
00047|        "junio",
00048|        "julio",
00049|        "agosto",
00050|        "septiembre",
00051|        "octubre",
00052|        "noviembre",
00053|        "diciembre",
00054|    ]
00055|    return f"{months[month]} {year}"
00056|
00057|
00058|def ym_key(year: int, month: int) -> str:
00059|    return f"{year}-{month:02d}"
00060|
00061|
00062|def previous_month(year: int, month: int) -> tuple[int, int]:
00063|    if month <= 1:
00064|        return year - 1, 12
00065|    return year, month - 1
00066|
00067|
00068|def sorted_unique_periods(pairs: list[tuple[int, int]]) -> list[tuple[int, int]]:
00069|    return sorted(set(pairs))
00070|
00071|
00072|def limit_rows(rows: list[Any], n: int) -> list[Any]:
00073|    if n <= 0:
00074|        return rows
00075|    return rows[:n]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsCmZyb20gdHlwaW5nIGltcG9ydCBBbnkKCgpkZWYgZGVjKHZhbHVlKSAtPiBEZWNpbWFsOgogICAgaWYgdmFsdWUgaXMgTm9uZToKICAgICAgICByZXR1cm4gRGVjaW1hbCgiMCIpCiAgICBpZiBpc2luc3RhbmNlKHZhbHVlLCBEZWNpbWFsKToKICAgICAgICByZXR1cm4gdmFsdWUKICAgIHRyeToKICAgICAgICByZXR1cm4gRGVjaW1hbChzdHIodmFsdWUpKQogICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICByZXR1cm4gRGVjaW1hbCgiMCIpCgoKZGVmIHBjdF9jaGFuZ2UoY3VyciwgcHJldikgLT4gc3RyOgogICAgYywgcCA9IGRlYyhjdXJyKSwgZGVjKHByZXYpCiAgICBpZiBwID09IDA6CiAgICAgICAgaWYgYyA9PSAwOgogICAgICAgICAgICByZXR1cm4gIjAlIgogICAgICAgIHJldHVybiAibi9kIChiYXNlIDApIgogICAgY2hhbmdlID0gKChjIC0gcCkgLyBhYnMocCkpICogRGVjaW1hbCgiMTAwIikKICAgIHNpZ24gPSAiKyIgaWYgY2hhbmdlID4gMCBlbHNlICIiCiAgICByZXR1cm4gZiJ7c2lnbn17Y2hhbmdlLnF1YW50aXplKERlY2ltYWwoJzAuMScpKX0lIgoKCmRlZiBkZWx0YShjdXJyLCBwcmV2KSAtPiBEZWNpbWFsOgogICAgcmV0dXJuIGRlYyhjdXJyKSAtIGRlYyhwcmV2KQoKCmRlZiBmbXRfbnVtKHZhbHVlLCBwbGFjZXM6IGludCA9IDEpIC0+IHN0cjoKICAgIGQgPSBkZWModmFsdWUpCiAgICBxID0gRGVjaW1hbCgiMSIpLnNjYWxlYigtcGxhY2VzKQogICAgcmV0dXJuIHN0cihkLnF1YW50aXplKHEpKQoKCmRlZiBwZXJpb2RfbGFiZWwoeWVhcjogaW50LCBtb250aDogaW50KSAtPiBzdHI6CiAgICBtb250aHMgPSBbCiAgICAgICAgIiIsCiAgICAgICAgImVuZXJvIiwKICAgICAgICAiZmVicmVybyIsCiAgICAgICAgIm1hcnpvIiwKICAgICAgICAiYWJyaWwiLAogICAgICAgICJtYXlvIiwKICAgICAgICAianVuaW8iLAogICAgICAgICJqdWxpbyIsCiAgICAgICAgImFnb3N0byIsCiAgICAgICAgInNlcHRpZW1icmUiLAogICAgICAgICJvY3R1YnJlIiwKICAgICAgICAibm92aWVtYnJlIiwKICAgICAgICAiZGljaWVtYnJlIiwKICAgIF0KICAgIHJldHVybiBmInttb250aHNbbW9udGhdfSB7eWVhcn0iCgoKZGVmIHltX2tleSh5ZWFyOiBpbnQsIG1vbnRoOiBpbnQpIC0+IHN0cjoKICAgIHJldHVybiBmInt5ZWFyfS17bW9udGg6MDJkfSIKCgpkZWYgcHJldmlvdXNfbW9udGgoeWVhcjogaW50LCBtb250aDogaW50KSAtPiB0dXBsZVtpbnQsIGludF06CiAgICBpZiBtb250aCA8PSAxOgogICAgICAgIHJldHVybiB5ZWFyIC0gMSwgMTIKICAgIHJldHVybiB5ZWFyLCBtb250aCAtIDEKCgpkZWYgc29ydGVkX3VuaXF1ZV9wZXJpb2RzKHBhaXJzOiBsaXN0W3R1cGxlW2ludCwgaW50XV0pIC0+IGxpc3RbdHVwbGVbaW50LCBpbnRdXToKICAgIHJldHVybiBzb3J0ZWQoc2V0KHBhaXJzKSkKCgpkZWYgbGltaXRfcm93cyhyb3dzOiBsaXN0W0FueV0sIG46IGludCkgLT4gbGlzdFtBbnldOgogICAgaWYgbiA8PSAwOgogICAgICAgIHJldHVybiByb3dzCiAgICByZXR1cm4gcm93c1s6bl0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/services/coverage.py
PATH_JSON="reports/services/coverage.py"
FILENAME=coverage.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=255
SIZE_BYTES_UTF8=9510
CONTENT_SHA256=1d1e0162278ede0ee13f17183107ddaba426be2630384de46527cb934f2a78b6
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
"""Reporte de cobertura / administración (solo .md)."""

from __future__ import annotations

from collections import defaultdict

from django.db.models import Count
from django.utils import timezone

from core.models import MetricDefinition, UNE
from imports.models import (
    CrossSaleImportRow,
    FileUpload,
    NewClientImportRow,
)
from pgc.models import (
    ManualRequirementsCompliance,
    MonthlyExchangeRate,
    MonthlyMetricResult,
    MonthlyModeScorecard,
    MonthlyTarget,
    PGCPlan,
)
from pgo.models import PgoResultadoPeriodo, Ticket
from reports.md_utils import ai_closing, bullets, h1, h2, h3, join_sections, md_table, p
from reports.models import ReportConfig
from reports.naming import report_stamp
from reports.services.common import period_label, ym_key
from risk.models import EstadoFinanciero, RiskOperationSnapshot


def build_admin_coverage_md(cfg: ReportConfig | None = None) -> str:
    cfg = cfg or ReportConfig.get_active()
    now = timezone.localtime()
    stamp = report_stamp(now).strip()

    sections = [
        h1("Reporte de administración / cobertura de datos"),
        p(f"**Generado:** {now.strftime('%Y-%m-%d %H:%M')} ({timezone.get_current_timezone_name()}) · marca `{stamp}`"),
        p(
            "Enfoque: disponibilidad y cobertura (no cifras de negocio). "
            "Áreas: **PGC**, **PGO**, **B. Riesgo**."
        ),
        p(f"**Config:** `{cfg.name}` · compact={cfg.compact_mode}"),
    ]

    # --- Global uploads ---
    uploads = FileUpload.objects.all().order_by("-created_at")
    up_rows = []
    for u in uploads[:40]:
        up_rows.append(
            [
                u.original_filename[:48],
                u.file_type_detected,
                u.status,
                f"{u.detected_year or '—'}-{int(u.detected_month or 0):02d}"
                if u.detected_month
                else "—",
                u.created_at.strftime("%Y-%m-%d") if u.created_at else "—",
            ]
        )
    sections += [
        h2("Archivos importados (recientes)"),
        md_table(
            ["Archivo", "Tipo", "Estado", "Período det.", "Creado"],
            up_rows
            or [["—", "—", "—", "—", "Sin uploads"]],
        ),
        p(f"Total FileUpload: **{uploads.count()}**"),
    ]

    # --- PGC coverage ---
    sections += _pgc_coverage()
    sections += _pgo_coverage()
    sections += _risk_coverage()

    hechos = [
        f"Uploads registrados: {uploads.count()}",
        f"Planes PGC: {PGCPlan.objects.count()}",
        f"Tickets PGO: {Ticket.objects.count()}",
        f"Snapshots riesgo: {RiskOperationSnapshot.objects.count()}",
    ]
    cambios = [
        "Este reporte es de cobertura; los cambios de negocio están en reportes PGC/PGO/B. Riesgo."
    ]
    vacios = _global_gaps()
    sections.append(ai_closing(hechos, cambios, vacios))
    return join_sections(*sections)


def _pgc_coverage() -> list[str]:
    out = [h2("PGC — cobertura por tema y período")]
    plans = list(PGCPlan.objects.order_by("year"))
    unes = list(UNE.objects.filter(is_active=True).order_by("sort_order"))
    metrics = list(MetricDefinition.objects.order_by("code"))

    out.append(h3("Disponible"))
    out.append(
        bullets(
            [
                f"Planes: {', '.join(str(p.year) for p in plans) or 'ninguno'}",
                f"UNEs activas: {', '.join(u.code for u in unes) or 'ninguna'}",
                f"Métricas: {', '.join(m.code for m in metrics) or 'ninguna'}",
                f"Filas clientes nuevos: {NewClientImportRow.objects.count()}",
                f"Filas venta cruzada: {CrossSaleImportRow.objects.count()}",
                f"Tipos de cambio: {MonthlyExchangeRate.objects.count()}",
                f"Metas (MonthlyTarget): {MonthlyTarget.objects.count()}",
                f"Resultados métrica: {MonthlyMetricResult.objects.count()}",
                f"Scorecards modo: {MonthlyModeScorecard.objects.count()}",
                f"Cumplimiento reqs: {ManualRequirementsCompliance.objects.count()}",
            ]
        )
    )

    by_period: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for y, m in MonthlyMetricResult.objects.values_list("year", "month").distinct():
        by_period[ym_key(y, m)]["resultados"] += 1
    for y, m in NewClientImportRow.objects.values_list("year", "month").distinct():
        by_period[ym_key(y, m)]["clientes"] += NewClientImportRow.objects.filter(
            year=y, month=m
        ).count()
    for y, m in CrossSaleImportRow.objects.values_list("year", "month").distinct():
        by_period[ym_key(y, m)]["venta_cruzada"] += CrossSaleImportRow.objects.filter(
            year=y, month=m
        ).count()
    for y, m in MonthlyModeScorecard.objects.values_list("year", "month").distinct():
        by_period[ym_key(y, m)]["scorecards"] += MonthlyModeScorecard.objects.filter(
            year=y, month=m
        ).count()
    for y, m in MonthlyExchangeRate.objects.values_list("year", "month"):
        by_period[ym_key(y, m)]["fx"] = 1
    for y, m in ManualRequirementsCompliance.objects.values_list("year", "month").distinct():
        by_period[ym_key(y, m)]["reqs"] += ManualRequirementsCompliance.objects.filter(
            year=y, month=m
        ).count()

    rows = []
    for key in sorted(by_period.keys()):
        d = by_period[key]
        rows.append(
            [
                key,
                d.get("resultados", 0),
                d.get("clientes", 0),
                d.get("venta_cruzada", 0),
                d.get("reqs", 0),
                d.get("scorecards", 0),
                "sí" if d.get("fx") else "no",
            ]
        )
    out.append(h3("Cobertura por período"))
    out.append(
        md_table(
            ["Período", "Resultados", "Clientes", "Vta cruzada", "Reqs", "Scores", "FX"],
            rows or [["—", 0, 0, 0, 0, 0, "no"]],
        )
    )

    missing = []
    if plans:
        year = plans[-1].year
        for month in range(1, 13):
            key = ym_key(year, month)
            d = by_period.get(key, {})
            gaps = []
            if not d.get("fx"):
                gaps.append("FX")
            if not d.get("scorecards"):
                gaps.append("score")
            if not d.get("resultados"):
                gaps.append("resultados")
            if gaps:
                missing.append(f"{period_label(year, month)}: falta {', '.join(gaps)}")
    out.append(h3("Faltante / pendiente (PGC)"))
    out.append(bullets(missing[:18] or ["Sin huecos evidentes en el último plan."]))
    return out


def _pgo_coverage() -> list[str]:
    out = [h2("PGO — cobertura")]
    tickets = Ticket.objects.count()
    periodos = list(
        PgoResultadoPeriodo.objects.values_list("periodo", flat=True).distinct().order_by("periodo")
    )
    by_estado = list(
        Ticket.objects.values("estado").annotate(n=Count("id")).order_by("estado")
    )
    out.append(h3("Disponible"))
    out.append(
        bullets(
            [
                f"Tickets: {tickets}",
                f"Resultados período: {PgoResultadoPeriodo.objects.count()}",
                f"Períodos con resultado: {', '.join(periodos) or 'ninguno'}",
            ]
            + [f"Estado {r['estado']}: {r['n']}" for r in by_estado]
        )
    )
    gaps = []
    if tickets == 0:
        gaps.append("Sin tickets cargados.")
    if not periodos:
        gaps.append("Sin PgoResultadoPeriodo calculados.")
    out.append(h3("Faltante / pendiente (PGO)"))
    out.append(bullets(gaps or ["Cobertura PGO presente."]))
    return out


def _risk_coverage() -> list[str]:
    out = [h2("B. Riesgo — cobertura")]
    snaps = RiskOperationSnapshot.objects.count()
    estados = EstadoFinanciero.objects.count()
    periods = sorted(
        {
            s.strftime("%Y-%m")
            for s in RiskOperationSnapshot.objects.values_list("fecha_snapshot", flat=True)
            if s
        }
    )
    ef_periods = sorted(set(EstadoFinanciero.objects.values_list("periodo", flat=True)))
    out.append(h3("Disponible"))
    out.append(
        bullets(
            [
                f"Snapshots operación: {snaps}",
                f"Estados financieros: {estados}",
                f"Períodos snapshot: {', '.join(periods[-12:]) or 'ninguno'}",
                f"Períodos EF: {', '.join(ef_periods[-12:]) or 'ninguno'}",
                f"Con alerta: {RiskOperationSnapshot.objects.filter(alerta=True).count()}",
            ]
        )
    )
    gaps = []
    if snaps == 0:
        gaps.append("Sin RiskOperationSnapshot.")
    if estados == 0:
        gaps.append("Sin EstadoFinanciero.")
    out.append(h3("Faltante / pendiente (B. Riesgo)"))
    out.append(bullets(gaps or ["Cobertura de riesgo presente."]))
    return out


def _global_gaps() -> list[str]:
    gaps = []
    if FileUpload.objects.filter(status=FileUpload.STATUS_UPLOADED).exists():
        gaps.append("Hay archivos UPLOADED pendientes de procesar.")
    if FileUpload.objects.filter(status=FileUpload.STATUS_PARSED_ERROR).exists():
        gaps.append("Hay archivos con PARSED_ERROR.")
    if not MonthlyExchangeRate.objects.exists():
        gaps.append("No hay tipos de cambio PGC.")
    if Ticket.objects.count() == 0:
        gaps.append("PGO sin tickets.")
    if RiskOperationSnapshot.objects.count() == 0:
        gaps.append("B. Riesgo sin snapshots.")
    return gaps or ["Sin vacíos globales críticos detectados."]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Reporte de cobertura / administración (solo .md)."""
00002|
00003|from __future__ import annotations
00004|
00005|from collections import defaultdict
00006|
00007|from django.db.models import Count
00008|from django.utils import timezone
00009|
00010|from core.models import MetricDefinition, UNE
00011|from imports.models import (
00012|    CrossSaleImportRow,
00013|    FileUpload,
00014|    NewClientImportRow,
00015|)
00016|from pgc.models import (
00017|    ManualRequirementsCompliance,
00018|    MonthlyExchangeRate,
00019|    MonthlyMetricResult,
00020|    MonthlyModeScorecard,
00021|    MonthlyTarget,
00022|    PGCPlan,
00023|)
00024|from pgo.models import PgoResultadoPeriodo, Ticket
00025|from reports.md_utils import ai_closing, bullets, h1, h2, h3, join_sections, md_table, p
00026|from reports.models import ReportConfig
00027|from reports.naming import report_stamp
00028|from reports.services.common import period_label, ym_key
00029|from risk.models import EstadoFinanciero, RiskOperationSnapshot
00030|
00031|
00032|def build_admin_coverage_md(cfg: ReportConfig | None = None) -> str:
00033|    cfg = cfg or ReportConfig.get_active()
00034|    now = timezone.localtime()
00035|    stamp = report_stamp(now).strip()
00036|
00037|    sections = [
00038|        h1("Reporte de administración / cobertura de datos"),
00039|        p(f"**Generado:** {now.strftime('%Y-%m-%d %H:%M')} ({timezone.get_current_timezone_name()}) · marca `{stamp}`"),
00040|        p(
00041|            "Enfoque: disponibilidad y cobertura (no cifras de negocio). "
00042|            "Áreas: **PGC**, **PGO**, **B. Riesgo**."
00043|        ),
00044|        p(f"**Config:** `{cfg.name}` · compact={cfg.compact_mode}"),
00045|    ]
00046|
00047|    # --- Global uploads ---
00048|    uploads = FileUpload.objects.all().order_by("-created_at")
00049|    up_rows = []
00050|    for u in uploads[:40]:
00051|        up_rows.append(
00052|            [
00053|                u.original_filename[:48],
00054|                u.file_type_detected,
00055|                u.status,
00056|                f"{u.detected_year or '—'}-{int(u.detected_month or 0):02d}"
00057|                if u.detected_month
00058|                else "—",
00059|                u.created_at.strftime("%Y-%m-%d") if u.created_at else "—",
00060|            ]
00061|        )
00062|    sections += [
00063|        h2("Archivos importados (recientes)"),
00064|        md_table(
00065|            ["Archivo", "Tipo", "Estado", "Período det.", "Creado"],
00066|            up_rows
00067|            or [["—", "—", "—", "—", "Sin uploads"]],
00068|        ),
00069|        p(f"Total FileUpload: **{uploads.count()}**"),
00070|    ]
00071|
00072|    # --- PGC coverage ---
00073|    sections += _pgc_coverage()
00074|    sections += _pgo_coverage()
00075|    sections += _risk_coverage()
00076|
00077|    hechos = [
00078|        f"Uploads registrados: {uploads.count()}",
00079|        f"Planes PGC: {PGCPlan.objects.count()}",
00080|        f"Tickets PGO: {Ticket.objects.count()}",
00081|        f"Snapshots riesgo: {RiskOperationSnapshot.objects.count()}",
00082|    ]
00083|    cambios = [
00084|        "Este reporte es de cobertura; los cambios de negocio están en reportes PGC/PGO/B. Riesgo."
00085|    ]
00086|    vacios = _global_gaps()
00087|    sections.append(ai_closing(hechos, cambios, vacios))
00088|    return join_sections(*sections)
00089|
00090|
00091|def _pgc_coverage() -> list[str]:
00092|    out = [h2("PGC — cobertura por tema y período")]
00093|    plans = list(PGCPlan.objects.order_by("year"))
00094|    unes = list(UNE.objects.filter(is_active=True).order_by("sort_order"))
00095|    metrics = list(MetricDefinition.objects.order_by("code"))
00096|
00097|    out.append(h3("Disponible"))
00098|    out.append(
00099|        bullets(
00100|            [
00101|                f"Planes: {', '.join(str(p.year) for p in plans) or 'ninguno'}",
00102|                f"UNEs activas: {', '.join(u.code for u in unes) or 'ninguna'}",
00103|                f"Métricas: {', '.join(m.code for m in metrics) or 'ninguna'}",
00104|                f"Filas clientes nuevos: {NewClientImportRow.objects.count()}",
00105|                f"Filas venta cruzada: {CrossSaleImportRow.objects.count()}",
00106|                f"Tipos de cambio: {MonthlyExchangeRate.objects.count()}",
00107|                f"Metas (MonthlyTarget): {MonthlyTarget.objects.count()}",
00108|                f"Resultados métrica: {MonthlyMetricResult.objects.count()}",
00109|                f"Scorecards modo: {MonthlyModeScorecard.objects.count()}",
00110|                f"Cumplimiento reqs: {ManualRequirementsCompliance.objects.count()}",
00111|            ]
00112|        )
00113|    )
00114|
00115|    by_period: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
00116|    for y, m in MonthlyMetricResult.objects.values_list("year", "month").distinct():
00117|        by_period[ym_key(y, m)]["resultados"] += 1
00118|    for y, m in NewClientImportRow.objects.values_list("year", "month").distinct():
00119|        by_period[ym_key(y, m)]["clientes"] += NewClientImportRow.objects.filter(
00120|            year=y, month=m
00121|        ).count()
00122|    for y, m in CrossSaleImportRow.objects.values_list("year", "month").distinct():
00123|        by_period[ym_key(y, m)]["venta_cruzada"] += CrossSaleImportRow.objects.filter(
00124|            year=y, month=m
00125|        ).count()
00126|    for y, m in MonthlyModeScorecard.objects.values_list("year", "month").distinct():
00127|        by_period[ym_key(y, m)]["scorecards"] += MonthlyModeScorecard.objects.filter(
00128|            year=y, month=m
00129|        ).count()
00130|    for y, m in MonthlyExchangeRate.objects.values_list("year", "month"):
00131|        by_period[ym_key(y, m)]["fx"] = 1
00132|    for y, m in ManualRequirementsCompliance.objects.values_list("year", "month").distinct():
00133|        by_period[ym_key(y, m)]["reqs"] += ManualRequirementsCompliance.objects.filter(
00134|            year=y, month=m
00135|        ).count()
00136|
00137|    rows = []
00138|    for key in sorted(by_period.keys()):
00139|        d = by_period[key]
00140|        rows.append(
00141|            [
00142|                key,
00143|                d.get("resultados", 0),
00144|                d.get("clientes", 0),
00145|                d.get("venta_cruzada", 0),
00146|                d.get("reqs", 0),
00147|                d.get("scorecards", 0),
00148|                "sí" if d.get("fx") else "no",
00149|            ]
00150|        )
00151|    out.append(h3("Cobertura por período"))
00152|    out.append(
00153|        md_table(
00154|            ["Período", "Resultados", "Clientes", "Vta cruzada", "Reqs", "Scores", "FX"],
00155|            rows or [["—", 0, 0, 0, 0, 0, "no"]],
00156|        )
00157|    )
00158|
00159|    missing = []
00160|    if plans:
00161|        year = plans[-1].year
00162|        for month in range(1, 13):
00163|            key = ym_key(year, month)
00164|            d = by_period.get(key, {})
00165|            gaps = []
00166|            if not d.get("fx"):
00167|                gaps.append("FX")
00168|            if not d.get("scorecards"):
00169|                gaps.append("score")
00170|            if not d.get("resultados"):
00171|                gaps.append("resultados")
00172|            if gaps:
00173|                missing.append(f"{period_label(year, month)}: falta {', '.join(gaps)}")
00174|    out.append(h3("Faltante / pendiente (PGC)"))
00175|    out.append(bullets(missing[:18] or ["Sin huecos evidentes en el último plan."]))
00176|    return out
00177|
00178|
00179|def _pgo_coverage() -> list[str]:
00180|    out = [h2("PGO — cobertura")]
00181|    tickets = Ticket.objects.count()
00182|    periodos = list(
00183|        PgoResultadoPeriodo.objects.values_list("periodo", flat=True).distinct().order_by("periodo")
00184|    )
00185|    by_estado = list(
00186|        Ticket.objects.values("estado").annotate(n=Count("id")).order_by("estado")
00187|    )
00188|    out.append(h3("Disponible"))
00189|    out.append(
00190|        bullets(
00191|            [
00192|                f"Tickets: {tickets}",
00193|                f"Resultados período: {PgoResultadoPeriodo.objects.count()}",
00194|                f"Períodos con resultado: {', '.join(periodos) or 'ninguno'}",
00195|            ]
00196|            + [f"Estado {r['estado']}: {r['n']}" for r in by_estado]
00197|        )
00198|    )
00199|    gaps = []
00200|    if tickets == 0:
00201|        gaps.append("Sin tickets cargados.")
00202|    if not periodos:
00203|        gaps.append("Sin PgoResultadoPeriodo calculados.")
00204|    out.append(h3("Faltante / pendiente (PGO)"))
00205|    out.append(bullets(gaps or ["Cobertura PGO presente."]))
00206|    return out
00207|
00208|
00209|def _risk_coverage() -> list[str]:
00210|    out = [h2("B. Riesgo — cobertura")]
00211|    snaps = RiskOperationSnapshot.objects.count()
00212|    estados = EstadoFinanciero.objects.count()
00213|    periods = sorted(
00214|        {
00215|            s.strftime("%Y-%m")
00216|            for s in RiskOperationSnapshot.objects.values_list("fecha_snapshot", flat=True)
00217|            if s
00218|        }
00219|    )
00220|    ef_periods = sorted(set(EstadoFinanciero.objects.values_list("periodo", flat=True)))
00221|    out.append(h3("Disponible"))
00222|    out.append(
00223|        bullets(
00224|            [
00225|                f"Snapshots operación: {snaps}",
00226|                f"Estados financieros: {estados}",
00227|                f"Períodos snapshot: {', '.join(periods[-12:]) or 'ninguno'}",
00228|                f"Períodos EF: {', '.join(ef_periods[-12:]) or 'ninguno'}",
00229|                f"Con alerta: {RiskOperationSnapshot.objects.filter(alerta=True).count()}",
00230|            ]
00231|        )
00232|    )
00233|    gaps = []
00234|    if snaps == 0:
00235|        gaps.append("Sin RiskOperationSnapshot.")
00236|    if estados == 0:
00237|        gaps.append("Sin EstadoFinanciero.")
00238|    out.append(h3("Faltante / pendiente (B. Riesgo)"))
00239|    out.append(bullets(gaps or ["Cobertura de riesgo presente."]))
00240|    return out
00241|
00242|
00243|def _global_gaps() -> list[str]:
00244|    gaps = []
00245|    if FileUpload.objects.filter(status=FileUpload.STATUS_UPLOADED).exists():
00246|        gaps.append("Hay archivos UPLOADED pendientes de procesar.")
00247|    if FileUpload.objects.filter(status=FileUpload.STATUS_PARSED_ERROR).exists():
00248|        gaps.append("Hay archivos con PARSED_ERROR.")
00249|    if not MonthlyExchangeRate.objects.exists():
00250|        gaps.append("No hay tipos de cambio PGC.")
00251|    if Ticket.objects.count() == 0:
00252|        gaps.append("PGO sin tickets.")
00253|    if RiskOperationSnapshot.objects.count() == 0:
00254|        gaps.append("B. Riesgo sin snapshots.")
00255|    return gaps or ["Sin vacíos globales críticos detectados."]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiUmVwb3J0ZSBkZSBjb2JlcnR1cmEgLyBhZG1pbmlzdHJhY2nDs24gKHNvbG8gLm1kKS4iIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmZyb20gY29sbGVjdGlvbnMgaW1wb3J0IGRlZmF1bHRkaWN0Cgpmcm9tIGRqYW5nby5kYi5tb2RlbHMgaW1wb3J0IENvdW50CmZyb20gZGphbmdvLnV0aWxzIGltcG9ydCB0aW1lem9uZQoKZnJvbSBjb3JlLm1vZGVscyBpbXBvcnQgTWV0cmljRGVmaW5pdGlvbiwgVU5FCmZyb20gaW1wb3J0cy5tb2RlbHMgaW1wb3J0ICgKICAgIENyb3NzU2FsZUltcG9ydFJvdywKICAgIEZpbGVVcGxvYWQsCiAgICBOZXdDbGllbnRJbXBvcnRSb3csCikKZnJvbSBwZ2MubW9kZWxzIGltcG9ydCAoCiAgICBNYW51YWxSZXF1aXJlbWVudHNDb21wbGlhbmNlLAogICAgTW9udGhseUV4Y2hhbmdlUmF0ZSwKICAgIE1vbnRobHlNZXRyaWNSZXN1bHQsCiAgICBNb250aGx5TW9kZVNjb3JlY2FyZCwKICAgIE1vbnRobHlUYXJnZXQsCiAgICBQR0NQbGFuLAopCmZyb20gcGdvLm1vZGVscyBpbXBvcnQgUGdvUmVzdWx0YWRvUGVyaW9kbywgVGlja2V0CmZyb20gcmVwb3J0cy5tZF91dGlscyBpbXBvcnQgYWlfY2xvc2luZywgYnVsbGV0cywgaDEsIGgyLCBoMywgam9pbl9zZWN0aW9ucywgbWRfdGFibGUsIHAKZnJvbSByZXBvcnRzLm1vZGVscyBpbXBvcnQgUmVwb3J0Q29uZmlnCmZyb20gcmVwb3J0cy5uYW1pbmcgaW1wb3J0IHJlcG9ydF9zdGFtcApmcm9tIHJlcG9ydHMuc2VydmljZXMuY29tbW9uIGltcG9ydCBwZXJpb2RfbGFiZWwsIHltX2tleQpmcm9tIHJpc2subW9kZWxzIGltcG9ydCBFc3RhZG9GaW5hbmNpZXJvLCBSaXNrT3BlcmF0aW9uU25hcHNob3QKCgpkZWYgYnVpbGRfYWRtaW5fY292ZXJhZ2VfbWQoY2ZnOiBSZXBvcnRDb25maWcgfCBOb25lID0gTm9uZSkgLT4gc3RyOgogICAgY2ZnID0gY2ZnIG9yIFJlcG9ydENvbmZpZy5nZXRfYWN0aXZlKCkKICAgIG5vdyA9IHRpbWV6b25lLmxvY2FsdGltZSgpCiAgICBzdGFtcCA9IHJlcG9ydF9zdGFtcChub3cpLnN0cmlwKCkKCiAgICBzZWN0aW9ucyA9IFsKICAgICAgICBoMSgiUmVwb3J0ZSBkZSBhZG1pbmlzdHJhY2nDs24gLyBjb2JlcnR1cmEgZGUgZGF0b3MiKSwKICAgICAgICBwKGYiKipHZW5lcmFkbzoqKiB7bm93LnN0cmZ0aW1lKCclWS0lbS0lZCAlSDolTScpfSAoe3RpbWV6b25lLmdldF9jdXJyZW50X3RpbWV6b25lX25hbWUoKX0pIMK3IG1hcmNhIGB7c3RhbXB9YCIpLAogICAgICAgIHAoCiAgICAgICAgICAgICJFbmZvcXVlOiBkaXNwb25pYmlsaWRhZCB5IGNvYmVydHVyYSAobm8gY2lmcmFzIGRlIG5lZ29jaW8pLiAiCiAgICAgICAgICAgICLDgXJlYXM6ICoqUEdDKiosICoqUEdPKiosICoqQi4gUmllc2dvKiouIgogICAgICAgICksCiAgICAgICAgcChmIioqQ29uZmlnOioqIGB7Y2ZnLm5hbWV9YCDCtyBjb21wYWN0PXtjZmcuY29tcGFjdF9tb2RlfSIpLAogICAgXQoKICAgICMgLS0tIEdsb2JhbCB1cGxvYWRzIC0tLQogICAgdXBsb2FkcyA9IEZpbGVVcGxvYWQub2JqZWN0cy5hbGwoKS5vcmRlcl9ieSgiLWNyZWF0ZWRfYXQiKQogICAgdXBfcm93cyA9IFtdCiAgICBmb3IgdSBpbiB1cGxvYWRzWzo0MF06CiAgICAgICAgdXBfcm93cy5hcHBlbmQoCiAgICAgICAgICAgIFsKICAgICAgICAgICAgICAgIHUub3JpZ2luYWxfZmlsZW5hbWVbOjQ4XSwKICAgICAgICAgICAgICAgIHUuZmlsZV90eXBlX2RldGVjdGVkLAogICAgICAgICAgICAgICAgdS5zdGF0dXMsCiAgICAgICAgICAgICAgICBmInt1LmRldGVjdGVkX3llYXIgb3IgJ+KAlCd9LXtpbnQodS5kZXRlY3RlZF9tb250aCBvciAwKTowMmR9IgogICAgICAgICAgICAgICAgaWYgdS5kZXRlY3RlZF9tb250aAogICAgICAgICAgICAgICAgZWxzZSAi4oCUIiwKICAgICAgICAgICAgICAgIHUuY3JlYXRlZF9hdC5zdHJmdGltZSgiJVktJW0tJWQiKSBpZiB1LmNyZWF0ZWRfYXQgZWxzZSAi4oCUIiwKICAgICAgICAgICAgXQogICAgICAgICkKICAgIHNlY3Rpb25zICs9IFsKICAgICAgICBoMigiQXJjaGl2b3MgaW1wb3J0YWRvcyAocmVjaWVudGVzKSIpLAogICAgICAgIG1kX3RhYmxlKAogICAgICAgICAgICBbIkFyY2hpdm8iLCAiVGlwbyIsICJFc3RhZG8iLCAiUGVyw61vZG8gZGV0LiIsICJDcmVhZG8iXSwKICAgICAgICAgICAgdXBfcm93cwogICAgICAgICAgICBvciBbWyLigJQiLCAi4oCUIiwgIuKAlCIsICLigJQiLCAiU2luIHVwbG9hZHMiXV0sCiAgICAgICAgKSwKICAgICAgICBwKGYiVG90YWwgRmlsZVVwbG9hZDogKip7dXBsb2Fkcy5jb3VudCgpfSoqIiksCiAgICBdCgogICAgIyAtLS0gUEdDIGNvdmVyYWdlIC0tLQogICAgc2VjdGlvbnMgKz0gX3BnY19jb3ZlcmFnZSgpCiAgICBzZWN0aW9ucyArPSBfcGdvX2NvdmVyYWdlKCkKICAgIHNlY3Rpb25zICs9IF9yaXNrX2NvdmVyYWdlKCkKCiAgICBoZWNob3MgPSBbCiAgICAgICAgZiJVcGxvYWRzIHJlZ2lzdHJhZG9zOiB7dXBsb2Fkcy5jb3VudCgpfSIsCiAgICAgICAgZiJQbGFuZXMgUEdDOiB7UEdDUGxhbi5vYmplY3RzLmNvdW50KCl9IiwKICAgICAgICBmIlRpY2tldHMgUEdPOiB7VGlja2V0Lm9iamVjdHMuY291bnQoKX0iLAogICAgICAgIGYiU25hcHNob3RzIHJpZXNnbzoge1Jpc2tPcGVyYXRpb25TbmFwc2hvdC5vYmplY3RzLmNvdW50KCl9IiwKICAgIF0KICAgIGNhbWJpb3MgPSBbCiAgICAgICAgIkVzdGUgcmVwb3J0ZSBlcyBkZSBjb2JlcnR1cmE7IGxvcyBjYW1iaW9zIGRlIG5lZ29jaW8gZXN0w6FuIGVuIHJlcG9ydGVzIFBHQy9QR08vQi4gUmllc2dvLiIKICAgIF0KICAgIHZhY2lvcyA9IF9nbG9iYWxfZ2FwcygpCiAgICBzZWN0aW9ucy5hcHBlbmQoYWlfY2xvc2luZyhoZWNob3MsIGNhbWJpb3MsIHZhY2lvcykpCiAgICByZXR1cm4gam9pbl9zZWN0aW9ucygqc2VjdGlvbnMpCgoKZGVmIF9wZ2NfY292ZXJhZ2UoKSAtPiBsaXN0W3N0cl06CiAgICBvdXQgPSBbaDIoIlBHQyDigJQgY29iZXJ0dXJhIHBvciB0ZW1hIHkgcGVyw61vZG8iKV0KICAgIHBsYW5zID0gbGlzdChQR0NQbGFuLm9iamVjdHMub3JkZXJfYnkoInllYXIiKSkKICAgIHVuZXMgPSBsaXN0KFVORS5vYmplY3RzLmZpbHRlcihpc19hY3RpdmU9VHJ1ZSkub3JkZXJfYnkoInNvcnRfb3JkZXIiKSkKICAgIG1ldHJpY3MgPSBsaXN0KE1ldHJpY0RlZmluaXRpb24ub2JqZWN0cy5vcmRlcl9ieSgiY29kZSIpKQoKICAgIG91dC5hcHBlbmQoaDMoIkRpc3BvbmlibGUiKSkKICAgIG91dC5hcHBlbmQoCiAgICAgICAgYnVsbGV0cygKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgZiJQbGFuZXM6IHsnLCAnLmpvaW4oc3RyKHAueWVhcikgZm9yIHAgaW4gcGxhbnMpIG9yICduaW5ndW5vJ30iLAogICAgICAgICAgICAgICAgZiJVTkVzIGFjdGl2YXM6IHsnLCAnLmpvaW4odS5jb2RlIGZvciB1IGluIHVuZXMpIG9yICduaW5ndW5hJ30iLAogICAgICAgICAgICAgICAgZiJNw6l0cmljYXM6IHsnLCAnLmpvaW4obS5jb2RlIGZvciBtIGluIG1ldHJpY3MpIG9yICduaW5ndW5hJ30iLAogICAgICAgICAgICAgICAgZiJGaWxhcyBjbGllbnRlcyBudWV2b3M6IHtOZXdDbGllbnRJbXBvcnRSb3cub2JqZWN0cy5jb3VudCgpfSIsCiAgICAgICAgICAgICAgICBmIkZpbGFzIHZlbnRhIGNydXphZGE6IHtDcm9zc1NhbGVJbXBvcnRSb3cub2JqZWN0cy5jb3VudCgpfSIsCiAgICAgICAgICAgICAgICBmIlRpcG9zIGRlIGNhbWJpbzoge01vbnRobHlFeGNoYW5nZVJhdGUub2JqZWN0cy5jb3VudCgpfSIsCiAgICAgICAgICAgICAgICBmIk1ldGFzIChNb250aGx5VGFyZ2V0KToge01vbnRobHlUYXJnZXQub2JqZWN0cy5jb3VudCgpfSIsCiAgICAgICAgICAgICAgICBmIlJlc3VsdGFkb3MgbcOpdHJpY2E6IHtNb250aGx5TWV0cmljUmVzdWx0Lm9iamVjdHMuY291bnQoKX0iLAogICAgICAgICAgICAgICAgZiJTY29yZWNhcmRzIG1vZG86IHtNb250aGx5TW9kZVNjb3JlY2FyZC5vYmplY3RzLmNvdW50KCl9IiwKICAgICAgICAgICAgICAgIGYiQ3VtcGxpbWllbnRvIHJlcXM6IHtNYW51YWxSZXF1aXJlbWVudHNDb21wbGlhbmNlLm9iamVjdHMuY291bnQoKX0iLAogICAgICAgICAgICBdCiAgICAgICAgKQogICAgKQoKICAgIGJ5X3BlcmlvZDogZGljdFtzdHIsIGRpY3Rbc3RyLCBpbnRdXSA9IGRlZmF1bHRkaWN0KGxhbWJkYTogZGVmYXVsdGRpY3QoaW50KSkKICAgIGZvciB5LCBtIGluIE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy52YWx1ZXNfbGlzdCgieWVhciIsICJtb250aCIpLmRpc3RpbmN0KCk6CiAgICAgICAgYnlfcGVyaW9kW3ltX2tleSh5LCBtKV1bInJlc3VsdGFkb3MiXSArPSAxCiAgICBmb3IgeSwgbSBpbiBOZXdDbGllbnRJbXBvcnRSb3cub2JqZWN0cy52YWx1ZXNfbGlzdCgieWVhciIsICJtb250aCIpLmRpc3RpbmN0KCk6CiAgICAgICAgYnlfcGVyaW9kW3ltX2tleSh5LCBtKV1bImNsaWVudGVzIl0gKz0gTmV3Q2xpZW50SW1wb3J0Um93Lm9iamVjdHMuZmlsdGVyKAogICAgICAgICAgICB5ZWFyPXksIG1vbnRoPW0KICAgICAgICApLmNvdW50KCkKICAgIGZvciB5LCBtIGluIENyb3NzU2FsZUltcG9ydFJvdy5vYmplY3RzLnZhbHVlc19saXN0KCJ5ZWFyIiwgIm1vbnRoIikuZGlzdGluY3QoKToKICAgICAgICBieV9wZXJpb2RbeW1fa2V5KHksIG0pXVsidmVudGFfY3J1emFkYSJdICs9IENyb3NzU2FsZUltcG9ydFJvdy5vYmplY3RzLmZpbHRlcigKICAgICAgICAgICAgeWVhcj15LCBtb250aD1tCiAgICAgICAgKS5jb3VudCgpCiAgICBmb3IgeSwgbSBpbiBNb250aGx5TW9kZVNjb3JlY2FyZC5vYmplY3RzLnZhbHVlc19saXN0KCJ5ZWFyIiwgIm1vbnRoIikuZGlzdGluY3QoKToKICAgICAgICBieV9wZXJpb2RbeW1fa2V5KHksIG0pXVsic2NvcmVjYXJkcyJdICs9IE1vbnRobHlNb2RlU2NvcmVjYXJkLm9iamVjdHMuZmlsdGVyKAogICAgICAgICAgICB5ZWFyPXksIG1vbnRoPW0KICAgICAgICApLmNvdW50KCkKICAgIGZvciB5LCBtIGluIE1vbnRobHlFeGNoYW5nZVJhdGUub2JqZWN0cy52YWx1ZXNfbGlzdCgieWVhciIsICJtb250aCIpOgogICAgICAgIGJ5X3BlcmlvZFt5bV9rZXkoeSwgbSldWyJmeCJdID0gMQogICAgZm9yIHksIG0gaW4gTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZS5vYmplY3RzLnZhbHVlc19saXN0KCJ5ZWFyIiwgIm1vbnRoIikuZGlzdGluY3QoKToKICAgICAgICBieV9wZXJpb2RbeW1fa2V5KHksIG0pXVsicmVxcyJdICs9IE1hbnVhbFJlcXVpcmVtZW50c0NvbXBsaWFuY2Uub2JqZWN0cy5maWx0ZXIoCiAgICAgICAgICAgIHllYXI9eSwgbW9udGg9bQogICAgICAgICkuY291bnQoKQoKICAgIHJvd3MgPSBbXQogICAgZm9yIGtleSBpbiBzb3J0ZWQoYnlfcGVyaW9kLmtleXMoKSk6CiAgICAgICAgZCA9IGJ5X3BlcmlvZFtrZXldCiAgICAgICAgcm93cy5hcHBlbmQoCiAgICAgICAgICAgIFsKICAgICAgICAgICAgICAgIGtleSwKICAgICAgICAgICAgICAgIGQuZ2V0KCJyZXN1bHRhZG9zIiwgMCksCiAgICAgICAgICAgICAgICBkLmdldCgiY2xpZW50ZXMiLCAwKSwKICAgICAgICAgICAgICAgIGQuZ2V0KCJ2ZW50YV9jcnV6YWRhIiwgMCksCiAgICAgICAgICAgICAgICBkLmdldCgicmVxcyIsIDApLAogICAgICAgICAgICAgICAgZC5nZXQoInNjb3JlY2FyZHMiLCAwKSwKICAgICAgICAgICAgICAgICJzw60iIGlmIGQuZ2V0KCJmeCIpIGVsc2UgIm5vIiwKICAgICAgICAgICAgXQogICAgICAgICkKICAgIG91dC5hcHBlbmQoaDMoIkNvYmVydHVyYSBwb3IgcGVyw61vZG8iKSkKICAgIG91dC5hcHBlbmQoCiAgICAgICAgbWRfdGFibGUoCiAgICAgICAgICAgIFsiUGVyw61vZG8iLCAiUmVzdWx0YWRvcyIsICJDbGllbnRlcyIsICJWdGEgY3J1emFkYSIsICJSZXFzIiwgIlNjb3JlcyIsICJGWCJdLAogICAgICAgICAgICByb3dzIG9yIFtbIuKAlCIsIDAsIDAsIDAsIDAsIDAsICJubyJdXSwKICAgICAgICApCiAgICApCgogICAgbWlzc2luZyA9IFtdCiAgICBpZiBwbGFuczoKICAgICAgICB5ZWFyID0gcGxhbnNbLTFdLnllYXIKICAgICAgICBmb3IgbW9udGggaW4gcmFuZ2UoMSwgMTMpOgogICAgICAgICAgICBrZXkgPSB5bV9rZXkoeWVhciwgbW9udGgpCiAgICAgICAgICAgIGQgPSBieV9wZXJpb2QuZ2V0KGtleSwge30pCiAgICAgICAgICAgIGdhcHMgPSBbXQogICAgICAgICAgICBpZiBub3QgZC5nZXQoImZ4Iik6CiAgICAgICAgICAgICAgICBnYXBzLmFwcGVuZCgiRlgiKQogICAgICAgICAgICBpZiBub3QgZC5nZXQoInNjb3JlY2FyZHMiKToKICAgICAgICAgICAgICAgIGdhcHMuYXBwZW5kKCJzY29yZSIpCiAgICAgICAgICAgIGlmIG5vdCBkLmdldCgicmVzdWx0YWRvcyIpOgogICAgICAgICAgICAgICAgZ2Fwcy5hcHBlbmQoInJlc3VsdGFkb3MiKQogICAgICAgICAgICBpZiBnYXBzOgogICAgICAgICAgICAgICAgbWlzc2luZy5hcHBlbmQoZiJ7cGVyaW9kX2xhYmVsKHllYXIsIG1vbnRoKX06IGZhbHRhIHsnLCAnLmpvaW4oZ2Fwcyl9IikKICAgIG91dC5hcHBlbmQoaDMoIkZhbHRhbnRlIC8gcGVuZGllbnRlIChQR0MpIikpCiAgICBvdXQuYXBwZW5kKGJ1bGxldHMobWlzc2luZ1s6MThdIG9yIFsiU2luIGh1ZWNvcyBldmlkZW50ZXMgZW4gZWwgw7psdGltbyBwbGFuLiJdKSkKICAgIHJldHVybiBvdXQKCgpkZWYgX3Bnb19jb3ZlcmFnZSgpIC0+IGxpc3Rbc3RyXToKICAgIG91dCA9IFtoMigiUEdPIOKAlCBjb2JlcnR1cmEiKV0KICAgIHRpY2tldHMgPSBUaWNrZXQub2JqZWN0cy5jb3VudCgpCiAgICBwZXJpb2RvcyA9IGxpc3QoCiAgICAgICAgUGdvUmVzdWx0YWRvUGVyaW9kby5vYmplY3RzLnZhbHVlc19saXN0KCJwZXJpb2RvIiwgZmxhdD1UcnVlKS5kaXN0aW5jdCgpLm9yZGVyX2J5KCJwZXJpb2RvIikKICAgICkKICAgIGJ5X2VzdGFkbyA9IGxpc3QoCiAgICAgICAgVGlja2V0Lm9iamVjdHMudmFsdWVzKCJlc3RhZG8iKS5hbm5vdGF0ZShuPUNvdW50KCJpZCIpKS5vcmRlcl9ieSgiZXN0YWRvIikKICAgICkKICAgIG91dC5hcHBlbmQoaDMoIkRpc3BvbmlibGUiKSkKICAgIG91dC5hcHBlbmQoCiAgICAgICAgYnVsbGV0cygKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgZiJUaWNrZXRzOiB7dGlja2V0c30iLAogICAgICAgICAgICAgICAgZiJSZXN1bHRhZG9zIHBlcsOtb2RvOiB7UGdvUmVzdWx0YWRvUGVyaW9kby5vYmplY3RzLmNvdW50KCl9IiwKICAgICAgICAgICAgICAgIGYiUGVyw61vZG9zIGNvbiByZXN1bHRhZG86IHsnLCAnLmpvaW4ocGVyaW9kb3MpIG9yICduaW5ndW5vJ30iLAogICAgICAgICAgICBdCiAgICAgICAgICAgICsgW2YiRXN0YWRvIHtyWydlc3RhZG8nXX06IHtyWyduJ119IiBmb3IgciBpbiBieV9lc3RhZG9dCiAgICAgICAgKQogICAgKQogICAgZ2FwcyA9IFtdCiAgICBpZiB0aWNrZXRzID09IDA6CiAgICAgICAgZ2Fwcy5hcHBlbmQoIlNpbiB0aWNrZXRzIGNhcmdhZG9zLiIpCiAgICBpZiBub3QgcGVyaW9kb3M6CiAgICAgICAgZ2Fwcy5hcHBlbmQoIlNpbiBQZ29SZXN1bHRhZG9QZXJpb2RvIGNhbGN1bGFkb3MuIikKICAgIG91dC5hcHBlbmQoaDMoIkZhbHRhbnRlIC8gcGVuZGllbnRlIChQR08pIikpCiAgICBvdXQuYXBwZW5kKGJ1bGxldHMoZ2FwcyBvciBbIkNvYmVydHVyYSBQR08gcHJlc2VudGUuIl0pKQogICAgcmV0dXJuIG91dAoKCmRlZiBfcmlza19jb3ZlcmFnZSgpIC0+IGxpc3Rbc3RyXToKICAgIG91dCA9IFtoMigiQi4gUmllc2dvIOKAlCBjb2JlcnR1cmEiKV0KICAgIHNuYXBzID0gUmlza09wZXJhdGlvblNuYXBzaG90Lm9iamVjdHMuY291bnQoKQogICAgZXN0YWRvcyA9IEVzdGFkb0ZpbmFuY2llcm8ub2JqZWN0cy5jb3VudCgpCiAgICBwZXJpb2RzID0gc29ydGVkKAogICAgICAgIHsKICAgICAgICAgICAgcy5zdHJmdGltZSgiJVktJW0iKQogICAgICAgICAgICBmb3IgcyBpbiBSaXNrT3BlcmF0aW9uU25hcHNob3Qub2JqZWN0cy52YWx1ZXNfbGlzdCgiZmVjaGFfc25hcHNob3QiLCBmbGF0PVRydWUpCiAgICAgICAgICAgIGlmIHMKICAgICAgICB9CiAgICApCiAgICBlZl9wZXJpb2RzID0gc29ydGVkKHNldChFc3RhZG9GaW5hbmNpZXJvLm9iamVjdHMudmFsdWVzX2xpc3QoInBlcmlvZG8iLCBmbGF0PVRydWUpKSkKICAgIG91dC5hcHBlbmQoaDMoIkRpc3BvbmlibGUiKSkKICAgIG91dC5hcHBlbmQoCiAgICAgICAgYnVsbGV0cygKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgZiJTbmFwc2hvdHMgb3BlcmFjacOzbjoge3NuYXBzfSIsCiAgICAgICAgICAgICAgICBmIkVzdGFkb3MgZmluYW5jaWVyb3M6IHtlc3RhZG9zfSIsCiAgICAgICAgICAgICAgICBmIlBlcsOtb2RvcyBzbmFwc2hvdDogeycsICcuam9pbihwZXJpb2RzWy0xMjpdKSBvciAnbmluZ3Vubyd9IiwKICAgICAgICAgICAgICAgIGYiUGVyw61vZG9zIEVGOiB7JywgJy5qb2luKGVmX3BlcmlvZHNbLTEyOl0pIG9yICduaW5ndW5vJ30iLAogICAgICAgICAgICAgICAgZiJDb24gYWxlcnRhOiB7Umlza09wZXJhdGlvblNuYXBzaG90Lm9iamVjdHMuZmlsdGVyKGFsZXJ0YT1UcnVlKS5jb3VudCgpfSIsCiAgICAgICAgICAgIF0KICAgICAgICApCiAgICApCiAgICBnYXBzID0gW10KICAgIGlmIHNuYXBzID09IDA6CiAgICAgICAgZ2Fwcy5hcHBlbmQoIlNpbiBSaXNrT3BlcmF0aW9uU25hcHNob3QuIikKICAgIGlmIGVzdGFkb3MgPT0gMDoKICAgICAgICBnYXBzLmFwcGVuZCgiU2luIEVzdGFkb0ZpbmFuY2llcm8uIikKICAgIG91dC5hcHBlbmQoaDMoIkZhbHRhbnRlIC8gcGVuZGllbnRlIChCLiBSaWVzZ28pIikpCiAgICBvdXQuYXBwZW5kKGJ1bGxldHMoZ2FwcyBvciBbIkNvYmVydHVyYSBkZSByaWVzZ28gcHJlc2VudGUuIl0pKQogICAgcmV0dXJuIG91dAoKCmRlZiBfZ2xvYmFsX2dhcHMoKSAtPiBsaXN0W3N0cl06CiAgICBnYXBzID0gW10KICAgIGlmIEZpbGVVcGxvYWQub2JqZWN0cy5maWx0ZXIoc3RhdHVzPUZpbGVVcGxvYWQuU1RBVFVTX1VQTE9BREVEKS5leGlzdHMoKToKICAgICAgICBnYXBzLmFwcGVuZCgiSGF5IGFyY2hpdm9zIFVQTE9BREVEIHBlbmRpZW50ZXMgZGUgcHJvY2VzYXIuIikKICAgIGlmIEZpbGVVcGxvYWQub2JqZWN0cy5maWx0ZXIoc3RhdHVzPUZpbGVVcGxvYWQuU1RBVFVTX1BBUlNFRF9FUlJPUikuZXhpc3RzKCk6CiAgICAgICAgZ2Fwcy5hcHBlbmQoIkhheSBhcmNoaXZvcyBjb24gUEFSU0VEX0VSUk9SLiIpCiAgICBpZiBub3QgTW9udGhseUV4Y2hhbmdlUmF0ZS5vYmplY3RzLmV4aXN0cygpOgogICAgICAgIGdhcHMuYXBwZW5kKCJObyBoYXkgdGlwb3MgZGUgY2FtYmlvIFBHQy4iKQogICAgaWYgVGlja2V0Lm9iamVjdHMuY291bnQoKSA9PSAwOgogICAgICAgIGdhcHMuYXBwZW5kKCJQR08gc2luIHRpY2tldHMuIikKICAgIGlmIFJpc2tPcGVyYXRpb25TbmFwc2hvdC5vYmplY3RzLmNvdW50KCkgPT0gMDoKICAgICAgICBnYXBzLmFwcGVuZCgiQi4gUmllc2dvIHNpbiBzbmFwc2hvdHMuIikKICAgIHJldHVybiBnYXBzIG9yIFsiU2luIHZhY8Otb3MgZ2xvYmFsZXMgY3LDrXRpY29zIGRldGVjdGFkb3MuIl0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/services/package.py
PATH_JSON="reports/services/package.py"
FILENAME=package.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=1
SIZE_BYTES_UTF8=85
CONTENT_SHA256=d0c58f53c86e49ab14076ea90f48ce0bd12d893d1808073ee5bd596bbbd33797
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
# reports/services package marker — generate_report_package exported from __init__

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|# reports/services package marker — generate_report_package exported from __init__

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IyByZXBvcnRzL3NlcnZpY2VzIHBhY2thZ2UgbWFya2VyIOKAlCBnZW5lcmF0ZV9yZXBvcnRfcGFja2FnZSBleHBvcnRlZCBmcm9tIF9faW5pdF9fCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/services/pgc_results.py
PATH_JSON="reports/services/pgc_results.py"
FILENAME=pgc_results.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=425
SIZE_BYTES_UTF8=15939
CONTENT_SHA256=cb3123f1fc3f18682dd806f15f8393b19865ae7d9c1fefcbf1693bb73e47778f
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
"""Resultados PGC extensos: tablero, charts, métricas, clientes browse, venta cruzada."""

from __future__ import annotations

from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from core.models import MetricDefinition, UNE
from imports.models import CrossSaleImportRow, NewClientImportRow
from pgc.models import (
    ManualRequirementsCompliance,
    MonthlyMetricResult,
    MonthlyMetricScore,
    MonthlyModeScorecard,
    MonthlyTarget,
)
from reports.md_utils import ai_closing, bullets, h1, h2, h3, join_sections, md_table, p
from reports.models import ReportConfig
from reports.naming import report_stamp
from reports.services.common import (
    fmt_num,
    pct_change,
    period_label,
    previous_month,
    ym_key,
)

SCORE_EXPLAIN = """
El **tablero principal PGC** consolida, por UNE y mes, los puntos de las métricas
scored (Ingresos, Clientes nuevos, Venta cruzada, Respuesta a requerimientos)
bajo una modalidad (`modo1` o `modo2`).

- Cada métrica tiene **meta** (`MonthlyTarget.target_value`) y **real**
  (`MonthlyMetricResult.measured_value`).
- El comando `recalc_pgc` asigna `points_awarded` en `MonthlyMetricScore`
  según la modalidad (cumplimiento meta vs real, con reglas adicionales en modo2).
- La suma es `MonthlyModeScorecard.total_points`.
- **Clasifica = Sí** si `total_points >= qualified_threshold` (default **80**).

Los charts del tablero grafican, por período y UNE, el **real vs meta** de
Ingresos (cifras en miles de US$), Clientes nuevos y Venta cruzada — no los
puntos del scorecard, sino las cifras de medición subyacentes.
""".strip()


def _all_score_periods() -> list[tuple[int, int]]:
    qs = (
        MonthlyModeScorecard.objects.order_by("year", "month")
        .values_list("year", "month")
        .distinct()
    )
    return [(int(y), int(m)) for y, m in qs]


def _sheet(name: str, title: str, headers: list, rows: list) -> dict:
    return {"name": name[:31], "title": title, "headers": headers, "rows": rows}


def build_pgc_results(cfg: ReportConfig | None = None) -> dict:
    cfg = cfg or ReportConfig.get_active()
    now = timezone.localtime()
    stamp = report_stamp(now)
    stamp_label = f"Generado {now.strftime('%Y-%m-%d %H:%M')} ({timezone.get_current_timezone_name()}) ·{stamp}"

    periods = _all_score_periods()
    if not periods and not MonthlyMetricResult.objects.exists():
        md = join_sections(
            h1("Reporte de resultados PGC"),
            p(stamp_label),
            p("No hay scorecards ni resultados PGC en la base."),
            ai_closing(
                ["Sin datos PGC."],
                ["Sin período anterior."],
                ["Cargar datos y ejecutar recalc_pgc."],
            ),
        )
        return {
            "md": md,
            "sheets": [
                _sheet("Resumen", "Sin datos", ["Nota"], [["Sin datos PGC"]])
            ],
            "stamp": stamp,
            "stamp_label": stamp_label,
        }

    mode = "modo1"
    latest = periods[-1] if periods else None
    if latest:
        prev = previous_month(*latest)
    else:
        prev = None

    # ---------- Scoreboard (como tablero) ----------
    scorecards = list(
        MonthlyModeScorecard.objects.filter(mode=mode)
        .select_related("une", "plan")
        .order_by("year", "month", "une__sort_order", "une__code")
    )
    score_map = {(s.year, s.month, s.une_id): s for s in scorecards}
    metric_scores = list(
        MonthlyMetricScore.objects.filter(mode=mode)
        .select_related("metric", "une")
        .order_by("year", "month", "metric__code")
    )
    points_by_key: dict[tuple[int, int, int], dict[str, Decimal]] = {}
    for ms in metric_scores:
        key = (ms.year, ms.month, ms.une_id)
        bucket = points_by_key.setdefault(key, {})
        bucket[ms.metric.code] = ms.points_awarded or Decimal("0")

    tablero_headers = [
        "UNE",
        "Periodo",
        "Pts Ingresos",
        "Pts Clientes",
        "Pts Venta cruzada",
        "Pts Respuesta reqs",
        "Total",
        "Umbral",
        "Clasifica",
    ]
    tablero_rows = []
    for s in scorecards:
        pts = points_by_key.get((s.year, s.month, s.une_id), {})
        tablero_rows.append(
            [
                s.une.code if s.une else "—",
                ym_key(s.year, s.month),
                fmt_num(pts.get(MetricDefinition.CODE_INGRESOS, 0)),
                fmt_num(pts.get(MetricDefinition.CODE_CLIENTES_NUEVOS, 0)),
                fmt_num(pts.get(MetricDefinition.CODE_VENTA_CRUZADA, 0)),
                fmt_num(pts.get(MetricDefinition.CODE_RESPUESTA_REQS, 0)),
                fmt_num(s.total_points),
                fmt_num(s.qualified_threshold or 80),
                "Sí" if s.is_month_qualified else "No",
            ]
        )

    # ---------- Chart series: real vs meta ----------
    chart_codes = [
        MetricDefinition.CODE_INGRESOS,
        MetricDefinition.CODE_CLIENTES_NUEVOS,
        MetricDefinition.CODE_VENTA_CRUZADA,
    ]
    chart_headers = ["Métrica", "Periodo", "UNE", "Meta", "Real", "Δ", "% Δ"]
    chart_rows = []
    for code in chart_codes:
        targets = MonthlyTarget.objects.filter(metric__code=code).select_related(
            "une", "metric"
        )
        results = {
            (r.year, r.month, r.une_id): r.measured_value
            for r in MonthlyMetricResult.objects.filter(metric__code=code)
        }
        for t in targets.order_by("year", "month", "une__sort_order"):
            real = results.get((t.year, t.month, t.une_id))
            meta = t.target_value
            dlt = (real or Decimal("0")) - (meta or Decimal("0")) if real is not None and meta is not None else None
            chart_rows.append(
                [
                    code,
                    ym_key(t.year, t.month),
                    t.une.code if t.une else "—",
                    fmt_num(meta, 2) if meta is not None else "—",
                    fmt_num(real, 2) if real is not None else "—",
                    fmt_num(dlt, 2) if dlt is not None else "—",
                    pct_change(real, meta) if real is not None and meta is not None else "—",
                ]
            )

    # ---------- Ingresos / clientes / venta cruzada measured dump ----------
    metric_result_headers = [
        "Métrica",
        "Periodo",
        "UNE",
        "Meta",
        "Real",
        "Moneda fuente",
        "Estado conversión",
        "Nota",
    ]
    metric_result_rows = []
    for r in (
        MonthlyMetricResult.objects.select_related("metric", "une")
        .order_by("metric__code", "year", "month", "une__sort_order")
    ):
        tgt = (
            MonthlyTarget.objects.filter(
                plan_id=r.plan_id,
                metric_id=r.metric_id,
                une_id=r.une_id,
                year=r.year,
                month=r.month,
            )
            .values_list("target_value", flat=True)
            .first()
        )
        metric_result_rows.append(
            [
                r.metric.code if r.metric else "—",
                ym_key(r.year, r.month),
                r.une.code if r.une else "—",
                fmt_num(tgt, 2) if tgt is not None else "—",
                fmt_num(r.measured_value, 2) if r.measured_value is not None else "—",
                getattr(r, "source_currency", "") or "—",
                getattr(r, "conversion_status", "") or "—",
                (r.calculation_note or "")[:120],
            ]
        )

    # ---------- Clientes nuevos — detalle browse ----------
    client_headers = [
        "Periodo",
        "UNE",
        "Cliente",
        "NIT",
        "Operación",
        "Contratos previos",
        "Cuenta como nuevo",
        "Moneda",
        "Monto (miles si USD PGC)",
        "UNE cruda",
        "Observaciones",
        "Fila origen",
    ]
    client_rows = []
    for row in (
        NewClientImportRow.objects.select_related("une", "currency")
        .order_by("year", "month", "une__sort_order", "client_name", "id")
    ):
        client_rows.append(
            [
                ym_key(row.year, row.month),
                row.une.code if row.une else "—",
                row.client_name,
                row.nit,
                row.operation_code,
                row.previous_contracts,
                "Sí" if row.counts_as_new else "No",
                row.currency.code if row.currency else "—",
                fmt_num(row.amount, 2) if row.amount is not None else "—",
                row.raw_une_value,
                row.observations or "",
                row.source_row_number or "",
            ]
        )

    # ---------- Venta cruzada detalle ----------
    xc_headers = [
        "Periodo",
        "Cliente",
        "Operación",
        "Fecha",
        "Moneda",
        "UNE origen",
        "UNE destino",
        "UNE origen raw",
        "UNE destino raw",
    ]
    xc_rows = []
    for row in (
        CrossSaleImportRow.objects.select_related(
            "currency", "une_origin", "une_destination"
        ).order_by("year", "month", "client_name", "id")
    ):
        xc_rows.append(
            [
                ym_key(row.year, row.month),
                row.client_name,
                row.operation_code,
                row.date.isoformat() if row.date else "",
                row.currency.code if row.currency else "—",
                row.une_origin.code if row.une_origin else "—",
                row.une_destination.code if row.une_destination else "—",
                row.raw_une_origin,
                row.raw_une_destination,
            ]
        )

    # ---------- Requerimientos ----------
    req_headers = ["Periodo", "UNE", "Cumple", "Nota incidente"]
    req_rows = []
    for r in ManualRequirementsCompliance.objects.select_related("une").order_by(
        "year", "month", "une__sort_order"
    ):
        req_rows.append(
            [
                ym_key(r.year, r.month),
                r.une.code if r.une else "—",
                "Sí" if r.is_compliant else "No",
                (r.incident_note or "")[:200],
            ]
        )

    # ---------- Comparación último vs anterior ----------
    cambios = []
    hechos = [
        f"Modalidad de score reportada: {mode}",
        f"Filas tablero (scorecards): {len(tablero_rows)}",
        f"Series chart (meta/real): {len(chart_rows)}",
        f"Resultados métrica: {len(metric_result_rows)}",
        f"Detalle clientes: {len(client_rows)}",
        f"Detalle venta cruzada: {len(xc_rows)}",
        f"Cumplimiento reqs: {len(req_rows)}",
    ]
    if latest:
        hechos.append(f"Último período con score: {period_label(*latest)} ({ym_key(*latest)})")
        ly, lm = latest
        for une in UNE.objects.filter(is_active=True).order_by("sort_order"):
            cur = score_map.get((ly, lm, une.id))
            if not cur or not prev:
                continue
            prv = score_map.get((prev[0], prev[1], une.id))
            if not prv:
                continue
            cambios.append(
                f"{une.code} {ym_key(*prev)}→{ym_key(*latest)}: "
                f"{fmt_num(prv.total_points)} → {fmt_num(cur.total_points)} "
                f"({pct_change(cur.total_points, prv.total_points)}); "
                f"Clasifica {('Sí' if prv.is_month_qualified else 'No')}→"
                f"{('Sí' if cur.is_month_qualified else 'No')}"
            )

    vacios = []
    if not tablero_rows:
        vacios.append("Sin MonthlyModeScorecard (ejecutar recalc_pgc).")
    if not client_rows:
        vacios.append("Sin NewClientImportRow.")
    if not xc_rows:
        vacios.append("Sin CrossSaleImportRow.")
    if not chart_rows:
        vacios.append("Sin metas/reales para charts.")
    if latest and prev and not cambios:
        vacios.append(
            f"Hay último período {ym_key(*latest)} pero pocas comparaciones vs {ym_key(*prev)}."
        )

    # ---------- Markdown ----------
    md_parts = [
        h1("Reporte de resultados PGC (extenso)"),
        p(stamp_label),
        p(
            "Propósito: entregar a IA generativa y a usuarios humanos el **detalle operativo** "
            "del PGC (tablero, cifras de charts, clientes, venta cruzada) para análisis estratégico."
        ),
        h2("Cómo interpretar el tablero y el cálculo"),
        p(SCORE_EXPLAIN),
        h2("Tabla de puntos del tablero principal"),
        p(f"Modalidad: **{mode}**. Filas: **{len(tablero_rows)}**."),
        md_table(tablero_headers, tablero_rows)
        if tablero_rows
        else p("_Sin scorecards._"),
        h2("Cifras base de los charts (meta vs real)"),
        p(
            "Ingresos en miles de US$ según regla PGC; clientes y venta cruzada en unidades del sistema. "
            f"Filas: **{len(chart_rows)}**."
        ),
        md_table(chart_headers, chart_rows) if chart_rows else p("_Sin series chart._"),
        h2("Resultados de métricas (MonthlyMetricResult)"),
        md_table(metric_result_headers, metric_result_rows)
        if metric_result_rows
        else p("_Sin resultados._"),
        h2("Clientes nuevos — detalle completo (browse)"),
        p(
            "Equivalente al detalle visto en Administración → Clientes (browse). "
            f"Registros: **{len(client_rows)}**."
        ),
        md_table(client_headers, client_rows) if client_rows else p("_Sin clientes importados._"),
        h2("Venta cruzada — detalle"),
        p(f"Registros: **{len(xc_rows)}**."),
        md_table(xc_headers, xc_rows) if xc_rows else p("_Sin venta cruzada._"),
        h2("Respuesta a requerimientos"),
        md_table(req_headers, req_rows) if req_rows else p("_Sin registros de requerimientos._"),
        h2("Cambios último período vs anterior"),
        bullets(cambios[:40] or ["Sin pares comparables suficientes."]),
        h2("Inventario de cobertura en este reporte"),
        bullets(hechos),
    ]
    if cfg.include_ai_section:
        md_parts.append(
            ai_closing(
                hechos,
                cambios[:30] if cfg.include_period_comparison else ["Comparación desactivada en config."],
                vacios or ["Sin vacíos críticos detectados en PGC."],
            )
        )
    md_parts.append(
        p(
            "_Instrucción para IA:_ con las tablas anteriores, elabora un análisis estratégico "
            "(estado, tendencias, riesgos, oportunidades y recomendaciones accionables) "
            "sin inventar cifras que no aparezcan aquí."
        )
    )

    sheets = [
        _sheet("Tablero puntos", f"Tablero PGC {mode}", tablero_headers, tablero_rows),
        _sheet("Charts meta real", "Series charts PGC", chart_headers, chart_rows),
        _sheet("Metricas medidas", "MonthlyMetricResult", metric_result_headers, metric_result_rows),
        _sheet("Clientes detalle", "NewClientImportRow browse", client_headers, client_rows),
        _sheet("Venta cruzada", "CrossSaleImportRow", xc_headers, xc_rows),
        _sheet("Requerimientos", "ManualRequirementsCompliance", req_headers, req_rows),
        _sheet(
            "Explicacion",
            "Sentido del cálculo PGC",
            ["Tema", "Detalle"],
            [
                ["Modalidad", mode],
                ["Umbral clasifica default", "80 puntos (qualified_threshold)"],
                ["Clasifica", "total_points >= qualified_threshold"],
                ["Charts", "real vs meta INGRESOS / CLIENTES_NUEVOS / VENTA_CRUZADA"],
                ["Fuente clientes", "NewClientImportRow (browse admin)"],
            ],
        ),
    ]

    return {
        "md": join_sections(*md_parts),
        "sheets": sheets,
        "stamp": stamp,
        "stamp_label": stamp_label,
        "period": latest,
        "prev_period": prev,
    }

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Resultados PGC extensos: tablero, charts, métricas, clientes browse, venta cruzada."""
00002|
00003|from __future__ import annotations
00004|
00005|from decimal import Decimal
00006|
00007|from django.db.models import Sum
00008|from django.utils import timezone
00009|
00010|from core.models import MetricDefinition, UNE
00011|from imports.models import CrossSaleImportRow, NewClientImportRow
00012|from pgc.models import (
00013|    ManualRequirementsCompliance,
00014|    MonthlyMetricResult,
00015|    MonthlyMetricScore,
00016|    MonthlyModeScorecard,
00017|    MonthlyTarget,
00018|)
00019|from reports.md_utils import ai_closing, bullets, h1, h2, h3, join_sections, md_table, p
00020|from reports.models import ReportConfig
00021|from reports.naming import report_stamp
00022|from reports.services.common import (
00023|    fmt_num,
00024|    pct_change,
00025|    period_label,
00026|    previous_month,
00027|    ym_key,
00028|)
00029|
00030|SCORE_EXPLAIN = """
00031|El **tablero principal PGC** consolida, por UNE y mes, los puntos de las métricas
00032|scored (Ingresos, Clientes nuevos, Venta cruzada, Respuesta a requerimientos)
00033|bajo una modalidad (`modo1` o `modo2`).
00034|
00035|- Cada métrica tiene **meta** (`MonthlyTarget.target_value`) y **real**
00036|  (`MonthlyMetricResult.measured_value`).
00037|- El comando `recalc_pgc` asigna `points_awarded` en `MonthlyMetricScore`
00038|  según la modalidad (cumplimiento meta vs real, con reglas adicionales en modo2).
00039|- La suma es `MonthlyModeScorecard.total_points`.
00040|- **Clasifica = Sí** si `total_points >= qualified_threshold` (default **80**).
00041|
00042|Los charts del tablero grafican, por período y UNE, el **real vs meta** de
00043|Ingresos (cifras en miles de US$), Clientes nuevos y Venta cruzada — no los
00044|puntos del scorecard, sino las cifras de medición subyacentes.
00045|""".strip()
00046|
00047|
00048|def _all_score_periods() -> list[tuple[int, int]]:
00049|    qs = (
00050|        MonthlyModeScorecard.objects.order_by("year", "month")
00051|        .values_list("year", "month")
00052|        .distinct()
00053|    )
00054|    return [(int(y), int(m)) for y, m in qs]
00055|
00056|
00057|def _sheet(name: str, title: str, headers: list, rows: list) -> dict:
00058|    return {"name": name[:31], "title": title, "headers": headers, "rows": rows}
00059|
00060|
00061|def build_pgc_results(cfg: ReportConfig | None = None) -> dict:
00062|    cfg = cfg or ReportConfig.get_active()
00063|    now = timezone.localtime()
00064|    stamp = report_stamp(now)
00065|    stamp_label = f"Generado {now.strftime('%Y-%m-%d %H:%M')} ({timezone.get_current_timezone_name()}) ·{stamp}"
00066|
00067|    periods = _all_score_periods()
00068|    if not periods and not MonthlyMetricResult.objects.exists():
00069|        md = join_sections(
00070|            h1("Reporte de resultados PGC"),
00071|            p(stamp_label),
00072|            p("No hay scorecards ni resultados PGC en la base."),
00073|            ai_closing(
00074|                ["Sin datos PGC."],
00075|                ["Sin período anterior."],
00076|                ["Cargar datos y ejecutar recalc_pgc."],
00077|            ),
00078|        )
00079|        return {
00080|            "md": md,
00081|            "sheets": [
00082|                _sheet("Resumen", "Sin datos", ["Nota"], [["Sin datos PGC"]])
00083|            ],
00084|            "stamp": stamp,
00085|            "stamp_label": stamp_label,
00086|        }
00087|
00088|    mode = "modo1"
00089|    latest = periods[-1] if periods else None
00090|    if latest:
00091|        prev = previous_month(*latest)
00092|    else:
00093|        prev = None
00094|
00095|    # ---------- Scoreboard (como tablero) ----------
00096|    scorecards = list(
00097|        MonthlyModeScorecard.objects.filter(mode=mode)
00098|        .select_related("une", "plan")
00099|        .order_by("year", "month", "une__sort_order", "une__code")
00100|    )
00101|    score_map = {(s.year, s.month, s.une_id): s for s in scorecards}
00102|    metric_scores = list(
00103|        MonthlyMetricScore.objects.filter(mode=mode)
00104|        .select_related("metric", "une")
00105|        .order_by("year", "month", "metric__code")
00106|    )
00107|    points_by_key: dict[tuple[int, int, int], dict[str, Decimal]] = {}
00108|    for ms in metric_scores:
00109|        key = (ms.year, ms.month, ms.une_id)
00110|        bucket = points_by_key.setdefault(key, {})
00111|        bucket[ms.metric.code] = ms.points_awarded or Decimal("0")
00112|
00113|    tablero_headers = [
00114|        "UNE",
00115|        "Periodo",
00116|        "Pts Ingresos",
00117|        "Pts Clientes",
00118|        "Pts Venta cruzada",
00119|        "Pts Respuesta reqs",
00120|        "Total",
00121|        "Umbral",
00122|        "Clasifica",
00123|    ]
00124|    tablero_rows = []
00125|    for s in scorecards:
00126|        pts = points_by_key.get((s.year, s.month, s.une_id), {})
00127|        tablero_rows.append(
00128|            [
00129|                s.une.code if s.une else "—",
00130|                ym_key(s.year, s.month),
00131|                fmt_num(pts.get(MetricDefinition.CODE_INGRESOS, 0)),
00132|                fmt_num(pts.get(MetricDefinition.CODE_CLIENTES_NUEVOS, 0)),
00133|                fmt_num(pts.get(MetricDefinition.CODE_VENTA_CRUZADA, 0)),
00134|                fmt_num(pts.get(MetricDefinition.CODE_RESPUESTA_REQS, 0)),
00135|                fmt_num(s.total_points),
00136|                fmt_num(s.qualified_threshold or 80),
00137|                "Sí" if s.is_month_qualified else "No",
00138|            ]
00139|        )
00140|
00141|    # ---------- Chart series: real vs meta ----------
00142|    chart_codes = [
00143|        MetricDefinition.CODE_INGRESOS,
00144|        MetricDefinition.CODE_CLIENTES_NUEVOS,
00145|        MetricDefinition.CODE_VENTA_CRUZADA,
00146|    ]
00147|    chart_headers = ["Métrica", "Periodo", "UNE", "Meta", "Real", "Δ", "% Δ"]
00148|    chart_rows = []
00149|    for code in chart_codes:
00150|        targets = MonthlyTarget.objects.filter(metric__code=code).select_related(
00151|            "une", "metric"
00152|        )
00153|        results = {
00154|            (r.year, r.month, r.une_id): r.measured_value
00155|            for r in MonthlyMetricResult.objects.filter(metric__code=code)
00156|        }
00157|        for t in targets.order_by("year", "month", "une__sort_order"):
00158|            real = results.get((t.year, t.month, t.une_id))
00159|            meta = t.target_value
00160|            dlt = (real or Decimal("0")) - (meta or Decimal("0")) if real is not None and meta is not None else None
00161|            chart_rows.append(
00162|                [
00163|                    code,
00164|                    ym_key(t.year, t.month),
00165|                    t.une.code if t.une else "—",
00166|                    fmt_num(meta, 2) if meta is not None else "—",
00167|                    fmt_num(real, 2) if real is not None else "—",
00168|                    fmt_num(dlt, 2) if dlt is not None else "—",
00169|                    pct_change(real, meta) if real is not None and meta is not None else "—",
00170|                ]
00171|            )
00172|
00173|    # ---------- Ingresos / clientes / venta cruzada measured dump ----------
00174|    metric_result_headers = [
00175|        "Métrica",
00176|        "Periodo",
00177|        "UNE",
00178|        "Meta",
00179|        "Real",
00180|        "Moneda fuente",
00181|        "Estado conversión",
00182|        "Nota",
00183|    ]
00184|    metric_result_rows = []
00185|    for r in (
00186|        MonthlyMetricResult.objects.select_related("metric", "une")
00187|        .order_by("metric__code", "year", "month", "une__sort_order")
00188|    ):
00189|        tgt = (
00190|            MonthlyTarget.objects.filter(
00191|                plan_id=r.plan_id,
00192|                metric_id=r.metric_id,
00193|                une_id=r.une_id,
00194|                year=r.year,
00195|                month=r.month,
00196|            )
00197|            .values_list("target_value", flat=True)
00198|            .first()
00199|        )
00200|        metric_result_rows.append(
00201|            [
00202|                r.metric.code if r.metric else "—",
00203|                ym_key(r.year, r.month),
00204|                r.une.code if r.une else "—",
00205|                fmt_num(tgt, 2) if tgt is not None else "—",
00206|                fmt_num(r.measured_value, 2) if r.measured_value is not None else "—",
00207|                getattr(r, "source_currency", "") or "—",
00208|                getattr(r, "conversion_status", "") or "—",
00209|                (r.calculation_note or "")[:120],
00210|            ]
00211|        )
00212|
00213|    # ---------- Clientes nuevos — detalle browse ----------
00214|    client_headers = [
00215|        "Periodo",
00216|        "UNE",
00217|        "Cliente",
00218|        "NIT",
00219|        "Operación",
00220|        "Contratos previos",
00221|        "Cuenta como nuevo",
00222|        "Moneda",
00223|        "Monto (miles si USD PGC)",
00224|        "UNE cruda",
00225|        "Observaciones",
00226|        "Fila origen",
00227|    ]
00228|    client_rows = []
00229|    for row in (
00230|        NewClientImportRow.objects.select_related("une", "currency")
00231|        .order_by("year", "month", "une__sort_order", "client_name", "id")
00232|    ):
00233|        client_rows.append(
00234|            [
00235|                ym_key(row.year, row.month),
00236|                row.une.code if row.une else "—",
00237|                row.client_name,
00238|                row.nit,
00239|                row.operation_code,
00240|                row.previous_contracts,
00241|                "Sí" if row.counts_as_new else "No",
00242|                row.currency.code if row.currency else "—",
00243|                fmt_num(row.amount, 2) if row.amount is not None else "—",
00244|                row.raw_une_value,
00245|                row.observations or "",
00246|                row.source_row_number or "",
00247|            ]
00248|        )
00249|
00250|    # ---------- Venta cruzada detalle ----------
00251|    xc_headers = [
00252|        "Periodo",
00253|        "Cliente",
00254|        "Operación",
00255|        "Fecha",
00256|        "Moneda",
00257|        "UNE origen",
00258|        "UNE destino",
00259|        "UNE origen raw",
00260|        "UNE destino raw",
00261|    ]
00262|    xc_rows = []
00263|    for row in (
00264|        CrossSaleImportRow.objects.select_related(
00265|            "currency", "une_origin", "une_destination"
00266|        ).order_by("year", "month", "client_name", "id")
00267|    ):
00268|        xc_rows.append(
00269|            [
00270|                ym_key(row.year, row.month),
00271|                row.client_name,
00272|                row.operation_code,
00273|                row.date.isoformat() if row.date else "",
00274|                row.currency.code if row.currency else "—",
00275|                row.une_origin.code if row.une_origin else "—",
00276|                row.une_destination.code if row.une_destination else "—",
00277|                row.raw_une_origin,
00278|                row.raw_une_destination,
00279|            ]
00280|        )
00281|
00282|    # ---------- Requerimientos ----------
00283|    req_headers = ["Periodo", "UNE", "Cumple", "Nota incidente"]
00284|    req_rows = []
00285|    for r in ManualRequirementsCompliance.objects.select_related("une").order_by(
00286|        "year", "month", "une__sort_order"
00287|    ):
00288|        req_rows.append(
00289|            [
00290|                ym_key(r.year, r.month),
00291|                r.une.code if r.une else "—",
00292|                "Sí" if r.is_compliant else "No",
00293|                (r.incident_note or "")[:200],
00294|            ]
00295|        )
00296|
00297|    # ---------- Comparación último vs anterior ----------
00298|    cambios = []
00299|    hechos = [
00300|        f"Modalidad de score reportada: {mode}",
00301|        f"Filas tablero (scorecards): {len(tablero_rows)}",
00302|        f"Series chart (meta/real): {len(chart_rows)}",
00303|        f"Resultados métrica: {len(metric_result_rows)}",
00304|        f"Detalle clientes: {len(client_rows)}",
00305|        f"Detalle venta cruzada: {len(xc_rows)}",
00306|        f"Cumplimiento reqs: {len(req_rows)}",
00307|    ]
00308|    if latest:
00309|        hechos.append(f"Último período con score: {period_label(*latest)} ({ym_key(*latest)})")
00310|        ly, lm = latest
00311|        for une in UNE.objects.filter(is_active=True).order_by("sort_order"):
00312|            cur = score_map.get((ly, lm, une.id))
00313|            if not cur or not prev:
00314|                continue
00315|            prv = score_map.get((prev[0], prev[1], une.id))
00316|            if not prv:
00317|                continue
00318|            cambios.append(
00319|                f"{une.code} {ym_key(*prev)}→{ym_key(*latest)}: "
00320|                f"{fmt_num(prv.total_points)} → {fmt_num(cur.total_points)} "
00321|                f"({pct_change(cur.total_points, prv.total_points)}); "
00322|                f"Clasifica {('Sí' if prv.is_month_qualified else 'No')}→"
00323|                f"{('Sí' if cur.is_month_qualified else 'No')}"
00324|            )
00325|
00326|    vacios = []
00327|    if not tablero_rows:
00328|        vacios.append("Sin MonthlyModeScorecard (ejecutar recalc_pgc).")
00329|    if not client_rows:
00330|        vacios.append("Sin NewClientImportRow.")
00331|    if not xc_rows:
00332|        vacios.append("Sin CrossSaleImportRow.")
00333|    if not chart_rows:
00334|        vacios.append("Sin metas/reales para charts.")
00335|    if latest and prev and not cambios:
00336|        vacios.append(
00337|            f"Hay último período {ym_key(*latest)} pero pocas comparaciones vs {ym_key(*prev)}."
00338|        )
00339|
00340|    # ---------- Markdown ----------
00341|    md_parts = [
00342|        h1("Reporte de resultados PGC (extenso)"),
00343|        p(stamp_label),
00344|        p(
00345|            "Propósito: entregar a IA generativa y a usuarios humanos el **detalle operativo** "
00346|            "del PGC (tablero, cifras de charts, clientes, venta cruzada) para análisis estratégico."
00347|        ),
00348|        h2("Cómo interpretar el tablero y el cálculo"),
00349|        p(SCORE_EXPLAIN),
00350|        h2("Tabla de puntos del tablero principal"),
00351|        p(f"Modalidad: **{mode}**. Filas: **{len(tablero_rows)}**."),
00352|        md_table(tablero_headers, tablero_rows)
00353|        if tablero_rows
00354|        else p("_Sin scorecards._"),
00355|        h2("Cifras base de los charts (meta vs real)"),
00356|        p(
00357|            "Ingresos en miles de US$ según regla PGC; clientes y venta cruzada en unidades del sistema. "
00358|            f"Filas: **{len(chart_rows)}**."
00359|        ),
00360|        md_table(chart_headers, chart_rows) if chart_rows else p("_Sin series chart._"),
00361|        h2("Resultados de métricas (MonthlyMetricResult)"),
00362|        md_table(metric_result_headers, metric_result_rows)
00363|        if metric_result_rows
00364|        else p("_Sin resultados._"),
00365|        h2("Clientes nuevos — detalle completo (browse)"),
00366|        p(
00367|            "Equivalente al detalle visto en Administración → Clientes (browse). "
00368|            f"Registros: **{len(client_rows)}**."
00369|        ),
00370|        md_table(client_headers, client_rows) if client_rows else p("_Sin clientes importados._"),
00371|        h2("Venta cruzada — detalle"),
00372|        p(f"Registros: **{len(xc_rows)}**."),
00373|        md_table(xc_headers, xc_rows) if xc_rows else p("_Sin venta cruzada._"),
00374|        h2("Respuesta a requerimientos"),
00375|        md_table(req_headers, req_rows) if req_rows else p("_Sin registros de requerimientos._"),
00376|        h2("Cambios último período vs anterior"),
00377|        bullets(cambios[:40] or ["Sin pares comparables suficientes."]),
00378|        h2("Inventario de cobertura en este reporte"),
00379|        bullets(hechos),
00380|    ]
00381|    if cfg.include_ai_section:
00382|        md_parts.append(
00383|            ai_closing(
00384|                hechos,
00385|                cambios[:30] if cfg.include_period_comparison else ["Comparación desactivada en config."],
00386|                vacios or ["Sin vacíos críticos detectados en PGC."],
00387|            )
00388|        )
00389|    md_parts.append(
00390|        p(
00391|            "_Instrucción para IA:_ con las tablas anteriores, elabora un análisis estratégico "
00392|            "(estado, tendencias, riesgos, oportunidades y recomendaciones accionables) "
00393|            "sin inventar cifras que no aparezcan aquí."
00394|        )
00395|    )
00396|
00397|    sheets = [
00398|        _sheet("Tablero puntos", f"Tablero PGC {mode}", tablero_headers, tablero_rows),
00399|        _sheet("Charts meta real", "Series charts PGC", chart_headers, chart_rows),
00400|        _sheet("Metricas medidas", "MonthlyMetricResult", metric_result_headers, metric_result_rows),
00401|        _sheet("Clientes detalle", "NewClientImportRow browse", client_headers, client_rows),
00402|        _sheet("Venta cruzada", "CrossSaleImportRow", xc_headers, xc_rows),
00403|        _sheet("Requerimientos", "ManualRequirementsCompliance", req_headers, req_rows),
00404|        _sheet(
00405|            "Explicacion",
00406|            "Sentido del cálculo PGC",
00407|            ["Tema", "Detalle"],
00408|            [
00409|                ["Modalidad", mode],
00410|                ["Umbral clasifica default", "80 puntos (qualified_threshold)"],
00411|                ["Clasifica", "total_points >= qualified_threshold"],
00412|                ["Charts", "real vs meta INGRESOS / CLIENTES_NUEVOS / VENTA_CRUZADA"],
00413|                ["Fuente clientes", "NewClientImportRow (browse admin)"],
00414|            ],
00415|        ),
00416|    ]
00417|
00418|    return {
00419|        "md": join_sections(*md_parts),
00420|        "sheets": sheets,
00421|        "stamp": stamp,
00422|        "stamp_label": stamp_label,
00423|        "period": latest,
00424|        "prev_period": prev,
00425|    }

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiUmVzdWx0YWRvcyBQR0MgZXh0ZW5zb3M6IHRhYmxlcm8sIGNoYXJ0cywgbcOpdHJpY2FzLCBjbGllbnRlcyBicm93c2UsIHZlbnRhIGNydXphZGEuIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgpmcm9tIGRlY2ltYWwgaW1wb3J0IERlY2ltYWwKCmZyb20gZGphbmdvLmRiLm1vZGVscyBpbXBvcnQgU3VtCmZyb20gZGphbmdvLnV0aWxzIGltcG9ydCB0aW1lem9uZQoKZnJvbSBjb3JlLm1vZGVscyBpbXBvcnQgTWV0cmljRGVmaW5pdGlvbiwgVU5FCmZyb20gaW1wb3J0cy5tb2RlbHMgaW1wb3J0IENyb3NzU2FsZUltcG9ydFJvdywgTmV3Q2xpZW50SW1wb3J0Um93CmZyb20gcGdjLm1vZGVscyBpbXBvcnQgKAogICAgTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZSwKICAgIE1vbnRobHlNZXRyaWNSZXN1bHQsCiAgICBNb250aGx5TWV0cmljU2NvcmUsCiAgICBNb250aGx5TW9kZVNjb3JlY2FyZCwKICAgIE1vbnRobHlUYXJnZXQsCikKZnJvbSByZXBvcnRzLm1kX3V0aWxzIGltcG9ydCBhaV9jbG9zaW5nLCBidWxsZXRzLCBoMSwgaDIsIGgzLCBqb2luX3NlY3Rpb25zLCBtZF90YWJsZSwgcApmcm9tIHJlcG9ydHMubW9kZWxzIGltcG9ydCBSZXBvcnRDb25maWcKZnJvbSByZXBvcnRzLm5hbWluZyBpbXBvcnQgcmVwb3J0X3N0YW1wCmZyb20gcmVwb3J0cy5zZXJ2aWNlcy5jb21tb24gaW1wb3J0ICgKICAgIGZtdF9udW0sCiAgICBwY3RfY2hhbmdlLAogICAgcGVyaW9kX2xhYmVsLAogICAgcHJldmlvdXNfbW9udGgsCiAgICB5bV9rZXksCikKClNDT1JFX0VYUExBSU4gPSAiIiIKRWwgKip0YWJsZXJvIHByaW5jaXBhbCBQR0MqKiBjb25zb2xpZGEsIHBvciBVTkUgeSBtZXMsIGxvcyBwdW50b3MgZGUgbGFzIG3DqXRyaWNhcwpzY29yZWQgKEluZ3Jlc29zLCBDbGllbnRlcyBudWV2b3MsIFZlbnRhIGNydXphZGEsIFJlc3B1ZXN0YSBhIHJlcXVlcmltaWVudG9zKQpiYWpvIHVuYSBtb2RhbGlkYWQgKGBtb2RvMWAgbyBgbW9kbzJgKS4KCi0gQ2FkYSBtw6l0cmljYSB0aWVuZSAqKm1ldGEqKiAoYE1vbnRobHlUYXJnZXQudGFyZ2V0X3ZhbHVlYCkgeSAqKnJlYWwqKgogIChgTW9udGhseU1ldHJpY1Jlc3VsdC5tZWFzdXJlZF92YWx1ZWApLgotIEVsIGNvbWFuZG8gYHJlY2FsY19wZ2NgIGFzaWduYSBgcG9pbnRzX2F3YXJkZWRgIGVuIGBNb250aGx5TWV0cmljU2NvcmVgCiAgc2Vnw7puIGxhIG1vZGFsaWRhZCAoY3VtcGxpbWllbnRvIG1ldGEgdnMgcmVhbCwgY29uIHJlZ2xhcyBhZGljaW9uYWxlcyBlbiBtb2RvMikuCi0gTGEgc3VtYSBlcyBgTW9udGhseU1vZGVTY29yZWNhcmQudG90YWxfcG9pbnRzYC4KLSAqKkNsYXNpZmljYSA9IFPDrSoqIHNpIGB0b3RhbF9wb2ludHMgPj0gcXVhbGlmaWVkX3RocmVzaG9sZGAgKGRlZmF1bHQgKio4MCoqKS4KCkxvcyBjaGFydHMgZGVsIHRhYmxlcm8gZ3JhZmljYW4sIHBvciBwZXLDrW9kbyB5IFVORSwgZWwgKipyZWFsIHZzIG1ldGEqKiBkZQpJbmdyZXNvcyAoY2lmcmFzIGVuIG1pbGVzIGRlIFVTJCksIENsaWVudGVzIG51ZXZvcyB5IFZlbnRhIGNydXphZGEg4oCUIG5vIGxvcwpwdW50b3MgZGVsIHNjb3JlY2FyZCwgc2lubyBsYXMgY2lmcmFzIGRlIG1lZGljacOzbiBzdWJ5YWNlbnRlcy4KIiIiLnN0cmlwKCkKCgpkZWYgX2FsbF9zY29yZV9wZXJpb2RzKCkgLT4gbGlzdFt0dXBsZVtpbnQsIGludF1dOgogICAgcXMgPSAoCiAgICAgICAgTW9udGhseU1vZGVTY29yZWNhcmQub2JqZWN0cy5vcmRlcl9ieSgieWVhciIsICJtb250aCIpCiAgICAgICAgLnZhbHVlc19saXN0KCJ5ZWFyIiwgIm1vbnRoIikKICAgICAgICAuZGlzdGluY3QoKQogICAgKQogICAgcmV0dXJuIFsoaW50KHkpLCBpbnQobSkpIGZvciB5LCBtIGluIHFzXQoKCmRlZiBfc2hlZXQobmFtZTogc3RyLCB0aXRsZTogc3RyLCBoZWFkZXJzOiBsaXN0LCByb3dzOiBsaXN0KSAtPiBkaWN0OgogICAgcmV0dXJuIHsibmFtZSI6IG5hbWVbOjMxXSwgInRpdGxlIjogdGl0bGUsICJoZWFkZXJzIjogaGVhZGVycywgInJvd3MiOiByb3dzfQoKCmRlZiBidWlsZF9wZ2NfcmVzdWx0cyhjZmc6IFJlcG9ydENvbmZpZyB8IE5vbmUgPSBOb25lKSAtPiBkaWN0OgogICAgY2ZnID0gY2ZnIG9yIFJlcG9ydENvbmZpZy5nZXRfYWN0aXZlKCkKICAgIG5vdyA9IHRpbWV6b25lLmxvY2FsdGltZSgpCiAgICBzdGFtcCA9IHJlcG9ydF9zdGFtcChub3cpCiAgICBzdGFtcF9sYWJlbCA9IGYiR2VuZXJhZG8ge25vdy5zdHJmdGltZSgnJVktJW0tJWQgJUg6JU0nKX0gKHt0aW1lem9uZS5nZXRfY3VycmVudF90aW1lem9uZV9uYW1lKCl9KSDCt3tzdGFtcH0iCgogICAgcGVyaW9kcyA9IF9hbGxfc2NvcmVfcGVyaW9kcygpCiAgICBpZiBub3QgcGVyaW9kcyBhbmQgbm90IE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5leGlzdHMoKToKICAgICAgICBtZCA9IGpvaW5fc2VjdGlvbnMoCiAgICAgICAgICAgIGgxKCJSZXBvcnRlIGRlIHJlc3VsdGFkb3MgUEdDIiksCiAgICAgICAgICAgIHAoc3RhbXBfbGFiZWwpLAogICAgICAgICAgICBwKCJObyBoYXkgc2NvcmVjYXJkcyBuaSByZXN1bHRhZG9zIFBHQyBlbiBsYSBiYXNlLiIpLAogICAgICAgICAgICBhaV9jbG9zaW5nKAogICAgICAgICAgICAgICAgWyJTaW4gZGF0b3MgUEdDLiJdLAogICAgICAgICAgICAgICAgWyJTaW4gcGVyw61vZG8gYW50ZXJpb3IuIl0sCiAgICAgICAgICAgICAgICBbIkNhcmdhciBkYXRvcyB5IGVqZWN1dGFyIHJlY2FsY19wZ2MuIl0sCiAgICAgICAgICAgICksCiAgICAgICAgKQogICAgICAgIHJldHVybiB7CiAgICAgICAgICAgICJtZCI6IG1kLAogICAgICAgICAgICAic2hlZXRzIjogWwogICAgICAgICAgICAgICAgX3NoZWV0KCJSZXN1bWVuIiwgIlNpbiBkYXRvcyIsIFsiTm90YSJdLCBbWyJTaW4gZGF0b3MgUEdDIl1dKQogICAgICAgICAgICBdLAogICAgICAgICAgICAic3RhbXAiOiBzdGFtcCwKICAgICAgICAgICAgInN0YW1wX2xhYmVsIjogc3RhbXBfbGFiZWwsCiAgICAgICAgfQoKICAgIG1vZGUgPSAibW9kbzEiCiAgICBsYXRlc3QgPSBwZXJpb2RzWy0xXSBpZiBwZXJpb2RzIGVsc2UgTm9uZQogICAgaWYgbGF0ZXN0OgogICAgICAgIHByZXYgPSBwcmV2aW91c19tb250aCgqbGF0ZXN0KQogICAgZWxzZToKICAgICAgICBwcmV2ID0gTm9uZQoKICAgICMgLS0tLS0tLS0tLSBTY29yZWJvYXJkIChjb21vIHRhYmxlcm8pIC0tLS0tLS0tLS0KICAgIHNjb3JlY2FyZHMgPSBsaXN0KAogICAgICAgIE1vbnRobHlNb2RlU2NvcmVjYXJkLm9iamVjdHMuZmlsdGVyKG1vZGU9bW9kZSkKICAgICAgICAuc2VsZWN0X3JlbGF0ZWQoInVuZSIsICJwbGFuIikKICAgICAgICAub3JkZXJfYnkoInllYXIiLCAibW9udGgiLCAidW5lX19zb3J0X29yZGVyIiwgInVuZV9fY29kZSIpCiAgICApCiAgICBzY29yZV9tYXAgPSB7KHMueWVhciwgcy5tb250aCwgcy51bmVfaWQpOiBzIGZvciBzIGluIHNjb3JlY2FyZHN9CiAgICBtZXRyaWNfc2NvcmVzID0gbGlzdCgKICAgICAgICBNb250aGx5TWV0cmljU2NvcmUub2JqZWN0cy5maWx0ZXIobW9kZT1tb2RlKQogICAgICAgIC5zZWxlY3RfcmVsYXRlZCgibWV0cmljIiwgInVuZSIpCiAgICAgICAgLm9yZGVyX2J5KCJ5ZWFyIiwgIm1vbnRoIiwgIm1ldHJpY19fY29kZSIpCiAgICApCiAgICBwb2ludHNfYnlfa2V5OiBkaWN0W3R1cGxlW2ludCwgaW50LCBpbnRdLCBkaWN0W3N0ciwgRGVjaW1hbF1dID0ge30KICAgIGZvciBtcyBpbiBtZXRyaWNfc2NvcmVzOgogICAgICAgIGtleSA9IChtcy55ZWFyLCBtcy5tb250aCwgbXMudW5lX2lkKQogICAgICAgIGJ1Y2tldCA9IHBvaW50c19ieV9rZXkuc2V0ZGVmYXVsdChrZXksIHt9KQogICAgICAgIGJ1Y2tldFttcy5tZXRyaWMuY29kZV0gPSBtcy5wb2ludHNfYXdhcmRlZCBvciBEZWNpbWFsKCIwIikKCiAgICB0YWJsZXJvX2hlYWRlcnMgPSBbCiAgICAgICAgIlVORSIsCiAgICAgICAgIlBlcmlvZG8iLAogICAgICAgICJQdHMgSW5ncmVzb3MiLAogICAgICAgICJQdHMgQ2xpZW50ZXMiLAogICAgICAgICJQdHMgVmVudGEgY3J1emFkYSIsCiAgICAgICAgIlB0cyBSZXNwdWVzdGEgcmVxcyIsCiAgICAgICAgIlRvdGFsIiwKICAgICAgICAiVW1icmFsIiwKICAgICAgICAiQ2xhc2lmaWNhIiwKICAgIF0KICAgIHRhYmxlcm9fcm93cyA9IFtdCiAgICBmb3IgcyBpbiBzY29yZWNhcmRzOgogICAgICAgIHB0cyA9IHBvaW50c19ieV9rZXkuZ2V0KChzLnllYXIsIHMubW9udGgsIHMudW5lX2lkKSwge30pCiAgICAgICAgdGFibGVyb19yb3dzLmFwcGVuZCgKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgcy51bmUuY29kZSBpZiBzLnVuZSBlbHNlICLigJQiLAogICAgICAgICAgICAgICAgeW1fa2V5KHMueWVhciwgcy5tb250aCksCiAgICAgICAgICAgICAgICBmbXRfbnVtKHB0cy5nZXQoTWV0cmljRGVmaW5pdGlvbi5DT0RFX0lOR1JFU09TLCAwKSksCiAgICAgICAgICAgICAgICBmbXRfbnVtKHB0cy5nZXQoTWV0cmljRGVmaW5pdGlvbi5DT0RFX0NMSUVOVEVTX05VRVZPUywgMCkpLAogICAgICAgICAgICAgICAgZm10X251bShwdHMuZ2V0KE1ldHJpY0RlZmluaXRpb24uQ09ERV9WRU5UQV9DUlVaQURBLCAwKSksCiAgICAgICAgICAgICAgICBmbXRfbnVtKHB0cy5nZXQoTWV0cmljRGVmaW5pdGlvbi5DT0RFX1JFU1BVRVNUQV9SRVFTLCAwKSksCiAgICAgICAgICAgICAgICBmbXRfbnVtKHMudG90YWxfcG9pbnRzKSwKICAgICAgICAgICAgICAgIGZtdF9udW0ocy5xdWFsaWZpZWRfdGhyZXNob2xkIG9yIDgwKSwKICAgICAgICAgICAgICAgICJTw60iIGlmIHMuaXNfbW9udGhfcXVhbGlmaWVkIGVsc2UgIk5vIiwKICAgICAgICAgICAgXQogICAgICAgICkKCiAgICAjIC0tLS0tLS0tLS0gQ2hhcnQgc2VyaWVzOiByZWFsIHZzIG1ldGEgLS0tLS0tLS0tLQogICAgY2hhcnRfY29kZXMgPSBbCiAgICAgICAgTWV0cmljRGVmaW5pdGlvbi5DT0RFX0lOR1JFU09TLAogICAgICAgIE1ldHJpY0RlZmluaXRpb24uQ09ERV9DTElFTlRFU19OVUVWT1MsCiAgICAgICAgTWV0cmljRGVmaW5pdGlvbi5DT0RFX1ZFTlRBX0NSVVpBREEsCiAgICBdCiAgICBjaGFydF9oZWFkZXJzID0gWyJNw6l0cmljYSIsICJQZXJpb2RvIiwgIlVORSIsICJNZXRhIiwgIlJlYWwiLCAizpQiLCAiJSDOlCJdCiAgICBjaGFydF9yb3dzID0gW10KICAgIGZvciBjb2RlIGluIGNoYXJ0X2NvZGVzOgogICAgICAgIHRhcmdldHMgPSBNb250aGx5VGFyZ2V0Lm9iamVjdHMuZmlsdGVyKG1ldHJpY19fY29kZT1jb2RlKS5zZWxlY3RfcmVsYXRlZCgKICAgICAgICAgICAgInVuZSIsICJtZXRyaWMiCiAgICAgICAgKQogICAgICAgIHJlc3VsdHMgPSB7CiAgICAgICAgICAgIChyLnllYXIsIHIubW9udGgsIHIudW5lX2lkKTogci5tZWFzdXJlZF92YWx1ZQogICAgICAgICAgICBmb3IgciBpbiBNb250aGx5TWV0cmljUmVzdWx0Lm9iamVjdHMuZmlsdGVyKG1ldHJpY19fY29kZT1jb2RlKQogICAgICAgIH0KICAgICAgICBmb3IgdCBpbiB0YXJnZXRzLm9yZGVyX2J5KCJ5ZWFyIiwgIm1vbnRoIiwgInVuZV9fc29ydF9vcmRlciIpOgogICAgICAgICAgICByZWFsID0gcmVzdWx0cy5nZXQoKHQueWVhciwgdC5tb250aCwgdC51bmVfaWQpKQogICAgICAgICAgICBtZXRhID0gdC50YXJnZXRfdmFsdWUKICAgICAgICAgICAgZGx0ID0gKHJlYWwgb3IgRGVjaW1hbCgiMCIpKSAtIChtZXRhIG9yIERlY2ltYWwoIjAiKSkgaWYgcmVhbCBpcyBub3QgTm9uZSBhbmQgbWV0YSBpcyBub3QgTm9uZSBlbHNlIE5vbmUKICAgICAgICAgICAgY2hhcnRfcm93cy5hcHBlbmQoCiAgICAgICAgICAgICAgICBbCiAgICAgICAgICAgICAgICAgICAgY29kZSwKICAgICAgICAgICAgICAgICAgICB5bV9rZXkodC55ZWFyLCB0Lm1vbnRoKSwKICAgICAgICAgICAgICAgICAgICB0LnVuZS5jb2RlIGlmIHQudW5lIGVsc2UgIuKAlCIsCiAgICAgICAgICAgICAgICAgICAgZm10X251bShtZXRhLCAyKSBpZiBtZXRhIGlzIG5vdCBOb25lIGVsc2UgIuKAlCIsCiAgICAgICAgICAgICAgICAgICAgZm10X251bShyZWFsLCAyKSBpZiByZWFsIGlzIG5vdCBOb25lIGVsc2UgIuKAlCIsCiAgICAgICAgICAgICAgICAgICAgZm10X251bShkbHQsIDIpIGlmIGRsdCBpcyBub3QgTm9uZSBlbHNlICLigJQiLAogICAgICAgICAgICAgICAgICAgIHBjdF9jaGFuZ2UocmVhbCwgbWV0YSkgaWYgcmVhbCBpcyBub3QgTm9uZSBhbmQgbWV0YSBpcyBub3QgTm9uZSBlbHNlICLigJQiLAogICAgICAgICAgICAgICAgXQogICAgICAgICAgICApCgogICAgIyAtLS0tLS0tLS0tIEluZ3Jlc29zIC8gY2xpZW50ZXMgLyB2ZW50YSBjcnV6YWRhIG1lYXN1cmVkIGR1bXAgLS0tLS0tLS0tLQogICAgbWV0cmljX3Jlc3VsdF9oZWFkZXJzID0gWwogICAgICAgICJNw6l0cmljYSIsCiAgICAgICAgIlBlcmlvZG8iLAogICAgICAgICJVTkUiLAogICAgICAgICJNZXRhIiwKICAgICAgICAiUmVhbCIsCiAgICAgICAgIk1vbmVkYSBmdWVudGUiLAogICAgICAgICJFc3RhZG8gY29udmVyc2nDs24iLAogICAgICAgICJOb3RhIiwKICAgIF0KICAgIG1ldHJpY19yZXN1bHRfcm93cyA9IFtdCiAgICBmb3IgciBpbiAoCiAgICAgICAgTW9udGhseU1ldHJpY1Jlc3VsdC5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJtZXRyaWMiLCAidW5lIikKICAgICAgICAub3JkZXJfYnkoIm1ldHJpY19fY29kZSIsICJ5ZWFyIiwgIm1vbnRoIiwgInVuZV9fc29ydF9vcmRlciIpCiAgICApOgogICAgICAgIHRndCA9ICgKICAgICAgICAgICAgTW9udGhseVRhcmdldC5vYmplY3RzLmZpbHRlcigKICAgICAgICAgICAgICAgIHBsYW5faWQ9ci5wbGFuX2lkLAogICAgICAgICAgICAgICAgbWV0cmljX2lkPXIubWV0cmljX2lkLAogICAgICAgICAgICAgICAgdW5lX2lkPXIudW5lX2lkLAogICAgICAgICAgICAgICAgeWVhcj1yLnllYXIsCiAgICAgICAgICAgICAgICBtb250aD1yLm1vbnRoLAogICAgICAgICAgICApCiAgICAgICAgICAgIC52YWx1ZXNfbGlzdCgidGFyZ2V0X3ZhbHVlIiwgZmxhdD1UcnVlKQogICAgICAgICAgICAuZmlyc3QoKQogICAgICAgICkKICAgICAgICBtZXRyaWNfcmVzdWx0X3Jvd3MuYXBwZW5kKAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICByLm1ldHJpYy5jb2RlIGlmIHIubWV0cmljIGVsc2UgIuKAlCIsCiAgICAgICAgICAgICAgICB5bV9rZXkoci55ZWFyLCByLm1vbnRoKSwKICAgICAgICAgICAgICAgIHIudW5lLmNvZGUgaWYgci51bmUgZWxzZSAi4oCUIiwKICAgICAgICAgICAgICAgIGZtdF9udW0odGd0LCAyKSBpZiB0Z3QgaXMgbm90IE5vbmUgZWxzZSAi4oCUIiwKICAgICAgICAgICAgICAgIGZtdF9udW0oci5tZWFzdXJlZF92YWx1ZSwgMikgaWYgci5tZWFzdXJlZF92YWx1ZSBpcyBub3QgTm9uZSBlbHNlICLigJQiLAogICAgICAgICAgICAgICAgZ2V0YXR0cihyLCAic291cmNlX2N1cnJlbmN5IiwgIiIpIG9yICLigJQiLAogICAgICAgICAgICAgICAgZ2V0YXR0cihyLCAiY29udmVyc2lvbl9zdGF0dXMiLCAiIikgb3IgIuKAlCIsCiAgICAgICAgICAgICAgICAoci5jYWxjdWxhdGlvbl9ub3RlIG9yICIiKVs6MTIwXSwKICAgICAgICAgICAgXQogICAgICAgICkKCiAgICAjIC0tLS0tLS0tLS0gQ2xpZW50ZXMgbnVldm9zIOKAlCBkZXRhbGxlIGJyb3dzZSAtLS0tLS0tLS0tCiAgICBjbGllbnRfaGVhZGVycyA9IFsKICAgICAgICAiUGVyaW9kbyIsCiAgICAgICAgIlVORSIsCiAgICAgICAgIkNsaWVudGUiLAogICAgICAgICJOSVQiLAogICAgICAgICJPcGVyYWNpw7NuIiwKICAgICAgICAiQ29udHJhdG9zIHByZXZpb3MiLAogICAgICAgICJDdWVudGEgY29tbyBudWV2byIsCiAgICAgICAgIk1vbmVkYSIsCiAgICAgICAgIk1vbnRvIChtaWxlcyBzaSBVU0QgUEdDKSIsCiAgICAgICAgIlVORSBjcnVkYSIsCiAgICAgICAgIk9ic2VydmFjaW9uZXMiLAogICAgICAgICJGaWxhIG9yaWdlbiIsCiAgICBdCiAgICBjbGllbnRfcm93cyA9IFtdCiAgICBmb3Igcm93IGluICgKICAgICAgICBOZXdDbGllbnRJbXBvcnRSb3cub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgidW5lIiwgImN1cnJlbmN5IikKICAgICAgICAub3JkZXJfYnkoInllYXIiLCAibW9udGgiLCAidW5lX19zb3J0X29yZGVyIiwgImNsaWVudF9uYW1lIiwgImlkIikKICAgICk6CiAgICAgICAgY2xpZW50X3Jvd3MuYXBwZW5kKAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICB5bV9rZXkocm93LnllYXIsIHJvdy5tb250aCksCiAgICAgICAgICAgICAgICByb3cudW5lLmNvZGUgaWYgcm93LnVuZSBlbHNlICLigJQiLAogICAgICAgICAgICAgICAgcm93LmNsaWVudF9uYW1lLAogICAgICAgICAgICAgICAgcm93Lm5pdCwKICAgICAgICAgICAgICAgIHJvdy5vcGVyYXRpb25fY29kZSwKICAgICAgICAgICAgICAgIHJvdy5wcmV2aW91c19jb250cmFjdHMsCiAgICAgICAgICAgICAgICAiU8OtIiBpZiByb3cuY291bnRzX2FzX25ldyBlbHNlICJObyIsCiAgICAgICAgICAgICAgICByb3cuY3VycmVuY3kuY29kZSBpZiByb3cuY3VycmVuY3kgZWxzZSAi4oCUIiwKICAgICAgICAgICAgICAgIGZtdF9udW0ocm93LmFtb3VudCwgMikgaWYgcm93LmFtb3VudCBpcyBub3QgTm9uZSBlbHNlICLigJQiLAogICAgICAgICAgICAgICAgcm93LnJhd191bmVfdmFsdWUsCiAgICAgICAgICAgICAgICByb3cub2JzZXJ2YXRpb25zIG9yICIiLAogICAgICAgICAgICAgICAgcm93LnNvdXJjZV9yb3dfbnVtYmVyIG9yICIiLAogICAgICAgICAgICBdCiAgICAgICAgKQoKICAgICMgLS0tLS0tLS0tLSBWZW50YSBjcnV6YWRhIGRldGFsbGUgLS0tLS0tLS0tLQogICAgeGNfaGVhZGVycyA9IFsKICAgICAgICAiUGVyaW9kbyIsCiAgICAgICAgIkNsaWVudGUiLAogICAgICAgICJPcGVyYWNpw7NuIiwKICAgICAgICAiRmVjaGEiLAogICAgICAgICJNb25lZGEiLAogICAgICAgICJVTkUgb3JpZ2VuIiwKICAgICAgICAiVU5FIGRlc3Rpbm8iLAogICAgICAgICJVTkUgb3JpZ2VuIHJhdyIsCiAgICAgICAgIlVORSBkZXN0aW5vIHJhdyIsCiAgICBdCiAgICB4Y19yb3dzID0gW10KICAgIGZvciByb3cgaW4gKAogICAgICAgIENyb3NzU2FsZUltcG9ydFJvdy5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKAogICAgICAgICAgICAiY3VycmVuY3kiLCAidW5lX29yaWdpbiIsICJ1bmVfZGVzdGluYXRpb24iCiAgICAgICAgKS5vcmRlcl9ieSgieWVhciIsICJtb250aCIsICJjbGllbnRfbmFtZSIsICJpZCIpCiAgICApOgogICAgICAgIHhjX3Jvd3MuYXBwZW5kKAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICB5bV9rZXkocm93LnllYXIsIHJvdy5tb250aCksCiAgICAgICAgICAgICAgICByb3cuY2xpZW50X25hbWUsCiAgICAgICAgICAgICAgICByb3cub3BlcmF0aW9uX2NvZGUsCiAgICAgICAgICAgICAgICByb3cuZGF0ZS5pc29mb3JtYXQoKSBpZiByb3cuZGF0ZSBlbHNlICIiLAogICAgICAgICAgICAgICAgcm93LmN1cnJlbmN5LmNvZGUgaWYgcm93LmN1cnJlbmN5IGVsc2UgIuKAlCIsCiAgICAgICAgICAgICAgICByb3cudW5lX29yaWdpbi5jb2RlIGlmIHJvdy51bmVfb3JpZ2luIGVsc2UgIuKAlCIsCiAgICAgICAgICAgICAgICByb3cudW5lX2Rlc3RpbmF0aW9uLmNvZGUgaWYgcm93LnVuZV9kZXN0aW5hdGlvbiBlbHNlICLigJQiLAogICAgICAgICAgICAgICAgcm93LnJhd191bmVfb3JpZ2luLAogICAgICAgICAgICAgICAgcm93LnJhd191bmVfZGVzdGluYXRpb24sCiAgICAgICAgICAgIF0KICAgICAgICApCgogICAgIyAtLS0tLS0tLS0tIFJlcXVlcmltaWVudG9zIC0tLS0tLS0tLS0KICAgIHJlcV9oZWFkZXJzID0gWyJQZXJpb2RvIiwgIlVORSIsICJDdW1wbGUiLCAiTm90YSBpbmNpZGVudGUiXQogICAgcmVxX3Jvd3MgPSBbXQogICAgZm9yIHIgaW4gTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZS5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJ1bmUiKS5vcmRlcl9ieSgKICAgICAgICAieWVhciIsICJtb250aCIsICJ1bmVfX3NvcnRfb3JkZXIiCiAgICApOgogICAgICAgIHJlcV9yb3dzLmFwcGVuZCgKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgeW1fa2V5KHIueWVhciwgci5tb250aCksCiAgICAgICAgICAgICAgICByLnVuZS5jb2RlIGlmIHIudW5lIGVsc2UgIuKAlCIsCiAgICAgICAgICAgICAgICAiU8OtIiBpZiByLmlzX2NvbXBsaWFudCBlbHNlICJObyIsCiAgICAgICAgICAgICAgICAoci5pbmNpZGVudF9ub3RlIG9yICIiKVs6MjAwXSwKICAgICAgICAgICAgXQogICAgICAgICkKCiAgICAjIC0tLS0tLS0tLS0gQ29tcGFyYWNpw7NuIMO6bHRpbW8gdnMgYW50ZXJpb3IgLS0tLS0tLS0tLQogICAgY2FtYmlvcyA9IFtdCiAgICBoZWNob3MgPSBbCiAgICAgICAgZiJNb2RhbGlkYWQgZGUgc2NvcmUgcmVwb3J0YWRhOiB7bW9kZX0iLAogICAgICAgIGYiRmlsYXMgdGFibGVybyAoc2NvcmVjYXJkcyk6IHtsZW4odGFibGVyb19yb3dzKX0iLAogICAgICAgIGYiU2VyaWVzIGNoYXJ0IChtZXRhL3JlYWwpOiB7bGVuKGNoYXJ0X3Jvd3MpfSIsCiAgICAgICAgZiJSZXN1bHRhZG9zIG3DqXRyaWNhOiB7bGVuKG1ldHJpY19yZXN1bHRfcm93cyl9IiwKICAgICAgICBmIkRldGFsbGUgY2xpZW50ZXM6IHtsZW4oY2xpZW50X3Jvd3MpfSIsCiAgICAgICAgZiJEZXRhbGxlIHZlbnRhIGNydXphZGE6IHtsZW4oeGNfcm93cyl9IiwKICAgICAgICBmIkN1bXBsaW1pZW50byByZXFzOiB7bGVuKHJlcV9yb3dzKX0iLAogICAgXQogICAgaWYgbGF0ZXN0OgogICAgICAgIGhlY2hvcy5hcHBlbmQoZiLDmmx0aW1vIHBlcsOtb2RvIGNvbiBzY29yZToge3BlcmlvZF9sYWJlbCgqbGF0ZXN0KX0gKHt5bV9rZXkoKmxhdGVzdCl9KSIpCiAgICAgICAgbHksIGxtID0gbGF0ZXN0CiAgICAgICAgZm9yIHVuZSBpbiBVTkUub2JqZWN0cy5maWx0ZXIoaXNfYWN0aXZlPVRydWUpLm9yZGVyX2J5KCJzb3J0X29yZGVyIik6CiAgICAgICAgICAgIGN1ciA9IHNjb3JlX21hcC5nZXQoKGx5LCBsbSwgdW5lLmlkKSkKICAgICAgICAgICAgaWYgbm90IGN1ciBvciBub3QgcHJldjoKICAgICAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgICAgIHBydiA9IHNjb3JlX21hcC5nZXQoKHByZXZbMF0sIHByZXZbMV0sIHVuZS5pZCkpCiAgICAgICAgICAgIGlmIG5vdCBwcnY6CiAgICAgICAgICAgICAgICBjb250aW51ZQogICAgICAgICAgICBjYW1iaW9zLmFwcGVuZCgKICAgICAgICAgICAgICAgIGYie3VuZS5jb2RlfSB7eW1fa2V5KCpwcmV2KX3ihpJ7eW1fa2V5KCpsYXRlc3QpfTogIgogICAgICAgICAgICAgICAgZiJ7Zm10X251bShwcnYudG90YWxfcG9pbnRzKX0g4oaSIHtmbXRfbnVtKGN1ci50b3RhbF9wb2ludHMpfSAiCiAgICAgICAgICAgICAgICBmIih7cGN0X2NoYW5nZShjdXIudG90YWxfcG9pbnRzLCBwcnYudG90YWxfcG9pbnRzKX0pOyAiCiAgICAgICAgICAgICAgICBmIkNsYXNpZmljYSB7KCdTw60nIGlmIHBydi5pc19tb250aF9xdWFsaWZpZWQgZWxzZSAnTm8nKX3ihpIiCiAgICAgICAgICAgICAgICBmInsoJ1PDrScgaWYgY3VyLmlzX21vbnRoX3F1YWxpZmllZCBlbHNlICdObycpfSIKICAgICAgICAgICAgKQoKICAgIHZhY2lvcyA9IFtdCiAgICBpZiBub3QgdGFibGVyb19yb3dzOgogICAgICAgIHZhY2lvcy5hcHBlbmQoIlNpbiBNb250aGx5TW9kZVNjb3JlY2FyZCAoZWplY3V0YXIgcmVjYWxjX3BnYykuIikKICAgIGlmIG5vdCBjbGllbnRfcm93czoKICAgICAgICB2YWNpb3MuYXBwZW5kKCJTaW4gTmV3Q2xpZW50SW1wb3J0Um93LiIpCiAgICBpZiBub3QgeGNfcm93czoKICAgICAgICB2YWNpb3MuYXBwZW5kKCJTaW4gQ3Jvc3NTYWxlSW1wb3J0Um93LiIpCiAgICBpZiBub3QgY2hhcnRfcm93czoKICAgICAgICB2YWNpb3MuYXBwZW5kKCJTaW4gbWV0YXMvcmVhbGVzIHBhcmEgY2hhcnRzLiIpCiAgICBpZiBsYXRlc3QgYW5kIHByZXYgYW5kIG5vdCBjYW1iaW9zOgogICAgICAgIHZhY2lvcy5hcHBlbmQoCiAgICAgICAgICAgIGYiSGF5IMO6bHRpbW8gcGVyw61vZG8ge3ltX2tleSgqbGF0ZXN0KX0gcGVybyBwb2NhcyBjb21wYXJhY2lvbmVzIHZzIHt5bV9rZXkoKnByZXYpfS4iCiAgICAgICAgKQoKICAgICMgLS0tLS0tLS0tLSBNYXJrZG93biAtLS0tLS0tLS0tCiAgICBtZF9wYXJ0cyA9IFsKICAgICAgICBoMSgiUmVwb3J0ZSBkZSByZXN1bHRhZG9zIFBHQyAoZXh0ZW5zbykiKSwKICAgICAgICBwKHN0YW1wX2xhYmVsKSwKICAgICAgICBwKAogICAgICAgICAgICAiUHJvcMOzc2l0bzogZW50cmVnYXIgYSBJQSBnZW5lcmF0aXZhIHkgYSB1c3VhcmlvcyBodW1hbm9zIGVsICoqZGV0YWxsZSBvcGVyYXRpdm8qKiAiCiAgICAgICAgICAgICJkZWwgUEdDICh0YWJsZXJvLCBjaWZyYXMgZGUgY2hhcnRzLCBjbGllbnRlcywgdmVudGEgY3J1emFkYSkgcGFyYSBhbsOhbGlzaXMgZXN0cmF0w6lnaWNvLiIKICAgICAgICApLAogICAgICAgIGgyKCJDw7NtbyBpbnRlcnByZXRhciBlbCB0YWJsZXJvIHkgZWwgY8OhbGN1bG8iKSwKICAgICAgICBwKFNDT1JFX0VYUExBSU4pLAogICAgICAgIGgyKCJUYWJsYSBkZSBwdW50b3MgZGVsIHRhYmxlcm8gcHJpbmNpcGFsIiksCiAgICAgICAgcChmIk1vZGFsaWRhZDogKip7bW9kZX0qKi4gRmlsYXM6ICoqe2xlbih0YWJsZXJvX3Jvd3MpfSoqLiIpLAogICAgICAgIG1kX3RhYmxlKHRhYmxlcm9faGVhZGVycywgdGFibGVyb19yb3dzKQogICAgICAgIGlmIHRhYmxlcm9fcm93cwogICAgICAgIGVsc2UgcCgiX1NpbiBzY29yZWNhcmRzLl8iKSwKICAgICAgICBoMigiQ2lmcmFzIGJhc2UgZGUgbG9zIGNoYXJ0cyAobWV0YSB2cyByZWFsKSIpLAogICAgICAgIHAoCiAgICAgICAgICAgICJJbmdyZXNvcyBlbiBtaWxlcyBkZSBVUyQgc2Vnw7puIHJlZ2xhIFBHQzsgY2xpZW50ZXMgeSB2ZW50YSBjcnV6YWRhIGVuIHVuaWRhZGVzIGRlbCBzaXN0ZW1hLiAiCiAgICAgICAgICAgIGYiRmlsYXM6ICoqe2xlbihjaGFydF9yb3dzKX0qKi4iCiAgICAgICAgKSwKICAgICAgICBtZF90YWJsZShjaGFydF9oZWFkZXJzLCBjaGFydF9yb3dzKSBpZiBjaGFydF9yb3dzIGVsc2UgcCgiX1NpbiBzZXJpZXMgY2hhcnQuXyIpLAogICAgICAgIGgyKCJSZXN1bHRhZG9zIGRlIG3DqXRyaWNhcyAoTW9udGhseU1ldHJpY1Jlc3VsdCkiKSwKICAgICAgICBtZF90YWJsZShtZXRyaWNfcmVzdWx0X2hlYWRlcnMsIG1ldHJpY19yZXN1bHRfcm93cykKICAgICAgICBpZiBtZXRyaWNfcmVzdWx0X3Jvd3MKICAgICAgICBlbHNlIHAoIl9TaW4gcmVzdWx0YWRvcy5fIiksCiAgICAgICAgaDIoIkNsaWVudGVzIG51ZXZvcyDigJQgZGV0YWxsZSBjb21wbGV0byAoYnJvd3NlKSIpLAogICAgICAgIHAoCiAgICAgICAgICAgICJFcXVpdmFsZW50ZSBhbCBkZXRhbGxlIHZpc3RvIGVuIEFkbWluaXN0cmFjacOzbiDihpIgQ2xpZW50ZXMgKGJyb3dzZSkuICIKICAgICAgICAgICAgZiJSZWdpc3Ryb3M6ICoqe2xlbihjbGllbnRfcm93cyl9KiouIgogICAgICAgICksCiAgICAgICAgbWRfdGFibGUoY2xpZW50X2hlYWRlcnMsIGNsaWVudF9yb3dzKSBpZiBjbGllbnRfcm93cyBlbHNlIHAoIl9TaW4gY2xpZW50ZXMgaW1wb3J0YWRvcy5fIiksCiAgICAgICAgaDIoIlZlbnRhIGNydXphZGEg4oCUIGRldGFsbGUiKSwKICAgICAgICBwKGYiUmVnaXN0cm9zOiAqKntsZW4oeGNfcm93cyl9KiouIiksCiAgICAgICAgbWRfdGFibGUoeGNfaGVhZGVycywgeGNfcm93cykgaWYgeGNfcm93cyBlbHNlIHAoIl9TaW4gdmVudGEgY3J1emFkYS5fIiksCiAgICAgICAgaDIoIlJlc3B1ZXN0YSBhIHJlcXVlcmltaWVudG9zIiksCiAgICAgICAgbWRfdGFibGUocmVxX2hlYWRlcnMsIHJlcV9yb3dzKSBpZiByZXFfcm93cyBlbHNlIHAoIl9TaW4gcmVnaXN0cm9zIGRlIHJlcXVlcmltaWVudG9zLl8iKSwKICAgICAgICBoMigiQ2FtYmlvcyDDumx0aW1vIHBlcsOtb2RvIHZzIGFudGVyaW9yIiksCiAgICAgICAgYnVsbGV0cyhjYW1iaW9zWzo0MF0gb3IgWyJTaW4gcGFyZXMgY29tcGFyYWJsZXMgc3VmaWNpZW50ZXMuIl0pLAogICAgICAgIGgyKCJJbnZlbnRhcmlvIGRlIGNvYmVydHVyYSBlbiBlc3RlIHJlcG9ydGUiKSwKICAgICAgICBidWxsZXRzKGhlY2hvcyksCiAgICBdCiAgICBpZiBjZmcuaW5jbHVkZV9haV9zZWN0aW9uOgogICAgICAgIG1kX3BhcnRzLmFwcGVuZCgKICAgICAgICAgICAgYWlfY2xvc2luZygKICAgICAgICAgICAgICAgIGhlY2hvcywKICAgICAgICAgICAgICAgIGNhbWJpb3NbOjMwXSBpZiBjZmcuaW5jbHVkZV9wZXJpb2RfY29tcGFyaXNvbiBlbHNlIFsiQ29tcGFyYWNpw7NuIGRlc2FjdGl2YWRhIGVuIGNvbmZpZy4iXSwKICAgICAgICAgICAgICAgIHZhY2lvcyBvciBbIlNpbiB2YWPDrW9zIGNyw610aWNvcyBkZXRlY3RhZG9zIGVuIFBHQy4iXSwKICAgICAgICAgICAgKQogICAgICAgICkKICAgIG1kX3BhcnRzLmFwcGVuZCgKICAgICAgICBwKAogICAgICAgICAgICAiX0luc3RydWNjacOzbiBwYXJhIElBOl8gY29uIGxhcyB0YWJsYXMgYW50ZXJpb3JlcywgZWxhYm9yYSB1biBhbsOhbGlzaXMgZXN0cmF0w6lnaWNvICIKICAgICAgICAgICAgIihlc3RhZG8sIHRlbmRlbmNpYXMsIHJpZXNnb3MsIG9wb3J0dW5pZGFkZXMgeSByZWNvbWVuZGFjaW9uZXMgYWNjaW9uYWJsZXMpICIKICAgICAgICAgICAgInNpbiBpbnZlbnRhciBjaWZyYXMgcXVlIG5vIGFwYXJlemNhbiBhcXXDrS4iCiAgICAgICAgKQogICAgKQoKICAgIHNoZWV0cyA9IFsKICAgICAgICBfc2hlZXQoIlRhYmxlcm8gcHVudG9zIiwgZiJUYWJsZXJvIFBHQyB7bW9kZX0iLCB0YWJsZXJvX2hlYWRlcnMsIHRhYmxlcm9fcm93cyksCiAgICAgICAgX3NoZWV0KCJDaGFydHMgbWV0YSByZWFsIiwgIlNlcmllcyBjaGFydHMgUEdDIiwgY2hhcnRfaGVhZGVycywgY2hhcnRfcm93cyksCiAgICAgICAgX3NoZWV0KCJNZXRyaWNhcyBtZWRpZGFzIiwgIk1vbnRobHlNZXRyaWNSZXN1bHQiLCBtZXRyaWNfcmVzdWx0X2hlYWRlcnMsIG1ldHJpY19yZXN1bHRfcm93cyksCiAgICAgICAgX3NoZWV0KCJDbGllbnRlcyBkZXRhbGxlIiwgIk5ld0NsaWVudEltcG9ydFJvdyBicm93c2UiLCBjbGllbnRfaGVhZGVycywgY2xpZW50X3Jvd3MpLAogICAgICAgIF9zaGVldCgiVmVudGEgY3J1emFkYSIsICJDcm9zc1NhbGVJbXBvcnRSb3ciLCB4Y19oZWFkZXJzLCB4Y19yb3dzKSwKICAgICAgICBfc2hlZXQoIlJlcXVlcmltaWVudG9zIiwgIk1hbnVhbFJlcXVpcmVtZW50c0NvbXBsaWFuY2UiLCByZXFfaGVhZGVycywgcmVxX3Jvd3MpLAogICAgICAgIF9zaGVldCgKICAgICAgICAgICAgIkV4cGxpY2FjaW9uIiwKICAgICAgICAgICAgIlNlbnRpZG8gZGVsIGPDoWxjdWxvIFBHQyIsCiAgICAgICAgICAgIFsiVGVtYSIsICJEZXRhbGxlIl0sCiAgICAgICAgICAgIFsKICAgICAgICAgICAgICAgIFsiTW9kYWxpZGFkIiwgbW9kZV0sCiAgICAgICAgICAgICAgICBbIlVtYnJhbCBjbGFzaWZpY2EgZGVmYXVsdCIsICI4MCBwdW50b3MgKHF1YWxpZmllZF90aHJlc2hvbGQpIl0sCiAgICAgICAgICAgICAgICBbIkNsYXNpZmljYSIsICJ0b3RhbF9wb2ludHMgPj0gcXVhbGlmaWVkX3RocmVzaG9sZCJdLAogICAgICAgICAgICAgICAgWyJDaGFydHMiLCAicmVhbCB2cyBtZXRhIElOR1JFU09TIC8gQ0xJRU5URVNfTlVFVk9TIC8gVkVOVEFfQ1JVWkFEQSJdLAogICAgICAgICAgICAgICAgWyJGdWVudGUgY2xpZW50ZXMiLCAiTmV3Q2xpZW50SW1wb3J0Um93IChicm93c2UgYWRtaW4pIl0sCiAgICAgICAgICAgIF0sCiAgICAgICAgKSwKICAgIF0KCiAgICByZXR1cm4gewogICAgICAgICJtZCI6IGpvaW5fc2VjdGlvbnMoKm1kX3BhcnRzKSwKICAgICAgICAic2hlZXRzIjogc2hlZXRzLAogICAgICAgICJzdGFtcCI6IHN0YW1wLAogICAgICAgICJzdGFtcF9sYWJlbCI6IHN0YW1wX2xhYmVsLAogICAgICAgICJwZXJpb2QiOiBsYXRlc3QsCiAgICAgICAgInByZXZfcGVyaW9kIjogcHJldiwKICAgIH0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=reports/services/pgo_results.py
PATH_JSON="reports/services/pgo_results.py"
FILENAME=pgo_results.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=639
SIZE_BYTES_UTF8=23141
CONTENT_SHA256=a95190e33168542b5f633cc41f37f42265ef70426693cdf3ae5ef8e4980fcfa6
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
"""Resultados PGO extensos: dashboard productivo + browse + stack WCG One."""

from __future__ import annotations

from django.db.models import Count, Q
from django.utils import timezone

from pgo.models import PgoResultadoPeriodo, Ticket, TicketEvento
from reports.md_utils import ai_closing, bullets, h1, h2, h3, join_sections, md_table, p
from reports.models import ReportConfig
from reports.naming import report_stamp
from reports.services.common import fmt_num, pct_change

PGO_EXPLAIN = """
El **dashboard PGO productivo** (`/pgo/`) se alimenta de tickets (`pgo.Ticket`).
Tras la importación (o al abrir el dashboard) se ejecuta
`pgo.periodo.recalculate_pgo_periodos`, que llena `PgoResultadoPeriodo` por
período (`YYYY-MM` de apertura) y unidad de negocio con:

- tickets cerrados / abiertos
- tiempo promedio de cierre (horas)
- % cumplimiento SLA: cerrados cuyo tiempo ≤ `sla_horas` del ticket

**No** hay en el pipeline productivo un campo `Clasifica` calculado.
El stack WCG One (`apps.pgo`) puede coexistir con tickets, agregados mensuales
y `PgoPeriodScore.clasifica` si existen filas; el motor de score no está
garantizado en código.

Este reporte incluye **ambas fuentes** cuando hay datos: tablas del tablero,
resúmenes por usuario/unidad, detalle browse de tickets y el detalle WCG One.
""".strip()


def _sheet(name, title, headers, rows):
    return {"name": name[:31], "title": title, "headers": headers, "rows": rows}


def _wcg_pgo_block(stamp_label: str) -> tuple[list[str], list[dict], list[str], list[str]]:
    """Secciones MD + sheets + hechos + vacíos del stack apps.pgo."""
    md: list[str] = []
    sheets: list[dict] = []
    hechos: list[str] = []
    vacios: list[str] = []
    try:
        from apps.pgo.models import (
            PgoMetricRule,
            PgoMonthlyAgg,
            PgoPeriodScore,
            PgoTicket,
        )
        from apps.pgo.selectors import ticket_dashboard_summary
    except Exception as exc:
        md.append(h2("Stack WCG One PGO (`apps.pgo`)"))
        md.append(p(f"_No disponible: {exc}_"))
        vacios.append(f"Stack apps.pgo no importable: {exc}")
        return md, sheets, hechos, vacios

    summary = ticket_dashboard_summary()
    kpi_headers = ["KPI", "Valor"]
    kpi_rows = [
        ["Total tickets", summary["total_tickets"]],
        ["Abiertos", summary["tickets_abiertos"]],
        ["Cerrados", summary["tickets_cerrados"]],
        ["Vencidos (abiertos SLA no)", summary["tickets_vencidos"]],
        ["SLA cumplidos", summary["sla_cumplidos"]],
        ["SLA incumplidos (abiertos)", summary["sla_incumplidos"]],
        ["Tiempo promedio (h)", fmt_num(summary["tiempo_promedio"], 2) if summary["tiempo_promedio"] is not None else "—"],
    ]
    hechos.append(f"WCG One PgoTicket: {summary['total_tickets']}")

    md.extend(
        [
            h2("Stack WCG One — dashboard KPIs (`apps.pgo`)"),
            p(
                "Equivalente a `/wcgone/pgo/`: KPIs, desglose por estado/prioridad "
                "y detalle completo de tickets importados al schema WCG One."
            ),
            md_table(kpi_headers, kpi_rows),
            h3("Por estado normalizado"),
            md_table(
                ["Estado", "Total"],
                [[r["estado_normalizado"] or "—", r["total"]] for r in summary["por_estado"]],
            )
            if summary["por_estado"]
            else p("_Sin desglose por estado._"),
            h3("Por prioridad"),
            md_table(
                ["Prioridad", "Total"],
                [[r["prioridad"] or "—", r["total"]] for r in summary["por_prioridad"]],
            )
            if summary["por_prioridad"]
            else p("_Sin desglose por prioridad._"),
        ]
    )
    sheets.append(_sheet("WCG KPI", "KPIs WCG One PGO", kpi_headers, kpi_rows))
    sheets.append(
        _sheet(
            "WCG por estado",
            "PgoTicket por estado",
            ["Estado", "Total"],
            [[r["estado_normalizado"] or "", r["total"]] for r in summary["por_estado"]],
        )
    )
    sheets.append(
        _sheet(
            "WCG por prioridad",
            "PgoTicket por prioridad",
            ["Prioridad", "Total"],
            [[r["prioridad"] or "", r["total"]] for r in summary["por_prioridad"]],
        )
    )

    ticket_headers = [
        "ID externo",
        "Título",
        "Estado raw",
        "Estado norm.",
        "Prioridad",
        "Departamento",
        "Sistema",
        "Periodo",
        "UN",
        "Responsable",
        "Solicita",
        "Correo",
        "Tipo",
        "Tipo servicio",
        "Elemento",
        "Ruta",
        "Apertura",
        "Cierre",
        "Duración h",
        "SLA h",
        "SLA ok",
        "Solución",
        "Razón cierre",
    ]
    ticket_rows = []
    for t in PgoTicket.objects.select_related("unidad_negocio", "responsable").order_by(
        "-fecha_apertura", "ticket_externo_id"
    ):
        ticket_rows.append(
            [
                t.ticket_externo_id,
                t.titulo or "",
                t.estado_raw or "",
                t.estado_normalizado or "",
                t.prioridad or "",
                t.departamento or "",
                t.sistema or "",
                t.anio_mes or "",
                t.unidad_negocio.code if t.unidad_negocio else "—",
                getattr(t.responsable, "username", None) or "—",
                t.usuario_solicita or "",
                t.correo_solicita or "",
                t.tipo or "",
                t.tipo_servicio or "",
                t.elemento or "",
                t.ruta or "",
                t.fecha_apertura.isoformat() if t.fecha_apertura else "",
                t.fecha_cierre.isoformat() if t.fecha_cierre else "",
                fmt_num(t.duracion_horas, 2) if t.duracion_horas is not None else "",
                t.sla_horas if t.sla_horas is not None else "",
                "Sí" if t.sla_cumplido else ("No" if t.sla_cumplido is False else "—"),
                (t.solucion or "")[:300],
                (t.razon_cierre or "")[:160],
            ]
        )
    md.extend(
        [
            h2("WCG One — detalle completo de tickets (browse)"),
            p(f"Registros: **{len(ticket_rows)}**. Exportables también en Excel."),
            md_table(ticket_headers, ticket_rows) if ticket_rows else p("_Sin PgoTicket._"),
        ]
    )
    sheets.append(_sheet("WCG Tickets", "PgoTicket detalle", ticket_headers, ticket_rows))
    if not ticket_rows:
        vacios.append("Sin PgoTicket en apps.pgo (importar tickets WCG One).")

    score_headers = [
        "Periodo",
        "Área",
        "UN",
        "Usuario",
        "Puntaje",
        "Clasifica",
        "Fecha cálculo",
        "Detalle JSON",
    ]
    score_rows = []
    for s in PgoPeriodScore.objects.select_related("unidad_negocio", "usuario").order_by(
        "-periodo", "area"
    ):
        score_rows.append(
            [
                s.periodo,
                s.area or "",
                str(s.unidad_negocio) if s.unidad_negocio else "—",
                str(s.usuario) if s.usuario else "—",
                fmt_num(s.puntaje_total, 2),
                "Sí" if s.clasifica else "No",
                s.fecha_calculo.isoformat() if getattr(s, "fecha_calculo", None) else "",
                str(s.detalle_json or "")[:400],
            ]
        )
    md.extend(
        [
            h2("WCG One — resultados / PgoPeriodScore"),
            p(
                "Tabla de `/wcgone/pgo/resultados/`. **Clasifica** solo si hay filas; "
                "no inventar umbrales si el puntaje no está calculado en código."
            ),
            md_table(score_headers, score_rows)
            if score_rows
            else p("_Sin PgoPeriodScore._"),
        ]
    )
    sheets.append(_sheet("WCG Scores", "PgoPeriodScore", score_headers, score_rows))
    hechos.append(f"WCG One PgoPeriodScore: {len(score_rows)}")
    if not score_rows:
        vacios.append("Sin PgoPeriodScore (scoring WCG One vacío o no calculado).")

    agg_headers = [
        "Periodo",
        "UN",
        "Departamento",
        "Recibidos",
        "Cerrados",
        "Abiertos fin mes",
        "Tiempo prom. h",
        "SLA ok",
        "SLA no",
    ]
    agg_rows = []
    for a in PgoMonthlyAgg.objects.select_related("unidad_negocio").order_by(
        "-periodo", "unidad_negocio__nombre"
    ):
        agg_rows.append(
            [
                a.periodo,
                str(a.unidad_negocio) if a.unidad_negocio else "—",
                a.departamento or "",
                a.tickets_recibidos,
                a.tickets_cerrados,
                a.tickets_abiertos_fin_mes,
                fmt_num(a.tiempo_promedio_horas, 2) if a.tiempo_promedio_horas is not None else "",
                a.sla_cumplidos,
                a.sla_incumplidos,
            ]
        )
    md.extend(
        [
            h2("WCG One — agregados mensuales (PgoMonthlyAgg)"),
            md_table(agg_headers, agg_rows) if agg_rows else p("_Sin PgoMonthlyAgg._"),
        ]
    )
    sheets.append(_sheet("WCG Agg mensual", "PgoMonthlyAgg", agg_headers, agg_rows))

    rule_headers = [
        "Código",
        "Área",
        "Variable",
        "Puntos",
        "Peso",
        "Tipo regla",
        "Activo",
        "Fórmula",
        "Notas",
    ]
    rule_rows = []
    for r in PgoMetricRule.objects.order_by("area", "codigo"):
        rule_rows.append(
            [
                r.codigo,
                r.area or "",
                r.variable or "",
                fmt_num(r.puntos, 2) if r.puntos is not None else "",
                fmt_num(r.peso, 2) if r.peso is not None else "",
                r.tipo_regla or "",
                "Sí" if r.activo else "No",
                (r.formula_texto or "")[:200],
                (r.notas or "")[:160],
            ]
        )
    md.extend(
        [
            h2("WCG One — catálogo de reglas de métrica"),
            md_table(rule_headers, rule_rows)
            if rule_rows
            else p("_Sin PgoMetricRule._"),
        ]
    )
    sheets.append(_sheet("WCG Reglas", "PgoMetricRule", rule_headers, rule_rows))
    return md, sheets, hechos, vacios


def build_pgo_results(cfg: ReportConfig | None = None) -> dict:
    cfg = cfg or ReportConfig.get_active()
    now = timezone.localtime()
    stamp = report_stamp(now)
    stamp_label = (
        f"Generado {now.strftime('%Y-%m-%d %H:%M')} "
        f"({timezone.get_current_timezone_name()}) ·{stamp}"
    )

    # ----- KPI tablero productivo -----
    recibidos = Ticket.objects.count()
    abiertos = Ticket.objects.filter(
        estado__in=["ABIERTO", "EN_PROCESO"]
    ).count()
    cerrados = Ticket.objects.filter(estado="CERRADO").count()
    kpi_headers = ["KPI dashboard /pgo/", "Valor"]
    kpi_rows = [
        ["Recibidos (total)", recibidos],
        ["Abiertos (ABIERTO+EN_PROCESO)", abiertos],
        ["Cerrados", cerrados],
    ]

    resultados = list(
        PgoResultadoPeriodo.objects.select_related("unidad_negocio").order_by(
            "periodo", "unidad_negocio__nombre"
        )
    )
    res_headers = [
        "Periodo",
        "Unidad",
        "Código UN",
        "Cerrados",
        "Abiertos",
        "Tiempo prom. h",
        "SLA %",
    ]
    res_rows = []
    for r in resultados:
        res_rows.append(
            [
                r.periodo,
                r.unidad_negocio.nombre if r.unidad_negocio else "—",
                r.unidad_negocio.code if r.unidad_negocio else "—",
                r.tickets_cerrados,
                r.tickets_abiertos,
                fmt_num(r.tiempo_promedio_horas, 2),
                fmt_num(r.cumplimiento_sla_pct, 2),
            ]
        )

    # Serie de cifras base (equivalente a “charts”): por período totales
    serie_headers = [
        "Periodo",
        "Cerrados",
        "Abiertos",
        "SLA % ponderado (promedio simple UN)",
        "Tiempo prom. h (promedio simple UN)",
    ]
    serie_rows = []
    by_period: dict[str, list] = {}
    for r in resultados:
        by_period.setdefault(r.periodo, []).append(r)
    for periodo in sorted(by_period):
        rows_p = by_period[periodo]
        n = len(rows_p) or 1
        serie_rows.append(
            [
                periodo,
                sum(x.tickets_cerrados for x in rows_p),
                sum(x.tickets_abiertos for x in rows_p),
                fmt_num(sum(float(x.cumplimiento_sla_pct or 0) for x in rows_p) / n, 2),
                fmt_num(sum(float(x.tiempo_promedio_horas or 0) for x in rows_p) / n, 2),
            ]
        )

    periodos = sorted({r.periodo for r in resultados})
    curr_p = periodos[-1] if periodos else None
    prev_p = periodos[-2] if len(periodos) > 1 else None
    cambios = []
    if curr_p and prev_p:
        prev_map = {r.unidad_negocio_id: r for r in resultados if r.periodo == prev_p}
        for r in [x for x in resultados if x.periodo == curr_p]:
            prv = prev_map.get(r.unidad_negocio_id)
            if not prv:
                continue
            cambios.append(
                f"{r.unidad_negocio.code if r.unidad_negocio else '?'}: "
                f"SLA {fmt_num(prv.cumplimiento_sla_pct, 2)}%→{fmt_num(r.cumplimiento_sla_pct, 2)}% "
                f"({pct_change(r.cumplimiento_sla_pct, prv.cumplimiento_sla_pct)}); "
                f"cerrados {prv.tickets_cerrados}→{r.tickets_cerrados}; "
                f"abiertos {prv.tickets_abiertos}→{r.tickets_abiertos}"
            )

    # Resumen por usuario (como /pgo/resumen/usuario/)
    user_headers = ["Usuario asignado", "Total tickets", "Abiertos"]
    user_rows = []
    for row in (
        Ticket.objects.values("asignado_a__username")
        .annotate(
            total=Count("id"),
            abiertos_n=Count("id", filter=Q(estado="ABIERTO")),
        )
        .order_by("-total")
    ):
        user_rows.append(
            [
                row["asignado_a__username"] or "(sin asignar)",
                row["total"],
                row["abiertos_n"],
            ]
        )

    # Resumen por unidad
    un_headers = ["Código UN", "Nombre", "Total tickets"]
    un_rows = []
    for row in (
        Ticket.objects.values("unidad_negocio__code", "unidad_negocio__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")
    ):
        un_rows.append(
            [
                row["unidad_negocio__code"] or "—",
                row["unidad_negocio__nombre"] or "—",
                row["total"],
            ]
        )

    by_estado = list(
        Ticket.objects.values("estado").annotate(n=Count("id")).order_by("estado")
    )
    by_prio = list(
        Ticket.objects.values("prioridad").annotate(n=Count("id")).order_by("prioridad")
    )

    ticket_headers = [
        "Código",
        "Título",
        "Descripción",
        "Estado",
        "Prioridad",
        "UN",
        "Entidad",
        "Asignado",
        "Apertura",
        "Cierre",
        "SLA horas",
        "Horas ciclo",
        "SLA ok",
        "Creado",
        "Actualizado",
    ]
    ticket_rows = []
    for t in Ticket.objects.select_related(
        "unidad_negocio", "entidad", "asignado_a"
    ).order_by("-fecha_apertura", "codigo"):
        horas = ""
        sla_ok = ""
        if t.fecha_apertura and t.fecha_cierre:
            try:
                delta = t.fecha_cierre - t.fecha_apertura
                horas_val = round(delta.total_seconds() / 3600, so=2)
                horas = horas_val
                sla_ok = "Sí" if horas_val <= float(t.sla_horas or 0) else "No"
            except Exception:
                pass
        ticket_rows.append(
            [
                t.codigo,
                t.titulo or "",
                t.descripcion or "",
                t.estado,
                t.prioridad,
                t.unidad_negocio.code if t.unidad_negocio else "—",
                getattr(t.entidad, "codigo", None)
                or getattr(t.entidad, "nombre", None)
                or "—",
                getattr(t.asignado_a, "username", None) or "—",
                t.fecha_apertura.isoformat() if t.fecha_apertura else "",
                t.fecha_cierre.isoformat() if t.fecha_cierre else "",
                t.sla_horas,
                horas,
                sla_ok,
                t.created_at.isoformat() if t.created_at else "",
                t.updated_at.isoformat() if t.updated_at else "",
            ]
        )

    evento_headers = ["Ticket", "Tipo", "Fecha", "Usuario", "Descripción"]
    evento_rows = []
    evento_cap = 5000
    for e in (
        TicketEvento.objects.select_related("ticket", "usuario")
        .order_by("-fecha")[:evento_cap]
    ):
        evento_rows.append(
            [
                e.ticket.codigo if e.ticket else "—",
                e.tipo,
                e.fecha.isoformat() if e.fecha else "",
                getattr(e.usuario, "username", None) or "—",
                e.descripcion or "",
            ]
        )
    evento_total = TicketEvento.objects.count()

    wcg_md, wcg_sheets, wcg_hechos, wcg_vacios = _wcg_pgo_block(stamp_label)

    hechos = [
        f"Tickets productivo: {recibidos}",
        f"Abiertos: {abiertos} · Cerrados: {cerrados}",
        f"Filas PgoResultadoPeriodo: {len(res_rows)}",
        f"Período último resultados: {curr_p or 'n/d'}",
        f"Período anterior: {prev_p or 'n/d'}",
        f"Eventos listados: {len(evento_rows)} de {evento_total}",
        *wcg_hechos,
    ]
    vacios = list(wcg_vacios)
    if not ticket_rows:
        vacios.append("Sin tickets en pgo.Ticket.")
    if not res_rows:
        vacios.append("Sin PgoResultadoPeriodo (importar tickets / recalcular períodos).")
    if evento_total > evento_cap:
        vacios.append(
            f"TicketEvento truncado a {evento_cap} filas más recientes (hay {evento_total})."
        )

    md_parts = [
        h1("Reporte de resultados PGO (extenso)"),
        p(stamp_label),
        p(
            "Propósito: datos operativos completos de PGO para análisis estratégico "
            "por IA y exportación Excel humana. CRM no se incluye."
        ),
        h2("Cómo se procesa PGO"),
        p(PGO_EXPLAIN),
        h2("Dashboard productivo — KPIs"),
        md_table(kpi_headers, kpi_rows),
        h2("Dashboard — resultados por período y unidad"),
        p(
            "Tabla del tablero `/pgo/` (`PgoResultadoPeriodo`). Sentido: medir "
            "carga y cumplimiento SLA por UN y mes de apertura del ticket."
        ),
        p(f"Filas: **{len(res_rows)}**."),
        md_table(res_headers, res_rows) if res_rows else p("_Sin resultados de período._"),
        h2("Cifras base por período (serie para análisis / gráficos)"),
        p(
            "Agregados por período a partir de la tabla de resultados — útiles para "
            "construir tendencias de volumen y SLA en Excel o por IA."
        ),
        md_table(serie_headers, serie_rows) if serie_rows else p("_Sin serie._"),
        h2("Cambios último vs período anterior"),
        bullets(cambios[:80] or ["Sin pares de períodos comparables."]),
        h2("Resumen de tickets por estado"),
        md_table(
            ["Estado", "Cantidad"],
            [[r["estado"], r["n"]] for r in by_estado],
        )
        if by_estado
        else p("_Sin tickets._"),
        h2("Resumen de tickets por prioridad"),
        md_table(
            ["Prioridad", "Cantidad"],
            [[r["prioridad"], r["n"]] for r in by_prio],
        )
        if by_prio
        else p("_Sin desglose._"),
        h2("Resumen por unidad de negocio (browse tablero)"),
        md_table(un_headers, un_rows) if un_rows else p("_Sin desglose._"),
        h2("Resumen por usuario asignado"),
        p("Equivalente a `/pgo/resumen/usuario/`."),
        md_table(user_headers, user_rows) if user_rows else p("_Sin asignación._"),
        h2("Detalle completo de tickets (browse administración)"),
        p(
            f"Registros: **{len(ticket_rows)}**. Incluye descripción completa "
            "como en el detalle del ticket."
        ),
        md_table(ticket_headers, ticket_rows) if ticket_rows else p("_Sin tickets._"),
        h2("Eventos de tickets"),
        p(
            f"Filas incluidas: **{len(evento_rows)}**"
            + (f" (tope {evento_cap}; total BD {evento_total})." if evento_total else ".")
        ),
        md_table(evento_headers, evento_rows) if evento_rows else p("_Sin eventos._"),
        *wcg_md,
        h2("Inventario"),
        bullets(hechos),
        h2("Guía de análisis estratégico (IA)"),
        p(
            "Con las tablas anteriores, construye un diagnóstico de operación PGO: "
            "(1) ¿el SLA mejora o empeora por UN y período?; "
            "(2) ¿hay sobrecarga en usuarios o unidades concretas?; "
            "(3) ¿cuántos tickets abiertos críticos/alta prioridad hay y desde cuándo?; "
            "(4) recomendaciones accionables (redistribuir, revisar SLA, priorizar backlog). "
            "Cita cifras explícitas. No inventes Clasifica ni umbrales ausentes en los datos."
        ),
    ]
    if cfg.include_ai_section:
        md_parts.append(
            ai_closing(
                hechos,
                cambios[:40] if cfg.include_period_comparison else ["Comparación desactivada."],
                vacios or ["Sin vacíos críticos adicionales."],
            )
        )

    sheets = [
        _sheet("KPI dashboard", "KPIs /pgo/", kpi_headers, kpi_rows),
        _sheet("Resultados periodo", "PgoResultadoPeriodo", res_headers, res_rows),
        _sheet("Serie por periodo", "Cifras base tendencia", serie_headers, serie_rows),
        _sheet("Por estado", "Conteo tickets", ["Estado", "N"], [[r["estado"], r["n"]] for r in by_estado]),
        _sheet(
            "Por prioridad",
            "Conteo prioridad",
            ["Prioridad", "N"],
            [[r["prioridad"], r["n"]] for r in by_prio],
        ),
        _sheet("Por UN", "Resumen unidad", un_headers, un_rows),
        _sheet("Por usuario", "Resumen asignado", user_headers, user_rows),
        _sheet("Tickets", "Detalle tickets PGO", ticket_headers, ticket_rows),
        _sheet("Eventos", f"TicketEvento (hasta {evento_cap})", evento_headers, evento_rows),
        _sheet(
            "Explicacion",
            "Proceso PGO",
            ["Tema", "Detalle"],
            [
                ["Fuente productiva", "pgo.Ticket + recalculate_pgo_periodos"],
                ["SLA", "horas ciclo <= sla_horas"],
                ["Clasifica PGO productivo", "No implementada"],
                ["Fuente WCG One", "apps.pgo.* si hay datos"],
            ],
        ),
        *wcg_sheets,
    ]

    return {
        "md": join_sections(*md_parts),
        "sheets": sheets,
        "stamp": stamp,
        "stamp_label": stamp_label,
        "period": curr_p,
        "prev_period": prev_p,
    }

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Resultados PGO extensos: dashboard productivo + browse + stack WCG One."""
00002|
00003|from __future__ import annotations
00004|
00005|from django.db.models import Count, Q
00006|from django.utils import timezone
00007|
00008|from pgo.models import PgoResultadoPeriodo, Ticket, TicketEvento
00009|from reports.md_utils import ai_closing, bullets, h1, h2, h3, join_sections, md_table, p
00010|from reports.models import ReportConfig
00011|from reports.naming import report_stamp
00012|from reports.services.common import fmt_num, pct_change
00013|
00014|PGO_EXPLAIN = """
00015|El **dashboard PGO productivo** (`/pgo/`) se alimenta de tickets (`pgo.Ticket`).
00016|Tras la importación (o al abrir el dashboard) se ejecuta
00017|`pgo.periodo.recalculate_pgo_periodos`, que llena `PgoResultadoPeriodo` por
00018|período (`YYYY-MM` de apertura) y unidad de negocio con:
00019|
00020|- tickets cerrados / abiertos
00021|- tiempo promedio de cierre (horas)
00022|- % cumplimiento SLA: cerrados cuyo tiempo ≤ `sla_horas` del ticket
00023|
00024|**No** hay en el pipeline productivo un campo `Clasifica` calculado.
00025|El stack WCG One (`apps.pgo`) puede coexistir con tickets, agregados mensuales
00026|y `PgoPeriodScore.clasifica` si existen filas; el motor de score no está
00027|garantizado en código.
00028|
00029|Este reporte incluye **ambas fuentes** cuando hay datos: tablas del tablero,
00030|resúmenes por usuario/unidad, detalle browse de tickets y el detalle WCG One.
00031|""".strip()
00032|
00033|
00034|def _sheet(name, title, headers, rows):
00035|    return {"name": name[:31], "title": title, "headers": headers, "rows": rows}
00036|
00037|
00038|def _wcg_pgo_block(stamp_label: str) -> tuple[list[str], list[dict], list[str], list[str]]:
00039|    """Secciones MD + sheets + hechos + vacíos del stack apps.pgo."""
00040|    md: list[str] = []
00041|    sheets: list[dict] = []
00042|    hechos: list[str] = []
00043|    vacios: list[str] = []
00044|    try:
00045|        from apps.pgo.models import (
00046|            PgoMetricRule,
00047|            PgoMonthlyAgg,
00048|            PgoPeriodScore,
00049|            PgoTicket,
00050|        )
00051|        from apps.pgo.selectors import ticket_dashboard_summary
00052|    except Exception as exc:
00053|        md.append(h2("Stack WCG One PGO (`apps.pgo`)"))
00054|        md.append(p(f"_No disponible: {exc}_"))
00055|        vacios.append(f"Stack apps.pgo no importable: {exc}")
00056|        return md, sheets, hechos, vacios
00057|
00058|    summary = ticket_dashboard_summary()
00059|    kpi_headers = ["KPI", "Valor"]
00060|    kpi_rows = [
00061|        ["Total tickets", summary["total_tickets"]],
00062|        ["Abiertos", summary["tickets_abiertos"]],
00063|        ["Cerrados", summary["tickets_cerrados"]],
00064|        ["Vencidos (abiertos SLA no)", summary["tickets_vencidos"]],
00065|        ["SLA cumplidos", summary["sla_cumplidos"]],
00066|        ["SLA incumplidos (abiertos)", summary["sla_incumplidos"]],
00067|        ["Tiempo promedio (h)", fmt_num(summary["tiempo_promedio"], 2) if summary["tiempo_promedio"] is not None else "—"],
00068|    ]
00069|    hechos.append(f"WCG One PgoTicket: {summary['total_tickets']}")
00070|
00071|    md.extend(
00072|        [
00073|            h2("Stack WCG One — dashboard KPIs (`apps.pgo`)"),
00074|            p(
00075|                "Equivalente a `/wcgone/pgo/`: KPIs, desglose por estado/prioridad "
00076|                "y detalle completo de tickets importados al schema WCG One."
00077|            ),
00078|            md_table(kpi_headers, kpi_rows),
00079|            h3("Por estado normalizado"),
00080|            md_table(
00081|                ["Estado", "Total"],
00082|                [[r["estado_normalizado"] or "—", r["total"]] for r in summary["por_estado"]],
00083|            )
00084|            if summary["por_estado"]
00085|            else p("_Sin desglose por estado._"),
00086|            h3("Por prioridad"),
00087|            md_table(
00088|                ["Prioridad", "Total"],
00089|                [[r["prioridad"] or "—", r["total"]] for r in summary["por_prioridad"]],
00090|            )
00091|            if summary["por_prioridad"]
00092|            else p("_Sin desglose por prioridad._"),
00093|        ]
00094|    )
00095|    sheets.append(_sheet("WCG KPI", "KPIs WCG One PGO", kpi_headers, kpi_rows))
00096|    sheets.append(
00097|        _sheet(
00098|            "WCG por estado",
00099|            "PgoTicket por estado",
00100|            ["Estado", "Total"],
00101|            [[r["estado_normalizado"] or "", r["total"]] for r in summary["por_estado"]],
00102|        )
00103|    )
00104|    sheets.append(
00105|        _sheet(
00106|            "WCG por prioridad",
00107|            "PgoTicket por prioridad",
00108|            ["Prioridad", "Total"],
00109|            [[r["prioridad"] or "", r["total"]] for r in summary["por_prioridad"]],
00110|        )
00111|    )
00112|
00113|    ticket_headers = [
00114|        "ID externo",
00115|        "Título",
00116|        "Estado raw",
00117|        "Estado norm.",
00118|        "Prioridad",
00119|        "Departamento",
00120|        "Sistema",
00121|        "Periodo",
00122|        "UN",
00123|        "Responsable",
00124|        "Solicita",
00125|        "Correo",
00126|        "Tipo",
00127|        "Tipo servicio",
00128|        "Elemento",
00129|        "Ruta",
00130|        "Apertura",
00131|        "Cierre",
00132|        "Duración h",
00133|        "SLA h",
00134|        "SLA ok",
00135|        "Solución",
00136|        "Razón cierre",
00137|    ]
00138|    ticket_rows = []
00139|    for t in PgoTicket.objects.select_related("unidad_negocio", "responsable").order_by(
00140|        "-fecha_apertura", "ticket_externo_id"
00141|    ):
00142|        ticket_rows.append(
00143|            [
00144|                t.ticket_externo_id,
00145|                t.titulo or "",
00146|                t.estado_raw or "",
00147|                t.estado_normalizado or "",
00148|                t.prioridad or "",
00149|                t.departamento or "",
00150|                t.sistema or "",
00151|                t.anio_mes or "",
00152|                t.unidad_negocio.code if t.unidad_negocio else "—",
00153|                getattr(t.responsable, "username", None) or "—",
00154|                t.usuario_solicita or "",
00155|                t.correo_solicita or "",
00156|                t.tipo or "",
00157|                t.tipo_servicio or "",
00158|                t.elemento or "",
00159|                t.ruta or "",
00160|                t.fecha_apertura.isoformat() if t.fecha_apertura else "",
00161|                t.fecha_cierre.isoformat() if t.fecha_cierre else "",
00162|                fmt_num(t.duracion_horas, 2) if t.duracion_horas is not None else "",
00163|                t.sla_horas if t.sla_horas is not None else "",
00164|                "Sí" if t.sla_cumplido else ("No" if t.sla_cumplido is False else "—"),
00165|                (t.solucion or "")[:300],
00166|                (t.razon_cierre or "")[:160],
00167|            ]
00168|        )
00169|    md.extend(
00170|        [
00171|            h2("WCG One — detalle completo de tickets (browse)"),
00172|            p(f"Registros: **{len(ticket_rows)}**. Exportables también en Excel."),
00173|            md_table(ticket_headers, ticket_rows) if ticket_rows else p("_Sin PgoTicket._"),
00174|        ]
00175|    )
00176|    sheets.append(_sheet("WCG Tickets", "PgoTicket detalle", ticket_headers, ticket_rows))
00177|    if not ticket_rows:
00178|        vacios.append("Sin PgoTicket en apps.pgo (importar tickets WCG One).")
00179|
00180|    score_headers = [
00181|        "Periodo",
00182|        "Área",
00183|        "UN",
00184|        "Usuario",
00185|        "Puntaje",
00186|        "Clasifica",
00187|        "Fecha cálculo",
00188|        "Detalle JSON",
00189|    ]
00190|    score_rows = []
00191|    for s in PgoPeriodScore.objects.select_related("unidad_negocio", "usuario").order_by(
00192|        "-periodo", "area"
00193|    ):
00194|        score_rows.append(
00195|            [
00196|                s.periodo,
00197|                s.area or "",
00198|                str(s.unidad_negocio) if s.unidad_negocio else "—",
00199|                str(s.usuario) if s.usuario else "—",
00200|                fmt_num(s.puntaje_total, 2),
00201|                "Sí" if s.clasifica else "No",
00202|                s.fecha_calculo.isoformat() if getattr(s, "fecha_calculo", None) else "",
00203|                str(s.detalle_json or "")[:400],
00204|            ]
00205|        )
00206|    md.extend(
00207|        [
00208|            h2("WCG One — resultados / PgoPeriodScore"),
00209|            p(
00210|                "Tabla de `/wcgone/pgo/resultados/`. **Clasifica** solo si hay filas; "
00211|                "no inventar umbrales si el puntaje no está calculado en código."
00212|            ),
00213|            md_table(score_headers, score_rows)
00214|            if score_rows
00215|            else p("_Sin PgoPeriodScore._"),
00216|        ]
00217|    )
00218|    sheets.append(_sheet("WCG Scores", "PgoPeriodScore", score_headers, score_rows))
00219|    hechos.append(f"WCG One PgoPeriodScore: {len(score_rows)}")
00220|    if not score_rows:
00221|        vacios.append("Sin PgoPeriodScore (scoring WCG One vacío o no calculado).")
00222|
00223|    agg_headers = [
00224|        "Periodo",
00225|        "UN",
00226|        "Departamento",
00227|        "Recibidos",
00228|        "Cerrados",
00229|        "Abiertos fin mes",
00230|        "Tiempo prom. h",
00231|        "SLA ok",
00232|        "SLA no",
00233|    ]
00234|    agg_rows = []
00235|    for a in PgoMonthlyAgg.objects.select_related("unidad_negocio").order_by(
00236|        "-periodo", "unidad_negocio__nombre"
00237|    ):
00238|        agg_rows.append(
00239|            [
00240|                a.periodo,
00241|                str(a.unidad_negocio) if a.unidad_negocio else "—",
00242|                a.departamento or "",
00243|                a.tickets_recibidos,
00244|                a.tickets_cerrados,
00245|                a.tickets_abiertos_fin_mes,
00246|                fmt_num(a.tiempo_promedio_horas, 2) if a.tiempo_promedio_horas is not None else "",
00247|                a.sla_cumplidos,
00248|                a.sla_incumplidos,
00249|            ]
00250|        )
00251|    md.extend(
00252|        [
00253|            h2("WCG One — agregados mensuales (PgoMonthlyAgg)"),
00254|            md_table(agg_headers, agg_rows) if agg_rows else p("_Sin PgoMonthlyAgg._"),
00255|        ]
00256|    )
00257|    sheets.append(_sheet("WCG Agg mensual", "PgoMonthlyAgg", agg_headers, agg_rows))
00258|
00259|    rule_headers = [
00260|        "Código",
00261|        "Área",
00262|        "Variable",
00263|        "Puntos",
00264|        "Peso",
00265|        "Tipo regla",
00266|        "Activo",
00267|        "Fórmula",
00268|        "Notas",
00269|    ]
00270|    rule_rows = []
00271|    for r in PgoMetricRule.objects.order_by("area", "codigo"):
00272|        rule_rows.append(
00273|            [
00274|                r.codigo,
00275|                r.area or "",
00276|                r.variable or "",
00277|                fmt_num(r.puntos, 2) if r.puntos is not None else "",
00278|                fmt_num(r.peso, 2) if r.peso is not None else "",
00279|                r.tipo_regla or "",
00280|                "Sí" if r.activo else "No",
00281|                (r.formula_texto or "")[:200],
00282|                (r.notas or "")[:160],
00283|            ]
00284|        )
00285|    md.extend(
00286|        [
00287|            h2("WCG One — catálogo de reglas de métrica"),
00288|            md_table(rule_headers, rule_rows)
00289|            if rule_rows
00290|            else p("_Sin PgoMetricRule._"),
00291|        ]
00292|    )
00293|    sheets.append(_sheet("WCG Reglas", "PgoMetricRule", rule_headers, rule_rows))
00294|    return md, sheets, hechos, vacios
00295|
00296|
00297|def build_pgo_results(cfg: ReportConfig | None = None) -> dict:
00298|    cfg = cfg or ReportConfig.get_active()
00299|    now = timezone.localtime()
00300|    stamp = report_stamp(now)
00301|    stamp_label = (
00302|        f"Generado {now.strftime('%Y-%m-%d %H:%M')} "
00303|        f"({timezone.get_current_timezone_name()}) ·{stamp}"
00304|    )
00305|
00306|    # ----- KPI tablero productivo -----
00307|    recibidos = Ticket.objects.count()
00308|    abiertos = Ticket.objects.filter(
00309|        estado__in=["ABIERTO", "EN_PROCESO"]
00310|    ).count()
00311|    cerrados = Ticket.objects.filter(estado="CERRADO").count()
00312|    kpi_headers = ["KPI dashboard /pgo/", "Valor"]
00313|    kpi_rows = [
00314|        ["Recibidos (total)", recibidos],
00315|        ["Abiertos (ABIERTO+EN_PROCESO)", abiertos],
00316|        ["Cerrados", cerrados],
00317|    ]
00318|
00319|    resultados = list(
00320|        PgoResultadoPeriodo.objects.select_related("unidad_negocio").order_by(
00321|            "periodo", "unidad_negocio__nombre"
00322|        )
00323|    )
00324|    res_headers = [
00325|        "Periodo",
00326|        "Unidad",
00327|        "Código UN",
00328|        "Cerrados",
00329|        "Abiertos",
00330|        "Tiempo prom. h",
00331|        "SLA %",
00332|    ]
00333|    res_rows = []
00334|    for r in resultados:
00335|        res_rows.append(
00336|            [
00337|                r.periodo,
00338|                r.unidad_negocio.nombre if r.unidad_negocio else "—",
00339|                r.unidad_negocio.code if r.unidad_negocio else "—",
00340|                r.tickets_cerrados,
00341|                r.tickets_abiertos,
00342|                fmt_num(r.tiempo_promedio_horas, 2),
00343|                fmt_num(r.cumplimiento_sla_pct, 2),
00344|            ]
00345|        )
00346|
00347|    # Serie de cifras base (equivalente a “charts”): por período totales
00348|    serie_headers = [
00349|        "Periodo",
00350|        "Cerrados",
00351|        "Abiertos",
00352|        "SLA % ponderado (promedio simple UN)",
00353|        "Tiempo prom. h (promedio simple UN)",
00354|    ]
00355|    serie_rows = []
00356|    by_period: dict[str, list] = {}
00357|    for r in resultados:
00358|        by_period.setdefault(r.periodo, []).append(r)
00359|    for periodo in sorted(by_period):
00360|        rows_p = by_period[periodo]
00361|        n = len(rows_p) or 1
00362|        serie_rows.append(
00363|            [
00364|                periodo,
00365|                sum(x.tickets_cerrados for x in rows_p),
00366|                sum(x.tickets_abiertos for x in rows_p),
00367|                fmt_num(sum(float(x.cumplimiento_sla_pct or 0) for x in rows_p) / n, 2),
00368|                fmt_num(sum(float(x.tiempo_promedio_horas or 0) for x in rows_p) / n, 2),
00369|            ]
00370|        )
00371|
00372|    periodos = sorted({r.periodo for r in resultados})
00373|    curr_p = periodos[-1] if periodos else None
00374|    prev_p = periodos[-2] if len(periodos) > 1 else None
00375|    cambios = []
00376|    if curr_p and prev_p:
00377|        prev_map = {r.unidad_negocio_id: r for r in resultados if r.periodo == prev_p}
00378|        for r in [x for x in resultados if x.periodo == curr_p]:
00379|            prv = prev_map.get(r.unidad_negocio_id)
00380|            if not prv:
00381|                continue
00382|            cambios.append(
00383|                f"{r.unidad_negocio.code if r.unidad_negocio else '?'}: "
00384|                f"SLA {fmt_num(prv.cumplimiento_sla_pct, 2)}%→{fmt_num(r.cumplimiento_sla_pct, 2)}% "
00385|                f"({pct_change(r.cumplimiento_sla_pct, prv.cumplimiento_sla_pct)}); "
00386|                f"cerrados {prv.tickets_cerrados}→{r.tickets_cerrados}; "
00387|                f"abiertos {prv.tickets_abiertos}→{r.tickets_abiertos}"
00388|            )
00389|
00390|    # Resumen por usuario (como /pgo/resumen/usuario/)
00391|    user_headers = ["Usuario asignado", "Total tickets", "Abiertos"]
00392|    user_rows = []
00393|    for row in (
00394|        Ticket.objects.values("asignado_a__username")
00395|        .annotate(
00396|            total=Count("id"),
00397|            abiertos_n=Count("id", filter=Q(estado="ABIERTO")),
00398|        )
00399|        .order_by("-total")
00400|    ):
00401|        user_rows.append(
00402|            [
00403|                row["asignado_a__username"] or "(sin asignar)",
00404|                row["total"],
00405|                row["abiertos_n"],
00406|            ]
00407|        )
00408|
00409|    # Resumen por unidad
00410|    un_headers = ["Código UN", "Nombre", "Total tickets"]
00411|    un_rows = []
00412|    for row in (
00413|        Ticket.objects.values("unidad_negocio__code", "unidad_negocio__nombre")
00414|        .annotate(total=Count("id"))
00415|        .order_by("-total")
00416|    ):
00417|        un_rows.append(
00418|            [
00419|                row["unidad_negocio__code"] or "—",
00420|                row["unidad_negocio__nombre"] or "—",
00421|                row["total"],
00422|            ]
00423|        )
00424|
00425|    by_estado = list(
00426|        Ticket.objects.values("estado").annotate(n=Count("id")).order_by("estado")
00427|    )
00428|    by_prio = list(
00429|        Ticket.objects.values("prioridad").annotate(n=Count("id")).order_by("prioridad")
00430|    )
00431|
00432|    ticket_headers = [
00433|        "Código",
00434|        "Título",
00435|        "Descripción",
00436|        "Estado",
00437|        "Prioridad",
00438|        "UN",
00439|        "Entidad",
00440|        "Asignado",
00441|        "Apertura",
00442|        "Cierre",
00443|        "SLA horas",
00444|        "Horas ciclo",
00445|        "SLA ok",
00446|        "Creado",
00447|        "Actualizado",
00448|    ]
00449|    ticket_rows = []
00450|    for t in Ticket.objects.select_related(
00451|        "unidad_negocio", "entidad", "asignado_a"
00452|    ).order_by("-fecha_apertura", "codigo"):
00453|        horas = ""
00454|        sla_ok = ""
00455|        if t.fecha_apertura and t.fecha_cierre:
00456|            try:
00457|                delta = t.fecha_cierre - t.fecha_apertura
00458|                horas_val = round(delta.total_seconds() / 3600, so=2)
00459|                horas = horas_val
00460|                sla_ok = "Sí" if horas_val <= float(t.sla_horas or 0) else "No"
00461|            except Exception:
00462|                pass
00463|        ticket_rows.append(
00464|            [
00465|                t.codigo,
00466|                t.titulo or "",
00467|                t.descripcion or "",
00468|                t.estado,
00469|                t.prioridad,
00470|                t.unidad_negocio.code if t.unidad_negocio else "—",
00471|                getattr(t.entidad, "codigo", None)
00472|                or getattr(t.entidad, "nombre", None)
00473|                or "—",
00474|                getattr(t.asignado_a, "username", None) or "—",
00475|                t.fecha_apertura.isoformat() if t.fecha_apertura else "",
00476|                t.fecha_cierre.isoformat() if t.fecha_cierre else "",
00477|                t.sla_horas,
00478|                horas,
00479|                sla_ok,
00480|                t.created_at.isoformat() if t.created_at else "",
00481|                t.updated_at.isoformat() if t.updated_at else "",
00482|            ]
00483|        )
00484|
00485|    evento_headers = ["Ticket", "Tipo", "Fecha", "Usuario", "Descripción"]
00486|    evento_rows = []
00487|    evento_cap = 5000
00488|    for e in (
00489|        TicketEvento.objects.select_related("ticket", "usuario")
00490|        .order_by("-fecha")[:evento_cap]
00491|    ):
00492|        evento_rows.append(
00493|            [
00494|                e.ticket.codigo if e.ticket else "—",
00495|                e.tipo,
00496|                e.fecha.isoformat() if e.fecha else "",
00497|                getattr(e.usuario, "username", None) or "—",
00498|                e.descripcion or "",
00499|            ]
00500|        )
00501|    evento_total = TicketEvento.objects.count()
00502|
00503|    wcg_md, wcg_sheets, wcg_hechos, wcg_vacios = _wcg_pgo_block(stamp_label)
00504|
00505|    hechos = [
00506|        f"Tickets productivo: {recibidos}",
00507|        f"Abiertos: {abiertos} · Cerrados: {cerrados}",
00508|        f"Filas PgoResultadoPeriodo: {len(res_rows)}",
00509|        f"Período último resultados: {curr_p or 'n/d'}",
00510|        f"Período anterior: {prev_p or 'n/d'}",
00511|        f"Eventos listados: {len(evento_rows)} de {evento_total}",
00512|        *wcg_hechos,
00513|    ]
00514|    vacios = list(wcg_vacios)
00515|    if not ticket_rows:
00516|        vacios.append("Sin tickets en pgo.Ticket.")
00517|    if not res_rows:
00518|        vacios.append("Sin PgoResultadoPeriodo (importar tickets / recalcular períodos).")
00519|    if evento_total > evento_cap:
00520|        vacios.append(
00521|            f"TicketEvento truncado a {evento_cap} filas más recientes (hay {evento_total})."
00522|        )
00523|
00524|    md_parts = [
00525|        h1("Reporte de resultados PGO (extenso)"),
00526|        p(stamp_label),
00527|        p(
00528|            "Propósito: datos operativos completos de PGO para análisis estratégico "
00529|            "por IA y exportación Excel humana. CRM no se incluye."
00530|        ),
00531|        h2("Cómo se procesa PGO"),
00532|        p(PGO_EXPLAIN),
00533|        h2("Dashboard productivo — KPIs"),
00534|        md_table(kpi_headers, kpi_rows),
00535|        h2("Dashboard — resultados por período y unidad"),
00536|        p(
00537|            "Tabla del tablero `/pgo/` (`PgoResultadoPeriodo`). Sentido: medir "
00538|            "carga y cumplimiento SLA por UN y mes de apertura del ticket."
00539|        ),
00540|        p(f"Filas: **{len(res_rows)}**."),
00541|        md_table(res_headers, res_rows) if res_rows else p("_Sin resultados de período._"),
00542|        h2("Cifras base por período (serie para análisis / gráficos)"),
00543|        p(
00544|            "Agregados por período a partir de la tabla de resultados — útiles para "
00545|            "construir tendencias de volumen y SLA en Excel o por IA."
00546|        ),
00547|        md_table(serie_headers, serie_rows) if serie_rows else p("_Sin serie._"),
00548|        h2("Cambios último vs período anterior"),
00549|        bullets(cambios[:80] or ["Sin pares de períodos comparables."]),
00550|        h2("Resumen de tickets por estado"),
00551|        md_table(
00552|            ["Estado", "Cantidad"],
00553|            [[r["estado"], r["n"]] for r in by_estado],
00554|        )
00555|        if by_estado
00556|        else p("_Sin tickets._"),
00557|        h2("Resumen de tickets por prioridad"),
00558|        md_table(
00559|            ["Prioridad", "Cantidad"],
00560|            [[r["prioridad"], r["n"]] for r in by_prio],
00561|        )
00562|        if by_prio
00563|        else p("_Sin desglose._"),
00564|        h2("Resumen por unidad de negocio (browse tablero)"),
00565|        md_table(un_headers, un_rows) if un_rows else p("_Sin desglose._"),
00566|        h2("Resumen por usuario asignado"),
00567|        p("Equivalente a `/pgo/resumen/usuario/`."),
00568|        md_table(user_headers, user_rows) if user_rows else p("_Sin asignación._"),
00569|        h2("Detalle completo de tickets (browse administración)"),
00570|        p(
00571|            f"Registros: **{len(ticket_rows)}**. Incluye descripción completa "
00572|            "como en el detalle del ticket."
00573|        ),
00574|        md_table(ticket_headers, ticket_rows) if ticket_rows else p("_Sin tickets._"),
00575|        h2("Eventos de tickets"),
00576|        p(
00577|            f"Filas incluidas: **{len(evento_rows)}**"
00578|            + (f" (tope {evento_cap}; total BD {evento_total})." if evento_total else ".")
00579|        ),
00580|        md_table(evento_headers, evento_rows) if evento_rows else p("_Sin eventos._"),
00581|        *wcg_md,
00582|        h2("Inventario"),
00583|        bullets(hechos),
00584|        h2("Guía de análisis estratégico (IA)"),
00585|        p(
00586|            "Con las tablas anteriores, construye un diagnóstico de operación PGO: "
00587|            "(1) ¿el SLA mejora o empeora por UN y período?; "
00588|            "(2) ¿hay sobrecarga en usuarios o unidades concretas?; "
00589|            "(3) ¿cuántos tickets abiertos críticos/alta prioridad hay y desde cuándo?; "
00590|            "(4) recomendaciones accionables (redistribuir, revisar SLA, priorizar backlog). "
00591|            "Cita cifras explícitas. No inventes Clasifica ni umbrales ausentes en los datos."
00592|        ),
00593|    ]
00594|    if cfg.include_ai_section:
00595|        md_parts.append(
00596|            ai_closing(
00597|                hechos,
00598|                cambios[:40] if cfg.include_period_comparison else ["Comparación desactivada."],
00599|                vacios or ["Sin vacíos críticos adicionales."],
00600|            )
00601|        )
00602|
00603|    sheets = [
00604|        _sheet("KPI dashboard", "KPIs /pgo/", kpi_headers, kpi_rows),
00605|        _sheet("Resultados periodo", "PgoResultadoPeriodo", res_headers, res_rows),
00606|        _sheet("Serie por periodo", "Cifras base tendencia", serie_headers, serie_rows),
00607|        _sheet("Por estado", "Conteo tickets", ["Estado", "N"], [[r["estado"], r["n"]] for r in by_estado]),
00608|        _sheet(
00609|            "Por prioridad",
00610|            "Conteo prioridad",
00611|            ["Prioridad", "N"],
00612|            [[r["prioridad"], r["n"]] for r in by_prio],
00613|        ),
00614|        _sheet("Por UN", "Resumen unidad", un_headers, un_rows),
00615|        _sheet("Por usuario", "Resumen asignado", user_headers, user_rows),
00616|        _sheet("Tickets", "Detalle tickets PGO", ticket_headers, ticket_rows),
00617|        _sheet("Eventos", f"TicketEvento (hasta {evento_cap})", evento_headers, evento_rows),
00618|        _sheet(
00619|            "Explicacion",
00620|            "Proceso PGO",
00621|            ["Tema", "Detalle"],
00622|            [
00623|                ["Fuente productiva", "pgo.Ticket + recalculate_pgo_periodos"],
00624|                ["SLA", "horas ciclo <= sla_horas"],
00625|                ["Clasifica PGO productivo", "No implementada"],
00626|                ["Fuente WCG One", "apps.pgo.* si hay datos"],
00627|            ],
00628|        ),
00629|        *wcg_sheets,
00630|    ]
00631|
00632|    return {
00633|        "md": join_sections(*md_parts),
00634|        "sheets": sheets,
00635|        "stamp": stamp,
00636|        "stamp_label": stamp_label,
00637|        "period": curr_p,
00638|        "prev_period": prev_p,
00639|    }

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiUmVzdWx0YWRvcyBQR08gZXh0ZW5zb3M6IGRhc2hib2FyZCBwcm9kdWN0aXZvICsgYnJvd3NlICsgc3RhY2sgV0NHIE9uZS4iIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmZyb20gZGphbmdvLmRiLm1vZGVscyBpbXBvcnQgQ291bnQsIFEKZnJvbSBkamFuZ28udXRpbHMgaW1wb3J0IHRpbWV6b25lCgpmcm9tIHBnby5tb2RlbHMgaW1wb3J0IFBnb1Jlc3VsdGFkb1BlcmlvZG8sIFRpY2tldCwgVGlja2V0RXZlbnRvCmZyb20gcmVwb3J0cy5tZF91dGlscyBpbXBvcnQgYWlfY2xvc2luZywgYnVsbGV0cywgaDEsIGgyLCBoMywgam9pbl9zZWN0aW9ucywgbWRfdGFibGUsIHAKZnJvbSByZXBvcnRzLm1vZGVscyBpbXBvcnQgUmVwb3J0Q29uZmlnCmZyb20gcmVwb3J0cy5uYW1pbmcgaW1wb3J0IHJlcG9ydF9zdGFtcApmcm9tIHJlcG9ydHMuc2VydmljZXMuY29tbW9uIGltcG9ydCBmbXRfbnVtLCBwY3RfY2hhbmdlCgpQR09fRVhQTEFJTiA9ICIiIgpFbCAqKmRhc2hib2FyZCBQR08gcHJvZHVjdGl2byoqIChgL3Bnby9gKSBzZSBhbGltZW50YSBkZSB0aWNrZXRzIChgcGdvLlRpY2tldGApLgpUcmFzIGxhIGltcG9ydGFjacOzbiAobyBhbCBhYnJpciBlbCBkYXNoYm9hcmQpIHNlIGVqZWN1dGEKYHBnby5wZXJpb2RvLnJlY2FsY3VsYXRlX3Bnb19wZXJpb2Rvc2AsIHF1ZSBsbGVuYSBgUGdvUmVzdWx0YWRvUGVyaW9kb2AgcG9yCnBlcsOtb2RvIChgWVlZWS1NTWAgZGUgYXBlcnR1cmEpIHkgdW5pZGFkIGRlIG5lZ29jaW8gY29uOgoKLSB0aWNrZXRzIGNlcnJhZG9zIC8gYWJpZXJ0b3MKLSB0aWVtcG8gcHJvbWVkaW8gZGUgY2llcnJlIChob3JhcykKLSAlIGN1bXBsaW1pZW50byBTTEE6IGNlcnJhZG9zIGN1eW8gdGllbXBvIOKJpCBgc2xhX2hvcmFzYCBkZWwgdGlja2V0CgoqKk5vKiogaGF5IGVuIGVsIHBpcGVsaW5lIHByb2R1Y3Rpdm8gdW4gY2FtcG8gYENsYXNpZmljYWAgY2FsY3VsYWRvLgpFbCBzdGFjayBXQ0cgT25lIChgYXBwcy5wZ29gKSBwdWVkZSBjb2V4aXN0aXIgY29uIHRpY2tldHMsIGFncmVnYWRvcyBtZW5zdWFsZXMKeSBgUGdvUGVyaW9kU2NvcmUuY2xhc2lmaWNhYCBzaSBleGlzdGVuIGZpbGFzOyBlbCBtb3RvciBkZSBzY29yZSBubyBlc3TDoQpnYXJhbnRpemFkbyBlbiBjw7NkaWdvLgoKRXN0ZSByZXBvcnRlIGluY2x1eWUgKiphbWJhcyBmdWVudGVzKiogY3VhbmRvIGhheSBkYXRvczogdGFibGFzIGRlbCB0YWJsZXJvLApyZXPDum1lbmVzIHBvciB1c3VhcmlvL3VuaWRhZCwgZGV0YWxsZSBicm93c2UgZGUgdGlja2V0cyB5IGVsIGRldGFsbGUgV0NHIE9uZS4KIiIiLnN0cmlwKCkKCgpkZWYgX3NoZWV0KG5hbWUsIHRpdGxlLCBoZWFkZXJzLCByb3dzKToKICAgIHJldHVybiB7Im5hbWUiOiBuYW1lWzozMV0sICJ0aXRsZSI6IHRpdGxlLCAiaGVhZGVycyI6IGhlYWRlcnMsICJyb3dzIjogcm93c30KCgpkZWYgX3djZ19wZ29fYmxvY2soc3RhbXBfbGFiZWw6IHN0cikgLT4gdHVwbGVbbGlzdFtzdHJdLCBsaXN0W2RpY3RdLCBsaXN0W3N0cl0sIGxpc3Rbc3RyXV06CiAgICAiIiJTZWNjaW9uZXMgTUQgKyBzaGVldHMgKyBoZWNob3MgKyB2YWPDrW9zIGRlbCBzdGFjayBhcHBzLnBnby4iIiIKICAgIG1kOiBsaXN0W3N0cl0gPSBbXQogICAgc2hlZXRzOiBsaXN0W2RpY3RdID0gW10KICAgIGhlY2hvczogbGlzdFtzdHJdID0gW10KICAgIHZhY2lvczogbGlzdFtzdHJdID0gW10KICAgIHRyeToKICAgICAgICBmcm9tIGFwcHMucGdvLm1vZGVscyBpbXBvcnQgKAogICAgICAgICAgICBQZ29NZXRyaWNSdWxlLAogICAgICAgICAgICBQZ29Nb250aGx5QWdnLAogICAgICAgICAgICBQZ29QZXJpb2RTY29yZSwKICAgICAgICAgICAgUGdvVGlja2V0LAogICAgICAgICkKICAgICAgICBmcm9tIGFwcHMucGdvLnNlbGVjdG9ycyBpbXBvcnQgdGlja2V0X2Rhc2hib2FyZF9zdW1tYXJ5CiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGV4YzoKICAgICAgICBtZC5hcHBlbmQoaDIoIlN0YWNrIFdDRyBPbmUgUEdPIChgYXBwcy5wZ29gKSIpKQogICAgICAgIG1kLmFwcGVuZChwKGYiX05vIGRpc3BvbmlibGU6IHtleGN9XyIpKQogICAgICAgIHZhY2lvcy5hcHBlbmQoZiJTdGFjayBhcHBzLnBnbyBubyBpbXBvcnRhYmxlOiB7ZXhjfSIpCiAgICAgICAgcmV0dXJuIG1kLCBzaGVldHMsIGhlY2hvcywgdmFjaW9zCgogICAgc3VtbWFyeSA9IHRpY2tldF9kYXNoYm9hcmRfc3VtbWFyeSgpCiAgICBrcGlfaGVhZGVycyA9IFsiS1BJIiwgIlZhbG9yIl0KICAgIGtwaV9yb3dzID0gWwogICAgICAgIFsiVG90YWwgdGlja2V0cyIsIHN1bW1hcnlbInRvdGFsX3RpY2tldHMiXV0sCiAgICAgICAgWyJBYmllcnRvcyIsIHN1bW1hcnlbInRpY2tldHNfYWJpZXJ0b3MiXV0sCiAgICAgICAgWyJDZXJyYWRvcyIsIHN1bW1hcnlbInRpY2tldHNfY2VycmFkb3MiXV0sCiAgICAgICAgWyJWZW5jaWRvcyAoYWJpZXJ0b3MgU0xBIG5vKSIsIHN1bW1hcnlbInRpY2tldHNfdmVuY2lkb3MiXV0sCiAgICAgICAgWyJTTEEgY3VtcGxpZG9zIiwgc3VtbWFyeVsic2xhX2N1bXBsaWRvcyJdXSwKICAgICAgICBbIlNMQSBpbmN1bXBsaWRvcyAoYWJpZXJ0b3MpIiwgc3VtbWFyeVsic2xhX2luY3VtcGxpZG9zIl1dLAogICAgICAgIFsiVGllbXBvIHByb21lZGlvIChoKSIsIGZtdF9udW0oc3VtbWFyeVsidGllbXBvX3Byb21lZGlvIl0sIDIpIGlmIHN1bW1hcnlbInRpZW1wb19wcm9tZWRpbyJdIGlzIG5vdCBOb25lIGVsc2UgIuKAlCJdLAogICAgXQogICAgaGVjaG9zLmFwcGVuZChmIldDRyBPbmUgUGdvVGlja2V0OiB7c3VtbWFyeVsndG90YWxfdGlja2V0cyddfSIpCgogICAgbWQuZXh0ZW5kKAogICAgICAgIFsKICAgICAgICAgICAgaDIoIlN0YWNrIFdDRyBPbmUg4oCUIGRhc2hib2FyZCBLUElzIChgYXBwcy5wZ29gKSIpLAogICAgICAgICAgICBwKAogICAgICAgICAgICAgICAgIkVxdWl2YWxlbnRlIGEgYC93Y2dvbmUvcGdvL2A6IEtQSXMsIGRlc2dsb3NlIHBvciBlc3RhZG8vcHJpb3JpZGFkICIKICAgICAgICAgICAgICAgICJ5IGRldGFsbGUgY29tcGxldG8gZGUgdGlja2V0cyBpbXBvcnRhZG9zIGFsIHNjaGVtYSBXQ0cgT25lLiIKICAgICAgICAgICAgKSwKICAgICAgICAgICAgbWRfdGFibGUoa3BpX2hlYWRlcnMsIGtwaV9yb3dzKSwKICAgICAgICAgICAgaDMoIlBvciBlc3RhZG8gbm9ybWFsaXphZG8iKSwKICAgICAgICAgICAgbWRfdGFibGUoCiAgICAgICAgICAgICAgICBbIkVzdGFkbyIsICJUb3RhbCJdLAogICAgICAgICAgICAgICAgW1tyWyJlc3RhZG9fbm9ybWFsaXphZG8iXSBvciAi4oCUIiwgclsidG90YWwiXV0gZm9yIHIgaW4gc3VtbWFyeVsicG9yX2VzdGFkbyJdXSwKICAgICAgICAgICAgKQogICAgICAgICAgICBpZiBzdW1tYXJ5WyJwb3JfZXN0YWRvIl0KICAgICAgICAgICAgZWxzZSBwKCJfU2luIGRlc2dsb3NlIHBvciBlc3RhZG8uXyIpLAogICAgICAgICAgICBoMygiUG9yIHByaW9yaWRhZCIpLAogICAgICAgICAgICBtZF90YWJsZSgKICAgICAgICAgICAgICAgIFsiUHJpb3JpZGFkIiwgIlRvdGFsIl0sCiAgICAgICAgICAgICAgICBbW3JbInByaW9yaWRhZCJdIG9yICLigJQiLCByWyJ0b3RhbCJdXSBmb3IgciBpbiBzdW1tYXJ5WyJwb3JfcHJpb3JpZGFkIl1dLAogICAgICAgICAgICApCiAgICAgICAgICAgIGlmIHN1bW1hcnlbInBvcl9wcmlvcmlkYWQiXQogICAgICAgICAgICBlbHNlIHAoIl9TaW4gZGVzZ2xvc2UgcG9yIHByaW9yaWRhZC5fIiksCiAgICAgICAgXQogICAgKQogICAgc2hlZXRzLmFwcGVuZChfc2hlZXQoIldDRyBLUEkiLCAiS1BJcyBXQ0cgT25lIFBHTyIsIGtwaV9oZWFkZXJzLCBrcGlfcm93cykpCiAgICBzaGVldHMuYXBwZW5kKAogICAgICAgIF9zaGVldCgKICAgICAgICAgICAgIldDRyBwb3IgZXN0YWRvIiwKICAgICAgICAgICAgIlBnb1RpY2tldCBwb3IgZXN0YWRvIiwKICAgICAgICAgICAgWyJFc3RhZG8iLCAiVG90YWwiXSwKICAgICAgICAgICAgW1tyWyJlc3RhZG9fbm9ybWFsaXphZG8iXSBvciAiIiwgclsidG90YWwiXV0gZm9yIHIgaW4gc3VtbWFyeVsicG9yX2VzdGFkbyJdXSwKICAgICAgICApCiAgICApCiAgICBzaGVldHMuYXBwZW5kKAogICAgICAgIF9zaGVldCgKICAgICAgICAgICAgIldDRyBwb3IgcHJpb3JpZGFkIiwKICAgICAgICAgICAgIlBnb1RpY2tldCBwb3IgcHJpb3JpZGFkIiwKICAgICAgICAgICAgWyJQcmlvcmlkYWQiLCAiVG90YWwiXSwKICAgICAgICAgICAgW1tyWyJwcmlvcmlkYWQiXSBvciAiIiwgclsidG90YWwiXV0gZm9yIHIgaW4gc3VtbWFyeVsicG9yX3ByaW9yaWRhZCJdXSwKICAgICAgICApCiAgICApCgogICAgdGlja2V0X2hlYWRlcnMgPSBbCiAgICAgICAgIklEIGV4dGVybm8iLAogICAgICAgICJUw610dWxvIiwKICAgICAgICAiRXN0YWRvIHJhdyIsCiAgICAgICAgIkVzdGFkbyBub3JtLiIsCiAgICAgICAgIlByaW9yaWRhZCIsCiAgICAgICAgIkRlcGFydGFtZW50byIsCiAgICAgICAgIlNpc3RlbWEiLAogICAgICAgICJQZXJpb2RvIiwKICAgICAgICAiVU4iLAogICAgICAgICJSZXNwb25zYWJsZSIsCiAgICAgICAgIlNvbGljaXRhIiwKICAgICAgICAiQ29ycmVvIiwKICAgICAgICAiVGlwbyIsCiAgICAgICAgIlRpcG8gc2VydmljaW8iLAogICAgICAgICJFbGVtZW50byIsCiAgICAgICAgIlJ1dGEiLAogICAgICAgICJBcGVydHVyYSIsCiAgICAgICAgIkNpZXJyZSIsCiAgICAgICAgIkR1cmFjacOzbiBoIiwKICAgICAgICAiU0xBIGgiLAogICAgICAgICJTTEEgb2siLAogICAgICAgICJTb2x1Y2nDs24iLAogICAgICAgICJSYXrDs24gY2llcnJlIiwKICAgIF0KICAgIHRpY2tldF9yb3dzID0gW10KICAgIGZvciB0IGluIFBnb1RpY2tldC5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJ1bmlkYWRfbmVnb2NpbyIsICJyZXNwb25zYWJsZSIpLm9yZGVyX2J5KAogICAgICAgICItZmVjaGFfYXBlcnR1cmEiLCAidGlja2V0X2V4dGVybm9faWQiCiAgICApOgogICAgICAgIHRpY2tldF9yb3dzLmFwcGVuZCgKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgdC50aWNrZXRfZXh0ZXJub19pZCwKICAgICAgICAgICAgICAgIHQudGl0dWxvIG9yICIiLAogICAgICAgICAgICAgICAgdC5lc3RhZG9fcmF3IG9yICIiLAogICAgICAgICAgICAgICAgdC5lc3RhZG9fbm9ybWFsaXphZG8gb3IgIiIsCiAgICAgICAgICAgICAgICB0LnByaW9yaWRhZCBvciAiIiwKICAgICAgICAgICAgICAgIHQuZGVwYXJ0YW1lbnRvIG9yICIiLAogICAgICAgICAgICAgICAgdC5zaXN0ZW1hIG9yICIiLAogICAgICAgICAgICAgICAgdC5hbmlvX21lcyBvciAiIiwKICAgICAgICAgICAgICAgIHQudW5pZGFkX25lZ29jaW8uY29kZSBpZiB0LnVuaWRhZF9uZWdvY2lvIGVsc2UgIuKAlCIsCiAgICAgICAgICAgICAgICBnZXRhdHRyKHQucmVzcG9uc2FibGUsICJ1c2VybmFtZSIsIE5vbmUpIG9yICLigJQiLAogICAgICAgICAgICAgICAgdC51c3VhcmlvX3NvbGljaXRhIG9yICIiLAogICAgICAgICAgICAgICAgdC5jb3JyZW9fc29saWNpdGEgb3IgIiIsCiAgICAgICAgICAgICAgICB0LnRpcG8gb3IgIiIsCiAgICAgICAgICAgICAgICB0LnRpcG9fc2VydmljaW8gb3IgIiIsCiAgICAgICAgICAgICAgICB0LmVsZW1lbnRvIG9yICIiLAogICAgICAgICAgICAgICAgdC5ydXRhIG9yICIiLAogICAgICAgICAgICAgICAgdC5mZWNoYV9hcGVydHVyYS5pc29mb3JtYXQoKSBpZiB0LmZlY2hhX2FwZXJ0dXJhIGVsc2UgIiIsCiAgICAgICAgICAgICAgICB0LmZlY2hhX2NpZXJyZS5pc29mb3JtYXQoKSBpZiB0LmZlY2hhX2NpZXJyZSBlbHNlICIiLAogICAgICAgICAgICAgICAgZm10X251bSh0LmR1cmFjaW9uX2hvcmFzLCAyKSBpZiB0LmR1cmFjaW9uX2hvcmFzIGlzIG5vdCBOb25lIGVsc2UgIiIsCiAgICAgICAgICAgICAgICB0LnNsYV9ob3JhcyBpZiB0LnNsYV9ob3JhcyBpcyBub3QgTm9uZSBlbHNlICIiLAogICAgICAgICAgICAgICAgIlPDrSIgaWYgdC5zbGFfY3VtcGxpZG8gZWxzZSAoIk5vIiBpZiB0LnNsYV9jdW1wbGlkbyBpcyBGYWxzZSBlbHNlICLigJQiKSwKICAgICAgICAgICAgICAgICh0LnNvbHVjaW9uIG9yICIiKVs6MzAwXSwKICAgICAgICAgICAgICAgICh0LnJhem9uX2NpZXJyZSBvciAiIilbOjE2MF0sCiAgICAgICAgICAgIF0KICAgICAgICApCiAgICBtZC5leHRlbmQoCiAgICAgICAgWwogICAgICAgICAgICBoMigiV0NHIE9uZSDigJQgZGV0YWxsZSBjb21wbGV0byBkZSB0aWNrZXRzIChicm93c2UpIiksCiAgICAgICAgICAgIHAoZiJSZWdpc3Ryb3M6ICoqe2xlbih0aWNrZXRfcm93cyl9KiouIEV4cG9ydGFibGVzIHRhbWJpw6luIGVuIEV4Y2VsLiIpLAogICAgICAgICAgICBtZF90YWJsZSh0aWNrZXRfaGVhZGVycywgdGlja2V0X3Jvd3MpIGlmIHRpY2tldF9yb3dzIGVsc2UgcCgiX1NpbiBQZ29UaWNrZXQuXyIpLAogICAgICAgIF0KICAgICkKICAgIHNoZWV0cy5hcHBlbmQoX3NoZWV0KCJXQ0cgVGlja2V0cyIsICJQZ29UaWNrZXQgZGV0YWxsZSIsIHRpY2tldF9oZWFkZXJzLCB0aWNrZXRfcm93cykpCiAgICBpZiBub3QgdGlja2V0X3Jvd3M6CiAgICAgICAgdmFjaW9zLmFwcGVuZCgiU2luIFBnb1RpY2tldCBlbiBhcHBzLnBnbyAoaW1wb3J0YXIgdGlja2V0cyBXQ0cgT25lKS4iKQoKICAgIHNjb3JlX2hlYWRlcnMgPSBbCiAgICAgICAgIlBlcmlvZG8iLAogICAgICAgICLDgXJlYSIsCiAgICAgICAgIlVOIiwKICAgICAgICAiVXN1YXJpbyIsCiAgICAgICAgIlB1bnRhamUiLAogICAgICAgICJDbGFzaWZpY2EiLAogICAgICAgICJGZWNoYSBjw6FsY3VsbyIsCiAgICAgICAgIkRldGFsbGUgSlNPTiIsCiAgICBdCiAgICBzY29yZV9yb3dzID0gW10KICAgIGZvciBzIGluIFBnb1BlcmlvZFNjb3JlLm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoInVuaWRhZF9uZWdvY2lvIiwgInVzdWFyaW8iKS5vcmRlcl9ieSgKICAgICAgICAiLXBlcmlvZG8iLCAiYXJlYSIKICAgICk6CiAgICAgICAgc2NvcmVfcm93cy5hcHBlbmQoCiAgICAgICAgICAgIFsKICAgICAgICAgICAgICAgIHMucGVyaW9kbywKICAgICAgICAgICAgICAgIHMuYXJlYSBvciAiIiwKICAgICAgICAgICAgICAgIHN0cihzLnVuaWRhZF9uZWdvY2lvKSBpZiBzLnVuaWRhZF9uZWdvY2lvIGVsc2UgIuKAlCIsCiAgICAgICAgICAgICAgICBzdHIocy51c3VhcmlvKSBpZiBzLnVzdWFyaW8gZWxzZSAi4oCUIiwKICAgICAgICAgICAgICAgIGZtdF9udW0ocy5wdW50YWplX3RvdGFsLCAyKSwKICAgICAgICAgICAgICAgICJTw60iIGlmIHMuY2xhc2lmaWNhIGVsc2UgIk5vIiwKICAgICAgICAgICAgICAgIHMuZmVjaGFfY2FsY3Vsby5pc29mb3JtYXQoKSBpZiBnZXRhdHRyKHMsICJmZWNoYV9jYWxjdWxvIiwgTm9uZSkgZWxzZSAiIiwKICAgICAgICAgICAgICAgIHN0cihzLmRldGFsbGVfanNvbiBvciAiIilbOjQwMF0sCiAgICAgICAgICAgIF0KICAgICAgICApCiAgICBtZC5leHRlbmQoCiAgICAgICAgWwogICAgICAgICAgICBoMigiV0NHIE9uZSDigJQgcmVzdWx0YWRvcyAvIFBnb1BlcmlvZFNjb3JlIiksCiAgICAgICAgICAgIHAoCiAgICAgICAgICAgICAgICAiVGFibGEgZGUgYC93Y2dvbmUvcGdvL3Jlc3VsdGFkb3MvYC4gKipDbGFzaWZpY2EqKiBzb2xvIHNpIGhheSBmaWxhczsgIgogICAgICAgICAgICAgICAgIm5vIGludmVudGFyIHVtYnJhbGVzIHNpIGVsIHB1bnRhamUgbm8gZXN0w6EgY2FsY3VsYWRvIGVuIGPDs2RpZ28uIgogICAgICAgICAgICApLAogICAgICAgICAgICBtZF90YWJsZShzY29yZV9oZWFkZXJzLCBzY29yZV9yb3dzKQogICAgICAgICAgICBpZiBzY29yZV9yb3dzCiAgICAgICAgICAgIGVsc2UgcCgiX1NpbiBQZ29QZXJpb2RTY29yZS5fIiksCiAgICAgICAgXQogICAgKQogICAgc2hlZXRzLmFwcGVuZChfc2hlZXQoIldDRyBTY29yZXMiLCAiUGdvUGVyaW9kU2NvcmUiLCBzY29yZV9oZWFkZXJzLCBzY29yZV9yb3dzKSkKICAgIGhlY2hvcy5hcHBlbmQoZiJXQ0cgT25lIFBnb1BlcmlvZFNjb3JlOiB7bGVuKHNjb3JlX3Jvd3MpfSIpCiAgICBpZiBub3Qgc2NvcmVfcm93czoKICAgICAgICB2YWNpb3MuYXBwZW5kKCJTaW4gUGdvUGVyaW9kU2NvcmUgKHNjb3JpbmcgV0NHIE9uZSB2YWPDrW8gbyBubyBjYWxjdWxhZG8pLiIpCgogICAgYWdnX2hlYWRlcnMgPSBbCiAgICAgICAgIlBlcmlvZG8iLAogICAgICAgICJVTiIsCiAgICAgICAgIkRlcGFydGFtZW50byIsCiAgICAgICAgIlJlY2liaWRvcyIsCiAgICAgICAgIkNlcnJhZG9zIiwKICAgICAgICAiQWJpZXJ0b3MgZmluIG1lcyIsCiAgICAgICAgIlRpZW1wbyBwcm9tLiBoIiwKICAgICAgICAiU0xBIG9rIiwKICAgICAgICAiU0xBIG5vIiwKICAgIF0KICAgIGFnZ19yb3dzID0gW10KICAgIGZvciBhIGluIFBnb01vbnRobHlBZ2cub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgidW5pZGFkX25lZ29jaW8iKS5vcmRlcl9ieSgKICAgICAgICAiLXBlcmlvZG8iLCAidW5pZGFkX25lZ29jaW9fX25vbWJyZSIKICAgICk6CiAgICAgICAgYWdnX3Jvd3MuYXBwZW5kKAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICBhLnBlcmlvZG8sCiAgICAgICAgICAgICAgICBzdHIoYS51bmlkYWRfbmVnb2NpbykgaWYgYS51bmlkYWRfbmVnb2NpbyBlbHNlICLigJQiLAogICAgICAgICAgICAgICAgYS5kZXBhcnRhbWVudG8gb3IgIiIsCiAgICAgICAgICAgICAgICBhLnRpY2tldHNfcmVjaWJpZG9zLAogICAgICAgICAgICAgICAgYS50aWNrZXRzX2NlcnJhZG9zLAogICAgICAgICAgICAgICAgYS50aWNrZXRzX2FiaWVydG9zX2Zpbl9tZXMsCiAgICAgICAgICAgICAgICBmbXRfbnVtKGEudGllbXBvX3Byb21lZGlvX2hvcmFzLCAyKSBpZiBhLnRpZW1wb19wcm9tZWRpb19ob3JhcyBpcyBub3QgTm9uZSBlbHNlICIiLAogICAgICAgICAgICAgICAgYS5zbGFfY3VtcGxpZG9zLAogICAgICAgICAgICAgICAgYS5zbGFfaW5jdW1wbGlkb3MsCiAgICAgICAgICAgIF0KICAgICAgICApCiAgICBtZC5leHRlbmQoCiAgICAgICAgWwogICAgICAgICAgICBoMigiV0NHIE9uZSDigJQgYWdyZWdhZG9zIG1lbnN1YWxlcyAoUGdvTW9udGhseUFnZykiKSwKICAgICAgICAgICAgbWRfdGFibGUoYWdnX2hlYWRlcnMsIGFnZ19yb3dzKSBpZiBhZ2dfcm93cyBlbHNlIHAoIl9TaW4gUGdvTW9udGhseUFnZy5fIiksCiAgICAgICAgXQogICAgKQogICAgc2hlZXRzLmFwcGVuZChfc2hlZXQoIldDRyBBZ2cgbWVuc3VhbCIsICJQZ29Nb250aGx5QWdnIiwgYWdnX2hlYWRlcnMsIGFnZ19yb3dzKSkKCiAgICBydWxlX2hlYWRlcnMgPSBbCiAgICAgICAgIkPDs2RpZ28iLAogICAgICAgICLDgXJlYSIsCiAgICAgICAgIlZhcmlhYmxlIiwKICAgICAgICAiUHVudG9zIiwKICAgICAgICAiUGVzbyIsCiAgICAgICAgIlRpcG8gcmVnbGEiLAogICAgICAgICJBY3Rpdm8iLAogICAgICAgICJGw7NybXVsYSIsCiAgICAgICAgIk5vdGFzIiwKICAgIF0KICAgIHJ1bGVfcm93cyA9IFtdCiAgICBmb3IgciBpbiBQZ29NZXRyaWNSdWxlLm9iamVjdHMub3JkZXJfYnkoImFyZWEiLCAiY29kaWdvIik6CiAgICAgICAgcnVsZV9yb3dzLmFwcGVuZCgKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgci5jb2RpZ28sCiAgICAgICAgICAgICAgICByLmFyZWEgb3IgIiIsCiAgICAgICAgICAgICAgICByLnZhcmlhYmxlIG9yICIiLAogICAgICAgICAgICAgICAgZm10X251bShyLnB1bnRvcywgMikgaWYgci5wdW50b3MgaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICAgICAgICAgIGZtdF9udW0oci5wZXNvLCAyKSBpZiByLnBlc28gaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICAgICAgICAgIHIudGlwb19yZWdsYSBvciAiIiwKICAgICAgICAgICAgICAgICJTw60iIGlmIHIuYWN0aXZvIGVsc2UgIk5vIiwKICAgICAgICAgICAgICAgIChyLmZvcm11bGFfdGV4dG8gb3IgIiIpWzoyMDBdLAogICAgICAgICAgICAgICAgKHIubm90YXMgb3IgIiIpWzoxNjBdLAogICAgICAgICAgICBdCiAgICAgICAgKQogICAgbWQuZXh0ZW5kKAogICAgICAgIFsKICAgICAgICAgICAgaDIoIldDRyBPbmUg4oCUIGNhdMOhbG9nbyBkZSByZWdsYXMgZGUgbcOpdHJpY2EiKSwKICAgICAgICAgICAgbWRfdGFibGUocnVsZV9oZWFkZXJzLCBydWxlX3Jvd3MpCiAgICAgICAgICAgIGlmIHJ1bGVfcm93cwogICAgICAgICAgICBlbHNlIHAoIl9TaW4gUGdvTWV0cmljUnVsZS5fIiksCiAgICAgICAgXQogICAgKQogICAgc2hlZXRzLmFwcGVuZChfc2hlZXQoIldDRyBSZWdsYXMiLCAiUGdvTWV0cmljUnVsZSIsIHJ1bGVfaGVhZGVycywgcnVsZV9yb3dzKSkKICAgIHJldHVybiBtZCwgc2hlZXRzLCBoZWNob3MsIHZhY2lvcwoKCmRlZiBidWlsZF9wZ29fcmVzdWx0cyhjZmc6IFJlcG9ydENvbmZpZyB8IE5vbmUgPSBOb25lKSAtPiBkaWN0OgogICAgY2ZnID0gY2ZnIG9yIFJlcG9ydENvbmZpZy5nZXRfYWN0aXZlKCkKICAgIG5vdyA9IHRpbWV6b25lLmxvY2FsdGltZSgpCiAgICBzdGFtcCA9IHJlcG9ydF9zdGFtcChub3cpCiAgICBzdGFtcF9sYWJlbCA9ICgKICAgICAgICBmIkdlbmVyYWRvIHtub3cuc3RyZnRpbWUoJyVZLSVtLSVkICVIOiVNJyl9ICIKICAgICAgICBmIih7dGltZXpvbmUuZ2V0X2N1cnJlbnRfdGltZXpvbmVfbmFtZSgpfSkgwrd7c3RhbXB9IgogICAgKQoKICAgICMgLS0tLS0gS1BJIHRhYmxlcm8gcHJvZHVjdGl2byAtLS0tLQogICAgcmVjaWJpZG9zID0gVGlja2V0Lm9iamVjdHMuY291bnQoKQogICAgYWJpZXJ0b3MgPSBUaWNrZXQub2JqZWN0cy5maWx0ZXIoCiAgICAgICAgZXN0YWRvX19pbj1bIkFCSUVSVE8iLCAiRU5fUFJPQ0VTTyJdCiAgICApLmNvdW50KCkKICAgIGNlcnJhZG9zID0gVGlja2V0Lm9iamVjdHMuZmlsdGVyKGVzdGFkbz0iQ0VSUkFETyIpLmNvdW50KCkKICAgIGtwaV9oZWFkZXJzID0gWyJLUEkgZGFzaGJvYXJkIC9wZ28vIiwgIlZhbG9yIl0KICAgIGtwaV9yb3dzID0gWwogICAgICAgIFsiUmVjaWJpZG9zICh0b3RhbCkiLCByZWNpYmlkb3NdLAogICAgICAgIFsiQWJpZXJ0b3MgKEFCSUVSVE8rRU5fUFJPQ0VTTykiLCBhYmllcnRvc10sCiAgICAgICAgWyJDZXJyYWRvcyIsIGNlcnJhZG9zXSwKICAgIF0KCiAgICByZXN1bHRhZG9zID0gbGlzdCgKICAgICAgICBQZ29SZXN1bHRhZG9QZXJpb2RvLm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoInVuaWRhZF9uZWdvY2lvIikub3JkZXJfYnkoCiAgICAgICAgICAgICJwZXJpb2RvIiwgInVuaWRhZF9uZWdvY2lvX19ub21icmUiCiAgICAgICAgKQogICAgKQogICAgcmVzX2hlYWRlcnMgPSBbCiAgICAgICAgIlBlcmlvZG8iLAogICAgICAgICJVbmlkYWQiLAogICAgICAgICJDw7NkaWdvIFVOIiwKICAgICAgICAiQ2VycmFkb3MiLAogICAgICAgICJBYmllcnRvcyIsCiAgICAgICAgIlRpZW1wbyBwcm9tLiBoIiwKICAgICAgICAiU0xBICUiLAogICAgXQogICAgcmVzX3Jvd3MgPSBbXQogICAgZm9yIHIgaW4gcmVzdWx0YWRvczoKICAgICAgICByZXNfcm93cy5hcHBlbmQoCiAgICAgICAgICAgIFsKICAgICAgICAgICAgICAgIHIucGVyaW9kbywKICAgICAgICAgICAgICAgIHIudW5pZGFkX25lZ29jaW8ubm9tYnJlIGlmIHIudW5pZGFkX25lZ29jaW8gZWxzZSAi4oCUIiwKICAgICAgICAgICAgICAgIHIudW5pZGFkX25lZ29jaW8uY29kZSBpZiByLnVuaWRhZF9uZWdvY2lvIGVsc2UgIuKAlCIsCiAgICAgICAgICAgICAgICByLnRpY2tldHNfY2VycmFkb3MsCiAgICAgICAgICAgICAgICByLnRpY2tldHNfYWJpZXJ0b3MsCiAgICAgICAgICAgICAgICBmbXRfbnVtKHIudGllbXBvX3Byb21lZGlvX2hvcmFzLCAyKSwKICAgICAgICAgICAgICAgIGZtdF9udW0oci5jdW1wbGltaWVudG9fc2xhX3BjdCwgMiksCiAgICAgICAgICAgIF0KICAgICAgICApCgogICAgIyBTZXJpZSBkZSBjaWZyYXMgYmFzZSAoZXF1aXZhbGVudGUgYSDigJxjaGFydHPigJ0pOiBwb3IgcGVyw61vZG8gdG90YWxlcwogICAgc2VyaWVfaGVhZGVycyA9IFsKICAgICAgICAiUGVyaW9kbyIsCiAgICAgICAgIkNlcnJhZG9zIiwKICAgICAgICAiQWJpZXJ0b3MiLAogICAgICAgICJTTEEgJSBwb25kZXJhZG8gKHByb21lZGlvIHNpbXBsZSBVTikiLAogICAgICAgICJUaWVtcG8gcHJvbS4gaCAocHJvbWVkaW8gc2ltcGxlIFVOKSIsCiAgICBdCiAgICBzZXJpZV9yb3dzID0gW10KICAgIGJ5X3BlcmlvZDogZGljdFtzdHIsIGxpc3RdID0ge30KICAgIGZvciByIGluIHJlc3VsdGFkb3M6CiAgICAgICAgYnlfcGVyaW9kLnNldGRlZmF1bHQoci5wZXJpb2RvLCBbXSkuYXBwZW5kKHIpCiAgICBmb3IgcGVyaW9kbyBpbiBzb3J0ZWQoYnlfcGVyaW9kKToKICAgICAgICByb3dzX3AgPSBieV9wZXJpb2RbcGVyaW9kb10KICAgICAgICBuID0gbGVuKHJvd3NfcCkgb3IgMQogICAgICAgIHNlcmllX3Jvd3MuYXBwZW5kKAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICBwZXJpb2RvLAogICAgICAgICAgICAgICAgc3VtKHgudGlja2V0c19jZXJyYWRvcyBmb3IgeCBpbiByb3dzX3ApLAogICAgICAgICAgICAgICAgc3VtKHgudGlja2V0c19hYmllcnRvcyBmb3IgeCBpbiByb3dzX3ApLAogICAgICAgICAgICAgICAgZm10X251bShzdW0oZmxvYXQoeC5jdW1wbGltaWVudG9fc2xhX3BjdCBvciAwKSBmb3IgeCBpbiByb3dzX3ApIC8gbiwgMiksCiAgICAgICAgICAgICAgICBmbXRfbnVtKHN1bShmbG9hdCh4LnRpZW1wb19wcm9tZWRpb19ob3JhcyBvciAwKSBmb3IgeCBpbiByb3dzX3ApIC8gbiwgMiksCiAgICAgICAgICAgIF0KICAgICAgICApCgogICAgcGVyaW9kb3MgPSBzb3J0ZWQoe3IucGVyaW9kbyBmb3IgciBpbiByZXN1bHRhZG9zfSkKICAgIGN1cnJfcCA9IHBlcmlvZG9zWy0xXSBpZiBwZXJpb2RvcyBlbHNlIE5vbmUKICAgIHByZXZfcCA9IHBlcmlvZG9zWy0yXSBpZiBsZW4ocGVyaW9kb3MpID4gMSBlbHNlIE5vbmUKICAgIGNhbWJpb3MgPSBbXQogICAgaWYgY3Vycl9wIGFuZCBwcmV2X3A6CiAgICAgICAgcHJldl9tYXAgPSB7ci51bmlkYWRfbmVnb2Npb19pZDogciBmb3IgciBpbiByZXN1bHRhZG9zIGlmIHIucGVyaW9kbyA9PSBwcmV2X3B9CiAgICAgICAgZm9yIHIgaW4gW3ggZm9yIHggaW4gcmVzdWx0YWRvcyBpZiB4LnBlcmlvZG8gPT0gY3Vycl9wXToKICAgICAgICAgICAgcHJ2ID0gcHJldl9tYXAuZ2V0KHIudW5pZGFkX25lZ29jaW9faWQpCiAgICAgICAgICAgIGlmIG5vdCBwcnY6CiAgICAgICAgICAgICAgICBjb250aW51ZQogICAgICAgICAgICBjYW1iaW9zLmFwcGVuZCgKICAgICAgICAgICAgICAgIGYie3IudW5pZGFkX25lZ29jaW8uY29kZSBpZiByLnVuaWRhZF9uZWdvY2lvIGVsc2UgJz8nfTogIgogICAgICAgICAgICAgICAgZiJTTEEge2ZtdF9udW0ocHJ2LmN1bXBsaW1pZW50b19zbGFfcGN0LCAyKX0l4oaSe2ZtdF9udW0oci5jdW1wbGltaWVudG9fc2xhX3BjdCwgMil9JSAiCiAgICAgICAgICAgICAgICBmIih7cGN0X2NoYW5nZShyLmN1bXBsaW1pZW50b19zbGFfcGN0LCBwcnYuY3VtcGxpbWllbnRvX3NsYV9wY3QpfSk7ICIKICAgICAgICAgICAgICAgIGYiY2VycmFkb3Mge3Bydi50aWNrZXRzX2NlcnJhZG9zfeKGkntyLnRpY2tldHNfY2VycmFkb3N9OyAiCiAgICAgICAgICAgICAgICBmImFiaWVydG9zIHtwcnYudGlja2V0c19hYmllcnRvc33ihpJ7ci50aWNrZXRzX2FiaWVydG9zfSIKICAgICAgICAgICAgKQoKICAgICMgUmVzdW1lbiBwb3IgdXN1YXJpbyAoY29tbyAvcGdvL3Jlc3VtZW4vdXN1YXJpby8pCiAgICB1c2VyX2hlYWRlcnMgPSBbIlVzdWFyaW8gYXNpZ25hZG8iLCAiVG90YWwgdGlja2V0cyIsICJBYmllcnRvcyJdCiAgICB1c2VyX3Jvd3MgPSBbXQogICAgZm9yIHJvdyBpbiAoCiAgICAgICAgVGlja2V0Lm9iamVjdHMudmFsdWVzKCJhc2lnbmFkb19hX191c2VybmFtZSIpCiAgICAgICAgLmFubm90YXRlKAogICAgICAgICAgICB0b3RhbD1Db3VudCgiaWQiKSwKICAgICAgICAgICAgYWJpZXJ0b3Nfbj1Db3VudCgiaWQiLCBmaWx0ZXI9UShlc3RhZG89IkFCSUVSVE8iKSksCiAgICAgICAgKQogICAgICAgIC5vcmRlcl9ieSgiLXRvdGFsIikKICAgICk6CiAgICAgICAgdXNlcl9yb3dzLmFwcGVuZCgKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgcm93WyJhc2lnbmFkb19hX191c2VybmFtZSJdIG9yICIoc2luIGFzaWduYXIpIiwKICAgICAgICAgICAgICAgIHJvd1sidG90YWwiXSwKICAgICAgICAgICAgICAgIHJvd1siYWJpZXJ0b3NfbiJdLAogICAgICAgICAgICBdCiAgICAgICAgKQoKICAgICMgUmVzdW1lbiBwb3IgdW5pZGFkCiAgICB1bl9oZWFkZXJzID0gWyJDw7NkaWdvIFVOIiwgIk5vbWJyZSIsICJUb3RhbCB0aWNrZXRzIl0KICAgIHVuX3Jvd3MgPSBbXQogICAgZm9yIHJvdyBpbiAoCiAgICAgICAgVGlja2V0Lm9iamVjdHMudmFsdWVzKCJ1bmlkYWRfbmVnb2Npb19fY29kZSIsICJ1bmlkYWRfbmVnb2Npb19fbm9tYnJlIikKICAgICAgICAuYW5ub3RhdGUodG90YWw9Q291bnQoImlkIikpCiAgICAgICAgLm9yZGVyX2J5KCItdG90YWwiKQogICAgKToKICAgICAgICB1bl9yb3dzLmFwcGVuZCgKICAgICAgICAgICAgWwogICAgICAgICAgICAgICAgcm93WyJ1bmlkYWRfbmVnb2Npb19fY29kZSJdIG9yICLigJQiLAogICAgICAgICAgICAgICAgcm93WyJ1bmlkYWRfbmVnb2Npb19fbm9tYnJlIl0gb3IgIuKAlCIsCiAgICAgICAgICAgICAgICByb3dbInRvdGFsIl0sCiAgICAgICAgICAgIF0KICAgICAgICApCgogICAgYnlfZXN0YWRvID0gbGlzdCgKICAgICAgICBUaWNrZXQub2JqZWN0cy52YWx1ZXMoImVzdGFkbyIpLmFubm90YXRlKG49Q291bnQoImlkIikpLm9yZGVyX2J5KCJlc3RhZG8iKQogICAgKQogICAgYnlfcHJpbyA9IGxpc3QoCiAgICAgICAgVGlja2V0Lm9iamVjdHMudmFsdWVzKCJwcmlvcmlkYWQiKS5hbm5vdGF0ZShuPUNvdW50KCJpZCIpKS5vcmRlcl9ieSgicHJpb3JpZGFkIikKICAgICkKCiAgICB0aWNrZXRfaGVhZGVycyA9IFsKICAgICAgICAiQ8OzZGlnbyIsCiAgICAgICAgIlTDrXR1bG8iLAogICAgICAgICJEZXNjcmlwY2nDs24iLAogICAgICAgICJFc3RhZG8iLAogICAgICAgICJQcmlvcmlkYWQiLAogICAgICAgICJVTiIsCiAgICAgICAgIkVudGlkYWQiLAogICAgICAgICJBc2lnbmFkbyIsCiAgICAgICAgIkFwZXJ0dXJhIiwKICAgICAgICAiQ2llcnJlIiwKICAgICAgICAiU0xBIGhvcmFzIiwKICAgICAgICAiSG9yYXMgY2ljbG8iLAogICAgICAgICJTTEEgb2siLAogICAgICAgICJDcmVhZG8iLAogICAgICAgICJBY3R1YWxpemFkbyIsCiAgICBdCiAgICB0aWNrZXRfcm93cyA9IFtdCiAgICBmb3IgdCBpbiBUaWNrZXQub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgKICAgICAgICAidW5pZGFkX25lZ29jaW8iLCAiZW50aWRhZCIsICJhc2lnbmFkb19hIgogICAgKS5vcmRlcl9ieSgiLWZlY2hhX2FwZXJ0dXJhIiwgImNvZGlnbyIpOgogICAgICAgIGhvcmFzID0gIiIKICAgICAgICBzbGFfb2sgPSAiIgogICAgICAgIGlmIHQuZmVjaGFfYXBlcnR1cmEgYW5kIHQuZmVjaGFfY2llcnJlOgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICBkZWx0YSA9IHQuZmVjaGFfY2llcnJlIC0gdC5mZWNoYV9hcGVydHVyYQogICAgICAgICAgICAgICAgaG9yYXNfdmFsID0gcm91bmQoZGVsdGEudG90YWxfc2Vjb25kcygpIC8gMzYwMCwgc289MikKICAgICAgICAgICAgICAgIGhvcmFzID0gaG9yYXNfdmFsCiAgICAgICAgICAgICAgICBzbGFfb2sgPSAiU8OtIiBpZiBob3Jhc192YWwgPD0gZmxvYXQodC5zbGFfaG9yYXMgb3IgMCkgZWxzZSAiTm8iCiAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgICAgICAgICBwYXNzCiAgICAgICAgdGlja2V0X3Jvd3MuYXBwZW5kKAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICB0LmNvZGlnbywKICAgICAgICAgICAgICAgIHQudGl0dWxvIG9yICIiLAogICAgICAgICAgICAgICAgdC5kZXNjcmlwY2lvbiBvciAiIiwKICAgICAgICAgICAgICAgIHQuZXN0YWRvLAogICAgICAgICAgICAgICAgdC5wcmlvcmlkYWQsCiAgICAgICAgICAgICAgICB0LnVuaWRhZF9uZWdvY2lvLmNvZGUgaWYgdC51bmlkYWRfbmVnb2NpbyBlbHNlICLigJQiLAogICAgICAgICAgICAgICAgZ2V0YXR0cih0LmVudGlkYWQsICJjb2RpZ28iLCBOb25lKQogICAgICAgICAgICAgICAgb3IgZ2V0YXR0cih0LmVudGlkYWQsICJub21icmUiLCBOb25lKQogICAgICAgICAgICAgICAgb3IgIuKAlCIsCiAgICAgICAgICAgICAgICBnZXRhdHRyKHQuYXNpZ25hZG9fYSwgInVzZXJuYW1lIiwgTm9uZSkgb3IgIuKAlCIsCiAgICAgICAgICAgICAgICB0LmZlY2hhX2FwZXJ0dXJhLmlzb2Zvcm1hdCgpIGlmIHQuZmVjaGFfYXBlcnR1cmEgZWxzZSAiIiwKICAgICAgICAgICAgICAgIHQuZmVjaGFfY2llcnJlLmlzb2Zvcm1hdCgpIGlmIHQuZmVjaGFfY2llcnJlIGVsc2UgIiIsCiAgICAgICAgICAgICAgICB0LnNsYV9ob3JhcywKICAgICAgICAgICAgICAgIGhvcmFzLAogICAgICAgICAgICAgICAgc2xhX29rLAogICAgICAgICAgICAgICAgdC5jcmVhdGVkX2F0Lmlzb2Zvcm1hdCgpIGlmIHQuY3JlYXRlZF9hdCBlbHNlICIiLAogICAgICAgICAgICAgICAgdC51cGRhdGVkX2F0Lmlzb2Zvcm1hdCgpIGlmIHQudXBkYXRlZF9hdCBlbHNlICIiLAogICAgICAgICAgICBdCiAgICAgICAgKQoKICAgIGV2ZW50b19oZWFkZXJzID0gWyJUaWNrZXQiLCAiVGlwbyIsICJGZWNoYSIsICJVc3VhcmlvIiwgIkRlc2NyaXBjacOzbiJdCiAgICBldmVudG9fcm93cyA9IFtdCiAgICBldmVudG9fY2FwID0gNTAwMAogICAgZm9yIGUgaW4gKAogICAgICAgIFRpY2tldEV2ZW50by5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJ0aWNrZXQiLCAidXN1YXJpbyIpCiAgICAgICAgLm9yZGVyX2J5KCItZmVjaGEiKVs6ZXZlbnRvX2NhcF0KICAgICk6CiAgICAgICAgZXZlbnRvX3Jvd3MuYXBwZW5kKAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICBlLnRpY2tldC5jb2RpZ28gaWYgZS50aWNrZXQgZWxzZSAi4oCUIiwKICAgICAgICAgICAgICAgIGUudGlwbywKICAgICAgICAgICAgICAgIGUuZmVjaGEuaXNvZm9ybWF0KCkgaWYgZS5mZWNoYSBlbHNlICIiLAogICAgICAgICAgICAgICAgZ2V0YXR0cihlLnVzdWFyaW8sICJ1c2VybmFtZSIsIE5vbmUpIG9yICLigJQiLAogICAgICAgICAgICAgICAgZS5kZXNjcmlwY2lvbiBvciAiIiwKICAgICAgICAgICAgXQogICAgICAgICkKICAgIGV2ZW50b190b3RhbCA9IFRpY2tldEV2ZW50by5vYmplY3RzLmNvdW50KCkKCiAgICB3Y2dfbWQsIHdjZ19zaGVldHMsIHdjZ19oZWNob3MsIHdjZ192YWNpb3MgPSBfd2NnX3Bnb19ibG9jayhzdGFtcF9sYWJlbCkKCiAgICBoZWNob3MgPSBbCiAgICAgICAgZiJUaWNrZXRzIHByb2R1Y3Rpdm86IHtyZWNpYmlkb3N9IiwKICAgICAgICBmIkFiaWVydG9zOiB7YWJpZXJ0b3N9IMK3IENlcnJhZG9zOiB7Y2VycmFkb3N9IiwKICAgICAgICBmIkZpbGFzIFBnb1Jlc3VsdGFkb1BlcmlvZG86IHtsZW4ocmVzX3Jvd3MpfSIsCiAgICAgICAgZiJQZXLDrW9kbyDDumx0aW1vIHJlc3VsdGFkb3M6IHtjdXJyX3Agb3IgJ24vZCd9IiwKICAgICAgICBmIlBlcsOtb2RvIGFudGVyaW9yOiB7cHJldl9wIG9yICduL2QnfSIsCiAgICAgICAgZiJFdmVudG9zIGxpc3RhZG9zOiB7bGVuKGV2ZW50b19yb3dzKX0gZGUge2V2ZW50b190b3RhbH0iLAogICAgICAgICp3Y2dfaGVjaG9zLAogICAgXQogICAgdmFjaW9zID0gbGlzdCh3Y2dfdmFjaW9zKQogICAgaWYgbm90IHRpY2tldF9yb3dzOgogICAgICAgIHZhY2lvcy5hcHBlbmQoIlNpbiB0aWNrZXRzIGVuIHBnby5UaWNrZXQuIikKICAgIGlmIG5vdCByZXNfcm93czoKICAgICAgICB2YWNpb3MuYXBwZW5kKCJTaW4gUGdvUmVzdWx0YWRvUGVyaW9kbyAoaW1wb3J0YXIgdGlja2V0cyAvIHJlY2FsY3VsYXIgcGVyw61vZG9zKS4iKQogICAgaWYgZXZlbnRvX3RvdGFsID4gZXZlbnRvX2NhcDoKICAgICAgICB2YWNpb3MuYXBwZW5kKAogICAgICAgICAgICBmIlRpY2tldEV2ZW50byB0cnVuY2FkbyBhIHtldmVudG9fY2FwfSBmaWxhcyBtw6FzIHJlY2llbnRlcyAoaGF5IHtldmVudG9fdG90YWx9KS4iCiAgICAgICAgKQoKICAgIG1kX3BhcnRzID0gWwogICAgICAgIGgxKCJSZXBvcnRlIGRlIHJlc3VsdGFkb3MgUEdPIChleHRlbnNvKSIpLAogICAgICAgIHAoc3RhbXBfbGFiZWwpLAogICAgICAgIHAoCiAgICAgICAgICAgICJQcm9ww7NzaXRvOiBkYXRvcyBvcGVyYXRpdm9zIGNvbXBsZXRvcyBkZSBQR08gcGFyYSBhbsOhbGlzaXMgZXN0cmF0w6lnaWNvICIKICAgICAgICAgICAgInBvciBJQSB5IGV4cG9ydGFjacOzbiBFeGNlbCBodW1hbmEuIENSTSBubyBzZSBpbmNsdXllLiIKICAgICAgICApLAogICAgICAgIGgyKCJDw7NtbyBzZSBwcm9jZXNhIFBHTyIpLAogICAgICAgIHAoUEdPX0VYUExBSU4pLAogICAgICAgIGgyKCJEYXNoYm9hcmQgcHJvZHVjdGl2byDigJQgS1BJcyIpLAogICAgICAgIG1kX3RhYmxlKGtwaV9oZWFkZXJzLCBrcGlfcm93cyksCiAgICAgICAgaDIoIkRhc2hib2FyZCDigJQgcmVzdWx0YWRvcyBwb3IgcGVyw61vZG8geSB1bmlkYWQiKSwKICAgICAgICBwKAogICAgICAgICAgICAiVGFibGEgZGVsIHRhYmxlcm8gYC9wZ28vYCAoYFBnb1Jlc3VsdGFkb1BlcmlvZG9gKS4gU2VudGlkbzogbWVkaXIgIgogICAgICAgICAgICAiY2FyZ2EgeSBjdW1wbGltaWVudG8gU0xBIHBvciBVTiB5IG1lcyBkZSBhcGVydHVyYSBkZWwgdGlja2V0LiIKICAgICAgICApLAogICAgICAgIHAoZiJGaWxhczogKip7bGVuKHJlc19yb3dzKX0qKi4iKSwKICAgICAgICBtZF90YWJsZShyZXNfaGVhZGVycywgcmVzX3Jvd3MpIGlmIHJlc19yb3dzIGVsc2UgcCgiX1NpbiByZXN1bHRhZG9zIGRlIHBlcsOtb2RvLl8iKSwKICAgICAgICBoMigiQ2lmcmFzIGJhc2UgcG9yIHBlcsOtb2RvIChzZXJpZSBwYXJhIGFuw6FsaXNpcyAvIGdyw6FmaWNvcykiKSwKICAgICAgICBwKAogICAgICAgICAgICAiQWdyZWdhZG9zIHBvciBwZXLDrW9kbyBhIHBhcnRpciBkZSBsYSB0YWJsYSBkZSByZXN1bHRhZG9zIOKAlCDDunRpbGVzIHBhcmEgIgogICAgICAgICAgICAiY29uc3RydWlyIHRlbmRlbmNpYXMgZGUgdm9sdW1lbiB5IFNMQSBlbiBFeGNlbCBvIHBvciBJQS4iCiAgICAgICAgKSwKICAgICAgICBtZF90YWJsZShzZXJpZV9oZWFkZXJzLCBzZXJpZV9yb3dzKSBpZiBzZXJpZV9yb3dzIGVsc2UgcCgiX1NpbiBzZXJpZS5fIiksCiAgICAgICAgaDIoIkNhbWJpb3Mgw7psdGltbyB2cyBwZXLDrW9kbyBhbnRlcmlvciIpLAogICAgICAgIGJ1bGxldHMoY2FtYmlvc1s6ODBdIG9yIFsiU2luIHBhcmVzIGRlIHBlcsOtb2RvcyBjb21wYXJhYmxlcy4iXSksCiAgICAgICAgaDIoIlJlc3VtZW4gZGUgdGlja2V0cyBwb3IgZXN0YWRvIiksCiAgICAgICAgbWRfdGFibGUoCiAgICAgICAgICAgIFsiRXN0YWRvIiwgIkNhbnRpZGFkIl0sCiAgICAgICAgICAgIFtbclsiZXN0YWRvIl0sIHJbIm4iXV0gZm9yIHIgaW4gYnlfZXN0YWRvXSwKICAgICAgICApCiAgICAgICAgaWYgYnlfZXN0YWRvCiAgICAgICAgZWxzZSBwKCJfU2luIHRpY2tldHMuXyIpLAogICAgICAgIGgyKCJSZXN1bWVuIGRlIHRpY2tldHMgcG9yIHByaW9yaWRhZCIpLAogICAgICAgIG1kX3RhYmxlKAogICAgICAgICAgICBbIlByaW9yaWRhZCIsICJDYW50aWRhZCJdLAogICAgICAgICAgICBbW3JbInByaW9yaWRhZCJdLCByWyJuIl1dIGZvciByIGluIGJ5X3ByaW9dLAogICAgICAgICkKICAgICAgICBpZiBieV9wcmlvCiAgICAgICAgZWxzZSBwKCJfU2luIGRlc2dsb3NlLl8iKSwKICAgICAgICBoMigiUmVzdW1lbiBwb3IgdW5pZGFkIGRlIG5lZ29jaW8gKGJyb3dzZSB0YWJsZXJvKSIpLAogICAgICAgIG1kX3RhYmxlKHVuX2hlYWRlcnMsIHVuX3Jvd3MpIGlmIHVuX3Jvd3MgZWxzZSBwKCJfU2luIGRlc2dsb3NlLl8iKSwKICAgICAgICBoMigiUmVzdW1lbiBwb3IgdXN1YXJpbyBhc2lnbmFkbyIpLAogICAgICAgIHAoIkVxdWl2YWxlbnRlIGEgYC9wZ28vcmVzdW1lbi91c3VhcmlvL2AuIiksCiAgICAgICAgbWRfdGFibGUodXNlcl9oZWFkZXJzLCB1c2VyX3Jvd3MpIGlmIHVzZXJfcm93cyBlbHNlIHAoIl9TaW4gYXNpZ25hY2nDs24uXyIpLAogICAgICAgIGgyKCJEZXRhbGxlIGNvbXBsZXRvIGRlIHRpY2tldHMgKGJyb3dzZSBhZG1pbmlzdHJhY2nDs24pIiksCiAgICAgICAgcCgKICAgICAgICAgICAgZiJSZWdpc3Ryb3M6ICoqe2xlbih0aWNrZXRfcm93cyl9KiouIEluY2x1eWUgZGVzY3JpcGNpw7NuIGNvbXBsZXRhICIKICAgICAgICAgICAgImNvbW8gZW4gZWwgZGV0YWxsZSBkZWwgdGlja2V0LiIKICAgICAgICApLAogICAgICAgIG1kX3RhYmxlKHRpY2tldF9oZWFkZXJzLCB0aWNrZXRfcm93cykgaWYgdGlja2V0X3Jvd3MgZWxzZSBwKCJfU2luIHRpY2tldHMuXyIpLAogICAgICAgIGgyKCJFdmVudG9zIGRlIHRpY2tldHMiKSwKICAgICAgICBwKAogICAgICAgICAgICBmIkZpbGFzIGluY2x1aWRhczogKip7bGVuKGV2ZW50b19yb3dzKX0qKiIKICAgICAgICAgICAgKyAoZiIgKHRvcGUge2V2ZW50b19jYXB9OyB0b3RhbCBCRCB7ZXZlbnRvX3RvdGFsfSkuIiBpZiBldmVudG9fdG90YWwgZWxzZSAiLiIpCiAgICAgICAgKSwKICAgICAgICBtZF90YWJsZShldmVudG9faGVhZGVycywgZXZlbnRvX3Jvd3MpIGlmIGV2ZW50b19yb3dzIGVsc2UgcCgiX1NpbiBldmVudG9zLl8iKSwKICAgICAgICAqd2NnX21kLAogICAgICAgIGgyKCJJbnZlbnRhcmlvIiksCiAgICAgICAgYnVsbGV0cyhoZWNob3MpLAogICAgICAgIGgyKCJHdcOtYSBkZSBhbsOhbGlzaXMgZXN0cmF0w6lnaWNvIChJQSkiKSwKICAgICAgICBwKAogICAgICAgICAgICAiQ29uIGxhcyB0YWJsYXMgYW50ZXJpb3JlcywgY29uc3RydXllIHVuIGRpYWduw7NzdGljbyBkZSBvcGVyYWNpw7NuIFBHTzogIgogICAgICAgICAgICAiKDEpIMK/ZWwgU0xBIG1lam9yYSBvIGVtcGVvcmEgcG9yIFVOIHkgcGVyw61vZG8/OyAiCiAgICAgICAgICAgICIoMikgwr9oYXkgc29icmVjYXJnYSBlbiB1c3VhcmlvcyBvIHVuaWRhZGVzIGNvbmNyZXRhcz87ICIKICAgICAgICAgICAgIigzKSDCv2N1w6FudG9zIHRpY2tldHMgYWJpZXJ0b3MgY3LDrXRpY29zL2FsdGEgcHJpb3JpZGFkIGhheSB5IGRlc2RlIGN1w6FuZG8/OyAiCiAgICAgICAgICAgICIoNCkgcmVjb21lbmRhY2lvbmVzIGFjY2lvbmFibGVzIChyZWRpc3RyaWJ1aXIsIHJldmlzYXIgU0xBLCBwcmlvcml6YXIgYmFja2xvZykuICIKICAgICAgICAgICAgIkNpdGEgY2lmcmFzIGV4cGzDrWNpdGFzLiBObyBpbnZlbnRlcyBDbGFzaWZpY2EgbmkgdW1icmFsZXMgYXVzZW50ZXMgZW4gbG9zIGRhdG9zLiIKICAgICAgICApLAogICAgXQogICAgaWYgY2ZnLmluY2x1ZGVfYWlfc2VjdGlvbjoKICAgICAgICBtZF9wYXJ0cy5hcHBlbmQoCiAgICAgICAgICAgIGFpX2Nsb3NpbmcoCiAgICAgICAgICAgICAgICBoZWNob3MsCiAgICAgICAgICAgICAgICBjYW1iaW9zWzo0MF0gaWYgY2ZnLmluY2x1ZGVfcGVyaW9kX2NvbXBhcmlzb24gZWxzZSBbIkNvbXBhcmFjacOzbiBkZXNhY3RpdmFkYS4iXSwKICAgICAgICAgICAgICAgIHZhY2lvcyBvciBbIlNpbiB2YWPDrW9zIGNyw610aWNvcyBhZGljaW9uYWxlcy4iXSwKICAgICAgICAgICAgKQogICAgICAgICkKCiAgICBzaGVldHMgPSBbCiAgICAgICAgX3NoZWV0KCJLUEkgZGFzaGJvYXJkIiwgIktQSXMgL3Bnby8iLCBrcGlfaGVhZGVycywga3BpX3Jvd3MpLAogICAgICAgIF9zaGVldCgiUmVzdWx0YWRvcyBwZXJpb2RvIiwgIlBnb1Jlc3VsdGFkb1BlcmlvZG8iLCByZXNfaGVhZGVycywgcmVzX3Jvd3MpLAogICAgICAgIF9zaGVldCgiU2VyaWUgcG9yIHBlcmlvZG8iLCAiQ2lmcmFzIGJhc2UgdGVuZGVuY2lhIiwgc2VyaWVfaGVhZGVycywgc2VyaWVfcm93cyksCiAgICAgICAgX3NoZWV0KCJQb3IgZXN0YWRvIiwgIkNvbnRlbyB0aWNrZXRzIiwgWyJFc3RhZG8iLCAiTiJdLCBbW3JbImVzdGFkbyJdLCByWyJuIl1dIGZvciByIGluIGJ5X2VzdGFkb10pLAogICAgICAgIF9zaGVldCgKICAgICAgICAgICAgIlBvciBwcmlvcmlkYWQiLAogICAgICAgICAgICAiQ29udGVvIHByaW9yaWRhZCIsCiAgICAgICAgICAgIFsiUHJpb3JpZGFkIiwgIk4iXSwKICAgICAgICAgICAgW1tyWyJwcmlvcmlkYWQiXSwgclsibiJdXSBmb3IgciBpbiBieV9wcmlvXSwKICAgICAgICApLAogICAgICAgIF9zaGVldCgiUG9yIFVOIiwgIlJlc3VtZW4gdW5pZGFkIiwgdW5faGVhZGVycywgdW5fcm93cyksCiAgICAgICAgX3NoZWV0KCJQb3IgdXN1YXJpbyIsICJSZXN1bWVuIGFzaWduYWRvIiwgdXNlcl9oZWFkZXJzLCB1c2VyX3Jvd3MpLAogICAgICAgIF9zaGVldCgiVGlja2V0cyIsICJEZXRhbGxlIHRpY2tldHMgUEdPIiwgdGlja2V0X2hlYWRlcnMsIHRpY2tldF9yb3dzKSwKICAgICAgICBfc2hlZXQoIkV2ZW50b3MiLCBmIlRpY2tldEV2ZW50byAoaGFzdGEge2V2ZW50b19jYXB9KSIsIGV2ZW50b19oZWFkZXJzLCBldmVudG9fcm93cyksCiAgICAgICAgX3NoZWV0KAogICAgICAgICAgICAiRXhwbGljYWNpb24iLAogICAgICAgICAgICAiUHJvY2VzbyBQR08iLAogICAgICAgICAgICBbIlRlbWEiLCAiRGV0YWxsZSJdLAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICBbIkZ1ZW50ZSBwcm9kdWN0aXZhIiwgInBnby5UaWNrZXQgKyByZWNhbGN1bGF0ZV9wZ29fcGVyaW9kb3MiXSwKICAgICAgICAgICAgICAgIFsiU0xBIiwgImhvcmFzIGNpY2xvIDw9IHNsYV9ob3JhcyJdLAogICAgICAgICAgICAgICAgWyJDbGFzaWZpY2EgUEdPIHByb2R1Y3Rpdm8iLCAiTm8gaW1wbGVtZW50YWRhIl0sCiAgICAgICAgICAgICAgICBbIkZ1ZW50ZSBXQ0cgT25lIiwgImFwcHMucGdvLiogc2kgaGF5IGRhdG9zIl0sCiAgICAgICAgICAgIF0sCiAgICAgICAgKSwKICAgICAgICAqd2NnX3NoZWV0cywKICAgIF0KCiAgICByZXR1cm4gewogICAgICAgICJtZCI6IGpvaW5fc2VjdGlvbnMoKm1kX3BhcnRzKSwKICAgICAgICAic2hlZXRzIjogc2hlZXRzLAogICAgICAgICJzdGFtcCI6IHN0YW1wLAogICAgICAgICJzdGFtcF9sYWJlbCI6IHN0YW1wX2xhYmVsLAogICAgICAgICJwZXJpb2QiOiBjdXJyX3AsCiAgICAgICAgInByZXZfcGVyaW9kIjogcHJldl9wLAogICAgfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
