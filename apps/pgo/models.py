from django.conf import settings
from django.db import models


class PgoTicket(models.Model):
    ticket_externo_id = models.CharField(max_length=100, blank=True, db_index=True)
    usuario_solicita = models.CharField(max_length=150, blank=True)
    correo_solicita = models.EmailField(blank=True)
    departamento = models.CharField(max_length=150, blank=True, db_index=True)
    tipo = models.CharField(max_length=100, blank=True)
    titulo = models.CharField(max_length=255)
    estado_raw = models.CharField(max_length=100, blank=True)
    estado_normalizado = models.CharField(max_length=50, blank=True, db_index=True)
    solucion = models.TextField(blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    fecha_apertura = models.DateTimeField(null=True, blank=True)
    fecha_registro = models.DateTimeField(null=True, blank=True)
    prioridad = models.CharField(max_length=50, blank=True, db_index=True)
    tipo_servicio = models.CharField(max_length=100, blank=True)
    razon_cierre = models.CharField(max_length=255, blank=True)
    sistema = models.CharField(max_length=100, blank=True, db_index=True)
    elemento = models.CharField(max_length=255, blank=True)
    ruta = models.CharField(max_length=255, blank=True)
    anio_mes = models.CharField(max_length=7, blank=True, db_index=True)
    duracion_horas = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sla_horas = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sla_cumplido = models.BooleanField(default=False)
    unidad_negocio = models.ForeignKey(
        "wcgone_core.UnidadNegocio",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_pgo_tickets",
    )
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_pgo_tickets",
    )
    import_batch = models.ForeignKey(
        "wcgone_core.DataImportBatch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_pgo_tickets",
    )
    payload_raw_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-fecha_apertura", "-id"]
        verbose_name = "Ticket PGO"
        verbose_name_plural = "Tickets PGO"

    def __str__(self):
        label = self.ticket_externo_id or str(self.pk)
        return f"{label} — {self.titulo}"


class PgoMetricRule(models.Model):
    TIPO_AUTOMATICA = "automatica"
    TIPO_MANUAL = "manual"
    TIPO_HIBRIDA = "hibrida"
    TIPO_CHOICES = [
        (TIPO_AUTOMATICA, "Automática"),
        (TIPO_MANUAL, "Manual"),
        (TIPO_HIBRIDA, "Híbrida"),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    area = models.CharField(max_length=100, blank=True)
    variable = models.CharField(max_length=100)
    criterio = models.TextField()
    unidad_negocio = models.ForeignKey(
        "wcgone_core.UnidadNegocio",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pgo_reglas",
    )
    puntos = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    peso = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    tipo_regla = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_AUTOMATICA)
    formula_texto = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["area", "codigo"]
        verbose_name = "Regla métrica PGO"
        verbose_name_plural = "Reglas métricas PGO"

    def __str__(self):
        return self.codigo


class PgoPeriodScore(models.Model):
    periodo = models.CharField(max_length=7, db_index=True)
    area = models.CharField(max_length=100, blank=True)
    unidad_negocio = models.ForeignKey(
        "wcgone_core.UnidadNegocio",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_pgo_period_scores",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_pgo_period_scores",
    )
    puntaje_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    clasifica = models.BooleanField(default=False)
    detalle_json = models.JSONField(default=dict, blank=True)
    fecha_calculo = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-periodo", "area"]
        verbose_name = "Puntaje PGO por período"
        verbose_name_plural = "Puntajes PGO por período"

    def __str__(self):
        return f"{self.periodo} — {self.area or 'general'}"


class PgoMonthlyAgg(models.Model):
    periodo = models.CharField(max_length=7, db_index=True)
    unidad_negocio = models.ForeignKey(
        "wcgone_core.UnidadNegocio",
        on_delete=models.CASCADE,
        related_name="pgo_monthly_aggs",
    )
    departamento = models.CharField(max_length=150, blank=True)
    tickets_recibidos = models.PositiveIntegerField(default=0)
    tickets_cerrados = models.PositiveIntegerField(default=0)
    tiempo_promedio_horas = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sla_cumplidos = models.PositiveIntegerField(default=0)
    sla_incumplidos = models.PositiveIntegerField(default=0)
    tickets_abiertos_fin_mes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-periodo", "unidad_negocio__nombre"]
        verbose_name = "Agregado mensual PGO"
        verbose_name_plural = "Agregados mensuales PGO"
        indexes = [
            models.Index(fields=["periodo", "departamento"]),
        ]

    def __str__(self):
        return f"{self.periodo} — {self.unidad_negocio}"
