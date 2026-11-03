from django.contrib import admin

from .models import PgoManualCaptureVersion, PgoResultadoPeriodo, Ticket, TicketEvento


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


@admin.register(PgoManualCaptureVersion)
class PgoManualCaptureVersionAdmin(admin.ModelAdmin):
    list_display = (
        "capture_type",
        "period_year",
        "period_month",
        "user",
        "created_at",
        "is_out_of_period",
    )
    list_filter = ("capture_type", "period_year", "is_out_of_period")
    search_fields = ("capture_type", "change_note", "user__username")
    readonly_fields = ("created_at", "payload", "user", "capture_type", "period_year", "period_month")
    ordering = ("-created_at",)

    def has_delete_permission(self, request, obj=None):
        return False
