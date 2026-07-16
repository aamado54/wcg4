from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import MetricDefinition, UNE
from pgc.admin_manual import save_fx, save_results
from pgc.income_conversion import gtq_to_usd, recalc_stale_ingresos
from pgc.models import (
    MonthlyExchangeRate,
    MonthlyMetricResult,
    PGCPlan,
)


class IngresosConversionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            username="ingresos_test",
            email="t@example.com",
            password="pass",
        )
        self.year = 2026
        self.month = 5
        self.plan = PGCPlan.objects.create(year=self.year, name="Plan test")
        self.une = UNE.objects.create(
            code=UNE.CODE_FACTORING,
            name="Factoring",
            name_es="Factoraje",
            sort_order=1,
        )
        self.metric, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_INGRESOS,
            defaults={"name": "Ingresos", "is_scored": True},
        )
        for code, name in (
            (MetricDefinition.CODE_CLIENTES_NUEVOS, "Clientes"),
            (MetricDefinition.CODE_VENTA_CRUZADA, "Venta cruzada"),
            (MetricDefinition.CODE_RESPUESTA_REQS, "Reqs"),
        ):
            MetricDefinition.objects.get_or_create(
                code=code, defaults={"name": name, "is_scored": True}
            )

    def test_gtq_to_usd_math(self):
        usd = gtq_to_usd(Decimal("7850"), Decimal("7.85"))
        self.assertEqual(usd, Decimal("1000.000000"))

    def test_save_ingresos_requires_fx(self):
        with self.assertRaises(ValueError) as ctx:
            save_results(
                self.user,
                self.year,
                self.month,
                {
                    f"result_{self.une.id}_{self.metric.id}": "1000.5",
                },
                reason="prueba sin FX",
            )
        self.assertIn("Falta tipo de cambio", str(ctx.exception))
        self.assertFalse(
            MonthlyMetricResult.objects.filter(
                plan=self.plan, une=self.une, metric=self.metric
            ).exists()
        )

    def test_save_ingresos_converts_and_logs(self):
        MonthlyExchangeRate.objects.create(
            year=self.year, month=self.month, usd_to_gtq=Decimal("7.85000")
        )
        changes = save_results(
            self.user,
            self.year,
            self.month,
            {f"result_{self.une.id}_{self.metric.id}": "7850.12345678"},
            reason="captura GTQ",
        )
        self.assertEqual(changes, 1)
        row = MonthlyMetricResult.objects.get(
            plan=self.plan, une=self.une, metric=self.metric, year=self.year, month=self.month
        )
        self.assertEqual(row.source_currency, "GTQ")
        self.assertEqual(row.source_value, Decimal("7850.12345678"))
        self.assertEqual(row.exchange_rate_used, Decimal("7.85000"))
        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_CONVERTED)
        self.assertEqual(row.measured_value, gtq_to_usd(Decimal("7850.12345678"), Decimal("7.85")))

    def test_fx_change_marks_stale_and_recalc(self):
        MonthlyExchangeRate.objects.create(
            year=self.year, month=self.month, usd_to_gtq=Decimal("7.85")
        )
        save_results(
            self.user,
            self.year,
            self.month,
            {f"result_{self.une.id}_{self.metric.id}": "7850"},
            reason="inicial",
        )
        save_fx(
            self.user,
            self.year,
            self.month,
            {"fx_value": "8.00"},
            reason="ajuste TC",
        )
        row = MonthlyMetricResult.objects.get(
            plan=self.plan, une=self.une, metric=self.metric
        )
        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_STALE_FX)
        old_usd = row.measured_value

        result = recalc_stale_ingresos(
            year=self.year, month=self.month, user=self.user, reason="recalc test"
        )
        self.assertEqual(result["updated"], 1)
        row.refresh_from_db()
        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_CONVERTED)
        self.assertEqual(row.exchange_rate_used, Decimal("8.00"))
        self.assertEqual(row.measured_value, gtq_to_usd(Decimal("7850"), Decimal("8.00")))
        self.assertNotEqual(row.measured_value, old_usd)

    def test_save_ingresos_usd_native_without_fx(self):
        changes = save_results(
            self.user,
            self.year,
            self.month,
            {
                f"result_{self.une.id}_{self.metric.id}": "1500.5",
                f"ingresos_curr_{self.une.id}": "USD",
            },
            reason="captura USD",
        )
        self.assertEqual(changes, 1)
        row = MonthlyMetricResult.objects.get(
            plan=self.plan, une=self.une, metric=self.metric, year=self.year, month=self.month
        )
        self.assertEqual(row.source_currency, "USD")
        self.assertEqual(row.measured_value, Decimal("1500.5"))
        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_NATIVE_USD)
        self.assertIsNone(row.exchange_rate_used)

    def test_save_fx_range_months(self):
        changes = save_fx(
            self.user,
            self.year,
            6,
            {"fx_value_5": "7.80", "fx_value_6": "7.85"},
            reason="rango 05-06",
            month_from=5,
        )
        self.assertEqual(changes, 2)
        self.assertEqual(
            MonthlyExchangeRate.objects.get(year=self.year, month=5).usd_to_gtq,
            Decimal("7.80"),
        )
        self.assertEqual(
            MonthlyExchangeRate.objects.get(year=self.year, month=6).usd_to_gtq,
            Decimal("7.85"),
        )


class IngresosYearGridTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            username="year_grid_test",
            email="y@example.com",
            password="pass",
        )
        self.year = 2026
        self.plan = PGCPlan.objects.create(year=self.year, name="Plan year")
        self.unes = []
        for i, (code, name, name_es) in enumerate(
            (
                (UNE.CODE_FACTORING, "Factoring", "Factoraje"),
                (UNE.CODE_LEASING, "Leasing", "Leasing"),
                (UNE.CODE_INSURANCE, "Insurance", "Insurance"),
                (UNE.CODE_INVESTMENT, "Investment", "Inversiones"),
            )
        ):
            self.unes.append(
                UNE.objects.create(
                    code=code, name=name, name_es=name_es, sort_order=i + 1
                )
            )
        self.metric, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_INGRESOS,
            defaults={"name": "Ingresos", "is_scored": True},
        )

    def test_year_grid_gtq_uses_month_fx(self):
        from pgc.admin_ingresos_year import save_ingresos_year

        post = {
            "capture_currency": "GTQ",
            "fx_3": "7.85",
            f"ing_3_{self.unes[0].id}": "7850",
        }
        result = save_ingresos_year(self.user, self.year, post, reason="matriz Q")
        self.assertEqual(result["income_changes"], 1)
        self.assertEqual(result["fx_changes"], 1)
        row = MonthlyMetricResult.objects.get(
            plan=self.plan,
            une=self.unes[0],
            metric=self.metric,
            year=self.year,
            month=3,
        )
        self.assertEqual(row.source_currency, "GTQ")
        self.assertEqual(row.measured_value, gtq_to_usd(Decimal("7850"), Decimal("7.85")))

    def test_year_grid_requires_fx_for_gtq(self):
        from pgc.admin_ingresos_year import save_ingresos_year

        with self.assertRaises(ValueError) as ctx:
            save_ingresos_year(
                self.user,
                self.year,
                {
                    "capture_currency": "GTQ",
                    f"ing_4_{self.unes[1].id}": "1000",
                },
                reason="sin tc",
            )
        self.assertIn("Falta tipo de cambio", str(ctx.exception))

    def test_year_grid_usd_without_fx(self):
        from pgc.admin_ingresos_year import save_ingresos_year

        result = save_ingresos_year(
            self.user,
            self.year,
            {
                "capture_currency": "USD",
                f"ing_1_{self.unes[2].id}": "2500",
            },
            reason="matriz $",
        )
        self.assertEqual(result["income_changes"], 1)
        row = MonthlyMetricResult.objects.get(
            plan=self.plan,
            une=self.unes[2],
            metric=self.metric,
            year=self.year,
            month=1,
        )
        self.assertEqual(row.measured_value, Decimal("2500"))
        self.assertEqual(row.conversion_status, MonthlyMetricResult.CONVERSION_NATIVE_USD)


class SmartRecalcTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            username="smart_recalc",
            email="s@example.com",
            password="pass",
        )
        self.year = 2026
        self.month = 3
        self.plan = PGCPlan.objects.create(year=self.year, name="Plan smart")
        self.une = UNE.objects.create(
            code=UNE.CODE_FACTORING,
            name="Factoring",
            name_es="Factoraje",
            sort_order=1,
        )
        self.metric, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_INGRESOS,
            defaults={"name": "Ingresos", "is_scored": True},
        )
        for code, name in (
            (MetricDefinition.CODE_CLIENTES_NUEVOS, "Clientes"),
            (MetricDefinition.CODE_VENTA_CRUZADA, "VC"),
            (MetricDefinition.CODE_RESPUESTA_REQS, "Reqs"),
        ):
            MetricDefinition.objects.get_or_create(
                code=code, defaults={"name": name, "is_scored": True}
            )

    def test_stale_marks_period_pending(self):
        from pgc.admin_recalc import get_global_recalc_status, period_pending_reasons

        MonthlyExchangeRate.objects.create(
            year=self.year, month=self.month, usd_to_gtq=Decimal("7.85")
        )
        MonthlyMetricResult.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric,
            year=self.year,
            month=self.month,
            measured_value=Decimal("1000"),
            source_currency="GTQ",
            source_value=Decimal("7850"),
            exchange_rate_used=Decimal("7.85"),
            conversion_status=MonthlyMetricResult.CONVERSION_STALE_FX,
        )
        reasons = period_pending_reasons(self.year, self.month)
        self.assertTrue(any("STALE" in r for r in reasons))
        status = get_global_recalc_status()
        self.assertTrue(status["is_pending"])
        self.assertEqual(status["state"], "pending")

    def test_empty_known_periods_ready(self):
        from pgc.admin_recalc import get_global_recalc_status

        status = get_global_recalc_status()
        self.assertEqual(status["pending_count"], 0)
        self.assertTrue(status["is_ready"])
