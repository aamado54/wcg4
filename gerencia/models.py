from django.conf import settings
from django.db import models


class GerenciaSettings(models.Model):
    """Ajustes globales del Centro Gerencial (una sola fila)."""

    strict_gerencial = models.BooleanField(
        default=False,
        help_text="Si está activo, 301010106 (acciones preferentes) se trata como pasivo a 1 año.",
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="gerencia_settings_updates",
    )

    class Meta:
        verbose_name = "Ajuste Centro Gerencial"
        verbose_name_plural = "Ajustes Centro Gerencial"

    def __str__(self) -> str:
        return "Centro Gerencial · " + (
            "vista estricta ON" if self.strict_gerencial else "vista estricta OFF"
        )

    @classmethod
    def get(cls) -> "GerenciaSettings":
        obj = cls.objects.order_by("pk").first()
        if obj:
            return obj
        return cls.objects.create(strict_gerencial=False)


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
