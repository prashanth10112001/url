import json
import logging
from redis import Redis, RedisError
from app.core.cache import redis_client

logger = logging.getLogger(__name__)

class CacheRepository:

    def __init__(self, redis_client:Redis):
        self.redis = redis_client
        self.PREFIX = "url:"

    def get(self, key:str) -> dict | None :
        try:
            key = f"{self.PREFIX}{key}"

            data = self.redis.get(key)

            if not data:
                return None

            
            return json.loads(data)
        except RedisError:
            logger.exception("Redis GET Failed")
            return None

    def set(self, key:str, value:dict, ttl:int):
        try:
            if(ttl>0):
                key = f"{self.PREFIX}{key}"
                self.redis.set(
                    name=key,
                    value=json.dumps(value),
                    ex=ttl
                )
        except RedisError:
            logger.exception("REDIS SET FAILED")
            pass

    def delete(self, key:str):
        try:
            self.redis.delete(f"{self.PREFIX}{key}")
        except RedisError:
            logger.exception("Redis DELETE Failed")


def get_cache_repository():
    return CacheRepository(redis_client)