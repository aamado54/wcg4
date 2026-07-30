from django.urls import path

from . import views

app_name = "gerencia"

urlpatterns = [
    path("", views.home, name="home"),
    path("intermediacion/", views.intermediacion, name="intermediacion"),
    path("liquidez/", views.liquidez, name="liquidez"),
    path("estructura/", views.estructura, name="estructura"),
    path("comando/", views.comando, name="comando"),
    path("indices/", views.indices, name="indices"),
    path("whatif/", views.whatif, name="whatif"),
    path("whatif/escenario/<int:pk>/", views.load_scenario, name="load_scenario"),
    path("detalle/", views.detalle, name="detalle"),
]
