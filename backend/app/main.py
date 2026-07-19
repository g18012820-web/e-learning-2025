from fastapi import FastAPI
from app.api.v1 import api_router
from app.core.settings import settings
from app.db.connection import init_db
from prometheus_client import start_http_server
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.metrics.instrumentation import PrometheusMiddleware
import asyncio

app = FastAPI(title="e-learning-2025 API")

# Add middlewares
app.add_middleware(RateLimiterMiddleware, calls=200, period=60)
app.add_middleware(PrometheusMiddleware)

@app.on_event('startup')
async def startup_event():
    # initialize DB connection pools
    await init_db()
    # optionally start prometheus exporter thread if not running externally
    if settings.PROMETHEUS_ENABLED:
        start_http_server(8001)

app.include_router(api_router)
