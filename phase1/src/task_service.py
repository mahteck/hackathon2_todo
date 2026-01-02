"""
Business logic layer for task operations.

Contains all domain validation, business rules, and orchestration
of repository calls. No direct storage access.
"""
from datetime import datetime
from typing import Optional

from src.models import Task, MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH
from src.task_repository import TaskRepository
from src.exceptions import ValidationError, TaskNotFoundError


class TaskService:
    """
    Service layer for task management operations.

    Handles business logic, validation, and coordinates repository calls.
    """

    def __init__(self, repository: TaskRepository) -> None:
        """
        Initialize service with repository.

        Args:
            repository: TaskRepository instance for data access
        """
        self.repository = repository

    def _validate_title(self, title: str) -> str:
        """
        Validate and normalize task title.

        Args:
            title: Raw title string

        Returns:
            Stripped title

        Raises:
            ValidationError: If title is empty or too long
        """
        stripped = title.strip()
        if not stripped:
            raise ValidationError("Task title cannot be empty")
        if len(stripped) > MAX_TITLE_LENGTH:
            raise ValidationError(
                f"Task title cannot exceed {MAX_TITLE_LENGTH} characters "
                f"(got {len(stripped)})"
            )
        return stripped

    def _validate_description(self, description: str) -> str:
        """
        Validate task description.

        Args:
            description: Description string

        Returns:
            Description (unchanged)

        Raises:
            ValidationError: If description is too long
        """
        if len(description) > MAX_DESCRIPTION_LENGTH:
            raise ValidationError(
                f"Task description cannot exceed {MAX_DESCRIPTION_LENGTH} characters "
                f"(got {len(description)})"
            )
        return description

    def _generate_timestamp(self) -> str:
        """
        Generate ISO 8601 timestamp for current time.

        Returns:
            Timestamp string in ISO 8601 format
        """
        return datetime.now().isoformat()

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Create a new task with validation.

        Args:
            title: Task title (required, 1-200 characters)
            description: Task description (optional, 0-1000 characters)

        Returns:
            Created Task object

        Raises:
            ValidationError: If title or description validation fails

        Examples:
            >>> service.add_task("Buy groceries")
            >>> service.add_task("Finish report", "Q4 analysis")
        """
        # Validate inputs
        validated_title = self._validate_title(title)
        validated_description = self._validate_description(description)

        # Generate ID and timestamps
        task_id = self.repository.generate_id()
        timestamp = self._generate_timestamp()

        # Create task object
        task: Task = {
            "id": task_id,
            "title": validated_title,
            "description": validated_description,
            "completed": False,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        # Store and return
        return self.repository.create(task)

    def get_all_tasks(self) -> list[Task]:
        """
        Retrieve all tasks sorted by ID.

        Returns:
            List of all tasks, sorted by ID ascending

        Examples:
            >>> tasks = service.get_all_tasks()
            >>> print(f"Total tasks: {len(tasks)}")
        """
        return self.repository.find_all()

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Retrieve a specific task by ID.

        Args:
            task_id: ID of task to retrieve

        Returns:
            Task object

        Raises:
            TaskNotFoundError: If task ID doesn't exist

        Examples:
            >>> task = service.get_task_by_id(1)
            >>> print(task["title"])
        """
        task = self.repository.find_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """
        Update task title and/or description.

        Args:
            task_id: ID of task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task ID doesn't exist
            ValidationError: If no fields provided or validation fails

        Examples:
            >>> service.update_task(1, title="New Title")
            >>> service.update_task(1, description="New Description")
            >>> service.update_task(1, title="Title", description="Desc")
        """
        # Validate at least one field provided
        if title is None and description is None:
            raise ValidationError(
                "Must provide at least one field to update (title or description)"
            )

        # Retrieve existing task
        task = self.get_task_by_id(task_id)  # Raises TaskNotFoundError if not found

        # Validate and update title if provided
        if title is not None:
            task["title"] = self._validate_title(title)

        # Validate and update description if provided
        if description is not None:
            task["description"] = self._validate_description(description)

        # Update timestamp
        task["updated_at"] = self._generate_timestamp()

        # Store and return
        return self.repository.update(task_id, task)

    def delete_task(self, task_id: int) -> Task:
        """
        Delete a task permanently.

        Args:
            task_id: ID of task to delete

        Returns:
            The deleted Task object (for confirmation message)

        Raises:
            TaskNotFoundError: If task ID doesn't exist

        Examples:
            >>> deleted = service.delete_task(1)
            >>> print(f"Deleted: {deleted['title']}")
        """
        # Retrieve task first (for return value and validation)
        task = self.get_task_by_id(task_id)  # Raises TaskNotFoundError if not found

        # Delete from repository
        self.repository.delete(task_id)

        return task

    def complete_task(self, task_id: int) -> Task:
        """
        Mark a task as completed.

        Args:
            task_id: ID of task to complete

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task ID doesn't exist

        Note:
            Idempotent - marking an already-completed task as complete
            is allowed and updates the timestamp.

        Examples:
            >>> task = service.complete_task(1)
            >>> print(f"Status: {task['completed']}")  # True
        """
        # Retrieve task
        task = self.get_task_by_id(task_id)

        # Update completion status
        task["completed"] = True
        task["updated_at"] = self._generate_timestamp()

        # Store and return
        return self.repository.update(task_id, task)

    def uncomplete_task(self, task_id: int) -> Task:
        """
        Mark a task as incomplete.

        Args:
            task_id: ID of task to mark incomplete

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task ID doesn't exist

        Note:
            Idempotent - marking an already-incomplete task as incomplete
            is allowed and updates the timestamp.

        Examples:
            >>> task = service.uncomplete_task(1)
            >>> print(f"Status: {task['completed']}")  # False
        """
        # Retrieve task
        task = self.get_task_by_id(task_id)

        # Update completion status
        task["completed"] = False
        task["updated_at"] = self._generate_timestamp()

        # Store and return
        return self.repository.update(task_id, task)
