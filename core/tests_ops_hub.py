from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from core.ops_hub import build_ops_hub, hub_landing_groups
from pgc.admin_recalc import get_auto_recalc_enabled


class OpsHubNavTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("ops", password="x")
        self.factory = RequestFactory()

    def test_admin_hub_path_is_home_section(self):
        request = self.factory.get("/admin-hub/")
        request.user = self.user
        hub = build_ops_hub(request)
        self.assertIsNotNone(hub)
        self.assertEqual(hub["active_section"], "home")

    def test_monthly_path_is_pgc_section(self):
        request = self.factory.get("/admin-hub/mensual/?year=2026&month=5")
        request.user = self.user
        hub = build_ops_hub(request)
        self.assertEqual(hub["active_section"], "pgc")
        active = [s for s in hub["subsections"] if s["active"]]
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0]["id"], "monthly")

    def test_landing_groups_ordered(self):
        request = self.factory.get("/admin-hub/")
        request.user = self.user
        groups = hub_landing_groups(request)
        titles = [g["title"] for g in groups]
        self.assertEqual(titles[0], "PGC · Cierre mensual")
        self.assertIn("Importación de datos", titles)

    def test_auto_recalc_enabled_by_default(self):
        self.assertTrue(get_auto_recalc_enabled())
