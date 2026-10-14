"""Exportar / comparar baseline PGC para regresión de imports operativos."""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Any

from django.conf import settings

from core.models import MetricDefinition
from pgc.models import (
    MonthlyMetricResult,
    MonthlyMetricScore,
    MonthlyModeScorecard,
    PGCPlan,
)

BASELINE_VERSION = 1
DEFAULT_BASELINE_DIR = Path(settings.BASE_DIR) / "pgc" / "fixtures" / "baselines"


def _dec(val) -> str | None:
    if val is None:
        return None
    return str(val)


def _from_dec(s) -> Decimal | None:
    if s is None:
        return None
    return Decimal(str(s))


def export_period_baseline(
    *,
    tag: str,
    year: int,
    month: int,
    mode: str = "modo2",
) -> dict[str, Any]:
    plan = PGCPlan.objects.get(year=year)
    payload: dict[str, Any] = {
        "version": BASELINE_VERSION,
        "tag": tag,
        "year": year,
        "month": month,
        "mode": mode,
        "plan_year": plan.year,
        "results": [],
        "metric_scores": [],
        "mode_scorecards": [],
    }

    results = MonthlyMetricResult.objects.filter(
        plan=plan, year=year, month=month
    ).select_related("une", "metric")
    for r in results.order_by("une__sort_order", "metric__code"):
        payload["results"].append(
            {
                "une": r.une.code,
                "metric": r.metric.code,
                "measured_value": _dec(r.measured_value),
                "source_value": _dec(r.source_value),
                "source_currency": r.source_currency or "",
                "target_value": _dec(r.target_value),
                "is_achieved": r.is_achieved,
                "points_awarded": r.points_awarded,
            }
        )

    scores = MonthlyMetricScore.objects.filter(
        plan=plan, year=year, month=month, mode=mode
    ).select_related("une", "metric")
    for s in scores.order_by("une__sort_order", "metric__code"):
        payload["metric_scores"].append(
            {
                "une": s.une.code,
                "metric": s.metric.code,
                "measured_value": _dec(s.measured_value),
                "target_value": _dec(s.target_value),
                "points_awarded": _dec(s.points_awarded),
                "is_achieved": s.is_achieved,
            }
        )

    cards = MonthlyModeScorecard.objects.filter(
        plan=plan, year=year, month=month, mode=mode
    ).select_related("une")
    for c in cards.order_by("une__sort_order"):
        payload["mode_scorecards"].append(
            {
                "une": c.une.code,
                "total_points": _dec(c.total_points),
                "is_month_qualified": c.is_month_qualified,
            }
        )

    return payload


def baseline_path(tag: str, year: int, month: int) -> Path:
    return DEFAULT_BASELINE_DIR / f"{tag}-{year}-{month:02d}.json"


def save_baseline_file(payload: dict[str, Any], path: Path | None = None) -> Path:
    path = path or baseline_path(payload["tag"], payload["year"], payload["month"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def load_baseline_file(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def compare_period_to_baseline(
    *,
    baseline: dict[str, Any],
    year: int,
    month: int,
    mode: str = "modo2",
    plan_year: int | None = None,
) -> list[dict[str, Any]]:
    plan = PGCPlan.objects.get(year=plan_year or baseline.get("plan_year") or year)
    diffs: list[dict[str, Any]] = []

    def _key(une: str, metric: str) -> tuple[str, str]:
        return (une, metric)

    expected_results = {
        _key(r["une"], r["metric"]): r for r in baseline.get("results", [])
    }
    actual_results = MonthlyMetricResult.objects.filter(
        plan=plan, year=year, month=month
    ).select_related("une", "metric")
    for r in actual_results:
        k = _key(r.une.code, r.metric.code)
        exp = expected_results.get(k)
        if not exp:
            diffs.append({"kind": "result_extra", "une": k[0], "metric": k[1]})
            continue
        for field in ("measured_value", "source_value"):
            ev = _from_dec(exp.get(field))
            av = r.measured_value if field == "measured_value" else r.source_value
            if ev is None and av is None:
                continue
            if ev is None or av is None or ev != av:
                diffs.append(
                    {
                        "kind": "result",
                        "une": k[0],
                        "metric": k[1],
                        "field": field,
                        "expected": exp.get(field),
                        "actual": _dec(av),
                    }
                )

    expected_scores = {
        _key(s["une"], s["metric"]): s for s in baseline.get("metric_scores", [])
    }
    actual_scores = MonthlyMetricScore.objects.filter(
        plan=plan, year=year, month=month, mode=mode
    ).select_related("une", "metric")
    for s in actual_scores:
        k = _key(s.une.code, s.metric.code)
        exp = expected_scores.get(k)
        if not exp:
            diffs.append({"kind": "score_extra", "une": k[0], "metric": k[1]})
            continue
        ev = _from_dec(exp.get("points_awarded"))
        if ev is None or s.points_awarded != ev:
            diffs.append(
                {
                    "kind": "score_points",
                    "une": k[0],
                    "metric": k[1],
                    "expected": exp.get("points_awarded"),
                    "actual": _dec(s.points_awarded),
                }
            )

    expected_cards = {c["une"]: c for c in baseline.get("mode_scorecards", [])}
    actual_cards = MonthlyModeScorecard.objects.filter(
        plan=plan, year=year, month=month, mode=mode
    ).select_related("une")
    for c in actual_cards:
        exp = expected_cards.get(c.une.code)
        if not exp:
            diffs.append({"kind": "card_extra", "une": c.une.code})
            continue
        ev = _from_dec(exp.get("total_points"))
        if ev is None or c.total_points != ev:
            diffs.append(
                {
                    "kind": "card_total",
                    "une": c.une.code,
                    "expected": exp.get("total_points"),
                    "actual": _dec(c.total_points),
                }
            )

    return diffs


def clear_sep_operational_results(plan: PGCPlan, year: int, month: int) -> None:
    """Borra resultados operativos del mes (no metas ni TC)."""
    codes = (
        MetricDefinition.CODE_INGRESOS,
        MetricDefinition.CODE_CLIENTES_NUEVOS,
        MetricDefinition.CODE_VENTA_CRUZADA,
    )
    metrics = MetricDefinition.objects.filter(code__in=codes)
    MonthlyMetricResult.objects.filter(
        plan=plan, year=year, month=month, metric__in=metrics
    ).delete()
