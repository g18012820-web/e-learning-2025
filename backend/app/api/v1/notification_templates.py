from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_session, require_owner
from app.utils.response import standard_response
from app.repositories.notification_template_repository import NotificationTemplateRepository

router = APIRouter(prefix='/v1/notification-templates', tags=['notifications'])

@router.post('', dependencies=[Depends(require_owner)])
async def create_template(payload: dict = Body(...), session: AsyncSession = Depends(get_session)):
    name = payload.get('name')
    channel = payload.get('channel')
    if not name or not channel:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='name and channel required')
    nt = await NotificationTemplateRepository.create(session, name=name, channel=channel, title_template=payload.get('title_template'), body_template=payload.get('body_template'), metadata=payload.get('metadata'), variables=payload.get('variables'))
    await session.commit()
    return standard_response(True, 'template created', {'id': str(nt.id)})

@router.get('')
async def list_templates(page: int = 1, per_page: int = 20, session: AsyncSession = Depends(get_session)):
    items = await NotificationTemplateRepository.list(session, page=page, per_page=per_page)
    out = []
    for t in items:
        out.append({'id': str(t.id), 'name': t.name, 'channel': t.channel, 'created_at': t.created_at.isoformat() if t.created_at else None})
    return standard_response(True, 'templates fetched', {'items': out, 'page': page, 'per_page': per_page})

@router.get('/{template_id}')
async def get_template(template_id: str, session: AsyncSession = Depends(get_session)):
    t = await NotificationTemplateRepository.get(session, template_id)
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Template not found')
    return standard_response(True, 'template fetched', {'id': str(t.id), 'name': t.name, 'channel': t.channel, 'title_template': t.title_template, 'body_template': t.body_template, 'metadata': t.metadata, 'variables': t.variables})

@router.put('/{template_id}', dependencies=[Depends(require_owner)])
async def update_template(template_id: str, payload: dict = Body(...), session: AsyncSession = Depends(get_session)):
    t = await NotificationTemplateRepository.update(session, template_id, **payload)
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Template not found')
    await session.commit()
    return standard_response(True, 'template updated', {'id': str(t.id)})

@router.delete('/{template_id}', dependencies=[Depends(require_owner)])
async def delete_template(template_id: str, session: AsyncSession = Depends(get_session)):
    ok = await NotificationTemplateRepository.delete(session, template_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Template not found')
    await session.commit()
    return standard_response(True, 'template deleted')
