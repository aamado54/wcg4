from datetime import datetime

from django.test import SimpleTestCase

from pgo.archivos_dates import parse_entrega, parse_inicio


class ArchivosDatesTests(SimpleTestCase):
    def test_inicio_dd_mm_text(self):
        dt = parse_inicio("15-03-2026")
        self.assertEqual(dt, datetime(2026, 3, 15))

    def test_entrega_mm_dd_text(self):
        dt = parse_entrega("03-15-2026")
        self.assertEqual(dt, datetime(2026, 3, 15))

    def test_entrega_disambiguate_day_gt_12(self):
        dt = parse_entrega("15-03-2026")
        self.assertEqual(dt, datetime(2026, 3, 15))
