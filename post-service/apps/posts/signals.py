import logging
from typing import Type

from tortoise.signals import post_save, post_delete
from tortoise import BaseDBAsyncClient

from apps.posts.events.producers import (
    post_created_event,
    post_updated_event,
    post_delete_event,
)
from apps.posts.models import Post, PostNFT, NFTStatusChoices, StatusChoices
from apps.posts.schemas import Post_Pydantic

logging.basicConfig(level="INFO")

LOGGER = logging.getLogger(__name__)


@post_delete(Post)
async def post_deleted(
    sender: "Type[Post]", instance: Post, using_db: BaseDBAsyncClient | None
) -> None:
    # TODO: Need to send post to analysis service by Redis publish service
    LOGGER.info("Sending post deleted event to redis subscriber.")
    await post_delete_event(await Post_Pydantic.from_tortoise_orm(instance))
    LOGGER.info("Successfully sent post deleted event to redis subscriber.")

    LOGGER.info("Deleting PostNFT for post [%s] those are failed or waiting for minting", instance.id)
    await PostNFT.get(
        post_id=instance.id,
        status__in=[NFTStatusChoices.READY_FOR_MINTING, NFTStatusChoices.MINTING_FAILED]
    ).delete()
    LOGGER.info("Successfully deleted PostNFT for post [%s] those are failed or waiting for minting", instance.id)


@post_save(Post)
async def post_created_or_updated(
    sender: "Type[Post]", instance: Post, created: bool, using_db: BaseDBAsyncClient | None, update_fields: list[str]
) -> None:
    # TODO: Need to send post to analysis service by Redis publish service
    if created:
        LOGGER.info("Sending post created event to redis subscriber.")
        await post_created_event(await Post_Pydantic.from_tortoise_orm(instance))
        LOGGER.info("Successfully sent post created event to redis subscriber.")
    else:
        LOGGER.info("Sending post updated event to redis subscriber.")
        await post_updated_event(await Post_Pydantic.from_tortoise_orm(instance))
        LOGGER.info("Successfully sent post updated event to redis subscriber.")

    if instance.status == StatusChoices.POSTED:
        await generate_post_nft(instance)


async def generate_post_nft(post: Post) -> None:
    LOGGER.info("Generating Post NFT for post [%s]", post.id)
    post_nft = await PostNFT.exists(post_id=post.id, status=NFTStatusChoices.READY_FOR_MINTING)
    if post_nft:
        await PostNFT.get(post_id=post.id, status=NFTStatusChoices.READY_FOR_MINTING).update(
            post=post, description=f"Post created by {post.created_by} at {post.created_at}",
            data=generate_nft_data_from_post(post), created_by=post.created_by, updated_by=post.updated_by
        )
    else:
        await PostNFT.create(
            post=post, description=f"Post created by {post.created_by} at {post.created_at}",
            data=generate_nft_data_from_post(post), created_by=post.created_by
        )
    LOGGER.info("Successfully, generated Post NFT for post [%s]", post.id)


def generate_nft_data_from_post(post: Post) -> dict:
    nft_data = {
        "name": post.id,
        "description": f"Post created by {post.created_by}",
        "image": None,
        "metadata": {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "types": post.types,
            "total_views": post.total_views,
            "total_comments": post.total_comments,
            "total_reactions": post.total_reactions,
            "score": post.score,
            "popularity": post.popularity,
            "created_by": post.created_by,
            "created_at": post.created_at,
            "updated_by": post.updated_by,
            "updated_at": post.updated_at
        }
    }
    return nft_data
