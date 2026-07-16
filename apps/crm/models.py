from django.conf import settings
from django.db import models


class Interaccion(models.Model):
    entidad = models.ForeignKey(
        "wcgone_core.Entidad",
        on_delete=models.CASCADE,
        related_name="interacciones",
    )
    producto = models.ForeignKey(
        "wcgone_core.Producto",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interacciones",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_crm_interacciones",
    )
    fecha = models.DateField(db_index=True)
    hora = models.TimeField(null=True, blank=True)
    tipo_interaccion = models.CharField(max_length=50, db_index=True)
    resumen = models.CharField(max_length=255)
    resultado = models.TextField(blank=True)
    seguimiento_requerido = models.BooleanField(default=False)
    notas = models.TextField(blank=True)
    import_batch = models.ForeignKey(
        "wcgone_core.DataImportBatch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_crm_interacciones",
    )

    class Meta:
        ordering = ["-fecha", "-id"]
        verbose_name = "Interacción"
        verbose_name_plural = "Interacciones"
        indexes = [
            models.Index(fields=["entidad", "fecha"]),
        ]

    def __str__(self):
        return f"{self.entidad} — {self.resumen}"


class Tarea(models.Model):
    entidad = models.ForeignKey(
        "wcgone_core.Entidad",
        on_delete=models.CASCADE,
        related_name="tareas",
    )
    contacto = models.ForeignKey(
        "wcgone_core.Contacto",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tareas",
    )
    asignado_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_crm_tareas",
    )
    fecha_limite = models.DateField(null=True, blank=True)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=20, blank=True)
    estado = models.CharField(max_length=30, default="pendiente")
    completada = models.BooleanField(default=False)
    fecha_completada = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["completada", "fecha_limite", "-id"]
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        indexes = [
            models.Index(fields=["completada", "fecha_limite"]),
            models.Index(fields=["entidad", "estado"]),
        ]

    def __str__(self):
        return f"{self.entidad} — {self.descripcion[:50]}"


class NotaEntidad(models.Model):
    entidad = models.ForeignKey(
        "wcgone_core.Entidad",
        on_delete=models.CASCADE,
        related_name="notas_entidad",
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_notas_entidad",
    )
    fecha = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Nota de entidad"
        verbose_name_plural = "Notas de entidad"

    def __str__(self):
        return f"{self.entidad} — {self.titulo}"
