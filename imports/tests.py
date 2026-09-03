"""Tests de autodetección de importaciones (3 capas)."""

from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase

from imports.detection import (
    TYPE_BANK_LOANS,
    TYPE_CRM_CLIENTES,
    TYPE_INVESTMENT_GROWTH,
    TYPE_PGO_TICKETS,
    detect_file,
    detect_from_name,
    detect_from_columns,
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

    def test_inversiones_crecimiento_by_name(self):
        r = detect_from_name("Inversiones_crecimiento_2026.csv")
        self.assertEqual(r.tipo, TYPE_INVESTMENT_GROWTH)

    def test_bancos_fin_mes_by_name(self):
        r = detect_from_name("Bancos_Fin_de_mes.xlsx")
        self.assertEqual(r.tipo, TYPE_BANK_LOANS)


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

    def test_csv_inversiones_crecimiento_detect(self):
        header = (
            "Cierre;instrumento;empresa;numero_inversion;moneda_inversion;monto_inversion;"
            "Inicio;Vencimiento;TipoCambio;Quetzalizado;Dolarizado\n"
        )
        row = "2026/07;AP;INVESTMENT - WC FACTORING;AP01220305;GTQ;200000;2022-03-21;2025-03-26;7.66;200000;26094\n"
        f = SimpleUploadedFile(
            "Inversiones_crecimiento_2026-07.csv",
            (header + row).encode("utf-8"),
            content_type="text/csv",
        )
        result = detect_file(f)
        self.assertEqual(result.tipo, TYPE_INVESTMENT_GROWTH)
        self.assertTrue(result.can_auto_import)


class NewClientsRowParseTests(SimpleTestCase):
    def test_spaced_headers_and_rates(self):
        from imports.client_rates import parse_rate, rate_basis_for, row_get

        row = {
            " Nit": " 577806-9 ",
            " Moneda": "GTQ",
            "Monto": "1275666.33",
            "Porcentaje": "2",
            " UNE": "Leasing",
        }
        self.assertEqual(row_get(row, "Nit"), "577806-9")
        self.assertEqual(row_get(row, "Moneda"), "GTQ")
        self.assertEqual(row_get(row, "Monto"), "1275666.33")
        self.assertEqual(row_get(row, "UNE"), "Leasing")
        self.assertEqual(parse_rate("8.5"), Decimal("8.5"))
        self.assertEqual(rate_basis_for(None, "INVESTMENT - WC FACTORING"), "annual")
        self.assertEqual(rate_basis_for(None, "Leasing"), "monthly")
        self.assertEqual(rate_basis_for(None, "Factoraje"), "monthly")
        self.assertEqual(rate_basis_for(None, "inversiones"), "annual")
        self.assertEqual(row_get({"Cliente": '"MG RENTAL"'}, "Cliente"), "MG RENTAL")
