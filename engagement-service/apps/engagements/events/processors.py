import logging
from typing import Any

from tortoise.exceptions import DoesNotExist

from apps.core.processors import AbstractBaseStreamEventProcessor
from apps.engagements.services import (
    create_user_engagement_profile,
    UserEngagement,
    calculate_and_update_user_engagement_score,
)


LOGGER = logging.getLogger(__name__)


class UserRegisteredEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            LOGGER.info("Processing user registered event for user [%s].", message.get("id"))
            return await create_user_engagement_profile(message)


class PostCreatedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            LOGGER.info("Processing post created event for user [%s].", message.get("created_by"))
            try:
                profile = await UserEngagement.get(user_id=message.get("created_by"))
            except DoesNotExist:
                profile = await create_user_engagement_profile({"id": message.get("created_by")})
            if profile:
                total_posts = profile.total_owned_posts + 1
                await UserEngagement.get(user_id=message.get("created_by")).update(total_owned_posts=total_posts)
                await profile.refresh_from_db()
                await calculate_and_update_user_engagement_score(profile, message)
        return


class PostDeletedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            LOGGER.info("Processing post deleted event for user [%s].", message.get("created_by"))
            try:
                profile = await UserEngagement.get(user_id=message.get("created_by"))
            except DoesNotExist:
                profile = await create_user_engagement_profile({"id": message.get("created_by")})
            if profile:
                total_posts = profile.total_owned_posts - 1
                await UserEngagement.get(user_id=message.get("created_by")).update(
                    total_owned_posts=max(0, total_posts)
                )
                await profile.refresh_from_db()
                await calculate_and_update_user_engagement_score(profile, message, "DELETE")
        return


class PostUpdatedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            LOGGER.info("Processing post updated event for user [%s].", message.get("created_by"))
            print(message)
        return


class ModerationPostDeleteRequestCompletedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            LOGGER.info("Processing moderation post deleted event for user [%s].", message.get("created_by"))
            print(message)
            # TODO: Need to generate notification for post owner
        return


class PostCommentCreatedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            LOGGER.info("Processing post comment created event for user [%s].", message.get("created_by"))
            try:
                profile = await UserEngagement.get(user_id=message.get("created_by"))
            except DoesNotExist:
                profile = await create_user_engagement_profile({"id": message.get("created_by")})
            total_post_comments = profile.total_post_comments + 1
            await UserEngagement.get(user_id=message.get("created_by")).update(
                total_post_comments=total_post_comments
            )
            await profile.refresh_from_db()
            # await calculate_and_update_user_engagement_profile(profile)
            # TODO: Need to generate notification for post owner
        return


class PostCommentUpdatedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            print(message)
        return


class ModerationPostCommentDeleteRequestCompletedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            print(message)
            # TODO: Need to generate notification for post comment owner
        return


class PostViewedRequestedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            LOGGER.info("Processing post viewed event for user [%s].", message.get("viewed_by"))
            try:
                profile = await UserEngagement.get(user_id=message.get("viewed_by"))
            except DoesNotExist:
                profile = await create_user_engagement_profile({"id": message.get("viewed_by")})
            if profile:
                total_post_views = profile.total_post_views + 1
                await UserEngagement.get(user_id=message.get("viewed_by")).update(total_post_views=total_post_views)
                await profile.refresh_from_db()
                # await calculate_and_update_user_engagement_profile(profile)
                print(message)
                # TODO: Need to generate notification for post owner
        return


class PostReactionCreatedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            LOGGER.info("Processing post reacted event for user [%s].", message.get("created_by"))
            try:
                profile = await UserEngagement.get(user_id=message.get("created_by"))
            except DoesNotExist:
                profile = await create_user_engagement_profile({"id": message.get("created_by")})
            total_post_reactions = profile.total_post_reactions + 1
            await UserEngagement.get(user_id=message.get("created_by")).update(
                total_post_reactions=total_post_reactions
            )
            await profile.refresh_from_db()
            # await calculate_and_update_user_engagement_profile(profile)
            # TODO: Need to generate notification for post owner
        return


class PostReactionDeletedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            LOGGER.info("Processing post reacted event for user [%s].", message.get("created_by"))
            try:
                profile = await UserEngagement.get(user_id=message.get("created_by"))
            except DoesNotExist:
                profile = await create_user_engagement_profile({"id": message.get("created_by")})
            total_post_reactions = profile.total_post_reactions - 1
            await UserEngagement.get(user_id=message.get("created_by")).update(
                total_post_reactions=total_post_reactions
            )
            await profile.refresh_from_db()
            # await calculate_and_update_user_engagement_profile(profile)
            # TODO: Need to generate notification for post owner
        return


class PostCommentDeletedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            LOGGER.info("Processing post comment deleted event for user [%s].", message.get("created_by"))
            try:
                profile = await UserEngagement.get(user_id=message.get("created_by"))
            except DoesNotExist:
                profile = await create_user_engagement_profile({"id": message.get("created_by")})
            if profile:
                total_post_comments = profile.total_post_comments - 1
                await UserEngagement.get(user_id=message.get("created_by")).update(
                    total_post_comments=total_post_comments
                )
                await profile.refresh_from_db()
                # await calculate_and_update_user_engagement_score(profile, message, "DELETE")
        return


class ModerationPostDeletRequestedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            print(message)
            # TODO: Need to generate notification for post owner
        return
