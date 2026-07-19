import uuid
from sqlalchemy import Column, String, Text, Numeric, DateTime, Integer, Boolean, Interval, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.connection import Base

class Course(Base):
    __tablename__ = 'courses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_id = Column(UUID(as_uuid=True))
    teacher_id = Column(UUID(as_uuid=True))
    title = Column(String, nullable=False)
    description = Column(Text)
    cover = Column(String)
    banner = Column(String)
    price = Column(Numeric(12,2), server_default='0')
    currency = Column(String(3), server_default='DZD')
    sale_price = Column(Numeric(12,2))
    level = Column(String)
    duration = Column(Interval)
    lessons_count = Column(Integer, server_default='0')
    status = Column(String, server_default='draft')
    allow_purchase = Column(Boolean, server_default='true')
    featured = Column(Boolean, server_default='false')
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
