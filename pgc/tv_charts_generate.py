"""
Generación server-side de wcg-g1..g4.png (misma lógica que Exportación 4 charts).

Se refrescan cuando cambian ingresos/meta YTD, tras import/recalc, al servir /tv/* si
hay desfase, y como máximo una vez por hora al abrir el tablero (sesión).
"""

from __future__ import annotations

import hashlib
import io
import logging
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from django.db import transaction
from django.utils import timezone

from core.models import MetricDefinition, SystemSetting
from pgc.models import MonthlyMetricResult, PGCPlan
from pgc.tv_charts import write_live_bytes

logger = logging.getLogger(__name__)

PGC_TV_CHARTS_FINGERPRINT_KEY = "pgc.tv_charts.ingresos_fingerprint"
PGC_TV_CHARTS_GENERATED_AT_KEY = "pgc.tv_charts.generated_at"

UNE_FACTORING = "FACTORING"
UNE_LEASING = "LEASING"
UNE_INSURANCE = "INSURANCE"

EXPORT_SUBTITLE = (
    "Real vs meta por período. Cifras acumuladas dentro del rango."
)
Y_AXIS_DEFAULT = "Cifras en miles de US$"

TV_CHART_CONFIGS: tuple[dict, ...] = (
    {"slot": 1, "title": "FACTORING", "une_codes": (UNE_FACTORING,)},
    {"slot": 2, "title": "LEASING", "une_codes": (UNE_LEASING,)},
    {"slot": 3, "title": "INSURANCE", "une_codes": (UNE_INSURANCE,)},
    {
        "slot": 4,
        "title": "GRUPO",
        "une_codes": (UNE_FACTORING, UNE_LEASING, UNE_INSURANCE),
    },
)

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
COLOR_TEXT = "#3D3F3F"
COLOR_REAL = "#1D284A"
COLOR_META = "#010202"

_refresh_lock = threading.Lock()
_refresh_scheduled = False


@dataclass(frozen=True)
class ExportPeriod:
    year: int
    month: int
    label: str
    by_une: dict[str, dict[str, float]]


def _active_plan() -> PGCPlan | None:
    plan = PGCPlan.objects.filter(is_active=True).order_by("-year").first()
    if plan:
        return plan
    return PGCPlan.objects.order_by("-year").first()


def get_tv_ytd_export_context(now: datetime | None = None) -> tuple[list[tuple[int, int]], str]:
    """Enero → mes anterior al calendario (misma regla que tablero por defecto)."""
    from pgc.views import (
        _build_ytd_period_range,
        _period_range_end,
        get_default_month_count,
        get_default_report_start,
    )

    start_year, start_month = get_default_report_start(now)
    month_count = get_default_month_count(now)
    end_year, end_month = _period_range_end(start_year, start_month, month_count)
    periods = _build_ytd_period_range(end_year, end_month)
    return periods, f"{end_year}-{end_month:02d}"


def load_export_ingresos_periods(
    periods: Sequence[tuple[int, int]] | None = None,
) -> tuple[list[ExportPeriod], str]:
    from pgc.views import _build_dashboard_chart_payload

    if periods is None:
        periods, _ = get_tv_ytd_export_context()

    payload = _build_dashboard_chart_payload(periods=list(periods))
    block = (payload.get("metrics") or {}).get(MetricDefinition.CODE_INGRESOS) or {}
    raw_periods = block.get("periods") or []
    y_axis = block.get("y_axis") or Y_AXIS_DEFAULT

    out: list[ExportPeriod] = []
    for p in raw_periods:
        by_une = {}
        for code, item in (p.get("by_une") or {}).items():
            by_une[str(code)] = {
                "real": float(item.get("real") or 0),
                "target": float(item.get("target") or 0),
            }
        out.append(
            ExportPeriod(
                year=int(p["year"]),
                month=int(p["month"]),
                label=str(p.get("label") or f"{p['year']}-{p['month']:02d}"),
                by_une=by_une,
            )
        )
    return out, y_axis


