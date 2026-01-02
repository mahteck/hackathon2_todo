# Phase II Implementation Plan - Full-Stack Web Todo App

**Project:** Evolution of Todo
**Phase:** II - Web Application
**Plan Version:** 1.0.0
**Status:** Ready for Task Breakdown
**Parent Documents:**
- [Global Constitution](../CONSTITUTION.md)
- [Phase II Constitution](./CONSTITUTION.md)
- [Phase II Specification](./SPECIFICATION.md)

---

## Plan Overview

### Objectives
1. Build RESTful API backend with FastAPI and PostgreSQL
2. Create responsive web UI with Next.js and TypeScript
3. Implement all Phase I features via web interface
4. Add Phase II features: priorities, tags, filters, due dates
5. Achieve ≥80% test coverage on backend
6. Deliver production-ready full-stack application

### Execution Strategy
- **Backend-First**: Build and test API before frontend
- **Incremental**: Deliver working features step-by-step
- **Test-Driven**: Write tests alongside implementation
- **Type-Safe**: Full TypeScript + Python type hints
- **Code Generation**: All production code via Claude Code from specs

### Duration Estimate
- **Backend Foundation**: Steps 1-3 (Setup, Models, Core API)
- **Frontend Foundation**: Steps 4-5 (Setup, Basic UI)
- **Feature Implementation**: Steps 6-8 (Forms, Tags, Filters)
- **Quality & Polish**: Steps 9-10 (Tests, Documentation)

---

## Implementation Steps

---

### **Step 1: Backend Project Setup & Database Connection**

**Type:** 🤖 **CODE GENERATION** (Claude Code Implementation)

#### Goal
Initialize FastAPI backend with SQLModel, establish Neon PostgreSQL connection, and set up development environment.

