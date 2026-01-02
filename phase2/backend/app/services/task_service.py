"""Task service with business logic for CRUD operations."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from typing import Optional, List, Tuple
from datetime import datetime

from app.models.task import Task, TaskTag, PriorityEnum
from app.models.tag import Tag
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """Service class for task-related business logic."""

    @staticmethod
    async def create_task(session: AsyncSession, task_data: TaskCreate, user_id: int = 1) -> Task:
        """Create a new task with tags."""
        # Create task
        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority.value,
            due_date=task_data.due_date,
            user_id=user_id
        )

        session.add(task)
        await session.flush()  # Get task ID

        # Handle tags
        if task_data.tags:
            for tag_name in task_data.tags:
                # Find or create tag
                result = await session.execute(
                    select(Tag).where(
                        and_(
                            func.lower(Tag.name) == tag_name.lower(),
                            Tag.user_id == user_id
                        )
                    )
                )
                tag = result.scalar_one_or_none()

                if not tag:
                    # Generate a random color for new tags
                    colors = ["#3B82F6", "#EF4444", "#F59E0B", "#10B981", "#8B5CF6", "#EC4899"]
                    import random
                    tag = Tag(name=tag_name.lower(), color=random.choice(colors), user_id=user_id)
                    session.add(tag)
                    await session.flush()

                # Link tag to task
                task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
                session.add(task_tag)

        await session.commit()

        # Reload task with relationships
        result = await session.execute(
            select(Task)
            .options(selectinload(Task.tags))
            .where(Task.id == task.id)
        )
        return result.scalar_one()

    @staticmethod
    async def list_tasks(
        session: AsyncSession,
        user_id: int = 1,
        status: str = "all",
        priority: Optional[PriorityEnum] = None,
        tags: Optional[List[str]] = None,
        sort_by: str = "created_desc",
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[Task], int]:
        """List tasks with filtering and sorting."""
        # Build query
        query = select(Task).options(selectinload(Task.tags)).where(Task.user_id == user_id)

        # Filter by status
        if status == "active":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        # Filter by priority
        if priority:
            query = query.where(Task.priority == priority.value)

        # Filter by tags
        if tags:
            # Tasks that have ANY of the specified tags
            query = query.join(TaskTag).join(Tag).where(
                func.lower(Tag.name).in_([t.lower() for t in tags])
            ).distinct()

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Apply sorting
        if sort_by == "created_asc":
            query = query.order_by(Task.created_at.asc())
        elif sort_by == "priority_desc":
            # High > Medium > Low
            priority_order = {"high": 0, "medium": 1, "low": 2}
            query = query.order_by(
                Task.priority.desc()  # This will work with the string values
            )
        elif sort_by == "due_asc":
            # Null values last
            query = query.order_by(Task.due_date.asc().nullslast())
        elif sort_by == "title_asc":
            query = query.order_by(Task.title.asc())
        else:  # created_desc (default)
            query = query.order_by(Task.created_at.desc())

        # Apply pagination
        query = query.limit(limit).offset(offset)

        # Execute query
        result = await session.execute(query)
        tasks = result.scalars().unique().all()

        return list(tasks), total

    @staticmethod
    async def get_task_by_id(session: AsyncSession, task_id: int, user_id: int = 1) -> Optional[Task]:
        """Get a specific task by ID."""
        result = await session.execute(
            select(Task)
            .options(selectinload(Task.tags))
            .where(and_(Task.id == task_id, Task.user_id == user_id))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_task(
        session: AsyncSession,
        task_id: int,
        task_data: TaskUpdate,
        user_id: int = 1
    ) -> Optional[Task]:
        """Update an existing task."""
        # Get task
        result = await session.execute(
            select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        )
        task = result.scalar_one_or_none()

        if not task:
            return None

        # Update fields if provided
        update_data = task_data.model_dump(exclude_unset=True, exclude={'tags'})

        for field, value in update_data.items():
            if field == 'priority' and value:
                setattr(task, field, value.value)
            else:
                setattr(task, field, value)

        task.updated_at = datetime.utcnow()

        # Handle tags update if provided
        if task_data.tags is not None:
            # Remove existing tag associations
            await session.execute(
                select(TaskTag).where(TaskTag.task_id == task_id)
            )
            await session.execute(
                TaskTag.__table__.delete().where(TaskTag.task_id == task_id)
            )

            # Add new tags
            for tag_name in task_data.tags:
                result = await session.execute(
                    select(Tag).where(
                        and_(
                            func.lower(Tag.name) == tag_name.lower(),
                            Tag.user_id == user_id
                        )
                    )
                )
                tag = result.scalar_one_or_none()

                if not tag:
                    import random
                    colors = ["#3B82F6", "#EF4444", "#F59E0B", "#10B981", "#8B5CF6", "#EC4899"]
                    tag = Tag(name=tag_name.lower(), color=random.choice(colors), user_id=user_id)
                    session.add(tag)
                    await session.flush()

                task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
                session.add(task_tag)

        await session.commit()

        # Reload with relationships
        result = await session.execute(
            select(Task)
            .options(selectinload(Task.tags))
            .where(Task.id == task_id)
        )
        return result.scalar_one()

    @staticmethod
    async def delete_task(session: AsyncSession, task_id: int, user_id: int = 1) -> bool:
        """Delete a task."""
        result = await session.execute(
            select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        )
        task = result.scalar_one_or_none()

        if not task:
            return False

        await session.delete(task)
        await session.commit()
        return True


class TagService:
    """Service class for tag-related business logic."""

    @staticmethod
    async def list_tags(session: AsyncSession, user_id: int = 1) -> List[Tag]:
        """List all tags for a user."""
        result = await session.execute(
            select(Tag).where(Tag.user_id == user_id).order_by(Tag.name)
        )
        return list(result.scalars().all())

    @staticmethod
    async def create_tag(session: AsyncSession, name: str, color: Optional[str] = None, user_id: int = 1) -> Tag:
        """Create a new tag."""
        # Check if tag already exists
        result = await session.execute(
            select(Tag).where(
                and_(
                    func.lower(Tag.name) == name.lower(),
                    Tag.user_id == user_id
                )
            )
        )
        existing_tag = result.scalar_one_or_none()

        if existing_tag:
            return existing_tag

        # Create new tag
        if not color:
            import random
            colors = ["#3B82F6", "#EF4444", "#F59E0B", "#10B981", "#8B5CF6", "#EC4899"]
            color = random.choice(colors)

        tag = Tag(name=name.lower(), color=color, user_id=user_id)
        session.add(tag)
        await session.commit()
        await session.refresh(tag)
        return tag
