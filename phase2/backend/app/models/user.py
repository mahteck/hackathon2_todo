"""User model for database."""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING, List

if TYPE_CHECKING:
    from .task import Task
    from .tag import Tag


class User(SQLModel, table=True):
    """User model - placeholder for Phase II (single user hardcoded)."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, index=True)
    email: str = Field(max_length=100, unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")
    tags: List["Tag"] = Relationship(back_populates="user")
