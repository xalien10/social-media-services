import json
import logging

from apps.engagements import InterestChoices
from apps.engagements.models import UserEngagement


LOGGER = logging.getLogger(__name__)


async def create_user_engagement_profile(user_data: dict) -> UserEngagement:
    LOGGER.info("Generating user engagement profile for user [%s].", user_data.get("id"))

    profile = await UserEngagement.get_or_none(user_id=user_data.get("id"))
    if profile is None:
        interests_data = {choice: 0.0 for choice in InterestChoices.values()}
        profile = await UserEngagement.create(user_id=user_data.get("id"), summary=json.dumps(interests_data))
        LOGGER.info("Successfully generated user engagement profile for user [%s].", user_data.get("id"))
    return profile


async def calculate_and_update_user_engagement_score(
        profile: UserEngagement, message: dict, action_type: str = "CREATE"
) -> None:
    LOGGER.info("Calculating user engagement profile score for user [%s].", message.get("created_by"))
    interests_data = profile.summary
    categories = message.get("types")
    for category in categories:
        match action_type:
            case "CREATE":
                interests_data[category] = interests_data[category] + 1
            case "UPDATE":
                interests_data[category] = interests_data[category] + 1
            case "DELETE":
                interests_data[category] = interests_data[category] - 1
    return await UserEngagement.filter(user_id=profile.user_id).update(summary=json.dumps(interests_data))
