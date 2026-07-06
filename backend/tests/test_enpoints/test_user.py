from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from database.models.users import User


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


def register_auth(client: TestClient, index: int = 1) -> tuple[dict, dict[str, str]]:
    response = client.post("/api/v1/auth/register", json=make_user_payload(index))
    assert response.status_code == 201
    data = response.json()
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    return data["user"], headers


def create_user(client: TestClient, index: int = 1) -> dict:
    user, _ = register_auth(client, index)
    return user


def auth_headers(client: TestClient, index: int = 1) -> dict[str, str]:
    _, headers = register_auth(client, index)
    return headers


def promote_admin(db_session: Session, user_id: int) -> None:
    db_user = db_session.get(User, user_id)
    assert db_user is not None
    db_user.is_admin = True
    db_session.commit()


def test_list_users(client: TestClient, db_session: Session):
    user1, admin_headers = register_auth(client, 1)
    register_auth(client, 2)
    promote_admin(db_session, user1["id"])

    response = client.get(
        "/api/v1/users/?skip=0&limit=100&sort=desc",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_user(client: TestClient, db_session: Session):
    user, headers = register_auth(client, 1)
    promote_admin(db_session, user["id"])

    response = client.get(f"/api/v1/users/{user['id']}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user["id"]


def test_get_user_public_profile(client: TestClient):
    user = create_user(client, 1)

    response = client.get(f"/api/v1/users/{user['id']}/public")

    assert response.status_code == 200
    assert response.json()["display_name"] == user["display_name"]


def test_get_user_with_posts(client: TestClient):
    user, headers = register_auth(client, 1)

    response = client.get(f"/api/v1/users/{user['id']}/posts", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user["id"]
    assert response.json()["posts"] == []


def test_get_user_with_posts_includes_post_fields(client: TestClient):
    from tests.test_enpoints.test_post import create_post

    user, headers = register_auth(client, 1)
    create_post(client, user["id"], 1, headers=headers)

    response = client.get(f"/api/v1/users/{user['id']}/posts", headers=headers)

    assert response.status_code == 200
    posts = response.json()["posts"]
    assert len(posts) == 1
    assert posts[0]["post_type"] == "post"
    assert posts[0]["slug"] == "post-test-1"


def test_get_user_with_comments(client: TestClient):
    user, headers = register_auth(client, 1)

    response = client.get(f"/api/v1/users/{user['id']}/comments", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user["id"]
    assert response.json()["comments"] == []


def test_get_user_detail(client: TestClient):
    user, headers = register_auth(client, 1)

    response = client.get(f"/api/v1/users/{user['id']}/detail", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == user["id"]
    assert response.json()["posts"] == []
    assert response.json()["comments"] == []


def test_update_user(client: TestClient):
    user, headers = register_auth(client, 1)
    payload = {
        "display_name": "Updated User Name",
        "bio": "Updated from tests.",
    }

    response = client.patch(
        f"/api/v1/users/{user['id']}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["display_name"] == payload["display_name"]


def test_update_user_admin(client: TestClient, db_session: Session):
    user, headers = register_auth(client, 1)
    promote_admin(db_session, user["id"])
    payload = {
        "is_active": False,
        "is_admin": True,
    }

    response = client.patch(
        f"/api/v1/users/{user['id']}/admin",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["is_admin"] is True
    assert response.json()["is_active"] is False


def test_delete_user(client: TestClient, db_session: Session):
    target, target_headers = register_auth(client, 1)
    admin, admin_headers = register_auth(client, 2)
    promote_admin(db_session, admin["id"])

    delete_response = client.delete(
        f"/api/v1/users/{target['id']}",
        headers=target_headers,
    )
    get_response = client.get(
        f"/api/v1/users/{target['id']}",
        headers=admin_headers,
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == target["id"]
    assert get_response.status_code == 404
