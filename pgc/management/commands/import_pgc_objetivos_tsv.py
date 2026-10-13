"""Carga ejecución Objetivos desde export TSV (hoja Objetivos) para todos los meses del archivo."""

from __future__ import annotations

import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from pgc.excel_import_guard import assert_pgc_objetivos_import_allowed

MONTHS = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}

UEN_TO_UNE = {
    "WC": "FACTORING",
    "WCL": "LEASING",
    "WCI": "INSURANCE",
    "WCINV": "INVESTMENT",
}


def _dec(raw):
    if raw is None:
        return None
    s = str(raw).strip().replace(",", "").replace(" ", "")
    if not s or s.upper() in ("-", "NOAPLICA", "NO APLICA"):
        return None
    if s.startswith("- "):
        s = "-" + s[2:]
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def _parse_mes(mes: str) -> tuple[int, int] | None:
    mes = (mes or "").strip()
    if "-" not in mes:
        return None
    mon_s, yr_s = mes.split("-", 1)
    mon = MONTHS.get(mon_s[:3].title())
    if not mon:
        return None
    try:
        yr = int(yr_s)
        if yr < 100:
            yr += 2000
    except ValueError:
        return None
    return yr, mon


class Command(BaseCommand):
    help = "Importa Objetivos desde TSV (todos los meses presentes) vía import_pgc_objetivos por mes."

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, required=True)
        parser.add_argument("--year", type=int, default=None, help="Filtrar solo este año")
        parser.add_argument(
            "--write-staging-xlsx",
            type=str,
            default="",
            help="Opcional: escribe xlsx temporal (no usado si vacío).",
        )
        parser.add_argument(
            "--force-legacy-excel",
            action="store_true",
            help="Permite import TSV/xlsx Objetivos sin ALLOW_PGC_EXCEL_IMPORT=1.",
        )

    def handle(self, *args, **options):
        assert_pgc_objetivos_import_allowed(
            self, force_legacy_excel=options.get("force_legacy_excel", False)
        )
        path = Path(options["path"]).expanduser()
        if not path.is_file():
            raise CommandError(f"No existe: {path}")

        periods: set[tuple[int, int]] = set()
        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                parsed = _parse_mes(row.get("Mes"))
                if not parsed:
                    continue
                year, month = parsed
                if options["year"] and year != options["year"]:
                    continue
                uen = (row.get("UEN") or "").strip().upper()
                if uen not in UEN_TO_UNE:
                    continue
                periods.add((year, month))

        if not periods:
            raise CommandError("Sin filas Objetivos válidas en el TSV.")

        # Reutiliza import mensual escribiendo un xlsx mínimo sería pesado;
        # duplicamos la lógica llamando import por mes con datos del TSV vía subcomando interno.
        # Si el path es xlsx, delegar por mes
        if path.suffix.lower() in (".xlsx", ".xlsm"):
            for year, month in sorted(periods):
                self.stdout.write(f"Import {year}-{month:02d} desde xlsx...")
                call_command(
                    "import_pgc_objetivos",
                    path=str(path),
                    year=year,
                    month=month,
                    force_legacy_excel=options.get("force_legacy_excel", False),
                )
            return

        # TSV: aplicar misma lógica que import_pgc_objetivos por cada mes
        from core.models import MetricDefinition, UNE
        from django.db import transaction
        from pgc.income_conversion import apply_result_achievement
        from pgc.models import MonthlyExchangeRate, MonthlyMetricResult, MonthlyTarget, PGCPlan

        from pgc.management.commands.import_pgc_objetivos import _gtq_comisiones_to_usd_miles

        metric_cli = MetricDefinition.objects.get(code=MetricDefinition.CODE_CLIENTES_NUEVOS)
        metric_ing = MetricDefinition.objects.get(code=MetricDefinition.CODE_INGRESOS)

        with path.open(encoding="utf-8-sig", newline="") as f:
            all_rows = list(csv.DictReader(f, delimiter="\t"))

        for year, month in sorted(periods):
            plan = PGCPlan.objects.filter(year=year).first()
            if not plan:
                raise CommandError(f"Sin PGCPlan {year}")
            fx_row = MonthlyExchangeRate.objects.filter(year=year, month=month).first()
            if not fx_row or not fx_row.usd_to_gtq:
                self.stdout.write(
                    self.style.WARNING(f"Omitido {year}-{month:02d}: sin TC")
                )
                continue
            fx = fx_row.usd_to_gtq

            with transaction.atomic():
                for row in all_rows:
                    parsed = _parse_mes(row.get("Mes"))
                    if parsed != (year, month):
                        continue
                    uen = (row.get("UEN") or "").strip().upper()
                    if uen not in UEN_TO_UNE:
                        continue
                    une = UNE.objects.get(code=UEN_TO_UNE[uen])
                    exec_cli = _dec(row.get("Clientes Nuevos  (Ejecución Mensual)"))
                    exec_com = _dec(row.get(" Comisiones  (Ejecución Mensual)"))
                    pres_com = _dec(row.get(" Comisiones  (Presupuesto Mensual)"))

                    if exec_cli is not None:
                        tgt_cli = MonthlyTarget.objects.filter(
                            plan=plan,
                            une=une,
                            metric=metric_cli,
                            year=year,
                            month=month,
                        ).first()
                        if tgt_cli:
                            mmr_cli, _ = MonthlyMetricResult.objects.get_or_create(
                                plan=plan,
                                une=une,
                                metric=metric_cli,
                                year=year,
                                month=month,
                                defaults={"target_value": tgt_cli.target_value},
                            )
                            mmr_cli.measured_value = exec_cli
                            mmr_cli.target_value = tgt_cli.target_value
                            mmr_cli.calculation_note = (
                                f"Importado TSV Objetivos {path.name} (clientes)."
                            )
                            apply_result_achievement(mmr_cli, tgt_cli)
                            mmr_cli.save()

                    if exec_com is not None:
                        tgt_ing = MonthlyTarget.objects.filter(
                            plan=plan,
                            une=une,
                            metric=metric_ing,
                            year=year,
                            month=month,
                        ).first()
                        if tgt_ing:
                            usd_miles = _gtq_comisiones_to_usd_miles(exec_com, fx)
                            mmr_ing, _ = MonthlyMetricResult.objects.get_or_create(
                                plan=plan,
                                une=une,
                                metric=metric_ing,
                                year=year,
                                month=month,
                                defaults={"target_value": tgt_ing.target_value},
                            )
                            mmr_ing.source_currency = MonthlyMetricResult.CURRENCY_GTQ
                            mmr_ing.source_value = exec_com
                            mmr_ing.exchange_rate_used = fx
                            mmr_ing.conversion_status = (
                                MonthlyMetricResult.CONVERSION_CONVERTED
                            )
                            mmr_ing.measured_value = usd_miles
                            mmr_ing.target_value = tgt_ing.target_value
                            mmr_ing.calculation_note = (
                                f"Importado TSV Objetivos {path.name} "
                                f"(GTQ={exec_com}, FX={fx})."
                            )
                            apply_result_achievement(mmr_ing, tgt_ing)
                            mmr_ing.save()
                            if pres_com is not None:
                                tgt_ing.presupuesto_gtq = pres_com
                                tgt_ing.save(
                                    update_fields=["presupuesto_gtq", "updated_at"]
                                )

            for mode in ("modo1", "modo2"):
                call_command("recalc_pgc", year=year, month=month, mode=mode)
            self.stdout.write(self.style.SUCCESS(f"OK {year}-{month:02d}"))

        self.stdout.write(self.style.SUCCESS("Import TSV Objetivos completado."))
