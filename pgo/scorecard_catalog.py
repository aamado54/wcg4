"""Catálogo de tablas y conceptos PGO (fuente: data/ref/PGO-.md)."""

from __future__ import annotations

from dataclasses import dataclass, field

UNE_CODES = ("FACTORING", "LEASING", "INVESTMENT", "INSURANCE")
UNE_LABELS = {
    "FACTORING": "Factoraje",
    "LEASING": "Leasing",
    "INVESTMENT": "Investment",
    "INSURANCE": "Insurance",
}


@dataclass(frozen=True)
class PgoConcept:
    id: str
    table_id: str
    category: str
    label: str
    max_points: dict[str, int]  # UNE code -> max; omit = N/A


@dataclass(frozen=True)
class PgoTable:
    id: str
    title: str
    area_weights: dict[str, str]  # UNE -> peso texto (ej. 33.30%)
    concepts: tuple[PgoConcept, ...] = field(default_factory=tuple)


def _c(cid: str, tid: str, cat: str, label: str, **pts: int) -> PgoConcept:
    return PgoConcept(id=cid, table_id=tid, category=cat, label=label, max_points=dict(pts))


PGO_TABLES: tuple[PgoTable, ...] = (
    PgoTable(
        id="legal",
        title="PGO Legal",
        area_weights={"FACTORING": "33.30%", "LEASING": "33.30%", "INVESTMENT": "33.30%"},
        concepts=(
            _c(
                "legal_garantias_100",
                "legal",
                "EFICIENCIA FINANCIERA",
                "Registro de garantía mobiliarias del 100% de las operaciones formalizadas",
                FACTORING=10,
                LEASING=10,
            ),
            _c(
                "legal_tiempos_garantias_3d",
                "legal",
                "AGILIDAD OPERATIVA",
                "Cumplimiento tiempos formalización y registro garantías mobiliarias (3 días hábiles)",
                FACTORING=65,
                LEASING=65,
            ),
            _c(
                "legal_titulos_inversion",
                "legal",
                "AGILIDAD OPERATIVA",
                "Emisión de títulos y contratos del 100% de las inversiones y préstamos",
                INVESTMENT=100,
            ),
            _c(
                "legal_contratos_acreedores_15d",
                "legal",
                "AGILIDAD OPERATIVA",
                "Formalizar contratos con acreedores de líneas de crédito 15 días calendario antes del vencimiento",
                FACTORING=20,
                LEASING=20,
            ),
            _c(
                "legal_actas_comite",
                "legal",
                "AGILIDAD OPERATIVA",
                "Elaboración y gestión de firmas de actas el día hábil siguiente al Comité de Créditos",
                FACTORING=5,
                LEASING=5,
            ),
        ),
    ),
    PgoTable(
        id="finanzas",
        title="PGO Finanzas y Riesgos",
        area_weights={
            "FACTORING": "50%",
            "LEASING": "30%",
            "INVESTMENT": "15%",
            "INSURANCE": "5%",
        },
        concepts=(
            _c(
                "fr_analisis_10d",
                "finanzas",
                "EFICIENCIA FINANCIERA",
                "Análisis del 100% de los casos ingresados en 10 días hábiles",
                FACTORING=30,
                LEASING=30,
            ),
            _c(
                "fr_valuacion_cartera",
                "finanzas",
                "EFICIENCIA FINANCIERA",
                "Cumplimiento del 100% de plan de valuación anual de cartera",
                FACTORING=40,
                LEASING=40,
            ),
            _c(
                "fr_carga_analitica",
                "finanzas",
                "EFICIENCIA FINANCIERA",
                "Carga mensual de datos para analítica (EEFF cartera, ingresos y pagos por UNE)",
                FACTORING=10,
                LEASING=10,
                INVESTMENT=50,
                INSURANCE=50,
            ),
            _c(
                "fr_info_acreedores_3m",
                "finanzas",
                "EFICIENCIA FINANCIERA",
                "Información a acreedores de líneas de crédito 3 meses antes del vencimiento",
                FACTORING=10,
                LEASING=10,
            ),
            _c(
                "fr_eeff_integraciones",
                "finanzas",
                "AGILIDAD OPERATIVA",
                "EEFF con integraciones cargados mensualmente en carpeta correspondiente",
                FACTORING=10,
                LEASING=10,
                INVESTMENT=50,
                INSURANCE=50,
            ),
        ),
    ),
    PgoTable(
        id="operaciones",
        title="PGO Operaciones",
        area_weights={u: "25.00%" for u in UNE_CODES},
        concepts=(
            _c(
                "op_cronograma_proyectos",
                "operaciones",
                "AGILIDAD OPERATIVA",
                "Cumplimiento del cronograma de proyectos estratégicos",
                FACTORING=55,
                LEASING=55,
                INVESTMENT=55,
                INSURANCE=55,
            ),
            _c(
                "op_pago_freelances_7",
                "operaciones",
                "AGILIDAD OPERATIVA",
                "Pago de comisiones al 100% a freelances, el 7 de cada mes",
                FACTORING=10,
                LEASING=10,
                INVESTMENT=10,
                INSURANCE=10,
            ),
            _c(
                "op_dashboard_jueves",
                "operaciones",
                "AGILIDAD OPERATIVA",
                "Actualización Dashboard operaciones (jueves) y disponibilidades en tiempo real",
                FACTORING=10,
                LEASING=10,
                INVESTMENT=10,
                INSURANCE=10,
            ),
            _c(
                "op_reportes_pgc_pgo_7",
                "operaciones",
                "AGILIDAD OPERATIVA",
                "Reportes requeridos para PGC y PGO el 7 de cada mes",
                FACTORING=10,
                LEASING=10,
                INVESTMENT=10,
                INSURANCE=10,
            ),
            _c(
                "op_gastos_admin_10",
                "operaciones",
                "EFICIENCIA FINANCIERA",
                "Consolidación y pago de gastos administrativos el 10 de cada mes",
                FACTORING=5,
                LEASING=5,
                INVESTMENT=5,
                INSURANCE=5,
            ),
        ),
    ),
    PgoTable(
        id="tecnologia",
        title="PGO Tecnología",
        area_weights={u: "25%" for u in UNE_CODES},
        concepts=(
            _c(
                "ti_reportes_7",
                "tecnologia",
                "AGILIDAD OPERATIVA",
                "Reportes analítica / PGC / PGO el 7 de cada mes",
                FACTORING=10,
                LEASING=10,
                INVESTMENT=10,
                INSURANCE=10,
            ),
            _c(
                "ti_max_5_tickets",
                "tecnologia",
                "AGILIDAD OPERATIVA",
                "Máximo 5 ticketes abiertos de gestiones de los cores (SIFCO, SISEG, ERP, etc.)",
                FACTORING=20,
                LEASING=20,
                INVESTMENT=20,
                INSURANCE=20,
            ),
            _c(
                "ti_cronograma_proyectos",
                "tecnologia",
                "AGILIDAD OPERATIVA",
                "Cumplimiento cronogramas de proyectos e implementación (CEO)",
                FACTORING=50,
                LEASING=50,
                INVESTMENT=50,
                INSURANCE=50,
            ),
            _c(
                "ti_encuesta_80",
                "tecnologia",
                "EXPERTOS EN EL CLIENTE",
                "Encuesta de atención (promedio superior a 80 puntos)",
                FACTORING=10,
                LEASING=10,
                INVESTMENT=10,
                INSURANCE=10,
            ),
            _c(
                "ti_backup_nas",
                "tecnologia",
                "EXPERTOS EN EL CLIENTE",
                "Implementación áreas y backup NAS cada trimestre natural",
                FACTORING=10,
                LEASING=10,
                INVESTMENT=10,
                INSURANCE=10,
            ),
        ),
    ),
)


