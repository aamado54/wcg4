from django.conf import settings
from django.db import models


class GerenciaScenario(models.Model):
    """Escenario what-if simplificado (inspirado en hoja Control de wc-mod5c)."""

    name = models.CharField(max_length=120)
    notes = models.TextField(blank=True, default="")
    growth_cartera_f = models.FloatField(default=0.10)
    growth_cartera_l = models.FloatField(default=0.08)
    rate_activa_f = models.FloatField(default=0.18)
    rate_activa_l = models.FloatField(default=0.14)
    rate_pasiva_inv = models.FloatField(default=0.09)
    rate_pasiva_bancos = models.FloatField(default=0.08)
    growth_overhead = models.FloatField(default=0.05)
    result_snapshot = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="gerencia_scenarios",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Escenario gerencial"
        verbose_name_plural = "Escenarios gerenciales"

    def __str__(self) -> str:
        return self.name
