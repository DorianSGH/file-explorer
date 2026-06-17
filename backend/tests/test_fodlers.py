def test_get_all_folders_empty(client):
    response = client.get("/folders")
    assert response.status_code == 200
    assert response.json() == []


def test_create_folder_at_root(client):
    response = client.post("/folders", json={"name": "docs", "parent_id": None})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "docs"
    assert data["parent_id"] is None


def test_create_subfolder(client):
    parent = client.post("/folders", json={"name": "docs", "parent_id": None}).json()

    response = client.post("/folders", json={"name": "images", "parent_id": parent["id"]})
    assert response.status_code == 201
    assert response.json()["parent_id"] == parent["id"]


def test_create_folder_invalid_parent(client):
    response = client.post("/folders", json={"name": "docs", "parent_id": 999})
    assert response.status_code == 400


def test_create_duplicate_folder(client):
    client.post("/folders", json={"name": "docs", "parent_id": None})
    response = client.post("/folders", json={"name": "docs", "parent_id": None})
    assert response.status_code == 400


def test_delete_folder(client):
    created = client.post("/folders", json={"name": "docs", "parent_id": None}).json()

    response = client.delete(f"/folders/{created['id']}")
    assert response.status_code == 200

    folders = client.get("/folders").json()
    assert not any(f["id"] == created["id"] for f in folders)


def test_delete_folder_not_found(client):
    response = client.delete("/folders/999")
    assert response.status_code == 404


def test_delete_folder_cascades_to_subfolders(client):
    parent = client.post("/folders", json={"name": "docs", "parent_id": None}).json()
    child = client.post("/folders", json={"name": "images", "parent_id": parent["id"]}).json()

    client.delete(f"/folders/{parent['id']}")

    folders = client.get("/folders").json()
    assert not any(f["id"] == child["id"] for f in folders)


def test_delete_folder_cascades_to_files(client):
    folder = client.post("/folders", json={"name": "docs", "parent_id": None}).json()
    file = client.post("/files", json={"name": "readme.txt", "folder_id": folder["id"]}).json()

    client.delete(f"/folders/{folder['id']}")

    files = client.get("/files").json()
    assert not any(f["id"] == file["id"] for f in files)


def test_browse_root(client):
    client.post("/folders", json={"name": "docs", "parent_id": None})
    client.post("/files", json={"name": "readme.txt", "folder_id": None})

    response = client.get("/folders/browse")
    assert response.status_code == 200
    data = response.json()
    assert any(f["name"] == "docs" for f in data["subfolders"])
    assert any(f["name"] == "readme.txt" for f in data["files"])


def test_browse_subfolder(client):
    parent = client.post("/folders", json={"name": "docs", "parent_id": None}).json()
    client.post("/folders", json={"name": "images", "parent_id": parent["id"]})
    client.post("/files", json={"name": "notes.txt", "folder_id": parent["id"]})

    response = client.get(f"/folders/browse?parent_id={parent['id']}")
    assert response.status_code == 200
    data = response.json()
    assert any(f["name"] == "images" for f in data["subfolders"])
    assert any(f["name"] == "notes.txt" for f in data["files"])


def test_browse_invalid_folder(client):
    response = client.get("/folders/browse?parent_id=999")
    assert response.status_code == 404