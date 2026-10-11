import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
import app as app_module

@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test_planner.db"
    monkeypatch.setattr(app_module, "DB_PATH", str(db_path))
    app_module.init_db()
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client

def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"FocusFlow" in response.data

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_api_returns_seed_tasks(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert len(response.json) >= 1

def test_add_task(client):
    response = client.post("/tasks", data={
        "title": "Prepare presentation",
        "category": "College",
        "priority": "High",
        "due_date": ""
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Prepare presentation" in response.data

def test_blank_task_is_rejected(client):
    response = client.post("/tasks", data={"title": "  "}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Please enter a task title" in response.data

def test_toggle_task(client):
    with app_module.connect_db() as db:
        task_id = db.execute("SELECT id FROM tasks LIMIT 1").fetchone()["id"]
    response = client.post(f"/tasks/{task_id}/toggle", follow_redirects=True)
    assert response.status_code == 200
    with app_module.connect_db() as db:
        task = db.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,)).fetchone()
    assert task["completed"] == 1

def test_delete_task(client):
    with app_module.connect_db() as db:
        task_id = db.execute("SELECT id FROM tasks LIMIT 1").fetchone()["id"]
    response = client.post(f"/tasks/{task_id}/delete", follow_redirects=True)
    assert response.status_code == 200
    with app_module.connect_db() as db:
        assert db.execute("SELECT id FROM tasks WHERE id = ?", (task_id,)).fetchone() is None
