# Informe: clientes nuevos e inversiones (sep-2026)

**Generado:** 2026-10-13  
**Ámbito:** reglas PGC, importadores `import_clientes_nuevos` e `import_inversiones_crecimiento`.

## Imagen `imagen.png` / OCR

| Búsqueda | Resultado |
|----------|-----------|
| `/home/caa/wc/**/imagen.png` | **No encontrado** |
| `/home/caa/wc/**/*imagen*` | Solo carpeta vacía de manuales (`manuales-usuario/imagenes`) |
| Assets de chat en `.cursor/projects/.../assets/` | **Sin PNG disponible** en el entorno actual |

**Conclusión:** no fue posible ejecutar OCR sobre `imagen.png`. Los criterios siguientes provienen del mensaje del usuario y del CSV `data/now/ClientesNuevos_2026-09_20261008.csv`.

## Referencia esperada (texto del usuario / imagen no disponible)

| Categoría | Identificaciones / notas |
|-----------|-------------------------|
| **Insurance** | 11339813-1, 1151283352 — **no cuentan** (clientes propios del grupo) |
| **Investment – WC Leasing** | 2339595, 6139035 + 1 fila sin identificación |
| **Investment – WCHG** | 1 fila sin identificación (ej. fideicomiso BI-BANK) |
| **Leasing operativo** | 475112-4, 5868494-8, 9209549-6 |

## Reglas implementadas en código (`imports/new_client_rules.py`)

1. **Insurance:** ninguna fila suma a la métrica `CLIENTES_NUEVOS`.
2. **Inversiones (clientes nuevos):** solo filas con `ContratosPrevios = 0` y categoría:
   - `INVESTMENT - WC LEASING`
   - `INVESTMENT - WORKING CAPITAL HOLDING GROUP` (WCHG)
   - Se **excluye** `INVESTMENT - WC FACTORING` y cualquier fila cuyo NIT/nombre sea entidad del grupo WC (WCF/WCL/WCI/WCS/WCHG).
3. **Todas las UNE (Leasing, Factoraje, Investment, etc.):** clientes únicos por NIT (o nombre / operación si no hay NIT); varias operaciones del mismo NIT cuentan **una vez**.
4. **CSV Inversiones_crecimiento:** no se importan saldos AP/PG cuyo `NumeroInversion` coincide con operaciones intercompañía detectadas en clientes nuevos (prestamos entre divisiones del grupo).

## Conteo de verificación con CSV sep-2026 (tras reglas)

Fuente: `ClientesNuevos_2026-09_20261008.csv`

| UNE | Conteo | Detalle |
|-----|--------|---------|
| Leasing | **3** clientes únicos | 475112-4, 9209549-6, 5868494-8 (7 contratos de Bodega Farmacéutica = 1 cliente) |
| Inversiones | **4** clientes únicos | PG02260901 (6139035), PG02260904 (sin NIT), PG02260903 (2339595), AP03260901 (WCHG / BI-BANK) |
| Insurance | **0** | Filas importadas pero excluidas del puntaje |
| Factoring | según CSV | Únicos por NIT con `ContratosPrevios = 0` |

Operaciones intercompañía detectadas para excluir en AP/PG: `AP01260904`, `AP01260701` (WCHG en vehículo Factoring Investment).

## Archivos modificados

- `imports/new_client_rules.py` — reglas compartidas
- `imports/management/commands/import_clientes_nuevos.py` — conteo al importar
- `imports/management/commands/import_inversiones_crecimiento.py` — filtro intercompañía
- `pgc/views.py` — tablero clientes nuevos (override Inversiones)
- `imports/tests_new_client_rules.py` — pruebas unitarias

## Próximo paso operativo

Reimportar en el entorno deseado:

```bash
python manage.py import_clientes_nuevos --path /ruta/ClientesNuevos_2026-09_....csv
python manage.py import_inversiones_crecimiento --path /ruta/Inversiones_crecimiento_2026_09.csv
```

Si dispone de `imagen.png`, colóquela en `data/now/imagen.png` para repetir OCR y contrastar NITs.
