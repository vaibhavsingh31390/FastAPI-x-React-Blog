from fastapi.testclient import TestClient

from tests.test_enpoints.test_user import create_user, register_auth


def make_post_payload(user_id: int, index: int = 1) -> dict:
    return {
        "slug": f"post-test-{index}",
        "title": f"Test Post {index}",
        "excerpt": "Created from the test.",
        "content": "This is a sample blog post body created from the test suite.",
        "cover_image_url": "https://example.com/covers/test-cover.jpg",
        "status": "draft",
        "published_at": None,
        "category_id": None,
        "author_id": user_id,
        "tag_ids": [],
    }


def create_post(
    client: TestClient,
    user_id: int,
    index: int = 1,
    *,
    headers: dict[str, str],
) -> dict:
    response = client.post(
        "/api/v1/posts/",
        json=make_post_payload(user_id, index),
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()


def test_create_post(client: TestClient):
    user, headers = register_auth(client, 1)

    response = client.post(
        "/api/v1/posts/",
        json=make_post_payload(user_id=user["id"], index=1),
        headers=headers,
    )

    assert response.status_code == 201
    assert response.json()["author_id"] == user["id"]


def test_create_post_without_slug_uses_title(client: TestClient):
    user, headers = register_auth(client, 1)
    payload = make_post_payload(user_id=user["id"], index=1)
    payload.pop("slug")

    response = client.post("/api/v1/posts/", json=payload, headers=headers)

    assert response.status_code == 201
    assert response.json()["slug"] == "test-post-1"


def test_list_posts(client: TestClient):
    user, headers = register_auth(client, 1)
    create_post(client, user["id"], 1, headers=headers)
    create_post(client, user["id"], 2, headers=headers)

    response = client.get("/api/v1/posts/?skip=0&limit=100&sort=desc")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_post(client: TestClient):
    user, headers = register_auth(client, 1)
    post = create_post(client, user["id"], 1, headers=headers)

    response = client.get(f"/api/v1/posts/{post['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == post["id"]


def test_get_post_detail(client: TestClient):
    user, headers = register_auth(client, 1)
    post = create_post(client, user["id"], 1, headers=headers)

    response = client.get(f"/api/v1/posts/{post['id']}/detail")

    assert response.status_code == 200
    assert response.json()["id"] == post["id"]
    assert response.json()["tags"] == []
    assert response.json()["comments"] == []


def test_get_post_by_slug(client: TestClient):
    user, headers = register_auth(client, 1)
    post = create_post(client, user["id"], 1, headers=headers)

    response = client.get(f"/api/v1/posts/slug/{post['slug']}")

    assert response.status_code == 200
    assert response.json()["slug"] == post["slug"]


def test_get_post_detail_by_slug(client: TestClient):
    user, headers = register_auth(client, 1)
    post = create_post(client, user["id"], 1, headers=headers)

    response = client.get(f"/api/v1/posts/slug/{post['slug']}/detail")

    assert response.status_code == 200
    assert response.json()["slug"] == post["slug"]
    assert response.json()["comments"] == []


def test_update_post(client: TestClient):
    user, headers = register_auth(client, 1)
    post = create_post(client, user["id"], 1, headers=headers)
    payload = {
        "title": "Updated Post Title",
        "status": "published",
    }

    response = client.patch(
        f"/api/v1/posts/{post['id']}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]


def test_delete_post(client: TestClient):
    user, headers = register_auth(client, 1)
    post = create_post(client, user["id"], 1, headers=headers)

    delete_response = client.delete(
        f"/api/v1/posts/{post['id']}",
        headers=headers,
    )
    get_response = client.get(f"/api/v1/posts/{post['id']}")

    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == post["id"]
    assert get_response.status_code == 404
