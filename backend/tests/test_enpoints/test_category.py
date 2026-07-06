from fastapi.testclient import TestClient

from tests.test_enpoints.test_post import make_post_payload
from tests.test_enpoints.test_user import create_user


def make_category_payload(index: int = 1) -> dict:
    return {
        "slug": f"category-test-{index}",
        "name": f"Category Test {index}",
        "description": "Created from the test suite.",
    }


def create_category(client: TestClient, index: int = 1) -> dict:
    response = client.post("/api/v1/categories/", json=make_category_payload(index))
    assert response.status_code == 201
    return response.json()


def create_post_for_category(
    client: TestClient,
    user_id: int,
    category_id: int,
    index: int = 1,
) -> dict:
    payload = make_post_payload(user_id=user_id, index=index)
    payload["category_id"] = category_id
    response = client.post("/api/v1/posts/", json=payload)
    assert response.status_code == 201
    return response.json()


def test_create_category(client: TestClient):
    payload = make_category_payload()

    response = client.post("/api/v1/categories/", json=payload)

    assert response.status_code == 201
    assert response.json()["name"] == payload["name"]


def test_create_category_without_slug_uses_name(client: TestClient):
    payload = make_category_payload()
    payload.pop("slug")

    response = client.post("/api/v1/categories/", json=payload)

    assert response.status_code == 201
    assert response.json()["slug"] == "category-test-1"


def test_list_categories(client: TestClient):
    create_category(client, 1)
    create_category(client, 2)

    response = client.get("/api/v1/categories/?skip=0&limit=100&sort=desc")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_category(client: TestClient):
    category = create_category(client, 1)

    response = client.get(f"/api/v1/categories/{category['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == category["id"]


def test_get_category_by_slug(client: TestClient):
    category = create_category(client, 1)

    response = client.get(f"/api/v1/categories/slug/{category['slug']}")

    assert response.status_code == 200
    assert response.json()["slug"] == category["slug"]


def test_get_category_with_posts(client: TestClient):
    user = create_user(client, 1)
    category = create_category(client, 1)
    post = create_post_for_category(client, user["id"], category["id"], 1)

    response = client.get(f"/api/v1/categories/{category['id']}/posts")

    assert response.status_code == 200
    assert response.json()["id"] == category["id"]
    assert len(response.json()["posts"]) == 1
    assert response.json()["posts"][0]["id"] == post["id"]


def test_get_category_with_posts_by_slug(client: TestClient):
    user = create_user(client, 1)
    category = create_category(client, 1)
    post = create_post_for_category(client, user["id"], category["id"], 1)

    response = client.get(f"/api/v1/categories/slug/{category['slug']}/posts")

    assert response.status_code == 200
    assert response.json()["slug"] == category["slug"]
    assert len(response.json()["posts"]) == 1
    assert response.json()["posts"][0]["id"] == post["id"]


def test_update_category(client: TestClient):
    category = create_category(client, 1)
    payload = {
        "name": "Updated Category Name",
        "description": "Updated from tests.",
    }

    response = client.patch(f"/api/v1/categories/{category['id']}", json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]


def test_delete_category(client: TestClient):
    category = create_category(client, 1)

    delete_response = client.delete(f"/api/v1/categories/{category['id']}")
    get_response = client.get(f"/api/v1/categories/{category['id']}")

    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == category["id"]
    assert get_response.status_code == 404
