"""
Importadores PGO.

Archivos referencia:
  - `pgo datos - Archivos para PGO.csv` (catálogo — informativo, no crea tickets)
  - `pgo datos - control de tickets marzo abril y mayo 2026 para PGO.xlsx`
  - `pgo ejemplo del analisis - PGO - TI Q22026.xlsx`

Columnas mínimas tickets (alias):
  - codigo: Ticket, ID, Folio, No_Ticket
  - titulo: Titulo, Asunto, Descripcion_Corta
  - estado, prioridad, asignado, fecha_apertura, fecha_cierre, unidad_negocio, sla_horas

Clave natural: `codigo`
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.services.column_map import normalize_columns, pick, pick_int, require_any
from core.services.import_base import read_dataframe, run_import_batch
from core.wcg_models import DataImportBatch, Entidad, UnidadNegocio
from crm.services import _resolve_unidad, _slug_codigo
from pgo.models import Ticket

User = get_user_model()


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


def _map_estado(raw: str) -> str:
    s = raw.upper()
    if "CERR" in s or "CLOSE" in s or "RESUEL" in s:
        return Ticket.ESTADO_CERRADO
    if "PROCES" in s or "PROGRESS" in s:
        return Ticket.ESTADO_EN_PROCESO
    return Ticket.ESTADO_ABIERTO


def _map_prioridad(raw: str) -> str:
    s = raw.upper()
    if "ALT" in s or "HIGH" in s:
        return Ticket.PRIORIDAD_ALTA
    if "BAJ" in s or "LOW" in s:
        return Ticket.PRIORIDAD_BAJA
    return Ticket.PRIORIDAD_MEDIA


def _read_tickets_dataframe(uploaded_file) -> pd.DataFrame:
    from core.services.import_base import read_dataframe

    return normalize_columns(read_dataframe(uploaded_file))


def import_tickets(user, uploaded_file) -> DataImportBatch:
    df = _read_tickets_dataframe(uploaded_file)
    require_any(df, [["codigo", "ticket", "id", "folio", "no_ticket"], ["titulo", "asunto", "descripcion"]])

    def handler(row: pd.Series, errors: list[str]):
        codigo = pick(row, "codigo", "ticket", "id", "folio", "no_ticket", "id_ticket")
        titulo = pick(row, "titulo", "asunto", "descripcion", "descripcion_corta", "tema")
        if not codigo or not titulo:
            errors.append("codigo y titulo obligatorios")
            return None
        entidad = None
        ent_code = pick(row, "entidad_codigo", "cliente_codigo", "nit")
        if ent_code:
            entidad = Entidad.objects.filter(codigo__iexact=_slug_codigo(ent_code)).first()
        unidad = _resolve_unidad(pick(row, "unidad_negocio", "unidad", "departamento", "area") or "TI")
        asignado = None
        username = pick(row, "asignado", "asignado_a", "responsable", "tecnico", "agente")
        if username:
            asignado = User.objects.filter(username__iexact=username.split()[0]).first()
        fecha_apertura = _parse_dt(pick(row, "fecha_apertura", "fecha_creacion", "creado", "apertura")) or timezone.now()
        fecha_cierre = _parse_dt(pick(row, "fecha_cierre", "cerrado", "fecha_resolucion"))
        estado = _map_estado(pick(row, "estado", "status", "estado_ticket"))
        if fecha_cierre and estado != Ticket.ESTADO_CERRADO:
            estado = Ticket.ESTADO_CERRADO
        _, created = Ticket.objects.update_or_create(
            codigo=str(codigo),
            defaults={
                "titulo": titulo[:200],
                "descripcion": pick(row, "descripcion", "detalle", "notas"),
                "entidad": entidad,
                "unidad_negocio": unidad,
                "estado": estado,
                "prioridad": _map_prioridad(pick(row, "prioridad", "prioridad_ticket")),
                "asignado_a": asignado,
                "fecha_apertura": fecha_apertura,
                "fecha_cierre": fecha_cierre,
                "sla_horas": pick_int(row, "sla_horas", "sla", default=48),
            },
        )
        return created, not created

    uploaded_file.seek(0)
    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_PGO,
        tipo_importacion="tickets",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_archivos_catalogo(user, uploaded_file) -> DataImportBatch:
    """
    Catálogo de archivos PGO — solo registra lote (sin crear tickets).
  TODO negocio: persistir catálogo si se requiere trazabilidad documental.
    """
    from core.wcg_models import DataImportBatch as Batch

    df = normalize_columns(read_dataframe(uploaded_file))
    batch = Batch.objects.create(
        modulo=Batch.MODULO_PGO,
        tipo_importacion="archivos_catalogo",
        archivo_nombre=uploaded_file.name,
        uploaded_by=user,
        filas_leidas=len(df),
        status=Batch.STATUS_OK,
        log_texto=f"Catálogo leído ({len(df)} filas). Sin carga a tickets.",
    )
    return batch
