# Documento 4 — Especificación de modelos, migraciones y admin para usar con Cursor

## Propósito

Este documento existe para un fin práctico: **ser usado directamente con Cursor** para que Cursor genere el esqueleto Django real de WCG One sin inventar arquitectura ni dispersar el modelo de datos.[cite:14]

El objetivo no es seguir documentando por documentar, sino bajar la conversación a un nivel donde Cursor pueda producir archivos concretos: modelos, migraciones iniciales, admin, formularios administrativos mínimos y estructura de proyecto consistente con la arquitectura ya acordada.[cite:14]

## Instrucción de uso con Cursor

La forma correcta de usar este documento con Cursor es esta:[cite:14]

1. Crear un archivo en el proyecto llamado `docs/documento-4-modelos-migraciones-admin-para-cursor.md`.
2. Pegar este documento completo.
3. Pedirle a Cursor que **genere código real**, no solo recomendaciones.
4. Pedirle que entregue archivos completos por app, en bloques pequeños y verificables.
5. No permitirle cambiar la arquitectura ya decidida.[cite:14]

## Objetivo técnico del entregable

Cursor debe generar una primera base operativa de WCG One con estos resultados mínimos:[cite:14]

- Proyecto Django contenedor listo para correr.
- Apps `portal`, `core`, `crm`, `risk`, `pgo`, `pgc` y `legacy_pgc1` creadas.[cite:14]
- Modelos V1 implementados con relaciones correctas.[cite:14]
- Migraciones iniciales creadas por app.[cite:14]
- Django Admin habilitado y bien organizado para todos los modelos principales.[cite:14]
- Índices, restricciones y `Meta` mínimos razonables para SQLite V1.[cite:14]
- Preparación para crecer luego sin rediseño mayor.[cite:14]

## Restricciones obligatorias para Cursor

Cursor debe respetar estas restricciones sin discutirlas:[cite:14]

- Un solo proyecto Django.[cite:14]
- Una sola base de datos SQLite en V1.[cite:14]
- Nada de microservicios.[cite:14]
- Nada de React ni frontend separado.[cite:14]
- Nada de múltiples proyectos raíz apuntando a la misma base.[cite:14]
- Templates server-rendered con Bootstrap simple.[cite:14]
- Código mantenible por una sola persona.[cite:14]
- PGC legado no se reescribe todavía; solo se prepara convivencia e integración progresiva.[cite:14]

## Estructura de proyecto que Cursor debe crear

```text
wcg_one/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── local.py
│       └── production.py
├── apps/
│   ├── portal/
│   ├── core/
│   ├── crm/
│   ├── risk/
│   ├── pgo/
│   ├── pgc/
│   └── legacy_pgc1/
├── templates/
├── static/
├── media/
├── uploads/
└── docs/
```

Esta estructura sigue el patrón ya decidido de proyecto contenedor, módulos separados por dominio y núcleo común compartido.[cite:14]

## Orden de construcción para Cursor

Cursor debe trabajar en este orden, sin saltárselo:[cite:14]

1. Crear proyecto y settings.
2. Crear apps y registrarlas en `INSTALLED_APPS`.
3. Crear modelos `core`.
4. Crear modelos `crm`.
5. Crear modelos `risk`.
6. Crear modelos `pgo`.
7. Crear `admin.py` por app.
8. Crear migraciones iniciales.
9. Crear `urls.py` base por app.
10. Crear placeholders mínimos de vistas/templates solo para comprobar integración.[cite:14]

## Modelos obligatorios V1

## App `core`

### 1. Entidad

Finalidad: maestro único de clientes, inversionistas, proveedores y otros terceros.[cite:14]

Campos obligatorios:

