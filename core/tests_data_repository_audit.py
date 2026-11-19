"""Tests de auditoría data/1-pgc … 5-plal (sin disco del repo)."""

from pathlib import Path

from django.test import SimpleTestCase

from core.services.data_repository_audit import (
    expected_tipo_from_name,
    find_duplicate_groups,
    iter_audit_files,
    folder_yymm_from_rel,
)
from core.services.data_repository_audit import AuditFileRow


class DataRepositoryAuditTests(SimpleTestCase):
    def test_expected_pgc_venta_cruzada(self):
        self.assertEqual(
            expected_tipo_from_name("VENTA_CRUZADA_PGC_import.csv", "pgc"),
            "cross_sale",
        )

    def test_folder_yymm(self):
        self.assertEqual(folder_yymm_from_rel(("1-pgc", "2610", "x.csv")), "2610")
        self.assertIsNone(folder_yymm_from_rel(("1-pgc", "otros", "x.csv")))

    def test_duplicate_group_flags_organizar(self):
        rows = [
            AuditFileRow(
                relpath="1-pgc/2610/a.csv",
                module_key="1-pgc",
                module_logical="pgc",
                folder_yymm="2610",
                import_tipo="cross_sale",
                tipo_label="",
                yymm="2610",
                yymm_source="token",
                expected_tipo="cross_sale",
            ),
            AuditFileRow(
                relpath="1-pgc/2610/b_other.csv",
                module_key="1-pgc",
                module_logical="pgc",
                folder_yymm="2610",
                import_tipo="cross_sale",
                tipo_label="",
                yymm="2610",
                yymm_source="token",
                expected_tipo="cross_sale",
            ),
        ]
        dupes = find_duplicate_groups(rows)
        self.assertEqual(len(dupes), 1)
        self.assertEqual(dupes[0]["note"], "organizar")

    def test_iter_audit_skips_ejemplo(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mod = root / "1-pgc" / "2601"
            mod.mkdir(parents=True)
            (mod / "real.csv").write_text("x", encoding="utf-8")
            (mod / "plantilla_ejemplo.csv").write_text("x", encoding="utf-8")
            rows = iter_audit_files(root)
            names = {Path(r.relpath).name for r in rows}
            self.assertIn("real.csv", names)
            self.assertNotIn("plantilla_ejemplo.csv", names)