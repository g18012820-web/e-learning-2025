from celery import Celery
from app.core.settings import settings

celery_app = Celery(
    'e_learning_tasks',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

# You can configure Celery here or via env
celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    result_expires=3600,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

# autodiscover tasks within the package
celery_app.autodiscover_tasks(['app.tasks.notification_tasks'])
