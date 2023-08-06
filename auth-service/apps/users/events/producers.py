import logging

from apps.core.redis import get_redis_client
from apps.users.events import EventProduerKeys

LOGGER = logging.getLogger(__name__)

redis_client = get_redis_client()


async def user_registered_event(user, redis_client=redis_client):

    LOGGER.info("Sending event for registered user.")
    try:
        redis_client.xadd(EventProduerKeys.USER_REGISTERED, {"message": user.json(), "type": "json"}, "*")
    except Exception as err:
        LOGGER.exception(f"Sending event failed due to {err}")
    else:
        LOGGER.info("Successfully sent event for registered user.")
