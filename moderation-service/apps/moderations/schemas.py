from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from apps.moderations.models import Moderation


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


Moderation_Pydantic = pydantic_model_creator(Moderation, name="Moderation")
ModerationIn_Pydantic = pydantic_model_creator(
    Moderation, name="ModerationIn", exclude=(
        "created_at", "created_by", "updated_at", "updated_by"
    ),
    exclude_readonly=True
)
