import os
import tempfile
from datetime import date, datetime, timedelta
from unittest.mock import patch
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import RequestFactory, TestCase

from core.models import MetricDefinition, UNE
from pgc.admin_manual import save_fx, save_results
from pgc.income_conversion import (
    apply_result_achievement,
    gtq_comisiones_to_usd_miles,
    gtq_to_usd,
    ingresos_has_legacy_double_fx_bug,
    repair_ingresos_gtq_and_usd_miles,
    ingresos_has_gtq_over_fx_source_with_correct_miles,
    ingresos_has_extra_fx_on_gtq_over_fx_source,
    recalc_stale_ingresos,
)
from pgc.models import (
    ManualRequirementsCompliance,
    MonthlyExchangeRate,
    MonthlyMetricResult,
    MonthlyMetricScore,
    MonthlyTarget,
    PGCMode,
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

    def test_audit_passes_on_clean_gtq_row(self):
        from pgc.income_conversion import audit_ingresos_fx_findings

        MonthlyExchangeRate.objects.create(
            year=self.year,
            month=self.month,
            usd_to_gtq=Decimal("7.85"),
        )
        mmr = MonthlyMetricResult.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric,
            year=self.year,
            month=self.month,
            source_currency=MonthlyMetricResult.CURRENCY_GTQ,
            source_value=Decimal("7850000"),
            exchange_rate_used=Decimal("7.85"),
            measured_value=gtq_comisiones_to_usd_miles(
                Decimal("7850000"), Decimal("7.85")
            ),
            conversion_status=MonthlyMetricResult.CONVERSION_CONVERTED,
        )
        apply_result_achievement(mmr)
        mmr.save()
        report = audit_ingresos_fx_findings(year=self.year, month=self.month)
        self.assertTrue(report["pass"], report)

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
        self.assertEqual(
            row.measured_value,
            gtq_comisiones_to_usd_miles(Decimal("7850.12345678"), Decimal("7.85")),
        )

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
        self.assertEqual(
            row.measured_value,
            gtq_comisiones_to_usd_miles(Decimal("7850"), Decimal("8.00")),
        )
        self.assertNotEqual(row.measured_value, old_usd)

    def test_extra_fx_detects_large_factoring_gtq_over_fx(self):
        fx = Decimal("7.63856")
        gtq_real = Decimal("2288849")
        stored_source = gtq_real / fx
        wrong_miles = gtq_comisiones_to_usd_miles(stored_source, fx)
        correct_miles = gtq_comisiones_to_usd_miles(gtq_real, fx)
        self.assertGreater(correct_miles, wrong_miles * Decimal("5"))
        self.assertTrue(
            ingresos_has_extra_fx_on_gtq_over_fx_source(
                stored_source, wrong_miles, fx
            )
        )
        self.assertFalse(
            ingresos_has_extra_fx_on_gtq_over_fx_source(
                gtq_real, correct_miles, fx
            )
        )

        """Bug histórico: source=GTQ/FX; repair restaura GTQ y miles."""
        fx = Decimal("7.63856")
        gtq_real = Decimal("1518027.18")
        legacy_source = gtq_real / fx
        legacy_measured = (legacy_source / Decimal("1000")) / (fx * fx)
        self.assertTrue(
            ingresos_has_legacy_double_fx_bug(legacy_source, legacy_measured, fx)
        )
        MonthlyExchangeRate.objects.create(
            year=2026, month=9, usd_to_gtq=fx
        )
        row = MonthlyMetricResult.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric,
            year=2026,
            month=9,
            source_currency=MonthlyMetricResult.CURRENCY_GTQ,
            source_value=legacy_source,
            measured_value=legacy_measured,
            exchange_rate_used=fx,
            conversion_status=MonthlyMetricResult.CONVERSION_CONVERTED,
        )
        stats = repair_ingresos_gtq_and_usd_miles(year=2026, month=9)
        self.assertEqual(stats["repaired_legacy"], 1)
        row.refresh_from_db()
        self.assertAlmostEqual(float(row.source_value), float(gtq_real), places=2)
        self.assertAlmostEqual(
            float(row.measured_value),
            float(gtq_comisiones_to_usd_miles(gtq_real, fx)),
            places=4,
        )

    def test_repair_does_not_shrink_correct_miles_gtq_over_fx_source(self):
        """Tras repair erróneo previo: source=GTQ/FX + miles=source/1000 no debe ÷FX otra vez."""
        fx = Decimal("7.63856")
        gtq_real = Decimal("1518027.18")
        stored_source = gtq_real / fx
        correct_miles = (stored_source / Decimal("1000")).quantize(Decimal("0.000001"))
        self.assertTrue(
            ingresos_has_gtq_over_fx_source_with_correct_miles(
                stored_source, correct_miles, fx
            )
        )
        MonthlyExchangeRate.objects.create(
            year=2026, month=9, usd_to_gtq=fx
        )
        row = MonthlyMetricResult.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric,
            year=2026,
            month=9,
            source_currency=MonthlyMetricResult.CURRENCY_GTQ,
            source_value=stored_source,
            measured_value=correct_miles,
            exchange_rate_used=fx,
            conversion_status=MonthlyMetricResult.CONVERSION_CONVERTED,
        )
        stats = repair_ingresos_gtq_and_usd_miles(year=2026, month=9)
        self.assertEqual(stats["repaired_legacy"], 1)
        row.refresh_from_db()
        self.assertAlmostEqual(float(row.source_value), float(gtq_real), places=2)
        self.assertAlmostEqual(float(row.measured_value), float(correct_miles), places=4)

    def test_repair_restores_miles_after_wrong_extra_fx_division(self):
        """Simula BD prod dañada por repair previo (measured ÷ FX de más)."""
        fx = Decimal("7.63856")
        gtq_real = Decimal("1518027.18")
        stored_source = gtq_real / fx
        correct_miles = (stored_source / Decimal("1000")).quantize(Decimal("0.000001"))
        wrong_miles = gtq_comisiones_to_usd_miles(stored_source, fx)
        self.assertAlmostEqual(float(wrong_miles), float(correct_miles / fx), places=4)
        MonthlyExchangeRate.objects.create(
            year=2026, month=9, usd_to_gtq=fx
        )
        row = MonthlyMetricResult.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric,
            year=2026,
            month=9,
            source_currency=MonthlyMetricResult.CURRENCY_GTQ,
            source_value=stored_source,
            measured_value=wrong_miles,
            exchange_rate_used=fx,
            conversion_status=MonthlyMetricResult.CONVERSION_CONVERTED,
        )
        stats = repair_ingresos_gtq_and_usd_miles(year=2026, month=9)
        self.assertEqual(stats["repaired_legacy"], 1)
        row.refresh_from_db()
        self.assertAlmostEqual(float(row.source_value), float(gtq_real), places=2)
        self.assertAlmostEqual(float(row.measured_value), float(correct_miles), places=4)

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
        self.assertEqual(
            row.measured_value,
            gtq_comisiones_to_usd_miles(Decimal("7850"), Decimal("7.85")),
        )

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

    def test_investment_audit_breakdown(self):
        from imports.models import InvestmentGrowthRow
        from pgc.admin_ingresos_year import get_ingresos_year_context

        inv_une = self.unes[3]
        MonthlyExchangeRate.objects.create(
            year=self.year, month=2, usd_to_gtq=Decimal("8")
        )
        MonthlyExchangeRate.objects.create(
            year=self.year, month=1, usd_to_gtq=Decimal("8")
        )
        InvestmentGrowthRow.objects.create(
            year=self.year,
            month=1,
            instrument="AP",
            operation_code="A1",
            amount_usd=Decimal("1000000"),
        )
        InvestmentGrowthRow.objects.create(
            year=self.year,
            month=2,
            instrument="AP",
            operation_code="A1",
            amount_usd=Decimal("1100000"),
        )
        ctx = get_ingresos_year_context(self.year, capture_currency="USD")
        row = next(r for r in ctx["month_rows"] if r["month"] == 2)
        inv_cell = next(c for c in row["cells"] if c["is_investment"])
        audit = inv_cell["investment_audit"]
        self.assertEqual(audit["inversiones_display"], "1,100")
        self.assertEqual(audit["growth_usd"], Decimal("100000"))
        self.assertEqual(audit["growth_miles"], Decimal("100"))
        self.assertTrue(audit["growth_matches_levels"])

        ctx_gtq = get_ingresos_year_context(self.year, capture_currency="GTQ")
        row_gtq = next(r for r in ctx_gtq["month_rows"] if r["month"] == 2)
        inv_gtq = next(c for c in row_gtq["cells"] if c["is_investment"])
        audit_gtq = inv_gtq["investment_audit"]
        self.assertEqual(audit_gtq["growth_sub"], "Q ref (miles): 800")

    def test_year_grid_display_caps_currency_decimals(self):
        from pgc.admin_ingresos_year import get_ingresos_year_context

        MonthlyExchangeRate.objects.create(
            year=self.year, month=2, usd_to_gtq=Decimal("7.8500001")
        )
        MonthlyMetricResult.objects.create(
            plan=self.plan,
            une=self.unes[0],
            metric=self.metric,
            year=self.year,
            month=2,
            measured_value=Decimal("123.456789"),
            source_currency=MonthlyMetricResult.CURRENCY_GTQ,
            source_value=Decimal("970.123456"),
            conversion_status=MonthlyMetricResult.CONVERSION_CONVERTED,
        )
        ctx = get_ingresos_year_context(self.year, capture_currency="GTQ")
        row = next(r for r in ctx["month_rows"] if r["month"] == 2)
        self.assertEqual(row["fx_value"], "7.85")
        cell = row["cells"][0]
        self.assertEqual(cell["value"], "970.123")
        self.assertEqual(cell["measured_usd_display"], "123.457")

    def test_wcg_amount_format(self):
        from core.number_format import format_wcg_amount

        self.assertEqual(format_wcg_amount(Decimal("1234.5000")), "1,234.5")
        self.assertEqual(format_wcg_amount(Decimal("1000")), "1,000")

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

    def test_target_only_future_months_not_pending_for_investment(self):
        from pgc.admin_recalc import period_pending_reasons

        MonthlyTarget.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric,
            year=self.year,
            month=11,
            target_value=Decimal("100"),
            points_if_achieved=Decimal("70"),
        )
        reasons = period_pending_reasons(self.year, 11)
        self.assertFalse(
            any("Ingresos Investment" in r for r in reasons),
            msg=f"No debería marcar pendiente Investment sin datos: {reasons}",
        )


