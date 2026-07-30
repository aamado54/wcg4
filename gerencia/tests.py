"""Smoke tests Centro Gerencial."""

from django.test import Client, TestCase
from django.urls import reverse

from gerencia.calc import board_indices, board_intermediacion, board_liquidez, load_finance


class GerenciaCalcTests(TestCase):
    def test_finance_loads(self):
        data = load_finance()
        self.assertIn("kpis", data)

    def test_intermediacion_ok(self):
        board = board_intermediacion(bu="T", months=12, mode="gerencial")
        self.assertEqual(board["status"], "ok")
        self.assertEqual(len(board["sections"]), 5)
        self.assertIn("labels", board["chart"])

    def test_liquidez_has_bands_and_peers(self):
        board = board_liquidez(bu="T")
        self.assertEqual(board["status"], "ok")
        self.assertTrue(board["cards"])
        self.assertTrue(board["peers"])
        self.assertIn("guides_liq", board["chart"])

    def test_indices_rows(self):
        board = board_indices(bu="T")
        self.assertEqual(board["status"], "ok")
        self.assertGreaterEqual(len(board["rows"]), 5)


class GerenciaViewTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        self.user = User.objects.create_user("gerencia_tester", password="x")
        self.client = Client()
        self.client.login(username="gerencia_tester", password="x")

    def test_intermediacion_200(self):
        resp = self.client.get(reverse("gerencia:intermediacion"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Intermediación")

    def test_liquidez_200(self):
        resp = self.client.get(reverse("gerencia:liquidez"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "bandas")

    def test_comando_200(self):
        resp = self.client.get(reverse("gerencia:comando"))
        self.assertEqual(resp.status_code, 200)

    def test_whatif_200(self):
        resp = self.client.get(reverse("gerencia:whatif"))
        self.assertEqual(resp.status_code, 200)
