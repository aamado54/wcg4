"""
Regresión PGC: baseline «sep-save» y réplica solo con imports operativos.

Uso típico (sep 2026):
  python manage.py pgc_operational_regression save --tag sep-save --year 2026 --month 9
  python manage.py pgc_operational_regression rebuild --year 2026 --month 9
  python manage.py pgc_operational_regression verify --tag sep-save --year 2026 --month 9
"""

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from pgc.operational_baseline import (
    baseline_path,
    compare_period_to_baseline,
    export_period_baseline,
    load_baseline_file,
    save_baseline_file,
)

SEP_2026_MANIFEST = {
    "clientes_csv": [
        "data/now/ClientesNuevos_2026-09_20261008.csv",
        "../data/now/ClientesNuevos_2026-09_20261008.csv",
    ],
    "inversiones_csv": [
        "data/now/Inversiones_crecimiento_2026_09.csv",
        "../data/now/Inversiones_crecimiento_2026_09.csv",
    ],
    "bancos_csv": [
        "data/now/Capital_Bancos_2026_09.csv",
        "../data/now/Capital_Bancos_2026_09.csv",
    ],
    "pga_mensuales_xlsx": [
        "data/now/0/PGA Mensuales WC WCL WCI 2026.xlsx",
        "../data/now/0/PGA Mensuales WC WCL WCI 2026.xlsx",
    ],
}


def _resolve_manifest_path(candidates: list[str]) -> Path:
    base = Path(settings.BASE_DIR)
    for rel in candidates:
        p = (base / rel).resolve() if not rel.startswith("/") else Path(rel)
        if p.is_file():
            return p
    raise CommandError(
        "No se encontró archivo operativo. Rutas probadas: "
        + ", ".join(candidates)
    )


class Command(BaseCommand):
    help = (
        "Guarda baseline PGC (sep-save), reconstruye un mes solo con imports "
        "operativos y verifica coincidencia al centavo en modo2."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            choices=("save", "rebuild", "verify"),
            help="save=exportar baseline; rebuild=imports operativos; verify=comparar.",
        )
        parser.add_argument("--tag", type=str, default="sep-save")
        parser.add_argument("--year", type=int, default=2026)
        parser.add_argument("--month", type=int, default=9)
        parser.add_argument(
            "--baseline-path",
            type=str,
            default="",
            help="JSON baseline (default pgc/fixtures/baselines/{tag}-YYYY-MM.json).",
        )
        parser.add_argument(
            "--skip-bancos",
            action="store_true",
            help="No importar Capital_Bancos (si el archivo no está disponible).",
        )

    def handle(self, *args, **options):
        action = options["action"]
        tag = options["tag"]
        year = options["year"]
        month = options["month"]

        if action == "save":
            payload = export_period_baseline(tag=tag, year=year, month=month)
            path = (
                Path(options["baseline_path"])
                if options["baseline_path"]
                else baseline_path(tag, year, month)
            )
            save_baseline_file(payload, path)
            self.stdout.write(self.style.SUCCESS(f"Baseline guardado: {path}"))
            return

        if action == "rebuild":
            self._rebuild_operational(year, month, skip_bancos=options["skip_bancos"])
            call_command("recalc_pgc", year=year, month=month, mode="modo1")
            call_command("recalc_pgc", year=year, month=month, mode="modo2")
            self.stdout.write(
                self.style.SUCCESS(
                    f"Rebuild operativo {year}-{month:02d} completado; recalc modo1+modo2."
                )
            )
            return

        if action == "verify":
            path = (
                Path(options["baseline_path"])
                if options["baseline_path"]
                else baseline_path(tag, year, month)
            )
            if not path.is_file():
                raise CommandError(f"Baseline no encontrado: {path}")
            baseline = load_baseline_file(path)
            diffs = compare_period_to_baseline(
                baseline=baseline, year=year, month=month, mode="modo2"
            )
            if not diffs:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"OK: {year}-{month:02d} coincide con baseline «{tag}» (modo2)."
                    )
                )
                return
            self.stdout.write(
                self.style.ERROR(
                    f"Diferencias {year}-{month:02d} vs «{tag}»: {len(diffs)}"
                )
            )
            for d in diffs[:40]:
                self.stdout.write(f"  {d}")
            if len(diffs) > 40:
                self.stdout.write(f"  … y {len(diffs) - 40} más.")
            raise CommandError("Verificación de regresión fallida.")

    @transaction.atomic
    def _rebuild_operational(self, year: int, month: int, *, skip_bancos: bool) -> None:
        if year == 2026 and month == 9:
            manifest = SEP_2026_MANIFEST
        else:
            raise CommandError(
                "Solo hay manifiesto operativo codificado para 2026-09; "
                "extienda SEP_2026_MANIFEST o pase rutas en futuras versiones."
            )

        clientes = _resolve_manifest_path(manifest["clientes_csv"])
        inv = _resolve_manifest_path(manifest["inversiones_csv"])
        pga = _resolve_manifest_path(manifest["pga_mensuales_xlsx"])

        self.stdout.write(f"→ import_clientes_nuevos {clientes.name}")
        call_command("import_clientes_nuevos", path=str(clientes))

        self.stdout.write(f"→ import_inversiones_crecimiento {inv.name}")
        call_command("import_inversiones_crecimiento", path=str(inv))

        if not skip_bancos:
            try:
                bancos = _resolve_manifest_path(manifest["bancos_csv"])
            except CommandError:
                self.stdout.write(
                    self.style.WARNING("Capital_Bancos omitido (archivo no encontrado).")
                )
            else:
                self.stdout.write(f"→ import_bancos_fin_mes {bancos.name}")
                call_command("import_bancos_fin_mes", path=str(bancos))

        self.stdout.write("→ recalc_investment_ingresos_from_new_clients")
        call_command(
            "recalc_investment_ingresos_from_new_clients",
            year=year,
            month=month,
        )

        for une_code in ("FACTORING", "LEASING", "INSURANCE"):
            self.stdout.write(
                f"→ import_ingresos PGA {une_code} ({pga.name})"
            )
            call_command(
                "import_ingresos",
                path=str(pga),
                year=year,
                month=month,
                une_code=une_code,
            )
