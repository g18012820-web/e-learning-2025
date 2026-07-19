import uuid
from sqlalchemy import Column, String, JSON, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.connection import Base

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id = Column(PG_UUID(as_uuid=True), nullable=True)
    title = Column(String)
    body = Column(String)
    type = Column(String(50), nullable=False, default='in_app')
    priority = Column(Integer, default=2)
    payload = Column(JSONB)
    channel = Column(String(50))
    target = Column(JSONB)
    status = Column(String(30), default='pending')
    scheduled_at = Column(DateTime(timezone=True))
    created_by = Column(PG_UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
