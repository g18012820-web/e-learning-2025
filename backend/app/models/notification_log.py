import uuid
from sqlalchemy import Column, String, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.connection import Base

class NotificationLog(Base):
    __tablename__ = 'notification_logs'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notification_id = Column(PG_UUID(as_uuid=True))
    channel = Column(String(30))
    recipient = Column(String)
    status = Column(String(30))
    response = Column(JSONB)
    attempt = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
