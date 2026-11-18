# Reunión de hoy — Capturas PGO en wcg.lol

**Cuándo:** jueves 5 de noviembre de 2026  
**Con quién:** Celeste, Cindy y José (en ese orden)  
**Quién conduce:** Armando Amado  
**Para qué:** alinear qué datos alimentan el tablero PGO y cómo pasarlos al sistema de capturas manuales.

Este texto es la guía de conversación. No hace falta leerlo palabra por palabra; sirve para que todos entiendan el mismo mapa antes de abrir pantallas.

---

## Antes de sentarnos: el hilo de la reunión

El PGO mide cumplimiento con indicadores concretos. Parte de esos indicadores sale de archivos que ya maneja Sergio (CSV ArchivosPGO, carpetas, reportes). Otra parte **solo existe en el día a día** de Legal, Finanzas y Operaciones: fechas de formalización, líneas con acreedores, si el cronograma del mes se cumplió, cierre de reportes del día 7. Esas piezas **no siempre están en un solo archivo**. Por eso existe **Capturas manuales** en [wcg.lol](https://wcg.lol): formularios donde cada responsable declara lo que el tablero necesita, con historial y sin borrar versiones anteriores.

Hoy no vamos a pedir perfección en la primera vuelta. La idea es simple y en dos tiempos:

1. **Ustedes traen la información como ya la trabajan.** Puede ser una hoja electrónica, un Excel, una lista en correo, o papel que alguien transcriba. El formato lo eligen ustedes; lo importante es que los datos sean los mismos que usarían para responder “¿cumplimos este mes?”.

2. **La primera vez que esos datos entren al sistema, lo hace Armando contigo en pantalla** (o Armando los carga a partir de lo que compartas). Así vemos juntos campos, dudas y advertencias del sistema. **Después de esa primera ronda, ustedes entran solos** con su usuario y contraseña de wcg.lol, en horario de oficina, y guardan actualizaciones cuando corresponda.

Si la primera entrega sigue siendo Excel o papel un par de semanas, no hay problema. El tablero gana cuando el dato es confiable y repetible; el canal puede madurar paso a paso.

---

## Lo que todos deben saber (cinco minutos en común)

**Dónde entrar.** Sitio [https://wcg.lol](https://wcg.lol). Ruta **PGO → Capturas manuales** ([/pgo/capturas/](https://wcg.lol/pgo/capturas/)). También hay acceso desde el tablero PGO con el botón **Capturas manuales**.

**Horario para crear capturas nuevas.** De lunes a viernes, **9:00 a 18:00**, hora de Guatemala. Fuera de ese horario se puede **consultar historial**, pero no abrir una captura nueva. (En el futuro se quiere flexibilizar desde la red de Working Capital; hoy el servidor aún no lo aplica.)

**Mes en curso.** Por defecto el formulario asume el mes actual. Si guardan otro mes, el sistema lo acepta pero marca **advertencia** para revisión.

**Sin eliminar.** No hay botón de borrar. Cada **Guardar** es una **nueva versión** con nombre de usuario y fecha/hora. Para corregir, se edita y se guarda otra vez; la versión anterior queda en **Historial**. (Las versiones muy antiguas pueden tener *nota de cambio* en historial; los formularios actuales ya no piden ese campo.)

**Principios de datos.** Primero el dato que ustedes ya tienen (fechas, IDs, entregas). Totales o sugerencias del sistema son opcionales. Archivos de respaldo: Excel, PDF, texto, md, csv, tsv o Word — no otros formatos. Detalle: [`pgo-capturas-principios-datos.md`](pgo-capturas-principios-datos.md).

**Usuarios.** Los crea administración en wcg.lol. En el directorio PGO (`seed_pgo_staff`) ya están definidos contactos y usuarios previstos; hoy la reunión confirma quién captura qué, no sustituye a TI en altas de contraseña.

---

## 1. Celeste Eugenia Chacón Flores — Legal

**Contacto:** [cchacon@workingcapitalsa.com](mailto:cchacon@workingcapitalsa.com)  
**Usuario wcg.lol:** `Celeste` (en garantías mobiliarias también puede apoyar **Erick**).

Celeste, tu trabajo en capturas es el puente entre lo que Legal ya hace en operaciones y lo que el tablero PGO necesita medir en **garantías mobiliarias** y **contratos con bancos acreedores**. No estamos inventando un trámite nuevo: estamos **registrando en un solo lugar** lo que hoy vive en expedientes, correos o listas internas, para que el scorecard no dependa de buscar en mil carpetas.

En **Capturas manuales → Legal** verás **tres enlaces**. Dos son para **ingresar datos**; uno es **solo consulta**.

**Registro de garantías mobiliarias** — una captura por operación. Ahí va la UNE (Factoraje o Leasing), número de operación, y las fechas de formalización y de registro de la garantía. Este formulario alimenta **dos** indicadores a la vez: que el registro esté al 100 % y que formalización/registro cumplan la regla de **tres días hábiles** cuando aplique. Si hoy llevas eso en una tabla propia, tráela hoy; Armando puede ayudarte a pasar la primera fila juntos.

**Contratos con acreedores (−15 días)** — un guardado por **línea de crédito** relevante: acreedor, vencimiento, si ya está formalizado y fecha de formalización. El calendario fino lo han coordinado con Sergio; la captura es la declaración mensual o según acuerden, no sustituye el archivo fuente si ese sigue existiendo.

**Títulos y contratos de inversiones** — **pantalla de solo lectura**. El sistema asume **100 % cumplimiento desde otros sistemas**; **no** hay que llenar campos ahí. Sirve para verificar en reunión que el indicador cuadra con lo automatizado.

Lo que **no** es tarea de Celeste en capturas: **Actas del Comité de Créditos** — eso sigue en flujo/archivo de **Sergio** y hoy aparece como pendiente en el catálogo.

**Rutina cuando ya estés sola:** después de una operación o al cierre del día, entras, eliges el formulario, **Guardar**, y si algo cambió, corriges y guardas de nuevo. El **Historial** es tu respaldo si alguien pregunta “¿quién movió esta fecha?”.

### Referencia rápida — Celeste

| Qué | Tipo | Ruta en wcg.lol |
| :---- | :---- | :---- |
| Registro Garantías Mobiliarias | Captura (datos) | `/pgo/capturas/legal_garantias_registro/` |
| Contratos con acreedores (−15 días) | Captura (datos) | `/pgo/capturas/legal_contratos_acreedores_15d/` |
| Títulos y contratos inversiones | Solo consulta | `/pgo/capturas/legal_titulos_inversion/` |

---

## 2. Cindy Gabriela Samayoa Pérez — Finanzas y Riesgos

**Contacto:** [csamayoa@workingcapitalsa.com](mailto:csamayoa@workingcapitalsa.com)  
**Usuario previsto:** `csamayoa` (o `Cindy`, según asigne administración). En el directorio staff la autorización para capturas aún puede estar en **false** hasta que den de alta el usuario; hoy la reunión es sobre **qué datos** preparar, no solo sobre el clic final.

Cindy, tu área concentra indicadores de **análisis de casos**, **valuación de cartera** e **información a acreedores** con anticipación. Esos temas ya los trabajas con expedientes, planner de WCG Créditos, calendarios y archivos PGO. El sistema de capturas **todavía no tiene publicados** los tres formularios de Finanzas; en la pantalla de índice aparecen con badge **Pendiente**. Seremos claros: **no es que falte tu compromiso**, es que **Armando y tú hoy acuerdan campos mínimos** para que TI pueda activar cada pantalla cuando toque.

**Lo que viene (pendiente de formulario en wcg.lol):**

- **Análisis 100 % de casos en ≤ 10 días hábiles** — suele salir del expediente (inicio/fin) y del planner; hace falta definir IDs de caso, fechas hábiles, UNE y cumple/no cumple.

- **Plan de valuación anual de cartera al 100 %** — calendario versus archivo PGO y listado de empresas por mes; hay que alinear qué fila del cuadro equivale a qué guardado en pantalla.

- **Información a acreedores con tres meses de anticipación al vencimiento** — concepto en catálogo pendiente de definición contigo; en la guía técnica se menciona coordinación con José en Operaciones/Finanzas para cerrar criterio.

**Lo que ya no requiere captura manual tuya** (otros medios, DONE): carga analítica mensual (filas ArchivosPGO) e integraciones EEFF mensuales.

**Qué hacer ahora y en las próximas semanas:** sigue manteniendo tus archivos fuente como siempre. En esta reunión, dime qué columnas no puedes prescindir. Armando anota el mapa hoja → formulario. Cuando cada slug se active (`fr_analisis_10d`, `fr_valuacion_cartera`, `fr_info_acreedores_3m`), el flujo será el mismo que con Celeste: **primera carga acompañada**, luego **tú sola** en horario 9–18, mes en curso, correcciones como nuevas versiones.

### Referencia rápida — Cindy (estado en catálogo hoy)

| Concepto PGO | Formulario en sistema | Estado |
| :---- | :---- | :---- |
| Análisis casos ≤ 10 días hábiles | `fr_analisis_10d` | Pendiente — definición con Cindy |
| Plan valuación anual cartera | `fr_valuacion_cartera` | Pendiente — definición con Cindy |
| Info acreedores −3 meses | `fr_info_acreedores_3m` | Pendiente — definición con Cindy |

---

## 3. José — Operaciones (capturas en pantalla)

En la empresa hay más de un José. **Esta reunión, para capturas PGO en Operaciones, es con José Roberto Velásquez Pineda** — [jvelasquez@workingcapitalsa.com](mailto:jvelasquez@workingcapitalsa.com), usuario **`jvelasquez`** (también puede figurar como **`Jose`**). En el directorio staff está autorizado para capturas; su nota de rol dice Finanzas senior y **capturas de Operaciones: cronograma y reportes día 7**.

**José Augusto Martínez Ramírez** (TI, dirige TI y Finanzas) **no es el protagonista de esta sección**, pero conviene nombrarlo un minuto: en **Capturas manuales → Tecnología** existe **Cronograma proyectos TI**, donde se registra **avance en porcentaje** (0, 25, 50, 75, 100) por UNE. Eso **complementa** el sí/no que declara José Roberto en Operaciones; son dos preguntas del PGO sobre el mismo cronograma estratégico del CEO, con responsables distintos. Si Augusto no está en la sala, solo dejamos acordado que no se mezclen las dos pantallas.

**José Roberto**, tu objetivo en capturas es declarar cumplimiento del **cronograma de proyectos estratégicos** (lo acordado con CEO / SharePoint) y, cuando corresponda, el **cierre manual de reportes PGC/PGO del mes**, alineado a lo que Sergio refleja en CSV y carpetas.

**Cronograma proyectos estratégicos** (`op_cronograma_proyectos`) — **una captura por mes** (mes y año en curso). Por cada UNE — Factoraje, Leasing, Investment, Insurance — respondes si **cumple el cronograma** (sí o no). Si más adelante cambia el criterio en el mes, guardas de nuevo; queda historial. Trae hoy, si puedes, cómo lo llevas en SharePoint o en una hoja; la primera pasada puede ser contigo mirando la pantalla mientras Armando guarda, y la siguiente la haces tú.

**Reportes PGC/PGO día 7** (`op_reportes_pgc_pgo_7`) — **sí está en el catálogo e implementado**. Tabla de reportes esperados (p. ej. *Reporte Cierre WC*, *VoBo Comisiones Investments*). El sistema **sugiere fechas** según el último ArchivosPGO importado; **tú ajustas** la fecha de cumplimiento por reporte para que coincida con lo realmente entregado. Debe cuadrar con Sergio y con las carpetas del mes.

Otros temas de Operaciones (pago freelances día 7, dashboard jueves, gastos administrativos día 10) siguen **pendientes de definición con Sergio** en capturas; no son deuda de José Roberto en esta reunión salvo que quieras comentar dependencias.

**Rutina:** al cierre de mes, cronograma por UNE → Guardar. Antes del **día 7** del mes siguiente, captura de reportes alineada a entregables reales. Correcciones = nueva versión en Historial.

### Referencia rápida — José Roberto

| Formulario | Para qué | Ruta |
| :---- | :---- | :---- |
| Cronograma proyectos estratégicos | Sí/no cumplimiento por UNE, mensual | `/pgo/capturas/op_cronograma_proyectos/` |
| Reportes PGC/PGO día 7 | Cierre manual y fechas vs ArchivosPGO | `/pgo/capturas/op_reportes_pgc_pgo_7/` |

---

## Cierre de la reunión (Armando)

Repasar en voz alta:

- Qué archivo o formato trae cada persona **esta semana** para la primera carga asistida.
- Qué usuario wcg.lol queda asignado y quién crea la contraseña (TI / administración).
- Para Cindy: lista corta de **campos mínimos** por concepto pendiente y fecha orientativa de activación (sin prometer fechas de deploy que no estén en main).
- Para José Roberto: confirmar **mes de prueba** en cronograma y si el día 7 del mes actual ya tiene filas claras en reportes.
- Recordar: **Capturas manuales** no reemplaza el trabajo de Sergio con ArchivosPGO; **lo complementa** donde el dato nace en personas y fechas, no solo en nombres de archivo.

Gracias por abrir el proceso con paciencia. El tablero PGO solo refleja lo que declaramos con cuidado; esta reunión es para que declarar sea más fácil que perseguir el dato después.

---

## Apéndice — Contactos PGO (referencia)

| Persona | Rol en capturas | Usuario wcg.lol (referencia) |
| :---- | :---- | :---- |
| Celeste Chacón | Legal — 2 capturas + 1 consulta | `Celeste` |
| Cindy Samayoa | Finanzas — formularios pendientes | `csamayoa` |
| José Roberto Velásquez | Operaciones — cronograma y reportes día 7 | `jvelasquez` |
| Erick Sazo | Apoyo Legal garantías | `Erick` |
| Sergio Rodas | ArchivosPGO, TI backup NAS | `srodas` |
| José Augusto Martínez | TI — cronograma % (no esta sección Ops) | (según alta TI) |

*Documento para la reunión del 5 nov 2026. No sustituye `pgo-guias-capturas-personas.md` (detalle campo por campo).*
