from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from reports.md_utils import h2, join_sections, md_table, normalize_markdown, p
from reports.naming import stamp_filename, report_stamp
from reports.services import generate_report_package


class ReportNamingTests(TestCase):
    def test_stamp_pattern(self):
        name = stamp_filename("reporte_pgc", "md")
        # e.g. reporte_pgc 26-07 16-05.md
        self.assertRegex(name, r"^reporte_pgc \d{2}-\d{2} \d{2}-\d{2}\.md$")
        self.assertTrue(report_stamp().startswith(" "))


class MarkdownFormatTests(TestCase):
    def test_blank_line_before_table(self):
        md = join_sections(
            h2("Clientes nuevos — detalle completo (browse)"),
            p("Equivalente al detalle visto en Administración. Registros: **40**."),
            md_table(
                ["Periodo", "UNE", "Cliente"],
                [["2026-01", "INVESTMENT", "EDGAR ESTUARDO ORTIZ FUENTES"]],
            ),
        )
        self.assertIn(
            "Registros: **40**.\n\n| Periodo | UNE | Cliente |",
            md,
        )
        self.assertIn("## Clientes nuevos — detalle completo (browse)\n\n", md)
        self.assertNotIn("\r", md)

    def test_normalize_inserts_blank_before_heading_and_table(self):
        broken = (
            "Intro sin blank.\n"
            "## Título pegado\n"
            "Párrafo.\n"
            "| A | B |\n"
            "| --- | --- |\n"
            "| 1 | 2 |\n"
            "### Otro título\n"
            "Fin."
        )
        fixed = normalize_markdown(broken)
        self.assertIn("Intro sin blank.\n\n## Título pegado\n\n", fixed)
        self.assertIn("Párrafo.\n\n| A | B |", fixed)
        self.assertIn("| 1 | 2 |\n\n### Otro título\n\nFin.", fixed)

    def test_pipe_and_newline_escaped_in_cells(self):
        table = md_table(["A"], [["x|y\nz"]])
        body_line = table.splitlines()[2]
        self.assertIn("x\\|y z", body_line)
        self.assertEqual(body_line, "| x\\|y z |")


class ReportGenerateTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="rep_tester", password="x", is_staff=True
        )

    def test_package_pgc_zip_or_files(self):
        name, content, ctype = generate_report_package(["pgc"])
        self.assertTrue(name.endswith(".zip") or name.endswith(".md") or name.endswith(".xlsx"))
        # pgc produces md+xlsx → zip
        self.assertTrue(name.endswith(".zip"))
        self.assertEqual(ctype, "application/zip")
        self.assertGreater(len(content), 50)

    def test_endpoint_requires_areas(self):
        self.client.force_login(self.user)
        url = reverse("reports:generate")
        resp = self.client.post(
            url, data='{"areas":[]}', content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

    def test_endpoint_generate_admin(self):
        self.client.force_login(self.user)
        url = reverse("reports:generate")
        resp = self.client.post(
            url, data='{"areas":["admin"]}', content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("attachment", resp.get("Content-Disposition", ""))
