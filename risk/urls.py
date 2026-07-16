from django.urls import path

from . import views

app_name = "risk"

urlpatterns = [
    path("", views.comando_balon, name="comando_balon"),
    path("cliente/<str:codigo>/", views.ClienteDetailView.as_view(), name="cliente_detail"),
    path("operacion/<int:pk>/", views.OperacionDetailView.as_view(), name="operacion_detail"),
    path("importar/", views.importar, name="importar"),
]
