# PGC: reglas permanentes de importación — clientes nuevos e inversiones

Fuente de verdad en código: `imports/new_client_rules.py`.

Todos los puntos que escriben o muestran `CLIENTES_NUEVOS` deben usar `aggregate_clientes_nuevos_counts()` (importador, admin, tablero PGC).

## Métrica CLIENTES_NUEVOS

### Insurance

Ninguna fila suma a la métrica (clientes propios del grupo WC).

### Investment

Solo filas con `ContratosPrevios = 0` y categoría en el CSV (`raw_une` / `raw_une_value`):

- `INVESTMENT - WC LEASING`
- `INVESTMENT - WORKING CAPITAL HOLDING GROUP` (WCHG)

No cuentan:

- `INVESTMENT - WC FACTORING` y otras categorías
- Cualquier fila cuyo NIT o nombre identifique entidad del grupo (WCF, WCL, WCI, WCS, WCHG) — ver `is_wc_group_entity()`

### Resto de UNE (Factoring, Leasing, …)

Filas con `ContratosPrevios = 0` y que no sean entidad del grupo WC.

### Deduplicación (todas las UNE)

Un cliente cuenta **una vez** por UNE y período, aunque tenga varias operaciones:

1. Clave principal: NIT normalizado (solo dígitos; se ignoran guiones y espacios).
2. Sin NIT: nombre normalizado.
3. Sin nombre: código de operación.

Implementación: `client_identity_key()` dentro de `aggregate_clientes_nuevos_counts()`.

## CSV Inversiones_crecimiento (AP/PG)

Comando: `import_inversiones_crecimiento`.

No se importan saldos cuyo `NumeroInversion` coincide con operaciones **intercompañía** del grupo WC detectadas en el histórico de clientes nuevos:

1. `intercompany_investment_operation_codes()` recorre `NewClientImportRow` con categoría de inversión y NIT/nombre de grupo.
2. `is_intercompany_investment_growth_row()` omite esas filas al cargar AP/PG.

Vuelva a importar clientes nuevos antes de inversiones si el archivo de crecimiento debe excluir operaciones nuevas.

## Comandos y pruebas

```bash
python manage.py import_clientes_nuevos --path /ruta/ClientesNuevos_....csv
python manage.py import_inversiones_crecimiento --path /ruta/Inversiones_crecimiento_....csv
python manage.py test imports.tests_new_client_rules
```

## Referencia operativa (sep-2026)

Conteo de verificación y notas OCR: `informe-clientes-nuevos-ocr-sep2026.md`.
