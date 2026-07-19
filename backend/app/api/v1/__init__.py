from app.api.v1 import api_router
from app.api.v1 import auth_v2
from app.api.v1 import media
from app.api.v1 import courses
from app.api.v1 import admin
from app.api.v1 import wallets
from app.api.v1 import activation
from app.api.v1 import student
from app.api.v1 import notification_templates
from app.api.v1 import health
from app.api.v1 import notifications_api
from app.api.v1 import sessions

# include routers
api_router.include_router(auth_v2.router)
api_router.include_router(media.router)
api_router.include_router(courses.router)
api_router.include_router(admin.router)
api_router.include_router(wallets.router)
api_router.include_router(activation.router)
api_router.include_router(student.router)
api_router.include_router(notification_templates.router)
api_router.include_router(health.router)
api_router.include_router(notifications_api.router)
api_router.include_router(sessions.router)