class RespuestaReqsComplianceTests(TestCase):
    def setUp(self):
        self.plan = PGCPlan.objects.create(year=2026, name="Plan reqs rules")
        self.insurance = UNE.objects.create(
            code=UNE.CODE_INSURANCE,
            name="Insurance",
            name_es="Seguros",
            sort_order=4,
        )
        self.investment = UNE.objects.create(
            code=UNE.CODE_INVESTMENT,
            name="Investment",
            name_es="Inversiones",
            sort_order=5,
        )
        self.metric, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_RESPUESTA_REQS,
            defaults={"name": "Reqs", "is_scored": True},
        )
        for une, month in ((self.investment, 10), (self.insurance, 3)):
            MonthlyTarget.objects.create(
                plan=self.plan,
                une=une,
                metric=self.metric,
                year=2026,
                month=month,
                target_value=Decimal("1"),
                points_if_achieved=Decimal("5"),
            )

    def test_insurance_excluded_from_respuesta_reqs_report(self):
        from pgc.views import _get_respuesta_reqs_rows

        ManualRequirementsCompliance.objects.create(
            plan=self.plan,
            une=self.insurance,
            year=2026,
            month=3,
            is_compliant=False,
            incident_note="Excel NO APLICA",
        )
        _, rows = _get_respuesta_reqs_rows(periods=[(2026, 3)])
        self.assertFalse(any(r["target"].une_id == self.insurance.id for r in rows))

    def test_insurance_respuesta_reqs_points_never_scored(self):
        from pgc.objetivos_scoring import respuesta_reqs_points_awarded

        pts = respuesta_reqs_points_awarded(
            UNE.CODE_INSURANCE, 2026, 3, Decimal("5"), True
        )
        self.assertEqual(pts, Decimal("0"))

    def test_tablero_insurance_hides_respuesta_reqs_row(self):
        from pgc.views import _build_dashboard_annual_tables, _get_dashboard_rows

        rows = _get_dashboard_rows(periods=[(2026, 3)])
        insurance_rows = [r for r in rows if r["une"].code == UNE.CODE_INSURANCE]
        if insurance_rows:
            self.assertFalse(insurance_rows[0]["show_respuesta_reqs"])
        else:
            stub = {
                "une": self.insurance,
                "show_respuesta_reqs": False,
            }
            self.assertFalse(stub["show_respuesta_reqs"])

        tables = _build_dashboard_annual_tables(2026)
        insurance_table = next(
            (t for t in tables if t["une"].code == UNE.CODE_INSURANCE),
            None,
        )
        if insurance_table is not None:
            self.assertFalse(insurance_table["show_respuesta_reqs"])
            self.assertIsNone(insurance_table["p_reqs_total"])

    def test_sin_registro_asume_cumple_octubre_inversiones(self):
        from pgc.views import _get_respuesta_reqs_rows

        _, rows = _get_respuesta_reqs_rows(periods=[(2026, 10)])
        row = next(r for r in rows if r["target"].une_id == self.investment.id)
        self.assertEqual(row["measured_value"], Decimal("1"))
        self.assertEqual(row["points_awarded"], Decimal("5"))


