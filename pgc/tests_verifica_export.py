"""Tests export verifica — parse plantilla y conteo filas 62–121."""

from pathlib import Path

from django.test import SimpleTestCase

from pgc.verifica_export import (
    EXPECTED_ROW_COUNT,
    ROW_END_2026,
    ROW_START_2026,
    normalize_wc_code,
    parse_verifica_template_rows,
)


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

    def test_wcg_rows_without_points_flag(self):
        path = self._template_path()
        if not path.is_file():
            self.skipTest("verifica.tsv no presente")
        specs = parse_verifica_template_rows(path, year=2026)
        wcg = [s for s in specs if s.wc_code == "WCG"]
        self.assertEqual(len(wcg), 12)
        self.assertTrue(all(not s.has_points for s in wcg))