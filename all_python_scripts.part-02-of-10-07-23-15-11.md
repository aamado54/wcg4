# CONCATENATED .PY FILES

PART_NUMBER=2
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
PATH_LITERAL=apps/pgo/imports/tickets.py
PATH_JSON="apps/pgo/imports/tickets.py"
FILENAME=tickets.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=175
SIZE_BYTES_UTF8=6451
CONTENT_SHA256=caae9ba3fe96d0a81c5ef6f5dab026efefc7b529f60e4c123124a90972af69f2
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
"""Importador PGO: tickets desde CSV/XLSX."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.core.imports.base import run_import_batch, row_to_json
from apps.core.imports.columns import normalize_columns, pick, pick_decimal, pick_int, require_any
from apps.core.imports.entities import resolve_unidad
from apps.pgo.models import PgoTicket

User = get_user_model()

MODULO = "pgo"
TIPO = "tickets"


def _parse_dt(value: str):
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y %H:%M", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            dt = datetime.strptime(value[:19], fmt)
            return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
        except ValueError:
            continue
    try:
        dt = pd.to_datetime(value).to_pydatetime()
        return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
    except Exception:
        return None


def _normalize_estado(raw: str) -> str:
    s = raw.lower()
    if any(k in s for k in ("cerr", "close", "resuel", "done")):
        return "cerrado"
    if any(k in s for k in ("proces", "progress", "curso")):
        return "en_proceso"
    if any(k in s for k in ("rechaz", "cancel")):
        return "rechazado"
    return "abierto"


def _periodo_from_dt(dt) -> str:
    if not dt:
        return ""
    return dt.strftime("%Y-%m")


def _calc_duracion_horas(apertura, cierre) -> Decimal | None:
    from decimal import Decimal

    if not apertura or not cierre:
        return None
    delta = cierre - apertura
    hours = Decimal(str(delta.total_seconds())) / Decimal("3600")
    return hours.quantize(Decimal("0.01")) if hours >= 0 else None


def _preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)
    require_any(
        df,
        [
            ["ticket_externo_id", "codigo", "ticket", "id", "folio", "no_ticket"],
            ["titulo", "asunto", "descripcion", "descripcion_corta", "tema"],
        ],
    )
    return df


def import_tickets(user, uploaded_file):
    uploaded_file.seek(0)

    def handler(row: pd.Series, errors: list[str], batch=None):
        ticket_id = pick(
            row,
            "ticket_externo_id",
            "codigo",
            "ticket",
            "id",
            "folio",
            "no_ticket",
            "id_ticket",
        )
        titulo = pick(row, "titulo", "asunto", "descripcion", "descripcion_corta", "tema")
        if not titulo:
            errors.append("Título obligatorio.")
            return None
        fecha_apertura = _parse_dt(
            pick(row, "fecha_apertura", "fecha_creacion", "creado", "apertura", "fecha_inicio")
        )
        fecha_cierre = _parse_dt(
            pick(row, "fecha_cierre", "cerrado", "fecha_resolucion", "fecha_fin")
        )
        fecha_registro = _parse_dt(pick(row, "fecha_registro", "fecha_alta")) or fecha_apertura
        estado_raw = pick(row, "estado", "status", "estado_ticket")
        estado_norm = _normalize_estado(estado_raw)
        if fecha_cierre and estado_norm == "abierto":
            estado_norm = "cerrado"
        duracion = pick_decimal(row, "duracion_horas", "duracion", "tiempo_horas")
        if duracion == 0 and fecha_apertura and fecha_cierre:
            duracion = _calc_duracion_horas(fecha_apertura, fecha_cierre) or duracion
        sla_horas = pick_decimal(row, "sla_horas", "sla", default="48")
        sla_cumplido = False
        if duracion and sla_horas:
            sla_cumplido = duracion <= sla_horas
        unidad = resolve_unidad(
            pick(row, "unidad_negocio", "unidad", "departamento", "area") or "TI"
        )
        responsable = None
        username = pick(row, "asignado", "asignado_a", "responsable", "tecnico", "agente")
        if username:
            responsable = User.objects.filter(username__iexact=username.split()[0]).first()
        anio_mes = pick(row, "anio_mes", "periodo", "mes") or _periodo_from_dt(
            fecha_apertura or fecha_registro
        )
        defaults = {
            "usuario_solicita": pick(row, "usuario_solicita", "solicitante", "usuario"),
            "correo_solicita": pick(row, "correo_solicita", "correo", "email"),
            "departamento": pick(row, "departamento", "area"),
            "tipo": pick(row, "tipo", "tipo_ticket"),
            "titulo": titulo[:255],
            "estado_raw": estado_raw,
            "estado_normalizado": estado_norm,
            "solucion": pick(row, "solucion", "resolucion", "detalle"),
            "fecha_cierre": fecha_cierre,
            "fecha_apertura": fecha_apertura,
            "fecha_registro": fecha_registro,
            "prioridad": pick(row, "prioridad", "prioridad_ticket"),
            "tipo_servicio": pick(row, "tipo_servicio", "servicio"),
            "razon_cierre": pick(row, "razon_cierre", "motivo_cierre"),
            "sistema": pick(row, "sistema", "aplicacion"),
            "elemento": pick(row, "elemento"),
            "ruta": pick(row, "ruta"),
            "anio_mes": anio_mes[:7] if anio_mes else "",
            "duracion_horas": duracion if duracion else None,
            "sla_horas": sla_horas,
            "sla_cumplido": sla_cumplido,
            "unidad_negocio": unidad,
            "responsable": responsable,
            "import_batch": batch,
            "payload_raw_json": row_to_json(row),
        }
        if ticket_id:
            obj, created = PgoTicket.objects.update_or_create(
                ticket_externo_id=str(ticket_id),
                defaults=defaults,
            )
            return created, not created
        if not fecha_registro:
            errors.append("Sin ticket_externo_id se requiere fecha_registro o fecha_apertura.")
            return None
        existing = PgoTicket.objects.filter(titulo=titulo, fecha_registro=fecha_registro).first()
        if existing:
            for key, value in defaults.items():
                setattr(existing, key, value)
            existing.save()
            return False, True
        PgoTicket.objects.create(ticket_externo_id="", **defaults)
        return True, False

    return run_import_batch(
        user=user,
        modulo=MODULO,
        tipo_importacion=TIPO,
        uploaded_file=uploaded_file,
        preprocess=_preprocess,
        row_handler=handler,
    )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Importador PGO: tickets desde CSV/XLSX."""
00002|
00003|from __future__ import annotations
00004|
00005|from datetime import datetime
00006|
00007|import pandas as pd
00008|from django.contrib.auth import get_user_model
00009|from django.utils import timezone
00010|
00011|from apps.core.imports.base import run_import_batch, row_to_json
00012|from apps.core.imports.columns import normalize_columns, pick, pick_decimal, pick_int, require_any
00013|from apps.core.imports.entities import resolve_unidad
00014|from apps.pgo.models import PgoTicket
00015|
00016|User = get_user_model()
00017|
00018|MODULO = "pgo"
00019|TIPO = "tickets"
00020|
00021|
00022|def _parse_dt(value: str):
00023|    if not value:
00024|        return None
00025|    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y %H:%M", "%d/%m/%Y", "%m/%d/%Y"):
00026|        try:
00027|            dt = datetime.strptime(value[:19], fmt)
00028|            return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
00029|        except ValueError:
00030|            continue
00031|    try:
00032|        dt = pd.to_datetime(value).to_pydatetime()
00033|        return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
00034|    except Exception:
00035|        return None
00036|
00037|
00038|def _normalize_estado(raw: str) -> str:
00039|    s = raw.lower()
00040|    if any(k in s for k in ("cerr", "close", "resuel", "done")):
00041|        return "cerrado"
00042|    if any(k in s for k in ("proces", "progress", "curso")):
00043|        return "en_proceso"
00044|    if any(k in s for k in ("rechaz", "cancel")):
00045|        return "rechazado"
00046|    return "abierto"
00047|
00048|
00049|def _periodo_from_dt(dt) -> str:
00050|    if not dt:
00051|        return ""
00052|    return dt.strftime("%Y-%m")
00053|
00054|
00055|def _calc_duracion_horas(apertura, cierre) -> Decimal | None:
00056|    from decimal import Decimal
00057|
00058|    if not apertura or not cierre:
00059|        return None
00060|    delta = cierre - apertura
00061|    hours = Decimal(str(delta.total_seconds())) / Decimal("3600")
00062|    return hours.quantize(Decimal("0.01")) if hours >= 0 else None
00063|
00064|
00065|def _preprocess(df: pd.DataFrame) -> pd.DataFrame:
00066|    df = normalize_columns(df)
00067|    require_any(
00068|        df,
00069|        [
00070|            ["ticket_externo_id", "codigo", "ticket", "id", "folio", "no_ticket"],
00071|            ["titulo", "asunto", "descripcion", "descripcion_corta", "tema"],
00072|        ],
00073|    )
00074|    return df
00075|
00076|
00077|def import_tickets(user, uploaded_file):
00078|    uploaded_file.seek(0)
00079|
00080|    def handler(row: pd.Series, errors: list[str], batch=None):
00081|        ticket_id = pick(
00082|            row,
00083|            "ticket_externo_id",
00084|            "codigo",
00085|            "ticket",
00086|            "id",
00087|            "folio",
00088|            "no_ticket",
00089|            "id_ticket",
00090|        )
00091|        titulo = pick(row, "titulo", "asunto", "descripcion", "descripcion_corta", "tema")
00092|        if not titulo:
00093|            errors.append("Título obligatorio.")
00094|            return None
00095|        fecha_apertura = _parse_dt(
00096|            pick(row, "fecha_apertura", "fecha_creacion", "creado", "apertura", "fecha_inicio")
00097|        )
00098|        fecha_cierre = _parse_dt(
00099|            pick(row, "fecha_cierre", "cerrado", "fecha_resolucion", "fecha_fin")
00100|        )
00101|        fecha_registro = _parse_dt(pick(row, "fecha_registro", "fecha_alta")) or fecha_apertura
00102|        estado_raw = pick(row, "estado", "status", "estado_ticket")
00103|        estado_norm = _normalize_estado(estado_raw)
00104|        if fecha_cierre and estado_norm == "abierto":
00105|            estado_norm = "cerrado"
00106|        duracion = pick_decimal(row, "duracion_horas", "duracion", "tiempo_horas")
00107|        if duracion == 0 and fecha_apertura and fecha_cierre:
00108|            duracion = _calc_duracion_horas(fecha_apertura, fecha_cierre) or duracion
00109|        sla_horas = pick_decimal(row, "sla_horas", "sla", default="48")
00110|        sla_cumplido = False
00111|        if duracion and sla_horas:
00112|            sla_cumplido = duracion <= sla_horas
00113|        unidad = resolve_unidad(
00114|            pick(row, "unidad_negocio", "unidad", "departamento", "area") or "TI"
00115|        )
00116|        responsable = None
00117|        username = pick(row, "asignado", "asignado_a", "responsable", "tecnico", "agente")
00118|        if username:
00119|            responsable = User.objects.filter(username__iexact=username.split()[0]).first()
00120|        anio_mes = pick(row, "anio_mes", "periodo", "mes") or _periodo_from_dt(
00121|            fecha_apertura or fecha_registro
00122|        )
00123|        defaults = {
00124|            "usuario_solicita": pick(row, "usuario_solicita", "solicitante", "usuario"),
00125|            "correo_solicita": pick(row, "correo_solicita", "correo", "email"),
00126|            "departamento": pick(row, "departamento", "area"),
00127|            "tipo": pick(row, "tipo", "tipo_ticket"),
00128|            "titulo": titulo[:255],
00129|            "estado_raw": estado_raw,
00130|            "estado_normalizado": estado_norm,
00131|            "solucion": pick(row, "solucion", "resolucion", "detalle"),
00132|            "fecha_cierre": fecha_cierre,
00133|            "fecha_apertura": fecha_apertura,
00134|            "fecha_registro": fecha_registro,
00135|            "prioridad": pick(row, "prioridad", "prioridad_ticket"),
00136|            "tipo_servicio": pick(row, "tipo_servicio", "servicio"),
00137|            "razon_cierre": pick(row, "razon_cierre", "motivo_cierre"),
00138|            "sistema": pick(row, "sistema", "aplicacion"),
00139|            "elemento": pick(row, "elemento"),
00140|            "ruta": pick(row, "ruta"),
00141|            "anio_mes": anio_mes[:7] if anio_mes else "",
00142|            "duracion_horas": duracion if duracion else None,
00143|            "sla_horas": sla_horas,
00144|            "sla_cumplido": sla_cumplido,
00145|            "unidad_negocio": unidad,
00146|            "responsable": responsable,
00147|            "import_batch": batch,
00148|            "payload_raw_json": row_to_json(row),
00149|        }
00150|        if ticket_id:
00151|            obj, created = PgoTicket.objects.update_or_create(
00152|                ticket_externo_id=str(ticket_id),
00153|                defaults=defaults,
00154|            )
00155|            return created, not created
00156|        if not fecha_registro:
00157|            errors.append("Sin ticket_externo_id se requiere fecha_registro o fecha_apertura.")
00158|            return None
00159|        existing = PgoTicket.objects.filter(titulo=titulo, fecha_registro=fecha_registro).first()
00160|        if existing:
00161|            for key, value in defaults.items():
00162|                setattr(existing, key, value)
00163|            existing.save()
00164|            return False, True
00165|        PgoTicket.objects.create(ticket_externo_id="", **defaults)
00166|        return True, False
00167|
00168|    return run_import_batch(
00169|        user=user,
00170|        modulo=MODULO,
00171|        tipo_importacion=TIPO,
00172|        uploaded_file=uploaded_file,
00173|        preprocess=_preprocess,
00174|        row_handler=handler,
00175|    )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiSW1wb3J0YWRvciBQR086IHRpY2tldHMgZGVzZGUgQ1NWL1hMU1guIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgpmcm9tIGRhdGV0aW1lIGltcG9ydCBkYXRldGltZQoKaW1wb3J0IHBhbmRhcyBhcyBwZApmcm9tIGRqYW5nby5jb250cmliLmF1dGggaW1wb3J0IGdldF91c2VyX21vZGVsCmZyb20gZGphbmdvLnV0aWxzIGltcG9ydCB0aW1lem9uZQoKZnJvbSBhcHBzLmNvcmUuaW1wb3J0cy5iYXNlIGltcG9ydCBydW5faW1wb3J0X2JhdGNoLCByb3dfdG9fanNvbgpmcm9tIGFwcHMuY29yZS5pbXBvcnRzLmNvbHVtbnMgaW1wb3J0IG5vcm1hbGl6ZV9jb2x1bW5zLCBwaWNrLCBwaWNrX2RlY2ltYWwsIHBpY2tfaW50LCByZXF1aXJlX2FueQpmcm9tIGFwcHMuY29yZS5pbXBvcnRzLmVudGl0aWVzIGltcG9ydCByZXNvbHZlX3VuaWRhZApmcm9tIGFwcHMucGdvLm1vZGVscyBpbXBvcnQgUGdvVGlja2V0CgpVc2VyID0gZ2V0X3VzZXJfbW9kZWwoKQoKTU9EVUxPID0gInBnbyIKVElQTyA9ICJ0aWNrZXRzIgoKCmRlZiBfcGFyc2VfZHQodmFsdWU6IHN0cik6CiAgICBpZiBub3QgdmFsdWU6CiAgICAgICAgcmV0dXJuIE5vbmUKICAgIGZvciBmbXQgaW4gKCIlWS0lbS0lZCAlSDolTTolUyIsICIlWS0lbS0lZCIsICIlZC8lbS8lWSAlSDolTSIsICIlZC8lbS8lWSIsICIlbS8lZC8lWSIpOgogICAgICAgIHRyeToKICAgICAgICAgICAgZHQgPSBkYXRldGltZS5zdHJwdGltZSh2YWx1ZVs6MTldLCBmbXQpCiAgICAgICAgICAgIHJldHVybiB0aW1lem9uZS5tYWtlX2F3YXJlKGR0KSBpZiB0aW1lem9uZS5pc19uYWl2ZShkdCkgZWxzZSBkdAogICAgICAgIGV4Y2VwdCBWYWx1ZUVycm9yOgogICAgICAgICAgICBjb250aW51ZQogICAgdHJ5OgogICAgICAgIGR0ID0gcGQudG9fZGF0ZXRpbWUodmFsdWUpLnRvX3B5ZGF0ZXRpbWUoKQogICAgICAgIHJldHVybiB0aW1lem9uZS5tYWtlX2F3YXJlKGR0KSBpZiB0aW1lem9uZS5pc19uYWl2ZShkdCkgZWxzZSBkdAogICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICByZXR1cm4gTm9uZQoKCmRlZiBfbm9ybWFsaXplX2VzdGFkbyhyYXc6IHN0cikgLT4gc3RyOgogICAgcyA9IHJhdy5sb3dlcigpCiAgICBpZiBhbnkoayBpbiBzIGZvciBrIGluICgiY2VyciIsICJjbG9zZSIsICJyZXN1ZWwiLCAiZG9uZSIpKToKICAgICAgICByZXR1cm4gImNlcnJhZG8iCiAgICBpZiBhbnkoayBpbiBzIGZvciBrIGluICgicHJvY2VzIiwgInByb2dyZXNzIiwgImN1cnNvIikpOgogICAgICAgIHJldHVybiAiZW5fcHJvY2VzbyIKICAgIGlmIGFueShrIGluIHMgZm9yIGsgaW4gKCJyZWNoYXoiLCAiY2FuY2VsIikpOgogICAgICAgIHJldHVybiAicmVjaGF6YWRvIgogICAgcmV0dXJuICJhYmllcnRvIgoKCmRlZiBfcGVyaW9kb19mcm9tX2R0KGR0KSAtPiBzdHI6CiAgICBpZiBub3QgZHQ6CiAgICAgICAgcmV0dXJuICIiCiAgICByZXR1cm4gZHQuc3RyZnRpbWUoIiVZLSVtIikKCgpkZWYgX2NhbGNfZHVyYWNpb25faG9yYXMoYXBlcnR1cmEsIGNpZXJyZSkgLT4gRGVjaW1hbCB8IE5vbmU6CiAgICBmcm9tIGRlY2ltYWwgaW1wb3J0IERlY2ltYWwKCiAgICBpZiBub3QgYXBlcnR1cmEgb3Igbm90IGNpZXJyZToKICAgICAgICByZXR1cm4gTm9uZQogICAgZGVsdGEgPSBjaWVycmUgLSBhcGVydHVyYQogICAgaG91cnMgPSBEZWNpbWFsKHN0cihkZWx0YS50b3RhbF9zZWNvbmRzKCkpKSAvIERlY2ltYWwoIjM2MDAiKQogICAgcmV0dXJuIGhvdXJzLnF1YW50aXplKERlY2ltYWwoIjAuMDEiKSkgaWYgaG91cnMgPj0gMCBlbHNlIE5vbmUKCgpkZWYgX3ByZXByb2Nlc3MoZGY6IHBkLkRhdGFGcmFtZSkgLT4gcGQuRGF0YUZyYW1lOgogICAgZGYgPSBub3JtYWxpemVfY29sdW1ucyhkZikKICAgIHJlcXVpcmVfYW55KAogICAgICAgIGRmLAogICAgICAgIFsKICAgICAgICAgICAgWyJ0aWNrZXRfZXh0ZXJub19pZCIsICJjb2RpZ28iLCAidGlja2V0IiwgImlkIiwgImZvbGlvIiwgIm5vX3RpY2tldCJdLAogICAgICAgICAgICBbInRpdHVsbyIsICJhc3VudG8iLCAiZGVzY3JpcGNpb24iLCAiZGVzY3JpcGNpb25fY29ydGEiLCAidGVtYSJdLAogICAgICAgIF0sCiAgICApCiAgICByZXR1cm4gZGYKCgpkZWYgaW1wb3J0X3RpY2tldHModXNlciwgdXBsb2FkZWRfZmlsZSk6CiAgICB1cGxvYWRlZF9maWxlLnNlZWsoMCkKCiAgICBkZWYgaGFuZGxlcihyb3c6IHBkLlNlcmllcywgZXJyb3JzOiBsaXN0W3N0cl0sIGJhdGNoPU5vbmUpOgogICAgICAgIHRpY2tldF9pZCA9IHBpY2soCiAgICAgICAgICAgIHJvdywKICAgICAgICAgICAgInRpY2tldF9leHRlcm5vX2lkIiwKICAgICAgICAgICAgImNvZGlnbyIsCiAgICAgICAgICAgICJ0aWNrZXQiLAogICAgICAgICAgICAiaWQiLAogICAgICAgICAgICAiZm9saW8iLAogICAgICAgICAgICAibm9fdGlja2V0IiwKICAgICAgICAgICAgImlkX3RpY2tldCIsCiAgICAgICAgKQogICAgICAgIHRpdHVsbyA9IHBpY2socm93LCAidGl0dWxvIiwgImFzdW50byIsICJkZXNjcmlwY2lvbiIsICJkZXNjcmlwY2lvbl9jb3J0YSIsICJ0ZW1hIikKICAgICAgICBpZiBub3QgdGl0dWxvOgogICAgICAgICAgICBlcnJvcnMuYXBwZW5kKCJUw610dWxvIG9ibGlnYXRvcmlvLiIpCiAgICAgICAgICAgIHJldHVybiBOb25lCiAgICAgICAgZmVjaGFfYXBlcnR1cmEgPSBfcGFyc2VfZHQoCiAgICAgICAgICAgIHBpY2socm93LCAiZmVjaGFfYXBlcnR1cmEiLCAiZmVjaGFfY3JlYWNpb24iLCAiY3JlYWRvIiwgImFwZXJ0dXJhIiwgImZlY2hhX2luaWNpbyIpCiAgICAgICAgKQogICAgICAgIGZlY2hhX2NpZXJyZSA9IF9wYXJzZV9kdCgKICAgICAgICAgICAgcGljayhyb3csICJmZWNoYV9jaWVycmUiLCAiY2VycmFkbyIsICJmZWNoYV9yZXNvbHVjaW9uIiwgImZlY2hhX2ZpbiIpCiAgICAgICAgKQogICAgICAgIGZlY2hhX3JlZ2lzdHJvID0gX3BhcnNlX2R0KHBpY2socm93LCAiZmVjaGFfcmVnaXN0cm8iLCAiZmVjaGFfYWx0YSIpKSBvciBmZWNoYV9hcGVydHVyYQogICAgICAgIGVzdGFkb19yYXcgPSBwaWNrKHJvdywgImVzdGFkbyIsICJzdGF0dXMiLCAiZXN0YWRvX3RpY2tldCIpCiAgICAgICAgZXN0YWRvX25vcm0gPSBfbm9ybWFsaXplX2VzdGFkbyhlc3RhZG9fcmF3KQogICAgICAgIGlmIGZlY2hhX2NpZXJyZSBhbmQgZXN0YWRvX25vcm0gPT0gImFiaWVydG8iOgogICAgICAgICAgICBlc3RhZG9fbm9ybSA9ICJjZXJyYWRvIgogICAgICAgIGR1cmFjaW9uID0gcGlja19kZWNpbWFsKHJvdywgImR1cmFjaW9uX2hvcmFzIiwgImR1cmFjaW9uIiwgInRpZW1wb19ob3JhcyIpCiAgICAgICAgaWYgZHVyYWNpb24gPT0gMCBhbmQgZmVjaGFfYXBlcnR1cmEgYW5kIGZlY2hhX2NpZXJyZToKICAgICAgICAgICAgZHVyYWNpb24gPSBfY2FsY19kdXJhY2lvbl9ob3JhcyhmZWNoYV9hcGVydHVyYSwgZmVjaGFfY2llcnJlKSBvciBkdXJhY2lvbgogICAgICAgIHNsYV9ob3JhcyA9IHBpY2tfZGVjaW1hbChyb3csICJzbGFfaG9yYXMiLCAic2xhIiwgZGVmYXVsdD0iNDgiKQogICAgICAgIHNsYV9jdW1wbGlkbyA9IEZhbHNlCiAgICAgICAgaWYgZHVyYWNpb24gYW5kIHNsYV9ob3JhczoKICAgICAgICAgICAgc2xhX2N1bXBsaWRvID0gZHVyYWNpb24gPD0gc2xhX2hvcmFzCiAgICAgICAgdW5pZGFkID0gcmVzb2x2ZV91bmlkYWQoCiAgICAgICAgICAgIHBpY2socm93LCAidW5pZGFkX25lZ29jaW8iLCAidW5pZGFkIiwgImRlcGFydGFtZW50byIsICJhcmVhIikgb3IgIlRJIgogICAgICAgICkKICAgICAgICByZXNwb25zYWJsZSA9IE5vbmUKICAgICAgICB1c2VybmFtZSA9IHBpY2socm93LCAiYXNpZ25hZG8iLCAiYXNpZ25hZG9fYSIsICJyZXNwb25zYWJsZSIsICJ0ZWNuaWNvIiwgImFnZW50ZSIpCiAgICAgICAgaWYgdXNlcm5hbWU6CiAgICAgICAgICAgIHJlc3BvbnNhYmxlID0gVXNlci5vYmplY3RzLmZpbHRlcih1c2VybmFtZV9faWV4YWN0PXVzZXJuYW1lLnNwbGl0KClbMF0pLmZpcnN0KCkKICAgICAgICBhbmlvX21lcyA9IHBpY2socm93LCAiYW5pb19tZXMiLCAicGVyaW9kbyIsICJtZXMiKSBvciBfcGVyaW9kb19mcm9tX2R0KAogICAgICAgICAgICBmZWNoYV9hcGVydHVyYSBvciBmZWNoYV9yZWdpc3RybwogICAgICAgICkKICAgICAgICBkZWZhdWx0cyA9IHsKICAgICAgICAgICAgInVzdWFyaW9fc29saWNpdGEiOiBwaWNrKHJvdywgInVzdWFyaW9fc29saWNpdGEiLCAic29saWNpdGFudGUiLCAidXN1YXJpbyIpLAogICAgICAgICAgICAiY29ycmVvX3NvbGljaXRhIjogcGljayhyb3csICJjb3JyZW9fc29saWNpdGEiLCAiY29ycmVvIiwgImVtYWlsIiksCiAgICAgICAgICAgICJkZXBhcnRhbWVudG8iOiBwaWNrKHJvdywgImRlcGFydGFtZW50byIsICJhcmVhIiksCiAgICAgICAgICAgICJ0aXBvIjogcGljayhyb3csICJ0aXBvIiwgInRpcG9fdGlja2V0IiksCiAgICAgICAgICAgICJ0aXR1bG8iOiB0aXR1bG9bOjI1NV0sCiAgICAgICAgICAgICJlc3RhZG9fcmF3IjogZXN0YWRvX3JhdywKICAgICAgICAgICAgImVzdGFkb19ub3JtYWxpemFkbyI6IGVzdGFkb19ub3JtLAogICAgICAgICAgICAic29sdWNpb24iOiBwaWNrKHJvdywgInNvbHVjaW9uIiwgInJlc29sdWNpb24iLCAiZGV0YWxsZSIpLAogICAgICAgICAgICAiZmVjaGFfY2llcnJlIjogZmVjaGFfY2llcnJlLAogICAgICAgICAgICAiZmVjaGFfYXBlcnR1cmEiOiBmZWNoYV9hcGVydHVyYSwKICAgICAgICAgICAgImZlY2hhX3JlZ2lzdHJvIjogZmVjaGFfcmVnaXN0cm8sCiAgICAgICAgICAgICJwcmlvcmlkYWQiOiBwaWNrKHJvdywgInByaW9yaWRhZCIsICJwcmlvcmlkYWRfdGlja2V0IiksCiAgICAgICAgICAgICJ0aXBvX3NlcnZpY2lvIjogcGljayhyb3csICJ0aXBvX3NlcnZpY2lvIiwgInNlcnZpY2lvIiksCiAgICAgICAgICAgICJyYXpvbl9jaWVycmUiOiBwaWNrKHJvdywgInJhem9uX2NpZXJyZSIsICJtb3Rpdm9fY2llcnJlIiksCiAgICAgICAgICAgICJzaXN0ZW1hIjogcGljayhyb3csICJzaXN0ZW1hIiwgImFwbGljYWNpb24iKSwKICAgICAgICAgICAgImVsZW1lbnRvIjogcGljayhyb3csICJlbGVtZW50byIpLAogICAgICAgICAgICAicnV0YSI6IHBpY2socm93LCAicnV0YSIpLAogICAgICAgICAgICAiYW5pb19tZXMiOiBhbmlvX21lc1s6N10gaWYgYW5pb19tZXMgZWxzZSAiIiwKICAgICAgICAgICAgImR1cmFjaW9uX2hvcmFzIjogZHVyYWNpb24gaWYgZHVyYWNpb24gZWxzZSBOb25lLAogICAgICAgICAgICAic2xhX2hvcmFzIjogc2xhX2hvcmFzLAogICAgICAgICAgICAic2xhX2N1bXBsaWRvIjogc2xhX2N1bXBsaWRvLAogICAgICAgICAgICAidW5pZGFkX25lZ29jaW8iOiB1bmlkYWQsCiAgICAgICAgICAgICJyZXNwb25zYWJsZSI6IHJlc3BvbnNhYmxlLAogICAgICAgICAgICAiaW1wb3J0X2JhdGNoIjogYmF0Y2gsCiAgICAgICAgICAgICJwYXlsb2FkX3Jhd19qc29uIjogcm93X3RvX2pzb24ocm93KSwKICAgICAgICB9CiAgICAgICAgaWYgdGlja2V0X2lkOgogICAgICAgICAgICBvYmosIGNyZWF0ZWQgPSBQZ29UaWNrZXQub2JqZWN0cy51cGRhdGVfb3JfY3JlYXRlKAogICAgICAgICAgICAgICAgdGlja2V0X2V4dGVybm9faWQ9c3RyKHRpY2tldF9pZCksCiAgICAgICAgICAgICAgICBkZWZhdWx0cz1kZWZhdWx0cywKICAgICAgICAgICAgKQogICAgICAgICAgICByZXR1cm4gY3JlYXRlZCwgbm90IGNyZWF0ZWQKICAgICAgICBpZiBub3QgZmVjaGFfcmVnaXN0cm86CiAgICAgICAgICAgIGVycm9ycy5hcHBlbmQoIlNpbiB0aWNrZXRfZXh0ZXJub19pZCBzZSByZXF1aWVyZSBmZWNoYV9yZWdpc3RybyBvIGZlY2hhX2FwZXJ0dXJhLiIpCiAgICAgICAgICAgIHJldHVybiBOb25lCiAgICAgICAgZXhpc3RpbmcgPSBQZ29UaWNrZXQub2JqZWN0cy5maWx0ZXIodGl0dWxvPXRpdHVsbywgZmVjaGFfcmVnaXN0cm89ZmVjaGFfcmVnaXN0cm8pLmZpcnN0KCkKICAgICAgICBpZiBleGlzdGluZzoKICAgICAgICAgICAgZm9yIGtleSwgdmFsdWUgaW4gZGVmYXVsdHMuaXRlbXMoKToKICAgICAgICAgICAgICAgIHNldGF0dHIoZXhpc3RpbmcsIGtleSwgdmFsdWUpCiAgICAgICAgICAgIGV4aXN0aW5nLnNhdmUoKQogICAgICAgICAgICByZXR1cm4gRmFsc2UsIFRydWUKICAgICAgICBQZ29UaWNrZXQub2JqZWN0cy5jcmVhdGUodGlja2V0X2V4dGVybm9faWQ9IiIsICoqZGVmYXVsdHMpCiAgICAgICAgcmV0dXJuIFRydWUsIEZhbHNlCgogICAgcmV0dXJuIHJ1bl9pbXBvcnRfYmF0Y2goCiAgICAgICAgdXNlcj11c2VyLAogICAgICAgIG1vZHVsbz1NT0RVTE8sCiAgICAgICAgdGlwb19pbXBvcnRhY2lvbj1USVBPLAogICAgICAgIHVwbG9hZGVkX2ZpbGU9dXBsb2FkZWRfZmlsZSwKICAgICAgICBwcmVwcm9jZXNzPV9wcmVwcm9jZXNzLAogICAgICAgIHJvd19oYW5kbGVyPWhhbmRsZXIsCiAgICApCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/pgo/models.py
PATH_JSON="apps/pgo/models.py"
FILENAME=models.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=153
SIZE_BYTES_UTF8=5881
CONTENT_SHA256=60ee86ba23faaf96cb021959bbf99f94614982c9c81c489e01c97bb4c31cad64
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


class PgoTicket(models.Model):
    ticket_externo_id = models.CharField(max_length=100, blank=True, db_index=True)
    usuario_solicita = models.CharField(max_length=150, blank=True)
    correo_solicita = models.EmailField(blank=True)
    departamento = models.CharField(max_length=150, blank=True, db_index=True)
    tipo = models.CharField(max_length=100, blank=True)
    titulo = models.CharField(max_length=255)
    estado_raw = models.CharField(max_length=100, blank=True)
    estado_normalizado = models.CharField(max_length=50, blank=True, db_index=True)
    solucion = models.TextField(blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    fecha_apertura = models.DateTimeField(null=True, blank=True)
    fecha_registro = models.DateTimeField(null=True, blank=True)
    prioridad = models.CharField(max_length=50, blank=True, db_index=True)
    tipo_servicio = models.CharField(max_length=100, blank=True)
    razon_cierre = models.CharField(max_length=255, blank=True)
    sistema = models.CharField(max_length=100, blank=True, db_index=True)
    elemento = models.CharField(max_length=255, blank=True)
    ruta = models.CharField(max_length=255, blank=True)
    anio_mes = models.CharField(max_length=7, blank=True, db_index=True)
    duracion_horas = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sla_horas = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sla_cumplido = models.BooleanField(default=False)
    unidad_negocio = models.ForeignKey(
        "wcgone_core.UnidadNegocio",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_pgo_tickets",
    )
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_pgo_tickets",
    )
    import_batch = models.ForeignKey(
        "wcgone_core.DataImportBatch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_pgo_tickets",
    )
    payload_raw_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-fecha_apertura", "-id"]
        verbose_name = "Ticket PGO"
        verbose_name_plural = "Tickets PGO"

    def __str__(self):
        label = self.ticket_externo_id or str(self.pk)
        return f"{label} — {self.titulo}"


class PgoMetricRule(models.Model):
    TIPO_AUTOMATICA = "automatica"
    TIPO_MANUAL = "manual"
    TIPO_HIBRIDA = "hibrida"
    TIPO_CHOICES = [
        (TIPO_AUTOMATICA, "Automática"),
        (TIPO_MANUAL, "Manual"),
        (TIPO_HIBRIDA, "Híbrida"),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    area = models.CharField(max_length=100, blank=True)
    variable = models.CharField(max_length=100)
    criterio = models.TextField()
    unidad_negocio = models.ForeignKey(
        "wcgone_core.UnidadNegocio",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pgo_reglas",
    )
    puntos = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    peso = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    tipo_regla = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_AUTOMATICA)
    formula_texto = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["area", "codigo"]
        verbose_name = "Regla métrica PGO"
        verbose_name_plural = "Reglas métricas PGO"

    def __str__(self):
        return self.codigo


class PgoPeriodScore(models.Model):
    periodo = models.CharField(max_length=7, db_index=True)
    area = models.CharField(max_length=100, blank=True)
    unidad_negocio = models.ForeignKey(
        "wcgone_core.UnidadNegocio",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_pgo_period_scores",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcgone_pgo_period_scores",
    )
    puntaje_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    clasifica = models.BooleanField(default=False)
    detalle_json = models.JSONField(default=dict, blank=True)
    fecha_calculo = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-periodo", "area"]
        verbose_name = "Puntaje PGO por período"
        verbose_name_plural = "Puntajes PGO por período"

    def __str__(self):
        return f"{self.periodo} — {self.area or 'general'}"


class PgoMonthlyAgg(models.Model):
    periodo = models.CharField(max_length=7, db_index=True)
    unidad_negocio = models.ForeignKey(
        "wcgone_core.UnidadNegocio",
        on_delete=models.CASCADE,
        related_name="pgo_monthly_aggs",
    )
    departamento = models.CharField(max_length=150, blank=True)
    tickets_recibidos = models.PositiveIntegerField(default=0)
    tickets_cerrados = models.PositiveIntegerField(default=0)
    tiempo_promedio_horas = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sla_cumplidos = models.PositiveIntegerField(default=0)
    sla_incumplidos = models.PositiveIntegerField(default=0)
    tickets_abiertos_fin_mes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-periodo", "unidad_negocio__nombre"]
        verbose_name = "Agregado mensual PGO"
        verbose_name_plural = "Agregados mensuales PGO"
        indexes = [
            models.Index(fields=["periodo", "departamento"]),
        ]

    def __str__(self):
        return f"{self.periodo} — {self.unidad_negocio}"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.conf import settings
00002|from django.db import models
00003|
00004|
00005|class PgoTicket(models.Model):
00006|    ticket_externo_id = models.CharField(max_length=100, blank=True, db_index=True)
00007|    usuario_solicita = models.CharField(max_length=150, blank=True)
00008|    correo_solicita = models.EmailField(blank=True)
00009|    departamento = models.CharField(max_length=150, blank=True, db_index=True)
00010|    tipo = models.CharField(max_length=100, blank=True)
00011|    titulo = models.CharField(max_length=255)
00012|    estado_raw = models.CharField(max_length=100, blank=True)
00013|    estado_normalizado = models.CharField(max_length=50, blank=True, db_index=True)
00014|    solucion = models.TextField(blank=True)
00015|    fecha_cierre = models.DateTimeField(null=True, blank=True)
00016|    fecha_apertura = models.DateTimeField(null=True, blank=True)
00017|    fecha_registro = models.DateTimeField(null=True, blank=True)
00018|    prioridad = models.CharField(max_length=50, blank=True, db_index=True)
00019|    tipo_servicio = models.CharField(max_length=100, blank=True)
00020|    razon_cierre = models.CharField(max_length=255, blank=True)
00021|    sistema = models.CharField(max_length=100, blank=True, db_index=True)
00022|    elemento = models.CharField(max_length=255, blank=True)
00023|    ruta = models.CharField(max_length=255, blank=True)
00024|    anio_mes = models.CharField(max_length=7, blank=True, db_index=True)
00025|    duracion_horas = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
00026|    sla_horas = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
00027|    sla_cumplido = models.BooleanField(default=False)
00028|    unidad_negocio = models.ForeignKey(
00029|        "wcgone_core.UnidadNegocio",
00030|        on_delete=models.SET_NULL,
00031|        null=True,
00032|        blank=True,
00033|        related_name="wcgone_pgo_tickets",
00034|    )
00035|    responsable = models.ForeignKey(
00036|        settings.AUTH_USER_MODEL,
00037|        on_delete=models.SET_NULL,
00038|        null=True,
00039|        blank=True,
00040|        related_name="wcgone_pgo_tickets",
00041|    )
00042|    import_batch = models.ForeignKey(
00043|        "wcgone_core.DataImportBatch",
00044|        on_delete=models.SET_NULL,
00045|        null=True,
00046|        blank=True,
00047|        related_name="wcgone_pgo_tickets",
00048|    )
00049|    payload_raw_json = models.JSONField(default=dict, blank=True)
00050|
00051|    class Meta:
00052|        ordering = ["-fecha_apertura", "-id"]
00053|        verbose_name = "Ticket PGO"
00054|        verbose_name_plural = "Tickets PGO"
00055|
00056|    def __str__(self):
00057|        label = self.ticket_externo_id or str(self.pk)
00058|        return f"{label} — {self.titulo}"
00059|
00060|
00061|class PgoMetricRule(models.Model):
00062|    TIPO_AUTOMATICA = "automatica"
00063|    TIPO_MANUAL = "manual"
00064|    TIPO_HIBRIDA = "hibrida"
00065|    TIPO_CHOICES = [
00066|        (TIPO_AUTOMATICA, "Automática"),
00067|        (TIPO_MANUAL, "Manual"),
00068|        (TIPO_HIBRIDA, "Híbrida"),
00069|    ]
00070|
00071|    codigo = models.CharField(max_length=50, unique=True)
00072|    area = models.CharField(max_length=100, blank=True)
00073|    variable = models.CharField(max_length=100)
00074|    criterio = models.TextField()
00075|    unidad_negocio = models.ForeignKey(
00076|        "wcgone_core.UnidadNegocio",
00077|        on_delete=models.SET_NULL,
00078|        null=True,
00079|        blank=True,
00080|        related_name="pgo_reglas",
00081|    )
00082|    puntos = models.DecimalField(max_digits=8, decimal_places=2, default=0)
00083|    peso = models.DecimalField(max_digits=8, decimal_places=2, default=1)
00084|    tipo_regla = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_AUTOMATICA)
00085|    formula_texto = models.TextField(blank=True)
00086|    activo = models.BooleanField(default=True)
00087|    notas = models.TextField(blank=True)
00088|
00089|    class Meta:
00090|        ordering = ["area", "codigo"]
00091|        verbose_name = "Regla métrica PGO"
00092|        verbose_name_plural = "Reglas métricas PGO"
00093|
00094|    def __str__(self):
00095|        return self.codigo
00096|
00097|
00098|class PgoPeriodScore(models.Model):
00099|    periodo = models.CharField(max_length=7, db_index=True)
00100|    area = models.CharField(max_length=100, blank=True)
00101|    unidad_negocio = models.ForeignKey(
00102|        "wcgone_core.UnidadNegocio",
00103|        on_delete=models.SET_NULL,
00104|        null=True,
00105|        blank=True,
00106|        related_name="wcgone_pgo_period_scores",
00107|    )
00108|    usuario = models.ForeignKey(
00109|        settings.AUTH_USER_MODEL,
00110|        on_delete=models.SET_NULL,
00111|        null=True,
00112|        blank=True,
00113|        related_name="wcgone_pgo_period_scores",
00114|    )
00115|    puntaje_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
00116|    clasifica = models.BooleanField(default=False)
00117|    detalle_json = models.JSONField(default=dict, blank=True)
00118|    fecha_calculo = models.DateTimeField(auto_now_add=True)
00119|
00120|    class Meta:
00121|        ordering = ["-periodo", "area"]
00122|        verbose_name = "Puntaje PGO por período"
00123|        verbose_name_plural = "Puntajes PGO por período"
00124|
00125|    def __str__(self):
00126|        return f"{self.periodo} — {self.area or 'general'}"
00127|
00128|
00129|class PgoMonthlyAgg(models.Model):
00130|    periodo = models.CharField(max_length=7, db_index=True)
00131|    unidad_negocio = models.ForeignKey(
00132|        "wcgone_core.UnidadNegocio",
00133|        on_delete=models.CASCADE,
00134|        related_name="pgo_monthly_aggs",
00135|    )
00136|    departamento = models.CharField(max_length=150, blank=True)
00137|    tickets_recibidos = models.PositiveIntegerField(default=0)
00138|    tickets_cerrados = models.PositiveIntegerField(default=0)
00139|    tiempo_promedio_horas = models.DecimalField(max_digits=12, decimal_places=2, default=0)
00140|    sla_cumplidos = models.PositiveIntegerField(default=0)
00141|    sla_incumplidos = models.PositiveIntegerField(default=0)
00142|    tickets_abiertos_fin_mes = models.PositiveIntegerField(default=0)
00143|
00144|    class Meta:
00145|        ordering = ["-periodo", "unidad_negocio__nombre"]
00146|        verbose_name = "Agregado mensual PGO"
00147|        verbose_name_plural = "Agregados mensuales PGO"
00148|        indexes = [
00149|            models.Index(fields=["periodo", "departamento"]),
00150|        ]
00151|
00152|    def __str__(self):
00153|        return f"{self.periodo} — {self.unidad_negocio}"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29uZiBpbXBvcnQgc2V0dGluZ3MKZnJvbSBkamFuZ28uZGIgaW1wb3J0IG1vZGVscwoKCmNsYXNzIFBnb1RpY2tldChtb2RlbHMuTW9kZWwpOgogICAgdGlja2V0X2V4dGVybm9faWQgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAwLCBibGFuaz1UcnVlLCBkYl9pbmRleD1UcnVlKQogICAgdXN1YXJpb19zb2xpY2l0YSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xNTAsIGJsYW5rPVRydWUpCiAgICBjb3JyZW9fc29saWNpdGEgPSBtb2RlbHMuRW1haWxGaWVsZChibGFuaz1UcnVlKQogICAgZGVwYXJ0YW1lbnRvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTE1MCwgYmxhbms9VHJ1ZSwgZGJfaW5kZXg9VHJ1ZSkKICAgIHRpcG8gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAwLCBibGFuaz1UcnVlKQogICAgdGl0dWxvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTI1NSkKICAgIGVzdGFkb19yYXcgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAwLCBibGFuaz1UcnVlKQogICAgZXN0YWRvX25vcm1hbGl6YWRvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTUwLCBibGFuaz1UcnVlLCBkYl9pbmRleD1UcnVlKQogICAgc29sdWNpb24gPSBtb2RlbHMuVGV4dEZpZWxkKGJsYW5rPVRydWUpCiAgICBmZWNoYV9jaWVycmUgPSBtb2RlbHMuRGF0ZVRpbWVGaWVsZChudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBmZWNoYV9hcGVydHVyYSA9IG1vZGVscy5EYXRlVGltZUZpZWxkKG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIGZlY2hhX3JlZ2lzdHJvID0gbW9kZWxzLkRhdGVUaW1lRmllbGQobnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgcHJpb3JpZGFkID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTUwLCBibGFuaz1UcnVlLCBkYl9pbmRleD1UcnVlKQogICAgdGlwb19zZXJ2aWNpbyA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMDAsIGJsYW5rPVRydWUpCiAgICByYXpvbl9jaWVycmUgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MjU1LCBibGFuaz1UcnVlKQogICAgc2lzdGVtYSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMDAsIGJsYW5rPVRydWUsIGRiX2luZGV4PVRydWUpCiAgICBlbGVtZW50byA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yNTUsIGJsYW5rPVRydWUpCiAgICBydXRhID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTI1NSwgYmxhbms9VHJ1ZSkKICAgIGFuaW9fbWVzID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTcsIGJsYW5rPVRydWUsIGRiX2luZGV4PVRydWUpCiAgICBkdXJhY2lvbl9ob3JhcyA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xMiwgZGVjaW1hbF9wbGFjZXM9MiwgbnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgc2xhX2hvcmFzID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTEyLCBkZWNpbWFsX3BsYWNlcz0yLCBudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBzbGFfY3VtcGxpZG8gPSBtb2RlbHMuQm9vbGVhbkZpZWxkKGRlZmF1bHQ9RmFsc2UpCiAgICB1bmlkYWRfbmVnb2NpbyA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgICJ3Y2dvbmVfY29yZS5VbmlkYWROZWdvY2lvIiwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0id2Nnb25lX3Bnb190aWNrZXRzIiwKICAgICkKICAgIHJlc3BvbnNhYmxlID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgc2V0dGluZ3MuQVVUSF9VU0VSX01PREVMLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJ3Y2dvbmVfcGdvX3RpY2tldHMiLAogICAgKQogICAgaW1wb3J0X2JhdGNoID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgIndjZ29uZV9jb3JlLkRhdGFJbXBvcnRCYXRjaCIsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5TRVRfTlVMTCwKICAgICAgICBudWxsPVRydWUsCiAgICAgICAgYmxhbms9VHJ1ZSwKICAgICAgICByZWxhdGVkX25hbWU9IndjZ29uZV9wZ29fdGlja2V0cyIsCiAgICApCiAgICBwYXlsb2FkX3Jhd19qc29uID0gbW9kZWxzLkpTT05GaWVsZChkZWZhdWx0PWRpY3QsIGJsYW5rPVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICBvcmRlcmluZyA9IFsiLWZlY2hhX2FwZXJ0dXJhIiwgIi1pZCJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIlRpY2tldCBQR08iCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJUaWNrZXRzIFBHTyIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICBsYWJlbCA9IHNlbGYudGlja2V0X2V4dGVybm9faWQgb3Igc3RyKHNlbGYucGspCiAgICAgICAgcmV0dXJuIGYie2xhYmVsfSDigJQge3NlbGYudGl0dWxvfSIKCgpjbGFzcyBQZ29NZXRyaWNSdWxlKG1vZGVscy5Nb2RlbCk6CiAgICBUSVBPX0FVVE9NQVRJQ0EgPSAiYXV0b21hdGljYSIKICAgIFRJUE9fTUFOVUFMID0gIm1hbnVhbCIKICAgIFRJUE9fSElCUklEQSA9ICJoaWJyaWRhIgogICAgVElQT19DSE9JQ0VTID0gWwogICAgICAgIChUSVBPX0FVVE9NQVRJQ0EsICJBdXRvbcOhdGljYSIpLAogICAgICAgIChUSVBPX01BTlVBTCwgIk1hbnVhbCIpLAogICAgICAgIChUSVBPX0hJQlJJREEsICJIw61icmlkYSIpLAogICAgXQoKICAgIGNvZGlnbyA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD01MCwgdW5pcXVlPVRydWUpCiAgICBhcmVhID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwMCwgYmxhbms9VHJ1ZSkKICAgIHZhcmlhYmxlID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwMCkKICAgIGNyaXRlcmlvID0gbW9kZWxzLlRleHRGaWVsZCgpCiAgICB1bmlkYWRfbmVnb2NpbyA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgICJ3Y2dvbmVfY29yZS5VbmlkYWROZWdvY2lvIiwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0icGdvX3JlZ2xhcyIsCiAgICApCiAgICBwdW50b3MgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9OCwgZGVjaW1hbF9wbGFjZXM9MiwgZGVmYXVsdD0wKQogICAgcGVzbyA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz04LCBkZWNpbWFsX3BsYWNlcz0yLCBkZWZhdWx0PTEpCiAgICB0aXBvX3JlZ2xhID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTIwLCBjaG9pY2VzPVRJUE9fQ0hPSUNFUywgZGVmYXVsdD1USVBPX0FVVE9NQVRJQ0EpCiAgICBmb3JtdWxhX3RleHRvID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQogICAgYWN0aXZvID0gbW9kZWxzLkJvb2xlYW5GaWVsZChkZWZhdWx0PVRydWUpCiAgICBub3RhcyA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIG9yZGVyaW5nID0gWyJhcmVhIiwgImNvZGlnbyJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIlJlZ2xhIG3DqXRyaWNhIFBHTyIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIlJlZ2xhcyBtw6l0cmljYXMgUEdPIgoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBzZWxmLmNvZGlnbwoKCmNsYXNzIFBnb1BlcmlvZFNjb3JlKG1vZGVscy5Nb2RlbCk6CiAgICBwZXJpb2RvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTcsIGRiX2luZGV4PVRydWUpCiAgICBhcmVhID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwMCwgYmxhbms9VHJ1ZSkKICAgIHVuaWRhZF9uZWdvY2lvID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgIndjZ29uZV9jb3JlLlVuaWRhZE5lZ29jaW8iLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJ3Y2dvbmVfcGdvX3BlcmlvZF9zY29yZXMiLAogICAgKQogICAgdXN1YXJpbyA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIHNldHRpbmdzLkFVVEhfVVNFUl9NT0RFTCwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0id2Nnb25lX3Bnb19wZXJpb2Rfc2NvcmVzIiwKICAgICkKICAgIHB1bnRhamVfdG90YWwgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9OCwgZGVjaW1hbF9wbGFjZXM9MiwgZGVmYXVsdD0wKQogICAgY2xhc2lmaWNhID0gbW9kZWxzLkJvb2xlYW5GaWVsZChkZWZhdWx0PUZhbHNlKQogICAgZGV0YWxsZV9qc29uID0gbW9kZWxzLkpTT05GaWVsZChkZWZhdWx0PWRpY3QsIGJsYW5rPVRydWUpCiAgICBmZWNoYV9jYWxjdWxvID0gbW9kZWxzLkRhdGVUaW1lRmllbGQoYXV0b19ub3dfYWRkPVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICBvcmRlcmluZyA9IFsiLXBlcmlvZG8iLCAiYXJlYSJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIlB1bnRhamUgUEdPIHBvciBwZXLDrW9kbyIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIlB1bnRhamVzIFBHTyBwb3IgcGVyw61vZG8iCgogICAgZGVmIF9fc3RyX18oc2VsZik6CiAgICAgICAgcmV0dXJuIGYie3NlbGYucGVyaW9kb30g4oCUIHtzZWxmLmFyZWEgb3IgJ2dlbmVyYWwnfSIKCgpjbGFzcyBQZ29Nb250aGx5QWdnKG1vZGVscy5Nb2RlbCk6CiAgICBwZXJpb2RvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTcsIGRiX2luZGV4PVRydWUpCiAgICB1bmlkYWRfbmVnb2NpbyA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgICJ3Y2dvbmVfY29yZS5VbmlkYWROZWdvY2lvIiwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJwZ29fbW9udGhseV9hZ2dzIiwKICAgICkKICAgIGRlcGFydGFtZW50byA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xNTAsIGJsYW5rPVRydWUpCiAgICB0aWNrZXRzX3JlY2liaWRvcyA9IG1vZGVscy5Qb3NpdGl2ZUludGVnZXJGaWVsZChkZWZhdWx0PTApCiAgICB0aWNrZXRzX2NlcnJhZG9zID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKGRlZmF1bHQ9MCkKICAgIHRpZW1wb19wcm9tZWRpb19ob3JhcyA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xMiwgZGVjaW1hbF9wbGFjZXM9MiwgZGVmYXVsdD0wKQogICAgc2xhX2N1bXBsaWRvcyA9IG1vZGVscy5Qb3NpdGl2ZUludGVnZXJGaWVsZChkZWZhdWx0PTApCiAgICBzbGFfaW5jdW1wbGlkb3MgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoZGVmYXVsdD0wKQogICAgdGlja2V0c19hYmllcnRvc19maW5fbWVzID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKGRlZmF1bHQ9MCkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIG9yZGVyaW5nID0gWyItcGVyaW9kbyIsICJ1bmlkYWRfbmVnb2Npb19fbm9tYnJlIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiQWdyZWdhZG8gbWVuc3VhbCBQR08iCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJBZ3JlZ2Fkb3MgbWVuc3VhbGVzIFBHTyIKICAgICAgICBpbmRleGVzID0gWwogICAgICAgICAgICBtb2RlbHMuSW5kZXgoZmllbGRzPVsicGVyaW9kbyIsICJkZXBhcnRhbWVudG8iXSksCiAgICAgICAgXQoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLnBlcmlvZG99IOKAlCB7c2VsZi51bmlkYWRfbmVnb2Npb30iCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/pgo/selectors.py
PATH_JSON="apps/pgo/selectors.py"
FILENAME=selectors.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=55
SIZE_BYTES_UTF8=1879
CONTENT_SHA256=9e88d5cb75b8dd2310fc9d805b3e7d7044c07006b60ad205c666e627ce6c3a62
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
"""Consultas reutilizables para PGO y KPIs."""

from __future__ import annotations

from django.db.models import Avg, Count, Q

from apps.pgo.models import PgoTicket

CERRADOS = Q(estado_normalizado__in=["cerrado", "closed", "cerrada"])


def ticket_list_queryset(request):
    qs = PgoTicket.objects.select_related("unidad_negocio", "responsable").order_by(
        "-fecha_apertura"
    )
    estado = request.GET.get("estado", "").strip()
    if estado:
        qs = qs.filter(estado_normalizado__icontains=estado)
    periodo = request.GET.get("periodo", "").strip()
    if periodo:
        qs = qs.filter(anio_mes=periodo)
    prioridad = request.GET.get("prioridad", "").strip()
    if prioridad:
        qs = qs.filter(prioridad__icontains=prioridad)
    return qs


def ticket_dashboard_summary():
    tickets = PgoTicket.objects.all()
    abiertos = tickets.exclude(CERRADOS)
    por_estado = list(
        tickets.values("estado_normalizado")
        .annotate(total=Count("id"))
        .order_by("-total")[:8]
    )
    por_prioridad = list(
        tickets.exclude(prioridad="")
        .values("prioridad")
        .annotate(total=Count("id"))
        .order_by("-total")[:8]
    )
    return {
        "total_tickets": tickets.count(),
        "tickets_cerrados": tickets.filter(CERRADOS).count(),
        "tickets_abiertos": abiertos.count(),
        "tickets_vencidos": abiertos.filter(sla_cumplido=False).count(),
        "sla_cumplidos": tickets.filter(sla_cumplido=True).count(),
        "sla_incumplidos": tickets.filter(sla_cumplido=False).exclude(CERRADOS).count(),
        "tiempo_promedio": tickets.filter(duracion_horas__isnull=False).aggregate(
            avg=Avg("duracion_horas")
        )["avg"],
        "por_estado": por_estado,
        "por_prioridad": por_prioridad,
        "tickets_recientes": tickets.order_by("-fecha_apertura")[:10],
    }

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Consultas reutilizables para PGO y KPIs."""
00002|
00003|from __future__ import annotations
00004|
00005|from django.db.models import Avg, Count, Q
00006|
00007|from apps.pgo.models import PgoTicket
00008|
00009|CERRADOS = Q(estado_normalizado__in=["cerrado", "closed", "cerrada"])
00010|
00011|
00012|def ticket_list_queryset(request):
00013|    qs = PgoTicket.objects.select_related("unidad_negocio", "responsable").order_by(
00014|        "-fecha_apertura"
00015|    )
00016|    estado = request.GET.get("estado", "").strip()
00017|    if estado:
00018|        qs = qs.filter(estado_normalizado__icontains=estado)
00019|    periodo = request.GET.get("periodo", "").strip()
00020|    if periodo:
00021|        qs = qs.filter(anio_mes=periodo)
00022|    prioridad = request.GET.get("prioridad", "").strip()
00023|    if prioridad:
00024|        qs = qs.filter(prioridad__icontains=prioridad)
00025|    return qs
00026|
00027|
00028|def ticket_dashboard_summary():
00029|    tickets = PgoTicket.objects.all()
00030|    abiertos = tickets.exclude(CERRADOS)
00031|    por_estado = list(
00032|        tickets.values("estado_normalizado")
00033|        .annotate(total=Count("id"))
00034|        .order_by("-total")[:8]
00035|    )
00036|    por_prioridad = list(
00037|        tickets.exclude(prioridad="")
00038|        .values("prioridad")
00039|        .annotate(total=Count("id"))
00040|        .order_by("-total")[:8]
00041|    )
00042|    return {
00043|        "total_tickets": tickets.count(),
00044|        "tickets_cerrados": tickets.filter(CERRADOS).count(),
00045|        "tickets_abiertos": abiertos.count(),
00046|        "tickets_vencidos": abiertos.filter(sla_cumplido=False).count(),
00047|        "sla_cumplidos": tickets.filter(sla_cumplido=True).count(),
00048|        "sla_incumplidos": tickets.filter(sla_cumplido=False).exclude(CERRADOS).count(),
00049|        "tiempo_promedio": tickets.filter(duracion_horas__isnull=False).aggregate(
00050|            avg=Avg("duracion_horas")
00051|        )["avg"],
00052|        "por_estado": por_estado,
00053|        "por_prioridad": por_prioridad,
00054|        "tickets_recientes": tickets.order_by("-fecha_apertura")[:10],
00055|    }

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiQ29uc3VsdGFzIHJldXRpbGl6YWJsZXMgcGFyYSBQR08geSBLUElzLiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKZnJvbSBkamFuZ28uZGIubW9kZWxzIGltcG9ydCBBdmcsIENvdW50LCBRCgpmcm9tIGFwcHMucGdvLm1vZGVscyBpbXBvcnQgUGdvVGlja2V0CgpDRVJSQURPUyA9IFEoZXN0YWRvX25vcm1hbGl6YWRvX19pbj1bImNlcnJhZG8iLCAiY2xvc2VkIiwgImNlcnJhZGEiXSkKCgpkZWYgdGlja2V0X2xpc3RfcXVlcnlzZXQocmVxdWVzdCk6CiAgICBxcyA9IFBnb1RpY2tldC5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJ1bmlkYWRfbmVnb2NpbyIsICJyZXNwb25zYWJsZSIpLm9yZGVyX2J5KAogICAgICAgICItZmVjaGFfYXBlcnR1cmEiCiAgICApCiAgICBlc3RhZG8gPSByZXF1ZXN0LkdFVC5nZXQoImVzdGFkbyIsICIiKS5zdHJpcCgpCiAgICBpZiBlc3RhZG86CiAgICAgICAgcXMgPSBxcy5maWx0ZXIoZXN0YWRvX25vcm1hbGl6YWRvX19pY29udGFpbnM9ZXN0YWRvKQogICAgcGVyaW9kbyA9IHJlcXVlc3QuR0VULmdldCgicGVyaW9kbyIsICIiKS5zdHJpcCgpCiAgICBpZiBwZXJpb2RvOgogICAgICAgIHFzID0gcXMuZmlsdGVyKGFuaW9fbWVzPXBlcmlvZG8pCiAgICBwcmlvcmlkYWQgPSByZXF1ZXN0LkdFVC5nZXQoInByaW9yaWRhZCIsICIiKS5zdHJpcCgpCiAgICBpZiBwcmlvcmlkYWQ6CiAgICAgICAgcXMgPSBxcy5maWx0ZXIocHJpb3JpZGFkX19pY29udGFpbnM9cHJpb3JpZGFkKQogICAgcmV0dXJuIHFzCgoKZGVmIHRpY2tldF9kYXNoYm9hcmRfc3VtbWFyeSgpOgogICAgdGlja2V0cyA9IFBnb1RpY2tldC5vYmplY3RzLmFsbCgpCiAgICBhYmllcnRvcyA9IHRpY2tldHMuZXhjbHVkZShDRVJSQURPUykKICAgIHBvcl9lc3RhZG8gPSBsaXN0KAogICAgICAgIHRpY2tldHMudmFsdWVzKCJlc3RhZG9fbm9ybWFsaXphZG8iKQogICAgICAgIC5hbm5vdGF0ZSh0b3RhbD1Db3VudCgiaWQiKSkKICAgICAgICAub3JkZXJfYnkoIi10b3RhbCIpWzo4XQogICAgKQogICAgcG9yX3ByaW9yaWRhZCA9IGxpc3QoCiAgICAgICAgdGlja2V0cy5leGNsdWRlKHByaW9yaWRhZD0iIikKICAgICAgICAudmFsdWVzKCJwcmlvcmlkYWQiKQogICAgICAgIC5hbm5vdGF0ZSh0b3RhbD1Db3VudCgiaWQiKSkKICAgICAgICAub3JkZXJfYnkoIi10b3RhbCIpWzo4XQogICAgKQogICAgcmV0dXJuIHsKICAgICAgICAidG90YWxfdGlja2V0cyI6IHRpY2tldHMuY291bnQoKSwKICAgICAgICAidGlja2V0c19jZXJyYWRvcyI6IHRpY2tldHMuZmlsdGVyKENFUlJBRE9TKS5jb3VudCgpLAogICAgICAgICJ0aWNrZXRzX2FiaWVydG9zIjogYWJpZXJ0b3MuY291bnQoKSwKICAgICAgICAidGlja2V0c192ZW5jaWRvcyI6IGFiaWVydG9zLmZpbHRlcihzbGFfY3VtcGxpZG89RmFsc2UpLmNvdW50KCksCiAgICAgICAgInNsYV9jdW1wbGlkb3MiOiB0aWNrZXRzLmZpbHRlcihzbGFfY3VtcGxpZG89VHJ1ZSkuY291bnQoKSwKICAgICAgICAic2xhX2luY3VtcGxpZG9zIjogdGlja2V0cy5maWx0ZXIoc2xhX2N1bXBsaWRvPUZhbHNlKS5leGNsdWRlKENFUlJBRE9TKS5jb3VudCgpLAogICAgICAgICJ0aWVtcG9fcHJvbWVkaW8iOiB0aWNrZXRzLmZpbHRlcihkdXJhY2lvbl9ob3Jhc19faXNudWxsPUZhbHNlKS5hZ2dyZWdhdGUoCiAgICAgICAgICAgIGF2Zz1BdmcoImR1cmFjaW9uX2hvcmFzIikKICAgICAgICApWyJhdmciXSwKICAgICAgICAicG9yX2VzdGFkbyI6IHBvcl9lc3RhZG8sCiAgICAgICAgInBvcl9wcmlvcmlkYWQiOiBwb3JfcHJpb3JpZGFkLAogICAgICAgICJ0aWNrZXRzX3JlY2llbnRlcyI6IHRpY2tldHMub3JkZXJfYnkoIi1mZWNoYV9hcGVydHVyYSIpWzoxMF0sCiAgICB9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/pgo/urls.py
PATH_JSON="apps/pgo/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=14
SIZE_BYTES_UTF8=526
CONTENT_SHA256=44f25391e027107d5d45a5f7cd760b316e99957078336f7f1ea630bf3f4a1266
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

app_name = "wcgone_pgo"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("tickets/", views.TicketListView.as_view(), name="ticket_list"),
    path("tickets/exportar/", views.export_tickets_csv, name="export_tickets"),
    path("tickets/<int:pk>/", views.TicketDetailView.as_view(), name="ticket_detail"),
    path("resultados/", views.resultados, name="resultados"),
    path("importar-tickets/", views.importar_tickets, name="importar_tickets"),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.urls import path
00002|
00003|from . import views
00004|
00005|app_name = "wcgone_pgo"
00006|
00007|urlpatterns = [
00008|    path("", views.dashboard, name="dashboard"),
00009|    path("tickets/", views.TicketListView.as_view(), name="ticket_list"),
00010|    path("tickets/exportar/", views.export_tickets_csv, name="export_tickets"),
00011|    path("tickets/<int:pk>/", views.TicketDetailView.as_view(), name="ticket_detail"),
00012|    path("resultados/", views.resultados, name="resultados"),
00013|    path("importar-tickets/", views.importar_tickets, name="importar_tickets"),
00014|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aAoKZnJvbSAuIGltcG9ydCB2aWV3cwoKYXBwX25hbWUgPSAid2Nnb25lX3BnbyIKCnVybHBhdHRlcm5zID0gWwogICAgcGF0aCgiIiwgdmlld3MuZGFzaGJvYXJkLCBuYW1lPSJkYXNoYm9hcmQiKSwKICAgIHBhdGgoInRpY2tldHMvIiwgdmlld3MuVGlja2V0TGlzdFZpZXcuYXNfdmlldygpLCBuYW1lPSJ0aWNrZXRfbGlzdCIpLAogICAgcGF0aCgidGlja2V0cy9leHBvcnRhci8iLCB2aWV3cy5leHBvcnRfdGlja2V0c19jc3YsIG5hbWU9ImV4cG9ydF90aWNrZXRzIiksCiAgICBwYXRoKCJ0aWNrZXRzLzxpbnQ6cGs+LyIsIHZpZXdzLlRpY2tldERldGFpbFZpZXcuYXNfdmlldygpLCBuYW1lPSJ0aWNrZXRfZGV0YWlsIiksCiAgICBwYXRoKCJyZXN1bHRhZG9zLyIsIHZpZXdzLnJlc3VsdGFkb3MsIG5hbWU9InJlc3VsdGFkb3MiKSwKICAgIHBhdGgoImltcG9ydGFyLXRpY2tldHMvIiwgdmlld3MuaW1wb3J0YXJfdGlja2V0cywgbmFtZT0iaW1wb3J0YXJfdGlja2V0cyIpLApdCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/pgo/views.py
PATH_JSON="apps/pgo/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=132
SIZE_BYTES_UTF8=4173
CONTENT_SHA256=94309c41ca93626f8974a8c34021c8aecf7363452179b8567781ca2840aa7e93
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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, ListView

from apps.core.exports import csv_response
from apps.core.forms import ImportFileForm

from .models import PgoMonthlyAgg, PgoPeriodScore, PgoTicket
from .selectors import ticket_dashboard_summary, ticket_list_queryset


@login_required
def dashboard(request):
    summary = ticket_dashboard_summary()
    context = {
        **summary,
        "breadcrumbs": [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "PGO — Operación"},
        ],
    }
    return render(request, "wcgone/pgo/dashboard.html", context)


class TicketListView(LoginRequiredMixin, ListView):
    model = PgoTicket
    template_name = "wcgone/pgo/ticket_list.html"
    context_object_name = "tickets"
    paginate_by = 25

    def get_queryset(self):
        return ticket_list_queryset(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "PGO — Operación", "url": "/wcgone/pgo/"},
            {"label": "Tickets"},
        ]
        context["export_query"] = self.request.GET.urlencode()
        return context


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = PgoTicket
    template_name = "wcgone/pgo/ticket_detail.html"
    context_object_name = "ticket"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = self.object
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "PGO — Operación", "url": "/wcgone/pgo/"},
            {"label": "Tickets", "url": "/wcgone/pgo/tickets/"},
            {"label": ticket.ticket_externo_id or f"#{ticket.pk}"},
        ]
        return context


@login_required
def resultados(request):
    periodo = request.GET.get("periodo", "").strip()
    scores = PgoPeriodScore.objects.select_related("unidad_negocio", "usuario").order_by(
        "-periodo", "area"
    )
    aggs = PgoMonthlyAgg.objects.select_related("unidad_negocio").order_by("-periodo")
    if periodo:
        scores = scores.filter(periodo=periodo)
        aggs = aggs.filter(periodo=periodo)
    context = {
        "scores": scores[:50],
        "aggs": aggs[:50],
        "breadcrumbs": [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "PGO — Operación", "url": "/wcgone/pgo/"},
            {"label": "Resultados por período"},
        ],
    }
    return render(request, "wcgone/pgo/resultados.html", context)


from django.contrib import messages  # noqa: E402
from django.shortcuts import redirect  # noqa: E402

from .imports.tickets import import_tickets  # noqa: E402


@login_required
def export_tickets_csv(request):
    qs = ticket_list_queryset(request)
    rows = []
    for t in qs:
        rows.append([
            t.ticket_externo_id or t.pk,
            t.titulo,
            t.estado_normalizado or t.estado_raw or "",
            t.prioridad or "",
            t.departamento or "",
            t.sistema or "",
            t.anio_mes or "",
            "Sí" if t.sla_cumplido else "No",
            t.fecha_apertura.strftime("%Y-%m-%d %H:%M") if t.fecha_apertura else "",
            t.fecha_cierre.strftime("%Y-%m-%d %H:%M") if t.fecha_cierre else "",
            t.duracion_horas or "",
        ])
    filename = f"pgo_tickets_{timezone.localdate().isoformat()}.csv"
    return csv_response(
        filename,
        [
            "ID ticket",
            "Título",
            "Estado",
            "Prioridad",
            "Departamento",
            "Sistema",
            "Período",
            "SLA cumplido",
            "Fecha apertura",
            "Fecha cierre",
            "Duración (h)",
        ],
        rows,
    )


@login_required
def importar_tickets(request):
    return redirect("imports:import_hub")

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib.auth.decorators import login_required
00002|from django.contrib.auth.mixins import LoginRequiredMixin
00003|from django.shortcuts import render
00004|from django.utils import timezone
00005|from django.views.generic import DetailView, ListView
00006|
00007|from apps.core.exports import csv_response
00008|from apps.core.forms import ImportFileForm
00009|
00010|from .models import PgoMonthlyAgg, PgoPeriodScore, PgoTicket
00011|from .selectors import ticket_dashboard_summary, ticket_list_queryset
00012|
00013|
00014|@login_required
00015|def dashboard(request):
00016|    summary = ticket_dashboard_summary()
00017|    context = {
00018|        **summary,
00019|        "breadcrumbs": [
00020|            {"label": "Panel principal", "url": "/panel/"},
00021|            {"label": "PGO — Operación"},
00022|        ],
00023|    }
00024|    return render(request, "wcgone/pgo/dashboard.html", context)
00025|
00026|
00027|class TicketListView(LoginRequiredMixin, ListView):
00028|    model = PgoTicket
00029|    template_name = "wcgone/pgo/ticket_list.html"
00030|    context_object_name = "tickets"
00031|    paginate_by = 25
00032|
00033|    def get_queryset(self):
00034|        return ticket_list_queryset(self.request)
00035|
00036|    def get_context_data(self, **kwargs):
00037|        context = super().get_context_data(**kwargs)
00038|        context["breadcrumbs"] = [
00039|            {"label": "Panel principal", "url": "/panel/"},
00040|            {"label": "PGO — Operación", "url": "/wcgone/pgo/"},
00041|            {"label": "Tickets"},
00042|        ]
00043|        context["export_query"] = self.request.GET.urlencode()
00044|        return context
00045|
00046|
00047|class TicketDetailView(LoginRequiredMixin, DetailView):
00048|    model = PgoTicket
00049|    template_name = "wcgone/pgo/ticket_detail.html"
00050|    context_object_name = "ticket"
00051|
00052|    def get_context_data(self, **kwargs):
00053|        context = super().get_context_data(**kwargs)
00054|        ticket = self.object
00055|        context["breadcrumbs"] = [
00056|            {"label": "Panel principal", "url": "/panel/"},
00057|            {"label": "PGO — Operación", "url": "/wcgone/pgo/"},
00058|            {"label": "Tickets", "url": "/wcgone/pgo/tickets/"},
00059|            {"label": ticket.ticket_externo_id or f"#{ticket.pk}"},
00060|        ]
00061|        return context
00062|
00063|
00064|@login_required
00065|def resultados(request):
00066|    periodo = request.GET.get("periodo", "").strip()
00067|    scores = PgoPeriodScore.objects.select_related("unidad_negocio", "usuario").order_by(
00068|        "-periodo", "area"
00069|    )
00070|    aggs = PgoMonthlyAgg.objects.select_related("unidad_negocio").order_by("-periodo")
00071|    if periodo:
00072|        scores = scores.filter(periodo=periodo)
00073|        aggs = aggs.filter(periodo=periodo)
00074|    context = {
00075|        "scores": scores[:50],
00076|        "aggs": aggs[:50],
00077|        "breadcrumbs": [
00078|            {"label": "Panel principal", "url": "/panel/"},
00079|            {"label": "PGO — Operación", "url": "/wcgone/pgo/"},
00080|            {"label": "Resultados por período"},
00081|        ],
00082|    }
00083|    return render(request, "wcgone/pgo/resultados.html", context)
00084|
00085|
00086|from django.contrib import messages  # noqa: E402
00087|from django.shortcuts import redirect  # noqa: E402
00088|
00089|from .imports.tickets import import_tickets  # noqa: E402
00090|
00091|
00092|@login_required
00093|def export_tickets_csv(request):
00094|    qs = ticket_list_queryset(request)
00095|    rows = []
00096|    for t in qs:
00097|        rows.append([
00098|            t.ticket_externo_id or t.pk,
00099|            t.titulo,
00100|            t.estado_normalizado or t.estado_raw or "",
00101|            t.prioridad or "",
00102|            t.departamento or "",
00103|            t.sistema or "",
00104|            t.anio_mes or "",
00105|            "Sí" if t.sla_cumplido else "No",
00106|            t.fecha_apertura.strftime("%Y-%m-%d %H:%M") if t.fecha_apertura else "",
00107|            t.fecha_cierre.strftime("%Y-%m-%d %H:%M") if t.fecha_cierre else "",
00108|            t.duracion_horas or "",
00109|        ])
00110|    filename = f"pgo_tickets_{timezone.localdate().isoformat()}.csv"
00111|    return csv_response(
00112|        filename,
00113|        [
00114|            "ID ticket",
00115|            "Título",
00116|            "Estado",
00117|            "Prioridad",
00118|            "Departamento",
00119|            "Sistema",
00120|            "Período",
00121|            "SLA cumplido",
00122|            "Fecha apertura",
00123|            "Fecha cierre",
00124|            "Duración (h)",
00125|        ],
00126|        rows,
00127|    )
00128|
00129|
00130|@login_required
00131|def importar_tickets(request):
00132|    return redirect("imports:import_hub")

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYi5hdXRoLmRlY29yYXRvcnMgaW1wb3J0IGxvZ2luX3JlcXVpcmVkCmZyb20gZGphbmdvLmNvbnRyaWIuYXV0aC5taXhpbnMgaW1wb3J0IExvZ2luUmVxdWlyZWRNaXhpbgpmcm9tIGRqYW5nby5zaG9ydGN1dHMgaW1wb3J0IHJlbmRlcgpmcm9tIGRqYW5nby51dGlscyBpbXBvcnQgdGltZXpvbmUKZnJvbSBkamFuZ28udmlld3MuZ2VuZXJpYyBpbXBvcnQgRGV0YWlsVmlldywgTGlzdFZpZXcKCmZyb20gYXBwcy5jb3JlLmV4cG9ydHMgaW1wb3J0IGNzdl9yZXNwb25zZQpmcm9tIGFwcHMuY29yZS5mb3JtcyBpbXBvcnQgSW1wb3J0RmlsZUZvcm0KCmZyb20gLm1vZGVscyBpbXBvcnQgUGdvTW9udGhseUFnZywgUGdvUGVyaW9kU2NvcmUsIFBnb1RpY2tldApmcm9tIC5zZWxlY3RvcnMgaW1wb3J0IHRpY2tldF9kYXNoYm9hcmRfc3VtbWFyeSwgdGlja2V0X2xpc3RfcXVlcnlzZXQKCgpAbG9naW5fcmVxdWlyZWQKZGVmIGRhc2hib2FyZChyZXF1ZXN0KToKICAgIHN1bW1hcnkgPSB0aWNrZXRfZGFzaGJvYXJkX3N1bW1hcnkoKQogICAgY29udGV4dCA9IHsKICAgICAgICAqKnN1bW1hcnksCiAgICAgICAgImJyZWFkY3J1bWJzIjogWwogICAgICAgICAgICB7ImxhYmVsIjogIlBhbmVsIHByaW5jaXBhbCIsICJ1cmwiOiAiL3BhbmVsLyJ9LAogICAgICAgICAgICB7ImxhYmVsIjogIlBHTyDigJQgT3BlcmFjacOzbiJ9LAogICAgICAgIF0sCiAgICB9CiAgICByZXR1cm4gcmVuZGVyKHJlcXVlc3QsICJ3Y2dvbmUvcGdvL2Rhc2hib2FyZC5odG1sIiwgY29udGV4dCkKCgpjbGFzcyBUaWNrZXRMaXN0VmlldyhMb2dpblJlcXVpcmVkTWl4aW4sIExpc3RWaWV3KToKICAgIG1vZGVsID0gUGdvVGlja2V0CiAgICB0ZW1wbGF0ZV9uYW1lID0gIndjZ29uZS9wZ28vdGlja2V0X2xpc3QuaHRtbCIKICAgIGNvbnRleHRfb2JqZWN0X25hbWUgPSAidGlja2V0cyIKICAgIHBhZ2luYXRlX2J5ID0gMjUKCiAgICBkZWYgZ2V0X3F1ZXJ5c2V0KHNlbGYpOgogICAgICAgIHJldHVybiB0aWNrZXRfbGlzdF9xdWVyeXNldChzZWxmLnJlcXVlc3QpCgogICAgZGVmIGdldF9jb250ZXh0X2RhdGEoc2VsZiwgKiprd2FyZ3MpOgogICAgICAgIGNvbnRleHQgPSBzdXBlcigpLmdldF9jb250ZXh0X2RhdGEoKiprd2FyZ3MpCiAgICAgICAgY29udGV4dFsiYnJlYWRjcnVtYnMiXSA9IFsKICAgICAgICAgICAgeyJsYWJlbCI6ICJQYW5lbCBwcmluY2lwYWwiLCAidXJsIjogIi9wYW5lbC8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJQR08g4oCUIE9wZXJhY2nDs24iLCAidXJsIjogIi93Y2dvbmUvcGdvLyJ9LAogICAgICAgICAgICB7ImxhYmVsIjogIlRpY2tldHMifSwKICAgICAgICBdCiAgICAgICAgY29udGV4dFsiZXhwb3J0X3F1ZXJ5Il0gPSBzZWxmLnJlcXVlc3QuR0VULnVybGVuY29kZSgpCiAgICAgICAgcmV0dXJuIGNvbnRleHQKCgpjbGFzcyBUaWNrZXREZXRhaWxWaWV3KExvZ2luUmVxdWlyZWRNaXhpbiwgRGV0YWlsVmlldyk6CiAgICBtb2RlbCA9IFBnb1RpY2tldAogICAgdGVtcGxhdGVfbmFtZSA9ICJ3Y2dvbmUvcGdvL3RpY2tldF9kZXRhaWwuaHRtbCIKICAgIGNvbnRleHRfb2JqZWN0X25hbWUgPSAidGlja2V0IgoKICAgIGRlZiBnZXRfY29udGV4dF9kYXRhKHNlbGYsICoqa3dhcmdzKToKICAgICAgICBjb250ZXh0ID0gc3VwZXIoKS5nZXRfY29udGV4dF9kYXRhKCoqa3dhcmdzKQogICAgICAgIHRpY2tldCA9IHNlbGYub2JqZWN0CiAgICAgICAgY29udGV4dFsiYnJlYWRjcnVtYnMiXSA9IFsKICAgICAgICAgICAgeyJsYWJlbCI6ICJQYW5lbCBwcmluY2lwYWwiLCAidXJsIjogIi9wYW5lbC8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJQR08g4oCUIE9wZXJhY2nDs24iLCAidXJsIjogIi93Y2dvbmUvcGdvLyJ9LAogICAgICAgICAgICB7ImxhYmVsIjogIlRpY2tldHMiLCAidXJsIjogIi93Y2dvbmUvcGdvL3RpY2tldHMvIn0sCiAgICAgICAgICAgIHsibGFiZWwiOiB0aWNrZXQudGlja2V0X2V4dGVybm9faWQgb3IgZiIje3RpY2tldC5wa30ifSwKICAgICAgICBdCiAgICAgICAgcmV0dXJuIGNvbnRleHQKCgpAbG9naW5fcmVxdWlyZWQKZGVmIHJlc3VsdGFkb3MocmVxdWVzdCk6CiAgICBwZXJpb2RvID0gcmVxdWVzdC5HRVQuZ2V0KCJwZXJpb2RvIiwgIiIpLnN0cmlwKCkKICAgIHNjb3JlcyA9IFBnb1BlcmlvZFNjb3JlLm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoInVuaWRhZF9uZWdvY2lvIiwgInVzdWFyaW8iKS5vcmRlcl9ieSgKICAgICAgICAiLXBlcmlvZG8iLCAiYXJlYSIKICAgICkKICAgIGFnZ3MgPSBQZ29Nb250aGx5QWdnLm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoInVuaWRhZF9uZWdvY2lvIikub3JkZXJfYnkoIi1wZXJpb2RvIikKICAgIGlmIHBlcmlvZG86CiAgICAgICAgc2NvcmVzID0gc2NvcmVzLmZpbHRlcihwZXJpb2RvPXBlcmlvZG8pCiAgICAgICAgYWdncyA9IGFnZ3MuZmlsdGVyKHBlcmlvZG89cGVyaW9kbykKICAgIGNvbnRleHQgPSB7CiAgICAgICAgInNjb3JlcyI6IHNjb3Jlc1s6NTBdLAogICAgICAgICJhZ2dzIjogYWdnc1s6NTBdLAogICAgICAgICJicmVhZGNydW1icyI6IFsKICAgICAgICAgICAgeyJsYWJlbCI6ICJQYW5lbCBwcmluY2lwYWwiLCAidXJsIjogIi9wYW5lbC8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJQR08g4oCUIE9wZXJhY2nDs24iLCAidXJsIjogIi93Y2dvbmUvcGdvLyJ9LAogICAgICAgICAgICB7ImxhYmVsIjogIlJlc3VsdGFkb3MgcG9yIHBlcsOtb2RvIn0sCiAgICAgICAgXSwKICAgIH0KICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgIndjZ29uZS9wZ28vcmVzdWx0YWRvcy5odG1sIiwgY29udGV4dCkKCgpmcm9tIGRqYW5nby5jb250cmliIGltcG9ydCBtZXNzYWdlcyAgIyBub3FhOiBFNDAyCmZyb20gZGphbmdvLnNob3J0Y3V0cyBpbXBvcnQgcmVkaXJlY3QgICMgbm9xYTogRTQwMgoKZnJvbSAuaW1wb3J0cy50aWNrZXRzIGltcG9ydCBpbXBvcnRfdGlja2V0cyAgIyBub3FhOiBFNDAyCgoKQGxvZ2luX3JlcXVpcmVkCmRlZiBleHBvcnRfdGlja2V0c19jc3YocmVxdWVzdCk6CiAgICBxcyA9IHRpY2tldF9saXN0X3F1ZXJ5c2V0KHJlcXVlc3QpCiAgICByb3dzID0gW10KICAgIGZvciB0IGluIHFzOgogICAgICAgIHJvd3MuYXBwZW5kKFsKICAgICAgICAgICAgdC50aWNrZXRfZXh0ZXJub19pZCBvciB0LnBrLAogICAgICAgICAgICB0LnRpdHVsbywKICAgICAgICAgICAgdC5lc3RhZG9fbm9ybWFsaXphZG8gb3IgdC5lc3RhZG9fcmF3IG9yICIiLAogICAgICAgICAgICB0LnByaW9yaWRhZCBvciAiIiwKICAgICAgICAgICAgdC5kZXBhcnRhbWVudG8gb3IgIiIsCiAgICAgICAgICAgIHQuc2lzdGVtYSBvciAiIiwKICAgICAgICAgICAgdC5hbmlvX21lcyBvciAiIiwKICAgICAgICAgICAgIlPDrSIgaWYgdC5zbGFfY3VtcGxpZG8gZWxzZSAiTm8iLAogICAgICAgICAgICB0LmZlY2hhX2FwZXJ0dXJhLnN0cmZ0aW1lKCIlWS0lbS0lZCAlSDolTSIpIGlmIHQuZmVjaGFfYXBlcnR1cmEgZWxzZSAiIiwKICAgICAgICAgICAgdC5mZWNoYV9jaWVycmUuc3RyZnRpbWUoIiVZLSVtLSVkICVIOiVNIikgaWYgdC5mZWNoYV9jaWVycmUgZWxzZSAiIiwKICAgICAgICAgICAgdC5kdXJhY2lvbl9ob3JhcyBvciAiIiwKICAgICAgICBdKQogICAgZmlsZW5hbWUgPSBmInBnb190aWNrZXRzX3t0aW1lem9uZS5sb2NhbGRhdGUoKS5pc29mb3JtYXQoKX0uY3N2IgogICAgcmV0dXJuIGNzdl9yZXNwb25zZSgKICAgICAgICBmaWxlbmFtZSwKICAgICAgICBbCiAgICAgICAgICAgICJJRCB0aWNrZXQiLAogICAgICAgICAgICAiVMOtdHVsbyIsCiAgICAgICAgICAgICJFc3RhZG8iLAogICAgICAgICAgICAiUHJpb3JpZGFkIiwKICAgICAgICAgICAgIkRlcGFydGFtZW50byIsCiAgICAgICAgICAgICJTaXN0ZW1hIiwKICAgICAgICAgICAgIlBlcsOtb2RvIiwKICAgICAgICAgICAgIlNMQSBjdW1wbGlkbyIsCiAgICAgICAgICAgICJGZWNoYSBhcGVydHVyYSIsCiAgICAgICAgICAgICJGZWNoYSBjaWVycmUiLAogICAgICAgICAgICAiRHVyYWNpw7NuIChoKSIsCiAgICAgICAgXSwKICAgICAgICByb3dzLAogICAgKQoKCkBsb2dpbl9yZXF1aXJlZApkZWYgaW1wb3J0YXJfdGlja2V0cyhyZXF1ZXN0KToKICAgIHJldHVybiByZWRpcmVjdCgiaW1wb3J0czppbXBvcnRfaHViIikK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/portal/__init__.py
PATH_JSON="apps/portal/__init__.py"
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
PATH_LITERAL=apps/portal/apps.py
PATH_JSON="apps/portal/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=8
SIZE_BYTES_UTF8=209
CONTENT_SHA256=80420c0bd0761646d3ae007e8145fccf51df53f1feadff1705456f7b069a6b7d
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


class PortalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.portal"
    label = "wcgone_portal"
    verbose_name = "Portal WCG"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class PortalConfig(AppConfig):
00005|    default_auto_field = "django.db.models.BigAutoField"
00006|    name = "apps.portal"
00007|    label = "wcgone_portal"
00008|    verbose_name = "Portal WCG"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgUG9ydGFsQ29uZmlnKEFwcENvbmZpZyk6CiAgICBkZWZhdWx0X2F1dG9fZmllbGQgPSAiZGphbmdvLmRiLm1vZGVscy5CaWdBdXRvRmllbGQiCiAgICBuYW1lID0gImFwcHMucG9ydGFsIgogICAgbGFiZWwgPSAid2Nnb25lX3BvcnRhbCIKICAgIHZlcmJvc2VfbmFtZSA9ICJQb3J0YWwgV0NHIgo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/portal/urls.py
PATH_JSON="apps/portal/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=12
SIZE_BYTES_UTF8=346
CONTENT_SHA256=3e258577e9e730ea681b934dc9a8919c86f2589958d22b38e34887b9f63c930b
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

app_name = "wcgone_portal"

urlpatterns = [
    path("panel/", views.PanelView.as_view(), name="panel"),
    path("ayuda/", views.AyudaView.as_view(), name="ayuda"),
    # splash de wcg_one opcional (no es la landing productiva)
    path("splash/", views.SplashView.as_view(), name="splash"),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.urls import path
00002|
00003|from . import views
00004|
00005|app_name = "wcgone_portal"
00006|
00007|urlpatterns = [
00008|    path("panel/", views.PanelView.as_view(), name="panel"),
00009|    path("ayuda/", views.AyudaView.as_view(), name="ayuda"),
00010|    # splash de wcg_one opcional (no es la landing productiva)
00011|    path("splash/", views.SplashView.as_view(), name="splash"),
00012|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aAoKZnJvbSAuIGltcG9ydCB2aWV3cwoKYXBwX25hbWUgPSAid2Nnb25lX3BvcnRhbCIKCnVybHBhdHRlcm5zID0gWwogICAgcGF0aCgicGFuZWwvIiwgdmlld3MuUGFuZWxWaWV3LmFzX3ZpZXcoKSwgbmFtZT0icGFuZWwiKSwKICAgIHBhdGgoImF5dWRhLyIsIHZpZXdzLkF5dWRhVmlldy5hc192aWV3KCksIG5hbWU9ImF5dWRhIiksCiAgICAjIHNwbGFzaCBkZSB3Y2dfb25lIG9wY2lvbmFsIChubyBlcyBsYSBsYW5kaW5nIHByb2R1Y3RpdmEpCiAgICBwYXRoKCJzcGxhc2gvIiwgdmlld3MuU3BsYXNoVmlldy5hc192aWV3KCksIG5hbWU9InNwbGFzaCIpLApdCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/portal/views.py
PATH_JSON="apps/portal/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=46
SIZE_BYTES_UTF8=1797
CONTENT_SHA256=c4bfabc8c253557dbc0e941d21519a2d5e417ae7272d0a0ec0c61cacf4a65365
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.models import DataImportBatch, Entidad
from apps.crm.models import Tarea
from apps.pgo.models import PgoTicket
from apps.risk.models import RiskOperacion, RiskOperationSnapshot


class SplashView(TemplateView):
    template_name = "portal/splash_wcgone.html"


class PanelView(LoginRequiredMixin, TemplateView):
    template_name = "portal/home_wcgone.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cerrados = ["cerrado", "closed", "cerrada"]
        context["stats"] = {
            "entidades_total": Entidad.objects.count(),
            "entidades_activas": Entidad.objects.filter(activo=True).count(),
            "operaciones_riesgo": RiskOperacion.objects.count(),
            "snapshots": RiskOperationSnapshot.objects.count(),
            "tickets_total": PgoTicket.objects.count(),
            "tickets_abiertos": PgoTicket.objects.exclude(
                estado_normalizado__in=cerrados
            ).count(),
            "tareas_pendientes": Tarea.objects.filter(completada=False).count(),
            "lotes_importacion": DataImportBatch.objects.count(),
            "importaciones_recientes": DataImportBatch.objects.order_by("-fecha_carga")[:5],
        }
        context["breadcrumbs"] = [{"label": "Panel principal"}]
        return context


class AyudaView(LoginRequiredMixin, TemplateView):
    template_name = "portal/ayuda.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "Guía de uso"},
        ]
        return context

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib.auth.mixins import LoginRequiredMixin
00002|from django.views.generic import TemplateView
00003|
00004|from apps.core.models import DataImportBatch, Entidad
00005|from apps.crm.models import Tarea
00006|from apps.pgo.models import PgoTicket
00007|from apps.risk.models import RiskOperacion, RiskOperationSnapshot
00008|
00009|
00010|class SplashView(TemplateView):
00011|    template_name = "portal/splash_wcgone.html"
00012|
00013|
00014|class PanelView(LoginRequiredMixin, TemplateView):
00015|    template_name = "portal/home_wcgone.html"
00016|
00017|    def get_context_data(self, **kwargs):
00018|        context = super().get_context_data(**kwargs)
00019|        cerrados = ["cerrado", "closed", "cerrada"]
00020|        context["stats"] = {
00021|            "entidades_total": Entidad.objects.count(),
00022|            "entidades_activas": Entidad.objects.filter(activo=True).count(),
00023|            "operaciones_riesgo": RiskOperacion.objects.count(),
00024|            "snapshots": RiskOperationSnapshot.objects.count(),
00025|            "tickets_total": PgoTicket.objects.count(),
00026|            "tickets_abiertos": PgoTicket.objects.exclude(
00027|                estado_normalizado__in=cerrados
00028|            ).count(),
00029|            "tareas_pendientes": Tarea.objects.filter(completada=False).count(),
00030|            "lotes_importacion": DataImportBatch.objects.count(),
00031|            "importaciones_recientes": DataImportBatch.objects.order_by("-fecha_carga")[:5],
00032|        }
00033|        context["breadcrumbs"] = [{"label": "Panel principal"}]
00034|        return context
00035|
00036|
00037|class AyudaView(LoginRequiredMixin, TemplateView):
00038|    template_name = "portal/ayuda.html"
00039|
00040|    def get_context_data(self, **kwargs):
00041|        context = super().get_context_data(**kwargs)
00042|        context["breadcrumbs"] = [
00043|            {"label": "Panel principal", "url": "/panel/"},
00044|            {"label": "Guía de uso"},
00045|        ]
00046|        return context

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYi5hdXRoLm1peGlucyBpbXBvcnQgTG9naW5SZXF1aXJlZE1peGluCmZyb20gZGphbmdvLnZpZXdzLmdlbmVyaWMgaW1wb3J0IFRlbXBsYXRlVmlldwoKZnJvbSBhcHBzLmNvcmUubW9kZWxzIGltcG9ydCBEYXRhSW1wb3J0QmF0Y2gsIEVudGlkYWQKZnJvbSBhcHBzLmNybS5tb2RlbHMgaW1wb3J0IFRhcmVhCmZyb20gYXBwcy5wZ28ubW9kZWxzIGltcG9ydCBQZ29UaWNrZXQKZnJvbSBhcHBzLnJpc2subW9kZWxzIGltcG9ydCBSaXNrT3BlcmFjaW9uLCBSaXNrT3BlcmF0aW9uU25hcHNob3QKCgpjbGFzcyBTcGxhc2hWaWV3KFRlbXBsYXRlVmlldyk6CiAgICB0ZW1wbGF0ZV9uYW1lID0gInBvcnRhbC9zcGxhc2hfd2Nnb25lLmh0bWwiCgoKY2xhc3MgUGFuZWxWaWV3KExvZ2luUmVxdWlyZWRNaXhpbiwgVGVtcGxhdGVWaWV3KToKICAgIHRlbXBsYXRlX25hbWUgPSAicG9ydGFsL2hvbWVfd2Nnb25lLmh0bWwiCgogICAgZGVmIGdldF9jb250ZXh0X2RhdGEoc2VsZiwgKiprd2FyZ3MpOgogICAgICAgIGNvbnRleHQgPSBzdXBlcigpLmdldF9jb250ZXh0X2RhdGEoKiprd2FyZ3MpCiAgICAgICAgY2VycmFkb3MgPSBbImNlcnJhZG8iLCAiY2xvc2VkIiwgImNlcnJhZGEiXQogICAgICAgIGNvbnRleHRbInN0YXRzIl0gPSB7CiAgICAgICAgICAgICJlbnRpZGFkZXNfdG90YWwiOiBFbnRpZGFkLm9iamVjdHMuY291bnQoKSwKICAgICAgICAgICAgImVudGlkYWRlc19hY3RpdmFzIjogRW50aWRhZC5vYmplY3RzLmZpbHRlcihhY3Rpdm89VHJ1ZSkuY291bnQoKSwKICAgICAgICAgICAgIm9wZXJhY2lvbmVzX3JpZXNnbyI6IFJpc2tPcGVyYWNpb24ub2JqZWN0cy5jb3VudCgpLAogICAgICAgICAgICAic25hcHNob3RzIjogUmlza09wZXJhdGlvblNuYXBzaG90Lm9iamVjdHMuY291bnQoKSwKICAgICAgICAgICAgInRpY2tldHNfdG90YWwiOiBQZ29UaWNrZXQub2JqZWN0cy5jb3VudCgpLAogICAgICAgICAgICAidGlja2V0c19hYmllcnRvcyI6IFBnb1RpY2tldC5vYmplY3RzLmV4Y2x1ZGUoCiAgICAgICAgICAgICAgICBlc3RhZG9fbm9ybWFsaXphZG9fX2luPWNlcnJhZG9zCiAgICAgICAgICAgICkuY291bnQoKSwKICAgICAgICAgICAgInRhcmVhc19wZW5kaWVudGVzIjogVGFyZWEub2JqZWN0cy5maWx0ZXIoY29tcGxldGFkYT1GYWxzZSkuY291bnQoKSwKICAgICAgICAgICAgImxvdGVzX2ltcG9ydGFjaW9uIjogRGF0YUltcG9ydEJhdGNoLm9iamVjdHMuY291bnQoKSwKICAgICAgICAgICAgImltcG9ydGFjaW9uZXNfcmVjaWVudGVzIjogRGF0YUltcG9ydEJhdGNoLm9iamVjdHMub3JkZXJfYnkoIi1mZWNoYV9jYXJnYSIpWzo1XSwKICAgICAgICB9CiAgICAgICAgY29udGV4dFsiYnJlYWRjcnVtYnMiXSA9IFt7ImxhYmVsIjogIlBhbmVsIHByaW5jaXBhbCJ9XQogICAgICAgIHJldHVybiBjb250ZXh0CgoKY2xhc3MgQXl1ZGFWaWV3KExvZ2luUmVxdWlyZWRNaXhpbiwgVGVtcGxhdGVWaWV3KToKICAgIHRlbXBsYXRlX25hbWUgPSAicG9ydGFsL2F5dWRhLmh0bWwiCgogICAgZGVmIGdldF9jb250ZXh0X2RhdGEoc2VsZiwgKiprd2FyZ3MpOgogICAgICAgIGNvbnRleHQgPSBzdXBlcigpLmdldF9jb250ZXh0X2RhdGEoKiprd2FyZ3MpCiAgICAgICAgY29udGV4dFsiYnJlYWRjcnVtYnMiXSA9IFsKICAgICAgICAgICAgeyJsYWJlbCI6ICJQYW5lbCBwcmluY2lwYWwiLCAidXJsIjogIi9wYW5lbC8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJHdcOtYSBkZSB1c28ifSwKICAgICAgICBdCiAgICAgICAgcmV0dXJuIGNvbnRleHQK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/risk/__init__.py
PATH_JSON="apps/risk/__init__.py"
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
PATH_LITERAL=apps/risk/admin.py
PATH_JSON="apps/risk/admin.py"
FILENAME=admin.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=148
SIZE_BYTES_UTF8=4038
CONTENT_SHA256=1d7e279c423698ce75c1a62398a65c83fb7436b3a3d751c224514932ac538505
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

from .models import (
    ContactoCobranza,
    EstadoFinanciero,
    RiskAlerta,
    RiskOperacion,
    RiskOperationSnapshot,
    RiskPagoProgramado,
    RiskPagoRealizado,
)


class RiskOperationSnapshotInline(admin.TabularInline):
    model = RiskOperationSnapshot
    extra = 0
    fields = ("fecha_snapshot", "estado_operacion", "past_due_balance", "due_days")
    readonly_fields = fields
    can_delete = False
    show_change_link = True


@admin.register(RiskOperacion)
class RiskOperacionAdmin(admin.ModelAdmin):
    list_display = (
        "codigo_operacion",
        "entidad",
        "producto",
        "unidad_negocio",
        "estado",
        "monto_original",
        "fecha_inicio",
    )
    list_filter = ("estado", "unidad_negocio", "moneda")
    search_fields = (
        "codigo_operacion",
        "contrato_numero",
        "entidad__nombre",
        "entidad__nit",
        "asesor",
    )
    autocomplete_fields = ("entidad", "producto", "unidad_negocio")
    inlines = [RiskOperationSnapshotInline]
    ordering = ("entidad__nombre", "codigo_operacion")


@admin.register(RiskOperationSnapshot)
class RiskOperationSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_snapshot",
        "operacion",
        "entidad",
        "estado_operacion",
        "capital_balance",
        "past_due_balance",
        "due_days",
    )
    list_filter = ("fecha_snapshot", "estado_operacion")
    search_fields = (
        "operacion__codigo_operacion",
        "entidad__nombre",
        "entidad__nit",
        "producto_nombre_raw",
    )
    date_hierarchy = "fecha_snapshot"
    autocomplete_fields = ("operacion", "entidad", "import_batch")
    ordering = ("-fecha_snapshot",)


@admin.register(EstadoFinanciero)
class EstadoFinancieroAdmin(admin.ModelAdmin):
    list_display = (
        "entidad",
        "fecha_corte",
        "ventas",
        "utilidad_neta",
        "patrimonio",
        "ebitda",
    )
    list_filter = ("fecha_corte",)
    search_fields = ("entidad__nombre", "entidad__nit", "auditor_contador")
    autocomplete_fields = ("entidad", "import_batch")
    ordering = ("-fecha_corte",)


@admin.register(RiskPagoProgramado)
class RiskPagoProgramadoAdmin(admin.ModelAdmin):
    list_display = (
        "operacion",
        "entidad",
        "fecha_programada",
        "monto_capital",
        "monto_interes",
        "estado",
    )
    list_filter = ("estado", "fecha_programada", "moneda")
    search_fields = ("operacion__codigo_operacion", "entidad__nombre")
    autocomplete_fields = ("operacion", "entidad")
    ordering = ("fecha_programada",)


@admin.register(RiskPagoRealizado)
class RiskPagoRealizadoAdmin(admin.ModelAdmin):
    list_display = (
        "operacion",
        "entidad",
        "fecha_pago",
        "monto_capital",
        "monto_interes",
        "referencia",
    )
    list_filter = ("fecha_pago", "moneda")
    search_fields = ("operacion__codigo_operacion", "entidad__nombre", "referencia")
    autocomplete_fields = ("operacion", "entidad")
    ordering = ("-fecha_pago",)


@admin.register(ContactoCobranza)
class ContactoCobranzaAdmin(admin.ModelAdmin):
    list_display = (
        "fecha",
        "entidad",
        "operacion",
        "tipo_contacto",
        "resultado",
        "fecha_compromiso",
    )
    list_filter = ("tipo_contacto", "fecha")
    search_fields = ("entidad__nombre", "resultado", "acuerdo")
    autocomplete_fields = ("entidad", "operacion", "contacto")
    ordering = ("-fecha",)


@admin.register(RiskAlerta)
class RiskAlertaAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_alerta",
        "entidad",
        "operacion",
        "tipo_alerta",
        "severidad",
        "activa",
        "origen",
    )
    list_filter = ("tipo_alerta", "severidad", "activa", "fecha_alerta")
    search_fields = ("mensaje", "entidad__nombre", "operacion__codigo_operacion")
    autocomplete_fields = ("entidad", "operacion")
    ordering = ("-fecha_alerta",)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib import admin
00002|
00003|from .models import (
00004|    ContactoCobranza,
00005|    EstadoFinanciero,
00006|    RiskAlerta,
00007|    RiskOperacion,
00008|    RiskOperationSnapshot,
00009|    RiskPagoProgramado,
00010|    RiskPagoRealizado,
00011|)
00012|
00013|
00014|class RiskOperationSnapshotInline(admin.TabularInline):
00015|    model = RiskOperationSnapshot
00016|    extra = 0
00017|    fields = ("fecha_snapshot", "estado_operacion", "past_due_balance", "due_days")
00018|    readonly_fields = fields
00019|    can_delete = False
00020|    show_change_link = True
00021|
00022|
00023|@admin.register(RiskOperacion)
00024|class RiskOperacionAdmin(admin.ModelAdmin):
00025|    list_display = (
00026|        "codigo_operacion",
00027|        "entidad",
00028|        "producto",
00029|        "unidad_negocio",
00030|        "estado",
00031|        "monto_original",
00032|        "fecha_inicio",
00033|    )
00034|    list_filter = ("estado", "unidad_negocio", "moneda")
00035|    search_fields = (
00036|        "codigo_operacion",
00037|        "contrato_numero",
00038|        "entidad__nombre",
00039|        "entidad__nit",
00040|        "asesor",
00041|    )
00042|    autocomplete_fields = ("entidad", "producto", "unidad_negocio")
00043|    inlines = [RiskOperationSnapshotInline]
00044|    ordering = ("entidad__nombre", "codigo_operacion")
00045|
00046|
00047|@admin.register(RiskOperationSnapshot)
00048|class RiskOperationSnapshotAdmin(admin.ModelAdmin):
00049|    list_display = (
00050|        "fecha_snapshot",
00051|        "operacion",
00052|        "entidad",
00053|        "estado_operacion",
00054|        "capital_balance",
00055|        "past_due_balance",
00056|        "due_days",
00057|    )
00058|    list_filter = ("fecha_snapshot", "estado_operacion")
00059|    search_fields = (
00060|        "operacion__codigo_operacion",
00061|        "entidad__nombre",
00062|        "entidad__nit",
00063|        "producto_nombre_raw",
00064|    )
00065|    date_hierarchy = "fecha_snapshot"
00066|    autocomplete_fields = ("operacion", "entidad", "import_batch")
00067|    ordering = ("-fecha_snapshot",)
00068|
00069|
00070|@admin.register(EstadoFinanciero)
00071|class EstadoFinancieroAdmin(admin.ModelAdmin):
00072|    list_display = (
00073|        "entidad",
00074|        "fecha_corte",
00075|        "ventas",
00076|        "utilidad_neta",
00077|        "patrimonio",
00078|        "ebitda",
00079|    )
00080|    list_filter = ("fecha_corte",)
00081|    search_fields = ("entidad__nombre", "entidad__nit", "auditor_contador")
00082|    autocomplete_fields = ("entidad", "import_batch")
00083|    ordering = ("-fecha_corte",)
00084|
00085|
00086|@admin.register(RiskPagoProgramado)
00087|class RiskPagoProgramadoAdmin(admin.ModelAdmin):
00088|    list_display = (
00089|        "operacion",
00090|        "entidad",
00091|        "fecha_programada",
00092|        "monto_capital",
00093|        "monto_interes",
00094|        "estado",
00095|    )
00096|    list_filter = ("estado", "fecha_programada", "moneda")
00097|    search_fields = ("operacion__codigo_operacion", "entidad__nombre")
00098|    autocomplete_fields = ("operacion", "entidad")
00099|    ordering = ("fecha_programada",)
00100|
00101|
00102|@admin.register(RiskPagoRealizado)
00103|class RiskPagoRealizadoAdmin(admin.ModelAdmin):
00104|    list_display = (
00105|        "operacion",
00106|        "entidad",
00107|        "fecha_pago",
00108|        "monto_capital",
00109|        "monto_interes",
00110|        "referencia",
00111|    )
00112|    list_filter = ("fecha_pago", "moneda")
00113|    search_fields = ("operacion__codigo_operacion", "entidad__nombre", "referencia")
00114|    autocomplete_fields = ("operacion", "entidad")
00115|    ordering = ("-fecha_pago",)
00116|
00117|
00118|@admin.register(ContactoCobranza)
00119|class ContactoCobranzaAdmin(admin.ModelAdmin):
00120|    list_display = (
00121|        "fecha",
00122|        "entidad",
00123|        "operacion",
00124|        "tipo_contacto",
00125|        "resultado",
00126|        "fecha_compromiso",
00127|    )
00128|    list_filter = ("tipo_contacto", "fecha")
00129|    search_fields = ("entidad__nombre", "resultado", "acuerdo")
00130|    autocomplete_fields = ("entidad", "operacion", "contacto")
00131|    ordering = ("-fecha",)
00132|
00133|
00134|@admin.register(RiskAlerta)
00135|class RiskAlertaAdmin(admin.ModelAdmin):
00136|    list_display = (
00137|        "fecha_alerta",
00138|        "entidad",
00139|        "operacion",
00140|        "tipo_alerta",
00141|        "severidad",
00142|        "activa",
00143|        "origen",
00144|    )
00145|    list_filter = ("tipo_alerta", "severidad", "activa", "fecha_alerta")
00146|    search_fields = ("mensaje", "entidad__nombre", "operacion__codigo_operacion")
00147|    autocomplete_fields = ("entidad", "operacion")
00148|    ordering = ("-fecha_alerta",)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgYWRtaW4KCmZyb20gLm1vZGVscyBpbXBvcnQgKAogICAgQ29udGFjdG9Db2JyYW56YSwKICAgIEVzdGFkb0ZpbmFuY2llcm8sCiAgICBSaXNrQWxlcnRhLAogICAgUmlza09wZXJhY2lvbiwKICAgIFJpc2tPcGVyYXRpb25TbmFwc2hvdCwKICAgIFJpc2tQYWdvUHJvZ3JhbWFkbywKICAgIFJpc2tQYWdvUmVhbGl6YWRvLAopCgoKY2xhc3MgUmlza09wZXJhdGlvblNuYXBzaG90SW5saW5lKGFkbWluLlRhYnVsYXJJbmxpbmUpOgogICAgbW9kZWwgPSBSaXNrT3BlcmF0aW9uU25hcHNob3QKICAgIGV4dHJhID0gMAogICAgZmllbGRzID0gKCJmZWNoYV9zbmFwc2hvdCIsICJlc3RhZG9fb3BlcmFjaW9uIiwgInBhc3RfZHVlX2JhbGFuY2UiLCAiZHVlX2RheXMiKQogICAgcmVhZG9ubHlfZmllbGRzID0gZmllbGRzCiAgICBjYW5fZGVsZXRlID0gRmFsc2UKICAgIHNob3dfY2hhbmdlX2xpbmsgPSBUcnVlCgoKQGFkbWluLnJlZ2lzdGVyKFJpc2tPcGVyYWNpb24pCmNsYXNzIFJpc2tPcGVyYWNpb25BZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgKICAgICAgICAiY29kaWdvX29wZXJhY2lvbiIsCiAgICAgICAgImVudGlkYWQiLAogICAgICAgICJwcm9kdWN0byIsCiAgICAgICAgInVuaWRhZF9uZWdvY2lvIiwKICAgICAgICAiZXN0YWRvIiwKICAgICAgICAibW9udG9fb3JpZ2luYWwiLAogICAgICAgICJmZWNoYV9pbmljaW8iLAogICAgKQogICAgbGlzdF9maWx0ZXIgPSAoImVzdGFkbyIsICJ1bmlkYWRfbmVnb2NpbyIsICJtb25lZGEiKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgKICAgICAgICAiY29kaWdvX29wZXJhY2lvbiIsCiAgICAgICAgImNvbnRyYXRvX251bWVybyIsCiAgICAgICAgImVudGlkYWRfX25vbWJyZSIsCiAgICAgICAgImVudGlkYWRfX25pdCIsCiAgICAgICAgImFzZXNvciIsCiAgICApCiAgICBhdXRvY29tcGxldGVfZmllbGRzID0gKCJlbnRpZGFkIiwgInByb2R1Y3RvIiwgInVuaWRhZF9uZWdvY2lvIikKICAgIGlubGluZXMgPSBbUmlza09wZXJhdGlvblNuYXBzaG90SW5saW5lXQogICAgb3JkZXJpbmcgPSAoImVudGlkYWRfX25vbWJyZSIsICJjb2RpZ29fb3BlcmFjaW9uIikKCgpAYWRtaW4ucmVnaXN0ZXIoUmlza09wZXJhdGlvblNuYXBzaG90KQpjbGFzcyBSaXNrT3BlcmF0aW9uU25hcHNob3RBZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgKICAgICAgICAiZmVjaGFfc25hcHNob3QiLAogICAgICAgICJvcGVyYWNpb24iLAogICAgICAgICJlbnRpZGFkIiwKICAgICAgICAiZXN0YWRvX29wZXJhY2lvbiIsCiAgICAgICAgImNhcGl0YWxfYmFsYW5jZSIsCiAgICAgICAgInBhc3RfZHVlX2JhbGFuY2UiLAogICAgICAgICJkdWVfZGF5cyIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgiZmVjaGFfc25hcHNob3QiLCAiZXN0YWRvX29wZXJhY2lvbiIpCiAgICBzZWFyY2hfZmllbGRzID0gKAogICAgICAgICJvcGVyYWNpb25fX2NvZGlnb19vcGVyYWNpb24iLAogICAgICAgICJlbnRpZGFkX19ub21icmUiLAogICAgICAgICJlbnRpZGFkX19uaXQiLAogICAgICAgICJwcm9kdWN0b19ub21icmVfcmF3IiwKICAgICkKICAgIGRhdGVfaGllcmFyY2h5ID0gImZlY2hhX3NuYXBzaG90IgogICAgYXV0b2NvbXBsZXRlX2ZpZWxkcyA9ICgib3BlcmFjaW9uIiwgImVudGlkYWQiLCAiaW1wb3J0X2JhdGNoIikKICAgIG9yZGVyaW5nID0gKCItZmVjaGFfc25hcHNob3QiLCkKCgpAYWRtaW4ucmVnaXN0ZXIoRXN0YWRvRmluYW5jaWVybykKY2xhc3MgRXN0YWRvRmluYW5jaWVyb0FkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKAogICAgICAgICJlbnRpZGFkIiwKICAgICAgICAiZmVjaGFfY29ydGUiLAogICAgICAgICJ2ZW50YXMiLAogICAgICAgICJ1dGlsaWRhZF9uZXRhIiwKICAgICAgICAicGF0cmltb25pbyIsCiAgICAgICAgImViaXRkYSIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgiZmVjaGFfY29ydGUiLCkKICAgIHNlYXJjaF9maWVsZHMgPSAoImVudGlkYWRfX25vbWJyZSIsICJlbnRpZGFkX19uaXQiLCAiYXVkaXRvcl9jb250YWRvciIpCiAgICBhdXRvY29tcGxldGVfZmllbGRzID0gKCJlbnRpZGFkIiwgImltcG9ydF9iYXRjaCIpCiAgICBvcmRlcmluZyA9ICgiLWZlY2hhX2NvcnRlIiwpCgoKQGFkbWluLnJlZ2lzdGVyKFJpc2tQYWdvUHJvZ3JhbWFkbykKY2xhc3MgUmlza1BhZ29Qcm9ncmFtYWRvQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoCiAgICAgICAgIm9wZXJhY2lvbiIsCiAgICAgICAgImVudGlkYWQiLAogICAgICAgICJmZWNoYV9wcm9ncmFtYWRhIiwKICAgICAgICAibW9udG9fY2FwaXRhbCIsCiAgICAgICAgIm1vbnRvX2ludGVyZXMiLAogICAgICAgICJlc3RhZG8iLAogICAgKQogICAgbGlzdF9maWx0ZXIgPSAoImVzdGFkbyIsICJmZWNoYV9wcm9ncmFtYWRhIiwgIm1vbmVkYSIpCiAgICBzZWFyY2hfZmllbGRzID0gKCJvcGVyYWNpb25fX2NvZGlnb19vcGVyYWNpb24iLCAiZW50aWRhZF9fbm9tYnJlIikKICAgIGF1dG9jb21wbGV0ZV9maWVsZHMgPSAoIm9wZXJhY2lvbiIsICJlbnRpZGFkIikKICAgIG9yZGVyaW5nID0gKCJmZWNoYV9wcm9ncmFtYWRhIiwpCgoKQGFkbWluLnJlZ2lzdGVyKFJpc2tQYWdvUmVhbGl6YWRvKQpjbGFzcyBSaXNrUGFnb1JlYWxpemFkb0FkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKAogICAgICAgICJvcGVyYWNpb24iLAogICAgICAgICJlbnRpZGFkIiwKICAgICAgICAiZmVjaGFfcGFnbyIsCiAgICAgICAgIm1vbnRvX2NhcGl0YWwiLAogICAgICAgICJtb250b19pbnRlcmVzIiwKICAgICAgICAicmVmZXJlbmNpYSIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgiZmVjaGFfcGFnbyIsICJtb25lZGEiKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgib3BlcmFjaW9uX19jb2RpZ29fb3BlcmFjaW9uIiwgImVudGlkYWRfX25vbWJyZSIsICJyZWZlcmVuY2lhIikKICAgIGF1dG9jb21wbGV0ZV9maWVsZHMgPSAoIm9wZXJhY2lvbiIsICJlbnRpZGFkIikKICAgIG9yZGVyaW5nID0gKCItZmVjaGFfcGFnbyIsKQoKCkBhZG1pbi5yZWdpc3RlcihDb250YWN0b0NvYnJhbnphKQpjbGFzcyBDb250YWN0b0NvYnJhbnphQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoCiAgICAgICAgImZlY2hhIiwKICAgICAgICAiZW50aWRhZCIsCiAgICAgICAgIm9wZXJhY2lvbiIsCiAgICAgICAgInRpcG9fY29udGFjdG8iLAogICAgICAgICJyZXN1bHRhZG8iLAogICAgICAgICJmZWNoYV9jb21wcm9taXNvIiwKICAgICkKICAgIGxpc3RfZmlsdGVyID0gKCJ0aXBvX2NvbnRhY3RvIiwgImZlY2hhIikKICAgIHNlYXJjaF9maWVsZHMgPSAoImVudGlkYWRfX25vbWJyZSIsICJyZXN1bHRhZG8iLCAiYWN1ZXJkbyIpCiAgICBhdXRvY29tcGxldGVfZmllbGRzID0gKCJlbnRpZGFkIiwgIm9wZXJhY2lvbiIsICJjb250YWN0byIpCiAgICBvcmRlcmluZyA9ICgiLWZlY2hhIiwpCgoKQGFkbWluLnJlZ2lzdGVyKFJpc2tBbGVydGEpCmNsYXNzIFJpc2tBbGVydGFBZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgKICAgICAgICAiZmVjaGFfYWxlcnRhIiwKICAgICAgICAiZW50aWRhZCIsCiAgICAgICAgIm9wZXJhY2lvbiIsCiAgICAgICAgInRpcG9fYWxlcnRhIiwKICAgICAgICAic2V2ZXJpZGFkIiwKICAgICAgICAiYWN0aXZhIiwKICAgICAgICAib3JpZ2VuIiwKICAgICkKICAgIGxpc3RfZmlsdGVyID0gKCJ0aXBvX2FsZXJ0YSIsICJzZXZlcmlkYWQiLCAiYWN0aXZhIiwgImZlY2hhX2FsZXJ0YSIpCiAgICBzZWFyY2hfZmllbGRzID0gKCJtZW5zYWplIiwgImVudGlkYWRfX25vbWJyZSIsICJvcGVyYWNpb25fX2NvZGlnb19vcGVyYWNpb24iKQogICAgYXV0b2NvbXBsZXRlX2ZpZWxkcyA9ICgiZW50aWRhZCIsICJvcGVyYWNpb24iKQogICAgb3JkZXJpbmcgPSAoIi1mZWNoYV9hbGVydGEiLCkK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/risk/apps.py
PATH_JSON="apps/risk/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=8
SIZE_BYTES_UTF8=209
CONTENT_SHA256=ad562e256d7e1a83bb2ee200a4f81213dc992ecff3290b6c6f451dbe82235b93
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


class RiskConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.risk"
    label = "wcgone_risk"
    verbose_name = "Balón de Riesgo"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class RiskConfig(AppConfig):
00005|    default_auto_field = "django.db.models.BigAutoField"
00006|    name = "apps.risk"
00007|    label = "wcgone_risk"
00008|    verbose_name = "Balón de Riesgo"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgUmlza0NvbmZpZyhBcHBDb25maWcpOgogICAgZGVmYXVsdF9hdXRvX2ZpZWxkID0gImRqYW5nby5kYi5tb2RlbHMuQmlnQXV0b0ZpZWxkIgogICAgbmFtZSA9ICJhcHBzLnJpc2siCiAgICBsYWJlbCA9ICJ3Y2dvbmVfcmlzayIKICAgIHZlcmJvc2VfbmFtZSA9ICJCYWzDs24gZGUgUmllc2dvIgo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/risk/forms.py
PATH_JSON="apps/risk/forms.py"
FILENAME=forms.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=12
SIZE_BYTES_UTF8=408
CONTENT_SHA256=c237da56c754a4e1ff3caf1df2bbca1d2aee6871533bf0f85499c57ef1c30a1a
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

from apps.core.forms import ImportFileForm


class RiskSnapshotImportForm(ImportFileForm):
    fecha_snapshot = forms.DateField(
        required=False,
        label="Fecha de snapshot (opcional)",
        help_text="Si el archivo no trae fecha por fila, use este valor para todas las filas.",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django import forms
00002|
00003|from apps.core.forms import ImportFileForm
00004|
00005|
00006|class RiskSnapshotImportForm(ImportFileForm):
00007|    fecha_snapshot = forms.DateField(
00008|        required=False,
00009|        label="Fecha de snapshot (opcional)",
00010|        help_text="Si el archivo no trae fecha por fila, use este valor para todas las filas.",
00011|        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
00012|    )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28gaW1wb3J0IGZvcm1zCgpmcm9tIGFwcHMuY29yZS5mb3JtcyBpbXBvcnQgSW1wb3J0RmlsZUZvcm0KCgpjbGFzcyBSaXNrU25hcHNob3RJbXBvcnRGb3JtKEltcG9ydEZpbGVGb3JtKToKICAgIGZlY2hhX3NuYXBzaG90ID0gZm9ybXMuRGF0ZUZpZWxkKAogICAgICAgIHJlcXVpcmVkPUZhbHNlLAogICAgICAgIGxhYmVsPSJGZWNoYSBkZSBzbmFwc2hvdCAob3BjaW9uYWwpIiwKICAgICAgICBoZWxwX3RleHQ9IlNpIGVsIGFyY2hpdm8gbm8gdHJhZSBmZWNoYSBwb3IgZmlsYSwgdXNlIGVzdGUgdmFsb3IgcGFyYSB0b2RhcyBsYXMgZmlsYXMuIiwKICAgICAgICB3aWRnZXQ9Zm9ybXMuRGF0ZUlucHV0KGF0dHJzPXsiY2xhc3MiOiAiZm9ybS1jb250cm9sIiwgInR5cGUiOiAiZGF0ZSJ9KSwKICAgICkK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/risk/imports/__init__.py
PATH_JSON="apps/risk/imports/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=4
SIZE_BYTES_UTF8=212
CONTENT_SHA256=9c305f91cb9a1ea2c44f534c44f5b4fa03bef045a2c33c6efef31590af9c99e6
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
from apps.risk.imports.estados_financieros import import_estados_financieros
from apps.risk.imports.snapshots import import_snapshots_leasing

__all__ = ["import_snapshots_leasing", "import_estados_financieros"]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from apps.risk.imports.estados_financieros import import_estados_financieros
00002|from apps.risk.imports.snapshots import import_snapshots_leasing
00003|
00004|__all__ = ["import_snapshots_leasing", "import_estados_financieros"]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBhcHBzLnJpc2suaW1wb3J0cy5lc3RhZG9zX2ZpbmFuY2llcm9zIGltcG9ydCBpbXBvcnRfZXN0YWRvc19maW5hbmNpZXJvcwpmcm9tIGFwcHMucmlzay5pbXBvcnRzLnNuYXBzaG90cyBpbXBvcnQgaW1wb3J0X3NuYXBzaG90c19sZWFzaW5nCgpfX2FsbF9fID0gWyJpbXBvcnRfc25hcHNob3RzX2xlYXNpbmciLCAiaW1wb3J0X2VzdGFkb3NfZmluYW5jaWVyb3MiXQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/risk/imports/estados_financieros.py
PATH_JSON="apps/risk/imports/estados_financieros.py"
FILENAME=estados_financieros.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=85
SIZE_BYTES_UTF8=2777
CONTENT_SHA256=a47674692bfdfb4b18de40d8df662ed3dc5dee8b4bee0a437b0922ddb2c70765
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
"""Importador Risk: estados financieros básicos."""

from __future__ import annotations

from datetime import date, datetime

import pandas as pd

from apps.core.imports.base import run_import_batch
from apps.core.imports.columns import normalize_columns, pick, pick_decimal, require_any
from apps.core.imports.entities import ensure_entidad_from_row
from apps.risk.models import EstadoFinanciero


MODULO = "risk"
TIPO = "estados_financieros"


def _parse_date(value: str) -> date | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m"):
        try:
            parsed = datetime.strptime(value[:10], fmt).date()
            return parsed.replace(day=1) if fmt == "%Y-%m" else parsed
        except ValueError:
            continue
    try:
        return pd.to_datetime(value).date()
    except Exception:
        return None


def _preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)
    require_any(
        df,
        [
            ["nit", "cliente", "nombre", "razon_social"],
            ["fecha_corte", "periodo", "anio_mes", "fecha"],
        ],
    )
    return df


def import_estados_financieros(user, uploaded_file):
    uploaded_file.seek(0)

    def handler(row: pd.Series, errors: list[str], batch=None):
        entidad = ensure_entidad_from_row(row, errors)
        if not entidad:
            return None
        fecha_raw = pick(row, "fecha_corte", "periodo", "anio_mes", "fecha", "corte")
        fecha = _parse_date(fecha_raw)
        if not fecha:
            errors.append("Fecha de corte inválida.")
            return None
        defaults = {
            "auditor_contador": pick(row, "auditor_contador", "auditor"),
            "ventas": pick_decimal(row, "ventas"),
            "utilidad_neta": pick_decimal(row, "utilidad_neta", "utilidad"),
            "activo_corriente": pick_decimal(row, "activo_corriente"),
            "activo_no_corriente": pick_decimal(row, "activo_no_corriente"),
            "pasivo_corriente": pick_decimal(row, "pasivo_corriente"),
            "pasivo_no_corriente": pick_decimal(row, "pasivo_no_corriente"),
            "patrimonio": pick_decimal(row, "patrimonio"),
            "ebitda": pick_decimal(row, "ebitda"),
            "observaciones": pick(row, "observaciones", "notas"),
            "import_batch": batch,
        }
        _, created = EstadoFinanciero.objects.update_or_create(
            entidad=entidad,
            fecha_corte=fecha,
            defaults=defaults,
        )
        return created, not created

    return run_import_batch(
        user=user,
        modulo=MODULO,
        tipo_importacion=TIPO,
        uploaded_file=uploaded_file,
        preprocess=_preprocess,
        row_handler=handler,
    )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Importador Risk: estados financieros básicos."""
00002|
00003|from __future__ import annotations
00004|
00005|from datetime import date, datetime
00006|
00007|import pandas as pd
00008|
00009|from apps.core.imports.base import run_import_batch
00010|from apps.core.imports.columns import normalize_columns, pick, pick_decimal, require_any
00011|from apps.core.imports.entities import ensure_entidad_from_row
00012|from apps.risk.models import EstadoFinanciero
00013|
00014|
00015|MODULO = "risk"
00016|TIPO = "estados_financieros"
00017|
00018|
00019|def _parse_date(value: str) -> date | None:
00020|    if not value:
00021|        return None
00022|    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m"):
00023|        try:
00024|            parsed = datetime.strptime(value[:10], fmt).date()
00025|            return parsed.replace(day=1) if fmt == "%Y-%m" else parsed
00026|        except ValueError:
00027|            continue
00028|    try:
00029|        return pd.to_datetime(value).date()
00030|    except Exception:
00031|        return None
00032|
00033|
00034|def _preprocess(df: pd.DataFrame) -> pd.DataFrame:
00035|    df = normalize_columns(df)
00036|    require_any(
00037|        df,
00038|        [
00039|            ["nit", "cliente", "nombre", "razon_social"],
00040|            ["fecha_corte", "periodo", "anio_mes", "fecha"],
00041|        ],
00042|    )
00043|    return df
00044|
00045|
00046|def import_estados_financieros(user, uploaded_file):
00047|    uploaded_file.seek(0)
00048|
00049|    def handler(row: pd.Series, errors: list[str], batch=None):
00050|        entidad = ensure_entidad_from_row(row, errors)
00051|        if not entidad:
00052|            return None
00053|        fecha_raw = pick(row, "fecha_corte", "periodo", "anio_mes", "fecha", "corte")
00054|        fecha = _parse_date(fecha_raw)
00055|        if not fecha:
00056|            errors.append("Fecha de corte inválida.")
00057|            return None
00058|        defaults = {
00059|            "auditor_contador": pick(row, "auditor_contador", "auditor"),
00060|            "ventas": pick_decimal(row, "ventas"),
00061|            "utilidad_neta": pick_decimal(row, "utilidad_neta", "utilidad"),
00062|            "activo_corriente": pick_decimal(row, "activo_corriente"),
00063|            "activo_no_corriente": pick_decimal(row, "activo_no_corriente"),
00064|            "pasivo_corriente": pick_decimal(row, "pasivo_corriente"),
00065|            "pasivo_no_corriente": pick_decimal(row, "pasivo_no_corriente"),
00066|            "patrimonio": pick_decimal(row, "patrimonio"),
00067|            "ebitda": pick_decimal(row, "ebitda"),
00068|            "observaciones": pick(row, "observaciones", "notas"),
00069|            "import_batch": batch,
00070|        }
00071|        _, created = EstadoFinanciero.objects.update_or_create(
00072|            entidad=entidad,
00073|            fecha_corte=fecha,
00074|            defaults=defaults,
00075|        )
00076|        return created, not created
00077|
00078|    return run_import_batch(
00079|        user=user,
00080|        modulo=MODULO,
00081|        tipo_importacion=TIPO,
00082|        uploaded_file=uploaded_file,
00083|        preprocess=_preprocess,
00084|        row_handler=handler,
00085|    )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiSW1wb3J0YWRvciBSaXNrOiBlc3RhZG9zIGZpbmFuY2llcm9zIGLDoXNpY29zLiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKZnJvbSBkYXRldGltZSBpbXBvcnQgZGF0ZSwgZGF0ZXRpbWUKCmltcG9ydCBwYW5kYXMgYXMgcGQKCmZyb20gYXBwcy5jb3JlLmltcG9ydHMuYmFzZSBpbXBvcnQgcnVuX2ltcG9ydF9iYXRjaApmcm9tIGFwcHMuY29yZS5pbXBvcnRzLmNvbHVtbnMgaW1wb3J0IG5vcm1hbGl6ZV9jb2x1bW5zLCBwaWNrLCBwaWNrX2RlY2ltYWwsIHJlcXVpcmVfYW55CmZyb20gYXBwcy5jb3JlLmltcG9ydHMuZW50aXRpZXMgaW1wb3J0IGVuc3VyZV9lbnRpZGFkX2Zyb21fcm93CmZyb20gYXBwcy5yaXNrLm1vZGVscyBpbXBvcnQgRXN0YWRvRmluYW5jaWVybwoKCk1PRFVMTyA9ICJyaXNrIgpUSVBPID0gImVzdGFkb3NfZmluYW5jaWVyb3MiCgoKZGVmIF9wYXJzZV9kYXRlKHZhbHVlOiBzdHIpIC0+IGRhdGUgfCBOb25lOgogICAgaWYgbm90IHZhbHVlOgogICAgICAgIHJldHVybiBOb25lCiAgICBmb3IgZm10IGluICgiJVktJW0tJWQiLCAiJWQvJW0vJVkiLCAiJW0vJWQvJVkiLCAiJVktJW0iKToKICAgICAgICB0cnk6CiAgICAgICAgICAgIHBhcnNlZCA9IGRhdGV0aW1lLnN0cnB0aW1lKHZhbHVlWzoxMF0sIGZtdCkuZGF0ZSgpCiAgICAgICAgICAgIHJldHVybiBwYXJzZWQucmVwbGFjZShkYXk9MSkgaWYgZm10ID09ICIlWS0lbSIgZWxzZSBwYXJzZWQKICAgICAgICBleGNlcHQgVmFsdWVFcnJvcjoKICAgICAgICAgICAgY29udGludWUKICAgIHRyeToKICAgICAgICByZXR1cm4gcGQudG9fZGF0ZXRpbWUodmFsdWUpLmRhdGUoKQogICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICByZXR1cm4gTm9uZQoKCmRlZiBfcHJlcHJvY2VzcyhkZjogcGQuRGF0YUZyYW1lKSAtPiBwZC5EYXRhRnJhbWU6CiAgICBkZiA9IG5vcm1hbGl6ZV9jb2x1bW5zKGRmKQogICAgcmVxdWlyZV9hbnkoCiAgICAgICAgZGYsCiAgICAgICAgWwogICAgICAgICAgICBbIm5pdCIsICJjbGllbnRlIiwgIm5vbWJyZSIsICJyYXpvbl9zb2NpYWwiXSwKICAgICAgICAgICAgWyJmZWNoYV9jb3J0ZSIsICJwZXJpb2RvIiwgImFuaW9fbWVzIiwgImZlY2hhIl0sCiAgICAgICAgXSwKICAgICkKICAgIHJldHVybiBkZgoKCmRlZiBpbXBvcnRfZXN0YWRvc19maW5hbmNpZXJvcyh1c2VyLCB1cGxvYWRlZF9maWxlKToKICAgIHVwbG9hZGVkX2ZpbGUuc2VlaygwKQoKICAgIGRlZiBoYW5kbGVyKHJvdzogcGQuU2VyaWVzLCBlcnJvcnM6IGxpc3Rbc3RyXSwgYmF0Y2g9Tm9uZSk6CiAgICAgICAgZW50aWRhZCA9IGVuc3VyZV9lbnRpZGFkX2Zyb21fcm93KHJvdywgZXJyb3JzKQogICAgICAgIGlmIG5vdCBlbnRpZGFkOgogICAgICAgICAgICByZXR1cm4gTm9uZQogICAgICAgIGZlY2hhX3JhdyA9IHBpY2socm93LCAiZmVjaGFfY29ydGUiLCAicGVyaW9kbyIsICJhbmlvX21lcyIsICJmZWNoYSIsICJjb3J0ZSIpCiAgICAgICAgZmVjaGEgPSBfcGFyc2VfZGF0ZShmZWNoYV9yYXcpCiAgICAgICAgaWYgbm90IGZlY2hhOgogICAgICAgICAgICBlcnJvcnMuYXBwZW5kKCJGZWNoYSBkZSBjb3J0ZSBpbnbDoWxpZGEuIikKICAgICAgICAgICAgcmV0dXJuIE5vbmUKICAgICAgICBkZWZhdWx0cyA9IHsKICAgICAgICAgICAgImF1ZGl0b3JfY29udGFkb3IiOiBwaWNrKHJvdywgImF1ZGl0b3JfY29udGFkb3IiLCAiYXVkaXRvciIpLAogICAgICAgICAgICAidmVudGFzIjogcGlja19kZWNpbWFsKHJvdywgInZlbnRhcyIpLAogICAgICAgICAgICAidXRpbGlkYWRfbmV0YSI6IHBpY2tfZGVjaW1hbChyb3csICJ1dGlsaWRhZF9uZXRhIiwgInV0aWxpZGFkIiksCiAgICAgICAgICAgICJhY3Rpdm9fY29ycmllbnRlIjogcGlja19kZWNpbWFsKHJvdywgImFjdGl2b19jb3JyaWVudGUiKSwKICAgICAgICAgICAgImFjdGl2b19ub19jb3JyaWVudGUiOiBwaWNrX2RlY2ltYWwocm93LCAiYWN0aXZvX25vX2NvcnJpZW50ZSIpLAogICAgICAgICAgICAicGFzaXZvX2NvcnJpZW50ZSI6IHBpY2tfZGVjaW1hbChyb3csICJwYXNpdm9fY29ycmllbnRlIiksCiAgICAgICAgICAgICJwYXNpdm9fbm9fY29ycmllbnRlIjogcGlja19kZWNpbWFsKHJvdywgInBhc2l2b19ub19jb3JyaWVudGUiKSwKICAgICAgICAgICAgInBhdHJpbW9uaW8iOiBwaWNrX2RlY2ltYWwocm93LCAicGF0cmltb25pbyIpLAogICAgICAgICAgICAiZWJpdGRhIjogcGlja19kZWNpbWFsKHJvdywgImViaXRkYSIpLAogICAgICAgICAgICAib2JzZXJ2YWNpb25lcyI6IHBpY2socm93LCAib2JzZXJ2YWNpb25lcyIsICJub3RhcyIpLAogICAgICAgICAgICAiaW1wb3J0X2JhdGNoIjogYmF0Y2gsCiAgICAgICAgfQogICAgICAgIF8sIGNyZWF0ZWQgPSBFc3RhZG9GaW5hbmNpZXJvLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgZW50aWRhZD1lbnRpZGFkLAogICAgICAgICAgICBmZWNoYV9jb3J0ZT1mZWNoYSwKICAgICAgICAgICAgZGVmYXVsdHM9ZGVmYXVsdHMsCiAgICAgICAgKQogICAgICAgIHJldHVybiBjcmVhdGVkLCBub3QgY3JlYXRlZAoKICAgIHJldHVybiBydW5faW1wb3J0X2JhdGNoKAogICAgICAgIHVzZXI9dXNlciwKICAgICAgICBtb2R1bG89TU9EVUxPLAogICAgICAgIHRpcG9faW1wb3J0YWNpb249VElQTywKICAgICAgICB1cGxvYWRlZF9maWxlPXVwbG9hZGVkX2ZpbGUsCiAgICAgICAgcHJlcHJvY2Vzcz1fcHJlcHJvY2VzcywKICAgICAgICByb3dfaGFuZGxlcj1oYW5kbGVyLAogICAgKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/risk/imports/snapshots.py
PATH_JSON="apps/risk/imports/snapshots.py"
FILENAME=snapshots.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=152
SIZE_BYTES_UTF8=5521
CONTENT_SHA256=21840996d99a2e5d350837ee0572062c2be4c44bcbbf2c2769be2553cb30b835
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
"""Importador Risk: snapshots operativos tipo leasing."""

from __future__ import annotations

import re
from datetime import date, datetime
from decimal import Decimal

import pandas as pd

from apps.core.imports.base import run_import_batch, row_to_json
from apps.core.imports.columns import normalize_columns, pick, pick_decimal, pick_int, require_any
from apps.core.imports.entities import ensure_entidad_from_row, resolve_unidad
from apps.core.models import Producto
from apps.risk.models import RiskOperacion, RiskOperationSnapshot


MODULO = "risk"
TIPO = "snapshots_leasing"


def _parse_date(value: str) -> date | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(value[:19], fmt).date()
        except ValueError:
            continue
    try:
        return pd.to_datetime(value).date()
    except Exception:
        return None


def _slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "", value.upper())[:30] or "GENERICO"


def _preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)
    require_any(
        df,
        [
            ["cliente", "nombre", "razon_social", "nombre_cliente"],
            [
                "operacion",
                "codigo_operacion",
                "referencia_operacion",
                "contrato",
                "no_operacion",
                "no_contrato",
            ],
        ],
    )
    return df


def import_snapshots_leasing(user, uploaded_file, fecha_snapshot_param: str | None = None):
    uploaded_file.seek(0)
    archivo_nombre = uploaded_file.name

    def handler(row: pd.Series, errors: list[str], batch=None):
        entidad = ensure_entidad_from_row(row, errors)
        if not entidad:
            return None
        codigo_operacion = pick(
            row,
            "operacion",
            "codigo_operacion",
            "referencia_operacion",
            "contrato",
            "no_operacion",
            "no_contrato",
        )
        if not codigo_operacion:
            errors.append("Falta código de operación.")
            return None
        fecha_raw = pick(
            row,
            "fecha_snapshot",
            "fecha_corte",
            "al_31_mayo",
            "fecha",
            "corte",
            "record_date",
        )
        fecha = _parse_date(fecha_snapshot_param or fecha_raw)
        if not fecha:
            errors.append("Falta fecha de snapshot válida.")
            return None
        unidad = resolve_unidad(pick(row, "unidad", "une", "unidad_negocio") or "LEASING")
        producto_nombre = pick(row, "producto", "producto_nombre", "tipo_producto") or "Leasing"
        producto, _ = Producto.objects.get_or_create(
            codigo=_slug(producto_nombre),
            defaults={"nombre": producto_nombre[:100], "activo": True},
        )
        operacion, op_created = RiskOperacion.objects.update_or_create(
            entidad=entidad,
            codigo_operacion=codigo_operacion,
            defaults={
                "producto": producto,
                "unidad_negocio": unidad,
                "contrato_numero": pick(row, "contrato", "no_contrato", "contrato_numero"),
                "asesor": pick(row, "asesor", "ejecutivo"),
                "moneda": pick(row, "moneda") or "GTQ",
                "estado": pick(row, "estado_operacion", "estado"),
            },
        )
        snapshot_defaults = {
            "entidad": entidad,
            "record_date_raw": fecha_raw,
            "estado_operacion": pick(row, "estado_operacion", "estado"),
            "producto_nombre_raw": producto_nombre,
            "monthly_rent": pick_decimal(row, "monthly_rent", "renta_mensual", "renta"),
            "capital_balance": pick_decimal(
                row, "capital_balance", "saldo_capital", "saldo", "saldo_total"
            ),
            "outstanding_installments": pick_decimal(
                row, "outstanding_installments", "cuotas_pendientes", "cuotas"
            ),
            "interest_balance": pick_decimal(row, "interest_balance", "saldo_interes", "intereses"),
            "insurance_balance": pick_decimal(row, "insurance_balance", "seguro"),
            "other_charges_balance": pick_decimal(row, "other_charges_balance", "otros_cargos"),
            "past_due_balance": pick_decimal(
                row, "past_due_balance", "saldo_vencido", "monto_vencido", "vencido"
            ),
            "due_days": pick_int(row, "due_days", "dias_mora", "dias_atraso", "dias_de_mora"),
            "purchase_option_value": pick_decimal(row, "purchase_option_value", "opcion_compra"),
            "initial_rent_value": pick_decimal(row, "initial_rent_value", "renta_inicial"),
            "total_rent_value": pick_decimal(row, "total_rent_value", "renta_total"),
            "archivo_origen": archivo_nombre,
            "import_batch": batch,
            "payload_raw_json": row_to_json(row),
        }
        _, snap_created = RiskOperationSnapshot.objects.update_or_create(
            operacion=operacion,
            fecha_snapshot=fecha,
            defaults=snapshot_defaults,
        )
        if op_created or snap_created:
            return True, False
        return False, True

    return run_import_batch(
        user=user,
        modulo=MODULO,
        tipo_importacion=TIPO,
        uploaded_file=uploaded_file,
        preprocess=_preprocess,
        row_handler=handler,
    )

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Importador Risk: snapshots operativos tipo leasing."""
00002|
00003|from __future__ import annotations
00004|
00005|import re
00006|from datetime import date, datetime
00007|from decimal import Decimal
00008|
00009|import pandas as pd
00010|
00011|from apps.core.imports.base import run_import_batch, row_to_json
00012|from apps.core.imports.columns import normalize_columns, pick, pick_decimal, pick_int, require_any
00013|from apps.core.imports.entities import ensure_entidad_from_row, resolve_unidad
00014|from apps.core.models import Producto
00015|from apps.risk.models import RiskOperacion, RiskOperationSnapshot
00016|
00017|
00018|MODULO = "risk"
00019|TIPO = "snapshots_leasing"
00020|
00021|
00022|def _parse_date(value: str) -> date | None:
00023|    if not value:
00024|        return None
00025|    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S"):
00026|        try:
00027|            return datetime.strptime(value[:19], fmt).date()
00028|        except ValueError:
00029|            continue
00030|    try:
00031|        return pd.to_datetime(value).date()
00032|    except Exception:
00033|        return None
00034|
00035|
00036|def _slug(value: str) -> str:
00037|    return re.sub(r"[^A-Za-z0-9]+", "", value.upper())[:30] or "GENERICO"
00038|
00039|
00040|def _preprocess(df: pd.DataFrame) -> pd.DataFrame:
00041|    df = normalize_columns(df)
00042|    require_any(
00043|        df,
00044|        [
00045|            ["cliente", "nombre", "razon_social", "nombre_cliente"],
00046|            [
00047|                "operacion",
00048|                "codigo_operacion",
00049|                "referencia_operacion",
00050|                "contrato",
00051|                "no_operacion",
00052|                "no_contrato",
00053|            ],
00054|        ],
00055|    )
00056|    return df
00057|
00058|
00059|def import_snapshots_leasing(user, uploaded_file, fecha_snapshot_param: str | None = None):
00060|    uploaded_file.seek(0)
00061|    archivo_nombre = uploaded_file.name
00062|
00063|    def handler(row: pd.Series, errors: list[str], batch=None):
00064|        entidad = ensure_entidad_from_row(row, errors)
00065|        if not entidad:
00066|            return None
00067|        codigo_operacion = pick(
00068|            row,
00069|            "operacion",
00070|            "codigo_operacion",
00071|            "referencia_operacion",
00072|            "contrato",
00073|            "no_operacion",
00074|            "no_contrato",
00075|        )
00076|        if not codigo_operacion:
00077|            errors.append("Falta código de operación.")
00078|            return None
00079|        fecha_raw = pick(
00080|            row,
00081|            "fecha_snapshot",
00082|            "fecha_corte",
00083|            "al_31_mayo",
00084|            "fecha",
00085|            "corte",
00086|            "record_date",
00087|        )
00088|        fecha = _parse_date(fecha_snapshot_param or fecha_raw)
00089|        if not fecha:
00090|            errors.append("Falta fecha de snapshot válida.")
00091|            return None
00092|        unidad = resolve_unidad(pick(row, "unidad", "une", "unidad_negocio") or "LEASING")
00093|        producto_nombre = pick(row, "producto", "producto_nombre", "tipo_producto") or "Leasing"
00094|        producto, _ = Producto.objects.get_or_create(
00095|            codigo=_slug(producto_nombre),
00096|            defaults={"nombre": producto_nombre[:100], "activo": True},
00097|        )
00098|        operacion, op_created = RiskOperacion.objects.update_or_create(
00099|            entidad=entidad,
00100|            codigo_operacion=codigo_operacion,
00101|            defaults={
00102|                "producto": producto,
00103|                "unidad_negocio": unidad,
00104|                "contrato_numero": pick(row, "contrato", "no_contrato", "contrato_numero"),
00105|                "asesor": pick(row, "asesor", "ejecutivo"),
00106|                "moneda": pick(row, "moneda") or "GTQ",
00107|                "estado": pick(row, "estado_operacion", "estado"),
00108|            },
00109|        )
00110|        snapshot_defaults = {
00111|            "entidad": entidad,
00112|            "record_date_raw": fecha_raw,
00113|            "estado_operacion": pick(row, "estado_operacion", "estado"),
00114|            "producto_nombre_raw": producto_nombre,
00115|            "monthly_rent": pick_decimal(row, "monthly_rent", "renta_mensual", "renta"),
00116|            "capital_balance": pick_decimal(
00117|                row, "capital_balance", "saldo_capital", "saldo", "saldo_total"
00118|            ),
00119|            "outstanding_installments": pick_decimal(
00120|                row, "outstanding_installments", "cuotas_pendientes", "cuotas"
00121|            ),
00122|            "interest_balance": pick_decimal(row, "interest_balance", "saldo_interes", "intereses"),
00123|            "insurance_balance": pick_decimal(row, "insurance_balance", "seguro"),
00124|            "other_charges_balance": pick_decimal(row, "other_charges_balance", "otros_cargos"),
00125|            "past_due_balance": pick_decimal(
00126|                row, "past_due_balance", "saldo_vencido", "monto_vencido", "vencido"
00127|            ),
00128|            "due_days": pick_int(row, "due_days", "dias_mora", "dias_atraso", "dias_de_mora"),
00129|            "purchase_option_value": pick_decimal(row, "purchase_option_value", "opcion_compra"),
00130|            "initial_rent_value": pick_decimal(row, "initial_rent_value", "renta_inicial"),
00131|            "total_rent_value": pick_decimal(row, "total_rent_value", "renta_total"),
00132|            "archivo_origen": archivo_nombre,
00133|            "import_batch": batch,
00134|            "payload_raw_json": row_to_json(row),
00135|        }
00136|        _, snap_created = RiskOperationSnapshot.objects.update_or_create(
00137|            operacion=operacion,
00138|            fecha_snapshot=fecha,
00139|            defaults=snapshot_defaults,
00140|        )
00141|        if op_created or snap_created:
00142|            return True, False
00143|        return False, True
00144|
00145|    return run_import_batch(
00146|        user=user,
00147|        modulo=MODULO,
00148|        tipo_importacion=TIPO,
00149|        uploaded_file=uploaded_file,
00150|        preprocess=_preprocess,
00151|        row_handler=handler,
00152|    )

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiSW1wb3J0YWRvciBSaXNrOiBzbmFwc2hvdHMgb3BlcmF0aXZvcyB0aXBvIGxlYXNpbmcuIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgppbXBvcnQgcmUKZnJvbSBkYXRldGltZSBpbXBvcnQgZGF0ZSwgZGF0ZXRpbWUKZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsCgppbXBvcnQgcGFuZGFzIGFzIHBkCgpmcm9tIGFwcHMuY29yZS5pbXBvcnRzLmJhc2UgaW1wb3J0IHJ1bl9pbXBvcnRfYmF0Y2gsIHJvd190b19qc29uCmZyb20gYXBwcy5jb3JlLmltcG9ydHMuY29sdW1ucyBpbXBvcnQgbm9ybWFsaXplX2NvbHVtbnMsIHBpY2ssIHBpY2tfZGVjaW1hbCwgcGlja19pbnQsIHJlcXVpcmVfYW55CmZyb20gYXBwcy5jb3JlLmltcG9ydHMuZW50aXRpZXMgaW1wb3J0IGVuc3VyZV9lbnRpZGFkX2Zyb21fcm93LCByZXNvbHZlX3VuaWRhZApmcm9tIGFwcHMuY29yZS5tb2RlbHMgaW1wb3J0IFByb2R1Y3RvCmZyb20gYXBwcy5yaXNrLm1vZGVscyBpbXBvcnQgUmlza09wZXJhY2lvbiwgUmlza09wZXJhdGlvblNuYXBzaG90CgoKTU9EVUxPID0gInJpc2siClRJUE8gPSAic25hcHNob3RzX2xlYXNpbmciCgoKZGVmIF9wYXJzZV9kYXRlKHZhbHVlOiBzdHIpIC0+IGRhdGUgfCBOb25lOgogICAgaWYgbm90IHZhbHVlOgogICAgICAgIHJldHVybiBOb25lCiAgICBmb3IgZm10IGluICgiJVktJW0tJWQiLCAiJWQvJW0vJVkiLCAiJW0vJWQvJVkiLCAiJVktJW0tJWQgJUg6JU06JVMiKToKICAgICAgICB0cnk6CiAgICAgICAgICAgIHJldHVybiBkYXRldGltZS5zdHJwdGltZSh2YWx1ZVs6MTldLCBmbXQpLmRhdGUoKQogICAgICAgIGV4Y2VwdCBWYWx1ZUVycm9yOgogICAgICAgICAgICBjb250aW51ZQogICAgdHJ5OgogICAgICAgIHJldHVybiBwZC50b19kYXRldGltZSh2YWx1ZSkuZGF0ZSgpCiAgICBleGNlcHQgRXhjZXB0aW9uOgogICAgICAgIHJldHVybiBOb25lCgoKZGVmIF9zbHVnKHZhbHVlOiBzdHIpIC0+IHN0cjoKICAgIHJldHVybiByZS5zdWIociJbXkEtWmEtejAtOV0rIiwgIiIsIHZhbHVlLnVwcGVyKCkpWzozMF0gb3IgIkdFTkVSSUNPIgoKCmRlZiBfcHJlcHJvY2VzcyhkZjogcGQuRGF0YUZyYW1lKSAtPiBwZC5EYXRhRnJhbWU6CiAgICBkZiA9IG5vcm1hbGl6ZV9jb2x1bW5zKGRmKQogICAgcmVxdWlyZV9hbnkoCiAgICAgICAgZGYsCiAgICAgICAgWwogICAgICAgICAgICBbImNsaWVudGUiLCAibm9tYnJlIiwgInJhem9uX3NvY2lhbCIsICJub21icmVfY2xpZW50ZSJdLAogICAgICAgICAgICBbCiAgICAgICAgICAgICAgICAib3BlcmFjaW9uIiwKICAgICAgICAgICAgICAgICJjb2RpZ29fb3BlcmFjaW9uIiwKICAgICAgICAgICAgICAgICJyZWZlcmVuY2lhX29wZXJhY2lvbiIsCiAgICAgICAgICAgICAgICAiY29udHJhdG8iLAogICAgICAgICAgICAgICAgIm5vX29wZXJhY2lvbiIsCiAgICAgICAgICAgICAgICAibm9fY29udHJhdG8iLAogICAgICAgICAgICBdLAogICAgICAgIF0sCiAgICApCiAgICByZXR1cm4gZGYKCgpkZWYgaW1wb3J0X3NuYXBzaG90c19sZWFzaW5nKHVzZXIsIHVwbG9hZGVkX2ZpbGUsIGZlY2hhX3NuYXBzaG90X3BhcmFtOiBzdHIgfCBOb25lID0gTm9uZSk6CiAgICB1cGxvYWRlZF9maWxlLnNlZWsoMCkKICAgIGFyY2hpdm9fbm9tYnJlID0gdXBsb2FkZWRfZmlsZS5uYW1lCgogICAgZGVmIGhhbmRsZXIocm93OiBwZC5TZXJpZXMsIGVycm9yczogbGlzdFtzdHJdLCBiYXRjaD1Ob25lKToKICAgICAgICBlbnRpZGFkID0gZW5zdXJlX2VudGlkYWRfZnJvbV9yb3cocm93LCBlcnJvcnMpCiAgICAgICAgaWYgbm90IGVudGlkYWQ6CiAgICAgICAgICAgIHJldHVybiBOb25lCiAgICAgICAgY29kaWdvX29wZXJhY2lvbiA9IHBpY2soCiAgICAgICAgICAgIHJvdywKICAgICAgICAgICAgIm9wZXJhY2lvbiIsCiAgICAgICAgICAgICJjb2RpZ29fb3BlcmFjaW9uIiwKICAgICAgICAgICAgInJlZmVyZW5jaWFfb3BlcmFjaW9uIiwKICAgICAgICAgICAgImNvbnRyYXRvIiwKICAgICAgICAgICAgIm5vX29wZXJhY2lvbiIsCiAgICAgICAgICAgICJub19jb250cmF0byIsCiAgICAgICAgKQogICAgICAgIGlmIG5vdCBjb2RpZ29fb3BlcmFjaW9uOgogICAgICAgICAgICBlcnJvcnMuYXBwZW5kKCJGYWx0YSBjw7NkaWdvIGRlIG9wZXJhY2nDs24uIikKICAgICAgICAgICAgcmV0dXJuIE5vbmUKICAgICAgICBmZWNoYV9yYXcgPSBwaWNrKAogICAgICAgICAgICByb3csCiAgICAgICAgICAgICJmZWNoYV9zbmFwc2hvdCIsCiAgICAgICAgICAgICJmZWNoYV9jb3J0ZSIsCiAgICAgICAgICAgICJhbF8zMV9tYXlvIiwKICAgICAgICAgICAgImZlY2hhIiwKICAgICAgICAgICAgImNvcnRlIiwKICAgICAgICAgICAgInJlY29yZF9kYXRlIiwKICAgICAgICApCiAgICAgICAgZmVjaGEgPSBfcGFyc2VfZGF0ZShmZWNoYV9zbmFwc2hvdF9wYXJhbSBvciBmZWNoYV9yYXcpCiAgICAgICAgaWYgbm90IGZlY2hhOgogICAgICAgICAgICBlcnJvcnMuYXBwZW5kKCJGYWx0YSBmZWNoYSBkZSBzbmFwc2hvdCB2w6FsaWRhLiIpCiAgICAgICAgICAgIHJldHVybiBOb25lCiAgICAgICAgdW5pZGFkID0gcmVzb2x2ZV91bmlkYWQocGljayhyb3csICJ1bmlkYWQiLCAidW5lIiwgInVuaWRhZF9uZWdvY2lvIikgb3IgIkxFQVNJTkciKQogICAgICAgIHByb2R1Y3RvX25vbWJyZSA9IHBpY2socm93LCAicHJvZHVjdG8iLCAicHJvZHVjdG9fbm9tYnJlIiwgInRpcG9fcHJvZHVjdG8iKSBvciAiTGVhc2luZyIKICAgICAgICBwcm9kdWN0bywgXyA9IFByb2R1Y3RvLm9iamVjdHMuZ2V0X29yX2NyZWF0ZSgKICAgICAgICAgICAgY29kaWdvPV9zbHVnKHByb2R1Y3RvX25vbWJyZSksCiAgICAgICAgICAgIGRlZmF1bHRzPXsibm9tYnJlIjogcHJvZHVjdG9fbm9tYnJlWzoxMDBdLCAiYWN0aXZvIjogVHJ1ZX0sCiAgICAgICAgKQogICAgICAgIG9wZXJhY2lvbiwgb3BfY3JlYXRlZCA9IFJpc2tPcGVyYWNpb24ub2JqZWN0cy51cGRhdGVfb3JfY3JlYXRlKAogICAgICAgICAgICBlbnRpZGFkPWVudGlkYWQsCiAgICAgICAgICAgIGNvZGlnb19vcGVyYWNpb249Y29kaWdvX29wZXJhY2lvbiwKICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgInByb2R1Y3RvIjogcHJvZHVjdG8sCiAgICAgICAgICAgICAgICAidW5pZGFkX25lZ29jaW8iOiB1bmlkYWQsCiAgICAgICAgICAgICAgICAiY29udHJhdG9fbnVtZXJvIjogcGljayhyb3csICJjb250cmF0byIsICJub19jb250cmF0byIsICJjb250cmF0b19udW1lcm8iKSwKICAgICAgICAgICAgICAgICJhc2Vzb3IiOiBwaWNrKHJvdywgImFzZXNvciIsICJlamVjdXRpdm8iKSwKICAgICAgICAgICAgICAgICJtb25lZGEiOiBwaWNrKHJvdywgIm1vbmVkYSIpIG9yICJHVFEiLAogICAgICAgICAgICAgICAgImVzdGFkbyI6IHBpY2socm93LCAiZXN0YWRvX29wZXJhY2lvbiIsICJlc3RhZG8iKSwKICAgICAgICAgICAgfSwKICAgICAgICApCiAgICAgICAgc25hcHNob3RfZGVmYXVsdHMgPSB7CiAgICAgICAgICAgICJlbnRpZGFkIjogZW50aWRhZCwKICAgICAgICAgICAgInJlY29yZF9kYXRlX3JhdyI6IGZlY2hhX3JhdywKICAgICAgICAgICAgImVzdGFkb19vcGVyYWNpb24iOiBwaWNrKHJvdywgImVzdGFkb19vcGVyYWNpb24iLCAiZXN0YWRvIiksCiAgICAgICAgICAgICJwcm9kdWN0b19ub21icmVfcmF3IjogcHJvZHVjdG9fbm9tYnJlLAogICAgICAgICAgICAibW9udGhseV9yZW50IjogcGlja19kZWNpbWFsKHJvdywgIm1vbnRobHlfcmVudCIsICJyZW50YV9tZW5zdWFsIiwgInJlbnRhIiksCiAgICAgICAgICAgICJjYXBpdGFsX2JhbGFuY2UiOiBwaWNrX2RlY2ltYWwoCiAgICAgICAgICAgICAgICByb3csICJjYXBpdGFsX2JhbGFuY2UiLCAic2FsZG9fY2FwaXRhbCIsICJzYWxkbyIsICJzYWxkb190b3RhbCIKICAgICAgICAgICAgKSwKICAgICAgICAgICAgIm91dHN0YW5kaW5nX2luc3RhbGxtZW50cyI6IHBpY2tfZGVjaW1hbCgKICAgICAgICAgICAgICAgIHJvdywgIm91dHN0YW5kaW5nX2luc3RhbGxtZW50cyIsICJjdW90YXNfcGVuZGllbnRlcyIsICJjdW90YXMiCiAgICAgICAgICAgICksCiAgICAgICAgICAgICJpbnRlcmVzdF9iYWxhbmNlIjogcGlja19kZWNpbWFsKHJvdywgImludGVyZXN0X2JhbGFuY2UiLCAic2FsZG9faW50ZXJlcyIsICJpbnRlcmVzZXMiKSwKICAgICAgICAgICAgImluc3VyYW5jZV9iYWxhbmNlIjogcGlja19kZWNpbWFsKHJvdywgImluc3VyYW5jZV9iYWxhbmNlIiwgInNlZ3VybyIpLAogICAgICAgICAgICAib3RoZXJfY2hhcmdlc19iYWxhbmNlIjogcGlja19kZWNpbWFsKHJvdywgIm90aGVyX2NoYXJnZXNfYmFsYW5jZSIsICJvdHJvc19jYXJnb3MiKSwKICAgICAgICAgICAgInBhc3RfZHVlX2JhbGFuY2UiOiBwaWNrX2RlY2ltYWwoCiAgICAgICAgICAgICAgICByb3csICJwYXN0X2R1ZV9iYWxhbmNlIiwgInNhbGRvX3ZlbmNpZG8iLCAibW9udG9fdmVuY2lkbyIsICJ2ZW5jaWRvIgogICAgICAgICAgICApLAogICAgICAgICAgICAiZHVlX2RheXMiOiBwaWNrX2ludChyb3csICJkdWVfZGF5cyIsICJkaWFzX21vcmEiLCAiZGlhc19hdHJhc28iLCAiZGlhc19kZV9tb3JhIiksCiAgICAgICAgICAgICJwdXJjaGFzZV9vcHRpb25fdmFsdWUiOiBwaWNrX2RlY2ltYWwocm93LCAicHVyY2hhc2Vfb3B0aW9uX3ZhbHVlIiwgIm9wY2lvbl9jb21wcmEiKSwKICAgICAgICAgICAgImluaXRpYWxfcmVudF92YWx1ZSI6IHBpY2tfZGVjaW1hbChyb3csICJpbml0aWFsX3JlbnRfdmFsdWUiLCAicmVudGFfaW5pY2lhbCIpLAogICAgICAgICAgICAidG90YWxfcmVudF92YWx1ZSI6IHBpY2tfZGVjaW1hbChyb3csICJ0b3RhbF9yZW50X3ZhbHVlIiwgInJlbnRhX3RvdGFsIiksCiAgICAgICAgICAgICJhcmNoaXZvX29yaWdlbiI6IGFyY2hpdm9fbm9tYnJlLAogICAgICAgICAgICAiaW1wb3J0X2JhdGNoIjogYmF0Y2gsCiAgICAgICAgICAgICJwYXlsb2FkX3Jhd19qc29uIjogcm93X3RvX2pzb24ocm93KSwKICAgICAgICB9CiAgICAgICAgXywgc25hcF9jcmVhdGVkID0gUmlza09wZXJhdGlvblNuYXBzaG90Lm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICAgICAgb3BlcmFjaW9uPW9wZXJhY2lvbiwKICAgICAgICAgICAgZmVjaGFfc25hcHNob3Q9ZmVjaGEsCiAgICAgICAgICAgIGRlZmF1bHRzPXNuYXBzaG90X2RlZmF1bHRzLAogICAgICAgICkKICAgICAgICBpZiBvcF9jcmVhdGVkIG9yIHNuYXBfY3JlYXRlZDoKICAgICAgICAgICAgcmV0dXJuIFRydWUsIEZhbHNlCiAgICAgICAgcmV0dXJuIEZhbHNlLCBUcnVlCgogICAgcmV0dXJuIHJ1bl9pbXBvcnRfYmF0Y2goCiAgICAgICAgdXNlcj11c2VyLAogICAgICAgIG1vZHVsbz1NT0RVTE8sCiAgICAgICAgdGlwb19pbXBvcnRhY2lvbj1USVBPLAogICAgICAgIHVwbG9hZGVkX2ZpbGU9dXBsb2FkZWRfZmlsZSwKICAgICAgICBwcmVwcm9jZXNzPV9wcmVwcm9jZXNzLAogICAgICAgIHJvd19oYW5kbGVyPWhhbmRsZXIsCiAgICApCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/risk/models.py
PATH_JSON="apps/risk/models.py"
FILENAME=models.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=258
SIZE_BYTES_UTF8=10044
CONTENT_SHA256=a24d36c4a972b89e70f6eb57590217136062a9d5c9ba6ff52df5274b500bb653
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

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.conf import settings
00002|from django.db import models
00003|
00004|
00005|class RiskOperacion(models.Model):
00006|    entidad = models.ForeignKey(
00007|        "wcgone_core.Entidad",
00008|        on_delete=models.CASCADE,
00009|        related_name="operaciones_riesgo",
00010|    )
00011|    producto = models.ForeignKey(
00012|        "wcgone_core.Producto",
00013|        on_delete=models.SET_NULL,
00014|        null=True,
00015|        blank=True,
00016|        related_name="operaciones_riesgo",
00017|    )
00018|    unidad_negocio = models.ForeignKey(
00019|        "wcgone_core.UnidadNegocio",
00020|        on_delete=models.SET_NULL,
00021|        null=True,
00022|        blank=True,
00023|        related_name="operaciones_riesgo",
00024|    )
00025|    codigo_operacion = models.CharField(max_length=100, db_index=True)
00026|    contrato_numero = models.CharField(max_length=100, blank=True, db_index=True)
00027|    asesor = models.CharField(max_length=150, blank=True)
00028|    moneda = models.CharField(max_length=10, blank=True)
00029|    fecha_inicio = models.DateField(null=True, blank=True)
00030|    monto_original = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00031|    estado = models.CharField(max_length=50, blank=True)
00032|    notas = models.TextField(blank=True)
00033|
00034|    class Meta:
00035|        ordering = ["entidad__nombre", "codigo_operacion"]
00036|        verbose_name = "Operación de riesgo"
00037|        verbose_name_plural = "Operaciones de riesgo"
00038|        constraints = [
00039|            models.UniqueConstraint(
00040|                fields=["entidad", "codigo_operacion"],
00041|                name="uniq_risk_operacion_entidad_codigo",
00042|            ),
00043|        ]
00044|
00045|    def __str__(self):
00046|        return f"{self.codigo_operacion} — {self.entidad}"
00047|
00048|
00049|class RiskOperationSnapshot(models.Model):
00050|    operacion = models.ForeignKey(
00051|        RiskOperacion,
00052|        on_delete=models.CASCADE,
00053|        related_name="snapshots",
00054|    )
00055|    entidad = models.ForeignKey(
00056|        "wcgone_core.Entidad",
00057|        on_delete=models.CASCADE,
00058|        related_name="risk_snapshots",
00059|    )
00060|    fecha_snapshot = models.DateField(db_index=True)
00061|    record_date_raw = models.CharField(max_length=100, blank=True)
00062|    estado_operacion = models.CharField(max_length=100, blank=True)
00063|    producto_nombre_raw = models.CharField(max_length=100, blank=True)
00064|    monthly_rent = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00065|    capital_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00066|    outstanding_installments = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00067|    interest_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00068|    insurance_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00069|    other_charges_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00070|    past_due_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00071|    due_days = models.IntegerField(null=True, blank=True)
00072|    purchase_option_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00073|    initial_rent_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00074|    total_rent_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00075|    archivo_origen = models.CharField(max_length=255, blank=True)
00076|    import_batch = models.ForeignKey(
00077|        "wcgone_core.DataImportBatch",
00078|        on_delete=models.SET_NULL,
00079|        null=True,
00080|        blank=True,
00081|        related_name="risk_snapshots",
00082|    )
00083|    payload_raw_json = models.JSONField(default=dict, blank=True)
00084|
00085|    class Meta:
00086|        ordering = ["-fecha_snapshot", "operacion_id"]
00087|        verbose_name = "Snapshot operativo de riesgo"
00088|        verbose_name_plural = "Snapshots operativos de riesgo"
00089|        constraints = [
00090|            models.UniqueConstraint(
00091|                fields=["operacion", "fecha_snapshot"],
00092|                name="uniq_risk_snapshot_operacion_fecha",
00093|            ),
00094|        ]
00095|
00096|    def __str__(self):
00097|        return f"{self.operacion.codigo_operacion} — {self.fecha_snapshot}"
00098|
00099|
00100|class EstadoFinanciero(models.Model):
00101|    entidad = models.ForeignKey(
00102|        "wcgone_core.Entidad",
00103|        on_delete=models.CASCADE,
00104|        related_name="estados_financieros",
00105|    )
00106|    fecha_corte = models.DateField()
00107|    auditor_contador = models.CharField(max_length=255, blank=True)
00108|    ventas = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00109|    utilidad_neta = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00110|    activo_corriente = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00111|    activo_no_corriente = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00112|    pasivo_corriente = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00113|    pasivo_no_corriente = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00114|    patrimonio = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00115|    ebitda = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00116|    observaciones = models.TextField(blank=True)
00117|    import_batch = models.ForeignKey(
00118|        "wcgone_core.DataImportBatch",
00119|        on_delete=models.SET_NULL,
00120|        null=True,
00121|        blank=True,
00122|        related_name="estados_financieros",
00123|    )
00124|
00125|    class Meta:
00126|        ordering = ["-fecha_corte", "entidad__nombre"]
00127|        verbose_name = "Estado financiero"
00128|        verbose_name_plural = "Estados financieros"
00129|        indexes = [
00130|            models.Index(fields=["entidad", "fecha_corte"]),
00131|        ]
00132|
00133|    def __str__(self):
00134|        return f"{self.entidad} — {self.fecha_corte}"
00135|
00136|
00137|class RiskPagoProgramado(models.Model):
00138|    operacion = models.ForeignKey(
00139|        RiskOperacion,
00140|        on_delete=models.CASCADE,
00141|        related_name="pagos_programados",
00142|    )
00143|    entidad = models.ForeignKey(
00144|        "wcgone_core.Entidad",
00145|        on_delete=models.CASCADE,
00146|        related_name="pagos_programados",
00147|    )
00148|    fecha_programada = models.DateField()
00149|    monto_capital = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00150|    monto_interes = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00151|    monto_mora = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00152|    monto_otros = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00153|    moneda = models.CharField(max_length=10, blank=True)
00154|    estado = models.CharField(max_length=50, blank=True)
00155|    notas = models.TextField(blank=True)
00156|
00157|    class Meta:
00158|        ordering = ["fecha_programada"]
00159|        verbose_name = "Pago programado"
00160|        verbose_name_plural = "Pagos programados"
00161|
00162|    def __str__(self):
00163|        return f"{self.operacion.codigo_operacion} — {self.fecha_programada}"
00164|
00165|
00166|class RiskPagoRealizado(models.Model):
00167|    operacion = models.ForeignKey(
00168|        RiskOperacion,
00169|        on_delete=models.CASCADE,
00170|        related_name="pagos_realizados",
00171|    )
00172|    entidad = models.ForeignKey(
00173|        "wcgone_core.Entidad",
00174|        on_delete=models.CASCADE,
00175|        related_name="pagos_realizados",
00176|    )
00177|    fecha_pago = models.DateField()
00178|    monto_capital = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00179|    monto_interes = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00180|    monto_mora = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00181|    monto_otros = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
00182|    moneda = models.CharField(max_length=10, blank=True)
00183|    referencia = models.CharField(max_length=100, blank=True)
00184|    notas = models.TextField(blank=True)
00185|
00186|    class Meta:
00187|        ordering = ["-fecha_pago"]
00188|        verbose_name = "Pago realizado"
00189|        verbose_name_plural = "Pagos realizados"
00190|
00191|    def __str__(self):
00192|        return f"{self.operacion.codigo_operacion} — {self.fecha_pago}"
00193|
00194|
00195|class ContactoCobranza(models.Model):
00196|    entidad = models.ForeignKey(
00197|        "wcgone_core.Entidad",
00198|        on_delete=models.CASCADE,
00199|        related_name="contactos_cobranza",
00200|    )
00201|    operacion = models.ForeignKey(
00202|        RiskOperacion,
00203|        on_delete=models.SET_NULL,
00204|        null=True,
00205|        blank=True,
00206|        related_name="contactos_cobranza",
00207|    )
00208|    contacto = models.ForeignKey(
00209|        "wcgone_core.Contacto",
00210|        on_delete=models.SET_NULL,
00211|        null=True,
00212|        blank=True,
00213|        related_name="contactos_cobranza",
00214|    )
00215|    fecha = models.DateField()
00216|    tipo_contacto = models.CharField(max_length=50)
00217|    resultado = models.CharField(max_length=255, blank=True)
00218|    acuerdo = models.TextField(blank=True)
00219|    fecha_compromiso = models.DateField(null=True, blank=True)
00220|    notas = models.TextField(blank=True)
00221|
00222|    class Meta:
00223|        ordering = ["-fecha", "entidad__nombre"]
00224|        verbose_name = "Contacto de cobranza"
00225|        verbose_name_plural = "Contactos de cobranza"
00226|
00227|    def __str__(self):
00228|        return f"{self.entidad} — {self.fecha}"
00229|
00230|
00231|class RiskAlerta(models.Model):
00232|    entidad = models.ForeignKey(
00233|        "wcgone_core.Entidad",
00234|        on_delete=models.CASCADE,
00235|        related_name="alertas_riesgo",
00236|    )
00237|    operacion = models.ForeignKey(
00238|        RiskOperacion,
00239|        on_delete=models.SET_NULL,
00240|        null=True,
00241|        blank=True,
00242|        related_name="alertas",
00243|    )
00244|    fecha_alerta = models.DateField(db_index=True)
00245|    tipo_alerta = models.CharField(max_length=50)
00246|    severidad = models.CharField(max_length=30)
00247|    mensaje = models.TextField()
00248|    activa = models.BooleanField(default=True)
00249|    origen = models.CharField(max_length=100, blank=True)
00250|    detalle_json = models.JSONField(default=dict, blank=True)
00251|
00252|    class Meta:
00253|        ordering = ["-fecha_alerta", "-id"]
00254|        verbose_name = "Alerta de riesgo"
00255|        verbose_name_plural = "Alertas de riesgo"
00256|
00257|    def __str__(self):
00258|        return f"{self.entidad} — {self.tipo_alerta}"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29uZiBpbXBvcnQgc2V0dGluZ3MKZnJvbSBkamFuZ28uZGIgaW1wb3J0IG1vZGVscwoKCmNsYXNzIFJpc2tPcGVyYWNpb24obW9kZWxzLk1vZGVsKToKICAgIGVudGlkYWQgPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICAid2Nnb25lX2NvcmUuRW50aWRhZCIsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLAogICAgICAgIHJlbGF0ZWRfbmFtZT0ib3BlcmFjaW9uZXNfcmllc2dvIiwKICAgICkKICAgIHByb2R1Y3RvID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgIndjZ29uZV9jb3JlLlByb2R1Y3RvIiwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0ib3BlcmFjaW9uZXNfcmllc2dvIiwKICAgICkKICAgIHVuaWRhZF9uZWdvY2lvID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgIndjZ29uZV9jb3JlLlVuaWRhZE5lZ29jaW8iLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJvcGVyYWNpb25lc19yaWVzZ28iLAogICAgKQogICAgY29kaWdvX29wZXJhY2lvbiA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMDAsIGRiX2luZGV4PVRydWUpCiAgICBjb250cmF0b19udW1lcm8gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAwLCBibGFuaz1UcnVlLCBkYl9pbmRleD1UcnVlKQogICAgYXNlc29yID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTE1MCwgYmxhbms9VHJ1ZSkKICAgIG1vbmVkYSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMCwgYmxhbms9VHJ1ZSkKICAgIGZlY2hhX2luaWNpbyA9IG1vZGVscy5EYXRlRmllbGQobnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgbW9udG9fb3JpZ2luYWwgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTIsIG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIGVzdGFkbyA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD01MCwgYmxhbms9VHJ1ZSkKICAgIG5vdGFzID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbImVudGlkYWRfX25vbWJyZSIsICJjb2RpZ29fb3BlcmFjaW9uIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiT3BlcmFjacOzbiBkZSByaWVzZ28iCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJPcGVyYWNpb25lcyBkZSByaWVzZ28iCiAgICAgICAgY29uc3RyYWludHMgPSBbCiAgICAgICAgICAgIG1vZGVscy5VbmlxdWVDb25zdHJhaW50KAogICAgICAgICAgICAgICAgZmllbGRzPVsiZW50aWRhZCIsICJjb2RpZ29fb3BlcmFjaW9uIl0sCiAgICAgICAgICAgICAgICBuYW1lPSJ1bmlxX3Jpc2tfb3BlcmFjaW9uX2VudGlkYWRfY29kaWdvIiwKICAgICAgICAgICAgKSwKICAgICAgICBdCgogICAgZGVmIF9fc3RyX18oc2VsZik6CiAgICAgICAgcmV0dXJuIGYie3NlbGYuY29kaWdvX29wZXJhY2lvbn0g4oCUIHtzZWxmLmVudGlkYWR9IgoKCmNsYXNzIFJpc2tPcGVyYXRpb25TbmFwc2hvdChtb2RlbHMuTW9kZWwpOgogICAgb3BlcmFjaW9uID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgUmlza09wZXJhY2lvbiwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJzbmFwc2hvdHMiLAogICAgKQogICAgZW50aWRhZCA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgICJ3Y2dvbmVfY29yZS5FbnRpZGFkIiwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJyaXNrX3NuYXBzaG90cyIsCiAgICApCiAgICBmZWNoYV9zbmFwc2hvdCA9IG1vZGVscy5EYXRlRmllbGQoZGJfaW5kZXg9VHJ1ZSkKICAgIHJlY29yZF9kYXRlX3JhdyA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMDAsIGJsYW5rPVRydWUpCiAgICBlc3RhZG9fb3BlcmFjaW9uID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwMCwgYmxhbms9VHJ1ZSkKICAgIHByb2R1Y3RvX25vbWJyZV9yYXcgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAwLCBibGFuaz1UcnVlKQogICAgbW9udGhseV9yZW50ID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTE4LCBkZWNpbWFsX3BsYWNlcz0yLCBudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBjYXBpdGFsX2JhbGFuY2UgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTIsIG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIG91dHN0YW5kaW5nX2luc3RhbGxtZW50cyA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9MiwgbnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgaW50ZXJlc3RfYmFsYW5jZSA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9MiwgbnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgaW5zdXJhbmNlX2JhbGFuY2UgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTIsIG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIG90aGVyX2NoYXJnZXNfYmFsYW5jZSA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9MiwgbnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgcGFzdF9kdWVfYmFsYW5jZSA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9MiwgbnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgZHVlX2RheXMgPSBtb2RlbHMuSW50ZWdlckZpZWxkKG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIHB1cmNoYXNlX29wdGlvbl92YWx1ZSA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9MiwgbnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgaW5pdGlhbF9yZW50X3ZhbHVlID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTE4LCBkZWNpbWFsX3BsYWNlcz0yLCBudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICB0b3RhbF9yZW50X3ZhbHVlID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTE4LCBkZWNpbWFsX3BsYWNlcz0yLCBudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBhcmNoaXZvX29yaWdlbiA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yNTUsIGJsYW5rPVRydWUpCiAgICBpbXBvcnRfYmF0Y2ggPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICAid2Nnb25lX2NvcmUuRGF0YUltcG9ydEJhdGNoIiwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0icmlza19zbmFwc2hvdHMiLAogICAgKQogICAgcGF5bG9hZF9yYXdfanNvbiA9IG1vZGVscy5KU09ORmllbGQoZGVmYXVsdD1kaWN0LCBibGFuaz1UcnVlKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbIi1mZWNoYV9zbmFwc2hvdCIsICJvcGVyYWNpb25faWQiXQogICAgICAgIHZlcmJvc2VfbmFtZSA9ICJTbmFwc2hvdCBvcGVyYXRpdm8gZGUgcmllc2dvIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiU25hcHNob3RzIG9wZXJhdGl2b3MgZGUgcmllc2dvIgogICAgICAgIGNvbnN0cmFpbnRzID0gWwogICAgICAgICAgICBtb2RlbHMuVW5pcXVlQ29uc3RyYWludCgKICAgICAgICAgICAgICAgIGZpZWxkcz1bIm9wZXJhY2lvbiIsICJmZWNoYV9zbmFwc2hvdCJdLAogICAgICAgICAgICAgICAgbmFtZT0idW5pcV9yaXNrX3NuYXBzaG90X29wZXJhY2lvbl9mZWNoYSIsCiAgICAgICAgICAgICksCiAgICAgICAgXQoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLm9wZXJhY2lvbi5jb2RpZ29fb3BlcmFjaW9ufSDigJQge3NlbGYuZmVjaGFfc25hcHNob3R9IgoKCmNsYXNzIEVzdGFkb0ZpbmFuY2llcm8obW9kZWxzLk1vZGVsKToKICAgIGVudGlkYWQgPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICAid2Nnb25lX2NvcmUuRW50aWRhZCIsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLAogICAgICAgIHJlbGF0ZWRfbmFtZT0iZXN0YWRvc19maW5hbmNpZXJvcyIsCiAgICApCiAgICBmZWNoYV9jb3J0ZSA9IG1vZGVscy5EYXRlRmllbGQoKQogICAgYXVkaXRvcl9jb250YWRvciA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yNTUsIGJsYW5rPVRydWUpCiAgICB2ZW50YXMgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTIsIG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIHV0aWxpZGFkX25ldGEgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTIsIG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIGFjdGl2b19jb3JyaWVudGUgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTIsIG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIGFjdGl2b19ub19jb3JyaWVudGUgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTIsIG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIHBhc2l2b19jb3JyaWVudGUgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTIsIG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIHBhc2l2b19ub19jb3JyaWVudGUgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTIsIG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIHBhdHJpbW9uaW8gPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTIsIG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIGViaXRkYSA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9MiwgbnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgb2JzZXJ2YWNpb25lcyA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKICAgIGltcG9ydF9iYXRjaCA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgICJ3Y2dvbmVfY29yZS5EYXRhSW1wb3J0QmF0Y2giLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJlc3RhZG9zX2ZpbmFuY2llcm9zIiwKICAgICkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIG9yZGVyaW5nID0gWyItZmVjaGFfY29ydGUiLCAiZW50aWRhZF9fbm9tYnJlIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiRXN0YWRvIGZpbmFuY2llcm8iCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJFc3RhZG9zIGZpbmFuY2llcm9zIgogICAgICAgIGluZGV4ZXMgPSBbCiAgICAgICAgICAgIG1vZGVscy5JbmRleChmaWVsZHM9WyJlbnRpZGFkIiwgImZlY2hhX2NvcnRlIl0pLAogICAgICAgIF0KCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi5lbnRpZGFkfSDigJQge3NlbGYuZmVjaGFfY29ydGV9IgoKCmNsYXNzIFJpc2tQYWdvUHJvZ3JhbWFkbyhtb2RlbHMuTW9kZWwpOgogICAgb3BlcmFjaW9uID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgUmlza09wZXJhY2lvbiwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJwYWdvc19wcm9ncmFtYWRvcyIsCiAgICApCiAgICBlbnRpZGFkID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgIndjZ29uZV9jb3JlLkVudGlkYWQiLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSwKICAgICAgICByZWxhdGVkX25hbWU9InBhZ29zX3Byb2dyYW1hZG9zIiwKICAgICkKICAgIGZlY2hhX3Byb2dyYW1hZGEgPSBtb2RlbHMuRGF0ZUZpZWxkKCkKICAgIG1vbnRvX2NhcGl0YWwgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTIsIG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIG1vbnRvX2ludGVyZXMgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTIsIG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIG1vbnRvX21vcmEgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTgsIGRlY2ltYWxfcGxhY2VzPTIsIG51bGw9VHJ1ZSwgYmxhbms9VHJ1ZSkKICAgIG1vbnRvX290cm9zID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTE4LCBkZWNpbWFsX3BsYWNlcz0yLCBudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBtb25lZGEgPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAsIGJsYW5rPVRydWUpCiAgICBlc3RhZG8gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9NTAsIGJsYW5rPVRydWUpCiAgICBub3RhcyA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIG9yZGVyaW5nID0gWyJmZWNoYV9wcm9ncmFtYWRhIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiUGFnbyBwcm9ncmFtYWRvIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiUGFnb3MgcHJvZ3JhbWFkb3MiCgogICAgZGVmIF9fc3RyX18oc2VsZik6CiAgICAgICAgcmV0dXJuIGYie3NlbGYub3BlcmFjaW9uLmNvZGlnb19vcGVyYWNpb259IOKAlCB7c2VsZi5mZWNoYV9wcm9ncmFtYWRhfSIKCgpjbGFzcyBSaXNrUGFnb1JlYWxpemFkbyhtb2RlbHMuTW9kZWwpOgogICAgb3BlcmFjaW9uID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgUmlza09wZXJhY2lvbiwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJwYWdvc19yZWFsaXphZG9zIiwKICAgICkKICAgIGVudGlkYWQgPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICAid2Nnb25lX2NvcmUuRW50aWRhZCIsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLAogICAgICAgIHJlbGF0ZWRfbmFtZT0icGFnb3NfcmVhbGl6YWRvcyIsCiAgICApCiAgICBmZWNoYV9wYWdvID0gbW9kZWxzLkRhdGVGaWVsZCgpCiAgICBtb250b19jYXBpdGFsID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTE4LCBkZWNpbWFsX3BsYWNlcz0yLCBudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBtb250b19pbnRlcmVzID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTE4LCBkZWNpbWFsX3BsYWNlcz0yLCBudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBtb250b19tb3JhID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTE4LCBkZWNpbWFsX3BsYWNlcz0yLCBudWxsPVRydWUsIGJsYW5rPVRydWUpCiAgICBtb250b19vdHJvcyA9IG1vZGVscy5EZWNpbWFsRmllbGQobWF4X2RpZ2l0cz0xOCwgZGVjaW1hbF9wbGFjZXM9MiwgbnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgbW9uZWRhID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTEwLCBibGFuaz1UcnVlKQogICAgcmVmZXJlbmNpYSA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0xMDAsIGJsYW5rPVRydWUpCiAgICBub3RhcyA9IG1vZGVscy5UZXh0RmllbGQoYmxhbms9VHJ1ZSkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIG9yZGVyaW5nID0gWyItZmVjaGFfcGFnbyJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIlBhZ28gcmVhbGl6YWRvIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiUGFnb3MgcmVhbGl6YWRvcyIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi5vcGVyYWNpb24uY29kaWdvX29wZXJhY2lvbn0g4oCUIHtzZWxmLmZlY2hhX3BhZ299IgoKCmNsYXNzIENvbnRhY3RvQ29icmFuemEobW9kZWxzLk1vZGVsKToKICAgIGVudGlkYWQgPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICAid2Nnb25lX2NvcmUuRW50aWRhZCIsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5DQVNDQURFLAogICAgICAgIHJlbGF0ZWRfbmFtZT0iY29udGFjdG9zX2NvYnJhbnphIiwKICAgICkKICAgIG9wZXJhY2lvbiA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIFJpc2tPcGVyYWNpb24sCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5TRVRfTlVMTCwKICAgICAgICBudWxsPVRydWUsCiAgICAgICAgYmxhbms9VHJ1ZSwKICAgICAgICByZWxhdGVkX25hbWU9ImNvbnRhY3Rvc19jb2JyYW56YSIsCiAgICApCiAgICBjb250YWN0byA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgICJ3Y2dvbmVfY29yZS5Db250YWN0byIsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5TRVRfTlVMTCwKICAgICAgICBudWxsPVRydWUsCiAgICAgICAgYmxhbms9VHJ1ZSwKICAgICAgICByZWxhdGVkX25hbWU9ImNvbnRhY3Rvc19jb2JyYW56YSIsCiAgICApCiAgICBmZWNoYSA9IG1vZGVscy5EYXRlRmllbGQoKQogICAgdGlwb19jb250YWN0byA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD01MCkKICAgIHJlc3VsdGFkbyA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD0yNTUsIGJsYW5rPVRydWUpCiAgICBhY3VlcmRvID0gbW9kZWxzLlRleHRGaWVsZChibGFuaz1UcnVlKQogICAgZmVjaGFfY29tcHJvbWlzbyA9IG1vZGVscy5EYXRlRmllbGQobnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgbm90YXMgPSBtb2RlbHMuVGV4dEZpZWxkKGJsYW5rPVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICBvcmRlcmluZyA9IFsiLWZlY2hhIiwgImVudGlkYWRfX25vbWJyZSJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIkNvbnRhY3RvIGRlIGNvYnJhbnphIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiQ29udGFjdG9zIGRlIGNvYnJhbnphIgoKICAgIGRlZiBfX3N0cl9fKHNlbGYpOgogICAgICAgIHJldHVybiBmIntzZWxmLmVudGlkYWR9IOKAlCB7c2VsZi5mZWNoYX0iCgoKY2xhc3MgUmlza0FsZXJ0YShtb2RlbHMuTW9kZWwpOgogICAgZW50aWRhZCA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgICJ3Y2dvbmVfY29yZS5FbnRpZGFkIiwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJhbGVydGFzX3JpZXNnbyIsCiAgICApCiAgICBvcGVyYWNpb24gPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICBSaXNrT3BlcmFjaW9uLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuU0VUX05VTEwsCiAgICAgICAgbnVsbD1UcnVlLAogICAgICAgIGJsYW5rPVRydWUsCiAgICAgICAgcmVsYXRlZF9uYW1lPSJhbGVydGFzIiwKICAgICkKICAgIGZlY2hhX2FsZXJ0YSA9IG1vZGVscy5EYXRlRmllbGQoZGJfaW5kZXg9VHJ1ZSkKICAgIHRpcG9fYWxlcnRhID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTUwKQogICAgc2V2ZXJpZGFkID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTMwKQogICAgbWVuc2FqZSA9IG1vZGVscy5UZXh0RmllbGQoKQogICAgYWN0aXZhID0gbW9kZWxzLkJvb2xlYW5GaWVsZChkZWZhdWx0PVRydWUpCiAgICBvcmlnZW4gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MTAwLCBibGFuaz1UcnVlKQogICAgZGV0YWxsZV9qc29uID0gbW9kZWxzLkpTT05GaWVsZChkZWZhdWx0PWRpY3QsIGJsYW5rPVRydWUpCgogICAgY2xhc3MgTWV0YToKICAgICAgICBvcmRlcmluZyA9IFsiLWZlY2hhX2FsZXJ0YSIsICItaWQiXQogICAgICAgIHZlcmJvc2VfbmFtZSA9ICJBbGVydGEgZGUgcmllc2dvIgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiQWxlcnRhcyBkZSByaWVzZ28iCgogICAgZGVmIF9fc3RyX18oc2VsZik6CiAgICAgICAgcmV0dXJuIGYie3NlbGYuZW50aWRhZH0g4oCUIHtzZWxmLnRpcG9fYWxlcnRhfSIK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/risk/selectors.py
PATH_JSON="apps/risk/selectors.py"
FILENAME=selectors.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=37
SIZE_BYTES_UTF8=1227
CONTENT_SHA256=dfd814f8252eb455f725a15e63dcd02c4636264a8150555188e9d835592bb94b
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
"""Consultas reutilizables para Risk y KPIs del Comando Balón."""

from __future__ import annotations

from django.db.models import Count, Sum

from apps.risk.models import RiskOperationSnapshot


def snapshot_queryset(request):
    qs = RiskOperationSnapshot.objects.select_related(
        "operacion",
        "entidad",
        "operacion__unidad_negocio",
        "operacion__producto",
    ).order_by("-fecha_snapshot", "-due_days", "entidad__nombre")
    cliente = request.GET.get("cliente", "").strip()
    if cliente:
        qs = qs.filter(entidad__nombre__icontains=cliente)
    estado = request.GET.get("estado", "").strip()
    if estado:
        qs = qs.filter(estado_operacion__icontains=estado)
    return qs


def snapshot_summary(queryset):
    clientes = queryset.values("entidad_id").distinct().count()
    con_mora = queryset.filter(due_days__gt=0).count()
    sum_vencido = queryset.aggregate(total=Sum("past_due_balance"))["total"] or 0
    operaciones = queryset.values("operacion_id").distinct().count()
    return {
        "total_snapshots": queryset.count(),
        "clientes": clientes,
        "operaciones": operaciones,
        "con_mora": con_mora,
        "suma_vencido": sum_vencido,
    }

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Consultas reutilizables para Risk y KPIs del Comando Balón."""
00002|
00003|from __future__ import annotations
00004|
00005|from django.db.models import Count, Sum
00006|
00007|from apps.risk.models import RiskOperationSnapshot
00008|
00009|
00010|def snapshot_queryset(request):
00011|    qs = RiskOperationSnapshot.objects.select_related(
00012|        "operacion",
00013|        "entidad",
00014|        "operacion__unidad_negocio",
00015|        "operacion__producto",
00016|    ).order_by("-fecha_snapshot", "-due_days", "entidad__nombre")
00017|    cliente = request.GET.get("cliente", "").strip()
00018|    if cliente:
00019|        qs = qs.filter(entidad__nombre__icontains=cliente)
00020|    estado = request.GET.get("estado", "").strip()
00021|    if estado:
00022|        qs = qs.filter(estado_operacion__icontains=estado)
00023|    return qs
00024|
00025|
00026|def snapshot_summary(queryset):
00027|    clientes = queryset.values("entidad_id").distinct().count()
00028|    con_mora = queryset.filter(due_days__gt=0).count()
00029|    sum_vencido = queryset.aggregate(total=Sum("past_due_balance"))["total"] or 0
00030|    operaciones = queryset.values("operacion_id").distinct().count()
00031|    return {
00032|        "total_snapshots": queryset.count(),
00033|        "clientes": clientes,
00034|        "operaciones": operaciones,
00035|        "con_mora": con_mora,
00036|        "suma_vencido": sum_vencido,
00037|    }

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiQ29uc3VsdGFzIHJldXRpbGl6YWJsZXMgcGFyYSBSaXNrIHkgS1BJcyBkZWwgQ29tYW5kbyBCYWzDs24uIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgpmcm9tIGRqYW5nby5kYi5tb2RlbHMgaW1wb3J0IENvdW50LCBTdW0KCmZyb20gYXBwcy5yaXNrLm1vZGVscyBpbXBvcnQgUmlza09wZXJhdGlvblNuYXBzaG90CgoKZGVmIHNuYXBzaG90X3F1ZXJ5c2V0KHJlcXVlc3QpOgogICAgcXMgPSBSaXNrT3BlcmF0aW9uU25hcHNob3Qub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgKICAgICAgICAib3BlcmFjaW9uIiwKICAgICAgICAiZW50aWRhZCIsCiAgICAgICAgIm9wZXJhY2lvbl9fdW5pZGFkX25lZ29jaW8iLAogICAgICAgICJvcGVyYWNpb25fX3Byb2R1Y3RvIiwKICAgICkub3JkZXJfYnkoIi1mZWNoYV9zbmFwc2hvdCIsICItZHVlX2RheXMiLCAiZW50aWRhZF9fbm9tYnJlIikKICAgIGNsaWVudGUgPSByZXF1ZXN0LkdFVC5nZXQoImNsaWVudGUiLCAiIikuc3RyaXAoKQogICAgaWYgY2xpZW50ZToKICAgICAgICBxcyA9IHFzLmZpbHRlcihlbnRpZGFkX19ub21icmVfX2ljb250YWlucz1jbGllbnRlKQogICAgZXN0YWRvID0gcmVxdWVzdC5HRVQuZ2V0KCJlc3RhZG8iLCAiIikuc3RyaXAoKQogICAgaWYgZXN0YWRvOgogICAgICAgIHFzID0gcXMuZmlsdGVyKGVzdGFkb19vcGVyYWNpb25fX2ljb250YWlucz1lc3RhZG8pCiAgICByZXR1cm4gcXMKCgpkZWYgc25hcHNob3Rfc3VtbWFyeShxdWVyeXNldCk6CiAgICBjbGllbnRlcyA9IHF1ZXJ5c2V0LnZhbHVlcygiZW50aWRhZF9pZCIpLmRpc3RpbmN0KCkuY291bnQoKQogICAgY29uX21vcmEgPSBxdWVyeXNldC5maWx0ZXIoZHVlX2RheXNfX2d0PTApLmNvdW50KCkKICAgIHN1bV92ZW5jaWRvID0gcXVlcnlzZXQuYWdncmVnYXRlKHRvdGFsPVN1bSgicGFzdF9kdWVfYmFsYW5jZSIpKVsidG90YWwiXSBvciAwCiAgICBvcGVyYWNpb25lcyA9IHF1ZXJ5c2V0LnZhbHVlcygib3BlcmFjaW9uX2lkIikuZGlzdGluY3QoKS5jb3VudCgpCiAgICByZXR1cm4gewogICAgICAgICJ0b3RhbF9zbmFwc2hvdHMiOiBxdWVyeXNldC5jb3VudCgpLAogICAgICAgICJjbGllbnRlcyI6IGNsaWVudGVzLAogICAgICAgICJvcGVyYWNpb25lcyI6IG9wZXJhY2lvbmVzLAogICAgICAgICJjb25fbW9yYSI6IGNvbl9tb3JhLAogICAgICAgICJzdW1hX3ZlbmNpZG8iOiBzdW1fdmVuY2lkbywKICAgIH0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/risk/urls.py
PATH_JSON="apps/risk/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=15
SIZE_BYTES_UTF8=685
CONTENT_SHA256=99425121932aa1240207d91ce230df8fd4f88fedec863b2e76989e576d551cec
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

app_name = "wcgone_risk"

urlpatterns = [
    path("comando-balon/", views.comando_balon, name="comando_balon"),
    path("comando-balon/exportar/", views.export_comando_balon_csv, name="export_comando_balon"),
    path("clientes/", views.ClienteListView.as_view(), name="cliente_list"),
    path("clientes/<int:pk>/", views.ClienteDetailView.as_view(), name="cliente_detail"),
    path("operaciones/<int:pk>/", views.OperacionDetailView.as_view(), name="operacion_detail"),
    path("importar-snapshots/", views.importar_snapshots, name="importar_snapshots"),
    path("importar-eeff/", views.importar_eeff, name="importar_eeff"),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.urls import path
00002|
00003|from . import views
00004|
00005|app_name = "wcgone_risk"
00006|
00007|urlpatterns = [
00008|    path("comando-balon/", views.comando_balon, name="comando_balon"),
00009|    path("comando-balon/exportar/", views.export_comando_balon_csv, name="export_comando_balon"),
00010|    path("clientes/", views.ClienteListView.as_view(), name="cliente_list"),
00011|    path("clientes/<int:pk>/", views.ClienteDetailView.as_view(), name="cliente_detail"),
00012|    path("operaciones/<int:pk>/", views.OperacionDetailView.as_view(), name="operacion_detail"),
00013|    path("importar-snapshots/", views.importar_snapshots, name="importar_snapshots"),
00014|    path("importar-eeff/", views.importar_eeff, name="importar_eeff"),
00015|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aAoKZnJvbSAuIGltcG9ydCB2aWV3cwoKYXBwX25hbWUgPSAid2Nnb25lX3Jpc2siCgp1cmxwYXR0ZXJucyA9IFsKICAgIHBhdGgoImNvbWFuZG8tYmFsb24vIiwgdmlld3MuY29tYW5kb19iYWxvbiwgbmFtZT0iY29tYW5kb19iYWxvbiIpLAogICAgcGF0aCgiY29tYW5kby1iYWxvbi9leHBvcnRhci8iLCB2aWV3cy5leHBvcnRfY29tYW5kb19iYWxvbl9jc3YsIG5hbWU9ImV4cG9ydF9jb21hbmRvX2JhbG9uIiksCiAgICBwYXRoKCJjbGllbnRlcy8iLCB2aWV3cy5DbGllbnRlTGlzdFZpZXcuYXNfdmlldygpLCBuYW1lPSJjbGllbnRlX2xpc3QiKSwKICAgIHBhdGgoImNsaWVudGVzLzxpbnQ6cGs+LyIsIHZpZXdzLkNsaWVudGVEZXRhaWxWaWV3LmFzX3ZpZXcoKSwgbmFtZT0iY2xpZW50ZV9kZXRhaWwiKSwKICAgIHBhdGgoIm9wZXJhY2lvbmVzLzxpbnQ6cGs+LyIsIHZpZXdzLk9wZXJhY2lvbkRldGFpbFZpZXcuYXNfdmlldygpLCBuYW1lPSJvcGVyYWNpb25fZGV0YWlsIiksCiAgICBwYXRoKCJpbXBvcnRhci1zbmFwc2hvdHMvIiwgdmlld3MuaW1wb3J0YXJfc25hcHNob3RzLCBuYW1lPSJpbXBvcnRhcl9zbmFwc2hvdHMiKSwKICAgIHBhdGgoImltcG9ydGFyLWVlZmYvIiwgdmlld3MuaW1wb3J0YXJfZWVmZiwgbmFtZT0iaW1wb3J0YXJfZWVmZiIpLApdCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=apps/risk/views.py
PATH_JSON="apps/risk/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=156
SIZE_BYTES_UTF8=5233
CONTENT_SHA256=1120b07061662fe453d84d5c5fd60d15d0c7f29218156bedf4bb16fdfeb69cff
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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max, Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView

from apps.core.exports import csv_response
from apps.core.models import Entidad

from .models import RiskOperacion, RiskOperationSnapshot
from .selectors import snapshot_queryset, snapshot_summary


@login_required
def comando_balon(request):
    qs = snapshot_queryset(request)
    context = {
        "snapshots": qs[:100],
        "summary": snapshot_summary(qs),
        "export_query": request.GET.urlencode(),
        "breadcrumbs": [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "Riesgo — Comando Balón"},
        ],
    }
    return render(request, "wcgone/risk/comando_balon.html", context)


@login_required
def export_comando_balon_csv(request):
    qs = snapshot_queryset(request)
    rows = []
    for snap in qs:
        rows.append([
            snap.fecha_snapshot.isoformat() if snap.fecha_snapshot else "",
            snap.entidad.nombre,
            snap.entidad.nit or "",
            snap.operacion.codigo_operacion,
            snap.producto_nombre_raw or "",
            snap.estado_operacion or "",
            snap.capital_balance or "",
            snap.past_due_balance or "",
            snap.due_days if snap.due_days is not None else "",
        ])
    filename = f"risk_comando_balon_{timezone.localdate().isoformat()}.csv"
    return csv_response(
        filename,
        [
            "Fecha snapshot",
            "Cliente",
            "NIT",
            "Operación",
            "Producto",
            "Estado",
            "Saldo capital",
            "Saldo vencido",
            "Días atraso",
        ],
        rows,
    )


class ClienteListView(LoginRequiredMixin, ListView):
    model = Entidad
    template_name = "wcgone/risk/cliente_list.html"
    context_object_name = "clientes"
    paginate_by = 25

    def get_queryset(self):
        qs = (
            Entidad.objects.filter(operaciones_riesgo__isnull=False)
            .annotate(
                num_operaciones=Count("operaciones_riesgo", distinct=True),
                ultimo_snapshot=Max("risk_snapshots__fecha_snapshot"),
            )
            .distinct()
            .order_by("nombre")
        )
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(nit__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "Balón de Riesgo"},
            {"label": "Clientes"},
        ]
        return context


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Entidad
    template_name = "wcgone/risk/cliente_detail.html"
    context_object_name = "cliente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.object
        context["operaciones"] = cliente.operaciones_riesgo.select_related(
            "producto", "unidad_negocio"
        ).order_by("codigo_operacion")
        context["snapshots_recientes"] = (
            cliente.risk_snapshots.select_related("operacion")
            .order_by("-fecha_snapshot")[:10]
        )
        context["alertas"] = cliente.alertas_riesgo.filter(activa=True).order_by(
            "-fecha_alerta"
        )[:10]
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "Balón de Riesgo"},
            {"label": "Clientes", "url": "/wcgone/risk/clientes/"},
            {"label": cliente.nombre},
        ]
        return context


class OperacionDetailView(LoginRequiredMixin, DetailView):
    model = RiskOperacion
    template_name = "wcgone/risk/operacion_detail.html"
    context_object_name = "operacion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        operacion = self.object
        context["snapshots"] = operacion.snapshots.order_by("-fecha_snapshot")
        context["pagos_programados"] = operacion.pagos_programados.order_by("fecha_programada")
        context["pagos_realizados"] = operacion.pagos_realizados.order_by("-fecha_pago")
        context["breadcrumbs"] = [
            {"label": "Panel principal", "url": "/panel/"},
            {"label": "Balón de Riesgo"},
            {"label": "Clientes", "url": "/wcgone/risk/clientes/"},
            {
                "label": operacion.entidad.nombre,
                "url": f"/wcgone/risk/clientes/{operacion.entidad_id}/",
            },
            {"label": operacion.codigo_operacion},
        ]
        return context


from django.contrib import messages  # noqa: E402
from django.shortcuts import redirect, render  # noqa: E402

@login_required
def importar_snapshots(request):
    return redirect("imports:import_hub")


@login_required
def importar_eeff(request):
    return redirect("imports:import_hub")

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib.auth.decorators import login_required
00002|from django.contrib.auth.mixins import LoginRequiredMixin
00003|from django.db.models import Count, Max, Q
00004|from django.shortcuts import redirect, render
00005|from django.utils import timezone
00006|from django.views.generic import DetailView, ListView
00007|
00008|from apps.core.exports import csv_response
00009|from apps.core.models import Entidad
00010|
00011|from .models import RiskOperacion, RiskOperationSnapshot
00012|from .selectors import snapshot_queryset, snapshot_summary
00013|
00014|
00015|@login_required
00016|def comando_balon(request):
00017|    qs = snapshot_queryset(request)
00018|    context = {
00019|        "snapshots": qs[:100],
00020|        "summary": snapshot_summary(qs),
00021|        "export_query": request.GET.urlencode(),
00022|        "breadcrumbs": [
00023|            {"label": "Panel principal", "url": "/panel/"},
00024|            {"label": "Riesgo — Comando Balón"},
00025|        ],
00026|    }
00027|    return render(request, "wcgone/risk/comando_balon.html", context)
00028|
00029|
00030|@login_required
00031|def export_comando_balon_csv(request):
00032|    qs = snapshot_queryset(request)
00033|    rows = []
00034|    for snap in qs:
00035|        rows.append([
00036|            snap.fecha_snapshot.isoformat() if snap.fecha_snapshot else "",
00037|            snap.entidad.nombre,
00038|            snap.entidad.nit or "",
00039|            snap.operacion.codigo_operacion,
00040|            snap.producto_nombre_raw or "",
00041|            snap.estado_operacion or "",
00042|            snap.capital_balance or "",
00043|            snap.past_due_balance or "",
00044|            snap.due_days if snap.due_days is not None else "",
00045|        ])
00046|    filename = f"risk_comando_balon_{timezone.localdate().isoformat()}.csv"
00047|    return csv_response(
00048|        filename,
00049|        [
00050|            "Fecha snapshot",
00051|            "Cliente",
00052|            "NIT",
00053|            "Operación",
00054|            "Producto",
00055|            "Estado",
00056|            "Saldo capital",
00057|            "Saldo vencido",
00058|            "Días atraso",
00059|        ],
00060|        rows,
00061|    )
00062|
00063|
00064|class ClienteListView(LoginRequiredMixin, ListView):
00065|    model = Entidad
00066|    template_name = "wcgone/risk/cliente_list.html"
00067|    context_object_name = "clientes"
00068|    paginate_by = 25
00069|
00070|    def get_queryset(self):
00071|        qs = (
00072|            Entidad.objects.filter(operaciones_riesgo__isnull=False)
00073|            .annotate(
00074|                num_operaciones=Count("operaciones_riesgo", distinct=True),
00075|                ultimo_snapshot=Max("risk_snapshots__fecha_snapshot"),
00076|            )
00077|            .distinct()
00078|            .order_by("nombre")
00079|        )
00080|        q = self.request.GET.get("q", "").strip()
00081|        if q:
00082|            qs = qs.filter(Q(nombre__icontains=q) | Q(nit__icontains=q))
00083|        return qs
00084|
00085|    def get_context_data(self, **kwargs):
00086|        context = super().get_context_data(**kwargs)
00087|        context["breadcrumbs"] = [
00088|            {"label": "Panel principal", "url": "/panel/"},
00089|            {"label": "Balón de Riesgo"},
00090|            {"label": "Clientes"},
00091|        ]
00092|        return context
00093|
00094|
00095|class ClienteDetailView(LoginRequiredMixin, DetailView):
00096|    model = Entidad
00097|    template_name = "wcgone/risk/cliente_detail.html"
00098|    context_object_name = "cliente"
00099|
00100|    def get_context_data(self, **kwargs):
00101|        context = super().get_context_data(**kwargs)
00102|        cliente = self.object
00103|        context["operaciones"] = cliente.operaciones_riesgo.select_related(
00104|            "producto", "unidad_negocio"
00105|        ).order_by("codigo_operacion")
00106|        context["snapshots_recientes"] = (
00107|            cliente.risk_snapshots.select_related("operacion")
00108|            .order_by("-fecha_snapshot")[:10]
00109|        )
00110|        context["alertas"] = cliente.alertas_riesgo.filter(activa=True).order_by(
00111|            "-fecha_alerta"
00112|        )[:10]
00113|        context["breadcrumbs"] = [
00114|            {"label": "Panel principal", "url": "/panel/"},
00115|            {"label": "Balón de Riesgo"},
00116|            {"label": "Clientes", "url": "/wcgone/risk/clientes/"},
00117|            {"label": cliente.nombre},
00118|        ]
00119|        return context
00120|
00121|
00122|class OperacionDetailView(LoginRequiredMixin, DetailView):
00123|    model = RiskOperacion
00124|    template_name = "wcgone/risk/operacion_detail.html"
00125|    context_object_name = "operacion"
00126|
00127|    def get_context_data(self, **kwargs):
00128|        context = super().get_context_data(**kwargs)
00129|        operacion = self.object
00130|        context["snapshots"] = operacion.snapshots.order_by("-fecha_snapshot")
00131|        context["pagos_programados"] = operacion.pagos_programados.order_by("fecha_programada")
00132|        context["pagos_realizados"] = operacion.pagos_realizados.order_by("-fecha_pago")
00133|        context["breadcrumbs"] = [
00134|            {"label": "Panel principal", "url": "/panel/"},
00135|            {"label": "Balón de Riesgo"},
00136|            {"label": "Clientes", "url": "/wcgone/risk/clientes/"},
00137|            {
00138|                "label": operacion.entidad.nombre,
00139|                "url": f"/wcgone/risk/clientes/{operacion.entidad_id}/",
00140|            },
00141|            {"label": operacion.codigo_operacion},
00142|        ]
00143|        return context
00144|
00145|
00146|from django.contrib import messages  # noqa: E402
00147|from django.shortcuts import redirect, render  # noqa: E402
00148|
00149|@login_required
00150|def importar_snapshots(request):
00151|    return redirect("imports:import_hub")
00152|
00153|
00154|@login_required
00155|def importar_eeff(request):
00156|    return redirect("imports:import_hub")

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYi5hdXRoLmRlY29yYXRvcnMgaW1wb3J0IGxvZ2luX3JlcXVpcmVkCmZyb20gZGphbmdvLmNvbnRyaWIuYXV0aC5taXhpbnMgaW1wb3J0IExvZ2luUmVxdWlyZWRNaXhpbgpmcm9tIGRqYW5nby5kYi5tb2RlbHMgaW1wb3J0IENvdW50LCBNYXgsIFEKZnJvbSBkamFuZ28uc2hvcnRjdXRzIGltcG9ydCByZWRpcmVjdCwgcmVuZGVyCmZyb20gZGphbmdvLnV0aWxzIGltcG9ydCB0aW1lem9uZQpmcm9tIGRqYW5nby52aWV3cy5nZW5lcmljIGltcG9ydCBEZXRhaWxWaWV3LCBMaXN0VmlldwoKZnJvbSBhcHBzLmNvcmUuZXhwb3J0cyBpbXBvcnQgY3N2X3Jlc3BvbnNlCmZyb20gYXBwcy5jb3JlLm1vZGVscyBpbXBvcnQgRW50aWRhZAoKZnJvbSAubW9kZWxzIGltcG9ydCBSaXNrT3BlcmFjaW9uLCBSaXNrT3BlcmF0aW9uU25hcHNob3QKZnJvbSAuc2VsZWN0b3JzIGltcG9ydCBzbmFwc2hvdF9xdWVyeXNldCwgc25hcHNob3Rfc3VtbWFyeQoKCkBsb2dpbl9yZXF1aXJlZApkZWYgY29tYW5kb19iYWxvbihyZXF1ZXN0KToKICAgIHFzID0gc25hcHNob3RfcXVlcnlzZXQocmVxdWVzdCkKICAgIGNvbnRleHQgPSB7CiAgICAgICAgInNuYXBzaG90cyI6IHFzWzoxMDBdLAogICAgICAgICJzdW1tYXJ5Ijogc25hcHNob3Rfc3VtbWFyeShxcyksCiAgICAgICAgImV4cG9ydF9xdWVyeSI6IHJlcXVlc3QuR0VULnVybGVuY29kZSgpLAogICAgICAgICJicmVhZGNydW1icyI6IFsKICAgICAgICAgICAgeyJsYWJlbCI6ICJQYW5lbCBwcmluY2lwYWwiLCAidXJsIjogIi9wYW5lbC8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJSaWVzZ28g4oCUIENvbWFuZG8gQmFsw7NuIn0sCiAgICAgICAgXSwKICAgIH0KICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgIndjZ29uZS9yaXNrL2NvbWFuZG9fYmFsb24uaHRtbCIsIGNvbnRleHQpCgoKQGxvZ2luX3JlcXVpcmVkCmRlZiBleHBvcnRfY29tYW5kb19iYWxvbl9jc3YocmVxdWVzdCk6CiAgICBxcyA9IHNuYXBzaG90X3F1ZXJ5c2V0KHJlcXVlc3QpCiAgICByb3dzID0gW10KICAgIGZvciBzbmFwIGluIHFzOgogICAgICAgIHJvd3MuYXBwZW5kKFsKICAgICAgICAgICAgc25hcC5mZWNoYV9zbmFwc2hvdC5pc29mb3JtYXQoKSBpZiBzbmFwLmZlY2hhX3NuYXBzaG90IGVsc2UgIiIsCiAgICAgICAgICAgIHNuYXAuZW50aWRhZC5ub21icmUsCiAgICAgICAgICAgIHNuYXAuZW50aWRhZC5uaXQgb3IgIiIsCiAgICAgICAgICAgIHNuYXAub3BlcmFjaW9uLmNvZGlnb19vcGVyYWNpb24sCiAgICAgICAgICAgIHNuYXAucHJvZHVjdG9fbm9tYnJlX3JhdyBvciAiIiwKICAgICAgICAgICAgc25hcC5lc3RhZG9fb3BlcmFjaW9uIG9yICIiLAogICAgICAgICAgICBzbmFwLmNhcGl0YWxfYmFsYW5jZSBvciAiIiwKICAgICAgICAgICAgc25hcC5wYXN0X2R1ZV9iYWxhbmNlIG9yICIiLAogICAgICAgICAgICBzbmFwLmR1ZV9kYXlzIGlmIHNuYXAuZHVlX2RheXMgaXMgbm90IE5vbmUgZWxzZSAiIiwKICAgICAgICBdKQogICAgZmlsZW5hbWUgPSBmInJpc2tfY29tYW5kb19iYWxvbl97dGltZXpvbmUubG9jYWxkYXRlKCkuaXNvZm9ybWF0KCl9LmNzdiIKICAgIHJldHVybiBjc3ZfcmVzcG9uc2UoCiAgICAgICAgZmlsZW5hbWUsCiAgICAgICAgWwogICAgICAgICAgICAiRmVjaGEgc25hcHNob3QiLAogICAgICAgICAgICAiQ2xpZW50ZSIsCiAgICAgICAgICAgICJOSVQiLAogICAgICAgICAgICAiT3BlcmFjacOzbiIsCiAgICAgICAgICAgICJQcm9kdWN0byIsCiAgICAgICAgICAgICJFc3RhZG8iLAogICAgICAgICAgICAiU2FsZG8gY2FwaXRhbCIsCiAgICAgICAgICAgICJTYWxkbyB2ZW5jaWRvIiwKICAgICAgICAgICAgIkTDrWFzIGF0cmFzbyIsCiAgICAgICAgXSwKICAgICAgICByb3dzLAogICAgKQoKCmNsYXNzIENsaWVudGVMaXN0VmlldyhMb2dpblJlcXVpcmVkTWl4aW4sIExpc3RWaWV3KToKICAgIG1vZGVsID0gRW50aWRhZAogICAgdGVtcGxhdGVfbmFtZSA9ICJ3Y2dvbmUvcmlzay9jbGllbnRlX2xpc3QuaHRtbCIKICAgIGNvbnRleHRfb2JqZWN0X25hbWUgPSAiY2xpZW50ZXMiCiAgICBwYWdpbmF0ZV9ieSA9IDI1CgogICAgZGVmIGdldF9xdWVyeXNldChzZWxmKToKICAgICAgICBxcyA9ICgKICAgICAgICAgICAgRW50aWRhZC5vYmplY3RzLmZpbHRlcihvcGVyYWNpb25lc19yaWVzZ29fX2lzbnVsbD1GYWxzZSkKICAgICAgICAgICAgLmFubm90YXRlKAogICAgICAgICAgICAgICAgbnVtX29wZXJhY2lvbmVzPUNvdW50KCJvcGVyYWNpb25lc19yaWVzZ28iLCBkaXN0aW5jdD1UcnVlKSwKICAgICAgICAgICAgICAgIHVsdGltb19zbmFwc2hvdD1NYXgoInJpc2tfc25hcHNob3RzX19mZWNoYV9zbmFwc2hvdCIpLAogICAgICAgICAgICApCiAgICAgICAgICAgIC5kaXN0aW5jdCgpCiAgICAgICAgICAgIC5vcmRlcl9ieSgibm9tYnJlIikKICAgICAgICApCiAgICAgICAgcSA9IHNlbGYucmVxdWVzdC5HRVQuZ2V0KCJxIiwgIiIpLnN0cmlwKCkKICAgICAgICBpZiBxOgogICAgICAgICAgICBxcyA9IHFzLmZpbHRlcihRKG5vbWJyZV9faWNvbnRhaW5zPXEpIHwgUShuaXRfX2ljb250YWlucz1xKSkKICAgICAgICByZXR1cm4gcXMKCiAgICBkZWYgZ2V0X2NvbnRleHRfZGF0YShzZWxmLCAqKmt3YXJncyk6CiAgICAgICAgY29udGV4dCA9IHN1cGVyKCkuZ2V0X2NvbnRleHRfZGF0YSgqKmt3YXJncykKICAgICAgICBjb250ZXh0WyJicmVhZGNydW1icyJdID0gWwogICAgICAgICAgICB7ImxhYmVsIjogIlBhbmVsIHByaW5jaXBhbCIsICJ1cmwiOiAiL3BhbmVsLyJ9LAogICAgICAgICAgICB7ImxhYmVsIjogIkJhbMOzbiBkZSBSaWVzZ28ifSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJDbGllbnRlcyJ9LAogICAgICAgIF0KICAgICAgICByZXR1cm4gY29udGV4dAoKCmNsYXNzIENsaWVudGVEZXRhaWxWaWV3KExvZ2luUmVxdWlyZWRNaXhpbiwgRGV0YWlsVmlldyk6CiAgICBtb2RlbCA9IEVudGlkYWQKICAgIHRlbXBsYXRlX25hbWUgPSAid2Nnb25lL3Jpc2svY2xpZW50ZV9kZXRhaWwuaHRtbCIKICAgIGNvbnRleHRfb2JqZWN0X25hbWUgPSAiY2xpZW50ZSIKCiAgICBkZWYgZ2V0X2NvbnRleHRfZGF0YShzZWxmLCAqKmt3YXJncyk6CiAgICAgICAgY29udGV4dCA9IHN1cGVyKCkuZ2V0X2NvbnRleHRfZGF0YSgqKmt3YXJncykKICAgICAgICBjbGllbnRlID0gc2VsZi5vYmplY3QKICAgICAgICBjb250ZXh0WyJvcGVyYWNpb25lcyJdID0gY2xpZW50ZS5vcGVyYWNpb25lc19yaWVzZ28uc2VsZWN0X3JlbGF0ZWQoCiAgICAgICAgICAgICJwcm9kdWN0byIsICJ1bmlkYWRfbmVnb2NpbyIKICAgICAgICApLm9yZGVyX2J5KCJjb2RpZ29fb3BlcmFjaW9uIikKICAgICAgICBjb250ZXh0WyJzbmFwc2hvdHNfcmVjaWVudGVzIl0gPSAoCiAgICAgICAgICAgIGNsaWVudGUucmlza19zbmFwc2hvdHMuc2VsZWN0X3JlbGF0ZWQoIm9wZXJhY2lvbiIpCiAgICAgICAgICAgIC5vcmRlcl9ieSgiLWZlY2hhX3NuYXBzaG90IilbOjEwXQogICAgICAgICkKICAgICAgICBjb250ZXh0WyJhbGVydGFzIl0gPSBjbGllbnRlLmFsZXJ0YXNfcmllc2dvLmZpbHRlcihhY3RpdmE9VHJ1ZSkub3JkZXJfYnkoCiAgICAgICAgICAgICItZmVjaGFfYWxlcnRhIgogICAgICAgIClbOjEwXQogICAgICAgIGNvbnRleHRbImJyZWFkY3J1bWJzIl0gPSBbCiAgICAgICAgICAgIHsibGFiZWwiOiAiUGFuZWwgcHJpbmNpcGFsIiwgInVybCI6ICIvcGFuZWwvIn0sCiAgICAgICAgICAgIHsibGFiZWwiOiAiQmFsw7NuIGRlIFJpZXNnbyJ9LAogICAgICAgICAgICB7ImxhYmVsIjogIkNsaWVudGVzIiwgInVybCI6ICIvd2Nnb25lL3Jpc2svY2xpZW50ZXMvIn0sCiAgICAgICAgICAgIHsibGFiZWwiOiBjbGllbnRlLm5vbWJyZX0sCiAgICAgICAgXQogICAgICAgIHJldHVybiBjb250ZXh0CgoKY2xhc3MgT3BlcmFjaW9uRGV0YWlsVmlldyhMb2dpblJlcXVpcmVkTWl4aW4sIERldGFpbFZpZXcpOgogICAgbW9kZWwgPSBSaXNrT3BlcmFjaW9uCiAgICB0ZW1wbGF0ZV9uYW1lID0gIndjZ29uZS9yaXNrL29wZXJhY2lvbl9kZXRhaWwuaHRtbCIKICAgIGNvbnRleHRfb2JqZWN0X25hbWUgPSAib3BlcmFjaW9uIgoKICAgIGRlZiBnZXRfY29udGV4dF9kYXRhKHNlbGYsICoqa3dhcmdzKToKICAgICAgICBjb250ZXh0ID0gc3VwZXIoKS5nZXRfY29udGV4dF9kYXRhKCoqa3dhcmdzKQogICAgICAgIG9wZXJhY2lvbiA9IHNlbGYub2JqZWN0CiAgICAgICAgY29udGV4dFsic25hcHNob3RzIl0gPSBvcGVyYWNpb24uc25hcHNob3RzLm9yZGVyX2J5KCItZmVjaGFfc25hcHNob3QiKQogICAgICAgIGNvbnRleHRbInBhZ29zX3Byb2dyYW1hZG9zIl0gPSBvcGVyYWNpb24ucGFnb3NfcHJvZ3JhbWFkb3Mub3JkZXJfYnkoImZlY2hhX3Byb2dyYW1hZGEiKQogICAgICAgIGNvbnRleHRbInBhZ29zX3JlYWxpemFkb3MiXSA9IG9wZXJhY2lvbi5wYWdvc19yZWFsaXphZG9zLm9yZGVyX2J5KCItZmVjaGFfcGFnbyIpCiAgICAgICAgY29udGV4dFsiYnJlYWRjcnVtYnMiXSA9IFsKICAgICAgICAgICAgeyJsYWJlbCI6ICJQYW5lbCBwcmluY2lwYWwiLCAidXJsIjogIi9wYW5lbC8ifSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJCYWzDs24gZGUgUmllc2dvIn0sCiAgICAgICAgICAgIHsibGFiZWwiOiAiQ2xpZW50ZXMiLCAidXJsIjogIi93Y2dvbmUvcmlzay9jbGllbnRlcy8ifSwKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgImxhYmVsIjogb3BlcmFjaW9uLmVudGlkYWQubm9tYnJlLAogICAgICAgICAgICAgICAgInVybCI6IGYiL3djZ29uZS9yaXNrL2NsaWVudGVzL3tvcGVyYWNpb24uZW50aWRhZF9pZH0vIiwKICAgICAgICAgICAgfSwKICAgICAgICAgICAgeyJsYWJlbCI6IG9wZXJhY2lvbi5jb2RpZ29fb3BlcmFjaW9ufSwKICAgICAgICBdCiAgICAgICAgcmV0dXJuIGNvbnRleHQKCgpmcm9tIGRqYW5nby5jb250cmliIGltcG9ydCBtZXNzYWdlcyAgIyBub3FhOiBFNDAyCmZyb20gZGphbmdvLnNob3J0Y3V0cyBpbXBvcnQgcmVkaXJlY3QsIHJlbmRlciAgIyBub3FhOiBFNDAyCgpAbG9naW5fcmVxdWlyZWQKZGVmIGltcG9ydGFyX3NuYXBzaG90cyhyZXF1ZXN0KToKICAgIHJldHVybiByZWRpcmVjdCgiaW1wb3J0czppbXBvcnRfaHViIikKCgpAbG9naW5fcmVxdWlyZWQKZGVmIGltcG9ydGFyX2VlZmYocmVxdWVzdCk6CiAgICByZXR1cm4gcmVkaXJlY3QoImltcG9ydHM6aW1wb3J0X2h1YiIpCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=config/__init__.py
PATH_JSON="config/__init__.py"
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
PATH_LITERAL=config/asgi.py
PATH_JSON="config/asgi.py"
FILENAME=asgi.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=16
SIZE_BYTES_UTF8=389
CONTENT_SHA256=0aae3f4019c7d4d758529344d24b9fc627debc4f5f0fe263c556415d698edc38
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
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|ASGI config for config project.
00003|
00004|It exposes the ASGI callable as a module-level variable named ``application``.
00005|
00006|For more information on this file, see
00007|https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
00008|"""
00009|
00010|import os
00011|
00012|from django.core.asgi import get_asgi_application
00013|
00014|os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
00015|
00016|application = get_asgi_application()

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiCkFTR0kgY29uZmlnIGZvciBjb25maWcgcHJvamVjdC4KCkl0IGV4cG9zZXMgdGhlIEFTR0kgY2FsbGFibGUgYXMgYSBtb2R1bGUtbGV2ZWwgdmFyaWFibGUgbmFtZWQgYGBhcHBsaWNhdGlvbmBgLgoKRm9yIG1vcmUgaW5mb3JtYXRpb24gb24gdGhpcyBmaWxlLCBzZWUKaHR0cHM6Ly9kb2NzLmRqYW5nb3Byb2plY3QuY29tL2VuLzUuMC9ob3d0by9kZXBsb3ltZW50L2FzZ2kvCiIiIgoKaW1wb3J0IG9zCgpmcm9tIGRqYW5nby5jb3JlLmFzZ2kgaW1wb3J0IGdldF9hc2dpX2FwcGxpY2F0aW9uCgpvcy5lbnZpcm9uLnNldGRlZmF1bHQoIkRKQU5HT19TRVRUSU5HU19NT0RVTEUiLCAiY29uZmlnLnNldHRpbmdzIikKCmFwcGxpY2F0aW9uID0gZ2V0X2FzZ2lfYXBwbGljYXRpb24oKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=config/formats/__init__.py
PATH_JSON="config/formats/__init__.py"
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
PATH_LITERAL=config/formats/es/__init__.py
PATH_JSON="config/formats/es/__init__.py"
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
PATH_LITERAL=config/formats/es/formats.py
PATH_JSON="config/formats/es/formats.py"
FILENAME=formats.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=5
SIZE_BYTES_UTF8=98
CONTENT_SHA256=99baf6481b86c5127f62a337f4046420617d7b28d0d9c95f6938f3928669becb
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
DECIMAL_SEPARATOR = "."
THOUSAND_SEPARATOR = ","
NUMBER_GROUPING = 3
USE_THOUSAND_SEPARATOR = True
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|DECIMAL_SEPARATOR = "."
00002|THOUSAND_SEPARATOR = ","
00003|NUMBER_GROUPING = 3
00004|USE_THOUSAND_SEPARATOR = True
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
REVDSU1BTF9TRVBBUkFUT1IgPSAiLiIKVEhPVVNBTkRfU0VQQVJBVE9SID0gIiwiCk5VTUJFUl9HUk9VUElORyA9IDMKVVNFX1RIT1VTQU5EX1NFUEFSQVRPUiA9IFRydWU=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=config/settings.py
PATH_JSON="config/settings.py"
FILENAME=settings.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=179
SIZE_BYTES_UTF8=4646
CONTENT_SHA256=046fa4356bb60f3fe7aea450bd0e58c8ead887471aa211581a9475a65f1e9890
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
# File: config/settings.py

from pathlib import Path
import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Si DEBUG no está en el entorno:
# - Local (sin Railway) → True
# - Railway / con RAILWAY_* → False (producción segura por defecto)
_raw_debug = os.environ.get("DEBUG")
if _raw_debug is None:
    _on_railway = bool(
        os.environ.get("RAILWAY_ENVIRONMENT")
        or os.environ.get("RAILWAY_PROJECT_ID")
        or os.environ.get("RAILWAY_STATIC_URL")
    )
    DEBUG = not _on_railway
else:
    DEBUG = _raw_debug.lower() == "true"

_secret = os.environ.get("SECRET_KEY")
if _secret:
    SECRET_KEY = _secret
elif DEBUG:
    SECRET_KEY = "unsafe-dev-key"
else:
    raise ImproperlyConfigured(
        "SECRET_KEY must be set via environment when DEBUG is False."
    )

FORMAT_MODULE_PATH = ["config.formats"]

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS",
        "127.0.0.1,localhost"
    ).split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CSRF_TRUSTED_ORIGINS",
        "http://127.0.0.1,http://localhost"
    ).split(",")
    if origin.strip()
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # PGC1 / operativo
    'core',
    'accounts.apps.AccountsConfig',
    'imports',
    'pgc',
    'feedback',
    'portal',
    'crm',
    'risk',
    'pgo',
    'reports',

    # WCG One (coexistencia de modelos / módulos)
    'apps.portal.apps.PortalConfig',
    'apps.core.apps.CoreConfig',
    'apps.crm.apps.CrmConfig',
    'apps.risk.apps.RiskConfig',
    'apps.pgo.apps.PgoConfig',
    'apps.pgc.apps.PgcConfig',
    'apps.legacy_pgc1.apps.LegacyPgc1Config',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-gt'
TIME_ZONE = 'America/Guatemala'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

UPLOADS_ROOT = BASE_DIR / 'uploads'
OUTPUT_ROOT = BASE_DIR / 'output'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/panel/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|# File: config/settings.py
00002|
00003|from pathlib import Path
00004|import os
00005|import dj_database_url
00006|from django.core.exceptions import ImproperlyConfigured
00007|
00008|BASE_DIR = Path(__file__).resolve().parent.parent
00009|
00010|# Si DEBUG no está en el entorno:
00011|# - Local (sin Railway) → True
00012|# - Railway / con RAILWAY_* → False (producción segura por defecto)
00013|_raw_debug = os.environ.get("DEBUG")
00014|if _raw_debug is None:
00015|    _on_railway = bool(
00016|        os.environ.get("RAILWAY_ENVIRONMENT")
00017|        or os.environ.get("RAILWAY_PROJECT_ID")
00018|        or os.environ.get("RAILWAY_STATIC_URL")
00019|    )
00020|    DEBUG = not _on_railway
00021|else:
00022|    DEBUG = _raw_debug.lower() == "true"
00023|
00024|_secret = os.environ.get("SECRET_KEY")
00025|if _secret:
00026|    SECRET_KEY = _secret
00027|elif DEBUG:
00028|    SECRET_KEY = "unsafe-dev-key"
00029|else:
00030|    raise ImproperlyConfigured(
00031|        "SECRET_KEY must be set via environment when DEBUG is False."
00032|    )
00033|
00034|FORMAT_MODULE_PATH = ["config.formats"]
00035|
00036|ALLOWED_HOSTS = [
00037|    host.strip()
00038|    for host in os.environ.get(
00039|        "ALLOWED_HOSTS",
00040|        "127.0.0.1,localhost"
00041|    ).split(",")
00042|    if host.strip()
00043|]
00044|
00045|CSRF_TRUSTED_ORIGINS = [
00046|    origin.strip()
00047|    for origin in os.environ.get(
00048|        "CSRF_TRUSTED_ORIGINS",
00049|        "http://127.0.0.1,http://localhost"
00050|    ).split(",")
00051|    if origin.strip()
00052|]
00053|
00054|SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
00055|
00056|if not DEBUG:
00057|    SESSION_COOKIE_SECURE = True
00058|    CSRF_COOKIE_SECURE = True
00059|    SECURE_SSL_REDIRECT = True
00060|    SECURE_HSTS_SECONDS = 31536000
00061|    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
00062|    SECURE_HSTS_PRELOAD = True
00063|
00064|INSTALLED_APPS = [
00065|    'django.contrib.admin',
00066|    'django.contrib.auth',
00067|    'django.contrib.contenttypes',
00068|    'django.contrib.sessions',
00069|    'django.contrib.messages',
00070|    'django.contrib.staticfiles',
00071|
00072|    # PGC1 / operativo
00073|    'core',
00074|    'accounts.apps.AccountsConfig',
00075|    'imports',
00076|    'pgc',
00077|    'feedback',
00078|    'portal',
00079|    'crm',
00080|    'risk',
00081|    'pgo',
00082|    'reports',
00083|
00084|    # WCG One (coexistencia de modelos / módulos)
00085|    'apps.portal.apps.PortalConfig',
00086|    'apps.core.apps.CoreConfig',
00087|    'apps.crm.apps.CrmConfig',
00088|    'apps.risk.apps.RiskConfig',
00089|    'apps.pgo.apps.PgoConfig',
00090|    'apps.pgc.apps.PgcConfig',
00091|    'apps.legacy_pgc1.apps.LegacyPgc1Config',
00092|]
00093|
00094|MIDDLEWARE = [
00095|    'django.middleware.security.SecurityMiddleware',
00096|    'whitenoise.middleware.WhiteNoiseMiddleware',
00097|    'django.contrib.sessions.middleware.SessionMiddleware',
00098|    'django.middleware.common.CommonMiddleware',
00099|    'django.middleware.csrf.CsrfViewMiddleware',
00100|    'django.contrib.auth.middleware.AuthenticationMiddleware',
00101|    'django.contrib.messages.middleware.MessageMiddleware',
00102|    'django.middleware.clickjacking.XFrameOptionsMiddleware',
00103|]
00104|
00105|ROOT_URLCONF = 'config.urls'
00106|
00107|TEMPLATES = [
00108|    {
00109|        'BACKEND': 'django.template.backends.django.DjangoTemplates',
00110|        'DIRS': [BASE_DIR / 'templates'],
00111|        'APP_DIRS': True,
00112|        'OPTIONS': {
00113|            'context_processors': [
00114|                'django.template.context_processors.debug',
00115|                'django.template.context_processors.request',
00116|                'django.contrib.auth.context_processors.auth',
00117|                'django.contrib.messages.context_processors.messages',
00118|            ],
00119|        },
00120|    },
00121|]
00122|
00123|WSGI_APPLICATION = 'config.wsgi.application'
00124|
00125|DATABASE_URL = os.environ.get('DATABASE_URL')
00126|
00127|if DATABASE_URL:
00128|    DATABASES = {
00129|        'default': dj_database_url.parse(
00130|            DATABASE_URL,
00131|            conn_max_age=600,
00132|            ssl_require=True
00133|        )
00134|    }
00135|else:
00136|    DATABASES = {
00137|        'default': {
00138|            'ENGINE': 'django.db.backends.sqlite3',
00139|            'NAME': BASE_DIR / 'db.sqlite3',
00140|        }
00141|    }
00142|
00143|AUTH_PASSWORD_VALIDATORS = [
00144|    {
00145|        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
00146|    },
00147|    {
00148|        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
00149|    },
00150|    {
00151|        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
00152|    },
00153|    {
00154|        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
00155|    },
00156|]
00157|
00158|LANGUAGE_CODE = 'es-gt'
00159|TIME_ZONE = 'America/Guatemala'
00160|USE_I18N = True
00161|USE_TZ = True
00162|
00163|STATIC_URL = '/static/'
00164|STATIC_ROOT = BASE_DIR / 'staticfiles'
00165|STATICFILES_DIRS = [BASE_DIR / 'static']
00166|STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
00167|
00168|MEDIA_URL = '/media/'
00169|MEDIA_ROOT = BASE_DIR / 'media'
00170|
00171|UPLOADS_ROOT = BASE_DIR / 'uploads'
00172|OUTPUT_ROOT = BASE_DIR / 'output'
00173|
00174|LOGIN_URL = '/accounts/login/'
00175|LOGIN_REDIRECT_URL = '/panel/'
00176|LOGOUT_REDIRECT_URL = '/accounts/login/'
00177|
00178|DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IyBGaWxlOiBjb25maWcvc2V0dGluZ3MucHkKCmZyb20gcGF0aGxpYiBpbXBvcnQgUGF0aAppbXBvcnQgb3MKaW1wb3J0IGRqX2RhdGFiYXNlX3VybApmcm9tIGRqYW5nby5jb3JlLmV4Y2VwdGlvbnMgaW1wb3J0IEltcHJvcGVybHlDb25maWd1cmVkCgpCQVNFX0RJUiA9IFBhdGgoX19maWxlX18pLnJlc29sdmUoKS5wYXJlbnQucGFyZW50CgojIFNpIERFQlVHIG5vIGVzdMOhIGVuIGVsIGVudG9ybm86CiMgLSBMb2NhbCAoc2luIFJhaWx3YXkpIOKGkiBUcnVlCiMgLSBSYWlsd2F5IC8gY29uIFJBSUxXQVlfKiDihpIgRmFsc2UgKHByb2R1Y2Npw7NuIHNlZ3VyYSBwb3IgZGVmZWN0bykKX3Jhd19kZWJ1ZyA9IG9zLmVudmlyb24uZ2V0KCJERUJVRyIpCmlmIF9yYXdfZGVidWcgaXMgTm9uZToKICAgIF9vbl9yYWlsd2F5ID0gYm9vbCgKICAgICAgICBvcy5lbnZpcm9uLmdldCgiUkFJTFdBWV9FTlZJUk9OTUVOVCIpCiAgICAgICAgb3Igb3MuZW52aXJvbi5nZXQoIlJBSUxXQVlfUFJPSkVDVF9JRCIpCiAgICAgICAgb3Igb3MuZW52aXJvbi5nZXQoIlJBSUxXQVlfU1RBVElDX1VSTCIpCiAgICApCiAgICBERUJVRyA9IG5vdCBfb25fcmFpbHdheQplbHNlOgogICAgREVCVUcgPSBfcmF3X2RlYnVnLmxvd2VyKCkgPT0gInRydWUiCgpfc2VjcmV0ID0gb3MuZW52aXJvbi5nZXQoIlNFQ1JFVF9LRVkiKQppZiBfc2VjcmV0OgogICAgU0VDUkVUX0tFWSA9IF9zZWNyZXQKZWxpZiBERUJVRzoKICAgIFNFQ1JFVF9LRVkgPSAidW5zYWZlLWRldi1rZXkiCmVsc2U6CiAgICByYWlzZSBJbXByb3Blcmx5Q29uZmlndXJlZCgKICAgICAgICAiU0VDUkVUX0tFWSBtdXN0IGJlIHNldCB2aWEgZW52aXJvbm1lbnQgd2hlbiBERUJVRyBpcyBGYWxzZS4iCiAgICApCgpGT1JNQVRfTU9EVUxFX1BBVEggPSBbImNvbmZpZy5mb3JtYXRzIl0KCkFMTE9XRURfSE9TVFMgPSBbCiAgICBob3N0LnN0cmlwKCkKICAgIGZvciBob3N0IGluIG9zLmVudmlyb24uZ2V0KAogICAgICAgICJBTExPV0VEX0hPU1RTIiwKICAgICAgICAiMTI3LjAuMC4xLGxvY2FsaG9zdCIKICAgICkuc3BsaXQoIiwiKQogICAgaWYgaG9zdC5zdHJpcCgpCl0KCkNTUkZfVFJVU1RFRF9PUklHSU5TID0gWwogICAgb3JpZ2luLnN0cmlwKCkKICAgIGZvciBvcmlnaW4gaW4gb3MuZW52aXJvbi5nZXQoCiAgICAgICAgIkNTUkZfVFJVU1RFRF9PUklHSU5TIiwKICAgICAgICAiaHR0cDovLzEyNy4wLjAuMSxodHRwOi8vbG9jYWxob3N0IgogICAgKS5zcGxpdCgiLCIpCiAgICBpZiBvcmlnaW4uc3RyaXAoKQpdCgpTRUNVUkVfUFJPWFlfU1NMX0hFQURFUiA9ICgnSFRUUF9YX0ZPUldBUkRFRF9QUk9UTycsICdodHRwcycpCgppZiBub3QgREVCVUc6CiAgICBTRVNTSU9OX0NPT0tJRV9TRUNVUkUgPSBUcnVlCiAgICBDU1JGX0NPT0tJRV9TRUNVUkUgPSBUcnVlCiAgICBTRUNVUkVfU1NMX1JFRElSRUNUID0gVHJ1ZQogICAgU0VDVVJFX0hTVFNfU0VDT05EUyA9IDMxNTM2MDAwCiAgICBTRUNVUkVfSFNUU19JTkNMVURFX1NVQkRPTUFJTlMgPSBUcnVlCiAgICBTRUNVUkVfSFNUU19QUkVMT0FEID0gVHJ1ZQoKSU5TVEFMTEVEX0FQUFMgPSBbCiAgICAnZGphbmdvLmNvbnRyaWIuYWRtaW4nLAogICAgJ2RqYW5nby5jb250cmliLmF1dGgnLAogICAgJ2RqYW5nby5jb250cmliLmNvbnRlbnR0eXBlcycsCiAgICAnZGphbmdvLmNvbnRyaWIuc2Vzc2lvbnMnLAogICAgJ2RqYW5nby5jb250cmliLm1lc3NhZ2VzJywKICAgICdkamFuZ28uY29udHJpYi5zdGF0aWNmaWxlcycsCgogICAgIyBQR0MxIC8gb3BlcmF0aXZvCiAgICAnY29yZScsCiAgICAnYWNjb3VudHMuYXBwcy5BY2NvdW50c0NvbmZpZycsCiAgICAnaW1wb3J0cycsCiAgICAncGdjJywKICAgICdmZWVkYmFjaycsCiAgICAncG9ydGFsJywKICAgICdjcm0nLAogICAgJ3Jpc2snLAogICAgJ3BnbycsCiAgICAncmVwb3J0cycsCgogICAgIyBXQ0cgT25lIChjb2V4aXN0ZW5jaWEgZGUgbW9kZWxvcyAvIG3Ds2R1bG9zKQogICAgJ2FwcHMucG9ydGFsLmFwcHMuUG9ydGFsQ29uZmlnJywKICAgICdhcHBzLmNvcmUuYXBwcy5Db3JlQ29uZmlnJywKICAgICdhcHBzLmNybS5hcHBzLkNybUNvbmZpZycsCiAgICAnYXBwcy5yaXNrLmFwcHMuUmlza0NvbmZpZycsCiAgICAnYXBwcy5wZ28uYXBwcy5QZ29Db25maWcnLAogICAgJ2FwcHMucGdjLmFwcHMuUGdjQ29uZmlnJywKICAgICdhcHBzLmxlZ2FjeV9wZ2MxLmFwcHMuTGVnYWN5UGdjMUNvbmZpZycsCl0KCk1JRERMRVdBUkUgPSBbCiAgICAnZGphbmdvLm1pZGRsZXdhcmUuc2VjdXJpdHkuU2VjdXJpdHlNaWRkbGV3YXJlJywKICAgICd3aGl0ZW5vaXNlLm1pZGRsZXdhcmUuV2hpdGVOb2lzZU1pZGRsZXdhcmUnLAogICAgJ2RqYW5nby5jb250cmliLnNlc3Npb25zLm1pZGRsZXdhcmUuU2Vzc2lvbk1pZGRsZXdhcmUnLAogICAgJ2RqYW5nby5taWRkbGV3YXJlLmNvbW1vbi5Db21tb25NaWRkbGV3YXJlJywKICAgICdkamFuZ28ubWlkZGxld2FyZS5jc3JmLkNzcmZWaWV3TWlkZGxld2FyZScsCiAgICAnZGphbmdvLmNvbnRyaWIuYXV0aC5taWRkbGV3YXJlLkF1dGhlbnRpY2F0aW9uTWlkZGxld2FyZScsCiAgICAnZGphbmdvLmNvbnRyaWIubWVzc2FnZXMubWlkZGxld2FyZS5NZXNzYWdlTWlkZGxld2FyZScsCiAgICAnZGphbmdvLm1pZGRsZXdhcmUuY2xpY2tqYWNraW5nLlhGcmFtZU9wdGlvbnNNaWRkbGV3YXJlJywKXQoKUk9PVF9VUkxDT05GID0gJ2NvbmZpZy51cmxzJwoKVEVNUExBVEVTID0gWwogICAgewogICAgICAgICdCQUNLRU5EJzogJ2RqYW5nby50ZW1wbGF0ZS5iYWNrZW5kcy5kamFuZ28uRGphbmdvVGVtcGxhdGVzJywKICAgICAgICAnRElSUyc6IFtCQVNFX0RJUiAvICd0ZW1wbGF0ZXMnXSwKICAgICAgICAnQVBQX0RJUlMnOiBUcnVlLAogICAgICAgICdPUFRJT05TJzogewogICAgICAgICAgICAnY29udGV4dF9wcm9jZXNzb3JzJzogWwogICAgICAgICAgICAgICAgJ2RqYW5nby50ZW1wbGF0ZS5jb250ZXh0X3Byb2Nlc3NvcnMuZGVidWcnLAogICAgICAgICAgICAgICAgJ2RqYW5nby50ZW1wbGF0ZS5jb250ZXh0X3Byb2Nlc3NvcnMucmVxdWVzdCcsCiAgICAgICAgICAgICAgICAnZGphbmdvLmNvbnRyaWIuYXV0aC5jb250ZXh0X3Byb2Nlc3NvcnMuYXV0aCcsCiAgICAgICAgICAgICAgICAnZGphbmdvLmNvbnRyaWIubWVzc2FnZXMuY29udGV4dF9wcm9jZXNzb3JzLm1lc3NhZ2VzJywKICAgICAgICAgICAgXSwKICAgICAgICB9LAogICAgfSwKXQoKV1NHSV9BUFBMSUNBVElPTiA9ICdjb25maWcud3NnaS5hcHBsaWNhdGlvbicKCkRBVEFCQVNFX1VSTCA9IG9zLmVudmlyb24uZ2V0KCdEQVRBQkFTRV9VUkwnKQoKaWYgREFUQUJBU0VfVVJMOgogICAgREFUQUJBU0VTID0gewogICAgICAgICdkZWZhdWx0JzogZGpfZGF0YWJhc2VfdXJsLnBhcnNlKAogICAgICAgICAgICBEQVRBQkFTRV9VUkwsCiAgICAgICAgICAgIGNvbm5fbWF4X2FnZT02MDAsCiAgICAgICAgICAgIHNzbF9yZXF1aXJlPVRydWUKICAgICAgICApCiAgICB9CmVsc2U6CiAgICBEQVRBQkFTRVMgPSB7CiAgICAgICAgJ2RlZmF1bHQnOiB7CiAgICAgICAgICAgICdFTkdJTkUnOiAnZGphbmdvLmRiLmJhY2tlbmRzLnNxbGl0ZTMnLAogICAgICAgICAgICAnTkFNRSc6IEJBU0VfRElSIC8gJ2RiLnNxbGl0ZTMnLAogICAgICAgIH0KICAgIH0KCkFVVEhfUEFTU1dPUkRfVkFMSURBVE9SUyA9IFsKICAgIHsKICAgICAgICAnTkFNRSc6ICdkamFuZ28uY29udHJpYi5hdXRoLnBhc3N3b3JkX3ZhbGlkYXRpb24uVXNlckF0dHJpYnV0ZVNpbWlsYXJpdHlWYWxpZGF0b3InLAogICAgfSwKICAgIHsKICAgICAgICAnTkFNRSc6ICdkamFuZ28uY29udHJpYi5hdXRoLnBhc3N3b3JkX3ZhbGlkYXRpb24uTWluaW11bUxlbmd0aFZhbGlkYXRvcicsCiAgICB9LAogICAgewogICAgICAgICdOQU1FJzogJ2RqYW5nby5jb250cmliLmF1dGgucGFzc3dvcmRfdmFsaWRhdGlvbi5Db21tb25QYXNzd29yZFZhbGlkYXRvcicsCiAgICB9LAogICAgewogICAgICAgICdOQU1FJzogJ2RqYW5nby5jb250cmliLmF1dGgucGFzc3dvcmRfdmFsaWRhdGlvbi5OdW1lcmljUGFzc3dvcmRWYWxpZGF0b3InLAogICAgfSwKXQoKTEFOR1VBR0VfQ09ERSA9ICdlcy1ndCcKVElNRV9aT05FID0gJ0FtZXJpY2EvR3VhdGVtYWxhJwpVU0VfSTE4TiA9IFRydWUKVVNFX1RaID0gVHJ1ZQoKU1RBVElDX1VSTCA9ICcvc3RhdGljLycKU1RBVElDX1JPT1QgPSBCQVNFX0RJUiAvICdzdGF0aWNmaWxlcycKU1RBVElDRklMRVNfRElSUyA9IFtCQVNFX0RJUiAvICdzdGF0aWMnXQpTVEFUSUNGSUxFU19TVE9SQUdFID0gJ3doaXRlbm9pc2Uuc3RvcmFnZS5Db21wcmVzc2VkTWFuaWZlc3RTdGF0aWNGaWxlc1N0b3JhZ2UnCgpNRURJQV9VUkwgPSAnL21lZGlhLycKTUVESUFfUk9PVCA9IEJBU0VfRElSIC8gJ21lZGlhJwoKVVBMT0FEU19ST09UID0gQkFTRV9ESVIgLyAndXBsb2FkcycKT1VUUFVUX1JPT1QgPSBCQVNFX0RJUiAvICdvdXRwdXQnCgpMT0dJTl9VUkwgPSAnL2FjY291bnRzL2xvZ2luLycKTE9HSU5fUkVESVJFQ1RfVVJMID0gJy9wYW5lbC8nCkxPR09VVF9SRURJUkVDVF9VUkwgPSAnL2FjY291bnRzL2xvZ2luLycKCkRFRkFVTFRfQVVUT19GSUVMRCA9ICdkamFuZ28uZGIubW9kZWxzLkJpZ0F1dG9GaWVsZCc=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=config/urls.py
PATH_JSON="config/urls.py"
FILENAME=urls.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=37
SIZE_BYTES_UTF8=1307
CONTENT_SHA256=64c5a69e1f9e5ebfa871e63e401347ec77bbfbc4193aa9a4b3f44ff277e2722c
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
from django.urls import include, path
from django.views.generic import RedirectView

from portal import views as portal_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("importaciones/", include("imports.urls")),

    # PGC1 WCG modules (rutas productivas actuales)
    path("crm/", include("crm.urls")),
    path("risk/", include("risk.urls")),
    path("pgo/", include("pgo.urls")),
    path("reports/", include("reports.urls")),

    # Entry: splash → menú
    path("", portal_views.splash, name="splash"),
    path("panel/", include("portal.urls")),
    path(
        "portal/",
        RedirectView.as_view(pattern_name="portal:home", permanent=False),
    ),

    # WCG One apps (modelos/vistas coexistentes bajo namespace)
    path("wcgone/core/", include("apps.core.urls")),
    path("wcgone/crm/", include("apps.crm.urls")),
    path("wcgone/risk/", include("apps.risk.urls")),
    path("wcgone/pgo/", include("apps.pgo.urls")),
    path("wcgone/", include("apps.portal.urls")),
    path("wcgone/pgc/", include("apps.pgc.urls")),
    path("wcgone/legacy-pgc1/", include("apps.legacy_pgc1.urls")),

    # PGC productivo (mantener rutas actuales)
    path("", include("pgc.urls")),
]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib import admin
00002|from django.urls import include, path
00003|from django.views.generic import RedirectView
00004|
00005|from portal import views as portal_views
00006|
00007|urlpatterns = [
00008|    path("admin/", admin.site.urls),
00009|    path("accounts/", include("django.contrib.auth.urls")),
00010|    path("importaciones/", include("imports.urls")),
00011|
00012|    # PGC1 WCG modules (rutas productivas actuales)
00013|    path("crm/", include("crm.urls")),
00014|    path("risk/", include("risk.urls")),
00015|    path("pgo/", include("pgo.urls")),
00016|    path("reports/", include("reports.urls")),
00017|
00018|    # Entry: splash → menú
00019|    path("", portal_views.splash, name="splash"),
00020|    path("panel/", include("portal.urls")),
00021|    path(
00022|        "portal/",
00023|        RedirectView.as_view(pattern_name="portal:home", permanent=False),
00024|    ),
00025|
00026|    # WCG One apps (modelos/vistas coexistentes bajo namespace)
00027|    path("wcgone/core/", include("apps.core.urls")),
00028|    path("wcgone/crm/", include("apps.crm.urls")),
00029|    path("wcgone/risk/", include("apps.risk.urls")),
00030|    path("wcgone/pgo/", include("apps.pgo.urls")),
00031|    path("wcgone/", include("apps.portal.urls")),
00032|    path("wcgone/pgc/", include("apps.pgc.urls")),
00033|    path("wcgone/legacy-pgc1/", include("apps.legacy_pgc1.urls")),
00034|
00035|    # PGC productivo (mantener rutas actuales)
00036|    path("", include("pgc.urls")),
00037|]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgYWRtaW4KZnJvbSBkamFuZ28udXJscyBpbXBvcnQgaW5jbHVkZSwgcGF0aApmcm9tIGRqYW5nby52aWV3cy5nZW5lcmljIGltcG9ydCBSZWRpcmVjdFZpZXcKCmZyb20gcG9ydGFsIGltcG9ydCB2aWV3cyBhcyBwb3J0YWxfdmlld3MKCnVybHBhdHRlcm5zID0gWwogICAgcGF0aCgiYWRtaW4vIiwgYWRtaW4uc2l0ZS51cmxzKSwKICAgIHBhdGgoImFjY291bnRzLyIsIGluY2x1ZGUoImRqYW5nby5jb250cmliLmF1dGgudXJscyIpKSwKICAgIHBhdGgoImltcG9ydGFjaW9uZXMvIiwgaW5jbHVkZSgiaW1wb3J0cy51cmxzIikpLAoKICAgICMgUEdDMSBXQ0cgbW9kdWxlcyAocnV0YXMgcHJvZHVjdGl2YXMgYWN0dWFsZXMpCiAgICBwYXRoKCJjcm0vIiwgaW5jbHVkZSgiY3JtLnVybHMiKSksCiAgICBwYXRoKCJyaXNrLyIsIGluY2x1ZGUoInJpc2sudXJscyIpKSwKICAgIHBhdGgoInBnby8iLCBpbmNsdWRlKCJwZ28udXJscyIpKSwKICAgIHBhdGgoInJlcG9ydHMvIiwgaW5jbHVkZSgicmVwb3J0cy51cmxzIikpLAoKICAgICMgRW50cnk6IHNwbGFzaCDihpIgbWVuw7oKICAgIHBhdGgoIiIsIHBvcnRhbF92aWV3cy5zcGxhc2gsIG5hbWU9InNwbGFzaCIpLAogICAgcGF0aCgicGFuZWwvIiwgaW5jbHVkZSgicG9ydGFsLnVybHMiKSksCiAgICBwYXRoKAogICAgICAgICJwb3J0YWwvIiwKICAgICAgICBSZWRpcmVjdFZpZXcuYXNfdmlldyhwYXR0ZXJuX25hbWU9InBvcnRhbDpob21lIiwgcGVybWFuZW50PUZhbHNlKSwKICAgICksCgogICAgIyBXQ0cgT25lIGFwcHMgKG1vZGVsb3MvdmlzdGFzIGNvZXhpc3RlbnRlcyBiYWpvIG5hbWVzcGFjZSkKICAgIHBhdGgoIndjZ29uZS9jb3JlLyIsIGluY2x1ZGUoImFwcHMuY29yZS51cmxzIikpLAogICAgcGF0aCgid2Nnb25lL2NybS8iLCBpbmNsdWRlKCJhcHBzLmNybS51cmxzIikpLAogICAgcGF0aCgid2Nnb25lL3Jpc2svIiwgaW5jbHVkZSgiYXBwcy5yaXNrLnVybHMiKSksCiAgICBwYXRoKCJ3Y2dvbmUvcGdvLyIsIGluY2x1ZGUoImFwcHMucGdvLnVybHMiKSksCiAgICBwYXRoKCJ3Y2dvbmUvIiwgaW5jbHVkZSgiYXBwcy5wb3J0YWwudXJscyIpKSwKICAgIHBhdGgoIndjZ29uZS9wZ2MvIiwgaW5jbHVkZSgiYXBwcy5wZ2MudXJscyIpKSwKICAgIHBhdGgoIndjZ29uZS9sZWdhY3ktcGdjMS8iLCBpbmNsdWRlKCJhcHBzLmxlZ2FjeV9wZ2MxLnVybHMiKSksCgogICAgIyBQR0MgcHJvZHVjdGl2byAobWFudGVuZXIgcnV0YXMgYWN0dWFsZXMpCiAgICBwYXRoKCIiLCBpbmNsdWRlKCJwZ2MudXJscyIpKSwKXQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=config/wsgi.py
PATH_JSON="config/wsgi.py"
FILENAME=wsgi.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=16
SIZE_BYTES_UTF8=389
CONTENT_SHA256=07e8b25db61f1d80eea4604c8bbea579308525c2eaefb5ab45e64a9e29c9841d
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
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|WSGI config for config project.
00003|
00004|It exposes the WSGI callable as a module-level variable named ``application``.
00005|
00006|For more information on this file, see
00007|https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
00008|"""
00009|
00010|import os
00011|
00012|from django.core.wsgi import get_wsgi_application
00013|
00014|os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
00015|
00016|application = get_wsgi_application()

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiCldTR0kgY29uZmlnIGZvciBjb25maWcgcHJvamVjdC4KCkl0IGV4cG9zZXMgdGhlIFdTR0kgY2FsbGFibGUgYXMgYSBtb2R1bGUtbGV2ZWwgdmFyaWFibGUgbmFtZWQgYGBhcHBsaWNhdGlvbmBgLgoKRm9yIG1vcmUgaW5mb3JtYXRpb24gb24gdGhpcyBmaWxlLCBzZWUKaHR0cHM6Ly9kb2NzLmRqYW5nb3Byb2plY3QuY29tL2VuLzUuMC9ob3d0by9kZXBsb3ltZW50L3dzZ2kvCiIiIgoKaW1wb3J0IG9zCgpmcm9tIGRqYW5nby5jb3JlLndzZ2kgaW1wb3J0IGdldF93c2dpX2FwcGxpY2F0aW9uCgpvcy5lbnZpcm9uLnNldGRlZmF1bHQoIkRKQU5HT19TRVRUSU5HU19NT0RVTEUiLCAiY29uZmlnLnNldHRpbmdzIikKCmFwcGxpY2F0aW9uID0gZ2V0X3dzZ2lfYXBwbGljYXRpb24oKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/__init__.py
PATH_JSON="core/__init__.py"
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
PATH_LITERAL=core/admin.py
PATH_JSON="core/admin.py"
FILENAME=admin.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=237
SIZE_BYTES_UTF8=8116
CONTENT_SHA256=92b13d9c83510248a494f20b2b8f4c03c725041c2dae7a6c0c5f854a4f680178
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
# core/admin.py 

from django import forms
from django.contrib import admin, messages
from django.core.management import call_command
from django.shortcuts import redirect, render
from django.urls import path, reverse

from .models import (
    UNE,
    UNEAlias,
    Currency,
    MetricDefinition,
    SystemSetting,
    Contacto,
    DataDictionary,
    DataImportBatch,
    Entidad,
    Producto,
    RelacionEntidadProducto,
    UnidadNegocio,
)


class RecalcOpsForm(forms.Form):
    year = forms.IntegerField(min_value=2020, max_value=2100, initial=2026, label="Año")
    month = forms.IntegerField(min_value=1, max_value=12, initial=4, label="Mes")
    run_investment_ingresos = forms.BooleanField(
        required=False, initial=True, label="Recalcular ingresos Investment"
    )
    run_pgc = forms.BooleanField(
        required=False, initial=True, label="Recalcular PGC"
    )
    mode = forms.ChoiceField(
        choices=[("modo1", "Modo 1"), ("modo2", "Modo 2")],
        initial="modo1",
        label="Modalidad de cálculo de PGC",
    )
  

@admin.register(UNE)
class UneAdmin(admin.ModelAdmin):
    list_display = ("code", "name_es", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    search_fields = ("code", "name", "name_es")


@admin.register(UNEAlias)
class UneAliasAdmin(admin.ModelAdmin):
    list_display = ("raw_value", "une", "alias_type", "is_active")
    list_filter = ("une", "is_active")
    search_fields = ("raw_value",)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "symbol", "is_active")
    list_editable = ("is_active",)
    search_fields = ("code", "name")


@admin.register(MetricDefinition)
class MetricDefinitionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_scored")
    list_editable = ("is_scored",)
    search_fields = ("code", "name")


class RecalcOpsForm(forms.Form):
    year = forms.IntegerField(min_value=2020, max_value=2100, initial=2026, label="Año")
    month = forms.IntegerField(min_value=1, max_value=12, initial=4, label="Mes")
    run_investment_ingresos = forms.BooleanField(required=False, initial=True, label="Recalcular ingresos Investment")
    run_pgc = forms.BooleanField(required=False, initial=True, label="Recalcular PGC")


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "value_text", "value_bool", "updated_by", "updated_at")
    list_filter = ("value_bool",)
    search_fields = ("key", "description", "value_text")
    readonly_fields = ("created_at", "updated_at", "updated_by")
    change_list_template = "admin/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "run-recalc-ops/",
                self.admin_site.admin_view(self.run_recalc_ops_view),
                name="core_systemsetting_run_recalc_ops",
            ),
        ]
        return custom_urls + urls

    def run_recalc_ops_view(self, request):
        if not request.user.is_superuser:
            self.message_user(
                request,
                "Solo superusuarios pueden ejecutar estas operaciones.",
                level=messages.ERROR,
            )
            return redirect("admin:core_systemsetting_changelist")

        if request.method == "POST":
            form = RecalcOpsForm(request.POST)
            if form.is_valid():
                year = form.cleaned_data["year"]
                month = form.cleaned_data["month"]
                mode = form.cleaned_data["mode"]
                run_investment_ingresos = form.cleaned_data["run_investment_ingresos"]
                run_pgc = form.cleaned_data["run_pgc"]

                if not run_investment_ingresos and not run_pgc:
                    self.message_user(
                        request,
                        "Debes seleccionar al menos una operación.",
                        level=messages.WARNING,
                    )
                    return redirect("admin:core_systemsetting_run_recalc_ops")

                try:
                    if run_investment_ingresos:
                        call_command(
                            "recalc_investment_ingresos_from_new_clients",
                            year=year,
                            month=month,
                        )
                        self.message_user(
                            request,
                            f"Ingresos Investment recalculados para {year}-{month:02d}.",
                            level=messages.SUCCESS,
                        )

                    if run_pgc:
                        call_command(
                            "recalc_pgc",
                            year=year,
                            month=month, 
                            mode=mode
                        )
                        self.message_user(
                            request,
                            f"PGC recalculado para {year}-{month:02d} en {mode}.",
        level=messages.SUCCESS,
                        )

                    return redirect("admin:core_systemsetting_changelist")

                except Exception as exc:
                    self.message_user(
                        request,
                        f"Error al ejecutar operaciones: {exc}",
                        level=messages.ERROR,
                    )
        else:
            form = RecalcOpsForm()

        context = {
            **self.admin_site.each_context(request),
            "title": "Operaciones de recálculo",
            "form": form,
            "opts": self.model._meta,
            "has_view_permission": self.has_view_permission(request),
        }
        return render(
            request,
            "admin/run_recalc_ops.html",
            context,
        )


@admin.register(UnidadNegocio)
class UnidadNegocioAdmin(admin.ModelAdmin):
    list_display = ("code", "nombre", "une_pgc", "activa", "updated_at")
    list_filter = ("activa",)
    search_fields = ("code", "nombre")
    ordering = ("nombre",)


@admin.register(Entidad)
class EntidadAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "nit", "tipo", "unidad_negocio", "activa")
    list_filter = ("tipo", "activa", "unidad_negocio")
    search_fields = ("codigo", "nombre", "nit")
    ordering = ("nombre",)


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "entidad", "email", "telefono", "es_principal", "activo")
    list_filter = ("es_principal", "activo", "entidad")
    search_fields = ("nombre", "email", "entidad__codigo", "entidad__nombre")
    ordering = ("entidad__nombre", "nombre")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "unidad_negocio", "activo")
    list_filter = ("activo", "unidad_negocio")
    search_fields = ("codigo", "nombre")
    ordering = ("nombre",)


@admin.register(RelacionEntidadProducto)
class RelacionEntidadProductoAdmin(admin.ModelAdmin):
    list_display = ("entidad", "producto", "estado", "fecha_inicio")
    list_filter = ("estado", "producto")
    search_fields = ("entidad__codigo", "entidad__nombre", "producto__codigo")
    ordering = ("entidad__nombre",)


@admin.register(DataDictionary)
class DataDictionaryAdmin(admin.ModelAdmin):
    list_display = ("modulo", "tabla", "campo", "etiqueta", "obligatorio")
    list_filter = ("modulo", "obligatorio")
    search_fields = ("modulo", "tabla", "campo", "etiqueta")
    ordering = ("modulo", "tabla", "campo")


@admin.register(DataImportBatch)
class DataImportBatchAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "modulo",
        "tipo_importacion",
        "archivo_nombre",
        "status",
        "creados",
        "actualizados",
        "errores",
        "uploaded_by",
    )
    list_filter = ("modulo", "status", "tipo_importacion")
    search_fields = ("archivo_nombre", "tipo_importacion", "log_texto")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|# core/admin.py 
00002|
00003|from django import forms
00004|from django.contrib import admin, messages
00005|from django.core.management import call_command
00006|from django.shortcuts import redirect, render
00007|from django.urls import path, reverse
00008|
00009|from .models import (
00010|    UNE,
00011|    UNEAlias,
00012|    Currency,
00013|    MetricDefinition,
00014|    SystemSetting,
00015|    Contacto,
00016|    DataDictionary,
00017|    DataImportBatch,
00018|    Entidad,
00019|    Producto,
00020|    RelacionEntidadProducto,
00021|    UnidadNegocio,
00022|)
00023|
00024|
00025|class RecalcOpsForm(forms.Form):
00026|    year = forms.IntegerField(min_value=2020, max_value=2100, initial=2026, label="Año")
00027|    month = forms.IntegerField(min_value=1, max_value=12, initial=4, label="Mes")
00028|    run_investment_ingresos = forms.BooleanField(
00029|        required=False, initial=True, label="Recalcular ingresos Investment"
00030|    )
00031|    run_pgc = forms.BooleanField(
00032|        required=False, initial=True, label="Recalcular PGC"
00033|    )
00034|    mode = forms.ChoiceField(
00035|        choices=[("modo1", "Modo 1"), ("modo2", "Modo 2")],
00036|        initial="modo1",
00037|        label="Modalidad de cálculo de PGC",
00038|    )
00039|  
00040|
00041|@admin.register(UNE)
00042|class UneAdmin(admin.ModelAdmin):
00043|    list_display = ("code", "name_es", "is_active", "sort_order")
00044|    list_editable = ("is_active", "sort_order")
00045|    search_fields = ("code", "name", "name_es")
00046|
00047|
00048|@admin.register(UNEAlias)
00049|class UneAliasAdmin(admin.ModelAdmin):
00050|    list_display = ("raw_value", "une", "alias_type", "is_active")
00051|    list_filter = ("une", "is_active")
00052|    search_fields = ("raw_value",)
00053|
00054|
00055|@admin.register(Currency)
00056|class CurrencyAdmin(admin.ModelAdmin):
00057|    list_display = ("code", "name", "symbol", "is_active")
00058|    list_editable = ("is_active",)
00059|    search_fields = ("code", "name")
00060|
00061|
00062|@admin.register(MetricDefinition)
00063|class MetricDefinitionAdmin(admin.ModelAdmin):
00064|    list_display = ("code", "name", "is_scored")
00065|    list_editable = ("is_scored",)
00066|    search_fields = ("code", "name")
00067|
00068|
00069|class RecalcOpsForm(forms.Form):
00070|    year = forms.IntegerField(min_value=2020, max_value=2100, initial=2026, label="Año")
00071|    month = forms.IntegerField(min_value=1, max_value=12, initial=4, label="Mes")
00072|    run_investment_ingresos = forms.BooleanField(required=False, initial=True, label="Recalcular ingresos Investment")
00073|    run_pgc = forms.BooleanField(required=False, initial=True, label="Recalcular PGC")
00074|
00075|
00076|@admin.register(SystemSetting)
00077|class SystemSettingAdmin(admin.ModelAdmin):
00078|    list_display = ("key", "value_text", "value_bool", "updated_by", "updated_at")
00079|    list_filter = ("value_bool",)
00080|    search_fields = ("key", "description", "value_text")
00081|    readonly_fields = ("created_at", "updated_at", "updated_by")
00082|    change_list_template = "admin/change_list.html"
00083|
00084|    def get_urls(self):
00085|        urls = super().get_urls()
00086|        custom_urls = [
00087|            path(
00088|                "run-recalc-ops/",
00089|                self.admin_site.admin_view(self.run_recalc_ops_view),
00090|                name="core_systemsetting_run_recalc_ops",
00091|            ),
00092|        ]
00093|        return custom_urls + urls
00094|
00095|    def run_recalc_ops_view(self, request):
00096|        if not request.user.is_superuser:
00097|            self.message_user(
00098|                request,
00099|                "Solo superusuarios pueden ejecutar estas operaciones.",
00100|                level=messages.ERROR,
00101|            )
00102|            return redirect("admin:core_systemsetting_changelist")
00103|
00104|        if request.method == "POST":
00105|            form = RecalcOpsForm(request.POST)
00106|            if form.is_valid():
00107|                year = form.cleaned_data["year"]
00108|                month = form.cleaned_data["month"]
00109|                mode = form.cleaned_data["mode"]
00110|                run_investment_ingresos = form.cleaned_data["run_investment_ingresos"]
00111|                run_pgc = form.cleaned_data["run_pgc"]
00112|
00113|                if not run_investment_ingresos and not run_pgc:
00114|                    self.message_user(
00115|                        request,
00116|                        "Debes seleccionar al menos una operación.",
00117|                        level=messages.WARNING,
00118|                    )
00119|                    return redirect("admin:core_systemsetting_run_recalc_ops")
00120|
00121|                try:
00122|                    if run_investment_ingresos:
00123|                        call_command(
00124|                            "recalc_investment_ingresos_from_new_clients",
00125|                            year=year,
00126|                            month=month,
00127|                        )
00128|                        self.message_user(
00129|                            request,
00130|                            f"Ingresos Investment recalculados para {year}-{month:02d}.",
00131|                            level=messages.SUCCESS,
00132|                        )
00133|
00134|                    if run_pgc:
00135|                        call_command(
00136|                            "recalc_pgc",
00137|                            year=year,
00138|                            month=month, 
00139|                            mode=mode
00140|                        )
00141|                        self.message_user(
00142|                            request,
00143|                            f"PGC recalculado para {year}-{month:02d} en {mode}.",
00144|        level=messages.SUCCESS,
00145|                        )
00146|
00147|                    return redirect("admin:core_systemsetting_changelist")
00148|
00149|                except Exception as exc:
00150|                    self.message_user(
00151|                        request,
00152|                        f"Error al ejecutar operaciones: {exc}",
00153|                        level=messages.ERROR,
00154|                    )
00155|        else:
00156|            form = RecalcOpsForm()
00157|
00158|        context = {
00159|            **self.admin_site.each_context(request),
00160|            "title": "Operaciones de recálculo",
00161|            "form": form,
00162|            "opts": self.model._meta,
00163|            "has_view_permission": self.has_view_permission(request),
00164|        }
00165|        return render(
00166|            request,
00167|            "admin/run_recalc_ops.html",
00168|            context,
00169|        )
00170|
00171|
00172|@admin.register(UnidadNegocio)
00173|class UnidadNegocioAdmin(admin.ModelAdmin):
00174|    list_display = ("code", "nombre", "une_pgc", "activa", "updated_at")
00175|    list_filter = ("activa",)
00176|    search_fields = ("code", "nombre")
00177|    ordering = ("nombre",)
00178|
00179|
00180|@admin.register(Entidad)
00181|class EntidadAdmin(admin.ModelAdmin):
00182|    list_display = ("codigo", "nombre", "nit", "tipo", "unidad_negocio", "activa")
00183|    list_filter = ("tipo", "activa", "unidad_negocio")
00184|    search_fields = ("codigo", "nombre", "nit")
00185|    ordering = ("nombre",)
00186|
00187|
00188|@admin.register(Contacto)
00189|class ContactoAdmin(admin.ModelAdmin):
00190|    list_display = ("nombre", "entidad", "email", "telefono", "es_principal", "activo")
00191|    list_filter = ("es_principal", "activo", "entidad")
00192|    search_fields = ("nombre", "email", "entidad__codigo", "entidad__nombre")
00193|    ordering = ("entidad__nombre", "nombre")
00194|
00195|
00196|@admin.register(Producto)
00197|class ProductoAdmin(admin.ModelAdmin):
00198|    list_display = ("codigo", "nombre", "unidad_negocio", "activo")
00199|    list_filter = ("activo", "unidad_negocio")
00200|    search_fields = ("codigo", "nombre")
00201|    ordering = ("nombre",)
00202|
00203|
00204|@admin.register(RelacionEntidadProducto)
00205|class RelacionEntidadProductoAdmin(admin.ModelAdmin):
00206|    list_display = ("entidad", "producto", "estado", "fecha_inicio")
00207|    list_filter = ("estado", "producto")
00208|    search_fields = ("entidad__codigo", "entidad__nombre", "producto__codigo")
00209|    ordering = ("entidad__nombre",)
00210|
00211|
00212|@admin.register(DataDictionary)
00213|class DataDictionaryAdmin(admin.ModelAdmin):
00214|    list_display = ("modulo", "tabla", "campo", "etiqueta", "obligatorio")
00215|    list_filter = ("modulo", "obligatorio")
00216|    search_fields = ("modulo", "tabla", "campo", "etiqueta")
00217|    ordering = ("modulo", "tabla", "campo")
00218|
00219|
00220|@admin.register(DataImportBatch)
00221|class DataImportBatchAdmin(admin.ModelAdmin):
00222|    list_display = (
00223|        "created_at",
00224|        "modulo",
00225|        "tipo_importacion",
00226|        "archivo_nombre",
00227|        "status",
00228|        "creados",
00229|        "actualizados",
00230|        "errores",
00231|        "uploaded_by",
00232|    )
00233|    list_filter = ("modulo", "status", "tipo_importacion")
00234|    search_fields = ("archivo_nombre", "tipo_importacion", "log_texto")
00235|    ordering = ("-created_at",)
00236|    readonly_fields = ("created_at", "updated_at")
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IyBjb3JlL2FkbWluLnB5IAoKZnJvbSBkamFuZ28gaW1wb3J0IGZvcm1zCmZyb20gZGphbmdvLmNvbnRyaWIgaW1wb3J0IGFkbWluLCBtZXNzYWdlcwpmcm9tIGRqYW5nby5jb3JlLm1hbmFnZW1lbnQgaW1wb3J0IGNhbGxfY29tbWFuZApmcm9tIGRqYW5nby5zaG9ydGN1dHMgaW1wb3J0IHJlZGlyZWN0LCByZW5kZXIKZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcGF0aCwgcmV2ZXJzZQoKZnJvbSAubW9kZWxzIGltcG9ydCAoCiAgICBVTkUsCiAgICBVTkVBbGlhcywKICAgIEN1cnJlbmN5LAogICAgTWV0cmljRGVmaW5pdGlvbiwKICAgIFN5c3RlbVNldHRpbmcsCiAgICBDb250YWN0bywKICAgIERhdGFEaWN0aW9uYXJ5LAogICAgRGF0YUltcG9ydEJhdGNoLAogICAgRW50aWRhZCwKICAgIFByb2R1Y3RvLAogICAgUmVsYWNpb25FbnRpZGFkUHJvZHVjdG8sCiAgICBVbmlkYWROZWdvY2lvLAopCgoKY2xhc3MgUmVjYWxjT3BzRm9ybShmb3Jtcy5Gb3JtKToKICAgIHllYXIgPSBmb3Jtcy5JbnRlZ2VyRmllbGQobWluX3ZhbHVlPTIwMjAsIG1heF92YWx1ZT0yMTAwLCBpbml0aWFsPTIwMjYsIGxhYmVsPSJBw7FvIikKICAgIG1vbnRoID0gZm9ybXMuSW50ZWdlckZpZWxkKG1pbl92YWx1ZT0xLCBtYXhfdmFsdWU9MTIsIGluaXRpYWw9NCwgbGFiZWw9Ik1lcyIpCiAgICBydW5faW52ZXN0bWVudF9pbmdyZXNvcyA9IGZvcm1zLkJvb2xlYW5GaWVsZCgKICAgICAgICByZXF1aXJlZD1GYWxzZSwgaW5pdGlhbD1UcnVlLCBsYWJlbD0iUmVjYWxjdWxhciBpbmdyZXNvcyBJbnZlc3RtZW50IgogICAgKQogICAgcnVuX3BnYyA9IGZvcm1zLkJvb2xlYW5GaWVsZCgKICAgICAgICByZXF1aXJlZD1GYWxzZSwgaW5pdGlhbD1UcnVlLCBsYWJlbD0iUmVjYWxjdWxhciBQR0MiCiAgICApCiAgICBtb2RlID0gZm9ybXMuQ2hvaWNlRmllbGQoCiAgICAgICAgY2hvaWNlcz1bKCJtb2RvMSIsICJNb2RvIDEiKSwgKCJtb2RvMiIsICJNb2RvIDIiKV0sCiAgICAgICAgaW5pdGlhbD0ibW9kbzEiLAogICAgICAgIGxhYmVsPSJNb2RhbGlkYWQgZGUgY8OhbGN1bG8gZGUgUEdDIiwKICAgICkKICAKCkBhZG1pbi5yZWdpc3RlcihVTkUpCmNsYXNzIFVuZUFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKCJjb2RlIiwgIm5hbWVfZXMiLCAiaXNfYWN0aXZlIiwgInNvcnRfb3JkZXIiKQogICAgbGlzdF9lZGl0YWJsZSA9ICgiaXNfYWN0aXZlIiwgInNvcnRfb3JkZXIiKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgiY29kZSIsICJuYW1lIiwgIm5hbWVfZXMiKQoKCkBhZG1pbi5yZWdpc3RlcihVTkVBbGlhcykKY2xhc3MgVW5lQWxpYXNBZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgicmF3X3ZhbHVlIiwgInVuZSIsICJhbGlhc190eXBlIiwgImlzX2FjdGl2ZSIpCiAgICBsaXN0X2ZpbHRlciA9ICgidW5lIiwgImlzX2FjdGl2ZSIpCiAgICBzZWFyY2hfZmllbGRzID0gKCJyYXdfdmFsdWUiLCkKCgpAYWRtaW4ucmVnaXN0ZXIoQ3VycmVuY3kpCmNsYXNzIEN1cnJlbmN5QWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoImNvZGUiLCAibmFtZSIsICJzeW1ib2wiLCAiaXNfYWN0aXZlIikKICAgIGxpc3RfZWRpdGFibGUgPSAoImlzX2FjdGl2ZSIsKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgiY29kZSIsICJuYW1lIikKCgpAYWRtaW4ucmVnaXN0ZXIoTWV0cmljRGVmaW5pdGlvbikKY2xhc3MgTWV0cmljRGVmaW5pdGlvbkFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKCJjb2RlIiwgIm5hbWUiLCAiaXNfc2NvcmVkIikKICAgIGxpc3RfZWRpdGFibGUgPSAoImlzX3Njb3JlZCIsKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgiY29kZSIsICJuYW1lIikKCgpjbGFzcyBSZWNhbGNPcHNGb3JtKGZvcm1zLkZvcm0pOgogICAgeWVhciA9IGZvcm1zLkludGVnZXJGaWVsZChtaW5fdmFsdWU9MjAyMCwgbWF4X3ZhbHVlPTIxMDAsIGluaXRpYWw9MjAyNiwgbGFiZWw9IkHDsW8iKQogICAgbW9udGggPSBmb3Jtcy5JbnRlZ2VyRmllbGQobWluX3ZhbHVlPTEsIG1heF92YWx1ZT0xMiwgaW5pdGlhbD00LCBsYWJlbD0iTWVzIikKICAgIHJ1bl9pbnZlc3RtZW50X2luZ3Jlc29zID0gZm9ybXMuQm9vbGVhbkZpZWxkKHJlcXVpcmVkPUZhbHNlLCBpbml0aWFsPVRydWUsIGxhYmVsPSJSZWNhbGN1bGFyIGluZ3Jlc29zIEludmVzdG1lbnQiKQogICAgcnVuX3BnYyA9IGZvcm1zLkJvb2xlYW5GaWVsZChyZXF1aXJlZD1GYWxzZSwgaW5pdGlhbD1UcnVlLCBsYWJlbD0iUmVjYWxjdWxhciBQR0MiKQoKCkBhZG1pbi5yZWdpc3RlcihTeXN0ZW1TZXR0aW5nKQpjbGFzcyBTeXN0ZW1TZXR0aW5nQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoImtleSIsICJ2YWx1ZV90ZXh0IiwgInZhbHVlX2Jvb2wiLCAidXBkYXRlZF9ieSIsICJ1cGRhdGVkX2F0IikKICAgIGxpc3RfZmlsdGVyID0gKCJ2YWx1ZV9ib29sIiwpCiAgICBzZWFyY2hfZmllbGRzID0gKCJrZXkiLCAiZGVzY3JpcHRpb24iLCAidmFsdWVfdGV4dCIpCiAgICByZWFkb25seV9maWVsZHMgPSAoImNyZWF0ZWRfYXQiLCAidXBkYXRlZF9hdCIsICJ1cGRhdGVkX2J5IikKICAgIGNoYW5nZV9saXN0X3RlbXBsYXRlID0gImFkbWluL2NoYW5nZV9saXN0Lmh0bWwiCgogICAgZGVmIGdldF91cmxzKHNlbGYpOgogICAgICAgIHVybHMgPSBzdXBlcigpLmdldF91cmxzKCkKICAgICAgICBjdXN0b21fdXJscyA9IFsKICAgICAgICAgICAgcGF0aCgKICAgICAgICAgICAgICAgICJydW4tcmVjYWxjLW9wcy8iLAogICAgICAgICAgICAgICAgc2VsZi5hZG1pbl9zaXRlLmFkbWluX3ZpZXcoc2VsZi5ydW5fcmVjYWxjX29wc192aWV3KSwKICAgICAgICAgICAgICAgIG5hbWU9ImNvcmVfc3lzdGVtc2V0dGluZ19ydW5fcmVjYWxjX29wcyIsCiAgICAgICAgICAgICksCiAgICAgICAgXQogICAgICAgIHJldHVybiBjdXN0b21fdXJscyArIHVybHMKCiAgICBkZWYgcnVuX3JlY2FsY19vcHNfdmlldyhzZWxmLCByZXF1ZXN0KToKICAgICAgICBpZiBub3QgcmVxdWVzdC51c2VyLmlzX3N1cGVydXNlcjoKICAgICAgICAgICAgc2VsZi5tZXNzYWdlX3VzZXIoCiAgICAgICAgICAgICAgICByZXF1ZXN0LAogICAgICAgICAgICAgICAgIlNvbG8gc3VwZXJ1c3VhcmlvcyBwdWVkZW4gZWplY3V0YXIgZXN0YXMgb3BlcmFjaW9uZXMuIiwKICAgICAgICAgICAgICAgIGxldmVsPW1lc3NhZ2VzLkVSUk9SLAogICAgICAgICAgICApCiAgICAgICAgICAgIHJldHVybiByZWRpcmVjdCgiYWRtaW46Y29yZV9zeXN0ZW1zZXR0aW5nX2NoYW5nZWxpc3QiKQoKICAgICAgICBpZiByZXF1ZXN0Lm1ldGhvZCA9PSAiUE9TVCI6CiAgICAgICAgICAgIGZvcm0gPSBSZWNhbGNPcHNGb3JtKHJlcXVlc3QuUE9TVCkKICAgICAgICAgICAgaWYgZm9ybS5pc192YWxpZCgpOgogICAgICAgICAgICAgICAgeWVhciA9IGZvcm0uY2xlYW5lZF9kYXRhWyJ5ZWFyIl0KICAgICAgICAgICAgICAgIG1vbnRoID0gZm9ybS5jbGVhbmVkX2RhdGFbIm1vbnRoIl0KICAgICAgICAgICAgICAgIG1vZGUgPSBmb3JtLmNsZWFuZWRfZGF0YVsibW9kZSJdCiAgICAgICAgICAgICAgICBydW5faW52ZXN0bWVudF9pbmdyZXNvcyA9IGZvcm0uY2xlYW5lZF9kYXRhWyJydW5faW52ZXN0bWVudF9pbmdyZXNvcyJdCiAgICAgICAgICAgICAgICBydW5fcGdjID0gZm9ybS5jbGVhbmVkX2RhdGFbInJ1bl9wZ2MiXQoKICAgICAgICAgICAgICAgIGlmIG5vdCBydW5faW52ZXN0bWVudF9pbmdyZXNvcyBhbmQgbm90IHJ1bl9wZ2M6CiAgICAgICAgICAgICAgICAgICAgc2VsZi5tZXNzYWdlX3VzZXIoCiAgICAgICAgICAgICAgICAgICAgICAgIHJlcXVlc3QsCiAgICAgICAgICAgICAgICAgICAgICAgICJEZWJlcyBzZWxlY2Npb25hciBhbCBtZW5vcyB1bmEgb3BlcmFjacOzbi4iLAogICAgICAgICAgICAgICAgICAgICAgICBsZXZlbD1tZXNzYWdlcy5XQVJOSU5HLAogICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgICAgICByZXR1cm4gcmVkaXJlY3QoImFkbWluOmNvcmVfc3lzdGVtc2V0dGluZ19ydW5fcmVjYWxjX29wcyIpCgogICAgICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgICAgIGlmIHJ1bl9pbnZlc3RtZW50X2luZ3Jlc29zOgogICAgICAgICAgICAgICAgICAgICAgICBjYWxsX2NvbW1hbmQoCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAicmVjYWxjX2ludmVzdG1lbnRfaW5ncmVzb3NfZnJvbV9uZXdfY2xpZW50cyIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBtb250aD1tb250aCwKICAgICAgICAgICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgICAgICAgICBzZWxmLm1lc3NhZ2VfdXNlcigKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHJlcXVlc3QsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBmIkluZ3Jlc29zIEludmVzdG1lbnQgcmVjYWxjdWxhZG9zIHBhcmEge3llYXJ9LXttb250aDowMmR9LiIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBsZXZlbD1tZXNzYWdlcy5TVUNDRVNTLAogICAgICAgICAgICAgICAgICAgICAgICApCgogICAgICAgICAgICAgICAgICAgIGlmIHJ1bl9wZ2M6CiAgICAgICAgICAgICAgICAgICAgICAgIGNhbGxfY29tbWFuZCgKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJyZWNhbGNfcGdjIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLCAKICAgICAgICAgICAgICAgICAgICAgICAgICAgIG1vZGU9bW9kZQogICAgICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAgICAgICAgIHNlbGYubWVzc2FnZV91c2VyKAogICAgICAgICAgICAgICAgICAgICAgICAgICAgcmVxdWVzdCwKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGYiUEdDIHJlY2FsY3VsYWRvIHBhcmEge3llYXJ9LXttb250aDowMmR9IGVuIHttb2RlfS4iLAogICAgICAgIGxldmVsPW1lc3NhZ2VzLlNVQ0NFU1MsCiAgICAgICAgICAgICAgICAgICAgICAgICkKCiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHJlZGlyZWN0KCJhZG1pbjpjb3JlX3N5c3RlbXNldHRpbmdfY2hhbmdlbGlzdCIpCgogICAgICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBleGM6CiAgICAgICAgICAgICAgICAgICAgc2VsZi5tZXNzYWdlX3VzZXIoCiAgICAgICAgICAgICAgICAgICAgICAgIHJlcXVlc3QsCiAgICAgICAgICAgICAgICAgICAgICAgIGYiRXJyb3IgYWwgZWplY3V0YXIgb3BlcmFjaW9uZXM6IHtleGN9IiwKICAgICAgICAgICAgICAgICAgICAgICAgbGV2ZWw9bWVzc2FnZXMuRVJST1IsCiAgICAgICAgICAgICAgICAgICAgKQogICAgICAgIGVsc2U6CiAgICAgICAgICAgIGZvcm0gPSBSZWNhbGNPcHNGb3JtKCkKCiAgICAgICAgY29udGV4dCA9IHsKICAgICAgICAgICAgKipzZWxmLmFkbWluX3NpdGUuZWFjaF9jb250ZXh0KHJlcXVlc3QpLAogICAgICAgICAgICAidGl0bGUiOiAiT3BlcmFjaW9uZXMgZGUgcmVjw6FsY3VsbyIsCiAgICAgICAgICAgICJmb3JtIjogZm9ybSwKICAgICAgICAgICAgIm9wdHMiOiBzZWxmLm1vZGVsLl9tZXRhLAogICAgICAgICAgICAiaGFzX3ZpZXdfcGVybWlzc2lvbiI6IHNlbGYuaGFzX3ZpZXdfcGVybWlzc2lvbihyZXF1ZXN0KSwKICAgICAgICB9CiAgICAgICAgcmV0dXJuIHJlbmRlcigKICAgICAgICAgICAgcmVxdWVzdCwKICAgICAgICAgICAgImFkbWluL3J1bl9yZWNhbGNfb3BzLmh0bWwiLAogICAgICAgICAgICBjb250ZXh0LAogICAgICAgICkKCgpAYWRtaW4ucmVnaXN0ZXIoVW5pZGFkTmVnb2NpbykKY2xhc3MgVW5pZGFkTmVnb2Npb0FkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKCJjb2RlIiwgIm5vbWJyZSIsICJ1bmVfcGdjIiwgImFjdGl2YSIsICJ1cGRhdGVkX2F0IikKICAgIGxpc3RfZmlsdGVyID0gKCJhY3RpdmEiLCkKICAgIHNlYXJjaF9maWVsZHMgPSAoImNvZGUiLCAibm9tYnJlIikKICAgIG9yZGVyaW5nID0gKCJub21icmUiLCkKCgpAYWRtaW4ucmVnaXN0ZXIoRW50aWRhZCkKY2xhc3MgRW50aWRhZEFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKCJjb2RpZ28iLCAibm9tYnJlIiwgIm5pdCIsICJ0aXBvIiwgInVuaWRhZF9uZWdvY2lvIiwgImFjdGl2YSIpCiAgICBsaXN0X2ZpbHRlciA9ICgidGlwbyIsICJhY3RpdmEiLCAidW5pZGFkX25lZ29jaW8iKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgiY29kaWdvIiwgIm5vbWJyZSIsICJuaXQiKQogICAgb3JkZXJpbmcgPSAoIm5vbWJyZSIsKQoKCkBhZG1pbi5yZWdpc3RlcihDb250YWN0bykKY2xhc3MgQ29udGFjdG9BZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgibm9tYnJlIiwgImVudGlkYWQiLCAiZW1haWwiLCAidGVsZWZvbm8iLCAiZXNfcHJpbmNpcGFsIiwgImFjdGl2byIpCiAgICBsaXN0X2ZpbHRlciA9ICgiZXNfcHJpbmNpcGFsIiwgImFjdGl2byIsICJlbnRpZGFkIikKICAgIHNlYXJjaF9maWVsZHMgPSAoIm5vbWJyZSIsICJlbWFpbCIsICJlbnRpZGFkX19jb2RpZ28iLCAiZW50aWRhZF9fbm9tYnJlIikKICAgIG9yZGVyaW5nID0gKCJlbnRpZGFkX19ub21icmUiLCAibm9tYnJlIikKCgpAYWRtaW4ucmVnaXN0ZXIoUHJvZHVjdG8pCmNsYXNzIFByb2R1Y3RvQWRtaW4oYWRtaW4uTW9kZWxBZG1pbik6CiAgICBsaXN0X2Rpc3BsYXkgPSAoImNvZGlnbyIsICJub21icmUiLCAidW5pZGFkX25lZ29jaW8iLCAiYWN0aXZvIikKICAgIGxpc3RfZmlsdGVyID0gKCJhY3Rpdm8iLCAidW5pZGFkX25lZ29jaW8iKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgiY29kaWdvIiwgIm5vbWJyZSIpCiAgICBvcmRlcmluZyA9ICgibm9tYnJlIiwpCgoKQGFkbWluLnJlZ2lzdGVyKFJlbGFjaW9uRW50aWRhZFByb2R1Y3RvKQpjbGFzcyBSZWxhY2lvbkVudGlkYWRQcm9kdWN0b0FkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKCJlbnRpZGFkIiwgInByb2R1Y3RvIiwgImVzdGFkbyIsICJmZWNoYV9pbmljaW8iKQogICAgbGlzdF9maWx0ZXIgPSAoImVzdGFkbyIsICJwcm9kdWN0byIpCiAgICBzZWFyY2hfZmllbGRzID0gKCJlbnRpZGFkX19jb2RpZ28iLCAiZW50aWRhZF9fbm9tYnJlIiwgInByb2R1Y3RvX19jb2RpZ28iKQogICAgb3JkZXJpbmcgPSAoImVudGlkYWRfX25vbWJyZSIsKQoKCkBhZG1pbi5yZWdpc3RlcihEYXRhRGljdGlvbmFyeSkKY2xhc3MgRGF0YURpY3Rpb25hcnlBZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgibW9kdWxvIiwgInRhYmxhIiwgImNhbXBvIiwgImV0aXF1ZXRhIiwgIm9ibGlnYXRvcmlvIikKICAgIGxpc3RfZmlsdGVyID0gKCJtb2R1bG8iLCAib2JsaWdhdG9yaW8iKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgibW9kdWxvIiwgInRhYmxhIiwgImNhbXBvIiwgImV0aXF1ZXRhIikKICAgIG9yZGVyaW5nID0gKCJtb2R1bG8iLCAidGFibGEiLCAiY2FtcG8iKQoKCkBhZG1pbi5yZWdpc3RlcihEYXRhSW1wb3J0QmF0Y2gpCmNsYXNzIERhdGFJbXBvcnRCYXRjaEFkbWluKGFkbWluLk1vZGVsQWRtaW4pOgogICAgbGlzdF9kaXNwbGF5ID0gKAogICAgICAgICJjcmVhdGVkX2F0IiwKICAgICAgICAibW9kdWxvIiwKICAgICAgICAidGlwb19pbXBvcnRhY2lvbiIsCiAgICAgICAgImFyY2hpdm9fbm9tYnJlIiwKICAgICAgICAic3RhdHVzIiwKICAgICAgICAiY3JlYWRvcyIsCiAgICAgICAgImFjdHVhbGl6YWRvcyIsCiAgICAgICAgImVycm9yZXMiLAogICAgICAgICJ1cGxvYWRlZF9ieSIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgibW9kdWxvIiwgInN0YXR1cyIsICJ0aXBvX2ltcG9ydGFjaW9uIikKICAgIHNlYXJjaF9maWVsZHMgPSAoImFyY2hpdm9fbm9tYnJlIiwgInRpcG9faW1wb3J0YWNpb24iLCAibG9nX3RleHRvIikKICAgIG9yZGVyaW5nID0gKCItY3JlYXRlZF9hdCIsKQogICAgcmVhZG9ubHlfZmllbGRzID0gKCJjcmVhdGVkX2F0IiwgInVwZGF0ZWRfYXQiKQ==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/apps.py
PATH_JSON="core/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=6
SIZE_BYTES_UTF8=140
CONTENT_SHA256=bf5ed4638a9bab73339adcd2ba6542beda0edb0ac40103855bc189a89ca75e84
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


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class CoreConfig(AppConfig):
00005|    default_auto_field = "django.db.models.BigAutoField"
00006|    name = "core"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgQ29yZUNvbmZpZyhBcHBDb25maWcpOgogICAgZGVmYXVsdF9hdXRvX2ZpZWxkID0gImRqYW5nby5kYi5tb2RlbHMuQmlnQXV0b0ZpZWxkIgogICAgbmFtZSA9ICJjb3JlIgo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/management/__init__.py
PATH_JSON="core/management/__init__.py"
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
PATH_LITERAL=core/management/commands/__init__.py
PATH_JSON="core/management/commands/__init__.py"
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
PATH_LITERAL=core/management/commands/bootstrap_wcg_demo.py
PATH_JSON="core/management/commands/bootstrap_wcg_demo.py"
FILENAME=bootstrap_wcg_demo.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=49
SIZE_BYTES_UTF8=1727
CONTENT_SHA256=09f2b4be0675e927548061c2132a020d61e9c3b06ec0b53d08f356eaa5794dd9
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
"""Bootstrap demo data on deployed environments (e.g. wcg.lol / Railway).

Usage on production (Railway shell or one-off):
  python manage.py bootstrap_wcg_demo --dir /app/data
  python manage.py bootstrap_wcg_demo --seed-only
  python manage.py bootstrap_wcg_demo --load-only --dir /app/../data
"""

from __future__ import annotations

from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed + carga de datos WCG para demo en producción"

    def add_arguments(self, parser):
        parser.add_argument("--dir", default="", help="Directorio con CSV/XLSX de data/")
        parser.add_argument("--seed-only", action="store_true")
        parser.add_argument("--load-only", action="store_true")

    def handle(self, *args, **options):
        if not options["load_only"]:
            self.stdout.write("→ seed_wcg_demo")
            call_command("seed_wcg_demo")

        if not options["seed_only"]:
            data_dir = options["dir"] or self._guess_data_dir()
            self.stdout.write(f"→ load_wcg_data --dir {data_dir}")
            call_command("load_wcg_data", dir=str(data_dir))

        self.stdout.write(self.style.SUCCESS("Bootstrap WCG demo finalizado."))

    def _guess_data_dir(self) -> Path:
        here = Path(__file__).resolve()
        candidates = [
            here.parents[3] / "demo_data",
            Path("/app/demo_data"),
            here.parents[4] / "data",
            Path("/home/caa/wc/wcg4/data"),
            here.parents[3] / "data" / "wcg",
        ]
        for c in candidates:
            if c.exists():
                return c
        return candidates[0]

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Bootstrap demo data on deployed environments (e.g. wcg.lol / Railway).
00002|
00003|Usage on production (Railway shell or one-off):
00004|  python manage.py bootstrap_wcg_demo --dir /app/data
00005|  python manage.py bootstrap_wcg_demo --seed-only
00006|  python manage.py bootstrap_wcg_demo --load-only --dir /app/../data
00007|"""
00008|
00009|from __future__ import annotations
00010|
00011|from pathlib import Path
00012|
00013|from django.core.management import call_command
00014|from django.core.management.base import BaseCommand
00015|
00016|
00017|class Command(BaseCommand):
00018|    help = "Seed + carga de datos WCG para demo en producción"
00019|
00020|    def add_arguments(self, parser):
00021|        parser.add_argument("--dir", default="", help="Directorio con CSV/XLSX de data/")
00022|        parser.add_argument("--seed-only", action="store_true")
00023|        parser.add_argument("--load-only", action="store_true")
00024|
00025|    def handle(self, *args, **options):
00026|        if not options["load_only"]:
00027|            self.stdout.write("→ seed_wcg_demo")
00028|            call_command("seed_wcg_demo")
00029|
00030|        if not options["seed_only"]:
00031|            data_dir = options["dir"] or self._guess_data_dir()
00032|            self.stdout.write(f"→ load_wcg_data --dir {data_dir}")
00033|            call_command("load_wcg_data", dir=str(data_dir))
00034|
00035|        self.stdout.write(self.style.SUCCESS("Bootstrap WCG demo finalizado."))
00036|
00037|    def _guess_data_dir(self) -> Path:
00038|        here = Path(__file__).resolve()
00039|        candidates = [
00040|            here.parents[3] / "demo_data",
00041|            Path("/app/demo_data"),
00042|            here.parents[4] / "data",
00043|            Path("/home/caa/wc/wcg4/data"),
00044|            here.parents[3] / "data" / "wcg",
00045|        ]
00046|        for c in candidates:
00047|            if c.exists():
00048|                return c
00049|        return candidates[0]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiQm9vdHN0cmFwIGRlbW8gZGF0YSBvbiBkZXBsb3llZCBlbnZpcm9ubWVudHMgKGUuZy4gd2NnLmxvbCAvIFJhaWx3YXkpLgoKVXNhZ2Ugb24gcHJvZHVjdGlvbiAoUmFpbHdheSBzaGVsbCBvciBvbmUtb2ZmKToKICBweXRob24gbWFuYWdlLnB5IGJvb3RzdHJhcF93Y2dfZGVtbyAtLWRpciAvYXBwL2RhdGEKICBweXRob24gbWFuYWdlLnB5IGJvb3RzdHJhcF93Y2dfZGVtbyAtLXNlZWQtb25seQogIHB5dGhvbiBtYW5hZ2UucHkgYm9vdHN0cmFwX3djZ19kZW1vIC0tbG9hZC1vbmx5IC0tZGlyIC9hcHAvLi4vZGF0YQoiIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmZyb20gcGF0aGxpYiBpbXBvcnQgUGF0aAoKZnJvbSBkamFuZ28uY29yZS5tYW5hZ2VtZW50IGltcG9ydCBjYWxsX2NvbW1hbmQKZnJvbSBkamFuZ28uY29yZS5tYW5hZ2VtZW50LmJhc2UgaW1wb3J0IEJhc2VDb21tYW5kCgoKY2xhc3MgQ29tbWFuZChCYXNlQ29tbWFuZCk6CiAgICBoZWxwID0gIlNlZWQgKyBjYXJnYSBkZSBkYXRvcyBXQ0cgcGFyYSBkZW1vIGVuIHByb2R1Y2Npw7NuIgoKICAgIGRlZiBhZGRfYXJndW1lbnRzKHNlbGYsIHBhcnNlcik6CiAgICAgICAgcGFyc2VyLmFkZF9hcmd1bWVudCgiLS1kaXIiLCBkZWZhdWx0PSIiLCBoZWxwPSJEaXJlY3RvcmlvIGNvbiBDU1YvWExTWCBkZSBkYXRhLyIpCiAgICAgICAgcGFyc2VyLmFkZF9hcmd1bWVudCgiLS1zZWVkLW9ubHkiLCBhY3Rpb249InN0b3JlX3RydWUiKQogICAgICAgIHBhcnNlci5hZGRfYXJndW1lbnQoIi0tbG9hZC1vbmx5IiwgYWN0aW9uPSJzdG9yZV90cnVlIikKCiAgICBkZWYgaGFuZGxlKHNlbGYsICphcmdzLCAqKm9wdGlvbnMpOgogICAgICAgIGlmIG5vdCBvcHRpb25zWyJsb2FkX29ubHkiXToKICAgICAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoIuKGkiBzZWVkX3djZ19kZW1vIikKICAgICAgICAgICAgY2FsbF9jb21tYW5kKCJzZWVkX3djZ19kZW1vIikKCiAgICAgICAgaWYgbm90IG9wdGlvbnNbInNlZWRfb25seSJdOgogICAgICAgICAgICBkYXRhX2RpciA9IG9wdGlvbnNbImRpciJdIG9yIHNlbGYuX2d1ZXNzX2RhdGFfZGlyKCkKICAgICAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoZiLihpIgbG9hZF93Y2dfZGF0YSAtLWRpciB7ZGF0YV9kaXJ9IikKICAgICAgICAgICAgY2FsbF9jb21tYW5kKCJsb2FkX3djZ19kYXRhIiwgZGlyPXN0cihkYXRhX2RpcikpCgogICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKHNlbGYuc3R5bGUuU1VDQ0VTUygiQm9vdHN0cmFwIFdDRyBkZW1vIGZpbmFsaXphZG8uIikpCgogICAgZGVmIF9ndWVzc19kYXRhX2RpcihzZWxmKSAtPiBQYXRoOgogICAgICAgIGhlcmUgPSBQYXRoKF9fZmlsZV9fKS5yZXNvbHZlKCkKICAgICAgICBjYW5kaWRhdGVzID0gWwogICAgICAgICAgICBoZXJlLnBhcmVudHNbM10gLyAiZGVtb19kYXRhIiwKICAgICAgICAgICAgUGF0aCgiL2FwcC9kZW1vX2RhdGEiKSwKICAgICAgICAgICAgaGVyZS5wYXJlbnRzWzRdIC8gImRhdGEiLAogICAgICAgICAgICBQYXRoKCIvaG9tZS9jYWEvd2Mvd2NnNC9kYXRhIiksCiAgICAgICAgICAgIGhlcmUucGFyZW50c1szXSAvICJkYXRhIiAvICJ3Y2ciLAogICAgICAgIF0KICAgICAgICBmb3IgYyBpbiBjYW5kaWRhdGVzOgogICAgICAgICAgICBpZiBjLmV4aXN0cygpOgogICAgICAgICAgICAgICAgcmV0dXJuIGMKICAgICAgICByZXR1cm4gY2FuZGlkYXRlc1swXQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=core/management/commands/import_wcg_data.py
PATH_JSON="core/management/commands/import_wcg_data.py"
FILENAME=import_wcg_data.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=57
SIZE_BYTES_UTF8=2041
CONTENT_SHA256=bd6d107604a22e742a8f3810ece838b538dd8a479d90c3ec4d4399c3a950bac0
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
Importa archivos reales WCG desde data/wcg/ (si existen).
Ejecutar: python manage.py import_wcg_data
"""

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand

from core.wcg_paths import (
    CRM_INFO_CLIENTES,
    PGO_ANALISIS_TI,
    PGO_ARCHIVOS,
    PGO_TICKETS_CONTROL,
    RISK_LEASING_DB,
    resolve_data_file,
)
from crm import services as crm_services
from pgo import services as pgo_services
from pgo.periodo import recalculate_pgo_periodos
from risk import services as risk_services

User = get_user_model()

IMPORTERS = [
    (CRM_INFO_CLIENTES, crm_services.import_infoclientes_wcg),
    (RISK_LEASING_DB, risk_services.import_leasing_database),
    (PGO_ARCHIVOS, pgo_services.import_archivos_catalogo),
    (PGO_TICKETS_CONTROL, pgo_services.import_tickets),
    (PGO_ANALISIS_TI, pgo_services.import_tickets),
]


class Command(BaseCommand):
    help = "Importa archivos de datos WCG desde data/wcg/"

    def handle(self, *args, **options):
        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if not user:
            self.stderr.write("No hay usuario en BD. Cree uno primero.")
            return
        for filename, importer in IMPORTERS:
            path = resolve_data_file(filename)
            if not path:
                self.stdout.write(self.style.WARNING(f"SKIP (no existe): {filename}"))
                continue
            content = path.read_bytes()
            upload = SimpleUploadedFile(path.name, content)
            batch = importer(user, upload)
            self.stdout.write(
                f"{filename}: {batch.status} — "
                f"creados={batch.creados} actualizados={batch.actualizados} errores={batch.errores}"
            )
            if batch.log_texto:
                self.stdout.write(batch.log_texto[:500])
        recalculate_pgo_periodos()
        self.stdout.write(self.style.SUCCESS("import_wcg_data finalizado."))

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Importa archivos reales WCG desde data/wcg/ (si existen).
00003|Ejecutar: python manage.py import_wcg_data
00004|"""
00005|
00006|from django.contrib.auth import get_user_model
00007|from django.core.files.uploadedfile import SimpleUploadedFile
00008|from django.core.management.base import BaseCommand
00009|
00010|from core.wcg_paths import (
00011|    CRM_INFO_CLIENTES,
00012|    PGO_ANALISIS_TI,
00013|    PGO_ARCHIVOS,
00014|    PGO_TICKETS_CONTROL,
00015|    RISK_LEASING_DB,
00016|    resolve_data_file,
00017|)
00018|from crm import services as crm_services
00019|from pgo import services as pgo_services
00020|from pgo.periodo import recalculate_pgo_periodos
00021|from risk import services as risk_services
00022|
00023|User = get_user_model()
00024|
00025|IMPORTERS = [
00026|    (CRM_INFO_CLIENTES, crm_services.import_infoclientes_wcg),
00027|    (RISK_LEASING_DB, risk_services.import_leasing_database),
00028|    (PGO_ARCHIVOS, pgo_services.import_archivos_catalogo),
00029|    (PGO_TICKETS_CONTROL, pgo_services.import_tickets),
00030|    (PGO_ANALISIS_TI, pgo_services.import_tickets),
00031|]
00032|
00033|
00034|class Command(BaseCommand):
00035|    help = "Importa archivos de datos WCG desde data/wcg/"
00036|
00037|    def handle(self, *args, **options):
00038|        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
00039|        if not user:
00040|            self.stderr.write("No hay usuario en BD. Cree uno primero.")
00041|            return
00042|        for filename, importer in IMPORTERS:
00043|            path = resolve_data_file(filename)
00044|            if not path:
00045|                self.stdout.write(self.style.WARNING(f"SKIP (no existe): {filename}"))
00046|                continue
00047|            content = path.read_bytes()
00048|            upload = SimpleUploadedFile(path.name, content)
00049|            batch = importer(user, upload)
00050|            self.stdout.write(
00051|                f"{filename}: {batch.status} — "
00052|                f"creados={batch.creados} actualizados={batch.actualizados} errores={batch.errores}"
00053|            )
00054|            if batch.log_texto:
00055|                self.stdout.write(batch.log_texto[:500])
00056|        recalculate_pgo_periodos()
00057|        self.stdout.write(self.style.SUCCESS("import_wcg_data finalizado."))

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiCkltcG9ydGEgYXJjaGl2b3MgcmVhbGVzIFdDRyBkZXNkZSBkYXRhL3djZy8gKHNpIGV4aXN0ZW4pLgpFamVjdXRhcjogcHl0aG9uIG1hbmFnZS5weSBpbXBvcnRfd2NnX2RhdGEKIiIiCgpmcm9tIGRqYW5nby5jb250cmliLmF1dGggaW1wb3J0IGdldF91c2VyX21vZGVsCmZyb20gZGphbmdvLmNvcmUuZmlsZXMudXBsb2FkZWRmaWxlIGltcG9ydCBTaW1wbGVVcGxvYWRlZEZpbGUKZnJvbSBkamFuZ28uY29yZS5tYW5hZ2VtZW50LmJhc2UgaW1wb3J0IEJhc2VDb21tYW5kCgpmcm9tIGNvcmUud2NnX3BhdGhzIGltcG9ydCAoCiAgICBDUk1fSU5GT19DTElFTlRFUywKICAgIFBHT19BTkFMSVNJU19USSwKICAgIFBHT19BUkNISVZPUywKICAgIFBHT19USUNLRVRTX0NPTlRST0wsCiAgICBSSVNLX0xFQVNJTkdfREIsCiAgICByZXNvbHZlX2RhdGFfZmlsZSwKKQpmcm9tIGNybSBpbXBvcnQgc2VydmljZXMgYXMgY3JtX3NlcnZpY2VzCmZyb20gcGdvIGltcG9ydCBzZXJ2aWNlcyBhcyBwZ29fc2VydmljZXMKZnJvbSBwZ28ucGVyaW9kbyBpbXBvcnQgcmVjYWxjdWxhdGVfcGdvX3BlcmlvZG9zCmZyb20gcmlzayBpbXBvcnQgc2VydmljZXMgYXMgcmlza19zZXJ2aWNlcwoKVXNlciA9IGdldF91c2VyX21vZGVsKCkKCklNUE9SVEVSUyA9IFsKICAgIChDUk1fSU5GT19DTElFTlRFUywgY3JtX3NlcnZpY2VzLmltcG9ydF9pbmZvY2xpZW50ZXNfd2NnKSwKICAgIChSSVNLX0xFQVNJTkdfREIsIHJpc2tfc2VydmljZXMuaW1wb3J0X2xlYXNpbmdfZGF0YWJhc2UpLAogICAgKFBHT19BUkNISVZPUywgcGdvX3NlcnZpY2VzLmltcG9ydF9hcmNoaXZvc19jYXRhbG9nbyksCiAgICAoUEdPX1RJQ0tFVFNfQ09OVFJPTCwgcGdvX3NlcnZpY2VzLmltcG9ydF90aWNrZXRzKSwKICAgIChQR09fQU5BTElTSVNfVEksIHBnb19zZXJ2aWNlcy5pbXBvcnRfdGlja2V0cyksCl0KCgpjbGFzcyBDb21tYW5kKEJhc2VDb21tYW5kKToKICAgIGhlbHAgPSAiSW1wb3J0YSBhcmNoaXZvcyBkZSBkYXRvcyBXQ0cgZGVzZGUgZGF0YS93Y2cvIgoKICAgIGRlZiBoYW5kbGUoc2VsZiwgKmFyZ3MsICoqb3B0aW9ucyk6CiAgICAgICAgdXNlciA9IFVzZXIub2JqZWN0cy5maWx0ZXIoaXNfc3VwZXJ1c2VyPVRydWUpLmZpcnN0KCkgb3IgVXNlci5vYmplY3RzLmZpcnN0KCkKICAgICAgICBpZiBub3QgdXNlcjoKICAgICAgICAgICAgc2VsZi5zdGRlcnIud3JpdGUoIk5vIGhheSB1c3VhcmlvIGVuIEJELiBDcmVlIHVubyBwcmltZXJvLiIpCiAgICAgICAgICAgIHJldHVybgogICAgICAgIGZvciBmaWxlbmFtZSwgaW1wb3J0ZXIgaW4gSU1QT1JURVJTOgogICAgICAgICAgICBwYXRoID0gcmVzb2x2ZV9kYXRhX2ZpbGUoZmlsZW5hbWUpCiAgICAgICAgICAgIGlmIG5vdCBwYXRoOgogICAgICAgICAgICAgICAgc2VsZi5zdGRvdXQud3JpdGUoc2VsZi5zdHlsZS5XQVJOSU5HKGYiU0tJUCAobm8gZXhpc3RlKToge2ZpbGVuYW1lfSIpKQogICAgICAgICAgICAgICAgY29udGludWUKICAgICAgICAgICAgY29udGVudCA9IHBhdGgucmVhZF9ieXRlcygpCiAgICAgICAgICAgIHVwbG9hZCA9IFNpbXBsZVVwbG9hZGVkRmlsZShwYXRoLm5hbWUsIGNvbnRlbnQpCiAgICAgICAgICAgIGJhdGNoID0gaW1wb3J0ZXIodXNlciwgdXBsb2FkKQogICAgICAgICAgICBzZWxmLnN0ZG91dC53cml0ZSgKICAgICAgICAgICAgICAgIGYie2ZpbGVuYW1lfToge2JhdGNoLnN0YXR1c30g4oCUICIKICAgICAgICAgICAgICAgIGYiY3JlYWRvcz17YmF0Y2guY3JlYWRvc30gYWN0dWFsaXphZG9zPXtiYXRjaC5hY3R1YWxpemFkb3N9IGVycm9yZXM9e2JhdGNoLmVycm9yZXN9IgogICAgICAgICAgICApCiAgICAgICAgICAgIGlmIGJhdGNoLmxvZ190ZXh0bzoKICAgICAgICAgICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKGJhdGNoLmxvZ190ZXh0b1s6NTAwXSkKICAgICAgICByZWNhbGN1bGF0ZV9wZ29fcGVyaW9kb3MoKQogICAgICAgIHNlbGYuc3Rkb3V0LndyaXRlKHNlbGYuc3R5bGUuU1VDQ0VTUygiaW1wb3J0X3djZ19kYXRhIGZpbmFsaXphZG8uIikpCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
