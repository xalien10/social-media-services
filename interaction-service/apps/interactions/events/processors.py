import logging
from typing import Any

from apps.core.processors import AbstractBaseStreamEventProcessor
from apps.interactions.models import Comment, PostReaction
from apps.interactions.events.producers import moderation_post_comment_delete_request_completed_event
from apps.interactions.schemas import Comment_Pydantic

LOGGER = logging.getLogger(__name__)


class PostCreatedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            print(message)


class PostDeletedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            LOGGER.info("Processing comments and reactions of post [%s] due to post deleted event.", message.get("id"))

            await Comment.filter(id=message.get("id")).delete()
            await PostReaction.filter(id=message.get("id")).delete()
            LOGGER.info(
                "Successfully processed moderation post delete request event for comment [%s]",
                message.get("content_id")
            )
            LOGGER.info(
                "Successfullly processed comments and reactions of post [%s] due to post deleted event.",
                message.get("id")
            )


class ModerationPostDeleteRequestEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            LOGGER.info("Processing moderation post delete request event for comment [%s]", message.get("content_id"))
            comment = await Comment.get(id=message.get("content_id"))
            await comment.delete()
            LOGGER.info(
                "Successfully processed moderation post delete request event for comment [%s]",
                message.get("content_id")
            )
            await moderation_post_comment_delete_request_completed_event(
                await Comment_Pydantic.from_tortoise_orm(comment)
            )
