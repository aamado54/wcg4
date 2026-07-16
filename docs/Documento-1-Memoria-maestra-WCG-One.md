## Documento 1

A continuación te dejo el texto ya redactado, en formato que puedes usar como **Memoria maestra**.

***

# Documento 1 – Memoria maestra

## WCG One – Implementación 2 de PGO + CRM + Balón de Riesgo sobre PGC existente

### 1. Propósito del documento

Este documento constituye la memoria maestra de referencia para la evolución de **WCG One**, entendido como el sistema integrado de Working Capital Group que reúne en una sola plataforma los módulos **PGC**, **CRM**, **PGO** y **Balón de Riesgo**, compartiendo un mismo modelo maestro de datos y una única base operativa.[^1][^2]

Su función es dejar asentado, en un solo lugar, el contexto histórico, las decisiones ya tomadas, el estado actual real del sistema, los criterios de diseño que se adoptan para esta etapa, las dudas aún abiertas y la dirección recomendada para continuar con el desarrollo sin perder consistencia entre conversaciones, documentos y código.[^2][^1]

### 2. Contexto de origen

Durante febrero se definió la necesidad de construir aplicaciones internas para WCG que soportaran, al menos, **PGC**, **CRM** y **Balón de Riesgo**, y posteriormente también **PGO**, con una visión de plataforma integrada más que de sistemas aislados.[^1][^2]
En una primera fase se construyó una estructura amplia y completa de base de datos para varios módulos, pero esa primera base quedó como esqueleto conceptual y no será la base operativa de esta etapa, aunque conserva valor como referencia de alcance futuro.[^2][^1]

Después se desarrolló y completó **PGC** en otra estructura, actualmente ubicada en `~/wc/pgc1/dashboard`, y ese producto es hoy el componente funcional más maduro del ecosistema.[^2]
Más adelante se recibieron archivos reales o parciales para una primera versión práctica de **CRM**, **PGO** y **Balón de Riesgo**, y se observó que el volumen de datos disponibles para esta etapa es menor que el previsto en las estructuras amplias iniciales, por lo que se adoptó un enfoque V1 más pragmático, incremental y apoyado en importaciones por archivo.[^1][^2]

### 3. Decisión arquitectónica principal

La decisión arquitectónica central ya adoptada es que **WCG One debe operar como un solo proyecto Django, con una sola base de datos y varios módulos internos**, y no como varios proyectos Django independientes conectados a una misma base ni como varias bases por subsistema.[^1][^2]
Esta decisión responde tanto a criterios de velocidad de implementación como a la necesidad de evitar duplicación de datos, reducir complejidad técnica y mantener una visión tipo datamart donde la información exista una sola vez y pueda ser usada desde distintas vistas de negocio.[^2][^1]

La arquitectura conceptual aprobada es la de un núcleo común con maestros compartidos —entidades, contactos, productos, relaciones, unidades y diccionario de datos— y varios módulos especializados que leen y extienden ese núcleo: `crm`, `risk`, `pgo` y `pgc`.[^1][^2]
PGC, por su estado de avance, no se reescribe ahora; convive temporalmente con el shell WCG One y conserva sus rutas históricas mientras se completa la integración funcional y posteriormente la integración visual.[^2]

### 4. Estado actual real del sistema

El estado real auditado de WCG One V1 se ubica en `~/wc/pgc1/dashboard`, con proyecto Django `config/`, base de datos SQLite local y apps internas en raíz: `core`, `portal`, `crm`, `risk`, `pgo`, `pgc`, además de componentes legacy asociados a PGC. [query]
La arquitectura real no usa proyecto `wcgone/` ni subcarpeta `apps/`; usa una organización pragmática sobre el repositorio existente, manteniendo PGC dentro del mismo árbol de proyecto. [query]

La pantalla raíz `/` ya no es el splash anterior sino un dashboard WCG con menú principal, y existen rutas funcionales para `/crm/`, `/risk/`, `/pgo/`, `/pgc/` y también para rutas históricas de PGC como `/tablero/` y otras asociadas al módulo legacy. [query]
La autenticación es única, basada en login estándar de Django, con `LOGIN_REDIRECT_URL = '/'`, y en V1 todavía no se han implementado permisos finos por grupo o por módulo. [query]

### 5. Núcleo común de datos

El núcleo común implementado en `core/wcg_models.py` contiene, al menos, las entidades funcionales base: `UnidadNegocio`, `Entidad`, `Contacto`, `Producto`, `RelacionEntidadProducto`, `DataDictionary` y `DataImportBatch`. [query]
Este núcleo es coherente con la documentación histórica de WCG3, que definía un maestro único de entidades, contactos y productos como columna vertebral para CRM, riesgo y demás vistas operativas.[^1][^2]

La tabla `Entidad` representa el maestro de clientes y prospectos y debe consolidarse como referencia canónica para CRM, riesgo y, cuando corresponda, integración posterior con PGC. [query][^1]
La tabla `DataDictionary` expresa una decisión importante: que cada variable relevante pueda documentarse formalmente en cuanto a nombre, ubicación, tipo, uso, fuente y significado, alineándose con la visión explícita del usuario de operar con lógica de datamart y catálogo auditable de información. [query][^2]

