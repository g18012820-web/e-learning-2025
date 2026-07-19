from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/elearning"
    REDIS_URL: str = "redis://localhost:6379/0"
    JWT_SECRET: str = "REPLACE_WITH_SECRET"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14

    class Config:
        env_file = ".env"

settings = Settings()
