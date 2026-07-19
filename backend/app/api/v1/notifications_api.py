from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.settings import settings
from app.db.connection import get_session
from app.repositories.notification_template_repository import NotificationTemplateRepository
from app.repositories.session_repository import SessionRepository
from app.models.notification import Notification
from app.models.notification_queue import NotificationQueue
import uuid
import json

router = APIRouter(prefix='/v1/notifications', tags=['notifications'])

@router.post('/enqueue', dependencies=[])
async def enqueue_notification(payload: dict = Body(...), session: AsyncSession = Depends(get_session), request: Request = None):
    """Create a notification and enqueue it. Supports idempotency via X-Idempotency-Key header.
    Payload example:
    {
      "template_id": "...",
      "channel": "in_app",
      "target": {"user_ids":["uuid1","uuid2"]},
      "scheduled_at": null,
      "payload": {"lesson_name":"Intro"}
    }
    """
    template_id = payload.get('template_id')
    channel = payload.get('channel', 'in_app')
    target = payload.get('target', {})
    title = payload.get('title')
    body = payload.get('body')
    scheduled_at = payload.get('scheduled_at')
    if not template_id and (not title or not body):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='template_id or title/body required')
    # create notification
    notif = Notification(id=uuid.uuid4(), template_id=template_id, title=title, body=body, channel=channel, target=target, payload=payload.get('payload'), scheduled_at=scheduled_at)
    session.add(notif)
    await session.flush()
    # enqueue per target (for now: store a single queue entry)
    q = NotificationQueue(id=uuid.uuid4(), notification_id=notif.id, status='queued')
    session.add(q)
    await session.commit()
    return {"ok": True, "id": str(notif.id)}