### 6. Alcance funcional por módulo en esta etapa

#### 6.1 CRM

El alcance V1 de CRM es deliberadamente mínimo pero útil: lista de entidades, detalle de entidad, contactos, productos relacionados, interacciones y tareas.[^2][^1]
Esto coincide con la definición previa de WCG3, donde CRM debía iniciar con filtros básicos, vista de detalle, productos vigentes y seguimiento simple, dejando para fases posteriores ampliaciones como estructuras más profundas de inversionistas, KYC o modelos extensos por tipo de entidad.[^1][^2]

El archivo inicial de CRM —`crm datos - InfoClientesWCG para CRM.csv`— se asume como punto de partida válido para poblar el maestro, enriquecerlo gradualmente y preparar el sistema para agregar más campos conforme madure el uso.[^2]
La regla conceptual clave es evitar duplicidades y consolidar un maestro único, idealmente con una clave de entidad consistente y luego enriquecido con identificadores fiscales u otros criterios de deduplicación.[^1][^2]

#### 6.2 Balón de Riesgo

La orientación funcional aprobada para esta etapa del Balón de Riesgo es comenzar por **snapshots operativos por operación**, en vez de intentar desde el inicio todo el universo de riesgo.[^2][^1]
El archivo de leasing disponible demuestra claramente el valor de este enfoque, porque contiene contrato, cliente, producto, estado, fecha de corte, renta mensual, saldo de capital, cuotas pendientes, intereses, seguros, otros cargos, saldo vencido y días de atraso, todo lo cual permite medir señales tempranas de deterioro operativo.[^3]

El valor estratégico del balón en esta fase no es todavía el scoring integral de riesgo, sino la acumulación de una serie histórica auditable de “fotografías” de operaciones para ver evolución, mora, comportamiento de pago y alertas prácticas de seguimiento.[^3][^1][^2]
Este enfoque está alineado con la documentación histórica que definía el Comando Balón como un cuadro gerencial actualizado y que priorizaba casos vigentes, cobranza operativa, pagos y estados financieros estructurados como base de control.[^1]

#### 6.3 PGO

El PGO se considera el módulo más incierto conceptualmente, por mezclar datos operativos de tickets con reglas de puntuación y evaluación por unidad de negocio.[^4][^2]
Por ello se adoptó una estrategia en dos niveles: primero construir un **PGO operativo** con tickets, tiempos y cumplimiento básico, y después superponer el modelo de puntos y ponderaciones más fiel a las reglas del negocio.[^2]

Las reglas documentadas muestran claramente que el PGO no es solo helpdesk; incorpora también cumplimiento de análisis, valuación, cargas de información analítica y medición por unidad con puntajes totales de 100 y umbral de clasificación satisfactoria de 80.[^5][^4]
Sin embargo, para V1 el eje computable más inmediato es el de tickets: recibidos, cerrados, duración, cumplimiento o incumplimiento de SLA, abiertos remanentes y agrupación por período, usuario o unidad.[^5][^2]

#### 6.4 PGC

PGC es el módulo más avanzado en código y operación, y por lo tanto su tratamiento en esta fase es de convivencia e integración progresiva, no de rediseño.[^2]
Debe preservarse intacto en sus rutas históricas y lógica actual, mientras WCG One lo incorpora al menú común y prepara el terreno para sincronizar maestros, poblar `UnidadNegocio` desde estructuras PGC y eventualmente unificar shell visual y KPIs. [query][^2]

### 7. Criterios de diseño adoptados

Los criterios rectores para esta fase son los siguientes:

- Una sola base de datos SQLite en V1, con posibilidad futura de migrar sin romper el modelo.[^1][^2]
- Un solo login y una sola sesión para entrar a todos los módulos.[^2]
- Separación modular a nivel de app Django, no a nivel de proyecto independiente.[^1][^2]
- Alimentación inicial por archivos Excel/CSV, con trazabilidad de importación y sin depender todavía de integraciones directas complejas.[^1][^2]
- Persistir principalmente datos base y snapshots; evitar persistir cálculos derivados cuando puedan recalcularse con claridad.[^2]
- Priorizar pantallas mínimas funcionales y limpias por módulo, antes que amplitud excesiva de opciones.[^1][^2]
- Mantener un diccionario de datos y una bitácora de cargas para sostener la visión datamart. [query][^2]


### 8. Estado reportado por Cursor y cómo debe interpretarse

La última respuesta de Cursor afirma que ya se realizaron tareas de integración y completado sobre el estado real de WCG One V1, incluyendo alineación de modelos, importadores ajustados, dashboards enriquecidos, cálculo básico de `PgoResultadoPeriodo`, un comando `seed_wcg_demo` y una migración adicional para `RiskOperationSnapshot` con `monto_exigible`. [query]
Esa respuesta también afirma que los archivos con nombres exactos indicados por el usuario no estaban presentes en disco al momento de su trabajo, y que por ello se crearon utilidades para preparar archivos de muestra en `data/wcg/` y luego cargar datos demostrativos. [query]

