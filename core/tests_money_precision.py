from decimal import Decimal

from django.test import SimpleTestCase

import pandas as pd

from core.money_precision import money_equal, quantize_store
from core.services.column_map import pick_money_decimal


class MoneyPrecisionTests(SimpleTestCase):
    def test_money_equal_uses_six_decimal_storage(self):
        self.assertTrue(money_equal(Decimal("100.001234"), Decimal("100.0012344")))
        self.assertFalse(money_equal(Decimal("100.001234"), Decimal("100.001235")))

    def test_quantize_store_half_up(self):
        self.assertEqual(
            quantize_store(Decimal("1.23456789")),
            Decimal("1.234568"),
        )

    def test_pick_money_decimal_normalizes_row(self):
        row = pd.Series({"monto": "1234.567891"})
        self.assertEqual(
            pick_money_decimal(row, "monto"),
            Decimal("1234.567891"),
        )