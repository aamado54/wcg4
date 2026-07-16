"""Resolución de entidades y unidades para importadores."""

from __future__ import annotations

import re

import pandas as pd

from apps.core.models import Contacto, Entidad, UnidadNegocio

from .columns import pick


def normalize_nit(value: str) -> str:
    return re.sub(r"[^0-9A-Za-z]", "", value or "").upper()


def normalize_nombre(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip())


def find_entidad(*, nit: str = "", nombre: str = "") -> Entidad | None:
    nit_clean = normalize_nit(nit)
    if nit_clean:
        entidad = Entidad.objects.filter(nit__iexact=nit_clean).first()
        if entidad:
            return entidad
        entidad = Entidad.objects.filter(nit__icontains=nit_clean[:20]).first()
        if entidad:
            return entidad
    nombre_clean = normalize_nombre(nombre)
    if nombre_clean:
        return Entidad.objects.filter(nombre__iexact=nombre_clean).first()
    return None


def upsert_entidad(
    *,
    nit: str = "",
    nombre: str,
    defaults: dict | None = None,
) -> tuple[Entidad, bool, bool]:
    """Retorna (entidad, creado, actualizado)."""
    defaults = defaults or {}
    nombre_clean = normalize_nombre(nombre)
    if not nombre_clean:
        raise ValueError("Nombre de entidad obligatorio.")
    nit_clean = normalize_nit(nit)
    entidad = find_entidad(nit=nit_clean, nombre=nombre_clean)
    field_defaults = {
        "nombre": nombre_clean,
        "activo": True,
        **defaults,
    }
    if nit_clean:
        field_defaults["nit"] = nit_clean
    if entidad:
        changed = False
        for key, value in field_defaults.items():
            if value and getattr(entidad, key) != value:
                setattr(entidad, key, value)
                changed = True
        if changed:
            entidad.save()
        return entidad, False, changed
    entidad = Entidad.objects.create(**field_defaults)
    return entidad, True, False


def resolve_unidad(code_or_name: str) -> UnidadNegocio | None:
    if not code_or_name:
        return None
    raw = code_or_name.strip()
    mapping = {
        "INVESTMENT - WC FACTORING": "FACTORING",
        "INVESTMENT - WC LEASING": "LEASING",
        "FACTORAJE": "FACTORING",
        "LEASING": "LEASING",
        "TI": "TI",
    }
    code = mapping.get(raw.upper(), raw.upper().replace(" ", "_")[:30])
    unidad = UnidadNegocio.objects.filter(codigo__iexact=code).first()
    if unidad:
        return unidad
    return UnidadNegocio.objects.filter(nombre__icontains=raw[:25]).first()


def upsert_contacto_from_row(entidad: Entidad, row: pd.Series) -> tuple[Contacto | None, bool]:
    contacto_nombre = pick(row, "contacto", "contacto_nombre", "nombre_contacto")
    if not contacto_nombre:
        return None, False
    email = pick(row, "email", "correo", "correo_electronico")
    defaults = {
        "nombre": contacto_nombre,
        "email": email,
        "telefono_movil": pick(row, "telefono", "tel", "celular", "telefono_movil"),
        "cargo": pick(row, "cargo", "puesto"),
        "activo": True,
    }
    if email:
        contacto, created = Contacto.objects.update_or_create(
            entidad=entidad,
            email=email,
            defaults=defaults,
        )
        return contacto, created
    contacto, created = Contacto.objects.update_or_create(
        entidad=entidad,
        nombre=contacto_nombre,
        defaults=defaults,
    )
    return contacto, created


def ensure_entidad_from_row(row: pd.Series, errors: list[str]) -> Entidad | None:
    nombre = pick(row, "nombre", "razon_social", "cliente", "nombre_cliente")
    nit = pick(row, "nit", "nit_cliente")
    if not nombre and not nit:
        errors.append("Falta nombre o NIT de entidad.")
        return None
    if not nombre:
        nombre = nit
    try:
        entidad, _, _ = upsert_entidad(
            nit=nit,
            nombre=nombre,
            defaults={
                "telefono": pick(row, "telefono", "tel"),
                "email": pick(row, "email", "correo"),
                "origen": "importacion",
            },
        )
        return entidad
    except ValueError as exc:
        errors.append(str(exc))
        return None
