import uuid
from sqlalchemy import Column, String, JSON, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.connection import Base

class WebhookEvent(Base):
    __tablename__ = 'webhook_events'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String)
    target_url = Column(String)
    payload = Column(JSONB)
    delivered = Column(Boolean, default=False)
    response = Column(JSONB)
    attempt = Column(Integer, default=0)
    next_try = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
