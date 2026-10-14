from django.test import SimpleTestCase, TestCase

from core.models import UNE
from imports.new_client_rules import (
    aggregate_clientes_nuevos_counts,
    counts_toward_clientes_nuevos_metric,
    intercompany_investment_operation_codes,
    is_intercompany_investment_growth_row,
    is_wc_group_entity,
    normalize_nit,
    raw_une_is_external_investment_category,
)


class NewClientRulesUnitTests(SimpleTestCase):
    def test_normalize_nit_strips_formatting(self):
        self.assertEqual(normalize_nit("475112-4"), "4751124")
        self.assertEqual(normalize_nit("9209549-6"), "92095496")

    def test_group_entity_detection(self):
        self.assertTrue(
            is_wc_group_entity("11339813-1", "WORKING CAPITAL LEASING, S.A.")
        )
        self.assertTrue(
            is_wc_group_entity("15575399622024", "WORKING CAPITAL HOLDING GROUP INC.")
        )
        self.assertFalse(is_wc_group_entity("2339595", "CARLOS DURÁN NAJARRO"))

    def test_insurance_never_counts(self):
        self.assertFalse(
            counts_toward_clientes_nuevos_metric(
                une_code=UNE.CODE_INSURANCE,
                raw_une="Insurance",
                nit="11339813-1",
                client_name="WORKING CAPITAL LEASING, S.A.",
                counts_as_new=True,
            )
        )

    def test_investment_only_leasing_and_wchg_categories(self):
        self.assertTrue(
            raw_une_is_external_investment_category("INVESTMENT - WC LEASING")
        )
        self.assertTrue(
            raw_une_is_external_investment_category(
                "INVESTMENT - WORKING CAPITAL HOLDING GROUP INC."
            )
        )
        self.assertFalse(
            raw_une_is_external_investment_category("INVESTMENT - WC FACTORING")
        )

    def test_investment_external_row_counts(self):
        self.assertTrue(
            counts_toward_clientes_nuevos_metric(
                une_code=UNE.CODE_INVESTMENT,
                raw_une="INVESTMENT - WC LEASING",
                nit="2339595",
                client_name="CARLOS DURÁN NAJARRO",
                counts_as_new=True,
            )
        )
        self.assertFalse(
            counts_toward_clientes_nuevos_metric(
                une_code=UNE.CODE_INVESTMENT,
                raw_une="INVESTMENT - WC FACTORING",
                nit="5024765",
                client_name="CESAR LOPEZ YUMAN",
                counts_as_new=True,
            )
        )
        self.assertFalse(
            counts_toward_clientes_nuevos_metric(
                une_code=UNE.CODE_INVESTMENT,
                raw_une="INVESTMENT - WC FACTORING",
                nit="15575399622024",
                client_name="WORKING CAPITAL HOLDING GROUP INC.",
                counts_as_new=True,
            )
        )

    def test_intercompany_growth_filter(self):
        ops = {"AP01260904", "AP01260701"}
        self.assertTrue(
            is_intercompany_investment_growth_row(
                "INVESTMENT - WC FACTORING",
                "AP01260904",
                intercompany_ops=ops,
            )
        )
        self.assertFalse(
            is_intercompany_investment_growth_row(
                "INVESTMENT - WC LEASING",
                "PG02260903",
                intercompany_ops=ops,
            )
        )


class NewClientRulesAggregationTests(TestCase):
    def test_unique_nits_all_unes_including_investment(self):
        class Row:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)

        class FakeUne:
            def __init__(self, code, id):
                self.code = code
                self.id = id

        leasing = FakeUne(UNE.CODE_LEASING, 2)
        investment = FakeUne(UNE.CODE_INVESTMENT, 4)

        rows = [
            Row(
                une=leasing,
                year=2026,
                month=9,
                nit="475112-4",
                client_name="BODEGA",
                operation_code="VHLEASE010057",
                raw_une_value="Leasing",
                counts_as_new=True,
            ),
            Row(
                une=leasing,
                year=2026,
                month=9,
                nit="475112-4",
                client_name="BODEGA",
                operation_code="VHLEASE010058",
                raw_une_value="Leasing",
                counts_as_new=True,
            ),
            Row(
                une=leasing,
                year=2026,
                month=9,
                nit="9209549-6",
                client_name="MOGORI",
                operation_code="ANTLEASE080025",
                raw_une_value="Leasing",
                counts_as_new=True,
            ),
            Row(
                une=investment,
                year=2026,
                month=9,
                nit="2339595",
                client_name="CARLOS",
                operation_code="PG02260903",
                raw_une_value="INVESTMENT - WC LEASING",
                counts_as_new=True,
            ),
            Row(
                une=investment,
                year=2026,
                month=9,
                nit="2339595",
                client_name="CARLOS",
                operation_code="PG02260903B",
                raw_une_value="INVESTMENT - WC LEASING",
                counts_as_new=True,
            ),
            Row(
                une=investment,
                year=2026,
                month=9,
                nit="6139035",
                client_name="JORGE",
                operation_code="PG02260901",
                raw_une_value="INVESTMENT - WC LEASING",
                counts_as_new=True,
            ),
            Row(
                une=investment,
                year=2026,
                month=9,
                nit="",
                client_name="FRANCISCO",
                operation_code="PG02260904",
                raw_une_value="INVESTMENT - WC LEASING",
                counts_as_new=True,
            ),
            Row(
                une=investment,
                year=2026,
                month=9,
                nit="",
                client_name="BI-BANK",
                operation_code="AP03260901",
                raw_une_value="INVESTMENT - WORKING CAPITAL HOLDING GROUP INC.",
                counts_as_new=True,
            ),
            Row(
                une=investment,
                year=2026,
                month=9,
                nit="15575399622024",
                client_name="WORKING CAPITAL HOLDING GROUP INC.",
                operation_code="AP01260904",
                raw_une_value="INVESTMENT - WC FACTORING",
                counts_as_new=True,
            ),
        ]

        counts = aggregate_clientes_nuevos_counts(rows)
        self.assertEqual(counts[(2026, 9, leasing.id)], 2)
        # Mismo NIT en dos operaciones de investment cuenta una sola vez.
        self.assertEqual(counts[(2026, 9, investment.id)], 4)

        factoring = FakeUne(UNE.CODE_FACTORING, 3)
        factoring_rows = rows + [
            Row(
                une=factoring,
                year=2026,
                month=9,
                nit="1111111-1",
                client_name="ACME",
                operation_code="F1",
                raw_une_value="Factoring",
                counts_as_new=True,
            ),
            Row(
                une=factoring,
                year=2026,
                month=9,
                nit="1111111-1",
                client_name="ACME",
                operation_code="F2",
                raw_une_value="Factoring",
                counts_as_new=True,
            ),
        ]
        factoring_counts = aggregate_clientes_nuevos_counts(factoring_rows)
        self.assertEqual(factoring_counts[(2026, 9, factoring.id)], 1)

        ops = intercompany_investment_operation_codes(rows)
        self.assertIn("AP01260904", ops)
