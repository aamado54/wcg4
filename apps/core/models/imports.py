"""Diccionario de datos y trazabilidad de importaciones."""

from django.conf import settings
from django.db import models


class DataDictionaryField(models.Model):
    modulo = models.CharField(max_length=50, db_index=True)
    nombre_logico = models.CharField(max_length=150)
    tabla_fisica = models.CharField(max_length=100)
    campo_fisico = models.CharField(max_length=100)
    tipo_dato = models.CharField(max_length=50, blank=True)
    definicion = models.TextField(blank=True)
    fuente = models.CharField(max_length=255, blank=True)
    periodicidad = models.CharField(max_length=50, blank=True)
    orden = models.PositiveIntegerField(default=0)
    notas = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["modulo", "orden", "tabla_fisica", "campo_fisico"]
        verbose_name = "Campo de diccionario de datos"
        verbose_name_plural = "Diccionario de datos"
        constraints = [
            models.UniqueConstraint(
                fields=["tabla_fisica", "campo_fisico"],
                name="uniq_data_dictionary_tabla_campo",
            ),
        ]

    def __str__(self):
        return f"{self.tabla_fisica}.{self.campo_fisico}"


class DataImportBatch(models.Model):
    ESTADO_PENDIENTE = "pendiente"
    ESTADO_PROCESANDO = "procesando"
    ESTADO_OK = "ok"
    ESTADO_PARCIAL = "parcial"
    ESTADO_ERROR = "error"
    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, "Pendiente"),
        (ESTADO_PROCESANDO, "Procesando"),
        (ESTADO_OK, "OK"),
        (ESTADO_PARCIAL, "Parcial"),
        (ESTADO_ERROR, "Error"),
    ]

    modulo = models.CharField(max_length=50, db_index=True)
    tipo_importacion = models.CharField(max_length=100)
    archivo_nombre = models.CharField(max_length=255)
    archivo_hash = models.CharField(max_length=128, blank=True)
    archivo_ruta = models.CharField(max_length=500, blank=True)
    fecha_carga = models.DateTimeField(auto_now_add=True, db_index=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_import_batches",
    )
    filas_leidas = models.PositiveIntegerField(default=0)
    filas_validas = models.PositiveIntegerField(default=0)
    filas_error = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha_carga"]
        verbose_name = "Lote de importación"
        verbose_name_plural = "Lotes de importación"

    def __str__(self):
        return f"{self.modulo}/{self.tipo_importacion} — {self.archivo_nombre}"


class DataImportError(models.Model):
    batch = models.ForeignKey(
        DataImportBatch,
        on_delete=models.CASCADE,
        related_name="errores",
    )
    fila_numero = models.PositiveIntegerField()
    campo = models.CharField(max_length=100, blank=True)
    valor_original = models.TextField(blank=True)
    mensaje_error = models.TextField()
    payload_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["batch", "fila_numero"]
        verbose_name = "Error de importación"
        verbose_name_plural = "Errores de importación"

    def __str__(self):
        return f"Lote {self.batch_id} fila {self.fila_numero}"
