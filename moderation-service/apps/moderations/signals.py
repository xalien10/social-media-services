import logging
from typing import Type

from tortoise.signals import post_save
from tortoise import BaseDBAsyncClient

from apps.moderations import ContentTypes
from apps.moderations.events.producers import (
    post_delete_requested_event,
    post_comment_delete_requested_event,
)
from apps.moderations.models import Moderation
from apps.moderations.schemas import Moderation_Pydantic


logging.basicConfig(level="INFO")

LOGGER = logging.getLogger(__name__)


@post_save(Moderation)
async def post_created_or_updated(
    sender: "Type[Moderation]", instance: Moderation, created: bool, using_db: BaseDBAsyncClient | None,
    update_fields: list[str]
) -> None:
    if created:
        LOGGER.info("Sending moderation created event to redis subscriber.")
        match instance.type:
            case ContentTypes.POST:
                await post_delete_requested_event(await Moderation_Pydantic.from_tortoise_orm(instance))
            case ContentTypes.COMMENT:
                await post_comment_delete_requested_event(await Moderation_Pydantic.from_tortoise_orm(instance))
            case _:
                pass
        LOGGER.info("Successfully sent moderation created event to redis subscriber.")
