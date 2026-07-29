# User Guide — wcup2.py (consolidación estados financieros WCG)

## Qué cambió respecto a wcup1

| Tema | wcup1 | wcup2 |
|------|-------|-------|
| Directorio de entrada | `wcsource2512a` (u otro) | **`wcsource`** |
| Config | `wconfig11.txt` | **`wconfig12.txt`** |
| Nombres de archivo | `WCF BG 2401.xlsx` / variantes | Canónico **`WCF\|WCL\|WCI\|WCS-ER\|BG-yyMM.xlsx`** |
| Paso preliminar | No | **Renombrado** de nombres en español |
| Detección de columnas | 2 formatos fijos | Headers `NUMERO CUENTA` / `CUENTA`+`NOMBRE` / etc. |
| Salida | hoja única | hojas `meta` + `consolidado` |

## Formato canónico de archivos

```
{WCF|WCL|WCI|WCS}-{ER|BG}-{yyMM}.xlsx
```

Ejemplos:

- `WCI-ER-2606.xlsx` — Insurance, Estado de resultados, junio 2026
- `WCF-BG-2605.xlsx` — Factoraje, Balance general, mayo 2026

Reglas de renombrado desde el nombre exportado:

1. Ignorar prefijo `N.` + espacio (ej. `5. `).
2. Entidad: `WC` → **WCF**; preservar `WCL`, `WCI`, `WCS`.
3. Separador original ` - ` → `-` en canónico.
4. `Estado de resultados` → **ER**; `Balance general` → **BG**.
5. `junio 2026` → **2606**; `mayo 2026` → **2605** (yyMM).

## Configuración — `wconfig12.txt`

Tres líneas:

```
wcsource2512a.xlsx
~/download/wcg4/lectura_de_datos_al_modelo/wcsource
wcout2d.xlsx
```

1. Archivo de estructura (chart of accounts; una sola hoja).
2. Directorio de entrada **`wcsource`**.
3. Archivo Excel de salida.

## Formatos de hoja `Datos` admitidos

El valor numérico siempre se toma de la **última celda numérica** de la fila.

| Tipo | Headers típicos | acode | aname |
|------|-----------------|-------|-------|
| Legacy A | `CUENTA`, `NOMBRE`, `SALDOFIN` | CUENTA | NOMBRE |
| Legacy B | `GRUPO`, `CUENTA`, `NOMBRE`, …, `SALDOFIN` | CUENTA | NOMBRE |
| 2026 BG | `NUMERO CUENTA`, `CUENTA`, `SALDO FINAL` | NUMERO CUENTA | CUENTA |
| 2026 ER | `GRUPO`, `NUMERO CUENTA`, `CUENTA`, `TIPO`, `SALDO FINAL` | NUMERO CUENTA | CUENTA |

## Ejecución

```bash
cd ~/download/wcg4/lectura_de_datos_al_modelo
python wcup2.py                 # renombra + consolida
python wcup2.py --skip-rename   # solo consolida
python wcup2.py --rename-only   # solo renombra
```

Salida esperada (consola):

```
Files processed: 50/50
Detected periods: [2504, 2505, 2601, 2602, 2603, 2604, 2605, 2606]
Process completed. Output saved to: wcout2d.xlsx
```

## Salida `wcout2d.xlsx`

- **`meta`**: parámetros, períodos, formatos detectados, archivos omitidos.
- **`consolidado`**: columnas `businessid`, `acode`, `aname`, `newcode`, `nYYMM`…

  - `newcode=0`: cuentas de la estructura (orden y blancos preservados).
  - `newcode=1`: cuentas nuevas descubiertas en los archivos, agrupadas F→L→I→S.

Unidades: **quetzales completos** (como vienen en los Excel fuente).  
El histórico `wc-mod5c.xlsx` / hoja Datos está en **000 quetzales** — al combinar hay que alinear unidades (÷1000 o ×1000).

## Relación con el Balón de Riesgo (wcg4)

Esta importación es el **primer paso** del subsistema financiero en `risk/financiero/`:

1. Renombrar + consolidar (`wcup2`) → tabla reciente.
2. Combinar con histórico `wc-mod5c.xlsx` (pestaña Datos).
3. Reportes gerenciales (utilidad contable vs gerencial, índices, proyección alineada a qf).

Revisión: abrir `wcout2d.xlsx` y contrastar filas clave (activo, cartera, utilidades) por BU y período.
