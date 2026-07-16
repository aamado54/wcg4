# Documento 2 – Especificación funcional V1
## WCG One – PGC + CRM + PGO + Balón de Riesgo

## 1. Objeto del documento

Este documento define la especificación funcional V1 de **WCG One**, la plataforma interna de Working Capital Group que integra en una misma base operativa los módulos **PGC**, **CRM**, **PGO** y **Balón de Riesgo**, compartiendo un núcleo común de entidades, contactos, productos, unidades de negocio y trazabilidad de cargas.[cite:14][cite:9]

Su propósito es traducir la memoria maestra y las decisiones ya tomadas a una definición funcional concreta: qué debe hacer cada módulo en esta etapa, qué pantallas debe mostrar, qué entradas y salidas se esperan, qué reglas mínimas deben aplicarse y qué temas quedan fuera del alcance de V1 para evitar dispersión.[cite:14][cite:9]

## 2. Alcance de V1

La V1 de WCG One debe ser una versión **presentable, usable y verificable** en un entorno interno de pocos usuarios, construida sobre un solo proyecto Django, una sola base de datos SQLite y módulos separados a nivel de app, no de proyecto.[cite:14][cite:9]

El alcance inmediato sí incluye: menú raíz WCG, convivencia con PGC existente, CRM mínimo funcional, Balón de Riesgo basado en snapshots operativos, PGO operativo basado en tickets, importaciones manuales desde archivos y dashboards básicos por módulo.[cite:14][cite:9][cite:11]

El alcance inmediato no incluye todavía: rediseño completo de PGC legacy, permisos finos por grupo y módulo, automatizaciones complejas con sistemas externos, modelado total de inversionistas/KYC, score avanzado de riesgo, ni implementación completa del PGO ponderado por todas sus reglas de negocio históricas.[cite:14][cite:9][cite:11]

## 3. Principios funcionales

La V1 debe respetar cinco principios funcionales: una sola fuente de verdad por dato, mínimo de pantallas por módulo, importaciones auditables, separación clara entre dato base y cálculo derivado, y facilidad de expansión sin rehacer el modelo.[cite:14][cite:9]

La experiencia del usuario debe ser simple: entrar al dashboard raíz, elegir módulo, consultar información útil y cargar archivos cuando corresponda, sin tener que entender la arquitectura técnica subyacente.[cite:9][cite:14]

## 4. Usuarios y uso esperado

En esta etapa se asume un uso interno por personal administrativo, operativo, comercial y gerencial, con autenticación única y acceso general a los módulos disponibles, aunque la documentación conceptual prevé que en fases posteriores cada usuario vea solo los módulos autorizados.[cite:9]

Los perfiles funcionales implícitos son al menos cuatro: gerencia, personal comercial/CRM, personal de riesgo/cobranza y personal operativo/tecnología para PGO, pero V1 no requiere todavía reglas sofisticadas de seguridad por perfil; basta con acceso autenticado y vistas estables.[cite:9][cite:14]

## 5. Estructura funcional general

WCG One debe funcionar como una plataforma con una pantalla inicial o dashboard principal en la ruta `/`, desde donde el usuario entra a cuatro dominios: **PGC**, **CRM**, **PGO** y **Balón de Riesgo**.[cite:14][cite:9]

Cada módulo debe tener entre tres y cinco vistas principales, suficientes para demostrar operación real con datos y apoyar conversación con negocio, sin intentar todavía cubrir todos los documentos históricos o todos los escenarios excepcionales.[cite:14][cite:9]

## 6. Dashboard raíz

### 6.1 Objetivo

El dashboard raíz debe ser la puerta de entrada única a WCG One y debe comunicar visualmente que el sistema ya integra cuatro frentes funcionales bajo una misma plataforma: PGC, CRM, PGO y Balón de Riesgo.[cite:14][cite:9]

### 6.2 Contenido mínimo

La pantalla debe mostrar, como mínimo:

- Tarjeta o acceso a **PGC**.
- Tarjeta o acceso a **CRM**.
- Tarjeta o acceso a **PGO**.
- Tarjeta o acceso a **Balón de Riesgo**.
- Navegación superior o lateral simple.
- Indicadores resumidos opcionales, si ya hay datos disponibles por seed o importación.[cite:14]

