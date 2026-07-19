from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.session import Session as AppSession
import uuid

class SessionRepository:
    @staticmethod
    async def create_session(session: AsyncSession, user_id: str, refresh_token: str, device_name: str = 'unknown', device_model: str = '', operating_system: str = '', app_version: str = '', ip_address: Optional[str] = None):
        sess = AppSession(id=uuid.uuid4(), user_id=user_id, device_name=device_name, device_model=device_model, operating_system=operating_system, app_version=app_version, ip_address=ip_address, refresh_token=refresh_token)
        session.add(sess)
        await session.flush()
        return sess

    @staticmethod
    async def get_sessions_by_user(session: AsyncSession, user_id: str) -> List[AppSession]:
        stmt = select(AppSession).where(AppSession.user_id == user_id).order_by(AppSession.login_at.desc())
        res = await session.execute(stmt)
        return res.scalars().all()

    @staticmethod
    async def revoke_session(session: AsyncSession, session_id: str):
        stmt = update(AppSession).where(AppSession.id == session_id).values(revoked=True, status='revoked')
        await session.execute(stmt)

    @staticmethod
    async def revoke_all_sessions_for_user(session: AsyncSession, user_id: str):
        stmt = update(AppSession).where(AppSession.user_id == user_id).values(revoked=True, status='revoked')
        await session.execute(stmt)

    @staticmethod
    async def get_session_by_refresh_token(session: AsyncSession, refresh_token: str) -> Optional[AppSession]:
        stmt = select(AppSession).where(AppSession.refresh_token == refresh_token)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    @staticmethod
    async def update_refresh_token(session: AsyncSession, session_id: str, new_refresh_token: str):
        stmt = update(AppSession).where(AppSession.id == session_id).values(refresh_token=new_refresh_token)
        await session.execute(stmt)
