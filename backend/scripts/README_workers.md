# Developer script: run worker

# Start Celery worker (example)
# CELERY_BROKER_URL should be set in environment (.env)
# Run from repository root:
#   poetry run celery -A app.tasks.celery_app.celery_app worker --loglevel=info

# Or using python module if celery installed as dependency:
#   celery -A app.tasks.celery_app.celery_app worker --loglevel=info

# For demo/test run directly the task once (requires redis and db configured):
#   python -c "from app.tasks.notification_tasks import process_notification_queue; process_notification_queue.delay()"
