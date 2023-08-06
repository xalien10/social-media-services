from enum import Enum


class EventProduerKeys(str, Enum):
    POST_CREATED = "post_created"
    POST_UPDATED = "post_updated"
    POST_DELETED = "post_deleted"
    MODERATION_POST_DELETE_REQUEST_COMPLETED = "moderation_post_delete_request_completed"


class EventConsumerKeys(str, Enum):
    USER_REGISTERED = "user_registered"
    POST_COMMENT_CREATED = "post_comment_created"
    POST_COMMENT_DELETED = "post_comment_deleted"
    POST_REACTION_CREATED = "post_reaction_created"
    POST_REACTION_DELETED = "post_reaction_deleted"
    POST_DELETE_REQUESTED = "post_delete_requested"
    POST_VIEWED = "post_viewed"


EVENT_CONSUMER_GROUP = "post_group"
