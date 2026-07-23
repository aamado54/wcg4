"""
Recálculo simple de PgoPeriodScore desde PgoResultadoPeriodo + PgoMetricRule.

No replica el motor PGC: evalúa fórmulas parametrizables sobre métricas del
agregado operativo (SLA %, cerrados, abiertos, tiempo promedio) y guarda
puntaje_total + clasifica (umbral default 80).
"""

from __future__ import annotations

import re
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from apps.core.models import UnidadNegocio as WcgoneUnidad
from apps.pgo.models import PgoMetricRule, PgoPeriodScore

DEFAULT_QUALIFY_THRESHOLD = Decimal("80")
AREA_OPERACION = "operacion"

# Reglas sembradas solo si no hay ninguna activa (parametrizables vía admin).
DEFAULT_RULES = [
    {
        "codigo": "SLA_SCORE",
        "area": AREA_OPERACION,
        "variable": "sla_pct",
        "criterio": "Puntaje proporcional al % de cumplimiento SLA del período",
        "formula_texto": "sla_pct",
        "puntos": Decimal("100"),
        "peso": Decimal("1"),
        "tipo_regla": PgoMetricRule.TIPO_AUTOMATICA,
        "notas": "Default: puntaje = cumplimiento_sla_pct (0–100).",
    },
]


def _q2(value: Decimal | float | int | str) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def ensure_default_metric_rules() -> int:
    """Crea reglas default si el catálogo activo está vacío. Retorna creadas."""
    if PgoMetricRule.objects.filter(activo=True).exists():
        return 0
    created = 0
    for spec in DEFAULT_RULES:
        _, was_created = PgoMetricRule.objects.get_or_create(
            codigo=spec["codigo"],
            defaults={**spec, "activo": True},
        )
        if was_created:
            created += 1
    return created


def resolve_wcgone_unidad(core_unidad) -> WcgoneUnidad | None:
    """Mapea UnidadNegocio productiva (`code`) → wcgone (`codigo`), creando si falta."""
    if core_unidad is None:
        return None
    code = (getattr(core_unidad, "code", None) or getattr(core_unidad, "codigo", None) or "").strip()
    if not code:
        return None
    nombre = getattr(core_unidad, "nombre", None) or code
    obj, _ = WcgoneUnidad.objects.get_or_create(
        codigo=code.upper()[:30],
        defaults={"nombre": nombre, "activa": True, "orden": 0},
    )
    return obj


def _metrics_from_resultado(resultado) -> dict[str, Decimal]:
    return {
        "sla_pct": _q2(getattr(resultado, "cumplimiento_sla_pct", 0) or 0),
        "cerrados": Decimal(str(getattr(resultado, "tickets_cerrados", 0) or 0)),
        "abiertos": Decimal(str(getattr(resultado, "tickets_abiertos", 0) or 0)),
        "tiempo_promedio_horas": _q2(getattr(resultado, "tiempo_promedio_horas", 0) or 0),
    }


def _parse_threshold(formula: str, default: Decimal = Decimal("80")) -> Decimal:
    m = re.search(r">=\s*([0-9]+(?:\.[0-9]+)?)", formula)
    if m:
        return Decimal(m.group(1))
    return default


def evaluate_rule(rule: PgoMetricRule, metrics: dict[str, Decimal]) -> dict[str, Any]:
    """
    Evalúa una regla. Fórmulas soportadas (formula_texto, case-insensitive):

    - ``sla_pct`` → awarded = puntos * (sla_pct/100)
    - ``sla_pct >= N`` → awarded = puntos si sla_pct >= N, si no 0
    - ``cerrados >= N`` → awarded = puntos si cerrados >= N
    - ``actividad`` → awarded = puntos si cerrados+abiertos > 0
    - vacío + variable con ``sla`` → igual que ``sla_pct``

    ``peso`` escala el aporte: awarded_final = awarded * peso (peso default 1).
    """
    formula = (rule.formula_texto or "").strip().lower()
    variable = (rule.variable or "").strip().lower()
    puntos = Decimal(rule.puntos or 0)
    peso = Decimal(rule.peso if rule.peso is not None else 1)
    if peso < 0:
        peso = Decimal("0")

    sla = metrics.get("sla_pct", Decimal("0"))
    cerrados = metrics.get("cerrados", Decimal("0"))
    abiertos = metrics.get("abiertos", Decimal("0"))

    awarded_base = Decimal("0")
    note = ""
    passed = False

    if not formula and "sla" in variable:
        formula = "sla_pct"

    if formula in ("sla_pct", "sla", "cumplimiento_sla", "cumplimiento_sla_pct"):
        awarded_base = puntos * (sla / Decimal("100"))
        passed = True
        note = f"SLA {sla}% → {_q2(awarded_base)} pts"
    elif formula.startswith("sla_pct") and ">=" in formula:
        thr = _parse_threshold(formula)
        passed = sla >= thr
        awarded_base = puntos if passed else Decimal("0")
        note = f"SLA {sla}% {'≥' if passed else '<'} {thr} → {_q2(awarded_base)} pts"
    elif formula.startswith("cerrados") and ">=" in formula:
        thr = _parse_threshold(formula, Decimal("1"))
        passed = cerrados >= thr
        awarded_base = puntos if passed else Decimal("0")
        note = f"Cerrados {cerrados} {'≥' if passed else '<'} {thr} → {_q2(awarded_base)} pts"
    elif formula in ("actividad", "activity", "tiene_tickets"):
        passed = (cerrados + abiertos) > 0
        awarded_base = puntos if passed else Decimal("0")
        note = f"Actividad {'sí' if passed else 'no'} → {_q2(awarded_base)} pts"
    else:
        note = f"Fórmula no reconocida ({rule.formula_texto or 'vacía'}); aporte 0"
        passed = False
        awarded_base = Decimal("0")

    awarded = _q2(awarded_base * peso)
    return {
        "codigo": rule.codigo,
        "variable": rule.variable,
        "puntos": str(_q2(puntos)),
        "peso": str(_q2(peso)),
        "awarded": str(awarded),
        "passed": passed,
        "note": note,
    }


