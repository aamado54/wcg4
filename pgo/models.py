from django.conf import settings
from django.db import models

from core.models import TimeStampedModel
from core.wcg_models import Entidad, UnidadNegocio


class Ticket(TimeStampedModel):
    """
    Ticket operativo PGO.
    Clave natural importación: `codigo` (ID ticket / folio).
    """
    ESTADO_ABIERTO = "ABIERTO"
    ESTADO_EN_PROCESO = "EN_PROCESO"
    ESTADO_CERRADO = "CERRADO"
    ESTADO_CHOICES = [
        (ESTADO_ABIERTO, "Abierto"),
        (ESTADO_EN_PROCESO, "En proceso"),
        (ESTADO_CERRADO, "Cerrado"),
    ]

    PRIORIDAD_BAJA = "BAJA"
    PRIORIDAD_MEDIA = "MEDIA"
    PRIORIDAD_ALTA = "ALTA"
    PRIORIDAD_CHOICES = [
        (PRIORIDAD_BAJA, "Baja"),
        (PRIORIDAD_MEDIA, "Media"),
        (PRIORIDAD_ALTA, "Alta"),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    entidad = models.ForeignKey(
        Entidad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )
    unidad_negocio = models.ForeignKey(
        UnidadNegocio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_ABIERTO)
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default=PRIORIDAD_MEDIA)
    asignado_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pgo_tickets",
    )
    fecha_apertura = models.DateTimeField()
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    sla_horas = models.PositiveIntegerField(default=48)

    class Meta:
        ordering = ["-fecha_apertura"]
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"{self.codigo} — {self.titulo}"


class TicketEvento(TimeStampedModel):
    TIPO_COMENTARIO = "COMENTARIO"
    TIPO_CAMBIO_ESTADO = "CAMBIO_ESTADO"
    TIPO_ASIGNACION = "ASIGNACION"
    TIPO_CHOICES = [
        (TIPO_COMENTARIO, "Comentario"),
        (TIPO_CAMBIO_ESTADO, "Cambio de estado"),
        (TIPO_ASIGNACION, "Asignación"),
    ]

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="eventos")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_COMENTARIO)
    descripcion = models.TextField()
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pgo_ticket_eventos",
    )
    fecha = models.DateTimeField()

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Evento de ticket"
        verbose_name_plural = "Eventos de ticket"

    def __str__(self):
        return f"{self.ticket.codigo} — {self.tipo}"


class PgoResultadoPeriodo(TimeStampedModel):
    """
    Agregado mensual por unidad. Clave natural: (`periodo` YYYY-MM, `unidad_negocio`).
    Calculado desde tickets vía `pgo.periodo.recalculate_pgo_periodos`.
    """
    periodo = models.CharField(max_length=7, help_text="YYYY-MM")
    unidad_negocio = models.ForeignKey(
        UnidadNegocio,
        on_delete=models.CASCADE,
        related_name="resultados_pgo",
    )
    tickets_cerrados = models.PositiveIntegerField(default=0)
    tickets_abiertos = models.PositiveIntegerField(default=0)
    tiempo_promedio_horas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cumplimiento_sla_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        unique_together = ("periodo", "unidad_negocio")
        ordering = ["-periodo", "unidad_negocio__nombre"]
        verbose_name = "Resultado PGO por período"
        verbose_name_plural = "Resultados PGO por período"

    def __str__(self):
        return f"{self.periodo} — {self.unidad_negocio.code}"