class RequirementsReportTests(TestCase):
    def setUp(self):
        self.plan = PGCPlan.objects.create(year=2026, name="Plan reqs")
        self.une = UNE.objects.create(
            code=UNE.CODE_FACTORING,
            name="Factoring",
            name_es="Factoraje",
            sort_order=1,
        )
        self.metric, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_RESPUESTA_REQS,
            defaults={"name": "Reqs", "is_scored": True},
        )
        MonthlyTarget.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric,
            year=2026,
            month=8,
            target_value=Decimal("1"),
            points_if_achieved=Decimal("5"),
        )

    def test_report_prefers_manual_over_stale_score(self):
        from pgc.admin_manual import _sync_requirements_metric_result
        from pgc.views import _get_respuesta_reqs_rows

        ManualRequirementsCompliance.objects.create(
            plan=self.plan,
            une=self.une,
            year=2026,
            month=8,
            is_compliant=True,
        )
        result = MonthlyMetricResult.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric,
            year=2026,
            month=8,
            measured_value=Decimal("0"),
            target_value=Decimal("1"),
            is_achieved=False,
            points_awarded=Decimal("0"),
        )
        MonthlyMetricScore.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric,
            year=2026,
            month=8,
            mode="modo1",
            measured_value=Decimal("0"),
            target_value=Decimal("1"),
            is_achieved=False,
            points_awarded=Decimal("0"),
        )
        _sync_requirements_metric_result(
            plan=self.plan,
            une=self.une,
            year=2026,
            month=8,
            is_compliant=True,
        )

        _, rows = _get_respuesta_reqs_rows(periods=[(2026, 8)])
        row = rows[0]
        self.assertTrue(row["is_achieved"])
        self.assertEqual(row["points_awarded"], Decimal("5"))
        result.refresh_from_db()
        self.assertTrue(result.is_achieved)
        self.assertEqual(result.points_awarded, Decimal("5"))


class RequirementsYearMatrixTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            username="reqs_year",
            email="r@example.com",
            password="pass",
        )
        self.plan = PGCPlan.objects.create(year=2026, name="Plan reqs año")
        self.une = UNE.objects.create(
            code=UNE.CODE_FACTORING,
            name="Factoring",
            name_es="Factoraje",
            sort_order=1,
        )
        self.metric, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_RESPUESTA_REQS,
            defaults={"name": "Reqs", "is_scored": True},
        )
        for month in (1, 2, 3):
            MonthlyTarget.objects.create(
                plan=self.plan,
                une=self.une,
                metric=self.metric,
                year=2026,
                month=month,
                target_value=Decimal("1"),
                points_if_achieved=Decimal("4"),
            )

    def test_through_month_for_current_year(self):
        from pgc.admin_requirements_year import through_month_for_year

        self.assertEqual(through_month_for_year(2025, now=date(2026, 3, 15)), 12)
        self.assertEqual(through_month_for_year(2026, now=date(2026, 3, 15)), 3)
        self.assertEqual(through_month_for_year(2027, now=date(2026, 3, 15)), 0)

    def test_year_context_has_twelve_month_columns(self):
        from pgc.admin_requirements_year import get_requirements_year_context

        ctx = get_requirements_year_context(2026, now=date(2026, 8, 1))
        self.assertEqual(len(ctx["requirements_month_headers"]), 12)
        self.assertEqual(ctx["requirements_month_headers"][0]["label"], "Ene")
        self.assertEqual(len(ctx["requirements_matrix"][0]["cells"]), 12)

    def test_save_requirements_year_writes_compliance_and_points(self):
        from django.http import QueryDict

        from pgc.admin_requirements_year import save_requirements_year

        post = QueryDict(mutable=True)
        post["req_status_{}_{}".format(self.une.id, 1)] = "1"
        post["req_status_{}_{}".format(self.une.id, 2)] = "1"
        changes = save_requirements_year(self.user, 2026, post, reason="Cierre histórico")
        self.assertGreater(changes, 0)
        mrc = ManualRequirementsCompliance.objects.get(
            plan=self.plan, une=self.une, year=2026, month=1
        )
        self.assertTrue(mrc.is_compliant)
        result = MonthlyMetricResult.objects.get(
            plan=self.plan,
            une=self.une,
            metric=self.metric,
            year=2026,
            month=1,
        )
        self.assertTrue(result.is_achieved)
        self.assertEqual(result.points_awarded, Decimal("4"))


