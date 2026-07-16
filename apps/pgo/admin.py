from django.contrib import admin

from .models import PgoMetricRule, PgoMonthlyAgg, PgoPeriodScore, PgoTicket


@admin.register(PgoTicket)
class PgoTicketAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_externo_id",
        "titulo",
        "estado_normalizado",
        "prioridad",
        "departamento",
        "sistema",
        "anio_mes",
        "sla_cumplido",
        "fecha_apertura",
    )
    list_filter = (
        "estado_normalizado",
        "prioridad",
        "departamento",
        "sistema",
        "anio_mes",
        "sla_cumplido",
    )
    search_fields = (
        "ticket_externo_id",
        "titulo",
        "usuario_solicita",
        "correo_solicita",
        "departamento",
    )
    autocomplete_fields = ("unidad_negocio", "responsable", "import_batch")
    ordering = ("-fecha_apertura",)


@admin.register(PgoMetricRule)
class PgoMetricRuleAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "area",
        "variable",
        "puntos",
        "peso",
        "tipo_regla",
        "activo",
    )
    list_filter = ("area", "tipo_regla", "activo", "unidad_negocio")
    search_fields = ("codigo", "variable", "criterio")
    autocomplete_fields = ("unidad_negocio",)
    ordering = ("area", "codigo")


@admin.register(PgoPeriodScore)
class PgoPeriodScoreAdmin(admin.ModelAdmin):
    list_display = (
        "periodo",
        "area",
        "unidad_negocio",
        "usuario",
        "puntaje_total",
        "clasifica",
        "fecha_calculo",
    )
    list_filter = ("periodo", "clasifica", "area", "unidad_negocio")
    search_fields = ("periodo", "area")
    date_hierarchy = "fecha_calculo"
    autocomplete_fields = ("unidad_negocio", "usuario")
    ordering = ("-periodo",)


@admin.register(PgoMonthlyAgg)
class PgoMonthlyAggAdmin(admin.ModelAdmin):
    list_display = (
        "periodo",
        "unidad_negocio",
        "departamento",
        "tickets_recibidos",
        "tickets_cerrados",
        "tiempo_promedio_horas",
        "sla_cumplidos",
        "sla_incumplidos",
    )
    list_filter = ("periodo", "unidad_negocio", "departamento")
    search_fields = ("periodo", "departamento")
    autocomplete_fields = ("unidad_negocio",)
    ordering = ("-periodo",)
