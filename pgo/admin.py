from django.contrib import admin

from .models import PgoResultadoPeriodo, Ticket, TicketEvento


class TicketEventoInline(admin.TabularInline):
    model = TicketEvento
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "titulo",
        "estado",
        "prioridad",
        "unidad_negocio",
        "asignado_a",
        "fecha_apertura",
    )
    list_filter = ("estado", "prioridad", "unidad_negocio")
    search_fields = ("codigo", "titulo", "descripcion")
    ordering = ("-fecha_apertura",)
    inlines = [TicketEventoInline]


@admin.register(TicketEvento)
class TicketEventoAdmin(admin.ModelAdmin):
    list_display = ("ticket", "tipo", "fecha", "usuario")
    list_filter = ("tipo", "fecha")
    search_fields = ("ticket__codigo", "descripcion")
    ordering = ("-fecha",)


@admin.register(PgoResultadoPeriodo)
class PgoResultadoPeriodoAdmin(admin.ModelAdmin):
    list_display = (
        "periodo",
        "unidad_negocio",
        "tickets_cerrados",
        "tickets_abiertos",
        "tiempo_promedio_horas",
        "cumplimiento_sla_pct",
    )
    list_filter = ("periodo", "unidad_negocio")
    search_fields = ("periodo", "unidad_negocio__code", "unidad_negocio__nombre")
    ordering = ("-periodo",)
