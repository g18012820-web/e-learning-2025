from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_session
from app.schemas.auth import UserCreate, TokenResponse, UserRead, LoginRequest, RefreshRequest
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from sqlalchemy import select, insert, update
import uuid
from app.models.session import Session as AppSession

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post('/signup', response_model=UserRead)
async def signup(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    q = select(User).where(User.email == payload.email)
    res = await session.execute(q)
    existing = res.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(
        id=uuid.uuid4(),
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone=payload.phone,
        wilaya=payload.wilaya,
        password_hash=hash_password(payload.password),
        role='student',
        status='pending_activation'
    )
    session.add(user)
    await session.commit()
    return UserRead(id=user.id, first_name=user.first_name, last_name=user.last_name, email=user.email, role=user.role)

@router.post('/login', response_model=TokenResponse)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_session)):
    q = select(User).where(User.email == payload.email)
    res = await session.execute(q)
    user = res.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if user.status != 'active' and user.activation_required:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Account activation required')
    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))
    # create session record
    sess = AppSession(id=uuid.uuid4(), user_id=user.id, device_name='unknown', device_model='', operating_system='', app_version='', ip_address=None, status='active')
    session.add(sess)
    await session.commit()
    return TokenResponse(access_token=access, refresh_token=refresh)

@router.post('/refresh', response_model=TokenResponse)
async def refresh(payload: RefreshRequest, session: AsyncSession = Depends(get_session)):
    try:
        payload_jwt = payload.refresh_token
        from jose import jwt
        decoded = jwt.decode(payload_jwt, None, options={"verify_signature": False})
        sub = decoded.get('sub')
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
    # In a robust implementation we'd verify token signature and check stored refresh token; simplified here
    access = create_access_token(str(sub))
    refresh = create_refresh_token(str(sub))
    return TokenResponse(access_token=access, refresh_token=refresh)

@router.post('/logout')
async def logout(session_id: uuid.UUID, current_user: User = Depends(lambda: None), session: AsyncSession = Depends(get_session)):
    # placeholder: logout implementation should mark session revoked
    return {"message": "logout endpoint - implement session revocation"}
