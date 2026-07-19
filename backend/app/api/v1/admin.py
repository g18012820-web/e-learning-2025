from fastapi import APIRouter, Depends
from app.core.deps import require_owner

router = APIRouter(prefix='/v1/admin', tags=['admin'])

@router.get('/dashboard')
async def owner_dashboard(_owner = Depends(require_owner)):
    # This will return metrics collected from DB, placeholder for now
    return {
        "total_students": 0,
        "total_courses": 0,
        "total_teachers": 0,
        "total_wallets": 0
    }

@router.get('/subjects')
async def list_subjects(_owner = Depends(require_owner)):
    return {"items": []}

@router.post('/subjects')
async def create_subject(_owner = Depends(require_owner)):
    return {"message": "create subject - implement"}
