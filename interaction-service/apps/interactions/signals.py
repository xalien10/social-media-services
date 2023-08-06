import logging
from typing import Type

from tortoise import BaseDBAsyncClient
from tortoise.signals import post_save, post_delete

from apps.interactions.events.producers import (
    comment_created_event,
    comment_deleted_event,
    post_reaction_created_event,
    post_reaction_deleted_event,
)
from apps.interactions.models import Comment, PostReaction, CommentNFT, NFTStatusChoices
from apps.interactions.schemas import Comment_Pydantic, PostReaction_Pydantic

logging.basicConfig(level="INFO")

LOGGER = logging.getLogger(__name__)


@post_save(Comment)
async def comment_added_or_updated(
    sender: "Type[Comment]", instance: Comment, created: bool, using_db: BaseDBAsyncClient | None,
    update_fields: list[str]
) -> None:
    # TODO: Need to send post to analysis service by Redis publish service
    if created:
        LOGGER.info("Sending comment added event to redis subscribers.")
        await comment_created_event(await Comment_Pydantic.from_tortoise_orm(instance))
        LOGGER.info("Successfully sent comment added event to redis subscribers.")
    await generate_comment_nft(instance)


@post_delete(Comment)
async def comment_deleted(sender: "Type[Comment]", instance: Comment, using_db: BaseDBAsyncClient | None) -> None:
    # TODO: Need to send post to analysis service by Redis publish service
    LOGGER.info("Sending comment deleted event to redis subscribers.")
    await comment_deleted_event(await Comment_Pydantic.from_tortoise_orm(instance))
    LOGGER.info("Successfully sent comment deleted event to redis subscribers.")

    LOGGER.info("Deleting CommentNFT for comment [%s] those are failed or waiting for minting", instance.id)
    await CommentNFT.get(
        comment_id=instance.id,
        status__in=[NFTStatusChoices.READY_FOR_MINTING, NFTStatusChoices.MINTING_FAILED]
    ).delete()
    LOGGER.info("Successfully deleted CommentNFT for comment [%s] those are failed or waiting for minting", instance.id)


@post_save(PostReaction)
async def post_reaction_added_or_updated(
    sender: "Type[PostReaction]", instance: PostReaction, created: bool, using_db: BaseDBAsyncClient | None,
    update_fields: list[str]
) -> None:
    # TODO: Need to send post to analysis service by Redis publish service
    if created:
        LOGGER.info("Sending post reaction added event to redis subscribers.")
        await post_reaction_created_event(await PostReaction_Pydantic.from_tortoise_orm(instance))
        LOGGER.info("Successfully sent post reaction added event to redis subscribers.")


@post_delete(PostReaction)
async def post_reaction_deleted(
    sender: "Type[PostReaction]", instance: PostReaction, using_db: BaseDBAsyncClient | None
) -> None:
    # TODO: Need to send post to analysis service by Redis publish service
    LOGGER.info("Sending post reaction deleted event to redis subscribers.")
    await post_reaction_deleted_event(await PostReaction_Pydantic.from_tortoise_orm(instance))
    LOGGER.info("Successfully sent post reaction deleted event to redis subscribers.")


async def generate_comment_nft(comment: Comment) -> None:
    LOGGER.info("Generating Comment NFT for comment [%s]", comment.id)
    comment_nft = await CommentNFT.exists(comment_id=comment.id, status=NFTStatusChoices.READY_FOR_MINTING)
    if comment_nft:
        await CommentNFT.get(comment_id=comment.id, status=NFTStatusChoices.READY_FOR_MINTING).update(
            comment=comment, description=f"Comment created by {comment.created_by} at {comment.created_at}",
            data=generate_nft_data_from_comment(comment), created_by=comment.created_by,
            updated_by=comment.updated_by
        )
    else:
        await CommentNFT.create(
            comment=comment, description=f"Comment created by {comment.created_by} at {comment.created_at}",
            data=generate_nft_data_from_comment(comment), created_by=comment.created_by
        )
    LOGGER.info("Successfully, generated Comment NFT for comment [%s]", comment.id)


def generate_nft_data_from_comment(comment: Comment) -> dict:
    nft_data = {
        "name": comment.id,
        "description": f"Comment created by {comment.created_by}",
        "image": None,
        "metadata": {
            "id": comment.id,
            "content": comment.content,
            "created_by": comment.created_by,
            "created_at": comment.created_at,
            "updated_by": comment.updated_by,
            "updated_at": comment.updated_at
        }
    }
    return nft_data
