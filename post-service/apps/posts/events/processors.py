from typing import Any

from tortoise.exceptions import DoesNotExist

from apps.core.processors import AbstractBaseStreamEventProcessor
from apps.posts.events.producers import post_delete_requested_completed_event
from apps.posts.models import Post
from apps.posts.schemas import Post_Pydantic
from apps.posts.utils import set_and_calculate_post_popularity_and_rating


class PostReactionCreatedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            post_object = await Post.get(id=message.get("post_id"))
            await Post.get(id=message.get("post_id")).update(total_reactions=post_object.total_reactions+1)
            await post_object.refresh_from_db()
            await set_and_calculate_post_popularity_and_rating(post_object)


class PostReactionDeletedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            post_object = await Post.get(id=message.get("post_id"))
            await Post.get(id=message.get("post_id")).update(total_reactions=post_object.total_reactions-1)
            await post_object.refresh_from_db()
            await set_and_calculate_post_popularity_and_rating(post_object)


class PostCommentCreatedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            post_object = await Post.get(id=message.get("post_id"))
            await Post.get(id=message.get("post_id")).update(total_comments=post_object.total_comments+1)
            await post_object.refresh_from_db()
            await set_and_calculate_post_popularity_and_rating(post_object)


class PostCommentDeletedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            post_object = await Post.get(id=message.get("post_id"))
            await Post.get(id=message.get("post_id")).update(total_comments=post_object.total_comments-1)
            await post_object.refresh_from_db()
            await set_and_calculate_post_popularity_and_rating(post_object)


class ModerationPostDeletRequestedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            try:
                post = await Post.get(id=message.get("content_id"))
            except DoesNotExist:
                pass
            else:
                await post.delete()
                await post_delete_requested_completed_event(await Post_Pydantic.from_tortoise_orm(post))


class PostViewedRequestedEventProcessor(AbstractBaseStreamEventProcessor):
    async def process(self) -> Any:
        for message in self.get_decoded_messages():
            post = await Post.get(id=message.get("id"))
            view_counts = post.total_views + 1
            await Post.get(id=message.get("id")).update(total_views=view_counts)
            await post.refresh_from_db()
            await set_and_calculate_post_popularity_and_rating(post)
