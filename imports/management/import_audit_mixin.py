"""Mixin para registrar ImportAuditEvent en comandos import_* vía CLI."""

from __future__ import annotations

from pathlib import Path

from imports.audit import cli_import_audit


class ImportAuditCommandMixin:
    """Envuelve `execute` con auditoría si existe `--path` y `import_audit_tipo`."""

    import_audit_tipo: str = ""

    def execute(self, *args, **options):
        tipo = (self.import_audit_tipo or "").strip()
        raw_path = options.get("path")
        if not tipo or not raw_path:
            return super().execute(*args, **options)

        path = Path(raw_path)
        if not path.exists():
            return super().execute(*args, **options)

        detail = {}
        year = options.get("year")
        month = options.get("month")
        if year is not None and month is not None:
            detail["year"] = year
            detail["month"] = month

        with cli_import_audit(
            path,
            tipo,
            file_upload_id=options.get("file_upload_id"),
            detail=detail or None,
        ):
            return super().execute(*args, **options)