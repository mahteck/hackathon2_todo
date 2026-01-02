"""
Unit tests for data models.

Tests Task TypedDict structure and validation constants.
"""
from src.models import Task, MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH


def test_task_has_all_required_fields():
    """Verify Task TypedDict has all 6 required fields."""
    # Create a valid task
    task: Task = {
        "id": 1,
        "title": "Test",
        "description": "Test description",
        "completed": False,
        "created_at": "2025-01-01T10:00:00",
        "updated_at": "2025-01-01T10:00:00"
    }

    assert "id" in task
    assert "title" in task
    assert "description" in task
    assert "completed" in task
    assert "created_at" in task
    assert "updated_at" in task


def test_task_field_types():
    """Verify Task field types are correct."""
    task: Task = {
        "id": 1,
        "title": "Test",
        "description": "Desc",
        "completed": True,
        "created_at": "2025-01-01T10:00:00",
        "updated_at": "2025-01-01T10:00:00"
    }

    assert isinstance(task["id"], int)
    assert isinstance(task["title"], str)
    assert isinstance(task["description"], str)
    assert isinstance(task["completed"], bool)
    assert isinstance(task["created_at"], str)
    assert isinstance(task["updated_at"], str)


def test_constants():
    """Verify validation constants have correct values."""
    assert MAX_TITLE_LENGTH == 200
    assert MAX_DESCRIPTION_LENGTH == 1000
