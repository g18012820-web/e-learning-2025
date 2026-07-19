import os
import httpx
from app.core.settings import settings

FCM_URL = 'https://fcm.googleapis.com/fcm/send'

async def send_push(token: str, title: str, body: str, data: dict = None):
    key = settings.FCM_SERVER_KEY if hasattr(settings, 'FCM_SERVER_KEY') else None
    if not key:
        # no key configured: simulate or raise
        return {"ok": False, "reason": "no_fcm_key"}
    headers = {'Authorization': f'key={key}', 'Content-Type': 'application/json'}
    payload = {
        'to': token,
        'notification': {'title': title, 'body': body},
        'data': data or {}
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(FCM_URL, json=payload, headers=headers)
        return {"ok": r.status_code == 200, "status_code": r.status_code, "body": r.text}
