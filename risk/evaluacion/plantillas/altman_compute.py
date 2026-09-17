"""Cálculo de ratios y Z-scores Altman desde métricas de Carátula."""

from __future__ import annotations

from typing import Any

# Coeficientes y umbrales de la hoja Altman del workbook de referencia WCG.
ALTMAN_MODELS: list[dict[str, Any]] = [
    {
        "id": 1,
        "label": "1. Altman Original (1968) – Manufactureras Públicas",
        "key": "z_altman_1968",
        "low": 1.81,
        "high": 2.99,
        "coefs": (1.2, 1.4, 3.3, 0.6, 1.0),
    },
    {
        "id": 2,
        "label": "2. Altman Revisado (1983) – Manufactureras Privadas",
        "key": "z_altman_1983",
        "low": 1.23,
        "high": 2.90,
        "coefs": (0.717, 0.847, 3.107, 0.42, 0.998),
    },
    {
        "id": 3,
        "label": "3. Z'' para No Manufactureras y Mercados Emergentes",
        "key": "z_emergentes",
        "low": 1.23,
        "high": 2.90,
        "coefs": (6.56, 3.26, 6.72, 1.05, 0.0),
    },
    {
        "id": 4,
        "label": "4. Altman Modificado (Ventas Ajustadas)",
        "key": "z_modificado",
        "low": 1.81,
        "high": 2.99,
        "coefs": (1.2, 1.4, 3.3, 0.6, 0.99),
    },
    {
        "id": 5,
        "label": "5. Z'-Score Revisado para PYMES de Europa Central y Este",
        "key": "z_pymes_ece",
        "low": 1.23,
        "high": 2.90,
        "coefs": (0.717, 0.847, 3.107, 0.42, 0.998),
    },
    {
        "id": 6,
        "label": "6. Z''-Score Mercados Emergentes (con constante)",
        "key": "z_emergentes_const",
        "low": 1.10,
        "high": 2.60,
        "coefs": (6.56, 3.26, 6.72, 1.05, 0.0),
    },
    {
        "id": 7,
        "label": "7. Pesos Iguales (Propuesta Experimental)",
        "key": "z_pesos_iguales",
        "low": 1.81,
        "high": 2.99,
        "coefs": (1.0, 1.0, 1.0, 1.0, 1.0),
    },
    {
        "id": 8,
        "label": "8. Ajuste para Empresas Medianas Latinoamericanas",
        "key": "z_latam",
        "low": 1.23,
        "high": 2.90,
        "coefs": (1.5, 1.0, 2.5, 0.5, 1.0),
    },
]

RATIO_LABELS = (
    "1. Capital de Trabajo / Activo",
    "2. Utilidades Retenidas / Activo",
    "3. EBITDA / Activo",
    "4. Patrimonio / Pasivo",
    "5. Ventas / Activo",
)

PRIMARY_MODEL_ID = 3


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip().replace(",", "")
        if not text or text.lower() in {"n/a", "na", "-", "—"}:
            return None
        try:
            return float(text)
        except ValueError:
            return None
    return None


def _metric_lookup(metric_rows: list[tuple[str, list]]) -> dict[str, list[float | None]]:
    aliases = {
        "ventas": ("ventas",),
        "capital_trabajo": ("capital de trabajo",),
        "utilidades_retenidas": ("utilidades retenidas",),
        "ebitda": ("ebitda",),
        "total_activo": ("total de activo", "total activo"),
        "total_patrimonio": ("total patrimonio",),
        "total_pasivo": ("total pasivo",),
    }
    out: dict[str, list[float | None]] = {k: [] for k in aliases}
    for label, vals in metric_rows:
        n = str(label or "").strip().lower()
        for key, needles in aliases.items():
            if any(needle in n for needle in needles):
                out[key] = [_to_float(v) for v in vals]
                break
    return out


def compute_altman_ratios(metrics: dict[str, list[float | None]]) -> list[list[float | None]]:
    n = max(len(v) for v in metrics.values()) if metrics else 0
    ratios: list[list[float | None]] = [[] for _ in RATIO_LABELS]

    def at(key: str, i: int) -> float | None:
        vals = metrics.get(key, [])
        return vals[i] if i < len(vals) else None

    for i in range(n):
        t_act = at("total_activo", i)
        t_pas = at("total_pasivo", i)
        ct = at("capital_trabajo", i)
        ur = at("utilidades_retenidas", i)
        ebitda = at("ebitda", i)
        pat = at("total_patrimonio", i)
        ventas = at("ventas", i)

        ratios[0].append(ct / t_act if ct is not None and t_act else None)
        ratios[1].append(ur / t_act if ur is not None and t_act else None)
        ratios[2].append(ebitda / t_act if ebitda is not None and t_act else None)
        ratios[3].append(pat / t_pas if pat is not None and t_pas else None)
        ratios[4].append(ventas / t_act if ventas is not None and t_act else None)

    return ratios


def compute_z_score(ratios: list[float | None], coefs: tuple[float, ...]) -> float | None:
    if len(ratios) != 5 or any(r is None for r in ratios):
        return None
    return sum(c * r for c, r in zip(coefs, ratios))


def classify_z_label(z: float | None, low: float, high: float) -> str | None:
    if z is None:
        return None
    if z < low:
        return "Mal"
    if z < high:
        return "Soso"
    return "Bien"


def build_altman_row_defs(
    metric_rows: list[tuple[str, list]],
) -> list[tuple[str, list | None]]:
    """Genera filas de ratios, Z-scores y calificación para la hoja Caratula."""
    metrics = _metric_lookup(metric_rows)
    if not any(metrics.values()):
        return []

    n = max(len(v) for v in metrics.values())
    ratio_vals = compute_altman_ratios(metrics)
    row_defs: list[tuple[str, list | None]] = [("", None)]

    for label, vals in zip(RATIO_LABELS, ratio_vals):
        row_defs.append((label, vals))

    row_defs.append(("", None))

    z_by_model: dict[int, list[float | None]] = {}
    for model in ALTMAN_MODELS:
        scores: list[float | None] = []
        for i in range(n):
            ratios_i = [ratio_vals[j][i] if i < len(ratio_vals[j]) else None for j in range(5)]
            scores.append(compute_z_score(ratios_i, model["coefs"]))
        z_by_model[model["id"]] = scores
        row_defs.append((model["label"], scores))

    primary = next(m for m in ALTMAN_MODELS if m["id"] == PRIMARY_MODEL_ID)
    labels = [
        classify_z_label(z, primary["low"], primary["high"])
        for z in z_by_model[PRIMARY_MODEL_ID]
    ]
    row_defs.append((primary["label"], labels))

    return row_defs