- `tipo_entidad = models.CharField(max_length=30, choices=...)`
- `es_persona = models.BooleanField(default=False)`
- `nombre = models.CharField(max_length=255)`
- `nombre_comercial = models.CharField(max_length=255, blank=True)`
- `nit = models.CharField(max_length=50, blank=True, db_index=True)`
- `pais = models.CharField(max_length=100, blank=True)`
- `departamento = models.CharField(max_length=100, blank=True)`
- `ciudad = models.CharField(max_length=100, blank=True)`
- `direccion_fiscal = models.TextField(blank=True)`
- `direccion_operativa = models.TextField(blank=True)`
- `telefono = models.CharField(max_length=50, blank=True)`
- `email = models.EmailField(blank=True)`
- `sector_economico = models.CharField(max_length=150, blank=True)`
- `codigo_sector = models.CharField(max_length=50, blank=True)`
- `activo = models.BooleanField(default=True)`
- `categoria_riesgo = models.CharField(max_length=50, blank=True)`
- `origen = models.CharField(max_length=100, blank=True)`
- `notas = models.TextField(blank=True)`
- `fecha_creacion = models.DateTimeField(auto_now_add=True)`
- `fecha_modificacion = models.DateTimeField(auto_now=True)`

Decisiones obligatorias:

- Agregar índices en `nit`, `nombre` y `(activo, tipo_entidad)`.[cite:14]
- No poner unicidad estricta en `nombre`.[cite:14]
- No poner unicidad estricta en `nit` porque puede venir vacío o sucio; usar validación en importadores además de índice.[cite:14]

### 2. Contacto

Campos obligatorios:

- `entidad = models.ForeignKey('core.Entidad', on_delete=models.CASCADE, related_name='contactos')`
- `nombre = models.CharField(max_length=255)`
- `cargo = models.CharField(max_length=150, blank=True)`
- `area = models.CharField(max_length=150, blank=True)`
- `email = models.EmailField(blank=True)`
- `telefono_movil = models.CharField(max_length=50, blank=True)`
- `telefono_oficina = models.CharField(max_length=50, blank=True)`
- `extension = models.CharField(max_length=20, blank=True)`
- `es_decisor_credito = models.BooleanField(default=False)`
- `es_contacto_cobranza = models.BooleanField(default=False)`
- `es_contacto_operativo = models.BooleanField(default=False)`
- `nivel_influencia = models.CharField(max_length=50, blank=True)`
- `nivel_apertura = models.CharField(max_length=50, blank=True)`
- `notas = models.TextField(blank=True)`
- `activo = models.BooleanField(default=True)`

Índices sugeridos:

- `(entidad, activo)`
- `email`.[cite:14]

### 3. Producto

Campos obligatorios:

- `codigo = models.CharField(max_length=30, unique=True)`
- `nombre = models.CharField(max_length=100)`
- `tipo_producto = models.CharField(max_length=100, blank=True)`
- `descripcion = models.TextField(blank=True)`
- `activo = models.BooleanField(default=True)`

### 4. UnidadNegocio

Campos obligatorios:

- `codigo = models.CharField(max_length=30, unique=True)`
- `nombre = models.CharField(max_length=100)`
- `activa = models.BooleanField(default=True)`
- `orden = models.PositiveIntegerField(default=0)`

### 5. RelacionEntidadProducto

Campos obligatorios:

- `entidad = models.ForeignKey('core.Entidad', on_delete=models.CASCADE)`
- `producto = models.ForeignKey('core.Producto', on_delete=models.PROTECT)`
- `unidad_negocio = models.ForeignKey('core.UnidadNegocio', on_delete=models.SET_NULL, null=True, blank=True)`
- `fecha_inicio = models.DateField(null=True, blank=True)`
- `fecha_fin = models.DateField(null=True, blank=True)`
- `estado = models.CharField(max_length=50, blank=True)`
- `monto_aprobado = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)`
- `moneda = models.CharField(max_length=10, blank=True)`
- `codigo_operacion_externo = models.CharField(max_length=100, blank=True, db_index=True)`
- `notas = models.TextField(blank=True)`

Índices sugeridos:

