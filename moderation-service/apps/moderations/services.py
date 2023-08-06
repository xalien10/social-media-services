import json
import logging
import random

from tortoise.exceptions import IntegrityError
from apps.moderations import ContentTypes
from apps.moderations.events.producers import post_delete_requested_event, post_comment_delete_requested_event
from apps.moderations.models import Moderation
from apps.moderations.schemas import Moderation_Pydantic

LOGGER = logging.getLogger(__name__)


def get_random_choice() -> bool:
    options = [True, False]
    seed_value = random.randint(0, 1000)
    random.seed(seed_value)
    return random.choice(options)


async def fake_content_analysis(content: dict, content_type: str) -> None:
    is_offensive_content = get_random_choice()
    if is_offensive_content:
        LOGGER.info("Generating moderation action for content with type [%s]", content_type.value)
        try:
            moderation = await Moderation.create(
                **{"type": content_type, "raw_content": json.dumps(content), "content_id": content.get("id")}
            )
        except IntegrityError as err:
            LOGGER.exception(f"Could not create moderation action due to {err}")
        else:
            if content_type == ContentTypes.POST:
                await post_delete_requested_event(await Moderation_Pydantic.from_tortoise_orm(moderation))
            else:
                await post_comment_delete_requested_event(await Moderation_Pydantic.from_tortoise_orm(moderation))
            LOGGER.info("Successfully generated moderation action for content")
