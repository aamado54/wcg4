"""Smoke tests for financiero institucional board."""

from django.test import TestCase
from django.urls import reverse

from risk.financiero.reports import build_financiero_board
from risk.financiero.reader import load_combined


class FinancieroInstitucionalTests(TestCase):
    def test_load_combined_ok(self):
        data = load_combined()
        self.assertEqual(data.get("status"), "ok")
        self.assertTrue(data.get("periods"))
        self.assertIn("T", data.get("kpis") or {})

    def test_build_board(self):
        board = build_financiero_board(load_combined(), bu="T")
        self.assertEqual(board.status, "ok")
        self.assertTrue(board.summary_cards)
        self.assertTrue(board.bu_table)
        self.assertTrue(board.chart_activo.get("labels"))

    def test_view_requires_login(self):
        url = reverse("risk:financiero_institucional")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_view_ok_when_logged_in(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user("fi_tester", password="x")
        self.client.force_login(user)
        resp = self.client.get(reverse("risk:financiero_institucional"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Estados financieros")
        self.assertContains(resp, "Utilidad contable")
