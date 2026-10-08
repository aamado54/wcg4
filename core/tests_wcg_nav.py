from django.test import RequestFactory, TestCase

from core.wcg_nav import resolve_wcg_nav


class WcgNavTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_clientes_nuevos_highlights_pgc_and_section(self):
        request = self.factory.get("/clientes-nuevos/")
        nav = resolve_wcg_nav(request)
        self.assertEqual(nav["module"], "pgc")
        self.assertEqual(nav["pgc_section"], "clientes")

    def test_tablero_section(self):
        request = self.factory.get("/tablero/")
        nav = resolve_wcg_nav(request)
        self.assertEqual(nav["pgc_section"], "tablero")

    def test_admin_hub_is_ops_not_pgc_reports(self):
        request = self.factory.get("/admin-hub/mensual/")
        nav = resolve_wcg_nav(request)
        self.assertEqual(nav["module"], "ops")
        self.assertEqual(nav["pgc_section"], "")
