from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from portal import views as portal_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("importaciones/", include("imports.urls")),

    # PGC1 WCG modules (rutas productivas actuales)
    path("crm/", include("crm.urls")),
    path("risk/", include("risk.urls")),
    path("pgo/", include("pgo.urls")),
    path("reports/", include("reports.urls")),

    # Entry: splash → menú
    path("", portal_views.splash, name="splash"),
    path("panel/", include("portal.urls")),
    path(
        "portal/",
        RedirectView.as_view(pattern_name="portal:home", permanent=False),
    ),

    # WCG One apps (modelos/vistas coexistentes bajo namespace)
    path("wcgone/core/", include("apps.core.urls")),
    path("wcgone/crm/", include("apps.crm.urls")),
    path("wcgone/risk/", include("apps.risk.urls")),
    path("wcgone/pgo/", include("apps.pgo.urls")),
    path("wcgone/", include("apps.portal.urls")),
    path("wcgone/pgc/", include("apps.pgc.urls")),
    path("wcgone/legacy-pgc1/", include("apps.legacy_pgc1.urls")),

    # PGC productivo (mantener rutas actuales)
    path("", include("pgc.urls")),
]
