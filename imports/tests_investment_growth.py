from decimal import Decimal
from pathlib import Path

from django.test import TestCase

from imports.investment_growth_parse import (
    parse_bancos_fin_mes_xlsx,
    parse_inversiones_crecimiento_csv,
)
from imports.models import BankLoanMonthSnapshot, InvestmentGrowthRow
from pgc.investment_ingresos import (
    investment_gross_usd,
    investment_net_growth_usd,
    investment_periods_with_data,
)


DATA_DIR = Path(__file__).resolve().parents[2] / "data"


class InvestmentGrowthParseTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.csv_path = DATA_DIR / "Inversiones_crecimiento_2026.csv"
        cls.bank_path = DATA_DIR / "Bancos_Fin_de_mes.xlsx"
        if not cls.csv_path.exists():
            alt = Path("/home/caa/wc/wcg4/data/Inversiones_crecimiento_2026.csv")
            if alt.exists():
                cls.csv_path = alt
        if not cls.bank_path.exists():
            alt = Path("/home/caa/wc/wcg4/data/Bancos_Fin_de_mes.xlsx")
            if alt.exists():
                cls.bank_path = alt

    def test_parse_csv_has_multiple_periods(self):
        if not self.csv_path.exists():
            self.skipTest("Archivo de muestra no disponible")
        rows = parse_inversiones_crecimiento_csv(self.csv_path)
        periods = {(r.year, r.month) for r in rows}
        self.assertIn((2025, 12), periods)
        self.assertIn((2026, 7), periods)
        self.assertTrue(any(r.instrument == "AP" for r in rows))
        self.assertTrue(any(r.instrument == "PG" for r in rows))

    def test_parse_banks_detects_quetzalizado_formula(self):
        if not self.bank_path.exists():
            self.skipTest("Archivo de bancos no disponible")
        snaps = parse_bancos_fin_mes_xlsx(self.bank_path)
        self.assertTrue(any(s.year == 2026 and s.month == 7 for s in snaps))
        july = next(s for s in snaps if s.year == 2026 and s.month == 7)
        self.assertGreater(july.total_usd, Decimal("1000000"))


class InvestmentGrowthCalcTests(TestCase):
    def test_net_growth_requires_previous_month(self):
        InvestmentGrowthRow.objects.create(
            year=2025,
            month=12,
            instrument="AP",
            operation_code="APTEST",
            amount_usd=Decimal("100"),
            amount_gtq=Decimal("700"),
        )
        BankLoanMonthSnapshot.objects.create(
            year=2025,
            month=12,
            exchange_rate=Decimal("7"),
            total_gtq=Decimal("700"),
            total_usd=Decimal("100"),
        )
        self.assertIsNone(investment_net_growth_usd(2025, 12))

        InvestmentGrowthRow.objects.create(
            year=2026,
            month=1,
            instrument="AP",
            operation_code="APTEST",
            amount_usd=Decimal("150"),
            amount_gtq=Decimal("1050"),
        )
        BankLoanMonthSnapshot.objects.create(
            year=2026,
            month=1,
            exchange_rate=Decimal("7"),
            total_gtq=Decimal("700"),
            total_usd=Decimal("100"),
        )
        growth = investment_net_growth_usd(2026, 1)
        self.assertEqual(growth, Decimal("50"))
        self.assertEqual(investment_periods_with_data(), [(2025, 12), (2026, 1)])

        gross = investment_gross_usd(2026, 1)
        self.assertEqual(gross["total_usd"], Decimal("250"))
