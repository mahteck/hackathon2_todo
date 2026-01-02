"""
Data access layer for task storage.

Manages in-memory storage of tasks using a dictionary.
Provides CRUD operations without business logic.
"""
from typing import Optional

from src.models import Task


class TaskRepository:
    """
    Manages in-memory storage and retrieval of tasks.

    Storage is a dictionary mapping task IDs to Task objects.
    IDs are auto-incremented starting from 1.
    """

    def __init__(self) -> None:
        """Initialize empty storage and ID counter."""
        self._storage: dict[int, Task] = {}
        self._next_id: int = 1

    def generate_id(self) -> int:
        """
        Generate unique sequential task ID.

        Returns:
            Next available task ID (auto-incremented)
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def create(self, task: Task) -> Task:
        """
        Store a new task in memory.

        Args:
            task: Task object to store (must have 'id' field)

        Returns:
            The stored task
        """
        self._storage[task["id"]] = task
        return task

    def find_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve task by ID.

        Args:
            task_id: ID of task to retrieve

        Returns:
            Task if found, None otherwise
        """
        return self._storage.get(task_id)

    def find_all(self) -> list[Task]:
        """
        Retrieve all tasks sorted by ID.

        Returns:
            List of all tasks, sorted by ID ascending
        """
        return [self._storage[task_id] for task_id in sorted(self._storage.keys())]

    def update(self, task_id: int, task: Task) -> Task:
        """
        Update existing task in storage.

        Args:
            task_id: ID of task to update
            task: Updated task object

        Returns:
            Updated task
        """
        self._storage[task_id] = task
        return task

    def delete(self, task_id: int) -> bool:
        """
        Delete task from storage.

        Args:
            task_id: ID of task to delete

        Returns:
            True if task existed and was deleted, False otherwise
        """
        if task_id in self._storage:
            del self._storage[task_id]
            return True
        return False

    def clear(self) -> None:
        """
        Clear all tasks from storage.

        Useful for testing. Resets ID counter to 1.
        """
        self._storage.clear()
        self._next_id = 1
