"""Tests unitarios de clasificación layout data/ (sin tocar disco real)."""

from django.test import SimpleTestCase

from core.services.data_layout import (
    YYMM_MODULES,
    classify_file,
    extract_yymm_from_filename,
    resolve_yymm,
)


class DataLayoutModuleTests(SimpleTestCase):
    def test_yymm_modules_fixed_set(self):
        self.assertEqual(YYMM_MODULES, frozenset({"pgc", "pgo", "ger", "pla"}))

    def test_classify_ger_financial_er_bg(self):
        tipo, module, _ = classify_file("WC F ER 2608.csv")
        self.assertEqual(tipo, "financial")
        self.assertEqual(module, "ger")

    def test_classify_pla_not_yymm_module_bucket_via_otros(self):
        tipo, module, _ = classify_file("plantilla_externa.xlsx", ("pla",))
        self.assertEqual(module, "stay")
        self.assertEqual(tipo, "plantilla")

    def test_classify_stay_verifica(self):
        tipo, module, _ = classify_file("verifica-export.tsv", ("now",))
        self.assertEqual(module, "stay")

    def test_yymm_from_eeff_token(self):
        y, src = extract_yymm_from_filename("WCF ER 2609 - Factoring.csv")
        self.assertEqual(y, "2609")
        self.assertEqual(src, "eeff_token")

    def test_yymm_from_spanish_month(self):
        y, src = extract_yymm_from_filename("informe agosto 2026.xlsx")
        self.assertEqual(y, "2608")
        self.assertIn("mes", src)


class DataLayoutResolveTests(SimpleTestCase):
    def test_resolve_prefers_filename(self):
        # Sin archivo en disco: solo nombre
        y, src = extract_yymm_from_filename("clientes_2607.csv")
        self.assertEqual(y, "2607")