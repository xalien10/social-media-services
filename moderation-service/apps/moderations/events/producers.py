import logging

from apps.core.redis import get_redis_client
from apps.moderations.events import EventProduerKeys

LOGGER = logging.getLogger(__name__)

redis_client = get_redis_client()


async def post_delete_requested_event(moderation, redis_client=redis_client):

    LOGGER.info("Sending post delete requested event.")
    try:
        redis_client.xadd(EventProduerKeys.POST_DELETE_REQUESTED, {"message": moderation.json(), "type": "json"}, "*")
    except Exception as err:
        LOGGER.exception(f"Sending event failed due to {err}")
    else:
        LOGGER.info("Successfully sent post delete requested event.")


async def post_comment_delete_requested_event(moderation, redis_client=redis_client):

    LOGGER.info("Sending post comment delete requested event.")
    try:
        redis_client.xadd(
            EventProduerKeys.MODERATION_POST_COMMENT_DELETE_REQUESTED,
            {
                "message": moderation.json(), "type": "json"
            },
            "*"
        )
    except Exception as err:
        LOGGER.exception(f"Sending event failed due to {err}")
    else:
        LOGGER.info("Successfully sent post comment delete requested event.")
