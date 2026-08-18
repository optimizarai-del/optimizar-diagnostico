"""Métricas del test A/B. Protegido con X-API-Key."""
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..models import Diagnostico, Evento

router = APIRouter(prefix="/api/metrics", tags=["metrics"])

# Orden del embudo, para leer el reporte de arriba hacia abajo
EMBUDO = [
    "landing_view",
    "form_start",
    "form_complete",
    "diagnostico_listo",
    "diagnostico_visto",
    "cta_whatsapp",
]


def _auth(x_api_key: str = Header(default="")) -> None:
    if not settings.ADMIN_API_KEY or x_api_key != settings.ADMIN_API_KEY:
        raise HTTPException(401, "No autorizado")


@router.get("/ab", dependencies=[Depends(_auth)])
def comparar(db: Session = Depends(get_db)):
    """Embudo completo por variante, más la distribución de calificación."""
    filas = (
        db.query(Evento.variante, Evento.tipo, func.count(Evento.id))
        .group_by(Evento.variante, Evento.tipo)
        .all()
    )
    conteos: dict[str, dict[str, int]] = {"a": {}, "b": {}}
    for variante, tipo, total in filas:
        if variante in conteos:
            conteos[variante][tipo] = total

    tiers = (
        db.query(Diagnostico.variante, Diagnostico.tier, func.count(Diagnostico.id))
        .group_by(Diagnostico.variante, Diagnostico.tier)
        .all()
    )
    calificacion: dict[str, dict[str, int]] = {"a": {}, "b": {}}
    for variante, tier, total in tiers:
        if variante in calificacion:
            calificacion[variante][tier] = total

    salida = {}
    for variante in ("a", "b"):
        c = conteos[variante]
        arranques = c.get("form_start", 0)
        completados = c.get("form_complete", 0)
        vistos = c.get("diagnostico_visto", 0)
        salida[variante] = {
            "embudo": {paso: c.get(paso, 0) for paso in EMBUDO},
            "tasa_completado": round(completados / arranques * 100, 1) if arranques else None,
            "tasa_lectura": round(vistos / completados * 100, 1) if completados else None,
            "tasa_cta": round(c.get("cta_whatsapp", 0) / vistos * 100, 1) if vistos else None,
            "calificacion": calificacion[variante],
        }
    return salida


@router.get("/leads", dependencies=[Depends(_auth)])
def leads(tier: str | None = None, limite: int = 50, db: Session = Depends(get_db)):
    """Los leads con su calificación — es lo que mira el equipo comercial."""
    q = db.query(Diagnostico).order_by(Diagnostico.creado_at.desc())
    if tier:
        q = q.filter(Diagnostico.tier == tier)
    return [
        {
            "token": d.token,
            "variante": d.variante,
            "nombre": d.nombre,
            "email": d.email,
            "telefono": d.telefono,
            "rubro": d.respuestas.get("rubro"),
            "tamano": d.respuestas.get("tamano"),
            "timing": d.respuestas.get("timing"),
            "prioridad": d.respuestas.get("prioridad"),
            "score": d.score,
            "tier": d.tier,
            "motivos": d.motivos,
            "estado": d.estado,
            "creado_at": d.creado_at,
        }
        for d in q.limit(limite).all()
    ]
