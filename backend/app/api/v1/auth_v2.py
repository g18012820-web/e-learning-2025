from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_session as deps_get_session
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from sqlalchemy import select, update
import uuid
from app.models.session import Session as AppSession
from app.services.session_service import SessionService
from app.repositories.user_repository import UserRepository
from app.repositories.session_repository import SessionRepository
from app.models.audit_log import AuditLog
from app.utils.response import standard_response
from app.core.security import settings
from jose import jwt

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post('/signup')
async def signup(payload: LoginRequest, session: AsyncSession = Depends(deps_get_session)):
    existing = await UserRepository.get_by_email(session, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(id=uuid.uuid4(), first_name='Unknown', last_name='Unknown', email=payload.email, password_hash=hash_password(payload.password), role='student', status='pending_activation')
    session.add(user)
    await session.commit()
    # audit
    al = AuditLog(user_id=user.id, action='user_signup', meta={'email': user.email})
    session.add(al)
    await session.commit()
    return standard_response(True, "user created", {"id": str(user.id), "email": user.email})

@router.post('/login', response_model=TokenResponse)
async def login(payload: LoginRequest, request: Request, session: AsyncSession = Depends(deps_get_session)):
    user = await UserRepository.get_by_email(session, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        # audit failed login
        al = AuditLog(user_id=None, action='login_failed', meta={'email': payload.email, 'ip': request.client.host if request.client else None})
        session.add(al)
        await session.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if user.status != 'active' and getattr(user, 'activation_required', False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Account activation required')
    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))
    # create session record and store refresh token
    sess = await SessionService.create_user_session(session, user, refresh, ip_address=request.client.host if request.client else None, user_agent=request.headers.get('user-agent'))
    # audit login
    al = AuditLog(user_id=user.id, action='login_success', ip_address=request.client.host if request.client else None, user_agent=request.headers.get('user-agent'))
    session.add(al)
    await session.commit()
    return TokenResponse(access_token=access, refresh_token=refresh)

@router.post('/refresh', response_model=TokenResponse)
async def refresh_token(payload: RefreshRequest, session: AsyncSession = Depends(deps_get_session)):
    # verify provided refresh token exists in sessions and not revoked
    sess = await SessionRepository.get_session_by_refresh_token(session, payload.refresh_token)
    if not sess or sess.revoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or revoked refresh token')
    try:
        decoded = jwt.decode(payload.refresh_token, settings.JWT_SECRET, algorithms=["HS256"])
        sub = decoded.get('sub')
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
    # rotate refresh token
    res = await SessionService.rotate_refresh(session, payload.refresh_token)
    if not res:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or revoked refresh token')
    new_refresh = res['new_refresh']
    new_access = create_access_token(str(sub))
    return TokenResponse(access_token=new_access, refresh_token=new_refresh)

@router.post('/logout')
async def logout(session_id: str, current_user: User = Depends(lambda: None), session: AsyncSession = Depends(deps_get_session)):
    # mark session revoked
    await SessionRepository.revoke_session(session, session_id)
    al = AuditLog(user_id=None, action='logout', meta={'session_id': session_id})
    session.add(al)
    await session.commit()
    return standard_response(True, "logout successful")

@router.post('/logout-all')
async def logout_all(request: Request, session: AsyncSession = Depends(deps_get_session), current_user: User = Depends(lambda: None)):
    # revoke all sessions for the user
    # current_user must be resolved via dependency in real implementation
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    await SessionService.revoke_all(session, str(current_user.id), actor_id=str(current_user.id))
    return standard_response(True, "all sessions revoked")

@router.get('/sessions')
async def list_sessions(current_user: User = Depends(lambda: None), session: AsyncSession = Depends(deps_get_session)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    sessions = await SessionRepository.get_sessions_by_user(session, str(current_user.id))
    items = []
    for s in sessions:
        items.append({"id": str(s.id), "device_name": s.device_name, "ip_address": s.ip_address, "login_at": s.login_at.isoformat() if s.login_at else None, "last_activity": s.last_activity.isoformat() if s.last_activity else None, "revoked": bool(s.revoked)})
    return standard_response(True, "sessions fetched", {"items": items})
