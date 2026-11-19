import json
import time

from redis import Redis, RedisError
from app.core.cache import redis_client
from app.core.config import RATE_LIMIT_CAPACITY, RATE_LIMIT_REFILL_RATE
from app.logging.logger import get_logger

logger = get_logger(__name__)

TOKEN_BUCKET_LUA = """
local key = KEYS[1]

local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local current_time = tonumber(ARGV[3])

local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')

local tokens = tonumber(bucket[1])
local last_refill = tonumber(bucket[2])

if not tokens or not last_refill then
    tokens = capacity
    last_refill = current_time
end

local elapsed = current_time - last_refill
local tokens_to_add = elapsed * refill_rate

tokens = math.min(
    capacity,
    tokens + tokens_to_add
)

if tokens < 1 then

    redis.call(
        'HMSET',
        key,
        'tokens',
        tokens,
        'last_refill',
        current_time
    )

    redis.call('EXPIRE', key, 3600)

    return 0
end

tokens = tokens - 1

redis.call(
    'HMSET',
    key,
    'tokens',
    tokens,
    'last_refill',
    current_time
)

redis.call('EXPIRE', key, 3600)

return 1
"""

class RedisTokenBucket:

    def __init__(
            self,
            redis_client:Redis,
            capacity : int = RATE_LIMIT_CAPACITY,
            refill_rate : int = RATE_LIMIT_REFILL_RATE
            ):
        self.redis = redis_client
        self.capacity = capacity
        self.refill_rate = refill_rate

    # def allow_request(self,ip_address:str) -> bool:

    #     current_time = time.time()

    #     bucket = self._get_bucket(ip_address)

    #     if bucket is None:
    #         bucket = {
    #             "tokens" : self.capacity ,
    #             "last_refill" : current_time
    #         }

    #     elapsed_time = (
    #         current_time - bucket["last_refill"]
    #     )

    #     tokens_to_add = elapsed_time * self.refill_rate

    #     bucket["tokens"] = min(self.capacity, bucket["tokens"] + tokens_to_add)

    #     bucket["last_refill"] = current_time

    #     if bucket["tokens"] < 1:
    #         self._save_bucket(
    #             ip_address,
    #             bucket
    #         )
    #         return False

    #     bucket["tokens"] -= 1

    #     self._save_bucket(
    #         ip_address,
    #         bucket
    #     )

    #     return True

    def allow_request(self, ip_address:str) -> bool:

        try:
            key = f"rate_limit:{ip_address}"
            
            result = self.redis.eval(
                TOKEN_BUCKET_LUA,
                1,
                key,
                self.capacity,
                self.refill_rate,
                time.time()
            )

            if not result:
                logger.warning(
                    "RATE_LIMIT_EXCEEDED | ip=%s",
                    ip_address
                )
    
            return bool(result)
        except RedisError:
            logger.exception(
                "Redis rate limiter failed for IP %s",
                ip_address
            )
            # Fail Open
            return True

    # def _bucket_key(
    #         self,
    #         ip_address:str
    # ) -> str:

    #     return f"rate_limit:{ip_address}"

    # def _get_bucket(
    #         self,
    #         ip_address:str
    # ) -> dict | None :

    #     key = self._bucket_key(ip_address)

    #     data = self.redis.get(key)

    #     if not data:
    #         return None

    #     return json.loads(data)

    # def _save_bucket(
    #         self,
    #         ip_address:str,
    #         bucket:dict
    # ) -> None:

    #     key = self._bucket_key(ip_address)

    #     self.redis.set(
    #         name=key,
    #         value=json.dumps(bucket),
    #         ex=3600
    #     )





def get_rate_limiter():
    return RedisTokenBucket(
    redis_client=redis_client,
    capacity=RATE_LIMIT_CAPACITY,
    refill_rate=RATE_LIMIT_REFILL_RATE
)

        