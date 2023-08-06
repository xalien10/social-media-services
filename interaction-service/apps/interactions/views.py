from typing import Annotated, List
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from tortoise.exceptions import DoesNotExist, IntegrityError

from apps.core.security import (
    authenticate_user,
    get_post_detail,
)
from apps.interactions.schemas import (
    Comment,
    CommentIn_Pydantic,
    Comment_Pydantic,
    PostReaction,
    PostReactionIn_Pydantic,
    PostReaction_Pydantic,
    UserSchema,
)
from apps.interactions.events.producers import generate_post_view_event

router = InferringRouter()


@cbv(router)
class CommentViews:

    current_user: UserSchema = Depends(authenticate_user)

    @router.post(
            "/{post_id}/comments", tags=["comment"], response_model=Comment_Pydantic,
            status_code=status.HTTP_201_CREATED
    )
    async def create_post_comment(self, post: Annotated[dict, Depends(get_post_detail)], comment: CommentIn_Pydantic):
        comment_data = comment.dict(exclude_unset=True)
        comment_data.update({"created_by": self.current_user.id, "post_id": post.get("id")})
        return await Comment_Pydantic.from_tortoise_orm(await Comment.create(**comment_data))

    @router.get("/{post_id}/comments", tags=["comment"], response_model=List[Comment_Pydantic])
    async def get_post_comments(self, post: Annotated[dict, Depends(get_post_detail)]):
        return await Comment_Pydantic.from_queryset(Comment.filter(post_id=post.get("id")))

    @router.get("/comments/{comment_id}", tags=["comment"], response_model=Comment_Pydantic)
    async def retrieve_post_comment_detail(self, comment_id: UUID):
        try:
            return await Comment_Pydantic.from_queryset_single(Comment.get(id=comment_id))
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post comment not found"
            )

    @router.put("/comments/{comment_id}", tags=["comment"], response_model=Comment_Pydantic)
    async def update_post_comment(self, comment_id: UUID, comment: CommentIn_Pydantic):
        try:
            await Comment.get(id=comment_id, created_by=self.current_user.id)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post comment not found"
            )
        else:
            await Comment.get(id=comment_id, created_by=self.current_user.id).update(
                **comment.dict(exclude_unset=True), updated_by=self.current_user.id
            )
        return await Comment_Pydantic.from_queryset_single(Comment.get(id=comment_id, created_by=self.current_user.id))

    @router.delete("/comments/{comment_id}", tags=["comment"], status_code=status.HTTP_204_NO_CONTENT)
    async def delete_post_comment(self, comment_id: UUID):
        try:
            comment = await Comment.get(id=comment_id, created_by=self.current_user.id)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post comment not found for deletion"
            )
        return await comment.delete()

    @router.get("/{post_id}/view", tags=["post-view"], status_code=status.HTTP_200_OK)
    async def view_post(self, post: Annotated[dict, Depends(get_post_detail)]):
        post.update({"total_views": post.get("total_views") + 1})
        return await generate_post_view_event({**post, "viewed_by": self.current_user.id})


@cbv(router)
class PostReactionViews:

    current_user: UserSchema = Depends(authenticate_user)

    @router.post(
            "/{post_id}/post-reactions", tags=["reaction"], response_model=PostReaction_Pydantic,
            status_code=status.HTTP_201_CREATED
    )
    async def create_post_reaction(
        self, post: Annotated[str, Depends(get_post_detail)], reaction: PostReactionIn_Pydantic
    ):
        reaction_data = reaction.dict(exclude_unset=True)
        reaction_data.update({"created_by": self.current_user.id, "post_id": post.get("id")})
        try:
            reaction_obj = await PostReaction.create(**reaction_data)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not react duplicate on same post."
            )
        return await PostReaction_Pydantic.from_tortoise_orm(reaction_obj)

    @router.get("/{post_id}/post-reactions", tags=["reaction"], response_model=List[PostReaction_Pydantic])
    async def get_post_reactions(self, post_id: UUID):
        return await PostReaction_Pydantic.from_queryset(PostReaction.filter(post_id=post_id))

    @router.get("/post-reactions/{reaction_id}", tags=["reaction"], response_model=PostReaction_Pydantic)
    async def retrieve_post_reaction_detail(self, reaction_id: UUID):
        try:
            await PostReaction.get(id=reaction_id)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post reaction not found"
            )
        return await PostReaction_Pydantic.from_queryset_single(PostReaction.get(id=reaction_id))

    @router.put("/post-reactions/{reaction_id}", tags=["reaction"], response_model=PostReaction_Pydantic)
    async def update_post_reaction(self, reaction_id: UUID, reaction: PostReactionIn_Pydantic):
        try:
            await PostReaction.get(id=reaction_id, created_by=self.current_user.id)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post reaction not found"
            )
        else:
            await PostReaction.get(id=reaction_id, created_by=self.current_user.id).update(
                **reaction.dict(exclude_unset=True), updated_by=self.current_user.id
            )
        return await PostReaction_Pydantic.from_queryset_single(
            PostReaction.get(id=reaction_id, created_by=self.current_user.id)
        )

    @router.delete("/post-reactions/{reaction_id}", tags=["reaction"], status_code=status.HTTP_204_NO_CONTENT)
    async def delete_post_reaction(self, reaction_id: UUID):
        try:
            post = await PostReaction.get(id=reaction_id, created_by=self.current_user.id)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post reaction not found for deletion"
            )
        return await post.delete()
