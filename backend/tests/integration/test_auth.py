def register_user(
        client,
        username="john",
        email="john@example.com",
        password="secret123"
        ):
    return client.post(
        "auth/register",
        json={
            "username":username,
            "email":email,
            "password":password
        }
    )


def login_user(
        client,
        username="john",
        password="secret123"
        ):
    return client.post(
        "auth/login",
        json={
            "username":username,
            "password":password
        }
    )

def get_auth_headers(client):
    login_response = login_user(client)

    token = login_response.json()["access_token"]

    return {
        "Authorization" : f"Bearer {token}"
    }

def test_register_user_success(client):
    response = register_user(client)

    assert response.status_code == 201

    body = response.json()

    assert body["message"] == "User registered successfully"
    assert "user_id" in body


def test_register_duplicate_username(client):
    register_user(client)

    response = register_user(
        client,
        username="john",
        email="another@example.com"
    )

    assert response.status_code == 409

    assert response.json()["detail"] == "Username already exists"


def test_register_duplicate_email(client):
    register_user(client)

    response = register_user(
        client,
        username="anotheruser",
        email="john@example.com"
    )

    assert response.status_code == 409

    assert response.json()["detail"] == "Email already exists"

def test_register_invalid_email(client):
    

    response = client.post(
        "auth/register",
        json={
        "username":"john",
        "email":"invalid-email",
        "password":"secret123"
        }
    )

    assert response.status_code == 422

def test_login_success(client):
    register_user(client)

    response = login_user(client)

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "Bearer"

def test_login_invalid_username(client):
    response = login_user(client,username="unknown",password="secret123")

    assert response.status_code == 401

    assert response.json()["detail"] == "Invalid username or password"

def test_login_invalid_password(client):
    register_user(client)

    response = login_user(client,username="john",password="wrong-password")

    assert response.status_code == 401

    assert response.json()["detail"] == "Invalid username or password"

def test_get_me_success(client):
    register_user(client)

    response = client.get(
        "auth/me",
        headers=get_auth_headers(client)
    )

    assert response.status_code == 200

    body = response.json()

    assert body["username"] == "john"
    assert body["email"] == "john@example.com"
    assert "id" in body

def test_get_me_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401

def test_get_me_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization" : "Bearer invalid-token"
        }
    )

    assert response.status_code == 401


