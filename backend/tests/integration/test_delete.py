

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


def create_url(
    client,
    headers,
    long_url="https://google.com"
):
    response = client.post(
        "/shorten",
        json={
            "long_url": long_url
        },
        headers=headers
    )

    return response.json()["short_code"]

def test_owner_can_delete_url(client):

    register_user(client)

    headers = auth_headers(client)

    code = create_url(
        client,
        headers
    )

    response = client.delete(
        f"/api/urls/{code}",
        headers=headers
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == (
        "URL deleted successfully"
    )


def test_deleted_url_cannot_be_accessed(client):

    register_user(client)

    headers = auth_headers(client)

    code = create_url(
        client,
        headers
    )

    delete_response = client.delete(
        f"/api/urls/{code}",
        headers=headers
    )

    assert delete_response.status_code == 200

    redirect_response = client.get(
        f"/{code}",
        follow_redirects=False
    )

    assert redirect_response.status_code == 404


def test_delete_requires_authentication(client):

    response = client.delete(
        "/api/urls/123"
    )

    assert response.status_code == 401


def test_delete_non_existing_url(client):

    register_user(client)

    headers = auth_headers(client)

    response = client.delete(
        "/api/urls/abc123",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "URL not found"
    )


def test_non_owner_cannot_delete_url(client):

    register_user(
        client,
        username="john",
        email="john@example.com"
    )

    john_headers = auth_headers(
        client,
        "john"
    )

    code = create_url(
        client,
        john_headers
    )

    register_user(
        client,
        username="alice",
        email="alice@example.com"
    )

    alice_headers = auth_headers(
        client,
        "alice"
    )

    response = client.delete(
        f"/api/urls/{code}",
        headers=alice_headers
    )

    assert response.status_code == 403

    assert response.json()["detail"] == (
        "You do not have access to this URL"
    )


def test_deleted_url_removed_from_user_urls(client):

    register_user(client)

    headers = auth_headers(client)

    code = create_url(client, headers)

    before = client.get(
        "/api/my-urls",
        headers=headers
    )

    assert len(before.json()) == 1

    client.delete(
        f"/api/urls/{code}",
        headers=headers
    )

    after = client.get(
        "/api/my-urls",
        headers=headers
    )

    assert after.status_code == 200
    assert len(after.json()) == 0
