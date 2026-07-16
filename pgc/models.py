# pgc/models.py

from django.conf import settings
from django.db import models
from core.models import TimeStampedModel, UNE, MetricDefinition


class PGCMode(models.TextChoices):
    MODO1 = "modo1", "Modo 1"
    MODO2 = "modo2", "Modo 2"


class MonthlyMetricScore(TimeStampedModel):
    plan = models.ForeignKey("PGCPlan", on_delete=models.CASCADE, related_name="metric_scores")
    une = models.ForeignKey(UNE, on_delete=models.CASCADE, related_name="metric_scores")
    metric = models.ForeignKey(MetricDefinition, on_delete=models.CASCADE, related_name="metric_scores")
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    mode = models.CharField(max_length=10, choices=PGCMode.choices, default=PGCMode.MODO1)

    measured_value = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    target_value = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)

    is_achieved = models.BooleanField(default=False)
    points_awarded = models.DecimalField(max_digits=18, decimal_places=4, default=0)

    carry_in = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    carry_used = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    carry_generated = models.DecimalField(max_digits=18, decimal_places=4, default=0)

    calculation_note = models.TextField(blank=True)

    class Meta:
        unique_together = ("plan", "une", "metric", "year", "month", "mode")
        ordering = ["year", "month", "une__sort_order", "metric__code", "mode"]

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.une.code} {self.metric.code} {self.mode}"


class MonthlyModeScorecard(TimeStampedModel):
    plan = models.ForeignKey("PGCPlan", on_delete=models.CASCADE, related_name="mode_scorecards")
    une = models.ForeignKey(UNE, on_delete=models.CASCADE, related_name="mode_scorecards")
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    mode = models.CharField(max_length=10, choices=PGCMode.choices, default=PGCMode.MODO1)

    total_points = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    qualified_threshold = models.DecimalField(max_digits=18, decimal_places=4, default=80)
    is_month_qualified = models.BooleanField(default=False)
    summary_note = models.TextField(blank=True)

    class Meta:
        unique_together = ("plan", "une", "year", "month", "mode")
        ordering = ["year", "month", "une__sort_order", "mode"]

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.une.code} {self.mode} ({self.total_points} pts)"


class MetricReserve(TimeStampedModel):
    plan = models.ForeignKey("PGCPlan", on_delete=models.CASCADE, related_name="metric_reserves")
    une = models.ForeignKey(UNE, on_delete=models.CASCADE, related_name="metric_reserves")
    metric = models.ForeignKey(MetricDefinition, on_delete=models.CASCADE, related_name="metric_reserves")

    mode = models.CharField(max_length=10, choices=PGCMode.choices, default=PGCMode.MODO2)

    source_year = models.PositiveIntegerField()
    source_month = models.PositiveIntegerField()

    amount = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    remaining = models.DecimalField(max_digits=18, decimal_places=4, default=0)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["source_year", "source_month", "une__sort_order", "metric__code"]

    def __str__(self):
        return f"{self.source_year}-{self.source_month:02d} {self.une.code} {self.metric.code} rem={self.remaining}"


class MonthlyExchangeRate(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    usd_to_gtq = models.DecimalField(max_digits=10, decimal_places=5)

    class Meta:
        unique_together = ("year", "month")
        ordering = ["year", "month"]

    def __str__(self):
        return f"{self.year}-{self.month:02d}: 1 USD = {self.usd_to_gtq} GTQ"


class PGCPlan(TimeStampedModel):
    year = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100, default="Plan PGC")
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-year"]
        verbose_name = "Plan PGC"
        verbose_name_plural = "Planes PGC"

    def __str__(self):
        return f"{self.name} {self.year}"


class MonthlyTarget(TimeStampedModel):
    plan = models.ForeignKey(
        PGCPlan,
        on_delete=models.CASCADE,
        related_name="monthly_targets",
    )
    une = models.ForeignKey(
        UNE,
        on_delete=models.CASCADE,
        related_name="monthly_targets",
    )
    metric = models.ForeignKey(
        MetricDefinition,
        on_delete=models.CASCADE,
        related_name="monthly_targets",
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    target_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    points_if_achieved = models.PositiveIntegerField(default=0)
    reference_annual_value = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Solo referencia; no asigna puntos por sí misma.",
    )
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("plan", "une", "metric", "year", "month")
        ordering = ["year", "month", "une__sort_order", "metric__code"]
        verbose_name = "Meta mensual"
        verbose_name_plural = "Metas mensuales"

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.une.code} {self.metric.code}"


