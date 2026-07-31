# Manual gerencial — Balón de Riesgo y Centro Gerencial

**Para:** dirección y gerencia de Working Capital Group  
**Sistema:** WCG One  
**Propósito:** saber qué mirar, en qué orden, con qué frecuencia — y leer de verdad, no solo “abrir la pantalla”.

---

## 1. Qué es este sistema (en una página)

WCG One reúne la información de la empresa en un solo lugar.  
Dos piezas trabajan juntas:

| Pieza | Pregunta que responde | Enfoque |
|--------|------------------------|---------|
| **Balón de Riesgo** | ¿Quién debe y qué tan grave está? | Operación crediticia y mora |
| **Centro Gerencial** | ¿Cómo va el negocio de intermediación? | Liquidez, fondeo, margen, utilidad |

También hay módulos de apoyo (PGC, PGO, CRM).  
Sirven al día a día comercial y operativo.  
Este manual se centra en **Balón + Centro Gerencial**.

### Idea simple

- El **Balón** mira la **cartera cliente por cliente**.  
- El **Centro Gerencial** mira la **institución** (factoraje, leasing y total).  
- Si solo mira uno, le falta la mitad de la foto.

---

## 2. Mapa rápido: qué hay en cada sitio

### Balón de Riesgo (`/risk/`)

1. **Comando Balón** — mora, alertas, operaciones que piden atención.  
2. **Evaluación de clientes** — lectura de riesgo por cliente.  
3. **Estados financieros institucionales** — cifras de la empresa (activo, utilidad, liquidez, apalancamiento).

### Centro Gerencial (`/gerencia/`)

1. **Intermediación** — el corazón del negocio: colocación, captación, margen, overhead, utilidad.  
2. **Liquidez** — ratios con bandas de referencia (“¿está bien o mal para una financiera como nosotros?”).  
3. **Estructura** — cómo está armado el fondeo y el patrimonio.  
4. **Comando** — pulso corto: finanzas + riesgo + operación.  
5. **Índices** — tabla de ratios con explicación.  
6. **What-if** — “¿qué pasa si crecemos X% o cambiamos tasas?”.  
7. **Detalle** — cifras trimestrales y series largas (cuando hace falta profundizar).

---

## 3. Disciplina de lectura (lo más importante)

El problema habitual no es la falta de reportes.  
Es que **no se leen con método**.

Proponga esta regla de casa:

> **Nadie dice “ya vi el sistema” sin haber contestado tres preguntas.**

### Las tres preguntas

1. **¿La intermediación está sana?** (margen y utilidad gerencial)  
2. **¿La liquidez y el fondeo están en zona razonable?** (bandas, no solo el número)  
3. **¿Hay fuego en la cartera?** (alertas y mora del Balón)

Si no puede responder las tres en cinco minutos, la revisión no terminó.

### Ritual sugerido (agenda fija)

| Quién | Cuándo | Duración | Qué abre |
|--------|--------|----------|----------|
| Gerencia general / financiera | **Día 3–5 hábil de cada mes** | 25–40 min | Centro Gerencial + Balón |
| Riesgo / cobranza | **Cada semana** (ej. lunes 20 min) | 15–25 min | Solo Balón (Comando) |
| Comité o dirección | **Una vez al mes** | 30–45 min | Comando gerencial + Intermediación + 5 alertas del Balón |

Póngalo en el calendario como reunión fija.  
No espere a “cuando haya tiempo”.

### Orden de pantallas (mensual)

Siga este orden. No salte al detalle primero.

```
1. Centro Gerencial → Comando          (3 min)  — pulso
2. Centro Gerencial → Intermediación   (8 min)  — el negocio
3. Centro Gerencial → Liquidez         (7 min)  — ¿estamos en zona?
4. Balón → Comando Balón               (8 min)  — ¿hay fuego?
5. Solo si hace falta → Estructura / Índices / What-if / EE.FF.
```

### Herramienta práctica: la hoja de 5 líneas

Al terminar la revisión, escriba (en correo, acta o chat interno) **solo esto**:

1. Período revisado (ej. junio 2026).  
2. Margen / utilidad gerencial: ¿subió o bajó?  
3. Liquidez: zona (óptimo / bajo / alto) y un número.  
4. Top 3 alertas del Balón (cliente o tema).  
5. Una decisión o seguimiento (dueño + fecha).

Si no hay esas 5 líneas, **no hubo revisión**.  
Esa es la disciplina.

---

## 4. Qué mirar primero, qué después

### Primera vez (conocer el sistema) — 45 minutos

1. Menú principal → **Centro Gerencial**.  
2. **Intermediación**: cambie Factoraje / Leasing / Total.  
3. **Liquidez**: lea las bandas y la tabla de peers.  
4. **Comando**: vea las tarjetas de señal.  
5. Menú → **Balón de Riesgo** → Comando Balón.  
6. Abra 2 o 3 operaciones en alerta.

### Cada mes (rutina) — 25–40 minutos

Use el orden de la sección 3.  
Termine con la hoja de 5 líneas.

### Cada semana (riesgo operativo) — 15–25 minutos

Solo Balón:

