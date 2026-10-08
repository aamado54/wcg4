"""Estado activo unificado de la navegación superior WCG."""

from __future__ import annotations

from typing import Any

# Rutas PGC productivas (raíz del sitio, no /pgc/ módulo demo).
PGC_REPORT_PREFIXES = (
    "/tablero",
    "/ingresos",
    "/clientes-nuevos",
    "/venta-cruzada",
    "/respuesta-reqs",
)


def _path(request) -> str:
    return (getattr(request, "path", None) or "").rstrip("/") or "/"


def _startswith(path: str, prefix: str) -> bool:
    p = prefix.rstrip("/")
    return path == p or path.startswith(p + "/")


def resolve_wcg_nav(request) -> dict[str, Any]:
    path = _path(request)

    is_portal_home = path in ("/panel", "/")
    is_ops = _startswith(path, "/admin-hub") or _startswith(path, "/importaciones")
    is_gerencia = _startswith(path, "/gerencia")
    is_risk = _startswith(path, "/risk") and not is_gerencia
    is_pgo = _startswith(path, "/pgo")
    is_crm = _startswith(path, "/crm")
    is_pgc_module = _startswith(path, "/pgc") or _startswith(path, "/wcgone/pgc")

    pgc_section = ""
    if _startswith(path, "/tablero"):
        pgc_section = "tablero"
    elif _startswith(path, "/ingresos"):
        pgc_section = "ingresos"
    elif _startswith(path, "/clientes-nuevos"):
        pgc_section = "clientes"
    elif _startswith(path, "/venta-cruzada"):
        pgc_section = "venta_cruzada"
    elif _startswith(path, "/respuesta-reqs"):
        pgc_section = "respuesta_reqs"

    is_pgc = bool(pgc_section) or is_pgc_module

    module = ""
    if is_portal_home:
        module = "portal"
    elif is_ops:
        module = "ops"
    elif is_gerencia:
        module = "gerencia"
    elif is_risk:
        module = "risk"
    elif is_pgo:
        module = "pgo"
    elif is_crm:
        module = "crm"
    elif is_pgc:
        module = "pgc"

    return {
        "is_portal_home": is_portal_home,
        "module": module,
        "pgc_section": pgc_section,
        "is_ops": is_ops,
    }


def wcg_nav_context(request):
    return {"wcg_nav": resolve_wcg_nav(request)}