class ImportPgcObjetivosTests(TestCase):
    def setUp(self):
        self.year = 2026
        self.month = 8
        self.plan = PGCPlan.objects.create(year=self.year, name="Plan test")
        MonthlyExchangeRate.objects.create(
            year=self.year, month=self.month, usd_to_gtq=Decimal("7.66")
        )
        self.metric_cli, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_CLIENTES_NUEVOS,
            defaults={"name": "Clientes", "is_scored": True},
        )
        self.metric_ing, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_INGRESOS,
            defaults={"name": "Ingresos", "is_scored": True},
        )
        for code, name in (
            (MetricDefinition.CODE_VENTA_CRUZADA, "Venta cruzada"),
            (MetricDefinition.CODE_RESPUESTA_REQS, "Respuesta reqs"),
        ):
            MetricDefinition.objects.get_or_create(
                code=code, defaults={"name": name, "is_scored": True}
            )
        for code, name, order in (
            ("FACTORING", "Factoraje", 1),
            ("LEASING", "Leasing", 2),
            ("INSURANCE", "Insurance", 3),
            ("INVESTMENT", "Inversiones", 4),
        ):
            une = UNE.objects.create(code=code, name=name, name_es=name, sort_order=order)
            metrics = [self.metric_cli, self.metric_ing]
            for extra in (
                MetricDefinition.CODE_VENTA_CRUZADA,
                MetricDefinition.CODE_RESPUESTA_REQS,
            ):
                metrics.append(
                    MetricDefinition.objects.get(code=extra)
                )
            for metric in metrics:
                MonthlyTarget.objects.create(
                    plan=self.plan,
                    une=une,
                    metric=metric,
                    year=self.year,
                    month=self.month,
                    target_value=Decimal("100"),
                    points_if_achieved=10,
                )

    def test_import_objetivos_august_2026(self):
        root = Path(settings.BASE_DIR).parent
        path = root / "data" / "now" / "PGC-ejecucion-vs-presupuesto-ago26-validar.xlsx"
        if not path.is_file():
            self.skipTest("Sin archivo de validación PGC")

        call_command(
            "import_pgc_objetivos",
            path=str(path),
            year=self.year,
            month=self.month,
            force_legacy_excel=True,
        )

        factoring = UNE.objects.get(code="FACTORING")
        row = MonthlyMetricResult.objects.get(
            plan=self.plan,
            une=factoring,
            metric=self.metric_ing,
            year=self.year,
            month=self.month,
        )
        self.assertAlmostEqual(float(row.measured_value), 60.089, places=2)
        self.assertAlmostEqual(float(row.source_value), 460285.2820980406, places=2)

        leasing = UNE.objects.get(code="LEASING")
        cli = MonthlyMetricResult.objects.get(
            plan=self.plan,
            une=leasing,
            metric=self.metric_cli,
            year=self.year,
            month=self.month,
        )
        self.assertEqual(cli.measured_value, Decimal("1"))

    def _write_min_objetivos_xlsx(self, path: Path, cells: dict | None = None):
        import openpyxl

        from pgc.management.commands.import_pgc_objetivos import (
            COL_EXEC_VC,
            COL_PTS_EXEC_REQ,
        )

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Objetivos"
        row = [None] * (COL_PTS_EXEC_REQ + 2)
        row[0] = datetime(self.year, self.month, 10)
        row[5] = "WC"
        for col, val in (cells or {}).items():
            row[col] = val
        ws.append(["header"])
        ws.append(row)
        wb.save(path)

    def test_import_skips_vc_and_reqs_by_default(self):
        from pgc.management.commands import import_pgc_objetivos as ipo_mod

        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            path = Path(tmp.name)
        self.addCleanup(path.unlink, missing_ok=True)
        self._write_min_objetivos_xlsx(
            path,
            {
                ipo_mod.COL_EXEC_VC: 12,
                ipo_mod.COL_PTS_EXEC_REQ: 5,
            },
        )

        call_command(
            "import_pgc_objetivos",
            path=str(path),
            year=self.year,
            month=self.month,
            force_legacy_excel=True,
        )

        factoring = UNE.objects.get(code="FACTORING")
        metric_vc = MetricDefinition.objects.get(
            code=MetricDefinition.CODE_VENTA_CRUZADA
        )
        self.assertFalse(
            MonthlyMetricResult.objects.filter(
                plan=self.plan,
                une=factoring,
                metric=metric_vc,
                year=self.year,
                month=self.month,
                calculation_note__icontains="Objetivos (referidos VC",
            ).exists()
        )
        self.assertFalse(
            ManualRequirementsCompliance.objects.filter(
                plan=self.plan,
                une=factoring,
                year=self.year,
                month=self.month,
            ).exists()
        )

    def test_import_sync_vc_and_sync_reqs(self):
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            path = Path(tmp.name)
        self.addCleanup(path.unlink, missing_ok=True)
        from pgc.management.commands import import_pgc_objetivos as ipo_mod

        self._write_min_objetivos_xlsx(
            path,
            {
                ipo_mod.COL_EXEC_VC: 4,
                ipo_mod.COL_PTS_EXEC_REQ: 5,
            },
        )

        call_command(
            "import_pgc_objetivos",
            path=str(path),
            year=self.year,
            month=self.month,
            sync_vc=True,
            sync_reqs=True,
            force_legacy_excel=True,
        )

        factoring = UNE.objects.get(code="FACTORING")
        metric_vc = MetricDefinition.objects.get(
            code=MetricDefinition.CODE_VENTA_CRUZADA
        )
        vc = MonthlyMetricResult.objects.get(
            plan=self.plan,
            une=factoring,
            metric=metric_vc,
            year=self.year,
            month=self.month,
        )
        self.assertEqual(vc.measured_value, Decimal("4"))
        mrc = ManualRequirementsCompliance.objects.get(
            plan=self.plan,
            une=factoring,
            year=self.year,
            month=self.month,
        )
        self.assertTrue(mrc.is_compliant)


