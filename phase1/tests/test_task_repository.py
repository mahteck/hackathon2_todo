"""
Unit tests for TaskRepository (data access layer).

Tests CRUD operations and ID generation.
"""
import pytest
from src.task_repository import TaskRepository


def test_generate_unique_ids(empty_repository):
    """Test that IDs are generated sequentially starting from 1."""
    repo = empty_repository
    assert repo.generate_id() == 1
    assert repo.generate_id() == 2
    assert repo.generate_id() == 3


def test_create_task(empty_repository):
    """Test task creation and storage."""
    repo = empty_repository
    task = {
        "id": 1,
        "title": "Test Task",
        "description": "Test Description",
        "completed": False,
        "created_at": "2025-01-01T10:00:00",
        "updated_at": "2025-01-01T10:00:00"
    }
    created = repo.create(task)
    assert created["id"] == 1
    assert created["title"] == "Test Task"


def test_find_by_id_existing(repository_with_tasks):
    """Test retrieving an existing task by ID."""
    repo = repository_with_tasks
    task = repo.find_by_id(2)
    assert task is not None
    assert task["id"] == 2
    assert task["title"] == "Task 2"


def test_find_by_id_not_found(empty_repository):
    """Test retrieving a non-existent task returns None."""
    repo = empty_repository
    task = repo.find_by_id(999)
    assert task is None


def test_find_all_empty(empty_repository):
    """Test finding all tasks in empty repository returns empty list."""
    repo = empty_repository
    tasks = repo.find_all()
    assert tasks == []


def test_find_all_multiple(repository_with_tasks):
    """Test retrieving all tasks returns them sorted by ID."""
    repo = repository_with_tasks
    tasks = repo.find_all()
    assert len(tasks) == 3
    assert tasks[0]["id"] == 1
    assert tasks[1]["id"] == 2
    assert tasks[2]["id"] == 3


def test_update_task(repository_with_tasks):
    """Test updating an existing task."""
    repo = repository_with_tasks
    task = repo.find_by_id(1)
    task["title"] = "Updated Title"
    updated = repo.update(1, task)
    assert updated["title"] == "Updated Title"

    # Verify it's persisted
    retrieved = repo.find_by_id(1)
    assert retrieved["title"] == "Updated Title"


def test_delete_task_existing(repository_with_tasks):
    """Test deleting an existing task."""
    repo = repository_with_tasks
    result = repo.delete(2)
    assert result is True

    # Verify it's deleted
    assert repo.find_by_id(2) is None


def test_delete_task_nonexistent(empty_repository):
    """Test deleting a non-existent task returns False."""
    repo = empty_repository
    result = repo.delete(999)
    assert result is False
