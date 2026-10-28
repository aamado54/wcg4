from decimal import Decimal
from pathlib import Path

from django.test import TestCase

from imports.ingresos_er_parse import (
    objetivos_style_ingresos_values,
    read_pga_mensuales_comisiones_gtq,
)

PGA_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "now"
    / "0"
    / "PGA Mensuales WC WCL WCI 2026.xlsx"
)
FALLBACK_PGA = (
    Path(__file__).resolve().parents[2].parent
    / "data"
    / "now"
    / "0"
    / "PGA Mensuales WC WCL WCI 2026.xlsx"
)


def _pga_file() -> Path:
    if PGA_PATH.is_file():
        return PGA_PATH
    if FALLBACK_PGA.is_file():
        return FALLBACK_PGA
    return PGA_PATH


class IngresosErParseTests(TestCase):
    def test_objetivos_style_sep_factoring_matches_baseline_db(self):
        """Sep-2026 Factoraje: GTQ PGA → miles USD (GTQ/1000/FX)."""
        fx = Decimal("7.63856")
        gtq = Decimal("1518027.18")
        source, measured = objetivos_style_ingresos_values(gtq, fx)
        self.assertEqual(source, gtq)
        self.assertAlmostEqual(float(measured), 198.73211442994492, places=4)

    def test_read_pga_sep_comisiones_if_file_present(self):
        path = _pga_file()
        if not path.is_file():
            self.skipTest("PGA Mensuales 2026 no disponible en el workspace.")
        gtq = read_pga_mensuales_comisiones_gtq(path, "FACTORING", 9)
        self.assertEqual(gtq, Decimal("1518027.18"))
