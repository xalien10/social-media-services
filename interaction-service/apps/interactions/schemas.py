from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from apps.interactions.models import Comment, PostReaction


class UserSchema(BaseModel):
    id: str
    email: str
    first_name: str = None
    last_name: str = None
    status: str
    is_verified: bool
    created_at: str
    updated_at: str
    date_joined: str
    total_connections: int


Comment_Pydantic = pydantic_model_creator(Comment, name="Comment")
CommentIn_Pydantic = pydantic_model_creator(
    Comment, name="CommentIn", exclude=("post_id", "created_at", "created_by", "updated_at", "updated_by"),
    exclude_readonly=True
)

PostReaction_Pydantic = pydantic_model_creator(PostReaction, name="PostReaction")
PostReactionIn_Pydantic = pydantic_model_creator(
    PostReaction, name="PostReactionIn", exclude=("post_id", "created_at", "created_by", "updated_at", "updated_by"),
    exclude_readonly=True
)
