import datetime as dt

from apps.posts.events.consumers import (
    consume_user_registered,
    consume_comment_created,
    consume_comment_deleted,
    consume_reaction_created,
    consume_reaction_deleted,
    consume_moderation_post_deleted,
    consume_post_viewed_event,
)


async def init_consumer_schedulers(schedule) -> None:

    schedule.minutely(dt.time(minute=1), consume_user_registered)
    schedule.minutely(dt.time(minute=1), consume_comment_created)
    schedule.minutely(dt.time(minute=1), consume_comment_deleted)
    schedule.minutely(dt.time(minute=1), consume_reaction_created)
    schedule.minutely(dt.time(minute=1), consume_reaction_deleted)
    schedule.minutely(dt.time(minute=1), consume_moderation_post_deleted)
    schedule.minutely(dt.time(minute=1), consume_post_viewed_event)
