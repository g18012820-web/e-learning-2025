import uuid
from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.connection import Base

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    icon = Column(String)
    image = Column(String)
    color = Column(String(7))
    display_order = Column(String)
    status = Column(String, server_default='active')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
