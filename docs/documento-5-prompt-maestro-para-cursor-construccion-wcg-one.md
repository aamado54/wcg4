# Documento 5 — Prompt maestro para usar con Cursor y construir WCG One

## Propósito

Este documento es el puente entre la estrategia ya acordada y la ejecución real en Cursor. Su valor no está en “leerlo”, sino en **pegarlo en Cursor para que produzca código real** sobre una arquitectura ya cerrada y una especificación ya madura.[cite:14]

Los Documentos 2, 3 y 4 sirven para alinear visión, técnica y estructura; este Documento 5 sirve para **hacer**. Si no se usa con Cursor, pierde gran parte de su utilidad práctica.[cite:14]

## Cómo usar este documento con Cursor

Uso recomendado:[cite:14]

1. Abrir el proyecto o carpeta destino en Cursor.
2. Crear `docs/documento-5-prompt-maestro-para-cursor-construccion-wcg-one.md`.
3. Pegar este documento completo.
4. Copiar el bloque del “Prompt maestro” y enviarlo a Cursor.
5. Pedir ejecución por etapas, no todo de una sola vez.[cite:14]

La mejor secuencia con Cursor es:[cite:14]

- Paso A: que genere base de proyecto, settings y modelos.
- Paso B: que genere admin, importadores y URLs.
- Paso C: que genere vistas, templates y dashboard mínimo.
- Paso D: que conecte con archivos reales y haga correcciones.
- Paso E: que pula demo y navegación gerencial.[cite:14]

## Qué debe producir Cursor

El resultado esperado de este prompt maestro es una primera versión funcional y demostrable de WCG One, con estas capacidades mínimas:[cite:14]

- Pantalla inicial única WCG.[cite:14]
- Menú con PGC, CRM, Risk y PGO.[cite:14]
- Base de datos única con modelo común de entidades, contactos, productos y operaciones.[cite:14]
- Importadores manuales por CSV/XLSX para CRM, Risk y PGO.[cite:14]
- Dashboards básicos y vistas mínimas por módulo.[cite:14]
- Django Admin completo para soporte operativo interno.[cite:14]
- Convivencia provisional con PGC legado.[cite:14]

## Restricciones que Cursor no puede romper

Cursor debe asumir como definitivas estas restricciones:[cite:14]

- Un solo proyecto Django.[cite:14]
- Una sola base de datos SQLite en V1.[cite:14]
- Apps internas por dominio: `portal`, `core`, `crm`, `risk`, `pgo`, `pgc`, `legacy_pgc1`.[cite:14]
- Un solo login y un solo menú principal.[cite:14]
- Todo server-rendered con Django templates y Bootstrap simple.[cite:14]
- Nada de microservicios.[cite:14]
- Nada de frontend separado.[cite:14]
- Nada de múltiples bases de datos.[cite:14]
- Nada de rediseñar PGC completo en esta iteración.[cite:14][cite:6]

## Prompt maestro para Cursor

Copia y pega este bloque completo en Cursor:

