from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from tortoise.exceptions import DoesNotExist
from tortoise.queryset import Q

from apps.posts import PostCategoryChoices, StatusChoices
from apps.posts.schemas import (
    Post,
    Post_Pydantic,
    PostIn_Pydantic,
    UserSchema,
)
from apps.core.security import (
    authenticate_user,
)

router = InferringRouter(tags=["post"])


@cbv(router)
class PostViews:

    current_user: UserSchema = Depends(authenticate_user)

    @router.get("/posts/category-choices", status_code=status.HTTP_200_OK)
    async def get_available_interests_choices(self):
        return JSONResponse(status_code=status.HTTP_200_OK, content=PostCategoryChoices.values())

    @router.post("/posts", response_model=Post_Pydantic, status_code=status.HTTP_201_CREATED)
    async def create_post(self, post: PostIn_Pydantic):
        if set(post.types).difference(set(PostCategoryChoices.values())):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Should be from valid post category choices"
            )
        post_obj = await Post.create(**post.dict(exclude_unset=True), created_by=self.current_user.id)
        return await Post_Pydantic.from_tortoise_orm(post_obj)

    @router.get("/posts", response_model=List[Post_Pydantic])
    async def get_posts(self):
        filters = Q(Q(status=StatusChoices.POSTED), Q(created_by=self.current_user.id), join_type="OR")
        return await Post_Pydantic.from_queryset(Post.filter(filters))

    @router.get("/posts/{post_id}", response_model=Post_Pydantic)
    async def retrieve_post_detail(self, post_id: UUID):
        try:
            await Post.get(id=post_id)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post object not found"
            )
        return await Post_Pydantic.from_queryset_single(Post.get(id=post_id))

    @router.put("/posts/{post_id}", response_model=Post_Pydantic)
    async def update_post(self, post_id: UUID, post: PostIn_Pydantic):
        if set(post.types).difference({item.value for item in PostCategoryChoices}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Should be from valid post category choices"
            )
        try:
            await Post.get(id=post_id, created_by=self.current_user.id)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found for update"
            )
        else:
            await Post.get(id=post_id, created_by=self.current_user.id).update(
                **post.dict(exclude_unset=True), updated_by=self.current_user.id
            )
        return await Post_Pydantic.from_queryset_single(Post.get(id=post_id, created_by=self.current_user.id))

    @router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_post(self, post_id: UUID):
        try:
            post = await Post.get(created_by=self.current_user.id, id=post_id)
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found for deleteing"
            )
        return await post.delete()
