"""
Unit tests for TaskService (business logic layer).

Tests validation, business rules, and service operations.
"""
import pytest
import time
from src.task_service import TaskService
from src.exceptions import ValidationError, TaskNotFoundError


# Add Task Tests
def test_add_task_with_title_and_description(task_service):
    """Test creating a task with both title and description."""
    task = task_service.add_task("Buy groceries", "Milk and eggs")
    assert task["id"] == 1
    assert task["title"] == "Buy groceries"
    assert task["description"] == "Milk and eggs"
    assert task["completed"] is False


def test_add_task_with_title_only(task_service):
    """Test creating a task with title only (empty description)."""
    task = task_service.add_task("Quick task")
    assert task["title"] == "Quick task"
    assert task["description"] == ""


def test_add_task_strips_whitespace(task_service):
    """Test that title whitespace is stripped."""
    task = task_service.add_task("  Spaced Title  ")
    assert task["title"] == "Spaced Title"


def test_add_task_empty_title_raises_error(task_service):
    """Test that empty title raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        task_service.add_task("")
    assert "cannot be empty" in str(exc_info.value)


def test_add_task_title_too_long_raises_error(task_service):
    """Test that title exceeding 200 characters raises ValidationError."""
    long_title = "a" * 201
    with pytest.raises(ValidationError) as exc_info:
        task_service.add_task(long_title)
    assert "cannot exceed 200 characters" in str(exc_info.value)


def test_add_task_description_too_long_raises_error(task_service):
    """Test that description exceeding 1000 characters raises ValidationError."""
    long_desc = "a" * 1001
    with pytest.raises(ValidationError) as exc_info:
        task_service.add_task("Title", long_desc)
    assert "cannot exceed 1000 characters" in str(exc_info.value)


# Get Tasks Tests
def test_get_all_tasks_empty(task_service):
    """Test getting all tasks from empty service returns empty list."""
    tasks = task_service.get_all_tasks()
    assert tasks == []


def test_get_all_tasks_multiple_sorted(task_service_with_data):
    """Test getting all tasks returns them sorted by ID."""
    tasks = task_service_with_data.get_all_tasks()
    assert len(tasks) == 3
    assert tasks[0]["id"] == 1
    assert tasks[1]["id"] == 2
    assert tasks[2]["id"] == 3


def test_get_task_by_id_found(task_service_with_data):
    """Test retrieving an existing task by ID."""
    task = task_service_with_data.get_task_by_id(2)
    assert task["id"] == 2
    assert task["title"] == "Task 2"


def test_get_task_by_id_not_found_raises_error(task_service):
    """Test that getting non-existent task raises TaskNotFoundError."""
    with pytest.raises(TaskNotFoundError) as exc_info:
        task_service.get_task_by_id(999)
    assert exc_info.value.task_id == 999


# Update Task Tests
def test_update_task_title_only(task_service_with_data):
    """Test updating only the title."""
    updated = task_service_with_data.update_task(1, title="New Title")
    assert updated["title"] == "New Title"
    assert updated["description"] == "Description 1"  # Unchanged


def test_update_task_description_only(task_service_with_data):
    """Test updating only the description."""
    updated = task_service_with_data.update_task(1, description="New Desc")
    assert updated["description"] == "New Desc"
    assert updated["title"] == "Task 1"  # Unchanged


def test_update_task_both_fields(task_service_with_data):
    """Test updating both title and description."""
    updated = task_service_with_data.update_task(
        1, title="New Title", description="New Desc"
    )
    assert updated["title"] == "New Title"
    assert updated["description"] == "New Desc"


def test_update_task_preserves_other_fields(task_service_with_data):
    """Test that update preserves ID, completed status, and created_at."""
    original = task_service_with_data.get_task_by_id(1)
    updated = task_service_with_data.update_task(1, title="New Title")

    assert updated["id"] == original["id"]
    assert updated["completed"] == original["completed"]
    assert updated["created_at"] == original["created_at"]


def test_update_task_not_found_raises_error(task_service):
    """Test updating non-existent task raises TaskNotFoundError."""
    with pytest.raises(TaskNotFoundError):
        task_service.update_task(999, title="New Title")


def test_update_task_invalid_title_raises_error(task_service_with_data):
    """Test updating with empty title raises ValidationError."""
    with pytest.raises(ValidationError):
        task_service_with_data.update_task(1, title="")


def test_update_task_no_fields_raises_error(task_service_with_data):
    """Test updating with no fields raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        task_service_with_data.update_task(1)
    assert "at least one field" in str(exc_info.value)


# Delete Task Tests
def test_delete_task_existing(task_service_with_data):
    """Test deleting an existing task."""
    deleted = task_service_with_data.delete_task(2)
    assert deleted["id"] == 2
    assert deleted["title"] == "Task 2"

    # Verify it's deleted
    with pytest.raises(TaskNotFoundError):
        task_service_with_data.get_task_by_id(2)


def test_delete_task_not_found_raises_error(task_service):
    """Test deleting non-existent task raises TaskNotFoundError."""
    with pytest.raises(TaskNotFoundError):
        task_service.delete_task(999)


# Complete/Uncomplete Tests
def test_complete_task(task_service_with_data):
    """Test marking a task as complete."""
    task = task_service_with_data.complete_task(1)
    assert task["completed"] is True


def test_complete_task_already_complete_idempotent(task_service_with_data):
    """Test that completing an already-complete task is idempotent."""
    # Task 2 is already complete
    task = task_service_with_data.complete_task(2)
    assert task["completed"] is True  # Should still be True


def test_uncomplete_task(task_service_with_data):
    """Test marking a task as incomplete."""
    # Task 2 is complete, mark it incomplete
    task = task_service_with_data.uncomplete_task(2)
    assert task["completed"] is False


def test_uncomplete_task_already_incomplete_idempotent(task_service_with_data):
    """Test that marking an incomplete task as incomplete is idempotent."""
    # Task 1 is already incomplete
    task = task_service_with_data.uncomplete_task(1)
    assert task["completed"] is False  # Should still be False


# Timestamp Tests
def test_timestamps_set_on_create(task_service):
    """Test that timestamps are set when creating a task."""
    task = task_service.add_task("Test")
    assert "created_at" in task
    assert "updated_at" in task
    assert task["created_at"] == task["updated_at"]  # Same initially


def test_updated_at_changes_on_update(task_service):
    """Test that updated_at changes when task is updated."""
    task = task_service.add_task("Test")
    original_updated = task["updated_at"]

    time.sleep(0.01)  # Small delay to ensure different timestamp

    updated = task_service.update_task(1, title="Updated")
    assert updated["updated_at"] != original_updated


def test_created_at_immutable_on_update(task_service):
    """Test that created_at doesn't change when task is updated."""
    task = task_service.add_task("Test")
    original_created = task["created_at"]

    time.sleep(0.01)

    updated = task_service.update_task(1, title="Updated")
    assert updated["created_at"] == original_created
