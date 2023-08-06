from typing import Any

from apps.core.processors import AbstractBaseStreamEventProcessor
from apps.moderations import ContentTypes, StatusChoices
from apps.moderations.models import Moderation
from apps.moderations.services import fake_content_analysis


class PostCreatedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            await fake_content_analysis(message, ContentTypes.POST)


class PostUpdatedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            await fake_content_analysis(message, ContentTypes.POST)


class ModerationPostDeleteRequestCompletedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            await Moderation.get(content_id=message.get("id"), status=StatusChoices.DELETE_REQUESTED).update(
                status=StatusChoices.DELETE_CONFIRMED
            )


class PostCommentCreatedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            await fake_content_analysis(message, ContentTypes.COMMENT)


class PostCommentUpdatedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            await fake_content_analysis(message, ContentTypes.COMMENT)


class ModerationPostCommentDeleteRequestCompletedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            await Moderation.get(content_id=message.get("id"), status=StatusChoices.DELETE_REQUESTED).update(
                status=StatusChoices.DELETE_CONFIRMED
            )
