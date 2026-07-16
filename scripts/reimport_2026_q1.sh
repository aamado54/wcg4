#!/usr/bin/env bash
set -e

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-${(%):-%x}}")/.." && pwd)"
DJANGO_DIR="$BASE_DIR/dashboard"

cd "$DJANGO_DIR"

echo "=== Reimportando PGC 2026-01 a 2026-03 ==="

echo
echo "1) Importar clientes nuevos..."
python manage.py import_clientes_nuevos --path "$BASE_DIR/data/clientes_nuevos/ClientesNuevos_2026-01-2026.csv"
python manage.py import_clientes_nuevos --path "$BASE_DIR/data/clientes_nuevos/ClientesNuevos_2026-02-2026.csv"
python manage.py import_clientes_nuevos --path "$BASE_DIR/data/clientes_nuevos/ClientesNuevos_2026-03_20260402.csv"

echo
echo "2) Importar estados de resultados (ingresos)..."
# OJO: sustituir IMPORT_ER_CMD por el nombre real de tu comando de importación de ER
ER_CMD="IMPORT_ER_CMD"

python manage.py "$ER_CMD" --path "$BASE_DIR/data/estados_financieros/WCF1 - Estado de resultados enero 2026.xlsx"
python manage.py "$ER_CMD" --path "$BASE_DIR/data/estados_financieros/WCF2 - Estado de resultados febrero 2026.xlsx"
python manage.py "$ER_CMD" --path "$BASE_DIR/data/estados_financieros/WCF3 - Estado de resultados marzo 2026.xlsx"

python manage.py "$ER_CMD" --path "$BASE_DIR/data/estados_financieros/WCI1 - Estado de resultados enero 2026.xlsx"
python manage.py "$ER_CMD" --path "$BASE_DIR/data/estados_financieros/WCI2 - Estado de resultados febrero 2026.xlsx"
python manage.py "$ER_CMD" --path "$BASE_DIR/data/estados_financieros/WCI3 - Estado de resultados marzo 2026.xlsx"

python manage.py "$ER_CMD" --path "$BASE_DIR/data/estados_financieros/WCL1 - Estado de resultados enero 2026.xlsx"
python manage.py "$ER_CMD" --path "$BASE_DIR/data/estados_financieros/WCL2 - Estado de resultados febrero 2026.xlsx"
python manage.py "$ER_CMD" --path "$BASE_DIR/data/estados_financieros/WCL3 - Estado de resultados marzo 2026.xlsx"

echo
echo "3) Importar venta cruzada (solo febrero 2026)..."
python manage.py import_venta_cruzada --path "$BASE_DIR/data/venta_cruzada/VentaCruzada_2026_02_202603172230-datos.tsv"

echo
echo "=== Reimportación completada. Verifica en el tablero y reportes. ==="
