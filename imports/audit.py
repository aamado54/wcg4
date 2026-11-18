"""Registro de eventos de auditoría de importación."""

from __future__ import annotations

from pathlib import Path

from django.utils import timezone

from imports.models import ImportAuditEvent


def file_available_on_disk(path_key: str) -> bool:
    if not path_key:
        return False
    try:
        return Path(path_key).expanduser().is_file()
    except OSError:
        return False


def record_import_audit_event(
    *,
    user,
    file_path_key: str,
    success: bool,
    source: str = ImportAuditEvent.SOURCE_OPS,
    error_message: str = "",
    import_tipo: str = "",
    file_upload=None,
    file_available: bool | None = None,
    detail: dict | None = None,
) -> ImportAuditEvent:
    if file_available is None:
        file_available = file_available_on_disk(file_path_key)
    return ImportAuditEvent.objects.create(
        user=user,
        file_path_key=(file_path_key or "")[:512],
        file_available=file_available,
        loaded_at=timezone.now(),
        success=success,
        error_message=(error_message or "")[:4000],
        source=source,
        import_tipo=(import_tipo or "")[:50],
        file_upload=file_upload,
        detail_json=detail or {},
    )


def resolve_path_key_from_upload(uploaded_file, batch=None) -> str:
    """Deriva clave de archivo para auditoría desde upload o batch."""
    if batch is not None:
        stored = getattr(batch, "stored_file", None)
        if stored:
            try:
                return str(stored.path)
            except Exception:
                pass
        name = getattr(batch, "original_filename", None)
        if name:
            return name
    if uploaded_file is not None:
        name = getattr(uploaded_file, "name", None)
        if name:
            return name
    return ""