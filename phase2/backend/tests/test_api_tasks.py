"""Tests for task API endpoints."""
import pytest


@pytest.mark.asyncio
async def test_create_task_api(client):
    """Test POST /api/v1/tasks endpoint."""
    response = await client.post(
        "/api/v1/tasks",
        json={
            "title": "API Test Task",
            "description": "Testing the API",
            "priority": "high",
            "tags": ["test"]
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert "data" in data
    assert data["data"]["title"] == "API Test Task"
    assert data["data"]["priority"] == "high"
    assert data["message"] == "Task created successfully"


@pytest.mark.asyncio
async def test_create_task_validation_error(client):
    """Test creating task with invalid data."""
    response = await client.post(
        "/api/v1/tasks",
        json={"description": "No title"}
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_tasks_api(client):
    """Test GET /api/v1/tasks endpoint."""
    # Create test tasks
    await client.post(
        "/api/v1/tasks",
        json={"title": "Task 1", "priority": "high"}
    )
    await client.post(
        "/api/v1/tasks",
        json={"title": "Task 2", "priority": "low"}
    )

    response = await client.get("/api/v1/tasks")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["total"] == 2
    assert len(data["data"]["tasks"]) == 2


@pytest.mark.asyncio
async def test_list_tasks_filter_priority(client):
    """Test filtering tasks by priority."""
    await client.post("/api/v1/tasks", json={"title": "High", "priority": "high"})
    await client.post("/api/v1/tasks", json={"title": "Low", "priority": "low"})

    response = await client.get("/api/v1/tasks?priority=high")

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total"] == 1
    assert data["data"]["tasks"][0]["title"] == "High"


@pytest.mark.asyncio
async def test_get_task_api(client):
    """Test GET /api/v1/tasks/{id} endpoint."""
    # Create a task
    create_response = await client.post(
        "/api/v1/tasks",
        json={"title": "Get Me"}
    )
    task_id = create_response.json()["data"]["id"]

    # Get the task
    response = await client.get(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == task_id
    assert data["data"]["title"] == "Get Me"


@pytest.mark.asyncio
async def test_get_task_not_found(client):
    """Test getting non-existent task."""
    response = await client.get("/api/v1/tasks/999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task_api(client):
    """Test PATCH /api/v1/tasks/{id} endpoint."""
    # Create a task
    create_response = await client.post(
        "/api/v1/tasks",
        json={"title": "Original"}
    )
    task_id = create_response.json()["data"]["id"]

    # Update the task
    response = await client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Updated", "completed": True}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["title"] == "Updated"
    assert data["data"]["completed"] is True
    assert data["message"] == "Task updated successfully"


@pytest.mark.asyncio
async def test_update_task_not_found(client):
    """Test updating non-existent task."""
    response = await client.patch(
        "/api/v1/tasks/999",
        json={"title": "Updated"}
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task_no_fields(client):
    """Test updating with no fields."""
    create_response = await client.post(
        "/api/v1/tasks",
        json={"title": "Task"}
    )
    task_id = create_response.json()["data"]["id"]

    response = await client.patch(f"/api/v1/tasks/{task_id}", json={})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_task_api(client):
    """Test DELETE /api/v1/tasks/{id} endpoint."""
    # Create a task
    create_response = await client.post(
        "/api/v1/tasks",
        json={"title": "Delete Me"}
    )
    task_id = create_response.json()["data"]["id"]

    # Delete the task
    response = await client.delete(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task deleted successfully"

    # Verify deletion
    get_response = await client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_not_found(client):
    """Test deleting non-existent task."""
    response = await client.delete("/api/v1/tasks/999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_tags_api(client):
    """Test GET /api/v1/tags endpoint."""
    # Create a task with tags
    await client.post(
        "/api/v1/tasks",
        json={"title": "Task", "tags": ["work", "urgent"]}
    )

    response = await client.get("/api/v1/tags")

    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2


@pytest.mark.asyncio
async def test_create_tag_api(client):
    """Test POST /api/v1/tags endpoint."""
    response = await client.post(
        "/api/v1/tags",
        json={"name": "personal", "color": "#3B82F6"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["data"]["name"] == "personal"
    assert data["data"]["color"] == "#3B82F6"
    assert data["message"] == "Tag created successfully"
