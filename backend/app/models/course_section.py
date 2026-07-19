import uuid
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.connection import Base

class CourseSection(Base):
    __tablename__ = 'course_sections'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True))
    title = Column(String, nullable=False)
    description = Column(String)
    order_number = Column(Integer, server_default='0')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
