"""Seed database with sample data for development."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.database import async_session
from app.models.user import User
from app.models.tag import Tag
from app.models.task import Task, TaskTag, PriorityEnum


async def seed_database():
    """Seed database with sample data."""
    async with async_session() as session:
        # Check if user already exists
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.id == 1))
        existing_user = result.scalar_one_or_none()

        if not existing_user:
            # Create default user
            user = User(
                id=1,
                username="default_user",
                email="user@example.com",
                created_at=datetime.utcnow()
            )
            session.add(user)
            print("✓ Created default user")
        else:
            print("✓ Default user already exists")

        # Create tags
        tags_data = [
            {"name": "personal", "color": "#3B82F6"},
            {"name": "work", "color": "#EF4444"},
            {"name": "urgent", "color": "#F59E0B"},
            {"name": "shopping", "color": "#10B981"},
        ]

        tags_created = []
        for tag_data in tags_data:
            result = await session.execute(
                select(Tag).where(Tag.name == tag_data["name"], Tag.user_id == 1)
            )
            existing_tag = result.scalar_one_or_none()

            if not existing_tag:
                tag = Tag(**tag_data, user_id=1)
                session.add(tag)
                tags_created.append(tag_data["name"])
            else:
                print(f"✓ Tag '{tag_data['name']}' already exists")

        if tags_created:
            print(f"✓ Created tags: {', '.join(tags_created)}")

        await session.commit()

        # Create sample tasks
        tasks_data = [
            {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, vegetables",
                "priority": PriorityEnum.HIGH.value,
                "due_date": datetime.utcnow() + timedelta(days=2),
                "user_id": 1,
                "tag_names": ["personal", "shopping"]
            },
            {
                "title": "Finish project report",
                "description": "Complete Q4 analysis and presentation",
                "priority": PriorityEnum.MEDIUM.value,
                "completed": True,
                "user_id": 1,
                "tag_names": ["work"]
            },
            {
                "title": "Call dentist",
                "description": "Schedule annual checkup",
                "priority": PriorityEnum.LOW.value,
                "user_id": 1,
                "tag_names": ["personal"]
            },
            {
                "title": "Review pull requests",
                "description": "Check team's code submissions",
                "priority": PriorityEnum.HIGH.value,
                "due_date": datetime.utcnow() + timedelta(hours=6),
                "user_id": 1,
                "tag_names": ["work", "urgent"]
            },
        ]

        tasks_created = []
        for task_data in tasks_data:
            tag_names = task_data.pop("tag_names", [])

            # Check if task already exists (by title)
            result = await session.execute(
                select(Task).where(Task.title == task_data["title"], Task.user_id == 1)
            )
            existing_task = result.scalar_one_or_none()

            if not existing_task:
                task = Task(**task_data)
                session.add(task)
                await session.flush()  # Get task ID

                # Link tags
                for tag_name in tag_names:
                    result = await session.execute(
                        select(Tag).where(Tag.name == tag_name, Tag.user_id == 1)
                    )
                    tag = result.scalar_one()
                    task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
                    session.add(task_tag)

                tasks_created.append(task_data["title"])
            else:
                print(f"✓ Task '{task_data['title']}' already exists")

        if tasks_created:
            print(f"✓ Created tasks: {', '.join(tasks_created)}")

        await session.commit()

        print("\n✅ Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_database())
