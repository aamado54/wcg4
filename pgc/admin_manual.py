"""
Edición manual del período con trazabilidad.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from django.db import transaction

from core.models import MetricDefinition, SystemSetting, UNE, UNEAlias
from imports.models import CrossSaleImportRow, NewClientImportRow
from pgc.models import (
    AdminManualEditLog,
    ManualRequirementsCompliance,
    MonthlyExchangeRate,
    MonthlyMetricResult,
    MonthlyTarget,
    PGCPlan,
)

from pgc.admin_utils import format_value, parse_decimal_or_none
from pgc.income_conversion import (
    count_stale_ingresos,
    format_usd_3,
    get_fx_rate,
    gtq_to_usd,
    mark_ingresos_stale_for_fx_change,
)

# Orden = ruta financiera sugerida (TC → metas → captura → resto).
MANUAL_TABS = (
    ("fx", "1 · Tipos de cambio"),
    ("targets", "2 · Metas (USD)"),
    ("results", "3 · Resultados"),
    ("requirements", "4 · Requerimientos"),
    ("imports", "Registros importados"),
    ("aliases", "Alias UNE"),
    ("notes", "Notas del período"),
)

CRITICAL_ENTITY_TYPES = {
    AdminManualEditLog.ENTITY_RESULT,
    AdminManualEditLog.ENTITY_REQUIREMENT,
}


def _period_note_key(year: int, month: int) -> str:
    return f"admin.period_note.{year}.{month:02d}"


def _get_plan(year: int) -> PGCPlan | None:
    return PGCPlan.objects.filter(year=year).first()


def log_manual_edit(
    *,
    user,
    year: int,
    month: int,
    entity_type: str,
    entity_id: int | None,
    field_name: str,
    old_value,
    new_value,
    reason: str = "",
) -> AdminManualEditLog:
    return AdminManualEditLog.objects.create(
        year=year,
        month=month,
        entity_type=entity_type,
        entity_id=entity_id,
        field_name=field_name,
        old_value=format_value(old_value),
        new_value=format_value(new_value),
        reason=reason or "",
        edited_by=user,
    )


def _metrics() -> list[MetricDefinition]:
    return list(MetricDefinition.objects.filter(code__in=[
        MetricDefinition.CODE_INGRESOS,
        MetricDefinition.CODE_CLIENTES_NUEVOS,
        MetricDefinition.CODE_VENTA_CRUZADA,
        MetricDefinition.CODE_RESPUESTA_REQS,
    ]).order_by("code"))


def _unes() -> list[UNE]:
    return list(UNE.objects.filter(is_active=True).order_by("sort_order", "code"))


def get_pending_alias_values(year: int, month: int, month_from: int | None = None) -> list[str]:
    known = {a.raw_value.strip().upper() for a in UNEAlias.objects.filter(is_active=True)}
    pending: set[str] = set()
    mf = month_from or month

    for raw in (
        NewClientImportRow.objects.filter(year=year, month__gte=mf, month__lte=month)
        .exclude(raw_une_value="")
        .values_list("raw_une_value", flat=True)
    ):
        key = (raw or "").strip().upper()
        if key and key not in known:
            pending.add(raw.strip())

    for raw_dest, raw_orig in CrossSaleImportRow.objects.filter(
        year=year, month__gte=mf, month__lte=month
    ).values_list("raw_une_destination", "raw_une_origin"):
        for raw in (raw_dest, raw_orig):
            key = (raw or "").strip().upper()
            if key and key not in known:
                pending.add(raw.strip())

    return sorted(pending, key=str.upper)


def get_manual_edit_context(year: int, month: int, tab: str, month_from: int | None = None) -> dict[str, Any]:
    plan = _get_plan(year)
    metrics = _metrics()
    unes = _unes()
    mf = month_from or month
    is_range = mf != month

    targets_map = {}
    results_map = {}
    if plan:
        for t in MonthlyTarget.objects.filter(plan=plan, year=year, month=month).select_related("une", "metric"):
            targets_map[(t.une_id, t.metric_id)] = t
        for r in MonthlyMetricResult.objects.filter(plan=plan, year=year, month=month).select_related("une", "metric"):
            results_map[(r.une_id, r.metric_id)] = r

    target_rows = []
    for une in unes:
        cells = []
        for metric in metrics:
            obj = targets_map.get((une.id, metric.id))
            cells.append({"metric": metric, "obj": obj, "value": getattr(obj, "target_value", None)})
        target_rows.append({"une": une, "cells": cells})

    fx = MonthlyExchangeRate.objects.filter(year=year, month=month).first()
    has_fx = fx is not None and fx.usd_to_gtq not in (None, Decimal("0"), 0)

    fx_by_month = {
        r.month: r
        for r in MonthlyExchangeRate.objects.filter(year=year, month__gte=mf, month__lte=month)
    }
    fx_rows = []
    for m in range(mf, month + 1):
        rate_obj = fx_by_month.get(m)
        fx_rows.append({
            "month": m,
            "label": f"{year}-{m:02d}",
            "obj": rate_obj,
            "value": rate_obj.usd_to_gtq if rate_obj else None,
            "is_focus": m == month,
            "missing": rate_obj is None or rate_obj.usd_to_gtq in (None, Decimal("0"), 0),
        })
    missing_fx_months = [row["label"] for row in fx_rows if row["missing"]]

    result_rows = []
    ingresos_code = MetricDefinition.CODE_INGRESOS
    for une in unes:
        cells = []
        for metric in metrics:
            obj = results_map.get((une.id, metric.id))
            is_ingresos = metric.code == ingresos_code
            source_gtq = None
            measured_usd = getattr(obj, "measured_value", None) if obj else None
            input_currency = "GTQ"
            if obj and is_ingresos and obj.source_currency == MonthlyMetricResult.CURRENCY_GTQ:
                source_gtq = obj.source_value
                input_currency = "GTQ"
                input_value = source_gtq
            elif obj and is_ingresos and obj.source_currency == MonthlyMetricResult.CURRENCY_USD:
                input_currency = "USD"
                input_value = measured_usd
            elif is_ingresos and obj and measured_usd is not None and not obj.source_currency:
                # Legado: measured_value ya era USD canónico.
                input_currency = "USD"
                input_value = measured_usd
            elif is_ingresos:
                input_currency = "GTQ"
                input_value = None
            else:
                input_value = measured_usd
            cells.append({
                "metric": metric,
                "obj": obj,
                "value": input_value,
                "is_ingresos": is_ingresos,
                "input_currency": input_currency,
                "source_gtq": source_gtq,
                "measured_usd": measured_usd,
                "measured_usd_display": format_usd_3(measured_usd) if is_ingresos else None,
                "fx_used": getattr(obj, "exchange_rate_used", None) if obj else None,
                "conversion_status": getattr(obj, "conversion_status", "") if obj else "",
                "input_disabled": is_ingresos and input_currency == "GTQ" and not has_fx,
            })
        result_rows.append({"une": une, "cells": cells})

    requirements = []
    req_map = {}
    if plan:
        req_map = {
            r.une_id: r
            for r in ManualRequirementsCompliance.objects.filter(plan=plan, year=year, month=month)
        }
    for une in unes:
        requirements.append({"une": une, "obj": req_map.get(une.id)})

    aliases = list(UNEAlias.objects.select_related("une").filter(is_active=True).order_by("raw_value")[:200])
    pending_aliases = get_pending_alias_values(year, month, month_from=mf)

    import_limit = 400 if is_range else 100
    new_client_rows = list(
        NewClientImportRow.objects.filter(year=year, month__gte=mf, month__lte=month)
        .select_related("une", "currency")
        .order_by("year", "month", "une__sort_order", "client_name")[:import_limit]
    )
    cross_sale_rows = list(
        CrossSaleImportRow.objects.filter(year=year, month__gte=mf, month__lte=month)
        .select_related("une_destination", "une_origin", "currency")
        .order_by("year", "month", "client_name")[:import_limit]
    )

    note_setting = SystemSetting.objects.filter(key=_period_note_key(year, month)).first()
    period_note = (note_setting.value_text or "") if note_setting else ""

    recent_edits = list(
        AdminManualEditLog.objects.filter(year=year, month__gte=mf, month__lte=month)
        .select_related("edited_by")
        .order_by("-created_at")[:15]
    )

    valid_tabs = {t[0] for t in MANUAL_TABS}
    if tab not in valid_tabs:
        tab = "targets"

    # FX aprovecha el rango completo; metas/resultados/reqs siguen enfocados en month_to.
    range_capable_tabs = {"imports", "aliases", "fx"}
    tab_uses_range = tab in range_capable_tabs

    return {
        "year": year,
        "month": month,
        "month_from": mf,
        "label": (
            f"{year}-{mf:02d} → {year}-{month:02d}" if is_range else f"{year}-{month:02d}"
        ),
        "focus_label": f"{year}-{month:02d}",
        "plan": plan,
        "tab_uses_range": tab_uses_range,
        "supports_month_range": tab_uses_range,
        "single_month_ops": not tab_uses_range,
        "tab": tab,
        "tabs": MANUAL_TABS,
        "metrics": metrics,
        "unes": unes,
        "target_rows": target_rows,
        "result_rows": result_rows,
        "requirements": requirements,
        "fx": fx,
        "fx_rows": fx_rows,
        "missing_fx_months": missing_fx_months,
        "has_fx": has_fx,
        "fx_rate": fx.usd_to_gtq if fx else None,
        "stale_ingresos_count": count_stale_ingresos(year, month),
        "aliases": aliases,
        "pending_aliases": pending_aliases,
        "new_client_rows": new_client_rows,
        "cross_sale_rows": cross_sale_rows,
        "period_note": period_note,
        "recent_edits": recent_edits,
    }


@transaction.atomic
def save_targets(user, year: int, month: int, post_data, reason: str = "") -> int:
    plan = _get_plan(year)
    if not plan:
        raise ValueError("No existe plan PGC para este año.")

    changes = 0
    for une in _unes():
        for metric in _metrics():
            key = f"target_{une.id}_{metric.id}"
            raw = (post_data.get(key) or "").strip()
            if raw == "":
                continue
            parsed = parse_decimal_or_none(raw)
            if parsed is None:
                raise ValueError(f"Valor inválido en meta {une.code} / {metric.code}.")

            obj, _ = MonthlyTarget.objects.get_or_create(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
                defaults={"target_value": parsed},
            )
            old = obj.target_value
            if old != parsed:
                obj.target_value = parsed
                obj.save(update_fields=["target_value", "updated_at"])
                log_manual_edit(
                    user=user,
                    year=year,
                    month=month,
                    entity_type=AdminManualEditLog.ENTITY_TARGET,
                    entity_id=obj.id,
                    field_name="target_value",
                    old_value=old,
                    new_value=parsed,
                    reason=reason,
                )
                changes += 1
    return changes


@transaction.atomic
def save_results(user, year: int, month: int, post_data, reason: str = "") -> int:
    if not reason.strip():
        raise ValueError("Debe indicar un motivo para cambios en resultados.")

    plan = _get_plan(year)
    if not plan:
        raise ValueError("No existe plan PGC para este año.")

    fx_rate = get_fx_rate(year, month)
    changes = 0
    for une in _unes():
        for metric in _metrics():
            key = f"result_{une.id}_{metric.id}"
            raw = (post_data.get(key) or "").strip()
            if raw == "":
                continue
            parsed = parse_decimal_or_none(raw)
            if parsed is None:
                raise ValueError(f"Valor inválido en resultado {une.code} / {metric.code}.")

            is_ingresos = metric.code == MetricDefinition.CODE_INGRESOS

            if is_ingresos:
                currency = (
                    post_data.get(f"ingresos_curr_{une.id}")
                    or post_data.get(f"ingresos_curr_{une.id}_{metric.id}")
                    or "GTQ"
                ).strip().upper()
                if currency not in (
                    MonthlyMetricResult.CURRENCY_GTQ,
                    MonthlyMetricResult.CURRENCY_USD,
                ):
                    currency = MonthlyMetricResult.CURRENCY_GTQ

                if currency == MonthlyMetricResult.CURRENCY_USD:
                    usd_value = parsed
                    obj, created = MonthlyMetricResult.objects.get_or_create(
                        plan=plan,
                        une=une,
                        metric=metric,
                        year=year,
                        month=month,
                        defaults={
                            "measured_value": usd_value,
                            "source_currency": MonthlyMetricResult.CURRENCY_USD,
                            "source_value": usd_value,
                            "exchange_rate_used": None,
                            "conversion_status": MonthlyMetricResult.CONVERSION_NATIVE_USD,
                        },
                    )
                    old_usd = None if created else obj.measured_value
                    old_curr = "" if created else (obj.source_currency or "")
                    changed = (
                        created
                        or old_usd != usd_value
                        or old_curr != MonthlyMetricResult.CURRENCY_USD
                    )
                    if not changed:
                        continue

                    obj.measured_value = usd_value
                    obj.source_currency = MonthlyMetricResult.CURRENCY_USD
                    obj.source_value = usd_value
                    obj.exchange_rate_used = None
                    obj.conversion_status = MonthlyMetricResult.CONVERSION_NATIVE_USD
                    obj.calculation_note = (
                        f"Captura manual USD nativo: {usd_value} USD [{year}-{month:02d}]"
                    )
                    obj.save(
                        update_fields=[
                            "measured_value",
                            "source_currency",
                            "source_value",
                            "exchange_rate_used",
                            "conversion_status",
                            "calculation_note",
                            "updated_at",
                        ]
                    )
                    log_manual_edit(
                        user=user,
                        year=year,
                        month=month,
                        entity_type=AdminManualEditLog.ENTITY_RESULT,
                        entity_id=obj.id,
                        field_name="ingresos_usd_native",
                        old_value=f"USD={old_usd}; curr={old_curr}",
                        new_value=f"USD={usd_value}",
                        reason=reason,
                    )
                    changes += 1
                    continue

                # Manual INGRESOS: capture GTQ, convert to canonical USD.
                if fx_rate is None:
                    raise ValueError(
                        f"Falta tipo de cambio para {year}-{month:02d}. "
                        f"No se pueden guardar ingresos (GTQ) de {une.name_es} sin TC. "
                        "Vaya a la pestaña «Tipos de cambio»."
                    )
                usd_value = gtq_to_usd(parsed, fx_rate)
                obj, created = MonthlyMetricResult.objects.get_or_create(
                    plan=plan,
                    une=une,
                    metric=metric,
                    year=year,
                    month=month,
                    defaults={
                        "measured_value": usd_value,
                        "source_currency": MonthlyMetricResult.CURRENCY_GTQ,
                        "source_value": parsed,
                        "exchange_rate_used": fx_rate,
                        "conversion_status": MonthlyMetricResult.CONVERSION_CONVERTED,
                    },
                )
                old_usd = None if created else obj.measured_value
                old_gtq = None if created else obj.source_value
                changed = (
                    created
                    or old_usd != usd_value
                    or old_gtq != parsed
                    or obj.source_currency != MonthlyMetricResult.CURRENCY_GTQ
                    or obj.exchange_rate_used != fx_rate
                )
                if not changed:
                    continue

                obj.measured_value = usd_value
                obj.source_currency = MonthlyMetricResult.CURRENCY_GTQ
                obj.source_value = parsed
                obj.exchange_rate_used = fx_rate
                obj.conversion_status = MonthlyMetricResult.CONVERSION_CONVERTED
                obj.calculation_note = (
                    f"Captura manual GTQ→USD: {parsed} GTQ / {fx_rate} = {usd_value} USD "
                    f"[{year}-{month:02d}]"
                )
                obj.save(
                    update_fields=[
                        "measured_value",
                        "source_currency",
                        "source_value",
                        "exchange_rate_used",
                        "conversion_status",
                        "calculation_note",
                        "updated_at",
                    ]
                )
                log_manual_edit(
                    user=user,
                    year=year,
                    month=month,
                    entity_type=AdminManualEditLog.ENTITY_RESULT,
                    entity_id=obj.id,
                    field_name="ingresos_gtq_to_usd",
                    old_value=f"GTQ={old_gtq}; USD={old_usd}",
                    new_value=f"GTQ={parsed}; FX={fx_rate}; USD={usd_value}",
                    reason=reason,
                )
                changes += 1
                continue

            # Non-INGRESOS metrics: keep legacy USD/native numeric semantics.
            obj, created = MonthlyMetricResult.objects.get_or_create(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
                defaults={
                    "measured_value": parsed,
                    "source_currency": "",
                    "conversion_status": MonthlyMetricResult.CONVERSION_NATIVE_USD,
                },
            )
            old = None if created else obj.measured_value
            if created or old != parsed:
                obj.measured_value = parsed
                obj.calculation_note = (obj.calculation_note or "") + " [Edición manual]"
                obj.save(update_fields=["measured_value", "calculation_note", "updated_at"])
                log_manual_edit(
                    user=user,
                    year=year,
                    month=month,
                    entity_type=AdminManualEditLog.ENTITY_RESULT,
                    entity_id=obj.id,
                    field_name="measured_value",
                    old_value=old,
                    new_value=parsed,
                    reason=reason,
                )
                changes += 1
    return changes


@transaction.atomic
def save_fx(user, year: int, month: int, post_data, reason: str = "", month_from: int | None = None) -> int:
    """Save FX for focus month and/or every month in [month_from, month].

    Accepts either:
    - ``fx_value`` for a single month (focus ``month``), or
    - ``fx_value_<m>`` for each month in the selected range.
    """
    mf = month_from or month
    if mf > month:
        mf = month

    entries: list[tuple[int, str]] = []
    saw_range_keys = False
    for m in range(mf, month + 1):
        key = f"fx_value_{m}"
        if key in post_data:
            saw_range_keys = True
            entries.append((m, (post_data.get(key) or "").strip()))
    if not saw_range_keys:
        entries = [(month, (post_data.get("fx_value") or "").strip())]

    changes = 0
    for m, raw in entries:
        if raw == "":
            continue
        parsed = parse_decimal_or_none(raw)
        if parsed is None:
            raise ValueError(f"Tipo de cambio inválido para {year}-{m:02d}.")

        obj, created = MonthlyExchangeRate.objects.get_or_create(
            year=year,
            month=m,
            defaults={"usd_to_gtq": parsed},
        )
        old = None if created else obj.usd_to_gtq
        if created or old != parsed:
            obj.usd_to_gtq = parsed
            obj.save(update_fields=["usd_to_gtq"])
            log_manual_edit(
                user=user,
                year=year,
                month=m,
                entity_type=AdminManualEditLog.ENTITY_FX,
                entity_id=obj.id,
                field_name="usd_to_gtq",
                old_value=old,
                new_value=parsed,
                reason=reason,
            )
            # Do not silently recalc incomes; mark convertible GTQ rows as stale.
            if not created and old != parsed:
                mark_ingresos_stale_for_fx_change(
                    year=year,
                    month=m,
                    old_fx=old,
                    new_fx=parsed,
                    user=user,
                    reason=reason,
                )
            changes += 1
    return changes


@transaction.atomic
def save_requirements(user, year: int, month: int, post_data, reason: str = "") -> int:
    plan = _get_plan(year)
    if not plan:
        raise ValueError("No existe plan PGC para este año.")

    changes = 0
    for une in _unes():
        compliant_key = f"req_compliant_{une.id}"
        note_key = f"req_note_{une.id}"
        is_compliant = post_data.get(compliant_key) == "1"
        incident_note = (post_data.get(note_key) or "").strip()

        if not is_compliant and not incident_note and not reason.strip():
            raise ValueError(f"Indique motivo o nota de incidencia para {une.name_es}.")

        obj, created = ManualRequirementsCompliance.objects.get_or_create(
            plan=plan,
            une=une,
            year=year,
            month=month,
            defaults={"is_compliant": is_compliant, "incident_note": incident_note},
        )
        old_compliant = None if created else obj.is_compliant
        old_note = "" if created else obj.incident_note

        changed = False
        if obj.is_compliant != is_compliant:
            obj.is_compliant = is_compliant
            changed = True
        if obj.incident_note != incident_note:
            obj.incident_note = incident_note
            changed = True

        if changed:
            obj.save(update_fields=["is_compliant", "incident_note", "updated_at"])
            log_manual_edit(
                user=user,
                year=year,
                month=month,
                entity_type=AdminManualEditLog.ENTITY_REQUIREMENT,
                entity_id=obj.id,
                field_name="is_compliant/incident_note",
                old_value=f"compliant={old_compliant}; note={old_note}",
                new_value=f"compliant={is_compliant}; note={incident_note}",
                reason=reason or incident_note,
            )
            changes += 1
    return changes


@transaction.atomic
def save_alias(user, year: int, month: int, post_data, reason: str = "") -> int:
    raw_value = (post_data.get("alias_raw") or "").strip()
    une_id = post_data.get("alias_une")
    if not raw_value or not une_id:
        raise ValueError("Debe indicar valor crudo y UNE destino.")

    une = UNE.objects.filter(id=une_id).first()
    if not une:
        raise ValueError("UNE no válida.")

    # Investment en el valor crudo siempre apunta a Inversiones.
    raw_lower = raw_value.lower()
    if any(
        token in raw_lower
        for token in (
            "investment",
            "investments",
            "invest",
            "inversiones",
            "inversion",
            "inversión",
        )
    ):
        investment = UNE.objects.filter(code=UNE.CODE_INVESTMENT).first()
        if investment:
            une = investment

    obj, created = UNEAlias.objects.get_or_create(
        raw_value=raw_value,
        defaults={"une": une, "is_active": True},
    )
    old_une = None if created else obj.une_id
    if not created and (obj.une_id != une.id or not obj.is_active):
        obj.une = une
        obj.is_active = True
        obj.save(update_fields=["une", "is_active", "updated_at"])
        log_manual_edit(
            user=user,
            year=year,
            month=month,
            entity_type=AdminManualEditLog.ENTITY_ALIAS,
            entity_id=obj.id,
            field_name="une",
            old_value=old_une,
            new_value=une.id,
            reason=reason or f"Mapeo {raw_value} -> {une.code}",
        )
        return 1

    if created:
        log_manual_edit(
            user=user,
            year=year,
            month=month,
            entity_type=AdminManualEditLog.ENTITY_ALIAS,
            entity_id=obj.id,
            field_name="raw_value",
            old_value="",
            new_value=raw_value,
            reason=reason or f"Nuevo alias -> {une.code}",
        )
        return 1
    return 0


@transaction.atomic
def save_aliases_bulk(user, year: int, month: int, post_data, reason: str = "") -> int:
    """Actualiza UNE de aliases existentes desde la tabla editable."""
    changes = 0
    investment = UNE.objects.filter(code=UNE.CODE_INVESTMENT).first()
    by_id = {u.id: u for u in UNE.objects.filter(is_active=True)}

    for alias in UNEAlias.objects.filter(is_active=True):
        raw = post_data.get(f"alias_{alias.id}_une")
        if raw is None:
            continue
        try:
            une_id = int(raw)
        except (TypeError, ValueError):
            continue
        une = by_id.get(une_id)
        if not une:
            continue

        raw_lower = (alias.raw_value or "").lower()
        if investment and any(
            token in raw_lower
            for token in (
                "investment",
                "investments",
                "invest",
                "inversiones",
                "inversion",
                "inversión",
            )
        ):
            une = investment

        if alias.une_id == une.id:
            continue

        old_une = alias.une_id
        alias.une = une
        alias.save(update_fields=["une", "updated_at"])
        log_manual_edit(
            user=user,
            year=year,
            month=month,
            entity_type=AdminManualEditLog.ENTITY_ALIAS,
            entity_id=alias.id,
            field_name="une",
            old_value=old_une,
            new_value=une.id,
            reason=reason or f"Corrección alias {alias.raw_value} -> {une.code}",
        )
        changes += 1
    return changes


@transaction.atomic
def save_import_rows(
    user,
    year: int,
    month: int,
    post_data,
    reason: str = "",
    month_from: int | None = None,
) -> int:
    changes = 0
    mf = month_from or month

    for row in NewClientImportRow.objects.filter(year=year, month__gte=mf, month__lte=month):
        prefix = f"nc_{row.id}_"
        counts = post_data.get(f"{prefix}counts_as_new") == "1"
        obs = (post_data.get(f"{prefix}observations") or "").strip()
        old_counts = row.counts_as_new
        old_obs = row.observations
        if counts != old_counts or obs != old_obs:
            row.counts_as_new = counts
            row.observations = obs
            row.save(update_fields=["counts_as_new", "observations", "updated_at"])
            log_manual_edit(
                user=user,
                year=row.year,
                month=row.month,
                entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
                entity_id=row.id,
                field_name="counts_as_new/observations",
                old_value=f"counts={old_counts}; obs={old_obs}",
                new_value=f"counts={counts}; obs={obs}",
                reason=reason,
            )
            changes += 1

    for row in CrossSaleImportRow.objects.filter(year=year, month__gte=mf, month__lte=month):
        prefix = f"cs_{row.id}_"
        dest_raw = post_data.get(f"{prefix}dest")
        orig_raw = post_data.get(f"{prefix}orig")
        if dest_raw is None and orig_raw is None:
            continue
        dest = int(dest_raw) if dest_raw else None
        orig = int(orig_raw) if orig_raw else None
        old_dest = row.une_destination_id
        old_orig = row.une_origin_id
        if row.une_destination_id == dest and row.une_origin_id == orig:
            continue
        row.une_destination_id = dest
        row.une_origin_id = orig
        row.save(update_fields=["une_destination", "une_origin", "updated_at"])
        log_manual_edit(
            user=user,
            year=row.year,
            month=row.month,
            entity_type=AdminManualEditLog.ENTITY_CROSS_SALE_ROW,
            entity_id=row.id,
            field_name="une_destination/une_origin",
            old_value=f"dest={old_dest}; orig={old_orig}",
            new_value=f"dest={dest}; orig={orig}",
            reason=reason,
        )
        changes += 1

    return changes


@transaction.atomic
def save_period_note(user, year: int, month: int, post_data, reason: str = "") -> int:
    note = (post_data.get("period_note") or "").strip()
    key = _period_note_key(year, month)
    setting, created = SystemSetting.objects.get_or_create(key=key, defaults={"value_text": note})
    old = "" if created else (setting.value_text or "")
    if old != note:
        setting.value_text = note
        setting.updated_by = user
        setting.save(update_fields=["value_text", "updated_by", "updated_at"])
        log_manual_edit(
            user=user,
            year=year,
            month=month,
            entity_type=AdminManualEditLog.ENTITY_PERIOD_NOTE,
            entity_id=setting.id,
            field_name="value_text",
            old_value=old,
            new_value=note,
            reason=reason,
        )
        return 1
    return 0
