from django.urls import path

from . import views

app_name = "gerencia"

urlpatterns = [
    path("", views.home, name="home"),
    path("intermediacion/", views.intermediacion, name="intermediacion"),
    path("liquidez/", views.liquidez, name="liquidez"),
    path("estructura/", views.estructura, name="estructura"),
    path("escenarios/", views.escenarios, name="escenarios"),
    path("escenarios/nov-2026/", views.escenario_nov2026, name="escenario_nov2026"),
    path("comando/", views.comando, name="comando"),
    path("indices/", views.indices, name="indices"),
    path("whatif/", views.whatif, name="whatif"),
    path("whatif/escenario/<int:pk>/", views.load_scenario, name="load_scenario"),
    path("detalle/", views.detalle, name="detalle"),
    path("ccy/", views.set_ccy, name="set_ccy"),
    path("ajustes/", views.config, name="config"),
]
