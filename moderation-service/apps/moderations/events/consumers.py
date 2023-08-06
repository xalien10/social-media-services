from functools import lru_cache
import logging

from apps.core.redis import get_redis_client
from apps.moderations.events import EVENT_CONSUMER_GROUP, EventConsumerKeys
from apps.moderations.events.processors import (
    PostCreatedEventProcessor,
    PostUpdatedEventProcessor,
    ModerationPostDeleteRequestCompletedEventProcessor,
    PostCommentCreatedEventProcessor,
    PostCommentUpdatedEventProcessor,
    ModerationPostCommentDeleteRequestCompletedEventProcessor,
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
        LOGGER.info("Reading post created from redis stream")
        if results:
            await PostCreatedEventProcessor(results).process()


async def consume_post_updated(redis_client=redis_client):

    create_consumer_group(EventConsumerKeys.POST_UPDATED)

    try:
        results = redis_client.xreadgroup(
            EVENT_CONSUMER_GROUP,
            EventConsumerKeys.POST_UPDATED,
            {
                EventConsumerKeys.POST_UPDATED: ">"
            },
            None
        )
    except Exception as err:
        LOGGER.exception(f"Result error due to {err}")
    else:
        LOGGER.info("Reading post updated from redis stream")
        if results:
            await PostUpdatedEventProcessor(results).process()


async def consume_post_request_delete_completed(redis_client=redis_client):

    create_consumer_group(EventConsumerKeys.MODERATION_POST_DELETE_REQUEST_COMPLETED)

    try:
        results = redis_client.xreadgroup(
            EVENT_CONSUMER_GROUP,
            EventConsumerKeys.MODERATION_POST_DELETE_REQUEST_COMPLETED,
            {
                EventConsumerKeys.MODERATION_POST_DELETE_REQUEST_COMPLETED: ">"
            },
            None
        )
    except Exception as err:
        LOGGER.exception(f"Result error due to {err}")
    else:
        LOGGER.info("Reading post deleted from redis stream")
        if results:
            await ModerationPostDeleteRequestCompletedEventProcessor(results).process()


async def consume_comment_created(redis_client=redis_client):

    create_consumer_group(EventConsumerKeys.POST_COMMENT_CREATED)

    try:
        results = redis_client.xreadgroup(
            EVENT_CONSUMER_GROUP,
            EventConsumerKeys.POST_COMMENT_CREATED,
            {
                EventConsumerKeys.POST_COMMENT_CREATED: ">"
            },
            None
        )
    except Exception as err:
        LOGGER.exception(f"Result error due to {err}")
    else:
        LOGGER.info("Reading comment created event from redis stream")
        if results:
            await PostCommentCreatedEventProcessor(results).process()


async def consume_comment_updated(redis_client=redis_client):

    create_consumer_group(EventConsumerKeys.POST_COMMENT_UPDATED)

    try:
        results = redis_client.xreadgroup(
            EVENT_CONSUMER_GROUP,
            EventConsumerKeys.POST_COMMENT_UPDATED,
            {
                EventConsumerKeys.POST_COMMENT_UPDATED: ">"
            },
            None
        )
    except Exception as err:
        LOGGER.exception(f"Result error due to {err}")
    else:
        LOGGER.info("Reading comment created event from redis stream")
        if results:
            await PostCommentUpdatedEventProcessor(results).process()


async def consume_comment_deleted(redis_client=redis_client):

    create_consumer_group(EventConsumerKeys.MODERATION_POST_COMMENT_DELETE_REQUEST_COMPLETED)

    try:
        results = redis_client.xreadgroup(
            EVENT_CONSUMER_GROUP,
            EventConsumerKeys.MODERATION_POST_COMMENT_DELETE_REQUEST_COMPLETED,
            {
                EventConsumerKeys.MODERATION_POST_COMMENT_DELETE_REQUEST_COMPLETED: ">"
            },
            None
        )
    except Exception as err:
        LOGGER.exception(f"Result error due to {err}")
    else:
        LOGGER.info("Reading comment deleted event from redis stream")
        if results:
            await ModerationPostCommentDeleteRequestCompletedEventProcessor(results).process()
