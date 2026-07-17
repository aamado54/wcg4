"""Autodetección de tipo de archivo para Importación General."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from core.services.column_map import _norm_header, normalize_columns
from core.services.import_base import ImportValidationError, read_dataframe


@dataclass
class DetectionResult:
    tipo: str
    confidence: float
    label: str
    reasons: list[str] = field(default_factory=list)
    suggestions: list[tuple[str, str]] = field(default_factory=list)


# Tipos canónicos del hub unificado
TYPE_CRM_CLIENTES = "crm_clientes"
TYPE_PGO_TICKETS = "pgo_tickets"
TYPE_PGO_CATALOGO = "pgo_catalogo"
TYPE_RISK_LEASING = "risk_leasing"
TYPE_RISK_RENTAS = "risk_rentas"
TYPE_NEW_CLIENTS = "new_clients"
TYPE_CROSS_SALE = "cross_sale"
TYPE_FINANCIAL = "financial"
TYPE_UNKNOWN = "unknown"

TYPE_LABELS = {
    TYPE_CRM_CLIENTES: "CRM — Clientes / entidades",
    TYPE_PGO_TICKETS: "PGO — Tickets helpdesk",
    TYPE_PGO_CATALOGO: "PGO — Catálogo de archivos (informativo)",
    TYPE_RISK_LEASING: "Balón de Riesgo — Base leasing / snapshots",
    TYPE_RISK_RENTAS: "Balón de Riesgo — Rentas / cuotas leasing",
    TYPE_NEW_CLIENTS: "PGC — Clientes nuevos",
    TYPE_CROSS_SALE: "PGC — Venta cruzada",
    TYPE_FINANCIAL: "PGC — Estado financiero (WC*)",
    TYPE_UNKNOWN: "Desconocido",
}

ALL_IMPORTABLE = [
    TYPE_CRM_CLIENTES,
    TYPE_PGO_TICKETS,
    TYPE_PGO_CATALOGO,
    TYPE_RISK_LEASING,
    TYPE_RISK_RENTAS,
    TYPE_NEW_CLIENTS,
    TYPE_CROSS_SALE,
]


def _score_columns(cols: set[str], required_groups: list[list[str]]) -> int:
    score = 0
    for group in required_groups:
        if any(_norm_header(g) in cols for g in group):
            score += 1
    return score


def detect_from_name(filename: str) -> DetectionResult | None:
    name = (filename or "").lower()
    compact = re.sub(r"[\s_\-.]+", "", name)

    checks = [
        (TYPE_NEW_CLIENTS, "clientesnuevos" in compact or "clientes_nuevos" in name, "nombre contiene ClientesNuevos"),
        (TYPE_CROSS_SALE, "ventacruzada" in compact, "nombre contiene VentaCruzada"),
        (TYPE_FINANCIAL, name.startswith("wc") or "estado_resultados" in name or "er_" in name, "patrón financiero WC*"),
        (TYPE_PGO_TICKETS, "pgo" in name and ("ticket" in name or "control" in name), "nombre PGO + tickets/control"),
        (TYPE_PGO_CATALOGO, "pgo" in name and "archivo" in name, "nombre PGO + archivos"),
        (TYPE_CRM_CLIENTES, "crm" in name or "infoclientes" in compact, "nombre CRM / InfoClientes"),
        (TYPE_RISK_RENTAS, "rentas" in name and "leasing" in name, "LeasingRentas"),
        (TYPE_RISK_LEASING, "baseleasing" in compact or ("balon" in name and "leasing" in name) or ("leasing" in name and "base" in name), "BaseLeasing / balón"),
    ]
    for tipo, matched, reason in checks:
        if matched:
            return DetectionResult(
                tipo=tipo,
                confidence=0.85,
                label=TYPE_LABELS[tipo],
                reasons=[reason],
            )
    return None


def detect_from_columns(cols: set[str]) -> DetectionResult | None:
    candidates: list[tuple[str, int, list[str]]] = []

    crm_score = _score_columns(
        cols,
        [["nit"], ["nombre", "nombre_cliente", "cliente", "razon_social"], ["wcf", "wcl", "wci"]],
    )
    if crm_score >= 2:
        candidates.append((TYPE_CRM_CLIENTES, crm_score, ["columnas NIT/NombreCliente/WCF|WCL|WCI"]))

    pgo_score = _score_columns(
        cols,
        [["id", "codigo", "ticket"], ["titulo", "asunto"], ["estado"], ["fecha_apertura", "usuario_solicita"]],
    )
    if pgo_score >= 3:
        candidates.append((TYPE_PGO_TICKETS, pgo_score, ["columnas ID/Titulo/Estado helpdesk"]))

    catalog_score = _score_columns(cols, [["carpeta", "archivo"], ["creado_por", "creado_en"]])
    if catalog_score >= 2:
        candidates.append((TYPE_PGO_CATALOGO, catalog_score, ["columnas Carpeta/Archivo"]))

    leasing_score = _score_columns(
        cols,
        [
            ["contract_number", "contrato", "no_contrato"],
            ["client_name", "cliente", "nombre_cliente"],
            ["capital_balance", "saldo", "duedays", "due_days"],
        ],
    )
    if leasing_score >= 2:
        candidates.append((TYPE_RISK_LEASING, leasing_score, ["columnas Contract/Client/Balance leasing"]))

    rentas_score = _score_columns(
        cols,
        [["no_contrato", "contrato"], ["vencimiento"], ["valor_renta", "renta_total"], ["estado"]],
    )
    if rentas_score >= 3:
        candidates.append((TYPE_RISK_RENTAS, rentas_score, ["columnas NoContrato/Vencimiento/ValorRenta"]))

    nc_score = _score_columns(cols, [["une"], ["cliente", "nombre"], ["fecha", "mes"]])
    if "une" in cols and nc_score >= 2:
        candidates.append((TYPE_NEW_CLIENTS, nc_score, ["patrón clientes nuevos"]))

    if not candidates:
        return None
    candidates.sort(key=lambda x: x[1], reverse=True)
    tipo, score, reasons = candidates[0]
    conf = min(0.95, 0.55 + 0.1 * score)
    suggestions = [(t, TYPE_LABELS[t]) for t, _, _ in candidates[1:3]]
    return DetectionResult(
        tipo=tipo,
        confidence=conf,
        label=TYPE_LABELS[tipo],
        reasons=reasons,
        suggestions=suggestions,
    )


def detect_file(uploaded_file) -> DetectionResult:
    by_name = detect_from_name(getattr(uploaded_file, "name", "") or "")
    try:
        df = normalize_columns(read_dataframe(uploaded_file, sheet_name=None))
        uploaded_file.seek(0)
        cols = set(df.columns)
        by_cols = detect_from_columns(cols)
    except Exception as exc:
        uploaded_file.seek(0)
        if by_name and by_name.confidence >= 0.8:
            by_name.reasons.append(f"columnas no leídas ({exc})")
            return by_name
        return DetectionResult(
            tipo=TYPE_UNKNOWN,
            confidence=0.0,
            label=TYPE_LABELS[TYPE_UNKNOWN],
            reasons=[f"No se pudo leer el archivo: {exc}"],
            suggestions=[(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE[:5]],
        )

    if by_name and by_cols and by_name.tipo == by_cols.tipo:
        return DetectionResult(
            tipo=by_name.tipo,
            confidence=min(0.99, (by_name.confidence + by_cols.confidence) / 2 + 0.1),
            label=TYPE_LABELS[by_name.tipo],
            reasons=by_name.reasons + by_cols.reasons,
        )
    if by_cols and by_cols.confidence >= 0.75:
        if by_name and by_name.tipo != by_cols.tipo:
            by_cols.suggestions = [(by_name.tipo, TYPE_LABELS[by_name.tipo])] + by_cols.suggestions
            by_cols.reasons.append(f"nombre sugería {by_name.tipo}, columnas priorizadas")
        return by_cols
    if by_name:
        if by_cols and by_cols.tipo != by_name.tipo:
            by_name.suggestions = [(by_cols.tipo, TYPE_LABELS[by_cols.tipo])]
            by_name.confidence = min(by_name.confidence, 0.7)
        return by_name
    return DetectionResult(
        tipo=TYPE_UNKNOWN,
        confidence=0.0,
        label=TYPE_LABELS[TYPE_UNKNOWN],
        reasons=["No se pudo identificar el tipo con suficiente confianza"],
        suggestions=[(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE],
    )


def detect_path(path: str) -> DetectionResult:
    from pathlib import Path

    from django.core.files.uploadedfile import SimpleUploadedFile

    p = Path(path)
    f = SimpleUploadedFile(p.name, p.read_bytes())
    return detect_file(f)
