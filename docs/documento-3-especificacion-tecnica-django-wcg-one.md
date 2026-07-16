# Documento 3 — Especificación técnica Django V1 para WCG One

## Propósito

Este documento define la especificación técnica V1 de **WCG One**, la plataforma unificada para Working Capital Group que integrará PGC, CRM, PGO y Balón de Riesgo en un solo proyecto Django, con una sola base de datos y un menú principal común.[cite:14]

La decisión arquitectónica central ya queda cerrada: no se construirán varios proyectos Django raíz ni múltiples bases de datos para esta fase, sino un solo proyecto contenedor con apps internas por dominio, porque esa estructura reduce complejidad operativa, evita duplicación y es consistente con la documentación previa del proyecto.[cite:14]

## Alcance V1

La V1 debe ser funcional, demostrable y mantenible por una sola persona en un plazo corto, priorizando importación de archivos, listados, detalles, dashboards básicos y trazabilidad de datos sobre sofisticación excesiva.[cite:14]

En esta fase sí entran: menú principal, autenticación básica, núcleo común de datos, CRM mínimo funcional, Balón de Riesgo basado primero en snapshots operativos, PGO basado primero en tickets y tiempos, integración provisional de PGC al menú, Django Admin completo y patrón uniforme de importación.[cite:14][cite:6]

Queda explícitamente fuera de V1: microservicios, frontend separado, scoring sofisticado de riesgo, stress testing avanzado, automatización masiva de fuentes externas, motor completo de señales proxy y reconstrucción total inmediata del módulo PGC ya existente.[cite:14][cite:8][cite:6]

## Principios técnicos

Los principios obligatorios de la implementación son los siguientes:[cite:14]

- Un solo proyecto Django.
- Una sola base de datos SQLite en V1.
- Apps internas separadas por dominio funcional.
- Un solo login y un solo menú raíz.
- Modelo maestro compartido de entidades, contactos, productos y operaciones comunes.
- Importación por archivos CSV/XLSX como mecanismo oficial de carga V1.
- Diseño tipo datamart con diccionario de datos y trazabilidad de importaciones.
- Bootstrap simple y renderizado server-side con Django templates.[cite:14]

## Arquitectura del proyecto

La estructura recomendada del proyecto debe ser esta, o una equivalente muy cercana:[cite:14]

```text
wcg_one/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── portal/
│   ├── core/
│   ├── crm/
│   ├── risk/
│   ├── pgo/
│   ├── pgc/
│   └── legacy_pgc1/
├── templates/
│   ├── base.html
│   ├── includes/
│   └── portal/
├── static/
├── media/
├── uploads/
├── output/
└── docs/
```

Esta estructura sigue el patrón ya propuesto en el material previo: un proyecto contenedor con separación estricta por dominios, donde cada app puede evolucionar casi como un mini-producto, pero compartiendo identidad maestra, autenticación, layout base y bitácoras de importación.[cite:14]

## Responsabilidad por app

| App | Responsabilidad principal |
|---|---|
| `portal` | Home, menú principal, navegación, permisos de entrada, panel inicial.[cite:14] |
| `core` | Entidades maestras, contactos base, productos, relaciones, catálogos, diccionario de datos, lotes de importación, errores de importación.[cite:14] |
| `crm` | Interacciones, tareas, vistas de seguimiento comercial y operativo sobre el maestro común.[cite:14] |
| `risk` | Operaciones, snapshots, estados financieros, pagos, cobranza, alertas y comando balón.[cite:14][cite:8] |
| `pgo` | Tickets, reglas de medición, resultados periódicos y dashboards de eficiencia operativa.[cite:14] |
| `pgc` | Integración futura del PGC al proyecto unificado, iniciando con placeholder y puente técnico.[cite:14][cite:6] |
| `legacy_pgc1` | Envoltorio transicional para convivir con el activo existente en `wc/pgc1/dashboard` mientras no se absorba por completo.[cite:14] |

## Reglas de dependencia

Las dependencias entre apps deben ser deliberadamente estrechas.[cite:14]

- `core` posee la identidad maestra.
- `crm` lee de `core` y agrega relaciones e interacciones.
- `risk` lee de `core` y gestiona operaciones, snapshots, EEFF, pagos y cobranza.
- `pgo` lee de `core` cuando necesita unidades, usuarios o entidades relacionadas, pero su lógica es propia.
- Ningún módulo debe escribir directamente tablas internas de otro módulo fuera de `core`.[cite:14]

