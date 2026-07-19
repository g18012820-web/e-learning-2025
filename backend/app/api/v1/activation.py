from fastapi import APIRouter, Depends, HTTPException
from app.services.stored_procs import call_use_activation_code
from app.core.deps import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_session

router = APIRouter(prefix='/v1/activation', tags=['activation'])

@router.post('/use')
async def use_code(code: str, current_user = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    res = await call_use_activation_code(session, str(current_user.id), code)
    if not res:
        raise HTTPException(status_code=400, detail='Failed to apply code')
    return {"result": res}
