from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UNE(TimeStampedModel):
    CODE_FACTORING = 'FACTORING'
    CODE_LEASING = 'LEASING'
    CODE_INSURANCE = 'INSURANCE'
    CODE_INVESTMENT = 'INVESTMENT'

    CODE_CHOICES = [
        (CODE_FACTORING, 'Factoraje'),
        (CODE_LEASING, 'Leasing'),
        (CODE_INSURANCE, 'Insurance'),
        (CODE_INVESTMENT, 'Inversiones'),
    ]

    UNIT_USD = 'USD'
    UNIT_KUSD = 'KUSD'
    UNIT_GTQ = 'GTQ'
    UNIT_KGTQ = 'KGTQ'

    UNIT_CHOICES = [
        (UNIT_USD, 'USD (dólares)'),
        (UNIT_KUSD, 'Miles de USD'),
        (UNIT_GTQ, 'GTQ (quetzales)'),
        (UNIT_KGTQ, 'Miles de GTQ'),
    ]

    code = models.CharField(max_length=20, unique=True, choices=CODE_CHOICES)
    name = models.CharField(max_length=50)
    name_es = models.CharField(max_length=50)
    default_amount_unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default=UNIT_KUSD,
        help_text='Unidad habitual de reporte para montos en esta UNE.',
    )
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name_es']
        verbose_name = 'UNE'
        verbose_name_plural = 'UNEs'

    def __str__(self):
        return self.name_es


class UNEAlias(TimeStampedModel):
    raw_value = models.CharField(max_length=255, unique=True)
    une = models.ForeignKey(UNE, on_delete=models.CASCADE, related_name='aliases')
    alias_type = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['raw_value']
        verbose_name = 'Alias de UNE'
        verbose_name_plural = 'Aliases de UNE'

    def __str__(self):
        return f'{self.raw_value} -> {self.une.code}'


class Currency(TimeStampedModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['code']
        verbose_name = 'Moneda'
        verbose_name_plural = 'Monedas'

    def __str__(self):
        return self.code


class MetricDefinition(TimeStampedModel):
    CODE_INGRESOS = 'INGRESOS'
    CODE_CLIENTES_NUEVOS = 'CLIENTES_NUEVOS'
    CODE_VENTA_CRUZADA = 'VENTA_CRUZADA'
    CODE_RESPUESTA_REQS = 'RESPUESTA_REQS'

    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_scored = models.BooleanField(default=True)

    class Meta:
        ordering = ['code']
        verbose_name = 'Métrica'
        verbose_name_plural = 'Métricas'

    def __str__(self):
        return self.name


class SystemSetting(TimeStampedModel):
    key = models.CharField(max_length=100, unique=True)
    value_text = models.TextField(blank=True, null=True)
    value_bool = models.BooleanField(blank=True, null=True)
    value_json = models.JSONField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_system_settings'
    )

    class Meta:
        ordering = ['key']
        verbose_name = 'Configuración del sistema'
        verbose_name_plural = 'Configuraciones del sistema'

    def __str__(self):
        return self.key


# Maestro común WCG One (CRM, Risk, PGO, PGC)
from .wcg_models import (  # noqa: E402, F401
    Contacto,
    DataDictionary,
    DataImportBatch,
    Entidad,
    Producto,
    RelacionEntidadProducto,
    UnidadNegocio,
)