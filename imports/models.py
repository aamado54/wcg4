import os
import re

from core.models import TimeStampedModel, UNE, Currency
from decimal import Decimal
from django.conf import settings
from django.db import models


def guess_file_format(filename: str) -> str:
    _, ext = os.path.splitext(filename.lower())
    ext = ext.strip('.')
    if ext == 'xlsx':
        return 'XLSX'
    if ext == 'csv':
        return 'CSV'
    if ext == 'tsv':
        return 'TSV'
    return 'OTHER'


def guess_file_type_and_period(filename: str):
    name = filename.lower()
    # Normaliza separadores para detectar "ClientesNuevos", "Clientes_Nuevos", etc.
    compact = re.sub(r"[\s_\-.]+", "", name)

    ym_match = re.search(r"(20\d{2})[-_/](0[1-9]|1[0-2])", name)
    year = None
    month = None

    if ym_match:
        year = int(ym_match.group(1))
        month = int(ym_match.group(2))
    else:
        compact_ym = re.search(r"(20\d{2})(0[1-9]|1[0-2])", name)
        if compact_ym:
            year = int(compact_ym.group(1))
            month = int(compact_ym.group(2))

    if name.startswith("wc") or "estado_resultados" in name or "er_" in name:
        file_type = "FINANCIAL"
    elif "clientesnuevos" in compact:
        file_type = "NEW_CLIENTS"
    elif "ventacruzada" in compact:
        file_type = "CROSS_SALE"
    elif "tiempos" in compact and "estacion" in compact:
        file_type = "STATION_TIMES"
    else:
        file_type = "UNKNOWN"

    return file_type, year, month


class FileUpload(TimeStampedModel):
    TYPE_FINANCIAL = 'FINANCIAL'
    TYPE_NEW_CLIENTS = 'NEW_CLIENTS'
    TYPE_CROSS_SALE = 'CROSS_SALE'
    TYPE_STATION_TIMES = 'STATION_TIMES'
    TYPE_UNKNOWN = 'UNKNOWN'

    TYPE_CHOICES = [
        (TYPE_FINANCIAL, 'Estado financiero (WC*)'),
        (TYPE_NEW_CLIENTS, 'Clientes nuevos'),
        (TYPE_CROSS_SALE, 'Venta cruzada'),
        (TYPE_STATION_TIMES, 'Tiempos de estaciones'),
        (TYPE_UNKNOWN, 'Desconocido'),
    ]

    FORMAT_XLSX = 'XLSX'
    FORMAT_CSV = 'CSV'
    FORMAT_TSV = 'TSV'
    FORMAT_OTHER = 'OTHER'

    FORMAT_CHOICES = [
        (FORMAT_XLSX, 'Excel (.xlsx)'),
        (FORMAT_CSV, 'CSV'),
        (FORMAT_TSV, 'TSV'),
        (FORMAT_OTHER, 'Otro'),
    ]

    STATUS_UPLOADED = 'UPLOADED'
    STATUS_PARSED_OK = 'PARSED_OK'
    STATUS_PARSED_ERROR = 'PARSED_ERROR'

    STATUS_CHOICES = [
        (STATUS_UPLOADED, 'P1. Archivo listo para lectura'),
        (STATUS_PARSED_OK, 'P2. Datos cargados correctamente'),
        (STATUS_PARSED_ERROR, 'E1. Error al leer los datos'),
    ]

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_files',
    )
    original_filename = models.CharField(max_length=255)
    stored_file = models.FileField(upload_to='uploads/')
    file_type_detected = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_UNKNOWN,
    )
    file_format = models.CharField(
        max_length=10,
        choices=FORMAT_CHOICES,
        default=FORMAT_OTHER,
    )
    mime_type = models.CharField(max_length=100, blank=True)
    file_size_bytes = models.BigIntegerField(default=0)
    sha256 = models.CharField(max_length=64, blank=True)
    detected_year = models.PositiveIntegerField(null=True, blank=True)
    detected_month = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_UPLOADED,
    )
    error_summary = models.TextField(blank=True)
    parsing_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Archivo subido'
        verbose_name_plural = 'Archivos subidos'

    def __str__(self):
        return f'{self.original_filename} ({self.file_type_detected})'

    def save(self, *args, **kwargs):
        # Nombre original desde el fichero si está vacío
        if not self.original_filename and self.stored_file:
            self.original_filename = self.stored_file.name

        # Detectar formato si no está definido o es genérico
        if self.original_filename and (not self.file_format or self.file_format == self.FORMAT_OTHER):
            self.file_format = guess_file_format(self.original_filename)

        # Detectar tipo y periodo
        if self.original_filename and (
            self.file_type_detected == self.TYPE_UNKNOWN
            or self.detected_year is None
            or self.detected_month is None
        ):
            file_type, year, month = guess_file_type_and_period(self.original_filename)
            if self.file_type_detected == self.TYPE_UNKNOWN:
                self.file_type_detected = file_type
            if self.detected_year is None and year is not None:
                self.detected_year = year
            if self.detected_month is None and month is not None:
                self.detected_month = month

        # Tamaño de archivo
        if self.stored_file and not self.file_size_bytes:
            try:
                self.file_size_bytes = self.stored_file.size
            except Exception:
                pass

        if self.stored_file and not self.sha256:
            try:
                hasher = hashlib.sha256()
                for chunk in self.stored_file.chunks():
                    hasher.update(chunk)
                self.sha256 = hasher.hexdigest()
                self.stored_file.seek(0)
            except Exception:
                pass

        super().save(*args, **kwargs)

        # Crear encabezados para NO financieros (los financieros los haremos después)
        if self.detected_year and self.detected_month:
            if self.file_type_detected == self.TYPE_NEW_CLIENTS:
                NewClientImportHeader.objects.update_or_create(
                    year=self.detected_year,
                    month=self.detected_month,
                    defaults={"file_upload": self},
                )
            elif self.file_type_detected == self.TYPE_CROSS_SALE:
                CrossSaleImportHeader.objects.update_or_create(
                    year=self.detected_year,
                    month=self.detected_month,
                    defaults={"file_upload": self},
                )
            elif self.file_type_detected == self.TYPE_STATION_TIMES:
                StationTimeImportHeader.objects.update_or_create(
                    year=self.detected_year,
                    month=self.detected_month,
                    defaults={"file_upload": self},
                )          

