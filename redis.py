import aioredis
import config
from datetime import timedelta


class Redis:

    def __init__(self) -> None:
        self.session = aioredis.Redis(
            host=config.REDIS_CONNECT["host"],
            port=config.REDIS_CONNECT["port"],
            max_connections=config.REDIS_CONNECT["max_connections"]
        )

    async def set_key(self, key: str, value: str, expire: int | timedelta = None) -> aioredis.Redis:
        return await self.session.set(key, value, expire)

    async def get_key(self, key: str) -> aioredis.Redis:
        return await self.session.get(key)

    async def remove_key(self, key: str) -> aioredis.Redis:
        return await self.session.delete(key)
