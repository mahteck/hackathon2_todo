"""
Data models and type definitions for the Todo application.

This module defines the core Task entity and validation constants.
"""
from typing import TypedDict


# Validation constants
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000


class Task(TypedDict):
    """
    Represents a single Todo task.

    Attributes:
        id: Unique integer identifier (auto-generated, immutable)
        title: Short task title (required, 1-200 characters)
        description: Optional detailed description (0-1000 characters)
        completed: Boolean flag indicating completion status
        created_at: ISO 8601 timestamp of task creation (immutable)
        updated_at: ISO 8601 timestamp of last modification
    """
    id: int
    title: str
    description: str
    completed: bool
    created_at: str
    updated_at: str
