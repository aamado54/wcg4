from django.urls import path

from . import views

app_name = "wcgone_pgo"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("tickets/", views.TicketListView.as_view(), name="ticket_list"),
    path("tickets/exportar/", views.export_tickets_csv, name="export_tickets"),
    path("tickets/<int:pk>/", views.TicketDetailView.as_view(), name="ticket_detail"),
    path("resultados/", views.resultados, name="resultados"),
    path("importar-tickets/", views.importar_tickets, name="importar_tickets"),
]
