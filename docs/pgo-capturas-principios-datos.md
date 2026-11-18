# PGO — Principios de datos en capturas manuales

Documento corto para colaboradores (Legal, Finanzas, Operaciones, TI). Alineado a `data/ref/PGO-.md` y a la reunión de capturas del 5 nov 2026.

---

## Los tres principios (Armando)

1. **Dato primario antes que derivado**  
   En pantalla, lo obligatorio son fechas, IDs y hechos que ustedes conocen en origen (expediente, contrato, entrega real). Totales, días calculados o fechas sugeridas por import son **opcionales** y van etiquetados como *Opcional — sustituto* o *Opcional — referencia derivada*. No sustituyen el campo primario.

2. **Formatos de archivo aceptables**  
   Si comparten archivos fuera del formulario (primera carga asistida, respaldo), usar solo: **Excel**, **PDF**, **texto**, **Markdown**, **CSV**, **TSV** o **Word**. No otros formatos de aplicaciones propietarias.

3. **Detalle causal cuando sea fácil**  
   Preferir filas concretas (una operación, una línea de crédito, un reporte del día 7) antes de un solo número agregado, cuando eso esté cerca de cómo ya reportan. Lo que **no** exige el PGO-.md queda **opcional** para el colaborador, con el mismo patrón primario + sustituto opcional.

---

## Cómo se ve en wcg.lol hoy

| Formulario | Primario (obligatorio) | Opcional (sustituto / derivado) |
| :---- | :---- | :---- |
| Registro garantías mobiliarias | UNE, ID operación, fechas formalización y registro | Referencia planner, mismo día de firma, caso en planner WCG Créditos |
| Contratos acreedores −15 días | Acreedor, vencimiento, formalizado, fecha realizada | Días de anticipación (calendario); si no se llenan, puede guardarse un cálculo auxiliar |
| Reportes PGC/PGO día 7 | Fecha de cumplimiento por cada uno de **6** reportes | Fecha sugerida desde import ArchivosPGO |

---

## Notas internas (TI)

- **`change_note`**: el modelo conserva el campo para versiones antiguas que incluyeron nota; los formularios actuales **no** lo muestran y guardan cadena vacía. No eliminar el campo salvo decisión explícita de migración.

---

*Complementa `pgo-guias-capturas-personas.md` y `pgo-reunion-capturas-conversacion.md`.*
