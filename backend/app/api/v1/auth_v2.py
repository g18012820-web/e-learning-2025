from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_session
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from sqlalchemy import select, insert, update
import uuid
from app.models.session import Session as AppSession
from app.core.deps import get_session as deps_get_session

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post('/signup')
async def signup(payload: LoginRequest, session: AsyncSession = Depends(deps_get_session)):
    # Using LoginRequest for simplicity here - in production use separate DTOs
    q = select(User).where(User.email == payload.email)
    res = await session.execute(q)
    existing = res.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(
        id=uuid.uuid4(),
        first_name='Unknown',
        last_name='Unknown',
        email=payload.email,
        phone=None,
        wilaya=None,
        password_hash=hash_password(payload.password),
        role='student',
        status='pending_activation'
    )
    session.add(user)
    await session.commit()
    return {"id": str(user.id), "email": user.email}

@router.post('/login', response_model=TokenResponse)
async def login(payload: LoginRequest, session: AsyncSession = Depends(deps_get_session)):
    q = select(User).where(User.email == payload.email)
    res = await session.execute(q)
    user = res.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if user.status != 'active' and user.activation_required:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Account activation required')
    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))
    # create session record and store refresh token
    sess = AppSession(id=uuid.uuid4(), user_id=user.id, device_name='unknown', device_model='', operating_system='', app_version='', ip_address=None, status='active', refresh_token=refresh)
    session.add(sess)
    await session.commit()
    return TokenResponse(access_token=access, refresh_token=refresh)

@router.post('/refresh', response_model=TokenResponse)
async def refresh_token(payload: RefreshRequest, session: AsyncSession = Depends(deps_get_session)):
    # verify provided refresh token exists in sessions and not revoked
    stmt = select(AppSession).where(AppSession.refresh_token == payload.refresh_token)
    res = await session.execute(stmt)
    sess = res.scalar_one_or_none()
    if not sess or sess.revoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or revoked refresh token')
    # verify token signature
    from jose import jwt
    try:
        decoded = jwt.decode(payload.refresh_token, "REPLACE_WITH_SECRET", algorithms=["HS256"])
        sub = decoded.get('sub')
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
    # rotate refresh token
    new_refresh = create_refresh_token(str(sub))
    new_access = create_access_token(str(sub))
    upd = update(AppSession).where(AppSession.id == sess.id).values(refresh_token=new_refresh)
    await session.execute(upd)
    await session.commit()
    return TokenResponse(access_token=new_access, refresh_token=new_refresh)

@router.post('/logout')
async def logout(session_id: str, session: AsyncSession = Depends(deps_get_session)):
    # mark session revoked
    upd = update(AppSession).where(AppSession.id == session_id).values(revoked=True, status='revoked')
    await session.execute(upd)
    await session.commit()
    return {"message": "logout successful"}
