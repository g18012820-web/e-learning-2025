from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def call_purchase_course(session: AsyncSession, user_id: str, course_id: str, amount: float):
    # Calls stored procedure public.purchase_course(p_user_id, p_course_id, p_amount)
    sql = text("SELECT * FROM public.purchase_course(:p_user_id, :p_course_id, :p_amount)")
    res = await session.execute(sql.bindparams(p_user_id=user_id, p_course_id=course_id, p_amount=amount))
    row = res.first()
    return row

async def call_use_activation_code(session: AsyncSession, user_id: str, code: str):
    sql = text("SELECT * FROM public.use_activation_code(:p_user_id, :p_code)")
    res = await session.execute(sql.bindparams(p_user_id=user_id, p_code=code))
    row = res.first()
    return row