La regla práctica es: compartir pocos datos estructurales, no compartir lógica de negocio. Eso evita que el proyecto se convierta en un “monstruo” difícil de mantener.[cite:14]

## Settings y despliegue

La configuración debe dividirse como mínimo en `base.py`, `local.py` y `production.py`, usando variables de entorno para `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`, `MEDIA_ROOT` y `STATIC_ROOT`.[cite:14]

Aunque la V1 opere con SQLite, el diseño debe mantener compatibilidad razonable para migrar luego a PostgreSQL sin rediseño mayor del modelo ni de los servicios de dominio.[cite:14]

## Navegación y URLs globales

La navegación raíz debe presentar una pantalla inicial WCG con acceso a PGC, PGO, CRM y Balón de Riesgo, tal como se ha planteado repetidamente en la documentación funcional e histórica.[cite:14][cite:6]

El enrutamiento global debe seguir un patrón de namespaces claros:[cite:14]

```python
urlpatterns = [
    path('', include('apps.portal.urls')),
    path('core/', include('apps.core.urls')),
    path('crm/', include('apps.crm.urls')),
    path('risk/', include('apps.risk.urls')),
    path('pgo/', include('apps.pgo.urls')),
    path('pgc/', include('apps.pgc.urls')),
    path('legacy-pgc1/', include('apps.legacy_pgc1.urls')),
    path('admin/', admin.site.urls),
]
```

Mientras dure la transición, `legacy_pgc1` puede actuar como punto de acceso provisional hacia el sistema existente, evitando reescribir PGC antes de tiempo.[cite:14]

## Modelo común V1

La base técnica más importante de WCG One es el núcleo común, porque CRM, riesgo y parcialmente PGO dependen de una identidad compartida de entidades, contactos, productos y relaciones.[cite:14]

### Modelos de `core`

#### Entidad

Representa cliente, inversionista, proveedor u otra contraparte relevante del negocio.[cite:14]

Campos sugeridos:

- `id`
- `tipo_entidad` (`cliente`, `inversionista`, `ambos`, `proveedor`, `otro`)
- `es_persona`
- `nombre`
- `nombre_comercial`
- `nit`
- `pais`
- `departamento`
- `ciudad`
- `direccion_fiscal`
- `direccion_operativa`
- `telefono`
- `email`
- `sector_economico`
- `codigo_sector`
- `activo`
- `categoria_riesgo`
- `origen`
- `notas`
- `fecha_creacion`
- `fecha_modificacion`

Restricciones recomendadas:

- índice por `nit`
- índice por `nombre`
- validación anti-duplicado por combinación razonable de `nit` y `nombre`
- preferencia por `nit` como clave natural cuando exista.[cite:14]

#### Contacto

Representa personas de contacto asociadas a una entidad, con roles comerciales, operativos o de cobranza.[cite:14]

Campos sugeridos:

- `id`
- `entidad` (FK)
- `nombre`
- `cargo`
- `area`
- `email`
- `telefono_movil`
- `telefono_oficina`
- `extension`
- `es_decisor_credito`
- `es_contacto_cobranza`
- `es_contacto_operativo`
- `nivel_influencia`
- `nivel_apertura`
- `notas`
- `activo`

#### Producto

Campos sugeridos:[cite:14]

- `id`
- `codigo`
- `nombre`
- `tipo_producto`
- `descripcion`
- `activo`

#### RelacionEntidadProducto

Esta tabla permite que una entidad tenga múltiples productos y que un producto exista en múltiples relaciones a lo largo del tiempo, algo que la documentación considera esencial para CRM y riesgo.[cite:14]

Campos sugeridos:

- `id`
- `entidad` (FK)
- `producto` (FK)
- `unidad_negocio` (FK nullable)
- `fecha_inicio`
- `fecha_fin`
- `estado`
- `monto_aprobado`
- `moneda`
- `codigo_operacion_externo`
- `notas`

#### UnidadNegocio

Debe representar como mínimo las UNE relevantes del negocio y, si ayuda, algunas áreas operativas como Tecnología, Legal, Operaciones o Finanzas/Riesgos.[cite:14][cite:6]

Campos sugeridos:

- `id`
- `codigo`
- `nombre`
- `activa`
- `orden`

#### DataDictionaryField

