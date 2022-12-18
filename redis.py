import aioredis
import config
import json
import logging as log
from datetime import timedelta


class Redis:

    def __init__(self) -> None:
        self.session = aioredis.Redis(
            host=config.REDIS_CONNECT["host"],
            port=config.REDIS_CONNECT["port"],
            max_connections=config.REDIS_CONNECT["max_connections"]
        )

    async def set_key(self, key: str, value: dict, expire: int | timedelta = None) -> aioredis.Redis:
        return await self.session.set(key, json.dumps(value), expire)

    async def get_key(self, key: str) -> aioredis.Redis:
        return await self.session.get(key)

    async def remove_key(self, key: str) -> aioredis.Redis:
        return await self.session.delete(key)

    async def get(self, key: str, skey: str = None) -> any or None:
        try:
            r = await self.get_key(key)
            redis_data = json.loads(bytes(r).decode())
            return redis_data[skey] if skey else redis_data

        except Exception as e:
            log.debug(e)

        finally:
            return None
