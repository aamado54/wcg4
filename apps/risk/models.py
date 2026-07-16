from django.conf import settings
from django.db import models


class RiskOperacion(models.Model):
    entidad = models.ForeignKey(
        "wcgone_core.Entidad",
        on_delete=models.CASCADE,
        related_name="operaciones_riesgo",
    )
    producto = models.ForeignKey(
        "wcgone_core.Producto",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="operaciones_riesgo",
    )
    unidad_negocio = models.ForeignKey(
        "wcgone_core.UnidadNegocio",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="operaciones_riesgo",
    )
    codigo_operacion = models.CharField(max_length=100, db_index=True)
    contrato_numero = models.CharField(max_length=100, blank=True, db_index=True)
    asesor = models.CharField(max_length=150, blank=True)
    moneda = models.CharField(max_length=10, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    monto_original = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=50, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["entidad__nombre", "codigo_operacion"]
        verbose_name = "Operación de riesgo"
        verbose_name_plural = "Operaciones de riesgo"
        constraints = [
            models.UniqueConstraint(
                fields=["entidad", "codigo_operacion"],
                name="uniq_risk_operacion_entidad_codigo",
            ),
        ]

    def __str__(self):
        return f"{self.codigo_operacion} — {self.entidad}"


class RiskOperationSnapshot(models.Model):
    operacion = models.ForeignKey(
        RiskOperacion,
        on_delete=models.CASCADE,
        related_name="snapshots",
    )
    entidad = models.ForeignKey(
        "wcgone_core.Entidad",
        on_delete=models.CASCADE,
        related_name="risk_snapshots",
    )
    fecha_snapshot = models.DateField(db_index=True)
    record_date_raw = models.CharField(max_length=100, blank=True)
    estado_operacion = models.CharField(max_length=100, blank=True)
    producto_nombre_raw = models.CharField(max_length=100, blank=True)
    monthly_rent = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    capital_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    outstanding_installments = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    interest_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    insurance_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    other_charges_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    past_due_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    due_days = models.IntegerField(null=True, blank=True)
    purchase_option_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    initial_rent_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    total_rent_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    archivo_origen = models.CharField(max_length=255, blank=True)
    import_batch = models.ForeignKey(
        "wcgone_core.DataImportBatch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="risk_snapshots",
    )
    payload_raw_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-fecha_snapshot", "operacion_id"]
        verbose_name = "Snapshot operativo de riesgo"
        verbose_name_plural = "Snapshots operativos de riesgo"
        constraints = [
            models.UniqueConstraint(
                fields=["operacion", "fecha_snapshot"],
                name="uniq_risk_snapshot_operacion_fecha",
            ),
        ]

    def __str__(self):
        return f"{self.operacion.codigo_operacion} — {self.fecha_snapshot}"


class EstadoFinanciero(models.Model):
    entidad = models.ForeignKey(
        "wcgone_core.Entidad",
        on_delete=models.CASCADE,
        related_name="estados_financieros",
    )
    fecha_corte = models.DateField()
    auditor_contador = models.CharField(max_length=255, blank=True)
    ventas = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    utilidad_neta = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    activo_corriente = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    activo_no_corriente = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    pasivo_corriente = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    pasivo_no_corriente = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    patrimonio = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    ebitda = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(blank=True)
    import_batch = models.ForeignKey(
        "wcgone_core.DataImportBatch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="estados_financieros",
    )

    class Meta:
        ordering = ["-fecha_corte", "entidad__nombre"]
        verbose_name = "Estado financiero"
        verbose_name_plural = "Estados financieros"
        indexes = [
            models.Index(fields=["entidad", "fecha_corte"]),
        ]

    def __str__(self):
        return f"{self.entidad} — {self.fecha_corte}"


class RiskPagoProgramado(models.Model):
    operacion = models.ForeignKey(
        RiskOperacion,
        on_delete=models.CASCADE,
        related_name="pagos_programados",
    )
    entidad = models.ForeignKey(
        "wcgone_core.Entidad",
        on_delete=models.CASCADE,
        related_name="pagos_programados",
    )
    fecha_programada = models.DateField()
    monto_capital = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    monto_interes = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    monto_mora = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    monto_otros = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    moneda = models.CharField(max_length=10, blank=True)
    estado = models.CharField(max_length=50, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["fecha_programada"]
        verbose_name = "Pago programado"
        verbose_name_plural = "Pagos programados"

    def __str__(self):
        return f"{self.operacion.codigo_operacion} — {self.fecha_programada}"


class RiskPagoRealizado(models.Model):
    operacion = models.ForeignKey(
        RiskOperacion,
        on_delete=models.CASCADE,
        related_name="pagos_realizados",
    )
    entidad = models.ForeignKey(
        "wcgone_core.Entidad",
        on_delete=models.CASCADE,
        related_name="pagos_realizados",
    )
    fecha_pago = models.DateField()
    monto_capital = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    monto_interes = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    monto_mora = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    monto_otros = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    moneda = models.CharField(max_length=10, blank=True)
    referencia = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha_pago"]
        verbose_name = "Pago realizado"
        verbose_name_plural = "Pagos realizados"

    def __str__(self):
        return f"{self.operacion.codigo_operacion} — {self.fecha_pago}"


class ContactoCobranza(models.Model):
    entidad = models.ForeignKey(
        "wcgone_core.Entidad",
        on_delete=models.CASCADE,
        related_name="contactos_cobranza",
    )
    operacion = models.ForeignKey(
        RiskOperacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contactos_cobranza",
    )
    contacto = models.ForeignKey(
        "wcgone_core.Contacto",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contactos_cobranza",
    )
    fecha = models.DateField()
    tipo_contacto = models.CharField(max_length=50)
    resultado = models.CharField(max_length=255, blank=True)
    acuerdo = models.TextField(blank=True)
    fecha_compromiso = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha", "entidad__nombre"]
        verbose_name = "Contacto de cobranza"
        verbose_name_plural = "Contactos de cobranza"

    def __str__(self):
        return f"{self.entidad} — {self.fecha}"


class RiskAlerta(models.Model):
    entidad = models.ForeignKey(
        "wcgone_core.Entidad",
        on_delete=models.CASCADE,
        related_name="alertas_riesgo",
    )
    operacion = models.ForeignKey(
        RiskOperacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alertas",
    )
    fecha_alerta = models.DateField(db_index=True)
    tipo_alerta = models.CharField(max_length=50)
    severidad = models.CharField(max_length=30)
    mensaje = models.TextField()
    activa = models.BooleanField(default=True)
    origen = models.CharField(max_length=100, blank=True)
    detalle_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-fecha_alerta", "-id"]
        verbose_name = "Alerta de riesgo"
        verbose_name_plural = "Alertas de riesgo"

    def __str__(self):
        return f"{self.entidad} — {self.tipo_alerta}"