Este modelo materializa la idea de datamart pedida desde el inicio, donde cada variable tenga definición, fuente y orden.[cite:14]

Campos sugeridos:

- `id`
- `modulo`
- `nombre_logico`
- `tabla_fisica`
- `campo_fisico`
- `tipo_dato`
- `definicion`
- `fuente`
- `periodicidad`
- `orden`
- `notas`
- `activo`

#### DataImportBatch

Toda carga debe quedar asociada a un lote auditable.[cite:14]

Campos sugeridos:

- `id`
- `modulo`
- `tipo_importacion`
- `archivo_nombre`
- `archivo_hash`
- `archivo_ruta`
- `fecha_carga`
- `usuario`
- `filas_leidas`
- `filas_validas`
- `filas_error`
- `estado`
- `observaciones`

#### DataImportError

Se recomienda fuertemente crear también una tabla de errores por fila, aunque en la documentación aparece como opcional implícita, porque mejora muchísimo la depuración de archivos reales.[cite:14]

Campos sugeridos:

- `id`
- `batch` (FK)
- `fila_numero`
- `campo`
- `valor_original`
- `mensaje_error`
- `payload_json`

## CRM V1

La V1 de CRM ya tiene base funcional suficiente en la documentación: maestro de entidades, contactos, productos relacionados, interacciones, tareas e importación inicial desde archivos estándar.[cite:14]

### Modelos de `crm`

#### Interaccion

Campos sugeridos:

- `id`
- `entidad` (FK)
- `producto` (FK nullable)
- `usuario`
- `fecha`
- `hora`
- `tipo_interaccion`
- `resumen`
- `resultado`
- `seguimiento_requerido`
- `notas`
- `import_batch` (nullable)

#### Tarea

Campos sugeridos:

- `id`
- `entidad` (FK)
- `contacto` (FK nullable)
- `asignado_a`
- `fecha_limite`
- `descripcion`
- `prioridad`
- `estado`
- `completada`
- `fecha_completada`
- `notas`

#### NotaEntidad (opcional recomendada)

Aunque no es indispensable, puede ser útil para separar notas libres de interacciones formales.[cite:14]

Campos sugeridos:

- `id`
- `entidad` (FK)
- `autor`
- `fecha`
- `titulo`
- `contenido`

### Reglas CRM V1

- Una entidad puede tener múltiples contactos.[cite:14]
- Una entidad puede tener múltiples productos o relaciones producto vigentes o históricas.[cite:14]
- El maestro debe controlar duplicidad básica por `nit` y `nombre`.[cite:14]
- Las vistas de CRM deben construirse sobre `core`, no duplicando tablas maestras.[cite:14]

## Risk V1

La recomendación técnica es implementar **ambas capas**, pero con prioridad clara en `RiskOperationSnapshot` porque el archivo real disponible soporta muy bien ese modelo y conserva el valor histórico por operación y fecha.[cite:14]

El enfoque de snapshots además es coherente con la visión de riesgo in-house, que valora señales operativas frecuentes, comportamiento de pago, días de atraso, cambios de patrón y alertas semanales antes del próximo cierre trimestral.[cite:8][cite:14]

### Modelos de `risk`

#### RiskOperacion

Esta tabla desacopla la identidad estable de una operación respecto a sus snapshots diarios.[cite:14]

Campos sugeridos:

- `id`
- `entidad` (FK)
- `producto` (FK)
- `unidad_negocio` (FK nullable)
- `codigo_operacion`
- `contrato_numero`
- `asesor`
- `moneda`
- `fecha_inicio`
- `monto_original`
- `estado`
- `notas`

Restricciones recomendadas:

- índice por `codigo_operacion`
- unicidad razonable por `codigo_operacion` y `entidad`.[cite:14]

#### RiskOperationSnapshot

Este es el modelo prioritario de Balón de Riesgo V1.[cite:14]

Campos sugeridos:

- `id`
- `operacion` (FK)
- `entidad` (FK)
- `fecha_snapshot`
- `record_date_raw`
- `estado_operacion`
- `producto_nombre_raw`
- `monthly_rent`
- `capital_balance`
- `outstanding_installments`
- `interest_balance`
- `insurance_balance`
- `other_charges_balance`
- `past_due_balance`
- `due_days`
- `purchase_option_value`
- `initial_rent_value`
- `total_rent_value`
- `archivo_origen`
- `import_batch` (FK)
- `payload_raw_json`

