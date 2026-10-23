from datetime import date, datetime

from django.test import SimpleTestCase

from pgo.archivos_pgo_parse import parse_creado_en, parse_event_date_from_archivo
from pgo.archivos_sla import cumple_plazo
from pgo.archivos_sla import CONCEPT_SLA


class ArchivosPgoParseTests(SimpleTestCase):
    def test_fecha_en_nombre_dd_mm_yyyy(self):
        d = parse_event_date_from_archivo("MEMO-COMITE DE RIESGO-5.08.2026.pdf")
        self.assertEqual(d, date(2026, 8, 5))

    def test_creado_en_iso(self):
        dt = parse_creado_en("2026-08-06 16:48:58")
        self.assertEqual(dt, datetime(2026, 8, 6, 16, 48, 58))

    def test_actas_comite_ejemplo_fila_36(self):
        event = date(2026, 8, 5)
        creado = datetime(2026, 8, 6, 16, 48, 58)
        rule = CONCEPT_SLA["legal_actas_comite"]
        self.assertTrue(
            cumple_plazo(datetime.combine(event, datetime.min.time()), creado, rule)
        )

    def test_actas_comite_ejemplo_fila_41_falla(self):
        event = date(2026, 8, 11)
        creado = datetime(2026, 8, 13, 15, 54, 17)
        rule = CONCEPT_SLA["legal_actas_comite"]
        self.assertFalse(
            cumple_plazo(datetime.combine(event, datetime.min.time()), creado, rule)
        )
