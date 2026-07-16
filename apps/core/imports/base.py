"""Utilidades compartidas de importación CSV/XLSX."""

from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
from typing import Any, Callable

import pandas as pd
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from apps.core.models import DataImportBatch, DataImportError


class ImportValidationError(Exception):
    pass


def cell_str(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def row_to_json(row: pd.Series) -> dict:
    data = {}
    for key, value in row.items():
        if pd.isna(value):
            data[str(key)] = None
        elif hasattr(value, "isoformat"):
            data[str(key)] = value.isoformat()
        else:
            data[str(key)] = str(value)
    return data


def read_dataframe(uploaded_file: UploadedFile, sheet_name=0) -> pd.DataFrame:
    name = (uploaded_file.name or "").lower()
    raw = uploaded_file.read()
    uploaded_file.seek(0)
    if not raw:
        raise ImportValidationError("El archivo está vacío.")
    if name.endswith((".xlsx", ".xls")):
        if sheet_name is None:
            xls = pd.ExcelFile(io.BytesIO(raw))
            sheet_name = xls.sheet_names[0]
            for candidate in xls.sheet_names:
                low = candidate.lower()
                if any(k in low for k in ("base", "leasing", "datos", "ticket", "hoja")):
                    sheet_name = candidate
                    break
            df = pd.read_excel(xls, sheet_name=sheet_name)
        else:
            df = pd.read_excel(io.BytesIO(raw), sheet_name=sheet_name)
    elif name.endswith((".csv", ".tsv", ".txt")):
        df = pd.read_csv(io.BytesIO(raw))
    else:
        raise ImportValidationError("Formato no soportado. Use CSV o XLSX.")
    if df.empty:
        raise ImportValidationError("El archivo no contiene filas de datos.")
    return df.dropna(how="all")


def save_upload_copy(uploaded_file: UploadedFile) -> tuple[str, str]:
    uploads_root = Path(settings.UPLOADS_ROOT)
    uploads_root.mkdir(parents=True, exist_ok=True)
    raw = uploaded_file.read()
    uploaded_file.seek(0)
    file_hash = hashlib.sha256(raw).hexdigest()
    dest = uploads_root / f"{file_hash[:16]}_{uploaded_file.name}"
    if not dest.exists():
        dest.write_bytes(raw)
    return str(dest.relative_to(settings.BASE_DIR)), file_hash


def run_import_batch(
    *,
    user,
    modulo: str,
    tipo_importacion: str,
    uploaded_file: UploadedFile,
    preprocess: Callable[[pd.DataFrame], pd.DataFrame] | None = None,
    row_handler: Callable[..., tuple[bool, bool] | None],
) -> DataImportBatch:
    """
    Ejecuta importación fila a fila.
    row_handler retorna (creado, actualizado) o None si hubo errores en row_errors.
    """
    archivo_ruta, archivo_hash = save_upload_copy(uploaded_file)
    batch = DataImportBatch.objects.create(
        modulo=modulo,
        tipo_importacion=tipo_importacion,
        archivo_nombre=uploaded_file.name,
        archivo_hash=archivo_hash,
        archivo_ruta=archivo_ruta,
        usuario=user,
        estado=DataImportBatch.ESTADO_PROCESANDO,
    )
    creados = 0
    actualizados = 0
    logs: list[str] = []

    try:
        df = read_dataframe(uploaded_file)
        if preprocess:
            df = preprocess(df)
        batch.filas_leidas = len(df)

        for idx, row in df.iterrows():
            fila_numero = int(idx) + 2
            row_errors: list[str] = []
            try:
                result = row_handler(row, row_errors, batch)
                if row_errors:
                    batch.filas_error += 1
                    for msg in row_errors:
                        DataImportError.objects.create(
                            batch=batch,
                            fila_numero=fila_numero,
                            mensaje_error=msg,
                            payload_json=row_to_json(row),
                        )
                    logs.append(f"Fila {fila_numero}: {'; '.join(row_errors)}")
                elif result is not None:
                    created, updated = result
                    batch.filas_validas += 1
                    if created:
                        creados += 1
                    if updated:
                        actualizados += 1
                else:
                    batch.filas_error += 1
                    DataImportError.objects.create(
                        batch=batch,
                        fila_numero=fila_numero,
                        mensaje_error="Fila omitida sin detalle.",
                        payload_json=row_to_json(row),
                    )
            except Exception as exc:
                batch.filas_error += 1
                DataImportError.objects.create(
                    batch=batch,
                    fila_numero=fila_numero,
                    mensaje_error=str(exc),
                    payload_json=row_to_json(row),
                )
                logs.append(f"Fila {fila_numero}: {exc}")

        if batch.filas_error == 0 and batch.filas_validas > 0:
            batch.estado = DataImportBatch.ESTADO_OK
        elif batch.filas_validas > 0:
            batch.estado = DataImportBatch.ESTADO_PARCIAL
        elif batch.filas_leidas == 0:
            batch.estado = DataImportBatch.ESTADO_ERROR
            logs.append("No se encontraron filas para procesar.")
        else:
            batch.estado = DataImportBatch.ESTADO_ERROR

    except ImportValidationError as exc:
        batch.estado = DataImportBatch.ESTADO_ERROR
        logs.append(str(exc))
    except Exception as exc:
        batch.estado = DataImportBatch.ESTADO_ERROR
        logs.append(f"Error general: {exc}")

    batch.observaciones = (
        f"Creados: {creados}, Actualizados: {actualizados}. "
        + (" | ".join(logs[:20]) if logs else "")
    )[:8000]
    batch.save()
    return batch