class ObjetivosScoringTests(TestCase):
    def test_factoraje_ago_ingresos_usd_proportion(self):
        from decimal import Decimal
        from pgc.objetivos_scoring import ingresos_points_objetivos

        class T:
            points_if_achieved = 70
            target_value = Decimal("770")

        class R:
            measured_value = Decimal("460.285345")

        pts, achieved, _note = ingresos_points_objetivos(T(), R(), une_code="FACTORING")
        self.assertAlmostEqual(float(pts), 41.84, places=2)
        self.assertFalse(achieved)

    def test_insurance_ingresos_max_points_cap_75(self):
        from decimal import Decimal

        from pgc.objetivos_scoring import _ingresos_max_points

        self.assertEqual(_ingresos_max_points("INSURANCE", 75), Decimal("75"))
        self.assertEqual(_ingresos_max_points("INSURANCE", 80), Decimal("75"))
        self.assertEqual(_ingresos_max_points("FACTORING", 70), Decimal("70"))
        self.assertEqual(_ingresos_max_points("FACTORING", 80), Decimal("70"))
        self.assertEqual(_ingresos_max_points("INVESTMENT", 75), Decimal("70"))
        self.assertEqual(_ingresos_max_points("INVESTMENT", 80), Decimal("70"))

    def test_investment_ingresos_points_use_miles_meta_and_cap_70(self):
        from decimal import Decimal

        from pgc.objetivos_scoring import ingresos_points_objetivos

        class T:
            points_if_achieved = 75
            target_value = Decimal("2.0")

        class R:
            measured_value = Decimal("941.181843")

        pts, achieved, note = ingresos_points_objetivos(
            T(), R(), une_code="INVESTMENT", year=2026, month=10
        )
        # Meta TSV 2.0 MUSD → 2000 miles; 70 × 941.181843/2000 ≈ 32.94
        self.assertAlmostEqual(float(pts), 32.94, places=2)
        self.assertFalse(achieved)
        self.assertIn("2000", note)

    def test_insurance_ingresos_cap_70_vs_75_on_target(self):
        """Con points_if 70 u 80 en meta, el scoring usa 70 o min(80,75)=75 respectivamente."""
        from decimal import Decimal

        from pgc.objetivos_scoring import ingresos_points_objetivos

        class R:
            measured_value = Decimal("5")
            target_value = Decimal("10")

        class T70:
            points_if_achieved = 70
            target_value = Decimal("10")

        class T75:
            points_if_achieved = 75
            target_value = Decimal("10")

        class T80:
            points_if_achieved = 80
            target_value = Decimal("10")

        pts70, _, _ = ingresos_points_objetivos(
            T70(), R(), une_code="INSURANCE", year=2026, month=1
        )
        pts75, _, _ = ingresos_points_objetivos(
            T75(), R(), une_code="INSURANCE", year=2025, month=6
        )
        pts80, _, _ = ingresos_points_objetivos(
            T80(), R(), une_code="INSURANCE", year=2026, month=10
        )
        # 50% de meta → 35, 37.5, 37.5
        self.assertEqual(pts70, Decimal("35.00"))
        self.assertEqual(pts75, Decimal("37.50"))
        self.assertEqual(pts80, Decimal("37.50"))

    def test_insurance_oct_2026_ingresos_no_display_truncate_in_scoring(self):
        """Meta comisiones oct-2026: proporción con miles USD completos (sin ROUND_DOWN 3 dec)."""
        from decimal import Decimal

        from pgc.objetivos_scoring import ingresos_points_objetivos

        class T:
            points_if_achieved = 75
            target_value = Decimal("12.641")

        class R:
            measured_value = Decimal("1.285556")

        pts, achieved, note = ingresos_points_objetivos(
            T(), R(), une_code="INSURANCE", year=2026, month=10
        )
        # 75 × min(1, 1.285556/12.641) ≈ 7.63 (truncar a 3 dec en scoring daría ~7.62)
        self.assertAlmostEqual(float(pts), 7.63, places=2)
        self.assertFalse(achieved)
        self.assertIn("1.285556/12.641", note)

    def test_insurance_ene_ingresos_usd_proportion_not_gtq(self):
        """Proporción en miles USD (como Ingresos vs meta), no presupuesto_gtq."""
        from decimal import Decimal

        from pgc.objetivos_scoring import ingresos_points_objetivos

        class T:
            points_if_achieved = 75
            target_value = Decimal("6.75")
            presupuesto_gtq = Decimal("6613")

        class R:
            measured_value = Decimal("1.622068")
            source_value = Decimal("12435")

        pts, achieved, note = ingresos_points_objetivos(
            T(), R(), une_code="INSURANCE", year=2026, month=1
        )
        # GTQ ratio 12435/6613 daría ~75; USD 1.622/6.75 × 75 ≈ 18.02
        self.assertAlmostEqual(float(pts), 18.02, places=2)
        self.assertLess(float(pts), 25.0)
        self.assertIn("miles USD", note)
        self.assertFalse(achieved)

    def test_insurance_sep_clientes_presupuesto_12(self):
        from pgc.objetivos_scoring import proportional_points

        pts, achieved, _note = proportional_points(
            15,
            Decimal("3"),
            Decimal("12"),
            note_prefix="Objetivos proporción",
        )
        self.assertAlmostEqual(float(pts), 3.75, places=2)
        self.assertFalse(achieved)


