import uuid
from sqlalchemy import Column, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.connection import Base

class UserNotificationSettings(Base):
    __tablename__ = 'user_notification_settings'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), nullable=False, unique=True)
    settings = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
