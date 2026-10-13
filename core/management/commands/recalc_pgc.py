from decimal import Decimal, ROUND_HALF_UP

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import MetricDefinition, UNE
from pgc.objetivos_scoring import (
    INSURANCE_REQS_GRACE_NOTE,
    ingresos_points_objetivos,
    insurance_reqs_uses_grace_points,
    proportional_points,
)
from pgc.models import (
    PGCPlan,
    MonthlyTarget,
    MonthlyMetricResult,
    MonthlyMetricScore,
    MonthlyModeScorecard,
    ManualRequirementsCompliance,
    MetricReserve,
)


class Command(BaseCommand):
    help = "Recalcula resultados y score PGC para un año y mes"

    SCORABLE_MODE2_CODES = (
        MetricDefinition.CODE_INGRESOS,
        MetricDefinition.CODE_CLIENTES_NUEVOS,
        MetricDefinition.CODE_VENTA_CRUZADA,
    )

    def add_arguments(self, parser):
        parser.add_argument("--year", type=int, required=True)
        parser.add_argument("--month", type=int, required=True)
        parser.add_argument(
            "--mode",
            type=str,
            default="modo1",
            choices=["modo1", "modo2"],
            help="Modalidad de cálculo de puntos: modo1 o modo2.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        year = options["year"]
        month = options["month"]
        mode = options["mode"]

        try:
            plan = PGCPlan.objects.get(year=year)
        except PGCPlan.DoesNotExist:
            raise CommandError(f"No existe PGCPlan para el año {year}")

        self.stdout.write(
            self.style.WARNING(
                f"Recalculando PGC {year}-{month:02d} en {mode}..."
            )
        )

        metrics = {
            m.code: m
            for m in MetricDefinition.objects.filter(
                code__in=[
                    MetricDefinition.CODE_INGRESOS,
                    MetricDefinition.CODE_CLIENTES_NUEVOS,
                    MetricDefinition.CODE_VENTA_CRUZADA,
                    MetricDefinition.CODE_RESPUESTA_REQS,
                ]
            )
        }

        if len(metrics) != 4:
            raise CommandError(
                "Faltan métricas base "
                "INGRESOS/CLIENTES_NUEVOS/VENTA_CRUZADA/RESPUESTA_REQS"
            )

        unes = UNE.objects.filter(is_active=True)

        metric_scores_created = 0
        metric_scores_updated = 0
        mode_scorecards_created = 0
        mode_scorecards_updated = 0

        for une in unes:
            total_points = Decimal("0")

            for metric in metrics.values():
                try:
                    target = MonthlyTarget.objects.get(
                        plan=plan,
                        une=une,
                        metric=metric,
                        year=year,
                        month=month,
                    )
                except MonthlyTarget.DoesNotExist:
                    continue

                source_result, _ = MonthlyMetricResult.objects.get_or_create(
                    plan=plan,
                    une=une,
                    metric=metric,
                    year=year,
                    month=month,
                    defaults={
                        "measured_value": None,
                        "target_value": target.target_value,
                        "is_achieved": False,
                        "points_awarded": 0,
                        "calculation_note": "",
                    },
                )

                score, created = MonthlyMetricScore.objects.get_or_create(
                    plan=plan,
                    une=une,
                    metric=metric,
                    year=year,
                    month=month,
                    mode=mode,
                    defaults={
                        "measured_value": source_result.measured_value,
                        "target_value": target.target_value,
                        "is_achieved": False,
                        "points_awarded": 0,
                        "calculation_note": "",
                    },
                )

                if created:
                    metric_scores_created += 1
                else:
                    metric_scores_updated += 1

                score.measured_value = source_result.measured_value
                score.target_value = target.target_value

                if mode == "modo1":
                    self.apply_modo1(score, metric, target)
                else:
                    self.apply_modo2(
                        plan,
                        year,
                        month,
                        une,
                        score,
                        metric,
                        target,
                        source_result=source_result,
                    )

                if metric.code == MetricDefinition.CODE_RESPUESTA_REQS:
                    self.apply_manual_requirements_override(
                        plan=plan,
                        une=une,
                        year=year,
                        month=month,
                        metric_score=score,
                        source_result=source_result,
                        target=target,
                    )

                score.save()
                total_points += Decimal(str(score.points_awarded or 0))

            mode_scorecard, created = MonthlyModeScorecard.objects.get_or_create(
                plan=plan,
                une=une,
                year=year,
                month=month,
                mode=mode,
                defaults={
                    "total_points": total_points,
                    "qualified_threshold": 80,
                    "is_month_qualified": total_points >= Decimal("80"),
                    "summary_note": f"Score recalculado en {mode}",
                },
            )

            if created:
                mode_scorecards_created += 1
            else:
                mode_scorecards_updated += 1

            if mode_scorecard.qualified_threshold is None:
                mode_scorecard.qualified_threshold = 80

            mode_scorecard.total_points = total_points
            mode_scorecard.is_month_qualified = total_points >= Decimal(
                str(mode_scorecard.qualified_threshold)
            )
            mode_scorecard.summary_note = f"Score recalculado en {mode}"
            mode_scorecard.save()

        self.stdout.write(
            f"MonthlyMetricScore: {metric_scores_created} creados, "
            f"{metric_scores_updated} actualizados"
        )
        self.stdout.write(
            f"MonthlyModeScorecard: {mode_scorecards_created} creados, "
            f"{mode_scorecards_updated} actualizados"
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Recalc PGC {year}-{month:02d} completado en {mode}."
            )
        )

    def apply_modo1(self, metric_score, metric, target):
        measured = metric_score.measured_value
        target_value = metric_score.target_value

        if measured is not None and target_value is not None:
            if measured >= target_value:
                metric_score.is_achieved = True
                metric_score.points_awarded = target.points_if_achieved
                metric_score.calculation_note = "Modo1 cumple meta objetivo."
            else:
                metric_score.is_achieved = False
                metric_score.points_awarded = 0
                metric_score.calculation_note = "Modo1 no cumple meta objetivo."
            return

        if metric.code in (
            MetricDefinition.CODE_VENTA_CRUZADA,
            MetricDefinition.CODE_RESPUESTA_REQS,
        ):
            if measured and measured >= Decimal("1"):
                metric_score.is_achieved = True
                metric_score.points_awarded = target.points_if_achieved
                metric_score.calculation_note = "Modo1 cumple condición binaria."
            else:
                metric_score.is_achieved = False
                metric_score.points_awarded = 0
                metric_score.calculation_note = "Modo1 sin datos suficientes o no cumplida."
        else:
            metric_score.is_achieved = False
            metric_score.points_awarded = 0
            metric_score.calculation_note = "Modo1 sin valor medido para este mes."

    def apply_modo2(
        self,
        plan,
        year,
        month,
        une,
        metric_score,
        metric,
        target,
        source_result=None,
    ):
        """
        2.Proporción alineado a hoja Objetivos (sin reservas de puntos).
        """
        if metric.code == MetricDefinition.CODE_RESPUESTA_REQS:
            self.apply_modo1(metric_score, metric, target)
            metric_score.calculation_note = (
                f"Modo2 requerimientos (binario). {metric_score.calculation_note}"
            )
            return

        if metric.code == MetricDefinition.CODE_INGRESOS:
            pts, achieved, note = ingresos_points_objetivos(
                target,
                source_result,
                une_code=une.code,
            )
            metric_score.points_awarded = pts
            metric_score.is_achieved = achieved
            metric_score.calculation_note = note
            return

        if metric.code not in self.SCORABLE_MODE2_CODES:
            self.apply_modo1(metric_score, metric, target)
            metric_score.calculation_note = (
                f"Modo2 sin regla Objetivos; modo1. {metric_score.calculation_note}"
            )
            return

        measured = metric_score.measured_value
        target_value = metric_score.target_value
        pts, achieved, note = proportional_points(
            target.points_if_achieved,
            measured,
            target_value,
        )
        metric_score.points_awarded = pts
        metric_score.is_achieved = achieved
        metric_score.calculation_note = note

    def apply_manual_requirements_override(
        self, plan, une, year, month, metric_score, source_result=None, target=None
    ):
        """
        El cumplimiento manual es la fuente de verdad para RESPUESTA_REQS.
        - Cumple: measured=1, puntos de la meta, is_achieved=True
        - No cumple: measured=0, 0 puntos, is_achieved=False
        Sin registro manual: no altera el cálculo previo.
        """
        try:
            mrc = ManualRequirementsCompliance.objects.get(
                plan=plan,
                une=une,
                year=year,
                month=month,
            )
        except ManualRequirementsCompliance.DoesNotExist:
            return

        points_if = Decimal("0")
        target_value = metric_score.target_value
        if target is not None:
            points_if = Decimal(str(target.points_if_achieved or 0))
            if target_value is None:
                target_value = target.target_value

        if mrc.is_compliant:
            metric_score.measured_value = Decimal("1")
            metric_score.target_value = target_value if target_value is not None else Decimal("1")
            metric_score.is_achieved = True
            metric_score.points_awarded = points_if
            note = "Cumplimiento manual: Cumple. Puntos otorgados según meta."
            if insurance_reqs_uses_grace_points(une.code, points_if):
                note += f" {INSURANCE_REQS_GRACE_NOTE}"
            metric_score.calculation_note = note
        else:
            metric_score.measured_value = Decimal("0")
            metric_score.target_value = target_value if target_value is not None else Decimal("1")
            metric_score.is_achieved = False
            metric_score.points_awarded = Decimal("0")
            note = (mrc.incident_note or "").strip()
            metric_score.calculation_note = (
                "Cumplimiento manual: No cumple; puntos en 0."
                + (f" Incidencia: {note}" if note else "")
            )

        if source_result is not None:
            source_result.measured_value = metric_score.measured_value
            source_result.target_value = metric_score.target_value
            source_result.is_achieved = metric_score.is_achieved
            source_result.points_awarded = metric_score.points_awarded
            source_result.calculation_note = metric_score.calculation_note
            source_result.save(
                update_fields=[
                    "measured_value",
                    "target_value",
                    "is_achieved",
                    "points_awarded",
                    "calculation_note",
                    "updated_at",
                ]
            )

    def get_available_reserve(self, plan, une, metric, year, month):
        reserves = MetricReserve.objects.filter(
            plan=plan,
            une=une,
            metric=metric,
            remaining__gt=0,
        ).exclude(
            source_year=year,
            source_month=month,
        )

        total = Decimal("0")
        for reserve in reserves:
            total += reserve.remaining or Decimal("0")
        return total

    def consume_reserve(self, plan, une, metric, year, month, amount_to_consume):
        pending = Decimal(str(amount_to_consume))

        reserves = (
            MetricReserve.objects.filter(
                plan=plan,
                une=une,
                metric=metric,
                remaining__gt=0,
            )
            .exclude(
                source_year=year,
                source_month=month,
            )
            .order_by("source_year", "source_month", "id")
        )

        for reserve in reserves:
            if pending <= Decimal("0"):
                break

            available = reserve.remaining or Decimal("0")
            used = min(available, pending)
            reserve.remaining = available - used
            reserve.save(update_fields=["remaining"])
            pending -= used