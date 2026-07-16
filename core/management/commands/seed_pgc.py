from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import UNE, MetricDefinition
from pgc.models import PGCPlan, MonthlyTarget


class Command(BaseCommand):
    help = "Carga catálogo base y metas mensuales PGC 2026"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Iniciando seed PGC 2026..."))

        une_map = self._seed_unes()
        metric_map = self._seed_metrics()
        plan = self._seed_plan()
        self._seed_monthly_targets(plan, une_map, metric_map)

        self.stdout.write(self.style.SUCCESS("Seed PGC 2026 completado."))

    def _seed_unes(self):
        data = [
            {"code": "FACTORING", "name_es": "Factoraje", "sort_order": 1},
            {"code": "LEASING", "name_es": "Leasing", "sort_order": 2},
            {"code": "INSURANCE", "name_es": "Insurance", "sort_order": 3},
            {"code": "INVESTMENT", "name_es": "Inversiones", "sort_order": 4},
        ]

        result = {}
        for item in data:
            obj, _ = UNE.objects.update_or_create(
                code=item["code"],
                defaults={
                    "name_es": item["name_es"],
                    "sort_order": item["sort_order"],
                },
            )
            result[item["code"]] = obj
            self.stdout.write(f"UNE OK: {obj.code}")
        return result

    def _seed_metrics(self):
        data = [
            {
                "code": "INGRESOS",
                "name": "Ingresos",
                "description": "Meta mensual de ingresos por UNE",
            },
            {
                "code": "CLIENTES_NUEVOS",
                "name": "Clientes nuevos",
                "description": "Cantidad mensual de clientes nuevos por UNE",
            },
            {
                "code": "VENTA_CRUZADA",
                "name": "Venta cruzada",
                "description": "Cumple si la UNE refiere al menos un cliente a otra UNE en el mes",
            },
            {
                "code": "RESPUESTA_REQS",
                "name": "Respuesta a requerimientos",
                "description": "Cumplimiento manual mensual por UNE; en inversiones no aplica puntos",
            },
        ]

        result = {}
        for item in data:
            obj, _ = MetricDefinition.objects.update_or_create(
                code=item["code"],
                defaults={
                    "name": item["name"],
                    "description": item["description"],
                },
            )
            result[item["code"]] = obj
            self.stdout.write(f"Metric OK: {obj.code}")
        return result

    def _seed_plan(self):
        obj, _ = PGCPlan.objects.update_or_create(
            year=2026,
            defaults={
                "name": "PGC 2026",
                "is_active": True,
                "notes": "Plan anual PGC 2026 cargado desde especificación inicial",
            },
        )
        self.stdout.write(f"Plan OK: {obj}")
        return obj

    def _seed_monthly_targets(self, plan, une_map, metric_map):
        monthly_data = {
            "FACTORING": {
                "INGRESOS": {
                    "annual": Decimal("11000"),
                    "points": 70,
                    "months": [660, 1100, 770, 440, 770, 770, 1650, 770, 330, 440, 1650, 1650],
                },
                "CLIENTES_NUEVOS": {
                    "annual": Decimal("12"),
                    "points": 15,
                    "months": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                },
                "VENTA_CRUZADA": {
                    "annual": None,
                    "points": 10,
                    "months": [1] * 12,
                },
                "RESPUESTA_REQS": {
                    "annual": None,
                    "points": 5,
                    "months": [1] * 12,
                },
            },
            "LEASING": {
                "INGRESOS": {
                    "annual": Decimal("1200"),
                    "points": 70,
                    "months": [96, 84, 84, 84, 96, 84, 108, 108, 108, 120, 108, 120],
                },
                "CLIENTES_NUEVOS": {
                    "annual": Decimal("15"),
                    "points": 15,
                    "months": [0, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2],
                },
                "VENTA_CRUZADA": {
                    "annual": None,
                    "points": 10,
                    "months": [1] * 12,
                },
                "RESPUESTA_REQS": {
                    "annual": None,
                    "points": 5,
                    "months": [1] * 12,
                },
            },
            "INSURANCE": {
                "INGRESOS": {
                    "annual": Decimal("119.0"),
                    "points": 70,
                    "months": [
                        Decimal("6.746"),
                        Decimal("5.765"),
                        Decimal("5.898"),
                        Decimal("6.050"),
                        Decimal("7.620"),
                        Decimal("7.570"),
                        Decimal("9.760"),
                        Decimal("10.330"),
                        Decimal("11.850"),
                        Decimal("17.182"),
                        Decimal("16.372"),
                        Decimal("13.762"),
                    ],
                },
                "CLIENTES_NUEVOS": {
                    "annual": Decimal("44"),
                    "points": 15,
                    "months": [1, 2, 3, 5, 3, 4, 6, 3, 4, 6, 3, 4],
                },
                "VENTA_CRUZADA": {
                    "annual": None,
                    "points": 10,
                    "months": [1] * 12,
                },
                "RESPUESTA_REQS": {
                    "annual": None,
                    "points": 5,
                    "months": [1] * 12,
                },
            },
            "INVESTMENT": {
                "INGRESOS": {
                    "annual": Decimal("16.2"),
                    "points": 75,
                    "months": [
                        Decimal("0.200"),
                        Decimal("0.200"),
                        Decimal("0.300"),
                        Decimal("3.000"),
                        Decimal("0.600"),
                        Decimal("1.000"),
                        Decimal("1.000"),
                        Decimal("1.000"),
                        Decimal("1.000"),
                        Decimal("2.000"),
                        Decimal("2.900"),
                        Decimal("3.000"),
                    ],
                },
                "CLIENTES_NUEVOS": {
                    "annual": Decimal("20"),
                    "points": 15,
                    "months": [1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2],
                },
                "VENTA_CRUZADA": {
                    "annual": None,
                    "points": 10,
                    "months": [1] * 12,
                },
                "RESPUESTA_REQS": {
                    "annual": None,
                    "points": 0,
                    "months": [0] * 12,
                },
            },
        }

        total_rows = 0

        for une_code, metrics in monthly_data.items():
            une = une_map[une_code]

            for metric_code, payload in metrics.items():
                metric = metric_map[metric_code]
                annual_value = payload["annual"]
                points = payload["points"]

                for month_index, target in enumerate(payload["months"], start=1):
                    MonthlyTarget.objects.update_or_create(
                        plan=plan,
                        une=une,
                        metric=metric,
                        year=2026,
                        month=month_index,
                        defaults={
                            "target_value": Decimal(str(target)) if target is not None else None,
                            "points_if_achieved": points,
                            "reference_annual_value": annual_value,
                            "notes": self._build_note(metric_code, une_code),
                        },
                    )
                    total_rows += 1

        self.stdout.write(f"MonthlyTarget OK: {total_rows} registros")

    def _build_note(self, metric_code, une_code):
        if metric_code == "VENTA_CRUZADA":
            return "Cumple con al menos 1 referencia enviada a cualquier otra UNE en el mes."
        if metric_code == "RESPUESTA_REQS" and une_code == "INVERSIONES":
            return "No aplica puntos para Inversiones en el MVP."
        if metric_code == "RESPUESTA_REQS":
            return "Cumplimiento manual mensual; si incumple, registrar incidencia."
        if metric_code == "INGRESOS" and une_code == "INVERSIONES":
            return "Para Inversiones, el ingreso mensual se calcula sumando montos del archivo de clientes nuevos, sean nuevos o no."
        return ""