- `(entidad, producto)`
- `codigo_operacion_externo`.[cite:14]

### 6. DataDictionaryField

Campos obligatorios:[cite:14]

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

Restricción sugerida:

- unicidad compuesta en `(tabla_fisica, campo_fisico)`.[cite:14]

### 7. DataImportBatch

Campos obligatorios:[cite:14]

- `modulo`
- `tipo_importacion`
- `archivo_nombre`
- `archivo_hash`
- `archivo_ruta`
- `fecha_carga`
- `usuario = ForeignKey(settings.AUTH_USER_MODEL, ...)`
- `filas_leidas`
- `filas_validas`
- `filas_error`
- `estado`
- `observaciones`

### 8. DataImportError

Campos obligatorios:

- `batch = models.ForeignKey('core.DataImportBatch', on_delete=models.CASCADE, related_name='errores')`
- `fila_numero = models.PositiveIntegerField()`
- `campo = models.CharField(max_length=100, blank=True)`
- `valor_original = models.TextField(blank=True)`
- `mensaje_error = models.TextField()`
- `payload_json = models.JSONField(default=dict, blank=True)`

## App `crm`

### 1. Interaccion

Campos obligatorios:[cite:14]

- `entidad = models.ForeignKey('core.Entidad', on_delete=models.CASCADE, related_name='interacciones')`
- `producto = models.ForeignKey('core.Producto', on_delete=models.SET_NULL, null=True, blank=True)`
- `usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)`
- `fecha = models.DateField()`
- `hora = models.TimeField(null=True, blank=True)`
- `tipo_interaccion = models.CharField(max_length=50)`
- `resumen = models.CharField(max_length=255)`
- `resultado = models.TextField(blank=True)`
- `seguimiento_requerido = models.BooleanField(default=False)`
- `notas = models.TextField(blank=True)`
- `import_batch = models.ForeignKey('core.DataImportBatch', on_delete=models.SET_NULL, null=True, blank=True)`

Índices sugeridos:

- `(entidad, fecha)`
- `tipo_interaccion`.[cite:14]

### 2. Tarea

Campos obligatorios:[cite:14]

- `entidad = models.ForeignKey('core.Entidad', on_delete=models.CASCADE, related_name='tareas')`
- `contacto = models.ForeignKey('core.Contacto', on_delete=models.SET_NULL, null=True, blank=True)`
- `asignado_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)`
- `fecha_limite = models.DateField(null=True, blank=True)`
- `descripcion = models.TextField()`
- `prioridad = models.CharField(max_length=20, blank=True)`
- `estado = models.CharField(max_length=30, default='pendiente')`
- `completada = models.BooleanField(default=False)`
- `fecha_completada = models.DateField(null=True, blank=True)`
- `notas = models.TextField(blank=True)`

Índices sugeridos:

- `(completada, fecha_limite)`
- `(entidad, estado)`.[cite:14]

### 3. NotaEntidad

Opcional recomendada, pero Cursor puede implementarla desde V1 porque es barata y útil.[cite:14]

Campos obligatorios:

- `entidad`
- `autor`
- `fecha`
- `titulo`
- `contenido`

## App `risk`

### Decisión estructural obligatoria

Cursor debe implementar ambas capas de riesgo, pero priorizando el snapshot operativo como corazón de la V1, porque ese es el dato real hoy disponible y el más útil para la demo de 15 días.[cite:14][cite:8]

### 1. RiskOperacion

Campos obligatorios:

- `entidad = models.ForeignKey('core.Entidad', on_delete=models.CASCADE, related_name='operaciones_riesgo')`
- `producto = models.ForeignKey('core.Producto', on_delete=models.SET_NULL, null=True, blank=True)`
- `unidad_negocio = models.ForeignKey('core.UnidadNegocio', on_delete=models.SET_NULL, null=True, blank=True)`
- `codigo_operacion = models.CharField(max_length=100, db_index=True)`
- `contrato_numero = models.CharField(max_length=100, blank=True, db_index=True)`
- `asesor = models.CharField(max_length=150, blank=True)`
- `moneda = models.CharField(max_length=10, blank=True)`
- `fecha_inicio = models.DateField(null=True, blank=True)`
- `monto_original = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)`
- `estado = models.CharField(max_length=50, blank=True)`
- `notas = models.TextField(blank=True)`

