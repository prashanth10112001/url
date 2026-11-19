import time

from app.core.config import RATE_LIMIT_CAPACITY, RATE_LIMIT_REFILL_RATE
from app.rate_limiters.redit_token_bucket import RedisTokenBucket, get_rate_limiter
# from app.core.cache import redis_client


# import os

# def test_print_rate_limit_values():

#     limiter = get_rate_limiter()

#     print(limiter.capacity)
#     print(limiter.refill_rate)


#     print("ENV:", os.getenv("RATE_LIMIT_CAPACITY"))
#     print("CONST:", RATE_LIMIT_CAPACITY)


#     assert limiter.capacity == 5
#     assert limiter.refill_rate == 1

def test_requests_under_limit_succeed(client):

    

    for i in range(5):

        response = client.post(
            "/shorten",
            json={
                "long_url": f"https://example{i}.com"
            }
        )

        assert response.status_code == 201



def test_rate_limit_exceeded(client):

    for i in range(5):

        response = client.post(
            "/shorten",
            json={
                "long_url": f"https://example{i}.com"
            }
        )

        assert response.status_code == 201

    response = client.post(
        "/shorten",
        json={
            "long_url": "https://blocked.com"
        }
    )

    assert response.status_code == 429

    assert response.json()["detail"] == (
        "Rate limit exceeded. Please try again later."
    )


def test_rate_limit_counts_multiple_requests(client):

    success_count = 0

    for i in range(10):

        response = client.post(
            "/shorten",
            json={
                "long_url": f"https://example{i}.com"
            }
        )

        if response.status_code == 201:
            success_count += 1

    assert success_count == 5


def test_rate_limit_refills(client):

    for i in range(5):
        client.post(
            "/shorten",
            json={
                "long_url": f"https://example{i}.com"
            }
        )

    blocked = client.post(
        "/shorten",
        json={
            "long_url": "https://blocked.com"
        }
    )

    assert blocked.status_code == 429

    time.sleep(1.1)

    response = client.post(
        "/shorten",
        json={
            "long_url": "https://allowed-after-refill.com"
        }
    )

    assert response.status_code == 201