from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import UNE, MetricDefinition
from pgc.models import (
    PGCPlan,
    MonthlyTarget,
    MonthlyMetricResult,
    ManualRequirementsCompliance,
)


class Command(BaseCommand):
    help = "Carga valores medidos de ejemplo para probar el cálculo PGC"

    @transaction.atomic
    def handle(self, *args, **options):
        year = 2026
        month = 1

        plan = PGCPlan.objects.get(year=year)

        une_fact = UNE.objects.get(code__in=["FACTORING", "FACTORAJE"])
        une_leas = UNE.objects.get(code="LEASING")
        une_ins = UNE.objects.get(code="INSURANCE")
        une_inv = UNE.objects.get(code__in=["INVESTMENT", "INVERSIONES"])

        m_ing = MetricDefinition.objects.get(code=MetricDefinition.CODE_INGRESOS)
        m_cli = MetricDefinition.objects.get(code=MetricDefinition.CODE_CLIENTES_NUEVOS)
        m_ven = MetricDefinition.objects.get(code=MetricDefinition.CODE_VENTA_CRUZADA)
        m_req = MetricDefinition.objects.get(code=MetricDefinition.CODE_RESPUESTA_REQS)

        self.stdout.write("Cargando valores medidos de ejemplo para 2026-01...")

        # Helper
        def set_result(une, metric, measured_value):
            target = MonthlyTarget.objects.get(
                plan=plan,
                une=une,
                metric=metric,
                year=year,
                month=month,
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
            mmr.measured_value = measured_value
            mmr.save()
            self.stdout.write(
                f"  {une.code} {metric.code}: medido={measured_value} meta={target.target_value}"
            )

        # FACTORAJE enero 2026
        # Meta ingresos: 660 KUSD, real ~2,289 => cumple
        set_result(une_fact, m_ing, Decimal("2289"))
        # Meta clientes nuevos: 1, real 0 => no cumple
        set_result(une_fact, m_cli, Decimal("0"))
        # Venta cruzada: simulamos que sí hubo al menos 1 => 1
        set_result(une_fact, m_ven, Decimal("1"))
        # Respuesta reqs: cumplido (1); además sin incidencia manual
        set_result(une_fact, m_req, Decimal("1"))

        # LEASING enero 2026
        # Meta ingresos: 96 KUSD, real ~535 => cumple
        set_result(une_leas, m_ing, Decimal("535"))
        # Meta clientes nuevos: 0, real 0 => cumple trivial (>=)
        set_result(une_leas, m_cli, Decimal("0"))
        # Venta cruzada: simulamos 0 => falla
        set_result(une_leas, m_ven, Decimal("0"))
        # Respuesta reqs: cumplido
        set_result(une_leas, m_req, Decimal("1"))

        # INSURANCE enero 2026 (Personas+Empresas agregadas)
        # Meta ingresos: 6.746 (miles), real 12.435 => cumple
        set_result(une_ins, m_ing, Decimal("12.435"))
        # Meta clientes nuevos: 1+0=1, real 0 => no cumple
        set_result(une_ins, m_cli, Decimal("0"))
        # Venta cruzada: simulamos 1 => cumple
        set_result(une_ins, m_ven, Decimal("1"))
        # Respuesta reqs: cumplido
        set_result(une_ins, m_req, Decimal("1"))

        # INVERSIONES enero 2026
        # Meta ingresos: 0.200, real 1.265 (ejemplo) => cumple
        set_result(une_inv, m_ing, Decimal("1.265"))
        # Meta clientes nuevos: 1, real 3 => cumple
        set_result(une_inv, m_cli, Decimal("3"))
        # Venta cruzada: simulamos 0 => falla
        set_result(une_inv, m_ven, Decimal("0"))
        # Respuesta reqs: no otorga puntos para inversiones; medido 0
        set_result(une_inv, m_req, Decimal("0"))

        # Cumplimiento manual de requerimientos:
        #   - FACTORAJE: cumple
        #   - LEASING: incumple (para ver impacto)
        #   - INSURANCE: cumple
        #   - INVERSIONES: no aplica puntos, pero lo marcamos como cumple
        ManualRequirementsCompliance.objects.update_or_create(
            plan=plan,
            une=une_fact,
            year=year,
            month=month,
            defaults={"is_compliant": True, "incident_note": ""},
        )
        ManualRequirementsCompliance.objects.update_or_create(
            plan=plan,
            une=une_leas,
            year=year,
            month=month,
            defaults={
                "is_compliant": False,
                "incident_note": "Incumplimiento ilustrativo en enero para Leasing.",
            },
        )
        ManualRequirementsCompliance.objects.update_or_create(
            plan=plan,
            une=une_ins,
            year=year,
            month=month,
            defaults={"is_compliant": True, "incident_note": ""},
        )
        ManualRequirementsCompliance.objects.update_or_create(
            plan=plan,
            une=une_inv,
            year=year,
            month=month,
            defaults={"is_compliant": True, "incident_note": ""},
        )

        self.stdout.write(self.style.SUCCESS("Valores de ejemplo cargados."))