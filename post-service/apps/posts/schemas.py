from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from apps.posts.models import Post


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


Post_Pydantic = pydantic_model_creator(Post, name="Post")
PostIn_Pydantic = pydantic_model_creator(
    Post, name="PostIn", exclude=(
        "created_at", "created_by", "updated_at", "updated_by",
        "total_comments", "total_reactions", "total_views",
        "score", "popularity"
    ),
    exclude_readonly=True
)
