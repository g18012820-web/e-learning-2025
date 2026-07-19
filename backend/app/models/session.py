import uuid
from sqlalchemy import Column, String, DateTime, text, Boolean
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.sql import func
from app.db.connection import Base

class Session(Base):
    __tablename__ = 'sessions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    device_name = Column(String)
    device_model = Column(String)
    operating_system = Column(String)
    app_version = Column(String)
    ip_address = Column(INET)
    country = Column(String)
    city = Column(String)
    login_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    status = Column(String, server_default='active')
    refresh_token = Column(String, nullable=True)
    revoked = Column(Boolean, server_default='false')
