from apps.core.enums import TextChoices


class EventConsumerKeys(TextChoices):
    USER_REGISTERED = "user_registered"
    POST_CREATED = "post_created"
    POST_UPDATED = "post_updated"
    POST_DELETED = "post_deleted"
    POST_VIEWED = "post_viewed"
    POST_COMMENT_CREATED = "post_comment_created"
    POST_COMMENT_UPDATED = "post_comment_updated"
    POST_COMMENT_DELETED = "post_comment_deleted"
    POST_REACTION_CREATED = "post_reaction_created"
    POST_REACTION_DELETED = "post_reaction_deleted"
    POST_DELETE_REQUESTED = "post_delete_requested"
    MODERATION_POST_DELETE_REQUEST_COMPLETED = "moderation_post_delete_request_completed"
    MODERATION_POST_COMMENT_DELETE_REQUEST_COMPLETED = "moderation_post_comment_delete_request_completed"


EVENT_CONSUMER_GROUP = "engagement_group"
