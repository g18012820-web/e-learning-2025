import uuid
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.connection import Base

class NotificationQueue(Base):
    __tablename__ = 'notification_queue'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notification_id = Column(PG_UUID(as_uuid=True))
    attempt = Column(Integer, default=0)
    status = Column(String(30), default='queued')
    next_try_at = Column(DateTime(timezone=True))
    idempotency_key = Column(String, nullable=True)
    worker_meta = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_attempt_at = Column(DateTime(timezone=True))
