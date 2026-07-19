import uuid
from sqlalchemy import Column, String, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.connection import Base

class WalletTransaction(Base):
    __tablename__ = 'wallet_transactions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wallet_id = Column(UUID(as_uuid=True))
    transaction_type = Column(String)
    amount = Column(Numeric(14,2))
    description = Column(String)
    reference = Column(String)
    status = Column(String, server_default='completed')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
