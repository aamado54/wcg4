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
