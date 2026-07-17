from django.urls import path

from . import views

app_name = "crm"

urlpatterns = [
    path("", views.EntidadListView.as_view(), name="entidad_list"),
    path("contactos/", views.ContactoListView.as_view(), name="contacto_list"),
    path("tareas/", views.TareaListView.as_view(), name="tarea_list"),
    path("exportar/", views.export_entidades, name="export_entidades"),
    path("entidades/<str:codigo>/", views.EntidadDetailView.as_view(), name="entidad_detail"),
    path("entidades/<str:codigo>/interaccion/nueva/", views.nueva_interaccion, name="nueva_interaccion"),
    path("entidades/<str:codigo>/tarea/nueva/", views.nueva_tarea, name="nueva_tarea"),
    path("importar/", views.importar, name="importar"),
    path("importar/<str:tipo>/", views.importar, name="importar_tipo"),
]
