# CONCATENATED .PY FILES

PART_NUMBER=6
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
PATH_LITERAL=pgc/admin_period.py
PATH_JSON="pgc/admin_period.py"
FILENAME=admin_period.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=777
SIZE_BYTES_UTF8=27972
CONTENT_SHA256=f24ee922112564f42b6596d0d7fd7c428e82ff87828e120d35b4e3870a5cf54b
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

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Servicios agregados para el tablero de Administración mensual.
00003|"""
00004|
00005|from __future__ import annotations
00006|
00007|from datetime import datetime
00008|from decimal import Decimal
00009|from typing import Any
00010|
00011|from django.core.management import call_command
00012|from django.db import transaction
00013|from django.db.models import Count, Q
00014|from django.utils import timezone
00015|
00016|from core.models import MetricDefinition, UNE, UNEAlias
00017|from imports.models import (
00018|    CrossSaleImportHeader,
00019|    CrossSaleImportRow,
00020|    FileUpload,
00021|    FinancialStatementImportHeader,
00022|    NewClientImportHeader,
00023|    NewClientImportRow,
00024|    StationTimeImportHeader,
00025|)
00026|from pgc.models import (
00027|    AdminManualEditLog,
00028|    ManualRequirementsCompliance,
00029|    MonthlyExchangeRate,
00030|    MonthlyMetricResult,
00031|    MonthlyModeScorecard,
00032|    MonthlyTarget,
00033|    PGCPlan,
00034|)
00035|
00036|from .admin_manual import log_manual_edit
00037|
00038|# Bloques del tablero (orden visual)
00039|BLOCK_TARGETS = "targets"
00040|BLOCK_FINANCIAL = "financial"
00041|BLOCK_NEW_CLIENTS = "new_clients"
00042|BLOCK_CROSS_SALE = "cross_sale"
00043|BLOCK_MANUAL_REQUIREMENTS = "manual_requirements"
00044|BLOCK_REVIEW = "review"
00045|
00046|BLOCK_ORDER = (
00047|    BLOCK_TARGETS,
00048|    BLOCK_FINANCIAL,
00049|    BLOCK_NEW_CLIENTS,
00050|    BLOCK_CROSS_SALE,
00051|    BLOCK_MANUAL_REQUIREMENTS,
00052|    BLOCK_REVIEW,
00053|)
00054|
00055|BLOCK_META = {
00056|    BLOCK_TARGETS: {"step": 1, "label": "Metas", "short": "Metas mensuales del plan"},
00057|    BLOCK_FINANCIAL: {"step": 2, "label": "Estados de resultados", "short": "Ingresos por UNE (WC*)"},
00058|    BLOCK_NEW_CLIENTS: {"step": 3, "label": "Clientes nuevos", "short": "Archivo de clientes nuevos"},
00059|    BLOCK_CROSS_SALE: {"step": 4, "label": "Venta cruzada", "short": "Referencias entre UNEs"},
00060|    BLOCK_MANUAL_REQUIREMENTS: {
00061|        "step": 5,
00062|        "label": "Requerimientos manuales",
00063|        "short": "Cumplimiento de respuesta a requerimientos",
00064|    },
00065|    BLOCK_REVIEW: {"step": 6, "label": "Revisar resultado", "short": "Score y tablero del período"},
00066|}
00067|
00068|STATUS_PENDING = "pending"
00069|STATUS_LOADED = "loaded"
00070|STATUS_OBSERVED = "observed"
00071|STATUS_REVIEWED = "reviewed"
00072|STATUS_CLOSED = "closed"
00073|
00074|STATUS_LABELS = {
00075|    STATUS_PENDING: "Pendiente",
00076|    STATUS_LOADED: "Cargado",
00077|    STATUS_OBSERVED: "Con observaciones",
00078|    STATUS_REVIEWED: "Revisado",
00079|    STATUS_CLOSED: "Cerrado",
00080|}
00081|
00082|PERIOD_INCOMPLETE = "incomplete"
00083|PERIOD_IN_REVIEW = "in_review"
00084|PERIOD_READY = "ready"
00085|PERIOD_CLOSED = "closed"
00086|
00087|PERIOD_STATUS_LABELS = {
00088|    PERIOD_INCOMPLETE: "Incompleto",
00089|    PERIOD_IN_REVIEW: "En revisión",
00090|    PERIOD_READY: "Listo",
00091|    PERIOD_CLOSED: "Cerrado",
00092|}
00093|
00094|INGRESOS_UNES = ("FACTORING", "FACTORAJE", "LEASING", "INSURANCE")
00095|METRIC_CODES = (
00096|    MetricDefinition.CODE_INGRESOS,
00097|    MetricDefinition.CODE_CLIENTES_NUEVOS,
00098|    MetricDefinition.CODE_VENTA_CRUZADA,
00099|    MetricDefinition.CODE_RESPUESTA_REQS,
00100|)
00101|
00102|
00103|def _period_label(year: int, month: int) -> str:
00104|    return f"{year}-{month:02d}"
00105|
00106|
00107|def _status_badge(status: str) -> str:
00108|    return STATUS_LABELS.get(status, status)
00109|
00110|
00111|def _get_plan(year: int) -> PGCPlan | None:
00112|    return PGCPlan.objects.filter(year=year).first()
00113|
00114|
00115|def _latest_upload_for_period(year: int, month: int, file_type: str) -> FileUpload | None:
00116|    return (
00117|        FileUpload.objects.filter(
00118|            detected_year=year,
00119|            detected_month=month,
00120|            file_type_detected=file_type,
00121|        )
00122|        .select_related("uploaded_by")
00123|        .order_by("-created_at")
00124|        .first()
00125|    )
00126|
00127|
00128|def _upload_actor(upload: FileUpload | None) -> str | None:
00129|    if upload and upload.uploaded_by:
00130|        return upload.uploaded_by.username
00131|    return None
00132|
00133|
00134|def _upload_timestamp(upload: FileUpload | None) -> datetime | None:
00135|    if upload:
00136|        return upload.updated_at or upload.created_at
00137|    return None
00138|
00139|
00140|def _count_pending_aliases(year: int, month: int) -> int:
00141|    known = {a.raw_value.strip().upper() for a in UNEAlias.objects.filter(is_active=True)}
00142|    pending = set()
00143|
00144|    for raw in (
00145|        NewClientImportRow.objects.filter(year=year, month=month)
00146|        .exclude(raw_une_value="")
00147|        .values_list("raw_une_value", flat=True)
00148|    ):
00149|        key = (raw or "").strip().upper()
00150|        if key and key not in known:
00151|            pending.add(key)
00152|
00153|    for raw_dest, raw_orig in CrossSaleImportRow.objects.filter(
00154|        year=year, month=month
00155|    ).values_list("raw_une_destination", "raw_une_origin"):
00156|        for raw in (raw_dest, raw_orig):
00157|            key = (raw or "").strip().upper()
00158|            if key and key not in known:
00159|                pending.add(key)
00160|
00161|    unresolved_cross = CrossSaleImportRow.objects.filter(
00162|        year=year, month=month
00163|    ).filter(Q(une_destination__isnull=True) | Q(une_origin__isnull=True)).count()
00164|
00165|    return len(pending) + unresolved_cross
00166|
00167|
00168|def _block_targets(plan: PGCPlan | None, year: int, month: int) -> dict[str, Any]:
00169|    if not plan:
00170|        return _empty_block(BLOCK_TARGETS, "No hay plan PGC para este año.")
00171|
00172|    count = MonthlyTarget.objects.filter(plan=plan, year=year, month=month).count()
00173|    active_unes = UNE.objects.filter(is_active=True).count()
00174|    expected = active_unes * len(METRIC_CODES)
00175|
00176|    status = STATUS_LOADED if count >= expected else STATUS_PENDING
00177|    summary = f"{count} metas registradas"
00178|
00179|    return {
00180|        **_block_shell(BLOCK_TARGETS),
00181|        "status": status,
00182|        "status_label": _status_badge(status),
00183|        "summary": summary,
00184|        "last_action_at": None,
00185|        "last_action_by": None,
00186|        "checklist": [
00187|            {"label": "Metas del plan cargadas", "done": count > 0},
00188|            {"label": "Cobertura completa por UNE y métrica", "done": count >= expected},
00189|        ],
00190|        "stats": {"targets_count": count, "expected": expected},
00191|    }
00192|
00193|
00194|def _block_financial(plan: PGCPlan | None, year: int, month: int) -> dict[str, Any]:
00195|    upload = _latest_upload_for_period(year, month, FileUpload.TYPE_FINANCIAL)
00196|    headers = FinancialStatementImportHeader.objects.filter(year=year, month=month)
00197|    header_count = headers.count()
00198|
00199|    ingresos_metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
00200|    results_count = 0
00201|    if plan and ingresos_metric:
00202|        results_count = MonthlyMetricResult.objects.filter(
00203|            plan=plan,
00204|            metric=ingresos_metric,
00205|            year=year,
00206|            month=month,
00207|            une__code__in=INGRESOS_UNES,
00208|            measured_value__isnull=False,
00209|        ).count()
00210|
00211|    has_fx = MonthlyExchangeRate.objects.filter(year=year, month=month).exists()
00212|    has_error = upload and upload.status == FileUpload.STATUS_PARSED_ERROR
00213|
00214|    if has_error:
00215|        status = STATUS_OBSERVED
00216|    elif results_count >= 3:
00217|        status = STATUS_LOADED
00218|    elif upload or header_count:
00219|        status = STATUS_OBSERVED
00220|    else:
00221|        status = STATUS_PENDING
00222|
00223|    summary_parts = []
00224|    if upload:
00225|        summary_parts.append(upload.original_filename)
00226|    summary_parts.append(f"{results_count}/3 UNEs con ingreso")
00227|    if not has_fx:
00228|        summary_parts.append("falta tipo de cambio")
00229|
00230|    return {
00231|        **_block_shell(BLOCK_FINANCIAL),
00232|        "status": status,
00233|        "status_label": _status_badge(status),
00234|        "summary": " · ".join(summary_parts),
00235|        "last_action_at": _upload_timestamp(upload),
00236|        "last_action_by": _upload_actor(upload),
00237|        "checklist": [
00238|            {"label": "Tipo de cambio del mes", "done": has_fx},
00239|            {"label": "Archivo(s) WC* subido(s)", "done": bool(upload)},
00240|            {"label": "Ingresos importados (Factoring, Leasing, Insurance)", "done": results_count >= 3},
00241|            {"label": "Sin errores de lectura", "done": not has_error},
00242|        ],
00243|        "stats": {
00244|            "upload_id": upload.id if upload else None,
00245|            "results_count": results_count,
00246|            "has_fx": has_fx,
00247|        },
00248|        "uploads": _period_uploads(year, month, FileUpload.TYPE_FINANCIAL),
00249|    }
00250|
00251|
00252|def _new_client_row_dedup_key(row: NewClientImportRow) -> tuple:
00253|    # counts_as_new is derived; ignore it so Sí/No twins count as duplicates.
00254|    return (
00255|        row.une_id,
00256|        (row.client_name or "").strip().casefold(),
00257|        (row.nit or "").strip(),
00258|        (row.operation_code or "").strip(),
00259|        row.previous_contracts,
00260|        row.currency_id,
00261|        str(row.amount) if row.amount is not None else "",
00262|    )
00263|
00264|
00265|def count_duplicate_new_client_rows(year: int, month: int) -> int:
00266|    """Cuenta filas duplicadas en el detalle de clientes nuevos del período."""
00267|    seen: set[tuple] = set()
00268|    duplicate_ids: list[int] = []
00269|    for row in NewClientImportRow.objects.filter(year=year, month=month).order_by("id"):
00270|        key = _new_client_row_dedup_key(row)
00271|        if key in seen:
00272|            duplicate_ids.append(row.id)
00273|        else:
00274|            seen.add(key)
00275|    return len(duplicate_ids)
00276|
00277|
00278|def _sync_clientes_nuevos_metrics_from_rows(year: int, month: int) -> int:
00279|    """Actualiza CLIENTES_NUEVOS desde las filas vigentes del período."""
00280|    plan = _get_plan(year)
00281|    if not plan:
00282|        return 0
00283|
00284|    metric = MetricDefinition.objects.get(code=MetricDefinition.CODE_CLIENTES_NUEVOS)
00285|    counts = {
00286|        row["une_id"]: row["cnt"]
00287|        for row in NewClientImportRow.objects.filter(year=year, month=month, counts_as_new=True)
00288|        .values("une_id")
00289|        .annotate(cnt=Count("id"))
00290|    }
00291|
00292|    updated = 0
00293|    for une in UNE.objects.filter(is_active=True):
00294|        count = counts.get(une.id, 0)
00295|        try:
00296|            target = MonthlyTarget.objects.get(
00297|                plan=plan,
00298|                une=une,
00299|                metric=metric,
00300|                year=year,
00301|                month=month,
00302|            )
00303|        except MonthlyTarget.DoesNotExist:
00304|            continue
00305|
00306|        mmr, _ = MonthlyMetricResult.objects.get_or_create(
00307|            plan=plan,
00308|            une=une,
00309|            metric=metric,
00310|            year=year,
00311|            month=month,
00312|            defaults={"target_value": target.target_value},
00313|        )
00314|        mmr.target_value = target.target_value
00315|        mmr.measured_value = Decimal(str(count))
00316|        mmr.calculation_note = f"{count} clientes nuevos contados desde filas del período"
00317|        mmr.save()
00318|        updated += 1
00319|    return updated
00320|
00321|
00322|@transaction.atomic
00323|def remove_duplicate_new_client_rows(year: int, month: int, user=None) -> dict[str, int]:
00324|    """
00325|    Elimina filas duplicadas del detalle de clientes nuevos (conserva la más antigua).
00326|    Opcionalmente sincroniza la métrica CLIENTES_NUEVOS.
00327|    """
00328|    seen: set[tuple] = set()
00329|    duplicate_ids: list[int] = []
00330|    for row in NewClientImportRow.objects.filter(year=year, month=month).order_by("id"):
00331|        key = _new_client_row_dedup_key(row)
00332|        if key in seen:
00333|            duplicate_ids.append(row.id)
00334|        else:
00335|            seen.add(key)
00336|
00337|    removed = NewClientImportRow.objects.filter(id__in=duplicate_ids).delete()[0]
00338|    metrics_updated = 0
00339|    if removed:
00340|        metrics_updated = _sync_clientes_nuevos_metrics_from_rows(year, month)
00341|        if user:
00342|            log_manual_edit(
00343|                user=user,
00344|                year=year,
00345|                month=month,
00346|                entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
00347|                entity_id=0,
00348|                field_name="dedup",
00349|                old_value=f"{removed} duplicados",
00350|                new_value="eliminados",
00351|                reason="Depuración de duplicados en detalle de clientes nuevos",
00352|            )
00353|    return {"removed": removed, "metrics_updated": metrics_updated}
00354|
00355|
00356|def _repoint_import_header_away_from_upload(upload: FileUpload) -> None:
00357|    """
00358|    Antes de borrar un FileUpload pendiente: si un encabezado lo apunta,
00359|    reasigna a otro archivo del período o elimina el encabezado vacío.
00360|    Nunca deja cascada sobre filas ya importadas.
00361|    """
00362|    specs: list[tuple[type, str, type | None]] = [
00363|        (NewClientImportHeader, FileUpload.TYPE_NEW_CLIENTS, NewClientImportRow),
00364|        (CrossSaleImportHeader, FileUpload.TYPE_CROSS_SALE, CrossSaleImportRow),
00365|        (StationTimeImportHeader, FileUpload.TYPE_STATION_TIMES, None),
00366|        (FinancialStatementImportHeader, FileUpload.TYPE_FINANCIAL, None),
00367|    ]
00368|    for header_model, file_type, row_model in specs:
00369|        headers = list(header_model.objects.filter(file_upload=upload))
00370|        for header in headers:
00371|            year = getattr(header, "year", upload.detected_year)
00372|            month = getattr(header, "month", upload.detected_month)
00373|            alt_qs = FileUpload.objects.filter(
00374|                file_type_detected=file_type,
00375|            ).exclude(pk=upload.pk)
00376|            if year is not None:
00377|                alt_qs = alt_qs.filter(detected_year=year)
00378|            if month is not None:
00379|                alt_qs = alt_qs.filter(detected_month=month)
00380|            alt = (
00381|                alt_qs.filter(status=FileUpload.STATUS_PARSED_OK)
00382|                .order_by("-created_at")
00383|                .first()
00384|                or alt_qs.order_by("-created_at").first()
00385|            )
00386|
00387|            has_rows = False
00388|            if row_model is not None:
00389|                has_rows = row_model.objects.filter(header=header).exists()
00390|
00391|            if alt is not None:
00392|                header.file_upload = alt
00393|                header.save(update_fields=["file_upload"])
00394|            elif has_rows:
00395|                raise ValueError(
00396|                    "No se puede quitar de la cola: el período ya tiene datos importados "
00397|                    "y no hay otro archivo procesado al cual conservar el vínculo."
00398|                )
00399|            else:
00400|                header.delete()
00401|
00402|
00403|@transaction.atomic
00404|def discard_pending_upload(upload: FileUpload) -> dict[str, Any]:
00405|    """
00406|    Elimina de la cola un archivo pendiente de procesar.
00407|    Solo UPLOADED / PARSED_ERROR. No toca PARSED_OK ni filas ya cargadas.
00408|    """
00409|    if upload.status == FileUpload.STATUS_PARSED_OK:
00410|        raise ValueError(
00411|            "Este archivo ya fue procesado; no se puede quitar de la cola."
00412|        )
00413|
00414|    filename = upload.original_filename
00415|    _repoint_import_header_away_from_upload(upload)
00416|
00417|    if upload.stored_file:
00418|        try:
00419|            upload.stored_file.delete(save=False)
00420|        except Exception:
00421|            pass
00422|    upload.delete()
00423|    return {"filename": filename, "ok": True}
00424|
00425|
00426|def _block_new_clients(plan: PGCPlan | None, year: int, month: int) -> dict[str, Any]:
00427|    upload = _latest_upload_for_period(year, month, FileUpload.TYPE_NEW_CLIENTS)
00428|    header = NewClientImportHeader.objects.filter(year=year, month=month).first()
00429|    rows_qs = NewClientImportRow.objects.filter(year=year, month=month)
00430|    valid_rows = rows_qs.filter(counts_as_new=True).count()
00431|    obs_rows = rows_qs.exclude(observations="").count()
00432|    duplicate_rows = count_duplicate_new_client_rows(year, month)
00433|    has_error = upload and upload.status == FileUpload.STATUS_PARSED_ERROR
00434|
00435|    if has_error or obs_rows:
00436|        status = STATUS_OBSERVED
00437|    elif header and valid_rows > 0:
00438|        status = STATUS_LOADED
00439|    elif upload:
00440|        status = STATUS_OBSERVED
00441|    else:
00442|        status = STATUS_PENDING
00443|
00444|    return {
00445|        **_block_shell(BLOCK_NEW_CLIENTS),
00446|        "status": status,
00447|        "status_label": _status_badge(status),
00448|        "summary": f"{valid_rows} clientes válidos" if valid_rows else "Sin datos procesados",
00449|        "last_action_at": _upload_timestamp(upload) or (header.updated_at if header else None),
00450|        "last_action_by": _upload_actor(upload),
00451|        "checklist": [
00452|            {"label": "Archivo subido", "done": bool(upload)},
00453|            {"label": "Estructura validada", "done": bool(header)},
00454|            {"label": "Filas importadas", "done": valid_rows > 0},
00455|            {"label": "Sin observaciones pendientes", "done": obs_rows == 0},
00456|        ],
00457|        "stats": {
00458|            "valid_rows": valid_rows,
00459|            "obs_rows": obs_rows,
00460|            "duplicate_rows": duplicate_rows,
00461|            "upload_id": upload.id if upload else None,
00462|        },
00463|        "uploads": _period_uploads(year, month, FileUpload.TYPE_NEW_CLIENTS),
00464|    }
00465|
00466|
00467|def _block_cross_sale(plan: PGCPlan | None, year: int, month: int) -> dict[str, Any]:
00468|    upload = _latest_upload_for_period(year, month, FileUpload.TYPE_CROSS_SALE)
00469|    header = CrossSaleImportHeader.objects.filter(year=year, month=month).first()
00470|    rows_count = CrossSaleImportRow.objects.filter(year=year, month=month).count()
00471|    unresolved = CrossSaleImportRow.objects.filter(year=year, month=month).filter(
00472|        Q(une_destination__isnull=True) | Q(une_origin__isnull=True)
00473|    ).count()
00474|    has_error = upload and upload.status == FileUpload.STATUS_PARSED_ERROR
00475|
00476|    if has_error or unresolved:
00477|        status = STATUS_OBSERVED
00478|    elif header and rows_count > 0:
00479|        status = STATUS_LOADED
00480|    elif upload:
00481|        status = STATUS_OBSERVED
00482|    else:
00483|        status = STATUS_PENDING
00484|
00485|    return {
00486|        **_block_shell(BLOCK_CROSS_SALE),
00487|        "status": status,
00488|        "status_label": _status_badge(status),
00489|        "summary": f"{rows_count} referencias" if rows_count else "Sin datos procesados",
00490|        "last_action_at": _upload_timestamp(upload) or (header.updated_at if header else None),
00491|        "last_action_by": _upload_actor(upload),
00492|        "checklist": [
00493|            {"label": "Archivo subido", "done": bool(upload)},
00494|            {"label": "Filas importadas", "done": rows_count > 0},
00495|            {"label": "UNE destino/origen resueltos", "done": unresolved == 0 and rows_count > 0},
00496|            {"label": "Sin errores de lectura", "done": not has_error},
00497|        ],
00498|        "stats": {"rows_count": rows_count, "unresolved": unresolved, "upload_id": upload.id if upload else None},
00499|        "uploads": _period_uploads(year, month, FileUpload.TYPE_CROSS_SALE),
00500|    }
00501|
00502|
00503|def _block_manual_requirements(plan: PGCPlan | None, year: int, month: int) -> dict[str, Any]:
00504|    if not plan:
00505|        return _empty_block(BLOCK_MANUAL_REQUIREMENTS, "No hay plan PGC.")
00506|
00507|    unes = list(UNE.objects.filter(is_active=True))
00508|    records = {
00509|        r.une_id: r
00510|        for r in ManualRequirementsCompliance.objects.filter(plan=plan, year=year, month=month)
00511|    }
00512|    non_compliant = [r for r in records.values() if not r.is_compliant]
00513|    filled = len(records)
00514|
00515|    if non_compliant:
00516|        status = STATUS_OBSERVED
00517|    elif filled >= len(unes):
00518|        status = STATUS_LOADED
00519|    else:
00520|        status = STATUS_PENDING
00521|
00522|    latest = (
00523|        ManualRequirementsCompliance.objects.filter(plan=plan, year=year, month=month)
00524|        .order_by("-updated_at")
00525|        .first()
00526|    )
00527|
00528|    return {
00529|        **_block_shell(BLOCK_MANUAL_REQUIREMENTS),
00530|        "status": status,
00531|        "status_label": _status_badge(status),
00532|        "summary": f"{filled}/{len(unes)} UNEs registradas",
00533|        "last_action_at": latest.updated_at if latest else None,
00534|        "last_action_by": None,
00535|        "checklist": [
00536|            {"label": "Registro por UNE", "done": filled >= len(unes)},
00537|            {"label": "Sin incidencias reportadas", "done": not non_compliant},
00538|        ],
00539|        "stats": {"filled": filled, "total_unes": len(unes), "non_compliant": len(non_compliant)},
00540|    }
00541|
00542|
00543|def _block_review(plan: PGCPlan | None, year: int, month: int) -> dict[str, Any]:
00544|    if not plan:
00545|        return _empty_block(BLOCK_REVIEW, "No hay plan PGC.")
00546|
00547|    scorecards = MonthlyModeScorecard.objects.filter(plan=plan, year=year, month=month)
00548|    count = scorecards.count()
00549|    latest = scorecards.order_by("-updated_at").first()
00550|
00551|    if count >= UNE.objects.filter(is_active=True).count():
00552|        status = STATUS_REVIEWED
00553|    elif count > 0:
00554|        status = STATUS_LOADED
00555|    else:
00556|        status = STATUS_PENDING
00557|
00558|    return {
00559|        **_block_shell(BLOCK_REVIEW),
00560|        "status": status,
00561|        "status_label": _status_badge(status),
00562|        "summary": f"Score actualizado ({count} UNEs)" if count else "Sin recálculo",
00563|        "last_action_at": latest.updated_at if latest else None,
00564|        "last_action_by": None,
00565|        "checklist": [
00566|            {"label": "Ingresos Investment recalculados", "done": _investment_ingresos_ready(plan, year, month)},
00567|            {"label": "Score PGC generado", "done": count > 0},
00568|            {"label": "Todas las UNEs con score", "done": count >= UNE.objects.filter(is_active=True).count()},
00569|        ],
00570|        "stats": {"scorecard_count": count},
00571|    }
00572|
00573|
00574|def _investment_ingresos_ready(plan: PGCPlan, year: int, month: int) -> bool:
00575|    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
00576|    une = UNE.objects.filter(code__in=["INVESTMENT", "INVESTMENTS", "INVERSIONES"]).first()
00577|    if not metric or not une:
00578|        return False
00579|    return MonthlyMetricResult.objects.filter(
00580|        plan=plan, metric=metric, une=une, year=year, month=month, measured_value__isnull=False
00581|    ).exists()
00582|
00583|
00584|def _empty_block(block_id: str, summary: str) -> dict[str, Any]:
00585|    return {
00586|        **_block_shell(block_id),
00587|        "status": STATUS_PENDING,
00588|        "status_label": _status_badge(STATUS_PENDING),
00589|        "summary": summary,
00590|        "last_action_at": None,
00591|        "last_action_by": None,
00592|        "checklist": [],
00593|        "stats": {},
00594|        "uploads": [],
00595|    }
00596|
00597|
00598|def _block_shell(block_id: str) -> dict[str, Any]:
00599|    meta = BLOCK_META[block_id]
00600|    return {
00601|        "id": block_id,
00602|        "step": meta["step"],
00603|        "label": meta["label"],
00604|        "short": meta["short"],
00605|    }
00606|
00607|
00608|def _period_uploads(year: int, month: int, file_type: str) -> list[dict[str, Any]]:
00609|    uploads = FileUpload.objects.filter(
00610|        detected_year=year,
00611|        detected_month=month,
00612|        file_type_detected=file_type,
00613|    ).select_related("uploaded_by").order_by("-created_at")[:5]
00614|    return [
00615|        {
00616|            "id": u.id,
00617|            "filename": u.original_filename,
00618|            "status": u.status,
00619|            "status_display": u.get_status_display(),
00620|            "created_at": u.created_at,
00621|            "user": _upload_actor(u),
00622|            "can_discard": u.status != FileUpload.STATUS_PARSED_OK,
00623|        }
00624|        for u in uploads
00625|    ]
00626|
00627|
00628|def _derive_period_status(blocks: list[dict[str, Any]]) -> tuple[str, str]:
00629|    statuses = [b["status"] for b in blocks]
00630|    if all(s in (STATUS_REVIEWED, STATUS_CLOSED) for s in statuses):
00631|        return PERIOD_CLOSED, PERIOD_STATUS_LABELS[PERIOD_CLOSED]
00632|    if all(s in (STATUS_LOADED, STATUS_REVIEWED, STATUS_OBSERVED, STATUS_CLOSED) for s in statuses):
00633|        if STATUS_OBSERVED in statuses or STATUS_PENDING in statuses:
00634|            return PERIOD_IN_REVIEW, PERIOD_STATUS_LABELS[PERIOD_IN_REVIEW]
00635|        return PERIOD_READY, PERIOD_STATUS_LABELS[PERIOD_READY]
00636|    if any(s != STATUS_PENDING for s in statuses):
00637|        return PERIOD_IN_REVIEW, PERIOD_STATUS_LABELS[PERIOD_IN_REVIEW]
00638|    return PERIOD_INCOMPLETE, PERIOD_STATUS_LABELS[PERIOD_INCOMPLETE]
00639|
00640|
00641|def get_admin_period_snapshot(year: int, month: int) -> dict[str, Any]:
00642|    plan = _get_plan(year)
00643|    blocks = [
00644|        _block_targets(plan, year, month),
00645|        _block_financial(plan, year, month),
00646|        _block_new_clients(plan, year, month),
00647|        _block_cross_sale(plan, year, month),
00648|        _block_manual_requirements(plan, year, month),
00649|        _block_review(plan, year, month),
00650|    ]
00651|    period_status, period_status_label = _derive_period_status(blocks)
00652|
00653|    uploads = FileUpload.objects.filter(detected_year=year, detected_month=month)
00654|    valid_rows = (
00655|        NewClientImportRow.objects.filter(year=year, month=month, counts_as_new=True).count()
00656|        + CrossSaleImportRow.objects.filter(year=year, month=month).count()
00657|    )
00658|    obs_rows = NewClientImportRow.objects.filter(year=year, month=month).exclude(observations="").count()
00659|    pending_aliases = _count_pending_aliases(year, month)
00660|
00661|    score_latest = None
00662|    if plan:
00663|        sc = (
00664|            MonthlyModeScorecard.objects.filter(plan=plan, year=year, month=month)
00665|            .order_by("-updated_at")
00666|            .first()
00667|        )
00668|        score_latest = sc.updated_at if sc else None
00669|
00670|    return {
00671|        "year": year,
00672|        "month": month,
00673|        "label": _period_label(year, month),
00674|        "plan": plan,
00675|        "period_status": period_status,
00676|        "period_status_label": period_status_label,
00677|        "blocks": blocks,
00678|        "blocks_by_id": {b["id"]: b for b in blocks},
00679|        "summary": {
00680|            "files_loaded": uploads.count(),
00681|            "valid_rows": valid_rows,
00682|            "rows_with_observations": obs_rows,
00683|            "pending_aliases": pending_aliases,
00684|            "metrics_recalculated": score_latest is not None,
00685|            "last_score_update": score_latest,
00686|        },
00687|    }
00688|
00689|
00690|def list_period_log(
00691|    year: int,
00692|    month: int,
00693|    limit: int = 50,
00694|    month_from: int | None = None,
00695|) -> list[dict[str, Any]]:
00696|    entries: list[dict[str, Any]] = []
00697|    mf = month_from or month
00698|
00699|    uploads = (
00700|        FileUpload.objects.filter(
00701|            detected_year=year,
00702|            detected_month__gte=mf,
00703|            detected_month__lte=month,
00704|        )
00705|        .select_related("uploaded_by")
00706|        .order_by("-created_at")
00707|    )
00708|    for upload in uploads[:limit]:
00709|        entries.append(
00710|            {
00711|                "at": upload.created_at,
00712|                "level": "INFO",
00713|                "title": f"Archivo: {upload.original_filename}",
00714|                "detail": (
00715|                    f"Tipo {upload.get_file_type_detected_display()} · "
00716|                    f"Estado {upload.get_status_display()}"
00717|                ),
00718|                "user": _upload_actor(upload),
00719|                "kind": "upload",
00720|            }
00721|        )
00722|        for log in upload.logs.all().order_by("-created_at")[:10]:
00723|            entries.append(
00724|                {
00725|                    "at": log.created_at,
00726|                    "level": log.level,
00727|                    "title": log.step_code or "Importación",
00728|                    "detail": log.message,
00729|                    "user": _upload_actor(upload),
00730|                    "kind": "log",
00731|                }
00732|            )
00733|
00734|    entries.sort(key=lambda e: e["at"] or timezone.now(), reverse=True)
00735|
00736|    for edit in AdminManualEditLog.objects.filter(
00737|        year=year, month__gte=mf, month__lte=month
00738|    ).select_related("edited_by")[:limit]:
00739|        entries.append(
00740|            {
00741|                "at": edit.created_at,
00742|                "level": "INFO",
00743|                "title": f"Edición manual: {edit.get_entity_type_display()}",
00744|                "detail": (
00745|                    f"{edit.field_name}: {edit.old_value or '—'} → {edit.new_value or '—'}"
00746|                    + (f" · Motivo: {edit.reason}" if edit.reason else "")
00747|                ),
00748|                "user": edit.edited_by.username if edit.edited_by else None,
00749|                "kind": "manual_edit",
00750|            }
00751|        )
00752|
00753|    entries.sort(key=lambda e: e["at"] or timezone.now(), reverse=True)
00754|    return entries[:limit]
00755|
00756|
00757|def recalculate_period(year: int, month: int) -> list[str]:
00758|    messages_out: list[str] = []
00759|    call_command("recalc_investment_ingresos_from_new_clients", year=year, month=month)
00760|    messages_out.append(f"Ingresos Investment recalculados para {_period_label(year, month)}.")
00761|    for mode in ("modo1", "modo2"):
00762|        call_command("recalc_pgc", year=year, month=month, mode=mode)
00763|    messages_out.append(f"Score PGC recalculado (modo1 y modo2) para {_period_label(year, month)}.")
00764|    return messages_out
00765|
00766|
00767|def recalculate_block(year: int, month: int, block_type: str) -> list[str]:
00768|    label = _period_label(year, month)
00769|    if block_type == BLOCK_NEW_CLIENTS:
00770|        call_command("recalc_investment_ingresos_from_new_clients", year=year, month=month)
00771|        return [f"Ingresos Investment recalculados para {label}."]
00772|    if block_type in (BLOCK_FINANCIAL, BLOCK_CROSS_SALE, BLOCK_MANUAL_REQUIREMENTS, BLOCK_REVIEW):
00773|        call_command("recalc_pgc", year=year, month=month, mode="modo1")
00774|        return [f"Score PGC recalculado para {label}."]
00775|    if block_type == BLOCK_TARGETS:
00776|        return ["Las metas no requieren recálculo."]
00777|    return ["Operación no aplicable a este bloque."]

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiClNlcnZpY2lvcyBhZ3JlZ2Fkb3MgcGFyYSBlbCB0YWJsZXJvIGRlIEFkbWluaXN0cmFjacOzbiBtZW5zdWFsLgoiIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmZyb20gZGF0ZXRpbWUgaW1wb3J0IGRhdGV0aW1lCmZyb20gZGVjaW1hbCBpbXBvcnQgRGVjaW1hbApmcm9tIHR5cGluZyBpbXBvcnQgQW55Cgpmcm9tIGRqYW5nby5jb3JlLm1hbmFnZW1lbnQgaW1wb3J0IGNhbGxfY29tbWFuZApmcm9tIGRqYW5nby5kYiBpbXBvcnQgdHJhbnNhY3Rpb24KZnJvbSBkamFuZ28uZGIubW9kZWxzIGltcG9ydCBDb3VudCwgUQpmcm9tIGRqYW5nby51dGlscyBpbXBvcnQgdGltZXpvbmUKCmZyb20gY29yZS5tb2RlbHMgaW1wb3J0IE1ldHJpY0RlZmluaXRpb24sIFVORSwgVU5FQWxpYXMKZnJvbSBpbXBvcnRzLm1vZGVscyBpbXBvcnQgKAogICAgQ3Jvc3NTYWxlSW1wb3J0SGVhZGVyLAogICAgQ3Jvc3NTYWxlSW1wb3J0Um93LAogICAgRmlsZVVwbG9hZCwKICAgIEZpbmFuY2lhbFN0YXRlbWVudEltcG9ydEhlYWRlciwKICAgIE5ld0NsaWVudEltcG9ydEhlYWRlciwKICAgIE5ld0NsaWVudEltcG9ydFJvdywKICAgIFN0YXRpb25UaW1lSW1wb3J0SGVhZGVyLAopCmZyb20gcGdjLm1vZGVscyBpbXBvcnQgKAogICAgQWRtaW5NYW51YWxFZGl0TG9nLAogICAgTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZSwKICAgIE1vbnRobHlFeGNoYW5nZVJhdGUsCiAgICBNb250aGx5TWV0cmljUmVzdWx0LAogICAgTW9udGhseU1vZGVTY29yZWNhcmQsCiAgICBNb250aGx5VGFyZ2V0LAogICAgUEdDUGxhbiwKKQoKZnJvbSAuYWRtaW5fbWFudWFsIGltcG9ydCBsb2dfbWFudWFsX2VkaXQKCiMgQmxvcXVlcyBkZWwgdGFibGVybyAob3JkZW4gdmlzdWFsKQpCTE9DS19UQVJHRVRTID0gInRhcmdldHMiCkJMT0NLX0ZJTkFOQ0lBTCA9ICJmaW5hbmNpYWwiCkJMT0NLX05FV19DTElFTlRTID0gIm5ld19jbGllbnRzIgpCTE9DS19DUk9TU19TQUxFID0gImNyb3NzX3NhbGUiCkJMT0NLX01BTlVBTF9SRVFVSVJFTUVOVFMgPSAibWFudWFsX3JlcXVpcmVtZW50cyIKQkxPQ0tfUkVWSUVXID0gInJldmlldyIKCkJMT0NLX09SREVSID0gKAogICAgQkxPQ0tfVEFSR0VUUywKICAgIEJMT0NLX0ZJTkFOQ0lBTCwKICAgIEJMT0NLX05FV19DTElFTlRTLAogICAgQkxPQ0tfQ1JPU1NfU0FMRSwKICAgIEJMT0NLX01BTlVBTF9SRVFVSVJFTUVOVFMsCiAgICBCTE9DS19SRVZJRVcsCikKCkJMT0NLX01FVEEgPSB7CiAgICBCTE9DS19UQVJHRVRTOiB7InN0ZXAiOiAxLCAibGFiZWwiOiAiTWV0YXMiLCAic2hvcnQiOiAiTWV0YXMgbWVuc3VhbGVzIGRlbCBwbGFuIn0sCiAgICBCTE9DS19GSU5BTkNJQUw6IHsic3RlcCI6IDIsICJsYWJlbCI6ICJFc3RhZG9zIGRlIHJlc3VsdGFkb3MiLCAic2hvcnQiOiAiSW5ncmVzb3MgcG9yIFVORSAoV0MqKSJ9LAogICAgQkxPQ0tfTkVXX0NMSUVOVFM6IHsic3RlcCI6IDMsICJsYWJlbCI6ICJDbGllbnRlcyBudWV2b3MiLCAic2hvcnQiOiAiQXJjaGl2byBkZSBjbGllbnRlcyBudWV2b3MifSwKICAgIEJMT0NLX0NST1NTX1NBTEU6IHsic3RlcCI6IDQsICJsYWJlbCI6ICJWZW50YSBjcnV6YWRhIiwgInNob3J0IjogIlJlZmVyZW5jaWFzIGVudHJlIFVORXMifSwKICAgIEJMT0NLX01BTlVBTF9SRVFVSVJFTUVOVFM6IHsKICAgICAgICAic3RlcCI6IDUsCiAgICAgICAgImxhYmVsIjogIlJlcXVlcmltaWVudG9zIG1hbnVhbGVzIiwKICAgICAgICAic2hvcnQiOiAiQ3VtcGxpbWllbnRvIGRlIHJlc3B1ZXN0YSBhIHJlcXVlcmltaWVudG9zIiwKICAgIH0sCiAgICBCTE9DS19SRVZJRVc6IHsic3RlcCI6IDYsICJsYWJlbCI6ICJSZXZpc2FyIHJlc3VsdGFkbyIsICJzaG9ydCI6ICJTY29yZSB5IHRhYmxlcm8gZGVsIHBlcsOtb2RvIn0sCn0KClNUQVRVU19QRU5ESU5HID0gInBlbmRpbmciClNUQVRVU19MT0FERUQgPSAibG9hZGVkIgpTVEFUVVNfT0JTRVJWRUQgPSAib2JzZXJ2ZWQiClNUQVRVU19SRVZJRVdFRCA9ICJyZXZpZXdlZCIKU1RBVFVTX0NMT1NFRCA9ICJjbG9zZWQiCgpTVEFUVVNfTEFCRUxTID0gewogICAgU1RBVFVTX1BFTkRJTkc6ICJQZW5kaWVudGUiLAogICAgU1RBVFVTX0xPQURFRDogIkNhcmdhZG8iLAogICAgU1RBVFVTX09CU0VSVkVEOiAiQ29uIG9ic2VydmFjaW9uZXMiLAogICAgU1RBVFVTX1JFVklFV0VEOiAiUmV2aXNhZG8iLAogICAgU1RBVFVTX0NMT1NFRDogIkNlcnJhZG8iLAp9CgpQRVJJT0RfSU5DT01QTEVURSA9ICJpbmNvbXBsZXRlIgpQRVJJT0RfSU5fUkVWSUVXID0gImluX3JldmlldyIKUEVSSU9EX1JFQURZID0gInJlYWR5IgpQRVJJT0RfQ0xPU0VEID0gImNsb3NlZCIKClBFUklPRF9TVEFUVVNfTEFCRUxTID0gewogICAgUEVSSU9EX0lOQ09NUExFVEU6ICJJbmNvbXBsZXRvIiwKICAgIFBFUklPRF9JTl9SRVZJRVc6ICJFbiByZXZpc2nDs24iLAogICAgUEVSSU9EX1JFQURZOiAiTGlzdG8iLAogICAgUEVSSU9EX0NMT1NFRDogIkNlcnJhZG8iLAp9CgpJTkdSRVNPU19VTkVTID0gKCJGQUNUT1JJTkciLCAiRkFDVE9SQUpFIiwgIkxFQVNJTkciLCAiSU5TVVJBTkNFIikKTUVUUklDX0NPREVTID0gKAogICAgTWV0cmljRGVmaW5pdGlvbi5DT0RFX0lOR1JFU09TLAogICAgTWV0cmljRGVmaW5pdGlvbi5DT0RFX0NMSUVOVEVTX05VRVZPUywKICAgIE1ldHJpY0RlZmluaXRpb24uQ09ERV9WRU5UQV9DUlVaQURBLAogICAgTWV0cmljRGVmaW5pdGlvbi5DT0RFX1JFU1BVRVNUQV9SRVFTLAopCgoKZGVmIF9wZXJpb2RfbGFiZWwoeWVhcjogaW50LCBtb250aDogaW50KSAtPiBzdHI6CiAgICByZXR1cm4gZiJ7eWVhcn0te21vbnRoOjAyZH0iCgoKZGVmIF9zdGF0dXNfYmFkZ2Uoc3RhdHVzOiBzdHIpIC0+IHN0cjoKICAgIHJldHVybiBTVEFUVVNfTEFCRUxTLmdldChzdGF0dXMsIHN0YXR1cykKCgpkZWYgX2dldF9wbGFuKHllYXI6IGludCkgLT4gUEdDUGxhbiB8IE5vbmU6CiAgICByZXR1cm4gUEdDUGxhbi5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIpLmZpcnN0KCkKCgpkZWYgX2xhdGVzdF91cGxvYWRfZm9yX3BlcmlvZCh5ZWFyOiBpbnQsIG1vbnRoOiBpbnQsIGZpbGVfdHlwZTogc3RyKSAtPiBGaWxlVXBsb2FkIHwgTm9uZToKICAgIHJldHVybiAoCiAgICAgICAgRmlsZVVwbG9hZC5vYmplY3RzLmZpbHRlcigKICAgICAgICAgICAgZGV0ZWN0ZWRfeWVhcj15ZWFyLAogICAgICAgICAgICBkZXRlY3RlZF9tb250aD1tb250aCwKICAgICAgICAgICAgZmlsZV90eXBlX2RldGVjdGVkPWZpbGVfdHlwZSwKICAgICAgICApCiAgICAgICAgLnNlbGVjdF9yZWxhdGVkKCJ1cGxvYWRlZF9ieSIpCiAgICAgICAgLm9yZGVyX2J5KCItY3JlYXRlZF9hdCIpCiAgICAgICAgLmZpcnN0KCkKICAgICkKCgpkZWYgX3VwbG9hZF9hY3Rvcih1cGxvYWQ6IEZpbGVVcGxvYWQgfCBOb25lKSAtPiBzdHIgfCBOb25lOgogICAgaWYgdXBsb2FkIGFuZCB1cGxvYWQudXBsb2FkZWRfYnk6CiAgICAgICAgcmV0dXJuIHVwbG9hZC51cGxvYWRlZF9ieS51c2VybmFtZQogICAgcmV0dXJuIE5vbmUKCgpkZWYgX3VwbG9hZF90aW1lc3RhbXAodXBsb2FkOiBGaWxlVXBsb2FkIHwgTm9uZSkgLT4gZGF0ZXRpbWUgfCBOb25lOgogICAgaWYgdXBsb2FkOgogICAgICAgIHJldHVybiB1cGxvYWQudXBkYXRlZF9hdCBvciB1cGxvYWQuY3JlYXRlZF9hdAogICAgcmV0dXJuIE5vbmUKCgpkZWYgX2NvdW50X3BlbmRpbmdfYWxpYXNlcyh5ZWFyOiBpbnQsIG1vbnRoOiBpbnQpIC0+IGludDoKICAgIGtub3duID0ge2EucmF3X3ZhbHVlLnN0cmlwKCkudXBwZXIoKSBmb3IgYSBpbiBVTkVBbGlhcy5vYmplY3RzLmZpbHRlcihpc19hY3RpdmU9VHJ1ZSl9CiAgICBwZW5kaW5nID0gc2V0KCkKCiAgICBmb3IgcmF3IGluICgKICAgICAgICBOZXdDbGllbnRJbXBvcnRSb3cub2JqZWN0cy5maWx0ZXIoeWVhcj15ZWFyLCBtb250aD1tb250aCkKICAgICAgICAuZXhjbHVkZShyYXdfdW5lX3ZhbHVlPSIiKQogICAgICAgIC52YWx1ZXNfbGlzdCgicmF3X3VuZV92YWx1ZSIsIGZsYXQ9VHJ1ZSkKICAgICk6CiAgICAgICAga2V5ID0gKHJhdyBvciAiIikuc3RyaXAoKS51cHBlcigpCiAgICAgICAgaWYga2V5IGFuZCBrZXkgbm90IGluIGtub3duOgogICAgICAgICAgICBwZW5kaW5nLmFkZChrZXkpCgogICAgZm9yIHJhd19kZXN0LCByYXdfb3JpZyBpbiBDcm9zc1NhbGVJbXBvcnRSb3cub2JqZWN0cy5maWx0ZXIoCiAgICAgICAgeWVhcj15ZWFyLCBtb250aD1tb250aAogICAgKS52YWx1ZXNfbGlzdCgicmF3X3VuZV9kZXN0aW5hdGlvbiIsICJyYXdfdW5lX29yaWdpbiIpOgogICAgICAgIGZvciByYXcgaW4gKHJhd19kZXN0LCByYXdfb3JpZyk6CiAgICAgICAgICAgIGtleSA9IChyYXcgb3IgIiIpLnN0cmlwKCkudXBwZXIoKQogICAgICAgICAgICBpZiBrZXkgYW5kIGtleSBub3QgaW4ga25vd246CiAgICAgICAgICAgICAgICBwZW5kaW5nLmFkZChrZXkpCgogICAgdW5yZXNvbHZlZF9jcm9zcyA9IENyb3NzU2FsZUltcG9ydFJvdy5vYmplY3RzLmZpbHRlcigKICAgICAgICB5ZWFyPXllYXIsIG1vbnRoPW1vbnRoCiAgICApLmZpbHRlcihRKHVuZV9kZXN0aW5hdGlvbl9faXNudWxsPVRydWUpIHwgUSh1bmVfb3JpZ2luX19pc251bGw9VHJ1ZSkpLmNvdW50KCkKCiAgICByZXR1cm4gbGVuKHBlbmRpbmcpICsgdW5yZXNvbHZlZF9jcm9zcwoKCmRlZiBfYmxvY2tfdGFyZ2V0cyhwbGFuOiBQR0NQbGFuIHwgTm9uZSwgeWVhcjogaW50LCBtb250aDogaW50KSAtPiBkaWN0W3N0ciwgQW55XToKICAgIGlmIG5vdCBwbGFuOgogICAgICAgIHJldHVybiBfZW1wdHlfYmxvY2soQkxPQ0tfVEFSR0VUUywgIk5vIGhheSBwbGFuIFBHQyBwYXJhIGVzdGUgYcOxby4iKQoKICAgIGNvdW50ID0gTW9udGhseVRhcmdldC5vYmplY3RzLmZpbHRlcihwbGFuPXBsYW4sIHllYXI9eWVhciwgbW9udGg9bW9udGgpLmNvdW50KCkKICAgIGFjdGl2ZV91bmVzID0gVU5FLm9iamVjdHMuZmlsdGVyKGlzX2FjdGl2ZT1UcnVlKS5jb3VudCgpCiAgICBleHBlY3RlZCA9IGFjdGl2ZV91bmVzICogbGVuKE1FVFJJQ19DT0RFUykKCiAgICBzdGF0dXMgPSBTVEFUVVNfTE9BREVEIGlmIGNvdW50ID49IGV4cGVjdGVkIGVsc2UgU1RBVFVTX1BFTkRJTkcKICAgIHN1bW1hcnkgPSBmIntjb3VudH0gbWV0YXMgcmVnaXN0cmFkYXMiCgogICAgcmV0dXJuIHsKICAgICAgICAqKl9ibG9ja19zaGVsbChCTE9DS19UQVJHRVRTKSwKICAgICAgICAic3RhdHVzIjogc3RhdHVzLAogICAgICAgICJzdGF0dXNfbGFiZWwiOiBfc3RhdHVzX2JhZGdlKHN0YXR1cyksCiAgICAgICAgInN1bW1hcnkiOiBzdW1tYXJ5LAogICAgICAgICJsYXN0X2FjdGlvbl9hdCI6IE5vbmUsCiAgICAgICAgImxhc3RfYWN0aW9uX2J5IjogTm9uZSwKICAgICAgICAiY2hlY2tsaXN0IjogWwogICAgICAgICAgICB7ImxhYmVsIjogIk1ldGFzIGRlbCBwbGFuIGNhcmdhZGFzIiwgImRvbmUiOiBjb3VudCA+IDB9LAogICAgICAgICAgICB7ImxhYmVsIjogIkNvYmVydHVyYSBjb21wbGV0YSBwb3IgVU5FIHkgbcOpdHJpY2EiLCAiZG9uZSI6IGNvdW50ID49IGV4cGVjdGVkfSwKICAgICAgICBdLAogICAgICAgICJzdGF0cyI6IHsidGFyZ2V0c19jb3VudCI6IGNvdW50LCAiZXhwZWN0ZWQiOiBleHBlY3RlZH0sCiAgICB9CgoKZGVmIF9ibG9ja19maW5hbmNpYWwocGxhbjogUEdDUGxhbiB8IE5vbmUsIHllYXI6IGludCwgbW9udGg6IGludCkgLT4gZGljdFtzdHIsIEFueV06CiAgICB1cGxvYWQgPSBfbGF0ZXN0X3VwbG9hZF9mb3JfcGVyaW9kKHllYXIsIG1vbnRoLCBGaWxlVXBsb2FkLlRZUEVfRklOQU5DSUFMKQogICAgaGVhZGVycyA9IEZpbmFuY2lhbFN0YXRlbWVudEltcG9ydEhlYWRlci5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKQogICAgaGVhZGVyX2NvdW50ID0gaGVhZGVycy5jb3VudCgpCgogICAgaW5ncmVzb3NfbWV0cmljID0gTWV0cmljRGVmaW5pdGlvbi5vYmplY3RzLmZpbHRlcihjb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9JTkdSRVNPUykuZmlyc3QoKQogICAgcmVzdWx0c19jb3VudCA9IDAKICAgIGlmIHBsYW4gYW5kIGluZ3Jlc29zX21ldHJpYzoKICAgICAgICByZXN1bHRzX2NvdW50ID0gTW9udGhseU1ldHJpY1Jlc3VsdC5vYmplY3RzLmZpbHRlcigKICAgICAgICAgICAgcGxhbj1wbGFuLAogICAgICAgICAgICBtZXRyaWM9aW5ncmVzb3NfbWV0cmljLAogICAgICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICB1bmVfX2NvZGVfX2luPUlOR1JFU09TX1VORVMsCiAgICAgICAgICAgIG1lYXN1cmVkX3ZhbHVlX19pc251bGw9RmFsc2UsCiAgICAgICAgKS5jb3VudCgpCgogICAgaGFzX2Z4ID0gTW9udGhseUV4Y2hhbmdlUmF0ZS5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKS5leGlzdHMoKQogICAgaGFzX2Vycm9yID0gdXBsb2FkIGFuZCB1cGxvYWQuc3RhdHVzID09IEZpbGVVcGxvYWQuU1RBVFVTX1BBUlNFRF9FUlJPUgoKICAgIGlmIGhhc19lcnJvcjoKICAgICAgICBzdGF0dXMgPSBTVEFUVVNfT0JTRVJWRUQKICAgIGVsaWYgcmVzdWx0c19jb3VudCA+PSAzOgogICAgICAgIHN0YXR1cyA9IFNUQVRVU19MT0FERUQKICAgIGVsaWYgdXBsb2FkIG9yIGhlYWRlcl9jb3VudDoKICAgICAgICBzdGF0dXMgPSBTVEFUVVNfT0JTRVJWRUQKICAgIGVsc2U6CiAgICAgICAgc3RhdHVzID0gU1RBVFVTX1BFTkRJTkcKCiAgICBzdW1tYXJ5X3BhcnRzID0gW10KICAgIGlmIHVwbG9hZDoKICAgICAgICBzdW1tYXJ5X3BhcnRzLmFwcGVuZCh1cGxvYWQub3JpZ2luYWxfZmlsZW5hbWUpCiAgICBzdW1tYXJ5X3BhcnRzLmFwcGVuZChmIntyZXN1bHRzX2NvdW50fS8zIFVORXMgY29uIGluZ3Jlc28iKQogICAgaWYgbm90IGhhc19meDoKICAgICAgICBzdW1tYXJ5X3BhcnRzLmFwcGVuZCgiZmFsdGEgdGlwbyBkZSBjYW1iaW8iKQoKICAgIHJldHVybiB7CiAgICAgICAgKipfYmxvY2tfc2hlbGwoQkxPQ0tfRklOQU5DSUFMKSwKICAgICAgICAic3RhdHVzIjogc3RhdHVzLAogICAgICAgICJzdGF0dXNfbGFiZWwiOiBfc3RhdHVzX2JhZGdlKHN0YXR1cyksCiAgICAgICAgInN1bW1hcnkiOiAiIMK3ICIuam9pbihzdW1tYXJ5X3BhcnRzKSwKICAgICAgICAibGFzdF9hY3Rpb25fYXQiOiBfdXBsb2FkX3RpbWVzdGFtcCh1cGxvYWQpLAogICAgICAgICJsYXN0X2FjdGlvbl9ieSI6IF91cGxvYWRfYWN0b3IodXBsb2FkKSwKICAgICAgICAiY2hlY2tsaXN0IjogWwogICAgICAgICAgICB7ImxhYmVsIjogIlRpcG8gZGUgY2FtYmlvIGRlbCBtZXMiLCAiZG9uZSI6IGhhc19meH0sCiAgICAgICAgICAgIHsibGFiZWwiOiAiQXJjaGl2byhzKSBXQyogc3ViaWRvKHMpIiwgImRvbmUiOiBib29sKHVwbG9hZCl9LAogICAgICAgICAgICB7ImxhYmVsIjogIkluZ3Jlc29zIGltcG9ydGFkb3MgKEZhY3RvcmluZywgTGVhc2luZywgSW5zdXJhbmNlKSIsICJkb25lIjogcmVzdWx0c19jb3VudCA+PSAzfSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJTaW4gZXJyb3JlcyBkZSBsZWN0dXJhIiwgImRvbmUiOiBub3QgaGFzX2Vycm9yfSwKICAgICAgICBdLAogICAgICAgICJzdGF0cyI6IHsKICAgICAgICAgICAgInVwbG9hZF9pZCI6IHVwbG9hZC5pZCBpZiB1cGxvYWQgZWxzZSBOb25lLAogICAgICAgICAgICAicmVzdWx0c19jb3VudCI6IHJlc3VsdHNfY291bnQsCiAgICAgICAgICAgICJoYXNfZngiOiBoYXNfZngsCiAgICAgICAgfSwKICAgICAgICAidXBsb2FkcyI6IF9wZXJpb2RfdXBsb2Fkcyh5ZWFyLCBtb250aCwgRmlsZVVwbG9hZC5UWVBFX0ZJTkFOQ0lBTCksCiAgICB9CgoKZGVmIF9uZXdfY2xpZW50X3Jvd19kZWR1cF9rZXkocm93OiBOZXdDbGllbnRJbXBvcnRSb3cpIC0+IHR1cGxlOgogICAgIyBjb3VudHNfYXNfbmV3IGlzIGRlcml2ZWQ7IGlnbm9yZSBpdCBzbyBTw60vTm8gdHdpbnMgY291bnQgYXMgZHVwbGljYXRlcy4KICAgIHJldHVybiAoCiAgICAgICAgcm93LnVuZV9pZCwKICAgICAgICAocm93LmNsaWVudF9uYW1lIG9yICIiKS5zdHJpcCgpLmNhc2Vmb2xkKCksCiAgICAgICAgKHJvdy5uaXQgb3IgIiIpLnN0cmlwKCksCiAgICAgICAgKHJvdy5vcGVyYXRpb25fY29kZSBvciAiIikuc3RyaXAoKSwKICAgICAgICByb3cucHJldmlvdXNfY29udHJhY3RzLAogICAgICAgIHJvdy5jdXJyZW5jeV9pZCwKICAgICAgICBzdHIocm93LmFtb3VudCkgaWYgcm93LmFtb3VudCBpcyBub3QgTm9uZSBlbHNlICIiLAogICAgKQoKCmRlZiBjb3VudF9kdXBsaWNhdGVfbmV3X2NsaWVudF9yb3dzKHllYXI6IGludCwgbW9udGg6IGludCkgLT4gaW50OgogICAgIiIiQ3VlbnRhIGZpbGFzIGR1cGxpY2FkYXMgZW4gZWwgZGV0YWxsZSBkZSBjbGllbnRlcyBudWV2b3MgZGVsIHBlcsOtb2RvLiIiIgogICAgc2Vlbjogc2V0W3R1cGxlXSA9IHNldCgpCiAgICBkdXBsaWNhdGVfaWRzOiBsaXN0W2ludF0gPSBbXQogICAgZm9yIHJvdyBpbiBOZXdDbGllbnRJbXBvcnRSb3cub2JqZWN0cy5maWx0ZXIoeWVhcj15ZWFyLCBtb250aD1tb250aCkub3JkZXJfYnkoImlkIik6CiAgICAgICAga2V5ID0gX25ld19jbGllbnRfcm93X2RlZHVwX2tleShyb3cpCiAgICAgICAgaWYga2V5IGluIHNlZW46CiAgICAgICAgICAgIGR1cGxpY2F0ZV9pZHMuYXBwZW5kKHJvdy5pZCkKICAgICAgICBlbHNlOgogICAgICAgICAgICBzZWVuLmFkZChrZXkpCiAgICByZXR1cm4gbGVuKGR1cGxpY2F0ZV9pZHMpCgoKZGVmIF9zeW5jX2NsaWVudGVzX251ZXZvc19tZXRyaWNzX2Zyb21fcm93cyh5ZWFyOiBpbnQsIG1vbnRoOiBpbnQpIC0+IGludDoKICAgICIiIkFjdHVhbGl6YSBDTElFTlRFU19OVUVWT1MgZGVzZGUgbGFzIGZpbGFzIHZpZ2VudGVzIGRlbCBwZXLDrW9kby4iIiIKICAgIHBsYW4gPSBfZ2V0X3BsYW4oeWVhcikKICAgIGlmIG5vdCBwbGFuOgogICAgICAgIHJldHVybiAwCgogICAgbWV0cmljID0gTWV0cmljRGVmaW5pdGlvbi5vYmplY3RzLmdldChjb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9DTElFTlRFU19OVUVWT1MpCiAgICBjb3VudHMgPSB7CiAgICAgICAgcm93WyJ1bmVfaWQiXTogcm93WyJjbnQiXQogICAgICAgIGZvciByb3cgaW4gTmV3Q2xpZW50SW1wb3J0Um93Lm9iamVjdHMuZmlsdGVyKHllYXI9eWVhciwgbW9udGg9bW9udGgsIGNvdW50c19hc19uZXc9VHJ1ZSkKICAgICAgICAudmFsdWVzKCJ1bmVfaWQiKQogICAgICAgIC5hbm5vdGF0ZShjbnQ9Q291bnQoImlkIikpCiAgICB9CgogICAgdXBkYXRlZCA9IDAKICAgIGZvciB1bmUgaW4gVU5FLm9iamVjdHMuZmlsdGVyKGlzX2FjdGl2ZT1UcnVlKToKICAgICAgICBjb3VudCA9IGNvdW50cy5nZXQodW5lLmlkLCAwKQogICAgICAgIHRyeToKICAgICAgICAgICAgdGFyZ2V0ID0gTW9udGhseVRhcmdldC5vYmplY3RzLmdldCgKICAgICAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgICAgIHVuZT11bmUsCiAgICAgICAgICAgICAgICBtZXRyaWM9bWV0cmljLAogICAgICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgICkKICAgICAgICBleGNlcHQgTW9udGhseVRhcmdldC5Eb2VzTm90RXhpc3Q6CiAgICAgICAgICAgIGNvbnRpbnVlCgogICAgICAgIG1tciwgXyA9IE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5nZXRfb3JfY3JlYXRlKAogICAgICAgICAgICBwbGFuPXBsYW4sCiAgICAgICAgICAgIHVuZT11bmUsCiAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgIGRlZmF1bHRzPXsidGFyZ2V0X3ZhbHVlIjogdGFyZ2V0LnRhcmdldF92YWx1ZX0sCiAgICAgICAgKQogICAgICAgIG1tci50YXJnZXRfdmFsdWUgPSB0YXJnZXQudGFyZ2V0X3ZhbHVlCiAgICAgICAgbW1yLm1lYXN1cmVkX3ZhbHVlID0gRGVjaW1hbChzdHIoY291bnQpKQogICAgICAgIG1tci5jYWxjdWxhdGlvbl9ub3RlID0gZiJ7Y291bnR9IGNsaWVudGVzIG51ZXZvcyBjb250YWRvcyBkZXNkZSBmaWxhcyBkZWwgcGVyw61vZG8iCiAgICAgICAgbW1yLnNhdmUoKQogICAgICAgIHVwZGF0ZWQgKz0gMQogICAgcmV0dXJuIHVwZGF0ZWQKCgpAdHJhbnNhY3Rpb24uYXRvbWljCmRlZiByZW1vdmVfZHVwbGljYXRlX25ld19jbGllbnRfcm93cyh5ZWFyOiBpbnQsIG1vbnRoOiBpbnQsIHVzZXI9Tm9uZSkgLT4gZGljdFtzdHIsIGludF06CiAgICAiIiIKICAgIEVsaW1pbmEgZmlsYXMgZHVwbGljYWRhcyBkZWwgZGV0YWxsZSBkZSBjbGllbnRlcyBudWV2b3MgKGNvbnNlcnZhIGxhIG3DoXMgYW50aWd1YSkuCiAgICBPcGNpb25hbG1lbnRlIHNpbmNyb25pemEgbGEgbcOpdHJpY2EgQ0xJRU5URVNfTlVFVk9TLgogICAgIiIiCiAgICBzZWVuOiBzZXRbdHVwbGVdID0gc2V0KCkKICAgIGR1cGxpY2F0ZV9pZHM6IGxpc3RbaW50XSA9IFtdCiAgICBmb3Igcm93IGluIE5ld0NsaWVudEltcG9ydFJvdy5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKS5vcmRlcl9ieSgiaWQiKToKICAgICAgICBrZXkgPSBfbmV3X2NsaWVudF9yb3dfZGVkdXBfa2V5KHJvdykKICAgICAgICBpZiBrZXkgaW4gc2VlbjoKICAgICAgICAgICAgZHVwbGljYXRlX2lkcy5hcHBlbmQocm93LmlkKQogICAgICAgIGVsc2U6CiAgICAgICAgICAgIHNlZW4uYWRkKGtleSkKCiAgICByZW1vdmVkID0gTmV3Q2xpZW50SW1wb3J0Um93Lm9iamVjdHMuZmlsdGVyKGlkX19pbj1kdXBsaWNhdGVfaWRzKS5kZWxldGUoKVswXQogICAgbWV0cmljc191cGRhdGVkID0gMAogICAgaWYgcmVtb3ZlZDoKICAgICAgICBtZXRyaWNzX3VwZGF0ZWQgPSBfc3luY19jbGllbnRlc19udWV2b3NfbWV0cmljc19mcm9tX3Jvd3MoeWVhciwgbW9udGgpCiAgICAgICAgaWYgdXNlcjoKICAgICAgICAgICAgbG9nX21hbnVhbF9lZGl0KAogICAgICAgICAgICAgICAgdXNlcj11c2VyLAogICAgICAgICAgICAgICAgeWVhcj15ZWFyLAogICAgICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgICAgICBlbnRpdHlfdHlwZT1BZG1pbk1hbnVhbEVkaXRMb2cuRU5USVRZX05FV19DTElFTlRfUk9XLAogICAgICAgICAgICAgICAgZW50aXR5X2lkPTAsCiAgICAgICAgICAgICAgICBmaWVsZF9uYW1lPSJkZWR1cCIsCiAgICAgICAgICAgICAgICBvbGRfdmFsdWU9ZiJ7cmVtb3ZlZH0gZHVwbGljYWRvcyIsCiAgICAgICAgICAgICAgICBuZXdfdmFsdWU9ImVsaW1pbmFkb3MiLAogICAgICAgICAgICAgICAgcmVhc29uPSJEZXB1cmFjacOzbiBkZSBkdXBsaWNhZG9zIGVuIGRldGFsbGUgZGUgY2xpZW50ZXMgbnVldm9zIiwKICAgICAgICAgICAgKQogICAgcmV0dXJuIHsicmVtb3ZlZCI6IHJlbW92ZWQsICJtZXRyaWNzX3VwZGF0ZWQiOiBtZXRyaWNzX3VwZGF0ZWR9CgoKZGVmIF9yZXBvaW50X2ltcG9ydF9oZWFkZXJfYXdheV9mcm9tX3VwbG9hZCh1cGxvYWQ6IEZpbGVVcGxvYWQpIC0+IE5vbmU6CiAgICAiIiIKICAgIEFudGVzIGRlIGJvcnJhciB1biBGaWxlVXBsb2FkIHBlbmRpZW50ZTogc2kgdW4gZW5jYWJlemFkbyBsbyBhcHVudGEsCiAgICByZWFzaWduYSBhIG90cm8gYXJjaGl2byBkZWwgcGVyw61vZG8gbyBlbGltaW5hIGVsIGVuY2FiZXphZG8gdmFjw61vLgogICAgTnVuY2EgZGVqYSBjYXNjYWRhIHNvYnJlIGZpbGFzIHlhIGltcG9ydGFkYXMuCiAgICAiIiIKICAgIHNwZWNzOiBsaXN0W3R1cGxlW3R5cGUsIHN0ciwgdHlwZSB8IE5vbmVdXSA9IFsKICAgICAgICAoTmV3Q2xpZW50SW1wb3J0SGVhZGVyLCBGaWxlVXBsb2FkLlRZUEVfTkVXX0NMSUVOVFMsIE5ld0NsaWVudEltcG9ydFJvdyksCiAgICAgICAgKENyb3NzU2FsZUltcG9ydEhlYWRlciwgRmlsZVVwbG9hZC5UWVBFX0NST1NTX1NBTEUsIENyb3NzU2FsZUltcG9ydFJvdyksCiAgICAgICAgKFN0YXRpb25UaW1lSW1wb3J0SGVhZGVyLCBGaWxlVXBsb2FkLlRZUEVfU1RBVElPTl9USU1FUywgTm9uZSksCiAgICAgICAgKEZpbmFuY2lhbFN0YXRlbWVudEltcG9ydEhlYWRlciwgRmlsZVVwbG9hZC5UWVBFX0ZJTkFOQ0lBTCwgTm9uZSksCiAgICBdCiAgICBmb3IgaGVhZGVyX21vZGVsLCBmaWxlX3R5cGUsIHJvd19tb2RlbCBpbiBzcGVjczoKICAgICAgICBoZWFkZXJzID0gbGlzdChoZWFkZXJfbW9kZWwub2JqZWN0cy5maWx0ZXIoZmlsZV91cGxvYWQ9dXBsb2FkKSkKICAgICAgICBmb3IgaGVhZGVyIGluIGhlYWRlcnM6CiAgICAgICAgICAgIHllYXIgPSBnZXRhdHRyKGhlYWRlciwgInllYXIiLCB1cGxvYWQuZGV0ZWN0ZWRfeWVhcikKICAgICAgICAgICAgbW9udGggPSBnZXRhdHRyKGhlYWRlciwgIm1vbnRoIiwgdXBsb2FkLmRldGVjdGVkX21vbnRoKQogICAgICAgICAgICBhbHRfcXMgPSBGaWxlVXBsb2FkLm9iamVjdHMuZmlsdGVyKAogICAgICAgICAgICAgICAgZmlsZV90eXBlX2RldGVjdGVkPWZpbGVfdHlwZSwKICAgICAgICAgICAgKS5leGNsdWRlKHBrPXVwbG9hZC5waykKICAgICAgICAgICAgaWYgeWVhciBpcyBub3QgTm9uZToKICAgICAgICAgICAgICAgIGFsdF9xcyA9IGFsdF9xcy5maWx0ZXIoZGV0ZWN0ZWRfeWVhcj15ZWFyKQogICAgICAgICAgICBpZiBtb250aCBpcyBub3QgTm9uZToKICAgICAgICAgICAgICAgIGFsdF9xcyA9IGFsdF9xcy5maWx0ZXIoZGV0ZWN0ZWRfbW9udGg9bW9udGgpCiAgICAgICAgICAgIGFsdCA9ICgKICAgICAgICAgICAgICAgIGFsdF9xcy5maWx0ZXIoc3RhdHVzPUZpbGVVcGxvYWQuU1RBVFVTX1BBUlNFRF9PSykKICAgICAgICAgICAgICAgIC5vcmRlcl9ieSgiLWNyZWF0ZWRfYXQiKQogICAgICAgICAgICAgICAgLmZpcnN0KCkKICAgICAgICAgICAgICAgIG9yIGFsdF9xcy5vcmRlcl9ieSgiLWNyZWF0ZWRfYXQiKS5maXJzdCgpCiAgICAgICAgICAgICkKCiAgICAgICAgICAgIGhhc19yb3dzID0gRmFsc2UKICAgICAgICAgICAgaWYgcm93X21vZGVsIGlzIG5vdCBOb25lOgogICAgICAgICAgICAgICAgaGFzX3Jvd3MgPSByb3dfbW9kZWwub2JqZWN0cy5maWx0ZXIoaGVhZGVyPWhlYWRlcikuZXhpc3RzKCkKCiAgICAgICAgICAgIGlmIGFsdCBpcyBub3QgTm9uZToKICAgICAgICAgICAgICAgIGhlYWRlci5maWxlX3VwbG9hZCA9IGFsdAogICAgICAgICAgICAgICAgaGVhZGVyLnNhdmUodXBkYXRlX2ZpZWxkcz1bImZpbGVfdXBsb2FkIl0pCiAgICAgICAgICAgIGVsaWYgaGFzX3Jvd3M6CiAgICAgICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKAogICAgICAgICAgICAgICAgICAgICJObyBzZSBwdWVkZSBxdWl0YXIgZGUgbGEgY29sYTogZWwgcGVyw61vZG8geWEgdGllbmUgZGF0b3MgaW1wb3J0YWRvcyAiCiAgICAgICAgICAgICAgICAgICAgInkgbm8gaGF5IG90cm8gYXJjaGl2byBwcm9jZXNhZG8gYWwgY3VhbCBjb25zZXJ2YXIgZWwgdsOtbmN1bG8uIgogICAgICAgICAgICAgICAgKQogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgaGVhZGVyLmRlbGV0ZSgpCgoKQHRyYW5zYWN0aW9uLmF0b21pYwpkZWYgZGlzY2FyZF9wZW5kaW5nX3VwbG9hZCh1cGxvYWQ6IEZpbGVVcGxvYWQpIC0+IGRpY3Rbc3RyLCBBbnldOgogICAgIiIiCiAgICBFbGltaW5hIGRlIGxhIGNvbGEgdW4gYXJjaGl2byBwZW5kaWVudGUgZGUgcHJvY2VzYXIuCiAgICBTb2xvIFVQTE9BREVEIC8gUEFSU0VEX0VSUk9SLiBObyB0b2NhIFBBUlNFRF9PSyBuaSBmaWxhcyB5YSBjYXJnYWRhcy4KICAgICIiIgogICAgaWYgdXBsb2FkLnN0YXR1cyA9PSBGaWxlVXBsb2FkLlNUQVRVU19QQVJTRURfT0s6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcigKICAgICAgICAgICAgIkVzdGUgYXJjaGl2byB5YSBmdWUgcHJvY2VzYWRvOyBubyBzZSBwdWVkZSBxdWl0YXIgZGUgbGEgY29sYS4iCiAgICAgICAgKQoKICAgIGZpbGVuYW1lID0gdXBsb2FkLm9yaWdpbmFsX2ZpbGVuYW1lCiAgICBfcmVwb2ludF9pbXBvcnRfaGVhZGVyX2F3YXlfZnJvbV91cGxvYWQodXBsb2FkKQoKICAgIGlmIHVwbG9hZC5zdG9yZWRfZmlsZToKICAgICAgICB0cnk6CiAgICAgICAgICAgIHVwbG9hZC5zdG9yZWRfZmlsZS5kZWxldGUoc2F2ZT1GYWxzZSkKICAgICAgICBleGNlcHQgRXhjZXB0aW9uOgogICAgICAgICAgICBwYXNzCiAgICB1cGxvYWQuZGVsZXRlKCkKICAgIHJldHVybiB7ImZpbGVuYW1lIjogZmlsZW5hbWUsICJvayI6IFRydWV9CgoKZGVmIF9ibG9ja19uZXdfY2xpZW50cyhwbGFuOiBQR0NQbGFuIHwgTm9uZSwgeWVhcjogaW50LCBtb250aDogaW50KSAtPiBkaWN0W3N0ciwgQW55XToKICAgIHVwbG9hZCA9IF9sYXRlc3RfdXBsb2FkX2Zvcl9wZXJpb2QoeWVhciwgbW9udGgsIEZpbGVVcGxvYWQuVFlQRV9ORVdfQ0xJRU5UUykKICAgIGhlYWRlciA9IE5ld0NsaWVudEltcG9ydEhlYWRlci5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKS5maXJzdCgpCiAgICByb3dzX3FzID0gTmV3Q2xpZW50SW1wb3J0Um93Lm9iamVjdHMuZmlsdGVyKHllYXI9eWVhciwgbW9udGg9bW9udGgpCiAgICB2YWxpZF9yb3dzID0gcm93c19xcy5maWx0ZXIoY291bnRzX2FzX25ldz1UcnVlKS5jb3VudCgpCiAgICBvYnNfcm93cyA9IHJvd3NfcXMuZXhjbHVkZShvYnNlcnZhdGlvbnM9IiIpLmNvdW50KCkKICAgIGR1cGxpY2F0ZV9yb3dzID0gY291bnRfZHVwbGljYXRlX25ld19jbGllbnRfcm93cyh5ZWFyLCBtb250aCkKICAgIGhhc19lcnJvciA9IHVwbG9hZCBhbmQgdXBsb2FkLnN0YXR1cyA9PSBGaWxlVXBsb2FkLlNUQVRVU19QQVJTRURfRVJST1IKCiAgICBpZiBoYXNfZXJyb3Igb3Igb2JzX3Jvd3M6CiAgICAgICAgc3RhdHVzID0gU1RBVFVTX09CU0VSVkVECiAgICBlbGlmIGhlYWRlciBhbmQgdmFsaWRfcm93cyA+IDA6CiAgICAgICAgc3RhdHVzID0gU1RBVFVTX0xPQURFRAogICAgZWxpZiB1cGxvYWQ6CiAgICAgICAgc3RhdHVzID0gU1RBVFVTX09CU0VSVkVECiAgICBlbHNlOgogICAgICAgIHN0YXR1cyA9IFNUQVRVU19QRU5ESU5HCgogICAgcmV0dXJuIHsKICAgICAgICAqKl9ibG9ja19zaGVsbChCTE9DS19ORVdfQ0xJRU5UUyksCiAgICAgICAgInN0YXR1cyI6IHN0YXR1cywKICAgICAgICAic3RhdHVzX2xhYmVsIjogX3N0YXR1c19iYWRnZShzdGF0dXMpLAogICAgICAgICJzdW1tYXJ5IjogZiJ7dmFsaWRfcm93c30gY2xpZW50ZXMgdsOhbGlkb3MiIGlmIHZhbGlkX3Jvd3MgZWxzZSAiU2luIGRhdG9zIHByb2Nlc2Fkb3MiLAogICAgICAgICJsYXN0X2FjdGlvbl9hdCI6IF91cGxvYWRfdGltZXN0YW1wKHVwbG9hZCkgb3IgKGhlYWRlci51cGRhdGVkX2F0IGlmIGhlYWRlciBlbHNlIE5vbmUpLAogICAgICAgICJsYXN0X2FjdGlvbl9ieSI6IF91cGxvYWRfYWN0b3IodXBsb2FkKSwKICAgICAgICAiY2hlY2tsaXN0IjogWwogICAgICAgICAgICB7ImxhYmVsIjogIkFyY2hpdm8gc3ViaWRvIiwgImRvbmUiOiBib29sKHVwbG9hZCl9LAogICAgICAgICAgICB7ImxhYmVsIjogIkVzdHJ1Y3R1cmEgdmFsaWRhZGEiLCAiZG9uZSI6IGJvb2woaGVhZGVyKX0sCiAgICAgICAgICAgIHsibGFiZWwiOiAiRmlsYXMgaW1wb3J0YWRhcyIsICJkb25lIjogdmFsaWRfcm93cyA+IDB9LAogICAgICAgICAgICB7ImxhYmVsIjogIlNpbiBvYnNlcnZhY2lvbmVzIHBlbmRpZW50ZXMiLCAiZG9uZSI6IG9ic19yb3dzID09IDB9LAogICAgICAgIF0sCiAgICAgICAgInN0YXRzIjogewogICAgICAgICAgICAidmFsaWRfcm93cyI6IHZhbGlkX3Jvd3MsCiAgICAgICAgICAgICJvYnNfcm93cyI6IG9ic19yb3dzLAogICAgICAgICAgICAiZHVwbGljYXRlX3Jvd3MiOiBkdXBsaWNhdGVfcm93cywKICAgICAgICAgICAgInVwbG9hZF9pZCI6IHVwbG9hZC5pZCBpZiB1cGxvYWQgZWxzZSBOb25lLAogICAgICAgIH0sCiAgICAgICAgInVwbG9hZHMiOiBfcGVyaW9kX3VwbG9hZHMoeWVhciwgbW9udGgsIEZpbGVVcGxvYWQuVFlQRV9ORVdfQ0xJRU5UUyksCiAgICB9CgoKZGVmIF9ibG9ja19jcm9zc19zYWxlKHBsYW46IFBHQ1BsYW4gfCBOb25lLCB5ZWFyOiBpbnQsIG1vbnRoOiBpbnQpIC0+IGRpY3Rbc3RyLCBBbnldOgogICAgdXBsb2FkID0gX2xhdGVzdF91cGxvYWRfZm9yX3BlcmlvZCh5ZWFyLCBtb250aCwgRmlsZVVwbG9hZC5UWVBFX0NST1NTX1NBTEUpCiAgICBoZWFkZXIgPSBDcm9zc1NhbGVJbXBvcnRIZWFkZXIub2JqZWN0cy5maWx0ZXIoeWVhcj15ZWFyLCBtb250aD1tb250aCkuZmlyc3QoKQogICAgcm93c19jb3VudCA9IENyb3NzU2FsZUltcG9ydFJvdy5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKS5jb3VudCgpCiAgICB1bnJlc29sdmVkID0gQ3Jvc3NTYWxlSW1wb3J0Um93Lm9iamVjdHMuZmlsdGVyKHllYXI9eWVhciwgbW9udGg9bW9udGgpLmZpbHRlcigKICAgICAgICBRKHVuZV9kZXN0aW5hdGlvbl9faXNudWxsPVRydWUpIHwgUSh1bmVfb3JpZ2luX19pc251bGw9VHJ1ZSkKICAgICkuY291bnQoKQogICAgaGFzX2Vycm9yID0gdXBsb2FkIGFuZCB1cGxvYWQuc3RhdHVzID09IEZpbGVVcGxvYWQuU1RBVFVTX1BBUlNFRF9FUlJPUgoKICAgIGlmIGhhc19lcnJvciBvciB1bnJlc29sdmVkOgogICAgICAgIHN0YXR1cyA9IFNUQVRVU19PQlNFUlZFRAogICAgZWxpZiBoZWFkZXIgYW5kIHJvd3NfY291bnQgPiAwOgogICAgICAgIHN0YXR1cyA9IFNUQVRVU19MT0FERUQKICAgIGVsaWYgdXBsb2FkOgogICAgICAgIHN0YXR1cyA9IFNUQVRVU19PQlNFUlZFRAogICAgZWxzZToKICAgICAgICBzdGF0dXMgPSBTVEFUVVNfUEVORElORwoKICAgIHJldHVybiB7CiAgICAgICAgKipfYmxvY2tfc2hlbGwoQkxPQ0tfQ1JPU1NfU0FMRSksCiAgICAgICAgInN0YXR1cyI6IHN0YXR1cywKICAgICAgICAic3RhdHVzX2xhYmVsIjogX3N0YXR1c19iYWRnZShzdGF0dXMpLAogICAgICAgICJzdW1tYXJ5IjogZiJ7cm93c19jb3VudH0gcmVmZXJlbmNpYXMiIGlmIHJvd3NfY291bnQgZWxzZSAiU2luIGRhdG9zIHByb2Nlc2Fkb3MiLAogICAgICAgICJsYXN0X2FjdGlvbl9hdCI6IF91cGxvYWRfdGltZXN0YW1wKHVwbG9hZCkgb3IgKGhlYWRlci51cGRhdGVkX2F0IGlmIGhlYWRlciBlbHNlIE5vbmUpLAogICAgICAgICJsYXN0X2FjdGlvbl9ieSI6IF91cGxvYWRfYWN0b3IodXBsb2FkKSwKICAgICAgICAiY2hlY2tsaXN0IjogWwogICAgICAgICAgICB7ImxhYmVsIjogIkFyY2hpdm8gc3ViaWRvIiwgImRvbmUiOiBib29sKHVwbG9hZCl9LAogICAgICAgICAgICB7ImxhYmVsIjogIkZpbGFzIGltcG9ydGFkYXMiLCAiZG9uZSI6IHJvd3NfY291bnQgPiAwfSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJVTkUgZGVzdGluby9vcmlnZW4gcmVzdWVsdG9zIiwgImRvbmUiOiB1bnJlc29sdmVkID09IDAgYW5kIHJvd3NfY291bnQgPiAwfSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJTaW4gZXJyb3JlcyBkZSBsZWN0dXJhIiwgImRvbmUiOiBub3QgaGFzX2Vycm9yfSwKICAgICAgICBdLAogICAgICAgICJzdGF0cyI6IHsicm93c19jb3VudCI6IHJvd3NfY291bnQsICJ1bnJlc29sdmVkIjogdW5yZXNvbHZlZCwgInVwbG9hZF9pZCI6IHVwbG9hZC5pZCBpZiB1cGxvYWQgZWxzZSBOb25lfSwKICAgICAgICAidXBsb2FkcyI6IF9wZXJpb2RfdXBsb2Fkcyh5ZWFyLCBtb250aCwgRmlsZVVwbG9hZC5UWVBFX0NST1NTX1NBTEUpLAogICAgfQoKCmRlZiBfYmxvY2tfbWFudWFsX3JlcXVpcmVtZW50cyhwbGFuOiBQR0NQbGFuIHwgTm9uZSwgeWVhcjogaW50LCBtb250aDogaW50KSAtPiBkaWN0W3N0ciwgQW55XToKICAgIGlmIG5vdCBwbGFuOgogICAgICAgIHJldHVybiBfZW1wdHlfYmxvY2soQkxPQ0tfTUFOVUFMX1JFUVVJUkVNRU5UUywgIk5vIGhheSBwbGFuIFBHQy4iKQoKICAgIHVuZXMgPSBsaXN0KFVORS5vYmplY3RzLmZpbHRlcihpc19hY3RpdmU9VHJ1ZSkpCiAgICByZWNvcmRzID0gewogICAgICAgIHIudW5lX2lkOiByCiAgICAgICAgZm9yIHIgaW4gTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZS5vYmplY3RzLmZpbHRlcihwbGFuPXBsYW4sIHllYXI9eWVhciwgbW9udGg9bW9udGgpCiAgICB9CiAgICBub25fY29tcGxpYW50ID0gW3IgZm9yIHIgaW4gcmVjb3Jkcy52YWx1ZXMoKSBpZiBub3Qgci5pc19jb21wbGlhbnRdCiAgICBmaWxsZWQgPSBsZW4ocmVjb3JkcykKCiAgICBpZiBub25fY29tcGxpYW50OgogICAgICAgIHN0YXR1cyA9IFNUQVRVU19PQlNFUlZFRAogICAgZWxpZiBmaWxsZWQgPj0gbGVuKHVuZXMpOgogICAgICAgIHN0YXR1cyA9IFNUQVRVU19MT0FERUQKICAgIGVsc2U6CiAgICAgICAgc3RhdHVzID0gU1RBVFVTX1BFTkRJTkcKCiAgICBsYXRlc3QgPSAoCiAgICAgICAgTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZS5vYmplY3RzLmZpbHRlcihwbGFuPXBsYW4sIHllYXI9eWVhciwgbW9udGg9bW9udGgpCiAgICAgICAgLm9yZGVyX2J5KCItdXBkYXRlZF9hdCIpCiAgICAgICAgLmZpcnN0KCkKICAgICkKCiAgICByZXR1cm4gewogICAgICAgICoqX2Jsb2NrX3NoZWxsKEJMT0NLX01BTlVBTF9SRVFVSVJFTUVOVFMpLAogICAgICAgICJzdGF0dXMiOiBzdGF0dXMsCiAgICAgICAgInN0YXR1c19sYWJlbCI6IF9zdGF0dXNfYmFkZ2Uoc3RhdHVzKSwKICAgICAgICAic3VtbWFyeSI6IGYie2ZpbGxlZH0ve2xlbih1bmVzKX0gVU5FcyByZWdpc3RyYWRhcyIsCiAgICAgICAgImxhc3RfYWN0aW9uX2F0IjogbGF0ZXN0LnVwZGF0ZWRfYXQgaWYgbGF0ZXN0IGVsc2UgTm9uZSwKICAgICAgICAibGFzdF9hY3Rpb25fYnkiOiBOb25lLAogICAgICAgICJjaGVja2xpc3QiOiBbCiAgICAgICAgICAgIHsibGFiZWwiOiAiUmVnaXN0cm8gcG9yIFVORSIsICJkb25lIjogZmlsbGVkID49IGxlbih1bmVzKX0sCiAgICAgICAgICAgIHsibGFiZWwiOiAiU2luIGluY2lkZW5jaWFzIHJlcG9ydGFkYXMiLCAiZG9uZSI6IG5vdCBub25fY29tcGxpYW50fSwKICAgICAgICBdLAogICAgICAgICJzdGF0cyI6IHsiZmlsbGVkIjogZmlsbGVkLCAidG90YWxfdW5lcyI6IGxlbih1bmVzKSwgIm5vbl9jb21wbGlhbnQiOiBsZW4obm9uX2NvbXBsaWFudCl9LAogICAgfQoKCmRlZiBfYmxvY2tfcmV2aWV3KHBsYW46IFBHQ1BsYW4gfCBOb25lLCB5ZWFyOiBpbnQsIG1vbnRoOiBpbnQpIC0+IGRpY3Rbc3RyLCBBbnldOgogICAgaWYgbm90IHBsYW46CiAgICAgICAgcmV0dXJuIF9lbXB0eV9ibG9jayhCTE9DS19SRVZJRVcsICJObyBoYXkgcGxhbiBQR0MuIikKCiAgICBzY29yZWNhcmRzID0gTW9udGhseU1vZGVTY29yZWNhcmQub2JqZWN0cy5maWx0ZXIocGxhbj1wbGFuLCB5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKQogICAgY291bnQgPSBzY29yZWNhcmRzLmNvdW50KCkKICAgIGxhdGVzdCA9IHNjb3JlY2FyZHMub3JkZXJfYnkoIi11cGRhdGVkX2F0IikuZmlyc3QoKQoKICAgIGlmIGNvdW50ID49IFVORS5vYmplY3RzLmZpbHRlcihpc19hY3RpdmU9VHJ1ZSkuY291bnQoKToKICAgICAgICBzdGF0dXMgPSBTVEFUVVNfUkVWSUVXRUQKICAgIGVsaWYgY291bnQgPiAwOgogICAgICAgIHN0YXR1cyA9IFNUQVRVU19MT0FERUQKICAgIGVsc2U6CiAgICAgICAgc3RhdHVzID0gU1RBVFVTX1BFTkRJTkcKCiAgICByZXR1cm4gewogICAgICAgICoqX2Jsb2NrX3NoZWxsKEJMT0NLX1JFVklFVyksCiAgICAgICAgInN0YXR1cyI6IHN0YXR1cywKICAgICAgICAic3RhdHVzX2xhYmVsIjogX3N0YXR1c19iYWRnZShzdGF0dXMpLAogICAgICAgICJzdW1tYXJ5IjogZiJTY29yZSBhY3R1YWxpemFkbyAoe2NvdW50fSBVTkVzKSIgaWYgY291bnQgZWxzZSAiU2luIHJlY8OhbGN1bG8iLAogICAgICAgICJsYXN0X2FjdGlvbl9hdCI6IGxhdGVzdC51cGRhdGVkX2F0IGlmIGxhdGVzdCBlbHNlIE5vbmUsCiAgICAgICAgImxhc3RfYWN0aW9uX2J5IjogTm9uZSwKICAgICAgICAiY2hlY2tsaXN0IjogWwogICAgICAgICAgICB7ImxhYmVsIjogIkluZ3Jlc29zIEludmVzdG1lbnQgcmVjYWxjdWxhZG9zIiwgImRvbmUiOiBfaW52ZXN0bWVudF9pbmdyZXNvc19yZWFkeShwbGFuLCB5ZWFyLCBtb250aCl9LAogICAgICAgICAgICB7ImxhYmVsIjogIlNjb3JlIFBHQyBnZW5lcmFkbyIsICJkb25lIjogY291bnQgPiAwfSwKICAgICAgICAgICAgeyJsYWJlbCI6ICJUb2RhcyBsYXMgVU5FcyBjb24gc2NvcmUiLCAiZG9uZSI6IGNvdW50ID49IFVORS5vYmplY3RzLmZpbHRlcihpc19hY3RpdmU9VHJ1ZSkuY291bnQoKX0sCiAgICAgICAgXSwKICAgICAgICAic3RhdHMiOiB7InNjb3JlY2FyZF9jb3VudCI6IGNvdW50fSwKICAgIH0KCgpkZWYgX2ludmVzdG1lbnRfaW5ncmVzb3NfcmVhZHkocGxhbjogUEdDUGxhbiwgeWVhcjogaW50LCBtb250aDogaW50KSAtPiBib29sOgogICAgbWV0cmljID0gTWV0cmljRGVmaW5pdGlvbi5vYmplY3RzLmZpbHRlcihjb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9JTkdSRVNPUykuZmlyc3QoKQogICAgdW5lID0gVU5FLm9iamVjdHMuZmlsdGVyKGNvZGVfX2luPVsiSU5WRVNUTUVOVCIsICJJTlZFU1RNRU5UUyIsICJJTlZFUlNJT05FUyJdKS5maXJzdCgpCiAgICBpZiBub3QgbWV0cmljIG9yIG5vdCB1bmU6CiAgICAgICAgcmV0dXJuIEZhbHNlCiAgICByZXR1cm4gTW9udGhseU1ldHJpY1Jlc3VsdC5vYmplY3RzLmZpbHRlcigKICAgICAgICBwbGFuPXBsYW4sIG1ldHJpYz1tZXRyaWMsIHVuZT11bmUsIHllYXI9eWVhciwgbW9udGg9bW9udGgsIG1lYXN1cmVkX3ZhbHVlX19pc251bGw9RmFsc2UKICAgICkuZXhpc3RzKCkKCgpkZWYgX2VtcHR5X2Jsb2NrKGJsb2NrX2lkOiBzdHIsIHN1bW1hcnk6IHN0cikgLT4gZGljdFtzdHIsIEFueV06CiAgICByZXR1cm4gewogICAgICAgICoqX2Jsb2NrX3NoZWxsKGJsb2NrX2lkKSwKICAgICAgICAic3RhdHVzIjogU1RBVFVTX1BFTkRJTkcsCiAgICAgICAgInN0YXR1c19sYWJlbCI6IF9zdGF0dXNfYmFkZ2UoU1RBVFVTX1BFTkRJTkcpLAogICAgICAgICJzdW1tYXJ5Ijogc3VtbWFyeSwKICAgICAgICAibGFzdF9hY3Rpb25fYXQiOiBOb25lLAogICAgICAgICJsYXN0X2FjdGlvbl9ieSI6IE5vbmUsCiAgICAgICAgImNoZWNrbGlzdCI6IFtdLAogICAgICAgICJzdGF0cyI6IHt9LAogICAgICAgICJ1cGxvYWRzIjogW10sCiAgICB9CgoKZGVmIF9ibG9ja19zaGVsbChibG9ja19pZDogc3RyKSAtPiBkaWN0W3N0ciwgQW55XToKICAgIG1ldGEgPSBCTE9DS19NRVRBW2Jsb2NrX2lkXQogICAgcmV0dXJuIHsKICAgICAgICAiaWQiOiBibG9ja19pZCwKICAgICAgICAic3RlcCI6IG1ldGFbInN0ZXAiXSwKICAgICAgICAibGFiZWwiOiBtZXRhWyJsYWJlbCJdLAogICAgICAgICJzaG9ydCI6IG1ldGFbInNob3J0Il0sCiAgICB9CgoKZGVmIF9wZXJpb2RfdXBsb2Fkcyh5ZWFyOiBpbnQsIG1vbnRoOiBpbnQsIGZpbGVfdHlwZTogc3RyKSAtPiBsaXN0W2RpY3Rbc3RyLCBBbnldXToKICAgIHVwbG9hZHMgPSBGaWxlVXBsb2FkLm9iamVjdHMuZmlsdGVyKAogICAgICAgIGRldGVjdGVkX3llYXI9eWVhciwKICAgICAgICBkZXRlY3RlZF9tb250aD1tb250aCwKICAgICAgICBmaWxlX3R5cGVfZGV0ZWN0ZWQ9ZmlsZV90eXBlLAogICAgKS5zZWxlY3RfcmVsYXRlZCgidXBsb2FkZWRfYnkiKS5vcmRlcl9ieSgiLWNyZWF0ZWRfYXQiKVs6NV0KICAgIHJldHVybiBbCiAgICAgICAgewogICAgICAgICAgICAiaWQiOiB1LmlkLAogICAgICAgICAgICAiZmlsZW5hbWUiOiB1Lm9yaWdpbmFsX2ZpbGVuYW1lLAogICAgICAgICAgICAic3RhdHVzIjogdS5zdGF0dXMsCiAgICAgICAgICAgICJzdGF0dXNfZGlzcGxheSI6IHUuZ2V0X3N0YXR1c19kaXNwbGF5KCksCiAgICAgICAgICAgICJjcmVhdGVkX2F0IjogdS5jcmVhdGVkX2F0LAogICAgICAgICAgICAidXNlciI6IF91cGxvYWRfYWN0b3IodSksCiAgICAgICAgICAgICJjYW5fZGlzY2FyZCI6IHUuc3RhdHVzICE9IEZpbGVVcGxvYWQuU1RBVFVTX1BBUlNFRF9PSywKICAgICAgICB9CiAgICAgICAgZm9yIHUgaW4gdXBsb2FkcwogICAgXQoKCmRlZiBfZGVyaXZlX3BlcmlvZF9zdGF0dXMoYmxvY2tzOiBsaXN0W2RpY3Rbc3RyLCBBbnldXSkgLT4gdHVwbGVbc3RyLCBzdHJdOgogICAgc3RhdHVzZXMgPSBbYlsic3RhdHVzIl0gZm9yIGIgaW4gYmxvY2tzXQogICAgaWYgYWxsKHMgaW4gKFNUQVRVU19SRVZJRVdFRCwgU1RBVFVTX0NMT1NFRCkgZm9yIHMgaW4gc3RhdHVzZXMpOgogICAgICAgIHJldHVybiBQRVJJT0RfQ0xPU0VELCBQRVJJT0RfU1RBVFVTX0xBQkVMU1tQRVJJT0RfQ0xPU0VEXQogICAgaWYgYWxsKHMgaW4gKFNUQVRVU19MT0FERUQsIFNUQVRVU19SRVZJRVdFRCwgU1RBVFVTX09CU0VSVkVELCBTVEFUVVNfQ0xPU0VEKSBmb3IgcyBpbiBzdGF0dXNlcyk6CiAgICAgICAgaWYgU1RBVFVTX09CU0VSVkVEIGluIHN0YXR1c2VzIG9yIFNUQVRVU19QRU5ESU5HIGluIHN0YXR1c2VzOgogICAgICAgICAgICByZXR1cm4gUEVSSU9EX0lOX1JFVklFVywgUEVSSU9EX1NUQVRVU19MQUJFTFNbUEVSSU9EX0lOX1JFVklFV10KICAgICAgICByZXR1cm4gUEVSSU9EX1JFQURZLCBQRVJJT0RfU1RBVFVTX0xBQkVMU1tQRVJJT0RfUkVBRFldCiAgICBpZiBhbnkocyAhPSBTVEFUVVNfUEVORElORyBmb3IgcyBpbiBzdGF0dXNlcyk6CiAgICAgICAgcmV0dXJuIFBFUklPRF9JTl9SRVZJRVcsIFBFUklPRF9TVEFUVVNfTEFCRUxTW1BFUklPRF9JTl9SRVZJRVddCiAgICByZXR1cm4gUEVSSU9EX0lOQ09NUExFVEUsIFBFUklPRF9TVEFUVVNfTEFCRUxTW1BFUklPRF9JTkNPTVBMRVRFXQoKCmRlZiBnZXRfYWRtaW5fcGVyaW9kX3NuYXBzaG90KHllYXI6IGludCwgbW9udGg6IGludCkgLT4gZGljdFtzdHIsIEFueV06CiAgICBwbGFuID0gX2dldF9wbGFuKHllYXIpCiAgICBibG9ja3MgPSBbCiAgICAgICAgX2Jsb2NrX3RhcmdldHMocGxhbiwgeWVhciwgbW9udGgpLAogICAgICAgIF9ibG9ja19maW5hbmNpYWwocGxhbiwgeWVhciwgbW9udGgpLAogICAgICAgIF9ibG9ja19uZXdfY2xpZW50cyhwbGFuLCB5ZWFyLCBtb250aCksCiAgICAgICAgX2Jsb2NrX2Nyb3NzX3NhbGUocGxhbiwgeWVhciwgbW9udGgpLAogICAgICAgIF9ibG9ja19tYW51YWxfcmVxdWlyZW1lbnRzKHBsYW4sIHllYXIsIG1vbnRoKSwKICAgICAgICBfYmxvY2tfcmV2aWV3KHBsYW4sIHllYXIsIG1vbnRoKSwKICAgIF0KICAgIHBlcmlvZF9zdGF0dXMsIHBlcmlvZF9zdGF0dXNfbGFiZWwgPSBfZGVyaXZlX3BlcmlvZF9zdGF0dXMoYmxvY2tzKQoKICAgIHVwbG9hZHMgPSBGaWxlVXBsb2FkLm9iamVjdHMuZmlsdGVyKGRldGVjdGVkX3llYXI9eWVhciwgZGV0ZWN0ZWRfbW9udGg9bW9udGgpCiAgICB2YWxpZF9yb3dzID0gKAogICAgICAgIE5ld0NsaWVudEltcG9ydFJvdy5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIsIG1vbnRoPW1vbnRoLCBjb3VudHNfYXNfbmV3PVRydWUpLmNvdW50KCkKICAgICAgICArIENyb3NzU2FsZUltcG9ydFJvdy5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKS5jb3VudCgpCiAgICApCiAgICBvYnNfcm93cyA9IE5ld0NsaWVudEltcG9ydFJvdy5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKS5leGNsdWRlKG9ic2VydmF0aW9ucz0iIikuY291bnQoKQogICAgcGVuZGluZ19hbGlhc2VzID0gX2NvdW50X3BlbmRpbmdfYWxpYXNlcyh5ZWFyLCBtb250aCkKCiAgICBzY29yZV9sYXRlc3QgPSBOb25lCiAgICBpZiBwbGFuOgogICAgICAgIHNjID0gKAogICAgICAgICAgICBNb250aGx5TW9kZVNjb3JlY2FyZC5vYmplY3RzLmZpbHRlcihwbGFuPXBsYW4sIHllYXI9eWVhciwgbW9udGg9bW9udGgpCiAgICAgICAgICAgIC5vcmRlcl9ieSgiLXVwZGF0ZWRfYXQiKQogICAgICAgICAgICAuZmlyc3QoKQogICAgICAgICkKICAgICAgICBzY29yZV9sYXRlc3QgPSBzYy51cGRhdGVkX2F0IGlmIHNjIGVsc2UgTm9uZQoKICAgIHJldHVybiB7CiAgICAgICAgInllYXIiOiB5ZWFyLAogICAgICAgICJtb250aCI6IG1vbnRoLAogICAgICAgICJsYWJlbCI6IF9wZXJpb2RfbGFiZWwoeWVhciwgbW9udGgpLAogICAgICAgICJwbGFuIjogcGxhbiwKICAgICAgICAicGVyaW9kX3N0YXR1cyI6IHBlcmlvZF9zdGF0dXMsCiAgICAgICAgInBlcmlvZF9zdGF0dXNfbGFiZWwiOiBwZXJpb2Rfc3RhdHVzX2xhYmVsLAogICAgICAgICJibG9ja3MiOiBibG9ja3MsCiAgICAgICAgImJsb2Nrc19ieV9pZCI6IHtiWyJpZCJdOiBiIGZvciBiIGluIGJsb2Nrc30sCiAgICAgICAgInN1bW1hcnkiOiB7CiAgICAgICAgICAgICJmaWxlc19sb2FkZWQiOiB1cGxvYWRzLmNvdW50KCksCiAgICAgICAgICAgICJ2YWxpZF9yb3dzIjogdmFsaWRfcm93cywKICAgICAgICAgICAgInJvd3Nfd2l0aF9vYnNlcnZhdGlvbnMiOiBvYnNfcm93cywKICAgICAgICAgICAgInBlbmRpbmdfYWxpYXNlcyI6IHBlbmRpbmdfYWxpYXNlcywKICAgICAgICAgICAgIm1ldHJpY3NfcmVjYWxjdWxhdGVkIjogc2NvcmVfbGF0ZXN0IGlzIG5vdCBOb25lLAogICAgICAgICAgICAibGFzdF9zY29yZV91cGRhdGUiOiBzY29yZV9sYXRlc3QsCiAgICAgICAgfSwKICAgIH0KCgpkZWYgbGlzdF9wZXJpb2RfbG9nKAogICAgeWVhcjogaW50LAogICAgbW9udGg6IGludCwKICAgIGxpbWl0OiBpbnQgPSA1MCwKICAgIG1vbnRoX2Zyb206IGludCB8IE5vbmUgPSBOb25lLAopIC0+IGxpc3RbZGljdFtzdHIsIEFueV1dOgogICAgZW50cmllczogbGlzdFtkaWN0W3N0ciwgQW55XV0gPSBbXQogICAgbWYgPSBtb250aF9mcm9tIG9yIG1vbnRoCgogICAgdXBsb2FkcyA9ICgKICAgICAgICBGaWxlVXBsb2FkLm9iamVjdHMuZmlsdGVyKAogICAgICAgICAgICBkZXRlY3RlZF95ZWFyPXllYXIsCiAgICAgICAgICAgIGRldGVjdGVkX21vbnRoX19ndGU9bWYsCiAgICAgICAgICAgIGRldGVjdGVkX21vbnRoX19sdGU9bW9udGgsCiAgICAgICAgKQogICAgICAgIC5zZWxlY3RfcmVsYXRlZCgidXBsb2FkZWRfYnkiKQogICAgICAgIC5vcmRlcl9ieSgiLWNyZWF0ZWRfYXQiKQogICAgKQogICAgZm9yIHVwbG9hZCBpbiB1cGxvYWRzWzpsaW1pdF06CiAgICAgICAgZW50cmllcy5hcHBlbmQoCiAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICJhdCI6IHVwbG9hZC5jcmVhdGVkX2F0LAogICAgICAgICAgICAgICAgImxldmVsIjogIklORk8iLAogICAgICAgICAgICAgICAgInRpdGxlIjogZiJBcmNoaXZvOiB7dXBsb2FkLm9yaWdpbmFsX2ZpbGVuYW1lfSIsCiAgICAgICAgICAgICAgICAiZGV0YWlsIjogKAogICAgICAgICAgICAgICAgICAgIGYiVGlwbyB7dXBsb2FkLmdldF9maWxlX3R5cGVfZGV0ZWN0ZWRfZGlzcGxheSgpfSDCtyAiCiAgICAgICAgICAgICAgICAgICAgZiJFc3RhZG8ge3VwbG9hZC5nZXRfc3RhdHVzX2Rpc3BsYXkoKX0iCiAgICAgICAgICAgICAgICApLAogICAgICAgICAgICAgICAgInVzZXIiOiBfdXBsb2FkX2FjdG9yKHVwbG9hZCksCiAgICAgICAgICAgICAgICAia2luZCI6ICJ1cGxvYWQiLAogICAgICAgICAgICB9CiAgICAgICAgKQogICAgICAgIGZvciBsb2cgaW4gdXBsb2FkLmxvZ3MuYWxsKCkub3JkZXJfYnkoIi1jcmVhdGVkX2F0IilbOjEwXToKICAgICAgICAgICAgZW50cmllcy5hcHBlbmQoCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgImF0IjogbG9nLmNyZWF0ZWRfYXQsCiAgICAgICAgICAgICAgICAgICAgImxldmVsIjogbG9nLmxldmVsLAogICAgICAgICAgICAgICAgICAgICJ0aXRsZSI6IGxvZy5zdGVwX2NvZGUgb3IgIkltcG9ydGFjacOzbiIsCiAgICAgICAgICAgICAgICAgICAgImRldGFpbCI6IGxvZy5tZXNzYWdlLAogICAgICAgICAgICAgICAgICAgICJ1c2VyIjogX3VwbG9hZF9hY3Rvcih1cGxvYWQpLAogICAgICAgICAgICAgICAgICAgICJraW5kIjogImxvZyIsCiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICkKCiAgICBlbnRyaWVzLnNvcnQoa2V5PWxhbWJkYSBlOiBlWyJhdCJdIG9yIHRpbWV6b25lLm5vdygpLCByZXZlcnNlPVRydWUpCgogICAgZm9yIGVkaXQgaW4gQWRtaW5NYW51YWxFZGl0TG9nLm9iamVjdHMuZmlsdGVyKAogICAgICAgIHllYXI9eWVhciwgbW9udGhfX2d0ZT1tZiwgbW9udGhfX2x0ZT1tb250aAogICAgKS5zZWxlY3RfcmVsYXRlZCgiZWRpdGVkX2J5IilbOmxpbWl0XToKICAgICAgICBlbnRyaWVzLmFwcGVuZCgKICAgICAgICAgICAgewogICAgICAgICAgICAgICAgImF0IjogZWRpdC5jcmVhdGVkX2F0LAogICAgICAgICAgICAgICAgImxldmVsIjogIklORk8iLAogICAgICAgICAgICAgICAgInRpdGxlIjogZiJFZGljacOzbiBtYW51YWw6IHtlZGl0LmdldF9lbnRpdHlfdHlwZV9kaXNwbGF5KCl9IiwKICAgICAgICAgICAgICAgICJkZXRhaWwiOiAoCiAgICAgICAgICAgICAgICAgICAgZiJ7ZWRpdC5maWVsZF9uYW1lfToge2VkaXQub2xkX3ZhbHVlIG9yICfigJQnfSDihpIge2VkaXQubmV3X3ZhbHVlIG9yICfigJQnfSIKICAgICAgICAgICAgICAgICAgICArIChmIiDCtyBNb3Rpdm86IHtlZGl0LnJlYXNvbn0iIGlmIGVkaXQucmVhc29uIGVsc2UgIiIpCiAgICAgICAgICAgICAgICApLAogICAgICAgICAgICAgICAgInVzZXIiOiBlZGl0LmVkaXRlZF9ieS51c2VybmFtZSBpZiBlZGl0LmVkaXRlZF9ieSBlbHNlIE5vbmUsCiAgICAgICAgICAgICAgICAia2luZCI6ICJtYW51YWxfZWRpdCIsCiAgICAgICAgICAgIH0KICAgICAgICApCgogICAgZW50cmllcy5zb3J0KGtleT1sYW1iZGEgZTogZVsiYXQiXSBvciB0aW1lem9uZS5ub3coKSwgcmV2ZXJzZT1UcnVlKQogICAgcmV0dXJuIGVudHJpZXNbOmxpbWl0XQoKCmRlZiByZWNhbGN1bGF0ZV9wZXJpb2QoeWVhcjogaW50LCBtb250aDogaW50KSAtPiBsaXN0W3N0cl06CiAgICBtZXNzYWdlc19vdXQ6IGxpc3Rbc3RyXSA9IFtdCiAgICBjYWxsX2NvbW1hbmQoInJlY2FsY19pbnZlc3RtZW50X2luZ3Jlc29zX2Zyb21fbmV3X2NsaWVudHMiLCB5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKQogICAgbWVzc2FnZXNfb3V0LmFwcGVuZChmIkluZ3Jlc29zIEludmVzdG1lbnQgcmVjYWxjdWxhZG9zIHBhcmEge19wZXJpb2RfbGFiZWwoeWVhciwgbW9udGgpfS4iKQogICAgZm9yIG1vZGUgaW4gKCJtb2RvMSIsICJtb2RvMiIpOgogICAgICAgIGNhbGxfY29tbWFuZCgicmVjYWxjX3BnYyIsIHllYXI9eWVhciwgbW9udGg9bW9udGgsIG1vZGU9bW9kZSkKICAgIG1lc3NhZ2VzX291dC5hcHBlbmQoZiJTY29yZSBQR0MgcmVjYWxjdWxhZG8gKG1vZG8xIHkgbW9kbzIpIHBhcmEge19wZXJpb2RfbGFiZWwoeWVhciwgbW9udGgpfS4iKQogICAgcmV0dXJuIG1lc3NhZ2VzX291dAoKCmRlZiByZWNhbGN1bGF0ZV9ibG9jayh5ZWFyOiBpbnQsIG1vbnRoOiBpbnQsIGJsb2NrX3R5cGU6IHN0cikgLT4gbGlzdFtzdHJdOgogICAgbGFiZWwgPSBfcGVyaW9kX2xhYmVsKHllYXIsIG1vbnRoKQogICAgaWYgYmxvY2tfdHlwZSA9PSBCTE9DS19ORVdfQ0xJRU5UUzoKICAgICAgICBjYWxsX2NvbW1hbmQoInJlY2FsY19pbnZlc3RtZW50X2luZ3Jlc29zX2Zyb21fbmV3X2NsaWVudHMiLCB5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKQogICAgICAgIHJldHVybiBbZiJJbmdyZXNvcyBJbnZlc3RtZW50IHJlY2FsY3VsYWRvcyBwYXJhIHtsYWJlbH0uIl0KICAgIGlmIGJsb2NrX3R5cGUgaW4gKEJMT0NLX0ZJTkFOQ0lBTCwgQkxPQ0tfQ1JPU1NfU0FMRSwgQkxPQ0tfTUFOVUFMX1JFUVVJUkVNRU5UUywgQkxPQ0tfUkVWSUVXKToKICAgICAgICBjYWxsX2NvbW1hbmQoInJlY2FsY19wZ2MiLCB5ZWFyPXllYXIsIG1vbnRoPW1vbnRoLCBtb2RlPSJtb2RvMSIpCiAgICAgICAgcmV0dXJuIFtmIlNjb3JlIFBHQyByZWNhbGN1bGFkbyBwYXJhIHtsYWJlbH0uIl0KICAgIGlmIGJsb2NrX3R5cGUgPT0gQkxPQ0tfVEFSR0VUUzoKICAgICAgICByZXR1cm4gWyJMYXMgbWV0YXMgbm8gcmVxdWllcmVuIHJlY8OhbGN1bG8uIl0KICAgIHJldHVybiBbIk9wZXJhY2nDs24gbm8gYXBsaWNhYmxlIGEgZXN0ZSBibG9xdWUuIl0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/admin_recalc.py
PATH_JSON="pgc/admin_recalc.py"
FILENAME=admin_recalc.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=324
SIZE_BYTES_UTF8=11174
CONTENT_SHA256=a6e8ccdb667dcb0e46534ff1fda19ad3a309de149d9472aeb8e113ba68140769
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
Recálculo inteligente global: detecta pendientes en todos los períodos
y ejecuta la cadena en orden estricto.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from django.core.management import call_command
from django.db.models import Max
from django.utils import timezone

from core.models import MetricDefinition, UNE
from imports.models import CrossSaleImportRow, FileUpload, NewClientImportRow
from pgc.income_conversion import count_stale_ingresos, recalc_stale_ingresos
from pgc.models import (
    ManualRequirementsCompliance,
    MonthlyMetricResult,
    MonthlyModeScorecard,
    MonthlyTarget,
    PGCPlan,
)

MODES = ("modo1", "modo2")
INVESTMENT_CODES = ("INVESTMENT", "INVESTMENTS", "INVERSIONES")


def _aware(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


def _max_ts(*values: datetime | None) -> datetime | None:
    aware = [_aware(v) for v in values if v is not None]
    return max(aware) if aware else None


def iter_known_periods() -> list[tuple[int, int]]:
    """Todos los (año, mes) con presencia de datos PGC / imports."""
    periods: set[tuple[int, int]] = set()

    for year, month in MonthlyTarget.objects.values_list("year", "month").distinct():
        periods.add((year, month))
    for year, month in MonthlyMetricResult.objects.values_list("year", "month").distinct():
        periods.add((year, month))
    for year, month in NewClientImportRow.objects.values_list("year", "month").distinct():
        periods.add((year, month))
    for year, month in CrossSaleImportRow.objects.values_list("year", "month").distinct():
        periods.add((year, month))
    for year, month in ManualRequirementsCompliance.objects.values_list(
        "year", "month"
    ).distinct():
        periods.add((year, month))
    for year, month in MonthlyModeScorecard.objects.values_list("year", "month").distinct():
        periods.add((year, month))
    for year, month in (
        FileUpload.objects.exclude(detected_year__isnull=True)
        .exclude(detected_month__isnull=True)
        .values_list("detected_year", "detected_month")
        .distinct()
    ):
        periods.add((int(year), int(month)))

    # Años con plan: al menos asegurar meses donde haya plan, aunque vacíos
    # (no los agregamos vacíos — solo datos reales).
    return sorted(periods)


def _investment_une() -> UNE | None:
    return (
        UNE.objects.filter(code__in=INVESTMENT_CODES)
        .order_by("sort_order", "id")
        .first()
    )


def _ingresos_metric() -> MetricDefinition | None:
    return MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()


def _data_timestamp(year: int, month: int) -> datetime | None:
    """Última modificación de insumos que alimentan el score."""
    stamps: list[datetime | None] = []
    for model in (
        MonthlyTarget,
        MonthlyMetricResult,
        NewClientImportRow,
        CrossSaleImportRow,
        ManualRequirementsCompliance,
    ):
        stamps.append(
            model.objects.filter(year=year, month=month).aggregate(m=Max("updated_at"))["m"]
        )
    stamps.append(
        FileUpload.objects.filter(detected_year=year, detected_month=month).aggregate(
            m=Max("created_at")
        )["m"]
    )
    return _max_ts(*stamps)


def _score_timestamp(plan: PGCPlan | None, year: int, month: int) -> datetime | None:
    if not plan:
        return None
    stamps = []
    qs = MonthlyModeScorecard.objects.filter(plan=plan, year=year, month=month)
    for mode in MODES:
        stamps.append(qs.filter(mode=mode).aggregate(m=Max("updated_at"))["m"])
    return _max_ts(*stamps)


def _has_scoreable_data(year: int, month: int) -> bool:
    return (
        MonthlyTarget.objects.filter(year=year, month=month).exists()
        or MonthlyMetricResult.objects.filter(year=year, month=month).exists()
        or NewClientImportRow.objects.filter(year=year, month=month).exists()
        or CrossSaleImportRow.objects.filter(year=year, month=month).exists()
        or ManualRequirementsCompliance.objects.filter(year=year, month=month).exists()
    )


def _score_complete(plan: PGCPlan | None, year: int, month: int) -> bool:
    if not plan:
        return False
    une_count = UNE.objects.filter(is_active=True).count()
    if une_count == 0:
        return False
    for mode in MODES:
        n = MonthlyModeScorecard.objects.filter(
            plan=plan, year=year, month=month, mode=mode
        ).count()
        if n < une_count:
            return False
    return True


def period_pending_reasons(year: int, month: int) -> list[str]:
    """Razones por las que el período necesita la cadena de recálculo."""
    reasons: list[str] = []
    plan = PGCPlan.objects.filter(year=year).first()
    label = f"{year}-{month:02d}"

    stale = count_stale_ingresos(year, month)
    if stale:
        reasons.append(f"{stale} ingreso(s) con TC desactualizado (STALE)")

    inv_une = _investment_une()
    metric = _ingresos_metric()
    if inv_une and NewClientImportRow.objects.filter(
        year=year, month=month, une=inv_une
    ).exists():
        latest_row_ts = NewClientImportRow.objects.filter(
            year=year, month=month, une=inv_une
        ).aggregate(m=Max("updated_at"))["m"]
        result = None
        if plan and metric:
            result = MonthlyMetricResult.objects.filter(
                plan=plan,
                metric=metric,
                une=inv_une,
                year=year,
                month=month,
            ).first()
        if result is None or result.measured_value is None:
            reasons.append("Ingresos Investment sin calcular desde clientes")
        elif latest_row_ts and result.updated_at and _aware(result.updated_at) < _aware(
            latest_row_ts
        ):
            reasons.append("Ingresos Investment desactualizados vs clientes")

    if _has_scoreable_data(year, month):
        if not plan:
            reasons.append(f"Sin plan PGC para {year} (no se puede scorear)")
        elif not _score_complete(plan, year, month):
            reasons.append("Score PGC incompleto (modo1/modo2)")
        else:
            data_ts = _data_timestamp(year, month)
            score_ts = _score_timestamp(plan, year, month)
            if data_ts and score_ts and score_ts < data_ts:
                reasons.append("Score desactualizado respecto a los datos")
            elif data_ts and not score_ts:
                reasons.append(f"Sin score para {label}")

    return reasons


def get_global_recalc_status() -> dict[str, Any]:
    pending_periods: list[dict[str, Any]] = []
    for year, month in iter_known_periods():
        reasons = period_pending_reasons(year, month)
        if reasons:
            pending_periods.append(
                {
                    "year": year,
                    "month": month,
                    "label": f"{year}-{month:02d}",
                    "reasons": reasons,
                }
            )

    pending_count = len(pending_periods)
    is_pending = pending_count > 0
    return {
        "is_pending": is_pending,
        "is_ready": not is_pending,
        "pending_count": pending_count,
        "pending_periods": pending_periods,
        "state": "pending" if is_pending else "ready",
        "state_label": (
            f"Pendiente · {pending_count} período(s)"
            if is_pending
            else "Al día · sin pendientes"
        ),
        "button_label": (
            f"△ Recalcular pendientes ({pending_count})"
            if is_pending
            else "✓ Recalcular (todo al día)"
        ),
        "button_hint": (
            "Hay cálculos faltantes o desactualizados en uno o más períodos."
            if is_pending
            else "No hay pendientes. Puede ejecutar de todos modos si quiere forzar revisión."
        ),
    }


def run_period_recalc_chain(
    year: int,
    month: int,
    *,
    user=None,
    force: bool = False,
) -> list[str]:
    """
    Orden estricto por período:
    1) Ingresos STALE GTQ→USD
    2) Ingresos Investment desde clientes nuevos
    3) Score PGC modo1 + modo2
    """
    messages_out: list[str] = []
    label = f"{year}-{month:02d}"

    try:
        stale_result = recalc_stale_ingresos(
            year=year,
            month=month,
            user=user,
            reason=f"Recálculo inteligente {label}",
            only_stale=True,
        )
        if stale_result["updated"]:
            messages_out.append(
                f"{label}: {stale_result['updated']} ingreso(s) STALE → USD "
                f"(TC={stale_result['fx']})."
            )
    except ValueError as exc:
        # Sin TC: no bloquear el resto; avisar.
        if count_stale_ingresos(year, month):
            messages_out.append(f"{label}: STALE no convertido — {exc}")

    has_clients = NewClientImportRow.objects.filter(year=year, month=month).exists()
    if has_clients or force:
        call_command(
            "recalc_investment_ingresos_from_new_clients", year=year, month=month
        )
        messages_out.append(f"{label}: ingresos Investment recalculados.")

    if _has_scoreable_data(year, month) or force or has_clients:
        for mode in MODES:
            call_command("recalc_pgc", year=year, month=month, mode=mode)
        messages_out.append(f"{label}: score PGC (modo1 y modo2) recalculado.")

    if not messages_out:
        messages_out.append(f"{label}: sin operaciones aplicables.")
    return messages_out


def run_smart_recalc_all(*, user=None, force_all: bool = False) -> dict[str, Any]:
    """
    Si hay pendientes: recalcula solo esos períodos (en orden cronológico).
    Si no hay pendientes y force_all=False: no-op informativo.
    Si force_all=True: corre la cadena en todos los períodos conocidos.
    """
    status_before = get_global_recalc_status()
    if force_all:
        targets = [
            {"year": y, "month": m, "label": f"{y}-{m:02d}", "reasons": ["forzado"]}
            for y, m in iter_known_periods()
        ]
    else:
        targets = list(status_before["pending_periods"])

    if not targets:
        return {
            "ran": False,
            "periods_processed": 0,
            "messages": ["Nada pendiente de calcular. Todo al día."],
            "status_before": status_before,
            "status_after": status_before,
        }

    messages: list[str] = []
    for item in targets:
        year, month = item["year"], item["month"]
        try:
            messages.extend(
                run_period_recalc_chain(year, month, user=user, force=force_all)
            )
        except Exception as exc:  # keep going across periods
            messages.append(f"{item['label']}: error — {exc}")

    status_after = get_global_recalc_status()
    return {
        "ran": True,
        "periods_processed": len(targets),
        "messages": messages,
        "status_before": status_before,
        "status_after": status_after,
    }

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Recálculo inteligente global: detecta pendientes en todos los períodos
00003|y ejecuta la cadena en orden estricto.
00004|"""
00005|
00006|from __future__ import annotations
00007|
00008|from datetime import datetime
00009|from typing import Any
00010|
00011|from django.core.management import call_command
00012|from django.db.models import Max
00013|from django.utils import timezone
00014|
00015|from core.models import MetricDefinition, UNE
00016|from imports.models import CrossSaleImportRow, FileUpload, NewClientImportRow
00017|from pgc.income_conversion import count_stale_ingresos, recalc_stale_ingresos
00018|from pgc.models import (
00019|    ManualRequirementsCompliance,
00020|    MonthlyMetricResult,
00021|    MonthlyModeScorecard,
00022|    MonthlyTarget,
00023|    PGCPlan,
00024|)
00025|
00026|MODES = ("modo1", "modo2")
00027|INVESTMENT_CODES = ("INVESTMENT", "INVESTMENTS", "INVERSIONES")
00028|
00029|
00030|def _aware(dt: datetime | None) -> datetime | None:
00031|    if dt is None:
00032|        return None
00033|    if timezone.is_naive(dt):
00034|        return timezone.make_aware(dt, timezone.get_current_timezone())
00035|    return dt
00036|
00037|
00038|def _max_ts(*values: datetime | None) -> datetime | None:
00039|    aware = [_aware(v) for v in values if v is not None]
00040|    return max(aware) if aware else None
00041|
00042|
00043|def iter_known_periods() -> list[tuple[int, int]]:
00044|    """Todos los (año, mes) con presencia de datos PGC / imports."""
00045|    periods: set[tuple[int, int]] = set()
00046|
00047|    for year, month in MonthlyTarget.objects.values_list("year", "month").distinct():
00048|        periods.add((year, month))
00049|    for year, month in MonthlyMetricResult.objects.values_list("year", "month").distinct():
00050|        periods.add((year, month))
00051|    for year, month in NewClientImportRow.objects.values_list("year", "month").distinct():
00052|        periods.add((year, month))
00053|    for year, month in CrossSaleImportRow.objects.values_list("year", "month").distinct():
00054|        periods.add((year, month))
00055|    for year, month in ManualRequirementsCompliance.objects.values_list(
00056|        "year", "month"
00057|    ).distinct():
00058|        periods.add((year, month))
00059|    for year, month in MonthlyModeScorecard.objects.values_list("year", "month").distinct():
00060|        periods.add((year, month))
00061|    for year, month in (
00062|        FileUpload.objects.exclude(detected_year__isnull=True)
00063|        .exclude(detected_month__isnull=True)
00064|        .values_list("detected_year", "detected_month")
00065|        .distinct()
00066|    ):
00067|        periods.add((int(year), int(month)))
00068|
00069|    # Años con plan: al menos asegurar meses donde haya plan, aunque vacíos
00070|    # (no los agregamos vacíos — solo datos reales).
00071|    return sorted(periods)
00072|
00073|
00074|def _investment_une() -> UNE | None:
00075|    return (
00076|        UNE.objects.filter(code__in=INVESTMENT_CODES)
00077|        .order_by("sort_order", "id")
00078|        .first()
00079|    )
00080|
00081|
00082|def _ingresos_metric() -> MetricDefinition | None:
00083|    return MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
00084|
00085|
00086|def _data_timestamp(year: int, month: int) -> datetime | None:
00087|    """Última modificación de insumos que alimentan el score."""
00088|    stamps: list[datetime | None] = []
00089|    for model in (
00090|        MonthlyTarget,
00091|        MonthlyMetricResult,
00092|        NewClientImportRow,
00093|        CrossSaleImportRow,
00094|        ManualRequirementsCompliance,
00095|    ):
00096|        stamps.append(
00097|            model.objects.filter(year=year, month=month).aggregate(m=Max("updated_at"))["m"]
00098|        )
00099|    stamps.append(
00100|        FileUpload.objects.filter(detected_year=year, detected_month=month).aggregate(
00101|            m=Max("created_at")
00102|        )["m"]
00103|    )
00104|    return _max_ts(*stamps)
00105|
00106|
00107|def _score_timestamp(plan: PGCPlan | None, year: int, month: int) -> datetime | None:
00108|    if not plan:
00109|        return None
00110|    stamps = []
00111|    qs = MonthlyModeScorecard.objects.filter(plan=plan, year=year, month=month)
00112|    for mode in MODES:
00113|        stamps.append(qs.filter(mode=mode).aggregate(m=Max("updated_at"))["m"])
00114|    return _max_ts(*stamps)
00115|
00116|
00117|def _has_scoreable_data(year: int, month: int) -> bool:
00118|    return (
00119|        MonthlyTarget.objects.filter(year=year, month=month).exists()
00120|        or MonthlyMetricResult.objects.filter(year=year, month=month).exists()
00121|        or NewClientImportRow.objects.filter(year=year, month=month).exists()
00122|        or CrossSaleImportRow.objects.filter(year=year, month=month).exists()
00123|        or ManualRequirementsCompliance.objects.filter(year=year, month=month).exists()
00124|    )
00125|
00126|
00127|def _score_complete(plan: PGCPlan | None, year: int, month: int) -> bool:
00128|    if not plan:
00129|        return False
00130|    une_count = UNE.objects.filter(is_active=True).count()
00131|    if une_count == 0:
00132|        return False
00133|    for mode in MODES:
00134|        n = MonthlyModeScorecard.objects.filter(
00135|            plan=plan, year=year, month=month, mode=mode
00136|        ).count()
00137|        if n < une_count:
00138|            return False
00139|    return True
00140|
00141|
00142|def period_pending_reasons(year: int, month: int) -> list[str]:
00143|    """Razones por las que el período necesita la cadena de recálculo."""
00144|    reasons: list[str] = []
00145|    plan = PGCPlan.objects.filter(year=year).first()
00146|    label = f"{year}-{month:02d}"
00147|
00148|    stale = count_stale_ingresos(year, month)
00149|    if stale:
00150|        reasons.append(f"{stale} ingreso(s) con TC desactualizado (STALE)")
00151|
00152|    inv_une = _investment_une()
00153|    metric = _ingresos_metric()
00154|    if inv_une and NewClientImportRow.objects.filter(
00155|        year=year, month=month, une=inv_une
00156|    ).exists():
00157|        latest_row_ts = NewClientImportRow.objects.filter(
00158|            year=year, month=month, une=inv_une
00159|        ).aggregate(m=Max("updated_at"))["m"]
00160|        result = None
00161|        if plan and metric:
00162|            result = MonthlyMetricResult.objects.filter(
00163|                plan=plan,
00164|                metric=metric,
00165|                une=inv_une,
00166|                year=year,
00167|                month=month,
00168|            ).first()
00169|        if result is None or result.measured_value is None:
00170|            reasons.append("Ingresos Investment sin calcular desde clientes")
00171|        elif latest_row_ts and result.updated_at and _aware(result.updated_at) < _aware(
00172|            latest_row_ts
00173|        ):
00174|            reasons.append("Ingresos Investment desactualizados vs clientes")
00175|
00176|    if _has_scoreable_data(year, month):
00177|        if not plan:
00178|            reasons.append(f"Sin plan PGC para {year} (no se puede scorear)")
00179|        elif not _score_complete(plan, year, month):
00180|            reasons.append("Score PGC incompleto (modo1/modo2)")
00181|        else:
00182|            data_ts = _data_timestamp(year, month)
00183|            score_ts = _score_timestamp(plan, year, month)
00184|            if data_ts and score_ts and score_ts < data_ts:
00185|                reasons.append("Score desactualizado respecto a los datos")
00186|            elif data_ts and not score_ts:
00187|                reasons.append(f"Sin score para {label}")
00188|
00189|    return reasons
00190|
00191|
00192|def get_global_recalc_status() -> dict[str, Any]:
00193|    pending_periods: list[dict[str, Any]] = []
00194|    for year, month in iter_known_periods():
00195|        reasons = period_pending_reasons(year, month)
00196|        if reasons:
00197|            pending_periods.append(
00198|                {
00199|                    "year": year,
00200|                    "month": month,
00201|                    "label": f"{year}-{month:02d}",
00202|                    "reasons": reasons,
00203|                }
00204|            )
00205|
00206|    pending_count = len(pending_periods)
00207|    is_pending = pending_count > 0
00208|    return {
00209|        "is_pending": is_pending,
00210|        "is_ready": not is_pending,
00211|        "pending_count": pending_count,
00212|        "pending_periods": pending_periods,
00213|        "state": "pending" if is_pending else "ready",
00214|        "state_label": (
00215|            f"Pendiente · {pending_count} período(s)"
00216|            if is_pending
00217|            else "Al día · sin pendientes"
00218|        ),
00219|        "button_label": (
00220|            f"△ Recalcular pendientes ({pending_count})"
00221|            if is_pending
00222|            else "✓ Recalcular (todo al día)"
00223|        ),
00224|        "button_hint": (
00225|            "Hay cálculos faltantes o desactualizados en uno o más períodos."
00226|            if is_pending
00227|            else "No hay pendientes. Puede ejecutar de todos modos si quiere forzar revisión."
00228|        ),
00229|    }
00230|
00231|
00232|def run_period_recalc_chain(
00233|    year: int,
00234|    month: int,
00235|    *,
00236|    user=None,
00237|    force: bool = False,
00238|) -> list[str]:
00239|    """
00240|    Orden estricto por período:
00241|    1) Ingresos STALE GTQ→USD
00242|    2) Ingresos Investment desde clientes nuevos
00243|    3) Score PGC modo1 + modo2
00244|    """
00245|    messages_out: list[str] = []
00246|    label = f"{year}-{month:02d}"
00247|
00248|    try:
00249|        stale_result = recalc_stale_ingresos(
00250|            year=year,
00251|            month=month,
00252|            user=user,
00253|            reason=f"Recálculo inteligente {label}",
00254|            only_stale=True,
00255|        )
00256|        if stale_result["updated"]:
00257|            messages_out.append(
00258|                f"{label}: {stale_result['updated']} ingreso(s) STALE → USD "
00259|                f"(TC={stale_result['fx']})."
00260|            )
00261|    except ValueError as exc:
00262|        # Sin TC: no bloquear el resto; avisar.
00263|        if count_stale_ingresos(year, month):
00264|            messages_out.append(f"{label}: STALE no convertido — {exc}")
00265|
00266|    has_clients = NewClientImportRow.objects.filter(year=year, month=month).exists()
00267|    if has_clients or force:
00268|        call_command(
00269|            "recalc_investment_ingresos_from_new_clients", year=year, month=month
00270|        )
00271|        messages_out.append(f"{label}: ingresos Investment recalculados.")
00272|
00273|    if _has_scoreable_data(year, month) or force or has_clients:
00274|        for mode in MODES:
00275|            call_command("recalc_pgc", year=year, month=month, mode=mode)
00276|        messages_out.append(f"{label}: score PGC (modo1 y modo2) recalculado.")
00277|
00278|    if not messages_out:
00279|        messages_out.append(f"{label}: sin operaciones aplicables.")
00280|    return messages_out
00281|
00282|
00283|def run_smart_recalc_all(*, user=None, force_all: bool = False) -> dict[str, Any]:
00284|    """
00285|    Si hay pendientes: recalcula solo esos períodos (en orden cronológico).
00286|    Si no hay pendientes y force_all=False: no-op informativo.
00287|    Si force_all=True: corre la cadena en todos los períodos conocidos.
00288|    """
00289|    status_before = get_global_recalc_status()
00290|    if force_all:
00291|        targets = [
00292|            {"year": y, "month": m, "label": f"{y}-{m:02d}", "reasons": ["forzado"]}
00293|            for y, m in iter_known_periods()
00294|        ]
00295|    else:
00296|        targets = list(status_before["pending_periods"])
00297|
00298|    if not targets:
00299|        return {
00300|            "ran": False,
00301|            "periods_processed": 0,
00302|            "messages": ["Nada pendiente de calcular. Todo al día."],
00303|            "status_before": status_before,
00304|            "status_after": status_before,
00305|        }
00306|
00307|    messages: list[str] = []
00308|    for item in targets:
00309|        year, month = item["year"], item["month"]
00310|        try:
00311|            messages.extend(
00312|                run_period_recalc_chain(year, month, user=user, force=force_all)
00313|            )
00314|        except Exception as exc:  # keep going across periods
00315|            messages.append(f"{item['label']}: error — {exc}")
00316|
00317|    status_after = get_global_recalc_status()
00318|    return {
00319|        "ran": True,
00320|        "periods_processed": len(targets),
00321|        "messages": messages,
00322|        "status_before": status_before,
00323|        "status_after": status_after,
00324|    }

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiClJlY8OhbGN1bG8gaW50ZWxpZ2VudGUgZ2xvYmFsOiBkZXRlY3RhIHBlbmRpZW50ZXMgZW4gdG9kb3MgbG9zIHBlcsOtb2Rvcwp5IGVqZWN1dGEgbGEgY2FkZW5hIGVuIG9yZGVuIGVzdHJpY3RvLgoiIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmZyb20gZGF0ZXRpbWUgaW1wb3J0IGRhdGV0aW1lCmZyb20gdHlwaW5nIGltcG9ydCBBbnkKCmZyb20gZGphbmdvLmNvcmUubWFuYWdlbWVudCBpbXBvcnQgY2FsbF9jb21tYW5kCmZyb20gZGphbmdvLmRiLm1vZGVscyBpbXBvcnQgTWF4CmZyb20gZGphbmdvLnV0aWxzIGltcG9ydCB0aW1lem9uZQoKZnJvbSBjb3JlLm1vZGVscyBpbXBvcnQgTWV0cmljRGVmaW5pdGlvbiwgVU5FCmZyb20gaW1wb3J0cy5tb2RlbHMgaW1wb3J0IENyb3NzU2FsZUltcG9ydFJvdywgRmlsZVVwbG9hZCwgTmV3Q2xpZW50SW1wb3J0Um93CmZyb20gcGdjLmluY29tZV9jb252ZXJzaW9uIGltcG9ydCBjb3VudF9zdGFsZV9pbmdyZXNvcywgcmVjYWxjX3N0YWxlX2luZ3Jlc29zCmZyb20gcGdjLm1vZGVscyBpbXBvcnQgKAogICAgTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZSwKICAgIE1vbnRobHlNZXRyaWNSZXN1bHQsCiAgICBNb250aGx5TW9kZVNjb3JlY2FyZCwKICAgIE1vbnRobHlUYXJnZXQsCiAgICBQR0NQbGFuLAopCgpNT0RFUyA9ICgibW9kbzEiLCAibW9kbzIiKQpJTlZFU1RNRU5UX0NPREVTID0gKCJJTlZFU1RNRU5UIiwgIklOVkVTVE1FTlRTIiwgIklOVkVSU0lPTkVTIikKCgpkZWYgX2F3YXJlKGR0OiBkYXRldGltZSB8IE5vbmUpIC0+IGRhdGV0aW1lIHwgTm9uZToKICAgIGlmIGR0IGlzIE5vbmU6CiAgICAgICAgcmV0dXJuIE5vbmUKICAgIGlmIHRpbWV6b25lLmlzX25haXZlKGR0KToKICAgICAgICByZXR1cm4gdGltZXpvbmUubWFrZV9hd2FyZShkdCwgdGltZXpvbmUuZ2V0X2N1cnJlbnRfdGltZXpvbmUoKSkKICAgIHJldHVybiBkdAoKCmRlZiBfbWF4X3RzKCp2YWx1ZXM6IGRhdGV0aW1lIHwgTm9uZSkgLT4gZGF0ZXRpbWUgfCBOb25lOgogICAgYXdhcmUgPSBbX2F3YXJlKHYpIGZvciB2IGluIHZhbHVlcyBpZiB2IGlzIG5vdCBOb25lXQogICAgcmV0dXJuIG1heChhd2FyZSkgaWYgYXdhcmUgZWxzZSBOb25lCgoKZGVmIGl0ZXJfa25vd25fcGVyaW9kcygpIC0+IGxpc3RbdHVwbGVbaW50LCBpbnRdXToKICAgICIiIlRvZG9zIGxvcyAoYcOxbywgbWVzKSBjb24gcHJlc2VuY2lhIGRlIGRhdG9zIFBHQyAvIGltcG9ydHMuIiIiCiAgICBwZXJpb2RzOiBzZXRbdHVwbGVbaW50LCBpbnRdXSA9IHNldCgpCgogICAgZm9yIHllYXIsIG1vbnRoIGluIE1vbnRobHlUYXJnZXQub2JqZWN0cy52YWx1ZXNfbGlzdCgieWVhciIsICJtb250aCIpLmRpc3RpbmN0KCk6CiAgICAgICAgcGVyaW9kcy5hZGQoKHllYXIsIG1vbnRoKSkKICAgIGZvciB5ZWFyLCBtb250aCBpbiBNb250aGx5TWV0cmljUmVzdWx0Lm9iamVjdHMudmFsdWVzX2xpc3QoInllYXIiLCAibW9udGgiKS5kaXN0aW5jdCgpOgogICAgICAgIHBlcmlvZHMuYWRkKCh5ZWFyLCBtb250aCkpCiAgICBmb3IgeWVhciwgbW9udGggaW4gTmV3Q2xpZW50SW1wb3J0Um93Lm9iamVjdHMudmFsdWVzX2xpc3QoInllYXIiLCAibW9udGgiKS5kaXN0aW5jdCgpOgogICAgICAgIHBlcmlvZHMuYWRkKCh5ZWFyLCBtb250aCkpCiAgICBmb3IgeWVhciwgbW9udGggaW4gQ3Jvc3NTYWxlSW1wb3J0Um93Lm9iamVjdHMudmFsdWVzX2xpc3QoInllYXIiLCAibW9udGgiKS5kaXN0aW5jdCgpOgogICAgICAgIHBlcmlvZHMuYWRkKCh5ZWFyLCBtb250aCkpCiAgICBmb3IgeWVhciwgbW9udGggaW4gTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZS5vYmplY3RzLnZhbHVlc19saXN0KAogICAgICAgICJ5ZWFyIiwgIm1vbnRoIgogICAgKS5kaXN0aW5jdCgpOgogICAgICAgIHBlcmlvZHMuYWRkKCh5ZWFyLCBtb250aCkpCiAgICBmb3IgeWVhciwgbW9udGggaW4gTW9udGhseU1vZGVTY29yZWNhcmQub2JqZWN0cy52YWx1ZXNfbGlzdCgieWVhciIsICJtb250aCIpLmRpc3RpbmN0KCk6CiAgICAgICAgcGVyaW9kcy5hZGQoKHllYXIsIG1vbnRoKSkKICAgIGZvciB5ZWFyLCBtb250aCBpbiAoCiAgICAgICAgRmlsZVVwbG9hZC5vYmplY3RzLmV4Y2x1ZGUoZGV0ZWN0ZWRfeWVhcl9faXNudWxsPVRydWUpCiAgICAgICAgLmV4Y2x1ZGUoZGV0ZWN0ZWRfbW9udGhfX2lzbnVsbD1UcnVlKQogICAgICAgIC52YWx1ZXNfbGlzdCgiZGV0ZWN0ZWRfeWVhciIsICJkZXRlY3RlZF9tb250aCIpCiAgICAgICAgLmRpc3RpbmN0KCkKICAgICk6CiAgICAgICAgcGVyaW9kcy5hZGQoKGludCh5ZWFyKSwgaW50KG1vbnRoKSkpCgogICAgIyBBw7FvcyBjb24gcGxhbjogYWwgbWVub3MgYXNlZ3VyYXIgbWVzZXMgZG9uZGUgaGF5YSBwbGFuLCBhdW5xdWUgdmFjw61vcwogICAgIyAobm8gbG9zIGFncmVnYW1vcyB2YWPDrW9zIOKAlCBzb2xvIGRhdG9zIHJlYWxlcykuCiAgICByZXR1cm4gc29ydGVkKHBlcmlvZHMpCgoKZGVmIF9pbnZlc3RtZW50X3VuZSgpIC0+IFVORSB8IE5vbmU6CiAgICByZXR1cm4gKAogICAgICAgIFVORS5vYmplY3RzLmZpbHRlcihjb2RlX19pbj1JTlZFU1RNRU5UX0NPREVTKQogICAgICAgIC5vcmRlcl9ieSgic29ydF9vcmRlciIsICJpZCIpCiAgICAgICAgLmZpcnN0KCkKICAgICkKCgpkZWYgX2luZ3Jlc29zX21ldHJpYygpIC0+IE1ldHJpY0RlZmluaXRpb24gfCBOb25lOgogICAgcmV0dXJuIE1ldHJpY0RlZmluaXRpb24ub2JqZWN0cy5maWx0ZXIoY29kZT1NZXRyaWNEZWZpbml0aW9uLkNPREVfSU5HUkVTT1MpLmZpcnN0KCkKCgpkZWYgX2RhdGFfdGltZXN0YW1wKHllYXI6IGludCwgbW9udGg6IGludCkgLT4gZGF0ZXRpbWUgfCBOb25lOgogICAgIiIiw5psdGltYSBtb2RpZmljYWNpw7NuIGRlIGluc3Vtb3MgcXVlIGFsaW1lbnRhbiBlbCBzY29yZS4iIiIKICAgIHN0YW1wczogbGlzdFtkYXRldGltZSB8IE5vbmVdID0gW10KICAgIGZvciBtb2RlbCBpbiAoCiAgICAgICAgTW9udGhseVRhcmdldCwKICAgICAgICBNb250aGx5TWV0cmljUmVzdWx0LAogICAgICAgIE5ld0NsaWVudEltcG9ydFJvdywKICAgICAgICBDcm9zc1NhbGVJbXBvcnRSb3csCiAgICAgICAgTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZSwKICAgICk6CiAgICAgICAgc3RhbXBzLmFwcGVuZCgKICAgICAgICAgICAgbW9kZWwub2JqZWN0cy5maWx0ZXIoeWVhcj15ZWFyLCBtb250aD1tb250aCkuYWdncmVnYXRlKG09TWF4KCJ1cGRhdGVkX2F0IikpWyJtIl0KICAgICAgICApCiAgICBzdGFtcHMuYXBwZW5kKAogICAgICAgIEZpbGVVcGxvYWQub2JqZWN0cy5maWx0ZXIoZGV0ZWN0ZWRfeWVhcj15ZWFyLCBkZXRlY3RlZF9tb250aD1tb250aCkuYWdncmVnYXRlKAogICAgICAgICAgICBtPU1heCgiY3JlYXRlZF9hdCIpCiAgICAgICAgKVsibSJdCiAgICApCiAgICByZXR1cm4gX21heF90cygqc3RhbXBzKQoKCmRlZiBfc2NvcmVfdGltZXN0YW1wKHBsYW46IFBHQ1BsYW4gfCBOb25lLCB5ZWFyOiBpbnQsIG1vbnRoOiBpbnQpIC0+IGRhdGV0aW1lIHwgTm9uZToKICAgIGlmIG5vdCBwbGFuOgogICAgICAgIHJldHVybiBOb25lCiAgICBzdGFtcHMgPSBbXQogICAgcXMgPSBNb250aGx5TW9kZVNjb3JlY2FyZC5vYmplY3RzLmZpbHRlcihwbGFuPXBsYW4sIHllYXI9eWVhciwgbW9udGg9bW9udGgpCiAgICBmb3IgbW9kZSBpbiBNT0RFUzoKICAgICAgICBzdGFtcHMuYXBwZW5kKHFzLmZpbHRlcihtb2RlPW1vZGUpLmFnZ3JlZ2F0ZShtPU1heCgidXBkYXRlZF9hdCIpKVsibSJdKQogICAgcmV0dXJuIF9tYXhfdHMoKnN0YW1wcykKCgpkZWYgX2hhc19zY29yZWFibGVfZGF0YSh5ZWFyOiBpbnQsIG1vbnRoOiBpbnQpIC0+IGJvb2w6CiAgICByZXR1cm4gKAogICAgICAgIE1vbnRobHlUYXJnZXQub2JqZWN0cy5maWx0ZXIoeWVhcj15ZWFyLCBtb250aD1tb250aCkuZXhpc3RzKCkKICAgICAgICBvciBNb250aGx5TWV0cmljUmVzdWx0Lm9iamVjdHMuZmlsdGVyKHllYXI9eWVhciwgbW9udGg9bW9udGgpLmV4aXN0cygpCiAgICAgICAgb3IgTmV3Q2xpZW50SW1wb3J0Um93Lm9iamVjdHMuZmlsdGVyKHllYXI9eWVhciwgbW9udGg9bW9udGgpLmV4aXN0cygpCiAgICAgICAgb3IgQ3Jvc3NTYWxlSW1wb3J0Um93Lm9iamVjdHMuZmlsdGVyKHllYXI9eWVhciwgbW9udGg9bW9udGgpLmV4aXN0cygpCiAgICAgICAgb3IgTWFudWFsUmVxdWlyZW1lbnRzQ29tcGxpYW5jZS5vYmplY3RzLmZpbHRlcih5ZWFyPXllYXIsIG1vbnRoPW1vbnRoKS5leGlzdHMoKQogICAgKQoKCmRlZiBfc2NvcmVfY29tcGxldGUocGxhbjogUEdDUGxhbiB8IE5vbmUsIHllYXI6IGludCwgbW9udGg6IGludCkgLT4gYm9vbDoKICAgIGlmIG5vdCBwbGFuOgogICAgICAgIHJldHVybiBGYWxzZQogICAgdW5lX2NvdW50ID0gVU5FLm9iamVjdHMuZmlsdGVyKGlzX2FjdGl2ZT1UcnVlKS5jb3VudCgpCiAgICBpZiB1bmVfY291bnQgPT0gMDoKICAgICAgICByZXR1cm4gRmFsc2UKICAgIGZvciBtb2RlIGluIE1PREVTOgogICAgICAgIG4gPSBNb250aGx5TW9kZVNjb3JlY2FyZC5vYmplY3RzLmZpbHRlcigKICAgICAgICAgICAgcGxhbj1wbGFuLCB5ZWFyPXllYXIsIG1vbnRoPW1vbnRoLCBtb2RlPW1vZGUKICAgICAgICApLmNvdW50KCkKICAgICAgICBpZiBuIDwgdW5lX2NvdW50OgogICAgICAgICAgICByZXR1cm4gRmFsc2UKICAgIHJldHVybiBUcnVlCgoKZGVmIHBlcmlvZF9wZW5kaW5nX3JlYXNvbnMoeWVhcjogaW50LCBtb250aDogaW50KSAtPiBsaXN0W3N0cl06CiAgICAiIiJSYXpvbmVzIHBvciBsYXMgcXVlIGVsIHBlcsOtb2RvIG5lY2VzaXRhIGxhIGNhZGVuYSBkZSByZWPDoWxjdWxvLiIiIgogICAgcmVhc29uczogbGlzdFtzdHJdID0gW10KICAgIHBsYW4gPSBQR0NQbGFuLm9iamVjdHMuZmlsdGVyKHllYXI9eWVhcikuZmlyc3QoKQogICAgbGFiZWwgPSBmInt5ZWFyfS17bW9udGg6MDJkfSIKCiAgICBzdGFsZSA9IGNvdW50X3N0YWxlX2luZ3Jlc29zKHllYXIsIG1vbnRoKQogICAgaWYgc3RhbGU6CiAgICAgICAgcmVhc29ucy5hcHBlbmQoZiJ7c3RhbGV9IGluZ3Jlc28ocykgY29uIFRDIGRlc2FjdHVhbGl6YWRvIChTVEFMRSkiKQoKICAgIGludl91bmUgPSBfaW52ZXN0bWVudF91bmUoKQogICAgbWV0cmljID0gX2luZ3Jlc29zX21ldHJpYygpCiAgICBpZiBpbnZfdW5lIGFuZCBOZXdDbGllbnRJbXBvcnRSb3cub2JqZWN0cy5maWx0ZXIoCiAgICAgICAgeWVhcj15ZWFyLCBtb250aD1tb250aCwgdW5lPWludl91bmUKICAgICkuZXhpc3RzKCk6CiAgICAgICAgbGF0ZXN0X3Jvd190cyA9IE5ld0NsaWVudEltcG9ydFJvdy5vYmplY3RzLmZpbHRlcigKICAgICAgICAgICAgeWVhcj15ZWFyLCBtb250aD1tb250aCwgdW5lPWludl91bmUKICAgICAgICApLmFnZ3JlZ2F0ZShtPU1heCgidXBkYXRlZF9hdCIpKVsibSJdCiAgICAgICAgcmVzdWx0ID0gTm9uZQogICAgICAgIGlmIHBsYW4gYW5kIG1ldHJpYzoKICAgICAgICAgICAgcmVzdWx0ID0gTW9udGhseU1ldHJpY1Jlc3VsdC5vYmplY3RzLmZpbHRlcigKICAgICAgICAgICAgICAgIHBsYW49cGxhbiwKICAgICAgICAgICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgICAgICAgICB1bmU9aW52X3VuZSwKICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICApLmZpcnN0KCkKICAgICAgICBpZiByZXN1bHQgaXMgTm9uZSBvciByZXN1bHQubWVhc3VyZWRfdmFsdWUgaXMgTm9uZToKICAgICAgICAgICAgcmVhc29ucy5hcHBlbmQoIkluZ3Jlc29zIEludmVzdG1lbnQgc2luIGNhbGN1bGFyIGRlc2RlIGNsaWVudGVzIikKICAgICAgICBlbGlmIGxhdGVzdF9yb3dfdHMgYW5kIHJlc3VsdC51cGRhdGVkX2F0IGFuZCBfYXdhcmUocmVzdWx0LnVwZGF0ZWRfYXQpIDwgX2F3YXJlKAogICAgICAgICAgICBsYXRlc3Rfcm93X3RzCiAgICAgICAgKToKICAgICAgICAgICAgcmVhc29ucy5hcHBlbmQoIkluZ3Jlc29zIEludmVzdG1lbnQgZGVzYWN0dWFsaXphZG9zIHZzIGNsaWVudGVzIikKCiAgICBpZiBfaGFzX3Njb3JlYWJsZV9kYXRhKHllYXIsIG1vbnRoKToKICAgICAgICBpZiBub3QgcGxhbjoKICAgICAgICAgICAgcmVhc29ucy5hcHBlbmQoZiJTaW4gcGxhbiBQR0MgcGFyYSB7eWVhcn0gKG5vIHNlIHB1ZWRlIHNjb3JlYXIpIikKICAgICAgICBlbGlmIG5vdCBfc2NvcmVfY29tcGxldGUocGxhbiwgeWVhciwgbW9udGgpOgogICAgICAgICAgICByZWFzb25zLmFwcGVuZCgiU2NvcmUgUEdDIGluY29tcGxldG8gKG1vZG8xL21vZG8yKSIpCiAgICAgICAgZWxzZToKICAgICAgICAgICAgZGF0YV90cyA9IF9kYXRhX3RpbWVzdGFtcCh5ZWFyLCBtb250aCkKICAgICAgICAgICAgc2NvcmVfdHMgPSBfc2NvcmVfdGltZXN0YW1wKHBsYW4sIHllYXIsIG1vbnRoKQogICAgICAgICAgICBpZiBkYXRhX3RzIGFuZCBzY29yZV90cyBhbmQgc2NvcmVfdHMgPCBkYXRhX3RzOgogICAgICAgICAgICAgICAgcmVhc29ucy5hcHBlbmQoIlNjb3JlIGRlc2FjdHVhbGl6YWRvIHJlc3BlY3RvIGEgbG9zIGRhdG9zIikKICAgICAgICAgICAgZWxpZiBkYXRhX3RzIGFuZCBub3Qgc2NvcmVfdHM6CiAgICAgICAgICAgICAgICByZWFzb25zLmFwcGVuZChmIlNpbiBzY29yZSBwYXJhIHtsYWJlbH0iKQoKICAgIHJldHVybiByZWFzb25zCgoKZGVmIGdldF9nbG9iYWxfcmVjYWxjX3N0YXR1cygpIC0+IGRpY3Rbc3RyLCBBbnldOgogICAgcGVuZGluZ19wZXJpb2RzOiBsaXN0W2RpY3Rbc3RyLCBBbnldXSA9IFtdCiAgICBmb3IgeWVhciwgbW9udGggaW4gaXRlcl9rbm93bl9wZXJpb2RzKCk6CiAgICAgICAgcmVhc29ucyA9IHBlcmlvZF9wZW5kaW5nX3JlYXNvbnMoeWVhciwgbW9udGgpCiAgICAgICAgaWYgcmVhc29uczoKICAgICAgICAgICAgcGVuZGluZ19wZXJpb2RzLmFwcGVuZCgKICAgICAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICAgICAieWVhciI6IHllYXIsCiAgICAgICAgICAgICAgICAgICAgIm1vbnRoIjogbW9udGgsCiAgICAgICAgICAgICAgICAgICAgImxhYmVsIjogZiJ7eWVhcn0te21vbnRoOjAyZH0iLAogICAgICAgICAgICAgICAgICAgICJyZWFzb25zIjogcmVhc29ucywKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgKQoKICAgIHBlbmRpbmdfY291bnQgPSBsZW4ocGVuZGluZ19wZXJpb2RzKQogICAgaXNfcGVuZGluZyA9IHBlbmRpbmdfY291bnQgPiAwCiAgICByZXR1cm4gewogICAgICAgICJpc19wZW5kaW5nIjogaXNfcGVuZGluZywKICAgICAgICAiaXNfcmVhZHkiOiBub3QgaXNfcGVuZGluZywKICAgICAgICAicGVuZGluZ19jb3VudCI6IHBlbmRpbmdfY291bnQsCiAgICAgICAgInBlbmRpbmdfcGVyaW9kcyI6IHBlbmRpbmdfcGVyaW9kcywKICAgICAgICAic3RhdGUiOiAicGVuZGluZyIgaWYgaXNfcGVuZGluZyBlbHNlICJyZWFkeSIsCiAgICAgICAgInN0YXRlX2xhYmVsIjogKAogICAgICAgICAgICBmIlBlbmRpZW50ZSDCtyB7cGVuZGluZ19jb3VudH0gcGVyw61vZG8ocykiCiAgICAgICAgICAgIGlmIGlzX3BlbmRpbmcKICAgICAgICAgICAgZWxzZSAiQWwgZMOtYSDCtyBzaW4gcGVuZGllbnRlcyIKICAgICAgICApLAogICAgICAgICJidXR0b25fbGFiZWwiOiAoCiAgICAgICAgICAgIGYi4pazIFJlY2FsY3VsYXIgcGVuZGllbnRlcyAoe3BlbmRpbmdfY291bnR9KSIKICAgICAgICAgICAgaWYgaXNfcGVuZGluZwogICAgICAgICAgICBlbHNlICLinJMgUmVjYWxjdWxhciAodG9kbyBhbCBkw61hKSIKICAgICAgICApLAogICAgICAgICJidXR0b25faGludCI6ICgKICAgICAgICAgICAgIkhheSBjw6FsY3Vsb3MgZmFsdGFudGVzIG8gZGVzYWN0dWFsaXphZG9zIGVuIHVubyBvIG3DoXMgcGVyw61vZG9zLiIKICAgICAgICAgICAgaWYgaXNfcGVuZGluZwogICAgICAgICAgICBlbHNlICJObyBoYXkgcGVuZGllbnRlcy4gUHVlZGUgZWplY3V0YXIgZGUgdG9kb3MgbW9kb3Mgc2kgcXVpZXJlIGZvcnphciByZXZpc2nDs24uIgogICAgICAgICksCiAgICB9CgoKZGVmIHJ1bl9wZXJpb2RfcmVjYWxjX2NoYWluKAogICAgeWVhcjogaW50LAogICAgbW9udGg6IGludCwKICAgICosCiAgICB1c2VyPU5vbmUsCiAgICBmb3JjZTogYm9vbCA9IEZhbHNlLAopIC0+IGxpc3Rbc3RyXToKICAgICIiIgogICAgT3JkZW4gZXN0cmljdG8gcG9yIHBlcsOtb2RvOgogICAgMSkgSW5ncmVzb3MgU1RBTEUgR1RR4oaSVVNECiAgICAyKSBJbmdyZXNvcyBJbnZlc3RtZW50IGRlc2RlIGNsaWVudGVzIG51ZXZvcwogICAgMykgU2NvcmUgUEdDIG1vZG8xICsgbW9kbzIKICAgICIiIgogICAgbWVzc2FnZXNfb3V0OiBsaXN0W3N0cl0gPSBbXQogICAgbGFiZWwgPSBmInt5ZWFyfS17bW9udGg6MDJkfSIKCiAgICB0cnk6CiAgICAgICAgc3RhbGVfcmVzdWx0ID0gcmVjYWxjX3N0YWxlX2luZ3Jlc29zKAogICAgICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgICAgICB1c2VyPXVzZXIsCiAgICAgICAgICAgIHJlYXNvbj1mIlJlY8OhbGN1bG8gaW50ZWxpZ2VudGUge2xhYmVsfSIsCiAgICAgICAgICAgIG9ubHlfc3RhbGU9VHJ1ZSwKICAgICAgICApCiAgICAgICAgaWYgc3RhbGVfcmVzdWx0WyJ1cGRhdGVkIl06CiAgICAgICAgICAgIG1lc3NhZ2VzX291dC5hcHBlbmQoCiAgICAgICAgICAgICAgICBmIntsYWJlbH06IHtzdGFsZV9yZXN1bHRbJ3VwZGF0ZWQnXX0gaW5ncmVzbyhzKSBTVEFMRSDihpIgVVNEICIKICAgICAgICAgICAgICAgIGYiKFRDPXtzdGFsZV9yZXN1bHRbJ2Z4J119KS4iCiAgICAgICAgICAgICkKICAgIGV4Y2VwdCBWYWx1ZUVycm9yIGFzIGV4YzoKICAgICAgICAjIFNpbiBUQzogbm8gYmxvcXVlYXIgZWwgcmVzdG87IGF2aXNhci4KICAgICAgICBpZiBjb3VudF9zdGFsZV9pbmdyZXNvcyh5ZWFyLCBtb250aCk6CiAgICAgICAgICAgIG1lc3NhZ2VzX291dC5hcHBlbmQoZiJ7bGFiZWx9OiBTVEFMRSBubyBjb252ZXJ0aWRvIOKAlCB7ZXhjfSIpCgogICAgaGFzX2NsaWVudHMgPSBOZXdDbGllbnRJbXBvcnRSb3cub2JqZWN0cy5maWx0ZXIoeWVhcj15ZWFyLCBtb250aD1tb250aCkuZXhpc3RzKCkKICAgIGlmIGhhc19jbGllbnRzIG9yIGZvcmNlOgogICAgICAgIGNhbGxfY29tbWFuZCgKICAgICAgICAgICAgInJlY2FsY19pbnZlc3RtZW50X2luZ3Jlc29zX2Zyb21fbmV3X2NsaWVudHMiLCB5ZWFyPXllYXIsIG1vbnRoPW1vbnRoCiAgICAgICAgKQogICAgICAgIG1lc3NhZ2VzX291dC5hcHBlbmQoZiJ7bGFiZWx9OiBpbmdyZXNvcyBJbnZlc3RtZW50IHJlY2FsY3VsYWRvcy4iKQoKICAgIGlmIF9oYXNfc2NvcmVhYmxlX2RhdGEoeWVhciwgbW9udGgpIG9yIGZvcmNlIG9yIGhhc19jbGllbnRzOgogICAgICAgIGZvciBtb2RlIGluIE1PREVTOgogICAgICAgICAgICBjYWxsX2NvbW1hbmQoInJlY2FsY19wZ2MiLCB5ZWFyPXllYXIsIG1vbnRoPW1vbnRoLCBtb2RlPW1vZGUpCiAgICAgICAgbWVzc2FnZXNfb3V0LmFwcGVuZChmIntsYWJlbH06IHNjb3JlIFBHQyAobW9kbzEgeSBtb2RvMikgcmVjYWxjdWxhZG8uIikKCiAgICBpZiBub3QgbWVzc2FnZXNfb3V0OgogICAgICAgIG1lc3NhZ2VzX291dC5hcHBlbmQoZiJ7bGFiZWx9OiBzaW4gb3BlcmFjaW9uZXMgYXBsaWNhYmxlcy4iKQogICAgcmV0dXJuIG1lc3NhZ2VzX291dAoKCmRlZiBydW5fc21hcnRfcmVjYWxjX2FsbCgqLCB1c2VyPU5vbmUsIGZvcmNlX2FsbDogYm9vbCA9IEZhbHNlKSAtPiBkaWN0W3N0ciwgQW55XToKICAgICIiIgogICAgU2kgaGF5IHBlbmRpZW50ZXM6IHJlY2FsY3VsYSBzb2xvIGVzb3MgcGVyw61vZG9zIChlbiBvcmRlbiBjcm9ub2zDs2dpY28pLgogICAgU2kgbm8gaGF5IHBlbmRpZW50ZXMgeSBmb3JjZV9hbGw9RmFsc2U6IG5vLW9wIGluZm9ybWF0aXZvLgogICAgU2kgZm9yY2VfYWxsPVRydWU6IGNvcnJlIGxhIGNhZGVuYSBlbiB0b2RvcyBsb3MgcGVyw61vZG9zIGNvbm9jaWRvcy4KICAgICIiIgogICAgc3RhdHVzX2JlZm9yZSA9IGdldF9nbG9iYWxfcmVjYWxjX3N0YXR1cygpCiAgICBpZiBmb3JjZV9hbGw6CiAgICAgICAgdGFyZ2V0cyA9IFsKICAgICAgICAgICAgeyJ5ZWFyIjogeSwgIm1vbnRoIjogbSwgImxhYmVsIjogZiJ7eX0te206MDJkfSIsICJyZWFzb25zIjogWyJmb3J6YWRvIl19CiAgICAgICAgICAgIGZvciB5LCBtIGluIGl0ZXJfa25vd25fcGVyaW9kcygpCiAgICAgICAgXQogICAgZWxzZToKICAgICAgICB0YXJnZXRzID0gbGlzdChzdGF0dXNfYmVmb3JlWyJwZW5kaW5nX3BlcmlvZHMiXSkKCiAgICBpZiBub3QgdGFyZ2V0czoKICAgICAgICByZXR1cm4gewogICAgICAgICAgICAicmFuIjogRmFsc2UsCiAgICAgICAgICAgICJwZXJpb2RzX3Byb2Nlc3NlZCI6IDAsCiAgICAgICAgICAgICJtZXNzYWdlcyI6IFsiTmFkYSBwZW5kaWVudGUgZGUgY2FsY3VsYXIuIFRvZG8gYWwgZMOtYS4iXSwKICAgICAgICAgICAgInN0YXR1c19iZWZvcmUiOiBzdGF0dXNfYmVmb3JlLAogICAgICAgICAgICAic3RhdHVzX2FmdGVyIjogc3RhdHVzX2JlZm9yZSwKICAgICAgICB9CgogICAgbWVzc2FnZXM6IGxpc3Rbc3RyXSA9IFtdCiAgICBmb3IgaXRlbSBpbiB0YXJnZXRzOgogICAgICAgIHllYXIsIG1vbnRoID0gaXRlbVsieWVhciJdLCBpdGVtWyJtb250aCJdCiAgICAgICAgdHJ5OgogICAgICAgICAgICBtZXNzYWdlcy5leHRlbmQoCiAgICAgICAgICAgICAgICBydW5fcGVyaW9kX3JlY2FsY19jaGFpbih5ZWFyLCBtb250aCwgdXNlcj11c2VyLCBmb3JjZT1mb3JjZV9hbGwpCiAgICAgICAgICAgICkKICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGV4YzogICMga2VlcCBnb2luZyBhY3Jvc3MgcGVyaW9kcwogICAgICAgICAgICBtZXNzYWdlcy5hcHBlbmQoZiJ7aXRlbVsnbGFiZWwnXX06IGVycm9yIOKAlCB7ZXhjfSIpCgogICAgc3RhdHVzX2FmdGVyID0gZ2V0X2dsb2JhbF9yZWNhbGNfc3RhdHVzKCkKICAgIHJldHVybiB7CiAgICAgICAgInJhbiI6IFRydWUsCiAgICAgICAgInBlcmlvZHNfcHJvY2Vzc2VkIjogbGVuKHRhcmdldHMpLAogICAgICAgICJtZXNzYWdlcyI6IG1lc3NhZ2VzLAogICAgICAgICJzdGF0dXNfYmVmb3JlIjogc3RhdHVzX2JlZm9yZSwKICAgICAgICAic3RhdHVzX2FmdGVyIjogc3RhdHVzX2FmdGVyLAogICAgfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/admin_utils.py
PATH_JSON="pgc/admin_utils.py"
FILENAME=admin_utils.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=278
SIZE_BYTES_UTF8=8090
CONTENT_SHA256=02bacbe8904806d2d376f0a4d1181457d5a2f4ded495df605cc632b10ee7248c
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
"""Utilidades compartidas del área de Administración."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from urllib.parse import urlencode

from django.db.models import Q, QuerySet
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone


@dataclass(frozen=True)
class AdminPeriod:
    """Período admin: rango de meses en un mismo año.

    Las pantallas de un solo mes usan ``month`` (= fin del rango).
    Las de datos/browse usan ``month_from``..``month_to``.
    """

    year: int
    month_from: int
    month_to: int

    @property
    def month(self) -> int:
        """Mes operativo (último del rango) para pantallas de un solo mes."""
        return self.month_to

    @property
    def is_range(self) -> bool:
        return self.month_from != self.month_to

    def months(self) -> list[int]:
        return list(range(self.month_from, self.month_to + 1))

    @property
    def label(self) -> str:
        if self.is_range:
            return f"{self.year}-{self.month_from:02d} → {self.year}-{self.month_to:02d}"
        return f"{self.year}-{self.month_to:02d}"

    @property
    def focus_label(self) -> str:
        return f"{self.year}-{self.month_to:02d}"

    def query_dict(self, **extra) -> dict:
        data = {
            "year": str(self.year),
            "month": str(self.month_to),
            "month_from": str(self.month_from),
            "month_to": str(self.month_to),
        }
        for key, value in extra.items():
            if value is None or value == "":
                continue
            data[key] = str(value)
        return data

    def querystring(self, **extra) -> str:
        return urlencode(self.query_dict(**extra))


def _clamp_month(value: int) -> int:
    return max(1, min(12, value))


def default_admin_period(now=None) -> AdminPeriod:
    """Rango maestro por defecto: año actual, mes 01 → mes anterior al actual.

    En enero (no hay mes anterior en el mismo año) queda 01→01.
    """
    now = now or timezone.now()
    year = now.year
    if now.month <= 1:
        return AdminPeriod(year=year, month_from=1, month_to=1)
    return AdminPeriod(year=year, month_from=1, month_to=now.month - 1)


def parse_admin_period(
    request,
    default_year: int | None = None,
    default_month: int | None = None,
) -> AdminPeriod:
    defaults = default_admin_period()
    if default_year is None:
        default_year = defaults.year
    if default_month is None:
        default_month = defaults.month_to

    get = request.GET
    post = request.POST

    def _raw(*keys: str) -> str | None:
        for key in keys:
            value = get.get(key) or post.get(key)
            if value not in (None, ""):
                return value
        return None

    year_raw = _raw("year")
    # month / month_to = fin del rango (compat + pantallas single-month)
    month_to_raw = _raw("month_to", "month")
    month_from_raw = _raw("month_from")

    # Sin parámetros de período → año actual, 01 hasta el mes anterior al actual.
    if year_raw is None and month_to_raw is None and month_from_raw is None:
        return AdminPeriod(
            year=default_year,
            month_from=1,
            month_to=_clamp_month(default_month),
        )

    year_raw = year_raw or str(default_year)
    month_to_raw = month_to_raw or str(default_month)
    # Si viene mes fin pero no "desde", interpretar como un solo mes (compat).
    month_from_raw = month_from_raw or month_to_raw

    try:
        year = int(year_raw)
        month_to = _clamp_month(int(month_to_raw))
        month_from = _clamp_month(int(month_from_raw))
    except (TypeError, ValueError):
        return AdminPeriod(
            year=default_year,
            month_from=1,
            month_to=_clamp_month(default_month),
        )

    if month_from > month_to:
        month_from, month_to = month_to, month_from

    return AdminPeriod(year=year, month_from=month_from, month_to=month_to)


def parse_period(
    request,
    default_year: int | None = None,
    default_month: int | None = None,
) -> tuple[int, int]:
    """Compat: (year, month_to). Preferir parse_admin_period."""
    period = parse_admin_period(request, default_year=default_year, default_month=default_month)
    return period.year, period.month


def period_filter(period: AdminPeriod, year_field: str = "year", month_field: str = "month") -> Q:
    return Q(**{year_field: period.year}) & Q(
        **{f"{month_field}__gte": period.month_from, f"{month_field}__lte": period.month_to}
    )


def apply_period_range(
    qs: QuerySet,
    period: AdminPeriod,
    *,
    year_field: str = "year",
    month_field: str = "month",
) -> QuerySet:
    return qs.filter(period_filter(period, year_field=year_field, month_field=month_field))


def admin_period_context(period: AdminPeriod) -> dict:
    from pgc.admin_recalc import get_global_recalc_status

    return {
        "period": period,
        "year": period.year,
        "month": period.month,
        "month_from": period.month_from,
        "month_to": period.month_to,
        "period_label": period.label,
        "period_focus_label": period.focus_label,
        "period_is_range": period.is_range,
        "period_qs": period.querystring(),
        "month_choices": list(range(1, 13)),
        "year_choices": list(range(2024, 2031)),
        "recalc_status": get_global_recalc_status(),
    }


def redirect_admin_monthly(
    year: int | AdminPeriod | None = None,
    month: int | None = None,
    block: str | None = None,
    *,
    period: AdminPeriod | None = None,
) -> redirect:
    p = _as_period(year, month, period)
    url = f"{reverse('pgc:admin_monthly')}?{p.querystring(block=block)}"
    return redirect(url)


def redirect_admin_manual(
    year: int | AdminPeriod | None = None,
    month: int | None = None,
    tab: str | None = None,
    *,
    period: AdminPeriod | None = None,
) -> redirect:
    p = _as_period(year, month, period)
    url = f"{reverse('pgc:admin_manual_edit')}?{p.querystring(tab=tab)}"
    return redirect(url)


def redirect_admin_new_clients_browse(
    year: int | AdminPeriod | None = None,
    month: int | None = None,
    *,
    period: AdminPeriod | None = None,
) -> redirect:
    p = _as_period(year, month, period)
    return redirect(f"{reverse('pgc:admin_new_clients_browse')}?{p.querystring()}")


def redirect_admin_new_clients_une(
    year: int | AdminPeriod | None = None,
    month: int | None = None,
    *,
    period: AdminPeriod | None = None,
) -> redirect:
    p = _as_period(year, month, period)
    return redirect(f"{reverse('pgc:admin_new_clients_une')}?{p.querystring()}")


def redirect_admin_ingresos_year(
    year: int | AdminPeriod | None = None,
    month: int | None = None,
    *,
    period: AdminPeriod | None = None,
    curr: str | None = None,
) -> redirect:
    p = _as_period(year, month, period)
    qs = p.querystring()
    if curr:
        qs = f"{qs}&curr={curr}"
    return redirect(f"{reverse('pgc:admin_ingresos_year')}?{qs}")


def _as_period(
    year: int | AdminPeriod | None,
    month: int | None,
    period: AdminPeriod | None,
) -> AdminPeriod:
    if isinstance(year, AdminPeriod):
        return year
    if period is not None:
        return period
    if year is None or month is None:
        raise TypeError("Debe indicar AdminPeriod o year/month")
    return AdminPeriod(year=year, month_from=month, month_to=month)


def parse_decimal_or_none(raw_value) -> Decimal | None:
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


def format_value(value) -> str:
    if value is None:
        return ""
    return str(value)

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Utilidades compartidas del área de Administración."""
00002|
00003|from __future__ import annotations
00004|
00005|from dataclasses import dataclass
00006|from decimal import Decimal, InvalidOperation
00007|from urllib.parse import urlencode
00008|
00009|from django.db.models import Q, QuerySet
00010|from django.shortcuts import redirect
00011|from django.urls import reverse
00012|from django.utils import timezone
00013|
00014|
00015|@dataclass(frozen=True)
00016|class AdminPeriod:
00017|    """Período admin: rango de meses en un mismo año.
00018|
00019|    Las pantallas de un solo mes usan ``month`` (= fin del rango).
00020|    Las de datos/browse usan ``month_from``..``month_to``.
00021|    """
00022|
00023|    year: int
00024|    month_from: int
00025|    month_to: int
00026|
00027|    @property
00028|    def month(self) -> int:
00029|        """Mes operativo (último del rango) para pantallas de un solo mes."""
00030|        return self.month_to
00031|
00032|    @property
00033|    def is_range(self) -> bool:
00034|        return self.month_from != self.month_to
00035|
00036|    def months(self) -> list[int]:
00037|        return list(range(self.month_from, self.month_to + 1))
00038|
00039|    @property
00040|    def label(self) -> str:
00041|        if self.is_range:
00042|            return f"{self.year}-{self.month_from:02d} → {self.year}-{self.month_to:02d}"
00043|        return f"{self.year}-{self.month_to:02d}"
00044|
00045|    @property
00046|    def focus_label(self) -> str:
00047|        return f"{self.year}-{self.month_to:02d}"
00048|
00049|    def query_dict(self, **extra) -> dict:
00050|        data = {
00051|            "year": str(self.year),
00052|            "month": str(self.month_to),
00053|            "month_from": str(self.month_from),
00054|            "month_to": str(self.month_to),
00055|        }
00056|        for key, value in extra.items():
00057|            if value is None or value == "":
00058|                continue
00059|            data[key] = str(value)
00060|        return data
00061|
00062|    def querystring(self, **extra) -> str:
00063|        return urlencode(self.query_dict(**extra))
00064|
00065|
00066|def _clamp_month(value: int) -> int:
00067|    return max(1, min(12, value))
00068|
00069|
00070|def default_admin_period(now=None) -> AdminPeriod:
00071|    """Rango maestro por defecto: año actual, mes 01 → mes anterior al actual.
00072|
00073|    En enero (no hay mes anterior en el mismo año) queda 01→01.
00074|    """
00075|    now = now or timezone.now()
00076|    year = now.year
00077|    if now.month <= 1:
00078|        return AdminPeriod(year=year, month_from=1, month_to=1)
00079|    return AdminPeriod(year=year, month_from=1, month_to=now.month - 1)
00080|
00081|
00082|def parse_admin_period(
00083|    request,
00084|    default_year: int | None = None,
00085|    default_month: int | None = None,
00086|) -> AdminPeriod:
00087|    defaults = default_admin_period()
00088|    if default_year is None:
00089|        default_year = defaults.year
00090|    if default_month is None:
00091|        default_month = defaults.month_to
00092|
00093|    get = request.GET
00094|    post = request.POST
00095|
00096|    def _raw(*keys: str) -> str | None:
00097|        for key in keys:
00098|            value = get.get(key) or post.get(key)
00099|            if value not in (None, ""):
00100|                return value
00101|        return None
00102|
00103|    year_raw = _raw("year")
00104|    # month / month_to = fin del rango (compat + pantallas single-month)
00105|    month_to_raw = _raw("month_to", "month")
00106|    month_from_raw = _raw("month_from")
00107|
00108|    # Sin parámetros de período → año actual, 01 hasta el mes anterior al actual.
00109|    if year_raw is None and month_to_raw is None and month_from_raw is None:
00110|        return AdminPeriod(
00111|            year=default_year,
00112|            month_from=1,
00113|            month_to=_clamp_month(default_month),
00114|        )
00115|
00116|    year_raw = year_raw or str(default_year)
00117|    month_to_raw = month_to_raw or str(default_month)
00118|    # Si viene mes fin pero no "desde", interpretar como un solo mes (compat).
00119|    month_from_raw = month_from_raw or month_to_raw
00120|
00121|    try:
00122|        year = int(year_raw)
00123|        month_to = _clamp_month(int(month_to_raw))
00124|        month_from = _clamp_month(int(month_from_raw))
00125|    except (TypeError, ValueError):
00126|        return AdminPeriod(
00127|            year=default_year,
00128|            month_from=1,
00129|            month_to=_clamp_month(default_month),
00130|        )
00131|
00132|    if month_from > month_to:
00133|        month_from, month_to = month_to, month_from
00134|
00135|    return AdminPeriod(year=year, month_from=month_from, month_to=month_to)
00136|
00137|
00138|def parse_period(
00139|    request,
00140|    default_year: int | None = None,
00141|    default_month: int | None = None,
00142|) -> tuple[int, int]:
00143|    """Compat: (year, month_to). Preferir parse_admin_period."""
00144|    period = parse_admin_period(request, default_year=default_year, default_month=default_month)
00145|    return period.year, period.month
00146|
00147|
00148|def period_filter(period: AdminPeriod, year_field: str = "year", month_field: str = "month") -> Q:
00149|    return Q(**{year_field: period.year}) & Q(
00150|        **{f"{month_field}__gte": period.month_from, f"{month_field}__lte": period.month_to}
00151|    )
00152|
00153|
00154|def apply_period_range(
00155|    qs: QuerySet,
00156|    period: AdminPeriod,
00157|    *,
00158|    year_field: str = "year",
00159|    month_field: str = "month",
00160|) -> QuerySet:
00161|    return qs.filter(period_filter(period, year_field=year_field, month_field=month_field))
00162|
00163|
00164|def admin_period_context(period: AdminPeriod) -> dict:
00165|    from pgc.admin_recalc import get_global_recalc_status
00166|
00167|    return {
00168|        "period": period,
00169|        "year": period.year,
00170|        "month": period.month,
00171|        "month_from": period.month_from,
00172|        "month_to": period.month_to,
00173|        "period_label": period.label,
00174|        "period_focus_label": period.focus_label,
00175|        "period_is_range": period.is_range,
00176|        "period_qs": period.querystring(),
00177|        "month_choices": list(range(1, 13)),
00178|        "year_choices": list(range(2024, 2031)),
00179|        "recalc_status": get_global_recalc_status(),
00180|    }
00181|
00182|
00183|def redirect_admin_monthly(
00184|    year: int | AdminPeriod | None = None,
00185|    month: int | None = None,
00186|    block: str | None = None,
00187|    *,
00188|    period: AdminPeriod | None = None,
00189|) -> redirect:
00190|    p = _as_period(year, month, period)
00191|    url = f"{reverse('pgc:admin_monthly')}?{p.querystring(block=block)}"
00192|    return redirect(url)
00193|
00194|
00195|def redirect_admin_manual(
00196|    year: int | AdminPeriod | None = None,
00197|    month: int | None = None,
00198|    tab: str | None = None,
00199|    *,
00200|    period: AdminPeriod | None = None,
00201|) -> redirect:
00202|    p = _as_period(year, month, period)
00203|    url = f"{reverse('pgc:admin_manual_edit')}?{p.querystring(tab=tab)}"
00204|    return redirect(url)
00205|
00206|
00207|def redirect_admin_new_clients_browse(
00208|    year: int | AdminPeriod | None = None,
00209|    month: int | None = None,
00210|    *,
00211|    period: AdminPeriod | None = None,
00212|) -> redirect:
00213|    p = _as_period(year, month, period)
00214|    return redirect(f"{reverse('pgc:admin_new_clients_browse')}?{p.querystring()}")
00215|
00216|
00217|def redirect_admin_new_clients_une(
00218|    year: int | AdminPeriod | None = None,
00219|    month: int | None = None,
00220|    *,
00221|    period: AdminPeriod | None = None,
00222|) -> redirect:
00223|    p = _as_period(year, month, period)
00224|    return redirect(f"{reverse('pgc:admin_new_clients_une')}?{p.querystring()}")
00225|
00226|
00227|def redirect_admin_ingresos_year(
00228|    year: int | AdminPeriod | None = None,
00229|    month: int | None = None,
00230|    *,
00231|    period: AdminPeriod | None = None,
00232|    curr: str | None = None,
00233|) -> redirect:
00234|    p = _as_period(year, month, period)
00235|    qs = p.querystring()
00236|    if curr:
00237|        qs = f"{qs}&curr={curr}"
00238|    return redirect(f"{reverse('pgc:admin_ingresos_year')}?{qs}")
00239|
00240|
00241|def _as_period(
00242|    year: int | AdminPeriod | None,
00243|    month: int | None,
00244|    period: AdminPeriod | None,
00245|) -> AdminPeriod:
00246|    if isinstance(year, AdminPeriod):
00247|        return year
00248|    if period is not None:
00249|        return period
00250|    if year is None or month is None:
00251|        raise TypeError("Debe indicar AdminPeriod o year/month")
00252|    return AdminPeriod(year=year, month_from=month, month_to=month)
00253|
00254|
00255|def parse_decimal_or_none(raw_value) -> Decimal | None:
00256|    if raw_value is None:
00257|        return None
00258|
00259|    text = str(raw_value).strip()
00260|    if text == "":
00261|        return None
00262|
00263|    text = text.replace(" ", "")
00264|    if "," in text and "." in text:
00265|        text = text.replace(",", "")
00266|    elif "," in text:
00267|        text = text.replace(",", ".")
00268|
00269|    try:
00270|        return Decimal(text)
00271|    except (InvalidOperation, ValueError):
00272|        return None
00273|
00274|
00275|def format_value(value) -> str:
00276|    if value is None:
00277|        return ""
00278|    return str(value)

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiVXRpbGlkYWRlcyBjb21wYXJ0aWRhcyBkZWwgw6FyZWEgZGUgQWRtaW5pc3RyYWNpw7NuLiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKZnJvbSBkYXRhY2xhc3NlcyBpbXBvcnQgZGF0YWNsYXNzCmZyb20gZGVjaW1hbCBpbXBvcnQgRGVjaW1hbCwgSW52YWxpZE9wZXJhdGlvbgpmcm9tIHVybGxpYi5wYXJzZSBpbXBvcnQgdXJsZW5jb2RlCgpmcm9tIGRqYW5nby5kYi5tb2RlbHMgaW1wb3J0IFEsIFF1ZXJ5U2V0CmZyb20gZGphbmdvLnNob3J0Y3V0cyBpbXBvcnQgcmVkaXJlY3QKZnJvbSBkamFuZ28udXJscyBpbXBvcnQgcmV2ZXJzZQpmcm9tIGRqYW5nby51dGlscyBpbXBvcnQgdGltZXpvbmUKCgpAZGF0YWNsYXNzKGZyb3plbj1UcnVlKQpjbGFzcyBBZG1pblBlcmlvZDoKICAgICIiIlBlcsOtb2RvIGFkbWluOiByYW5nbyBkZSBtZXNlcyBlbiB1biBtaXNtbyBhw7FvLgoKICAgIExhcyBwYW50YWxsYXMgZGUgdW4gc29sbyBtZXMgdXNhbiBgYG1vbnRoYGAgKD0gZmluIGRlbCByYW5nbykuCiAgICBMYXMgZGUgZGF0b3MvYnJvd3NlIHVzYW4gYGBtb250aF9mcm9tYGAuLmBgbW9udGhfdG9gYC4KICAgICIiIgoKICAgIHllYXI6IGludAogICAgbW9udGhfZnJvbTogaW50CiAgICBtb250aF90bzogaW50CgogICAgQHByb3BlcnR5CiAgICBkZWYgbW9udGgoc2VsZikgLT4gaW50OgogICAgICAgICIiIk1lcyBvcGVyYXRpdm8gKMO6bHRpbW8gZGVsIHJhbmdvKSBwYXJhIHBhbnRhbGxhcyBkZSB1biBzb2xvIG1lcy4iIiIKICAgICAgICByZXR1cm4gc2VsZi5tb250aF90bwoKICAgIEBwcm9wZXJ0eQogICAgZGVmIGlzX3JhbmdlKHNlbGYpIC0+IGJvb2w6CiAgICAgICAgcmV0dXJuIHNlbGYubW9udGhfZnJvbSAhPSBzZWxmLm1vbnRoX3RvCgogICAgZGVmIG1vbnRocyhzZWxmKSAtPiBsaXN0W2ludF06CiAgICAgICAgcmV0dXJuIGxpc3QocmFuZ2Uoc2VsZi5tb250aF9mcm9tLCBzZWxmLm1vbnRoX3RvICsgMSkpCgogICAgQHByb3BlcnR5CiAgICBkZWYgbGFiZWwoc2VsZikgLT4gc3RyOgogICAgICAgIGlmIHNlbGYuaXNfcmFuZ2U6CiAgICAgICAgICAgIHJldHVybiBmIntzZWxmLnllYXJ9LXtzZWxmLm1vbnRoX2Zyb206MDJkfSDihpIge3NlbGYueWVhcn0te3NlbGYubW9udGhfdG86MDJkfSIKICAgICAgICByZXR1cm4gZiJ7c2VsZi55ZWFyfS17c2VsZi5tb250aF90bzowMmR9IgoKICAgIEBwcm9wZXJ0eQogICAgZGVmIGZvY3VzX2xhYmVsKHNlbGYpIC0+IHN0cjoKICAgICAgICByZXR1cm4gZiJ7c2VsZi55ZWFyfS17c2VsZi5tb250aF90bzowMmR9IgoKICAgIGRlZiBxdWVyeV9kaWN0KHNlbGYsICoqZXh0cmEpIC0+IGRpY3Q6CiAgICAgICAgZGF0YSA9IHsKICAgICAgICAgICAgInllYXIiOiBzdHIoc2VsZi55ZWFyKSwKICAgICAgICAgICAgIm1vbnRoIjogc3RyKHNlbGYubW9udGhfdG8pLAogICAgICAgICAgICAibW9udGhfZnJvbSI6IHN0cihzZWxmLm1vbnRoX2Zyb20pLAogICAgICAgICAgICAibW9udGhfdG8iOiBzdHIoc2VsZi5tb250aF90byksCiAgICAgICAgfQogICAgICAgIGZvciBrZXksIHZhbHVlIGluIGV4dHJhLml0ZW1zKCk6CiAgICAgICAgICAgIGlmIHZhbHVlIGlzIE5vbmUgb3IgdmFsdWUgPT0gIiI6CiAgICAgICAgICAgICAgICBjb250aW51ZQogICAgICAgICAgICBkYXRhW2tleV0gPSBzdHIodmFsdWUpCiAgICAgICAgcmV0dXJuIGRhdGEKCiAgICBkZWYgcXVlcnlzdHJpbmcoc2VsZiwgKipleHRyYSkgLT4gc3RyOgogICAgICAgIHJldHVybiB1cmxlbmNvZGUoc2VsZi5xdWVyeV9kaWN0KCoqZXh0cmEpKQoKCmRlZiBfY2xhbXBfbW9udGgodmFsdWU6IGludCkgLT4gaW50OgogICAgcmV0dXJuIG1heCgxLCBtaW4oMTIsIHZhbHVlKSkKCgpkZWYgZGVmYXVsdF9hZG1pbl9wZXJpb2Qobm93PU5vbmUpIC0+IEFkbWluUGVyaW9kOgogICAgIiIiUmFuZ28gbWFlc3RybyBwb3IgZGVmZWN0bzogYcOxbyBhY3R1YWwsIG1lcyAwMSDihpIgbWVzIGFudGVyaW9yIGFsIGFjdHVhbC4KCiAgICBFbiBlbmVybyAobm8gaGF5IG1lcyBhbnRlcmlvciBlbiBlbCBtaXNtbyBhw7FvKSBxdWVkYSAwMeKGkjAxLgogICAgIiIiCiAgICBub3cgPSBub3cgb3IgdGltZXpvbmUubm93KCkKICAgIHllYXIgPSBub3cueWVhcgogICAgaWYgbm93Lm1vbnRoIDw9IDE6CiAgICAgICAgcmV0dXJuIEFkbWluUGVyaW9kKHllYXI9eWVhciwgbW9udGhfZnJvbT0xLCBtb250aF90bz0xKQogICAgcmV0dXJuIEFkbWluUGVyaW9kKHllYXI9eWVhciwgbW9udGhfZnJvbT0xLCBtb250aF90bz1ub3cubW9udGggLSAxKQoKCmRlZiBwYXJzZV9hZG1pbl9wZXJpb2QoCiAgICByZXF1ZXN0LAogICAgZGVmYXVsdF95ZWFyOiBpbnQgfCBOb25lID0gTm9uZSwKICAgIGRlZmF1bHRfbW9udGg6IGludCB8IE5vbmUgPSBOb25lLAopIC0+IEFkbWluUGVyaW9kOgogICAgZGVmYXVsdHMgPSBkZWZhdWx0X2FkbWluX3BlcmlvZCgpCiAgICBpZiBkZWZhdWx0X3llYXIgaXMgTm9uZToKICAgICAgICBkZWZhdWx0X3llYXIgPSBkZWZhdWx0cy55ZWFyCiAgICBpZiBkZWZhdWx0X21vbnRoIGlzIE5vbmU6CiAgICAgICAgZGVmYXVsdF9tb250aCA9IGRlZmF1bHRzLm1vbnRoX3RvCgogICAgZ2V0ID0gcmVxdWVzdC5HRVQKICAgIHBvc3QgPSByZXF1ZXN0LlBPU1QKCiAgICBkZWYgX3Jhdygqa2V5czogc3RyKSAtPiBzdHIgfCBOb25lOgogICAgICAgIGZvciBrZXkgaW4ga2V5czoKICAgICAgICAgICAgdmFsdWUgPSBnZXQuZ2V0KGtleSkgb3IgcG9zdC5nZXQoa2V5KQogICAgICAgICAgICBpZiB2YWx1ZSBub3QgaW4gKE5vbmUsICIiKToKICAgICAgICAgICAgICAgIHJldHVybiB2YWx1ZQogICAgICAgIHJldHVybiBOb25lCgogICAgeWVhcl9yYXcgPSBfcmF3KCJ5ZWFyIikKICAgICMgbW9udGggLyBtb250aF90byA9IGZpbiBkZWwgcmFuZ28gKGNvbXBhdCArIHBhbnRhbGxhcyBzaW5nbGUtbW9udGgpCiAgICBtb250aF90b19yYXcgPSBfcmF3KCJtb250aF90byIsICJtb250aCIpCiAgICBtb250aF9mcm9tX3JhdyA9IF9yYXcoIm1vbnRoX2Zyb20iKQoKICAgICMgU2luIHBhcsOhbWV0cm9zIGRlIHBlcsOtb2RvIOKGkiBhw7FvIGFjdHVhbCwgMDEgaGFzdGEgZWwgbWVzIGFudGVyaW9yIGFsIGFjdHVhbC4KICAgIGlmIHllYXJfcmF3IGlzIE5vbmUgYW5kIG1vbnRoX3RvX3JhdyBpcyBOb25lIGFuZCBtb250aF9mcm9tX3JhdyBpcyBOb25lOgogICAgICAgIHJldHVybiBBZG1pblBlcmlvZCgKICAgICAgICAgICAgeWVhcj1kZWZhdWx0X3llYXIsCiAgICAgICAgICAgIG1vbnRoX2Zyb209MSwKICAgICAgICAgICAgbW9udGhfdG89X2NsYW1wX21vbnRoKGRlZmF1bHRfbW9udGgpLAogICAgICAgICkKCiAgICB5ZWFyX3JhdyA9IHllYXJfcmF3IG9yIHN0cihkZWZhdWx0X3llYXIpCiAgICBtb250aF90b19yYXcgPSBtb250aF90b19yYXcgb3Igc3RyKGRlZmF1bHRfbW9udGgpCiAgICAjIFNpIHZpZW5lIG1lcyBmaW4gcGVybyBubyAiZGVzZGUiLCBpbnRlcnByZXRhciBjb21vIHVuIHNvbG8gbWVzIChjb21wYXQpLgogICAgbW9udGhfZnJvbV9yYXcgPSBtb250aF9mcm9tX3JhdyBvciBtb250aF90b19yYXcKCiAgICB0cnk6CiAgICAgICAgeWVhciA9IGludCh5ZWFyX3JhdykKICAgICAgICBtb250aF90byA9IF9jbGFtcF9tb250aChpbnQobW9udGhfdG9fcmF3KSkKICAgICAgICBtb250aF9mcm9tID0gX2NsYW1wX21vbnRoKGludChtb250aF9mcm9tX3JhdykpCiAgICBleGNlcHQgKFR5cGVFcnJvciwgVmFsdWVFcnJvcik6CiAgICAgICAgcmV0dXJuIEFkbWluUGVyaW9kKAogICAgICAgICAgICB5ZWFyPWRlZmF1bHRfeWVhciwKICAgICAgICAgICAgbW9udGhfZnJvbT0xLAogICAgICAgICAgICBtb250aF90bz1fY2xhbXBfbW9udGgoZGVmYXVsdF9tb250aCksCiAgICAgICAgKQoKICAgIGlmIG1vbnRoX2Zyb20gPiBtb250aF90bzoKICAgICAgICBtb250aF9mcm9tLCBtb250aF90byA9IG1vbnRoX3RvLCBtb250aF9mcm9tCgogICAgcmV0dXJuIEFkbWluUGVyaW9kKHllYXI9eWVhciwgbW9udGhfZnJvbT1tb250aF9mcm9tLCBtb250aF90bz1tb250aF90bykKCgpkZWYgcGFyc2VfcGVyaW9kKAogICAgcmVxdWVzdCwKICAgIGRlZmF1bHRfeWVhcjogaW50IHwgTm9uZSA9IE5vbmUsCiAgICBkZWZhdWx0X21vbnRoOiBpbnQgfCBOb25lID0gTm9uZSwKKSAtPiB0dXBsZVtpbnQsIGludF06CiAgICAiIiJDb21wYXQ6ICh5ZWFyLCBtb250aF90bykuIFByZWZlcmlyIHBhcnNlX2FkbWluX3BlcmlvZC4iIiIKICAgIHBlcmlvZCA9IHBhcnNlX2FkbWluX3BlcmlvZChyZXF1ZXN0LCBkZWZhdWx0X3llYXI9ZGVmYXVsdF95ZWFyLCBkZWZhdWx0X21vbnRoPWRlZmF1bHRfbW9udGgpCiAgICByZXR1cm4gcGVyaW9kLnllYXIsIHBlcmlvZC5tb250aAoKCmRlZiBwZXJpb2RfZmlsdGVyKHBlcmlvZDogQWRtaW5QZXJpb2QsIHllYXJfZmllbGQ6IHN0ciA9ICJ5ZWFyIiwgbW9udGhfZmllbGQ6IHN0ciA9ICJtb250aCIpIC0+IFE6CiAgICByZXR1cm4gUSgqKnt5ZWFyX2ZpZWxkOiBwZXJpb2QueWVhcn0pICYgUSgKICAgICAgICAqKntmInttb250aF9maWVsZH1fX2d0ZSI6IHBlcmlvZC5tb250aF9mcm9tLCBmInttb250aF9maWVsZH1fX2x0ZSI6IHBlcmlvZC5tb250aF90b30KICAgICkKCgpkZWYgYXBwbHlfcGVyaW9kX3JhbmdlKAogICAgcXM6IFF1ZXJ5U2V0LAogICAgcGVyaW9kOiBBZG1pblBlcmlvZCwKICAgICosCiAgICB5ZWFyX2ZpZWxkOiBzdHIgPSAieWVhciIsCiAgICBtb250aF9maWVsZDogc3RyID0gIm1vbnRoIiwKKSAtPiBRdWVyeVNldDoKICAgIHJldHVybiBxcy5maWx0ZXIocGVyaW9kX2ZpbHRlcihwZXJpb2QsIHllYXJfZmllbGQ9eWVhcl9maWVsZCwgbW9udGhfZmllbGQ9bW9udGhfZmllbGQpKQoKCmRlZiBhZG1pbl9wZXJpb2RfY29udGV4dChwZXJpb2Q6IEFkbWluUGVyaW9kKSAtPiBkaWN0OgogICAgZnJvbSBwZ2MuYWRtaW5fcmVjYWxjIGltcG9ydCBnZXRfZ2xvYmFsX3JlY2FsY19zdGF0dXMKCiAgICByZXR1cm4gewogICAgICAgICJwZXJpb2QiOiBwZXJpb2QsCiAgICAgICAgInllYXIiOiBwZXJpb2QueWVhciwKICAgICAgICAibW9udGgiOiBwZXJpb2QubW9udGgsCiAgICAgICAgIm1vbnRoX2Zyb20iOiBwZXJpb2QubW9udGhfZnJvbSwKICAgICAgICAibW9udGhfdG8iOiBwZXJpb2QubW9udGhfdG8sCiAgICAgICAgInBlcmlvZF9sYWJlbCI6IHBlcmlvZC5sYWJlbCwKICAgICAgICAicGVyaW9kX2ZvY3VzX2xhYmVsIjogcGVyaW9kLmZvY3VzX2xhYmVsLAogICAgICAgICJwZXJpb2RfaXNfcmFuZ2UiOiBwZXJpb2QuaXNfcmFuZ2UsCiAgICAgICAgInBlcmlvZF9xcyI6IHBlcmlvZC5xdWVyeXN0cmluZygpLAogICAgICAgICJtb250aF9jaG9pY2VzIjogbGlzdChyYW5nZSgxLCAxMykpLAogICAgICAgICJ5ZWFyX2Nob2ljZXMiOiBsaXN0KHJhbmdlKDIwMjQsIDIwMzEpKSwKICAgICAgICAicmVjYWxjX3N0YXR1cyI6IGdldF9nbG9iYWxfcmVjYWxjX3N0YXR1cygpLAogICAgfQoKCmRlZiByZWRpcmVjdF9hZG1pbl9tb250aGx5KAogICAgeWVhcjogaW50IHwgQWRtaW5QZXJpb2QgfCBOb25lID0gTm9uZSwKICAgIG1vbnRoOiBpbnQgfCBOb25lID0gTm9uZSwKICAgIGJsb2NrOiBzdHIgfCBOb25lID0gTm9uZSwKICAgICosCiAgICBwZXJpb2Q6IEFkbWluUGVyaW9kIHwgTm9uZSA9IE5vbmUsCikgLT4gcmVkaXJlY3Q6CiAgICBwID0gX2FzX3BlcmlvZCh5ZWFyLCBtb250aCwgcGVyaW9kKQogICAgdXJsID0gZiJ7cmV2ZXJzZSgncGdjOmFkbWluX21vbnRobHknKX0/e3AucXVlcnlzdHJpbmcoYmxvY2s9YmxvY2spfSIKICAgIHJldHVybiByZWRpcmVjdCh1cmwpCgoKZGVmIHJlZGlyZWN0X2FkbWluX21hbnVhbCgKICAgIHllYXI6IGludCB8IEFkbWluUGVyaW9kIHwgTm9uZSA9IE5vbmUsCiAgICBtb250aDogaW50IHwgTm9uZSA9IE5vbmUsCiAgICB0YWI6IHN0ciB8IE5vbmUgPSBOb25lLAogICAgKiwKICAgIHBlcmlvZDogQWRtaW5QZXJpb2QgfCBOb25lID0gTm9uZSwKKSAtPiByZWRpcmVjdDoKICAgIHAgPSBfYXNfcGVyaW9kKHllYXIsIG1vbnRoLCBwZXJpb2QpCiAgICB1cmwgPSBmIntyZXZlcnNlKCdwZ2M6YWRtaW5fbWFudWFsX2VkaXQnKX0/e3AucXVlcnlzdHJpbmcodGFiPXRhYil9IgogICAgcmV0dXJuIHJlZGlyZWN0KHVybCkKCgpkZWYgcmVkaXJlY3RfYWRtaW5fbmV3X2NsaWVudHNfYnJvd3NlKAogICAgeWVhcjogaW50IHwgQWRtaW5QZXJpb2QgfCBOb25lID0gTm9uZSwKICAgIG1vbnRoOiBpbnQgfCBOb25lID0gTm9uZSwKICAgICosCiAgICBwZXJpb2Q6IEFkbWluUGVyaW9kIHwgTm9uZSA9IE5vbmUsCikgLT4gcmVkaXJlY3Q6CiAgICBwID0gX2FzX3BlcmlvZCh5ZWFyLCBtb250aCwgcGVyaW9kKQogICAgcmV0dXJuIHJlZGlyZWN0KGYie3JldmVyc2UoJ3BnYzphZG1pbl9uZXdfY2xpZW50c19icm93c2UnKX0/e3AucXVlcnlzdHJpbmcoKX0iKQoKCmRlZiByZWRpcmVjdF9hZG1pbl9uZXdfY2xpZW50c191bmUoCiAgICB5ZWFyOiBpbnQgfCBBZG1pblBlcmlvZCB8IE5vbmUgPSBOb25lLAogICAgbW9udGg6IGludCB8IE5vbmUgPSBOb25lLAogICAgKiwKICAgIHBlcmlvZDogQWRtaW5QZXJpb2QgfCBOb25lID0gTm9uZSwKKSAtPiByZWRpcmVjdDoKICAgIHAgPSBfYXNfcGVyaW9kKHllYXIsIG1vbnRoLCBwZXJpb2QpCiAgICByZXR1cm4gcmVkaXJlY3QoZiJ7cmV2ZXJzZSgncGdjOmFkbWluX25ld19jbGllbnRzX3VuZScpfT97cC5xdWVyeXN0cmluZygpfSIpCgoKZGVmIHJlZGlyZWN0X2FkbWluX2luZ3Jlc29zX3llYXIoCiAgICB5ZWFyOiBpbnQgfCBBZG1pblBlcmlvZCB8IE5vbmUgPSBOb25lLAogICAgbW9udGg6IGludCB8IE5vbmUgPSBOb25lLAogICAgKiwKICAgIHBlcmlvZDogQWRtaW5QZXJpb2QgfCBOb25lID0gTm9uZSwKICAgIGN1cnI6IHN0ciB8IE5vbmUgPSBOb25lLAopIC0+IHJlZGlyZWN0OgogICAgcCA9IF9hc19wZXJpb2QoeWVhciwgbW9udGgsIHBlcmlvZCkKICAgIHFzID0gcC5xdWVyeXN0cmluZygpCiAgICBpZiBjdXJyOgogICAgICAgIHFzID0gZiJ7cXN9JmN1cnI9e2N1cnJ9IgogICAgcmV0dXJuIHJlZGlyZWN0KGYie3JldmVyc2UoJ3BnYzphZG1pbl9pbmdyZXNvc195ZWFyJyl9P3txc30iKQoKCmRlZiBfYXNfcGVyaW9kKAogICAgeWVhcjogaW50IHwgQWRtaW5QZXJpb2QgfCBOb25lLAogICAgbW9udGg6IGludCB8IE5vbmUsCiAgICBwZXJpb2Q6IEFkbWluUGVyaW9kIHwgTm9uZSwKKSAtPiBBZG1pblBlcmlvZDoKICAgIGlmIGlzaW5zdGFuY2UoeWVhciwgQWRtaW5QZXJpb2QpOgogICAgICAgIHJldHVybiB5ZWFyCiAgICBpZiBwZXJpb2QgaXMgbm90IE5vbmU6CiAgICAgICAgcmV0dXJuIHBlcmlvZAogICAgaWYgeWVhciBpcyBOb25lIG9yIG1vbnRoIGlzIE5vbmU6CiAgICAgICAgcmFpc2UgVHlwZUVycm9yKCJEZWJlIGluZGljYXIgQWRtaW5QZXJpb2QgbyB5ZWFyL21vbnRoIikKICAgIHJldHVybiBBZG1pblBlcmlvZCh5ZWFyPXllYXIsIG1vbnRoX2Zyb209bW9udGgsIG1vbnRoX3RvPW1vbnRoKQoKCmRlZiBwYXJzZV9kZWNpbWFsX29yX25vbmUocmF3X3ZhbHVlKSAtPiBEZWNpbWFsIHwgTm9uZToKICAgIGlmIHJhd192YWx1ZSBpcyBOb25lOgogICAgICAgIHJldHVybiBOb25lCgogICAgdGV4dCA9IHN0cihyYXdfdmFsdWUpLnN0cmlwKCkKICAgIGlmIHRleHQgPT0gIiI6CiAgICAgICAgcmV0dXJuIE5vbmUKCiAgICB0ZXh0ID0gdGV4dC5yZXBsYWNlKCIgIiwgIiIpCiAgICBpZiAiLCIgaW4gdGV4dCBhbmQgIi4iIGluIHRleHQ6CiAgICAgICAgdGV4dCA9IHRleHQucmVwbGFjZSgiLCIsICIiKQogICAgZWxpZiAiLCIgaW4gdGV4dDoKICAgICAgICB0ZXh0ID0gdGV4dC5yZXBsYWNlKCIsIiwgIi4iKQoKICAgIHRyeToKICAgICAgICByZXR1cm4gRGVjaW1hbCh0ZXh0KQogICAgZXhjZXB0IChJbnZhbGlkT3BlcmF0aW9uLCBWYWx1ZUVycm9yKToKICAgICAgICByZXR1cm4gTm9uZQoKCmRlZiBmb3JtYXRfdmFsdWUodmFsdWUpIC0+IHN0cjoKICAgIGlmIHZhbHVlIGlzIE5vbmU6CiAgICAgICAgcmV0dXJuICIiCiAgICByZXR1cm4gc3RyKHZhbHVlKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/admin_views.py
PATH_JSON="pgc/admin_views.py"
FILENAME=admin_views.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=690
SIZE_BYTES_UTF8=27809
CONTENT_SHA256=a91a574e88c59bd3e937816b3082ccb2cba8845bbf33b2f911093f2a3c3d79b1
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
Vistas del área de Administración rediseñada.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.management import call_command
from django.shortcuts import redirect, render
from django.urls import reverse

logger = logging.getLogger("pgc.admin_ingresos")

from imports.forms import FileUploadForm
from imports.models import FileUpload, guess_file_type_and_period

from .admin_manual import (
    get_manual_edit_context,
    save_alias,
    save_aliases_bulk,
    save_fx,
    save_import_rows,
    save_period_note,
    save_requirements,
    save_results,
    save_targets,
)
from .income_conversion import recalc_stale_ingresos
from .admin_period import (
    BLOCK_CROSS_SALE,
    BLOCK_FINANCIAL,
    BLOCK_META,
    BLOCK_NEW_CLIENTS,
    BLOCK_ORDER,
    BLOCK_REVIEW,
    discard_pending_upload,
    get_admin_period_snapshot,
    list_period_log,
    recalculate_block,
    recalculate_period,
    remove_duplicate_new_client_rows,
)
from .admin_new_clients_browse import (
    browse_context,
    save_browse_rows,
    save_une_reassignments,
)
from .admin_ingresos_year import get_ingresos_year_context, save_ingresos_year
from .admin_recalc import run_smart_recalc_all
from .admin_utils import (
    admin_period_context,
    parse_admin_period,
    parse_period,
    redirect_admin_ingresos_year,
    redirect_admin_manual,
    redirect_admin_monthly,
    redirect_admin_new_clients_browse,
    redirect_admin_new_clients_une,
)


def _save_upload(request, year: int, month: int, expected_type: str | None = None) -> FileUpload | None:
    uploaded = request.FILES.get("stored_file")
    if not uploaded:
        messages.error(request, "Debe seleccionar un archivo.")
        return None

    hasher = hashlib.sha256()
    for chunk in uploaded.chunks():
        hasher.update(chunk)
    uploaded_sha256 = hasher.hexdigest()
    uploaded.seek(0)

    original_filename = uploaded.name
    file_type, detected_year, detected_month = guess_file_type_and_period(original_filename)

    if expected_type and file_type != expected_type:
        messages.warning(
            request,
            f"El archivo parece ser de tipo distinto al bloque ({file_type} vs {expected_type}).",
        )

    if detected_year and detected_month and (detected_year != year or detected_month != month):
        messages.warning(
            request,
            f"El archivo sugiere período {detected_year}-{detected_month:02d}, "
            f"pero trabaja en {year}-{month:02d}.",
        )

    obj = FileUpload(
        uploaded_by=request.user,
        stored_file=uploaded,
        original_filename=original_filename,
        mime_type=getattr(uploaded, "content_type", "") or "",
        sha256=uploaded_sha256,
        detected_year=detected_year or year,
        detected_month=detected_month or month,
        file_type_detected=file_type if file_type != FileUpload.TYPE_UNKNOWN else (expected_type or file_type),
    )
    obj.save()
    messages.success(request, f"Archivo recibido: {obj.original_filename}.")
    return obj


def _process_upload(request, upload: FileUpload, year: int, month: int, block: str) -> None:
    path = Path(upload.stored_file.path)
    if not path.exists():
        messages.error(request, "El archivo físico no existe en el servidor.")
        return

    try:
        if block == BLOCK_NEW_CLIENTS:
            if upload.status == FileUpload.STATUS_PARSED_OK:
                messages.warning(
                    request,
                    "Este archivo ya fue procesado. Para evitar duplicados no se importó de nuevo. "
                    "Si necesita reprocesar, suba el archivo otra vez.",
                )
                return
            call_command(
                "import_clientes_nuevos",
                path=str(path),
                file_upload_id=upload.id,
            )
            upload.status = FileUpload.STATUS_PARSED_OK
            upload.save(update_fields=["status"])
            messages.success(request, "Clientes nuevos procesados correctamente.")
        elif block == BLOCK_CROSS_SALE:
            if upload.status == FileUpload.STATUS_PARSED_OK:
                messages.warning(
                    request,
                    "Este archivo ya fue procesado. Para evitar duplicados no se importó de nuevo. "
                    "Si necesita reprocesar, suba el archivo otra vez.",
                )
                return
            call_command("import_venta_cruzada", path=str(path))
            upload.status = FileUpload.STATUS_PARSED_OK
            upload.save(update_fields=["status"])
            messages.success(request, "Venta cruzada procesada correctamente.")
        elif block == BLOCK_FINANCIAL:
            call_command("import_ingresos", path=str(path), year=year, month=month)
            upload.status = FileUpload.STATUS_PARSED_OK
            upload.save(update_fields=["status"])
            messages.success(request, "Estado de resultados importado correctamente.")
        else:
            messages.error(request, "Este bloque no admite procesamiento de archivo.")
    except Exception as exc:
        upload.status = FileUpload.STATUS_PARSED_ERROR
        upload.error_summary = str(exc)[:500]
        upload.save(update_fields=["status", "error_summary"])
        messages.error(request, f"Error al procesar: {exc}")


def _admin_period_context(year: int, month: int) -> dict:
    # Compat legacy; prefer admin_period_context(period).
    from .admin_utils import AdminPeriod

    return admin_period_context(AdminPeriod(year=year, month_from=month, month_to=month))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_smart_recalc(request):
    """Botón único: recalcula en orden todo lo pendiente (todos los períodos)."""
    period = parse_admin_period(request)
    next_url = (request.POST.get("next") or "").strip()

    if request.method != "POST":
        return redirect_admin_monthly(period=period)

    try:
        result = run_smart_recalc_all(user=request.user, force_all=False)
        if not result["ran"]:
            messages.info(request, result["messages"][0] if result["messages"] else "Nada pendiente.")
        else:
            messages.success(
                request,
                f"Recálculo inteligente: {result['periods_processed']} período(s) procesado(s).",
            )
            for msg in result["messages"][:40]:
                messages.success(request, msg)
            if len(result["messages"]) > 40:
                messages.info(
                    request,
                    f"… y {len(result['messages']) - 40} mensaje(s) más.",
                )
            after = result["status_after"]
            if after["is_pending"]:
                messages.warning(
                    request,
                    f"Aún quedan {after['pending_count']} período(s) con pendientes "
                    "(p.ej. falta tipo de cambio para convertir STALE).",
                )
            else:
                messages.success(request, "Estado global: al día (verde).")
    except Exception as exc:
        messages.error(request, f"Error en recálculo inteligente: {exc}")

    if next_url.startswith("/"):
        return redirect(next_url)
    return redirect_admin_monthly(period=period)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_hub(request):
    """Punto de entrada legado: redirige al tablero mensual."""
    period = parse_admin_period(request)
    return redirect(f"{reverse('pgc:admin_monthly')}?{period.querystring()}")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_monthly(request):
    period = parse_admin_period(request)
    year, month = period.year, period.month
    selected_block = (request.GET.get("block") or request.POST.get("block") or BLOCK_ORDER[0]).strip()

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()

        if action == "recalculate_period":
            try:
                for msg in recalculate_period(year, month):
                    messages.success(request, msg)
            except Exception as exc:
                messages.error(request, f"Error al recalcular período: {exc}")
            return redirect_admin_monthly(period=period, block=selected_block)

        if action == "recalculate_block":
            block = request.POST.get("block") or selected_block
            try:
                for msg in recalculate_block(year, month, block):
                    messages.success(request, msg)
            except Exception as exc:
                messages.error(request, f"Error al recalcular bloque: {exc}")
            return redirect_admin_monthly(period=period, block=block)

        if action == "upload":
            block = request.POST.get("block") or selected_block
            type_map = {
                BLOCK_FINANCIAL: FileUpload.TYPE_FINANCIAL,
                BLOCK_NEW_CLIENTS: FileUpload.TYPE_NEW_CLIENTS,
                BLOCK_CROSS_SALE: FileUpload.TYPE_CROSS_SALE,
            }
            _save_upload(request, year, month, type_map.get(block))
            return redirect_admin_monthly(period=period, block=block)

        if action == "process":
            block = request.POST.get("block") or selected_block
            try:
                file_id = int(request.POST.get("file_id") or "0")
            except (TypeError, ValueError):
                file_id = 0
            upload = FileUpload.objects.filter(id=file_id).first()
            if not upload:
                messages.error(request, "Archivo no encontrado.")
            else:
                _process_upload(request, upload, year, month, block)
            return redirect_admin_monthly(period=period, block=block)

        if action == "discard_pending":
            block = request.POST.get("block") or selected_block
            try:
                file_id = int(request.POST.get("file_id") or "0")
            except (TypeError, ValueError):
                file_id = 0
            upload = FileUpload.objects.filter(id=file_id).first()
            if not upload:
                messages.error(request, "Archivo no encontrado.")
            else:
                try:
                    result = discard_pending_upload(upload)
                    messages.success(
                        request,
                        f"Se quitó de la cola: {result['filename']}. "
                        "Los datos ya procesados no se modificaron.",
                    )
                except ValueError as exc:
                    messages.error(request, str(exc))
                except Exception as exc:
                    messages.error(request, f"No se pudo quitar el archivo de la cola: {exc}")
            return redirect_admin_monthly(period=period, block=block)

        if action == "dedup_new_clients":
            try:
                result = remove_duplicate_new_client_rows(year, month, user=request.user)
                if result["removed"]:
                    messages.success(
                        request,
                        f"Se eliminaron {result['removed']} registro(s) duplicado(s) "
                        f"y se actualizaron {result['metrics_updated']} métrica(s) de clientes nuevos.",
                    )
                else:
                    messages.info(request, "No se encontraron duplicados en el detalle de clientes.")
            except Exception as exc:
                messages.error(request, f"Error al eliminar duplicados: {exc}")
            return redirect_admin_monthly(period=period, block=BLOCK_NEW_CLIENTS)

    snapshot = get_admin_period_snapshot(year, month)
    if selected_block not in snapshot["blocks_by_id"]:
        selected_block = BLOCK_ORDER[0]

    context = {
        **admin_period_context(period),
        "snapshot": snapshot,
        "selected_block": selected_block,
        "block_detail": snapshot["blocks_by_id"][selected_block],
        "block_order": BLOCK_ORDER,
        "block_meta": BLOCK_META,
        "upload_form": FileUploadForm(),
        "recent_log": list_period_log(year, month, limit=8, month_from=period.month_from),
        "supports_month_range": False,
        "single_month_ops": True,
    }
    return render(request, "pgc/admin_monthly.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_manual_edit(request):
    period = parse_admin_period(request)
    year, month = period.year, period.month
    tab = (request.GET.get("tab") or request.POST.get("tab") or "targets").strip()

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()
        reason = (request.POST.get("reason") or "").strip()
        recalc_after = request.POST.get("recalc_after") == "1"

        try:
            changes = 0
            if action == "save_targets":
                changes = save_targets(request.user, year, month, request.POST, reason)
            elif action == "save_results":
                changes = save_results(request.user, year, month, request.POST, reason)
            elif action == "recalc_stale_ingresos":
                result = recalc_stale_ingresos(
                    year=year,
                    month=month,
                    user=request.user,
                    reason=reason or "Recálculo de ingresos STALE desde admin",
                )
                changes = result["updated"]
                if changes:
                    messages.success(
                        request,
                        f"Se recalcularon {changes} ingreso(s) con TC={result['fx']}.",
                    )
                    if recalc_after:
                        try:
                            for msg in recalculate_period(year, month):
                                messages.success(request, msg)
                        except Exception as exc:
                            messages.warning(
                                request,
                                f"Recálculo de ingresos listo, pero falló el score: {exc}",
                            )
                    return redirect_admin_manual(period=period, tab=tab)
                messages.info(request, "No hay ingresos STALE para recalcular.")
                return redirect_admin_manual(period=period, tab=tab)
            elif action == "save_requirements":
                changes = save_requirements(request.user, year, month, request.POST, reason)
            elif action == "save_fx":
                changes = save_fx(
                    request.user,
                    year,
                    month,
                    request.POST,
                    reason,
                    month_from=period.month_from,
                )
            elif action == "save_alias":
                changes = save_alias(request.user, year, month, request.POST, reason)
            elif action == "save_aliases_bulk":
                changes = save_aliases_bulk(request.user, year, month, request.POST, reason)
            elif action == "save_imports":
                changes = save_import_rows(
                    request.user,
                    year,
                    month,
                    request.POST,
                    reason,
                    month_from=period.month_from,
                )
            elif action == "save_notes":
                changes = save_period_note(request.user, year, month, request.POST, reason)
            else:
                messages.error(request, "Acción no reconocida.")
                return redirect_admin_manual(period=period, tab=tab)

            if changes:
                messages.success(request, f"Se guardaron {changes} cambio(s).")
                if recalc_after:
                    try:
                        for msg in recalculate_period(year, month):
                            messages.success(request, msg)
                    except Exception as exc:
                        messages.warning(request, f"Cambios guardados, pero falló el recálculo: {exc}")
            else:
                messages.info(request, "No hubo cambios que guardar.")
        except ValueError as exc:
            messages.error(request, str(exc))
        except Exception as exc:
            messages.error(request, f"Error al guardar: {exc}")

        return redirect_admin_manual(period=period, tab=tab)

    context = {
        **admin_period_context(period),
        **get_manual_edit_context(year, month, tab, month_from=period.month_from),
    }
    return render(request, "pgc/admin_manual_edit.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_ingresos_year(request):
    """Matriz anual: 12 meses × 4 UNEs + TC (captura de ingresos reales)."""
    period = parse_admin_period(request)
    year = period.year
    capture_currency = (request.GET.get("curr") or request.POST.get("capture_currency") or "GTQ").strip()

    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()
        reason = (request.POST.get("reason") or "").strip()
        recalc_after = request.POST.get("recalc_after") == "1"
        capture_currency = (request.POST.get("capture_currency") or capture_currency).strip()

        if action == "save_ingresos_year":
            ing_keys = sorted(k for k in request.POST if k.startswith("ing_"))
            fx_keys = sorted(k for k in request.POST if k.startswith("fx_"))
            logger.warning(
                "ingresos_year POST year=%s curr=%s reason_len=%s "
                "ing_nonempty=%s fx_nonempty=%s ing_sample=%s fx_sample=%s",
                year,
                capture_currency,
                len(reason),
                sum(1 for k in ing_keys if (request.POST.get(k) or "").strip()),
                sum(1 for k in fx_keys if (request.POST.get(k) or "").strip()),
                [(k, request.POST.get(k)) for k in ing_keys if (request.POST.get(k) or "").strip()][:8],
                [(k, request.POST.get(k)) for k in fx_keys if (request.POST.get(k) or "").strip()][:8],
            )
            try:
                result = save_ingresos_year(request.user, year, request.POST, reason)
                income_n = result["income_changes"]
                fx_n = result["fx_changes"]
                logger.warning(
                    "ingresos_year result year=%s income_changes=%s fx_changes=%s currency=%s",
                    year,
                    income_n,
                    fx_n,
                    result["currency"],
                )
                if income_n:
                    messages.success(
                        request,
                        f"Guardado: {income_n} ingreso(s), {fx_n} TC; "
                        f"moneda captura={result['currency']}.",
                    )
                    if recalc_after:
                        # Recalcula score del mes foco del selector (no los 12).
                        try:
                            for msg in recalculate_period(year, period.month):
                                messages.success(request, msg)
                        except Exception as exc:
                            messages.warning(
                                request,
                                f"Ingresos guardados, pero falló el score de "
                                f"{year}-{period.month:02d}: {exc}",
                            )
                elif fx_n:
                    messages.warning(
                        request,
                        f"Solo se guardaron {fx_n} tipo(s) de cambio. "
                        "No llegó ningún valor de ingreso en el POST "
                        "(celdas vacías o no enviadas). Complete ingresos y vuelva a Guardar.",
                    )
                else:
                    messages.warning(
                        request,
                        "Sin cambios: no se recibieron ingresos ni tipos de cambio "
                        "con valor nuevo. Revise el formulario y el motivo, luego reintente.",
                    )
            except Exception as exc:
                logger.warning("ingresos_year save failed year=%s err=%s", year, exc)
                messages.error(request, str(exc))
            return redirect_admin_ingresos_year(
                period=period, curr=capture_currency
            )

    context = {
        **admin_period_context(period),
        **get_ingresos_year_context(year, capture_currency=capture_currency),
        "supports_month_range": False,
        "single_month_ops": False,
    }
    return render(request, "pgc/admin_ingresos_year.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_monthly_log(request):
    period = parse_admin_period(request)
    year, month = period.year, period.month
    entries = list_period_log(year, month, limit=150, month_from=period.month_from)
    snapshot = get_admin_period_snapshot(year, month)

    context = {
        **admin_period_context(period),
        "period_label": period.label,
        "entries": entries,
        "snapshot": snapshot,
        "supports_month_range": True,
        "single_month_ops": False,
    }
    return render(request, "pgc/admin_monthly_log.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_new_clients_browse(request):
    period = parse_admin_period(request)

    if request.method == "POST":
        reason = (request.POST.get("reason") or "").strip()
        recalc_after = request.POST.get("recalc_after") == "1"
        try:
            result = save_browse_rows(request.user, period, request.POST, reason)
            if result["total"]:
                parts = []
                if result["updated"]:
                    parts.append(f"{result['updated']} editado(s)")
                if result["deleted"]:
                    parts.append(f"{result['deleted']} eliminado(s)")
                if result["created"]:
                    parts.append(f"{result['created']} creado(s)")
                messages.success(
                    request,
                    f"Guardado: {', '.join(parts)}. "
                    f"Métricas actualizadas: {result['metrics_updated']}.",
                )
                if recalc_after:
                    try:
                        for msg in recalculate_block(
                            period.year, period.month, BLOCK_NEW_CLIENTS
                        ):
                            messages.success(request, msg)
                    except Exception as exc:
                        messages.warning(
                            request,
                            f"Cambios guardados, pero falló el recálculo: {exc}",
                        )
            else:
                messages.info(request, "No hubo cambios que guardar.")
        except ValueError as exc:
            messages.error(request, str(exc))
        except Exception as exc:
            messages.error(request, f"Error al guardar: {exc}")
        return redirect_admin_new_clients_browse(period=period)

    context = {
        **admin_period_context(period),
        **browse_context(period),
        "adm_nav_active": "clients_browse",
    }
    return render(request, "pgc/admin_new_clients_browse.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_new_clients_une(request):
    period = parse_admin_period(request)

    if request.method == "POST":
        reason = (request.POST.get("reason") or "").strip()
        recalc_after = request.POST.get("recalc_after") == "1"
        try:
            result = save_une_reassignments(
                request.user, period, request.POST, reason
            )
            if result["changed"]:
                messages.success(
                    request,
                    f"Se reasignaron {result['changed']} registro(s). "
                    f"Métricas actualizadas: {result['metrics_updated']}.",
                )
                if recalc_after:
                    try:
                        for msg in recalculate_block(
                            period.year, period.month, BLOCK_NEW_CLIENTS
                        ):
                            messages.success(request, msg)
                    except Exception as exc:
                        messages.warning(
                            request,
                            f"Cambios guardados, pero falló el recálculo: {exc}",
                        )
            else:
                messages.info(request, "No hubo cambios de UNE.")
        except ValueError as exc:
            messages.error(request, str(exc))
        except Exception as exc:
            messages.error(request, f"Error al guardar: {exc}")
        return redirect_admin_new_clients_une(period=period)

    context = {
        **admin_period_context(period),
        **browse_context(period),
        "adm_nav_active": "clients_une",
    }
    return render(request, "pgc/admin_new_clients_une.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def legacy_run_recalc_pgc(request):
    """Compatibilidad con URLs/formularios antiguos de recálculo."""
    year, month = parse_period(request)
    if request.method != "POST":
        messages.error(request, "Método no permitido.")
        return redirect_admin_monthly(year, month, BLOCK_REVIEW)

    year_raw = (request.POST.get("year") or "").strip()
    month_raw = (request.POST.get("month") or "").strip()
    try:
        year = int(year_raw)
        month = int(month_raw)
        if month < 1 or month > 12:
            raise ValueError
    except (TypeError, ValueError):
        messages.error(request, "Debes indicar año y mes válidos.")
        return redirect_admin_monthly(year, month, BLOCK_REVIEW)

    try:
        for msg in recalculate_period(year, month):
            messages.success(request, msg)
    except Exception as exc:
        messages.error(request, f"Error al ejecutar recalc PGC: {exc}")

    return redirect_admin_monthly(year, month, BLOCK_REVIEW)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def legacy_run_recalc_investment(request):
    """Compatibilidad con URLs/formularios antiguos de recálculo Investment."""
    year, month = parse_period(request)
    if request.method != "POST":
        messages.error(request, "Método no permitido.")
        return redirect_admin_monthly(year, month, BLOCK_NEW_CLIENTS)

    year_raw = (request.POST.get("year") or "").strip()
    month_raw = (request.POST.get("month") or "").strip()
    try:
        year = int(year_raw)
        month = int(month_raw)
        if month < 1 or month > 12:
            raise ValueError
    except (TypeError, ValueError):
        messages.error(request, "Debes indicar año y mes válidos.")
        return redirect_admin_monthly(year, month, BLOCK_NEW_CLIENTS)

    try:
        for msg in recalculate_block(year, month, BLOCK_NEW_CLIENTS):
            messages.success(request, msg)
    except Exception as exc:
        messages.error(request, f"Error al ejecutar recalc Investment: {exc}")

    return redirect_admin_monthly(year, month, BLOCK_NEW_CLIENTS)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def redirect_manual_results(request):
    """Legacy URL: /admin-hub/ingresos-manual-capture → matriz anual de ingresos."""
    period = parse_admin_period(request)
    return redirect_admin_ingresos_year(period=period)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def redirect_manual_fx(request):
    year, month = parse_period(request)
    return redirect_admin_manual(year, month, "fx")

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""
00002|Vistas del área de Administración rediseñada.
00003|"""
00004|
00005|from __future__ import annotations
00006|
00007|import hashlib
00008|import logging
00009|from pathlib import Path
00010|
00011|from django.contrib import messages
00012|from django.contrib.auth.decorators import login_required, user_passes_test
00013|from django.core.management import call_command
00014|from django.shortcuts import redirect, render
00015|from django.urls import reverse
00016|
00017|logger = logging.getLogger("pgc.admin_ingresos")
00018|
00019|from imports.forms import FileUploadForm
00020|from imports.models import FileUpload, guess_file_type_and_period
00021|
00022|from .admin_manual import (
00023|    get_manual_edit_context,
00024|    save_alias,
00025|    save_aliases_bulk,
00026|    save_fx,
00027|    save_import_rows,
00028|    save_period_note,
00029|    save_requirements,
00030|    save_results,
00031|    save_targets,
00032|)
00033|from .income_conversion import recalc_stale_ingresos
00034|from .admin_period import (
00035|    BLOCK_CROSS_SALE,
00036|    BLOCK_FINANCIAL,
00037|    BLOCK_META,
00038|    BLOCK_NEW_CLIENTS,
00039|    BLOCK_ORDER,
00040|    BLOCK_REVIEW,
00041|    discard_pending_upload,
00042|    get_admin_period_snapshot,
00043|    list_period_log,
00044|    recalculate_block,
00045|    recalculate_period,
00046|    remove_duplicate_new_client_rows,
00047|)
00048|from .admin_new_clients_browse import (
00049|    browse_context,
00050|    save_browse_rows,
00051|    save_une_reassignments,
00052|)
00053|from .admin_ingresos_year import get_ingresos_year_context, save_ingresos_year
00054|from .admin_recalc import run_smart_recalc_all
00055|from .admin_utils import (
00056|    admin_period_context,
00057|    parse_admin_period,
00058|    parse_period,
00059|    redirect_admin_ingresos_year,
00060|    redirect_admin_manual,
00061|    redirect_admin_monthly,
00062|    redirect_admin_new_clients_browse,
00063|    redirect_admin_new_clients_une,
00064|)
00065|
00066|
00067|def _save_upload(request, year: int, month: int, expected_type: str | None = None) -> FileUpload | None:
00068|    uploaded = request.FILES.get("stored_file")
00069|    if not uploaded:
00070|        messages.error(request, "Debe seleccionar un archivo.")
00071|        return None
00072|
00073|    hasher = hashlib.sha256()
00074|    for chunk in uploaded.chunks():
00075|        hasher.update(chunk)
00076|    uploaded_sha256 = hasher.hexdigest()
00077|    uploaded.seek(0)
00078|
00079|    original_filename = uploaded.name
00080|    file_type, detected_year, detected_month = guess_file_type_and_period(original_filename)
00081|
00082|    if expected_type and file_type != expected_type:
00083|        messages.warning(
00084|            request,
00085|            f"El archivo parece ser de tipo distinto al bloque ({file_type} vs {expected_type}).",
00086|        )
00087|
00088|    if detected_year and detected_month and (detected_year != year or detected_month != month):
00089|        messages.warning(
00090|            request,
00091|            f"El archivo sugiere período {detected_year}-{detected_month:02d}, "
00092|            f"pero trabaja en {year}-{month:02d}.",
00093|        )
00094|
00095|    obj = FileUpload(
00096|        uploaded_by=request.user,
00097|        stored_file=uploaded,
00098|        original_filename=original_filename,
00099|        mime_type=getattr(uploaded, "content_type", "") or "",
00100|        sha256=uploaded_sha256,
00101|        detected_year=detected_year or year,
00102|        detected_month=detected_month or month,
00103|        file_type_detected=file_type if file_type != FileUpload.TYPE_UNKNOWN else (expected_type or file_type),
00104|    )
00105|    obj.save()
00106|    messages.success(request, f"Archivo recibido: {obj.original_filename}.")
00107|    return obj
00108|
00109|
00110|def _process_upload(request, upload: FileUpload, year: int, month: int, block: str) -> None:
00111|    path = Path(upload.stored_file.path)
00112|    if not path.exists():
00113|        messages.error(request, "El archivo físico no existe en el servidor.")
00114|        return
00115|
00116|    try:
00117|        if block == BLOCK_NEW_CLIENTS:
00118|            if upload.status == FileUpload.STATUS_PARSED_OK:
00119|                messages.warning(
00120|                    request,
00121|                    "Este archivo ya fue procesado. Para evitar duplicados no se importó de nuevo. "
00122|                    "Si necesita reprocesar, suba el archivo otra vez.",
00123|                )
00124|                return
00125|            call_command(
00126|                "import_clientes_nuevos",
00127|                path=str(path),
00128|                file_upload_id=upload.id,
00129|            )
00130|            upload.status = FileUpload.STATUS_PARSED_OK
00131|            upload.save(update_fields=["status"])
00132|            messages.success(request, "Clientes nuevos procesados correctamente.")
00133|        elif block == BLOCK_CROSS_SALE:
00134|            if upload.status == FileUpload.STATUS_PARSED_OK:
00135|                messages.warning(
00136|                    request,
00137|                    "Este archivo ya fue procesado. Para evitar duplicados no se importó de nuevo. "
00138|                    "Si necesita reprocesar, suba el archivo otra vez.",
00139|                )
00140|                return
00141|            call_command("import_venta_cruzada", path=str(path))
00142|            upload.status = FileUpload.STATUS_PARSED_OK
00143|            upload.save(update_fields=["status"])
00144|            messages.success(request, "Venta cruzada procesada correctamente.")
00145|        elif block == BLOCK_FINANCIAL:
00146|            call_command("import_ingresos", path=str(path), year=year, month=month)
00147|            upload.status = FileUpload.STATUS_PARSED_OK
00148|            upload.save(update_fields=["status"])
00149|            messages.success(request, "Estado de resultados importado correctamente.")
00150|        else:
00151|            messages.error(request, "Este bloque no admite procesamiento de archivo.")
00152|    except Exception as exc:
00153|        upload.status = FileUpload.STATUS_PARSED_ERROR
00154|        upload.error_summary = str(exc)[:500]
00155|        upload.save(update_fields=["status", "error_summary"])
00156|        messages.error(request, f"Error al procesar: {exc}")
00157|
00158|
00159|def _admin_period_context(year: int, month: int) -> dict:
00160|    # Compat legacy; prefer admin_period_context(period).
00161|    from .admin_utils import AdminPeriod
00162|
00163|    return admin_period_context(AdminPeriod(year=year, month_from=month, month_to=month))
00164|
00165|
00166|@login_required
00167|@user_passes_test(lambda u: u.is_superuser)
00168|def admin_smart_recalc(request):
00169|    """Botón único: recalcula en orden todo lo pendiente (todos los períodos)."""
00170|    period = parse_admin_period(request)
00171|    next_url = (request.POST.get("next") or "").strip()
00172|
00173|    if request.method != "POST":
00174|        return redirect_admin_monthly(period=period)
00175|
00176|    try:
00177|        result = run_smart_recalc_all(user=request.user, force_all=False)
00178|        if not result["ran"]:
00179|            messages.info(request, result["messages"][0] if result["messages"] else "Nada pendiente.")
00180|        else:
00181|            messages.success(
00182|                request,
00183|                f"Recálculo inteligente: {result['periods_processed']} período(s) procesado(s).",
00184|            )
00185|            for msg in result["messages"][:40]:
00186|                messages.success(request, msg)
00187|            if len(result["messages"]) > 40:
00188|                messages.info(
00189|                    request,
00190|                    f"… y {len(result['messages']) - 40} mensaje(s) más.",
00191|                )
00192|            after = result["status_after"]
00193|            if after["is_pending"]:
00194|                messages.warning(
00195|                    request,
00196|                    f"Aún quedan {after['pending_count']} período(s) con pendientes "
00197|                    "(p.ej. falta tipo de cambio para convertir STALE).",
00198|                )
00199|            else:
00200|                messages.success(request, "Estado global: al día (verde).")
00201|    except Exception as exc:
00202|        messages.error(request, f"Error en recálculo inteligente: {exc}")
00203|
00204|    if next_url.startswith("/"):
00205|        return redirect(next_url)
00206|    return redirect_admin_monthly(period=period)
00207|
00208|
00209|@login_required
00210|@user_passes_test(lambda u: u.is_superuser)
00211|def admin_hub(request):
00212|    """Punto de entrada legado: redirige al tablero mensual."""
00213|    period = parse_admin_period(request)
00214|    return redirect(f"{reverse('pgc:admin_monthly')}?{period.querystring()}")
00215|
00216|
00217|@login_required
00218|@user_passes_test(lambda u: u.is_superuser)
00219|def admin_monthly(request):
00220|    period = parse_admin_period(request)
00221|    year, month = period.year, period.month
00222|    selected_block = (request.GET.get("block") or request.POST.get("block") or BLOCK_ORDER[0]).strip()
00223|
00224|    if request.method == "POST":
00225|        action = (request.POST.get("action") or "").strip()
00226|
00227|        if action == "recalculate_period":
00228|            try:
00229|                for msg in recalculate_period(year, month):
00230|                    messages.success(request, msg)
00231|            except Exception as exc:
00232|                messages.error(request, f"Error al recalcular período: {exc}")
00233|            return redirect_admin_monthly(period=period, block=selected_block)
00234|
00235|        if action == "recalculate_block":
00236|            block = request.POST.get("block") or selected_block
00237|            try:
00238|                for msg in recalculate_block(year, month, block):
00239|                    messages.success(request, msg)
00240|            except Exception as exc:
00241|                messages.error(request, f"Error al recalcular bloque: {exc}")
00242|            return redirect_admin_monthly(period=period, block=block)
00243|
00244|        if action == "upload":
00245|            block = request.POST.get("block") or selected_block
00246|            type_map = {
00247|                BLOCK_FINANCIAL: FileUpload.TYPE_FINANCIAL,
00248|                BLOCK_NEW_CLIENTS: FileUpload.TYPE_NEW_CLIENTS,
00249|                BLOCK_CROSS_SALE: FileUpload.TYPE_CROSS_SALE,
00250|            }
00251|            _save_upload(request, year, month, type_map.get(block))
00252|            return redirect_admin_monthly(period=period, block=block)
00253|
00254|        if action == "process":
00255|            block = request.POST.get("block") or selected_block
00256|            try:
00257|                file_id = int(request.POST.get("file_id") or "0")
00258|            except (TypeError, ValueError):
00259|                file_id = 0
00260|            upload = FileUpload.objects.filter(id=file_id).first()
00261|            if not upload:
00262|                messages.error(request, "Archivo no encontrado.")
00263|            else:
00264|                _process_upload(request, upload, year, month, block)
00265|            return redirect_admin_monthly(period=period, block=block)
00266|
00267|        if action == "discard_pending":
00268|            block = request.POST.get("block") or selected_block
00269|            try:
00270|                file_id = int(request.POST.get("file_id") or "0")
00271|            except (TypeError, ValueError):
00272|                file_id = 0
00273|            upload = FileUpload.objects.filter(id=file_id).first()
00274|            if not upload:
00275|                messages.error(request, "Archivo no encontrado.")
00276|            else:
00277|                try:
00278|                    result = discard_pending_upload(upload)
00279|                    messages.success(
00280|                        request,
00281|                        f"Se quitó de la cola: {result['filename']}. "
00282|                        "Los datos ya procesados no se modificaron.",
00283|                    )
00284|                except ValueError as exc:
00285|                    messages.error(request, str(exc))
00286|                except Exception as exc:
00287|                    messages.error(request, f"No se pudo quitar el archivo de la cola: {exc}")
00288|            return redirect_admin_monthly(period=period, block=block)
00289|
00290|        if action == "dedup_new_clients":
00291|            try:
00292|                result = remove_duplicate_new_client_rows(year, month, user=request.user)
00293|                if result["removed"]:
00294|                    messages.success(
00295|                        request,
00296|                        f"Se eliminaron {result['removed']} registro(s) duplicado(s) "
00297|                        f"y se actualizaron {result['metrics_updated']} métrica(s) de clientes nuevos.",
00298|                    )
00299|                else:
00300|                    messages.info(request, "No se encontraron duplicados en el detalle de clientes.")
00301|            except Exception as exc:
00302|                messages.error(request, f"Error al eliminar duplicados: {exc}")
00303|            return redirect_admin_monthly(period=period, block=BLOCK_NEW_CLIENTS)
00304|
00305|    snapshot = get_admin_period_snapshot(year, month)
00306|    if selected_block not in snapshot["blocks_by_id"]:
00307|        selected_block = BLOCK_ORDER[0]
00308|
00309|    context = {
00310|        **admin_period_context(period),
00311|        "snapshot": snapshot,
00312|        "selected_block": selected_block,
00313|        "block_detail": snapshot["blocks_by_id"][selected_block],
00314|        "block_order": BLOCK_ORDER,
00315|        "block_meta": BLOCK_META,
00316|        "upload_form": FileUploadForm(),
00317|        "recent_log": list_period_log(year, month, limit=8, month_from=period.month_from),
00318|        "supports_month_range": False,
00319|        "single_month_ops": True,
00320|    }
00321|    return render(request, "pgc/admin_monthly.html", context)
00322|
00323|
00324|@login_required
00325|@user_passes_test(lambda u: u.is_superuser)
00326|def admin_manual_edit(request):
00327|    period = parse_admin_period(request)
00328|    year, month = period.year, period.month
00329|    tab = (request.GET.get("tab") or request.POST.get("tab") or "targets").strip()
00330|
00331|    if request.method == "POST":
00332|        action = (request.POST.get("action") or "").strip()
00333|        reason = (request.POST.get("reason") or "").strip()
00334|        recalc_after = request.POST.get("recalc_after") == "1"
00335|
00336|        try:
00337|            changes = 0
00338|            if action == "save_targets":
00339|                changes = save_targets(request.user, year, month, request.POST, reason)
00340|            elif action == "save_results":
00341|                changes = save_results(request.user, year, month, request.POST, reason)
00342|            elif action == "recalc_stale_ingresos":
00343|                result = recalc_stale_ingresos(
00344|                    year=year,
00345|                    month=month,
00346|                    user=request.user,
00347|                    reason=reason or "Recálculo de ingresos STALE desde admin",
00348|                )
00349|                changes = result["updated"]
00350|                if changes:
00351|                    messages.success(
00352|                        request,
00353|                        f"Se recalcularon {changes} ingreso(s) con TC={result['fx']}.",
00354|                    )
00355|                    if recalc_after:
00356|                        try:
00357|                            for msg in recalculate_period(year, month):
00358|                                messages.success(request, msg)
00359|                        except Exception as exc:
00360|                            messages.warning(
00361|                                request,
00362|                                f"Recálculo de ingresos listo, pero falló el score: {exc}",
00363|                            )
00364|                    return redirect_admin_manual(period=period, tab=tab)
00365|                messages.info(request, "No hay ingresos STALE para recalcular.")
00366|                return redirect_admin_manual(period=period, tab=tab)
00367|            elif action == "save_requirements":
00368|                changes = save_requirements(request.user, year, month, request.POST, reason)
00369|            elif action == "save_fx":
00370|                changes = save_fx(
00371|                    request.user,
00372|                    year,
00373|                    month,
00374|                    request.POST,
00375|                    reason,
00376|                    month_from=period.month_from,
00377|                )
00378|            elif action == "save_alias":
00379|                changes = save_alias(request.user, year, month, request.POST, reason)
00380|            elif action == "save_aliases_bulk":
00381|                changes = save_aliases_bulk(request.user, year, month, request.POST, reason)
00382|            elif action == "save_imports":
00383|                changes = save_import_rows(
00384|                    request.user,
00385|                    year,
00386|                    month,
00387|                    request.POST,
00388|                    reason,
00389|                    month_from=period.month_from,
00390|                )
00391|            elif action == "save_notes":
00392|                changes = save_period_note(request.user, year, month, request.POST, reason)
00393|            else:
00394|                messages.error(request, "Acción no reconocida.")
00395|                return redirect_admin_manual(period=period, tab=tab)
00396|
00397|            if changes:
00398|                messages.success(request, f"Se guardaron {changes} cambio(s).")
00399|                if recalc_after:
00400|                    try:
00401|                        for msg in recalculate_period(year, month):
00402|                            messages.success(request, msg)
00403|                    except Exception as exc:
00404|                        messages.warning(request, f"Cambios guardados, pero falló el recálculo: {exc}")
00405|            else:
00406|                messages.info(request, "No hubo cambios que guardar.")
00407|        except ValueError as exc:
00408|            messages.error(request, str(exc))
00409|        except Exception as exc:
00410|            messages.error(request, f"Error al guardar: {exc}")
00411|
00412|        return redirect_admin_manual(period=period, tab=tab)
00413|
00414|    context = {
00415|        **admin_period_context(period),
00416|        **get_manual_edit_context(year, month, tab, month_from=period.month_from),
00417|    }
00418|    return render(request, "pgc/admin_manual_edit.html", context)
00419|
00420|
00421|@login_required
00422|@user_passes_test(lambda u: u.is_superuser)
00423|def admin_ingresos_year(request):
00424|    """Matriz anual: 12 meses × 4 UNEs + TC (captura de ingresos reales)."""
00425|    period = parse_admin_period(request)
00426|    year = period.year
00427|    capture_currency = (request.GET.get("curr") or request.POST.get("capture_currency") or "GTQ").strip()
00428|
00429|    if request.method == "POST":
00430|        action = (request.POST.get("action") or "").strip()
00431|        reason = (request.POST.get("reason") or "").strip()
00432|        recalc_after = request.POST.get("recalc_after") == "1"
00433|        capture_currency = (request.POST.get("capture_currency") or capture_currency).strip()
00434|
00435|        if action == "save_ingresos_year":
00436|            ing_keys = sorted(k for k in request.POST if k.startswith("ing_"))
00437|            fx_keys = sorted(k for k in request.POST if k.startswith("fx_"))
00438|            logger.warning(
00439|                "ingresos_year POST year=%s curr=%s reason_len=%s "
00440|                "ing_nonempty=%s fx_nonempty=%s ing_sample=%s fx_sample=%s",
00441|                year,
00442|                capture_currency,
00443|                len(reason),
00444|                sum(1 for k in ing_keys if (request.POST.get(k) or "").strip()),
00445|                sum(1 for k in fx_keys if (request.POST.get(k) or "").strip()),
00446|                [(k, request.POST.get(k)) for k in ing_keys if (request.POST.get(k) or "").strip()][:8],
00447|                [(k, request.POST.get(k)) for k in fx_keys if (request.POST.get(k) or "").strip()][:8],
00448|            )
00449|            try:
00450|                result = save_ingresos_year(request.user, year, request.POST, reason)
00451|                income_n = result["income_changes"]
00452|                fx_n = result["fx_changes"]
00453|                logger.warning(
00454|                    "ingresos_year result year=%s income_changes=%s fx_changes=%s currency=%s",
00455|                    year,
00456|                    income_n,
00457|                    fx_n,
00458|                    result["currency"],
00459|                )
00460|                if income_n:
00461|                    messages.success(
00462|                        request,
00463|                        f"Guardado: {income_n} ingreso(s), {fx_n} TC; "
00464|                        f"moneda captura={result['currency']}.",
00465|                    )
00466|                    if recalc_after:
00467|                        # Recalcula score del mes foco del selector (no los 12).
00468|                        try:
00469|                            for msg in recalculate_period(year, period.month):
00470|                                messages.success(request, msg)
00471|                        except Exception as exc:
00472|                            messages.warning(
00473|                                request,
00474|                                f"Ingresos guardados, pero falló el score de "
00475|                                f"{year}-{period.month:02d}: {exc}",
00476|                            )
00477|                elif fx_n:
00478|                    messages.warning(
00479|                        request,
00480|                        f"Solo se guardaron {fx_n} tipo(s) de cambio. "
00481|                        "No llegó ningún valor de ingreso en el POST "
00482|                        "(celdas vacías o no enviadas). Complete ingresos y vuelva a Guardar.",
00483|                    )
00484|                else:
00485|                    messages.warning(
00486|                        request,
00487|                        "Sin cambios: no se recibieron ingresos ni tipos de cambio "
00488|                        "con valor nuevo. Revise el formulario y el motivo, luego reintente.",
00489|                    )
00490|            except Exception as exc:
00491|                logger.warning("ingresos_year save failed year=%s err=%s", year, exc)
00492|                messages.error(request, str(exc))
00493|            return redirect_admin_ingresos_year(
00494|                period=period, curr=capture_currency
00495|            )
00496|
00497|    context = {
00498|        **admin_period_context(period),
00499|        **get_ingresos_year_context(year, capture_currency=capture_currency),
00500|        "supports_month_range": False,
00501|        "single_month_ops": False,
00502|    }
00503|    return render(request, "pgc/admin_ingresos_year.html", context)
00504|
00505|
00506|@login_required
00507|@user_passes_test(lambda u: u.is_superuser)
00508|def admin_monthly_log(request):
00509|    period = parse_admin_period(request)
00510|    year, month = period.year, period.month
00511|    entries = list_period_log(year, month, limit=150, month_from=period.month_from)
00512|    snapshot = get_admin_period_snapshot(year, month)
00513|
00514|    context = {
00515|        **admin_period_context(period),
00516|        "period_label": period.label,
00517|        "entries": entries,
00518|        "snapshot": snapshot,
00519|        "supports_month_range": True,
00520|        "single_month_ops": False,
00521|    }
00522|    return render(request, "pgc/admin_monthly_log.html", context)
00523|
00524|
00525|@login_required
00526|@user_passes_test(lambda u: u.is_superuser)
00527|def admin_new_clients_browse(request):
00528|    period = parse_admin_period(request)
00529|
00530|    if request.method == "POST":
00531|        reason = (request.POST.get("reason") or "").strip()
00532|        recalc_after = request.POST.get("recalc_after") == "1"
00533|        try:
00534|            result = save_browse_rows(request.user, period, request.POST, reason)
00535|            if result["total"]:
00536|                parts = []
00537|                if result["updated"]:
00538|                    parts.append(f"{result['updated']} editado(s)")
00539|                if result["deleted"]:
00540|                    parts.append(f"{result['deleted']} eliminado(s)")
00541|                if result["created"]:
00542|                    parts.append(f"{result['created']} creado(s)")
00543|                messages.success(
00544|                    request,
00545|                    f"Guardado: {', '.join(parts)}. "
00546|                    f"Métricas actualizadas: {result['metrics_updated']}.",
00547|                )
00548|                if recalc_after:
00549|                    try:
00550|                        for msg in recalculate_block(
00551|                            period.year, period.month, BLOCK_NEW_CLIENTS
00552|                        ):
00553|                            messages.success(request, msg)
00554|                    except Exception as exc:
00555|                        messages.warning(
00556|                            request,
00557|                            f"Cambios guardados, pero falló el recálculo: {exc}",
00558|                        )
00559|            else:
00560|                messages.info(request, "No hubo cambios que guardar.")
00561|        except ValueError as exc:
00562|            messages.error(request, str(exc))
00563|        except Exception as exc:
00564|            messages.error(request, f"Error al guardar: {exc}")
00565|        return redirect_admin_new_clients_browse(period=period)
00566|
00567|    context = {
00568|        **admin_period_context(period),
00569|        **browse_context(period),
00570|        "adm_nav_active": "clients_browse",
00571|    }
00572|    return render(request, "pgc/admin_new_clients_browse.html", context)
00573|
00574|
00575|@login_required
00576|@user_passes_test(lambda u: u.is_superuser)
00577|def admin_new_clients_une(request):
00578|    period = parse_admin_period(request)
00579|
00580|    if request.method == "POST":
00581|        reason = (request.POST.get("reason") or "").strip()
00582|        recalc_after = request.POST.get("recalc_after") == "1"
00583|        try:
00584|            result = save_une_reassignments(
00585|                request.user, period, request.POST, reason
00586|            )
00587|            if result["changed"]:
00588|                messages.success(
00589|                    request,
00590|                    f"Se reasignaron {result['changed']} registro(s). "
00591|                    f"Métricas actualizadas: {result['metrics_updated']}.",
00592|                )
00593|                if recalc_after:
00594|                    try:
00595|                        for msg in recalculate_block(
00596|                            period.year, period.month, BLOCK_NEW_CLIENTS
00597|                        ):
00598|                            messages.success(request, msg)
00599|                    except Exception as exc:
00600|                        messages.warning(
00601|                            request,
00602|                            f"Cambios guardados, pero falló el recálculo: {exc}",
00603|                        )
00604|            else:
00605|                messages.info(request, "No hubo cambios de UNE.")
00606|        except ValueError as exc:
00607|            messages.error(request, str(exc))
00608|        except Exception as exc:
00609|            messages.error(request, f"Error al guardar: {exc}")
00610|        return redirect_admin_new_clients_une(period=period)
00611|
00612|    context = {
00613|        **admin_period_context(period),
00614|        **browse_context(period),
00615|        "adm_nav_active": "clients_une",
00616|    }
00617|    return render(request, "pgc/admin_new_clients_une.html", context)
00618|
00619|
00620|@login_required
00621|@user_passes_test(lambda u: u.is_superuser)
00622|def legacy_run_recalc_pgc(request):
00623|    """Compatibilidad con URLs/formularios antiguos de recálculo."""
00624|    year, month = parse_period(request)
00625|    if request.method != "POST":
00626|        messages.error(request, "Método no permitido.")
00627|        return redirect_admin_monthly(year, month, BLOCK_REVIEW)
00628|
00629|    year_raw = (request.POST.get("year") or "").strip()
00630|    month_raw = (request.POST.get("month") or "").strip()
00631|    try:
00632|        year = int(year_raw)
00633|        month = int(month_raw)
00634|        if month < 1 or month > 12:
00635|            raise ValueError
00636|    except (TypeError, ValueError):
00637|        messages.error(request, "Debes indicar año y mes válidos.")
00638|        return redirect_admin_monthly(year, month, BLOCK_REVIEW)
00639|
00640|    try:
00641|        for msg in recalculate_period(year, month):
00642|            messages.success(request, msg)
00643|    except Exception as exc:
00644|        messages.error(request, f"Error al ejecutar recalc PGC: {exc}")
00645|
00646|    return redirect_admin_monthly(year, month, BLOCK_REVIEW)
00647|
00648|
00649|@login_required
00650|@user_passes_test(lambda u: u.is_superuser)
00651|def legacy_run_recalc_investment(request):
00652|    """Compatibilidad con URLs/formularios antiguos de recálculo Investment."""
00653|    year, month = parse_period(request)
00654|    if request.method != "POST":
00655|        messages.error(request, "Método no permitido.")
00656|        return redirect_admin_monthly(year, month, BLOCK_NEW_CLIENTS)
00657|
00658|    year_raw = (request.POST.get("year") or "").strip()
00659|    month_raw = (request.POST.get("month") or "").strip()
00660|    try:
00661|        year = int(year_raw)
00662|        month = int(month_raw)
00663|        if month < 1 or month > 12:
00664|            raise ValueError
00665|    except (TypeError, ValueError):
00666|        messages.error(request, "Debes indicar año y mes válidos.")
00667|        return redirect_admin_monthly(year, month, BLOCK_NEW_CLIENTS)
00668|
00669|    try:
00670|        for msg in recalculate_block(year, month, BLOCK_NEW_CLIENTS):
00671|            messages.success(request, msg)
00672|    except Exception as exc:
00673|        messages.error(request, f"Error al ejecutar recalc Investment: {exc}")
00674|
00675|    return redirect_admin_monthly(year, month, BLOCK_NEW_CLIENTS)
00676|
00677|
00678|@login_required
00679|@user_passes_test(lambda u: u.is_superuser)
00680|def redirect_manual_results(request):
00681|    """Legacy URL: /admin-hub/ingresos-manual-capture → matriz anual de ingresos."""
00682|    period = parse_admin_period(request)
00683|    return redirect_admin_ingresos_year(period=period)
00684|
00685|
00686|@login_required
00687|@user_passes_test(lambda u: u.is_superuser)
00688|def redirect_manual_fx(request):
00689|    year, month = parse_period(request)
00690|    return redirect_admin_manual(year, month, "fx")

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiClZpc3RhcyBkZWwgw6FyZWEgZGUgQWRtaW5pc3RyYWNpw7NuIHJlZGlzZcOxYWRhLgoiIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmltcG9ydCBoYXNobGliCmltcG9ydCBsb2dnaW5nCmZyb20gcGF0aGxpYiBpbXBvcnQgUGF0aAoKZnJvbSBkamFuZ28uY29udHJpYiBpbXBvcnQgbWVzc2FnZXMKZnJvbSBkamFuZ28uY29udHJpYi5hdXRoLmRlY29yYXRvcnMgaW1wb3J0IGxvZ2luX3JlcXVpcmVkLCB1c2VyX3Bhc3Nlc190ZXN0CmZyb20gZGphbmdvLmNvcmUubWFuYWdlbWVudCBpbXBvcnQgY2FsbF9jb21tYW5kCmZyb20gZGphbmdvLnNob3J0Y3V0cyBpbXBvcnQgcmVkaXJlY3QsIHJlbmRlcgpmcm9tIGRqYW5nby51cmxzIGltcG9ydCByZXZlcnNlCgpsb2dnZXIgPSBsb2dnaW5nLmdldExvZ2dlcigicGdjLmFkbWluX2luZ3Jlc29zIikKCmZyb20gaW1wb3J0cy5mb3JtcyBpbXBvcnQgRmlsZVVwbG9hZEZvcm0KZnJvbSBpbXBvcnRzLm1vZGVscyBpbXBvcnQgRmlsZVVwbG9hZCwgZ3Vlc3NfZmlsZV90eXBlX2FuZF9wZXJpb2QKCmZyb20gLmFkbWluX21hbnVhbCBpbXBvcnQgKAogICAgZ2V0X21hbnVhbF9lZGl0X2NvbnRleHQsCiAgICBzYXZlX2FsaWFzLAogICAgc2F2ZV9hbGlhc2VzX2J1bGssCiAgICBzYXZlX2Z4LAogICAgc2F2ZV9pbXBvcnRfcm93cywKICAgIHNhdmVfcGVyaW9kX25vdGUsCiAgICBzYXZlX3JlcXVpcmVtZW50cywKICAgIHNhdmVfcmVzdWx0cywKICAgIHNhdmVfdGFyZ2V0cywKKQpmcm9tIC5pbmNvbWVfY29udmVyc2lvbiBpbXBvcnQgcmVjYWxjX3N0YWxlX2luZ3Jlc29zCmZyb20gLmFkbWluX3BlcmlvZCBpbXBvcnQgKAogICAgQkxPQ0tfQ1JPU1NfU0FMRSwKICAgIEJMT0NLX0ZJTkFOQ0lBTCwKICAgIEJMT0NLX01FVEEsCiAgICBCTE9DS19ORVdfQ0xJRU5UUywKICAgIEJMT0NLX09SREVSLAogICAgQkxPQ0tfUkVWSUVXLAogICAgZGlzY2FyZF9wZW5kaW5nX3VwbG9hZCwKICAgIGdldF9hZG1pbl9wZXJpb2Rfc25hcHNob3QsCiAgICBsaXN0X3BlcmlvZF9sb2csCiAgICByZWNhbGN1bGF0ZV9ibG9jaywKICAgIHJlY2FsY3VsYXRlX3BlcmlvZCwKICAgIHJlbW92ZV9kdXBsaWNhdGVfbmV3X2NsaWVudF9yb3dzLAopCmZyb20gLmFkbWluX25ld19jbGllbnRzX2Jyb3dzZSBpbXBvcnQgKAogICAgYnJvd3NlX2NvbnRleHQsCiAgICBzYXZlX2Jyb3dzZV9yb3dzLAogICAgc2F2ZV91bmVfcmVhc3NpZ25tZW50cywKKQpmcm9tIC5hZG1pbl9pbmdyZXNvc195ZWFyIGltcG9ydCBnZXRfaW5ncmVzb3NfeWVhcl9jb250ZXh0LCBzYXZlX2luZ3Jlc29zX3llYXIKZnJvbSAuYWRtaW5fcmVjYWxjIGltcG9ydCBydW5fc21hcnRfcmVjYWxjX2FsbApmcm9tIC5hZG1pbl91dGlscyBpbXBvcnQgKAogICAgYWRtaW5fcGVyaW9kX2NvbnRleHQsCiAgICBwYXJzZV9hZG1pbl9wZXJpb2QsCiAgICBwYXJzZV9wZXJpb2QsCiAgICByZWRpcmVjdF9hZG1pbl9pbmdyZXNvc195ZWFyLAogICAgcmVkaXJlY3RfYWRtaW5fbWFudWFsLAogICAgcmVkaXJlY3RfYWRtaW5fbW9udGhseSwKICAgIHJlZGlyZWN0X2FkbWluX25ld19jbGllbnRzX2Jyb3dzZSwKICAgIHJlZGlyZWN0X2FkbWluX25ld19jbGllbnRzX3VuZSwKKQoKCmRlZiBfc2F2ZV91cGxvYWQocmVxdWVzdCwgeWVhcjogaW50LCBtb250aDogaW50LCBleHBlY3RlZF90eXBlOiBzdHIgfCBOb25lID0gTm9uZSkgLT4gRmlsZVVwbG9hZCB8IE5vbmU6CiAgICB1cGxvYWRlZCA9IHJlcXVlc3QuRklMRVMuZ2V0KCJzdG9yZWRfZmlsZSIpCiAgICBpZiBub3QgdXBsb2FkZWQ6CiAgICAgICAgbWVzc2FnZXMuZXJyb3IocmVxdWVzdCwgIkRlYmUgc2VsZWNjaW9uYXIgdW4gYXJjaGl2by4iKQogICAgICAgIHJldHVybiBOb25lCgogICAgaGFzaGVyID0gaGFzaGxpYi5zaGEyNTYoKQogICAgZm9yIGNodW5rIGluIHVwbG9hZGVkLmNodW5rcygpOgogICAgICAgIGhhc2hlci51cGRhdGUoY2h1bmspCiAgICB1cGxvYWRlZF9zaGEyNTYgPSBoYXNoZXIuaGV4ZGlnZXN0KCkKICAgIHVwbG9hZGVkLnNlZWsoMCkKCiAgICBvcmlnaW5hbF9maWxlbmFtZSA9IHVwbG9hZGVkLm5hbWUKICAgIGZpbGVfdHlwZSwgZGV0ZWN0ZWRfeWVhciwgZGV0ZWN0ZWRfbW9udGggPSBndWVzc19maWxlX3R5cGVfYW5kX3BlcmlvZChvcmlnaW5hbF9maWxlbmFtZSkKCiAgICBpZiBleHBlY3RlZF90eXBlIGFuZCBmaWxlX3R5cGUgIT0gZXhwZWN0ZWRfdHlwZToKICAgICAgICBtZXNzYWdlcy53YXJuaW5nKAogICAgICAgICAgICByZXF1ZXN0LAogICAgICAgICAgICBmIkVsIGFyY2hpdm8gcGFyZWNlIHNlciBkZSB0aXBvIGRpc3RpbnRvIGFsIGJsb3F1ZSAoe2ZpbGVfdHlwZX0gdnMge2V4cGVjdGVkX3R5cGV9KS4iLAogICAgICAgICkKCiAgICBpZiBkZXRlY3RlZF95ZWFyIGFuZCBkZXRlY3RlZF9tb250aCBhbmQgKGRldGVjdGVkX3llYXIgIT0geWVhciBvciBkZXRlY3RlZF9tb250aCAhPSBtb250aCk6CiAgICAgICAgbWVzc2FnZXMud2FybmluZygKICAgICAgICAgICAgcmVxdWVzdCwKICAgICAgICAgICAgZiJFbCBhcmNoaXZvIHN1Z2llcmUgcGVyw61vZG8ge2RldGVjdGVkX3llYXJ9LXtkZXRlY3RlZF9tb250aDowMmR9LCAiCiAgICAgICAgICAgIGYicGVybyB0cmFiYWphIGVuIHt5ZWFyfS17bW9udGg6MDJkfS4iLAogICAgICAgICkKCiAgICBvYmogPSBGaWxlVXBsb2FkKAogICAgICAgIHVwbG9hZGVkX2J5PXJlcXVlc3QudXNlciwKICAgICAgICBzdG9yZWRfZmlsZT11cGxvYWRlZCwKICAgICAgICBvcmlnaW5hbF9maWxlbmFtZT1vcmlnaW5hbF9maWxlbmFtZSwKICAgICAgICBtaW1lX3R5cGU9Z2V0YXR0cih1cGxvYWRlZCwgImNvbnRlbnRfdHlwZSIsICIiKSBvciAiIiwKICAgICAgICBzaGEyNTY9dXBsb2FkZWRfc2hhMjU2LAogICAgICAgIGRldGVjdGVkX3llYXI9ZGV0ZWN0ZWRfeWVhciBvciB5ZWFyLAogICAgICAgIGRldGVjdGVkX21vbnRoPWRldGVjdGVkX21vbnRoIG9yIG1vbnRoLAogICAgICAgIGZpbGVfdHlwZV9kZXRlY3RlZD1maWxlX3R5cGUgaWYgZmlsZV90eXBlICE9IEZpbGVVcGxvYWQuVFlQRV9VTktOT1dOIGVsc2UgKGV4cGVjdGVkX3R5cGUgb3IgZmlsZV90eXBlKSwKICAgICkKICAgIG9iai5zYXZlKCkKICAgIG1lc3NhZ2VzLnN1Y2Nlc3MocmVxdWVzdCwgZiJBcmNoaXZvIHJlY2liaWRvOiB7b2JqLm9yaWdpbmFsX2ZpbGVuYW1lfS4iKQogICAgcmV0dXJuIG9iagoKCmRlZiBfcHJvY2Vzc191cGxvYWQocmVxdWVzdCwgdXBsb2FkOiBGaWxlVXBsb2FkLCB5ZWFyOiBpbnQsIG1vbnRoOiBpbnQsIGJsb2NrOiBzdHIpIC0+IE5vbmU6CiAgICBwYXRoID0gUGF0aCh1cGxvYWQuc3RvcmVkX2ZpbGUucGF0aCkKICAgIGlmIG5vdCBwYXRoLmV4aXN0cygpOgogICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsICJFbCBhcmNoaXZvIGbDrXNpY28gbm8gZXhpc3RlIGVuIGVsIHNlcnZpZG9yLiIpCiAgICAgICAgcmV0dXJuCgogICAgdHJ5OgogICAgICAgIGlmIGJsb2NrID09IEJMT0NLX05FV19DTElFTlRTOgogICAgICAgICAgICBpZiB1cGxvYWQuc3RhdHVzID09IEZpbGVVcGxvYWQuU1RBVFVTX1BBUlNFRF9PSzoKICAgICAgICAgICAgICAgIG1lc3NhZ2VzLndhcm5pbmcoCiAgICAgICAgICAgICAgICAgICAgcmVxdWVzdCwKICAgICAgICAgICAgICAgICAgICAiRXN0ZSBhcmNoaXZvIHlhIGZ1ZSBwcm9jZXNhZG8uIFBhcmEgZXZpdGFyIGR1cGxpY2Fkb3Mgbm8gc2UgaW1wb3J0w7MgZGUgbnVldm8uICIKICAgICAgICAgICAgICAgICAgICAiU2kgbmVjZXNpdGEgcmVwcm9jZXNhciwgc3ViYSBlbCBhcmNoaXZvIG90cmEgdmV6LiIsCiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICByZXR1cm4KICAgICAgICAgICAgY2FsbF9jb21tYW5kKAogICAgICAgICAgICAgICAgImltcG9ydF9jbGllbnRlc19udWV2b3MiLAogICAgICAgICAgICAgICAgcGF0aD1zdHIocGF0aCksCiAgICAgICAgICAgICAgICBmaWxlX3VwbG9hZF9pZD11cGxvYWQuaWQsCiAgICAgICAgICAgICkKICAgICAgICAgICAgdXBsb2FkLnN0YXR1cyA9IEZpbGVVcGxvYWQuU1RBVFVTX1BBUlNFRF9PSwogICAgICAgICAgICB1cGxvYWQuc2F2ZSh1cGRhdGVfZmllbGRzPVsic3RhdHVzIl0pCiAgICAgICAgICAgIG1lc3NhZ2VzLnN1Y2Nlc3MocmVxdWVzdCwgIkNsaWVudGVzIG51ZXZvcyBwcm9jZXNhZG9zIGNvcnJlY3RhbWVudGUuIikKICAgICAgICBlbGlmIGJsb2NrID09IEJMT0NLX0NST1NTX1NBTEU6CiAgICAgICAgICAgIGlmIHVwbG9hZC5zdGF0dXMgPT0gRmlsZVVwbG9hZC5TVEFUVVNfUEFSU0VEX09LOgogICAgICAgICAgICAgICAgbWVzc2FnZXMud2FybmluZygKICAgICAgICAgICAgICAgICAgICByZXF1ZXN0LAogICAgICAgICAgICAgICAgICAgICJFc3RlIGFyY2hpdm8geWEgZnVlIHByb2Nlc2Fkby4gUGFyYSBldml0YXIgZHVwbGljYWRvcyBubyBzZSBpbXBvcnTDsyBkZSBudWV2by4gIgogICAgICAgICAgICAgICAgICAgICJTaSBuZWNlc2l0YSByZXByb2Nlc2FyLCBzdWJhIGVsIGFyY2hpdm8gb3RyYSB2ZXouIiwKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIHJldHVybgogICAgICAgICAgICBjYWxsX2NvbW1hbmQoImltcG9ydF92ZW50YV9jcnV6YWRhIiwgcGF0aD1zdHIocGF0aCkpCiAgICAgICAgICAgIHVwbG9hZC5zdGF0dXMgPSBGaWxlVXBsb2FkLlNUQVRVU19QQVJTRURfT0sKICAgICAgICAgICAgdXBsb2FkLnNhdmUodXBkYXRlX2ZpZWxkcz1bInN0YXR1cyJdKQogICAgICAgICAgICBtZXNzYWdlcy5zdWNjZXNzKHJlcXVlc3QsICJWZW50YSBjcnV6YWRhIHByb2Nlc2FkYSBjb3JyZWN0YW1lbnRlLiIpCiAgICAgICAgZWxpZiBibG9jayA9PSBCTE9DS19GSU5BTkNJQUw6CiAgICAgICAgICAgIGNhbGxfY29tbWFuZCgiaW1wb3J0X2luZ3Jlc29zIiwgcGF0aD1zdHIocGF0aCksIHllYXI9eWVhciwgbW9udGg9bW9udGgpCiAgICAgICAgICAgIHVwbG9hZC5zdGF0dXMgPSBGaWxlVXBsb2FkLlNUQVRVU19QQVJTRURfT0sKICAgICAgICAgICAgdXBsb2FkLnNhdmUodXBkYXRlX2ZpZWxkcz1bInN0YXR1cyJdKQogICAgICAgICAgICBtZXNzYWdlcy5zdWNjZXNzKHJlcXVlc3QsICJFc3RhZG8gZGUgcmVzdWx0YWRvcyBpbXBvcnRhZG8gY29ycmVjdGFtZW50ZS4iKQogICAgICAgIGVsc2U6CiAgICAgICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsICJFc3RlIGJsb3F1ZSBubyBhZG1pdGUgcHJvY2VzYW1pZW50byBkZSBhcmNoaXZvLiIpCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGV4YzoKICAgICAgICB1cGxvYWQuc3RhdHVzID0gRmlsZVVwbG9hZC5TVEFUVVNfUEFSU0VEX0VSUk9SCiAgICAgICAgdXBsb2FkLmVycm9yX3N1bW1hcnkgPSBzdHIoZXhjKVs6NTAwXQogICAgICAgIHVwbG9hZC5zYXZlKHVwZGF0ZV9maWVsZHM9WyJzdGF0dXMiLCAiZXJyb3Jfc3VtbWFyeSJdKQogICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsIGYiRXJyb3IgYWwgcHJvY2VzYXI6IHtleGN9IikKCgpkZWYgX2FkbWluX3BlcmlvZF9jb250ZXh0KHllYXI6IGludCwgbW9udGg6IGludCkgLT4gZGljdDoKICAgICMgQ29tcGF0IGxlZ2FjeTsgcHJlZmVyIGFkbWluX3BlcmlvZF9jb250ZXh0KHBlcmlvZCkuCiAgICBmcm9tIC5hZG1pbl91dGlscyBpbXBvcnQgQWRtaW5QZXJpb2QKCiAgICByZXR1cm4gYWRtaW5fcGVyaW9kX2NvbnRleHQoQWRtaW5QZXJpb2QoeWVhcj15ZWFyLCBtb250aF9mcm9tPW1vbnRoLCBtb250aF90bz1tb250aCkpCgoKQGxvZ2luX3JlcXVpcmVkCkB1c2VyX3Bhc3Nlc190ZXN0KGxhbWJkYSB1OiB1LmlzX3N1cGVydXNlcikKZGVmIGFkbWluX3NtYXJ0X3JlY2FsYyhyZXF1ZXN0KToKICAgICIiIkJvdMOzbiDDum5pY286IHJlY2FsY3VsYSBlbiBvcmRlbiB0b2RvIGxvIHBlbmRpZW50ZSAodG9kb3MgbG9zIHBlcsOtb2RvcykuIiIiCiAgICBwZXJpb2QgPSBwYXJzZV9hZG1pbl9wZXJpb2QocmVxdWVzdCkKICAgIG5leHRfdXJsID0gKHJlcXVlc3QuUE9TVC5nZXQoIm5leHQiKSBvciAiIikuc3RyaXAoKQoKICAgIGlmIHJlcXVlc3QubWV0aG9kICE9ICJQT1NUIjoKICAgICAgICByZXR1cm4gcmVkaXJlY3RfYWRtaW5fbW9udGhseShwZXJpb2Q9cGVyaW9kKQoKICAgIHRyeToKICAgICAgICByZXN1bHQgPSBydW5fc21hcnRfcmVjYWxjX2FsbCh1c2VyPXJlcXVlc3QudXNlciwgZm9yY2VfYWxsPUZhbHNlKQogICAgICAgIGlmIG5vdCByZXN1bHRbInJhbiJdOgogICAgICAgICAgICBtZXNzYWdlcy5pbmZvKHJlcXVlc3QsIHJlc3VsdFsibWVzc2FnZXMiXVswXSBpZiByZXN1bHRbIm1lc3NhZ2VzIl0gZWxzZSAiTmFkYSBwZW5kaWVudGUuIikKICAgICAgICBlbHNlOgogICAgICAgICAgICBtZXNzYWdlcy5zdWNjZXNzKAogICAgICAgICAgICAgICAgcmVxdWVzdCwKICAgICAgICAgICAgICAgIGYiUmVjw6FsY3VsbyBpbnRlbGlnZW50ZToge3Jlc3VsdFsncGVyaW9kc19wcm9jZXNzZWQnXX0gcGVyw61vZG8ocykgcHJvY2VzYWRvKHMpLiIsCiAgICAgICAgICAgICkKICAgICAgICAgICAgZm9yIG1zZyBpbiByZXN1bHRbIm1lc3NhZ2VzIl1bOjQwXToKICAgICAgICAgICAgICAgIG1lc3NhZ2VzLnN1Y2Nlc3MocmVxdWVzdCwgbXNnKQogICAgICAgICAgICBpZiBsZW4ocmVzdWx0WyJtZXNzYWdlcyJdKSA+IDQwOgogICAgICAgICAgICAgICAgbWVzc2FnZXMuaW5mbygKICAgICAgICAgICAgICAgICAgICByZXF1ZXN0LAogICAgICAgICAgICAgICAgICAgIGYi4oCmIHkge2xlbihyZXN1bHRbJ21lc3NhZ2VzJ10pIC0gNDB9IG1lbnNhamUocykgbcOhcy4iLAogICAgICAgICAgICAgICAgKQogICAgICAgICAgICBhZnRlciA9IHJlc3VsdFsic3RhdHVzX2FmdGVyIl0KICAgICAgICAgICAgaWYgYWZ0ZXJbImlzX3BlbmRpbmciXToKICAgICAgICAgICAgICAgIG1lc3NhZ2VzLndhcm5pbmcoCiAgICAgICAgICAgICAgICAgICAgcmVxdWVzdCwKICAgICAgICAgICAgICAgICAgICBmIkHDum4gcXVlZGFuIHthZnRlclsncGVuZGluZ19jb3VudCddfSBwZXLDrW9kbyhzKSBjb24gcGVuZGllbnRlcyAiCiAgICAgICAgICAgICAgICAgICAgIihwLmVqLiBmYWx0YSB0aXBvIGRlIGNhbWJpbyBwYXJhIGNvbnZlcnRpciBTVEFMRSkuIiwKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIG1lc3NhZ2VzLnN1Y2Nlc3MocmVxdWVzdCwgIkVzdGFkbyBnbG9iYWw6IGFsIGTDrWEgKHZlcmRlKS4iKQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBleGM6CiAgICAgICAgbWVzc2FnZXMuZXJyb3IocmVxdWVzdCwgZiJFcnJvciBlbiByZWPDoWxjdWxvIGludGVsaWdlbnRlOiB7ZXhjfSIpCgogICAgaWYgbmV4dF91cmwuc3RhcnRzd2l0aCgiLyIpOgogICAgICAgIHJldHVybiByZWRpcmVjdChuZXh0X3VybCkKICAgIHJldHVybiByZWRpcmVjdF9hZG1pbl9tb250aGx5KHBlcmlvZD1wZXJpb2QpCgoKQGxvZ2luX3JlcXVpcmVkCkB1c2VyX3Bhc3Nlc190ZXN0KGxhbWJkYSB1OiB1LmlzX3N1cGVydXNlcikKZGVmIGFkbWluX2h1YihyZXF1ZXN0KToKICAgICIiIlB1bnRvIGRlIGVudHJhZGEgbGVnYWRvOiByZWRpcmlnZSBhbCB0YWJsZXJvIG1lbnN1YWwuIiIiCiAgICBwZXJpb2QgPSBwYXJzZV9hZG1pbl9wZXJpb2QocmVxdWVzdCkKICAgIHJldHVybiByZWRpcmVjdChmIntyZXZlcnNlKCdwZ2M6YWRtaW5fbW9udGhseScpfT97cGVyaW9kLnF1ZXJ5c3RyaW5nKCl9IikKCgpAbG9naW5fcmVxdWlyZWQKQHVzZXJfcGFzc2VzX3Rlc3QobGFtYmRhIHU6IHUuaXNfc3VwZXJ1c2VyKQpkZWYgYWRtaW5fbW9udGhseShyZXF1ZXN0KToKICAgIHBlcmlvZCA9IHBhcnNlX2FkbWluX3BlcmlvZChyZXF1ZXN0KQogICAgeWVhciwgbW9udGggPSBwZXJpb2QueWVhciwgcGVyaW9kLm1vbnRoCiAgICBzZWxlY3RlZF9ibG9jayA9IChyZXF1ZXN0LkdFVC5nZXQoImJsb2NrIikgb3IgcmVxdWVzdC5QT1NULmdldCgiYmxvY2siKSBvciBCTE9DS19PUkRFUlswXSkuc3RyaXAoKQoKICAgIGlmIHJlcXVlc3QubWV0aG9kID09ICJQT1NUIjoKICAgICAgICBhY3Rpb24gPSAocmVxdWVzdC5QT1NULmdldCgiYWN0aW9uIikgb3IgIiIpLnN0cmlwKCkKCiAgICAgICAgaWYgYWN0aW9uID09ICJyZWNhbGN1bGF0ZV9wZXJpb2QiOgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICBmb3IgbXNnIGluIHJlY2FsY3VsYXRlX3BlcmlvZCh5ZWFyLCBtb250aCk6CiAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMuc3VjY2VzcyhyZXF1ZXN0LCBtc2cpCiAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZXhjOgogICAgICAgICAgICAgICAgbWVzc2FnZXMuZXJyb3IocmVxdWVzdCwgZiJFcnJvciBhbCByZWNhbGN1bGFyIHBlcsOtb2RvOiB7ZXhjfSIpCiAgICAgICAgICAgIHJldHVybiByZWRpcmVjdF9hZG1pbl9tb250aGx5KHBlcmlvZD1wZXJpb2QsIGJsb2NrPXNlbGVjdGVkX2Jsb2NrKQoKICAgICAgICBpZiBhY3Rpb24gPT0gInJlY2FsY3VsYXRlX2Jsb2NrIjoKICAgICAgICAgICAgYmxvY2sgPSByZXF1ZXN0LlBPU1QuZ2V0KCJibG9jayIpIG9yIHNlbGVjdGVkX2Jsb2NrCiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIGZvciBtc2cgaW4gcmVjYWxjdWxhdGVfYmxvY2soeWVhciwgbW9udGgsIGJsb2NrKToKICAgICAgICAgICAgICAgICAgICBtZXNzYWdlcy5zdWNjZXNzKHJlcXVlc3QsIG1zZykKICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBleGM6CiAgICAgICAgICAgICAgICBtZXNzYWdlcy5lcnJvcihyZXF1ZXN0LCBmIkVycm9yIGFsIHJlY2FsY3VsYXIgYmxvcXVlOiB7ZXhjfSIpCiAgICAgICAgICAgIHJldHVybiByZWRpcmVjdF9hZG1pbl9tb250aGx5KHBlcmlvZD1wZXJpb2QsIGJsb2NrPWJsb2NrKQoKICAgICAgICBpZiBhY3Rpb24gPT0gInVwbG9hZCI6CiAgICAgICAgICAgIGJsb2NrID0gcmVxdWVzdC5QT1NULmdldCgiYmxvY2siKSBvciBzZWxlY3RlZF9ibG9jawogICAgICAgICAgICB0eXBlX21hcCA9IHsKICAgICAgICAgICAgICAgIEJMT0NLX0ZJTkFOQ0lBTDogRmlsZVVwbG9hZC5UWVBFX0ZJTkFOQ0lBTCwKICAgICAgICAgICAgICAgIEJMT0NLX05FV19DTElFTlRTOiBGaWxlVXBsb2FkLlRZUEVfTkVXX0NMSUVOVFMsCiAgICAgICAgICAgICAgICBCTE9DS19DUk9TU19TQUxFOiBGaWxlVXBsb2FkLlRZUEVfQ1JPU1NfU0FMRSwKICAgICAgICAgICAgfQogICAgICAgICAgICBfc2F2ZV91cGxvYWQocmVxdWVzdCwgeWVhciwgbW9udGgsIHR5cGVfbWFwLmdldChibG9jaykpCiAgICAgICAgICAgIHJldHVybiByZWRpcmVjdF9hZG1pbl9tb250aGx5KHBlcmlvZD1wZXJpb2QsIGJsb2NrPWJsb2NrKQoKICAgICAgICBpZiBhY3Rpb24gPT0gInByb2Nlc3MiOgogICAgICAgICAgICBibG9jayA9IHJlcXVlc3QuUE9TVC5nZXQoImJsb2NrIikgb3Igc2VsZWN0ZWRfYmxvY2sKICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgZmlsZV9pZCA9IGludChyZXF1ZXN0LlBPU1QuZ2V0KCJmaWxlX2lkIikgb3IgIjAiKQogICAgICAgICAgICBleGNlcHQgKFR5cGVFcnJvciwgVmFsdWVFcnJvcik6CiAgICAgICAgICAgICAgICBmaWxlX2lkID0gMAogICAgICAgICAgICB1cGxvYWQgPSBGaWxlVXBsb2FkLm9iamVjdHMuZmlsdGVyKGlkPWZpbGVfaWQpLmZpcnN0KCkKICAgICAgICAgICAgaWYgbm90IHVwbG9hZDoKICAgICAgICAgICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsICJBcmNoaXZvIG5vIGVuY29udHJhZG8uIikKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIF9wcm9jZXNzX3VwbG9hZChyZXF1ZXN0LCB1cGxvYWQsIHllYXIsIG1vbnRoLCBibG9jaykKICAgICAgICAgICAgcmV0dXJuIHJlZGlyZWN0X2FkbWluX21vbnRobHkocGVyaW9kPXBlcmlvZCwgYmxvY2s9YmxvY2spCgogICAgICAgIGlmIGFjdGlvbiA9PSAiZGlzY2FyZF9wZW5kaW5nIjoKICAgICAgICAgICAgYmxvY2sgPSByZXF1ZXN0LlBPU1QuZ2V0KCJibG9jayIpIG9yIHNlbGVjdGVkX2Jsb2NrCiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIGZpbGVfaWQgPSBpbnQocmVxdWVzdC5QT1NULmdldCgiZmlsZV9pZCIpIG9yICIwIikKICAgICAgICAgICAgZXhjZXB0IChUeXBlRXJyb3IsIFZhbHVlRXJyb3IpOgogICAgICAgICAgICAgICAgZmlsZV9pZCA9IDAKICAgICAgICAgICAgdXBsb2FkID0gRmlsZVVwbG9hZC5vYmplY3RzLmZpbHRlcihpZD1maWxlX2lkKS5maXJzdCgpCiAgICAgICAgICAgIGlmIG5vdCB1cGxvYWQ6CiAgICAgICAgICAgICAgICBtZXNzYWdlcy5lcnJvcihyZXF1ZXN0LCAiQXJjaGl2byBubyBlbmNvbnRyYWRvLiIpCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgcmVzdWx0ID0gZGlzY2FyZF9wZW5kaW5nX3VwbG9hZCh1cGxvYWQpCiAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMuc3VjY2VzcygKICAgICAgICAgICAgICAgICAgICAgICAgcmVxdWVzdCwKICAgICAgICAgICAgICAgICAgICAgICAgZiJTZSBxdWl0w7MgZGUgbGEgY29sYToge3Jlc3VsdFsnZmlsZW5hbWUnXX0uICIKICAgICAgICAgICAgICAgICAgICAgICAgIkxvcyBkYXRvcyB5YSBwcm9jZXNhZG9zIG5vIHNlIG1vZGlmaWNhcm9uLiIsCiAgICAgICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgZXhjZXB0IFZhbHVlRXJyb3IgYXMgZXhjOgogICAgICAgICAgICAgICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsIHN0cihleGMpKQogICAgICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBleGM6CiAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMuZXJyb3IocmVxdWVzdCwgZiJObyBzZSBwdWRvIHF1aXRhciBlbCBhcmNoaXZvIGRlIGxhIGNvbGE6IHtleGN9IikKICAgICAgICAgICAgcmV0dXJuIHJlZGlyZWN0X2FkbWluX21vbnRobHkocGVyaW9kPXBlcmlvZCwgYmxvY2s9YmxvY2spCgogICAgICAgIGlmIGFjdGlvbiA9PSAiZGVkdXBfbmV3X2NsaWVudHMiOgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICByZXN1bHQgPSByZW1vdmVfZHVwbGljYXRlX25ld19jbGllbnRfcm93cyh5ZWFyLCBtb250aCwgdXNlcj1yZXF1ZXN0LnVzZXIpCiAgICAgICAgICAgICAgICBpZiByZXN1bHRbInJlbW92ZWQiXToKICAgICAgICAgICAgICAgICAgICBtZXNzYWdlcy5zdWNjZXNzKAogICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0LAogICAgICAgICAgICAgICAgICAgICAgICBmIlNlIGVsaW1pbmFyb24ge3Jlc3VsdFsncmVtb3ZlZCddfSByZWdpc3RybyhzKSBkdXBsaWNhZG8ocykgIgogICAgICAgICAgICAgICAgICAgICAgICBmInkgc2UgYWN0dWFsaXphcm9uIHtyZXN1bHRbJ21ldHJpY3NfdXBkYXRlZCddfSBtw6l0cmljYShzKSBkZSBjbGllbnRlcyBudWV2b3MuIiwKICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgICAgIG1lc3NhZ2VzLmluZm8ocmVxdWVzdCwgIk5vIHNlIGVuY29udHJhcm9uIGR1cGxpY2Fkb3MgZW4gZWwgZGV0YWxsZSBkZSBjbGllbnRlcy4iKQogICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGV4YzoKICAgICAgICAgICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsIGYiRXJyb3IgYWwgZWxpbWluYXIgZHVwbGljYWRvczoge2V4Y30iKQogICAgICAgICAgICByZXR1cm4gcmVkaXJlY3RfYWRtaW5fbW9udGhseShwZXJpb2Q9cGVyaW9kLCBibG9jaz1CTE9DS19ORVdfQ0xJRU5UUykKCiAgICBzbmFwc2hvdCA9IGdldF9hZG1pbl9wZXJpb2Rfc25hcHNob3QoeWVhciwgbW9udGgpCiAgICBpZiBzZWxlY3RlZF9ibG9jayBub3QgaW4gc25hcHNob3RbImJsb2Nrc19ieV9pZCJdOgogICAgICAgIHNlbGVjdGVkX2Jsb2NrID0gQkxPQ0tfT1JERVJbMF0KCiAgICBjb250ZXh0ID0gewogICAgICAgICoqYWRtaW5fcGVyaW9kX2NvbnRleHQocGVyaW9kKSwKICAgICAgICAic25hcHNob3QiOiBzbmFwc2hvdCwKICAgICAgICAic2VsZWN0ZWRfYmxvY2siOiBzZWxlY3RlZF9ibG9jaywKICAgICAgICAiYmxvY2tfZGV0YWlsIjogc25hcHNob3RbImJsb2Nrc19ieV9pZCJdW3NlbGVjdGVkX2Jsb2NrXSwKICAgICAgICAiYmxvY2tfb3JkZXIiOiBCTE9DS19PUkRFUiwKICAgICAgICAiYmxvY2tfbWV0YSI6IEJMT0NLX01FVEEsCiAgICAgICAgInVwbG9hZF9mb3JtIjogRmlsZVVwbG9hZEZvcm0oKSwKICAgICAgICAicmVjZW50X2xvZyI6IGxpc3RfcGVyaW9kX2xvZyh5ZWFyLCBtb250aCwgbGltaXQ9OCwgbW9udGhfZnJvbT1wZXJpb2QubW9udGhfZnJvbSksCiAgICAgICAgInN1cHBvcnRzX21vbnRoX3JhbmdlIjogRmFsc2UsCiAgICAgICAgInNpbmdsZV9tb250aF9vcHMiOiBUcnVlLAogICAgfQogICAgcmV0dXJuIHJlbmRlcihyZXF1ZXN0LCAicGdjL2FkbWluX21vbnRobHkuaHRtbCIsIGNvbnRleHQpCgoKQGxvZ2luX3JlcXVpcmVkCkB1c2VyX3Bhc3Nlc190ZXN0KGxhbWJkYSB1OiB1LmlzX3N1cGVydXNlcikKZGVmIGFkbWluX21hbnVhbF9lZGl0KHJlcXVlc3QpOgogICAgcGVyaW9kID0gcGFyc2VfYWRtaW5fcGVyaW9kKHJlcXVlc3QpCiAgICB5ZWFyLCBtb250aCA9IHBlcmlvZC55ZWFyLCBwZXJpb2QubW9udGgKICAgIHRhYiA9IChyZXF1ZXN0LkdFVC5nZXQoInRhYiIpIG9yIHJlcXVlc3QuUE9TVC5nZXQoInRhYiIpIG9yICJ0YXJnZXRzIikuc3RyaXAoKQoKICAgIGlmIHJlcXVlc3QubWV0aG9kID09ICJQT1NUIjoKICAgICAgICBhY3Rpb24gPSAocmVxdWVzdC5QT1NULmdldCgiYWN0aW9uIikgb3IgIiIpLnN0cmlwKCkKICAgICAgICByZWFzb24gPSAocmVxdWVzdC5QT1NULmdldCgicmVhc29uIikgb3IgIiIpLnN0cmlwKCkKICAgICAgICByZWNhbGNfYWZ0ZXIgPSByZXF1ZXN0LlBPU1QuZ2V0KCJyZWNhbGNfYWZ0ZXIiKSA9PSAiMSIKCiAgICAgICAgdHJ5OgogICAgICAgICAgICBjaGFuZ2VzID0gMAogICAgICAgICAgICBpZiBhY3Rpb24gPT0gInNhdmVfdGFyZ2V0cyI6CiAgICAgICAgICAgICAgICBjaGFuZ2VzID0gc2F2ZV90YXJnZXRzKHJlcXVlc3QudXNlciwgeWVhciwgbW9udGgsIHJlcXVlc3QuUE9TVCwgcmVhc29uKQogICAgICAgICAgICBlbGlmIGFjdGlvbiA9PSAic2F2ZV9yZXN1bHRzIjoKICAgICAgICAgICAgICAgIGNoYW5nZXMgPSBzYXZlX3Jlc3VsdHMocmVxdWVzdC51c2VyLCB5ZWFyLCBtb250aCwgcmVxdWVzdC5QT1NULCByZWFzb24pCiAgICAgICAgICAgIGVsaWYgYWN0aW9uID09ICJyZWNhbGNfc3RhbGVfaW5ncmVzb3MiOgogICAgICAgICAgICAgICAgcmVzdWx0ID0gcmVjYWxjX3N0YWxlX2luZ3Jlc29zKAogICAgICAgICAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgICAgICAgICBtb250aD1tb250aCwKICAgICAgICAgICAgICAgICAgICB1c2VyPXJlcXVlc3QudXNlciwKICAgICAgICAgICAgICAgICAgICByZWFzb249cmVhc29uIG9yICJSZWPDoWxjdWxvIGRlIGluZ3Jlc29zIFNUQUxFIGRlc2RlIGFkbWluIiwKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIGNoYW5nZXMgPSByZXN1bHRbInVwZGF0ZWQiXQogICAgICAgICAgICAgICAgaWYgY2hhbmdlczoKICAgICAgICAgICAgICAgICAgICBtZXNzYWdlcy5zdWNjZXNzKAogICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0LAogICAgICAgICAgICAgICAgICAgICAgICBmIlNlIHJlY2FsY3VsYXJvbiB7Y2hhbmdlc30gaW5ncmVzbyhzKSBjb24gVEM9e3Jlc3VsdFsnZngnXX0uIiwKICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAgICAgaWYgcmVjYWxjX2FmdGVyOgogICAgICAgICAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBmb3IgbXNnIGluIHJlY2FsY3VsYXRlX3BlcmlvZCh5ZWFyLCBtb250aCk6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMuc3VjY2VzcyhyZXF1ZXN0LCBtc2cpCiAgICAgICAgICAgICAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZXhjOgogICAgICAgICAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMud2FybmluZygKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0LAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGYiUmVjw6FsY3VsbyBkZSBpbmdyZXNvcyBsaXN0bywgcGVybyBmYWxsw7MgZWwgc2NvcmU6IHtleGN9IiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgICAgICByZXR1cm4gcmVkaXJlY3RfYWRtaW5fbWFudWFsKHBlcmlvZD1wZXJpb2QsIHRhYj10YWIpCiAgICAgICAgICAgICAgICBtZXNzYWdlcy5pbmZvKHJlcXVlc3QsICJObyBoYXkgaW5ncmVzb3MgU1RBTEUgcGFyYSByZWNhbGN1bGFyLiIpCiAgICAgICAgICAgICAgICByZXR1cm4gcmVkaXJlY3RfYWRtaW5fbWFudWFsKHBlcmlvZD1wZXJpb2QsIHRhYj10YWIpCiAgICAgICAgICAgIGVsaWYgYWN0aW9uID09ICJzYXZlX3JlcXVpcmVtZW50cyI6CiAgICAgICAgICAgICAgICBjaGFuZ2VzID0gc2F2ZV9yZXF1aXJlbWVudHMocmVxdWVzdC51c2VyLCB5ZWFyLCBtb250aCwgcmVxdWVzdC5QT1NULCByZWFzb24pCiAgICAgICAgICAgIGVsaWYgYWN0aW9uID09ICJzYXZlX2Z4IjoKICAgICAgICAgICAgICAgIGNoYW5nZXMgPSBzYXZlX2Z4KAogICAgICAgICAgICAgICAgICAgIHJlcXVlc3QudXNlciwKICAgICAgICAgICAgICAgICAgICB5ZWFyLAogICAgICAgICAgICAgICAgICAgIG1vbnRoLAogICAgICAgICAgICAgICAgICAgIHJlcXVlc3QuUE9TVCwKICAgICAgICAgICAgICAgICAgICByZWFzb24sCiAgICAgICAgICAgICAgICAgICAgbW9udGhfZnJvbT1wZXJpb2QubW9udGhfZnJvbSwKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgZWxpZiBhY3Rpb24gPT0gInNhdmVfYWxpYXMiOgogICAgICAgICAgICAgICAgY2hhbmdlcyA9IHNhdmVfYWxpYXMocmVxdWVzdC51c2VyLCB5ZWFyLCBtb250aCwgcmVxdWVzdC5QT1NULCByZWFzb24pCiAgICAgICAgICAgIGVsaWYgYWN0aW9uID09ICJzYXZlX2FsaWFzZXNfYnVsayI6CiAgICAgICAgICAgICAgICBjaGFuZ2VzID0gc2F2ZV9hbGlhc2VzX2J1bGsocmVxdWVzdC51c2VyLCB5ZWFyLCBtb250aCwgcmVxdWVzdC5QT1NULCByZWFzb24pCiAgICAgICAgICAgIGVsaWYgYWN0aW9uID09ICJzYXZlX2ltcG9ydHMiOgogICAgICAgICAgICAgICAgY2hhbmdlcyA9IHNhdmVfaW1wb3J0X3Jvd3MoCiAgICAgICAgICAgICAgICAgICAgcmVxdWVzdC51c2VyLAogICAgICAgICAgICAgICAgICAgIHllYXIsCiAgICAgICAgICAgICAgICAgICAgbW9udGgsCiAgICAgICAgICAgICAgICAgICAgcmVxdWVzdC5QT1NULAogICAgICAgICAgICAgICAgICAgIHJlYXNvbiwKICAgICAgICAgICAgICAgICAgICBtb250aF9mcm9tPXBlcmlvZC5tb250aF9mcm9tLAogICAgICAgICAgICAgICAgKQogICAgICAgICAgICBlbGlmIGFjdGlvbiA9PSAic2F2ZV9ub3RlcyI6CiAgICAgICAgICAgICAgICBjaGFuZ2VzID0gc2F2ZV9wZXJpb2Rfbm90ZShyZXF1ZXN0LnVzZXIsIHllYXIsIG1vbnRoLCByZXF1ZXN0LlBPU1QsIHJlYXNvbikKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsICJBY2Npw7NuIG5vIHJlY29ub2NpZGEuIikKICAgICAgICAgICAgICAgIHJldHVybiByZWRpcmVjdF9hZG1pbl9tYW51YWwocGVyaW9kPXBlcmlvZCwgdGFiPXRhYikKCiAgICAgICAgICAgIGlmIGNoYW5nZXM6CiAgICAgICAgICAgICAgICBtZXNzYWdlcy5zdWNjZXNzKHJlcXVlc3QsIGYiU2UgZ3VhcmRhcm9uIHtjaGFuZ2VzfSBjYW1iaW8ocykuIikKICAgICAgICAgICAgICAgIGlmIHJlY2FsY19hZnRlcjoKICAgICAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgICAgIGZvciBtc2cgaW4gcmVjYWxjdWxhdGVfcGVyaW9kKHllYXIsIG1vbnRoKToKICAgICAgICAgICAgICAgICAgICAgICAgICAgIG1lc3NhZ2VzLnN1Y2Nlc3MocmVxdWVzdCwgbXNnKQogICAgICAgICAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZXhjOgogICAgICAgICAgICAgICAgICAgICAgICBtZXNzYWdlcy53YXJuaW5nKHJlcXVlc3QsIGYiQ2FtYmlvcyBndWFyZGFkb3MsIHBlcm8gZmFsbMOzIGVsIHJlY8OhbGN1bG86IHtleGN9IikKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIG1lc3NhZ2VzLmluZm8ocmVxdWVzdCwgIk5vIGh1Ym8gY2FtYmlvcyBxdWUgZ3VhcmRhci4iKQogICAgICAgIGV4Y2VwdCBWYWx1ZUVycm9yIGFzIGV4YzoKICAgICAgICAgICAgbWVzc2FnZXMuZXJyb3IocmVxdWVzdCwgc3RyKGV4YykpCiAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBleGM6CiAgICAgICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsIGYiRXJyb3IgYWwgZ3VhcmRhcjoge2V4Y30iKQoKICAgICAgICByZXR1cm4gcmVkaXJlY3RfYWRtaW5fbWFudWFsKHBlcmlvZD1wZXJpb2QsIHRhYj10YWIpCgogICAgY29udGV4dCA9IHsKICAgICAgICAqKmFkbWluX3BlcmlvZF9jb250ZXh0KHBlcmlvZCksCiAgICAgICAgKipnZXRfbWFudWFsX2VkaXRfY29udGV4dCh5ZWFyLCBtb250aCwgdGFiLCBtb250aF9mcm9tPXBlcmlvZC5tb250aF9mcm9tKSwKICAgIH0KICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgInBnYy9hZG1pbl9tYW51YWxfZWRpdC5odG1sIiwgY29udGV4dCkKCgpAbG9naW5fcmVxdWlyZWQKQHVzZXJfcGFzc2VzX3Rlc3QobGFtYmRhIHU6IHUuaXNfc3VwZXJ1c2VyKQpkZWYgYWRtaW5faW5ncmVzb3NfeWVhcihyZXF1ZXN0KToKICAgICIiIk1hdHJpeiBhbnVhbDogMTIgbWVzZXMgw5cgNCBVTkVzICsgVEMgKGNhcHR1cmEgZGUgaW5ncmVzb3MgcmVhbGVzKS4iIiIKICAgIHBlcmlvZCA9IHBhcnNlX2FkbWluX3BlcmlvZChyZXF1ZXN0KQogICAgeWVhciA9IHBlcmlvZC55ZWFyCiAgICBjYXB0dXJlX2N1cnJlbmN5ID0gKHJlcXVlc3QuR0VULmdldCgiY3VyciIpIG9yIHJlcXVlc3QuUE9TVC5nZXQoImNhcHR1cmVfY3VycmVuY3kiKSBvciAiR1RRIikuc3RyaXAoKQoKICAgIGlmIHJlcXVlc3QubWV0aG9kID09ICJQT1NUIjoKICAgICAgICBhY3Rpb24gPSAocmVxdWVzdC5QT1NULmdldCgiYWN0aW9uIikgb3IgIiIpLnN0cmlwKCkKICAgICAgICByZWFzb24gPSAocmVxdWVzdC5QT1NULmdldCgicmVhc29uIikgb3IgIiIpLnN0cmlwKCkKICAgICAgICByZWNhbGNfYWZ0ZXIgPSByZXF1ZXN0LlBPU1QuZ2V0KCJyZWNhbGNfYWZ0ZXIiKSA9PSAiMSIKICAgICAgICBjYXB0dXJlX2N1cnJlbmN5ID0gKHJlcXVlc3QuUE9TVC5nZXQoImNhcHR1cmVfY3VycmVuY3kiKSBvciBjYXB0dXJlX2N1cnJlbmN5KS5zdHJpcCgpCgogICAgICAgIGlmIGFjdGlvbiA9PSAic2F2ZV9pbmdyZXNvc195ZWFyIjoKICAgICAgICAgICAgaW5nX2tleXMgPSBzb3J0ZWQoayBmb3IgayBpbiByZXF1ZXN0LlBPU1QgaWYgay5zdGFydHN3aXRoKCJpbmdfIikpCiAgICAgICAgICAgIGZ4X2tleXMgPSBzb3J0ZWQoayBmb3IgayBpbiByZXF1ZXN0LlBPU1QgaWYgay5zdGFydHN3aXRoKCJmeF8iKSkKICAgICAgICAgICAgbG9nZ2VyLndhcm5pbmcoCiAgICAgICAgICAgICAgICAiaW5ncmVzb3NfeWVhciBQT1NUIHllYXI9JXMgY3Vycj0lcyByZWFzb25fbGVuPSVzICIKICAgICAgICAgICAgICAgICJpbmdfbm9uZW1wdHk9JXMgZnhfbm9uZW1wdHk9JXMgaW5nX3NhbXBsZT0lcyBmeF9zYW1wbGU9JXMiLAogICAgICAgICAgICAgICAgeWVhciwKICAgICAgICAgICAgICAgIGNhcHR1cmVfY3VycmVuY3ksCiAgICAgICAgICAgICAgICBsZW4ocmVhc29uKSwKICAgICAgICAgICAgICAgIHN1bSgxIGZvciBrIGluIGluZ19rZXlzIGlmIChyZXF1ZXN0LlBPU1QuZ2V0KGspIG9yICIiKS5zdHJpcCgpKSwKICAgICAgICAgICAgICAgIHN1bSgxIGZvciBrIGluIGZ4X2tleXMgaWYgKHJlcXVlc3QuUE9TVC5nZXQoaykgb3IgIiIpLnN0cmlwKCkpLAogICAgICAgICAgICAgICAgWyhrLCByZXF1ZXN0LlBPU1QuZ2V0KGspKSBmb3IgayBpbiBpbmdfa2V5cyBpZiAocmVxdWVzdC5QT1NULmdldChrKSBvciAiIikuc3RyaXAoKV1bOjhdLAogICAgICAgICAgICAgICAgWyhrLCByZXF1ZXN0LlBPU1QuZ2V0KGspKSBmb3IgayBpbiBmeF9rZXlzIGlmIChyZXF1ZXN0LlBPU1QuZ2V0KGspIG9yICIiKS5zdHJpcCgpXVs6OF0sCiAgICAgICAgICAgICkKICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgcmVzdWx0ID0gc2F2ZV9pbmdyZXNvc195ZWFyKHJlcXVlc3QudXNlciwgeWVhciwgcmVxdWVzdC5QT1NULCByZWFzb24pCiAgICAgICAgICAgICAgICBpbmNvbWVfbiA9IHJlc3VsdFsiaW5jb21lX2NoYW5nZXMiXQogICAgICAgICAgICAgICAgZnhfbiA9IHJlc3VsdFsiZnhfY2hhbmdlcyJdCiAgICAgICAgICAgICAgICBsb2dnZXIud2FybmluZygKICAgICAgICAgICAgICAgICAgICAiaW5ncmVzb3NfeWVhciByZXN1bHQgeWVhcj0lcyBpbmNvbWVfY2hhbmdlcz0lcyBmeF9jaGFuZ2VzPSVzIGN1cnJlbmN5PSVzIiwKICAgICAgICAgICAgICAgICAgICB5ZWFyLAogICAgICAgICAgICAgICAgICAgIGluY29tZV9uLAogICAgICAgICAgICAgICAgICAgIGZ4X24sCiAgICAgICAgICAgICAgICAgICAgcmVzdWx0WyJjdXJyZW5jeSJdLAogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgaWYgaW5jb21lX246CiAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMuc3VjY2VzcygKICAgICAgICAgICAgICAgICAgICAgICAgcmVxdWVzdCwKICAgICAgICAgICAgICAgICAgICAgICAgZiJHdWFyZGFkbzoge2luY29tZV9ufSBpbmdyZXNvKHMpLCB7Znhfbn0gVEM7ICIKICAgICAgICAgICAgICAgICAgICAgICAgZiJtb25lZGEgY2FwdHVyYT17cmVzdWx0WydjdXJyZW5jeSddfS4iLAogICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgICAgICBpZiByZWNhbGNfYWZ0ZXI6CiAgICAgICAgICAgICAgICAgICAgICAgICMgUmVjYWxjdWxhIHNjb3JlIGRlbCBtZXMgZm9jbyBkZWwgc2VsZWN0b3IgKG5vIGxvcyAxMikuCiAgICAgICAgICAgICAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGZvciBtc2cgaW4gcmVjYWxjdWxhdGVfcGVyaW9kKHllYXIsIHBlcmlvZC5tb250aCk6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMuc3VjY2VzcyhyZXF1ZXN0LCBtc2cpCiAgICAgICAgICAgICAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZXhjOgogICAgICAgICAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMud2FybmluZygKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0LAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGYiSW5ncmVzb3MgZ3VhcmRhZG9zLCBwZXJvIGZhbGzDsyBlbCBzY29yZSBkZSAiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZiJ7eWVhcn0te3BlcmlvZC5tb250aDowMmR9OiB7ZXhjfSIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICBlbGlmIGZ4X246CiAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMud2FybmluZygKICAgICAgICAgICAgICAgICAgICAgICAgcmVxdWVzdCwKICAgICAgICAgICAgICAgICAgICAgICAgZiJTb2xvIHNlIGd1YXJkYXJvbiB7Znhfbn0gdGlwbyhzKSBkZSBjYW1iaW8uICIKICAgICAgICAgICAgICAgICAgICAgICAgIk5vIGxsZWfDsyBuaW5nw7puIHZhbG9yIGRlIGluZ3Jlc28gZW4gZWwgUE9TVCAiCiAgICAgICAgICAgICAgICAgICAgICAgICIoY2VsZGFzIHZhY8OtYXMgbyBubyBlbnZpYWRhcykuIENvbXBsZXRlIGluZ3Jlc29zIHkgdnVlbHZhIGEgR3VhcmRhci4iLAogICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMud2FybmluZygKICAgICAgICAgICAgICAgICAgICAgICAgcmVxdWVzdCwKICAgICAgICAgICAgICAgICAgICAgICAgIlNpbiBjYW1iaW9zOiBubyBzZSByZWNpYmllcm9uIGluZ3Jlc29zIG5pIHRpcG9zIGRlIGNhbWJpbyAiCiAgICAgICAgICAgICAgICAgICAgICAgICJjb24gdmFsb3IgbnVldm8uIFJldmlzZSBlbCBmb3JtdWxhcmlvIHkgZWwgbW90aXZvLCBsdWVnbyByZWludGVudGUuIiwKICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZXhjOgogICAgICAgICAgICAgICAgbG9nZ2VyLndhcm5pbmcoImluZ3Jlc29zX3llYXIgc2F2ZSBmYWlsZWQgeWVhcj0lcyBlcnI9JXMiLCB5ZWFyLCBleGMpCiAgICAgICAgICAgICAgICBtZXNzYWdlcy5lcnJvcihyZXF1ZXN0LCBzdHIoZXhjKSkKICAgICAgICAgICAgcmV0dXJuIHJlZGlyZWN0X2FkbWluX2luZ3Jlc29zX3llYXIoCiAgICAgICAgICAgICAgICBwZXJpb2Q9cGVyaW9kLCBjdXJyPWNhcHR1cmVfY3VycmVuY3kKICAgICAgICAgICAgKQoKICAgIGNvbnRleHQgPSB7CiAgICAgICAgKiphZG1pbl9wZXJpb2RfY29udGV4dChwZXJpb2QpLAogICAgICAgICoqZ2V0X2luZ3Jlc29zX3llYXJfY29udGV4dCh5ZWFyLCBjYXB0dXJlX2N1cnJlbmN5PWNhcHR1cmVfY3VycmVuY3kpLAogICAgICAgICJzdXBwb3J0c19tb250aF9yYW5nZSI6IEZhbHNlLAogICAgICAgICJzaW5nbGVfbW9udGhfb3BzIjogRmFsc2UsCiAgICB9CiAgICByZXR1cm4gcmVuZGVyKHJlcXVlc3QsICJwZ2MvYWRtaW5faW5ncmVzb3NfeWVhci5odG1sIiwgY29udGV4dCkKCgpAbG9naW5fcmVxdWlyZWQKQHVzZXJfcGFzc2VzX3Rlc3QobGFtYmRhIHU6IHUuaXNfc3VwZXJ1c2VyKQpkZWYgYWRtaW5fbW9udGhseV9sb2cocmVxdWVzdCk6CiAgICBwZXJpb2QgPSBwYXJzZV9hZG1pbl9wZXJpb2QocmVxdWVzdCkKICAgIHllYXIsIG1vbnRoID0gcGVyaW9kLnllYXIsIHBlcmlvZC5tb250aAogICAgZW50cmllcyA9IGxpc3RfcGVyaW9kX2xvZyh5ZWFyLCBtb250aCwgbGltaXQ9MTUwLCBtb250aF9mcm9tPXBlcmlvZC5tb250aF9mcm9tKQogICAgc25hcHNob3QgPSBnZXRfYWRtaW5fcGVyaW9kX3NuYXBzaG90KHllYXIsIG1vbnRoKQoKICAgIGNvbnRleHQgPSB7CiAgICAgICAgKiphZG1pbl9wZXJpb2RfY29udGV4dChwZXJpb2QpLAogICAgICAgICJwZXJpb2RfbGFiZWwiOiBwZXJpb2QubGFiZWwsCiAgICAgICAgImVudHJpZXMiOiBlbnRyaWVzLAogICAgICAgICJzbmFwc2hvdCI6IHNuYXBzaG90LAogICAgICAgICJzdXBwb3J0c19tb250aF9yYW5nZSI6IFRydWUsCiAgICAgICAgInNpbmdsZV9tb250aF9vcHMiOiBGYWxzZSwKICAgIH0KICAgIHJldHVybiByZW5kZXIocmVxdWVzdCwgInBnYy9hZG1pbl9tb250aGx5X2xvZy5odG1sIiwgY29udGV4dCkKCgpAbG9naW5fcmVxdWlyZWQKQHVzZXJfcGFzc2VzX3Rlc3QobGFtYmRhIHU6IHUuaXNfc3VwZXJ1c2VyKQpkZWYgYWRtaW5fbmV3X2NsaWVudHNfYnJvd3NlKHJlcXVlc3QpOgogICAgcGVyaW9kID0gcGFyc2VfYWRtaW5fcGVyaW9kKHJlcXVlc3QpCgogICAgaWYgcmVxdWVzdC5tZXRob2QgPT0gIlBPU1QiOgogICAgICAgIHJlYXNvbiA9IChyZXF1ZXN0LlBPU1QuZ2V0KCJyZWFzb24iKSBvciAiIikuc3RyaXAoKQogICAgICAgIHJlY2FsY19hZnRlciA9IHJlcXVlc3QuUE9TVC5nZXQoInJlY2FsY19hZnRlciIpID09ICIxIgogICAgICAgIHRyeToKICAgICAgICAgICAgcmVzdWx0ID0gc2F2ZV9icm93c2Vfcm93cyhyZXF1ZXN0LnVzZXIsIHBlcmlvZCwgcmVxdWVzdC5QT1NULCByZWFzb24pCiAgICAgICAgICAgIGlmIHJlc3VsdFsidG90YWwiXToKICAgICAgICAgICAgICAgIHBhcnRzID0gW10KICAgICAgICAgICAgICAgIGlmIHJlc3VsdFsidXBkYXRlZCJdOgogICAgICAgICAgICAgICAgICAgIHBhcnRzLmFwcGVuZChmIntyZXN1bHRbJ3VwZGF0ZWQnXX0gZWRpdGFkbyhzKSIpCiAgICAgICAgICAgICAgICBpZiByZXN1bHRbImRlbGV0ZWQiXToKICAgICAgICAgICAgICAgICAgICBwYXJ0cy5hcHBlbmQoZiJ7cmVzdWx0WydkZWxldGVkJ119IGVsaW1pbmFkbyhzKSIpCiAgICAgICAgICAgICAgICBpZiByZXN1bHRbImNyZWF0ZWQiXToKICAgICAgICAgICAgICAgICAgICBwYXJ0cy5hcHBlbmQoZiJ7cmVzdWx0WydjcmVhdGVkJ119IGNyZWFkbyhzKSIpCiAgICAgICAgICAgICAgICBtZXNzYWdlcy5zdWNjZXNzKAogICAgICAgICAgICAgICAgICAgIHJlcXVlc3QsCiAgICAgICAgICAgICAgICAgICAgZiJHdWFyZGFkbzogeycsICcuam9pbihwYXJ0cyl9LiAiCiAgICAgICAgICAgICAgICAgICAgZiJNw6l0cmljYXMgYWN0dWFsaXphZGFzOiB7cmVzdWx0WydtZXRyaWNzX3VwZGF0ZWQnXX0uIiwKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIGlmIHJlY2FsY19hZnRlcjoKICAgICAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgICAgIGZvciBtc2cgaW4gcmVjYWxjdWxhdGVfYmxvY2soCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBwZXJpb2QueWVhciwgcGVyaW9kLm1vbnRoLCBCTE9DS19ORVdfQ0xJRU5UUwogICAgICAgICAgICAgICAgICAgICAgICApOgogICAgICAgICAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMuc3VjY2VzcyhyZXF1ZXN0LCBtc2cpCiAgICAgICAgICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBleGM6CiAgICAgICAgICAgICAgICAgICAgICAgIG1lc3NhZ2VzLndhcm5pbmcoCiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0LAogICAgICAgICAgICAgICAgICAgICAgICAgICAgZiJDYW1iaW9zIGd1YXJkYWRvcywgcGVybyBmYWxsw7MgZWwgcmVjw6FsY3Vsbzoge2V4Y30iLAogICAgICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBtZXNzYWdlcy5pbmZvKHJlcXVlc3QsICJObyBodWJvIGNhbWJpb3MgcXVlIGd1YXJkYXIuIikKICAgICAgICBleGNlcHQgVmFsdWVFcnJvciBhcyBleGM6CiAgICAgICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsIHN0cihleGMpKQogICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZXhjOgogICAgICAgICAgICBtZXNzYWdlcy5lcnJvcihyZXF1ZXN0LCBmIkVycm9yIGFsIGd1YXJkYXI6IHtleGN9IikKICAgICAgICByZXR1cm4gcmVkaXJlY3RfYWRtaW5fbmV3X2NsaWVudHNfYnJvd3NlKHBlcmlvZD1wZXJpb2QpCgogICAgY29udGV4dCA9IHsKICAgICAgICAqKmFkbWluX3BlcmlvZF9jb250ZXh0KHBlcmlvZCksCiAgICAgICAgKipicm93c2VfY29udGV4dChwZXJpb2QpLAogICAgICAgICJhZG1fbmF2X2FjdGl2ZSI6ICJjbGllbnRzX2Jyb3dzZSIsCiAgICB9CiAgICByZXR1cm4gcmVuZGVyKHJlcXVlc3QsICJwZ2MvYWRtaW5fbmV3X2NsaWVudHNfYnJvd3NlLmh0bWwiLCBjb250ZXh0KQoKCkBsb2dpbl9yZXF1aXJlZApAdXNlcl9wYXNzZXNfdGVzdChsYW1iZGEgdTogdS5pc19zdXBlcnVzZXIpCmRlZiBhZG1pbl9uZXdfY2xpZW50c191bmUocmVxdWVzdCk6CiAgICBwZXJpb2QgPSBwYXJzZV9hZG1pbl9wZXJpb2QocmVxdWVzdCkKCiAgICBpZiByZXF1ZXN0Lm1ldGhvZCA9PSAiUE9TVCI6CiAgICAgICAgcmVhc29uID0gKHJlcXVlc3QuUE9TVC5nZXQoInJlYXNvbiIpIG9yICIiKS5zdHJpcCgpCiAgICAgICAgcmVjYWxjX2FmdGVyID0gcmVxdWVzdC5QT1NULmdldCgicmVjYWxjX2FmdGVyIikgPT0gIjEiCiAgICAgICAgdHJ5OgogICAgICAgICAgICByZXN1bHQgPSBzYXZlX3VuZV9yZWFzc2lnbm1lbnRzKAogICAgICAgICAgICAgICAgcmVxdWVzdC51c2VyLCBwZXJpb2QsIHJlcXVlc3QuUE9TVCwgcmVhc29uCiAgICAgICAgICAgICkKICAgICAgICAgICAgaWYgcmVzdWx0WyJjaGFuZ2VkIl06CiAgICAgICAgICAgICAgICBtZXNzYWdlcy5zdWNjZXNzKAogICAgICAgICAgICAgICAgICAgIHJlcXVlc3QsCiAgICAgICAgICAgICAgICAgICAgZiJTZSByZWFzaWduYXJvbiB7cmVzdWx0WydjaGFuZ2VkJ119IHJlZ2lzdHJvKHMpLiAiCiAgICAgICAgICAgICAgICAgICAgZiJNw6l0cmljYXMgYWN0dWFsaXphZGFzOiB7cmVzdWx0WydtZXRyaWNzX3VwZGF0ZWQnXX0uIiwKICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIGlmIHJlY2FsY19hZnRlcjoKICAgICAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgICAgIGZvciBtc2cgaW4gcmVjYWxjdWxhdGVfYmxvY2soCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBwZXJpb2QueWVhciwgcGVyaW9kLm1vbnRoLCBCTE9DS19ORVdfQ0xJRU5UUwogICAgICAgICAgICAgICAgICAgICAgICApOgogICAgICAgICAgICAgICAgICAgICAgICAgICAgbWVzc2FnZXMuc3VjY2VzcyhyZXF1ZXN0LCBtc2cpCiAgICAgICAgICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBleGM6CiAgICAgICAgICAgICAgICAgICAgICAgIG1lc3NhZ2VzLndhcm5pbmcoCiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0LAogICAgICAgICAgICAgICAgICAgICAgICAgICAgZiJDYW1iaW9zIGd1YXJkYWRvcywgcGVybyBmYWxsw7MgZWwgcmVjw6FsY3Vsbzoge2V4Y30iLAogICAgICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBtZXNzYWdlcy5pbmZvKHJlcXVlc3QsICJObyBodWJvIGNhbWJpb3MgZGUgVU5FLiIpCiAgICAgICAgZXhjZXB0IFZhbHVlRXJyb3IgYXMgZXhjOgogICAgICAgICAgICBtZXNzYWdlcy5lcnJvcihyZXF1ZXN0LCBzdHIoZXhjKSkKICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGV4YzoKICAgICAgICAgICAgbWVzc2FnZXMuZXJyb3IocmVxdWVzdCwgZiJFcnJvciBhbCBndWFyZGFyOiB7ZXhjfSIpCiAgICAgICAgcmV0dXJuIHJlZGlyZWN0X2FkbWluX25ld19jbGllbnRzX3VuZShwZXJpb2Q9cGVyaW9kKQoKICAgIGNvbnRleHQgPSB7CiAgICAgICAgKiphZG1pbl9wZXJpb2RfY29udGV4dChwZXJpb2QpLAogICAgICAgICoqYnJvd3NlX2NvbnRleHQocGVyaW9kKSwKICAgICAgICAiYWRtX25hdl9hY3RpdmUiOiAiY2xpZW50c191bmUiLAogICAgfQogICAgcmV0dXJuIHJlbmRlcihyZXF1ZXN0LCAicGdjL2FkbWluX25ld19jbGllbnRzX3VuZS5odG1sIiwgY29udGV4dCkKCgpAbG9naW5fcmVxdWlyZWQKQHVzZXJfcGFzc2VzX3Rlc3QobGFtYmRhIHU6IHUuaXNfc3VwZXJ1c2VyKQpkZWYgbGVnYWN5X3J1bl9yZWNhbGNfcGdjKHJlcXVlc3QpOgogICAgIiIiQ29tcGF0aWJpbGlkYWQgY29uIFVSTHMvZm9ybXVsYXJpb3MgYW50aWd1b3MgZGUgcmVjw6FsY3Vsby4iIiIKICAgIHllYXIsIG1vbnRoID0gcGFyc2VfcGVyaW9kKHJlcXVlc3QpCiAgICBpZiByZXF1ZXN0Lm1ldGhvZCAhPSAiUE9TVCI6CiAgICAgICAgbWVzc2FnZXMuZXJyb3IocmVxdWVzdCwgIk3DqXRvZG8gbm8gcGVybWl0aWRvLiIpCiAgICAgICAgcmV0dXJuIHJlZGlyZWN0X2FkbWluX21vbnRobHkoeWVhciwgbW9udGgsIEJMT0NLX1JFVklFVykKCiAgICB5ZWFyX3JhdyA9IChyZXF1ZXN0LlBPU1QuZ2V0KCJ5ZWFyIikgb3IgIiIpLnN0cmlwKCkKICAgIG1vbnRoX3JhdyA9IChyZXF1ZXN0LlBPU1QuZ2V0KCJtb250aCIpIG9yICIiKS5zdHJpcCgpCiAgICB0cnk6CiAgICAgICAgeWVhciA9IGludCh5ZWFyX3JhdykKICAgICAgICBtb250aCA9IGludChtb250aF9yYXcpCiAgICAgICAgaWYgbW9udGggPCAxIG9yIG1vbnRoID4gMTI6CiAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IKICAgIGV4Y2VwdCAoVHlwZUVycm9yLCBWYWx1ZUVycm9yKToKICAgICAgICBtZXNzYWdlcy5lcnJvcihyZXF1ZXN0LCAiRGViZXMgaW5kaWNhciBhw7FvIHkgbWVzIHbDoWxpZG9zLiIpCiAgICAgICAgcmV0dXJuIHJlZGlyZWN0X2FkbWluX21vbnRobHkoeWVhciwgbW9udGgsIEJMT0NLX1JFVklFVykKCiAgICB0cnk6CiAgICAgICAgZm9yIG1zZyBpbiByZWNhbGN1bGF0ZV9wZXJpb2QoeWVhciwgbW9udGgpOgogICAgICAgICAgICBtZXNzYWdlcy5zdWNjZXNzKHJlcXVlc3QsIG1zZykKICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZXhjOgogICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsIGYiRXJyb3IgYWwgZWplY3V0YXIgcmVjYWxjIFBHQzoge2V4Y30iKQoKICAgIHJldHVybiByZWRpcmVjdF9hZG1pbl9tb250aGx5KHllYXIsIG1vbnRoLCBCTE9DS19SRVZJRVcpCgoKQGxvZ2luX3JlcXVpcmVkCkB1c2VyX3Bhc3Nlc190ZXN0KGxhbWJkYSB1OiB1LmlzX3N1cGVydXNlcikKZGVmIGxlZ2FjeV9ydW5fcmVjYWxjX2ludmVzdG1lbnQocmVxdWVzdCk6CiAgICAiIiJDb21wYXRpYmlsaWRhZCBjb24gVVJMcy9mb3JtdWxhcmlvcyBhbnRpZ3VvcyBkZSByZWPDoWxjdWxvIEludmVzdG1lbnQuIiIiCiAgICB5ZWFyLCBtb250aCA9IHBhcnNlX3BlcmlvZChyZXF1ZXN0KQogICAgaWYgcmVxdWVzdC5tZXRob2QgIT0gIlBPU1QiOgogICAgICAgIG1lc3NhZ2VzLmVycm9yKHJlcXVlc3QsICJNw6l0b2RvIG5vIHBlcm1pdGlkby4iKQogICAgICAgIHJldHVybiByZWRpcmVjdF9hZG1pbl9tb250aGx5KHllYXIsIG1vbnRoLCBCTE9DS19ORVdfQ0xJRU5UUykKCiAgICB5ZWFyX3JhdyA9IChyZXF1ZXN0LlBPU1QuZ2V0KCJ5ZWFyIikgb3IgIiIpLnN0cmlwKCkKICAgIG1vbnRoX3JhdyA9IChyZXF1ZXN0LlBPU1QuZ2V0KCJtb250aCIpIG9yICIiKS5zdHJpcCgpCiAgICB0cnk6CiAgICAgICAgeWVhciA9IGludCh5ZWFyX3JhdykKICAgICAgICBtb250aCA9IGludChtb250aF9yYXcpCiAgICAgICAgaWYgbW9udGggPCAxIG9yIG1vbnRoID4gMTI6CiAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IKICAgIGV4Y2VwdCAoVHlwZUVycm9yLCBWYWx1ZUVycm9yKToKICAgICAgICBtZXNzYWdlcy5lcnJvcihyZXF1ZXN0LCAiRGViZXMgaW5kaWNhciBhw7FvIHkgbWVzIHbDoWxpZG9zLiIpCiAgICAgICAgcmV0dXJuIHJlZGlyZWN0X2FkbWluX21vbnRobHkoeWVhciwgbW9udGgsIEJMT0NLX05FV19DTElFTlRTKQoKICAgIHRyeToKICAgICAgICBmb3IgbXNnIGluIHJlY2FsY3VsYXRlX2Jsb2NrKHllYXIsIG1vbnRoLCBCTE9DS19ORVdfQ0xJRU5UUyk6CiAgICAgICAgICAgIG1lc3NhZ2VzLnN1Y2Nlc3MocmVxdWVzdCwgbXNnKQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBleGM6CiAgICAgICAgbWVzc2FnZXMuZXJyb3IocmVxdWVzdCwgZiJFcnJvciBhbCBlamVjdXRhciByZWNhbGMgSW52ZXN0bWVudDoge2V4Y30iKQoKICAgIHJldHVybiByZWRpcmVjdF9hZG1pbl9tb250aGx5KHllYXIsIG1vbnRoLCBCTE9DS19ORVdfQ0xJRU5UUykKCgpAbG9naW5fcmVxdWlyZWQKQHVzZXJfcGFzc2VzX3Rlc3QobGFtYmRhIHU6IHUuaXNfc3VwZXJ1c2VyKQpkZWYgcmVkaXJlY3RfbWFudWFsX3Jlc3VsdHMocmVxdWVzdCk6CiAgICAiIiJMZWdhY3kgVVJMOiAvYWRtaW4taHViL2luZ3Jlc29zLW1hbnVhbC1jYXB0dXJlIOKGkiBtYXRyaXogYW51YWwgZGUgaW5ncmVzb3MuIiIiCiAgICBwZXJpb2QgPSBwYXJzZV9hZG1pbl9wZXJpb2QocmVxdWVzdCkKICAgIHJldHVybiByZWRpcmVjdF9hZG1pbl9pbmdyZXNvc195ZWFyKHBlcmlvZD1wZXJpb2QpCgoKQGxvZ2luX3JlcXVpcmVkCkB1c2VyX3Bhc3Nlc190ZXN0KGxhbWJkYSB1OiB1LmlzX3N1cGVydXNlcikKZGVmIHJlZGlyZWN0X21hbnVhbF9meChyZXF1ZXN0KToKICAgIHllYXIsIG1vbnRoID0gcGFyc2VfcGVyaW9kKHJlcXVlc3QpCiAgICByZXR1cm4gcmVkaXJlY3RfYWRtaW5fbWFudWFsKHllYXIsIG1vbnRoLCAiZngiKQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/apps.py
PATH_JSON="pgc/apps.py"
FILENAME=apps.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=6
SIZE_BYTES_UTF8=138
CONTENT_SHA256=7af6cc76ac61e70a87fedbf05b9dd422f5a48ed057b839ac47f9b0b8e595a37a
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


class PgcConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pgc"

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|from django.apps import AppConfig
00002|
00003|
00004|class PgcConfig(AppConfig):
00005|    default_auto_field = "django.db.models.BigAutoField"
00006|    name = "pgc"

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgUGdjQ29uZmlnKEFwcENvbmZpZyk6CiAgICBkZWZhdWx0X2F1dG9fZmllbGQgPSAiZGphbmdvLmRiLm1vZGVscy5CaWdBdXRvRmllbGQiCiAgICBuYW1lID0gInBnYyIK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=pgc/income_conversion.py
PATH_JSON="pgc/income_conversion.py"
FILENAME=income_conversion.py
EXTENSION=.py
LANGUAGE_HINT=python
LINE_COUNT=182
SIZE_BYTES_UTF8=5731
CONTENT_SHA256=340420fd39670a9088cf86be77dbc4e2eeeb093afa2d9b89a6fe5e5c3adbe934
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
"""Conversión y recálculo de ingresos (GTQ → USD canónico)."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction

from core.models import MetricDefinition
from pgc.models import AdminManualEditLog, MonthlyExchangeRate, MonthlyMetricResult


USD_DISPLAY_PLACES = Decimal("0.001")
USD_STORE_PLACES = Decimal("0.000001")


def get_fx_rate(year: int, month: int) -> Decimal | None:
    fx = MonthlyExchangeRate.objects.filter(year=year, month=month).first()
    if not fx or fx.usd_to_gtq in (None, Decimal("0")):
        return None
    return fx.usd_to_gtq


def gtq_to_usd(gtq: Decimal, usd_to_gtq: Decimal) -> Decimal:
    """1 USD = usd_to_gtq GTQ ⇒ USD = GTQ / usd_to_gtq."""
    if usd_to_gtq <= 0:
        raise ValueError("Tipo de cambio inválido.")
    return (gtq / usd_to_gtq).quantize(USD_STORE_PLACES, rounding=ROUND_HALF_UP)


def format_usd_3(value: Decimal | None) -> str:
    if value is None:
        return ""
    return str(value.quantize(USD_DISPLAY_PLACES, rounding=ROUND_HALF_UP))


def _log_edit(*, user, year, month, entity_id, field_name, old_value, new_value, reason):
    if user is None:
        return
    from pgc.admin_utils import format_value

    AdminManualEditLog.objects.create(
        year=year,
        month=month,
        entity_type=AdminManualEditLog.ENTITY_RESULT,
        entity_id=entity_id,
        field_name=field_name,
        old_value=format_value(old_value),
        new_value=format_value(new_value),
        reason=reason or "",
        edited_by=user,
    )


def mark_ingresos_stale_for_fx_change(
    *,
    year: int,
    month: int,
    old_fx,
    new_fx,
    user=None,
    reason: str = "",
) -> int:
    """Marca INGRESOS convertidos del mes como STALE_FX (no recalcula USD)."""
    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
    if not metric:
        return 0

    qs = MonthlyMetricResult.objects.filter(
        year=year,
        month=month,
        metric=metric,
        source_currency=MonthlyMetricResult.CURRENCY_GTQ,
        source_value__isnull=False,
    ).exclude(conversion_status=MonthlyMetricResult.CONVERSION_STALE_FX)

    marked = 0
    for row in qs:
        old_status = row.conversion_status
        row.conversion_status = MonthlyMetricResult.CONVERSION_STALE_FX
        note = (
            f"[TC cambió {old_fx} → {new_fx}; USD previo={row.measured_value}; "
            f"GTQ origen={row.source_value}]"
        )
        row.calculation_note = ((row.calculation_note or "") + " " + note).strip()
        row.save(update_fields=["conversion_status", "calculation_note", "updated_at"])
        _log_edit(
            user=user,
            year=year,
            month=month,
            entity_id=row.id,
            field_name="conversion_status",
            old_value=old_status or "",
            new_value=MonthlyMetricResult.CONVERSION_STALE_FX,
            reason=reason
            or f"TC actualizado {old_fx} → {new_fx}; ingresos pendientes de recálculo",
        )
        marked += 1
    return marked


@transaction.atomic
def recalc_stale_ingresos(
    *,
    year: int,
    month: int,
    user=None,
    reason: str = "",
    only_stale: bool = True,
) -> dict:
    """
    Recalcula USD desde source_value GTQ usando el FX actual del mes.
    Por defecto solo filas con conversion_status=STALE_FX.
    """
    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
    if not metric:
        raise ValueError("No existe métrica INGRESOS.")

    fx = get_fx_rate(year, month)
    if fx is None:
        raise ValueError(
            f"Falta tipo de cambio para {year}-{month:02d}. "
            "Defínalo antes de recalcular ingresos."
        )

    qs = MonthlyMetricResult.objects.filter(
        year=year,
        month=month,
        metric=metric,
        source_currency=MonthlyMetricResult.CURRENCY_GTQ,
        source_value__isnull=False,
    )
    if only_stale:
        qs = qs.filter(conversion_status=MonthlyMetricResult.CONVERSION_STALE_FX)

    updated = 0
    for row in qs:
        old_usd = row.measured_value
        old_fx = row.exchange_rate_used
        new_usd = gtq_to_usd(row.source_value, fx)
        row.measured_value = new_usd
        row.exchange_rate_used = fx
        row.conversion_status = MonthlyMetricResult.CONVERSION_CONVERTED
        row.calculation_note = (
            (row.calculation_note or "")
            + f" [Recalc GTQ→USD: {row.source_value} GTQ / {fx} = {new_usd} USD; "
            f"prev USD={old_usd}, prev FX={old_fx}]"
        ).strip()
        row.save(
            update_fields=[
                "measured_value",
                "exchange_rate_used",
                "conversion_status",
                "calculation_note",
                "updated_at",
            ]
        )
        _log_edit(
            user=user,
            year=year,
            month=month,
            entity_id=row.id,
            field_name="measured_value/exchange_rate_used",
            old_value=f"USD={old_usd}; FX={old_fx}",
            new_value=f"USD={new_usd}; FX={fx}; GTQ={row.source_value}",
            reason=reason or "Recálculo de ingresos tras cambio de TC",
        )
        updated += 1

    return {"updated": updated, "fx": fx}


def count_stale_ingresos(year: int, month: int) -> int:
    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
    if not metric:
        return 0
    return MonthlyMetricResult.objects.filter(
        year=year,
        month=month,
        metric=metric,
        conversion_status=MonthlyMetricResult.CONVERSION_STALE_FX,
    ).count()

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|"""Conversión y recálculo de ingresos (GTQ → USD canónico)."""
00002|
00003|from __future__ import annotations
00004|
00005|from decimal import Decimal, ROUND_HALF_UP
00006|
00007|from django.db import transaction
00008|
00009|from core.models import MetricDefinition
00010|from pgc.models import AdminManualEditLog, MonthlyExchangeRate, MonthlyMetricResult
00011|
00012|
00013|USD_DISPLAY_PLACES = Decimal("0.001")
00014|USD_STORE_PLACES = Decimal("0.000001")
00015|
00016|
00017|def get_fx_rate(year: int, month: int) -> Decimal | None:
00018|    fx = MonthlyExchangeRate.objects.filter(year=year, month=month).first()
00019|    if not fx or fx.usd_to_gtq in (None, Decimal("0")):
00020|        return None
00021|    return fx.usd_to_gtq
00022|
00023|
00024|def gtq_to_usd(gtq: Decimal, usd_to_gtq: Decimal) -> Decimal:
00025|    """1 USD = usd_to_gtq GTQ ⇒ USD = GTQ / usd_to_gtq."""
00026|    if usd_to_gtq <= 0:
00027|        raise ValueError("Tipo de cambio inválido.")
00028|    return (gtq / usd_to_gtq).quantize(USD_STORE_PLACES, rounding=ROUND_HALF_UP)
00029|
00030|
00031|def format_usd_3(value: Decimal | None) -> str:
00032|    if value is None:
00033|        return ""
00034|    return str(value.quantize(USD_DISPLAY_PLACES, rounding=ROUND_HALF_UP))
00035|
00036|
00037|def _log_edit(*, user, year, month, entity_id, field_name, old_value, new_value, reason):
00038|    if user is None:
00039|        return
00040|    from pgc.admin_utils import format_value
00041|
00042|    AdminManualEditLog.objects.create(
00043|        year=year,
00044|        month=month,
00045|        entity_type=AdminManualEditLog.ENTITY_RESULT,
00046|        entity_id=entity_id,
00047|        field_name=field_name,
00048|        old_value=format_value(old_value),
00049|        new_value=format_value(new_value),
00050|        reason=reason or "",
00051|        edited_by=user,
00052|    )
00053|
00054|
00055|def mark_ingresos_stale_for_fx_change(
00056|    *,
00057|    year: int,
00058|    month: int,
00059|    old_fx,
00060|    new_fx,
00061|    user=None,
00062|    reason: str = "",
00063|) -> int:
00064|    """Marca INGRESOS convertidos del mes como STALE_FX (no recalcula USD)."""
00065|    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
00066|    if not metric:
00067|        return 0
00068|
00069|    qs = MonthlyMetricResult.objects.filter(
00070|        year=year,
00071|        month=month,
00072|        metric=metric,
00073|        source_currency=MonthlyMetricResult.CURRENCY_GTQ,
00074|        source_value__isnull=False,
00075|    ).exclude(conversion_status=MonthlyMetricResult.CONVERSION_STALE_FX)
00076|
00077|    marked = 0
00078|    for row in qs:
00079|        old_status = row.conversion_status
00080|        row.conversion_status = MonthlyMetricResult.CONVERSION_STALE_FX
00081|        note = (
00082|            f"[TC cambió {old_fx} → {new_fx}; USD previo={row.measured_value}; "
00083|            f"GTQ origen={row.source_value}]"
00084|        )
00085|        row.calculation_note = ((row.calculation_note or "") + " " + note).strip()
00086|        row.save(update_fields=["conversion_status", "calculation_note", "updated_at"])
00087|        _log_edit(
00088|            user=user,
00089|            year=year,
00090|            month=month,
00091|            entity_id=row.id,
00092|            field_name="conversion_status",
00093|            old_value=old_status or "",
00094|            new_value=MonthlyMetricResult.CONVERSION_STALE_FX,
00095|            reason=reason
00096|            or f"TC actualizado {old_fx} → {new_fx}; ingresos pendientes de recálculo",
00097|        )
00098|        marked += 1
00099|    return marked
00100|
00101|
00102|@transaction.atomic
00103|def recalc_stale_ingresos(
00104|    *,
00105|    year: int,
00106|    month: int,
00107|    user=None,
00108|    reason: str = "",
00109|    only_stale: bool = True,
00110|) -> dict:
00111|    """
00112|    Recalcula USD desde source_value GTQ usando el FX actual del mes.
00113|    Por defecto solo filas con conversion_status=STALE_FX.
00114|    """
00115|    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
00116|    if not metric:
00117|        raise ValueError("No existe métrica INGRESOS.")
00118|
00119|    fx = get_fx_rate(year, month)
00120|    if fx is None:
00121|        raise ValueError(
00122|            f"Falta tipo de cambio para {year}-{month:02d}. "
00123|            "Defínalo antes de recalcular ingresos."
00124|        )
00125|
00126|    qs = MonthlyMetricResult.objects.filter(
00127|        year=year,
00128|        month=month,
00129|        metric=metric,
00130|        source_currency=MonthlyMetricResult.CURRENCY_GTQ,
00131|        source_value__isnull=False,
00132|    )
00133|    if only_stale:
00134|        qs = qs.filter(conversion_status=MonthlyMetricResult.CONVERSION_STALE_FX)
00135|
00136|    updated = 0
00137|    for row in qs:
00138|        old_usd = row.measured_value
00139|        old_fx = row.exchange_rate_used
00140|        new_usd = gtq_to_usd(row.source_value, fx)
00141|        row.measured_value = new_usd
00142|        row.exchange_rate_used = fx
00143|        row.conversion_status = MonthlyMetricResult.CONVERSION_CONVERTED
00144|        row.calculation_note = (
00145|            (row.calculation_note or "")
00146|            + f" [Recalc GTQ→USD: {row.source_value} GTQ / {fx} = {new_usd} USD; "
00147|            f"prev USD={old_usd}, prev FX={old_fx}]"
00148|        ).strip()
00149|        row.save(
00150|            update_fields=[
00151|                "measured_value",
00152|                "exchange_rate_used",
00153|                "conversion_status",
00154|                "calculation_note",
00155|                "updated_at",
00156|            ]
00157|        )
00158|        _log_edit(
00159|            user=user,
00160|            year=year,
00161|            month=month,
00162|            entity_id=row.id,
00163|            field_name="measured_value/exchange_rate_used",
00164|            old_value=f"USD={old_usd}; FX={old_fx}",
00165|            new_value=f"USD={new_usd}; FX={fx}; GTQ={row.source_value}",
00166|            reason=reason or "Recálculo de ingresos tras cambio de TC",
00167|        )
00168|        updated += 1
00169|
00170|    return {"updated": updated, "fx": fx}
00171|
00172|
00173|def count_stale_ingresos(year: int, month: int) -> int:
00174|    metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
00175|    if not metric:
00176|        return 0
00177|    return MonthlyMetricResult.objects.filter(
00178|        year=year,
00179|        month=month,
00180|        metric=metric,
00181|        conversion_status=MonthlyMetricResult.CONVERSION_STALE_FX,
00182|    ).count()

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
IiIiQ29udmVyc2nDs24geSByZWPDoWxjdWxvIGRlIGluZ3Jlc29zIChHVFEg4oaSIFVTRCBjYW7Ds25pY28pLiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsLCBST1VORF9IQUxGX1VQCgpmcm9tIGRqYW5nby5kYiBpbXBvcnQgdHJhbnNhY3Rpb24KCmZyb20gY29yZS5tb2RlbHMgaW1wb3J0IE1ldHJpY0RlZmluaXRpb24KZnJvbSBwZ2MubW9kZWxzIGltcG9ydCBBZG1pbk1hbnVhbEVkaXRMb2csIE1vbnRobHlFeGNoYW5nZVJhdGUsIE1vbnRobHlNZXRyaWNSZXN1bHQKCgpVU0RfRElTUExBWV9QTEFDRVMgPSBEZWNpbWFsKCIwLjAwMSIpClVTRF9TVE9SRV9QTEFDRVMgPSBEZWNpbWFsKCIwLjAwMDAwMSIpCgoKZGVmIGdldF9meF9yYXRlKHllYXI6IGludCwgbW9udGg6IGludCkgLT4gRGVjaW1hbCB8IE5vbmU6CiAgICBmeCA9IE1vbnRobHlFeGNoYW5nZVJhdGUub2JqZWN0cy5maWx0ZXIoeWVhcj15ZWFyLCBtb250aD1tb250aCkuZmlyc3QoKQogICAgaWYgbm90IGZ4IG9yIGZ4LnVzZF90b19ndHEgaW4gKE5vbmUsIERlY2ltYWwoIjAiKSk6CiAgICAgICAgcmV0dXJuIE5vbmUKICAgIHJldHVybiBmeC51c2RfdG9fZ3RxCgoKZGVmIGd0cV90b191c2QoZ3RxOiBEZWNpbWFsLCB1c2RfdG9fZ3RxOiBEZWNpbWFsKSAtPiBEZWNpbWFsOgogICAgIiIiMSBVU0QgPSB1c2RfdG9fZ3RxIEdUUSDih5IgVVNEID0gR1RRIC8gdXNkX3RvX2d0cS4iIiIKICAgIGlmIHVzZF90b19ndHEgPD0gMDoKICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJUaXBvIGRlIGNhbWJpbyBpbnbDoWxpZG8uIikKICAgIHJldHVybiAoZ3RxIC8gdXNkX3RvX2d0cSkucXVhbnRpemUoVVNEX1NUT1JFX1BMQUNFUywgcm91bmRpbmc9Uk9VTkRfSEFMRl9VUCkKCgpkZWYgZm9ybWF0X3VzZF8zKHZhbHVlOiBEZWNpbWFsIHwgTm9uZSkgLT4gc3RyOgogICAgaWYgdmFsdWUgaXMgTm9uZToKICAgICAgICByZXR1cm4gIiIKICAgIHJldHVybiBzdHIodmFsdWUucXVhbnRpemUoVVNEX0RJU1BMQVlfUExBQ0VTLCByb3VuZGluZz1ST1VORF9IQUxGX1VQKSkKCgpkZWYgX2xvZ19lZGl0KCosIHVzZXIsIHllYXIsIG1vbnRoLCBlbnRpdHlfaWQsIGZpZWxkX25hbWUsIG9sZF92YWx1ZSwgbmV3X3ZhbHVlLCByZWFzb24pOgogICAgaWYgdXNlciBpcyBOb25lOgogICAgICAgIHJldHVybgogICAgZnJvbSBwZ2MuYWRtaW5fdXRpbHMgaW1wb3J0IGZvcm1hdF92YWx1ZQoKICAgIEFkbWluTWFudWFsRWRpdExvZy5vYmplY3RzLmNyZWF0ZSgKICAgICAgICB5ZWFyPXllYXIsCiAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgZW50aXR5X3R5cGU9QWRtaW5NYW51YWxFZGl0TG9nLkVOVElUWV9SRVNVTFQsCiAgICAgICAgZW50aXR5X2lkPWVudGl0eV9pZCwKICAgICAgICBmaWVsZF9uYW1lPWZpZWxkX25hbWUsCiAgICAgICAgb2xkX3ZhbHVlPWZvcm1hdF92YWx1ZShvbGRfdmFsdWUpLAogICAgICAgIG5ld192YWx1ZT1mb3JtYXRfdmFsdWUobmV3X3ZhbHVlKSwKICAgICAgICByZWFzb249cmVhc29uIG9yICIiLAogICAgICAgIGVkaXRlZF9ieT11c2VyLAogICAgKQoKCmRlZiBtYXJrX2luZ3Jlc29zX3N0YWxlX2Zvcl9meF9jaGFuZ2UoCiAgICAqLAogICAgeWVhcjogaW50LAogICAgbW9udGg6IGludCwKICAgIG9sZF9meCwKICAgIG5ld19meCwKICAgIHVzZXI9Tm9uZSwKICAgIHJlYXNvbjogc3RyID0gIiIsCikgLT4gaW50OgogICAgIiIiTWFyY2EgSU5HUkVTT1MgY29udmVydGlkb3MgZGVsIG1lcyBjb21vIFNUQUxFX0ZYIChubyByZWNhbGN1bGEgVVNEKS4iIiIKICAgIG1ldHJpYyA9IE1ldHJpY0RlZmluaXRpb24ub2JqZWN0cy5maWx0ZXIoY29kZT1NZXRyaWNEZWZpbml0aW9uLkNPREVfSU5HUkVTT1MpLmZpcnN0KCkKICAgIGlmIG5vdCBtZXRyaWM6CiAgICAgICAgcmV0dXJuIDAKCiAgICBxcyA9IE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5maWx0ZXIoCiAgICAgICAgeWVhcj15ZWFyLAogICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgc291cmNlX2N1cnJlbmN5PU1vbnRobHlNZXRyaWNSZXN1bHQuQ1VSUkVOQ1lfR1RRLAogICAgICAgIHNvdXJjZV92YWx1ZV9faXNudWxsPUZhbHNlLAogICAgKS5leGNsdWRlKGNvbnZlcnNpb25fc3RhdHVzPU1vbnRobHlNZXRyaWNSZXN1bHQuQ09OVkVSU0lPTl9TVEFMRV9GWCkKCiAgICBtYXJrZWQgPSAwCiAgICBmb3Igcm93IGluIHFzOgogICAgICAgIG9sZF9zdGF0dXMgPSByb3cuY29udmVyc2lvbl9zdGF0dXMKICAgICAgICByb3cuY29udmVyc2lvbl9zdGF0dXMgPSBNb250aGx5TWV0cmljUmVzdWx0LkNPTlZFUlNJT05fU1RBTEVfRlgKICAgICAgICBub3RlID0gKAogICAgICAgICAgICBmIltUQyBjYW1iacOzIHtvbGRfZnh9IOKGkiB7bmV3X2Z4fTsgVVNEIHByZXZpbz17cm93Lm1lYXN1cmVkX3ZhbHVlfTsgIgogICAgICAgICAgICBmIkdUUSBvcmlnZW49e3Jvdy5zb3VyY2VfdmFsdWV9XSIKICAgICAgICApCiAgICAgICAgcm93LmNhbGN1bGF0aW9uX25vdGUgPSAoKHJvdy5jYWxjdWxhdGlvbl9ub3RlIG9yICIiKSArICIgIiArIG5vdGUpLnN0cmlwKCkKICAgICAgICByb3cuc2F2ZSh1cGRhdGVfZmllbGRzPVsiY29udmVyc2lvbl9zdGF0dXMiLCAiY2FsY3VsYXRpb25fbm90ZSIsICJ1cGRhdGVkX2F0Il0pCiAgICAgICAgX2xvZ19lZGl0KAogICAgICAgICAgICB1c2VyPXVzZXIsCiAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgIGVudGl0eV9pZD1yb3cuaWQsCiAgICAgICAgICAgIGZpZWxkX25hbWU9ImNvbnZlcnNpb25fc3RhdHVzIiwKICAgICAgICAgICAgb2xkX3ZhbHVlPW9sZF9zdGF0dXMgb3IgIiIsCiAgICAgICAgICAgIG5ld192YWx1ZT1Nb250aGx5TWV0cmljUmVzdWx0LkNPTlZFUlNJT05fU1RBTEVfRlgsCiAgICAgICAgICAgIHJlYXNvbj1yZWFzb24KICAgICAgICAgICAgb3IgZiJUQyBhY3R1YWxpemFkbyB7b2xkX2Z4fSDihpIge25ld19meH07IGluZ3Jlc29zIHBlbmRpZW50ZXMgZGUgcmVjw6FsY3VsbyIsCiAgICAgICAgKQogICAgICAgIG1hcmtlZCArPSAxCiAgICByZXR1cm4gbWFya2VkCgoKQHRyYW5zYWN0aW9uLmF0b21pYwpkZWYgcmVjYWxjX3N0YWxlX2luZ3Jlc29zKAogICAgKiwKICAgIHllYXI6IGludCwKICAgIG1vbnRoOiBpbnQsCiAgICB1c2VyPU5vbmUsCiAgICByZWFzb246IHN0ciA9ICIiLAogICAgb25seV9zdGFsZTogYm9vbCA9IFRydWUsCikgLT4gZGljdDoKICAgICIiIgogICAgUmVjYWxjdWxhIFVTRCBkZXNkZSBzb3VyY2VfdmFsdWUgR1RRIHVzYW5kbyBlbCBGWCBhY3R1YWwgZGVsIG1lcy4KICAgIFBvciBkZWZlY3RvIHNvbG8gZmlsYXMgY29uIGNvbnZlcnNpb25fc3RhdHVzPVNUQUxFX0ZYLgogICAgIiIiCiAgICBtZXRyaWMgPSBNZXRyaWNEZWZpbml0aW9uLm9iamVjdHMuZmlsdGVyKGNvZGU9TWV0cmljRGVmaW5pdGlvbi5DT0RFX0lOR1JFU09TKS5maXJzdCgpCiAgICBpZiBub3QgbWV0cmljOgogICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoIk5vIGV4aXN0ZSBtw6l0cmljYSBJTkdSRVNPUy4iKQoKICAgIGZ4ID0gZ2V0X2Z4X3JhdGUoeWVhciwgbW9udGgpCiAgICBpZiBmeCBpcyBOb25lOgogICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoCiAgICAgICAgICAgIGYiRmFsdGEgdGlwbyBkZSBjYW1iaW8gcGFyYSB7eWVhcn0te21vbnRoOjAyZH0uICIKICAgICAgICAgICAgIkRlZsOtbmFsbyBhbnRlcyBkZSByZWNhbGN1bGFyIGluZ3Jlc29zLiIKICAgICAgICApCgogICAgcXMgPSBNb250aGx5TWV0cmljUmVzdWx0Lm9iamVjdHMuZmlsdGVyKAogICAgICAgIHllYXI9eWVhciwKICAgICAgICBtb250aD1tb250aCwKICAgICAgICBtZXRyaWM9bWV0cmljLAogICAgICAgIHNvdXJjZV9jdXJyZW5jeT1Nb250aGx5TWV0cmljUmVzdWx0LkNVUlJFTkNZX0dUUSwKICAgICAgICBzb3VyY2VfdmFsdWVfX2lzbnVsbD1GYWxzZSwKICAgICkKICAgIGlmIG9ubHlfc3RhbGU6CiAgICAgICAgcXMgPSBxcy5maWx0ZXIoY29udmVyc2lvbl9zdGF0dXM9TW9udGhseU1ldHJpY1Jlc3VsdC5DT05WRVJTSU9OX1NUQUxFX0ZYKQoKICAgIHVwZGF0ZWQgPSAwCiAgICBmb3Igcm93IGluIHFzOgogICAgICAgIG9sZF91c2QgPSByb3cubWVhc3VyZWRfdmFsdWUKICAgICAgICBvbGRfZnggPSByb3cuZXhjaGFuZ2VfcmF0ZV91c2VkCiAgICAgICAgbmV3X3VzZCA9IGd0cV90b191c2Qocm93LnNvdXJjZV92YWx1ZSwgZngpCiAgICAgICAgcm93Lm1lYXN1cmVkX3ZhbHVlID0gbmV3X3VzZAogICAgICAgIHJvdy5leGNoYW5nZV9yYXRlX3VzZWQgPSBmeAogICAgICAgIHJvdy5jb252ZXJzaW9uX3N0YXR1cyA9IE1vbnRobHlNZXRyaWNSZXN1bHQuQ09OVkVSU0lPTl9DT05WRVJURUQKICAgICAgICByb3cuY2FsY3VsYXRpb25fbm90ZSA9ICgKICAgICAgICAgICAgKHJvdy5jYWxjdWxhdGlvbl9ub3RlIG9yICIiKQogICAgICAgICAgICArIGYiIFtSZWNhbGMgR1RR4oaSVVNEOiB7cm93LnNvdXJjZV92YWx1ZX0gR1RRIC8ge2Z4fSA9IHtuZXdfdXNkfSBVU0Q7ICIKICAgICAgICAgICAgZiJwcmV2IFVTRD17b2xkX3VzZH0sIHByZXYgRlg9e29sZF9meH1dIgogICAgICAgICkuc3RyaXAoKQogICAgICAgIHJvdy5zYXZlKAogICAgICAgICAgICB1cGRhdGVfZmllbGRzPVsKICAgICAgICAgICAgICAgICJtZWFzdXJlZF92YWx1ZSIsCiAgICAgICAgICAgICAgICAiZXhjaGFuZ2VfcmF0ZV91c2VkIiwKICAgICAgICAgICAgICAgICJjb252ZXJzaW9uX3N0YXR1cyIsCiAgICAgICAgICAgICAgICAiY2FsY3VsYXRpb25fbm90ZSIsCiAgICAgICAgICAgICAgICAidXBkYXRlZF9hdCIsCiAgICAgICAgICAgIF0KICAgICAgICApCiAgICAgICAgX2xvZ19lZGl0KAogICAgICAgICAgICB1c2VyPXVzZXIsCiAgICAgICAgICAgIHllYXI9eWVhciwKICAgICAgICAgICAgbW9udGg9bW9udGgsCiAgICAgICAgICAgIGVudGl0eV9pZD1yb3cuaWQsCiAgICAgICAgICAgIGZpZWxkX25hbWU9Im1lYXN1cmVkX3ZhbHVlL2V4Y2hhbmdlX3JhdGVfdXNlZCIsCiAgICAgICAgICAgIG9sZF92YWx1ZT1mIlVTRD17b2xkX3VzZH07IEZYPXtvbGRfZnh9IiwKICAgICAgICAgICAgbmV3X3ZhbHVlPWYiVVNEPXtuZXdfdXNkfTsgRlg9e2Z4fTsgR1RRPXtyb3cuc291cmNlX3ZhbHVlfSIsCiAgICAgICAgICAgIHJlYXNvbj1yZWFzb24gb3IgIlJlY8OhbGN1bG8gZGUgaW5ncmVzb3MgdHJhcyBjYW1iaW8gZGUgVEMiLAogICAgICAgICkKICAgICAgICB1cGRhdGVkICs9IDEKCiAgICByZXR1cm4geyJ1cGRhdGVkIjogdXBkYXRlZCwgImZ4IjogZnh9CgoKZGVmIGNvdW50X3N0YWxlX2luZ3Jlc29zKHllYXI6IGludCwgbW9udGg6IGludCkgLT4gaW50OgogICAgbWV0cmljID0gTWV0cmljRGVmaW5pdGlvbi5vYmplY3RzLmZpbHRlcihjb2RlPU1ldHJpY0RlZmluaXRpb24uQ09ERV9JTkdSRVNPUykuZmlyc3QoKQogICAgaWYgbm90IG1ldHJpYzoKICAgICAgICByZXR1cm4gMAogICAgcmV0dXJuIE1vbnRobHlNZXRyaWNSZXN1bHQub2JqZWN0cy5maWx0ZXIoCiAgICAgICAgeWVhcj15ZWFyLAogICAgICAgIG1vbnRoPW1vbnRoLAogICAgICAgIG1ldHJpYz1tZXRyaWMsCiAgICAgICAgY29udmVyc2lvbl9zdGF0dXM9TW9udGhseU1ldHJpY1Jlc3VsdC5DT05WRVJTSU9OX1NUQUxFX0ZYLAogICAgKS5jb3VudCgpCg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
