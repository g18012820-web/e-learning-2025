import uuid
from sqlalchemy import Column, Numeric, String, BigInteger, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.connection import Base

class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    balance = Column(Numeric(14,2), server_default='0')
    total_recharged = Column(Numeric(14,2), server_default='0')
    total_spent = Column(Numeric(14,2), server_default='0')
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
