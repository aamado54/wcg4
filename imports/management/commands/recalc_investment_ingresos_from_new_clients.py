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
        "Recalcula INGRESOS de INVESTMENT desde NewClientImportRow "
        "(misma lógica que /pgc/ingresos/: todos los registros del mes; "
        "amount ya está en miles, sin volver a dividir entre 1000)."
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
            raise CommandError(
                f"No existe MonthlyExchangeRate válido para {year}-{month:02d}."
            )

        total_usd = summary["total_usd"]
        used_rows = summary["used_rows"]

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
        mmr.calculation_note = (
            "INVESTMENT INGRESOS recalculado desde NewClientImportRow "
            f"(todos los registros del mes; alineado con /pgc/ingresos/). "
            f"Filas={used_rows}. "
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
