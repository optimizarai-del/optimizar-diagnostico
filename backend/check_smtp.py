"""Verifica que la casilla de envío funcione, antes de mandar el primer lead.

    python check_smtp.py                    # solo conecta y autentica
    python check_smtp.py vos@gmail.com      # además manda un mail de prueba real

Si el segundo modo llega a tu bandeja de entrada (no a spam), la variante A del
test A/B está lista.
"""
import smtplib
import ssl
import sys

from app.config import settings
from app.schemas import ContenidoDiagnostico, CuelloBotella, QuickWin, Recomendacion
from app.services.email import enviar

MUESTRA = ContenidoDiagnostico(
    titular="Entre 10 y 20 horas por semana se van en responder consultas.",
    resumen=(
        "Este es un mail de prueba del sistema de diagnóstico. Si te llegó a la "
        "bandeja de entrada y no a spam, la configuración de correo está bien."
    ),
    cuellos=[
        CuelloBotella(
            titulo="Cuello de botella de ejemplo",
            descripcion="Texto de prueba.",
            impacto="~5 h/semana",
        )
    ],
    recomendacion=Recomendacion(
        titulo="Recomendación de ejemplo", descripcion="Texto de prueba.", plazo="3 a 4 semanas"
    ),
    quick_win=QuickWin(titulo="Quick win de ejemplo", pasos=["Paso uno", "Paso dos"]),
    cierre="Cierre de prueba.",
)


def main() -> int:
    print(f"Servidor : {settings.SMTP_HOST}:{settings.SMTP_PORT}")
    print(f"Casilla  : {settings.SMTP_USER or '(vacía)'}")

    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print("\nFalta SMTP_USER o SMTP_PASSWORD en backend/.env")
        return 1

    # 1. Conexión y autenticación
    try:
        with smtplib.SMTP_SSL(
            settings.SMTP_HOST, settings.SMTP_PORT, context=ssl.create_default_context(), timeout=20
        ) as smtp:
            smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        print("\n[OK] Conecta y autentica.")
    except smtplib.SMTPAuthenticationError:
        print("\n[ERROR] Usuario o contraseña rechazados.")
        print("        En Hostinger la contraseña SMTP es la misma de la casilla.")
        print("        Si la cambiaste hace poco, esperá unos minutos a que propague.")
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"\n[ERROR] No se pudo conectar: {exc}")
        print("        Revisá host y puerto (465 = SSL, 587 = STARTTLS).")
        return 1

    # 2. Envío real, si pasaron un destinatario
    if len(sys.argv) > 1:
        destino = sys.argv[1]
        print(f"\nMandando mail de prueba a {destino}…")
        try:
            enviar(destino, "Prueba", MUESTRA, f"{settings.PUBLIC_URL}/d/PRUEBA")
            print("[OK] Enviado.")
            print("\nAhora revisá:")
            print("  1. ¿Llegó a la bandeja de entrada o a spam?")
            print("  2. En Gmail: abrir el mail → ⋮ → 'Mostrar original'")
            print("     Tienen que decir PASS: SPF, DKIM y DMARC.")
        except Exception as exc:  # noqa: BLE001
            print(f"[ERROR] No se pudo enviar: {exc}")
            return 1
    else:
        print("\nPara mandar un mail de prueba real:")
        print("  python check_smtp.py tu-mail@gmail.com")

    return 0


if __name__ == "__main__":
    sys.exit(main())
