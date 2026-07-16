# pgc/views.py

import json
import re
from .models import (
    PGCPlan,
    MonthlyMetricResult,
    MonthlyScorecard,
    MonthlyTarget,
    MonthlyMetricScore,
    MonthlyModeScorecard,
    MonthlyExchangeRate,
)
from accounts.models import UserUNEPermission
from core.models import MetricDefinition, UNE, SystemSetting

from datetime import datetime
from decimal import Decimal, ROUND_DOWN, InvalidOperation
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.management import call_command
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import smart_str
from imports.models import NewClientImportRow, CrossSaleImportRow


DEFAULT_MONTH_COUNT = 4
MAX_MONTH_COUNT = 24

REPORT_DATE_ORDER_OPTIONS = ("asc", "desc")
REPORT_GROUP_MODE_OPTIONS = ("une", "period")

DEFAULT_REPORT_DATE_ORDER = "asc"
DEFAULT_REPORT_GROUP_MODE = "une"

report_une_order = {
    "FACTORING": 1,
    "FACTORAJE": 1,
    "LEASING": 2,
    "INSURANCE": 3,
    "INVESTMENT": 4,
    "INVESTMENTS": 4,
    "INVERSIONES": 4,
}

PGC_MODE_KEY = "pgc.mode"
PGC_DEFAULT_MODE = "modo1"
PGC_MODE_OPTIONS = ("modo1", "modo2")
DEFAULT_PGC_MODE = "modo1"


from pgc.investment_ingresos import (
    build_fx_map,
    convert_row_amount_to_usd,
    get_investment_une,
    investment_real_map_for_periods,
)


def _convert_row_amount_to_usd(row, fx_map):
    """Compat: delega al helper compartido con la vista/comando de Investment."""
    return convert_row_amount_to_usd(row, fx_map)
  

def _get_pgc_mode(request):
    raw_mode = (request.GET.get("mode") or request.session.get("pgc_mode") or DEFAULT_PGC_MODE).strip().lower()

    if raw_mode not in PGC_MODE_OPTIONS:
        raw_mode = DEFAULT_PGC_MODE

    request.session["pgc_mode"] = raw_mode
    return raw_mode
  

def get_pgc_mode():
    setting = SystemSetting.objects.filter(key=PGC_MODE_KEY).first()
    if not setting or not setting.value_text:
        return PGC_DEFAULT_MODE
    value = setting.value_text.strip().lower()
    return value if value in ("modo1", "modo2") else PGC_DEFAULT_MODE

def set_pgc_mode(mode: str):
    if mode not in ("modo1", "modo2"):
        mode = PGC_DEFAULT_MODE
    SystemSetting.objects.update_or_create(
        key=PGC_MODE_KEY,
        defaults={"value_text": mode},
    )


def get_default_month_count():
    fallback = DEFAULT_MONTH_COUNT

    setting = SystemSetting.objects.filter(key="pgc.default_month_count").first()
    if not setting or setting.value_text in (None, ""):
        return fallback

    try:
        value = int(str(setting.value_text).strip())
    except (TypeError, ValueError):
        return fallback

    if value < 1:
        return fallback
    if value > MAX_MONTH_COUNT:
        return MAX_MONTH_COUNT

    return value


def get_active_pgc_plan():
    plan = PGCPlan.objects.filter(is_active=True).order_by("-year").first()
    if plan:
        return plan
    return PGCPlan.objects.order_by("-year").first()


def parse_decimal_or_none(raw_value):
    if raw_value is None:
        return None

    text = str(raw_value).strip()
    if text == "":
        return None

    text = text.replace(" ", "")

    if "," in text and "." in text:
        text = text.replace(",", "")
    elif "," in text:
        text = text.replace(",", ".")

    try:
        return Decimal(text)
    except (InvalidOperation, ValueError):
        return None


def _get_active_pgc_plan():
    return get_active_pgc_plan()
  

def _get_dashboard_rows(periods=None, mode=DEFAULT_PGC_MODE):
    active_plan = _get_active_pgc_plan()
    if not active_plan:
        return []

    scorecards = (
        MonthlyModeScorecard.objects
        .select_related("une", "plan")
        .filter(plan=active_plan, mode=mode)
        .order_by("-year", "-month", "une__sort_order", "une__name_es")
    )

    metric_results = (
        MonthlyMetricScore.objects
        .select_related("une", "metric", "plan")
        .filter(plan=active_plan, mode=mode)
    )

    if periods:
        period_q = _build_period_q(periods)
        scorecards = scorecards.filter(period_q)
        metric_results = metric_results.filter(period_q)

    use_legacy = not scorecards.exists()

    if use_legacy:
        scorecards = (
            MonthlyScorecard.objects
            .select_related("une", "plan")
            .filter(plan=active_plan)
            .order_by("-year", "-month", "une__sort_order", "une__name_es")
        )

        metric_results = (
            MonthlyMetricResult.objects
            .select_related("une", "metric", "plan")
            .filter(plan=active_plan)
        )

        if periods:
            period_q = _build_period_q(periods)
            scorecards = scorecards.filter(period_q)
            metric_results = metric_results.filter(period_q)

    metric_map = {}
    for metric_result in metric_results:
        key = (
            metric_result.plan_id,
            metric_result.une_id,
            metric_result.year,
            metric_result.month,
        )
        metric_map.setdefault(key, {})
        metric_map[key][metric_result.metric.code] = metric_result

    rows = []
    for scorecard in scorecards:
        key = (
            scorecard.plan_id,
            scorecard.une_id,
            scorecard.year,
            scorecard.month,
        )
        metrics = metric_map.get(key, {})

        rows.append(
            {
                "scorecard": scorecard,
                "year": scorecard.year,
                "month": scorecard.month,
                "une": scorecard.une,
                "p_ingresos": getattr(
                    metrics.get(MetricDefinition.CODE_INGRESOS),
                    "points_awarded",
                    0,
                ),
                "p_clientes": getattr(
                    metrics.get(MetricDefinition.CODE_CLIENTES_NUEVOS),
                    "points_awarded",
                    0,
                ),
                "p_venta_cruzada": getattr(
                    metrics.get(MetricDefinition.CODE_VENTA_CRUZADA),
                    "points_awarded",
                    0,
                ),
                "p_respuesta_reqs": getattr(
                    metrics.get(MetricDefinition.CODE_RESPUESTA_REQS),
                    "points_awarded",
                    0,
                ),
                "total_points": getattr(scorecard, "total_points", 0),
                "is_month_qualified": getattr(scorecard, "is_month_qualified", False),
            }
        )

    return rows



