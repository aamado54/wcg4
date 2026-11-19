"""Inventario de comandos CLI `import_*` y cobertura de ImportAuditCommandMixin."""

from __future__ import annotations

# Filas: management command name (sin app prefix), import_tipo, mixin activo.
CLI_IMPORT_COMMANDS: list[dict[str, object]] = [
    {"command": "import_clientes_nuevos", "tipo": "new_clients", "mixin": True, "app": "imports"},
    {"command": "import_venta_cruzada", "tipo": "cross_sale", "mixin": True, "app": "imports"},
    {"command": "import_ingresos", "tipo": "financial", "mixin": True, "app": "imports"},
    {"command": "import_inversiones_crecimiento", "tipo": "investment_growth", "mixin": True, "app": "imports"},
    {"command": "import_bancos_fin_mes", "tipo": "bank_loans", "mixin": True, "app": "imports"},
    {"command": "import_ingresos_comisiones_tsv", "tipo": "ingresos_comisiones", "mixin": True, "app": "imports"},
    {"command": "import_pgc_objetivos", "tipo": "pgc_objetivos", "mixin": True, "app": "pgc"},
    {"command": "import_pgc_objetivos_tsv", "tipo": "pgc_objetivos_tsv", "mixin": True, "app": "pgc"},
    {"command": "import_pgc_metas", "tipo": "pgc_metas", "mixin": True, "app": "pgc"},
    {"command": "import_archivos_pgo_file", "tipo": "pgo_catalogo", "mixin": True, "app": "pgo"},
    {"command": "import_estados_financieros", "tipo": "eeff_legacy", "mixin": True, "app": "core"},
    {"command": "import_wcg_data", "tipo": "", "mixin": False, "app": "core", "note": "orquestador multi-módulo"},
    {"command": "load_wcg_data", "tipo": "", "mixin": False, "app": "imports", "note": "carga demo"},
]

# Despacho hub (`run_import`) — siempre audita vía `_audit_after_dispatch`.
DISPATCH_IMPORT_TIPOS = (
    "crm_clientes",
    "pgo_tickets",
    "pgo_catalogo",
    "pgo_expedientes",
    "risk_leasing",
    "risk_rentas",
    "new_clients",
    "cross_sale",
    "financial",
    "investment_growth",
    "bank_loans",
)


def cli_audit_coverage_ratio() -> tuple[int, int, float]:
    """(con mixin, total CLI catalogados, porcentaje)."""
    rows = [r for r in CLI_IMPORT_COMMANDS if r.get("app")]
    with_mixin = sum(1 for r in rows if r.get("mixin"))
    total = len(rows)
    pct = (100.0 * with_mixin / total) if total else 100.0
    return with_mixin, total, pct


def missing_cli_mixin_commands() -> list[str]:
    return [str(r["command"]) for r in CLI_IMPORT_COMMANDS if not r.get("mixin")]