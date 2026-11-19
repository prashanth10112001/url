def register_user(client):
    client.post(
        "/auth/register",
        json={
            "username": "john",
            "email": "john@example.com",
            "password": "secret123"
        }
    )


def login_user(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "john",
            "password": "secret123"
        }
    )

    return response.json()["access_token"]


def auth_headers(client):
    token = login_user(client)

    return {
        "Authorization": f"Bearer {token}"
    }

def test_create_short_url_anonymous(client):
    response = client.post(
        "/shorten",
        json={
            "long_url" : "https://www.google.com"
        }
    )

    assert response.status_code == 201

    body = response.json()

    assert body["message"] == "Success"
    assert "short_code" in body
    assert "short_url" in body


def test_create_short_url_authenticated_user(client):
    register_user(client)

    response = client.post(
        "/shorten",
        json={
            "long_url" : "https://www.github.com"
        },
        headers=auth_headers(client)
    )

    assert response.status_code == 201

    body = response.json()

    assert "short_code" in body
    assert "short_url" in body

def test_create_multiple_urls_returns_different_codes(client):
    response1 = client.post(
        "/shorten",
        json={
            "long_url" : "https://www.google.com"
        }
    )

    response2 = client.post(
            "/shorten",
            json={
                "long_url" : "https://www.google.com"
            }
        )

    code1 = response1.json()["short_code"]
    code2 = response2.json()["short_code"]

    assert code1 != code2


def test_create_short_url_invalid_url(client):
    response = client.post(
        "/shorten",
        json={
            "long_url": "not-a-valid-url"
        }
    )

    assert response.status_code == 422


def test_get_my_urls_requires_authentication(client):
    response = client.get("/api/my-urls")

    assert response.status_code == 401


def test_get_my_urls_returns_user_urls(client):
    register_user(client)

    headers = auth_headers(client)

    client.post(
        "/shorten",
        json={
            "long_url": "https://google.com"
        },
        headers=headers
    )

    client.post(
        "/shorten",
        json={
            "long_url": "https://github.com"
        },
        headers=headers
    )

    response = client.get(
        "/api/my-urls",
        headers=headers
    )

    assert response.status_code == 200

    urls = response.json()

    assert len(urls) == 2

    assert urls[0]["short_code"]
    assert urls[0]["short_url"]
    assert urls[0]["long_url"]
