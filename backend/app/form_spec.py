"""Fuente de verdad del formulario en el backend.

El frontend renderiza desde `frontend/src/data/questions.js`; los IDs de pregunta
y los valores de opción tienen que coincidir con este archivo. Acá viven las
etiquetas en castellano (para armar el prompt de la IA) y los pesos de scoring.
"""

# --- Etiquetas: id de pregunta -> {valor: texto legible} ------------------

PREGUNTAS: dict[str, dict] = {
    "rubro": {
        "texto": "¿A qué se dedica tu empresa?",
        "opciones": {
            "contable": "Estudio contable / impositivo",
            "inmobiliaria": "Inmobiliaria",
            "construccion": "Constructora o desarrollador",
            "eventos": "Producción de eventos",
            "agro": "Agro",
            "comercio": "Comercio o distribuidora",
            "servicios": "Servicios profesionales",
            "salud": "Salud",
            "otro": "Otro",
        },
    },
    "provincia": {
        "texto": "¿En qué provincia operan?",  # solo se muestra si rubro = contable
        "opciones": {
            "la-pampa": "La Pampa",
            "buenos-aires": "Buenos Aires / CABA",
            "cordoba": "Córdoba",
            "santa-fe": "Santa Fe",
            "otra": "Otra provincia",
        },
    },
    "tamano": {
        "texto": "¿Cuántas personas trabajan con vos?",
        "opciones": {
            "solo": "Solo yo",
            "2-4": "2 a 4",
            "5-15": "5 a 15",
            "16-50": "16 a 50",
            "50+": "Más de 50",
        },
    },
    "rol": {
        "texto": "¿Cuál es tu rol?",
        "opciones": {
            "dueno": "Dueño o socio",
            "director": "Director o gerente general",
            "area": "Responsable de un área",
            "empleado": "Trabajo en la empresa",
        },
    },
    "tareas": {
        "texto": "¿Cuál de estas te come más tiempo?",
        "multiple": True,
        "opciones": {
            "consultas": "Responder consultas de clientes",
            "carga-datos": "Cargar datos a mano",
            "presupuestos": "Armar presupuestos o contratos",
            "cobranzas": "Perseguir cobranzas",
            "reportes": "Armar reportes",
            "coordinar": "Coordinar al equipo",
            "buscar-info": "Buscar información desparramada",
            "turnos": "Turnos y agenda",
        },
    },
    "horas": {
        "texto": "Entre todo el equipo, ¿cuántas horas por semana se van en eso?",
        "opciones": {
            "menos-5": "Menos de 5 horas",
            "5-10": "5 a 10 horas",
            "10-20": "10 a 20 horas",
            "20+": "Más de 20 horas",
            "no-se": "No tengo idea",
        },
    },
    "quien": {
        "texto": "¿Quién lo hace hoy?",
        "opciones": {
            "yo-mismo": "Yo mismo",
            "una-persona": "Una persona del equipo",
            "varias": "Varias personas",
            "a-medias": "Se hace a medias, cuando se puede",
        },
    },
    "canales": {
        "texto": "¿Por dónde te llegan los clientes nuevos?",
        "multiple": True,
        "opciones": {
            "whatsapp": "WhatsApp",
            "redes": "Instagram o Facebook",
            "web": "La web",
            "telefono": "Teléfono",
            "referidos": "Referidos",
            "presencial": "Presencial",
            "salgo-a-buscar": "No me llegan solos, salgo a buscarlos",
        },
    },
    "respuesta": {
        "texto": "Cuando entra una consulta, ¿en cuánto responden?",
        "opciones": {
            "minutos": "En minutos",
            "horas": "En horas",
            "dia-siguiente": "Al día siguiente",
            "depende": "Depende del día",
            "se-pierden": "A veces se nos pierden",
        },
    },
    "seguimiento": {
        "texto": "¿Le hacés seguimiento al que consultó y no compró?",
        "opciones": {
            "sistematico": "Sí, sistemático",
            "a-veces": "A veces, cuando me acuerdo",
            "no": "No",
        },
    },
    "sistemas": {
        "texto": "¿Con qué trabajan hoy?",
        "multiple": True,
        "opciones": {
            "excel": "Excel o Google Sheets",
            "whatsapp": "WhatsApp",
            "papel": "Papel o cuaderno",
            "erp": "Un sistema de gestión / ERP",
            "crm": "Un CRM",
            "cada-uno": "Cada uno con lo suyo",
        },
    },
    "trazabilidad": {
        "texto": (
            "Si ahora necesitás saber cuánto facturaste este mes "
            "o qué te debe un cliente, ¿cuánto tardás?"
        ),
        "opciones": {
            "al-toque": "Lo veo al toque",
            "minutos": "Unos minutos",
            "pedirlo": "Se lo tengo que pedir a alguien",
            "no-puedo": "No lo puedo saber con certeza",
        },
    },
    "prioridad": {
        "texto": "Si pudieras resolver una sola cosa en los próximos 3 meses, ¿cuál sería?",
        "abierta": True,
    },
    "timing": {
        "texto": "¿Para cuándo?",
        "opciones": {
            "ya": "Ya, es urgente",
            "1-3-meses": "En 1 a 3 meses",
            "este-ano": "Este año",
            "mirando": "Estoy mirando nomás",
        },
    },
}


