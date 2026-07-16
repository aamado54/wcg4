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