def all_concepts() -> list[PgoConcept]:
    out: list[PgoConcept] = []
    for table in PGO_TABLES:
        out.extend(table.concepts)
    return out


def table_by_id(table_id: str) -> PgoTable | None:
    for t in PGO_TABLES:
        if t.id == table_id:
            return t
    return None


CONCEPT_SHORT_LABELS: dict[str, str] = {
    "legal_garantias_100": "Garantías mobiliarias 100%",
    "legal_tiempos_garantias_3d": "Formalización garantías ≤3 días",
    "legal_titulos_inversion": "Títulos y contratos inversiones",
    "legal_contratos_acreedores_15d": "Contratos acreedores −15 días",
    "legal_actas_comite": "Actas post Comité de Créditos",
    "fr_analisis_10d": "Análisis casos ≤10 días hábiles",
    "fr_valuacion_cartera": "Plan valuación anual cartera",
    "fr_carga_analitica": "Carga datos analítica mensual",
    "fr_info_acreedores_3m": "Info acreedores −3 meses",
    "fr_eeff_integraciones": "EEFF con integraciones",
    "op_cronograma_proyectos": "Cronograma proyectos estratégicos",
    "op_pago_freelances_7": "Pago freelances día 7",
    "op_dashboard_jueves": "Dashboard operaciones (jueves)",
    "op_reportes_pgc_pgo_7": "Reportes PGC/PGO día 7",
    "op_gastos_admin_10": "Gastos administrativos día 10",
    "ti_reportes_7": "Reportes analítica/PGC/PGO",
    "ti_max_5_tickets": "Máx. 5 tickets cores abiertos",
    "ti_cronograma_proyectos": "Cronograma proyectos TI",
    "ti_encuesta_80": "Encuesta atención ≥80 pts",
    "ti_backup_nas": "Backup NAS trimestral",
}


def concept_short_label(concept: PgoConcept) -> str:
    return CONCEPT_SHORT_LABELS.get(concept.id, concept.label[:40])
