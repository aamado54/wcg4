from django.urls import path

from . import views

app_name = "wcgone_crm"

urlpatterns = [
    path("entidades/", views.EntidadListView.as_view(), name="entidad_list"),
    path("entidades/exportar/", views.export_entidades_csv, name="export_entidades"),
    path("entidades/<int:pk>/", views.EntidadDetailView.as_view(), name="entidad_detail"),
    path("contactos/", views.ContactoListView.as_view(), name="contacto_list"),
    path("tareas/", views.TareaListView.as_view(), name="tarea_list"),
    path("importar/", views.importar_entidades, name="importar"),
]
