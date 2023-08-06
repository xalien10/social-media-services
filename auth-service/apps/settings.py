from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite://:memory:"
    SECRET_KEY: str = "SuperSecret Key"
    APP_NAME: str = "Authentication Service API"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20160  # 14 Days
    TOKEN_ALGORITHM: str = "HS256"
    # SMTP_SERVER: str
    MAIL_SENDER: str = "noreply@example.com"
    API_PREFIX: str = "/api/v1"
    HOST: str = "localhost"
    PORT: str = 8000
    BASE_URL: str = "{}:{}/".format(HOST, str(PORT))
    MODELS: list[str] = [
        "apps.users.models", "aerich.models"
    ]
    REDIS_URL: str = "redis://127.0.0.1:6379"


@lru_cache()
def get_settings():
    return Settings()
