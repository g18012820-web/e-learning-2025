from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
import uuid

class UserRepository:
    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> Optional[User]:
        q = select(User).where(User.email == email)
        res = await session.execute(q)
        return res.scalar_one_or_none()

    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
        q = select(User).where(User.id == user_id)
        res = await session.execute(q)
        return res.scalar_one_or_none()

    @staticmethod
    async def create(session: AsyncSession, first_name: str, last_name: str, email: str, password_hash: str, role: str = 'student') -> User:
        user = User(id=uuid.uuid4(), first_name=first_name, last_name=last_name, email=email, password_hash=password_hash, role=role, status='pending_activation')
        session.add(user)
        await session.flush()
        return user
