"""
Servicios agregados para el tablero de Administración mensual.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from django.core.management import call_command
from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone

from core.models import MetricDefinition, UNE, UNEAlias
from imports.models import (
    CrossSaleImportHeader,
    CrossSaleImportRow,
    FileUpload,
    FinancialStatementImportHeader,
    NewClientImportHeader,
    NewClientImportRow,
    StationTimeImportHeader,
)
from pgc.models import (
    AdminManualEditLog,
    ManualRequirementsCompliance,
    MonthlyExchangeRate,
    MonthlyMetricResult,
    MonthlyModeScorecard,
    MonthlyTarget,
    PGCPlan,
)

from .admin_manual import log_manual_edit

# Bloques del tablero (orden visual)
BLOCK_TARGETS = "targets"
BLOCK_FINANCIAL = "financial"
BLOCK_NEW_CLIENTS = "new_clients"
BLOCK_CROSS_SALE = "cross_sale"
BLOCK_MANUAL_REQUIREMENTS = "manual_requirements"
BLOCK_REVIEW = "review"

BLOCK_ORDER = (
    BLOCK_TARGETS,
    BLOCK_FINANCIAL,
    BLOCK_NEW_CLIENTS,
    BLOCK_CROSS_SALE,
    BLOCK_MANUAL_REQUIREMENTS,
    BLOCK_REVIEW,
)

BLOCK_META = {
    BLOCK_TARGETS: {"step": 1, "label": "Metas", "short": "Metas mensuales del plan"},
    BLOCK_FINANCIAL: {"step": 2, "label": "Estados de resultados", "short": "Ingresos por UNE (WC*)"},
    BLOCK_NEW_CLIENTS: {"step": 3, "label": "Clientes nuevos", "short": "Archivo de clientes nuevos"},
    BLOCK_CROSS_SALE: {"step": 4, "label": "Venta cruzada", "short": "Referencias entre UNEs"},
    BLOCK_MANUAL_REQUIREMENTS: {
        "step": 5,
        "label": "Requerimientos manuales",
        "short": "Cumplimiento de respuesta a requerimientos",
    },
    BLOCK_REVIEW: {"step": 6, "label": "Revisar resultado", "short": "Score y tablero del período"},
}

STATUS_PENDING = "pending"
STATUS_LOADED = "loaded"
STATUS_OBSERVED = "observed"
STATUS_REVIEWED = "reviewed"
STATUS_CLOSED = "closed"

STATUS_LABELS = {
    STATUS_PENDING: "Pendiente",
    STATUS_LOADED: "Cargado",
    STATUS_OBSERVED: "Con observaciones",
    STATUS_REVIEWED: "Revisado",
    STATUS_CLOSED: "Cerrado",
}

PERIOD_INCOMPLETE = "incomplete"
PERIOD_IN_REVIEW = "in_review"
PERIOD_READY = "ready"
PERIOD_CLOSED = "closed"

PERIOD_STATUS_LABELS = {
    PERIOD_INCOMPLETE: "Incompleto",
    PERIOD_IN_REVIEW: "En revisión",
    PERIOD_READY: "Listo",
    PERIOD_CLOSED: "Cerrado",
}

INGRESOS_UNES = ("FACTORING", "FACTORAJE", "LEASING", "INSURANCE")
METRIC_CODES = (
    MetricDefinition.CODE_INGRESOS,
    MetricDefinition.CODE_CLIENTES_NUEVOS,
    MetricDefinition.CODE_VENTA_CRUZADA,
    MetricDefinition.CODE_RESPUESTA_REQS,
)


def _period_label(year: int, month: int) -> str:
    return f"{year}-{month:02d}"


def _status_badge(status: str) -> str:
    return STATUS_LABELS.get(status, status)


def _get_plan(year: int) -> PGCPlan | None:
    return PGCPlan.objects.filter(year=year).first()


def _latest_upload_for_period(year: int, month: int, file_type: str) -> FileUpload | None:
    return (
        FileUpload.objects.filter(
            detected_year=year,
            detected_month=month,
            file_type_detected=file_type,
        )
        .select_related("uploaded_by")
        .order_by("-created_at")
        .first()
    )


def _upload_actor(upload: FileUpload | None) -> str | None:
    if upload and upload.uploaded_by:
        return upload.uploaded_by.username
    return None


def _upload_timestamp(upload: FileUpload | None) -> datetime | None:
    if upload:
        return upload.updated_at or upload.created_at
    return None


def _count_pending_aliases(year: int, month: int) -> int:
    known = {a.raw_value.strip().upper() for a in UNEAlias.objects.filter(is_active=True)}
    pending = set()

    for raw in (
        NewClientImportRow.objects.filter(year=year, month=month)
        .exclude(raw_une_value="")
        .values_list("raw_une_value", flat=True)
    ):
        key = (raw or "").strip().upper()
        if key and key not in known:
            pending.add(key)

    for raw_dest, raw_orig in CrossSaleImportRow.objects.filter(
        year=year, month=month
    ).values_list("raw_une_destination", "raw_une_origin"):
        for raw in (raw_dest, raw_orig):
            key = (raw or "").strip().upper()
            if key and key not in known:
                pending.add(key)

    unresolved_cross = CrossSaleImportRow.objects.filter(
        year=year, month=month
    ).filter(Q(une_destination__isnull=True) | Q(une_origin__isnull=True)).count()

    return len(pending) + unresolved_cross


def _block_targets(plan: PGCPlan | None, year: int, month: int) -> dict[str, Any]:
    if not plan:
        return _empty_block(BLOCK_TARGETS, "No hay plan PGC para este año.")

    count = MonthlyTarget.objects.filter(plan=plan, year=year, month=month).count()
    active_unes = UNE.objects.filter(is_active=True).count()
    expected = active_unes * len(METRIC_CODES)

    status = STATUS_LOADED if count >= expected else STATUS_PENDING
    summary = f"{count} metas registradas"

    return {
        **_block_shell(BLOCK_TARGETS),
        "status": status,
        "status_label": _status_badge(status),
        "summary": summary,
        "last_action_at": None,
        "last_action_by": None,
        "checklist": [
            {"label": "Metas del plan cargadas", "done": count > 0},
            {"label": "Cobertura completa por UNE y métrica", "done": count >= expected},
        ],
        "stats": {"targets_count": count, "expected": expected},
    }


def _block_financial(plan: PGCPlan | None, year: int, month: int) -> dict[str, Any]:
    upload = _latest_upload_for_period(year, month, FileUpload.TYPE_FINANCIAL)
    headers = FinancialStatementImportHeader.objects.filter(year=year, month=month)
    header_count = headers.count()

    ingresos_metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
    results_count = 0
    if plan and ingresos_metric:
        results_count = MonthlyMetricResult.objects.filter(
            plan=plan,
            metric=ingresos_metric,
            year=year,
            month=month,
            une__code__in=INGRESOS_UNES,
            measured_value__isnull=False,
        ).count()

    has_fx = MonthlyExchangeRate.objects.filter(year=year, month=month).exists()
    has_error = upload and upload.status == FileUpload.STATUS_PARSED_ERROR

    if has_error:
        status = STATUS_OBSERVED
    elif results_count >= 3:
        status = STATUS_LOADED
    elif upload or header_count:
        status = STATUS_OBSERVED
    else:
        status = STATUS_PENDING

    summary_parts = []
    if upload:
        summary_parts.append(upload.original_filename)
    summary_parts.append(f"{results_count}/3 UNEs con ingreso")
    if not has_fx:
        summary_parts.append("falta tipo de cambio")

    return {
        **_block_shell(BLOCK_FINANCIAL),
        "status": status,
        "status_label": _status_badge(status),
        "summary": " · ".join(summary_parts),
        "last_action_at": _upload_timestamp(upload),
        "last_action_by": _upload_actor(upload),
        "checklist": [
            {"label": "Tipo de cambio del mes", "done": has_fx},
            {"label": "Archivo(s) WC* subido(s)", "done": bool(upload)},
            {"label": "Ingresos importados (Factoring, Leasing, Insurance)", "done": results_count >= 3},
            {"label": "Sin errores de lectura", "done": not has_error},
        ],
        "stats": {
            "upload_id": upload.id if upload else None,
            "results_count": results_count,
            "has_fx": has_fx,
        },
        "uploads": _period_uploads(year, month, FileUpload.TYPE_FINANCIAL),
    }


def _new_client_row_dedup_key(row: NewClientImportRow) -> tuple:
    # counts_as_new is derived; ignore it so Sí/No twins count as duplicates.
    return (
        row.une_id,
        (row.client_name or "").strip().casefold(),
        (row.nit or "").strip(),
        (row.operation_code or "").strip(),
        row.previous_contracts,
        row.currency_id,
        str(row.amount) if row.amount is not None else "",
    )


def count_duplicate_new_client_rows(year: int, month: int) -> int:
    """Cuenta filas duplicadas en el detalle de clientes nuevos del período."""
    seen: set[tuple] = set()
    duplicate_ids: list[int] = []
    for row in NewClientImportRow.objects.filter(year=year, month=month).order_by("id"):
        key = _new_client_row_dedup_key(row)
        if key in seen:
            duplicate_ids.append(row.id)
        else:
            seen.add(key)
    return len(duplicate_ids)


def _sync_clientes_nuevos_metrics_from_rows(year: int, month: int) -> int:
    """Actualiza CLIENTES_NUEVOS desde las filas vigentes del período."""
    plan = _get_plan(year)
    if not plan:
        return 0

    metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_CLIENTES_NUEVOS)
    counts = {
        row["une_id"]: row["cnt"]
        for row in NewClientImportRow.objects.filter(year=year, month=month, counts_as_new=True)
        .values("une_id")
        .annotate(cnt=Count("id"))
    }

    updated = 0
    for une in UNE.objects.filter(is_active=True):
        count = counts.get(une.id, 0)
        try:
            target = MonthlyTarget.objects.get(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
            )
        except MonthlyTarget.DoesNotExist:
            continue

        mmr, _ = MonthlyMetricResult.objects.get_or_create(
            plan=plan,
            une=une,
            metric=metric,
            year=year,
            month=month,
            defaults={"target_value": target.target_value},
        )
        mmr.target_value = target.target_value
        mmr.measured_value = Decimal(str(count))
        mmr.calculation_note = f"{count} clientes nuevos contados desde filas del período"
        mmr.save()
        updated += 1
    return updated


@transaction.atomic
def remove_duplicate_new_client_rows(year: int, month: int, user=None) -> dict[str, int]:
    """
    Elimina filas duplicadas del detalle de clientes nuevos (conserva la más antigua).
    Opcionalmente sincroniza la métrica CLIENTES_NUEVOS.
    """
    seen: set[tuple] = set()
    duplicate_ids: list[int] = []
    for row in NewClientImportRow.objects.filter(year=year, month=month).order_by("id"):
        key = _new_client_row_dedup_key(row)
        if key in seen:
            duplicate_ids.append(row.id)
        else:
            seen.add(key)

    removed = NewClientImportRow.objects.filter(id__in=duplicate_ids).delete()[0]
    metrics_updated = 0
    if removed:
        metrics_updated = _sync_clientes_nuevos_metrics_from_rows(year, month)
        if user:
            log_manual_edit(
                user=user,
                year=year,
                month=month,
                entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
                entity_id=0,
                field_name="dedup",
                old_value=f"{removed} duplicados",
                new_value="eliminados",
                reason="Depuración de duplicados en detalle de clientes nuevos",
            )
    return {"removed": removed, "metrics_updated": metrics_updated}


def _repoint_import_header_away_from_upload(upload: FileUpload) -> None:
    """
    Antes de borrar un FileUpload pendiente: si un encabezado lo apunta,
    reasigna a otro archivo del período o elimina el encabezado vacío.
    Nunca deja cascada sobre filas ya importadas.
    """
    specs: list[tuple[type, str, type | None]] = [
        (NewClientImportHeader, FileUpload.TYPE_NEW_CLIENTS, NewClientImportRow),
        (CrossSaleImportHeader, FileUpload.TYPE_CROSS_SALE, CrossSaleImportRow),
        (StationTimeImportHeader, FileUpload.TYPE_STATION_TIMES, None),
        (FinancialStatementImportHeader, FileUpload.TYPE_FINANCIAL, None),
    ]
    for header_model, file_type, row_model in specs:
        headers = list(header_model.objects.filter(file_upload=upload))
        for header in headers:
            year = getattr(header, "year", upload.detected_year)
            month = getattr(header, "month", upload.detected_month)
            alt_qs = FileUpload.objects.filter(
                file_type_detected=file_type,
            ).exclude(pk=upload.pk)
            if year is not None:
                alt_qs = alt_qs.filter(detected_year=year)
            if month is not None:
                alt_qs = alt_qs.filter(detected_month=month)
            alt = (
                alt_qs.filter(status=FileUpload.STATUS_PARSED_OK)
                .order_by("-created_at")
                .first()
                or alt_qs.order_by("-created_at").first()
            )

            has_rows = False
            if row_model is not None:
                has_rows = row_model.objects.filter(header=header).exists()

            if alt is not None:
                header.file_upload = alt
                header.save(update_fields=["file_upload"])
            elif has_rows:
                raise ValueError(
                    "No se puede quitar de la cola: el período ya tiene datos importados "
                    "y no hay otro archivo procesado al cual conservar el vínculo."
                )
            else:
                header.delete()


@transaction.atomic
def discard_pending_upload(upload: FileUpload) -> dict[str, Any]:
    """
    Elimina de la cola un archivo pendiente de procesar.
    Solo UPLOADED / PARSED_ERROR. No toca PARSED_OK ni filas ya cargadas.
    """
    if upload.status == FileUpload.STATUS_PARSED_OK:
        raise ValueError(
            "Este archivo ya fue procesado; no se puede quitar de la cola."
        )

    filename = upload.original_filename
    _repoint_import_header_away_from_upload(upload)

    if upload.stored_file:
        try:
            upload.stored_file.delete(save=False)
        except Exception:
            pass
    upload.delete()
    return {"filename": filename, "ok": True}


def _block_new_clients(plan: PGCPlan | None, year: int, month: int) -> dict[str, Any]:
    upload = _latest_upload_for_period(year, month, FileUpload.TYPE_NEW_CLIENTS)
    header = NewClientImportHeader.objects.filter(year=year, month=month).first()
    rows_qs = NewClientImportRow.objects.filter(year=year, month=month)
    valid_rows = rows_qs.filter(counts_as_new=True).count()
    obs_rows = rows_qs.exclude(observations="").count()
    duplicate_rows = count_duplicate_new_client_rows(year, month)
    has_error = upload and upload.status == FileUpload.STATUS_PARSED_ERROR

    if has_error or obs_rows:
        status = STATUS_OBSERVED
    elif header and valid_rows > 0:
        status = STATUS_LOADED
    elif upload:
        status = STATUS_OBSERVED
    else:
        status = STATUS_PENDING

    return {
        **_block_shell(BLOCK_NEW_CLIENTS),
        "status": status,
        "status_label": _status_badge(status),
        "summary": f"{valid_rows} clientes válidos" if valid_rows else "Sin datos procesados",
        "last_action_at": _upload_timestamp(upload) or (header.updated_at if header else None),
        "last_action_by": _upload_actor(upload),
        "checklist": [
            {"label": "Archivo subido", "done": bool(upload)},
            {"label": "Estructura validada", "done": bool(header)},
            {"label": "Filas importadas", "done": valid_rows > 0},
            {"label": "Sin observaciones pendientes", "done": obs_rows == 0},
        ],
        "stats": {
            "valid_rows": valid_rows,
            "obs_rows": obs_rows,
            "duplicate_rows": duplicate_rows,
            "upload_id": upload.id if upload else None,
        },
        "uploads": _period_uploads(year, month, FileUpload.TYPE_NEW_CLIENTS),
    }


def _block_cross_sale(plan: PGCPlan | None, year: int, month: int) -> dict[str, Any]:
    upload = _latest_upload_for_period(year, month, FileUpload.TYPE_CROSS_SALE)
    header = CrossSaleImportHeader.objects.filter(year=year, month=month).first()
    rows_count = CrossSaleImportRow.objects.filter(year=year, month=month).count()
    unresolved = CrossSaleImportRow.objects.filter(year=year, month=month).filter(
        Q(une_destination__isnull=True) | Q(une_origin__isnull=True)
    ).count()
    has_error = upload and upload.status == FileUpload.STATUS_PARSED_ERROR

    if has_error or unresolved:
        status = STATUS_OBSERVED
    elif header and rows_count > 0:
        status = STATUS_LOADED
    elif upload:
        status = STATUS_OBSERVED
    else:
        status = STATUS_PENDING

    return {
        **_block_shell(BLOCK_CROSS_SALE),
        "status": status,
        "status_label": _status_badge(status),
        "summary": f"{rows_count} referencias" if rows_count else "Sin datos procesados",
        "last_action_at": _upload_timestamp(upload) or (header.updated_at if header else None),
        "last_action_by": _upload_actor(upload),
        "checklist": [
            {"label": "Archivo subido", "done": bool(upload)},
            {"label": "Filas importadas", "done": rows_count > 0},
            {"label": "UNE destino/origen resueltos", "done": unresolved == 0 and rows_count > 0},
            {"label": "Sin errores de lectura", "done": not has_error},
        ],
        "stats": {"rows_count": rows_count, "unresolved": unresolved, "upload_id": upload.id if upload else None},
        "uploads": _period_uploads(year, month, FileUpload.TYPE_CROSS_SALE),
    }


def _block_manual_requirements(plan: PGCPlan | None, year: int, month: int) -> dict[str, Any]:
    if not plan:
        return _empty_block(BLOCK_MANUAL_REQUIREMENTS, "No hay plan PGC.")

    unes = list(UNE.objects.filter(is_active=True))
    records = {
        r.une_id: r
        for r in ManualRequirementsCompliance.objects.filter(plan=plan, year=year, month=month)
    }
    non_compliant = [r for r in records.values() if not r.is_compliant]
    filled = len(records)

    if non_compliant:
        status = STATUS_OBSERVED
    elif filled >= len(unes):
        status = STATUS_LOADED
    else:
        status = STATUS_PENDING

    latest = (
        ManualRequirementsCompliance.objects.filter(plan=plan, year=year, month=month)
        .order_by("-updated_at")
        .first()
    )

    return {
        **_block_shell(BLOCK_MANUAL_REQUIREMENTS),
        "status": status,
        "status_label": _status_badge(status),
        "summary": f"{filled}/{len(unes)} UNEs registradas",
        "last_action_at": latest.updated_at if latest else None,
        "last_action_by": None,
        "checklist": [
            {"label": "Registro por UNE", "done": filled >= len(unes)},
            {"label": "Sin incidencias reportadas", "done": not non_compliant},
        ],
        "stats": {"filled": filled, "total_unes": len(unes), "non_compliant": len(non_compliant)},
    }


def _block_review(plan: PGCPlan | None, year: int, month: int) -> dict[str, Any]:
    if not plan:
        return _empty_block(BLOCK_REVIEW, "No hay plan PGC.")

    scorecards = MonthlyModeScorecard.objects.filter(plan=plan, year=year, month=month)
    count = scorecards.count()
    latest = scorecards.order_by("-updated_at").first()

    if count >= UNE.objects.filter(is_active=True).count():
        status = STATUS_REVIEWED
    elif count > 0:
        status = STATUS_LOADED
    else:
        status = STATUS_PENDING

    return {
        **_block_shell(BLOCK_REVIEW),
        "status": status,
        "status_label": _status_badge(status),
        "summary": f"Score actualizado ({count} UNEs)" if count else "Sin recálculo",
        "last_action_at": latest.updated_at if latest else None,
        "last_action_by": None,
        "checklist": [
            {"label": "Ingresos Investment recalculados", "done": _investment_ingresos_ready(plan, year, month)},
            {"label": "Score PGC generado", "done": count > 0},
            {"label": "Todas las UNEs con score", "done": count >= UNE.objects.filter(is_active=True).count()},
        ],
        "stats": {"scorecard_count": count},
    }


def _investment_ingresos_ready(plan: PGCPlan, year: int, month: int) -> bool:
    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
    une = UNE.objects.filter(code__in=["INVESTMENT", "INVESTMENTS", "INVERSIONES"]).first()
    if not metric or not une:
        return False
    return MonthlyMetricResult.objects.filter(
        plan=plan, metric=metric, une=une, year=year, month=month, measured_value__isnull=False
    ).exists()


def _empty_block(block_id: str, summary: str) -> dict[str, Any]:
    return {
        **_block_shell(block_id),
        "status": STATUS_PENDING,
        "status_label": _status_badge(STATUS_PENDING),
        "summary": summary,
        "last_action_at": None,
        "last_action_by": None,
        "checklist": [],
        "stats": {},
        "uploads": [],
    }


def _block_shell(block_id: str) -> dict[str, Any]:
    meta = BLOCK_META[block_id]
    return {
        "id": block_id,
        "step": meta["step"],
        "label": meta["label"],
        "short": meta["short"],
    }


def _period_uploads(year: int, month: int, file_type: str) -> list[dict[str, Any]]:
    uploads = FileUpload.objects.filter(
        detected_year=year,
        detected_month=month,
        file_type_detected=file_type,
    ).select_related("uploaded_by").order_by("-created_at")[:5]
    return [
        {
            "id": u.id,
            "filename": u.original_filename,
            "status": u.status,
            "status_display": u.get_status_display(),
            "created_at": u.created_at,
            "user": _upload_actor(u),
            "can_discard": u.status != FileUpload.STATUS_PARSED_OK,
        }
        for u in uploads
    ]


def _derive_period_status(blocks: list[dict[str, Any]]) -> tuple[str, str]:
    statuses = [b["status"] for b in blocks]
    if all(s in (STATUS_REVIEWED, STATUS_CLOSED) for s in statuses):
        return PERIOD_CLOSED, PERIOD_STATUS_LABELS[PERIOD_CLOSED]
    if all(s in (STATUS_LOADED, STATUS_REVIEWED, STATUS_OBSERVED, STATUS_CLOSED) for s in statuses):
        if STATUS_OBSERVED in statuses or STATUS_PENDING in statuses:
            return PERIOD_IN_REVIEW, PERIOD_STATUS_LABELS[PERIOD_IN_REVIEW]
        return PERIOD_READY, PERIOD_STATUS_LABELS[PERIOD_READY]
    if any(s != STATUS_PENDING for s in statuses):
        return PERIOD_IN_REVIEW, PERIOD_STATUS_LABELS[PERIOD_IN_REVIEW]
    return PERIOD_INCOMPLETE, PERIOD_STATUS_LABELS[PERIOD_INCOMPLETE]


def get_admin_period_snapshot(year: int, month: int) -> dict[str, Any]:
    plan = _get_plan(year)
    blocks = [
        _block_targets(plan, year, month),
        _block_financial(plan, year, month),
        _block_new_clients(plan, year, month),
        _block_cross_sale(plan, year, month),
        _block_manual_requirements(plan, year, month),
        _block_review(plan, year, month),
    ]
    period_status, period_status_label = _derive_period_status(blocks)

    uploads = FileUpload.objects.filter(detected_year=year, detected_month=month)
    valid_rows = (
        NewClientImportRow.objects.filter(year=year, month=month, counts_as_new=True).count()
        + CrossSaleImportRow.objects.filter(year=year, month=month).count()
    )
    obs_rows = NewClientImportRow.objects.filter(year=year, month=month).exclude(observations="").count()
    pending_aliases = _count_pending_aliases(year, month)

    score_latest = None
    if plan:
        sc = (
            MonthlyModeScorecard.objects.filter(plan=plan, year=year, month=month)
            .order_by("-updated_at")
            .first()
        )
        score_latest = sc.updated_at if sc else None

    return {
        "year": year,
        "month": month,
        "label": _period_label(year, month),
        "plan": plan,
        "period_status": period_status,
        "period_status_label": period_status_label,
        "blocks": blocks,
        "blocks_by_id": {b["id"]: b for b in blocks},
        "summary": {
            "files_loaded": uploads.count(),
            "valid_rows": valid_rows,
            "rows_with_observations": obs_rows,
            "pending_aliases": pending_aliases,
            "metrics_recalculated": score_latest is not None,
            "last_score_update": score_latest,
        },
    }


def list_period_log(
    year: int,
    month: int,
    limit: int = 50,
    month_from: int | None = None,
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    mf = month_from or month

    uploads = (
        FileUpload.objects.filter(
            detected_year=year,
            detected_month__gte=mf,
            detected_month__lte=month,
        )
        .select_related("uploaded_by")
        .order_by("-created_at")
    )
    for upload in uploads[:limit]:
        entries.append(
            {
                "at": upload.created_at,
                "level": "INFO",
                "title": f"Archivo: {upload.original_filename}",
                "detail": (
                    f"Tipo {upload.get_file_type_detected_display()} · "
                    f"Estado {upload.get_status_display()}"
                ),
                "user": _upload_actor(upload),
                "kind": "upload",
            }
        )
        for log in upload.logs.all().order_by("-created_at")[:10]:
            entries.append(
                {
                    "at": log.created_at,
                    "level": log.level,
                    "title": log.step_code or "Importación",
                    "detail": log.message,
                    "user": _upload_actor(upload),
                    "kind": "log",
                }
            )

    entries.sort(key=lambda e: e["at"] or timezone.now(), reverse=True)

    for edit in AdminManualEditLog.objects.filter(
        year=year, month__gte=mf, month__lte=month
    ).select_related("edited_by")[:limit]:
        entries.append(
            {
                "at": edit.created_at,
                "level": "INFO",
                "title": f"Edición manual: {edit.get_entity_type_display()}",
                "detail": (
                    f"{edit.field_name}: {edit.old_value or '—'} → {edit.new_value or '—'}"
                    + (f" · Motivo: {edit.reason}" if edit.reason else "")
                ),
                "user": edit.edited_by.username if edit.edited_by else None,
                "kind": "manual_edit",
            }
        )

    entries.sort(key=lambda e: e["at"] or timezone.now(), reverse=True)
    return entries[:limit]


def recalculate_period(year: int, month: int) -> list[str]:
    messages_out: list[str] = []
    call_command("recalc_investment_ingresos_from_new_clients", year=year, month=month)
    messages_out.append(f"Ingresos Investment recalculados para {_period_label(year, month)}.")
    for mode in ("modo1", "modo2"):
        call_command("recalc_pgc", year=year, month=month, mode=mode)
    messages_out.append(f"Score PGC recalculado (modo1 y modo2) para {_period_label(year, month)}.")
    return messages_out


def recalculate_block(year: int, month: int, block_type: str) -> list[str]:
    label = _period_label(year, month)
    if block_type == BLOCK_NEW_CLIENTS:
        call_command("recalc_investment_ingresos_from_new_clients", year=year, month=month)
        return [f"Ingresos Investment recalculados para {label}."]
    if block_type in (BLOCK_FINANCIAL, BLOCK_CROSS_SALE, BLOCK_MANUAL_REQUIREMENTS, BLOCK_REVIEW):
        call_command("recalc_pgc", year=year, month=month, mode="modo1")
        return [f"Score PGC recalculado para {label}."]
    if block_type == BLOCK_TARGETS:
        return ["Las metas no requieren recálculo."]
    return ["Operación no aplicable a este bloque."]
