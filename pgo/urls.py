from django.urls import path

from . import scorecard_views, views

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
]
