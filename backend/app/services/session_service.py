from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.core.security import create_access_token, create_refresh_token
from app.models.audit_log import AuditLog
from sqlalchemy import insert
import uuid

class SessionService:
    @staticmethod
    async def create_user_session(session: AsyncSession, user, refresh_token: str, **device_info):
        # create session record
        sess = await SessionRepository.create_session(session, str(user.id), refresh_token, device_name=device_info.get('device_name','unknown'), device_model=device_info.get('device_model',''), operating_system=device_info.get('operating_system',''), app_version=device_info.get('app_version',''), ip_address=device_info.get('ip_address'))
        # audit log
        al = AuditLog(user_id=user.id, action='session_created', ip_address=device_info.get('ip_address'), user_agent=device_info.get('user_agent'), meta={'session_id': str(sess.id)})
        session.add(al)
        await session.commit()
        return sess

    @staticmethod
    async def revoke_all(session: AsyncSession, user_id: str, actor_id: str = None):
        await SessionRepository.revoke_all_sessions_for_user(session, user_id)
        # audit
        al = AuditLog(user_id=user_id, action='sessions_revoked', meta={'by': actor_id})
        session.add(al)
        await session.commit()

    @staticmethod
    async def rotate_refresh(session: AsyncSession, old_refresh_token: str):
        sess = await SessionRepository.get_session_by_refresh_token(session, old_refresh_token)
        if not sess or sess.revoked:
            return None
        # rotate
        new_refresh = create_refresh_token(str(sess.user_id))
        await SessionRepository.update_refresh_token(session, str(sess.id), new_refresh)
        al = AuditLog(user_id=sess.user_id, action='refresh_rotated', meta={'session_id': str(sess.id)})
        session.add(al)
        await session.commit()
        return {"session": sess, "new_refresh": new_refresh}
