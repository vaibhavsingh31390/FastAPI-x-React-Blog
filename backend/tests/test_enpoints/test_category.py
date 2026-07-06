from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.test_enpoints.test_post import make_post_payload
from tests.test_enpoints.test_user import promote_admin, register_auth


def make_category_payload(index: int = 1) -> dict:
    return {
        "slug": f"category-test-{index}",
        "name": f"Category Test {index}",
        "description": "Created from the test suite.",
    }


def create_category(
    client: TestClient,
    index: int = 1,
    *,
    headers: dict[str, str],
) -> dict:
    response = client.post(
        "/api/v1/categories/",
        json=make_category_payload(index),
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()


def create_post_for_category(
    client: TestClient,
    user_id: int,
    category_id: int,
    index: int = 1,
    *,
    headers: dict[str, str],
) -> dict:
    payload = make_post_payload(user_id=user_id, index=index)
    payload["category_id"] = category_id
    response = client.post("/api/v1/posts/", json=payload, headers=headers)
    assert response.status_code == 201
    return response.json()


def admin_auth(client: TestClient, db_session: Session, index: int = 1):
    user, headers = register_auth(client, index)
    promote_admin(db_session, user["id"])
    return user, headers


def test_create_category(client: TestClient, db_session: Session):
    _, headers = admin_auth(client, db_session, 1)
    payload = make_category_payload()

    response = client.post("/api/v1/categories/", json=payload, headers=headers)

    assert response.status_code == 201
    assert response.json()["name"] == payload["name"]


def test_create_category_without_slug_uses_name(client: TestClient, db_session: Session):
    _, headers = admin_auth(client, db_session, 1)
    payload = make_category_payload()
    payload.pop("slug")

    response = client.post("/api/v1/categories/", json=payload, headers=headers)

    assert response.status_code == 201
    assert response.json()["slug"] == "category-test-1"


def test_list_categories(client: TestClient, db_session: Session):
    _, headers = admin_auth(client, db_session, 1)
    create_category(client, 1, headers=headers)
    create_category(client, 2, headers=headers)

    response = client.get("/api/v1/categories/?skip=0&limit=100&sort=desc")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_category(client: TestClient, db_session: Session):
    _, headers = admin_auth(client, db_session, 1)
    category = create_category(client, 1, headers=headers)

    response = client.get(f"/api/v1/categories/{category['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == category["id"]


def test_get_category_by_slug(client: TestClient, db_session: Session):
    _, headers = admin_auth(client, db_session, 1)
    category = create_category(client, 1, headers=headers)

    response = client.get(f"/api/v1/categories/slug/{category['slug']}")

    assert response.status_code == 200
    assert response.json()["slug"] == category["slug"]


def test_get_category_with_posts(client: TestClient, db_session: Session):
    user, user_headers = register_auth(client, 1)
    _, admin_headers = admin_auth(client, db_session, 2)
    category = create_category(client, 1, headers=admin_headers)
    post = create_post_for_category(
        client,
        user["id"],
        category["id"],
        1,
        headers=user_headers,
    )

    response = client.get(f"/api/v1/categories/{category['id']}/posts")

    assert response.status_code == 200
    assert response.json()["id"] == category["id"]
    assert len(response.json()["posts"]) == 1
    assert response.json()["posts"][0]["id"] == post["id"]


def test_get_category_with_posts_by_slug(client: TestClient, db_session: Session):
    user, user_headers = register_auth(client, 1)
    _, admin_headers = admin_auth(client, db_session, 2)
    category = create_category(client, 1, headers=admin_headers)
    post = create_post_for_category(
        client,
        user["id"],
        category["id"],
        1,
        headers=user_headers,
    )

    response = client.get(f"/api/v1/categories/slug/{category['slug']}/posts")

    assert response.status_code == 200
    assert response.json()["slug"] == category["slug"]
    assert len(response.json()["posts"]) == 1
    assert response.json()["posts"][0]["id"] == post["id"]


def test_update_category(client: TestClient, db_session: Session):
    _, headers = admin_auth(client, db_session, 1)
    category = create_category(client, 1, headers=headers)
    payload = {
        "name": "Updated Category Name",
        "description": "Updated from tests.",
    }

    response = client.patch(
        f"/api/v1/categories/{category['id']}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]


def test_delete_category(client: TestClient, db_session: Session):
    _, headers = admin_auth(client, db_session, 1)
    category = create_category(client, 1, headers=headers)

    delete_response = client.delete(
        f"/api/v1/categories/{category['id']}",
        headers=headers,
    )
    get_response = client.get(f"/api/v1/categories/{category['id']}")

    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == category["id"]
    assert get_response.status_code == 404
