from django.contrib import admin

from .models import (
    ContactoCobranza,
    EstadoFinanciero,
    PagoRealizado,
    ProgramacionPago,
    RiskOperationSnapshot,
)


@admin.register(EstadoFinanciero)
class EstadoFinancieroAdmin(admin.ModelAdmin):
    list_display = ("entidad", "periodo", "saldo_total", "mora_dias", "exposicion")
    list_filter = ("periodo",)
    search_fields = ("entidad__codigo", "entidad__nombre")
    ordering = ("-periodo",)


@admin.register(ProgramacionPago)
class ProgramacionPagoAdmin(admin.ModelAdmin):
    list_display = ("entidad", "referencia", "fecha_programada", "monto", "moneda", "producto")
    list_filter = ("fecha_programada", "moneda")
    search_fields = ("referencia", "entidad__codigo", "entidad__nombre")
    ordering = ("fecha_programada",)


@admin.register(PagoRealizado)
class PagoRealizadoAdmin(admin.ModelAdmin):
    list_display = ("entidad", "referencia", "fecha_pago", "monto", "moneda")
    list_filter = ("fecha_pago", "moneda")
    search_fields = ("referencia", "entidad__codigo", "entidad__nombre")
    ordering = ("-fecha_pago",)


@admin.register(ContactoCobranza)
class ContactoCobranzaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "entidad", "telefono", "email", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre", "entidad__codigo", "entidad__nombre")
    ordering = ("entidad__nombre",)


@admin.register(RiskOperationSnapshot)
class RiskOperationSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_snapshot",
        "entidad",
        "referencia_operacion",
        "nivel_riesgo",
        "dias_mora",
        "saldo",
        "monto_exigible",
        "alerta",
    )
    list_filter = ("nivel_riesgo", "alerta", "fecha_snapshot")
    search_fields = ("referencia_operacion", "entidad__codigo", "entidad__nombre")
    ordering = ("-fecha_snapshot",)
