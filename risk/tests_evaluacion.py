"""Tests de la extensión evaluación financiera (aislada del Comando Balón)."""

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from risk.evaluacion import build_portfolio_view, load_evaluacion
from risk.evaluacion.portfolio import classify_z
from risk.evaluacion.reader import AltmanModel


class EvaluacionReaderTests(SimpleTestCase):
    def test_load_default_xlsx(self):
        ds = load_evaluacion()
        self.assertEqual(ds.status, "ok")
        self.assertFalse(ds.errors, ds.errors)
        self.assertIn("Caratula", ds.sheets_read)
        self.assertIn("Altman", ds.sheets_read)
        self.assertGreaterEqual(len(ds.companies), 10)
        self.assertGreaterEqual(len(ds.altman_models), 3)
        sample = ds.companies[0]
        self.assertTrue(sample.periods)
        self.assertIn("z_emergentes", sample.periods[-1].z_scores)

    def test_missing_file_safe(self):
        ds = load_evaluacion(path="/tmp/no-existe-evaluacion-wcg.xlsx")
        self.assertEqual(ds.status, "error")
        self.assertFalse(ds.companies)
        self.assertTrue(ds.errors)
        pv = build_portfolio_view(ds)
        self.assertEqual(pv.status, "error")
        self.assertEqual(pv.summary["clientes"], 0)

    def test_portfolio_ranking_and_story(self):
        pv = build_portfolio_view(load_evaluacion())
        self.assertIn(pv.status, ("ok", "partial"))
        self.assertGreater(pv.summary["clientes"], 0)
        self.assertTrue(pv.ranking)
        self.assertTrue(pv.headline)
        self.assertIn("concentracion_pct", pv.summary)
        with_z = [r for r in pv.ranking if r.z is not None]
        zs = [r.z for r in with_z]
        self.assertEqual(zs, sorted(zs))

    def test_classify_z_thresholds(self):
        model = AltmanModel(3, "test", 1.23, 2.9, None, None, None)
        self.assertEqual(classify_z(0.5, z_label=None, model=model), "alto")
        self.assertEqual(classify_z(2.0, z_label=None, model=model), "moderado")
        self.assertEqual(classify_z(3.1, z_label=None, model=model), "bajo")
        self.assertEqual(classify_z(9.0, z_label="Mal", model=model), "alto")


class EvaluacionViewTests(TestCase):
    def test_requires_login(self):
        url = reverse("risk:evaluacion_clientes")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login", resp.url)

    def test_comando_balon_still_ok(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user("ev_test", password="x")
        self.client.force_login(user)
        resp = self.client.get(reverse("risk:comando_balon"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Evaluación financiera")
        resp2 = self.client.get(reverse("risk:evaluacion_clientes"))
        self.assertEqual(resp2.status_code, 200)
        self.assertContains(resp2, "Ranking por Z")
        self.assertContains(resp2, "Concentración")
