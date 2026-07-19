import uuid
from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.connection import Base

class NotificationTemplate(Base):
    __tablename__ = 'notification_templates'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    channel = Column(String(30), nullable=False)
    title_template = Column(String)
    body_template = Column(String)
    metadata = Column(JSONB)
    variables = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
