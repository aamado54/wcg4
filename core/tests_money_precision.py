from decimal import Decimal

from django.test import SimpleTestCase

from core.money_precision import money_equal, quantize_store


class MoneyPrecisionTests(SimpleTestCase):
    def test_money_equal_uses_six_decimal_storage(self):
        self.assertTrue(money_equal(Decimal("100.001234"), Decimal("100.0012344")))
        self.assertFalse(money_equal(Decimal("100.001234"), Decimal("100.001235")))

    def test_quantize_store_half_up(self):
        self.assertEqual(
            quantize_store(Decimal("1.23456789")),
            Decimal("1.234568"),
        )