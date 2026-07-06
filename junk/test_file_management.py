import pytest
from fastapi.testclient import TestClient

import test


@pytest.fixture
def client(tmp_path, monkeypatch):
    file_path = tmp_path / "file.txt"
    monkeypatch.setattr(test, "FILE_PATH", str(file_path))
    return TestClient(test.app)


def test_list_files_when_missing(client):
    response = client.get("/list_files")

    assert response.status_code == 200
    assert response.json() == {"status": "success", "data": ""}


def test_add_to_file_writes_content(client):
    response = client.post("/add_to_file", json={"content": "hello world"})

    assert response.status_code == 200
    assert response.json() == {"status": "success", "data": "hello world"}


def test_list_files_after_write(client):
    client.post("/add_to_file", json={"content": "hello world"})
    response = client.get("/list_files")

    assert response.status_code == 200
    assert response.json() == {"status": "success", "data": "hello world"}


def test_add_to_file_appends_content(client):
    client.post("/add_to_file", json={"content": "first"})
    client.post("/add_to_file", json={"content": " second"})
    response = client.get("/list_files")

    assert response.status_code == 200
    assert response.json() == {"status": "success", "data": "first second"}
