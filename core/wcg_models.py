"""Maestro común WCG One — compartido por CRM, Risk, PGO y PGC."""

from django.conf import settings
from django.db import models

from .models import TimeStampedModel, UNE


class UnidadNegocio(TimeStampedModel):
    """
    Unidad de negocio WCG.
    Clave natural importación: `code` (ej. LEASING, FACTORING).
    """

    code = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=120)
    une_pgc = models.ForeignKey(
        UNE,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="unidades_negocio_wcg",
        help_text="Vínculo opcional con UNE existente del PGC.",
    )
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Unidad de negocio"
        verbose_name_plural = "Unidades de negocio"

    def __str__(self):
        return self.nombre


class Entidad(TimeStampedModel):
    """
    Maestro de clientes/prospectos WCG.
    Clave natural importación: `codigo` (preferido) o `nit` si no hay código explícito.
    """
    TIPO_CLIENTE = "CLIENTE"
    TIPO_PROSPECTO = "PROSPECTO"
    TIPO_OTRO = "OTRO"
    TIPO_CHOICES = [
        (TIPO_CLIENTE, "Cliente"),
        (TIPO_PROSPECTO, "Prospecto"),
        (TIPO_OTRO, "Otro"),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    nit = models.CharField(max_length=30, blank=True, db_index=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_CLIENTE)
    unidad_negocio = models.ForeignKey(
        UnidadNegocio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entidades",
    )
    activa = models.BooleanField(default=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Entidad"
        verbose_name_plural = "Entidades"

    def __str__(self):
        return f"{self.codigo} — {self.nombre}"


class Contacto(TimeStampedModel):
    """
    Contacto comercial de una entidad.
    Clave natural importación: (`entidad`, `email`) si hay email; si no (`entidad`, `nombre`).
    """
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="contactos")
    nombre = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=40, blank=True)
    cargo = models.CharField(max_length=120, blank=True)
    es_principal = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["entidad__nombre", "nombre"]
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"

    def __str__(self):
        return f"{self.nombre} ({self.entidad.codigo})"


class Producto(TimeStampedModel):
    """Catálogo de productos. Clave natural: `codigo`."""

    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    unidad_negocio = models.ForeignKey(
        UnidadNegocio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos",
    )
    activo = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre


class RelacionEntidadProducto(TimeStampedModel):
    """Vínculo entidad-producto. Clave natural: (`entidad`, `producto`)."""

    ESTADO_ACTIVO = "ACTIVO"
    ESTADO_INACTIVO = "INACTIVO"
    ESTADO_CHOICES = [
        (ESTADO_ACTIVO, "Activo"),
        (ESTADO_INACTIVO, "Inactivo"),
    ]

    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="productos_relacionados")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="entidades_relacionadas")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_ACTIVO)
    fecha_inicio = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        unique_together = ("entidad", "producto")
        ordering = ["entidad__nombre", "producto__nombre"]
        verbose_name = "Relación entidad-producto"
        verbose_name_plural = "Relaciones entidad-producto"

    def __str__(self):
        return f"{self.entidad.codigo} / {self.producto.codigo}"


class DataDictionary(TimeStampedModel):
    modulo = models.CharField(max_length=30, db_index=True)
    tabla = models.CharField(max_length=80)
    campo = models.CharField(max_length=80)
    etiqueta = models.CharField(max_length=120)
    tipo_dato = models.CharField(max_length=40, blank=True)
    obligatorio = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True)

    class Meta:
        unique_together = ("modulo", "tabla", "campo")
        ordering = ["modulo", "tabla", "campo"]
        verbose_name = "Diccionario de datos"
        verbose_name_plural = "Diccionario de datos"

    def __str__(self):
        return f"{self.modulo}.{self.tabla}.{self.campo}"


class DataImportBatch(TimeStampedModel):
    MODULO_CRM = "CRM"
    MODULO_RISK = "RISK"
    MODULO_PGO = "PGO"
    MODULO_PGC = "PGC"
    MODULO_CHOICES = [
        (MODULO_CRM, "CRM"),
        (MODULO_RISK, "Risk"),
        (MODULO_PGO, "PGO"),
        (MODULO_PGC, "PGC"),
    ]

    STATUS_PENDING = "PENDING"
    STATUS_OK = "OK"
    STATUS_PARTIAL = "PARTIAL"
    STATUS_ERROR = "ERROR"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pendiente"),
        (STATUS_OK, "OK"),
        (STATUS_PARTIAL, "Parcial"),
        (STATUS_ERROR, "Error"),
    ]

    modulo = models.CharField(max_length=20, choices=MODULO_CHOICES)
    tipo_importacion = models.CharField(max_length=80)
    archivo_nombre = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="import_batches",
    )
    filas_leidas = models.PositiveIntegerField(default=0)
    creados = models.PositiveIntegerField(default=0)
    actualizados = models.PositiveIntegerField(default=0)
    errores = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    log_texto = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Lote de importación"
        verbose_name_plural = "Lotes de importación"

    def __str__(self):
        return f"{self.modulo}/{self.tipo_importacion} — {self.archivo_nombre}"
