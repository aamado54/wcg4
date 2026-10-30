"""Aplica comisiones GTQ del TSV EEFF a MonthlyMetricResult (INGRESOS F/L/I)."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import MetricDefinition, UNE
from imports.ingresos_er_parse import (
    load_comisiones_tsv,
    objetivos_style_ingresos_values,
)
from pgc.income_conversion import apply_result_achievement
from pgc.models import MonthlyExchangeRate, MonthlyMetricResult, MonthlyTarget, PGCPlan


class Command(BaseCommand):
    help = (
        "Importa comisiones mensuales GTQ desde TSV Ingresos-Financieros "
        "y actualiza INGRESOS por UNE (FACTORING, LEASING, INSURANCE)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            required=True,
            help="Ruta al TSV (ej. /app/media/audit/comisiones-2026.tsv).",
        )
        parser.add_argument(
            "--year",
            type=int,
            default=2026,
            help="Año del plan y filas a aplicar (default 2026).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Solo muestra cambios sin escribir en BD.",
        )

    def _get_exchange_rate(self, year: int, month: int) -> Decimal:
        try:
            rate = MonthlyExchangeRate.objects.get(year=year, month=month)
        except MonthlyExchangeRate.DoesNotExist:
            raise CommandError(
                f"No existe tipo de cambio para {year}-{month:02d}."
            )
        if rate.usd_to_gtq in (None, Decimal("0")):
            raise CommandError(
                f"Tipo de cambio inválido para {year}-{month:02d}: {rate.usd_to_gtq}"
            )
        return rate.usd_to_gtq

    @transaction.atomic
    def handle(self, *args, **options):
        path = Path(options["path"]).expanduser()
        year = options["year"]
        dry_run = options["dry_run"]

        if not path.is_file():
            raise CommandError(f"Archivo no encontrado: {path}")

        ref = load_comisiones_tsv(path)
        if not ref:
            raise CommandError(f"TSV sin filas parseables: {path}")

        try:
            plan = PGCPlan.objects.get(year=year)
        except PGCPlan.DoesNotExist:
            raise CommandError(f"No existe PGCPlan para year={year}")

        try:
            metric = MetricDefinition.objects.get(
                code=MetricDefinition.CODE_INGRESOS
            )
        except MetricDefinition.DoesNotExist:
            raise CommandError("No existe MetricDefinition CODE_INGRESOS")

        updated = 0
        for (une_code, row_year, month), gtq in sorted(ref.items()):
            if row_year != year:
                continue
            if une_code == "INVESTMENT":
                continue

            try:
                une = UNE.objects.get(code=une_code)
            except UNE.DoesNotExist:
                raise CommandError(f"UNE {une_code} no existe.")

            tipo_cambio = self._get_exchange_rate(year, month)
            source_value, ingreso_usd_miles = objetivos_style_ingresos_values(
                gtq, tipo_cambio
            )

            try:
                target = MonthlyTarget.objects.get(
                    plan=plan,
                    une=une,
                    metric=metric,
                    year=year,
                    month=month,
                )
            except MonthlyTarget.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Sin MonthlyTarget INGRESOS {une_code} {year}-{month:02d}; omitido."
                    )
                )
                continue

            label = (
                f"{une_code} {year}-{month:02d}: GTQ={gtq} "
                f"miles={ingreso_usd_miles} fx={tipo_cambio}"
            )
            if dry_run:
                self.stdout.write(f"[dry-run] {label}")
                updated += 1
                continue

            mmr, _ = MonthlyMetricResult.objects.get_or_create(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
                defaults={"target_value": target.target_value},
            )
            mmr.target_value = target.target_value
            mmr.source_currency = MonthlyMetricResult.CURRENCY_GTQ
            mmr.source_value = source_value
            mmr.exchange_rate_used = tipo_cambio
            mmr.conversion_status = MonthlyMetricResult.CONVERSION_CONVERTED
            mmr.measured_value = ingreso_usd_miles
            apply_result_achievement(mmr, target)
            mmr.calculation_note = (
                f"Ingreso desde TSV {path.name} (tsv_comisiones). "
                f"ComisionesGTQ={gtq}, TipoCambioGTQxUSD={tipo_cambio}, "
                f"USD miles={ingreso_usd_miles}, UNE={une_code}."
            )
            mmr.save()
            updated += 1
            self.stdout.write(self.style.SUCCESS(label))

        if dry_run:
            self.stdout.write(
                self.style.WARNING(f"Dry-run: {updated} fila(s) listas para aplicar.")
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Import TSV comisiones completado: {updated} fila(s) desde {path.name}."
            )
        )

        if updated:
            try:
                from pgc.admin_recalc import maybe_auto_recalc

                auto = maybe_auto_recalc(source="import_ingresos_comisiones_tsv")
                if auto and auto.get("ran"):
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Auto-recalcular: {auto.get('periods_processed', 0)} período(s)."
                        )
                    )
            except Exception as exc:
                self.stdout.write(
                    self.style.WARNING(f"Auto-recalcular no completó: {exc}")
                )
