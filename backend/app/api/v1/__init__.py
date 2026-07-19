from fastapi import APIRouter
from app.api.v1 import auth

router = APIRouter()
router.include_router(auth.router)

# Admin / Owner routes skeleton
from fastapi import APIRouter
admin_router = APIRouter(prefix="/v1/admin", tags=["admin"])

@admin_router.get('/dashboard')
async def owner_dashboard():
    return {"message": "Owner dashboard metrics will be implemented here."}

router.include_router(admin_router)