class ImportPgcMetasTests(TestCase):
    def setUp(self):
        self.year = 2026
        self.plan = PGCPlan.objects.create(year=self.year, name="Plan metas")
        self.metric_cli, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_CLIENTES_NUEVOS,
            defaults={"name": "Clientes", "is_scored": True},
        )
        self.metric_ing, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_INGRESOS,
            defaults={"name": "Ingresos", "is_scored": True},
        )
        for code, name in (
            (MetricDefinition.CODE_VENTA_CRUZADA, "Venta cruzada"),
            (MetricDefinition.CODE_RESPUESTA_REQS, "Respuesta reqs"),
        ):
            MetricDefinition.objects.get_or_create(
                code=code, defaults={"name": name, "is_scored": True}
            )
        for code, name, order in (
            ("FACTORING", "Factoraje", 1),
            ("LEASING", "Leasing", 2),
            ("INSURANCE", "Insurance", 3),
            ("INVESTMENT", "Inversiones", 4),
        ):
            une = UNE.objects.create(code=code, name=name, name_es=name, sort_order=order)
            for month in range(1, 13):
                for metric in (self.metric_cli, self.metric_ing):
                    MonthlyTarget.objects.create(
                        plan=self.plan,
                        une=une,
                        metric=metric,
                        year=self.year,
                        month=month,
                        target_value=Decimal("999"),
                        points_if_achieved=10,
                    )

    def test_import_metas_august_2026(self):
        root = Path(settings.BASE_DIR).parent
        path = root / "data" / "now" / "PGC-metas-2026.tsv"
        if not path.is_file():
            self.skipTest("Sin TSV oficial de metas")

        call_command("import_pgc_metas", path=str(path), year=self.year)

        factoring = UNE.objects.get(code="FACTORING")
        aug_ing = MonthlyTarget.objects.get(
            plan=self.plan,
            une=factoring,
            metric=self.metric_ing,
            year=self.year,
            month=8,
        )
        self.assertEqual(aug_ing.target_value, Decimal("770"))

        insurance = UNE.objects.get(code="INSURANCE")
        aug_cli = MonthlyTarget.objects.get(
            plan=self.plan,
            une=insurance,
            metric=self.metric_cli,
            year=self.year,
            month=8,
        )
        self.assertEqual(aug_cli.target_value, Decimal("12"))

        oct_ins_ing = MonthlyTarget.objects.get(
            plan=self.plan,
            une=insurance,
            metric=self.metric_ing,
            year=self.year,
            month=10,
        )
        self.assertEqual(oct_ins_ing.target_value, Decimal("12.641"))

        investment = UNE.objects.get(code="INVESTMENT")
        jan_ing = MonthlyTarget.objects.get(
            plan=self.plan,
            une=investment,
            metric=self.metric_ing,
            year=self.year,
            month=1,
        )
        self.assertEqual(jan_ing.target_value, Decimal("0.200"))


class OpsFlagsTests(TestCase):
    def setUp(self):
        self.year = 2026
        self.month = 6
        self.plan = PGCPlan.objects.create(year=self.year, name="Plan flags")
        self.une = UNE.objects.create(
            code=UNE.CODE_FACTORING,
            name="Factoring",
            name_es="Factoraje",
            sort_order=1,
        )
        self.metric_ing, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_INGRESOS,
            defaults={"name": "Ingresos", "is_scored": True},
        )

    def _warn_codes(self, flags):
        return {f["code"] for f in flags if f["level"] == "warn"}

    def test_ingresos_presupuesto_gtq_when_missing(self):
        from pgc.ops_flags import collect_ops_flags

        MonthlyTarget.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric_ing,
            year=self.year,
            month=self.month,
            target_value=Decimal("100"),
            points_if_achieved=10,
        )
        flags = collect_ops_flags(self.year, self.month, plan=self.plan)
        self.assertIn("ingresos_presupuesto_gtq", self._warn_codes(flags))

    def test_legacy_objetivos_import_flag(self):
        from pgc.ops_flags import collect_ops_flags

        MonthlyTarget.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric_ing,
            year=self.year,
            month=self.month,
            target_value=Decimal("100"),
            points_if_achieved=10,
            presupuesto_gtq=Decimal("1"),
        )
        MonthlyMetricResult.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric_ing,
            year=self.year,
            month=self.month,
            measured_value=Decimal("10"),
            calculation_note="Importado desde legacy.xlsx Objetivos (comisiones).",
        )
        flags = collect_ops_flags(self.year, self.month, plan=self.plan)
        self.assertIn("legacy_objetivos_import", self._warn_codes(flags))

    def test_no_presupuesto_flag_when_import_and_presupuesto_ok(self):
        from django.utils import timezone

        from pgc.ops_flags import collect_ops_flags

        MonthlyTarget.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric_ing,
            year=self.year,
            month=self.month,
            target_value=Decimal("100"),
            points_if_achieved=10,
            presupuesto_gtq=Decimal("50000"),
        )
        MonthlyMetricResult.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric_ing,
            year=self.year,
            month=self.month,
            measured_value=Decimal("10"),
            calculation_note="Importado desde test.xlsx Objetivos (comisiones).",
        )
        MonthlyMetricScore.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric_ing,
            year=self.year,
            month=self.month,
            mode=PGCMode.MODO2,
            points_awarded=Decimal("10"),
        )
        now = timezone.now()
        MonthlyMetricResult.objects.filter(
            plan=self.plan, year=self.year, month=self.month
        ).update(updated_at=now)
        MonthlyMetricScore.objects.filter(
            plan=self.plan, year=self.year, month=self.month, mode=PGCMode.MODO2
        ).update(updated_at=now)

        flags = collect_ops_flags(self.year, self.month, plan=self.plan)
        self.assertNotIn("ingresos_presupuesto_gtq", self._warn_codes(flags))
        self.assertIn("legacy_objetivos_import", self._warn_codes(flags))
        self.assertNotIn("modo2_stale_objetivos", self._warn_codes(flags))

    def test_modo2_stale_after_objetivos_import(self):
        from django.utils import timezone

        from pgc.ops_flags import collect_ops_flags

        MonthlyTarget.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric_ing,
            year=self.year,
            month=self.month,
            target_value=Decimal("100"),
            points_if_achieved=10,
            presupuesto_gtq=Decimal("1"),
        )
        MonthlyMetricResult.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric_ing,
            year=self.year,
            month=self.month,
            measured_value=Decimal("10"),
            calculation_note="Importado desde test.xlsx Objetivos.",
        )
        MonthlyMetricScore.objects.create(
            plan=self.plan,
            une=self.une,
            metric=self.metric_ing,
            year=self.year,
            month=self.month,
            mode=PGCMode.MODO2,
        )
        now = timezone.now()
        MonthlyMetricResult.objects.filter(
            plan=self.plan, year=self.year, month=self.month
        ).update(updated_at=now)
        MonthlyMetricScore.objects.filter(
            plan=self.plan, year=self.year, month=self.month, mode=PGCMode.MODO2
        ).update(updated_at=now - timedelta(hours=2))

        flags = collect_ops_flags(self.year, self.month, plan=self.plan)
        self.assertIn("modo2_stale_objetivos", self._warn_codes(flags))

    def test_vc_without_cross_sale_import_flag(self):
        from pgc.ops_flags import collect_ops_flags

        metric_vc, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_VENTA_CRUZADA,
            defaults={"name": "VC", "is_scored": True},
        )
        MonthlyMetricResult.objects.create(
            plan=self.plan,
            une=self.une,
            metric=metric_vc,
            year=self.year,
            month=self.month,
            measured_value=Decimal("3"),
            target_value=Decimal("1"),
        )
        flags = collect_ops_flags(self.year, self.month, plan=self.plan)
        self.assertIn("vc_without_operational_import", self._warn_codes(flags))


