"""Mixin para registrar ImportAuditEvent en comandos import_* vía CLI."""

from __future__ import annotations

from pathlib import Path

from imports.audit import cli_import_audit


class ImportAuditCommandMixin:
    """Envuelve `execute` con auditoría si existe `--path` y `import_audit_tipo`."""

    import_audit_tipo: str = ""

    def _resolve_audit_path(self, options) -> Path | None:
        for key in ("path", "source_dir", "file"):
            raw = options.get(key)
            if raw:
                return Path(str(raw)).expanduser()
        return None

    def execute(self, *args, **options):
        tipo = (self.import_audit_tipo or "").strip()
        path = self._resolve_audit_path(options)
        if not tipo or path is None:
            return super().execute(*args, **options)

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