"""Tablas. Dos: el diagnóstico en sí y los eventos del embudo (para el test A/B)."""
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def _ahora() -> datetime:
    return datetime.now(timezone.utc)


class Diagnostico(Base):
    __tablename__ = "diagnosticos"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Token corto e impredecible — es la URL pública /d/{token}
    token: Mapped[str] = mapped_column(String(24), unique=True, index=True)

    # "a" = captura por email · "b" = captura por WhatsApp
    variante: Mapped[str] = mapped_column(String(1), index=True)

    # Origen del anuncio (utm_source / utm_campaign), para cruzar con Meta Ads
    utm: Mapped[dict] = mapped_column(JSON, default=dict)

    # Respuestas crudas del formulario: {"rubro": "contable", "tamano": "5-15", ...}
    respuestas: Mapped[dict] = mapped_column(JSON)

    # Calificación interna — el prospecto nunca la ve
    score: Mapped[int] = mapped_column(Integer, default=0)
    tier: Mapped[str] = mapped_column(String(10), default="amarillo")
    motivos: Mapped[list] = mapped_column(JSON, default=list)

    # Contacto
    nombre: Mapped[str | None] = mapped_column(String(120), nullable=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(40), nullable=True)

    # pendiente → generando → listo → error
    estado: Mapped[str] = mapped_column(String(20), default="pendiente", index=True)
    contenido: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    creado_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_ahora)
    generado_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    entregado_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    visto_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cta_click_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    eventos: Mapped[list["Evento"]] = relationship(back_populates="diagnostico")


class Evento(Base):
    """Un evento por paso del embudo. Es la base de todas las métricas A/B."""

    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(primary_key=True)
    diagnostico_id: Mapped[int | None] = mapped_column(
        ForeignKey("diagnosticos.id"), nullable=True, index=True
    )
    # landing_view · form_start · form_step · form_complete · captura
    # diagnostico_listo · diagnostico_visto · cta_whatsapp
    tipo: Mapped[str] = mapped_column(String(40), index=True)
    variante: Mapped[str | None] = mapped_column(String(1), index=True, nullable=True)
    datos: Mapped[dict] = mapped_column(JSON, default=dict)
    creado_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_ahora)

    diagnostico: Mapped[Diagnostico | None] = relationship(back_populates="eventos")
