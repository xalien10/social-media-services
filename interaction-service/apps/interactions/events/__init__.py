from apps.core.enums import TextChoices


class EventProduerKeys(TextChoices):
    POST_COMMENT_CREATED = "post_comment_created"
    POST_COMMENT_UPDATED = "post_comment_updated"
    POST_COMMENT_DELETED = "post_comment_deleted"
    POST_REACTION_CREATED = "post_reaction_created"
    POST_REACTION_DELETED = "post_reaction_deleted"
    POST_VIEWED = "post_viewed"
    MODERATION_POST_COMMENT_DELETE_REQUEST_COMPLETED = "moderation_post_comment_delete_request_completed"


class EventConsumerKeys(TextChoices):
    POST_CREATED = "post_created"
    POST_DELETED = "post_deleted"
    MODERATION_POST_COMMENT_DELETE_REQUESTED = "moderation_post_comment_delete_requested"


EVENT_CONSUMER_GROUP = "interaction_group"
