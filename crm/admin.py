from django.contrib import admin

from .models import Interaccion, Tarea


@admin.register(Interaccion)
class InteraccionAdmin(admin.ModelAdmin):
    list_display = ("fecha", "entidad", "tipo", "asunto", "usuario")
    list_filter = ("tipo", "fecha")
    search_fields = ("asunto", "descripcion", "entidad__codigo", "entidad__nombre")
    ordering = ("-fecha",)


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "entidad", "estado", "fecha_vencimiento", "asignado_a")
    list_filter = ("estado", "fecha_vencimiento")
    search_fields = ("titulo", "descripcion", "entidad__codigo", "entidad__nombre")
    ordering = ("estado", "fecha_vencimiento")
