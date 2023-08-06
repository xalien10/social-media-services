import logging
from typing import Type

from tortoise.signals import post_save
from tortoise import BaseDBAsyncClient

from apps.engagements.models import UserEngagement

logging.basicConfig(level="INFO")

LOGGER = logging.getLogger(__name__)


@post_save(UserEngagement)
async def user_engagement_profile_created_or_updated(
    sender: "Type[UserEngagement]", instance: UserEngagement, created: bool,
    using_db: BaseDBAsyncClient | None, update_fields: list[str]
) -> None:
    if created:
        LOGGER.info("Sending user engagement profile created event to redis subscriber.")
        print(sender, instance, using_db, update_fields)
        LOGGER.info("Successfully sent post created event to redis subscriber.")
    else:
        LOGGER.info("Sending user engagement profile created event to redis subscriber.")
        print(sender, instance, using_db, update_fields)
        LOGGER.info("Successfully user engagement profile created event to redis subscriber.")
