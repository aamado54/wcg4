"""Navegación unificada del Centro de operaciones (admin-hub, importaciones, sistema)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.urls import NoReverseMatch, reverse

from core.access import can_access_ops, can_access_risk_gerencia


@dataclass(frozen=True)
class OpsLink:
    id: str
    label: str
    url_name: str
    url_kwargs: dict | None = None
    path_prefixes: tuple[str, ...] = ()
    superuser_only: bool = False
    gerencia_only: bool = False

    def resolve_url(self) -> str:
        try:
            return reverse(self.url_name, kwargs=self.url_kwargs or {})
        except NoReverseMatch:
            return "#"


def _pgc_period_qs(request) -> str:
    from pgc.admin_utils import parse_admin_period

    period = parse_admin_period(request)
    return period.querystring()


def _pgc_url(request, url_name: str) -> str:
    base = reverse(url_name)
    qs = _pgc_period_qs(request)
    return f"{base}?{qs}" if qs else base


PGC_WORKFLOW: tuple[OpsLink, ...] = (
    OpsLink("monthly", "1. Tablero mensual", "pgc:admin_monthly", path_prefixes=("/admin-hub/mensual",)),
    OpsLink(
        "ingresos_year",
        "2. Ingresos (año completo)",
        "pgc:admin_ingresos_year",
        path_prefixes=("/admin-hub/mensual/ingresos",),
    ),
    OpsLink(
        "requirements_year",
        "3. Requerimientos (año completo)",
        "pgc:admin_requirements_year",
        path_prefixes=("/admin-hub/mensual/requerimientos",),
    ),
    OpsLink(
        "manual",
        "4. Edición manual",
        "pgc:admin_manual_edit",
        path_prefixes=("/admin-hub/mensual/edicion",),
    ),
    OpsLink(
        "clients_browse",
        "5. Clientes nuevos (registros)",
        "pgc:admin_new_clients_browse",
        path_prefixes=("/admin-hub/mensual/clientes-nuevos",),
    ),
    OpsLink(
        "clients_une",
        "6. Clientes nuevos (UNE)",
        "pgc:admin_new_clients_une",
        path_prefixes=("/admin-hub/mensual/clientes-nuevos/une",),
    ),
    OpsLink(
        "log",
        "7. Bitácora del período",
        "pgc:admin_monthly_log",
        path_prefixes=("/admin-hub/mensual/bitacora",),
    ),
    OpsLink(
        "tv_charts",
        "8. Gráficas para TV",
        "pgc:admin_tv_charts",
        path_prefixes=("/admin-hub/tv-charts",),
    ),
)

IMPORT_LINKS: tuple[OpsLink, ...] = (
    OpsLink(
        "import_hub",
        "Importación general",
        "imports:import_hub",
        path_prefixes=("/importaciones", "/admin-hub/importaciones"),
    ),
    OpsLink(
        "duplicates",
        "Revisar duplicados",
        "imports:duplicates_review",
        path_prefixes=("/importaciones/duplicados",),
    ),
)

SYSTEM_LINKS: tuple[OpsLink, ...] = (
    OpsLink("estado", "Estado del sistema", "portal:estado", path_prefixes=("/panel/estado",)),
    OpsLink("ayuda", "Guía de uso", "portal:ayuda", path_prefixes=("/panel/ayuda",)),
    OpsLink("django_admin", "Soporte técnico (Django)", "", path_prefixes=("/admin/",), superuser_only=True),
)

GERENCIA_LINKS: tuple[OpsLink, ...] = (
    OpsLink(
        "gerencia_config",
        "Ajustes de interpretación",
        "gerencia:config",
        path_prefixes=("/gerencia/ajustes",),
        gerencia_only=True,
    ),
)


def _path(request) -> str:
    return getattr(request, "path", "") or ""


def _link_active(path: str, link: OpsLink) -> bool:
    if link.id == "django_admin":
        return path.startswith("/admin/") and not path.startswith("/admin-hub")
    if link.id == "clients_browse":
        return path.startswith("/admin-hub/mensual/clientes-nuevos") and "/une" not in path
    if link.id == "clients_une":
        return "/admin-hub/mensual/clientes-nuevos/une" in path
    for prefix in link.path_prefixes:
        if path.startswith(prefix):
            return True
    if link.url_name:
        try:
            resolved = reverse(link.url_name, kwargs=link.url_kwargs or {})
            if path == resolved or path.rstrip("/") == resolved.rstrip("/"):
                return True
        except NoReverseMatch:
            pass
    return False


def _section_active(path: str, section_id: str) -> bool:
    if section_id == "home":
        return path.rstrip("/") == reverse("pgc:admin_hub").rstrip("/")
    if section_id == "pgc":
        if path.rstrip("/") == reverse("pgc:admin_hub").rstrip("/"):
            return False
        return any(
            path.startswith(p)
            for p in (
                "/admin-hub/mensual",
                "/admin-hub/tv-charts",
                "/admin-hub/recalcular",
                "/admin-hub/auto-recalcular",
                "/admin-hub/run-recalc",
                "/admin-hub/exchange-rates",
                "/admin-hub/ingresos-manual-capture",
            )
        )
    if section_id == "import":
        return path.startswith("/importaciones") or path.startswith("/admin-hub/importaciones")
    if section_id == "gerencia":
        return path.startswith("/gerencia/ajustes")
    if section_id == "system":
        return any(_link_active(path, l) for l in SYSTEM_LINKS)
    return False


def _visible_links(user, links: tuple[OpsLink, ...]) -> list[OpsLink]:
    out: list[OpsLink] = []
    for link in links:
        if link.superuser_only and not getattr(user, "is_superuser", False):
            continue
        if link.gerencia_only and not can_access_risk_gerencia(user):
            continue
        out.append(link)
    return out


def build_ops_hub(request) -> dict[str, Any] | None:
    user = getattr(request, "user", None)
    if not can_access_ops(user):
        return None
    path = _path(request)
    if not (
        path.startswith("/admin-hub")
        or path.startswith("/importaciones")
        or path.startswith("/panel/estado")
        or path.startswith("/panel/ayuda")
        or (path.startswith("/gerencia/ajustes") and can_access_risk_gerencia(user))
    ):
        return None

    sections = [
        {"id": "home", "label": "Inicio", "url": reverse("pgc:admin_hub")},
        {"id": "pgc", "label": "PGC · Cierre mensual", "url": _pgc_url(request, "pgc:admin_monthly")},
        {"id": "import", "label": "Importación de datos", "url": reverse("imports:import_hub")},
    ]
    if can_access_risk_gerencia(user):
        sections.append(
            {
                "id": "gerencia",
                "label": "Centro gerencial",
                "url": reverse("gerencia:config"),
            }
        )
    sections.append({"id": "system", "label": "Sistema", "url": reverse("portal:estado")})

    active_section = "pgc"
    for sid in ("home", "import", "gerencia", "system", "pgc"):
        if _section_active(path, sid):
            active_section = sid
            break

    for sec in sections:
        sec["active"] = sec["id"] == active_section

    subsections: list[dict[str, Any]] = []
    if active_section == "pgc":
        for link in PGC_WORKFLOW:
            subsections.append(
                {
                    "id": link.id,
                    "label": link.label,
                    "url": _pgc_url(request, link.url_name),
                    "active": _link_active(path, link),
                }
            )
    elif active_section == "import":
        for link in _visible_links(user, IMPORT_LINKS):
            subsections.append(
                {
                    "id": link.id,
                    "label": link.label,
                    "url": link.resolve_url(),
                    "active": _link_active(path, link),
                }
            )
    elif active_section == "gerencia":
        for link in _visible_links(user, GERENCIA_LINKS):
            subsections.append(
                {
                    "id": link.id,
                    "label": link.label,
                    "url": link.resolve_url(),
                    "active": _link_active(path, link),
                }
            )
    elif active_section == "system":
        for link in _visible_links(user, SYSTEM_LINKS):
            url = "/admin/" if link.id == "django_admin" else link.resolve_url()
            subsections.append(
                {
                    "id": link.id,
                    "label": link.label,
                    "url": url,
                    "active": _link_active(path, link),
                    "external": link.id == "django_admin",
                }
            )

    return {
        "active_section": active_section,
        "sections": sections,
        "subsections": subsections,
        "pgc_workflow": PGC_WORKFLOW,
    }


def ops_hub_context(request):
    hub = build_ops_hub(request)
    return {
        "ops_hub": hub,
        "in_ops_hub": hub is not None,
    }


def hub_landing_groups(request) -> list[dict[str, Any]]:
    """Tarjetas del inicio del centro de operaciones, en orden operativo."""
    user = getattr(request, "user", None)
    groups: list[dict[str, Any]] = [
        {
            "title": "PGC · Cierre mensual",
            "lead": "Flujo recomendado: tablero → cargas → ingresos → ajustes → clientes → cierre.",
            "links": [
                {"label": link.label, "url": _pgc_url(request, link.url_name)}
                for link in PGC_WORKFLOW
            ],
        },
        {
            "title": "Importación de datos",
            "lead": "Carga única para CRM, PGO, Balón, PGC y archivos operativos.",
            "links": [
                {"label": link.label, "url": link.resolve_url()}
                for link in _visible_links(user, IMPORT_LINKS)
            ],
        },
    ]
    if can_access_risk_gerencia(user):
        groups.append(
            {
                "title": "Centro gerencial",
                "lead": "Parámetros de interpretación para vistas de gerencia.",
                "links": [
                    {"label": link.label, "url": link.resolve_url()}
                    for link in _visible_links(user, GERENCIA_LINKS)
                ],
            }
        )
    groups.append(
        {
            "title": "Sistema",
            "lead": "Salud de datos, documentación y administración técnica.",
            "links": [
                {
                    "label": link.label,
                    "url": "/admin/" if link.id == "django_admin" else link.resolve_url(),
                    "external": link.id == "django_admin",
                }
                for link in _visible_links(user, SYSTEM_LINKS)
            ],
        }
    )
    return groups
