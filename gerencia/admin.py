from django.contrib import admin

from .models import GerenciaScenario


@admin.register(GerenciaScenario)
class GerenciaScenarioAdmin(admin.ModelAdmin):
    list_display = ("name", "updated_at", "created_by")
    search_fields = ("name", "notes")
