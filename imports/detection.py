"""Autodetección de tipo de archivo para Importación General.

Capas (en orden de evaluación, luego fusión):
1. Nombre del archivo
2. Estructura (columnas / encabezados / hojas)
3. Contenido de muestra (valores que desambiguan tipos parecidos)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from core.services.column_map import _norm_header, normalize_columns
from core.services.import_base import ImportValidationError, read_dataframe

CONFIDENCE_AUTO = 0.80


@dataclass
class DetectionResult:
    tipo: str
    confidence: float
    label: str
    reasons: list[str] = field(default_factory=list)
    suggestions: list[tuple[str, str]] = field(default_factory=list)
    layer: str = ""
    ambiguous: bool = False
    candidates: list[tuple[str, float, str]] = field(default_factory=list)

    @property
    def can_auto_import(self) -> bool:
        return (
            self.tipo != TYPE_UNKNOWN
            and not self.ambiguous
            and self.confidence >= CONFIDENCE_AUTO
        )

    @property
    def rule_summary(self) -> str:
        """Texto corto para bitácora."""
        parts = [
            f"tipo={self.tipo}",
            f"capa={self.layer or 'n/a'}",
            f"confianza={self.confidence:.0%}",
            f"auto={'sí' if self.can_auto_import else 'no'}",
        ]
        if self.reasons:
            parts.append("reglas=[" + "; ".join(self.reasons[:6]) + "]")
        if self.ambiguous:
            parts.append("ambiguo=sí")
        return " | ".join(parts)


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

IMPORTER_LABELS = {
    TYPE_CRM_CLIENTES: "crm.services.import_entidades",
    TYPE_PGO_TICKETS: "pgo.services.import_tickets",
    TYPE_PGO_CATALOGO: "pgo.services.import_archivos_catalogo",
    TYPE_RISK_LEASING: "risk.services.import_leasing_database",
    TYPE_RISK_RENTAS: "risk.services.import_leasing_rentas",
    TYPE_NEW_CLIENTS: "import_clientes_nuevos",
    TYPE_CROSS_SALE: "import_venta_cruzada",
    TYPE_FINANCIAL: "pgc.admin_monthly (manual)",
}


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
        (TYPE_NEW_CLIENTS, "clientesnuevos" in compact or "clientes_nuevos" in name, "nombre: ClientesNuevos"),
        (TYPE_CROSS_SALE, "ventacruzada" in compact, "nombre: VentaCruzada"),
        (TYPE_FINANCIAL, name.startswith("wc") or "estado_resultados" in name or "er_" in name, "nombre: WC*/ER financiero"),
        (TYPE_PGO_TICKETS, "pgo" in name and ("ticket" in name or "control" in name), "nombre: PGO+tickets/control"),
        (TYPE_PGO_CATALOGO, "pgo" in name and "archivo" in name, "nombre: PGO+archivos"),
        (TYPE_CRM_CLIENTES, "crm" in name or "infoclientes" in compact, "nombre: CRM/InfoClientes"),
        (TYPE_RISK_RENTAS, "rentas" in name and "leasing" in name, "nombre: LeasingRentas"),
        (
            TYPE_RISK_LEASING,
            "baseleasing" in compact
            or ("balon" in name and "leasing" in name)
            or ("leasing" in name and "base" in name),
            "nombre: BaseLeasing/balón",
        ),
    ]
    for tipo, matched, reason in checks:
        if matched:
            return DetectionResult(
                tipo=tipo,
                confidence=0.85,
                label=TYPE_LABELS[tipo],
                reasons=[reason],
                layer="nombre",
            )
    return None


def detect_from_columns(cols: set[str]) -> DetectionResult | None:
    candidates: list[tuple[str, int, list[str]]] = []

    crm_score = _score_columns(
        cols,
        [["nit"], ["nombre", "nombre_cliente", "cliente", "razon_social"], ["wcf", "wcl", "wci"]],
    )
    if crm_score >= 2:
        candidates.append((TYPE_CRM_CLIENTES, crm_score, ["estructura: NIT/Nombre/WCF|WCL|WCI"]))

    pgo_score = _score_columns(
        cols,
        [["id", "codigo", "ticket"], ["titulo", "asunto"], ["estado"], ["fecha_apertura", "usuario_solicita"]],
    )
    if pgo_score >= 3:
        candidates.append((TYPE_PGO_TICKETS, pgo_score, ["estructura: ID/Titulo/Estado helpdesk"]))

    catalog_score = _score_columns(cols, [["carpeta", "archivo"], ["creado_por", "creado_en"]])
    if catalog_score >= 2:
        candidates.append((TYPE_PGO_CATALOGO, catalog_score, ["estructura: Carpeta/Archivo"]))

    leasing_score = _score_columns(
        cols,
        [
            ["contract_number", "contrato", "no_contrato"],
            ["client_name", "cliente", "nombre_cliente"],
            ["capital_balance", "saldo", "duedays", "due_days"],
        ],
    )
    if leasing_score >= 2:
        candidates.append((TYPE_RISK_LEASING, leasing_score, ["estructura: Contract/Client/Balance"]))

    rentas_score = _score_columns(
        cols,
        [["no_contrato", "contrato"], ["vencimiento"], ["valor_renta", "renta_total"], ["estado"]],
    )
    if rentas_score >= 3:
        candidates.append((TYPE_RISK_RENTAS, rentas_score, ["estructura: NoContrato/Vencimiento/ValorRenta"]))

    nc_score = _score_columns(cols, [["une"], ["cliente", "nombre"], ["fecha", "mes"], ["monto", "amount", "ingreso"]])
    if "une" in cols and nc_score >= 2:
        candidates.append((TYPE_NEW_CLIENTS, nc_score, ["estructura: UNE + cliente/periodo"]))

    xc_score = _score_columns(
        cols,
        [
            ["une", "unidad"],
            ["producto_origen", "origen", "producto"],
            ["producto_destino", "destino", "cruzado"],
            ["cliente", "nombre"],
        ],
    )
    if xc_score >= 3:
        candidates.append((TYPE_CROSS_SALE, xc_score, ["estructura: venta cruzada origen/destino"]))

    if not candidates:
        return None
    candidates.sort(key=lambda x: x[1], reverse=True)
    tipo, score, reasons = candidates[0]
    conf = min(0.95, 0.55 + 0.1 * score)
    suggestions = [(t, TYPE_LABELS[t]) for t, _, _ in candidates[1:3]]
    ambiguous = len(candidates) > 1 and candidates[0][1] == candidates[1][1]
    return DetectionResult(
        tipo=tipo,
        confidence=conf * (0.75 if ambiguous else 1.0),
        label=TYPE_LABELS[tipo],
        reasons=reasons,
        suggestions=suggestions,
        layer="estructura",
        ambiguous=ambiguous,
        candidates=[(t, float(s), "; ".join(r)) for t, s, r in candidates],
    )


def detect_from_content(df) -> DetectionResult | None:
    """Capa 3: patrones en valores de muestra (primeras filas)."""
    if df is None or df.empty:
        return None

    sample = df.head(40)
    cols = set(sample.columns)
    scores: dict[str, float] = {}
    reasons: dict[str, list[str]] = {}

    def bump(tipo: str, pts: float, reason: str) -> None:
        scores[tipo] = scores.get(tipo, 0.0) + pts
        reasons.setdefault(tipo, []).append(reason)

    # NIT / documento típico CRM
    for col in ("nit", "documento", "ruc", "identificacion"):
        if col in cols:
            series = sample[col].astype(str).str.replace(r"\s+", "", regex=True)
            nit_hits = series.str.match(r"^\d{6,14}(-\d)?$").sum()
            if nit_hits >= 3:
                bump(TYPE_CRM_CLIENTES, 1.5, f"contenido: {nit_hits} NITs en '{col}'")

    # Flags UNE en columnas WCF/WCL/WCI
    une_flag_cols = [c for c in ("wcf", "wcl", "wci") if c in cols]
    if une_flag_cols:
        bump(TYPE_CRM_CLIENTES, 1.0, f"contenido: columnas producto {', '.join(une_flag_cols)}")

    # Tickets PGO: estados / prioridades frecuentes
    if "estado" in cols:
        estados = " ".join(sample["estado"].astype(str).str.lower().unique()[:20])
        if any(k in estados for k in ("abierto", "cerrado", "pendiente", "en proceso", "resuelto")):
            bump(TYPE_PGO_TICKETS, 1.2, "contenido: estados tipo helpdesk")
        if any(k in estados for k in ("vigente", "vencid", "pagad", "mora")):
            bump(TYPE_RISK_RENTAS, 1.0, "contenido: estados tipo renta/cuota")

    if any(c in cols for c in ("titulo", "asunto")) and any(c in cols for c in ("id", "codigo", "ticket")):
        bump(TYPE_PGO_TICKETS, 0.8, "contenido: id+titulo ticket")

    # Leasing: días de mora / saldo
    for col in ("duedays", "due_days", "dias_mora", "diasmora"):
        if col in cols:
            numeric = sample[col].apply(lambda v: _is_number(v))
            if numeric.sum() >= 3:
                bump(TYPE_RISK_LEASING, 1.3, f"contenido: días mora en '{col}'")

    for col in ("capital_balance", "saldo", "saldo_capital", "outstanding"):
        if col in cols and sample[col].apply(_is_number).sum() >= 3:
            bump(TYPE_RISK_LEASING, 0.9, f"contenido: saldos en '{col}'")

    for col in ("valor_renta", "renta_total", "monto_renta"):
        if col in cols and sample[col].apply(_is_number).sum() >= 3:
            bump(TYPE_RISK_RENTAS, 1.2, f"contenido: montos renta en '{col}'")

    # Clientes nuevos: códigos UNE
    if "une" in cols:
        unes = " ".join(sample["une"].astype(str).str.upper().unique()[:30])
        if any(k in unes for k in ("WCF", "WCL", "WCI", "INVEST", "FACTOR")):
            bump(TYPE_NEW_CLIENTS, 1.4, "contenido: códigos UNE comerciales")

    # Venta cruzada: mención origen/destino en valores o columnas
    if any(c in cols for c in ("producto_origen", "producto_destino", "origen", "destino")):
        bump(TYPE_CROSS_SALE, 1.2, "contenido: columnas origen/destino producto")

    if not scores:
        return None

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_tipo, best_score = ranked[0]
    conf = min(0.92, 0.45 + 0.12 * best_score)
    ambiguous = len(ranked) > 1 and (ranked[0][1] - ranked[1][1]) < 0.6
    suggestions = [(t, TYPE_LABELS[t]) for t, _ in ranked[1:3] if t in TYPE_LABELS]
    return DetectionResult(
        tipo=best_tipo,
        confidence=conf * (0.7 if ambiguous else 1.0),
        label=TYPE_LABELS.get(best_tipo, best_tipo),
        reasons=reasons.get(best_tipo, [])[:4],
        suggestions=suggestions,
        layer="contenido",
        ambiguous=ambiguous,
        candidates=[(t, s, "; ".join(reasons.get(t, [])[:2])) for t, s in ranked],
    )


def _is_number(value) -> bool:
    try:
        if value is None:
            return False
        s = str(value).strip().replace(",", "")
        if not s or s.lower() in ("nan", "none", "-"):
            return False
        float(s)
        return True
    except (TypeError, ValueError):
        return False


def _merge_detections(
    by_name: DetectionResult | None,
    by_cols: DetectionResult | None,
    by_content: DetectionResult | None,
) -> DetectionResult:
    """Fusiona las tres capas con prioridad nombre → estructura → contenido."""
    votes: dict[str, float] = {}
    all_reasons: list[str] = []
    layers_used: list[str] = []

    def add_vote(det: DetectionResult | None, weight: float) -> None:
        if not det or det.tipo == TYPE_UNKNOWN:
            return
        votes[det.tipo] = votes.get(det.tipo, 0.0) + det.confidence * weight
        all_reasons.extend(det.reasons)
        if det.layer:
            layers_used.append(det.layer)

    # Pesos: nombre fuerte si coincide; estructura y contenido refuerzan
    add_vote(by_name, 1.0)
    add_vote(by_cols, 1.15)
    add_vote(by_content, 1.05)

    if not votes:
        return DetectionResult(
            tipo=TYPE_UNKNOWN,
            confidence=0.0,
            label=TYPE_LABELS[TYPE_UNKNOWN],
            reasons=["No se pudo identificar el tipo con ninguna capa"],
            suggestions=[(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE],
            layer="ninguna",
            ambiguous=True,
        )

    ranked = sorted(votes.items(), key=lambda x: x[1], reverse=True)
    best_tipo, best_vote = ranked[0]
    second_vote = ranked[1][1] if len(ranked) > 1 else 0.0

    # Acuerdo nombre + estructura → alta confianza
    name_tipo = by_name.tipo if by_name else None
    cols_tipo = by_cols.tipo if by_cols else None
    content_tipo = by_content.tipo if by_content else None

    agreement = sum(
        1
        for t in (name_tipo, cols_tipo, content_tipo)
        if t and t == best_tipo
    )

    confidence = min(0.99, best_vote / max(1.0, agreement + 0.5))
    if agreement >= 2:
        confidence = max(confidence, 0.88)
    if agreement >= 3:
        confidence = max(confidence, 0.95)

    conflict = False
    if name_tipo and cols_tipo and name_tipo != cols_tipo:
        conflict = True
        all_reasons.append(f"conflicto nombre({name_tipo}) vs estructura({cols_tipo})")
        confidence = min(confidence, 0.72)

    if content_tipo and cols_tipo and content_tipo != cols_tipo and agreement < 2:
        conflict = True
        all_reasons.append(f"contenido({content_tipo}) difiere de estructura({cols_tipo})")

    margin_tight = (best_vote - second_vote) < 0.25 and len(ranked) > 1
    ambiguous = conflict or margin_tight or confidence < CONFIDENCE_AUTO

    suggestions: list[tuple[str, str]] = []
    for t, _ in ranked[1:4]:
        if t in TYPE_LABELS:
            suggestions.append((t, TYPE_LABELS[t]))
    # Incluir capas discrepantes
    for t in (name_tipo, cols_tipo, content_tipo):
        if t and t != best_tipo and t in TYPE_LABELS:
            pair = (t, TYPE_LABELS[t])
            if pair not in suggestions:
                suggestions.append(pair)

    layer = "+".join(dict.fromkeys(layers_used)) or "combinada"
    if agreement >= 2:
        layer = f"combinada({agreement} capas)"

    return DetectionResult(
        tipo=best_tipo,
        confidence=confidence,
        label=TYPE_LABELS.get(best_tipo, best_tipo),
        reasons=list(dict.fromkeys(all_reasons))[:8],
        suggestions=suggestions[:4],
        layer=layer,
        ambiguous=ambiguous,
        candidates=[(t, v, "") for t, v in ranked],
    )


def detect_file(uploaded_file) -> DetectionResult:
    by_name = detect_from_name(getattr(uploaded_file, "name", "") or "")
    df = None
    by_cols = None
    by_content = None

    try:
        df = normalize_columns(read_dataframe(uploaded_file, sheet_name=None))
        uploaded_file.seek(0)
        cols = set(df.columns)
        by_cols = detect_from_columns(cols)
        by_content = detect_from_content(df)
    except Exception as exc:
        uploaded_file.seek(0)
        if by_name and by_name.confidence >= 0.8:
            by_name.reasons.append(f"columnas no leídas ({exc})")
            by_name.ambiguous = False
            return by_name
        return DetectionResult(
            tipo=TYPE_UNKNOWN,
            confidence=0.0,
            label=TYPE_LABELS[TYPE_UNKNOWN],
            reasons=[f"No se pudo leer el archivo: {exc}"],
            suggestions=[(t, TYPE_LABELS[t]) for t in ALL_IMPORTABLE[:5]],
            layer="error",
            ambiguous=True,
        )

    return _merge_detections(by_name, by_cols, by_content)


def detect_path(path: str) -> DetectionResult:
    from pathlib import Path

    from django.core.files.uploadedfile import SimpleUploadedFile

    p = Path(path)
    f = SimpleUploadedFile(p.name, p.read_bytes())
    return detect_file(f)
