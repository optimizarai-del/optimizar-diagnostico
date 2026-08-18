"""App FastAPI del diagnóstico de Optimizar."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import Base, engine
from .routers import diagnostico, metrics

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Crea las tablas al arrancar. No hay sistema de migraciones todavía.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Optimizar — Diagnóstico",
    description="Formulario de diagnóstico operativo con IA + test A/B de captura",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diagnostico.router)
app.include_router(metrics.router)


@app.get("/api/health")
def health():
    return {"ok": True, "modelo": settings.MODELO}
