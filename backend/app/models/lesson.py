import uuid
from sqlalchemy import Column, String, Text, Integer, JSON, DateTime, Interval
from sqlalchemy.dialects.postgresql import UUID
from app.db.connection import Base
from sqlalchemy.sql import func

class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True))
    section_id = Column(UUID(as_uuid=True))
    title = Column(String, nullable=False)
    description = Column(Text)
    lesson_type = Column(String, server_default='video')
    content = Column(JSON)
    order_number = Column(Integer, server_default='0')
    duration = Column(Interval)
    release_date = Column(DateTime(timezone=True))
    live_date = Column(DateTime(timezone=True))
    is_locked = Column(String)
    is_hidden = Column(String)
    status = Column(String, server_default='draft')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
