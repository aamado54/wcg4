# imports/management/commands/import_ingresos.py

import argparse
from decimal import Decimal
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import UNE, MetricDefinition
from imports.ingresos_er_parse import (
    infer_prev_er_path,
    is_pga_mensuales_workbook,
    objetivos_style_ingresos_values,
    read_pga_mensuales_comisiones_gtq,
    read_wc_er_comisiones_gtq,
)
from pgc.income_conversion import apply_result_achievement
from pgc.models import PGCPlan, MonthlyTarget, MonthlyMetricResult, MonthlyExchangeRate


class Command(BaseCommand):
    help = (
        "Importa ingresos mensuales desde archivo de estado de resultados "
        "(xlsx) y actualiza la métrica INGRESOS por UNE (no incluye INVESTMENT)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            required=True,
            help="Ruta al archivo de estado de resultados (xlsx).",
        )
        parser.add_argument(
            "--year",
            type=int,
            required=True,
            help="Año del período, por ejemplo 2026.",
        )
        parser.add_argument(
            "--month",
            type=int,
            required=True,
            help="Mes del período, 1-12.",
        )
        parser.add_argument(
            "--prev-path",
            type=str,
            default="",
            help="ER del mes anterior (opcional; se infiere por nombre si falta).",
        )
        parser.add_argument(
            "--une-code",
            type=str,
            default="",
            help="UNE explícita (FACTORING/LEASING/INSURANCE) para PGA Mensuales u otros xlsx sin prefijo WCF/WCL/WCI.",
        )
        parser.add_argument(
            "--er-monthly-saldo",
            action=argparse.BooleanOptionalAction,
            default=True,
            help=(
                "ER WC*: SALDO FINAL de cuentas 4+8 es comisión del mes (default). "
                "Use --no-er-monthly-saldo para delta YTD legacy."
            ),
        )

    def _infer_une_from_filename(self, path: Path) -> UNE:
        name = path.name.upper().strip()

        if name.startswith("WCI"):
            code = "INSURANCE"
        elif name.startswith("WCL"):
            code = "LEASING"
        elif name.startswith("WCF"):
            code = "FACTORING"
        elif name.startswith("WC"):
            code = "FACTORING"
        else:
            raise CommandError(
                f"No se pudo inferir UNE desde el nombre de archivo: {path.name}. "
                "Esperaba prefijos WC / WCF / WCI / WCL."
            )

        try:
            return UNE.objects.get(code=code)
        except UNE.DoesNotExist:
            raise CommandError(f"UNE con code={code} no existe en la base de datos.")

    def _get_exchange_rate(self, year: int, month: int) -> Decimal:
        try:
            rate = MonthlyExchangeRate.objects.get(year=year, month=month)
        except MonthlyExchangeRate.DoesNotExist:
            raise CommandError(
                f"No existe tipo de cambio para {year}-{month:02d}. "
                "Debe registrar MonthlyExchangeRate antes de importar ingresos."
            )

        if rate.usd_to_gtq in (None, Decimal("0")):
            raise CommandError(
                f"Tipo de cambio inválido para {year}-{month:02d}: {rate.usd_to_gtq}"
            )

        return rate.usd_to_gtq

    @transaction.atomic
    def handle(self, *args, **options):
        path = Path(options["path"])
        year = options["year"]
        month = options["month"]

        if not path.exists():
            raise CommandError(f"Archivo no encontrado: {path}")

        prev_path = (
            Path(options["prev_path"]).expanduser()
            if options.get("prev_path")
            else infer_prev_er_path(path, month)
        )

        self.stdout.write(
            self.style.WARNING(f"Leyendo estado de resultados desde {path} ...")
        )
        if prev_path:
            self.stdout.write(f"  ER mes anterior: {prev_path.name}")

        try:
            plan = PGCPlan.objects.get(year=year)
        except PGCPlan.DoesNotExist:
            raise CommandError(f"No existe PGCPlan para year={year}")

        try:
            metric = MetricDefinition.objects.get(
                code=MetricDefinition.CODE_INGRESOS
            )
        except MetricDefinition.DoesNotExist:
            raise CommandError("No existe MetricDefinition para CODE_INGRESOS")

        une_code_opt = (options.get("une_code") or "").strip().upper()
        monthly_saldo = options.get("er_monthly_saldo", True)
        if is_pga_mensuales_workbook(path):
            if not une_code_opt:
                raise CommandError(
                    "Archivo PGA Mensuales: indique --une-code "
                    "(FACTORING, LEASING o INSURANCE)."
                )
            try:
                une = UNE.objects.get(code=une_code_opt)
            except UNE.DoesNotExist:
                raise CommandError(f"UNE {une_code_opt} no existe.")
            ingreso_mensual_gtq = read_pga_mensuales_comisiones_gtq(
                path, une.code, month
            )
            method = "pga_mensuales_comisiones"
        else:
            une = (
                UNE.objects.get(code=une_code_opt)
                if une_code_opt
                else self._infer_une_from_filename(path)
            )
            ingreso_mensual_gtq, method = read_wc_er_comisiones_gtq(
                path,
                month,
                prev_path=prev_path,
                monthly_saldo=monthly_saldo,
            )

        if une.code == "INVESTMENT":
            raise CommandError(
                "Este comando no debe usarse para INVESTMENT; "
                "para esa UNE use el recálculo desde NewClientImportRow."
            )

        self.stdout.write(self.style.WARNING(f"Archivo detectado para UNE={une.code}"))

        tipo_cambio = self._get_exchange_rate(year, month)
        source_value, ingreso_usd_miles = objetivos_style_ingresos_values(
            ingreso_mensual_gtq, tipo_cambio
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
            raise CommandError(
                f"No existe MonthlyTarget para INGRESOS {une.code} "
                f"{year}-{month:02d}."
            )

        if (
            (target.presupuesto_gtq is None or target.presupuesto_gtq <= 0)
            and target.target_value is not None
            and target.target_value > 0
        ):
            target.presupuesto_gtq = Decimal(str(target.target_value)) * Decimal(
                "1000"
            )
            target.save(update_fields=["presupuesto_gtq", "updated_at"])
            self.stdout.write(
                self.style.WARNING(
                    f"presupuesto_gtq derivado de meta (miles×1000)="
                    f"{target.presupuesto_gtq} para modo2."
                )
            )

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
            f"Ingreso importado desde {path.name} ({method}). "
            f"ComisionesGTQ={ingreso_mensual_gtq}, "
            f"TipoCambioGTQxUSD={tipo_cambio}, "
            f"USD miles (tablero)={ingreso_usd_miles}, UNE={une.code}."
        )
        mmr.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Actualizado INGRESOS {une.code} {year}-{month:02d}: "
                f"real={mmr.measured_value} meta={mmr.target_value} "
                f"logrado={mmr.is_achieved} puntos={mmr.points_awarded} "
                f"({method})"
            )
        )
        self.stdout.write(self.style.SUCCESS("Import INGRESOS completado."))

        try:
            from pgc.admin_recalc import maybe_auto_recalc

            auto = maybe_auto_recalc(source="import_ingresos")
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

        try:
            from pgc.tv_charts_generate import schedule_tv_charts_refresh

            schedule_tv_charts_refresh(reason="import_ingresos")
        except Exception as exc:
            self.stdout.write(
                self.style.WARNING(f"Refresh charts TV no programado: {exc}")
            )
