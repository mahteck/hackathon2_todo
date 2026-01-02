"""
Pytest configuration and shared fixtures.

Provides reusable test fixtures for repository and service instances.
"""
import pytest
from src.task_repository import TaskRepository
from src.task_service import TaskService


@pytest.fixture
def empty_repository():
    """Provide a fresh, empty repository for each test."""
    repo = TaskRepository()
    repo.clear()
    return repo


@pytest.fixture
def repository_with_tasks(empty_repository):
    """Provide a repository with 3 sample tasks."""
    repo = empty_repository

    # Create sample tasks directly in repository
    task1 = {
        "id": 1,
        "title": "Task 1",
        "description": "Description 1",
        "completed": False,
        "created_at": "2025-01-01T10:00:00",
        "updated_at": "2025-01-01T10:00:00"
    }
    task2 = {
        "id": 2,
        "title": "Task 2",
        "description": "",
        "completed": True,
        "created_at": "2025-01-01T11:00:00",
        "updated_at": "2025-01-01T11:00:00"
    }
    task3 = {
        "id": 3,
        "title": "Task 3",
        "description": "Description 3",
        "completed": False,
        "created_at": "2025-01-01T12:00:00",
        "updated_at": "2025-01-01T12:00:00"
    }

    repo.create(task1)
    repo.create(task2)
    repo.create(task3)
    repo._next_id = 4  # Set next ID to 4

    return repo


@pytest.fixture
def task_service(empty_repository):
    """Provide a TaskService with empty repository."""
    return TaskService(empty_repository)


@pytest.fixture
def task_service_with_data(repository_with_tasks):
    """Provide a TaskService with sample data."""
    return TaskService(repository_with_tasks)
