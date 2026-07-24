"""Evaluación financiera de clientes (Altman / Carátula) — extensión aislada del Balón.

Fuente inicial: plantilla Excel `WCG-evaluacion-riesgo-clientes-2025.xlsx`
(sheets Caratula, Altman, Balance, Resultados). No altera snapshots ni reportes
operativos existentes.

Costura para importación formal (sin reescribir la vista):
    dataset = load_evaluacion()                      # path default / settings
    dataset = load_evaluacion(path="/ruta/plantilla.xlsx")
    dataset = load_evaluacion(uploaded_file=request.FILES["plantilla"])
    portfolio = build_portfolio_view(dataset)
La vista solo consume `build_portfolio_view` + `EvaluacionDataset`; el origen
del archivo puede cambiar sin tocar el template.
"""

from .portfolio import build_portfolio_view
from .reader import load_evaluacion

__all__ = ["load_evaluacion", "build_portfolio_view"]
