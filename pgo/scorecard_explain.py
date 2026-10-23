"""Textos de ayuda por fila del tablero PGO (Info verde / amarillo / rojo)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pgo.scorecard_catalog import PgoConcept, UNE_CODES, UNE_LABELS, all_concepts, table_by_id
from pgo.scorecard_engine import ScoreGrid

InfoLevel = Literal["green", "yellow", "red"]


@dataclass
class RowInfo:
    level: InfoLevel
    body: str


_STATIC_MISSING: dict[str, tuple[str, str]] = {
    "legal_garantias_100": (
        "Falta integración con Planner WCG Créditos (Power App) o registro de garantías mobiliarias por operación.",
        "Necesitamos: definir fuente (export Planner / SharePoint) y regla «100% operaciones formalizadas el mismo día de firma».",
    ),
    "legal_tiempos_garantias_3d": (
        "Solo cuentan casos en Planner; no hay esos datos en WCG.",
        "Necesitamos: export con fecha firma vs fecha registro y contador de días hábiles ≤ 3.",
    ),
    "legal_titulos_inversion": (
        "Sin trazabilidad de emisión de títulos/contratos AP/PG en ≤ 2 días hábiles.",
        "Necesitamos: fuente legal/operativa por operación Investment.",
    ),
    "legal_contratos_acreedores_15d": (
        "Sin calendario de vencimiento de líneas de crédito ni evidencia de formalización 15 días antes.",
        "Necesitamos: maestro de líneas y fechas de renovación.",
    ),
    "legal_actas_comite": (
        "Sin registro de fechas de Comité de Créditos ni gestión de actas.",
        "Necesitamos: calendario de comités y confirmación de firma día hábil siguiente.",
    ),
    "fr_analisis_10d": (
        "Análisis de casos en Planner (10 días hábiles) no está en BD.",
        "Necesitamos: mismo export WCG Créditos con fecha ingreso vs fecha análisis.",
    ),
    "fr_valuacion_cartera": (
        "Plan de valuación anual y dictámenes no están modelados.",
        "Necesitamos: checklist de valuación Factoring/Leasing por año.",
    ),
    "fr_info_acreedores_3m": (
        "Sin alertas de vencimiento de líneas ni envío a acreedores 3 meses antes.",
        "Necesitamos: fechas de vencimiento y registro de envíos.",
    ),
    "op_cronograma_proyectos": (
        "Cronograma estratégico acordado con CEO no está en el sistema.",
        "Necesitamos: hitos por proyecto y % cumplimiento mensual.",
    ),
    "op_pago_freelances_7": (
        "Sin registro de pagos a freelances ni fecha de corte día 7.",
        "Necesitamos: nómina/comisiones freelances por mes.",
    ),
    "op_dashboard_jueves": (
        "Actualización de dashboard Teams y disponibilidades no se audita en WCG.",
        "Necesitamos: evidencia semanal (log o checklist).",
    ),
    "op_gastos_admin_10": (
        "Consolidación y pago gastos administrativos día 10 no está integrado.",
        "Necesitamos: cierre tesorería/contabilidad por mes.",
    ),
    "ti_cronograma_proyectos": (
        "Cronograma TI (Faktorlab, extracto, etc.) no está en BD.",
        "Necesitamos: hitos TI vs CEO.",
    ),
    "ti_encuesta_80": (
        "Encuesta de atención helpdesk no está cargada.",
        "Necesitamos: promedio mensual de encuesta ≥ 80 puntos.",
    ),
}


def _months_with_scores(grid: ScoreGrid, year: int, concept_id: str, une: str) -> list[int]:
    out = []
    for m in range(1, 13):
        cell = grid.get(year, m, une, concept_id)
        if cell.points is not None:
            out.append(m)
    return out


def _confidence_level(grid: ScoreGrid, year: int, concept_id: str, une: str) -> InfoLevel:
    highs = lows = nones = 0
    for m in range(1, 13):
        c = grid.get(year, m, une, concept_id)
        if c.confidence == "high":
            highs += 1
        elif c.confidence == "low":
            lows += 1
        elif c.confidence == "none":
            nones += 1
    if highs and not lows and not nones:
        return "green"
    if highs and not lows:
        return "green"
    if lows or highs:
        return "yellow"
    return "red"


def explain_concept_row(
    concept: PgoConcept,
    year: int,
    grid: ScoreGrid,
    une: str | None = None,
) -> RowInfo:
    """Explicación para una fila (opcionalmente acotada a una UNE)."""
    unes = [une] if une else [u for u in UNE_CODES if u in concept.max_points]
    if not unes:
        return RowInfo("red", "Este concepto no aplica a ninguna UNE seleccionada.")

    levels = [_confidence_level(grid, year, concept.id, u) for u in unes]
    if all(l == "red" for l in levels):
        level = "red"
    elif all(l == "green" for l in levels):
        level = "green"
    else:
        level = "yellow"

    parts: list[str] = []
    cid = concept.id

    if level == "yellow":
        doubts = _doubts_for(concept.id)
        if doubts:
            parts.append("DUDAS:\n" + doubts)

    if cid in _STATIC_MISSING and level == "red":
        what, need = _STATIC_MISSING[cid]
        parts.append(f"No se puede calcular de forma confiable.\n\nQué falta: {need}\n\nDetalle: {what}")
        return RowInfo(level, "\n\n".join(parts))

    if cid == "fr_eeff_integraciones":
        parts.append(_explain_eeff(year, grid, unes, concept.id))
    elif cid == "fr_carga_analitica":
        parts.append(_explain_carga_analitica(year, grid, unes, concept.id))
    elif cid in ("op_reportes_pgc_pgo_7", "ti_reportes_7"):
        parts.append(_explain_reportes_proxy(year, grid, unes, concept.id))
    elif cid == "ti_max_5_tickets":
        parts.append(_explain_tickets(year, grid, unes))
    elif cid == "ti_backup_nas":
        parts.append(_explain_backup(year))
    elif level == "red":
        static = _STATIC_MISSING.get(cid)
        if static:
            parts.append(f"No automatizado.\n\nQué falta: {static[1]}\n\n{static[0]}")
        else:
            parts.append("Sin reglas ni datos en WCG para este indicador.")
    else:
        sample_months = _months_with_scores(grid, year, concept.id, unes[0])
        parts.append(
            f"Cálculo automático parcial para {year}. "
            f"Meses con puntaje en {UNE_LABELS.get(unes[0], unes[0])}: "
            f"{', '.join(str(m) for m in sample_months) or 'ninguno'}."
        )

    if level == "green":
        parts.insert(0, "Cálculo confiable con la fuente indicada abajo.")
    elif level == "yellow" and not parts[0].startswith("DUDAS"):
        parts.insert(0, "Hay datos pero el cálculo es aproximado o incompleto.")

    return RowInfo(level, "\n\n".join(parts))


def explain_total_row(table_id: str, year: int, grid: ScoreGrid, une: str) -> RowInfo:
    table = table_by_id(table_id)
    if not table:
        return RowInfo("red", "Tabla no encontrada.")
    levels = []
    for c in table.concepts:
        if une in c.max_points:
            levels.append(_confidence_level(grid, year, c.id, une))
    if not levels or all(l == "red" for l in levels):
        return RowInfo(
            "red",
            "No se puede totalizar: ningún concepto de esta tabla tiene puntaje automático "
            f"para {UNE_LABELS.get(une, une)} en {year}.",
        )
    if all(l == "green" for l in levels):
        lvl = "green"
    elif any(l == "green" for l in levels) or any(l == "yellow" for l in levels):
        lvl = "yellow"
    else:
        lvl = "red"
    body = (
        f"Suma de los conceptos de «{table.title}» para {UNE_LABELS.get(une, une)}. "
        "Solo entran meses donde cada concepto tiene valor; los conceptos sin fuente quedan en — "
        "y no suman al total."
    )
    if lvl == "yellow":
        body = "DUDAS:\nEl total mezcla conceptos calculados y conceptos sin dato; no equivale al dictamen PGO oficial.\n\n" + body
    return RowInfo(lvl, body)


def _doubts_for(concept_id: str) -> str:
    return {
        "fr_carga_analitica": (
            "• Mezclamos EEFF gerencial, ingresos PGC e inversiones AP/PG sin validar fecha «antes del 7».\n"
            "• Investment/Insurance usan reglas distintas a Factoring/Leasing."
        ),
        "op_reportes_pgc_pgo_7": (
            "• No comprobamos carpeta SharePoint ni entrega el día 7.\n"
            "• Inferimos solo por presencia de EEFF en seed e imports del mes."
        ),
        "ti_reportes_7": (
            "• Mismo proxy que operaciones; no distingue reportes analítica vs PGC."
        ),
        "ti_max_5_tickets": (
            "• El helpdesk no trae UNE PGO: repetimos el mismo conteo en las 4 columnas.\n"
            "• Usamos horas de calendario, no horas hábiles del reporte TI.\n"
            "• Sin importar Tickets-YYYY-MM.xlsx la BD puede estar vacía o desactualizada."
        ),
        "ti_backup_nas": (
            "• Asumimos cumplido en mar/jun/sep/dic sin log de backup NAS."
        ),
    }.get(concept_id, "")


def _explain_eeff(year: int, grid: ScoreGrid, unes: list[str], concept_id: str) -> str:
    lines = [
        "Cómo se calcula: si en el seed gerencial (risk/financiero/combined_full) existe el mes "
        "YYYY-MM con KPI de la BU (F/L/I/S), se otorgan los puntos máximos del concepto; si no, 0.",
        f"Año {year}:",
    ]
    from pgo.scorecard_engine import _BU_MAP

    for u in unes:
        bu = _BU_MAP.get(u, "?")
        ms = _months_with_scores(grid, year, concept_id, u)
        lines.append(f"  • {UNE_LABELS.get(u, u)}: meses con dato → {ms or 'ninguno'}")
    return "\n".join(lines)


def _explain_carga_analitica(year: int, grid: ScoreGrid, unes: list[str], concept_id: str) -> str:
    return (
        "Cómo se calcula (proxy): Factoring/Leasing requieren EEFF del mes + fila INGRESOS PGC; "
        "Investment/Insurance aceptan EEFF o filas de inversiones AP/PG importadas. "
        "No valida carga «antes del 7» ni carpetas SharePoint.\n"
        + _explain_eeff(year, grid, unes, concept_id)
    )


def _explain_reportes_proxy(year: int, grid: ScoreGrid, unes: list[str], concept_id: str) -> str:
    return (
        "Cómo se calcula (proxy): mes con período en seed EEFF y/o FileUpload de clientes, "
        "inversiones o financieros en imports. No sustituye checklist real de reportes PGC/PGO."
    )


def _explain_tickets(year: int, grid: ScoreGrid, unes: list[str]) -> str:
    from pgo.models import Ticket

    if not Ticket.objects.exists():
        return (
            "No hay tickets en la base de datos.\n\n"
            "Qué falta: importar el Excel mensual (ej. Tickets-2026-09.xlsx) vía hub PGO."
        )
    return (
        "Cómo se calcula: al cierre de cada mes se cuentan tickets con apertura ≤ fin de mes y "
        "sin cierre o cierre posterior. Si el conteo ≤ 5 → puntos completos; si > 5 → 0. "
        "Mismo conteo para todas las UNE (limitación del dato)."
    )


def _explain_backup(year: int) -> str:
    return (
        "Cómo se calcula (placeholder): puntos completos en marzo, junio, septiembre y diciembre; "
        "0 en otros meses. No hay verificación de backup NAS en el sistema."
    )


def concept_by_id(concept_id: str) -> PgoConcept | None:
    for c in all_concepts():
        if c.id == concept_id:
            return c
    return None
