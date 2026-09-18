"""Smoke tests Centro Gerencial."""

from django.test import Client, TestCase
from django.urls import reverse

from gerencia.calc import board_indices, board_intermediacion, board_liquidez, load_finance
from gerencia.calc.accounts import div_pref_month, preferentes_stock


class GerenciaCalcTests(TestCase):
    def test_finance_loads(self):
        data = load_finance()
        self.assertIn("kpis", data)
        self.assertTrue(data.get("accounts"))

    def test_real_accounts_exist(self):
        data = load_finance()
        periods = data["periods"]
        latest = periods[-1]
        self.assertGreater(preferentes_stock(data, "F", latest), 0)
        self.assertGreater(preferentes_stock(data, "T", latest), 0)
        self.assertGreater(div_pref_month(data, "T", latest), 0)

    def test_div_pref_sums_f_and_l_then_increment(self):
        from gerencia.calc.accounts import combined_line, DIV_PREF, max0_inc_combined

        data = load_finance()
        latest = data["periods"][-1]
        combined = combined_line(data, ("F", "L"), DIV_PREF, latest)
        self.assertGreater(combined, 0)
        self.assertAlmostEqual(
            div_pref_month(data, "T", latest),
            max0_inc_combined(data, ("F", "L"), DIV_PREF, latest),
        )

    def test_intermediacion_ok(self):
        board = board_intermediacion(bu="T", months=12, mode="gerencial")
        self.assertEqual(board["status"], "ok")
        self.assertEqual(len(board["sections"]), 5)
        self.assertIn("labels", board["chart"])
        self.assertIn("fondeo_detalle", board)
        self.assertIn("preferentes", board["fondeo_detalle"]["totals"])

    def test_overhead_same_contable_gerencial(self):
        c = board_intermediacion(bu="T", months=12, mode="contable")
        g = board_intermediacion(bu="T", months=12, mode="gerencial")
        self.assertAlmostEqual(
            c["aggregated"]["overhead_neto"],
            g["aggregated"]["overhead_neto"],
            places=4,
        )
        self.assertNotAlmostEqual(
            c["aggregated"]["utilidad"],
            g["aggregated"]["utilidad"],
            places=2,
        )

    def test_liquidez_gerencial_normal_same_leverage(self):
        c = board_liquidez(bu="T", vista="contable", strict=False)
        g = board_liquidez(bu="T", vista="gerencial", strict=False)
        self.assertEqual(c["status"], "ok")
        self.assertEqual(g["status"], "ok")
        self.assertEqual(c["cards"][3]["display"], g["cards"][3]["display"])

    def test_liquidez_estricta_higher_leverage(self):
        g = board_liquidez(bu="T", vista="gerencial", strict=False)
        s = board_liquidez(bu="T", vista="gerencial", strict=True)
        self.assertNotEqual(g["cards"][3]["display"], s["cards"][3]["display"])

    def test_indices_rows(self):
        board = board_indices(bu="T", vista="gerencial")
        self.assertEqual(board["status"], "ok")
        self.assertGreaterEqual(len(board["rows"]), 5)

    def test_escenario_nov2026_board(self):
        from gerencia.calc.escenarios import build_nov2026_board, default_shocks

        board = build_nov2026_board(load_finance())
        self.assertEqual(board["status"], "ok")
        self.assertEqual(board["base_period"], "2026-08")
        self.assertIn("mini_balance_corte_rows", board)
        self.assertIn("mini_results", board)
        self.assertIn("mini_results_real", board)
        self.assertIn("mini_results_sim", board)
        self.assertIn("compare_rows", board)
        self.assertIn("balance_end_rows", board)
        self.assertEqual(len(board["chart_timeline"]["labels"]), 11)
        self.assertTrue(board["precautions"])
        self.assertIn("slug", board["precautions"][0])

    def test_sim_base_vivo_differ_with_extreme(self):
        from gerencia.calc.escenarios import BASE_PRESETS, VIVO_PRESETS, build_nov2026_board, default_shocks

        sb = {**default_shocks(), **{k: v for k, v in BASE_PRESETS["cero"].items() if k != "label"}}
        sv = {**default_shocks(), **{k: v for k, v in VIVO_PRESETS["extremo"].items() if k != "label"}}
        board = build_nov2026_board(load_finance(), shocks_base=sb, shocks_vivo=sv)
        self.assertNotEqual(
            board["balance_end_rows"][0]["base"],
            board["balance_end_rows"][0]["vivo"],
        )
        row = board["mini_balance_corte_rows"][0]
        self.assertNotEqual(row["activo_base"], row["activo_vivo"])
        self.assertNotEqual(row["activo_real"], row["activo_vivo"])
        self.assertNotEqual(
            board["mini_results"][0]["base"],
            board["mini_results"][0]["vivo"],
        )
        self.assertNotEqual(
            board["mini_results_sim"][3]["base"],
            board["mini_results_sim"][3]["vivo"],
        )

    def test_factoraje_mom_affects_simulation(self):
        from gerencia.calc.escenarios import build_nov2026_board, default_shocks

        base = default_shocks()
        flat = build_nov2026_board(load_finance(), shocks_base=base, shocks_vivo=base)
        shrink = dict(base)
        shrink["factoraje_mom_pct"] = -5.0
        down = build_nov2026_board(load_finance(), shocks_base=shrink, shocks_vivo=shrink)
        self.assertNotEqual(
            flat["sim_vivo"]["utilidad"][-1],
            down["sim_vivo"]["utilidad"][-1],
        )


class GerenciaViewTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        self.user = User.objects.create_user("caa", password="x")
        self.client = Client()
        self.client.login(username="caa", password="x")

    def test_intermediacion_200(self):
        resp = self.client.get(reverse("gerencia:intermediacion"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Intermediación")
        self.assertContains(resp, "ge-ccy")
        self.assertContains(resp, "detalle")

    def test_ccy_switch(self):
        resp = self.client.get(reverse("gerencia:set_ccy") + "?ccy=USD", follow=False)
        self.assertEqual(resp.status_code, 302)
        session = self.client.session
        self.assertEqual(session.get("gerencia_ccy"), "USD")

    def test_liquidez_200(self):
        resp = self.client.get(reverse("gerencia:liquidez"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "bandas")

    def test_comando_200(self):
        resp = self.client.get(reverse("gerencia:comando"))
        self.assertEqual(resp.status_code, 200)

    def test_escenarios_200(self):
        resp = self.client.get(reverse("gerencia:escenarios"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Escenarios")
        self.assertContains(resp, "ge-nav-scenarios")

    def test_escenario_nov2026_200(self):
        resp = self.client.get(reverse("gerencia:escenario_nov2026"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Mini balance")
        self.assertContains(resp, "Drivers · base vs vivo")
        self.assertContains(resp, "Base cero")
        self.assertContains(resp, "Vivo moderado")
        self.assertContains(resp, "esc-split-coach")
        self.assertContains(resp, "Scroll en cada mitad")

    def test_escenario_preset(self):
        resp = self.client.get(reverse("gerencia:escenario_nov2026") + "?preset_vivo=severo")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Comparación base vs vivo")

    def test_escenario_preset_base(self):
        resp = self.client.get(reverse("gerencia:escenario_nov2026") + "?preset_base=moderado")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Base moderado")

    def test_escenario_precaucion(self):
        resp = self.client.get(
            reverse("gerencia:escenario_nov2026_precaucion", kwargs={"slug": "liquidez-war-room"})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Regreso")
        self.assertContains(resp, "Qué significa")

    def test_whatif_200(self):
        resp = self.client.get(reverse("gerencia:whatif"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Comparar con anterior")

    def test_config_strict(self):
        resp = self.client.get(reverse("gerencia:config"))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(reverse("gerencia:config"), {"strict_gerencial": "on"})
        self.assertEqual(resp.status_code, 302)
        from gerencia.models import GerenciaSettings

        self.assertTrue(GerenciaSettings.get().strict_gerencial)
