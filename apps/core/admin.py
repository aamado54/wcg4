from django.contrib import admin

from .models import (
    Contacto,
    DataDictionaryField,
    DataImportBatch,
    DataImportError,
    Entidad,
    Producto,
    RelacionEntidadProducto,
    UnidadNegocio,
)


class ContactoInline(admin.TabularInline):
    model = Contacto
    extra = 0
    fields = ("nombre", "cargo", "email", "telefono_movil", "activo")


class RelacionEntidadProductoInline(admin.TabularInline):
    model = RelacionEntidadProducto
    extra = 0
    autocomplete_fields = ("producto", "unidad_negocio")


@admin.register(UnidadNegocio)
class UnidadNegocioAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "activa", "orden")
    list_filter = ("activa",)
    search_fields = ("codigo", "nombre")
    ordering = ("orden", "nombre")


@admin.register(Entidad)
class EntidadAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "nit",
        "tipo_entidad",
        "ciudad",
        "categoria_riesgo",
        "activo",
        "fecha_modificacion",
    )
    list_filter = ("tipo_entidad", "activo", "categoria_riesgo", "pais")
    search_fields = ("nombre", "nombre_comercial", "nit", "email")
    ordering = ("nombre",)
    inlines = [ContactoInline, RelacionEntidadProductoInline]
    readonly_fields = ("fecha_creacion", "fecha_modificacion")


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "entidad",
        "cargo",
        "email",
        "es_contacto_cobranza",
        "activo",
    )
    list_filter = ("activo", "es_decisor_credito", "es_contacto_cobranza", "es_contacto_operativo")
    search_fields = ("nombre", "email", "entidad__nombre", "entidad__nit")
    autocomplete_fields = ("entidad",)
    ordering = ("entidad__nombre", "nombre")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "tipo_producto", "activo")
    list_filter = ("activo", "tipo_producto")
    search_fields = ("codigo", "nombre")
    ordering = ("nombre",)


@admin.register(RelacionEntidadProducto)
class RelacionEntidadProductoAdmin(admin.ModelAdmin):
    list_display = (
        "entidad",
        "producto",
        "unidad_negocio",
        "estado",
        "fecha_inicio",
        "monto_aprobado",
    )
    list_filter = ("estado", "unidad_negocio", "moneda")
    search_fields = (
        "entidad__nombre",
        "entidad__nit",
        "producto__codigo",
        "codigo_operacion_externo",
    )
    autocomplete_fields = ("entidad", "producto", "unidad_negocio")


@admin.register(DataDictionaryField)
class DataDictionaryFieldAdmin(admin.ModelAdmin):
    list_display = (
        "modulo",
        "nombre_logico",
        "tabla_fisica",
        "campo_fisico",
        "tipo_dato",
        "activo",
        "orden",
    )
    list_filter = ("modulo", "activo", "periodicidad")
    search_fields = ("nombre_logico", "tabla_fisica", "campo_fisico", "definicion")
    ordering = ("modulo", "orden", "tabla_fisica")


class DataImportErrorInline(admin.TabularInline):
    model = DataImportError
    extra = 0
    readonly_fields = ("fila_numero", "campo", "valor_original", "mensaje_error")
    can_delete = False


@admin.register(DataImportBatch)
class DataImportBatchAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_carga",
        "modulo",
        "tipo_importacion",
        "archivo_nombre",
        "estado",
        "filas_leidas",
        "filas_validas",
        "filas_error",
        "usuario",
    )
    list_filter = ("modulo", "estado", "tipo_importacion")
    search_fields = ("archivo_nombre", "tipo_importacion", "observaciones")
    date_hierarchy = "fecha_carga"
    readonly_fields = ("fecha_carga",)
    inlines = [DataImportErrorInline]


@admin.register(DataImportError)
class DataImportErrorAdmin(admin.ModelAdmin):
    list_display = ("batch", "fila_numero", "campo", "mensaje_error")
    list_filter = ("batch__modulo",)
    search_fields = ("mensaje_error", "valor_original", "campo")
    ordering = ("-batch__fecha_carga", "fila_numero")
