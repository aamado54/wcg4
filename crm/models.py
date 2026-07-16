from django.conf import settings
from django.db import models

from core.models import TimeStampedModel
from core.wcg_models import Entidad


class Interaccion(TimeStampedModel):
    """Registro CRM. Clave: id autoincremental; vinculada a Entidad."""
    TIPO_LLAMADA = "LLAMADA"
    TIPO_REUNION = "REUNION"
    TIPO_EMAIL = "EMAIL"
    TIPO_OTRO = "OTRO"
    TIPO_CHOICES = [
        (TIPO_LLAMADA, "Llamada"),
        (TIPO_REUNION, "Reunión"),
        (TIPO_EMAIL, "Email"),
        (TIPO_OTRO, "Otro"),
    ]

    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="interacciones")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_LLAMADA)
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField()
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_interacciones",
    )

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Interacción"
        verbose_name_plural = "Interacciones"

    def __str__(self):
        return f"{self.entidad.codigo} — {self.asunto}"


class Tarea(TimeStampedModel):
    """Tarea CRM. Clave: id autoincremental; vinculada a Entidad."""
    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_EN_PROCESO = "EN_PROCESO"
    ESTADO_HECHA = "HECHA"
    ESTADO_CANCELADA = "CANCELADA"
    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, "Pendiente"),
        (ESTADO_EN_PROCESO, "En proceso"),
        (ESTADO_HECHA, "Hecha"),
        (ESTADO_CANCELADA, "Cancelada"),
    ]

    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="tareas")
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)
    asignado_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_tareas",
    )

    class Meta:
        ordering = ["estado", "fecha_vencimiento", "-created_at"]
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"

    def __str__(self):
        return f"{self.entidad.codigo} — {self.titulo}"
