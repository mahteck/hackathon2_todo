"""Task model for database."""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING, List
from enum import Enum
from .task_tag import TaskTag

if TYPE_CHECKING:
    from .user import User
    from .tag import Tag


class PriorityEnum(str, Enum):
    """Priority levels for tasks."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task(SQLModel, table=True):
    """Task model with all Phase II fields."""

    __tablename__ = "tasks"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Core fields
    title: str = Field(max_length=200, index=True)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False, index=True)

    # New Phase II fields
    priority: str = Field(default=PriorityEnum.MEDIUM.value, index=True)
    due_date: Optional[datetime] = Field(default=None, nullable=True, index=True)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign keys
    user_id: int = Field(foreign_key="users.id", index=True, default=1)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tasks")
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model=TaskTag)
