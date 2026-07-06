from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from database.models.users import User
from tests.test_enpoints.test_user import make_user_payload


def test_register_user(client: TestClient):
    payload = make_user_payload()

    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == payload["email"]


def test_register_duplicate_email(client: TestClient):
    payload = make_user_payload()

    client.post("/api/v1/auth/register", json=payload)
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_user(client: TestClient):
    payload = make_user_payload()
    client.post("/api/v1/auth/register", json=payload)

    response = client.post(
        "/api/v1/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["user"]["email"] == payload["email"]


def test_login_invalid_credentials(client: TestClient):
    payload = make_user_payload()
    client.post("/api/v1/auth/register", json=payload)

    response = client.post(
        "/api/v1/auth/login",
        json={"email": payload["email"], "password": "wrongpassword"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_inactive_user(client: TestClient, db_session: Session):
    payload = make_user_payload()
    register_response = client.post("/api/v1/auth/register", json=payload)
    user = register_response.json()["user"]

    db_user = db_session.get(User, user["id"])
    assert db_user is not None
    db_user.is_active = False
    db_session.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Account is inactive"
