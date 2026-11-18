"""Registro de eventos de auditoría de importación."""

from __future__ import annotations

import threading
from contextlib import contextmanager
from pathlib import Path

from django.contrib.auth import get_user_model
from django.utils import timezone

from imports.models import FileUpload, ImportAuditEvent

_audit_suppress = threading.local()


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
        name = getattr(batch, "original_filename", None) or getattr(
            batch, "archivo_nombre", None
        )
        if name:
            return name
    if uploaded_file is not None:
        name = getattr(uploaded_file, "name", None)
        if name:
            return name
    return ""


def normalize_path_key(path: str | Path) -> str:
    try:
        return str(Path(path).expanduser())
    except (TypeError, ValueError, OSError):
        return str(path or "")[:512]


def import_audit_suppressed() -> bool:
    return bool(getattr(_audit_suppress, "depth", 0))


@contextmanager
def suppress_import_audit():
    """Evita eventos duplicados cuando dispatch invoca importadores CLI."""
    depth = getattr(_audit_suppress, "depth", 0)
    _audit_suppress.depth = depth + 1
    try:
        yield
    finally:
        _audit_suppress.depth = max(0, depth)


@contextmanager
def cli_import_audit(
    path: str | Path,
    import_tipo: str,
    *,
    user=None,
    file_upload_id: int | None = None,
    source: str = ImportAuditEvent.SOURCE_OPS,
    detail: dict | None = None,
):
    """Registra auditoría al finalizar un comando `import_*` invocado directamente."""
    if import_audit_suppressed():
        yield
        return

    path_key = normalize_path_key(path)
    success = True
    error_message = ""
    extra_detail = dict(detail or {})
    try:
        yield
    except Exception as exc:
        success = False
        error_message = str(exc)
        raise
    finally:
        if import_audit_suppressed():
            return
        fu = None
        if file_upload_id:
            fu = FileUpload.objects.filter(pk=file_upload_id).first()
        op_user = user
        if op_user is None:
            User = get_user_model()
            op_user = User.objects.filter(is_superuser=True).first()
        record_import_audit_event(
            user=op_user,
            file_path_key=path_key,
            success=success,
            source=source,
            error_message=error_message,
            import_tipo=import_tipo,
            file_upload=fu,
            detail={**extra_detail, "cli": True},
        )


def record_import_audit_for_path(
    *,
    user,
    path: str | Path,
    success: bool,
    import_tipo: str,
    source: str = ImportAuditEvent.SOURCE_MANUAL,
    error_message: str = "",
    file_upload=None,
    detail: dict | None = None,
) -> ImportAuditEvent | None:
    """Atajo para importaciones fuera de `run_import` (p. ej. Admin mensual)."""
    path_key = normalize_path_key(path)
    if not path_key:
        return None
    return record_import_audit_event(
        user=user,
        file_path_key=path_key,
        success=success,
        source=source,
        error_message=error_message,
        import_tipo=import_tipo,
        file_upload=file_upload,
        detail=detail,
    )


def latest_events_for_path(path_key: str, *, limit: int = 20):
    """Últimos eventos cuyo file_path_key coincide o termina en el mismo nombre."""
    from django.db.models import Q

    path_key = (path_key or "").strip()
    if not path_key:
        return ImportAuditEvent.objects.none()
    name = Path(path_key).name
    cond = Q(file_path_key=path_key)
    if name and name != path_key:
        cond |= Q(file_path_key__endswith=name)
    return (
        ImportAuditEvent.objects.filter(cond)
        .select_related("user", "file_upload")
        .order_by("-loaded_at")[:limit]
    )


def audit_summary_counts():
    """Conteos rápidos para checklist / admin."""
    from django.db.models import Count

    qs = ImportAuditEvent.objects.all()
    total = qs.count()
    fail = qs.filter(success=False).count()
    by_tipo = list(
        qs.exclude(import_tipo="")
        .values("import_tipo")
        .annotate(n=Count("id"))
        .order_by("-n")
    )
    return {"total": total, "ok": total - fail, "fail": fail, "by_tipo": by_tipo}