# pgc/admin.py

from django.contrib import admin

from .models import (
    AdminManualEditLog,
    ManualRequirementsCompliance,
    MetricReserve,
    MonthlyExchangeRate,
    MonthlyMetricResult,
    MonthlyMetricScore,
    MonthlyModeScorecard,
    MonthlyScorecard,
    MonthlyTarget,
    PGCPlan,
)


@admin.register(MonthlyMetricScore)
class MonthlyMetricScoreAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "year",
        "month",
        "mode",
        "une",
        "metric",
        "measured_value",
        "target_value",
        "points_awarded",
        "carry_in",
        "carry_used",
        "carry_generated",
        "is_achieved",
    )
    list_filter = (
        "plan",
        "year",
        "month",
        "mode",
        "une",
        "metric",
        "is_achieved",
    )
    search_fields = (
        "une__name_es",
        "metric__name",
        "calculation_note",
    )


@admin.register(MonthlyModeScorecard)
class MonthlyModeScorecardAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "year",
        "month",
        "mode",
        "une",
        "total_points",
        "qualified_threshold",
        "is_month_qualified",
    )
    list_filter = (
        "plan",
        "year",
        "month",
        "mode",
        "une",
        "is_month_qualified",
    )
    search_fields = (
        "une__name_es",
        "summary_note",
    )


@admin.register(MetricReserve)
class MetricReserveAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "mode",
        "une",
        "metric",
        "source_year",
        "source_month",
        "amount",
        "remaining",
    )
    list_filter = (
        "plan",
        "mode",
        "une",
        "metric",
        "source_year",
        "source_month",
    )
    search_fields = (
        "une__name_es",
        "metric__name",
        "notes",
    )


@admin.register(MonthlyExchangeRate)
class MonthlyExchangeRateAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "month",
        "usd_to_gtq",
    )
    list_filter = ("year",)
    ordering = ("-year", "month")


@admin.register(PGCPlan)
class PGCPlanAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "name",
        "is_active",
        "created_at",
    )
    list_filter = (
        "is_active",
        "year",
    )
    search_fields = (
        "name",
        "notes",
    )


@admin.register(MonthlyTarget)
class MonthlyTargetAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "year",
        "month",
        "une",
        "metric",
        "target_value",
        "points_if_achieved",
        "reference_annual_value",
    )
    list_filter = (
        "plan",
        "year",
        "month",
        "une",
        "metric",
    )
    search_fields = (
        "une__name_es",
        "metric__name",
        "notes",
    )


@admin.register(MonthlyMetricResult)
class MonthlyMetricResultAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "year",
        "month",
        "une",
        "metric",
        "measured_value",
        "target_value",
        "is_achieved",
        "points_awarded",
    )
    list_filter = (
        "plan",
        "year",
        "month",
        "une",
        "metric",
        "is_achieved",
    )
    search_fields = (
        "une__name_es",
        "metric__name",
        "calculation_note",
    )


@admin.register(MonthlyScorecard)
class MonthlyScorecardAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "year",
        "month",
        "une",
        "total_points",
        "qualified_threshold",
        "is_month_qualified",
    )
    list_filter = (
        "plan",
        "year",
        "month",
        "une",
        "is_month_qualified",
    )
    search_fields = (
        "une__name_es",
        "summary_note",
    )


@admin.register(AdminManualEditLog)
class AdminManualEditLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "year",
        "month",
        "entity_type",
        "field_name",
        "edited_by",
    )
    list_filter = ("entity_type", "year", "month")
    search_fields = ("field_name", "old_value", "new_value", "reason")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ManualRequirementsCompliance)
class ManualRequirementsComplianceAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "year",
        "month",
        "une",
        "is_compliant",
    )
    list_filter = (
        "plan",
        "year",
        "month",
        "une",
        "is_compliant",
    )
    search_fields = (
        "une__name_es",
        "incident_note",
    )