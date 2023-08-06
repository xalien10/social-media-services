from tortoise import fields
from tortoise.models import Model

from apps.core.models import AbstractUUIDBaseModel
from apps.engagements import (
    StatusChoices,
    NotificationStatusChoices,
    NotificationTypes,
)


class UserEngagement(AbstractUUIDBaseModel):
    user_id = fields.UUIDField(unique=True)
    total_owned_posts = fields.IntField(default=0)
    total_post_views = fields.IntField(default=0)
    total_post_reactions = fields.IntField(default=0)
    total_post_comments = fields.IntField(default=0)
    engagement_score = fields.FloatField(default=0)
    status = fields.CharEnumField(StatusChoices, default=StatusChoices.ISOLATED)
    summary = fields.JSONField()

    class Meta:
        table = "user_engagement"
        ordering = ["-created_at"]


class Notification(Model):
    for_user_id = fields.UUIDField()
    type = fields.CharEnumField(NotificationTypes)
    message = fields.TextField()
    status = fields.CharEnumField(NotificationStatusChoices, default=NotificationStatusChoices.GENERATED)
    created_at = fields.DatetimeField(auto_now_add=True, use_tz=False, null=True)
    updated_at = fields.DatetimeField(auto_now=True, use_tz=False, null=True)

    class Meta:
        table = "notification"
        ordering = ["-created_at"]