### 6.3 Criterios de aceptación

Se considerará funcional cuando un usuario autenticado pueda entrar a `/`, ver los cuatro módulos y navegar sin errores a `/crm/`, `/risk/`, `/pgo/` y `/pgc/`, mientras PGC legacy sigue accesible por sus rutas históricas como `/tablero/`.[cite:14]

## 7. Módulo CRM

### 7.1 Objetivo funcional

El CRM V1 debe consolidar un **maestro único de entidades** y permitir consultar la información básica relacional de clientes, prospectos y otros actores relevantes: contactos, productos asociados, interacciones y tareas de seguimiento.[cite:9][cite:14]

Este módulo no pretende todavía resolver toda la profundidad de un CRM corporativo, sino proveer una base operativa limpia y ampliable para que WCG deje de depender de listas dispersas y pueda relacionar clientes con productos y acciones comerciales o de seguimiento.[cite:9][cite:14]

### 7.2 Entidades funcionales del CRM

Las piezas funcionales mínimas del CRM V1 son:

| Entidad funcional | Propósito V1 |
|---|---|
| Entidad | Maestro principal de cliente/prospecto/tercero [cite:14][cite:9] |
| Contacto | Personas vinculadas a una entidad [cite:9] |
| Producto | Catálogo básico de productos WCG [cite:9] |
| Relación entidad-producto | Qué productos tiene o ha tenido una entidad [cite:9][cite:14] |
| Interacción | Registro de llamadas, reuniones, correos u otros contactos [cite:9] |
| Tarea | Seguimiento pendiente con responsable y fecha [cite:9][cite:14] |

### 7.3 Pantallas mínimas CRM

#### a) Lista de entidades – `/crm/`

Debe mostrar una tabla o listado de entidades importadas o creadas, con filtros básicos por texto y, cuando exista el dato, por tipo de entidad o unidad vinculada.[cite:9][cite:14]

**Datos visibles sugeridos:**

- Código.
- Nombre.
- Tipo.
- Identificador fiscal/NIT si existe.
- Unidad o segmento si existe.
- Estado.
- Cantidad de contactos.
- Cantidad de productos relacionados.[cite:9][cite:14]

**Acciones mínimas:**

- Buscar.
- Entrar al detalle.
- Acceder a importación de entidades.
- Acceder a importación de contactos.[cite:14]

#### b) Detalle de entidad – `/crm/entidades/<codigo>/`

Debe mostrar la ficha principal de la entidad y consolidar en una sola vista los bloques clave de relación comercial y seguimiento.[cite:9][cite:14]

**Bloques mínimos del detalle:**

- Datos generales de la entidad.
- Contactos.
- Productos relacionados.
- Interacciones recientes.
- Tareas abiertas o recientes.[cite:9][cite:14]

#### c) Nueva interacción – `/crm/entidades/<codigo>/interaccion/nueva/`

Debe permitir registrar una interacción simple asociada a la entidad, dejando al menos fecha, tipo/medio, usuario o responsable, resumen y observaciones.[cite:9]

#### d) Nueva tarea – `/crm/entidades/<codigo>/tarea/nueva/`

Debe permitir registrar una tarea o seguimiento asociado a la entidad, con asunto, responsable, fecha objetivo, estado y notas.[cite:9][cite:14]

#### e) Importación CRM – `/crm/importar/entidades/` y `/crm/importar/contactos/`

Debe permitir cargar archivos estandarizados para poblar entidades y contactos, registrando la carga en la bitácora correspondiente y evitando duplicaciones obvias.[cite:9][cite:14]

### 7.4 Reglas funcionales CRM

Las reglas mínimas del CRM V1 son estas:

