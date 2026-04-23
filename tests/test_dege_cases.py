USER_CREATE_PATH = "/auth/register"


def create_user(client, username="alice", email="alice@example.com"):
    return client.post(USER_CREATE_PATH, json={
        "username": username,
        "email": email,
        "password": "123456"
    })


def test_duplicate_user(client):
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "123456"
    }

    first_response = client.post(USER_CREATE_PATH, json=payload)
    second_response = client.post(USER_CREATE_PATH, json=payload)

    assert first_response.status_code in (200, 201)
    assert second_response.status_code in (400, 409)


def test_invalid_note_input(client):
    create_user(client)

    response = client.post("/notes/", json={
        "title": "",
        "content": "hello world"
    })

    assert response.status_code in (400, 422)


def test_note_not_found(client):
    response = client.get("/notes/999")
    assert response.status_code == 404


def test_update_not_found(client):
    response = client.patch("/notes/9999", json={
        "title": "new title",
        "content": "new content"
    })

    assert response.status_code == 404


def test_unauthorized_access_to_notes(unauthorized_client):
    response = unauthorized_client.get("/notes/")
    assert response.status_code in (401, 403)


def test_login_user_not_found(client):
    response = client.post("/auth/login", data={
        "username": "notexistqwerty",
        "password": "123456"
    })

    assert response.status_code == 404


def test_login_wrong_password(client):
    create_user(client, username="wrongpass_user", email="wrongpass@example.com")

    response = client.post("/auth/login", data={
        "username": "wrongpass_user",
        "password": "wrongpassword"
    })

    assert response.status_code == 400

