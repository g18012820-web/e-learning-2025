import httpx
from app.core.settings import settings

async def send_webhook(url: str, payload: dict, headers: dict = None, timeout: int = 10):
    headers = headers or {}
    # sign payload if secret exists
    secret = getattr(settings, 'WEBHOOK_SECRET', None)
    if secret:
        import hmac, hashlib
        import base64
        sig = hmac.new(secret.encode(), msg=str(payload).encode(), digestmod=hashlib.sha256).hexdigest()
        headers['X-Signature'] = sig
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(url, json=payload, headers=headers)
        return {"ok": r.status_code in (200,201,202), "status_code": r.status_code, "text": r.text}