def accumulate(values: Sequence[float]) -> list[float]:
    running = 0.0
    out: list[float] = []
    for v in values:
        running += float(v or 0)
        out.append(running)
    return out


def build_income_series(
    periods: Sequence[ExportPeriod],
    une_codes: Sequence[str],
) -> tuple[list[str], list[float], list[float]]:
    labels: list[str] = []
    reals: list[float] = []
    targets: list[float] = []
    for period in periods:
        labels.append(period.label)
        real_sum = 0.0
        target_sum = 0.0
        for code in une_codes:
            item = period.by_une.get(code) or {}
            real_sum += float(item.get("real") or 0)
            target_sum += float(item.get("target") or 0)
        reals.append(real_sum)
        targets.append(target_sum)
    return labels, accumulate(reals), accumulate(targets)


def compute_ingresos_fingerprint(
    periods: Sequence[tuple[int, int]] | None = None,
) -> str:
    """Huella de datos INGRESOS YTD (real, meta, updated_at por UNE/mes)."""
    if periods is None:
        periods, _ = get_tv_ytd_export_context()
    if not periods:
        return "empty"

    plan = _active_plan()
    metric = MetricDefinition.objects.filter(
        code=MetricDefinition.CODE_INGRESOS
    ).first()
    if not plan or not metric:
        return "no-plan"

    h = hashlib.sha256()
    period_q = None
    from pgc.views import _build_period_q

    period_q = _build_period_q(list(periods))
    une_codes = (UNE_FACTORING, UNE_LEASING, UNE_INSURANCE)

    for row in (
        MonthlyMetricResult.objects.filter(
            plan=plan,
            metric=metric,
        )
        .filter(period_q)
        .filter(une__code__in=une_codes)
        .select_related("une")
        .order_by("year", "month", "une__code")
        .values_list(
            "year",
            "month",
            "une__code",
            "measured_value",
            "target_value",
            "updated_at",
        )
    ):
        h.update(repr(row).encode("utf-8"))

    from pgc.models import MonthlyTarget

    for row in (
        MonthlyTarget.objects.filter(plan=plan, metric=metric)
        .filter(period_q)
        .filter(une__code__in=une_codes)
        .select_related("une")
        .order_by("year", "month", "une__code")
        .values_list(
            "year", "month", "une__code", "target_value", "updated_at"
        )
    ):
        h.update(repr(row).encode("utf-8"))

    h.update(repr(list(periods)).encode("utf-8"))
    return h.hexdigest()


def _stored_fingerprint() -> str:
    row = SystemSetting.objects.filter(key=PGC_TV_CHARTS_FINGERPRINT_KEY).first()
    return (row.value_text or "").strip() if row else ""


def _persist_generation_meta(fingerprint: str) -> None:
    now = timezone.now()
    SystemSetting.objects.update_or_create(
        key=PGC_TV_CHARTS_FINGERPRINT_KEY,
        defaults={
            "value_text": fingerprint,
            "description": "Huella YTD ingresos usada en charts TV vivos",
        },
    )
    SystemSetting.objects.update_or_create(
        key=PGC_TV_CHARTS_GENERATED_AT_KEY,
        defaults={
            "value_text": now.isoformat(),
            "description": "Última generación server-side wcg-g1..g4",
        },
    )


