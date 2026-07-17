"""
Edición browse de clientes nuevos y reasignación de UNE.
"""

from __future__ import annotations

from django.core.files.base import ContentFile
from django.db import transaction

from core.models import Currency, UNE
from imports.models import FileUpload, NewClientImportHeader, NewClientImportRow
from pgc.admin_manual import log_manual_edit
from pgc.admin_period import _sync_clientes_nuevos_metrics_from_rows
from pgc.admin_utils import AdminPeriod, apply_period_range, parse_decimal_or_none
from pgc.models import AdminManualEditLog


BASE_CURRENCIES = (
    ("GTQ", "Quetzal guatemalteco", "Q"),
    ("USD", "Dólar estadounidense", "$"),
)


def ensure_base_currencies() -> list[Currency]:
    """Garantiza GTQ/USD activos (catálogo usado por el browse de clientes)."""
    for code, name, symbol in BASE_CURRENCIES:
        Currency.objects.update_or_create(
            code=code,
            defaults={"name": name, "symbol": symbol, "is_active": True},
        )
    return list(Currency.objects.filter(is_active=True).order_by("code"))


ALLOWED_UNE_CODES = (
    UNE.CODE_FACTORING,
    UNE.CODE_LEASING,
    UNE.CODE_INSURANCE,
    UNE.CODE_INVESTMENT,
)

UNE_SHORT = {
    UNE.CODE_FACTORING: "1·Fa",
    UNE.CODE_LEASING: "2·Le",
    UNE.CODE_INSURANCE: "3·In",
    UNE.CODE_INVESTMENT: "4·Iv",
}


def period_unes():
    return list(
        UNE.objects.filter(is_active=True, code__in=ALLOWED_UNE_CODES).order_by(
            "sort_order", "code"
        )
    )


def une_options_for_template():
    return [
        {
            "id": une.id,
            "code": une.code,
            "name_es": une.name_es,
            "short": UNE_SHORT.get(une.code, une.code[:2]),
        }
        for une in period_unes()
    ]


def ensure_new_client_header(year: int, month: int, user) -> NewClientImportHeader:
    header = NewClientImportHeader.objects.filter(year=year, month=month).first()
    if header:
        return header

    upload = FileUpload(
        uploaded_by=user,
        original_filename=f"manual-clientes-{year}-{month:02d}.tsv",
        file_type_detected=FileUpload.TYPE_NEW_CLIENTS,
        detected_year=year,
        detected_month=month,
        status=FileUpload.STATUS_PARSED_OK,
        parsing_notes="Encabezado creado automáticamente para edición manual de filas.",
        file_format=FileUpload.FORMAT_TSV,
    )
    upload.stored_file.save(
        f"manual-clientes-{year}-{month:02d}.tsv",
        ContentFile(b"# manual new clients\n"),
        save=False,
    )
    upload.save()
    header = NewClientImportHeader.objects.filter(year=year, month=month).first()
    if not header:
        raise ValueError(
            f"No se pudo crear encabezado de clientes nuevos para {year}-{month:02d}."
        )
    return header


def browse_context(period: AdminPeriod) -> dict:
    rows = list(
        apply_period_range(NewClientImportRow.objects.all(), period)
        .select_related("une", "currency", "header")
        .order_by("year", "month", "une__sort_order", "client_name", "operation_code", "id")
    )
    currencies = ensure_base_currencies()
    return {
        "rows": rows,
        "unes": une_options_for_template(),
        "currencies": currencies,
        "header": NewClientImportHeader.objects.filter(
            year=period.year, month=period.month
        ).first(),
        "label": period.label,
        "row_count": len(rows),
        "supports_month_range": True,
        "single_month_ops": False,
    }


def _parse_bool(post_data, key: str) -> bool:
    return post_data.get(key) == "1"


def _parse_int(raw, default=0):
    text = (raw or "").strip()
    if text == "":
        return default
    try:
        return int(text)
    except (TypeError, ValueError):
        return default


def _parse_optional_int(raw):
    text = (raw or "").strip()
    if text == "":
        return None
    try:
        return int(text)
    except (TypeError, ValueError):
        return None


def _allowed_une_ids() -> set[int]:
    return {u.id for u in period_unes()}


def _resolve_currency_id(raw) -> int | None:
    text = (raw or "").strip()
    if not text:
        return None
    try:
        cid = int(text)
    except (TypeError, ValueError):
        return None
    if Currency.objects.filter(id=cid, is_active=True).exists():
        return cid
    return None


