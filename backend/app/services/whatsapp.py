"""WhatsApp — fase 1: click-to-chat.

No usamos la API de Meta todavía, y es a propósito. WhatsApp no deja escribirle
primero a alguien con texto libre: fuera de la ventana de 24 h hace falta una
plantilla aprobada por Meta, y esa aprobación tarda días.

Acá el prospecto abre la conversación él (con el mensaje ya escrito). Eso abre
la ventana de 24 h y podemos responderle libremente. Capturamos el número igual
—cuando escribe— y el lead es mejor porque ya hizo el gesto de contactarnos.

Cuando haya volumen se migra a YCloud / Meta Cloud API y solo cambia este módulo.
"""
from urllib.parse import quote

from ..config import settings


def link_conversacion(token: str, tier: str = "amarillo", contexto: str = "diagnostico") -> str:
    """Link wa.me con el mensaje precargado.

    El token va en el mensaje: cuando la persona escribe, el agente de WhatsApp
    lo levanta, busca el diagnóstico y ya sabe con quién habla y cómo calificó.
    """
    if contexto == "captura":
        texto = f"Hola, completé el diagnóstico y quiero recibirlo. Código: {token}"
    else:
        texto = f"Hola, leí mi diagnóstico y quiero avanzar. Código: {token}"
    return f"https://wa.me/{settings.WHATSAPP_NUMERO}?text={quote(texto)}"
