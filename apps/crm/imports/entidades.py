"""Importador CRM: entidades y contactos desde CSV/XLSX."""

from __future__ import annotations

import pandas as pd

from apps.core.imports.base import run_import_batch
from apps.core.imports.columns import normalize_columns, pick, require_any
from apps.core.imports.entities import upsert_contacto_from_row, upsert_entidad
from apps.core.models import Entidad


MODULO = "crm"
TIPO = "entidades_clientes"


def _preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)
    require_any(
        df,
        [
            ["nit", "nit_cliente", "codigo", "codigo_cliente"],
            ["nombre", "razon_social", "cliente", "nombre_cliente"],
        ],
    )
    return df


def import_entidades_clientes(user, uploaded_file):
    uploaded_file.seek(0)

    def handler(row: pd.Series, errors: list[str], batch=None):
        nombre = pick(row, "nombre", "razon_social", "cliente", "nombre_cliente")
        nit = pick(row, "nit", "nit_cliente", "codigo", "codigo_cliente")
        if not nombre and not nit:
            errors.append("Falta nombre o NIT.")
            return None
        if not nombre:
            nombre = nit
        tipo_raw = pick(row, "tipo", "tipo_entidad", "tipo_cliente").lower()
        tipo = Entidad.TIPO_CLIENTE
        if "prospect" in tipo_raw:
            tipo = Entidad.TIPO_PROSPECTO
        elif "proveedor" in tipo_raw:
            tipo = Entidad.TIPO_PROVEEDOR
        try:
            entidad, created_e, updated_e = upsert_entidad(
                nit=nit,
                nombre=nombre,
                defaults={
                    "tipo_entidad": tipo,
                    "telefono": pick(row, "telefono", "tel"),
                    "email": pick(row, "email", "correo"),
                    "ciudad": pick(row, "ciudad"),
                    "notas": pick(row, "notas", "observaciones"),
                    "origen": "importacion_crm",
                },
            )
        except ValueError as exc:
            errors.append(str(exc))
            return None
        _, created_c = upsert_contacto_from_row(entidad, row)
        if created_e or created_c:
            return True, False
        if updated_e:
            return False, True
        return False, False

    return run_import_batch(
        user=user,
        modulo=MODULO,
        tipo_importacion=TIPO,
        uploaded_file=uploaded_file,
        preprocess=_preprocess,
        row_handler=handler,
    )
