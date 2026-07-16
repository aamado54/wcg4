"""
Importadores CRM ajustados a archivos reales WCG.

Archivo referencia: `crm datos - InfoClientesWCG para CRM.csv`
Columnas mínimas (cualquier alias listado):
  - codigo: Codigo, CodigoCliente, ID_Cliente (o NIT como fallback)
  - nombre: Nombre, RazonSocial, Cliente, NombreCliente
  - nit: NIT, Nit (opcional si hay codigo)
  - unidad_negocio: UNE, UnidadNegocio, Unidad
  - contacto_nombre: Contacto, ContactoNombre, NombreContacto
  - email, telefono, cargo: opcionales

Clave natural Entidad: `codigo`
Clave natural Contacto: (`entidad`, `email`) o (`entidad`, `nombre`)
"""

from __future__ import annotations

import re

import pandas as pd

from core.services.column_map import normalize_columns, pick, require_any
from core.services.import_base import cell_str, run_import_batch
from core.wcg_models import Contacto, DataImportBatch, Entidad, UnidadNegocio


def _slug_codigo(value: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "", value.upper())[:50]
    return s or "SINCODIGO"


def _resolve_unidad(code_or_name: str) -> UnidadNegocio | None:
    if not code_or_name:
        return None
    raw = code_or_name.strip()
    raw_upper = raw.upper()
    raw_lower = raw.lower()

    # Si dice Investment/Inversión, es Inversiones (no Factoraje/Leasing).
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
        }
        code = mapping.get(raw_upper, raw_upper.replace(" ", "_")[:30])

    un = UnidadNegocio.objects.filter(code__iexact=code).first()
    if un:
        return un
    # TODO negocio: confirmar catálogo oficial de códigos UNE → UnidadNegocio
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


def import_infoclientes_wcg(user, uploaded_file) -> DataImportBatch:
    from core.services.import_base import read_dataframe

    df = normalize_columns(read_dataframe(uploaded_file))
    require_any(
        df,
        [["codigo", "codigo_cliente", "nit", "nombre", "cliente", "razon_social"]],
    )
    uploaded_file.seek(0)

    def handler(row: pd.Series, errors: list[str]):
        codigo = _entidad_codigo_from_row(row)
        nombre = pick(row, "nombre", "razon_social", "cliente", "nombre_cliente")
        if not codigo or not nombre:
            errors.append("falta identificador o nombre de entidad")
            return None
        unidad = _resolve_unidad(pick(row, "une", "unidad_negocio", "unidad", "une_origen"))
        tipo_raw = pick(row, "tipo", "tipo_entidad", "tipo_cliente").upper()
        tipo = Entidad.TIPO_CLIENTE
        if "PROSPECT" in tipo_raw:
            tipo = Entidad.TIPO_PROSPECTO
        entidad, created_e = Entidad.objects.update_or_create(
            codigo=codigo,
            defaults={
                "nombre": nombre,
                "nit": pick(row, "nit", "nit_cliente"),
                "tipo": tipo,
                "unidad_negocio": unidad,
                "activa": True,
                "notas": pick(row, "notas", "observaciones"),
            },
        )
        contacto_nombre = pick(row, "contacto", "contacto_nombre", "nombre_contacto")
        if contacto_nombre:
            email = pick(row, "email", "correo", "correo_electronico")
            defaults = {
                "nombre": contacto_nombre,
                "email": email,
                "telefono": pick(row, "telefono", "tel", "celular"),
                "cargo": pick(row, "cargo", "puesto"),
                "es_principal": True,
                "activo": True,
            }
            if email:
                _, created_c = Contacto.objects.update_or_create(
                    entidad=entidad, email=email, defaults=defaults
                )
            else:
                _, created_c = Contacto.objects.update_or_create(
                    entidad=entidad, nombre=contacto_nombre, defaults=defaults
                )
            return created_e or created_c, not (created_e or created_c)
        return created_e, not created_e

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
