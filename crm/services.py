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
