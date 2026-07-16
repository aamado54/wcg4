from django.contrib import admin

from .models import ReportConfig


@admin.register(ReportConfig)
class ReportConfigAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "include_pgc_by_default",
        "include_pgo_by_default",
        "include_risk_by_default",
        "compact_mode",
        "updated_at",
    )
    list_filter = ("is_active", "compact_mode")
    search_fields = ("name", "intro_note")
    fieldsets = (
        (None, {"fields": ("name", "is_active", "intro_note")}),
        (
            "Defaults del checklist",
            {
                "fields": (
                    "include_admin_by_default",
                    "include_pgc_by_default",
                    "include_pgo_by_default",
                    "include_risk_by_default",
                )
            },
        ),
        (
            "Secciones y densidad",
            {
                "fields": (
                    "include_executive_summary",
                    "include_period_comparison",
                    "include_ai_section",
                    "compact_mode",
                    "max_table_rows",
                )
            },
        ),
    )
