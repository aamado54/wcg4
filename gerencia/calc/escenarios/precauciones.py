"""Artículos detallados de precauciones · escenario Nov 2026."""

from __future__ import annotations

from typing import Any

PRECAUTION_ARTICLES: dict[str, dict[str, Any]] = {
    "liquidez-war-room": {
        "title": "Activar war room de liquidez",
        "summary": "La liquidez simulada cae bajo la banda de alerta. Hay que vigilar vencimientos día a día.",
        "sections": [
            {
                "title": "A — Qué significa",
                "body": (
                    "Liquidez AC/PC mide cuántas veces el activo corriente cubre el pasivo corriente. "
                    "Si baja de 1.20×, la financiera tiene poco margen para pagar obligaciones de corto plazo "
                    "sin vender cartera o pedir fondeo de emergencia."
                ),
            },
            {
                "title": "B — Qué hacer esta semana",
                "body": (
                    "Arme un calendario diario de entradas y salidas de efectivo: cupones a inversionistas, "
                    "vencimientos bancarios, retiros esperados y cobros de cartera. "
                    "Una sola persona debe consolidarlo cada mañana hasta pasar enero."
                ),
            },
            {
                "title": "C — Reglas simples",
                "body": (
                    "No originar crédito nuevo que empeore el descalce. "
                    "No contar como liquidez una línea bancaria que no se ha usado en los últimos 90 días. "
                    "Avisar al directorio si la liquidez proyectada a 7 días cae bajo 1.15×."
                ),
            },
        ],
    },
    "back-to-back-sep-oct": {
        "title": "Confirmar back-to-backs antes del 3 de noviembre",
        "summary": "Sep–oct son meses de preparación. Los cupos bancarios deben quedar probados, no solo firmados.",
        "sections": [
            {
                "title": "A — Por qué ahora",
                "body": (
                    "El escenario vivo incluye retiros de pasivas o menor disponibilidad interbancaria. "
                    "WCG financia inversiones y pagos con operaciones prenegociadas en banco "
                    "(depósito + préstamo, back-to-back). Esas líneas deben estar operativas antes de la tensión electoral."
                ),
            },
            {
                "title": "B — Checklist con el banco",
                "body": (
                    "1) Confirmar monto y plazo del back-to-back. "
                    "2) Hacer una operación de prueba pequeña. "
                    "3) Verificar que tesorería puede ejecutarla en el mismo día. "
                    "4) Tener contacto directo (no solo correo) con el oficial bancario."
                ),
            },
            {
                "title": "C — Qué no hacer",
                "body": (
                    "No asumir que un cupo aprobado en papel es liquidez real. "
                    "No esperar a noviembre para la primera prueba operativa."
                ),
            },
        ],
    },
    "descalce-fx": {
        "title": "Reducir descalce cambiario USD/GTQ",
        "summary": "Un shock cambiario golpea clientes en quetzales con deuda en dólares y encarece pasivos indexados.",
        "sections": [
            {
                "title": "A — Dónde está el riesgo",
                "body": (
                    "Clientes que importan o pagan en quetzales pero deben en dólares sufren si el tipo de cambio sube. "
                    "Parte del pasivo de WCG (AP/PG en dólares) también se encarece al depreciar el quetzal."
                ),
            },
            {
                "title": "B — Acciones concretas",
                "body": (
                    "Pausar nuevos créditos en dólares a quien no tenga ingresos en dólares documentados. "
                    "Exigir prueba de pago con TC +10% y +15%. "
                    "Revisar cobertura natural (exportadores, remesas) antes de renovar."
                ),
            },
            {
                "title": "C — Comunicación",
                "body": (
                    "Explique a clientes expuestos que el escenario no es predicción, pero la institución se protege. "
                    "Evite mensajes alarmistas; use cifras de su propio flujo de caja."
                ),
            },
        ],
    },
    "utilidad-crisis-cobranza": {
        "title": "Priorizar cobranza en ventana de crisis",
        "summary": "La utilidad acumulada nov–ene sale negativa en el escenario vivo. Cobrar antes de prestar.",
        "sections": [
            {
                "title": "A — Qué dice el número",
                "body": (
                    "Utilidad gerencial ya resta pagos a preferentes mes a mes. "
                    "Si además caen ingresos por mora o suben costos de fondeo, el margen no alcanza "
                    "y la utilidad del trimestre de crisis se vuelve negativa."
                ),
            },
            {
                "title": "B — Prioridades",
                "body": (
                    "1) Cobranza agresiva en cartera factoraje legacy. "
                    "2) Congelar bonos largos o posiciones especulativas. "
                    "3) Retrasar gastos discrecionales, no pagos a inversionistas sin plan."
                ),
            },
            {
                "title": "C — Factoraje en transición",
                "body": (
                    "La rampa con anclas puede seguir, pero con presupuesto explícito de utilidad negativa "
                    "en el corto plazo. No mezclar el costo del pivot con el shock macro."
                ),
            },
        ],
    },
    "preparacion-sep-oct": {
        "title": "Usar sep–oct como ventana de preparación",
        "summary": "Con los drivers actuales no hay alerta extrema, pero el calendario político exige disciplina.",
        "sections": [
            {
                "title": "A — Ventana de dos meses",
                "body": (
                    "Sepiembre y octubre no tienen shock en el modelo. Son el único tiempo para alinear "
                    "tesorería, probar bancos y revisar descalces antes del 3 de noviembre."
                ),
            },
            {
                "title": "B — Tareas mínimas",
                "body": (
                    "Actualizar mini balance y utilidades gerenciales cada cierre. "
                    "Simular retiros de pasivas con el escenario vivo moderado. "
                    "Documentar plan de comunicación a inversionistas."
                ),
            },
            {
                "title": "C — Después",
                "body": (
                    "A partir de noviembre el modelo activa stress parcial y luego pleno. "
                    "Lo preparado en sep–oct determina si la crisis es incómoda o peligrosa."
                ),
            },
        ],
    },
}


def get_precaution_article(slug: str) -> dict[str, Any] | None:
    return PRECAUTION_ARTICLES.get(slug)
