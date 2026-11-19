# Brechas auditoría y precisión — Fase 2 (hooks, no bloquea release PGC)

**Fecha:** 2026-11-18  
**Relación:** `precision-and-audit-scope-20261118.md`, `import-audit-verification-20261118.md` (repo padre)

## Alcance Fase 1 (listo para cierre PGC)

| Ruta | `ImportAuditEvent` |
|------|-------------------|
| Hub `run_import` / `_audit_after_dispatch` | Sí (`manual` / `ops`) |
| Admin mensual PGC `_process_upload` (clientes, cruzada, ER) | Sí + `suppress` en CLI |
| Legacy `process_new_clients` / `process_cross_sale` | Sí |
| CLI `import_clientes_nuevos`, `import_venta_cruzada`, `import_ingresos`, `import_inversiones_crecimiento`, `import_bancos_fin_mes` | Sí (`ImportAuditCommandMixin`) |
| UI staff lista/detalle `/importaciones/auditoria/` | Sí |
| `audit_import_status --detailed\|--checklist\|--path` | Sí |

**Inversiones AP/PG y bancos:** solo vía hub general o CLI con mixin (no bloque admin mensual de ingresos ER).

## Fase 2 — sin implementar (planificar antes de ampliar CRM/PGO/Risk)

### Auditoría

| Hook | Notas |
|------|-------|
| Comandos PGO (`import_*` sueltos, capturas) | Solo batch CRM vía hub hoy; repetir patrón mixin |
| Comandos Risk / leasing / rentas CLI | Idem |
| `import_pgc_objetivos`, `import_pgc_metas` | Carga Excel metas; alto impacto — audit + suppress si llama otros imports |
| `import_ingresos_comisiones_tsv` | TSV auxiliar; registrar `import_tipo` dedicado |
| `recalc_*` / `pgc_operational_regression` | No son import de archivo; opcional `detail_json` ops |
| Cruce `data/pgc/YYMM/manifest.json` ↔ eventos | Manual: `--path` + inventario layout |

### Precisión monetaria

| Módulo | Campos | Acción Fase 2 |
|--------|--------|---------------|
| **PGO** | `PgoScorecardCache.points`, `max_points` (`FloatField`) | Evaluar `Decimal` + backfill si puntos pasan a reporte financiero |
| **Risk** | `saldo_total`, `exposicion`, montos leasing | Migración 4–6 dec + script comparación snapshots |
| **Gerencia** | tasas `FloatField` | Mantener (escenarios, no ledger) |
| Filas fuente imports | `NewClientImportRow.amount` (2 dec) | Canónico ya en PGC/Investment 6 dec donde aplica |

### Layout `data/`

- **YYMM solo** en `pgc/`, `pgo/`, `ger/`, `pla/` (`YYMM_MODULES` en `core/services/data_layout.py`).
- `pla/` usa `otros/` sin período cuando no hay YYMM.
- `dudas/` **sin** subcarpetas YYMM (cola plana o `dudas/otros/`).
- Comandos: `scaffold_data_layout`, `inventory_data_layout`, `apply_data_layout_moves` (`--dry-run` default).

## Criterio de entrada Fase 2

1. Recarga PGC prod validada con migraciones `pgc.0009`, `imports.0012`.
2. Un cierre mensual real usando UI auditoría + `--checklist` sin FAIL no explicados.
3. Decisión explícita sobre backfill Risk/PGO con usuarios de reportes históricos.