"""Comando ejecutivo cruzado — señales de Riesgo, PGO, CRM + finanzas."""

from __future__ import annotations

from typing import Any

from .indices import build_indices_catalog
from .intermediacion import build_intermediacion
from .utils import fmt


def _safe(fn, default=None):
    try:
        return fn()
    except Exception:  # noqa: BLE001
        return default


def _risk_summary() -> dict:
    from risk.selectors import latest_snapshots_queryset, snapshot_summary

    return snapshot_summary(latest_snapshots_queryset(None))


def _pgo_summary() -> dict:
    from pgo.models import Ticket

    total = Ticket.objects.count()
    abiertos = Ticket.objects.filter(estado=Ticket.ESTADO_ABIERTO).count()
    return {
        "total_tickets": total,
        "tickets_abiertos": abiertos,
        "tickets_cerrados": max(total - abiertos, 0),
    }


def _crm_summary() -> dict:
    try:
        from crm.models import Entidad

        return {"entidades": Entidad.objects.count()}
    except Exception:  # noqa: BLE001
        from core.wcg_models import Entidad

        return {"entidades": Entidad.objects.count()}


def build_comando(data: dict) -> dict[str, Any]:
    idx = build_indices_catalog(data, bu="T", periods=6)
    inter = build_intermediacion(data, bu="T", months=6, mode="gerencial")

    risk = _safe(_risk_summary, {}) or {}
    pgo = _safe(_pgo_summary, {}) or {}
    crm = _safe(_crm_summary, {"entidades": 0}) or {"entidades": 0}

    m = (idx.get("metrics") or {}) if idx.get("status") == "ok" else {}
    latest_inter = (inter.get("latest") or {}) if inter.get("status") == "ok" else {}

    liq = m.get("liquidez")
    apa = m.get("apalancamiento")
    z = m.get("z_score")

    signals = [
        {
            "domain": "Intermediación",
            "title": "Margen bruto",
            "value": fmt(latest_inter.get("margen_bruto")),
            "tone": "ok" if (latest_inter.get("margen_bruto") or 0) > 0 else "risk",
            "detail": f"Utilidad gerencial {fmt(latest_inter.get('utilidad'))}",
            "href": "/gerencia/intermediacion/",
        },
        {
            "domain": "Liquidez",
            "title": "Liquidez AC/PC",
            "value": f"{liq:.2f}×" if liq is not None else "—",
            "tone": "ok" if (liq or 0) >= 1.2 else "risk",
            "detail": f"Z-score {z:.2f}" if z is not None else "Sin Z",
            "href": "/gerencia/liquidez/",
        },
        {
            "domain": "Riesgo",
            "title": "Operaciones en alerta",
            "value": str(risk.get("alertas", "—")),
            "tone": "warn" if (risk.get("alertas") or 0) > 0 else "ok",
            "detail": f"{risk.get('con_mora', 0)} con mora · {risk.get('operaciones', 0)} ops",
            "href": "/risk/",
        },
        {
            "domain": "PGO",
            "title": "Tickets abiertos",
            "value": str(pgo.get("tickets_abiertos", "—")),
            "tone": "warn" if (pgo.get("tickets_abiertos") or 0) > 20 else "ok",
            "detail": f"Total {pgo.get('total_tickets', '—')}",
            "href": "/pgo/",
        },
        {
            "domain": "CRM",
            "title": "Entidades",
            "value": str(crm.get("entidades", "—")),
            "tone": "neutral",
            "detail": "Base comercial",
            "href": "/crm/",
        },
        {
            "domain": "Estructura",
            "title": "Apalancamiento",
            "value": f"{apa:.2f}×" if apa is not None else "—",
            "tone": "ok" if (apa or 0) <= 2.2 else "warn",
            "detail": "Pasivo / Patrimonio",
            "href": "/gerencia/estructura/",
        },
    ]

    narrative: list[str] = []
    if idx.get("status") == "ok":
        liq_s = f"{liq:.2f}×" if liq is not None else "n/d"
        apa_s = f"{apa:.2f}×" if apa is not None else "n/d"
        narrative.append(
            f"Período ancla {idx['period']}: liquidez {liq_s}, apalancamiento {apa_s}."
        )
    if latest_inter:
        narrative.append(
            f"Intermediación: margen {fmt(latest_inter.get('margen_bruto'))}, "
            f"overhead {fmt(latest_inter.get('overhead_neto'))}, "
            f"utilidad gerencial {fmt(latest_inter.get('utilidad'))}."
        )
    narrative.append(
        f"Balón de riesgo: {risk.get('alertas', 0)} alertas, {risk.get('con_mora', 0)} con mora."
    )
    narrative.append(
        f"Operación PGO: {pgo.get('tickets_abiertos', 0)} tickets abiertos "
        f"de {pgo.get('total_tickets', 0)}."
    )
    narrative.append(
        "Use What-if para probar crecimientos de cartera y tasas antes de fijar metas."
    )

    return {
        "status": "ok",
        "period": idx.get("period"),
        "signals": signals,
        "narrative": narrative[:5],
        "finance_ok": idx.get("status") == "ok",
    }
