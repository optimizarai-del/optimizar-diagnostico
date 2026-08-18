"""Calificación del lead contra el ICP.

El resultado no se le muestra al prospecto: es lo que lee el agente de WhatsApp
para saber con quién está hablando antes de intentar agendar.
"""
from .form_spec import PESOS

# Verde  → agendar llamada de diagnóstico ya
# Amarillo → encaja pero sin urgencia; nutrir, no forzar
# Rojo   → recibe el diagnóstico igual, no se le ofrece llamada
UMBRAL_VERDE = 85
UMBRAL_AMARILLO = 45


def calificar(respuestas: dict) -> tuple[int, str, list[str]]:
    """Devuelve (score, tier, motivos)."""
    score = 0
    motivos: list[str] = []

    for pregunta_id, tabla in PESOS.items():
        valor = respuestas.get(pregunta_id)
        if isinstance(valor, str):
            score += tabla.get(valor, 0)

    # --- Exclusión dura (contractual, no negociable) ----------------------
    # Exclusividad territorial con Larrañaga y Asociados: no prospectar
    # estudios contables radicados en La Pampa. Otros rubros sí están permitidos.
    if respuestas.get("rubro") == "contable" and respuestas.get("provincia") == "la-pampa":
        return score, "rojo", ["Exclusión contractual: estudio contable en La Pampa"]

    # --- Señales de alarma de icp.md -------------------------------------
    if respuestas.get("tamano") == "solo":
        motivos.append("Unipersonal: fuera del rango 5-50 empleados del ICP")
    if respuestas.get("tamano") == "50+":
        motivos.append("Más de 50 empleados: probablemente tenga área de IT propia")
    if respuestas.get("rol") == "empleado":
        motivos.append("No es el decisor")
    if respuestas.get("timing") == "mirando":
        motivos.append("Sin intención de compra declarada")

    # --- Señales a favor --------------------------------------------------
    if respuestas.get("respuesta") == "se-pierden":
        motivos.append("Pierde consultas: dolor agudo y cuantificable")
    if respuestas.get("horas") in ("10-20", "20+"):
        motivos.append("Más de 10 h/semana perdidas en una sola tarea")
    if respuestas.get("quien") == "yo-mismo":
        motivos.append("El dueño hace la tarea él mismo")
    if respuestas.get("timing") == "ya":
        motivos.append("Urgencia declarada")

    if score >= UMBRAL_VERDE:
        tier = "verde"
    elif score >= UMBRAL_AMARILLO:
        tier = "amarillo"
    else:
        tier = "rojo"

    return score, tier, motivos