- Cada entidad debe tener un identificador interno único; si existe un identificador fiscal confiable, debe usarse como apoyo de deduplicación y no como único criterio universal.[cite:9][cite:14]
- Debe evitarse crear duplicados evidentes cuando coincidan código, nombre o clave fiscal según el mapeo acordado para el archivo de entrada.[cite:9]
- Las interacciones y tareas deben quedar siempre ligadas a una entidad concreta.[cite:9]
- Los productos no deben duplicarse por cada entidad; deben vivir en catálogo y relacionarse mediante una tabla puente o relación equivalente.[cite:9]

### 7.5 Entradas y salidas CRM

**Entradas:**

- Archivo CSV inicial de clientes (`crm datos - InfoClientesWCG para CRM.csv`).[cite:14]
- Alta manual de interacción.
- Alta manual de tarea.
- Alta futura o ampliación de contactos/productos.[cite:9][cite:14]

**Salidas:**

- Lista de entidades.
- Ficha consolidada por entidad.
- Seguimiento manual utilizable en reuniones o gestión comercial.[cite:9]

### 7.6 Fuera de alcance CRM V1

Quedan fuera por ahora: campañas, embudos complejos, workflow automático, scoring comercial, jerarquías societarias avanzadas, KYC completo, módulos profundos de inversionistas y reportes analíticos sofisticados de conversión o pipeline.[cite:9][cite:14]

## 8. Módulo Balón de Riesgo

### 8.1 Objetivo funcional

El Balón de Riesgo V1 debe servir como **cuadro de alerta operativa temprana** apoyado primero en snapshots de operaciones, especialmente del archivo de leasing, para identificar situación por cliente, contrato, saldo, mora y días de atraso.[cite:5][cite:14][cite:9]

En esta fase el valor no está en modelar toda la teoría de riesgo, sino en capturar y consultar fotografías periódicas que permitan seguir evolución por operación y detectar comportamientos problemáticos o relevantes para análisis y cobranza.[cite:5][cite:14]

### 8.2 Fuentes y estructura funcional

La principal fuente de esta etapa es el archivo de leasing que incluye campos como cliente, contrato, asesor, producto, estado, fecha de registro o corte, renta mensual, saldo de capital, cuotas pendientes, saldo de interés, seguro, otros cargos, saldo vencido y días de atraso.[cite:5]

La especificación funcional adopta el enfoque de **snapshot acumulativo**, es decir, cada archivo o corte genera registros históricos y no sobrescribe la fotografía anterior de la operación, salvo que una regla explícita de negocio establezca otra cosa para ciertos procesos de consolidación.[cite:5][cite:14]

### 8.3 Pantallas mínimas Risk

#### a) Comando Balón – `/risk/`

Debe ser el dashboard operativo principal del módulo y presentar una vista resumida de operaciones o clientes con señales de atención.[cite:9][cite:14]

**Columnas mínimas a mostrar:**

- Cliente.
- Operación o contrato.
- Unidad o negocio.
- Producto.
- Estado.
- Saldo o capital balance.
- Días de atraso.
- Monto exigible o monto relevante para cobranza/seguimiento si ya está definido en el modelo.[cite:5][cite:14]

**Funciones mínimas:**

- Filtrar por cliente.
- Filtrar por estado o condición.
- Entrar al detalle de operación.
- Entrar al detalle de cliente si existe vista separada.[cite:14][cite:9]

#### b) Detalle cliente riesgo – `/risk/cliente/<codigo>/`

Debe consolidar, por entidad, las operaciones y snapshots vinculados, permitiendo ver de forma agrupada la exposición y su historia reciente.[cite:14][cite:9]

#### c) Detalle operación – `/risk/operacion/<pk>/`

Debe mostrar la operación individual y listar sus snapshots históricos en orden cronológico o inverso cronológico, para visualizar evolución de saldo, mora y demás campos relevantes.[cite:14][cite:5]

#### d) Importación risk – `/risk/importar/`

Debe permitir seleccionar y cargar el archivo fuente para snapshots y, cuando ya existan, otras clases de archivo como estados financieros, programación de pagos y pagos realizados.[cite:14][cite:9]

### 8.4 Reglas funcionales Risk

Las reglas funcionales mínimas son estas:

