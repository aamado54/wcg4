"""Orquestación de fuentes y consolidación para la vista de evaluación."""

from __future__ import annotations

from pathlib import Path

from django.conf import settings

from risk.evaluacion.persist import load_latest_dataset, save_import_run
from risk.evaluacion.reader import default_plantillas_dir, default_xlsx_path, load_evaluacion
from risk.evaluacion.storage import has_uploaded_plantillas, upload_plantillas_dir
from risk.models import EvaluacionPlantilla


def _plantillas_dir_for_uploads() -> Path | None:
    directory = upload_plantillas_dir()
    active = EvaluacionPlantilla.objects.filter(is_active=True).exists()
    if active or any(directory.glob("*.xlsx")):
        return directory
    return None


def resolve_evaluacion_dataset(source_mode: str = "auto"):
    mode = (source_mode or "auto").strip().lower()

    if mode == "db":
        dataset = load_latest_dataset()
        if dataset:
            return dataset, "db"
        return load_evaluacion(), "consolidado"

    if mode == "upload":
        directory = _plantillas_dir_for_uploads()
        if directory:
            return load_evaluacion(templates_dir=directory), "upload"
        return load_evaluacion(), "consolidado"

    if mode == "plantillas":
        plantillas = default_plantillas_dir()
        if plantillas and any(plantillas.glob("*.xlsx")):
            return load_evaluacion(templates_dir=plantillas), "plantillas"
        return load_evaluacion(), "consolidado"

    if mode == "consolidado":
        return load_evaluacion(), "consolidado"

    # auto: uploads (prod) → plantillas ejemplo → xlsx docs
    upload_dir = _plantillas_dir_for_uploads()
    if upload_dir:
        return load_evaluacion(templates_dir=upload_dir), "upload"

    plantillas = default_plantillas_dir()
    if plantillas and any(plantillas.glob("*.xlsx")):
        return load_evaluacion(templates_dir=plantillas), "plantillas"

    xlsx = default_xlsx_path()
    if xlsx.is_file():
        return load_evaluacion(path=xlsx), "consolidado"

    return load_evaluacion(), "consolidado"


def consolidate_and_persist(dataset, *, user=None) -> None:
    if not dataset.companies:
        return
    active_count = EvaluacionPlantilla.objects.filter(is_active=True).count()
    save_import_run(
        dataset,
        user=user,
        plantillas_count=active_count,
    )


def refresh_evaluacion_from_uploads(*, user=None):
    directory = _plantillas_dir_for_uploads()
    if not directory:
        return None
    dataset = load_evaluacion(templates_dir=directory)
    consolidate_and_persist(dataset, user=user)
    return dataset