```text
Actúa como arquitecto senior de software y desarrollador lead Django 5 / Python 3.11.

Tu tarea es CONSTRUIR una primera versión funcional de WCG One, una plataforma interna para Working Capital Group que unifica PGC, CRM, PGO y Balón de Riesgo bajo un solo proyecto Django y una sola base de datos SQLite en esta etapa.

IMPORTANTE
No quiero nuevas propuestas conceptuales. No quiero otra arquitectura. La arquitectura ya fue decidida. Quiero implementación real, ordenada y pragmática, compatible con una entrega demostrable en 15 días.

## CONTEXTO DE NEGOCIO
WCG necesita una plataforma única interna, práctica y rápida de implementar, mantenible por una sola persona, y construida solamente con Django + Python.

La V1 debe priorizar:
- rapidez de entrega
- claridad del modelo de datos
- importación de archivos reales
- dashboards básicos útiles
- navegación uniforme
- facilidad de crecimiento posterior

## DECISIONES DE ARQUITECTURA YA CERRADAS
Debes asumir estas decisiones como obligatorias:
1. Un solo proyecto Django.
2. Una sola base de datos SQLite en V1.
3. Apps internas:
   - portal
   - core
   - crm
   - risk
   - pgo
   - pgc
   - legacy_pgc1
4. Un solo menú principal.
5. Un solo login con Django auth.
6. Un maestro común de entidades, contactos, productos y operaciones compartidas.
7. Importaciones por archivos CSV/XLSX como mecanismo oficial de carga en V1.
8. Diseño tipo datamart con diccionario de datos y trazabilidad de importaciones.
9. Nada de microservicios, nada de React, nada de frontend separado.
10. PGC legado debe convivir primero y migrarse después.

## ALCANCE FUNCIONAL V1
### Portal
Debe existir una home principal con tarjetas o botones para:
- PGC
- CRM
- Balón de Riesgo
- PGO
- configuración / admin / importaciones recientes si aplica

### CRM
Debe incluir como mínimo:
- lista de entidades
- detalle de entidad
- contactos por entidad
- relaciones entidad-producto
- registro de interacciones
- registro de tareas
- importador de entidades/clientes desde CSV/XLSX

### Risk
Debe incluir como mínimo:
- comando balón
- lista de clientes/operaciones en riesgo
- detalle de cliente de riesgo
- detalle de operación
- importador de snapshots operativos tipo leasing
- importador básico de estados financieros
- base para pagos programados, pagos realizados y contactos de cobranza

### PGO
Debe incluir como mínimo:
- dashboard PGO
- lista de tickets
- detalle de ticket
- resumen por período / usuario / unidad si alcanza
- importador de tickets
- base para reglas de puntos parametrizables

### PGC
No reconstruyas PGC completo. Solo:
- placeholder ordenado en el nuevo proyecto
- integración al menú principal
- app legacy_pgc1 para convivencia transitoria

## MODELO DE DATOS OBLIGATORIO
### Core
Debes implementar:
- Entidad
- Contacto
- Producto
- UnidadNegocio
- RelacionEntidadProducto
- DataDictionaryField
- DataImportBatch
- DataImportError

### CRM
Debes implementar:
- Interaccion
- Tarea
- NotaEntidad (si aporta y no complica)

### Risk
Debes implementar:
- RiskOperacion
- RiskOperationSnapshot
- EstadoFinanciero
- RiskPagoProgramado
- RiskPagoRealizado
- ContactoCobranza
- RiskAlerta

### PGO
Debes implementar:
- PgoTicket
- PgoMetricRule
- PgoPeriodScore
- PgoMonthlyAgg (si aporta y no complica demasiado)

## REGLAS FUNCIONALES OBLIGATORIAS
- El maestro común vive en core.
- Una entidad puede tener múltiples contactos.
- Una entidad puede tener múltiples productos/relaciones.
- Un snapshot de riesgo nunca sobrescribe otro snapshot de otra fecha.
- RiskOperationSnapshot es el corazón de Risk V1.
- PgoTicket debe guardar estado crudo y estado normalizado.
- La duración del ticket debe poder recalcularse si el archivo viene inconsistente.
- Toda carga debe quedar asociada a DataImportBatch.
- Toda fila inválida debe poder registrarse en DataImportError.
- La app debe quedar preparada para crecer luego a PostgreSQL sin rediseño mayor.

## PATRÓN DE CÓDIGO OBLIGATORIO
Organiza cada app con estructura clara. Si conviene, usa paquetes internos:
- models/
- views/
- services/
- selectors/
- imports/
- reports/
- tests/

Si el proyecto recién empieza, puedes comenzar con archivos simples por app, pero deja listo el patrón para crecer.

Reglas de código:
- No pongas lógica compleja en templates.
- No pongas lógica de negocio pesada en views.
- No crees utils.py genérico para todo.
- No crees clases abstractas innecesarias.
- Usa nombres explícitos.
- Mantén archivos razonablemente pequeños.
- Agrega Meta indexes y UniqueConstraint solo donde realmente aportan.

## IMPORTADORES V1
Debes preparar importadores para:
1. CRM entidades/clientes
2. Risk snapshots tipo leasing
3. Risk estados financieros básicos
4. PGO tickets

Cada importador debe:
- aceptar CSV/XLSX
- validar encabezados
- normalizar columnas
- crear o actualizar registros según clave natural
- registrar lote de importación
- registrar errores de fila
- devolver resumen de filas válidas / inválidas

## URLS MÍNIMAS
Quiero al menos este árbol:
- /
- /crm/entidades/
- /crm/entidades/<id>/
- /crm/contactos/
- /crm/tareas/
- /crm/importar/
- /risk/comando-balon/
- /risk/clientes/
- /risk/clientes/<id>/
- /risk/operaciones/<id>/
- /risk/importar-snapshots/
- /risk/importar-eeff/
- /pgo/
- /pgo/tickets/
- /pgo/tickets/<id>/
- /pgo/resultados/
- /pgo/reglas/
- /pgo/importar-tickets/
- /pgc/
- /legacy-pgc1/
- /admin/

## DISEÑO DE INTERFAZ
- Todo con Django templates y Bootstrap CDN.
- Diseño interno, sobrio, ejecutivo.
- Navbar superior común.
- Breadcrumb simple.
- Mensajes Django.
- Tablas limpias, filtros sencillos, botones claros.
- La home debe verse seria aunque no haya datos.

## ORDEN DE IMPLEMENTACIÓN
Trabaja en esta secuencia:
1. estructura de proyecto y settings
2. apps + INSTALLED_APPS
3. modelos core
4. modelos crm
5. modelos risk
6. modelos pgo
7. admin.py por app
8. urls.py globales y por app
9. views mínimas
10. templates base + home principal
11. importadores
12. datos de ejemplo mínimos o fixtures si ayudan
13. instrucciones para correr el proyecto

## FORMA DE RESPUESTA OBLIGATORIA
Responde exactamente en este orden:
1. resumen ejecutivo de lo que vas a construir
2. árbol de archivos
3. código completo solo de archivos nuevos o modificados
4. comandos para instalar y correr
5. checklist de pruebas manuales
6. notas técnicas y supuestos

## REGLA DE CONTROL DE CONTEXTO
Si el contexto se vuelve demasiado largo, NO resumes de forma vaga.
Divide tu entrega en fases concretas y entrega primero solo:
- settings
- urls globales
- modelos core
- modelos crm
- modelos risk
- modelos pgo
- admin básicos
Y espera confirmación para seguir con views, templates e importadores.

## CRITERIO DE CALIDAD
La solución debe ser:
- funcional
- clara
- mantenible
- demostrable en 15 días
- consistente con la arquitectura ya aprobada
- útil para luego integrar PGC y crecer a V1.1
```

