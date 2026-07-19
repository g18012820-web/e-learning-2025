import uuid
from sqlalchemy import Column, String, BigInteger, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.connection import Base

class FileStorage(Base):
    __tablename__ = 'file_storage'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    media_id = Column(UUID(as_uuid=True))
    path = Column(String)
    size = Column(BigInteger)
    content_type = Column(String)
    storage_provider = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
