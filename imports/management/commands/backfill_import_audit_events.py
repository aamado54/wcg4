"""Backfill sintético de ImportAuditEvent para cargas históricas ya en BD."""

from __future__ import annotations

from collections import Counter
from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from imports.backfill_import_audit_plan import (
    BackfillCandidate,
    build_backfill_plan,
    is_duplicate_event,
    resolve_backfill_user,
)
from imports.models import ImportAuditEvent


class Command(BaseCommand):
    help = (
        "Genera ImportAuditEvent sintéticos para importaciones que ya dejaron datos "
        "en BD (dry-run por defecto; --apply para insertar)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Insertar eventos (sin esto solo dry-run).",
        )
        parser.add_argument(
            "--year",
            type=int,
            default=2026,
            help="Filtrar períodos de este año (default 2026).",
        )
        parser.add_argument(
            "--inventory",
            type=str,
            default="",
            help="Ruta TSV inventario data-layout (opcional).",
        )
        parser.add_argument(
            "--user-id",
            type=int,
            default=0,
            help="Forzar usuario (default: caa / staff ops).",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Máximo eventos a crear (0 = sin límite).",
        )

    def handle(self, *args, **options):
        apply = options["apply"]
        year = options["year"]
        inv = Path(options["inventory"]) if options.get("inventory") else None

        if options["user_id"]:
            from django.contrib.auth import get_user_model

            user = get_user_model().objects.filter(
                pk=options["user_id"], is_active=True
            ).first()
            user_note = f"forced user_id={options['user_id']}"
        else:
            user, user_note = resolve_backfill_user()

        if user is None:
            self.stderr.write(self.style.ERROR("No hay usuario activo para backfill."))
            return

        plan = build_backfill_plan(inventory_path=inv, year_filter=year)
        backfill_date = timezone.now().date().isoformat()

        to_create: list[BackfillCandidate] = []
        skipped = 0
        for cand in plan:
            if is_duplicate_event(
                backfill_id=cand.backfill_id,
                file_path_key=cand.file_path_key,
                loaded_at=cand.loaded_at,
                known_ids=set(),
            ):
                skipped += 1
                continue
            to_create.append(cand)

        if options["limit"] and len(to_create) > options["limit"]:
            to_create = to_create[: options["limit"]]

        self.stdout.write(
            f"Plan: {len(plan)} candidatos | crear={len(to_create)} | "
            f"omitidos(idempotencia)={skipped} | usuario={user.pk} ({user.username}) "
            f"[{user_note}]"
        )

        by_tipo = Counter(c.import_tipo for c in to_create)
        by_month: Counter[tuple[str, int | None]] = Counter()
        for c in to_create:
            by_month[(c.import_tipo, c.month)] += 1

        self.stdout.write("Por tipo (a crear):")
        for tipo, n in sorted(by_tipo.items()):
            self.stdout.write(f"  {tipo}: {n}")

        for cand in to_create[:15]:
            self.stdout.write(
                f"  + {cand.backfill_id} | {cand.import_tipo} | "
                f"{cand.loaded_at.date()} | {cand.file_path_key}"
            )
        if len(to_create) > 15:
            self.stdout.write(f"  … y {len(to_create) - 15} más.")

        if not apply:
            self.stdout.write(self.style.WARNING("Dry-run: use --apply para insertar."))
            return

        created = 0
        with transaction.atomic():
            for cand in to_create:
                fu = None
                if cand.file_upload_id:
                    from imports.models import FileUpload

                    fu = FileUpload.objects.filter(pk=cand.file_upload_id).first()

                ImportAuditEvent.objects.create(
                    user=user,
                    file_path_key=cand.file_path_key[:512],
                    file_available=False,
                    loaded_at=cand.loaded_at,
                    success=True,
                    error_message="",
                    source=cand.source,
                    import_tipo=cand.import_tipo[:50],
                    file_upload=fu,
                    detail_json={
                        "synthetic_backfill": True,
                        "backfill_date": backfill_date,
                        "backfill_id": cand.backfill_id,
                        "reasoning": cand.reasoning,
                        "evidence": cand.evidence,
                    },
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"ImportAuditEvent creados: {created}"))