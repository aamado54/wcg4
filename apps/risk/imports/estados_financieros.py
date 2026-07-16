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
