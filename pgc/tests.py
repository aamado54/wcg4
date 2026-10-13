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
from django.test import TestCase

from core.models import MetricDefinition, UNE
from pgc.admin_manual import save_fx, save_results
from pgc.income_conversion import gtq_to_usd, recalc_stale_ingresos
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
    def test_factoraje_ago_ingresos_gtq_proportion(self):
        from decimal import Decimal
        from pgc.objetivos_scoring import ingresos_points_objetivos

        class T:
            points_if_achieved = 70
            presupuesto_gtq = Decimal("770000")
            target_value = Decimal("770")

        class R:
            source_currency = "GTQ"
            source_value = Decimal("460285")
            measured_value = Decimal("60.29")

        pts, achieved, _note = ingresos_points_objetivos(T(), R(), une_code="FACTORING")
        self.assertAlmostEqual(float(pts), 41.84, places=1)
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
        self.assertEqual(aug_cli.target_value, Decimal("3"))

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
