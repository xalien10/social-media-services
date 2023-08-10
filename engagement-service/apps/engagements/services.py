import json
import logging

from apps.engagements import InterestChoices
from apps.engagements.models import UserEngagement


LOGGER = logging.getLogger(__name__)


async def create_user_engagement_profile(user_data: dict) -> None:
    LOGGER.info("Generating user engagement profile for user [%s].", user_data.get("id"))

    user_exists = await UserEngagement.exists(user_id=user_data.get("id"))
    if not user_exists:
        interests_data = {choice: 0.0 for choice in InterestChoices.values()}
        await UserEngagement.create(user_id=user_data.get("id"), summary=json.dumps(interests_data))
    LOGGER.info("Successfully generated user engagement profile for user [%s].", user_data.get("id"))
