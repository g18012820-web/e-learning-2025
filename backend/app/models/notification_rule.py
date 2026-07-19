import uuid
from sqlalchemy import Column, String, JSON, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.connection import Base

class NotificationRule(Base):
    __tablename__ = 'notification_rules'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    trigger_type = Column(String(50), nullable=False)
    condition = Column(JSONB)
    actions = Column(JSONB)
    active = Column(Boolean, default=True)
    priority = Column(Integer, default=100)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
