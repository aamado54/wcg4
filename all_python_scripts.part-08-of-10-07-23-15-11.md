# CONCATENATED .PY FILES

PART_NUMBER=8
TOTAL_PARTS=10

DOCUMENT_MODE=LITERAL_CODE_ARCHIVE
PARSING_PRIORITY=PATH_LITERAL->CONTENT_NUMBERED_BEGIN->CONTENT_BASE64_BEGIN->CONTENT_BEGIN
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
RECORD_SEPARATOR=BEGIN_LITERAL_FILE_RECORD|END_LITERAL_FILE_RECORD
RECORD_BOUNDARY=========== RECORD_BOUNDARY ==========
CONTENT_POLICY=PRESERVE_EXACT_TEXT_WITH_METADATA_AND_NUMBERED_FALLBACK
READING_HINT=Prefer PATH_LITERAL first for file identity. Prefer CONTENT_NUMBERED_BEGIN for faithful line-by-line reading. Use CONTENT_BASE64_BEGIN for exact reconstruction when available. Use CONTENT_BEGIN only as a convenience view. If CONTENT_BEGIN looks compacted, flattened, or visually altered, do not use it to infer exact identifiers, variable names, paths, punctuation grouping, or spacing.
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/views.py
PATH_JSON="pgc/views.py"
FILENAME=views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=1904
SIZE_BYTES_UTF8=60617
CONTENT_SHA256=d371e8e05eef59ad975a32763481081188c7c03251ef82fe2530f68057196ab1
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
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
MAX_MONTH_COUNT = 12

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
PGC_MODE_LABELS = {
    "modo1": "1.Absolutos",
    "modo2": "2.Proporción",
}
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


def get_default_month_count(now=None):
    """Meses incluidos por defecto: enero → mes inmediato anterior al actual."""
    now = now or datetime.now()
    count = now.month - 1
    if count < 1:
        # En enero no hay mes previo del año en curso; mostrar al menos 1.
        count = 1
    if count > MAX_MONTH_COUNT:
        count = MAX_MONTH_COUNT
    return count


def get_default_report_start(now=None):
    """Desde por defecto: enero del año en curso."""
    now = now or datetime.now()
    return now.year, 1


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
    periods = []

    if active_plan:
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

    # Asegurar que el año en curso (ene–dic) siempre esté en el selector "Desde".
    now = datetime.now()
    seen = set(periods)
    for month in range(1, 13):
        key = (now.year, month)
        if key not in seen:
            periods.append(key)
            seen.add(key)

    periods.sort(key=lambda ym: (ym[0], ym[1]), reverse=True)

    return [
        {
            "year": year,
            "month": month,
            "key": f"{year}-{month:02d}",
        }
        for year, month in periods
    ]


MONTH_COUNT_OPTIONS = list(range(1, 13))


def shift_month(year, month, delta):
    total = year * 12 + (month - 1) + delta
    new_year = total // 12
    new_month = total % 12 + 1
    return new_year, new_month
  

def _get_report_filter(request, mode=DEFAULT_PGC_MODE):
    dynamic_default_month_count = get_default_month_count()
    default_start_year, default_start_month = get_default_report_start()

    get_start_year = _safe_int(request.GET.get("start_year"))
    get_start_month = _safe_int(request.GET.get("start_month"))
    get_month_count = _safe_int(request.GET.get("month_count"))

    session_start_year = _safe_int(request.session.get("pgc_report_start_year"))
    session_start_month = _safe_int(request.session.get("pgc_report_start_month"))
    session_month_count = _safe_int(request.session.get("pgc_report_month_count"))

    # Preferir GET; si no, defaults YTD (ene → mes anterior). Session solo si ya hay GET parcial.
    has_get_filter = any(
        request.GET.get(k) not in (None, "")
        for k in ("start_year", "start_month", "month_count")
    )

    if get_month_count:
        month_count = get_month_count
    elif has_get_filter and session_month_count:
        month_count = session_month_count
    else:
        month_count = dynamic_default_month_count

    if month_count < 1:
        month_count = dynamic_default_month_count
    if month_count > MAX_MONTH_COUNT:
        month_count = MAX_MONTH_COUNT

    if get_start_year and get_start_month:
        start_year, start_month = get_start_year, get_start_month
    elif has_get_filter and session_start_year and session_start_month:
        start_year, start_month = session_start_year, session_start_month
    else:
        start_year, start_month = default_start_year, default_start_month

    if start_month < 1 or start_month > 12:
        start_year, start_month = default_start_year, default_start_month

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
        "selected_mode_label": PGC_MODE_LABELS.get(selected_mode, selected_mode),
        "mode_options": PGC_MODE_OPTIONS,
        "mode_choices": [(m, PGC_MODE_LABELS[m]) for m in PGC_MODE_OPTIONS],
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
        f"- Modalidad: {PGC_MODE_LABELS.get(selected_mode, selected_mode)}",
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



~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|# pgc/views.py
00002|
00003|import json
00004|import re
00005|from .models import (
00006|    PGCPlan,
00007|    MonthlyMetricResult,
00008|    MonthlyScorecard,
00009|    MonthlyTarget,
00010|    MonthlyMetricScore,
00011|    MonthlyModeScorecard,
00012|    MonthlyExchangeRate,
00013|)
00014|from accounts.models import UserUNEPermission
00015|from core.models import MetricDefinition, UNE, SystemSetting
00016|
00017|from datetime import datetime
00018|from decimal import Decimal, ROUND_DOWN, InvalidOperation
00019|from django.contrib import messages
00020|from django.contrib.auth.decorators import login_required, user_passes_test
00021|from django.core.management import call_command
00022|from django.db.models import Q
00023|from django.http import HttpResponse, HttpResponseForbidden, Http404
00024|from django.shortcuts import get_object_or_404, render, redirect
00025|from django.template.loader import get_template
00026|from django.urls import reverse
00027|from django.utils.encoding import smart_str
00028|from imports.models import NewClientImportRow, CrossSaleImportRow
00029|
00030|
00031|DEFAULT_MONTH_COUNT = 4
00032|MAX_MONTH_COUNT = 12
00033|
00034|REPORT_DATE_ORDER_OPTIONS = ("asc", "desc")
00035|REPORT_GROUP_MODE_OPTIONS = ("une", "period")
00036|
00037|DEFAULT_REPORT_DATE_ORDER = "asc"
00038|DEFAULT_REPORT_GROUP_MODE = "une"
00039|
00040|report_une_order = {
00041|    "FACTORING": 1,
00042|    "FACTORAJE": 1,
00043|    "LEASING": 2,
00044|    "INSURANCE": 3,
00045|    "INVESTMENT": 4,
00046|    "INVESTMENTS": 4,
00047|    "INVERSIONES": 4,
00048|}
00049|
00050|PGC_MODE_KEY = "pgc.mode"
00051|PGC_DEFAULT_MODE = "modo1"
00052|PGC_MODE_OPTIONS = ("modo1", "modo2")
00053|PGC_MODE_LABELS = {
00054|    "modo1": "1.Absolutos",
00055|    "modo2": "2.Proporción",
00056|}
00057|DEFAULT_PGC_MODE = "modo1"
00058|
00059|
00060|from pgc.investment_ingresos import (
00061|    build_fx_map,
00062|    convert_row_amount_to_usd,
00063|    get_investment_une,
00064|    investment_real_map_for_periods,
00065|)
00066|
00067|
00068|def _convert_row_amount_to_usd(row, fx_map):
00069|    """Compat: delega al helper compartido con la vista/comando de Investment."""
00070|    return convert_row_amount_to_usd(row, fx_map)
00071|  
00072|
00073|def _get_pgc_mode(request):
00074|    raw_mode = (request.GET.get("mode") or request.session.get("pgc_mode") or DEFAULT_PGC_MODE).strip().lower()
00075|
00076|    if raw_mode not in PGC_MODE_OPTIONS:
00077|        raw_mode = DEFAULT_PGC_MODE
00078|
00079|    request.session["pgc_mode"] = raw_mode
00080|    return raw_mode
00081|  
00082|
00083|def get_pgc_mode():
00084|    setting = SystemSetting.objects.filter(key=PGC_MODE_KEY).first()
00085|    if not setting or not setting.value_text:
00086|        return PGC_DEFAULT_MODE
00087|    value = setting.value_text.strip().lower()
00088|    return value if value in ("modo1", "modo2") else PGC_DEFAULT_MODE
00089|
00090|def set_pgc_mode(mode: str):
00091|    if mode not in ("modo1", "modo2"):
00092|        mode = PGC_DEFAULT_MODE
00093|    SystemSetting.objects.update_or_create(
00094|        key=PGC_MODE_KEY,
00095|        defaults={"value_text": mode},
00096|    )
00097|
00098|
00099|def get_default_month_count(now=None):
00100|    """Meses incluidos por defecto: enero → mes inmediato anterior al actual."""
00101|    now = now or datetime.now()
00102|    count = now.month - 1
00103|    if count < 1:
00104|        # En enero no hay mes previo del año en curso; mostrar al menos 1.
00105|        count = 1
00106|    if count > MAX_MONTH_COUNT:
00107|        count = MAX_MONTH_COUNT
00108|    return count
00109|
00110|
00111|def get_default_report_start(now=None):
00112|    """Desde por defecto: enero del año en curso."""
00113|    now = now or datetime.now()
00114|    return now.year, 1
00115|
00116|
00117|def get_active_pgc_plan():
00118|    plan = PGCPlan.objects.filter(is_active=True).order_by("-year").first()
00119|    if plan:
00120|        return plan
00121|    return PGCPlan.objects.order_by("-year").first()
00122|
00123|
00124|def parse_decimal_or_none(raw_value):
00125|    if raw_value is None:
00126|        return None
00127|
00128|    text = str(raw_value).strip()
00129|    if text == "":
00130|        return None
00131|
00132|    text = text.replace(" ", "")
00133|
00134|    if "," in text and "." in text:
00135|        text = text.replace(",", "")
00136|    elif "," in text:
00137|        text = text.replace(",", ".")
00138|
00139|    try:
00140|        return Decimal(text)
00141|    except (InvalidOperation, ValueError):
00142|        return None
00143|
00144|
00145|def _get_active_pgc_plan():
00146|    return get_active_pgc_plan()
00147|  
00148|
00149|def _get_dashboard_rows(periods=None, mode=DEFAULT_PGC_MODE):
00150|    active_plan = _get_active_pgc_plan()
00151|    if not active_plan:
00152|        return []
00153|
00154|    scorecards = (
00155|        MonthlyModeScorecard.objects
00156|        .select_related("une", "plan")
00157|        .filter(plan=active_plan, mode=mode)
00158|        .order_by("-year", "-month", "une__sort_order", "une__name_es")
00159|    )
00160|
00161|    metric_results = (
00162|        MonthlyMetricScore.objects
00163|        .select_related("une", "metric", "plan")
00164|        .filter(plan=active_plan, mode=mode)
00165|    )
00166|
00167|    if periods:
00168|        period_q = _build_period_q(periods)
00169|        scorecards = scorecards.filter(period_q)
00170|        metric_results = metric_results.filter(period_q)
00171|
00172|    use_legacy = not scorecards.exists()
00173|
00174|    if use_legacy:
00175|        scorecards = (
00176|            MonthlyScorecard.objects
00177|            .select_related("une", "plan")
00178|            .filter(plan=active_plan)
00179|            .order_by("-year", "-month", "une__sort_order", "une__name_es")
00180|        )
00181|
00182|        metric_results = (
00183|            MonthlyMetricResult.objects
00184|            .select_related("une", "metric", "plan")
00185|            .filter(plan=active_plan)
00186|        )
00187|
00188|        if periods:
00189|            period_q = _build_period_q(periods)
00190|            scorecards = scorecards.filter(period_q)
00191|            metric_results = metric_results.filter(period_q)
00192|
00193|    metric_map = {}
00194|    for metric_result in metric_results:
00195|        key = (
00196|            metric_result.plan_id,
00197|            metric_result.une_id,
00198|            metric_result.year,
00199|            metric_result.month,
00200|        )
00201|        metric_map.setdefault(key, {})
00202|        metric_map[key][metric_result.metric.code] = metric_result
00203|
00204|    rows = []
00205|    for scorecard in scorecards:
00206|        key = (
00207|            scorecard.plan_id,
00208|            scorecard.une_id,
00209|            scorecard.year,
00210|            scorecard.month,
00211|        )
00212|        metrics = metric_map.get(key, {})
00213|
00214|        rows.append(
00215|            {
00216|                "scorecard": scorecard,
00217|                "year": scorecard.year,
00218|                "month": scorecard.month,
00219|                "une": scorecard.une,
00220|                "p_ingresos": getattr(
00221|                    metrics.get(MetricDefinition.CODE_INGRESOS),
00222|                    "points_awarded",
00223|                    0,
00224|                ),
00225|                "p_clientes": getattr(
00226|                    metrics.get(MetricDefinition.CODE_CLIENTES_NUEVOS),
00227|                    "points_awarded",
00228|                    0,
00229|                ),
00230|                "p_venta_cruzada": getattr(
00231|                    metrics.get(MetricDefinition.CODE_VENTA_CRUZADA),
00232|                    "points_awarded",
00233|                    0,
00234|                ),
00235|                "p_respuesta_reqs": getattr(
00236|                    metrics.get(MetricDefinition.CODE_RESPUESTA_REQS),
00237|                    "points_awarded",
00238|                    0,
00239|                ),
00240|                "total_points": getattr(scorecard, "total_points", 0),
00241|                "is_month_qualified": getattr(scorecard, "is_month_qualified", False),
00242|            }
00243|        )
00244|
00245|    return rows
00246|
00247|
00248|
00249|def get_report_row_meta(row):
00250|    if row.get("is_separator"):
00251|        return None
00252|
00253|    source = row.get("target") or row.get("scorecard") or row.get("result")
00254|    if source is None:
00255|        raise ValueError("No se pudo inferir target, scorecard o result para ordenar la fila.")
00256|
00257|    une = getattr(source, "une", None)
00258|    year = getattr(source, "year", None)
00259|    month = getattr(source, "month", None)
00260|
00261|    une_code = (getattr(une, "code", "") or "").upper()
00262|    une_name = (
00263|        getattr(une, "name_es", None)
00264|        or getattr(une, "name", None)
00265|        or une_code
00266|    )
00267|
00268|    une_sort_order = report_une_order.get(une_code)
00269|    if une_sort_order is None:
00270|        une_sort_order = getattr(une, "sort_order", None)
00271|    if une_sort_order is None:
00272|        une_sort_order = getattr(une, "sort_order", None)
00273|    if une_sort_order is None:
00274|        une_sort_order = 999999
00275|
00276|    return {
00277|        "une_code": une_code,
00278|        "une_name": une_name,
00279|        "une_sort_order": une_sort_order,
00280|        "year": year,
00281|        "month": month,
00282|    }
00283|
00284|
00285|def sort_report_rows(rows, report_sort):
00286|    date_order = report_sort["date_order"]
00287|    group_mode = report_sort["group_mode"]
00288|    reverse_date = date_order == "desc"
00289|
00290|    enriched_rows = []
00291|    for row in rows:
00292|        row_meta = get_report_row_meta(row)
00293|        enriched_rows.append((row_meta, row))
00294|
00295|    if group_mode == "une":
00296|        enriched_rows.sort(
00297|            key=lambda item: (
00298|                item[0]["une_sort_order"],
00299|                item[0]["une_name"].lower(),
00300|                -item[0]["year"] if reverse_date else item[0]["year"],
00301|                -item[0]["month"] if reverse_date else item[0]["month"],
00302|            )
00303|        )
00304|    else:
00305|        enriched_rows.sort(
00306|            key=lambda item: (
00307|                -item[0]["year"] if reverse_date else item[0]["year"],
00308|                -item[0]["month"] if reverse_date else item[0]["month"],
00309|                item[0]["une_sort_order"],
00310|                item[0]["une_name"].lower(),
00311|            )
00312|        )
00313|
00314|    sorted_rows = [row for _, row in enriched_rows]
00315|
00316|    if group_mode != "une":
00317|        return sorted_rows
00318|
00319|    separated_rows = []
00320|    previous_une_key = None
00321|
00322|    for row in sorted_rows:
00323|        row_meta = get_report_row_meta(row)
00324|        current_une_key = (
00325|            row_meta["une_sort_order"],
00326|            row_meta["une_name"].lower(),
00327|        )
00328|
00329|        if previous_une_key is not None and current_une_key != previous_une_key:
00330|            separated_rows.append({"is_separator": True})
00331|
00332|        separated_rows.append(row)
00333|        previous_une_key = current_une_key
00334|
00335|    return separated_rows
00336|
00337|
00338|def get_report_sort(request):
00339|    raw_date_order = (
00340|        request.GET.get("date_order")
00341|        or ""
00342|    ).strip().lower()
00343|
00344|    raw_group_mode = (
00345|        request.GET.get("group_mode")
00346|        or ""
00347|    ).strip().lower()
00348|
00349|    session_date_order = (
00350|        request.session.get("pgc_report_date_order")
00351|        or DEFAULT_REPORT_DATE_ORDER
00352|    ).strip().lower()
00353|
00354|    session_group_mode = (
00355|        request.session.get("pgc_report_group_mode")
00356|        or DEFAULT_REPORT_GROUP_MODE
00357|    ).strip().lower()
00358|
00359|    date_order = raw_date_order or session_date_order
00360|    group_mode = raw_group_mode or session_group_mode
00361|
00362|    if date_order not in REPORT_DATE_ORDER_OPTIONS:
00363|        date_order = DEFAULT_REPORT_DATE_ORDER
00364|
00365|    if group_mode not in REPORT_GROUP_MODE_OPTIONS:
00366|        group_mode = DEFAULT_REPORT_GROUP_MODE
00367|
00368|    request.session["pgc_report_date_order"] = date_order
00369|    request.session["pgc_report_group_mode"] = group_mode
00370|
00371|    return {
00372|        "date_order": date_order,
00373|        "group_mode": group_mode,
00374|    }
00375|
00376|
00377|def get_ingresos_row_meta(row):
00378|    source = row.get("target") or row.get("scorecard")
00379|    if source is None:
00380|        raise KeyError("La fila no contiene ni 'target' ni 'scorecard'.")
00381|
00382|    une = source.une
00383|    une_code = (getattr(une, "code", "") or "").upper()
00384|    une_name = getattr(une, "name_es", "") if hasattr(une, "name_es") else getattr(une, "name_es", "")
00385|
00386|    une_sort_order = report_une_order.get(une_code)
00387|    if une_sort_order is None:
00388|        une_sort_order = getattr(une, "sort_order", None) if hasattr(une, "sort_order") else getattr(une, "sort_order", None)
00389|    if une_sort_order is None:
00390|        une_sort_order = 999999
00391|
00392|    return {
00393|        "une_code": une_code,
00394|        "une_name": une_name or une_code,
00395|        "une_sort_order": une_sort_order,
00396|        "year": source.year,
00397|        "month": source.month,
00398|    }
00399|
00400|
00401|def sort_ingresos_rows(rows, report_sort):
00402|    date_order = report_sort["date_order"]
00403|    group_mode = report_sort["group_mode"]
00404|
00405|    reverse_date = date_order == "desc"
00406|
00407|    enriched_rows = []
00408|    for row in rows:
00409|        row_meta = get_ingresos_row_meta(row)
00410|        enriched_rows.append((row_meta, row))
00411|
00412|    if group_mode == "une":
00413|        enriched_rows.sort(
00414|            key=lambda item: (
00415|                item[0]["une_sort_order"],
00416|                item[0]["une_name"].lower(),
00417|                -item[0]["year"] if reverse_date else item[0]["year"],
00418|                -item[0]["month"] if reverse_date else item[0]["month"],
00419|            )
00420|        )
00421|    else:
00422|        enriched_rows.sort(
00423|            key=lambda item: (
00424|                -item[0]["year"] if reverse_date else item[0]["year"],
00425|                -item[0]["month"] if reverse_date else item[0]["month"],
00426|                item[0]["une_sort_order"],
00427|                item[0]["une_name"].lower(),
00428|            )
00429|        )
00430|
00431|    sorted_rows = [row for _, row in enriched_rows]
00432|
00433|    if group_mode != "une":
00434|        return sorted_rows
00435|
00436|    separated_rows = []
00437|    previous_une_key = None
00438|
00439|    for row in sorted_rows:
00440|        row_meta = get_ingresos_row_meta(row)
00441|        current_une_key = (
00442|            row_meta["une_sort_order"],
00443|            row_meta["une_name"].lower(),
00444|        )
00445|
00446|        if previous_une_key is not None and current_une_key != previous_une_key:
00447|            separated_rows.append({"is_separator": True})
00448|
00449|        separated_rows.append(row)
00450|        previous_une_key = current_une_key
00451|
00452|    return separated_rows
00453|
00454|
00455|def _safe_int(value, default=None):
00456|    try:
00457|        return int(value)
00458|    except (TypeError, ValueError):
00459|        return default
00460|
00461|
00462|def _build_period_range(start_year, start_month, month_count):
00463|  
00464|    periods = []
00465|    year = start_year
00466|    month = start_month
00467|
00468|    for _ in range(month_count):
00469|        periods.append((year, month))
00470|        month += 1
00471|        if month > 12:
00472|            month = 1
00473|            year += 1
00474|
00475|    return periods
00476|
00477|
00478|def _period_range_end(start_year, start_month, month_count):
00479|    """Mes final inclusivo del rango (start + month_count - 1)."""
00480|    periods = _build_period_range(start_year, start_month, month_count)
00481|    if not periods:
00482|        return start_year, start_month
00483|    return periods[-1]
00484|
00485|
00486|def _build_ytd_period_range(end_year, end_month):
00487|    """Enero del año del mes final → mes final (inclusive)."""
00488|    end_month = max(1, min(12, int(end_month)))
00489|    return [(end_year, m) for m in range(1, end_month + 1)]
00490|
00491|
00492|def _build_period_q(periods):
00493|    query = Q()
00494|    for year, month in periods:
00495|        query |= Q(year=year, month=month)
00496|    return query  
00497|
00498|
00499|def _get_available_periods(mode=None):
00500|    active_plan = _get_active_pgc_plan()
00501|    periods = []
00502|
00503|    if active_plan:
00504|        periods = list(
00505|            MonthlyModeScorecard.objects
00506|            .filter(plan=active_plan, mode=mode or DEFAULT_PGC_MODE)
00507|            .order_by("-year", "-month")
00508|            .values_list("year", "month")
00509|            .distinct()
00510|        )
00511|
00512|        if not periods:
00513|            periods = list(
00514|                MonthlyScorecard.objects
00515|                .filter(plan=active_plan)
00516|                .order_by("-year", "-month")
00517|                .values_list("year", "month")
00518|                .distinct()
00519|            )
00520|
00521|    # Asegurar que el año en curso (ene–dic) siempre esté en el selector "Desde".
00522|    now = datetime.now()
00523|    seen = set(periods)
00524|    for month in range(1, 13):
00525|        key = (now.year, month)
00526|        if key not in seen:
00527|            periods.append(key)
00528|            seen.add(key)
00529|
00530|    periods.sort(key=lambda ym: (ym[0], ym[1]), reverse=True)
00531|
00532|    return [
00533|        {
00534|            "year": year,
00535|            "month": month,
00536|            "key": f"{year}-{month:02d}",
00537|        }
00538|        for year, month in periods
00539|    ]
00540|
00541|
00542|MONTH_COUNT_OPTIONS = list(range(1, 13))
00543|
00544|
00545|def shift_month(year, month, delta):
00546|    total = year * 12 + (month - 1) + delta
00547|    new_year = total // 12
00548|    new_month = total % 12 + 1
00549|    return new_year, new_month
00550|  
00551|
00552|def _get_report_filter(request, mode=DEFAULT_PGC_MODE):
00553|    dynamic_default_month_count = get_default_month_count()
00554|    default_start_year, default_start_month = get_default_report_start()
00555|
00556|    get_start_year = _safe_int(request.GET.get("start_year"))
00557|    get_start_month = _safe_int(request.GET.get("start_month"))
00558|    get_month_count = _safe_int(request.GET.get("month_count"))
00559|
00560|    session_start_year = _safe_int(request.session.get("pgc_report_start_year"))
00561|    session_start_month = _safe_int(request.session.get("pgc_report_start_month"))
00562|    session_month_count = _safe_int(request.session.get("pgc_report_month_count"))
00563|
00564|    # Preferir GET; si no, defaults YTD (ene → mes anterior). Session solo si ya hay GET parcial.
00565|    has_get_filter = any(
00566|        request.GET.get(k) not in (None, "")
00567|        for k in ("start_year", "start_month", "month_count")
00568|    )
00569|
00570|    if get_month_count:
00571|        month_count = get_month_count
00572|    elif has_get_filter and session_month_count:
00573|        month_count = session_month_count
00574|    else:
00575|        month_count = dynamic_default_month_count
00576|
00577|    if month_count < 1:
00578|        month_count = dynamic_default_month_count
00579|    if month_count > MAX_MONTH_COUNT:
00580|        month_count = MAX_MONTH_COUNT
00581|
00582|    if get_start_year and get_start_month:
00583|        start_year, start_month = get_start_year, get_start_month
00584|    elif has_get_filter and session_start_year and session_start_month:
00585|        start_year, start_month = session_start_year, session_start_month
00586|    else:
00587|        start_year, start_month = default_start_year, default_start_month
00588|
00589|    if start_month < 1 or start_month > 12:
00590|        start_year, start_month = default_start_year, default_start_month
00591|
00592|    request.session["pgc_report_start_year"] = start_year
00593|    request.session["pgc_report_start_month"] = start_month
00594|    request.session["pgc_report_month_count"] = month_count
00595|
00596|    return {
00597|        "start_year": start_year,
00598|        "start_month": start_month,
00599|        "month_count": month_count,
00600|    }
00601|
00602|
00603|@login_required
00604|def pgc_home(request):
00605|    """Acceso directo al tablero PGC (sin pantalla intermedia)."""
00606|    return redirect("pgc:dashboard")
00607|
00608|
00609|def splash(request):
00610|    """
00611|    Pantalla inicial: muestra splash y, al primer click/tecla,
00612|    redirige al tablero principal.
00613|    """
00614|    # Si ya está autenticado, igual mostramos splash una vez.
00615|    return render(request, "splash.html")
00616|
00617|
00618|@login_required
00619|def pgc_dashboard_export_md(request):
00620|    report_filter = _get_report_filter(request)
00621|    report_sort = get_report_sort(request)
00622|    selected_mode = _get_pgc_mode(request)
00623|
00624|    periods = _build_period_range(
00625|        report_filter["start_year"],
00626|        report_filter["start_month"],
00627|        report_filter["month_count"],
00628|    )
00629|
00630|    rows = _get_dashboard_rows(periods=periods, mode=selected_mode)
00631|    rows = sort_report_rows(rows, report_sort)
00632|
00633|    content = _build_dashboard_markdown(
00634|        rows,
00635|        report_filter,
00636|        selected_mode=selected_mode,
00637|    )
00638|
00639|    generated_suffix = datetime.now().strftime("%Y%m%d-%H%M")
00640|    start_year = report_filter["start_year"]
00641|    start_month = report_filter["start_month"]
00642|    month_count = report_filter["month_count"]
00643|
00644|    filename = (
00645|        f"pgc-tablero-principal-"
00646|        f"{selected_mode}-"
00647|        f"fy{start_year}-m{start_month:02d}-n{month_count}-"
00648|        f"{generated_suffix}.md"
00649|    )
00650|
00651|    response = HttpResponse(
00652|        smart_str(content),
00653|        content_type="text/plain; charset=utf-8",
00654|    )
00655|    response["Content-Disposition"] = f'attachment; filename="{filename}"'
00656|    return response
00657|
00658|
00659|@login_required
00660|def pgc_dashboard(request):
00661|    selected_mode = _get_pgc_mode(request)
00662|    report_filter = _get_report_filter(request, mode=selected_mode)
00663|    report_sort = get_report_sort(request)
00664|
00665|    periods = _build_period_range(
00666|        report_filter["start_year"],
00667|        report_filter["start_month"],
00668|        report_filter["month_count"],
00669|    )
00670|
00671|    rows = _get_dashboard_rows(periods=periods, mode=selected_mode)
00672|    rows = sort_report_rows(rows, report_sort)
00673|
00674|    chart_payload = _build_dashboard_chart_payload(
00675|        periods=periods,
00676|        mode=selected_mode,
00677|    )
00678|
00679|    # Serie aparte para exportación SVG 4-charts: siempre enero → mes final del rango.
00680|    end_year, end_month = _period_range_end(
00681|        report_filter["start_year"],
00682|        report_filter["start_month"],
00683|        report_filter["month_count"],
00684|    )
00685|    ytd_periods = _build_ytd_period_range(end_year, end_month)
00686|    ytd_payload = _build_dashboard_chart_payload(
00687|        periods=ytd_periods,
00688|        mode=selected_mode,
00689|    )
00690|    ingresos_ytd = (ytd_payload.get("metrics") or {}).get(
00691|        MetricDefinition.CODE_INGRESOS, {}
00692|    )
00693|    chart_payload["export_ingresos"] = {
00694|        "end_year": end_year,
00695|        "end_month": end_month,
00696|        "periods": ingresos_ytd.get("periods") or [],
00697|        "y_axis": ingresos_ytd.get("y_axis") or "Cifras en miles de US$",
00698|    }
00699|
00700|    context = {
00701|        "rows": rows,
00702|        "report_filter": report_filter,
00703|        "report_sort": report_sort,
00704|        "selected_mode": selected_mode,
00705|        "selected_mode_label": PGC_MODE_LABELS.get(selected_mode, selected_mode),
00706|        "mode_options": PGC_MODE_OPTIONS,
00707|        "mode_choices": [(m, PGC_MODE_LABELS[m]) for m in PGC_MODE_OPTIONS],
00708|        "available_periods": _get_available_periods(mode=selected_mode),
00709|        "month_count_options": MONTH_COUNT_OPTIONS,
00710|        "chart_payload_json": json.dumps(chart_payload, ensure_ascii=False),
00711|        "chart_rows": [
00712|            {
00713|                "une": row["une"].name_es,
00714|                "periodo": f"{row['year']}-{row['month']:02d}",              
00715|                "p_ingresos": row["p_ingresos"],
00716|                "p_clientes": row["p_clientes"],
00717|                "p_venta_cruzada": row["p_venta_cruzada"],
00718|                "p_respuesta_reqs": row["p_respuesta_reqs"],
00719|                "total": row["total_points"],
00720|            }
00721|            for row in rows
00722|            if not row.get("is_separator")
00723|        ],
00724|    }
00725|    return render(request, "pgc/dashboard.html", context)
00726|  
00727|
00728|def _decimal_to_number(value):
00729|    if value is None:
00730|        return None
00731|    try:
00732|        return float(value)
00733|    except Exception:
00734|        return None
00735|
00736|
00737|def _build_dashboard_chart_payload(periods=None, mode=DEFAULT_PGC_MODE):
00738|    active_plan = get_active_pgc_plan()
00739|    if not active_plan:
00740|        return {"periods": [], "unes": [], "metrics": {}}
00741|
00742|    metric_codes = [
00743|        MetricDefinition.CODE_INGRESOS,
00744|        MetricDefinition.CODE_CLIENTES_NUEVOS,
00745|        MetricDefinition.CODE_VENTA_CRUZADA,
00746|    ]
00747|
00748|    targets = (
00749|        MonthlyTarget.objects
00750|        .select_related("une", "plan", "metric")
00751|        .filter(plan=active_plan, metric__code__in=metric_codes)
00752|    )
00753|
00754|    results = (
00755|        MonthlyMetricResult.objects
00756|        .select_related("une", "plan", "metric")
00757|        .filter(plan=active_plan, metric__code__in=metric_codes)
00758|    )
00759|
00760|    if periods:
00761|        period_q = _build_period_q(periods)
00762|        targets = targets.filter(period_q)
00763|        results = results.filter(period_q)
00764|
00765|    target_map = {}
00766|    for t in targets:
00767|        key = (t.metric.code, t.year, t.month, t.une.code)
00768|        target_map[key] = _decimal_to_number(t.target_value)
00769|
00770|    result_map = {}
00771|    for r in results:
00772|        key = (r.metric.code, r.year, r.month, r.une.code)
00773|        result_map[key] = _decimal_to_number(r.measured_value)
00774|
00775|    une_map = {}
00776|    for t in targets:
00777|        une_map[t.une.code] = {
00778|            "code": t.une.code,
00779|            "name_es": t.une.name_es,
00780|            "sort_order": t.une.sort_order,
00781|        }
00782|    for r in results:
00783|        une_map[r.une.code] = {
00784|            "code": r.une.code,
00785|            "name_es": r.une.name_es,
00786|            "sort_order": r.une.sort_order,
00787|        }
00788|
00789|    unes = sorted(
00790|        une_map.values(),
00791|        key=lambda x: (x["sort_order"] if x["sort_order"] is not None else 999999, x["name_es"])
00792|    )
00793|
00794|    periods_list = []
00795|    for year, month in (periods or []):
00796|        periods_list.append({
00797|            "year": year,
00798|            "month": month,
00799|            "key": f"{year}-{month:02d}",
00800|            "label": f"{year}-{month:02d}",
00801|        })
00802|
00803|    series = {}
00804|    for metric_code in metric_codes:
00805|        metric_periods = []
00806|        for year, month in (periods or []):
00807|            by_une = {}
00808|            for une in unes:
00809|                une_code = une["code"]
00810|                by_une[une_code] = {
00811|                    "target": target_map.get((metric_code, year, month, une_code), 0),
00812|                    "real": result_map.get((metric_code, year, month, une_code), 0),
00813|                }
00814|
00815|            metric_periods.append({
00816|                "year": year,
00817|                "month": month,
00818|                "key": f"{year}-{month:02d}",
00819|                "label": f"{year}-{month:02d}",
00820|                "by_une": by_une,
00821|            })
00822|
00823|        series[metric_code] = metric_periods
00824|    return {
00825|        "periods": periods_list,
00826|        "unes": [
00827|            {"code": u["code"], "name_es": u["name_es"]}
00828|            for u in unes
00829|        ],
00830|        "metrics": {
00831|            MetricDefinition.CODE_INGRESOS: {
00832|                "title": "Ingresos brutos",
00833|                "subtitle": "Real vs meta por período",
00834|                "y_axis": "Cifras en miles de US$",
00835|                "metric_code": MetricDefinition.CODE_INGRESOS,
00836|                "periods": series[MetricDefinition.CODE_INGRESOS],
00837|            },
00838|            MetricDefinition.CODE_CLIENTES_NUEVOS: {
00839|                "title": "Clientes nuevos",
00840|                "subtitle": "Real vs meta por período",
00841|                "y_axis": "Cantidad de clientes",
00842|                "metric_code": MetricDefinition.CODE_CLIENTES_NUEVOS,
00843|                "periods": series[MetricDefinition.CODE_CLIENTES_NUEVOS],
00844|            },
00845|            MetricDefinition.CODE_VENTA_CRUZADA: {
00846|                "title": "Venta cruzada",
00847|                "subtitle": "Real vs meta por período",
00848|                "y_axis": "Cantidad",
00849|                "metric_code": MetricDefinition.CODE_VENTA_CRUZADA,
00850|                "periods": series[MetricDefinition.CODE_VENTA_CRUZADA],
00851|            },
00852|        },
00853|    }
00854|
00855|
00856|def _build_dashboard_markdown(rows, report_filter, selected_mode="modo1"):
00857|    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
00858|    start_year = report_filter["start_year"]
00859|    start_month = report_filter["start_month"]
00860|    month_count = report_filter["month_count"]
00861|
00862|    periods = _build_period_range(start_year, start_month, month_count)
00863|    end_year, end_month = periods[-1]
00864|
00865|    lines = [
00866|        "PGC - Tablero principal de puntos por UNE y mes",
00867|        "",
00868|        f"Generado: {generated_at}",
00869|        "",
00870|        "Filtros",
00871|        f"- Modalidad: {PGC_MODE_LABELS.get(selected_mode, selected_mode)}",
00872|        f"- Desde: {start_year}-{start_month:02d}",
00873|        f"- Hasta: {end_year}-{end_month:02d}",
00874|        f"- Meses incluidos: {month_count}",
00875|        "",
00876|        "Descripción",
00877|        "Resumen mensual de puntos por UNE y periodo.",
00878|        "",
00879|        "Datos",
00880|        "",
00881|        "| UNE | Periodo | Puntos ingresos | Puntos clientes nuevos | Puntos venta cruzada | Puntos respuesta reqs | Total | Clasifica |",
00882|        "| --- | --- | --- | --- | --- | --- | --- | --- |",
00883|    ]
00884|
00885|    if not rows:
00886|        lines.append("| Sin datos | - | - | - | - | - | - | - |")
00887|    else:
00888|        for row in rows:
00889|            if row.get("is_separator"):
00890|                continue
00891|
00892|            clasifica = "Sí" if row["is_month_qualified"] else "No"
00893|            periodo = f"{row['year']}-{row['month']:02d}"
00894|
00895|            lines.append(
00896|                f"| {row['une'].name_es} | {periodo} | "
00897|                f"{row['p_ingresos']} | {row['p_clientes']} | "
00898|                f"{row['p_venta_cruzada']} | {row['p_respuesta_reqs']} | "
00899|                f"{row['total_points']} | {clasifica} |"
00900|            )
00901|
00902|    lines.extend([
00903|        "",
00904|        "Nota",
00905|        "Este reporte muestra el puntaje total y sus componentes por UNE y periodo.",
00906|        "",
00907|    ])
00908|
00909|    return "\n".join(lines)
00910|
00911|
00912|@login_required
00913|def clientes_nuevos_report(request):
00914|    report_filter = _get_report_filter(request)
00915|    report_sort = get_report_sort(request)
00916|
00917|    periods = _build_period_range(
00918|        report_filter["start_year"],
00919|        report_filter["start_month"],
00920|        report_filter["month_count"],
00921|    )
00922|
00923|    metric, rows = _get_clientes_nuevos_rows(periods=periods)
00924|    rows = sort_report_rows(rows, report_sort)
00925|    
00926|    context = {
00927|        "rows": rows,
00928|        "metric": metric,
00929|        "report_filter": report_filter,
00930|        "report_sort": report_sort,
00931|        "available_periods": _get_available_periods(),
00932|        "month_count_options": MONTH_COUNT_OPTIONS,
00933|    }
00934|    return render(request, "pgc/clientes_nuevos.html", context)
00935|
00936|
00937|def _get_clientes_nuevos_rows(periods=None):
00938|    try:
00939|        metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_CLIENTES_NUEVOS)
00940|    except MetricDefinition.DoesNotExist:
00941|        metric = None
00942|
00943|    targets = MonthlyTarget.objects.select_related("une", "plan").filter(
00944|        metric__code=MetricDefinition.CODE_CLIENTES_NUEVOS
00945|    )
00946|    results = MonthlyMetricResult.objects.select_related("une", "plan", "metric").filter(
00947|        metric__code=MetricDefinition.CODE_CLIENTES_NUEVOS
00948|    )
00949|    scorecards = MonthlyScorecard.objects.select_related("une", "plan")
00950|
00951|    if periods:
00952|        period_q = _build_period_q(periods)
00953|        targets = targets.filter(period_q)
00954|        results = results.filter(period_q)
00955|        scorecards = scorecards.filter(period_q)
00956|
00957|    result_map = {}
00958|    for r in results:
00959|        key = (r.plan_id, r.une_id, r.year, r.month)
00960|        result_map[key] = r
00961|
00962|    score_map = {}
00963|    for sc in scorecards:
00964|        key = (sc.plan_id, sc.une_id, sc.year, sc.month)
00965|        score_map[key] = sc
00966|
00967|    detail_rows = NewClientImportRow.objects.filter(une__isnull=False)
00968|
00969|    if periods:
00970|        detail_period_q = Q()
00971|        for year, month in periods:
00972|            detail_period_q |= Q(year=year, month=month)
00973|            detail_period_q |= Q(header__year=year, header__month=month)
00974|        detail_rows = detail_rows.filter(detail_period_q)
00975|
00976|    detail_keys = set()
00977|
00978|    for row in detail_rows.select_related("header"):
00979|        row_year = row.year or (row.header.year if row.header else None)
00980|        row_month = row.month or (row.header.month if row.header else None)
00981|
00982|        if row.une_id and row_year and row_month:
00983|            detail_keys.add((row.une_id, row_year, row_month))
00984|
00985|    investment_new_clients_map = {}
00986|    investment_ingresos_map = {}
00987|    
00988|    investment_une = (
00989|        UNE.objects.filter(code__in=["INVESTMENT", "INVESTMENTS", "INVERSIONES"])
00990|        .order_by("sort_order", "id")
00991|        .first()
00992|    )
00993|    
00994|    fx_map = {
00995|        (item.year, item.month): item.usd_to_gtq
00996|        for item in MonthlyExchangeRate.objects.all()
00997|    }
00998|    
00999|    if investment_une:
01000|        for row in detail_rows.select_related("currency", "header"):
01001|            row_year = row.year or (row.header.year if row.header else None)
01002|            row_month = row.month or (row.header.month if row.header else None)
01003|    
01004|            if row.une_id != investment_une.id or not row_year or not row_month:
01005|                continue
01006|    
01007|            key = (row.une_id, row_year, row_month)
01008|    
01009|            if row.counts_as_new:
01010|                investment_new_clients_map[key] = investment_new_clients_map.get(key, 0) + 1
01011|    
01012|            investment_ingresos_map[key] = (
01013|                investment_ingresos_map.get(key, Decimal("0"))
01014|                + _convert_row_amount_to_usd(row, fx_map)
01015|            )
01016|  
01017|    rows = []
01018|    for t in targets.order_by("year", "month", "une__sort_order"):
01019|        key = (t.plan_id, t.une_id, t.year, t.month)
01020|        mr = result_map.get(key)
01021|        sc = score_map.get(key)
01022|
01023|        real_value_override = None
01024|        if investment_une and t.une_id == investment_une.id:
01025|            real_value_override = investment_new_clients_map.get((t.une_id, t.year, t.month), 0)
01026|      
01027|        rows.append(
01028|            {
01029|                "target": t,
01030|                "result": mr,
01031|                "scorecard": sc,
01032|                "has_detail": (t.une_id, t.year, t.month) in detail_keys,
01033|                "investment_ingresos": investment_ingresos_map.get((t.une_id, t.year, t.month)),
01034|                "real_value_override": real_value_override,
01035|            }
01036|        )
01037|      
01038|    return metric, rows
01039|
01040|
01041|def _build_clientes_nuevos_markdown(rows, report_filter):
01042|    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
01043|
01044|    start_year = report_filter["start_year"]
01045|    start_month = report_filter["start_month"]
01046|    month_count = report_filter["month_count"]
01047|    periods = _build_period_range(start_year, start_month, month_count)
01048|    end_year, end_month = periods[-1]
01049|
01050|    lines = [
01051|        "# PGC - Clientes nuevos vs meta",
01052|        "",
01053|        f"Generado: {generated_at}",
01054|        "",
01055|        "## Filtros",
01056|        f"- Desde: {start_year}-{start_month:02d}",
01057|        f"- Hasta: {end_year}-{end_month:02d}",
01058|        f"- Meses incluidos: {month_count}",
01059|        "",
01060|        "## Descripción",
01061|        "Meta y resultado mensual de clientes nuevos por UNE y periodo.",
01062|        "",
01063|        "## Datos",
01064|        "",
01065|        "| UNE | Periodo | Meta clientes | Clientes reales | Cumple | Puntos asignados | Total del mes |",
01066|        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
01067|    ]
01068|
01069|    if not rows:
01070|        lines.append("| Sin datos | - | - | - | - | - | - |")
01071|    else:
01072|        for row in rows:
01073|            if row.get("is_separator"):
01074|                continue
01075|        
01076|            target = row["target"]
01077|            result = row["result"]
01078|            scorecard = row["scorecard"]
01079|
01080|            periodo = f"{target.year}-{target.month:02d}"
01081|            meta = int(target.target_value) if target.target_value is not None else "-"
01082|            
01083|            real_override = row.get("real_value_override", None)
01084|            if real_override is not None:
01085|                reales = int(real_override)
01086|            else:
01087|                reales = int(result.measured_value) if result and result.measured_value is not None else "-"
01088|          
01089|            cumple = "Sí" if result and result.is_achieved else "No"
01090|            puntos = result.points_awarded if result else 0
01091|            total_mes = scorecard.total_points if scorecard else 0
01092|
01093|            lines.append(
01094|                f"| {target.une.name_es} | {periodo} | {meta} | {reales} | {cumple} | {puntos} | {total_mes} |"
01095|            )
01096|
01097|    lines.extend([
01098|        "",
01099|        "## Nota",
01100|        "Este reporte muestra la meta mensual de clientes nuevos, el resultado observado y su impacto en el puntaje total del mes.",
01101|        "",
01102|    ])
01103|    return "\n".join(lines)
01104|
01105|
01106|@login_required
01107|def clientes_nuevos_export_md(request):
01108|    report_filter = _get_report_filter(request)
01109|    report_sort = get_report_sort(request)
01110|    periods = _build_period_range(
01111|        report_filter["start_year"],
01112|        report_filter["start_month"],
01113|        report_filter["month_count"],
01114|    )
01115|    metric, rows = _get_clientes_nuevos_rows(periods=periods)
01116|    rows = sort_report_rows(rows, report_sort)
01117|
01118|    content = _build_clientes_nuevos_markdown(rows, report_filter)
01119|
01120|    generated_suffix = datetime.now().strftime("%Y%m%d-%H%M")
01121|    start_year = report_filter["start_year"]
01122|    start_month = report_filter["start_month"]
01123|    month_count = report_filter["month_count"]
01124|    filename = (
01125|        f"pgc-clientes-nuevos-"
01126|        f"fy{start_year}-m{start_month:02d}-n{month_count}-"
01127|        f"{generated_suffix}.md"
01128|    )
01129|
01130|    response = HttpResponse(
01131|        smart_str(content),
01132|        content_type="text/plain; charset=utf-8",
01133|    )
01134|    response["Content-Disposition"] = f'attachment; filename="{filename}"'
01135|    return response
01136|
01137|
01138|def _get_venta_cruzada_rows(periods=None):
01139|    try:
01140|        metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_VENTA_CRUZADA)
01141|    except MetricDefinition.DoesNotExist:
01142|        metric = None
01143|
01144|    targets = MonthlyTarget.objects.select_related("une", "plan").filter(
01145|        metric__code=MetricDefinition.CODE_VENTA_CRUZADA
01146|    )
01147|    results = MonthlyMetricResult.objects.select_related("une", "plan", "metric").filter(
01148|        metric__code=MetricDefinition.CODE_VENTA_CRUZADA
01149|    )
01150|    scorecards = MonthlyScorecard.objects.select_related("une", "plan")
01151|
01152|    if periods:
01153|        period_q = _build_period_q(periods)
01154|        targets = targets.filter(period_q)
01155|        results = results.filter(period_q)
01156|        scorecards = scorecards.filter(period_q)
01157|
01158|    result_map = {}
01159|    for r in results:
01160|        key = (r.plan_id, r.une_id, r.year, r.month)
01161|        result_map[key] = r
01162|
01163|    score_map = {}
01164|    for sc in scorecards:
01165|        key = (sc.plan_id, sc.une_id, sc.year, sc.month)
01166|        score_map[key] = sc
01167|
01168|    rows = []
01169|    for t in targets.order_by("year", "month", "une__sort_order"):
01170|        key = (t.plan_id, t.une_id, t.year, t.month)
01171|        mr = result_map.get(key)
01172|        sc = score_map.get(key)
01173|        rows.append({
01174|            "target": t,
01175|            "result": mr,
01176|            "scorecard": sc,
01177|        })
01178|
01179|    return metric, rows
01180|  
01181|
01182|@login_required
01183|def venta_cruzada_report(request):
01184|    report_filter = _get_report_filter(request)
01185|    report_sort = get_report_sort(request)
01186|
01187|    periods = _build_period_range(
01188|        report_filter["start_year"],
01189|        report_filter["start_month"],
01190|        report_filter["month_count"],
01191|    )
01192|
01193|    metric, rows = _get_venta_cruzada_rows(periods=periods)
01194|    rows = sort_report_rows(rows, report_sort)
01195|    
01196|    context = {
01197|        "rows": rows,
01198|        "metric": metric,
01199|        "report_filter": report_filter,
01200|        "report_sort": report_sort,
01201|        "available_periods": _get_available_periods(),
01202|        "month_count_options": MONTH_COUNT_OPTIONS,
01203|    }
01204|    return render(request, "pgc/venta_cruzada.html", context)
01205|
01206|
01207|def _build_venta_cruzada_markdown(rows, report_filter):
01208|    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
01209|
01210|    start_year = report_filter["start_year"]
01211|    start_month = report_filter["start_month"]
01212|    month_count = report_filter["month_count"]
01213|    periods = _build_period_range(start_year, start_month, month_count)
01214|    end_year, end_month = periods[-1]
01215|
01216|    lines = [
01217|        "# PGC - Venta cruzada vs meta",
01218|        "",
01219|        f"Generado: {generated_at}",
01220|        "",
01221|        "## Filtros",
01222|        f"- Desde: {start_year}-{start_month:02d}",
01223|        f"- Hasta: {end_year}-{end_month:02d}",
01224|        f"- Meses incluidos: {month_count}",
01225|        "",
01226|        "## Descripción",
01227|        "Meta y resultado mensual de venta cruzada por UNE y periodo.",
01228|        "",
01229|        "## Datos",
01230|        "",
01231|        "| UNE | Periodo | Meta venta cruzada | Venta cruzada real | Cumple | Puntos asignados | Total del mes |",
01232|        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
01233|    ]
01234|
01235|    if not rows:
01236|        lines.append("| Sin datos | - | - | - | - | - | - |")
01237|    else:
01238|        for row in rows:
01239|            if row.get("is_separator"):
01240|                continue
01241|        
01242|            target = row["target"]
01243|            result = row["result"]
01244|            scorecard = row["scorecard"]          
01245|
01246|            periodo = f"{target.year}-{target.month:02d}"
01247|            meta = int(target.target_value) if target.target_value is not None else "-"
01248|            reales = int(result.measured_value) if result and result.measured_value is not None else "-"
01249|            cumple = "Sí" if result and result.is_achieved else "No"
01250|            puntos = result.points_awarded if result else 0
01251|            total_mes = scorecard.total_points if scorecard else 0
01252|
01253|            lines.append(
01254|                f"| {target.une.name_es} | {periodo} | {meta} | {reales} | {cumple} | {puntos} | {total_mes} |"
01255|            )
01256|
01257|    lines.extend([
01258|        "",
01259|        "## Nota",
01260|        "Este reporte muestra la meta mensual de venta cruzada, el resultado observado y su impacto en el puntaje total del mes.",
01261|        "",
01262|    ])
01263|    return "\n".join(lines)
01264|
01265|
01266|@login_required
01267|def venta_cruzada_export_md(request):
01268|    report_filter = _get_report_filter(request)
01269|    report_sort = get_report_sort(request)
01270|    periods = _build_period_range(
01271|        report_filter["start_year"],
01272|        report_filter["start_month"],
01273|        report_filter["month_count"],
01274|    )
01275|    metric, rows = _get_venta_cruzada_rows(periods=periods)
01276|    rows = sort_report_rows(rows, report_sort)
01277|
01278|    content = _build_venta_cruzada_markdown(rows, report_filter)
01279|
01280|    generated_suffix = datetime.now().strftime("%Y%m%d-%H%M")
01281|    start_year = report_filter["start_year"]
01282|    start_month = report_filter["start_month"]
01283|    month_count = report_filter["month_count"]
01284|    filename = (
01285|        f"pgc-venta-cruzada-"
01286|        f"fy{start_year}-m{start_month:02d}-n{month_count}-"
01287|        f"{generated_suffix}.md"
01288|    )
01289|
01290|    response = HttpResponse(
01291|        smart_str(content),
01292|        content_type="text/plain; charset=utf-8",
01293|    )
01294|    response["Content-Disposition"] = f'attachment; filename="{filename}"'
01295|    return response
01296|
01297|
01298|def _get_respuesta_reqs_rows(periods=None):
01299|    try:
01300|        metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_RESPUESTA_REQS)
01301|    except MetricDefinition.DoesNotExist:
01302|        metric = None
01303|
01304|    targets = MonthlyTarget.objects.select_related("une", "plan").filter(
01305|        metric__code=MetricDefinition.CODE_RESPUESTA_REQS
01306|    )
01307|    results = MonthlyMetricResult.objects.select_related("une", "plan", "metric").filter(
01308|        metric__code=MetricDefinition.CODE_RESPUESTA_REQS
01309|    )
01310|    scorecards = MonthlyScorecard.objects.select_related("une", "plan")
01311|
01312|    if periods:
01313|        period_q = _build_period_q(periods)
01314|        targets = targets.filter(period_q)
01315|        results = results.filter(period_q)
01316|        scorecards = scorecards.filter(period_q)
01317|
01318|    result_map = {}
01319|    for r in results:
01320|        key = (r.plan_id, r.une_id, r.year, r.month)
01321|        result_map[key] = r
01322|
01323|    score_map = {}
01324|    for sc in scorecards:
01325|        key = (sc.plan_id, sc.une_id, sc.year, sc.month)
01326|        score_map[key] = sc
01327|
01328|    rows = []
01329|    for t in targets.order_by("year", "month", "une__sort_order"):
01330|        key = (t.plan_id, t.une_id, t.year, t.month)
01331|        mr = result_map.get(key)
01332|        sc = score_map.get(key)
01333|        rows.append({
01334|            "target": t,
01335|            "result": mr,
01336|            "scorecard": sc,
01337|        })
01338|
01339|    return metric, rows
01340|  
01341|
01342|@login_required
01343|def respuesta_reqs_report(request):
01344|    report_filter = _get_report_filter(request)
01345|    report_sort = get_report_sort(request)
01346|
01347|    periods = _build_period_range(
01348|        report_filter["start_year"],
01349|        report_filter["start_month"],
01350|        report_filter["month_count"],
01351|    )
01352|
01353|    metric, rows = _get_respuesta_reqs_rows(periods=periods)
01354|    rows = sort_report_rows(rows, report_sort)
01355|
01356|    context = {
01357|        "rows": rows,
01358|        "metric": metric,
01359|        "report_filter": report_filter,
01360|        "report_sort": report_sort,
01361|        "available_periods": _get_available_periods(),
01362|        "month_count_options": MONTH_COUNT_OPTIONS,
01363|    }
01364|    return render(request, "pgc/respuesta_reqs.html", context)
01365|
01366|
01367|def _build_respuesta_reqs_markdown(rows, report_filter):
01368|    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
01369|
01370|    start_year = report_filter["start_year"]
01371|    start_month = report_filter["start_month"]
01372|    month_count = report_filter["month_count"]
01373|    periods = _build_period_range(start_year, start_month, month_count)
01374|    end_year, end_month = periods[-1]
01375|
01376|    lines = [
01377|        "# PGC - Respuesta a requerimientos vs meta",
01378|        "",
01379|        f"Generado: {generated_at}",
01380|        "",
01381|        "## Filtros",
01382|        f"- Desde: {start_year}-{start_month:02d}",
01383|        f"- Hasta: {end_year}-{end_month:02d}",
01384|        f"- Meses incluidos: {month_count}",
01385|        "",
01386|        "## Descripción",
01387|        "Meta y resultado mensual de respuesta a requerimientos por UNE y periodo.",
01388|        "",
01389|        "## Datos",
01390|        "",
01391|        "| UNE | Periodo | Meta respuesta reqs | Respuesta reqs real | Cumple | Puntos asignados | Total del mes |",
01392|        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
01393|    ]
01394|
01395|    if not rows:
01396|        lines.append("| Sin datos | - | - | - | - | - | - |")
01397|    else:
01398|        for row in rows:
01399|            if row.get("is_separator"):
01400|                continue
01401|        
01402|            target = row["target"]
01403|            result = row["result"]
01404|            scorecard = row["scorecard"]
01405|          
01406|            periodo = f"{target.year}-{target.month:02d}"
01407|            meta = int(target.target_value) if target.target_value is not None else "-"
01408|            reales = int(result.measured_value) if result and result.measured_value is not None else "-"
01409|            cumple = "Sí" if result and result.is_achieved else "No"
01410|            puntos = result.points_awarded if result else 0
01411|            total_mes = scorecard.total_points if scorecard else 0
01412|
01413|            lines.append(
01414|                f"| {target.une.name_es} | {periodo} | {meta} | {reales} | {cumple} | {puntos} | {total_mes} |"
01415|            )
01416|
01417|    lines.extend([
01418|        "",
01419|        "## Nota",
01420|        "Este reporte muestra la meta mensual de respuesta a requerimientos, el resultado observado y su impacto en el puntaje total del mes.",
01421|        "",
01422|    ])
01423|    return "\n".join(lines)
01424|
01425|
01426|@login_required
01427|def respuesta_reqs_export_md(request):
01428|    report_filter = _get_report_filter(request)
01429|    report_sort = get_report_sort(request)
01430|    periods = _build_period_range(
01431|        report_filter["start_year"],
01432|        report_filter["start_month"],
01433|        report_filter["month_count"],
01434|    )
01435|    metric, rows = _get_respuesta_reqs_rows(periods=periods)
01436|    rows = sort_report_rows(rows, report_sort)
01437|
01438|    content = _build_respuesta_reqs_markdown(rows, report_filter)
01439|
01440|    generated_suffix = datetime.now().strftime("%Y%m%d-%H%M")
01441|    start_year = report_filter["start_year"]
01442|    start_month = report_filter["start_month"]
01443|    month_count = report_filter["month_count"]
01444|    filename = (
01445|        f"pgc-respuesta-reqs-"
01446|        f"fy{start_year}-m{start_month:02d}-n{month_count}-"
01447|        f"{generated_suffix}.md"
01448|    )
01449|
01450|    response = HttpResponse(
01451|        smart_str(content),
01452|        content_type="text/plain; charset=utf-8",
01453|    )
01454|    response["Content-Disposition"] = f'attachment; filename="{filename}"'
01455|    return response
01456|
01457|
01458|def _get_ingresos_rows(periods=None):
01459|
01460|    investment_une = get_investment_une()
01461|    fx_map = build_fx_map()
01462|    investment_real_map = investment_real_map_for_periods(
01463|        periods, une=investment_une, fx_map=fx_map
01464|    )
01465|
01466|  
01467|    try:
01468|        metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_INGRESOS)
01469|    except MetricDefinition.DoesNotExist:
01470|        metric = None
01471|
01472|    targets = MonthlyTarget.objects.select_related("une", "plan", "metric").filter(
01473|        metric__code=MetricDefinition.CODE_INGRESOS
01474|    )
01475|    results = MonthlyMetricResult.objects.select_related("une", "plan", "metric").filter(
01476|        metric__code=MetricDefinition.CODE_INGRESOS
01477|    )
01478|    scorecards = MonthlyScorecard.objects.select_related("une", "plan")
01479|
01480|    if periods:
01481|        period_q = _build_period_q(periods)
01482|        targets = targets.filter(period_q)
01483|        results = results.filter(period_q)
01484|        scorecards = scorecards.filter(period_q)
01485|
01486|    result_map = {}
01487|    for r in results:
01488|        key = (r.plan_id, r.une_id, r.year, r.month)
01489|        result_map[key] = r
01490|
01491|    score_map = {}
01492|    for sc in scorecards:
01493|        key = (sc.plan_id, sc.une_id, sc.year, sc.month)
01494|        score_map[key] = sc
01495|
01496|    rows = []
01497|    for target in targets.order_by("-year", "-month", "une__sort_order", "une__name_es"):
01498|        key = (target.plan_id, target.une_id, target.year, target.month)
01499|        result = result_map.get(key)
01500|        scorecard = score_map.get(key)
01501|
01502|        meta = target.target_value if target.target_value is not None else None
01503|        real = result.measured_value if result and result.measured_value is not None else None
01504|
01505|        investment_codes = {"INVESTMENT", "INVESTMENTS", "INVERSIONES"}
01506|        
01507|        if target.une.code in investment_codes:
01508|            real = investment_real_map.get(
01509|                (target.year, target.month, target.une_id),
01510|                Decimal("0"),
01511|            )
01512|
01513|        # Insurance siempre con 3 decimales
01514|        if target.une.code == "INSURANCE":
01515|            if meta is not None:
01516|                meta = meta.quantize(Decimal("0.001"), rounding=ROUND_DOWN)
01517|            if real is not None:
01518|                real = real.quantize(Decimal("0.001"), rounding=ROUND_DOWN)
01519|
01520|        if meta is not None and real is not None:
01521|            diferencia = real - meta
01522|            if target.une.code == "INSURANCE":
01523|                diferencia = diferencia.quantize(Decimal("0.001"), rounding=ROUND_DOWN)
01524|        else:
01525|            diferencia = None
01526|
01527|        if target.une.code in {"INVESTMENT", "INVESTMENTS", "INVERSIONES"}:
01528|            metodo = "Suma de montos del archivo de clientes nuevos del mes"
01529|            observacion = (
01530|                "En Investment, el ingreso del score mensual se calcula como la suma "
01531|                "de montos de todos los registros del archivo de clientes del mes."
01532|            )
01533|            observacion_base = observacion
01534|            tc_label = ""
01535|        else:
01536|            metodo = "Estado de resultados"
01537|            observacion = ""
01538|            observacion_base = ""
01539|            tc_label = ""
01540|            if result and result.calculation_note:
01541|                note = result.calculation_note.strip()
01542|
01543|                base_note = note
01544|                tc_text = ""
01545|
01546|                if "[FX_APPLIED]" in note and "GTQ a USD:" in note:
01547|                    base_note = note.split("[FX_APPLIED]")[0].strip()
01548|
01549|                    try:
01550|                        fx_part = note.split("/")[1].split("=")[0].strip()
01551|                        fx_value = Decimal(fx_part).quantize(Decimal("0.001"), rounding=ROUND_DOWN)
01552|                        tc_text = f"TC {fx_value}"
01553|                    except Exception:
01554|                        tc_text = ""
01555|
01556|                if base_note and tc_text:
01557|                    observacion = f"{base_note} {tc_text}"
01558|                elif base_note:
01559|                    observacion = base_note
01560|                elif tc_text:
01561|                    observacion = tc_text
01562|
01563|                observacion_base = base_note
01564|                tc_label = tc_text
01565|
01566|        # Presentación: TC desde captura manual GTQ→USD si no vino en calculation_note.
01567|        if not tc_label and result and getattr(result, "exchange_rate_used", None):
01568|            try:
01569|                tc_label = f"TC {Decimal(result.exchange_rate_used).quantize(Decimal('0.001'), rounding=ROUND_DOWN)}"
01570|            except Exception:
01571|                tc_label = f"TC {result.exchange_rate_used}"
01572|
01573|        if not tc_label and observacion:
01574|            m = re.search(r"TC[= ]\s*([0-9]+(?:\.[0-9]+)?)", observacion, flags=re.IGNORECASE)
01575|            if m:
01576|                tc_label = f"TC {m.group(1)}"
01577|
01578|        # Evitar duplicar el TC en el texto cuando ya hay badge.
01579|        display_base = observacion_base or observacion or ""
01580|        if tc_label and display_base:
01581|            display_base = re.sub(
01582|                r"\s*TC[= ]\s*[0-9]+(?:\.[0-9]+)?\s*",
01583|                " ",
01584|                display_base,
01585|                flags=re.IGNORECASE,
01586|            ).strip()
01587|
01588|        source_gtq = None
01589|        if (
01590|            result
01591|            and getattr(result, "source_currency", "") == "GTQ"
01592|            and getattr(result, "source_value", None) is not None
01593|        ):
01594|            source_gtq = result.source_value
01595|
01596|        rows.append({
01597|            "target": target,
01598|            "result": result,
01599|            "scorecard": scorecard,
01600|            "meta": meta,
01601|            "real": real,
01602|            "diferencia": diferencia,
01603|            "cumple": result.is_achieved if result else False,
01604|            "metodo": metodo,
01605|            "observacion": observacion,
01606|            "observacion_base": display_base,
01607|            "tc_label": tc_label,
01608|            "source_gtq": source_gtq,
01609|            "is_insurance": target.une.code == "INSURANCE",  # Flag para el template
01610|        })
01611|
01612|    return metric, rows
01613|
01614|
01615|def build_ingresos_markdown(rows, report_filter):
01616|    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
01617|
01618|    start_year = report_filter["start_year"]
01619|    start_month = report_filter["start_month"]
01620|    month_count = report_filter["month_count"]
01621|    periods = _build_period_range(start_year, start_month, month_count)
01622|    end_year, end_month = periods[-1]
01623|
01624|    lines = [
01625|        "# PGC - Ingresos vs meta por UNE",
01626|        "",
01627|        f"Generado: {generated_at}",
01628|        "",
01629|        "## Filtros",
01630|        f"- Desde: {start_year}-{start_month:02d}",
01631|        f"- Hasta: {end_year}-{end_month:02d}",
01632|        f"- Meses incluidos: {month_count}",
01633|        "",
01634|        "## Datos",
01635|        "",
01636|        "| UNE | Periodo | Meta USD | Real USD | Dif. USD | Cumple | Método de cálculo | Observación |",
01637|        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
01638|    ]
01639|
01640|    if not rows:
01641|        lines.append("| Sin datos | - | - | - | - | - | - | - |")
01642|    else:
01643|        for row in rows:
01644|            if row.get("is_separator"):
01645|                continue
01646|
01647|            target = row["target"]
01648|            period = f"{target.year}-{target.month:02d}"
01649|            meta = row["meta"]
01650|            real = row["real"]
01651|            diferencia = row["diferencia"]
01652|            
01653|            # Insurance con 3 decimales en MD
01654|            is_insurance = target.une.code == "INSURANCE"
01655|            
01656|            if is_insurance:
01657|                meta_txt = f"{meta:.3f}" if meta is not None else "-"
01658|                real_txt = f"{real:.3f}" if real is not None else "-"
01659|                diferencia_txt = f"{diferencia:.3f}" if diferencia is not None else "-"
01660|            else:
01661|                meta_txt = f"{int(meta)}" if meta is not None else "-"
01662|                real_txt = f"{int(real)}" if real is not None else "-"
01663|                diferencia_txt = f"{int(diferencia)}" if diferencia is not None else "-"
01664|            
01665|            lines.append(
01666|                f"| {target.une.name_es if hasattr(target.une, 'name_es') else target.une.name_es} | "
01667|                f"{period} | "
01668|                f"{meta_txt} | "
01669|                f"{real_txt} | "
01670|                f"{diferencia_txt} | "
01671|                f"{'Sí' if row['cumple'] else 'No'} | "
01672|                f"{row['metodo']} | "
01673|                f"{row['observacion'] or '-'} |"
01674|            )
01675|
01676|    lines.extend([
01677|        "",
01678|        "## Nota",
01679|        "Este reporte muestra la meta de ingresos, el valor real observado y el método usado para explicar el puntaje mensual.",
01680|        "Insurance se presenta siempre con 3 decimales.",
01681|        "",
01682|    ])
01683|    return "\n".join(lines)
01684|
01685|
01686|@login_required
01687|def ingresos_report(request):
01688|    report_filter = _get_report_filter(request)
01689|    report_sort = get_report_sort(request)
01690|
01691|    periods = _build_period_range(
01692|        report_filter["start_year"],
01693|        report_filter["start_month"],
01694|        report_filter["month_count"],
01695|    )
01696|
01697|    metric, rows = _get_ingresos_rows(periods=periods)
01698|    rows = sort_ingresos_rows(rows, report_sort)
01699|
01700|    context = {
01701|        "rows": rows,
01702|        "metric": metric,
01703|        "report_filter": report_filter,
01704|        "report_sort": report_sort,
01705|        "available_periods": _get_available_periods(),
01706|        "month_count_options": MONTH_COUNT_OPTIONS,
01707|    }
01708|
01709|    return render(request, "pgc/ingresos.html", context)
01710|
01711|
01712|@login_required
01713|def ingresos_export_md(request):
01714|    report_filter = _get_report_filter(request)
01715|    report_sort = get_report_sort(request)
01716|
01717|    periods = _build_period_range(
01718|        report_filter["start_year"],
01719|        report_filter["start_month"],
01720|        report_filter["month_count"],
01721|    )
01722|
01723|    metric, rows = _get_ingresos_rows(periods=periods)
01724|    rows = sort_ingresos_rows(rows, report_sort)
01725|
01726|    content = build_ingresos_markdown(rows, report_filter)
01727|
01728|    generated_suffix = datetime.now().strftime("%Y%m%d-%H%M")
01729|    start_year = report_filter["start_year"]
01730|    start_month = report_filter["start_month"]
01731|    month_count = report_filter["month_count"]
01732|
01733|    filename = (
01734|        f"pgc-ingresos-vs-meta-"
01735|        f"fy{start_year}-m{start_month:02d}-n{month_count}-"
01736|        f"{generated_suffix}.md"
01737|    )
01738|
01739|    response = HttpResponse(
01740|        smart_str(content),
01741|        content_type="text/plain; charset=utf-8",
01742|    )
01743|    response["Content-Disposition"] = f'attachment; filename="{filename}"'
01744|    return response
01745|
01746|
01747|def user_can_view_une_summary(user, une):
01748|    if user.is_superuser:
01749|        return True
01750|    profile = getattr(user, "profile", None)  # related_name real
01751|    if profile and profile.default_all_une_access:
01752|        return True
01753|    return user.une_permissions.filter(une=une, can_view_summary=True).exists()
01754|
01755|
01756|def user_can_view_une_detail(user, une):
01757|    if user.is_superuser:
01758|        return True
01759|    profile = getattr(user, "profile", None)
01760|    if profile and profile.default_all_une_access:
01761|        # si decides que este flag también implica ver detalle
01762|        return True
01763|    return user.une_permissions.filter(une=une, can_view_detail=True).exists()
01764|
01765|
01766|def user_can_view_detail(user, une):
01767|    if user.is_superuser:
01768|        return True
01769|
01770|    profile = getattr(user, "profile", None)
01771|    if profile and getattr(profile, "default_all_une_access", False):
01772|        return True
01773|
01774|    return UserUNEPermission.objects.filter(
01775|        user=user,
01776|        une=une,
01777|        can_view_detail=True,
01778|    ).exists()
01779|
01780|
01781|@login_required
01782|def clientes_nuevos_detail(request):
01783|
01784|    une_id = request.GET.get("une_id")
01785|    year_raw = request.GET.get("year")
01786|    month_raw = request.GET.get("month")
01787|    
01788|    if not une_id or not year_raw or not month_raw:
01789|        raise Http404("Faltan parámetros obligatorios: une_id, year, month.")
01790|    
01791|    try:
01792|        une_id = int(une_id)
01793|        year = int(year_raw)
01794|        month = int(month_raw)
01795|    except (TypeError, ValueError):
01796|        raise Http404("Parámetros inválidos: une_id, year, month.")
01797|
01798|    if month < 1 or month > 12:
01799|        raise Http404("Mes inválido.")
01800|
01801|    une = get_object_or_404(UNE, pk=une_id)
01802|
01803|    if not user_can_view_detail(request.user, une):
01804|        return HttpResponseForbidden("No tienes permiso para ver detalle de esta UNE.")
01805|
01806|    rows_queryset = (
01807|        NewClientImportRow.objects
01808|        .select_related("header", "currency", "une")
01809|        .filter(une=une)
01810|        .filter(
01811|            Q(header__year=year, header__month=month) |
01812|            Q(year=year, month=month)
01813|        )
01814|        .order_by("client_name", "operation_code", "id")
01815|    )
01816|
01817|    detail_rows = []
01818|    for row in rows_queryset:
01819|        detail_rows.append({
01820|            "id": row.id,
01821|            "client_name": row.client_name or "",
01822|            "nit": row.nit or "",
01823|            "operation_code": row.operation_code or "",
01824|            "currency_code": row.currency.code if row.currency else "",
01825|            "amount": row.amount,
01826|            "previous_contracts": row.previous_contracts,
01827|            "counts_as_new": row.counts_as_new,
01828|            "raw_une_value": row.raw_une_value or "",
01829|            "observations": row.observations or "",
01830|            "source_row_number": row.source_row_number,
01831|            "header_year": getattr(row.header, "year", None),
01832|            "header_month": getattr(row.header, "month", None),
01833|            "row_year": getattr(row, "year", None),
01834|            "row_month": getattr(row, "month", None),
01835|        })
01836|
01837|    fx_map = {
01838|      (item.year, item.month): item.usd_to_gtq
01839|      for item in MonthlyExchangeRate.objects.all()
01840|    }
01841|
01842|    investment_ingresos_total = Decimal("0")
01843|    for row in rows_queryset:
01844|        investment_ingresos_total += _convert_row_amount_to_usd(row, fx_map)
01845|  
01846|    context = {
01847|        "une": une,
01848|        "year": year,
01849|        "month": month,
01850|        "rows": detail_rows,
01851|        "row_count": len(detail_rows),
01852|        "investment_ingresos_total": investment_ingresos_total,
01853|    }
01854|
01855|    return render(request, "pgc/clientes_nuevos_detail.html", context)
01856|
01857|
01858|@login_required
01859|def venta_cruzada_detail(request):
01860|    year = request.GET.get("year")
01861|    month = request.GET.get("month")
01862|    une = request.GET.get("une")
01863|
01864|    rows = CrossSaleImportRow.objects.select_related(
01865|        "une_origin",
01866|        "une_destination",
01867|        "currency",
01868|    ).all()
01869|
01870|    if year:
01871|        rows = rows.filter(year=year)
01872|    if month:
01873|        rows = rows.filter(month=month)
01874|    if une:
01875|        rows = rows.filter(une_origin__code=une)
01876|
01877|    rows = rows.order_by(
01878|        "year",
01879|        "month",
01880|        "une_origin__sort_order",
01881|        "une_destination__sort_order",
01882|        "client_name",
01883|        "operation_code",
01884|    )
01885|
01886|    available_years = (
01887|        CrossSaleImportRow.objects.order_by("-year")
01888|        .values_list("year", flat=True)
01889|        .distinct()
01890|    )
01891|    unes = UNE.objects.order_by("sort_order")
01892|
01893|    context = {
01894|        "rows": rows,
01895|        "available_years": available_years,
01896|        "months": range(1, 13),
01897|        "unes": unes,
01898|        "selected_year": year or "",
01899|        "selected_month": month or "",
01900|        "selected_une": une or "",
01901|    }
01902|    return render(request, "pgc/venta_cruzada_detail.html", context)
01903|
01904|

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IyBwZ2Mvdmlld3MucHkKCmltcG9ydCBqc29uCmltcG9ydCByZQpmcm9tIC5tb2RlbHMgaW1wb3J0ICgKICAgIFBHQ1BsYW4sCiAgICBNb250aGx5TWV0cmljUmVzdWx0LAogICAgTW9udGhseVNjb3JlY2FyZCwKICAgIE1vbnRobHlUYXJnZXQsCiAgICBNb250aGx5TWV0cmljU2NvcmUsCiAgICBNb250aGx5TW9kZVNjb3JlY2FyZCwKICAgIE1vbnRobHlFeGNoYW5nZVJhdGUsCikKZnJvbSBhY2NvdW50cy5tb2RlbHMgaW1wb3J0IFVzZXJVTkVQZXJtaXNzaW9uCmZyb20gY29yZS5tb2RlbHMgaW1wb3J0IE1ldHJpY0RlZmluaXRpb24sIFVORSwgU3lzdGVtU2V0dGluZwoKZnJvbSBkYXRldGltZSBpbXBvcnQgZGF0ZXRpbWUKZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsLCBST1VORF9ET1dOLCBJbnZhbGlkT3BlcmF0aW9uCmZyb20gZGphbmdvLmNvbnRyaWIgaW1wb3J0IG1lc3NhZ2VzCmZyb20gZGphbmdvLmNvbnRyaWIuYXV0aC5kZWNvcmF0b3JzIGltcG9ydCBsb2dpbl9yZXF1aXJlZCwgdXNlcl9wYXNzZXNfdGVzdApmcm9tIGRqYW5nby5jb3JlLm1hbmFnZW1lbnQgaW1wb3J0IGNhbGxfY29tbWFuZApmcm9tIGRqYW5nby5kYi5tb2RlbHMgaW1wb3J0IFEKZnJvbSBkamFuZ28uaHR0cCBpbXBvcnQgSHR0cFJlc3BvbnNlLCBIdHRwUmVzcG9uc2VGb3JiaWRkZW4sIEh0dHA0MDQKZnJvbSBkamFuZ28uc2hvcnRjdXRzIGltcG9ydCBnZXRfb2JqZWN0X29yXzQwNCwgcmVuZGVyLCByZWRpcmVjdApmcm9tIGRqYW5nby50ZW1wbGF0ZS5sb2FkZXIgaW1wb3J0IGdldF90ZW1wbGF0ZQpmcm9tIGRqYW5nby51cmxzIGltcG9ydCByZXZlcnNlCmZyb20gZGphbmdvLnV0aWxzLmVuY29kaW5nIGltcG9ydCBzbWFydF9zdHIKZnJvbSBpbXBvcnRzLm1vZGVscyBpbXBvcnQgTmV3Q2xpZW50SW1wb3J0Um93LCBDcm9zc1NhbGVJbXBvcnRSb3cKCgpERUZBVUxUX01PTlRIX0NPVU5UID0gNApNQVhfTU9OVEhfQ09VTlQgPSAxMgoKUkVQT1JUX0RBVEVfT1JERVJfT1BUSU9OUyA9ICgiYXNjIiwgImRlc2MiKQpSRVBPUlRfR1JPVVBfTU9ERV9PUFRJT05TID0gKCJ1bmUiLCAicGVyaW9kIikKCkRFRkFVTFRfUkVQT1JUX0RBVEVfT1JERVIgPSAiYXNjIgpERUZBVUxUX1JFUE9SVF9HUk9VUF9NT0RFID0gInVuZSIKCnJlcG9ydF91bmVfb3JkZXIgPSB7CiAgICAiRkFDVE9SSU5HIjogMSwKICAgICJGQUNUT1JBSkUiOiAxLAogICAgIkxFQVNJTkciOiAyLAogICAgIklOU1VSQU5DRSI6IDMsCiAgICAiSU5WRVNUTUVOVCI6IDQsCiAgICAiSU5WRVNUTUVOVFMiOiA0LAogICAgIklOVkVSU0lPTkVTIjogNCwKfQoKUEdDX01PREVfS0VZID0gInBnYy5tb2RlIgpQR0NfREVGQVVMVF9NT0RFID0gIm1vZG8xIgpQR0NfTU9ERV9PUFRJT05TID0gKCJtb2RvMSIsICJtb2RvMiIpClBHQ19NT0RFX0xBQkVMUyA9IHsKICAgICJtb2RvMSI6ICIxLkFic29sdXRvcyIsCiAgICAibW9kbzIiOiAiMi5Qcm9wb3JjacOzbiIsCn0KREVGQVVMVF9QR0NfTU9ERSA9ICJtb2RvMSIKCgpmcm9tIHBnYy5pbnZlc3RtZW50X2luZ3Jlc29zIGltcG9ydCAoCiAgICBidWlsZF9meF9tYXAsCiAgICBjb252ZXJ0X3Jvd19hbW91bnRfdG9fdXNkLAogICAgZ2V0X2ludmVzdG1lbnRfdW5lLAogICAgaW52ZXN0bWVudF9yZWFsX21hcF9mb3JfcGVyaW9kcywKKQoKCmRlZiBfY29udmVydF9yb3dfYW1vdW50X3RvX3VzZChyb3csIGZ4X21hcCk6CiAgICAiIiJDb21wYXQ6IGRlbGVnYSBhbCBoZWxwZXIgY29tcGFydGlkbyBjb24gbGEgdmlzdGEvY29tYW5kbyBkZSBJbnZlc3RtZW50LiIiIgogICAgcmV0dXJuIGNvbnZlcnRfcm93X2Ftb3VudF90b191c2Qocm93LCBmeF9tYXApCiAgCgpkZWYgX2dldF9wZ2NfbW9kZShyZXF1ZXN0KToKICAgIHJhd19tb2RlID0gKHJlcXVlc3QuR0VULmdldCgibW9kZSIpIG9yIHJlcXVlc3Quc2Vzc2lvbi5nZXQoInBnY19tb2RlIikgb3IgREVGQVVMVF9QR0NfTU9ERSkuc3RyaXAoKS5sb3dlcigpCgogICAgaWYgcmF3X21vZGUgbm90IGluIFBHQ19NT0RFX09QVElPTlM6CiAgICAgICAgcmF3X21vZGUgPSBERUZBVUxUX1BHQ19NT0RFCgogICAgcmVxdWVzdC5zZXNzaW9uWyJwZ2NfbW9kZSJdID0gcmF3X21vZGUKICAgIHJldHVybiByYXdfbW9kZQogIAoKZGVmIGdldF9wZ2NfbW9kZSgpOgogICAgc2V0dGluZyA9IFN5c3RlbVNldHRpbmcub2JqZWN0cy5maWx0ZXIoa2V5PVBHQ19NT0RFX0tFWSkuZmlyc3QoKQogICAgaWYgbm90IHNldHRpbmcgb3Igbm90IHNldHRpbmcudmFsdWVfdGV4dDoKICAgICAgICByZXR1cm4gUEdDX0RFRkFVTFRfTU9ERQogICAgdmFsdWUgPSBzZXR0aW5nLnZhbHVlX3RleHQuc3RyaXAoKS5sb3dlcigpCiAgICByZXR1cm4gdmFsdWUgaWYgdmFsdWUgaW4gKCJtb2RvMSIsICJtb2RvMiIpIGVsc2UgUEdDX0RFRkFVTFRfTU9ERQoKZGVmIHNldF9wZ2NfbW9kZShtb2RlOiBzdHIpOgogICAgaWYgbW9kZSBub3QgaW4gKCJtb2RvMSIsICJtb2RvMiIpOgogICAgICAgIG1vZGUgPSBQR0NfREVGQVVMVF9NT0RFCiAgICBTeXN0ZW1TZXR0aW5nLm9iamVjdHMudXBkYXRlX29yX2NyZWF0ZSgKICAgICAgICBrZXk9UEdDX01PREVfS0VZLAogICAgICAgIGRlZmF1bHRzPXsidmFsdWVfdGV4dCI6IG1vZGV9LAogICAgKQoKCmRlZiBnZXRfZGVmYXVsdF9tb250aF9jb3VudChub3c9Tm9uZSk6CiAgICAiIiJNZXNlcyBpbmNsdWlkb3MgcG9yIGRlZmVjdG86IGVuZXJvIOKGkiBtZXMgaW5tZWRpYXRvIGFudGVyaW9yIGFsIGFjdHVhbC4iIiIKICAgIG5vdyA9IG5vdyBvciBkYXRldGltZS5ub3coKQogICAgY291bnQgPSBub3cubW9udGggLSAxCiAgICBpZiBjb3VudCA8IDE6CiAgICAgICAgIyBFbiBlbmVybyBubyBoYXkgbWVzIHByZXZpbyBkZWwgYcOxbyBlbiBjdXJzbzsgbW9zdHJhciBhbCBtZW5vcyAxLgogICAgICAgIGNvdW50ID0gMQogICAgaWYgY291bnQgPiBNQVhfTU9OVEhfQ09VTlQ6CiAgICAgICAgY291bnQgPSBNQVhfTU9OVEhfQ09VTlQKICAgIHJldHVybiBjb3VudAoKCmRlZiBnZXRfZGVmYXVsdF9yZXBvcnRfc3RhcnQobm93PU5vbmUpOgogICAgIiIiRGVzZGUgcG9yIGRlZmVjdG86IGVuZXJvIGRlbCBhw7FvIGVuIGN1cnNvLiIiIgogICAgbm93ID0gbm93IG9yIGRhdGV0aW1lLm5vdygpCiAgICByZXR1cm4gbm93LnllYXIsIDEKCgpkZWYgZ2V0X2FjdGl2ZV9wZ2NfcGxhbigpOgogICAgcGxhbiA9IFBHQ1BsYW4ub2JqZWN0cy5maWx0ZXIoaXNfYWN0aXZlPVRydWUpLm9yZGVyX2J5KCIteWVhciIpLmZpcnN0KCkKICAgIGlmIHBsYW46CiAgICAgICAgcmV0dXJuIHBsYW4KICAgIHJldHVybiBQR0NQbGFuLm9iamVjdHMub3JkZXJfYnkoIi15ZWFyIikuZmlyc3QoKQoKCmRlZiBwYXJzZV9kZWNpbWFsX29yX25vbmUocmF3X3ZhbHVlKToKICAgIGlmIHJhd192YWx1ZSBpcyBOb25lOgogICAgICAgIHJldHVybiBOb25lCgogICAgdGV4dCA9IHN0cihyYXdfdmFsdWUpLnN0cmlwKCkKICAgIGlmIHRleHQgPT0gIiI6CiAgICAgICAgcmV0dXJuIE5vbmUKCiAgICB0ZXh0ID0gdGV4dC5yZXBsYWNlKCIgIiwgIiIpCgogICAgaWYgIiwiIGluIHRleHQgYW5kICIuIiBpbiB0ZXh0OgogICAgICAgIHRleHQgPSB0ZXh0LnJlcGxhY2UoIiwiLCAiIikKICAgIGVsaWYgIiwiIGluIHRleHQ6CiAgICAgICAgdGV4dCA9IHRleHQucmVwbGFjZSgiLCIsICIuIikKCiAgICB0cnk6CiAgICAgICAgcmV0dXJuIERlY2ltYWwodGV4dCkKICAgIGV4Y2VwdCAoSW52YWxpZE9wZXJhdGlvbiwgVmFsdWVFcnJvcik6CiAgICAgICAgcmV0dXJuIE5vbmUKCgpkZWYgX2dldF9hY3RpdmVfcGdjX3BsYW4oKToKICAgIHJldHVybiBnZXRfYWN0aXZlX3BnY19wbGFuKCkKICAKCmRlZiBfZ2V0X2Rhc2hib2FyZF9yb3dzKHBlcmlvZHM9Tm9uZSwgbW9kZT1ERUZBVUxUX1BHQ19NT0RFKToKICAgIGFjdGl2ZV9wbGFuID0gX2dldF9hY3RpdmVfcGdjX3BsYW4oKQogICAgaWYgbm90IGFjdGl2ZV9wbGFuOgogICAgICAgIHJldHVybiBbXQoKICAgIHNjb3JlY2FyZHMgPSAoCiAgICAgICAgTW9udGhseU1vZGVTY29yZWNhcmQub2JqZWN0cwogICAgICAgIC5zZWxlY3RfcmVsYXRlZCgidW5lIiwgInBsYW4iKQogICAgICAgIC5maWx0ZXIocGxhbj1hY3RpdmVfcGxhbiwgbW9kZT1tb2RlKQogICAgICAgIC5vcmRlcl9ieSgiLXllYXIiLCAiLW1vbnRoIiwgInVuZV9fc29ydF9vcmRlciIsICJ1bmVfX25hbWVfZXMiKQogICAgKQoKICAgIG1ldHJpY19yZXN1bHRzID0gKAogICAgICAgIE1vbnRobHlNZXRyaWNTY29yZS5vYmplY3RzCiAgICAgICAgLnNlbGVjdF9yZWxhdGVkKCJ1bmUiLCAibWV0cmljIiwgInBsYW4iKQogICAgICAgIC5maWx0ZXIocGxhbj1hY3RpdmVfcGxhbiwgbW9kZT1tb2RlKQogICAgKQoKICAgIGlmIHBlcmlvZHM6CiAgICAgICAgcGVyaW9kX3EgPSBfYnVpbGRfcGVyaW9kX3EocGVyaW9kcykKICAgICAgICBzY29yZWNhcmRzID0gc2NvcmVjYXJkcy5maWx0ZXIocGVyaW9kX3EpCiAgICAgICAgbWV0cmljX3Jlc3VsdHMgPSBtZXRyaWNfcmVzdWx0cy5maWx0ZXIocGVyaW9kX3EpCgogICAgdXNlX2xlZ2FjeSA9IG5vdCBzY29yZWNhcmRzLmV4aXN0cygpCgogICAgaWYgdXNlX2xlZ2FjeToKICAgICAgICBzY29yZWNhcmRzID0gKAogICAgICAgICAgICBNb250aGx5U2NvcmVjYXJkLm9iamVjdHMKICAgICAgICAgICAgLnNlbGVjdF9yZWxhdGVkKCJ1bmUiLCAicGxhbiIpCiAgICAgICAgICAgIC5maWx0ZXIocGxhbj1hY3RpdmVfcGxhbikKICAgICAgICAgICAgLm9yZGVyX2J5KCIteWVhciIsICItbW9udGgiLCAidW5lX19zb3J0X29yZGVyIiwgInVuZV9fbmFtZV9lcyIpCiAgICAgICAgKQoKICAgICAgICBtZXRyaWNfcmVzdWx0cyA9ICgKICAgICAgICAgICAgTW9udGhseU1ldHJpY1Jlc3VsdC5vYmplY3RzCiAgICAgICAgICAgIC5zZWxlY3RfcmVsYXRlZCgidW5lIiwgIm1ldHJpYyIsICJwbGFuIikKICAgICAgICAgICAgLmZpbHRlcihwbGFuPWFjdGl2ZV9wbGFuKQogICAgICAgICkKCiAgICAgICAgaWYgcGVyaW9kczoKICAgICAgICAgICAgcGVyaW9kX3EgPSBfYnVpbGRfcGVyaW9kX3EocGVyaW9kcykKICAgICAgICAgICAgc2NvcmVjYXJkcyA9IHNjb3JlY2FyZHMuZmlsdGVyKHBlcmlvZF9xKQogICAgICAgICAgICBtZXRyaWNfcmVzdWx0cyA9IG1ldHJpY19yZXN1bHRzLmZpbHRlcihwZXJpb2RfcSkKCiAgICBtZXRyaWNfbWFwID0ge30KICAgIGZvciBtZXRyaWNfcmVzdWx0IGluIG1ldHJpY19yZXN1bHRzOgogICAgICAgIGtleSA9ICgKICAgICAgICAgICAgbWV0cmljX3Jlc3VsdC5wbGFuX2lkLAogICAgICAgICAgICBtZXRyaWNfcmVzdWx0LnVuZV9pZCwKICAgICAgICAgICAgbWV0cmljX3Jlc3VsdC55ZWFyLAogICAgICAgICAgICBtZXRyaWNfcmVzdWx0Lm1vbnRoLAogICAgICAgICkKICAgICAgICBtZXRyaWNfbWFwLnNldGRlZmF1bHQoa2V5LCB7fSkKICAgICAgICBtZXRyaWNfbWFwW2tleV1bbWV0cmljX3Jlc3VsdC5tZXRyaWMuY29kZV0gPSBtZXRyaWNfcmVzdWx0CgogICAgcm93cyA9IFtdCiAgICBmb3Igc2NvcmVjYXJkIGluIHNjb3JlY2FyZHM6CiAgICAgICAga2V5ID0gKAogICAgICAgICAgICBzY29yZWNhcmQucGxhbl9pZCwKICAgICAgICAgICAgc2NvcmVjYXJkLnVuZV9pZCwKICAgICAgICAgICAgc2NvcmVjYXJkLnllYXIsCiAgICAgICAgICAgIHNjb3JlY2FyZC5tb250aCwKICAgICAgICApCiAgICAgICAgbWV0cmljcyA9IG1ldHJpY19tYXAuZ2V0KGtleSwge30pCgogICAgICAgIHJvd3MuYXBwZW5kKAogICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAic2NvcmVjYXJkIjogc2NvcmVjYXJkLAogICAgICAgICAgICAgICAgInllYXIiOiBzY29yZWNhcmQueWVhciwKICAgICAgICAgICAgICAgICJtb250aCI6IHNjb3JlY2FyZC5tb250aCwKICAgICAgICAgICAgICAgICJ1bmUiOiBzY29yZWNhcmQudW5lLAogICAgICAgICAgICAgICAgInBfaW5ncmVzb3MiOiBnZXRhdHRyKAogICAgICAgICAgICAgICAgICAgIG1ldHJpY3MuZ2V0KE1ldHJpY0RlZmluaXRpb24uQ09ERV9JTkdSRVNPUyksCiAgICAgICAgICAgICAgICAgICAgInBvaW50c19hd2FyZGVkIiwKICAgICAgICAgICAgICAgICAgICAwLAogICAgICAgICAgICAgICAgKSwKICAgICAgICAgICAgICAgICJwX2NsaWVudGVzIjogZ2V0YXR0cigKICAgICAgICAgICAgICAgICAgICBtZXRyaWNzLmdldChNZXRyaWNEZWZpbml0aW9uLkNPREVfQ0xJRU5URVNfTlVFVk9TKSwKICAgICAgICAgICAgICAgICAgICAicG9pbnRzX2F3YXJkZWQiLAogICAgICAgICAgICAgICAgICAgIDAsCiAgICAgICAgICAgICAgICApLAogICAgICAgICAgICAgICAgInBfdmVudGFfY3J1emFkYSI6IGdldGF0dHIoCiAgICAgICAgICAgICAgICAgICAgbWV0cmljcy5nZXQoTWV0cmljRGVmaW5pdGlvbi5DT0RFX1ZFTlRBX0NSVVpBREEpLAogICAgICAgICAgICAgICAgICAgICJwb2ludHNfYXdhcmRlZCIsCiAgICAgICAgICAgICAgICAgICAgMCwKICAgICAgICAgICAgICAgICksCiAgICAgICAgICAgICAgICAicF9yZXNwdWVzdGFfcmVxcyI6IGdldGF0dHIoCiAgICAgICAgICAgICAgICAgICAgbWV0cmljcy5nZXQoTWV0cmljRGVmaW5pdGlvbi5DT0RFX1JFU1BVRVNUQV9SRVFTKSwKICAgICAgICAgICAgICAgICAgICAicG9pbnRzX2F3YXJkZWQiLAogICAgICAgICAgICAgICAgICAgIDAsCiAgICAgICAgICAgICAgICApLAogICAgICAgICAgICAgICAgInRvdGFsX3BvaW50cyI6IGdldGF0dHIoc2NvcmVjYXJkLCAidG90YWxfcG9pbnRzIiwgMCksCiAgICAgICAgICAgICAgICAiaXNfbW9udGhfcXVhbGlmaWVkIjogZ2V0YXR0cihzY29yZWNhcmQsICJpc19tb250aF9xdWFsaWZpZWQiLCBGYWxzZSksCiAgICAgICAgICAgIH0KICAgICAgICApCgogICAgcmV0dXJuIHJvd3MKCgoKZGVmIGdldF9yZXBvcnRfcm93X21ldGEocm93KToKICAgIGlmIHJvdy5nZXQoImlzX3NlcGFyYXRvciIpOgogICAgICAgIHJldHVybiBOb25lCgogICAgc291cmNlID0gcm93LmdldCgidGFyZ2V0Iikgb3Igcm93LmdldCgic2NvcmVjYXJkIikgb3Igcm93LmdldCgicmVzdWx0IikKICAgIGlmIHNvdXJjZSBpcyBOb25lOgogICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoIk5vIHNlIHB1ZG8gaW5mZXJpciB0YXJnZXQsIHNjb3JlY2FyZCBvIHJlc3VsdCBwYXJhIG9yZGVuYXIgbGEgZmlsYS4iKQoKICAgIHVuZSA9IGdldGF0dHIoc291cmNlLCAidW5lIiwgTm9uZSkKICAgIHllYXIgPSBnZXRhdHRyKHNvdXJjZSwgInllYXIiLCBOb25lKQogICAgbW9udGggPSBnZXRhdHRyKHNvdXJjZSwgIm1vbnRoIiwgTm9uZSkKCiAgICB1bmVfY29kZSA9IChnZXRhdHRyKHVuZSwgImNvZGUiLCAiIikgb3IgIiIpLnVwcGVyKCkKICAgIHVuZV9uYW1lID0gKAogICAgICAgIGdldGF0dHIodW5lLCAibmFtZV9lcyIsIE5vbmUpCiAgICAgICAgb3IgZ2V0YXR0cih1bmUsICJuYW1lIiwgTm9uZSkKICAgICAgICBvciB1bmVfY29kZQogICAgKQoKICAgIHVuZV9zb3J0X29yZGVyID0gcmVwb3J0X3VuZV9vcmRlci5nZXQodW5lX2NvZGUpCiAgICBpZiB1bmVfc29ydF9vcmRlciBpcyBOb25lOgogICAgICAgIHVuZV9zb3J0X29yZGVyID0gZ2V0YXR0cih1bmUsICJzb3J0X29yZGVyIiwgTm9uZSkKICAgIGlmIHVuZV9zb3J0X29yZGVyIGlzIE5vbmU6CiAgICAgICAgdW5lX3NvcnRfb3JkZXIgPSBnZXRhdHRyKHVuZSwgInNvcnRfb3JkZXIiLCBOb25lKQogICAgaWYgdW5lX3NvcnRfb3JkZXIgaXMgTm9uZToKICAgICAgICB1bmVfc29ydF9vcmRlciA9IDk5OTk5OQoKICAgIHJldHVybiB7CiAgICAgICAgInVuZV9jb2RlIjogdW5lX2NvZGUsCiAgICAgICAgInVuZV9uYW1lIjogdW5lX25hbWUsCiAgICAgICAgInVuZV9zb3J0X29yZGVyIjogdW5lX3NvcnRfb3JkZXIsCiAgICAgICAgInllYXIiOiB5ZWFyLAogICAgICAgICJtb250aCI6IG1vbnRoLAogICAgfQoKCmRlZiBzb3J0X3JlcG9ydF9yb3dzKHJvd3MsIHJlcG9ydF9zb3J0KToKICAgIGRhdGVfb3JkZXIgPSByZXBvcnRfc29ydFsiZGF0ZV9vcmRlciJdCiAgICBncm91cF9tb2RlID0gcmVwb3J0X3NvcnRbImdyb3VwX21vZGUiXQogICAgcmV2ZXJzZV9kYXRlID0gZGF0ZV9vcmRlciA9PSAiZGVzYyIKCiAgICBlbnJpY2hlZF9yb3dzID0gW10KICAgIGZvciByb3cgaW4gcm93czoKICAgICAgICByb3dfbWV0YSA9IGdldF9yZXBvcnRfcm93X21ldGEocm93KQogICAgICAgIGVucmljaGVkX3Jvd3MuYXBwZW5kKChyb3dfbWV0YSwgcm93KSkKCiAgICBpZiBncm91cF9tb2RlID09ICJ1bmUiOgogICAgICAgIGVucmljaGVkX3Jvd3Muc29ydCgKICAgICAgICAgICAga2V5PWxhbWJkYSBpdGVtOiAoCiAgICAgICAgICAgICAgICBpdGVtWzBdWyJ1bmVfc29ydF9vcmRlciJdLAogICAgICAgICAgICAgICAgaXRlbVswXVsidW5lX25hbWUiXS5sb3dlcigpLAogICAgICAgICAgICAgICAgLWl0ZW1bMF1bInllYXIiXSBpZiByZXZlcnNlX2RhdGUgZWxzZSBpdGVtWzBdWyJ5ZWFyIl0sCiAgICAgICAgICAgICAgICAtaXRlbVswXVsibW9udGgiXSBpZiByZXZlcnNlX2RhdGUgZWxzZSBpdGVtWzBdWyJtb250aCJdLAogICAgICAgICAgICApCiAgICAgICAgKQogICAgZWxzZToKICAgICAgICBlbnJpY2hlZF9yb3dzLnNvcnQoCiAgICAgICAgICAgIGtleT1sYW1iZGEgaXRlbTogKAogICAgICAgICAgICAgICAgLWl0ZW1bMF1bInllYXIiXSBpZiByZXZlcnNlX2RhdGUgZWxzZSBpdGVtWzBdWyJ5ZWFyIl0sCiAgICAgICAgICAgICAgICAtaXRlbVswXVsibW9udGgiXSBpZiByZXZlcnNlX2RhdGUgZWxzZSBpdGVtWzBdWyJtb250aCJdLAogICAgICAgICAgICAgICAgaXRlbVswXVsidW5lX3NvcnRfb3JkZXIiXSwKICAgICAgICAgICAgICAgIGl0ZW1bMF1bInVuZV9uYW1lIl0ubG93ZXIoKSwKICAgICAgICAgICAgKQogICAgICAgICkKCiAgICBzb3J0ZWRfcm93cyA9IFtyb3cgZm9yIF8sIHJvdyBpbiBlbnJpY2hlZF9yb3dzXQoKICAgIGlmIGdyb3VwX21vZGUgIT0gInVuZSI6CiAgICAgICAgcmV0dXJuIHNvcnRlZF9yb3dzCgogICAgc2VwYXJhdGVkX3Jvd3MgPSBbXQogICAgcHJldmlvdXNfdW5lX2tleSA9IE5vbmUKCiAgICBmb3Igcm93IGluIHNvcnRlZF9yb3dzOgogICAgICAgIHJvd19tZXRhID0gZ2V0X3JlcG9ydF9yb3dfbWV0YShyb3cpCiAgICAgICAgY3VycmVudF91bmVfa2V5ID0gKAogICAgICAgICAgICByb3dfbWV0YVsidW5lX3NvcnRfb3JkZXIiXSwKICAgICAgICAgICAgcm93X21ldGFbInVuZV9uYW1lIl0ubG93ZXIoKSwKICAgICAgICApCgogICAgICAgIGlmIHByZXZpb3VzX3VuZV9rZXkgaXMgbm90IE5vbmUgYW5kIGN1cnJlbnRfdW5lX2tleSAhPSBwcmV2aW91c191bmVfa2V5OgogICAgICAgICAgICBzZXBhcmF0ZWRfcm93cy5hcHBlbmQoeyJpc19zZXBhcmF0b3IiOiBUcnVlfSkKCiAgICAgICAgc2VwYXJhdGVkX3Jvd3MuYXBwZW5kKHJvdykKICAgICAgICBwcmV2aW91c191bmVfa2V5ID0gY3VycmVudF91bmVfa2V5CgogICAgcmV0dXJuIHNlcGFyYXRlZF9yb3dzCgoKZGVmIGdldF9yZXBvcnRfc29ydChyZXF1ZXN0KToKICAgIHJhd19kYXRlX29yZGVyID0gKAogICAgICAgIHJlcXVlc3QuR0VULmdldCgiZGF0ZV9vcmRlciIpCiAgICAgICAgb3IgIiIKICAgICkuc3RyaXAoKS5sb3dlcigpCgogICAgcmF3X2dyb3VwX21vZGUgPSAoCiAgICAgICAgcmVxdWVzdC5HRVQuZ2V0KCJncm91cF9tb2RlIikKICAgICAgICBvciAiIgogICAgKS5zdHJpcCgpLmxvd2VyKCkKCiAgICBzZXNzaW9uX2RhdGVfb3JkZXIgPSAoCiAgICAgICAgcmVxdWVzdC5zZXNzaW9uLmdldCgicGdjX3JlcG9ydF9kYXRlX29yZGVyIikKICAgICAgICBvciBERUZBVUxUX1JFUE9SVF9EQVRFX09SREVSCiAgICApLnN0cmlwKCkubG93ZXIoKQoKICAgIHNlc3Npb25fZ3JvdXBfbW9kZSA9ICgKICAgICAgICByZXF1ZXN0LnNlc3Npb24uZ2V0KCJwZ2NfcmVwb3J0X2dyb3VwX21vZGUiKQogICAgICAgIG9yIERFRkFVTFRfUkVQT1JUX0dST1VQX01PREUKICAgICkuc3RyaXAoKS5sb3dlcigpCgogICAgZGF0ZV9vcmRlciA9IHJhd19kYXRlX29yZGVyIG9yIHNlc3Npb25fZGF0ZV9vcmRlcgogICAgZ3JvdXBfbW9kZSA9IHJhd19ncm91cF9tb2RlIG9yIHNlc3Npb25fZ3JvdXBfbW9kZQoKICAgIGlmIGRhdGVfb3JkZXIgbm90IGluIFJFUE9SVF9EQVRFX09SREVSX09QVElPTlM6CiAgICAgICAgZGF0ZV9vcmRlciA9IERFRkFVTFRfUkVQT1JUX0RBVEVfT1JERVIKCiAgICBpZiBncm91cF9tb2RlIG5vdCBpbiBSRVBPUlRfR1JPVVBfTU9ERV9PUFRJT05TOgogICAgICAgIGdyb3VwX21vZGUgPSBERUZBVUxUX1JFUE9SVF9HUk9VUF9NT0RFCgogICAgcmVxdWVzdC5zZXNzaW9uWyJwZ2NfcmVwb3J0X2RhdGVfb3JkZXIiXSA9IGRhdGVfb3JkZXIKICAgIHJlcXVlc3Quc2Vzc2lvblsicGdjX3JlcG9ydF9ncm91cF9tb2RlIl0gPSBncm91cF9tb2RlCgogICAgcmV0dXJuIHsKICAgICAgICAiZGF0ZV9vcmRlciI6IGRhdGVfb3JkZXIsCiAgICAgICAgImdyb3VwX21vZGUiOiBncm91cF9tb2RlLAogICAgfQoKCmRlZiBnZXRfaW5ncmVzb3Nfcm93X21ldGEocm93KToKICAgIHNvdXJjZSA9IHJvdy5nZXQoInRhcmdldCIpIG9yIHJvdy5nZXQoInNjb3JlY2FyZCIpCiAgICBpZiBzb3VyY2UgaXMgTm9uZToKICAgICAgICByYWlzZSBLZXlFcnJvcigiTGEgZmlsYSBubyBjb250aWVuZSBuaSAndGFyZ2V0JyBuaSAnc2NvcmVjYXJkJy4iKQoKICAgIHVuZSA9IHNvdXJjZS51bmUKICAgIHVuZV9jb2RlID0gKGdldGF0dHIodW5lLCAiY29kZSIsICIiKSBvciAiIikudXBwZXIoKQogICAgdW5lX25hbWUgPSBnZXRhdHRyKHVuZSwgIm5hbWVfZXMiLCAiIikgaWYgaGFzYXR0cih1bmUsICJuYW1lX2VzIikgZWxzZSBnZXRhdHRyKHVuZSwgIm5hbWVfZXMiLCAiIikKCiAgICB1bmVfc29ydF9vcmRlciA9IHJlcG9ydF91bmVfb3JkZXIuZ2V0KHVuZV9jb2RlKQogICAgaWYgdW5lX3NvcnRfb3JkZXIgaXMgTm9uZToKICAgICAgICB1bmVfc29ydF9vcmRlciA9IGdldGF0dHIodW5lLCAic29ydF9vcmRlciIsIE5vbmUpIGlmIGhhc2F0dHIodW5lLCAic29ydF9vcmRlciIpIGVsc2UgZ2V0YXR0cih1bmUsICJzb3J0X29yZGVyIiwgTm9uZSkKICAgIGlmIHVuZV9zb3J0X29yZGVyIGlzIE5vbmU6CiAgICAgICAgdW5lX3NvcnRfb3JkZXIgPSA5OTk5OTkKCiAgICByZXR1cm4gewogICAgICAgICJ1bmVfY29kZSI6IHVuZV9jb2RlLAogICAgICAgICJ1bmVfbmFtZSI6IHVuZV9uYW1lIG9yIHVuZV9jb2RlLAogICAgICAgICJ1bmVfc29ydF9vcmRlciI6IHVuZV9zb3J0X29yZGVyLAogICAgICAgICJ5ZWFyIjogc291cmNlLnllYXIsCiAgICAgICAgIm1vbnRoIjogc291cmNlLm1vbnRoLAogICAgfQoKCmRlZiBzb3J0X2luZ3Jlc29zX3Jvd3Mocm93cywgcmVwb3J0X3NvcnQpOgogICAgZGF0ZV9vcmRlciA9IHJlcG9ydF9zb3J0WyJkYXRlX29yZGVyIl0KICAgIGdyb3VwX21vZGUgPSByZXBvcnRfc29ydFsiZ3JvdXBfbW9kZSJdCgogICAgcmV2ZXJzZV9kYXRlID0gZGF0ZV9vcmRlciA9PSAiZGVzYyIKCiAgICBlbnJpY2hlZF9yb3dzID0gW10KICAgIGZvciByb3cgaW4gcm93czoKICAgICAgICByb3dfbWV0YSA9IGdldF9pbmdyZXNvc19yb3dfbWV0YShyb3cpCiAgICAgICAgZW5yaWNoZWRfcm93cy5hcHBlbmQoKHJvd19tZXRhLCByb3cpKQoKICAgIGlmIGdyb3VwX21vZGUgPT0gInVuZSI6CiAgICAgICAgZW5yaWNoZWRfcm93cy5zb3J0KAogICAgICAgICAgICBrZXk9bGFtYmRhIGl0ZW06ICgKICAgICAgICAgICAgICAgIGl0ZW1bMF1bInVuZV9zb3J0X29yZGVyIl0sCiAgICAgICAgICAgICAgICBpdGVtWzBdWyJ1bmVfbmFtZSJdLmxvd2VyKCksCiAgICAgICAgICAgICAgICAtaXRlbVswXVsieWVhciJdIGlmIHJldmVyc2VfZGF0ZSBlbHNlIGl0ZW1bMF1bInllYXIiXSwKICAgICAgICAgICAgICAgIC1pdGVtWzBdWyJtb250aCJdIGlmIHJldmVyc2VfZGF0ZSBlbHNlIGl0ZW1bMF1bIm1vbnRoIl0sCiAgICAgICAgICAgICkKICAgICAgICApCiAgICBlbHNlOgogICAgICAgIGVucmljaGVkX3Jvd3Muc29ydCgKICAgICAgICAgICAga2V5PWxhbWJkYSBpdGVtOiAoCiAgICAgICAgICAgICAgICAtaXRlbVswXVsieWVhciJdIGlmIHJldmVyc2VfZGF0ZSBlbHNlIGl0ZW1bMF1bInllYXIiXSwKICAgICAgICAgICAgICAgIC1pdGVtWzBdWyJtb250aCJdIGlmIHJldmVyc2VfZGF0ZSBlbHNlIGl0ZW1bMF1bIm1vbnRoIl0sCiAgICAgICAgICAgICAgICBpdGVtWzBdWyJ1bmVfc29ydF9vcmRlciJdLAogICAgICAgICAgICAgICAgaXRlbVswXVsidW5lX25hbWUiXS5sb3dlcigpLAogICAgICAgICAgICApCiAgICAgICAgKQoKICAgIHNvcnRlZF9yb3dzID0gW3JvdyBmb3IgXywgcm93IGluIGVucmljaGVkX3Jvd3NdCgogICAgaWYgZ3JvdXBfbW9kZSAhPSAidW5lIjoKICAgICAgICByZXR1cm4gc29ydGVkX3Jvd3MKCiAgICBzZXBhcmF0ZWRfcm93cyA9IFtdCiAgICBwcmV2aW91c191bmVfa2V5ID0gTm9uZQoKICAgIGZvciByb3cgaW4gc29ydGVkX3Jvd3M6CiAgICAgICAgcm93X21ldGEgPSBnZXRfaW5ncmVzb3Nfcm93X21ldGEocm93KQogICAgICAgIGN1cnJlbnRfdW5lX2tleSA9ICgKICAgICAgICAgICAgcm93X21ldGFbInVuZV9zb3J0X29yZGVyIl0sCiAgICAgICAgICAgIHJvd19tZXRhWyJ1bmVfbmFtZSJdLmxvd2VyKCksCiAgICAgICAgKQoKICAgICAgICBpZiBwcmV2aW91c191bmVfa2V5IGlzIG5vdCBOb25lIGFuZCBjdXJyZW50X3VuZV9rZXkgIT0gcHJldmlvdXNfdW5lX2tleToKICAgICAgICAgICAgc2VwYXJhdGVkX3Jvd3MuYXBwZW5kKHsiaXNfc2VwYXJhdG9yIjogVHJ1ZX0pCgogICAgICAgIHNlcGFyYXRlZF9yb3dzLmFwcGVuZChyb3cpCiAgICAgICAgcHJldmlvdXNfdW5lX2tleSA9IGN1cnJlbnRfdW5lX2tleQoKICAgIHJldHVybiBzZXBhcmF0ZWRfcm93cwoKCmRlZiBfc2FmZV9pbnQodmFsdWUsIGRlZmF1bHQ9Tm9uZSk6CiAgICB0cnk6CiAgICAgICAgcmV0dXJuIGludCh2YWx1ZSkKICAgIGV4Y2VwdCAoVHlwZUVycm9yLCBWYWx1ZUVycm9yKToKICAgICAgICByZXR1cm4gZGVmYXVsdAoKCmRlZiBfYnVpbGRfcGVyaW9kX3JhbmdlKHN0YXJ0X3llYXIsIHN0YXJ0X21vbnRoLCBtb250aF9jb3VudCk6CiAgCiAgICBwZXJpb2RzID0gW10KICAgIHllYXIgPSBzdGFydF95ZWFyCiAgICBtb250aCA9IHN0YXJ0X21vbnRoCgogICAgZm9yIF8gaW4gcmFuZ2UobW9udGhfY291bnQpOgogICAgICAgIHBlcmlvZHMuYXBwZW5kKCh5ZWFyLCBtb250aCkpCiAgICAgICAgbW9udGggKz0gMQogICAgICAgIGlmIG1vbnRoID4gMTI6CiAgICAgICAgICAgIG1vbnRoID0gMQogICAgICAgICAgICB5ZWFyICs9IDEKCiAgICByZXR1cm4gcGVyaW9kcwoKCmRlZiBfcGVyaW9kX3JhbmdlX2VuZChzdGFydF95ZWFyLCBzdGFydF9tb250aCwgbW9udGhfY291bnQpOgogICAgIiIiTWVzIGZpbmFsIGluY2x1c2l2byBkZWwgcmFuZ28gKHN0YXJ0ICsgbW9udGhfY291bnQgLSAxKS4iIiIKICAgIHBlcmlvZHMgPSBfYnVpbGRfcGVyaW9kX3JhbmdlKHN0YXJ0X3llYXIsIHN0YXJ0X21vbnRoLCBtb250aF9jb3VudCkKICAgIGlmIG5vdCBwZXJpb2RzOgogICAgICAgIHJldHVybiBzdGFydF95ZWFyLCBzdGFydF9tb250aAogICAgcmV0dXJuIHBlcmlvZHNbLTFdCgoKZGVmIF9idWlsZF95dGRfcGVyaW9kX3JhbmdlKGVuZF95ZWFyLCBlbmRfbW9udGgpOgogICAgIiIiRW5lcm8gZGVsIGHDsW8gZGVsIG1lcyBmaW5hbCDihpIgbWVzIGZpbmFsIChpbmNsdXNpdmUpLiIiIgogICAgZW5kX21vbnRoID0gbWF4KDEsIG1pbigxMiwgaW50KGVuZF9tb250aCkpKQogICAgcmV0dXJuIFsoZW5kX3llYXIsIG0pIGZvciBtIGluIHJhbmdlKDEsIGVuZF9tb250aCArIDEpXQoKCmRlZiBfYnVpbGRfcGVyaW9kX3EocGVyaW9kcyk6CiAgICBxdWVyeSA9IFEoKQogICAgZm9yIHllYXIsIG1vbnRoIGluIHBlcmlvZHM6CiAgICAgICAgcXVlcnkgfD0gUSh5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKQogICAgcmV0dXJuIHF1ZXJ5ICAKCgpkZWYgX2dldF9hdmFpbGFibGVfcGVyaW9kcyhtb2RlPU5vbmUpOgogICAgYWN0aXZlX3BsYW4gPSBfZ2V0X2FjdGl2ZV9wZ2NfcGxhbigpCiAgICBwZXJpb2RzID0gW10KCiAgICBpZiBhY3RpdmVfcGxhbjoKICAgICAgICBwZXJpb2RzID0gbGlzdCgKICAgICAgICAgICAgTW9udGhseU1vZGVTY29yZWNhcmQub2JqZWN0cwogICAgICAgICAgICAuZmlsdGVyKHBsYW49YWN0aXZlX3BsYW4sIG1vZGU9bW9kZSBvciBERUZBVUxUX1BHQ19NT0RFKQogICAgICAgICAgICAub3JkZXJfYnkoIi15ZWFyIiwgIi1tb250aCIpCiAgICAgICAgICAgIC52YWx1ZXNfbGlzdCgieWVhciIsICJtb250aCIpCiAgICAgICAgICAgIC5kaXN0aW5jdCgpCiAgICAgICAgKQoKICAgICAgICBpZiBub3QgcGVyaW9kczoKICAgICAgICAgICAgcGVyaW9kcyA9IGxpc3QoCiAgICAgICAgICAgICAgICBNb250aGx5U2NvcmVjYXJkLm9iamVjdHMKICAgICAgICAgICAgICAgIC5maWx0ZXIocGxhbj1hY3RpdmVfcGxhbikKICAgICAgICAgICAgICAgIC5vcmRlcl9ieSgiLXllYXIiLCAiLW1vbnRoIikKICAgICAgICAgICAgICAgIC52YWx1ZXNfbGlzdCgieWVhciIsICJtb250aCIpCiAgICAgICAgICAgICAgICAuZGlzdGluY3QoKQogICAgICAgICAgICApCgogICAgIyBBc2VndXJhciBxdWUgZWwgYcOxbyBlbiBjdXJzbyAoZW5l4oCTZGljKSBzaWVtcHJlIGVzdMOpIGVuIGVsIHNlbGVjdG9yICJEZXNkZSIuCiAgICBub3cgPSBkYXRldGltZS5ub3coKQogICAgc2VlbiA9IHNldChwZXJpb2RzKQogICAgZm9yIG1vbnRoIGluIHJhbmdlKDEsIDEzKToKICAgICAgICBrZXkgPSAobm93LnllYXIsIG1vbnRoKQogICAgICAgIGlmIGtleSBub3QgaW4gc2VlbjoKICAgICAgICAgICAgcGVyaW9kcy5hcHBlbmQoa2V5KQogICAgICAgICAgICBzZWVuLmFkZChrZXkpCgogICAgcGVyaW9kcy5zb3J0KGtleT1sYW1iZGEgeW06ICh5bVswXSwgeW1bMV0pLCByZXZlcnNlPVRydWUpCgogICAgcmV0dXJuIFsKICAgICAgICB7CiAgICAgICAgICAgICJ5ZWFyIjogeWVhciwKICAgICAgICAgICAgIm1vbnRoIjogbW9udGgsCiAgICAgICAgICAgICJrZXkiOiBmInt5ZWFyfS17bW9udGg6MDJkfSIsCiAgICAgICAgfQogICAgICAgIGZvciB5ZWFyLCBtb250aCBpbiBwZXJpb2RzCiAgICBdCgoKTU9OVEhfQ09VTlRfT1BUSU9OUyA9IGxpc3QocmFuZ2UoMSwgMTMpKQoKCmRlZiBzaGlmdF9tb250aCh5ZWFyLCBtb250aCwgZGVsdGEpOgogICAgdG90YWwgPSB5ZWFyICogMTIgKyAobW9udGggLSAxKSArIGRlbHRhCiAgICBuZXdfeWVhciA9IHRvdGFsIC8vIDEyCiAgICBuZXdfbW9udGggPSB0b3RhbCAlIDEyICsgMQogICAgcmV0dXJuIG5ld195ZWFyLCBuZXdfbW9udGgKICAKCmRlZiBfZ2V0X3JlcG9ydF9maWx0ZXIocmVxdWVzdCwgbW9kZT1ERUZBVUxUX1BHQ19NT0RFKToKICAgIGR5bmFtaWNfZGVmYXVsdF9tb250aF9jb3VudCA9IGdldF9kZWZhdWx0X21vbnRoX2NvdW50KCkKICAgIGRlZmF1bHRfc3RhcnRfeWVhciwgZGVmYXVsdF9zdGFydF9tb250aCA9IGdldF9kZWZhdWx0X3JlcG9ydF9zdGFydCgpCgogICAgZ2V0X3N0YXJ0X3llYXIgPSBfc2FmZV9pbnQocmVxdWVzdC5HRVQuZ2V0KCJzdGFydF95ZWFyIikpCiAgICBnZXRfc3RhcnRfbW9udGggPSBfc2FmZV9pbnQocmVxdWVzdC5HRVQuZ2V0KCJzdGFydF9tb250aCIpKQogICAgZ2V0X21vbnRoX2NvdW50ID0gX3NhZmVfaW50KHJlcXVlc3QuR0VULmdldCgibW9udGhfY291bnQiKSkKCiAgICBzZXNzaW9uX3N0YXJ0X3llYXIgPSBfc2FmZV9pbnQocmVxdWVzdC5zZXNzaW9uLmdldCgicGdjX3JlcG9ydF9zdGFydF95ZWFyIikpCiAgICBzZXNzaW9uX3N0YXJ0X21vbnRoID0gX3NhZmVfaW50KHJlcXVlc3Quc2Vzc2lvbi5nZXQoInBnY19yZXBvcnRfc3RhcnRfbW9udGgiKSkKICAgIHNlc3Npb25fbW9udGhfY291bnQgPSBfc2FmZV9pbnQocmVxdWVzdC5zZXNzaW9uLmdldCgicGdjX3JlcG9ydF9tb250aF9jb3VudCIpKQoKICAgICMgUHJlZmVyaXIgR0VUOyBzaSBubywgZGVmYXVsdHMgWVREIChlbmUg4oaSIG1lcyBhbnRlcmlvcikuIFNlc3Npb24gc29sbyBzaSB5YSBoYXkgR0VUIHBhcmNpYWwuCiAgICBoYXNfZ2V0X2ZpbHRlciA9IGFueSgKICAgICAgICByZXF1ZXN0LkdFVC5nZXQoaykgbm90IGluIChOb25lLCAiIikKICAgICAgICBmb3IgayBpbiAoInN0YXJ0X3llYXIiLCAic3RhcnRfbW9udGgiLCAibW9udGhfY291bnQiKQogICAgKQoKICAgIGlmIGdldF9tb250aF9jb3VudDoKICAgICAgICBtb250aF9jb3VudCA9IGdldF9tb250aF9jb3VudAogICAgZWxpZiBoYXNfZ2V0X2ZpbHRlciBhbmQgc2Vzc2lvbl9tb250aF9jb3VudDoKICAgICAgICBtb250aF9jb3VudCA9IHNlc3Npb25fbW9udGhfY291bnQKICAgIGVsc2U6CiAgICAgICAgbW9udGhfY291bnQgPSBkeW5hbWljX2RlZmF1bHRfbW9udGhfY291bnQKCiAgICBpZiBtb250aF9jb3VudCA8IDE6CiAgICAgICAgbW9udGhfY291bnQgPSBkeW5hbWljX2RlZmF1bHRfbW9udGhfY291bnQKICAgIGlmIG1vbnRoX2NvdW50ID4gTUFYX01PTlRIX0NPVU5UOgogICAgICAgIG1vbnRoX2NvdW50ID0gTUFYX01PTlRIX0NPVU5UCgogICAgaWYgZ2V0X3N0YXJ0X3llYXIgYW5kIGdldF9zdGFydF9tb250aDoKICAgICAgICBzdGFydF95ZWFyLCBzdGFydF9tb250aCA9IGdldF9zdGFydF95ZWFyLCBnZXRfc3RhcnRfbW9udGgKICAgIGVsaWYgaGFzX2dldF9maWx0ZXIgYW5kIHNlc3Npb25fc3RhcnRfeWVhciBhbmQgc2Vzc2lvbl9zdGFydF9tb250aDoKICAgICAgICBzdGFydF95ZWFyLCBzdGFydF9tb250aCA9IHNlc3Npb25fc3RhcnRfeWVhciwgc2Vzc2lvbl9zdGFydF9tb250aAogICAgZWxzZToKICAgICAgICBzdGFydF95ZWFyLCBzdGFydF9tb250aCA9IGRlZmF1bHRfc3RhcnRfeWVhciwgZGVmYXVsdF9zdGFydF9tb250aAoKICAgIGlmIHN0YXJ0X21vbnRoIDwgMSBvciBzdGFydF9tb250aCA+IDEyOgogICAgICAgIHN0YXJ0X3llYXIsIHN0YXJ0X21vbnRoID0gZGVmYXVsdF9zdGFydF95ZWFyLCBkZWZhdWx0X3N0YXJ0X21vbnRoCgogICAgcmVxdWVzdC5zZXNzaW9uWyJwZ2NfcmVwb3J0X3N0YXJ0X3llYXIiXSA9IHN0YXJ0X3llYXIKICAgIHJlcXVlc3Quc2Vzc2lvblsicGdjX3JlcG9ydF9zdGFydF9tb250aCJdID0gc3RhcnRfbW9udGgKICAgIHJlcXVlc3Quc2Vzc2lvblsicGdjX3JlcG9ydF9tb250aF9jb3VudCJdID0gbW9udGhfY291bnQKCiAgICByZXR1cm4gewogICAgICAgICJzdGFydF95ZWFyIjogc3RhcnRfeWVhciwKICAgICAgICAic3RhcnRfbW9udGgiOiBzdGFydF9tb250aCwKICAgICAgICAibW9udGhfY291bnQiOiBtb250aF9jb3VudCwKICAgIH0KCgpAbG9naW5fcmVxdWlyZWQKZGVmIHBnY19ob21lKHJlcXVlc3QpOgogICAgIiIiQWNjZXNvIGRpcmVjdG8gYWwgdGFibGVybyBQR0MgKHNpbiBwYW50YWxsYSBpbnRlcm1lZGlhKS4iIiIKICAgIHJldHVybiByZWRpcmVjdCgicGdjOmRhc2hib2FyZCIpCgoKZGVmIHNwbGFzaChyZXF1ZXN0KToKICAgICIiIgogICAgUGFudGFsbGEgaW5pY2lhbDogbXVlc3RyYSBzcGxhc2ggeSwgYWwgcHJpbWVyIGNsaWNrL3RlY2xhLAogICAgcmVkaXJpZ2UgYWwgdGFibGVybyBwcmluY2lwYWwuCiAgICAiIiIKICAgICMgU2kgeWEgZXN0w6EgYXV0ZW50aWNhZG8sIGlndWFsIG1vc3RyYW1vcyBzcGxhc2ggdW5hIHZlei4KICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgInNwbGFzaC5odG1sIikKCgpAbG9naW5fcmVxdWlyZWQKZGVmIHBnY19kYXNoYm9hcmRfZXhwb3J0X21kKHJlcXVlc3QpOgogICAgcmVwb3J0X2ZpbHRlciA9IF9nZXRfcmVwb3J0X2ZpbHRlcihyZXF1ZXN0KQogICAgcmVwb3J0X3NvcnQgPSBnZXRfcmVwb3J0X3NvcnQocmVxdWVzdCkKICAgIHNlbGVjdGVkX21vZGUgPSBfZ2V0X3BnY19tb2RlKHJlcXVlc3QpCgogICAgcGVyaW9kcyA9IF9idWlsZF9wZXJpb2RfcmFuZ2UoCiAgICAgICAgcmVwb3J0X2ZpbHRlclsic3RhcnRfeWVhciJdLAogICAgICAgIHJlcG9ydF9maWx0ZXJbInN0YXJ0X21vbnRoIl0sCiAgICAgICAgcmVwb3J0X2ZpbHRlclsibW9udGhfY291bnQiXSwKICAgICkKCiAgICByb3dzID0gX2dldF9kYXNoYm9hcmRfcm93cyhwZXJpb2RzPXBlcmlvZHMsIG1vZGU9c2VsZWN0ZWRfbW9kZSkKICAgIHJvd3MgPSBzb3J0X3JlcG9ydF9yb3dzKHJvd3MsIHJlcG9ydF9zb3J0KQoKICAgIGNvbnRlbnQgPSBfYnVpbGRfZGFzaGJvYXJkX21hcmtkb3duKAogICAgICAgIHJvd3MsCiAgICAgICAgcmVwb3J0X2ZpbHRlciwKICAgICAgICBzZWxlY3RlZF9tb2RlPXNlbGVjdGVkX21vZGUsCiAgICApCgogICAgZ2VuZXJhdGVkX3N1ZmZpeCA9IGRhdGV0aW1lLm5vdygpLnN0cmZ0aW1lKCIlWSVtJWQtJUglTSIpCiAgICBzdGFydF95ZWFyID0gcmVwb3J0X2ZpbHRlclsic3RhcnRfeWVhciJdCiAgICBzdGFydF9tb250aCA9IHJlcG9ydF9maWx0ZXJbInN0YXJ0X21vbnRoIl0KICAgIG1vbnRoX2NvdW50ID0gcmVwb3J0X2ZpbHRlclsibW9udGhfY291bnQiXQoKICAgIGZpbGVuYW1lID0gKAogICAgICAgIGYicGdjLXRhYmxlcm8tcHJpbmNpcGFsLSIKICAgICAgICBmIntzZWxlY3RlZF9tb2RlfS0iCiAgICAgICAgZiJmeXtzdGFydF95ZWFyfS1te3N0YXJ0X21vbnRoOjAyZH0tbnttb250aF9jb3VudH0tIgogICAgICAgIGYie2dlbmVyYXRlZF9zdWZmaXh9Lm1kIgogICAgKQoKICAgIHJlc3BvbnNlID0gSHR0cFJlc3BvbnNlKAogICAgICAgIHNtYXJ0X3N0cihjb250ZW50KSwKICAgICAgICBjb250ZW50X3R5cGU9InRleHQvcGxhaW47IGNoYXJzZXQ9dXRmLTgiLAogICAgKQogICAgcmVzcG9uc2VbIkNvbnRlbnQtRGlzcG9zaXRpb24iXSA9IGYnYXR0YWNobWVudDsgZmlsZW5hbWU9IntmaWxlbmFtZX0iJwogICAgcmV0dXJuIHJlc3BvbnNlCgoKQGxvZ2luX3JlcXVpcmVkCmRlZiBwZ2NfZGFzaGJvYXJkKHJlcXVlc3QpOgogICAgc2VsZWN0ZWRfbW9kZSA9IF9nZXRfcGdjX21vZGUocmVxdWVzdCkKICAgIHJlcG9ydF9maWx0ZXIgPSBfZ2V0X3JlcG9ydF9maWx0ZXIocmVxdWVzdCwgbW9kZT1zZWxlY3RlZF9tb2RlKQogICAgcmVwb3J0X3NvcnQgPSBnZXRfcmVwb3J0X3NvcnQocmVxdWVzdCkKCiAgICBwZXJpb2RzID0gX2J1aWxkX3BlcmlvZF9yYW5nZSgKICAgICAgICByZXBvcnRfZmlsdGVyWyJzdGFydF95ZWFyIl0sCiAgICAgICAgcmVwb3J0X2ZpbHRlclsic3RhcnRfbW9udGgiXSwKICAgICAgICByZXBvcnRfZmlsdGVyWyJtb250aF9jb3VudCJdLAogICAgKQoKICAgIHJvd3MgPSBfZ2V0X2Rhc2hib2FyZF9yb3dzKHBlcmlvZHM9cGVyaW9kcywgbW9kZT1zZWxlY3RlZF9tb2RlKQogICAgcm93cyA9IHNvcnRfcmVwb3J0X3Jvd3Mocm93cywgcmVwb3J0X3NvcnQpCgogICAgY2hhcnRfcGF5bG9hZCA9IF9idWlsZF9kYXNoYm9hcmRfY2hhcnRfcGF5bG9hZCgKICAgICAgICBwZXJpb2RzPXBlcmlvZHMsCiAgICAgICAgbW9kZT1zZWxlY3RlZF9tb2RlLAogICAgKQoKICAgICMgU2VyaWUgYXBhcnRlIHBhcmEgZXhwb3J0YWNpw7NuIFNWRyA0LWNoYXJ0czogc2llbXByZSBlbmVybyDihpIgbWVzIGZpbmFsIGRlbCByYW5nby4KICAgIGVuZF95ZWFyLCBlbmRfbW9udGggPSBfcGVyaW9kX3JhbmdlX2VuZCgKICAgICAgICByZXBvcnRfZmlsdGVyWyJzdGFydF95ZWFyIl0sCiAgICAgICAgcmVwb3J0X2ZpbHRlclsic3RhcnRfbW9udGgiXSwKICAgICAgICByZXBvcnRfZmlsdGVyWyJtb250aF9jb3VudCJdLAogICAgKQogICAgeXRkX3BlcmlvZHMgPSBfYnVpbGRfeXRkX3BlcmlvZF9yYW5nZShlbmRfeWVhciwgZW5kX21vbnRoKQogICAgeXRkX3BheWxvYWQgPSBfYnVpbGRfZGFzaGJvYXJkX2NoYXJ0X3BheWxvYWQoCiAgICAgICAgcGVyaW9kcz15dGRfcGVyaW9kcywKICAgICAgICBtb2RlPXNlbGVjdGVkX21vZGUsCiAgICApCiAgICBpbmdyZXNvc195dGQgPSAoeXRkX3BheWxvYWQuZ2V0KCJtZXRyaWNzIikgb3Ige30pLmdldCgKICAgICAgICBNZXRyaWNEZWZpbml0aW9uLkNPREVfSU5HUkVTT1MsIHt9CiAgICApCiAgICBjaGFydF9wYXlsb2FkWyJleHBvcnRfaW5ncmVzb3MiXSA9IHsKICAgICAgICAiZW5kX3llYXIiOiBlbmRfeWVhciwKICAgICAgICAiZW5kX21vbnRoIjogZW5kX21vbnRoLAogICAgICAgICJwZXJpb2RzIjogaW5ncmVzb3NfeXRkLmdldCgicGVyaW9kcyIpIG9yIFtdLAogICAgICAgICJ5X2F4aXMiOiBpbmdyZXNvc195dGQuZ2V0KCJ5X2F4aXMiKSBvciAiQ2lmcmFzIGVuIG1pbGVzIGRlIFVTJCIsCiAgICB9CgogICAgY29udGV4dCA9IHsKICAgICAgICAicm93cyI6IHJvd3MsCiAgICAgICAgInJlcG9ydF9maWx0ZXIiOiByZXBvcnRfZmlsdGVyLAogICAgICAgICJyZXBvcnRfc29ydCI6IHJlcG9ydF9zb3J0LAogICAgICAgICJzZWxlY3RlZF9tb2RlIjogc2VsZWN0ZWRfbW9kZSwKICAgICAgICAic2VsZWN0ZWRfbW9kZV9sYWJlbCI6IFBHQ19NT0RFX0xBQkVMUy5nZXQoc2VsZWN0ZWRfbW9kZSwgc2VsZWN0ZWRfbW9kZSksCiAgICAgICAgIm1vZGVfb3B0aW9ucyI6IFBHQ19NT0RFX09QVElPTlMsCiAgICAgICAgIm1vZGVfY2hvaWNlcyI6IFsobSwgUEdDX01PREVfTEFCRUxTW21dKSBmb3IgbSBpbiBQR0NfTU9ERV9PUFRJT05TXSwKICAgICAgICAiYXZhaWxhYmxlX3BlcmlvZHMiOiBfZ2V0X2F2YWlsYWJsZV9wZXJpb2RzKG1vZGU9c2VsZWN0ZWRfbW9kZSksCiAgICAgICAgIm1vbnRoX2NvdW50X29wdGlvbnMiOiBNT05USF9DT1VOVF9PUFRJT05TLAogICAgICAgICJjaGFydF9wYXlsb2FkX2pzb24iOiBqc29uLmR1bXBzKGNoYXJ0X3BheWxvYWQsIGVuc3VyZV9hc2NpaT1GYWxzZSksCiAgICAgICAgImNoYXJ0X3Jvd3MiOiBbCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICJ1bmUiOiByb3dbInVuZSJdLm5hbWVfZXMsCiAgICAgICAgICAgICAgICAicGVyaW9kbyI6IGYie3Jvd1sneWVhciddfS17cm93Wydtb250aCddOjAyZH0iLCAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAicF9pbmdyZXNvcyI6IHJvd1sicF9pbmdyZXNvcyJdLAogICAgICAgICAgICAgICAgInBfY2xpZW50ZXMiOiByb3dbInBfY2xpZW50ZXMiXSwKICAgICAgICAgICAgICAgICJwX3ZlbnRhX2NydXphZGEiOiByb3dbInBfdmVudGFfY3J1emFkYSJdLAogICAgICAgICAgICAgICAgInBfcmVzcHVlc3RhX3JlcXMiOiByb3dbInBfcmVzcHVlc3RhX3JlcXMiXSwKICAgICAgICAgICAgICAgICJ0b3RhbCI6IHJvd1sidG90YWxfcG9pbnRzIl0sCiAgICAgICAgICAgIH0KICAgICAgICAgICAgZm9yIHJvdyBpbiByb3dzCiAgICAgICAgICAgIGlmIG5vdCByb3cuZ2V0KCJpc19zZXBhcmF0b3IiKQogICAgICAgIF0sCiAgICB9CiAgICByZXR1cm4gcmVuZGVyKHJlcXVlc3QsICJwZ2MvZGFzaGJvYXJkLmh0bWwiLCBjb250ZXh0KQogIAoKZGVmIF9kZWNpbWFsX3RvX251bWJlcih2YWx1ZSk6CiAgICBpZiB2YWx1ZSBpcyBOb25lOgogICAgICAgIHJldHVybiBOb25lCiAgICB0cnk6CiAgICAgICAgcmV0dXJuIGZsb2F0KHZhbHVlKQogICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICByZXR1cm4gTm9uZQoKCmRlZiBfYnVpbGRfZGFzaGJvYXJkX2NoYXJ0X3BheWxvYWQocGVyaW9kcz1Ob25lLCBtb2RlPURFRkFVTFRfUEdDX01PREUpOgogICAgYWN0aXZlX3BsYW4gPSBnZXRfYWN0aXZlX3BnY19wbGFuKCkKICAgIGlmIG5vdCBhY3RpdmVfcGxhbjoKICAgICAgICByZXR1cm4geyJwZXJpb2RzIjogW10sICJ1bmVzIjogW10sICJtZXRyaWNzIjoge319CgogICAgbWV0cmljX2NvZGVzID0gWwogICAgICAgIE1ldHJpY0RlZmluaXRpb24uQ09ERV9JTkdSRVNPUywKICAgICAgICBNZXRyaWNEZWZpbml0aW9uLkNPREVfQ0xJRU5URVNfTlVFVk9TLAogICAgICAgIE1ldHJpY0RlZmluaXRpb24uQ09ERV9WRU5UQV9DUlVaQURBLAogICAgXQoKICAgIHRhcmdldHMgPSAoCiAgICAgICAgTW9udGhseVRhcmdldC5vYmplY3RzCiAgICAgICAgLnNlbGVjdF9yZWxhdGVkKCJ1bmUiLCAicGxhbiIsICJtZXRyaWMiKQogICAgICAgIC5maWx0ZXIocGxhbj1hY3RpdmVfcGxhbiwgbWV0cmljX19jb2RlX19pbj1tZXRyaWNfY29kZXMpCiAgICApCgogICAgcmVzdWx0cyA9ICgKICAgICAgICBNb250aGx5TWV0cmljUmVzdWx0Lm9iamVjdHMKICAgICAgICAuc2VsZWN0X3JlbGF0ZWQoInVuZSIsICJwbGFuIiwgIm1ldHJpYyIpCiAgICAgICAgLmZpbHRlcihwbGFuPWFjdGl2ZV9wbGFuLCBtZXRyaWNfX2NvZGVfX2luPW1ldHJpY19jb2RlcykKICAgICkKCiAgICBpZiBwZXJpb2RzOgogICAgICAgIHBlcmlvZF9xID0gX2J1aWxkX3BlcmlvZF9xKHBlcmlvZHMpCiAgICAgICAgdGFyZ2V0cyA9IHRhcmdldHMuZmlsdGVyKHBlcmlvZF9xKQogICAgICAgIHJlc3VsdHMgPSByZXN1bHRzLmZpbHRlcihwZXJpb2RfcSkKCiAgICB0YXJnZXRfbWFwID0ge30KICAgIGZvciB0IGluIHRhcmdldHM6CiAgICAgICAga2V5ID0gKHQubWV0cmljLmNvZGUsIHQueWVhciwgdC5tb250aCwgdC51bmUuY29kZSkKICAgICAgICB0YXJnZXRfbWFwW2tleV0gPSBfZGVjaW1hbF90b19udW1iZXIodC50YXJnZXRfdmFsdWUpCgogICAgcmVzdWx0X21hcCA9IHt9CiAgICBmb3IgciBpbiByZXN1bHRzOgogICAgICAgIGtleSA9IChyLm1ldHJpYy5jb2RlLCByLnllYXIsIHIubW9udGgsIHIudW5lLmNvZGUpCiAgICAgICAgcmVzdWx0X21hcFtrZXldID0gX2RlY2ltYWxfdG9fbnVtYmVyKHIubWVhc3VyZWRfdmFsdWUpCgogICAgdW5lX21hcCA9IHt9CiAgICBmb3IgdCBpbiB0YXJnZXRzOgogICAgICAgIHVuZV9tYXBbdC51bmUuY29kZV0gPSB7CiAgICAgICAgICAgICJjb2RlIjogdC51bmUuY29kZSwKICAgICAgICAgICAgIm5hbWVfZXMiOiB0LnVuZS5uYW1lX2VzLAogICAgICAgICAgICAic29ydF9vcmRlciI6IHQudW5lLnNvcnRfb3JkZXIsCiAgICAgICAgfQogICAgZm9yIHIgaW4gcmVzdWx0czoKICAgICAgICB1bmVfbWFwW3IudW5lLmNvZGVdID0gewogICAgICAgICAgICAiY29kZSI6IHIudW5lLmNvZGUsCiAgICAgICAgICAgICJuYW1lX2VzIjogci51bmUubmFtZV9lcywKICAgICAgICAgICAgInNvcnRfb3JkZXIiOiByLnVuZS5zb3J0X29yZGVyLAogICAgICAgIH0KCiAgICB1bmVzID0gc29ydGVkKAogICAgICAgIHVuZV9tYXAudmFsdWVzKCksCiAgICAgICAga2V5PWxhbWJkYSB4OiAoeFsic29ydF9vcmRlciJdIGlmIHhbInNvcnRfb3JkZXIiXSBpcyBub3QgTm9uZSBlbHNlIDk5OTk5OSwgeFsibmFtZV9lcyJdKQogICAgKQoKICAgIHBlcmlvZHNfbGlzdCA9IFtdCiAgICBmb3IgeWVhciwgbW9udGggaW4gKHBlcmlvZHMgb3IgW10pOgogICAgICAgIHBlcmlvZHNfbGlzdC5hcHBlbmQoewogICAgICAgICAgICAieWVhciI6IHllYXIsCiAgICAgICAgICAgICJtb250aCI6IG1vbnRoLAogICAgICAgICAgICAia2V5IjogZiJ7eWVhcn0te21vbnRoOjAyZH0iLAogICAgICAgICAgICAibGFiZWwiOiBmInt5ZWFyfS17bW9udGg6MDJkfSIsCiAgICAgICAgfSkKCiAgICBzZXJpZXMgPSB7fQogICAgZm9yIG1ldHJpY19jb2RlIGluIG1ldHJpY19jb2RlczoKICAgICAgICBtZXRyaWNfcGVyaW9kcyA9IFtdCiAgICAgICAgZm9yIHllYXIsIG1vbnRoIGluIChwZXJpb2RzIG9yIFtdKToKICAgICAgICAgICAgYnlfdW5lID0ge30KICAgICAgICAgICAgZm9yIHVuZSBpbiB1bmVzOgogICAgICAgICAgICAgICAgdW5lX2NvZGUgPSB1bmVbImNvZGUiXQogICAgICAgICAgICAgICAgYnlfdW5lW3VuZV9jb2RlXSA9IHsKICAgICAgICAgICAgICAgICAgICAidGFyZ2V0IjogdGFyZ2V0X21hcC5nZXQoKG1ldHJpY19jb2RlLCB5ZWFyLCBtb250aCwgdW5lX2NvZGUpLCAwKSwKICAgICAgICAgICAgICAgICAgICAicmVhbCI6IHJlc3VsdF9tYXAuZ2V0KChtZXRyaWNfY29kZSwgeWVhciwgbW9udGgsIHVuZV9jb2RlKSwgMCksCiAgICAgICAgICAgICAgICB9CgogICAgICAgICAgICBtZXRyaWNfcGVyaW9kcy5hcHBlbmQoewogICAgICAgICAgICAgICAgInllYXIiOiB5ZWFyLAogICAgICAgICAgICAgICAgIm1vbnRoIjogbW9udGgsCiAgICAgICAgICAgICAgICAia2V5IjogZiJ7eWVhcn0te21vbnRoOjAyZH0iLAogICAgICAgICAgICAgICAgImxhYmVsIjogZiJ7eWVhcn0te21vbnRoOjAyZH0iLAogICAgICAgICAgICAgICAgImJ5X3VuZSI6IGJ5X3VuZSwKICAgICAgICAgICAgfSkKCiAgICAgICAgc2VyaWVzW21ldHJpY19jb2RlXSA9IG1ldHJpY19wZXJpb2RzCiAgICByZXR1cm4gewogICAgICAgICJwZXJpb2RzIjogcGVyaW9kc19saXN0LAogICAgICAgICJ1bmVzIjogWwogICAgICAgICAgICB7ImNvZGUiOiB1WyJjb2RlIl0sICJuYW1lX2VzIjogdVsibmFtZV9lcyJdfQogICAgICAgICAgICBmb3IgdSBpbiB1bmVzCiAgICAgICAgXSwKICAgICAgICAibWV0cmljcyI6IHsKICAgICAgICAgICAgTWV0cmljRGVmaW5pdGlvbi5DT0RFX0lOR1JFU09TOiB7CiAgICAgICAgICAgICAgICAidGl0bGUiOiAiSW5ncmVzb3MgYnJ1dG9zIiwKICAgICAgICAgICAgICAgICJzdWJ0aXRsZSI6ICJSZWFsIHZzIG1ldGEgcG9yIHBlcsOtb2RvIiwKICAgICAgICAgICAgICAgICJ5X2F4aXMiOiAiQ2lmcmFzIGVuIG1pbGVzIGRlIFVTJCIsCiAgICAgICAgICAgICAgICAibWV0cmljX2NvZGUiOiBNZXRyaWNEZWZpbml0aW9uLkNPREVfSU5HUkVTT1MsCiAgICAgICAgICAgICAgICAicGVyaW9kcyI6IHNlcmllc1tNZXRyaWNEZWZpbml0aW9uLkNPREVfSU5HUkVTT1NdLAogICAgICAgICAgICB9LAogICAgICAgICAgICBNZXRyaWNEZWZpbml0aW9uLkNPREVfQ0xJRU5URVNfTlVFVk9TOiB7CiAgICAgICAgICAgICAgICAidGl0bGUiOiAiQ2xpZW50ZXMgbnVldm9zIiwKICAgICAgICAgICAgICAgICJzdWJ0aXRsZSI6ICJSZWFsIHZzIG1ldGEgcG9yIHBlcsOtb2RvIiwKICAgICAgICAgICAgICAgICJ5X2F4aXMiOiAiQ2FudGlkYWQgZGUgY2xpZW50ZXMiLAogICAgICAgICAgICAgICAgIm1ldHJpY19jb2RlIjogTWV0cmljRGVmaW5pdGlvbi5DT0RFX0NMSUVOVEVTX05VRVZPUywKICAgICAgICAgICAgICAgICJwZXJpb2RzIjogc2VyaWVzW01ldHJpY0RlZmluaXRpb24uQ09ERV9DTElFTlRFU19OVUVWT1NdLAogICAgICAgICAgICB9LAogICAgICAgICAgICBNZXRyaWNEZWZpbml0aW9uLkNPREVfVkVOVEFfQ1JVWkFEQTogewogICAgICAgICAgICAgICAgInRpdGxlIjogIlZlbnRhIGNydXphZGEiLAogICAgICAgICAgICAgICAgInN1YnRpdGxlIjogIlJlYWwgdnMgbWV0YSBwb3IgcGVyw61vZG8iLAogICAgICAgICAgICAgICAgInlfYXhpcyI6ICJDYW50aWRhZCIsCiAgICAgICAgICAgICAgICAibWV0cmljX2NvZGUiOiBNZXRyaWNEZWZpbml0aW9uLkNPREVfVkVOVEFfQ1JVWkFEQSwKICAgICAgICAgICAgICAgICJwZXJpb2RzIjogc2VyaWVzW01ldHJpY0RlZmluaXRpb24uQ09ERV9WRU5UQV9DUlVaQURBXSwKICAgICAgICAgICAgfSwKICAgICAgICB9LAogICAgfQoKCmRlZiBfYnVpbGRfZGFzaGJvYXJkX21hcmtkb3duKHJvd3MsIHJlcG9ydF9maWx0ZXIsIHNlbGVjdGVkX21vZGU9Im1vZG8xIik6CiAgICBnZW5lcmF0ZWRfYXQgPSBkYXRldGltZS5ub3coKS5zdHJmdGltZSgiJVktJW0tJWQgJUg6JU0iKQogICAgc3RhcnRfeWVhciA9IHJlcG9ydF9maWx0ZXJbInN0YXJ0X3llYXIiXQogICAgc3RhcnRfbW9udGggPSByZXBvcnRfZmlsdGVyWyJzdGFydF9tb250aCJdCiAgICBtb250aF9jb3VudCA9IHJlcG9ydF9maWx0ZXJbIm1vbnRoX2NvdW50Il0KCiAgICBwZXJpb2RzID0gX2J1aWxkX3BlcmlvZF9yYW5nZShzdGFydF95ZWFyLCBzdGFydF9tb250aCwgbW9udGhfY291bnQpCiAgICBlbmRfeWVhciwgZW5kX21vbnRoID0gcGVyaW9kc1stMV0KCiAgICBsaW5lcyA9IFsKICAgICAgICAiUEdDIC0gVGFibGVybyBwcmluY2lwYWwgZGUgcHVudG9zIHBvciBVTkUgeSBtZXMiLAogICAgICAgICIiLAogICAgICAgIGYiR2VuZXJhZG86IHtnZW5lcmF0ZWRfYXR9IiwKICAgICAgICAiIiwKICAgICAgICAiRmlsdHJvcyIsCiAgICAgICAgZiItIE1vZGFsaWRhZDoge1BHQ19NT0RFX0xBQkVMUy5nZXQoc2VsZWN0ZWRfbW9kZSwgc2VsZWN0ZWRfbW9kZSl9IiwKICAgICAgICBmIi0gRGVzZGU6IHtzdGFydF95ZWFyfS17c3RhcnRfbW9udGg6MDJkfSIsCiAgICAgICAgZiItIEhhc3RhOiB7ZW5kX3llYXJ9LXtlbmRfbW9udGg6MDJkfSIsCiAgICAgICAgZiItIE1lc2VzIGluY2x1aWRvczoge21vbnRoX2NvdW50fSIsCiAgICAgICAgIiIsCiAgICAgICAgIkRlc2NyaXBjacOzbiIsCiAgICAgICAgIlJlc3VtZW4gbWVuc3VhbCBkZSBwdW50b3MgcG9yIFVORSB5IHBlcmlvZG8uIiwKICAgICAgICAiIiwKICAgICAgICAiRGF0b3MiLAogICAgICAgICIiLAogICAgICAgICJ8IFVORSB8IFBlcmlvZG8gfCBQdW50b3MgaW5ncmVzb3MgfCBQdW50b3MgY2xpZW50ZXMgbnVldm9zIHwgUHVudG9zIHZlbnRhIGNydXphZGEgfCBQdW50b3MgcmVzcHVlc3RhIHJlcXMgfCBUb3RhbCB8IENsYXNpZmljYSB8IiwKICAgICAgICAifCAtLS0gfCAtLS0gfCAtLS0gfCAtLS0gfCAtLS0gfCAtLS0gfCAtLS0gfCAtLS0gfCIsCiAgICBdCgogICAgaWYgbm90IHJvd3M6CiAgICAgICAgbGluZXMuYXBwZW5kKCJ8IFNpbiBkYXRvcyB8IC0gfCAtIHwgLSB8IC0gfCAtIHwgLSB8IC0gfCIpCiAgICBlbHNlOgogICAgICAgIGZvciByb3cgaW4gcm93czoKICAgICAgICAgICAgaWYgcm93LmdldCgiaXNfc2VwYXJhdG9yIik6CiAgICAgICAgICAgICAgICBjb250aW51ZQoKICAgICAgICAgICAgY2xhc2lmaWNhID0gIlPDrSIgaWYgcm93WyJpc19tb250aF9xdWFsaWZpZWQiXSBlbHNlICJObyIKICAgICAgICAgICAgcGVyaW9kbyA9IGYie3Jvd1sneWVhciddfS17cm93Wydtb250aCddOjAyZH0iCgogICAgICAgICAgICBsaW5lcy5hcHBlbmQoCiAgICAgICAgICAgICAgICBmInwge3Jvd1sndW5lJ10ubmFtZV9lc30gfCB7cGVyaW9kb30gfCAiCiAgICAgICAgICAgICAgICBmIntyb3dbJ3BfaW5ncmVzb3MnXX0gfCB7cm93WydwX2NsaWVudGVzJ119IHwgIgogICAgICAgICAgICAgICAgZiJ7cm93WydwX3ZlbnRhX2NydXphZGEnXX0gfCB7cm93WydwX3Jlc3B1ZXN0YV9yZXFzJ119IHwgIgogICAgICAgICAgICAgICAgZiJ7cm93Wyd0b3RhbF9wb2ludHMnXX0gfCB7Y2xhc2lmaWNhfSB8IgogICAgICAgICAgICApCgogICAgbGluZXMuZXh0ZW5kKFsKICAgICAgICAiIiwKICAgICAgICAiTm90YSIsCiAgICAgICAgIkVzdGUgcmVwb3J0ZSBtdWVzdHJhIGVsIHB1bnRhamUgdG90YWwgeSBzdXMgY29tcG9uZW50ZXMgcG9yIFVORSB5IHBlcmlvZG8uIiwKICAgICAgICAiIiwKICAgIF0pCgogICAgcmV0dXJuICJcbiIuam9pbihsaW5lcykKCgpAbG9naW5fcmVxdWlyZWQKZGVmIGNsaWVudGVzX251ZXZvc19yZXBvcnQocmVxdWVzdCk6CiAgICByZXBvcnRfZmlsdGVyID0gX2dldF9yZXBvcnRfZmlsdGVyKHJlcXVlc3QpCiAgICByZXBvcnRfc29ydCA9IGdldF9yZXBvcnRfc29ydChyZXF1ZXN0KQoKICAgIHBlcmlvZHMgPSBfYnVpbGRfcGVyaW9kX3JhbmdlKAogICAgICAgIHJlcG9ydF9maWx0ZXJbInN0YXJ0X3llYXIiXSwKICAgICAgICByZXBvcnRfZmlsdGVyWyJzdGFydF9tb250aCJdLAogICAgICAgIHJlcG9ydF9maWx0ZXJbIm1vbnRoX2NvdW50Il0sCiAgICApCgogICAgbWV0cmljLCByb3dzID0gX2dldF9jbGllbnRlc19udWV2b3Nfcm93cyhwZXJpb2RzPXBlcmlvZHMpCiAgICByb3dzID0gc29ydF9yZXBvcnRfcm93cyhyb3dzLCByZXBvcnRfc29ydCkKICAgIAogICAgY29udGV4dCA9IHsKICAgICAgICAicm93cyI6IHJvd3MsCiAgICAgICAgIm1ldHJpYyI6IG1ldHJpYywKICAgICAgICAicmVwb3J0X2ZpbHRlciI6IHJlcG9ydF9maWx0ZXIsCiAgICAgICAgInJlcG9ydF9zb3J0IjogcmVwb3J0X3NvcnQsCiAgICAgICAgImF2YWlsYWJsZV9wZXJpb2RzIjogX2dldF9hdmFpbGFibGVfcGVyaW9kcygpLAogICAgICAgICJtb250aF9jb3VudF9vcHRpb25zIjogTU9OVEhfQ09VTlRfT1BUSU9OUywKICAgIH0KICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgInBnYy9jbGllbnRlc19udWV2b3MuaHRtbCIsIGNvbnRleHQpCgoKZGVmIF9nZXRfY2xpZW50ZXNfbnVldm9zX3Jvd3MocGVyaW9kcz1Ob25lKToKICAgIHRyeToKICAgICAgICBtZXRyaWMgPSBNZXRyaWNEZWZpbml0aW9uLm9iamVjdHMuZ2V0KGNvZGU9TWV0cmljRGVmaW5pdGlvbi5DT0RFX0NMSUVOVEVTX05VRVZPUykKICAgIGV4Y2VwdCBNZXRyaWNEZWZpbml0aW9uLkRvZXNOb3RFeGlzdDoKICAgICAgICBtZXRyaWMgPSBOb25lCgogICAgdGFyZ2V0cyA9IE1vbnRobHlUYXJnZXQub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgidW5lIiwgInBsYW4iKS5maWx0ZXIoCiAgICAgICAgbWV0cmljX19jb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9DTElFTlRFU19OVUVWT1MKICAgICkKICAgIHJlc3VsdHMgPSBNb250aGx5TWV0cmljUmVzdWx0Lm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoInVuZSIsICJwbGFuIiwgIm1ldHJpYyIpLmZpbHRlcigKICAgICAgICBtZXRyaWNfX2NvZGU9TWV0cmljRGVmaW5pdGlvbi5DT0RFX0NMSUVOVEVTX05VRVZPUwogICAgKQogICAgc2NvcmVjYXJkcyA9IE1vbnRobHlTY29yZWNhcmQub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgidW5lIiwgInBsYW4iKQoKICAgIGlmIHBlcmlvZHM6CiAgICAgICAgcGVyaW9kX3EgPSBfYnVpbGRfcGVyaW9kX3EocGVyaW9kcykKICAgICAgICB0YXJnZXRzID0gdGFyZ2V0cy5maWx0ZXIocGVyaW9kX3EpCiAgICAgICAgcmVzdWx0cyA9IHJlc3VsdHMuZmlsdGVyKHBlcmlvZF9xKQogICAgICAgIHNjb3JlY2FyZHMgPSBzY29yZWNhcmRzLmZpbHRlcihwZXJpb2RfcSkKCiAgICByZXN1bHRfbWFwID0ge30KICAgIGZvciByIGluIHJlc3VsdHM6CiAgICAgICAga2V5ID0gKHIucGxhbl9pZCwgci51bmVfaWQsIHIueWVhciwgci5tb250aCkKICAgICAgICByZXN1bHRfbWFwW2tleV0gPSByCgogICAgc2NvcmVfbWFwID0ge30KICAgIGZvciBzYyBpbiBzY29yZWNhcmRzOgogICAgICAgIGtleSA9IChzYy5wbGFuX2lkLCBzYy51bmVfaWQsIHNjLnllYXIsIHNjLm1vbnRoKQogICAgICAgIHNjb3JlX21hcFtrZXldID0gc2MKCiAgICBkZXRhaWxfcm93cyA9IE5ld0NsaWVudEltcG9ydFJvdy5vYmplY3RzLmZpbHRlcih1bmVfX2lzbnVsbD1GYWxzZSkKCiAgICBpZiBwZXJpb2RzOgogICAgICAgIGRldGFpbF9wZXJpb2RfcSA9IFEoKQogICAgICAgIGZvciB5ZWFyLCBtb250aCBpbiBwZXJpb2RzOgogICAgICAgICAgICBkZXRhaWxfcGVyaW9kX3EgfD0gUSh5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKQogICAgICAgICAgICBkZXRhaWxfcGVyaW9kX3EgfD0gUShoZWFkZXJfX3llYXI9eWVhciwgaGVhZGVyX19tb250aD1tb250aCkKICAgICAgICBkZXRhaWxfcm93cyA9IGRldGFpbF9yb3dzLmZpbHRlcihkZXRhaWxfcGVyaW9kX3EpCgogICAgZGV0YWlsX2tleXMgPSBzZXQoKQoKICAgIGZvciByb3cgaW4gZGV0YWlsX3Jvd3Muc2VsZWN0X3JlbGF0ZWQoImhlYWRlciIpOgogICAgICAgIHJvd195ZWFyID0gcm93LnllYXIgb3IgKHJvdy5oZWFkZXIueWVhciBpZiByb3cuaGVhZGVyIGVsc2UgTm9uZSkKICAgICAgICByb3dfbW9udGggPSByb3cubW9udGggb3IgKHJvdy5oZWFkZXIubW9udGggaWYgcm93LmhlYWRlciBlbHNlIE5vbmUpCgogICAgICAgIGlmIHJvdy51bmVfaWQgYW5kIHJvd195ZWFyIGFuZCByb3dfbW9udGg6CiAgICAgICAgICAgIGRldGFpbF9rZXlzLmFkZCgocm93LnVuZV9pZCwgcm93X3llYXIsIHJvd19tb250aCkpCgogICAgaW52ZXN0bWVudF9uZXdfY2xpZW50c19tYXAgPSB7fQogICAgaW52ZXN0bWVudF9pbmdyZXNvc19tYXAgPSB7fQogICAgCiAgICBpbnZlc3RtZW50X3VuZSA9ICgKICAgICAgICBVTkUub2JqZWN0cy5maWx0ZXIoY29kZV9faW49WyJJTlZFU1RNRU5UIiwgIklOVkVTVE1FTlRTIiwgIklOVkVSU0lPTkVTIl0pCiAgICAgICAgLm9yZGVyX2J5KCJzb3J0X29yZGVyIiwgImlkIikKICAgICAgICAuZmlyc3QoKQogICAgKQogICAgCiAgICBmeF9tYXAgPSB7CiAgICAgICAgKGl0ZW0ueWVhciwgaXRlbS5tb250aCk6IGl0ZW0udXNkX3RvX2d0cQogICAgICAgIGZvciBpdGVtIGluIE1vbnRobHlFeGNoYW5nZVJhdGUub2JqZWN0cy5hbGwoKQogICAgfQogICAgCiAgICBpZiBpbnZlc3RtZW50X3VuZToKICAgICAgICBmb3Igcm93IGluIGRldGFpbF9yb3dzLnNlbGVjdF9yZWxhdGVkKCJjdXJyZW5jeSIsICJoZWFkZXIiKToKICAgICAgICAgICAgcm93X3llYXIgPSByb3cueWVhciBvciAocm93LmhlYWRlci55ZWFyIGlmIHJvdy5oZWFkZXIgZWxzZSBOb25lKQogICAgICAgICAgICByb3dfbW9udGggPSByb3cubW9udGggb3IgKHJvdy5oZWFkZXIubW9udGggaWYgcm93LmhlYWRlciBlbHNlIE5vbmUpCiAgICAKICAgICAgICAgICAgaWYgcm93LnVuZV9pZCAhPSBpbnZlc3RtZW50X3VuZS5pZCBvciBub3Qgcm93X3llYXIgb3Igbm90IHJvd19tb250aDoKICAgICAgICAgICAgICAgIGNvbnRpbnVlCiAgICAKICAgICAgICAgICAga2V5ID0gKHJvdy51bmVfaWQsIHJvd195ZWFyLCByb3dfbW9udGgpCiAgICAKICAgICAgICAgICAgaWYgcm93LmNvdW50c19hc19uZXc6CiAgICAgICAgICAgICAgICBpbnZlc3RtZW50X25ld19jbGllbnRzX21hcFtrZXldID0gaW52ZXN0bWVudF9uZXdfY2xpZW50c19tYXAuZ2V0KGtleSwgMCkgKyAxCiAgICAKICAgICAgICAgICAgaW52ZXN0bWVudF9pbmdyZXNvc19tYXBba2V5XSA9ICgKICAgICAgICAgICAgICAgIGludmVzdG1lbnRfaW5ncmVzb3NfbWFwLmdldChrZXksIERlY2ltYWwoIjAiKSkKICAgICAgICAgICAgICAgICsgX2NvbnZlcnRfcm93X2Ftb3VudF90b191c2Qocm93LCBmeF9tYXApCiAgICAgICAgICAgICkKICAKICAgIHJvd3MgPSBbXQogICAgZm9yIHQgaW4gdGFyZ2V0cy5vcmRlcl9ieSgieWVhciIsICJtb250aCIsICJ1bmVfX3NvcnRfb3JkZXIiKToKICAgICAgICBrZXkgPSAodC5wbGFuX2lkLCB0LnVuZV9pZCwgdC55ZWFyLCB0Lm1vbnRoKQogICAgICAgIG1yID0gcmVzdWx0X21hcC5nZXQoa2V5KQogICAgICAgIHNjID0gc2NvcmVfbWFwLmdldChrZXkpCgogICAgICAgIHJlYWxfdmFsdWVfb3ZlcnJpZGUgPSBOb25lCiAgICAgICAgaWYgaW52ZXN0bWVudF91bmUgYW5kIHQudW5lX2lkID09IGludmVzdG1lbnRfdW5lLmlkOgogICAgICAgICAgICByZWFsX3ZhbHVlX292ZXJyaWRlID0gaW52ZXN0bWVudF9uZXdfY2xpZW50c19tYXAuZ2V0KCh0LnVuZV9pZCwgdC55ZWFyLCB0Lm1vbnRoKSwgMCkKICAgICAgCiAgICAgICAgcm93cy5hcHBlbmQoCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICJ0YXJnZXQiOiB0LAogICAgICAgICAgICAgICAgInJlc3VsdCI6IG1yLAogICAgICAgICAgICAgICAgInNjb3JlY2FyZCI6IHNjLAogICAgICAgICAgICAgICAgImhhc19kZXRhaWwiOiAodC51bmVfaWQsIHQueWVhciwgdC5tb250aCkgaW4gZGV0YWlsX2tleXMsCiAgICAgICAgICAgICAgICAiaW52ZXN0bWVudF9pbmdyZXNvcyI6IGludmVzdG1lbnRfaW5ncmVzb3NfbWFwLmdldCgodC51bmVfaWQsIHQueWVhciwgdC5tb250aCkpLAogICAgICAgICAgICAgICAgInJlYWxfdmFsdWVfb3ZlcnJpZGUiOiByZWFsX3ZhbHVlX292ZXJyaWRlLAogICAgICAgICAgICB9CiAgICAgICAgKQogICAgICAKICAgIHJldHVybiBtZXRyaWMsIHJvd3MKCgpkZWYgX2J1aWxkX2NsaWVudGVzX251ZXZvc19tYXJrZG93bihyb3dzLCByZXBvcnRfZmlsdGVyKToKICAgIGdlbmVyYXRlZF9hdCA9IGRhdGV0aW1lLm5vdygpLnN0cmZ0aW1lKCIlWS0lbS0lZCAlSDolTSIpCgogICAgc3RhcnRfeWVhciA9IHJlcG9ydF9maWx0ZXJbInN0YXJ0X3llYXIiXQogICAgc3RhcnRfbW9udGggPSByZXBvcnRfZmlsdGVyWyJzdGFydF9tb250aCJdCiAgICBtb250aF9jb3VudCA9IHJlcG9ydF9maWx0ZXJbIm1vbnRoX2NvdW50Il0KICAgIHBlcmlvZHMgPSBfYnVpbGRfcGVyaW9kX3JhbmdlKHN0YXJ0X3llYXIsIHN0YXJ0X21vbnRoLCBtb250aF9jb3VudCkKICAgIGVuZF95ZWFyLCBlbmRfbW9udGggPSBwZXJpb2RzWy0xXQoKICAgIGxpbmVzID0gWwogICAgICAgICIjIFBHQyAtIENsaWVudGVzIG51ZXZvcyB2cyBtZXRhIiwKICAgICAgICAiIiwKICAgICAgICBmIkdlbmVyYWRvOiB7Z2VuZXJhdGVkX2F0fSIsCiAgICAgICAgIiIsCiAgICAgICAgIiMjIEZpbHRyb3MiLAogICAgICAgIGYiLSBEZXNkZToge3N0YXJ0X3llYXJ9LXtzdGFydF9tb250aDowMmR9IiwKICAgICAgICBmIi0gSGFzdGE6IHtlbmRfeWVhcn0te2VuZF9tb250aDowMmR9IiwKICAgICAgICBmIi0gTWVzZXMgaW5jbHVpZG9zOiB7bW9udGhfY291bnR9IiwKICAgICAgICAiIiwKICAgICAgICAiIyMgRGVzY3JpcGNpw7NuIiwKICAgICAgICAiTWV0YSB5IHJlc3VsdGFkbyBtZW5zdWFsIGRlIGNsaWVudGVzIG51ZXZvcyBwb3IgVU5FIHkgcGVyaW9kby4iLAogICAgICAgICIiLAogICAgICAgICIjIyBEYXRvcyIsCiAgICAgICAgIiIsCiAgICAgICAgInwgVU5FIHwgUGVyaW9kbyB8IE1ldGEgY2xpZW50ZXMgfCBDbGllbnRlcyByZWFsZXMgfCBDdW1wbGUgfCBQdW50b3MgYXNpZ25hZG9zIHwgVG90YWwgZGVsIG1lcyB8IiwKICAgICAgICAifCA6LS0tIHwgOi0tLTogfCA6LS0tOiB8IDotLS06IHwgOi0tLTogfCA6LS0tOiB8IDotLS06IHwiLAogICAgXQoKICAgIGlmIG5vdCByb3dzOgogICAgICAgIGxpbmVzLmFwcGVuZCgifCBTaW4gZGF0b3MgfCAtIHwgLSB8IC0gfCAtIHwgLSB8IC0gfCIpCiAgICBlbHNlOgogICAgICAgIGZvciByb3cgaW4gcm93czoKICAgICAgICAgICAgaWYgcm93LmdldCgiaXNfc2VwYXJhdG9yIik6CiAgICAgICAgICAgICAgICBjb250aW51ZQogICAgICAgIAogICAgICAgICAgICB0YXJnZXQgPSByb3dbInRhcmdldCJdCiAgICAgICAgICAgIHJlc3VsdCA9IHJvd1sicmVzdWx0Il0KICAgICAgICAgICAgc2NvcmVjYXJkID0gcm93WyJzY29yZWNhcmQiXQoKICAgICAgICAgICAgcGVyaW9kbyA9IGYie3RhcmdldC55ZWFyfS17dGFyZ2V0Lm1vbnRoOjAyZH0iCiAgICAgICAgICAgIG1ldGEgPSBpbnQodGFyZ2V0LnRhcmdldF92YWx1ZSkgaWYgdGFyZ2V0LnRhcmdldF92YWx1ZSBpcyBub3QgTm9uZSBlbHNlICItIgogICAgICAgICAgICAKICAgICAgICAgICAgcmVhbF9vdmVycmlkZSA9IHJvdy5nZXQoInJlYWxfdmFsdWVfb3ZlcnJpZGUiLCBOb25lKQogICAgICAgICAgICBpZiByZWFsX292ZXJyaWRlIGlzIG5vdCBOb25lOgogICAgICAgICAgICAgICAgcmVhbGVzID0gaW50KHJlYWxfb3ZlcnJpZGUpCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICByZWFsZXMgPSBpbnQocmVzdWx0Lm1lYXN1cmVkX3ZhbHVlKSBpZiByZXN1bHQgYW5kIHJlc3VsdC5tZWFzdXJlZF92YWx1ZSBpcyBub3QgTm9uZSBlbHNlICItIgogICAgICAgICAgCiAgICAgICAgICAgIGN1bXBsZSA9ICJTw60iIGlmIHJlc3VsdCBhbmQgcmVzdWx0LmlzX2FjaGlldmVkIGVsc2UgIk5vIgogICAgICAgICAgICBwdW50b3MgPSByZXN1bHQucG9pbnRzX2F3YXJkZWQgaWYgcmVzdWx0IGVsc2UgMAogICAgICAgICAgICB0b3RhbF9tZXMgPSBzY29yZWNhcmQudG90YWxfcG9pbnRzIGlmIHNjb3JlY2FyZCBlbHNlIDAKCiAgICAgICAgICAgIGxpbmVzLmFwcGVuZCgKICAgICAgICAgICAgICAgIGYifCB7dGFyZ2V0LnVuZS5uYW1lX2VzfSB8IHtwZXJpb2RvfSB8IHttZXRhfSB8IHtyZWFsZXN9IHwge2N1bXBsZX0gfCB7cHVudG9zfSB8IHt0b3RhbF9tZXN9IHwiCiAgICAgICAgICAgICkKCiAgICBsaW5lcy5leHRlbmQoWwogICAgICAgICIiLAogICAgICAgICIjIyBOb3RhIiwKICAgICAgICAiRXN0ZSByZXBvcnRlIG11ZXN0cmEgbGEgbWV0YSBtZW5zdWFsIGRlIGNsaWVudGVzIG51ZXZvcywgZWwgcmVzdWx0YWRvIG9ic2VydmFkbyB5IHN1IGltcGFjdG8gZW4gZWwgcHVudGFqZSB0b3RhbCBkZWwgbWVzLiIsCiAgICAgICAgIiIsCiAgICBdKQogICAgcmV0dXJuICJcbiIuam9pbihsaW5lcykKCgpAbG9naW5fcmVxdWlyZWQKZGVmIGNsaWVudGVzX251ZXZvc19leHBvcnRfbWQocmVxdWVzdCk6CiAgICByZXBvcnRfZmlsdGVyID0gX2dldF9yZXBvcnRfZmlsdGVyKHJlcXVlc3QpCiAgICByZXBvcnRfc29ydCA9IGdldF9yZXBvcnRfc29ydChyZXF1ZXN0KQogICAgcGVyaW9kcyA9IF9idWlsZF9wZXJpb2RfcmFuZ2UoCiAgICAgICAgcmVwb3J0X2ZpbHRlclsic3RhcnRfeWVhciJdLAogICAgICAgIHJlcG9ydF9maWx0ZXJbInN0YXJ0X21vbnRoIl0sCiAgICAgICAgcmVwb3J0X2ZpbHRlclsibW9udGhfY291bnQiXSwKICAgICkKICAgIG1ldHJpYywgcm93cyA9IF9nZXRfY2xpZW50ZXNfbnVldm9zX3Jvd3MocGVyaW9kcz1wZXJpb2RzKQogICAgcm93cyA9IHNvcnRfcmVwb3J0X3Jvd3Mocm93cywgcmVwb3J0X3NvcnQpCgogICAgY29udGVudCA9IF9idWlsZF9jbGllbnRlc19udWV2b3NfbWFya2Rvd24ocm93cywgcmVwb3J0X2ZpbHRlcikKCiAgICBnZW5lcmF0ZWRfc3VmZml4ID0gZGF0ZXRpbWUubm93KCkuc3RyZnRpbWUoIiVZJW0lZC0lSCVNIikKICAgIHN0YXJ0X3llYXIgPSByZXBvcnRfZmlsdGVyWyJzdGFydF95ZWFyIl0KICAgIHN0YXJ0X21vbnRoID0gcmVwb3J0X2ZpbHRlclsic3RhcnRfbW9udGgiXQogICAgbW9udGhfY291bnQgPSByZXBvcnRfZmlsdGVyWyJtb250aF9jb3VudCJdCiAgICBmaWxlbmFtZSA9ICgKICAgICAgICBmInBnYy1jbGllbnRlcy1udWV2b3MtIgogICAgICAgIGYiZnl7c3RhcnRfeWVhcn0tbXtzdGFydF9tb250aDowMmR9LW57bW9udGhfY291bnR9LSIKICAgICAgICBmIntnZW5lcmF0ZWRfc3VmZml4fS5tZCIKICAgICkKCiAgICByZXNwb25zZSA9IEh0dHBSZXNwb25zZSgKICAgICAgICBzbWFydF9zdHIoY29udGVudCksCiAgICAgICAgY29udGVudF90eXBlPSJ0ZXh0L3BsYWluOyBjaGFyc2V0PXV0Zi04IiwKICAgICkKICAgIHJlc3BvbnNlWyJDb250ZW50LURpc3Bvc2l0aW9uIl0gPSBmJ2F0dGFjaG1lbnQ7IGZpbGVuYW1lPSJ7ZmlsZW5hbWV9IicKICAgIHJldHVybiByZXNwb25zZQoKCmRlZiBfZ2V0X3ZlbnRhX2NydXphZGFfcm93cyhwZXJpb2RzPU5vbmUpOgogICAgdHJ5OgogICAgICAgIG1ldHJpYyA9IE1ldHJpY0RlZmluaXRpb24ub2JqZWN0cy5nZXQoY29kZT1NZXRyaWNEZWZpbml0aW9uLkNPREVfVkVOVEFfQ1JVWkFEQSkKICAgIGV4Y2VwdCBNZXRyaWNEZWZpbml0aW9uLkRvZXNOb3RFeGlzdDoKICAgICAgICBtZXRyaWMgPSBOb25lCgogICAgdGFyZ2V0cyA9IE1vbnRobHlUYXJnZXQub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgidW5lIiwgInBsYW4iKS5maWx0ZXIoCiAgICAgICAgbWV0cmljX19jb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9WRU5UQV9DUlVaQURBCiAgICApCiAgICByZXN1bHRzID0gTW9udGhseU1ldHJpY1Jlc3VsdC5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJ1bmUiLCAicGxhbiIsICJtZXRyaWMiKS5maWx0ZXIoCiAgICAgICAgbWV0cmljX19jb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9WRU5UQV9DUlVaQURBCiAgICApCiAgICBzY29yZWNhcmRzID0gTW9udGhseVNjb3JlY2FyZC5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJ1bmUiLCAicGxhbiIpCgogICAgaWYgcGVyaW9kczoKICAgICAgICBwZXJpb2RfcSA9IF9idWlsZF9wZXJpb2RfcShwZXJpb2RzKQogICAgICAgIHRhcmdldHMgPSB0YXJnZXRzLmZpbHRlcihwZXJpb2RfcSkKICAgICAgICByZXN1bHRzID0gcmVzdWx0cy5maWx0ZXIocGVyaW9kX3EpCiAgICAgICAgc2NvcmVjYXJkcyA9IHNjb3JlY2FyZHMuZmlsdGVyKHBlcmlvZF9xKQoKICAgIHJlc3VsdF9tYXAgPSB7fQogICAgZm9yIHIgaW4gcmVzdWx0czoKICAgICAgICBrZXkgPSAoci5wbGFuX2lkLCByLnVuZV9pZCwgci55ZWFyLCByLm1vbnRoKQogICAgICAgIHJlc3VsdF9tYXBba2V5XSA9IHIKCiAgICBzY29yZV9tYXAgPSB7fQogICAgZm9yIHNjIGluIHNjb3JlY2FyZHM6CiAgICAgICAga2V5ID0gKHNjLnBsYW5faWQsIHNjLnVuZV9pZCwgc2MueWVhciwgc2MubW9udGgpCiAgICAgICAgc2NvcmVfbWFwW2tleV0gPSBzYwoKICAgIHJvd3MgPSBbXQogICAgZm9yIHQgaW4gdGFyZ2V0cy5vcmRlcl9ieSgieWVhciIsICJtb250aCIsICJ1bmVfX3NvcnRfb3JkZXIiKToKICAgICAgICBrZXkgPSAodC5wbGFuX2lkLCB0LnVuZV9pZCwgdC55ZWFyLCB0Lm1vbnRoKQogICAgICAgIG1yID0gcmVzdWx0X21hcC5nZXQoa2V5KQogICAgICAgIHNjID0gc2NvcmVfbWFwLmdldChrZXkpCiAgICAgICAgcm93cy5hcHBlbmQoewogICAgICAgICAgICAidGFyZ2V0IjogdCwKICAgICAgICAgICAgInJlc3VsdCI6IG1yLAogICAgICAgICAgICAic2NvcmVjYXJkIjogc2MsCiAgICAgICAgfSkKCiAgICByZXR1cm4gbWV0cmljLCByb3dzCiAgCgpAbG9naW5fcmVxdWlyZWQKZGVmIHZlbnRhX2NydXphZGFfcmVwb3J0KHJlcXVlc3QpOgogICAgcmVwb3J0X2ZpbHRlciA9IF9nZXRfcmVwb3J0X2ZpbHRlcihyZXF1ZXN0KQogICAgcmVwb3J0X3NvcnQgPSBnZXRfcmVwb3J0X3NvcnQocmVxdWVzdCkKCiAgICBwZXJpb2RzID0gX2J1aWxkX3BlcmlvZF9yYW5nZSgKICAgICAgICByZXBvcnRfZmlsdGVyWyJzdGFydF95ZWFyIl0sCiAgICAgICAgcmVwb3J0X2ZpbHRlclsic3RhcnRfbW9udGgiXSwKICAgICAgICByZXBvcnRfZmlsdGVyWyJtb250aF9jb3VudCJdLAogICAgKQoKICAgIG1ldHJpYywgcm93cyA9IF9nZXRfdmVudGFfY3J1emFkYV9yb3dzKHBlcmlvZHM9cGVyaW9kcykKICAgIHJvd3MgPSBzb3J0X3JlcG9ydF9yb3dzKHJvd3MsIHJlcG9ydF9zb3J0KQogICAgCiAgICBjb250ZXh0ID0gewogICAgICAgICJyb3dzIjogcm93cywKICAgICAgICAibWV0cmljIjogbWV0cmljLAogICAgICAgICJyZXBvcnRfZmlsdGVyIjogcmVwb3J0X2ZpbHRlciwKICAgICAgICAicmVwb3J0X3NvcnQiOiByZXBvcnRfc29ydCwKICAgICAgICAiYXZhaWxhYmxlX3BlcmlvZHMiOiBfZ2V0X2F2YWlsYWJsZV9wZXJpb2RzKCksCiAgICAgICAgIm1vbnRoX2NvdW50X29wdGlvbnMiOiBNT05USF9DT1VOVF9PUFRJT05TLAogICAgfQogICAgcmV0dXJuIHJlbmRlcihyZXF1ZXN0LCAicGdjL3ZlbnRhX2NydXphZGEuaHRtbCIsIGNvbnRleHQpCgoKZGVmIF9idWlsZF92ZW50YV9jcnV6YWRhX21hcmtkb3duKHJvd3MsIHJlcG9ydF9maWx0ZXIpOgogICAgZ2VuZXJhdGVkX2F0ID0gZGF0ZXRpbWUubm93KCkuc3RyZnRpbWUoIiVZLSVtLSVkICVIOiVNIikKCiAgICBzdGFydF95ZWFyID0gcmVwb3J0X2ZpbHRlclsic3RhcnRfeWVhciJdCiAgICBzdGFydF9tb250aCA9IHJlcG9ydF9maWx0ZXJbInN0YXJ0X21vbnRoIl0KICAgIG1vbnRoX2NvdW50ID0gcmVwb3J0X2ZpbHRlclsibW9udGhfY291bnQiXQogICAgcGVyaW9kcyA9IF9idWlsZF9wZXJpb2RfcmFuZ2Uoc3RhcnRfeWVhciwgc3RhcnRfbW9udGgsIG1vbnRoX2NvdW50KQogICAgZW5kX3llYXIsIGVuZF9tb250aCA9IHBlcmlvZHNbLTFdCgogICAgbGluZXMgPSBbCiAgICAgICAgIiMgUEdDIC0gVmVudGEgY3J1emFkYSB2cyBtZXRhIiwKICAgICAgICAiIiwKICAgICAgICBmIkdlbmVyYWRvOiB7Z2VuZXJhdGVkX2F0fSIsCiAgICAgICAgIiIsCiAgICAgICAgIiMjIEZpbHRyb3MiLAogICAgICAgIGYiLSBEZXNkZToge3N0YXJ0X3llYXJ9LXtzdGFydF9tb250aDowMmR9IiwKICAgICAgICBmIi0gSGFzdGE6IHtlbmRfeWVhcn0te2VuZF9tb250aDowMmR9IiwKICAgICAgICBmIi0gTWVzZXMgaW5jbHVpZG9zOiB7bW9udGhfY291bnR9IiwKICAgICAgICAiIiwKICAgICAgICAiIyMgRGVzY3JpcGNpw7NuIiwKICAgICAgICAiTWV0YSB5IHJlc3VsdGFkbyBtZW5zdWFsIGRlIHZlbnRhIGNydXphZGEgcG9yIFVORSB5IHBlcmlvZG8uIiwKICAgICAgICAiIiwKICAgICAgICAiIyMgRGF0b3MiLAogICAgICAgICIiLAogICAgICAgICJ8IFVORSB8IFBlcmlvZG8gfCBNZXRhIHZlbnRhIGNydXphZGEgfCBWZW50YSBjcnV6YWRhIHJlYWwgfCBDdW1wbGUgfCBQdW50b3MgYXNpZ25hZG9zIHwgVG90YWwgZGVsIG1lcyB8IiwKICAgICAgICAifCA6LS0tIHwgOi0tLTogfCA6LS0tOiB8IDotLS06IHwgOi0tLTogfCA6LS0tOiB8IDotLS06IHwiLAogICAgXQoKICAgIGlmIG5vdCByb3dzOgogICAgICAgIGxpbmVzLmFwcGVuZCgifCBTaW4gZGF0b3MgfCAtIHwgLSB8IC0gfCAtIHwgLSB8IC0gfCIpCiAgICBlbHNlOgogICAgICAgIGZvciByb3cgaW4gcm93czoKICAgICAgICAgICAgaWYgcm93LmdldCgiaXNfc2VwYXJhdG9yIik6CiAgICAgICAgICAgICAgICBjb250aW51ZQogICAgICAgIAogICAgICAgICAgICB0YXJnZXQgPSByb3dbInRhcmdldCJdCiAgICAgICAgICAgIHJlc3VsdCA9IHJvd1sicmVzdWx0Il0KICAgICAgICAgICAgc2NvcmVjYXJkID0gcm93WyJzY29yZWNhcmQiXSAgICAgICAgICAKCiAgICAgICAgICAgIHBlcmlvZG8gPSBmInt0YXJnZXQueWVhcn0te3RhcmdldC5tb250aDowMmR9IgogICAgICAgICAgICBtZXRhID0gaW50KHRhcmdldC50YXJnZXRfdmFsdWUpIGlmIHRhcmdldC50YXJnZXRfdmFsdWUgaXMgbm90IE5vbmUgZWxzZSAiLSIKICAgICAgICAgICAgcmVhbGVzID0gaW50KHJlc3VsdC5tZWFzdXJlZF92YWx1ZSkgaWYgcmVzdWx0IGFuZCByZXN1bHQubWVhc3VyZWRfdmFsdWUgaXMgbm90IE5vbmUgZWxzZSAiLSIKICAgICAgICAgICAgY3VtcGxlID0gIlPDrSIgaWYgcmVzdWx0IGFuZCByZXN1bHQuaXNfYWNoaWV2ZWQgZWxzZSAiTm8iCiAgICAgICAgICAgIHB1bnRvcyA9IHJlc3VsdC5wb2ludHNfYXdhcmRlZCBpZiByZXN1bHQgZWxzZSAwCiAgICAgICAgICAgIHRvdGFsX21lcyA9IHNjb3JlY2FyZC50b3RhbF9wb2ludHMgaWYgc2NvcmVjYXJkIGVsc2UgMAoKICAgICAgICAgICAgbGluZXMuYXBwZW5kKAogICAgICAgICAgICAgICAgZiJ8IHt0YXJnZXQudW5lLm5hbWVfZXN9IHwge3BlcmlvZG99IHwge21ldGF9IHwge3JlYWxlc30gfCB7Y3VtcGxlfSB8IHtwdW50b3N9IHwge3RvdGFsX21lc30gfCIKICAgICAgICAgICAgKQoKICAgIGxpbmVzLmV4dGVuZChbCiAgICAgICAgIiIsCiAgICAgICAgIiMjIE5vdGEiLAogICAgICAgICJFc3RlIHJlcG9ydGUgbXVlc3RyYSBsYSBtZXRhIG1lbnN1YWwgZGUgdmVudGEgY3J1emFkYSwgZWwgcmVzdWx0YWRvIG9ic2VydmFkbyB5IHN1IGltcGFjdG8gZW4gZWwgcHVudGFqZSB0b3RhbCBkZWwgbWVzLiIsCiAgICAgICAgIiIsCiAgICBdKQogICAgcmV0dXJuICJcbiIuam9pbihsaW5lcykKCgpAbG9naW5fcmVxdWlyZWQKZGVmIHZlbnRhX2NydXphZGFfZXhwb3J0X21kKHJlcXVlc3QpOgogICAgcmVwb3J0X2ZpbHRlciA9IF9nZXRfcmVwb3J0X2ZpbHRlcihyZXF1ZXN0KQogICAgcmVwb3J0X3NvcnQgPSBnZXRfcmVwb3J0X3NvcnQocmVxdWVzdCkKICAgIHBlcmlvZHMgPSBfYnVpbGRfcGVyaW9kX3JhbmdlKAogICAgICAgIHJlcG9ydF9maWx0ZXJbInN0YXJ0X3llYXIiXSwKICAgICAgICByZXBvcnRfZmlsdGVyWyJzdGFydF9tb250aCJdLAogICAgICAgIHJlcG9ydF9maWx0ZXJbIm1vbnRoX2NvdW50Il0sCiAgICApCiAgICBtZXRyaWMsIHJvd3MgPSBfZ2V0X3ZlbnRhX2NydXphZGFfcm93cyhwZXJpb2RzPXBlcmlvZHMpCiAgICByb3dzID0gc29ydF9yZXBvcnRfcm93cyhyb3dzLCByZXBvcnRfc29ydCkKCiAgICBjb250ZW50ID0gX2J1aWxkX3ZlbnRhX2NydXphZGFfbWFya2Rvd24ocm93cywgcmVwb3J0X2ZpbHRlcikKCiAgICBnZW5lcmF0ZWRfc3VmZml4ID0gZGF0ZXRpbWUubm93KCkuc3RyZnRpbWUoIiVZJW0lZC0lSCVNIikKICAgIHN0YXJ0X3llYXIgPSByZXBvcnRfZmlsdGVyWyJzdGFydF95ZWFyIl0KICAgIHN0YXJ0X21vbnRoID0gcmVwb3J0X2ZpbHRlclsic3RhcnRfbW9udGgiXQogICAgbW9udGhfY291bnQgPSByZXBvcnRfZmlsdGVyWyJtb250aF9jb3VudCJdCiAgICBmaWxlbmFtZSA9ICgKICAgICAgICBmInBnYy12ZW50YS1jcnV6YWRhLSIKICAgICAgICBmImZ5e3N0YXJ0X3llYXJ9LW17c3RhcnRfbW9udGg6MDJkfS1ue21vbnRoX2NvdW50fS0iCiAgICAgICAgZiJ7Z2VuZXJhdGVkX3N1ZmZpeH0ubWQiCiAgICApCgogICAgcmVzcG9uc2UgPSBIdHRwUmVzcG9uc2UoCiAgICAgICAgc21hcnRfc3RyKGNvbnRlbnQpLAogICAgICAgIGNvbnRlbnRfdHlwZT0idGV4dC9wbGFpbjsgY2hhcnNldD11dGYtOCIsCiAgICApCiAgICByZXNwb25zZVsiQ29udGVudC1EaXNwb3NpdGlvbiJdID0gZidhdHRhY2htZW50OyBmaWxlbmFtZT0ie2ZpbGVuYW1lfSInCiAgICByZXR1cm4gcmVzcG9uc2UKCgpkZWYgX2dldF9yZXNwdWVzdGFfcmVxc19yb3dzKHBlcmlvZHM9Tm9uZSk6CiAgICB0cnk6CiAgICAgICAgbWV0cmljID0gTWV0cmljRGVmaW5pdGlvbi5vYmplY3RzLmdldChjb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9SRVNQVUVTVEFfUkVRUykKICAgIGV4Y2VwdCBNZXRyaWNEZWZpbml0aW9uLkRvZXNOb3RFeGlzdDoKICAgICAgICBtZXRyaWMgPSBOb25lCgogICAgdGFyZ2V0cyA9IE1vbnRobHlUYXJnZXQub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgidW5lIiwgInBsYW4iKS5maWx0ZXIoCiAgICAgICAgbWV0cmljX19jb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9SRVNQVUVTVEFfUkVRUwogICAgKQogICAgcmVzdWx0cyA9IE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgidW5lIiwgInBsYW4iLCAibWV0cmljIikuZmlsdGVyKAogICAgICAgIG1ldHJpY19fY29kZT1NZXRyaWNEZWZpbml0aW9uLkNPREVfUkVTUFVFU1RBX1JFUVMKICAgICkKICAgIHNjb3JlY2FyZHMgPSBNb250aGx5U2NvcmVjYXJkLm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoInVuZSIsICJwbGFuIikKCiAgICBpZiBwZXJpb2RzOgogICAgICAgIHBlcmlvZF9xID0gX2J1aWxkX3BlcmlvZF9xKHBlcmlvZHMpCiAgICAgICAgdGFyZ2V0cyA9IHRhcmdldHMuZmlsdGVyKHBlcmlvZF9xKQogICAgICAgIHJlc3VsdHMgPSByZXN1bHRzLmZpbHRlcihwZXJpb2RfcSkKICAgICAgICBzY29yZWNhcmRzID0gc2NvcmVjYXJkcy5maWx0ZXIocGVyaW9kX3EpCgogICAgcmVzdWx0X21hcCA9IHt9CiAgICBmb3IgciBpbiByZXN1bHRzOgogICAgICAgIGtleSA9IChyLnBsYW5faWQsIHIudW5lX2lkLCByLnllYXIsIHIubW9udGgpCiAgICAgICAgcmVzdWx0X21hcFtrZXldID0gcgoKICAgIHNjb3JlX21hcCA9IHt9CiAgICBmb3Igc2MgaW4gc2NvcmVjYXJkczoKICAgICAgICBrZXkgPSAoc2MucGxhbl9pZCwgc2MudW5lX2lkLCBzYy55ZWFyLCBzYy5tb250aCkKICAgICAgICBzY29yZV9tYXBba2V5XSA9IHNjCgogICAgcm93cyA9IFtdCiAgICBmb3IgdCBpbiB0YXJnZXRzLm9yZGVyX2J5KCJ5ZWFyIiwgIm1vbnRoIiwgInVuZV9fc29ydF9vcmRlciIpOgogICAgICAgIGtleSA9ICh0LnBsYW5faWQsIHQudW5lX2lkLCB0LnllYXIsIHQubW9udGgpCiAgICAgICAgbXIgPSByZXN1bHRfbWFwLmdldChrZXkpCiAgICAgICAgc2MgPSBzY29yZV9tYXAuZ2V0KGtleSkKICAgICAgICByb3dzLmFwcGVuZCh7CiAgICAgICAgICAgICJ0YXJnZXQiOiB0LAogICAgICAgICAgICAicmVzdWx0IjogbXIsCiAgICAgICAgICAgICJzY29yZWNhcmQiOiBzYywKICAgICAgICB9KQoKICAgIHJldHVybiBtZXRyaWMsIHJvd3MKICAKCkBsb2dpbl9yZXF1aXJlZApkZWYgcmVzcHVlc3RhX3JlcXNfcmVwb3J0KHJlcXVlc3QpOgogICAgcmVwb3J0X2ZpbHRlciA9IF9nZXRfcmVwb3J0X2ZpbHRlcihyZXF1ZXN0KQogICAgcmVwb3J0X3NvcnQgPSBnZXRfcmVwb3J0X3NvcnQocmVxdWVzdCkKCiAgICBwZXJpb2RzID0gX2J1aWxkX3BlcmlvZF9yYW5nZSgKICAgICAgICByZXBvcnRfZmlsdGVyWyJzdGFydF95ZWFyIl0sCiAgICAgICAgcmVwb3J0X2ZpbHRlclsic3RhcnRfbW9udGgiXSwKICAgICAgICByZXBvcnRfZmlsdGVyWyJtb250aF9jb3VudCJdLAogICAgKQoKICAgIG1ldHJpYywgcm93cyA9IF9nZXRfcmVzcHVlc3RhX3JlcXNfcm93cyhwZXJpb2RzPXBlcmlvZHMpCiAgICByb3dzID0gc29ydF9yZXBvcnRfcm93cyhyb3dzLCByZXBvcnRfc29ydCkKCiAgICBjb250ZXh0ID0gewogICAgICAgICJyb3dzIjogcm93cywKICAgICAgICAibWV0cmljIjogbWV0cmljLAogICAgICAgICJyZXBvcnRfZmlsdGVyIjogcmVwb3J0X2ZpbHRlciwKICAgICAgICAicmVwb3J0X3NvcnQiOiByZXBvcnRfc29ydCwKICAgICAgICAiYXZhaWxhYmxlX3BlcmlvZHMiOiBfZ2V0X2F2YWlsYWJsZV9wZXJpb2RzKCksCiAgICAgICAgIm1vbnRoX2NvdW50X29wdGlvbnMiOiBNT05USF9DT1VOVF9PUFRJT05TLAogICAgfQogICAgcmV0dXJuIHJlbmRlcihyZXF1ZXN0LCAicGdjL3Jlc3B1ZXN0YV9yZXFzLmh0bWwiLCBjb250ZXh0KQoKCmRlZiBfYnVpbGRfcmVzcHVlc3RhX3JlcXNfbWFya2Rvd24ocm93cywgcmVwb3J0X2ZpbHRlcik6CiAgICBnZW5lcmF0ZWRfYXQgPSBkYXRldGltZS5ub3coKS5zdHJmdGltZSgiJVktJW0tJWQgJUg6JU0iKQoKICAgIHN0YXJ0X3llYXIgPSByZXBvcnRfZmlsdGVyWyJzdGFydF95ZWFyIl0KICAgIHN0YXJ0X21vbnRoID0gcmVwb3J0X2ZpbHRlclsic3RhcnRfbW9udGgiXQogICAgbW9udGhfY291bnQgPSByZXBvcnRfZmlsdGVyWyJtb250aF9jb3VudCJdCiAgICBwZXJpb2RzID0gX2J1aWxkX3BlcmlvZF9yYW5nZShzdGFydF95ZWFyLCBzdGFydF9tb250aCwgbW9udGhfY291bnQpCiAgICBlbmRfeWVhciwgZW5kX21vbnRoID0gcGVyaW9kc1stMV0KCiAgICBsaW5lcyA9IFsKICAgICAgICAiIyBQR0MgLSBSZXNwdWVzdGEgYSByZXF1ZXJpbWllbnRvcyB2cyBtZXRhIiwKICAgICAgICAiIiwKICAgICAgICBmIkdlbmVyYWRvOiB7Z2VuZXJhdGVkX2F0fSIsCiAgICAgICAgIiIsCiAgICAgICAgIiMjIEZpbHRyb3MiLAogICAgICAgIGYiLSBEZXNkZToge3N0YXJ0X3llYXJ9LXtzdGFydF9tb250aDowMmR9IiwKICAgICAgICBmIi0gSGFzdGE6IHtlbmRfeWVhcn0te2VuZF9tb250aDowMmR9IiwKICAgICAgICBmIi0gTWVzZXMgaW5jbHVpZG9zOiB7bW9udGhfY291bnR9IiwKICAgICAgICAiIiwKICAgICAgICAiIyMgRGVzY3JpcGNpw7NuIiwKICAgICAgICAiTWV0YSB5IHJlc3VsdGFkbyBtZW5zdWFsIGRlIHJlc3B1ZXN0YSBhIHJlcXVlcmltaWVudG9zIHBvciBVTkUgeSBwZXJpb2RvLiIsCiAgICAgICAgIiIsCiAgICAgICAgIiMjIERhdG9zIiwKICAgICAgICAiIiwKICAgICAgICAifCBVTkUgfCBQZXJpb2RvIHwgTWV0YSByZXNwdWVzdGEgcmVxcyB8IFJlc3B1ZXN0YSByZXFzIHJlYWwgfCBDdW1wbGUgfCBQdW50b3MgYXNpZ25hZG9zIHwgVG90YWwgZGVsIG1lcyB8IiwKICAgICAgICAifCA6LS0tIHwgOi0tLTogfCA6LS0tOiB8IDotLS06IHwgOi0tLTogfCA6LS0tOiB8IDotLS06IHwiLAogICAgXQoKICAgIGlmIG5vdCByb3dzOgogICAgICAgIGxpbmVzLmFwcGVuZCgifCBTaW4gZGF0b3MgfCAtIHwgLSB8IC0gfCAtIHwgLSB8IC0gfCIpCiAgICBlbHNlOgogICAgICAgIGZvciByb3cgaW4gcm93czoKICAgICAgICAgICAgaWYgcm93LmdldCgiaXNfc2VwYXJhdG9yIik6CiAgICAgICAgICAgICAgICBjb250aW51ZQogICAgICAgIAogICAgICAgICAgICB0YXJnZXQgPSByb3dbInRhcmdldCJdCiAgICAgICAgICAgIHJlc3VsdCA9IHJvd1sicmVzdWx0Il0KICAgICAgICAgICAgc2NvcmVjYXJkID0gcm93WyJzY29yZWNhcmQiXQogICAgICAgICAgCiAgICAgICAgICAgIHBlcmlvZG8gPSBmInt0YXJnZXQueWVhcn0te3RhcmdldC5tb250aDowMmR9IgogICAgICAgICAgICBtZXRhID0gaW50KHRhcmdldC50YXJnZXRfdmFsdWUpIGlmIHRhcmdldC50YXJnZXRfdmFsdWUgaXMgbm90IE5vbmUgZWxzZSAiLSIKICAgICAgICAgICAgcmVhbGVzID0gaW50KHJlc3VsdC5tZWFzdXJlZF92YWx1ZSkgaWYgcmVzdWx0IGFuZCByZXN1bHQubWVhc3VyZWRfdmFsdWUgaXMgbm90IE5vbmUgZWxzZSAiLSIKICAgICAgICAgICAgY3VtcGxlID0gIlPDrSIgaWYgcmVzdWx0IGFuZCByZXN1bHQuaXNfYWNoaWV2ZWQgZWxzZSAiTm8iCiAgICAgICAgICAgIHB1bnRvcyA9IHJlc3VsdC5wb2ludHNfYXdhcmRlZCBpZiByZXN1bHQgZWxzZSAwCiAgICAgICAgICAgIHRvdGFsX21lcyA9IHNjb3JlY2FyZC50b3RhbF9wb2ludHMgaWYgc2NvcmVjYXJkIGVsc2UgMAoKICAgICAgICAgICAgbGluZXMuYXBwZW5kKAogICAgICAgICAgICAgICAgZiJ8IHt0YXJnZXQudW5lLm5hbWVfZXN9IHwge3BlcmlvZG99IHwge21ldGF9IHwge3JlYWxlc30gfCB7Y3VtcGxlfSB8IHtwdW50b3N9IHwge3RvdGFsX21lc30gfCIKICAgICAgICAgICAgKQoKICAgIGxpbmVzLmV4dGVuZChbCiAgICAgICAgIiIsCiAgICAgICAgIiMjIE5vdGEiLAogICAgICAgICJFc3RlIHJlcG9ydGUgbXVlc3RyYSBsYSBtZXRhIG1lbnN1YWwgZGUgcmVzcHVlc3RhIGEgcmVxdWVyaW1pZW50b3MsIGVsIHJlc3VsdGFkbyBvYnNlcnZhZG8geSBzdSBpbXBhY3RvIGVuIGVsIHB1bnRhamUgdG90YWwgZGVsIG1lcy4iLAogICAgICAgICIiLAogICAgXSkKICAgIHJldHVybiAiXG4iLmpvaW4obGluZXMpCgoKQGxvZ2luX3JlcXVpcmVkCmRlZiByZXNwdWVzdGFfcmVxc19leHBvcnRfbWQocmVxdWVzdCk6CiAgICByZXBvcnRfZmlsdGVyID0gX2dldF9yZXBvcnRfZmlsdGVyKHJlcXVlc3QpCiAgICByZXBvcnRfc29ydCA9IGdldF9yZXBvcnRfc29ydChyZXF1ZXN0KQogICAgcGVyaW9kcyA9IF9idWlsZF9wZXJpb2RfcmFuZ2UoCiAgICAgICAgcmVwb3J0X2ZpbHRlclsic3RhcnRfeWVhciJdLAogICAgICAgIHJlcG9ydF9maWx0ZXJbInN0YXJ0X21vbnRoIl0sCiAgICAgICAgcmVwb3J0X2ZpbHRlclsibW9udGhfY291bnQiXSwKICAgICkKICAgIG1ldHJpYywgcm93cyA9IF9nZXRfcmVzcHVlc3RhX3JlcXNfcm93cyhwZXJpb2RzPXBlcmlvZHMpCiAgICByb3dzID0gc29ydF9yZXBvcnRfcm93cyhyb3dzLCByZXBvcnRfc29ydCkKCiAgICBjb250ZW50ID0gX2J1aWxkX3Jlc3B1ZXN0YV9yZXFzX21hcmtkb3duKHJvd3MsIHJlcG9ydF9maWx0ZXIpCgogICAgZ2VuZXJhdGVkX3N1ZmZpeCA9IGRhdGV0aW1lLm5vdygpLnN0cmZ0aW1lKCIlWSVtJWQtJUglTSIpCiAgICBzdGFydF95ZWFyID0gcmVwb3J0X2ZpbHRlclsic3RhcnRfeWVhciJdCiAgICBzdGFydF9tb250aCA9IHJlcG9ydF9maWx0ZXJbInN0YXJ0X21vbnRoIl0KICAgIG1vbnRoX2NvdW50ID0gcmVwb3J0X2ZpbHRlclsibW9udGhfY291bnQiXQogICAgZmlsZW5hbWUgPSAoCiAgICAgICAgZiJwZ2MtcmVzcHVlc3RhLXJlcXMtIgogICAgICAgIGYiZnl7c3RhcnRfeWVhcn0tbXtzdGFydF9tb250aDowMmR9LW57bW9udGhfY291bnR9LSIKICAgICAgICBmIntnZW5lcmF0ZWRfc3VmZml4fS5tZCIKICAgICkKCiAgICByZXNwb25zZSA9IEh0dHBSZXNwb25zZSgKICAgICAgICBzbWFydF9zdHIoY29udGVudCksCiAgICAgICAgY29udGVudF90eXBlPSJ0ZXh0L3BsYWluOyBjaGFyc2V0PXV0Zi04IiwKICAgICkKICAgIHJlc3BvbnNlWyJDb250ZW50LURpc3Bvc2l0aW9uIl0gPSBmJ2F0dGFjaG1lbnQ7IGZpbGVuYW1lPSJ7ZmlsZW5hbWV9IicKICAgIHJldHVybiByZXNwb25zZQoKCmRlZiBfZ2V0X2luZ3Jlc29zX3Jvd3MocGVyaW9kcz1Ob25lKToKCiAgICBpbnZlc3RtZW50X3VuZSA9IGdldF9pbnZlc3RtZW50X3VuZSgpCiAgICBmeF9tYXAgPSBidWlsZF9meF9tYXAoKQogICAgaW52ZXN0bWVudF9yZWFsX21hcCA9IGludmVzdG1lbnRfcmVhbF9tYXBfZm9yX3BlcmlvZHMoCiAgICAgICAgcGVyaW9kcywgdW5lPWludmVzdG1lbnRfdW5lLCBmeF9tYXA9ZnhfbWFwCiAgICApCgogIAogICAgdHJ5OgogICAgICAgIG1ldHJpYyA9IE1ldHJpY0RlZmluaXRpb24ub2JqZWN0cy5nZXQoY29kZT1NZXRyaWNEZWZpbml0aW9uLkNPREVfSU5HUkVTT1MpCiAgICBleGNlcHQgTWV0cmljRGVmaW5pdGlvbi5Eb2VzTm90RXhpc3Q6CiAgICAgICAgbWV0cmljID0gTm9uZQoKICAgIHRhcmdldHMgPSBNb250aGx5VGFyZ2V0Lm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoInVuZSIsICJwbGFuIiwgIm1ldHJpYyIpLmZpbHRlcigKICAgICAgICBtZXRyaWNfX2NvZGU9TWV0cmljRGVmaW5pdGlvbi5DT0RFX0lOR1JFU09TCiAgICApCiAgICByZXN1bHRzID0gTW9udGhseU1ldHJpY1Jlc3VsdC5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKCJ1bmUiLCAicGxhbiIsICJtZXRyaWMiKS5maWx0ZXIoCiAgICAgICAgbWV0cmljX19jb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9JTkdSRVNPUwogICAgKQogICAgc2NvcmVjYXJkcyA9IE1vbnRobHlTY29yZWNhcmQub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgidW5lIiwgInBsYW4iKQoKICAgIGlmIHBlcmlvZHM6CiAgICAgICAgcGVyaW9kX3EgPSBfYnVpbGRfcGVyaW9kX3EocGVyaW9kcykKICAgICAgICB0YXJnZXRzID0gdGFyZ2V0cy5maWx0ZXIocGVyaW9kX3EpCiAgICAgICAgcmVzdWx0cyA9IHJlc3VsdHMuZmlsdGVyKHBlcmlvZF9xKQogICAgICAgIHNjb3JlY2FyZHMgPSBzY29yZWNhcmRzLmZpbHRlcihwZXJpb2RfcSkKCiAgICByZXN1bHRfbWFwID0ge30KICAgIGZvciByIGluIHJlc3VsdHM6CiAgICAgICAga2V5ID0gKHIucGxhbl9pZCwgci51bmVfaWQsIHIueWVhciwgci5tb250aCkKICAgICAgICByZXN1bHRfbWFwW2tleV0gPSByCgogICAgc2NvcmVfbWFwID0ge30KICAgIGZvciBzYyBpbiBzY29yZWNhcmRzOgogICAgICAgIGtleSA9IChzYy5wbGFuX2lkLCBzYy51bmVfaWQsIHNjLnllYXIsIHNjLm1vbnRoKQogICAgICAgIHNjb3JlX21hcFtrZXldID0gc2MKCiAgICByb3dzID0gW10KICAgIGZvciB0YXJnZXQgaW4gdGFyZ2V0cy5vcmRlcl9ieSgiLXllYXIiLCAiLW1vbnRoIiwgInVuZV9fc29ydF9vcmRlciIsICJ1bmVfX25hbWVfZXMiKToKICAgICAgICBrZXkgPSAodGFyZ2V0LnBsYW5faWQsIHRhcmdldC51bmVfaWQsIHRhcmdldC55ZWFyLCB0YXJnZXQubW9udGgpCiAgICAgICAgcmVzdWx0ID0gcmVzdWx0X21hcC5nZXQoa2V5KQogICAgICAgIHNjb3JlY2FyZCA9IHNjb3JlX21hcC5nZXQoa2V5KQoKICAgICAgICBtZXRhID0gdGFyZ2V0LnRhcmdldF92YWx1ZSBpZiB0YXJnZXQudGFyZ2V0X3ZhbHVlIGlzIG5vdCBOb25lIGVsc2UgTm9uZQogICAgICAgIHJlYWwgPSByZXN1bHQubWVhc3VyZWRfdmFsdWUgaWYgcmVzdWx0IGFuZCByZXN1bHQubWVhc3VyZWRfdmFsdWUgaXMgbm90IE5vbmUgZWxzZSBOb25lCgogICAgICAgIGludmVzdG1lbnRfY29kZXMgPSB7IklOVkVTVE1FTlQiLCAiSU5WRVNUTUVOVFMiLCAiSU5WRVJTSU9ORVMifQogICAgICAgIAogICAgICAgIGlmIHRhcmdldC51bmUuY29kZSBpbiBpbnZlc3RtZW50X2NvZGVzOgogICAgICAgICAgICByZWFsID0gaW52ZXN0bWVudF9yZWFsX21hcC5nZXQoCiAgICAgICAgICAgICAgICAodGFyZ2V0LnllYXIsIHRhcmdldC5tb250aCwgdGFyZ2V0LnVuZV9pZCksCiAgICAgICAgICAgICAgICBEZWNpbWFsKCIwIiksCiAgICAgICAgICAgICkKCiAgICAgICAgIyBJbnN1cmFuY2Ugc2llbXByZSBjb24gMyBkZWNpbWFsZXMKICAgICAgICBpZiB0YXJnZXQudW5lLmNvZGUgPT0gIklOU1VSQU5DRSI6CiAgICAgICAgICAgIGlmIG1ldGEgaXMgbm90IE5vbmU6CiAgICAgICAgICAgICAgICBtZXRhID0gbWV0YS5xdWFudGl6ZShEZWNpbWFsKCIwLjAwMSIpLCByb3VuZGluZz1ST1VORF9ET1dOKQogICAgICAgICAgICBpZiByZWFsIGlzIG5vdCBOb25lOgogICAgICAgICAgICAgICAgcmVhbCA9IHJlYWwucXVhbnRpemUoRGVjaW1hbCgiMC4wMDEiKSwgcm91bmRpbmc9Uk9VTkRfRE9XTikKCiAgICAgICAgaWYgbWV0YSBpcyBub3QgTm9uZSBhbmQgcmVhbCBpcyBub3QgTm9uZToKICAgICAgICAgICAgZGlmZXJlbmNpYSA9IHJlYWwgLSBtZXRhCiAgICAgICAgICAgIGlmIHRhcmdldC51bmUuY29kZSA9PSAiSU5TVVJBTkNFIjoKICAgICAgICAgICAgICAgIGRpZmVyZW5jaWEgPSBkaWZlcmVuY2lhLnF1YW50aXplKERlY2ltYWwoIjAuMDAxIiksIHJvdW5kaW5nPVJPVU5EX0RPV04pCiAgICAgICAgZWxzZToKICAgICAgICAgICAgZGlmZXJlbmNpYSA9IE5vbmUKCiAgICAgICAgaWYgdGFyZ2V0LnVuZS5jb2RlIGluIHsiSU5WRVNUTUVOVCIsICJJTlZFU1RNRU5UUyIsICJJTlZFUlNJT05FUyJ9OgogICAgICAgICAgICBtZXRvZG8gPSAiU3VtYSBkZSBtb250b3MgZGVsIGFyY2hpdm8gZGUgY2xpZW50ZXMgbnVldm9zIGRlbCBtZXMiCiAgICAgICAgICAgIG9ic2VydmFjaW9uID0gKAogICAgICAgICAgICAgICAgIkVuIEludmVzdG1lbnQsIGVsIGluZ3Jlc28gZGVsIHNjb3JlIG1lbnN1YWwgc2UgY2FsY3VsYSBjb21vIGxhIHN1bWEgIgogICAgICAgICAgICAgICAgImRlIG1vbnRvcyBkZSB0b2RvcyBsb3MgcmVnaXN0cm9zIGRlbCBhcmNoaXZvIGRlIGNsaWVudGVzIGRlbCBtZXMuIgogICAgICAgICAgICApCiAgICAgICAgICAgIG9ic2VydmFjaW9uX2Jhc2UgPSBvYnNlcnZhY2lvbgogICAgICAgICAgICB0Y19sYWJlbCA9ICIiCiAgICAgICAgZWxzZToKICAgICAgICAgICAgbWV0b2RvID0gIkVzdGFkbyBkZSByZXN1bHRhZG9zIgogICAgICAgICAgICBvYnNlcnZhY2lvbiA9ICIiCiAgICAgICAgICAgIG9ic2VydmFjaW9uX2Jhc2UgPSAiIgogICAgICAgICAgICB0Y19sYWJlbCA9ICIiCiAgICAgICAgICAgIGlmIHJlc3VsdCBhbmQgcmVzdWx0LmNhbGN1bGF0aW9uX25vdGU6CiAgICAgICAgICAgICAgICBub3RlID0gcmVzdWx0LmNhbGN1bGF0aW9uX25vdGUuc3RyaXAoKQoKICAgICAgICAgICAgICAgIGJhc2Vfbm90ZSA9IG5vdGUKICAgICAgICAgICAgICAgIHRjX3RleHQgPSAiIgoKICAgICAgICAgICAgICAgIGlmICJbRlhfQVBQTElFRF0iIGluIG5vdGUgYW5kICJHVFEgYSBVU0Q6IiBpbiBub3RlOgogICAgICAgICAgICAgICAgICAgIGJhc2Vfbm90ZSA9IG5vdGUuc3BsaXQoIltGWF9BUFBMSUVEXSIpWzBdLnN0cmlwKCkKCiAgICAgICAgICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgICAgICAgICBmeF9wYXJ0ID0gbm90ZS5zcGxpdCgiLyIpWzFdLnNwbGl0KCI9IilbMF0uc3RyaXAoKQogICAgICAgICAgICAgICAgICAgICAgICBmeF92YWx1ZSA9IERlY2ltYWwoZnhfcGFydCkucXVhbnRpemUoRGVjaW1hbCgiMC4wMDEiKSwgcm91bmRpbmc9Uk9VTkRfRE9XTikKICAgICAgICAgICAgICAgICAgICAgICAgdGNfdGV4dCA9IGYiVEMge2Z4X3ZhbHVlfSIKICAgICAgICAgICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uOgogICAgICAgICAgICAgICAgICAgICAgICB0Y190ZXh0ID0gIiIKCiAgICAgICAgICAgICAgICBpZiBiYXNlX25vdGUgYW5kIHRjX3RleHQ6CiAgICAgICAgICAgICAgICAgICAgb2JzZXJ2YWNpb24gPSBmIntiYXNlX25vdGV9IHt0Y190ZXh0fSIKICAgICAgICAgICAgICAgIGVsaWYgYmFzZV9ub3RlOgogICAgICAgICAgICAgICAgICAgIG9ic2VydmFjaW9uID0gYmFzZV9ub3RlCiAgICAgICAgICAgICAgICBlbGlmIHRjX3RleHQ6CiAgICAgICAgICAgICAgICAgICAgb2JzZXJ2YWNpb24gPSB0Y190ZXh0CgogICAgICAgICAgICAgICAgb2JzZXJ2YWNpb25fYmFzZSA9IGJhc2Vfbm90ZQogICAgICAgICAgICAgICAgdGNfbGFiZWwgPSB0Y190ZXh0CgogICAgICAgICMgUHJlc2VudGFjacOzbjogVEMgZGVzZGUgY2FwdHVyYSBtYW51YWwgR1RR4oaSVVNEIHNpIG5vIHZpbm8gZW4gY2FsY3VsYXRpb25fbm90ZS4KICAgICAgICBpZiBub3QgdGNfbGFiZWwgYW5kIHJlc3VsdCBhbmQgZ2V0YXR0cihyZXN1bHQsICJleGNoYW5nZV9yYXRlX3VzZWQiLCBOb25lKToKICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgdGNfbGFiZWwgPSBmIlRDIHtEZWNpbWFsKHJlc3VsdC5leGNoYW5nZV9yYXRlX3VzZWQpLnF1YW50aXplKERlY2ltYWwoJzAuMDAxJyksIHJvdW5kaW5nPVJPVU5EX0RPV04pfSIKICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICAgICAgICAgIHRjX2xhYmVsID0gZiJUQyB7cmVzdWx0LmV4Y2hhbmdlX3JhdGVfdXNlZH0iCgogICAgICAgIGlmIG5vdCB0Y19sYWJlbCBhbmQgb2JzZXJ2YWNpb246CiAgICAgICAgICAgIG0gPSByZS5zZWFyY2gociJUQ1s9IF1ccyooWzAtOV0rKD86XC5bMC05XSspPykiLCBvYnNlcnZhY2lvbiwgZmxhZ3M9cmUuSUdOT1JFQ0FTRSkKICAgICAgICAgICAgaWYgbToKICAgICAgICAgICAgICAgIHRjX2xhYmVsID0gZiJUQyB7bS5ncm91cCgxKX0iCgogICAgICAgICMgRXZpdGFyIGR1cGxpY2FyIGVsIFRDIGVuIGVsIHRleHRvIGN1YW5kbyB5YSBoYXkgYmFkZ2UuCiAgICAgICAgZGlzcGxheV9iYXNlID0gb2JzZXJ2YWNpb25fYmFzZSBvciBvYnNlcnZhY2lvbiBvciAiIgogICAgICAgIGlmIHRjX2xhYmVsIGFuZCBkaXNwbGF5X2Jhc2U6CiAgICAgICAgICAgIGRpc3BsYXlfYmFzZSA9IHJlLnN1YigKICAgICAgICAgICAgICAgIHIiXHMqVENbPSBdXHMqWzAtOV0rKD86XC5bMC05XSspP1xzKiIsCiAgICAgICAgICAgICAgICAiICIsCiAgICAgICAgICAgICAgICBkaXNwbGF5X2Jhc2UsCiAgICAgICAgICAgICAgICBmbGFncz1yZS5JR05PUkVDQVNFLAogICAgICAgICAgICApLnN0cmlwKCkKCiAgICAgICAgc291cmNlX2d0cSA9IE5vbmUKICAgICAgICBpZiAoCiAgICAgICAgICAgIHJlc3VsdAogICAgICAgICAgICBhbmQgZ2V0YXR0cihyZXN1bHQsICJzb3VyY2VfY3VycmVuY3kiLCAiIikgPT0gIkdUUSIKICAgICAgICAgICAgYW5kIGdldGF0dHIocmVzdWx0LCAic291cmNlX3ZhbHVlIiwgTm9uZSkgaXMgbm90IE5vbmUKICAgICAgICApOgogICAgICAgICAgICBzb3VyY2VfZ3RxID0gcmVzdWx0LnNvdXJjZV92YWx1ZQoKICAgICAgICByb3dzLmFwcGVuZCh7CiAgICAgICAgICAgICJ0YXJnZXQiOiB0YXJnZXQsCiAgICAgICAgICAgICJyZXN1bHQiOiByZXN1bHQsCiAgICAgICAgICAgICJzY29yZWNhcmQiOiBzY29yZWNhcmQsCiAgICAgICAgICAgICJtZXRhIjogbWV0YSwKICAgICAgICAgICAgInJlYWwiOiByZWFsLAogICAgICAgICAgICAiZGlmZXJlbmNpYSI6IGRpZmVyZW5jaWEsCiAgICAgICAgICAgICJjdW1wbGUiOiByZXN1bHQuaXNfYWNoaWV2ZWQgaWYgcmVzdWx0IGVsc2UgRmFsc2UsCiAgICAgICAgICAgICJtZXRvZG8iOiBtZXRvZG8sCiAgICAgICAgICAgICJvYnNlcnZhY2lvbiI6IG9ic2VydmFjaW9uLAogICAgICAgICAgICAib2JzZXJ2YWNpb25fYmFzZSI6IGRpc3BsYXlfYmFzZSwKICAgICAgICAgICAgInRjX2xhYmVsIjogdGNfbGFiZWwsCiAgICAgICAgICAgICJzb3VyY2VfZ3RxIjogc291cmNlX2d0cSwKICAgICAgICAgICAgImlzX2luc3VyYW5jZSI6IHRhcmdldC51bmUuY29kZSA9PSAiSU5TVVJBTkNFIiwgICMgRmxhZyBwYXJhIGVsIHRlbXBsYXRlCiAgICAgICAgfSkKCiAgICByZXR1cm4gbWV0cmljLCByb3dzCgoKZGVmIGJ1aWxkX2luZ3Jlc29zX21hcmtkb3duKHJvd3MsIHJlcG9ydF9maWx0ZXIpOgogICAgZ2VuZXJhdGVkX2F0ID0gZGF0ZXRpbWUubm93KCkuc3RyZnRpbWUoIiVZLSVtLSVkICVIOiVNIikKCiAgICBzdGFydF95ZWFyID0gcmVwb3J0X2ZpbHRlclsic3RhcnRfeWVhciJdCiAgICBzdGFydF9tb250aCA9IHJlcG9ydF9maWx0ZXJbInN0YXJ0X21vbnRoIl0KICAgIG1vbnRoX2NvdW50ID0gcmVwb3J0X2ZpbHRlclsibW9udGhfY291bnQiXQogICAgcGVyaW9kcyA9IF9idWlsZF9wZXJpb2RfcmFuZ2Uoc3RhcnRfeWVhciwgc3RhcnRfbW9udGgsIG1vbnRoX2NvdW50KQogICAgZW5kX3llYXIsIGVuZF9tb250aCA9IHBlcmlvZHNbLTFdCgogICAgbGluZXMgPSBbCiAgICAgICAgIiMgUEdDIC0gSW5ncmVzb3MgdnMgbWV0YSBwb3IgVU5FIiwKICAgICAgICAiIiwKICAgICAgICBmIkdlbmVyYWRvOiB7Z2VuZXJhdGVkX2F0fSIsCiAgICAgICAgIiIsCiAgICAgICAgIiMjIEZpbHRyb3MiLAogICAgICAgIGYiLSBEZXNkZToge3N0YXJ0X3llYXJ9LXtzdGFydF9tb250aDowMmR9IiwKICAgICAgICBmIi0gSGFzdGE6IHtlbmRfeWVhcn0te2VuZF9tb250aDowMmR9IiwKICAgICAgICBmIi0gTWVzZXMgaW5jbHVpZG9zOiB7bW9udGhfY291bnR9IiwKICAgICAgICAiIiwKICAgICAgICAiIyMgRGF0b3MiLAogICAgICAgICIiLAogICAgICAgICJ8IFVORSB8IFBlcmlvZG8gfCBNZXRhIFVTRCB8IFJlYWwgVVNEIHwgRGlmLiBVU0QgfCBDdW1wbGUgfCBNw6l0b2RvIGRlIGPDoWxjdWxvIHwgT2JzZXJ2YWNpw7NuIHwiLAogICAgICAgICJ8IDotLS0gfCA6LS0tOiB8IDotLS06IHwgOi0tLTogfCA6LS0tOiB8IDotLS06IHwgOi0tLTogfCA6LS0tOiB8IiwKICAgIF0KCiAgICBpZiBub3Qgcm93czoKICAgICAgICBsaW5lcy5hcHBlbmQoInwgU2luIGRhdG9zIHwgLSB8IC0gfCAtIHwgLSB8IC0gfCAtIHwgLSB8IikKICAgIGVsc2U6CiAgICAgICAgZm9yIHJvdyBpbiByb3dzOgogICAgICAgICAgICBpZiByb3cuZ2V0KCJpc19zZXBhcmF0b3IiKToKICAgICAgICAgICAgICAgIGNvbnRpbnVlCgogICAgICAgICAgICB0YXJnZXQgPSByb3dbInRhcmdldCJdCiAgICAgICAgICAgIHBlcmlvZCA9IGYie3RhcmdldC55ZWFyfS17dGFyZ2V0Lm1vbnRoOjAyZH0iCiAgICAgICAgICAgIG1ldGEgPSByb3dbIm1ldGEiXQogICAgICAgICAgICByZWFsID0gcm93WyJyZWFsIl0KICAgICAgICAgICAgZGlmZXJlbmNpYSA9IHJvd1siZGlmZXJlbmNpYSJdCiAgICAgICAgICAgIAogICAgICAgICAgICAjIEluc3VyYW5jZSBjb24gMyBkZWNpbWFsZXMgZW4gTUQKICAgICAgICAgICAgaXNfaW5zdXJhbmNlID0gdGFyZ2V0LnVuZS5jb2RlID09ICJJTlNVUkFOQ0UiCiAgICAgICAgICAgIAogICAgICAgICAgICBpZiBpc19pbnN1cmFuY2U6CiAgICAgICAgICAgICAgICBtZXRhX3R4dCA9IGYie21ldGE6LjNmfSIgaWYgbWV0YSBpcyBub3QgTm9uZSBlbHNlICItIgogICAgICAgICAgICAgICAgcmVhbF90eHQgPSBmIntyZWFsOi4zZn0iIGlmIHJlYWwgaXMgbm90IE5vbmUgZWxzZSAiLSIKICAgICAgICAgICAgICAgIGRpZmVyZW5jaWFfdHh0ID0gZiJ7ZGlmZXJlbmNpYTouM2Z9IiBpZiBkaWZlcmVuY2lhIGlzIG5vdCBOb25lIGVsc2UgIi0iCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBtZXRhX3R4dCA9IGYie2ludChtZXRhKX0iIGlmIG1ldGEgaXMgbm90IE5vbmUgZWxzZSAiLSIKICAgICAgICAgICAgICAgIHJlYWxfdHh0ID0gZiJ7aW50KHJlYWwpfSIgaWYgcmVhbCBpcyBub3QgTm9uZSBlbHNlICItIgogICAgICAgICAgICAgICAgZGlmZXJlbmNpYV90eHQgPSBmIntpbnQoZGlmZXJlbmNpYSl9IiBpZiBkaWZlcmVuY2lhIGlzIG5vdCBOb25lIGVsc2UgIi0iCiAgICAgICAgICAgIAogICAgICAgICAgICBsaW5lcy5hcHBlbmQoCiAgICAgICAgICAgICAgICBmInwge3RhcmdldC51bmUubmFtZV9lcyBpZiBoYXNhdHRyKHRhcmdldC51bmUsICduYW1lX2VzJykgZWxzZSB0YXJnZXQudW5lLm5hbWVfZXN9IHwgIgogICAgICAgICAgICAgICAgZiJ7cGVyaW9kfSB8ICIKICAgICAgICAgICAgICAgIGYie21ldGFfdHh0fSB8ICIKICAgICAgICAgICAgICAgIGYie3JlYWxfdHh0fSB8ICIKICAgICAgICAgICAgICAgIGYie2RpZmVyZW5jaWFfdHh0fSB8ICIKICAgICAgICAgICAgICAgIGYieydTw60nIGlmIHJvd1snY3VtcGxlJ10gZWxzZSAnTm8nfSB8ICIKICAgICAgICAgICAgICAgIGYie3Jvd1snbWV0b2RvJ119IHwgIgogICAgICAgICAgICAgICAgZiJ7cm93WydvYnNlcnZhY2lvbiddIG9yICctJ30gfCIKICAgICAgICAgICAgKQoKICAgIGxpbmVzLmV4dGVuZChbCiAgICAgICAgIiIsCiAgICAgICAgIiMjIE5vdGEiLAogICAgICAgICJFc3RlIHJlcG9ydGUgbXVlc3RyYSBsYSBtZXRhIGRlIGluZ3Jlc29zLCBlbCB2YWxvciByZWFsIG9ic2VydmFkbyB5IGVsIG3DqXRvZG8gdXNhZG8gcGFyYSBleHBsaWNhciBlbCBwdW50YWplIG1lbnN1YWwuIiwKICAgICAgICAiSW5zdXJhbmNlIHNlIHByZXNlbnRhIHNpZW1wcmUgY29uIDMgZGVjaW1hbGVzLiIsCiAgICAgICAgIiIsCiAgICBdKQogICAgcmV0dXJuICJcbiIuam9pbihsaW5lcykKCgpAbG9naW5fcmVxdWlyZWQKZGVmIGluZ3Jlc29zX3JlcG9ydChyZXF1ZXN0KToKICAgIHJlcG9ydF9maWx0ZXIgPSBfZ2V0X3JlcG9ydF9maWx0ZXIocmVxdWVzdCkKICAgIHJlcG9ydF9zb3J0ID0gZ2V0X3JlcG9ydF9zb3J0KHJlcXVlc3QpCgogICAgcGVyaW9kcyA9IF9idWlsZF9wZXJpb2RfcmFuZ2UoCiAgICAgICAgcmVwb3J0X2ZpbHRlclsic3RhcnRfeWVhciJdLAogICAgICAgIHJlcG9ydF9maWx0ZXJbInN0YXJ0X21vbnRoIl0sCiAgICAgICAgcmVwb3J0X2ZpbHRlclsibW9udGhfY291bnQiXSwKICAgICkKCiAgICBtZXRyaWMsIHJvd3MgPSBfZ2V0X2luZ3Jlc29zX3Jvd3MocGVyaW9kcz1wZXJpb2RzKQogICAgcm93cyA9IHNvcnRfaW5ncmVzb3Nfcm93cyhyb3dzLCByZXBvcnRfc29ydCkKCiAgICBjb250ZXh0ID0gewogICAgICAgICJyb3dzIjogcm93cywKICAgICAgICAibWV0cmljIjogbWV0cmljLAogICAgICAgICJyZXBvcnRfZmlsdGVyIjogcmVwb3J0X2ZpbHRlciwKICAgICAgICAicmVwb3J0X3NvcnQiOiByZXBvcnRfc29ydCwKICAgICAgICAiYXZhaWxhYmxlX3BlcmlvZHMiOiBfZ2V0X2F2YWlsYWJsZV9wZXJpb2RzKCksCiAgICAgICAgIm1vbnRoX2NvdW50X29wdGlvbnMiOiBNT05USF9DT1VOVF9PUFRJT05TLAogICAgfQoKICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgInBnYy9pbmdyZXNvcy5odG1sIiwgY29udGV4dCkKCgpAbG9naW5fcmVxdWlyZWQKZGVmIGluZ3Jlc29zX2V4cG9ydF9tZChyZXF1ZXN0KToKICAgIHJlcG9ydF9maWx0ZXIgPSBfZ2V0X3JlcG9ydF9maWx0ZXIocmVxdWVzdCkKICAgIHJlcG9ydF9zb3J0ID0gZ2V0X3JlcG9ydF9zb3J0KHJlcXVlc3QpCgogICAgcGVyaW9kcyA9IF9idWlsZF9wZXJpb2RfcmFuZ2UoCiAgICAgICAgcmVwb3J0X2ZpbHRlclsic3RhcnRfeWVhciJdLAogICAgICAgIHJlcG9ydF9maWx0ZXJbInN0YXJ0X21vbnRoIl0sCiAgICAgICAgcmVwb3J0X2ZpbHRlclsibW9udGhfY291bnQiXSwKICAgICkKCiAgICBtZXRyaWMsIHJvd3MgPSBfZ2V0X2luZ3Jlc29zX3Jvd3MocGVyaW9kcz1wZXJpb2RzKQogICAgcm93cyA9IHNvcnRfaW5ncmVzb3Nfcm93cyhyb3dzLCByZXBvcnRfc29ydCkKCiAgICBjb250ZW50ID0gYnVpbGRfaW5ncmVzb3NfbWFya2Rvd24ocm93cywgcmVwb3J0X2ZpbHRlcikKCiAgICBnZW5lcmF0ZWRfc3VmZml4ID0gZGF0ZXRpbWUubm93KCkuc3RyZnRpbWUoIiVZJW0lZC0lSCVNIikKICAgIHN0YXJ0X3llYXIgPSByZXBvcnRfZmlsdGVyWyJzdGFydF95ZWFyIl0KICAgIHN0YXJ0X21vbnRoID0gcmVwb3J0X2ZpbHRlclsic3RhcnRfbW9udGgiXQogICAgbW9udGhfY291bnQgPSByZXBvcnRfZmlsdGVyWyJtb250aF9jb3VudCJdCgogICAgZmlsZW5hbWUgPSAoCiAgICAgICAgZiJwZ2MtaW5ncmVzb3MtdnMtbWV0YS0iCiAgICAgICAgZiJmeXtzdGFydF95ZWFyfS1te3N0YXJ0X21vbnRoOjAyZH0tbnttb250aF9jb3VudH0tIgogICAgICAgIGYie2dlbmVyYXRlZF9zdWZmaXh9Lm1kIgogICAgKQoKICAgIHJlc3BvbnNlID0gSHR0cFJlc3BvbnNlKAogICAgICAgIHNtYXJ0X3N0cihjb250ZW50KSwKICAgICAgICBjb250ZW50X3R5cGU9InRleHQvcGxhaW47IGNoYXJzZXQ9dXRmLTgiLAogICAgKQogICAgcmVzcG9uc2VbIkNvbnRlbnQtRGlzcG9zaXRpb24iXSA9IGYnYXR0YWNobWVudDsgZmlsZW5hbWU9IntmaWxlbmFtZX0iJwogICAgcmV0dXJuIHJlc3BvbnNlCgoKZGVmIHVzZXJfY2FuX3ZpZXdfdW5lX3N1bW1hcnkodXNlciwgdW5lKToKICAgIGlmIHVzZXIuaXNfc3VwZXJ1c2VyOgogICAgICAgIHJldHVybiBUcnVlCiAgICBwcm9maWxlID0gZ2V0YXR0cih1c2VyLCAicHJvZmlsZSIsIE5vbmUpICAjIHJlbGF0ZWRfbmFtZSByZWFsCiAgICBpZiBwcm9maWxlIGFuZCBwcm9maWxlLmRlZmF1bHRfYWxsX3VuZV9hY2Nlc3M6CiAgICAgICAgcmV0dXJuIFRydWUKICAgIHJldHVybiB1c2VyLnVuZV9wZXJtaXNzaW9ucy5maWx0ZXIodW5lPXVuZSwgY2FuX3ZpZXdfc3VtbWFyeT1UcnVlKS5leGlzdHMoKQoKCmRlZiB1c2VyX2Nhbl92aWV3X3VuZV9kZXRhaWwodXNlciwgdW5lKToKICAgIGlmIHVzZXIuaXNfc3VwZXJ1c2VyOgogICAgICAgIHJldHVybiBUcnVlCiAgICBwcm9maWxlID0gZ2V0YXR0cih1c2VyLCAicHJvZmlsZSIsIE5vbmUpCiAgICBpZiBwcm9maWxlIGFuZCBwcm9maWxlLmRlZmF1bHRfYWxsX3VuZV9hY2Nlc3M6CiAgICAgICAgIyBzaSBkZWNpZGVzIHF1ZSBlc3RlIGZsYWcgdGFtYmnDqW4gaW1wbGljYSB2ZXIgZGV0YWxsZQogICAgICAgIHJldHVybiBUcnVlCiAgICByZXR1cm4gdXNlci51bmVfcGVybWlzc2lvbnMuZmlsdGVyKHVuZT11bmUsIGNhbl92aWV3X2RldGFpbD1UcnVlKS5leGlzdHMoKQoKCmRlZiB1c2VyX2Nhbl92aWV3X2RldGFpbCh1c2VyLCB1bmUpOgogICAgaWYgdXNlci5pc19zdXBlcnVzZXI6CiAgICAgICAgcmV0dXJuIFRydWUKCiAgICBwcm9maWxlID0gZ2V0YXR0cih1c2VyLCAicHJvZmlsZSIsIE5vbmUpCiAgICBpZiBwcm9maWxlIGFuZCBnZXRhdHRyKHByb2ZpbGUsICJkZWZhdWx0X2FsbF91bmVfYWNjZXNzIiwgRmFsc2UpOgogICAgICAgIHJldHVybiBUcnVlCgogICAgcmV0dXJuIFVzZXJVTkVQZXJtaXNzaW9uLm9iamVjdHMuZmlsdGVyKAogICAgICAgIHVzZXI9dXNlciwKICAgICAgICB1bmU9dW5lLAogICAgICAgIGNhbl92aWV3X2RldGFpbD1UcnVlLAogICAgKS5leGlzdHMoKQoKCkBsb2dpbl9yZXF1aXJlZApkZWYgY2xpZW50ZXNfbnVldm9zX2RldGFpbChyZXF1ZXN0KToKCiAgICB1bmVfaWQgPSByZXF1ZXN0LkdFVC5nZXQoInVuZV9pZCIpCiAgICB5ZWFyX3JhdyA9IHJlcXVlc3QuR0VULmdldCgieWVhciIpCiAgICBtb250aF9yYXcgPSByZXF1ZXN0LkdFVC5nZXQoIm1vbnRoIikKICAgIAogICAgaWYgbm90IHVuZV9pZCBvciBub3QgeWVhcl9yYXcgb3Igbm90IG1vbnRoX3JhdzoKICAgICAgICByYWlzZSBIdHRwNDA0KCJGYWx0YW4gcGFyw6FtZXRyb3Mgb2JsaWdhdG9yaW9zOiB1bmVfaWQsIHllYXIsIG1vbnRoLiIpCiAgICAKICAgIHRyeToKICAgICAgICB1bmVfaWQgPSBpbnQodW5lX2lkKQogICAgICAgIHllYXIgPSBpbnQoeWVhcl9yYXcpCiAgICAgICAgbW9udGggPSBpbnQobW9udGhfcmF3KQogICAgZXhjZXB0IChUeXBlRXJyb3IsIFZhbHVlRXJyb3IpOgogICAgICAgIHJhaXNlIEh0dHA0MDQoIlBhcsOhbWV0cm9zIGludsOhbGlkb3M6IHVuZV9pZCwgeWVhciwgbW9udGguIikKCiAgICBpZiBtb250aCA8IDEgb3IgbW9udGggPiAxMjoKICAgICAgICByYWlzZSBIdHRwNDA0KCJNZXMgaW52w6FsaWRvLiIpCgogICAgdW5lID0gZ2V0X29iamVjdF9vcl80MDQoVU5FLCBwaz11bmVfaWQpCgogICAgaWYgbm90IHVzZXJfY2FuX3ZpZXdfZGV0YWlsKHJlcXVlc3QudXNlciwgdW5lKToKICAgICAgICByZXR1cm4gSHR0cFJlc3BvbnNlRm9yYmlkZGVuKCJObyB0aWVuZXMgcGVybWlzbyBwYXJhIHZlciBkZXRhbGxlIGRlIGVzdGEgVU5FLiIpCgogICAgcm93c19xdWVyeXNldCA9ICgKICAgICAgICBOZXdDbGllbnRJbXBvcnRSb3cub2JqZWN0cwogICAgICAgIC5zZWxlY3RfcmVsYXRlZCgiaGVhZGVyIiwgImN1cnJlbmN5IiwgInVuZSIpCiAgICAgICAgLmZpbHRlcih1bmU9dW5lKQogICAgICAgIC5maWx0ZXIoCiAgICAgICAgICAgIFEoaGVhZGVyX195ZWFyPXllYXIsIGhlYWRlcl9fbW9udGg9bW9udGgpIHwKICAgICAgICAgICAgUSh5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKQogICAgICAgICkKICAgICAgICAub3JkZXJfYnkoImNsaWVudF9uYW1lIiwgIm9wZXJhdGlvbl9jb2RlIiwgImlkIikKICAgICkKCiAgICBkZXRhaWxfcm93cyA9IFtdCiAgICBmb3Igcm93IGluIHJvd3NfcXVlcnlzZXQ6CiAgICAgICAgZGV0YWlsX3Jvd3MuYXBwZW5kKHsKICAgICAgICAgICAgImlkIjogcm93LmlkLAogICAgICAgICAgICAiY2xpZW50X25hbWUiOiByb3cuY2xpZW50X25hbWUgb3IgIiIsCiAgICAgICAgICAgICJuaXQiOiByb3cubml0IG9yICIiLAogICAgICAgICAgICAib3BlcmF0aW9uX2NvZGUiOiByb3cub3BlcmF0aW9uX2NvZGUgb3IgIiIsCiAgICAgICAgICAgICJjdXJyZW5jeV9jb2RlIjogcm93LmN1cnJlbmN5LmNvZGUgaWYgcm93LmN1cnJlbmN5IGVsc2UgIiIsCiAgICAgICAgICAgICJhbW91bnQiOiByb3cuYW1vdW50LAogICAgICAgICAgICAicHJldmlvdXNfY29udHJhY3RzIjogcm93LnByZXZpb3VzX2NvbnRyYWN0cywKICAgICAgICAgICAgImNvdW50c19hc19uZXciOiByb3cuY291bnRzX2FzX25ldywKICAgICAgICAgICAgInJhd191bmVfdmFsdWUiOiByb3cucmF3X3VuZV92YWx1ZSBvciAiIiwKICAgICAgICAgICAgIm9ic2VydmF0aW9ucyI6IHJvdy5vYnNlcnZhdGlvbnMgb3IgIiIsCiAgICAgICAgICAgICJzb3VyY2Vfcm93X251bWJlciI6IHJvdy5zb3VyY2Vfcm93X251bWJlciwKICAgICAgICAgICAgImhlYWRlcl95ZWFyIjogZ2V0YXR0cihyb3cuaGVhZGVyLCAieWVhciIsIE5vbmUpLAogICAgICAgICAgICAiaGVhZGVyX21vbnRoIjogZ2V0YXR0cihyb3cuaGVhZGVyLCAibW9udGgiLCBOb25lKSwKICAgICAgICAgICAgInJvd195ZWFyIjogZ2V0YXR0cihyb3csICJ5ZWFyIiwgTm9uZSksCiAgICAgICAgICAgICJyb3dfbW9udGgiOiBnZXRhdHRyKHJvdywgIm1vbnRoIiwgTm9uZSksCiAgICAgICAgfSkKCiAgICBmeF9tYXAgPSB7CiAgICAgIChpdGVtLnllYXIsIGl0ZW0ubW9udGgpOiBpdGVtLnVzZF90b19ndHEKICAgICAgZm9yIGl0ZW0gaW4gTW9udGhseUV4Y2hhbmdlUmF0ZS5vYmplY3RzLmFsbCgpCiAgICB9CgogICAgaW52ZXN0bWVudF9pbmdyZXNvc190b3RhbCA9IERlY2ltYWwoIjAiKQogICAgZm9yIHJvdyBpbiByb3dzX3F1ZXJ5c2V0OgogICAgICAgIGludmVzdG1lbnRfaW5ncmVzb3NfdG90YWwgKz0gX2NvbnZlcnRfcm93X2Ftb3VudF90b191c2Qocm93LCBmeF9tYXApCiAgCiAgICBjb250ZXh0ID0gewogICAgICAgICJ1bmUiOiB1bmUsCiAgICAgICAgInllYXIiOiB5ZWFyLAogICAgICAgICJtb250aCI6IG1vbnRoLAogICAgICAgICJyb3dzIjogZGV0YWlsX3Jvd3MsCiAgICAgICAgInJvd19jb3VudCI6IGxlbihkZXRhaWxfcm93cyksCiAgICAgICAgImludmVzdG1lbnRfaW5ncmVzb3NfdG90YWwiOiBpbnZlc3RtZW50X2luZ3Jlc29zX3RvdGFsLAogICAgfQoKICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgInBnYy9jbGllbnRlc19udWV2b3NfZGV0YWlsLmh0bWwiLCBjb250ZXh0KQoKCkBsb2dpbl9yZXF1aXJlZApkZWYgdmVudGFfY3J1emFkYV9kZXRhaWwocmVxdWVzdCk6CiAgICB5ZWFyID0gcmVxdWVzdC5HRVQuZ2V0KCJ5ZWFyIikKICAgIG1vbnRoID0gcmVxdWVzdC5HRVQuZ2V0KCJtb250aCIpCiAgICB1bmUgPSByZXF1ZXN0LkdFVC5nZXQoInVuZSIpCgogICAgcm93cyA9IENyb3NzU2FsZUltcG9ydFJvdy5vYmplY3RzLnNlbGVjdF9yZWxhdGVkKAogICAgICAgICJ1bmVfb3JpZ2luIiwKICAgICAgICAidW5lX2Rlc3RpbmF0aW9uIiwKICAgICAgICAiY3VycmVuY3kiLAogICAgKS5hbGwoKQoKICAgIGlmIHllYXI6CiAgICAgICAgcm93cyA9IHJvd3MuZmlsdGVyKHllYXI9eWVhcikKICAgIGlmIG1vbnRoOgogICAgICAgIHJvd3MgPSByb3dzLmZpbHRlcihtb250aD1tb250aCkKICAgIGlmIHVuZToKICAgICAgICByb3dzID0gcm93cy5maWx0ZXIodW5lX29yaWdpbl9fY29kZT11bmUpCgogICAgcm93cyA9IHJvd3Mub3JkZXJfYnkoCiAgICAgICAgInllYXIiLAogICAgICAgICJtb250aCIsCiAgICAgICAgInVuZV9vcmlnaW5fX3NvcnRfb3JkZXIiLAogICAgICAgICJ1bmVfZGVzdGluYXRpb25fX3NvcnRfb3JkZXIiLAogICAgICAgICJjbGllbnRfbmFtZSIsCiAgICAgICAgIm9wZXJhdGlvbl9jb2RlIiwKICAgICkKCiAgICBhdmFpbGFibGVfeWVhcnMgPSAoCiAgICAgICAgQ3Jvc3NTYWxlSW1wb3J0Um93Lm9iamVjdHMub3JkZXJfYnkoIi15ZWFyIikKICAgICAgICAudmFsdWVzX2xpc3QoInllYXIiLCBmbGF0PVRydWUpCiAgICAgICAgLmRpc3RpbmN0KCkKICAgICkKICAgIHVuZXMgPSBVTkUub2JqZWN0cy5vcmRlcl9ieSgic29ydF9vcmRlciIpCgogICAgY29udGV4dCA9IHsKICAgICAgICAicm93cyI6IHJvd3MsCiAgICAgICAgImF2YWlsYWJsZV95ZWFycyI6IGF2YWlsYWJsZV95ZWFycywKICAgICAgICAibW9udGhzIjogcmFuZ2UoMSwgMTMpLAogICAgICAgICJ1bmVzIjogdW5lcywKICAgICAgICAic2VsZWN0ZWRfeWVhciI6IHllYXIgb3IgIiIsCiAgICAgICAgInNlbGVjdGVkX21vbnRoIjogbW9udGggb3IgIiIsCiAgICAgICAgInNlbGVjdGVkX3VuZSI6IHVuZSBvciAiIiwKICAgIH0KICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgInBnYy92ZW50YV9jcnV6YWRhX2RldGFpbC5odG1sIiwgY29udGV4dCkKCgo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgo/__init__.py
PATH_JSON="pgo/__init__.py"
FILENAME=__init__.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=0
SIZE_BYTES_UTF8=0
CONTENT_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ENDS_WITH_NEWLINE=FALSE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN

CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgo/admin.py
PATH_JSON="pgo/admin.py"
FILENAME=admin.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=49
SIZE_BYTES_UTF8=1339
CONTENT_SHA256=7a6fed77bc26bf357e60fcdc639441f1ddb87e209e333f8e81ff4add2c6009fb
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.contrib import admin

from .models import PgoResultadoPeriodo, Ticket, TicketEvento


class TicketEventoInline(admin.TabularInline):
    model = TicketEvento
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "titulo",
        "estado",
        "prioridad",
        "unidad_negocio",
        "asignado_a",
        "fecha_apertura",
    )
    list_filter = ("estado", "prioridad", "unidad_negocio")
    search_fields = ("codigo", "titulo", "descripcion")
    ordering = ("-fecha_apertura",)
    inlines = [TicketEventoInline]


@admin.register(TicketEvento)
class TicketEventoAdmin(admin.ModelAdmin):
    list_display = ("ticket", "tipo", "fecha", "usuario")
    list_filter = ("tipo", "fecha")
    search_fields = ("ticket__codigo", "descripcion")
    ordering = ("-fecha",)


@admin.register(PgoResultadoPeriodo)
class PgoResultadoPeriodoAdmin(admin.ModelAdmin):
    list_display = (
        "periodo",
        "unidad_negocio",
        "tickets_cerrados",
        "tickets_abiertos",
        "tiempo_promedio_horas",
        "cumplimiento_sla_pct",
    )
    list_filter = ("periodo", "unidad_negocio")
    search_fields = ("periodo", "unidad_negocio__code", "unidad_negocio__nombre")
    ordering = ("-periodo",)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.contrib import admin
00002|
00003|from .models import PgoResultadoPeriodo, Ticket, TicketEvento
00004|
00005|
00006|class TicketEventoInline(admin.TabularInline):
00007|    model = TicketEvento
00008|    extra = 0
00009|    readonly_fields = ("created_at",)
00010|
00011|
00012|@admin.register(Ticket)
00013|class TicketAdmin(admin.ModelAdmin):
00014|    list_display = (
00015|        "codigo",
00016|        "titulo",
00017|        "estado",
00018|        "prioridad",
00019|        "unidad_negocio",
00020|        "asignado_a",
00021|        "fecha_apertura",
00022|    )
00023|    list_filter = ("estado", "prioridad", "unidad_negocio")
00024|    search_fields = ("codigo", "titulo", "descripcion")
00025|    ordering = ("-fecha_apertura",)
00026|    inlines = [TicketEventoInline]
00027|
00028|
00029|@admin.register(TicketEvento)
00030|class TicketEventoAdmin(admin.ModelAdmin):
00031|    list_display = ("ticket", "tipo", "fecha", "usuario")
00032|    list_filter = ("tipo", "fecha")
00033|    search_fields = ("ticket__codigo", "descripcion")
00034|    ordering = ("-fecha",)
00035|
00036|
00037|@admin.register(PgoResultadoPeriodo)
00038|class PgoResultadoPeriodoAdmin(admin.ModelAdmin):
00039|    list_display = (
00040|        "periodo",
00041|        "unidad_negocio",
00042|        "tickets_cerrados",
00043|        "tickets_abiertos",
00044|        "tiempo_promedio_horas",
00045|        "cumplimiento_sla_pct",
00046|    )
00047|    list_filter = ("periodo", "unidad_negocio")
00048|    search_fields = ("periodo", "unidad_negocio__code", "unidad_negocio__nombre")
00049|    ordering = ("-periodo",)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgYWRtaW4KCmZyb20gLm1vZGVscyBpbXBvcnQgUGdvUmVzdWx0YWRvUGVyaW9kbywgVGlja2V0LCBUaWNrZXRFdmVudG8KCgpjbGFzcyBUaWNrZXRFdmVudG9JbmxpbmUoYWRtaW4uVGFidWxhcklubGluZSk6CiAgICBtb2RlbCA9IFRpY2tldEV2ZW50bwogICAgZXh0cmEgPSAwCiAgICByZWFkb25seV9maWVsZHMgPSAoImNyZWF0ZWRfYXQiLCkKCgpAYWRtaW4ucmVnaXN0ZXIoVGlja2V0KQpjbGFzcyBUaWNrZXRBZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgKICAgICAgICAiY29kaWdvIiwKICAgICAgICAidGl0dWxvIiwKICAgICAgICAiZXN0YWRvIiwKICAgICAgICAicHJpb3JpZGFkIiwKICAgICAgICAidW5pZGFkX25lZ29jaW8iLAogICAgICAgICJhc2lnbmFkb19hIiwKICAgICAgICAiZmVjaGFfYXBlcnR1cmEiLAogICAgKQogICAgbGlzdF9maWx0ZXIgPSAoImVzdGFkbyIsICJwcmlvcmlkYWQiLCAidW5pZGFkX25lZ29jaW8iKQogICAgc2VhcmNoX2ZpZWxkcyA9ICgiY29kaWdvIiwgInRpdHVsbyIsICJkZXNjcmlwY2lvbiIpCiAgICBvcmRlcmluZyA9ICgiLWZlY2hhX2FwZXJ0dXJhIiwpCiAgICBpbmxpbmVzID0gW1RpY2tldEV2ZW50b0lubGluZV0KCgpAYWRtaW4ucmVnaXN0ZXIoVGlja2V0RXZlbnRvKQpjbGFzcyBUaWNrZXRFdmVudG9BZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgidGlja2V0IiwgInRpcG8iLCAiZmVjaGEiLCAidXN1YXJpbyIpCiAgICBsaXN0X2ZpbHRlciA9ICgidGlwbyIsICJmZWNoYSIpCiAgICBzZWFyY2hfZmllbGRzID0gKCJ0aWNrZXRfX2NvZGlnbyIsICJkZXNjcmlwY2lvbiIpCiAgICBvcmRlcmluZyA9ICgiLWZlY2hhIiwpCgoKQGFkbWluLnJlZ2lzdGVyKFBnb1Jlc3VsdGFkb1BlcmlvZG8pCmNsYXNzIFBnb1Jlc3VsdGFkb1BlcmlvZG9BZG1pbihhZG1pbi5Nb2RlbEFkbWluKToKICAgIGxpc3RfZGlzcGxheSA9ICgKICAgICAgICAicGVyaW9kbyIsCiAgICAgICAgInVuaWRhZF9uZWdvY2lvIiwKICAgICAgICAidGlja2V0c19jZXJyYWRvcyIsCiAgICAgICAgInRpY2tldHNfYWJpZXJ0b3MiLAogICAgICAgICJ0aWVtcG9fcHJvbWVkaW9faG9yYXMiLAogICAgICAgICJjdW1wbGltaWVudG9fc2xhX3BjdCIsCiAgICApCiAgICBsaXN0X2ZpbHRlciA9ICgicGVyaW9kbyIsICJ1bmlkYWRfbmVnb2NpbyIpCiAgICBzZWFyY2hfZmllbGRzID0gKCJwZXJpb2RvIiwgInVuaWRhZF9uZWdvY2lvX19jb2RlIiwgInVuaWRhZF9uZWdvY2lvX19ub21icmUiKQogICAgb3JkZXJpbmcgPSAoIi1wZXJpb2RvIiwpCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgo/apps.py
PATH_JSON="pgo/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=6
SIZE_BYTES_UTF8=138
CONTENT_SHA256=f2f5e42f9c9a92c1a75bbcd12d87569bc9ecdbeb861740d5177f9b21289fbaad
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.apps import AppConfig


class PgoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pgo'

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class PgoConfig(AppConfig):
00005|    default_auto_field = 'django.db.models.BigAutoField'
00006|    name = 'pgo'

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgUGdvQ29uZmlnKEFwcENvbmZpZyk6CiAgICBkZWZhdWx0X2F1dG9fZmllbGQgPSAnZGphbmdvLmRiLm1vZGVscy5CaWdBdXRvRmllbGQnCiAgICBuYW1lID0gJ3BnbycK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgo/forms.py
PATH_JSON="pgo/forms.py"
FILENAME=forms.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=5
SIZE_BYTES_UTF8=119
CONTENT_SHA256=c1b64b87ac9047389b8d52220cbf10f9c3457839c8b5a3c7c5fb2de19f5460dc
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django import forms


class ImportFileForm(forms.Form):
    archivo = forms.FileField(label="Archivo CSV o XLSX")

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django import forms
00002|
00003|
00004|class ImportFileForm(forms.Form):
00005|    archivo = forms.FileField(label="Archivo CSV o XLSX")

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28gaW1wb3J0IGZvcm1zCgoKY2xhc3MgSW1wb3J0RmlsZUZvcm0oZm9ybXMuRm9ybSk6CiAgICBhcmNoaXZvID0gZm9ybXMuRmlsZUZpZWxkKGxhYmVsPSJBcmNoaXZvIENTViBvIFhMU1giKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgo/models.py
PATH_JSON="pgo/models.py"
FILENAME=models.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=124
SIZE_BYTES_UTF8=4033
CONTENT_SHA256=3c150241daa50963707e7a1485be7ba93b985103625336daf0998a698ec9a10f
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.conf import settings
from django.db import models

from core.models import TimeStampedModel
from core.wcg_models import Entidad, UnidadNegocio


class Ticket(TimeStampedModel):
    """
    Ticket operativo PGO.
    Clave natural importación: `codigo` (ID ticket / folio).
    """
    ESTADO_ABIERTO = "ABIERTO"
    ESTADO_EN_PROCESO = "EN_PROCESO"
    ESTADO_CERRADO = "CERRADO"
    ESTADO_CHOICES = [
        (ESTADO_ABIERTO, "Abierto"),
        (ESTADO_EN_PROCESO, "En proceso"),
        (ESTADO_CERRADO, "Cerrado"),
    ]

    PRIORIDAD_BAJA = "BAJA"
    PRIORIDAD_MEDIA = "MEDIA"
    PRIORIDAD_ALTA = "ALTA"
    PRIORIDAD_CHOICES = [
        (PRIORIDAD_BAJA, "Baja"),
        (PRIORIDAD_MEDIA, "Media"),
        (PRIORIDAD_ALTA, "Alta"),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    entidad = models.ForeignKey(
        Entidad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )
    unidad_negocio = models.ForeignKey(
        UnidadNegocio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_ABIERTO)
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default=PRIORIDAD_MEDIA)
    asignado_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pgo_tickets",
    )
    fecha_apertura = models.DateTimeField()
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    sla_horas = models.PositiveIntegerField(default=48)

    class Meta:
        ordering = ["-fecha_apertura"]
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"{self.codigo} — {self.titulo}"


class TicketEvento(TimeStampedModel):
    TIPO_COMENTARIO = "COMENTARIO"
    TIPO_CAMBIO_ESTADO = "CAMBIO_ESTADO"
    TIPO_ASIGNACION = "ASIGNACION"
    TIPO_CHOICES = [
        (TIPO_COMENTARIO, "Comentario"),
        (TIPO_CAMBIO_ESTADO, "Cambio de estado"),
        (TIPO_ASIGNACION, "Asignación"),
    ]

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="eventos")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_COMENTARIO)
    descripcion = models.TextField()
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pgo_ticket_eventos",
    )
    fecha = models.DateTimeField()

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Evento de ticket"
        verbose_name_plural = "Eventos de ticket"

    def __str__(self):
        return f"{self.ticket.codigo} — {self.tipo}"


class PgoResultadoPeriodo(TimeStampedModel):
    """
    Agregado mensual por unidad. Clave natural: (`periodo` YYYY-MM, `unidad_negocio`).
    Calculado desde tickets vía `pgo.periodo.recalculate_pgo_periodos`.
    """
    periodo = models.CharField(max_length=7, help_text="YYYY-MM")
    unidad_negocio = models.ForeignKey(
        UnidadNegocio,
        on_delete=models.CASCADE,
        related_name="resultados_pgo",
    )
    tickets_cerrados = models.PositiveIntegerField(default=0)
    tickets_abiertos = models.PositiveIntegerField(default=0)
    tiempo_promedio_horas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cumplimiento_sla_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        unique_together = ("periodo", "unidad_negocio")
        ordering = ["-periodo", "unidad_negocio__nombre"]
        verbose_name = "Resultado PGO por período"
        verbose_name_plural = "Resultados PGO por período"

    def __str__(self):
        return f"{self.periodo} — {self.unidad_negocio.code}"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.conf import settings
00002|from django.db import models
00003|
00004|from core.models import TimeStampedModel
00005|from core.wcg_models import Entidad, UnidadNegocio
00006|
00007|
00008|class Ticket(TimeStampedModel):
00009|    """
00010|    Ticket operativo PGO.
00011|    Clave natural importación: `codigo` (ID ticket / folio).
00012|    """
00013|    ESTADO_ABIERTO = "ABIERTO"
00014|    ESTADO_EN_PROCESO = "EN_PROCESO"
00015|    ESTADO_CERRADO = "CERRADO"
00016|    ESTADO_CHOICES = [
00017|        (ESTADO_ABIERTO, "Abierto"),
00018|        (ESTADO_EN_PROCESO, "En proceso"),
00019|        (ESTADO_CERRADO, "Cerrado"),
00020|    ]
00021|
00022|    PRIORIDAD_BAJA = "BAJA"
00023|    PRIORIDAD_MEDIA = "MEDIA"
00024|    PRIORIDAD_ALTA = "ALTA"
00025|    PRIORIDAD_CHOICES = [
00026|        (PRIORIDAD_BAJA, "Baja"),
00027|        (PRIORIDAD_MEDIA, "Media"),
00028|        (PRIORIDAD_ALTA, "Alta"),
00029|    ]
00030|
00031|    codigo = models.CharField(max_length=50, unique=True)
00032|    titulo = models.CharField(max_length=200)
00033|    descripcion = models.TextField(blank=True)
00034|    entidad = models.ForeignKey(
00035|        Entidad,
00036|        on_delete=models.SET_NULL,
00037|        null=True,
00038|        blank=True,
00039|        related_name="tickets",
00040|    )
00041|    unidad_negocio = models.ForeignKey(
00042|        UnidadNegocio,
00043|        on_delete=models.SET_NULL,
00044|        null=True,
00045|        blank=True,
00046|        related_name="tickets",
00047|    )
00048|    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_ABIERTO)
00049|    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default=PRIORIDAD_MEDIA)
00050|    asignado_a = models.ForeignKey(
00051|        settings.AUTH_USER_MODEL,
00052|        on_delete=models.SET_NULL,
00053|        null=True,
00054|        blank=True,
00055|        related_name="pgo_tickets",
00056|    )
00057|    fecha_apertura = models.DateTimeField()
00058|    fecha_cierre = models.DateTimeField(null=True, blank=True)
00059|    sla_horas = models.PositiveIntegerField(default=48)
00060|
00061|    class Meta:
00062|        ordering = ["-fecha_apertura"]
00063|        verbose_name = "Ticket"
00064|        verbose_name_plural = "Tickets"
00065|
00066|    def __str__(self):
00067|        return f"{self.codigo} — {self.titulo}"
00068|
00069|
00070|class TicketEvento(TimeStampedModel):
00071|    TIPO_COMENTARIO = "COMENTARIO"
00072|    TIPO_CAMBIO_ESTADO = "CAMBIO_ESTADO"
00073|    TIPO_ASIGNACION = "ASIGNACION"
00074|    TIPO_CHOICES = [
00075|        (TIPO_COMENTARIO, "Comentario"),
00076|        (TIPO_CAMBIO_ESTADO, "Cambio de estado"),
00077|        (TIPO_ASIGNACION, "Asignación"),
00078|    ]
00079|
00080|    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="eventos")
00081|    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_COMENTARIO)
00082|    descripcion = models.TextField()
00083|    usuario = models.ForeignKey(
00084|        settings.AUTH_USER_MODEL,
00085|        on_delete=models.SET_NULL,
00086|        null=True,
00087|        blank=True,
00088|        related_name="pgo_ticket_eventos",
00089|    )
00090|    fecha = models.DateTimeField()
00091|
00092|    class Meta:
00093|        ordering = ["-fecha"]
00094|        verbose_name = "Evento de ticket"
00095|        verbose_name_plural = "Eventos de ticket"
00096|
00097|    def __str__(self):
00098|        return f"{self.ticket.codigo} — {self.tipo}"
00099|
00100|
00101|class PgoResultadoPeriodo(TimeStampedModel):
00102|    """
00103|    Agregado mensual por unidad. Clave natural: (`periodo` YYYY-MM, `unidad_negocio`).
00104|    Calculado desde tickets vía `pgo.periodo.recalculate_pgo_periodos`.
00105|    """
00106|    periodo = models.CharField(max_length=7, help_text="YYYY-MM")
00107|    unidad_negocio = models.ForeignKey(
00108|        UnidadNegocio,
00109|        on_delete=models.CASCADE,
00110|        related_name="resultados_pgo",
00111|    )
00112|    tickets_cerrados = models.PositiveIntegerField(default=0)
00113|    tickets_abiertos = models.PositiveIntegerField(default=0)
00114|    tiempo_promedio_horas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
00115|    cumplimiento_sla_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
00116|
00117|    class Meta:
00118|        unique_together = ("periodo", "unidad_negocio")
00119|        ordering = ["-periodo", "unidad_negocio__nombre"]
00120|        verbose_name = "Resultado PGO por período"
00121|        verbose_name_plural = "Resultados PGO por período"
00122|
00123|    def __str__(self):
00124|        return f"{self.periodo} — {self.unidad_negocio.code}"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uY29uZiBpbXBvcnQgc2V0dGluZ3MKZnJvbSBkamFuZ28uZGIgaW1wb3J0IG1vZGVscwoKZnJvbSBjb3JlLm1vZGVscyBpbXBvcnQgVGltZVN0YW1wZWRNb2RlbApmcm9tIGNvcmUud2NnX21vZGVscyBpbXBvcnQgRW50aWRhZCwgVW5pZGFkTmVnb2NpbwoKCmNsYXNzIFRpY2tldChUaW1lU3RhbXBlZE1vZGVsKToKICAgICIiIgogICAgVGlja2V0IG9wZXJhdGl2byBQR08uCiAgICBDbGF2ZSBuYXR1cmFsIGltcG9ydGFjacOzbjogYGNvZGlnb2AgKElEIHRpY2tldCAvIGZvbGlvKS4KICAgICIiIgogICAgRVNUQURPX0FCSUVSVE8gPSAiQUJJRVJUTyIKICAgIEVTVEFET19FTl9QUk9DRVNPID0gIkVOX1BST0NFU08iCiAgICBFU1RBRE9fQ0VSUkFETyA9ICJDRVJSQURPIgogICAgRVNUQURPX0NIT0lDRVMgPSBbCiAgICAgICAgKEVTVEFET19BQklFUlRPLCAiQWJpZXJ0byIpLAogICAgICAgIChFU1RBRE9fRU5fUFJPQ0VTTywgIkVuIHByb2Nlc28iKSwKICAgICAgICAoRVNUQURPX0NFUlJBRE8sICJDZXJyYWRvIiksCiAgICBdCgogICAgUFJJT1JJREFEX0JBSkEgPSAiQkFKQSIKICAgIFBSSU9SSURBRF9NRURJQSA9ICJNRURJQSIKICAgIFBSSU9SSURBRF9BTFRBID0gIkFMVEEiCiAgICBQUklPUklEQURfQ0hPSUNFUyA9IFsKICAgICAgICAoUFJJT1JJREFEX0JBSkEsICJCYWphIiksCiAgICAgICAgKFBSSU9SSURBRF9NRURJQSwgIk1lZGlhIiksCiAgICAgICAgKFBSSU9SSURBRF9BTFRBLCAiQWx0YSIpLAogICAgXQoKICAgIGNvZGlnbyA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD01MCwgdW5pcXVlPVRydWUpCiAgICB0aXR1bG8gPSBtb2RlbHMuQ2hhckZpZWxkKG1heF9sZW5ndGg9MjAwKQogICAgZGVzY3JpcGNpb24gPSBtb2RlbHMuVGV4dEZpZWxkKGJsYW5rPVRydWUpCiAgICBlbnRpZGFkID0gbW9kZWxzLkZvcmVpZ25LZXkoCiAgICAgICAgRW50aWRhZCwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0idGlja2V0cyIsCiAgICApCiAgICB1bmlkYWRfbmVnb2NpbyA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIFVuaWRhZE5lZ29jaW8sCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5TRVRfTlVMTCwKICAgICAgICBudWxsPVRydWUsCiAgICAgICAgYmxhbms9VHJ1ZSwKICAgICAgICByZWxhdGVkX25hbWU9InRpY2tldHMiLAogICAgKQogICAgZXN0YWRvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTIwLCBjaG9pY2VzPUVTVEFET19DSE9JQ0VTLCBkZWZhdWx0PUVTVEFET19BQklFUlRPKQogICAgcHJpb3JpZGFkID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTIwLCBjaG9pY2VzPVBSSU9SSURBRF9DSE9JQ0VTLCBkZWZhdWx0PVBSSU9SSURBRF9NRURJQSkKICAgIGFzaWduYWRvX2EgPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICBzZXR0aW5ncy5BVVRIX1VTRVJfTU9ERUwsCiAgICAgICAgb25fZGVsZXRlPW1vZGVscy5TRVRfTlVMTCwKICAgICAgICBudWxsPVRydWUsCiAgICAgICAgYmxhbms9VHJ1ZSwKICAgICAgICByZWxhdGVkX25hbWU9InBnb190aWNrZXRzIiwKICAgICkKICAgIGZlY2hhX2FwZXJ0dXJhID0gbW9kZWxzLkRhdGVUaW1lRmllbGQoKQogICAgZmVjaGFfY2llcnJlID0gbW9kZWxzLkRhdGVUaW1lRmllbGQobnVsbD1UcnVlLCBibGFuaz1UcnVlKQogICAgc2xhX2hvcmFzID0gbW9kZWxzLlBvc2l0aXZlSW50ZWdlckZpZWxkKGRlZmF1bHQ9NDgpCgogICAgY2xhc3MgTWV0YToKICAgICAgICBvcmRlcmluZyA9IFsiLWZlY2hhX2FwZXJ0dXJhIl0KICAgICAgICB2ZXJib3NlX25hbWUgPSAiVGlja2V0IgogICAgICAgIHZlcmJvc2VfbmFtZV9wbHVyYWwgPSAiVGlja2V0cyIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi5jb2RpZ299IOKAlCB7c2VsZi50aXR1bG99IgoKCmNsYXNzIFRpY2tldEV2ZW50byhUaW1lU3RhbXBlZE1vZGVsKToKICAgIFRJUE9fQ09NRU5UQVJJTyA9ICJDT01FTlRBUklPIgogICAgVElQT19DQU1CSU9fRVNUQURPID0gIkNBTUJJT19FU1RBRE8iCiAgICBUSVBPX0FTSUdOQUNJT04gPSAiQVNJR05BQ0lPTiIKICAgIFRJUE9fQ0hPSUNFUyA9IFsKICAgICAgICAoVElQT19DT01FTlRBUklPLCAiQ29tZW50YXJpbyIpLAogICAgICAgIChUSVBPX0NBTUJJT19FU1RBRE8sICJDYW1iaW8gZGUgZXN0YWRvIiksCiAgICAgICAgKFRJUE9fQVNJR05BQ0lPTiwgIkFzaWduYWNpw7NuIiksCiAgICBdCgogICAgdGlja2V0ID0gbW9kZWxzLkZvcmVpZ25LZXkoVGlja2V0LCBvbl9kZWxldGU9bW9kZWxzLkNBU0NBREUsIHJlbGF0ZWRfbmFtZT0iZXZlbnRvcyIpCiAgICB0aXBvID0gbW9kZWxzLkNoYXJGaWVsZChtYXhfbGVuZ3RoPTIwLCBjaG9pY2VzPVRJUE9fQ0hPSUNFUywgZGVmYXVsdD1USVBPX0NPTUVOVEFSSU8pCiAgICBkZXNjcmlwY2lvbiA9IG1vZGVscy5UZXh0RmllbGQoKQogICAgdXN1YXJpbyA9IG1vZGVscy5Gb3JlaWduS2V5KAogICAgICAgIHNldHRpbmdzLkFVVEhfVVNFUl9NT0RFTCwKICAgICAgICBvbl9kZWxldGU9bW9kZWxzLlNFVF9OVUxMLAogICAgICAgIG51bGw9VHJ1ZSwKICAgICAgICBibGFuaz1UcnVlLAogICAgICAgIHJlbGF0ZWRfbmFtZT0icGdvX3RpY2tldF9ldmVudG9zIiwKICAgICkKICAgIGZlY2hhID0gbW9kZWxzLkRhdGVUaW1lRmllbGQoKQoKICAgIGNsYXNzIE1ldGE6CiAgICAgICAgb3JkZXJpbmcgPSBbIi1mZWNoYSJdCiAgICAgICAgdmVyYm9zZV9uYW1lID0gIkV2ZW50byBkZSB0aWNrZXQiCiAgICAgICAgdmVyYm9zZV9uYW1lX3BsdXJhbCA9ICJFdmVudG9zIGRlIHRpY2tldCIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi50aWNrZXQuY29kaWdvfSDigJQge3NlbGYudGlwb30iCgoKY2xhc3MgUGdvUmVzdWx0YWRvUGVyaW9kbyhUaW1lU3RhbXBlZE1vZGVsKToKICAgICIiIgogICAgQWdyZWdhZG8gbWVuc3VhbCBwb3IgdW5pZGFkLiBDbGF2ZSBuYXR1cmFsOiAoYHBlcmlvZG9gIFlZWVktTU0sIGB1bmlkYWRfbmVnb2Npb2ApLgogICAgQ2FsY3VsYWRvIGRlc2RlIHRpY2tldHMgdsOtYSBgcGdvLnBlcmlvZG8ucmVjYWxjdWxhdGVfcGdvX3BlcmlvZG9zYC4KICAgICIiIgogICAgcGVyaW9kbyA9IG1vZGVscy5DaGFyRmllbGQobWF4X2xlbmd0aD03LCBoZWxwX3RleHQ9IllZWVktTU0iKQogICAgdW5pZGFkX25lZ29jaW8gPSBtb2RlbHMuRm9yZWlnbktleSgKICAgICAgICBVbmlkYWROZWdvY2lvLAogICAgICAgIG9uX2RlbGV0ZT1tb2RlbHMuQ0FTQ0FERSwKICAgICAgICByZWxhdGVkX25hbWU9InJlc3VsdGFkb3NfcGdvIiwKICAgICkKICAgIHRpY2tldHNfY2VycmFkb3MgPSBtb2RlbHMuUG9zaXRpdmVJbnRlZ2VyRmllbGQoZGVmYXVsdD0wKQogICAgdGlja2V0c19hYmllcnRvcyA9IG1vZGVscy5Qb3NpdGl2ZUludGVnZXJGaWVsZChkZWZhdWx0PTApCiAgICB0aWVtcG9fcHJvbWVkaW9faG9yYXMgPSBtb2RlbHMuRGVjaW1hbEZpZWxkKG1heF9kaWdpdHM9MTAsIGRlY2ltYWxfcGxhY2VzPTIsIGRlZmF1bHQ9MCkKICAgIGN1bXBsaW1pZW50b19zbGFfcGN0ID0gbW9kZWxzLkRlY2ltYWxGaWVsZChtYXhfZGlnaXRzPTUsIGRlY2ltYWxfcGxhY2VzPTIsIGRlZmF1bHQ9MCkKCiAgICBjbGFzcyBNZXRhOgogICAgICAgIHVuaXF1ZV90b2dldGhlciA9ICgicGVyaW9kbyIsICJ1bmlkYWRfbmVnb2NpbyIpCiAgICAgICAgb3JkZXJpbmcgPSBbIi1wZXJpb2RvIiwgInVuaWRhZF9uZWdvY2lvX19ub21icmUiXQogICAgICAgIHZlcmJvc2VfbmFtZSA9ICJSZXN1bHRhZG8gUEdPIHBvciBwZXLDrW9kbyIKICAgICAgICB2ZXJib3NlX25hbWVfcGx1cmFsID0gIlJlc3VsdGFkb3MgUEdPIHBvciBwZXLDrW9kbyIKCiAgICBkZWYgX19zdHJfXyhzZWxmKToKICAgICAgICByZXR1cm4gZiJ7c2VsZi5wZXJpb2RvfSDigJQge3NlbGYudW5pZGFkX25lZ29jaW8uY29kZX0iCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgo/periodo.py
PATH_JSON="pgo/periodo.py"
FILENAME=periodo.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=94
SIZE_BYTES_UTF8=3149
CONTENT_SHA256=691854cfd96da217e2ec989dd7bc7f97e6807a4d58c1672f80621e0f80bb9fcc
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Cálculo de agregados PGO por período y unidad."""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from core.wcg_models import UnidadNegocio
from pgo.models import PgoResultadoPeriodo, Ticket


def _periodo_from_dt(dt) -> str:
    if not dt:
        return timezone.now().strftime("%Y-%m")
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt)
    local = timezone.localtime(dt)
    return local.strftime("%Y-%m")


def _horas_entre(inicio, fin) -> Decimal:
    if not inicio or not fin:
        return Decimal("0")
    if timezone.is_naive(inicio):
        inicio = timezone.make_aware(inicio)
    if timezone.is_naive(fin):
        fin = timezone.make_aware(fin)
    delta = fin - inicio
    return Decimal(str(round(delta.total_seconds() / 3600, 2)))


@transaction.atomic
def recalculate_pgo_periodos(periodo: str | None = None) -> list[PgoResultadoPeriodo]:
    """
    Recalcula PgoResultadoPeriodo desde tickets.
    Métricas: recibidos, cerrados, abiertos, tiempo promedio horas, % SLA cumplido.
    """
    tickets = Ticket.objects.select_related("unidad_negocio").all()
    buckets: dict[tuple[str, int | None], dict] = defaultdict(
        lambda: {
            "cerrados": 0,
            "abiertos": 0,
            "horas_total": Decimal("0"),
            "sla_ok": 0,
            "sla_total": 0,
        }
    )

    for t in tickets:
        p = _periodo_from_dt(t.fecha_apertura)
        if periodo and p != periodo:
            continue
        un_id = t.unidad_negocio_id
        key = (p, un_id)
        if t.estado == Ticket.ESTADO_CERRADO:
            buckets[key]["cerrados"] += 1
            if t.fecha_cierre:
                horas = _horas_entre(t.fecha_apertura, t.fecha_cierre)
                buckets[key]["horas_total"] += horas
                buckets[key]["sla_total"] += 1
                if horas <= Decimal(t.sla_horas):
                    buckets[key]["sla_ok"] += 1
        else:
            buckets[key]["abiertos"] += 1

    resultados: list[PgoResultadoPeriodo] = []
    default_un = UnidadNegocio.objects.filter(code="TI").first()

    for (p, un_id), data in buckets.items():
        unidad = UnidadNegocio.objects.filter(pk=un_id).first() if un_id else default_un
        if not unidad:
            continue
        cerrados = data["cerrados"]
        tiempo_prom = (data["horas_total"] / Decimal(cerrados)) if cerrados else Decimal("0")
        sla_pct = (
            (Decimal(data["sla_ok"]) / Decimal(data["sla_total"]) * Decimal("100"))
            if data["sla_total"]
            else Decimal("0")
        )
        obj, _ = PgoResultadoPeriodo.objects.update_or_create(
            periodo=p,
            unidad_negocio=unidad,
            defaults={
                "tickets_cerrados": cerrados,
                "tickets_abiertos": data["abiertos"],
                "tiempo_promedio_horas": tiempo_prom,
                "cumplimiento_sla_pct": sla_pct.quantize(Decimal("0.01")),
            },
        )
        resultados.append(obj)
    return resultados

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Cálculo de agregados PGO por período y unidad."""
00002|
00003|from __future__ import annotations
00004|
00005|from collections import defaultdict
00006|from decimal import Decimal
00007|
00008|from django.db import transaction
00009|from django.utils import timezone
00010|
00011|from core.wcg_models import UnidadNegocio
00012|from pgo.models import PgoResultadoPeriodo, Ticket
00013|
00014|
00015|def _periodo_from_dt(dt) -> str:
00016|    if not dt:
00017|        return timezone.now().strftime("%Y-%m")
00018|    if timezone.is_naive(dt):
00019|        dt = timezone.make_aware(dt)
00020|    local = timezone.localtime(dt)
00021|    return local.strftime("%Y-%m")
00022|
00023|
00024|def _horas_entre(inicio, fin) -> Decimal:
00025|    if not inicio or not fin:
00026|        return Decimal("0")
00027|    if timezone.is_naive(inicio):
00028|        inicio = timezone.make_aware(inicio)
00029|    if timezone.is_naive(fin):
00030|        fin = timezone.make_aware(fin)
00031|    delta = fin - inicio
00032|    return Decimal(str(round(delta.total_seconds() / 3600, 2)))
00033|
00034|
00035|@transaction.atomic
00036|def recalculate_pgo_periodos(periodo: str | None = None) -> list[PgoResultadoPeriodo]:
00037|    """
00038|    Recalcula PgoResultadoPeriodo desde tickets.
00039|    Métricas: recibidos, cerrados, abiertos, tiempo promedio horas, % SLA cumplido.
00040|    """
00041|    tickets = Ticket.objects.select_related("unidad_negocio").all()
00042|    buckets: dict[tuple[str, int | None], dict] = defaultdict(
00043|        lambda: {
00044|            "cerrados": 0,
00045|            "abiertos": 0,
00046|            "horas_total": Decimal("0"),
00047|            "sla_ok": 0,
00048|            "sla_total": 0,
00049|        }
00050|    )
00051|
00052|    for t in tickets:
00053|        p = _periodo_from_dt(t.fecha_apertura)
00054|        if periodo and p != periodo:
00055|            continue
00056|        un_id = t.unidad_negocio_id
00057|        key = (p, un_id)
00058|        if t.estado == Ticket.ESTADO_CERRADO:
00059|            buckets[key]["cerrados"] += 1
00060|            if t.fecha_cierre:
00061|                horas = _horas_entre(t.fecha_apertura, t.fecha_cierre)
00062|                buckets[key]["horas_total"] += horas
00063|                buckets[key]["sla_total"] += 1
00064|                if horas <= Decimal(t.sla_horas):
00065|                    buckets[key]["sla_ok"] += 1
00066|        else:
00067|            buckets[key]["abiertos"] += 1
00068|
00069|    resultados: list[PgoResultadoPeriodo] = []
00070|    default_un = UnidadNegocio.objects.filter(code="TI").first()
00071|
00072|    for (p, un_id), data in buckets.items():
00073|        unidad = UnidadNegocio.objects.filter(pk=un_id).first() if un_id else default_un
00074|        if not unidad:
00075|            continue
00076|        cerrados = data["cerrados"]
00077|        tiempo_prom = (data["horas_total"] / Decimal(cerrados)) if cerrados else Decimal("0")
00078|        sla_pct = (
00079|            (Decimal(data["sla_ok"]) / Decimal(data["sla_total"]) * Decimal("100"))
00080|            if data["sla_total"]
00081|            else Decimal("0")
00082|        )
00083|        obj, _ = PgoResultadoPeriodo.objects.update_or_create(
00084|            periodo=p,
00085|            unidad_negocio=unidad,
00086|            defaults={
00087|                "tickets_cerrados": cerrados,
00088|                "tickets_abiertos": data["abiertos"],
00089|                "tiempo_promedio_horas": tiempo_prom,
00090|                "cumplimiento_sla_pct": sla_pct.quantize(Decimal("0.01")),
00091|            },
00092|        )
00093|        resultados.append(obj)
00094|    return resultados

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiQ8OhbGN1bG8gZGUgYWdyZWdhZG9zIFBHTyBwb3IgcGVyw61vZG8geSB1bmlkYWQuIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgpmcm9tIGNvbGxlY3Rpb25zIGltcG9ydCBkZWZhdWx0ZGljdApmcm9tIGRlY2ltYWwgaW1wb3J0IERlY2ltYWwKCmZyb20gZGphbmdvLmRiIGltcG9ydCB0cmFuc2FjdGlvbgpmcm9tIGRqYW5nby51dGlscyBpbXBvcnQgdGltZXpvbmUKCmZyb20gY29yZS53Y2dfbW9kZWxzIGltcG9ydCBVbmlkYWROZWdvY2lvCmZyb20gcGdvLm1vZGVscyBpbXBvcnQgUGdvUmVzdWx0YWRvUGVyaW9kbywgVGlja2V0CgoKZGVmIF9wZXJpb2RvX2Zyb21fZHQoZHQpIC0+IHN0cjoKICAgIGlmIG5vdCBkdDoKICAgICAgICByZXR1cm4gdGltZXpvbmUubm93KCkuc3RyZnRpbWUoIiVZLSVtIikKICAgIGlmIHRpbWV6b25lLmlzX25haXZlKGR0KToKICAgICAgICBkdCA9IHRpbWV6b25lLm1ha2VfYXdhcmUoZHQpCiAgICBsb2NhbCA9IHRpbWV6b25lLmxvY2FsdGltZShkdCkKICAgIHJldHVybiBsb2NhbC5zdHJmdGltZSgiJVktJW0iKQoKCmRlZiBfaG9yYXNfZW50cmUoaW5pY2lvLCBmaW4pIC0+IERlY2ltYWw6CiAgICBpZiBub3QgaW5pY2lvIG9yIG5vdCBmaW46CiAgICAgICAgcmV0dXJuIERlY2ltYWwoIjAiKQogICAgaWYgdGltZXpvbmUuaXNfbmFpdmUoaW5pY2lvKToKICAgICAgICBpbmljaW8gPSB0aW1lem9uZS5tYWtlX2F3YXJlKGluaWNpbykKICAgIGlmIHRpbWV6b25lLmlzX25haXZlKGZpbik6CiAgICAgICAgZmluID0gdGltZXpvbmUubWFrZV9hd2FyZShmaW4pCiAgICBkZWx0YSA9IGZpbiAtIGluaWNpbwogICAgcmV0dXJuIERlY2ltYWwoc3RyKHJvdW5kKGRlbHRhLnRvdGFsX3NlY29uZHMoKSAvIDM2MDAsIDIpKSkKCgpAdHJhbnNhY3Rpb24uYXRvbWljCmRlZiByZWNhbGN1bGF0ZV9wZ29fcGVyaW9kb3MocGVyaW9kbzogc3RyIHwgTm9uZSA9IE5vbmUpIC0+IGxpc3RbUGdvUmVzdWx0YWRvUGVyaW9kb106CiAgICAiIiIKICAgIFJlY2FsY3VsYSBQZ29SZXN1bHRhZG9QZXJpb2RvIGRlc2RlIHRpY2tldHMuCiAgICBNw6l0cmljYXM6IHJlY2liaWRvcywgY2VycmFkb3MsIGFiaWVydG9zLCB0aWVtcG8gcHJvbWVkaW8gaG9yYXMsICUgU0xBIGN1bXBsaWRvLgogICAgIiIiCiAgICB0aWNrZXRzID0gVGlja2V0Lm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoInVuaWRhZF9uZWdvY2lvIikuYWxsKCkKICAgIGJ1Y2tldHM6IGRpY3RbdHVwbGVbc3RyLCBpbnQgfCBOb25lXSwgZGljdF0gPSBkZWZhdWx0ZGljdCgKICAgICAgICBsYW1iZGE6IHsKICAgICAgICAgICAgImNlcnJhZG9zIjogMCwKICAgICAgICAgICAgImFiaWVydG9zIjogMCwKICAgICAgICAgICAgImhvcmFzX3RvdGFsIjogRGVjaW1hbCgiMCIpLAogICAgICAgICAgICAic2xhX29rIjogMCwKICAgICAgICAgICAgInNsYV90b3RhbCI6IDAsCiAgICAgICAgfQogICAgKQoKICAgIGZvciB0IGluIHRpY2tldHM6CiAgICAgICAgcCA9IF9wZXJpb2RvX2Zyb21fZHQodC5mZWNoYV9hcGVydHVyYSkKICAgICAgICBpZiBwZXJpb2RvIGFuZCBwICE9IHBlcmlvZG86CiAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgdW5faWQgPSB0LnVuaWRhZF9uZWdvY2lvX2lkCiAgICAgICAga2V5ID0gKHAsIHVuX2lkKQogICAgICAgIGlmIHQuZXN0YWRvID09IFRpY2tldC5FU1RBRE9fQ0VSUkFETzoKICAgICAgICAgICAgYnVja2V0c1trZXldWyJjZXJyYWRvcyJdICs9IDEKICAgICAgICAgICAgaWYgdC5mZWNoYV9jaWVycmU6CiAgICAgICAgICAgICAgICBob3JhcyA9IF9ob3Jhc19lbnRyZSh0LmZlY2hhX2FwZXJ0dXJhLCB0LmZlY2hhX2NpZXJyZSkKICAgICAgICAgICAgICAgIGJ1Y2tldHNba2V5XVsiaG9yYXNfdG90YWwiXSArPSBob3JhcwogICAgICAgICAgICAgICAgYnVja2V0c1trZXldWyJzbGFfdG90YWwiXSArPSAxCiAgICAgICAgICAgICAgICBpZiBob3JhcyA8PSBEZWNpbWFsKHQuc2xhX2hvcmFzKToKICAgICAgICAgICAgICAgICAgICBidWNrZXRzW2tleV1bInNsYV9vayJdICs9IDEKICAgICAgICBlbHNlOgogICAgICAgICAgICBidWNrZXRzW2tleV1bImFiaWVydG9zIl0gKz0gMQoKICAgIHJlc3VsdGFkb3M6IGxpc3RbUGdvUmVzdWx0YWRvUGVyaW9kb10gPSBbXQogICAgZGVmYXVsdF91biA9IFVuaWRhZE5lZ29jaW8ub2JqZWN0cy5maWx0ZXIoY29kZT0iVEkiKS5maXJzdCgpCgogICAgZm9yIChwLCB1bl9pZCksIGRhdGEgaW4gYnVja2V0cy5pdGVtcygpOgogICAgICAgIHVuaWRhZCA9IFVuaWRhZE5lZ29jaW8ub2JqZWN0cy5maWx0ZXIocGs9dW5faWQpLmZpcnN0KCkgaWYgdW5faWQgZWxzZSBkZWZhdWx0X3VuCiAgICAgICAgaWYgbm90IHVuaWRhZDoKICAgICAgICAgICAgY29udGludWUKICAgICAgICBjZXJyYWRvcyA9IGRhdGFbImNlcnJhZG9zIl0KICAgICAgICB0aWVtcG9fcHJvbSA9IChkYXRhWyJob3Jhc190b3RhbCJdIC8gRGVjaW1hbChjZXJyYWRvcykpIGlmIGNlcnJhZG9zIGVsc2UgRGVjaW1hbCgiMCIpCiAgICAgICAgc2xhX3BjdCA9ICgKICAgICAgICAgICAgKERlY2ltYWwoZGF0YVsic2xhX29rIl0pIC8gRGVjaW1hbChkYXRhWyJzbGFfdG90YWwiXSkgKiBEZWNpbWFsKCIxMDAiKSkKICAgICAgICAgICAgaWYgZGF0YVsic2xhX3RvdGFsIl0KICAgICAgICAgICAgZWxzZSBEZWNpbWFsKCIwIikKICAgICAgICApCiAgICAgICAgb2JqLCBfID0gUGdvUmVzdWx0YWRvUGVyaW9kby5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgIHBlcmlvZG89cCwKICAgICAgICAgICAgdW5pZGFkX25lZ29jaW89dW5pZGFkLAogICAgICAgICAgICBkZWZhdWx0cz17CiAgICAgICAgICAgICAgICAidGlja2V0c19jZXJyYWRvcyI6IGNlcnJhZG9zLAogICAgICAgICAgICAgICAgInRpY2tldHNfYWJpZXJ0b3MiOiBkYXRhWyJhYmllcnRvcyJdLAogICAgICAgICAgICAgICAgInRpZW1wb19wcm9tZWRpb19ob3JhcyI6IHRpZW1wb19wcm9tLAogICAgICAgICAgICAgICAgImN1bXBsaW1pZW50b19zbGFfcGN0Ijogc2xhX3BjdC5xdWFudGl6ZShEZWNpbWFsKCIwLjAxIikpLAogICAgICAgICAgICB9LAogICAgICAgICkKICAgICAgICByZXN1bHRhZG9zLmFwcGVuZChvYmopCiAgICByZXR1cm4gcmVzdWx0YWRvcwo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgo/selectors.py
PATH_JSON="pgo/selectors.py"
FILENAME=selectors.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=81
SIZE_BYTES_UTF8=2614
CONTENT_SHA256=12c2e47e8eda1b85261149981243a06c3aa3f132c1a361889f298b366c69a2a1
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""Consultas reutilizables PGO (modelos productivos)."""

from __future__ import annotations

from decimal import Decimal

from django.db.models import Avg, Count, Q
from django.utils import timezone

from pgo.models import Ticket

CERRADOS = Q(estado=Ticket.ESTADO_CERRADO)


def _horas_entre(inicio, fin) -> float | None:
    if not inicio or not fin:
        return None
    if timezone.is_naive(inicio):
        inicio = timezone.make_aware(inicio)
    if timezone.is_naive(fin):
        fin = timezone.make_aware(fin)
    return (fin - inicio).total_seconds() / 3600


def ticket_list_queryset(request):
    qs = Ticket.objects.select_related("unidad_negocio", "asignado_a", "entidad").order_by(
        "-fecha_apertura"
    )
    estado = request.GET.get("estado", "").strip()
    if estado:
        qs = qs.filter(estado=estado)
    prioridad = request.GET.get("prioridad", "").strip()
    if prioridad:
        qs = qs.filter(prioridad=prioridad)
    unidad = request.GET.get("unidad", "").strip()
    if unidad:
        qs = qs.filter(unidad_negocio_id=unidad)
    return qs


def ticket_dashboard_summary():
    tickets = Ticket.objects.select_related("unidad_negocio", "asignado_a")
    abiertos = tickets.exclude(CERRADOS)
    cerrados = tickets.filter(CERRADOS)

    # SLA: cerrado dentro de sla_horas, o abierto ya excedido
    vencidos = 0
    horas_list = []
    for t in tickets.filter(fecha_cierre__isnull=False):
        h = _horas_entre(t.fecha_apertura, t.fecha_cierre)
        if h is not None:
            horas_list.append(h)
    now = timezone.now()
    for t in abiertos:
        h = _horas_entre(t.fecha_apertura, now)
        if h is not None and h > t.sla_horas:
            vencidos += 1

    por_estado = list(
        tickets.values("estado").annotate(total=Count("id")).order_by("-total")
    )
    por_prioridad = list(
        tickets.values("prioridad").annotate(total=Count("id")).order_by("-total")
    )
    avg_h = sum(horas_list) / len(horas_list) if horas_list else None

    return {
        "total_tickets": tickets.count(),
        "tickets_cerrados": cerrados.count(),
        "tickets_abiertos": abiertos.count(),
        "tickets_vencidos": vencidos,
        "tiempo_promedio": avg_h,
        "por_estado": por_estado,
        "por_prioridad": por_prioridad,
        "tickets_recientes": list(tickets.order_by("-fecha_apertura")[:12]),
        "resultados": list(
            __import__("pgo.models", fromlist=["PgoResultadoPeriodo"])
            .PgoResultadoPeriodo.objects.select_related("unidad_negocio")
            .order_by("-periodo")[:12]
        ),
    }

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Consultas reutilizables PGO (modelos productivos)."""
00002|
00003|from __future__ import annotations
00004|
00005|from decimal import Decimal
00006|
00007|from django.db.models import Avg, Count, Q
00008|from django.utils import timezone
00009|
00010|from pgo.models import Ticket
00011|
00012|CERRADOS = Q(estado=Ticket.ESTADO_CERRADO)
00013|
00014|
00015|def _horas_entre(inicio, fin) -> float | None:
00016|    if not inicio or not fin:
00017|        return None
00018|    if timezone.is_naive(inicio):
00019|        inicio = timezone.make_aware(inicio)
00020|    if timezone.is_naive(fin):
00021|        fin = timezone.make_aware(fin)
00022|    return (fin - inicio).total_seconds() / 3600
00023|
00024|
00025|def ticket_list_queryset(request):
00026|    qs = Ticket.objects.select_related("unidad_negocio", "asignado_a", "entidad").order_by(
00027|        "-fecha_apertura"
00028|    )
00029|    estado = request.GET.get("estado", "").strip()
00030|    if estado:
00031|        qs = qs.filter(estado=estado)
00032|    prioridad = request.GET.get("prioridad", "").strip()
00033|    if prioridad:
00034|        qs = qs.filter(prioridad=prioridad)
00035|    unidad = request.GET.get("unidad", "").strip()
00036|    if unidad:
00037|        qs = qs.filter(unidad_negocio_id=unidad)
00038|    return qs
00039|
00040|
00041|def ticket_dashboard_summary():
00042|    tickets = Ticket.objects.select_related("unidad_negocio", "asignado_a")
00043|    abiertos = tickets.exclude(CERRADOS)
00044|    cerrados = tickets.filter(CERRADOS)
00045|
00046|    # SLA: cerrado dentro de sla_horas, o abierto ya excedido
00047|    vencidos = 0
00048|    horas_list = []
00049|    for t in tickets.filter(fecha_cierre__isnull=False):
00050|        h = _horas_entre(t.fecha_apertura, t.fecha_cierre)
00051|        if h is not None:
00052|            horas_list.append(h)
00053|    now = timezone.now()
00054|    for t in abiertos:
00055|        h = _horas_entre(t.fecha_apertura, now)
00056|        if h is not None and h > t.sla_horas:
00057|            vencidos += 1
00058|
00059|    por_estado = list(
00060|        tickets.values("estado").annotate(total=Count("id")).order_by("-total")
00061|    )
00062|    por_prioridad = list(
00063|        tickets.values("prioridad").annotate(total=Count("id")).order_by("-total")
00064|    )
00065|    avg_h = sum(horas_list) / len(horas_list) if horas_list else None
00066|
00067|    return {
00068|        "total_tickets": tickets.count(),
00069|        "tickets_cerrados": cerrados.count(),
00070|        "tickets_abiertos": abiertos.count(),
00071|        "tickets_vencidos": vencidos,
00072|        "tiempo_promedio": avg_h,
00073|        "por_estado": por_estado,
00074|        "por_prioridad": por_prioridad,
00075|        "tickets_recientes": list(tickets.order_by("-fecha_apertura")[:12]),
00076|        "resultados": list(
00077|            __import__("pgo.models", fromlist=["PgoResultadoPeriodo"])
00078|            .PgoResultadoPeriodo.objects.select_related("unidad_negocio")
00079|            .order_by("-periodo")[:12]
00080|        ),
00081|    }

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiQ29uc3VsdGFzIHJldXRpbGl6YWJsZXMgUEdPIChtb2RlbG9zIHByb2R1Y3Rpdm9zKS4iIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmZyb20gZGVjaW1hbCBpbXBvcnQgRGVjaW1hbAoKZnJvbSBkamFuZ28uZGIubW9kZWxzIGltcG9ydCBBdmcsIENvdW50LCBRCmZyb20gZGphbmdvLnV0aWxzIGltcG9ydCB0aW1lem9uZQoKZnJvbSBwZ28ubW9kZWxzIGltcG9ydCBUaWNrZXQKCkNFUlJBRE9TID0gUShlc3RhZG89VGlja2V0LkVTVEFET19DRVJSQURPKQoKCmRlZiBfaG9yYXNfZW50cmUoaW5pY2lvLCBmaW4pIC0+IGZsb2F0IHwgTm9uZToKICAgIGlmIG5vdCBpbmljaW8gb3Igbm90IGZpbjoKICAgICAgICByZXR1cm4gTm9uZQogICAgaWYgdGltZXpvbmUuaXNfbmFpdmUoaW5pY2lvKToKICAgICAgICBpbmljaW8gPSB0aW1lem9uZS5tYWtlX2F3YXJlKGluaWNpbykKICAgIGlmIHRpbWV6b25lLmlzX25haXZlKGZpbik6CiAgICAgICAgZmluID0gdGltZXpvbmUubWFrZV9hd2FyZShmaW4pCiAgICByZXR1cm4gKGZpbiAtIGluaWNpbykudG90YWxfc2Vjb25kcygpIC8gMzYwMAoKCmRlZiB0aWNrZXRfbGlzdF9xdWVyeXNldChyZXF1ZXN0KToKICAgIHFzID0gVGlja2V0Lm9iamVjdHMuc2VsZWN0X3JlbGF0ZWQoInVuaWRhZF9uZWdvY2lvIiwgImFzaWduYWRvX2EiLCAiZW50aWRhZCIpLm9yZGVyX2J5KAogICAgICAgICItZmVjaGFfYXBlcnR1cmEiCiAgICApCiAgICBlc3RhZG8gPSByZXF1ZXN0LkdFVC5nZXQoImVzdGFkbyIsICIiKS5zdHJpcCgpCiAgICBpZiBlc3RhZG86CiAgICAgICAgcXMgPSBxcy5maWx0ZXIoZXN0YWRvPWVzdGFkbykKICAgIHByaW9yaWRhZCA9IHJlcXVlc3QuR0VULmdldCgicHJpb3JpZGFkIiwgIiIpLnN0cmlwKCkKICAgIGlmIHByaW9yaWRhZDoKICAgICAgICBxcyA9IHFzLmZpbHRlcihwcmlvcmlkYWQ9cHJpb3JpZGFkKQogICAgdW5pZGFkID0gcmVxdWVzdC5HRVQuZ2V0KCJ1bmlkYWQiLCAiIikuc3RyaXAoKQogICAgaWYgdW5pZGFkOgogICAgICAgIHFzID0gcXMuZmlsdGVyKHVuaWRhZF9uZWdvY2lvX2lkPXVuaWRhZCkKICAgIHJldHVybiBxcwoKCmRlZiB0aWNrZXRfZGFzaGJvYXJkX3N1bW1hcnkoKToKICAgIHRpY2tldHMgPSBUaWNrZXQub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgidW5pZGFkX25lZ29jaW8iLCAiYXNpZ25hZG9fYSIpCiAgICBhYmllcnRvcyA9IHRpY2tldHMuZXhjbHVkZShDRVJSQURPUykKICAgIGNlcnJhZG9zID0gdGlja2V0cy5maWx0ZXIoQ0VSUkFET1MpCgogICAgIyBTTEE6IGNlcnJhZG8gZGVudHJvIGRlIHNsYV9ob3JhcywgbyBhYmllcnRvIHlhIGV4Y2VkaWRvCiAgICB2ZW5jaWRvcyA9IDAKICAgIGhvcmFzX2xpc3QgPSBbXQogICAgZm9yIHQgaW4gdGlja2V0cy5maWx0ZXIoZmVjaGFfY2llcnJlX19pc251bGw9RmFsc2UpOgogICAgICAgIGggPSBfaG9yYXNfZW50cmUodC5mZWNoYV9hcGVydHVyYSwgdC5mZWNoYV9jaWVycmUpCiAgICAgICAgaWYgaCBpcyBub3QgTm9uZToKICAgICAgICAgICAgaG9yYXNfbGlzdC5hcHBlbmQoaCkKICAgIG5vdyA9IHRpbWV6b25lLm5vdygpCiAgICBmb3IgdCBpbiBhYmllcnRvczoKICAgICAgICBoID0gX2hvcmFzX2VudHJlKHQuZmVjaGFfYXBlcnR1cmEsIG5vdykKICAgICAgICBpZiBoIGlzIG5vdCBOb25lIGFuZCBoID4gdC5zbGFfaG9yYXM6CiAgICAgICAgICAgIHZlbmNpZG9zICs9IDEKCiAgICBwb3JfZXN0YWRvID0gbGlzdCgKICAgICAgICB0aWNrZXRzLnZhbHVlcygiZXN0YWRvIikuYW5ub3RhdGUodG90YWw9Q291bnQoImlkIikpLm9yZGVyX2J5KCItdG90YWwiKQogICAgKQogICAgcG9yX3ByaW9yaWRhZCA9IGxpc3QoCiAgICAgICAgdGlja2V0cy52YWx1ZXMoInByaW9yaWRhZCIpLmFubm90YXRlKHRvdGFsPUNvdW50KCJpZCIpKS5vcmRlcl9ieSgiLXRvdGFsIikKICAgICkKICAgIGF2Z19oID0gc3VtKGhvcmFzX2xpc3QpIC8gbGVuKGhvcmFzX2xpc3QpIGlmIGhvcmFzX2xpc3QgZWxzZSBOb25lCgogICAgcmV0dXJuIHsKICAgICAgICAidG90YWxfdGlja2V0cyI6IHRpY2tldHMuY291bnQoKSwKICAgICAgICAidGlja2V0c19jZXJyYWRvcyI6IGNlcnJhZG9zLmNvdW50KCksCiAgICAgICAgInRpY2tldHNfYWJpZXJ0b3MiOiBhYmllcnRvcy5jb3VudCgpLAogICAgICAgICJ0aWNrZXRzX3ZlbmNpZG9zIjogdmVuY2lkb3MsCiAgICAgICAgInRpZW1wb19wcm9tZWRpbyI6IGF2Z19oLAogICAgICAgICJwb3JfZXN0YWRvIjogcG9yX2VzdGFkbywKICAgICAgICAicG9yX3ByaW9yaWRhZCI6IHBvcl9wcmlvcmlkYWQsCiAgICAgICAgInRpY2tldHNfcmVjaWVudGVzIjogbGlzdCh0aWNrZXRzLm9yZGVyX2J5KCItZmVjaGFfYXBlcnR1cmEiKVs6MTJdKSwKICAgICAgICAicmVzdWx0YWRvcyI6IGxpc3QoCiAgICAgICAgICAgIF9faW1wb3J0X18oInBnby5tb2RlbHMiLCBmcm9tbGlzdD1bIlBnb1Jlc3VsdGFkb1BlcmlvZG8iXSkKICAgICAgICAgICAgLlBnb1Jlc3VsdGFkb1BlcmlvZG8ub2JqZWN0cy5zZWxlY3RfcmVsYXRlZCgidW5pZGFkX25lZ29jaW8iKQogICAgICAgICAgICAub3JkZXJfYnkoIi1wZXJpb2RvIilbOjEyXQogICAgICAgICksCiAgICB9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgo/services.py
PATH_JSON="pgo/services.py"
FILENAME=services.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=221
SIZE_BYTES_UTF8=8585
CONTENT_SHA256=beea64b1d5d9ef86ce491592fbcd4262c1267cf3cedab657be0c22b6c7e921c1
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
"""
Importadores PGO.

Archivos referencia:
  - `pgo datos - Archivos para PGO.csv` (catálogo — informativo, no crea tickets)
  - `pgo datos - control de tickets marzo abril y mayo 2026 para PGO.xlsx`
  - `pgo ejemplo del analisis - PGO - TI Q22026.xlsx`

Columnas mínimas tickets (alias):
  - codigo: Ticket, ID, Folio, No_Ticket
  - titulo: Titulo, Asunto, Descripcion_Corta
  - estado, prioridad, asignado, fecha_apertura, fecha_cierre, unidad_negocio, sla_horas

Clave natural: `codigo`
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.services.column_map import normalize_columns, pick, pick_int, require_any
from core.services.import_base import read_dataframe, run_import_batch
from core.wcg_models import DataImportBatch, Entidad, UnidadNegocio
from crm.services import _resolve_unidad, _slug_codigo
from pgo.models import Ticket

User = get_user_model()


def _parse_dt(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, datetime):
        dt = value
        return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
    if hasattr(value, "to_pydatetime"):
        try:
            dt = value.to_pydatetime()
            return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
        except Exception:
            pass
    text = str(value).strip()
    if not text or text.lower() in ("nan", "nat", "none"):
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y %H:%M", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            dt = datetime.strptime(text[:19], fmt)
            return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
        except ValueError:
            continue
    try:
        dt = pd.to_datetime(text).to_pydatetime()
        return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
    except Exception:
        return None


def _map_estado(raw: str) -> str:
    s = (raw or "").upper()
    if any(k in s for k in ("CERR", "CLOSE", "RESUEL", "RECHAZ", "CONFIGUR", "NO EXISTE")):
        return Ticket.ESTADO_CERRADO
    if any(k in s for k in ("PROCES", "PROGRESS", "PRUEBA", "ESPERA", "PROVEEDOR", "CURSO")):
        return Ticket.ESTADO_EN_PROCESO
    return Ticket.ESTADO_ABIERTO


def _map_prioridad(raw: str) -> str:
    s = (raw or "").upper()
    if "ALT" in s or "HIGH" in s:
        return Ticket.PRIORIDAD_ALTA
    if "BAJ" in s or "LOW" in s:
        return Ticket.PRIORIDAD_BAJA
    return Ticket.PRIORIDAD_MEDIA


def _read_tickets_dataframe(uploaded_file) -> pd.DataFrame:
    name = (uploaded_file.name or "").lower()
    if name.endswith((".xlsx", ".xls")):
        return normalize_columns(read_dataframe(uploaded_file, all_data_sheets=True))
    return normalize_columns(read_dataframe(uploaded_file))


def import_tickets(user, uploaded_file) -> DataImportBatch:
    df = _read_tickets_dataframe(uploaded_file)
    require_any(
        df,
        [
            ["codigo", "ticket", "id", "folio", "no_ticket"],
            ["titulo", "asunto", "descripcion", "tema"],
        ],
    )

    def handler(row: pd.Series, errors: list[str]):
        codigo = pick(row, "codigo", "ticket", "id", "folio", "no_ticket", "id_ticket")
        titulo = pick(row, "titulo", "asunto", "descripcion", "descripcion_corta", "tema")
        if not codigo or not titulo:
            errors.append("codigo y titulo obligatorios")
            return None
        # Evitar IDs float "368.0"
        if codigo.endswith(".0") and codigo[:-2].isdigit():
            codigo = codigo[:-2]
        entidad = None
        ent_code = pick(row, "entidad_codigo", "cliente_codigo", "nit")
        if ent_code:
            entidad = Entidad.objects.filter(codigo__iexact=_slug_codigo(ent_code)).first()
        unidad_raw = pick(row, "unidad_negocio", "unidad", "departamento", "area", "sistema") or "TI"
        unidad = _resolve_unidad(unidad_raw)
        if unidad is None:
            # Departamentos internos → TI por defecto
            unidad, _ = UnidadNegocio.objects.get_or_create(
                code="TI",
                defaults={"nombre": "Tecnología / TI", "activa": True},
            )
        asignado = None
        username = pick(row, "asignado", "asignado_a", "responsable", "tecnico", "agente", "estado2")
        if username and username.lower() not in ("sin asignarse", "sin asignar", "none", "nan"):
            first = username.split()[0]
            asignado = User.objects.filter(username__iexact=first).first()
            if not asignado:
                asignado = User.objects.filter(first_name__icontains=first).first()
        fecha_apertura = (
            _parse_dt(pick(row, "fecha_apertura", "fecha_creacion", "creado", "apertura", "fecha_registro"))
            or timezone.now()
        )
        fecha_cierre = _parse_dt(pick(row, "fecha_cierre", "cerrado", "fecha_resolucion"))
        estado = _map_estado(pick(row, "estado", "status", "estado_ticket"))
        if fecha_cierre and estado == Ticket.ESTADO_ABIERTO:
            # Rechazado/Resuelto con fecha de cierre → cerrado
            if any(k in pick(row, "estado").upper() for k in ("RECHAZ", "RESUEL", "CERR")):
                estado = Ticket.ESTADO_CERRADO
        duracion = pick(row, "duracion")
        sla = pick_int(row, "sla_horas", "sla", default=48)
        if duracion:
            try:
                # Duración en horas del archivo helpdesk; SLA = max(48, ceil(duracion*1.2))
                d = float(str(duracion).replace(",", "."))
                if d > 0:
                    sla = max(sla, int(d) + 8)
            except ValueError:
                pass
        descripcion = pick(row, "descripcion", "detalle", "notas", "solucion")
        solicitante = pick(row, "usuario_solicita", "solicitante")
        if solicitante:
            descripcion = f"Solicita: {solicitante}\n{descripcion}".strip()
        _, created = Ticket.objects.update_or_create(
            codigo=str(codigo),
            defaults={
                "titulo": titulo[:200],
                "descripcion": descripcion,
                "entidad": entidad,
                "unidad_negocio": unidad,
                "estado": estado,
                "prioridad": _map_prioridad(pick(row, "prioridad", "prioridad_ticket")),
                "asignado_a": asignado,
                "fecha_apertura": fecha_apertura,
                "fecha_cierre": fecha_cierre,
                "sla_horas": sla,
            },
        )
        return created, not created

    uploaded_file.seek(0)

    # run_import_batch re-lee el archivo; para multi-hoja usamos handler sobre df ya leído
    batch = DataImportBatch.objects.create(
        modulo=DataImportBatch.MODULO_PGO,
        tipo_importacion="tickets",
        archivo_nombre=uploaded_file.name,
        uploaded_by=user,
        status=DataImportBatch.STATUS_PENDING,
        filas_leidas=len(df),
    )
    logs: list[str] = []
    for idx, row in df.iterrows():
        row_errors: list[str] = []
        try:
            result = handler(row, row_errors)
            if row_errors:
                batch.errores += 1
                logs.append(f"Fila {idx + 2}: {'; '.join(row_errors)}")
            elif result:
                created, updated = result
                if created:
                    batch.creados += 1
                if updated:
                    batch.actualizados += 1
        except Exception as exc:
            batch.errores += 1
            logs.append(f"Fila {idx + 2}: {exc}")
    if batch.errores == 0:
        batch.status = DataImportBatch.STATUS_OK
    elif batch.creados + batch.actualizados > 0:
        batch.status = DataImportBatch.STATUS_PARTIAL
    else:
        batch.status = DataImportBatch.STATUS_ERROR
    batch.log_texto = "\n".join(logs)[:8000]
    batch.save()
    return batch


def import_archivos_catalogo(user, uploaded_file) -> DataImportBatch:
    """
    Catálogo de archivos PGO — solo registra lote (sin crear tickets).
    """
    from core.wcg_models import DataImportBatch as Batch

    df = normalize_columns(read_dataframe(uploaded_file))
    batch = Batch.objects.create(
        modulo=Batch.MODULO_PGO,
        tipo_importacion="archivos_catalogo",
        archivo_nombre=uploaded_file.name,
        uploaded_by=user,
        filas_leidas=len(df),
        status=Batch.STATUS_OK,
        log_texto=f"Catálogo leído ({len(df)} filas). Sin carga a tickets.",
    )
    return batch

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Importadores PGO.
00003|
00004|Archivos referencia:
00005|  - `pgo datos - Archivos para PGO.csv` (catálogo — informativo, no crea tickets)
00006|  - `pgo datos - control de tickets marzo abril y mayo 2026 para PGO.xlsx`
00007|  - `pgo ejemplo del analisis - PGO - TI Q22026.xlsx`
00008|
00009|Columnas mínimas tickets (alias):
00010|  - codigo: Ticket, ID, Folio, No_Ticket
00011|  - titulo: Titulo, Asunto, Descripcion_Corta
00012|  - estado, prioridad, asignado, fecha_apertura, fecha_cierre, unidad_negocio, sla_horas
00013|
00014|Clave natural: `codigo`
00015|"""
00016|
00017|from __future__ import annotations
00018|
00019|from datetime import datetime
00020|
00021|import pandas as pd
00022|from django.contrib.auth import get_user_model
00023|from django.utils import timezone
00024|
00025|from core.services.column_map import normalize_columns, pick, pick_int, require_any
00026|from core.services.import_base import read_dataframe, run_import_batch
00027|from core.wcg_models import DataImportBatch, Entidad, UnidadNegocio
00028|from crm.services import _resolve_unidad, _slug_codigo
00029|from pgo.models import Ticket
00030|
00031|User = get_user_model()
00032|
00033|
00034|def _parse_dt(value):
00035|    if value is None or (isinstance(value, float) and pd.isna(value)):
00036|        return None
00037|    if isinstance(value, datetime):
00038|        dt = value
00039|        return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
00040|    if hasattr(value, "to_pydatetime"):
00041|        try:
00042|            dt = value.to_pydatetime()
00043|            return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
00044|        except Exception:
00045|            pass
00046|    text = str(value).strip()
00047|    if not text or text.lower() in ("nan", "nat", "none"):
00048|        return None
00049|    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y %H:%M", "%d/%m/%Y", "%m/%d/%Y"):
00050|        try:
00051|            dt = datetime.strptime(text[:19], fmt)
00052|            return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
00053|        except ValueError:
00054|            continue
00055|    try:
00056|        dt = pd.to_datetime(text).to_pydatetime()
00057|        return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
00058|    except Exception:
00059|        return None
00060|
00061|
00062|def _map_estado(raw: str) -> str:
00063|    s = (raw or "").upper()
00064|    if any(k in s for k in ("CERR", "CLOSE", "RESUEL", "RECHAZ", "CONFIGUR", "NO EXISTE")):
00065|        return Ticket.ESTADO_CERRADO
00066|    if any(k in s for k in ("PROCES", "PROGRESS", "PRUEBA", "ESPERA", "PROVEEDOR", "CURSO")):
00067|        return Ticket.ESTADO_EN_PROCESO
00068|    return Ticket.ESTADO_ABIERTO
00069|
00070|
00071|def _map_prioridad(raw: str) -> str:
00072|    s = (raw or "").upper()
00073|    if "ALT" in s or "HIGH" in s:
00074|        return Ticket.PRIORIDAD_ALTA
00075|    if "BAJ" in s or "LOW" in s:
00076|        return Ticket.PRIORIDAD_BAJA
00077|    return Ticket.PRIORIDAD_MEDIA
00078|
00079|
00080|def _read_tickets_dataframe(uploaded_file) -> pd.DataFrame:
00081|    name = (uploaded_file.name or "").lower()
00082|    if name.endswith((".xlsx", ".xls")):
00083|        return normalize_columns(read_dataframe(uploaded_file, all_data_sheets=True))
00084|    return normalize_columns(read_dataframe(uploaded_file))
00085|
00086|
00087|def import_tickets(user, uploaded_file) -> DataImportBatch:
00088|    df = _read_tickets_dataframe(uploaded_file)
00089|    require_any(
00090|        df,
00091|        [
00092|            ["codigo", "ticket", "id", "folio", "no_ticket"],
00093|            ["titulo", "asunto", "descripcion", "tema"],
00094|        ],
00095|    )
00096|
00097|    def handler(row: pd.Series, errors: list[str]):
00098|        codigo = pick(row, "codigo", "ticket", "id", "folio", "no_ticket", "id_ticket")
00099|        titulo = pick(row, "titulo", "asunto", "descripcion", "descripcion_corta", "tema")
00100|        if not codigo or not titulo:
00101|            errors.append("codigo y titulo obligatorios")
00102|            return None
00103|        # Evitar IDs float "368.0"
00104|        if codigo.endswith(".0") and codigo[:-2].isdigit():
00105|            codigo = codigo[:-2]
00106|        entidad = None
00107|        ent_code = pick(row, "entidad_codigo", "cliente_codigo", "nit")
00108|        if ent_code:
00109|            entidad = Entidad.objects.filter(codigo__iexact=_slug_codigo(ent_code)).first()
00110|        unidad_raw = pick(row, "unidad_negocio", "unidad", "departamento", "area", "sistema") or "TI"
00111|        unidad = _resolve_unidad(unidad_raw)
00112|        if unidad is None:
00113|            # Departamentos internos → TI por defecto
00114|            unidad, _ = UnidadNegocio.objects.get_or_create(
00115|                code="TI",
00116|                defaults={"nombre": "Tecnología / TI", "activa": True},
00117|            )
00118|        asignado = None
00119|        username = pick(row, "asignado", "asignado_a", "responsable", "tecnico", "agente", "estado2")
00120|        if username and username.lower() not in ("sin asignarse", "sin asignar", "none", "nan"):
00121|            first = username.split()[0]
00122|            asignado = User.objects.filter(username__iexact=first).first()
00123|            if not asignado:
00124|                asignado = User.objects.filter(first_name__icontains=first).first()
00125|        fecha_apertura = (
00126|            _parse_dt(pick(row, "fecha_apertura", "fecha_creacion", "creado", "apertura", "fecha_registro"))
00127|            or timezone.now()
00128|        )
00129|        fecha_cierre = _parse_dt(pick(row, "fecha_cierre", "cerrado", "fecha_resolucion"))
00130|        estado = _map_estado(pick(row, "estado", "status", "estado_ticket"))
00131|        if fecha_cierre and estado == Ticket.ESTADO_ABIERTO:
00132|            # Rechazado/Resuelto con fecha de cierre → cerrado
00133|            if any(k in pick(row, "estado").upper() for k in ("RECHAZ", "RESUEL", "CERR")):
00134|                estado = Ticket.ESTADO_CERRADO
00135|        duracion = pick(row, "duracion")
00136|        sla = pick_int(row, "sla_horas", "sla", default=48)
00137|        if duracion:
00138|            try:
00139|                # Duración en horas del archivo helpdesk; SLA = max(48, ceil(duracion*1.2))
00140|                d = float(str(duracion).replace(",", "."))
00141|                if d > 0:
00142|                    sla = max(sla, int(d) + 8)
00143|            except ValueError:
00144|                pass
00145|        descripcion = pick(row, "descripcion", "detalle", "notas", "solucion")
00146|        solicitante = pick(row, "usuario_solicita", "solicitante")
00147|        if solicitante:
00148|            descripcion = f"Solicita: {solicitante}\n{descripcion}".strip()
00149|        _, created = Ticket.objects.update_or_create(
00150|            codigo=str(codigo),
00151|            defaults={
00152|                "titulo": titulo[:200],
00153|                "descripcion": descripcion,
00154|                "entidad": entidad,
00155|                "unidad_negocio": unidad,
00156|                "estado": estado,
00157|                "prioridad": _map_prioridad(pick(row, "prioridad", "prioridad_ticket")),
00158|                "asignado_a": asignado,
00159|                "fecha_apertura": fecha_apertura,
00160|                "fecha_cierre": fecha_cierre,
00161|                "sla_horas": sla,
00162|            },
00163|        )
00164|        return created, not created
00165|
00166|    uploaded_file.seek(0)
00167|
00168|    # run_import_batch re-lee el archivo; para multi-hoja usamos handler sobre df ya leído
00169|    batch = DataImportBatch.objects.create(
00170|        modulo=DataImportBatch.MODULO_PGO,
00171|        tipo_importacion="tickets",
00172|        archivo_nombre=uploaded_file.name,
00173|        uploaded_by=user,
00174|        status=DataImportBatch.STATUS_PENDING,
00175|        filas_leidas=len(df),
00176|    )
00177|    logs: list[str] = []
00178|    for idx, row in df.iterrows():
00179|        row_errors: list[str] = []
00180|        try:
00181|            result = handler(row, row_errors)
00182|            if row_errors:
00183|                batch.errores += 1
00184|                logs.append(f"Fila {idx + 2}: {'; '.join(row_errors)}")
00185|            elif result:
00186|                created, updated = result
00187|                if created:
00188|                    batch.creados += 1
00189|                if updated:
00190|                    batch.actualizados += 1
00191|        except Exception as exc:
00192|            batch.errores += 1
00193|            logs.append(f"Fila {idx + 2}: {exc}")
00194|    if batch.errores == 0:
00195|        batch.status = DataImportBatch.STATUS_OK
00196|    elif batch.creados + batch.actualizados > 0:
00197|        batch.status = DataImportBatch.STATUS_PARTIAL
00198|    else:
00199|        batch.status = DataImportBatch.STATUS_ERROR
00200|    batch.log_texto = "\n".join(logs)[:8000]
00201|    batch.save()
00202|    return batch
00203|
00204|
00205|def import_archivos_catalogo(user, uploaded_file) -> DataImportBatch:
00206|    """
00207|    Catálogo de archivos PGO — solo registra lote (sin crear tickets).
00208|    """
00209|    from core.wcg_models import DataImportBatch as Batch
00210|
00211|    df = normalize_columns(read_dataframe(uploaded_file))
00212|    batch = Batch.objects.create(
00213|        modulo=Batch.MODULO_PGO,
00214|        tipo_importacion="archivos_catalogo",
00215|        archivo_nombre=uploaded_file.name,
00216|        uploaded_by=user,
00217|        filas_leidas=len(df),
00218|        status=Batch.STATUS_OK,
00219|        log_texto=f"Catálogo leído ({len(df)} filas). Sin carga a tickets.",
00220|    )
00221|    return batch

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiCkltcG9ydGFkb3JlcyBQR08uCgpBcmNoaXZvcyByZWZlcmVuY2lhOgogIC0gYHBnbyBkYXRvcyAtIEFyY2hpdm9zIHBhcmEgUEdPLmNzdmAgKGNhdMOhbG9nbyDigJQgaW5mb3JtYXRpdm8sIG5vIGNyZWEgdGlja2V0cykKICAtIGBwZ28gZGF0b3MgLSBjb250cm9sIGRlIHRpY2tldHMgbWFyem8gYWJyaWwgeSBtYXlvIDIwMjYgcGFyYSBQR08ueGxzeGAKICAtIGBwZ28gZWplbXBsbyBkZWwgYW5hbGlzaXMgLSBQR08gLSBUSSBRMjIwMjYueGxzeGAKCkNvbHVtbmFzIG3DrW5pbWFzIHRpY2tldHMgKGFsaWFzKToKICAtIGNvZGlnbzogVGlja2V0LCBJRCwgRm9saW8sIE5vX1RpY2tldAogIC0gdGl0dWxvOiBUaXR1bG8sIEFzdW50bywgRGVzY3JpcGNpb25fQ29ydGEKICAtIGVzdGFkbywgcHJpb3JpZGFkLCBhc2lnbmFkbywgZmVjaGFfYXBlcnR1cmEsIGZlY2hhX2NpZXJyZSwgdW5pZGFkX25lZ29jaW8sIHNsYV9ob3JhcwoKQ2xhdmUgbmF0dXJhbDogYGNvZGlnb2AKIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgpmcm9tIGRhdGV0aW1lIGltcG9ydCBkYXRldGltZQoKaW1wb3J0IHBhbmRhcyBhcyBwZApmcm9tIGRqYW5nby5jb250cmliLmF1dGggaW1wb3J0IGdldF91c2VyX21vZGVsCmZyb20gZGphbmdvLnV0aWxzIGltcG9ydCB0aW1lem9uZQoKZnJvbSBjb3JlLnNlcnZpY2VzLmNvbHVtbl9tYXAgaW1wb3J0IG5vcm1hbGl6ZV9jb2x1bW5zLCBwaWNrLCBwaWNrX2ludCwgcmVxdWlyZV9hbnkKZnJvbSBjb3JlLnNlcnZpY2VzLmltcG9ydF9iYXNlIGltcG9ydCByZWFkX2RhdGFmcmFtZSwgcnVuX2ltcG9ydF9iYXRjaApmcm9tIGNvcmUud2NnX21vZGVscyBpbXBvcnQgRGF0YUltcG9ydEJhdGNoLCBFbnRpZGFkLCBVbmlkYWROZWdvY2lvCmZyb20gY3JtLnNlcnZpY2VzIGltcG9ydCBfcmVzb2x2ZV91bmlkYWQsIF9zbHVnX2NvZGlnbwpmcm9tIHBnby5tb2RlbHMgaW1wb3J0IFRpY2tldAoKVXNlciA9IGdldF91c2VyX21vZGVsKCkKCgpkZWYgX3BhcnNlX2R0KHZhbHVlKToKICAgIGlmIHZhbHVlIGlzIE5vbmUgb3IgKGlzaW5zdGFuY2UodmFsdWUsIGZsb2F0KSBhbmQgcGQuaXNuYSh2YWx1ZSkpOgogICAgICAgIHJldHVybiBOb25lCiAgICBpZiBpc2luc3RhbmNlKHZhbHVlLCBkYXRldGltZSk6CiAgICAgICAgZHQgPSB2YWx1ZQogICAgICAgIHJldHVybiB0aW1lem9uZS5tYWtlX2F3YXJlKGR0KSBpZiB0aW1lem9uZS5pc19uYWl2ZShkdCkgZWxzZSBkdAogICAgaWYgaGFzYXR0cih2YWx1ZSwgInRvX3B5ZGF0ZXRpbWUiKToKICAgICAgICB0cnk6CiAgICAgICAgICAgIGR0ID0gdmFsdWUudG9fcHlkYXRldGltZSgpCiAgICAgICAgICAgIHJldHVybiB0aW1lem9uZS5tYWtlX2F3YXJlKGR0KSBpZiB0aW1lem9uZS5pc19uYWl2ZShkdCkgZWxzZSBkdAogICAgICAgIGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgICAgIHBhc3MKICAgIHRleHQgPSBzdHIodmFsdWUpLnN0cmlwKCkKICAgIGlmIG5vdCB0ZXh0IG9yIHRleHQubG93ZXIoKSBpbiAoIm5hbiIsICJuYXQiLCAibm9uZSIpOgogICAgICAgIHJldHVybiBOb25lCiAgICBmb3IgZm10IGluICgiJVktJW0tJWQgJUg6JU06JVMiLCAiJVktJW0tJWQiLCAiJWQvJW0vJVkgJUg6JU0iLCAiJWQvJW0vJVkiLCAiJW0vJWQvJVkiKToKICAgICAgICB0cnk6CiAgICAgICAgICAgIGR0ID0gZGF0ZXRpbWUuc3RycHRpbWUodGV4dFs6MTldLCBmbXQpCiAgICAgICAgICAgIHJldHVybiB0aW1lem9uZS5tYWtlX2F3YXJlKGR0KSBpZiB0aW1lem9uZS5pc19uYWl2ZShkdCkgZWxzZSBkdAogICAgICAgIGV4Y2VwdCBWYWx1ZUVycm9yOgogICAgICAgICAgICBjb250aW51ZQogICAgdHJ5OgogICAgICAgIGR0ID0gcGQudG9fZGF0ZXRpbWUodGV4dCkudG9fcHlkYXRldGltZSgpCiAgICAgICAgcmV0dXJuIHRpbWV6b25lLm1ha2VfYXdhcmUoZHQpIGlmIHRpbWV6b25lLmlzX25haXZlKGR0KSBlbHNlIGR0CiAgICBleGNlcHQgRXhjZXB0aW9uOgogICAgICAgIHJldHVybiBOb25lCgoKZGVmIF9tYXBfZXN0YWRvKHJhdzogc3RyKSAtPiBzdHI6CiAgICBzID0gKHJhdyBvciAiIikudXBwZXIoKQogICAgaWYgYW55KGsgaW4gcyBmb3IgayBpbiAoIkNFUlIiLCAiQ0xPU0UiLCAiUkVTVUVMIiwgIlJFQ0hBWiIsICJDT05GSUdVUiIsICJOTyBFWElTVEUiKSk6CiAgICAgICAgcmV0dXJuIFRpY2tldC5FU1RBRE9fQ0VSUkFETwogICAgaWYgYW55KGsgaW4gcyBmb3IgayBpbiAoIlBST0NFUyIsICJQUk9HUkVTUyIsICJQUlVFQkEiLCAiRVNQRVJBIiwgIlBST1ZFRURPUiIsICJDVVJTTyIpKToKICAgICAgICByZXR1cm4gVGlja2V0LkVTVEFET19FTl9QUk9DRVNPCiAgICByZXR1cm4gVGlja2V0LkVTVEFET19BQklFUlRPCgoKZGVmIF9tYXBfcHJpb3JpZGFkKHJhdzogc3RyKSAtPiBzdHI6CiAgICBzID0gKHJhdyBvciAiIikudXBwZXIoKQogICAgaWYgIkFMVCIgaW4gcyBvciAiSElHSCIgaW4gczoKICAgICAgICByZXR1cm4gVGlja2V0LlBSSU9SSURBRF9BTFRBCiAgICBpZiAiQkFKIiBpbiBzIG9yICJMT1ciIGluIHM6CiAgICAgICAgcmV0dXJuIFRpY2tldC5QUklPUklEQURfQkFKQQogICAgcmV0dXJuIFRpY2tldC5QUklPUklEQURfTUVESUEKCgpkZWYgX3JlYWRfdGlja2V0c19kYXRhZnJhbWUodXBsb2FkZWRfZmlsZSkgLT4gcGQuRGF0YUZyYW1lOgogICAgbmFtZSA9ICh1cGxvYWRlZF9maWxlLm5hbWUgb3IgIiIpLmxvd2VyKCkKICAgIGlmIG5hbWUuZW5kc3dpdGgoKCIueGxzeCIsICIueGxzIikpOgogICAgICAgIHJldHVybiBub3JtYWxpemVfY29sdW1ucyhyZWFkX2RhdGFmcmFtZSh1cGxvYWRlZF9maWxlLCBhbGxfZGF0YV9zaGVldHM9VHJ1ZSkpCiAgICByZXR1cm4gbm9ybWFsaXplX2NvbHVtbnMocmVhZF9kYXRhZnJhbWUodXBsb2FkZWRfZmlsZSkpCgoKZGVmIGltcG9ydF90aWNrZXRzKHVzZXIsIHVwbG9hZGVkX2ZpbGUpIC0+IERhdGFJbXBvcnRCYXRjaDoKICAgIGRmID0gX3JlYWRfdGlja2V0c19kYXRhZnJhbWUodXBsb2FkZWRfZmlsZSkKICAgIHJlcXVpcmVfYW55KAogICAgICAgIGRmLAogICAgICAgIFsKICAgICAgICAgICAgWyJjb2RpZ28iLCAidGlja2V0IiwgImlkIiwgImZvbGlvIiwgIm5vX3RpY2tldCJdLAogICAgICAgICAgICBbInRpdHVsbyIsICJhc3VudG8iLCAiZGVzY3JpcGNpb24iLCAidGVtYSJdLAogICAgICAgIF0sCiAgICApCgogICAgZGVmIGhhbmRsZXIocm93OiBwZC5TZXJpZXMsIGVycm9yczogbGlzdFtzdHJdKToKICAgICAgICBjb2RpZ28gPSBwaWNrKHJvdywgImNvZGlnbyIsICJ0aWNrZXQiLCAiaWQiLCAiZm9saW8iLCAibm9fdGlja2V0IiwgImlkX3RpY2tldCIpCiAgICAgICAgdGl0dWxvID0gcGljayhyb3csICJ0aXR1bG8iLCAiYXN1bnRvIiwgImRlc2NyaXBjaW9uIiwgImRlc2NyaXBjaW9uX2NvcnRhIiwgInRlbWEiKQogICAgICAgIGlmIG5vdCBjb2RpZ28gb3Igbm90IHRpdHVsbzoKICAgICAgICAgICAgZXJyb3JzLmFwcGVuZCgiY29kaWdvIHkgdGl0dWxvIG9ibGlnYXRvcmlvcyIpCiAgICAgICAgICAgIHJldHVybiBOb25lCiAgICAgICAgIyBFdml0YXIgSURzIGZsb2F0ICIzNjguMCIKICAgICAgICBpZiBjb2RpZ28uZW5kc3dpdGgoIi4wIikgYW5kIGNvZGlnb1s6LTJdLmlzZGlnaXQoKToKICAgICAgICAgICAgY29kaWdvID0gY29kaWdvWzotMl0KICAgICAgICBlbnRpZGFkID0gTm9uZQogICAgICAgIGVudF9jb2RlID0gcGljayhyb3csICJlbnRpZGFkX2NvZGlnbyIsICJjbGllbnRlX2NvZGlnbyIsICJuaXQiKQogICAgICAgIGlmIGVudF9jb2RlOgogICAgICAgICAgICBlbnRpZGFkID0gRW50aWRhZC5vYmplY3RzLmZpbHRlcihjb2RpZ29fX2lleGFjdD1fc2x1Z19jb2RpZ28oZW50X2NvZGUpKS5maXJzdCgpCiAgICAgICAgdW5pZGFkX3JhdyA9IHBpY2socm93LCAidW5pZGFkX25lZ29jaW8iLCAidW5pZGFkIiwgImRlcGFydGFtZW50byIsICJhcmVhIiwgInNpc3RlbWEiKSBvciAiVEkiCiAgICAgICAgdW5pZGFkID0gX3Jlc29sdmVfdW5pZGFkKHVuaWRhZF9yYXcpCiAgICAgICAgaWYgdW5pZGFkIGlzIE5vbmU6CiAgICAgICAgICAgICMgRGVwYXJ0YW1lbnRvcyBpbnRlcm5vcyDihpIgVEkgcG9yIGRlZmVjdG8KICAgICAgICAgICAgdW5pZGFkLCBfID0gVW5pZGFkTmVnb2Npby5vYmplY3RzLmdldF9vcl9jcmVhdGUoCiAgICAgICAgICAgICAgICBjb2RlPSJUSSIsCiAgICAgICAgICAgICAgICBkZWZhdWx0cz17Im5vbWJyZSI6ICJUZWNub2xvZ8OtYSAvIFRJIiwgImFjdGl2YSI6IFRydWV9LAogICAgICAgICAgICApCiAgICAgICAgYXNpZ25hZG8gPSBOb25lCiAgICAgICAgdXNlcm5hbWUgPSBwaWNrKHJvdywgImFzaWduYWRvIiwgImFzaWduYWRvX2EiLCAicmVzcG9uc2FibGUiLCAidGVjbmljbyIsICJhZ2VudGUiLCAiZXN0YWRvMiIpCiAgICAgICAgaWYgdXNlcm5hbWUgYW5kIHVzZXJuYW1lLmxvd2VyKCkgbm90IGluICgic2luIGFzaWduYXJzZSIsICJzaW4gYXNpZ25hciIsICJub25lIiwgIm5hbiIpOgogICAgICAgICAgICBmaXJzdCA9IHVzZXJuYW1lLnNwbGl0KClbMF0KICAgICAgICAgICAgYXNpZ25hZG8gPSBVc2VyLm9iamVjdHMuZmlsdGVyKHVzZXJuYW1lX19pZXhhY3Q9Zmlyc3QpLmZpcnN0KCkKICAgICAgICAgICAgaWYgbm90IGFzaWduYWRvOgogICAgICAgICAgICAgICAgYXNpZ25hZG8gPSBVc2VyLm9iamVjdHMuZmlsdGVyKGZpcnN0X25hbWVfX2ljb250YWlucz1maXJzdCkuZmlyc3QoKQogICAgICAgIGZlY2hhX2FwZXJ0dXJhID0gKAogICAgICAgICAgICBfcGFyc2VfZHQocGljayhyb3csICJmZWNoYV9hcGVydHVyYSIsICJmZWNoYV9jcmVhY2lvbiIsICJjcmVhZG8iLCAiYXBlcnR1cmEiLCAiZmVjaGFfcmVnaXN0cm8iKSkKICAgICAgICAgICAgb3IgdGltZXpvbmUubm93KCkKICAgICAgICApCiAgICAgICAgZmVjaGFfY2llcnJlID0gX3BhcnNlX2R0KHBpY2socm93LCAiZmVjaGFfY2llcnJlIiwgImNlcnJhZG8iLCAiZmVjaGFfcmVzb2x1Y2lvbiIpKQogICAgICAgIGVzdGFkbyA9IF9tYXBfZXN0YWRvKHBpY2socm93LCAiZXN0YWRvIiwgInN0YXR1cyIsICJlc3RhZG9fdGlja2V0IikpCiAgICAgICAgaWYgZmVjaGFfY2llcnJlIGFuZCBlc3RhZG8gPT0gVGlja2V0LkVTVEFET19BQklFUlRPOgogICAgICAgICAgICAjIFJlY2hhemFkby9SZXN1ZWx0byBjb24gZmVjaGEgZGUgY2llcnJlIOKGkiBjZXJyYWRvCiAgICAgICAgICAgIGlmIGFueShrIGluIHBpY2socm93LCAiZXN0YWRvIikudXBwZXIoKSBmb3IgayBpbiAoIlJFQ0hBWiIsICJSRVNVRUwiLCAiQ0VSUiIpKToKICAgICAgICAgICAgICAgIGVzdGFkbyA9IFRpY2tldC5FU1RBRE9fQ0VSUkFETwogICAgICAgIGR1cmFjaW9uID0gcGljayhyb3csICJkdXJhY2lvbiIpCiAgICAgICAgc2xhID0gcGlja19pbnQocm93LCAic2xhX2hvcmFzIiwgInNsYSIsIGRlZmF1bHQ9NDgpCiAgICAgICAgaWYgZHVyYWNpb246CiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgICMgRHVyYWNpw7NuIGVuIGhvcmFzIGRlbCBhcmNoaXZvIGhlbHBkZXNrOyBTTEEgPSBtYXgoNDgsIGNlaWwoZHVyYWNpb24qMS4yKSkKICAgICAgICAgICAgICAgIGQgPSBmbG9hdChzdHIoZHVyYWNpb24pLnJlcGxhY2UoIiwiLCAiLiIpKQogICAgICAgICAgICAgICAgaWYgZCA+IDA6CiAgICAgICAgICAgICAgICAgICAgc2xhID0gbWF4KHNsYSwgaW50KGQpICsgOCkKICAgICAgICAgICAgZXhjZXB0IFZhbHVlRXJyb3I6CiAgICAgICAgICAgICAgICBwYXNzCiAgICAgICAgZGVzY3JpcGNpb24gPSBwaWNrKHJvdywgImRlc2NyaXBjaW9uIiwgImRldGFsbGUiLCAibm90YXMiLCAic29sdWNpb24iKQogICAgICAgIHNvbGljaXRhbnRlID0gcGljayhyb3csICJ1c3VhcmlvX3NvbGljaXRhIiwgInNvbGljaXRhbnRlIikKICAgICAgICBpZiBzb2xpY2l0YW50ZToKICAgICAgICAgICAgZGVzY3JpcGNpb24gPSBmIlNvbGljaXRhOiB7c29saWNpdGFudGV9XG57ZGVzY3JpcGNpb259Ii5zdHJpcCgpCiAgICAgICAgXywgY3JlYXRlZCA9IFRpY2tldC5vYmplY3RzLnVwZGF0ZV9vcl9jcmVhdGUoCiAgICAgICAgICAgIGNvZGlnbz1zdHIoY29kaWdvKSwKICAgICAgICAgICAgZGVmYXVsdHM9ewogICAgICAgICAgICAgICAgInRpdHVsbyI6IHRpdHVsb1s6MjAwXSwKICAgICAgICAgICAgICAgICJkZXNjcmlwY2lvbiI6IGRlc2NyaXBjaW9uLAogICAgICAgICAgICAgICAgImVudGlkYWQiOiBlbnRpZGFkLAogICAgICAgICAgICAgICAgInVuaWRhZF9uZWdvY2lvIjogdW5pZGFkLAogICAgICAgICAgICAgICAgImVzdGFkbyI6IGVzdGFkbywKICAgICAgICAgICAgICAgICJwcmlvcmlkYWQiOiBfbWFwX3ByaW9yaWRhZChwaWNrKHJvdywgInByaW9yaWRhZCIsICJwcmlvcmlkYWRfdGlja2V0IikpLAogICAgICAgICAgICAgICAgImFzaWduYWRvX2EiOiBhc2lnbmFkbywKICAgICAgICAgICAgICAgICJmZWNoYV9hcGVydHVyYSI6IGZlY2hhX2FwZXJ0dXJhLAogICAgICAgICAgICAgICAgImZlY2hhX2NpZXJyZSI6IGZlY2hhX2NpZXJyZSwKICAgICAgICAgICAgICAgICJzbGFfaG9yYXMiOiBzbGEsCiAgICAgICAgICAgIH0sCiAgICAgICAgKQogICAgICAgIHJldHVybiBjcmVhdGVkLCBub3QgY3JlYXRlZAoKICAgIHVwbG9hZGVkX2ZpbGUuc2VlaygwKQoKICAgICMgcnVuX2ltcG9ydF9iYXRjaCByZS1sZWUgZWwgYXJjaGl2bzsgcGFyYSBtdWx0aS1ob2phIHVzYW1vcyBoYW5kbGVyIHNvYnJlIGRmIHlhIGxlw61kbwogICAgYmF0Y2ggPSBEYXRhSW1wb3J0QmF0Y2gub2JqZWN0cy5jcmVhdGUoCiAgICAgICAgbW9kdWxvPURhdGFJbXBvcnRCYXRjaC5NT0RVTE9fUEdPLAogICAgICAgIHRpcG9faW1wb3J0YWNpb249InRpY2tldHMiLAogICAgICAgIGFyY2hpdm9fbm9tYnJlPXVwbG9hZGVkX2ZpbGUubmFtZSwKICAgICAgICB1cGxvYWRlZF9ieT11c2VyLAogICAgICAgIHN0YXR1cz1EYXRhSW1wb3J0QmF0Y2guU1RBVFVTX1BFTkRJTkcsCiAgICAgICAgZmlsYXNfbGVpZGFzPWxlbihkZiksCiAgICApCiAgICBsb2dzOiBsaXN0W3N0cl0gPSBbXQogICAgZm9yIGlkeCwgcm93IGluIGRmLml0ZXJyb3dzKCk6CiAgICAgICAgcm93X2Vycm9yczogbGlzdFtzdHJdID0gW10KICAgICAgICB0cnk6CiAgICAgICAgICAgIHJlc3VsdCA9IGhhbmRsZXIocm93LCByb3dfZXJyb3JzKQogICAgICAgICAgICBpZiByb3dfZXJyb3JzOgogICAgICAgICAgICAgICAgYmF0Y2guZXJyb3JlcyArPSAxCiAgICAgICAgICAgICAgICBsb2dzLmFwcGVuZChmIkZpbGEge2lkeCArIDJ9OiB7JzsgJy5qb2luKHJvd19lcnJvcnMpfSIpCiAgICAgICAgICAgIGVsaWYgcmVzdWx0OgogICAgICAgICAgICAgICAgY3JlYXRlZCwgdXBkYXRlZCA9IHJlc3VsdAogICAgICAgICAgICAgICAgaWYgY3JlYXRlZDoKICAgICAgICAgICAgICAgICAgICBiYXRjaC5jcmVhZG9zICs9IDEKICAgICAgICAgICAgICAgIGlmIHVwZGF0ZWQ6CiAgICAgICAgICAgICAgICAgICAgYmF0Y2guYWN0dWFsaXphZG9zICs9IDEKICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGV4YzoKICAgICAgICAgICAgYmF0Y2guZXJyb3JlcyArPSAxCiAgICAgICAgICAgIGxvZ3MuYXBwZW5kKGYiRmlsYSB7aWR4ICsgMn06IHtleGN9IikKICAgIGlmIGJhdGNoLmVycm9yZXMgPT0gMDoKICAgICAgICBiYXRjaC5zdGF0dXMgPSBEYXRhSW1wb3J0QmF0Y2guU1RBVFVTX09LCiAgICBlbGlmIGJhdGNoLmNyZWFkb3MgKyBiYXRjaC5hY3R1YWxpemFkb3MgPiAwOgogICAgICAgIGJhdGNoLnN0YXR1cyA9IERhdGFJbXBvcnRCYXRjaC5TVEFUVVNfUEFSVElBTAogICAgZWxzZToKICAgICAgICBiYXRjaC5zdGF0dXMgPSBEYXRhSW1wb3J0QmF0Y2guU1RBVFVTX0VSUk9SCiAgICBiYXRjaC5sb2dfdGV4dG8gPSAiXG4iLmpvaW4obG9ncylbOjgwMDBdCiAgICBiYXRjaC5zYXZlKCkKICAgIHJldHVybiBiYXRjaAoKCmRlZiBpbXBvcnRfYXJjaGl2b3NfY2F0YWxvZ28odXNlciwgdXBsb2FkZWRfZmlsZSkgLT4gRGF0YUltcG9ydEJhdGNoOgogICAgIiIiCiAgICBDYXTDoWxvZ28gZGUgYXJjaGl2b3MgUEdPIOKAlCBzb2xvIHJlZ2lzdHJhIGxvdGUgKHNpbiBjcmVhciB0aWNrZXRzKS4KICAgICIiIgogICAgZnJvbSBjb3JlLndjZ19tb2RlbHMgaW1wb3J0IERhdGFJbXBvcnRCYXRjaCBhcyBCYXRjaAoKICAgIGRmID0gbm9ybWFsaXplX2NvbHVtbnMocmVhZF9kYXRhZnJhbWUodXBsb2FkZWRfZmlsZSkpCiAgICBiYXRjaCA9IEJhdGNoLm9iamVjdHMuY3JlYXRlKAogICAgICAgIG1vZHVsbz1CYXRjaC5NT0RVTE9fUEdPLAogICAgICAgIHRpcG9faW1wb3J0YWNpb249ImFyY2hpdm9zX2NhdGFsb2dvIiwKICAgICAgICBhcmNoaXZvX25vbWJyZT11cGxvYWRlZF9maWxlLm5hbWUsCiAgICAgICAgdXBsb2FkZWRfYnk9dXNlciwKICAgICAgICBmaWxhc19sZWlkYXM9bGVuKGRmKSwKICAgICAgICBzdGF0dXM9QmF0Y2guU1RBVFVTX09LLAogICAgICAgIGxvZ190ZXh0bz1mIkNhdMOhbG9nbyBsZcOtZG8gKHtsZW4oZGYpfSBmaWxhcykuIFNpbiBjYXJnYSBhIHRpY2tldHMuIiwKICAgICkKICAgIHJldHVybiBiYXRjaAo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgo/tests.py
PATH_JSON="pgo/tests.py"
FILENAME=tests.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=3
SIZE_BYTES_UTF8=60
CONTENT_SHA256=9ab6c6191360e63c1b4c9b5659aef348a743c9e078be68190917369e4e9563e8
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~python
from django.test import TestCase

# Create your tests here.

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.test import TestCase
00002|
00003|# Create your tests here.

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28udGVzdCBpbXBvcnQgVGVzdENhc2UKCiMgQ3JlYXRlIHlvdXIgdGVzdHMgaGVyZS4K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