@transaction.atomic
def save_browse_rows(user, period: AdminPeriod, post_data, reason: str = "") -> dict:
    """
    Guarda ediciones browse: actualizar, eliminar y alta.
    Retorna dict con counts: updated, deleted, created, metrics_updated.
    """
    allowed_unes = _allowed_une_ids()
    existing = {
        row.id: row
        for row in apply_period_range(NewClientImportRow.objects.all(), period)
    }
    touched_months: set[int] = set()

    deleted = 0
    updated = 0

    delete_ids = set()
    for raw_id in post_data.getlist("delete_ids"):
        try:
            delete_ids.add(int(raw_id))
        except (TypeError, ValueError):
            continue

    for row_id in list(delete_ids):
        row = existing.pop(row_id, None)
        if not row:
            continue
        touched_months.add(row.month)
        log_manual_edit(
            user=user,
            year=row.year,
            month=row.month,
            entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
            entity_id=row.id,
            field_name="delete",
            old_value=f"{row.client_name}|{row.operation_code}|une={row.une_id}",
            new_value="",
            reason=reason or "Eliminación desde browse de clientes nuevos",
        )
        row.delete()
        deleted += 1

    for row_id, row in existing.items():
        prefix = f"row_{row_id}_"
        if f"{prefix}client_name" not in post_data:
            continue

        une_id = _parse_optional_int(post_data.get(f"{prefix}une"))
        if une_id not in allowed_unes:
            raise ValueError(f"UNE inválida en fila {row_id}.")

        new_vals = {
            "client_name": (post_data.get(f"{prefix}client_name") or "").strip(),
            "nit": (post_data.get(f"{prefix}nit") or "").strip(),
            "operation_code": (post_data.get(f"{prefix}operation_code") or "").strip(),
            "previous_contracts": _parse_int(post_data.get(f"{prefix}previous_contracts"), 0),
            "counts_as_new": _parse_bool(post_data, f"{prefix}counts_as_new"),
            "currency_id": _resolve_currency_id(post_data.get(f"{prefix}currency")),
            "amount": parse_decimal_or_none(post_data.get(f"{prefix}amount")),
            "raw_une_value": (post_data.get(f"{prefix}raw_une_value") or "").strip(),
            "observations": (post_data.get(f"{prefix}observations") or "").strip(),
            "une_id": une_id,
            "source_row_number": _parse_optional_int(
                post_data.get(f"{prefix}source_row_number")
            ),
        }

        changed_fields = []
        for field, new_value in new_vals.items():
            old_value = getattr(row, field)
            if old_value != new_value:
                setattr(row, field, new_value)
                changed_fields.append(field)

        if not changed_fields:
            continue

        row.save()
        touched_months.add(row.month)
        log_manual_edit(
            user=user,
            year=row.year,
            month=row.month,
            entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
            entity_id=row.id,
            field_name=",".join(changed_fields),
            old_value="edit",
            new_value=",".join(changed_fields),
            reason=reason or "Edición browse de clientes nuevos",
        )
        updated += 1

    created = 0
    new_client = (post_data.get("new_client_name") or "").strip()
    new_nit = (post_data.get("new_nit") or "").strip()
    new_op = (post_data.get("new_operation_code") or "").strip()
    new_une = _parse_optional_int(post_data.get("new_une"))
    has_new = any([new_client, new_nit, new_op, post_data.get("new_amount")])

    if has_new:
        if new_une not in allowed_unes:
            raise ValueError("Debe elegir UNE válida para el registro nuevo.")
        new_month = _parse_int(post_data.get("new_month"), period.month)
        if new_month < period.month_from or new_month > period.month_to:
            new_month = period.month
        header = ensure_new_client_header(period.year, new_month, user)
        row = NewClientImportRow.objects.create(
            header=header,
            une_id=new_une,
            year=period.year,
            month=new_month,
            client_name=new_client,
            nit=new_nit,
            operation_code=new_op,
            previous_contracts=_parse_int(post_data.get("new_previous_contracts"), 0),
            counts_as_new=_parse_bool(post_data, "new_counts_as_new"),
            currency_id=_resolve_currency_id(post_data.get("new_currency")),
            amount=parse_decimal_or_none(post_data.get("new_amount")),
            raw_une_value=(post_data.get("new_raw_une_value") or "").strip(),
            observations=(post_data.get("new_observations") or "").strip(),
            source_row_number=_parse_optional_int(post_data.get("new_source_row_number")),
        )
        touched_months.add(new_month)
        log_manual_edit(
            user=user,
            year=period.year,
            month=new_month,
            entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
            entity_id=row.id,
            field_name="create",
            old_value="",
            new_value=f"{row.client_name}|{row.operation_code}|une={row.une_id}",
            reason=reason or "Alta desde browse de clientes nuevos",
        )
        created += 1

    metrics_updated = 0
    for m in sorted(touched_months):
        metrics_updated += _sync_clientes_nuevos_metrics_from_rows(period.year, m)

    return {
        "updated": updated,
        "deleted": deleted,
        "created": created,
        "metrics_updated": metrics_updated,
        "total": updated + deleted + created,
    }


@transaction.atomic
def save_une_reassignments(user, period: AdminPeriod, post_data, reason: str = "") -> dict:
    """Solo permite cambiar UNE entre las cuatro UNEs activas del negocio."""
    allowed_unes = _allowed_une_ids()
    une_by_id = {u.id: u for u in period_unes()}
    changed = 0
    touched_months: set[int] = set()

    qs = apply_period_range(NewClientImportRow.objects.all(), period).select_related("une")
    for row in qs:
        raw = post_data.get(f"une_{row.id}")
        if raw is None:
            continue
        new_une_id = _parse_optional_int(raw)
        if new_une_id not in allowed_unes:
            raise ValueError(f"UNE inválida para fila {row.id}.")
        if new_une_id == row.une_id:
            continue

        old_une = row.une
        new_une = une_by_id[new_une_id]
        row.une_id = new_une_id
        row.raw_une_value = new_une.name_es
        row.save(update_fields=["une", "raw_une_value", "updated_at"])
        touched_months.add(row.month)
        log_manual_edit(
            user=user,
            year=row.year,
            month=row.month,
            entity_type=AdminManualEditLog.ENTITY_NEW_CLIENT_ROW,
            entity_id=row.id,
            field_name="une",
            old_value=f"{old_une.code} ({old_une.name_es})",
            new_value=f"{new_une.code} ({new_une.name_es})",
            reason=reason or "Reasignación de UNE",
        )
        changed += 1

    metrics_updated = 0
    for m in sorted(touched_months):
        metrics_updated += _sync_clientes_nuevos_metrics_from_rows(period.year, m)

    return {"changed": changed, "metrics_updated": metrics_updated}
