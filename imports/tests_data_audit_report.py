"""Smoke tests: vista auditoría de datos (repositorio)."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class DataAuditReportViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dataaudit", password="x")
        self.client = Client()
        self.client.login(username="dataaudit", password="x")
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        mod = self.root / "1-pgc" / "2601"
        mod.mkdir(parents=True)
        (mod / "VENTA_CRUZADA_PGC.csv").write_text("a", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_requires_login(self):
        anon = Client()
        url = reverse("imports:data_audit_report")
        self.assertEqual(anon.get(url).status_code, 302)

    @patch("imports.audit_views.repo_data_root")
    def test_report_200_and_lists_file(self, mock_root):
        mock_root.return_value = self.root
        url = reverse("imports:data_audit_report")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Auditoría de datos")
        self.assertContains(resp, "VENTA_CRUZADA_PGC.csv")

    @patch("imports.audit_views.repo_data_root")
    def test_refresh_bypasses_cache(self, mock_root):
        mock_root.return_value = self.root
        url = reverse("imports:data_audit_report")
        resp1 = self.client.get(url)
        self.assertEqual(resp1.status_code, 200)
        resp2 = self.client.get(url, {"refresh": "1"})
        self.assertEqual(resp2.status_code, 200)
        self.assertContains(resp2, "escaneo nuevo")