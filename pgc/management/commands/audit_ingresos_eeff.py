"""Cuadra comisiones GTQ/miles USD en BD vs TSV de referencia (EEFF / Ingresos-Financieros)."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from core.models import MetricDefinition, UNE
from imports.ingresos_er_parse import load_comisiones_tsv
from pgc.income_conversion import get_fx_rate, gtq_comisiones_to_usd_miles
from pgc.models import MonthlyMetricResult, PGCPlan


class Command(BaseCommand):
    help = (
        "Compara INGRESOS en BD vs TSV Ingresos-Financieros-Comisiones (GTQ y miles USD)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            required=True,
            help="Ruta al TSV (ej. Ingresos-Financieros-Comisiones - 1.tsv).",
        )
        parser.add_argument("--year", type=int, default=2026)

    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.is_file():
            raise CommandError(f"No existe: {path}")
        ref = load_comisiones_tsv(path)
        if not ref:
            raise CommandError("TSV sin filas parseables.")

        plan = PGCPlan.objects.filter(is_active=True).order_by("-year").first()
        metric = MetricDefinition.objects.filter(code=MetricDefinition.CODE_INGRESOS).first()
        if not plan or not metric:
            raise CommandError("Falta plan PGC activo o métrica INGRESOS.")

        fail = 0
        ok = 0
        tol_gtq = Decimal("1")
        tol_miles = Decimal("0.05")

        for (une_code, year, month), ref_gtq in sorted(ref.items()):
            if year != options["year"]:
                continue
            fx = get_fx_rate(year, month)
            if not fx:
                self.stdout.write(self.style.WARNING(f"{year}-{month:02d} {une_code}: sin FX"))
                fail += 1
                continue
            expected_miles = gtq_comisiones_to_usd_miles(ref_gtq, fx)
            une = UNE.objects.filter(code=une_code).first()
            if not une:
                fail += 1
                continue
            row = MonthlyMetricResult.objects.filter(
                plan=plan, metric=metric, une=une, year=year, month=month
            ).first()
            if not row or row.measured_value is None:
                self.stdout.write(
                    self.style.ERROR(f"FAIL {year}-{month:02d} {une_code}: sin fila en BD")
                )
                fail += 1
                continue
            src = row.source_value or Decimal("0")
            miles = Decimal(str(row.measured_value))
            gtq_ok = abs(src - ref_gtq) <= tol_gtq
            miles_ok = abs(miles - expected_miles) <= tol_miles
            if gtq_ok and miles_ok:
                ok += 1
                continue
            fail += 1
            self.stdout.write(
                self.style.ERROR(
                    f"FAIL {year}-{month:02d} {une_code}: "
                    f"GTQ ref={ref_gtq} bd={src} | "
                    f"miles ref={expected_miles} bd={miles} fx={fx}"
                )
            )

        self.stdout.write(f"OK={ok} FAIL={fail} (referencia {path.name})")
        if fail:
            raise CommandError("Cuadre EEFF vs BD: hay diferencias.")
