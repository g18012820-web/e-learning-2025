import uuid
from sqlalchemy import Column, String, Numeric, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.connection import Base

class ActivationCode(Base):
    __tablename__ = 'activation_codes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True)
    code_type = Column(String)
    value = Column(Numeric(14,2))
    usage_limit = Column(Integer, server_default='1')
    usage_count = Column(Integer, server_default='0')
    expires_at = Column(DateTime(timezone=True))
    status = Column(String, server_default='active')
    created_by = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
