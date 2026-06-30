import json

import redis.asyncio as redis
from arq.connections import RedisSettings, create_pool

from app.core.config import settings

if not settings.REDIS_URL:
    raise RuntimeError("REDIS_URL is not set. Check your .env file.")

REDIS_URL: str = settings.REDIS_URL

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

arq_redis_settings = RedisSettings.from_dsn(REDIS_URL)


async def get_arq_pool():
    return await create_pool(arq_redis_settings)


async def cache_get(key: str):
    value = await redis_client.get(key)
    if value:
        return json.loads(value)
    return None


async def cache_set(key: str, value, ttl: int = 60):
    await redis_client.set(key, json.dumps(value), ex=ttl)


async def cache_delete_pattern(pattern: str):
    async for key in redis_client.scan_iter(match=pattern):
        await redis_client.delete(key)
