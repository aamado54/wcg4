"""Vista gerencial sobre el dataset de evaluación (ranking, alertas, evolución)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .reader import AltmanModel, EvaluacionDataset


ZONE_ALTO = "alto"
ZONE_MODERADO = "moderado"
ZONE_BAJO = "bajo"
ZONE_SIN_DATO = "sin_dato"

ZONE_LABELS = {
    ZONE_ALTO: "Alto riesgo",
    ZONE_MODERADO: "Riesgo moderado",
    ZONE_BAJO: "Bajo riesgo",
    ZONE_SIN_DATO: "Sin dato",
}

LABEL_TO_ZONE = {
    "mal": ZONE_ALTO,
    "soso": ZONE_MODERADO,
    "bien": ZONE_BAJO,
}

DELTA_CAE = -0.25
DELTA_MEJORA = 0.25


@dataclass
class RankedClient:
    code: str
    name: str
    year: int | None
    z: float | None
    zone: str
    zone_label: str
    z_delta: float | None
    liquidez: float | None
    apalancamiento: float | None
    roe: float | None
    crecimiento_ventas: float | None
    utilidad_neta: float | None
    ventas: float | None
    status: str | None
    currency_unit: str | None
    alert_reasons: list[str] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class PortfolioView:
    source: str
    primary_z_key: str
    primary_model_name: str
    thresholds: dict[str, float | None]
    summary: dict[str, Any]
    headline: str
    ranking: list[RankedClient]
    alerts: list[RankedClient]
    falling: list[RankedClient]
    improving: list[RankedClient]
    chart_z_evolution: dict[str, Any]
    chart_zone_mix: dict[str, Any]
    errors: list[str]
    sheets_read: list[str]
    status: str  # ok | empty | error | partial

    def to_context(self) -> dict[str, Any]:
        return asdict(self)


def classify_z(
    z: float | None,
    *,
    z_label: str | None,
    model: AltmanModel | None,
) -> str:
    if z_label:
        mapped = LABEL_TO_ZONE.get(z_label.strip().lower())
        if mapped:
            return mapped
    if z is None:
        return ZONE_SIN_DATO
    low = model.low_cut if model and model.low_cut is not None else 1.23
    high = model.high_cut if model and model.high_cut is not None else 2.90
    if z < low:
        return ZONE_ALTO
    if z < high:
        return ZONE_MODERADO
    return ZONE_BAJO


def _primary_model(dataset: EvaluacionDataset) -> AltmanModel | None:
    for m in dataset.altman_models:
        if m.id == 3:
            return m
    return dataset.altman_models[0] if dataset.altman_models else None


def _alert_reasons(zone: str, z_delta: float | None) -> list[str]:
    reasons: list[str] = []
    if zone == ZONE_ALTO:
        reasons.append("Zona de alto riesgo")
    if z_delta is not None and z_delta < DELTA_CAE:
        reasons.append("Caída de Z vs período previo")
    return reasons


def _build_headline(summary: dict[str, Any], ranked: list[RankedClient]) -> str:
    n = summary.get("clientes") or 0
    if n == 0:
        return "Sin cartera para evaluar en esta plantilla."
    alto = summary.get("alto") or 0
    mod = summary.get("moderado") or 0
    cae = summary.get("deterioro") or 0
    mejora = summary.get("mejora") or 0
    conc = summary.get("concentracion_pct")
    worst = next((r for r in ranked if r.z is not None), None)
    parts = []
    if conc is not None:
        parts.append(f"{conc:.0f}% del portafolio en zona alta o moderada")
    if worst:
        parts.append(f"peor Z: {worst.name} ({worst.z:.2f})")
    if cae or mejora:
        parts.append(f"{cae} caen · {mejora} mejoran")
    if alto:
        parts.append(f"{alto} en alto riesgo")
    elif mod:
        parts.append(f"{mod} en riesgo moderado")
    return " · ".join(parts) if parts else f"{n} clientes con evaluación Z."


def build_portfolio_view(
    dataset: EvaluacionDataset,
    *,
    cliente: str | None = None,
) -> PortfolioView:
    model = _primary_model(dataset)
    z_key = dataset.primary_z_key
    ranked: list[RankedClient] = []

    for company in dataset.companies:
        if (
            cliente
            and cliente.lower() not in company.name.lower()
            and cliente.lower() != company.code.lower()
        ):
            continue
        latest = company.latest()
        if not latest:
            continue
        z = latest.z_scores.get(z_key)
        # Fallback: si falta el modelo primario, usar el primer Z numérico disponible.
        if z is None and latest.z_scores:
            for _k, val in latest.z_scores.items():
                if val is not None:
                    z = val
                    break
        zone = classify_z(z, z_label=latest.z_label, model=model)

        ordered = sorted(company.periods, key=lambda p: p.year)
        prev = ordered[-2] if len(ordered) >= 2 else None
        z_delta = None
        if z is not None and prev is not None:
            pz = prev.z_scores.get(z_key)
            if pz is None and prev.z_scores:
                for val in prev.z_scores.values():
                    if val is not None:
                        pz = val
                        break
            if pz is not None:
                z_delta = z - pz

        history = []
        for p in ordered:
            pz = p.z_scores.get(z_key)
            if pz is None and p.z_scores:
                for val in p.z_scores.values():
                    if val is not None:
                        pz = val
                        break
            p_zone = classify_z(pz, z_label=p.z_label, model=model)
            spark_h = 3
            if pz is not None:
                spark_h = max(3, min(22, int(round(abs(pz) * 4))))
            history.append(
                {
                    "year": p.year,
                    "z": pz,
                    "zone": p_zone,
                    "zone_label": ZONE_LABELS[p_zone],
                    "liquidez": p.metrics.get("liquidez"),
                    "roe": p.metrics.get("roe"),
                    "ventas": p.metrics.get("ventas"),
                    "utilidad_neta": p.metrics.get("utilidad_neta"),
                    "apalancamiento": p.metrics.get("apalancamiento"),
                    "status": p.status,
                    "spark_h": spark_h,
                }
            )

        ranked.append(
            RankedClient(
                code=company.code,
                name=company.name,
                year=latest.year,
                z=z,
                zone=zone,
                zone_label=ZONE_LABELS[zone],
                z_delta=z_delta,
                liquidez=latest.metrics.get("liquidez"),
                apalancamiento=latest.metrics.get("apalancamiento"),
                roe=latest.metrics.get("roe"),
                crecimiento_ventas=latest.metrics.get("crecimiento_ventas"),
                utilidad_neta=latest.metrics.get("utilidad_neta"),
                ventas=latest.metrics.get("ventas"),
                status=latest.status,
                currency_unit=company.currency_unit,
                alert_reasons=_alert_reasons(zone, z_delta),
                history=history,
            )
        )

    def sort_key(item: RankedClient):
        if item.z is None:
            return (1, 0.0, item.name)
        return (0, item.z, item.name)

    ranked.sort(key=sort_key)

    alerts = [r for r in ranked if r.alert_reasons]
    falling = sorted(
        [r for r in ranked if r.z_delta is not None and r.z_delta < DELTA_CAE],
        key=lambda r: r.z_delta or 0,
    )
    improving = sorted(
        [r for r in ranked if r.z_delta is not None and r.z_delta > DELTA_MEJORA],
        key=lambda r: -(r.z_delta or 0),
    )

    counts = {ZONE_ALTO: 0, ZONE_MODERADO: 0, ZONE_BAJO: 0, ZONE_SIN_DATO: 0}
    for r in ranked:
        counts[r.zone] = counts.get(r.zone, 0) + 1

    zs = [r.z for r in ranked if r.z is not None]
    n = len(ranked)
    riesgo_conc = counts[ZONE_ALTO] + counts[ZONE_MODERADO]
    concentracion_pct = round(100.0 * riesgo_conc / n, 1) if n else None

    summary = {
        "clientes": n,
        "alto": counts[ZONE_ALTO],
        "moderado": counts[ZONE_MODERADO],
        "bajo": counts[ZONE_BAJO],
        "sin_dato": counts[ZONE_SIN_DATO],
        "z_promedio": round(sum(zs) / len(zs), 2) if zs else None,
        "deterioro": len(falling),
        "mejora": len(improving),
        "concentracion_pct": concentracion_pct,
        "en_riesgo": riesgo_conc,
    }

    low = model.low_cut if model and model.low_cut is not None else 1.23
    high = model.high_cut if model and model.high_cut is not None else 2.90

    chart_z = _chart_z_evolution(ranked, low=low, high=high)
    chart_mix = {
        "labels": ["Alto", "Moderado", "Bajo", "Sin dato"],
        "values": [
            counts[ZONE_ALTO],
            counts[ZONE_MODERADO],
            counts[ZONE_BAJO],
            counts[ZONE_SIN_DATO],
        ],
        "colors": ["#b4534a", "#c4a35a", "#4a7c6f", "#94a3b8"],
    }

    # Propagar status del dataset; empty si filtro sin resultados.
    status = dataset.status
    if status == "ok" and n == 0:
        status = "empty"

    return PortfolioView(
        source=dataset.source,
        primary_z_key=z_key,
        primary_model_name=(
            model.name if model else "Z'' No manufactureras / mercados emergentes"
        ),
        thresholds={"alto_lt": low, "bajo_gte": high},
        summary=summary,
        headline=_build_headline(summary, ranked),
        ranking=ranked,
        alerts=alerts,
        falling=falling[:5],
        improving=improving[:5],
        chart_z_evolution=chart_z,
        chart_zone_mix=chart_mix,
        errors=list(dataset.errors),
        sheets_read=list(dataset.sheets_read),
        status=status,
    )


def _chart_z_evolution(
    ranked: list[RankedClient],
    *,
    low: float,
    high: float,
) -> dict[str, Any]:
    """Peores 4 + mejores 2; incluye líneas de umbral para lectura gerencial."""
    with_z = [r for r in ranked if r.z is not None]
    worst = with_z[:4]
    best = list(reversed(with_z[-2:])) if len(with_z) > 4 else []
    selected = []
    seen = set()
    for r in worst + best:
        if r.code not in seen:
            selected.append(r)
            seen.add(r.code)

    years: set[int] = set()
    for r in selected:
        for h in r.history:
            if h.get("z") is not None:
                years.add(h["year"])
    labels = sorted(years)

    datasets = []
    palette = [
        "#b4534a",
        "#c4a35a",
        "#5b7c99",
        "#6b5b7a",
        "#4a7c6f",
        "#8b7355",
    ]
    for idx, r in enumerate(selected):
        by_year = {h["year"]: h.get("z") for h in r.history}
        datasets.append(
            {
                "label": r.name[:28],
                "data": [by_year.get(y) for y in labels],
                "borderColor": palette[idx % len(palette)],
                "backgroundColor": "transparent",
            }
        )
    return {
        "labels": labels,
        "datasets": datasets,
        "thresholds": {"alto_lt": low, "bajo_gte": high},
        "has_series": bool(datasets and labels),
    }
