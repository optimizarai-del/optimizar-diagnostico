"""Envío del diagnóstico por email (variante A) vía SMTP de Hostinger.

El mail no lleva el diagnóstico entero: lleva el titular y un link a la página
`/d/{token}`. Así se mide la apertura real, se ve como el producto que vendemos
y el CTA a WhatsApp vive dentro de la página.
"""
import smtplib
from email.message import EmailMessage

from ..config import settings
from ..schemas import ContenidoDiagnostico


def _html(nombre: str, contenido: ContenidoDiagnostico, url: str) -> str:
    return f"""\
<!doctype html>
<html lang="es">
<body style="margin:0;padding:0;background:#0D0F1A;font-family:Poppins,Montserrat,Helvetica,Arial,sans-serif;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#0D0F1A;padding:32px 16px;">
    <tr><td align="center">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#141726;border-radius:16px;padding:32px;">
        <tr><td>
          <p style="margin:0 0 24px;font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#8B5CF6;">Optimizar · Diagnóstico</p>
          <h1 style="margin:0 0 16px;font-size:24px;line-height:1.3;color:#ffffff;font-weight:600;">{nombre}, esto es lo que encontramos</h1>
          <p style="margin:0 0 28px;font-size:17px;line-height:1.6;color:#C9CCD8;">{contenido.titular}</p>
          <p style="margin:0 0 28px;font-size:15px;line-height:1.7;color:#9AA0B4;">{contenido.resumen}</p>
          <table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="border-radius:10px;background:#6B5CE7;">
            <a href="{url}" style="display:inline-block;padding:14px 28px;font-size:15px;font-weight:600;color:#ffffff;text-decoration:none;">Ver el diagnóstico completo</a>
          </td></tr></table>
          <p style="margin:28px 0 0;font-size:13px;line-height:1.6;color:#6B7089;">
            Adentro vas a encontrar los tres cuellos de botella que detectamos, qué automatizaríamos primero y algo que podés hacer solo esta semana.
          </p>
        </td></tr>
      </table>
      <p style="margin:20px 0 0;font-size:12px;color:#4A4F63;">Optimizar — socio operativo con IA para PyMEs</p>
    </td></tr>
  </table>
</body>
</html>"""


def enviar(destinatario: str, nombre: str, contenido: ContenidoDiagnostico, url: str) -> None:
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        raise RuntimeError("Falta configurar SMTP_USER / SMTP_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = f"{nombre}, tu diagnóstico de Optimizar"
    msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_USER}>"
    msg["To"] = destinatario
    msg.set_content(
        f"{nombre}, esto es lo que encontramos:\n\n{contenido.titular}\n\n"
        f"{contenido.resumen}\n\nVer el diagnóstico completo: {url}\n\n"
        "Optimizar"
    )
    msg.add_alternative(_html(nombre, contenido, url), subtype="html")

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
        smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        smtp.send_message(msg)
