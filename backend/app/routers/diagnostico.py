"""Endpoints públicos: recibir el formulario, generar y servir el diagnóstico."""
import logging
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..config import settings
from ..database import SessionLocal, get_db
from ..models import Diagnostico, Evento, Solicitud
from ..schemas import DiagnosticoCrear, DiagnosticoPublico, EventoCrear
from ..scoring import calificar
from ..services import ai, email, whatsapp

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["diagnostico"])


def _ahora() -> datetime:
    return datetime.now(timezone.utc)


def _registrar(db: Session, tipo: str, variante: str | None, diagnostico_id: int | None = None, **datos) -> None:
    db.add(Evento(tipo=tipo, variante=variante, diagnostico_id=diagnostico_id, datos=datos))
    db.commit()


# --- Límites del endpoint público ----------------------------------------

def _ip_cliente(request: Request) -> str:
    """IP real del visitante.

    Detrás de Traefik el `request.client.host` es el del proxy, así que el dato
    bueno está en X-Forwarded-For. Traefik va agregando al final, por lo que el
    primer elemento es el cliente original.
    """
    reenviado = request.headers.get("x-forwarded-for", "")
    if reenviado:
        return reenviado.split(",")[0].strip()[:64]
    return request.client.host[:64] if request.client else "desconocido"


def _verificar_limite(db: Session, ip: str) -> None:
    """Corta el request con 429 si se pasó de los topes configurados.

    Se cuenta lo aceptado, no lo intentado: una persona real que completa el
    formulario una vez nunca lo ve.
    """
    ahora = _ahora()
    desde_dia = ahora - timedelta(days=1)
    desde_hora = ahora - timedelta(hours=1)

    def _contar(*filtros) -> int:
        return db.query(func.count(Solicitud.id)).filter(*filtros).scalar() or 0

    if _contar(Solicitud.creado_at >= desde_dia) >= settings.LIMITE_GLOBAL_DIA:
        log.error("Tope global diario alcanzado (%s). Endpoint cerrado por hoy.",
                  settings.LIMITE_GLOBAL_DIA)
        raise HTTPException(
            429,
            "Estamos recibiendo muchas consultas hoy. Escribinos por WhatsApp y "
            "te hacemos el diagnóstico igual.",
            headers={"Retry-After": "3600"},
        )

    if _contar(Solicitud.ip == ip, Solicitud.creado_at >= desde_dia) >= settings.LIMITE_IP_DIA:
        raise HTTPException(
            429,
            "Ya hiciste varios diagnósticos hoy. Si necesitás otro, escribinos por WhatsApp.",
            headers={"Retry-After": "86400"},
        )

    if _contar(Solicitud.ip == ip, Solicitud.creado_at >= desde_hora) >= settings.LIMITE_IP_HORA:
        raise HTTPException(
            429,
            "Esperá un rato antes de mandar otro diagnóstico. Si es urgente, escribinos por WhatsApp.",
            headers={"Retry-After": "3600"},
        )


# --- Generación en background --------------------------------------------

def _procesar(diagnostico_id: int) -> None:
    """Genera el diagnóstico y lo entrega. Corre fuera del request.

    Sesión propia: la del request ya está cerrada cuando esto arranca.
    """
    db = SessionLocal()
    try:
        d = db.get(Diagnostico, diagnostico_id)
        if d is None or d.estado != "pendiente":
            return

        d.estado = "generando"
        db.commit()

        try:
            contenido = ai.generar(d.respuestas, d.nombre)
        except ai.DiagnosticoRechazado as exc:
            log.warning("Diagnóstico %s rechazado por los clasificadores: %s", d.token, exc)
            d.estado, d.error = "error", f"rechazado: {exc}"
            db.commit()
            return
        except Exception as exc:  # noqa: BLE001 — cualquier fallo deja rastro
            log.exception("Falló la generación del diagnóstico %s", d.token)
            d.estado, d.error = "error", str(exc)
            db.commit()
            return

        d.contenido = contenido.model_dump()
        d.estado = "listo"
        d.generado_at = _ahora()
        db.commit()
        _registrar(db, "diagnostico_listo", d.variante, d.id)

        # Variante A: se lo mandamos por mail.
        # Variante B: no mandamos nada — el prospecto ya abrió WhatsApp desde el
        # último paso del formulario y el agente responde con el link.
        if d.variante == "a" and d.email:
            url = f"{settings.PUBLIC_URL}/d/{d.token}"
            try:
                email.enviar(d.email, d.nombre or "Hola", contenido, url)
                d.entregado_at = _ahora()
                db.commit()
                _registrar(db, "email_enviado", d.variante, d.id)
            except Exception:  # noqa: BLE001
                log.exception("No se pudo enviar el mail del diagnóstico %s", d.token)
    finally:
        db.close()


