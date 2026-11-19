"""Plan de eventos ImportAuditEvent sintéticos según datos ya en BD."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone

from core.wcg_models import DataImportBatch
from imports.audit_cli_registry import CLI_IMPORT_COMMANDS, DISPATCH_IMPORT_TIPOS
from imports.models import (
    BankLoanMonthSnapshot,
    CrossSaleImportHeader,
    FileUpload,
    ImportAuditEvent,
    InvestmentGrowthRow,
    NewClientImportRow,
)

AUDITABLE_TIPOS = frozenset(
    set(DISPATCH_IMPORT_TIPOS)
    | {str(r["tipo"]) for r in CLI_IMPORT_COMMANDS if r.get("tipo")}
)

FILE_UPLOAD_TIPO = {
    FileUpload.TYPE_NEW_CLIENTS: "new_clients",
    FileUpload.TYPE_CROSS_SALE: "cross_sale",
    FileUpload.TYPE_INVESTMENT_GROWTH: "investment_growth",
    FileUpload.TYPE_BANK_LOANS: "bank_loans",
    FileUpload.TYPE_FINANCIAL: "financial",
}

BATCH_TIPO = {
    (DataImportBatch.MODULO_CRM, "infoclientes_wcg"): "crm_clientes",
    (DataImportBatch.MODULO_PGO, "tickets"): "pgo_tickets",
    (DataImportBatch.MODULO_PGO, "archivos_catalogo"): "pgo_catalogo",
    (DataImportBatch.MODULO_PGO, "archivos_expedientes"): "pgo_expedientes",
    (DataImportBatch.MODULO_RISK, "leasing_database"): "risk_leasing",
    (DataImportBatch.MODULO_RISK, "leasing_rentas"): "risk_rentas",
}

_MONTH_IN_NAME = re.compile(
    r"(?:^|[^0-9])(2026)[_\-\s/](\d{1,2})(?:[^0-9]|$)|"
    r"BaseLeasing2026(\d{2})|Base_Leasing2026(\d{2})|"
    r"ClientesNuevos_2026-(\d{2})|Clientes_Nuevos_2026-(\d{2})",
    re.I,
)


@dataclass
class BackfillCandidate:
    backfill_id: str
    import_tipo: str
    file_path_key: str
    loaded_at: datetime
    year: int | None = None
    month: int | None = None
    source: str = ImportAuditEvent.SOURCE_OPS
    file_upload_id: int | None = None
    reasoning: str = ""
    evidence: dict = field(default_factory=dict)


def default_inventory_path() -> Path:
    base = Path(settings.BASE_DIR)
    for rel in (
        "../data/other/data-layout-inventory-20261118.tsv",
        "data/other/data-layout-inventory-20261118.tsv",
    ):
        p = (base / rel).resolve()
        if p.is_file():
            return p
    return (base / "../data/other/data-layout-inventory-20261118.tsv").resolve()


def _is_junk_relpath(relpath: str) -> bool:
    name = Path(relpath).name.lower()
    if name.startswith("dup_") or ".fixed." in name or " (1)" in name:
        return True
    if "prod_vc_verify" in name:
        return True
    return False


def load_inventory(path: Path | None = None) -> dict[tuple[str, str], list[str]]:
    path = path or default_inventory_path()
    by_key: dict[tuple[str, str], list[str]] = {}
    if not path.is_file():
        return by_key
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            tipo = (row.get("import_tipo") or "").strip()
            yymm = (row.get("yymm") or "").strip()
            if not tipo or not yymm or tipo not in AUDITABLE_TIPOS:
                continue
            dest = (row.get("dest_relpath") or row.get("relpath") or "").strip()
            if not dest or _is_junk_relpath(dest):
                continue
            by_key.setdefault((tipo, yymm), [])
            if dest not in by_key[(tipo, yymm)]:
                by_key[(tipo, yymm)].append(dest)
    return by_key


def yymm_label(year: int, month: int) -> str:
    return f"{year % 100:02d}{month:02d}"


def loaded_at_day7(year: int, month: int) -> datetime:
    naive = datetime(year, month, 7, 12, 0, 0)
    if timezone.is_naive(naive):
        return timezone.make_aware(naive, timezone.get_current_timezone())
    return naive


def parse_period_from_name(name: str) -> tuple[int, int] | None:
    if not name:
        return None
    m = re.search(r"BaseLeasing2026(\d{2})", name, re.I)
    if m:
        return 2026, int(m.group(1))
    m = re.search(r"Base_Leasing2026(\d{2})", name, re.I)
    if m:
        return 2026, int(m.group(1))
    m = re.search(r"2026[_\-](\d{1,2})", name)
    if m:
        mo = int(m.group(1))
        if 1 <= mo <= 12:
            return 2026, mo
    m = re.search(r"2026-(\d{2})", name)
    if m:
        mo = int(m.group(1))
        if 1 <= mo <= 12:
            return 2026, mo
    return None


def resolve_backfill_user():
    User = get_user_model()
    for username in ("caa", "aamado", "armando"):
        user = User.objects.filter(username__iexact=username, is_active=True).first()
        if user:
            return user, f"username={user.username}"
    user = User.objects.filter(is_staff=True, is_active=True).order_by("id").first()
    if user:
        return user, f"first_active_staff id={user.pk}"
    user = User.objects.filter(is_superuser=True).first()
    return user, "fallback_superuser"


def pick_path(
    inventory: dict[tuple[str, str], list[str]],
    *,
    tipo: str,
    year: int,
    month: int,
    filename_hint: str = "",
    fallback_template: str = "",
) -> tuple[str, str]:
    yymm = yymm_label(year, month)
    paths = inventory.get((tipo, yymm), [])
    clean = [p for p in paths if not _is_junk_relpath(p)]
    if filename_hint:
        hint = filename_hint.lower()
        for p in clean:
            if Path(p).name.lower() == hint.lower() or hint in p.lower():
                return p, "inventory_filename_match"
    if clean:
        return clean[0], "inventory_yymm"
    if filename_hint:
        return f"pgc/{yymm}/{filename_hint}", "upload_filename"
    if fallback_template:
        return fallback_template.format(yymm=yymm, year=year, month=month), "synthetic_template"
    return f"pgc/{yymm}/{tipo}-{yymm}.csv", "synthetic_tipo"


def existing_backfill_ids() -> set[str]:
    ids: set[str] = set()
    for detail in ImportAuditEvent.objects.exclude(detail_json={}).values_list(
        "detail_json", flat=True
    ):
        if isinstance(detail, dict) and detail.get("backfill_id"):
            ids.add(str(detail["backfill_id"]))
    return ids


def is_duplicate_event(
  *, backfill_id: str, file_path_key: str, loaded_at: datetime, known_ids: set[str]
) -> bool:
    if backfill_id in known_ids:
        return True
    if ImportAuditEvent.objects.filter(detail_json__backfill_id=backfill_id).exists():
        return True
    return ImportAuditEvent.objects.filter(
        file_path_key=file_path_key,
        loaded_at__date=loaded_at.date(),
    ).exists()


def _periods_new_clients() -> list[tuple[int, int]]:
    return [
        (r["year"], r["month"])
        for r in NewClientImportRow.objects.values("year", "month")
        .annotate(n=Count("id"))
        .filter(n__gt=0, year=2026)
        .order_by("month")
    ]


def _periods_cross_sale() -> list[tuple[int, int]]:
    return [
        (r["year"], r["month"])
        for r in CrossSaleImportHeader.objects.values("year", "month")
        .annotate(n=Count("id"))
        .filter(n__gt=0, year=2026)
        .order_by("month")
    ]


def _periods_investment() -> list[tuple[int, int]]:
    return [
        (r["year"], r["month"])
        for r in InvestmentGrowthRow.objects.values("year", "month")
        .annotate(n=Count("id"))
        .filter(n__gt=0, year=2026)
        .order_by("month")
    ]


def _periods_bank() -> list[tuple[int, int]]:
    return list(
        BankLoanMonthSnapshot.objects.filter(year=2026)
        .order_by("month")
        .values_list("year", "month")
    )


def _upload_hints_by_period(tipo: str) -> dict[tuple[int, int], FileUpload]:
    out: dict[tuple[int, int], FileUpload] = {}
    for fu in FileUpload.objects.filter(file_type_detected__in=FILE_UPLOAD_TIPO).order_by("id"):
        mapped = FILE_UPLOAD_TIPO.get(fu.file_type_detected)
        if mapped != tipo:
            continue
        year, month = fu.detected_year, fu.detected_month
        if not year or not month:
            parsed = parse_period_from_name(fu.original_filename)
            if parsed:
                year, month = parsed
        if not year or not month:
            continue
        prev = out.get((year, month))
        if prev is None or fu.id > prev.id:
            if not _is_junk_relpath(fu.original_filename):
                out[(year, month)] = fu
    return out


def build_backfill_plan(
    *,
    inventory_path: Path | None = None,
    year_filter: int | None = 2026,
) -> list[BackfillCandidate]:
    inventory = load_inventory(inventory_path)
    candidates: list[BackfillCandidate] = []
    seen_ids: set[str] = set()

    def add(c: BackfillCandidate) -> None:
        if c.backfill_id in seen_ids:
            return
        if year_filter and c.year and c.year != year_filter:
            return
        seen_ids.add(c.backfill_id)
        candidates.append(c)

    upload_nc = _upload_hints_by_period("new_clients")
    for year, month in _periods_new_clients():
        fu = upload_nc.get((year, month))
        hint = fu.original_filename if fu else ""
        path, path_reason = pick_path(
            inventory,
            tipo="new_clients",
            year=year,
            month=month,
            filename_hint=hint,
            fallback_template="pgc/{yymm}/ClientesNuevos_{year}-{month:02d}.csv",
        )
        add(
            BackfillCandidate(
                backfill_id=f"new_clients:{year}-{month:02d}",
                import_tipo="new_clients",
                file_path_key=path,
                loaded_at=loaded_at_day7(year, month),
                year=year,
                month=month,
                source=ImportAuditEvent.SOURCE_OPS,
                file_upload_id=fu.id if fu else None,
                reasoning=f"NewClientImportRow en BD; path={path_reason}",
                evidence={"rows": True, "file_upload_id": fu.id if fu else None},
            )
        )

    upload_xc = _upload_hints_by_period("cross_sale")
    for year, month in _periods_cross_sale():
        fu = upload_xc.get((year, month))
        hint = fu.original_filename if fu else ""
        path, path_reason = pick_path(
            inventory,
            tipo="cross_sale",
            year=year,
            month=month,
            filename_hint=hint,
            fallback_template="pgc/{yymm}/VentaCruzada_{year}-{month:02d}.csv",
        )
        add(
            BackfillCandidate(
                backfill_id=f"cross_sale:{year}-{month:02d}",
                import_tipo="cross_sale",
                file_path_key=path,
                loaded_at=loaded_at_day7(year, month),
                year=year,
                month=month,
                source=ImportAuditEvent.SOURCE_OPS,
                file_upload_id=fu.id if fu else None,
                reasoning=f"CrossSaleImportHeader en BD; path={path_reason}",
            )
        )

    for year, month in _periods_investment():
        path, path_reason = pick_path(
            inventory,
            tipo="investment_growth",
            year=year,
            month=month,
            fallback_template="pgc/{yymm}/Inversiones_crecimiento_{year}_{month:02d}.csv",
        )
        fu = FileUpload.objects.filter(
            file_type_detected=FileUpload.TYPE_INVESTMENT_GROWTH
        ).order_by("-id").first()
        add(
            BackfillCandidate(
                backfill_id=f"investment_growth:{year}-{month:02d}",
                import_tipo="investment_growth",
                file_path_key=path,
                loaded_at=loaded_at_day7(year, month),
                year=year,
                month=month,
                source=ImportAuditEvent.SOURCE_OPS,
                file_upload_id=fu.id if fu and month in (8, 9, 10) else None,
                reasoning=f"InvestmentGrowthRow en BD; path={path_reason}",
            )
        )

    upload_bank = _upload_hints_by_period("bank_loans")
    for year, month in _periods_bank():
        fu = upload_bank.get((year, month))
        hint = fu.original_filename if fu else ""
        path, path_reason = pick_path(
            inventory,
            tipo="bank_loans",
            year=year,
            month=month,
            filename_hint=hint,
            fallback_template="pgc/{yymm}/Capital_Bancos_{year}_{month:02d}.csv",
        )
        add(
            BackfillCandidate(
                backfill_id=f"bank_loans:{year}-{month:02d}",
                import_tipo="bank_loans",
                file_path_key=path,
                loaded_at=loaded_at_day7(year, month),
                year=year,
                month=month,
                source=ImportAuditEvent.SOURCE_OPS,
                file_upload_id=fu.id if fu else None,
                reasoning=f"BankLoanMonthSnapshot en BD; path={path_reason}",
            )
        )

    for batch in DataImportBatch.objects.filter(status=DataImportBatch.STATUS_OK).order_by(
        "id"
    ):
        key = (batch.modulo, batch.tipo_importacion)
        tipo = BATCH_TIPO.get(key)
        if not tipo or tipo not in AUDITABLE_TIPOS:
            continue
        period = parse_period_from_name(batch.archivo_nombre)
        year, month = period if period else (None, None)
        if year and month:
            path, path_reason = pick_path(
                inventory,
                tipo=tipo,
                year=year,
                month=month,
                filename_hint=batch.archivo_nombre,
            )
            loaded = loaded_at_day7(year, month)
        else:
            path = batch.archivo_nombre
            path_reason = "batch_filename"
            loaded = batch.created_at if batch.created_at else timezone.now()
        add(
            BackfillCandidate(
                backfill_id=f"batch:{batch.id}",
                import_tipo=tipo,
                file_path_key=path,
                loaded_at=loaded,
                year=year,
                month=month,
                source=ImportAuditEvent.SOURCE_OPS,
                reasoning=(
                    f"DataImportBatch OK id={batch.id} modulo={batch.modulo}; "
                    f"path={path_reason}"
                ),
                evidence={"batch_id": batch.id, "archivo": batch.archivo_nombre},
            )
        )

    return candidates