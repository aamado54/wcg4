"""Utilidades base para importaciones CSV/XLSX."""

from __future__ import annotations

import io
from typing import Any, Callable

import pandas as pd
from django.core.files.uploadedfile import UploadedFile

from core.wcg_models import DataImportBatch


class ImportValidationError(Exception):
    pass


def read_dataframe(uploaded_file, sheet_name=0) -> pd.DataFrame:
    name = (uploaded_file.name or "").lower()
    raw = uploaded_file.read()
    uploaded_file.seek(0)
    if name.endswith((".xlsx", ".xls")):
        if sheet_name is None:
            xls = pd.ExcelFile(io.BytesIO(raw))
            sheet_name = xls.sheet_names[0]
            for candidate in xls.sheet_names:
                low = candidate.lower()
                if any(k in low for k in ("base", "leasing", "datos", "ticket")):
                    sheet_name = candidate
                    break
            return pd.read_excel(xls, sheet_name=sheet_name)
        return pd.read_excel(io.BytesIO(raw), sheet_name=sheet_name)
    if name.endswith((".csv", ".tsv", ".txt")):
        return pd.read_csv(io.BytesIO(raw))
    raise ImportValidationError("Formato no soportado. Use CSV o XLSX.")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    from .column_map import normalize_columns as _norm

    return _norm(df)


def read_dataframe_from_path(path) -> pd.DataFrame:
    """Lee CSV/XLSX desde ruta en disco (comandos de management)."""
    path_str = str(path).lower()
    if path_str.endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    return pd.read_csv(path)


def require_columns(df: pd.DataFrame, required: list[str]) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ImportValidationError(f"Faltan columnas: {', '.join(missing)}")


def cell_str(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def run_import_batch(
    *,
    user,
    modulo: str,
    tipo_importacion: str,
    uploaded_file: UploadedFile,
    required_columns: list[str],
    row_handler: Callable[[pd.Series, list[str]], tuple[bool, bool] | None],
) -> DataImportBatch:
    """
    row_handler recibe la fila y una lista mutable de mensajes de error por fila.
    Debe retornar (creado, actualizado) o None si hubo error en row_errors.
    """
    batch = DataImportBatch.objects.create(
        modulo=modulo,
        tipo_importacion=tipo_importacion,
        archivo_nombre=uploaded_file.name,
        uploaded_by=user,
        status=DataImportBatch.STATUS_PENDING,
    )
    logs: list[str] = []
    try:
        df = normalize_columns(read_dataframe(uploaded_file))
        require_columns(df, required_columns)
        batch.filas_leidas = len(df)
        for idx, row in df.iterrows():
            row_errors: list[str] = []
            try:
                result = row_handler(row, row_errors)
                if row_errors:
                    batch.errores += 1
                    logs.append(f"Fila {idx + 2}: {'; '.join(row_errors)}")
                elif result:
                    created, updated = result
                    if created:
                        batch.creados += 1
                    if updated:
                        batch.actualizados += 1
            except Exception as exc:
                batch.errores += 1
                logs.append(f"Fila {idx + 2}: {exc}")
        if batch.errores == 0:
            batch.status = DataImportBatch.STATUS_OK
        elif batch.creados + batch.actualizados > 0:
            batch.status = DataImportBatch.STATUS_PARTIAL
        else:
            batch.status = DataImportBatch.STATUS_ERROR
    except Exception as exc:
        batch.status = DataImportBatch.STATUS_ERROR
        logs.append(str(exc))
    batch.log_texto = "\n".join(logs)[:8000]
    batch.save()
    return batch
