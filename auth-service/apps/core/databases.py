from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from apps.settings import get_settings

settings = get_settings()


TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL.split("?")[0]},
    "apps": {
        "models": {
            "models": settings.MODELS,
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:

    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
