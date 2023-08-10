import json
import logging

from apps.core.redis import get_redis_client
from apps.interactions.events import EventProduerKeys

LOGGER = logging.getLogger(__name__)

redis_client = get_redis_client()


async def comment_created_event(comment, redis_client=redis_client):

    LOGGER.info("Sending event for post comment.")
    try:
        redis_client.xadd(EventProduerKeys.POST_COMMENT_CREATED, {"message": comment.json(), "type": "json"}, "*")
    except Exception as err:
        LOGGER.exception(f"Sending event failed due to {err}")
    else:
        LOGGER.info("Successfully sent event for post comment.")


async def comment_deleted_event(comment, redis_client=redis_client):

    LOGGER.info("Sending event for post comment deleted.")
    try:
        redis_client.xadd(EventProduerKeys.POST_COMMENT_DELETED, {"message": comment.json(), "type": "json"}, "*")
    except Exception as err:
        LOGGER.exception(f"Sending event failed due to {err}")
    else:
        LOGGER.info("Successfully sent event for post comment deleted.")


async def post_reaction_created_event(post_reaction, redis_client=redis_client):

    LOGGER.info("Sending event for post reaction added.")
    try:
        redis_client.xadd(
            EventProduerKeys.POST_REACTION_CREATED,
            {
                "message": post_reaction.json(),
                "type": "json"
            },
            "*"
        )
    except Exception as err:
        LOGGER.exception(f"Sending event failed due to {err}")
    else:
        LOGGER.info("Successfully sent event for post reaction addeed.")


async def post_reaction_deleted_event(post_reaction, redis_client=redis_client):

    LOGGER.info("Sending event for post reaction deleted.")
    try:
        redis_client.xadd(
            EventProduerKeys.POST_REACTION_DELETED,
            {
                "message": post_reaction.json(), "type": "json"
            },
            "*"
        )
    except Exception as err:
        LOGGER.exception(f"Sending event failed due to {err}")
    else:
        LOGGER.info("Successfully sent event for post reaction deleted.")


async def moderation_post_comment_delete_request_completed_event(post_comment, redis_client=redis_client):

    LOGGER.info("Sending moderation post comment delete request completed event.")
    try:
        redis_client.xadd(
            EventProduerKeys.MODERATION_POST_COMMENT_DELETE_REQUEST_COMPLETED,
            {
                "message": post_comment.json(), "type": "json"
            },
            "*"
        )
    except Exception as err:
        LOGGER.exception(f"Sending event failed due to {err}")
    else:
        LOGGER.info("Successfully sent moderation post comment delete request completed event.")


async def generate_post_view_event(post: dict, redis_client=redis_client):

    LOGGER.info("Sending post view event.")
    try:
        redis_client.xadd(
            EventProduerKeys.POST_VIEWED,
            {
                "message": json.dumps(post, indent=2), "type": "json"
            },
            "*"
        )
    except Exception as err:
        LOGGER.exception(f"Sending event failed due to {err}")
    else:
        LOGGER.info("Successfully post view event.")
    return post
