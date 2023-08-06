import json
import logging

from typing import Type

from tortoise import BaseDBAsyncClient
from tortoise.signals import post_save

from apps.core.models import UserDetailInfo
from apps.core.redis import normalize_redis_hash_data
from apps.users.events.producers import user_registered_event
from apps.users.models import User
from apps.users.schemas import User_Pydantic

logging.basicConfig(level="INFO")

LOGGER = logging.getLogger(__name__)


@post_save(User)
async def user_registered(
    sender: "Type[User]", instance: User, created: bool, using_db: BaseDBAsyncClient | None, update_fields: list[str]
) -> None:
    if created:
        LOGGER.info("Sending user registered event to redis subscriber.")
        await user_registered_event(await User_Pydantic.from_tortoise_orm(instance))
        LOGGER.info("Successfully sent user registered event to redis subscriber.")

    await generate_and_save_user_data_for_redis_hash_model(instance)


async def generate_and_save_user_data_for_redis_hash_model(user_instance: User) -> dict:
    connections = [str(connection.id) for connection in await user_instance.connections.all()]
    user = await User_Pydantic.from_tortoise_orm(user_instance)
    user_data = json.loads(user.json())
    user_detail_info = {
        "pk": str(user.id), **user_data, "connections": connections, "total_connections": len(connections)
    }

    LOGGER.info("Saving user detail info for redis hash model")
    UserDetailInfo(** await normalize_redis_hash_data(user_detail_info)).save()
    LOGGER.info("Successfully saved user detail info for redis hash model")
