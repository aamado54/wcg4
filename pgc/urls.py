# pgc/urls.py

from django.urls import path
from . import admin_views, tv_charts, views

app_name = "pgc"

urlpatterns = [
    path("tablero/", views.pgc_dashboard, name="dashboard"),
    path("pgc/", views.pgc_home, name="module_home"),
    path("clientes-nuevos/", views.clientes_nuevos_report, name="clientes_nuevos"),
    path("export/dashboard.md", views.pgc_dashboard_export_md, name="dashboard_export_md"),
    path("venta-cruzada/", views.venta_cruzada_report, name="venta_cruzada"),
    path("export/venta-cruzada.md", views.venta_cruzada_export_md, name="venta_cruzada_export_md"),
    path("respuesta-reqs/", views.respuesta_reqs_report, name="respuesta_reqs"),
    path("export/respuesta-reqs.md", views.respuesta_reqs_export_md, name="respuesta_reqs_export_md"),
    path("admin-hub/", admin_views.admin_hub, name="admin_hub"),
    path("admin-hub/mensual/", admin_views.admin_monthly, name="admin_monthly"),
    path(
        "admin-hub/recalcular/",
        admin_views.admin_smart_recalc,
        name="admin_smart_recalc",
    ),
    path("admin-hub/mensual/edicion/", admin_views.admin_manual_edit, name="admin_manual_edit"),
    path(
        "admin-hub/mensual/ingresos/",
        admin_views.admin_ingresos_year,
        name="admin_ingresos_year",
    ),
    path("admin-hub/mensual/bitacora/", admin_views.admin_monthly_log, name="admin_monthly_log"),
    path(
        "admin-hub/mensual/clientes-nuevos/",
        admin_views.admin_new_clients_browse,
        name="admin_new_clients_browse",
    ),
    path(
        "admin-hub/mensual/clientes-nuevos/une/",
        admin_views.admin_new_clients_une,
        name="admin_new_clients_une",
    ),
    path("admin-hub/tv-charts/", tv_charts.admin_tv_charts, name="admin_tv_charts"),
    path(
        "admin-hub/tv-charts/upload/",
        tv_charts.tv_charts_upload,
        name="tv_charts_upload",
    ),
    path(
        "admin-hub/tv-charts/archivo/<path:name>",
        tv_charts.tv_archive_png,
        name="tv_archive_png",
    ),
    path("tv/<str:name>", tv_charts.tv_live_png, name="tv_live_png"),
    path(
        "admin-hub/run-recalc-pgc",
        admin_views.legacy_run_recalc_pgc,
        name="run_recalc_pgc",
    ),

    path(
        "admin-hub/run-recalc-investment-ingresos/",
        admin_views.legacy_run_recalc_investment,
        name="run_recalc_investment_ingresos",
    ),
  
    path(
        "admin-hub/ingresos-manual-capture",
        admin_views.redirect_manual_results,
        name="ingresos_manual_capture",
    ),

    path(
        "admin-hub/exchange-rates/",
        admin_views.redirect_manual_fx,
        name="exchange_rates_manual_capture",
    ),
  
    path("ingresos/", views.ingresos_report, name="ingresos"),
    path("export/ingresos.md", views.ingresos_export_md, name="ingresos_export_md"),
    path("export/clientes-nuevos.md", views.clientes_nuevos_export_md, name="clientes_nuevos_export_md"),
    path("clientes-nuevos/detalle/", views.clientes_nuevos_detail, name="clientes_nuevos_detail"),
    path(
        "venta-cruzada/detalle/",
        views.venta_cruzada_detail,
        name="venta_cruzada_detail",
        ),
]
