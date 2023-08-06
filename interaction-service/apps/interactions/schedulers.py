import datetime as dt

from apps.interactions.events.consumers import (
    consume_post_created,
    consume_moderation_post_comment_delete_requested,
    consume_post_deleted,
)


async def init_consumer_schedulers(schedule) -> None:

    schedule.minutely(dt.time(minute=1), consume_post_created)
    schedule.minutely(dt.time(minute=1), consume_moderation_post_comment_delete_requested)
    schedule.minutely(dt.time(minute=1), consume_post_deleted)
