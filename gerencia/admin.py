from django.contrib import admin

from .models import GerenciaScenario, GerenciaSettings


@admin.register(GerenciaSettings)
class GerenciaSettingsAdmin(admin.ModelAdmin):
    list_display = ("strict_gerencial", "updated_at", "updated_by")


@admin.register(GerenciaScenario)
class GerenciaScenarioAdmin(admin.ModelAdmin):
    list_display = ("name", "updated_at", "created_by")
    search_fields = ("name", "notes")
