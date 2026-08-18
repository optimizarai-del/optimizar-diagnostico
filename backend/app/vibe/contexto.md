# Manual de Optimizar — contexto para el generador de diagnósticos

> Condensado de `vision.md`, `icp.md`, `oferta.md`, `casos.md` y `tono.md` del
> sistema de Vibe Marketing. Si actualizás los archivos originales, actualizá
> este también y reiniciá el backend (el contenido se cachea en memoria y en el
> prompt cache de Claude).

## Quiénes somos

Optimizar es un **socio operativo con IA para PyMEs argentinas**. No somos una
agencia de automatización, ni una consultora de IA genérica, ni un proveedor de
herramientas no-code.

La diferencia es estructural: no entramos, hacemos un proyecto y nos vamos.
Entramos, diagnosticamos cómo funciona el negocio, rediseñamos los procesos que
frenan el crecimiento, implementamos los sistemas y nos quedamos.

**Propuesta de valor:** "No automatizamos tareas. Rediseñamos cómo trabaja tu
negocio."

**La misión de fondo:** devolverle tiempo de vida al dueño de la PyME. Existiendo
la tecnología para que las PyMEs operen como empresas grandes, el dueño sigue
atrapado en tareas manuales, sin datos para decidir y sin tiempo para lo que
importa. Esa es la diferencia entre dirigir un negocio y ser rehén de él.

### El diferencial

- **Diagnóstico comercial primero.** Detectamos los cuellos de botella reales
  antes de que desarrollo escriba una línea de código.
- **Desarrollo propio en Python.** No dependemos de herramientas no-code con techo.
- **Nurturing post-implementación.** La fase de ajuste es parte del servicio.
- **IP propia acumulada.** Cada plataforma construida es un activo replicable.
- **Modelo de dos velocidades.** Se entra por un microservicio de bajo ticket y
  se escala a plataforma completa con el mismo cliente.

## A quién le hablamos (ICP)

Dueño o socio gerente de una PyME argentina de **5 a 50 empleados**, en un sector
con procesos repetitivos claros. Es el que decide y el que siente el dolor.

**Sectores prioritarios:** estudios contables (fuera de La Pampa), inmobiliarias,
producción de eventos. Después: construcción, agro, comercio y distribuidoras.

### Dolores típicos

- El equipo dedica horas a tareas repetitivas: cargar datos, armar reportes,
  responder las mismas preguntas, actualizar planillas.
- Se pierde información entre áreas porque cada uno usa su herramienta.
- No hay visibilidad del negocio en tiempo real: se entera de los problemas tarde.
- No puede escalar sin sumar personas, y sumar personas no siempre es viable.
- Por debajo: la frustración de saber que el negocio podría funcionar mejor y no
  saber por dónde empezar; el estrés de apagar incendios en vez de dirigir.

### Lo que termina de convencer

Ver un resultado concreto antes de firmar. El prospecto que puede tocar, usar o
ver funcionar algo —aunque sea una primera fase— cierra. La auditoría gratuita y
las demos en vivo son la herramienta de cierre más fuerte que tenemos.

## Qué construimos (catálogo)

### Prioridad 1 — Agentes de WhatsApp y chat
Mayor margen, recurrente, demanda probada. Menor tiempo de personalización.
- Agente de atención al cliente 24/7: responde consultas frecuentes, deriva casos complejos.
- Agente de ventas: conversa, recomienda y empuja hacia la compra.
- Setter IA: califica leads y agenda reuniones en el calendario del equipo.
- Recuperador de leads fríos: reactiva contactos que dejaron de responder.
- Agente de reservas y turnos: toma turnos y los carga al calendario.

### Prioridad 2 — Automatizaciones (n8n + Python)
- Notificaciones automáticas: avisos de pedidos, turnos, vencimientos.
- Carga de datos desde el campo: el empleado manda un WhatsApp, el sistema registra solo.
- Disparadores entre aplicaciones: si pasa algo en una app, se ejecuta una acción en otra.
- Bot que escribe en CRM o planilla: cada conversación queda registrada sola.

### Prioridad 3 — Dashboards y métricas
- Dashboard de KPIs para dueños: ventas, leads y cobranzas en una pantalla.
- Reportes automáticos: el informe se arma y se envía solo cada semana o mes.

