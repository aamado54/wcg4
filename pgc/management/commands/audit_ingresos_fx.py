"""Certificación: cero filas INGRESOS con doble FX o miles USD incoherentes."""

import json

from django.core.management.base import BaseCommand, CommandError

from pgc.income_conversion import audit_ingresos_fx_findings


class Command(BaseCommand):
    help = (
        "Audita MonthlyMetricResult INGRESOS (GTQ→miles USD). "
        "Exit code 1 si queda doble FX, mismatch, STALE o filas que repair corregiría. "
        "Gerencia/Risk/PGO no se auditan aquí (otras fuentes)."
    )

    def add_arguments(self, parser):
        parser.add_argument("--year", type=int, default=None)
        parser.add_argument("--month", type=int, default=None)
        parser.add_argument(
            "--json",
            action="store_true",
            help="Salida JSON (para CI o scripts).",
        )

    def handle(self, *args, **options):
        report = audit_ingresos_fx_findings(
            year=options["year"],
            month=options.get("month"),
        )

        if options["json"]:
            self.stdout.write(json.dumps(report, ensure_ascii=False, default=str))
        else:
            c = report["counts"]
            self.stdout.write(
                f"Escaneadas={c.get('scanned', 0)} ok={c.get('ok', 0)} "
                f"legacy_doble_fx={c.get('legacy_double_fx', 0)} "
                f"extra_fx={c.get('extra_fx_division', 0)} "
                f"mismatch={c.get('measured_mismatch', 0)} "
                f"semi_legacy_source={c.get('semi_legacy_source', 0)} "
                f"stale_fx={c.get('stale_fx', 0)} sin_fx={c.get('no_fx', 0)} "
                f"repair_pendiente(dry-run)={report.get('needs_repair', 0)}"
            )
            for s in report.get("samples") or []:
                self.stdout.write(f"  · {s['issue']} {s['period']} {s['une']} …")

        if report["pass"]:
            self.stdout.write(self.style.SUCCESS("PASS — certificación FX ingresos OK."))
            return

        self.stdout.write(
            self.style.ERROR(
                "FAIL — ejecute repair_ingresos_gtq (dry-run primero), "
                "recalc_stale solo tras source GTQ canónico, luego recalc_pgc."
            )
        )
        raise CommandError("Auditoría FX ingresos: quedan outliers.")