def get_report_row_meta(row):
    if row.get("is_separator"):
        return None

    source = row.get("target") or row.get("scorecard") or row.get("result")
    if source is None:
        raise ValueError("No se pudo inferir target, scorecard o result para ordenar la fila.")

    une = getattr(source, "une", None)
    year = getattr(source, "year", None)
    month = getattr(source, "month", None)

    une_code = (getattr(une, "code", "") or "").upper()
    une_name = (
        getattr(une, "name_es", None)
        or getattr(une, "name", None)
        or une_code
    )

    une_sort_order = report_une_order.get(une_code)
    if une_sort_order is None:
        une_sort_order = getattr(une, "sort_order", None)
    if une_sort_order is None:
        une_sort_order = getattr(une, "sort_order", None)
    if une_sort_order is None:
        une_sort_order = 999999

    return {
        "une_code": une_code,
        "une_name": une_name,
        "une_sort_order": une_sort_order,
        "year": year,
        "month": month,
    }


def sort_report_rows(rows, report_sort):
    date_order = report_sort["date_order"]
    group_mode = report_sort["group_mode"]
    reverse_date = date_order == "desc"

    enriched_rows = []
    for row in rows:
        row_meta = get_report_row_meta(row)
        enriched_rows.append((row_meta, row))

    if group_mode == "une":
        enriched_rows.sort(
            key=lambda item: (
                item[0]["une_sort_order"],
                item[0]["une_name"].lower(),
                -item[0]["year"] if reverse_date else item[0]["year"],
                -item[0]["month"] if reverse_date else item[0]["month"],
            )
        )
    else:
        enriched_rows.sort(
            key=lambda item: (
                -item[0]["year"] if reverse_date else item[0]["year"],
                -item[0]["month"] if reverse_date else item[0]["month"],
                item[0]["une_sort_order"],
                item[0]["une_name"].lower(),
            )
        )

    sorted_rows = [row for _, row in enriched_rows]

    if group_mode != "une":
        return sorted_rows

    separated_rows = []
    previous_une_key = None

    for row in sorted_rows:
        row_meta = get_report_row_meta(row)
        current_une_key = (
            row_meta["une_sort_order"],
            row_meta["une_name"].lower(),
        )

        if previous_une_key is not None and current_une_key != previous_une_key:
            separated_rows.append({"is_separator": True})

        separated_rows.append(row)
        previous_une_key = current_une_key

    return separated_rows


def get_report_sort(request):
    raw_date_order = (
        request.GET.get("date_order")
        or ""
    ).strip().lower()

    raw_group_mode = (
        request.GET.get("group_mode")
        or ""
    ).strip().lower()

    session_date_order = (
        request.session.get("pgc_report_date_order")
        or DEFAULT_REPORT_DATE_ORDER
    ).strip().lower()

    session_group_mode = (
        request.session.get("pgc_report_group_mode")
        or DEFAULT_REPORT_GROUP_MODE
    ).strip().lower()

    date_order = raw_date_order or session_date_order
    group_mode = raw_group_mode or session_group_mode

    if date_order not in REPORT_DATE_ORDER_OPTIONS:
        date_order = DEFAULT_REPORT_DATE_ORDER

    if group_mode not in REPORT_GROUP_MODE_OPTIONS:
        group_mode = DEFAULT_REPORT_GROUP_MODE

    request.session["pgc_report_date_order"] = date_order
    request.session["pgc_report_group_mode"] = group_mode

    return {
        "date_order": date_order,
        "group_mode": group_mode,
    }


def get_ingresos_row_meta(row):
    source = row.get("target") or row.get("scorecard")
    if source is None:
        raise KeyError("La fila no contiene ni 'target' ni 'scorecard'.")

    une = source.une
    une_code = (getattr(une, "code", "") or "").upper()
    une_name = getattr(une, "name_es", "") if hasattr(une, "name_es") else getattr(une, "name_es", "")

    une_sort_order = report_une_order.get(une_code)
    if une_sort_order is None:
        une_sort_order = getattr(une, "sort_order", None) if hasattr(une, "sort_order") else getattr(une, "sort_order", None)
    if une_sort_order is None:
        une_sort_order = 999999

    return {
        "une_code": une_code,
        "une_name": une_name or une_code,
        "une_sort_order": une_sort_order,
        "year": source.year,
        "month": source.month,
    }


def sort_ingresos_rows(rows, report_sort):
    date_order = report_sort["date_order"]
    group_mode = report_sort["group_mode"]

    reverse_date = date_order == "desc"

    enriched_rows = []
    for row in rows:
        row_meta = get_ingresos_row_meta(row)
        enriched_rows.append((row_meta, row))

    if group_mode == "une":
        enriched_rows.sort(
            key=lambda item: (
                item[0]["une_sort_order"],
                item[0]["une_name"].lower(),
                -item[0]["year"] if reverse_date else item[0]["year"],
                -item[0]["month"] if reverse_date else item[0]["month"],
            )
        )
    else:
        enriched_rows.sort(
            key=lambda item: (
                -item[0]["year"] if reverse_date else item[0]["year"],
                -item[0]["month"] if reverse_date else item[0]["month"],
                item[0]["une_sort_order"],
                item[0]["une_name"].lower(),
            )
        )

    sorted_rows = [row for _, row in enriched_rows]

    if group_mode != "une":
        return sorted_rows

    separated_rows = []
    previous_une_key = None

    for row in sorted_rows:
        row_meta = get_ingresos_row_meta(row)
        current_une_key = (
            row_meta["une_sort_order"],
            row_meta["une_name"].lower(),
        )

        if previous_une_key is not None and current_une_key != previous_une_key:
            separated_rows.append({"is_separator": True})

        separated_rows.append(row)
        previous_une_key = current_une_key

    return separated_rows


