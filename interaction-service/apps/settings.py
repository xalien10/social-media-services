from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite://:memory:"
    SECRET_KEY: str = "SuperSecret Key"
    APP_NAME: str = "Interaction Service API"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20160  # 14 Days
    TOKEN_ALGORITHM: str = "HS256"
    # SMTP_SERVER: str
    MAIL_SENDER: str = "noreply@example.com"
    API_PREFIX: str = "/api/v1"
    HOST: str = "localhost"
    PORT: str = 8001
    BASE_URL: str = "{}:{}/".format(HOST, str(PORT))
    MODELS: list[str] = [
        "apps.interactions.models", "aerich.models"
    ]
    AUTHENTICATION_VERIFICATION_URL: str = "http://0.0.0.0:8000/api/v1/auth/verify-token"
    REDIS_URL: str = "redis://127.0.0.1:6379"
    POST_SERVICE_URL: str = "http://127.0.0.1:8001"


@lru_cache()
def get_settings():
    return Settings()
