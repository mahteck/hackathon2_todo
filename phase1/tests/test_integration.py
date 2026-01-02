"""
Integration tests for complete user workflows.

Tests end-to-end scenarios across all layers.
"""
import pytest
import time
from src.task_service import TaskService
from src.task_repository import TaskRepository


@pytest.fixture
def fresh_service():
    """Provide a fresh service for each integration test."""
    return TaskService(TaskRepository())


def test_complete_user_workflow(fresh_service):
    """
    Test complete user workflow: add → view → update → complete → delete.

    Simulates a user creating, managing, and deleting a task.
    """
    service = fresh_service

    # Add task
    task = service.add_task("Buy groceries", "Milk and eggs")
    assert task["id"] == 1
    assert task["title"] == "Buy groceries"
    assert task["completed"] is False

    # View all tasks
    tasks = service.get_all_tasks()
    assert len(tasks) == 1

    # View task detail
    retrieved = service.get_task_by_id(1)
    assert retrieved["title"] == "Buy groceries"

    # Update task
    updated = service.update_task(1, title="Buy groceries and snacks")
    assert updated["title"] == "Buy groceries and snacks"

    # Complete task
    completed = service.complete_task(1)
    assert completed["completed"] is True

    # Delete task
    deleted = service.delete_task(1)
    assert deleted["id"] == 1

    # Verify deletion
    tasks = service.get_all_tasks()
    assert len(tasks) == 0


def test_multiple_tasks_management(fresh_service):
    """
    Test managing multiple tasks simultaneously.

    Create 10 tasks, complete 5, delete 2, verify state.
    """
    service = fresh_service

    # Add 10 tasks
    for i in range(1, 11):
        service.add_task(f"Task {i}", f"Description {i}")

    # Verify all created
    tasks = service.get_all_tasks()
    assert len(tasks) == 10

    # Complete tasks 1, 3, 5, 7, 9
    for task_id in [1, 3, 5, 7, 9]:
        service.complete_task(task_id)

    # Delete tasks 2, 4
    service.delete_task(2)
    service.delete_task(4)

    # Verify final state
    tasks = service.get_all_tasks()
    assert len(tasks) == 8

    # Count completed tasks
    completed_count = sum(1 for task in tasks if task["completed"])
    assert completed_count == 5


def test_error_recovery(fresh_service):
    """
    Test that application continues after errors.

    Trigger validation error, then successfully add task.
    """
    service = fresh_service

    # Trigger validation error
    with pytest.raises(Exception):
        service.add_task("")  # Empty title

    # Application should still work
    task = service.add_task("Valid task")
    assert task["id"] == 1


def test_task_independence(fresh_service):
    """
    Test that modifying one task doesn't affect others.

    Create 3 tasks, update task 2, verify tasks 1 and 3 unchanged.
    """
    service = fresh_service

    # Create 3 tasks
    task1 = service.add_task("Task 1", "Desc 1")
    task2 = service.add_task("Task 2", "Desc 2")
    task3 = service.add_task("Task 3", "Desc 3")

    # Update task 2
    service.update_task(2, title="Updated Task 2")

    # Verify task 1 unchanged
    retrieved1 = service.get_task_by_id(1)
    assert retrieved1["title"] == "Task 1"
    assert retrieved1["description"] == "Desc 1"

    # Verify task 3 unchanged
    retrieved3 = service.get_task_by_id(3)
    assert retrieved3["title"] == "Task 3"
    assert retrieved3["description"] == "Desc 3"

    # Verify task 2 changed
    retrieved2 = service.get_task_by_id(2)
    assert retrieved2["title"] == "Updated Task 2"


def test_idempotent_operations(fresh_service):
    """
    Test that idempotent operations work correctly.

    Complete task twice, uncomplete task twice.
    """
    service = fresh_service

    task = service.add_task("Test Task")

    # Mark complete twice
    service.complete_task(1)
    service.complete_task(1)  # Should not error

    retrieved = service.get_task_by_id(1)
    assert retrieved["completed"] is True

    # Mark incomplete twice
    service.uncomplete_task(1)
    service.uncomplete_task(1)  # Should not error

    retrieved = service.get_task_by_id(1)
    assert retrieved["completed"] is False


def test_timestamp_behavior(fresh_service):
    """
    Test that timestamps behave correctly.

    Verify created_at is immutable, updated_at changes.
    """
    service = fresh_service

    task = service.add_task("Test Task")
    original_created = task["created_at"]
    original_updated = task["updated_at"]

    # Wait briefly to ensure timestamp difference
    time.sleep(0.01)

    # Update task
    updated = service.update_task(1, title="New Title")

    # created_at should be unchanged
    assert updated["created_at"] == original_created

    # updated_at should be different
    assert updated["updated_at"] != original_updated