def _safe_int(value, default=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _build_period_range(start_year, start_month, month_count):
  
    periods = []
    year = start_year
    month = start_month

    for _ in range(month_count):
        periods.append((year, month))
        month += 1
        if month > 12:
            month = 1
            year += 1

    return periods


def _period_range_end(start_year, start_month, month_count):
    """Mes final inclusivo del rango (start + month_count - 1)."""
    periods = _build_period_range(start_year, start_month, month_count)
    if not periods:
        return start_year, start_month
    return periods[-1]


def _build_ytd_period_range(end_year, end_month):
    """Enero del año del mes final → mes final (inclusive)."""
    end_month = max(1, min(12, int(end_month)))
    return [(end_year, m) for m in range(1, end_month + 1)]


def _build_period_q(periods):
    query = Q()
    for year, month in periods:
        query |= Q(year=year, month=month)
    return query  


def _get_available_periods(mode=None):
    active_plan = _get_active_pgc_plan()
    if not active_plan:
        return []

    periods = list(
        MonthlyModeScorecard.objects
        .filter(plan=active_plan, mode=mode or DEFAULT_PGC_MODE)
        .order_by("-year", "-month")
        .values_list("year", "month")
        .distinct()
    )

    if not periods:
        periods = list(
            MonthlyScorecard.objects
            .filter(plan=active_plan)
            .order_by("-year", "-month")
            .values_list("year", "month")
            .distinct()
        )

    return [
        {
            "year": year,
            "month": month,
            "key": f"{year}-{month:02d}",
        }
        for year, month in periods
    ]


MONTH_COUNT_OPTIONS = [2, 3, 4, 6, 9, 12]


def shift_month(year, month, delta):
    total = year * 12 + (month - 1) + delta
    new_year = total // 12
    new_month = total % 12 + 1
    return new_year, new_month
  

def _get_report_filter(request, mode=DEFAULT_PGC_MODE):
    dynamic_default_month_count = get_default_month_count()

    get_start_year = _safe_int(request.GET.get("start_year"))
    get_start_month = _safe_int(request.GET.get("start_month"))
    get_month_count = _safe_int(request.GET.get("month_count"))

    session_start_year = _safe_int(request.session.get("pgc_report_start_year"))
    session_start_month = _safe_int(request.session.get("pgc_report_start_month"))
    session_month_count = _safe_int(request.session.get("pgc_report_month_count"))

    month_count = get_month_count or session_month_count or dynamic_default_month_count
    if month_count < 1:
        month_count = dynamic_default_month_count
    if month_count > MAX_MONTH_COUNT:
        month_count = MAX_MONTH_COUNT

    start_year = get_start_year or session_start_year
    start_month = get_start_month or session_start_month

    if not start_year or not start_month or start_month < 1 or start_month > 12:
        active_plan = _get_active_pgc_plan()

        if active_plan:
            latest_period = (
                MonthlyModeScorecard.objects
                .filter(plan=active_plan, mode=mode)
                .order_by("-year", "-month")
                .values("year", "month")
                .first()
            )

            if not latest_period:
                latest_period = (
                    MonthlyScorecard.objects
                    .filter(plan=active_plan)
                    .order_by("-year", "-month")
                    .values("year", "month")
                    .first()
                )

            if latest_period:
                start_year, start_month = shift_month(
                    latest_period["year"],
                    latest_period["month"],
                    -(month_count - 1),
                )
            else:
                now = datetime.now()
                start_year, start_month = shift_month(
                    now.year,
                    now.month,
                    -(month_count - 1),
                )
        else:
            now = datetime.now()
            start_year, start_month = shift_month(
                now.year,
                now.month,
                -(month_count - 1),
            )

    request.session["pgc_report_start_year"] = start_year
    request.session["pgc_report_start_month"] = start_month
    request.session["pgc_report_month_count"] = month_count

    return {
        "start_year": start_year,
        "start_month": start_month,
        "month_count": month_count,
    }


@login_required
def pgc_home(request):
    """Acceso directo al tablero PGC (sin pantalla intermedia)."""
    return redirect("pgc:dashboard")


def splash(request):
    """
    Pantalla inicial: muestra splash y, al primer click/tecla,
    redirige al tablero principal.
    """
    # Si ya está autenticado, igual mostramos splash una vez.
    return render(request, "splash.html")


@login_required
def pgc_dashboard_export_md(request):
    report_filter = _get_report_filter(request)
    report_sort = get_report_sort(request)
    selected_mode = _get_pgc_mode(request)

    periods = _build_period_range(
        report_filter["start_year"],
        report_filter["start_month"],
        report_filter["month_count"],
    )

    rows = _get_dashboard_rows(periods=periods, mode=selected_mode)
    rows = sort_report_rows(rows, report_sort)

    content = _build_dashboard_markdown(
        rows,
        report_filter,
        selected_mode=selected_mode,
    )

    generated_suffix = datetime.now().strftime("%Y%m%d-%H%M")
    start_year = report_filter["start_year"]
    start_month = report_filter["start_month"]
    month_count = report_filter["month_count"]

    filename = (
        f"pgc-tablero-principal-"
        f"{selected_mode}-"
        f"fy{start_year}-m{start_month:02d}-n{month_count}-"
        f"{generated_suffix}.md"
    )

    response = HttpResponse(
        smart_str(content),
        content_type="text/plain; charset=utf-8",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@login_required
def pgc_dashboard(request):
    selected_mode = _get_pgc_mode(request)
    report_filter = _get_report_filter(request, mode=selected_mode)
    report_sort = get_report_sort(request)

    periods = _build_period_range(
        report_filter["start_year"],
        report_filter["start_month"],
        report_filter["month_count"],
    )

    rows = _get_dashboard_rows(periods=periods, mode=selected_mode)
    rows = sort_report_rows(rows, report_sort)

    chart_payload = _build_dashboard_chart_payload(
        periods=periods,
        mode=selected_mode,
    )

    # Serie aparte para exportación SVG 4-charts: siempre enero → mes final del rango.
    end_year, end_month = _period_range_end(
        report_filter["start_year"],
        report_filter["start_month"],
        report_filter["month_count"],
    )
    ytd_periods = _build_ytd_period_range(end_year, end_month)
    ytd_payload = _build_dashboard_chart_payload(
        periods=ytd_periods,
        mode=selected_mode,
    )
    ingresos_ytd = (ytd_payload.get("metrics") or {}).get(
        MetricDefinition.CODE_INGRESOS, {}
    )
    chart_payload["export_ingresos"] = {
        "end_year": end_year,
        "end_month": end_month,
        "periods": ingresos_ytd.get("periods") or [],
        "y_axis": ingresos_ytd.get("y_axis") or "Cifras en miles de US$",
    }

    context = {
        "rows": rows,
        "report_filter": report_filter,
        "report_sort": report_sort,
        "selected_mode": selected_mode,
        "mode_options": PGC_MODE_OPTIONS,
        "available_periods": _get_available_periods(mode=selected_mode),
        "month_count_options": MONTH_COUNT_OPTIONS,
        "chart_payload_json": json.dumps(chart_payload, ensure_ascii=False),
        "chart_rows": [
            {
                "une": row["une"].name_es,
                "periodo": f"{row['year']}-{row['month']:02d}",              
                "p_ingresos": row["p_ingresos"],
                "p_clientes": row["p_clientes"],
                "p_venta_cruzada": row["p_venta_cruzada"],
                "p_respuesta_reqs": row["p_respuesta_reqs"],
                "total": row["total_points"],
            }
            for row in rows
            if not row.get("is_separator")
        ],
    }
    return render(request, "pgc/dashboard.html", context)
  

def _decimal_to_number(value):
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        return None


def _build_dashboard_chart_payload(periods=None, mode=DEFAULT_PGC_MODE):
    active_plan = get_active_pgc_plan()
    if not active_plan:
        return {"periods": [], "unes": [], "metrics": {}}

    metric_codes = [
        MetricDefinition.CODE_INGRESOS,
        MetricDefinition.CODE_CLIENTES_NUEVOS,
        MetricDefinition.CODE_VENTA_CRUZADA,
    ]

    targets = (
        MonthlyTarget.objects
        .select_related("une", "plan", "metric")
        .filter(plan=active_plan, metric__code__in=metric_codes)
    )

    results = (
        MonthlyMetricResult.objects
        .select_related("une", "plan", "metric")
        .filter(plan=active_plan, metric__code__in=metric_codes)
    )

    if periods:
        period_q = _build_period_q(periods)
        targets = targets.filter(period_q)
        results = results.filter(period_q)

    target_map = {}
    for t in targets:
        key = (t.metric.code, t.year, t.month, t.une.code)
        target_map[key] = _decimal_to_number(t.target_value)

    result_map = {}
    for r in results:
        key = (r.metric.code, r.year, r.month, r.une.code)
        result_map[key] = _decimal_to_number(r.measured_value)

    une_map = {}
    for t in targets:
        une_map[t.une.code] = {
            "code": t.une.code,
            "name_es": t.une.name_es,
            "sort_order": t.une.sort_order,
        }
    for r in results:
        une_map[r.une.code] = {
            "code": r.une.code,
            "name_es": r.une.name_es,
            "sort_order": r.une.sort_order,
        }

    unes = sorted(
        une_map.values(),
        key=lambda x: (x["sort_order"] if x["sort_order"] is not None else 999999, x["name_es"])
    )

    periods_list = []
    for year, month in (periods or []):
        periods_list.append({
            "year": year,
            "month": month,
            "key": f"{year}-{month:02d}",
            "label": f"{year}-{month:02d}",
        })

    series = {}
    for metric_code in metric_codes:
        metric_periods = []
        for year, month in (periods or []):
            by_une = {}
            for une in unes:
                une_code = une["code"]
                by_une[une_code] = {
                    "target": target_map.get((metric_code, year, month, une_code), 0),
                    "real": result_map.get((metric_code, year, month, une_code), 0),
                }

            metric_periods.append({
                "year": year,
                "month": month,
                "key": f"{year}-{month:02d}",
                "label": f"{year}-{month:02d}",
                "by_une": by_une,
            })

        series[metric_code] = metric_periods
    return {
        "periods": periods_list,
        "unes": [
            {"code": u["code"], "name_es": u["name_es"]}
            for u in unes
        ],
        "metrics": {
            MetricDefinition.CODE_INGRESOS: {
                "title": "Ingresos brutos",
                "subtitle": "Real vs meta por período",
                "y_axis": "Cifras en miles de US$",
                "metric_code": MetricDefinition.CODE_INGRESOS,
                "periods": series[MetricDefinition.CODE_INGRESOS],
            },
            MetricDefinition.CODE_CLIENTES_NUEVOS: {
                "title": "Clientes nuevos",
                "subtitle": "Real vs meta por período",
                "y_axis": "Cantidad de clientes",
                "metric_code": MetricDefinition.CODE_CLIENTES_NUEVOS,
                "periods": series[MetricDefinition.CODE_CLIENTES_NUEVOS],
            },
            MetricDefinition.CODE_VENTA_CRUZADA: {
                "title": "Venta cruzada",
                "subtitle": "Real vs meta por período",
                "y_axis": "Cantidad",
                "metric_code": MetricDefinition.CODE_VENTA_CRUZADA,
                "periods": series[MetricDefinition.CODE_VENTA_CRUZADA],
            },
        },
    }


def _build_dashboard_markdown(rows, report_filter, selected_mode="modo1"):
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    start_year = report_filter["start_year"]
    start_month = report_filter["start_month"]
    month_count = report_filter["month_count"]

    periods = _build_period_range(start_year, start_month, month_count)
    end_year, end_month = periods[-1]

    lines = [
        "PGC - Tablero principal de puntos por UNE y mes",
        "",
        f"Generado: {generated_at}",
        "",
        "Filtros",
        f"- Modalidad: {selected_mode}",
        f"- Desde: {start_year}-{start_month:02d}",
        f"- Hasta: {end_year}-{end_month:02d}",
        f"- Meses incluidos: {month_count}",
        "",
        "Descripción",
        "Resumen mensual de puntos por UNE y periodo.",
        "",
        "Datos",
        "",
        "| UNE | Periodo | Puntos ingresos | Puntos clientes nuevos | Puntos venta cruzada | Puntos respuesta reqs | Total | Clasifica |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    if not rows:
        lines.append("| Sin datos | - | - | - | - | - | - | - |")
    else:
        for row in rows:
            if row.get("is_separator"):
                continue

            clasifica = "Sí" if row["is_month_qualified"] else "No"
            periodo = f"{row['year']}-{row['month']:02d}"

            lines.append(
                f"| {row['une'].name_es} | {periodo} | "
                f"{row['p_ingresos']} | {row['p_clientes']} | "
                f"{row['p_venta_cruzada']} | {row['p_respuesta_reqs']} | "
                f"{row['total_points']} | {clasifica} |"
            )

    lines.extend([
        "",
        "Nota",
        "Este reporte muestra el puntaje total y sus componentes por UNE y periodo.",
        "",
    ])

    return "\n".join(lines)


@login_required
def clientes_nuevos_report(request):
    report_filter = _get_report_filter(request)
    report_sort = get_report_sort(request)

    periods = _build_period_range(
        report_filter["start_year"],
        report_filter["start_month"],
        report_filter["month_count"],
    )

    metric, rows = _get_clientes_nuevos_rows(periods=periods)
    rows = sort_report_rows(rows, report_sort)
    
    context = {
        "rows": rows,
        "metric": metric,
        "report_filter": report_filter,
        "report_sort": report_sort,
        "available_periods": _get_available_periods(),
        "month_count_options": MONTH_COUNT_OPTIONS,
    }
    return render(request, "pgc/clientes_nuevos.html", context)


def _get_clientes_nuevos_rows(periods=None):
    try:
        metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_CLIENTES_NUEVOS)
    except MetricDefinition.DoesNotExist:
        metric = None

    targets = MonthlyTarget.objects.select_related("une", "plan").filter(
        metric__code=MetricDefinition.CODE_CLIENTES_NUEVOS
    )
    results = MonthlyMetricResult.objects.select_related("une", "plan", "metric").filter(
        metric__code=MetricDefinition.CODE_CLIENTES_NUEVOS
    )
    scorecards = MonthlyScorecard.objects.select_related("une", "plan")

    if periods:
        period_q = _build_period_q(periods)
        targets = targets.filter(period_q)
        results = results.filter(period_q)
        scorecards = scorecards.filter(period_q)

    result_map = {}
    for r in results:
        key = (r.plan_id, r.une_id, r.year, r.month)
        result_map[key] = r

    score_map = {}
    for sc in scorecards:
        key = (sc.plan_id, sc.une_id, sc.year, sc.month)
        score_map[key] = sc

    detail_rows = NewClientImportRow.objects.filter(une__isnull=False)

    if periods:
        detail_period_q = Q()
        for year, month in periods:
            detail_period_q |= Q(year=year, month=month)
            detail_period_q |= Q(header__year=year, header__month=month)
        detail_rows = detail_rows.filter(detail_period_q)

    detail_keys = set()

    for row in detail_rows.select_related("header"):
        row_year = row.year or (row.header.year if row.header else None)
        row_month = row.month or (row.header.month if row.header else None)

        if row.une_id and row_year and row_month:
            detail_keys.add((row.une_id, row_year, row_month))

    investment_new_clients_map = {}
    investment_ingresos_map = {}
    
    investment_une = (
        UNE.objects.filter(code__in=["INVESTMENT", "INVESTMENTS", "INVERSIONES"])
        .order_by("sort_order", "id")
        .first()
    )
    
    fx_map = {
        (item.year, item.month): item.usd_to_gtq
        for item in MonthlyExchangeRate.objects.all()
    }
    
    if investment_une:
        for row in detail_rows.select_related("currency", "header"):
            row_year = row.year or (row.header.year if row.header else None)
            row_month = row.month or (row.header.month if row.header else None)
    
            if row.une_id != investment_une.id or not row_year or not row_month:
                continue
    
            key = (row.une_id, row_year, row_month)
    
            if row.counts_as_new:
                investment_new_clients_map[key] = investment_new_clients_map.get(key, 0) + 1
    
            investment_ingresos_map[key] = (
                investment_ingresos_map.get(key, Decimal("0"))
                + _convert_row_amount_to_usd(row, fx_map)
            )
  
    rows = []
    for t in targets.order_by("year", "month", "une__sort_order"):
        key = (t.plan_id, t.une_id, t.year, t.month)
        mr = result_map.get(key)
        sc = score_map.get(key)

        real_value_override = None
        if investment_une and t.une_id == investment_une.id:
            real_value_override = investment_new_clients_map.get((t.une_id, t.year, t.month), 0)
      
        rows.append(
            {
                "target": t,
                "result": mr,
                "scorecard": sc,
                "has_detail": (t.une_id, t.year, t.month) in detail_keys,
                "investment_ingresos": investment_ingresos_map.get((t.une_id, t.year, t.month)),
                "real_value_override": real_value_override,
            }
        )
      
    return metric, rows


def _build_clientes_nuevos_markdown(rows, report_filter):
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    start_year = report_filter["start_year"]
    start_month = report_filter["start_month"]
    month_count = report_filter["month_count"]
    periods = _build_period_range(start_year, start_month, month_count)
    end_year, end_month = periods[-1]

    lines = [
        "# PGC - Clientes nuevos vs meta",
        "",
        f"Generado: {generated_at}",
        "",
        "## Filtros",
        f"- Desde: {start_year}-{start_month:02d}",
        f"- Hasta: {end_year}-{end_month:02d}",
        f"- Meses incluidos: {month_count}",
        "",
        "## Descripción",
        "Meta y resultado mensual de clientes nuevos por UNE y periodo.",
        "",
        "## Datos",
        "",
        "| UNE | Periodo | Meta clientes | Clientes reales | Cumple | Puntos asignados | Total del mes |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]

    if not rows:
        lines.append("| Sin datos | - | - | - | - | - | - |")
    else:
        for row in rows:
            if row.get("is_separator"):
                continue
        
            target = row["target"]
            result = row["result"]
            scorecard = row["scorecard"]

            periodo = f"{target.year}-{target.month:02d}"
            meta = int(target.target_value) if target.target_value is not None else "-"
            
            real_override = row.get("real_value_override", None)
            if real_override is not None:
                reales = int(real_override)
            else:
                reales = int(result.measured_value) if result and result.measured_value is not None else "-"
          
            cumple = "Sí" if result and result.is_achieved else "No"
            puntos = result.points_awarded if result else 0
            total_mes = scorecard.total_points if scorecard else 0

            lines.append(
                f"| {target.une.name_es} | {periodo} | {meta} | {reales} | {cumple} | {puntos} | {total_mes} |"
            )

    lines.extend([
        "",
        "## Nota",
        "Este reporte muestra la meta mensual de clientes nuevos, el resultado observado y su impacto en el puntaje total del mes.",
        "",
    ])
    return "\n".join(lines)


@login_required
def clientes_nuevos_export_md(request):
    report_filter = _get_report_filter(request)
    report_sort = get_report_sort(request)
    periods = _build_period_range(
        report_filter["start_year"],
        report_filter["start_month"],
        report_filter["month_count"],
    )
    metric, rows = _get_clientes_nuevos_rows(periods=periods)
    rows = sort_report_rows(rows, report_sort)

    content = _build_clientes_nuevos_markdown(rows, report_filter)

    generated_suffix = datetime.now().strftime("%Y%m%d-%H%M")
    start_year = report_filter["start_year"]
    start_month = report_filter["start_month"]
    month_count = report_filter["month_count"]
    filename = (
        f"pgc-clientes-nuevos-"
        f"fy{start_year}-m{start_month:02d}-n{month_count}-"
        f"{generated_suffix}.md"
    )

    response = HttpResponse(
        smart_str(content),
        content_type="text/plain; charset=utf-8",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def _get_venta_cruzada_rows(periods=None):
    try:
        metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_VENTA_CRUZADA)
    except MetricDefinition.DoesNotExist:
        metric = None

    targets = MonthlyTarget.objects.select_related("une", "plan").filter(
        metric__code=MetricDefinition.CODE_VENTA_CRUZADA
    )
    results = MonthlyMetricResult.objects.select_related("une", "plan", "metric").filter(
        metric__code=MetricDefinition.CODE_VENTA_CRUZADA
    )
    scorecards = MonthlyScorecard.objects.select_related("une", "plan")

    if periods:
        period_q = _build_period_q(periods)
        targets = targets.filter(period_q)
        results = results.filter(period_q)
        scorecards = scorecards.filter(period_q)

    result_map = {}
    for r in results:
        key = (r.plan_id, r.une_id, r.year, r.month)
        result_map[key] = r

    score_map = {}
    for sc in scorecards:
        key = (sc.plan_id, sc.une_id, sc.year, sc.month)
        score_map[key] = sc

    rows = []
    for t in targets.order_by("year", "month", "une__sort_order"):
        key = (t.plan_id, t.une_id, t.year, t.month)
        mr = result_map.get(key)
        sc = score_map.get(key)
        rows.append({
            "target": t,
            "result": mr,
            "scorecard": sc,
        })

    return metric, rows
  

@login_required
def venta_cruzada_report(request):
    report_filter = _get_report_filter(request)
    report_sort = get_report_sort(request)

    periods = _build_period_range(
        report_filter["start_year"],
        report_filter["start_month"],
        report_filter["month_count"],
    )

    metric, rows = _get_venta_cruzada_rows(periods=periods)
    rows = sort_report_rows(rows, report_sort)
    
    context = {
        "rows": rows,
        "metric": metric,
        "report_filter": report_filter,
        "report_sort": report_sort,
        "available_periods": _get_available_periods(),
        "month_count_options": MONTH_COUNT_OPTIONS,
    }
    return render(request, "pgc/venta_cruzada.html", context)


def _build_venta_cruzada_markdown(rows, report_filter):
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    start_year = report_filter["start_year"]
    start_month = report_filter["start_month"]
    month_count = report_filter["month_count"]
    periods = _build_period_range(start_year, start_month, month_count)
    end_year, end_month = periods[-1]

    lines = [
        "# PGC - Venta cruzada vs meta",
        "",
        f"Generado: {generated_at}",
        "",
        "## Filtros",
        f"- Desde: {start_year}-{start_month:02d}",
        f"- Hasta: {end_year}-{end_month:02d}",
        f"- Meses incluidos: {month_count}",
        "",
        "## Descripción",
        "Meta y resultado mensual de venta cruzada por UNE y periodo.",
        "",
        "## Datos",
        "",
        "| UNE | Periodo | Meta venta cruzada | Venta cruzada real | Cumple | Puntos asignados | Total del mes |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]

    if not rows:
        lines.append("| Sin datos | - | - | - | - | - | - |")
    else:
        for row in rows:
            if row.get("is_separator"):
                continue
        
            target = row["target"]
            result = row["result"]
            scorecard = row["scorecard"]          

            periodo = f"{target.year}-{target.month:02d}"
            meta = int(target.target_value) if target.target_value is not None else "-"
            reales = int(result.measured_value) if result and result.measured_value is not None else "-"
            cumple = "Sí" if result and result.is_achieved else "No"
            puntos = result.points_awarded if result else 0
            total_mes = scorecard.total_points if scorecard else 0

            lines.append(
                f"| {target.une.name_es} | {periodo} | {meta} | {reales} | {cumple} | {puntos} | {total_mes} |"
            )

    lines.extend([
        "",
        "## Nota",
        "Este reporte muestra la meta mensual de venta cruzada, el resultado observado y su impacto en el puntaje total del mes.",
        "",
    ])
    return "\n".join(lines)


@login_required
def venta_cruzada_export_md(request):
    report_filter = _get_report_filter(request)
    report_sort = get_report_sort(request)
    periods = _build_period_range(
        report_filter["start_year"],
        report_filter["start_month"],
        report_filter["month_count"],
    )
    metric, rows = _get_venta_cruzada_rows(periods=periods)
    rows = sort_report_rows(rows, report_sort)

    content = _build_venta_cruzada_markdown(rows, report_filter)

    generated_suffix = datetime.now().strftime("%Y%m%d-%H%M")
    start_year = report_filter["start_year"]
    start_month = report_filter["start_month"]
    month_count = report_filter["month_count"]
    filename = (
        f"pgc-venta-cruzada-"
        f"fy{start_year}-m{start_month:02d}-n{month_count}-"
        f"{generated_suffix}.md"
    )

    response = HttpResponse(
        smart_str(content),
        content_type="text/plain; charset=utf-8",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def _get_respuesta_reqs_rows(periods=None):
    try:
        metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_RESPUESTA_REQS)
    except MetricDefinition.DoesNotExist:
        metric = None

    targets = MonthlyTarget.objects.select_related("une", "plan").filter(
        metric__code=MetricDefinition.CODE_RESPUESTA_REQS
    )
    results = MonthlyMetricResult.objects.select_related("une", "plan", "metric").filter(
        metric__code=MetricDefinition.CODE_RESPUESTA_REQS
    )
    scorecards = MonthlyScorecard.objects.select_related("une", "plan")

    if periods:
        period_q = _build_period_q(periods)
        targets = targets.filter(period_q)
        results = results.filter(period_q)
        scorecards = scorecards.filter(period_q)

    result_map = {}
    for r in results:
        key = (r.plan_id, r.une_id, r.year, r.month)
        result_map[key] = r

    score_map = {}
    for sc in scorecards:
        key = (sc.plan_id, sc.une_id, sc.year, sc.month)
        score_map[key] = sc

    rows = []
    for t in targets.order_by("year", "month", "une__sort_order"):
        key = (t.plan_id, t.une_id, t.year, t.month)
        mr = result_map.get(key)
        sc = score_map.get(key)
        rows.append({
            "target": t,
            "result": mr,
            "scorecard": sc,
        })

    return metric, rows
  

@login_required
def respuesta_reqs_report(request):
    report_filter = _get_report_filter(request)
    report_sort = get_report_sort(request)

    periods = _build_period_range(
        report_filter["start_year"],
        report_filter["start_month"],
        report_filter["month_count"],
    )

    metric, rows = _get_respuesta_reqs_rows(periods=periods)
    rows = sort_report_rows(rows, report_sort)

    context = {
        "rows": rows,
        "metric": metric,
        "report_filter": report_filter,
        "report_sort": report_sort,
        "available_periods": _get_available_periods(),
        "month_count_options": MONTH_COUNT_OPTIONS,
    }
    return render(request, "pgc/respuesta_reqs.html", context)


def _build_respuesta_reqs_markdown(rows, report_filter):
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    start_year = report_filter["start_year"]
    start_month = report_filter["start_month"]
    month_count = report_filter["month_count"]
    periods = _build_period_range(start_year, start_month, month_count)
    end_year, end_month = periods[-1]

    lines = [
        "# PGC - Respuesta a requerimientos vs meta",
        "",
        f"Generado: {generated_at}",
        "",
        "## Filtros",
        f"- Desde: {start_year}-{start_month:02d}",
        f"- Hasta: {end_year}-{end_month:02d}",
        f"- Meses incluidos: {month_count}",
        "",
        "## Descripción",
        "Meta y resultado mensual de respuesta a requerimientos por UNE y periodo.",
        "",
        "## Datos",
        "",
        "| UNE | Periodo | Meta respuesta reqs | Respuesta reqs real | Cumple | Puntos asignados | Total del mes |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]

    if not rows:
        lines.append("| Sin datos | - | - | - | - | - | - |")
    else:
        for row in rows:
            if row.get("is_separator"):
                continue
        
            target = row["target"]
            result = row["result"]
            scorecard = row["scorecard"]
          
            periodo = f"{target.year}-{target.month:02d}"
            meta = int(target.target_value) if target.target_value is not None else "-"
            reales = int(result.measured_value) if result and result.measured_value is not None else "-"
            cumple = "Sí" if result and result.is_achieved else "No"
            puntos = result.points_awarded if result else 0
            total_mes = scorecard.total_points if scorecard else 0

            lines.append(
                f"| {target.une.name_es} | {periodo} | {meta} | {reales} | {cumple} | {puntos} | {total_mes} |"
            )

    lines.extend([
        "",
        "## Nota",
        "Este reporte muestra la meta mensual de respuesta a requerimientos, el resultado observado y su impacto en el puntaje total del mes.",
        "",
    ])
    return "\n".join(lines)


@login_required
def respuesta_reqs_export_md(request):
    report_filter = _get_report_filter(request)
    report_sort = get_report_sort(request)
    periods = _build_period_range(
        report_filter["start_year"],
        report_filter["start_month"],
        report_filter["month_count"],
    )
    metric, rows = _get_respuesta_reqs_rows(periods=periods)
    rows = sort_report_rows(rows, report_sort)

    content = _build_respuesta_reqs_markdown(rows, report_filter)

    generated_suffix = datetime.now().strftime("%Y%m%d-%H%M")
    start_year = report_filter["start_year"]
    start_month = report_filter["start_month"]
    month_count = report_filter["month_count"]
    filename = (
        f"pgc-respuesta-reqs-"
        f"fy{start_year}-m{start_month:02d}-n{month_count}-"
        f"{generated_suffix}.md"
    )

    response = HttpResponse(
        smart_str(content),
        content_type="text/plain; charset=utf-8",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def _get_ingresos_rows(periods=None):

    investment_une = get_investment_une()
    fx_map = build_fx_map()
    investment_real_map = investment_real_map_for_periods(
        periods, une=investment_une, fx_map=fx_map
    )

  
    try:
        metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_INGRESOS)
    except MetricDefinition.DoesNotExist:
        metric = None

    targets = MonthlyTarget.objects.select_related("une", "plan", "metric").filter(
        metric__code=MetricDefinition.CODE_INGRESOS
    )
    results = MonthlyMetricResult.objects.select_related("une", "plan", "metric").filter(
        metric__code=MetricDefinition.CODE_INGRESOS
    )
    scorecards = MonthlyScorecard.objects.select_related("une", "plan")

    if periods:
        period_q = _build_period_q(periods)
        targets = targets.filter(period_q)
        results = results.filter(period_q)
        scorecards = scorecards.filter(period_q)

    result_map = {}
    for r in results:
        key = (r.plan_id, r.une_id, r.year, r.month)
        result_map[key] = r

    score_map = {}
    for sc in scorecards:
        key = (sc.plan_id, sc.une_id, sc.year, sc.month)
        score_map[key] = sc

    rows = []
    for target in targets.order_by("-year", "-month", "une__sort_order", "une__name_es"):
        key = (target.plan_id, target.une_id, target.year, target.month)
        result = result_map.get(key)
        scorecard = score_map.get(key)

        meta = target.target_value if target.target_value is not None else None
        real = result.measured_value if result and result.measured_value is not None else None

        investment_codes = {"INVESTMENT", "INVESTMENTS", "INVERSIONES"}
        
        if target.une.code in investment_codes:
            real = investment_real_map.get(
                (target.year, target.month, target.une_id),
                Decimal("0"),
            )

        # Insurance siempre con 3 decimales
        if target.une.code == "INSURANCE":
            if meta is not None:
                meta = meta.quantize(Decimal("0.001"), rounding=ROUND_DOWN)
            if real is not None:
                real = real.quantize(Decimal("0.001"), rounding=ROUND_DOWN)

        if meta is not None and real is not None:
            diferencia = real - meta
            if target.une.code == "INSURANCE":
                diferencia = diferencia.quantize(Decimal("0.001"), rounding=ROUND_DOWN)
        else:
            diferencia = None

        if target.une.code in {"INVESTMENT", "INVESTMENTS", "INVERSIONES"}:
            metodo = "Suma de montos del archivo de clientes nuevos del mes"
            observacion = (
                "En Investment, el ingreso del score mensual se calcula como la suma "
                "de montos de todos los registros del archivo de clientes del mes."
            )
            observacion_base = observacion
            tc_label = ""
        else:
            metodo = "Estado de resultados"
            observacion = ""
            observacion_base = ""
            tc_label = ""
            if result and result.calculation_note:
                note = result.calculation_note.strip()

                base_note = note
                tc_text = ""

                if "[FX_APPLIED]" in note and "GTQ a USD:" in note:
                    base_note = note.split("[FX_APPLIED]")[0].strip()

                    try:
                        fx_part = note.split("/")[1].split("=")[0].strip()
                        fx_value = Decimal(fx_part).quantize(Decimal("0.001"), rounding=ROUND_DOWN)
                        tc_text = f"TC {fx_value}"
                    except Exception:
                        tc_text = ""

                if base_note and tc_text:
                    observacion = f"{base_note} {tc_text}"
                elif base_note:
                    observacion = base_note
                elif tc_text:
                    observacion = tc_text

                observacion_base = base_note
                tc_label = tc_text

        # Presentación: TC desde captura manual GTQ→USD si no vino en calculation_note.
        if not tc_label and result and getattr(result, "exchange_rate_used", None):
            try:
                tc_label = f"TC {Decimal(result.exchange_rate_used).quantize(Decimal('0.001'), rounding=ROUND_DOWN)}"
            except Exception:
                tc_label = f"TC {result.exchange_rate_used}"

        if not tc_label and observacion:
            m = re.search(r"TC[= ]\s*([0-9]+(?:\.[0-9]+)?)", observacion, flags=re.IGNORECASE)
            if m:
                tc_label = f"TC {m.group(1)}"

        # Evitar duplicar el TC en el texto cuando ya hay badge.
        display_base = observacion_base or observacion or ""
        if tc_label and display_base:
            display_base = re.sub(
                r"\s*TC[= ]\s*[0-9]+(?:\.[0-9]+)?\s*",
                " ",
                display_base,
                flags=re.IGNORECASE,
            ).strip()

        source_gtq = None
        if (
            result
            and getattr(result, "source_currency", "") == "GTQ"
            and getattr(result, "source_value", None) is not None
        ):
            source_gtq = result.source_value

        rows.append({
            "target": target,
            "result": result,
            "scorecard": scorecard,
            "meta": meta,
            "real": real,
            "diferencia": diferencia,
            "cumple": result.is_achieved if result else False,
            "metodo": metodo,
            "observacion": observacion,
            "observacion_base": display_base,
            "tc_label": tc_label,
            "source_gtq": source_gtq,
            "is_insurance": target.une.code == "INSURANCE",  # Flag para el template
        })

    return metric, rows


def build_ingresos_markdown(rows, report_filter):
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    start_year = report_filter["start_year"]
    start_month = report_filter["start_month"]
    month_count = report_filter["month_count"]
    periods = _build_period_range(start_year, start_month, month_count)
    end_year, end_month = periods[-1]

    lines = [
        "# PGC - Ingresos vs meta por UNE",
        "",
        f"Generado: {generated_at}",
        "",
        "## Filtros",
        f"- Desde: {start_year}-{start_month:02d}",
        f"- Hasta: {end_year}-{end_month:02d}",
        f"- Meses incluidos: {month_count}",
        "",
        "## Datos",
        "",
        "| UNE | Periodo | Meta USD | Real USD | Dif. USD | Cumple | Método de cálculo | Observación |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]

    if not rows:
        lines.append("| Sin datos | - | - | - | - | - | - | - |")
    else:
        for row in rows:
            if row.get("is_separator"):
                continue

            target = row["target"]
            period = f"{target.year}-{target.month:02d}"
            meta = row["meta"]
            real = row["real"]
            diferencia = row["diferencia"]
            
            # Insurance con 3 decimales en MD
            is_insurance = target.une.code == "INSURANCE"
            
            if is_insurance:
                meta_txt = f"{meta:.3f}" if meta is not None else "-"
                real_txt = f"{real:.3f}" if real is not None else "-"
                diferencia_txt = f"{diferencia:.3f}" if diferencia is not None else "-"
            else:
                meta_txt = f"{int(meta)}" if meta is not None else "-"
                real_txt = f"{int(real)}" if real is not None else "-"
                diferencia_txt = f"{int(diferencia)}" if diferencia is not None else "-"
            
            lines.append(
                f"| {target.une.name_es if hasattr(target.une, 'name_es') else target.une.name_es} | "
                f"{period} | "
                f"{meta_txt} | "
                f"{real_txt} | "
                f"{diferencia_txt} | "
                f"{'Sí' if row['cumple'] else 'No'} | "
                f"{row['metodo']} | "
                f"{row['observacion'] or '-'} |"
            )

    lines.extend([
        "",
        "## Nota",
        "Este reporte muestra la meta de ingresos, el valor real observado y el método usado para explicar el puntaje mensual.",
        "Insurance se presenta siempre con 3 decimales.",
        "",
    ])
    return "\n".join(lines)


@login_required
def ingresos_report(request):
    report_filter = _get_report_filter(request)
    report_sort = get_report_sort(request)

    periods = _build_period_range(
        report_filter["start_year"],
        report_filter["start_month"],
        report_filter["month_count"],
    )

    metric, rows = _get_ingresos_rows(periods=periods)
    rows = sort_ingresos_rows(rows, report_sort)

    context = {
        "rows": rows,
        "metric": metric,
        "report_filter": report_filter,
        "report_sort": report_sort,
        "available_periods": _get_available_periods(),
        "month_count_options": MONTH_COUNT_OPTIONS,
    }

    return render(request, "pgc/ingresos.html", context)


@login_required
def ingresos_export_md(request):
    report_filter = _get_report_filter(request)
    report_sort = get_report_sort(request)

    periods = _build_period_range(
        report_filter["start_year"],
        report_filter["start_month"],
        report_filter["month_count"],
    )

    metric, rows = _get_ingresos_rows(periods=periods)
    rows = sort_ingresos_rows(rows, report_sort)

    content = build_ingresos_markdown(rows, report_filter)

    generated_suffix = datetime.now().strftime("%Y%m%d-%H%M")
    start_year = report_filter["start_year"]
    start_month = report_filter["start_month"]
    month_count = report_filter["month_count"]

    filename = (
        f"pgc-ingresos-vs-meta-"
        f"fy{start_year}-m{start_month:02d}-n{month_count}-"
        f"{generated_suffix}.md"
    )

    response = HttpResponse(
        smart_str(content),
        content_type="text/plain; charset=utf-8",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def user_can_view_une_summary(user, une):
    if user.is_superuser:
        return True
    profile = getattr(user, "profile", None)  # related_name real
    if profile and profile.default_all_une_access:
        return True
    return user.une_permissions.filter(une=une, can_view_summary=True).exists()


def user_can_view_une_detail(user, une):
    if user.is_superuser:
        return True
    profile = getattr(user, "profile", None)
    if profile and profile.default_all_une_access:
        # si decides que este flag también implica ver detalle
        return True
    return user.une_permissions.filter(une=une, can_view_detail=True).exists()


def user_can_view_detail(user, une):
    if user.is_superuser:
        return True

    profile = getattr(user, "profile", None)
    if profile and getattr(profile, "default_all_une_access", False):
        return True

    return UserUNEPermission.objects.filter(
        user=user,
        une=une,
        can_view_detail=True,
    ).exists()


@login_required
def clientes_nuevos_detail(request):

    une_id = request.GET.get("une_id")
    year_raw = request.GET.get("year")
    month_raw = request.GET.get("month")
    
    if not une_id or not year_raw or not month_raw:
        raise Http404("Faltan parámetros obligatorios: une_id, year, month.")
    
    try:
        une_id = int(une_id)
        year = int(year_raw)
        month = int(month_raw)
    except (TypeError, ValueError):
        raise Http404("Parámetros inválidos: une_id, year, month.")

    if month < 1 or month > 12:
        raise Http404("Mes inválido.")

    une = get_object_or_404(UNE, pk=une_id)

    if not user_can_view_detail(request.user, une):
        return HttpResponseForbidden("No tienes permiso para ver detalle de esta UNE.")

    rows_queryset = (
        NewClientImportRow.objects
        .select_related("header", "currency", "une")
        .filter(une=une)
        .filter(
            Q(header__year=year, header__month=month) |
            Q(year=year, month=month)
        )
        .order_by("client_name", "operation_code", "id")
    )

    detail_rows = []
    for row in rows_queryset:
        detail_rows.append({
            "id": row.id,
            "client_name": row.client_name or "",
            "nit": row.nit or "",
            "operation_code": row.operation_code or "",
            "currency_code": row.currency.code if row.currency else "",
            "amount": row.amount,
            "previous_contracts": row.previous_contracts,
            "counts_as_new": row.counts_as_new,
            "raw_une_value": row.raw_une_value or "",
            "observations": row.observations or "",
            "source_row_number": row.source_row_number,
            "header_year": getattr(row.header, "year", None),
            "header_month": getattr(row.header, "month", None),
            "row_year": getattr(row, "year", None),
            "row_month": getattr(row, "month", None),
        })

    fx_map = {
      (item.year, item.month): item.usd_to_gtq
      for item in MonthlyExchangeRate.objects.all()
    }

    investment_ingresos_total = Decimal("0")
    for row in rows_queryset:
        investment_ingresos_total += _convert_row_amount_to_usd(row, fx_map)
  
    context = {
        "une": une,
        "year": year,
        "month": month,
        "rows": detail_rows,
        "row_count": len(detail_rows),
        "investment_ingresos_total": investment_ingresos_total,
    }

    return render(request, "pgc/clientes_nuevos_detail.html", context)


@login_required
def venta_cruzada_detail(request):
    year = request.GET.get("year")
    month = request.GET.get("month")
    une = request.GET.get("une")

    rows = CrossSaleImportRow.objects.select_related(
        "une_origin",
        "une_destination",
        "currency",
    ).all()

    if year:
        rows = rows.filter(year=year)
    if month:
        rows = rows.filter(month=month)
    if une:
        rows = rows.filter(une_origin__code=une)

    rows = rows.order_by(
        "year",
        "month",
        "une_origin__sort_order",
        "une_destination__sort_order",
        "client_name",
        "operation_code",
    )

    available_years = (
        CrossSaleImportRow.objects.order_by("-year")
        .values_list("year", flat=True)
        .distinct()
    )
    unes = UNE.objects.order_by("sort_order")

    context = {
        "rows": rows,
        "available_years": available_years,
        "months": range(1, 13),
        "unes": unes,
        "selected_year": year or "",
        "selected_month": month or "",
        "selected_une": une or "",
    }
    return render(request, "pgc/venta_cruzada_detail.html", context)


