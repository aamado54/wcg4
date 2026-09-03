# imports/management/commands/recalc_investment_ingresos_from_new_clients.py

from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import MetricDefinition
from pgc.investment_ingresos import get_investment_une, sum_investment_ingresos_usd
from pgc.models import (
    MonthlyMetricResult,
    MonthlyTarget,
    PGCPlan,
)


class Command(BaseCommand):
    help = (
        "Recalcula INGRESOS de INVESTMENT desde crecimiento neto mensual "
        "(AP + PG + préstamos bancarios, dolarizado en miles USD). "
        "Si no hay archivos de crecimiento, usa clientes nuevos como fallback."
    )

    def add_arguments(self, parser):
        parser.add_argument("--year", type=int, required=True)
        parser.add_argument("--month", type=int, required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        year = options["year"]
        month = options["month"]

        try:
            plan = PGCPlan.objects.get(year=year)
        except PGCPlan.DoesNotExist:
            raise CommandError(f"No existe PGCPlan para {year}.")

        une = get_investment_une()
        if not une:
            raise CommandError("No existe UNE Investment.")

        try:
            metric = MetricDefinition.objects.get(
                code=MetricDefinition.CODE_INGRESOS
            )
        except MetricDefinition.DoesNotExist:
            raise CommandError("No existe MetricDefinition para CODE_INGRESOS.")

        try:
            target = MonthlyTarget.objects.get(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
            )
        except MonthlyTarget.DoesNotExist:
            raise CommandError(
                f"No existe MonthlyTarget para INGRESOS INVESTMENT "
                f"{year}-{month:02d}."
            )

        summary = sum_investment_ingresos_usd(year, month, une=une)
        fx = summary["fx"]
        if fx in (None, Decimal("0")):
            from pgc.models import MonthlyExchangeRate

            latest = MonthlyExchangeRate.objects.order_by("-year", "-month").first()
            if latest and latest.usd_to_gtq:
                fx = latest.usd_to_gtq
                self.stdout.write(
                    self.style.WARNING(
                        f"Sin TC {year}-{month:02d}; se usa {latest.year}-{latest.month:02d} = {fx}."
                    )
                )
            else:
                raise CommandError(
                    f"No existe MonthlyExchangeRate válido para {year}-{month:02d}."
                )

        total_usd = summary["total_usd"]
        used_rows = summary["used_rows"]
        source = summary.get("source", "new_clients")
        gross = summary.get("gross") or {}
        growth_usd = summary.get("growth_usd")

        mmr, _ = MonthlyMetricResult.objects.get_or_create(
            plan=plan,
            une=une,
            metric=metric,
            year=year,
            month=month,
            defaults={"target_value": target.target_value},
        )

        mmr.target_value = target.target_value
        mmr.measured_value = total_usd
        mmr.source_currency = MonthlyMetricResult.CURRENCY_USD
        mmr.source_value = total_usd
        mmr.exchange_rate_used = fx
        mmr.conversion_status = MonthlyMetricResult.CONVERSION_NATIVE_USD
        mmr.is_achieved = (
            total_usd >= target.target_value
            if target.target_value is not None
            else False
        )
        mmr.points_awarded = (
            target.points_if_achieved if mmr.is_achieved else 0
        )
        if source == "investment_growth":
            note = summary.get("note") or ""
            if growth_usd is not None:
                mmr.calculation_note = (
                    "INVESTMENT INGRESOS = crecimiento neto mensual dolarizado "
                    f"(AP+PG+bancos). Bruto USD={gross.get('total_usd')}; "
                    f"Δ mes={growth_usd}; miles={total_usd}. "
                    f"Operaciones={used_rows}. TC={fx}."
                )
            else:
                mmr.calculation_note = (
                    "INVESTMENT INGRESOS sin crecimiento neto: "
                    f"no hay saldo del mes anterior. Bruto USD={gross.get('total_usd')}. "
                    f"{note}"
                )
        else:
            mmr.calculation_note = (
                "INVESTMENT INGRESOS recalculado desde NewClientImportRow "
                f"(fallback; todos los registros del mes). Filas={used_rows}. "
                f"GTQ->USD usando TC={fx} del {year}-{month:02d}. "
                f"TotalUSD={total_usd}."
            )
        mmr.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Actualizado INGRESOS INVESTMENT {year}-{month:02d}: "
                f"USD {total_usd} con {used_rows} filas."
            )
        )
