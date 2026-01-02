"""TaskTag join table model."""
from sqlmodel import SQLModel, Field


class TaskTag(SQLModel, table=True):
    """Join table for many-to-many relationship between tasks and tags."""

    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)