## Prompt de seguimiento A

Después del prompt maestro, este es el mejor siguiente prompt para Cursor si quieres controlar el proceso por bloques:[cite:14]

```text
Continúa solo con la Fase A.
Quiero que generes exclusivamente:
- config/settings/base.py
- config/settings/local.py
- config/settings/production.py
- config/urls.py
- apps/core/models.py o apps/core/models/*
- apps/crm/models.py o apps/crm/models/*
- apps/risk/models.py o apps/risk/models/*
- apps/pgo/models.py o apps/pgo/models/*
- admin.py básicos por app

No generes todavía importadores, templates ni vistas complejas.
Entrega archivos completos y listos para copiar.
```

## Prompt de seguimiento B

Cuando Cursor termine la Fase A, usar este prompt:[cite:14]

```text
Ahora continúa con la Fase B.
Genera exclusivamente:
- urls.py por app
- views mínimas por app
- templates base.html y home principal
- placeholders de páginas mínimas por módulo
- navegación común Bootstrap
- mensajes y breadcrumbs simples

No generes todavía lógica compleja de reportes.
Entrega archivos completos.
```

## Prompt de seguimiento C

Y después, para volverlo útil con datos reales:[cite:14]

```text
Ahora continúa con la Fase C.
Genera exclusivamente:
- importador CRM entidades/clientes
- importador Risk snapshots leasing
- importador Risk estados financieros básicos
- importador PGO tickets
- formularios de carga
- vistas para subir archivo y ver resultado del lote
- registro de DataImportBatch y DataImportError

Entrega archivos completos y listos para probar.
```

## Qué no hacer con Cursor

No conviene usar este documento para pedirle a Cursor “todo de una vez” si el contexto del proyecto ya está largo, porque aumenta el riesgo de respuestas truncadas o de código inconsistente.[cite:14]

Tampoco conviene dejarle libertad para rediseñar arquitectura, porque esa parte ya está suficientemente decidida y volver a discutirla te quita tiempo de implementación real.[cite:14]

## Resultado esperado

Si este prompt maestro se usa bien, Cursor debería producir una base funcional real sobre la cual ya podrás iterar con archivos verdaderos, correcciones concretas y pulido para demo, que era justamente el propósito práctico de toda esta serie documental.[cite:14]
