from django.urls import path

from . import views

app_name = "wcgone_risk"

urlpatterns = [
    path("comando-balon/", views.comando_balon, name="comando_balon"),
    path("comando-balon/exportar/", views.export_comando_balon_csv, name="export_comando_balon"),
    path("clientes/", views.ClienteListView.as_view(), name="cliente_list"),
    path("clientes/<int:pk>/", views.ClienteDetailView.as_view(), name="cliente_detail"),
    path("operaciones/<int:pk>/", views.OperacionDetailView.as_view(), name="operacion_detail"),
    path("importar-snapshots/", views.importar_snapshots, name="importar_snapshots"),
    path("importar-eeff/", views.importar_eeff, name="importar_eeff"),
]