#### Inputs from Spec
- [SPECIFICATION.md § Backend API Specification](./SPECIFICATION.md#backend-api-specification)
- [SPECIFICATION.md § Database Schema](./SPECIFICATION.md#database-schema)
- [CONSTITUTION.md § Technology Stack](./CONSTITUTION.md#technology-stack)

#### Implementation Tasks

##### 1.1: Create Backend Directory Structure
```
phase2/backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── database.py          # Database connection
│   ├── config.py            # Configuration
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           └── __init__.py
│   └── services/
│       └── __init__.py
├── alembic/
│   └── versions/
├── tests/
│   └── __init__.py
├── requirements.txt
├── .env.example
├── alembic.ini
└── README.md
```

##### 1.2: Generate `requirements.txt`
```txt
# FastAPI and server
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
python-dotenv>=1.0.0

# Database
sqlmodel>=0.0.14
asyncpg>=0.29.0
alembic>=1.12.0
psycopg2-binary>=2.9.9

# Validation and serialization
pydantic>=2.5.0
pydantic-settings>=2.1.0

# CORS
python-multipart>=0.0.6

# Development
pytest>=7.4.0
pytest-asyncio>=0.21.0
httpx>=0.25.0
pytest-cov>=4.1.0
ruff>=0.1.0
mypy>=1.7.0
```

##### 1.3: Create `app/config.py`
```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # App
    APP_NAME: str = "Todo API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

##### 1.4: Create `app/database.py`
```python
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Async engine for SQLModel
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def init_db():
    """Create database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

##### 1.5: Create `app/main.py`
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Evolution of Todo - Phase II API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}

@app.get("/")
async def root():
    return {
        "message": "Todo API - Phase II",
        "docs": "/docs",
        "health": "/health"
    }
```

##### 1.6: Create `.env.example`
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/todo_db
CORS_ORIGINS=http://localhost:3000
DEBUG=True
LOG_LEVEL=INFO
```

##### 1.7: Initialize Alembic
```bash
alembic init alembic
```

Configure `alembic.ini` and `alembic/env.py` for SQLModel.

#### Expected Artifacts
- ✅ Backend directory structure created
- ✅ `requirements.txt` with all dependencies
- ✅ `app/config.py` with settings management
- ✅ `app/database.py` with async SQLModel setup
- ✅ `app/main.py` with FastAPI app and CORS
- ✅ `.env.example` template
- ✅ Alembic initialized

#### Acceptance Criteria
- [ ] FastAPI app runs: `uvicorn app.main:app --reload`
- [ ] Health endpoint accessible: `GET /health` returns 200
- [ ] API docs accessible: `/docs` shows Swagger UI
- [ ] Database connection successful (can connect to Neon)
- [ ] CORS headers present in responses
- [ ] All imports resolve correctly
- [ ] No linting errors: `ruff check app/`
- [ ] Type checking passes: `mypy app/`

#### Validation Commands
```bash
cd phase2/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# In another terminal:
curl http://localhost:8000/health
```

---

### **Step 2: Database Models & Migrations**

**Type:** 🤖 **CODE GENERATION** (Claude Code Implementation)

#### Goal
Implement SQLModel models for Task, Tag, TaskTag, and User with complete schema, relationships, and Alembic migrations.

#### Inputs from Spec
- [SPECIFICATION.md § Database Schema § SQLModel Definitions](./SPECIFICATION.md#database-schema)
- [SPECIFICATION.md § Data Model](./SPECIFICATION.md#data-model)

#### Implementation Tasks

##### 2.1: Create `app/models/user.py`
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.tag import Tag

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, index=True)
    email: str = Field(max_length=100, unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user")
    tags: list["Tag"] = Relationship(back_populates="user")
```

##### 2.2: Create `app/models/tag.py`
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User

class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, index=True)
    color: Optional[str] = Field(default=None, max_length=7)
    user_id: int = Field(foreign_key="users.id", default=1)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tags")
    tasks: list["Task"] = Relationship(back_populates="tags", link_model="TaskTag")
```

##### 2.3: Create `app/models/task.py`
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from app.models.tag import Tag
    from app.models.user import User

class PriorityEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Core fields
    title: str = Field(max_length=200, index=True)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False, index=True)

    # Phase II fields
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM, index=True)
    due_date: Optional[datetime] = Field(default=None, nullable=True, index=True)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key
    user_id: int = Field(foreign_key="users.id", index=True, default=1)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tasks")
    tags: list["Tag"] = Relationship(back_populates="tasks", link_model=TaskTag)
```

##### 2.4: Create `app/models/__init__.py`
```python
from app.models.user import User
from app.models.tag import Tag
from app.models.task import Task, TaskTag, PriorityEnum

__all__ = ["User", "Tag", "Task", "TaskTag", "PriorityEnum"]
```

##### 2.5: Create Initial Migration
```bash
alembic revision --autogenerate -m "Initial schema"
```

Edit generated migration to:
- Add indexes as specified in [SPECIFICATION.md § Database Indexes](./SPECIFICATION.md#database-schema)
- Insert default user (id=1)
- Add constraints

##### 2.6: Create Seed Data Script
```python
# scripts/seed_data.py
from app.database import async_session
from app.models import User, Tag, Task, PriorityEnum
from datetime import datetime

async def seed():
    async with async_session() as session:
        # Create default user if not exists
        user = User(id=1, username="default_user", email="user@example.com")
        session.add(user)

        # Create sample tags
        tags = [
            Tag(name="personal", color="#3B82F6", user_id=1),
            Tag(name="work", color="#EF4444", user_id=1),
            Tag(name="urgent", color="#F59E0B", user_id=1),
        ]
        for tag in tags:
            session.add(tag)

        await session.commit()
        print("✅ Database seeded")

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed())
```

#### Expected Artifacts
- ✅ `app/models/user.py` - User model
- ✅ `app/models/tag.py` - Tag model
- ✅ `app/models/task.py` - Task, TaskTag models, PriorityEnum
- ✅ `app/models/__init__.py` - Module exports
- ✅ Alembic migration file (001_initial.py)
- ✅ `scripts/seed_data.py` - Development data

#### Acceptance Criteria
- [ ] All models have proper type hints
- [ ] Relationships defined correctly
- [ ] Migration runs successfully: `alembic upgrade head`
- [ ] Migration rollback works: `alembic downgrade -1`
- [ ] Seed script creates default user and tags
- [ ] Database schema matches specification
- [ ] Indexes created as specified
- [ ] Type checking passes on models

#### Validation Commands
```bash
cd phase2/backend
alembic upgrade head
python scripts/seed_data.py
# Verify in database:
psql $DATABASE_URL -c "SELECT * FROM users;"
psql $DATABASE_URL -c "SELECT * FROM tags;"
```

---

### **Step 3: Pydantic Schemas & Core API Endpoints**

**Type:** 🤖 **CODE GENERATION** (Claude Code Implementation)

#### Goal
Create Pydantic validation schemas and implement core CRUD API endpoints for tasks.

#### Inputs from Spec
- [SPECIFICATION.md § Task Schemas](./SPECIFICATION.md#task-schemas-pydantic-models)
- [SPECIFICATION.md § API Endpoints](./SPECIFICATION.md#api-endpoints-detailed)

#### Implementation Tasks

##### 3.1: Create `app/schemas/task.py`
```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from app.models.task import PriorityEnum

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    priority: PriorityEnum = PriorityEnum.MEDIUM
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

class TaskCreate(TaskBase):
    tags: list[str] = Field(default_factory=list)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[PriorityEnum] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    tags: Optional[list[str]] = None

class TagSchema(BaseModel):
    id: int
    name: str
    color: Optional[str] = None

    class Config:
        from_attributes = True

class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: int
    tags: list[TagSchema]

    class Config:
        from_attributes = True
```

##### 3.2: Create `app/schemas/common.py`
```python
from pydantic import BaseModel
from typing import Any, Optional

class SuccessResponse(BaseModel):
    data: Any
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    error: dict
```

##### 3.3: Create `app/services/task_service.py`
```python
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task, Tag, TaskTag, PriorityEnum
from app.schemas.task import TaskCreate, TaskUpdate
from datetime import datetime
from typing import Optional

class TaskService:
    @staticmethod
    async def create_task(
        session: AsyncSession,
        task_data: TaskCreate,
        user_id: int = 1
    ) -> Task:
        """Create new task with tags."""
        # Create task
        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            due_date=task_data.due_date,
            user_id=user_id
        )
        session.add(task)
        await session.flush()  # Get task.id

        # Handle tags
        if task_data.tags:
            for tag_name in task_data.tags:
                # Find or create tag
                result = await session.execute(
                    select(Tag).where(Tag.name == tag_name, Tag.user_id == user_id)
                )
                tag = result.scalar_one_or_none()

                if not tag:
                    tag = Tag(name=tag_name, user_id=user_id)
                    session.add(tag)
                    await session.flush()

                # Link tag to task
                task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
                session.add(task_tag)

        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def list_tasks(
        session: AsyncSession,
        user_id: int = 1,
        status: str = "all",
        priority: Optional[PriorityEnum] = None,
        tags: Optional[list[str]] = None,
        sort_by: str = "created_desc",
        limit: int = 100,
        offset: int = 0
    ) -> tuple[list[Task], int]:
        """List tasks with filters."""
        # Build query
        query = select(Task).where(Task.user_id == user_id)

        # Filter by status
        if status == "active":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        # Filter by priority
        if priority:
            query = query.where(Task.priority == priority)

        # TODO: Filter by tags (requires join)

        # Sort
        if sort_by == "created_desc":
            query = query.order_by(Task.created_at.desc())
        elif sort_by == "created_asc":
            query = query.order_by(Task.created_at.asc())
        elif sort_by == "priority_desc":
            # Custom order: high, medium, low
            query = query.order_by(Task.priority.desc())
        elif sort_by == "due_asc":
            query = query.order_by(Task.due_date.asc())
        elif sort_by == "title_asc":
            query = query.order_by(Task.title.asc())

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Paginate
        query = query.offset(offset).limit(limit)

        # Execute
        result = await session.execute(query)
        tasks = result.scalars().all()

        return tasks, total

    @staticmethod
    async def get_task(
        session: AsyncSession,
        task_id: int,
        user_id: int = 1
    ) -> Optional[Task]:
        """Get task by ID."""
        result = await session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_task(
        session: AsyncSession,
        task_id: int,
        task_data: TaskUpdate,
        user_id: int = 1
    ) -> Optional[Task]:
        """Update task."""
        task = await TaskService.get_task(session, task_id, user_id)
        if not task:
            return None

        # Update fields
        update_data = task_data.model_dump(exclude_unset=True)
        tags = update_data.pop('tags', None)

        for key, value in update_data.items():
            setattr(task, key, value)

        task.updated_at = datetime.utcnow()

        # Update tags if provided
        if tags is not None:
            # Remove existing tags
            await session.execute(
                delete(TaskTag).where(TaskTag.task_id == task_id)
            )

            # Add new tags
            for tag_name in tags:
                result = await session.execute(
                    select(Tag).where(Tag.name == tag_name, Tag.user_id == user_id)
                )
                tag = result.scalar_one_or_none()

                if not tag:
                    tag = Tag(name=tag_name, user_id=user_id)
                    session.add(tag)
                    await session.flush()

                task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
                session.add(task_tag)

        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def delete_task(
        session: AsyncSession,
        task_id: int,
        user_id: int = 1
    ) -> bool:
        """Delete task."""
        task = await TaskService.get_task(session, task_id, user_id)
        if not task:
            return False

        await session.delete(task)
        await session.commit()
        return True
```

##### 3.4: Create `app/api/v1/endpoints/tasks.py`
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.common import SuccessResponse
from app.services.task_service import TaskService
from typing import Optional
from app.models.task import PriorityEnum

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=SuccessResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create a new task."""
    task = await TaskService.create_task(session, task_data)
    return SuccessResponse(
        data=TaskResponse.from_orm(task),
        message="Task created successfully"
    )

@router.get("", response_model=SuccessResponse)
async def list_tasks(
    status: str = "all",
    priority: Optional[PriorityEnum] = None,
    sort: str = "created_desc",
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(get_session)
):
    """List tasks with filtering and sorting."""
    tasks, total = await TaskService.list_tasks(
        session, status=status, priority=priority,
        sort_by=sort, limit=limit, offset=offset
    )

    return SuccessResponse(
        data={
            "tasks": [TaskResponse.from_orm(t) for t in tasks],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    )

@router.get("/{task_id}", response_model=SuccessResponse)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get task by ID."""
    task = await TaskService.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return SuccessResponse(data=TaskResponse.from_orm(task))

@router.patch("/{task_id}", response_model=SuccessResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update task."""
    task = await TaskService.update_task(session, task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return SuccessResponse(
        data=TaskResponse.from_orm(task),
        message="Task updated successfully"
    )

@router.delete("/{task_id}", response_model=SuccessResponse)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete task."""
    deleted = await TaskService.delete_task(session, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return SuccessResponse(data=None, message="Task deleted successfully")
```

##### 3.5: Update `app/main.py` to include router
```python
from app.api.v1.endpoints import tasks

app.include_router(tasks.router, prefix="/api/v1")
```

#### Expected Artifacts
- ✅ `app/schemas/task.py` - Pydantic schemas
- ✅ `app/schemas/common.py` - Response schemas
- ✅ `app/services/task_service.py` - Business logic
- ✅ `app/api/v1/endpoints/tasks.py` - API routes
- ✅ Updated `app/main.py` with router

#### Acceptance Criteria
- [ ] All 5 task endpoints accessible
- [ ] `/docs` shows complete API documentation
- [ ] POST /api/v1/tasks creates task: `201 Created`
- [ ] GET /api/v1/tasks lists tasks: `200 OK`
- [ ] GET /api/v1/tasks/{id} returns task: `200 OK`
- [ ] PATCH /api/v1/tasks/{id} updates task: `200 OK`
- [ ] DELETE /api/v1/tasks/{id} deletes task: `200 OK`
- [ ] Validation errors return `422 Unprocessable Entity`
- [ ] Not found returns `404 Not Found`
- [ ] Type checking passes

#### Validation Commands
```bash
# Test with curl
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","priority":"high","tags":["test"]}'

curl http://localhost:8000/api/v1/tasks

curl http://localhost:8000/api/v1/tasks/1

curl -X PATCH http://localhost:8000/api/v1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

curl -X DELETE http://localhost:8000/api/v1/tasks/1
```

---

### **Step 4: Frontend Project Setup & API Client**

**Type:** 🤖 **CODE GENERATION** (Claude Code Implementation)

#### Goal
Initialize Next.js 14 frontend with TypeScript, Tailwind CSS, and create type-safe API client.

#### Inputs from Spec
- [SPECIFICATION.md § Frontend Specification](./SPECIFICATION.md#frontend-specification)
- [SPECIFICATION.md § TypeScript Types](./SPECIFICATION.md#typescript-types)
- [SPECIFICATION.md § API Client](./SPECIFICATION.md#api-client)

#### Implementation Tasks

##### 4.1: Create Next.js Project
```bash
cd phase2
npx create-next-app@latest frontend \
  --typescript \
  --tailwind \
  --app \
  --no-src-dir \
  --import-alias "@/*"
```

##### 4.2: Install Additional Dependencies
```bash
cd frontend
npm install date-fns
npm install -D @types/node
```

##### 4.3: Create `lib/types.ts`
```typescript
export enum Priority {
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low',
}

export interface Tag {
  id: number;
  name: string;
  color?: string;
}

export interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  priority: Priority;
  due_date?: string;
  tags: Tag[];
  created_at: string;
  updated_at: string;
  user_id: number;
}

export interface TaskCreateInput {
  title: string;
  description?: string;
  priority?: Priority;
  due_date?: string;
  tags?: string[];
}

export interface TaskUpdateInput {
  title?: string;
  description?: string;
  priority?: Priority;
  completed?: boolean;
  due_date?: string;
  tags?: string[];
}

export interface FilterParams {
  status?: 'all' | 'active' | 'completed';
  priority?: Priority;
  tag?: string[];
  sort?: string;
}

export interface TaskListResponse {
  data: {
    tasks: Task[];
    total: number;
    limit: number;
    offset: number;
  };
}

export interface TaskResponse {
  data: Task;
  message?: string;
}
```

##### 4.4: Create `lib/api.ts`
```typescript
import { Task, TaskCreateInput, TaskUpdateInput, Tag, FilterParams } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class ApiError extends Error {
  constructor(public status: number, message: string, public details?: any) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new ApiError(
      response.status,
      data.error?.message || data.detail || 'An error occurred',
      data.error?.details
    );
  }

  return data;
}

export const taskApi = {
  list: async (params: FilterParams = {}) => {
    const searchParams = new URLSearchParams();
    if (params.status) searchParams.set('status', params.status);
    if (params.priority) searchParams.set('priority', params.priority);
    if (params.tag) params.tag.forEach(t => searchParams.append('tag', t));
    if (params.sort) searchParams.set('sort', params.sort);

    const query = searchParams.toString();
    return fetchAPI<{ data: { tasks: Task[]; total: number; limit: number; offset: number } }>(
      `/api/v1/tasks${query ? `?${query}` : ''}`
    );
  },

  get: (id: number) =>
    fetchAPI<{ data: Task }>(`/api/v1/tasks/${id}`),

  create: (data: TaskCreateInput) =>
    fetchAPI<{ data: Task; message: string }>('/api/v1/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: number, data: TaskUpdateInput) =>
    fetchAPI<{ data: Task; message: string }>(`/api/v1/tasks/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  delete: (id: number) =>
    fetchAPI<{ message: string }>(`/api/v1/tasks/${id}`, {
      method: 'DELETE',
    }),
};

export const tagApi = {
  list: () =>
    fetchAPI<{ data: Tag[] }>('/api/v1/tags'),

  create: (data: { name: string; color?: string }) =>
    fetchAPI<{ data: Tag }>('/api/v1/tags', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};
```

##### 4.5: Create `.env.local`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

##### 4.6: Update `tailwind.config.ts`
Add custom colors for priorities:
```typescript
const config: Config = {
  theme: {
    extend: {
      colors: {
        priority: {
          high: '#EF4444',
          medium: '#F59E0B',
          low: '#3B82F6',
        },
      },
    },
  },
};
```

#### Expected Artifacts
- ✅ Next.js project initialized
- ✅ `lib/types.ts` - TypeScript interfaces
- ✅ `lib/api.ts` - API client functions
- ✅ `.env.local` - Environment configuration
- ✅ Tailwind configured with custom colors
- ✅ `package.json` with dependencies

#### Acceptance Criteria
- [ ] Next.js dev server runs: `npm run dev`
- [ ] TypeScript compiles without errors
- [ ] API client types match backend schemas
- [ ] Environment variable accessible
- [ ] Tailwind CSS working

#### Validation Commands
```bash
cd phase2/frontend
npm run dev
# Visit http://localhost:3000
npm run build  # Verify TypeScript compiles
```

---

### **Step 5: Task List Page with Filters**

**Type:** 🤖 **CODE GENERATION** (Claude Code Implementation)

#### Goal
Build home page that lists tasks with filtering, sorting, and basic UI components.

#### Inputs from Spec
- [SPECIFICATION.md § TaskList Component](./SPECIFICATION.md#component-specifications)
- [SPECIFICATION.md § TaskCard Component](./SPECIFICATION.md#component-specifications)
- [SPECIFICATION.md § Filtering & Sorting](./SPECIFICATION.md#feature-3-filtering--sorting)

#### Implementation Tasks

##### 5.1: Create `components/TaskCard.tsx`
Client component with checkbox toggle, priority badge, tags display.

##### 5.2: Create `components/PriorityBadge.tsx`
Display priority with colored badge.

##### 5.3: Create `components/TaskList.tsx`
Server component that fetches and displays tasks.

##### 5.4: Create `components/FilterPanel.tsx`
Client component with filter controls (status, priority, sort).

##### 5.5: Create `components/Navigation.tsx`
App header with "New Task" button.

##### 5.6: Create `app/layout.tsx`
Root layout with navigation.

##### 5.7: Create `app/page.tsx`
Home page that renders TaskList with filters from URL search params.

#### Expected Artifacts
- ✅ `components/TaskCard.tsx`
- ✅ `components/PriorityBadge.tsx`
- ✅ `components/TaskList.tsx`
- ✅ `components/FilterPanel.tsx`
- ✅ `components/Navigation.tsx`
- ✅ `app/layout.tsx`
- ✅ `app/page.tsx`

#### Acceptance Criteria
- [ ] Home page displays list of tasks
- [ ] Each task shows title, description, priority, tags
- [ ] Checkbox toggles complete/incomplete (optimistic UI)
- [ ] Filter panel allows filtering by status and priority
- [ ] Sort dropdown changes task order
- [ ] Active filters persist in URL
- [ ] Mobile-responsive layout
- [ ] Loading state while fetching

#### Validation Commands
```bash
# Visit http://localhost:3000
# Create tasks via API (curl or Swagger)
# Verify they appear in UI
# Test filters and sorting
```

---

### **Step 6: Create & Edit Task Forms**

**Type:** 🤖 **CODE GENERATION** (Claude Code Implementation)

#### Goal
Implement task creation and editing forms with validation, tag input, date picker.

#### Inputs from Spec
- [SPECIFICATION.md § TaskForm Component](./SPECIFICATION.md#component-specifications)
- [SPECIFICATION.md § Flow 2: Create Task](./SPECIFICATION.md#ui-flows)

#### Implementation Tasks

##### 6.1: Create `components/TaskForm.tsx`
Client component with form fields, validation, submission.

##### 6.2: Create `components/TagInput.tsx`
Tag autocomplete with chip display.

##### 6.3: Create `components/PrioritySelector.tsx`
Priority dropdown/radio buttons.

##### 6.4: Create `components/DueDatePicker.tsx`
Date input component.

##### 6.5: Create `app/tasks/new/page.tsx`
Page with TaskForm for creating new task.

##### 6.6: Create `app/tasks/[id]/page.tsx`
Page with TaskForm pre-filled for editing.

#### Expected Artifacts
- ✅ `components/TaskForm.tsx`
- ✅ `components/TagInput.tsx`
- ✅ `components/PrioritySelector.tsx`
- ✅ `components/DueDatePicker.tsx`
- ✅ `app/tasks/new/page.tsx`
- ✅ `app/tasks/[id]/page.tsx`

#### Acceptance Criteria
- [ ] "New Task" button navigates to `/tasks/new`
- [ ] Form validates title (required, ≤200 chars)
- [ ] Form validates description (≤1000 chars)
- [ ] Priority selector works (default: medium)
- [ ] Tag input autocompletes existing tags
- [ ] Due date picker allows selecting date
- [ ] Submit button disabled while submitting
- [ ] Success redirects to home with toast
- [ ] Validation errors display inline
- [ ] Edit page pre-fills form with task data
- [ ] Cancel button goes back

#### Validation Commands
```bash
# Click "New Task"
# Fill form and submit
# Verify task created
# Click task title
# Edit and save
# Verify task updated
```

---

### **Step 7: Tags API & Management**

**Type:** 🤖 **CODE GENERATION** (Claude Code Implementation)

#### Goal
Implement tags API endpoint and optional tag management page.

#### Inputs from Spec
- [SPECIFICATION.md § Tag Model](./SPECIFICATION.md#tag-model)
- [SPECIFICATION.md § List Tags Endpoint](./SPECIFICATION.md#6-list-tags)

#### Implementation Tasks

##### 7.1: Create `app/api/v1/endpoints/tags.py`
```python
from fastapi import APIRouter, Depends
from app.database import get_session
from app.models import Tag

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("")
async def list_tags(session: AsyncSession = Depends(get_session)):
    """List all tags."""
    result = await session.execute(select(Tag).where(Tag.user_id == 1))
    tags = result.scalars().all()
    return SuccessResponse(data=[TagSchema.from_orm(t) for t in tags])

@router.post("")
async def create_tag(
    tag_data: TagCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create new tag."""
    tag = Tag(**tag_data.dict(), user_id=1)
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return SuccessResponse(data=TagSchema.from_orm(tag), message="Tag created")
```

##### 7.2: Include tags router in main.py

##### 7.3: (Optional) Create `app/tags/page.tsx`
Page for managing tags (list, create, delete).

#### Expected Artifacts
- ✅ `app/api/v1/endpoints/tags.py`
- ✅ Tags router in main.py
- ✅ (Optional) `app/tags/page.tsx`

#### Acceptance Criteria
- [ ] GET /api/v1/tags returns list of tags
- [ ] POST /api/v1/tags creates new tag
- [ ] TagInput component fetches tags on mount
- [ ] New tags can be created inline in TaskForm

---

### **Step 8: Error Handling & Loading States**

**Type:** 🤖 **CODE GENERATION** (Claude Code Implementation)

#### Goal
Add comprehensive error handling, loading states, and user feedback (toasts).

#### Inputs from Spec
- [SPECIFICATION.md § Error Handling](./SPECIFICATION.md#error-handling)

#### Implementation Tasks

##### 8.1: Create `components/ui/Toast.tsx`
Toast notification component for success/error messages.

##### 8.2: Create `components/ui/Loader.tsx`
Loading spinner component.

##### 8.3: Create `lib/utils.ts`
Utility functions for error formatting.

##### 8.4: Add loading states to TaskList

##### 8.5: Add error boundaries to pages

##### 8.6: Implement toast notifications in TaskForm

#### Expected Artifacts
- ✅ `components/ui/Toast.tsx`
- ✅ `components/ui/Loader.tsx`
- ✅ `lib/utils.ts`
- ✅ Loading states in components
- ✅ Error handling in API calls

#### Acceptance Criteria
- [ ] Loading spinner shown while fetching tasks
- [ ] API errors display user-friendly messages
- [ ] Success toasts on create/update/delete
- [ ] Error toasts on API failures
- [ ] Form shows validation errors inline
- [ ] Network errors handled gracefully

---

### **Step 9: Backend Testing**

**Type:** 🤖 **CODE GENERATION** (Claude Code Implementation)

#### Goal
Write comprehensive backend tests for API endpoints and business logic.

#### Inputs from Spec
- [SPECIFICATION.md § Backend Tests](./SPECIFICATION.md#backend-tests)

#### Implementation Tasks

##### 9.1: Create `tests/conftest.py`
Pytest fixtures for database session, test client.

##### 9.2: Create `tests/test_task_service.py`
Unit tests for TaskService methods.

##### 9.3: Create `tests/test_api_tasks.py`
Integration tests for task API endpoints.

##### 9.4: Create `tests/test_models.py`
Tests for SQLModel models.

#### Expected Artifacts
- ✅ `tests/conftest.py`
- ✅ `tests/test_task_service.py`
- ✅ `tests/test_api_tasks.py`
- ✅ `tests/test_models.py`

#### Acceptance Criteria
- [ ] All tests pass: `pytest tests/ -v`
- [ ] Test coverage ≥80%: `pytest --cov=app --cov-report=term-missing`
- [ ] API tests cover all endpoints
- [ ] Service tests cover business logic
- [ ] Model tests verify relationships

#### Validation Commands
```bash
cd phase2/backend
pytest tests/ -v
pytest --cov=app --cov-report=html
```

---

### **Step 10: Documentation & Deployment Prep**

**Type:** 🤖 **CODE GENERATION** (Claude Code Implementation)

#### Goal
Complete README, API documentation, and deployment configuration.

#### Inputs from Spec
- [SPECIFICATION.md § Deployment & Configuration](./SPECIFICATION.md#deployment--configuration)

#### Implementation Tasks

##### 10.1: Update `phase2/backend/README.md`
- Setup instructions
- API documentation link
- Environment variables
- Running tests

##### 10.2: Update `phase2/frontend/README.md`
- Setup instructions
- Environment variables
- Development workflow

##### 10.3: Create `docker-compose.yml`
Local development environment with Postgres, backend, frontend.

##### 10.4: Create deployment documentation

#### Expected Artifacts
- ✅ `backend/README.md`
- ✅ `frontend/README.md`
- ✅ `docker-compose.yml`
- ✅ Deployment guide

#### Acceptance Criteria
- [ ] README has complete setup instructions
- [ ] docker-compose.yml works for local dev
- [ ] Environment variables documented
- [ ] API documentation accessible

---

## Milestones & Dependencies

### Milestone 1: Backend Foundation (Steps 1-3)
**Goal:** RESTful API with database operational
**Deliverables:**
- [ ] FastAPI app running with CORS
- [ ] Database models and migrations
- [ ] All 5 task endpoints working
- [ ] OpenAPI docs accessible

**Dependencies:** None
**Estimated Effort:** ~35% of backend work

---

### Milestone 2: Frontend Foundation (Steps 4-5)
**Goal:** Basic UI displaying tasks
**Deliverables:**
- [ ] Next.js app running
- [ ] API client implemented
- [ ] Task list page with filters
- [ ] Mobile-responsive layout

**Dependencies:** Milestone 1 complete (need API)
**Estimated Effort:** ~30% of frontend work

---

### Milestone 3: Full CRUD UI (Steps 6-8)
**Goal:** Complete user workflows
**Deliverables:**
- [ ] Create/edit task forms
- [ ] Tag management
- [ ] Error handling and loading states
- [ ] User feedback (toasts)

**Dependencies:** Milestone 2 complete
**Estimated Effort:** ~50% of frontend work

---

### Milestone 4: Testing & Quality (Steps 9-10)
**Goal:** Production-ready application
**Deliverables:**
- [ ] Backend tests ≥80% coverage
- [ ] Frontend component tests
- [ ] Complete documentation
- [ ] Deployment ready

**Dependencies:** Milestones 1-3 complete
**Estimated Effort:** ~20% of total work

---

## Testing Strategy

### Backend Tests (pytest)
- **Unit Tests**: Services, models (≥80% coverage target)
- **Integration Tests**: API endpoints (all 7 endpoints)
- **Database Tests**: Migrations, relationships

### Frontend Tests (Jest + Playwright)
- **Component Tests**: Critical components (TaskCard, TaskForm)
- **E2E Tests**: Main user flows (create, edit, filter)

### Manual Testing Checklist
- [ ] Create task with all fields
- [ ] Edit task and verify changes
- [ ] Delete task with confirmation
- [ ] Filter by status, priority, tags
- [ ] Sort tasks multiple ways
- [ ] Toggle complete/incomplete
- [ ] Tag autocomplete works
- [ ] Due date picker works
- [ ] Mobile responsive design
- [ ] Error messages clear
- [ ] Loading states shown

---

## Success Criteria

### Phase II Complete When:

#### Functionality
- ✅ All Phase I features work via web
- ✅ All Phase II features implemented (priorities, tags, filters, due dates)
- ✅ CRUD operations work end-to-end
- ✅ Filtering and sorting functional

#### Quality
- ✅ Backend test coverage ≥80%
- ✅ All API endpoints documented
- ✅ TypeScript strict mode passes
- ✅ No console errors in production build
- ✅ Mobile-responsive design

#### User Experience
- ✅ Intuitive UI
- ✅ Fast response times (<2s page loads)
- ✅ Clear error messages
- ✅ Loading states prevent confusion
- ✅ Success feedback on actions

#### Documentation
- ✅ README with setup instructions
- ✅ API documentation (OpenAPI)
- ✅ Environment variables documented
- ✅ Deployment guide available

---

## Risk Management

### Risk 1: Database Connection Issues
**Mitigation:** Test Neon connection early, have local Postgres fallback

### Risk 2: CORS Problems
**Mitigation:** Configure CORS in Step 1, test immediately

### Risk 3: Type Mismatches (Backend ↔ Frontend)
**Mitigation:** Define types early, validate against API responses

### Risk 4: Performance with Many Tasks
**Mitigation:** Implement pagination, test with 100+ tasks

---

## Development Workflow

### Daily Workflow
1. Pull latest from repo
2. Backend: `uvicorn app.main:app --reload`
3. Frontend: `npm run dev`
4. Make changes per task
5. Test manually + automated
6. Commit when acceptance criteria met

### Code Review Checklist
- [ ] Matches specification exactly
- [ ] Type hints/TypeScript complete
- [ ] Error handling comprehensive
- [ ] Tests passing
- [ ] Documentation updated

---

**Plan Version:** 1.0.0
**Created:** 2025-12-26
**Status:** APPROVED FOR TASK BREAKDOWN

**Next Command:** `/sp.tasks phase2`

This will decompose each step into atomic, executable tasks for Claude Code.
