# Alcance real: precisión monetaria y auditoría de importaciones

**Fecha:** 2026-11-18 (actualizado tras barrido completo)  
**Cierre detallado:** `docs/PRECISION-AUDIT-COMPLETION-20261118.md`

---

## Cobertura global (%)

| Eje | % |
|-----|---|
| Precisión ledger (apps activas) | **~92%** |
| Hub dispatch audit | **100%** (11/11 tipos) |
| CLI `import_*` mixin (catálogo) | **83%** (10/12; excl. orquestadores) |
| UI auditoría staff | **100%** |

---

## Qué está hecho

### Precisión monetaria

| Área | Estado |
|------|--------|
| `core.money_precision` + tests | Hecho |
| PGC metas / ingresos / investment / bancos | 6 dec (migraciones previas + CLI) |
| **Risk** saldos / montos / exposición | **6 dec** (`risk.0004`) + `pick_money_decimal` |
| **NewClientImportRow.amount** | **6 dec** (`imports.0013`) |
| **PGO scorecard cache** celdas | **Decimal 6 dec** (`pgo.0008`) |
| Objetivos / metas CLI | `quantize_store` en parse |

### Auditoría

| Capa | Cobertura |
|------|-----------|
| `run_import` → `_audit_after_dispatch` | 11 tipos CRM/PGO/Risk/PGC |
| Mixin CLI | 10 comandos (ver `audit_cli_registry.py`) |
| Admin mensual + legacy PGC views | Hecho |
| UI `/importaciones/auditoria/` | Hecho |
| `audit_import_status` | `--detailed`, `--checklist`, `--path`, `--coverage` |
| Tests | `imports/tests_import_audit.py`, `core/tests_money_precision.py` |

---

## Qué sigue diferido (consciente)

| Ítem | Razón |
|------|--------|
| `apps/*` legacy duplicados | No en rutas activas |
| gerencia `FloatField` | Escenarios, no ledger |
| `import_wcg_data` / `load_wcg_data` audit | Orquestadores |
| manifest ↔ eventos automático | Fase ops manual |
| Wipe PGC prod | Post-recarga usuario |

---

## Inventario FloatField (apps activas)

```
gerencia/models.py  — 8 campos tasas/crecimiento (escenario)
(pgo scorecard Float eliminado → Decimal en 0008)
```

## Inventario money 2 dec restante

```
pgo/models.py     tiempo_promedio_horas, cumplimiento_sla_pct (SLA KPI)
apps/*            legacy sin migrar
```

---

## Referencias

- Checklist decimales: `wcg4/docs/precision-audit-checklist.md`
- Gap histórico F1: `docs/import-audit-gap-phase2-20261118.md` (hooks F2 ahora mayormente cerrados)
- Commit alcance PGC original: `4da4d65`