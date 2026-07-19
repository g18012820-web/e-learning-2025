from fastapi import FastAPI
from app.api.v1 import api_router
from app.core.settings import settings
from app.db.connection import init_db
from prometheus_client import start_http_server
import asyncio

app = FastAPI(title="e-learning-2025 API")

@app.on_event('startup')
async def startup_event():
    # initialize DB connection pools
    await init_db()
    # optionally start prometheus pushgateway or exporter (if desired)
    if settings.PROMETHEUS_ENABLED:
        # start a prometheus metrics HTTP endpoint if running as separate process is not used
        # Note: prometheus_client.start_http_server opens a blocking thread for metrics
        start_http_server(8001)

app.include_router(api_router)
