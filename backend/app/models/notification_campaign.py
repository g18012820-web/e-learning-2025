import uuid
from sqlalchemy import Column, String, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.connection import Base

class NotificationCampaign(Base):
    __tablename__ = 'notification_campaigns'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    notification_id = Column(PG_UUID(as_uuid=True))
    status = Column(String(30), default='draft')
    sent_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
