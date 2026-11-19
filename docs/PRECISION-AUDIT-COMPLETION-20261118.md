# Precisión monetaria y auditoría de importaciones — cierre 2026-11-18

**Repo:** `dashboard/` (wcg4)  
**Alcance:** barrido integral apps activas (`pgc`, `pgo`, `imports`, `core`, `risk`, hub `gerencia`/`config`/`wcgone`/`apps/*` legacy)  
**Sin commit / sin push** (solicitud del operador).

---

## Resumen ejecutivo

| Eje | Cobertura | Nota |
|-----|-----------|------|
| Precisión ledger / montos USD-GTQ | **~92%** módulos con dinero en rutas activas | Ver tabla módulos |
| Auditoría `ImportAuditEvent` hub dispatch | **100%** (11 tipos) | `run_import` + `_audit_after_dispatch` |
| Auditoría CLI `import_*` con mixin | **10/12 = 83%** catalogados | Excluye orquestadores demo |
| UI staff auditoría | **100%** lista + detalle + hub | Tests en `tests_import_audit` |
| `audit_import_status` | **100%** detailed, checklist, path, **--coverage** | |
| Migraciones nuevas (seguras widen) | `risk.0004`, `imports.0013`, `pgo.0008` | No borran histórico |

---

## Precisión — 100% (hecho)

| Módulo | Qué |
|--------|-----|
| **core** | `money_precision`, `pick_money_decimal` en `column_map` |
| **pgc** | Metas/ingresos 6 dec (previo + `quantize` en objetivos/metas CLI) |
| **imports** | Investment/bancos 6 dec (0010–0012); `NewClientImportRow.amount` → 6 dec (0013); montos en CLI clientes nuevos |
| **risk** | Todos los `Decimal` de saldo/monto/exposición → 6 dec + `pick_money_decimal` en `risk/services.py` |
| **pgo** | `PgoScorecardCell.points` / `max_points` → `Decimal(6)` + cuantización al persistir caché |
| **pgc/paths** | `import_pgc_objetivos`, comisiones TSV vía `income_conversion` / `quantize_store` en `_cell_decimal` |

### Cobertura por app (% aproximado del inventario monetario activo)

| App | % | Comentario |
|-----|---|------------|
| pgc | **100%** | Modelos migrados + calculate/save en ingresos/objetivos/recalc |
| imports | **95%** | Filas fuente + investment + clientes; detection usa `float` solo para scores de confianza (no ledger) |
| risk | **100%** | Modelos dashboard `risk/` + import batch |
| pgo | **90%** | Montos tablero en Decimal; SLA horas/% siguen 2 dec (métricas operativas, no dinero) |
| gerencia | **N/A ledger** | 8× `FloatField` escenario what-if — sin migración (parámetros, no contabilidad) |
| apps/core, apps/risk, apps/pgo | **0% migración** | Legacy duplicado; rutas prod usan apps top-level |
| wcgone / config | **N/A** | Sin campos money en código Python activo revisado |

---

## Precisión — diferido con razón

| Ítem | Razón |
|------|--------|
| **apps/** legacy `decimal_places=2` | Duplicados históricos; no referenciados por dispatch ni admin activo |
| **gerencia** `FloatField` tasas | Escenarios gerenciales, no ledger PGC |
| **pgo** `tiempo_promedio_horas`, `cumplimiento_sla_pct` | KPI tiempo/% (2 dec suficiente) |
| **risk/evaluacion/** `float()` en Excel Altman | Métricas índice / lectura plantilla; no persiste montos contrato |
| **Wipe / backfill PGC prod** | Solo tras recarga explícita del usuario (fuera de este barrido) |

---

## Auditoría — 100% (hecho)

1. **Hub:** los 11 tipos en `DISPATCH_IMPORT_TIPOS` pasan por `run_import` → `_audit_after_dispatch`.
2. **PGC admin / legacy views:** `record_import_audit_for_path` + `suppress` en re-dispatch CLI (sin duplicados).
3. **CLI mixin** añadido en: `import_ingresos_comisiones_tsv`, `import_pgc_objetivos`, `import_pgc_objetivos_tsv`, `import_pgc_metas`, `import_archivos_pgo_file`, `import_estados_financieros` (+ 5 imports previos).
4. **Mixin** acepta `--path`, `--source-dir`, `--file`.
5. **UI:** `/importaciones/auditoria/` lista (filtros) + detalle + historial misma ruta.
6. **Ops:** `audit_import_status --checklist`, `--coverage`, `--path`, `--since`, `--fail-only`.
7. **Registry:** `imports/audit_cli_registry.py` documenta cobertura.

### Auditoría — diferido

| Ítem | Razón |
|------|--------|
| `import_wcg_data`, `load_wcg_data` | Orquestadores / demo; sin archivo único trazable |
| Cruce automático `manifest.json` ↔ eventos | Manual vía `--path` + layout `data/` |
| `recalc_*`, `pgc_operational_regression` | No son import de archivo; opcional futuro `detail_json` ops |

---

## Layout data / reclasificación

- Referencia **8c62fe8d** no aparece en el repo; no hay tarea pendiente nombrada con ese id.
- **Reclasificación layout** (`apply_data_layout_moves`): comandos presentes; **default dry-run**. Aplicación en disco queda al operador (nota en `RELEASE-BLOCK-20261118.md`).

---

## Migraciones a aplicar en entornos

```text
risk.0004_risk_money_precision
imports.0013_newclient_amount_precision
pgo.0008_scorecard_cell_decimal_precision
```

(junto con `pgc.0009`, `imports.0011`–`0012` ya documentadas)

---

## Verificación

```bash
cd dashboard
.venv/bin/python manage.py test imports pgc core pgo risk -v1
.venv/bin/python manage.py audit_import_status --coverage
.venv/bin/python manage.py audit_import_status --checklist
```

**Resultado 2026-11-18:** `144` tests ejecutados — **4 fallos preexistentes** en `risk` (financiero vistas 302 sin permiso fixture; evaluación plantillas sin archivos demo en CI). **17/17** OK en `imports.tests_import_audit` + `core.tests_money_precision`. Migraciones nuevas aplican limpio en BD de test.

---

## Archivos clave tocados

- `core/services/column_map.py` — `pick_money_decimal`
- `risk/models.py`, `risk/services.py`, `risk/migrations/0004_*`
- `imports/models.py`, `imports/migrations/0013_*`
- `pgo/models.py`, `pgo/scorecard_cache.py`, `pgo/migrations/0008_*`
- `imports/audit_cli_registry.py`, `audit_import_status.py`, comandos `import_*` extendidos
- `docs/precision-and-audit-scope-20261118.md` — % actualizados