Restricción sugerida:

- `UniqueConstraint(fields=['entidad', 'codigo_operacion'], name='uniq_risk_operacion_entidad_codigo')`.[cite:14]

### 2. RiskOperationSnapshot

Campos obligatorios:

- `operacion = models.ForeignKey('risk.RiskOperacion', on_delete=models.CASCADE, related_name='snapshots')`
- `entidad = models.ForeignKey('core.Entidad', on_delete=models.CASCADE)`
- `fecha_snapshot = models.DateField(db_index=True)`
- `record_date_raw = models.CharField(max_length=100, blank=True)`
- `estado_operacion = models.CharField(max_length=100, blank=True)`
- `producto_nombre_raw = models.CharField(max_length=100, blank=True)`
- `monthly_rent = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)`
- `capital_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)`
- `outstanding_installments = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)`
- `interest_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)`
- `insurance_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)`
- `other_charges_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)`
- `past_due_balance = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)`
- `due_days = models.IntegerField(null=True, blank=True)`
- `purchase_option_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)`
- `initial_rent_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)`
- `total_rent_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)`
- `archivo_origen = models.CharField(max_length=255, blank=True)`
- `import_batch = models.ForeignKey('core.DataImportBatch', on_delete=models.SET_NULL, null=True, blank=True)`
- `payload_raw_json = models.JSONField(default=dict, blank=True)`

Restricción obligatoria:

- `UniqueConstraint(fields=['operacion', 'fecha_snapshot'], name='uniq_risk_snapshot_operacion_fecha')`.[cite:14]

### 3. EstadoFinanciero

Campos obligatorios:

- `entidad`
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
- `import_batch`

Índice sugerido:

- `(entidad, fecha_corte)`.[cite:14]

### 4. RiskPagoProgramado

Campos obligatorios:

- `operacion`
- `entidad`
- `fecha_programada`
- `monto_capital`
- `monto_interes`
- `monto_mora`
- `monto_otros`
- `moneda`
- `estado`
- `notas`

### 5. RiskPagoRealizado

Campos obligatorios:

- `operacion`
- `entidad`
- `fecha_pago`
- `monto_capital`
- `monto_interes`
- `monto_mora`
- `monto_otros`
- `moneda`
- `referencia`
- `notas`

### 6. ContactoCobranza

Campos obligatorios:

- `entidad`
- `operacion`
- `contacto`
- `fecha`
- `tipo_contacto`
- `resultado`
- `acuerdo`
- `fecha_compromiso`
- `notas`

### 7. RiskAlerta

Campos obligatorios:

- `entidad`
- `operacion`
- `fecha_alerta`
- `tipo_alerta`
- `severidad`
- `mensaje`
- `activa`
- `origen`
- `detalle_json`

## App `pgo`

### 1. PgoTicket

Campos obligatorios:[cite:14]

