from functools import lru_cache
import logging

from apps.core.redis import get_redis_client
from apps.interactions.events import EventConsumerKeys, EVENT_CONSUMER_GROUP
from apps.interactions.events.processors import (
    ModerationPostDeleteRequestEventProcessor,
    PostCreatedEventProcessor,
    PostDeletedEventProcessor,
)

LOGGER = logging.getLogger(__name__)

redis_client = get_redis_client()


@lru_cache
def create_consumer_group(consumer_key: str, group_name: str = None) -> None:

    if group_name is None:
        group_name = EVENT_CONSUMER_GROUP

    # Creating redis consumer group
    try:
        LOGGER.info(f"Creating consumer group with name [{group_name}]")
        redis_client.xgroup_create(consumer_key, group_name, mkstream=True)
    except Exception:
        LOGGER.info(f"{group_name} Group already exists!")


async def consume_post_created(redis_client=redis_client):
    create_consumer_group(EventConsumerKeys.POST_CREATED)
    try:
        results = redis_client.xreadgroup(
            EVENT_CONSUMER_GROUP,
            EventConsumerKeys.POST_CREATED,
            {
                EventConsumerKeys.POST_CREATED: ">"
            },
            None
        )
    except Exception as err:
        LOGGER.exception(f"Result error due to {err}")
    else:
        LOGGER.info("Reading from redis stream for interaction backend")
        if results:
            await PostCreatedEventProcessor(results).process()


async def consume_post_deleted(redis_client=redis_client):
    create_consumer_group(EventConsumerKeys.POST_DELETED)
    try:
        results = redis_client.xreadgroup(
            EVENT_CONSUMER_GROUP,
            EventConsumerKeys.POST_DELETED,
            {
                EventConsumerKeys.POST_DELETED: ">"
            },
            None
        )
    except Exception as err:
        LOGGER.exception(f"Result error due to {err}")
    else:
        LOGGER.info("Reading from redis stream for interaction backend")
        if results:
            await PostDeletedEventProcessor(results).process()


async def consume_moderation_post_comment_delete_requested(redis_client=redis_client):
    create_consumer_group(EventConsumerKeys.MODERATION_POST_COMMENT_DELETE_REQUESTED)
    try:
        results = redis_client.xreadgroup(
            EVENT_CONSUMER_GROUP,
            EventConsumerKeys.MODERATION_POST_COMMENT_DELETE_REQUESTED,
            {
                EventConsumerKeys.MODERATION_POST_COMMENT_DELETE_REQUESTED: ">"
            },
            None
        )
    except Exception as err:
        LOGGER.exception(f"Result error due to {err}")
    else:
        LOGGER.info("Reading from redis stream for moderation post comment delete requested event")
        if results:
            await ModerationPostDeleteRequestEventProcessor(results).process()
