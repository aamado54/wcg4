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


def _parse_dt(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, datetime):
        dt = value
        return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
    if hasattr(value, "to_pydatetime"):
        try:
            dt = value.to_pydatetime()
            return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
        except Exception:
            pass
    text = str(value).strip()
    if not text or text.lower() in ("nan", "nat", "none"):
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y %H:%M", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            dt = datetime.strptime(text[:19], fmt)
            return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
        except ValueError:
            continue
    try:
        dt = pd.to_datetime(text).to_pydatetime()
        return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
    except Exception:
        return None


def _map_estado(raw: str) -> str:
    s = (raw or "").upper()
    if any(k in s for k in ("CERR", "CLOSE", "RESUEL", "RECHAZ", "CONFIGUR", "NO EXISTE")):
        return Ticket.ESTADO_CERRADO
    if any(k in s for k in ("PROCES", "PROGRESS", "PRUEBA", "ESPERA", "PROVEEDOR", "CURSO")):
        return Ticket.ESTADO_EN_PROCESO
    return Ticket.ESTADO_ABIERTO


def _map_prioridad(raw: str) -> str:
    s = (raw or "").upper()
    if "ALT" in s or "HIGH" in s:
        return Ticket.PRIORIDAD_ALTA
    if "BAJ" in s or "LOW" in s:
        return Ticket.PRIORIDAD_BAJA
    return Ticket.PRIORIDAD_MEDIA


def _read_tickets_dataframe(uploaded_file) -> pd.DataFrame:
    name = (uploaded_file.name or "").lower()
    if name.endswith((".xlsx", ".xls")):
        return normalize_columns(read_dataframe(uploaded_file, all_data_sheets=True))
    return normalize_columns(read_dataframe(uploaded_file))


def import_tickets(user, uploaded_file) -> DataImportBatch:
    df = _read_tickets_dataframe(uploaded_file)
    require_any(
        df,
        [
            ["codigo", "ticket", "id", "folio", "no_ticket"],
            ["titulo", "asunto", "descripcion", "tema"],
        ],
    )

    def handler(row: pd.Series, errors: list[str]):
        codigo = pick(row, "codigo", "ticket", "id", "folio", "no_ticket", "id_ticket")
        titulo = pick(row, "titulo", "asunto", "descripcion", "descripcion_corta", "tema")
        if not codigo or not titulo:
            errors.append("codigo y titulo obligatorios")
            return None
        # Evitar IDs float "368.0"
        if codigo.endswith(".0") and codigo[:-2].isdigit():
            codigo = codigo[:-2]
        entidad = None
        ent_code = pick(row, "entidad_codigo", "cliente_codigo", "nit")
        if ent_code:
            entidad = Entidad.objects.filter(codigo__iexact=_slug_codigo(ent_code)).first()
        unidad_raw = pick(row, "unidad_negocio", "unidad", "departamento", "area", "sistema") or "TI"
        unidad = _resolve_unidad(unidad_raw)
        if unidad is None:
            # Departamentos internos → TI por defecto
            unidad, _ = UnidadNegocio.objects.get_or_create(
                code="TI",
                defaults={"nombre": "Tecnología / TI", "activa": True},
            )
        asignado = None
        username = pick(row, "asignado", "asignado_a", "responsable", "tecnico", "agente", "estado2")
        if username and username.lower() not in ("sin asignarse", "sin asignar", "none", "nan"):
            first = username.split()[0]
            asignado = User.objects.filter(username__iexact=first).first()
            if not asignado:
                asignado = User.objects.filter(first_name__icontains=first).first()
        fecha_apertura = (
            _parse_dt(pick(row, "fecha_apertura", "fecha_creacion", "creado", "apertura", "fecha_registro"))
            or timezone.now()
        )
        fecha_cierre = _parse_dt(pick(row, "fecha_cierre", "cerrado", "fecha_resolucion"))
        estado = _map_estado(pick(row, "estado", "status", "estado_ticket"))
        if fecha_cierre and estado == Ticket.ESTADO_ABIERTO:
            # Rechazado/Resuelto con fecha de cierre → cerrado
            if any(k in pick(row, "estado").upper() for k in ("RECHAZ", "RESUEL", "CERR")):
                estado = Ticket.ESTADO_CERRADO
        duracion = pick(row, "duracion")
        sla = pick_int(row, "sla_horas", "sla", default=48)
        if duracion:
            try:
                # Duración en horas del archivo helpdesk; SLA = max(48, ceil(duracion*1.2))
                d = float(str(duracion).replace(",", "."))
                if d > 0:
                    sla = max(sla, int(d) + 8)
            except ValueError:
                pass
        descripcion = pick(row, "descripcion", "detalle", "notas", "solucion")
        solicitante = pick(row, "usuario_solicita", "solicitante")
        if solicitante:
            descripcion = f"Solicita: {solicitante}\n{descripcion}".strip()
        _, created = Ticket.objects.update_or_create(
            codigo=str(codigo),
            defaults={
                "titulo": titulo[:200],
                "descripcion": descripcion,
                "entidad": entidad,
                "unidad_negocio": unidad,
                "estado": estado,
                "prioridad": _map_prioridad(pick(row, "prioridad", "prioridad_ticket")),
                "asignado_a": asignado,
                "fecha_apertura": fecha_apertura,
                "fecha_cierre": fecha_cierre,
                "sla_horas": sla,
            },
        )
        return created, not created

    uploaded_file.seek(0)

    # run_import_batch re-lee el archivo; para multi-hoja usamos handler sobre df ya leído
    batch = DataImportBatch.objects.create(
        modulo=DataImportBatch.MODULO_PGO,
        tipo_importacion="tickets",
        archivo_nombre=uploaded_file.name,
        uploaded_by=user,
        status=DataImportBatch.STATUS_PENDING,
        filas_leidas=len(df),
    )
    logs: list[str] = []
    for idx, row in df.iterrows():
        row_errors: list[str] = []
        try:
            result = handler(row, row_errors)
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
    batch.log_texto = "\n".join(logs)[:8000]
    batch.save()
    return batch


def import_archivos_catalogo(user, uploaded_file) -> DataImportBatch:
    """
    Catálogo de archivos PGO — solo registra lote (sin crear tickets).
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
