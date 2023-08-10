from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField

from apps.core.models import AbstractUUIDBaseModel
from apps.posts import StatusChoices, PostCategoryChoices, NFTStatusChoices


class Post(AbstractUUIDBaseModel):
    title = fields.CharField(max_length=100, null=True)
    content = fields.TextField()
    types = ArrayField(element_type="text", choices=PostCategoryChoices)
    status = fields.CharEnumField(StatusChoices, default=StatusChoices.DRAFT)
    total_views = fields.IntField(default=0, null=True)
    total_comments = fields.IntField(default=0, null=True)
    total_reactions = fields.IntField(default=0, null=True)
    score = fields.FloatField(default=0.0, null=True)
    popularity = fields.FloatField(default=0.0, null=True)

    class Meta:
        table = "post"
        ordering = ["-created_at"]


# Model for generating and saving ERC721 or ERC1155 NFT for blockchain
class PostNFT(AbstractUUIDBaseModel):
    post = fields.ForeignKeyField("models.Post", on_delete=fields.CASCADE, related_name="nfts")
    title = fields.CharField(max_length=100, null=True)
    description = fields.TextField()
    data = fields.JSONField()
    token_uri = fields.CharField(max_length=150, null=True)
    status = fields.CharEnumField(NFTStatusChoices, default=NFTStatusChoices.READY_FOR_MINTING)

    class Meta:
        table = "post_nft"
        ordering = ["-created_at"]
