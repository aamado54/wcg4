"""Tests de ImportAuditEvent y despacho."""

from io import StringIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse

from core.wcg_models import DataImportBatch
from imports.audit import (
    audit_summary_counts,
    cli_import_audit,
    record_import_audit_event,
    resolve_path_key_from_upload,
    suppress_import_audit,
)
from django.core.management.base import BaseCommand

from imports.dispatch import _audit_after_dispatch, run_import
from imports.management.import_audit_mixin import ImportAuditCommandMixin
from imports.audit_cli_registry import cli_audit_coverage_ratio
from imports.models import ImportAuditEvent

User = get_user_model()


class ImportAuditHelpersTests(TestCase):
    def test_resolve_path_key_data_import_batch(self):
        batch = DataImportBatch(
            modulo=DataImportBatch.MODULO_CRM,
            tipo_importacion="entidades",
            archivo_nombre="InfoClientes.csv",
        )
        key = resolve_path_key_from_upload(None, batch)
        self.assertEqual(key, "InfoClientes.csv")

    def test_resolve_path_key_uploaded_file_name(self):
        f = SimpleUploadedFile("demo.csv", b"a,b\n1,2\n")
        self.assertEqual(resolve_path_key_from_upload(f, None), "demo.csv")


class DispatchAuditTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="audituser", password="x")

    def test_run_import_ambiguous_records_fail_audit(self):
        f = SimpleUploadedFile(
            "ambiguo.csv",
            b"col1,col2\n1,2\n",
            content_type="text/csv",
        )
        result = run_import(self.user, f)
        self.assertFalse(result.ok)
        ev = ImportAuditEvent.objects.get()
        self.assertFalse(ev.success)
        self.assertEqual(ev.file_path_key, "ambiguo.csv")
        self.assertEqual(ev.source, ImportAuditEvent.SOURCE_MANUAL)
        self.assertEqual(ev.user, self.user)

    def test_audit_after_dispatch_crm_batch(self):
        from imports.detection import DetectionResult
        from imports.dispatch import DispatchResult

        batch = DataImportBatch(
            modulo=DataImportBatch.MODULO_CRM,
            tipo_importacion="entidades",
            archivo_nombre="InfoClientes.csv",
            status=DataImportBatch.STATUS_OK,
        )
        detection = DetectionResult(
            tipo="crm_clientes",
            confidence=0.9,
            label="CRM",
            layer="test",
        )
        result = DispatchResult(
            tipo="crm_clientes",
            label="CRM",
            detection=detection,
            batch=batch,
            ok=True,
        )
        _audit_after_dispatch(self.user, None, "", result, source="manual")
        ev = ImportAuditEvent.objects.get()
        self.assertTrue(ev.success)
        self.assertEqual(ev.file_path_key, "InfoClientes.csv")
        self.assertEqual(ev.detail_json.get("batch_status"), DataImportBatch.STATUS_OK)


class CliAuditMixinTests(TestCase):
    class _StubCommand(ImportAuditCommandMixin, BaseCommand):
        import_audit_tipo = "cross_sale"

        def add_arguments(self, parser):
            parser.add_argument("--path", type=str)

        def handle(self, *args, **options):
            return None

    def test_mixin_records_on_execute(self):
        with tempfile_named_csv() as path:
            cmd = self._StubCommand(stdout=StringIO(), stderr=StringIO())
            parser = cmd.create_parser("test", "stub")
            opts = parser.parse_args(["--path", str(path)])
            cmd.execute(**vars(opts))
        self.assertEqual(ImportAuditEvent.objects.count(), 1)
        ev = ImportAuditEvent.objects.get()
        self.assertTrue(ev.success)
        self.assertEqual(ev.import_tipo, "cross_sale")

    def test_suppress_avoids_duplicate_cli_audit(self):
        with tempfile_named_csv() as path:
            with suppress_import_audit():
                with cli_import_audit(path, "cross_sale"):
                    pass
        self.assertEqual(ImportAuditEvent.objects.count(), 0)

        with tempfile_named_csv() as path:
            with cli_import_audit(path, "cross_sale"):
                pass
        self.assertEqual(ImportAuditEvent.objects.count(), 1)


class AuditImportStatusCommandTests(TestCase):
    def test_cli_coverage_meets_threshold(self):
        with_mixin, total, pct = cli_audit_coverage_ratio()
        self.assertGreaterEqual(total, 10)
        self.assertGreaterEqual(pct, 80.0)
        self.assertGreaterEqual(with_mixin, 9)

    def test_command_coverage_runs(self):
        out = StringIO()
        call_command("audit_import_status", "--coverage", stdout=out)
        body = out.getvalue()
        self.assertIn("CLI import_* con mixin", body)
        self.assertIn("import_pgc_objetivos", body)

    def test_command_detailed_runs(self):
        out = StringIO()
        call_command("audit_import_status", "--detailed", stdout=out)
        self.assertIn("ImportAuditEvent", out.getvalue())

    def test_checklist_lists_failures(self):
        user = User.objects.create_user(username="clicheck", password="x")
        record_import_audit_event(
            user=user,
            file_path_key="/tmp/fail.csv",
            success=False,
            import_tipo="new_clients",
            error_message="parse error",
        )
        out = StringIO()
        call_command("audit_import_status", "--checklist", stdout=out)
        body = out.getvalue()
        self.assertIn("FAIL", body)
        self.assertIn("clicheck", body)
        self.assertIn("auditoria", body)

    def test_audit_summary_empty(self):
        summary = audit_summary_counts()
        self.assertEqual(summary["total"], 0)
        self.assertEqual(summary["fail"], 0)


class ImportAuditViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="auditview", password="x")
        self.client = Client()
        self.client.login(username="auditview", password="x")

    def test_list_requires_login(self):
        anon = Client()
        url = reverse("imports:import_audit_list")
        resp = anon.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_list_and_filter(self):
        record_import_audit_event(
            user=self.user,
            file_path_key="ok_file.csv",
            success=True,
            import_tipo="cross_sale",
        )
        record_import_audit_event(
            user=self.user,
            file_path_key="bad_file.csv",
            success=False,
            import_tipo="new_clients",
            error_message="broken",
        )
        url = reverse("imports:import_audit_list")
        resp = self.client.get(url, {"success": "fail"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "bad_file.csv")
        self.assertNotContains(resp, "ok_file.csv")

    def test_detail_page(self):
        ev = record_import_audit_event(
            user=self.user,
            file_path_key="detail.csv",
            success=True,
            import_tipo="financial",
            detail={"cli": True},
        )
        url = reverse("imports:import_audit_detail", kwargs={"event_id": ev.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "detail.csv")
        self.assertContains(resp, "cli")


class BackfillImportAuditCommandTests(TestCase):
    def test_backfill_dry_run_empty_db(self):
        User.objects.create_user(username="caa", password="x", is_staff=True)
        out = StringIO()
        call_command("backfill_import_audit_events", stdout=out)
        self.assertIn("Dry-run", out.getvalue())
        self.assertEqual(ImportAuditEvent.objects.count(), 0)


def tempfile_named_csv():
    import tempfile
    from pathlib import Path

    class _Ctx:
        def __enter__(self):
            self._tmp = tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False, encoding="utf-8"
            )
            self._tmp.write("a,b\n1,2\n")
            self._tmp.close()
            return Path(self._tmp.name)

        def __exit__(self, *args):
            Path(self._tmp.name).unlink(missing_ok=True)

    return _Ctx()