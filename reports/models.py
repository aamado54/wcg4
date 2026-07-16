from django.db import models

from core.models import TimeStampedModel


class ReportConfig(TimeStampedModel):
    """Configuración ampliable para generación de reportes desde PGC."""

    name = models.CharField(max_length=80, unique=True, default="default")
    is_active = models.BooleanField(default=True)

    include_admin_by_default = models.BooleanField(default=False)
    include_pgc_by_default = models.BooleanField(default=True)
    include_pgo_by_default = models.BooleanField(default=False)
    include_risk_by_default = models.BooleanField(default=False)

    include_executive_summary = models.BooleanField(default=True)
    include_period_comparison = models.BooleanField(default=True)
    include_ai_section = models.BooleanField(default=True)
    compact_mode = models.BooleanField(
        default=True,
        help_text="Limita tablas y listas a hallazgos de alta densidad.",
    )
    max_table_rows = models.PositiveIntegerField(default=25)
    intro_note = models.TextField(
        blank=True,
        help_text="Nota opcional al inicio de cada reporte de resultados.",
    )

    class Meta:
        verbose_name = "Configuración de reportes"
        verbose_name_plural = "Configuraciones de reportes"

    def __str__(self):
        return f"ReportConfig:{self.name}"

    @classmethod
    def get_active(cls) -> "ReportConfig":
        obj = cls.objects.filter(is_active=True).order_by("id").first()
        if obj:
            return obj
        return cls.objects.create(name="default", is_active=True)
