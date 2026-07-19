from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.settings import settings
import aioredis
import time

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.redis = None

    async def dispatch(self, request: Request, call_next):
        if not self.redis:
            self.redis = await aioredis.from_url(settings.REDIS_URL)
        client_ip = request.client.host if request.client else 'unknown'
        key = f"ratelimit:{client_ip}"
        cur = await self.redis.get(key)
        if cur is None:
            await self.redis.set(key, 1, ex=self.period)
        else:
            cur = int(cur)
            if cur >= self.calls:
                raise HTTPException(status_code=429, detail='Too Many Requests')
            await self.redis.incr(key)
        response = await call_next(request)
        return response