class MonthlyMetricResult(TimeStampedModel):
    # conversion_status for manual/auto income capture
    CONVERSION_NATIVE_USD = "NATIVE_USD"
    CONVERSION_CONVERTED = "CONVERTED"
    CONVERSION_MISSING_FX = "MISSING_FX"
    CONVERSION_STALE_FX = "STALE_FX"
    CONVERSION_CHOICES = [
        (CONVERSION_NATIVE_USD, "USD nativo / legado"),
        (CONVERSION_CONVERTED, "Convertido GTQ→USD"),
        (CONVERSION_MISSING_FX, "Sin tipo de cambio"),
        (CONVERSION_STALE_FX, "TC desactualizado"),
    ]

    CURRENCY_GTQ = "GTQ"
    CURRENCY_USD = "USD"

    plan = models.ForeignKey(
        PGCPlan,
        on_delete=models.CASCADE,
        related_name="metric_results",
    )
    une = models.ForeignKey(
        UNE,
        on_delete=models.CASCADE,
        related_name="metric_results",
    )
    metric = models.ForeignKey(
        MetricDefinition,
        on_delete=models.CASCADE,
        related_name="metric_results",
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    # Canonical value for scoring/reporting: always USD for INGRESOS.
    measured_value = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    target_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    is_achieved = models.BooleanField(default=False)
    points_awarded = models.PositiveIntegerField(default=0)
    calculation_note = models.TextField(blank=True)

    # Financial capture trail (mainly for manual/auto INGRESOS).
    source_currency = models.CharField(max_length=3, blank=True, default="")
    source_value = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    exchange_rate_used = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    conversion_status = models.CharField(
        max_length=20,
        choices=CONVERSION_CHOICES,
        blank=True,
        default="",
    )

    class Meta:
        unique_together = ("plan", "une", "metric", "year", "month")
        ordering = ["year", "month", "une__sort_order", "metric__code"]
        verbose_name = "Resultado mensual de métrica"
        verbose_name_plural = "Resultados mensuales de métricas"

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.une.code} {self.metric.code}"


class MonthlyScorecard(TimeStampedModel):
    plan = models.ForeignKey(
        PGCPlan,
        on_delete=models.CASCADE,
        related_name="scorecards",
    )
    une = models.ForeignKey(
        UNE,
        on_delete=models.CASCADE,
        related_name="scorecards",
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    total_points = models.PositiveIntegerField(default=0)
    qualified_threshold = models.PositiveIntegerField(default=80)
    is_month_qualified = models.BooleanField(default=False)
    summary_note = models.TextField(blank=True)

    class Meta:
        unique_together = ("plan", "une", "year", "month")
        ordering = ["year", "month", "une__sort_order"]
        verbose_name = "Score mensual"
        verbose_name_plural = "Scores mensuales"

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.une.code} ({self.total_points} pts)"


class ManualRequirementsCompliance(TimeStampedModel):
    plan = models.ForeignKey(
        PGCPlan,
        on_delete=models.CASCADE,
        related_name="manual_requirements",
    )
    une = models.ForeignKey(
        UNE,
        on_delete=models.CASCADE,
        related_name="manual_requirements",
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    is_compliant = models.BooleanField(default=True)
    incident_note = models.TextField(blank=True)

    class Meta:
        unique_together = ("plan", "une", "year", "month")
        ordering = ["year", "month", "une__sort_order"]
        verbose_name = "Cumplimiento manual de requerimientos"
        verbose_name_plural = "Cumplimientos manuales de requerimientos"

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.une.code} cumplimiento={self.is_compliant}"


class AdminManualEditLog(TimeStampedModel):
    """Trazabilidad básica de cambios manuales desde Administración."""

    ENTITY_TARGET = "target"
    ENTITY_RESULT = "result"
    ENTITY_REQUIREMENT = "requirement"
    ENTITY_FX = "fx"
    ENTITY_ALIAS = "alias"
    ENTITY_NEW_CLIENT_ROW = "new_client_row"
    ENTITY_CROSS_SALE_ROW = "cross_sale_row"
    ENTITY_PERIOD_NOTE = "period_note"

    ENTITY_CHOICES = [
        (ENTITY_TARGET, "Meta mensual"),
        (ENTITY_RESULT, "Resultado mensual"),
        (ENTITY_REQUIREMENT, "Requerimiento manual"),
        (ENTITY_FX, "Tipo de cambio"),
        (ENTITY_ALIAS, "Alias UNE"),
        (ENTITY_NEW_CLIENT_ROW, "Fila cliente nuevo"),
        (ENTITY_CROSS_SALE_ROW, "Fila venta cruzada"),
        (ENTITY_PERIOD_NOTE, "Nota del período"),
    ]

    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    entity_type = models.CharField(max_length=30, choices=ENTITY_CHOICES)
    entity_id = models.PositiveIntegerField(null=True, blank=True)
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    reason = models.TextField(blank=True)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admin_manual_edits",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Bitácora de edición manual"
        verbose_name_plural = "Bitácora de ediciones manuales"

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.entity_type}.{self.field_name}"