import asyncio
from celery import shared_task
from app.db.connection import engine
from sqlalchemy import text
import json

RETRY_BACKOFF = [30, 60, 300, 900, 3600]

@shared_task(bind=True, max_retries=6)
def process_notification_queue(self, batch_size: int = 50):
    """Simple worker task that picks queued notifications and dispatches them.

    This is a skeleton implementation: it marks attempts, writes logs, and
    demonstrates retry/backoff. Adapters (FCM/Email/Webhook) must be
    implemented separately and integrated here.
    """
    try:
        async def _run():
            async with engine.begin() as conn:
                # select next batch of queued items (for demo: status='queued')
                rows = await conn.execute(text(
                    "SELECT id, notification_id, attempt FROM notification_queue WHERE status = 'queued' ORDER BY created_at LIMIT :limit FOR UPDATE SKIP LOCKED"
                ), {"limit": batch_size})
                items = rows.fetchall()
                for item in items:
                    qid = item[0]
                    nid = item[1]
                    attempt = item[2] or 0
                    # mark as processing
                    await conn.execute(text("UPDATE notification_queue SET status='processing', last_attempt_at=now(), attempt = :a WHERE id = :id"), {"a": attempt + 1, "id": qid})
                    # --- dispatch placeholder ---
                    # Here you'd resolve recipients, render templates, and call adapters
                    # For now we insert a log entry showing 'sent' simulation
                    await conn.execute(text("INSERT INTO notification_logs (id, notification_id, channel, recipient, status, response, attempt, created_at) VALUES (gen_random_uuid(), :nid, 'in_app', 'user:demo', 'delivered', :resp::jsonb, :att, now())"), {"nid": nid, "resp": json.dumps({"msg": "simulated delivery"}), "att": attempt + 1})
                    # mark queue item done
                    await conn.execute(text("UPDATE notification_queue SET status='done' WHERE id = :id"), {"id": qid})
        asyncio.run(_run())
    except Exception as exc:
        try:
            self.retry(countdown=RETRY_BACKOFF[min(self.request.retries, len(RETRY_BACKOFF)-1)])
        except Exception:
            raise