- El snapshot es histórico; no debe borrarse ni sustituirse sin justificación explícita.[cite:14][cite:5]
- La combinación de fecha de snapshot, operación y entidad debe funcionar como base natural de control contra duplicados en la práctica del importador.[cite:14]
- Deben persistirse los datos operativos relevantes que vienen en el archivo fuente, especialmente los que expresan estado de la operación y exposición al riesgo.[cite:5]
- Los cálculos analíticos complejos o scores agregados pueden quedar para una fase posterior si aún no hay regla de negocio estable.[cite:9][cite:14]

### 8.5 Entradas y salidas Risk

**Entradas:**

- Archivo `balon datos - Ejemplo de datos Riesgo al 31-mayo para una operacion - Base de datos Leasing.xlsx` como referencia estructural inicial.[cite:5]
- Futuras cargas de estados financieros, pagos programados, pagos realizados y bitácoras de cobranza.[cite:9]

**Salidas:**

- Comando Balón para consulta gerencial y operativa.[cite:9]
- Historial por operación.[cite:14][cite:5]
- Ficha de cliente con operaciones y señales básicas.[cite:14]

### 8.6 Fuera de alcance Risk V1

Quedan fuera por ahora: scoring cuantitativo integral, motor automático de alertas, conciliación plena con fuentes contables, proyecciones avanzadas, modelos estadísticos y toda la profundidad de análisis financiero expandido no indispensable para la primera presentación operativa.[cite:9][cite:14]

## 9. Módulo PGO

### 9.1 Objetivo funcional

El PGO V1 debe medir inicialmente la eficiencia operativa a partir de **tickets y tiempos de atención**, generando indicadores simples pero útiles por período, usuario o unidad, y dejando preparado el terreno para un modelo de puntuación más completo en una etapa posterior.[cite:14][cite:11][cite:1]

La documentación disponible demuestra que el PGO formal incluye pesos por unidad de negocio, reglas de cumplimiento y umbral de calificación, pero la forma más práctica de arrancarlo es usar el archivo de tickets como capa operativa base y construir sobre él resúmenes periódicos confiables.[cite:11][cite:1][cite:14]

### 9.2 Insumos funcionales del PGO

Los datos disponibles incluyen por lo menos un archivo de tickets y un ejemplo de análisis con puntajes y tablas por unidad, donde aparecen variables como usuario solicitante, correo, departamento, ID, tipo, título, estado, solución, fecha de cierre, fecha de apertura, prioridad, tipo de servicio, razón de cierre, sistema, duración y período año-mes.[cite:14][cite:1]

El documento de reglas del PGO fija, entre otras cosas, objetivos como análisis en 10 días hábiles, carga mensual de datos antes del día 7, cumplimiento del plan de valuación, helpdesk con tiempos de respuesta, total de 100 puntos por unidad y umbral satisfactorio de 80 puntos.[cite:11]

### 9.3 Pantallas mínimas PGO

#### a) Dashboard PGO – `/pgo/`

Debe mostrar indicadores agregados del período o de los últimos períodos, usando una tabla o resumen calculado a partir de tickets y, si ya existe el cálculo, de `PgoResultadoPeriodo` o su equivalente.[cite:14]

**Indicadores mínimos sugeridos:**

- Tickets recibidos.
- Tickets cerrados.
- Tickets abiertos.
- Tiempo promedio de atención o cierre.
- SLA cumplido.
- SLA incumplido.
- Resultado por período y unidad si ya fue calculado.[cite:14][cite:11][cite:1]

#### b) Lista de tickets – `/pgo/tickets/`

Debe permitir revisar tickets cargados con filtros básicos por estado, prioridad, período, departamento o unidad, y entrar al detalle del ticket.[cite:14]

#### c) Detalle ticket – `/pgo/tickets/<codigo>/`

Debe mostrar la ficha del ticket con sus datos operativos relevantes, incluyendo fechas, prioridad, estado, solicitante, unidad/departamento y duración si existe.[cite:14][cite:1]

#### d) Importación PGO – `/pgo/importar/`

Debe permitir cargar archivos de tickets y registrar la importación para auditoría y reproceso controlado.[cite:14]

#### e) Resúmenes por usuario y por unidad – `/pgo/resumen/usuario/` y `/pgo/resumen/unidad/`

