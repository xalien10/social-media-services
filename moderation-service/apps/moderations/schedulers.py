import datetime as dt

from apps.moderations.events.consumers import (
    consume_comment_created,
    consume_comment_updated,
    consume_comment_deleted,
    consume_post_created,
    consume_post_updated,
    consume_post_request_delete_completed,
)


async def init_consumer_schedulers(schedule) -> None:

    schedule.minutely(dt.time(minute=1), consume_comment_created)
    schedule.minutely(dt.time(minute=1), consume_comment_updated)
    schedule.minutely(dt.time(minute=1), consume_comment_deleted)
    schedule.minutely(dt.time(minute=1), consume_post_created)
    schedule.minutely(dt.time(minute=1), consume_post_updated)
    schedule.minutely(dt.time(minute=1), consume_post_request_delete_completed)
