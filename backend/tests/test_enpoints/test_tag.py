from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.test_enpoints.test_post import make_post_payload
from tests.test_enpoints.test_user import promote_admin, register_auth


def make_tag_payload(index: int = 1) -> dict:
    return {
        "slug": f"tag-test-{index}",
        "name": f"Tag Test {index}",
    }


def create_tag(
    client: TestClient,
    index: int = 1,
    *,
    headers: dict[str, str],
) -> dict:
    response = client.post(
        "/api/v1/tags/",
        json=make_tag_payload(index),
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()


def create_post_for_tag(
    client: TestClient,
    user_id: int,
    tag_id: int,
    index: int = 1,
    *,
    headers: dict[str, str],
) -> dict:
    payload = make_post_payload(user_id=user_id, index=index)
    payload["tag_ids"] = [tag_id]
    response = client.post("/api/v1/posts/", json=payload, headers=headers)
    assert response.status_code == 201
    return response.json()


def admin_auth(client: TestClient, db_session: Session, index: int = 1):
    user, headers = register_auth(client, index)
    promote_admin(db_session, user["id"])
    return user, headers


def test_create_tag(client: TestClient, db_session: Session):
    _, headers = admin_auth(client, db_session, 1)
    payload = make_tag_payload()

    response = client.post("/api/v1/tags/", json=payload, headers=headers)

    assert response.status_code == 201
    assert response.json()["name"] == payload["name"]


def test_create_tag_without_slug_uses_name(client: TestClient, db_session: Session):
    _, headers = admin_auth(client, db_session, 1)
    payload = make_tag_payload()
    payload.pop("slug")

    response = client.post("/api/v1/tags/", json=payload, headers=headers)

    assert response.status_code == 201
    assert response.json()["slug"] == "tag-test-1"


def test_list_tags(client: TestClient, db_session: Session):
    _, headers = admin_auth(client, db_session, 1)
    create_tag(client, 1, headers=headers)
    create_tag(client, 2, headers=headers)

    response = client.get("/api/v1/tags/?skip=0&limit=100&sort=desc")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_tag(client: TestClient, db_session: Session):
    _, headers = admin_auth(client, db_session, 1)
    tag = create_tag(client, 1, headers=headers)

    response = client.get(f"/api/v1/tags/{tag['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == tag["id"]


def test_get_tag_by_slug(client: TestClient, db_session: Session):
    _, headers = admin_auth(client, db_session, 1)
    tag = create_tag(client, 1, headers=headers)

    response = client.get(f"/api/v1/tags/slug/{tag['slug']}")

    assert response.status_code == 200
    assert response.json()["slug"] == tag["slug"]


def test_get_tag_with_posts(client: TestClient, db_session: Session):
    user, user_headers = register_auth(client, 1)
    _, admin_headers = admin_auth(client, db_session, 2)
    tag = create_tag(client, 1, headers=admin_headers)
    post = create_post_for_tag(
        client,
        user["id"],
        tag["id"],
        1,
        headers=user_headers,
    )

    response = client.get(f"/api/v1/tags/{tag['id']}/posts")

    assert response.status_code == 200
    assert response.json()["id"] == tag["id"]
    assert len(response.json()["posts"]) == 1
    assert response.json()["posts"][0]["id"] == post["id"]


def test_get_tag_with_posts_by_slug(client: TestClient, db_session: Session):
    user, user_headers = register_auth(client, 1)
    _, admin_headers = admin_auth(client, db_session, 2)
    tag = create_tag(client, 1, headers=admin_headers)
    post = create_post_for_tag(
        client,
        user["id"],
        tag["id"],
        1,
        headers=user_headers,
    )

    response = client.get(f"/api/v1/tags/slug/{tag['slug']}/posts")

    assert response.status_code == 200
    assert response.json()["slug"] == tag["slug"]
    assert len(response.json()["posts"]) == 1
    assert response.json()["posts"][0]["id"] == post["id"]


def test_update_tag(client: TestClient, db_session: Session):
    _, headers = admin_auth(client, db_session, 1)
    tag = create_tag(client, 1, headers=headers)
    payload = {
        "name": "tag-test-updated",
    }

    response = client.patch(
        f"/api/v1/tags/{tag['id']}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]


def test_delete_tag(client: TestClient, db_session: Session):
    _, headers = admin_auth(client, db_session, 1)
    tag = create_tag(client, 1, headers=headers)

    delete_response = client.delete(f"/api/v1/tags/{tag['id']}", headers=headers)
    get_response = client.get(f"/api/v1/tags/{tag['id']}")

    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == tag["id"]
    assert get_response.status_code == 404