Clave natural recomendada:

- `fecha_snapshot + codigo_operacion + entidad`
- si el archivo real lo exige, ampliar a `fecha_snapshot + contrato_numero + entidad + unidad_negocio`.[cite:14]

Reglas de persistencia:

- Persistir los valores crudos del archivo que representan evidencia histórica, aunque algunos puedan derivarse visualmente después.[cite:14]
- No persistir como columnas fijas indicadores triviales calculables en tiempo real, por ejemplo banderas de color o clasificación visual derivada de `due_days` y `past_due_balance`.[cite:14]

#### EstadoFinanciero

Aunque no sea el corazón de V1, conviene dejarlo desde el inicio para no cerrar el camino a la evolución prevista del módulo de riesgo.[cite:14][cite:8]

Campos sugeridos:

- `id`
- `entidad` (FK)
- `fecha_corte`
- `auditor_contador`
- `ventas`
- `utilidad_neta`
- `activo_corriente`
- `activo_no_corriente`
- `pasivo_corriente`
- `pasivo_no_corriente`
- `patrimonio`
- `ebitda`
- `observaciones`
- `import_batch` (FK nullable)

#### RiskPagoProgramado

Campos sugeridos:

- `id`
- `operacion` (FK)
- `entidad` (FK)
- `fecha_programada`
- `monto_capital`
- `monto_interes`
- `monto_mora`
- `monto_otros`
- `moneda`
- `estado`
- `notas`

#### RiskPagoRealizado

Campos sugeridos:

- `id`
- `operacion` (FK)
- `entidad` (FK)
- `fecha_pago`
- `monto_capital`
- `monto_interes`
- `monto_mora`
- `monto_otros`
- `moneda`
- `referencia`
- `notas`

#### ContactoCobranza

Campos sugeridos:

- `id`
- `entidad` (FK)
- `operacion` (FK nullable)
- `contacto` (FK nullable)
- `fecha`
- `tipo_contacto`
- `resultado`
- `acuerdo`
- `fecha_compromiso`
- `notas`

#### RiskAlerta (recomendada)

Dado que los documentos de riesgo enfatizan alertas semanales de deterioro, conviene dejar una tabla simple de alertas desde V1, aunque su generación inicial sea muy básica.[cite:8]

Campos sugeridos:

- `id`
- `entidad` (FK)
- `operacion` (FK nullable)
- `fecha_alerta`
- `tipo_alerta`
- `severidad`
- `mensaje`
- `activa`
- `origen`
- `detalle_json`

### Reglas Risk V1

- Un snapshot nunca sobrescribe otro snapshot de distinta fecha.[cite:14]
- Por defecto se muestran casos vigentes, no históricos cerrados, salvo consulta explícita.[cite:14]
- La lógica del comando balón debe concentrarse primero en operaciones activas, saldo vencido, días de atraso, tendencia reciente e historial por operación.[cite:14][cite:8]
- Las alertas V1 pueden basarse en reglas simples: `due_days > 0`, aumento de saldo vencido respecto al snapshot anterior, o ausencia de pago real frente a pago programado.[cite:8][cite:14]

## PGO V1

El PGO debe arrancar con una capa operativa real basada en tickets, tiempos de atención y resúmenes por usuario, departamento, prioridad, sistema y período; el scoring más completo puede madurar después sobre reglas parametrizables.[cite:14]

### Modelos de `pgo`

#### PgoTicket

Campos sugeridos:

- `id`
- `ticket_externo_id`
- `usuario_solicita`
- `correo_solicita`
- `departamento`
- `tipo`
- `titulo`
- `estado_raw`
- `estado_normalizado`
- `solucion`
- `fecha_cierre`
- `fecha_apertura`
- `fecha_registro`
- `prioridad`
- `tipo_servicio`
- `razon_cierre`
- `sistema`
- `elemento`
- `ruta`
- `anio_mes`
- `duracion_horas`
- `sla_horas` (nullable)
- `sla_cumplido`
- `unidad_negocio` (FK nullable)
- `responsable` (nullable)
- `import_batch` (FK)
- `payload_raw_json`

Índices recomendados:

- `ticket_externo_id`
- `anio_mes`
- `departamento`
- `sistema`
- `estado_normalizado`
- `prioridad`.[cite:14]

#### PgoMetricRule

