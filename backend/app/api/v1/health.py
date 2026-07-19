from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_session
import json
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

router = APIRouter(prefix="/v1/health", tags=["health"])

@router.get('/live')
async def liveness_probe():
    return {"status": "ok"}

@router.get('/ready')
async def readiness_probe(session: AsyncSession = Depends(get_session)):
    # simple DB check
    try:
        await session.execute('SELECT 1')
    except Exception as e:
        return Response(content=json.dumps({"status": "error", "detail": str(e)}), status_code=status.HTTP_503_SERVICE_UNAVAILABLE, media_type='application/json')
    return {"status": "ready"}

@router.get('/metrics')
async def metrics():
    # Expose Prometheus metrics (default registry)
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
