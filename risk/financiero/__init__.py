"""Estados financieros institucionales — extensión del Balón de Riesgo.

Combina:
  - Importación reciente (wcup2 → wcout2d.xlsx)
  - Histórico wc-mod5c.xlsx (hoja Datos)
  - Extracto/proyección estilo qf (wc_mod5c_extract.json)

Unidades canónicas en reportes: **000 quetzales**.
"""

from .reports import build_financiero_board
from .reader import load_combined

__all__ = ["load_combined", "build_financiero_board"]
