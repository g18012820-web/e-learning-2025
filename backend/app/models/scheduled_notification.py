import uuid
from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.connection import Base

class ScheduledNotification(Base):
    __tablename__ = 'scheduled_notifications'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notification_id = Column(PG_UUID(as_uuid=True))
    cron_expr = Column(String)
    timezone = Column(String)
    next_run = Column(DateTime(timezone=True))
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