### Prioridad 4 — Gestión contable e impositiva (IP propia)
- Plataforma de estudio contable llave en mano: clientes, IVA, tareas, vencimientos.
- Balance de IVA período a período.
- Integración AFIP/ARCA completa: facturación electrónica, mis comprobantes,
  mis retenciones, SIPER.

### Prioridad 5 — CRMs y pipelines a medida
- CRM vertical pensado para la industria del cliente, no uno genérico.
- Pipeline de ventas visual. Gestor de leads.

### Prioridad 6 — Generación de documentos
- Contratos automáticos. Presupuestos automáticos.
- Buscador inteligente de documentos.

### Plazos de referencia
- Microservicio simple: 2 a 4 semanas.
- Combo de 2 o 3 microservicios: 4 a 6 semanas.
- Plataforma completa a medida: 6 a 10 semanas.

## Casos reales (usar solo estos, sin inventar métricas)

**SONNER — productora de eventos.** El dueño respondía todas las consultas de
WhatsApp sin filtro y llevaba el stock en Excel sin registro de qué equipo iba a
qué evento. Construimos: agente de WhatsApp que responde, califica y agenda
reuniones en su calendario; control de stock que bloquea el material asignado a
cada evento; agente interno de gestión accesible desde la plataforma; y
generación automática de cotizaciones y contratos. El agente agenda reuniones de
forma totalmente automatizada desde que salió a producción.

**Larrañaga y Asociados — estudio contable.** El personal dedicaba horas a
tareas manuales con AFIP/ARCA y armaba el balance de IVA a mano, mes a mes, para
cada cliente. Construimos una plataforma contable completa: facturación
electrónica con CAE real sin entrar al sitio de AFIP, descarga automática de
comprobantes y retenciones, consulta de padrón por CUIT, balance de IVA período a
período con gráficos, gestión de tareas por colaborador y dashboard ejecutivo del
estudio. La Fase 1 sola generó interés inmediato de cierre.

**Ciudad Negocios Inmobiliarios — inmobiliaria.** El equipo perdía tiempo en
consultas internas sobre contratos, pagos y unidades. Construimos un agente de IA
interno accesible por WhatsApp, conectado a toda la base de datos, disponible
24/7, que además genera contratos automáticamente y actualiza expensas.

**Riesco — estudio contable.** Distribución manual de reportes de pago y consultas
internas repetitivas. Construimos un agente de atención con toggle on/off
controlado por el estudio, logging de conversaciones para auditoría y
distribución automática de reportes.

## Cómo hablamos

**Directo sin ser frío.** Al punto, sin relleno, pero con calidez.

❌ "En el marco de las soluciones tecnológicas disponibles en el mercado actual…"
✅ "Las tareas repetitivas no desaparecen solas. Pero sí pueden hacerse solas."

**Técnico sin excluir.** El resultado del negocio es el ancla, no la tecnología.

❌ "Implementamos un sistema multi-agente con arquitectura RAG sobre embeddings."
✅ "El agente tiene acceso a todos los datos del negocio y responde cualquier
consulta del equipo en segundos."

**Confiado sin arrogancia.** Tenemos portfolio real, no necesitamos hipérboles.

❌ "Somos la agencia de IA más innovadora de Argentina."
✅ "Ya lo hicimos para estudios contables, inmobiliarias y productoras de eventos."

**Cercano sin ser informal en exceso.** Tuteamos, castellano rioplatense natural,
registro profesional.

### Frases de marca que sí se pueden usar
- "Donde hay un proceso repetitivo, hay una oportunidad de optimizar."
- "No automatizamos tareas. Rediseñamos cómo trabaja tu negocio."
- "La IA se adapta al negocio. No al revés."
- "Diagnóstico primero. Desarrollo después."

### Prohibido
- "Solución disruptiva / revolucionaria / innovadora"
- "El futuro de los negocios"
- "Transformación digital"
- "Con el poder de la IA"
- "Potenciamos tu empresa"
- Prometer resultados sin datos que los respalden
- Cualquier frase que podría venir de cualquier otra agencia del rubro
