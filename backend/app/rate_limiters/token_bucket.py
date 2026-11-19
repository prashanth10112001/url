from dataclasses import dataclass
import time

@dataclass
class Bucket:
    tokens: float
    last_refill : float


class TokenBucket:
    def __init__(self, capacity: int = 100, refill_rate : int = 10):
        self.capacity = capacity
        self.refill_rate = refill_rate

        self.buckets : dict[str, Bucket] = {}

    def allow_request(self, ip_address : str) -> bool:

        current_time = time.time()

        bucket  = self.buckets.get(ip_address)

        if bucket is None:
            bucket = Bucket(
                tokens=self.capacity - 1,
                last_refill=current_time
            )

            self.buckets[ip_address] = bucket

            return True

        self._refill(bucket, current_time)

        if bucket.tokens < 1:
            return False

        bucket.tokens -= 1

        return True

    def _refill(self, bucket : Bucket, current_time : float) -> None:

        elapsed_time = current_time - bucket.last_refill

        tokens_to_add = elapsed_time * self.refill_rate

        bucket.tokens = min(
            self.capacity,
            bucket.tokens + tokens_to_add
        )

        bucket.last_refill = current_time




token_bucket = TokenBucket(
    capacity=100,
    refill_rate=10
)

def get_rate_limiter():
    return token_bucket