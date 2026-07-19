from fastapi import APIRouter, Depends
from app.api.v1 import api_router
from app.api.v1 import auth_v2
from app.api.v1 import media
from app.api.v1 import courses
from app.api.v1 import admin
from app.api.v1 import wallets
from app.api.v1 import activation

# include routers
api_router.include_router(auth_v2.router)
api_router.include_router(media.router)
api_router.include_router(courses.router)
api_router.include_router(admin.router)
api_router.include_router(wallets.router)
api_router.include_router(activation.router)
