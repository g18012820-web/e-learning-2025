import uuid
from sqlalchemy import Column, String, JSON, DateTime, Interval
from sqlalchemy.dialects.postgresql import UUID
from app.db.connection import Base
from sqlalchemy.sql import func

class LessonVideo(Base):
    __tablename__ = 'lesson_videos'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = Column(UUID(as_uuid=True))
    provider = Column(String)
    original_url = Column(String)
    secure_url = Column(String)
    drm_type = Column(String)
    encryption_key = Column(String)
    quality = Column(String)
    subtitles = Column(JSON)
    thumbnail = Column(String)
    duration = Column(Interval)
    watermark_enabled = Column(String)
    allow_download = Column(String)
    allow_screenshot = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