Las reglas de puntos no deben hardcodearse más de lo necesario; conviene modelarlas desde el inicio, aunque algunas se apliquen manualmente o parcialmente en V1.[cite:14]

Campos sugeridos:

- `id`
- `codigo`
- `area`
- `variable`
- `criterio`
- `unidad_negocio` (FK nullable)
- `puntos`
- `peso`
- `tipo_regla` (`automatica`, `manual`, `hibrida`)
- `formula_texto`
- `activo`
- `notas`

#### PgoPeriodScore

Campos sugeridos:

- `id`
- `periodo`
- `area`
- `unidad_negocio` (FK nullable)
- `usuario` (nullable)
- `puntaje_total`
- `clasifica`
- `detalle_json`
- `fecha_calculo`

#### PgoMonthlyAgg (opcional recomendada)

En SQLite y en V1 no es indispensable, pero una tabla agregada por período puede simplificar dashboards si el volumen crece.[cite:14]

Campos sugeridos:

- `id`
- `periodo`
- `unidad_negocio`
- `departamento`
- `tickets_recibidos`
- `tickets_cerrados`
- `tiempo_promedio_horas`
- `sla_cumplidos`
- `sla_incumplidos`
- `tickets_abiertos_fin_mes`

### Reglas PGO V1

- El ticket debe conservar el estado crudo importado y también un estado normalizado para análisis.[cite:14]
- La duración debe calcularse si falta o si el archivo trae inconsistencias entre apertura y cierre.[cite:14]
- El scoring mensual puede mezclar reglas automáticas y cargas manuales parciales en V1.[cite:14]
- Criterios como “máximo 3 tickets abiertos”, “cumplimiento de tiempos de helpdesk” y “clasificación satisfactoria desde 80 puntos” ya tienen respaldo documental para una primera parametrización.[cite:14]

## Pantallas mínimas V1

### Portal

| URL | Objetivo | Componentes principales |
|---|---|---|
| `/` | Home WCG One | Tarjetas a PGC, CRM, Risk, PGO; indicadores rápidos; accesos a importaciones recientes.[cite:14][cite:6] |

### CRM

| URL | Objetivo | Componentes principales |
|---|---|---|
| `/crm/entidades/` | Listado maestro | Filtros por nombre, NIT, tipo, ciudad, riesgo, activo; tabla exportable.[cite:14] |
| `/crm/entidades/<id>/` | Detalle entidad | Datos generales, contactos, productos, interacciones recientes, tareas.[cite:14] |
| `/crm/contactos/` | Gestión de contactos | Tabla filtrable y acceso rápido desde entidad.[cite:14] |
| `/crm/tareas/` | Seguimiento comercial | Pendientes, vencidas, asignadas, completadas.[cite:14] |
| `/crm/importar/` | Carga inicial CRM | Subida de CSV/XLSX, validación, lote, resultado.[cite:14] |

### Risk

| URL | Objetivo | Componentes principales |
|---|---|---|
| `/risk/comando-balon/` | Vista gerencial diaria | Tabla resumen por cliente/operación, saldo vencido, días atraso, alertas, ranking.[cite:14][cite:8] |
| `/risk/clientes/` | Clientes de riesgo | Filtros por categoría, días atraso, unidad, producto.[cite:14] |
| `/risk/clientes/<id>/` | Detalle cliente riesgo | Datos base, operaciones activas, EEFF, alertas, contactos cobranza.[cite:14] |
| `/risk/operaciones/<id>/` | Detalle operación | Historial de snapshots, pagos programados, pagos realizados.[cite:14] |
| `/risk/importar-snapshots/` | Carga snapshot leasing | Validación, deduplicación, lote, resultado.[cite:14] |
| `/risk/importar-eeff/` | Carga EEFF | Importación trimestral básica.[cite:14] |

### PGO

| URL | Objetivo | Componentes principales |
|---|---|---|
| `/pgo/` | Dashboard PGO | KPIs, tickets abiertos, cerrados, tiempo promedio, SLA, por sistema y prioridad.[cite:14] |
| `/pgo/tickets/` | Lista de tickets | Filtros por período, estado, prioridad, sistema, departamento.[cite:14] |
| `/pgo/tickets/<id>/` | Detalle ticket | Datos completos, tiempos, normalización, trazabilidad.[cite:14] |
| `/pgo/resultados/` | Resumen por período | Resultados preliminares por unidad/persona/área.[cite:14] |
| `/pgo/reglas/` | Reglas de puntos | Lista y edición administrativa de reglas parametrizadas.[cite:14] |
| `/pgo/importar-tickets/` | Carga tickets | Validación, transformación, lote, resultado.[cite:14] |

