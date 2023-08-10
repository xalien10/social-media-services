from apps.core.enums import TextChoices


class EventProduerKeys(TextChoices):
    POST_DELETE_REQUESTED = "post_delete_requested"
    MODERATION_POST_COMMENT_DELETE_REQUESTED = "moderation_post_comment_delete_requested"


class EventConsumerKeys(TextChoices):
    POST_CREATED = "post_created"
    POST_UPDATED = "post_updated"
    POST_COMMENT_CREATED = "post_comment_created"
    POST_COMMENT_UPDATED = "post_comment_updated"
    MODERATION_POST_DELETE_REQUEST_COMPLETED = "moderation_post_delete_request_completed"
    MODERATION_POST_COMMENT_DELETE_REQUEST_COMPLETED = "moderation_post_comment_delete_request_completed"


EVENT_CONSUMER_GROUP = "moderation_group"
