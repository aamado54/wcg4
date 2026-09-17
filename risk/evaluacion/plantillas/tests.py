"""Tests del consolidador de plantillas."""

from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

from risk.evaluacion import load_evaluacion
from risk.evaluacion.plantillas import consolidate_templates


class PlantillasConsolidateTests(SimpleTestCase):
    def test_consolidate_ejemplos_produces_loadable_workbook(self):
        root = Path(settings.BASE_DIR).parent
        source = root / "data" / "now" / "plantillas" / "ejemplos"
        reference = root / "data" / "now" / "WCG-evaluacion-riesgo-clientes-2025.xlsx"
        if not source.is_dir():
            self.skipTest("Sin directorio de ejemplos")
        out = root / "data" / "now" / "_test_evaluacion_plantillas.xlsx"
        ref = reference if reference.is_file() else None

        result = consolidate_templates(source, out, reference_workbook=ref)
        self.assertGreater(result.files_processed, 0)
        self.assertTrue(out.is_file())

        ds = load_evaluacion(path=out)
        self.assertIn(ds.status, ("ok", "partial"))
        self.assertGreater(len(ds.companies), 0)
        self.assertTrue(any(c.periods for c in ds.companies))
        self.assertTrue(
            any(p.z_label for c in ds.companies for p in c.periods),
            "Se esperaban calificaciones Z (Bien/Soso/Mal)",
        )

        lu3 = next((c for c in ds.companies if "AMERICAN_MEDICAL" in c.code), None)
        if lu3:
            p2024 = next((p for p in lu3.periods if p.year == 2024), None)
            if p2024:
                z = p2024.z_scores.get("z_emergentes")
                self.assertIsNotNone(z)
                self.assertAlmostEqual(z, 1.329, places=2)
                self.assertEqual(p2024.z_label, "Soso")

        out.unlink(missing_ok=True)
