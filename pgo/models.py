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


class PgoArchivoRegistro(TimeStampedModel):
    """Fila de ArchivosPGO_YYYY-MM.csv (SharePoint / carpetas PGO)."""

    carpeta = models.CharField(max_length=500)
    archivo = models.CharField(max_length=500)
    creado_por = models.CharField(max_length=200, blank=True)
    creado_en = models.DateTimeField()
    event_date = models.DateField(null=True, blank=True, db_index=True)
    snapshot_key = models.CharField(max_length=40, db_index=True)
    import_batch_id = models.PositiveIntegerField(db_index=True)

    class Meta:
        ordering = ["-creado_en"]
        verbose_name = "Registro ArchivosPGO"
        verbose_name_plural = "Registros ArchivosPGO"
        constraints = [
            models.UniqueConstraint(
                fields=["snapshot_key", "carpeta", "archivo", "creado_en"],
                name="pgo_archivo_registro_uniq",
            ),
        ]

    def __str__(self):
        return f"{self.archivo[:50]} ({self.event_date})"


class PgoExpediente(TimeStampedModel):
    """
    Trabajo / expediente desde export «Archivos» (inicio → entrega).
    Clave natural: (source_batch_id, row_key) o external_id si existe.
    """

    external_id = models.CharField(max_length=120, blank=True, db_index=True)
    row_key = models.CharField(max_length=64, db_index=True)
    concept_id = models.CharField(max_length=80, db_index=True)
    une = models.CharField(max_length=20, db_index=True)
    fecha_inicio = models.DateTimeField()
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    cumple_plazo = models.BooleanField(null=True, blank=True)
    sla_kind = models.CharField(max_length=40, blank=True)
    titulo = models.CharField(max_length=255, blank=True)
    tipo_tramite = models.CharField(max_length=120, blank=True)
    source_file = models.CharField(max_length=255, blank=True)
    import_batch_id = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha_inicio"]
        verbose_name = "Expediente PGO (Archivos)"
        verbose_name_plural = "Expedientes PGO (Archivos)"
        constraints = [
            models.UniqueConstraint(
                fields=["import_batch_id", "row_key"],
                name="pgo_expediente_batch_row_key",
            ),
        ]

    def __str__(self):
        return f"{self.concept_id} {self.une} {self.fecha_inicio:%Y-%m-%d}"


class PgoScorecardCacheMeta(models.Model):
    """Metadatos del último snapshot del tablero por puntos (fila única pk=1)."""

    id = models.PositiveSmallIntegerField(primary_key=True, default=1)
    fingerprint = models.CharField(max_length=64)
    computed_at = models.DateTimeField()
    years = models.JSONField(default=list)
    processed_months = models.JSONField(default=dict)

    class Meta:
        verbose_name = "Caché tablero PGO (meta)"
        verbose_name_plural = "Caché tablero PGO (meta)"

    def __str__(self):
        return f"Tablero PGO {self.computed_at:%Y-%m-%d %H:%M} ({self.fingerprint[:8]}…)"


class PgoScorecardCell(models.Model):
    """Celda persistida: año, mes, UNE, concepto."""

    year = models.PositiveSmallIntegerField(db_index=True)
    month = models.PositiveSmallIntegerField(db_index=True)
    une = models.CharField(max_length=20, db_index=True)
    concept_id = models.CharField(max_length=80, db_index=True)
    points = models.FloatField(null=True, blank=True)
    max_points = models.FloatField(default=0)
    confidence = models.CharField(max_length=10, default="none")
    note = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["year", "month", "une", "concept_id"],
                name="pgo_scorecard_cell_uniq",
            ),
        ]
        indexes = [
            models.Index(fields=["year", "month"]),
        ]
        verbose_name = "Celda tablero PGO"
        verbose_name_plural = "Celdas tablero PGO"

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.une} {self.concept_id}"
