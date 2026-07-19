import uuid
from sqlalchemy import Column, String, Text, Integer, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.connection import Base

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    avatar = Column(String)
    biography = Column(Text)
    specialization = Column(String)
    experience_years = Column(Integer)
    certificates = Column(JSON)
    social_links = Column(JSON)
    email = Column(String)
    phone = Column(String)
    status = Column(String, server_default='active')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
