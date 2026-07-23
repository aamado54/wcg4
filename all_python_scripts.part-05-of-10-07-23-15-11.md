# CONCATENATED .PY FILES

PART_NUMBER=5
TOTAL_PARTS=10

DOCUMENT_MODE=LITERAL_CODE_ARCHIVE
PARSING_PRIORITY=PATH_LITERAL->CONTENT_NUMBERED_BEGIN->CONTENT_BASE64_BEGIN->CONTENT_BEGIN
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
RECORD_SEPARATOR=BEGIN_LITERAL_FILE_RECORD|END_LITERAL_FILE_RECORD
RECORD_BOUNDARY=========== RECORD_BOUNDARY ==========
CONTENT_POLICY=PRESERVE_EXACT_TEXT_WITH_METADATA_AND_NUMBERED_FALLBACK
READING_HINT=Prefer PATH_LITERAL first for file identity. Prefer CONTENT_NUMBERED_BEGIN for faithful line-by-line reading. Use CONTENT_BASE64_BEGIN for exact reconstruction when available. Use CONTENT_BEGIN only as a convenience view. If CONTENT_BEGIN looks compacted, flattened, or visually altered, do not use it to infer exact identifiers, variable names, paths, punctuation grouping, or spacing.
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/models.py
PATH_JSON="imports/models.py"
FILENAME=models.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=397
SIZE_BYTES_UTF8=13034
CONTENT_SHA256=8cc55123a02a8354f76bc912ba615ad6b7676217720f51ffa944a936c28ca1da
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
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

  
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|import os
00002|import re
00003|
00004|from core.models import TimeStampedModel, UNE, Currency
00005|from decimal import Decimal
00006|from django.conf import settings
00007|from django.db import models
00008|
00009|
00010|def guess_file_format(filename: str) -> str:
00011|    _, ext = os.path.splitext(filename.lower())
00012|    ext = ext.strip('.')
00013|    if ext == 'xlsx':
00014|        return 'XLSX'
00015|    if ext == 'csv':
00016|        return 'CSV'
00017|    if ext == 'tsv':
00018|        return 'TSV'
00019|    return 'OTHER'
00020|
00021|
00022|def guess_file_type_and_period(filename: str):
00023|    name = filename.lower()
00024|    # Normaliza separadores para detectar "ClientesNuevos", "Clientes_Nuevos", etc.
00025|    compact = re.sub(r"[\s_\-.]+", "", name)
00026|
00027|    ym_match = re.search(r"(20\d{2})[-_/](0[1-9]|1[0-2])", name)
00028|    year = None
00029|    month = None
00030|
00031|    if ym_match:
00032|        year = int(ym_match.group(1))
00033|        month = int(ym_match.group(2))
00034|    else:
00035|        compact_ym = re.search(r"(20\d{2})(0[1-9]|1[0-2])", name)
00036|        if compact_ym:
00037|            year = int(compact_ym.group(1))
00038|            month = int(compact_ym.group(2))
00039|
00040|    if name.startswith("wc") or "estado_resultados" in name or "er_" in name:
00041|        file_type = "FINANCIAL"
00042|    elif "clientesnuevos" in compact:
00043|        file_type = "NEW_CLIENTS"
00044|    elif "ventacruzada" in compact:
00045|        file_type = "CROSS_SALE"
00046|    elif "tiempos" in compact and "estacion" in compact:
00047|        file_type = "STATION_TIMES"
00048|    else:
00049|        file_type = "UNKNOWN"
00050|
00051|    return file_type, year, month
00052|
00053|
00054|class FileUpload(TimeStampedModel):
00055|    TYPE_FINANCIAL = 'FINANCIAL'
00056|    TYPE_NEW_CLIENTS = 'NEW_CLIENTS'
00057|    TYPE_CROSS_SALE = 'CROSS_SALE'
00058|    TYPE_STATION_TIMES = 'STATION_TIMES'
00059|    TYPE_UNKNOWN = 'UNKNOWN'
00060|
00061|    TYPE_CHOICES = [
00062|        (TYPE_FINANCIAL, 'Estado financiero (WC*)'),
00063|        (TYPE_NEW_CLIENTS, 'Clientes nuevos'),
00064|        (TYPE_CROSS_SALE, 'Venta cruzada'),
00065|        (TYPE_STATION_TIMES, 'Tiempos de estaciones'),
00066|        (TYPE_UNKNOWN, 'Desconocido'),
00067|    ]
00068|
00069|    FORMAT_XLSX = 'XLSX'
00070|    FORMAT_CSV = 'CSV'
00071|    FORMAT_TSV = 'TSV'
00072|    FORMAT_OTHER = 'OTHER'
00073|
00074|    FORMAT_CHOICES = [
00075|        (FORMAT_XLSX, 'Excel (.xlsx)'),
00076|        (FORMAT_CSV, 'CSV'),
00077|        (FORMAT_TSV, 'TSV'),
00078|        (FORMAT_OTHER, 'Otro'),
00079|    ]
00080|
00081|    STATUS_UPLOADED = 'UPLOADED'
00082|    STATUS_PARSED_OK = 'PARSED_OK'
00083|    STATUS_PARSED_ERROR = 'PARSED_ERROR'
00084|
00085|    STATUS_CHOICES = [
00086|        (STATUS_UPLOADED, 'P1. Archivo listo para lectura'),
00087|        (STATUS_PARSED_OK, 'P2. Datos cargados correctamente'),
00088|        (STATUS_PARSED_ERROR, 'E1. Error al leer los datos'),
00089|    ]
00090|
00091|    uploaded_by = models.ForeignKey(
00092|        settings.AUTH_USER_MODEL,
00093|        on_delete=models.SET_NULL,
00094|        null=True,
00095|        blank=True,
00096|        related_name='uploaded_files',
00097|    )
00098|    original_filename = models.CharField(max_length=255)
00099|    stored_file = models.FileField(upload_to='uploads/')
00100|    file_type_detected = models.CharField(
00101|        max_length=20,
00102|        choices=TYPE_CHOICES,
00103|        default=TYPE_UNKNOWN,
00104|    )
00105|    file_format = models.CharField(
00106|        max_length=10,
00107|        choices=FORMAT_CHOICES,
00108|        default=FORMAT_OTHER,
00109|    )
00110|    mime_type = models.CharField(max_length=100, blank=True)
00111|    file_size_bytes = models.BigIntegerField(default=0)
00112|    sha256 = models.CharField(max_length=64, blank=True)
00113|    detected_year = models.PositiveIntegerField(null=True, blank=True)
00114|    detected_month = models.PositiveIntegerField(null=True, blank=True)
00115|    status = models.CharField(
00116|        max_length=20,
00117|        choices=STATUS_CHOICES,
00118|        default=STATUS_UPLOADED,
00119|    )
00120|    error_summary = models.TextField(blank=True)
00121|    parsing_notes = models.TextField(blank=True)
00122|
00123|    class Meta:
00124|        ordering = ['-created_at']
00125|        verbose_name = 'Archivo subido'
00126|        verbose_name_plural = 'Archivos subidos'
00127|
00128|    def __str__(self):
00129|        return f'{self.original_filename} ({self.file_type_detected})'
00130|
00131|    def save(self, *args, **kwargs):
00132|        # Nombre original desde el fichero si está vacío
00133|        if not self.original_filename and self.stored_file:
00134|            self.original_filename = self.stored_file.name
00135|
00136|        # Detectar formato si no está definido o es genérico
00137|        if self.original_filename and (not self.file_format or self.file_format == self.FORMAT_OTHER):
00138|            self.file_format = guess_file_format(self.original_filename)
00139|
00140|        # Detectar tipo y periodo
00141|        if self.original_filename and (
00142|            self.file_type_detected == self.TYPE_UNKNOWN
00143|            or self.detected_year is None
00144|            or self.detected_month is None
00145|        ):
00146|            file_type, year, month = guess_file_type_and_period(self.original_filename)
00147|            if self.file_type_detected == self.TYPE_UNKNOWN:
00148|                self.file_type_detected = file_type
00149|            if self.detected_year is None and year is not None:
00150|                self.detected_year = year
00151|            if self.detected_month is None and month is not None:
00152|                self.detected_month = month
00153|
00154|        # Tamaño de archivo
00155|        if self.stored_file and not self.file_size_bytes:
00156|            try:
00157|                self.file_size_bytes = self.stored_file.size
00158|            except Exception:
00159|                pass
00160|
00161|        if self.stored_file and not self.sha256:
00162|            try:
00163|                hasher = hashlib.sha256()
00164|                for chunk in self.stored_file.chunks():
00165|                    hasher.update(chunk)
00166|                self.sha256 = hasher.hexdigest()
00167|                self.stored_file.seek(0)
00168|            except Exception:
00169|                pass
00170|
00171|        super().save(*args, **kwargs)
00172|
00173|        # Crear encabezados para NO financieros (los financieros los haremos después)
00174|        if self.detected_year and self.detected_month:
00175|            if self.file_type_detected == self.TYPE_NEW_CLIENTS:
00176|                NewClientImportHeader.objects.update_or_create(
00177|                    year=self.detected_year,
00178|                    month=self.detected_month,
00179|                    defaults={"file_upload": self},
00180|                )
00181|            elif self.file_type_detected == self.TYPE_CROSS_SALE:
00182|                CrossSaleImportHeader.objects.update_or_create(
00183|                    year=self.detected_year,
00184|                    month=self.detected_month,
00185|                    defaults={"file_upload": self},
00186|                )
00187|            elif self.file_type_detected == self.TYPE_STATION_TIMES:
00188|                StationTimeImportHeader.objects.update_or_create(
00189|                    year=self.detected_year,
00190|                    month=self.detected_month,
00191|                    defaults={"file_upload": self},
00192|                )          
00193|
00194|class FileImportLog(TimeStampedModel):
00195|    LEVEL_INFO = 'INFO'
00196|    LEVEL_WARNING = 'WARNING'
00197|    LEVEL_ERROR = 'ERROR'
00198|
00199|    LEVEL_CHOICES = [
00200|        (LEVEL_INFO, 'Info'),
00201|        (LEVEL_WARNING, 'Warning'),
00202|        (LEVEL_ERROR, 'Error'),
00203|    ]
00204|
00205|    file_upload = models.ForeignKey(
00206|        FileUpload,
00207|        on_delete=models.CASCADE,
00208|        related_name='logs',
00209|    )
00210|    step_code = models.CharField(max_length=100, blank=True)
00211|    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default=LEVEL_INFO)
00212|    message = models.TextField()
00213|    line_number = models.PositiveIntegerField(null=True, blank=True)
00214|    payload_json = models.JSONField(blank=True, null=True)
00215|
00216|    class Meta:
00217|        ordering = ['created_at']
00218|        verbose_name = 'Log de importación'
00219|        verbose_name_plural = 'Logs de importación'
00220|
00221|    def __str__(self):
00222|        return f'{self.level} - {self.step_code or ""} ({self.file_upload_id})'
00223|
00224|
00225|class FinancialStatementImportHeader(TimeStampedModel):
00226|    file_upload = models.OneToOneField(
00227|        FileUpload,
00228|        on_delete=models.CASCADE,
00229|        related_name='financial_header',
00230|    )
00231|    une = models.ForeignKey(
00232|        UNE,
00233|        on_delete=models.CASCADE,
00234|        related_name='financial_imports',
00235|    )
00236|    year = models.PositiveIntegerField()
00237|    month = models.PositiveIntegerField()
00238|    statement_type = models.CharField(max_length=50, default='ER')
00239|    source_sheet_name = models.CharField(max_length=50, blank=True)
00240|    source_entity_name = models.CharField(max_length=255, blank=True)
00241|    notes = models.TextField(blank=True)
00242|
00243|    class Meta:
00244|        unique_together = ('une', 'year', 'month', 'statement_type')
00245|        verbose_name = 'Encabezado estado financiero'
00246|        verbose_name_plural = 'Encabezados estados financieros'
00247|
00248|    def __str__(self):
00249|        return f'{self.une.code} {self.year}-{self.month:02d} ({self.statement_type})'
00250|
00251|
00252|class NewClientImportHeader(TimeStampedModel):
00253|    # FK (no OneToOne): un mismo FileUpload puede alimentar varios meses.
00254|    file_upload = models.ForeignKey(
00255|        FileUpload,
00256|        on_delete=models.CASCADE,
00257|        related_name="new_clients_headers",
00258|    )
00259|    year = models.PositiveIntegerField()
00260|    month = models.PositiveIntegerField()
00261|
00262|    class Meta:
00263|        unique_together = ("year", "month")
00264|        verbose_name = "Encabezado clientes nuevos"
00265|        verbose_name_plural = "Encabezados clientes nuevos"
00266|
00267|    def __str__(self):
00268|        return f"Clientes nuevos {self.year}-{self.month:02d}"
00269|
00270|
00271|class CrossSaleImportHeader(TimeStampedModel):
00272|    file_upload = models.OneToOneField(
00273|        FileUpload,
00274|        on_delete=models.CASCADE,
00275|        related_name='cross_sales_header',
00276|    )
00277|    year = models.PositiveIntegerField()
00278|    month = models.PositiveIntegerField()
00279|
00280|    class Meta:
00281|        unique_together = ('year', 'month')
00282|        verbose_name = 'Encabezado ventas cruzadas'
00283|        verbose_name_plural = 'Encabezados ventas cruzadas'
00284|
00285|    def __str__(self):
00286|        return f'Ventas cruzadas {self.year}-{self.month:02d}'
00287|
00288|
00289|class CrossSaleImportRow(TimeStampedModel):
00290|    header = models.ForeignKey(
00291|        CrossSaleImportHeader,
00292|        on_delete=models.CASCADE,
00293|        related_name="rows",
00294|    )
00295|    year = models.PositiveIntegerField()
00296|    month = models.PositiveIntegerField()
00297|
00298|    client_name = models.CharField(max_length=255, blank=True)
00299|    operation_code = models.CharField(max_length=100, blank=True)
00300|    date = models.DateField(null=True, blank=True)
00301|
00302|    currency = models.ForeignKey(
00303|        Currency,
00304|        on_delete=models.SET_NULL,
00305|        null=True,
00306|        blank=True,
00307|        related_name="cross_sale_rows",
00308|    )
00309|
00310|    une_destination = models.ForeignKey(
00311|        UNE,
00312|        on_delete=models.SET_NULL,
00313|        null=True,
00314|        blank=True,
00315|        related_name="cross_sales_received",
00316|    )
00317|    une_origin = models.ForeignKey(
00318|        UNE,
00319|        on_delete=models.SET_NULL,
00320|        null=True,
00321|        blank=True,
00322|        related_name="cross_sales_sent",
00323|    )
00324|
00325|    raw_une_destination = models.CharField(max_length=255, blank=True)
00326|    raw_une_origin = models.CharField(max_length=255, blank=True)
00327|
00328|    class Meta:
00329|        verbose_name = "Detalle venta cruzada"
00330|        verbose_name_plural = "Detalles venta cruzada"
00331|
00332|    def __str__(self):
00333|        return f"{self.year}-{self.month:02d} {self.client_name} {self.operation_code}"
00334|
00335|
00336|class StationTimeImportHeader(TimeStampedModel):
00337|    file_upload = models.OneToOneField(
00338|        FileUpload,
00339|        on_delete=models.CASCADE,
00340|        related_name='station_times_header',
00341|    )
00342|    year = models.PositiveIntegerField()
00343|    month = models.PositiveIntegerField()
00344|
00345|    class Meta:
00346|        unique_together = ('year', 'month')
00347|        verbose_name = 'Encabezado tiempos estaciones'
00348|        verbose_name_plural = 'Encabezados tiempos estaciones'
00349|
00350|    def __str__(self):
00351|        return f'Tiempos estaciones {self.year}-{self.month:02d}'
00352|
00353|
00354|class NewClientImportRow(TimeStampedModel):
00355|    header = models.ForeignKey(
00356|        "imports.NewClientImportHeader",
00357|        on_delete=models.CASCADE,
00358|        related_name="rows",
00359|    )
00360|    une = models.ForeignKey(
00361|        UNE,
00362|        on_delete=models.CASCADE,
00363|        related_name="new_client_import_rows",
00364|    )
00365|    year = models.PositiveIntegerField()
00366|    month = models.PositiveIntegerField()
00367|
00368|    client_name = models.CharField(max_length=255, blank=True)
00369|    nit = models.CharField(max_length=50, blank=True)
00370|    operation_code = models.CharField(max_length=100, blank=True)
00371|    previous_contracts = models.IntegerField(default=0)
00372|
00373|    counts_as_new = models.BooleanField(default=False)
00374|
00375|    currency = models.ForeignKey(
00376|        Currency,
00377|        on_delete=models.SET_NULL,
00378|        null=True,
00379|        blank=True,
00380|        related_name="new_client_import_rows",
00381|    )
00382|    amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00383|
00384|    source_row_number = models.PositiveIntegerField(null=True, blank=True)
00385|    raw_une_value = models.CharField(max_length=255, blank=True)
00386|    observations = models.TextField(blank=True)
00387|
00388|    class Meta:
00389|        ordering = ["year", "month", "une__sort_order", "client_name", "operation_code"]
00390|        verbose_name = "Detalle importado de cliente nuevo"
00391|        verbose_name_plural = "Detalles importados de clientes nuevos"
00392|
00393|    def __str__(self):
00394|        return f"{self.year}-{self.month:02d} {self.une.code} {self.client_name or self.operation_code}"
00395|
00396|  
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
aW1wb3J0IG9zCmltcG9ydCByZQoKZnJvbSBjb3JlLm1vZGVscyBpbXBvcnQgVGltZVN0YW1wZWRNb2RlbCwgVU5FLCBDdXJyZW5jeQpmcm9tIGRlY2ltYWwgaW1wb3J0IERlY2ltYWwKZnJvbSBkamFuZ28uY29uZiBpbXBvcnQgc2V0dGluZ3MKZnJvbSBkamFuZ28uZGIgaW1wb3J0IG1vZGVscwoKCmRlZiBndWVzc19maWxlX2Zvcm1hdChmaWxlbmFtZTogc3RyKSAtPiBzdHI6CiAgICBfLCBleHQgPSBvcy5wYXRoLnNwbGl0ZXh0KGZpbGVuYW1lLmxvd2VyKCkpCiAgICBleHQgPSBleHQuc3RyaXAoJy4nKQogICAgaWYgZXh0ID09ICd4bHN4JzoKICAgICAgICByZXR1cm4gJ1hMU1gnCiAgICBpZiBleHQgPT0gJ2Nzdic6CiAgICAgICAgcmV0dXJuICdDU1YnCiAgICBpZiBleHQgPT0gJ3Rzdic6CiAgICAgICAgcmV0dXJuICdUU1YnCiAgICByZXR1cm4gJ09USEVSJwoKCmRlZiBndWVzc19maWxlX3R5cGVfYW5kX3BlcmlvZChmaWxlbmFtZTogc3RyKToKICAgIG5hbWUgPSBmaWxlbmFtZS5sb3dlcigpCiAgICAjIE5vcm1hbGl6YSBzZXBhcmFkb3JlcyBwYXJhIGRldGVjdGFyICJDbGllbnRlc051ZXZvcyIsICJDbGllbnRlc19OdWV2b3MiLCBldGMuCiAgICBjb21wYWN0ID0gcmUuc3ViKHIiW1xzX1wtLl0rIiwgIiIsIG5hbWUpCgogICAgeW1fbWF0Y2ggPSByZS5zZWFyY2gociIoMjBcZHsyfSlbLV8vXSgwWzEtOV18MVswLTJdKSIsIG5hbWUpCiAgICB5ZWFyID0gTm9uZQogICAgbW9udGggPSBOb25lCgogICAgaWYgeW1fbWF0Y2g6CiAgICAgICAgeWVhciA9IGludCh5bV9tYXRjaC5ncm91cCgxKSkKICAgICAgICBtb250aCA9IGludCh5bV9tYXRjaC5ncm91cCgyKSkKICAgIGVsc2U6CiAgICAgICAgY29tcGFjdF95bSA9IHJlLnNlYXJjaChyIigyMFxkezJ9KSgwWzEtOV18MVswLTJdKSIsIG5hbWUpCiAgICAgICAgaWYgY29tcGFjdF95bToKICAgICAgICAgICAgeWVhciA9IGludChjb21wYWN0X3ltLmdyb3VwKDEpKQogICAgICAgICAgICBtb250aCA9IGludChjb21wYWN0X3ltLmdyb3VwKDIpKQoKICAgIGlmIG5hbWUuc3RhcnRzd2l0aCgid2MiKSBvciAiZXN0YWRvX3Jlc3VsdGFkb3MiIGluIG5hbWUgb3IgImVyXyIgaW4gbmFtZToKICAgICAgICBmaWxlX3R5cGUgPSAiRklOQU5DSUFMIgogICAgZWxpZiAiY2xpZW50ZXNudWV2b3MiIGluIGNvbXBhY3Q6CiAgICAgICAgZmlsZV90eXBlID0gIk5FV19DTElFTlRTIgogICAgZWxpZiAidmVudGFjcnV6YWRhIiBpbiBjb21wYWN0OgogICAgICAgIGZpbGVfdHlwZSA9ICJDUk9TU19TQUxFIgogICAgZWxpZiAidGllbXBvcyIgaW4gY29tcGFjdCBhbmQgImVzdGFjaW9uIiBpbiBjb21wYWN0OgogICAgICAgIGZpbGVfdHlwZSA9ICJTVEFUSU9OX1RJTUVTIgogICAgZWxzZToKICAgICAgICBmaWxlX3R5cGUgPSAiVU5LTk9XTiIKCiAgICByZXR1cm4gZmlsZV90eXBlLCB5ZWFyLCBtb250aAoKCmNsYXNzIEZpbGVVcGxvYWQoVGltZVN0YW1wZWRNb2RlbCk6CiAgICBUWVBFX0ZJTkFOQ0lBTCA9ICdGSU5BTkNJQUwnCiAgICBUWVBFX05FV19DTElFTlRTID0gJ05FV19DTElFTlRTJwogICAgVFlQRV9DUk9TU19TQUxFID0gJ0NST1NTX1NBTEUnCiAgICBUWVBFX1NUQVRJT05fVElNRVMgPSAnU1RBVElPTl9USU1FUycKICAgIFRZUEVfVU5LTk9XTiA9ICdVTktOT1dOJwoKICAgIFRZUEVfQ0hPSUNFUyA9IFsKICAgICAgICAoVFlQRV9GSU5BTkNJQUwsICdFc3RhZG8gZmluYW5jaWVybyAoV0MqKScpLAogICAgICAgIChUWVBFX05FV19DTElFTlRTLCAnQ2xpZW50ZXMgbnVldm9zJyksCiAgICAgICAgKFRZUEVfQ1JPU1NfU0FMRSwgJ1ZlbnRhIGNydXphZGEnKSwKICAgICAgICAoVFlQRV9TVEFUSU9OX1RJTUVTLCAnVGllbXBvcyBkZSBlc3RhY2lvbmVzJyksCiAgICAgICAgKFRZUEVfVU5LTk9XTiwgJ0Rlc2Nvbm9jaWRvJyksCiAgICBdCgogICAgRk9STUFUX1hMU1ggPSAnWExTWCcKICAgIEZPUk1BVF9DU1YgPSAnQ1NWJwogICAgRk9STUFUX1RTViA9ICdUU1YnCiAgICBGT1JNQVRfT1RIRVIgPSAnT1RIRVInCgogICAgRk9STUFUX0NIT0lDRVMgPSBbCiAgICAgICAgKEZPUk1BVF9YTFNYLCAnRXhjZWwgKC54bHN4KScpLAogICAgICAgIChGT1JNQVRfQ1NWLCAnQ1NWJyksCiAgICAgICAgKEZPUk1BVF9UU1YsICdUU1YnKSwKICAgICAgICAoRk9STUFUX09USEVSLCAnT3RybycpLAogICAgXQoKICAgIFNUQVRVU19VUExPQURFRCA9ICdVUExPQURFRCcKICAgIFNUQVRVU19QQVJTRURfT0sgPSAnUEFSU0VEX09LJwogICAgU1RBVFVTX1BBUlNFRF9FUlJPUiA9ICdQQVJTRURfRVJST1InCgogICAgU1RBVFVTX0NIT0lDRVMgPSBbCiAgICAgICAgKFNUQVRVU19VUExPQURFRCwgJ1AxLiBBcmNoaXZvIGxpc3RvIHBhcmEgbGVjdHVyYScpLAogICAgICAgIChTVEFUVVNfUEFSU0VEX09LLCAnUDIuIERhdG9zIGNhcmdhZG9zIGNvcnJlY3RhbWVudGUnKSwKICAgICAgICAoU1RBVFVTX1BBUlNFRF9FUlJPUiwgJ0UxLiBFcnJvciBhbCBsZWVyIGxvcyBkYXRvcycpLAogICAgXQoKICAgIHVwbG9hZGVkX2J5ID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgc2V0dGluZ3MuQVVUSF9VU0VSX01PREVMLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSd1cGxvYWRlZF9maWxlcycsCiAgICApCiAgICBvcmlnaW5hbF9maWxlbmFtZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yNTUpCiAgICBzdG9yZWRfZmlsZSA9IG1vZGVscy5GaWxlRmllbGQodXBsb2FkX3RvPSd1cGxvYWRzLycpCiAgICBmaWxlX3R5cGVfZGV0ZWN0ZWQgPSBtb2RlbHMuQ2hhckZpZWxkKAogICAgICAgIG1heF9sZW5ndGg9MjAsCiAgICAgICAgY2hvaWNlcz1UWVBFX0NIT0lDRVMsCiAgICAgICAgZGVmYXVsdD1UWVBFX1VOS05PV04sCiAgICApCiAgICBmaWxlX2Zvcm1hdCA9IG1vZGVscy5DaGFyRmllbGQoCiAgICAgICAgbWF4X2xlbmd0aD0xMCwKICAgICAgICBjaG9pY2VzPUZPUk1BVF9DSE9JQ0VTLAogICAgICAgIGRlZmF1bHQ9Rk9STUFUX09USEVSLAogICAgKQogICAgbWltZV90eXBlID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwMCwgYmxhbms9VHJ1ZSkKICAgIGZpbGVfc2l6ZV9ieXRlcyA9IG1vZGVscy5CaWdJbnRlZ2VyRmllbGQoZGVmYXVsdD0wKQogICAgc2hhMjU2ID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTY0LCBibGFuaz1UcnVlKQogICAgZGV0ZWN0ZWRfeWVhciA9IG1vZGVscy5Qb3NpdGl2ZUludGVnZXJGaWVsZChudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBkZXRlY3RlZF9tb250aCA9IG1vZGVscy5Qb3NpdGl2ZUludGVnZXJGaWVsZChudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBzdGF0dXMgPSBtb2RlbHMuQ2hhckZpZWxkKAogICAgICAgIG1heF9sZW5ndGg9MjAsCiAgICAgICAgY2hvaWNlcz1TVEFUVVNfQ0hPSUNFUywKICAgICAgICBkZWZhdWx0PVNUQVRVU19VUExPQURFRCwKICAgICkKICAgIGVycm9yX3N1bW1hcnkgPSBtb2RlbHMuVGV4dEZpZWxkKGJsYW5rPVRydWUpCiAgICBwYXJzaW5nX25vdGVzID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbJy1jcmVhdGVkX2F0J10KICAgICAgICB2ZXJib3NlX25hbWUgPSAnQXJjaGl2byBzdWJpZG8nCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICdBcmNoaXZvcyBzdWJpZG9zJwoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmJ3tzZWxmLm9yaWdpbmFsX2ZpbGVuYW1lfSAoe3NlbGYuZmlsZV90eXBlX2RldGVjdGVkfSknCgogICAgZGVmIHNhdmUoc2VsZiwgKmFyZ3MsICoqa3dhcmdzKToKICAgICAgICAjIE5vbWJyZSBvcmlnaW5hbCBkZXNkZSBlbCBmaWNoZXJvIHNpIGVzdMOhIHZhY8OtbwogICAgICAgIGlmIG5vdCBzZWxmLm9yaWdpbmFsX2ZpbGVuYW1lIGFuZCBzZWxmLnN0b3JlZF9maWxlOgogICAgICAgICAgICBzZWxmLm9yaWdpbmFsX2ZpbGVuYW1lID0gc2VsZi5zdG9yZWRfZmlsZS5uYW1lCgogICAgICAgICMgRGV0ZWN0YXIgZm9ybWF0byBzaSBubyBlc3TDoSBkZWZpbmlkbyBvIGVzIGdlbsOpcmljbwogICAgICAgIGlmIHNlbGYub3JpZ2luYWxfZmlsZW5hbWUgYW5kIChub3Qgc2VsZi5maWxlX2Zvcm1hdCBvciBzZWxmLmZpbGVfZm9ybWF0ID09IHNlbGYuRk9STUFUX09USEVSKToKICAgICAgICAgICAgc2VsZi5maWxlX2Zvcm1hdCA9IGd1ZXNzX2ZpbGVfZm9ybWF0KHNlbGYub3JpZ2luYWxfZmlsZW5hbWUpCgogICAgICAgICMgRGV0ZWN0YXIgdGlwbyB5IHBlcmlvZG8KICAgICAgICBpZiBzZWxmLm9yaWdpbmFsX2ZpbGVuYW1lIGFuZCAoCiAgICAgICAgICAgIHNlbGYuZmlsZV90eXBlX2RldGVjdGVkID09IHNlbGYuVFlQRV9VTktOT1dOCiAgICAgICAgICAgIG9yIHNlbGYuZGV0ZWN0ZWRfeWVhciBpcyBOb25lCiAgICAgICAgICAgIG9yIHNlbGYuZGV0ZWN0ZWRfbW9udGggaXMgTm9uZQogICAgICAgICk6CiAgICAgICAgICAgIGZpbGVfdHlwZSwgeWVhciwgbW9udGggPSBndWVzc19maWxlX3R5cGVfYW5kX3BlcmlvZChzZWxmLm9yaWdpbmFsX2ZpbGVuYW1lKQogICAgICAgICAgICBpZiBzZWxmLmZpbGVfdHlwZV9kZXRlY3RlZCA9PSBzZWxmLlRZUEVfVU5LTk9XTjoKICAgICAgICAgICAgICAgIHNlbGYuZmlsZV90eXBlX2RldGVjdGVkID0gZmlsZV90eXBlCiAgICAgICAgICAgIGlmIHNlbGYuZGV0ZWN0ZWRfeWVhciBpcyBOb25lIGFuZCB5ZWFyIGlzIG5vdCBOb25lOgogICAgICAgICAgICAgICAgc2VsZi5kZXRlY3RlZF95ZWFyID0geWVhcgogICAgICAgICAgICBpZiBzZWxmLmRldGVjdGVkX21vbnRoIGlzIE5vbmUgYW5kIG1vbnRoIGlzIG5vdCBOb25lOgogICAgICAgICAgICAgICAgc2VsZi5kZXRlY3RlZF9tb250aCA9IG1vbnRoCgogICAgICAgICMgVGFtYcOxbyBkZSBhcmNoaXZvCiAgICAgICAgaWYgc2VsZi5zdG9yZWRfZmlsZSBhbmQgbm90IHNlbGYuZmlsZV9zaXplX2J5dGVzOgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICBzZWxmLmZpbGVfc2l6ZV9ieXRlcyA9IHNlbGYuc3RvcmVkX2ZpbGUuc2l6ZQogICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uOgogICAgICAgICAgICAgICAgcGFzcwoKICAgICAgICBpZiBzZWxmLnN0b3JlZF9maWxlIGFuZCBub3Qgc2VsZi5zaGEyNTY6CiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIGhhc2hlciA9IGhhc2hsaWIuc2hhMjU2KCkKICAgICAgICAgICAgICAgIGZvciBjaHVuayBpbiBzZWxmLnN0b3JlZF9maWxlLmNodW5rcygpOgogICAgICAgICAgICAgICAgICAgIGhhc2hlci51cGRhdGUoY2h1bmspCiAgICAgICAgICAgICAgICBzZWxmLnNoYTI1NiA9IGhhc2hlci5oZXhkaWdlc3QoKQogICAgICAgICAgICAgICAgc2VsZi5zdG9yZWRfZmlsZS5zZWVrKDApCiAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgICAgICAgICBwYXNzCgogICAgICAgIHN1cGVyKCkuc2F2ZSgqYXJncywgKiprd2FyZ3MpCgogICAgICAgICMgQ3JlYXIgZW5jYWJlemFkb3MgcGFyYSBOTyBmaW5hbmNpZXJvcyAobG9zIGZpbmFuY2llcm9zIGxvcyBoYXJlbW9zIGRlc3B1w6lzKQogICAgICAgIGlmIHNlbGYuZGV0ZWN0ZWRfeWVhciBhbmQgc2VsZi5kZXRlY3RlZF9tb250aDoKICAgICAgICAgICAgaWYgc2VsZi5maWxlX3R5cGVfZGV0ZWN0ZWQgPT0gc2VsZi5UWVBFX05FV19DTElFTlRTOgogICAgICAgICAgICAgICAgTmV3Q2xpZW50SW1wb3J0SGVhZGVyLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgICAgICAgICB5ZWFyPXNlbGYuZGV0ZWN0ZWRfeWVhciwKICAgICAgICAgICAgICAgICAgICBtb250aD1zZWxmLmRldGVjdGVkX21vbnRoLAogICAgICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsiZmlsZV91cGxvYWQiOiBzZWxmfSwKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgZWxpZiBzZWxmLmZpbGVfdHlwZV9kZXRlY3RlZCA9PSBzZWxmLlRZUEVfQ1JPU1NfU0FMRToKICAgICAgICAgICAgICAgIENyb3NzU2FsZUltcG9ydEhlYWRlci5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICAgICAgeWVhcj1zZWxmLmRldGVjdGVkX3llYXIsCiAgICAgICAgICAgICAgICAgICAgbW9udGg9c2VsZi5kZXRlY3RlZF9tb250aCwKICAgICAgICAgICAgICAgICAgICBkZWZhdWx0cz17ImZpbGVfdXBsb2FkIjogc2VsZn0sCiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgIGVsaWYgc2VsZi5maWxlX3R5cGVfZGV0ZWN0ZWQgPT0gc2VsZi5UWVBFX1NUQVRJT05fVElNRVM6CiAgICAgICAgICAgICAgICBTdGF0aW9uVGltZUltcG9ydEhlYWRlci5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICAgICAgeWVhcj1zZWxmLmRldGVjdGVkX3llYXIsCiAgICAgICAgICAgICAgICAgICAgbW9udGg9c2VsZi5kZXRlY3RlZF9tb250aCwKICAgICAgICAgICAgICAgICAgICBkZWZhdWx0cz17ImZpbGVfdXBsb2FkIjogc2VsZn0sCiAgICAgICAgICAgICAgICApICAgICAgICAgIAoKY2xhc3MgRmlsZUltcG9ydExvZyhUaW1lU3RhbXBlZE1vZGVsKToKICAgIExFVkVMX0lORk8gPSAnSU5GTycKICAgIExFVkVMX1dBUk5JTkcgPSAnV0FSTklORycKICAgIExFVkVMX0VSUk9SID0gJ0VSUk9SJwoKICAgIExFVkVMX0NIT0lDRVMgPSBbCiAgICAgICAgKExFVkVMX0lORk8sICdJbmZvJyksCiAgICAgICAgKExFVkVMX1dBUk5JTkcsICdXYXJuaW5nJyksCiAgICAgICAgKExFVkVMX0VSUk9SLCAnRXJyb3InKSwKICAgIF0KCiAgICBmaWxlX3VwbG9hZCA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIEZpbGVVcGxvYWQsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLAogICAgICAgIHJlbGF0ZWRfbmFtZT0nbG9ncycsCiAgICApCiAgICBzdGVwX2NvZGUgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAwLCBibGFuaz1UcnVlKQogICAgbGV2ZWwgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAsIGNob2ljZXM9TEVWRUxfQ0hPSUNFUywgZGVmYXVsdD1MRVZFTF9JTkZPKQogICAgbWVzc2FnZSA9IG1vZGVscy5UZXh0RmllbGQoKQogICAgbGluZV9udW1iZXIgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQobnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgcGF5bG9hZF9qc29uID0gbW9kZWxzLkpTT05GaWVsZChibGFuaz1UcnVlLCBudWxsPVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICBvcmRlcmluZyA9IFsnY3JlYXRlZF9hdCddCiAgICAgICAgdmVyYm9zZV9uYW1lID0gJ0xvZyBkZSBpbXBvcnRhY2nDs24nCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICdMb2dzIGRlIGltcG9ydGFjacOzbicKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZid7c2VsZi5sZXZlbH0gLSB7c2VsZi5zdGVwX2NvZGUgb3IgIiJ9ICh7c2VsZi5maWxlX3VwbG9hZF9pZH0pJwoKCmNsYXNzIEZpbmFuY2lhbFN0YXRlbWVudEltcG9ydEhlYWRlcihUaW1lU3RhbXBlZE1vZGVsKToKICAgIGZpbGVfdXBsb2FkID0gbW9kZWxzLk9uZVRvT25lRmllbGQoCiAgICAgICAgRmlsZVVwbG9hZCwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSdmaW5hbmNpYWxfaGVhZGVyJywKICAgICkKICAgIHVuZSA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIFVORSwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSdmaW5hbmNpYWxfaW1wb3J0cycsCiAgICApCiAgICB5ZWFyID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKCkKICAgIG1vbnRoID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKCkKICAgIHN0YXRlbWVudF90eXBlID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTUwLCBkZWZhdWx0PSdFUicpCiAgICBzb3VyY2Vfc2hlZXRfbmFtZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD01MCwgYmxhbms9VHJ1ZSkKICAgIHNvdXJjZV9lbnRpdHlfbmFtZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yNTUsIGJsYW5rPVRydWUpCiAgICBub3RlcyA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIHVuaXF1ZV90b2dldGhlciA9ICgndW5lJywgJ3llYXInLCAnbW9udGgnLCAnc3RhdGVtZW50X3R5cGUnKQogICAgICAgIHZlcmJvc2VfbmFtZSA9ICdFbmNhYmV6YWRvIGVzdGFkbyBmaW5hbmNpZXJvJwogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAnRW5jYWJlemFkb3MgZXN0YWRvcyBmaW5hbmNpZXJvcycKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZid7c2VsZi51bmUuY29kZX0ge3NlbGYueWVhcn0te3NlbGYubW9udGg6MDJkfSAoe3NlbGYuc3RhdGVtZW50X3R5cGV9KScKCgpjbGFzcyBOZXdDbGllbnRJbXBvcnRIZWFkZXIoVGltZVN0YW1wZWRNb2RlbCk6CiAgICAjIEZLIChubyBPbmVUb09uZSk6IHVuIG1pc21vIEZpbGVVcGxvYWQgcHVlZGUgYWxpbWVudGFyIHZhcmlvcyBtZXNlcy4KICAgIGZpbGVfdXBsb2FkID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgRmlsZVVwbG9hZCwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJuZXdfY2xpZW50c19oZWFkZXJzIiwKICAgICkKICAgIHllYXIgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoKQogICAgbW9udGggPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgdW5pcXVlX3RvZ2V0aGVyID0gKCJ5ZWFyIiwgIm1vbnRoIikKICAgICAgICB2ZXJib3NlX25hbWUgPSAiRW5jYWJlemFkbyBjbGllbnRlcyBudWV2b3MiCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJFbmNhYmV6YWRvcyBjbGllbnRlcyBudWV2b3MiCgogICAgZGVmIF9fc3RyX18oc2VsZik6CiAgICAgICAgcmV0dXJuIGYiQ2xpZW50ZXMgbnVldm9zIHtzZWxmLnllYXJ9LXtzZWxmLm1vbnRoOjAyZH0iCgoKY2xhc3MgQ3Jvc3NTYWxlSW1wb3J0SGVhZGVyKFRpbWVTdGFtcGVkTW9kZWwpOgogICAgZmlsZV91cGxvYWQgPSBtb2RlbHMuT25lVG9PbmVGaWVsZCgKICAgICAgICBGaWxlVXBsb2FkLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSwKICAgICAgICByZWxhdGVkX25hbWU9J2Nyb3NzX3NhbGVzX2hlYWRlcicsCiAgICApCiAgICB5ZWFyID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKCkKICAgIG1vbnRoID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKCkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIHVuaXF1ZV90b2dldGhlciA9ICgneWVhcicsICdtb250aCcpCiAgICAgICAgdmVyYm9zZV9uYW1lID0gJ0VuY2FiZXphZG8gdmVudGFzIGNydXphZGFzJwogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAnRW5jYWJlemFkb3MgdmVudGFzIGNydXphZGFzJwoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmJ1ZlbnRhcyBjcnV6YWRhcyB7c2VsZi55ZWFyfS17c2VsZi5tb250aDowMmR9JwoKCmNsYXNzIENyb3NzU2FsZUltcG9ydFJvdyhUaW1lU3RhbXBlZE1vZGVsKToKICAgIGhlYWRlciA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIENyb3NzU2FsZUltcG9ydEhlYWRlciwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJyb3dzIiwKICAgICkKICAgIHllYXIgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoKQogICAgbW9udGggPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoKQoKICAgIGNsaWVudF9uYW1lID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTI1NSwgYmxhbms9VHJ1ZSkKICAgIG9wZXJhdGlvbl9jb2RlID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwMCwgYmxhbms9VHJ1ZSkKICAgIGRhdGUgPSBtb2RlbHMuRGF0ZUZpZWxkKG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKCiAgICBjdXJyZW5jeSA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIEN1cnJlbmN5LAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJjcm9zc19zYWxlX3Jvd3MiLAogICAgKQoKICAgIHVuZV9kZXN0aW5hdGlvbiA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIFVORSwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0iY3Jvc3Nfc2FsZXNfcmVjZWl2ZWQiLAogICAgKQogICAgdW5lX29yaWdpbiA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIFVORSwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0iY3Jvc3Nfc2FsZXNfc2VudCIsCiAgICApCgogICAgcmF3X3VuZV9kZXN0aW5hdGlvbiA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yNTUsIGJsYW5rPVRydWUpCiAgICByYXdfdW5lX29yaWdpbiA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yNTUsIGJsYW5rPVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICB2ZXJib3NlX25hbWUgPSAiRGV0YWxsZSB2ZW50YSBjcnV6YWRhIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiRGV0YWxsZXMgdmVudGEgY3J1emFkYSIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi55ZWFyfS17c2VsZi5tb250aDowMmR9IHtzZWxmLmNsaWVudF9uYW1lfSB7c2VsZi5vcGVyYXRpb25fY29kZX0iCgoKY2xhc3MgU3RhdGlvblRpbWVJbXBvcnRIZWFkZXIoVGltZVN0YW1wZWRNb2RlbCk6CiAgICBmaWxlX3VwbG9hZCA9IG1vZGVscy5PbmVUb09uZUZpZWxkKAogICAgICAgIEZpbGVVcGxvYWQsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLAogICAgICAgIHJlbGF0ZWRfbmFtZT0nc3RhdGlvbl90aW1lc19oZWFkZXInLAogICAgKQogICAgeWVhciA9IG1vZGVscy5Qb3NpdGl2ZUludGVnZXJGaWVsZCgpCiAgICBtb250aCA9IG1vZGVscy5Qb3NpdGl2ZUludGVnZXJGaWVsZCgpCgogICAgY2xhc3MgTWV0YToKICAgICAgICB1bmlxdWVfdG9nZXRoZXIgPSAoJ3llYXInLCAnbW9udGgnKQogICAgICAgIHZlcmJvc2VfbmFtZSA9ICdFbmNhYmV6YWRvIHRpZW1wb3MgZXN0YWNpb25lcycKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gJ0VuY2FiZXphZG9zIHRpZW1wb3MgZXN0YWNpb25lcycKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZidUaWVtcG9zIGVzdGFjaW9uZXMge3NlbGYueWVhcn0te3NlbGYubW9udGg6MDJkfScKCgpjbGFzcyBOZXdDbGllbnRJbXBvcnRSb3coVGltZVN0YW1wZWRNb2RlbCk6CiAgICBoZWFkZXIgPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICAiaW1wb3J0cy5OZXdDbGllbnRJbXBvcnRIZWFkZXIiLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSwKICAgICAgICByZWxhdGVkX25hbWU9InJvd3MiLAogICAgKQogICAgdW5lID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgVU5FLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSwKICAgICAgICByZWxhdGVkX25hbWU9Im5ld19jbGllbnRfaW1wb3J0X3Jvd3MiLAogICAgKQogICAgeWVhciA9IG1vZGVscy5Qb3NpdGl2ZUludGVnZXJGaWVsZCgpCiAgICBtb250aCA9IG1vZGVscy5Qb3NpdGl2ZUludGVnZXJGaWVsZCgpCgogICAgY2xpZW50X25hbWUgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MjU1LCBibGFuaz1UcnVlKQogICAgbml0ID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTUwLCBibGFuaz1UcnVlKQogICAgb3BlcmF0aW9uX2NvZGUgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAwLCBibGFuaz1UcnVlKQogICAgcHJldmlvdXNfY29udHJhY3RzID0gbW9kZWxzLkludGVnZXJGaWVsZChkZWZhdWx0PTApCgogICAgY291bnRzX2FzX25ldyA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1GYWxzZSkKCiAgICBjdXJyZW5jeSA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIEN1cnJlbmN5LAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJuZXdfY2xpZW50X2ltcG9ydF9yb3dzIiwKICAgICkKICAgIGFtb3VudCA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9MiwgbnVsbD1UcnVlLCBibGFuaz1UcnVlKQoKICAgIHNvdXJjZV9yb3dfbnVtYmVyID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIHJhd191bmVfdmFsdWUgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MjU1LCBibGFuaz1UcnVlKQogICAgb2JzZXJ2YXRpb25zID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbInllYXIiLCAibW9udGgiLCAidW5lX19zb3J0X29yZGVyIiwgImNsaWVudF9uYW1lIiwgIm9wZXJhdGlvbl9jb2RlIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiRGV0YWxsZSBpbXBvcnRhZG8gZGUgY2xpZW50ZSBudWV2byIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIkRldGFsbGVzIGltcG9ydGFkb3MgZGUgY2xpZW50ZXMgbnVldm9zIgoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLnllYXJ9LXtzZWxmLm1vbnRoOjAyZH0ge3NlbGYudW5lLmNvZGV9IHtzZWxmLmNsaWVudF9uYW1lIG9yIHNlbGYub3BlcmF0aW9uX2NvZGV9IgoKICA=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/tests.py
PATH_JSON="imports/tests.py"
FILENAME=tests.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=58
SIZE_BYTES_UTF8=2228
CONTENT_SHA256=be0136d67f04ad6636562c4d356880d3e1d0272701d7072b473de4a8e296b34e
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Tests de autodetección de importaciones (3 capas)."""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

from imports.detection import (
    TYPE_CRM_CLIENTES,
    TYPE_PGO_TICKETS,
    detect_from_columns,
    detect_from_name,
    detect_file,
    _merge_detections,
)


class DetectionNameTests(SimpleTestCase):
    def test_clientes_nuevos_by_name(self):
        r = detect_from_name("ClientesNuevos_2024-03.xlsx")
        self.assertIsNotNone(r)
        self.assertEqual(r.tipo, "new_clients")
        self.assertGreaterEqual(r.confidence, 0.8)

    def test_crm_infoclientes_by_name(self):
        r = detect_from_name("InfoClientes_WCG.xlsx")
        self.assertEqual(r.tipo, TYPE_CRM_CLIENTES)


class DetectionStructureTests(SimpleTestCase):
    def test_pgo_columns(self):
        r = detect_from_columns({"id", "titulo", "estado", "fecha_apertura"})
        self.assertIsNotNone(r)
        self.assertEqual(r.tipo, TYPE_PGO_TICKETS)


class DetectionMergeTests(SimpleTestCase):
    def test_agreement_high_confidence(self):
        by_name = detect_from_name("crm_clientes.xlsx")
        by_cols = detect_from_columns({"nit", "nombre_cliente", "wcf"})
        merged = _merge_detections(by_name, by_cols, None)
        self.assertEqual(merged.tipo, TYPE_CRM_CLIENTES)
        self.assertTrue(merged.can_auto_import)

    def test_conflict_is_ambiguous(self):
        by_name = detect_from_name("pgo_tickets_control.xlsx")
        by_cols = detect_from_columns({"nit", "nombre", "wcf"})
        merged = _merge_detections(by_name, by_cols, None)
        self.assertTrue(merged.ambiguous)
        self.assertFalse(merged.can_auto_import)


class DetectionFileTests(SimpleTestCase):
    def test_csv_crm_detect(self):
        content = b"NIT,NombreCliente,WCF\n123456789,Acme,1\n987654321,Beta,0\n111222333,Gamma,1\n"
        f = SimpleUploadedFile("InfoClientes.csv", content, content_type="text/csv")
        result = detect_file(f)
        self.assertEqual(result.tipo, TYPE_CRM_CLIENTES)
        self.assertTrue(result.can_auto_import)
        self.assertTrue(any("CRM" in r or "NIT" in r or "nit" in r for r in result.reasons) or "combinada" in result.layer)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Tests de autodetección de importaciones (3 capas)."""
00002|
00003|from django.core.files.uploadedfile import SimpleUploadedFile
00004|from django.test import SimpleTestCase
00005|
00006|from imports.detection import (
00007|    TYPE_CRM_CLIENTES,
00008|    TYPE_PGO_TICKETS,
00009|    detect_from_columns,
00010|    detect_from_name,
00011|    detect_file,
00012|    _merge_detections,
00013|)
00014|
00015|
00016|class DetectionNameTests(SimpleTestCase):
00017|    def test_clientes_nuevos_by_name(self):
00018|        r = detect_from_name("ClientesNuevos_2024-03.xlsx")
00019|        self.assertIsNotNone(r)
00020|        self.assertEqual(r.tipo, "new_clients")
00021|        self.assertGreaterEqual(r.confidence, 0.8)
00022|
00023|    def test_crm_infoclientes_by_name(self):
00024|        r = detect_from_name("InfoClientes_WCG.xlsx")
00025|        self.assertEqual(r.tipo, TYPE_CRM_CLIENTES)
00026|
00027|
00028|class DetectionStructureTests(SimpleTestCase):
00029|    def test_pgo_columns(self):
00030|        r = detect_from_columns({"id", "titulo", "estado", "fecha_apertura"})
00031|        self.assertIsNotNone(r)
00032|        self.assertEqual(r.tipo, TYPE_PGO_TICKETS)
00033|
00034|
00035|class DetectionMergeTests(SimpleTestCase):
00036|    def test_agreement_high_confidence(self):
00037|        by_name = detect_from_name("crm_clientes.xlsx")
00038|        by_cols = detect_from_columns({"nit", "nombre_cliente", "wcf"})
00039|        merged = _merge_detections(by_name, by_cols, None)
00040|        self.assertEqual(merged.tipo, TYPE_CRM_CLIENTES)
00041|        self.assertTrue(merged.can_auto_import)
00042|
00043|    def test_conflict_is_ambiguous(self):
00044|        by_name = detect_from_name("pgo_tickets_control.xlsx")
00045|        by_cols = detect_from_columns({"nit", "nombre", "wcf"})
00046|        merged = _merge_detections(by_name, by_cols, None)
00047|        self.assertTrue(merged.ambiguous)
00048|        self.assertFalse(merged.can_auto_import)
00049|
00050|
00051|class DetectionFileTests(SimpleTestCase):
00052|    def test_csv_crm_detect(self):
00053|        content = b"NIT,NombreCliente,WCF\n123456789,Acme,1\n987654321,Beta,0\n111222333,Gamma,1\n"
00054|        f = SimpleUploadedFile("InfoClientes.csv", content, content_type="text/csv")
00055|        result = detect_file(f)
00056|        self.assertEqual(result.tipo, TYPE_CRM_CLIENTES)
00057|        self.assertTrue(result.can_auto_import)
00058|        self.assertTrue(any("CRM" in r or "NIT" in r or "nit" in r for r in result.reasons) or "combinada" in result.layer)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiVGVzdHMgZGUgYXV0b2RldGVjY2nDs24gZGUgaW1wb3J0YWNpb25lcyAoMyBjYXBhcykuIiIiCgpmcm9tIGRqYW5nby5jb3JlLmZpbGVzLnVwbG9hZGVkZmlsZSBpbXBvcnQgU2ltcGxlVXBsb2FkZWRGaWxlCmZyb20gZGphbmdvLnRlc3QgaW1wb3J0IFNpbXBsZVRlc3RDYXNlCgpmcm9tIGltcG9ydHMuZGV0ZWN0aW9uIGltcG9ydCAoCiAgICBUWVBFX0NSTV9DTElFTlRFUywKICAgIFRZUEVfUEdPX1RJQ0tFVFMsCiAgICBkZXRlY3RfZnJvbV9jb2x1bW5zLAogICAgZGV0ZWN0X2Zyb21fbmFtZSwKICAgIGRldGVjdF9maWxlLAogICAgX21lcmdlX2RldGVjdGlvbnMsCikKCgpjbGFzcyBEZXRlY3Rpb25OYW1lVGVzdHMoU2ltcGxlVGVzdENhc2UpOgogICAgZGVmIHRlc3RfY2xpZW50ZXNfbnVldm9zX2J5X25hbWUoc2VsZik6CiAgICAgICAgciA9IGRldGVjdF9mcm9tX25hbWUoIkNsaWVudGVzTnVldm9zXzIwMjQtMDMueGxzeCIpCiAgICAgICAgc2VsZi5hc3NlcnRJc05vdE5vbmUocikKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKHIudGlwbywgIm5ld19jbGllbnRzIikKICAgICAgICBzZWxmLmFzc2VydEdyZWF0ZXJFcXVhbChyLmNvbmZpZGVuY2UsIDAuOCkKCiAgICBkZWYgdGVzdF9jcm1faW5mb2NsaWVudGVzX2J5X25hbWUoc2VsZik6CiAgICAgICAgciA9IGRldGVjdF9mcm9tX25hbWUoIkluZm9DbGllbnRlc19XQ0cueGxzeCIpCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChyLnRpcG8sIFRZUEVfQ1JNX0NMSUVOVEVTKQoKCmNsYXNzIERldGVjdGlvblN0cnVjdHVyZVRlc3RzKFNpbXBsZVRlc3RDYXNlKToKICAgIGRlZiB0ZXN0X3Bnb19jb2x1bW5zKHNlbGYpOgogICAgICAgIHIgPSBkZXRlY3RfZnJvbV9jb2x1bW5zKHsiaWQiLCAidGl0dWxvIiwgImVzdGFkbyIsICJmZWNoYV9hcGVydHVyYSJ9KQogICAgICAgIHNlbGYuYXNzZXJ0SXNOb3ROb25lKHIpCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChyLnRpcG8sIFRZUEVfUEdPX1RJQ0tFVFMpCgoKY2xhc3MgRGV0ZWN0aW9uTWVyZ2VUZXN0cyhTaW1wbGVUZXN0Q2FzZSk6CiAgICBkZWYgdGVzdF9hZ3JlZW1lbnRfaGlnaF9jb25maWRlbmNlKHNlbGYpOgogICAgICAgIGJ5X25hbWUgPSBkZXRlY3RfZnJvbV9uYW1lKCJjcm1fY2xpZW50ZXMueGxzeCIpCiAgICAgICAgYnlfY29scyA9IGRldGVjdF9mcm9tX2NvbHVtbnMoeyJuaXQiLCAibm9tYnJlX2NsaWVudGUiLCAid2NmIn0pCiAgICAgICAgbWVyZ2VkID0gX21lcmdlX2RldGVjdGlvbnMoYnlfbmFtZSwgYnlfY29scywgTm9uZSkKICAgICAgICBzZWxmLmFzc2VydEVxdWFsKG1lcmdlZC50aXBvLCBUWVBFX0NSTV9DTElFTlRFUykKICAgICAgICBzZWxmLmFzc2VydFRydWUobWVyZ2VkLmNhbl9hdXRvX2ltcG9ydCkKCiAgICBkZWYgdGVzdF9jb25mbGljdF9pc19hbWJpZ3VvdXMoc2VsZik6CiAgICAgICAgYnlfbmFtZSA9IGRldGVjdF9mcm9tX25hbWUoInBnb190aWNrZXRzX2NvbnRyb2wueGxzeCIpCiAgICAgICAgYnlfY29scyA9IGRldGVjdF9mcm9tX2NvbHVtbnMoeyJuaXQiLCAibm9tYnJlIiwgIndjZiJ9KQogICAgICAgIG1lcmdlZCA9IF9tZXJnZV9kZXRlY3Rpb25zKGJ5X25hbWUsIGJ5X2NvbHMsIE5vbmUpCiAgICAgICAgc2VsZi5hc3NlcnRUcnVlKG1lcmdlZC5hbWJpZ3VvdXMpCiAgICAgICAgc2VsZi5hc3NlcnRGYWxzZShtZXJnZWQuY2FuX2F1dG9faW1wb3J0KQoKCmNsYXNzIERldGVjdGlvbkZpbGVUZXN0cyhTaW1wbGVUZXN0Q2FzZSk6CiAgICBkZWYgdGVzdF9jc3ZfY3JtX2RldGVjdChzZWxmKToKICAgICAgICBjb250ZW50ID0gYiJOSVQsTm9tYnJlQ2xpZW50ZSxXQ0ZcbjEyMzQ1Njc4OSxBY21lLDFcbjk4NzY1NDMyMSxCZXRhLDBcbjExMTIyMjMzMyxHYW1tYSwxXG4iCiAgICAgICAgZiA9IFNpbXBsZVVwbG9hZGVkRmlsZSgiSW5mb0NsaWVudGVzLmNzdiIsIGNvbnRlbnQsIGNvbnRlbnRfdHlwZT0idGV4dC9jc3YiKQogICAgICAgIHJlc3VsdCA9IGRldGVjdF9maWxlKGYpCiAgICAgICAgc2VsZi5hc3NlcnRFcXVhbChyZXN1bHQudGlwbywgVFlQRV9DUk1fQ0xJRU5URVMpCiAgICAgICAgc2VsZi5hc3NlcnRUcnVlKHJlc3VsdC5jYW5fYXV0b19pbXBvcnQpCiAgICAgICAgc2VsZi5hc3NlcnRUcnVlKGFueSgiQ1JNIiBpbiByIG9yICJOSVQiIGluIHIgb3IgIm5pdCIgaW4gciBmb3IgciBpbiByZXN1bHQucmVhc29ucykgb3IgImNvbWJpbmFkYSIgaW4gcmVzdWx0LmxheWVyKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/urls.py
PATH_JSON="imports/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=11
SIZE_BYTES_UTF8=453
CONTENT_SHA256=7dbe591ebbe93907971535bdaf680570108bebd094206751acbc010b6c9560d5
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.urls import path
from . import views

app_name = "imports"

urlpatterns = [
    path("", views.import_hub, name="import_hub"),
    path("<int:file_id>/process-new-clients/", views.process_new_clients, name="process_new_clients"),
    path("<int:file_id>/process-cross-sale/", views.process_cross_sale, name="process_cross_sale"),
    path("<int:file_id>/process-station-times/", views.process_station_times, name="process_station_times"),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.urls import path
00002|from . import views
00003|
00004|app_name = "imports"
00005|
00006|urlpatterns = [
00007|    path("", views.import_hub, name="import_hub"),
00008|    path("<int:file_id>/process-new-clients/", views.process_new_clients, name="process_new_clients"),
00009|    path("<int:file_id>/process-cross-sale/", views.process_cross_sale, name="process_cross_sale"),
00010|    path("<int:file_id>/process-station-times/", views.process_station_times, name="process_station_times"),
00011|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aApmcm9tIC4gaW1wb3J0IHZpZXdzCgphcHBfbmFtZSA9ICJpbXBvcnRzIgoKdXJscGF0dGVybnMgPSBbCiAgICBwYXRoKCIiLCB2aWV3cy5pbXBvcnRfaHViLCBuYW1lPSJpbXBvcnRfaHViIiksCiAgICBwYXRoKCI8aW50OmZpbGVfaWQ+L3Byb2Nlc3MtbmV3LWNsaWVudHMvIiwgdmlld3MucHJvY2Vzc19uZXdfY2xpZW50cywgbmFtZT0icHJvY2Vzc19uZXdfY2xpZW50cyIpLAogICAgcGF0aCgiPGludDpmaWxlX2lkPi9wcm9jZXNzLWNyb3NzLXNhbGUvIiwgdmlld3MucHJvY2Vzc19jcm9zc19zYWxlLCBuYW1lPSJwcm9jZXNzX2Nyb3NzX3NhbGUiKSwKICAgIHBhdGgoIjxpbnQ6ZmlsZV9pZD4vcHJvY2Vzcy1zdGF0aW9uLXRpbWVzLyIsIHZpZXdzLnByb2Nlc3Nfc3RhdGlvbl90aW1lcywgbmFtZT0icHJvY2Vzc19zdGF0aW9uX3RpbWVzIiksCl0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=imports/views.py
PATH_JSON="imports/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=187
SIZE_BYTES_UTF8=7443
CONTENT_SHA256=e44ec03d18879890e24a3bbd6a43be2c5483eb69ba6c1d7182c6f8fe8002f2f2
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
# imports/views.py

from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.management import call_command
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from core.wcg_models import DataImportBatch
from pgc.admin_utils import parse_period

from .detection import ALL_IMPORTABLE, TYPE_LABELS, TYPE_UNKNOWN, detect_file
from .dispatch import run_import
from .forms import GeneralImportForm
from .models import FileUpload


def _redirect_imports_to_admin(request, block: str | None = None):
    year, month = parse_period(request)
    url = f"{reverse('pgc:admin_monthly')}?year={year}&month={month}"
    if block:
        url += f"&block={block}"
    return redirect(url)


@login_required
def import_hub(request):
    """Administración → Importación General (punto único CRM / PGO / Risk / PGC)."""
    result = None
    detection_preview = None
    form = GeneralImportForm()

    if request.method == "POST":
        action = request.POST.get("action", "import")
        form = GeneralImportForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.cleaned_data["archivo"]
            tipo_forzado = form.cleaned_data.get("tipo_forzado") or None
            if action == "detect":
                detection_preview = detect_file(uploaded)
                uploaded.seek(0)
                form = GeneralImportForm(
                    initial={
                        "tipo_forzado": (
                            detection_preview.tipo
                            if detection_preview.tipo != TYPE_UNKNOWN
                            else ""
                        )
                    }
                )
                level = messages.WARNING if detection_preview.ambiguous else messages.INFO
                messages.add_message(
                    request,
                    level,
                    f"Detección: {detection_preview.label} "
                    f"({int(detection_preview.confidence * 100)}% · capa {detection_preview.layer}). "
                    f"{'Seleccione el tipo manualmente — hay ambigüedad. ' if detection_preview.ambiguous else ''}"
                    f"Vuelva a seleccionar el archivo y confirme la importación.",
                )
            else:
                result = run_import(request.user, uploaded, tipo_forzado=tipo_forzado or None)
                if result.ok:
                    messages.success(request, result.message)
                    form = GeneralImportForm()
                elif result.needs_manual:
                    messages.warning(request, result.message)
                    detection_preview = result.detection
                    form = GeneralImportForm(
                        initial={
                            "tipo_forzado": (
                                result.detection.tipo
                                if result.detection.tipo != TYPE_UNKNOWN
                                else ""
                            )
                        }
                    )
                else:
                    messages.warning(request, result.message or "Importación incompleta.")
                    form = GeneralImportForm()

    batches = DataImportBatch.objects.select_related("uploaded_by").order_by("-created_at")[:25]
    uploads = FileUpload.objects.order_by("-created_at")[:15]

    return render(
        request,
        "imports/general_hub.html",
        {
            "form": form,
            "result": result,
            "detection_preview": detection_preview,
            "batches": batches,
            "uploads": uploads,
            "type_labels": TYPE_LABELS,
            "importable_types": [(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE],
            "breadcrumbs": [
                {"label": "Inicio", "url": reverse("portal:home")},
                {"label": "Administración"},
                {"label": "Importación General"},
            ],
        },
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def process_new_clients(request, file_id):
    upload = get_object_or_404(FileUpload, id=file_id)

    if request.method == "POST":
        if upload.file_type_detected != FileUpload.TYPE_NEW_CLIENTS:
            messages.error(request, "Este archivo no es de tipo Clientes nuevos.")
            return _redirect_imports_to_admin(request, "new_clients")

        if not upload.stored_file:
            messages.error(request, "El archivo no tiene fichero almacenado.")
            return _redirect_imports_to_admin(request, "new_clients")

        file_path = Path(upload.stored_file.path)
        if not file_path.exists():
            messages.error(request, f"El archivo físico no existe: {file_path}")
            return _redirect_imports_to_admin(request, "new_clients")

        try:
            call_command(
                "import_clientes_nuevos",
                path=str(file_path),
                file_upload_id=upload.id,
            )
            messages.success(
                request,
                f"Clientes nuevos procesados correctamente desde {upload.original_filename}.",
            )
            upload.status = FileUpload.STATUS_PARSED_OK
            upload.save(update_fields=["status"])
        except Exception as exc:
            messages.error(request, f"Error al procesar clientes nuevos: {exc}")
            upload.status = FileUpload.STATUS_PARSED_ERROR
            upload.error_summary = str(exc)[:500]
            upload.save(update_fields=["status", "error_summary"])

    return _redirect_imports_to_admin(request, "new_clients")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def process_cross_sale(request, file_id):
    upload = get_object_or_404(FileUpload, id=file_id)

    if request.method == "POST":
        if upload.file_type_detected != FileUpload.TYPE_CROSS_SALE:
            messages.error(request, "Este archivo no es de tipo Venta cruzada.")
            return _redirect_imports_to_admin(request, "cross_sale")

        file_path = Path(upload.stored_file.path)
        if not file_path.exists():
            messages.error(request, f"El archivo físico no existe: {file_path}")
            return _redirect_imports_to_admin(request, "cross_sale")

        try:
            call_command("import_venta_cruzada", path=str(file_path))
            messages.success(
                request,
                f"Venta cruzada procesada correctamente desde {upload.original_filename}.",
            )
            upload.status = FileUpload.STATUS_PARSED_OK
            upload.save(update_fields=["status"])
        except Exception as exc:
            messages.error(request, f"Error al procesar venta cruzada: {exc}")
            upload.status = FileUpload.STATUS_PARSED_ERROR
            upload.error_summary = str(exc)[:500]
            upload.save(update_fields=["status", "error_summary"])

    return _redirect_imports_to_admin(request, "cross_sale")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def process_station_times(request, file_id):
    upload = get_object_or_404(FileUpload, id=file_id)
    if request.method == "POST":
        messages.warning(
            request,
            "El procesamiento de tiempos de estación aún no está implementado.",
        )
    return _redirect_imports_to_admin(request)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|# imports/views.py
00002|
00003|from pathlib import Path
00004|
00005|from django.contrib import messages
00006|from django.contrib.auth.decorators import login_required, user_passes_test
00007|from django.core.management import call_command
00008|from django.shortcuts import get_object_or_404, redirect, render
00009|from django.urls import reverse
00010|
00011|from core.wcg_models import DataImportBatch
00012|from pgc.admin_utils import parse_period
00013|
00014|from .detection import ALL_IMPORTABLE, TYPE_LABELS, TYPE_UNKNOWN, detect_file
00015|from .dispatch import run_import
00016|from .forms import GeneralImportForm
00017|from .models import FileUpload
00018|
00019|
00020|def _redirect_imports_to_admin(request, block: str | None = None):
00021|    year, month = parse_period(request)
00022|    url = f"{reverse('pgc:admin_monthly')}?year={year}&month={month}"
00023|    if block:
00024|        url += f"&block={block}"
00025|    return redirect(url)
00026|
00027|
00028|@login_required
00029|def import_hub(request):
00030|    """Administración → Importación General (punto único CRM / PGO / Risk / PGC)."""
00031|    result = None
00032|    detection_preview = None
00033|    form = GeneralImportForm()
00034|
00035|    if request.method == "POST":
00036|        action = request.POST.get("action", "import")
00037|        form = GeneralImportForm(request.POST, request.FILES)
00038|        if form.is_valid():
00039|            uploaded = form.cleaned_data["archivo"]
00040|            tipo_forzado = form.cleaned_data.get("tipo_forzado") or None
00041|            if action == "detect":
00042|                detection_preview = detect_file(uploaded)
00043|                uploaded.seek(0)
00044|                form = GeneralImportForm(
00045|                    initial={
00046|                        "tipo_forzado": (
00047|                            detection_preview.tipo
00048|                            if detection_preview.tipo != TYPE_UNKNOWN
00049|                            else ""
00050|                        )
00051|                    }
00052|                )
00053|                level = messages.WARNING if detection_preview.ambiguous else messages.INFO
00054|                messages.add_message(
00055|                    request,
00056|                    level,
00057|                    f"Detección: {detection_preview.label} "
00058|                    f"({int(detection_preview.confidence * 100)}% · capa {detection_preview.layer}). "
00059|                    f"{'Seleccione el tipo manualmente — hay ambigüedad. ' if detection_preview.ambiguous else ''}"
00060|                    f"Vuelva a seleccionar el archivo y confirme la importación.",
00061|                )
00062|            else:
00063|                result = run_import(request.user, uploaded, tipo_forzado=tipo_forzado or None)
00064|                if result.ok:
00065|                    messages.success(request, result.message)
00066|                    form = GeneralImportForm()
00067|                elif result.needs_manual:
00068|                    messages.warning(request, result.message)
00069|                    detection_preview = result.detection
00070|                    form = GeneralImportForm(
00071|                        initial={
00072|                            "tipo_forzado": (
00073|                                result.detection.tipo
00074|                                if result.detection.tipo != TYPE_UNKNOWN
00075|                                else ""
00076|                            )
00077|                        }
00078|                    )
00079|                else:
00080|                    messages.warning(request, result.message or "Importación incompleta.")
00081|                    form = GeneralImportForm()
00082|
00083|    batches = DataImportBatch.objects.select_related("uploaded_by").order_by("-created_at")[:25]
00084|    uploads = FileUpload.objects.order_by("-created_at")[:15]
00085|
00086|    return render(
00087|        request,
00088|        "imports/general_hub.html",
00089|        {
00090|            "form": form,
00091|            "result": result,
00092|            "detection_preview": detection_preview,
00093|            "batches": batches,
00094|            "uploads": uploads,
00095|            "type_labels": TYPE_LABELS,
00096|            "importable_types": [(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE],
00097|            "breadcrumbs": [
00098|                {"label": "Inicio", "url": reverse("portal:home")},
00099|                {"label": "Administración"},
00100|                {"label": "Importación General"},
00101|            ],
00102|        },
00103|    )
00104|
00105|
00106|@login_required
00107|@user_passes_test(lambda u: u.is_superuser)
00108|def process_new_clients(request, file_id):
00109|    upload = get_object_or_404(FileUpload, id=file_id)
00110|
00111|    if request.method == "POST":
00112|        if upload.file_type_detected != FileUpload.TYPE_NEW_CLIENTS:
00113|            messages.error(request, "Este archivo no es de tipo Clientes nuevos.")
00114|            return _redirect_imports_to_admin(request, "new_clients")
00115|
00116|        if not upload.stored_file:
00117|            messages.error(request, "El archivo no tiene fichero almacenado.")
00118|            return _redirect_imports_to_admin(request, "new_clients")
00119|
00120|        file_path = Path(upload.stored_file.path)
00121|        if not file_path.exists():
00122|            messages.error(request, f"El archivo físico no existe: {file_path}")
00123|            return _redirect_imports_to_admin(request, "new_clients")
00124|
00125|        try:
00126|            call_command(
00127|                "import_clientes_nuevos",
00128|                path=str(file_path),
00129|                file_upload_id=upload.id,
00130|            )
00131|            messages.success(
00132|                request,
00133|                f"Clientes nuevos procesados correctamente desde {upload.original_filename}.",
00134|            )
00135|            upload.status = FileUpload.STATUS_PARSED_OK
00136|            upload.save(update_fields=["status"])
00137|        except Exception as exc:
00138|            messages.error(request, f"Error al procesar clientes nuevos: {exc}")
00139|            upload.status = FileUpload.STATUS_PARSED_ERROR
00140|            upload.error_summary = str(exc)[:500]
00141|            upload.save(update_fields=["status", "error_summary"])
00142|
00143|    return _redirect_imports_to_admin(request, "new_clients")
00144|
00145|
00146|@login_required
00147|@user_passes_test(lambda u: u.is_superuser)
00148|def process_cross_sale(request, file_id):
00149|    upload = get_object_or_404(FileUpload, id=file_id)
00150|
00151|    if request.method == "POST":
00152|        if upload.file_type_detected != FileUpload.TYPE_CROSS_SALE:
00153|            messages.error(request, "Este archivo no es de tipo Venta cruzada.")
00154|            return _redirect_imports_to_admin(request, "cross_sale")
00155|
00156|        file_path = Path(upload.stored_file.path)
00157|        if not file_path.exists():
00158|            messages.error(request, f"El archivo físico no existe: {file_path}")
00159|            return _redirect_imports_to_admin(request, "cross_sale")
00160|
00161|        try:
00162|            call_command("import_venta_cruzada", path=str(file_path))
00163|            messages.success(
00164|                request,
00165|                f"Venta cruzada procesada correctamente desde {upload.original_filename}.",
00166|            )
00167|            upload.status = FileUpload.STATUS_PARSED_OK
00168|            upload.save(update_fields=["status"])
00169|        except Exception as exc:
00170|            messages.error(request, f"Error al procesar venta cruzada: {exc}")
00171|            upload.status = FileUpload.STATUS_PARSED_ERROR
00172|            upload.error_summary = str(exc)[:500]
00173|            upload.save(update_fields=["status", "error_summary"])
00174|
00175|    return _redirect_imports_to_admin(request, "cross_sale")
00176|
00177|
00178|@login_required
00179|@user_passes_test(lambda u: u.is_superuser)
00180|def process_station_times(request, file_id):
00181|    upload = get_object_or_404(FileUpload, id=file_id)
00182|    if request.method == "POST":
00183|        messages.warning(
00184|            request,
00185|            "El procesamiento de tiempos de estación aún no está implementado.",
00186|        )
00187|    return _redirect_imports_to_admin(request)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IyBpbXBvcnRzL3ZpZXdzLnB5Cgpmcm9tIHBhdGhsaWIgaW1wb3J0IFBhdGgKCmZyb20gZGphbmdvLmNvbnRyaWIgaW1wb3J0IG1lc3NhZ2VzCmZyb20gZGphbmdvLmNvbnRyaWIuYXV0aC5kZWNvcmF0b3JzIGltcG9ydCBsb2dpbl9yZXF1aXJlZCwgdXNlcl9wYXNzZXNfdGVzdApmcm9tIGRqYW5nby5jb3JlLm1hbmFnZW1lbnQgaW1wb3J0IGNhbGxfY29tbWFuZApmcm9tIGRqYW5nby5zaG9ydGN1dHMgaW1wb3J0IGdldF9vYmplY3Rfb3JfNDA0LCByZWRpcmVjdCwgcmVuZGVyCmZyb20gZGphbmdvLnVybHMgaW1wb3J0IHJldmVyc2UKCmZyb20gY29yZS53Y2dfbW9kZWxzIGltcG9ydCBEYXRhSW1wb3J0QmF0Y2gKZnJvbSBwZ2MuYWRtaW5fdXRpbHMgaW1wb3J0IHBhcnNlX3BlcmlvZAoKZnJvbSAuZGV0ZWN0aW9uIGltcG9ydCBBTExfSU1QT1JUQUJMRSwgVFlQRV9MQUJFTFMsIFRZUEVfVU5LTk9XTiwgZGV0ZWN0X2ZpbGUKZnJvbSAuZGlzcGF0Y2ggaW1wb3J0IHJ1bl9pbXBvcnQKZnJvbSAuZm9ybXMgaW1wb3J0IEdlbmVyYWxJbXBvcnRGb3JtCmZyb20gLm1vZGVscyBpbXBvcnQgRmlsZVVwbG9hZAoKCmRlZiBfcmVkaXJlY3RfaW1wb3J0c190b19hZG1pbihyZXF1ZXN0LCBibG9jazogc3RyIHwgTm9uZSA9IE5vbmUpOgogICAgeWVhciwgbW9udGggPSBwYXJzZV9wZXJpb2QocmVxdWVzdCkKICAgIHVybCA9IGYie3JldmVyc2UoJ3BnYzphZG1pbl9tb250aGx5Jyl9P3llYXI9e3llYXJ9Jm1vbnRoPXttb250aH0iCiAgICBpZiBibG9jazoKICAgICAgICB1cmwgKz0gZiImYmxvY2s9e2Jsb2NrfSIKICAgIHJldHVybiByZWRpcmVjdCh1cmwpCgoKQGxvZ2luX3JlcXVpcmVkCmRlZiBpbXBvcnRfaHViKHJlcXVlc3QpOgogICAgIiIiQWRtaW5pc3RyYWNpw7NuIOKGkiBJbXBvcnRhY2nDs24gR2VuZXJhbCAocHVudG8gw7puaWNvIENSTSAvIFBHTyAvIFJpc2sgLyBQR0MpLiIiIgogICAgcmVzdWx0ID0gTm9uZQogICAgZGV0ZWN0aW9uX3ByZXZpZXcgPSBOb25lCiAgICBmb3JtID0gR2VuZXJhbEltcG9ydEZvcm0oKQoKICAgIGlmIHJlcXVlc3QubWV0aG9kID09ICJQT1NUIjoKICAgICAgICBhY3Rpb24gPSByZXF1ZXN0LlBPU1QuZ2V0KCJhY3Rpb24iLCAiaW1wb3J0IikKICAgICAgICBmb3JtID0gR2VuZXJhbEltcG9ydEZvcm0ocmVxdWVzdC5QT1NULCByZXF1ZXN0LkZJTEVTKQogICAgICAgIGlmIGZvcm0uaXNfdmFsaWQoKToKICAgICAgICAgICAgdXBsb2FkZWQgPSBmb3JtLmNsZWFuZWRfZGF0YVsiYXJjaGl2byJdCiAgICAgICAgICAgIHRpcG9fZm9yemFkbyA9IGZvcm0uY2xlYW5lZF9kYXRhLmdldCgidGlwb19mb3J6YWRvIikgb3IgTm9uZQogICAgICAgICAgICBpZiBhY3Rpb24gPT0gImRldGVjdCI6CiAgICAgICAgICAgICAgICBkZXRlY3Rpb25fcHJldmlldyA9IGRldGVjdF9maWxlKHVwbG9hZGVkKQogICAgICAgICAgICAgICAgdXBsb2FkZWQuc2VlaygwKQogICAgICAgICAgICAgICAgZm9ybSA9IEdlbmVyYWxJbXBvcnRGb3JtKAogICAgICAgICAgICAgICAgICAgIGluaXRpYWw9ewogICAgICAgICAgICAgICAgICAgICAgICAidGlwb19mb3J6YWRvIjogKAogICAgICAgICAgICAgICAgICAgICAgICAgICAgZGV0ZWN0aW9uX3ByZXZpZXcudGlwbwogICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgZGV0ZWN0aW9uX3ByZXZpZXcudGlwbyAhPSBUWVBFX1VOS05PV04KICAgICAgICAgICAgICAgICAgICAgICAgICAgIGVsc2UgIiIKICAgICAgICAgICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIGxldmVsID0gbWVzc2FnZXMuV0FSTklORyBpZiBkZXRlY3Rpb25fcHJldmlldy5hbWJpZ3VvdXMgZWxzZSBtZXNzYWdlcy5JTkZPCiAgICAgICAgICAgICAgICBtZXNzYWdlcy5hZGRfbWVzc2FnZSgKICAgICAgICAgICAgICAgICAgICByZXF1ZXN0LAogICAgICAgICAgICAgICAgICAgIGxldmVsLAogICAgICAgICAgICAgICAgICAgIGYiRGV0ZWNjacOzbjoge2RldGVjdGlvbl9wcmV2aWV3LmxhYmVsfSAiCiAgICAgICAgICAgICAgICAgICAgZiIoe2ludChkZXRlY3Rpb25fcHJldmlldy5jb25maWRlbmNlICogMTAwKX0lIMK3IGNhcGEge2RldGVjdGlvbl9wcmV2aWV3LmxheWVyfSkuICIKICAgICAgICAgICAgICAgICAgICBmInsnU2VsZWNjaW9uZSBlbCB0aXBvIG1hbnVhbG1lbnRlIOKAlCBoYXkgYW1iaWfDvGVkYWQuICcgaWYgZGV0ZWN0aW9uX3ByZXZpZXcuYW1iaWd1b3VzIGVsc2UgJyd9IgogICAgICAgICAgICAgICAgICAgIGYiVnVlbHZhIGEgc2VsZWNjaW9uYXIgZWwgYXJjaGl2byB5IGNvbmZpcm1lIGxhIGltcG9ydGFjacOzbi4iLAogICAgICAgICAgICAgICAgKQogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgcmVzdWx0ID0gcnVuX2ltcG9ydChyZXF1ZXN0LnVzZXIsIHVwbG9hZGVkLCB0aXBvX2ZvcnphZG89dGlwb19mb3J6YWRvIG9yIE5vbmUpCiAgICAgICAgICAgICAgICBpZiByZXN1bHQub2s6CiAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMuc3VjY2VzcyhyZXF1ZXN0LCByZXN1bHQubWVzc2FnZSkKICAgICAgICAgICAgICAgICAgICBmb3JtID0gR2VuZXJhbEltcG9ydEZvcm0oKQogICAgICAgICAgICAgICAgZWxpZiByZXN1bHQubmVlZHNfbWFudWFsOgogICAgICAgICAgICAgICAgICAgIG1lc3NhZ2VzLndhcm5pbmcocmVxdWVzdCwgcmVzdWx0Lm1lc3NhZ2UpCiAgICAgICAgICAgICAgICAgICAgZGV0ZWN0aW9uX3ByZXZpZXcgPSByZXN1bHQuZGV0ZWN0aW9uCiAgICAgICAgICAgICAgICAgICAgZm9ybSA9IEdlbmVyYWxJbXBvcnRGb3JtKAogICAgICAgICAgICAgICAgICAgICAgICBpbml0aWFsPXsKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJ0aXBvX2ZvcnphZG8iOiAoCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcmVzdWx0LmRldGVjdGlvbi50aXBvCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgcmVzdWx0LmRldGVjdGlvbi50aXBvICE9IFRZUEVfVU5LTk9XTgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGVsc2UgIiIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMud2FybmluZyhyZXF1ZXN0LCByZXN1bHQubWVzc2FnZSBvciAiSW1wb3J0YWNpw7NuIGluY29tcGxldGEuIikKICAgICAgICAgICAgICAgICAgICBmb3JtID0gR2VuZXJhbEltcG9ydEZvcm0oKQoKICAgIGJhdGNoZXMgPSBEYXRhSW1wb3J0QmF0Y2gub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgidXBsb2FkZWRfYnkiKS5vcmRlcl9ieSgiLWNyZWF0ZWRfYXQiKVs6MjVdCiAgICB1cGxvYWRzID0gRmlsZVVwbG9hZC5vYmplY3RzLm9yZGVyX2J5KCItY3JlYXRlZF9hdCIpWzoxNV0KCiAgICByZXR1cm4gcmVuZGVyKAogICAgICAgIHJlcXVlc3QsCiAgICAgICAgImltcG9ydHMvZ2VuZXJhbF9odWIuaHRtbCIsCiAgICAgICAgewogICAgICAgICAgICAiZm9ybSI6IGZvcm0sCiAgICAgICAgICAgICJyZXN1bHQiOiByZXN1bHQsCiAgICAgICAgICAgICJkZXRlY3Rpb25fcHJldmlldyI6IGRldGVjdGlvbl9wcmV2aWV3LAogICAgICAgICAgICAiYmF0Y2hlcyI6IGJhdGNoZXMsCiAgICAgICAgICAgICJ1cGxvYWRzIjogdXBsb2FkcywKICAgICAgICAgICAgInR5cGVfbGFiZWxzIjogVFlQRV9MQUJFTFMsCiAgICAgICAgICAgICJpbXBvcnRhYmxlX3R5cGVzIjogWyh0LCBUWVBFX0xBQkVMU1t0XSkgZm9yIHQgaW4gQUxMX0lNUE9SVEFCTEVdLAogICAgICAgICAgICAiYnJlYWRjcnVtYnMiOiBbCiAgICAgICAgICAgICAgICB7ImxhYmVsIjogIkluaWNpbyIsICJ1cmwiOiByZXZlcnNlKCJwb3J0YWw6aG9tZSIpfSwKICAgICAgICAgICAgICAgIHsibGFiZWwiOiAiQWRtaW5pc3RyYWNpw7NuIn0sCiAgICAgICAgICAgICAgICB7ImxhYmVsIjogIkltcG9ydGFjacOzbiBHZW5lcmFsIn0sCiAgICAgICAgICAgIF0sCiAgICAgICAgfSwKICAgICkKCgpAbG9naW5fcmVxdWlyZWQKQHVzZXJfcGFzc2VzX3Rlc3QobGFtYmRhIHU6IHUuaXNfc3VwZXJ1c2VyKQpkZWYgcHJvY2Vzc19uZXdfY2xpZW50cyhyZXF1ZXN0LCBmaWxlX2lkKToKICAgIHVwbG9hZCA9IGdldF9vYmplY3Rfb3JfNDA0KEZpbGVVcGxvYWQsIGlkPWZpbGVfaWQpCgogICAgaWYgcmVxdWVzdC5tZXRob2QgPT0gIlBPU1QiOgogICAgICAgIGlmIHVwbG9hZC5maWxlX3R5cGVfZGV0ZWN0ZWQgIT0gRmlsZVVwbG9hZC5UWVBFX05FV19DTElFTlRTOgogICAgICAgICAgICBtZXNzYWdlcy5lcnJvcihyZXF1ZXN0LCAiRXN0ZSBhcmNoaXZvIG5vIGVzIGRlIHRpcG8gQ2xpZW50ZXMgbnVldm9zLiIpCiAgICAgICAgICAgIHJldHVybiBfcmVkaXJlY3RfaW1wb3J0c190b19hZG1pbihyZXF1ZXN0LCAibmV3X2NsaWVudHMiKQoKICAgICAgICBpZiBub3QgdXBsb2FkLnN0b3JlZF9maWxlOgogICAgICAgICAgICBtZXNzYWdlcy5lcnJvcihyZXF1ZXN0LCAiRWwgYXJjaGl2byBubyB0aWVuZSBmaWNoZXJvIGFsbWFjZW5hZG8uIikKICAgICAgICAgICAgcmV0dXJuIF9yZWRpcmVjdF9pbXBvcnRzX3RvX2FkbWluKHJlcXVlc3QsICJuZXdfY2xpZW50cyIpCgogICAgICAgIGZpbGVfcGF0aCA9IFBhdGgodXBsb2FkLnN0b3JlZF9maWxlLnBhdGgpCiAgICAgICAgaWYgbm90IGZpbGVfcGF0aC5leGlzdHMoKToKICAgICAgICAgICAgbWVzc2FnZXMuZXJyb3IocmVxdWVzdCwgZiJFbCBhcmNoaXZvIGbDrXNpY28gbm8gZXhpc3RlOiB7ZmlsZV9wYXRofSIpCiAgICAgICAgICAgIHJldHVybiBfcmVkaXJlY3RfaW1wb3J0c190b19hZG1pbihyZXF1ZXN0LCAibmV3X2NsaWVudHMiKQoKICAgICAgICB0cnk6CiAgICAgICAgICAgIGNhbGxfY29tbWFuZCgKICAgICAgICAgICAgICAgICJpbXBvcnRfY2xpZW50ZXNfbnVldm9zIiwKICAgICAgICAgICAgICAgIHBhdGg9c3RyKGZpbGVfcGF0aCksCiAgICAgICAgICAgICAgICBmaWxlX3VwbG9hZF9pZD11cGxvYWQuaWQsCiAgICAgICAgICAgICkKICAgICAgICAgICAgbWVzc2FnZXMuc3VjY2VzcygKICAgICAgICAgICAgICAgIHJlcXVlc3QsCiAgICAgICAgICAgICAgICBmIkNsaWVudGVzIG51ZXZvcyBwcm9jZXNhZG9zIGNvcnJlY3RhbWVudGUgZGVzZGUge3VwbG9hZC5vcmlnaW5hbF9maWxlbmFtZX0uIiwKICAgICAgICAgICAgKQogICAgICAgICAgICB1cGxvYWQuc3RhdHVzID0gRmlsZVVwbG9hZC5TVEFUVVNfUEFSU0VEX09LCiAgICAgICAgICAgIHVwbG9hZC5zYXZlKHVwZGF0ZV9maWVsZHM9WyJzdGF0dXMiXSkKICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGV4YzoKICAgICAgICAgICAgbWVzc2FnZXMuZXJyb3IocmVxdWVzdCwgZiJFcnJvciBhbCBwcm9jZXNhciBjbGllbnRlcyBudWV2b3M6IHtleGN9IikKICAgICAgICAgICAgdXBsb2FkLnN0YXR1cyA9IEZpbGVVcGxvYWQuU1RBVFVTX1BBUlNFRF9FUlJPUgogICAgICAgICAgICB1cGxvYWQuZXJyb3Jfc3VtbWFyeSA9IHN0cihleGMpWzo1MDBdCiAgICAgICAgICAgIHVwbG9hZC5zYXZlKHVwZGF0ZV9maWVsZHM9WyJzdGF0dXMiLCAiZXJyb3Jfc3VtbWFyeSJdKQoKICAgIHJldHVybiBfcmVkaXJlY3RfaW1wb3J0c190b19hZG1pbihyZXF1ZXN0LCAibmV3X2NsaWVudHMiKQoKCkBsb2dpbl9yZXF1aXJlZApAdXNlcl9wYXNzZXNfdGVzdChsYW1iZGEgdTogdS5pc19zdXBlcnVzZXIpCmRlZiBwcm9jZXNzX2Nyb3NzX3NhbGUocmVxdWVzdCwgZmlsZV9pZCk6CiAgICB1cGxvYWQgPSBnZXRfb2JqZWN0X29yXzQwNChGaWxlVXBsb2FkLCBpZD1maWxlX2lkKQoKICAgIGlmIHJlcXVlc3QubWV0aG9kID09ICJQT1NUIjoKICAgICAgICBpZiB1cGxvYWQuZmlsZV90eXBlX2RldGVjdGVkICE9IEZpbGVVcGxvYWQuVFlQRV9DUk9TU19TQUxFOgogICAgICAgICAgICBtZXNzYWdlcy5lcnJvcihyZXF1ZXN0LCAiRXN0ZSBhcmNoaXZvIG5vIGVzIGRlIHRpcG8gVmVudGEgY3J1emFkYS4iKQogICAgICAgICAgICByZXR1cm4gX3JlZGlyZWN0X2ltcG9ydHNfdG9fYWRtaW4ocmVxdWVzdCwgImNyb3NzX3NhbGUiKQoKICAgICAgICBmaWxlX3BhdGggPSBQYXRoKHVwbG9hZC5zdG9yZWRfZmlsZS5wYXRoKQogICAgICAgIGlmIG5vdCBmaWxlX3BhdGguZXhpc3RzKCk6CiAgICAgICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsIGYiRWwgYXJjaGl2byBmw61zaWNvIG5vIGV4aXN0ZToge2ZpbGVfcGF0aH0iKQogICAgICAgICAgICByZXR1cm4gX3JlZGlyZWN0X2ltcG9ydHNfdG9fYWRtaW4ocmVxdWVzdCwgImNyb3NzX3NhbGUiKQoKICAgICAgICB0cnk6CiAgICAgICAgICAgIGNhbGxfY29tbWFuZCgiaW1wb3J0X3ZlbnRhX2NydXphZGEiLCBwYXRoPXN0cihmaWxlX3BhdGgpKQogICAgICAgICAgICBtZXNzYWdlcy5zdWNjZXNzKAogICAgICAgICAgICAgICAgcmVxdWVzdCwKICAgICAgICAgICAgICAgIGYiVmVudGEgY3J1emFkYSBwcm9jZXNhZGEgY29ycmVjdGFtZW50ZSBkZXNkZSB7dXBsb2FkLm9yaWdpbmFsX2ZpbGVuYW1lfS4iLAogICAgICAgICAgICApCiAgICAgICAgICAgIHVwbG9hZC5zdGF0dXMgPSBGaWxlVXBsb2FkLlNUQVRVU19QQVJTRURfT0sKICAgICAgICAgICAgdXBsb2FkLnNhdmUodXBkYXRlX2ZpZWxkcz1bInN0YXR1cyJdKQogICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZXhjOgogICAgICAgICAgICBtZXNzYWdlcy5lcnJvcihyZXF1ZXN0LCBmIkVycm9yIGFsIHByb2Nlc2FyIHZlbnRhIGNydXphZGE6IHtleGN9IikKICAgICAgICAgICAgdXBsb2FkLnN0YXR1cyA9IEZpbGVVcGxvYWQuU1RBVFVTX1BBUlNFRF9FUlJPUgogICAgICAgICAgICB1cGxvYWQuZXJyb3Jfc3VtbWFyeSA9IHN0cihleGMpWzo1MDBdCiAgICAgICAgICAgIHVwbG9hZC5zYXZlKHVwZGF0ZV9maWVsZHM9WyJzdGF0dXMiLCAiZXJyb3Jfc3VtbWFyeSJdKQoKICAgIHJldHVybiBfcmVkaXJlY3RfaW1wb3J0c190b19hZG1pbihyZXF1ZXN0LCAiY3Jvc3Nfc2FsZSIpCgoKQGxvZ2luX3JlcXVpcmVkCkB1c2VyX3Bhc3Nlc190ZXN0KGxhbWJkYSB1OiB1LmlzX3N1cGVydXNlcikKZGVmIHByb2Nlc3Nfc3RhdGlvbl90aW1lcyhyZXF1ZXN0LCBmaWxlX2lkKToKICAgIHVwbG9hZCA9IGdldF9vYmplY3Rfb3JfNDA0KEZpbGVVcGxvYWQsIGlkPWZpbGVfaWQpCiAgICBpZiByZXF1ZXN0Lm1ldGhvZCA9PSAiUE9TVCI6CiAgICAgICAgbWVzc2FnZXMud2FybmluZygKICAgICAgICAgICAgcmVxdWVzdCwKICAgICAgICAgICAgIkVsIHByb2Nlc2FtaWVudG8gZGUgdGllbXBvcyBkZSBlc3RhY2nDs24gYcO6biBubyBlc3TDoSBpbXBsZW1lbnRhZG8uIiwKICAgICAgICApCiAgICByZXR1cm4gX3JlZGlyZWN0X2ltcG9ydHNfdG9fYWRtaW4ocmVxdWVzdCkK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/__init__.py
PATH_JSON="pgc/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/admin.py
PATH_JSON="pgc/admin.py"
FILENAME=admin.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=247
SIZE_BYTES_UTF8=4723
CONTENT_SHA256=eac6b01dfc10abb78dcace233886ec186ac434501ee8ffae6ad51598c4fab851
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
# pgc/admin.py

from django.contrib import admin

from .models import (
    AdminManualEditLog,
    ManualRequirementsCompliance,
    MetricReserve,
    MonthlyExchangeRate,
    MonthlyMetricResult,
    MonthlyMetricScore,
    MonthlyModeScorecard,
    MonthlyScorecard,
    MonthlyTarget,
    PGCPlan,
)


@admin.register(MonthlyMetricScore)
class MonthlyMetricScoreAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "year",
        "month",
        "mode",
        "une",
        "metric",
        "measured_value",
        "target_value",
        "points_awarded",
        "carry_in",
        "carry_used",
        "carry_generated",
        "is_achieved",
    )
    list_filter = (
        "plan",
        "year",
        "month",
        "mode",
        "une",
        "metric",
        "is_achieved",
    )
    search_fields = (
        "une__name_es",
        "metric__name",
        "calculation_note",
    )


@admin.register(MonthlyModeScorecard)
class MonthlyModeScorecardAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "year",
        "month",
        "mode",
        "une",
        "total_points",
        "qualified_threshold",
        "is_month_qualified",
    )
    list_filter = (
        "plan",
        "year",
        "month",
        "mode",
        "une",
        "is_month_qualified",
    )
    search_fields = (
        "une__name_es",
        "summary_note",
    )


@admin.register(MetricReserve)
class MetricReserveAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "mode",
        "une",
        "metric",
        "source_year",
        "source_month",
        "amount",
        "remaining",
    )
    list_filter = (
        "plan",
        "mode",
        "une",
        "metric",
        "source_year",
        "source_month",
    )
    search_fields = (
        "une__name_es",
        "metric__name",
        "notes",
    )


@admin.register(MonthlyExchangeRate)
class MonthlyExchangeRateAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "month",
        "usd_to_gtq",
    )
    list_filter = ("year",)
    ordering = ("-year", "month")


@admin.register(PGCPlan)
class PGCPlanAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "name",
        "is_active",
        "created_at",
    )
    list_filter = (
        "is_active",
        "year",
    )
    search_fields = (
        "name",
        "notes",
    )


@admin.register(MonthlyTarget)
class MonthlyTargetAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "year",
        "month",
        "une",
        "metric",
        "target_value",
        "points_if_achieved",
        "reference_annual_value",
    )
    list_filter = (
        "plan",
        "year",
        "month",
        "une",
        "metric",
    )
    search_fields = (
        "une__name_es",
        "metric__name",
        "notes",
    )


@admin.register(MonthlyMetricResult)
class MonthlyMetricResultAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "year",
        "month",
        "une",
        "metric",
        "measured_value",
        "target_value",
        "is_achieved",
        "points_awarded",
    )
    list_filter = (
        "plan",
        "year",
        "month",
        "une",
        "metric",
        "is_achieved",
    )
    search_fields = (
        "une__name_es",
        "metric__name",
        "calculation_note",
    )


@admin.register(MonthlyScorecard)
class MonthlyScorecardAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "year",
        "month",
        "une",
        "total_points",
        "qualified_threshold",
        "is_month_qualified",
    )
    list_filter = (
        "plan",
        "year",
        "month",
        "une",
        "is_month_qualified",
    )
    search_fields = (
        "une__name_es",
        "summary_note",
    )


@admin.register(AdminManualEditLog)
class AdminManualEditLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "year",
        "month",
        "entity_type",
        "field_name",
        "edited_by",
    )
    list_filter = ("entity_type", "year", "month")
    search_fields = ("field_name", "old_value", "new_value", "reason")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ManualRequirementsCompliance)
class ManualRequirementsComplianceAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "year",
        "month",
        "une",
        "is_compliant",
    )
    list_filter = (
        "plan",
        "year",
        "month",
        "une",
        "is_compliant",
    )
    search_fields = (
        "une__name_es",
        "incident_note",
    )
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|# pgc/admin.py
00002|
00003|from django.contrib import admin
00004|
00005|from .models import (
00006|    AdminManualEditLog,
00007|    ManualRequirementsCompliance,
00008|    MetricReserve,
00009|    MonthlyExchangeRate,
00010|    MonthlyMetricResult,
00011|    MonthlyMetricScore,
00012|    MonthlyModeScorecard,
00013|    MonthlyScorecard,
00014|    MonthlyTarget,
00015|    PGCPlan,
00016|)
00017|
00018|
00019|@admin.register(MonthlyMetricScore)
00020|class MonthlyMetricScoreAdmin(admin.ModelAdmin):
00021|    list_display = (
00022|        "plan",
00023|        "year",
00024|        "month",
00025|        "mode",
00026|        "une",
00027|        "metric",
00028|        "measured_value",
00029|        "target_value",
00030|        "points_awarded",
00031|        "carry_in",
00032|        "carry_used",
00033|        "carry_generated",
00034|        "is_achieved",
00035|    )
00036|    list_filter = (
00037|        "plan",
00038|        "year",
00039|        "month",
00040|        "mode",
00041|        "une",
00042|        "metric",
00043|        "is_achieved",
00044|    )
00045|    search_fields = (
00046|        "une__name_es",
00047|        "metric__name",
00048|        "calculation_note",
00049|    )
00050|
00051|
00052|@admin.register(MonthlyModeScorecard)
00053|class MonthlyModeScorecardAdmin(admin.ModelAdmin):
00054|    list_display = (
00055|        "plan",
00056|        "year",
00057|        "month",
00058|        "mode",
00059|        "une",
00060|        "total_points",
00061|        "qualified_threshold",
00062|        "is_month_qualified",
00063|    )
00064|    list_filter = (
00065|        "plan",
00066|        "year",
00067|        "month",
00068|        "mode",
00069|        "une",
00070|        "is_month_qualified",
00071|    )
00072|    search_fields = (
00073|        "une__name_es",
00074|        "summary_note",
00075|    )
00076|
00077|
00078|@admin.register(MetricReserve)
00079|class MetricReserveAdmin(admin.ModelAdmin):
00080|    list_display = (
00081|        "plan",
00082|        "mode",
00083|        "une",
00084|        "metric",
00085|        "source_year",
00086|        "source_month",
00087|        "amount",
00088|        "remaining",
00089|    )
00090|    list_filter = (
00091|        "plan",
00092|        "mode",
00093|        "une",
00094|        "metric",
00095|        "source_year",
00096|        "source_month",
00097|    )
00098|    search_fields = (
00099|        "une__name_es",
00100|        "metric__name",
00101|        "notes",
00102|    )
00103|
00104|
00105|@admin.register(MonthlyExchangeRate)
00106|class MonthlyExchangeRateAdmin(admin.ModelAdmin):
00107|    list_display = (
00108|        "year",
00109|        "month",
00110|        "usd_to_gtq",
00111|    )
00112|    list_filter = ("year",)
00113|    ordering = ("-year", "month")
00114|
00115|
00116|@admin.register(PGCPlan)
00117|class PGCPlanAdmin(admin.ModelAdmin):
00118|    list_display = (
00119|        "year",
00120|        "name",
00121|        "is_active",
00122|        "created_at",
00123|    )
00124|    list_filter = (
00125|        "is_active",
00126|        "year",
00127|    )
00128|    search_fields = (
00129|        "name",
00130|        "notes",
00131|    )
00132|
00133|
00134|@admin.register(MonthlyTarget)
00135|class MonthlyTargetAdmin(admin.ModelAdmin):
00136|    list_display = (
00137|        "plan",
00138|        "year",
00139|        "month",
00140|        "une",
00141|        "metric",
00142|        "target_value",
00143|        "points_if_achieved",
00144|        "reference_annual_value",
00145|    )
00146|    list_filter = (
00147|        "plan",
00148|        "year",
00149|        "month",
00150|        "une",
00151|        "metric",
00152|    )
00153|    search_fields = (
00154|        "une__name_es",
00155|        "metric__name",
00156|        "notes",
00157|    )
00158|
00159|
00160|@admin.register(MonthlyMetricResult)
00161|class MonthlyMetricResultAdmin(admin.ModelAdmin):
00162|    list_display = (
00163|        "plan",
00164|        "year",
00165|        "month",
00166|        "une",
00167|        "metric",
00168|        "measured_value",
00169|        "target_value",
00170|        "is_achieved",
00171|        "points_awarded",
00172|    )
00173|    list_filter = (
00174|        "plan",
00175|        "year",
00176|        "month",
00177|        "une",
00178|        "metric",
00179|        "is_achieved",
00180|    )
00181|    search_fields = (
00182|        "une__name_es",
00183|        "metric__name",
00184|        "calculation_note",
00185|    )
00186|
00187|
00188|@admin.register(MonthlyScorecard)
00189|class MonthlyScorecardAdmin(admin.ModelAdmin):
00190|    list_display = (
00191|        "plan",
00192|        "year",
00193|        "month",
00194|        "une",
00195|        "total_points",
00196|        "qualified_threshold",
00197|        "is_month_qualified",
00198|    )
00199|    list_filter = (
00200|        "plan",
00201|        "year",
00202|        "month",
00203|        "une",
00204|        "is_month_qualified",
00205|    )
00206|    search_fields = (
00207|        "une__name_es",
00208|        "summary_note",
00209|    )
00210|
00211|
00212|@admin.register(AdminManualEditLog)
00213|class AdminManualEditLogAdmin(admin.ModelAdmin):
00214|    list_display = (
00215|        "created_at",
00216|        "year",
00217|        "month",
00218|        "entity_type",
00219|        "field_name",
00220|        "edited_by",
00221|    )
00222|    list_filter = ("entity_type", "year", "month")
00223|    search_fields = ("field_name", "old_value", "new_value", "reason")
00224|    readonly_fields = ("created_at", "updated_at")
00225|
00226|
00227|@admin.register(ManualRequirementsCompliance)
00228|class ManualRequirementsComplianceAdmin(admin.ModelAdmin):
00229|    list_display = (
00230|        "plan",
00231|        "year",
00232|        "month",
00233|        "une",
00234|        "is_compliant",
00235|    )
00236|    list_filter = (
00237|        "plan",
00238|        "year",
00239|        "month",
00240|        "une",
00241|        "is_compliant",
00242|    )
00243|    search_fields = (
00244|        "une__name_es",
00245|        "incident_note",
00246|    )
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IyBwZ2MvYWRtaW4ucHkKCmZyb20gZGphbmdvLmNvbnRyaWIgaW1wb3J0IGFkbWluCgpmcm9tIC5tb2RlbHMgaW1wb3J0ICgKICAgIEFkbWluTWFudWFsRWRpdExvZywKICAgIE1hbnVhbFJlcXVpcmVtZW50c0NvbXBsaWFuY2UsCiAgICBNZXRyaWNSZXNlcnZlLAogICAgTW9udGhseUV4Y2hhbmdlUmF0ZSwKICAgIE1vbnRobHlNZXRyaWNSZXN1bHQsCiAgICBNb250aGx5TWV0cmljU2NvcmUsCiAgICBNb250aGx5TW9kZVNjb3JlY2FyZCwKICAgIE1vbnRobHlTY29yZWNhcmQsCiAgICBNb250aGx5VGFyZ2V0LAogICAgUEdDUGxhbiwKKQoKCkBhZG1pbi5yZWdpc3RlcihNb250aGx5TWV0cmljU2NvcmUpCmNsYXNzIE1vbnRobHlNZXRyaWNTY29yZUFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKAogICAgICAgICJwbGFuIiwKICAgICAgICAieWVhciIsCiAgICAgICAgIm1vbnRoIiwKICAgICAgICAibW9kZSIsCiAgICAgICAgInVuZSIsCiAgICAgICAgIm1ldHJpYyIsCiAgICAgICAgIm1lYXN1cmVkX3ZhbHVlIiwKICAgICAgICAidGFyZ2V0X3ZhbHVlIiwKICAgICAgICAicG9pbnRzX2F3YXJkZWQiLAogICAgICAgICJjYXJyeV9pbiIsCiAgICAgICAgImNhcnJ5X3VzZWQiLAogICAgICAgICJjYXJyeV9nZW5lcmF0ZWQiLAogICAgICAgICJpc19hY2hpZXZlZCIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgKICAgICAgICAicGxhbiIsCiAgICAgICAgInllYXIiLAogICAgICAgICJtb250aCIsCiAgICAgICAgIm1vZGUiLAogICAgICAgICJ1bmUiLAogICAgICAgICJtZXRyaWMiLAogICAgICAgICJpc19hY2hpZXZlZCIsCiAgICApCiAgICBzZWFyY2hfZmllbGRzID0gKAogICAgICAgICJ1bmVfX25hbWVfZXMiLAogICAgICAgICJtZXRyaWNfX25hbWUiLAogICAgICAgICJjYWxjdWxhdGlvbl9ub3RlIiwKICAgICkKCgpAYWRtaW4ucmVnaXN0ZXIoTW9udGhseU1vZGVTY29yZWNhcmQpCmNsYXNzIE1vbnRobHlNb2RlU2NvcmVjYXJkQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoCiAgICAgICAgInBsYW4iLAogICAgICAgICJ5ZWFyIiwKICAgICAgICAibW9udGgiLAogICAgICAgICJtb2RlIiwKICAgICAgICAidW5lIiwKICAgICAgICAidG90YWxfcG9pbnRzIiwKICAgICAgICAicXVhbGlmaWVkX3RocmVzaG9sZCIsCiAgICAgICAgImlzX21vbnRoX3F1YWxpZmllZCIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgKICAgICAgICAicGxhbiIsCiAgICAgICAgInllYXIiLAogICAgICAgICJtb250aCIsCiAgICAgICAgIm1vZGUiLAogICAgICAgICJ1bmUiLAogICAgICAgICJpc19tb250aF9xdWFsaWZpZWQiLAogICAgKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgKICAgICAgICAidW5lX19uYW1lX2VzIiwKICAgICAgICAic3VtbWFyeV9ub3RlIiwKICAgICkKCgpAYWRtaW4ucmVnaXN0ZXIoTWV0cmljUmVzZXJ2ZSkKY2xhc3MgTWV0cmljUmVzZXJ2ZUFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKAogICAgICAgICJwbGFuIiwKICAgICAgICAibW9kZSIsCiAgICAgICAgInVuZSIsCiAgICAgICAgIm1ldHJpYyIsCiAgICAgICAgInNvdXJjZV95ZWFyIiwKICAgICAgICAic291cmNlX21vbnRoIiwKICAgICAgICAiYW1vdW50IiwKICAgICAgICAicmVtYWluaW5nIiwKICAgICkKICAgIGxpc3RfZmlsdGVyID0gKAogICAgICAgICJwbGFuIiwKICAgICAgICAibW9kZSIsCiAgICAgICAgInVuZSIsCiAgICAgICAgIm1ldHJpYyIsCiAgICAgICAgInNvdXJjZV95ZWFyIiwKICAgICAgICAic291cmNlX21vbnRoIiwKICAgICkKICAgIHNlYXJjaF9maWVsZHMgPSAoCiAgICAgICAgInVuZV9fbmFtZV9lcyIsCiAgICAgICAgIm1ldHJpY19fbmFtZSIsCiAgICAgICAgIm5vdGVzIiwKICAgICkKCgpAYWRtaW4ucmVnaXN0ZXIoTW9udGhseUV4Y2hhbmdlUmF0ZSkKY2xhc3MgTW9udGhseUV4Y2hhbmdlUmF0ZUFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKAogICAgICAgICJ5ZWFyIiwKICAgICAgICAibW9udGgiLAogICAgICAgICJ1c2RfdG9fZ3RxIiwKICAgICkKICAgIGxpc3RfZmlsdGVyID0gKCJ5ZWFyIiwpCiAgICBvcmRlcmluZyA9ICgiLXllYXIiLCAibW9udGgiKQoKCkBhZG1pbi5yZWdpc3RlcihQR0NQbGFuKQpjbGFzcyBQR0NQbGFuQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoCiAgICAgICAgInllYXIiLAogICAgICAgICJuYW1lIiwKICAgICAgICAiaXNfYWN0aXZlIiwKICAgICAgICAiY3JlYXRlZF9hdCIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgKICAgICAgICAiaXNfYWN0aXZlIiwKICAgICAgICAieWVhciIsCiAgICApCiAgICBzZWFyY2hfZmllbGRzID0gKAogICAgICAgICJuYW1lIiwKICAgICAgICAibm90ZXMiLAogICAgKQoKCkBhZG1pbi5yZWdpc3RlcihNb250aGx5VGFyZ2V0KQpjbGFzcyBNb250aGx5VGFyZ2V0QWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoCiAgICAgICAgInBsYW4iLAogICAgICAgICJ5ZWFyIiwKICAgICAgICAibW9udGgiLAogICAgICAgICJ1bmUiLAogICAgICAgICJtZXRyaWMiLAogICAgICAgICJ0YXJnZXRfdmFsdWUiLAogICAgICAgICJwb2ludHNfaWZfYWNoaWV2ZWQiLAogICAgICAgICJyZWZlcmVuY2VfYW5udWFsX3ZhbHVlIiwKICAgICkKICAgIGxpc3RfZmlsdGVyID0gKAogICAgICAgICJwbGFuIiwKICAgICAgICAieWVhciIsCiAgICAgICAgIm1vbnRoIiwKICAgICAgICAidW5lIiwKICAgICAgICAibWV0cmljIiwKICAgICkKICAgIHNlYXJjaF9maWVsZHMgPSAoCiAgICAgICAgInVuZV9fbmFtZV9lcyIsCiAgICAgICAgIm1ldHJpY19fbmFtZSIsCiAgICAgICAgIm5vdGVzIiwKICAgICkKCgpAYWRtaW4ucmVnaXN0ZXIoTW9udGhseU1ldHJpY1Jlc3VsdCkKY2xhc3MgTW9udGhseU1ldHJpY1Jlc3VsdEFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKAogICAgICAgICJwbGFuIiwKICAgICAgICAieWVhciIsCiAgICAgICAgIm1vbnRoIiwKICAgICAgICAidW5lIiwKICAgICAgICAibWV0cmljIiwKICAgICAgICAibWVhc3VyZWRfdmFsdWUiLAogICAgICAgICJ0YXJnZXRfdmFsdWUiLAogICAgICAgICJpc19hY2hpZXZlZCIsCiAgICAgICAgInBvaW50c19hd2FyZGVkIiwKICAgICkKICAgIGxpc3RfZmlsdGVyID0gKAogICAgICAgICJwbGFuIiwKICAgICAgICAieWVhciIsCiAgICAgICAgIm1vbnRoIiwKICAgICAgICAidW5lIiwKICAgICAgICAibWV0cmljIiwKICAgICAgICAiaXNfYWNoaWV2ZWQiLAogICAgKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgKICAgICAgICAidW5lX19uYW1lX2VzIiwKICAgICAgICAibWV0cmljX19uYW1lIiwKICAgICAgICAiY2FsY3VsYXRpb25fbm90ZSIsCiAgICApCgoKQGFkbWluLnJlZ2lzdGVyKE1vbnRobHlTY29yZWNhcmQpCmNsYXNzIE1vbnRobHlTY29yZWNhcmRBZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgKICAgICAgICAicGxhbiIsCiAgICAgICAgInllYXIiLAogICAgICAgICJtb250aCIsCiAgICAgICAgInVuZSIsCiAgICAgICAgInRvdGFsX3BvaW50cyIsCiAgICAgICAgInF1YWxpZmllZF90aHJlc2hvbGQiLAogICAgICAgICJpc19tb250aF9xdWFsaWZpZWQiLAogICAgKQogICAgbGlzdF9maWx0ZXIgPSAoCiAgICAgICAgInBsYW4iLAogICAgICAgICJ5ZWFyIiwKICAgICAgICAibW9udGgiLAogICAgICAgICJ1bmUiLAogICAgICAgICJpc19tb250aF9xdWFsaWZpZWQiLAogICAgKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgKICAgICAgICAidW5lX19uYW1lX2VzIiwKICAgICAgICAic3VtbWFyeV9ub3RlIiwKICAgICkKCgpAYWRtaW4ucmVnaXN0ZXIoQWRtaW5NYW51YWxFZGl0TG9nKQpjbGFzcyBBZG1pbk1hbnVhbEVkaXRMb2dBZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgKICAgICAgICAiY3JlYXRlZF9hdCIsCiAgICAgICAgInllYXIiLAogICAgICAgICJtb250aCIsCiAgICAgICAgImVudGl0eV90eXBlIiwKICAgICAgICAiZmllbGRfbmFtZSIsCiAgICAgICAgImVkaXRlZF9ieSIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgiZW50aXR5X3R5cGUiLCAieWVhciIsICJtb250aCIpCiAgICBzZWFyY2hfZmllbGRzID0gKCJmaWVsZF9uYW1lIiwgIm9sZF92YWx1ZSIsICJuZXdfdmFsdWUiLCAicmVhc29uIikKICAgIHJlYWRvbmx5X2ZpZWxkcyA9ICgiY3JlYXRlZF9hdCIsICJ1cGRhdGVkX2F0IikKCgpAYWRtaW4ucmVnaXN0ZXIoTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZSkKY2xhc3MgTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZUFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKAogICAgICAgICJwbGFuIiwKICAgICAgICAieWVhciIsCiAgICAgICAgIm1vbnRoIiwKICAgICAgICAidW5lIiwKICAgICAgICAiaXNfY29tcGxpYW50IiwKICAgICkKICAgIGxpc3RfZmlsdGVyID0gKAogICAgICAgICJwbGFuIiwKICAgICAgICAieWVhciIsCiAgICAgICAgIm1vbnRoIiwKICAgICAgICAidW5lIiwKICAgICAgICAiaXNfY29tcGxpYW50IiwKICAgICkKICAgIHNlYXJjaF9maWVsZHMgPSAoCiAgICAgICAgInVuZV9fbmFtZV9lcyIsCiAgICAgICAgImluY2lkZW50X25vdGUiLAogICAgKQ==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/admin_ingresos_year.py
PATH_JSON="pgc/admin_ingresos_year.py"
FILENAME=admin_ingresos_year.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=298
SIZE_BYTES_UTF8=10586
CONTENT_SHA256=0ac37e96cdb5c1b1dd31b9ff18fc2e6443f4e23a94f928356969fe4a16da3e81
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""
Matriz anual de ingresos reales: 12 meses × 4 UNEs + TC editable.
"""

from __future__ import annotations

from decimal import Decimal

from django.db import transaction

from core.models import MetricDefinition, UNE
from pgc.admin_manual import log_manual_edit, save_fx
from pgc.admin_utils import parse_decimal_or_none
from pgc.income_conversion import format_usd_3, get_fx_rate, gtq_to_usd
from pgc.models import (
    AdminManualEditLog,
    MonthlyExchangeRate,
    MonthlyMetricResult,
    PGCPlan,
)

MONTH_LABELS = (
    (1, "Enero"),
    (2, "Febrero"),
    (3, "Marzo"),
    (4, "Abril"),
    (5, "Mayo"),
    (6, "Junio"),
    (7, "Julio"),
    (8, "Agosto"),
    (9, "Septiembre"),
    (10, "Octubre"),
    (11, "Noviembre"),
    (12, "Diciembre"),
)


def _unes() -> list[UNE]:
    return list(UNE.objects.filter(is_active=True).order_by("sort_order", "code"))


def _ingresos_metric() -> MetricDefinition | None:
    return MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()


def _normalize_currency(raw: str | None) -> str:
    curr = (raw or "GTQ").strip().upper()
    if curr in ("Q", "GTQ"):
        return MonthlyMetricResult.CURRENCY_GTQ
    if curr in ("$", "USD", "US$"):
        return MonthlyMetricResult.CURRENCY_USD
    return MonthlyMetricResult.CURRENCY_GTQ


def get_ingresos_year_context(year: int, capture_currency: str = "GTQ") -> dict:
    currency = _normalize_currency(capture_currency)
    plan = PGCPlan.objects.filter(year=year).first()
    unes = _unes()
    metric = _ingresos_metric()

    fx_by_month = {
        r.month: r
        for r in MonthlyExchangeRate.objects.filter(year=year)
    }
    results_map: dict[tuple[int, int], MonthlyMetricResult] = {}
    if plan and metric:
        for row in MonthlyMetricResult.objects.filter(
            plan=plan, metric=metric, year=year
        ).select_related("une"):
            results_map[(row.month, row.une_id)] = row

    month_rows = []
    missing_fx_for_gtq = []
    for month, label in MONTH_LABELS:
        fx_obj = fx_by_month.get(month)
        fx_value = fx_obj.usd_to_gtq if fx_obj else None
        has_fx = fx_value not in (None, Decimal("0"), 0)
        if currency == MonthlyMetricResult.CURRENCY_GTQ and not has_fx:
            missing_fx_for_gtq.append(f"{year}-{month:02d}")

        cells = []
        for une in unes:
            obj = results_map.get((month, une.id))
            measured_usd = getattr(obj, "measured_value", None) if obj else None
            source_curr = (getattr(obj, "source_currency", "") or "") if obj else ""
            source_value = getattr(obj, "source_value", None) if obj else None

            if currency == MonthlyMetricResult.CURRENCY_GTQ:
                if source_curr == MonthlyMetricResult.CURRENCY_GTQ:
                    input_value = source_value
                else:
                    input_value = None
            else:
                input_value = measured_usd

            cells.append({
                "une": une,
                "obj": obj,
                "value": input_value,
                "measured_usd": measured_usd,
                "measured_usd_display": format_usd_3(measured_usd) if measured_usd is not None else None,
                "source_currency": source_curr,
                "conversion_status": getattr(obj, "conversion_status", "") if obj else "",
                "input_disabled": (
                    currency == MonthlyMetricResult.CURRENCY_GTQ and not has_fx
                ),
            })

        month_rows.append({
            "month": month,
            "label": label,
            "fx_value": fx_value,
            "has_fx": has_fx,
            "cells": cells,
        })

    return {
        "year": year,
        "plan": plan,
        "unes": unes,
        "month_rows": month_rows,
        "capture_currency": currency,
        "missing_fx_months": missing_fx_for_gtq,
        "label": str(year),
    }


@transaction.atomic
def save_ingresos_year(user, year: int, post_data, reason: str = "") -> dict:
    if not reason.strip():
        raise ValueError("Debe indicar un motivo para guardar ingresos del año.")

    plan = PGCPlan.objects.filter(year=year).first()
    if not plan:
        raise ValueError(f"No existe plan PGC para {year}.")

    metric = _ingresos_metric()
    if not metric:
        raise ValueError("No existe la métrica INGRESOS.")

    currency = _normalize_currency(post_data.get("capture_currency"))
    unes = _unes()

    # 1) Guardar TC de todos los meses primero (afecta conversión GTQ).
    fx_post = {f"fx_value_{m}": (post_data.get(f"fx_{m}") or "") for m in range(1, 13)}
    fx_changes = save_fx(
        user,
        year,
        12,
        fx_post,
        reason=reason or "TC desde matriz anual de ingresos",
        month_from=1,
    )

    income_changes = 0
    for month, _label in MONTH_LABELS:
        fx_rate = get_fx_rate(year, month)
        for une in unes:
            key = f"ing_{month}_{une.id}"
            raw = (post_data.get(key) or "").strip()
            if raw == "":
                continue
            parsed = parse_decimal_or_none(raw)
            if parsed is None:
                raise ValueError(
                    f"Valor inválido en {year}-{month:02d} / {une.name_es}."
                )

            if currency == MonthlyMetricResult.CURRENCY_USD:
                usd_value = parsed
                obj, created = MonthlyMetricResult.objects.get_or_create(
                    plan=plan,
                    une=une,
                    metric=metric,
                    year=year,
                    month=month,
                    defaults={
                        "measured_value": usd_value,
                        "source_currency": MonthlyMetricResult.CURRENCY_USD,
                        "source_value": usd_value,
                        "exchange_rate_used": None,
                        "conversion_status": MonthlyMetricResult.CONVERSION_NATIVE_USD,
                    },
                )
                old_usd = None if created else obj.measured_value
                old_curr = "" if created else (obj.source_currency or "")
                changed = (
                    created
                    or old_usd != usd_value
                    or old_curr != MonthlyMetricResult.CURRENCY_USD
                )
                if not changed:
                    continue
                obj.measured_value = usd_value
                obj.source_currency = MonthlyMetricResult.CURRENCY_USD
                obj.source_value = usd_value
                obj.exchange_rate_used = None
                obj.conversion_status = MonthlyMetricResult.CONVERSION_NATIVE_USD
                obj.calculation_note = (
                    f"Matriz anual USD: {usd_value} USD [{year}-{month:02d}]"
                )
                obj.save(
                    update_fields=[
                        "measured_value",
                        "source_currency",
                        "source_value",
                        "exchange_rate_used",
                        "conversion_status",
                        "calculation_note",
                        "updated_at",
                    ]
                )
                log_manual_edit(
                    user=user,
                    year=year,
                    month=month,
                    entity_type=AdminManualEditLog.ENTITY_RESULT,
                    entity_id=obj.id,
                    field_name="ingresos_year_usd",
                    old_value=f"USD={old_usd}; curr={old_curr}",
                    new_value=f"USD={usd_value}",
                    reason=reason,
                )
                income_changes += 1
                continue

            # GTQ → USD
            if fx_rate is None:
                raise ValueError(
                    f"Falta tipo de cambio para {year}-{month:02d}. "
                    f"No se puede convertir ingresos de {une.name_es} en Q. "
                    "Complete la columna TC de ese mes."
                )
            usd_value = gtq_to_usd(parsed, fx_rate)
            obj, created = MonthlyMetricResult.objects.get_or_create(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
                defaults={
                    "measured_value": usd_value,
                    "source_currency": MonthlyMetricResult.CURRENCY_GTQ,
                    "source_value": parsed,
                    "exchange_rate_used": fx_rate,
                    "conversion_status": MonthlyMetricResult.CONVERSION_CONVERTED,
                },
            )
            old_usd = None if created else obj.measured_value
            old_gtq = None if created else obj.source_value
            changed = (
                created
                or old_usd != usd_value
                or old_gtq != parsed
                or obj.source_currency != MonthlyMetricResult.CURRENCY_GTQ
                or obj.exchange_rate_used != fx_rate
            )
            if not changed:
                continue
            obj.measured_value = usd_value
            obj.source_currency = MonthlyMetricResult.CURRENCY_GTQ
            obj.source_value = parsed
            obj.exchange_rate_used = fx_rate
            obj.conversion_status = MonthlyMetricResult.CONVERSION_CONVERTED
            obj.calculation_note = (
                f"Matriz anual GTQ→USD: {parsed} GTQ / {fx_rate} = {usd_value} USD "
                f"[{year}-{month:02d}]"
            )
            obj.save(
                update_fields=[
                    "measured_value",
                    "source_currency",
                    "source_value",
                    "exchange_rate_used",
                    "conversion_status",
                    "calculation_note",
                    "updated_at",
                ]
            )
            log_manual_edit(
                user=user,
                year=year,
                month=month,
                entity_type=AdminManualEditLog.ENTITY_RESULT,
                entity_id=obj.id,
                field_name="ingresos_year_gtq",
                old_value=f"GTQ={old_gtq}; USD={old_usd}",
                new_value=f"GTQ={parsed}; FX={fx_rate}; USD={usd_value}",
                reason=reason,
            )
            income_changes += 1

    return {
        "fx_changes": fx_changes,
        "income_changes": income_changes,
        "changes": fx_changes + income_changes,
        "currency": currency,
    }

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Matriz anual de ingresos reales: 12 meses × 4 UNEs + TC editable.
00003|"""
00004|
00005|from __future__ import annotations
00006|
00007|from decimal import Decimal
00008|
00009|from django.db import transaction
00010|
00011|from core.models import MetricDefinition, UNE
00012|from pgc.admin_manual import log_manual_edit, save_fx
00013|from pgc.admin_utils import parse_decimal_or_none
00014|from pgc.income_conversion import format_usd_3, get_fx_rate, gtq_to_usd
00015|from pgc.models import (
00016|    AdminManualEditLog,
00017|    MonthlyExchangeRate,
00018|    MonthlyMetricResult,
00019|    PGCPlan,
00020|)
00021|
00022|MONTH_LABELS = (
00023|    (1, "Enero"),
00024|    (2, "Febrero"),
00025|    (3, "Marzo"),
00026|    (4, "Abril"),
00027|    (5, "Mayo"),
00028|    (6, "Junio"),
00029|    (7, "Julio"),
00030|    (8, "Agosto"),
00031|    (9, "Septiembre"),
00032|    (10, "Octubre"),
00033|    (11, "Noviembre"),
00034|    (12, "Diciembre"),
00035|)
00036|
00037|
00038|def _unes() -> list[UNE]:
00039|    return list(UNE.objects.filter(is_active=True).order_by("sort_order", "code"))
00040|
00041|
00042|def _ingresos_metric() -> MetricDefinition | None:
00043|    return MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
00044|
00045|
00046|def _normalize_currency(raw: str | None) -> str:
00047|    curr = (raw or "GTQ").strip().upper()
00048|    if curr in ("Q", "GTQ"):
00049|        return MonthlyMetricResult.CURRENCY_GTQ
00050|    if curr in ("$", "USD", "US$"):
00051|        return MonthlyMetricResult.CURRENCY_USD
00052|    return MonthlyMetricResult.CURRENCY_GTQ
00053|
00054|
00055|def get_ingresos_year_context(year: int, capture_currency: str = "GTQ") -> dict:
00056|    currency = _normalize_currency(capture_currency)
00057|    plan = PGCPlan.objects.filter(year=year).first()
00058|    unes = _unes()
00059|    metric = _ingresos_metric()
00060|
00061|    fx_by_month = {
00062|        r.month: r
00063|        for r in MonthlyExchangeRate.objects.filter(year=year)
00064|    }
00065|    results_map: dict[tuple[int, int], MonthlyMetricResult] = {}
00066|    if plan and metric:
00067|        for row in MonthlyMetricResult.objects.filter(
00068|            plan=plan, metric=metric, year=year
00069|        ).select_related("une"):
00070|            results_map[(row.month, row.une_id)] = row
00071|
00072|    month_rows = []
00073|    missing_fx_for_gtq = []
00074|    for month, label in MONTH_LABELS:
00075|        fx_obj = fx_by_month.get(month)
00076|        fx_value = fx_obj.usd_to_gtq if fx_obj else None
00077|        has_fx = fx_value not in (None, Decimal("0"), 0)
00078|        if currency == MonthlyMetricResult.CURRENCY_GTQ and not has_fx:
00079|            missing_fx_for_gtq.append(f"{year}-{month:02d}")
00080|
00081|        cells = []
00082|        for une in unes:
00083|            obj = results_map.get((month, une.id))
00084|            measured_usd = getattr(obj, "measured_value", None) if obj else None
00085|            source_curr = (getattr(obj, "source_currency", "") or "") if obj else ""
00086|            source_value = getattr(obj, "source_value", None) if obj else None
00087|
00088|            if currency == MonthlyMetricResult.CURRENCY_GTQ:
00089|                if source_curr == MonthlyMetricResult.CURRENCY_GTQ:
00090|                    input_value = source_value
00091|                else:
00092|                    input_value = None
00093|            else:
00094|                input_value = measured_usd
00095|
00096|            cells.append({
00097|                "une": une,
00098|                "obj": obj,
00099|                "value": input_value,
00100|                "measured_usd": measured_usd,
00101|                "measured_usd_display": format_usd_3(measured_usd) if measured_usd is not None else None,
00102|                "source_currency": source_curr,
00103|                "conversion_status": getattr(obj, "conversion_status", "") if obj else "",
00104|                "input_disabled": (
00105|                    currency == MonthlyMetricResult.CURRENCY_GTQ and not has_fx
00106|                ),
00107|            })
00108|
00109|        month_rows.append({
00110|            "month": month,
00111|            "label": label,
00112|            "fx_value": fx_value,
00113|            "has_fx": has_fx,
00114|            "cells": cells,
00115|        })
00116|
00117|    return {
00118|        "year": year,
00119|        "plan": plan,
00120|        "unes": unes,
00121|        "month_rows": month_rows,
00122|        "capture_currency": currency,
00123|        "missing_fx_months": missing_fx_for_gtq,
00124|        "label": str(year),
00125|    }
00126|
00127|
00128|@transaction.atomic
00129|def save_ingresos_year(user, year: int, post_data, reason: str = "") -> dict:
00130|    if not reason.strip():
00131|        raise ValueError("Debe indicar un motivo para guardar ingresos del año.")
00132|
00133|    plan = PGCPlan.objects.filter(year=year).first()
00134|    if not plan:
00135|        raise ValueError(f"No existe plan PGC para {year}.")
00136|
00137|    metric = _ingresos_metric()
00138|    if not metric:
00139|        raise ValueError("No existe la métrica INGRESOS.")
00140|
00141|    currency = _normalize_currency(post_data.get("capture_currency"))
00142|    unes = _unes()
00143|
00144|    # 1) Guardar TC de todos los meses primero (afecta conversión GTQ).
00145|    fx_post = {f"fx_value_{m}": (post_data.get(f"fx_{m}") or "") for m in range(1, 13)}
00146|    fx_changes = save_fx(
00147|        user,
00148|        year,
00149|        12,
00150|        fx_post,
00151|        reason=reason or "TC desde matriz anual de ingresos",
00152|        month_from=1,
00153|    )
00154|
00155|    income_changes = 0
00156|    for month, _label in MONTH_LABELS:
00157|        fx_rate = get_fx_rate(year, month)
00158|        for une in unes:
00159|            key = f"ing_{month}_{une.id}"
00160|            raw = (post_data.get(key) or "").strip()
00161|            if raw == "":
00162|                continue
00163|            parsed = parse_decimal_or_none(raw)
00164|            if parsed is None:
00165|                raise ValueError(
00166|                    f"Valor inválido en {year}-{month:02d} / {une.name_es}."
00167|                )
00168|
00169|            if currency == MonthlyMetricResult.CURRENCY_USD:
00170|                usd_value = parsed
00171|                obj, created = MonthlyMetricResult.objects.get_or_create(
00172|                    plan=plan,
00173|                    une=une,
00174|                    metric=metric,
00175|                    year=year,
00176|                    month=month,
00177|                    defaults={
00178|                        "measured_value": usd_value,
00179|                        "source_currency": MonthlyMetricResult.CURRENCY_USD,
00180|                        "source_value": usd_value,
00181|                        "exchange_rate_used": None,
00182|                        "conversion_status": MonthlyMetricResult.CONVERSION_NATIVE_USD,
00183|                    },
00184|                )
00185|                old_usd = None if created else obj.measured_value
00186|                old_curr = "" if created else (obj.source_currency or "")
00187|                changed = (
00188|                    created
00189|                    or old_usd != usd_value
00190|                    or old_curr != MonthlyMetricResult.CURRENCY_USD
00191|                )
00192|                if not changed:
00193|                    continue
00194|                obj.measured_value = usd_value
00195|                obj.source_currency = MonthlyMetricResult.CURRENCY_USD
00196|                obj.source_value = usd_value
00197|                obj.exchange_rate_used = None
00198|                obj.conversion_status = MonthlyMetricResult.CONVERSION_NATIVE_USD
00199|                obj.calculation_note = (
00200|                    f"Matriz anual USD: {usd_value} USD [{year}-{month:02d}]"
00201|                )
00202|                obj.save(
00203|                    update_fields=[
00204|                        "measured_value",
00205|                        "source_currency",
00206|                        "source_value",
00207|                        "exchange_rate_used",
00208|                        "conversion_status",
00209|                        "calculation_note",
00210|                        "updated_at",
00211|                    ]
00212|                )
00213|                log_manual_edit(
00214|                    user=user,
00215|                    year=year,
00216|                    month=month,
00217|                    entity_type=AdminManualEditLog.ENTITY_RESULT,
00218|                    entity_id=obj.id,
00219|                    field_name="ingresos_year_usd",
00220|                    old_value=f"USD={old_usd}; curr={old_curr}",
00221|                    new_value=f"USD={usd_value}",
00222|                    reason=reason,
00223|                )
00224|                income_changes += 1
00225|                continue
00226|
00227|            # GTQ → USD
00228|            if fx_rate is None:
00229|                raise ValueError(
00230|                    f"Falta tipo de cambio para {year}-{month:02d}. "
00231|                    f"No se puede convertir ingresos de {une.name_es} en Q. "
00232|                    "Complete la columna TC de ese mes."
00233|                )
00234|            usd_value = gtq_to_usd(parsed, fx_rate)
00235|            obj, created = MonthlyMetricResult.objects.get_or_create(
00236|                plan=plan,
00237|                une=une,
00238|                metric=metric,
00239|                year=year,
00240|                month=month,
00241|                defaults={
00242|                    "measured_value": usd_value,
00243|                    "source_currency": MonthlyMetricResult.CURRENCY_GTQ,
00244|                    "source_value": parsed,
00245|                    "exchange_rate_used": fx_rate,
00246|                    "conversion_status": MonthlyMetricResult.CONVERSION_CONVERTED,
00247|                },
00248|            )
00249|            old_usd = None if created else obj.measured_value
00250|            old_gtq = None if created else obj.source_value
00251|            changed = (
00252|                created
00253|                or old_usd != usd_value
00254|                or old_gtq != parsed
00255|                or obj.source_currency != MonthlyMetricResult.CURRENCY_GTQ
00256|                or obj.exchange_rate_used != fx_rate
00257|            )
00258|            if not changed:
00259|                continue
00260|            obj.measured_value = usd_value
00261|            obj.source_currency = MonthlyMetricResult.CURRENCY_GTQ
00262|            obj.source_value = parsed
00263|            obj.exchange_rate_used = fx_rate
00264|            obj.conversion_status = MonthlyMetricResult.CONVERSION_CONVERTED
00265|            obj.calculation_note = (
00266|                f"Matriz anual GTQ→USD: {parsed} GTQ / {fx_rate} = {usd_value} USD "
00267|                f"[{year}-{month:02d}]"
00268|            )
00269|            obj.save(
00270|                update_fields=[
00271|                    "measured_value",
00272|                    "source_currency",
00273|                    "source_value",
00274|                    "exchange_rate_used",
00275|                    "conversion_status",
00276|                    "calculation_note",
00277|                    "updated_at",
00278|                ]
00279|            )
00280|            log_manual_edit(
00281|                user=user,
00282|                year=year,
00283|                month=month,
00284|                entity_type=AdminManualEditLog.ENTITY_RESULT,
00285|                entity_id=obj.id,
00286|                field_name="ingresos_year_gtq",
00287|                old_value=f"GTQ={old_gtq}; USD={old_usd}",
00288|                new_value=f"GTQ={parsed}; FX={fx_rate}; USD={usd_value}",
00289|                reason=reason,
00290|            )
00291|            income_changes += 1
00292|
00293|    return {
00294|        "fx_changes": fx_changes,
00295|        "income_changes": income_changes,
00296|        "changes": fx_changes + income_changes,
00297|        "currency": currency,
00298|    }

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiCk1hdHJpeiBhbnVhbCBkZSBpbmdyZXNvcyByZWFsZXM6IDEyIG1lc2VzIMOXIDQgVU5FcyArIFRDIGVkaXRhYmxlLgoiIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmZyb20gZGVjaW1hbCBpbXBvcnQgRGVjaW1hbAoKZnJvbSBkamFuZ28uZGIgaW1wb3J0IHRyYW5zYWN0aW9uCgpmcm9tIGNvcmUubW9kZWxzIGltcG9ydCBNZXRyaWNEZWZpbml0aW9uLCBVTkUKZnJvbSBwZ2MuYWRtaW5fbWFudWFsIGltcG9ydCBsb2dfbWFudWFsX2VkaXQsIHNhdmVfZngKZnJvbSBwZ2MuYWRtaW5fdXRpbHMgaW1wb3J0IHBhcnNlX2RlY2ltYWxfb3Jfbm9uZQpmcm9tIHBnYy5pbmNvbWVfY29udmVyc2lvbiBpbXBvcnQgZm9ybWF0X3VzZF8zLCBnZXRfZnhfcmF0ZSwgZ3RxX3RvX3VzZApmcm9tIHBnYy5tb2RlbHMgaW1wb3J0ICgKICAgIEFkbWluTWFudWFsRWRpdExvZywKICAgIE1vbnRobHlFeGNoYW5nZVJhdGUsCiAgICBNb250aGx5TWV0cmljUmVzdWx0LAogICAgUEdDUGxhbiwKKQoKTU9OVEhfTEFCRUxTID0gKAogICAgKDEsICJFbmVybyIpLAogICAgKDIsICJGZWJyZXJvIiksCiAgICAoMywgIk1hcnpvIiksCiAgICAoNCwgIkFicmlsIiksCiAgICAoNSwgIk1heW8iKSwKICAgICg2LCAiSnVuaW8iKSwKICAgICg3LCAiSnVsaW8iKSwKICAgICg4LCAiQWdvc3RvIiksCiAgICAoOSwgIlNlcHRpZW1icmUiKSwKICAgICgxMCwgIk9jdHVicmUiKSwKICAgICgxMSwgIk5vdmllbWJyZSIpLAogICAgKDEyLCAiRGljaWVtYnJlIiksCikKCgpkZWYgX3VuZXMoKSAtPiBsaXN0W1VORV06CiAgICByZXR1cm4gbGlzdChVTkUub2JqZWN0cy5maWx0ZXIoaXNfYWN0aXZlPVRydWUpLm9yZGVyX2J5KCJzb3J0X29yZGVyIiwgImNvZGUiKSkKCgpkZWYgX2luZ3Jlc29zX21ldHJpYygpIC0+IE1ldHJpY0RlZmluaXRpb24gfCBOb25lOgogICAgcmV0dXJuIE1ldHJpY0RlZmluaXRpb24ub2JqZWN0cy5maWx0ZXIoY29kZT1NZXRyaWNEZWZpbml0aW9uLkNPREVfSU5HUkVTT1MpLmZpcnN0KCkKCgpkZWYgX25vcm1hbGl6ZV9jdXJyZW5jeShyYXc6IHN0ciB8IE5vbmUpIC0+IHN0cjoKICAgIGN1cnIgPSAocmF3IG9yICJHVFEiKS5zdHJpcCgpLnVwcGVyKCkKICAgIGlmIGN1cnIgaW4gKCJRIiwgIkdUUSIpOgogICAgICAgIHJldHVybiBNb250aGx5TWV0cmljUmVzdWx0LkNVUlJFTkNZX0dUUQogICAgaWYgY3VyciBpbiAoIiQiLCAiVVNEIiwgIlVTJCIpOgogICAgICAgIHJldHVybiBNb250aGx5TWV0cmljUmVzdWx0LkNVUlJFTkNZX1VTRAogICAgcmV0dXJuIE1vbnRobHlNZXRyaWNSZXN1bHQuQ1VSUkVOQ1lfR1RRCgoKZGVmIGdldF9pbmdyZXNvc195ZWFyX2NvbnRleHQoeWVhcjogaW50LCBjYXB0dXJlX2N1cnJlbmN5OiBzdHIgPSAiR1RRIikgLT4gZGljdDoKICAgIGN1cnJlbmN5ID0gX25vcm1hbGl6ZV9jdXJyZW5jeShjYXB0dXJlX2N1cnJlbmN5KQogICAgcGxhbiA9IFBHQ1BsYW4ub2JqZWN0cy5maWx0ZXIoeWVhcj15ZWFyKS5maXJzdCgpCiAgICB1bmVzID0gX3VuZXMoKQogICAgbWV0cmljID0gX2luZ3Jlc29zX21ldHJpYygpCgogICAgZnhfYnlfbW9udGggPSB7CiAgICAgICAgci5tb250aDogcgogICAgICAgIGZvciByIGluIE1vbnRobHlFeGNoYW5nZVJhdGUub2JqZWN0cy5maWx0ZXIoeWVhcj15ZWFyKQogICAgfQogICAgcmVzdWx0c19tYXA6IGRpY3RbdHVwbGVbaW50LCBpbnRdLCBNb250aGx5TWV0cmljUmVzdWx0XSA9IHt9CiAgICBpZiBwbGFuIGFuZCBtZXRyaWM6CiAgICAgICAgZm9yIHJvdyBpbiBNb250aGx5TWV0cmljUmVzdWx0Lm9iamVjdHMuZmlsdGVyKAogICAgICAgICAgICBwbGFuPXBsYW4sIG1ldHJpYz1tZXRyaWMsIHllYXI9eWVhcgogICAgICAgICkuc2VsZWN0X3JlbGF0ZWQoInVuZSIpOgogICAgICAgICAgICByZXN1bHRzX21hcFsocm93Lm1vbnRoLCByb3cudW5lX2lkKV0gPSByb3cKCiAgICBtb250aF9yb3dzID0gW10KICAgIG1pc3NpbmdfZnhfZm9yX2d0cSA9IFtdCiAgICBmb3IgbW9udGgsIGxhYmVsIGluIE1PTlRIX0xBQkVMUzoKICAgICAgICBmeF9vYmogPSBmeF9ieV9tb250aC5nZXQobW9udGgpCiAgICAgICAgZnhfdmFsdWUgPSBmeF9vYmoudXNkX3RvX2d0cSBpZiBmeF9vYmogZWxzZSBOb25lCiAgICAgICAgaGFzX2Z4ID0gZnhfdmFsdWUgbm90IGluIChOb25lLCBEZWNpbWFsKCIwIiksIDApCiAgICAgICAgaWYgY3VycmVuY3kgPT0gTW9udGhseU1ldHJpY1Jlc3VsdC5DVVJSRU5DWV9HVFEgYW5kIG5vdCBoYXNfZng6CiAgICAgICAgICAgIG1pc3NpbmdfZnhfZm9yX2d0cS5hcHBlbmQoZiJ7eWVhcn0te21vbnRoOjAyZH0iKQoKICAgICAgICBjZWxscyA9IFtdCiAgICAgICAgZm9yIHVuZSBpbiB1bmVzOgogICAgICAgICAgICBvYmogPSByZXN1bHRzX21hcC5nZXQoKG1vbnRoLCB1bmUuaWQpKQogICAgICAgICAgICBtZWFzdXJlZF91c2QgPSBnZXRhdHRyKG9iaiwgIm1lYXN1cmVkX3ZhbHVlIiwgTm9uZSkgaWYgb2JqIGVsc2UgTm9uZQogICAgICAgICAgICBzb3VyY2VfY3VyciA9IChnZXRhdHRyKG9iaiwgInNvdXJjZV9jdXJyZW5jeSIsICIiKSBvciAiIikgaWYgb2JqIGVsc2UgIiIKICAgICAgICAgICAgc291cmNlX3ZhbHVlID0gZ2V0YXR0cihvYmosICJzb3VyY2VfdmFsdWUiLCBOb25lKSBpZiBvYmogZWxzZSBOb25lCgogICAgICAgICAgICBpZiBjdXJyZW5jeSA9PSBNb250aGx5TWV0cmljUmVzdWx0LkNVUlJFTkNZX0dUUToKICAgICAgICAgICAgICAgIGlmIHNvdXJjZV9jdXJyID09IE1vbnRobHlNZXRyaWNSZXN1bHQuQ1VSUkVOQ1lfR1RROgogICAgICAgICAgICAgICAgICAgIGlucHV0X3ZhbHVlID0gc291cmNlX3ZhbHVlCiAgICAgICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgICAgIGlucHV0X3ZhbHVlID0gTm9uZQogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgaW5wdXRfdmFsdWUgPSBtZWFzdXJlZF91c2QKCiAgICAgICAgICAgIGNlbGxzLmFwcGVuZCh7CiAgICAgICAgICAgICAgICAidW5lIjogdW5lLAogICAgICAgICAgICAgICAgIm9iaiI6IG9iaiwKICAgICAgICAgICAgICAgICJ2YWx1ZSI6IGlucHV0X3ZhbHVlLAogICAgICAgICAgICAgICAgIm1lYXN1cmVkX3VzZCI6IG1lYXN1cmVkX3VzZCwKICAgICAgICAgICAgICAgICJtZWFzdXJlZF91c2RfZGlzcGxheSI6IGZvcm1hdF91c2RfMyhtZWFzdXJlZF91c2QpIGlmIG1lYXN1cmVkX3VzZCBpcyBub3QgTm9uZSBlbHNlIE5vbmUsCiAgICAgICAgICAgICAgICAic291cmNlX2N1cnJlbmN5Ijogc291cmNlX2N1cnIsCiAgICAgICAgICAgICAgICAiY29udmVyc2lvbl9zdGF0dXMiOiBnZXRhdHRyKG9iaiwgImNvbnZlcnNpb25fc3RhdHVzIiwgIiIpIGlmIG9iaiBlbHNlICIiLAogICAgICAgICAgICAgICAgImlucHV0X2Rpc2FibGVkIjogKAogICAgICAgICAgICAgICAgICAgIGN1cnJlbmN5ID09IE1vbnRobHlNZXRyaWNSZXN1bHQuQ1VSUkVOQ1lfR1RRIGFuZCBub3QgaGFzX2Z4CiAgICAgICAgICAgICAgICApLAogICAgICAgICAgICB9KQoKICAgICAgICBtb250aF9yb3dzLmFwcGVuZCh7CiAgICAgICAgICAgICJtb250aCI6IG1vbnRoLAogICAgICAgICAgICAibGFiZWwiOiBsYWJlbCwKICAgICAgICAgICAgImZ4X3ZhbHVlIjogZnhfdmFsdWUsCiAgICAgICAgICAgICJoYXNfZngiOiBoYXNfZngsCiAgICAgICAgICAgICJjZWxscyI6IGNlbGxzLAogICAgICAgIH0pCgogICAgcmV0dXJuIHsKICAgICAgICAieWVhciI6IHllYXIsCiAgICAgICAgInBsYW4iOiBwbGFuLAogICAgICAgICJ1bmVzIjogdW5lcywKICAgICAgICAibW9udGhfcm93cyI6IG1vbnRoX3Jvd3MsCiAgICAgICAgImNhcHR1cmVfY3VycmVuY3kiOiBjdXJyZW5jeSwKICAgICAgICAibWlzc2luZ19meF9tb250aHMiOiBtaXNzaW5nX2Z4X2Zvcl9ndHEsCiAgICAgICAgImxhYmVsIjogc3RyKHllYXIpLAogICAgfQoKCkB0cmFuc2FjdGlvbi5hdG9taWMKZGVmIHNhdmVfaW5ncmVzb3NfeWVhcih1c2VyLCB5ZWFyOiBpbnQsIHBvc3RfZGF0YSwgcmVhc29uOiBzdHIgPSAiIikgLT4gZGljdDoKICAgIGlmIG5vdCByZWFzb24uc3RyaXAoKToKICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJEZWJlIGluZGljYXIgdW4gbW90aXZvIHBhcmEgZ3VhcmRhciBpbmdyZXNvcyBkZWwgYcOxby4iKQoKICAgIHBsYW4gPSBQR0NQbGFuLm9iamVjdHMuZmlsdGVyKHllYXI9eWVhcikuZmlyc3QoKQogICAgaWYgbm90IHBsYW46CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIk5vIGV4aXN0ZSBwbGFuIFBHQyBwYXJhIHt5ZWFyfS4iKQoKICAgIG1ldHJpYyA9IF9pbmdyZXNvc19tZXRyaWMoKQogICAgaWYgbm90IG1ldHJpYzoKICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJObyBleGlzdGUgbGEgbcOpdHJpY2EgSU5HUkVTT1MuIikKCiAgICBjdXJyZW5jeSA9IF9ub3JtYWxpemVfY3VycmVuY3kocG9zdF9kYXRhLmdldCgiY2FwdHVyZV9jdXJyZW5jeSIpKQogICAgdW5lcyA9IF91bmVzKCkKCiAgICAjIDEpIEd1YXJkYXIgVEMgZGUgdG9kb3MgbG9zIG1lc2VzIHByaW1lcm8gKGFmZWN0YSBjb252ZXJzacOzbiBHVFEpLgogICAgZnhfcG9zdCA9IHtmImZ4X3ZhbHVlX3ttfSI6IChwb3N0X2RhdGEuZ2V0KGYiZnhfe219Iikgb3IgIiIpIGZvciBtIGluIHJhbmdlKDEsIDEzKX0KICAgIGZ4X2NoYW5nZXMgPSBzYXZlX2Z4KAogICAgICAgIHVzZXIsCiAgICAgICAgeWVhciwKICAgICAgICAxMiwKICAgICAgICBmeF9wb3N0LAogICAgICAgIHJlYXNvbj1yZWFzb24gb3IgIlRDIGRlc2RlIG1hdHJpeiBhbnVhbCBkZSBpbmdyZXNvcyIsCiAgICAgICAgbW9udGhfZnJvbT0xLAogICAgKQoKICAgIGluY29tZV9jaGFuZ2VzID0gMAogICAgZm9yIG1vbnRoLCBfbGFiZWwgaW4gTU9OVEhfTEFCRUxTOgogICAgICAgIGZ4X3JhdGUgPSBnZXRfZnhfcmF0ZSh5ZWFyLCBtb250aCkKICAgICAgICBmb3IgdW5lIGluIHVuZXM6CiAgICAgICAgICAgIGtleSA9IGYiaW5nX3ttb250aH1fe3VuZS5pZH0iCiAgICAgICAgICAgIHJhdyA9IChwb3N0X2RhdGEuZ2V0KGtleSkgb3IgIiIpLnN0cmlwKCkKICAgICAgICAgICAgaWYgcmF3ID09ICIiOgogICAgICAgICAgICAgICAgY29udGludWUKICAgICAgICAgICAgcGFyc2VkID0gcGFyc2VfZGVjaW1hbF9vcl9ub25lKHJhdykKICAgICAgICAgICAgaWYgcGFyc2VkIGlzIE5vbmU6CiAgICAgICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKAogICAgICAgICAgICAgICAgICAgIGYiVmFsb3IgaW52w6FsaWRvIGVuIHt5ZWFyfS17bW9udGg6MDJkfSAvIHt1bmUubmFtZV9lc30uIgogICAgICAgICAgICAgICAgKQoKICAgICAgICAgICAgaWYgY3VycmVuY3kgPT0gTW9udGhseU1ldHJpY1Jlc3VsdC5DVVJSRU5DWV9VU0Q6CiAgICAgICAgICAgICAgICB1c2RfdmFsdWUgPSBwYXJzZWQKICAgICAgICAgICAgICAgIG9iaiwgY3JlYXRlZCA9IE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgICAgICAgICB1bmU9dW5lLAogICAgICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICAgICAgICAgIm1lYXN1cmVkX3ZhbHVlIjogdXNkX3ZhbHVlLAogICAgICAgICAgICAgICAgICAgICAgICAic291cmNlX2N1cnJlbmN5IjogTW9udGhseU1ldHJpY1Jlc3VsdC5DVVJSRU5DWV9VU0QsCiAgICAgICAgICAgICAgICAgICAgICAgICJzb3VyY2VfdmFsdWUiOiB1c2RfdmFsdWUsCiAgICAgICAgICAgICAgICAgICAgICAgICJleGNoYW5nZV9yYXRlX3VzZWQiOiBOb25lLAogICAgICAgICAgICAgICAgICAgICAgICAiY29udmVyc2lvbl9zdGF0dXMiOiBNb250aGx5TWV0cmljUmVzdWx0LkNPTlZFUlNJT05fTkFUSVZFX1VTRCwKICAgICAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgb2xkX3VzZCA9IE5vbmUgaWYgY3JlYXRlZCBlbHNlIG9iai5tZWFzdXJlZF92YWx1ZQogICAgICAgICAgICAgICAgb2xkX2N1cnIgPSAiIiBpZiBjcmVhdGVkIGVsc2UgKG9iai5zb3VyY2VfY3VycmVuY3kgb3IgIiIpCiAgICAgICAgICAgICAgICBjaGFuZ2VkID0gKAogICAgICAgICAgICAgICAgICAgIGNyZWF0ZWQKICAgICAgICAgICAgICAgICAgICBvciBvbGRfdXNkICE9IHVzZF92YWx1ZQogICAgICAgICAgICAgICAgICAgIG9yIG9sZF9jdXJyICE9IE1vbnRobHlNZXRyaWNSZXN1bHQuQ1VSUkVOQ1lfVVNECiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICBpZiBub3QgY2hhbmdlZDoKICAgICAgICAgICAgICAgICAgICBjb250aW51ZQogICAgICAgICAgICAgICAgb2JqLm1lYXN1cmVkX3ZhbHVlID0gdXNkX3ZhbHVlCiAgICAgICAgICAgICAgICBvYmouc291cmNlX2N1cnJlbmN5ID0gTW9udGhseU1ldHJpY1Jlc3VsdC5DVVJSRU5DWV9VU0QKICAgICAgICAgICAgICAgIG9iai5zb3VyY2VfdmFsdWUgPSB1c2RfdmFsdWUKICAgICAgICAgICAgICAgIG9iai5leGNoYW5nZV9yYXRlX3VzZWQgPSBOb25lCiAgICAgICAgICAgICAgICBvYmouY29udmVyc2lvbl9zdGF0dXMgPSBNb250aGx5TWV0cmljUmVzdWx0LkNPTlZFUlNJT05fTkFUSVZFX1VTRAogICAgICAgICAgICAgICAgb2JqLmNhbGN1bGF0aW9uX25vdGUgPSAoCiAgICAgICAgICAgICAgICAgICAgZiJNYXRyaXogYW51YWwgVVNEOiB7dXNkX3ZhbHVlfSBVU0QgW3t5ZWFyfS17bW9udGg6MDJkfV0iCiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICBvYmouc2F2ZSgKICAgICAgICAgICAgICAgICAgICB1cGRhdGVfZmllbGRzPVsKICAgICAgICAgICAgICAgICAgICAgICAgIm1lYXN1cmVkX3ZhbHVlIiwKICAgICAgICAgICAgICAgICAgICAgICAgInNvdXJjZV9jdXJyZW5jeSIsCiAgICAgICAgICAgICAgICAgICAgICAgICJzb3VyY2VfdmFsdWUiLAogICAgICAgICAgICAgICAgICAgICAgICAiZXhjaGFuZ2VfcmF0ZV91c2VkIiwKICAgICAgICAgICAgICAgICAgICAgICAgImNvbnZlcnNpb25fc3RhdHVzIiwKICAgICAgICAgICAgICAgICAgICAgICAgImNhbGN1bGF0aW9uX25vdGUiLAogICAgICAgICAgICAgICAgICAgICAgICAidXBkYXRlZF9hdCIsCiAgICAgICAgICAgICAgICAgICAgXQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgbG9nX21hbnVhbF9lZGl0KAogICAgICAgICAgICAgICAgICAgIHVzZXI9dXNlciwKICAgICAgICAgICAgICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgICAgICAgICAgZW50aXR5X3R5cGU9QWRtaW5NYW51YWxFZGl0TG9nLkVOVElUWV9SRVNVTFQsCiAgICAgICAgICAgICAgICAgICAgZW50aXR5X2lkPW9iai5pZCwKICAgICAgICAgICAgICAgICAgICBmaWVsZF9uYW1lPSJpbmdyZXNvc195ZWFyX3VzZCIsCiAgICAgICAgICAgICAgICAgICAgb2xkX3ZhbHVlPWYiVVNEPXtvbGRfdXNkfTsgY3Vycj17b2xkX2N1cnJ9IiwKICAgICAgICAgICAgICAgICAgICBuZXdfdmFsdWU9ZiJVU0Q9e3VzZF92YWx1ZX0iLAogICAgICAgICAgICAgICAgICAgIHJlYXNvbj1yZWFzb24sCiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICBpbmNvbWVfY2hhbmdlcyArPSAxCiAgICAgICAgICAgICAgICBjb250aW51ZQoKICAgICAgICAgICAgIyBHVFEg4oaSIFVTRAogICAgICAgICAgICBpZiBmeF9yYXRlIGlzIE5vbmU6CiAgICAgICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKAogICAgICAgICAgICAgICAgICAgIGYiRmFsdGEgdGlwbyBkZSBjYW1iaW8gcGFyYSB7eWVhcn0te21vbnRoOjAyZH0uICIKICAgICAgICAgICAgICAgICAgICBmIk5vIHNlIHB1ZWRlIGNvbnZlcnRpciBpbmdyZXNvcyBkZSB7dW5lLm5hbWVfZXN9IGVuIFEuICIKICAgICAgICAgICAgICAgICAgICAiQ29tcGxldGUgbGEgY29sdW1uYSBUQyBkZSBlc2UgbWVzLiIKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgdXNkX3ZhbHVlID0gZ3RxX3RvX3VzZChwYXJzZWQsIGZ4X3JhdGUpCiAgICAgICAgICAgIG9iaiwgY3JlYXRlZCA9IE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgcGxhbj1wbGFuLAogICAgICAgICAgICAgICAgdW5lPXVuZSwKICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgICAgICAgICBtb250aD1tb250aCwKICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICAgICAibWVhc3VyZWRfdmFsdWUiOiB1c2RfdmFsdWUsCiAgICAgICAgICAgICAgICAgICAgInNvdXJjZV9jdXJyZW5jeSI6IE1vbnRobHlNZXRyaWNSZXN1bHQuQ1VSUkVOQ1lfR1RRLAogICAgICAgICAgICAgICAgICAgICJzb3VyY2VfdmFsdWUiOiBwYXJzZWQsCiAgICAgICAgICAgICAgICAgICAgImV4Y2hhbmdlX3JhdGVfdXNlZCI6IGZ4X3JhdGUsCiAgICAgICAgICAgICAgICAgICAgImNvbnZlcnNpb25fc3RhdHVzIjogTW9udGhseU1ldHJpY1Jlc3VsdC5DT05WRVJTSU9OX0NPTlZFUlRFRCwKICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICkKICAgICAgICAgICAgb2xkX3VzZCA9IE5vbmUgaWYgY3JlYXRlZCBlbHNlIG9iai5tZWFzdXJlZF92YWx1ZQogICAgICAgICAgICBvbGRfZ3RxID0gTm9uZSBpZiBjcmVhdGVkIGVsc2Ugb2JqLnNvdXJjZV92YWx1ZQogICAgICAgICAgICBjaGFuZ2VkID0gKAogICAgICAgICAgICAgICAgY3JlYXRlZAogICAgICAgICAgICAgICAgb3Igb2xkX3VzZCAhPSB1c2RfdmFsdWUKICAgICAgICAgICAgICAgIG9yIG9sZF9ndHEgIT0gcGFyc2VkCiAgICAgICAgICAgICAgICBvciBvYmouc291cmNlX2N1cnJlbmN5ICE9IE1vbnRobHlNZXRyaWNSZXN1bHQuQ1VSUkVOQ1lfR1RRCiAgICAgICAgICAgICAgICBvciBvYmouZXhjaGFuZ2VfcmF0ZV91c2VkICE9IGZ4X3JhdGUKICAgICAgICAgICAgKQogICAgICAgICAgICBpZiBub3QgY2hhbmdlZDoKICAgICAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgICAgIG9iai5tZWFzdXJlZF92YWx1ZSA9IHVzZF92YWx1ZQogICAgICAgICAgICBvYmouc291cmNlX2N1cnJlbmN5ID0gTW9udGhseU1ldHJpY1Jlc3VsdC5DVVJSRU5DWV9HVFEKICAgICAgICAgICAgb2JqLnNvdXJjZV92YWx1ZSA9IHBhcnNlZAogICAgICAgICAgICBvYmouZXhjaGFuZ2VfcmF0ZV91c2VkID0gZnhfcmF0ZQogICAgICAgICAgICBvYmouY29udmVyc2lvbl9zdGF0dXMgPSBNb250aGx5TWV0cmljUmVzdWx0LkNPTlZFUlNJT05fQ09OVkVSVEVECiAgICAgICAgICAgIG9iai5jYWxjdWxhdGlvbl9ub3RlID0gKAogICAgICAgICAgICAgICAgZiJNYXRyaXogYW51YWwgR1RR4oaSVVNEOiB7cGFyc2VkfSBHVFEgLyB7ZnhfcmF0ZX0gPSB7dXNkX3ZhbHVlfSBVU0QgIgogICAgICAgICAgICAgICAgZiJbe3llYXJ9LXttb250aDowMmR9XSIKICAgICAgICAgICAgKQogICAgICAgICAgICBvYmouc2F2ZSgKICAgICAgICAgICAgICAgIHVwZGF0ZV9maWVsZHM9WwogICAgICAgICAgICAgICAgICAgICJtZWFzdXJlZF92YWx1ZSIsCiAgICAgICAgICAgICAgICAgICAgInNvdXJjZV9jdXJyZW5jeSIsCiAgICAgICAgICAgICAgICAgICAgInNvdXJjZV92YWx1ZSIsCiAgICAgICAgICAgICAgICAgICAgImV4Y2hhbmdlX3JhdGVfdXNlZCIsCiAgICAgICAgICAgICAgICAgICAgImNvbnZlcnNpb25fc3RhdHVzIiwKICAgICAgICAgICAgICAgICAgICAiY2FsY3VsYXRpb25fbm90ZSIsCiAgICAgICAgICAgICAgICAgICAgInVwZGF0ZWRfYXQiLAogICAgICAgICAgICAgICAgXQogICAgICAgICAgICApCiAgICAgICAgICAgIGxvZ19tYW51YWxfZWRpdCgKICAgICAgICAgICAgICAgIHVzZXI9dXNlciwKICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgZW50aXR5X3R5cGU9QWRtaW5NYW51YWxFZGl0TG9nLkVOVElUWV9SRVNVTFQsCiAgICAgICAgICAgICAgICBlbnRpdHlfaWQ9b2JqLmlkLAogICAgICAgICAgICAgICAgZmllbGRfbmFtZT0iaW5ncmVzb3NfeWVhcl9ndHEiLAogICAgICAgICAgICAgICAgb2xkX3ZhbHVlPWYiR1RRPXtvbGRfZ3RxfTsgVVNEPXtvbGRfdXNkfSIsCiAgICAgICAgICAgICAgICBuZXdfdmFsdWU9ZiJHVFE9e3BhcnNlZH07IEZYPXtmeF9yYXRlfTsgVVNEPXt1c2RfdmFsdWV9IiwKICAgICAgICAgICAgICAgIHJlYXNvbj1yZWFzb24sCiAgICAgICAgICAgICkKICAgICAgICAgICAgaW5jb21lX2NoYW5nZXMgKz0gMQoKICAgIHJldHVybiB7CiAgICAgICAgImZ4X2NoYW5nZXMiOiBmeF9jaGFuZ2VzLAogICAgICAgICJpbmNvbWVfY2hhbmdlcyI6IGluY29tZV9jaGFuZ2VzLAogICAgICAgICJjaGFuZ2VzIjogZnhfY2hhbmdlcyArIGluY29tZV9jaGFuZ2VzLAogICAgICAgICJjdXJyZW5jeSI6IGN1cnJlbmN5LAogICAgfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/admin_manual.py
PATH_JSON="pgc/admin_manual.py"
FILENAME=admin_manual.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=842
SIZE_BYTES_UTF8=30476
CONTENT_SHA256=871ea2d18ca859612c965dc76a53a65445db97ccb7ff73dff48799eaef2dc07a
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""
Edición manual del período con trazabilidad.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from django.db import transaction

from core.models import MetricDefinition, SystemSetting, UNE, UNEAlias
from imports.models import CrossSaleImportRow, NewClientImportRow
from pgc.models import (
    AdminManualEditLog,
    ManualRequirementsCompliance,
    MonthlyExchangeRate,
    MonthlyMetricResult,
    MonthlyTarget,
    PGCPlan,
)

from pgc.admin_utils import format_value, parse_decimal_or_none
from pgc.income_conversion import (
    count_stale_ingresos,
    format_usd_3,
    get_fx_rate,
    gtq_to_usd,
    mark_ingresos_stale_for_fx_change,
)

# Orden = ruta financiera sugerida (TC → metas → captura → resto).
MANUAL_TABS = (
    ("fx", "1 · Tipos de cambio"),
    ("targets", "2 · Metas (USD)"),
    ("results", "3 · Resultados"),
    ("requirements", "4 · Requerimientos"),
    ("imports", "Registros importados"),
    ("aliases", "Alias UNE"),
    ("notes", "Notas del período"),
)

CRITICAL_ENTITY_TYPES = {
    AdminManualEditLog.ENTITY_RESULT,
    AdminManualEditLog.ENTITY_REQUIREMENT,
}


def _period_note_key(year: int, month: int) -> str:
    return f"admin.period_note.{year}.{month:02d}"


def _get_plan(year: int) -> PGCPlan | None:
    return PGCPlan.objects.filter(year=year).first()


def log_manual_edit(
    *,
    user,
    year: int,
    month: int,
    entity_type: str,
    entity_id: int | None,
    field_name: str,
    old_value,
    new_value,
    reason: str = "",
) -> AdminManualEditLog:
    return AdminManualEditLog.objects.create(
        year=year,
        month=month,
        entity_type=entity_type,
        entity_id=entity_id,
        field_name=field_name,
        old_value=format_value(old_value),
        new_value=format_value(new_value),
        reason=reason or "",
        edited_by=user,
    )


def _metrics() -> list[MetricDefinition]:
    return list(MetricDefinition.objects.filter(code__in=[
        MetricDefinition.CODE_INGRESOS,
        MetricDefinition.CODE_CLIENTES_NUEVOS,
        MetricDefinition.CODE_VENTA_CRUZADA,
        MetricDefinition.CODE_RESPUESTA_REQS,
    ]).order_by("code"))


def _unes() -> list[UNE]:
    return list(UNE.objects.filter(is_active=True).order_by("sort_order", "code"))


def get_pending_alias_values(year: int, month: int, month_from: int | None = None) -> list[str]:
    known = {a.raw_value.strip().upper() for a in UNEAlias.objects.filter(is_active=True)}
    pending: set[str] = set()
    mf = month_from or month

    for raw in (
        NewClientImportRow.objects.filter(year=year, month__gte=mf, month__lte=month)
        .exclude(raw_une_value="")
        .values_list("raw_une_value", flat=True)
    ):
        key = (raw or "").strip().upper()
        if key and key not in known:
            pending.add(raw.strip())

    for raw_dest, raw_orig in CrossSaleImportRow.objects.filter(
        year=year, month__gte=mf, month__lte=month
    ).values_list("raw_une_destination", "raw_une_origin"):
        for raw in (raw_dest, raw_orig):
            key = (raw or "").strip().upper()
            if key and key not in known:
                pending.add(raw.strip())

    return sorted(pending, key=str.upper)


def get_manual_edit_context(year: int, month: int, tab: str, month_from: int | None = None) -> dict[str, Any]:
    plan = _get_plan(year)
    metrics = _metrics()
    unes = _unes()
    mf = month_from or month
    is_range = mf != month

    targets_map = {}
    results_map = {}
    if plan:
        for t in MonthlyTarget.objects.filter(plan=plan, year=year, month=month).select_related("une", "metric"):
            targets_map[(t.une_id, t.metric_id)] = t
        for r in MonthlyMetricResult.objects.filter(plan=plan, year=year, month=month).select_related("une", "metric"):
            results_map[(r.une_id, r.metric_id)] = r

    target_rows = []
    for une in unes:
        cells = []
        for metric in metrics:
            obj = targets_map.get((une.id, metric.id))
            cells.append({"metric": metric, "obj": obj, "value": getattr(obj, "target_value", None)})
        target_rows.append({"une": une, "cells": cells})

    fx = MonthlyExchangeRate.objects.filter(year=year, month=month).first()
    has_fx = fx is not None and fx.usd_to_gtq not in (None, Decimal("0"), 0)

    fx_by_month = {
        r.month: r
        for r in MonthlyExchangeRate.objects.filter(year=year, month__gte=mf, month__lte=month)
    }
    fx_rows = []
    for m in range(mf, month + 1):
        rate_obj = fx_by_month.get(m)
        fx_rows.append({
            "month": m,
            "label": f"{year}-{m:02d}",
            "obj": rate_obj,
            "value": rate_obj.usd_to_gtq if rate_obj else None,
            "is_focus": m == month,
            "missing": rate_obj is None or rate_obj.usd_to_gtq in (None, Decimal("0"), 0),
        })
    missing_fx_months = [row["label"] for row in fx_rows if row["missing"]]

    result_rows = []
    ingresos_code = MetricDefinition.CODE_INGRESOS
    for une in unes:
        cells = []
        for metric in metrics:
            obj = results_map.get((une.id, metric.id))
            is_ingresos = metric.code == ingresos_code
            source_gtq = None
            measured_usd = getattr(obj, "measured_value", None) if obj else None
            input_currency = "GTQ"
            if obj and is_ingresos and obj.source_currency == MonthlyMetricResult.CURRENCY_GTQ:
                source_gtq = obj.source_value
                input_currency = "GTQ"
                input_value = source_gtq
            elif obj and is_ingresos and obj.source_currency == MonthlyMetricResult.CURRENCY_USD:
                input_currency = "USD"
                input_value = measured_usd
            elif is_ingresos and obj and measured_usd is not None and not obj.source_currency:
                # Legado: measured_value ya era USD canónico.
                input_currency = "USD"
                input_value = measured_usd
            elif is_ingresos:
                input_currency = "GTQ"
                input_value = None
            else:
                input_value = measured_usd
            cells.append({
                "metric": metric,
                "obj": obj,
                "value": input_value,
                "is_ingresos": is_ingresos,
                "input_currency": input_currency,
                "source_gtq": source_gtq,
                "measured_usd": measured_usd,
                "measured_usd_display": format_usd_3(measured_usd) if is_ingresos else None,
                "fx_used": getattr(obj, "exchange_rate_used", None) if obj else None,
                "conversion_status": getattr(obj, "conversion_status", "") if obj else "",
                "input_disabled": is_ingresos and input_currency == "GTQ" and not has_fx,
            })
        result_rows.append({"une": une, "cells": cells})

    requirements = []
    req_map = {}
    if plan:
        req_map = {
            r.une_id: r
            for r in ManualRequirementsCompliance.objects.filter(plan=plan, year=year, month=month)
        }
    for une in unes:
        requirements.append({"une": une, "obj": req_map.get(une.id)})

    aliases = list(UNEAlias.objects.select_related("une").filter(is_active=True).order_by("raw_value")[:200])
    pending_aliases = get_pending_alias_values(year, month, month_from=mf)

    import_limit = 400 if is_range else 100
    new_client_rows = list(
        NewClientImportRow.objects.filter(year=year, month__gte=mf, month__lte=month)
        .select_related("une", "currency")
        .order_by("year", "month", "une__sort_order", "client_name")[:import_limit]
    )
    cross_sale_rows = list(
        CrossSaleImportRow.objects.filter(year=year, month__gte=mf, month__lte=month)
        .select_related("une_destination", "une_origin", "currency")
        .order_by("year", "month", "client_name")[:import_limit]
    )

    note_setting = SystemSetting.objects.filter(key=_period_note_key(year, month)).first()
    period_note = (note_setting.value_text or "") if note_setting else ""

    recent_edits = list(
        AdminManualEditLog.objects.filter(year=year, month__gte=mf, month__lte=month)
        .select_related("edited_by")
        .order_by("-created_at")[:15]
    )

    valid_tabs = {t[0] for t in MANUAL_TABS}
    if tab not in valid_tabs:
        tab = "targets"

    # FX aprovecha el rango completo; metas/resultados/reqs siguen enfocados en month_to.
    range_capable_tabs = {"imports", "aliases", "fx"}
    tab_uses_range = tab in range_capable_tabs

    return {
        "year": year,
        "month": month,
        "month_from": mf,
        "label": (
            f"{year}-{mf:02d} → {year}-{month:02d}" if is_range else f"{year}-{month:02d}"
        ),
        "focus_label": f"{year}-{month:02d}",
        "plan": plan,
        "tab_uses_range": tab_uses_range,
        "supports_month_range": tab_uses_range,
        "single_month_ops": not tab_uses_range,
        "tab": tab,
        "tabs": MANUAL_TABS,
        "metrics": metrics,
        "unes": unes,
        "target_rows": target_rows,
        "result_rows": result_rows,
        "requirements": requirements,
        "fx": fx,
        "fx_rows": fx_rows,
        "missing_fx_months": missing_fx_months,
        "has_fx": has_fx,
        "fx_rate": fx.usd_to_gtq if fx else None,
        "stale_ingresos_count": count_stale_ingresos(year, month),
        "aliases": aliases,
        "pending_aliases": pending_aliases,
        "new_client_rows": new_client_rows,
        "cross_sale_rows": cross_sale_rows,
        "period_note": period_note,
        "recent_edits": recent_edits,
    }


@transaction.atomic
def save_targets(user, year: int, month: int, post_data, reason: str = "") -> int:
    plan = _get_plan(year)
    if not plan:
        raise ValueError("No existe plan PGC para este año.")

    changes = 0
    for une in _unes():
        for metric in _metrics():
            key = f"target_{une.id}_{metric.id}"
            raw = (post_data.get(key) or "").strip()
            if raw == "":
                continue
            parsed = parse_decimal_or_none(raw)
            if parsed is None:
                raise ValueError(f"Valor inválido en meta {une.code} / {metric.code}.")

            obj, _ = MonthlyTarget.objects.get_or_create(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
                defaults={"target_value": parsed},
            )
            old = obj.target_value
            if old != parsed:
                obj.target_value = parsed
                obj.save(update_fields=["target_value", "updated_at"])
                log_manual_edit(
                    user=user,
                    year=year,
                    month=month,
                    entity_type=AdminManualEditLog.ENTITY_TARGET,
                    entity_id=obj.id,
                    field_name="target_value",
                    old_value=old,
                    new_value=parsed,
                    reason=reason,
                )
                changes += 1
    return changes


@transaction.atomic
def save_results(user, year: int, month: int, post_data, reason: str = "") -> int:
    if not reason.strip():
        raise ValueError("Debe indicar un motivo para cambios en resultados.")

    plan = _get_plan(year)
    if not plan:
        raise ValueError("No existe plan PGC para este año.")

    fx_rate = get_fx_rate(year, month)
    changes = 0
    for une in _unes():
        for metric in _metrics():
            key = f"result_{une.id}_{metric.id}"
            raw = (post_data.get(key) or "").strip()
            if raw == "":
                continue
            parsed = parse_decimal_or_none(raw)
            if parsed is None:
                raise ValueError(f"Valor inválido en resultado {une.code} / {metric.code}.")

            is_ingresos = metric.code == MetricDefinition.CODE_INGRESOS

            if is_ingresos:
                currency = (
                    post_data.get(f"ingresos_curr_{une.id}")
                    or post_data.get(f"ingresos_curr_{une.id}_{metric.id}")
                    or "GTQ"
                ).strip().upper()
                if currency not in (
                    MonthlyMetricResult.CURRENCY_GTQ,
                    MonthlyMetricResult.CURRENCY_USD,
                ):
                    currency = MonthlyMetricResult.CURRENCY_GTQ

                if currency == MonthlyMetricResult.CURRENCY_USD:
                    usd_value = parsed
                    obj, created = MonthlyMetricResult.objects.get_or_create(
                        plan=plan,
                        une=une,
                        metric=metric,
                        year=year,
                        month=month,
                        defaults={
                            "measured_value": usd_value,
                            "source_currency": MonthlyMetricResult.CURRENCY_USD,
                            "source_value": usd_value,
                            "exchange_rate_used": None,
                            "conversion_status": MonthlyMetricResult.CONVERSION_NATIVE_USD,
                        },
                    )
                    old_usd = None if created else obj.measured_value
                    old_curr = "" if created else (obj.source_currency or "")
                    changed = (
                        created
                        or old_usd != usd_value
                        or old_curr != MonthlyMetricResult.CURRENCY_USD
                    )
                    if not changed:
                        continue

                    obj.measured_value = usd_value
                    obj.source_currency = MonthlyMetricResult.CURRENCY_USD
                    obj.source_value = usd_value
                    obj.exchange_rate_used = None
                    obj.conversion_status = MonthlyMetricResult.CONVERSION_NATIVE_USD
                    obj.calculation_note = (
                        f"Captura manual USD nativo: {usd_value} USD [{year}-{month:02d}]"
                    )
                    obj.save(
                        update_fields=[
                            "measured_value",
                            "source_currency",
                            "source_value",
                            "exchange_rate_used",
                            "conversion_status",
                            "calculation_note",
                            "updated_at",
                        ]
                    )
                    log_manual_edit(
                        user=user,
                        year=year,
                        month=month,
                        entity_type=AdminManualEditLog.ENTITY_RESULT,
                        entity_id=obj.id,
                        field_name="ingresos_usd_native",
                        old_value=f"USD={old_usd}; curr={old_curr}",
                        new_value=f"USD={usd_value}",
                        reason=reason,
                    )
                    changes += 1
                    continue

                # Manual INGRESOS: capture GTQ, convert to canonical USD.
                if fx_rate is None:
                    raise ValueError(
                        f"Falta tipo de cambio para {year}-{month:02d}. "
                        f"No se pueden guardar ingresos (GTQ) de {une.name_es} sin TC. "
                        "Vaya a la pestaña «Tipos de cambio»."
                    )
                usd_value = gtq_to_usd(parsed, fx_rate)
                obj, created = MonthlyMetricResult.objects.get_or_create(
                    plan=plan,
                    une=une,
                    metric=metric,
                    year=year,
                    month=month,
                    defaults={
                        "measured_value": usd_value,
                        "source_currency": MonthlyMetricResult.CURRENCY_GTQ,
                        "source_value": parsed,
                        "exchange_rate_used": fx_rate,
                        "conversion_status": MonthlyMetricResult.CONVERSION_CONVERTED,
                    },
                )
                old_usd = None if created else obj.measured_value
                old_gtq = None if created else obj.source_value
                changed = (
                    created
                    or old_usd != usd_value
                    or old_gtq != parsed
                    or obj.source_currency != MonthlyMetricResult.CURRENCY_GTQ
                    or obj.exchange_rate_used != fx_rate
                )
                if not changed:
                    continue

                obj.measured_value = usd_value
                obj.source_currency = MonthlyMetricResult.CURRENCY_GTQ
                obj.source_value = parsed
                obj.exchange_rate_used = fx_rate
                obj.conversion_status = MonthlyMetricResult.CONVERSION_CONVERTED
                obj.calculation_note = (
                    f"Captura manual GTQ→USD: {parsed} GTQ / {fx_rate} = {usd_value} USD "
                    f"[{year}-{month:02d}]"
                )
                obj.save(
                    update_fields=[
                        "measured_value",
                        "source_currency",
                        "source_value",
                        "exchange_rate_used",
                        "conversion_status",
                        "calculation_note",
                        "updated_at",
                    ]
                )
                log_manual_edit(
                    user=user,
                    year=year,
                    month=month,
                    entity_type=AdminManualEditLog.ENTITY_RESULT,
                    entity_id=obj.id,
                    field_name="ingresos_gtq_to_usd",
                    old_value=f"GTQ={old_gtq}; USD={old_usd}",
                    new_value=f"GTQ={parsed}; FX={fx_rate}; USD={usd_value}",
                    reason=reason,
                )
                changes += 1
                continue

            # Non-INGRESOS metrics: keep legacy USD/native numeric semantics.
            obj, created = MonthlyMetricResult.objects.get_or_create(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
                defaults={
                    "measured_value": parsed,
                    "source_currency": "",
                    "conversion_status": MonthlyMetricResult.CONVERSION_NATIVE_USD,
                },
            )
            old = None if created else obj.measured_value
            if created or old != parsed:
                obj.measured_value = parsed
                obj.calculation_note = (obj.calculation_note or "") + " [Edición manual]"
                obj.save(update_fields=["measured_value", "calculation_note", "updated_at"])
                log_manual_edit(
                    user=user,
                    year=year,
                    month=month,
                    entity_type=AdminManualEditLog.ENTITY_RESULT,
                    entity_id=obj.id,
                    field_name="measured_value",
                    old_value=old,
                    new_value=parsed,
                    reason=reason,
                )
                changes += 1
    return changes


@transaction.atomic
def save_fx(user, year: int, month: int, post_data, reason: str = "", month_from: int | None = None) -> int:
    """Save FX for focus month and/or every month in [month_from, month].

    Accepts either:
    - ``fx_value`` for a single month (focus ``month``), or
    - ``fx_value_<m>`` for each month in the selected range.
    """
    mf = month_from or month
    if mf > month:
        mf = month

    entries: list[tuple[int, str]] = []
    saw_range_keys = False
    for m in range(mf, month + 1):
        key = f"fx_value_{m}"
        if key in post_data:
            saw_range_keys = True
            entries.append((m, (post_data.get(key) or "").strip()))
    if not saw_range_keys:
        entries = [(month, (post_data.get("fx_value") or "").strip())]

    changes = 0
    for m, raw in entries:
        if raw == "":
            continue
        parsed = parse_decimal_or_none(raw)
        if parsed is None:
            raise ValueError(f"Tipo de cambio inválido para {year}-{m:02d}.")

        obj, created = MonthlyExchangeRate.objects.get_or_create(
            year=year,
            month=m,
            defaults={"usd_to_gtq": parsed},
        )
        old = None if created else obj.usd_to_gtq
        if created or old != parsed:
            obj.usd_to_gtq = parsed
            obj.save(update_fields=["usd_to_gtq"])
            log_manual_edit(
                user=user,
                year=year,
                month=m,
                entity_type=AdminManualEditLog.ENTITY_FX,
                entity_id=obj.id,
                field_name="usd_to_gtq",
                old_value=old,
                new_value=parsed,
                reason=reason,
            )
            # Do not silently recalc incomes; mark convertible GTQ rows as stale.
            if not created and old != parsed:
                mark_ingresos_stale_for_fx_change(
                    year=year,
                    month=m,
                    old_fx=old,
                    new_fx=parsed,
                    user=user,
                    reason=reason,
                )
            changes += 1
    return changes


@transaction.atomic
def save_requirements(user, year: int, month: int, post_data, reason: str = "") -> int:
    plan = _get_plan(year)
    if not plan:
        raise ValueError("No existe plan PGC para este año.")

    changes = 0
    for une in _unes():
        compliant_key = f"req_compliant_{une.id}"
        note_key = f"req_note_{une.id}"
        is_compliant = post_data.get(compliant_key) == "1"
        incident_note = (post_data.get(note_key) or "").strip()

        if not is_compliant and not incident_note and not reason.strip():
            raise ValueError(f"Indique motivo o nota de incidencia para {une.name_es}.")

        obj, created = ManualRequirementsCompliance.objects.get_or_create(
            plan=plan,
            une=une,
            year=year,
            month=month,
            defaults={"is_compliant": is_compliant, "incident_note": incident_note},
        )
        old_compliant = None if created else obj.is_compliant
        old_note = "" if created else obj.incident_note

        changed = False
        if obj.is_compliant != is_compliant:
            obj.is_compliant = is_compliant
            changed = True
        if obj.incident_note != incident_note:
            obj.incident_note = incident_note
            changed = True

        if changed:
            obj.save(update_fields=["is_compliant", "incident_note", "updated_at"])
            log_manual_edit(
                user=user,
                year=year,
                month=month,
                entity_type=AdminManualEditLog.ENTITY_REQUIREMENT,
                entity_id=obj.id,
                field_name="is_compliant/incident_note",
                old_value=f"compliant={old_compliant}; note={old_note}",
                new_value=f"compliant={is_compliant}; note={incident_note}",
                reason=reason or incident_note,
            )
            changes += 1
    return changes


@transaction.atomic
def save_alias(user, year: int, month: int, post_data, reason: str = "") -> int:
    raw_value = (post_data.get("alias_raw") or "").strip()
    une_id = post_data.get("alias_une")
    if not raw_value or not une_id:
        raise ValueError("Debe indicar valor crudo y UNE destino.")

    une = UNE.objects.filter(id=une_id).first()
    if not une:
        raise ValueError("UNE no válida.")

    # Investment en el valor crudo siempre apunta a Inversiones.
    raw_lower = raw_value.lower()
    if any(
        token in raw_lower
        for token in (
            "investment",
            "investments",
            "invest",
            "inversiones",
            "inversion",
            "inversión",
        )
    ):
        investment = UNE.objects.filter(code=UNE.CODE_INVESTMENT).first()
        if investment:
            une = investment

    obj, created = UNEAlias.objects.get_or_create(
        raw_value=raw_value,
        defaults={"une": une, "is_active": True},
    )
    old_une = None if created else obj.une_id
    if not created and (obj.une_id != une.id or not obj.is_active):
        obj.une = une
        obj.is_active = True
        obj.save(update_fields=["une", "is_active", "updated_at"])
        log_manual_edit(
            user=user,
            year=year,
            month=month,
            entity_type=AdminManualEditLog.ENTITY_ALIAS,
            entity_id=obj.id,
            field_name="une",
            old_value=old_une,
            new_value=une.id,
            reason=reason or f"Mapeo {raw_value} -> {une.code}",
        )
        return 1

    if created:
        log_manual_edit(
            user=user,
            year=year,
            month=month,
            entity_type=AdminManualEditLog.ENTITY_ALIAS,
            entity_id=obj.id,
            field_name="raw_value",
            old_value="",
            new_value=raw_value,
            reason=reason or f"Nuevo alias -> {une.code}",
        )
        return 1
    return 0


@transaction.atomic
def save_aliases_bulk(user, year: int, month: int, post_data, reason: str = "") -> int:
    """Actualiza UNE de aliases existentes desde la tabla editable."""
    changes = 0
    investment = UNE.objects.filter(code=UNE.CODE_INVESTMENT).first()
    by_id = {u.id: u for u in UNE.objects.filter(is_active=True)}

    for alias in UNEAlias.objects.filter(is_active=True):
        raw = post_data.get(f"alias_{alias.id}_une")
        if raw is None:
            continue
        try:
            une_id = int(raw)
        except (TypeError, ValueError):
            continue
        une = by_id.get(une_id)
        if not une:
            continue

        raw_lower = (alias.raw_value or "").lower()
        if investment and any(
            token in raw_lower
            for token in (
                "investment",
                "investments",
                "invest",
                "inversiones",
                "inversion",
                "inversión",
            )
        ):
            une = investment

        if alias.une_id == une.id:
            continue

        old_une = alias.une_id
        alias.une = une
        alias.save(update_fields=["une", "updated_at"])
        log_manual_edit(
            user=user,
            year=year,
            month=month,
            entity_type=AdminManualEditLog.ENTITY_ALIAS,
            entity_id=alias.id,
            field_name="une",
            old_value=old_une,
            new_value=une.id,
            reason=reason or f"Corrección alias {alias.raw_value} -> {une.code}",
        )
        changes += 1
    return changes


@transaction.atomic
def save_import_rows(
    user,
    year: int,
    month: int,
    post_data,
    reason: str = "",
    month_from: int | None = None,
) -> int:
    changes = 0
    mf = month_from or month

    for row in NewClientImportRow.objects.filter(year=year, month__gte=mf, month__lte=month):
        prefix = f"nc_{row.id}_"
        counts = post_data.get(f"{prefix}counts_as_new") == "1"
        obs = (post_data.get(f"{prefix}observations") or "").strip()
        old_counts = row.counts_as_new
        old_obs = row.observations
        if counts != old_counts or obs != old_obs:
            row.counts_as_new = counts
            row.observations = obs
            row.save(update_fields=["counts_as_new", "observations", "updated_at"])
            log_manual_edit(
                user=user,
                year=row.year,
                month=row.month,
                entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
                entity_id=row.id,
                field_name="counts_as_new/observations",
                old_value=f"counts={old_counts}; obs={old_obs}",
                new_value=f"counts={counts}; obs={obs}",
                reason=reason,
            )
            changes += 1

    for row in CrossSaleImportRow.objects.filter(year=year, month__gte=mf, month__lte=month):
        prefix = f"cs_{row.id}_"
        dest_raw = post_data.get(f"{prefix}dest")
        orig_raw = post_data.get(f"{prefix}orig")
        if dest_raw is None and orig_raw is None:
            continue
        dest = int(dest_raw) if dest_raw else None
        orig = int(orig_raw) if orig_raw else None
        old_dest = row.une_destination_id
        old_orig = row.une_origin_id
        if row.une_destination_id == dest and row.une_origin_id == orig:
            continue
        row.une_destination_id = dest
        row.une_origin_id = orig
        row.save(update_fields=["une_destination", "une_origin", "updated_at"])
        log_manual_edit(
            user=user,
            year=row.year,
            month=row.month,
            entity_type=AdminManualEditLog.ENTITY_CROSS_SALE_ROW,
            entity_id=row.id,
            field_name="une_destination/une_origin",
            old_value=f"dest={old_dest}; orig={old_orig}",
            new_value=f"dest={dest}; orig={orig}",
            reason=reason,
        )
        changes += 1

    return changes


@transaction.atomic
def save_period_note(user, year: int, month: int, post_data, reason: str = "") -> int:
    note = (post_data.get("period_note") or "").strip()
    key = _period_note_key(year, month)
    setting, created = SystemSetting.objects.get_or_create(key=key, defaults={"value_text": note})
    old = "" if created else (setting.value_text or "")
    if old != note:
        setting.value_text = note
        setting.updated_by = user
        setting.save(update_fields=["value_text", "updated_by", "updated_at"])
        log_manual_edit(
            user=user,
            year=year,
            month=month,
            entity_type=AdminManualEditLog.ENTITY_PERIOD_NOTE,
            entity_id=setting.id,
            field_name="value_text",
            old_value=old,
            new_value=note,
            reason=reason,
        )
        return 1
    return 0

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Edición manual del período con trazabilidad.
00003|"""
00004|
00005|from __future__ import annotations
00006|
00007|from decimal import Decimal
00008|from typing import Any
00009|
00010|from django.db import transaction
00011|
00012|from core.models import MetricDefinition, SystemSetting, UNE, UNEAlias
00013|from imports.models import CrossSaleImportRow, NewClientImportRow
00014|from pgc.models import (
00015|    AdminManualEditLog,
00016|    ManualRequirementsCompliance,
00017|    MonthlyExchangeRate,
00018|    MonthlyMetricResult,
00019|    MonthlyTarget,
00020|    PGCPlan,
00021|)
00022|
00023|from pgc.admin_utils import format_value, parse_decimal_or_none
00024|from pgc.income_conversion import (
00025|    count_stale_ingresos,
00026|    format_usd_3,
00027|    get_fx_rate,
00028|    gtq_to_usd,
00029|    mark_ingresos_stale_for_fx_change,
00030|)
00031|
00032|# Orden = ruta financiera sugerida (TC → metas → captura → resto).
00033|MANUAL_TABS = (
00034|    ("fx", "1 · Tipos de cambio"),
00035|    ("targets", "2 · Metas (USD)"),
00036|    ("results", "3 · Resultados"),
00037|    ("requirements", "4 · Requerimientos"),
00038|    ("imports", "Registros importados"),
00039|    ("aliases", "Alias UNE"),
00040|    ("notes", "Notas del período"),
00041|)
00042|
00043|CRITICAL_ENTITY_TYPES = {
00044|    AdminManualEditLog.ENTITY_RESULT,
00045|    AdminManualEditLog.ENTITY_REQUIREMENT,
00046|}
00047|
00048|
00049|def _period_note_key(year: int, month: int) -> str:
00050|    return f"admin.period_note.{year}.{month:02d}"
00051|
00052|
00053|def _get_plan(year: int) -> PGCPlan | None:
00054|    return PGCPlan.objects.filter(year=year).first()
00055|
00056|
00057|def log_manual_edit(
00058|    *,
00059|    user,
00060|    year: int,
00061|    month: int,
00062|    entity_type: str,
00063|    entity_id: int | None,
00064|    field_name: str,
00065|    old_value,
00066|    new_value,
00067|    reason: str = "",
00068|) -> AdminManualEditLog:
00069|    return AdminManualEditLog.objects.create(
00070|        year=year,
00071|        month=month,
00072|        entity_type=entity_type,
00073|        entity_id=entity_id,
00074|        field_name=field_name,
00075|        old_value=format_value(old_value),
00076|        new_value=format_value(new_value),
00077|        reason=reason or "",
00078|        edited_by=user,
00079|    )
00080|
00081|
00082|def _metrics() -> list[MetricDefinition]:
00083|    return list(MetricDefinition.objects.filter(code__in=[
00084|        MetricDefinition.CODE_INGRESOS,
00085|        MetricDefinition.CODE_CLIENTES_NUEVOS,
00086|        MetricDefinition.CODE_VENTA_CRUZADA,
00087|        MetricDefinition.CODE_RESPUESTA_REQS,
00088|    ]).order_by("code"))
00089|
00090|
00091|def _unes() -> list[UNE]:
00092|    return list(UNE.objects.filter(is_active=True).order_by("sort_order", "code"))
00093|
00094|
00095|def get_pending_alias_values(year: int, month: int, month_from: int | None = None) -> list[str]:
00096|    known = {a.raw_value.strip().upper() for a in UNEAlias.objects.filter(is_active=True)}
00097|    pending: set[str] = set()
00098|    mf = month_from or month
00099|
00100|    for raw in (
00101|        NewClientImportRow.objects.filter(year=year, month__gte=mf, month__lte=month)
00102|        .exclude(raw_une_value="")
00103|        .values_list("raw_une_value", flat=True)
00104|    ):
00105|        key = (raw or "").strip().upper()
00106|        if key and key not in known:
00107|            pending.add(raw.strip())
00108|
00109|    for raw_dest, raw_orig in CrossSaleImportRow.objects.filter(
00110|        year=year, month__gte=mf, month__lte=month
00111|    ).values_list("raw_une_destination", "raw_une_origin"):
00112|        for raw in (raw_dest, raw_orig):
00113|            key = (raw or "").strip().upper()
00114|            if key and key not in known:
00115|                pending.add(raw.strip())
00116|
00117|    return sorted(pending, key=str.upper)
00118|
00119|
00120|def get_manual_edit_context(year: int, month: int, tab: str, month_from: int | None = None) -> dict[str, Any]:
00121|    plan = _get_plan(year)
00122|    metrics = _metrics()
00123|    unes = _unes()
00124|    mf = month_from or month
00125|    is_range = mf != month
00126|
00127|    targets_map = {}
00128|    results_map = {}
00129|    if plan:
00130|        for t in MonthlyTarget.objects.filter(plan=plan, year=year, month=month).select_related("une", "metric"):
00131|            targets_map[(t.une_id, t.metric_id)] = t
00132|        for r in MonthlyMetricResult.objects.filter(plan=plan, year=year, month=month).select_related("une", "metric"):
00133|            results_map[(r.une_id, r.metric_id)] = r
00134|
00135|    target_rows = []
00136|    for une in unes:
00137|        cells = []
00138|        for metric in metrics:
00139|            obj = targets_map.get((une.id, metric.id))
00140|            cells.append({"metric": metric, "obj": obj, "value": getattr(obj, "target_value", None)})
00141|        target_rows.append({"une": une, "cells": cells})
00142|
00143|    fx = MonthlyExchangeRate.objects.filter(year=year, month=month).first()
00144|    has_fx = fx is not None and fx.usd_to_gtq not in (None, Decimal("0"), 0)
00145|
00146|    fx_by_month = {
00147|        r.month: r
00148|        for r in MonthlyExchangeRate.objects.filter(year=year, month__gte=mf, month__lte=month)
00149|    }
00150|    fx_rows = []
00151|    for m in range(mf, month + 1):
00152|        rate_obj = fx_by_month.get(m)
00153|        fx_rows.append({
00154|            "month": m,
00155|            "label": f"{year}-{m:02d}",
00156|            "obj": rate_obj,
00157|            "value": rate_obj.usd_to_gtq if rate_obj else None,
00158|            "is_focus": m == month,
00159|            "missing": rate_obj is None or rate_obj.usd_to_gtq in (None, Decimal("0"), 0),
00160|        })
00161|    missing_fx_months = [row["label"] for row in fx_rows if row["missing"]]
00162|
00163|    result_rows = []
00164|    ingresos_code = MetricDefinition.CODE_INGRESOS
00165|    for une in unes:
00166|        cells = []
00167|        for metric in metrics:
00168|            obj = results_map.get((une.id, metric.id))
00169|            is_ingresos = metric.code == ingresos_code
00170|            source_gtq = None
00171|            measured_usd = getattr(obj, "measured_value", None) if obj else None
00172|            input_currency = "GTQ"
00173|            if obj and is_ingresos and obj.source_currency == MonthlyMetricResult.CURRENCY_GTQ:
00174|                source_gtq = obj.source_value
00175|                input_currency = "GTQ"
00176|                input_value = source_gtq
00177|            elif obj and is_ingresos and obj.source_currency == MonthlyMetricResult.CURRENCY_USD:
00178|                input_currency = "USD"
00179|                input_value = measured_usd
00180|            elif is_ingresos and obj and measured_usd is not None and not obj.source_currency:
00181|                # Legado: measured_value ya era USD canónico.
00182|                input_currency = "USD"
00183|                input_value = measured_usd
00184|            elif is_ingresos:
00185|                input_currency = "GTQ"
00186|                input_value = None
00187|            else:
00188|                input_value = measured_usd
00189|            cells.append({
00190|                "metric": metric,
00191|                "obj": obj,
00192|                "value": input_value,
00193|                "is_ingresos": is_ingresos,
00194|                "input_currency": input_currency,
00195|                "source_gtq": source_gtq,
00196|                "measured_usd": measured_usd,
00197|                "measured_usd_display": format_usd_3(measured_usd) if is_ingresos else None,
00198|                "fx_used": getattr(obj, "exchange_rate_used", None) if obj else None,
00199|                "conversion_status": getattr(obj, "conversion_status", "") if obj else "",
00200|                "input_disabled": is_ingresos and input_currency == "GTQ" and not has_fx,
00201|            })
00202|        result_rows.append({"une": une, "cells": cells})
00203|
00204|    requirements = []
00205|    req_map = {}
00206|    if plan:
00207|        req_map = {
00208|            r.une_id: r
00209|            for r in ManualRequirementsCompliance.objects.filter(plan=plan, year=year, month=month)
00210|        }
00211|    for une in unes:
00212|        requirements.append({"une": une, "obj": req_map.get(une.id)})
00213|
00214|    aliases = list(UNEAlias.objects.select_related("une").filter(is_active=True).order_by("raw_value")[:200])
00215|    pending_aliases = get_pending_alias_values(year, month, month_from=mf)
00216|
00217|    import_limit = 400 if is_range else 100
00218|    new_client_rows = list(
00219|        NewClientImportRow.objects.filter(year=year, month__gte=mf, month__lte=month)
00220|        .select_related("une", "currency")
00221|        .order_by("year", "month", "une__sort_order", "client_name")[:import_limit]
00222|    )
00223|    cross_sale_rows = list(
00224|        CrossSaleImportRow.objects.filter(year=year, month__gte=mf, month__lte=month)
00225|        .select_related("une_destination", "une_origin", "currency")
00226|        .order_by("year", "month", "client_name")[:import_limit]
00227|    )
00228|
00229|    note_setting = SystemSetting.objects.filter(key=_period_note_key(year, month)).first()
00230|    period_note = (note_setting.value_text or "") if note_setting else ""
00231|
00232|    recent_edits = list(
00233|        AdminManualEditLog.objects.filter(year=year, month__gte=mf, month__lte=month)
00234|        .select_related("edited_by")
00235|        .order_by("-created_at")[:15]
00236|    )
00237|
00238|    valid_tabs = {t[0] for t in MANUAL_TABS}
00239|    if tab not in valid_tabs:
00240|        tab = "targets"
00241|
00242|    # FX aprovecha el rango completo; metas/resultados/reqs siguen enfocados en month_to.
00243|    range_capable_tabs = {"imports", "aliases", "fx"}
00244|    tab_uses_range = tab in range_capable_tabs
00245|
00246|    return {
00247|        "year": year,
00248|        "month": month,
00249|        "month_from": mf,
00250|        "label": (
00251|            f"{year}-{mf:02d} → {year}-{month:02d}" if is_range else f"{year}-{month:02d}"
00252|        ),
00253|        "focus_label": f"{year}-{month:02d}",
00254|        "plan": plan,
00255|        "tab_uses_range": tab_uses_range,
00256|        "supports_month_range": tab_uses_range,
00257|        "single_month_ops": not tab_uses_range,
00258|        "tab": tab,
00259|        "tabs": MANUAL_TABS,
00260|        "metrics": metrics,
00261|        "unes": unes,
00262|        "target_rows": target_rows,
00263|        "result_rows": result_rows,
00264|        "requirements": requirements,
00265|        "fx": fx,
00266|        "fx_rows": fx_rows,
00267|        "missing_fx_months": missing_fx_months,
00268|        "has_fx": has_fx,
00269|        "fx_rate": fx.usd_to_gtq if fx else None,
00270|        "stale_ingresos_count": count_stale_ingresos(year, month),
00271|        "aliases": aliases,
00272|        "pending_aliases": pending_aliases,
00273|        "new_client_rows": new_client_rows,
00274|        "cross_sale_rows": cross_sale_rows,
00275|        "period_note": period_note,
00276|        "recent_edits": recent_edits,
00277|    }
00278|
00279|
00280|@transaction.atomic
00281|def save_targets(user, year: int, month: int, post_data, reason: str = "") -> int:
00282|    plan = _get_plan(year)
00283|    if not plan:
00284|        raise ValueError("No existe plan PGC para este año.")
00285|
00286|    changes = 0
00287|    for une in _unes():
00288|        for metric in _metrics():
00289|            key = f"target_{une.id}_{metric.id}"
00290|            raw = (post_data.get(key) or "").strip()
00291|            if raw == "":
00292|                continue
00293|            parsed = parse_decimal_or_none(raw)
00294|            if parsed is None:
00295|                raise ValueError(f"Valor inválido en meta {une.code} / {metric.code}.")
00296|
00297|            obj, _ = MonthlyTarget.objects.get_or_create(
00298|                plan=plan,
00299|                une=une,
00300|                metric=metric,
00301|                year=year,
00302|                month=month,
00303|                defaults={"target_value": parsed},
00304|            )
00305|            old = obj.target_value
00306|            if old != parsed:
00307|                obj.target_value = parsed
00308|                obj.save(update_fields=["target_value", "updated_at"])
00309|                log_manual_edit(
00310|                    user=user,
00311|                    year=year,
00312|                    month=month,
00313|                    entity_type=AdminManualEditLog.ENTITY_TARGET,
00314|                    entity_id=obj.id,
00315|                    field_name="target_value",
00316|                    old_value=old,
00317|                    new_value=parsed,
00318|                    reason=reason,
00319|                )
00320|                changes += 1
00321|    return changes
00322|
00323|
00324|@transaction.atomic
00325|def save_results(user, year: int, month: int, post_data, reason: str = "") -> int:
00326|    if not reason.strip():
00327|        raise ValueError("Debe indicar un motivo para cambios en resultados.")
00328|
00329|    plan = _get_plan(year)
00330|    if not plan:
00331|        raise ValueError("No existe plan PGC para este año.")
00332|
00333|    fx_rate = get_fx_rate(year, month)
00334|    changes = 0
00335|    for une in _unes():
00336|        for metric in _metrics():
00337|            key = f"result_{une.id}_{metric.id}"
00338|            raw = (post_data.get(key) or "").strip()
00339|            if raw == "":
00340|                continue
00341|            parsed = parse_decimal_or_none(raw)
00342|            if parsed is None:
00343|                raise ValueError(f"Valor inválido en resultado {une.code} / {metric.code}.")
00344|
00345|            is_ingresos = metric.code == MetricDefinition.CODE_INGRESOS
00346|
00347|            if is_ingresos:
00348|                currency = (
00349|                    post_data.get(f"ingresos_curr_{une.id}")
00350|                    or post_data.get(f"ingresos_curr_{une.id}_{metric.id}")
00351|                    or "GTQ"
00352|                ).strip().upper()
00353|                if currency not in (
00354|                    MonthlyMetricResult.CURRENCY_GTQ,
00355|                    MonthlyMetricResult.CURRENCY_USD,
00356|                ):
00357|                    currency = MonthlyMetricResult.CURRENCY_GTQ
00358|
00359|                if currency == MonthlyMetricResult.CURRENCY_USD:
00360|                    usd_value = parsed
00361|                    obj, created = MonthlyMetricResult.objects.get_or_create(
00362|                        plan=plan,
00363|                        une=une,
00364|                        metric=metric,
00365|                        year=year,
00366|                        month=month,
00367|                        defaults={
00368|                            "measured_value": usd_value,
00369|                            "source_currency": MonthlyMetricResult.CURRENCY_USD,
00370|                            "source_value": usd_value,
00371|                            "exchange_rate_used": None,
00372|                            "conversion_status": MonthlyMetricResult.CONVERSION_NATIVE_USD,
00373|                        },
00374|                    )
00375|                    old_usd = None if created else obj.measured_value
00376|                    old_curr = "" if created else (obj.source_currency or "")
00377|                    changed = (
00378|                        created
00379|                        or old_usd != usd_value
00380|                        or old_curr != MonthlyMetricResult.CURRENCY_USD
00381|                    )
00382|                    if not changed:
00383|                        continue
00384|
00385|                    obj.measured_value = usd_value
00386|                    obj.source_currency = MonthlyMetricResult.CURRENCY_USD
00387|                    obj.source_value = usd_value
00388|                    obj.exchange_rate_used = None
00389|                    obj.conversion_status = MonthlyMetricResult.CONVERSION_NATIVE_USD
00390|                    obj.calculation_note = (
00391|                        f"Captura manual USD nativo: {usd_value} USD [{year}-{month:02d}]"
00392|                    )
00393|                    obj.save(
00394|                        update_fields=[
00395|                            "measured_value",
00396|                            "source_currency",
00397|                            "source_value",
00398|                            "exchange_rate_used",
00399|                            "conversion_status",
00400|                            "calculation_note",
00401|                            "updated_at",
00402|                        ]
00403|                    )
00404|                    log_manual_edit(
00405|                        user=user,
00406|                        year=year,
00407|                        month=month,
00408|                        entity_type=AdminManualEditLog.ENTITY_RESULT,
00409|                        entity_id=obj.id,
00410|                        field_name="ingresos_usd_native",
00411|                        old_value=f"USD={old_usd}; curr={old_curr}",
00412|                        new_value=f"USD={usd_value}",
00413|                        reason=reason,
00414|                    )
00415|                    changes += 1
00416|                    continue
00417|
00418|                # Manual INGRESOS: capture GTQ, convert to canonical USD.
00419|                if fx_rate is None:
00420|                    raise ValueError(
00421|                        f"Falta tipo de cambio para {year}-{month:02d}. "
00422|                        f"No se pueden guardar ingresos (GTQ) de {une.name_es} sin TC. "
00423|                        "Vaya a la pestaña «Tipos de cambio»."
00424|                    )
00425|                usd_value = gtq_to_usd(parsed, fx_rate)
00426|                obj, created = MonthlyMetricResult.objects.get_or_create(
00427|                    plan=plan,
00428|                    une=une,
00429|                    metric=metric,
00430|                    year=year,
00431|                    month=month,
00432|                    defaults={
00433|                        "measured_value": usd_value,
00434|                        "source_currency": MonthlyMetricResult.CURRENCY_GTQ,
00435|                        "source_value": parsed,
00436|                        "exchange_rate_used": fx_rate,
00437|                        "conversion_status": MonthlyMetricResult.CONVERSION_CONVERTED,
00438|                    },
00439|                )
00440|                old_usd = None if created else obj.measured_value
00441|                old_gtq = None if created else obj.source_value
00442|                changed = (
00443|                    created
00444|                    or old_usd != usd_value
00445|                    or old_gtq != parsed
00446|                    or obj.source_currency != MonthlyMetricResult.CURRENCY_GTQ
00447|                    or obj.exchange_rate_used != fx_rate
00448|                )
00449|                if not changed:
00450|                    continue
00451|
00452|                obj.measured_value = usd_value
00453|                obj.source_currency = MonthlyMetricResult.CURRENCY_GTQ
00454|                obj.source_value = parsed
00455|                obj.exchange_rate_used = fx_rate
00456|                obj.conversion_status = MonthlyMetricResult.CONVERSION_CONVERTED
00457|                obj.calculation_note = (
00458|                    f"Captura manual GTQ→USD: {parsed} GTQ / {fx_rate} = {usd_value} USD "
00459|                    f"[{year}-{month:02d}]"
00460|                )
00461|                obj.save(
00462|                    update_fields=[
00463|                        "measured_value",
00464|                        "source_currency",
00465|                        "source_value",
00466|                        "exchange_rate_used",
00467|                        "conversion_status",
00468|                        "calculation_note",
00469|                        "updated_at",
00470|                    ]
00471|                )
00472|                log_manual_edit(
00473|                    user=user,
00474|                    year=year,
00475|                    month=month,
00476|                    entity_type=AdminManualEditLog.ENTITY_RESULT,
00477|                    entity_id=obj.id,
00478|                    field_name="ingresos_gtq_to_usd",
00479|                    old_value=f"GTQ={old_gtq}; USD={old_usd}",
00480|                    new_value=f"GTQ={parsed}; FX={fx_rate}; USD={usd_value}",
00481|                    reason=reason,
00482|                )
00483|                changes += 1
00484|                continue
00485|
00486|            # Non-INGRESOS metrics: keep legacy USD/native numeric semantics.
00487|            obj, created = MonthlyMetricResult.objects.get_or_create(
00488|                plan=plan,
00489|                une=une,
00490|                metric=metric,
00491|                year=year,
00492|                month=month,
00493|                defaults={
00494|                    "measured_value": parsed,
00495|                    "source_currency": "",
00496|                    "conversion_status": MonthlyMetricResult.CONVERSION_NATIVE_USD,
00497|                },
00498|            )
00499|            old = None if created else obj.measured_value
00500|            if created or old != parsed:
00501|                obj.measured_value = parsed
00502|                obj.calculation_note = (obj.calculation_note or "") + " [Edición manual]"
00503|                obj.save(update_fields=["measured_value", "calculation_note", "updated_at"])
00504|                log_manual_edit(
00505|                    user=user,
00506|                    year=year,
00507|                    month=month,
00508|                    entity_type=AdminManualEditLog.ENTITY_RESULT,
00509|                    entity_id=obj.id,
00510|                    field_name="measured_value",
00511|                    old_value=old,
00512|                    new_value=parsed,
00513|                    reason=reason,
00514|                )
00515|                changes += 1
00516|    return changes
00517|
00518|
00519|@transaction.atomic
00520|def save_fx(user, year: int, month: int, post_data, reason: str = "", month_from: int | None = None) -> int:
00521|    """Save FX for focus month and/or every month in [month_from, month].
00522|
00523|    Accepts either:
00524|    - ``fx_value`` for a single month (focus ``month``), or
00525|    - ``fx_value_<m>`` for each month in the selected range.
00526|    """
00527|    mf = month_from or month
00528|    if mf > month:
00529|        mf = month
00530|
00531|    entries: list[tuple[int, str]] = []
00532|    saw_range_keys = False
00533|    for m in range(mf, month + 1):
00534|        key = f"fx_value_{m}"
00535|        if key in post_data:
00536|            saw_range_keys = True
00537|            entries.append((m, (post_data.get(key) or "").strip()))
00538|    if not saw_range_keys:
00539|        entries = [(month, (post_data.get("fx_value") or "").strip())]
00540|
00541|    changes = 0
00542|    for m, raw in entries:
00543|        if raw == "":
00544|            continue
00545|        parsed = parse_decimal_or_none(raw)
00546|        if parsed is None:
00547|            raise ValueError(f"Tipo de cambio inválido para {year}-{m:02d}.")
00548|
00549|        obj, created = MonthlyExchangeRate.objects.get_or_create(
00550|            year=year,
00551|            month=m,
00552|            defaults={"usd_to_gtq": parsed},
00553|        )
00554|        old = None if created else obj.usd_to_gtq
00555|        if created or old != parsed:
00556|            obj.usd_to_gtq = parsed
00557|            obj.save(update_fields=["usd_to_gtq"])
00558|            log_manual_edit(
00559|                user=user,
00560|                year=year,
00561|                month=m,
00562|                entity_type=AdminManualEditLog.ENTITY_FX,
00563|                entity_id=obj.id,
00564|                field_name="usd_to_gtq",
00565|                old_value=old,
00566|                new_value=parsed,
00567|                reason=reason,
00568|            )
00569|            # Do not silently recalc incomes; mark convertible GTQ rows as stale.
00570|            if not created and old != parsed:
00571|                mark_ingresos_stale_for_fx_change(
00572|                    year=year,
00573|                    month=m,
00574|                    old_fx=old,
00575|                    new_fx=parsed,
00576|                    user=user,
00577|                    reason=reason,
00578|                )
00579|            changes += 1
00580|    return changes
00581|
00582|
00583|@transaction.atomic
00584|def save_requirements(user, year: int, month: int, post_data, reason: str = "") -> int:
00585|    plan = _get_plan(year)
00586|    if not plan:
00587|        raise ValueError("No existe plan PGC para este año.")
00588|
00589|    changes = 0
00590|    for une in _unes():
00591|        compliant_key = f"req_compliant_{une.id}"
00592|        note_key = f"req_note_{une.id}"
00593|        is_compliant = post_data.get(compliant_key) == "1"
00594|        incident_note = (post_data.get(note_key) or "").strip()
00595|
00596|        if not is_compliant and not incident_note and not reason.strip():
00597|            raise ValueError(f"Indique motivo o nota de incidencia para {une.name_es}.")
00598|
00599|        obj, created = ManualRequirementsCompliance.objects.get_or_create(
00600|            plan=plan,
00601|            une=une,
00602|            year=year,
00603|            month=month,
00604|            defaults={"is_compliant": is_compliant, "incident_note": incident_note},
00605|        )
00606|        old_compliant = None if created else obj.is_compliant
00607|        old_note = "" if created else obj.incident_note
00608|
00609|        changed = False
00610|        if obj.is_compliant != is_compliant:
00611|            obj.is_compliant = is_compliant
00612|            changed = True
00613|        if obj.incident_note != incident_note:
00614|            obj.incident_note = incident_note
00615|            changed = True
00616|
00617|        if changed:
00618|            obj.save(update_fields=["is_compliant", "incident_note", "updated_at"])
00619|            log_manual_edit(
00620|                user=user,
00621|                year=year,
00622|                month=month,
00623|                entity_type=AdminManualEditLog.ENTITY_REQUIREMENT,
00624|                entity_id=obj.id,
00625|                field_name="is_compliant/incident_note",
00626|                old_value=f"compliant={old_compliant}; note={old_note}",
00627|                new_value=f"compliant={is_compliant}; note={incident_note}",
00628|                reason=reason or incident_note,
00629|            )
00630|            changes += 1
00631|    return changes
00632|
00633|
00634|@transaction.atomic
00635|def save_alias(user, year: int, month: int, post_data, reason: str = "") -> int:
00636|    raw_value = (post_data.get("alias_raw") or "").strip()
00637|    une_id = post_data.get("alias_une")
00638|    if not raw_value or not une_id:
00639|        raise ValueError("Debe indicar valor crudo y UNE destino.")
00640|
00641|    une = UNE.objects.filter(id=une_id).first()
00642|    if not une:
00643|        raise ValueError("UNE no válida.")
00644|
00645|    # Investment en el valor crudo siempre apunta a Inversiones.
00646|    raw_lower = raw_value.lower()
00647|    if any(
00648|        token in raw_lower
00649|        for token in (
00650|            "investment",
00651|            "investments",
00652|            "invest",
00653|            "inversiones",
00654|            "inversion",
00655|            "inversión",
00656|        )
00657|    ):
00658|        investment = UNE.objects.filter(code=UNE.CODE_INVESTMENT).first()
00659|        if investment:
00660|            une = investment
00661|
00662|    obj, created = UNEAlias.objects.get_or_create(
00663|        raw_value=raw_value,
00664|        defaults={"une": une, "is_active": True},
00665|    )
00666|    old_une = None if created else obj.une_id
00667|    if not created and (obj.une_id != une.id or not obj.is_active):
00668|        obj.une = une
00669|        obj.is_active = True
00670|        obj.save(update_fields=["une", "is_active", "updated_at"])
00671|        log_manual_edit(
00672|            user=user,
00673|            year=year,
00674|            month=month,
00675|            entity_type=AdminManualEditLog.ENTITY_ALIAS,
00676|            entity_id=obj.id,
00677|            field_name="une",
00678|            old_value=old_une,
00679|            new_value=une.id,
00680|            reason=reason or f"Mapeo {raw_value} -> {une.code}",
00681|        )
00682|        return 1
00683|
00684|    if created:
00685|        log_manual_edit(
00686|            user=user,
00687|            year=year,
00688|            month=month,
00689|            entity_type=AdminManualEditLog.ENTITY_ALIAS,
00690|            entity_id=obj.id,
00691|            field_name="raw_value",
00692|            old_value="",
00693|            new_value=raw_value,
00694|            reason=reason or f"Nuevo alias -> {une.code}",
00695|        )
00696|        return 1
00697|    return 0
00698|
00699|
00700|@transaction.atomic
00701|def save_aliases_bulk(user, year: int, month: int, post_data, reason: str = "") -> int:
00702|    """Actualiza UNE de aliases existentes desde la tabla editable."""
00703|    changes = 0
00704|    investment = UNE.objects.filter(code=UNE.CODE_INVESTMENT).first()
00705|    by_id = {u.id: u for u in UNE.objects.filter(is_active=True)}
00706|
00707|    for alias in UNEAlias.objects.filter(is_active=True):
00708|        raw = post_data.get(f"alias_{alias.id}_une")
00709|        if raw is None:
00710|            continue
00711|        try:
00712|            une_id = int(raw)
00713|        except (TypeError, ValueError):
00714|            continue
00715|        une = by_id.get(une_id)
00716|        if not une:
00717|            continue
00718|
00719|        raw_lower = (alias.raw_value or "").lower()
00720|        if investment and any(
00721|            token in raw_lower
00722|            for token in (
00723|                "investment",
00724|                "investments",
00725|                "invest",
00726|                "inversiones",
00727|                "inversion",
00728|                "inversión",
00729|            )
00730|        ):
00731|            une = investment
00732|
00733|        if alias.une_id == une.id:
00734|            continue
00735|
00736|        old_une = alias.une_id
00737|        alias.une = une
00738|        alias.save(update_fields=["une", "updated_at"])
00739|        log_manual_edit(
00740|            user=user,
00741|            year=year,
00742|            month=month,
00743|            entity_type=AdminManualEditLog.ENTITY_ALIAS,
00744|            entity_id=alias.id,
00745|            field_name="une",
00746|            old_value=old_une,
00747|            new_value=une.id,
00748|            reason=reason or f"Corrección alias {alias.raw_value} -> {une.code}",
00749|        )
00750|        changes += 1
00751|    return changes
00752|
00753|
00754|@transaction.atomic
00755|def save_import_rows(
00756|    user,
00757|    year: int,
00758|    month: int,
00759|    post_data,
00760|    reason: str = "",
00761|    month_from: int | None = None,
00762|) -> int:
00763|    changes = 0
00764|    mf = month_from or month
00765|
00766|    for row in NewClientImportRow.objects.filter(year=year, month__gte=mf, month__lte=month):
00767|        prefix = f"nc_{row.id}_"
00768|        counts = post_data.get(f"{prefix}counts_as_new") == "1"
00769|        obs = (post_data.get(f"{prefix}observations") or "").strip()
00770|        old_counts = row.counts_as_new
00771|        old_obs = row.observations
00772|        if counts != old_counts or obs != old_obs:
00773|            row.counts_as_new = counts
00774|            row.observations = obs
00775|            row.save(update_fields=["counts_as_new", "observations", "updated_at"])
00776|            log_manual_edit(
00777|                user=user,
00778|                year=row.year,
00779|                month=row.month,
00780|                entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
00781|                entity_id=row.id,
00782|                field_name="counts_as_new/observations",
00783|                old_value=f"counts={old_counts}; obs={old_obs}",
00784|                new_value=f"counts={counts}; obs={obs}",
00785|                reason=reason,
00786|            )
00787|            changes += 1
00788|
00789|    for row in CrossSaleImportRow.objects.filter(year=year, month__gte=mf, month__lte=month):
00790|        prefix = f"cs_{row.id}_"
00791|        dest_raw = post_data.get(f"{prefix}dest")
00792|        orig_raw = post_data.get(f"{prefix}orig")
00793|        if dest_raw is None and orig_raw is None:
00794|            continue
00795|        dest = int(dest_raw) if dest_raw else None
00796|        orig = int(orig_raw) if orig_raw else None
00797|        old_dest = row.une_destination_id
00798|        old_orig = row.une_origin_id
00799|        if row.une_destination_id == dest and row.une_origin_id == orig:
00800|            continue
00801|        row.une_destination_id = dest
00802|        row.une_origin_id = orig
00803|        row.save(update_fields=["une_destination", "une_origin", "updated_at"])
00804|        log_manual_edit(
00805|            user=user,
00806|            year=row.year,
00807|            month=row.month,
00808|            entity_type=AdminManualEditLog.ENTITY_CROSS_SALE_ROW,
00809|            entity_id=row.id,
00810|            field_name="une_destination/une_origin",
00811|            old_value=f"dest={old_dest}; orig={old_orig}",
00812|            new_value=f"dest={dest}; orig={orig}",
00813|            reason=reason,
00814|        )
00815|        changes += 1
00816|
00817|    return changes
00818|
00819|
00820|@transaction.atomic
00821|def save_period_note(user, year: int, month: int, post_data, reason: str = "") -> int:
00822|    note = (post_data.get("period_note") or "").strip()
00823|    key = _period_note_key(year, month)
00824|    setting, created = SystemSetting.objects.get_or_create(key=key, defaults={"value_text": note})
00825|    old = "" if created else (setting.value_text or "")
00826|    if old != note:
00827|        setting.value_text = note
00828|        setting.updated_by = user
00829|        setting.save(update_fields=["value_text", "updated_by", "updated_at"])
00830|        log_manual_edit(
00831|            user=user,
00832|            year=year,
00833|            month=month,
00834|            entity_type=AdminManualEditLog.ENTITY_PERIOD_NOTE,
00835|            entity_id=setting.id,
00836|            field_name="value_text",
00837|            old_value=old,
00838|            new_value=note,
00839|            reason=reason,
00840|        )
00841|        return 1
00842|    return 0

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiCkVkaWNpw7NuIG1hbnVhbCBkZWwgcGVyw61vZG8gY29uIHRyYXphYmlsaWRhZC4KIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgpmcm9tIGRlY2ltYWwgaW1wb3J0IERlY2ltYWwKZnJvbSB0eXBpbmcgaW1wb3J0IEFueQoKZnJvbSBkamFuZ28uZGIgaW1wb3J0IHRyYW5zYWN0aW9uCgpmcm9tIGNvcmUubW9kZWxzIGltcG9ydCBNZXRyaWNEZWZpbml0aW9uLCBTeXN0ZW1TZXR0aW5nLCBVTkUsIFVORUFsaWFzCmZyb20gaW1wb3J0cy5tb2RlbHMgaW1wb3J0IENyb3NzU2FsZUltcG9ydFJvdywgTmV3Q2xpZW50SW1wb3J0Um93CmZyb20gcGdjLm1vZGVscyBpbXBvcnQgKAogICAgQWRtaW5NYW51YWxFZGl0TG9nLAogICAgTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZSwKICAgIE1vbnRobHlFeGNoYW5nZVJhdGUsCiAgICBNb250aGx5TWV0cmljUmVzdWx0LAogICAgTW9udGhseVRhcmdldCwKICAgIFBHQ1BsYW4sCikKCmZyb20gcGdjLmFkbWluX3V0aWxzIGltcG9ydCBmb3JtYXRfdmFsdWUsIHBhcnNlX2RlY2ltYWxfb3Jfbm9uZQpmcm9tIHBnYy5pbmNvbWVfY29udmVyc2lvbiBpbXBvcnQgKAogICAgY291bnRfc3RhbGVfaW5ncmVzb3MsCiAgICBmb3JtYXRfdXNkXzMsCiAgICBnZXRfZnhfcmF0ZSwKICAgIGd0cV90b191c2QsCiAgICBtYXJrX2luZ3Jlc29zX3N0YWxlX2Zvcl9meF9jaGFuZ2UsCikKCiMgT3JkZW4gPSBydXRhIGZpbmFuY2llcmEgc3VnZXJpZGEgKFRDIOKGkiBtZXRhcyDihpIgY2FwdHVyYSDihpIgcmVzdG8pLgpNQU5VQUxfVEFCUyA9ICgKICAgICgiZngiLCAiMSDCtyBUaXBvcyBkZSBjYW1iaW8iKSwKICAgICgidGFyZ2V0cyIsICIyIMK3IE1ldGFzIChVU0QpIiksCiAgICAoInJlc3VsdHMiLCAiMyDCtyBSZXN1bHRhZG9zIiksCiAgICAoInJlcXVpcmVtZW50cyIsICI0IMK3IFJlcXVlcmltaWVudG9zIiksCiAgICAoImltcG9ydHMiLCAiUmVnaXN0cm9zIGltcG9ydGFkb3MiKSwKICAgICgiYWxpYXNlcyIsICJBbGlhcyBVTkUiKSwKICAgICgibm90ZXMiLCAiTm90YXMgZGVsIHBlcsOtb2RvIiksCikKCkNSSVRJQ0FMX0VOVElUWV9UWVBFUyA9IHsKICAgIEFkbWluTWFudWFsRWRpdExvZy5FTlRJVFlfUkVTVUxULAogICAgQWRtaW5NYW51YWxFZGl0TG9nLkVOVElUWV9SRVFVSVJFTUVOVCwKfQoKCmRlZiBfcGVyaW9kX25vdGVfa2V5KHllYXI6IGludCwgbW9udGg6IGludCkgLT4gc3RyOgogICAgcmV0dXJuIGYiYWRtaW4ucGVyaW9kX25vdGUue3llYXJ9Lnttb250aDowMmR9IgoKCmRlZiBfZ2V0X3BsYW4oeWVhcjogaW50KSAtPiBQR0NQbGFuIHwgTm9uZToKICAgIHJldHVybiBQR0NQbGFuLm9iamVjdHMuZmlsdGVyKHllYXI9eWVhcikuZmlyc3QoKQoKCmRlZiBsb2dfbWFudWFsX2VkaXQoCiAgICAqLAogICAgdXNlciwKICAgIHllYXI6IGludCwKICAgIG1vbnRoOiBpbnQsCiAgICBlbnRpdHlfdHlwZTogc3RyLAogICAgZW50aXR5X2lkOiBpbnQgfCBOb25lLAogICAgZmllbGRfbmFtZTogc3RyLAogICAgb2xkX3ZhbHVlLAogICAgbmV3X3ZhbHVlLAogICAgcmVhc29uOiBzdHIgPSAiIiwKKSAtPiBBZG1pbk1hbnVhbEVkaXRMb2c6CiAgICByZXR1cm4gQWRtaW5NYW51YWxFZGl0TG9nLm9iamVjdHMuY3JlYXRlKAogICAgICAgIHllYXI9eWVhciwKICAgICAgICBtb250aD1tb250aCwKICAgICAgICBlbnRpdHlfdHlwZT1lbnRpdHlfdHlwZSwKICAgICAgICBlbnRpdHlfaWQ9ZW50aXR5X2lkLAogICAgICAgIGZpZWxkX25hbWU9ZmllbGRfbmFtZSwKICAgICAgICBvbGRfdmFsdWU9Zm9ybWF0X3ZhbHVlKG9sZF92YWx1ZSksCiAgICAgICAgbmV3X3ZhbHVlPWZvcm1hdF92YWx1ZShuZXdfdmFsdWUpLAogICAgICAgIHJlYXNvbj1yZWFzb24gb3IgIiIsCiAgICAgICAgZWRpdGVkX2J5PXVzZXIsCiAgICApCgoKZGVmIF9tZXRyaWNzKCkgLT4gbGlzdFtNZXRyaWNEZWZpbml0aW9uXToKICAgIHJldHVybiBsaXN0KE1ldHJpY0RlZmluaXRpb24ub2JqZWN0cy5maWx0ZXIoY29kZV9faW49WwogICAgICAgIE1ldHJpY0RlZmluaXRpb24uQ09ERV9JTkdSRVNPUywKICAgICAgICBNZXRyaWNEZWZpbml0aW9uLkNPREVfQ0xJRU5URVNfTlVFVk9TLAogICAgICAgIE1ldHJpY0RlZmluaXRpb24uQ09ERV9WRU5UQV9DUlVaQURBLAogICAgICAgIE1ldHJpY0RlZmluaXRpb24uQ09ERV9SRVNQVUVTVEFfUkVRUywKICAgIF0pLm9yZGVyX2J5KCJjb2RlIikpCgoKZGVmIF91bmVzKCkgLT4gbGlzdFtVTkVdOgogICAgcmV0dXJuIGxpc3QoVU5FLm9iamVjdHMuZmlsdGVyKGlzX2FjdGl2ZT1UcnVlKS5vcmRlcl9ieSgic29ydF9vcmRlciIsICJjb2RlIikpCgoKZGVmIGdldF9wZW5kaW5nX2FsaWFzX3ZhbHVlcyh5ZWFyOiBpbnQsIG1vbnRoOiBpbnQsIG1vbnRoX2Zyb206IGludCB8IE5vbmUgPSBOb25lKSAtPiBsaXN0W3N0cl06CiAgICBrbm93biA9IHthLnJhd192YWx1ZS5zdHJpcCgpLnVwcGVyKCkgZm9yIGEgaW4gVU5FQWxpYXMub2JqZWN0cy5maWx0ZXIoaXNfYWN0aXZlPVRydWUpfQogICAgcGVuZGluZzogc2V0W3N0cl0gPSBzZXQoKQogICAgbWYgPSBtb250aF9mcm9tIG9yIG1vbnRoCgogICAgZm9yIHJhdyBpbiAoCiAgICAgICAgTmV3Q2xpZW50SW1wb3J0Um93Lm9iamVjdHMuZmlsdGVyKHllYXI9eWVhciwgbW9udGhfX2d0ZT1tZiwgbW9udGhfX2x0ZT1tb250aCkKICAgICAgICAuZXhjbHVkZShyYXdfdW5lX3ZhbHVlPSIiKQogICAgICAgIC52YWx1ZXNfbGlzdCgicmF3X3VuZV92YWx1ZSIsIGZsYXQ9VHJ1ZSkKICAgICk6CiAgICAgICAga2V5ID0gKHJhdyBvciAiIikuc3RyaXAoKS51cHBlcigpCiAgICAgICAgaWYga2V5IGFuZCBrZXkgbm90IGluIGtub3duOgogICAgICAgICAgICBwZW5kaW5nLmFkZChyYXcuc3RyaXAoKSkKCiAgICBmb3IgcmF3X2Rlc3QsIHJhd19vcmlnIGluIENyb3NzU2FsZUltcG9ydFJvdy5vYmplY3RzLmZpbHRlcigKICAgICAgICB5ZWFyPXllYXIsIG1vbnRoX19ndGU9bWYsIG1vbnRoX19sdGU9bW9udGgKICAgICkudmFsdWVzX2xpc3QoInJhd191bmVfZGVzdGluYXRpb24iLCAicmF3X3VuZV9vcmlnaW4iKToKICAgICAgICBmb3IgcmF3IGluIChyYXdfZGVzdCwgcmF3X29yaWcpOgogICAgICAgICAgICBrZXkgPSAocmF3IG9yICIiKS5zdHJpcCgpLnVwcGVyKCkKICAgICAgICAgICAgaWYga2V5IGFuZCBrZXkgbm90IGluIGtub3duOgogICAgICAgICAgICAgICAgcGVuZGluZy5hZGQocmF3LnN0cmlwKCkpCgogICAgcmV0dXJuIHNvcnRlZChwZW5kaW5nLCBrZXk9c3RyLnVwcGVyKQoKCmRlZiBnZXRfbWFudWFsX2VkaXRfY29udGV4dCh5ZWFyOiBpbnQsIG1vbnRoOiBpbnQsIHRhYjogc3RyLCBtb250aF9mcm9tOiBpbnQgfCBOb25lID0gTm9uZSkgLT4gZGljdFtzdHIsIEFueV06CiAgICBwbGFuID0gX2dldF9wbGFuKHllYXIpCiAgICBtZXRyaWNzID0gX21ldHJpY3MoKQogICAgdW5lcyA9IF91bmVzKCkKICAgIG1mID0gbW9udGhfZnJvbSBvciBtb250aAogICAgaXNfcmFuZ2UgPSBtZiAhPSBtb250aAoKICAgIHRhcmdldHNfbWFwID0ge30KICAgIHJlc3VsdHNfbWFwID0ge30KICAgIGlmIHBsYW46CiAgICAgICAgZm9yIHQgaW4gTW9udGhseVRhcmdldC5vYmplY3RzLmZpbHRlcihwbGFuPXBsYW4sIHllYXI9eWVhciwgbW9udGg9bW9udGgpLnNlbGVjdF9yZWxhdGVkKCJ1bmUiLCAibWV0cmljIik6CiAgICAgICAgICAgIHRhcmdldHNfbWFwWyh0LnVuZV9pZCwgdC5tZXRyaWNfaWQpXSA9IHQKICAgICAgICBmb3IgciBpbiBNb250aGx5TWV0cmljUmVzdWx0Lm9iamVjdHMuZmlsdGVyKHBsYW49cGxhbiwgeWVhcj15ZWFyLCBtb250aD1tb250aCkuc2VsZWN0X3JlbGF0ZWQoInVuZSIsICJtZXRyaWMiKToKICAgICAgICAgICAgcmVzdWx0c19tYXBbKHIudW5lX2lkLCByLm1ldHJpY19pZCldID0gcgoKICAgIHRhcmdldF9yb3dzID0gW10KICAgIGZvciB1bmUgaW4gdW5lczoKICAgICAgICBjZWxscyA9IFtdCiAgICAgICAgZm9yIG1ldHJpYyBpbiBtZXRyaWNzOgogICAgICAgICAgICBvYmogPSB0YXJnZXRzX21hcC5nZXQoKHVuZS5pZCwgbWV0cmljLmlkKSkKICAgICAgICAgICAgY2VsbHMuYXBwZW5kKHsibWV0cmljIjogbWV0cmljLCAib2JqIjogb2JqLCAidmFsdWUiOiBnZXRhdHRyKG9iaiwgInRhcmdldF92YWx1ZSIsIE5vbmUpfSkKICAgICAgICB0YXJnZXRfcm93cy5hcHBlbmQoeyJ1bmUiOiB1bmUsICJjZWxscyI6IGNlbGxzfSkKCiAgICBmeCA9IE1vbnRobHlFeGNoYW5nZVJhdGUub2JqZWN0cy5maWx0ZXIoeWVhcj15ZWFyLCBtb250aD1tb250aCkuZmlyc3QoKQogICAgaGFzX2Z4ID0gZnggaXMgbm90IE5vbmUgYW5kIGZ4LnVzZF90b19ndHEgbm90IGluIChOb25lLCBEZWNpbWFsKCIwIiksIDApCgogICAgZnhfYnlfbW9udGggPSB7CiAgICAgICAgci5tb250aDogcgogICAgICAgIGZvciByIGluIE1vbnRobHlFeGNoYW5nZVJhdGUub2JqZWN0cy5maWx0ZXIoeWVhcj15ZWFyLCBtb250aF9fZ3RlPW1mLCBtb250aF9fbHRlPW1vbnRoKQogICAgfQogICAgZnhfcm93cyA9IFtdCiAgICBmb3IgbSBpbiByYW5nZShtZiwgbW9udGggKyAxKToKICAgICAgICByYXRlX29iaiA9IGZ4X2J5X21vbnRoLmdldChtKQogICAgICAgIGZ4X3Jvd3MuYXBwZW5kKHsKICAgICAgICAgICAgIm1vbnRoIjogbSwKICAgICAgICAgICAgImxhYmVsIjogZiJ7eWVhcn0te206MDJkfSIsCiAgICAgICAgICAgICJvYmoiOiByYXRlX29iaiwKICAgICAgICAgICAgInZhbHVlIjogcmF0ZV9vYmoudXNkX3RvX2d0cSBpZiByYXRlX29iaiBlbHNlIE5vbmUsCiAgICAgICAgICAgICJpc19mb2N1cyI6IG0gPT0gbW9udGgsCiAgICAgICAgICAgICJtaXNzaW5nIjogcmF0ZV9vYmogaXMgTm9uZSBvciByYXRlX29iai51c2RfdG9fZ3RxIGluIChOb25lLCBEZWNpbWFsKCIwIiksIDApLAogICAgICAgIH0pCiAgICBtaXNzaW5nX2Z4X21vbnRocyA9IFtyb3dbImxhYmVsIl0gZm9yIHJvdyBpbiBmeF9yb3dzIGlmIHJvd1sibWlzc2luZyJdXQoKICAgIHJlc3VsdF9yb3dzID0gW10KICAgIGluZ3Jlc29zX2NvZGUgPSBNZXRyaWNEZWZpbml0aW9uLkNPREVfSU5HUkVTT1MKICAgIGZvciB1bmUgaW4gdW5lczoKICAgICAgICBjZWxscyA9IFtdCiAgICAgICAgZm9yIG1ldHJpYyBpbiBtZXRyaWNzOgogICAgICAgICAgICBvYmogPSByZXN1bHRzX21hcC5nZXQoKHVuZS5pZCwgbWV0cmljLmlkKSkKICAgICAgICAgICAgaXNfaW5ncmVzb3MgPSBtZXRyaWMuY29kZSA9PSBpbmdyZXNvc19jb2RlCiAgICAgICAgICAgIHNvdXJjZV9ndHEgPSBOb25lCiAgICAgICAgICAgIG1lYXN1cmVkX3VzZCA9IGdldGF0dHIob2JqLCAibWVhc3VyZWRfdmFsdWUiLCBOb25lKSBpZiBvYmogZWxzZSBOb25lCiAgICAgICAgICAgIGlucHV0X2N1cnJlbmN5ID0gIkdUUSIKICAgICAgICAgICAgaWYgb2JqIGFuZCBpc19pbmdyZXNvcyBhbmQgb2JqLnNvdXJjZV9jdXJyZW5jeSA9PSBNb250aGx5TWV0cmljUmVzdWx0LkNVUlJFTkNZX0dUUToKICAgICAgICAgICAgICAgIHNvdXJjZV9ndHEgPSBvYmouc291cmNlX3ZhbHVlCiAgICAgICAgICAgICAgICBpbnB1dF9jdXJyZW5jeSA9ICJHVFEiCiAgICAgICAgICAgICAgICBpbnB1dF92YWx1ZSA9IHNvdXJjZV9ndHEKICAgICAgICAgICAgZWxpZiBvYmogYW5kIGlzX2luZ3Jlc29zIGFuZCBvYmouc291cmNlX2N1cnJlbmN5ID09IE1vbnRobHlNZXRyaWNSZXN1bHQuQ1VSUkVOQ1lfVVNEOgogICAgICAgICAgICAgICAgaW5wdXRfY3VycmVuY3kgPSAiVVNEIgogICAgICAgICAgICAgICAgaW5wdXRfdmFsdWUgPSBtZWFzdXJlZF91c2QKICAgICAgICAgICAgZWxpZiBpc19pbmdyZXNvcyBhbmQgb2JqIGFuZCBtZWFzdXJlZF91c2QgaXMgbm90IE5vbmUgYW5kIG5vdCBvYmouc291cmNlX2N1cnJlbmN5OgogICAgICAgICAgICAgICAgIyBMZWdhZG86IG1lYXN1cmVkX3ZhbHVlIHlhIGVyYSBVU0QgY2Fuw7NuaWNvLgogICAgICAgICAgICAgICAgaW5wdXRfY3VycmVuY3kgPSAiVVNEIgogICAgICAgICAgICAgICAgaW5wdXRfdmFsdWUgPSBtZWFzdXJlZF91c2QKICAgICAgICAgICAgZWxpZiBpc19pbmdyZXNvczoKICAgICAgICAgICAgICAgIGlucHV0X2N1cnJlbmN5ID0gIkdUUSIKICAgICAgICAgICAgICAgIGlucHV0X3ZhbHVlID0gTm9uZQogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgaW5wdXRfdmFsdWUgPSBtZWFzdXJlZF91c2QKICAgICAgICAgICAgY2VsbHMuYXBwZW5kKHsKICAgICAgICAgICAgICAgICJtZXRyaWMiOiBtZXRyaWMsCiAgICAgICAgICAgICAgICAib2JqIjogb2JqLAogICAgICAgICAgICAgICAgInZhbHVlIjogaW5wdXRfdmFsdWUsCiAgICAgICAgICAgICAgICAiaXNfaW5ncmVzb3MiOiBpc19pbmdyZXNvcywKICAgICAgICAgICAgICAgICJpbnB1dF9jdXJyZW5jeSI6IGlucHV0X2N1cnJlbmN5LAogICAgICAgICAgICAgICAgInNvdXJjZV9ndHEiOiBzb3VyY2VfZ3RxLAogICAgICAgICAgICAgICAgIm1lYXN1cmVkX3VzZCI6IG1lYXN1cmVkX3VzZCwKICAgICAgICAgICAgICAgICJtZWFzdXJlZF91c2RfZGlzcGxheSI6IGZvcm1hdF91c2RfMyhtZWFzdXJlZF91c2QpIGlmIGlzX2luZ3Jlc29zIGVsc2UgTm9uZSwKICAgICAgICAgICAgICAgICJmeF91c2VkIjogZ2V0YXR0cihvYmosICJleGNoYW5nZV9yYXRlX3VzZWQiLCBOb25lKSBpZiBvYmogZWxzZSBOb25lLAogICAgICAgICAgICAgICAgImNvbnZlcnNpb25fc3RhdHVzIjogZ2V0YXR0cihvYmosICJjb252ZXJzaW9uX3N0YXR1cyIsICIiKSBpZiBvYmogZWxzZSAiIiwKICAgICAgICAgICAgICAgICJpbnB1dF9kaXNhYmxlZCI6IGlzX2luZ3Jlc29zIGFuZCBpbnB1dF9jdXJyZW5jeSA9PSAiR1RRIiBhbmQgbm90IGhhc19meCwKICAgICAgICAgICAgfSkKICAgICAgICByZXN1bHRfcm93cy5hcHBlbmQoeyJ1bmUiOiB1bmUsICJjZWxscyI6IGNlbGxzfSkKCiAgICByZXF1aXJlbWVudHMgPSBbXQogICAgcmVxX21hcCA9IHt9CiAgICBpZiBwbGFuOgogICAgICAgIHJlcV9tYXAgPSB7CiAgICAgICAgICAgIHIudW5lX2lkOiByCiAgICAgICAgICAgIGZvciByIGluIE1hbnVhbFJlcXVpcmVtZW50c0NvbXBsaWFuY2Uub2JqZWN0cy5maWx0ZXIocGxhbj1wbGFuLCB5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKQogICAgICAgIH0KICAgIGZvciB1bmUgaW4gdW5lczoKICAgICAgICByZXF1aXJlbWVudHMuYXBwZW5kKHsidW5lIjogdW5lLCAib2JqIjogcmVxX21hcC5nZXQodW5lLmlkKX0pCgogICAgYWxpYXNlcyA9IGxpc3QoVU5FQWxpYXMub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgidW5lIikuZmlsdGVyKGlzX2FjdGl2ZT1UcnVlKS5vcmRlcl9ieSgicmF3X3ZhbHVlIilbOjIwMF0pCiAgICBwZW5kaW5nX2FsaWFzZXMgPSBnZXRfcGVuZGluZ19hbGlhc192YWx1ZXMoeWVhciwgbW9udGgsIG1vbnRoX2Zyb209bWYpCgogICAgaW1wb3J0X2xpbWl0ID0gNDAwIGlmIGlzX3JhbmdlIGVsc2UgMTAwCiAgICBuZXdfY2xpZW50X3Jvd3MgPSBsaXN0KAogICAgICAgIE5ld0NsaWVudEltcG9ydFJvdy5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIsIG1vbnRoX19ndGU9bWYsIG1vbnRoX19sdGU9bW9udGgpCiAgICAgICAgLnNlbGVjdF9yZWxhdGVkKCJ1bmUiLCAiY3VycmVuY3kiKQogICAgICAgIC5vcmRlcl9ieSgieWVhciIsICJtb250aCIsICJ1bmVfX3NvcnRfb3JkZXIiLCAiY2xpZW50X25hbWUiKVs6aW1wb3J0X2xpbWl0XQogICAgKQogICAgY3Jvc3Nfc2FsZV9yb3dzID0gbGlzdCgKICAgICAgICBDcm9zc1NhbGVJbXBvcnRSb3cub2JqZWN0cy5maWx0ZXIoeWVhcj15ZWFyLCBtb250aF9fZ3RlPW1mLCBtb250aF9fbHRlPW1vbnRoKQogICAgICAgIC5zZWxlY3RfcmVsYXRlZCgidW5lX2Rlc3RpbmF0aW9uIiwgInVuZV9vcmlnaW4iLCAiY3VycmVuY3kiKQogICAgICAgIC5vcmRlcl9ieSgieWVhciIsICJtb250aCIsICJjbGllbnRfbmFtZSIpWzppbXBvcnRfbGltaXRdCiAgICApCgogICAgbm90ZV9zZXR0aW5nID0gU3lzdGVtU2V0dGluZy5vYmplY3RzLmZpbHRlcihrZXk9X3BlcmlvZF9ub3RlX2tleSh5ZWFyLCBtb250aCkpLmZpcnN0KCkKICAgIHBlcmlvZF9ub3RlID0gKG5vdGVfc2V0dGluZy52YWx1ZV90ZXh0IG9yICIiKSBpZiBub3RlX3NldHRpbmcgZWxzZSAiIgoKICAgIHJlY2VudF9lZGl0cyA9IGxpc3QoCiAgICAgICAgQWRtaW5NYW51YWxFZGl0TG9nLm9iamVjdHMuZmlsdGVyKHllYXI9eWVhciwgbW9udGhfX2d0ZT1tZiwgbW9udGhfX2x0ZT1tb250aCkKICAgICAgICAuc2VsZWN0X3JlbGF0ZWQoImVkaXRlZF9ieSIpCiAgICAgICAgLm9yZGVyX2J5KCItY3JlYXRlZF9hdCIpWzoxNV0KICAgICkKCiAgICB2YWxpZF90YWJzID0ge3RbMF0gZm9yIHQgaW4gTUFOVUFMX1RBQlN9CiAgICBpZiB0YWIgbm90IGluIHZhbGlkX3RhYnM6CiAgICAgICAgdGFiID0gInRhcmdldHMiCgogICAgIyBGWCBhcHJvdmVjaGEgZWwgcmFuZ28gY29tcGxldG87IG1ldGFzL3Jlc3VsdGFkb3MvcmVxcyBzaWd1ZW4gZW5mb2NhZG9zIGVuIG1vbnRoX3RvLgogICAgcmFuZ2VfY2FwYWJsZV90YWJzID0geyJpbXBvcnRzIiwgImFsaWFzZXMiLCAiZngifQogICAgdGFiX3VzZXNfcmFuZ2UgPSB0YWIgaW4gcmFuZ2VfY2FwYWJsZV90YWJzCgogICAgcmV0dXJuIHsKICAgICAgICAieWVhciI6IHllYXIsCiAgICAgICAgIm1vbnRoIjogbW9udGgsCiAgICAgICAgIm1vbnRoX2Zyb20iOiBtZiwKICAgICAgICAibGFiZWwiOiAoCiAgICAgICAgICAgIGYie3llYXJ9LXttZjowMmR9IOKGkiB7eWVhcn0te21vbnRoOjAyZH0iIGlmIGlzX3JhbmdlIGVsc2UgZiJ7eWVhcn0te21vbnRoOjAyZH0iCiAgICAgICAgKSwKICAgICAgICAiZm9jdXNfbGFiZWwiOiBmInt5ZWFyfS17bW9udGg6MDJkfSIsCiAgICAgICAgInBsYW4iOiBwbGFuLAogICAgICAgICJ0YWJfdXNlc19yYW5nZSI6IHRhYl91c2VzX3JhbmdlLAogICAgICAgICJzdXBwb3J0c19tb250aF9yYW5nZSI6IHRhYl91c2VzX3JhbmdlLAogICAgICAgICJzaW5nbGVfbW9udGhfb3BzIjogbm90IHRhYl91c2VzX3JhbmdlLAogICAgICAgICJ0YWIiOiB0YWIsCiAgICAgICAgInRhYnMiOiBNQU5VQUxfVEFCUywKICAgICAgICAibWV0cmljcyI6IG1ldHJpY3MsCiAgICAgICAgInVuZXMiOiB1bmVzLAogICAgICAgICJ0YXJnZXRfcm93cyI6IHRhcmdldF9yb3dzLAogICAgICAgICJyZXN1bHRfcm93cyI6IHJlc3VsdF9yb3dzLAogICAgICAgICJyZXF1aXJlbWVudHMiOiByZXF1aXJlbWVudHMsCiAgICAgICAgImZ4IjogZngsCiAgICAgICAgImZ4X3Jvd3MiOiBmeF9yb3dzLAogICAgICAgICJtaXNzaW5nX2Z4X21vbnRocyI6IG1pc3NpbmdfZnhfbW9udGhzLAogICAgICAgICJoYXNfZngiOiBoYXNfZngsCiAgICAgICAgImZ4X3JhdGUiOiBmeC51c2RfdG9fZ3RxIGlmIGZ4IGVsc2UgTm9uZSwKICAgICAgICAic3RhbGVfaW5ncmVzb3NfY291bnQiOiBjb3VudF9zdGFsZV9pbmdyZXNvcyh5ZWFyLCBtb250aCksCiAgICAgICAgImFsaWFzZXMiOiBhbGlhc2VzLAogICAgICAgICJwZW5kaW5nX2FsaWFzZXMiOiBwZW5kaW5nX2FsaWFzZXMsCiAgICAgICAgIm5ld19jbGllbnRfcm93cyI6IG5ld19jbGllbnRfcm93cywKICAgICAgICAiY3Jvc3Nfc2FsZV9yb3dzIjogY3Jvc3Nfc2FsZV9yb3dzLAogICAgICAgICJwZXJpb2Rfbm90ZSI6IHBlcmlvZF9ub3RlLAogICAgICAgICJyZWNlbnRfZWRpdHMiOiByZWNlbnRfZWRpdHMsCiAgICB9CgoKQHRyYW5zYWN0aW9uLmF0b21pYwpkZWYgc2F2ZV90YXJnZXRzKHVzZXIsIHllYXI6IGludCwgbW9udGg6IGludCwgcG9zdF9kYXRhLCByZWFzb246IHN0ciA9ICIiKSAtPiBpbnQ6CiAgICBwbGFuID0gX2dldF9wbGFuKHllYXIpCiAgICBpZiBub3QgcGxhbjoKICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJObyBleGlzdGUgcGxhbiBQR0MgcGFyYSBlc3RlIGHDsW8uIikKCiAgICBjaGFuZ2VzID0gMAogICAgZm9yIHVuZSBpbiBfdW5lcygpOgogICAgICAgIGZvciBtZXRyaWMgaW4gX21ldHJpY3MoKToKICAgICAgICAgICAga2V5ID0gZiJ0YXJnZXRfe3VuZS5pZH1fe21ldHJpYy5pZH0iCiAgICAgICAgICAgIHJhdyA9IChwb3N0X2RhdGEuZ2V0KGtleSkgb3IgIiIpLnN0cmlwKCkKICAgICAgICAgICAgaWYgcmF3ID09ICIiOgogICAgICAgICAgICAgICAgY29udGludWUKICAgICAgICAgICAgcGFyc2VkID0gcGFyc2VfZGVjaW1hbF9vcl9ub25lKHJhdykKICAgICAgICAgICAgaWYgcGFyc2VkIGlzIE5vbmU6CiAgICAgICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKGYiVmFsb3IgaW52w6FsaWRvIGVuIG1ldGEge3VuZS5jb2RlfSAvIHttZXRyaWMuY29kZX0uIikKCiAgICAgICAgICAgIG9iaiwgXyA9IE1vbnRobHlUYXJnZXQub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgcGxhbj1wbGFuLAogICAgICAgICAgICAgICAgdW5lPXVuZSwKICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgICAgICAgICBtb250aD1tb250aCwKICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsidGFyZ2V0X3ZhbHVlIjogcGFyc2VkfSwKICAgICAgICAgICAgKQogICAgICAgICAgICBvbGQgPSBvYmoudGFyZ2V0X3ZhbHVlCiAgICAgICAgICAgIGlmIG9sZCAhPSBwYXJzZWQ6CiAgICAgICAgICAgICAgICBvYmoudGFyZ2V0X3ZhbHVlID0gcGFyc2VkCiAgICAgICAgICAgICAgICBvYmouc2F2ZSh1cGRhdGVfZmllbGRzPVsidGFyZ2V0X3ZhbHVlIiwgInVwZGF0ZWRfYXQiXSkKICAgICAgICAgICAgICAgIGxvZ19tYW51YWxfZWRpdCgKICAgICAgICAgICAgICAgICAgICB1c2VyPXVzZXIsCiAgICAgICAgICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgICAgIGVudGl0eV90eXBlPUFkbWluTWFudWFsRWRpdExvZy5FTlRJVFlfVEFSR0VULAogICAgICAgICAgICAgICAgICAgIGVudGl0eV9pZD1vYmouaWQsCiAgICAgICAgICAgICAgICAgICAgZmllbGRfbmFtZT0idGFyZ2V0X3ZhbHVlIiwKICAgICAgICAgICAgICAgICAgICBvbGRfdmFsdWU9b2xkLAogICAgICAgICAgICAgICAgICAgIG5ld192YWx1ZT1wYXJzZWQsCiAgICAgICAgICAgICAgICAgICAgcmVhc29uPXJlYXNvbiwKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIGNoYW5nZXMgKz0gMQogICAgcmV0dXJuIGNoYW5nZXMKCgpAdHJhbnNhY3Rpb24uYXRvbWljCmRlZiBzYXZlX3Jlc3VsdHModXNlciwgeWVhcjogaW50LCBtb250aDogaW50LCBwb3N0X2RhdGEsIHJlYXNvbjogc3RyID0gIiIpIC0+IGludDoKICAgIGlmIG5vdCByZWFzb24uc3RyaXAoKToKICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJEZWJlIGluZGljYXIgdW4gbW90aXZvIHBhcmEgY2FtYmlvcyBlbiByZXN1bHRhZG9zLiIpCgogICAgcGxhbiA9IF9nZXRfcGxhbih5ZWFyKQogICAgaWYgbm90IHBsYW46CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcigiTm8gZXhpc3RlIHBsYW4gUEdDIHBhcmEgZXN0ZSBhw7FvLiIpCgogICAgZnhfcmF0ZSA9IGdldF9meF9yYXRlKHllYXIsIG1vbnRoKQogICAgY2hhbmdlcyA9IDAKICAgIGZvciB1bmUgaW4gX3VuZXMoKToKICAgICAgICBmb3IgbWV0cmljIGluIF9tZXRyaWNzKCk6CiAgICAgICAgICAgIGtleSA9IGYicmVzdWx0X3t1bmUuaWR9X3ttZXRyaWMuaWR9IgogICAgICAgICAgICByYXcgPSAocG9zdF9kYXRhLmdldChrZXkpIG9yICIiKS5zdHJpcCgpCiAgICAgICAgICAgIGlmIHJhdyA9PSAiIjoKICAgICAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgICAgIHBhcnNlZCA9IHBhcnNlX2RlY2ltYWxfb3Jfbm9uZShyYXcpCiAgICAgICAgICAgIGlmIHBhcnNlZCBpcyBOb25lOgogICAgICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIlZhbG9yIGludsOhbGlkbyBlbiByZXN1bHRhZG8ge3VuZS5jb2RlfSAvIHttZXRyaWMuY29kZX0uIikKCiAgICAgICAgICAgIGlzX2luZ3Jlc29zID0gbWV0cmljLmNvZGUgPT0gTWV0cmljRGVmaW5pdGlvbi5DT0RFX0lOR1JFU09TCgogICAgICAgICAgICBpZiBpc19pbmdyZXNvczoKICAgICAgICAgICAgICAgIGN1cnJlbmN5ID0gKAogICAgICAgICAgICAgICAgICAgIHBvc3RfZGF0YS5nZXQoZiJpbmdyZXNvc19jdXJyX3t1bmUuaWR9IikKICAgICAgICAgICAgICAgICAgICBvciBwb3N0X2RhdGEuZ2V0KGYiaW5ncmVzb3NfY3Vycl97dW5lLmlkfV97bWV0cmljLmlkfSIpCiAgICAgICAgICAgICAgICAgICAgb3IgIkdUUSIKICAgICAgICAgICAgICAgICkuc3RyaXAoKS51cHBlcigpCiAgICAgICAgICAgICAgICBpZiBjdXJyZW5jeSBub3QgaW4gKAogICAgICAgICAgICAgICAgICAgIE1vbnRobHlNZXRyaWNSZXN1bHQuQ1VSUkVOQ1lfR1RRLAogICAgICAgICAgICAgICAgICAgIE1vbnRobHlNZXRyaWNSZXN1bHQuQ1VSUkVOQ1lfVVNELAogICAgICAgICAgICAgICAgKToKICAgICAgICAgICAgICAgICAgICBjdXJyZW5jeSA9IE1vbnRobHlNZXRyaWNSZXN1bHQuQ1VSUkVOQ1lfR1RRCgogICAgICAgICAgICAgICAgaWYgY3VycmVuY3kgPT0gTW9udGhseU1ldHJpY1Jlc3VsdC5DVVJSRU5DWV9VU0Q6CiAgICAgICAgICAgICAgICAgICAgdXNkX3ZhbHVlID0gcGFyc2VkCiAgICAgICAgICAgICAgICAgICAgb2JqLCBjcmVhdGVkID0gTW9udGhseU1ldHJpY1Jlc3VsdC5vYmplY3RzLmdldF9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgICAgICAgICAgICAgdW5lPXVuZSwKICAgICAgICAgICAgICAgICAgICAgICAgbWV0cmljPW1ldHJpYywKICAgICAgICAgICAgICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgICAgICAgICBtb250aD1tb250aCwKICAgICAgICAgICAgICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgICAgICAgICAgICAgIm1lYXN1cmVkX3ZhbHVlIjogdXNkX3ZhbHVlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgInNvdXJjZV9jdXJyZW5jeSI6IE1vbnRobHlNZXRyaWNSZXN1bHQuQ1VSUkVOQ1lfVVNELAogICAgICAgICAgICAgICAgICAgICAgICAgICAgInNvdXJjZV92YWx1ZSI6IHVzZF92YWx1ZSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJleGNoYW5nZV9yYXRlX3VzZWQiOiBOb25lLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImNvbnZlcnNpb25fc3RhdHVzIjogTW9udGhseU1ldHJpY1Jlc3VsdC5DT05WRVJTSU9OX05BVElWRV9VU0QsCiAgICAgICAgICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgICAgIG9sZF91c2QgPSBOb25lIGlmIGNyZWF0ZWQgZWxzZSBvYmoubWVhc3VyZWRfdmFsdWUKICAgICAgICAgICAgICAgICAgICBvbGRfY3VyciA9ICIiIGlmIGNyZWF0ZWQgZWxzZSAob2JqLnNvdXJjZV9jdXJyZW5jeSBvciAiIikKICAgICAgICAgICAgICAgICAgICBjaGFuZ2VkID0gKAogICAgICAgICAgICAgICAgICAgICAgICBjcmVhdGVkCiAgICAgICAgICAgICAgICAgICAgICAgIG9yIG9sZF91c2QgIT0gdXNkX3ZhbHVlCiAgICAgICAgICAgICAgICAgICAgICAgIG9yIG9sZF9jdXJyICE9IE1vbnRobHlNZXRyaWNSZXN1bHQuQ1VSUkVOQ1lfVVNECiAgICAgICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgICAgIGlmIG5vdCBjaGFuZ2VkOgogICAgICAgICAgICAgICAgICAgICAgICBjb250aW51ZQoKICAgICAgICAgICAgICAgICAgICBvYmoubWVhc3VyZWRfdmFsdWUgPSB1c2RfdmFsdWUKICAgICAgICAgICAgICAgICAgICBvYmouc291cmNlX2N1cnJlbmN5ID0gTW9udGhseU1ldHJpY1Jlc3VsdC5DVVJSRU5DWV9VU0QKICAgICAgICAgICAgICAgICAgICBvYmouc291cmNlX3ZhbHVlID0gdXNkX3ZhbHVlCiAgICAgICAgICAgICAgICAgICAgb2JqLmV4Y2hhbmdlX3JhdGVfdXNlZCA9IE5vbmUKICAgICAgICAgICAgICAgICAgICBvYmouY29udmVyc2lvbl9zdGF0dXMgPSBNb250aGx5TWV0cmljUmVzdWx0LkNPTlZFUlNJT05fTkFUSVZFX1VTRAogICAgICAgICAgICAgICAgICAgIG9iai5jYWxjdWxhdGlvbl9ub3RlID0gKAogICAgICAgICAgICAgICAgICAgICAgICBmIkNhcHR1cmEgbWFudWFsIFVTRCBuYXRpdm86IHt1c2RfdmFsdWV9IFVTRCBbe3llYXJ9LXttb250aDowMmR9XSIKICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAgICAgb2JqLnNhdmUoCiAgICAgICAgICAgICAgICAgICAgICAgIHVwZGF0ZV9maWVsZHM9WwogICAgICAgICAgICAgICAgICAgICAgICAgICAgIm1lYXN1cmVkX3ZhbHVlIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJzb3VyY2VfY3VycmVuY3kiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgInNvdXJjZV92YWx1ZSIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAiZXhjaGFuZ2VfcmF0ZV91c2VkIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJjb252ZXJzaW9uX3N0YXR1cyIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAiY2FsY3VsYXRpb25fbm90ZSIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAidXBkYXRlZF9hdCIsCiAgICAgICAgICAgICAgICAgICAgICAgIF0KICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAgICAgbG9nX21hbnVhbF9lZGl0KAogICAgICAgICAgICAgICAgICAgICAgICB1c2VyPXVzZXIsCiAgICAgICAgICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgICAgICAgICAgICAgIGVudGl0eV90eXBlPUFkbWluTWFudWFsRWRpdExvZy5FTlRJVFlfUkVTVUxULAogICAgICAgICAgICAgICAgICAgICAgICBlbnRpdHlfaWQ9b2JqLmlkLAogICAgICAgICAgICAgICAgICAgICAgICBmaWVsZF9uYW1lPSJpbmdyZXNvc191c2RfbmF0aXZlIiwKICAgICAgICAgICAgICAgICAgICAgICAgb2xkX3ZhbHVlPWYiVVNEPXtvbGRfdXNkfTsgY3Vycj17b2xkX2N1cnJ9IiwKICAgICAgICAgICAgICAgICAgICAgICAgbmV3X3ZhbHVlPWYiVVNEPXt1c2RfdmFsdWV9IiwKICAgICAgICAgICAgICAgICAgICAgICAgcmVhc29uPXJlYXNvbiwKICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAgICAgY2hhbmdlcyArPSAxCiAgICAgICAgICAgICAgICAgICAgY29udGludWUKCiAgICAgICAgICAgICAgICAjIE1hbnVhbCBJTkdSRVNPUzogY2FwdHVyZSBHVFEsIGNvbnZlcnQgdG8gY2Fub25pY2FsIFVTRC4KICAgICAgICAgICAgICAgIGlmIGZ4X3JhdGUgaXMgTm9uZToKICAgICAgICAgICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKAogICAgICAgICAgICAgICAgICAgICAgICBmIkZhbHRhIHRpcG8gZGUgY2FtYmlvIHBhcmEge3llYXJ9LXttb250aDowMmR9LiAiCiAgICAgICAgICAgICAgICAgICAgICAgIGYiTm8gc2UgcHVlZGVuIGd1YXJkYXIgaW5ncmVzb3MgKEdUUSkgZGUge3VuZS5uYW1lX2VzfSBzaW4gVEMuICIKICAgICAgICAgICAgICAgICAgICAgICAgIlZheWEgYSBsYSBwZXN0YcOxYSDCq1RpcG9zIGRlIGNhbWJpb8K7LiIKICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICB1c2RfdmFsdWUgPSBndHFfdG9fdXNkKHBhcnNlZCwgZnhfcmF0ZSkKICAgICAgICAgICAgICAgIG9iaiwgY3JlYXRlZCA9IE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgICAgICAgICB1bmU9dW5lLAogICAgICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICAgICAgICAgIm1lYXN1cmVkX3ZhbHVlIjogdXNkX3ZhbHVlLAogICAgICAgICAgICAgICAgICAgICAgICAic291cmNlX2N1cnJlbmN5IjogTW9udGhseU1ldHJpY1Jlc3VsdC5DVVJSRU5DWV9HVFEsCiAgICAgICAgICAgICAgICAgICAgICAgICJzb3VyY2VfdmFsdWUiOiBwYXJzZWQsCiAgICAgICAgICAgICAgICAgICAgICAgICJleGNoYW5nZV9yYXRlX3VzZWQiOiBmeF9yYXRlLAogICAgICAgICAgICAgICAgICAgICAgICAiY29udmVyc2lvbl9zdGF0dXMiOiBNb250aGx5TWV0cmljUmVzdWx0LkNPTlZFUlNJT05fQ09OVkVSVEVELAogICAgICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICBvbGRfdXNkID0gTm9uZSBpZiBjcmVhdGVkIGVsc2Ugb2JqLm1lYXN1cmVkX3ZhbHVlCiAgICAgICAgICAgICAgICBvbGRfZ3RxID0gTm9uZSBpZiBjcmVhdGVkIGVsc2Ugb2JqLnNvdXJjZV92YWx1ZQogICAgICAgICAgICAgICAgY2hhbmdlZCA9ICgKICAgICAgICAgICAgICAgICAgICBjcmVhdGVkCiAgICAgICAgICAgICAgICAgICAgb3Igb2xkX3VzZCAhPSB1c2RfdmFsdWUKICAgICAgICAgICAgICAgICAgICBvciBvbGRfZ3RxICE9IHBhcnNlZAogICAgICAgICAgICAgICAgICAgIG9yIG9iai5zb3VyY2VfY3VycmVuY3kgIT0gTW9udGhseU1ldHJpY1Jlc3VsdC5DVVJSRU5DWV9HVFEKICAgICAgICAgICAgICAgICAgICBvciBvYmouZXhjaGFuZ2VfcmF0ZV91c2VkICE9IGZ4X3JhdGUKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIGlmIG5vdCBjaGFuZ2VkOgogICAgICAgICAgICAgICAgICAgIGNvbnRpbnVlCgogICAgICAgICAgICAgICAgb2JqLm1lYXN1cmVkX3ZhbHVlID0gdXNkX3ZhbHVlCiAgICAgICAgICAgICAgICBvYmouc291cmNlX2N1cnJlbmN5ID0gTW9udGhseU1ldHJpY1Jlc3VsdC5DVVJSRU5DWV9HVFEKICAgICAgICAgICAgICAgIG9iai5zb3VyY2VfdmFsdWUgPSBwYXJzZWQKICAgICAgICAgICAgICAgIG9iai5leGNoYW5nZV9yYXRlX3VzZWQgPSBmeF9yYXRlCiAgICAgICAgICAgICAgICBvYmouY29udmVyc2lvbl9zdGF0dXMgPSBNb250aGx5TWV0cmljUmVzdWx0LkNPTlZFUlNJT05fQ09OVkVSVEVECiAgICAgICAgICAgICAgICBvYmouY2FsY3VsYXRpb25fbm90ZSA9ICgKICAgICAgICAgICAgICAgICAgICBmIkNhcHR1cmEgbWFudWFsIEdUUeKGklVTRDoge3BhcnNlZH0gR1RRIC8ge2Z4X3JhdGV9ID0ge3VzZF92YWx1ZX0gVVNEICIKICAgICAgICAgICAgICAgICAgICBmIlt7eWVhcn0te21vbnRoOjAyZH1dIgogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgb2JqLnNhdmUoCiAgICAgICAgICAgICAgICAgICAgdXBkYXRlX2ZpZWxkcz1bCiAgICAgICAgICAgICAgICAgICAgICAgICJtZWFzdXJlZF92YWx1ZSIsCiAgICAgICAgICAgICAgICAgICAgICAgICJzb3VyY2VfY3VycmVuY3kiLAogICAgICAgICAgICAgICAgICAgICAgICAic291cmNlX3ZhbHVlIiwKICAgICAgICAgICAgICAgICAgICAgICAgImV4Y2hhbmdlX3JhdGVfdXNlZCIsCiAgICAgICAgICAgICAgICAgICAgICAgICJjb252ZXJzaW9uX3N0YXR1cyIsCiAgICAgICAgICAgICAgICAgICAgICAgICJjYWxjdWxhdGlvbl9ub3RlIiwKICAgICAgICAgICAgICAgICAgICAgICAgInVwZGF0ZWRfYXQiLAogICAgICAgICAgICAgICAgICAgIF0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIGxvZ19tYW51YWxfZWRpdCgKICAgICAgICAgICAgICAgICAgICB1c2VyPXVzZXIsCiAgICAgICAgICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgICAgIGVudGl0eV90eXBlPUFkbWluTWFudWFsRWRpdExvZy5FTlRJVFlfUkVTVUxULAogICAgICAgICAgICAgICAgICAgIGVudGl0eV9pZD1vYmouaWQsCiAgICAgICAgICAgICAgICAgICAgZmllbGRfbmFtZT0iaW5ncmVzb3NfZ3RxX3RvX3VzZCIsCiAgICAgICAgICAgICAgICAgICAgb2xkX3ZhbHVlPWYiR1RRPXtvbGRfZ3RxfTsgVVNEPXtvbGRfdXNkfSIsCiAgICAgICAgICAgICAgICAgICAgbmV3X3ZhbHVlPWYiR1RRPXtwYXJzZWR9OyBGWD17ZnhfcmF0ZX07IFVTRD17dXNkX3ZhbHVlfSIsCiAgICAgICAgICAgICAgICAgICAgcmVhc29uPXJlYXNvbiwKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIGNoYW5nZXMgKz0gMQogICAgICAgICAgICAgICAgY29udGludWUKCiAgICAgICAgICAgICMgTm9uLUlOR1JFU09TIG1ldHJpY3M6IGtlZXAgbGVnYWN5IFVTRC9uYXRpdmUgbnVtZXJpYyBzZW1hbnRpY3MuCiAgICAgICAgICAgIG9iaiwgY3JlYXRlZCA9IE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgcGxhbj1wbGFuLAogICAgICAgICAgICAgICAgdW5lPXVuZSwKICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgICAgICAgICBtb250aD1tb250aCwKICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICAgICAibWVhc3VyZWRfdmFsdWUiOiBwYXJzZWQsCiAgICAgICAgICAgICAgICAgICAgInNvdXJjZV9jdXJyZW5jeSI6ICIiLAogICAgICAgICAgICAgICAgICAgICJjb252ZXJzaW9uX3N0YXR1cyI6IE1vbnRobHlNZXRyaWNSZXN1bHQuQ09OVkVSU0lPTl9OQVRJVkVfVVNELAogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgKQogICAgICAgICAgICBvbGQgPSBOb25lIGlmIGNyZWF0ZWQgZWxzZSBvYmoubWVhc3VyZWRfdmFsdWUKICAgICAgICAgICAgaWYgY3JlYXRlZCBvciBvbGQgIT0gcGFyc2VkOgogICAgICAgICAgICAgICAgb2JqLm1lYXN1cmVkX3ZhbHVlID0gcGFyc2VkCiAgICAgICAgICAgICAgICBvYmouY2FsY3VsYXRpb25fbm90ZSA9IChvYmouY2FsY3VsYXRpb25fbm90ZSBvciAiIikgKyAiIFtFZGljacOzbiBtYW51YWxdIgogICAgICAgICAgICAgICAgb2JqLnNhdmUodXBkYXRlX2ZpZWxkcz1bIm1lYXN1cmVkX3ZhbHVlIiwgImNhbGN1bGF0aW9uX25vdGUiLCAidXBkYXRlZF9hdCJdKQogICAgICAgICAgICAgICAgbG9nX21hbnVhbF9lZGl0KAogICAgICAgICAgICAgICAgICAgIHVzZXI9dXNlciwKICAgICAgICAgICAgICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgICAgICAgICAgZW50aXR5X3R5cGU9QWRtaW5NYW51YWxFZGl0TG9nLkVOVElUWV9SRVNVTFQsCiAgICAgICAgICAgICAgICAgICAgZW50aXR5X2lkPW9iai5pZCwKICAgICAgICAgICAgICAgICAgICBmaWVsZF9uYW1lPSJtZWFzdXJlZF92YWx1ZSIsCiAgICAgICAgICAgICAgICAgICAgb2xkX3ZhbHVlPW9sZCwKICAgICAgICAgICAgICAgICAgICBuZXdfdmFsdWU9cGFyc2VkLAogICAgICAgICAgICAgICAgICAgIHJlYXNvbj1yZWFzb24sCiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICBjaGFuZ2VzICs9IDEKICAgIHJldHVybiBjaGFuZ2VzCgoKQHRyYW5zYWN0aW9uLmF0b21pYwpkZWYgc2F2ZV9meCh1c2VyLCB5ZWFyOiBpbnQsIG1vbnRoOiBpbnQsIHBvc3RfZGF0YSwgcmVhc29uOiBzdHIgPSAiIiwgbW9udGhfZnJvbTogaW50IHwgTm9uZSA9IE5vbmUpIC0+IGludDoKICAgICIiIlNhdmUgRlggZm9yIGZvY3VzIG1vbnRoIGFuZC9vciBldmVyeSBtb250aCBpbiBbbW9udGhfZnJvbSwgbW9udGhdLgoKICAgIEFjY2VwdHMgZWl0aGVyOgogICAgLSBgYGZ4X3ZhbHVlYGAgZm9yIGEgc2luZ2xlIG1vbnRoIChmb2N1cyBgYG1vbnRoYGApLCBvcgogICAgLSBgYGZ4X3ZhbHVlXzxtPmBgIGZvciBlYWNoIG1vbnRoIGluIHRoZSBzZWxlY3RlZCByYW5nZS4KICAgICIiIgogICAgbWYgPSBtb250aF9mcm9tIG9yIG1vbnRoCiAgICBpZiBtZiA+IG1vbnRoOgogICAgICAgIG1mID0gbW9udGgKCiAgICBlbnRyaWVzOiBsaXN0W3R1cGxlW2ludCwgc3RyXV0gPSBbXQogICAgc2F3X3JhbmdlX2tleXMgPSBGYWxzZQogICAgZm9yIG0gaW4gcmFuZ2UobWYsIG1vbnRoICsgMSk6CiAgICAgICAga2V5ID0gZiJmeF92YWx1ZV97bX0iCiAgICAgICAgaWYga2V5IGluIHBvc3RfZGF0YToKICAgICAgICAgICAgc2F3X3JhbmdlX2tleXMgPSBUcnVlCiAgICAgICAgICAgIGVudHJpZXMuYXBwZW5kKChtLCAocG9zdF9kYXRhLmdldChrZXkpIG9yICIiKS5zdHJpcCgpKSkKICAgIGlmIG5vdCBzYXdfcmFuZ2Vfa2V5czoKICAgICAgICBlbnRyaWVzID0gWyhtb250aCwgKHBvc3RfZGF0YS5nZXQoImZ4X3ZhbHVlIikgb3IgIiIpLnN0cmlwKCkpXQoKICAgIGNoYW5nZXMgPSAwCiAgICBmb3IgbSwgcmF3IGluIGVudHJpZXM6CiAgICAgICAgaWYgcmF3ID09ICIiOgogICAgICAgICAgICBjb250aW51ZQogICAgICAgIHBhcnNlZCA9IHBhcnNlX2RlY2ltYWxfb3Jfbm9uZShyYXcpCiAgICAgICAgaWYgcGFyc2VkIGlzIE5vbmU6CiAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJUaXBvIGRlIGNhbWJpbyBpbnbDoWxpZG8gcGFyYSB7eWVhcn0te206MDJkfS4iKQoKICAgICAgICBvYmosIGNyZWF0ZWQgPSBNb250aGx5RXhjaGFuZ2VSYXRlLm9iamVjdHMuZ2V0X29yX2NyZWF0ZSgKICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICBtb250aD1tLAogICAgICAgICAgICBkZWZhdWx0cz17InVzZF90b19ndHEiOiBwYXJzZWR9LAogICAgICAgICkKICAgICAgICBvbGQgPSBOb25lIGlmIGNyZWF0ZWQgZWxzZSBvYmoudXNkX3RvX2d0cQogICAgICAgIGlmIGNyZWF0ZWQgb3Igb2xkICE9IHBhcnNlZDoKICAgICAgICAgICAgb2JqLnVzZF90b19ndHEgPSBwYXJzZWQKICAgICAgICAgICAgb2JqLnNhdmUodXBkYXRlX2ZpZWxkcz1bInVzZF90b19ndHEiXSkKICAgICAgICAgICAgbG9nX21hbnVhbF9lZGl0KAogICAgICAgICAgICAgICAgdXNlcj11c2VyLAogICAgICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgbW9udGg9bSwKICAgICAgICAgICAgICAgIGVudGl0eV90eXBlPUFkbWluTWFudWFsRWRpdExvZy5FTlRJVFlfRlgsCiAgICAgICAgICAgICAgICBlbnRpdHlfaWQ9b2JqLmlkLAogICAgICAgICAgICAgICAgZmllbGRfbmFtZT0idXNkX3RvX2d0cSIsCiAgICAgICAgICAgICAgICBvbGRfdmFsdWU9b2xkLAogICAgICAgICAgICAgICAgbmV3X3ZhbHVlPXBhcnNlZCwKICAgICAgICAgICAgICAgIHJlYXNvbj1yZWFzb24sCiAgICAgICAgICAgICkKICAgICAgICAgICAgIyBEbyBub3Qgc2lsZW50bHkgcmVjYWxjIGluY29tZXM7IG1hcmsgY29udmVydGlibGUgR1RRIHJvd3MgYXMgc3RhbGUuCiAgICAgICAgICAgIGlmIG5vdCBjcmVhdGVkIGFuZCBvbGQgIT0gcGFyc2VkOgogICAgICAgICAgICAgICAgbWFya19pbmdyZXNvc19zdGFsZV9mb3JfZnhfY2hhbmdlKAogICAgICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgICAgICBtb250aD1tLAogICAgICAgICAgICAgICAgICAgIG9sZF9meD1vbGQsCiAgICAgICAgICAgICAgICAgICAgbmV3X2Z4PXBhcnNlZCwKICAgICAgICAgICAgICAgICAgICB1c2VyPXVzZXIsCiAgICAgICAgICAgICAgICAgICAgcmVhc29uPXJlYXNvbiwKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgY2hhbmdlcyArPSAxCiAgICByZXR1cm4gY2hhbmdlcwoKCkB0cmFuc2FjdGlvbi5hdG9taWMKZGVmIHNhdmVfcmVxdWlyZW1lbnRzKHVzZXIsIHllYXI6IGludCwgbW9udGg6IGludCwgcG9zdF9kYXRhLCByZWFzb246IHN0ciA9ICIiKSAtPiBpbnQ6CiAgICBwbGFuID0gX2dldF9wbGFuKHllYXIpCiAgICBpZiBub3QgcGxhbjoKICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJObyBleGlzdGUgcGxhbiBQR0MgcGFyYSBlc3RlIGHDsW8uIikKCiAgICBjaGFuZ2VzID0gMAogICAgZm9yIHVuZSBpbiBfdW5lcygpOgogICAgICAgIGNvbXBsaWFudF9rZXkgPSBmInJlcV9jb21wbGlhbnRfe3VuZS5pZH0iCiAgICAgICAgbm90ZV9rZXkgPSBmInJlcV9ub3RlX3t1bmUuaWR9IgogICAgICAgIGlzX2NvbXBsaWFudCA9IHBvc3RfZGF0YS5nZXQoY29tcGxpYW50X2tleSkgPT0gIjEiCiAgICAgICAgaW5jaWRlbnRfbm90ZSA9IChwb3N0X2RhdGEuZ2V0KG5vdGVfa2V5KSBvciAiIikuc3RyaXAoKQoKICAgICAgICBpZiBub3QgaXNfY29tcGxpYW50IGFuZCBub3QgaW5jaWRlbnRfbm90ZSBhbmQgbm90IHJlYXNvbi5zdHJpcCgpOgogICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKGYiSW5kaXF1ZSBtb3Rpdm8gbyBub3RhIGRlIGluY2lkZW5jaWEgcGFyYSB7dW5lLm5hbWVfZXN9LiIpCgogICAgICAgIG9iaiwgY3JlYXRlZCA9IE1hbnVhbFJlcXVpcmVtZW50c0NvbXBsaWFuY2Uub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICBwbGFuPXBsYW4sCiAgICAgICAgICAgIHVuZT11bmUsCiAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgIGRlZmF1bHRzPXsiaXNfY29tcGxpYW50IjogaXNfY29tcGxpYW50LCAiaW5jaWRlbnRfbm90ZSI6IGluY2lkZW50X25vdGV9LAogICAgICAgICkKICAgICAgICBvbGRfY29tcGxpYW50ID0gTm9uZSBpZiBjcmVhdGVkIGVsc2Ugb2JqLmlzX2NvbXBsaWFudAogICAgICAgIG9sZF9ub3RlID0gIiIgaWYgY3JlYXRlZCBlbHNlIG9iai5pbmNpZGVudF9ub3RlCgogICAgICAgIGNoYW5nZWQgPSBGYWxzZQogICAgICAgIGlmIG9iai5pc19jb21wbGlhbnQgIT0gaXNfY29tcGxpYW50OgogICAgICAgICAgICBvYmouaXNfY29tcGxpYW50ID0gaXNfY29tcGxpYW50CiAgICAgICAgICAgIGNoYW5nZWQgPSBUcnVlCiAgICAgICAgaWYgb2JqLmluY2lkZW50X25vdGUgIT0gaW5jaWRlbnRfbm90ZToKICAgICAgICAgICAgb2JqLmluY2lkZW50X25vdGUgPSBpbmNpZGVudF9ub3RlCiAgICAgICAgICAgIGNoYW5nZWQgPSBUcnVlCgogICAgICAgIGlmIGNoYW5nZWQ6CiAgICAgICAgICAgIG9iai5zYXZlKHVwZGF0ZV9maWVsZHM9WyJpc19jb21wbGlhbnQiLCAiaW5jaWRlbnRfbm90ZSIsICJ1cGRhdGVkX2F0Il0pCiAgICAgICAgICAgIGxvZ19tYW51YWxfZWRpdCgKICAgICAgICAgICAgICAgIHVzZXI9dXNlciwKICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgZW50aXR5X3R5cGU9QWRtaW5NYW51YWxFZGl0TG9nLkVOVElUWV9SRVFVSVJFTUVOVCwKICAgICAgICAgICAgICAgIGVudGl0eV9pZD1vYmouaWQsCiAgICAgICAgICAgICAgICBmaWVsZF9uYW1lPSJpc19jb21wbGlhbnQvaW5jaWRlbnRfbm90ZSIsCiAgICAgICAgICAgICAgICBvbGRfdmFsdWU9ZiJjb21wbGlhbnQ9e29sZF9jb21wbGlhbnR9OyBub3RlPXtvbGRfbm90ZX0iLAogICAgICAgICAgICAgICAgbmV3X3ZhbHVlPWYiY29tcGxpYW50PXtpc19jb21wbGlhbnR9OyBub3RlPXtpbmNpZGVudF9ub3RlfSIsCiAgICAgICAgICAgICAgICByZWFzb249cmVhc29uIG9yIGluY2lkZW50X25vdGUsCiAgICAgICAgICAgICkKICAgICAgICAgICAgY2hhbmdlcyArPSAxCiAgICByZXR1cm4gY2hhbmdlcwoKCkB0cmFuc2FjdGlvbi5hdG9taWMKZGVmIHNhdmVfYWxpYXModXNlciwgeWVhcjogaW50LCBtb250aDogaW50LCBwb3N0X2RhdGEsIHJlYXNvbjogc3RyID0gIiIpIC0+IGludDoKICAgIHJhd192YWx1ZSA9IChwb3N0X2RhdGEuZ2V0KCJhbGlhc19yYXciKSBvciAiIikuc3RyaXAoKQogICAgdW5lX2lkID0gcG9zdF9kYXRhLmdldCgiYWxpYXNfdW5lIikKICAgIGlmIG5vdCByYXdfdmFsdWUgb3Igbm90IHVuZV9pZDoKICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJEZWJlIGluZGljYXIgdmFsb3IgY3J1ZG8geSBVTkUgZGVzdGluby4iKQoKICAgIHVuZSA9IFVORS5vYmplY3RzLmZpbHRlcihpZD11bmVfaWQpLmZpcnN0KCkKICAgIGlmIG5vdCB1bmU6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcigiVU5FIG5vIHbDoWxpZGEuIikKCiAgICAjIEludmVzdG1lbnQgZW4gZWwgdmFsb3IgY3J1ZG8gc2llbXByZSBhcHVudGEgYSBJbnZlcnNpb25lcy4KICAgIHJhd19sb3dlciA9IHJhd192YWx1ZS5sb3dlcigpCiAgICBpZiBhbnkoCiAgICAgICAgdG9rZW4gaW4gcmF3X2xvd2VyCiAgICAgICAgZm9yIHRva2VuIGluICgKICAgICAgICAgICAgImludmVzdG1lbnQiLAogICAgICAgICAgICAiaW52ZXN0bWVudHMiLAogICAgICAgICAgICAiaW52ZXN0IiwKICAgICAgICAgICAgImludmVyc2lvbmVzIiwKICAgICAgICAgICAgImludmVyc2lvbiIsCiAgICAgICAgICAgICJpbnZlcnNpw7NuIiwKICAgICAgICApCiAgICApOgogICAgICAgIGludmVzdG1lbnQgPSBVTkUub2JqZWN0cy5maWx0ZXIoY29kZT1VTkUuQ09ERV9JTlZFU1RNRU5UKS5maXJzdCgpCiAgICAgICAgaWYgaW52ZXN0bWVudDoKICAgICAgICAgICAgdW5lID0gaW52ZXN0bWVudAoKICAgIG9iaiwgY3JlYXRlZCA9IFVORUFsaWFzLm9iamVjdHMuZ2V0X29yX2NyZWF0ZSgKICAgICAgICByYXdfdmFsdWU9cmF3X3ZhbHVlLAogICAgICAgIGRlZmF1bHRzPXsidW5lIjogdW5lLCAiaXNfYWN0aXZlIjogVHJ1ZX0sCiAgICApCiAgICBvbGRfdW5lID0gTm9uZSBpZiBjcmVhdGVkIGVsc2Ugb2JqLnVuZV9pZAogICAgaWYgbm90IGNyZWF0ZWQgYW5kIChvYmoudW5lX2lkICE9IHVuZS5pZCBvciBub3Qgb2JqLmlzX2FjdGl2ZSk6CiAgICAgICAgb2JqLnVuZSA9IHVuZQogICAgICAgIG9iai5pc19hY3RpdmUgPSBUcnVlCiAgICAgICAgb2JqLnNhdmUodXBkYXRlX2ZpZWxkcz1bInVuZSIsICJpc19hY3RpdmUiLCAidXBkYXRlZF9hdCJdKQogICAgICAgIGxvZ19tYW51YWxfZWRpdCgKICAgICAgICAgICAgdXNlcj11c2VyLAogICAgICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICBlbnRpdHlfdHlwZT1BZG1pbk1hbnVhbEVkaXRMb2cuRU5USVRZX0FMSUFTLAogICAgICAgICAgICBlbnRpdHlfaWQ9b2JqLmlkLAogICAgICAgICAgICBmaWVsZF9uYW1lPSJ1bmUiLAogICAgICAgICAgICBvbGRfdmFsdWU9b2xkX3VuZSwKICAgICAgICAgICAgbmV3X3ZhbHVlPXVuZS5pZCwKICAgICAgICAgICAgcmVhc29uPXJlYXNvbiBvciBmIk1hcGVvIHtyYXdfdmFsdWV9IC0+IHt1bmUuY29kZX0iLAogICAgICAgICkKICAgICAgICByZXR1cm4gMQoKICAgIGlmIGNyZWF0ZWQ6CiAgICAgICAgbG9nX21hbnVhbF9lZGl0KAogICAgICAgICAgICB1c2VyPXVzZXIsCiAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgIGVudGl0eV90eXBlPUFkbWluTWFudWFsRWRpdExvZy5FTlRJVFlfQUxJQVMsCiAgICAgICAgICAgIGVudGl0eV9pZD1vYmouaWQsCiAgICAgICAgICAgIGZpZWxkX25hbWU9InJhd192YWx1ZSIsCiAgICAgICAgICAgIG9sZF92YWx1ZT0iIiwKICAgICAgICAgICAgbmV3X3ZhbHVlPXJhd192YWx1ZSwKICAgICAgICAgICAgcmVhc29uPXJlYXNvbiBvciBmIk51ZXZvIGFsaWFzIC0+IHt1bmUuY29kZX0iLAogICAgICAgICkKICAgICAgICByZXR1cm4gMQogICAgcmV0dXJuIDAKCgpAdHJhbnNhY3Rpb24uYXRvbWljCmRlZiBzYXZlX2FsaWFzZXNfYnVsayh1c2VyLCB5ZWFyOiBpbnQsIG1vbnRoOiBpbnQsIHBvc3RfZGF0YSwgcmVhc29uOiBzdHIgPSAiIikgLT4gaW50OgogICAgIiIiQWN0dWFsaXphIFVORSBkZSBhbGlhc2VzIGV4aXN0ZW50ZXMgZGVzZGUgbGEgdGFibGEgZWRpdGFibGUuIiIiCiAgICBjaGFuZ2VzID0gMAogICAgaW52ZXN0bWVudCA9IFVORS5vYmplY3RzLmZpbHRlcihjb2RlPVVORS5DT0RFX0lOVkVTVE1FTlQpLmZpcnN0KCkKICAgIGJ5X2lkID0ge3UuaWQ6IHUgZm9yIHUgaW4gVU5FLm9iamVjdHMuZmlsdGVyKGlzX2FjdGl2ZT1UcnVlKX0KCiAgICBmb3IgYWxpYXMgaW4gVU5FQWxpYXMub2JqZWN0cy5maWx0ZXIoaXNfYWN0aXZlPVRydWUpOgogICAgICAgIHJhdyA9IHBvc3RfZGF0YS5nZXQoZiJhbGlhc197YWxpYXMuaWR9X3VuZSIpCiAgICAgICAgaWYgcmF3IGlzIE5vbmU6CiAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgdHJ5OgogICAgICAgICAgICB1bmVfaWQgPSBpbnQocmF3KQogICAgICAgIGV4Y2VwdCAoVHlwZUVycm9yLCBWYWx1ZUVycm9yKToKICAgICAgICAgICAgY29udGludWUKICAgICAgICB1bmUgPSBieV9pZC5nZXQodW5lX2lkKQogICAgICAgIGlmIG5vdCB1bmU6CiAgICAgICAgICAgIGNvbnRpbnVlCgogICAgICAgIHJhd19sb3dlciA9IChhbGlhcy5yYXdfdmFsdWUgb3IgIiIpLmxvd2VyKCkKICAgICAgICBpZiBpbnZlc3RtZW50IGFuZCBhbnkoCiAgICAgICAgICAgIHRva2VuIGluIHJhd19sb3dlcgogICAgICAgICAgICBmb3IgdG9rZW4gaW4gKAogICAgICAgICAgICAgICAgImludmVzdG1lbnQiLAogICAgICAgICAgICAgICAgImludmVzdG1lbnRzIiwKICAgICAgICAgICAgICAgICJpbnZlc3QiLAogICAgICAgICAgICAgICAgImludmVyc2lvbmVzIiwKICAgICAgICAgICAgICAgICJpbnZlcnNpb24iLAogICAgICAgICAgICAgICAgImludmVyc2nDs24iLAogICAgICAgICAgICApCiAgICAgICAgKToKICAgICAgICAgICAgdW5lID0gaW52ZXN0bWVudAoKICAgICAgICBpZiBhbGlhcy51bmVfaWQgPT0gdW5lLmlkOgogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICBvbGRfdW5lID0gYWxpYXMudW5lX2lkCiAgICAgICAgYWxpYXMudW5lID0gdW5lCiAgICAgICAgYWxpYXMuc2F2ZSh1cGRhdGVfZmllbGRzPVsidW5lIiwgInVwZGF0ZWRfYXQiXSkKICAgICAgICBsb2dfbWFudWFsX2VkaXQoCiAgICAgICAgICAgIHVzZXI9dXNlciwKICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICBtb250aD1tb250aCwKICAgICAgICAgICAgZW50aXR5X3R5cGU9QWRtaW5NYW51YWxFZGl0TG9nLkVOVElUWV9BTElBUywKICAgICAgICAgICAgZW50aXR5X2lkPWFsaWFzLmlkLAogICAgICAgICAgICBmaWVsZF9uYW1lPSJ1bmUiLAogICAgICAgICAgICBvbGRfdmFsdWU9b2xkX3VuZSwKICAgICAgICAgICAgbmV3X3ZhbHVlPXVuZS5pZCwKICAgICAgICAgICAgcmVhc29uPXJlYXNvbiBvciBmIkNvcnJlY2Npw7NuIGFsaWFzIHthbGlhcy5yYXdfdmFsdWV9IC0+IHt1bmUuY29kZX0iLAogICAgICAgICkKICAgICAgICBjaGFuZ2VzICs9IDEKICAgIHJldHVybiBjaGFuZ2VzCgoKQHRyYW5zYWN0aW9uLmF0b21pYwpkZWYgc2F2ZV9pbXBvcnRfcm93cygKICAgIHVzZXIsCiAgICB5ZWFyOiBpbnQsCiAgICBtb250aDogaW50LAogICAgcG9zdF9kYXRhLAogICAgcmVhc29uOiBzdHIgPSAiIiwKICAgIG1vbnRoX2Zyb206IGludCB8IE5vbmUgPSBOb25lLAopIC0+IGludDoKICAgIGNoYW5nZXMgPSAwCiAgICBtZiA9IG1vbnRoX2Zyb20gb3IgbW9udGgKCiAgICBmb3Igcm93IGluIE5ld0NsaWVudEltcG9ydFJvdy5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIsIG1vbnRoX19ndGU9bWYsIG1vbnRoX19sdGU9bW9udGgpOgogICAgICAgIHByZWZpeCA9IGYibmNfe3Jvdy5pZH1fIgogICAgICAgIGNvdW50cyA9IHBvc3RfZGF0YS5nZXQoZiJ7cHJlZml4fWNvdW50c19hc19uZXciKSA9PSAiMSIKICAgICAgICBvYnMgPSAocG9zdF9kYXRhLmdldChmIntwcmVmaXh9b2JzZXJ2YXRpb25zIikgb3IgIiIpLnN0cmlwKCkKICAgICAgICBvbGRfY291bnRzID0gcm93LmNvdW50c19hc19uZXcKICAgICAgICBvbGRfb2JzID0gcm93Lm9ic2VydmF0aW9ucwogICAgICAgIGlmIGNvdW50cyAhPSBvbGRfY291bnRzIG9yIG9icyAhPSBvbGRfb2JzOgogICAgICAgICAgICByb3cuY291bnRzX2FzX25ldyA9IGNvdW50cwogICAgICAgICAgICByb3cub2JzZXJ2YXRpb25zID0gb2JzCiAgICAgICAgICAgIHJvdy5zYXZlKHVwZGF0ZV9maWVsZHM9WyJjb3VudHNfYXNfbmV3IiwgIm9ic2VydmF0aW9ucyIsICJ1cGRhdGVkX2F0Il0pCiAgICAgICAgICAgIGxvZ19tYW51YWxfZWRpdCgKICAgICAgICAgICAgICAgIHVzZXI9dXNlciwKICAgICAgICAgICAgICAgIHllYXI9cm93LnllYXIsCiAgICAgICAgICAgICAgICBtb250aD1yb3cubW9udGgsCiAgICAgICAgICAgICAgICBlbnRpdHlfdHlwZT1BZG1pbk1hbnVhbEVkaXRMb2cuRU5USVRZX05FV19DTElFTlRfUk9XLAogICAgICAgICAgICAgICAgZW50aXR5X2lkPXJvdy5pZCwKICAgICAgICAgICAgICAgIGZpZWxkX25hbWU9ImNvdW50c19hc19uZXcvb2JzZXJ2YXRpb25zIiwKICAgICAgICAgICAgICAgIG9sZF92YWx1ZT1mImNvdW50cz17b2xkX2NvdW50c307IG9icz17b2xkX29ic30iLAogICAgICAgICAgICAgICAgbmV3X3ZhbHVlPWYiY291bnRzPXtjb3VudHN9OyBvYnM9e29ic30iLAogICAgICAgICAgICAgICAgcmVhc29uPXJlYXNvbiwKICAgICAgICAgICAgKQogICAgICAgICAgICBjaGFuZ2VzICs9IDEKCiAgICBmb3Igcm93IGluIENyb3NzU2FsZUltcG9ydFJvdy5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIsIG1vbnRoX19ndGU9bWYsIG1vbnRoX19sdGU9bW9udGgpOgogICAgICAgIHByZWZpeCA9IGYiY3Nfe3Jvdy5pZH1fIgogICAgICAgIGRlc3RfcmF3ID0gcG9zdF9kYXRhLmdldChmIntwcmVmaXh9ZGVzdCIpCiAgICAgICAgb3JpZ19yYXcgPSBwb3N0X2RhdGEuZ2V0KGYie3ByZWZpeH1vcmlnIikKICAgICAgICBpZiBkZXN0X3JhdyBpcyBOb25lIGFuZCBvcmlnX3JhdyBpcyBOb25lOgogICAgICAgICAgICBjb250aW51ZQogICAgICAgIGRlc3QgPSBpbnQoZGVzdF9yYXcpIGlmIGRlc3RfcmF3IGVsc2UgTm9uZQogICAgICAgIG9yaWcgPSBpbnQob3JpZ19yYXcpIGlmIG9yaWdfcmF3IGVsc2UgTm9uZQogICAgICAgIG9sZF9kZXN0ID0gcm93LnVuZV9kZXN0aW5hdGlvbl9pZAogICAgICAgIG9sZF9vcmlnID0gcm93LnVuZV9vcmlnaW5faWQKICAgICAgICBpZiByb3cudW5lX2Rlc3RpbmF0aW9uX2lkID09IGRlc3QgYW5kIHJvdy51bmVfb3JpZ2luX2lkID09IG9yaWc6CiAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgcm93LnVuZV9kZXN0aW5hdGlvbl9pZCA9IGRlc3QKICAgICAgICByb3cudW5lX29yaWdpbl9pZCA9IG9yaWcKICAgICAgICByb3cuc2F2ZSh1cGRhdGVfZmllbGRzPVsidW5lX2Rlc3RpbmF0aW9uIiwgInVuZV9vcmlnaW4iLCAidXBkYXRlZF9hdCJdKQogICAgICAgIGxvZ19tYW51YWxfZWRpdCgKICAgICAgICAgICAgdXNlcj11c2VyLAogICAgICAgICAgICB5ZWFyPXJvdy55ZWFyLAogICAgICAgICAgICBtb250aD1yb3cubW9udGgsCiAgICAgICAgICAgIGVudGl0eV90eXBlPUFkbWluTWFudWFsRWRpdExvZy5FTlRJVFlfQ1JPU1NfU0FMRV9ST1csCiAgICAgICAgICAgIGVudGl0eV9pZD1yb3cuaWQsCiAgICAgICAgICAgIGZpZWxkX25hbWU9InVuZV9kZXN0aW5hdGlvbi91bmVfb3JpZ2luIiwKICAgICAgICAgICAgb2xkX3ZhbHVlPWYiZGVzdD17b2xkX2Rlc3R9OyBvcmlnPXtvbGRfb3JpZ30iLAogICAgICAgICAgICBuZXdfdmFsdWU9ZiJkZXN0PXtkZXN0fTsgb3JpZz17b3JpZ30iLAogICAgICAgICAgICByZWFzb249cmVhc29uLAogICAgICAgICkKICAgICAgICBjaGFuZ2VzICs9IDEKCiAgICByZXR1cm4gY2hhbmdlcwoKCkB0cmFuc2FjdGlvbi5hdG9taWMKZGVmIHNhdmVfcGVyaW9kX25vdGUodXNlciwgeWVhcjogaW50LCBtb250aDogaW50LCBwb3N0X2RhdGEsIHJlYXNvbjogc3RyID0gIiIpIC0+IGludDoKICAgIG5vdGUgPSAocG9zdF9kYXRhLmdldCgicGVyaW9kX25vdGUiKSBvciAiIikuc3RyaXAoKQogICAga2V5ID0gX3BlcmlvZF9ub3RlX2tleSh5ZWFyLCBtb250aCkKICAgIHNldHRpbmcsIGNyZWF0ZWQgPSBTeXN0ZW1TZXR0aW5nLm9iamVjdHMuZ2V0X29yX2NyZWF0ZShrZXk9a2V5LCBkZWZhdWx0cz17InZhbHVlX3RleHQiOiBub3RlfSkKICAgIG9sZCA9ICIiIGlmIGNyZWF0ZWQgZWxzZSAoc2V0dGluZy52YWx1ZV90ZXh0IG9yICIiKQogICAgaWYgb2xkICE9IG5vdGU6CiAgICAgICAgc2V0dGluZy52YWx1ZV90ZXh0ID0gbm90ZQogICAgICAgIHNldHRpbmcudXBkYXRlZF9ieSA9IHVzZXIKICAgICAgICBzZXR0aW5nLnNhdmUodXBkYXRlX2ZpZWxkcz1bInZhbHVlX3RleHQiLCAidXBkYXRlZF9ieSIsICJ1cGRhdGVkX2F0Il0pCiAgICAgICAgbG9nX21hbnVhbF9lZGl0KAogICAgICAgICAgICB1c2VyPXVzZXIsCiAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgIGVudGl0eV90eXBlPUFkbWluTWFudWFsRWRpdExvZy5FTlRJVFlfUEVSSU9EX05PVEUsCiAgICAgICAgICAgIGVudGl0eV9pZD1zZXR0aW5nLmlkLAogICAgICAgICAgICBmaWVsZF9uYW1lPSJ2YWx1ZV90ZXh0IiwKICAgICAgICAgICAgb2xkX3ZhbHVlPW9sZCwKICAgICAgICAgICAgbmV3X3ZhbHVlPW5vdGUsCiAgICAgICAgICAgIHJlYXNvbj1yZWFzb24sCiAgICAgICAgKQogICAgICAgIHJldHVybiAxCiAgICByZXR1cm4gMAo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/admin_new_clients_browse.py
PATH_JSON="pgc/admin_new_clients_browse.py"
FILENAME=admin_new_clients_browse.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=351
SIZE_BYTES_UTF8=11731
CONTENT_SHA256=05db1dc568f29aa9341318c27b3dca1f8c74f07bc364df2aaf6045f44d3ba280
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""
Edición browse de clientes nuevos y reasignación de UNE.
"""

from __future__ import annotations

from django.core.files.base import ContentFile
from django.db import transaction

from core.models import Currency, UNE
from imports.models import FileUpload, NewClientImportHeader, NewClientImportRow
from pgc.admin_manual import log_manual_edit
from pgc.admin_period import _sync_clientes_nuevos_metrics_from_rows
from pgc.admin_utils import AdminPeriod, apply_period_range, parse_decimal_or_none
from pgc.models import AdminManualEditLog


BASE_CURRENCIES = (
    ("GTQ", "Quetzal guatemalteco", "Q"),
    ("USD", "Dólar estadounidense", "$"),
)


def ensure_base_currencies() -> list[Currency]:
    """Garantiza GTQ/USD activos (catálogo usado por el browse de clientes)."""
    for code, name, symbol in BASE_CURRENCIES:
        Currency.objects.update_or_create(
            code=code,
            defaults={"name": name, "symbol": symbol, "is_active": True},
        )
    return list(Currency.objects.filter(is_active=True).order_by("code"))


ALLOWED_UNE_CODES = (
    UNE.CODE_FACTORING,
    UNE.CODE_LEASING,
    UNE.CODE_INSURANCE,
    UNE.CODE_INVESTMENT,
)

UNE_SHORT = {
    UNE.CODE_FACTORING: "1·Fa",
    UNE.CODE_LEASING: "2·Le",
    UNE.CODE_INSURANCE: "3·In",
    UNE.CODE_INVESTMENT: "4·Iv",
}


def period_unes():
    return list(
        UNE.objects.filter(is_active=True, code__in=ALLOWED_UNE_CODES).order_by(
            "sort_order", "code"
        )
    )


def une_options_for_template():
    return [
        {
            "id": une.id,
            "code": une.code,
            "name_es": une.name_es,
            "short": UNE_SHORT.get(une.code, une.code[:2]),
        }
        for une in period_unes()
    ]


def ensure_new_client_header(year: int, month: int, user) -> NewClientImportHeader:
    header = NewClientImportHeader.objects.filter(year=year, month=month).first()
    if header:
        return header

    upload = FileUpload(
        uploaded_by=user,
        original_filename=f"manual-clientes-{year}-{month:02d}.tsv",
        file_type_detected=FileUpload.TYPE_NEW_CLIENTS,
        detected_year=year,
        detected_month=month,
        status=FileUpload.STATUS_PARSED_OK,
        parsing_notes="Encabezado creado automáticamente para edición manual de filas.",
        file_format=FileUpload.FORMAT_TSV,
    )
    upload.stored_file.save(
        f"manual-clientes-{year}-{month:02d}.tsv",
        ContentFile(b"# manual new clients\n"),
        save=False,
    )
    upload.save()
    header = NewClientImportHeader.objects.filter(year=year, month=month).first()
    if not header:
        raise ValueError(
            f"No se pudo crear encabezado de clientes nuevos para {year}-{month:02d}."
        )
    return header


def browse_context(period: AdminPeriod) -> dict:
    rows = list(
        apply_period_range(NewClientImportRow.objects.all(), period)
        .select_related("une", "currency", "header")
        .order_by("year", "month", "une__sort_order", "client_name", "operation_code", "id")
    )
    currencies = ensure_base_currencies()
    return {
        "rows": rows,
        "unes": une_options_for_template(),
        "currencies": currencies,
        "header": NewClientImportHeader.objects.filter(
            year=period.year, month=period.month
        ).first(),
        "label": period.label,
        "row_count": len(rows),
        "supports_month_range": True,
        "single_month_ops": False,
    }


def _parse_bool(post_data, key: str) -> bool:
    return post_data.get(key) == "1"


def _parse_int(raw, default=0):
    text = (raw or "").strip()
    if text == "":
        return default
    try:
        return int(text)
    except (TypeError, ValueError):
        return default


def _parse_optional_int(raw):
    text = (raw or "").strip()
    if text == "":
        return None
    try:
        return int(text)
    except (TypeError, ValueError):
        return None


def _allowed_une_ids() -> set[int]:
    return {u.id for u in period_unes()}


def _resolve_currency_id(raw) -> int | None:
    text = (raw or "").strip()
    if not text:
        return None
    try:
        cid = int(text)
    except (TypeError, ValueError):
        return None
    if Currency.objects.filter(id=cid, is_active=True).exists():
        return cid
    return None


@transaction.atomic
def save_browse_rows(user, period: AdminPeriod, post_data, reason: str = "") -> dict:
    """
    Guarda ediciones browse: actualizar, eliminar y alta.
    Retorna dict con counts: updated, deleted, created, metrics_updated.
    """
    allowed_unes = _allowed_une_ids()
    existing = {
        row.id: row
        for row in apply_period_range(NewClientImportRow.objects.all(), period)
    }
    touched_months: set[int] = set()

    deleted = 0
    updated = 0

    delete_ids = set()
    for raw_id in post_data.getlist("delete_ids"):
        try:
            delete_ids.add(int(raw_id))
        except (TypeError, ValueError):
            continue

    for row_id in list(delete_ids):
        row = existing.pop(row_id, None)
        if not row:
            continue
        touched_months.add(row.month)
        log_manual_edit(
            user=user,
            year=row.year,
            month=row.month,
            entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
            entity_id=row.id,
            field_name="delete",
            old_value=f"{row.client_name}|{row.operation_code}|une={row.une_id}",
            new_value="",
            reason=reason or "Eliminación desde browse de clientes nuevos",
        )
        row.delete()
        deleted += 1

    for row_id, row in existing.items():
        prefix = f"row_{row_id}_"
        if f"{prefix}client_name" not in post_data:
            continue

        une_id = _parse_optional_int(post_data.get(f"{prefix}une"))
        if une_id not in allowed_unes:
            raise ValueError(f"UNE inválida en fila {row_id}.")

        new_vals = {
            "client_name": (post_data.get(f"{prefix}client_name") or "").strip(),
            "nit": (post_data.get(f"{prefix}nit") or "").strip(),
            "operation_code": (post_data.get(f"{prefix}operation_code") or "").strip(),
            "previous_contracts": _parse_int(post_data.get(f"{prefix}previous_contracts"), 0),
            "counts_as_new": _parse_bool(post_data, f"{prefix}counts_as_new"),
            "currency_id": _resolve_currency_id(post_data.get(f"{prefix}currency")),
            "amount": parse_decimal_or_none(post_data.get(f"{prefix}amount")),
            "raw_une_value": (post_data.get(f"{prefix}raw_une_value") or "").strip(),
            "observations": (post_data.get(f"{prefix}observations") or "").strip(),
            "une_id": une_id,
            "source_row_number": _parse_optional_int(
                post_data.get(f"{prefix}source_row_number")
            ),
        }

        changed_fields = []
        for field, new_value in new_vals.items():
            old_value = getattr(row, field)
            if old_value != new_value:
                setattr(row, field, new_value)
                changed_fields.append(field)

        if not changed_fields:
            continue

        row.save()
        touched_months.add(row.month)
        log_manual_edit(
            user=user,
            year=row.year,
            month=row.month,
            entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
            entity_id=row.id,
            field_name=",".join(changed_fields),
            old_value="edit",
            new_value=",".join(changed_fields),
            reason=reason or "Edición browse de clientes nuevos",
        )
        updated += 1

    created = 0
    new_client = (post_data.get("new_client_name") or "").strip()
    new_nit = (post_data.get("new_nit") or "").strip()
    new_op = (post_data.get("new_operation_code") or "").strip()
    new_une = _parse_optional_int(post_data.get("new_une"))
    has_new = any([new_client, new_nit, new_op, post_data.get("new_amount")])

    if has_new:
        if new_une not in allowed_unes:
            raise ValueError("Debe elegir UNE válida para el registro nuevo.")
        new_month = _parse_int(post_data.get("new_month"), period.month)
        if new_month < period.month_from or new_month > period.month_to:
            new_month = period.month
        header = ensure_new_client_header(period.year, new_month, user)
        row = NewClientImportRow.objects.create(
            header=header,
            une_id=new_une,
            year=period.year,
            month=new_month,
            client_name=new_client,
            nit=new_nit,
            operation_code=new_op,
            previous_contracts=_parse_int(post_data.get("new_previous_contracts"), 0),
            counts_as_new=_parse_bool(post_data, "new_counts_as_new"),
            currency_id=_resolve_currency_id(post_data.get("new_currency")),
            amount=parse_decimal_or_none(post_data.get("new_amount")),
            raw_une_value=(post_data.get("new_raw_une_value") or "").strip(),
            observations=(post_data.get("new_observations") or "").strip(),
            source_row_number=_parse_optional_int(post_data.get("new_source_row_number")),
        )
        touched_months.add(new_month)
        log_manual_edit(
            user=user,
            year=period.year,
            month=new_month,
            entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
            entity_id=row.id,
            field_name="create",
            old_value="",
            new_value=f"{row.client_name}|{row.operation_code}|une={row.une_id}",
            reason=reason or "Alta desde browse de clientes nuevos",
        )
        created += 1

    metrics_updated = 0
    for m in sorted(touched_months):
        metrics_updated += _sync_clientes_nuevos_metrics_from_rows(period.year, m)

    return {
        "updated": updated,
        "deleted": deleted,
        "created": created,
        "metrics_updated": metrics_updated,
        "total": updated + deleted + created,
    }


@transaction.atomic
def save_une_reassignments(user, period: AdminPeriod, post_data, reason: str = "") -> dict:
    """Solo permite cambiar UNE entre las cuatro UNEs activas del negocio."""
    allowed_unes = _allowed_une_ids()
    une_by_id = {u.id: u for u in period_unes()}
    changed = 0
    touched_months: set[int] = set()

    qs = apply_period_range(NewClientImportRow.objects.all(), period).select_related("une")
    for row in qs:
        raw = post_data.get(f"une_{row.id}")
        if raw is None:
            continue
        new_une_id = _parse_optional_int(raw)
        if new_une_id not in allowed_unes:
            raise ValueError(f"UNE inválida para fila {row.id}.")
        if new_une_id == row.une_id:
            continue

        old_une = row.une
        new_une = une_by_id[new_une_id]
        row.une_id = new_une_id
        row.raw_une_value = new_une.name_es
        row.save(update_fields=["une", "raw_une_value", "updated_at"])
        touched_months.add(row.month)
        log_manual_edit(
            user=user,
            year=row.year,
            month=row.month,
            entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
            entity_id=row.id,
            field_name="une",
            old_value=f"{old_une.code} ({old_une.name_es})",
            new_value=f"{new_une.code} ({new_une.name_es})",
            reason=reason or "Reasignación de UNE",
        )
        changed += 1

    metrics_updated = 0
    for m in sorted(touched_months):
        metrics_updated += _sync_clientes_nuevos_metrics_from_rows(period.year, m)

    return {"changed": changed, "metrics_updated": metrics_updated}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Edición browse de clientes nuevos y reasignación de UNE.
00003|"""
00004|
00005|from __future__ import annotations
00006|
00007|from django.core.files.base import ContentFile
00008|from django.db import transaction
00009|
00010|from core.models import Currency, UNE
00011|from imports.models import FileUpload, NewClientImportHeader, NewClientImportRow
00012|from pgc.admin_manual import log_manual_edit
00013|from pgc.admin_period import _sync_clientes_nuevos_metrics_from_rows
00014|from pgc.admin_utils import AdminPeriod, apply_period_range, parse_decimal_or_none
00015|from pgc.models import AdminManualEditLog
00016|
00017|
00018|BASE_CURRENCIES = (
00019|    ("GTQ", "Quetzal guatemalteco", "Q"),
00020|    ("USD", "Dólar estadounidense", "$"),
00021|)
00022|
00023|
00024|def ensure_base_currencies() -> list[Currency]:
00025|    """Garantiza GTQ/USD activos (catálogo usado por el browse de clientes)."""
00026|    for code, name, symbol in BASE_CURRENCIES:
00027|        Currency.objects.update_or_create(
00028|            code=code,
00029|            defaults={"name": name, "symbol": symbol, "is_active": True},
00030|        )
00031|    return list(Currency.objects.filter(is_active=True).order_by("code"))
00032|
00033|
00034|ALLOWED_UNE_CODES = (
00035|    UNE.CODE_FACTORING,
00036|    UNE.CODE_LEASING,
00037|    UNE.CODE_INSURANCE,
00038|    UNE.CODE_INVESTMENT,
00039|)
00040|
00041|UNE_SHORT = {
00042|    UNE.CODE_FACTORING: "1·Fa",
00043|    UNE.CODE_LEASING: "2·Le",
00044|    UNE.CODE_INSURANCE: "3·In",
00045|    UNE.CODE_INVESTMENT: "4·Iv",
00046|}
00047|
00048|
00049|def period_unes():
00050|    return list(
00051|        UNE.objects.filter(is_active=True, code__in=ALLOWED_UNE_CODES).order_by(
00052|            "sort_order", "code"
00053|        )
00054|    )
00055|
00056|
00057|def une_options_for_template():
00058|    return [
00059|        {
00060|            "id": une.id,
00061|            "code": une.code,
00062|            "name_es": une.name_es,
00063|            "short": UNE_SHORT.get(une.code, une.code[:2]),
00064|        }
00065|        for une in period_unes()
00066|    ]
00067|
00068|
00069|def ensure_new_client_header(year: int, month: int, user) -> NewClientImportHeader:
00070|    header = NewClientImportHeader.objects.filter(year=year, month=month).first()
00071|    if header:
00072|        return header
00073|
00074|    upload = FileUpload(
00075|        uploaded_by=user,
00076|        original_filename=f"manual-clientes-{year}-{month:02d}.tsv",
00077|        file_type_detected=FileUpload.TYPE_NEW_CLIENTS,
00078|        detected_year=year,
00079|        detected_month=month,
00080|        status=FileUpload.STATUS_PARSED_OK,
00081|        parsing_notes="Encabezado creado automáticamente para edición manual de filas.",
00082|        file_format=FileUpload.FORMAT_TSV,
00083|    )
00084|    upload.stored_file.save(
00085|        f"manual-clientes-{year}-{month:02d}.tsv",
00086|        ContentFile(b"# manual new clients\n"),
00087|        save=False,
00088|    )
00089|    upload.save()
00090|    header = NewClientImportHeader.objects.filter(year=year, month=month).first()
00091|    if not header:
00092|        raise ValueError(
00093|            f"No se pudo crear encabezado de clientes nuevos para {year}-{month:02d}."
00094|        )
00095|    return header
00096|
00097|
00098|def browse_context(period: AdminPeriod) -> dict:
00099|    rows = list(
00100|        apply_period_range(NewClientImportRow.objects.all(), period)
00101|        .select_related("une", "currency", "header")
00102|        .order_by("year", "month", "une__sort_order", "client_name", "operation_code", "id")
00103|    )
00104|    currencies = ensure_base_currencies()
00105|    return {
00106|        "rows": rows,
00107|        "unes": une_options_for_template(),
00108|        "currencies": currencies,
00109|        "header": NewClientImportHeader.objects.filter(
00110|            year=period.year, month=period.month
00111|        ).first(),
00112|        "label": period.label,
00113|        "row_count": len(rows),
00114|        "supports_month_range": True,
00115|        "single_month_ops": False,
00116|    }
00117|
00118|
00119|def _parse_bool(post_data, key: str) -> bool:
00120|    return post_data.get(key) == "1"
00121|
00122|
00123|def _parse_int(raw, default=0):
00124|    text = (raw or "").strip()
00125|    if text == "":
00126|        return default
00127|    try:
00128|        return int(text)
00129|    except (TypeError, ValueError):
00130|        return default
00131|
00132|
00133|def _parse_optional_int(raw):
00134|    text = (raw or "").strip()
00135|    if text == "":
00136|        return None
00137|    try:
00138|        return int(text)
00139|    except (TypeError, ValueError):
00140|        return None
00141|
00142|
00143|def _allowed_une_ids() -> set[int]:
00144|    return {u.id for u in period_unes()}
00145|
00146|
00147|def _resolve_currency_id(raw) -> int | None:
00148|    text = (raw or "").strip()
00149|    if not text:
00150|        return None
00151|    try:
00152|        cid = int(text)
00153|    except (TypeError, ValueError):
00154|        return None
00155|    if Currency.objects.filter(id=cid, is_active=True).exists():
00156|        return cid
00157|    return None
00158|
00159|
00160|@transaction.atomic
00161|def save_browse_rows(user, period: AdminPeriod, post_data, reason: str = "") -> dict:
00162|    """
00163|    Guarda ediciones browse: actualizar, eliminar y alta.
00164|    Retorna dict con counts: updated, deleted, created, metrics_updated.
00165|    """
00166|    allowed_unes = _allowed_une_ids()
00167|    existing = {
00168|        row.id: row
00169|        for row in apply_period_range(NewClientImportRow.objects.all(), period)
00170|    }
00171|    touched_months: set[int] = set()
00172|
00173|    deleted = 0
00174|    updated = 0
00175|
00176|    delete_ids = set()
00177|    for raw_id in post_data.getlist("delete_ids"):
00178|        try:
00179|            delete_ids.add(int(raw_id))
00180|        except (TypeError, ValueError):
00181|            continue
00182|
00183|    for row_id in list(delete_ids):
00184|        row = existing.pop(row_id, None)
00185|        if not row:
00186|            continue
00187|        touched_months.add(row.month)
00188|        log_manual_edit(
00189|            user=user,
00190|            year=row.year,
00191|            month=row.month,
00192|            entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
00193|            entity_id=row.id,
00194|            field_name="delete",
00195|            old_value=f"{row.client_name}|{row.operation_code}|une={row.une_id}",
00196|            new_value="",
00197|            reason=reason or "Eliminación desde browse de clientes nuevos",
00198|        )
00199|        row.delete()
00200|        deleted += 1
00201|
00202|    for row_id, row in existing.items():
00203|        prefix = f"row_{row_id}_"
00204|        if f"{prefix}client_name" not in post_data:
00205|            continue
00206|
00207|        une_id = _parse_optional_int(post_data.get(f"{prefix}une"))
00208|        if une_id not in allowed_unes:
00209|            raise ValueError(f"UNE inválida en fila {row_id}.")
00210|
00211|        new_vals = {
00212|            "client_name": (post_data.get(f"{prefix}client_name") or "").strip(),
00213|            "nit": (post_data.get(f"{prefix}nit") or "").strip(),
00214|            "operation_code": (post_data.get(f"{prefix}operation_code") or "").strip(),
00215|            "previous_contracts": _parse_int(post_data.get(f"{prefix}previous_contracts"), 0),
00216|            "counts_as_new": _parse_bool(post_data, f"{prefix}counts_as_new"),
00217|            "currency_id": _resolve_currency_id(post_data.get(f"{prefix}currency")),
00218|            "amount": parse_decimal_or_none(post_data.get(f"{prefix}amount")),
00219|            "raw_une_value": (post_data.get(f"{prefix}raw_une_value") or "").strip(),
00220|            "observations": (post_data.get(f"{prefix}observations") or "").strip(),
00221|            "une_id": une_id,
00222|            "source_row_number": _parse_optional_int(
00223|                post_data.get(f"{prefix}source_row_number")
00224|            ),
00225|        }
00226|
00227|        changed_fields = []
00228|        for field, new_value in new_vals.items():
00229|            old_value = getattr(row, field)
00230|            if old_value != new_value:
00231|                setattr(row, field, new_value)
00232|                changed_fields.append(field)
00233|
00234|        if not changed_fields:
00235|            continue
00236|
00237|        row.save()
00238|        touched_months.add(row.month)
00239|        log_manual_edit(
00240|            user=user,
00241|            year=row.year,
00242|            month=row.month,
00243|            entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
00244|            entity_id=row.id,
00245|            field_name=",".join(changed_fields),
00246|            old_value="edit",
00247|            new_value=",".join(changed_fields),
00248|            reason=reason or "Edición browse de clientes nuevos",
00249|        )
00250|        updated += 1
00251|
00252|    created = 0
00253|    new_client = (post_data.get("new_client_name") or "").strip()
00254|    new_nit = (post_data.get("new_nit") or "").strip()
00255|    new_op = (post_data.get("new_operation_code") or "").strip()
00256|    new_une = _parse_optional_int(post_data.get("new_une"))
00257|    has_new = any([new_client, new_nit, new_op, post_data.get("new_amount")])
00258|
00259|    if has_new:
00260|        if new_une not in allowed_unes:
00261|            raise ValueError("Debe elegir UNE válida para el registro nuevo.")
00262|        new_month = _parse_int(post_data.get("new_month"), period.month)
00263|        if new_month < period.month_from or new_month > period.month_to:
00264|            new_month = period.month
00265|        header = ensure_new_client_header(period.year, new_month, user)
00266|        row = NewClientImportRow.objects.create(
00267|            header=header,
00268|            une_id=new_une,
00269|            year=period.year,
00270|            month=new_month,
00271|            client_name=new_client,
00272|            nit=new_nit,
00273|            operation_code=new_op,
00274|            previous_contracts=_parse_int(post_data.get("new_previous_contracts"), 0),
00275|            counts_as_new=_parse_bool(post_data, "new_counts_as_new"),
00276|            currency_id=_resolve_currency_id(post_data.get("new_currency")),
00277|            amount=parse_decimal_or_none(post_data.get("new_amount")),
00278|            raw_une_value=(post_data.get("new_raw_une_value") or "").strip(),
00279|            observations=(post_data.get("new_observations") or "").strip(),
00280|            source_row_number=_parse_optional_int(post_data.get("new_source_row_number")),
00281|        )
00282|        touched_months.add(new_month)
00283|        log_manual_edit(
00284|            user=user,
00285|            year=period.year,
00286|            month=new_month,
00287|            entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
00288|            entity_id=row.id,
00289|            field_name="create",
00290|            old_value="",
00291|            new_value=f"{row.client_name}|{row.operation_code}|une={row.une_id}",
00292|            reason=reason or "Alta desde browse de clientes nuevos",
00293|        )
00294|        created += 1
00295|
00296|    metrics_updated = 0
00297|    for m in sorted(touched_months):
00298|        metrics_updated += _sync_clientes_nuevos_metrics_from_rows(period.year, m)
00299|
00300|    return {
00301|        "updated": updated,
00302|        "deleted": deleted,
00303|        "created": created,
00304|        "metrics_updated": metrics_updated,
00305|        "total": updated + deleted + created,
00306|    }
00307|
00308|
00309|@transaction.atomic
00310|def save_une_reassignments(user, period: AdminPeriod, post_data, reason: str = "") -> dict:
00311|    """Solo permite cambiar UNE entre las cuatro UNEs activas del negocio."""
00312|    allowed_unes = _allowed_une_ids()
00313|    une_by_id = {u.id: u for u in period_unes()}
00314|    changed = 0
00315|    touched_months: set[int] = set()
00316|
00317|    qs = apply_period_range(NewClientImportRow.objects.all(), period).select_related("une")
00318|    for row in qs:
00319|        raw = post_data.get(f"une_{row.id}")
00320|        if raw is None:
00321|            continue
00322|        new_une_id = _parse_optional_int(raw)
00323|        if new_une_id not in allowed_unes:
00324|            raise ValueError(f"UNE inválida para fila {row.id}.")
00325|        if new_une_id == row.une_id:
00326|            continue
00327|
00328|        old_une = row.une
00329|        new_une = une_by_id[new_une_id]
00330|        row.une_id = new_une_id
00331|        row.raw_une_value = new_une.name_es
00332|        row.save(update_fields=["une", "raw_une_value", "updated_at"])
00333|        touched_months.add(row.month)
00334|        log_manual_edit(
00335|            user=user,
00336|            year=row.year,
00337|            month=row.month,
00338|            entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
00339|            entity_id=row.id,
00340|            field_name="une",
00341|            old_value=f"{old_une.code} ({old_une.name_es})",
00342|            new_value=f"{new_une.code} ({new_une.name_es})",
00343|            reason=reason or "Reasignación de UNE",
00344|        )
00345|        changed += 1
00346|
00347|    metrics_updated = 0
00348|    for m in sorted(touched_months):
00349|        metrics_updated += _sync_clientes_nuevos_metrics_from_rows(period.year, m)
00350|
00351|    return {"changed": changed, "metrics_updated": metrics_updated}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiCkVkaWNpw7NuIGJyb3dzZSBkZSBjbGllbnRlcyBudWV2b3MgeSByZWFzaWduYWNpw7NuIGRlIFVORS4KIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgpmcm9tIGRqYW5nby5jb3JlLmZpbGVzLmJhc2UgaW1wb3J0IENvbnRlbnRGaWxlCmZyb20gZGphbmdvLmRiIGltcG9ydCB0cmFuc2FjdGlvbgoKZnJvbSBjb3JlLm1vZGVscyBpbXBvcnQgQ3VycmVuY3ksIFVORQpmcm9tIGltcG9ydHMubW9kZWxzIGltcG9ydCBGaWxlVXBsb2FkLCBOZXdDbGllbnRJbXBvcnRIZWFkZXIsIE5ld0NsaWVudEltcG9ydFJvdwpmcm9tIHBnYy5hZG1pbl9tYW51YWwgaW1wb3J0IGxvZ19tYW51YWxfZWRpdApmcm9tIHBnYy5hZG1pbl9wZXJpb2QgaW1wb3J0IF9zeW5jX2NsaWVudGVzX251ZXZvc19tZXRyaWNzX2Zyb21fcm93cwpmcm9tIHBnYy5hZG1pbl91dGlscyBpbXBvcnQgQWRtaW5QZXJpb2QsIGFwcGx5X3BlcmlvZF9yYW5nZSwgcGFyc2VfZGVjaW1hbF9vcl9ub25lCmZyb20gcGdjLm1vZGVscyBpbXBvcnQgQWRtaW5NYW51YWxFZGl0TG9nCgoKQkFTRV9DVVJSRU5DSUVTID0gKAogICAgKCJHVFEiLCAiUXVldHphbCBndWF0ZW1hbHRlY28iLCAiUSIpLAogICAgKCJVU0QiLCAiRMOzbGFyIGVzdGFkb3VuaWRlbnNlIiwgIiQiKSwKKQoKCmRlZiBlbnN1cmVfYmFzZV9jdXJyZW5jaWVzKCkgLT4gbGlzdFtDdXJyZW5jeV06CiAgICAiIiJHYXJhbnRpemEgR1RRL1VTRCBhY3Rpdm9zIChjYXTDoWxvZ28gdXNhZG8gcG9yIGVsIGJyb3dzZSBkZSBjbGllbnRlcykuIiIiCiAgICBmb3IgY29kZSwgbmFtZSwgc3ltYm9sIGluIEJBU0VfQ1VSUkVOQ0lFUzoKICAgICAgICBDdXJyZW5jeS5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgIGNvZGU9Y29kZSwKICAgICAgICAgICAgZGVmYXVsdHM9eyJuYW1lIjogbmFtZSwgInN5bWJvbCI6IHN5bWJvbCwgImlzX2FjdGl2ZSI6IFRydWV9LAogICAgICAgICkKICAgIHJldHVybiBsaXN0KEN1cnJlbmN5Lm9iamVjdHMuZmlsdGVyKGlzX2FjdGl2ZT1UcnVlKS5vcmRlcl9ieSgiY29kZSIpKQoKCkFMTE9XRURfVU5FX0NPREVTID0gKAogICAgVU5FLkNPREVfRkFDVE9SSU5HLAogICAgVU5FLkNPREVfTEVBU0lORywKICAgIFVORS5DT0RFX0lOU1VSQU5DRSwKICAgIFVORS5DT0RFX0lOVkVTVE1FTlQsCikKClVORV9TSE9SVCA9IHsKICAgIFVORS5DT0RFX0ZBQ1RPUklORzogIjHCt0ZhIiwKICAgIFVORS5DT0RFX0xFQVNJTkc6ICIywrdMZSIsCiAgICBVTkUuQ09ERV9JTlNVUkFOQ0U6ICIzwrdJbiIsCiAgICBVTkUuQ09ERV9JTlZFU1RNRU5UOiAiNMK3SXYiLAp9CgoKZGVmIHBlcmlvZF91bmVzKCk6CiAgICByZXR1cm4gbGlzdCgKICAgICAgICBVTkUub2JqZWN0cy5maWx0ZXIoaXNfYWN0aXZlPVRydWUsIGNvZGVfX2luPUFMTE9XRURfVU5FX0NPREVTKS5vcmRlcl9ieSgKICAgICAgICAgICAgInNvcnRfb3JkZXIiLCAiY29kZSIKICAgICAgICApCiAgICApCgoKZGVmIHVuZV9vcHRpb25zX2Zvcl90ZW1wbGF0ZSgpOgogICAgcmV0dXJuIFsKICAgICAgICB7CiAgICAgICAgICAgICJpZCI6IHVuZS5pZCwKICAgICAgICAgICAgImNvZGUiOiB1bmUuY29kZSwKICAgICAgICAgICAgIm5hbWVfZXMiOiB1bmUubmFtZV9lcywKICAgICAgICAgICAgInNob3J0IjogVU5FX1NIT1JULmdldCh1bmUuY29kZSwgdW5lLmNvZGVbOjJdKSwKICAgICAgICB9CiAgICAgICAgZm9yIHVuZSBpbiBwZXJpb2RfdW5lcygpCiAgICBdCgoKZGVmIGVuc3VyZV9uZXdfY2xpZW50X2hlYWRlcih5ZWFyOiBpbnQsIG1vbnRoOiBpbnQsIHVzZXIpIC0+IE5ld0NsaWVudEltcG9ydEhlYWRlcjoKICAgIGhlYWRlciA9IE5ld0NsaWVudEltcG9ydEhlYWRlci5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKS5maXJzdCgpCiAgICBpZiBoZWFkZXI6CiAgICAgICAgcmV0dXJuIGhlYWRlcgoKICAgIHVwbG9hZCA9IEZpbGVVcGxvYWQoCiAgICAgICAgdXBsb2FkZWRfYnk9dXNlciwKICAgICAgICBvcmlnaW5hbF9maWxlbmFtZT1mIm1hbnVhbC1jbGllbnRlcy17eWVhcn0te21vbnRoOjAyZH0udHN2IiwKICAgICAgICBmaWxlX3R5cGVfZGV0ZWN0ZWQ9RmlsZVVwbG9hZC5UWVBFX05FV19DTElFTlRTLAogICAgICAgIGRldGVjdGVkX3llYXI9eWVhciwKICAgICAgICBkZXRlY3RlZF9tb250aD1tb250aCwKICAgICAgICBzdGF0dXM9RmlsZVVwbG9hZC5TVEFUVVNfUEFSU0VEX09LLAogICAgICAgIHBhcnNpbmdfbm90ZXM9IkVuY2FiZXphZG8gY3JlYWRvIGF1dG9tw6F0aWNhbWVudGUgcGFyYSBlZGljacOzbiBtYW51YWwgZGUgZmlsYXMuIiwKICAgICAgICBmaWxlX2Zvcm1hdD1GaWxlVXBsb2FkLkZPUk1BVF9UU1YsCiAgICApCiAgICB1cGxvYWQuc3RvcmVkX2ZpbGUuc2F2ZSgKICAgICAgICBmIm1hbnVhbC1jbGllbnRlcy17eWVhcn0te21vbnRoOjAyZH0udHN2IiwKICAgICAgICBDb250ZW50RmlsZShiIiMgbWFudWFsIG5ldyBjbGllbnRzXG4iKSwKICAgICAgICBzYXZlPUZhbHNlLAogICAgKQogICAgdXBsb2FkLnNhdmUoKQogICAgaGVhZGVyID0gTmV3Q2xpZW50SW1wb3J0SGVhZGVyLm9iamVjdHMuZmlsdGVyKHllYXI9eWVhciwgbW9udGg9bW9udGgpLmZpcnN0KCkKICAgIGlmIG5vdCBoZWFkZXI6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcigKICAgICAgICAgICAgZiJObyBzZSBwdWRvIGNyZWFyIGVuY2FiZXphZG8gZGUgY2xpZW50ZXMgbnVldm9zIHBhcmEge3llYXJ9LXttb250aDowMmR9LiIKICAgICAgICApCiAgICByZXR1cm4gaGVhZGVyCgoKZGVmIGJyb3dzZV9jb250ZXh0KHBlcmlvZDogQWRtaW5QZXJpb2QpIC0+IGRpY3Q6CiAgICByb3dzID0gbGlzdCgKICAgICAgICBhcHBseV9wZXJpb2RfcmFuZ2UoTmV3Q2xpZW50SW1wb3J0Um93Lm9iamVjdHMuYWxsKCksIHBlcmlvZCkKICAgICAgICAuc2VsZWN0X3JlbGF0ZWQoInVuZSIsICJjdXJyZW5jeSIsICJoZWFkZXIiKQogICAgICAgIC5vcmRlcl9ieSgieWVhciIsICJtb250aCIsICJ1bmVfX3NvcnRfb3JkZXIiLCAiY2xpZW50X25hbWUiLCAib3BlcmF0aW9uX2NvZGUiLCAiaWQiKQogICAgKQogICAgY3VycmVuY2llcyA9IGVuc3VyZV9iYXNlX2N1cnJlbmNpZXMoKQogICAgcmV0dXJuIHsKICAgICAgICAicm93cyI6IHJvd3MsCiAgICAgICAgInVuZXMiOiB1bmVfb3B0aW9uc19mb3JfdGVtcGxhdGUoKSwKICAgICAgICAiY3VycmVuY2llcyI6IGN1cnJlbmNpZXMsCiAgICAgICAgImhlYWRlciI6IE5ld0NsaWVudEltcG9ydEhlYWRlci5vYmplY3RzLmZpbHRlcigKICAgICAgICAgICAgeWVhcj1wZXJpb2QueWVhciwgbW9udGg9cGVyaW9kLm1vbnRoCiAgICAgICAgKS5maXJzdCgpLAogICAgICAgICJsYWJlbCI6IHBlcmlvZC5sYWJlbCwKICAgICAgICAicm93X2NvdW50IjogbGVuKHJvd3MpLAogICAgICAgICJzdXBwb3J0c19tb250aF9yYW5nZSI6IFRydWUsCiAgICAgICAgInNpbmdsZV9tb250aF9vcHMiOiBGYWxzZSwKICAgIH0KCgpkZWYgX3BhcnNlX2Jvb2wocG9zdF9kYXRhLCBrZXk6IHN0cikgLT4gYm9vbDoKICAgIHJldHVybiBwb3N0X2RhdGEuZ2V0KGtleSkgPT0gIjEiCgoKZGVmIF9wYXJzZV9pbnQocmF3LCBkZWZhdWx0PTApOgogICAgdGV4dCA9IChyYXcgb3IgIiIpLnN0cmlwKCkKICAgIGlmIHRleHQgPT0gIiI6CiAgICAgICAgcmV0dXJuIGRlZmF1bHQKICAgIHRyeToKICAgICAgICByZXR1cm4gaW50KHRleHQpCiAgICBleGNlcHQgKFR5cGVFcnJvciwgVmFsdWVFcnJvcik6CiAgICAgICAgcmV0dXJuIGRlZmF1bHQKCgpkZWYgX3BhcnNlX29wdGlvbmFsX2ludChyYXcpOgogICAgdGV4dCA9IChyYXcgb3IgIiIpLnN0cmlwKCkKICAgIGlmIHRleHQgPT0gIiI6CiAgICAgICAgcmV0dXJuIE5vbmUKICAgIHRyeToKICAgICAgICByZXR1cm4gaW50KHRleHQpCiAgICBleGNlcHQgKFR5cGVFcnJvciwgVmFsdWVFcnJvcik6CiAgICAgICAgcmV0dXJuIE5vbmUKCgpkZWYgX2FsbG93ZWRfdW5lX2lkcygpIC0+IHNldFtpbnRdOgogICAgcmV0dXJuIHt1LmlkIGZvciB1IGluIHBlcmlvZF91bmVzKCl9CgoKZGVmIF9yZXNvbHZlX2N1cnJlbmN5X2lkKHJhdykgLT4gaW50IHwgTm9uZToKICAgIHRleHQgPSAocmF3IG9yICIiKS5zdHJpcCgpCiAgICBpZiBub3QgdGV4dDoKICAgICAgICByZXR1cm4gTm9uZQogICAgdHJ5OgogICAgICAgIGNpZCA9IGludCh0ZXh0KQogICAgZXhjZXB0IChUeXBlRXJyb3IsIFZhbHVlRXJyb3IpOgogICAgICAgIHJldHVybiBOb25lCiAgICBpZiBDdXJyZW5jeS5vYmplY3RzLmZpbHRlcihpZD1jaWQsIGlzX2FjdGl2ZT1UcnVlKS5leGlzdHMoKToKICAgICAgICByZXR1cm4gY2lkCiAgICByZXR1cm4gTm9uZQoKCkB0cmFuc2FjdGlvbi5hdG9taWMKZGVmIHNhdmVfYnJvd3NlX3Jvd3ModXNlciwgcGVyaW9kOiBBZG1pblBlcmlvZCwgcG9zdF9kYXRhLCByZWFzb246IHN0ciA9ICIiKSAtPiBkaWN0OgogICAgIiIiCiAgICBHdWFyZGEgZWRpY2lvbmVzIGJyb3dzZTogYWN0dWFsaXphciwgZWxpbWluYXIgeSBhbHRhLgogICAgUmV0b3JuYSBkaWN0IGNvbiBjb3VudHM6IHVwZGF0ZWQsIGRlbGV0ZWQsIGNyZWF0ZWQsIG1ldHJpY3NfdXBkYXRlZC4KICAgICIiIgogICAgYWxsb3dlZF91bmVzID0gX2FsbG93ZWRfdW5lX2lkcygpCiAgICBleGlzdGluZyA9IHsKICAgICAgICByb3cuaWQ6IHJvdwogICAgICAgIGZvciByb3cgaW4gYXBwbHlfcGVyaW9kX3JhbmdlKE5ld0NsaWVudEltcG9ydFJvdy5vYmplY3RzLmFsbCgpLCBwZXJpb2QpCiAgICB9CiAgICB0b3VjaGVkX21vbnRoczogc2V0W2ludF0gPSBzZXQoKQoKICAgIGRlbGV0ZWQgPSAwCiAgICB1cGRhdGVkID0gMAoKICAgIGRlbGV0ZV9pZHMgPSBzZXQoKQogICAgZm9yIHJhd19pZCBpbiBwb3N0X2RhdGEuZ2V0bGlzdCgiZGVsZXRlX2lkcyIpOgogICAgICAgIHRyeToKICAgICAgICAgICAgZGVsZXRlX2lkcy5hZGQoaW50KHJhd19pZCkpCiAgICAgICAgZXhjZXB0IChUeXBlRXJyb3IsIFZhbHVlRXJyb3IpOgogICAgICAgICAgICBjb250aW51ZQoKICAgIGZvciByb3dfaWQgaW4gbGlzdChkZWxldGVfaWRzKToKICAgICAgICByb3cgPSBleGlzdGluZy5wb3Aocm93X2lkLCBOb25lKQogICAgICAgIGlmIG5vdCByb3c6CiAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgdG91Y2hlZF9tb250aHMuYWRkKHJvdy5tb250aCkKICAgICAgICBsb2dfbWFudWFsX2VkaXQoCiAgICAgICAgICAgIHVzZXI9dXNlciwKICAgICAgICAgICAgeWVhcj1yb3cueWVhciwKICAgICAgICAgICAgbW9udGg9cm93Lm1vbnRoLAogICAgICAgICAgICBlbnRpdHlfdHlwZT1BZG1pbk1hbnVhbEVkaXRMb2cuRU5USVRZX05FV19DTElFTlRfUk9XLAogICAgICAgICAgICBlbnRpdHlfaWQ9cm93LmlkLAogICAgICAgICAgICBmaWVsZF9uYW1lPSJkZWxldGUiLAogICAgICAgICAgICBvbGRfdmFsdWU9ZiJ7cm93LmNsaWVudF9uYW1lfXx7cm93Lm9wZXJhdGlvbl9jb2RlfXx1bmU9e3Jvdy51bmVfaWR9IiwKICAgICAgICAgICAgbmV3X3ZhbHVlPSIiLAogICAgICAgICAgICByZWFzb249cmVhc29uIG9yICJFbGltaW5hY2nDs24gZGVzZGUgYnJvd3NlIGRlIGNsaWVudGVzIG51ZXZvcyIsCiAgICAgICAgKQogICAgICAgIHJvdy5kZWxldGUoKQogICAgICAgIGRlbGV0ZWQgKz0gMQoKICAgIGZvciByb3dfaWQsIHJvdyBpbiBleGlzdGluZy5pdGVtcygpOgogICAgICAgIHByZWZpeCA9IGYicm93X3tyb3dfaWR9XyIKICAgICAgICBpZiBmIntwcmVmaXh9Y2xpZW50X25hbWUiIG5vdCBpbiBwb3N0X2RhdGE6CiAgICAgICAgICAgIGNvbnRpbnVlCgogICAgICAgIHVuZV9pZCA9IF9wYXJzZV9vcHRpb25hbF9pbnQocG9zdF9kYXRhLmdldChmIntwcmVmaXh9dW5lIikpCiAgICAgICAgaWYgdW5lX2lkIG5vdCBpbiBhbGxvd2VkX3VuZXM6CiAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJVTkUgaW52w6FsaWRhIGVuIGZpbGEge3Jvd19pZH0uIikKCiAgICAgICAgbmV3X3ZhbHMgPSB7CiAgICAgICAgICAgICJjbGllbnRfbmFtZSI6IChwb3N0X2RhdGEuZ2V0KGYie3ByZWZpeH1jbGllbnRfbmFtZSIpIG9yICIiKS5zdHJpcCgpLAogICAgICAgICAgICAibml0IjogKHBvc3RfZGF0YS5nZXQoZiJ7cHJlZml4fW5pdCIpIG9yICIiKS5zdHJpcCgpLAogICAgICAgICAgICAib3BlcmF0aW9uX2NvZGUiOiAocG9zdF9kYXRhLmdldChmIntwcmVmaXh9b3BlcmF0aW9uX2NvZGUiKSBvciAiIikuc3RyaXAoKSwKICAgICAgICAgICAgInByZXZpb3VzX2NvbnRyYWN0cyI6IF9wYXJzZV9pbnQocG9zdF9kYXRhLmdldChmIntwcmVmaXh9cHJldmlvdXNfY29udHJhY3RzIiksIDApLAogICAgICAgICAgICAiY291bnRzX2FzX25ldyI6IF9wYXJzZV9ib29sKHBvc3RfZGF0YSwgZiJ7cHJlZml4fWNvdW50c19hc19uZXciKSwKICAgICAgICAgICAgImN1cnJlbmN5X2lkIjogX3Jlc29sdmVfY3VycmVuY3lfaWQocG9zdF9kYXRhLmdldChmIntwcmVmaXh9Y3VycmVuY3kiKSksCiAgICAgICAgICAgICJhbW91bnQiOiBwYXJzZV9kZWNpbWFsX29yX25vbmUocG9zdF9kYXRhLmdldChmIntwcmVmaXh9YW1vdW50IikpLAogICAgICAgICAgICAicmF3X3VuZV92YWx1ZSI6IChwb3N0X2RhdGEuZ2V0KGYie3ByZWZpeH1yYXdfdW5lX3ZhbHVlIikgb3IgIiIpLnN0cmlwKCksCiAgICAgICAgICAgICJvYnNlcnZhdGlvbnMiOiAocG9zdF9kYXRhLmdldChmIntwcmVmaXh9b2JzZXJ2YXRpb25zIikgb3IgIiIpLnN0cmlwKCksCiAgICAgICAgICAgICJ1bmVfaWQiOiB1bmVfaWQsCiAgICAgICAgICAgICJzb3VyY2Vfcm93X251bWJlciI6IF9wYXJzZV9vcHRpb25hbF9pbnQoCiAgICAgICAgICAgICAgICBwb3N0X2RhdGEuZ2V0KGYie3ByZWZpeH1zb3VyY2Vfcm93X251bWJlciIpCiAgICAgICAgICAgICksCiAgICAgICAgfQoKICAgICAgICBjaGFuZ2VkX2ZpZWxkcyA9IFtdCiAgICAgICAgZm9yIGZpZWxkLCBuZXdfdmFsdWUgaW4gbmV3X3ZhbHMuaXRlbXMoKToKICAgICAgICAgICAgb2xkX3ZhbHVlID0gZ2V0YXR0cihyb3csIGZpZWxkKQogICAgICAgICAgICBpZiBvbGRfdmFsdWUgIT0gbmV3X3ZhbHVlOgogICAgICAgICAgICAgICAgc2V0YXR0cihyb3csIGZpZWxkLCBuZXdfdmFsdWUpCiAgICAgICAgICAgICAgICBjaGFuZ2VkX2ZpZWxkcy5hcHBlbmQoZmllbGQpCgogICAgICAgIGlmIG5vdCBjaGFuZ2VkX2ZpZWxkczoKICAgICAgICAgICAgY29udGludWUKCiAgICAgICAgcm93LnNhdmUoKQogICAgICAgIHRvdWNoZWRfbW9udGhzLmFkZChyb3cubW9udGgpCiAgICAgICAgbG9nX21hbnVhbF9lZGl0KAogICAgICAgICAgICB1c2VyPXVzZXIsCiAgICAgICAgICAgIHllYXI9cm93LnllYXIsCiAgICAgICAgICAgIG1vbnRoPXJvdy5tb250aCwKICAgICAgICAgICAgZW50aXR5X3R5cGU9QWRtaW5NYW51YWxFZGl0TG9nLkVOVElUWV9ORVdfQ0xJRU5UX1JPVywKICAgICAgICAgICAgZW50aXR5X2lkPXJvdy5pZCwKICAgICAgICAgICAgZmllbGRfbmFtZT0iLCIuam9pbihjaGFuZ2VkX2ZpZWxkcyksCiAgICAgICAgICAgIG9sZF92YWx1ZT0iZWRpdCIsCiAgICAgICAgICAgIG5ld192YWx1ZT0iLCIuam9pbihjaGFuZ2VkX2ZpZWxkcyksCiAgICAgICAgICAgIHJlYXNvbj1yZWFzb24gb3IgIkVkaWNpw7NuIGJyb3dzZSBkZSBjbGllbnRlcyBudWV2b3MiLAogICAgICAgICkKICAgICAgICB1cGRhdGVkICs9IDEKCiAgICBjcmVhdGVkID0gMAogICAgbmV3X2NsaWVudCA9IChwb3N0X2RhdGEuZ2V0KCJuZXdfY2xpZW50X25hbWUiKSBvciAiIikuc3RyaXAoKQogICAgbmV3X25pdCA9IChwb3N0X2RhdGEuZ2V0KCJuZXdfbml0Iikgb3IgIiIpLnN0cmlwKCkKICAgIG5ld19vcCA9IChwb3N0X2RhdGEuZ2V0KCJuZXdfb3BlcmF0aW9uX2NvZGUiKSBvciAiIikuc3RyaXAoKQogICAgbmV3X3VuZSA9IF9wYXJzZV9vcHRpb25hbF9pbnQocG9zdF9kYXRhLmdldCgibmV3X3VuZSIpKQogICAgaGFzX25ldyA9IGFueShbbmV3X2NsaWVudCwgbmV3X25pdCwgbmV3X29wLCBwb3N0X2RhdGEuZ2V0KCJuZXdfYW1vdW50IildKQoKICAgIGlmIGhhc19uZXc6CiAgICAgICAgaWYgbmV3X3VuZSBub3QgaW4gYWxsb3dlZF91bmVzOgogICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJEZWJlIGVsZWdpciBVTkUgdsOhbGlkYSBwYXJhIGVsIHJlZ2lzdHJvIG51ZXZvLiIpCiAgICAgICAgbmV3X21vbnRoID0gX3BhcnNlX2ludChwb3N0X2RhdGEuZ2V0KCJuZXdfbW9udGgiKSwgcGVyaW9kLm1vbnRoKQogICAgICAgIGlmIG5ld19tb250aCA8IHBlcmlvZC5tb250aF9mcm9tIG9yIG5ld19tb250aCA+IHBlcmlvZC5tb250aF90bzoKICAgICAgICAgICAgbmV3X21vbnRoID0gcGVyaW9kLm1vbnRoCiAgICAgICAgaGVhZGVyID0gZW5zdXJlX25ld19jbGllbnRfaGVhZGVyKHBlcmlvZC55ZWFyLCBuZXdfbW9udGgsIHVzZXIpCiAgICAgICAgcm93ID0gTmV3Q2xpZW50SW1wb3J0Um93Lm9iamVjdHMuY3JlYXRlKAogICAgICAgICAgICBoZWFkZXI9aGVhZGVyLAogICAgICAgICAgICB1bmVfaWQ9bmV3X3VuZSwKICAgICAgICAgICAgeWVhcj1wZXJpb2QueWVhciwKICAgICAgICAgICAgbW9udGg9bmV3X21vbnRoLAogICAgICAgICAgICBjbGllbnRfbmFtZT1uZXdfY2xpZW50LAogICAgICAgICAgICBuaXQ9bmV3X25pdCwKICAgICAgICAgICAgb3BlcmF0aW9uX2NvZGU9bmV3X29wLAogICAgICAgICAgICBwcmV2aW91c19jb250cmFjdHM9X3BhcnNlX2ludChwb3N0X2RhdGEuZ2V0KCJuZXdfcHJldmlvdXNfY29udHJhY3RzIiksIDApLAogICAgICAgICAgICBjb3VudHNfYXNfbmV3PV9wYXJzZV9ib29sKHBvc3RfZGF0YSwgIm5ld19jb3VudHNfYXNfbmV3IiksCiAgICAgICAgICAgIGN1cnJlbmN5X2lkPV9yZXNvbHZlX2N1cnJlbmN5X2lkKHBvc3RfZGF0YS5nZXQoIm5ld19jdXJyZW5jeSIpKSwKICAgICAgICAgICAgYW1vdW50PXBhcnNlX2RlY2ltYWxfb3Jfbm9uZShwb3N0X2RhdGEuZ2V0KCJuZXdfYW1vdW50IikpLAogICAgICAgICAgICByYXdfdW5lX3ZhbHVlPShwb3N0X2RhdGEuZ2V0KCJuZXdfcmF3X3VuZV92YWx1ZSIpIG9yICIiKS5zdHJpcCgpLAogICAgICAgICAgICBvYnNlcnZhdGlvbnM9KHBvc3RfZGF0YS5nZXQoIm5ld19vYnNlcnZhdGlvbnMiKSBvciAiIikuc3RyaXAoKSwKICAgICAgICAgICAgc291cmNlX3Jvd19udW1iZXI9X3BhcnNlX29wdGlvbmFsX2ludChwb3N0X2RhdGEuZ2V0KCJuZXdfc291cmNlX3Jvd19udW1iZXIiKSksCiAgICAgICAgKQogICAgICAgIHRvdWNoZWRfbW9udGhzLmFkZChuZXdfbW9udGgpCiAgICAgICAgbG9nX21hbnVhbF9lZGl0KAogICAgICAgICAgICB1c2VyPXVzZXIsCiAgICAgICAgICAgIHllYXI9cGVyaW9kLnllYXIsCiAgICAgICAgICAgIG1vbnRoPW5ld19tb250aCwKICAgICAgICAgICAgZW50aXR5X3R5cGU9QWRtaW5NYW51YWxFZGl0TG9nLkVOVElUWV9ORVdfQ0xJRU5UX1JPVywKICAgICAgICAgICAgZW50aXR5X2lkPXJvdy5pZCwKICAgICAgICAgICAgZmllbGRfbmFtZT0iY3JlYXRlIiwKICAgICAgICAgICAgb2xkX3ZhbHVlPSIiLAogICAgICAgICAgICBuZXdfdmFsdWU9ZiJ7cm93LmNsaWVudF9uYW1lfXx7cm93Lm9wZXJhdGlvbl9jb2RlfXx1bmU9e3Jvdy51bmVfaWR9IiwKICAgICAgICAgICAgcmVhc29uPXJlYXNvbiBvciAiQWx0YSBkZXNkZSBicm93c2UgZGUgY2xpZW50ZXMgbnVldm9zIiwKICAgICAgICApCiAgICAgICAgY3JlYXRlZCArPSAxCgogICAgbWV0cmljc191cGRhdGVkID0gMAogICAgZm9yIG0gaW4gc29ydGVkKHRvdWNoZWRfbW9udGhzKToKICAgICAgICBtZXRyaWNzX3VwZGF0ZWQgKz0gX3N5bmNfY2xpZW50ZXNfbnVldm9zX21ldHJpY3NfZnJvbV9yb3dzKHBlcmlvZC55ZWFyLCBtKQoKICAgIHJldHVybiB7CiAgICAgICAgInVwZGF0ZWQiOiB1cGRhdGVkLAogICAgICAgICJkZWxldGVkIjogZGVsZXRlZCwKICAgICAgICAiY3JlYXRlZCI6IGNyZWF0ZWQsCiAgICAgICAgIm1ldHJpY3NfdXBkYXRlZCI6IG1ldHJpY3NfdXBkYXRlZCwKICAgICAgICAidG90YWwiOiB1cGRhdGVkICsgZGVsZXRlZCArIGNyZWF0ZWQsCiAgICB9CgoKQHRyYW5zYWN0aW9uLmF0b21pYwpkZWYgc2F2ZV91bmVfcmVhc3NpZ25tZW50cyh1c2VyLCBwZXJpb2Q6IEFkbWluUGVyaW9kLCBwb3N0X2RhdGEsIHJlYXNvbjogc3RyID0gIiIpIC0+IGRpY3Q6CiAgICAiIiJTb2xvIHBlcm1pdGUgY2FtYmlhciBVTkUgZW50cmUgbGFzIGN1YXRybyBVTkVzIGFjdGl2YXMgZGVsIG5lZ29jaW8uIiIiCiAgICBhbGxvd2VkX3VuZXMgPSBfYWxsb3dlZF91bmVfaWRzKCkKICAgIHVuZV9ieV9pZCA9IHt1LmlkOiB1IGZvciB1IGluIHBlcmlvZF91bmVzKCl9CiAgICBjaGFuZ2VkID0gMAogICAgdG91Y2hlZF9tb250aHM6IHNldFtpbnRdID0gc2V0KCkKCiAgICBxcyA9IGFwcGx5X3BlcmlvZF9yYW5nZShOZXdDbGllbnRJbXBvcnRSb3cub2JqZWN0cy5hbGwoKSwgcGVyaW9kKS5zZWxlY3RfcmVsYXRlZCgidW5lIikKICAgIGZvciByb3cgaW4gcXM6CiAgICAgICAgcmF3ID0gcG9zdF9kYXRhLmdldChmInVuZV97cm93LmlkfSIpCiAgICAgICAgaWYgcmF3IGlzIE5vbmU6CiAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgbmV3X3VuZV9pZCA9IF9wYXJzZV9vcHRpb25hbF9pbnQocmF3KQogICAgICAgIGlmIG5ld191bmVfaWQgbm90IGluIGFsbG93ZWRfdW5lczoKICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIlVORSBpbnbDoWxpZGEgcGFyYSBmaWxhIHtyb3cuaWR9LiIpCiAgICAgICAgaWYgbmV3X3VuZV9pZCA9PSByb3cudW5lX2lkOgogICAgICAgICAgICBjb250aW51ZQoKICAgICAgICBvbGRfdW5lID0gcm93LnVuZQogICAgICAgIG5ld191bmUgPSB1bmVfYnlfaWRbbmV3X3VuZV9pZF0KICAgICAgICByb3cudW5lX2lkID0gbmV3X3VuZV9pZAogICAgICAgIHJvdy5yYXdfdW5lX3ZhbHVlID0gbmV3X3VuZS5uYW1lX2VzCiAgICAgICAgcm93LnNhdmUodXBkYXRlX2ZpZWxkcz1bInVuZSIsICJyYXdfdW5lX3ZhbHVlIiwgInVwZGF0ZWRfYXQiXSkKICAgICAgICB0b3VjaGVkX21vbnRocy5hZGQocm93Lm1vbnRoKQogICAgICAgIGxvZ19tYW51YWxfZWRpdCgKICAgICAgICAgICAgdXNlcj11c2VyLAogICAgICAgICAgICB5ZWFyPXJvdy55ZWFyLAogICAgICAgICAgICBtb250aD1yb3cubW9udGgsCiAgICAgICAgICAgIGVudGl0eV90eXBlPUFkbWluTWFudWFsRWRpdExvZy5FTlRJVFlfTkVXX0NMSUVOVF9ST1csCiAgICAgICAgICAgIGVudGl0eV9pZD1yb3cuaWQsCiAgICAgICAgICAgIGZpZWxkX25hbWU9InVuZSIsCiAgICAgICAgICAgIG9sZF92YWx1ZT1mIntvbGRfdW5lLmNvZGV9ICh7b2xkX3VuZS5uYW1lX2VzfSkiLAogICAgICAgICAgICBuZXdfdmFsdWU9ZiJ7bmV3X3VuZS5jb2RlfSAoe25ld191bmUubmFtZV9lc30pIiwKICAgICAgICAgICAgcmVhc29uPXJlYXNvbiBvciAiUmVhc2lnbmFjacOzbiBkZSBVTkUiLAogICAgICAgICkKICAgICAgICBjaGFuZ2VkICs9IDEKCiAgICBtZXRyaWNzX3VwZGF0ZWQgPSAwCiAgICBmb3IgbSBpbiBzb3J0ZWQodG91Y2hlZF9tb250aHMpOgogICAgICAgIG1ldHJpY3NfdXBkYXRlZCArPSBfc3luY19jbGllbnRlc19udWV2b3NfbWV0cmljc19mcm9tX3Jvd3MocGVyaW9kLnllYXIsIG0pCgogICAgcmV0dXJuIHsiY2hhbmdlZCI6IGNoYW5nZWQsICJtZXRyaWNzX3VwZGF0ZWQiOiBtZXRyaWNzX3VwZGF0ZWR9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
