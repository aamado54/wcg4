"""Elimina VC y MRC heredados de imports Objetivos (política operativa 2026)."""

from __future__ import annotations

from decimal import Decimal

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import MetricDefinition, UNE
from pgc.income_conversion import apply_result_achievement
from pgc.models import ManualRequirementsCompliance, MonthlyMetricResult, MonthlyTarget, PGCPlan

MRC_DELETE_UNE_CODES = (
    UNE.CODE_FACTORING,
    UNE.CODE_LEASING,
    UNE.CODE_INVESTMENT,
)


class Command(BaseCommand):
    help = (
        "Pone VC en 0 por UNE y borra ManualRequirementsCompliance de Factoraje/Leasing/"
        "Inversiones para los meses indicados (conserva Insurance)."
    )

    def add_arguments(self, parser):
        parser.add_argument("--year", type=int, required=True)
        parser.add_argument(
            "--months",
            type=str,
            required=True,
            help="Meses separados por coma, p. ej. 8,9",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Solo muestra conteos sin escribir.",
        )
        parser.add_argument(
            "--no-recalc",
            action="store_true",
            help="No ejecutar recalc_pgc tras la limpieza.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        year = options["year"]
        months = self._parse_months(options["months"])
        dry_run = options["dry_run"]

        try:
            plan = PGCPlan.objects.get(year=year)
        except PGCPlan.DoesNotExist:
            raise CommandError(f"No existe PGCPlan para {year}")

        metric_vc = MetricDefinition.objects.get(code=MetricDefinition.CODE_VENTA_CRUZADA)

        for month in months:
            vc_qs = MonthlyMetricResult.objects.filter(
                plan=plan,
                metric=metric_vc,
                year=year,
                month=month,
            ).select_related("une")
            mrc_qs = ManualRequirementsCompliance.objects.filter(
                plan=plan,
                year=year,
                month=month,
                une__code__in=MRC_DELETE_UNE_CODES,
            )

            self.stdout.write(
                f"{year}-{month:02d}: VC filas={vc_qs.count()}, "
                f"MRC a borrar={mrc_qs.count()}"
            )

            if dry_run:
                continue

            for mmr in vc_qs:
                tgt = MonthlyTarget.objects.filter(
                    plan=plan,
                    une=mmr.une,
                    metric=metric_vc,
                    year=year,
                    month=month,
                ).first()
                mmr.measured_value = Decimal("0")
                mmr.calculation_note = (
                    "VC=0 (limpieza post-Objetivos; sin venta cruzada operativa)."
                )
                if tgt:
                    mmr.target_value = tgt.target_value
                    apply_result_achievement(mmr, tgt)
                else:
                    mmr.is_achieved = False
                    mmr.points_awarded = Decimal("0")
                mmr.save()

            deleted, _ = mrc_qs.delete()
            self.stdout.write(self.style.SUCCESS(f"  MRC eliminados: {deleted}"))

            if not options["no_recalc"]:
                for mode in ("modo1", "modo2"):
                    call_command("recalc_pgc", year=year, month=month, mode=mode)

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry-run: sin cambios."))
        else:
            self.stdout.write(self.style.SUCCESS("Limpieza completada."))

    def _parse_months(self, raw: str) -> list[int]:
        out: list[int] = []
        for part in raw.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                m = int(part)
            except ValueError as exc:
                raise CommandError(f"Mes inválido: {part!r}") from exc
            if m < 1 or m > 12:
                raise CommandError(f"Mes fuera de rango: {m}")
            out.append(m)
        if not out:
            raise CommandError("Indique al menos un mes en --months")
        return sorted(set(out))
