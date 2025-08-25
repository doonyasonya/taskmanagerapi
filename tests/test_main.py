import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_task():
    response = client.post(
        "/tasks/",
        json={"title": "Test task", "description": "Some desc"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["status"] == "created"


def test_get_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_valid_status_transitions():
    # create
    create = client.post("/tasks/", json={"title": "StatusFlow"})
    task_id = create.json()["id"]

    # valid transition: created -> in_progress
    r1 = client.put(f"/tasks/{task_id}", json={"status": "in_progress"})
    assert r1.status_code == 200
    assert r1.json()["status"] == "in_progress"

    # valid transition: in_progress -> done
    r2 = client.put(f"/tasks/{task_id}", json={"status": "done"})
    assert r2.status_code == 200
    assert r2.json()["status"] == "done"


def test_invalid_status_transitions():
    # create
    create = client.post("/tasks/", json={"title": "InvalidFlow"})
    task_id = create.json()["id"]

    # try invalid: created -> done
    r1 = client.put(f"/tasks/{task_id}", json={"status": "done"})
    assert r1.status_code == 422

    # move to in_progress
    client.put(f"/tasks/{task_id}", json={"status": "in_progress"})

    # try invalid: in_progress -> created
    r2 = client.put(f"/tasks/{task_id}", json={"status": "created"})
    assert r2.status_code == 422

    # move to done
    client.put(f"/tasks/{task_id}", json={"status": "done"})

    # try invalid: done -> in_progress
    r3 = client.put(f"/tasks/{task_id}", json={"status": "in_progress"})
    assert r3.status_code == 422


def test_delete_task():
    create = client.post("/tasks/", json={"title": "ToDelete"})
    task_id = create.json()["id"]

    delete = client.delete(f"/tasks/{task_id}")
    assert delete.status_code == 204

    get = client.get(f"/tasks/{task_id}")
    assert get.status_code == 404
