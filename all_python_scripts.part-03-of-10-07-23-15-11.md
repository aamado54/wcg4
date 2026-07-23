# CONCATENATED .PY FILES

PART_NUMBER=3
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
PATH_LITERAL=core/management/commands/prepare_wcg_data_files.py
PATH_JSON="core/management/commands/prepare_wcg_data_files.py"
FILENAME=prepare_wcg_data_files.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=94
SIZE_BYTES_UTF8=3740
CONTENT_SHA256=b90206750c078eb0e23a33f64b40f20e427ac1a7fc99969cfc5b76a20bfde6b0
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
Genera archivos de muestra en data/wcg/ con los nombres esperados por import_wcg_data.
Útil cuando los archivos reales aún no están en el repositorio.
"""

import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from openpyxl import Workbook


class Command(BaseCommand):
    help = "Crea archivos CSV/XLSX de muestra en data/wcg/"

    def handle(self, *args, **options):
        target = settings.BASE_DIR / "data" / "wcg"
        target.mkdir(parents=True, exist_ok=True)

        crm_path = target / "crm datos - InfoClientesWCG para CRM.csv"
        with crm_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([
                "Codigo", "NIT", "Nombre", "UNE", "Tipo", "Telefono", "Email",
                "Contacto", "Cargo", "Notas",
            ])
            w.writerow([
                "9852115", "9852115", "VICENTE SOLER MUNGUÍA",
                "INVESTMENT - WC LEASING", "Cliente", "5025550101",
                "contacto@soler.gt", "María Soler", "Gerente", "Import demo",
            ])
            w.writerow([
                "DEMO002", "1234567-8", "Distribuidora Me Llega, S.A.",
                "INVESTMENT - WC FACTORING", "Cliente", "5025550202",
                "jperez@melega.gt", "Juan Pérez", "CFO", "",
            ])

        risk_path = target / (
            "balon datos - Ejemplo de datos Riesgo al 31-mayo para una operacion - Base de datos Leasing.xlsx"
        )
        wb = Workbook()
        ws = wb.active
        ws.title = "Base de datos Leasing"
        ws.append([
            "Cliente", "NIT", "Operacion", "Unidad", "Saldo", "Dias_Mora",
            "Monto_Exigible", "Fecha_Snapshot", "Nivel_Riesgo", "Alerta",
        ])
        ws.append([
            "VICENTE SOLER MUNGUÍA", "9852115", "PG01260302", "LEASING",
            125000, 45, 42000, "2026-05-31", "ALTO", "SI",
        ])
        ws.append([
            "Ingenio Palo Gordo, S.A.", "8765432-1", "LG01260115", "LEASING",
            890000, 62, 120000, "2026-05-31", "CRITICO", "SI",
        ])
        wb.save(risk_path)

        pgo_cat = target / "pgo datos - Archivos para PGO.csv"
        with pgo_cat.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Archivo", "Descripcion", "Modulo"])
            w.writerow(["control tickets", "Tickets TI Q2", "PGO"])

        tickets_path = target / "pgo datos - control de tickets marzo abril y mayo 2026 para PGO.xlsx"
        wb2 = Workbook()
        ws2 = wb2.active
        ws2.title = "Tickets"
        ws2.append([
            "Ticket", "Titulo", "Estado", "Prioridad", "Asignado", "Fecha_Apertura",
            "Fecha_Cierre", "Unidad_Negocio", "SLA_Horas",
        ])
        ws2.append([
            "TI-IMP-001", "Instalar cliente VPN", "Cerrado", "Alta", "caa",
            "2026-03-05 09:00:00", "2026-03-05 14:00:00", "TI", 48,
        ])
        ws2.append([
            "TI-IMP-002", "Error importación CRM", "Abierto", "Media", "caa",
            "2026-05-10 11:30:00", "", "TI", 48,
        ])
        wb2.save(tickets_path)

        analisis_path = target / "pgo ejemplo del analisis - PGO - TI Q22026.xlsx"
        wb3 = Workbook()
        ws3 = wb3.active
        ws3.title = "PGO TI Q2"
        ws3.append(["ID", "Asunto", "Status", "Prioridad", "Tecnico", "Creado", "Cerrado", "Area", "SLA"])
        ws3.append([
            "TI-Q2-001", "Migración servidor", "Cerrado", "Alta", "caa",
            "2026-04-01 08:00:00", "2026-04-02 10:00:00", "TI", 48,
        ])
        wb3.save(analisis_path)

        self.stdout.write(self.style.SUCCESS(f"Archivos creados en {target}"))

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Genera archivos de muestra en data/wcg/ con los nombres esperados por import_wcg_data.
00003|Útil cuando los archivos reales aún no están en el repositorio.
00004|"""
00005|
00006|import csv
00007|from pathlib import Path
00008|
00009|from django.conf import settings
00010|from django.core.management.base import BaseCommand
00011|from openpyxl import Workbook
00012|
00013|
00014|class Command(BaseCommand):
00015|    help = "Crea archivos CSV/XLSX de muestra en data/wcg/"
00016|
00017|    def handle(self, *args, **options):
00018|        target = settings.BASE_DIR / "data" / "wcg"
00019|        target.mkdir(parents=True, exist_ok=True)
00020|
00021|        crm_path = target / "crm datos - InfoClientesWCG para CRM.csv"
00022|        with crm_path.open("w", newline="", encoding="utf-8") as f:
00023|            w = csv.writer(f)
00024|            w.writerow([
00025|                "Codigo", "NIT", "Nombre", "UNE", "Tipo", "Telefono", "Email",
00026|                "Contacto", "Cargo", "Notas",
00027|            ])
00028|            w.writerow([
00029|                "9852115", "9852115", "VICENTE SOLER MUNGUÍA",
00030|                "INVESTMENT - WC LEASING", "Cliente", "5025550101",
00031|                "contacto@soler.gt", "María Soler", "Gerente", "Import demo",
00032|            ])
00033|            w.writerow([
00034|                "DEMO002", "1234567-8", "Distribuidora Me Llega, S.A.",
00035|                "INVESTMENT - WC FACTORING", "Cliente", "5025550202",
00036|                "jperez@melega.gt", "Juan Pérez", "CFO", "",
00037|            ])
00038|
00039|        risk_path = target / (
00040|            "balon datos - Ejemplo de datos Riesgo al 31-mayo para una operacion - Base de datos Leasing.xlsx"
00041|        )
00042|        wb = Workbook()
00043|        ws = wb.active
00044|        ws.title = "Base de datos Leasing"
00045|        ws.append([
00046|            "Cliente", "NIT", "Operacion", "Unidad", "Saldo", "Dias_Mora",
00047|            "Monto_Exigible", "Fecha_Snapshot", "Nivel_Riesgo", "Alerta",
00048|        ])
00049|        ws.append([
00050|            "VICENTE SOLER MUNGUÍA", "9852115", "PG01260302", "LEASING",
00051|            125000, 45, 42000, "2026-05-31", "ALTO", "SI",
00052|        ])
00053|        ws.append([
00054|            "Ingenio Palo Gordo, S.A.", "8765432-1", "LG01260115", "LEASING",
00055|            890000, 62, 120000, "2026-05-31", "CRITICO", "SI",
00056|        ])
00057|        wb.save(risk_path)
00058|
00059|        pgo_cat = target / "pgo datos - Archivos para PGO.csv"
00060|        with pgo_cat.open("w", newline="", encoding="utf-8") as f:
00061|            w = csv.writer(f)
00062|            w.writerow(["Archivo", "Descripcion", "Modulo"])
00063|            w.writerow(["control tickets", "Tickets TI Q2", "PGO"])
00064|
00065|        tickets_path = target / "pgo datos - control de tickets marzo abril y mayo 2026 para PGO.xlsx"
00066|        wb2 = Workbook()
00067|        ws2 = wb2.active
00068|        ws2.title = "Tickets"
00069|        ws2.append([
00070|            "Ticket", "Titulo", "Estado", "Prioridad", "Asignado", "Fecha_Apertura",
00071|            "Fecha_Cierre", "Unidad_Negocio", "SLA_Horas",
00072|        ])
00073|        ws2.append([
00074|            "TI-IMP-001", "Instalar cliente VPN", "Cerrado", "Alta", "caa",
00075|            "2026-03-05 09:00:00", "2026-03-05 14:00:00", "TI", 48,
00076|        ])
00077|        ws2.append([
00078|            "TI-IMP-002", "Error importación CRM", "Abierto", "Media", "caa",
00079|            "2026-05-10 11:30:00", "", "TI", 48,
00080|        ])
00081|        wb2.save(tickets_path)
00082|
00083|        analisis_path = target / "pgo ejemplo del analisis - PGO - TI Q22026.xlsx"
00084|        wb3 = Workbook()
00085|        ws3 = wb3.active
00086|        ws3.title = "PGO TI Q2"
00087|        ws3.append(["ID", "Asunto", "Status", "Prioridad", "Tecnico", "Creado", "Cerrado", "Area", "SLA"])
00088|        ws3.append([
00089|            "TI-Q2-001", "Migración servidor", "Cerrado", "Alta", "caa",
00090|            "2026-04-01 08:00:00", "2026-04-02 10:00:00", "TI", 48,
00091|        ])
00092|        wb3.save(analisis_path)
00093|
00094|        self.stdout.write(self.style.SUCCESS(f"Archivos creados en {target}"))

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiCkdlbmVyYSBhcmNoaXZvcyBkZSBtdWVzdHJhIGVuIGRhdGEvd2NnLyBjb24gbG9zIG5vbWJyZXMgZXNwZXJhZG9zIHBvciBpbXBvcnRfd2NnX2RhdGEuCsOadGlsIGN1YW5kbyBsb3MgYXJjaGl2b3MgcmVhbGVzIGHDum4gbm8gZXN0w6FuIGVuIGVsIHJlcG9zaXRvcmlvLgoiIiIKCmltcG9ydCBjc3YKZnJvbSBwYXRobGliIGltcG9ydCBQYXRoCgpmcm9tIGRqYW5nby5jb25mIGltcG9ydCBzZXR0aW5ncwpmcm9tIGRqYW5nby5jb3JlLm1hbmFnZW1lbnQuYmFzZSBpbXBvcnQgQmFzZUNvbW1hbmQKZnJvbSBvcGVucHl4bCBpbXBvcnQgV29ya2Jvb2sKCgpjbGFzcyBDb21tYW5kKEJhc2VDb21tYW5kKToKICAgIGhlbHAgPSAiQ3JlYSBhcmNoaXZvcyBDU1YvWExTWCBkZSBtdWVzdHJhIGVuIGRhdGEvd2NnLyIKCiAgICBkZWYgaGFuZGxlKHNlbGYsICphcmdzLCAqKm9wdGlvbnMpOgogICAgICAgIHRhcmdldCA9IHNldHRpbmdzLkJBU0VfRElSIC8gImRhdGEiIC8gIndjZyIKICAgICAgICB0YXJnZXQubWtkaXIocGFyZW50cz1UcnVlLCBleGlzdF9vaz1UcnVlKQoKICAgICAgICBjcm1fcGF0aCA9IHRhcmdldCAvICJjcm0gZGF0b3MgLSBJbmZvQ2xpZW50ZXNXQ0cgcGFyYSBDUk0uY3N2IgogICAgICAgIHdpdGggY3JtX3BhdGgub3BlbigidyIsIG5ld2xpbmU9IiIsIGVuY29kaW5nPSJ1dGYtOCIpIGFzIGY6CiAgICAgICAgICAgIHcgPSBjc3Yud3JpdGVyKGYpCiAgICAgICAgICAgIHcud3JpdGVyb3coWwogICAgICAgICAgICAgICAgIkNvZGlnbyIsICJOSVQiLCAiTm9tYnJlIiwgIlVORSIsICJUaXBvIiwgIlRlbGVmb25vIiwgIkVtYWlsIiwKICAgICAgICAgICAgICAgICJDb250YWN0byIsICJDYXJnbyIsICJOb3RhcyIsCiAgICAgICAgICAgIF0pCiAgICAgICAgICAgIHcud3JpdGVyb3coWwogICAgICAgICAgICAgICAgIjk4NTIxMTUiLCAiOTg1MjExNSIsICJWSUNFTlRFIFNPTEVSIE1VTkdVw41BIiwKICAgICAgICAgICAgICAgICJJTlZFU1RNRU5UIC0gV0MgTEVBU0lORyIsICJDbGllbnRlIiwgIjUwMjU1NTAxMDEiLAogICAgICAgICAgICAgICAgImNvbnRhY3RvQHNvbGVyLmd0IiwgIk1hcsOtYSBTb2xlciIsICJHZXJlbnRlIiwgIkltcG9ydCBkZW1vIiwKICAgICAgICAgICAgXSkKICAgICAgICAgICAgdy53cml0ZXJvdyhbCiAgICAgICAgICAgICAgICAiREVNTzAwMiIsICIxMjM0NTY3LTgiLCAiRGlzdHJpYnVpZG9yYSBNZSBMbGVnYSwgUy5BLiIsCiAgICAgICAgICAgICAgICAiSU5WRVNUTUVOVCAtIFdDIEZBQ1RPUklORyIsICJDbGllbnRlIiwgIjUwMjU1NTAyMDIiLAogICAgICAgICAgICAgICAgImpwZXJlekBtZWxlZ2EuZ3QiLCAiSnVhbiBQw6lyZXoiLCAiQ0ZPIiwgIiIsCiAgICAgICAgICAgIF0pCgogICAgICAgIHJpc2tfcGF0aCA9IHRhcmdldCAvICgKICAgICAgICAgICAgImJhbG9uIGRhdG9zIC0gRWplbXBsbyBkZSBkYXRvcyBSaWVzZ28gYWwgMzEtbWF5byBwYXJhIHVuYSBvcGVyYWNpb24gLSBCYXNlIGRlIGRhdG9zIExlYXNpbmcueGxzeCIKICAgICAgICApCiAgICAgICAgd2IgPSBXb3JrYm9vaygpCiAgICAgICAgd3MgPSB3Yi5hY3RpdmUKICAgICAgICB3cy50aXRsZSA9ICJCYXNlIGRlIGRhdG9zIExlYXNpbmciCiAgICAgICAgd3MuYXBwZW5kKFsKICAgICAgICAgICAgIkNsaWVudGUiLCAiTklUIiwgIk9wZXJhY2lvbiIsICJVbmlkYWQiLCAiU2FsZG8iLCAiRGlhc19Nb3JhIiwKICAgICAgICAgICAgIk1vbnRvX0V4aWdpYmxlIiwgIkZlY2hhX1NuYXBzaG90IiwgIk5pdmVsX1JpZXNnbyIsICJBbGVydGEiLAogICAgICAgIF0pCiAgICAgICAgd3MuYXBwZW5kKFsKICAgICAgICAgICAgIlZJQ0VOVEUgU09MRVIgTVVOR1XDjUEiLCAiOTg1MjExNSIsICJQRzAxMjYwMzAyIiwgIkxFQVNJTkciLAogICAgICAgICAgICAxMjUwMDAsIDQ1LCA0MjAwMCwgIjIwMjYtMDUtMzEiLCAiQUxUTyIsICJTSSIsCiAgICAgICAgXSkKICAgICAgICB3cy5hcHBlbmQoWwogICAgICAgICAgICAiSW5nZW5pbyBQYWxvIEdvcmRvLCBTLkEuIiwgIjg3NjU0MzItMSIsICJMRzAxMjYwMTE1IiwgIkxFQVNJTkciLAogICAgICAgICAgICA4OTAwMDAsIDYyLCAxMjAwMDAsICIyMDI2LTA1LTMxIiwgIkNSSVRJQ08iLCAiU0kiLAogICAgICAgIF0pCiAgICAgICAgd2Iuc2F2ZShyaXNrX3BhdGgpCgogICAgICAgIHBnb19jYXQgPSB0YXJnZXQgLyAicGdvIGRhdG9zIC0gQXJjaGl2b3MgcGFyYSBQR08uY3N2IgogICAgICAgIHdpdGggcGdvX2NhdC5vcGVuKCJ3IiwgbmV3bGluZT0iIiwgZW5jb2Rpbmc9InV0Zi04IikgYXMgZjoKICAgICAgICAgICAgdyA9IGNzdi53cml0ZXIoZikKICAgICAgICAgICAgdy53cml0ZXJvdyhbIkFyY2hpdm8iLCAiRGVzY3JpcGNpb24iLCAiTW9kdWxvIl0pCiAgICAgICAgICAgIHcud3JpdGVyb3coWyJjb250cm9sIHRpY2tldHMiLCAiVGlja2V0cyBUSSBRMiIsICJQR08iXSkKCiAgICAgICAgdGlja2V0c19wYXRoID0gdGFyZ2V0IC8gInBnbyBkYXRvcyAtIGNvbnRyb2wgZGUgdGlja2V0cyBtYXJ6byBhYnJpbCB5IG1heW8gMjAyNiBwYXJhIFBHTy54bHN4IgogICAgICAgIHdiMiA9IFdvcmtib29rKCkKICAgICAgICB3czIgPSB3YjIuYWN0aXZlCiAgICAgICAgd3MyLnRpdGxlID0gIlRpY2tldHMiCiAgICAgICAgd3MyLmFwcGVuZChbCiAgICAgICAgICAgICJUaWNrZXQiLCAiVGl0dWxvIiwgIkVzdGFkbyIsICJQcmlvcmlkYWQiLCAiQXNpZ25hZG8iLCAiRmVjaGFfQXBlcnR1cmEiLAogICAgICAgICAgICAiRmVjaGFfQ2llcnJlIiwgIlVuaWRhZF9OZWdvY2lvIiwgIlNMQV9Ib3JhcyIsCiAgICAgICAgXSkKICAgICAgICB3czIuYXBwZW5kKFsKICAgICAgICAgICAgIlRJLUlNUC0wMDEiLCAiSW5zdGFsYXIgY2xpZW50ZSBWUE4iLCAiQ2VycmFkbyIsICJBbHRhIiwgImNhYSIsCiAgICAgICAgICAgICIyMDI2LTAzLTA1IDA5OjAwOjAwIiwgIjIwMjYtMDMtMDUgMTQ6MDA6MDAiLCAiVEkiLCA0OCwKICAgICAgICBdKQogICAgICAgIHdzMi5hcHBlbmQoWwogICAgICAgICAgICAiVEktSU1QLTAwMiIsICJFcnJvciBpbXBvcnRhY2nDs24gQ1JNIiwgIkFiaWVydG8iLCAiTWVkaWEiLCAiY2FhIiwKICAgICAgICAgICAgIjIwMjYtMDUtMTAgMTE6MzA6MDAiLCAiIiwgIlRJIiwgNDgsCiAgICAgICAgXSkKICAgICAgICB3YjIuc2F2ZSh0aWNrZXRzX3BhdGgpCgogICAgICAgIGFuYWxpc2lzX3BhdGggPSB0YXJnZXQgLyAicGdvIGVqZW1wbG8gZGVsIGFuYWxpc2lzIC0gUEdPIC0gVEkgUTIyMDI2Lnhsc3giCiAgICAgICAgd2IzID0gV29ya2Jvb2soKQogICAgICAgIHdzMyA9IHdiMy5hY3RpdmUKICAgICAgICB3czMudGl0bGUgPSAiUEdPIFRJIFEyIgogICAgICAgIHdzMy5hcHBlbmQoWyJJRCIsICJBc3VudG8iLCAiU3RhdHVzIiwgIlByaW9yaWRhZCIsICJUZWNuaWNvIiwgIkNyZWFkbyIsICJDZXJyYWRvIiwgIkFyZWEiLCAiU0xBIl0pCiAgICAgICAgd3MzLmFwcGVuZChbCiAgICAgICAgICAgICJUSS1RMi0wMDEiLCAiTWlncmFjacOzbiBzZXJ2aWRvciIsICJDZXJyYWRvIiwgIkFsdGEiLCAiY2FhIiwKICAgICAgICAgICAgIjIwMjYtMDQtMDEgMDg6MDA6MDAiLCAiMjAyNi0wNC0wMiAxMDowMDowMCIsICJUSSIsIDQ4LAogICAgICAgIF0pCiAgICAgICAgd2IzLnNhdmUoYW5hbGlzaXNfcGF0aCkKCiAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoc2VsZi5zdHlsZS5TVUNDRVNTKGYiQXJjaGl2b3MgY3JlYWRvcyBlbiB7dGFyZ2V0fSIpKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/management/commands/recalc_pgc.py
PATH_JSON="core/management/commands/recalc_pgc.py"
FILENAME=recalc_pgc.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=372
SIZE_BYTES_UTF8=13085
CONTENT_SHA256=3dd3553d0a74e21726bf7caae16b8576b296cd1b7e93407229ec274e4d42a301
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
from decimal import Decimal, ROUND_HALF_UP

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import MetricDefinition, UNE
from pgc.models import (
    PGCPlan,
    MonthlyTarget,
    MonthlyMetricResult,
    MonthlyMetricScore,
    MonthlyModeScorecard,
    ManualRequirementsCompliance,
    MetricReserve,
)


class Command(BaseCommand):
    help = "Recalcula resultados y score PGC para un año y mes"

    SCORABLE_MODE2_CODES = (
        MetricDefinition.CODE_INGRESOS,
        MetricDefinition.CODE_CLIENTES_NUEVOS,
        MetricDefinition.CODE_VENTA_CRUZADA,
    )

    def add_arguments(self, parser):
        parser.add_argument("--year", type=int, required=True)
        parser.add_argument("--month", type=int, required=True)
        parser.add_argument(
            "--mode",
            type=str,
            default="modo1",
            choices=["modo1", "modo2"],
            help="Modalidad de cálculo de puntos: modo1 o modo2.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        year = options["year"]
        month = options["month"]
        mode = options["mode"]

        try:
            plan = PGCPlan.objects.get(year=year)
        except PGCPlan.DoesNotExist:
            raise CommandError(f"No existe PGCPlan para el año {year}")

        self.stdout.write(
            self.style.WARNING(
                f"Recalculando PGC {year}-{month:02d} en {mode}..."
            )
        )

        metrics = {
            m.code: m
            for m in MetricDefinition.objects.filter(
                code__in=[
                    MetricDefinition.CODE_INGRESOS,
                    MetricDefinition.CODE_CLIENTES_NUEVOS,
                    MetricDefinition.CODE_VENTA_CRUZADA,
                    MetricDefinition.CODE_RESPUESTA_REQS,
                ]
            )
        }

        if len(metrics) != 4:
            raise CommandError(
                "Faltan métricas base "
                "INGRESOS/CLIENTES_NUEVOS/VENTA_CRUZADA/RESPUESTA_REQS"
            )

        unes = UNE.objects.filter(is_active=True)

        metric_scores_created = 0
        metric_scores_updated = 0
        mode_scorecards_created = 0
        mode_scorecards_updated = 0

        for une in unes:
            total_points = Decimal("0")

            for metric in metrics.values():
                try:
                    target = MonthlyTarget.objects.get(
                        plan=plan,
                        une=une,
                        metric=metric,
                        year=year,
                        month=month,
                    )
                except MonthlyTarget.DoesNotExist:
                    continue

                source_result, _ = MonthlyMetricResult.objects.get_or_create(
                    plan=plan,
                    une=une,
                    metric=metric,
                    year=year,
                    month=month,
                    defaults={
                        "measured_value": None,
                        "target_value": target.target_value,
                        "is_achieved": False,
                        "points_awarded": 0,
                        "calculation_note": "",
                    },
                )

                score, created = MonthlyMetricScore.objects.get_or_create(
                    plan=plan,
                    une=une,
                    metric=metric,
                    year=year,
                    month=month,
                    mode=mode,
                    defaults={
                        "measured_value": source_result.measured_value,
                        "target_value": target.target_value,
                        "is_achieved": False,
                        "points_awarded": 0,
                        "calculation_note": "",
                    },
                )

                if created:
                    metric_scores_created += 1
                else:
                    metric_scores_updated += 1

                score.measured_value = source_result.measured_value
                score.target_value = target.target_value

                if mode == "modo1":
                    self.apply_modo1(score, metric, target)
                else:
                    self.apply_modo2(plan, year, month, une, score, metric, target)

                if metric.code == MetricDefinition.CODE_RESPUESTA_REQS:
                    self.apply_manual_requirements_override(
                        plan=plan,
                        une=une,
                        year=year,
                        month=month,
                        metric_score=score,
                    )

                score.save()
                total_points += Decimal(str(score.points_awarded or 0))

            mode_scorecard, created = MonthlyModeScorecard.objects.get_or_create(
                plan=plan,
                une=une,
                year=year,
                month=month,
                mode=mode,
                defaults={
                    "total_points": total_points,
                    "qualified_threshold": 80,
                    "is_month_qualified": total_points >= Decimal("80"),
                    "summary_note": f"Score recalculado en {mode}",
                },
            )

            if created:
                mode_scorecards_created += 1
            else:
                mode_scorecards_updated += 1

            if mode_scorecard.qualified_threshold is None:
                mode_scorecard.qualified_threshold = 80

            mode_scorecard.total_points = total_points
            mode_scorecard.is_month_qualified = total_points >= Decimal(
                str(mode_scorecard.qualified_threshold)
            )
            mode_scorecard.summary_note = f"Score recalculado en {mode}"
            mode_scorecard.save()

        self.stdout.write(
            f"MonthlyMetricScore: {metric_scores_created} creados, "
            f"{metric_scores_updated} actualizados"
        )
        self.stdout.write(
            f"MonthlyModeScorecard: {mode_scorecards_created} creados, "
            f"{mode_scorecards_updated} actualizados"
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Recalc PGC {year}-{month:02d} completado en {mode}."
            )
        )

    def apply_modo1(self, metric_score, metric, target):
        measured = metric_score.measured_value
        target_value = metric_score.target_value

        if measured is not None and target_value is not None:
            if measured >= target_value:
                metric_score.is_achieved = True
                metric_score.points_awarded = target.points_if_achieved
                metric_score.calculation_note = "Modo1 cumple meta objetivo."
            else:
                metric_score.is_achieved = False
                metric_score.points_awarded = 0
                metric_score.calculation_note = "Modo1 no cumple meta objetivo."
            return

        if metric.code in (
            MetricDefinition.CODE_VENTA_CRUZADA,
            MetricDefinition.CODE_RESPUESTA_REQS,
        ):
            if measured and measured >= Decimal("1"):
                metric_score.is_achieved = True
                metric_score.points_awarded = target.points_if_achieved
                metric_score.calculation_note = "Modo1 cumple condición binaria."
            else:
                metric_score.is_achieved = False
                metric_score.points_awarded = 0
                metric_score.calculation_note = "Modo1 sin datos suficientes o no cumplida."
        else:
            metric_score.is_achieved = False
            metric_score.points_awarded = 0
            metric_score.calculation_note = "Modo1 sin valor medido para este mes."

    def apply_modo2(self, plan, year, month, une, metric_score, metric, target):
        if metric.code == MetricDefinition.CODE_RESPUESTA_REQS:
            self.apply_modo1(metric_score, metric, target)
            metric_score.calculation_note = (
                f"Modo2 requerimientos se calculan igual que modo1. "
                f"{metric_score.calculation_note}"
            )
            return

        if metric.code not in self.SCORABLE_MODE2_CODES:
            self.apply_modo1(metric_score, metric, target)
            metric_score.calculation_note = (
                f"Modo2 métrica no configurada para proporcionalidad. "
                f"{metric_score.calculation_note}"
            )
            return

        measured = metric_score.measured_value or Decimal("0")
        target_value = metric_score.target_value or Decimal("0")
        full_points = Decimal(str(target.points_if_achieved or 0))

        if target_value <= Decimal("0"):
            metric_score.is_achieved = False
            metric_score.points_awarded = Decimal("0")
            metric_score.calculation_note = "Modo2 meta vacía o igual a cero."
            return

        reserve_points_available = self.get_available_reserve(
            plan, une, metric, year, month
        )

        raw_points = (
            full_points * (measured / target_value)
        ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

        available_points = raw_points + reserve_points_available
        points_awarded = min(full_points, available_points).quantize(
            Decimal("0.0001"), rounding=ROUND_HALF_UP
        )

        reserve_points_to_use = min(
            reserve_points_available,
            max(Decimal("0"), points_awarded - raw_points)
        ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

        if reserve_points_to_use > 0:
            self.consume_reserve(
                plan, une, metric, year, month, reserve_points_to_use
            )

        extra_points_current_month = max(
            Decimal("0"), raw_points - full_points
        ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

        if extra_points_current_month > 0:
            MetricReserve.objects.create(
                plan=plan,
                une=une,
                metric=metric,
                source_year=year,
                source_month=month,
                amount=extra_points_current_month,
                remaining=extra_points_current_month,
            )

        metric_score.is_achieved = points_awarded >= full_points
        metric_score.points_awarded = points_awarded

        reserve_points_remaining = (
            reserve_points_available - reserve_points_to_use + extra_points_current_month
        ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

        metric_score.calculation_note = (
            f"Modo2 medido={measured}, "
            f"meta={target_value}, "
            f"puntos_teoricos={raw_points}, "
            f"reserva_puntos_disponible={reserve_points_available}, "
            f"reserva_puntos_usada={reserve_points_to_use}, "
            f"puntos_otorgados={points_awarded}, "
            f"excedente_puntos_generado={extra_points_current_month}, "
            f"reserva_puntos_final={reserve_points_remaining}."
        )

    def apply_manual_requirements_override(
        self, plan, une, year, month, metric_score
    ):
        try:
            mrc = ManualRequirementsCompliance.objects.get(
                plan=plan,
                une=une,
                year=year,
                month=month,
            )
        except ManualRequirementsCompliance.DoesNotExist:
            return

        if mrc.is_compliant is False:
            metric_score.points_awarded = 0
            metric_score.is_achieved = False
            metric_score.calculation_note = (
                "Marcado como no cumplido en cumplimiento manual; "
                "puntos removidos."
            )

    def get_available_reserve(self, plan, une, metric, year, month):
        reserves = MetricReserve.objects.filter(
            plan=plan,
            une=une,
            metric=metric,
            remaining__gt=0,
        ).exclude(
            source_year=year,
            source_month=month,
        )

        total = Decimal("0")
        for reserve in reserves:
            total += reserve.remaining or Decimal("0")
        return total

    def consume_reserve(self, plan, une, metric, year, month, amount_to_consume):
        pending = Decimal(str(amount_to_consume))

        reserves = (
            MetricReserve.objects.filter(
                plan=plan,
                une=une,
                metric=metric,
                remaining__gt=0,
            )
            .exclude(
                source_year=year,
                source_month=month,
            )
            .order_by("source_year", "source_month", "id")
        )

        for reserve in reserves:
            if pending <= Decimal("0"):
                break

            available = reserve.remaining or Decimal("0")
            used = min(available, pending)
            reserve.remaining = available - used
            reserve.save(update_fields=["remaining"])
            pending -= used
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from decimal import Decimal, ROUND_HALF_UP
00002|
00003|from django.core.management.base import BaseCommand, CommandError
00004|from django.db import transaction
00005|
00006|from core.models import MetricDefinition, UNE
00007|from pgc.models import (
00008|    PGCPlan,
00009|    MonthlyTarget,
00010|    MonthlyMetricResult,
00011|    MonthlyMetricScore,
00012|    MonthlyModeScorecard,
00013|    ManualRequirementsCompliance,
00014|    MetricReserve,
00015|)
00016|
00017|
00018|class Command(BaseCommand):
00019|    help = "Recalcula resultados y score PGC para un año y mes"
00020|
00021|    SCORABLE_MODE2_CODES = (
00022|        MetricDefinition.CODE_INGRESOS,
00023|        MetricDefinition.CODE_CLIENTES_NUEVOS,
00024|        MetricDefinition.CODE_VENTA_CRUZADA,
00025|    )
00026|
00027|    def add_arguments(self, parser):
00028|        parser.add_argument("--year", type=int, required=True)
00029|        parser.add_argument("--month", type=int, required=True)
00030|        parser.add_argument(
00031|            "--mode",
00032|            type=str,
00033|            default="modo1",
00034|            choices=["modo1", "modo2"],
00035|            help="Modalidad de cálculo de puntos: modo1 o modo2.",
00036|        )
00037|
00038|    @transaction.atomic
00039|    def handle(self, *args, **options):
00040|        year = options["year"]
00041|        month = options["month"]
00042|        mode = options["mode"]
00043|
00044|        try:
00045|            plan = PGCPlan.objects.get(year=year)
00046|        except PGCPlan.DoesNotExist:
00047|            raise CommandError(f"No existe PGCPlan para el año {year}")
00048|
00049|        self.stdout.write(
00050|            self.style.WARNING(
00051|                f"Recalculando PGC {year}-{month:02d} en {mode}..."
00052|            )
00053|        )
00054|
00055|        metrics = {
00056|            m.code: m
00057|            for m in MetricDefinition.objects.filter(
00058|                code__in=[
00059|                    MetricDefinition.CODE_INGRESOS,
00060|                    MetricDefinition.CODE_CLIENTES_NUEVOS,
00061|                    MetricDefinition.CODE_VENTA_CRUZADA,
00062|                    MetricDefinition.CODE_RESPUESTA_REQS,
00063|                ]
00064|            )
00065|        }
00066|
00067|        if len(metrics) != 4:
00068|            raise CommandError(
00069|                "Faltan métricas base "
00070|                "INGRESOS/CLIENTES_NUEVOS/VENTA_CRUZADA/RESPUESTA_REQS"
00071|            )
00072|
00073|        unes = UNE.objects.filter(is_active=True)
00074|
00075|        metric_scores_created = 0
00076|        metric_scores_updated = 0
00077|        mode_scorecards_created = 0
00078|        mode_scorecards_updated = 0
00079|
00080|        for une in unes:
00081|            total_points = Decimal("0")
00082|
00083|            for metric in metrics.values():
00084|                try:
00085|                    target = MonthlyTarget.objects.get(
00086|                        plan=plan,
00087|                        une=une,
00088|                        metric=metric,
00089|                        year=year,
00090|                        month=month,
00091|                    )
00092|                except MonthlyTarget.DoesNotExist:
00093|                    continue
00094|
00095|                source_result, _ = MonthlyMetricResult.objects.get_or_create(
00096|                    plan=plan,
00097|                    une=une,
00098|                    metric=metric,
00099|                    year=year,
00100|                    month=month,
00101|                    defaults={
00102|                        "measured_value": None,
00103|                        "target_value": target.target_value,
00104|                        "is_achieved": False,
00105|                        "points_awarded": 0,
00106|                        "calculation_note": "",
00107|                    },
00108|                )
00109|
00110|                score, created = MonthlyMetricScore.objects.get_or_create(
00111|                    plan=plan,
00112|                    une=une,
00113|                    metric=metric,
00114|                    year=year,
00115|                    month=month,
00116|                    mode=mode,
00117|                    defaults={
00118|                        "measured_value": source_result.measured_value,
00119|                        "target_value": target.target_value,
00120|                        "is_achieved": False,
00121|                        "points_awarded": 0,
00122|                        "calculation_note": "",
00123|                    },
00124|                )
00125|
00126|                if created:
00127|                    metric_scores_created += 1
00128|                else:
00129|                    metric_scores_updated += 1
00130|
00131|                score.measured_value = source_result.measured_value
00132|                score.target_value = target.target_value
00133|
00134|                if mode == "modo1":
00135|                    self.apply_modo1(score, metric, target)
00136|                else:
00137|                    self.apply_modo2(plan, year, month, une, score, metric, target)
00138|
00139|                if metric.code == MetricDefinition.CODE_RESPUESTA_REQS:
00140|                    self.apply_manual_requirements_override(
00141|                        plan=plan,
00142|                        une=une,
00143|                        year=year,
00144|                        month=month,
00145|                        metric_score=score,
00146|                    )
00147|
00148|                score.save()
00149|                total_points += Decimal(str(score.points_awarded or 0))
00150|
00151|            mode_scorecard, created = MonthlyModeScorecard.objects.get_or_create(
00152|                plan=plan,
00153|                une=une,
00154|                year=year,
00155|                month=month,
00156|                mode=mode,
00157|                defaults={
00158|                    "total_points": total_points,
00159|                    "qualified_threshold": 80,
00160|                    "is_month_qualified": total_points >= Decimal("80"),
00161|                    "summary_note": f"Score recalculado en {mode}",
00162|                },
00163|            )
00164|
00165|            if created:
00166|                mode_scorecards_created += 1
00167|            else:
00168|                mode_scorecards_updated += 1
00169|
00170|            if mode_scorecard.qualified_threshold is None:
00171|                mode_scorecard.qualified_threshold = 80
00172|
00173|            mode_scorecard.total_points = total_points
00174|            mode_scorecard.is_month_qualified = total_points >= Decimal(
00175|                str(mode_scorecard.qualified_threshold)
00176|            )
00177|            mode_scorecard.summary_note = f"Score recalculado en {mode}"
00178|            mode_scorecard.save()
00179|
00180|        self.stdout.write(
00181|            f"MonthlyMetricScore: {metric_scores_created} creados, "
00182|            f"{metric_scores_updated} actualizados"
00183|        )
00184|        self.stdout.write(
00185|            f"MonthlyModeScorecard: {mode_scorecards_created} creados, "
00186|            f"{mode_scorecards_updated} actualizados"
00187|        )
00188|        self.stdout.write(
00189|            self.style.SUCCESS(
00190|                f"Recalc PGC {year}-{month:02d} completado en {mode}."
00191|            )
00192|        )
00193|
00194|    def apply_modo1(self, metric_score, metric, target):
00195|        measured = metric_score.measured_value
00196|        target_value = metric_score.target_value
00197|
00198|        if measured is not None and target_value is not None:
00199|            if measured >= target_value:
00200|                metric_score.is_achieved = True
00201|                metric_score.points_awarded = target.points_if_achieved
00202|                metric_score.calculation_note = "Modo1 cumple meta objetivo."
00203|            else:
00204|                metric_score.is_achieved = False
00205|                metric_score.points_awarded = 0
00206|                metric_score.calculation_note = "Modo1 no cumple meta objetivo."
00207|            return
00208|
00209|        if metric.code in (
00210|            MetricDefinition.CODE_VENTA_CRUZADA,
00211|            MetricDefinition.CODE_RESPUESTA_REQS,
00212|        ):
00213|            if measured and measured >= Decimal("1"):
00214|                metric_score.is_achieved = True
00215|                metric_score.points_awarded = target.points_if_achieved
00216|                metric_score.calculation_note = "Modo1 cumple condición binaria."
00217|            else:
00218|                metric_score.is_achieved = False
00219|                metric_score.points_awarded = 0
00220|                metric_score.calculation_note = "Modo1 sin datos suficientes o no cumplida."
00221|        else:
00222|            metric_score.is_achieved = False
00223|            metric_score.points_awarded = 0
00224|            metric_score.calculation_note = "Modo1 sin valor medido para este mes."
00225|
00226|    def apply_modo2(self, plan, year, month, une, metric_score, metric, target):
00227|        if metric.code == MetricDefinition.CODE_RESPUESTA_REQS:
00228|            self.apply_modo1(metric_score, metric, target)
00229|            metric_score.calculation_note = (
00230|                f"Modo2 requerimientos se calculan igual que modo1. "
00231|                f"{metric_score.calculation_note}"
00232|            )
00233|            return
00234|
00235|        if metric.code not in self.SCORABLE_MODE2_CODES:
00236|            self.apply_modo1(metric_score, metric, target)
00237|            metric_score.calculation_note = (
00238|                f"Modo2 métrica no configurada para proporcionalidad. "
00239|                f"{metric_score.calculation_note}"
00240|            )
00241|            return
00242|
00243|        measured = metric_score.measured_value or Decimal("0")
00244|        target_value = metric_score.target_value or Decimal("0")
00245|        full_points = Decimal(str(target.points_if_achieved or 0))
00246|
00247|        if target_value <= Decimal("0"):
00248|            metric_score.is_achieved = False
00249|            metric_score.points_awarded = Decimal("0")
00250|            metric_score.calculation_note = "Modo2 meta vacía o igual a cero."
00251|            return
00252|
00253|        reserve_points_available = self.get_available_reserve(
00254|            plan, une, metric, year, month
00255|        )
00256|
00257|        raw_points = (
00258|            full_points * (measured / target_value)
00259|        ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
00260|
00261|        available_points = raw_points + reserve_points_available
00262|        points_awarded = min(full_points, available_points).quantize(
00263|            Decimal("0.0001"), rounding=ROUND_HALF_UP
00264|        )
00265|
00266|        reserve_points_to_use = min(
00267|            reserve_points_available,
00268|            max(Decimal("0"), points_awarded - raw_points)
00269|        ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
00270|
00271|        if reserve_points_to_use > 0:
00272|            self.consume_reserve(
00273|                plan, une, metric, year, month, reserve_points_to_use
00274|            )
00275|
00276|        extra_points_current_month = max(
00277|            Decimal("0"), raw_points - full_points
00278|        ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
00279|
00280|        if extra_points_current_month > 0:
00281|            MetricReserve.objects.create(
00282|                plan=plan,
00283|                une=une,
00284|                metric=metric,
00285|                source_year=year,
00286|                source_month=month,
00287|                amount=extra_points_current_month,
00288|                remaining=extra_points_current_month,
00289|            )
00290|
00291|        metric_score.is_achieved = points_awarded >= full_points
00292|        metric_score.points_awarded = points_awarded
00293|
00294|        reserve_points_remaining = (
00295|            reserve_points_available - reserve_points_to_use + extra_points_current_month
00296|        ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
00297|
00298|        metric_score.calculation_note = (
00299|            f"Modo2 medido={measured}, "
00300|            f"meta={target_value}, "
00301|            f"puntos_teoricos={raw_points}, "
00302|            f"reserva_puntos_disponible={reserve_points_available}, "
00303|            f"reserva_puntos_usada={reserve_points_to_use}, "
00304|            f"puntos_otorgados={points_awarded}, "
00305|            f"excedente_puntos_generado={extra_points_current_month}, "
00306|            f"reserva_puntos_final={reserve_points_remaining}."
00307|        )
00308|
00309|    def apply_manual_requirements_override(
00310|        self, plan, une, year, month, metric_score
00311|    ):
00312|        try:
00313|            mrc = ManualRequirementsCompliance.objects.get(
00314|                plan=plan,
00315|                une=une,
00316|                year=year,
00317|                month=month,
00318|            )
00319|        except ManualRequirementsCompliance.DoesNotExist:
00320|            return
00321|
00322|        if mrc.is_compliant is False:
00323|            metric_score.points_awarded = 0
00324|            metric_score.is_achieved = False
00325|            metric_score.calculation_note = (
00326|                "Marcado como no cumplido en cumplimiento manual; "
00327|                "puntos removidos."
00328|            )
00329|
00330|    def get_available_reserve(self, plan, une, metric, year, month):
00331|        reserves = MetricReserve.objects.filter(
00332|            plan=plan,
00333|            une=une,
00334|            metric=metric,
00335|            remaining__gt=0,
00336|        ).exclude(
00337|            source_year=year,
00338|            source_month=month,
00339|        )
00340|
00341|        total = Decimal("0")
00342|        for reserve in reserves:
00343|            total += reserve.remaining or Decimal("0")
00344|        return total
00345|
00346|    def consume_reserve(self, plan, une, metric, year, month, amount_to_consume):
00347|        pending = Decimal(str(amount_to_consume))
00348|
00349|        reserves = (
00350|            MetricReserve.objects.filter(
00351|                plan=plan,
00352|                une=une,
00353|                metric=metric,
00354|                remaining__gt=0,
00355|            )
00356|            .exclude(
00357|                source_year=year,
00358|                source_month=month,
00359|            )
00360|            .order_by("source_year", "source_month", "id")
00361|        )
00362|
00363|        for reserve in reserves:
00364|            if pending <= Decimal("0"):
00365|                break
00366|
00367|            available = reserve.remaining or Decimal("0")
00368|            used = min(available, pending)
00369|            reserve.remaining = available - used
00370|            reserve.save(update_fields=["remaining"])
00371|            pending -= used
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsLCBST1VORF9IQUxGX1VQCgpmcm9tIGRqYW5nby5jb3JlLm1hbmFnZW1lbnQuYmFzZSBpbXBvcnQgQmFzZUNvbW1hbmQsIENvbW1hbmRFcnJvcgpmcm9tIGRqYW5nby5kYiBpbXBvcnQgdHJhbnNhY3Rpb24KCmZyb20gY29yZS5tb2RlbHMgaW1wb3J0IE1ldHJpY0RlZmluaXRpb24sIFVORQpmcm9tIHBnYy5tb2RlbHMgaW1wb3J0ICgKICAgIFBHQ1BsYW4sCiAgICBNb250aGx5VGFyZ2V0LAogICAgTW9udGhseU1ldHJpY1Jlc3VsdCwKICAgIE1vbnRobHlNZXRyaWNTY29yZSwKICAgIE1vbnRobHlNb2RlU2NvcmVjYXJkLAogICAgTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZSwKICAgIE1ldHJpY1Jlc2VydmUsCikKCgpjbGFzcyBDb21tYW5kKEJhc2VDb21tYW5kKToKICAgIGhlbHAgPSAiUmVjYWxjdWxhIHJlc3VsdGFkb3MgeSBzY29yZSBQR0MgcGFyYSB1biBhw7FvIHkgbWVzIgoKICAgIFNDT1JBQkxFX01PREUyX0NPREVTID0gKAogICAgICAgIE1ldHJpY0RlZmluaXRpb24uQ09ERV9JTkdSRVNPUywKICAgICAgICBNZXRyaWNEZWZpbml0aW9uLkNPREVfQ0xJRU5URVNfTlVFVk9TLAogICAgICAgIE1ldHJpY0RlZmluaXRpb24uQ09ERV9WRU5UQV9DUlVaQURBLAogICAgKQoKICAgIGRlZiBhZGRfYXJndW1lbnRzKHNlbGYsIHBhcnNlcik6CiAgICAgICAgcGFyc2VyLmFkZF9hcmd1bWVudCgiLS15ZWFyIiwgdHlwZT1pbnQsIHJlcXVpcmVkPVRydWUpCiAgICAgICAgcGFyc2VyLmFkZF9hcmd1bWVudCgiLS1tb250aCIsIHR5cGU9aW50LCByZXF1aXJlZD1UcnVlKQogICAgICAgIHBhcnNlci5hZGRfYXJndW1lbnQoCiAgICAgICAgICAgICItLW1vZGUiLAogICAgICAgICAgICB0eXBlPXN0ciwKICAgICAgICAgICAgZGVmYXVsdD0ibW9kbzEiLAogICAgICAgICAgICBjaG9pY2VzPVsibW9kbzEiLCAibW9kbzIiXSwKICAgICAgICAgICAgaGVscD0iTW9kYWxpZGFkIGRlIGPDoWxjdWxvIGRlIHB1bnRvczogbW9kbzEgbyBtb2RvMi4iLAogICAgICAgICkKCiAgICBAdHJhbnNhY3Rpb24uYXRvbWljCiAgICBkZWYgaGFuZGxlKHNlbGYsICphcmdzLCAqKm9wdGlvbnMpOgogICAgICAgIHllYXIgPSBvcHRpb25zWyJ5ZWFyIl0KICAgICAgICBtb250aCA9IG9wdGlvbnNbIm1vbnRoIl0KICAgICAgICBtb2RlID0gb3B0aW9uc1sibW9kZSJdCgogICAgICAgIHRyeToKICAgICAgICAgICAgcGxhbiA9IFBHQ1BsYW4ub2JqZWN0cy5nZXQoeWVhcj15ZWFyKQogICAgICAgIGV4Y2VwdCBQR0NQbGFuLkRvZXNOb3RFeGlzdDoKICAgICAgICAgICAgcmFpc2UgQ29tbWFuZEVycm9yKGYiTm8gZXhpc3RlIFBHQ1BsYW4gcGFyYSBlbCBhw7FvIHt5ZWFyfSIpCgogICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKAogICAgICAgICAgICBzZWxmLnN0eWxlLldBUk5JTkcoCiAgICAgICAgICAgICAgICBmIlJlY2FsY3VsYW5kbyBQR0Mge3llYXJ9LXttb250aDowMmR9IGVuIHttb2RlfS4uLiIKICAgICAgICAgICAgKQogICAgICAgICkKCiAgICAgICAgbWV0cmljcyA9IHsKICAgICAgICAgICAgbS5jb2RlOiBtCiAgICAgICAgICAgIGZvciBtIGluIE1ldHJpY0RlZmluaXRpb24ub2JqZWN0cy5maWx0ZXIoCiAgICAgICAgICAgICAgICBjb2RlX19pbj1bCiAgICAgICAgICAgICAgICAgICAgTWV0cmljRGVmaW5pdGlvbi5DT0RFX0lOR1JFU09TLAogICAgICAgICAgICAgICAgICAgIE1ldHJpY0RlZmluaXRpb24uQ09ERV9DTElFTlRFU19OVUVWT1MsCiAgICAgICAgICAgICAgICAgICAgTWV0cmljRGVmaW5pdGlvbi5DT0RFX1ZFTlRBX0NSVVpBREEsCiAgICAgICAgICAgICAgICAgICAgTWV0cmljRGVmaW5pdGlvbi5DT0RFX1JFU1BVRVNUQV9SRVFTLAogICAgICAgICAgICAgICAgXQogICAgICAgICAgICApCiAgICAgICAgfQoKICAgICAgICBpZiBsZW4obWV0cmljcykgIT0gNDoKICAgICAgICAgICAgcmFpc2UgQ29tbWFuZEVycm9yKAogICAgICAgICAgICAgICAgIkZhbHRhbiBtw6l0cmljYXMgYmFzZSAiCiAgICAgICAgICAgICAgICAiSU5HUkVTT1MvQ0xJRU5URVNfTlVFVk9TL1ZFTlRBX0NSVVpBREEvUkVTUFVFU1RBX1JFUVMiCiAgICAgICAgICAgICkKCiAgICAgICAgdW5lcyA9IFVORS5vYmplY3RzLmZpbHRlcihpc19hY3RpdmU9VHJ1ZSkKCiAgICAgICAgbWV0cmljX3Njb3Jlc19jcmVhdGVkID0gMAogICAgICAgIG1ldHJpY19zY29yZXNfdXBkYXRlZCA9IDAKICAgICAgICBtb2RlX3Njb3JlY2FyZHNfY3JlYXRlZCA9IDAKICAgICAgICBtb2RlX3Njb3JlY2FyZHNfdXBkYXRlZCA9IDAKCiAgICAgICAgZm9yIHVuZSBpbiB1bmVzOgogICAgICAgICAgICB0b3RhbF9wb2ludHMgPSBEZWNpbWFsKCIwIikKCiAgICAgICAgICAgIGZvciBtZXRyaWMgaW4gbWV0cmljcy52YWx1ZXMoKToKICAgICAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgICAgICB0YXJnZXQgPSBNb250aGx5VGFyZ2V0Lm9iamVjdHMuZ2V0KAogICAgICAgICAgICAgICAgICAgICAgICBwbGFuPXBsYW4sCiAgICAgICAgICAgICAgICAgICAgICAgIHVuZT11bmUsCiAgICAgICAgICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgZXhjZXB0IE1vbnRobHlUYXJnZXQuRG9lc05vdEV4aXN0OgogICAgICAgICAgICAgICAgICAgIGNvbnRpbnVlCgogICAgICAgICAgICAgICAgc291cmNlX3Jlc3VsdCwgXyA9IE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgICAgICAgICB1bmU9dW5lLAogICAgICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICAgICAgICAgIm1lYXN1cmVkX3ZhbHVlIjogTm9uZSwKICAgICAgICAgICAgICAgICAgICAgICAgInRhcmdldF92YWx1ZSI6IHRhcmdldC50YXJnZXRfdmFsdWUsCiAgICAgICAgICAgICAgICAgICAgICAgICJpc19hY2hpZXZlZCI6IEZhbHNlLAogICAgICAgICAgICAgICAgICAgICAgICAicG9pbnRzX2F3YXJkZWQiOiAwLAogICAgICAgICAgICAgICAgICAgICAgICAiY2FsY3VsYXRpb25fbm90ZSI6ICIiLAogICAgICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICAgICApCgogICAgICAgICAgICAgICAgc2NvcmUsIGNyZWF0ZWQgPSBNb250aGx5TWV0cmljU2NvcmUub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgICAgICAgICB1bmU9dW5lLAogICAgICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgICAgIG1vZGU9bW9kZSwKICAgICAgICAgICAgICAgICAgICBkZWZhdWx0cz17CiAgICAgICAgICAgICAgICAgICAgICAgICJtZWFzdXJlZF92YWx1ZSI6IHNvdXJjZV9yZXN1bHQubWVhc3VyZWRfdmFsdWUsCiAgICAgICAgICAgICAgICAgICAgICAgICJ0YXJnZXRfdmFsdWUiOiB0YXJnZXQudGFyZ2V0X3ZhbHVlLAogICAgICAgICAgICAgICAgICAgICAgICAiaXNfYWNoaWV2ZWQiOiBGYWxzZSwKICAgICAgICAgICAgICAgICAgICAgICAgInBvaW50c19hd2FyZGVkIjogMCwKICAgICAgICAgICAgICAgICAgICAgICAgImNhbGN1bGF0aW9uX25vdGUiOiAiIiwKICAgICAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgKQoKICAgICAgICAgICAgICAgIGlmIGNyZWF0ZWQ6CiAgICAgICAgICAgICAgICAgICAgbWV0cmljX3Njb3Jlc19jcmVhdGVkICs9IDEKICAgICAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICAgICAgbWV0cmljX3Njb3Jlc191cGRhdGVkICs9IDEKCiAgICAgICAgICAgICAgICBzY29yZS5tZWFzdXJlZF92YWx1ZSA9IHNvdXJjZV9yZXN1bHQubWVhc3VyZWRfdmFsdWUKICAgICAgICAgICAgICAgIHNjb3JlLnRhcmdldF92YWx1ZSA9IHRhcmdldC50YXJnZXRfdmFsdWUKCiAgICAgICAgICAgICAgICBpZiBtb2RlID09ICJtb2RvMSI6CiAgICAgICAgICAgICAgICAgICAgc2VsZi5hcHBseV9tb2RvMShzY29yZSwgbWV0cmljLCB0YXJnZXQpCiAgICAgICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgICAgIHNlbGYuYXBwbHlfbW9kbzIocGxhbiwgeWVhciwgbW9udGgsIHVuZSwgc2NvcmUsIG1ldHJpYywgdGFyZ2V0KQoKICAgICAgICAgICAgICAgIGlmIG1ldHJpYy5jb2RlID09IE1ldHJpY0RlZmluaXRpb24uQ09ERV9SRVNQVUVTVEFfUkVRUzoKICAgICAgICAgICAgICAgICAgICBzZWxmLmFwcGx5X21hbnVhbF9yZXF1aXJlbWVudHNfb3ZlcnJpZGUoCiAgICAgICAgICAgICAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgICAgICAgICAgICAgdW5lPXVuZSwKICAgICAgICAgICAgICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgICAgICAgICBtb250aD1tb250aCwKICAgICAgICAgICAgICAgICAgICAgICAgbWV0cmljX3Njb3JlPXNjb3JlLAogICAgICAgICAgICAgICAgICAgICkKCiAgICAgICAgICAgICAgICBzY29yZS5zYXZlKCkKICAgICAgICAgICAgICAgIHRvdGFsX3BvaW50cyArPSBEZWNpbWFsKHN0cihzY29yZS5wb2ludHNfYXdhcmRlZCBvciAwKSkKCiAgICAgICAgICAgIG1vZGVfc2NvcmVjYXJkLCBjcmVhdGVkID0gTW9udGhseU1vZGVTY29yZWNhcmQub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgcGxhbj1wbGFuLAogICAgICAgICAgICAgICAgdW5lPXVuZSwKICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgbW9kZT1tb2RlLAogICAgICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgICAgICJ0b3RhbF9wb2ludHMiOiB0b3RhbF9wb2ludHMsCiAgICAgICAgICAgICAgICAgICAgInF1YWxpZmllZF90aHJlc2hvbGQiOiA4MCwKICAgICAgICAgICAgICAgICAgICAiaXNfbW9udGhfcXVhbGlmaWVkIjogdG90YWxfcG9pbnRzID49IERlY2ltYWwoIjgwIiksCiAgICAgICAgICAgICAgICAgICAgInN1bW1hcnlfbm90ZSI6IGYiU2NvcmUgcmVjYWxjdWxhZG8gZW4ge21vZGV9IiwKICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICkKCiAgICAgICAgICAgIGlmIGNyZWF0ZWQ6CiAgICAgICAgICAgICAgICBtb2RlX3Njb3JlY2FyZHNfY3JlYXRlZCArPSAxCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBtb2RlX3Njb3JlY2FyZHNfdXBkYXRlZCArPSAxCgogICAgICAgICAgICBpZiBtb2RlX3Njb3JlY2FyZC5xdWFsaWZpZWRfdGhyZXNob2xkIGlzIE5vbmU6CiAgICAgICAgICAgICAgICBtb2RlX3Njb3JlY2FyZC5xdWFsaWZpZWRfdGhyZXNob2xkID0gODAKCiAgICAgICAgICAgIG1vZGVfc2NvcmVjYXJkLnRvdGFsX3BvaW50cyA9IHRvdGFsX3BvaW50cwogICAgICAgICAgICBtb2RlX3Njb3JlY2FyZC5pc19tb250aF9xdWFsaWZpZWQgPSB0b3RhbF9wb2ludHMgPj0gRGVjaW1hbCgKICAgICAgICAgICAgICAgIHN0cihtb2RlX3Njb3JlY2FyZC5xdWFsaWZpZWRfdGhyZXNob2xkKQogICAgICAgICAgICApCiAgICAgICAgICAgIG1vZGVfc2NvcmVjYXJkLnN1bW1hcnlfbm90ZSA9IGYiU2NvcmUgcmVjYWxjdWxhZG8gZW4ge21vZGV9IgogICAgICAgICAgICBtb2RlX3Njb3JlY2FyZC5zYXZlKCkKCiAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoCiAgICAgICAgICAgIGYiTW9udGhseU1ldHJpY1Njb3JlOiB7bWV0cmljX3Njb3Jlc19jcmVhdGVkfSBjcmVhZG9zLCAiCiAgICAgICAgICAgIGYie21ldHJpY19zY29yZXNfdXBkYXRlZH0gYWN0dWFsaXphZG9zIgogICAgICAgICkKICAgICAgICBzZWxmLnN0ZG91dC53cml0ZSgKICAgICAgICAgICAgZiJNb250aGx5TW9kZVNjb3JlY2FyZDoge21vZGVfc2NvcmVjYXJkc19jcmVhdGVkfSBjcmVhZG9zLCAiCiAgICAgICAgICAgIGYie21vZGVfc2NvcmVjYXJkc191cGRhdGVkfSBhY3R1YWxpemFkb3MiCiAgICAgICAgKQogICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKAogICAgICAgICAgICBzZWxmLnN0eWxlLlNVQ0NFU1MoCiAgICAgICAgICAgICAgICBmIlJlY2FsYyBQR0Mge3llYXJ9LXttb250aDowMmR9IGNvbXBsZXRhZG8gZW4ge21vZGV9LiIKICAgICAgICAgICAgKQogICAgICAgICkKCiAgICBkZWYgYXBwbHlfbW9kbzEoc2VsZiwgbWV0cmljX3Njb3JlLCBtZXRyaWMsIHRhcmdldCk6CiAgICAgICAgbWVhc3VyZWQgPSBtZXRyaWNfc2NvcmUubWVhc3VyZWRfdmFsdWUKICAgICAgICB0YXJnZXRfdmFsdWUgPSBtZXRyaWNfc2NvcmUudGFyZ2V0X3ZhbHVlCgogICAgICAgIGlmIG1lYXN1cmVkIGlzIG5vdCBOb25lIGFuZCB0YXJnZXRfdmFsdWUgaXMgbm90IE5vbmU6CiAgICAgICAgICAgIGlmIG1lYXN1cmVkID49IHRhcmdldF92YWx1ZToKICAgICAgICAgICAgICAgIG1ldHJpY19zY29yZS5pc19hY2hpZXZlZCA9IFRydWUKICAgICAgICAgICAgICAgIG1ldHJpY19zY29yZS5wb2ludHNfYXdhcmRlZCA9IHRhcmdldC5wb2ludHNfaWZfYWNoaWV2ZWQKICAgICAgICAgICAgICAgIG1ldHJpY19zY29yZS5jYWxjdWxhdGlvbl9ub3RlID0gIk1vZG8xIGN1bXBsZSBtZXRhIG9iamV0aXZvLiIKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIG1ldHJpY19zY29yZS5pc19hY2hpZXZlZCA9IEZhbHNlCiAgICAgICAgICAgICAgICBtZXRyaWNfc2NvcmUucG9pbnRzX2F3YXJkZWQgPSAwCiAgICAgICAgICAgICAgICBtZXRyaWNfc2NvcmUuY2FsY3VsYXRpb25fbm90ZSA9ICJNb2RvMSBubyBjdW1wbGUgbWV0YSBvYmpldGl2by4iCiAgICAgICAgICAgIHJldHVybgoKICAgICAgICBpZiBtZXRyaWMuY29kZSBpbiAoCiAgICAgICAgICAgIE1ldHJpY0RlZmluaXRpb24uQ09ERV9WRU5UQV9DUlVaQURBLAogICAgICAgICAgICBNZXRyaWNEZWZpbml0aW9uLkNPREVfUkVTUFVFU1RBX1JFUVMsCiAgICAgICAgKToKICAgICAgICAgICAgaWYgbWVhc3VyZWQgYW5kIG1lYXN1cmVkID49IERlY2ltYWwoIjEiKToKICAgICAgICAgICAgICAgIG1ldHJpY19zY29yZS5pc19hY2hpZXZlZCA9IFRydWUKICAgICAgICAgICAgICAgIG1ldHJpY19zY29yZS5wb2ludHNfYXdhcmRlZCA9IHRhcmdldC5wb2ludHNfaWZfYWNoaWV2ZWQKICAgICAgICAgICAgICAgIG1ldHJpY19zY29yZS5jYWxjdWxhdGlvbl9ub3RlID0gIk1vZG8xIGN1bXBsZSBjb25kaWNpw7NuIGJpbmFyaWEuIgogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgbWV0cmljX3Njb3JlLmlzX2FjaGlldmVkID0gRmFsc2UKICAgICAgICAgICAgICAgIG1ldHJpY19zY29yZS5wb2ludHNfYXdhcmRlZCA9IDAKICAgICAgICAgICAgICAgIG1ldHJpY19zY29yZS5jYWxjdWxhdGlvbl9ub3RlID0gIk1vZG8xIHNpbiBkYXRvcyBzdWZpY2llbnRlcyBvIG5vIGN1bXBsaWRhLiIKICAgICAgICBlbHNlOgogICAgICAgICAgICBtZXRyaWNfc2NvcmUuaXNfYWNoaWV2ZWQgPSBGYWxzZQogICAgICAgICAgICBtZXRyaWNfc2NvcmUucG9pbnRzX2F3YXJkZWQgPSAwCiAgICAgICAgICAgIG1ldHJpY19zY29yZS5jYWxjdWxhdGlvbl9ub3RlID0gIk1vZG8xIHNpbiB2YWxvciBtZWRpZG8gcGFyYSBlc3RlIG1lcy4iCgogICAgZGVmIGFwcGx5X21vZG8yKHNlbGYsIHBsYW4sIHllYXIsIG1vbnRoLCB1bmUsIG1ldHJpY19zY29yZSwgbWV0cmljLCB0YXJnZXQpOgogICAgICAgIGlmIG1ldHJpYy5jb2RlID09IE1ldHJpY0RlZmluaXRpb24uQ09ERV9SRVNQVUVTVEFfUkVRUzoKICAgICAgICAgICAgc2VsZi5hcHBseV9tb2RvMShtZXRyaWNfc2NvcmUsIG1ldHJpYywgdGFyZ2V0KQogICAgICAgICAgICBtZXRyaWNfc2NvcmUuY2FsY3VsYXRpb25fbm90ZSA9ICgKICAgICAgICAgICAgICAgIGYiTW9kbzIgcmVxdWVyaW1pZW50b3Mgc2UgY2FsY3VsYW4gaWd1YWwgcXVlIG1vZG8xLiAiCiAgICAgICAgICAgICAgICBmInttZXRyaWNfc2NvcmUuY2FsY3VsYXRpb25fbm90ZX0iCiAgICAgICAgICAgICkKICAgICAgICAgICAgcmV0dXJuCgogICAgICAgIGlmIG1ldHJpYy5jb2RlIG5vdCBpbiBzZWxmLlNDT1JBQkxFX01PREUyX0NPREVTOgogICAgICAgICAgICBzZWxmLmFwcGx5X21vZG8xKG1ldHJpY19zY29yZSwgbWV0cmljLCB0YXJnZXQpCiAgICAgICAgICAgIG1ldHJpY19zY29yZS5jYWxjdWxhdGlvbl9ub3RlID0gKAogICAgICAgICAgICAgICAgZiJNb2RvMiBtw6l0cmljYSBubyBjb25maWd1cmFkYSBwYXJhIHByb3BvcmNpb25hbGlkYWQuICIKICAgICAgICAgICAgICAgIGYie21ldHJpY19zY29yZS5jYWxjdWxhdGlvbl9ub3RlfSIKICAgICAgICAgICAgKQogICAgICAgICAgICByZXR1cm4KCiAgICAgICAgbWVhc3VyZWQgPSBtZXRyaWNfc2NvcmUubWVhc3VyZWRfdmFsdWUgb3IgRGVjaW1hbCgiMCIpCiAgICAgICAgdGFyZ2V0X3ZhbHVlID0gbWV0cmljX3Njb3JlLnRhcmdldF92YWx1ZSBvciBEZWNpbWFsKCIwIikKICAgICAgICBmdWxsX3BvaW50cyA9IERlY2ltYWwoc3RyKHRhcmdldC5wb2ludHNfaWZfYWNoaWV2ZWQgb3IgMCkpCgogICAgICAgIGlmIHRhcmdldF92YWx1ZSA8PSBEZWNpbWFsKCIwIik6CiAgICAgICAgICAgIG1ldHJpY19zY29yZS5pc19hY2hpZXZlZCA9IEZhbHNlCiAgICAgICAgICAgIG1ldHJpY19zY29yZS5wb2ludHNfYXdhcmRlZCA9IERlY2ltYWwoIjAiKQogICAgICAgICAgICBtZXRyaWNfc2NvcmUuY2FsY3VsYXRpb25fbm90ZSA9ICJNb2RvMiBtZXRhIHZhY8OtYSBvIGlndWFsIGEgY2Vyby4iCiAgICAgICAgICAgIHJldHVybgoKICAgICAgICByZXNlcnZlX3BvaW50c19hdmFpbGFibGUgPSBzZWxmLmdldF9hdmFpbGFibGVfcmVzZXJ2ZSgKICAgICAgICAgICAgcGxhbiwgdW5lLCBtZXRyaWMsIHllYXIsIG1vbnRoCiAgICAgICAgKQoKICAgICAgICByYXdfcG9pbnRzID0gKAogICAgICAgICAgICBmdWxsX3BvaW50cyAqIChtZWFzdXJlZCAvIHRhcmdldF92YWx1ZSkKICAgICAgICApLnF1YW50aXplKERlY2ltYWwoIjAuMDAwMSIpLCByb3VuZGluZz1ST1VORF9IQUxGX1VQKQoKICAgICAgICBhdmFpbGFibGVfcG9pbnRzID0gcmF3X3BvaW50cyArIHJlc2VydmVfcG9pbnRzX2F2YWlsYWJsZQogICAgICAgIHBvaW50c19hd2FyZGVkID0gbWluKGZ1bGxfcG9pbnRzLCBhdmFpbGFibGVfcG9pbnRzKS5xdWFudGl6ZSgKICAgICAgICAgICAgRGVjaW1hbCgiMC4wMDAxIiksIHJvdW5kaW5nPVJPVU5EX0hBTEZfVVAKICAgICAgICApCgogICAgICAgIHJlc2VydmVfcG9pbnRzX3RvX3VzZSA9IG1pbigKICAgICAgICAgICAgcmVzZXJ2ZV9wb2ludHNfYXZhaWxhYmxlLAogICAgICAgICAgICBtYXgoRGVjaW1hbCgiMCIpLCBwb2ludHNfYXdhcmRlZCAtIHJhd19wb2ludHMpCiAgICAgICAgKS5xdWFudGl6ZShEZWNpbWFsKCIwLjAwMDEiKSwgcm91bmRpbmc9Uk9VTkRfSEFMRl9VUCkKCiAgICAgICAgaWYgcmVzZXJ2ZV9wb2ludHNfdG9fdXNlID4gMDoKICAgICAgICAgICAgc2VsZi5jb25zdW1lX3Jlc2VydmUoCiAgICAgICAgICAgICAgICBwbGFuLCB1bmUsIG1ldHJpYywgeWVhciwgbW9udGgsIHJlc2VydmVfcG9pbnRzX3RvX3VzZQogICAgICAgICAgICApCgogICAgICAgIGV4dHJhX3BvaW50c19jdXJyZW50X21vbnRoID0gbWF4KAogICAgICAgICAgICBEZWNpbWFsKCIwIiksIHJhd19wb2ludHMgLSBmdWxsX3BvaW50cwogICAgICAgICkucXVhbnRpemUoRGVjaW1hbCgiMC4wMDAxIiksIHJvdW5kaW5nPVJPVU5EX0hBTEZfVVApCgogICAgICAgIGlmIGV4dHJhX3BvaW50c19jdXJyZW50X21vbnRoID4gMDoKICAgICAgICAgICAgTWV0cmljUmVzZXJ2ZS5vYmplY3RzLmNyZWF0ZSgKICAgICAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgICAgIHVuZT11bmUsCiAgICAgICAgICAgICAgICBtZXRyaWM9bWV0cmljLAogICAgICAgICAgICAgICAgc291cmNlX3llYXI9eWVhciwKICAgICAgICAgICAgICAgIHNvdXJjZV9tb250aD1tb250aCwKICAgICAgICAgICAgICAgIGFtb3VudD1leHRyYV9wb2ludHNfY3VycmVudF9tb250aCwKICAgICAgICAgICAgICAgIHJlbWFpbmluZz1leHRyYV9wb2ludHNfY3VycmVudF9tb250aCwKICAgICAgICAgICAgKQoKICAgICAgICBtZXRyaWNfc2NvcmUuaXNfYWNoaWV2ZWQgPSBwb2ludHNfYXdhcmRlZCA+PSBmdWxsX3BvaW50cwogICAgICAgIG1ldHJpY19zY29yZS5wb2ludHNfYXdhcmRlZCA9IHBvaW50c19hd2FyZGVkCgogICAgICAgIHJlc2VydmVfcG9pbnRzX3JlbWFpbmluZyA9ICgKICAgICAgICAgICAgcmVzZXJ2ZV9wb2ludHNfYXZhaWxhYmxlIC0gcmVzZXJ2ZV9wb2ludHNfdG9fdXNlICsgZXh0cmFfcG9pbnRzX2N1cnJlbnRfbW9udGgKICAgICAgICApLnF1YW50aXplKERlY2ltYWwoIjAuMDAwMSIpLCByb3VuZGluZz1ST1VORF9IQUxGX1VQKQoKICAgICAgICBtZXRyaWNfc2NvcmUuY2FsY3VsYXRpb25fbm90ZSA9ICgKICAgICAgICAgICAgZiJNb2RvMiBtZWRpZG89e21lYXN1cmVkfSwgIgogICAgICAgICAgICBmIm1ldGE9e3RhcmdldF92YWx1ZX0sICIKICAgICAgICAgICAgZiJwdW50b3NfdGVvcmljb3M9e3Jhd19wb2ludHN9LCAiCiAgICAgICAgICAgIGYicmVzZXJ2YV9wdW50b3NfZGlzcG9uaWJsZT17cmVzZXJ2ZV9wb2ludHNfYXZhaWxhYmxlfSwgIgogICAgICAgICAgICBmInJlc2VydmFfcHVudG9zX3VzYWRhPXtyZXNlcnZlX3BvaW50c190b191c2V9LCAiCiAgICAgICAgICAgIGYicHVudG9zX290b3JnYWRvcz17cG9pbnRzX2F3YXJkZWR9LCAiCiAgICAgICAgICAgIGYiZXhjZWRlbnRlX3B1bnRvc19nZW5lcmFkbz17ZXh0cmFfcG9pbnRzX2N1cnJlbnRfbW9udGh9LCAiCiAgICAgICAgICAgIGYicmVzZXJ2YV9wdW50b3NfZmluYWw9e3Jlc2VydmVfcG9pbnRzX3JlbWFpbmluZ30uIgogICAgICAgICkKCiAgICBkZWYgYXBwbHlfbWFudWFsX3JlcXVpcmVtZW50c19vdmVycmlkZSgKICAgICAgICBzZWxmLCBwbGFuLCB1bmUsIHllYXIsIG1vbnRoLCBtZXRyaWNfc2NvcmUKICAgICk6CiAgICAgICAgdHJ5OgogICAgICAgICAgICBtcmMgPSBNYW51YWxSZXF1aXJlbWVudHNDb21wbGlhbmNlLm9iamVjdHMuZ2V0KAogICAgICAgICAgICAgICAgcGxhbj1wbGFuLAogICAgICAgICAgICAgICAgdW5lPXVuZSwKICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICApCiAgICAgICAgZXhjZXB0IE1hbnVhbFJlcXVpcmVtZW50c0NvbXBsaWFuY2UuRG9lc05vdEV4aXN0OgogICAgICAgICAgICByZXR1cm4KCiAgICAgICAgaWYgbXJjLmlzX2NvbXBsaWFudCBpcyBGYWxzZToKICAgICAgICAgICAgbWV0cmljX3Njb3JlLnBvaW50c19hd2FyZGVkID0gMAogICAgICAgICAgICBtZXRyaWNfc2NvcmUuaXNfYWNoaWV2ZWQgPSBGYWxzZQogICAgICAgICAgICBtZXRyaWNfc2NvcmUuY2FsY3VsYXRpb25fbm90ZSA9ICgKICAgICAgICAgICAgICAgICJNYXJjYWRvIGNvbW8gbm8gY3VtcGxpZG8gZW4gY3VtcGxpbWllbnRvIG1hbnVhbDsgIgogICAgICAgICAgICAgICAgInB1bnRvcyByZW1vdmlkb3MuIgogICAgICAgICAgICApCgogICAgZGVmIGdldF9hdmFpbGFibGVfcmVzZXJ2ZShzZWxmLCBwbGFuLCB1bmUsIG1ldHJpYywgeWVhciwgbW9udGgpOgogICAgICAgIHJlc2VydmVzID0gTWV0cmljUmVzZXJ2ZS5vYmplY3RzLmZpbHRlcigKICAgICAgICAgICAgcGxhbj1wbGFuLAogICAgICAgICAgICB1bmU9dW5lLAogICAgICAgICAgICBtZXRyaWM9bWV0cmljLAogICAgICAgICAgICByZW1haW5pbmdfX2d0PTAsCiAgICAgICAgKS5leGNsdWRlKAogICAgICAgICAgICBzb3VyY2VfeWVhcj15ZWFyLAogICAgICAgICAgICBzb3VyY2VfbW9udGg9bW9udGgsCiAgICAgICAgKQoKICAgICAgICB0b3RhbCA9IERlY2ltYWwoIjAiKQogICAgICAgIGZvciByZXNlcnZlIGluIHJlc2VydmVzOgogICAgICAgICAgICB0b3RhbCArPSByZXNlcnZlLnJlbWFpbmluZyBvciBEZWNpbWFsKCIwIikKICAgICAgICByZXR1cm4gdG90YWwKCiAgICBkZWYgY29uc3VtZV9yZXNlcnZlKHNlbGYsIHBsYW4sIHVuZSwgbWV0cmljLCB5ZWFyLCBtb250aCwgYW1vdW50X3RvX2NvbnN1bWUpOgogICAgICAgIHBlbmRpbmcgPSBEZWNpbWFsKHN0cihhbW91bnRfdG9fY29uc3VtZSkpCgogICAgICAgIHJlc2VydmVzID0gKAogICAgICAgICAgICBNZXRyaWNSZXNlcnZlLm9iamVjdHMuZmlsdGVyKAogICAgICAgICAgICAgICAgcGxhbj1wbGFuLAogICAgICAgICAgICAgICAgdW5lPXVuZSwKICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICByZW1haW5pbmdfX2d0PTAsCiAgICAgICAgICAgICkKICAgICAgICAgICAgLmV4Y2x1ZGUoCiAgICAgICAgICAgICAgICBzb3VyY2VfeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgc291cmNlX21vbnRoPW1vbnRoLAogICAgICAgICAgICApCiAgICAgICAgICAgIC5vcmRlcl9ieSgic291cmNlX3llYXIiLCAic291cmNlX21vbnRoIiwgImlkIikKICAgICAgICApCgogICAgICAgIGZvciByZXNlcnZlIGluIHJlc2VydmVzOgogICAgICAgICAgICBpZiBwZW5kaW5nIDw9IERlY2ltYWwoIjAiKToKICAgICAgICAgICAgICAgIGJyZWFrCgogICAgICAgICAgICBhdmFpbGFibGUgPSByZXNlcnZlLnJlbWFpbmluZyBvciBEZWNpbWFsKCIwIikKICAgICAgICAgICAgdXNlZCA9IG1pbihhdmFpbGFibGUsIHBlbmRpbmcpCiAgICAgICAgICAgIHJlc2VydmUucmVtYWluaW5nID0gYXZhaWxhYmxlIC0gdXNlZAogICAgICAgICAgICByZXNlcnZlLnNhdmUodXBkYXRlX2ZpZWxkcz1bInJlbWFpbmluZyJdKQogICAgICAgICAgICBwZW5kaW5nIC09IHVzZWQ=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/management/commands/seed_pgc.py
PATH_JSON="core/management/commands/seed_pgc.py"
FILENAME=seed_pgc.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=262
SIZE_BYTES_UTF8=9631
CONTENT_SHA256=c6135b0470fdc4ce580c471a51431c8708f22a20e72d3096116c5078c2973dce
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
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import UNE, MetricDefinition, Currency
from pgc.models import PGCPlan, MonthlyTarget


class Command(BaseCommand):
    help = "Carga catálogo base y metas mensuales PGC 2026"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Iniciando seed PGC 2026..."))

        self._seed_currencies()
        une_map = self._seed_unes()
        metric_map = self._seed_metrics()
        plan = self._seed_plan()
        self._seed_monthly_targets(plan, une_map, metric_map)

        self.stdout.write(self.style.SUCCESS("Seed PGC 2026 completado."))

    def _seed_currencies(self):
        data = [
            {"code": "USD", "name": "Dólar estadounidense", "symbol": "$"},
            {"code": "GTQ", "name": "Quetzal guatemalteco", "symbol": "Q"},
        ]
        for item in data:
            obj, _ = Currency.objects.update_or_create(
                code=item["code"],
                defaults={
                    "name": item["name"],
                    "symbol": item["symbol"],
                    "is_active": True,
                },
            )
            self.stdout.write(f"Currency OK: {obj.code}")
            {"code": "LEASING", "name_es": "Leasing", "sort_order": 2},
            {"code": "INSURANCE", "name_es": "Insurance", "sort_order": 3},
            {"code": "INVESTMENT", "name_es": "Inversiones", "sort_order": 4},
        ]

        result = {}
        for item in data:
            obj, _ = UNE.objects.update_or_create(
                code=item["code"],
                defaults={
                    "name_es": item["name_es"],
                    "sort_order": item["sort_order"],
                },
            )
            result[item["code"]] = obj
            self.stdout.write(f"UNE OK: {obj.code}")
        return result

    def _seed_metrics(self):
        data = [
            {
                "code": "INGRESOS",
                "name": "Ingresos",
                "description": "Meta mensual de ingresos por UNE",
            },
            {
                "code": "CLIENTES_NUEVOS",
                "name": "Clientes nuevos",
                "description": "Cantidad mensual de clientes nuevos por UNE",
            },
            {
                "code": "VENTA_CRUZADA",
                "name": "Venta cruzada",
                "description": "Cumple si la UNE refiere al menos un cliente a otra UNE en el mes",
            },
            {
                "code": "RESPUESTA_REQS",
                "name": "Respuesta a requerimientos",
                "description": "Cumplimiento manual mensual por UNE; en inversiones no aplica puntos",
            },
        ]

        result = {}
        for item in data:
            obj, _ = MetricDefinition.objects.update_or_create(
                code=item["code"],
                defaults={
                    "name": item["name"],
                    "description": item["description"],
                },
            )
            result[item["code"]] = obj
            self.stdout.write(f"Metric OK: {obj.code}")
        return result

    def _seed_plan(self):
        obj, _ = PGCPlan.objects.update_or_create(
            year=2026,
            defaults={
                "name": "PGC 2026",
                "is_active": True,
                "notes": "Plan anual PGC 2026 cargado desde especificación inicial",
            },
        )
        self.stdout.write(f"Plan OK: {obj}")
        return obj

    def _seed_monthly_targets(self, plan, une_map, metric_map):
        monthly_data = {
            "FACTORING": {
                "INGRESOS": {
                    "annual": Decimal("11000"),
                    "points": 70,
                    "months": [660, 1100, 770, 440, 770, 770, 1650, 770, 330, 440, 1650, 1650],
                },
                "CLIENTES_NUEVOS": {
                    "annual": Decimal("12"),
                    "points": 15,
                    "months": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                },
                "VENTA_CRUZADA": {
                    "annual": None,
                    "points": 10,
                    "months": [1] * 12,
                },
                "RESPUESTA_REQS": {
                    "annual": None,
                    "points": 5,
                    "months": [1] * 12,
                },
            },
            "LEASING": {
                "INGRESOS": {
                    "annual": Decimal("1200"),
                    "points": 70,
                    "months": [96, 84, 84, 84, 96, 84, 108, 108, 108, 120, 108, 120],
                },
                "CLIENTES_NUEVOS": {
                    "annual": Decimal("15"),
                    "points": 15,
                    "months": [0, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2],
                },
                "VENTA_CRUZADA": {
                    "annual": None,
                    "points": 10,
                    "months": [1] * 12,
                },
                "RESPUESTA_REQS": {
                    "annual": None,
                    "points": 5,
                    "months": [1] * 12,
                },
            },
            "INSURANCE": {
                "INGRESOS": {
                    "annual": Decimal("119.0"),
                    "points": 70,
                    "months": [
                        Decimal("6.746"),
                        Decimal("5.765"),
                        Decimal("5.898"),
                        Decimal("6.050"),
                        Decimal("7.620"),
                        Decimal("7.570"),
                        Decimal("9.760"),
                        Decimal("10.330"),
                        Decimal("11.850"),
                        Decimal("17.182"),
                        Decimal("16.372"),
                        Decimal("13.762"),
                    ],
                },
                "CLIENTES_NUEVOS": {
                    "annual": Decimal("44"),
                    "points": 15,
                    "months": [1, 2, 3, 5, 3, 4, 6, 3, 4, 6, 3, 4],
                },
                "VENTA_CRUZADA": {
                    "annual": None,
                    "points": 10,
                    "months": [1] * 12,
                },
                "RESPUESTA_REQS": {
                    "annual": None,
                    "points": 5,
                    "months": [1] * 12,
                },
            },
            "INVESTMENT": {
                "INGRESOS": {
                    "annual": Decimal("16.2"),
                    "points": 75,
                    "months": [
                        Decimal("0.200"),
                        Decimal("0.200"),
                        Decimal("0.300"),
                        Decimal("3.000"),
                        Decimal("0.600"),
                        Decimal("1.000"),
                        Decimal("1.000"),
                        Decimal("1.000"),
                        Decimal("1.000"),
                        Decimal("2.000"),
                        Decimal("2.900"),
                        Decimal("3.000"),
                    ],
                },
                "CLIENTES_NUEVOS": {
                    "annual": Decimal("20"),
                    "points": 15,
                    "months": [1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2],
                },
                "VENTA_CRUZADA": {
                    "annual": None,
                    "points": 10,
                    "months": [1] * 12,
                },
                "RESPUESTA_REQS": {
                    "annual": None,
                    "points": 0,
                    "months": [0] * 12,
                },
            },
        }

        total_rows = 0

        for une_code, metrics in monthly_data.items():
            une = une_map[une_code]

            for metric_code, payload in metrics.items():
                metric = metric_map[metric_code]
                annual_value = payload["annual"]
                points = payload["points"]

                for month_index, target in enumerate(payload["months"], start=1):
                    MonthlyTarget.objects.update_or_create(
                        plan=plan,
                        une=une,
                        metric=metric,
                        year=2026,
                        month=month_index,
                        defaults={
                            "target_value": Decimal(str(target)) if target is not None else None,
                            "points_if_achieved": points,
                            "reference_annual_value": annual_value,
                            "notes": self._build_note(metric_code, une_code),
                        },
                    )
                    total_rows += 1

        self.stdout.write(f"MonthlyTarget OK: {total_rows} registros")

    def _build_note(self, metric_code, une_code):
        if metric_code == "VENTA_CRUZADA":
            return "Cumple con al menos 1 referencia enviada a cualquier otra UNE en el mes."
        if metric_code == "RESPUESTA_REQS" and une_code == "INVERSIONES":
            return "No aplica puntos para Inversiones en el MVP."
        if metric_code == "RESPUESTA_REQS":
            return "Cumplimiento manual mensual; si incumple, registrar incidencia."
        if metric_code == "INGRESOS" and une_code == "INVERSIONES":
            return "Para Inversiones, el ingreso mensual se calcula sumando montos del archivo de clientes nuevos, sean nuevos o no."
        return ""
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from decimal import Decimal
00002|from django.core.management.base import BaseCommand
00003|from django.db import transaction
00004|
00005|from core.models import UNE, MetricDefinition, Currency
00006|from pgc.models import PGCPlan, MonthlyTarget
00007|
00008|
00009|class Command(BaseCommand):
00010|    help = "Carga catálogo base y metas mensuales PGC 2026"
00011|
00012|    @transaction.atomic
00013|    def handle(self, *args, **options):
00014|        self.stdout.write(self.style.WARNING("Iniciando seed PGC 2026..."))
00015|
00016|        self._seed_currencies()
00017|        une_map = self._seed_unes()
00018|        metric_map = self._seed_metrics()
00019|        plan = self._seed_plan()
00020|        self._seed_monthly_targets(plan, une_map, metric_map)
00021|
00022|        self.stdout.write(self.style.SUCCESS("Seed PGC 2026 completado."))
00023|
00024|    def _seed_currencies(self):
00025|        data = [
00026|            {"code": "USD", "name": "Dólar estadounidense", "symbol": "$"},
00027|            {"code": "GTQ", "name": "Quetzal guatemalteco", "symbol": "Q"},
00028|        ]
00029|        for item in data:
00030|            obj, _ = Currency.objects.update_or_create(
00031|                code=item["code"],
00032|                defaults={
00033|                    "name": item["name"],
00034|                    "symbol": item["symbol"],
00035|                    "is_active": True,
00036|                },
00037|            )
00038|            self.stdout.write(f"Currency OK: {obj.code}")
00039|            {"code": "LEASING", "name_es": "Leasing", "sort_order": 2},
00040|            {"code": "INSURANCE", "name_es": "Insurance", "sort_order": 3},
00041|            {"code": "INVESTMENT", "name_es": "Inversiones", "sort_order": 4},
00042|        ]
00043|
00044|        result = {}
00045|        for item in data:
00046|            obj, _ = UNE.objects.update_or_create(
00047|                code=item["code"],
00048|                defaults={
00049|                    "name_es": item["name_es"],
00050|                    "sort_order": item["sort_order"],
00051|                },
00052|            )
00053|            result[item["code"]] = obj
00054|            self.stdout.write(f"UNE OK: {obj.code}")
00055|        return result
00056|
00057|    def _seed_metrics(self):
00058|        data = [
00059|            {
00060|                "code": "INGRESOS",
00061|                "name": "Ingresos",
00062|                "description": "Meta mensual de ingresos por UNE",
00063|            },
00064|            {
00065|                "code": "CLIENTES_NUEVOS",
00066|                "name": "Clientes nuevos",
00067|                "description": "Cantidad mensual de clientes nuevos por UNE",
00068|            },
00069|            {
00070|                "code": "VENTA_CRUZADA",
00071|                "name": "Venta cruzada",
00072|                "description": "Cumple si la UNE refiere al menos un cliente a otra UNE en el mes",
00073|            },
00074|            {
00075|                "code": "RESPUESTA_REQS",
00076|                "name": "Respuesta a requerimientos",
00077|                "description": "Cumplimiento manual mensual por UNE; en inversiones no aplica puntos",
00078|            },
00079|        ]
00080|
00081|        result = {}
00082|        for item in data:
00083|            obj, _ = MetricDefinition.objects.update_or_create(
00084|                code=item["code"],
00085|                defaults={
00086|                    "name": item["name"],
00087|                    "description": item["description"],
00088|                },
00089|            )
00090|            result[item["code"]] = obj
00091|            self.stdout.write(f"Metric OK: {obj.code}")
00092|        return result
00093|
00094|    def _seed_plan(self):
00095|        obj, _ = PGCPlan.objects.update_or_create(
00096|            year=2026,
00097|            defaults={
00098|                "name": "PGC 2026",
00099|                "is_active": True,
00100|                "notes": "Plan anual PGC 2026 cargado desde especificación inicial",
00101|            },
00102|        )
00103|        self.stdout.write(f"Plan OK: {obj}")
00104|        return obj
00105|
00106|    def _seed_monthly_targets(self, plan, une_map, metric_map):
00107|        monthly_data = {
00108|            "FACTORING": {
00109|                "INGRESOS": {
00110|                    "annual": Decimal("11000"),
00111|                    "points": 70,
00112|                    "months": [660, 1100, 770, 440, 770, 770, 1650, 770, 330, 440, 1650, 1650],
00113|                },
00114|                "CLIENTES_NUEVOS": {
00115|                    "annual": Decimal("12"),
00116|                    "points": 15,
00117|                    "months": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
00118|                },
00119|                "VENTA_CRUZADA": {
00120|                    "annual": None,
00121|                    "points": 10,
00122|                    "months": [1] * 12,
00123|                },
00124|                "RESPUESTA_REQS": {
00125|                    "annual": None,
00126|                    "points": 5,
00127|                    "months": [1] * 12,
00128|                },
00129|            },
00130|            "LEASING": {
00131|                "INGRESOS": {
00132|                    "annual": Decimal("1200"),
00133|                    "points": 70,
00134|                    "months": [96, 84, 84, 84, 96, 84, 108, 108, 108, 120, 108, 120],
00135|                },
00136|                "CLIENTES_NUEVOS": {
00137|                    "annual": Decimal("15"),
00138|                    "points": 15,
00139|                    "months": [0, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2],
00140|                },
00141|                "VENTA_CRUZADA": {
00142|                    "annual": None,
00143|                    "points": 10,
00144|                    "months": [1] * 12,
00145|                },
00146|                "RESPUESTA_REQS": {
00147|                    "annual": None,
00148|                    "points": 5,
00149|                    "months": [1] * 12,
00150|                },
00151|            },
00152|            "INSURANCE": {
00153|                "INGRESOS": {
00154|                    "annual": Decimal("119.0"),
00155|                    "points": 70,
00156|                    "months": [
00157|                        Decimal("6.746"),
00158|                        Decimal("5.765"),
00159|                        Decimal("5.898"),
00160|                        Decimal("6.050"),
00161|                        Decimal("7.620"),
00162|                        Decimal("7.570"),
00163|                        Decimal("9.760"),
00164|                        Decimal("10.330"),
00165|                        Decimal("11.850"),
00166|                        Decimal("17.182"),
00167|                        Decimal("16.372"),
00168|                        Decimal("13.762"),
00169|                    ],
00170|                },
00171|                "CLIENTES_NUEVOS": {
00172|                    "annual": Decimal("44"),
00173|                    "points": 15,
00174|                    "months": [1, 2, 3, 5, 3, 4, 6, 3, 4, 6, 3, 4],
00175|                },
00176|                "VENTA_CRUZADA": {
00177|                    "annual": None,
00178|                    "points": 10,
00179|                    "months": [1] * 12,
00180|                },
00181|                "RESPUESTA_REQS": {
00182|                    "annual": None,
00183|                    "points": 5,
00184|                    "months": [1] * 12,
00185|                },
00186|            },
00187|            "INVESTMENT": {
00188|                "INGRESOS": {
00189|                    "annual": Decimal("16.2"),
00190|                    "points": 75,
00191|                    "months": [
00192|                        Decimal("0.200"),
00193|                        Decimal("0.200"),
00194|                        Decimal("0.300"),
00195|                        Decimal("3.000"),
00196|                        Decimal("0.600"),
00197|                        Decimal("1.000"),
00198|                        Decimal("1.000"),
00199|                        Decimal("1.000"),
00200|                        Decimal("1.000"),
00201|                        Decimal("2.000"),
00202|                        Decimal("2.900"),
00203|                        Decimal("3.000"),
00204|                    ],
00205|                },
00206|                "CLIENTES_NUEVOS": {
00207|                    "annual": Decimal("20"),
00208|                    "points": 15,
00209|                    "months": [1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2],
00210|                },
00211|                "VENTA_CRUZADA": {
00212|                    "annual": None,
00213|                    "points": 10,
00214|                    "months": [1] * 12,
00215|                },
00216|                "RESPUESTA_REQS": {
00217|                    "annual": None,
00218|                    "points": 0,
00219|                    "months": [0] * 12,
00220|                },
00221|            },
00222|        }
00223|
00224|        total_rows = 0
00225|
00226|        for une_code, metrics in monthly_data.items():
00227|            une = une_map[une_code]
00228|
00229|            for metric_code, payload in metrics.items():
00230|                metric = metric_map[metric_code]
00231|                annual_value = payload["annual"]
00232|                points = payload["points"]
00233|
00234|                for month_index, target in enumerate(payload["months"], start=1):
00235|                    MonthlyTarget.objects.update_or_create(
00236|                        plan=plan,
00237|                        une=une,
00238|                        metric=metric,
00239|                        year=2026,
00240|                        month=month_index,
00241|                        defaults={
00242|                            "target_value": Decimal(str(target)) if target is not None else None,
00243|                            "points_if_achieved": points,
00244|                            "reference_annual_value": annual_value,
00245|                            "notes": self._build_note(metric_code, une_code),
00246|                        },
00247|                    )
00248|                    total_rows += 1
00249|
00250|        self.stdout.write(f"MonthlyTarget OK: {total_rows} registros")
00251|
00252|    def _build_note(self, metric_code, une_code):
00253|        if metric_code == "VENTA_CRUZADA":
00254|            return "Cumple con al menos 1 referencia enviada a cualquier otra UNE en el mes."
00255|        if metric_code == "RESPUESTA_REQS" and une_code == "INVERSIONES":
00256|            return "No aplica puntos para Inversiones en el MVP."
00257|        if metric_code == "RESPUESTA_REQS":
00258|            return "Cumplimiento manual mensual; si incumple, registrar incidencia."
00259|        if metric_code == "INGRESOS" and une_code == "INVERSIONES":
00260|            return "Para Inversiones, el ingreso mensual se calcula sumando montos del archivo de clientes nuevos, sean nuevos o no."
00261|        return ""
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsCmZyb20gZGphbmdvLmNvcmUubWFuYWdlbWVudC5iYXNlIGltcG9ydCBCYXNlQ29tbWFuZApmcm9tIGRqYW5nby5kYiBpbXBvcnQgdHJhbnNhY3Rpb24KCmZyb20gY29yZS5tb2RlbHMgaW1wb3J0IFVORSwgTWV0cmljRGVmaW5pdGlvbiwgQ3VycmVuY3kKZnJvbSBwZ2MubW9kZWxzIGltcG9ydCBQR0NQbGFuLCBNb250aGx5VGFyZ2V0CgoKY2xhc3MgQ29tbWFuZChCYXNlQ29tbWFuZCk6CiAgICBoZWxwID0gIkNhcmdhIGNhdMOhbG9nbyBiYXNlIHkgbWV0YXMgbWVuc3VhbGVzIFBHQyAyMDI2IgoKICAgIEB0cmFuc2FjdGlvbi5hdG9taWMKICAgIGRlZiBoYW5kbGUoc2VsZiwgKmFyZ3MsICoqb3B0aW9ucyk6CiAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoc2VsZi5zdHlsZS5XQVJOSU5HKCJJbmljaWFuZG8gc2VlZCBQR0MgMjAyNi4uLiIpKQoKICAgICAgICBzZWxmLl9zZWVkX2N1cnJlbmNpZXMoKQogICAgICAgIHVuZV9tYXAgPSBzZWxmLl9zZWVkX3VuZXMoKQogICAgICAgIG1ldHJpY19tYXAgPSBzZWxmLl9zZWVkX21ldHJpY3MoKQogICAgICAgIHBsYW4gPSBzZWxmLl9zZWVkX3BsYW4oKQogICAgICAgIHNlbGYuX3NlZWRfbW9udGhseV90YXJnZXRzKHBsYW4sIHVuZV9tYXAsIG1ldHJpY19tYXApCgogICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKHNlbGYuc3R5bGUuU1VDQ0VTUygiU2VlZCBQR0MgMjAyNiBjb21wbGV0YWRvLiIpKQoKICAgIGRlZiBfc2VlZF9jdXJyZW5jaWVzKHNlbGYpOgogICAgICAgIGRhdGEgPSBbCiAgICAgICAgICAgIHsiY29kZSI6ICJVU0QiLCAibmFtZSI6ICJEw7NsYXIgZXN0YWRvdW5pZGVuc2UiLCAic3ltYm9sIjogIiQifSwKICAgICAgICAgICAgeyJjb2RlIjogIkdUUSIsICJuYW1lIjogIlF1ZXR6YWwgZ3VhdGVtYWx0ZWNvIiwgInN5bWJvbCI6ICJRIn0sCiAgICAgICAgXQogICAgICAgIGZvciBpdGVtIGluIGRhdGE6CiAgICAgICAgICAgIG9iaiwgXyA9IEN1cnJlbmN5Lm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgICAgIGNvZGU9aXRlbVsiY29kZSJdLAogICAgICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgICAgICJuYW1lIjogaXRlbVsibmFtZSJdLAogICAgICAgICAgICAgICAgICAgICJzeW1ib2wiOiBpdGVtWyJzeW1ib2wiXSwKICAgICAgICAgICAgICAgICAgICAiaXNfYWN0aXZlIjogVHJ1ZSwKICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICkKICAgICAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoZiJDdXJyZW5jeSBPSzoge29iai5jb2RlfSIpCiAgICAgICAgICAgIHsiY29kZSI6ICJMRUFTSU5HIiwgIm5hbWVfZXMiOiAiTGVhc2luZyIsICJzb3J0X29yZGVyIjogMn0sCiAgICAgICAgICAgIHsiY29kZSI6ICJJTlNVUkFOQ0UiLCAibmFtZV9lcyI6ICJJbnN1cmFuY2UiLCAic29ydF9vcmRlciI6IDN9LAogICAgICAgICAgICB7ImNvZGUiOiAiSU5WRVNUTUVOVCIsICJuYW1lX2VzIjogIkludmVyc2lvbmVzIiwgInNvcnRfb3JkZXIiOiA0fSwKICAgICAgICBdCgogICAgICAgIHJlc3VsdCA9IHt9CiAgICAgICAgZm9yIGl0ZW0gaW4gZGF0YToKICAgICAgICAgICAgb2JqLCBfID0gVU5FLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgICAgIGNvZGU9aXRlbVsiY29kZSJdLAogICAgICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgICAgICJuYW1lX2VzIjogaXRlbVsibmFtZV9lcyJdLAogICAgICAgICAgICAgICAgICAgICJzb3J0X29yZGVyIjogaXRlbVsic29ydF9vcmRlciJdLAogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgKQogICAgICAgICAgICByZXN1bHRbaXRlbVsiY29kZSJdXSA9IG9iagogICAgICAgICAgICBzZWxmLnN0ZG91dC53cml0ZShmIlVORSBPSzoge29iai5jb2RlfSIpCiAgICAgICAgcmV0dXJuIHJlc3VsdAoKICAgIGRlZiBfc2VlZF9tZXRyaWNzKHNlbGYpOgogICAgICAgIGRhdGEgPSBbCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICJjb2RlIjogIklOR1JFU09TIiwKICAgICAgICAgICAgICAgICJuYW1lIjogIkluZ3Jlc29zIiwKICAgICAgICAgICAgICAgICJkZXNjcmlwdGlvbiI6ICJNZXRhIG1lbnN1YWwgZGUgaW5ncmVzb3MgcG9yIFVORSIsCiAgICAgICAgICAgIH0sCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICJjb2RlIjogIkNMSUVOVEVTX05VRVZPUyIsCiAgICAgICAgICAgICAgICAibmFtZSI6ICJDbGllbnRlcyBudWV2b3MiLAogICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIkNhbnRpZGFkIG1lbnN1YWwgZGUgY2xpZW50ZXMgbnVldm9zIHBvciBVTkUiLAogICAgICAgICAgICB9LAogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAiY29kZSI6ICJWRU5UQV9DUlVaQURBIiwKICAgICAgICAgICAgICAgICJuYW1lIjogIlZlbnRhIGNydXphZGEiLAogICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIkN1bXBsZSBzaSBsYSBVTkUgcmVmaWVyZSBhbCBtZW5vcyB1biBjbGllbnRlIGEgb3RyYSBVTkUgZW4gZWwgbWVzIiwKICAgICAgICAgICAgfSwKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgImNvZGUiOiAiUkVTUFVFU1RBX1JFUVMiLAogICAgICAgICAgICAgICAgIm5hbWUiOiAiUmVzcHVlc3RhIGEgcmVxdWVyaW1pZW50b3MiLAogICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIkN1bXBsaW1pZW50byBtYW51YWwgbWVuc3VhbCBwb3IgVU5FOyBlbiBpbnZlcnNpb25lcyBubyBhcGxpY2EgcHVudG9zIiwKICAgICAgICAgICAgfSwKICAgICAgICBdCgogICAgICAgIHJlc3VsdCA9IHt9CiAgICAgICAgZm9yIGl0ZW0gaW4gZGF0YToKICAgICAgICAgICAgb2JqLCBfID0gTWV0cmljRGVmaW5pdGlvbi5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICBjb2RlPWl0ZW1bImNvZGUiXSwKICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICAgICAibmFtZSI6IGl0ZW1bIm5hbWUiXSwKICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiBpdGVtWyJkZXNjcmlwdGlvbiJdLAogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgKQogICAgICAgICAgICByZXN1bHRbaXRlbVsiY29kZSJdXSA9IG9iagogICAgICAgICAgICBzZWxmLnN0ZG91dC53cml0ZShmIk1ldHJpYyBPSzoge29iai5jb2RlfSIpCiAgICAgICAgcmV0dXJuIHJlc3VsdAoKICAgIGRlZiBfc2VlZF9wbGFuKHNlbGYpOgogICAgICAgIG9iaiwgXyA9IFBHQ1BsYW4ub2JqZWN0cy51cGRhdGVfb3JfY3JlYXRlKAogICAgICAgICAgICB5ZWFyPTIwMjYsCiAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICJuYW1lIjogIlBHQyAyMDI2IiwKICAgICAgICAgICAgICAgICJpc19hY3RpdmUiOiBUcnVlLAogICAgICAgICAgICAgICAgIm5vdGVzIjogIlBsYW4gYW51YWwgUEdDIDIwMjYgY2FyZ2FkbyBkZXNkZSBlc3BlY2lmaWNhY2nDs24gaW5pY2lhbCIsCiAgICAgICAgICAgIH0sCiAgICAgICAgKQogICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKGYiUGxhbiBPSzoge29ian0iKQogICAgICAgIHJldHVybiBvYmoKCiAgICBkZWYgX3NlZWRfbW9udGhseV90YXJnZXRzKHNlbGYsIHBsYW4sIHVuZV9tYXAsIG1ldHJpY19tYXApOgogICAgICAgIG1vbnRobHlfZGF0YSA9IHsKICAgICAgICAgICAgIkZBQ1RPUklORyI6IHsKICAgICAgICAgICAgICAgICJJTkdSRVNPUyI6IHsKICAgICAgICAgICAgICAgICAgICAiYW5udWFsIjogRGVjaW1hbCgiMTEwMDAiKSwKICAgICAgICAgICAgICAgICAgICAicG9pbnRzIjogNzAsCiAgICAgICAgICAgICAgICAgICAgIm1vbnRocyI6IFs2NjAsIDExMDAsIDc3MCwgNDQwLCA3NzAsIDc3MCwgMTY1MCwgNzcwLCAzMzAsIDQ0MCwgMTY1MCwgMTY1MF0sCiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgIkNMSUVOVEVTX05VRVZPUyI6IHsKICAgICAgICAgICAgICAgICAgICAiYW5udWFsIjogRGVjaW1hbCgiMTIiKSwKICAgICAgICAgICAgICAgICAgICAicG9pbnRzIjogMTUsCiAgICAgICAgICAgICAgICAgICAgIm1vbnRocyI6IFsxLCAxLCAxLCAxLCAxLCAxLCAxLCAxLCAxLCAxLCAxLCAxXSwKICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICAgICAiVkVOVEFfQ1JVWkFEQSI6IHsKICAgICAgICAgICAgICAgICAgICAiYW5udWFsIjogTm9uZSwKICAgICAgICAgICAgICAgICAgICAicG9pbnRzIjogMTAsCiAgICAgICAgICAgICAgICAgICAgIm1vbnRocyI6IFsxXSAqIDEyLAogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICJSRVNQVUVTVEFfUkVRUyI6IHsKICAgICAgICAgICAgICAgICAgICAiYW5udWFsIjogTm9uZSwKICAgICAgICAgICAgICAgICAgICAicG9pbnRzIjogNSwKICAgICAgICAgICAgICAgICAgICAibW9udGhzIjogWzFdICogMTIsCiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICB9LAogICAgICAgICAgICAiTEVBU0lORyI6IHsKICAgICAgICAgICAgICAgICJJTkdSRVNPUyI6IHsKICAgICAgICAgICAgICAgICAgICAiYW5udWFsIjogRGVjaW1hbCgiMTIwMCIpLAogICAgICAgICAgICAgICAgICAgICJwb2ludHMiOiA3MCwKICAgICAgICAgICAgICAgICAgICAibW9udGhzIjogWzk2LCA4NCwgODQsIDg0LCA5NiwgODQsIDEwOCwgMTA4LCAxMDgsIDEyMCwgMTA4LCAxMjBdLAogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICJDTElFTlRFU19OVUVWT1MiOiB7CiAgICAgICAgICAgICAgICAgICAgImFubnVhbCI6IERlY2ltYWwoIjE1IiksCiAgICAgICAgICAgICAgICAgICAgInBvaW50cyI6IDE1LAogICAgICAgICAgICAgICAgICAgICJtb250aHMiOiBbMCwgMiwgMSwgMiwgMSwgMiwgMSwgMSwgMSwgMSwgMSwgMl0sCiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgIlZFTlRBX0NSVVpBREEiOiB7CiAgICAgICAgICAgICAgICAgICAgImFubnVhbCI6IE5vbmUsCiAgICAgICAgICAgICAgICAgICAgInBvaW50cyI6IDEwLAogICAgICAgICAgICAgICAgICAgICJtb250aHMiOiBbMV0gKiAxMiwKICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICAgICAiUkVTUFVFU1RBX1JFUVMiOiB7CiAgICAgICAgICAgICAgICAgICAgImFubnVhbCI6IE5vbmUsCiAgICAgICAgICAgICAgICAgICAgInBvaW50cyI6IDUsCiAgICAgICAgICAgICAgICAgICAgIm1vbnRocyI6IFsxXSAqIDEyLAogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgfSwKICAgICAgICAgICAgIklOU1VSQU5DRSI6IHsKICAgICAgICAgICAgICAgICJJTkdSRVNPUyI6IHsKICAgICAgICAgICAgICAgICAgICAiYW5udWFsIjogRGVjaW1hbCgiMTE5LjAiKSwKICAgICAgICAgICAgICAgICAgICAicG9pbnRzIjogNzAsCiAgICAgICAgICAgICAgICAgICAgIm1vbnRocyI6IFsKICAgICAgICAgICAgICAgICAgICAgICAgRGVjaW1hbCgiNi43NDYiKSwKICAgICAgICAgICAgICAgICAgICAgICAgRGVjaW1hbCgiNS43NjUiKSwKICAgICAgICAgICAgICAgICAgICAgICAgRGVjaW1hbCgiNS44OTgiKSwKICAgICAgICAgICAgICAgICAgICAgICAgRGVjaW1hbCgiNi4wNTAiKSwKICAgICAgICAgICAgICAgICAgICAgICAgRGVjaW1hbCgiNy42MjAiKSwKICAgICAgICAgICAgICAgICAgICAgICAgRGVjaW1hbCgiNy41NzAiKSwKICAgICAgICAgICAgICAgICAgICAgICAgRGVjaW1hbCgiOS43NjAiKSwKICAgICAgICAgICAgICAgICAgICAgICAgRGVjaW1hbCgiMTAuMzMwIiksCiAgICAgICAgICAgICAgICAgICAgICAgIERlY2ltYWwoIjExLjg1MCIpLAogICAgICAgICAgICAgICAgICAgICAgICBEZWNpbWFsKCIxNy4xODIiKSwKICAgICAgICAgICAgICAgICAgICAgICAgRGVjaW1hbCgiMTYuMzcyIiksCiAgICAgICAgICAgICAgICAgICAgICAgIERlY2ltYWwoIjEzLjc2MiIpLAogICAgICAgICAgICAgICAgICAgIF0sCiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgIkNMSUVOVEVTX05VRVZPUyI6IHsKICAgICAgICAgICAgICAgICAgICAiYW5udWFsIjogRGVjaW1hbCgiNDQiKSwKICAgICAgICAgICAgICAgICAgICAicG9pbnRzIjogMTUsCiAgICAgICAgICAgICAgICAgICAgIm1vbnRocyI6IFsxLCAyLCAzLCA1LCAzLCA0LCA2LCAzLCA0LCA2LCAzLCA0XSwKICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICAgICAiVkVOVEFfQ1JVWkFEQSI6IHsKICAgICAgICAgICAgICAgICAgICAiYW5udWFsIjogTm9uZSwKICAgICAgICAgICAgICAgICAgICAicG9pbnRzIjogMTAsCiAgICAgICAgICAgICAgICAgICAgIm1vbnRocyI6IFsxXSAqIDEyLAogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICJSRVNQVUVTVEFfUkVRUyI6IHsKICAgICAgICAgICAgICAgICAgICAiYW5udWFsIjogTm9uZSwKICAgICAgICAgICAgICAgICAgICAicG9pbnRzIjogNSwKICAgICAgICAgICAgICAgICAgICAibW9udGhzIjogWzFdICogMTIsCiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICB9LAogICAgICAgICAgICAiSU5WRVNUTUVOVCI6IHsKICAgICAgICAgICAgICAgICJJTkdSRVNPUyI6IHsKICAgICAgICAgICAgICAgICAgICAiYW5udWFsIjogRGVjaW1hbCgiMTYuMiIpLAogICAgICAgICAgICAgICAgICAgICJwb2ludHMiOiA3NSwKICAgICAgICAgICAgICAgICAgICAibW9udGhzIjogWwogICAgICAgICAgICAgICAgICAgICAgICBEZWNpbWFsKCIwLjIwMCIpLAogICAgICAgICAgICAgICAgICAgICAgICBEZWNpbWFsKCIwLjIwMCIpLAogICAgICAgICAgICAgICAgICAgICAgICBEZWNpbWFsKCIwLjMwMCIpLAogICAgICAgICAgICAgICAgICAgICAgICBEZWNpbWFsKCIzLjAwMCIpLAogICAgICAgICAgICAgICAgICAgICAgICBEZWNpbWFsKCIwLjYwMCIpLAogICAgICAgICAgICAgICAgICAgICAgICBEZWNpbWFsKCIxLjAwMCIpLAogICAgICAgICAgICAgICAgICAgICAgICBEZWNpbWFsKCIxLjAwMCIpLAogICAgICAgICAgICAgICAgICAgICAgICBEZWNpbWFsKCIxLjAwMCIpLAogICAgICAgICAgICAgICAgICAgICAgICBEZWNpbWFsKCIxLjAwMCIpLAogICAgICAgICAgICAgICAgICAgICAgICBEZWNpbWFsKCIyLjAwMCIpLAogICAgICAgICAgICAgICAgICAgICAgICBEZWNpbWFsKCIyLjkwMCIpLAogICAgICAgICAgICAgICAgICAgICAgICBEZWNpbWFsKCIzLjAwMCIpLAogICAgICAgICAgICAgICAgICAgIF0sCiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgIkNMSUVOVEVTX05VRVZPUyI6IHsKICAgICAgICAgICAgICAgICAgICAiYW5udWFsIjogRGVjaW1hbCgiMjAiKSwKICAgICAgICAgICAgICAgICAgICAicG9pbnRzIjogMTUsCiAgICAgICAgICAgICAgICAgICAgIm1vbnRocyI6IFsxLCAyLCAyLCAyLCAyLCAyLCAxLCAxLCAxLCAyLCAyLCAyXSwKICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICAgICAiVkVOVEFfQ1JVWkFEQSI6IHsKICAgICAgICAgICAgICAgICAgICAiYW5udWFsIjogTm9uZSwKICAgICAgICAgICAgICAgICAgICAicG9pbnRzIjogMTAsCiAgICAgICAgICAgICAgICAgICAgIm1vbnRocyI6IFsxXSAqIDEyLAogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICJSRVNQVUVTVEFfUkVRUyI6IHsKICAgICAgICAgICAgICAgICAgICAiYW5udWFsIjogTm9uZSwKICAgICAgICAgICAgICAgICAgICAicG9pbnRzIjogMCwKICAgICAgICAgICAgICAgICAgICAibW9udGhzIjogWzBdICogMTIsCiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICB9LAogICAgICAgIH0KCiAgICAgICAgdG90YWxfcm93cyA9IDAKCiAgICAgICAgZm9yIHVuZV9jb2RlLCBtZXRyaWNzIGluIG1vbnRobHlfZGF0YS5pdGVtcygpOgogICAgICAgICAgICB1bmUgPSB1bmVfbWFwW3VuZV9jb2RlXQoKICAgICAgICAgICAgZm9yIG1ldHJpY19jb2RlLCBwYXlsb2FkIGluIG1ldHJpY3MuaXRlbXMoKToKICAgICAgICAgICAgICAgIG1ldHJpYyA9IG1ldHJpY19tYXBbbWV0cmljX2NvZGVdCiAgICAgICAgICAgICAgICBhbm51YWxfdmFsdWUgPSBwYXlsb2FkWyJhbm51YWwiXQogICAgICAgICAgICAgICAgcG9pbnRzID0gcGF5bG9hZFsicG9pbnRzIl0KCiAgICAgICAgICAgICAgICBmb3IgbW9udGhfaW5kZXgsIHRhcmdldCBpbiBlbnVtZXJhdGUocGF5bG9hZFsibW9udGhzIl0sIHN0YXJ0PTEpOgogICAgICAgICAgICAgICAgICAgIE1vbnRobHlUYXJnZXQub2JqZWN0cy51cGRhdGVfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgICAgICAgICBwbGFuPXBsYW4sCiAgICAgICAgICAgICAgICAgICAgICAgIHVuZT11bmUsCiAgICAgICAgICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICAgICAgICAgIHllYXI9MjAyNiwKICAgICAgICAgICAgICAgICAgICAgICAgbW9udGg9bW9udGhfaW5kZXgsCiAgICAgICAgICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJ0YXJnZXRfdmFsdWUiOiBEZWNpbWFsKHN0cih0YXJnZXQpKSBpZiB0YXJnZXQgaXMgbm90IE5vbmUgZWxzZSBOb25lLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgInBvaW50c19pZl9hY2hpZXZlZCI6IHBvaW50cywKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJyZWZlcmVuY2VfYW5udWFsX3ZhbHVlIjogYW5udWFsX3ZhbHVlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgIm5vdGVzIjogc2VsZi5fYnVpbGRfbm90ZShtZXRyaWNfY29kZSwgdW5lX2NvZGUpLAogICAgICAgICAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgICAgICB0b3RhbF9yb3dzICs9IDEKCiAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoZiJNb250aGx5VGFyZ2V0IE9LOiB7dG90YWxfcm93c30gcmVnaXN0cm9zIikKCiAgICBkZWYgX2J1aWxkX25vdGUoc2VsZiwgbWV0cmljX2NvZGUsIHVuZV9jb2RlKToKICAgICAgICBpZiBtZXRyaWNfY29kZSA9PSAiVkVOVEFfQ1JVWkFEQSI6CiAgICAgICAgICAgIHJldHVybiAiQ3VtcGxlIGNvbiBhbCBtZW5vcyAxIHJlZmVyZW5jaWEgZW52aWFkYSBhIGN1YWxxdWllciBvdHJhIFVORSBlbiBlbCBtZXMuIgogICAgICAgIGlmIG1ldHJpY19jb2RlID09ICJSRVNQVUVTVEFfUkVRUyIgYW5kIHVuZV9jb2RlID09ICJJTlZFUlNJT05FUyI6CiAgICAgICAgICAgIHJldHVybiAiTm8gYXBsaWNhIHB1bnRvcyBwYXJhIEludmVyc2lvbmVzIGVuIGVsIE1WUC4iCiAgICAgICAgaWYgbWV0cmljX2NvZGUgPT0gIlJFU1BVRVNUQV9SRVFTIjoKICAgICAgICAgICAgcmV0dXJuICJDdW1wbGltaWVudG8gbWFudWFsIG1lbnN1YWw7IHNpIGluY3VtcGxlLCByZWdpc3RyYXIgaW5jaWRlbmNpYS4iCiAgICAgICAgaWYgbWV0cmljX2NvZGUgPT0gIklOR1JFU09TIiBhbmQgdW5lX2NvZGUgPT0gIklOVkVSU0lPTkVTIjoKICAgICAgICAgICAgcmV0dXJuICJQYXJhIEludmVyc2lvbmVzLCBlbCBpbmdyZXNvIG1lbnN1YWwgc2UgY2FsY3VsYSBzdW1hbmRvIG1vbnRvcyBkZWwgYXJjaGl2byBkZSBjbGllbnRlcyBudWV2b3MsIHNlYW4gbnVldm9zIG8gbm8uIgogICAgICAgIHJldHVybiAiIg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/management/commands/seed_sample_results.py
PATH_JSON="core/management/commands/seed_sample_results.py"
FILENAME=seed_sample_results.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=139
SIZE_BYTES_UTF8=5231
CONTENT_SHA256=c10bee9dc9a105a099c88ef10ce4b09632d63d25ecc287fc2992a4c27c36f8fd
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
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import UNE, MetricDefinition
from pgc.models import (
    PGCPlan,
    MonthlyTarget,
    MonthlyMetricResult,
    ManualRequirementsCompliance,
)


class Command(BaseCommand):
    help = "Carga valores medidos de ejemplo para probar el cálculo PGC"

    @transaction.atomic
    def handle(self, *args, **options):
        year = 2026
        month = 1

        plan = PGCPlan.objects.get(year=year)

        une_fact = UNE.objects.get(code__in=["FACTORING", "FACTORAJE"])
        une_leas = UNE.objects.get(code="LEASING")
        une_ins = UNE.objects.get(code="INSURANCE")
        une_inv = UNE.objects.get(code__in=["INVESTMENT", "INVERSIONES"])

        m_ing = MetricDefinition.objects.get(code=MetricDefinition.CODE_INGRESOS)
        m_cli = MetricDefinition.objects.get(code=MetricDefinition.CODE_CLIENTES_NUEVOS)
        m_ven = MetricDefinition.objects.get(code=MetricDefinition.CODE_VENTA_CRUZADA)
        m_req = MetricDefinition.objects.get(code=MetricDefinition.CODE_RESPUESTA_REQS)

        self.stdout.write("Cargando valores medidos de ejemplo para 2026-01...")

        # Helper
        def set_result(une, metric, measured_value):
            target = MonthlyTarget.objects.get(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
            )
            mmr, _ = MonthlyMetricResult.objects.get_or_create(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
                defaults={"target_value": target.target_value},
            )
            mmr.target_value = target.target_value
            mmr.measured_value = measured_value
            mmr.save()
            self.stdout.write(
                f"  {une.code} {metric.code}: medido={measured_value} meta={target.target_value}"
            )

        # FACTORAJE enero 2026
        # Meta ingresos: 660 KUSD, real ~2,289 => cumple
        set_result(une_fact, m_ing, Decimal("2289"))
        # Meta clientes nuevos: 1, real 0 => no cumple
        set_result(une_fact, m_cli, Decimal("0"))
        # Venta cruzada: simulamos que sí hubo al menos 1 => 1
        set_result(une_fact, m_ven, Decimal("1"))
        # Respuesta reqs: cumplido (1); además sin incidencia manual
        set_result(une_fact, m_req, Decimal("1"))

        # LEASING enero 2026
        # Meta ingresos: 96 KUSD, real ~535 => cumple
        set_result(une_leas, m_ing, Decimal("535"))
        # Meta clientes nuevos: 0, real 0 => cumple trivial (>=)
        set_result(une_leas, m_cli, Decimal("0"))
        # Venta cruzada: simulamos 0 => falla
        set_result(une_leas, m_ven, Decimal("0"))
        # Respuesta reqs: cumplido
        set_result(une_leas, m_req, Decimal("1"))

        # INSURANCE enero 2026 (Personas+Empresas agregadas)
        # Meta ingresos: 6.746 (miles), real 12.435 => cumple
        set_result(une_ins, m_ing, Decimal("12.435"))
        # Meta clientes nuevos: 1+0=1, real 0 => no cumple
        set_result(une_ins, m_cli, Decimal("0"))
        # Venta cruzada: simulamos 1 => cumple
        set_result(une_ins, m_ven, Decimal("1"))
        # Respuesta reqs: cumplido
        set_result(une_ins, m_req, Decimal("1"))

        # INVERSIONES enero 2026
        # Meta ingresos: 0.200, real 1.265 (ejemplo) => cumple
        set_result(une_inv, m_ing, Decimal("1.265"))
        # Meta clientes nuevos: 1, real 3 => cumple
        set_result(une_inv, m_cli, Decimal("3"))
        # Venta cruzada: simulamos 0 => falla
        set_result(une_inv, m_ven, Decimal("0"))
        # Respuesta reqs: no otorga puntos para inversiones; medido 0
        set_result(une_inv, m_req, Decimal("0"))

        # Cumplimiento manual de requerimientos:
        #   - FACTORAJE: cumple
        #   - LEASING: incumple (para ver impacto)
        #   - INSURANCE: cumple
        #   - INVERSIONES: no aplica puntos, pero lo marcamos como cumple
        ManualRequirementsCompliance.objects.update_or_create(
            plan=plan,
            une=une_fact,
            year=year,
            month=month,
            defaults={"is_compliant": True, "incident_note": ""},
        )
        ManualRequirementsCompliance.objects.update_or_create(
            plan=plan,
            une=une_leas,
            year=year,
            month=month,
            defaults={
                "is_compliant": False,
                "incident_note": "Incumplimiento ilustrativo en enero para Leasing.",
            },
        )
        ManualRequirementsCompliance.objects.update_or_create(
            plan=plan,
            une=une_ins,
            year=year,
            month=month,
            defaults={"is_compliant": True, "incident_note": ""},
        )
        ManualRequirementsCompliance.objects.update_or_create(
            plan=plan,
            une=une_inv,
            year=year,
            month=month,
            defaults={"is_compliant": True, "incident_note": ""},
        )

        self.stdout.write(self.style.SUCCESS("Valores de ejemplo cargados."))
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from decimal import Decimal
00002|
00003|from django.core.management.base import BaseCommand
00004|from django.db import transaction
00005|
00006|from core.models import UNE, MetricDefinition
00007|from pgc.models import (
00008|    PGCPlan,
00009|    MonthlyTarget,
00010|    MonthlyMetricResult,
00011|    ManualRequirementsCompliance,
00012|)
00013|
00014|
00015|class Command(BaseCommand):
00016|    help = "Carga valores medidos de ejemplo para probar el cálculo PGC"
00017|
00018|    @transaction.atomic
00019|    def handle(self, *args, **options):
00020|        year = 2026
00021|        month = 1
00022|
00023|        plan = PGCPlan.objects.get(year=year)
00024|
00025|        une_fact = UNE.objects.get(code__in=["FACTORING", "FACTORAJE"])
00026|        une_leas = UNE.objects.get(code="LEASING")
00027|        une_ins = UNE.objects.get(code="INSURANCE")
00028|        une_inv = UNE.objects.get(code__in=["INVESTMENT", "INVERSIONES"])
00029|
00030|        m_ing = MetricDefinition.objects.get(code=MetricDefinition.CODE_INGRESOS)
00031|        m_cli = MetricDefinition.objects.get(code=MetricDefinition.CODE_CLIENTES_NUEVOS)
00032|        m_ven = MetricDefinition.objects.get(code=MetricDefinition.CODE_VENTA_CRUZADA)
00033|        m_req = MetricDefinition.objects.get(code=MetricDefinition.CODE_RESPUESTA_REQS)
00034|
00035|        self.stdout.write("Cargando valores medidos de ejemplo para 2026-01...")
00036|
00037|        # Helper
00038|        def set_result(une, metric, measured_value):
00039|            target = MonthlyTarget.objects.get(
00040|                plan=plan,
00041|                une=une,
00042|                metric=metric,
00043|                year=year,
00044|                month=month,
00045|            )
00046|            mmr, _ = MonthlyMetricResult.objects.get_or_create(
00047|                plan=plan,
00048|                une=une,
00049|                metric=metric,
00050|                year=year,
00051|                month=month,
00052|                defaults={"target_value": target.target_value},
00053|            )
00054|            mmr.target_value = target.target_value
00055|            mmr.measured_value = measured_value
00056|            mmr.save()
00057|            self.stdout.write(
00058|                f"  {une.code} {metric.code}: medido={measured_value} meta={target.target_value}"
00059|            )
00060|
00061|        # FACTORAJE enero 2026
00062|        # Meta ingresos: 660 KUSD, real ~2,289 => cumple
00063|        set_result(une_fact, m_ing, Decimal("2289"))
00064|        # Meta clientes nuevos: 1, real 0 => no cumple
00065|        set_result(une_fact, m_cli, Decimal("0"))
00066|        # Venta cruzada: simulamos que sí hubo al menos 1 => 1
00067|        set_result(une_fact, m_ven, Decimal("1"))
00068|        # Respuesta reqs: cumplido (1); además sin incidencia manual
00069|        set_result(une_fact, m_req, Decimal("1"))
00070|
00071|        # LEASING enero 2026
00072|        # Meta ingresos: 96 KUSD, real ~535 => cumple
00073|        set_result(une_leas, m_ing, Decimal("535"))
00074|        # Meta clientes nuevos: 0, real 0 => cumple trivial (>=)
00075|        set_result(une_leas, m_cli, Decimal("0"))
00076|        # Venta cruzada: simulamos 0 => falla
00077|        set_result(une_leas, m_ven, Decimal("0"))
00078|        # Respuesta reqs: cumplido
00079|        set_result(une_leas, m_req, Decimal("1"))
00080|
00081|        # INSURANCE enero 2026 (Personas+Empresas agregadas)
00082|        # Meta ingresos: 6.746 (miles), real 12.435 => cumple
00083|        set_result(une_ins, m_ing, Decimal("12.435"))
00084|        # Meta clientes nuevos: 1+0=1, real 0 => no cumple
00085|        set_result(une_ins, m_cli, Decimal("0"))
00086|        # Venta cruzada: simulamos 1 => cumple
00087|        set_result(une_ins, m_ven, Decimal("1"))
00088|        # Respuesta reqs: cumplido
00089|        set_result(une_ins, m_req, Decimal("1"))
00090|
00091|        # INVERSIONES enero 2026
00092|        # Meta ingresos: 0.200, real 1.265 (ejemplo) => cumple
00093|        set_result(une_inv, m_ing, Decimal("1.265"))
00094|        # Meta clientes nuevos: 1, real 3 => cumple
00095|        set_result(une_inv, m_cli, Decimal("3"))
00096|        # Venta cruzada: simulamos 0 => falla
00097|        set_result(une_inv, m_ven, Decimal("0"))
00098|        # Respuesta reqs: no otorga puntos para inversiones; medido 0
00099|        set_result(une_inv, m_req, Decimal("0"))
00100|
00101|        # Cumplimiento manual de requerimientos:
00102|        #   - FACTORAJE: cumple
00103|        #   - LEASING: incumple (para ver impacto)
00104|        #   - INSURANCE: cumple
00105|        #   - INVERSIONES: no aplica puntos, pero lo marcamos como cumple
00106|        ManualRequirementsCompliance.objects.update_or_create(
00107|            plan=plan,
00108|            une=une_fact,
00109|            year=year,
00110|            month=month,
00111|            defaults={"is_compliant": True, "incident_note": ""},
00112|        )
00113|        ManualRequirementsCompliance.objects.update_or_create(
00114|            plan=plan,
00115|            une=une_leas,
00116|            year=year,
00117|            month=month,
00118|            defaults={
00119|                "is_compliant": False,
00120|                "incident_note": "Incumplimiento ilustrativo en enero para Leasing.",
00121|            },
00122|        )
00123|        ManualRequirementsCompliance.objects.update_or_create(
00124|            plan=plan,
00125|            une=une_ins,
00126|            year=year,
00127|            month=month,
00128|            defaults={"is_compliant": True, "incident_note": ""},
00129|        )
00130|        ManualRequirementsCompliance.objects.update_or_create(
00131|            plan=plan,
00132|            une=une_inv,
00133|            year=year,
00134|            month=month,
00135|            defaults={"is_compliant": True, "incident_note": ""},
00136|        )
00137|
00138|        self.stdout.write(self.style.SUCCESS("Valores de ejemplo cargados."))
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsCgpmcm9tIGRqYW5nby5jb3JlLm1hbmFnZW1lbnQuYmFzZSBpbXBvcnQgQmFzZUNvbW1hbmQKZnJvbSBkamFuZ28uZGIgaW1wb3J0IHRyYW5zYWN0aW9uCgpmcm9tIGNvcmUubW9kZWxzIGltcG9ydCBVTkUsIE1ldHJpY0RlZmluaXRpb24KZnJvbSBwZ2MubW9kZWxzIGltcG9ydCAoCiAgICBQR0NQbGFuLAogICAgTW9udGhseVRhcmdldCwKICAgIE1vbnRobHlNZXRyaWNSZXN1bHQsCiAgICBNYW51YWxSZXF1aXJlbWVudHNDb21wbGlhbmNlLAopCgoKY2xhc3MgQ29tbWFuZChCYXNlQ29tbWFuZCk6CiAgICBoZWxwID0gIkNhcmdhIHZhbG9yZXMgbWVkaWRvcyBkZSBlamVtcGxvIHBhcmEgcHJvYmFyIGVsIGPDoWxjdWxvIFBHQyIKCiAgICBAdHJhbnNhY3Rpb24uYXRvbWljCiAgICBkZWYgaGFuZGxlKHNlbGYsICphcmdzLCAqKm9wdGlvbnMpOgogICAgICAgIHllYXIgPSAyMDI2CiAgICAgICAgbW9udGggPSAxCgogICAgICAgIHBsYW4gPSBQR0NQbGFuLm9iamVjdHMuZ2V0KHllYXI9eWVhcikKCiAgICAgICAgdW5lX2ZhY3QgPSBVTkUub2JqZWN0cy5nZXQoY29kZV9faW49WyJGQUNUT1JJTkciLCAiRkFDVE9SQUpFIl0pCiAgICAgICAgdW5lX2xlYXMgPSBVTkUub2JqZWN0cy5nZXQoY29kZT0iTEVBU0lORyIpCiAgICAgICAgdW5lX2lucyA9IFVORS5vYmplY3RzLmdldChjb2RlPSJJTlNVUkFOQ0UiKQogICAgICAgIHVuZV9pbnYgPSBVTkUub2JqZWN0cy5nZXQoY29kZV9faW49WyJJTlZFU1RNRU5UIiwgIklOVkVSU0lPTkVTIl0pCgogICAgICAgIG1faW5nID0gTWV0cmljRGVmaW5pdGlvbi5vYmplY3RzLmdldChjb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9JTkdSRVNPUykKICAgICAgICBtX2NsaSA9IE1ldHJpY0RlZmluaXRpb24ub2JqZWN0cy5nZXQoY29kZT1NZXRyaWNEZWZpbml0aW9uLkNPREVfQ0xJRU5URVNfTlVFVk9TKQogICAgICAgIG1fdmVuID0gTWV0cmljRGVmaW5pdGlvbi5vYmplY3RzLmdldChjb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9WRU5UQV9DUlVaQURBKQogICAgICAgIG1fcmVxID0gTWV0cmljRGVmaW5pdGlvbi5vYmplY3RzLmdldChjb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9SRVNQVUVTVEFfUkVRUykKCiAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoIkNhcmdhbmRvIHZhbG9yZXMgbWVkaWRvcyBkZSBlamVtcGxvIHBhcmEgMjAyNi0wMS4uLiIpCgogICAgICAgICMgSGVscGVyCiAgICAgICAgZGVmIHNldF9yZXN1bHQodW5lLCBtZXRyaWMsIG1lYXN1cmVkX3ZhbHVlKToKICAgICAgICAgICAgdGFyZ2V0ID0gTW9udGhseVRhcmdldC5vYmplY3RzLmdldCgKICAgICAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgICAgIHVuZT11bmUsCiAgICAgICAgICAgICAgICBtZXRyaWM9bWV0cmljLAogICAgICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgICkKICAgICAgICAgICAgbW1yLCBfID0gTW9udGhseU1ldHJpY1Jlc3VsdC5vYmplY3RzLmdldF9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICBwbGFuPXBsYW4sCiAgICAgICAgICAgICAgICB1bmU9dW5lLAogICAgICAgICAgICAgICAgbWV0cmljPW1ldHJpYywKICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICAgICAgZGVmYXVsdHM9eyJ0YXJnZXRfdmFsdWUiOiB0YXJnZXQudGFyZ2V0X3ZhbHVlfSwKICAgICAgICAgICAgKQogICAgICAgICAgICBtbXIudGFyZ2V0X3ZhbHVlID0gdGFyZ2V0LnRhcmdldF92YWx1ZQogICAgICAgICAgICBtbXIubWVhc3VyZWRfdmFsdWUgPSBtZWFzdXJlZF92YWx1ZQogICAgICAgICAgICBtbXIuc2F2ZSgpCiAgICAgICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKAogICAgICAgICAgICAgICAgZiIgIHt1bmUuY29kZX0ge21ldHJpYy5jb2RlfTogbWVkaWRvPXttZWFzdXJlZF92YWx1ZX0gbWV0YT17dGFyZ2V0LnRhcmdldF92YWx1ZX0iCiAgICAgICAgICAgICkKCiAgICAgICAgIyBGQUNUT1JBSkUgZW5lcm8gMjAyNgogICAgICAgICMgTWV0YSBpbmdyZXNvczogNjYwIEtVU0QsIHJlYWwgfjIsMjg5ID0+IGN1bXBsZQogICAgICAgIHNldF9yZXN1bHQodW5lX2ZhY3QsIG1faW5nLCBEZWNpbWFsKCIyMjg5IikpCiAgICAgICAgIyBNZXRhIGNsaWVudGVzIG51ZXZvczogMSwgcmVhbCAwID0+IG5vIGN1bXBsZQogICAgICAgIHNldF9yZXN1bHQodW5lX2ZhY3QsIG1fY2xpLCBEZWNpbWFsKCIwIikpCiAgICAgICAgIyBWZW50YSBjcnV6YWRhOiBzaW11bGFtb3MgcXVlIHPDrSBodWJvIGFsIG1lbm9zIDEgPT4gMQogICAgICAgIHNldF9yZXN1bHQodW5lX2ZhY3QsIG1fdmVuLCBEZWNpbWFsKCIxIikpCiAgICAgICAgIyBSZXNwdWVzdGEgcmVxczogY3VtcGxpZG8gKDEpOyBhZGVtw6FzIHNpbiBpbmNpZGVuY2lhIG1hbnVhbAogICAgICAgIHNldF9yZXN1bHQodW5lX2ZhY3QsIG1fcmVxLCBEZWNpbWFsKCIxIikpCgogICAgICAgICMgTEVBU0lORyBlbmVybyAyMDI2CiAgICAgICAgIyBNZXRhIGluZ3Jlc29zOiA5NiBLVVNELCByZWFsIH41MzUgPT4gY3VtcGxlCiAgICAgICAgc2V0X3Jlc3VsdCh1bmVfbGVhcywgbV9pbmcsIERlY2ltYWwoIjUzNSIpKQogICAgICAgICMgTWV0YSBjbGllbnRlcyBudWV2b3M6IDAsIHJlYWwgMCA9PiBjdW1wbGUgdHJpdmlhbCAoPj0pCiAgICAgICAgc2V0X3Jlc3VsdCh1bmVfbGVhcywgbV9jbGksIERlY2ltYWwoIjAiKSkKICAgICAgICAjIFZlbnRhIGNydXphZGE6IHNpbXVsYW1vcyAwID0+IGZhbGxhCiAgICAgICAgc2V0X3Jlc3VsdCh1bmVfbGVhcywgbV92ZW4sIERlY2ltYWwoIjAiKSkKICAgICAgICAjIFJlc3B1ZXN0YSByZXFzOiBjdW1wbGlkbwogICAgICAgIHNldF9yZXN1bHQodW5lX2xlYXMsIG1fcmVxLCBEZWNpbWFsKCIxIikpCgogICAgICAgICMgSU5TVVJBTkNFIGVuZXJvIDIwMjYgKFBlcnNvbmFzK0VtcHJlc2FzIGFncmVnYWRhcykKICAgICAgICAjIE1ldGEgaW5ncmVzb3M6IDYuNzQ2IChtaWxlcyksIHJlYWwgMTIuNDM1ID0+IGN1bXBsZQogICAgICAgIHNldF9yZXN1bHQodW5lX2lucywgbV9pbmcsIERlY2ltYWwoIjEyLjQzNSIpKQogICAgICAgICMgTWV0YSBjbGllbnRlcyBudWV2b3M6IDErMD0xLCByZWFsIDAgPT4gbm8gY3VtcGxlCiAgICAgICAgc2V0X3Jlc3VsdCh1bmVfaW5zLCBtX2NsaSwgRGVjaW1hbCgiMCIpKQogICAgICAgICMgVmVudGEgY3J1emFkYTogc2ltdWxhbW9zIDEgPT4gY3VtcGxlCiAgICAgICAgc2V0X3Jlc3VsdCh1bmVfaW5zLCBtX3ZlbiwgRGVjaW1hbCgiMSIpKQogICAgICAgICMgUmVzcHVlc3RhIHJlcXM6IGN1bXBsaWRvCiAgICAgICAgc2V0X3Jlc3VsdCh1bmVfaW5zLCBtX3JlcSwgRGVjaW1hbCgiMSIpKQoKICAgICAgICAjIElOVkVSU0lPTkVTIGVuZXJvIDIwMjYKICAgICAgICAjIE1ldGEgaW5ncmVzb3M6IDAuMjAwLCByZWFsIDEuMjY1IChlamVtcGxvKSA9PiBjdW1wbGUKICAgICAgICBzZXRfcmVzdWx0KHVuZV9pbnYsIG1faW5nLCBEZWNpbWFsKCIxLjI2NSIpKQogICAgICAgICMgTWV0YSBjbGllbnRlcyBudWV2b3M6IDEsIHJlYWwgMyA9PiBjdW1wbGUKICAgICAgICBzZXRfcmVzdWx0KHVuZV9pbnYsIG1fY2xpLCBEZWNpbWFsKCIzIikpCiAgICAgICAgIyBWZW50YSBjcnV6YWRhOiBzaW11bGFtb3MgMCA9PiBmYWxsYQogICAgICAgIHNldF9yZXN1bHQodW5lX2ludiwgbV92ZW4sIERlY2ltYWwoIjAiKSkKICAgICAgICAjIFJlc3B1ZXN0YSByZXFzOiBubyBvdG9yZ2EgcHVudG9zIHBhcmEgaW52ZXJzaW9uZXM7IG1lZGlkbyAwCiAgICAgICAgc2V0X3Jlc3VsdCh1bmVfaW52LCBtX3JlcSwgRGVjaW1hbCgiMCIpKQoKICAgICAgICAjIEN1bXBsaW1pZW50byBtYW51YWwgZGUgcmVxdWVyaW1pZW50b3M6CiAgICAgICAgIyAgIC0gRkFDVE9SQUpFOiBjdW1wbGUKICAgICAgICAjICAgLSBMRUFTSU5HOiBpbmN1bXBsZSAocGFyYSB2ZXIgaW1wYWN0bykKICAgICAgICAjICAgLSBJTlNVUkFOQ0U6IGN1bXBsZQogICAgICAgICMgICAtIElOVkVSU0lPTkVTOiBubyBhcGxpY2EgcHVudG9zLCBwZXJvIGxvIG1hcmNhbW9zIGNvbW8gY3VtcGxlCiAgICAgICAgTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZS5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgdW5lPXVuZV9mYWN0LAogICAgICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICBkZWZhdWx0cz17ImlzX2NvbXBsaWFudCI6IFRydWUsICJpbmNpZGVudF9ub3RlIjogIiJ9LAogICAgICAgICkKICAgICAgICBNYW51YWxSZXF1aXJlbWVudHNDb21wbGlhbmNlLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgcGxhbj1wbGFuLAogICAgICAgICAgICB1bmU9dW5lX2xlYXMsCiAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICJpc19jb21wbGlhbnQiOiBGYWxzZSwKICAgICAgICAgICAgICAgICJpbmNpZGVudF9ub3RlIjogIkluY3VtcGxpbWllbnRvIGlsdXN0cmF0aXZvIGVuIGVuZXJvIHBhcmEgTGVhc2luZy4iLAogICAgICAgICAgICB9LAogICAgICAgICkKICAgICAgICBNYW51YWxSZXF1aXJlbWVudHNDb21wbGlhbmNlLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgcGxhbj1wbGFuLAogICAgICAgICAgICB1bmU9dW5lX2lucywKICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICBtb250aD1tb250aCwKICAgICAgICAgICAgZGVmYXVsdHM9eyJpc19jb21wbGlhbnQiOiBUcnVlLCAiaW5jaWRlbnRfbm90ZSI6ICIifSwKICAgICAgICApCiAgICAgICAgTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZS5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgdW5lPXVuZV9pbnYsCiAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgIGRlZmF1bHRzPXsiaXNfY29tcGxpYW50IjogVHJ1ZSwgImluY2lkZW50X25vdGUiOiAiIn0sCiAgICAgICAgKQoKICAgICAgICBzZWxmLnN0ZG91dC53cml0ZShzZWxmLnN0eWxlLlNVQ0NFU1MoIlZhbG9yZXMgZGUgZWplbXBsbyBjYXJnYWRvcy4iKSk=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/management/commands/seed_wcg_demo.py
PATH_JSON="core/management/commands/seed_wcg_demo.py"
FILENAME=seed_wcg_demo.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=206
SIZE_BYTES_UTF8=9012
CONTENT_SHA256=e768d2942f4153bff9f8a62fc5c0da44bd8f243683f9509101be8fd1d5cd58a4
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
Carga demo WCG One: unidades, entidades, contactos, risk snapshots y tickets PGO.
Ejecutar: python manage.py seed_wcg_demo
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from core.models import UNE
from core.wcg_models import Contacto, Entidad, Producto, RelacionEntidadProducto, UnidadNegocio
from crm.models import Interaccion, Tarea
from pgo.models import Ticket
from pgo.periodo import recalculate_pgo_periodos
from risk.models import RiskOperationSnapshot

User = get_user_model()


class Command(BaseCommand):
    help = "Carga datos demo para CRM, Risk y PGO (sin depender de imports externos)"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Sembrando WCG One demo...")
        unidades = self._seed_unidades()
        productos = self._seed_productos(unidades)
        entidades = self._seed_entidades(unidades)
        self._seed_contactos(entidades)
        self._seed_relaciones(entidades, productos)
        self._seed_crm_activity(entidades)
        self._seed_risk(entidades, productos)
        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        self._seed_tickets(entidades, unidades, user)
        recalculate_pgo_periodos()
        self.stdout.write(self.style.SUCCESS(
            f"Demo OK: {Entidad.objects.count()} entidades, "
            f"{RiskOperationSnapshot.objects.count()} snapshots, "
            f"{Ticket.objects.count()} tickets"
        ))

    def _seed_unidades(self):
        mapping = [
            ("FACTORING", "Factoraje", "FACTORING"),
            ("LEASING", "Leasing", "LEASING"),
            ("INSURANCE", "Insurance", "INSURANCE"),
            ("INVESTMENT", "Inversiones", "INVESTMENT"),
            ("TI", "Tecnología / TI", None),
        ]
        result = {}
        for code, nombre, une_code in mapping:
            une = UNE.objects.filter(code=une_code).first() if une_code else None
            obj, _ = UnidadNegocio.objects.update_or_create(
                code=code,
                defaults={"nombre": nombre, "une_pgc": une, "activa": True},
            )
            result[code] = obj
        return result

    def _seed_productos(self, unidades):
        data = [
            ("LEASING", "Leasing operativo", "LEASING"),
            ("FACTORING", "Factoraje", "FACTORING"),
        ]
        out = {}
        for code, nombre, un_code in data:
            obj, _ = Producto.objects.update_or_create(
                codigo=code,
                defaults={"nombre": nombre, "unidad_negocio": unidades[un_code], "activo": True},
            )
            out[code] = obj
        return out

    def _seed_entidades(self, unidades):
        data = [
            ("9852115", "VICENTE SOLER MUNGUÍA", "9852115", "LEASING"),
            ("DEMO002", "Distribuidora Me Llega, S.A.", "1234567-8", "FACTORING"),
            ("DEMO003", "Ingenio Palo Gordo, S.A.", "8765432-1", "LEASING"),
            ("DEMO004", "Helvetia Centroamérica", "5566778-9", "INSURANCE"),
            ("DEMO005", "Corporación Mogori", "9988776-5", "INVESTMENT"),
        ]
        out = {}
        for codigo, nombre, nit, un_code in data:
            obj, _ = Entidad.objects.update_or_create(
                codigo=codigo,
                defaults={
                    "nombre": nombre,
                    "nit": nit,
                    "tipo": Entidad.TIPO_CLIENTE,
                    "unidad_negocio": unidades[un_code],
                    "activa": True,
                },
            )
            out[codigo] = obj
        return out

    def _seed_contactos(self, entidades):
        samples = [
            ("9852115", "María Soler", "maria@soler.gt", "Gerente General"),
            ("DEMO002", "Juan Pérez", "jperez@melega.gt", "CFO"),
            ("DEMO003", "Ana Morales", "ana@palogordo.gt", "Tesorería"),
        ]
        for codigo, nombre, email, cargo in samples:
            ent = entidades[codigo]
            Contacto.objects.update_or_create(
                entidad=ent,
                email=email,
                defaults={"nombre": nombre, "cargo": cargo, "es_principal": True, "activo": True},
            )

    def _seed_relaciones(self, entidades, productos):
        RelacionEntidadProducto.objects.update_or_create(
            entidad=entidades["9852115"],
            producto=productos["LEASING"],
            defaults={"estado": RelacionEntidadProducto.ESTADO_ACTIVO},
        )

    def _seed_crm_activity(self, entidades):
        user = User.objects.filter(is_superuser=True).first()
        now = timezone.now()
        ent = entidades["9852115"]
        if not ent.interacciones.exists():
            Interaccion.objects.create(
                entidad=ent,
                tipo=Interaccion.TIPO_REUNION,
                asunto="Revisión cartera leasing",
                descripcion="Seguimiento trimestral",
                fecha=now - timedelta(days=3),
                usuario=user,
            )
        if not ent.tareas.exists():
            Tarea.objects.create(
                entidad=ent,
                titulo="Enviar estados financieros actualizados",
                fecha_vencimiento=date.today() + timedelta(days=7),
                estado=Tarea.ESTADO_PENDIENTE,
                asignado_a=user,
            )

    def _seed_risk(self, entidades, productos):
        base = date(2026, 5, 31)
        ops = [
            ("9852115", "PG01260302", 45, Decimal("125000.00"), Decimal("42000.00"), True),
            ("DEMO003", "LG01260115", 62, Decimal("890000.00"), Decimal("120000.00"), True),
            ("DEMO002", "FC01260288", 12, Decimal("55000.00"), Decimal("0"), False),
        ]
        for codigo, ref, mora, saldo, exigible, alerta in ops:
            ent = entidades[codigo]
            nivel = RiskOperationSnapshot.NIVEL_ALTO if mora >= 30 else RiskOperationSnapshot.NIVEL_BAJO
            RiskOperationSnapshot.objects.update_or_create(
                entidad=ent,
                referencia_operacion=ref,
                fecha_snapshot=base,
                defaults={
                    "producto": productos.get("LEASING") or productos.get("FACTORING"),
                    "nivel_riesgo": nivel,
                    "dias_mora": mora,
                    "saldo": saldo,
                    "monto_exigible": exigible,
                    "alerta": alerta,
                    "detalle": "Snapshot demo mayo 2026",
                },
            )

    def _seed_tickets(self, entidades, unidades, user):
        now = timezone.now()
        samples = [
            ("TI-2026-001", "VPN no conecta", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_ALTA, 24, 18),
            ("TI-2026-002", "Nuevo usuario CRM", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_MEDIA, 48, 36),
            ("TI-2026-003", "Impresora piso 3", Ticket.ESTADO_EN_PROCESO, Ticket.PRIORIDAD_BAJA, 72, None),
            ("TI-2026-004", "Error reporte PGO", Ticket.ESTADO_ABIERTO, Ticket.PRIORIDAD_ALTA, 48, None),
            ("TI-2026-005", "Correo bloqueado", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_MEDIA, 48, 40),
            ("TI-2026-006", "Acceso Balón Riesgo", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_MEDIA, 48, 12),
            ("TI-2026-007", "Lentitud red", Ticket.ESTADO_EN_PROCESO, Ticket.PRIORIDAD_ALTA, 24, None),
            ("TI-2026-008", "Backup fallido", Ticket.ESTADO_ABIERTO, Ticket.PRIORIDAD_ALTA, 24, None),
            ("TI-2026-009", "Licencia Office", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_BAJA, 72, 60),
            ("TI-2026-010", "Actualizar antivirus", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_MEDIA, 48, 20),
            ("TI-2026-011", "Solicitud laptop", Ticket.ESTADO_ABIERTO, Ticket.PRIORIDAD_MEDIA, 48, None),
            ("TI-2026-012", "Reset MFA", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_ALTA, 24, 6),
        ]
        for i, (codigo, titulo, estado, prioridad, sla, horas_cierre) in enumerate(samples):
            apertura = now - timedelta(days=30 - i)
            cierre = apertura + timedelta(hours=horas_cierre) if horas_cierre else None
            if estado == Ticket.ESTADO_CERRADO and not cierre:
                cierre = apertura + timedelta(hours=sla - 2)
            Ticket.objects.update_or_create(
                codigo=codigo,
                defaults={
                    "titulo": titulo,
                    "descripcion": f"Ticket demo {codigo}",
                    "entidad": entidades.get("DEMO004"),
                    "unidad_negocio": unidades["TI"],
                    "estado": estado,
                    "prioridad": prioridad,
                    "asignado_a": user,
                    "fecha_apertura": apertura,
                    "fecha_cierre": cierre,
                    "sla_horas": sla,
                },
            )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Carga demo WCG One: unidades, entidades, contactos, risk snapshots y tickets PGO.
00003|Ejecutar: python manage.py seed_wcg_demo
00004|"""
00005|
00006|from __future__ import annotations
00007|
00008|from datetime import date, timedelta
00009|from decimal import Decimal
00010|
00011|from django.contrib.auth import get_user_model
00012|from django.core.management.base import BaseCommand
00013|from django.db import transaction
00014|from django.utils import timezone
00015|
00016|from core.models import UNE
00017|from core.wcg_models import Contacto, Entidad, Producto, RelacionEntidadProducto, UnidadNegocio
00018|from crm.models import Interaccion, Tarea
00019|from pgo.models import Ticket
00020|from pgo.periodo import recalculate_pgo_periodos
00021|from risk.models import RiskOperationSnapshot
00022|
00023|User = get_user_model()
00024|
00025|
00026|class Command(BaseCommand):
00027|    help = "Carga datos demo para CRM, Risk y PGO (sin depender de imports externos)"
00028|
00029|    @transaction.atomic
00030|    def handle(self, *args, **options):
00031|        self.stdout.write("Sembrando WCG One demo...")
00032|        unidades = self._seed_unidades()
00033|        productos = self._seed_productos(unidades)
00034|        entidades = self._seed_entidades(unidades)
00035|        self._seed_contactos(entidades)
00036|        self._seed_relaciones(entidades, productos)
00037|        self._seed_crm_activity(entidades)
00038|        self._seed_risk(entidades, productos)
00039|        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
00040|        self._seed_tickets(entidades, unidades, user)
00041|        recalculate_pgo_periodos()
00042|        self.stdout.write(self.style.SUCCESS(
00043|            f"Demo OK: {Entidad.objects.count()} entidades, "
00044|            f"{RiskOperationSnapshot.objects.count()} snapshots, "
00045|            f"{Ticket.objects.count()} tickets"
00046|        ))
00047|
00048|    def _seed_unidades(self):
00049|        mapping = [
00050|            ("FACTORING", "Factoraje", "FACTORING"),
00051|            ("LEASING", "Leasing", "LEASING"),
00052|            ("INSURANCE", "Insurance", "INSURANCE"),
00053|            ("INVESTMENT", "Inversiones", "INVESTMENT"),
00054|            ("TI", "Tecnología / TI", None),
00055|        ]
00056|        result = {}
00057|        for code, nombre, une_code in mapping:
00058|            une = UNE.objects.filter(code=une_code).first() if une_code else None
00059|            obj, _ = UnidadNegocio.objects.update_or_create(
00060|                code=code,
00061|                defaults={"nombre": nombre, "une_pgc": une, "activa": True},
00062|            )
00063|            result[code] = obj
00064|        return result
00065|
00066|    def _seed_productos(self, unidades):
00067|        data = [
00068|            ("LEASING", "Leasing operativo", "LEASING"),
00069|            ("FACTORING", "Factoraje", "FACTORING"),
00070|        ]
00071|        out = {}
00072|        for code, nombre, un_code in data:
00073|            obj, _ = Producto.objects.update_or_create(
00074|                codigo=code,
00075|                defaults={"nombre": nombre, "unidad_negocio": unidades[un_code], "activo": True},
00076|            )
00077|            out[code] = obj
00078|        return out
00079|
00080|    def _seed_entidades(self, unidades):
00081|        data = [
00082|            ("9852115", "VICENTE SOLER MUNGUÍA", "9852115", "LEASING"),
00083|            ("DEMO002", "Distribuidora Me Llega, S.A.", "1234567-8", "FACTORING"),
00084|            ("DEMO003", "Ingenio Palo Gordo, S.A.", "8765432-1", "LEASING"),
00085|            ("DEMO004", "Helvetia Centroamérica", "5566778-9", "INSURANCE"),
00086|            ("DEMO005", "Corporación Mogori", "9988776-5", "INVESTMENT"),
00087|        ]
00088|        out = {}
00089|        for codigo, nombre, nit, un_code in data:
00090|            obj, _ = Entidad.objects.update_or_create(
00091|                codigo=codigo,
00092|                defaults={
00093|                    "nombre": nombre,
00094|                    "nit": nit,
00095|                    "tipo": Entidad.TIPO_CLIENTE,
00096|                    "unidad_negocio": unidades[un_code],
00097|                    "activa": True,
00098|                },
00099|            )
00100|            out[codigo] = obj
00101|        return out
00102|
00103|    def _seed_contactos(self, entidades):
00104|        samples = [
00105|            ("9852115", "María Soler", "maria@soler.gt", "Gerente General"),
00106|            ("DEMO002", "Juan Pérez", "jperez@melega.gt", "CFO"),
00107|            ("DEMO003", "Ana Morales", "ana@palogordo.gt", "Tesorería"),
00108|        ]
00109|        for codigo, nombre, email, cargo in samples:
00110|            ent = entidades[codigo]
00111|            Contacto.objects.update_or_create(
00112|                entidad=ent,
00113|                email=email,
00114|                defaults={"nombre": nombre, "cargo": cargo, "es_principal": True, "activo": True},
00115|            )
00116|
00117|    def _seed_relaciones(self, entidades, productos):
00118|        RelacionEntidadProducto.objects.update_or_create(
00119|            entidad=entidades["9852115"],
00120|            producto=productos["LEASING"],
00121|            defaults={"estado": RelacionEntidadProducto.ESTADO_ACTIVO},
00122|        )
00123|
00124|    def _seed_crm_activity(self, entidades):
00125|        user = User.objects.filter(is_superuser=True).first()
00126|        now = timezone.now()
00127|        ent = entidades["9852115"]
00128|        if not ent.interacciones.exists():
00129|            Interaccion.objects.create(
00130|                entidad=ent,
00131|                tipo=Interaccion.TIPO_REUNION,
00132|                asunto="Revisión cartera leasing",
00133|                descripcion="Seguimiento trimestral",
00134|                fecha=now - timedelta(days=3),
00135|                usuario=user,
00136|            )
00137|        if not ent.tareas.exists():
00138|            Tarea.objects.create(
00139|                entidad=ent,
00140|                titulo="Enviar estados financieros actualizados",
00141|                fecha_vencimiento=date.today() + timedelta(days=7),
00142|                estado=Tarea.ESTADO_PENDIENTE,
00143|                asignado_a=user,
00144|            )
00145|
00146|    def _seed_risk(self, entidades, productos):
00147|        base = date(2026, 5, 31)
00148|        ops = [
00149|            ("9852115", "PG01260302", 45, Decimal("125000.00"), Decimal("42000.00"), True),
00150|            ("DEMO003", "LG01260115", 62, Decimal("890000.00"), Decimal("120000.00"), True),
00151|            ("DEMO002", "FC01260288", 12, Decimal("55000.00"), Decimal("0"), False),
00152|        ]
00153|        for codigo, ref, mora, saldo, exigible, alerta in ops:
00154|            ent = entidades[codigo]
00155|            nivel = RiskOperationSnapshot.NIVEL_ALTO if mora >= 30 else RiskOperationSnapshot.NIVEL_BAJO
00156|            RiskOperationSnapshot.objects.update_or_create(
00157|                entidad=ent,
00158|                referencia_operacion=ref,
00159|                fecha_snapshot=base,
00160|                defaults={
00161|                    "producto": productos.get("LEASING") or productos.get("FACTORING"),
00162|                    "nivel_riesgo": nivel,
00163|                    "dias_mora": mora,
00164|                    "saldo": saldo,
00165|                    "monto_exigible": exigible,
00166|                    "alerta": alerta,
00167|                    "detalle": "Snapshot demo mayo 2026",
00168|                },
00169|            )
00170|
00171|    def _seed_tickets(self, entidades, unidades, user):
00172|        now = timezone.now()
00173|        samples = [
00174|            ("TI-2026-001", "VPN no conecta", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_ALTA, 24, 18),
00175|            ("TI-2026-002", "Nuevo usuario CRM", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_MEDIA, 48, 36),
00176|            ("TI-2026-003", "Impresora piso 3", Ticket.ESTADO_EN_PROCESO, Ticket.PRIORIDAD_BAJA, 72, None),
00177|            ("TI-2026-004", "Error reporte PGO", Ticket.ESTADO_ABIERTO, Ticket.PRIORIDAD_ALTA, 48, None),
00178|            ("TI-2026-005", "Correo bloqueado", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_MEDIA, 48, 40),
00179|            ("TI-2026-006", "Acceso Balón Riesgo", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_MEDIA, 48, 12),
00180|            ("TI-2026-007", "Lentitud red", Ticket.ESTADO_EN_PROCESO, Ticket.PRIORIDAD_ALTA, 24, None),
00181|            ("TI-2026-008", "Backup fallido", Ticket.ESTADO_ABIERTO, Ticket.PRIORIDAD_ALTA, 24, None),
00182|            ("TI-2026-009", "Licencia Office", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_BAJA, 72, 60),
00183|            ("TI-2026-010", "Actualizar antivirus", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_MEDIA, 48, 20),
00184|            ("TI-2026-011", "Solicitud laptop", Ticket.ESTADO_ABIERTO, Ticket.PRIORIDAD_MEDIA, 48, None),
00185|            ("TI-2026-012", "Reset MFA", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_ALTA, 24, 6),
00186|        ]
00187|        for i, (codigo, titulo, estado, prioridad, sla, horas_cierre) in enumerate(samples):
00188|            apertura = now - timedelta(days=30 - i)
00189|            cierre = apertura + timedelta(hours=horas_cierre) if horas_cierre else None
00190|            if estado == Ticket.ESTADO_CERRADO and not cierre:
00191|                cierre = apertura + timedelta(hours=sla - 2)
00192|            Ticket.objects.update_or_create(
00193|                codigo=codigo,
00194|                defaults={
00195|                    "titulo": titulo,
00196|                    "descripcion": f"Ticket demo {codigo}",
00197|                    "entidad": entidades.get("DEMO004"),
00198|                    "unidad_negocio": unidades["TI"],
00199|                    "estado": estado,
00200|                    "prioridad": prioridad,
00201|                    "asignado_a": user,
00202|                    "fecha_apertura": apertura,
00203|                    "fecha_cierre": cierre,
00204|                    "sla_horas": sla,
00205|                },
00206|            )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiCkNhcmdhIGRlbW8gV0NHIE9uZTogdW5pZGFkZXMsIGVudGlkYWRlcywgY29udGFjdG9zLCByaXNrIHNuYXBzaG90cyB5IHRpY2tldHMgUEdPLgpFamVjdXRhcjogcHl0aG9uIG1hbmFnZS5weSBzZWVkX3djZ19kZW1vCiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKZnJvbSBkYXRldGltZSBpbXBvcnQgZGF0ZSwgdGltZWRlbHRhCmZyb20gZGVjaW1hbCBpbXBvcnQgRGVjaW1hbAoKZnJvbSBkamFuZ28uY29udHJpYi5hdXRoIGltcG9ydCBnZXRfdXNlcl9tb2RlbApmcm9tIGRqYW5nby5jb3JlLm1hbmFnZW1lbnQuYmFzZSBpbXBvcnQgQmFzZUNvbW1hbmQKZnJvbSBkamFuZ28uZGIgaW1wb3J0IHRyYW5zYWN0aW9uCmZyb20gZGphbmdvLnV0aWxzIGltcG9ydCB0aW1lem9uZQoKZnJvbSBjb3JlLm1vZGVscyBpbXBvcnQgVU5FCmZyb20gY29yZS53Y2dfbW9kZWxzIGltcG9ydCBDb250YWN0bywgRW50aWRhZCwgUHJvZHVjdG8sIFJlbGFjaW9uRW50aWRhZFByb2R1Y3RvLCBVbmlkYWROZWdvY2lvCmZyb20gY3JtLm1vZGVscyBpbXBvcnQgSW50ZXJhY2Npb24sIFRhcmVhCmZyb20gcGdvLm1vZGVscyBpbXBvcnQgVGlja2V0CmZyb20gcGdvLnBlcmlvZG8gaW1wb3J0IHJlY2FsY3VsYXRlX3Bnb19wZXJpb2Rvcwpmcm9tIHJpc2subW9kZWxzIGltcG9ydCBSaXNrT3BlcmF0aW9uU25hcHNob3QKClVzZXIgPSBnZXRfdXNlcl9tb2RlbCgpCgoKY2xhc3MgQ29tbWFuZChCYXNlQ29tbWFuZCk6CiAgICBoZWxwID0gIkNhcmdhIGRhdG9zIGRlbW8gcGFyYSBDUk0sIFJpc2sgeSBQR08gKHNpbiBkZXBlbmRlciBkZSBpbXBvcnRzIGV4dGVybm9zKSIKCiAgICBAdHJhbnNhY3Rpb24uYXRvbWljCiAgICBkZWYgaGFuZGxlKHNlbGYsICphcmdzLCAqKm9wdGlvbnMpOgogICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKCJTZW1icmFuZG8gV0NHIE9uZSBkZW1vLi4uIikKICAgICAgICB1bmlkYWRlcyA9IHNlbGYuX3NlZWRfdW5pZGFkZXMoKQogICAgICAgIHByb2R1Y3RvcyA9IHNlbGYuX3NlZWRfcHJvZHVjdG9zKHVuaWRhZGVzKQogICAgICAgIGVudGlkYWRlcyA9IHNlbGYuX3NlZWRfZW50aWRhZGVzKHVuaWRhZGVzKQogICAgICAgIHNlbGYuX3NlZWRfY29udGFjdG9zKGVudGlkYWRlcykKICAgICAgICBzZWxmLl9zZWVkX3JlbGFjaW9uZXMoZW50aWRhZGVzLCBwcm9kdWN0b3MpCiAgICAgICAgc2VsZi5fc2VlZF9jcm1fYWN0aXZpdHkoZW50aWRhZGVzKQogICAgICAgIHNlbGYuX3NlZWRfcmlzayhlbnRpZGFkZXMsIHByb2R1Y3RvcykKICAgICAgICB1c2VyID0gVXNlci5vYmplY3RzLmZpbHRlcihpc19zdXBlcnVzZXI9VHJ1ZSkuZmlyc3QoKSBvciBVc2VyLm9iamVjdHMuZmlyc3QoKQogICAgICAgIHNlbGYuX3NlZWRfdGlja2V0cyhlbnRpZGFkZXMsIHVuaWRhZGVzLCB1c2VyKQogICAgICAgIHJlY2FsY3VsYXRlX3Bnb19wZXJpb2RvcygpCiAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoc2VsZi5zdHlsZS5TVUNDRVNTKAogICAgICAgICAgICBmIkRlbW8gT0s6IHtFbnRpZGFkLm9iamVjdHMuY291bnQoKX0gZW50aWRhZGVzLCAiCiAgICAgICAgICAgIGYie1Jpc2tPcGVyYXRpb25TbmFwc2hvdC5vYmplY3RzLmNvdW50KCl9IHNuYXBzaG90cywgIgogICAgICAgICAgICBmIntUaWNrZXQub2JqZWN0cy5jb3VudCgpfSB0aWNrZXRzIgogICAgICAgICkpCgogICAgZGVmIF9zZWVkX3VuaWRhZGVzKHNlbGYpOgogICAgICAgIG1hcHBpbmcgPSBbCiAgICAgICAgICAgICgiRkFDVE9SSU5HIiwgIkZhY3RvcmFqZSIsICJGQUNUT1JJTkciKSwKICAgICAgICAgICAgKCJMRUFTSU5HIiwgIkxlYXNpbmciLCAiTEVBU0lORyIpLAogICAgICAgICAgICAoIklOU1VSQU5DRSIsICJJbnN1cmFuY2UiLCAiSU5TVVJBTkNFIiksCiAgICAgICAgICAgICgiSU5WRVNUTUVOVCIsICJJbnZlcnNpb25lcyIsICJJTlZFU1RNRU5UIiksCiAgICAgICAgICAgICgiVEkiLCAiVGVjbm9sb2fDrWEgLyBUSSIsIE5vbmUpLAogICAgICAgIF0KICAgICAgICByZXN1bHQgPSB7fQogICAgICAgIGZvciBjb2RlLCBub21icmUsIHVuZV9jb2RlIGluIG1hcHBpbmc6CiAgICAgICAgICAgIHVuZSA9IFVORS5vYmplY3RzLmZpbHRlcihjb2RlPXVuZV9jb2RlKS5maXJzdCgpIGlmIHVuZV9jb2RlIGVsc2UgTm9uZQogICAgICAgICAgICBvYmosIF8gPSBVbmlkYWROZWdvY2lvLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgICAgIGNvZGU9Y29kZSwKICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsibm9tYnJlIjogbm9tYnJlLCAidW5lX3BnYyI6IHVuZSwgImFjdGl2YSI6IFRydWV9LAogICAgICAgICAgICApCiAgICAgICAgICAgIHJlc3VsdFtjb2RlXSA9IG9iagogICAgICAgIHJldHVybiByZXN1bHQKCiAgICBkZWYgX3NlZWRfcHJvZHVjdG9zKHNlbGYsIHVuaWRhZGVzKToKICAgICAgICBkYXRhID0gWwogICAgICAgICAgICAoIkxFQVNJTkciLCAiTGVhc2luZyBvcGVyYXRpdm8iLCAiTEVBU0lORyIpLAogICAgICAgICAgICAoIkZBQ1RPUklORyIsICJGYWN0b3JhamUiLCAiRkFDVE9SSU5HIiksCiAgICAgICAgXQogICAgICAgIG91dCA9IHt9CiAgICAgICAgZm9yIGNvZGUsIG5vbWJyZSwgdW5fY29kZSBpbiBkYXRhOgogICAgICAgICAgICBvYmosIF8gPSBQcm9kdWN0by5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICBjb2RpZ289Y29kZSwKICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsibm9tYnJlIjogbm9tYnJlLCAidW5pZGFkX25lZ29jaW8iOiB1bmlkYWRlc1t1bl9jb2RlXSwgImFjdGl2byI6IFRydWV9LAogICAgICAgICAgICApCiAgICAgICAgICAgIG91dFtjb2RlXSA9IG9iagogICAgICAgIHJldHVybiBvdXQKCiAgICBkZWYgX3NlZWRfZW50aWRhZGVzKHNlbGYsIHVuaWRhZGVzKToKICAgICAgICBkYXRhID0gWwogICAgICAgICAgICAoIjk4NTIxMTUiLCAiVklDRU5URSBTT0xFUiBNVU5HVcONQSIsICI5ODUyMTE1IiwgIkxFQVNJTkciKSwKICAgICAgICAgICAgKCJERU1PMDAyIiwgIkRpc3RyaWJ1aWRvcmEgTWUgTGxlZ2EsIFMuQS4iLCAiMTIzNDU2Ny04IiwgIkZBQ1RPUklORyIpLAogICAgICAgICAgICAoIkRFTU8wMDMiLCAiSW5nZW5pbyBQYWxvIEdvcmRvLCBTLkEuIiwgIjg3NjU0MzItMSIsICJMRUFTSU5HIiksCiAgICAgICAgICAgICgiREVNTzAwNCIsICJIZWx2ZXRpYSBDZW50cm9hbcOpcmljYSIsICI1NTY2Nzc4LTkiLCAiSU5TVVJBTkNFIiksCiAgICAgICAgICAgICgiREVNTzAwNSIsICJDb3Jwb3JhY2nDs24gTW9nb3JpIiwgIjk5ODg3NzYtNSIsICJJTlZFU1RNRU5UIiksCiAgICAgICAgXQogICAgICAgIG91dCA9IHt9CiAgICAgICAgZm9yIGNvZGlnbywgbm9tYnJlLCBuaXQsIHVuX2NvZGUgaW4gZGF0YToKICAgICAgICAgICAgb2JqLCBfID0gRW50aWRhZC5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICBjb2RpZ289Y29kaWdvLAogICAgICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgICAgICJub21icmUiOiBub21icmUsCiAgICAgICAgICAgICAgICAgICAgIm5pdCI6IG5pdCwKICAgICAgICAgICAgICAgICAgICAidGlwbyI6IEVudGlkYWQuVElQT19DTElFTlRFLAogICAgICAgICAgICAgICAgICAgICJ1bmlkYWRfbmVnb2NpbyI6IHVuaWRhZGVzW3VuX2NvZGVdLAogICAgICAgICAgICAgICAgICAgICJhY3RpdmEiOiBUcnVlLAogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgKQogICAgICAgICAgICBvdXRbY29kaWdvXSA9IG9iagogICAgICAgIHJldHVybiBvdXQKCiAgICBkZWYgX3NlZWRfY29udGFjdG9zKHNlbGYsIGVudGlkYWRlcyk6CiAgICAgICAgc2FtcGxlcyA9IFsKICAgICAgICAgICAgKCI5ODUyMTE1IiwgIk1hcsOtYSBTb2xlciIsICJtYXJpYUBzb2xlci5ndCIsICJHZXJlbnRlIEdlbmVyYWwiKSwKICAgICAgICAgICAgKCJERU1PMDAyIiwgIkp1YW4gUMOpcmV6IiwgImpwZXJlekBtZWxlZ2EuZ3QiLCAiQ0ZPIiksCiAgICAgICAgICAgICgiREVNTzAwMyIsICJBbmEgTW9yYWxlcyIsICJhbmFAcGFsb2dvcmRvLmd0IiwgIlRlc29yZXLDrWEiKSwKICAgICAgICBdCiAgICAgICAgZm9yIGNvZGlnbywgbm9tYnJlLCBlbWFpbCwgY2FyZ28gaW4gc2FtcGxlczoKICAgICAgICAgICAgZW50ID0gZW50aWRhZGVzW2NvZGlnb10KICAgICAgICAgICAgQ29udGFjdG8ub2JqZWN0cy51cGRhdGVfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgZW50aWRhZD1lbnQsCiAgICAgICAgICAgICAgICBlbWFpbD1lbWFpbCwKICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsibm9tYnJlIjogbm9tYnJlLCAiY2FyZ28iOiBjYXJnbywgImVzX3ByaW5jaXBhbCI6IFRydWUsICJhY3Rpdm8iOiBUcnVlfSwKICAgICAgICAgICAgKQoKICAgIGRlZiBfc2VlZF9yZWxhY2lvbmVzKHNlbGYsIGVudGlkYWRlcywgcHJvZHVjdG9zKToKICAgICAgICBSZWxhY2lvbkVudGlkYWRQcm9kdWN0by5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgIGVudGlkYWQ9ZW50aWRhZGVzWyI5ODUyMTE1Il0sCiAgICAgICAgICAgIHByb2R1Y3RvPXByb2R1Y3Rvc1siTEVBU0lORyJdLAogICAgICAgICAgICBkZWZhdWx0cz17ImVzdGFkbyI6IFJlbGFjaW9uRW50aWRhZFByb2R1Y3RvLkVTVEFET19BQ1RJVk99LAogICAgICAgICkKCiAgICBkZWYgX3NlZWRfY3JtX2FjdGl2aXR5KHNlbGYsIGVudGlkYWRlcyk6CiAgICAgICAgdXNlciA9IFVzZXIub2JqZWN0cy5maWx0ZXIoaXNfc3VwZXJ1c2VyPVRydWUpLmZpcnN0KCkKICAgICAgICBub3cgPSB0aW1lem9uZS5ub3coKQogICAgICAgIGVudCA9IGVudGlkYWRlc1siOTg1MjExNSJdCiAgICAgICAgaWYgbm90IGVudC5pbnRlcmFjY2lvbmVzLmV4aXN0cygpOgogICAgICAgICAgICBJbnRlcmFjY2lvbi5vYmplY3RzLmNyZWF0ZSgKICAgICAgICAgICAgICAgIGVudGlkYWQ9ZW50LAogICAgICAgICAgICAgICAgdGlwbz1JbnRlcmFjY2lvbi5USVBPX1JFVU5JT04sCiAgICAgICAgICAgICAgICBhc3VudG89IlJldmlzacOzbiBjYXJ0ZXJhIGxlYXNpbmciLAogICAgICAgICAgICAgICAgZGVzY3JpcGNpb249IlNlZ3VpbWllbnRvIHRyaW1lc3RyYWwiLAogICAgICAgICAgICAgICAgZmVjaGE9bm93IC0gdGltZWRlbHRhKGRheXM9MyksCiAgICAgICAgICAgICAgICB1c3VhcmlvPXVzZXIsCiAgICAgICAgICAgICkKICAgICAgICBpZiBub3QgZW50LnRhcmVhcy5leGlzdHMoKToKICAgICAgICAgICAgVGFyZWEub2JqZWN0cy5jcmVhdGUoCiAgICAgICAgICAgICAgICBlbnRpZGFkPWVudCwKICAgICAgICAgICAgICAgIHRpdHVsbz0iRW52aWFyIGVzdGFkb3MgZmluYW5jaWVyb3MgYWN0dWFsaXphZG9zIiwKICAgICAgICAgICAgICAgIGZlY2hhX3ZlbmNpbWllbnRvPWRhdGUudG9kYXkoKSArIHRpbWVkZWx0YShkYXlzPTcpLAogICAgICAgICAgICAgICAgZXN0YWRvPVRhcmVhLkVTVEFET19QRU5ESUVOVEUsCiAgICAgICAgICAgICAgICBhc2lnbmFkb19hPXVzZXIsCiAgICAgICAgICAgICkKCiAgICBkZWYgX3NlZWRfcmlzayhzZWxmLCBlbnRpZGFkZXMsIHByb2R1Y3Rvcyk6CiAgICAgICAgYmFzZSA9IGRhdGUoMjAyNiwgNSwgMzEpCiAgICAgICAgb3BzID0gWwogICAgICAgICAgICAoIjk4NTIxMTUiLCAiUEcwMTI2MDMwMiIsIDQ1LCBEZWNpbWFsKCIxMjUwMDAuMDAiKSwgRGVjaW1hbCgiNDIwMDAuMDAiKSwgVHJ1ZSksCiAgICAgICAgICAgICgiREVNTzAwMyIsICJMRzAxMjYwMTE1IiwgNjIsIERlY2ltYWwoIjg5MDAwMC4wMCIpLCBEZWNpbWFsKCIxMjAwMDAuMDAiKSwgVHJ1ZSksCiAgICAgICAgICAgICgiREVNTzAwMiIsICJGQzAxMjYwMjg4IiwgMTIsIERlY2ltYWwoIjU1MDAwLjAwIiksIERlY2ltYWwoIjAiKSwgRmFsc2UpLAogICAgICAgIF0KICAgICAgICBmb3IgY29kaWdvLCByZWYsIG1vcmEsIHNhbGRvLCBleGlnaWJsZSwgYWxlcnRhIGluIG9wczoKICAgICAgICAgICAgZW50ID0gZW50aWRhZGVzW2NvZGlnb10KICAgICAgICAgICAgbml2ZWwgPSBSaXNrT3BlcmF0aW9uU25hcHNob3QuTklWRUxfQUxUTyBpZiBtb3JhID49IDMwIGVsc2UgUmlza09wZXJhdGlvblNuYXBzaG90Lk5JVkVMX0JBSk8KICAgICAgICAgICAgUmlza09wZXJhdGlvblNuYXBzaG90Lm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgICAgIGVudGlkYWQ9ZW50LAogICAgICAgICAgICAgICAgcmVmZXJlbmNpYV9vcGVyYWNpb249cmVmLAogICAgICAgICAgICAgICAgZmVjaGFfc25hcHNob3Q9YmFzZSwKICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsKICAgICAgICAgICAgICAgICAgICAicHJvZHVjdG8iOiBwcm9kdWN0b3MuZ2V0KCJMRUFTSU5HIikgb3IgcHJvZHVjdG9zLmdldCgiRkFDVE9SSU5HIiksCiAgICAgICAgICAgICAgICAgICAgIm5pdmVsX3JpZXNnbyI6IG5pdmVsLAogICAgICAgICAgICAgICAgICAgICJkaWFzX21vcmEiOiBtb3JhLAogICAgICAgICAgICAgICAgICAgICJzYWxkbyI6IHNhbGRvLAogICAgICAgICAgICAgICAgICAgICJtb250b19leGlnaWJsZSI6IGV4aWdpYmxlLAogICAgICAgICAgICAgICAgICAgICJhbGVydGEiOiBhbGVydGEsCiAgICAgICAgICAgICAgICAgICAgImRldGFsbGUiOiAiU25hcHNob3QgZGVtbyBtYXlvIDIwMjYiLAogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgKQoKICAgIGRlZiBfc2VlZF90aWNrZXRzKHNlbGYsIGVudGlkYWRlcywgdW5pZGFkZXMsIHVzZXIpOgogICAgICAgIG5vdyA9IHRpbWV6b25lLm5vdygpCiAgICAgICAgc2FtcGxlcyA9IFsKICAgICAgICAgICAgKCJUSS0yMDI2LTAwMSIsICJWUE4gbm8gY29uZWN0YSIsIFRpY2tldC5FU1RBRE9fQ0VSUkFETywgVGlja2V0LlBSSU9SSURBRF9BTFRBLCAyNCwgMTgpLAogICAgICAgICAgICAoIlRJLTIwMjYtMDAyIiwgIk51ZXZvIHVzdWFyaW8gQ1JNIiwgVGlja2V0LkVTVEFET19DRVJSQURPLCBUaWNrZXQuUFJJT1JJREFEX01FRElBLCA0OCwgMzYpLAogICAgICAgICAgICAoIlRJLTIwMjYtMDAzIiwgIkltcHJlc29yYSBwaXNvIDMiLCBUaWNrZXQuRVNUQURPX0VOX1BST0NFU08sIFRpY2tldC5QUklPUklEQURfQkFKQSwgNzIsIE5vbmUpLAogICAgICAgICAgICAoIlRJLTIwMjYtMDA0IiwgIkVycm9yIHJlcG9ydGUgUEdPIiwgVGlja2V0LkVTVEFET19BQklFUlRPLCBUaWNrZXQuUFJJT1JJREFEX0FMVEEsIDQ4LCBOb25lKSwKICAgICAgICAgICAgKCJUSS0yMDI2LTAwNSIsICJDb3JyZW8gYmxvcXVlYWRvIiwgVGlja2V0LkVTVEFET19DRVJSQURPLCBUaWNrZXQuUFJJT1JJREFEX01FRElBLCA0OCwgNDApLAogICAgICAgICAgICAoIlRJLTIwMjYtMDA2IiwgIkFjY2VzbyBCYWzDs24gUmllc2dvIiwgVGlja2V0LkVTVEFET19DRVJSQURPLCBUaWNrZXQuUFJJT1JJREFEX01FRElBLCA0OCwgMTIpLAogICAgICAgICAgICAoIlRJLTIwMjYtMDA3IiwgIkxlbnRpdHVkIHJlZCIsIFRpY2tldC5FU1RBRE9fRU5fUFJPQ0VTTywgVGlja2V0LlBSSU9SSURBRF9BTFRBLCAyNCwgTm9uZSksCiAgICAgICAgICAgICgiVEktMjAyNi0wMDgiLCAiQmFja3VwIGZhbGxpZG8iLCBUaWNrZXQuRVNUQURPX0FCSUVSVE8sIFRpY2tldC5QUklPUklEQURfQUxUQSwgMjQsIE5vbmUpLAogICAgICAgICAgICAoIlRJLTIwMjYtMDA5IiwgIkxpY2VuY2lhIE9mZmljZSIsIFRpY2tldC5FU1RBRE9fQ0VSUkFETywgVGlja2V0LlBSSU9SSURBRF9CQUpBLCA3MiwgNjApLAogICAgICAgICAgICAoIlRJLTIwMjYtMDEwIiwgIkFjdHVhbGl6YXIgYW50aXZpcnVzIiwgVGlja2V0LkVTVEFET19DRVJSQURPLCBUaWNrZXQuUFJJT1JJREFEX01FRElBLCA0OCwgMjApLAogICAgICAgICAgICAoIlRJLTIwMjYtMDExIiwgIlNvbGljaXR1ZCBsYXB0b3AiLCBUaWNrZXQuRVNUQURPX0FCSUVSVE8sIFRpY2tldC5QUklPUklEQURfTUVESUEsIDQ4LCBOb25lKSwKICAgICAgICAgICAgKCJUSS0yMDI2LTAxMiIsICJSZXNldCBNRkEiLCBUaWNrZXQuRVNUQURPX0NFUlJBRE8sIFRpY2tldC5QUklPUklEQURfQUxUQSwgMjQsIDYpLAogICAgICAgIF0KICAgICAgICBmb3IgaSwgKGNvZGlnbywgdGl0dWxvLCBlc3RhZG8sIHByaW9yaWRhZCwgc2xhLCBob3Jhc19jaWVycmUpIGluIGVudW1lcmF0ZShzYW1wbGVzKToKICAgICAgICAgICAgYXBlcnR1cmEgPSBub3cgLSB0aW1lZGVsdGEoZGF5cz0zMCAtIGkpCiAgICAgICAgICAgIGNpZXJyZSA9IGFwZXJ0dXJhICsgdGltZWRlbHRhKGhvdXJzPWhvcmFzX2NpZXJyZSkgaWYgaG9yYXNfY2llcnJlIGVsc2UgTm9uZQogICAgICAgICAgICBpZiBlc3RhZG8gPT0gVGlja2V0LkVTVEFET19DRVJSQURPIGFuZCBub3QgY2llcnJlOgogICAgICAgICAgICAgICAgY2llcnJlID0gYXBlcnR1cmEgKyB0aW1lZGVsdGEoaG91cnM9c2xhIC0gMikKICAgICAgICAgICAgVGlja2V0Lm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgICAgIGNvZGlnbz1jb2RpZ28sCiAgICAgICAgICAgICAgICBkZWZhdWx0cz17CiAgICAgICAgICAgICAgICAgICAgInRpdHVsbyI6IHRpdHVsbywKICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcGNpb24iOiBmIlRpY2tldCBkZW1vIHtjb2RpZ299IiwKICAgICAgICAgICAgICAgICAgICAiZW50aWRhZCI6IGVudGlkYWRlcy5nZXQoIkRFTU8wMDQiKSwKICAgICAgICAgICAgICAgICAgICAidW5pZGFkX25lZ29jaW8iOiB1bmlkYWRlc1siVEkiXSwKICAgICAgICAgICAgICAgICAgICAiZXN0YWRvIjogZXN0YWRvLAogICAgICAgICAgICAgICAgICAgICJwcmlvcmlkYWQiOiBwcmlvcmlkYWQsCiAgICAgICAgICAgICAgICAgICAgImFzaWduYWRvX2EiOiB1c2VyLAogICAgICAgICAgICAgICAgICAgICJmZWNoYV9hcGVydHVyYSI6IGFwZXJ0dXJhLAogICAgICAgICAgICAgICAgICAgICJmZWNoYV9jaWVycmUiOiBjaWVycmUsCiAgICAgICAgICAgICAgICAgICAgInNsYV9ob3JhcyI6IHNsYSwKICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICkK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/models.py
PATH_JSON="core/models.py"
FILENAME=models.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=142
SIZE_BYTES_UTF8=3973
CONTENT_SHA256=2d33144c010847fdf67798f1a590b6499168f73923a041d2aa64d73c07871c34
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
from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UNE(TimeStampedModel):
    CODE_FACTORING = 'FACTORING'
    CODE_LEASING = 'LEASING'
    CODE_INSURANCE = 'INSURANCE'
    CODE_INVESTMENT = 'INVESTMENT'

    CODE_CHOICES = [
        (CODE_FACTORING, 'Factoraje'),
        (CODE_LEASING, 'Leasing'),
        (CODE_INSURANCE, 'Insurance'),
        (CODE_INVESTMENT, 'Inversiones'),
    ]

    UNIT_USD = 'USD'
    UNIT_KUSD = 'KUSD'
    UNIT_GTQ = 'GTQ'
    UNIT_KGTQ = 'KGTQ'

    UNIT_CHOICES = [
        (UNIT_USD, 'USD (dólares)'),
        (UNIT_KUSD, 'Miles de USD'),
        (UNIT_GTQ, 'GTQ (quetzales)'),
        (UNIT_KGTQ, 'Miles de GTQ'),
    ]

    code = models.CharField(max_length=20, unique=True, choices=CODE_CHOICES)
    name = models.CharField(max_length=50)
    name_es = models.CharField(max_length=50)
    default_amount_unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default=UNIT_KUSD,
        help_text='Unidad habitual de reporte para montos en esta UNE.',
    )
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name_es']
        verbose_name = 'UNE'
        verbose_name_plural = 'UNEs'

    def __str__(self):
        return self.name_es


class UNEAlias(TimeStampedModel):
    raw_value = models.CharField(max_length=255, unique=True)
    une = models.ForeignKey(UNE, on_delete=models.CASCADE, related_name='aliases')
    alias_type = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['raw_value']
        verbose_name = 'Alias de UNE'
        verbose_name_plural = 'Aliases de UNE'

    def __str__(self):
        return f'{self.raw_value} -> {self.une.code}'


class Currency(TimeStampedModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['code']
        verbose_name = 'Moneda'
        verbose_name_plural = 'Monedas'

    def __str__(self):
        return self.code


class MetricDefinition(TimeStampedModel):
    CODE_INGRESOS = 'INGRESOS'
    CODE_CLIENTES_NUEVOS = 'CLIENTES_NUEVOS'
    CODE_VENTA_CRUZADA = 'VENTA_CRUZADA'
    CODE_RESPUESTA_REQS = 'RESPUESTA_REQS'

    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_scored = models.BooleanField(default=True)

    class Meta:
        ordering = ['code']
        verbose_name = 'Métrica'
        verbose_name_plural = 'Métricas'

    def __str__(self):
        return self.name


class SystemSetting(TimeStampedModel):
    key = models.CharField(max_length=100, unique=True)
    value_text = models.TextField(blank=True, null=True)
    value_bool = models.BooleanField(blank=True, null=True)
    value_json = models.JSONField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_system_settings'
    )

    class Meta:
        ordering = ['key']
        verbose_name = 'Configuración del sistema'
        verbose_name_plural = 'Configuraciones del sistema'

    def __str__(self):
        return self.key


# Maestro común WCG One (CRM, Risk, PGO, PGC)
from .wcg_models import (  # noqa: E402, F401
    Contacto,
    DataDictionary,
    DataImportBatch,
    Entidad,
    Producto,
    RelacionEntidadProducto,
    UnidadNegocio,
)
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.conf import settings
00002|from django.db import models
00003|
00004|
00005|class TimeStampedModel(models.Model):
00006|    created_at = models.DateTimeField(auto_now_add=True)
00007|    updated_at = models.DateTimeField(auto_now=True)
00008|
00009|    class Meta:
00010|        abstract = True
00011|
00012|
00013|class UNE(TimeStampedModel):
00014|    CODE_FACTORING = 'FACTORING'
00015|    CODE_LEASING = 'LEASING'
00016|    CODE_INSURANCE = 'INSURANCE'
00017|    CODE_INVESTMENT = 'INVESTMENT'
00018|
00019|    CODE_CHOICES = [
00020|        (CODE_FACTORING, 'Factoraje'),
00021|        (CODE_LEASING, 'Leasing'),
00022|        (CODE_INSURANCE, 'Insurance'),
00023|        (CODE_INVESTMENT, 'Inversiones'),
00024|    ]
00025|
00026|    UNIT_USD = 'USD'
00027|    UNIT_KUSD = 'KUSD'
00028|    UNIT_GTQ = 'GTQ'
00029|    UNIT_KGTQ = 'KGTQ'
00030|
00031|    UNIT_CHOICES = [
00032|        (UNIT_USD, 'USD (dólares)'),
00033|        (UNIT_KUSD, 'Miles de USD'),
00034|        (UNIT_GTQ, 'GTQ (quetzales)'),
00035|        (UNIT_KGTQ, 'Miles de GTQ'),
00036|    ]
00037|
00038|    code = models.CharField(max_length=20, unique=True, choices=CODE_CHOICES)
00039|    name = models.CharField(max_length=50)
00040|    name_es = models.CharField(max_length=50)
00041|    default_amount_unit = models.CharField(
00042|        max_length=10,
00043|        choices=UNIT_CHOICES,
00044|        default=UNIT_KUSD,
00045|        help_text='Unidad habitual de reporte para montos en esta UNE.',
00046|    )
00047|    is_active = models.BooleanField(default=True)
00048|    sort_order = models.PositiveSmallIntegerField(default=0)
00049|
00050|    class Meta:
00051|        ordering = ['sort_order', 'name_es']
00052|        verbose_name = 'UNE'
00053|        verbose_name_plural = 'UNEs'
00054|
00055|    def __str__(self):
00056|        return self.name_es
00057|
00058|
00059|class UNEAlias(TimeStampedModel):
00060|    raw_value = models.CharField(max_length=255, unique=True)
00061|    une = models.ForeignKey(UNE, on_delete=models.CASCADE, related_name='aliases')
00062|    alias_type = models.CharField(max_length=50, blank=True)
00063|    is_active = models.BooleanField(default=True)
00064|
00065|    class Meta:
00066|        ordering = ['raw_value']
00067|        verbose_name = 'Alias de UNE'
00068|        verbose_name_plural = 'Aliases de UNE'
00069|
00070|    def __str__(self):
00071|        return f'{self.raw_value} -> {self.une.code}'
00072|
00073|
00074|class Currency(TimeStampedModel):
00075|    code = models.CharField(max_length=10, unique=True)
00076|    name = models.CharField(max_length=50)
00077|    symbol = models.CharField(max_length=10, blank=True)
00078|    is_active = models.BooleanField(default=True)
00079|
00080|    class Meta:
00081|        ordering = ['code']
00082|        verbose_name = 'Moneda'
00083|        verbose_name_plural = 'Monedas'
00084|
00085|    def __str__(self):
00086|        return self.code
00087|
00088|
00089|class MetricDefinition(TimeStampedModel):
00090|    CODE_INGRESOS = 'INGRESOS'
00091|    CODE_CLIENTES_NUEVOS = 'CLIENTES_NUEVOS'
00092|    CODE_VENTA_CRUZADA = 'VENTA_CRUZADA'
00093|    CODE_RESPUESTA_REQS = 'RESPUESTA_REQS'
00094|
00095|    code = models.CharField(max_length=50, unique=True)
00096|    name = models.CharField(max_length=100)
00097|    description = models.TextField(blank=True)
00098|    is_scored = models.BooleanField(default=True)
00099|
00100|    class Meta:
00101|        ordering = ['code']
00102|        verbose_name = 'Métrica'
00103|        verbose_name_plural = 'Métricas'
00104|
00105|    def __str__(self):
00106|        return self.name
00107|
00108|
00109|class SystemSetting(TimeStampedModel):
00110|    key = models.CharField(max_length=100, unique=True)
00111|    value_text = models.TextField(blank=True, null=True)
00112|    value_bool = models.BooleanField(blank=True, null=True)
00113|    value_json = models.JSONField(blank=True, null=True)
00114|    description = models.CharField(max_length=255, blank=True)
00115|    updated_by = models.ForeignKey(
00116|        settings.AUTH_USER_MODEL,
00117|        on_delete=models.SET_NULL,
00118|        null=True,
00119|        blank=True,
00120|        related_name='updated_system_settings'
00121|    )
00122|
00123|    class Meta:
00124|        ordering = ['key']
00125|        verbose_name = 'Configuración del sistema'
00126|        verbose_name_plural = 'Configuraciones del sistema'
00127|
00128|    def __str__(self):
00129|        return self.key
00130|
00131|
00132|# Maestro común WCG One (CRM, Risk, PGO, PGC)
00133|from .wcg_models import (  # noqa: E402, F401
00134|    Contacto,
00135|    DataDictionary,
00136|    DataImportBatch,
00137|    Entidad,
00138|    Producto,
00139|    RelacionEntidadProducto,
00140|    UnidadNegocio,
00141|)
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29uZiBpbXBvcnQgc2V0dGluZ3MKZnJvbSBkamFuZ28uZGIgaW1wb3J0IG1vZGVscwoKCmNsYXNzIFRpbWVTdGFtcGVkTW9kZWwobW9kZWxzLk1vZGVsKToKICAgIGNyZWF0ZWRfYXQgPSBtb2RlbHMuRGF0ZVRpbWVGaWVsZChhdXRvX25vd19hZGQ9VHJ1ZSkKICAgIHVwZGF0ZWRfYXQgPSBtb2RlbHMuRGF0ZVRpbWVGaWVsZChhdXRvX25vdz1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgYWJzdHJhY3QgPSBUcnVlCgoKY2xhc3MgVU5FKFRpbWVTdGFtcGVkTW9kZWwpOgogICAgQ09ERV9GQUNUT1JJTkcgPSAnRkFDVE9SSU5HJwogICAgQ09ERV9MRUFTSU5HID0gJ0xFQVNJTkcnCiAgICBDT0RFX0lOU1VSQU5DRSA9ICdJTlNVUkFOQ0UnCiAgICBDT0RFX0lOVkVTVE1FTlQgPSAnSU5WRVNUTUVOVCcKCiAgICBDT0RFX0NIT0lDRVMgPSBbCiAgICAgICAgKENPREVfRkFDVE9SSU5HLCAnRmFjdG9yYWplJyksCiAgICAgICAgKENPREVfTEVBU0lORywgJ0xlYXNpbmcnKSwKICAgICAgICAoQ09ERV9JTlNVUkFOQ0UsICdJbnN1cmFuY2UnKSwKICAgICAgICAoQ09ERV9JTlZFU1RNRU5ULCAnSW52ZXJzaW9uZXMnKSwKICAgIF0KCiAgICBVTklUX1VTRCA9ICdVU0QnCiAgICBVTklUX0tVU0QgPSAnS1VTRCcKICAgIFVOSVRfR1RRID0gJ0dUUScKICAgIFVOSVRfS0dUUSA9ICdLR1RRJwoKICAgIFVOSVRfQ0hPSUNFUyA9IFsKICAgICAgICAoVU5JVF9VU0QsICdVU0QgKGTDs2xhcmVzKScpLAogICAgICAgIChVTklUX0tVU0QsICdNaWxlcyBkZSBVU0QnKSwKICAgICAgICAoVU5JVF9HVFEsICdHVFEgKHF1ZXR6YWxlcyknKSwKICAgICAgICAoVU5JVF9LR1RRLCAnTWlsZXMgZGUgR1RRJyksCiAgICBdCgogICAgY29kZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yMCwgdW5pcXVlPVRydWUsIGNob2ljZXM9Q09ERV9DSE9JQ0VTKQogICAgbmFtZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD01MCkKICAgIG5hbWVfZXMgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9NTApCiAgICBkZWZhdWx0X2Ftb3VudF91bml0ID0gbW9kZWxzLkNoYXJGaWVsZCgKICAgICAgICBtYXhfbGVuZ3RoPTEwLAogICAgICAgIGNob2ljZXM9VU5JVF9DSE9JQ0VTLAogICAgICAgIGRlZmF1bHQ9VU5JVF9LVVNELAogICAgICAgIGhlbHBfdGV4dD0nVW5pZGFkIGhhYml0dWFsIGRlIHJlcG9ydGUgcGFyYSBtb250b3MgZW4gZXN0YSBVTkUuJywKICAgICkKICAgIGlzX2FjdGl2ZSA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1UcnVlKQogICAgc29ydF9vcmRlciA9IG1vZGVscy5Qb3NpdGl2ZVNtYWxsSW50ZWdlckZpZWxkKGRlZmF1bHQ9MCkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIG9yZGVyaW5nID0gWydzb3J0X29yZGVyJywgJ25hbWVfZXMnXQogICAgICAgIHZlcmJvc2VfbmFtZSA9ICdVTkUnCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICdVTkVzJwoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBzZWxmLm5hbWVfZXMKCgpjbGFzcyBVTkVBbGlhcyhUaW1lU3RhbXBlZE1vZGVsKToKICAgIHJhd192YWx1ZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yNTUsIHVuaXF1ZT1UcnVlKQogICAgdW5lID0gbW9kZWxzLkZvcmVpZ25LZXkoVU5FLCBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsIHJlbGF0ZWRfbmFtZT0nYWxpYXNlcycpCiAgICBhbGlhc190eXBlID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTUwLCBibGFuaz1UcnVlKQogICAgaXNfYWN0aXZlID0gbW9kZWxzLkJvb2xlYW5GaWVsZChkZWZhdWx0PVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICBvcmRlcmluZyA9IFsncmF3X3ZhbHVlJ10KICAgICAgICB2ZXJib3NlX25hbWUgPSAnQWxpYXMgZGUgVU5FJwogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAnQWxpYXNlcyBkZSBVTkUnCgogICAgZGVmIF9fc3RyX18oc2VsZik6CiAgICAgICAgcmV0dXJuIGYne3NlbGYucmF3X3ZhbHVlfSAtPiB7c2VsZi51bmUuY29kZX0nCgoKY2xhc3MgQ3VycmVuY3koVGltZVN0YW1wZWRNb2RlbCk6CiAgICBjb2RlID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwLCB1bmlxdWU9VHJ1ZSkKICAgIG5hbWUgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9NTApCiAgICBzeW1ib2wgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAsIGJsYW5rPVRydWUpCiAgICBpc19hY3RpdmUgPSBtb2RlbHMuQm9vbGVhbkZpZWxkKGRlZmF1bHQ9VHJ1ZSkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIG9yZGVyaW5nID0gWydjb2RlJ10KICAgICAgICB2ZXJib3NlX25hbWUgPSAnTW9uZWRhJwogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAnTW9uZWRhcycKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gc2VsZi5jb2RlCgoKY2xhc3MgTWV0cmljRGVmaW5pdGlvbihUaW1lU3RhbXBlZE1vZGVsKToKICAgIENPREVfSU5HUkVTT1MgPSAnSU5HUkVTT1MnCiAgICBDT0RFX0NMSUVOVEVTX05VRVZPUyA9ICdDTElFTlRFU19OVUVWT1MnCiAgICBDT0RFX1ZFTlRBX0NSVVpBREEgPSAnVkVOVEFfQ1JVWkFEQScKICAgIENPREVfUkVTUFVFU1RBX1JFUVMgPSAnUkVTUFVFU1RBX1JFUVMnCgogICAgY29kZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD01MCwgdW5pcXVlPVRydWUpCiAgICBuYW1lID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwMCkKICAgIGRlc2NyaXB0aW9uID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQogICAgaXNfc2NvcmVkID0gbW9kZWxzLkJvb2xlYW5GaWVsZChkZWZhdWx0PVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICBvcmRlcmluZyA9IFsnY29kZSddCiAgICAgICAgdmVyYm9zZV9uYW1lID0gJ03DqXRyaWNhJwogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAnTcOpdHJpY2FzJwoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBzZWxmLm5hbWUKCgpjbGFzcyBTeXN0ZW1TZXR0aW5nKFRpbWVTdGFtcGVkTW9kZWwpOgogICAga2V5ID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwMCwgdW5pcXVlPVRydWUpCiAgICB2YWx1ZV90ZXh0ID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlLCBudWxsPVRydWUpCiAgICB2YWx1ZV9ib29sID0gbW9kZWxzLkJvb2xlYW5GaWVsZChibGFuaz1UcnVlLCBudWxsPVRydWUpCiAgICB2YWx1ZV9qc29uID0gbW9kZWxzLkpTT05GaWVsZChibGFuaz1UcnVlLCBudWxsPVRydWUpCiAgICBkZXNjcmlwdGlvbiA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yNTUsIGJsYW5rPVRydWUpCiAgICB1cGRhdGVkX2J5ID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgc2V0dGluZ3MuQVVUSF9VU0VSX01PREVMLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSd1cGRhdGVkX3N5c3RlbV9zZXR0aW5ncycKICAgICkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIG9yZGVyaW5nID0gWydrZXknXQogICAgICAgIHZlcmJvc2VfbmFtZSA9ICdDb25maWd1cmFjacOzbiBkZWwgc2lzdGVtYScKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gJ0NvbmZpZ3VyYWNpb25lcyBkZWwgc2lzdGVtYScKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gc2VsZi5rZXkKCgojIE1hZXN0cm8gY29tw7puIFdDRyBPbmUgKENSTSwgUmlzaywgUEdPLCBQR0MpCmZyb20gLndjZ19tb2RlbHMgaW1wb3J0ICggICMgbm9xYTogRTQwMiwgRjQwMQogICAgQ29udGFjdG8sCiAgICBEYXRhRGljdGlvbmFyeSwKICAgIERhdGFJbXBvcnRCYXRjaCwKICAgIEVudGlkYWQsCiAgICBQcm9kdWN0bywKICAgIFJlbGFjaW9uRW50aWRhZFByb2R1Y3RvLAogICAgVW5pZGFkTmVnb2NpbywKKQ==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/services/__init__.py
PATH_JSON="core/services/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=1
SIZE_BYTES_UTF8=1
CONTENT_SHA256=01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
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


~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/services/column_map.py
PATH_JSON="core/services/column_map.py"
FILENAME=column_map.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=71
SIZE_BYTES_UTF8=2165
CONTENT_SHA256=c976ce2c016553d09cea37c67efc07009dee2c309239151fb463ae800665ff84
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
"""Mapeo de columnas reales (CSV/XLSX) a nombres canónicos de importación."""

from __future__ import annotations

import re
import unicodedata

import pandas as pd

from .import_base import cell_str


def _norm_header(name: str) -> str:
    s = unicodedata.normalize("NFKD", str(name))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("\ufeff", "").strip()
    # NombreCliente / Client Name → snake_case usable por aliases
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    s = s.lower()
    s = re.sub(r"[^\w]+", "_", s)
    return s.strip("_")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [_norm_header(c) for c in df.columns]
    return df


def pick(row: pd.Series, *aliases: str) -> str:
    """Primer alias presente en la fila (columnas ya normalizadas)."""
    for alias in aliases:
        key = _norm_header(alias)
        if key in row.index:
            val = cell_str(row.get(key))
            if val:
                return val
    return ""


def pick_decimal(row: pd.Series, *aliases: str, default: str = "0"):
    from decimal import Decimal, InvalidOperation

    raw = pick(row, *aliases) or default
    try:
        return Decimal(raw.replace(",", "").replace("Q", "").replace("$", "").strip())
    except (InvalidOperation, AttributeError):
        return Decimal(default)


def pick_int(row: pd.Series, *aliases: str, default: int = 0) -> int:
    try:
        return int(pick_decimal(row, *aliases, default=str(default)))
    except (ValueError, TypeError):
        return default


def require_any(df: pd.DataFrame, groups: list[list[str]]) -> None:
    """Cada grupo es OR de columnas; todos los grupos deben resolverse."""
    cols = set(df.columns)
    missing_groups = []
    for group in groups:
        keys = {_norm_header(g) for g in group}
        if not keys.intersection(cols):
            missing_groups.append(" o ".join(group))
    if missing_groups:
        from .import_base import ImportValidationError

        raise ImportValidationError(
            "Faltan columnas (al menos una por grupo): " + "; ".join(missing_groups)
        )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Mapeo de columnas reales (CSV/XLSX) a nombres canónicos de importación."""
00002|
00003|from __future__ import annotations
00004|
00005|import re
00006|import unicodedata
00007|
00008|import pandas as pd
00009|
00010|from .import_base import cell_str
00011|
00012|
00013|def _norm_header(name: str) -> str:
00014|    s = unicodedata.normalize("NFKD", str(name))
00015|    s = "".join(c for c in s if not unicodedata.combining(c))
00016|    s = s.replace("\ufeff", "").strip()
00017|    # NombreCliente / Client Name → snake_case usable por aliases
00018|    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
00019|    s = s.lower()
00020|    s = re.sub(r"[^\w]+", "_", s)
00021|    return s.strip("_")
00022|
00023|
00024|def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
00025|    df = df.copy()
00026|    df.columns = [_norm_header(c) for c in df.columns]
00027|    return df
00028|
00029|
00030|def pick(row: pd.Series, *aliases: str) -> str:
00031|    """Primer alias presente en la fila (columnas ya normalizadas)."""
00032|    for alias in aliases:
00033|        key = _norm_header(alias)
00034|        if key in row.index:
00035|            val = cell_str(row.get(key))
00036|            if val:
00037|                return val
00038|    return ""
00039|
00040|
00041|def pick_decimal(row: pd.Series, *aliases: str, default: str = "0"):
00042|    from decimal import Decimal, InvalidOperation
00043|
00044|    raw = pick(row, *aliases) or default
00045|    try:
00046|        return Decimal(raw.replace(",", "").replace("Q", "").replace("$", "").strip())
00047|    except (InvalidOperation, AttributeError):
00048|        return Decimal(default)
00049|
00050|
00051|def pick_int(row: pd.Series, *aliases: str, default: int = 0) -> int:
00052|    try:
00053|        return int(pick_decimal(row, *aliases, default=str(default)))
00054|    except (ValueError, TypeError):
00055|        return default
00056|
00057|
00058|def require_any(df: pd.DataFrame, groups: list[list[str]]) -> None:
00059|    """Cada grupo es OR de columnas; todos los grupos deben resolverse."""
00060|    cols = set(df.columns)
00061|    missing_groups = []
00062|    for group in groups:
00063|        keys = {_norm_header(g) for g in group}
00064|        if not keys.intersection(cols):
00065|            missing_groups.append(" o ".join(group))
00066|    if missing_groups:
00067|        from .import_base import ImportValidationError
00068|
00069|        raise ImportValidationError(
00070|            "Faltan columnas (al menos una por grupo): " + "; ".join(missing_groups)
00071|        )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiTWFwZW8gZGUgY29sdW1uYXMgcmVhbGVzIChDU1YvWExTWCkgYSBub21icmVzIGNhbsOzbmljb3MgZGUgaW1wb3J0YWNpw7NuLiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKaW1wb3J0IHJlCmltcG9ydCB1bmljb2RlZGF0YQoKaW1wb3J0IHBhbmRhcyBhcyBwZAoKZnJvbSAuaW1wb3J0X2Jhc2UgaW1wb3J0IGNlbGxfc3RyCgoKZGVmIF9ub3JtX2hlYWRlcihuYW1lOiBzdHIpIC0+IHN0cjoKICAgIHMgPSB1bmljb2RlZGF0YS5ub3JtYWxpemUoIk5GS0QiLCBzdHIobmFtZSkpCiAgICBzID0gIiIuam9pbihjIGZvciBjIGluIHMgaWYgbm90IHVuaWNvZGVkYXRhLmNvbWJpbmluZyhjKSkKICAgIHMgPSBzLnJlcGxhY2UoIlx1ZmVmZiIsICIiKS5zdHJpcCgpCiAgICAjIE5vbWJyZUNsaWVudGUgLyBDbGllbnQgTmFtZSDihpIgc25ha2VfY2FzZSB1c2FibGUgcG9yIGFsaWFzZXMKICAgIHMgPSByZS5zdWIociIoW2EtejAtOV0pKFtBLVpdKSIsIHIiXDFfXDIiLCBzKQogICAgcyA9IHMubG93ZXIoKQogICAgcyA9IHJlLnN1YihyIlteXHddKyIsICJfIiwgcykKICAgIHJldHVybiBzLnN0cmlwKCJfIikKCgpkZWYgbm9ybWFsaXplX2NvbHVtbnMoZGY6IHBkLkRhdGFGcmFtZSkgLT4gcGQuRGF0YUZyYW1lOgogICAgZGYgPSBkZi5jb3B5KCkKICAgIGRmLmNvbHVtbnMgPSBbX25vcm1faGVhZGVyKGMpIGZvciBjIGluIGRmLmNvbHVtbnNdCiAgICByZXR1cm4gZGYKCgpkZWYgcGljayhyb3c6IHBkLlNlcmllcywgKmFsaWFzZXM6IHN0cikgLT4gc3RyOgogICAgIiIiUHJpbWVyIGFsaWFzIHByZXNlbnRlIGVuIGxhIGZpbGEgKGNvbHVtbmFzIHlhIG5vcm1hbGl6YWRhcykuIiIiCiAgICBmb3IgYWxpYXMgaW4gYWxpYXNlczoKICAgICAgICBrZXkgPSBfbm9ybV9oZWFkZXIoYWxpYXMpCiAgICAgICAgaWYga2V5IGluIHJvdy5pbmRleDoKICAgICAgICAgICAgdmFsID0gY2VsbF9zdHIocm93LmdldChrZXkpKQogICAgICAgICAgICBpZiB2YWw6CiAgICAgICAgICAgICAgICByZXR1cm4gdmFsCiAgICByZXR1cm4gIiIKCgpkZWYgcGlja19kZWNpbWFsKHJvdzogcGQuU2VyaWVzLCAqYWxpYXNlczogc3RyLCBkZWZhdWx0OiBzdHIgPSAiMCIpOgogICAgZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsLCBJbnZhbGlkT3BlcmF0aW9uCgogICAgcmF3ID0gcGljayhyb3csICphbGlhc2VzKSBvciBkZWZhdWx0CiAgICB0cnk6CiAgICAgICAgcmV0dXJuIERlY2ltYWwocmF3LnJlcGxhY2UoIiwiLCAiIikucmVwbGFjZSgiUSIsICIiKS5yZXBsYWNlKCIkIiwgIiIpLnN0cmlwKCkpCiAgICBleGNlcHQgKEludmFsaWRPcGVyYXRpb24sIEF0dHJpYnV0ZUVycm9yKToKICAgICAgICByZXR1cm4gRGVjaW1hbChkZWZhdWx0KQoKCmRlZiBwaWNrX2ludChyb3c6IHBkLlNlcmllcywgKmFsaWFzZXM6IHN0ciwgZGVmYXVsdDogaW50ID0gMCkgLT4gaW50OgogICAgdHJ5OgogICAgICAgIHJldHVybiBpbnQocGlja19kZWNpbWFsKHJvdywgKmFsaWFzZXMsIGRlZmF1bHQ9c3RyKGRlZmF1bHQpKSkKICAgIGV4Y2VwdCAoVmFsdWVFcnJvciwgVHlwZUVycm9yKToKICAgICAgICByZXR1cm4gZGVmYXVsdAoKCmRlZiByZXF1aXJlX2FueShkZjogcGQuRGF0YUZyYW1lLCBncm91cHM6IGxpc3RbbGlzdFtzdHJdXSkgLT4gTm9uZToKICAgICIiIkNhZGEgZ3J1cG8gZXMgT1IgZGUgY29sdW1uYXM7IHRvZG9zIGxvcyBncnVwb3MgZGViZW4gcmVzb2x2ZXJzZS4iIiIKICAgIGNvbHMgPSBzZXQoZGYuY29sdW1ucykKICAgIG1pc3NpbmdfZ3JvdXBzID0gW10KICAgIGZvciBncm91cCBpbiBncm91cHM6CiAgICAgICAga2V5cyA9IHtfbm9ybV9oZWFkZXIoZykgZm9yIGcgaW4gZ3JvdXB9CiAgICAgICAgaWYgbm90IGtleXMuaW50ZXJzZWN0aW9uKGNvbHMpOgogICAgICAgICAgICBtaXNzaW5nX2dyb3Vwcy5hcHBlbmQoIiBvICIuam9pbihncm91cCkpCiAgICBpZiBtaXNzaW5nX2dyb3VwczoKICAgICAgICBmcm9tIC5pbXBvcnRfYmFzZSBpbXBvcnQgSW1wb3J0VmFsaWRhdGlvbkVycm9yCgogICAgICAgIHJhaXNlIEltcG9ydFZhbGlkYXRpb25FcnJvcigKICAgICAgICAgICAgIkZhbHRhbiBjb2x1bW5hcyAoYWwgbWVub3MgdW5hIHBvciBncnVwbyk6ICIgKyAiOyAiLmpvaW4obWlzc2luZ19ncm91cHMpCiAgICAgICAgKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/services/import_base.py
PATH_JSON="core/services/import_base.py"
FILENAME=import_base.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=131
SIZE_BYTES_UTF8=4659
CONTENT_SHA256=650c5fb229f47691f59cf7e0d7c3dad5c781327ebcf1e7811057d84ebc244fbc
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
"""Utilidades base para importaciones CSV/XLSX."""

from __future__ import annotations

import io
from typing import Any, Callable

import pandas as pd
from django.core.files.uploadedfile import UploadedFile

from core.wcg_models import DataImportBatch


class ImportValidationError(Exception):
    pass


def read_dataframe(uploaded_file, sheet_name=0, all_data_sheets: bool = False) -> pd.DataFrame:
    name = (uploaded_file.name or "").lower()
    raw = uploaded_file.read()
    uploaded_file.seek(0)
    if name.endswith((".xlsx", ".xls")):
        xls = pd.ExcelFile(io.BytesIO(raw))
        if all_data_sheets or sheet_name == "__all_data__":
            frames = []
            for candidate in xls.sheet_names:
                low = candidate.lower()
                if low.startswith("soporte") or "pivot" in low or "resumen" in low:
                    continue
                part = pd.read_excel(xls, sheet_name=candidate)
                if part.empty or len(part.columns) < 3:
                    continue
                part["_hoja_origen"] = candidate
                frames.append(part)
            if not frames:
                raise ImportValidationError("No se encontraron hojas de datos en el Excel.")
            return pd.concat(frames, ignore_index=True)
        if sheet_name is None:
            sheet_name = xls.sheet_names[0]
            for candidate in xls.sheet_names:
                low = candidate.lower()
                if any(k in low for k in ("base", "leasing", "datos", "ticket")):
                    sheet_name = candidate
                    break
            return pd.read_excel(xls, sheet_name=sheet_name)
        return pd.read_excel(xls, sheet_name=sheet_name)
    if name.endswith((".csv", ".tsv", ".txt")):
        sep = "\t" if name.endswith(".tsv") else ","
        return pd.read_csv(io.BytesIO(raw), sep=sep)
    raise ImportValidationError("Formato no soportado. Use CSV o XLSX.")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    from .column_map import normalize_columns as _norm

    return _norm(df)


def read_dataframe_from_path(path) -> pd.DataFrame:
    """Lee CSV/XLSX desde ruta en disco (comandos de management)."""
    path_str = str(path).lower()
    if path_str.endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    return pd.read_csv(path)


def require_columns(df: pd.DataFrame, required: list[str]) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ImportValidationError(f"Faltan columnas: {', '.join(missing)}")


def cell_str(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def run_import_batch(
    *,
    user,
    modulo: str,
    tipo_importacion: str,
    uploaded_file: UploadedFile,
    required_columns: list[str],
    row_handler: Callable[[pd.Series, list[str]], tuple[bool, bool] | None],
) -> DataImportBatch:
    """
    row_handler recibe la fila y una lista mutable de mensajes de error por fila.
    Debe retornar (creado, actualizado) o None si hubo error en row_errors.
    """
    batch = DataImportBatch.objects.create(
        modulo=modulo,
        tipo_importacion=tipo_importacion,
        archivo_nombre=uploaded_file.name,
        uploaded_by=user,
        status=DataImportBatch.STATUS_PENDING,
    )
    logs: list[str] = []
    try:
        df = normalize_columns(read_dataframe(uploaded_file))
        require_columns(df, required_columns)
        batch.filas_leidas = len(df)
        for idx, row in df.iterrows():
            row_errors: list[str] = []
            try:
                result = row_handler(row, row_errors)
                if row_errors:
                    batch.errores += 1
                    logs.append(f"Fila {idx + 2}: {'; '.join(row_errors)}")
                elif result:
                    created, updated = result
                    if created:
                        batch.creados += 1
                    if updated:
                        batch.actualizados += 1
            except Exception as exc:
                batch.errores += 1
                logs.append(f"Fila {idx + 2}: {exc}")
        if batch.errores == 0:
            batch.status = DataImportBatch.STATUS_OK
        elif batch.creados + batch.actualizados > 0:
            batch.status = DataImportBatch.STATUS_PARTIAL
        else:
            batch.status = DataImportBatch.STATUS_ERROR
    except Exception as exc:
        batch.status = DataImportBatch.STATUS_ERROR
        logs.append(str(exc))
    batch.log_texto = "\n".join(logs)[:8000]
    batch.save()
    return batch

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Utilidades base para importaciones CSV/XLSX."""
00002|
00003|from __future__ import annotations
00004|
00005|import io
00006|from typing import Any, Callable
00007|
00008|import pandas as pd
00009|from django.core.files.uploadedfile import UploadedFile
00010|
00011|from core.wcg_models import DataImportBatch
00012|
00013|
00014|class ImportValidationError(Exception):
00015|    pass
00016|
00017|
00018|def read_dataframe(uploaded_file, sheet_name=0, all_data_sheets: bool = False) -> pd.DataFrame:
00019|    name = (uploaded_file.name or "").lower()
00020|    raw = uploaded_file.read()
00021|    uploaded_file.seek(0)
00022|    if name.endswith((".xlsx", ".xls")):
00023|        xls = pd.ExcelFile(io.BytesIO(raw))
00024|        if all_data_sheets or sheet_name == "__all_data__":
00025|            frames = []
00026|            for candidate in xls.sheet_names:
00027|                low = candidate.lower()
00028|                if low.startswith("soporte") or "pivot" in low or "resumen" in low:
00029|                    continue
00030|                part = pd.read_excel(xls, sheet_name=candidate)
00031|                if part.empty or len(part.columns) < 3:
00032|                    continue
00033|                part["_hoja_origen"] = candidate
00034|                frames.append(part)
00035|            if not frames:
00036|                raise ImportValidationError("No se encontraron hojas de datos en el Excel.")
00037|            return pd.concat(frames, ignore_index=True)
00038|        if sheet_name is None:
00039|            sheet_name = xls.sheet_names[0]
00040|            for candidate in xls.sheet_names:
00041|                low = candidate.lower()
00042|                if any(k in low for k in ("base", "leasing", "datos", "ticket")):
00043|                    sheet_name = candidate
00044|                    break
00045|            return pd.read_excel(xls, sheet_name=sheet_name)
00046|        return pd.read_excel(xls, sheet_name=sheet_name)
00047|    if name.endswith((".csv", ".tsv", ".txt")):
00048|        sep = "\t" if name.endswith(".tsv") else ","
00049|        return pd.read_csv(io.BytesIO(raw), sep=sep)
00050|    raise ImportValidationError("Formato no soportado. Use CSV o XLSX.")
00051|
00052|
00053|def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
00054|    from .column_map import normalize_columns as _norm
00055|
00056|    return _norm(df)
00057|
00058|
00059|def read_dataframe_from_path(path) -> pd.DataFrame:
00060|    """Lee CSV/XLSX desde ruta en disco (comandos de management)."""
00061|    path_str = str(path).lower()
00062|    if path_str.endswith((".xlsx", ".xls")):
00063|        return pd.read_excel(path)
00064|    return pd.read_csv(path)
00065|
00066|
00067|def require_columns(df: pd.DataFrame, required: list[str]) -> None:
00068|    missing = [c for c in required if c not in df.columns]
00069|    if missing:
00070|        raise ImportValidationError(f"Faltan columnas: {', '.join(missing)}")
00071|
00072|
00073|def cell_str(value: Any) -> str:
00074|    if value is None or (isinstance(value, float) and pd.isna(value)):
00075|        return ""
00076|    return str(value).strip()
00077|
00078|
00079|def run_import_batch(
00080|    *,
00081|    user,
00082|    modulo: str,
00083|    tipo_importacion: str,
00084|    uploaded_file: UploadedFile,
00085|    required_columns: list[str],
00086|    row_handler: Callable[[pd.Series, list[str]], tuple[bool, bool] | None],
00087|) -> DataImportBatch:
00088|    """
00089|    row_handler recibe la fila y una lista mutable de mensajes de error por fila.
00090|    Debe retornar (creado, actualizado) o None si hubo error en row_errors.
00091|    """
00092|    batch = DataImportBatch.objects.create(
00093|        modulo=modulo,
00094|        tipo_importacion=tipo_importacion,
00095|        archivo_nombre=uploaded_file.name,
00096|        uploaded_by=user,
00097|        status=DataImportBatch.STATUS_PENDING,
00098|    )
00099|    logs: list[str] = []
00100|    try:
00101|        df = normalize_columns(read_dataframe(uploaded_file))
00102|        require_columns(df, required_columns)
00103|        batch.filas_leidas = len(df)
00104|        for idx, row in df.iterrows():
00105|            row_errors: list[str] = []
00106|            try:
00107|                result = row_handler(row, row_errors)
00108|                if row_errors:
00109|                    batch.errores += 1
00110|                    logs.append(f"Fila {idx + 2}: {'; '.join(row_errors)}")
00111|                elif result:
00112|                    created, updated = result
00113|                    if created:
00114|                        batch.creados += 1
00115|                    if updated:
00116|                        batch.actualizados += 1
00117|            except Exception as exc:
00118|                batch.errores += 1
00119|                logs.append(f"Fila {idx + 2}: {exc}")
00120|        if batch.errores == 0:
00121|            batch.status = DataImportBatch.STATUS_OK
00122|        elif batch.creados + batch.actualizados > 0:
00123|            batch.status = DataImportBatch.STATUS_PARTIAL
00124|        else:
00125|            batch.status = DataImportBatch.STATUS_ERROR
00126|    except Exception as exc:
00127|        batch.status = DataImportBatch.STATUS_ERROR
00128|        logs.append(str(exc))
00129|    batch.log_texto = "\n".join(logs)[:8000]
00130|    batch.save()
00131|    return batch

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiVXRpbGlkYWRlcyBiYXNlIHBhcmEgaW1wb3J0YWNpb25lcyBDU1YvWExTWC4iIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmltcG9ydCBpbwpmcm9tIHR5cGluZyBpbXBvcnQgQW55LCBDYWxsYWJsZQoKaW1wb3J0IHBhbmRhcyBhcyBwZApmcm9tIGRqYW5nby5jb3JlLmZpbGVzLnVwbG9hZGVkZmlsZSBpbXBvcnQgVXBsb2FkZWRGaWxlCgpmcm9tIGNvcmUud2NnX21vZGVscyBpbXBvcnQgRGF0YUltcG9ydEJhdGNoCgoKY2xhc3MgSW1wb3J0VmFsaWRhdGlvbkVycm9yKEV4Y2VwdGlvbik6CiAgICBwYXNzCgoKZGVmIHJlYWRfZGF0YWZyYW1lKHVwbG9hZGVkX2ZpbGUsIHNoZWV0X25hbWU9MCwgYWxsX2RhdGFfc2hlZXRzOiBib29sID0gRmFsc2UpIC0+IHBkLkRhdGFGcmFtZToKICAgIG5hbWUgPSAodXBsb2FkZWRfZmlsZS5uYW1lIG9yICIiKS5sb3dlcigpCiAgICByYXcgPSB1cGxvYWRlZF9maWxlLnJlYWQoKQogICAgdXBsb2FkZWRfZmlsZS5zZWVrKDApCiAgICBpZiBuYW1lLmVuZHN3aXRoKCgiLnhsc3giLCAiLnhscyIpKToKICAgICAgICB4bHMgPSBwZC5FeGNlbEZpbGUoaW8uQnl0ZXNJTyhyYXcpKQogICAgICAgIGlmIGFsbF9kYXRhX3NoZWV0cyBvciBzaGVldF9uYW1lID09ICJfX2FsbF9kYXRhX18iOgogICAgICAgICAgICBmcmFtZXMgPSBbXQogICAgICAgICAgICBmb3IgY2FuZGlkYXRlIGluIHhscy5zaGVldF9uYW1lczoKICAgICAgICAgICAgICAgIGxvdyA9IGNhbmRpZGF0ZS5sb3dlcigpCiAgICAgICAgICAgICAgICBpZiBsb3cuc3RhcnRzd2l0aCgic29wb3J0ZSIpIG9yICJwaXZvdCIgaW4gbG93IG9yICJyZXN1bWVuIiBpbiBsb3c6CiAgICAgICAgICAgICAgICAgICAgY29udGludWUKICAgICAgICAgICAgICAgIHBhcnQgPSBwZC5yZWFkX2V4Y2VsKHhscywgc2hlZXRfbmFtZT1jYW5kaWRhdGUpCiAgICAgICAgICAgICAgICBpZiBwYXJ0LmVtcHR5IG9yIGxlbihwYXJ0LmNvbHVtbnMpIDwgMzoKICAgICAgICAgICAgICAgICAgICBjb250aW51ZQogICAgICAgICAgICAgICAgcGFydFsiX2hvamFfb3JpZ2VuIl0gPSBjYW5kaWRhdGUKICAgICAgICAgICAgICAgIGZyYW1lcy5hcHBlbmQocGFydCkKICAgICAgICAgICAgaWYgbm90IGZyYW1lczoKICAgICAgICAgICAgICAgIHJhaXNlIEltcG9ydFZhbGlkYXRpb25FcnJvcigiTm8gc2UgZW5jb250cmFyb24gaG9qYXMgZGUgZGF0b3MgZW4gZWwgRXhjZWwuIikKICAgICAgICAgICAgcmV0dXJuIHBkLmNvbmNhdChmcmFtZXMsIGlnbm9yZV9pbmRleD1UcnVlKQogICAgICAgIGlmIHNoZWV0X25hbWUgaXMgTm9uZToKICAgICAgICAgICAgc2hlZXRfbmFtZSA9IHhscy5zaGVldF9uYW1lc1swXQogICAgICAgICAgICBmb3IgY2FuZGlkYXRlIGluIHhscy5zaGVldF9uYW1lczoKICAgICAgICAgICAgICAgIGxvdyA9IGNhbmRpZGF0ZS5sb3dlcigpCiAgICAgICAgICAgICAgICBpZiBhbnkoayBpbiBsb3cgZm9yIGsgaW4gKCJiYXNlIiwgImxlYXNpbmciLCAiZGF0b3MiLCAidGlja2V0IikpOgogICAgICAgICAgICAgICAgICAgIHNoZWV0X25hbWUgPSBjYW5kaWRhdGUKICAgICAgICAgICAgICAgICAgICBicmVhawogICAgICAgICAgICByZXR1cm4gcGQucmVhZF9leGNlbCh4bHMsIHNoZWV0X25hbWU9c2hlZXRfbmFtZSkKICAgICAgICByZXR1cm4gcGQucmVhZF9leGNlbCh4bHMsIHNoZWV0X25hbWU9c2hlZXRfbmFtZSkKICAgIGlmIG5hbWUuZW5kc3dpdGgoKCIuY3N2IiwgIi50c3YiLCAiLnR4dCIpKToKICAgICAgICBzZXAgPSAiXHQiIGlmIG5hbWUuZW5kc3dpdGgoIi50c3YiKSBlbHNlICIsIgogICAgICAgIHJldHVybiBwZC5yZWFkX2Nzdihpby5CeXRlc0lPKHJhdyksIHNlcD1zZXApCiAgICByYWlzZSBJbXBvcnRWYWxpZGF0aW9uRXJyb3IoIkZvcm1hdG8gbm8gc29wb3J0YWRvLiBVc2UgQ1NWIG8gWExTWC4iKQoKCmRlZiBub3JtYWxpemVfY29sdW1ucyhkZjogcGQuRGF0YUZyYW1lKSAtPiBwZC5EYXRhRnJhbWU6CiAgICBmcm9tIC5jb2x1bW5fbWFwIGltcG9ydCBub3JtYWxpemVfY29sdW1ucyBhcyBfbm9ybQoKICAgIHJldHVybiBfbm9ybShkZikKCgpkZWYgcmVhZF9kYXRhZnJhbWVfZnJvbV9wYXRoKHBhdGgpIC0+IHBkLkRhdGFGcmFtZToKICAgICIiIkxlZSBDU1YvWExTWCBkZXNkZSBydXRhIGVuIGRpc2NvIChjb21hbmRvcyBkZSBtYW5hZ2VtZW50KS4iIiIKICAgIHBhdGhfc3RyID0gc3RyKHBhdGgpLmxvd2VyKCkKICAgIGlmIHBhdGhfc3RyLmVuZHN3aXRoKCgiLnhsc3giLCAiLnhscyIpKToKICAgICAgICByZXR1cm4gcGQucmVhZF9leGNlbChwYXRoKQogICAgcmV0dXJuIHBkLnJlYWRfY3N2KHBhdGgpCgoKZGVmIHJlcXVpcmVfY29sdW1ucyhkZjogcGQuRGF0YUZyYW1lLCByZXF1aXJlZDogbGlzdFtzdHJdKSAtPiBOb25lOgogICAgbWlzc2luZyA9IFtjIGZvciBjIGluIHJlcXVpcmVkIGlmIGMgbm90IGluIGRmLmNvbHVtbnNdCiAgICBpZiBtaXNzaW5nOgogICAgICAgIHJhaXNlIEltcG9ydFZhbGlkYXRpb25FcnJvcihmIkZhbHRhbiBjb2x1bW5hczogeycsICcuam9pbihtaXNzaW5nKX0iKQoKCmRlZiBjZWxsX3N0cih2YWx1ZTogQW55KSAtPiBzdHI6CiAgICBpZiB2YWx1ZSBpcyBOb25lIG9yIChpc2luc3RhbmNlKHZhbHVlLCBmbG9hdCkgYW5kIHBkLmlzbmEodmFsdWUpKToKICAgICAgICByZXR1cm4gIiIKICAgIHJldHVybiBzdHIodmFsdWUpLnN0cmlwKCkKCgpkZWYgcnVuX2ltcG9ydF9iYXRjaCgKICAgICosCiAgICB1c2VyLAogICAgbW9kdWxvOiBzdHIsCiAgICB0aXBvX2ltcG9ydGFjaW9uOiBzdHIsCiAgICB1cGxvYWRlZF9maWxlOiBVcGxvYWRlZEZpbGUsCiAgICByZXF1aXJlZF9jb2x1bW5zOiBsaXN0W3N0cl0sCiAgICByb3dfaGFuZGxlcjogQ2FsbGFibGVbW3BkLlNlcmllcywgbGlzdFtzdHJdXSwgdHVwbGVbYm9vbCwgYm9vbF0gfCBOb25lXSwKKSAtPiBEYXRhSW1wb3J0QmF0Y2g6CiAgICAiIiIKICAgIHJvd19oYW5kbGVyIHJlY2liZSBsYSBmaWxhIHkgdW5hIGxpc3RhIG11dGFibGUgZGUgbWVuc2FqZXMgZGUgZXJyb3IgcG9yIGZpbGEuCiAgICBEZWJlIHJldG9ybmFyIChjcmVhZG8sIGFjdHVhbGl6YWRvKSBvIE5vbmUgc2kgaHVibyBlcnJvciBlbiByb3dfZXJyb3JzLgogICAgIiIiCiAgICBiYXRjaCA9IERhdGFJbXBvcnRCYXRjaC5vYmplY3RzLmNyZWF0ZSgKICAgICAgICBtb2R1bG89bW9kdWxvLAogICAgICAgIHRpcG9faW1wb3J0YWNpb249dGlwb19pbXBvcnRhY2lvbiwKICAgICAgICBhcmNoaXZvX25vbWJyZT11cGxvYWRlZF9maWxlLm5hbWUsCiAgICAgICAgdXBsb2FkZWRfYnk9dXNlciwKICAgICAgICBzdGF0dXM9RGF0YUltcG9ydEJhdGNoLlNUQVRVU19QRU5ESU5HLAogICAgKQogICAgbG9nczogbGlzdFtzdHJdID0gW10KICAgIHRyeToKICAgICAgICBkZiA9IG5vcm1hbGl6ZV9jb2x1bW5zKHJlYWRfZGF0YWZyYW1lKHVwbG9hZGVkX2ZpbGUpKQogICAgICAgIHJlcXVpcmVfY29sdW1ucyhkZiwgcmVxdWlyZWRfY29sdW1ucykKICAgICAgICBiYXRjaC5maWxhc19sZWlkYXMgPSBsZW4oZGYpCiAgICAgICAgZm9yIGlkeCwgcm93IGluIGRmLml0ZXJyb3dzKCk6CiAgICAgICAgICAgIHJvd19lcnJvcnM6IGxpc3Rbc3RyXSA9IFtdCiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIHJlc3VsdCA9IHJvd19oYW5kbGVyKHJvdywgcm93X2Vycm9ycykKICAgICAgICAgICAgICAgIGlmIHJvd19lcnJvcnM6CiAgICAgICAgICAgICAgICAgICAgYmF0Y2guZXJyb3JlcyArPSAxCiAgICAgICAgICAgICAgICAgICAgbG9ncy5hcHBlbmQoZiJGaWxhIHtpZHggKyAyfTogeyc7ICcuam9pbihyb3dfZXJyb3JzKX0iKQogICAgICAgICAgICAgICAgZWxpZiByZXN1bHQ6CiAgICAgICAgICAgICAgICAgICAgY3JlYXRlZCwgdXBkYXRlZCA9IHJlc3VsdAogICAgICAgICAgICAgICAgICAgIGlmIGNyZWF0ZWQ6CiAgICAgICAgICAgICAgICAgICAgICAgIGJhdGNoLmNyZWFkb3MgKz0gMQogICAgICAgICAgICAgICAgICAgIGlmIHVwZGF0ZWQ6CiAgICAgICAgICAgICAgICAgICAgICAgIGJhdGNoLmFjdHVhbGl6YWRvcyArPSAxCiAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZXhjOgogICAgICAgICAgICAgICAgYmF0Y2guZXJyb3JlcyArPSAxCiAgICAgICAgICAgICAgICBsb2dzLmFwcGVuZChmIkZpbGEge2lkeCArIDJ9OiB7ZXhjfSIpCiAgICAgICAgaWYgYmF0Y2guZXJyb3JlcyA9PSAwOgogICAgICAgICAgICBiYXRjaC5zdGF0dXMgPSBEYXRhSW1wb3J0QmF0Y2guU1RBVFVTX09LCiAgICAgICAgZWxpZiBiYXRjaC5jcmVhZG9zICsgYmF0Y2guYWN0dWFsaXphZG9zID4gMDoKICAgICAgICAgICAgYmF0Y2guc3RhdHVzID0gRGF0YUltcG9ydEJhdGNoLlNUQVRVU19QQVJUSUFMCiAgICAgICAgZWxzZToKICAgICAgICAgICAgYmF0Y2guc3RhdHVzID0gRGF0YUltcG9ydEJhdGNoLlNUQVRVU19FUlJPUgogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBleGM6CiAgICAgICAgYmF0Y2guc3RhdHVzID0gRGF0YUltcG9ydEJhdGNoLlNUQVRVU19FUlJPUgogICAgICAgIGxvZ3MuYXBwZW5kKHN0cihleGMpKQogICAgYmF0Y2gubG9nX3RleHRvID0gIlxuIi5qb2luKGxvZ3MpWzo4MDAwXQogICAgYmF0Y2guc2F2ZSgpCiAgICByZXR1cm4gYmF0Y2gK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/services/une_resolve.py
PATH_JSON="core/services/une_resolve.py"
FILENAME=une_resolve.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=52
SIZE_BYTES_UTF8=1422
CONTENT_SHA256=754f434079ba0a01f221b24e9b53806f892f514ab62afc8f00ff8160729926c8
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
"""Resolución de UNE a partir de texto crudo de importaciones."""

from __future__ import annotations


def _mentions_investment(raw_lower: str) -> bool:
    return (
        "investment" in raw_lower
        or "investments" in raw_lower
        or "invest" in raw_lower
        or "inversiones" in raw_lower
        or "inversion" in raw_lower
        or "inversión" in raw_lower
    )


def resolve_une_from_text(raw_value, aliases: dict, unes_by_code: dict):
    """
    Regla de negocio: si el valor crudo menciona Investment/Inversiones,
    SIEMPRE es UNE Inversiones — aunque también diga Factoring/Leasing
    y aunque exista un alias incorrecto.
    """
    if not raw_value:
        return None

    raw_clean = str(raw_value).strip()
    if not raw_clean:
        return None

    raw_upper = raw_clean.upper()
    raw_lower = raw_clean.lower()

    if _mentions_investment(raw_lower):
        return unes_by_code.get("INVESTMENT")

    if raw_upper in aliases:
        return aliases[raw_upper]

    if "factoring" in raw_lower or "factoraje" in raw_lower or "factor" in raw_lower:
        return unes_by_code.get("FACTORING")

    if "leasing" in raw_lower:
        return unes_by_code.get("LEASING")

    if (
        "insurance" in raw_lower
        or "seguros" in raw_lower
        or "seguro" in raw_lower
    ):
        return unes_by_code.get("INSURANCE")

    return unes_by_code.get(raw_upper)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Resolución de UNE a partir de texto crudo de importaciones."""
00002|
00003|from __future__ import annotations
00004|
00005|
00006|def _mentions_investment(raw_lower: str) -> bool:
00007|    return (
00008|        "investment" in raw_lower
00009|        or "investments" in raw_lower
00010|        or "invest" in raw_lower
00011|        or "inversiones" in raw_lower
00012|        or "inversion" in raw_lower
00013|        or "inversión" in raw_lower
00014|    )
00015|
00016|
00017|def resolve_une_from_text(raw_value, aliases: dict, unes_by_code: dict):
00018|    """
00019|    Regla de negocio: si el valor crudo menciona Investment/Inversiones,
00020|    SIEMPRE es UNE Inversiones — aunque también diga Factoring/Leasing
00021|    y aunque exista un alias incorrecto.
00022|    """
00023|    if not raw_value:
00024|        return None
00025|
00026|    raw_clean = str(raw_value).strip()
00027|    if not raw_clean:
00028|        return None
00029|
00030|    raw_upper = raw_clean.upper()
00031|    raw_lower = raw_clean.lower()
00032|
00033|    if _mentions_investment(raw_lower):
00034|        return unes_by_code.get("INVESTMENT")
00035|
00036|    if raw_upper in aliases:
00037|        return aliases[raw_upper]
00038|
00039|    if "factoring" in raw_lower or "factoraje" in raw_lower or "factor" in raw_lower:
00040|        return unes_by_code.get("FACTORING")
00041|
00042|    if "leasing" in raw_lower:
00043|        return unes_by_code.get("LEASING")
00044|
00045|    if (
00046|        "insurance" in raw_lower
00047|        or "seguros" in raw_lower
00048|        or "seguro" in raw_lower
00049|    ):
00050|        return unes_by_code.get("INSURANCE")
00051|
00052|    return unes_by_code.get(raw_upper)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiUmVzb2x1Y2nDs24gZGUgVU5FIGEgcGFydGlyIGRlIHRleHRvIGNydWRvIGRlIGltcG9ydGFjaW9uZXMuIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgoKZGVmIF9tZW50aW9uc19pbnZlc3RtZW50KHJhd19sb3dlcjogc3RyKSAtPiBib29sOgogICAgcmV0dXJuICgKICAgICAgICAiaW52ZXN0bWVudCIgaW4gcmF3X2xvd2VyCiAgICAgICAgb3IgImludmVzdG1lbnRzIiBpbiByYXdfbG93ZXIKICAgICAgICBvciAiaW52ZXN0IiBpbiByYXdfbG93ZXIKICAgICAgICBvciAiaW52ZXJzaW9uZXMiIGluIHJhd19sb3dlcgogICAgICAgIG9yICJpbnZlcnNpb24iIGluIHJhd19sb3dlcgogICAgICAgIG9yICJpbnZlcnNpw7NuIiBpbiByYXdfbG93ZXIKICAgICkKCgpkZWYgcmVzb2x2ZV91bmVfZnJvbV90ZXh0KHJhd192YWx1ZSwgYWxpYXNlczogZGljdCwgdW5lc19ieV9jb2RlOiBkaWN0KToKICAgICIiIgogICAgUmVnbGEgZGUgbmVnb2Npbzogc2kgZWwgdmFsb3IgY3J1ZG8gbWVuY2lvbmEgSW52ZXN0bWVudC9JbnZlcnNpb25lcywKICAgIFNJRU1QUkUgZXMgVU5FIEludmVyc2lvbmVzIOKAlCBhdW5xdWUgdGFtYmnDqW4gZGlnYSBGYWN0b3JpbmcvTGVhc2luZwogICAgeSBhdW5xdWUgZXhpc3RhIHVuIGFsaWFzIGluY29ycmVjdG8uCiAgICAiIiIKICAgIGlmIG5vdCByYXdfdmFsdWU6CiAgICAgICAgcmV0dXJuIE5vbmUKCiAgICByYXdfY2xlYW4gPSBzdHIocmF3X3ZhbHVlKS5zdHJpcCgpCiAgICBpZiBub3QgcmF3X2NsZWFuOgogICAgICAgIHJldHVybiBOb25lCgogICAgcmF3X3VwcGVyID0gcmF3X2NsZWFuLnVwcGVyKCkKICAgIHJhd19sb3dlciA9IHJhd19jbGVhbi5sb3dlcigpCgogICAgaWYgX21lbnRpb25zX2ludmVzdG1lbnQocmF3X2xvd2VyKToKICAgICAgICByZXR1cm4gdW5lc19ieV9jb2RlLmdldCgiSU5WRVNUTUVOVCIpCgogICAgaWYgcmF3X3VwcGVyIGluIGFsaWFzZXM6CiAgICAgICAgcmV0dXJuIGFsaWFzZXNbcmF3X3VwcGVyXQoKICAgIGlmICJmYWN0b3JpbmciIGluIHJhd19sb3dlciBvciAiZmFjdG9yYWplIiBpbiByYXdfbG93ZXIgb3IgImZhY3RvciIgaW4gcmF3X2xvd2VyOgogICAgICAgIHJldHVybiB1bmVzX2J5X2NvZGUuZ2V0KCJGQUNUT1JJTkciKQoKICAgIGlmICJsZWFzaW5nIiBpbiByYXdfbG93ZXI6CiAgICAgICAgcmV0dXJuIHVuZXNfYnlfY29kZS5nZXQoIkxFQVNJTkciKQoKICAgIGlmICgKICAgICAgICAiaW5zdXJhbmNlIiBpbiByYXdfbG93ZXIKICAgICAgICBvciAic2VndXJvcyIgaW4gcmF3X2xvd2VyCiAgICAgICAgb3IgInNlZ3VybyIgaW4gcmF3X2xvd2VyCiAgICApOgogICAgICAgIHJldHVybiB1bmVzX2J5X2NvZGUuZ2V0KCJJTlNVUkFOQ0UiKQoKICAgIHJldHVybiB1bmVzX2J5X2NvZGUuZ2V0KHJhd191cHBlcikK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/tests.py
PATH_JSON="core/tests.py"
FILENAME=tests.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=3
SIZE_BYTES_UTF8=60
CONTENT_SHA256=9ab6c6191360e63c1b4c9b5659aef348a743c9e078be68190917369e4e9563e8
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
from django.test import TestCase

# Create your tests here.

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.test import TestCase
00002|
00003|# Create your tests here.

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udGVzdCBpbXBvcnQgVGVzdENhc2UKCiMgQ3JlYXRlIHlvdXIgdGVzdHMgaGVyZS4K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/views.py
PATH_JSON="core/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=3
SIZE_BYTES_UTF8=63
CONTENT_SHA256=c5cd48407aec8a3ee3df74d46e8fbfa1ec32defb34de9c3f7ada4159a318265d
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
from django.shortcuts import render

# Create your views here.

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.shortcuts import render
00002|
00003|# Create your views here.

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uc2hvcnRjdXRzIGltcG9ydCByZW5kZXIKCiMgQ3JlYXRlIHlvdXIgdmlld3MgaGVyZS4K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/wcg_models.py
PATH_JSON="core/wcg_models.py"
FILENAME=wcg_models.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=210
SIZE_BYTES_UTF8=6750
CONTENT_SHA256=499a99771c97c4f88f644c97b76a2519c139b5e808fa966a0d28be3aa10160ef
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

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Maestro común WCG One — compartido por CRM, Risk, PGO y PGC."""
00002|
00003|from django.conf import settings
00004|from django.db import models
00005|
00006|from .models import TimeStampedModel, UNE
00007|
00008|
00009|class UnidadNegocio(TimeStampedModel):
00010|    """
00011|    Unidad de negocio WCG.
00012|    Clave natural importación: `code` (ej. LEASING, FACTORING).
00013|    """
00014|
00015|    code = models.CharField(max_length=30, unique=True)
00016|    nombre = models.CharField(max_length=120)
00017|    une_pgc = models.ForeignKey(
00018|        UNE,
00019|        on_delete=models.SET_NULL,
00020|        null=True,
00021|        blank=True,
00022|        related_name="unidades_negocio_wcg",
00023|        help_text="Vínculo opcional con UNE existente del PGC.",
00024|    )
00025|    activa = models.BooleanField(default=True)
00026|
00027|    class Meta:
00028|        ordering = ["nombre"]
00029|        verbose_name = "Unidad de negocio"
00030|        verbose_name_plural = "Unidades de negocio"
00031|
00032|    def __str__(self):
00033|        return self.nombre
00034|
00035|
00036|class Entidad(TimeStampedModel):
00037|    """
00038|    Maestro de clientes/prospectos WCG.
00039|    Clave natural importación: `codigo` (preferido) o `nit` si no hay código explícito.
00040|    """
00041|    TIPO_CLIENTE = "CLIENTE"
00042|    TIPO_PROSPECTO = "PROSPECTO"
00043|    TIPO_OTRO = "OTRO"
00044|    TIPO_CHOICES = [
00045|        (TIPO_CLIENTE, "Cliente"),
00046|        (TIPO_PROSPECTO, "Prospecto"),
00047|        (TIPO_OTRO, "Otro"),
00048|    ]
00049|
00050|    codigo = models.CharField(max_length=50, unique=True)
00051|    nombre = models.CharField(max_length=255)
00052|    nit = models.CharField(max_length=30, blank=True, db_index=True)
00053|    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_CLIENTE)
00054|    unidad_negocio = models.ForeignKey(
00055|        UnidadNegocio,
00056|        on_delete=models.SET_NULL,
00057|        null=True,
00058|        blank=True,
00059|        related_name="entidades",
00060|    )
00061|    activa = models.BooleanField(default=True)
00062|    notas = models.TextField(blank=True)
00063|
00064|    class Meta:
00065|        ordering = ["nombre"]
00066|        verbose_name = "Entidad"
00067|        verbose_name_plural = "Entidades"
00068|
00069|    def __str__(self):
00070|        return f"{self.codigo} — {self.nombre}"
00071|
00072|
00073|class Contacto(TimeStampedModel):
00074|    """
00075|    Contacto comercial de una entidad.
00076|    Clave natural importación: (`entidad`, `email`) si hay email; si no (`entidad`, `nombre`).
00077|    """
00078|    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="contactos")
00079|    nombre = models.CharField(max_length=120)
00080|    email = models.EmailField(blank=True)
00081|    telefono = models.CharField(max_length=40, blank=True)
00082|    cargo = models.CharField(max_length=120, blank=True)
00083|    es_principal = models.BooleanField(default=False)
00084|    activo = models.BooleanField(default=True)
00085|
00086|    class Meta:
00087|        ordering = ["entidad__nombre", "nombre"]
00088|        verbose_name = "Contacto"
00089|        verbose_name_plural = "Contactos"
00090|
00091|    def __str__(self):
00092|        return f"{self.nombre} ({self.entidad.codigo})"
00093|
00094|
00095|class Producto(TimeStampedModel):
00096|    """Catálogo de productos. Clave natural: `codigo`."""
00097|
00098|    codigo = models.CharField(max_length=50, unique=True)
00099|    nombre = models.CharField(max_length=200)
00100|    unidad_negocio = models.ForeignKey(
00101|        UnidadNegocio,
00102|        on_delete=models.SET_NULL,
00103|        null=True,
00104|        blank=True,
00105|        related_name="productos",
00106|    )
00107|    activo = models.BooleanField(default=True)
00108|    descripcion = models.TextField(blank=True)
00109|
00110|    class Meta:
00111|        ordering = ["nombre"]
00112|        verbose_name = "Producto"
00113|        verbose_name_plural = "Productos"
00114|
00115|    def __str__(self):
00116|        return self.nombre
00117|
00118|
00119|class RelacionEntidadProducto(TimeStampedModel):
00120|    """Vínculo entidad-producto. Clave natural: (`entidad`, `producto`)."""
00121|
00122|    ESTADO_ACTIVO = "ACTIVO"
00123|    ESTADO_INACTIVO = "INACTIVO"
00124|    ESTADO_CHOICES = [
00125|        (ESTADO_ACTIVO, "Activo"),
00126|        (ESTADO_INACTIVO, "Inactivo"),
00127|    ]
00128|
00129|    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="productos_relacionados")
00130|    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="entidades_relacionadas")
00131|    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_ACTIVO)
00132|    fecha_inicio = models.DateField(null=True, blank=True)
00133|    notas = models.TextField(blank=True)
00134|
00135|    class Meta:
00136|        unique_together = ("entidad", "producto")
00137|        ordering = ["entidad__nombre", "producto__nombre"]
00138|        verbose_name = "Relación entidad-producto"
00139|        verbose_name_plural = "Relaciones entidad-producto"
00140|
00141|    def __str__(self):
00142|        return f"{self.entidad.codigo} / {self.producto.codigo}"
00143|
00144|
00145|class DataDictionary(TimeStampedModel):
00146|    modulo = models.CharField(max_length=30, db_index=True)
00147|    tabla = models.CharField(max_length=80)
00148|    campo = models.CharField(max_length=80)
00149|    etiqueta = models.CharField(max_length=120)
00150|    tipo_dato = models.CharField(max_length=40, blank=True)
00151|    obligatorio = models.BooleanField(default=False)
00152|    descripcion = models.TextField(blank=True)
00153|
00154|    class Meta:
00155|        unique_together = ("modulo", "tabla", "campo")
00156|        ordering = ["modulo", "tabla", "campo"]
00157|        verbose_name = "Diccionario de datos"
00158|        verbose_name_plural = "Diccionario de datos"
00159|
00160|    def __str__(self):
00161|        return f"{self.modulo}.{self.tabla}.{self.campo}"
00162|
00163|
00164|class DataImportBatch(TimeStampedModel):
00165|    MODULO_CRM = "CRM"
00166|    MODULO_RISK = "RISK"
00167|    MODULO_PGO = "PGO"
00168|    MODULO_PGC = "PGC"
00169|    MODULO_CHOICES = [
00170|        (MODULO_CRM, "CRM"),
00171|        (MODULO_RISK, "Risk"),
00172|        (MODULO_PGO, "PGO"),
00173|        (MODULO_PGC, "PGC"),
00174|    ]
00175|
00176|    STATUS_PENDING = "PENDING"
00177|    STATUS_OK = "OK"
00178|    STATUS_PARTIAL = "PARTIAL"
00179|    STATUS_ERROR = "ERROR"
00180|    STATUS_CHOICES = [
00181|        (STATUS_PENDING, "Pendiente"),
00182|        (STATUS_OK, "OK"),
00183|        (STATUS_PARTIAL, "Parcial"),
00184|        (STATUS_ERROR, "Error"),
00185|    ]
00186|
00187|    modulo = models.CharField(max_length=20, choices=MODULO_CHOICES)
00188|    tipo_importacion = models.CharField(max_length=80)
00189|    archivo_nombre = models.CharField(max_length=255)
00190|    uploaded_by = models.ForeignKey(
00191|        settings.AUTH_USER_MODEL,
00192|        on_delete=models.SET_NULL,
00193|        null=True,
00194|        blank=True,
00195|        related_name="import_batches",
00196|    )
00197|    filas_leidas = models.PositiveIntegerField(default=0)
00198|    creados = models.PositiveIntegerField(default=0)
00199|    actualizados = models.PositiveIntegerField(default=0)
00200|    errores = models.PositiveIntegerField(default=0)
00201|    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
00202|    log_texto = models.TextField(blank=True)
00203|
00204|    class Meta:
00205|        ordering = ["-created_at"]
00206|        verbose_name = "Lote de importación"
00207|        verbose_name_plural = "Lotes de importación"
00208|
00209|    def __str__(self):
00210|        return f"{self.modulo}/{self.tipo_importacion} — {self.archivo_nombre}"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiTWFlc3RybyBjb23Dum4gV0NHIE9uZSDigJQgY29tcGFydGlkbyBwb3IgQ1JNLCBSaXNrLCBQR08geSBQR0MuIiIiCgpmcm9tIGRqYW5nby5jb25mIGltcG9ydCBzZXR0aW5ncwpmcm9tIGRqYW5nby5kYiBpbXBvcnQgbW9kZWxzCgpmcm9tIC5tb2RlbHMgaW1wb3J0IFRpbWVTdGFtcGVkTW9kZWwsIFVORQoKCmNsYXNzIFVuaWRhZE5lZ29jaW8oVGltZVN0YW1wZWRNb2RlbCk6CiAgICAiIiIKICAgIFVuaWRhZCBkZSBuZWdvY2lvIFdDRy4KICAgIENsYXZlIG5hdHVyYWwgaW1wb3J0YWNpw7NuOiBgY29kZWAgKGVqLiBMRUFTSU5HLCBGQUNUT1JJTkcpLgogICAgIiIiCgogICAgY29kZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0zMCwgdW5pcXVlPVRydWUpCiAgICBub21icmUgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTIwKQogICAgdW5lX3BnYyA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIFVORSwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0idW5pZGFkZXNfbmVnb2Npb193Y2ciLAogICAgICAgIGhlbHBfdGV4dD0iVsOtbmN1bG8gb3BjaW9uYWwgY29uIFVORSBleGlzdGVudGUgZGVsIFBHQy4iLAogICAgKQogICAgYWN0aXZhID0gbW9kZWxzLkJvb2xlYW5GaWVsZChkZWZhdWx0PVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICBvcmRlcmluZyA9IFsibm9tYnJlIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiVW5pZGFkIGRlIG5lZ29jaW8iCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJVbmlkYWRlcyBkZSBuZWdvY2lvIgoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBzZWxmLm5vbWJyZQoKCmNsYXNzIEVudGlkYWQoVGltZVN0YW1wZWRNb2RlbCk6CiAgICAiIiIKICAgIE1hZXN0cm8gZGUgY2xpZW50ZXMvcHJvc3BlY3RvcyBXQ0cuCiAgICBDbGF2ZSBuYXR1cmFsIGltcG9ydGFjacOzbjogYGNvZGlnb2AgKHByZWZlcmlkbykgbyBgbml0YCBzaSBubyBoYXkgY8OzZGlnbyBleHBsw61jaXRvLgogICAgIiIiCiAgICBUSVBPX0NMSUVOVEUgPSAiQ0xJRU5URSIKICAgIFRJUE9fUFJPU1BFQ1RPID0gIlBST1NQRUNUTyIKICAgIFRJUE9fT1RSTyA9ICJPVFJPIgogICAgVElQT19DSE9JQ0VTID0gWwogICAgICAgIChUSVBPX0NMSUVOVEUsICJDbGllbnRlIiksCiAgICAgICAgKFRJUE9fUFJPU1BFQ1RPLCAiUHJvc3BlY3RvIiksCiAgICAgICAgKFRJUE9fT1RSTywgIk90cm8iKSwKICAgIF0KCiAgICBjb2RpZ28gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9NTAsIHVuaXF1ZT1UcnVlKQogICAgbm9tYnJlID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTI1NSkKICAgIG5pdCA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0zMCwgYmxhbms9VHJ1ZSwgZGJfaW5kZXg9VHJ1ZSkKICAgIHRpcG8gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MjAsIGNob2ljZXM9VElQT19DSE9JQ0VTLCBkZWZhdWx0PVRJUE9fQ0xJRU5URSkKICAgIHVuaWRhZF9uZWdvY2lvID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgVW5pZGFkTmVnb2NpbywKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0iZW50aWRhZGVzIiwKICAgICkKICAgIGFjdGl2YSA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1UcnVlKQogICAgbm90YXMgPSBtb2RlbHMuVGV4dEZpZWxkKGJsYW5rPVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICBvcmRlcmluZyA9IFsibm9tYnJlIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiRW50aWRhZCIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIkVudGlkYWRlcyIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi5jb2RpZ299IOKAlCB7c2VsZi5ub21icmV9IgoKCmNsYXNzIENvbnRhY3RvKFRpbWVTdGFtcGVkTW9kZWwpOgogICAgIiIiCiAgICBDb250YWN0byBjb21lcmNpYWwgZGUgdW5hIGVudGlkYWQuCiAgICBDbGF2ZSBuYXR1cmFsIGltcG9ydGFjacOzbjogKGBlbnRpZGFkYCwgYGVtYWlsYCkgc2kgaGF5IGVtYWlsOyBzaSBubyAoYGVudGlkYWRgLCBgbm9tYnJlYCkuCiAgICAiIiIKICAgIGVudGlkYWQgPSBtb2RlbHMuRm9yZWlnbktleShFbnRpZGFkLCBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsIHJlbGF0ZWRfbmFtZT0iY29udGFjdG9zIikKICAgIG5vbWJyZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMjApCiAgICBlbWFpbCA9IG1vZGVscy5FbWFpbEZpZWxkKGJsYW5rPVRydWUpCiAgICB0ZWxlZm9ubyA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD00MCwgYmxhbms9VHJ1ZSkKICAgIGNhcmdvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEyMCwgYmxhbms9VHJ1ZSkKICAgIGVzX3ByaW5jaXBhbCA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1GYWxzZSkKICAgIGFjdGl2byA9IG1vZGVscy5Cb29sZWFuRmllbGQoZGVmYXVsdD1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbImVudGlkYWRfX25vbWJyZSIsICJub21icmUiXQogICAgICAgIHZlcmJvc2VfbmFtZSA9ICJDb250YWN0byIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIkNvbnRhY3RvcyIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi5ub21icmV9ICh7c2VsZi5lbnRpZGFkLmNvZGlnb30pIgoKCmNsYXNzIFByb2R1Y3RvKFRpbWVTdGFtcGVkTW9kZWwpOgogICAgIiIiQ2F0w6Fsb2dvIGRlIHByb2R1Y3Rvcy4gQ2xhdmUgbmF0dXJhbDogYGNvZGlnb2AuIiIiCgogICAgY29kaWdvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTUwLCB1bmlxdWU9VHJ1ZSkKICAgIG5vbWJyZSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yMDApCiAgICB1bmlkYWRfbmVnb2NpbyA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIFVuaWRhZE5lZ29jaW8sCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5TRVRfTlVMTCwKICAgICAgICBudWxsPVRydWUsCiAgICAgICAgYmxhbms9VHJ1ZSwKICAgICAgICByZWxhdGVkX25hbWU9InByb2R1Y3RvcyIsCiAgICApCiAgICBhY3Rpdm8gPSBtb2RlbHMuQm9vbGVhbkZpZWxkKGRlZmF1bHQ9VHJ1ZSkKICAgIGRlc2NyaXBjaW9uID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbIm5vbWJyZSJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIlByb2R1Y3RvIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiUHJvZHVjdG9zIgoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBzZWxmLm5vbWJyZQoKCmNsYXNzIFJlbGFjaW9uRW50aWRhZFByb2R1Y3RvKFRpbWVTdGFtcGVkTW9kZWwpOgogICAgIiIiVsOtbmN1bG8gZW50aWRhZC1wcm9kdWN0by4gQ2xhdmUgbmF0dXJhbDogKGBlbnRpZGFkYCwgYHByb2R1Y3RvYCkuIiIiCgogICAgRVNUQURPX0FDVElWTyA9ICJBQ1RJVk8iCiAgICBFU1RBRE9fSU5BQ1RJVk8gPSAiSU5BQ1RJVk8iCiAgICBFU1RBRE9fQ0hPSUNFUyA9IFsKICAgICAgICAoRVNUQURPX0FDVElWTywgIkFjdGl2byIpLAogICAgICAgIChFU1RBRE9fSU5BQ1RJVk8sICJJbmFjdGl2byIpLAogICAgXQoKICAgIGVudGlkYWQgPSBtb2RlbHMuRm9yZWlnbktleShFbnRpZGFkLCBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsIHJlbGF0ZWRfbmFtZT0icHJvZHVjdG9zX3JlbGFjaW9uYWRvcyIpCiAgICBwcm9kdWN0byA9IG1vZGVscy5Gb3JlaWduS2V5KFByb2R1Y3RvLCBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsIHJlbGF0ZWRfbmFtZT0iZW50aWRhZGVzX3JlbGFjaW9uYWRhcyIpCiAgICBlc3RhZG8gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MjAsIGNob2ljZXM9RVNUQURPX0NIT0lDRVMsIGRlZmF1bHQ9RVNUQURPX0FDVElWTykKICAgIGZlY2hhX2luaWNpbyA9IG1vZGVscy5EYXRlRmllbGQobnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgbm90YXMgPSBtb2RlbHMuVGV4dEZpZWxkKGJsYW5rPVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICB1bmlxdWVfdG9nZXRoZXIgPSAoImVudGlkYWQiLCAicHJvZHVjdG8iKQogICAgICAgIG9yZGVyaW5nID0gWyJlbnRpZGFkX19ub21icmUiLCAicHJvZHVjdG9fX25vbWJyZSJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIlJlbGFjacOzbiBlbnRpZGFkLXByb2R1Y3RvIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiUmVsYWNpb25lcyBlbnRpZGFkLXByb2R1Y3RvIgoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLmVudGlkYWQuY29kaWdvfSAvIHtzZWxmLnByb2R1Y3RvLmNvZGlnb30iCgoKY2xhc3MgRGF0YURpY3Rpb25hcnkoVGltZVN0YW1wZWRNb2RlbCk6CiAgICBtb2R1bG8gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MzAsIGRiX2luZGV4PVRydWUpCiAgICB0YWJsYSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD04MCkKICAgIGNhbXBvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTgwKQogICAgZXRpcXVldGEgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTIwKQogICAgdGlwb19kYXRvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTQwLCBibGFuaz1UcnVlKQogICAgb2JsaWdhdG9yaW8gPSBtb2RlbHMuQm9vbGVhbkZpZWxkKGRlZmF1bHQ9RmFsc2UpCiAgICBkZXNjcmlwY2lvbiA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIHVuaXF1ZV90b2dldGhlciA9ICgibW9kdWxvIiwgInRhYmxhIiwgImNhbXBvIikKICAgICAgICBvcmRlcmluZyA9IFsibW9kdWxvIiwgInRhYmxhIiwgImNhbXBvIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiRGljY2lvbmFyaW8gZGUgZGF0b3MiCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJEaWNjaW9uYXJpbyBkZSBkYXRvcyIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi5tb2R1bG99LntzZWxmLnRhYmxhfS57c2VsZi5jYW1wb30iCgoKY2xhc3MgRGF0YUltcG9ydEJhdGNoKFRpbWVTdGFtcGVkTW9kZWwpOgogICAgTU9EVUxPX0NSTSA9ICJDUk0iCiAgICBNT0RVTE9fUklTSyA9ICJSSVNLIgogICAgTU9EVUxPX1BHTyA9ICJQR08iCiAgICBNT0RVTE9fUEdDID0gIlBHQyIKICAgIE1PRFVMT19DSE9JQ0VTID0gWwogICAgICAgIChNT0RVTE9fQ1JNLCAiQ1JNIiksCiAgICAgICAgKE1PRFVMT19SSVNLLCAiUmlzayIpLAogICAgICAgIChNT0RVTE9fUEdPLCAiUEdPIiksCiAgICAgICAgKE1PRFVMT19QR0MsICJQR0MiKSwKICAgIF0KCiAgICBTVEFUVVNfUEVORElORyA9ICJQRU5ESU5HIgogICAgU1RBVFVTX09LID0gIk9LIgogICAgU1RBVFVTX1BBUlRJQUwgPSAiUEFSVElBTCIKICAgIFNUQVRVU19FUlJPUiA9ICJFUlJPUiIKICAgIFNUQVRVU19DSE9JQ0VTID0gWwogICAgICAgIChTVEFUVVNfUEVORElORywgIlBlbmRpZW50ZSIpLAogICAgICAgIChTVEFUVVNfT0ssICJPSyIpLAogICAgICAgIChTVEFUVVNfUEFSVElBTCwgIlBhcmNpYWwiKSwKICAgICAgICAoU1RBVFVTX0VSUk9SLCAiRXJyb3IiKSwKICAgIF0KCiAgICBtb2R1bG8gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MjAsIGNob2ljZXM9TU9EVUxPX0NIT0lDRVMpCiAgICB0aXBvX2ltcG9ydGFjaW9uID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTgwKQogICAgYXJjaGl2b19ub21icmUgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MjU1KQogICAgdXBsb2FkZWRfYnkgPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICBzZXR0aW5ncy5BVVRIX1VTRVJfTU9ERUwsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5TRVRfTlVMTCwKICAgICAgICBudWxsPVRydWUsCiAgICAgICAgYmxhbms9VHJ1ZSwKICAgICAgICByZWxhdGVkX25hbWU9ImltcG9ydF9iYXRjaGVzIiwKICAgICkKICAgIGZpbGFzX2xlaWRhcyA9IG1vZGVscy5Qb3NpdGl2ZUludGVnZXJGaWVsZChkZWZhdWx0PTApCiAgICBjcmVhZG9zID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKGRlZmF1bHQ9MCkKICAgIGFjdHVhbGl6YWRvcyA9IG1vZGVscy5Qb3NpdGl2ZUludGVnZXJGaWVsZChkZWZhdWx0PTApCiAgICBlcnJvcmVzID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKGRlZmF1bHQ9MCkKICAgIHN0YXR1cyA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yMCwgY2hvaWNlcz1TVEFUVVNfQ0hPSUNFUywgZGVmYXVsdD1TVEFUVVNfUEVORElORykKICAgIGxvZ190ZXh0byA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIG9yZGVyaW5nID0gWyItY3JlYXRlZF9hdCJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIkxvdGUgZGUgaW1wb3J0YWNpw7NuIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiTG90ZXMgZGUgaW1wb3J0YWNpw7NuIgoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLm1vZHVsb30ve3NlbGYudGlwb19pbXBvcnRhY2lvbn0g4oCUIHtzZWxmLmFyY2hpdm9fbm9tYnJlfSIK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/wcg_paths.py
PATH_JSON="core/wcg_paths.py"
FILENAME=wcg_paths.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=27
SIZE_BYTES_UTF8=890
CONTENT_SHA256=7f0c3b8c7250320be0f43b78ffefd98f7fc7e36821b370e9e5453de6d41cf672
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
"""Rutas estándar de archivos de datos WCG (fuera del código de negocio)."""

from pathlib import Path

from django.conf import settings

# Directorios donde se buscan archivos reales (en orden).
WCG_DATA_DIRS = [
    settings.BASE_DIR / "data" / "wcg",
    settings.BASE_DIR.parent / "data" / "wcg",
]

CRM_INFO_CLIENTES = "crm datos - InfoClientesWCG para CRM.csv"
RISK_LEASING_DB = (
    "balon datos - Ejemplo de datos Riesgo al 31-mayo para una operacion - Base de datos Leasing.xlsx"
)
PGO_ARCHIVOS = "pgo datos - Archivos para PGO.csv"
PGO_TICKETS_CONTROL = "pgo datos - control de tickets marzo abril y mayo 2026 para PGO.xlsx"
PGO_ANALISIS_TI = "pgo ejemplo del analisis - PGO - TI Q22026.xlsx"


def resolve_data_file(filename: str) -> Path | None:
    for base in WCG_DATA_DIRS:
        path = base / filename
        if path.is_file():
            return path
    return None

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Rutas estándar de archivos de datos WCG (fuera del código de negocio)."""
00002|
00003|from pathlib import Path
00004|
00005|from django.conf import settings
00006|
00007|# Directorios donde se buscan archivos reales (en orden).
00008|WCG_DATA_DIRS = [
00009|    settings.BASE_DIR / "data" / "wcg",
00010|    settings.BASE_DIR.parent / "data" / "wcg",
00011|]
00012|
00013|CRM_INFO_CLIENTES = "crm datos - InfoClientesWCG para CRM.csv"
00014|RISK_LEASING_DB = (
00015|    "balon datos - Ejemplo de datos Riesgo al 31-mayo para una operacion - Base de datos Leasing.xlsx"
00016|)
00017|PGO_ARCHIVOS = "pgo datos - Archivos para PGO.csv"
00018|PGO_TICKETS_CONTROL = "pgo datos - control de tickets marzo abril y mayo 2026 para PGO.xlsx"
00019|PGO_ANALISIS_TI = "pgo ejemplo del analisis - PGO - TI Q22026.xlsx"
00020|
00021|
00022|def resolve_data_file(filename: str) -> Path | None:
00023|    for base in WCG_DATA_DIRS:
00024|        path = base / filename
00025|        if path.is_file():
00026|            return path
00027|    return None

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiUnV0YXMgZXN0w6FuZGFyIGRlIGFyY2hpdm9zIGRlIGRhdG9zIFdDRyAoZnVlcmEgZGVsIGPDs2RpZ28gZGUgbmVnb2NpbykuIiIiCgpmcm9tIHBhdGhsaWIgaW1wb3J0IFBhdGgKCmZyb20gZGphbmdvLmNvbmYgaW1wb3J0IHNldHRpbmdzCgojIERpcmVjdG9yaW9zIGRvbmRlIHNlIGJ1c2NhbiBhcmNoaXZvcyByZWFsZXMgKGVuIG9yZGVuKS4KV0NHX0RBVEFfRElSUyA9IFsKICAgIHNldHRpbmdzLkJBU0VfRElSIC8gImRhdGEiIC8gIndjZyIsCiAgICBzZXR0aW5ncy5CQVNFX0RJUi5wYXJlbnQgLyAiZGF0YSIgLyAid2NnIiwKXQoKQ1JNX0lORk9fQ0xJRU5URVMgPSAiY3JtIGRhdG9zIC0gSW5mb0NsaWVudGVzV0NHIHBhcmEgQ1JNLmNzdiIKUklTS19MRUFTSU5HX0RCID0gKAogICAgImJhbG9uIGRhdG9zIC0gRWplbXBsbyBkZSBkYXRvcyBSaWVzZ28gYWwgMzEtbWF5byBwYXJhIHVuYSBvcGVyYWNpb24gLSBCYXNlIGRlIGRhdG9zIExlYXNpbmcueGxzeCIKKQpQR09fQVJDSElWT1MgPSAicGdvIGRhdG9zIC0gQXJjaGl2b3MgcGFyYSBQR08uY3N2IgpQR09fVElDS0VUU19DT05UUk9MID0gInBnbyBkYXRvcyAtIGNvbnRyb2wgZGUgdGlja2V0cyBtYXJ6byBhYnJpbCB5IG1heW8gMjAyNiBwYXJhIFBHTy54bHN4IgpQR09fQU5BTElTSVNfVEkgPSAicGdvIGVqZW1wbG8gZGVsIGFuYWxpc2lzIC0gUEdPIC0gVEkgUTIyMDI2Lnhsc3giCgoKZGVmIHJlc29sdmVfZGF0YV9maWxlKGZpbGVuYW1lOiBzdHIpIC0+IFBhdGggfCBOb25lOgogICAgZm9yIGJhc2UgaW4gV0NHX0RBVEFfRElSUzoKICAgICAgICBwYXRoID0gYmFzZSAvIGZpbGVuYW1lCiAgICAgICAgaWYgcGF0aC5pc19maWxlKCk6CiAgICAgICAgICAgIHJldHVybiBwYXRoCiAgICByZXR1cm4gTm9uZQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=crm/__init__.py
PATH_JSON="crm/__init__.py"
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
PATH_LITERAL=crm/admin.py
PATH_JSON="crm/admin.py"
FILENAME=admin.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=19
SIZE_BYTES_UTF8=690
CONTENT_SHA256=aeb2b388dbc1d94d4b8f0d0cb7312cd525c503e2f5203f21744598956b4316e8
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
from django.contrib import admin

from .models import Interaccion, Tarea


@admin.register(Interaccion)
class InteraccionAdmin(admin.ModelAdmin):
    list_display = ("fecha", "entidad", "tipo", "asunto", "usuario")
    list_filter = ("tipo", "fecha")
    search_fields = ("asunto", "descripcion", "entidad__codigo", "entidad__nombre")
    ordering = ("-fecha",)


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "entidad", "estado", "fecha_vencimiento", "asignado_a")
    list_filter = ("estado", "fecha_vencimiento")
    search_fields = ("titulo", "descripcion", "entidad__codigo", "entidad__nombre")
    ordering = ("estado", "fecha_vencimiento")

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib import admin
00002|
00003|from .models import Interaccion, Tarea
00004|
00005|
00006|@admin.register(Interaccion)
00007|class InteraccionAdmin(admin.ModelAdmin):
00008|    list_display = ("fecha", "entidad", "tipo", "asunto", "usuario")
00009|    list_filter = ("tipo", "fecha")
00010|    search_fields = ("asunto", "descripcion", "entidad__codigo", "entidad__nombre")
00011|    ordering = ("-fecha",)
00012|
00013|
00014|@admin.register(Tarea)
00015|class TareaAdmin(admin.ModelAdmin):
00016|    list_display = ("titulo", "entidad", "estado", "fecha_vencimiento", "asignado_a")
00017|    list_filter = ("estado", "fecha_vencimiento")
00018|    search_fields = ("titulo", "descripcion", "entidad__codigo", "entidad__nombre")
00019|    ordering = ("estado", "fecha_vencimiento")

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgYWRtaW4KCmZyb20gLm1vZGVscyBpbXBvcnQgSW50ZXJhY2Npb24sIFRhcmVhCgoKQGFkbWluLnJlZ2lzdGVyKEludGVyYWNjaW9uKQpjbGFzcyBJbnRlcmFjY2lvbkFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKCJmZWNoYSIsICJlbnRpZGFkIiwgInRpcG8iLCAiYXN1bnRvIiwgInVzdWFyaW8iKQogICAgbGlzdF9maWx0ZXIgPSAoInRpcG8iLCAiZmVjaGEiKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgiYXN1bnRvIiwgImRlc2NyaXBjaW9uIiwgImVudGlkYWRfX2NvZGlnbyIsICJlbnRpZGFkX19ub21icmUiKQogICAgb3JkZXJpbmcgPSAoIi1mZWNoYSIsKQoKCkBhZG1pbi5yZWdpc3RlcihUYXJlYSkKY2xhc3MgVGFyZWFBZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgidGl0dWxvIiwgImVudGlkYWQiLCAiZXN0YWRvIiwgImZlY2hhX3ZlbmNpbWllbnRvIiwgImFzaWduYWRvX2EiKQogICAgbGlzdF9maWx0ZXIgPSAoImVzdGFkbyIsICJmZWNoYV92ZW5jaW1pZW50byIpCiAgICBzZWFyY2hfZmllbGRzID0gKCJ0aXR1bG8iLCAiZGVzY3JpcGNpb24iLCAiZW50aWRhZF9fY29kaWdvIiwgImVudGlkYWRfX25vbWJyZSIpCiAgICBvcmRlcmluZyA9ICgiZXN0YWRvIiwgImZlY2hhX3ZlbmNpbWllbnRvIikK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=crm/apps.py
PATH_JSON="crm/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=6
SIZE_BYTES_UTF8=138
CONTENT_SHA256=16e6c4014a7ad127f8d67de9c08041aabc879ebeb37cc78a239574dff98d2543
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
from django.apps import AppConfig


class CrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crm'

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class CrmConfig(AppConfig):
00005|    default_auto_field = 'django.db.models.BigAutoField'
00006|    name = 'crm'

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgQ3JtQ29uZmlnKEFwcENvbmZpZyk6CiAgICBkZWZhdWx0X2F1dG9fZmllbGQgPSAnZGphbmdvLmRiLm1vZGVscy5CaWdBdXRvRmllbGQnCiAgICBuYW1lID0gJ2NybScK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=crm/forms.py
PATH_JSON="crm/forms.py"
FILENAME=forms.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=27
SIZE_BYTES_UTF8=801
CONTENT_SHA256=65d3456518aac73fbdfb25bf7a0d4f807d220d8cf851a24895cedd5896357bc4
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
from django import forms

from .models import Interaccion, Tarea


class InteraccionForm(forms.ModelForm):
    class Meta:
        model = Interaccion
        fields = ["tipo", "asunto", "descripcion", "fecha"]
        widgets = {
            "fecha": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "descripcion": forms.Textarea(attrs={"rows": 4}),
        }


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ["titulo", "descripcion", "fecha_vencimiento", "estado", "asignado_a"]
        widgets = {
            "fecha_vencimiento": forms.DateInput(attrs={"type": "date"}),
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }


class ImportFileForm(forms.Form):
    archivo = forms.FileField(label="Archivo CSV o XLSX")

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django import forms
00002|
00003|from .models import Interaccion, Tarea
00004|
00005|
00006|class InteraccionForm(forms.ModelForm):
00007|    class Meta:
00008|        model = Interaccion
00009|        fields = ["tipo", "asunto", "descripcion", "fecha"]
00010|        widgets = {
00011|            "fecha": forms.DateTimeInput(attrs={"type": "datetime-local"}),
00012|            "descripcion": forms.Textarea(attrs={"rows": 4}),
00013|        }
00014|
00015|
00016|class TareaForm(forms.ModelForm):
00017|    class Meta:
00018|        model = Tarea
00019|        fields = ["titulo", "descripcion", "fecha_vencimiento", "estado", "asignado_a"]
00020|        widgets = {
00021|            "fecha_vencimiento": forms.DateInput(attrs={"type": "date"}),
00022|            "descripcion": forms.Textarea(attrs={"rows": 3}),
00023|        }
00024|
00025|
00026|class ImportFileForm(forms.Form):
00027|    archivo = forms.FileField(label="Archivo CSV o XLSX")

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28gaW1wb3J0IGZvcm1zCgpmcm9tIC5tb2RlbHMgaW1wb3J0IEludGVyYWNjaW9uLCBUYXJlYQoKCmNsYXNzIEludGVyYWNjaW9uRm9ybShmb3Jtcy5Nb2RlbEZvcm0pOgogICAgY2xhc3MgTWV0YToKICAgICAgICBtb2RlbCA9IEludGVyYWNjaW9uCiAgICAgICAgZmllbGRzID0gWyJ0aXBvIiwgImFzdW50byIsICJkZXNjcmlwY2lvbiIsICJmZWNoYSJdCiAgICAgICAgd2lkZ2V0cyA9IHsKICAgICAgICAgICAgImZlY2hhIjogZm9ybXMuRGF0ZVRpbWVJbnB1dChhdHRycz17InR5cGUiOiAiZGF0ZXRpbWUtbG9jYWwifSksCiAgICAgICAgICAgICJkZXNjcmlwY2lvbiI6IGZvcm1zLlRleHRhcmVhKGF0dHJzPXsicm93cyI6IDR9KSwKICAgICAgICB9CgoKY2xhc3MgVGFyZWFGb3JtKGZvcm1zLk1vZGVsRm9ybSk6CiAgICBjbGFzcyBNZXRhOgogICAgICAgIG1vZGVsID0gVGFyZWEKICAgICAgICBmaWVsZHMgPSBbInRpdHVsbyIsICJkZXNjcmlwY2lvbiIsICJmZWNoYV92ZW5jaW1pZW50byIsICJlc3RhZG8iLCAiYXNpZ25hZG9fYSJdCiAgICAgICAgd2lkZ2V0cyA9IHsKICAgICAgICAgICAgImZlY2hhX3ZlbmNpbWllbnRvIjogZm9ybXMuRGF0ZUlucHV0KGF0dHJzPXsidHlwZSI6ICJkYXRlIn0pLAogICAgICAgICAgICAiZGVzY3JpcGNpb24iOiBmb3Jtcy5UZXh0YXJlYShhdHRycz17InJvd3MiOiAzfSksCiAgICAgICAgfQoKCmNsYXNzIEltcG9ydEZpbGVGb3JtKGZvcm1zLkZvcm0pOgogICAgYXJjaGl2byA9IGZvcm1zLkZpbGVGaWVsZChsYWJlbD0iQXJjaGl2byBDU1YgbyBYTFNYIikK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=crm/models.py
PATH_JSON="crm/models.py"
FILENAME=models.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=75
SIZE_BYTES_UTF8=2416
CONTENT_SHA256=825354bd0f7c515578cd56166416adec353a68095892323a39d34bf3a70ea930
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

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.conf import settings
00002|from django.db import models
00003|
00004|from core.models import TimeStampedModel
00005|from core.wcg_models import Entidad
00006|
00007|
00008|class Interaccion(TimeStampedModel):
00009|    """Registro CRM. Clave: id autoincremental; vinculada a Entidad."""
00010|    TIPO_LLAMADA = "LLAMADA"
00011|    TIPO_REUNION = "REUNION"
00012|    TIPO_EMAIL = "EMAIL"
00013|    TIPO_OTRO = "OTRO"
00014|    TIPO_CHOICES = [
00015|        (TIPO_LLAMADA, "Llamada"),
00016|        (TIPO_REUNION, "Reunión"),
00017|        (TIPO_EMAIL, "Email"),
00018|        (TIPO_OTRO, "Otro"),
00019|    ]
00020|
00021|    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="interacciones")
00022|    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_LLAMADA)
00023|    asunto = models.CharField(max_length=200)
00024|    descripcion = models.TextField(blank=True)
00025|    fecha = models.DateTimeField()
00026|    usuario = models.ForeignKey(
00027|        settings.AUTH_USER_MODEL,
00028|        on_delete=models.SET_NULL,
00029|        null=True,
00030|        blank=True,
00031|        related_name="crm_interacciones",
00032|    )
00033|
00034|    class Meta:
00035|        ordering = ["-fecha"]
00036|        verbose_name = "Interacción"
00037|        verbose_name_plural = "Interacciones"
00038|
00039|    def __str__(self):
00040|        return f"{self.entidad.codigo} — {self.asunto}"
00041|
00042|
00043|class Tarea(TimeStampedModel):
00044|    """Tarea CRM. Clave: id autoincremental; vinculada a Entidad."""
00045|    ESTADO_PENDIENTE = "PENDIENTE"
00046|    ESTADO_EN_PROCESO = "EN_PROCESO"
00047|    ESTADO_HECHA = "HECHA"
00048|    ESTADO_CANCELADA = "CANCELADA"
00049|    ESTADO_CHOICES = [
00050|        (ESTADO_PENDIENTE, "Pendiente"),
00051|        (ESTADO_EN_PROCESO, "En proceso"),
00052|        (ESTADO_HECHA, "Hecha"),
00053|        (ESTADO_CANCELADA, "Cancelada"),
00054|    ]
00055|
00056|    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="tareas")
00057|    titulo = models.CharField(max_length=200)
00058|    descripcion = models.TextField(blank=True)
00059|    fecha_vencimiento = models.DateField(null=True, blank=True)
00060|    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)
00061|    asignado_a = models.ForeignKey(
00062|        settings.AUTH_USER_MODEL,
00063|        on_delete=models.SET_NULL,
00064|        null=True,
00065|        blank=True,
00066|        related_name="crm_tareas",
00067|    )
00068|
00069|    class Meta:
00070|        ordering = ["estado", "fecha_vencimiento", "-created_at"]
00071|        verbose_name = "Tarea"
00072|        verbose_name_plural = "Tareas"
00073|
00074|    def __str__(self):
00075|        return f"{self.entidad.codigo} — {self.titulo}"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29uZiBpbXBvcnQgc2V0dGluZ3MKZnJvbSBkamFuZ28uZGIgaW1wb3J0IG1vZGVscwoKZnJvbSBjb3JlLm1vZGVscyBpbXBvcnQgVGltZVN0YW1wZWRNb2RlbApmcm9tIGNvcmUud2NnX21vZGVscyBpbXBvcnQgRW50aWRhZAoKCmNsYXNzIEludGVyYWNjaW9uKFRpbWVTdGFtcGVkTW9kZWwpOgogICAgIiIiUmVnaXN0cm8gQ1JNLiBDbGF2ZTogaWQgYXV0b2luY3JlbWVudGFsOyB2aW5jdWxhZGEgYSBFbnRpZGFkLiIiIgogICAgVElQT19MTEFNQURBID0gIkxMQU1BREEiCiAgICBUSVBPX1JFVU5JT04gPSAiUkVVTklPTiIKICAgIFRJUE9fRU1BSUwgPSAiRU1BSUwiCiAgICBUSVBPX09UUk8gPSAiT1RSTyIKICAgIFRJUE9fQ0hPSUNFUyA9IFsKICAgICAgICAoVElQT19MTEFNQURBLCAiTGxhbWFkYSIpLAogICAgICAgIChUSVBPX1JFVU5JT04sICJSZXVuacOzbiIpLAogICAgICAgIChUSVBPX0VNQUlMLCAiRW1haWwiKSwKICAgICAgICAoVElQT19PVFJPLCAiT3RybyIpLAogICAgXQoKICAgIGVudGlkYWQgPSBtb2RlbHMuRm9yZWlnbktleShFbnRpZGFkLCBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsIHJlbGF0ZWRfbmFtZT0iaW50ZXJhY2Npb25lcyIpCiAgICB0aXBvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTIwLCBjaG9pY2VzPVRJUE9fQ0hPSUNFUywgZGVmYXVsdD1USVBPX0xMQU1BREEpCiAgICBhc3VudG8gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MjAwKQogICAgZGVzY3JpcGNpb24gPSBtb2RlbHMuVGV4dEZpZWxkKGJsYW5rPVRydWUpCiAgICBmZWNoYSA9IG1vZGVscy5EYXRlVGltZUZpZWxkKCkKICAgIHVzdWFyaW8gPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICBzZXR0aW5ncy5BVVRIX1VTRVJfTU9ERUwsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5TRVRfTlVMTCwKICAgICAgICBudWxsPVRydWUsCiAgICAgICAgYmxhbms9VHJ1ZSwKICAgICAgICByZWxhdGVkX25hbWU9ImNybV9pbnRlcmFjY2lvbmVzIiwKICAgICkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIG9yZGVyaW5nID0gWyItZmVjaGEiXQogICAgICAgIHZlcmJvc2VfbmFtZSA9ICJJbnRlcmFjY2nDs24iCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJJbnRlcmFjY2lvbmVzIgoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLmVudGlkYWQuY29kaWdvfSDigJQge3NlbGYuYXN1bnRvfSIKCgpjbGFzcyBUYXJlYShUaW1lU3RhbXBlZE1vZGVsKToKICAgICIiIlRhcmVhIENSTS4gQ2xhdmU6IGlkIGF1dG9pbmNyZW1lbnRhbDsgdmluY3VsYWRhIGEgRW50aWRhZC4iIiIKICAgIEVTVEFET19QRU5ESUVOVEUgPSAiUEVORElFTlRFIgogICAgRVNUQURPX0VOX1BST0NFU08gPSAiRU5fUFJPQ0VTTyIKICAgIEVTVEFET19IRUNIQSA9ICJIRUNIQSIKICAgIEVTVEFET19DQU5DRUxBREEgPSAiQ0FOQ0VMQURBIgogICAgRVNUQURPX0NIT0lDRVMgPSBbCiAgICAgICAgKEVTVEFET19QRU5ESUVOVEUsICJQZW5kaWVudGUiKSwKICAgICAgICAoRVNUQURPX0VOX1BST0NFU08sICJFbiBwcm9jZXNvIiksCiAgICAgICAgKEVTVEFET19IRUNIQSwgIkhlY2hhIiksCiAgICAgICAgKEVTVEFET19DQU5DRUxBREEsICJDYW5jZWxhZGEiKSwKICAgIF0KCiAgICBlbnRpZGFkID0gbW9kZWxzLkZvcmVpZ25LZXkoRW50aWRhZCwgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLCByZWxhdGVkX25hbWU9InRhcmVhcyIpCiAgICB0aXR1bG8gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MjAwKQogICAgZGVzY3JpcGNpb24gPSBtb2RlbHMuVGV4dEZpZWxkKGJsYW5rPVRydWUpCiAgICBmZWNoYV92ZW5jaW1pZW50byA9IG1vZGVscy5EYXRlRmllbGQobnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgZXN0YWRvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTIwLCBjaG9pY2VzPUVTVEFET19DSE9JQ0VTLCBkZWZhdWx0PUVTVEFET19QRU5ESUVOVEUpCiAgICBhc2lnbmFkb19hID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgc2V0dGluZ3MuQVVUSF9VU0VSX01PREVMLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJjcm1fdGFyZWFzIiwKICAgICkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIG9yZGVyaW5nID0gWyJlc3RhZG8iLCAiZmVjaGFfdmVuY2ltaWVudG8iLCAiLWNyZWF0ZWRfYXQiXQogICAgICAgIHZlcmJvc2VfbmFtZSA9ICJUYXJlYSIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIlRhcmVhcyIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi5lbnRpZGFkLmNvZGlnb30g4oCUIHtzZWxmLnRpdHVsb30iCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=crm/selectors.py
PATH_JSON="crm/selectors.py"
FILENAME=selectors.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=51
SIZE_BYTES_UTF8=1611
CONTENT_SHA256=a7b4991d44084bdd52f0da3920ad31d4ff70f8c991c261212abab79ad0f74bf0
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
"""Consultas reutilizables CRM (modelos productivos)."""

from __future__ import annotations

from django.db.models import Count, Q

from core.wcg_models import Entidad


def entidad_list_queryset(request):
    qs = Entidad.objects.select_related("unidad_negocio").annotate(
        num_contactos=Count("contactos", distinct=True),
        num_productos=Count("productos_relacionados", distinct=True),
    ).order_by("nombre")
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q) | Q(nit__icontains=q) | Q(codigo__icontains=q)
        )
    tipo = request.GET.get("tipo", "").strip()
    if tipo:
        qs = qs.filter(tipo=tipo)
    unidad = request.GET.get("unidad", "").strip()
    if unidad:
        qs = qs.filter(unidad_negocio_id=unidad)
    activo = request.GET.get("activo", "").strip()
    if activo == "1":
        qs = qs.filter(activa=True)
    elif activo == "0":
        qs = qs.filter(activa=False)
    return qs


def entidad_summary(queryset=None):
    base = queryset if queryset is not None else Entidad.objects.all()
    por_unidad = list(
        base.filter(unidad_negocio__isnull=False)
        .values("unidad_negocio__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )
    por_tipo = list(
        base.values("tipo").annotate(total=Count("id")).order_by("-total")
    )
    return {
        "total": base.count(),
        "activas": base.filter(activa=True).count(),
        "inactivas": base.filter(activa=False).count(),
        "por_unidad": por_unidad,
        "por_tipo": por_tipo,
    }

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Consultas reutilizables CRM (modelos productivos)."""
00002|
00003|from __future__ import annotations
00004|
00005|from django.db.models import Count, Q
00006|
00007|from core.wcg_models import Entidad
00008|
00009|
00010|def entidad_list_queryset(request):
00011|    qs = Entidad.objects.select_related("unidad_negocio").annotate(
00012|        num_contactos=Count("contactos", distinct=True),
00013|        num_productos=Count("productos_relacionados", distinct=True),
00014|    ).order_by("nombre")
00015|    q = request.GET.get("q", "").strip()
00016|    if q:
00017|        qs = qs.filter(
00018|            Q(nombre__icontains=q) | Q(nit__icontains=q) | Q(codigo__icontains=q)
00019|        )
00020|    tipo = request.GET.get("tipo", "").strip()
00021|    if tipo:
00022|        qs = qs.filter(tipo=tipo)
00023|    unidad = request.GET.get("unidad", "").strip()
00024|    if unidad:
00025|        qs = qs.filter(unidad_negocio_id=unidad)
00026|    activo = request.GET.get("activo", "").strip()
00027|    if activo == "1":
00028|        qs = qs.filter(activa=True)
00029|    elif activo == "0":
00030|        qs = qs.filter(activa=False)
00031|    return qs
00032|
00033|
00034|def entidad_summary(queryset=None):
00035|    base = queryset if queryset is not None else Entidad.objects.all()
00036|    por_unidad = list(
00037|        base.filter(unidad_negocio__isnull=False)
00038|        .values("unidad_negocio__nombre")
00039|        .annotate(total=Count("id"))
00040|        .order_by("-total")[:5]
00041|    )
00042|    por_tipo = list(
00043|        base.values("tipo").annotate(total=Count("id")).order_by("-total")
00044|    )
00045|    return {
00046|        "total": base.count(),
00047|        "activas": base.filter(activa=True).count(),
00048|        "inactivas": base.filter(activa=False).count(),
00049|        "por_unidad": por_unidad,
00050|        "por_tipo": por_tipo,
00051|    }

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiQ29uc3VsdGFzIHJldXRpbGl6YWJsZXMgQ1JNIChtb2RlbG9zIHByb2R1Y3Rpdm9zKS4iIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmZyb20gZGphbmdvLmRiLm1vZGVscyBpbXBvcnQgQ291bnQsIFEKCmZyb20gY29yZS53Y2dfbW9kZWxzIGltcG9ydCBFbnRpZGFkCgoKZGVmIGVudGlkYWRfbGlzdF9xdWVyeXNldChyZXF1ZXN0KToKICAgIHFzID0gRW50aWRhZC5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJ1bmlkYWRfbmVnb2NpbyIpLmFubm90YXRlKAogICAgICAgIG51bV9jb250YWN0b3M9Q291bnQoImNvbnRhY3RvcyIsIGRpc3RpbmN0PVRydWUpLAogICAgICAgIG51bV9wcm9kdWN0b3M9Q291bnQoInByb2R1Y3Rvc19yZWxhY2lvbmFkb3MiLCBkaXN0aW5jdD1UcnVlKSwKICAgICkub3JkZXJfYnkoIm5vbWJyZSIpCiAgICBxID0gcmVxdWVzdC5HRVQuZ2V0KCJxIiwgIiIpLnN0cmlwKCkKICAgIGlmIHE6CiAgICAgICAgcXMgPSBxcy5maWx0ZXIoCiAgICAgICAgICAgIFEobm9tYnJlX19pY29udGFpbnM9cSkgfCBRKG5pdF9faWNvbnRhaW5zPXEpIHwgUShjb2RpZ29fX2ljb250YWlucz1xKQogICAgICAgICkKICAgIHRpcG8gPSByZXF1ZXN0LkdFVC5nZXQoInRpcG8iLCAiIikuc3RyaXAoKQogICAgaWYgdGlwbzoKICAgICAgICBxcyA9IHFzLmZpbHRlcih0aXBvPXRpcG8pCiAgICB1bmlkYWQgPSByZXF1ZXN0LkdFVC5nZXQoInVuaWRhZCIsICIiKS5zdHJpcCgpCiAgICBpZiB1bmlkYWQ6CiAgICAgICAgcXMgPSBxcy5maWx0ZXIodW5pZGFkX25lZ29jaW9faWQ9dW5pZGFkKQogICAgYWN0aXZvID0gcmVxdWVzdC5HRVQuZ2V0KCJhY3Rpdm8iLCAiIikuc3RyaXAoKQogICAgaWYgYWN0aXZvID09ICIxIjoKICAgICAgICBxcyA9IHFzLmZpbHRlcihhY3RpdmE9VHJ1ZSkKICAgIGVsaWYgYWN0aXZvID09ICIwIjoKICAgICAgICBxcyA9IHFzLmZpbHRlcihhY3RpdmE9RmFsc2UpCiAgICByZXR1cm4gcXMKCgpkZWYgZW50aWRhZF9zdW1tYXJ5KHF1ZXJ5c2V0PU5vbmUpOgogICAgYmFzZSA9IHF1ZXJ5c2V0IGlmIHF1ZXJ5c2V0IGlzIG5vdCBOb25lIGVsc2UgRW50aWRhZC5vYmplY3RzLmFsbCgpCiAgICBwb3JfdW5pZGFkID0gbGlzdCgKICAgICAgICBiYXNlLmZpbHRlcih1bmlkYWRfbmVnb2Npb19faXNudWxsPUZhbHNlKQogICAgICAgIC52YWx1ZXMoInVuaWRhZF9uZWdvY2lvX19ub21icmUiKQogICAgICAgIC5hbm5vdGF0ZSh0b3RhbD1Db3VudCgiaWQiKSkKICAgICAgICAub3JkZXJfYnkoIi10b3RhbCIpWzo1XQogICAgKQogICAgcG9yX3RpcG8gPSBsaXN0KAogICAgICAgIGJhc2UudmFsdWVzKCJ0aXBvIikuYW5ub3RhdGUodG90YWw9Q291bnQoImlkIikpLm9yZGVyX2J5KCItdG90YWwiKQogICAgKQogICAgcmV0dXJuIHsKICAgICAgICAidG90YWwiOiBiYXNlLmNvdW50KCksCiAgICAgICAgImFjdGl2YXMiOiBiYXNlLmZpbHRlcihhY3RpdmE9VHJ1ZSkuY291bnQoKSwKICAgICAgICAiaW5hY3RpdmFzIjogYmFzZS5maWx0ZXIoYWN0aXZhPUZhbHNlKS5jb3VudCgpLAogICAgICAgICJwb3JfdW5pZGFkIjogcG9yX3VuaWRhZCwKICAgICAgICAicG9yX3RpcG8iOiBwb3JfdGlwbywKICAgIH0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=crm/services.py
PATH_JSON="crm/services.py"
FILENAME=services.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=270
SIZE_BYTES_UTF8=9994
CONTENT_SHA256=e582c9251de153fed000e3a5c8ea1c41e54254d710def5defc5f56483382e6c9
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
Importadores CRM ajustados a archivos reales WCG.

Archivo referencia: `crm datos - InfoClientesWCG para CRM.csv`
Columnas: NIT, NombreCliente, Teléfono, Correo, WCF, WCL, WCI

Clave natural Entidad: `codigo` (NIT normalizado)
Clave natural Contacto: (`entidad`, `email`) o (`entidad`, `nombre`)
"""

from __future__ import annotations

import re

import pandas as pd

from core.services.column_map import normalize_columns, pick, require_any
from core.services.import_base import cell_str, run_import_batch
from core.wcg_models import Contacto, DataImportBatch, Entidad, Producto, RelacionEntidadProducto, UnidadNegocio


def _slug_codigo(value: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "", value.upper())[:50]
    return s or "SINCODIGO"


def _resolve_unidad(code_or_name: str) -> UnidadNegocio | None:
    if not code_or_name:
        return None
    raw = code_or_name.strip()
    raw_upper = raw.upper()
    raw_lower = raw.lower()

    if any(
        token in raw_lower
        for token in ("investment", "investments", "invest", "inversiones", "inversion", "inversión")
    ):
        code = "INVESTMENT"
    else:
        mapping = {
            "FACTORAJE": "FACTORING",
            "FACTORING": "FACTORING",
            "LEASING": "LEASING",
            "INSURANCE": "INSURANCE",
            "INVESTMENT": "INVESTMENT",
            "WCF": "FACTORING",
            "WCL": "LEASING",
            "WCI": "INVESTMENT",
            "TI": "TI",
            "TECNOLOGIA": "TI",
            "TECNOLOGÍA": "TI",
        }
        code = mapping.get(raw_upper, raw_upper.replace(" ", "_")[:30])

    un = UnidadNegocio.objects.filter(code__iexact=code).first()
    if un:
        return un
    return UnidadNegocio.objects.filter(nombre__icontains=raw[:20]).first()


def _entidad_codigo_from_row(row: pd.Series) -> str:
    codigo = pick(row, "codigo", "codigo_cliente", "id_cliente", "cod_cliente")
    if codigo:
        return _slug_codigo(codigo)
    nit = pick(row, "nit", "nit_cliente")
    if nit:
        return _slug_codigo(nit)
    nombre = pick(row, "nombre", "razon_social", "cliente", "nombre_cliente")
    return _slug_codigo(nombre[:20]) if nombre else ""


def _flag_activo(raw: str) -> bool:
    s = (raw or "").strip().lower()
    if not s:
        return False
    if any(x in s for x in ("✅", "si", "sí", "yes", "true", "1", "x")):
        return True
    if any(x in s for x in ("❌", "no", "false", "0")):
        return False
    return False


def _ensure_producto(code: str, nombre: str, unidad_code: str) -> Producto:
    unidad = UnidadNegocio.objects.filter(code=unidad_code).first()
    prod, _ = Producto.objects.update_or_create(
        codigo=code,
        defaults={"nombre": nombre, "unidad_negocio": unidad, "activo": True},
    )
    return prod


def import_infoclientes_wcg(user, uploaded_file) -> DataImportBatch:
    from core.services.import_base import read_dataframe

    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(
        df,
        [["codigo", "codigo_cliente", "nit", "nombre", "cliente", "razon_social", "nombre_cliente"]],
    )
    uploaded_file.seek(0)

    prod_wcf = _ensure_producto("WCF", "Working Capital Factoring", "FACTORING")
    prod_wcl = _ensure_producto("WCL", "Working Capital Leasing", "LEASING")
    prod_wci = _ensure_producto("WCI", "Working Capital Investment", "INVESTMENT")

    def handler(row: pd.Series, errors: list[str]):
        codigo = _entidad_codigo_from_row(row)
        nombre = pick(row, "nombre", "razon_social", "cliente", "nombre_cliente")
        if not codigo or not nombre:
            errors.append("falta identificador o nombre de entidad")
            return None

        # Unidad principal según flags WCF/WCL/WCI (prioridad Leasing > Factoring > Investment)
        flags = {
            "LEASING": _flag_activo(pick(row, "wcl")),
            "FACTORING": _flag_activo(pick(row, "wcf")),
            "INVESTMENT": _flag_activo(pick(row, "wci")),
        }
        unidad = _resolve_unidad(pick(row, "une", "unidad_negocio", "unidad", "une_origen"))
        if not unidad:
            for code in ("LEASING", "FACTORING", "INVESTMENT"):
                if flags[code]:
                    unidad = UnidadNegocio.objects.filter(code=code).first()
                    break

        tipo_raw = pick(row, "tipo", "tipo_entidad", "tipo_cliente").upper()
        tipo = Entidad.TIPO_CLIENTE
        if "PROSPECT" in tipo_raw:
            tipo = Entidad.TIPO_PROSPECTO

        notas_parts = []
        for label, active in (("WCF", flags["FACTORING"]), ("WCL", flags["LEASING"]), ("WCI", flags["INVESTMENT"])):
            notas_parts.append(f"{label}={'Sí' if active else 'No'}")
        notas = pick(row, "notas", "observaciones")
        if notas_parts:
            notas = (notas + " | " if notas else "") + ", ".join(notas_parts)

        entidad, created_e = Entidad.objects.update_or_create(
            codigo=codigo,
            defaults={
                "nombre": nombre,
                "nit": pick(row, "nit", "nit_cliente"),
                "tipo": tipo,
                "unidad_negocio": unidad,
                "activa": True,
                "notas": notas,
            },
        )

        created_any = created_e
        updated_any = not created_e

        # Relaciones producto por flags
        for flag_key, prod in (
            ("FACTORING", prod_wcf),
            ("LEASING", prod_wcl),
            ("INVESTMENT", prod_wci),
        ):
            if flags[flag_key]:
                _, created_r = RelacionEntidadProducto.objects.update_or_create(
                    entidad=entidad,
                    producto=prod,
                    defaults={"estado": RelacionEntidadProducto.ESTADO_ACTIVO},
                )
                created_any = created_any or created_r
                updated_any = updated_any or (not created_r)

        # Contacto desde correo/teléfono del archivo InfoClientes
        email_raw = pick(row, "email", "correo", "correo_electronico")
        telefono = pick(row, "telefono", "tel", "celular")
        contacto_nombre = pick(row, "contacto", "contacto_nombre", "nombre_contacto")
        if not contacto_nombre and (email_raw or telefono):
            # Primer correo como etiqueta de contacto
            contacto_nombre = (email_raw.split(",")[0].strip().split("@")[0] if email_raw else "Contacto")[:120]

        if contacto_nombre:
            # Tomar primer email si vienen varios
            email = email_raw.split(",")[0].strip() if email_raw else ""
            if email and "@" not in email:
                email = ""
            tel = telefono.split(",")[0].strip()[:40] if telefono else ""
            defaults = {
                "nombre": contacto_nombre[:120],
                "email": email[:254] if email else "",
                "telefono": tel,
                "cargo": pick(row, "cargo", "puesto"),
                "es_principal": True,
                "activo": True,
            }
            try:
                if email:
                    _, created_c = Contacto.objects.update_or_create(
                        entidad=entidad, email=email, defaults=defaults
                    )
                else:
                    _, created_c = Contacto.objects.update_or_create(
                        entidad=entidad, nombre=contacto_nombre[:120], defaults=defaults
                    )
                created_any = created_any or created_c
                updated_any = updated_any or (not created_c)
            except Exception as exc:
                errors.append(f"contacto: {exc}")
                return None

        return created_any, updated_any and not created_any

    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_CRM,
        tipo_importacion="infoclientes_wcg",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_entidades(user, uploaded_file) -> DataImportBatch:
    """Alias compatible con UI existente — usa mapeo InfoClientes."""
    return import_infoclientes_wcg(user, uploaded_file)


def import_contactos(user, uploaded_file) -> DataImportBatch:
    """
    Archivo dedicado de contactos (si viene separado del maestro).
    Columnas mínimas: entidad_codigo o nit + nombre contacto.
    """
    from core.services.import_base import read_dataframe

    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(df, [["entidad_codigo", "nit", "codigo"], ["nombre", "contacto", "contacto_nombre"]])

    def handler(row: pd.Series, errors: list[str]):
        ent_code = pick(row, "entidad_codigo", "codigo", "codigo_cliente") or _slug_codigo(
            pick(row, "nit")
        )
        nombre = pick(row, "nombre", "contacto", "contacto_nombre")
        if not ent_code or not nombre:
            errors.append("entidad y nombre contacto obligatorios")
            return None
        entidad = Entidad.objects.filter(codigo__iexact=ent_code).first()
        if not entidad:
            errors.append(f"entidad no encontrada: {ent_code}")
            return None
        email = pick(row, "email", "correo")
        defaults = {
            "nombre": nombre,
            "email": email,
            "telefono": pick(row, "telefono"),
            "cargo": pick(row, "cargo"),
            "activo": True,
        }
        if email:
            _, created = Contacto.objects.update_or_create(
                entidad=entidad, email=email, defaults=defaults
            )
        else:
            _, created = Contacto.objects.update_or_create(
                entidad=entidad, nombre=nombre, defaults=defaults
            )
        return created, not created

    uploaded_file.seek(0)
    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_CRM,
        tipo_importacion="contactos",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Importadores CRM ajustados a archivos reales WCG.
00003|
00004|Archivo referencia: `crm datos - InfoClientesWCG para CRM.csv`
00005|Columnas: NIT, NombreCliente, Teléfono, Correo, WCF, WCL, WCI
00006|
00007|Clave natural Entidad: `codigo` (NIT normalizado)
00008|Clave natural Contacto: (`entidad`, `email`) o (`entidad`, `nombre`)
00009|"""
00010|
00011|from __future__ import annotations
00012|
00013|import re
00014|
00015|import pandas as pd
00016|
00017|from core.services.column_map import normalize_columns, pick, require_any
00018|from core.services.import_base import cell_str, run_import_batch
00019|from core.wcg_models import Contacto, DataImportBatch, Entidad, Producto, RelacionEntidadProducto, UnidadNegocio
00020|
00021|
00022|def _slug_codigo(value: str) -> str:
00023|    s = re.sub(r"[^A-Za-z0-9]+", "", value.upper())[:50]
00024|    return s or "SINCODIGO"
00025|
00026|
00027|def _resolve_unidad(code_or_name: str) -> UnidadNegocio | None:
00028|    if not code_or_name:
00029|        return None
00030|    raw = code_or_name.strip()
00031|    raw_upper = raw.upper()
00032|    raw_lower = raw.lower()
00033|
00034|    if any(
00035|        token in raw_lower
00036|        for token in ("investment", "investments", "invest", "inversiones", "inversion", "inversión")
00037|    ):
00038|        code = "INVESTMENT"
00039|    else:
00040|        mapping = {
00041|            "FACTORAJE": "FACTORING",
00042|            "FACTORING": "FACTORING",
00043|            "LEASING": "LEASING",
00044|            "INSURANCE": "INSURANCE",
00045|            "INVESTMENT": "INVESTMENT",
00046|            "WCF": "FACTORING",
00047|            "WCL": "LEASING",
00048|            "WCI": "INVESTMENT",
00049|            "TI": "TI",
00050|            "TECNOLOGIA": "TI",
00051|            "TECNOLOGÍA": "TI",
00052|        }
00053|        code = mapping.get(raw_upper, raw_upper.replace(" ", "_")[:30])
00054|
00055|    un = UnidadNegocio.objects.filter(code__iexact=code).first()
00056|    if un:
00057|        return un
00058|    return UnidadNegocio.objects.filter(nombre__icontains=raw[:20]).first()
00059|
00060|
00061|def _entidad_codigo_from_row(row: pd.Series) -> str:
00062|    codigo = pick(row, "codigo", "codigo_cliente", "id_cliente", "cod_cliente")
00063|    if codigo:
00064|        return _slug_codigo(codigo)
00065|    nit = pick(row, "nit", "nit_cliente")
00066|    if nit:
00067|        return _slug_codigo(nit)
00068|    nombre = pick(row, "nombre", "razon_social", "cliente", "nombre_cliente")
00069|    return _slug_codigo(nombre[:20]) if nombre else ""
00070|
00071|
00072|def _flag_activo(raw: str) -> bool:
00073|    s = (raw or "").strip().lower()
00074|    if not s:
00075|        return False
00076|    if any(x in s for x in ("✅", "si", "sí", "yes", "true", "1", "x")):
00077|        return True
00078|    if any(x in s for x in ("❌", "no", "false", "0")):
00079|        return False
00080|    return False
00081|
00082|
00083|def _ensure_producto(code: str, nombre: str, unidad_code: str) -> Producto:
00084|    unidad = UnidadNegocio.objects.filter(code=unidad_code).first()
00085|    prod, _ = Producto.objects.update_or_create(
00086|        codigo=code,
00087|        defaults={"nombre": nombre, "unidad_negocio": unidad, "activo": True},
00088|    )
00089|    return prod
00090|
00091|
00092|def import_infoclientes_wcg(user, uploaded_file) -> DataImportBatch:
00093|    from core.services.import_base import read_dataframe
00094|
00095|    df = normalize_columns(read_dataframe(uploaded_file))
00096|    require_any(
00097|        df,
00098|        [["codigo", "codigo_cliente", "nit", "nombre", "cliente", "razon_social", "nombre_cliente"]],
00099|    )
00100|    uploaded_file.seek(0)
00101|
00102|    prod_wcf = _ensure_producto("WCF", "Working Capital Factoring", "FACTORING")
00103|    prod_wcl = _ensure_producto("WCL", "Working Capital Leasing", "LEASING")
00104|    prod_wci = _ensure_producto("WCI", "Working Capital Investment", "INVESTMENT")
00105|
00106|    def handler(row: pd.Series, errors: list[str]):
00107|        codigo = _entidad_codigo_from_row(row)
00108|        nombre = pick(row, "nombre", "razon_social", "cliente", "nombre_cliente")
00109|        if not codigo or not nombre:
00110|            errors.append("falta identificador o nombre de entidad")
00111|            return None
00112|
00113|        # Unidad principal según flags WCF/WCL/WCI (prioridad Leasing > Factoring > Investment)
00114|        flags = {
00115|            "LEASING": _flag_activo(pick(row, "wcl")),
00116|            "FACTORING": _flag_activo(pick(row, "wcf")),
00117|            "INVESTMENT": _flag_activo(pick(row, "wci")),
00118|        }
00119|        unidad = _resolve_unidad(pick(row, "une", "unidad_negocio", "unidad", "une_origen"))
00120|        if not unidad:
00121|            for code in ("LEASING", "FACTORING", "INVESTMENT"):
00122|                if flags[code]:
00123|                    unidad = UnidadNegocio.objects.filter(code=code).first()
00124|                    break
00125|
00126|        tipo_raw = pick(row, "tipo", "tipo_entidad", "tipo_cliente").upper()
00127|        tipo = Entidad.TIPO_CLIENTE
00128|        if "PROSPECT" in tipo_raw:
00129|            tipo = Entidad.TIPO_PROSPECTO
00130|
00131|        notas_parts = []
00132|        for label, active in (("WCF", flags["FACTORING"]), ("WCL", flags["LEASING"]), ("WCI", flags["INVESTMENT"])):
00133|            notas_parts.append(f"{label}={'Sí' if active else 'No'}")
00134|        notas = pick(row, "notas", "observaciones")
00135|        if notas_parts:
00136|            notas = (notas + " | " if notas else "") + ", ".join(notas_parts)
00137|
00138|        entidad, created_e = Entidad.objects.update_or_create(
00139|            codigo=codigo,
00140|            defaults={
00141|                "nombre": nombre,
00142|                "nit": pick(row, "nit", "nit_cliente"),
00143|                "tipo": tipo,
00144|                "unidad_negocio": unidad,
00145|                "activa": True,
00146|                "notas": notas,
00147|            },
00148|        )
00149|
00150|        created_any = created_e
00151|        updated_any = not created_e
00152|
00153|        # Relaciones producto por flags
00154|        for flag_key, prod in (
00155|            ("FACTORING", prod_wcf),
00156|            ("LEASING", prod_wcl),
00157|            ("INVESTMENT", prod_wci),
00158|        ):
00159|            if flags[flag_key]:
00160|                _, created_r = RelacionEntidadProducto.objects.update_or_create(
00161|                    entidad=entidad,
00162|                    producto=prod,
00163|                    defaults={"estado": RelacionEntidadProducto.ESTADO_ACTIVO},
00164|                )
00165|                created_any = created_any or created_r
00166|                updated_any = updated_any or (not created_r)
00167|
00168|        # Contacto desde correo/teléfono del archivo InfoClientes
00169|        email_raw = pick(row, "email", "correo", "correo_electronico")
00170|        telefono = pick(row, "telefono", "tel", "celular")
00171|        contacto_nombre = pick(row, "contacto", "contacto_nombre", "nombre_contacto")
00172|        if not contacto_nombre and (email_raw or telefono):
00173|            # Primer correo como etiqueta de contacto
00174|            contacto_nombre = (email_raw.split(",")[0].strip().split("@")[0] if email_raw else "Contacto")[:120]
00175|
00176|        if contacto_nombre:
00177|            # Tomar primer email si vienen varios
00178|            email = email_raw.split(",")[0].strip() if email_raw else ""
00179|            if email and "@" not in email:
00180|                email = ""
00181|            tel = telefono.split(",")[0].strip()[:40] if telefono else ""
00182|            defaults = {
00183|                "nombre": contacto_nombre[:120],
00184|                "email": email[:254] if email else "",
00185|                "telefono": tel,
00186|                "cargo": pick(row, "cargo", "puesto"),
00187|                "es_principal": True,
00188|                "activo": True,
00189|            }
00190|            try:
00191|                if email:
00192|                    _, created_c = Contacto.objects.update_or_create(
00193|                        entidad=entidad, email=email, defaults=defaults
00194|                    )
00195|                else:
00196|                    _, created_c = Contacto.objects.update_or_create(
00197|                        entidad=entidad, nombre=contacto_nombre[:120], defaults=defaults
00198|                    )
00199|                created_any = created_any or created_c
00200|                updated_any = updated_any or (not created_c)
00201|            except Exception as exc:
00202|                errors.append(f"contacto: {exc}")
00203|                return None
00204|
00205|        return created_any, updated_any and not created_any
00206|
00207|    return run_import_batch(
00208|        user=user,
00209|        modulo=DataImportBatch.MODULO_CRM,
00210|        tipo_importacion="infoclientes_wcg",
00211|        uploaded_file=uploaded_file,
00212|        required_columns=[],
00213|        row_handler=handler,
00214|    )
00215|
00216|
00217|def import_entidades(user, uploaded_file) -> DataImportBatch:
00218|    """Alias compatible con UI existente — usa mapeo InfoClientes."""
00219|    return import_infoclientes_wcg(user, uploaded_file)
00220|
00221|
00222|def import_contactos(user, uploaded_file) -> DataImportBatch:
00223|    """
00224|    Archivo dedicado de contactos (si viene separado del maestro).
00225|    Columnas mínimas: entidad_codigo o nit + nombre contacto.
00226|    """
00227|    from core.services.import_base import read_dataframe
00228|
00229|    df = normalize_columns(read_dataframe(uploaded_file))
00230|    require_any(df, [["entidad_codigo", "nit", "codigo"], ["nombre", "contacto", "contacto_nombre"]])
00231|
00232|    def handler(row: pd.Series, errors: list[str]):
00233|        ent_code = pick(row, "entidad_codigo", "codigo", "codigo_cliente") or _slug_codigo(
00234|            pick(row, "nit")
00235|        )
00236|        nombre = pick(row, "nombre", "contacto", "contacto_nombre")
00237|        if not ent_code or not nombre:
00238|            errors.append("entidad y nombre contacto obligatorios")
00239|            return None
00240|        entidad = Entidad.objects.filter(codigo__iexact=ent_code).first()
00241|        if not entidad:
00242|            errors.append(f"entidad no encontrada: {ent_code}")
00243|            return None
00244|        email = pick(row, "email", "correo")
00245|        defaults = {
00246|            "nombre": nombre,
00247|            "email": email,
00248|            "telefono": pick(row, "telefono"),
00249|            "cargo": pick(row, "cargo"),
00250|            "activo": True,
00251|        }
00252|        if email:
00253|            _, created = Contacto.objects.update_or_create(
00254|                entidad=entidad, email=email, defaults=defaults
00255|            )
00256|        else:
00257|            _, created = Contacto.objects.update_or_create(
00258|                entidad=entidad, nombre=nombre, defaults=defaults
00259|            )
00260|        return created, not created
00261|
00262|    uploaded_file.seek(0)
00263|    return run_import_batch(
00264|        user=user,
00265|        modulo=DataImportBatch.MODULO_CRM,
00266|        tipo_importacion="contactos",
00267|        uploaded_file=uploaded_file,
00268|        required_columns=[],
00269|        row_handler=handler,
00270|    )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiCkltcG9ydGFkb3JlcyBDUk0gYWp1c3RhZG9zIGEgYXJjaGl2b3MgcmVhbGVzIFdDRy4KCkFyY2hpdm8gcmVmZXJlbmNpYTogYGNybSBkYXRvcyAtIEluZm9DbGllbnRlc1dDRyBwYXJhIENSTS5jc3ZgCkNvbHVtbmFzOiBOSVQsIE5vbWJyZUNsaWVudGUsIFRlbMOpZm9ubywgQ29ycmVvLCBXQ0YsIFdDTCwgV0NJCgpDbGF2ZSBuYXR1cmFsIEVudGlkYWQ6IGBjb2RpZ29gIChOSVQgbm9ybWFsaXphZG8pCkNsYXZlIG5hdHVyYWwgQ29udGFjdG86IChgZW50aWRhZGAsIGBlbWFpbGApIG8gKGBlbnRpZGFkYCwgYG5vbWJyZWApCiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKaW1wb3J0IHJlCgppbXBvcnQgcGFuZGFzIGFzIHBkCgpmcm9tIGNvcmUuc2VydmljZXMuY29sdW1uX21hcCBpbXBvcnQgbm9ybWFsaXplX2NvbHVtbnMsIHBpY2ssIHJlcXVpcmVfYW55CmZyb20gY29yZS5zZXJ2aWNlcy5pbXBvcnRfYmFzZSBpbXBvcnQgY2VsbF9zdHIsIHJ1bl9pbXBvcnRfYmF0Y2gKZnJvbSBjb3JlLndjZ19tb2RlbHMgaW1wb3J0IENvbnRhY3RvLCBEYXRhSW1wb3J0QmF0Y2gsIEVudGlkYWQsIFByb2R1Y3RvLCBSZWxhY2lvbkVudGlkYWRQcm9kdWN0bywgVW5pZGFkTmVnb2NpbwoKCmRlZiBfc2x1Z19jb2RpZ28odmFsdWU6IHN0cikgLT4gc3RyOgogICAgcyA9IHJlLnN1YihyIlteQS1aYS16MC05XSsiLCAiIiwgdmFsdWUudXBwZXIoKSlbOjUwXQogICAgcmV0dXJuIHMgb3IgIlNJTkNPRElHTyIKCgpkZWYgX3Jlc29sdmVfdW5pZGFkKGNvZGVfb3JfbmFtZTogc3RyKSAtPiBVbmlkYWROZWdvY2lvIHwgTm9uZToKICAgIGlmIG5vdCBjb2RlX29yX25hbWU6CiAgICAgICAgcmV0dXJuIE5vbmUKICAgIHJhdyA9IGNvZGVfb3JfbmFtZS5zdHJpcCgpCiAgICByYXdfdXBwZXIgPSByYXcudXBwZXIoKQogICAgcmF3X2xvd2VyID0gcmF3Lmxvd2VyKCkKCiAgICBpZiBhbnkoCiAgICAgICAgdG9rZW4gaW4gcmF3X2xvd2VyCiAgICAgICAgZm9yIHRva2VuIGluICgiaW52ZXN0bWVudCIsICJpbnZlc3RtZW50cyIsICJpbnZlc3QiLCAiaW52ZXJzaW9uZXMiLCAiaW52ZXJzaW9uIiwgImludmVyc2nDs24iKQogICAgKToKICAgICAgICBjb2RlID0gIklOVkVTVE1FTlQiCiAgICBlbHNlOgogICAgICAgIG1hcHBpbmcgPSB7CiAgICAgICAgICAgICJGQUNUT1JBSkUiOiAiRkFDVE9SSU5HIiwKICAgICAgICAgICAgIkZBQ1RPUklORyI6ICJGQUNUT1JJTkciLAogICAgICAgICAgICAiTEVBU0lORyI6ICJMRUFTSU5HIiwKICAgICAgICAgICAgIklOU1VSQU5DRSI6ICJJTlNVUkFOQ0UiLAogICAgICAgICAgICAiSU5WRVNUTUVOVCI6ICJJTlZFU1RNRU5UIiwKICAgICAgICAgICAgIldDRiI6ICJGQUNUT1JJTkciLAogICAgICAgICAgICAiV0NMIjogIkxFQVNJTkciLAogICAgICAgICAgICAiV0NJIjogIklOVkVTVE1FTlQiLAogICAgICAgICAgICAiVEkiOiAiVEkiLAogICAgICAgICAgICAiVEVDTk9MT0dJQSI6ICJUSSIsCiAgICAgICAgICAgICJURUNOT0xPR8ONQSI6ICJUSSIsCiAgICAgICAgfQogICAgICAgIGNvZGUgPSBtYXBwaW5nLmdldChyYXdfdXBwZXIsIHJhd191cHBlci5yZXBsYWNlKCIgIiwgIl8iKVs6MzBdKQoKICAgIHVuID0gVW5pZGFkTmVnb2Npby5vYmplY3RzLmZpbHRlcihjb2RlX19pZXhhY3Q9Y29kZSkuZmlyc3QoKQogICAgaWYgdW46CiAgICAgICAgcmV0dXJuIHVuCiAgICByZXR1cm4gVW5pZGFkTmVnb2Npby5vYmplY3RzLmZpbHRlcihub21icmVfX2ljb250YWlucz1yYXdbOjIwXSkuZmlyc3QoKQoKCmRlZiBfZW50aWRhZF9jb2RpZ29fZnJvbV9yb3cocm93OiBwZC5TZXJpZXMpIC0+IHN0cjoKICAgIGNvZGlnbyA9IHBpY2socm93LCAiY29kaWdvIiwgImNvZGlnb19jbGllbnRlIiwgImlkX2NsaWVudGUiLCAiY29kX2NsaWVudGUiKQogICAgaWYgY29kaWdvOgogICAgICAgIHJldHVybiBfc2x1Z19jb2RpZ28oY29kaWdvKQogICAgbml0ID0gcGljayhyb3csICJuaXQiLCAibml0X2NsaWVudGUiKQogICAgaWYgbml0OgogICAgICAgIHJldHVybiBfc2x1Z19jb2RpZ28obml0KQogICAgbm9tYnJlID0gcGljayhyb3csICJub21icmUiLCAicmF6b25fc29jaWFsIiwgImNsaWVudGUiLCAibm9tYnJlX2NsaWVudGUiKQogICAgcmV0dXJuIF9zbHVnX2NvZGlnbyhub21icmVbOjIwXSkgaWYgbm9tYnJlIGVsc2UgIiIKCgpkZWYgX2ZsYWdfYWN0aXZvKHJhdzogc3RyKSAtPiBib29sOgogICAgcyA9IChyYXcgb3IgIiIpLnN0cmlwKCkubG93ZXIoKQogICAgaWYgbm90IHM6CiAgICAgICAgcmV0dXJuIEZhbHNlCiAgICBpZiBhbnkoeCBpbiBzIGZvciB4IGluICgi4pyFIiwgInNpIiwgInPDrSIsICJ5ZXMiLCAidHJ1ZSIsICIxIiwgIngiKSk6CiAgICAgICAgcmV0dXJuIFRydWUKICAgIGlmIGFueSh4IGluIHMgZm9yIHggaW4gKCLinYwiLCAibm8iLCAiZmFsc2UiLCAiMCIpKToKICAgICAgICByZXR1cm4gRmFsc2UKICAgIHJldHVybiBGYWxzZQoKCmRlZiBfZW5zdXJlX3Byb2R1Y3RvKGNvZGU6IHN0ciwgbm9tYnJlOiBzdHIsIHVuaWRhZF9jb2RlOiBzdHIpIC0+IFByb2R1Y3RvOgogICAgdW5pZGFkID0gVW5pZGFkTmVnb2Npby5vYmplY3RzLmZpbHRlcihjb2RlPXVuaWRhZF9jb2RlKS5maXJzdCgpCiAgICBwcm9kLCBfID0gUHJvZHVjdG8ub2JqZWN0cy51cGRhdGVfb3JfY3JlYXRlKAogICAgICAgIGNvZGlnbz1jb2RlLAogICAgICAgIGRlZmF1bHRzPXsibm9tYnJlIjogbm9tYnJlLCAidW5pZGFkX25lZ29jaW8iOiB1bmlkYWQsICJhY3Rpdm8iOiBUcnVlfSwKICAgICkKICAgIHJldHVybiBwcm9kCgoKZGVmIGltcG9ydF9pbmZvY2xpZW50ZXNfd2NnKHVzZXIsIHVwbG9hZGVkX2ZpbGUpIC0+IERhdGFJbXBvcnRCYXRjaDoKICAgIGZyb20gY29yZS5zZXJ2aWNlcy5pbXBvcnRfYmFzZSBpbXBvcnQgcmVhZF9kYXRhZnJhbWUKCiAgICBkZiA9IG5vcm1hbGl6ZV9jb2x1bW5zKHJlYWRfZGF0YWZyYW1lKHVwbG9hZGVkX2ZpbGUpKQogICAgcmVxdWlyZV9hbnkoCiAgICAgICAgZGYsCiAgICAgICAgW1siY29kaWdvIiwgImNvZGlnb19jbGllbnRlIiwgIm5pdCIsICJub21icmUiLCAiY2xpZW50ZSIsICJyYXpvbl9zb2NpYWwiLCAibm9tYnJlX2NsaWVudGUiXV0sCiAgICApCiAgICB1cGxvYWRlZF9maWxlLnNlZWsoMCkKCiAgICBwcm9kX3djZiA9IF9lbnN1cmVfcHJvZHVjdG8oIldDRiIsICJXb3JraW5nIENhcGl0YWwgRmFjdG9yaW5nIiwgIkZBQ1RPUklORyIpCiAgICBwcm9kX3djbCA9IF9lbnN1cmVfcHJvZHVjdG8oIldDTCIsICJXb3JraW5nIENhcGl0YWwgTGVhc2luZyIsICJMRUFTSU5HIikKICAgIHByb2Rfd2NpID0gX2Vuc3VyZV9wcm9kdWN0bygiV0NJIiwgIldvcmtpbmcgQ2FwaXRhbCBJbnZlc3RtZW50IiwgIklOVkVTVE1FTlQiKQoKICAgIGRlZiBoYW5kbGVyKHJvdzogcGQuU2VyaWVzLCBlcnJvcnM6IGxpc3Rbc3RyXSk6CiAgICAgICAgY29kaWdvID0gX2VudGlkYWRfY29kaWdvX2Zyb21fcm93KHJvdykKICAgICAgICBub21icmUgPSBwaWNrKHJvdywgIm5vbWJyZSIsICJyYXpvbl9zb2NpYWwiLCAiY2xpZW50ZSIsICJub21icmVfY2xpZW50ZSIpCiAgICAgICAgaWYgbm90IGNvZGlnbyBvciBub3Qgbm9tYnJlOgogICAgICAgICAgICBlcnJvcnMuYXBwZW5kKCJmYWx0YSBpZGVudGlmaWNhZG9yIG8gbm9tYnJlIGRlIGVudGlkYWQiKQogICAgICAgICAgICByZXR1cm4gTm9uZQoKICAgICAgICAjIFVuaWRhZCBwcmluY2lwYWwgc2Vnw7puIGZsYWdzIFdDRi9XQ0wvV0NJIChwcmlvcmlkYWQgTGVhc2luZyA+IEZhY3RvcmluZyA+IEludmVzdG1lbnQpCiAgICAgICAgZmxhZ3MgPSB7CiAgICAgICAgICAgICJMRUFTSU5HIjogX2ZsYWdfYWN0aXZvKHBpY2socm93LCAid2NsIikpLAogICAgICAgICAgICAiRkFDVE9SSU5HIjogX2ZsYWdfYWN0aXZvKHBpY2socm93LCAid2NmIikpLAogICAgICAgICAgICAiSU5WRVNUTUVOVCI6IF9mbGFnX2FjdGl2byhwaWNrKHJvdywgIndjaSIpKSwKICAgICAgICB9CiAgICAgICAgdW5pZGFkID0gX3Jlc29sdmVfdW5pZGFkKHBpY2socm93LCAidW5lIiwgInVuaWRhZF9uZWdvY2lvIiwgInVuaWRhZCIsICJ1bmVfb3JpZ2VuIikpCiAgICAgICAgaWYgbm90IHVuaWRhZDoKICAgICAgICAgICAgZm9yIGNvZGUgaW4gKCJMRUFTSU5HIiwgIkZBQ1RPUklORyIsICJJTlZFU1RNRU5UIik6CiAgICAgICAgICAgICAgICBpZiBmbGFnc1tjb2RlXToKICAgICAgICAgICAgICAgICAgICB1bmlkYWQgPSBVbmlkYWROZWdvY2lvLm9iamVjdHMuZmlsdGVyKGNvZGU9Y29kZSkuZmlyc3QoKQogICAgICAgICAgICAgICAgICAgIGJyZWFrCgogICAgICAgIHRpcG9fcmF3ID0gcGljayhyb3csICJ0aXBvIiwgInRpcG9fZW50aWRhZCIsICJ0aXBvX2NsaWVudGUiKS51cHBlcigpCiAgICAgICAgdGlwbyA9IEVudGlkYWQuVElQT19DTElFTlRFCiAgICAgICAgaWYgIlBST1NQRUNUIiBpbiB0aXBvX3JhdzoKICAgICAgICAgICAgdGlwbyA9IEVudGlkYWQuVElQT19QUk9TUEVDVE8KCiAgICAgICAgbm90YXNfcGFydHMgPSBbXQogICAgICAgIGZvciBsYWJlbCwgYWN0aXZlIGluICgoIldDRiIsIGZsYWdzWyJGQUNUT1JJTkciXSksICgiV0NMIiwgZmxhZ3NbIkxFQVNJTkciXSksICgiV0NJIiwgZmxhZ3NbIklOVkVTVE1FTlQiXSkpOgogICAgICAgICAgICBub3Rhc19wYXJ0cy5hcHBlbmQoZiJ7bGFiZWx9PXsnU8OtJyBpZiBhY3RpdmUgZWxzZSAnTm8nfSIpCiAgICAgICAgbm90YXMgPSBwaWNrKHJvdywgIm5vdGFzIiwgIm9ic2VydmFjaW9uZXMiKQogICAgICAgIGlmIG5vdGFzX3BhcnRzOgogICAgICAgICAgICBub3RhcyA9IChub3RhcyArICIgfCAiIGlmIG5vdGFzIGVsc2UgIiIpICsgIiwgIi5qb2luKG5vdGFzX3BhcnRzKQoKICAgICAgICBlbnRpZGFkLCBjcmVhdGVkX2UgPSBFbnRpZGFkLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgY29kaWdvPWNvZGlnbywKICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgIm5vbWJyZSI6IG5vbWJyZSwKICAgICAgICAgICAgICAgICJuaXQiOiBwaWNrKHJvdywgIm5pdCIsICJuaXRfY2xpZW50ZSIpLAogICAgICAgICAgICAgICAgInRpcG8iOiB0aXBvLAogICAgICAgICAgICAgICAgInVuaWRhZF9uZWdvY2lvIjogdW5pZGFkLAogICAgICAgICAgICAgICAgImFjdGl2YSI6IFRydWUsCiAgICAgICAgICAgICAgICAibm90YXMiOiBub3RhcywKICAgICAgICAgICAgfSwKICAgICAgICApCgogICAgICAgIGNyZWF0ZWRfYW55ID0gY3JlYXRlZF9lCiAgICAgICAgdXBkYXRlZF9hbnkgPSBub3QgY3JlYXRlZF9lCgogICAgICAgICMgUmVsYWNpb25lcyBwcm9kdWN0byBwb3IgZmxhZ3MKICAgICAgICBmb3IgZmxhZ19rZXksIHByb2QgaW4gKAogICAgICAgICAgICAoIkZBQ1RPUklORyIsIHByb2Rfd2NmKSwKICAgICAgICAgICAgKCJMRUFTSU5HIiwgcHJvZF93Y2wpLAogICAgICAgICAgICAoIklOVkVTVE1FTlQiLCBwcm9kX3djaSksCiAgICAgICAgKToKICAgICAgICAgICAgaWYgZmxhZ3NbZmxhZ19rZXldOgogICAgICAgICAgICAgICAgXywgY3JlYXRlZF9yID0gUmVsYWNpb25FbnRpZGFkUHJvZHVjdG8ub2JqZWN0cy51cGRhdGVfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgICAgIGVudGlkYWQ9ZW50aWRhZCwKICAgICAgICAgICAgICAgICAgICBwcm9kdWN0bz1wcm9kLAogICAgICAgICAgICAgICAgICAgIGRlZmF1bHRzPXsiZXN0YWRvIjogUmVsYWNpb25FbnRpZGFkUHJvZHVjdG8uRVNUQURPX0FDVElWT30sCiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICBjcmVhdGVkX2FueSA9IGNyZWF0ZWRfYW55IG9yIGNyZWF0ZWRfcgogICAgICAgICAgICAgICAgdXBkYXRlZF9hbnkgPSB1cGRhdGVkX2FueSBvciAobm90IGNyZWF0ZWRfcikKCiAgICAgICAgIyBDb250YWN0byBkZXNkZSBjb3JyZW8vdGVsw6lmb25vIGRlbCBhcmNoaXZvIEluZm9DbGllbnRlcwogICAgICAgIGVtYWlsX3JhdyA9IHBpY2socm93LCAiZW1haWwiLCAiY29ycmVvIiwgImNvcnJlb19lbGVjdHJvbmljbyIpCiAgICAgICAgdGVsZWZvbm8gPSBwaWNrKHJvdywgInRlbGVmb25vIiwgInRlbCIsICJjZWx1bGFyIikKICAgICAgICBjb250YWN0b19ub21icmUgPSBwaWNrKHJvdywgImNvbnRhY3RvIiwgImNvbnRhY3RvX25vbWJyZSIsICJub21icmVfY29udGFjdG8iKQogICAgICAgIGlmIG5vdCBjb250YWN0b19ub21icmUgYW5kIChlbWFpbF9yYXcgb3IgdGVsZWZvbm8pOgogICAgICAgICAgICAjIFByaW1lciBjb3JyZW8gY29tbyBldGlxdWV0YSBkZSBjb250YWN0bwogICAgICAgICAgICBjb250YWN0b19ub21icmUgPSAoZW1haWxfcmF3LnNwbGl0KCIsIilbMF0uc3RyaXAoKS5zcGxpdCgiQCIpWzBdIGlmIGVtYWlsX3JhdyBlbHNlICJDb250YWN0byIpWzoxMjBdCgogICAgICAgIGlmIGNvbnRhY3RvX25vbWJyZToKICAgICAgICAgICAgIyBUb21hciBwcmltZXIgZW1haWwgc2kgdmllbmVuIHZhcmlvcwogICAgICAgICAgICBlbWFpbCA9IGVtYWlsX3Jhdy5zcGxpdCgiLCIpWzBdLnN0cmlwKCkgaWYgZW1haWxfcmF3IGVsc2UgIiIKICAgICAgICAgICAgaWYgZW1haWwgYW5kICJAIiBub3QgaW4gZW1haWw6CiAgICAgICAgICAgICAgICBlbWFpbCA9ICIiCiAgICAgICAgICAgIHRlbCA9IHRlbGVmb25vLnNwbGl0KCIsIilbMF0uc3RyaXAoKVs6NDBdIGlmIHRlbGVmb25vIGVsc2UgIiIKICAgICAgICAgICAgZGVmYXVsdHMgPSB7CiAgICAgICAgICAgICAgICAibm9tYnJlIjogY29udGFjdG9fbm9tYnJlWzoxMjBdLAogICAgICAgICAgICAgICAgImVtYWlsIjogZW1haWxbOjI1NF0gaWYgZW1haWwgZWxzZSAiIiwKICAgICAgICAgICAgICAgICJ0ZWxlZm9ubyI6IHRlbCwKICAgICAgICAgICAgICAgICJjYXJnbyI6IHBpY2socm93LCAiY2FyZ28iLCAicHVlc3RvIiksCiAgICAgICAgICAgICAgICAiZXNfcHJpbmNpcGFsIjogVHJ1ZSwKICAgICAgICAgICAgICAgICJhY3Rpdm8iOiBUcnVlLAogICAgICAgICAgICB9CiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIGlmIGVtYWlsOgogICAgICAgICAgICAgICAgICAgIF8sIGNyZWF0ZWRfYyA9IENvbnRhY3RvLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgICAgICAgICAgICAgZW50aWRhZD1lbnRpZGFkLCBlbWFpbD1lbWFpbCwgZGVmYXVsdHM9ZGVmYXVsdHMKICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgICAgIF8sIGNyZWF0ZWRfYyA9IENvbnRhY3RvLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgICAgICAgICAgICAgZW50aWRhZD1lbnRpZGFkLCBub21icmU9Y29udGFjdG9fbm9tYnJlWzoxMjBdLCBkZWZhdWx0cz1kZWZhdWx0cwogICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIGNyZWF0ZWRfYW55ID0gY3JlYXRlZF9hbnkgb3IgY3JlYXRlZF9jCiAgICAgICAgICAgICAgICB1cGRhdGVkX2FueSA9IHVwZGF0ZWRfYW55IG9yIChub3QgY3JlYXRlZF9jKQogICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGV4YzoKICAgICAgICAgICAgICAgIGVycm9ycy5hcHBlbmQoZiJjb250YWN0bzoge2V4Y30iKQogICAgICAgICAgICAgICAgcmV0dXJuIE5vbmUKCiAgICAgICAgcmV0dXJuIGNyZWF0ZWRfYW55LCB1cGRhdGVkX2FueSBhbmQgbm90IGNyZWF0ZWRfYW55CgogICAgcmV0dXJuIHJ1bl9pbXBvcnRfYmF0Y2goCiAgICAgICAgdXNlcj11c2VyLAogICAgICAgIG1vZHVsbz1EYXRhSW1wb3J0QmF0Y2guTU9EVUxPX0NSTSwKICAgICAgICB0aXBvX2ltcG9ydGFjaW9uPSJpbmZvY2xpZW50ZXNfd2NnIiwKICAgICAgICB1cGxvYWRlZF9maWxlPXVwbG9hZGVkX2ZpbGUsCiAgICAgICAgcmVxdWlyZWRfY29sdW1ucz1bXSwKICAgICAgICByb3dfaGFuZGxlcj1oYW5kbGVyLAogICAgKQoKCmRlZiBpbXBvcnRfZW50aWRhZGVzKHVzZXIsIHVwbG9hZGVkX2ZpbGUpIC0+IERhdGFJbXBvcnRCYXRjaDoKICAgICIiIkFsaWFzIGNvbXBhdGlibGUgY29uIFVJIGV4aXN0ZW50ZSDigJQgdXNhIG1hcGVvIEluZm9DbGllbnRlcy4iIiIKICAgIHJldHVybiBpbXBvcnRfaW5mb2NsaWVudGVzX3djZyh1c2VyLCB1cGxvYWRlZF9maWxlKQoKCmRlZiBpbXBvcnRfY29udGFjdG9zKHVzZXIsIHVwbG9hZGVkX2ZpbGUpIC0+IERhdGFJbXBvcnRCYXRjaDoKICAgICIiIgogICAgQXJjaGl2byBkZWRpY2FkbyBkZSBjb250YWN0b3MgKHNpIHZpZW5lIHNlcGFyYWRvIGRlbCBtYWVzdHJvKS4KICAgIENvbHVtbmFzIG3DrW5pbWFzOiBlbnRpZGFkX2NvZGlnbyBvIG5pdCArIG5vbWJyZSBjb250YWN0by4KICAgICIiIgogICAgZnJvbSBjb3JlLnNlcnZpY2VzLmltcG9ydF9iYXNlIGltcG9ydCByZWFkX2RhdGFmcmFtZQoKICAgIGRmID0gbm9ybWFsaXplX2NvbHVtbnMocmVhZF9kYXRhZnJhbWUodXBsb2FkZWRfZmlsZSkpCiAgICByZXF1aXJlX2FueShkZiwgW1siZW50aWRhZF9jb2RpZ28iLCAibml0IiwgImNvZGlnbyJdLCBbIm5vbWJyZSIsICJjb250YWN0byIsICJjb250YWN0b19ub21icmUiXV0pCgogICAgZGVmIGhhbmRsZXIocm93OiBwZC5TZXJpZXMsIGVycm9yczogbGlzdFtzdHJdKToKICAgICAgICBlbnRfY29kZSA9IHBpY2socm93LCAiZW50aWRhZF9jb2RpZ28iLCAiY29kaWdvIiwgImNvZGlnb19jbGllbnRlIikgb3IgX3NsdWdfY29kaWdvKAogICAgICAgICAgICBwaWNrKHJvdywgIm5pdCIpCiAgICAgICAgKQogICAgICAgIG5vbWJyZSA9IHBpY2socm93LCAibm9tYnJlIiwgImNvbnRhY3RvIiwgImNvbnRhY3RvX25vbWJyZSIpCiAgICAgICAgaWYgbm90IGVudF9jb2RlIG9yIG5vdCBub21icmU6CiAgICAgICAgICAgIGVycm9ycy5hcHBlbmQoImVudGlkYWQgeSBub21icmUgY29udGFjdG8gb2JsaWdhdG9yaW9zIikKICAgICAgICAgICAgcmV0dXJuIE5vbmUKICAgICAgICBlbnRpZGFkID0gRW50aWRhZC5vYmplY3RzLmZpbHRlcihjb2RpZ29fX2lleGFjdD1lbnRfY29kZSkuZmlyc3QoKQogICAgICAgIGlmIG5vdCBlbnRpZGFkOgogICAgICAgICAgICBlcnJvcnMuYXBwZW5kKGYiZW50aWRhZCBubyBlbmNvbnRyYWRhOiB7ZW50X2NvZGV9IikKICAgICAgICAgICAgcmV0dXJuIE5vbmUKICAgICAgICBlbWFpbCA9IHBpY2socm93LCAiZW1haWwiLCAiY29ycmVvIikKICAgICAgICBkZWZhdWx0cyA9IHsKICAgICAgICAgICAgIm5vbWJyZSI6IG5vbWJyZSwKICAgICAgICAgICAgImVtYWlsIjogZW1haWwsCiAgICAgICAgICAgICJ0ZWxlZm9ubyI6IHBpY2socm93LCAidGVsZWZvbm8iKSwKICAgICAgICAgICAgImNhcmdvIjogcGljayhyb3csICJjYXJnbyIpLAogICAgICAgICAgICAiYWN0aXZvIjogVHJ1ZSwKICAgICAgICB9CiAgICAgICAgaWYgZW1haWw6CiAgICAgICAgICAgIF8sIGNyZWF0ZWQgPSBDb250YWN0by5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICBlbnRpZGFkPWVudGlkYWQsIGVtYWlsPWVtYWlsLCBkZWZhdWx0cz1kZWZhdWx0cwogICAgICAgICAgICApCiAgICAgICAgZWxzZToKICAgICAgICAgICAgXywgY3JlYXRlZCA9IENvbnRhY3RvLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgICAgIGVudGlkYWQ9ZW50aWRhZCwgbm9tYnJlPW5vbWJyZSwgZGVmYXVsdHM9ZGVmYXVsdHMKICAgICAgICAgICAgKQogICAgICAgIHJldHVybiBjcmVhdGVkLCBub3QgY3JlYXRlZAoKICAgIHVwbG9hZGVkX2ZpbGUuc2VlaygwKQogICAgcmV0dXJuIHJ1bl9pbXBvcnRfYmF0Y2goCiAgICAgICAgdXNlcj11c2VyLAogICAgICAgIG1vZHVsbz1EYXRhSW1wb3J0QmF0Y2guTU9EVUxPX0NSTSwKICAgICAgICB0aXBvX2ltcG9ydGFjaW9uPSJjb250YWN0b3MiLAogICAgICAgIHVwbG9hZGVkX2ZpbGU9dXBsb2FkZWRfZmlsZSwKICAgICAgICByZXF1aXJlZF9jb2x1bW5zPVtdLAogICAgICAgIHJvd19oYW5kbGVyPWhhbmRsZXIsCiAgICApCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=crm/tests.py
PATH_JSON="crm/tests.py"
FILENAME=tests.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=3
SIZE_BYTES_UTF8=60
CONTENT_SHA256=9ab6c6191360e63c1b4c9b5659aef348a743c9e078be68190917369e4e9563e8
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
from django.test import TestCase

# Create your tests here.

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.test import TestCase
00002|
00003|# Create your tests here.

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udGVzdCBpbXBvcnQgVGVzdENhc2UKCiMgQ3JlYXRlIHlvdXIgdGVzdHMgaGVyZS4K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=crm/urls.py
PATH_JSON="crm/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=17
SIZE_BYTES_UTF8=795
CONTENT_SHA256=ce9167037bfe843e991576d063bbd6fe41378eb391f138fa0684050cdecfcc88
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

app_name = "crm"

urlpatterns = [
    path("", views.EntidadListView.as_view(), name="entidad_list"),
    path("contactos/", views.ContactoListView.as_view(), name="contacto_list"),
    path("tareas/", views.TareaListView.as_view(), name="tarea_list"),
    path("exportar/", views.export_entidades, name="export_entidades"),
    path("entidades/<str:codigo>/", views.EntidadDetailView.as_view(), name="entidad_detail"),
    path("entidades/<str:codigo>/interaccion/nueva/", views.nueva_interaccion, name="nueva_interaccion"),
    path("entidades/<str:codigo>/tarea/nueva/", views.nueva_tarea, name="nueva_tarea"),
    path("importar/", views.importar, name="importar"),
    path("importar/<str:tipo>/", views.importar, name="importar_tipo"),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.urls import path
00002|
00003|from . import views
00004|
00005|app_name = "crm"
00006|
00007|urlpatterns = [
00008|    path("", views.EntidadListView.as_view(), name="entidad_list"),
00009|    path("contactos/", views.ContactoListView.as_view(), name="contacto_list"),
00010|    path("tareas/", views.TareaListView.as_view(), name="tarea_list"),
00011|    path("exportar/", views.export_entidades, name="export_entidades"),
00012|    path("entidades/<str:codigo>/", views.EntidadDetailView.as_view(), name="entidad_detail"),
00013|    path("entidades/<str:codigo>/interaccion/nueva/", views.nueva_interaccion, name="nueva_interaccion"),
00014|    path("entidades/<str:codigo>/tarea/nueva/", views.nueva_tarea, name="nueva_tarea"),
00015|    path("importar/", views.importar, name="importar"),
00016|    path("importar/<str:tipo>/", views.importar, name="importar_tipo"),
00017|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aAoKZnJvbSAuIGltcG9ydCB2aWV3cwoKYXBwX25hbWUgPSAiY3JtIgoKdXJscGF0dGVybnMgPSBbCiAgICBwYXRoKCIiLCB2aWV3cy5FbnRpZGFkTGlzdFZpZXcuYXNfdmlldygpLCBuYW1lPSJlbnRpZGFkX2xpc3QiKSwKICAgIHBhdGgoImNvbnRhY3Rvcy8iLCB2aWV3cy5Db250YWN0b0xpc3RWaWV3LmFzX3ZpZXcoKSwgbmFtZT0iY29udGFjdG9fbGlzdCIpLAogICAgcGF0aCgidGFyZWFzLyIsIHZpZXdzLlRhcmVhTGlzdFZpZXcuYXNfdmlldygpLCBuYW1lPSJ0YXJlYV9saXN0IiksCiAgICBwYXRoKCJleHBvcnRhci8iLCB2aWV3cy5leHBvcnRfZW50aWRhZGVzLCBuYW1lPSJleHBvcnRfZW50aWRhZGVzIiksCiAgICBwYXRoKCJlbnRpZGFkZXMvPHN0cjpjb2RpZ28+LyIsIHZpZXdzLkVudGlkYWREZXRhaWxWaWV3LmFzX3ZpZXcoKSwgbmFtZT0iZW50aWRhZF9kZXRhaWwiKSwKICAgIHBhdGgoImVudGlkYWRlcy88c3RyOmNvZGlnbz4vaW50ZXJhY2Npb24vbnVldmEvIiwgdmlld3MubnVldmFfaW50ZXJhY2Npb24sIG5hbWU9Im51ZXZhX2ludGVyYWNjaW9uIiksCiAgICBwYXRoKCJlbnRpZGFkZXMvPHN0cjpjb2RpZ28+L3RhcmVhL251ZXZhLyIsIHZpZXdzLm51ZXZhX3RhcmVhLCBuYW1lPSJudWV2YV90YXJlYSIpLAogICAgcGF0aCgiaW1wb3J0YXIvIiwgdmlld3MuaW1wb3J0YXIsIG5hbWU9ImltcG9ydGFyIiksCiAgICBwYXRoKCJpbXBvcnRhci88c3RyOnRpcG8+LyIsIHZpZXdzLmltcG9ydGFyLCBuYW1lPSJpbXBvcnRhcl90aXBvIiksCl0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
