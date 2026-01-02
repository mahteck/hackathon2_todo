"""Pydantic schemas for task validation and serialization."""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from app.models.task import PriorityEnum


class TagSchema(BaseModel):
    """Schema for tag representation in responses."""

    id: int
    name: str
    color: Optional[str] = None

    model_config = {"from_attributes": True}


class TaskBase(BaseModel):
    """Base task schema with common fields."""

    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    priority: PriorityEnum = PriorityEnum.MEDIUM
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not just whitespace."""
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    tags: List[str] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    """Schema for updating an existing task (all fields optional)."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[PriorityEnum] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not just whitespace if provided."""
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip() if v else None


class TaskResponse(TaskBase):
    """Schema for task in responses."""

    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: int
    tags: List[TagSchema]

    model_config = {"from_attributes": True}


class TagCreate(BaseModel):
    """Schema for creating a new tag."""

    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field(None, max_length=7)

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        """Validate tag name is not just whitespace."""
        if not v.strip():
            raise ValueError('Tag name cannot be empty')
        return v.strip().lower()  # Normalize to lowercase
