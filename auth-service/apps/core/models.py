import json

from redis_om import HashModel
from tortoise import fields
from tortoise.models import Model

from apps.core.redis import get_redis_client


redis_client = get_redis_client()


class AbstractUUIDBaseModel(Model):
    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, use_tz=False, null=True)
    created_by = fields.UUIDField(null=True)
    updated_at = fields.DatetimeField(auto_now=True, use_tz=False, null=True)
    updated_by = fields.UUIDField(null=True)

    class Meta:
        abstract = True


class UserDetailInfo(HashModel):
    email = str
    first_name: str = None
    last_name: str = None
    connections: str = None
    is_verified: int = 0
    date_joined: str = None
    rating: float = 0.0
    status: str = None
    interests: str = None
    total_connections: int = 0

    class Meta:
        orm_mode = True
        database = redis_client
        arbitrary_types_allowed = True
        extra = "allow"

    def get_user_connections(self) -> list[str]:
        return json.loads(self.connections)

    def get_user_interests(self) -> list[str]:
        return json.loads(self.interests)
