from django.urls import path

from . import views

app_name = "crm"

urlpatterns = [
    path("", views.EntidadListView.as_view(), name="entidad_list"),
    path("entidades/<str:codigo>/", views.EntidadDetailView.as_view(), name="entidad_detail"),
    path("entidades/<str:codigo>/interaccion/nueva/", views.nueva_interaccion, name="nueva_interaccion"),
    path("entidades/<str:codigo>/tarea/nueva/", views.nueva_tarea, name="nueva_tarea"),
    path("importar/<str:tipo>/", views.importar, name="importar"),
]