class FileImportLog(TimeStampedModel):
    LEVEL_INFO = 'INFO'
    LEVEL_WARNING = 'WARNING'
    LEVEL_ERROR = 'ERROR'

    LEVEL_CHOICES = [
        (LEVEL_INFO, 'Info'),
        (LEVEL_WARNING, 'Warning'),
        (LEVEL_ERROR, 'Error'),
    ]

    file_upload = models.ForeignKey(
        FileUpload,
        on_delete=models.CASCADE,
        related_name='logs',
    )
    step_code = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default=LEVEL_INFO)
    message = models.TextField()
    line_number = models.PositiveIntegerField(null=True, blank=True)
    payload_json = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Log de importación'
        verbose_name_plural = 'Logs de importación'

    def __str__(self):
        return f'{self.level} - {self.step_code or ""} ({self.file_upload_id})'


class FinancialStatementImportHeader(TimeStampedModel):
    file_upload = models.OneToOneField(
        FileUpload,
        on_delete=models.CASCADE,
        related_name='financial_header',
    )
    une = models.ForeignKey(
        UNE,
        on_delete=models.CASCADE,
        related_name='financial_imports',
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    statement_type = models.CharField(max_length=50, default='ER')
    source_sheet_name = models.CharField(max_length=50, blank=True)
    source_entity_name = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('une', 'year', 'month', 'statement_type')
        verbose_name = 'Encabezado estado financiero'
        verbose_name_plural = 'Encabezados estados financieros'

    def __str__(self):
        return f'{self.une.code} {self.year}-{self.month:02d} ({self.statement_type})'


class NewClientImportHeader(TimeStampedModel):
    # FK (no OneToOne): un mismo FileUpload puede alimentar varios meses.
    file_upload = models.ForeignKey(
        FileUpload,
        on_delete=models.CASCADE,
        related_name="new_clients_headers",
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    class Meta:
        unique_together = ("year", "month")
        verbose_name = "Encabezado clientes nuevos"
        verbose_name_plural = "Encabezados clientes nuevos"

    def __str__(self):
        return f"Clientes nuevos {self.year}-{self.month:02d}"


class CrossSaleImportHeader(TimeStampedModel):
    file_upload = models.OneToOneField(
        FileUpload,
        on_delete=models.CASCADE,
        related_name='cross_sales_header',
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    class Meta:
        unique_together = ('year', 'month')
        verbose_name = 'Encabezado ventas cruzadas'
        verbose_name_plural = 'Encabezados ventas cruzadas'

    def __str__(self):
        return f'Ventas cruzadas {self.year}-{self.month:02d}'


class CrossSaleImportRow(TimeStampedModel):
    header = models.ForeignKey(
        CrossSaleImportHeader,
        on_delete=models.CASCADE,
        related_name="rows",
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    client_name = models.CharField(max_length=255, blank=True)
    operation_code = models.CharField(max_length=100, blank=True)
    date = models.DateField(null=True, blank=True)

    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cross_sale_rows",
    )

    une_destination = models.ForeignKey(
        UNE,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cross_sales_received",
    )
    une_origin = models.ForeignKey(
        UNE,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cross_sales_sent",
    )

    raw_une_destination = models.CharField(max_length=255, blank=True)
    raw_une_origin = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Detalle venta cruzada"
        verbose_name_plural = "Detalles venta cruzada"

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.client_name} {self.operation_code}"


class StationTimeImportHeader(TimeStampedModel):
    file_upload = models.OneToOneField(
        FileUpload,
        on_delete=models.CASCADE,
        related_name='station_times_header',
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    class Meta:
        unique_together = ('year', 'month')
        verbose_name = 'Encabezado tiempos estaciones'
        verbose_name_plural = 'Encabezados tiempos estaciones'

    def __str__(self):
        return f'Tiempos estaciones {self.year}-{self.month:02d}'


class NewClientImportRow(TimeStampedModel):
    header = models.ForeignKey(
        "imports.NewClientImportHeader",
        on_delete=models.CASCADE,
        related_name="rows",
    )
    une = models.ForeignKey(
        UNE,
        on_delete=models.CASCADE,
        related_name="new_client_import_rows",
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    client_name = models.CharField(max_length=255, blank=True)
    nit = models.CharField(max_length=50, blank=True)
    operation_code = models.CharField(max_length=100, blank=True)
    previous_contracts = models.IntegerField(default=0)

    counts_as_new = models.BooleanField(default=False)

    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="new_client_import_rows",
    )
    amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    source_row_number = models.PositiveIntegerField(null=True, blank=True)
    raw_une_value = models.CharField(max_length=255, blank=True)
    observations = models.TextField(blank=True)

    class Meta:
        ordering = ["year", "month", "une__sort_order", "client_name", "operation_code"]
        verbose_name = "Detalle importado de cliente nuevo"
        verbose_name_plural = "Detalles importados de clientes nuevos"

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.une.code} {self.client_name or self.operation_code}"

  