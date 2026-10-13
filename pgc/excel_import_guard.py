"""Bloqueo de imports desde hoja Objetivos (libro Cumplimiento Objetivos PGC).

No afecta otros xlsx operativos (ER / import_ingresos, hub financiero).
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from django.core.management.base import CommandError

if TYPE_CHECKING:
    from django.core.management.base import BaseCommand

ENV_ALLOW_PGC_EXCEL_IMPORT = "ALLOW_PGC_EXCEL_IMPORT"
DOC_POLICY = "docs/pgc-sin-excel-objetivos-validacion.md"

_LEGACY_WARNING = (
    "ADVERTENCIA: import legacy desde hoja Objetivos (libro compartido de validación). "
    "No usar en cierre mensual de producción; use import_ingresos y cargas del hub."
)


def pgc_excel_import_env_allowed() -> bool:
    return os.environ.get(ENV_ALLOW_PGC_EXCEL_IMPORT, "").strip() in (
        "1",
        "true",
        "True",
        "yes",
        "YES",
    )


def assert_pgc_objetivos_import_allowed(
    command: BaseCommand,
    *,
    force_legacy_excel: bool = False,
) -> None:
    """Permite import Objetivos solo con ALLOW_PGC_EXCEL_IMPORT=1 o --force-legacy-excel."""
    if pgc_excel_import_env_allowed():
        return
    if force_legacy_excel:
        command.stdout.write(command.style.WARNING(_LEGACY_WARNING))
        return
    raise CommandError(
        "Import desde la hoja Objetivos del libro «Cumplimiento Objetivos PGC» "
        "(validación compartida) está deshabilitado. "
        "Ejecución oficial: `import_ingresos` (xlsx ER Factoraje/Leasing), hub financiero, "
        "clientes y venta cruzada. "
        "Cuadre sin cargar datos: "
        "`python tools/pgc/validate_ejecucion_excel.py <archivo.xlsx> --year AÑO`. "
        f"Legacy (dev/migración): export {ENV_ALLOW_PGC_EXCEL_IMPORT}=1 "
        "o `--force-legacy-excel`. "
        f"Ver {DOC_POLICY}."
    )
