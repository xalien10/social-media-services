from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from apps.engagements.models import UserEngagement


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


UserEngagement_Pydantic = pydantic_model_creator(UserEngagement, name="UserEngagement")
