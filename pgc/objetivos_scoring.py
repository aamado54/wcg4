"""
Puntos PGC modo 2.Proporción — ingresos alineados al reporte Ingresos vs meta (miles USD).

Ver docs/pgc-puntos-proporcion-objetivos.md (histórico GTQ obsoleto para scoring).
"""

from __future__ import annotations

from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP

from core.money_precision import MONEY_STORE_PLACES, quantize_store
from core.models import MetricDefinition, UNE

POINTS_QUANTIZE = Decimal("0.01")


def _cap_ratio(numerator: Decimal, denominator: Decimal) -> Decimal:
    if denominator is None or denominator <= 0 or numerator is None:
        return Decimal("0")
    ratio = numerator / denominator
    if ratio < 0:
        return Decimal("0")
    if ratio > 1:
        return Decimal("1")
    return ratio


def proportional_points(
    points_if_achieved: int | Decimal,
    measured,
    target,
    *,
    note_prefix: str = "Objetivos proporción",
) -> tuple[Decimal, bool, str]:
    """
    Puntos = points_if × min(1, medido/meta) para conteos o unidades homogéneas.
    """
    full = Decimal(str(points_if_achieved or 0))
    if full <= 0:
        return Decimal("0"), False, f"{note_prefix}: sin puntos en meta."
    if measured is None or target is None:
        return Decimal("0"), False, f"{note_prefix}: falta medido o meta."
    try:
        m = Decimal(str(measured))
        t = Decimal(str(target))
    except Exception:
        return Decimal("0"), False, f"{note_prefix}: valores no numéricos."
    if t <= 0:
        return Decimal("0"), False, f"{note_prefix}: meta ≤ 0."
    ratio = _cap_ratio(m, t)
    pts = (full * ratio).quantize(POINTS_QUANTIZE, rounding=ROUND_HALF_UP)
    achieved = ratio >= Decimal("1")
    return (
        pts,
        achieved,
        f"{note_prefix}: {full}×min(1,{m}/{t})={pts}.",
    )


def clientes_points_objetivos(
    target,
    measured,
) -> tuple[Decimal, bool, str]:
    """
    Clientes nuevos: proporción habitual; si presupuesto ≤ 0 y ejecución 0, la hoja
    otorga los puntos completos (único caso documentado: WCL ene-2026).
    """
    full = Decimal(str(target.points_if_achieved or 0))
    target_value = getattr(target, "target_value", None)
    try:
        t = Decimal(str(target_value)) if target_value is not None else Decimal("0")
        m = Decimal(str(measured)) if measured is not None else Decimal("0")
    except Exception:
        t = Decimal("0")
        m = Decimal("0")
    if full > 0 and t <= 0 and m <= 0:
        return (
            full.quantize(POINTS_QUANTIZE, rounding=ROUND_HALF_UP),
            True,
            "Objetivos clientes: presupuesto≤0 y ejecución 0 → puntos completos (hoja).",
        )
    return proportional_points(
        full,
        measured,
        target_value,
        note_prefix="Objetivos clientes",
    )


def _ingresos_max_points(une_code: str, points_if_achieved) -> Decimal:
    """Factoraje, Leasing e Insurance: tope 70 pt en Proporción (ingresos vs meta)."""
    full = Decimal(str(points_if_achieved or 0))
    if (une_code or "").upper() in (
        UNE.CODE_FACTORING,
        UNE.CODE_LEASING,
        UNE.CODE_INSURANCE,
    ):
        return min(full, Decimal("70"))
    return full


def _ingresos_vs_meta_inputs(
    measured, target, *, une_code: str
) -> tuple[Decimal | None, Decimal | None]:
    """
    Mismas magnitudes que el reporte Ingresos vs meta (miles USD).
    Insurance trunca meta y ejecutado a 3 decimales (ROUND_DOWN), como en la vista.
    """
    if measured is None or target is None:
        return None, None
    try:
        m = Decimal(str(measured))
        t = Decimal(str(target))
    except Exception:
        return None, None
    if (une_code or "").upper() == UNE.CODE_INSURANCE:
        q = Decimal("0.001")
        m = m.quantize(q, rounding=ROUND_DOWN)
        t = t.quantize(q, rounding=ROUND_DOWN)
    else:
        m = quantize_store(m, places=MONEY_STORE_PLACES) or m
        t = quantize_store(t, places=MONEY_STORE_PLACES) or t
    return m, t


def ingresos_points_objetivos(
    target,
    source_result,
    *,
    une_code: str,
    year: int | None = None,
    month: int | None = None,
) -> tuple[Decimal, bool, str]:
    """
    Ingresos (Proporción): mismos valores que el reporte Ingresos vs meta — ejecutado y meta
    en miles US$, proporcional con tope 70 en F/L/I.
    """
    from pgc.investment_ingresos import investment_net_growth_miles

    full = _ingresos_max_points(une_code, target.points_if_achieved)
    target_value = getattr(target, "target_value", None)

    measured = source_result.measured_value if source_result else None
    if (une_code or "").upper() in {UNE.CODE_INVESTMENT, "INVESTMENTS", "INVERSIONES"}:
        if year is not None and month is not None:
            growth = investment_net_growth_miles(year, month)
            if growth is not None:
                measured = growth

    measured, target_value = _ingresos_vs_meta_inputs(
        measured, target_value, une_code=une_code
    )

    pts, achieved, note = proportional_points(
        full,
        measured,
        target_value,
        note_prefix="Ingresos vs meta (miles USD)",
    )
    return pts, achieved, note


INSURANCE_REQS_GRACE_NOTE = (
    "Insurance: se otorgan puntos de respuesta a requerimientos de forma provisional "
    "(sin penalización) mientras no exista información completa ni un esquema de "
    "evaluación equivalente al de otras UNE; la hoja Objetivos marca «NO APLICA»."
)


def insurance_reqs_grace_applies(une_code: str) -> bool:
    """Insurance: siempre cumple reqs con puntos provisionales (hoja marca NO APLICA)."""
    return (une_code or "").upper() == UNE.CODE_INSURANCE


def insurance_reqs_uses_grace_points(une_code: str, points_awarded) -> bool:
    return insurance_reqs_grace_applies(une_code) and Decimal(
        str(points_awarded or 0)
    ) > 0


def resolve_respuesta_reqs_compliance(une_code: str, manual=None) -> tuple[bool, str]:
    """
    Fuente única para scoring y reporte «Respuesta reqs real» (meta binaria 1).
    - Insurance: grace (cumple aunque Excel/MRC diga no).
    - Sin ManualRequirementsCompliance: asume cumple.
    - Con registro manual: respeta is_compliant.
    """
    if insurance_reqs_grace_applies(une_code):
        return True, "insurance_grace"
    if manual is None:
        return True, "default_sin_registro"
    if manual.is_compliant:
        return True, "manual_compliant"
    return False, "manual_non_compliant"


def respuesta_reqs_points_awarded(une_code, year, month, points_if, is_compliant) -> Decimal:
    """
    Puntos de respuesta a reqs.
    Insurance: 5 en todos los meses. Investment oct-2026: igual (5), aunque la meta diga 0.
    """
    if not is_compliant:
        return Decimal("0")
    pts = Decimal(str(points_if or 0))
    code = (une_code or "").upper()
    if code == UNE.CODE_INSURANCE and pts < Decimal("5"):
        pts = Decimal("5")
    if (
        code in {UNE.CODE_INVESTMENT, "INVESTMENTS", "INVERSIONES"}
        and int(year or 0) == 2026
        and int(month or 0) == 10
        and pts < Decimal("5")
    ):
        pts = Decimal("5")
    return pts
