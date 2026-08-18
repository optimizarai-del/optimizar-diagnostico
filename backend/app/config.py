"""Configuración central. Todo se lee de variables de entorno (.env)."""
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Base de datos — SQLite en local, Postgres/Supabase en producción
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./diagnostico.db")

    # URL pública del sitio (se usa para armar el link del diagnóstico)
    PUBLIC_URL: str = os.getenv("PUBLIC_URL", "http://localhost:5173").rstrip("/")

    # Claude
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    MODELO: str = os.getenv("MODELO", "claude-opus-5")

    # Email (Hostinger SMTP — ya operativo según stack.md)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.hostinger.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "465"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_NAME: str = os.getenv("SMTP_FROM_NAME", "Optimizar")

    # WhatsApp — click-to-chat (fase 1, sin API ni plantillas de Meta)
    WHATSAPP_NUMERO: str = os.getenv("WHATSAPP_NUMERO", "5492954000000")

    # Clave para los endpoints de métricas
    ADMIN_API_KEY: str = os.getenv("ADMIN_API_KEY", "")

    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:4173"
    ).split(",")


settings = Settings()
