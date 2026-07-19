from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password
from app.core.security import create_access_token, create_refresh_token
from app.models.session import Session as AppSession
import uuid

class UserService:
    @staticmethod
    async def signup(session: AsyncSession, first_name: str, last_name: str, email: str, password: str):
        existing = await UserRepository.get_by_email(session, email)
        if existing:
            raise ValueError('Email already registered')
        hashed = hash_password(password)
        user = await UserRepository.create(session, first_name, last_name, email, hashed)
        await session.commit()
        return user

    @staticmethod
    async def authenticate(session: AsyncSession, email: str, password: str):
        user = await UserRepository.get_by_email(session, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        access = create_access_token(str(user.id))
        refresh = create_refresh_token(str(user.id))
        # create a session record
        sess = AppSession(id=uuid.uuid4(), user_id=user.id, device_name='unknown', device_model='', operating_system='', app_version='', ip_address=None, status='active', refresh_token=refresh)
        session.add(sess)
        await session.commit()
        return {"user": user, "access": access, "refresh": refresh}
