from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from app.models.notification_template import NotificationTemplate
import uuid

class NotificationTemplateRepository:
    @staticmethod
    async def create(session: AsyncSession, name: str, channel: str, title_template: Optional[str] = None, body_template: Optional[str] = None, metadata: Optional[dict] = None, variables: Optional[dict] = None):
        nt = NotificationTemplate(id=uuid.uuid4(), name=name, channel=channel, title_template=title_template, body_template=body_template, metadata=metadata or {}, variables=variables or {})
        session.add(nt)
        await session.flush()
        return nt

    @staticmethod
    async def get(session: AsyncSession, template_id: str) -> Optional[NotificationTemplate]:
        stmt = select(NotificationTemplate).where(NotificationTemplate.id == template_id)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    @staticmethod
    async def list(session: AsyncSession, page: int = 1, per_page: int = 20):
        stmt = select(NotificationTemplate).limit(per_page).offset((page-1)*per_page)
        res = await session.execute(stmt)
        return res.scalars().all()

    @staticmethod
    async def update(session: AsyncSession, template_id: str, **patch):
        t = await NotificationTemplateRepository.get(session, template_id)
        if not t:
            return None
        for k, v in patch.items():
            if hasattr(t, k):
                setattr(t, k, v)
        session.add(t)
        await session.flush()
        return t

    @staticmethod
    async def delete(session: AsyncSession, template_id: str):
        t = await NotificationTemplateRepository.get(session, template_id)
        if not t:
            return False
        await session.delete(t)
        return True
