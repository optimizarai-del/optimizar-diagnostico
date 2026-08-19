"""Generación del diagnóstico con Claude.

Dos decisiones que importan:

1. **Structured outputs.** Le pasamos el modelo Pydantic como `output_format`,
   así que la respuesta viene validada. No parseamos texto ni reintentamos por
   JSON roto.

2. **Prompt caching.** El contexto de marca (`vibe/`) es idéntico en cada
   diagnóstico, así que va en `system` con `cache_control` y se cobra ~10% a
   partir del segundo pedido. Lo único que cambia entre requests son las
   respuestas del formulario, que van en `messages` — después del breakpoint.
"""
import functools
import pathlib

import anthropic

from ..config import settings
from ..form_spec import TAREA_A_SOLUCION, respuestas_legibles
from ..schemas import ContenidoDiagnostico

VIBE_DIR = pathlib.Path(__file__).resolve().parent.parent / "vibe"


class DiagnosticoRechazado(Exception):
    """Los clasificadores de seguridad declinaron el pedido."""


@functools.lru_cache(maxsize=1)
def _contexto_vibe() -> str:
    """Concatena todos los .md de vibe/ en orden alfabético.

    Se cachea en memoria: el contenido tiene que ser byte-idéntico entre
    requests o se invalida el prompt cache. Si editás los .md, reiniciá el
    backend.
    """
    partes = [p.read_text(encoding="utf-8") for p in sorted(VIBE_DIR.glob("*.md"))]
    return "\n\n---\n\n".join(partes)


INSTRUCCIONES = """\
# Tu tarea

Sos el analista de Optimizar. Alguien completó el formulario de diagnóstico \
gratuito desde un anuncio. Con sus respuestas tenés que escribir un diagnóstico \
breve y honesto del estado operativo de su negocio.

Escribí para el dueño de la PyME, no para un técnico.

Castellano rioplatense, hablando de **vos**: nunca de tú ni de usted. Escribí \n"perdés", "tenés", "podés", "sabés", "creá", "armá", "fijate" — nunca \n"pierdes", "tienes", "puedes", "sabes", "crea", "arma", "fíjate". Tampoco \n"ustedes deben" ni "su empresa": es "tu empresa".

Le hablás a esa persona directamente. Nunca la menciones en tercera persona \nni repitas su nombre dentro del texto: no escribas "Gabriel dijo que...", \nescribí "me contaste que..." o simplemente "dijiste que...".

## Reglas que no se negocian

1. **No inventes nada: ni números ni hechos.** Todo lo que afirmes sobre el \nnegocio de esta persona tiene que estar en sus respuestas. Si respondió que usa \n"Excel y WhatsApp", no digas que usa Word, ni que manda PDFs, ni que los \nclientes piden cambios: no lo sabés. Toda cifra tiene que derivarse de lo que \nrespondió; si eligió "no tengo idea" en las horas, ese *es* el hallazgo, porque \nno se puede mejorar lo que no se mide. Nada de benchmarks de industria ni \nporcentajes de otros casos.

   Ante la duda, escribí qué habría que medir en vez de tapar el hueco con una \nsuposición verosímil. Una frase como "convendría medir cuánto tarda hoy un \npresupuesto" vale mucho más que un dato inventado: la persona conoce su negocio \ny detecta el invento al instante. Un solo detalle falso te tira abajo el \ndiagnóstico entero.

2. **No prometas resultados.** Podés decir "esto normalmente se resuelve en 3 a \
4 semanas". No podés decir "vas a ahorrar un 40%".

3. **Un solo caso, si suma.** Podés mencionar un caso real de `casos.md` cuando \
el rubro coincide. Nunca inventes un caso ni le pongas métricas que no estén \
documentadas.

4. **El quick win se regala de verdad.** Tiene que ser algo que la persona pueda \
hacer sola esta semana, sin contratarnos y sin comprar nada. Si es un anzuelo \
disfrazado, no sirve.

5. **La recomendación sale del catálogo de `oferta.md`.** Recomendá lo que \
Optimizar realmente construye, no una idea genérica de automatización.

6. **Nada de jerga.** Ni API, ni backend, ni LLM, ni embeddings. Sistema, \
agente, automatización, ahorro de tiempo, menos errores, más control.

7. Si las respuestas no alcanzan para un diagnóstico serio, decilo en el \
resumen y enfocá el diagnóstico en qué habría que medir primero.

## Tono

Directo sin ser frío. Confiado sin arrogancia. Nada de "transformamos tu \
negocio", "soluciones disruptivas" ni "con el poder de la IA". Si una frase \
podría venir de cualquier agencia de IA de LinkedIn, reescribila.
"""


def _cliente() -> anthropic.Anthropic:
    if not settings.ANTHROPIC_API_KEY:
        raise RuntimeError("Falta ANTHROPIC_API_KEY en el entorno")
    return anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


def _prompt_usuario(respuestas: dict, nombre: str | None) -> str:
    tareas = respuestas.get("tareas") or []
    pistas = [TAREA_A_SOLUCION[t] for t in tareas if t in TAREA_A_SOLUCION]

    bloques = [
        f"Nombre de quien completó el formulario: {nombre or 'no lo dejó'}",
        "",
        "## Respuestas del formulario",
        "",
        respuestas_legibles(respuestas),
    ]
    if pistas:
        bloques += [
            "",
            "## Servicios del catálogo que encajan con las tareas que eligió",
            "",
            *(f"- {p}" for p in pistas),
        ]
    bloques += ["", "Escribí el diagnóstico."]
    return "\n".join(bloques)


def generar(respuestas: dict, nombre: str | None = None) -> ContenidoDiagnostico:
    """Genera el diagnóstico. Lanza DiagnosticoRechazado si Claude declina."""
    cliente = _cliente()

    respuesta = cliente.messages.parse(
        model=settings.MODELO,
        max_tokens=16000,
        system=[
            {
                "type": "text",
                "text": (
                    "Trabajás para Optimizar. Este es el manual de la empresa: "
                    "leelo antes de escribir nada.\n\n" + _contexto_vibe()
                ),
            },
            {
                "type": "text",
                "text": INSTRUCCIONES,
                # Breakpoint: todo lo de arriba es idéntico en cada diagnóstico.
                "cache_control": {"type": "ephemeral"},
            },
        ],
        messages=[{"role": "user", "content": _prompt_usuario(respuestas, nombre)}],
        output_format=ContenidoDiagnostico,
    )

    # Los clasificadores de seguridad pueden declinar (HTTP 200 + refusal).
    # Hay que chequearlo antes de tocar el contenido.
    if respuesta.stop_reason == "refusal":
        raise DiagnosticoRechazado(
            getattr(respuesta.stop_details, "explanation", None) or "sin detalle"
        )

    if respuesta.parsed_output is None:
        raise RuntimeError(f"La respuesta no validó contra el esquema (stop_reason={respuesta.stop_reason})")

    return respuesta.parsed_output
