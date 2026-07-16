from django.urls import path

from . import views

app_name = "pgo"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("tickets/", views.TicketListView.as_view(), name="ticket_list"),
    path("tickets/<str:codigo>/", views.TicketDetailView.as_view(), name="ticket_detail"),
    path("importar/", views.importar, name="importar"),
    path("resumen/usuario/", views.resumen_usuario, name="resumen_usuario"),
    path("resumen/unidad/", views.resumen_unidad, name="resumen_unidad"),
]
