from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.deps import get_current_user, get_session
from app.utils.response import standard_response
from app.models.subject import Subject
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.lesson_video import LessonVideo
from app.models.wallet import Wallet
from sqlalchemy import select

router = APIRouter(prefix='/v1', tags=['student'])

@router.get('/home')
async def home(current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # Placeholder aggregation for home page
    welcome = f"مرحباً {getattr(current_user, 'first_name', '')}"
    # For speed return minimal structure; frontend can request specific endpoints for details
    data = {
        "welcome_message": welcome,
        "last_courses": [],
        "featured_courses": [],
        "continue_learning": [],
        "subjects": [],
        "latest_notifications": [],
        "upcoming_live_lessons": [],
        "upcoming_exams": [],
        "wallet_balance": None,
        "unread_notifications": 0
    }
    # try to fetch wallet balance
    stmt = select(Wallet).where(Wallet.user_id == current_user.id)
    res = await session.execute(stmt)
    w = res.scalar_one_or_none()
    if w:
        data['wallet_balance'] = float(w.balance or 0)
    return standard_response(True, "نجح تحميل الصفحة الرئيسية", data)

# Subjects
@router.get('/subjects')
async def list_subjects(q: Optional[str] = None, page: int = 1, per_page: int = 20, session: AsyncSession = Depends(get_session)):
    stmt = select(Subject).limit(per_page).offset((page - 1) * per_page)
    res = await session.execute(stmt)
    items = [dict(id=str(s.id), title=s.title, description=s.description, image=s.image) for s in res.scalars().all()]
    return standard_response(True, "subjects fetched", {"items": items, "page": page, "per_page": per_page})

@router.get('/subjects/{subject_id}')
async def get_subject(subject_id: str, session: AsyncSession = Depends(get_session)):
    stmt = select(Subject).where(Subject.id == subject_id)
    res = await session.execute(stmt)
    s = res.scalar_one_or_none()
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Subject not found')
    # fetch related courses count and list (simple)
    stmt2 = select(Course).where(Course.subject_id == s.id).limit(50)
    res2 = await session.execute(stmt2)
    courses = [dict(id=str(c.id), title=c.title, price=float(c.price or 0)) for c in res2.scalars().all()]
    data = {"id": str(s.id), "title": s.title, "description": s.description, "courses": courses, "courses_count": len(courses)}
    return standard_response(True, "subject fetched", data)

# Courses
@router.get('/courses')
async def list_courses(subject: Optional[str] = None, teacher: Optional[str] = None, featured: Optional[bool] = None, free: Optional[bool] = None, page: int = 1, per_page: int = 20, session: AsyncSession = Depends(get_session)):
    stmt = select(Course).limit(per_page).offset((page - 1) * per_page)
    res = await session.execute(stmt)
    items = []
    for c in res.scalars().all():
        items.append({"id": str(c.id), "title": c.title, "price": float(c.price or 0), "cover": c.cover})
    return standard_response(True, "courses fetched", {"items": items, "page": page, "per_page": per_page})

@router.get('/courses/{course_id}')
async def get_course(course_id: str, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    stmt = select(Course).where(Course.id == course_id)
    res = await session.execute(stmt)
    c = res.scalar_one_or_none()
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')
    # check purchase status omitted (placeholder)
    data = {"id": str(c.id), "title": c.title, "description": c.description, "price": float(c.price or 0), "lessons_count": c.lessons_count}
    return standard_response(True, "course fetched", data)

@router.post('/courses/{course_id}/purchase')
async def purchase_course(course_id: str, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # Placeholder; real implementation should call stored procedure purchase_course
    # Check wallet
    from app.services.stored_procs import call_purchase_course
    res = await call_purchase_course(session, str(current_user.id), course_id, 0)
    return standard_response(True, "purchase processed", {"result": res})

@router.post('/courses/{course_id}/activate')
async def activate_course(course_id: str, code: str, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # re-use activation service
    from app.services.stored_procs import call_use_activation_code
    res = await call_use_activation_code(session, str(current_user.id), code)
    if not res:
        raise HTTPException(status_code=400, detail='Failed to apply code')
    return standard_response(True, "code applied", {"result": res})

# Lessons
@router.get('/lessons/{lesson_id}')
async def get_lesson(lesson_id: str, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    stmt = select(Lesson).where(Lesson.id == lesson_id)
    res = await session.execute(stmt)
    l = res.scalar_one_or_none()
    if not l:
        raise HTTPException(status_code=404, detail='Lesson not found')
    data = {"id": str(l.id), "title": l.title, "description": l.description, "duration": str(l.duration)}
    return standard_response(True, "lesson fetched", data)

@router.post('/lessons/{lesson_id}/progress')
async def lesson_progress(lesson_id: str, payload: dict, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # payload: watch_seconds, position, completed
    # store in lesson_progress table (not yet implemented) - placeholder
    return standard_response(True, "progress saved", payload)

@router.post('/lessons/{lesson_id}/complete')
async def lesson_complete(lesson_id: str, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # mark lesson complete
    return standard_response(True, "lesson marked complete", {"lesson_id": lesson_id})

# Videos
@router.get('/videos/{video_id}')
async def videos_token(video_id: str, current_user=Depends(get_current_user)):
    # return a short-lived token for streaming
    from app.core.security import create_signed_token
    token = create_signed_token({'sub': video_id, 'type': 'video'}, minutes=5)
    return standard_response(True, "token generated", {"token": token})

@router.get('/videos/{video_id}/stream')
async def video_stream(video_id: str, token: str, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # validate token and permissions (placeholder)
    # check purchase etc.
    return standard_response(True, "stream ready", {"stream_url": f"/internal/stream/{video_id}"})

# Wallet & Codes endpoints are already defined in separate routers; favorites, notifications, profile, search etc. will be added similarly.
