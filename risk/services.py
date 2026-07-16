"""
Importadores Risk / Balón.

Archivo referencia leasing:
  `balon datos - Ejemplo de datos Riesgo al 31-mayo para una operacion - Base de datos Leasing.xlsx`

Columnas mínimas (alias):
  - cliente / nombre + nit (crea Entidad si no existe)
  - operacion / referencia_operacion / contrato
  - fecha_snapshot / fecha_corte / al_31_mayo
  - saldo, dias_mora / dias_atraso, monto_exigible / exigible

Clave natural snapshot: (entidad, referencia_operacion, fecha_snapshot)
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

import pandas as pd

from core.services.column_map import normalize_columns, pick, pick_decimal, pick_int, require_any
from core.services.import_base import read_dataframe, run_import_batch
from core.wcg_models import DataImportBatch, Entidad, Producto, UnidadNegocio
from crm.services import _entidad_codigo_from_row, _resolve_unidad, _slug_codigo
from risk.models import (
    EstadoFinanciero,
    PagoRealizado,
    ProgramacionPago,
    RiskOperationSnapshot,
)


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


def _ensure_entidad_from_row(row: pd.Series, errors: list[str]) -> Entidad | None:
    nombre = pick(row, "cliente", "nombre", "razon_social", "nombre_cliente")
    nit = pick(row, "nit", "nit_cliente")
    codigo = pick(row, "entidad_codigo", "codigo_cliente") or _entidad_codigo_from_row(row)
    if not nombre and not codigo:
        errors.append("falta cliente o identificador")
        return None
    if not nombre:
        nombre = codigo
    unidad = _resolve_unidad(pick(row, "unidad", "une", "unidad_negocio") or "LEASING")
    entidad, _ = Entidad.objects.update_or_create(
        codigo=codigo,
        defaults={"nombre": nombre, "nit": nit, "unidad_negocio": unidad, "activa": True},
    )
    return entidad


def _nivel_from_mora(dias: int) -> str:
    if dias >= 90:
        return RiskOperationSnapshot.NIVEL_CRITICO
    if dias >= 60:
        return RiskOperationSnapshot.NIVEL_ALTO
    if dias >= 30:
        return RiskOperationSnapshot.NIVEL_MEDIO
    return RiskOperationSnapshot.NIVEL_BAJO


def import_leasing_database(user, uploaded_file) -> DataImportBatch:
    from core.services.import_base import read_dataframe

    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(
        df,
        [
            ["cliente", "nombre", "razon_social"],
            ["operacion", "referencia_operacion", "contrato", "no_operacion"],
        ],
    )
    uploaded_file.seek(0)

    def handler(row: pd.Series, errors: list[str]):
        entidad = _ensure_entidad_from_row(row, errors)
        if not entidad:
            return None
        referencia = pick(row, "operacion", "referencia_operacion", "contrato", "no_operacion", "no_contrato")
        if not referencia:
            errors.append("falta referencia de operación")
            return None
        fecha_raw = pick(row, "fecha_snapshot", "fecha_corte", "al_31_mayo", "fecha", "corte")
        fecha = _parse_date(fecha_raw) or date(2026, 5, 31)
        dias = pick_int(row, "dias_mora", "dias_atraso", "dias_de_mora", "mora_dias")
        saldo = pick_decimal(row, "saldo", "saldo_total", "saldo_operacion")
        exigible = pick_decimal(row, "monto_exigible", "exigible", "monto_vencido", "vencido")
        if exigible == 0 and saldo > 0 and dias > 0:
            # TODO negocio: regla oficial de monto exigible vs saldo total
            exigible = saldo
        nivel = pick(row, "nivel_riesgo", "categoria_riesgo").upper() or _nivel_from_mora(dias)
        if nivel not in dict(RiskOperationSnapshot.NIVEL_CHOICES):
            nivel = _nivel_from_mora(dias)
        alerta_raw = pick(row, "alerta", "en_alerta")
        alerta = dias >= 30 or alerta_raw.lower() in ("1", "si", "sí", "true", "yes")
        prod_code = pick(row, "producto", "producto_codigo") or "LEASING"
        producto, _ = Producto.objects.get_or_create(
            codigo=_slug_codigo(prod_code),
            defaults={"nombre": "Leasing", "activo": True},
        )
        _, created = RiskOperationSnapshot.objects.update_or_create(
            entidad=entidad,
            referencia_operacion=referencia,
            fecha_snapshot=fecha,
            defaults={
                "producto": producto,
                "nivel_riesgo": nivel,
                "dias_mora": dias,
                "saldo": saldo,
                "monto_exigible": exigible,
                "alerta": alerta,
                "detalle": pick(row, "detalle", "observaciones", "notas"),
            },
        )
        # Estado financiero agregado por período del snapshot
        periodo = fecha.strftime("%Y-%m")
        EstadoFinanciero.objects.update_or_create(
            entidad=entidad,
            periodo=periodo,
            defaults={
                "saldo_total": saldo,
                "mora_dias": dias,
                "exposicion": saldo,
            },
        )
        return created, not created

    uploaded_file.seek(0)
    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_RISK,
        tipo_importacion="leasing_database",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_estados_financieros(user, uploaded_file) -> DataImportBatch:
    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(df, [["entidad_codigo", "nit", "cliente"], ["periodo"]])

    def handler(row: pd.Series, errors: list[str]):
        entidad = _ensure_entidad_from_row(row, errors)
        if not entidad:
            return None
        periodo = pick(row, "periodo", "anio_mes", "mes")
        if not periodo:
            errors.append("periodo obligatorio")
            return None
        periodo = periodo.replace("/", "-")[:7]
        _, created = EstadoFinanciero.objects.update_or_create(
            entidad=entidad,
            periodo=periodo,
            defaults={
                "saldo_total": pick_decimal(row, "saldo_total", "saldo"),
                "mora_dias": pick_int(row, "mora_dias", "dias_mora"),
                "exposicion": pick_decimal(row, "exposicion"),
                "notas": pick(row, "notas"),
            },
        )
        return created, not created

    uploaded_file.seek(0)
    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_RISK,
        tipo_importacion="estados_financieros",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_programacion_pagos(user, uploaded_file) -> DataImportBatch:
    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(df, [["referencia", "operacion"], ["fecha_programada", "fecha_pago_programada"], ["monto"]])

    def handler(row: pd.Series, errors: list[str]):
        entidad = _ensure_entidad_from_row(row, errors)
        if not entidad:
            return None
        referencia = pick(row, "referencia", "operacion", "cuota")
        fecha = _parse_date(pick(row, "fecha_programada", "fecha_vencimiento"))
        if not referencia or not fecha:
            errors.append("referencia y fecha_programada obligatorias")
            return None
        _, created = ProgramacionPago.objects.update_or_create(
            entidad=entidad,
            referencia=referencia,
            defaults={
                "fecha_programada": fecha,
                "monto": pick_decimal(row, "monto"),
                "moneda": pick(row, "moneda") or "GTQ",
            },
        )
        return created, not created

    uploaded_file.seek(0)
    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_RISK,
        tipo_importacion="programacion_pagos",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_pagos_realizados(user, uploaded_file) -> DataImportBatch:
    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(df, [["referencia", "operacion"], ["fecha_pago"], ["monto"]])

    def handler(row: pd.Series, errors: list[str]):
        entidad = _ensure_entidad_from_row(row, errors)
        if not entidad:
            return None
        referencia = pick(row, "referencia", "operacion", "cuota")
        fecha = _parse_date(pick(row, "fecha_pago"))
        if not referencia or not fecha:
            errors.append("referencia y fecha_pago obligatorias")
            return None
        _, created = PagoRealizado.objects.update_or_create(
            entidad=entidad,
            referencia=referencia,
            defaults={
                "fecha_pago": fecha,
                "monto": pick_decimal(row, "monto"),
                "moneda": pick(row, "moneda") or "GTQ",
            },
        )
        return created, not created

    uploaded_file.seek(0)
    return run_import_batch(
        user=user,
        modulo=DataImportBatch.MODULO_RISK,
        tipo_importacion="pagos_realizados",
        uploaded_file=uploaded_file,
        required_columns=[],
        row_handler=handler,
    )


def import_snapshots(user, uploaded_file) -> DataImportBatch:
    """CSV genérico de snapshots — mismo mapeo que leasing en formato plano."""
    return import_leasing_database(user, uploaded_file)
