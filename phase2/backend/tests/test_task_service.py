"""Tests for TaskService."""
import pytest
from datetime import datetime, timedelta

from app.services.task_service import TaskService, TagService
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.task import PriorityEnum


@pytest.mark.asyncio
async def test_create_task_basic(db_session):
    """Test creating a basic task."""
    task_data = TaskCreate(
        title="Test Task",
        description="Test description",
        priority=PriorityEnum.HIGH
    )

    task = await TaskService.create_task(db_session, task_data)

    assert task.id is not None
    assert task.title == "Test Task"
    assert task.description == "Test description"
    assert task.priority == "high"
    assert task.completed is False
    assert len(task.tags) == 0


@pytest.mark.asyncio
async def test_create_task_with_tags(db_session):
    """Test creating a task with tags."""
    task_data = TaskCreate(
        title="Tagged Task",
        tags=["work", "urgent"]
    )

    task = await TaskService.create_task(db_session, task_data)

    assert task.id is not None
    assert len(task.tags) == 2
    assert {tag.name for tag in task.tags} == {"work", "urgent"}


@pytest.mark.asyncio
async def test_list_tasks_all(db_session):
    """Test listing all tasks."""
    # Create tasks
    await TaskService.create_task(
        db_session,
        TaskCreate(title="Task 1", priority=PriorityEnum.HIGH)
    )
    await TaskService.create_task(
        db_session,
        TaskCreate(title="Task 2", priority=PriorityEnum.MEDIUM)
    )

    tasks, total = await TaskService.list_tasks(db_session)

    assert total == 2
    assert len(tasks) == 2


@pytest.mark.asyncio
async def test_list_tasks_filter_status(db_session):
    """Test filtering tasks by status."""
    # Create tasks
    task1 = await TaskService.create_task(
        db_session,
        TaskCreate(title="Active Task")
    )
    task2 = await TaskService.create_task(
        db_session,
        TaskCreate(title="Completed Task")
    )

    # Mark one as completed
    await TaskService.update_task(
        db_session,
        task2.id,
        TaskUpdate(completed=True)
    )

    # Filter active
    tasks, total = await TaskService.list_tasks(db_session, status="active")
    assert total == 1
    assert tasks[0].title == "Active Task"

    # Filter completed
    tasks, total = await TaskService.list_tasks(db_session, status="completed")
    assert total == 1
    assert tasks[0].title == "Completed Task"


@pytest.mark.asyncio
async def test_list_tasks_filter_priority(db_session):
    """Test filtering tasks by priority."""
    await TaskService.create_task(
        db_session,
        TaskCreate(title="High Priority", priority=PriorityEnum.HIGH)
    )
    await TaskService.create_task(
        db_session,
        TaskCreate(title="Low Priority", priority=PriorityEnum.LOW)
    )

    tasks, total = await TaskService.list_tasks(
        db_session,
        priority=PriorityEnum.HIGH
    )

    assert total == 1
    assert tasks[0].title == "High Priority"


@pytest.mark.asyncio
async def test_get_task_by_id(db_session):
    """Test getting a task by ID."""
    created_task = await TaskService.create_task(
        db_session,
        TaskCreate(title="Find Me")
    )

    task = await TaskService.get_task_by_id(db_session, created_task.id)

    assert task is not None
    assert task.id == created_task.id
    assert task.title == "Find Me"


@pytest.mark.asyncio
async def test_get_task_not_found(db_session):
    """Test getting a non-existent task."""
    task = await TaskService.get_task_by_id(db_session, 999)
    assert task is None


@pytest.mark.asyncio
async def test_update_task(db_session):
    """Test updating a task."""
    task = await TaskService.create_task(
        db_session,
        TaskCreate(title="Original Title", priority=PriorityEnum.LOW)
    )

    updated_task = await TaskService.update_task(
        db_session,
        task.id,
        TaskUpdate(title="Updated Title", priority=PriorityEnum.HIGH, completed=True)
    )

    assert updated_task is not None
    assert updated_task.title == "Updated Title"
    assert updated_task.priority == "high"
    assert updated_task.completed is True


@pytest.mark.asyncio
async def test_delete_task(db_session):
    """Test deleting a task."""
    task = await TaskService.create_task(
        db_session,
        TaskCreate(title="To Be Deleted")
    )

    result = await TaskService.delete_task(db_session, task.id)
    assert result is True

    # Verify deletion
    deleted_task = await TaskService.get_task_by_id(db_session, task.id)
    assert deleted_task is None


@pytest.mark.asyncio
async def test_delete_task_not_found(db_session):
    """Test deleting a non-existent task."""
    result = await TaskService.delete_task(db_session, 999)
    assert result is False


@pytest.mark.asyncio
async def test_create_tag(db_session):
    """Test creating a tag."""
    tag = await TagService.create_tag(db_session, "personal", "#3B82F6")

    assert tag.id is not None
    assert tag.name == "personal"
    assert tag.color == "#3B82F6"


@pytest.mark.asyncio
async def test_list_tags(db_session):
    """Test listing tags."""
    await TagService.create_tag(db_session, "work", "#EF4444")
    await TagService.create_tag(db_session, "personal", "#3B82F6")

    tags = await TagService.list_tags(db_session)

    assert len(tags) == 2
    assert {tag.name for tag in tags} == {"work", "personal"}
