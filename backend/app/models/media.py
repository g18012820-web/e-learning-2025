import uuid
from sqlalchemy import Column, String, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.connection import Base

class MediaLibrary(Base):
    __tablename__ = 'media_library'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True))
    type = Column(String)
    provider = Column(String)
    original_url = Column(String)
    secure_url = Column(String)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
