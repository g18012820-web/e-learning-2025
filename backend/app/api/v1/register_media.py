from app.api.v1 import router as api_router
from app.api.v1 import admin_router
from app.api.v1 import auth
from app.api.v1 import media

# include media router
api_router.include_router(media.router)