Deben mostrar vistas agregadas que ayuden a la gerencia a leer desempeño operativo por responsable o por área.[cite:14]

### 9.4 Reglas funcionales PGO V1

Las reglas mínimas que sí deben operar en V1 son:

- Un ticket debe tener código o identificador único utilizable para matching de importación.[cite:14]
- Debe poder determinarse si un ticket está abierto, cerrado, rechazado u otro estado relevante según el archivo cargado.[cite:1][cite:14]
- Debe calcularse, cuando existan fechas suficientes, una duración o tiempo de atención/cierre.[cite:1][cite:14]
- Debe poder clasificarse cumplimiento básico de SLA con una regla simple y documentada, aunque luego cambie la regla fina por unidad o tipo.[cite:11][cite:14]
- Debe existir un resumen por período que consolide tickets recibidos, cerrados, tiempos y cumplimiento, incluso si el score ponderado total del PGO aún es parcial.[cite:11][cite:1][cite:14]

### 9.5 Entradas y salidas PGO

**Entradas:**

- `pgo datos - Archivos para PGO.csv`.[cite:14]
- `pgo datos - control de tickets marzo abril y mayo 2026 para PGO.xlsx`.[cite:14]
- `pgo ejemplo del analisis - PGO - TI Q22026.xlsx` como referencia de presentación y lectura del score.[cite:1][cite:14]
- `Reglas para el PGO - como se calcula y aplica.md` como fuente normativa inicial.[cite:11]

**Salidas:**

- Dashboard operativo de tickets.[cite:14]
- Resumen por período, usuario y unidad.[cite:14]
- Cálculo base para `PgoResultadoPeriodo` o estructura equivalente.[cite:14]

### 9.6 Fuera de alcance PGO V1

Quedan fuera por ahora: implementación completa de todas las ponderaciones del PGO formal, planner total por unidades, integración directa con Power Apps o SharePoint, cronogramas de proyectos no expresados en tickets y cálculo definitivo de la nota corporativa total del mes con todas las reglas maduras de negocio.[cite:11][cite:1][cite:14]

## 10. Módulo PGC dentro de WCG One

### 10.1 Objetivo funcional en esta etapa

PGC debe seguir operando como módulo existente y probado, mientras WCG One lo incorpora al menú y lo reconoce como uno de sus cuatro dominios funcionales principales.[cite:14]

### 10.2 Comportamiento esperado en V1

En V1 basta con que el usuario pueda entrar al acceso de PGC desde el shell WCG, llegar al home o placeholder del módulo y desde allí enlazarse a las rutas históricas activas de PGC, como tablero y administración mensual, sin alterar su lógica actual.[query]

### 10.3 Fuera de alcance PGC en esta etapa

No se debe tocar todavía:

- Lógica legacy de PGC.
- Rutas históricas como `/tablero/`.
- Administración mensual PGC.
- Unificación visual completa con `base_wcg.html`.[query]

## 11. Importaciones y bitácora de cargas

### 11.1 Propósito

Todas las cargas de V1 deben considerarse importaciones controladas, asociadas a archivo, fecha, módulo, resultado y observaciones, porque una parte importante del valor del sistema está en la trazabilidad del dato y no solo en la visualización.[cite:14][cite:9]

### 11.2 Reglas mínimas

Cada importación debe:

- Identificar módulo de destino.
- Conocer el archivo fuente.
- Registrar filas leídas, válidas y observadas cuando sea posible.
- Evitar duplicados evidentes según clave natural definida para la tabla de destino.
- Permitir reproceso controlado en caso de ajustes de mapping.[cite:14]

### 11.3 Importaciones incluidas en V1

| Módulo | Importaciones mínimas V1 |
|---|---|
| CRM | Entidades y contactos [cite:14][cite:9] |
| Risk | Snapshots operativos de leasing; opcionalmente pagos o EEFF si ya existe mapping estable [cite:5][cite:9] |
| PGO | Tickets y archivos de soporte al cálculo base [cite:14][cite:11][cite:1] |

## 12. Datos demo y seed

