"""Tests de ImportAuditEvent y despacho."""

from io import StringIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase

from core.wcg_models import DataImportBatch
from imports.audit import (
    audit_summary_counts,
    cli_import_audit,
    resolve_path_key_from_upload,
    suppress_import_audit,
)
from django.core.management.base import BaseCommand

from imports.dispatch import _audit_after_dispatch, run_import
from imports.management.import_audit_mixin import ImportAuditCommandMixin
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
    def test_command_detailed_runs(self):
        out = StringIO()
        call_command("audit_import_status", "--detailed", stdout=out)
        self.assertIn("ImportAuditEvent", out.getvalue())

    def test_audit_summary_empty(self):
        summary = audit_summary_counts()
        self.assertEqual(summary["total"], 0)
        self.assertEqual(summary["fail"], 0)


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