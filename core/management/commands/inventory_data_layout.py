"""Inventario de data/ y reporte TSV/MD (sin mover archivos)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand

from core.services.data_layout import inventory_rows, repo_data_root, write_inventory_report


class Command(BaseCommand):
    help = (
        "Inventario de archivos bajo data/ (pgc/pgo/ger/pla/dudas), YYMM y acción. "
        "Escribe reporte en data/done/; no mueve archivos."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--report",
            type=str,
            default="",
            help="Ruta del reporte (default data/done/data-layout-inventory-YYYYMMDD.tsv).",
        )
        parser.add_argument(
            "--format",
            choices=("tsv", "md", "both"),
            default="both",
            help="Formato de salida (default both).",
        )

    def handle(self, *args, **options):
        root = repo_data_root()
        rows = inventory_rows(root)
        today = date.today().strftime("%Y%m%d")
        default = root / "done" / f"data-layout-inventory-{today}.tsv"
        report_path = Path(options["report"]) if options["report"] else default
        if not report_path.is_absolute():
            report_path = root.parent / report_path if str(report_path).startswith("data/") else report_path

        paths = write_inventory_report(rows, report_path, fmt=options["format"])
        moves = sum(1 for r in rows if r.action == "move_yymm" and not r.ambiguous)
        otros = sum(1 for r in rows if r.action == "move_otros")
        stay = sum(1 for r in rows if r.action == "stay")
        self.stdout.write(self.style.SUCCESS(f"Inventario: {len(rows)} archivos"))
        self.stdout.write(f"  move_yymm (claro): {moves}")
        self.stdout.write(f"  move_otros / stay: {otros} / {stay}")
        for p in paths:
            self.stdout.write(f"Reporte: {p}")