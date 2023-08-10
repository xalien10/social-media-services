import re

from passlib.hash import bcrypt
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField
from tortoise.validators import RegexValidator

from apps.core.models import AbstractUUIDBaseModel
from apps.users import StatusChoices, InterestChoices


class User(AbstractUUIDBaseModel):
    email = fields.CharField(
        max_length=50, unique=True,
        validators=[RegexValidator("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", re.I)]
    )
    first_name = fields.CharField(max_length=100, null=True)
    last_name = fields.CharField(max_length=100, null=True)
    connections = fields.ManyToManyField("models.User", related_names="connections")
    password = fields.CharField(max_length=128, null=False)
    is_verified = fields.BooleanField(default=False, null=True)
    date_joined = fields.DatetimeField(auto_now_add=True, use_tz=False, null=True)
    rating = fields.FloatField(default=0.0, null=True)
    status = fields.CharEnumField(StatusChoices, default=StatusChoices.INACTIVE)
    interests = ArrayField(element_type="text", choices=InterestChoices)

    class Meta:
        table = "user"
        ordering = ["-date_joined"]

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password)


class UserToken(AbstractUUIDBaseModel):
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE, related_name="user_tokens")

    class Meta:
        table = "user_token"
        ordering = ["-created_at"]
