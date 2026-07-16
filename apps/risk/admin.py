from django.contrib import admin

from .models import (
    ContactoCobranza,
    EstadoFinanciero,
    RiskAlerta,
    RiskOperacion,
    RiskOperationSnapshot,
    RiskPagoProgramado,
    RiskPagoRealizado,
)


class RiskOperationSnapshotInline(admin.TabularInline):
    model = RiskOperationSnapshot
    extra = 0
    fields = ("fecha_snapshot", "estado_operacion", "past_due_balance", "due_days")
    readonly_fields = fields
    can_delete = False
    show_change_link = True


@admin.register(RiskOperacion)
class RiskOperacionAdmin(admin.ModelAdmin):
    list_display = (
        "codigo_operacion",
        "entidad",
        "producto",
        "unidad_negocio",
        "estado",
        "monto_original",
        "fecha_inicio",
    )
    list_filter = ("estado", "unidad_negocio", "moneda")
    search_fields = (
        "codigo_operacion",
        "contrato_numero",
        "entidad__nombre",
        "entidad__nit",
        "asesor",
    )
    autocomplete_fields = ("entidad", "producto", "unidad_negocio")
    inlines = [RiskOperationSnapshotInline]
    ordering = ("entidad__nombre", "codigo_operacion")


@admin.register(RiskOperationSnapshot)
class RiskOperationSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_snapshot",
        "operacion",
        "entidad",
        "estado_operacion",
        "capital_balance",
        "past_due_balance",
        "due_days",
    )
    list_filter = ("fecha_snapshot", "estado_operacion")
    search_fields = (
        "operacion__codigo_operacion",
        "entidad__nombre",
        "entidad__nit",
        "producto_nombre_raw",
    )
    date_hierarchy = "fecha_snapshot"
    autocomplete_fields = ("operacion", "entidad", "import_batch")
    ordering = ("-fecha_snapshot",)


@admin.register(EstadoFinanciero)
class EstadoFinancieroAdmin(admin.ModelAdmin):
    list_display = (
        "entidad",
        "fecha_corte",
        "ventas",
        "utilidad_neta",
        "patrimonio",
        "ebitda",
    )
    list_filter = ("fecha_corte",)
    search_fields = ("entidad__nombre", "entidad__nit", "auditor_contador")
    autocomplete_fields = ("entidad", "import_batch")
    ordering = ("-fecha_corte",)


@admin.register(RiskPagoProgramado)
class RiskPagoProgramadoAdmin(admin.ModelAdmin):
    list_display = (
        "operacion",
        "entidad",
        "fecha_programada",
        "monto_capital",
        "monto_interes",
        "estado",
    )
    list_filter = ("estado", "fecha_programada", "moneda")
    search_fields = ("operacion__codigo_operacion", "entidad__nombre")
    autocomplete_fields = ("operacion", "entidad")
    ordering = ("fecha_programada",)


@admin.register(RiskPagoRealizado)
class RiskPagoRealizadoAdmin(admin.ModelAdmin):
    list_display = (
        "operacion",
        "entidad",
        "fecha_pago",
        "monto_capital",
        "monto_interes",
        "referencia",
    )
    list_filter = ("fecha_pago", "moneda")
    search_fields = ("operacion__codigo_operacion", "entidad__nombre", "referencia")
    autocomplete_fields = ("operacion", "entidad")
    ordering = ("-fecha_pago",)


@admin.register(ContactoCobranza)
class ContactoCobranzaAdmin(admin.ModelAdmin):
    list_display = (
        "fecha",
        "entidad",
        "operacion",
        "tipo_contacto",
        "resultado",
        "fecha_compromiso",
    )
    list_filter = ("tipo_contacto", "fecha")
    search_fields = ("entidad__nombre", "resultado", "acuerdo")
    autocomplete_fields = ("entidad", "operacion", "contacto")
    ordering = ("-fecha",)


@admin.register(RiskAlerta)
class RiskAlertaAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_alerta",
        "entidad",
        "operacion",
        "tipo_alerta",
        "severidad",
        "activa",
        "origen",
    )
    list_filter = ("tipo_alerta", "severidad", "activa", "fecha_alerta")
    search_fields = ("mensaje", "entidad__nombre", "operacion__codigo_operacion")
    autocomplete_fields = ("entidad", "operacion")
    ordering = ("-fecha_alerta",)
