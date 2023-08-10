from tortoise import fields

from apps.core.models import AbstractUUIDBaseModel
from apps.moderations import ContentTypes, StatusChoices, ModerationReasons


class Moderation(AbstractUUIDBaseModel):
    type = fields.CharEnumField(ContentTypes)
    content_id = fields.UUIDField()
    raw_content = fields.JSONField(null=True)
    status = fields.CharEnumField(StatusChoices, default=StatusChoices.DELETE_REQUESTED)
    reason = fields.CharEnumField(ModerationReasons, default=ModerationReasons.RULES_VIOLATION)

    class Meta:
        table = "moderation"
        ordering = ["-created_at"]