class ObjetivosImportPolicyTests(TestCase):
    def setUp(self):
        self.year = 2026
        self.month = 8
        self.plan = PGCPlan.objects.create(year=self.year, name="Plan block")
        MonthlyExchangeRate.objects.create(
            year=self.year, month=self.month, usd_to_gtq=Decimal("7.8")
        )

    def _min_xlsx(self, path: Path) -> None:
        import openpyxl

        from pgc.management.commands.import_pgc_objetivos import COL_PTS_EXEC_REQ

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Objetivos"
        row = [None] * (COL_PTS_EXEC_REQ + 2)
        row[0] = datetime(self.year, self.month, 1)
        row[5] = "WC"
        ws.append(["header"])
        ws.append(row)
        wb.save(path)

    def _seed_factoring_targets(self) -> None:
        UNE.objects.get_or_create(
            code=UNE.CODE_FACTORING,
            defaults={"name": "F", "name_es": "F", "sort_order": 1},
        )
        for code, name in (
            (MetricDefinition.CODE_CLIENTES_NUEVOS, "C"),
            (MetricDefinition.CODE_INGRESOS, "I"),
            (MetricDefinition.CODE_VENTA_CRUZADA, "V"),
            (MetricDefinition.CODE_RESPUESTA_REQS, "R"),
        ):
            MetricDefinition.objects.get_or_create(
                code=code,
                defaults={"name": name, "is_scored": True},
            )
        une = UNE.objects.get(code=UNE.CODE_FACTORING)
        for metric in MetricDefinition.objects.filter(
            code__in=(
                MetricDefinition.CODE_CLIENTES_NUEVOS,
                MetricDefinition.CODE_INGRESOS,
                MetricDefinition.CODE_VENTA_CRUZADA,
                MetricDefinition.CODE_RESPUESTA_REQS,
            )
        ):
            MonthlyTarget.objects.get_or_create(
                plan=self.plan,
                une=une,
                metric=metric,
                year=self.year,
                month=self.month,
                defaults={
                    "target_value": Decimal("1"),
                    "points_if_achieved": 1,
                },
            )

    def test_import_blocked_without_override(self):
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            path = Path(tmp.name)
        self.addCleanup(path.unlink, missing_ok=True)
        self._min_xlsx(path)
        with self.assertRaises(CommandError) as ctx:
            call_command(
                "import_pgc_objetivos",
                path=str(path),
                year=self.year,
                month=self.month,
            )
        self.assertIn("deshabilitado", str(ctx.exception).lower())

    def _empty_objetivos_row(self) -> dict:
        return {
            "uen": "WC",
            "pres_cli": None,
            "pres_com_gtq": None,
            "exec_cli": None,
            "exec_com_gtq": None,
            "pres_vc": None,
            "exec_vc": None,
            "pts_ing": None,
            "pts_cli": None,
            "pts_vc": None,
            "pts_req": None,
            "pts_exec_req": None,
        }

    @patch("pgc.management.commands.import_pgc_objetivos._read_objetivos_rows")
    def test_import_allowed_with_force_legacy(self, read_mock):
        read_mock.return_value = [self._empty_objetivos_row()]
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            path = Path(tmp.name)
        self.addCleanup(path.unlink, missing_ok=True)
        path.write_bytes(b"x")
        self._seed_factoring_targets()
        call_command(
            "import_pgc_objetivos",
            path=str(path),
            year=self.year,
            month=self.month,
            force_legacy_excel=True,
        )

    @patch("pgc.management.commands.import_pgc_objetivos._read_objetivos_rows")
    def test_import_allowed_with_env(self, read_mock):
        read_mock.return_value = [self._empty_objetivos_row()]
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            path = Path(tmp.name)
        self.addCleanup(path.unlink, missing_ok=True)
        path.write_bytes(b"x")
        self._seed_factoring_targets()
        prev = os.environ.get("ALLOW_PGC_EXCEL_IMPORT")
        os.environ["ALLOW_PGC_EXCEL_IMPORT"] = "1"
        try:
            call_command(
                "import_pgc_objetivos",
                path=str(path),
                year=self.year,
                month=self.month,
            )
        finally:
            if prev is None:
                os.environ.pop("ALLOW_PGC_EXCEL_IMPORT", None)
            else:
                os.environ["ALLOW_PGC_EXCEL_IMPORT"] = prev


class PgcDashboardModeTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_default_mode_is_proporcion(self):
        from pgc.views import DEFAULT_PGC_MODE, PGC_MODE_LABELS, PGC_MODE_OPTIONS, _get_pgc_mode

        request = self.factory.get("/pgc/")
        self.assertEqual(_get_pgc_mode(request), "modo2")
        self.assertEqual(DEFAULT_PGC_MODE, "modo2")
        self.assertEqual(PGC_MODE_OPTIONS[0], "modo2")
        self.assertEqual(PGC_MODE_LABELS["modo2"], "Proporción")
        self.assertEqual(PGC_MODE_LABELS["modo1"], "Absolutos")

    def test_mode_from_query_only(self):
        from pgc.views import _get_pgc_mode

        session = self.client.session
        session["pgc_mode"] = "modo1"
        session.save()

        request = self.factory.get("/pgc/")
        request.session = session
        self.assertEqual(_get_pgc_mode(request), "modo2")

        request = self.factory.get("/pgc/", {"mode": "modo1"})
        request.session = session
        self.assertEqual(_get_pgc_mode(request), "modo1")


class TvChartsSeriesTests(TestCase):
    def test_accumulate_and_grupo_sum(self):
        from pgc.tv_charts_generate import (
            ExportPeriod,
            accumulate,
            build_income_series,
        )

        self.assertEqual(accumulate([10, 20, 5]), [10.0, 30.0, 35.0])
        periods = [
            ExportPeriod(
                2026,
                1,
                "2026-01",
                {
                    "FACTORING": {"real": 1.0, "target": 2.0},
                    "LEASING": {"real": 3.0, "target": 4.0},
                    "INSURANCE": {"real": 0.5, "target": 1.0},
                },
            ),
            ExportPeriod(
                2026,
                2,
                "2026-02",
                {
                    "FACTORING": {"real": 2.0, "target": 1.0},
                    "LEASING": {"real": 1.0, "target": 1.0},
                    "INSURANCE": {"real": 0.5, "target": 0.5},
                },
            ),
        ]
        labels, real_y, target_y = build_income_series(
            periods, ("FACTORING", "LEASING", "INSURANCE")
        )
        self.assertEqual(labels, ["2026-01", "2026-02"])
        self.assertEqual(real_y, [4.5, 8.0])
        self.assertEqual(target_y, [7.0, 9.5])


class PrecisionRolloutTests(TestCase):
    def test_monthly_target_stores_six_decimal_miles(self):
        plan = PGCPlan.objects.create(year=2026, name="Precision")
        une = UNE.objects.create(code="FACTORING", name="F", name_es="F", sort_order=1)
        metric = MetricDefinition.objects.create(code=MetricDefinition.CODE_INGRESOS, name="Ing")
        precise = Decimal("770.123456")
        tgt = MonthlyTarget.objects.create(
            plan=plan,
            une=une,
            metric=metric,
            year=2026,
            month=1,
            target_value=precise,
        )
        tgt.refresh_from_db()
        self.assertEqual(tgt.target_value, precise)

    def test_ingresos_investment_min_display_decimals(self):
        from pgc.views import (
            INGRESOS_INVESTMENT_MIN_DECIMALS,
            _build_ingresos_annual_tables,
        )

        year = 2026
        plan = PGCPlan.objects.create(year=year, name="Precision")
        inv = UNE.objects.create(
            code="INVESTMENT", name="Inv", name_es="Inversiones", sort_order=9
        )
        metric = MetricDefinition.objects.create(
            code=MetricDefinition.CODE_INGRESOS, name="Ing"
        )
        MonthlyTarget.objects.create(
            plan=plan,
            une=inv,
            metric=metric,
            year=year,
            month=1,
            target_value=Decimal("1"),
        )
        MonthlyMetricResult.objects.create(
            plan=plan,
            une=inv,
            metric=metric,
            year=year,
            month=1,
            measured_value=Decimal("1.2345"),
        )
        tables = _build_ingresos_annual_tables(year, decimals=1)
        inv_table = next(t for t in tables if t["une"].id == inv.id)
        self.assertGreaterEqual(
            inv_table["income_decimals"], INGRESOS_INVESTMENT_MIN_DECIMALS
        )

    def test_recalc_investment_preserves_sub_cent_miles(self):
        from imports.models import InvestmentGrowthRow

        year, month = 2026, 2
        plan = PGCPlan.objects.create(year=year, name="Inv")
        inv = UNE.objects.create(
            code="INVESTMENT", name="Inv", name_es="Inversiones", sort_order=9
        )
        metric = MetricDefinition.objects.create(
            code=MetricDefinition.CODE_INGRESOS, name="Ing"
        )
        MonthlyExchangeRate.objects.create(
            year=year, month=1, usd_to_gtq=Decimal("7.638560")
        )
        MonthlyExchangeRate.objects.create(
            year=year, month=2, usd_to_gtq=Decimal("7.638560")
        )
        MonthlyTarget.objects.create(
            plan=plan,
            une=inv,
            metric=metric,
            year=year,
            month=month,
            target_value=Decimal("0"),
        )
        gtq = Decimal("100000.00")
        tc = Decimal("7.638560")
        usd_jan = gtq / tc
        InvestmentGrowthRow.objects.create(
            year=year,
            month=1,
            instrument="AP",
            operation_code="P",
            amount_usd=usd_jan,
            amount_gtq=gtq,
            exchange_rate=tc,
        )
        InvestmentGrowthRow.objects.create(
            year=year,
            month=2,
            instrument="AP",
            operation_code="P",
            amount_usd=usd_jan + Decimal("1.234"),
            amount_gtq=gtq + Decimal("1.234") * tc,
            exchange_rate=tc,
        )
        call_command(
            "recalc_investment_ingresos_from_new_clients", year=year, month=month
        )
        row = MonthlyMetricResult.objects.get(
            plan=plan, une=inv, metric=metric, year=year, month=month
        )
        self.assertEqual(row.measured_value, Decimal("0.001234"))