Para efectos de presentación y validación funcional, debe existir un mecanismo de datos demo que permita que `/`, `/crm/`, `/risk/` y `/pgo/` muestren contenido útil aun sin haber cargado aún archivos productivos definitivos.[query]

Esto es coherente con la necesidad práctica de demostración en corto plazo y no contradice el modelo general, siempre que los datos demo se distingan claramente del dato de producción o al menos se entiendan como semilla de entorno de prueba.[query]

## 13. Reglas de navegación y usabilidad

La navegación de V1 debe ser consistente: desde el shell WCG se debe poder entrar a cada módulo y volver fácilmente al inicio, manteniendo nomenclatura clara y páginas con enfoque operativo, no excesivamente técnico.[cite:14][cite:9]

Las pantallas deben priorizar tablas legibles, formularios simples, pocos filtros útiles y enlaces claros a detalle, en vez de interfaces recargadas o múltiples variantes de reporte que todavía no agregan valor demostrable.[cite:14][cite:9]

## 14. Criterios de aceptación por módulo

### CRM

Se considera aceptado si:

- Lista entidades importadas o sembradas.[cite:14]
- Permite ver detalle por entidad.[cite:14][cite:9]
- Muestra contactos, productos, interacciones y tareas de forma coherente.[cite:9][cite:14]
- Permite registrar al menos una interacción y una tarea.[cite:9]

### Risk

Se considera aceptado si:

- El Comando Balón muestra operaciones reales o demo.[cite:14][cite:5]
- Puede verse cliente, operación, saldo, días de atraso y monto exigible o equivalente.[cite:14][cite:5]
- Puede consultarse historial por operación.[cite:14]
- Puede importarse al menos el archivo base de leasing o su equivalente estructural.[cite:5][cite:14]

### PGO

Se considera aceptado si:

- Puede cargarse un conjunto de tickets.[cite:14]
- Existe lista y detalle de tickets.[cite:14]
- Se genera un resumen por período con tickets recibidos, cerrados y duración promedio.[cite:14][cite:1]
- Existe lectura básica de cumplimiento o incumplimiento de SLA.[cite:11][cite:14]

### Dashboard raíz

Se considera aceptado si:

- Presenta los cuatro módulos.[cite:14][cite:9]
- Navega sin error a cada módulo nuevo.[cite:14]
- Convive con PGC legacy sin romper sus rutas históricas.[query]

## 15. Pendientes explícitos

Quedan pendientes explícitos para documentos o iteraciones posteriores:

- Definir con precisión de negocio las claves naturales finales de cada importador.[cite:14]
- Cerrar mapping productivo de todos los archivos reales de PGO y CRM, además del ya entendible archivo de leasing.[cite:14][cite:5]
- Definir permisos por módulo y perfil.[cite:9]
- Integrar PGC al maestro común sin tocar su operación actual antes de tiempo.[query][cite:14]
- Cerrar la versión V1.1 del score PGO ponderado por unidad.[cite:11][cite:1]

## 16. Decisiones cerradas para Cursor y desarrollo

Este documento deja cerradas para el desarrollo V1 las siguientes decisiones funcionales:

- WCG One se desarrolla sobre el estado actual del proyecto y no como sistema nuevo paralelo.[query]
- La arquitectura funcional es de una sola plataforma con cuatro módulos.[cite:14][cite:9]
- CRM se enfoca en maestro de entidades y seguimiento básico.[cite:9][cite:14]
- Risk se enfoca primero en snapshots operativos e historial por operación.[cite:5][cite:14]
- PGO se enfoca primero en tickets, tiempos y resumen por período.[cite:11][cite:1][cite:14]
- PGC se preserva y se integra gradualmente sin reescritura ahora.[query][cite:14]

## 17. Próximo documento recomendado

El siguiente documento natural después de esta especificación funcional es el **Documento 3 – Especificación técnica Django**, donde esta funcionalidad debe aterrizarse a modelos, relaciones, URLs, vistas, servicios de importación, comandos de seed, reglas de cálculo y criterios técnicos de despliegue sobre `~/wc/pgc1/dashboard`.[cite:14][cite:9]
