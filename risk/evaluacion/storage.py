"""Almacenamiento de plantillas individuales subidas vía UI (Task 3B)."""

from __future__ import annotations

import re
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile

SAFE_XLSX = re.compile(r"^[\w.\- ()áéíóúñÁÉÍÓÚÑ]+\.xlsx$", re.IGNORECASE)


def upload_plantillas_dir() -> Path:
    configured = getattr(settings, "WCG_EVALUACION_UPLOAD_DIR", None)
    path = Path(configured) if configured else Path(settings.MEDIA_ROOT) / "evaluacion" / "plantillas"
    path.mkdir(parents=True, exist_ok=True)
    return path


def sanitize_plantilla_name(name: str) -> str:
    base = Path(name or "plantilla.xlsx").name.strip()
    if not base.lower().endswith(".xlsx"):
        base = f"{base}.xlsx"
    base = re.sub(r"[^\w.\- ()áéíóúñÁÉÍÓÚÑ]", "_", base)
    if not SAFE_XLSX.match(base):
        raise ValueError(f"Nombre de archivo no permitido: {name}")
    return base


def has_uploaded_plantillas() -> bool:
    from risk.models import EvaluacionPlantilla

    if EvaluacionPlantilla.objects.filter(is_active=True).exists():
        return True
    directory = upload_plantillas_dir()
    return any(directory.glob("*.xlsx"))


def save_uploaded_plantilla(uploaded: UploadedFile, *, user) -> "EvaluacionPlantilla":
    from risk.models import EvaluacionPlantilla

    original = sanitize_plantilla_name(uploaded.name or "plantilla.xlsx")
    content = uploaded.read()
    if not content:
        raise ValueError("El archivo está vacío.")

    plantilla = EvaluacionPlantilla(
        original_filename=original,
        uploaded_by=user if getattr(user, "is_authenticated", False) else None,
        file_size=len(content),
        is_active=True,
    )
    plantilla.stored_file.save(original, ContentFile(content), save=False)
    plantilla.save()
    return plantilla
