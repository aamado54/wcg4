"""Bootstrap demo data on deployed environments (e.g. wcg.lol / Railway).

Usage on production (Railway shell or one-off):
  python manage.py bootstrap_wcg_demo --dir /app/data
  python manage.py bootstrap_wcg_demo --seed-only
  python manage.py bootstrap_wcg_demo --load-only --dir /app/../data
"""

from __future__ import annotations

from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed + carga de datos WCG para demo en producción"

    def add_arguments(self, parser):
        parser.add_argument("--dir", default="", help="Directorio con CSV/XLSX de data/")
        parser.add_argument("--seed-only", action="store_true")
        parser.add_argument("--load-only", action="store_true")

    def handle(self, *args, **options):
        if not options["load_only"]:
            self.stdout.write("→ seed_wcg_demo")
            call_command("seed_wcg_demo")

        if not options["seed_only"]:
            data_dir = options["dir"] or self._guess_data_dir()
            self.stdout.write(f"→ load_wcg_data --dir {data_dir}")
            call_command("load_wcg_data", dir=str(data_dir))

        self.stdout.write(self.style.SUCCESS("Bootstrap WCG demo finalizado."))

    def _guess_data_dir(self) -> Path:
        here = Path(__file__).resolve()
        candidates = [
            here.parents[3] / "demo_data",
            Path("/app/demo_data"),
            here.parents[4] / "data",
            Path("/home/caa/wc/wcg4/data"),
            here.parents[3] / "data" / "wcg",
        ]
        for c in candidates:
            if c.exists():
                return c
        return candidates[0]