def render_chart_png(
    title: str,
    labels: Sequence[str],
    real_y: Sequence[float],
    target_y: Sequence[float],
    *,
    y_axis: str = Y_AXIS_DEFAULT,
) -> bytes:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter

    dpi = 100
    fig_w = IMAGE_WIDTH / dpi
    fig_h = IMAGE_HEIGHT / dpi
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)

    x = list(range(len(labels)))
    width = 0.55
    ax.bar(
        x,
        list(real_y),
        width=width,
        color=COLOR_REAL,
        label="Real",
        zorder=2,
    )
    ax.plot(
        x,
        list(target_y),
        color=COLOR_META,
        linewidth=3,
        linestyle=(0, (8, 6)),
        label="Meta",
        zorder=3,
    )

    ax.set_xticks(x)
    ax.set_xticklabels(list(labels), fontsize=11, color=COLOR_TEXT)
    ax.set_ylabel(y_axis, fontsize=12, color=COLOR_TEXT)
    ax.set_xlabel("Período", fontsize=12, color=COLOR_TEXT)
    ax.tick_params(axis="y", labelsize=11, colors=COLOR_TEXT)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:,.0f}"))
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", color="#e2e8f0", linewidth=1, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.suptitle(
        title,
        fontsize=22,
        fontweight="bold",
        color=COLOR_TEXT,
        y=0.96,
    )
    fig.text(
        0.5,
        0.915,
        EXPORT_SUBTITLE,
        ha="center",
        fontsize=11,
        color=COLOR_TEXT,
    )
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=2,
        frameon=False,
        fontsize=11,
    )
    fig.subplots_adjust(left=0.08, right=0.98, top=0.88, bottom=0.22)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor="white", edgecolor="none")
    plt.close(fig)
    return buf.getvalue()


def regenerate_tv_live_charts(*, force: bool = False) -> dict:
    """
    Escribe wcg-g1..g4.png en live/ + Postgres si la huella cambió o force=True.
    """
    periods, range_label = get_tv_ytd_export_context()
    fingerprint = compute_ingresos_fingerprint(periods)
    if not force and fingerprint == _stored_fingerprint():
        return {"ran": False, "reason": "up_to_date", "fingerprint": fingerprint}

    export_periods, y_axis = load_export_ingresos_periods(periods)
    if not export_periods:
        return {"ran": False, "reason": "no_data", "fingerprint": fingerprint}

    stamp = datetime.now().strftime("%y-%m-%d %H-%M")
    written: list[str] = []
    with _refresh_lock:
        for cfg in TV_CHART_CONFIGS:
            labels, real_y, target_y = build_income_series(
                export_periods, cfg["une_codes"]
            )
            png = render_chart_png(
                cfg["title"],
                labels,
                real_y,
                target_y,
                y_axis=y_axis,
            )
            name = write_live_bytes(cfg["slot"], "png", png, stamp=stamp)
            written.append(name)

        _persist_generation_meta(fingerprint)

    logger.info(
        "TV charts regenerated (%s, range=%s, files=%s)",
        fingerprint[:12],
        range_label,
        written,
    )
    return {
        "ran": True,
        "fingerprint": fingerprint,
        "files": written,
        "range": range_label,
    }


def charts_need_refresh() -> bool:
    fp = compute_ingresos_fingerprint()
    if fp != _stored_fingerprint():
        return True
    from pgc.tv_charts import live_path

    for cfg in TV_CHART_CONFIGS:
        path = live_path(cfg["slot"], "png")
        if not path.is_file() or path.stat().st_size == 0:
            return True
    return False


def ensure_tv_live_charts_current(*, force: bool = False) -> None:
    """Regenera si los vivos no coinciden con ingresos en BD."""
    try:
        if force or charts_need_refresh():
            regenerate_tv_live_charts(force=force)
    except Exception:
        logger.exception("ensure_tv_live_charts_current failed")


def schedule_tv_charts_refresh(*, reason: str = "") -> None:
    """Una sola corrida por ola de commits (import / recalc)."""
    global _refresh_scheduled

    def _run() -> None:
        global _refresh_scheduled
        try:
            ensure_tv_live_charts_current()
        finally:
            _refresh_scheduled = False

    with _refresh_lock:
        if _refresh_scheduled:
            return
        _refresh_scheduled = True

    conn = transaction.get_connection()
    if conn.in_atomic_block:
        transaction.on_commit(_run)
    else:
        _run()

    if reason:
        logger.debug("TV charts refresh scheduled (%s)", reason)

