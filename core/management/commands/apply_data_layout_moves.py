"""Mueve archivos a data/pgc|pgo/YYMM u otros/ según inventario (dry-run por defecto)."""

from __future__ import annotations

from django.core.management.base import BaseCommand

from core.services.data_layout import (
    apply_moves,
    inventory_rows,
    repo_data_root,
    write_reclass_report,
    write_reorg_summary,
)


class Command(BaseCommand):
    help = (
        "Aplica movimientos layout: por defecto --dry-run. "
        "Use --apply para ejecutar mv (nunca borra). Actualiza manifest.json al mover a YYMM."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Ejecutar mv real (sin esto solo dry-run).",
        )
        parser.add_argument(
            "--include-ambiguous",
            action="store_true",
            help="Incluir filas ambiguas hacia data/*/otros/ (no recomendado).",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Máximo de movimientos a procesar (0 = sin límite).",
        )

    def handle(self, *args, **options):
        dry_run = not options["apply"]
        root = repo_data_root()
        rows = inventory_rows(root)
        summary = apply_moves(
            root,
            rows,
            dry_run=dry_run,
            include_ambiguous=options["include_ambiguous"],
            limit=options["limit"] or None,
        )
        mode = "DRY-RUN" if dry_run else "APPLY"
        self.stdout.write(self.style.WARNING(f"Modo: {mode}"))
        self.stdout.write(f"Ejecutados/planificados: {summary['done']}")
        self.stdout.write(f"Omitidos: {summary['skipped']}")
        if summary.get("collisions"):
            self.stdout.write(self.style.WARNING(f"Colisiones: {len(summary['collisions'])}"))
            for c in summary["collisions"][:15]:
                self.stdout.write(f"  - {c}")
        if summary["errors"]:
            self.stdout.write(self.style.ERROR(f"Errores: {len(summary['errors'])}"))
            for e in summary["errors"][:20]:
                self.stdout.write(f"  - {e}")
        summary["dry_run"] = dry_run
        report = write_reorg_summary(root, rows, summary)
        self.stdout.write(f"Resumen: {report}")
        reclass = write_reclass_report(
            root, rows, summary, report_name="data-layout-reclass-20261118"
        )
        self.stdout.write(f"Reclasificación: {reclass}")
        if not dry_run and summary["done"]:
            self.stdout.write(self.style.SUCCESS("Movimientos aplicados; revisar manifest.json por mes."))
        elif dry_run:
            self.stdout.write("Sin cambios en disco. Use --apply tras revisar inventario.")