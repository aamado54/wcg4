"""Tests de autodetección de importaciones (3 capas)."""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

from imports.detection import (
    TYPE_CRM_CLIENTES,
    TYPE_PGO_TICKETS,
    detect_from_columns,
    detect_from_name,
    detect_file,
    _merge_detections,
)


class DetectionNameTests(SimpleTestCase):
    def test_clientes_nuevos_by_name(self):
        r = detect_from_name("ClientesNuevos_2024-03.xlsx")
        self.assertIsNotNone(r)
        self.assertEqual(r.tipo, "new_clients")
        self.assertGreaterEqual(r.confidence, 0.8)

    def test_crm_infoclientes_by_name(self):
        r = detect_from_name("InfoClientes_WCG.xlsx")
        self.assertEqual(r.tipo, TYPE_CRM_CLIENTES)


class DetectionStructureTests(SimpleTestCase):
    def test_pgo_columns(self):
        r = detect_from_columns({"id", "titulo", "estado", "fecha_apertura"})
        self.assertIsNotNone(r)
        self.assertEqual(r.tipo, TYPE_PGO_TICKETS)


class DetectionMergeTests(SimpleTestCase):
    def test_agreement_high_confidence(self):
        by_name = detect_from_name("crm_clientes.xlsx")
        by_cols = detect_from_columns({"nit", "nombre_cliente", "wcf"})
        merged = _merge_detections(by_name, by_cols, None)
        self.assertEqual(merged.tipo, TYPE_CRM_CLIENTES)
        self.assertTrue(merged.can_auto_import)

    def test_conflict_is_ambiguous(self):
        by_name = detect_from_name("pgo_tickets_control.xlsx")
        by_cols = detect_from_columns({"nit", "nombre", "wcf"})
        merged = _merge_detections(by_name, by_cols, None)
        self.assertTrue(merged.ambiguous)
        self.assertFalse(merged.can_auto_import)


class DetectionFileTests(SimpleTestCase):
    def test_csv_crm_detect(self):
        content = b"NIT,NombreCliente,WCF\n123456789,Acme,1\n987654321,Beta,0\n111222333,Gamma,1\n"
        f = SimpleUploadedFile("InfoClientes.csv", content, content_type="text/csv")
        result = detect_file(f)
        self.assertEqual(result.tipo, TYPE_CRM_CLIENTES)
        self.assertTrue(result.can_auto_import)
        self.assertTrue(any("CRM" in r or "NIT" in r or "nit" in r for r in result.reasons) or "combinada" in result.layer)
