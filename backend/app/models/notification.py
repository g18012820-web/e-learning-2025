import uuid
from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.connection import Base

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    body = Column(String)
    image = Column(String)
    action_url = Column(String)
    notification_type = Column(String)
    target_type = Column(String)
    target_id = Column(UUID(as_uuid=True))
    scheduled_at = Column(DateTime(timezone=True))
    sent_at = Column(DateTime(timezone=True))
    status = Column(String, server_default='scheduled')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
