def test_register(client):
    res = client.post("/auth/register", json={
        "username": "bob",
        "email": "bob@test.com",
        "password": "123456"
    })
    assert res.status_code == 201


def test_login(client):
    client.post("/auth/register", json={
        "username": "bob",
        "email": "bob@test.com",
        "password": "123456"
    })

    res = client.post("/auth/login", data={
        "username": "bob",
        "password": "123456"
    })

    assert res.status_code == 200
    assert "access_token" in res.json()