- `ticket_externo_id = models.CharField(max_length=100, blank=True, db_index=True)`
- `usuario_solicita = models.CharField(max_length=150, blank=True)`
- `correo_solicita = models.EmailField(blank=True)`
- `departamento = models.CharField(max_length=150, blank=True, db_index=True)`
- `tipo = models.CharField(max_length=100, blank=True)`
- `titulo = models.CharField(max_length=255)`
- `estado_raw = models.CharField(max_length=100, blank=True)`
- `estado_normalizado = models.CharField(max_length=50, blank=True, db_index=True)`
- `solucion = models.TextField(blank=True)`
- `fecha_cierre = models.DateTimeField(null=True, blank=True)`
- `fecha_apertura = models.DateTimeField(null=True, blank=True)`
- `fecha_registro = models.DateTimeField(null=True, blank=True)`
- `prioridad = models.CharField(max_length=50, blank=True, db_index=True)`
- `tipo_servicio = models.CharField(max_length=100, blank=True)`
- `razon_cierre = models.CharField(max_length=255, blank=True)`
- `sistema = models.CharField(max_length=100, blank=True, db_index=True)`
- `elemento = models.CharField(max_length=255, blank=True)`
- `ruta = models.CharField(max_length=255, blank=True)`
- `anio_mes = models.CharField(max_length=7, blank=True, db_index=True)`
- `duracion_horas = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)`
- `sla_horas = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)`
- `sla_cumplido = models.BooleanField(default=False)`
- `unidad_negocio = models.ForeignKey('core.UnidadNegocio', on_delete=models.SET_NULL, null=True, blank=True)`
- `responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)`
- `import_batch = models.ForeignKey('core.DataImportBatch', on_delete=models.SET_NULL, null=True, blank=True)`
- `payload_raw_json = models.JSONField(default=dict, blank=True)`

Índices obligatorios:

- `ticket_externo_id`
- `anio_mes`
- `departamento`
- `sistema`
- `estado_normalizado`
- `prioridad`.[cite:14]

### 2. PgoMetricRule

Campos obligatorios:[cite:14]

- `codigo = models.CharField(max_length=50, unique=True)`
- `area = models.CharField(max_length=100, blank=True)`
- `variable = models.CharField(max_length=100)`
- `criterio = models.TextField()`
- `unidad_negocio = models.ForeignKey('core.UnidadNegocio', on_delete=models.SET_NULL, null=True, blank=True)`
- `puntos = models.DecimalField(max_digits=8, decimal_places=2, default=0)`
- `peso = models.DecimalField(max_digits=8, decimal_places=2, default=1)`
- `tipo_regla = models.CharField(max_length=20, default='automatica')`
- `formula_texto = models.TextField(blank=True)`
- `activo = models.BooleanField(default=True)`
- `notas = models.TextField(blank=True)`

### 3. PgoPeriodScore

Campos obligatorios:

- `periodo = models.CharField(max_length=7, db_index=True)`
- `area = models.CharField(max_length=100, blank=True)`
- `unidad_negocio = models.ForeignKey('core.UnidadNegocio', on_delete=models.SET_NULL, null=True, blank=True)`
- `usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)`
- `puntaje_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)`
- `clasifica = models.BooleanField(default=False)`
- `detalle_json = models.JSONField(default=dict, blank=True)`
- `fecha_calculo = models.DateTimeField(auto_now_add=True)`

### 4. PgoMonthlyAgg

Opcional recomendada para simplificar dashboards.[cite:14]

Campos sugeridos:

- `periodo`
- `unidad_negocio`
- `departamento`
- `tickets_recibidos`
- `tickets_cerrados`
- `tiempo_promedio_horas`
- `sla_cumplidos`
- `sla_incumplidos`
- `tickets_abiertos_fin_mes`

## App `portal`

Cursor debe crear una app mínima con:[cite:14]

- vista `home`
- template `portal/home.html`
- menú con tarjetas a `pgc`, `crm`, `risk`, `pgo`
- KPI placeholders si no hay datos
- integración con layout base.[cite:14]

## App `pgc`

En V1 solo debe existir como placeholder ordenado para futura absorción del legado.[cite:14][cite:6]

Debe incluir:

- `urls.py`
- `views.py`
- `templates/pgc/home.html`
- mensaje indicando módulo en transición.[cite:14]

## App `legacy_pgc1`

Debe existir como puente técnico transitorio hacia el activo ya implementado en `wc/pgc1/dashboard`.[cite:14]

No debe intentar copiar toda la lógica todavía.[cite:14]

## Django Admin

Cursor debe crear `admin.py` bien estructurados, no mínimos improvisados.[cite:14]

