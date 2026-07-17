"""End-to-end tests for the todo CRUD API (v1)."""

BASE = "/v1/todos"


def test_list_todos_empty(client):
    resp = client.get(BASE)
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_todo(client):
    resp = client.post(BASE, json={"title": "Buy milk", "status": "open"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Buy milk"
    assert body["status"] == "open"
    assert body["id"] >= 1
    assert "created_at" in body and "updated_at" in body


def test_get_todo_detail(client):
    created = client.post(BASE, json={"title": "Read book", "status": "open"}).json()
    resp = client.get(f"{BASE}/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Read book"


def test_get_missing_todo_returns_400(client):
    resp = client.get(f"{BASE}/999")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Todo is not found"


def test_patch_todo(client):
    created = client.post(BASE, json={"title": "Walk", "status": "open"}).json()
    resp = client.patch(f"{BASE}/{created['id']}", json={"status": "done"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "done"
    assert body["title"] == "Walk"  # untouched by partial update


def test_put_todo(client):
    created = client.post(BASE, json={"title": "Old", "status": "open"}).json()
    resp = client.put(f"{BASE}/{created['id']}", json={"title": "New", "status": "done"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["title"] == "New"
    assert body["status"] == "done"


def test_delete_todo(client):
    created = client.post(BASE, json={"title": "Temp", "status": "open"}).json()
    resp = client.delete(f"{BASE}/{created['id']}")
    assert resp.status_code == 204
    assert client.get(f"{BASE}/{created['id']}").status_code == 400


def test_delete_missing_todo_returns_400(client):
    resp = client.delete(f"{BASE}/999")
    assert resp.status_code == 400