# --- Endpoints ------------------------------------------------------------

@router.post("/diagnostico", status_code=201)
def crear(
    payload: DiagnosticoCrear,
    tareas: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    ip = _ip_cliente(request)
    _verificar_limite(db, ip)

    if payload.variante == "a" and not payload.email:
        raise HTTPException(422, "La variante A necesita email")
    if payload.variante == "b" and not payload.telefono:
        raise HTTPException(422, "La variante B necesita teléfono")

    score, tier, motivos = calificar(payload.respuestas)
    token = secrets.token_urlsafe(9)

    d = Diagnostico(
        token=token,
        variante=payload.variante,
        utm=payload.utm,
        respuestas=payload.respuestas,
        score=score,
        tier=tier,
        motivos=motivos,
        nombre=payload.nombre.strip(),
        email=(payload.email or "").strip() or None,
        telefono=(payload.telefono or "").strip() or None,
    )
    db.add(d)
    db.add(Solicitud(ip=ip))
    db.commit()
    db.refresh(d)

    _registrar(db, "form_complete", d.variante, d.id, tier=tier, score=score)
    tareas.add_task(_procesar, d.id)

    return {
        "token": d.token,
        "url": f"{settings.PUBLIC_URL}/d/{d.token}",
        # La variante B usa esto para abrir WhatsApp desde el último paso.
        "whatsapp_url": whatsapp.link_conversacion(d.token, tier, contexto="captura"),
    }


@router.get("/diagnostico/{token}", response_model=DiagnosticoPublico)
def obtener(token: str, db: Session = Depends(get_db)):
    d = db.query(Diagnostico).filter(Diagnostico.token == token).first()
    if d is None:
        raise HTTPException(404, "No existe ese diagnóstico")

    if d.estado == "listo" and d.visto_at is None:
        d.visto_at = _ahora()
        db.commit()
        _registrar(db, "diagnostico_visto", d.variante, d.id)

    return DiagnosticoPublico(
        token=d.token,
        estado=d.estado,
        nombre=d.nombre,
        contenido=d.contenido,
        whatsapp_url=whatsapp.link_conversacion(d.token, d.tier) if d.estado == "listo" else None,
    )


@router.post("/diagnostico/{token}/cta", status_code=204)
def click_cta(token: str, db: Session = Depends(get_db)):
    """Se llama justo antes de abrir WhatsApp. Es la métrica de conversión final."""
    d = db.query(Diagnostico).filter(Diagnostico.token == token).first()
    if d is None:
        raise HTTPException(404, "No existe ese diagnóstico")
    if d.cta_click_at is None:
        d.cta_click_at = _ahora()
        db.commit()
    _registrar(db, "cta_whatsapp", d.variante, d.id)


@router.post("/eventos", status_code=204)
def evento(payload: EventoCrear, db: Session = Depends(get_db)):
    """Tracking del embudo desde el frontend (vistas, arranque, pasos)."""
    diagnostico_id = None
    if payload.token:
        d = db.query(Diagnostico).filter(Diagnostico.token == payload.token).first()
        diagnostico_id = d.id if d else None
    _registrar(db, payload.tipo, payload.variante, diagnostico_id, **payload.datos)
