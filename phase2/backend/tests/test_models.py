"""Tests for database models."""
import pytest
from datetime import datetime

from app.models import User, Tag, Task, TaskTag, PriorityEnum


@pytest.mark.asyncio
async def test_create_user(db_session):
    """Test creating a user."""
    user = User(username="testuser", email="test@example.com")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert isinstance(user.created_at, datetime)


@pytest.mark.asyncio
async def test_create_tag(db_session):
    """Test creating a tag."""
    tag = Tag(name="personal", color="#3B82F6", user_id=1)
    db_session.add(tag)
    await db_session.commit()
    await db_session.refresh(tag)

    assert tag.id is not None
    assert tag.name == "personal"
    assert tag.color == "#3B82F6"
    assert tag.user_id == 1


@pytest.mark.asyncio
async def test_create_task(db_session):
    """Test creating a task."""
    task = Task(
        title="Test Task",
        description="Test description",
        priority=PriorityEnum.HIGH.value,
        user_id=1
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    assert task.id is not None
    assert task.title == "Test Task"
    assert task.description == "Test description"
    assert task.priority == "high"
    assert task.completed is False
    assert task.user_id == 1
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


@pytest.mark.asyncio
async def test_task_with_tags(db_session):
    """Test task with tag relationships."""
    # Create tag
    tag = Tag(name="work", color="#EF4444", user_id=1)
    db_session.add(tag)
    await db_session.flush()

    # Create task
    task = Task(title="Work Task", user_id=1)
    db_session.add(task)
    await db_session.flush()

    # Link task and tag
    task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
    db_session.add(task_tag)
    await db_session.commit()

    # Verify relationship
    await db_session.refresh(task)
    assert len(task.tags) == 1
    assert task.tags[0].name == "work"


@pytest.mark.asyncio
async def test_priority_enum():
    """Test PriorityEnum values."""
    assert PriorityEnum.HIGH.value == "high"
    assert PriorityEnum.MEDIUM.value == "medium"
    assert PriorityEnum.LOW.value == "low"
