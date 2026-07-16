from django.contrib import admin

from .models import Interaccion, NotaEntidad, Tarea


@admin.register(Interaccion)
class InteraccionAdmin(admin.ModelAdmin):
    list_display = (
        "fecha",
        "entidad",
        "tipo_interaccion",
        "resumen",
        "usuario",
        "seguimiento_requerido",
    )
    list_filter = ("tipo_interaccion", "fecha", "seguimiento_requerido")
    search_fields = ("resumen", "resultado", "entidad__nombre", "entidad__nit")
    date_hierarchy = "fecha"
    autocomplete_fields = ("entidad", "producto", "usuario")
    ordering = ("-fecha",)


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = (
        "descripcion",
        "entidad",
        "estado",
        "prioridad",
        "fecha_limite",
        "completada",
        "asignado_a",
    )
    list_filter = ("estado", "completada", "prioridad", "fecha_limite")
    search_fields = ("descripcion", "entidad__nombre", "entidad__nit")
    autocomplete_fields = ("entidad", "contacto", "asignado_a")
    ordering = ("completada", "fecha_limite")


@admin.register(NotaEntidad)
class NotaEntidadAdmin(admin.ModelAdmin):
    list_display = ("fecha", "entidad", "titulo", "autor")
    list_filter = ("fecha",)
    search_fields = ("titulo", "contenido", "entidad__nombre")
    autocomplete_fields = ("entidad", "autor")
    ordering = ("-fecha",)
