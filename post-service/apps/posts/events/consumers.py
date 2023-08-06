from functools import lru_cache
import logging

from apps.core.redis import get_redis_client
from apps.posts.events import EVENT_CONSUMER_GROUP, EventConsumerKeys
from apps.posts.events.processors import (
    PostReactionCreatedEventProcessor,
    PostReactionDeletedEventProcessor,
    PostCommentCreatedEventProcessor,
    PostCommentDeletedEventProcessor,
    ModerationPostDeletRequestedEventProcessor,
    PostViewedRequestedEventProcessor,
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


async def consume_user_registered(redis_client=redis_client):

    create_consumer_group(EventConsumerKeys.USER_REGISTERED)

    try:
        results = redis_client.xreadgroup(
            EVENT_CONSUMER_GROUP,
            EventConsumerKeys.USER_REGISTERED,
            {
                EventConsumerKeys.USER_REGISTERED: ">"
            },
            None
        )
    except Exception as err:
        LOGGER.exception(f"Result error due to {err}")
    else:
        LOGGER.info("Reading user registered event from redis stream")
        print(results)


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


async def consume_comment_deleted(redis_client=redis_client):

    create_consumer_group(EventConsumerKeys.POST_COMMENT_DELETED)

    try:
        results = redis_client.xreadgroup(
            EVENT_CONSUMER_GROUP,
            EventConsumerKeys.POST_COMMENT_DELETED,
            {
                EventConsumerKeys.POST_COMMENT_DELETED: ">"
            },
            None
        )
    except Exception as err:
        LOGGER.exception(f"Result error due to {err}")
    else:
        LOGGER.info("Reading comment deleted event from redis stream")
        if results:
            await PostCommentDeletedEventProcessor(results).process()


async def consume_reaction_created(redis_client=redis_client):

    create_consumer_group(EventConsumerKeys.POST_REACTION_CREATED)

    try:
        results = redis_client.xreadgroup(
            EVENT_CONSUMER_GROUP,
            EventConsumerKeys.POST_REACTION_CREATED,
            {
                EventConsumerKeys.POST_REACTION_CREATED: ">"
            },
            None
        )
    except Exception as err:
        LOGGER.exception(f"Result error due to {err}")
    else:
        LOGGER.info("Reading post reaction added from redis stream")
        if results:
            await PostReactionCreatedEventProcessor(results).process()


async def consume_reaction_deleted(redis_client=redis_client):

    create_consumer_group(EventConsumerKeys.POST_REACTION_DELETED)

    try:
        results = redis_client.xreadgroup(
            EVENT_CONSUMER_GROUP,
            EventConsumerKeys.POST_REACTION_DELETED,
            {
                EventConsumerKeys.POST_REACTION_DELETED: ">"
            },
            None
        )
    except Exception as err:
        LOGGER.exception(f"Result error due to {err}")
    else:
        LOGGER.info("Reading post reaction deleted from redis stream")
        if results:
            await PostReactionDeletedEventProcessor(results).process()


async def consume_moderation_post_deleted(redis_client=redis_client):

    create_consumer_group(EventConsumerKeys.POST_DELETE_REQUESTED)

    try:
        results = redis_client.xreadgroup(
            EVENT_CONSUMER_GROUP,
            EventConsumerKeys.POST_DELETE_REQUESTED,
            {
                EventConsumerKeys.POST_DELETE_REQUESTED: ">"
            },
            None
        )
    except Exception as err:
        LOGGER.exception(f"Result error due to {err}")
    else:
        LOGGER.info("Reading post reaction deleted from redis stream")
        if results:
            await ModerationPostDeletRequestedEventProcessor(results).process()


async def consume_post_viewed_event(redis_client=redis_client):

    create_consumer_group(EventConsumerKeys.POST_VIEWED)

    try:
        results = redis_client.xreadgroup(
            EVENT_CONSUMER_GROUP,
            EventConsumerKeys.POST_VIEWED,
            {
                EventConsumerKeys.POST_VIEWED: ">"
            },
            None
        )
    except Exception as err:
        LOGGER.exception(f"Result error due to {err}")
    else:
        LOGGER.info("Reading post viewed event from redis stream")
        if results:
            await PostViewedRequestedEventProcessor(results).process()
