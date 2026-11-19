import json

from app.core.cache import redis_client




def register_user(
    client,
    username="john",
    email="john@example.com"
):
    response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "secret123"
        }
    )

    return response


def auth_headers(
    client,
    username="john"
):
    response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": "secret123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

def test_cache_created_after_first_redirect(client):

    response = client.post(
        "/shorten",
        json={
            "long_url": "https://google.com"
        }
    )

    code = response.json()["short_code"]

    cache_key = f"url:{code}"

    assert redis_client.get(cache_key) is None

    client.get(
        f"/{code}",
        follow_redirects=False
    )

    assert redis_client.get(cache_key) is not None




def test_cache_contains_correct_url(client):

    response = client.post(
        "/shorten",
        json={
            "long_url": "https://google.com"
        }
    )

    code = response.json()["short_code"]

    client.get(
        f"/{code}",
        follow_redirects=False
    )

    cached_data = redis_client.get(
        f"url:{code}"
    )

    cached_data = json.loads(cached_data)

    assert cached_data["long_url"] == "https://google.com/"


def test_delete_url_clears_cache(client):

    register_user(client)

    headers = auth_headers(client)

    create_response = client.post(
        "/shorten",
        json={
            "long_url": "https://google.com"
        },
        headers=headers
    )

    code = create_response.json()["short_code"]

    client.get(
        f"/{code}",
        follow_redirects=False
    )

    assert redis_client.get(
        f"url:{code}"
    ) is not None

    client.delete(
        f"/api/urls/{code}",
        headers=headers
    )

    assert redis_client.get(
        f"url:{code}"
    ) is None


from datetime import datetime, timedelta, timezone


def test_update_expiration_clears_cache(client):

    register_user(client)

    headers = auth_headers(client)

    create_response = client.post(
        "/shorten",
        json={
            "long_url": "https://google.com"
        },
        headers=headers
    )

    code = create_response.json()["short_code"]

    client.get(
        f"/{code}",
        follow_redirects=False
    )

    assert redis_client.get(
        f"url:{code}"
    ) is not None

    client.patch(
        f"/api/urls/{code}/expiration",
        json={
            "expires_at": (
                datetime.now(timezone.utc)
                + timedelta(days=1)
            ).isoformat()
        },
        headers=headers
    )

    assert redis_client.get(
        f"url:{code}"
    ) is None