import json
from typing import Any

import redis.asyncio as redis

from app.core.config import settings

_redis: redis.Redis | None = None


async def get_redis() -> redis.Redis | None:
    global _redis
    if _redis is None:
        try:
            _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
            await _redis.ping()
        except Exception:
            _redis = None
    return _redis


async def cache_get(key: str) -> Any | None:
    r = await get_redis()
    if r is None:
        return None
    data = await r.get(key)
    if data:
        return json.loads(data)
    return None


async def cache_set(key: str, value: Any, ttl: int = 3600) -> None:
    r = await get_redis()
    if r is None:
        return
    await r.setex(key, ttl, json.dumps(value, ensure_ascii=False, default=str))


def make_cache_key(*parts: str) -> str:
    return ":".join(str(p) for p in parts)
