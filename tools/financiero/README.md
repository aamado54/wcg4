# Herramientas financiero (wcup2 / integración)

**Flujo integrado (usar):** [`../../integracion-eeff/README.md`](../../integracion-eeff/README.md)  
**Comando:** `manage.py refresh_estados_financieros` — implementación en `pipeline_integracion.py`.

| Módulo | Rol |
|--------|-----|
| `wcup2.py` | Consolida WC* mensuales → `wcout2d` |
| `merge_wcout.py` | Fusiona lote nuevo sobre merge-base |
| `rebuild_combined.py` | Histórico + reciente → JSON |
| `export_tabla.py` | Excel vaciado + tabla revisión (Datos/KPIs/Advertencias) |
| `pipeline_integracion.py` | Orquestación única |

Detalle wcup2: `wcup2.md`.
