import logging

from redis_om.model.model import NotFoundError

from apps.core.models import UserDetailInfo
from apps.posts.models import Post

LOGGER = logging.getLogger(__name__)


async def set_and_calculate_post_popularity_and_rating(post) -> None:

    try:
        total_user_connections = UserDetailInfo.get(pk=post.created_by).total_connections
    except NotFoundError:
        total_user_connections = 0

    LOGGER.info("Calculating post popularity for post [%s].", post.id)
    view_count = post.total_views
    try:
        popularity = view_count / total_user_connections
    except ZeroDivisionError:
        # When view is greater than total user connections then obviously,
        # post is popular, so the post popularity is 100%
        popularity = 100.00

    LOGGER.info("Calculating post score for post [%s].", post.id)
    # TODO: Need to fix score based on positive reactions
    try:
        post_score = (post.total_reactions + post.total_comments)/post.total_views
    except ZeroDivisionError:
        post_score = 0.0

    LOGGER.info("Successfully calculated post score and popularity for post [%s].", post.id)

    LOGGER.info("Updating post score and popularity for post [%s].", post.id)
    await Post.get(id=post.id).update(
        total_views=view_count, popularity=min(100.00, popularity),
        score=min(100, float(format(post_score, ".2f")))
    )
    LOGGER.info("Successfully updated post score and popularity for post [%s].", post.id)
