from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user
from app.db.connection import get_session
from app.services.stored_procs import call_purchase_course
from app.models.course import Course
from sqlalchemy import select

router = APIRouter(prefix='/v1/courses', tags=['courses'])

@router.get('/')
async def list_courses(q: str = None, session: AsyncSession = Depends(get_session)):
    stmt = select(Course).limit(50)
    res = await session.execute(stmt)
    items = res.scalars().all()
    return items

@router.post('/{course_id}/purchase')
async def purchase_course(course_id: str, session: AsyncSession = Depends(get_session), current_user = Depends(get_current_user)):
    # For example amount we fetch course price
    stmt = select(Course).where(Course.id == course_id)
    res = await session.execute(stmt)
    course = res.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')
    # call stored proc
    row = await call_purchase_course(session, str(current_user.id), course_id, float(course.price or 0))
    return {"result": row}
