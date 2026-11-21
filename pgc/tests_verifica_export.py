"""Tests export verifica — parse plantilla y conteo filas 62–121."""

from decimal import Decimal
from pathlib import Path

from django.test import SimpleTestCase, TestCase

from core.models import MetricDefinition, UNE
from pgc.models import MonthlyMetricResult, MonthlyTarget, PGCPlan
from pgc.verifica_export import (
    EXPECTED_ROW_COUNT,
    ROW_END_2026,
    ROW_START_2026,
    VERIFICA_UNE_ORDER,
    VerificaRowSpec,
    build_output_row,
    default_row_specs,
    normalize_wc_code,
    parse_verifica_template_rows,
    _presupuesto_comisiones_gtq,
)


def expected_une_then_month_keys() -> list[tuple[str, int]]:
    return [(wc, month) for wc in VERIFICA_UNE_ORDER for month in range(1, 13)]


class VerificaParseTests(SimpleTestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[2]
        self.template = self.root / "data" / "ref" / "verifica.tsv"
        self.fallback = self.root / "data" / "now" / "verifica.tsv"

    def _template_path(self) -> Path:
        if self.template.is_file():
            return self.template
        return self.fallback

    def test_normalize_wc_codes(self):
        self.assertEqual(normalize_wc_code("INVESTMENTS"), "WCINV")
        self.assertEqual(normalize_wc_code(" WCG"), "WCG")
        self.assertEqual(normalize_wc_code("wc"), "WC")

    def test_parse_2026_row_count(self):
        path = self._template_path()
        if not path.is_file():
            self.skipTest("verifica.tsv no presente en data/ref o data/now")
        specs = parse_verifica_template_rows(path, year=2026)
        self.assertEqual(len(specs), EXPECTED_ROW_COUNT)
        self.assertEqual(EXPECTED_ROW_COUNT, ROW_END_2026 - ROW_START_2026 + 1)

    def test_parse_2026_months_and_uens(self):
        path = self._template_path()
        if not path.is_file():
            self.skipTest("verifica.tsv no presente")
        specs = parse_verifica_template_rows(path, year=2026)
        months = {s.month for s in specs}
        self.assertEqual(months, set(range(1, 13)))
        codes = {s.wc_code for s in specs}
        self.assertEqual(codes, {"WC", "WCL", "WCI", "WCINV", "WCG"})

    def test_parse_2026_row_order_une_then_month(self):
        path = self._template_path()
        if not path.is_file():
            self.skipTest("verifica.tsv no presente")
        specs = parse_verifica_template_rows(path, year=2026)
        actual = [(s.wc_code, s.month) for s in specs]
        self.assertEqual(actual, expected_une_then_month_keys())

    def test_default_row_specs_matches_template_order(self):
        specs = default_row_specs(2026)
        self.assertEqual(len(specs), EXPECTED_ROW_COUNT)
        actual = [(s.wc_code, s.month) for s in specs]
        self.assertEqual(actual, expected_une_then_month_keys())
        path = self._template_path()
        if path.is_file():
            from_template = parse_verifica_template_rows(path, year=2026)
            self.assertEqual(
                [(s.wc_code, s.month) for s in from_template],
                actual,
            )

    def test_wcg_rows_without_points_flag(self):
        path = self._template_path()
        if not path.is_file():
            self.skipTest("verifica.tsv no presente")
        specs = parse_verifica_template_rows(path, year=2026)
        wcg = [s for s in specs if s.wc_code == "WCG"]
        self.assertEqual(len(wcg), 12)
        self.assertTrue(all(not s.has_points for s in wcg))


class VerificaBuildOutputTests(TestCase):
    def setUp(self):
        self.plan = PGCPlan.objects.create(year=2026, name="Verifica")
        self.factoring = UNE.objects.create(
            code=UNE.CODE_FACTORING,
            name="Factoring",
            name_es="Factoraje",
            sort_order=1,
        )
        self.metric_ing, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_INGRESOS,
            defaults={"name": "Ingresos", "is_scored": True},
        )
        self.metric_cli, _ = MetricDefinition.objects.get_or_create(
            code=MetricDefinition.CODE_CLIENTES_NUEVOS,
            defaults={"name": "Clientes", "is_scored": True},
        )

    def test_presupuesto_comisiones_falls_back_to_meta_miles_times_1000(self):
        tgt = MonthlyTarget.objects.create(
            plan=self.plan,
            une=self.factoring,
            metric=self.metric_ing,
            year=2026,
            month=4,
            target_value=Decimal("440"),
            presupuesto_gtq=None,
        )
        self.assertEqual(_presupuesto_comisiones_gtq(tgt), Decimal("440000"))

    def test_exec_com_usd_from_measured_miles_not_gtq(self):
        MonthlyTarget.objects.create(
            plan=self.plan,
            une=self.factoring,
            metric=self.metric_cli,
            year=2026,
            month=5,
            target_value=Decimal("1"),
        )
        MonthlyTarget.objects.create(
            plan=self.plan,
            une=self.factoring,
            metric=self.metric_ing,
            year=2026,
            month=5,
            target_value=Decimal("770"),
            presupuesto_gtq=Decimal("770000"),
        )
        MonthlyMetricResult.objects.create(
            plan=self.plan,
            une=self.factoring,
            metric=self.metric_ing,
            year=2026,
            month=5,
            measured_value=Decimal("219.483"),
            source_currency="GTQ",
            source_value=Decimal("999999"),
        )
        spec = VerificaRowSpec(year=2026, month=5, wc_code="WC", label_a="May-26")
        row = build_output_row(spec, self.plan)
        self.assertEqual(row[3], "770000")
        self.assertEqual(row[5], "219483")