## Patrón uniforme de importación

Todos los módulos deben usar un patrón uniforme de carga, porque eso ya existe conceptualmente en PGC1 y se ha señalado como una pieza estructural para la nueva plataforma.[cite:14][cite:6]

Flujo estándar de importación:[cite:14]

1. El usuario sube un archivo.
2. Se crea `DataImportBatch`.
3. El archivo queda en staging (`uploads/`).
4. Un validador detecta tipo y columnas.
5. El importador del módulo procesa filas.
6. Se guardan filas válidas.
7. Se registran errores y warnings.
8. Se actualizan estadísticas de carga.
9. Se genera bitácora auditable.[cite:14]

## Flujos de importación V1

### CRM

Entrada principal: archivo de clientes básico en CSV/XLSX.[cite:14]

Pseudoflujo:

1. Leer archivo con `pandas` si es tabular estándar; usar `csv` puro si el formato es muy simple.[cite:14]
2. Normalizar encabezados.
3. Buscar entidad por `nit`; si no existe, buscar por `nombre` normalizado.[cite:14]
4. Si existe, actualizar campos básicos permitidos.
5. Si no existe, crear entidad nueva.
6. Registrar batch y errores por fila.
7. Opcionalmente crear contactos si el archivo los incluye.[cite:14]

### Risk

Entrada principal: archivo maestro tipo leasing por operación y fecha.[cite:14]

Pseudoflujo:

1. Leer Excel con `pandas` + `openpyxl`.[cite:14]
2. Normalizar nombres de columnas.
3. Determinar `fecha_snapshot` desde archivo o parámetro explícito.
4. Resolver o crear `Entidad`.
5. Resolver o crear `RiskOperacion` por `codigo_operacion`/`contrato_numero` y entidad.[cite:14]
6. Construir clave natural de snapshot.
7. Si ya existe snapshot igual, omitir o marcar duplicado sin destruir historial.[cite:14]
8. Crear snapshot nuevo con valores crudos relevantes.
9. Registrar errores por filas inválidas.
10. Asociar todo al `DataImportBatch`.[cite:14]

### PGO

Entrada principal: archivo de tickets Excel/CSV.[cite:14]

Pseudoflujo:

1. Leer archivo con `pandas`.[cite:14]
2. Normalizar encabezados y estados.
3. Convertir fechas de apertura, cierre y registro.
4. Si `duracion_horas` viene vacía o inconsistente, recalcular desde apertura y cierre.[cite:14]
5. Resolver clave natural por `ticket_externo_id`; si no existe, usar combinación de ID lógico + fecha de registro.[cite:14]
6. Crear o actualizar ticket de manera incremental.
7. Guardar `estado_raw` y `estado_normalizado`.[cite:14]
8. Calcular `anio_mes`, `sla_cumplido` y banderas simples.
9. Registrar batch y errores.[cite:14]

## Servicios, selectors y organización interna

Cada app debe seguir una estructura modular simple y consistente para evitar archivos gigantes y lógica incrustada en vistas o templates.[cite:14]

Patrón recomendado por app:[cite:14]

```text
apps/risk/
├── admin.py
├── apps.py
├── urls.py
├── forms.py
├── views/
├── models/
├── services/
├── selectors/
├── imports/
├── reports/
└── tests/
```

Criterios prácticos:[cite:14]

- `models/`: estructura de datos del dominio.
- `services/`: reglas de negocio y procesos.
- `selectors/`: lecturas y queries complejas.
- `imports/`: lectura, validación y carga de archivos.
- `reports/`: exportaciones o tablas resumidas.
- `views/`: composición web, no lógica pesada.[cite:14]

## Decisiones tecnológicas recomendadas

