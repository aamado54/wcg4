from django.contrib import admin

from .models import GerenciaScenario, GerenciaSettings, GerenciaStressReport


@admin.register(GerenciaSettings)
class GerenciaSettingsAdmin(admin.ModelAdmin):
    list_display = ("strict_gerencial", "updated_at", "updated_by")


@admin.register(GerenciaScenario)
class GerenciaScenarioAdmin(admin.ModelAdmin):
    list_display = ("name", "updated_at", "created_by")
    search_fields = ("name", "notes")


@admin.register(GerenciaStressReport)
class GerenciaStressReportAdmin(admin.ModelAdmin):
    list_display = ("fecha", "tema", "slug", "title", "created_at")
    list_filter = ("fecha",)
    search_fields = ("tema", "title", "slug")
    prepopulated_fields = {"slug": ("tema",)}
    readonly_fields = ("created_at",)
