from tortoise import fields

from apps.core.models import AbstractUUIDBaseModel
from apps.interactions import ReactionChoices, NFTStatusChoices


class Comment(AbstractUUIDBaseModel):
    post_id = fields.UUIDField()
    content = fields.TextField()

    class Meta:
        table = "comment"
        ordering = ["-created_at"]


class PostReaction(AbstractUUIDBaseModel):
    post_id = fields.UUIDField()
    type = fields.CharEnumField(ReactionChoices, default=ReactionChoices.LIKE)

    class Meta:
        table = "reaction"
        unique_together = ("post_id", "created_by")
        ordering = ["-created_at"]


class CommentNFT(AbstractUUIDBaseModel):
    comment = fields.ForeignKeyField("models.Comment", on_delete=fields.CASCADE, related_name="nfts")
    description = fields.TextField()
    data = fields.JSONField()
    token_uri = fields.CharField(max_length=150, null=True)
    status = fields.CharEnumField(NFTStatusChoices, default=NFTStatusChoices.READY_FOR_MINTING)

    class Meta:
        table = "comment_nft"
        ordering = ["-created_at"]
