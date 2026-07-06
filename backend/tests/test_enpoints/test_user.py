from fastapi.testclient import TestClient


def make_user_payload(index: int = 1) -> dict:
    return {
        "email": f"test_user_{index}@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": f"User{index}",
        "display_name": f"Test User {index}",
        "bio": "Created from the tests.",
        "avatar_url": "https://example.com/avatars/test-user.png",
    }


def create_user(client: TestClient, index: int = 1) -> dict:
    response = client.post("/api/v1/users/", json=make_user_payload(index))
    assert response.status_code == 201
    return response.json()


def test_register_user(client: TestClient):
    payload = make_user_payload()

    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == 201
    assert response.json()["email"] == payload["email"]


def test_list_users(client: TestClient):
    create_user(client, 1)
    create_user(client, 2)

    response = client.get("/api/v1/users/?skip=0&limit=100&sort=desc")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_user(client: TestClient):
    user = create_user(client, 1)

    response = client.get(f"/api/v1/users/{user['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == user["id"]


def test_get_user_public_profile(client: TestClient):
    user = create_user(client, 1)

    response = client.get(f"/api/v1/users/{user['id']}/public")

    assert response.status_code == 200
    assert response.json()["display_name"] == user["display_name"]


def test_get_user_with_posts(client: TestClient):
    user = create_user(client, 1)

    response = client.get(f"/api/v1/users/{user['id']}/posts")

    assert response.status_code == 200
    assert response.json()["id"] == user["id"]
    assert response.json()["posts"] == []


def test_get_user_with_comments(client: TestClient):
    user = create_user(client, 1)

    response = client.get(f"/api/v1/users/{user['id']}/comments")

    assert response.status_code == 200
    assert response.json()["id"] == user["id"]
    assert response.json()["comments"] == []


def test_get_user_detail(client: TestClient):
    user = create_user(client, 1)

    response = client.get(f"/api/v1/users/{user['id']}/detail")

    assert response.status_code == 200
    assert response.json()["id"] == user["id"]
    assert response.json()["posts"] == []
    assert response.json()["comments"] == []


def test_update_user(client: TestClient):
    user = create_user(client, 1)
    payload = {
        "display_name": "Updated User Name",
        "bio": "Updated from tests.",
    }

    response = client.patch(f"/api/v1/users/{user['id']}", json=payload)

    assert response.status_code == 200
    assert response.json()["display_name"] == payload["display_name"]


def test_update_user_admin(client: TestClient):
    user = create_user(client, 1)
    payload = {
        "is_active": False,
        "is_admin": True,
    }

    response = client.patch(f"/api/v1/users/{user['id']}/admin", json=payload)

    assert response.status_code == 200
    assert response.json()["is_admin"] is True
    assert response.json()["is_active"] is False


def test_delete_user(client: TestClient):
    user = create_user(client, 1)

    delete_response = client.delete(f"/api/v1/users/{user['id']}")
    get_response = client.get(f"/api/v1/users/{user['id']}")

    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == user["id"]
    assert get_response.status_code == 404
