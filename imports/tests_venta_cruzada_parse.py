from datetime import date
from pathlib import Path

from django.test import SimpleTestCase

from imports.venta_cruzada_parse import (
    parse_cross_sale_date,
    parse_cross_sale_period,
)


class VentaCruzadaParseTests(SimpleTestCase):
    def test_period_numeric(self):
        self.assertEqual(parse_cross_sale_period("2026/10"), (2026, 10))

    def test_period_spanish_month(self):
        self.assertEqual(parse_cross_sale_period("octubre"), (2026, 10))
        self.assertEqual(parse_cross_sale_period("septeimbre"), (2026, 9))

    def test_date_iso_and_slash(self):
        self.assertEqual(parse_cross_sale_date("2026-10-28"), date(2026, 10, 28))
        self.assertEqual(parse_cross_sale_date("10/28/2026"), date(2026, 10, 28))