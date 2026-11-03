from django.urls import path

from . import scorecard_views, views, capturas_views

app_name = "pgo"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("tablero/", scorecard_views.tablero_puntos, name="tablero_puntos"),
    path("ayuda/pgo-referencia.pdf", scorecard_views.ayuda_pgo_pdf, name="ayuda_pgo_pdf"),
    path("tickets/", views.TicketListView.as_view(), name="ticket_list"),
    path("tickets/<str:codigo>/", views.TicketDetailView.as_view(), name="ticket_detail"),
    path("resultados/", views.resultados, name="resultados"),
    path("exportar/", views.export_tickets, name="export_tickets"),
    path("importar/", views.importar, name="importar"),
    path("resumen/usuario/", views.resumen_usuario, name="resumen_usuario"),
    path("resumen/unidad/", views.resumen_unidad, name="resumen_unidad"),
    path("capturas/", capturas_views.capturas_index, name="capturas_index"),
    path("capturas/<slug:slug>/", capturas_views.capturas_page, name="capturas_page"),
    path("capturas/<slug:slug>/historial/", capturas_views.capturas_history, name="capturas_history"),
    path(
        "capturas/<slug:slug>/version/<int:version_id>/",
        capturas_views.capturas_version_detail,
        name="capturas_version_detail",
    ),
]
