"""
Custom exceptions for the Todo application.

Defines domain-specific exception hierarchy for better error handling
and user-friendly error messages.
"""


class TodoAppError(Exception):
    """Base exception for all Todo app errors."""
    pass


class ValidationError(TodoAppError):
    """
    Raised when input validation fails.

    Examples: empty title, title too long, description too long.
    """
    pass


class TaskNotFoundError(TodoAppError):
    """
    Raised when a task ID doesn't exist in storage.

    Attributes:
        task_id: The ID that was not found
    """

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class InvalidTaskIdError(TodoAppError):
    """
    Raised when task ID format is invalid.

    Examples: non-numeric ID, negative ID, zero ID.

    Attributes:
        value: The invalid value provided
    """

    def __init__(self, value: str):
        self.value = value
        super().__init__("Invalid task ID: must be a positive integer")