Reglas para admin:

- `list_display` útil en todos los modelos principales.
- `search_fields` en `Entidad`, `Contacto`, `RiskOperacion`, `PgoTicket`.[cite:14]
- `list_filter` en estados, fechas, unidades y activos.[cite:14]
- `autocomplete_fields` en relaciones pesadas.[cite:14]
- `date_hierarchy` en modelos temporales como `DataImportBatch`, `RiskOperationSnapshot`, `Interaccion`, `PgoPeriodScore`.[cite:14]

## Migraciones

Cursor debe generar migraciones iniciales por app y mantener dependencias limpias.[cite:14]

Orden esperado:

1. `core`
2. `crm`
3. `risk`
4. `pgo`
5. `portal` y `pgc` si requieren algo mínimo.[cite:14]

Además, debe dejar un comando claro para correr:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Prompt listo para pegar en Cursor

Copia y pega este bloque completo en Cursor:

```text
Actúa como desarrollador senior Django 5 / Python 3.11.

Quiero que construyas el esqueleto técnico real de WCG One a partir de la especificación ya aprobada. NO quiero nuevas propuestas de arquitectura; quiero código.

OBJETIVO
Genera el proyecto Django contenedor para WCG One con estas apps:
- portal
- core
- crm
- risk
- pgo
- pgc
- legacy_pgc1

DECISIONES OBLIGATORIAS
- Un solo proyecto Django.
- Una sola base SQLite en V1.
- Nada de microservicios.
- Nada de frontend separado.
- Templates Django + Bootstrap.
- El maestro común vive en core.
- PGC legado solo convive por ahora, no se reescribe completo.

TAREA PRINCIPAL
Quiero que generes, en este orden:
1. estructura de proyecto
2. settings base/local/production
3. modelos de core
4. modelos de crm
5. modelos de risk
6. modelos de pgo
7. admin.py completos por app
8. urls.py base por app
9. placeholders mínimos de views/templates para probar integración
10. instrucciones para correr migraciones

MODELOS OBLIGATORIOS
Core:
- Entidad
- Contacto
- Producto
- UnidadNegocio
- RelacionEntidadProducto
- DataDictionaryField
- DataImportBatch
- DataImportError

CRM:
- Interaccion
- Tarea
- NotaEntidad (si no estorba)

Risk:
- RiskOperacion
- RiskOperationSnapshot
- EstadoFinanciero
- RiskPagoProgramado
- RiskPagoRealizado
- ContactoCobranza
- RiskAlerta

PGO:
- PgoTicket
- PgoMetricRule
- PgoPeriodScore
- PgoMonthlyAgg (opcional si aporta)

REGLAS IMPORTANTES
- Usa ForeignKey y related_name claros.
- Agrega Meta indexes y UniqueConstraint solo donde de verdad aporten en SQLite V1.
- No crees abstracciones mágicas.
- No uses utils.py genérico para todo.
- Mantén archivos claros y pequeños.
- No pongas lógica pesada en views.
- Prepara el código para crecer después a PostgreSQL sin rediseño mayor.

FORMA DE RESPUESTA
Responde exactamente en este orden:
1. resumen de lo que vas a crear
2. árbol de archivos
3. código completo de archivos nuevos o modificados, por bloques
4. comandos para instalar y correr
5. notas técnicas y supuestos

IMPORTANTE
Entrega código real y completo. No entregues pseudoarquitectura ni recomendaciones vagas. Si el contexto es muy largo, entrega primero solo:
- config/settings
- core/models.py o core/models/*
- core/admin.py
- crm/models.py
- risk/models.py
- pgo/models.py
Y espera confirmación antes de seguir.
```

## Resultado esperado

Si Cursor sigue este documento correctamente, al terminar deberá existir una base técnica real de WCG One lista para migrar, administrar en Django Admin y usar como plataforma de importadores, vistas y reportes V1.[cite:14]
