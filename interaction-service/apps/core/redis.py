from functools import lru_cache
import json

from redis_om import get_redis_connection

from apps.settings import get_settings

settings = get_settings()


@lru_cache
def get_redis_client(url=settings.REDIS_URL):
    redis_client = get_redis_connection(
        url=url,
        decode_responses=True
    )
    return redis_client


async def normalize_redis_hash_data(data: dict) -> dict:
    for key, val in data.items():
        if isinstance(val, dict) or isinstance(val, list):
            data[key] = json.dumps(val)
        elif isinstance(val, bool):
            data[key] = int(val)
        elif val is None:
            data[key] = json.dumps(val)
    return data
