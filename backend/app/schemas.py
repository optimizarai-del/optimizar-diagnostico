"""Modelos Pydantic: request/response de la API y la forma del diagnóstico
que la IA está obligada a devolver (structured outputs)."""
from typing import Literal

from pydantic import BaseModel, Field


# --- Entrada del formulario ----------------------------------------------

class DiagnosticoCrear(BaseModel):
    variante: Literal["a", "b"]
    respuestas: dict
    nombre: str = Field(min_length=1, max_length=120)
    email: str | None = None
    telefono: str | None = None
    utm: dict = Field(default_factory=dict)


class EventoCrear(BaseModel):
    tipo: str
    variante: str | None = None
    token: str | None = None
    datos: dict = Field(default_factory=dict)


# --- Forma del diagnóstico que genera la IA -------------------------------
# Estos modelos se pasan como `output_format` a Claude, así que la respuesta
# viene validada: no hay que parsear texto ni reintentar por JSON roto.

class CuelloBotella(BaseModel):
    titulo: str = Field(description="El cuello de botella en 4-8 palabras")
    descripcion: str = Field(
        description=(
            "2-3 oraciones. Explica qué pasa hoy y por qué cuesta plata o tiempo. "
            "Usá los números que dio el prospecto; nunca inventes cifras."
        )
    )
    impacto: str = Field(
        description=(
            "El impacto estimado en una frase corta, derivado SOLO de lo que "
            "respondió. Ej: '~14 horas por semana del equipo'. Si no dio datos "
            "suficientes, decí qué habría que medir en vez de estimar."
        )
    )


class Recomendacion(BaseModel):
    titulo: str = Field(description="Qué automatizaría primero, en una frase")
    descripcion: str = Field(description="2-4 oraciones: qué se construye y cómo cambia el día a día")
    plazo: str = Field(description="Tiempo estimado de implementación. Ej: '3 a 4 semanas'")


class QuickWin(BaseModel):
    titulo: str = Field(description="Algo que puede hacer solo esta semana, sin contratar a nadie")
    pasos: list[str] = Field(description="2 a 4 pasos concretos y accionables")


class ContenidoDiagnostico(BaseModel):
    titular: str = Field(
        description=(
            "El hallazgo principal en una frase con su número. "
            "Ej: 'Tu equipo pierde unas 14 horas por semana respondiendo lo mismo.'"
        )
    )
    resumen: str = Field(description="2-3 oraciones que enmarcan la situación general del negocio")
    cuellos: list[CuelloBotella] = Field(description="Exactamente 3 cuellos de botella")
    recomendacion: Recomendacion
    quick_win: QuickWin
    cierre: str = Field(description="Una o dos oraciones antes del botón de WhatsApp. Sin presión.")


# --- Salida de la API -----------------------------------------------------

class DiagnosticoPublico(BaseModel):
    """Lo que se devuelve en /api/diagnostico/{token}. Sin score ni datos internos."""

    token: str
    estado: str
    nombre: str | None = None
    contenido: ContenidoDiagnostico | None = None
    whatsapp_url: str | None = None
