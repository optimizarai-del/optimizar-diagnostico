# Optimizar — Diagnóstico

Landing + formulario de diagnóstico operativo. Genera el diagnóstico con Claude,
lo entrega por email o WhatsApp según la variante del test A/B, y termina en un
CTA a WhatsApp donde el agente califica al prospecto e intenta agendar una
llamada.

## Cómo funciona

```
Anuncio A ──┐                          ┌─→ nombre + email    ─→ mail con link
            ├─→ Landing → 13 preguntas ─┤
Anuncio B ──┘                          └─→ nombre + teléfono ─→ abre WhatsApp
                     │                                                │
                     ↓                                                ↓
              Supabase: respuestas + score                  Página /d/{token}
                     │                                                │
                     ↓                                    [ Hablar por WhatsApp ]
              Claude genera el diagnóstico                            │
              (contexto: app/vibe/)                                   ↓
                                                       Agente califica y agenda
```

## Arranque local

**Backend**

```bash
cd backend
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt     # Linux/Mac: .venv/bin/pip
cp .env.example .env                              # completar ANTHROPIC_API_KEY
.venv/Scripts/uvicorn app.main:app --reload --port 8000
```

API en `http://localhost:8000` · Swagger en `/docs`

**Frontend**

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173
```

Vite proxea `/api/*` al backend. Las tablas se crean solas al arrancar.

## El test A/B

Las dos variantes comparten landing y formulario. Lo único que cambia es la
pantalla de captura y el canal de entrega.

| | Variante A | Variante B |
|---|---|---|
| URL del anuncio | `/?v=a` | `/?v=b` |
| Captura | Nombre + email | Nombre + teléfono |
| Entrega | Mail con link a `/d/{token}` | Abre WhatsApp con el mensaje escrito |
| Riesgo | El mail puede caer en spam | Requiere que la persona toque "enviar" |

Sin `?v=`, se sortea 50/50 y se guarda en `sessionStorage` para que un refresh
no cambie de rama a mitad del formulario.

### Por qué B no manda el mensaje solo

WhatsApp no deja escribirle primero a alguien con texto libre: fuera de la
ventana de 24 h hace falta una plantilla aprobada por Meta, y esa aprobación
tarda días. Acá el prospecto abre la conversación él, con el mensaje ya escrito.
Eso abre la ventana y podemos responderle sin plantilla.

Capturamos el número igual (lo escribe en el formulario) y el lead llega mejor
calificado, porque ya hizo el gesto de contactarnos. Cuando haya volumen se
migra a YCloud o Meta Cloud API y solo cambia `services/whatsapp.py`.

### Métricas

```bash
curl -H "X-API-Key: $ADMIN_API_KEY" http://localhost:8000/api/metrics/ab
curl -H "X-API-Key: $ADMIN_API_KEY" "http://localhost:8000/api/metrics/leads?tier=verde"
```

`/metrics/ab` devuelve el embudo por variante — vista, arranque, completado,
generado, leído, click al CTA — más la distribución de calificación.

Los `utm_*` de la URL se guardan con cada lead, así que se cruzan con Meta Ads
sin trabajo extra.

## El formulario

13 preguntas, una por pantalla, ~2 minutos. Casi todas de un toque.

Están definidas en dos lugares que **tienen que mantenerse sincronizados**:

- `frontend/src/data/questions.js` — lo que se renderiza
- `backend/app/form_spec.py` — etiquetas para la IA y pesos de calificación

Los IDs de pregunta y los valores de opción son los que unen ambos lados. Si
agregás una pregunta, tocá los dos archivos y después corré:

```bash
cd backend && python check_sync.py
```

Compara los dos archivos y falla si se desincronizaron. Vale la pena porque el
síntoma es silencioso: el scoring puntúa mal y la IA recibe valores crudos en
vez de texto legible, sin que nada tire error.

La pregunta de provincia solo aparece si el rubro es contable: sirve para
aplicar la exclusión territorial con Larrañaga y Asociados.

## La calificación

Cada respuesta suma o resta (`backend/app/scoring.py`). El prospecto nunca la
ve — es para el agente de WhatsApp.

| Tier | Qué significa |
|---|---|
| 🟢 verde | 5–50 empleados, dueño, +10 h/semana perdidas, urgencia → agendar |
| 🟡 amarillo | Encaja pero sin urgencia, o no es el decisor → nutrir |
| 🔴 rojo | Unipersonal, +50 empleados o "estoy mirando nomás" → diagnóstico sin llamada |

**Exclusión dura:** estudio contable radicado en La Pampa se marca rojo
automáticamente, por la exclusividad territorial con Larrañaga.

## El generador

`backend/app/services/ai.py`. Dos decisiones:

**Structured outputs.** El modelo Pydantic va como `output_format`, así que la
respuesta viene validada. No parseamos texto ni reintentamos por JSON roto.

**Prompt caching.** El contexto de marca (`app/vibe/`) es idéntico en cada
diagnóstico, así que va en `system` con `cache_control` y se cobra ~10% a partir
del segundo pedido. Lo único que cambia entre requests son las respuestas del
formulario, que van en `messages` — después del breakpoint.

Editar los `.md` de `app/vibe/` cambia el diagnóstico sin tocar código. Después
de editarlos hay que reiniciar el backend: el contenido se cachea en memoria
para que sea byte-idéntico entre requests (si cambia, se invalida el prompt
cache).

> **Nota:** el `CLAUDE.md` de OPTIMIZAR-PLATAFORMA prohíbe usar la API de
> Anthropic y obliga al scheduled agent con polling invertido. Para el funnel de
> prospección tiene sentido. Acá no: el diagnóstico tiene que llegar en dos
> minutos, no cuando corra el próximo ciclo. Es una excepción consciente.

## Producción

```bash
docker compose up -d --build
```

Backend en 8000, frontend servido por nginx en 80. Para EasyPanel, apuntar cada
servicio a su Dockerfile y cargar el `.env` del backend como variables de
entorno.

**Antes de publicar:**

- [ ] `ANTHROPIC_API_KEY` cargada
- [ ] `PUBLIC_URL` apuntando al dominio real (se usa en el link del mail)
- [ ] `WHATSAPP_NUMERO` con código de país y sin el 15
- [ ] `DATABASE_URL` de Supabase
- [ ] SPF, DKIM y DMARC del dominio de envío
- [ ] `ADMIN_API_KEY` puesta (sin ella, `/metrics` devuelve 401 siempre)