| Tema | Decisión recomendada |
|---|---|
| Formularios administrativos simples | Usar Django Admin cuando sea CRUD puro.[cite:14] |
| Vistas orientadas a usuario final | Crear vistas propias con templates Bootstrap.[cite:14] |
| Vistas simples de listado/detalle | Preferir class-based views si reducen boilerplate sin complicar lógica.[cite:14] |
| Vistas con mucha agregación o múltiples acciones | Preferir function-based views o class-based especializadas, según claridad.[cite:14] |
| Lectura Excel compleja | Usar `pandas` + `openpyxl`.[cite:14] |
| CSV simple | `pandas` o módulo `csv`; elegir lo más simple para el caso.[cite:14] |
| Índices SQLite V1 | Poner solo los que ayudan de verdad: claves naturales, fechas, estado, período, NIT, ticket ID.[cite:14] |
| Qué no complicar | No crear abstracciones mágicas, clases base innecesarias, ni modelos universales con campos para todo.[cite:14] |

## Integración de PGC y legado

La estrategia correcta para PGC no es reescribirlo de inmediato, sino proteger el activo existente y convivir con él mediante una transición por fases.[cite:14][cite:6]

Fases recomendadas:[cite:14]

- **Fase A — Encapsular:** registrar `legacy_pgc1` y enlazarlo desde el menú común.
- **Fase B — Puente:** compartir login, layout y navegación cuando sea posible.
- **Fase C — Absorción:** migrar gradualmente la lógica útil a `apps/pgc/`.[cite:14]

Ese orden protege el producto ya construido y evita bloquear los módulos nuevos por una refactorización prematura del sistema heredado.[cite:14]

## Plan de implementación en 15 días

El orden de construcción más prudente ya está bastante bien definido en el material previo y sigue siendo válido para esta especificación.[cite:14]

| Fase | Objetivo |
|---|---|
| 1 | Crear proyecto contenedor, settings, portal, core, login y menú principal.[cite:14] |
| 2 | Implementar modelos base, admin y diccionario de datos/import batches.[cite:14] |
| 3 | Construir importadores CRM, Risk y PGO.[cite:14] |
| 4 | Construir listados y detalles mínimos por módulo.[cite:14] |
| 5 | Construir dashboards y reportes básicos.[cite:14][cite:8] |
| 6 | Integrar acceso provisional a PGC legado y preparar demo.[cite:14][cite:6] |

## Riesgos técnicos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| El modelo crece desordenadamente | Separar por dominio, mantener `core` pequeño y evitar campos “por si acaso”.[cite:14] |
| Los importadores se vuelven opacos | Registrar `DataImportBatch` y `DataImportError` siempre.[cite:14] |
| Duplicidad de clientes | Priorizar `nit`, normalizar nombre y validar antes de crear.[cite:14] |
| PGO intenta resolver todo de una vez | Empezar por tickets y tiempos; dejar scoring sofisticado para V1.1.[cite:14] |
| Riesgo se dispersa en demasiadas tablas conceptuales | Priorizar `RiskOperationSnapshot` y complementar progresivamente.[cite:14][cite:8] |
| PGC retrasa la entrega | Mantener integración provisional mediante `legacy_pgc1`.[cite:14] |

## Decisiones cerradas

Las decisiones que este documento deja cerradas son estas:[cite:14]

- WCG One se implementa como un solo proyecto Django.
- La V1 usa una sola base SQLite.
- Se crean apps `portal`, `core`, `crm`, `risk`, `pgo`, `pgc` y `legacy_pgc1`.
- El núcleo maestro vive en `core`.
- CRM se construye sobre entidades, contactos, productos, interacciones y tareas.
- Risk prioriza snapshots operativos por operación y fecha, complementados por EEFF y cobranza.
- PGO prioriza tickets, tiempos y reglas parametrizables.
- Toda carga queda asociada a lotes auditables.
- PGC legado convive primero y se absorbe después.[cite:14]

## Siguiente documento

La siguiente pieza natural no tiene por qué convertirse en una cadena indefinida de documentos. Técnicamente, después de este Documento 3 basta con producir, como mucho, dos piezas muy prácticas:[cite:14]

1. **Documento 4 — Especificación de modelos, migraciones y admin**, si se desea bajar aún más a nivel de código antes de Cursor.[cite:14]
2. **Documento 5 — Prompt maestro de construcción para Cursor**, si se prefiere pasar ya de especificación a generación guiada de código.[cite:14]

No es necesario seguir creando “documento 6, 7, 8…” salvo que al probar la implementación aparezca un hueco concreto. Ese criterio es coherente con la recomendación previa de trabajar por capas reales: construir, corregir e integrar, y luego pulir demo, en vez de adelantarse demasiado al proceso.[cite:14]