def _rules_for_unidad(wcgone_unidad: WcgoneUnidad | None):
    qs = PgoMetricRule.objects.filter(activo=True).exclude(
        tipo_regla=PgoMetricRule.TIPO_MANUAL
    )
    if wcgone_unidad:
        return qs.filter(
            Q(unidad_negocio__isnull=True) | Q(unidad_negocio=wcgone_unidad)
        ).order_by("area", "codigo")
    return qs.filter(unidad_negocio__isnull=True).order_by("area", "codigo")


def score_resultado(
    resultado,
    *,
    threshold: Decimal = DEFAULT_QUALIFY_THRESHOLD,
    rules: list[PgoMetricRule] | None = None,
) -> PgoPeriodScore:
    """Calcula y persiste un PgoPeriodScore para un PgoResultadoPeriodo."""
    wcgone_un = resolve_wcgone_unidad(resultado.unidad_negocio)
    metrics = _metrics_from_resultado(resultado)
    rule_list = list(rules) if rules is not None else list(_rules_for_unidad(wcgone_un))

    detalle_rules = []
    total = Decimal("0")
    for rule in rule_list:
        if rule.unidad_negocio_id and wcgone_un and rule.unidad_negocio_id != wcgone_un.id:
            continue
        if rule.unidad_negocio_id and wcgone_un is None:
            continue
        ev = evaluate_rule(rule, metrics)
        detalle_rules.append(ev)
        total += Decimal(ev["awarded"])

    total = _q2(total)
    clasifica = total >= threshold
    detalle = {
        "threshold": str(_q2(threshold)),
        "source": "PgoResultadoPeriodo",
        "periodo": resultado.periodo,
        "unidad_code": getattr(resultado.unidad_negocio, "code", None),
        "metrics": {k: str(v) for k, v in metrics.items()},
        "rules": detalle_rules,
        "puntaje_total": str(total),
        "clasifica": clasifica,
        "summary": "; ".join(r["note"] for r in detalle_rules if r.get("note"))[:400],
    }

    score = PgoPeriodScore.objects.filter(
        periodo=resultado.periodo,
        unidad_negocio=wcgone_un,
        area=AREA_OPERACION,
        usuario__isnull=True,
    ).first()
    if score is None:
        score = PgoPeriodScore(
            periodo=resultado.periodo,
            unidad_negocio=wcgone_un,
            area=AREA_OPERACION,
        )
    score.puntaje_total = total
    score.clasifica = clasifica
    score.detalle_json = detalle
    score.fecha_calculo = timezone.now()
    score.save()
    return score


@transaction.atomic
def recalculate_pgo_scores(
    periodo: str | None = None,
    *,
    threshold: Decimal = DEFAULT_QUALIFY_THRESHOLD,
    ensure_rules: bool = True,
) -> dict[str, Any]:
    """Recalcula PgoPeriodScore desde PgoResultadoPeriodo (opción filtrar período)."""
    from pgo.models import PgoResultadoPeriodo
    from pgo.periodo import recalculate_pgo_periodos

    recalculate_pgo_periodos(periodo=periodo)
    rules_created = ensure_default_metric_rules() if ensure_rules else 0

    qs = PgoResultadoPeriodo.objects.select_related("unidad_negocio").order_by(
        "-periodo", "unidad_negocio__code"
    )
    if periodo:
        qs = qs.filter(periodo=periodo)

    scores: list[PgoPeriodScore] = []
    for resultado in qs:
        scores.append(score_resultado(resultado, threshold=threshold))

    return {
        "periodos_fuente": qs.count(),
        "scores_escritos": len(scores),
        "rules_created": rules_created,
        "threshold": threshold,
        "scores": scores,
    }


def period_scores_for_dashboard(limit: int = 40):
    """Queryset listo para la tabla de resultados del dashboard."""
    return (
        PgoPeriodScore.objects.select_related("unidad_negocio")
        .filter(area=AREA_OPERACION)
        .order_by("-periodo", "unidad_negocio__codigo")[:limit]
    )


def brief_detalle(score: PgoPeriodScore) -> str:
    data = score.detalle_json or {}
    if isinstance(data, dict):
        summary = data.get("summary") or ""
        if summary:
            return str(summary)[:160]
        metrics = data.get("metrics") or {}
        sla = metrics.get("sla_pct")
        if sla is not None:
            return f"SLA {sla}%"
    return ""
