"""Repara GTQ canónico en INGRESOS y recalcula miles USD sin reimportar archivos."""

from django.core.management.base import BaseCommand, CommandError

from pgc.income_conversion import repair_ingresos_gtq_and_usd_miles


class Command(BaseCommand):
    help = (
        "Normaliza source_value a comisiones GTQ y recalcula measured_value (miles USD). "
        "Corrige filas del bug histórico (GTQ/FX guardado como source). "
        "Luego ejecute recalc_pgc."
    )

    def add_arguments(self, parser):
        parser.add_argument("--year", type=int, default=None)
        parser.add_argument("--month", type=int, default=None)
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Solo cuenta filas a reparar, sin escribir en BD.",
        )

    def handle(self, *args, **options):
        try:
            stats = repair_ingresos_gtq_and_usd_miles(
                year=options["year"],
                month=options.get("month"),
                dry_run=options["dry_run"],
            )
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        prefix = "DRY-RUN" if stats["dry_run"] else "OK"
        self.stdout.write(
            self.style.SUCCESS(
                f"{prefix}: escaneadas={stats['scanned']} "
                f"legacy_reparadas={stats['repaired_legacy']} "
                f"solo_miles={stats['repaired_measured']} "
                f"ya_ok={stats['skipped_ok']} "
                f"usd_native={stats['skipped_usd']} "
                f"sin_fx={stats['skipped_no_fx']}"
            )
        )
        self.stdout.write(
            "Railway shell: use /app/.venv/bin/python manage.py … (no hay python3 en PATH)."
        )
