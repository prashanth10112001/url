def register_user(client, username="john"):
    client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "secret123"
        }
    )


def login_user(client, username="john"):
    response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": "secret123"
        }
    )

    return response.json()["access_token"]


def auth_headers(client, username="john"):
    token = login_user(client, username)

    return {
        "Authorization": f"Bearer {token}"
    }


def create_url(client, headers):
    response = client.post(
        "/shorten",
        json={
            "long_url": "https://google.com"
        },
        headers=headers
    )

    return response.json()["short_code"]


def test_stats_initially_zero(client):
    register_user(client)

    headers = auth_headers(client)

    code = create_url(client, headers)

    response = client.get(
        f"/api/stats/{code}",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["total_clicks"] == 0

def test_stats_after_single_click(client):
    register_user(client)

    headers = auth_headers(client)

    code = create_url(client, headers)

    client.get(
        f"/{code}",
        follow_redirects=False
    )

    response = client.get(
        f"/api/stats/{code}",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["total_clicks"] == 1

def test_stats_after_multiple_clicks(client):
    register_user(client)

    headers = auth_headers(client)

    code = create_url(client, headers)

    for _ in range(5):
        client.get(
            f"/{code}",
            follow_redirects=False
        )

    response = client.get(
        f"/api/stats/{code}",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["total_clicks"] == 5

def test_stats_url_not_found(client):
    register_user(client)

    headers = auth_headers(client)

    response = client.get(
        "/api/stats/abc123",
        headers=headers
    )

    assert response.status_code == 404


def test_stats_requires_authentication(client):
    response = client.get(
        "/api/stats/anything"
    )

    assert response.status_code == 401


def test_non_owner_cannot_view_stats(client):

    register_user(client, "john")
    owner_headers = auth_headers(client, "john")

    code = create_url(client, owner_headers)

    register_user(client, "alice")
    alice_headers = auth_headers(client, "alice")

    response = client.get(
        f"/api/stats/{code}",
        headers=alice_headers
    )

    assert response.status_code == 403


def test_my_urls_contains_click_count(client):
    register_user(client)

    headers = auth_headers(client)

    code = create_url(client, headers)

    # Generate 3 clicks
    for _ in range(3):
        client.get(
            f"/{code}",
            follow_redirects=False
        )

    response = client.get(
        "/api/my-urls",
        headers=headers
    )

    assert response.status_code == 200

    urls = response.json()

    # Find the created URL
    url = next(
        item for item in urls
        if item["short_code"] == code
    )

    assert "total_clicks" in url
    assert url["total_clicks"] == 3