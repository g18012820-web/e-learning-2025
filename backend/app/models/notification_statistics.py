import uuid
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.connection import Base

class NotificationStatistics(Base):
    __tablename__ = 'notification_statistics'

    notification_id = Column(PG_UUID(as_uuid=True), primary_key=True)
    sent = Column(Integer, default=0)
    delivered = Column(Integer, default=0)
    opened = Column(Integer, default=0)
    clicked = Column(Integer, default=0)
