from django.conf import settings
from django.db import models

from core.models import TimeStampedModel
from core.wcg_models import Entidad, Producto


class EstadoFinanciero(TimeStampedModel):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="estados_financieros")
    periodo = models.CharField(max_length=7, help_text="YYYY-MM")
    saldo_total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    mora_dias = models.PositiveIntegerField(default=0)
    exposicion = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    notas = models.TextField(blank=True)

    class Meta:
        unique_together = ("entidad", "periodo")
        ordering = ["-periodo", "entidad__nombre"]
        verbose_name = "Estado financiero"
        verbose_name_plural = "Estados financieros"

    def __str__(self):
        return f"{self.entidad.codigo} {self.periodo}"


class ProgramacionPago(TimeStampedModel):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="programaciones_pago")
    referencia = models.CharField(max_length=80)
    fecha_programada = models.DateField()
    monto = models.DecimalField(max_digits=16, decimal_places=2)
    moneda = models.CharField(max_length=3, default="GTQ")
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="programaciones_pago",
    )

    class Meta:
        unique_together = ("entidad", "referencia")
        ordering = ["fecha_programada"]
        verbose_name = "Programación de pago"
        verbose_name_plural = "Programaciones de pago"

    def __str__(self):
        return f"{self.entidad.codigo} — {self.referencia}"


class PagoRealizado(TimeStampedModel):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="pagos_realizados")
    referencia = models.CharField(max_length=80)
    fecha_pago = models.DateField()
    monto = models.DecimalField(max_digits=16, decimal_places=2)
    moneda = models.CharField(max_length=3, default="GTQ")

    class Meta:
        unique_together = ("entidad", "referencia")
        ordering = ["-fecha_pago"]
        verbose_name = "Pago realizado"
        verbose_name_plural = "Pagos realizados"

    def __str__(self):
        return f"{self.entidad.codigo} — {self.referencia}"


class ContactoCobranza(TimeStampedModel):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="contactos_cobranza")
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["entidad__nombre", "nombre"]
        verbose_name = "Contacto de cobranza"
        verbose_name_plural = "Contactos de cobranza"

    def __str__(self):
        return f"{self.nombre} ({self.entidad.codigo})"


class RiskOperationSnapshot(TimeStampedModel):
    """
    Snapshot operativo de riesgo (Balón).
    Clave natural: (`entidad`, `referencia_operacion`, `fecha_snapshot`).
    """
    NIVEL_BAJO = "BAJO"
    NIVEL_MEDIO = "MEDIO"
    NIVEL_ALTO = "ALTO"
    NIVEL_CRITICO = "CRITICO"
    NIVEL_CHOICES = [
        (NIVEL_BAJO, "Bajo"),
        (NIVEL_MEDIO, "Medio"),
        (NIVEL_ALTO, "Alto"),
        (NIVEL_CRITICO, "Crítico"),
    ]

    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="risk_snapshots")
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="risk_snapshots",
    )
    referencia_operacion = models.CharField(max_length=80, db_index=True)
    fecha_snapshot = models.DateField()
    nivel_riesgo = models.CharField(max_length=20, choices=NIVEL_CHOICES, default=NIVEL_MEDIO)
    dias_mora = models.PositiveIntegerField(default=0)
    saldo = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    monto_exigible = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        help_text="Monto vencido/exigible al momento del snapshot.",
    )
    alerta = models.BooleanField(default=False)
    detalle = models.TextField(blank=True)

    class Meta:
        unique_together = ("entidad", "referencia_operacion", "fecha_snapshot")
        ordering = ["-fecha_snapshot", "entidad__nombre"]
        verbose_name = "Snapshot operativo de riesgo"
        verbose_name_plural = "Snapshots operativos de riesgo"

    def __str__(self):
        return f"{self.referencia_operacion} — {self.fecha_snapshot}"


class EvaluacionPlantilla(TimeStampedModel):
    """Plantilla Excel individual subida desde /risk/evaluacion/."""

    original_filename = models.CharField(max_length=255)
    stored_file = models.FileField(upload_to="evaluacion/plantillas/")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evaluacion_plantillas",
    )
    file_size = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Plantilla de evaluación"
        verbose_name_plural = "Plantillas de evaluación"

    def __str__(self):
        return self.original_filename


class EvaluacionImportRun(TimeStampedModel):
    """Snapshot consolidado tras importar plantillas (dataset serializado)."""

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evaluacion_import_runs",
    )
    source_label = models.CharField(max_length=500, blank=True)
    companies_count = models.PositiveIntegerField(default=0)
    plantillas_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="ok")
    dataset_json = models.JSONField(default=dict, blank=True)
    alerts = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Importación evaluación"
        verbose_name_plural = "Importaciones evaluación"

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} — {self.companies_count} empresas"
