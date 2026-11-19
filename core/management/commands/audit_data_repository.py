"""Audita archivos en data/1-pgc … 5-plal y escribe data/done/data-audit-report-YYYYMMDD.md"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand

from core.services.data_layout import repo_data_root
from core.services.data_repository_audit import run_data_repository_audit


class Command(BaseCommand):
    help = (
        "Clasifica archivos en data/1-pgc, 2-pgo, 3-ger, 4-plaf, 5-plal; "
        "marca duplicados y YYMM; escribe data/done/data-audit-report-YYYYMMDD.md."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--root",
            type=str,
            default="",
            help="Raíz data/ alternativa (default: repo data/).",
        )
        parser.add_argument(
            "--stdout-only",
            action="store_true",
            help="No escribe markdown; solo resume en consola.",
        )
        parser.add_argument(
            "--date",
            type=str,
            default="",
            help="Sufijo YYYYMMDD del reporte (default: hoy).",
        )

    def handle(self, *args, **options):
        root = Path(options["root"]).expanduser() if options.get("root") else repo_data_root()
        if not root.is_dir():
            self.stderr.write(self.style.ERROR(f"No existe: {root}"))
            return

        report_date = None
        if options.get("date"):
            raw = options["date"].strip()
            report_date = date(int(raw[:4]), int(raw[4:6]), int(raw[6:8]))

        rows, report_path = run_data_repository_audit(
            root=root,
            write_report=not options.get("stdout_only"),
            report_date=report_date,
        )
        flagged = sum(1 for r in rows if r.flags)
        from core.services.data_repository_audit import find_duplicate_groups

        n_dupes = len(find_duplicate_groups(rows))
        self.stdout.write(
            f"Archivos: {len(rows)} · alertas: {flagged} · grupos organizar: {n_dupes}"
        )
        if report_path:
            self.stdout.write(self.style.SUCCESS(f"Reporte: {report_path}"))
        for mod in ("1-pgc", "2-pgo", "3-ger", "4-plaf", "5-plal"):
            n = sum(1 for r in rows if r.module_key == mod)
            if n:
                self.stdout.write(f"  {mod}: {n}")