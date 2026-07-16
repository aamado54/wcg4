"""Maestros compartidos: entidades, contactos, productos y unidades."""

from django.db import models


class UnidadNegocio(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "Unidad de negocio"
        verbose_name_plural = "Unidades de negocio"

    def __str__(self):
        return self.nombre


class Entidad(models.Model):
    TIPO_CLIENTE = "cliente"
    TIPO_INVERSIONISTA = "inversionista"
    TIPO_AMBOS = "ambos"
    TIPO_PROVEEDOR = "proveedor"
    TIPO_OTRO = "otro"
    TIPO_CHOICES = [
        (TIPO_CLIENTE, "Cliente"),
        (TIPO_INVERSIONISTA, "Inversionista"),
        (TIPO_AMBOS, "Ambos"),
        (TIPO_PROVEEDOR, "Proveedor"),
        (TIPO_OTRO, "Otro"),
    ]

    tipo_entidad = models.CharField(max_length=30, choices=TIPO_CHOICES, default=TIPO_CLIENTE)
    es_persona = models.BooleanField(default=False)
    nombre = models.CharField(max_length=255, db_index=True)
    nombre_comercial = models.CharField(max_length=255, blank=True)
    nit = models.CharField(max_length=50, blank=True, db_index=True)
    pais = models.CharField(max_length=100, blank=True)
    departamento = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    direccion_fiscal = models.TextField(blank=True)
    direccion_operativa = models.TextField(blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    sector_economico = models.CharField(max_length=150, blank=True)
    codigo_sector = models.CharField(max_length=50, blank=True)
    activo = models.BooleanField(default=True)
    categoria_riesgo = models.CharField(max_length=50, blank=True)
    origen = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Entidad"
        verbose_name_plural = "Entidades"
        indexes = [
            models.Index(fields=["activo", "tipo_entidad"]),
        ]

    def __str__(self):
        return self.nombre


class Contacto(models.Model):
    entidad = models.ForeignKey(
        Entidad,
        on_delete=models.CASCADE,
        related_name="contactos",
    )
    nombre = models.CharField(max_length=255)
    cargo = models.CharField(max_length=150, blank=True)
    area = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True, db_index=True)
    telefono_movil = models.CharField(max_length=50, blank=True)
    telefono_oficina = models.CharField(max_length=50, blank=True)
    extension = models.CharField(max_length=20, blank=True)
    es_decisor_credito = models.BooleanField(default=False)
    es_contacto_cobranza = models.BooleanField(default=False)
    es_contacto_operativo = models.BooleanField(default=False)
    nivel_influencia = models.CharField(max_length=50, blank=True)
    nivel_apertura = models.CharField(max_length=50, blank=True)
    notas = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["entidad__nombre", "nombre"]
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        indexes = [
            models.Index(fields=["entidad", "activo"]),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.entidad})"


class Producto(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    tipo_producto = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre


class RelacionEntidadProducto(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="relaciones_producto")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="relaciones_entidad")
    unidad_negocio = models.ForeignKey(
        UnidadNegocio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="relaciones_entidad_producto",
    )
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=50, blank=True)
    monto_aprobado = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    moneda = models.CharField(max_length=10, blank=True)
    codigo_operacion_externo = models.CharField(max_length=100, blank=True, db_index=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["entidad__nombre", "producto__nombre"]
        verbose_name = "Relación entidad-producto"
        verbose_name_plural = "Relaciones entidad-producto"
        indexes = [
            models.Index(fields=["entidad", "producto"]),
        ]

    def __str__(self):
        return f"{self.entidad} / {self.producto}"