Esto debe interpretarse con cuidado: la memoria maestra no debe asumir como verdad absoluta cada detalle de implementación reportado por Cursor hasta que se confirme en repositorio, pero sí debe registrar que existe ya una línea de trabajo concreta reportada y que los siguientes pasos deberán auditarla y estabilizarla, no reiniciarla. [query]
Por tanto, la posición correcta es: **se reconoce una integración V1 reportada por Cursor, pendiente de validación puntual de código, archivos reales y consistencia con negocio**. [query]

### 9. Verdades operativas que sí quedan fijadas

Quedan fijadas como verdades operativas de esta etapa las siguientes:

- El producto debe seguir llamándose conceptualmente **WCG One**. [query]
- La implementación vive sobre `~/wc/pgc1/dashboard`, no en un proyecto nuevo separado. [query]
- El proyecto Django real se llama `config/`, no `wcgone/`. [query]
- La base es SQLite única. [query][^1]
- Los módulos vigentes son `portal`, `core`, `crm`, `risk`, `pgo` y `pgc`. [query]
- PGC legacy no debe tocarse estructuralmente en esta fase. [query]
- El shell WCG usa `base_wcg.html`, pero PGC legacy todavía conserva `base.html` propia. [query]
- No hay todavía permisos finos por módulo ni unificación visual total de PGC. [query]
- El enfoque correcto para riesgo V1 es snapshot operacional.[^3][^2]
- El enfoque correcto para PGO V1 es tickets + métricas básicas + score simplificado o progresivo.[^4][^5][^2]


### 10. Asuntos todavía abiertos

Aunque la dirección general está definida, siguen abiertos varios asuntos que esta memoria debe dejar explícitos:

1. **Claves naturales definitivas por importador.**
En CRM, riesgo y PGO todavía debe terminar de fijarse qué campos se tomarán como clave natural de matching en producción para evitar duplicados sin bloquear crecimiento.[^2]
2. **Mapeo oficial de archivos reales.**
El archivo de leasing ya permite entender muy bien el diseño del importador de snapshots, pero todavía debe validarse fila por fila el mapeo exacto de columnas productivas y sus conversiones.[^3]
En PGO, también debe definirse qué parte del modelo sale del archivo de tickets y qué parte viene de reglas separadas de evaluación.[^4][^5]
3. **Relación entre PGC y el maestro común.**
La integración lógica entre entidades de PGC y `core.Entidad` queda reconocida como necesaria, pero todavía no cerrada operacionalmente. [query][^2]
4. **Permisos y perfiles.**
La visión documental sí contempla usuarios con acceso por módulo, pero esa capa todavía no está implementada en V1. [query][^1]
5. **Catálogo de unidades de negocio.**
Debe estandarizarse la correspondencia entre unidades PGC, unidades operativas de riesgo y unidades consideradas por las reglas de PGO.[^5][^4][^1]

### 11. Estructura documental recomendada a partir de esta memoria

Esta Memoria maestra debe servir como documento base, y a partir de ella conviene producir los siguientes documentos derivados:

- **Documento 2 – Especificación funcional V1**, por módulo y pantalla.
- **Documento 3 – Especificación técnica Django**, con modelos, URLs, servicios, importadores y reglas de dependencia.
- **Documento 4 – Catálogo de datos e importaciones**, con archivos fuente, columnas, tipos, claves naturales, validaciones y observaciones.
- **Documento 5 – Roadmap V1.1 y V2**, con integración PGC, permisos, reglas avanzadas PGO y expansión del balón.

Esa secuencia respeta el orden correcto: primero fijar memoria y verdad compartida; luego definir funcionamiento; después aterrizar técnica; luego cerrar datos; y por último planificar expansión.[^1][^2]

### 12. Directriz de trabajo para siguientes iteraciones

A partir de este documento, toda nueva conversación o instrucción a Cursor debería partir de este principio:

> WCG One ya existe como V1 estructural sobre `~/wc/pgc1/dashboard`; no se debe reinventar la arquitectura, sino completar, alinear, validar datos reales, mejorar dashboards, consolidar importadores y cerrar el puente entre PGC legacy y el núcleo común.

Esa directriz es consistente con la decisión original del proyecto, con la realidad del repositorio actual y con el tipo de avance que más valor entregará en el corto plazo. [query][^1][^2]

### 13. Declaración de concepto común

El concepto común adoptado provisionalmente para guiar el desarrollo es este:

**WCG One es una plataforma interna única de gestión comercial, operativa y de riesgo, basada en un maestro común de entidades y en snapshots auditables, construida para crecer por etapas sin duplicar información.**[^2][^1]

### 14. Cierre operativo de esta memoria

Esta memoria no sustituye las especificaciones funcionales ni técnicas detalladas, pero sí fija el marco que evita contradicciones futuras: qué sistema existe, dónde vive, cómo está organizado, qué módulos lo componen, cuál es la filosofía de datos y cuál es la estrategia práctica de avance.[^1][^2]
Su valor principal es servir como documento rector para que tú, yo y Cursor trabajemos sobre una base común estable, acumulativa y verificable.[^2]

