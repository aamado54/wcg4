# core/admin.py 

from django import forms
from django.contrib import admin, messages
from django.core.management import call_command
from django.shortcuts import redirect, render
from django.urls import path, reverse

from .models import (
    UNE,
    UNEAlias,
    Currency,
    MetricDefinition,
    SystemSetting,
    Contacto,
    DataDictionary,
    DataImportBatch,
    Entidad,
    Producto,
    RelacionEntidadProducto,
    UnidadNegocio,
)


class RecalcOpsForm(forms.Form):
    year = forms.IntegerField(min_value=2020, max_value=2100, initial=2026, label="Año")
    month = forms.IntegerField(min_value=1, max_value=12, initial=4, label="Mes")
    run_investment_ingresos = forms.BooleanField(
        required=False, initial=True, label="Recalcular ingresos Investment"
    )
    run_pgc = forms.BooleanField(
        required=False, initial=True, label="Recalcular PGC"
    )
    mode = forms.ChoiceField(
        choices=[("modo1", "Modo 1"), ("modo2", "Modo 2")],
        initial="modo1",
        label="Modalidad de cálculo de PGC",
    )
  

@admin.register(UNE)
class UneAdmin(admin.ModelAdmin):
    list_display = ("code", "name_es", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    search_fields = ("code", "name", "name_es")


@admin.register(UNEAlias)
class UneAliasAdmin(admin.ModelAdmin):
    list_display = ("raw_value", "une", "alias_type", "is_active")
    list_filter = ("une", "is_active")
    search_fields = ("raw_value",)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "symbol", "is_active")
    list_editable = ("is_active",)
    search_fields = ("code", "name")


@admin.register(MetricDefinition)
class MetricDefinitionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_scored")
    list_editable = ("is_scored",)
    search_fields = ("code", "name")


class RecalcOpsForm(forms.Form):
    year = forms.IntegerField(min_value=2020, max_value=2100, initial=2026, label="Año")
    month = forms.IntegerField(min_value=1, max_value=12, initial=4, label="Mes")
    run_investment_ingresos = forms.BooleanField(required=False, initial=True, label="Recalcular ingresos Investment")
    run_pgc = forms.BooleanField(required=False, initial=True, label="Recalcular PGC")


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "value_text", "value_bool", "updated_by", "updated_at")
    list_filter = ("value_bool",)
    search_fields = ("key", "description", "value_text")
    readonly_fields = ("created_at", "updated_at", "updated_by")
    change_list_template = "admin/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "run-recalc-ops/",
                self.admin_site.admin_view(self.run_recalc_ops_view),
                name="core_systemsetting_run_recalc_ops",
            ),
        ]
        return custom_urls + urls

    def run_recalc_ops_view(self, request):
        if not request.user.is_superuser:
            self.message_user(
                request,
                "Solo superusuarios pueden ejecutar estas operaciones.",
                level=messages.ERROR,
            )
            return redirect("admin:core_systemsetting_changelist")

        if request.method == "POST":
            form = RecalcOpsForm(request.POST)
            if form.is_valid():
                year = form.cleaned_data["year"]
                month = form.cleaned_data["month"]
                mode = form.cleaned_data["mode"]
                run_investment_ingresos = form.cleaned_data["run_investment_ingresos"]
                run_pgc = form.cleaned_data["run_pgc"]

                if not run_investment_ingresos and not run_pgc:
                    self.message_user(
                        request,
                        "Debes seleccionar al menos una operación.",
                        level=messages.WARNING,
                    )
                    return redirect("admin:core_systemsetting_run_recalc_ops")

                try:
                    if run_investment_ingresos:
                        call_command(
                            "recalc_investment_ingresos_from_new_clients",
                            year=year,
                            month=month,
                        )
                        self.message_user(
                            request,
                            f"Ingresos Investment recalculados para {year}-{month:02d}.",
                            level=messages.SUCCESS,
                        )

                    if run_pgc:
                        call_command(
                            "recalc_pgc",
                            year=year,
                            month=month, 
                            mode=mode
                        )
                        self.message_user(
                            request,
                            f"PGC recalculado para {year}-{month:02d} en {mode}.",
        level=messages.SUCCESS,
                        )

                    return redirect("admin:core_systemsetting_changelist")

                except Exception as exc:
                    self.message_user(
                        request,
                        f"Error al ejecutar operaciones: {exc}",
                        level=messages.ERROR,
                    )
        else:
            form = RecalcOpsForm()

        context = {
            **self.admin_site.each_context(request),
            "title": "Operaciones de recálculo",
            "form": form,
            "opts": self.model._meta,
            "has_view_permission": self.has_view_permission(request),
        }
        return render(
            request,
            "admin/run_recalc_ops.html",
            context,
        )


@admin.register(UnidadNegocio)
class UnidadNegocioAdmin(admin.ModelAdmin):
    list_display = ("code", "nombre", "une_pgc", "activa", "updated_at")
    list_filter = ("activa",)
    search_fields = ("code", "nombre")
    ordering = ("nombre",)


@admin.register(Entidad)
class EntidadAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "nit", "tipo", "unidad_negocio", "activa")
    list_filter = ("tipo", "activa", "unidad_negocio")
    search_fields = ("codigo", "nombre", "nit")
    ordering = ("nombre",)


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "entidad", "email", "telefono", "es_principal", "activo")
    list_filter = ("es_principal", "activo", "entidad")
    search_fields = ("nombre", "email", "entidad__codigo", "entidad__nombre")
    ordering = ("entidad__nombre", "nombre")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "unidad_negocio", "activo")
    list_filter = ("activo", "unidad_negocio")
    search_fields = ("codigo", "nombre")
    ordering = ("nombre",)


@admin.register(RelacionEntidadProducto)
class RelacionEntidadProductoAdmin(admin.ModelAdmin):
    list_display = ("entidad", "producto", "estado", "fecha_inicio")
    list_filter = ("estado", "producto")
    search_fields = ("entidad__codigo", "entidad__nombre", "producto__codigo")
    ordering = ("entidad__nombre",)


@admin.register(DataDictionary)
class DataDictionaryAdmin(admin.ModelAdmin):
    list_display = ("modulo", "tabla", "campo", "etiqueta", "obligatorio")
    list_filter = ("modulo", "obligatorio")
    search_fields = ("modulo", "tabla", "campo", "etiqueta")
    ordering = ("modulo", "tabla", "campo")


@admin.register(DataImportBatch)
class DataImportBatchAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "modulo",
        "tipo_importacion",
        "archivo_nombre",
        "status",
        "creados",
        "actualizados",
        "errores",
        "uploaded_by",
    )
    list_filter = ("modulo", "status", "tipo_importacion")
    search_fields = ("archivo_nombre", "tipo_importacion", "log_texto")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")