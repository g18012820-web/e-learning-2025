import aiosmtplib
from email.message import EmailMessage
from app.core.settings import settings

async def send_email(to_email: str, subject: str, html: str, text: str = ''):
    smtp_host = getattr(settings, 'SMTP_HOST', None)
    smtp_port = getattr(settings, 'SMTP_PORT', 587)
    smtp_user = getattr(settings, 'SMTP_USER', None)
    smtp_pass = getattr(settings, 'SMTP_PASS', None)
    if not smtp_host:
        return {"ok": False, "reason": "no_smtp_config"}
    message = EmailMessage()
    message['From'] = smtp_user or 'no-reply@example.com'
    message['To'] = to_email
    message['Subject'] = subject
    message.set_content(text)
    message.add_alternative(html, subtype='html')
    try:
        await aiosmtplib.send(message, hostname=smtp_host, port=smtp_port, username=smtp_user, password=smtp_pass, start_tls=True)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
