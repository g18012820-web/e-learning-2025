from typing import Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(...)
    REDIS_URL: str = Field(...)
    JWT_SECRET: str = Field(...)
    SENTRY_DSN: Optional[str] = None
    BACKUP_STORAGE: str = 'local'
    S3_ENDPOINT: Optional[str] = None
    S3_BUCKET: Optional[str] = None
    S3_KEY: Optional[str] = None
    S3_SECRET: Optional[str] = None
    PROMETHEUS_ENABLED: bool = True

    class Config:
        env_file = '.env'

settings = Settings()
