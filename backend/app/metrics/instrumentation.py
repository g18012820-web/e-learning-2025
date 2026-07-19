from fastapi import Request
from prometheus_client import Counter, Histogram
import time

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP request latency', ['endpoint'])

class PrometheusMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return
        method = scope['method']
        path = scope['path']
        start = time.time()
        async def send_wrapper(message):
            if message['type'] == 'http.response.start':
                status = message['status']
                REQUEST_COUNT.labels(method=method, endpoint=path, http_status=str(status)).inc()
            await send(message)
        await self.app(scope, receive, send_wrapper)
        duration = time.time() - start
        try:
            REQUEST_LATENCY.labels(endpoint=path).observe(duration)
        except Exception:
            pass
