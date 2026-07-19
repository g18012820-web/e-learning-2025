from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_session
from app.schemas.user import UserCreate, TokenResponse, UserRead
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from sqlalchemy import select
import uuid

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post('/signup', response_model=UserRead)
async def signup(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    # check existing
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
async def login(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    # reuse UserCreate for incoming fields email & password
    q = select(User).where(User.email == payload.email)
    res = await session.execute(q)
    user = res.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))
    return TokenResponse(access_token=access, refresh_token=refresh)
