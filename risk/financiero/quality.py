"""Calidad de datos y exportación Excel del dataset financiero."""

from __future__ import annotations

import io
import json
from pathlib import Path
from typing import Any

from django.conf import settings


def _seed_dir() -> Path:
    return Path(settings.BASE_DIR) / "risk" / "financiero" / "seed"


def load_warnings() -> dict[str, Any]:
    p = _seed_dir() / "data_warnings.json"
    if not p.exists():
        return {"count": 0, "warnings": [], "status": "empty"}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        data["status"] = "ok"
        return data
    except Exception:  # noqa: BLE001
        return {"count": 0, "warnings": [], "status": "error"}


def tabla_xlsx_path() -> Path | None:
    p = _seed_dir() / "estados_financieros_tabla.xlsx"
    return p if p.exists() else None


def summarize_warnings(raw: dict[str, Any], limit: int = 12) -> list[dict[str, Any]]:
    """Collapse noisy per-period rows into short UI bullets."""
    items = list(raw.get("warnings") or [])
    # Prefer mapping / account gaps over every period duplicate
    priority = {"missing_account": 0, "kpi_map": 1, "kpi_gap": 2, "missing_periods": 3}
    items.sort(key=lambda w: (priority.get(w.get("severity", ""), 9), w.get("bu", ""), w.get("metric", "")))

    bullets: list[dict[str, Any]] = []
    seen: set[tuple] = set()
    for w in items:
        sev = w.get("severity") or ""
        bu = w.get("bu") or ""
        metric = w.get("metric") or ""
        key = (sev, bu, metric)
        if key in seen:
            continue
        seen.add(key)
        if sev == "kpi_gap" and metric == "activo":
            text = (
                f"{bu}: KPI «activo» (cuenta 1) falta en varios meses 2025; "
                f"existen 101/102 (el tablero deriva activo = 101+102 para mostrar)."
            )
        elif sev == "kpi_map" and metric == "cartera":
            text = (
                f"{bu}: «Cartera» en 0 porque el KPI solo busca códigos de Factoraje (10103*). "
                f"Leasing usa otras cuentas (p. ej. 1020204)."
            )
        elif sev == "missing_account":
            text = f"{bu}: no hay cuenta {metric} en el dataset combinado."
        elif sev == "missing_periods":
            text = f"{bu} cuenta {metric}: faltan períodos ({w.get('period')}). {w.get('detail') or ''}"
        else:
            text = f"{bu} · {metric}: {w.get('detail') or sev}"
        bullets.append({"severity": sev, "bu": bu, "metric": metric, "text": text})
        if len(bullets) >= limit:
            break
    return bullets


def enrich_kpi_row(row: dict[str, Any] | None) -> dict[str, Any]:
    """Fill display gaps: activo ← 101+102 when cuenta 1 missing."""
    if not row:
        return {}
    out = dict(row)
    if out.get("activo") is None:
        ac = out.get("activo_corriente")
        anc = out.get("activo_no_corriente")
        if ac is not None or anc is not None:
            out["activo"] = (ac or 0) + (anc or 0)
            out["_activo_derived"] = True
    return out
