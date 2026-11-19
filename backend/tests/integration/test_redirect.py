from datetime import datetime, timedelta, timezone


def create_url(client, long_url="https://google.com"):
    response = client.post(
        "/shorten",
        json={
            "long_url": long_url
        }
    )

    return response.json()["short_code"]


def test_redirect_existing_url(client):
    code = create_url(client)

    response = client.get(
        f"/{code}",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert response.headers["location"] == "https://google.com/"


def test_redirect_different_url(client):
    code = create_url(
        client,
        "https://github.com"
    )

    response = client.get(
        f"/{code}",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert response.headers["location"] == "https://github.com/"


def test_redirect_unknown_short_code(client):
    response = client.get(
        "/abc123",
        follow_redirects=False
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "URL not found"


def test_redirect_invalid_short_code_format(client):
    response = client.get(
        "/$$$",
        follow_redirects=False
    )

    assert response.status_code == 400