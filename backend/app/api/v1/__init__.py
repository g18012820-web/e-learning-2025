from app.api.v1 import router as api_router
from app.api.v1 import auth
from app.api.v1 import media
from app.api.v1 import courses

# include routers
api_router.include_router(auth.router)
api_router.include_router(media.router)
api_router.include_router(courses.router)

# Admin / Owner routes skeleton
from fastapi import APIRouter
admin_router = APIRouter(prefix="/v1/admin", tags=["admin"])

@admin_router.get('/dashboard')
async def owner_dashboard():
    return {"message": "Owner dashboard metrics will be implemented here."}

api_router.include_router(admin_router)
