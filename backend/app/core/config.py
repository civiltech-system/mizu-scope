from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://mizumap:mizumap_password@localhost:5432/mizumap"
    REDIS_URL: str = "redis://localhost:6379/0"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]
    APP_ENV: str = "development"

    model_config = {"env_file": ".env"}


settings = Settings()
