#!/usr/bin/env python3
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.settings import settings

async def run_sql(path):
    engine = create_async_engine(settings.DATABASE_URL, future=True)
    async with engine.begin() as conn:
        with open(path, 'r') as f:
            sql = f.read()
            await conn.execute(sql)
    await engine.dispose()

if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else 'backend/migrations/init_notifications.sql'
    asyncio.run(run_sql(path))
