"""Tag model for database."""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING, List
from .task_tag import TaskTag

if TYPE_CHECKING:
    from .user import User
    from .task import Task


class Tag(SQLModel, table=True):
    """Tag model for categorizing tasks."""

    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, index=True)
    color: Optional[str] = Field(default=None, max_length=7)  # Hex color code

    # Foreign key
    user_id: int = Field(foreign_key="users.id", default=1, index=True)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tags")
    tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTag)
