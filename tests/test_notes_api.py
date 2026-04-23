USER_CREATE_PATH = "/auth/register"


def create_note_user(client):
    return client.post(USER_CREATE_PATH, json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "123456"
    })


def test_create_note(client):
    create_note_user(client)

    response = client.post("/notes/", json={
        "title": "test note",
        "content": "hello world"
    })

    assert response.status_code in (200, 201)
    data = response.json()
    assert data["title"] == "test note"
    assert data["content"] == "hello world"


def test_get_notes(client):
    create_note_user(client)

    create_res = client.post("/notes/", json={
        "title": "note for test_get_notes",
        "content": "content for test_content"
    })
    assert create_res.status_code in (200, 201)

    response = client.get("/notes/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_update_note(client):
    create_note_user(client)

    create_res = client.post("/notes/", json={
        "title": "old title",
        "content": "old content"
    })

    assert create_res.status_code in (200, 201)
    note_id = create_res.json()["id"]

    response = client.patch(f"/notes/{note_id}", json={
        "title": "new title",
        "content": "new content"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "new title"
    assert data["content"] == "new content"


def test_delete_note(client):
    create_note_user(client)

    create_res = client.post("/notes/", json={
        "title": "title to delete",
        "content": "content to delete"
    })

    assert create_res.status_code in (200, 201)
    note_id = create_res.json()["id"]

    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 204