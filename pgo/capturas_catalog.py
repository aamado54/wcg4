"""Catálogo de tipos de captura manual PGO (índice y metadatos UI)."""

from __future__ import annotations

from dataclasses import dataclass

from pgo.scorecard_catalog import CONCEPT_SHORT_LABELS


@dataclass(frozen=True)
class CapturaType:
    slug: str
    concept_ids: tuple[str, ...]
    area: str  # legal | finanzas | operaciones | tecnologia
    title: str
    description: str
    implemented: bool = True
    pending_note: str = ""


AREA_LABELS = {
    "legal": "Legal",
    "finanzas": "Finanzas",
    "operaciones": "Operaciones",
    "tecnologia": "Tecnología",
}

AREA_ORDER = ("legal", "finanzas", "operaciones", "tecnologia")


CAPTURA_TYPES: tuple[CapturaType, ...] = (
    CapturaType(
        slug="legal_garantias_registro",
        concept_ids=("legal_garantias_100", "legal_tiempos_garantias_3d"),
        area="legal",
        title="Registro Garantías Mobiliarias",
        description=(
            "Captura por operación (Factoraje/Leasing): UNE, ID operación, "
            "fechas primarias; campos opcionales planner / mismo día."
        ),
    ),
    CapturaType(
        slug="legal_contratos_acreedores_15d",
        concept_ids=("legal_contratos_acreedores_15d",),
        area="legal",
        title="Contratos con acreedores (−15 días)",
        description="Líneas de crédito: acreedor, vencimiento, formalización; días anticipación opcional.",
    ),
    CapturaType(
        slug="legal_titulos_inversion",
        concept_ids=("legal_titulos_inversion",),
        area="legal",
        title="Títulos y contratos inversiones",
        description="Valor por defecto 100% desde sistemas; sin captura manual.",
        implemented=True,
    ),
    CapturaType(
        slug="legal_actas_comite",
        concept_ids=("legal_actas_comite",),
        area="legal",
        title="Actas Comité de Créditos",
        description="Pendiente: archivo provisto por Sergio.",
        implemented=False,
        pending_note="Sergio — solo archivo",
    ),
    CapturaType(
        slug="fr_analisis_10d",
        concept_ids=("fr_analisis_10d",),
        area="finanzas",
        title="Análisis casos ≤10 días hábiles",
        description="Pendiente definición Cindi.",
        implemented=False,
        pending_note="Cindi",
    ),
    CapturaType(
        slug="fr_valuacion_cartera",
        concept_ids=("fr_valuacion_cartera",),
        area="finanzas",
        title="Plan valuación anual cartera",
        description="Pendiente definición Cindi.",
        implemented=False,
        pending_note="Cindi",
    ),
    CapturaType(
        slug="fr_info_acreedores_3m",
        concept_ids=("fr_info_acreedores_3m",),
        area="finanzas",
        title="Información acreedores −3 meses",
        description="Pendiente definición Cindi.",
        implemented=False,
        pending_note="Cindi",
    ),
    CapturaType(
        slug="op_cronograma_proyectos",
        concept_ids=("op_cronograma_proyectos",),
        area="operaciones",
        title="Cronograma proyectos estratégicos",
        description="Por mes: cumplimiento del cronograma por UNE (José).",
    ),
    CapturaType(
        slug="op_reportes_pgc_pgo_7",
        concept_ids=("op_reportes_pgc_pgo_7",),
        area="operaciones",
        title="Reportes PGC/PGO día 7",
        description="Seis reportes del día 7: fecha primaria de cumplimiento; sugerencia opcional desde ArchivosPGO.",
    ),
    CapturaType(
        slug="op_pago_freelances_7",
        concept_ids=("op_pago_freelances_7",),
        area="operaciones",
        title="Pago freelances día 7",
        description="Pendiente definición Sergio.",
        implemented=False,
        pending_note="Sergio",
    ),
    CapturaType(
        slug="op_dashboard_jueves",
        concept_ids=("op_dashboard_jueves",),
        area="operaciones",
        title="Dashboard operaciones (jueves)",
        description="Pendiente definición Sergio.",
        implemented=False,
        pending_note="Sergio",
    ),
    CapturaType(
        slug="op_gastos_admin_10",
        concept_ids=("op_gastos_admin_10",),
        area="operaciones",
        title="Gastos administrativos día 10",
        description="Pendiente definición Sergio.",
        implemented=False,
        pending_note="Sergio",
    ),
    CapturaType(
        slug="ti_cronograma_proyectos",
        concept_ids=("ti_cronograma_proyectos",),
        area="tecnologia",
        title="Cronograma proyectos TI",
        description="Avance por UNE: 0%, 25%, 50%, 75% o 100%.",
    ),
    CapturaType(
        slug="ti_backup_nas",
        concept_ids=("ti_backup_nas",),
        area="tecnologia",
        title="Backup NAS trimestral",
        description="Checklist trimestral: implementación áreas y respaldo NAS.",
    ),
)

CAPTURA_BY_SLUG = {c.slug: c for c in CAPTURA_TYPES}

PENDING_FOOTNOTES: dict[str, str] = {
    "Cindi": "Conceptos en espera de especificación con Cindi (Finanzas y Riesgos).",
    "Sergio": "Conceptos en espera de especificación o archivo con Sergio (Operaciones / Legal actas).",
}


def captura_type_or_404(slug: str) -> CapturaType | None:
    return CAPTURA_BY_SLUG.get(slug)


def index_by_area() -> list[tuple[str, str, list[CapturaType]]]:
    buckets: dict[str, list[CapturaType]] = {a: [] for a in AREA_ORDER}
    for c in CAPTURA_TYPES:
        buckets[c.area].append(c)
    return [(a, AREA_LABELS[a], buckets[a]) for a in AREA_ORDER]


def concept_labels_for(c: CapturaType) -> str:
    parts = [CONCEPT_SHORT_LABELS.get(cid, cid) for cid in c.concept_ids]
    return " · ".join(parts)
