"""Carga los archivos de demo desde el directorio data/ hacia los módulos WCG."""

from __future__ import annotations

from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from imports.dispatch import run_import_path
from pgo.periodo import recalculate_pgo_periodos

User = get_user_model()

# Orden importa: CRM y leasing base antes de rentas
DEFAULT_FILES = [
    ("crm datos - InfoClientesWCG para CRM.csv", None),
    ("pgo datos - control de tickets marzo abril y mayo 2026 para PGO.xlsx", "pgo_tickets"),
    ("pgo datos - Archivos para PGO.csv", "pgo_catalogo"),
    ("BaseLeasing202606.csv", "risk_leasing"),
    ("balon datos - BaseLeasing202605.csv", "risk_leasing"),
    ("LeasingRentas2026-06-30.csv", "risk_rentas"),
]


class Command(BaseCommand):
    help = "Importa archivos de /wcg4/data o demo_data/ vía Importación General"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir",
            default="",
            help="Directorio de datos (default: demo_data/ o ../data)",
        )
        parser.add_argument("--user", default="", help="Username que registra los lotes")

    def handle(self, *args, **options):
        base = Path(options["dir"]) if options["dir"] else self._default_data_dir()
        if not base.exists():
            self.stderr.write(self.style.ERROR(f"No existe directorio: {base}"))
            return

        user = None
        if options["user"]:
            user = User.objects.filter(username=options["user"]).first()
        user = user or User.objects.filter(is_superuser=True).first() or User.objects.first()
        if not user:
            self.stderr.write(self.style.ERROR("No hay usuario para asociar lotes."))
            return

        self.stdout.write(f"Importando desde {base} como {user.username}")
        for filename, forced in DEFAULT_FILES:
            path = base / filename
            if not path.exists():
                self.stdout.write(self.style.WARNING(f"  skip (no encontrado): {filename}"))
                continue
            result = run_import_path(user, str(path), tipo_forzado=forced)
            style = self.style.SUCCESS if result.ok else self.style.WARNING
            self.stdout.write(style(f"  [{result.tipo}] {filename}: {result.message}"))

        recalculate_pgo_periodos()
        self.stdout.write(self.style.SUCCESS("Recálculo PGO OK. Importación general finalizada."))

    def _default_data_dir(self) -> Path:
        here = Path(__file__).resolve()
        candidates = [
            here.parents[3] / "demo_data",  # dashboard/demo_data (deploy)
            here.parents[4] / "data",  # /wc/wcg4/data
            here.parents[3] / "data" / "wcg",
            Path("/app/demo_data"),
            Path("/home/caa/wc/wcg4/data"),
        ]
        for c in candidates:
            if c.exists():
                return c
        return candidates[0]
