from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import AsyncGenerator
from jose import jwt
from fastapi import Depends, HTTPException, status
from app.core.config import settings
from app.db.connection import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: AsyncSession = Depends(get_session)) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    q = select(User).where(User.id == sub)
    res = await session.execute(q)
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

async def require_owner(user: User = Depends(get_current_user)) -> User:
    if user.role != 'owner':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Owner access required')
    return user