- ¿Cuántas alertas nuevas?  
- ¿Quién entró a mora ≥ 30?  
- ¿Qué acción quedó pendiente la semana pasada?

### Cuando hay duda o decisión grande

- **What-if** — antes de fijar metas de crecimiento.  
- **Estructura** — si cambia el fondeo o el patrimonio.  
- **Detalle / EE.FF.** — si necesita probar un número ante el consejo.

---

## 5. Frecuencia de la información

No todo se mueve igual.  
Ajuste la expectativa.

| Información | Frecuencia típica hoy | Dónde se ve |
|-------------|------------------------|-------------|
| Estados financieros / ratios / intermediación / liquidez / Z | **Mensual** (tras cierre e importación) | Centro Gerencial + EE.FF. del Balón |
| Metas y resultados comerciales (PGC) | **Mensual** | PGC |
| Tickets y SLA (PGO) | **Más frecuente** (al importar / operar) | PGO y tarjetas del Comando |
| Mora, alertas, operaciones (Balón) | **Puede ser semanal o al cargar archivo** | Comando Balón |
| CRM (contactos, seguimiento) | Según uso comercial | CRM |

### Mensaje claro para gerencia

- **Mensual** = lectura estratégica (intermediación, liquidez, estructura).  
- **Semanal** = lectura de riesgo operativo (Balón).  
- No espere que el margen de intermediación “cambie todos los días”.  
  Eso no es el ciclo del negocio.

---

## 6. Cómo “sí leer” los números (sin ser analista)

### No pregunte solo “¿subió o bajó?”

Pregunte:

- **¿Está en zona?** (verde / ámbar / rojo de las bandas)  
- **¿El cambio es estructural?** (salto grande de un mes a otro)  
- **¿Factoraje y leasing cuentan la misma historia?**

### Ejemplo útil

Si la liquidez baja de 1.8 a 1.2 y el apalancamiento casi no se mueve:

- No diga solo “bajó la liquidez”.  
- Diga: “cambió la estructura de corto plazo; el apalancamiento total no se disparó”.  
- Luego mire **Liquidez** (bandas) y **Estructura** (pasivo corto vs patrimonio).

### Utilidad contable vs gerencial

- **Contable:** no resta del todo el costo a inversionistas / preferentes.  
- **Gerencial:** sí lo refleja mejor para decidir.  
En Intermediación, use el modo **gerencial** para la reunión de dirección.

---

## 7. Roles sugeridos (quién es dueño de qué)

| Rol | Dueño de lectura | Entrega |
|-----|------------------|---------|
| Gerencia financiera | Centro Gerencial completo | Hoja de 5 líneas mensual |
| Riesgo / cobranza | Balón semanal | Lista de alertas + acciones |
| Comercial | PGC + CRM | Avance vs meta |
| Operaciones / TI | PGO | Tickets abiertos / SLA |
| Dirección | Comando + Intermediación + 3 alertas | Decisiones del mes |

Un solo dueño por ritual.  
Si “todos son dueños”, nadie lee.

---

## 8. Próximos desarrollos (prioridades)

Para que la gerencia lea más y mejor, afinar el proceso y el sistema en este orden:

### Prioridad A — ya ayuda a la disciplina

1. **Checklist mensual en pantalla** (las 3 preguntas + casilla “hoja de 5 líneas enviada”).  
2. **Resumen PDF o correo flash** el día 5: Comando + Intermediación + top alertas.  
3. **Recordatorio de calendario** ligado al cierre contable (no a la intuición).

### Prioridad B — más frecuencia donde sí importa

4. **Balón más fresco:** carga o refresco semanal de mora/alertas (aunque los EE.FF. sigan mensuales).  
5. **Semáforo del Comando** con fecha de “última actualización” por tarjeta (para no mezclar dato viejo con dato nuevo).

### Prioridad C — enriquecer el análisis

6. Intermediación con más detalle de productos y costos reales (menos estimación).  
7. Bandas y peers afinados con financieras locales comparables.  
8. What-if con escenarios guardados del comité (meta oficial del mes).

### Qué no priorizar primero

- Decenas de gráficos nuevos.  
- Reportes que nadie tiene dueño ni fecha de lectura.  
Primero **rito + resumen corto**. Después profundidad.

---

## 9. Ruta de 10 minutos (si solo hay una ventana corta)

1. Centro Gerencial → **Comando** (2 min).  
2. **Intermediación** Total, modo gerencial (3 min).  
3. **Liquidez**: mire zona de liquidez y Z (2 min).  
4. Balón → **alertas** (3 min).  
5. Escriba las 5 líneas.

Eso ya es una revisión gerencial útil.

---

## 10. Cierre

El sistema ya muestra el negocio y el riesgo juntos.  
El valor aparece cuando la gerencia:

- mira en **orden**,  
- con **frecuencia fija**,  
- y deja **constancia escrita** (5 líneas).

Sin eso, los dashboards son pantallas bonitas.  
Con eso, son una herramienta de dirección.

---

*Documento interno WCG — Centro Gerencial y Balón de Riesgo. Actualizar cuando cambien rituales o frecuencias de carga.*
