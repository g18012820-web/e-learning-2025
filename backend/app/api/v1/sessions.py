from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_session
from app.repositories.session_repository import SessionRepository
from app.models.session import Session as AppSession
from app.utils.response import standard_response
from typing import List

router = APIRouter(prefix='/v1/sessions', tags=['auth'])

@router.get('')
async def list_sessions(current_user=Depends(lambda: None), session: AsyncSession = Depends(get_session)):
    # current_user dependency should be replaced with real auth dependency
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    items = await SessionRepository.get_sessions_by_user(session, str(current_user.id))
    out = []
    for s in items:
        out.append({
            'id': str(s.id),
            'device_name': s.device_name,
            'ip_address': s.ip_address,
            'login_at': s.login_at.isoformat() if s.login_at else None,
            'last_activity': s.last_activity.isoformat() if s.last_activity else None,
            'revoked': bool(s.revoked)
        })
    return standard_response(True, 'sessions fetched', {'items': out})

@router.post('/revoke')
async def revoke_session(payload: dict, current_user=Depends(lambda: None), session: AsyncSession = Depends(get_session)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    session_id = payload.get('session_id')
    if not session_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='session_id required')
    await SessionRepository.revoke_session(session, session_id)
    await session.commit()
    return standard_response(True, 'session revoked')

@router.post('/revoke-all')
async def revoke_all(current_user=Depends(lambda: None), session: AsyncSession = Depends(get_session)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    await SessionRepository.revoke_all_sessions_for_user(session, str(current_user.id))
    await session.commit()
    return standard_response(True, 'all sessions revoked')
