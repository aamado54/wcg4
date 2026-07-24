from django.urls import path

from . import views

app_name = "risk"

urlpatterns = [
    path("", views.comando_balon, name="comando_balon"),
    path("evaluacion/", views.evaluacion_clientes, name="evaluacion_clientes"),
    path("clientes/", views.ClienteListView.as_view(), name="cliente_list"),
    path("cliente/<str:codigo>/", views.ClienteDetailView.as_view(), name="cliente_detail"),
    path("operacion/<int:pk>/", views.OperacionDetailView.as_view(), name="operacion_detail"),
    path("exportar/", views.export_comando_balon, name="export_comando_balon"),
    path("importar/", views.importar, name="importar"),
]