# --- Pesos de calificación (no los ve el prospecto) ------------------------

PESOS: dict[str, dict[str, int]] = {
    "tamano": {"solo": -30, "2-4": 0, "5-15": 25, "16-50": 25, "50+": 5},
    "rol": {"dueno": 25, "director": 20, "area": 5, "empleado": -20},
    "horas": {"menos-5": 0, "5-10": 10, "10-20": 20, "20+": 25, "no-se": 10},
    "quien": {"yo-mismo": 12, "una-persona": 5, "varias": 8, "a-medias": 10},
    "respuesta": {
        "minutos": 0,
        "horas": 5,
        "dia-siguiente": 10,
        "depende": 10,
        "se-pierden": 20,
    },
    "seguimiento": {"sistematico": 0, "a-veces": 6, "no": 10},
    "trazabilidad": {"al-toque": 0, "minutos": 5, "pedirlo": 12, "no-puedo": 18},
    "timing": {"ya": 25, "1-3-meses": 20, "este-ano": 8, "mirando": -15},
}

# Qué categoría de `oferta.md` sugiere cada tarea. Lo usa la IA como pista.
TAREA_A_SOLUCION: dict[str, str] = {
    "consultas": "Agente de atención al cliente 24/7 (WhatsApp) — Prioridad 1",
    "carga-datos": "Carga de datos desde el campo / automatización n8n — Prioridad 2",
    "presupuestos": "Presupuestos y contratos automáticos — Prioridad 6",
    "cobranzas": "Recuperador de leads fríos + notificaciones automáticas — Prioridad 1 y 2",
    "reportes": "Reportes automáticos + dashboard de KPIs — Prioridad 3",
    "coordinar": "Dashboard ejecutivo + agente interno de consulta — Prioridad 3",
    "buscar-info": "Buscador inteligente de documentos + agente interno — Prioridad 6",
    "turnos": "Agente de reservas y turnos — Prioridad 1",
}


def etiqueta(pregunta_id: str, valor: str) -> str:
    """Devuelve el texto legible de una opción (o el valor crudo si no existe)."""
    pregunta = PREGUNTAS.get(pregunta_id, {})
    return pregunta.get("opciones", {}).get(valor, valor)


def respuestas_legibles(respuestas: dict) -> str:
    """Convierte las respuestas crudas en el bloque de texto que lee la IA."""
    lineas: list[str] = []
    for pid, definicion in PREGUNTAS.items():
        if pid not in respuestas:
            continue
        valor = respuestas[pid]
        if definicion.get("abierta"):
            texto = str(valor).strip() or "(sin respuesta)"
        elif isinstance(valor, list):
            texto = ", ".join(etiqueta(pid, v) for v in valor) or "(ninguna)"
        else:
            texto = etiqueta(pid, valor)
        lineas.append(f"- {definicion['texto']}\n  → {texto}")
    return "\n".join(lineas)
