import logging

from apps.core.redis import get_redis_client
from apps.posts.events import EventProduerKeys

LOGGER = logging.getLogger(__name__)

redis_client = get_redis_client()


async def post_delete_requested_completed_event(post, redis_client=redis_client):

    LOGGER.info("Sending post delete requested completed event.")
    try:
        redis_client.xadd(
            EventProduerKeys.MODERATION_POST_DELETE_REQUEST_COMPLETED, {"message": post.json(), "type": "json"}, "*"
        )
    except Exception as err:
        LOGGER.exception(f"Sending event failed due to {err}")
    else:
        LOGGER.info("Successfully sent post delete requested completed event.")


async def post_delete_event(post, redis_client=redis_client):

    LOGGER.info("Sending post deleted event.")
    try:
        redis_client.xadd(
            EventProduerKeys.POST_DELETED, {"message": post.json(), "type": "json"}, "*"
        )
    except Exception as err:
        LOGGER.exception(f"Sending event failed due to {err}")
    else:
        LOGGER.info("Successfully sent post deleted event.")


async def post_created_event(post, redis_client=redis_client):

    LOGGER.info("Sending post created event.")
    try:
        redis_client.xadd(EventProduerKeys.POST_CREATED, {"message": post.json(), "type": "json"}, "*")
    except Exception as err:
        LOGGER.exception(f"Sending event failed due to {err}")
    else:
        LOGGER.info("Successfully sent post comment delete requested event.")


async def post_updated_event(post, redis_client=redis_client):

    LOGGER.info("Sending post updated event.")
    try:
        redis_client.xadd(EventProduerKeys.POST_UPDATED, {"message": post.json(), "type": "json"}, "*")
    except Exception as err:
        LOGGER.exception(f"Sending event failed due to {err}")
    else:
        LOGGER.info("Successfully sent post updated event.")
