import pytest


def test_get_all_files_empty(client):
    response = client.get("/files")
    assert response.status_code == 200
    assert response.json() == []


def test_create_file_at_root(client):
    response = client.post("/files", json={"name": "readme.txt", "folder_id": None})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "readme.txt"
    assert data["folder_id"] is None


def test_create_file_invalid_folder(client):
    response = client.post("/files", json={"name": "test.txt", "folder_id": 999})
    assert response.status_code == 400


def test_create_duplicate_file(client):
    client.post("/files", json={"name": "readme.txt", "folder_id": None})
    response = client.post("/files", json={"name": "readme.txt", "folder_id": None})
    assert response.status_code == 400


def test_delete_file(client):
    created = client.post("/files", json={"name": "readme.txt", "folder_id": None})
    file_id = created.json()["id"]

    response = client.delete(f"/files/{file_id}")
    assert response.status_code == 200

    files = client.get("/files").json()
    assert not any(f["id"] == file_id for f in files)


def test_delete_file_not_found(client):
    response = client.delete("/files/999")
    assert response.status_code == 404


def test_search_exact(client):
    client.post("/files", json={"name": "notes.txt", "folder_id": None})
    client.post("/files", json={"name": "other.txt", "folder_id": None})

    response = client.get("/search?q=notes.txt")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "notes.txt"


def test_search_exact_no_results(client):
    response = client.get("/search?q=nonexistent.txt")
    assert response.status_code == 200
    assert response.json() == []


def test_search_exact_scoped_to_folder(client):
    folder = client.post("/folders", json={"name": "docs", "parent_id": None}).json()
    client.post("/files", json={"name": "notes.txt", "folder_id": None})
    client.post("/files", json={"name": "notes.txt", "folder_id": folder["id"]})

    response = client.get(f"/search?q=notes.txt&folder_id={folder['id']}")
    assert len(response.json()) == 1
    assert response.json()[0]["folder_id"] == folder["id"]


def test_autocomplete(client):
    client.post("/files", json={"name": "readme.txt", "folder_id": None})
    client.post("/files", json={"name": "report.txt", "folder_id": None})
    client.post("/files", json={"name": "other.txt", "folder_id": None})

    response = client.get("/search/autocomplete?q=re")
    assert response.status_code == 200
    names = [f["name"] for f in response.json()]
    assert "readme.txt" in names
    assert "report.txt" in names
    assert "other.txt" not in names


def test_autocomplete_limit(client):
    for i in range(15):
        client.post("/files", json={"name": f"file{i:02d}.txt", "folder_id": None})

    response = client.get("/search/autocomplete?q=file")
    assert len(response.json()) <= 10


def test_autocomplete_case_insensitive(client):
    client.post("/files", json={"name": "README.txt", "folder_id": None})

    response = client.get("/search/autocomplete?q=read")
    assert len(response.json()) == 1