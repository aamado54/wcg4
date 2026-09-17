# imports/management/commands/import_ingresos.py

import re
from decimal import Decimal
from pathlib import Path

import openpyxl
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import UNE, MetricDefinition
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

    def _to_decimal(self, raw_value, context: str) -> Decimal:
        if raw_value in (None, ""):
            return Decimal("0")

        text = str(raw_value).strip().replace(",", "")
        try:
            return Decimal(text)
        except Exception:
            raise CommandError(
                f"No se pudo convertir a decimal ({context}). Valor bruto={raw_value!r}"
            )

    def _saldo_fin_col(self, ws) -> int | None:
        for col_idx, cell in enumerate(ws[1], start=1):
            if cell.value is None:
                continue
            header = str(cell.value).strip().upper().replace(" ", "")
            if header in ("SALDOFIN", "SALDOFINAL"):
                return col_idx
        return None

    def _month_col(self, ws, month: int) -> int | None:
        month_names = {
            1: "ENERO",
            2: "FEBRERO",
            3: "MARZO",
            4: "ABRIL",
            5: "MAYO",
            6: "JUNIO",
            7: "JULIO",
            8: "AGOSTO",
            9: "SEPTIEMBRE",
            10: "OCTUBRE",
            11: "NOVIEMBRE",
            12: "DICIEMBRE",
        }
        month_name = month_names.get(month)
        if not month_name:
            return None
        for col_idx, cell in enumerate(ws[1], start=1):
            if cell.value is None:
                continue
            if str(cell.value).strip().upper() == month_name:
                return col_idx
        return None

    def _ytd_from_summary_rows(self, ws, prefix: str) -> Decimal | None:
        """Suma YTD de filas resumen NUMERO CUENTA == 4 u 8."""
        saldo_fin_col = self._saldo_fin_col(ws)
        if saldo_fin_col is None:
            return None

        for row in ws.iter_rows(min_row=2):
            for cell in row[:4]:
                if cell.value is None:
                    continue
                if str(cell.value).strip() == prefix:
                    saldo_value = row[saldo_fin_col - 1].value
                    return self._to_decimal(
                        saldo_value,
                        f"hoja Datos fila CUENTA={prefix} SALDOFIN",
                    )
        return None

    def _sum_detail_month_column(self, ws, month: int, prefix: str) -> Decimal | None:
        """Suma cuentas detalle (9 dígitos) en columna mensual ENERO..DICIEMBRE."""
        month_col = self._month_col(ws, month)
        if month_col is None:
            return None

        total = Decimal("0")
        found = False
        for row in ws.iter_rows(min_row=2):
            cuenta = row[1].value if len(row) > 1 else None
            if cuenta is None:
                continue
            cuenta_str = str(cuenta).strip()
            cuenta_digits = "".join(ch for ch in cuenta_str if ch.isdigit())
            if not (cuenta_digits.startswith(prefix) and len(cuenta_digits) == 9):
                continue
            tipo = row[3].value if len(row) > 3 else None
            if tipo != "D":
                continue
            month_value = row[month_col - 1].value
            if month_value in (None, ""):
                continue
            total += self._to_decimal(
                month_value,
                f"cuenta {cuenta_str} columna mes {month}",
            )
            found = True
        return total if found else None

    def _ytd_total(self, ws) -> Decimal:
        y4 = self._ytd_from_summary_rows(ws, "4")
        y8 = self._ytd_from_summary_rows(ws, "8")
        if y4 is not None or y8 is not None:
            return (y4 or Decimal("0")) + (y8 or Decimal("0"))

        # Sin filas resumen: sumar detalle en SALDO FINAL (poco común).
        saldo_fin_col = self._saldo_fin_col(ws)
        if saldo_fin_col is None:
            return Decimal("0")
        total = Decimal("0")
        for row in ws.iter_rows(min_row=2):
            cuenta = row[1].value if len(row) > 1 else None
            if cuenta is None:
                continue
            digits = "".join(ch for ch in str(cuenta).strip() if ch.isdigit())
            if len(digits) != 9:
                continue
            if not (digits.startswith("4") or digits.startswith("8")):
                continue
            if (row[3].value if len(row) > 3 else None) != "D":
                continue
            total += self._to_decimal(
                row[saldo_fin_col - 1].value,
                f"detalle {cuenta}",
            )
        return total

    def _infer_prev_path(self, path: Path, year: int, month: int) -> Path | None:
        if month <= 1:
            return None
        m = re.search(r"(\d{4})\.xlsx$", path.name, re.I)
        if not m:
            return None
        yymm = int(m.group(1))
        prev_yymm = yymm - 1
        if prev_yymm % 100 == 0:
            prev_yymm = (yymm // 100 - 1) * 100 + 12
        candidate = path.with_name(path.name.replace(f"{yymm:04d}", f"{prev_yymm:04d}"))
        return candidate if candidate.is_file() else None

    def _read_ingreso_from_excel(
        self,
        path: Path,
        month: int,
        *,
        prev_path: Path | None,
    ) -> tuple[Decimal, str]:
        """
        Lee ingreso mensual GTQ (cuentas 4+8).

        Prioridad:
        1) Columna mensual (ENERO..DICIEMBRE) en cuentas detalle.
        2) Delta YTD (SALDO FINAL mes actual − mes anterior).
        """
        try:
            wb = openpyxl.load_workbook(path, data_only=True)
        except Exception as e:
            raise CommandError(f"No se pudo abrir el archivo Excel: {e}")

        if "Datos" not in wb.sheetnames:
            raise CommandError(
                f"El archivo {path.name} no contiene hoja 'Datos'. "
                f"Hojas disponibles: {', '.join(wb.sheetnames)}"
            )

        ws = wb["Datos"]
        monthly_4 = self._sum_detail_month_column(ws, month, "4")
        monthly_8 = self._sum_detail_month_column(ws, month, "8")
        if monthly_4 is not None or monthly_8 is not None:
            total = (monthly_4 or Decimal("0")) + (monthly_8 or Decimal("0"))
            wb.close()
            return total, "columna_mensual"

        ytd_current = self._ytd_total(ws)
        wb.close()

        ytd_prev = Decimal("0")
        method = "ytd_sin_previo"
        if prev_path and prev_path.is_file():
            try:
                wb_prev = openpyxl.load_workbook(prev_path, data_only=True)
                if "Datos" in wb_prev.sheetnames:
                    ytd_prev = self._ytd_total(wb_prev["Datos"])
                    method = "ytd_delta"
                wb_prev.close()
            except Exception:
                method = "ytd_sin_previo"

        monthly = ytd_current - ytd_prev
        return monthly, method

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
            else self._infer_prev_path(path, year, month)
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

        une = self._infer_une_from_filename(path)
        if une.code == "INVESTMENT":
            raise CommandError(
                "Este comando no debe usarse para INVESTMENT; "
                "para esa UNE use el recálculo desde NewClientImportRow."
            )

        self.stdout.write(self.style.WARNING(f"Archivo detectado para UNE={une.code}"))

        ingreso_mensual_gtq, method = self._read_ingreso_from_excel(
            path, month, prev_path=prev_path
        )

        if une.code in ("FACTORING", "LEASING", "INSURANCE"):
            ingreso_ajustado_gtq = ingreso_mensual_gtq / Decimal("1000")
        else:
            ingreso_ajustado_gtq = ingreso_mensual_gtq

        tipo_cambio = self._get_exchange_rate(year, month)
        ingreso_usd_miles = ingreso_ajustado_gtq / tipo_cambio

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
        mmr.source_value = ingreso_mensual_gtq
        mmr.exchange_rate_used = tipo_cambio
        mmr.conversion_status = MonthlyMetricResult.CONVERSION_CONVERTED
        mmr.measured_value = ingreso_usd_miles
        apply_result_achievement(mmr, target)

        mmr.calculation_note = (
            f"Ingreso importado desde {path.name}, hoja Datos ({method}). "
            f"MensualGTQ(4+8)={ingreso_mensual_gtq}, "
            f"AjustadoGTQ={ingreso_ajustado_gtq}, "
            f"TipoCambioGTQxUSD={tipo_cambio}, "
            f"USD miles={ingreso_usd_miles}, UNE={une.code}."
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
