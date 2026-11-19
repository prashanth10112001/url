from prometheus_client import Counter

cache_hits_total = Counter(
    "cache_hits_total",
    "Total number of cache hits"
)

cache_misses_total = Counter(
    "cache_misses_total",
    "Total number of cache misses"
)




rate_limit_exceeded_total = Counter(
    "rate_limit_exceeded_total",
    "Total number of rate-limited requests"
)



urls_created_total = Counter(
    "urls_created_total",
    "Total number of short URLs created"
)

redirects_total = Counter(
    "redirects_total",
    "Total successful redirects"
)

expired_urls_total = Counter(
    "expired_urls_total",
    "Total expired URL accesses"
)