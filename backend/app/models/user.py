import uuid
from sqlalchemy import Column, String, Boolean, DateTime, text
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=True)
    wilaya = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    role = Column(String, nullable=False)
    status = Column(String, nullable=False)
    activation_required = Column(Boolean, nullable=False, server_default=text('false'))
    activation_completed = Column(Boolean, nullable=False, server_default=text('false'))
    last_login = Column(DateTime(timezone=True))
    last_ip = Column(INET)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    is_migrated = Column(Boolean, nullable=False, server_default=text('false'))
