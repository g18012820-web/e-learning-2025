import uuid
from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.connection import Base

class DeviceToken(Base):
    __tablename__ = 'device_tokens'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), nullable=True)
    provider = Column(String(30))
    token = Column(String)
    platform = Column(String(30))
    meta = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True))
