"""
Puntos PGC modo 2.Proporción alineados a la hoja Objetivos (autor).

Ver docs/pgc-puntos-proporcion-objetivos.md
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

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


def ingresos_points_objetivos(
    target,
    source_result,
    *,
    une_code: str,
) -> tuple[Decimal, bool, str]:
    """
    Ingresos: proporción en GTQ (excepción documentada) si hay presupuesto_gtq
    y source_value GTQ; si no, fallback miles USD medido/meta.
    """
    full = Decimal(str(target.points_if_achieved or 0))
    target_value = getattr(target, "target_value", None)
    pres_gtq = getattr(target, "presupuesto_gtq", None)
    exec_gtq = None
    if source_result and getattr(source_result, "source_currency", "") == "GTQ":
        exec_gtq = source_result.source_value

    # Convención hoja Objetivos: presupuesto GTQ ≈ meta (miles) × 1000 cuando no hay campo explícito.
    if (pres_gtq is None or pres_gtq <= 0) and target_value is not None:
        try:
            tv = Decimal(str(target_value))
            if tv > 0:
                pres_gtq = tv * Decimal("1000")
        except Exception:
            pass

    if pres_gtq and exec_gtq is not None and pres_gtq > 0:
        if exec_gtq < 0:
            return (
                Decimal("0"),
                False,
                "Objetivos ingresos (GTQ): ejecución negativa → 0 puntos.",
            )
        ratio = _cap_ratio(Decimal(str(exec_gtq)), Decimal(str(pres_gtq)))
        pts = (full * ratio).quantize(POINTS_QUANTIZE, rounding=ROUND_HALF_UP)
        achieved = ratio >= Decimal("1")
        return (
            pts,
            achieved,
            f"Objetivos ingresos (GTQ): {full}×min(1,{exec_gtq}/{pres_gtq})={pts}.",
        )

    measured = source_result.measured_value if source_result else None
    pts, achieved, note = proportional_points(
        full,
        measured,
        target_value,
        note_prefix="Objetivos ingresos (USD miles fallback)",
    )
    return pts, achieved, note


INSURANCE_REQS_GRACE_NOTE = (
    "Insurance: se otorgan puntos de respuesta a requerimientos de forma provisional "
    "(sin penalización) mientras no exista información completa ni un esquema de "
    "evaluación equivalente al de otras UNE; la hoja Objetivos marca «NO APLICA»."
)


def insurance_reqs_uses_grace_points(une_code: str, points_awarded) -> bool:
    return (une_code or "").upper() == UNE.CODE_INSURANCE and Decimal(
        str(points_awarded or 0)
    ) > 0
