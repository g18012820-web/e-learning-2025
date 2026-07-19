import os
import uuid
import asyncio
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_session, require_owner
from app.models.media import MediaLibrary
from app.models.file_storage import FileStorage
from app.db.connection import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from sqlalchemy import insert

router = APIRouter(prefix='/v1/media', tags=['media'])

UPLOAD_DIR = os.getenv('UPLOAD_DIR', '/app/uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def _save_file(upload_file: UploadFile, dest_path: str) -> int:
    content = await upload_file.read()
    # write in thread to avoid blocking
    await asyncio.to_thread(lambda: open(dest_path, 'wb').write(content))
    return len(content)

@router.post('/upload')
async def upload_media(file: UploadFile = File(...), owner_id: str = Form(None), session: AsyncSession = Depends(get_session), _owner = Depends(require_owner)):
    # owner verification done; owner_id optional to track uploader
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    dest = os.path.join(UPLOAD_DIR, filename)
    size = await _save_file(file, dest)
    # store media record
    stmt = insert(MediaLibrary).values(owner_id=owner_id, type=file.content_type, provider='local', original_url=dest, secure_url=dest, metadata=None)
    await session.execute(stmt)
    await session.commit()
    return JSONResponse({'message': 'uploaded', 'path': dest, 'size': size})

@router.post('/link')
async def link_media(url: str = Form(...), owner_id: str = Form(None), provider: str = Form('external'), session: AsyncSession = Depends(get_session), _owner = Depends(require_owner)):
    stmt = insert(MediaLibrary).values(owner_id=owner_id, type='external', provider=provider, original_url=url, secure_url=url)
    await session.execute(stmt)
    await session.commit()
    return JSONResponse({'message': 'linked', 'url': url})
