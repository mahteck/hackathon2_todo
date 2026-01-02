# Phase II Specification - Full-Stack Web Todo App

**Project:** Evolution of Todo
**Phase:** II - Web Application
**Version:** 1.0.0
**Status:** Draft for Approval
**Parent Documents:**
- [Global Constitution](../CONSTITUTION.md)
- [Phase I Specification](../phase1/SPECIFICATION.md)
- [Phase II Constitution](./CONSTITUTION.md)

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Backend API Specification](#backend-api-specification)
3. [Database Schema](#database-schema)
4. [Frontend Specification](#frontend-specification)
5. [Feature Specifications](#feature-specifications)
6. [Integration & Data Flow](#integration--data-flow)
7. [Testing Requirements](#testing-requirements)
8. [Deployment & Configuration](#deployment--configuration)
9. [Acceptance Criteria](#acceptance-criteria)

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                        │
│                   (Next.js 14 App Router)                   │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Pages     │  │  Components  │  │  Server Actions  │  │
│  │  (Routes)   │  │  (UI Logic)  │  │   (API Calls)    │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓ HTTP/JSON ↑
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│                   (Python 3.10+ Async)                      │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Routes    │  │   Services   │  │   Repositories   │  │
│  │ (Endpoints) │  │ (Bus. Logic) │  │  (Data Access)   │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓ SQL ↑
┌─────────────────────────────────────────────────────────────┐
│                PostgreSQL (Neon Managed)                    │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  tasks   │  │   tags   │  │task_tags │  │  users   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 14 (App Router) | React-based SSR/SSG framework |
| | TypeScript | Type-safe JavaScript |
| | Tailwind CSS | Utility-first styling |
| | React Server Components | Server-side rendering |
| **Backend** | FastAPI | High-performance async Python API |
| | Pydantic v2 | Data validation and serialization |
| | SQLModel | ORM combining SQLAlchemy + Pydantic |
| **Database** | PostgreSQL (Neon) | Managed relational database |
| | Alembic | Database migration tool |
| **Testing** | pytest + httpx | Backend API testing |
| | Jest + RTL | Frontend component testing |
| **DevOps** | Docker Compose | Local development environment |
| | uvicorn | ASGI server for FastAPI |

---

## Backend API Specification

### API Design Principles

1. **RESTful**: Resources identified by URLs, actions by HTTP verbs
2. **Versioned**: All endpoints under `/api/v1/` prefix
3. **Consistent**: Standard response formats across all endpoints
4. **Validated**: Pydantic models enforce schemas
5. **Documented**: OpenAPI schema auto-generated at `/docs`

### Base Configuration

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="Evolution of Todo - Phase II API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Response Schemas

#### Success Response (Pydantic)

```python
from pydantic import BaseModel
from typing import Any, Optional

class SuccessResponse(BaseModel):
    data: Any
    message: Optional[str] = None

# Example
{
  "data": { "id": 1, "title": "Task" },
  "message": "Task created successfully"
}
```

#### Error Response (Pydantic)

```python
class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str

class ErrorResponse(BaseModel):
    error: dict
    # error = {
    #   "code": "VALIDATION_ERROR",
    #   "message": "Invalid input",
    #   "details": [{"field": "title", "message": "Required"}]
    # }
```

### Task Schemas (Pydantic Models)

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum

class PriorityEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

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

class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: int
    tags: list[TagSchema]

    class Config:
        from_attributes = True  # For SQLModel compatibility
```

### API Endpoints (Detailed)

#### 1. Create Task

**Endpoint:** `POST /api/v1/tasks`

**Request:**
```python
# Request body (TaskCreate schema)
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "high",
  "due_date": "2025-12-31T23:59:59Z",
  "tags": ["personal", "shopping"]
}
```

**Implementation:**
```python
@app.post("/api/v1/tasks", response_model=SuccessResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new task.

    - **title**: Required, 1-200 characters
    - **description**: Optional, max 1000 characters
    - **priority**: high, medium (default), or low
    - **due_date**: Optional ISO 8601 datetime
    - **tags**: Array of tag names (creates new tags if needed)
    """
    # Business logic
    new_task = await task_service.create_task(session, task_data)

    return SuccessResponse(
        data=new_task,
        message="Task created successfully"
    )
```

**Response:** `201 Created`
```json
{
  "data": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "priority": "high",
    "due_date": "2025-12-31T23:59:59Z",
    "tags": [
      {"id": 1, "name": "personal", "color": "#3B82F6"},
      {"id": 2, "name": "shopping", "color": "#10B981"}
    ],
    "created_at": "2025-12-26T10:00:00Z",
    "updated_at": "2025-12-26T10:00:00Z",
    "user_id": 1
  },
  "message": "Task created successfully"
}
```

**Validation Errors:** `422 Unprocessable Entity`
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "title",
        "message": "Title cannot be empty"
      }
    ]
  }
}
```

---

#### 2. List Tasks

**Endpoint:** `GET /api/v1/tasks`

**Query Parameters:**
```python
class TaskFilterParams(BaseModel):
    status: Optional[str] = "all"  # all, active, completed
    priority: Optional[PriorityEnum] = None
    tag: Optional[list[str]] = None  # Can specify multiple
    sort: Optional[str] = "created_desc"  # created_desc, created_asc, priority_desc, due_asc, title_asc
    limit: int = 100  # Max 1000
    offset: int = 0
```

**Implementation:**
```python
@app.get("/api/v1/tasks", response_model=SuccessResponse)
async def list_tasks(
    status: str = "all",
    priority: Optional[PriorityEnum] = None,
    tag: Optional[list[str]] = Query(None),
    sort: str = "created_desc",
    limit: int = Query(100, le=1000),
    offset: int = 0,
    session: AsyncSession = Depends(get_session)
):
    """
    List tasks with filtering and sorting.

    Filters:
    - **status**: all (default), active, completed
    - **priority**: Filter by priority level
    - **tag**: Filter by tag name (can specify multiple)

    Sorting:
    - created_desc (default), created_asc, priority_desc, due_asc, title_asc

    Pagination:
    - **limit**: Max results (default 100, max 1000)
    - **offset**: Skip N results
    """
    tasks, total = await task_service.list_tasks(
        session,
        status=status,
        priority=priority,
        tags=tag,
        sort_by=sort,
        limit=limit,
        offset=offset,
        user_id=1  # Hardcoded for Phase II
    )

    return SuccessResponse(
        data={
            "tasks": tasks,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    )
```

**Response:** `200 OK`
```json
{
  "data": {
    "tasks": [
      {
        "id": 1,
        "title": "Buy groceries",
        "completed": false,
        "priority": "high",
        "tags": [{"id": 1, "name": "personal", "color": "#3B82F6"}],
        "due_date": "2025-12-31T23:59:59Z",
        "created_at": "2025-12-26T10:00:00Z",
        "updated_at": "2025-12-26T10:00:00Z"
      }
    ],
    "total": 1,
    "limit": 100,
    "offset": 0
  }
}
```

---

#### 3. Get Task by ID

**Endpoint:** `GET /api/v1/tasks/{task_id}`

**Implementation:**
```python
@app.get("/api/v1/tasks/{task_id}", response_model=SuccessResponse)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Retrieve a specific task by ID."""
    task = await task_service.get_task_by_id(session, task_id, user_id=1)

    if not task:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Task with ID {task_id} not found"
                }
            }
        )

    return SuccessResponse(data=task)
```

**Response:** `200 OK` (same as task object in list response)

**Error:** `404 Not Found`

---

#### 4. Update Task

**Endpoint:** `PATCH /api/v1/tasks/{task_id}`

**Request:** (all fields optional)
```json
{
  "title": "Updated title",
  "description": "New description",
  "priority": "medium",
  "completed": true,
  "due_date": "2025-12-31T23:59:59Z",
  "tags": ["work", "important"]
}
```

**Implementation:**
```python
@app.patch("/api/v1/tasks/{task_id}", response_model=SuccessResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_session)
):
    """
    Update a task (partial update).

    All fields are optional. Only provided fields will be updated.
    """
    # Validate at least one field provided
    if not any(task_data.model_dump(exclude_unset=True).values()):
        raise HTTPException(
            status_code=422,
            detail={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "At least one field must be provided"
                }
            }
        )

    updated_task = await task_service.update_task(
        session, task_id, task_data, user_id=1
    )

    return SuccessResponse(
        data=updated_task,
        message="Task updated successfully"
    )
```

**Response:** `200 OK` (updated task object)

---

#### 5. Delete Task

**Endpoint:** `DELETE /api/v1/tasks/{task_id}`

**Implementation:**
```python
@app.delete("/api/v1/tasks/{task_id}", response_model=SuccessResponse)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete a task permanently."""
    await task_service.delete_task(session, task_id, user_id=1)

    return SuccessResponse(
        data=None,
        message="Task deleted successfully"
    )
```

**Response:** `200 OK`
```json
{
  "data": null,
  "message": "Task deleted successfully"
}
```

---

#### 6. List Tags

**Endpoint:** `GET /api/v1/tags`

**Implementation:**
```python
@app.get("/api/v1/tags", response_model=SuccessResponse)
async def list_tags(
    session: AsyncSession = Depends(get_session)
):
    """List all tags for the current user."""
    tags = await tag_service.list_tags(session, user_id=1)

    return SuccessResponse(data=tags)
```

**Response:** `200 OK`
```json
{
  "data": [
    {"id": 1, "name": "personal", "color": "#3B82F6"},
    {"id": 2, "name": "work", "color": "#EF4444"},
    {"id": 3, "name": "urgent", "color": "#F59E0B"}
  ]
}
```

---

#### 7. Create Tag

**Endpoint:** `POST /api/v1/tags`

**Request:**
```json
{
  "name": "urgent",
  "color": "#F59E0B"
}
```

**Response:** `201 Created`
```json
{
  "data": {
    "id": 3,
    "name": "urgent",
    "color": "#F59E0B"
  },
  "message": "Tag created successfully"
}
```

---

## Database Schema

### SQLModel Definitions

#### Task Model (Complete)

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .tag import Tag
    from .user import User

class PriorityEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Core fields (from Phase I)
    title: str = Field(max_length=200, index=True)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False, index=True)

    # New Phase II fields
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM, index=True)
    due_date: Optional[datetime] = Field(default=None, nullable=True, index=True)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign keys
    user_id: int = Field(foreign_key="users.id", index=True, default=1)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tasks")
    tags: list["Tag"] = Relationship(
        back_populates="tasks",
        link_model=TaskTag
    )
```

#### Tag Model

```python
class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True, index=True)
    color: Optional[str] = Field(default=None, max_length=7)  # Hex color

    # Foreign key
    user_id: int = Field(foreign_key="users.id", default=1)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tags")
    tasks: list["Task"] = Relationship(
        back_populates="tags",
        link_model=TaskTag
    )
```

#### TaskTag (Link Model)

```python
class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True, ondelete="CASCADE")
    tag_id: int = Field(foreign_key="tags.id", primary_key=True, ondelete="CASCADE")
```

#### User Model (Placeholder)

```python
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

### Database Migrations (Alembic)

#### Initial Migration

```python
# alembic/versions/001_initial.py
"""Initial schema

Revision ID: 001
Revises:
Create Date: 2025-12-26
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('email', sa.String(100), unique=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.String(1000), nullable=False, default=''),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('priority', sa.String(10), nullable=False, default='medium'),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
    )

    # Create tags table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(50), unique=True, nullable=False),
        sa.Column('color', sa.String(7), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
    )

    # Create task_tags junction table
    op.create_table(
        'task_tags',
        sa.Column('task_id', sa.Integer(), sa.ForeignKey('tasks.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('tag_id', sa.Integer(), sa.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    )

    # Create indexes
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_completed', 'tasks', ['completed'])
    op.create_index('idx_tasks_priority', 'tasks', ['priority'])
    op.create_index('idx_tasks_due_date', 'tasks', ['due_date'])
    op.create_index('idx_tasks_created_at', 'tasks', ['created_at'])

    op.create_index('idx_tags_name', 'tags', ['name'])
    op.create_index('idx_tags_user_id', 'tags', ['user_id'])

    # Insert default user
    op.execute(
        "INSERT INTO users (id, username, email, created_at) "
        "VALUES (1, 'default_user', 'user@example.com', NOW())"
    )

def downgrade() -> None:
    op.drop_table('task_tags')
    op.drop_table('tags')
    op.drop_table('tasks')
    op.drop_table('users')
```

### Seed Data

```python
# scripts/seed_data.py
async def seed_database(session: AsyncSession):
    """Seed database with sample data for development."""

    # Create tags
    tags_data = [
        Tag(id=1, name="personal", color="#3B82F6", user_id=1),
        Tag(id=2, name="work", color="#EF4444", user_id=1),
        Tag(id=3, name="urgent", color="#F59E0B", user_id=1),
        Tag(id=4, name="shopping", color="#10B981", user_id=1),
    ]

    for tag in tags_data:
        session.add(tag)

    await session.commit()

    # Create sample tasks
    tasks_data = [
        Task(
            title="Buy groceries",
            description="Milk, eggs, bread",
            priority=PriorityEnum.HIGH,
            due_date=datetime(2025, 12, 31, 23, 59, 59),
            user_id=1
        ),
        Task(
            title="Finish project report",
            description="Q4 analysis",
            priority=PriorityEnum.MEDIUM,
            completed=True,
            user_id=1
        ),
        Task(
            title="Call dentist",
            priority=PriorityEnum.LOW,
            user_id=1
        ),
    ]

    for task in tasks_data:
        session.add(task)

    await session.commit()

    # Link tags to tasks
    # Task 1 (groceries) -> personal, shopping
    # Task 2 (report) -> work
    # Task 3 (dentist) -> personal

    print("✅ Database seeded successfully")
```

---

## Frontend Specification

### Project Structure

```
phase2/frontend/
├── app/
│   ├── layout.tsx                    # Root layout
│   ├── page.tsx                      # Home page (task list)
│   ├── tasks/
│   │   ├── new/
│   │   │   └── page.tsx             # Create task page
│   │   └── [id]/
│   │       └── page.tsx             # Task detail/edit page
│   ├── tags/
│   │   └── page.tsx                 # Tag management
│   └── api/
│       └── tasks/
│           └── route.ts             # API route handlers (if needed)
├── components/
│   ├── TaskList.tsx                 # Server component
│   ├── TaskCard.tsx                 # Task item component
│   ├── TaskForm.tsx                 # Client component
│   ├── FilterPanel.tsx              # Client component
│   ├── TagInput.tsx                 # Client component
│   ├── PriorityBadge.tsx           # Priority indicator
│   ├── PrioritySelector.tsx        # Priority dropdown
│   ├── DueDatePicker.tsx           # Date input
│   ├── Navigation.tsx              # Nav bar
│   └── ui/
│       ├── Button.tsx              # Reusable button
│       ├── Input.tsx               # Reusable input
│       ├── Select.tsx              # Reusable select
│       └── Toast.tsx               # Toast notifications
├── lib/
│   ├── api.ts                      # API client functions
│   ├── types.ts                    # TypeScript types
│   └── utils.ts                    # Utility functions
├── public/
│   └── (static assets)
├── .env.local                      # Environment variables
├── next.config.js                  # Next.js configuration
├── tailwind.config.ts              # Tailwind CSS config
├── tsconfig.json                   # TypeScript config
└── package.json                    # Dependencies
```

### TypeScript Types

```typescript
// lib/types.ts

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
  due_date?: string; // ISO 8601
  tags: Tag[];
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
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

export interface FilterParams {
  status?: 'all' | 'active' | 'completed';
  priority?: Priority;
  tag?: string[];
  sort?: string;
}
```

### API Client

```typescript
// lib/api.ts

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
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

  if (!response.ok) {
    const error = await response.json();
    throw new ApiError(
      response.status,
      error.error?.message || 'An error occurred'
    );
  }

  return response.json();
}

// Task API functions
export const taskApi = {
  list: (params: FilterParams = {}) => {
    const searchParams = new URLSearchParams();
    if (params.status) searchParams.set('status', params.status);
    if (params.priority) searchParams.set('priority', params.priority);
    if (params.tag) params.tag.forEach(t => searchParams.append('tag', t));
    if (params.sort) searchParams.set('sort', params.sort);

    const query = searchParams.toString();
    return fetchAPI<TaskListResponse>(
      `/api/v1/tasks${query ? `?${query}` : ''}`
    );
  },

  get: (id: number) =>
    fetchAPI<TaskResponse>(`/api/v1/tasks/${id}`),

  create: (data: TaskCreateInput) =>
    fetchAPI<TaskResponse>('/api/v1/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: number, data: TaskUpdateInput) =>
    fetchAPI<TaskResponse>(`/api/v1/tasks/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  delete: (id: number) =>
    fetchAPI<{ message: string }>(`/api/v1/tasks/${id}`, {
      method: 'DELETE',
    }),
};

// Tag API functions
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

### Component Specifications

#### TaskList (Server Component)

```typescript
// components/TaskList.tsx
import { taskApi } from '@/lib/api';
import TaskCard from './TaskCard';

interface TaskListProps {
  status?: 'all' | 'active' | 'completed';
  priority?: Priority;
  tags?: string[];
  sort?: string;
}

export default async function TaskList({
  status = 'all',
  priority,
  tags,
  sort
}: TaskListProps) {
  const { data } = await taskApi.list({ status, priority, tag: tags, sort });

  if (data.tasks.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p className="text-lg">No tasks found</p>
        <p className="text-sm mt-2">Create your first task to get started</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {data.tasks.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
      <div className="text-sm text-gray-500 text-center mt-4">
        Showing {data.tasks.length} of {data.total} tasks
      </div>
    </div>
  );
}
```

#### TaskCard (Client Component)

```typescript
// components/TaskCard.tsx
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Task } from '@/lib/types';
import { taskApi } from '@/lib/api';
import PriorityBadge from './PriorityBadge';

interface TaskCardProps {
  task: Task;
}

export default function TaskCard({ task }: TaskCardProps) {
  const [completed, setCompleted] = useState(task.completed);
  const [isUpdating, setIsUpdating] = useState(false);

  const handleToggleComplete = async () => {
    setIsUpdating(true);
    const newStatus = !completed;
    setCompleted(newStatus); // Optimistic update

    try {
      await taskApi.update(task.id, { completed: newStatus });
    } catch (error) {
      setCompleted(!newStatus); // Revert on error
      console.error('Failed to update task:', error);
    } finally {
      setIsUpdating(false);
    }
  };

  const isOverdue = task.due_date && new Date(task.due_date) < new Date();

  return (
    <div className="border rounded-lg p-4 hover:shadow-md transition">
      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          checked={completed}
          onChange={handleToggleComplete}
          disabled={isUpdating}
          className="mt-1 h-5 w-5 rounded border-gray-300"
        />

        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <Link
              href={`/tasks/${task.id}`}
              className={`text-lg font-medium hover:text-blue-600 ${
                completed ? 'line-through text-gray-500' : ''
              }`}
            >
              {task.title}
            </Link>
            <PriorityBadge priority={task.priority} />
            {isOverdue && (
              <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded">
                Overdue
              </span>
            )}
          </div>

          {task.description && (
            <p className="text-sm text-gray-600 mb-2">{task.description}</p>
          )}

          <div className="flex items-center gap-2 text-sm text-gray-500">
            {task.due_date && (
              <span>📅 Due: {new Date(task.due_date).toLocaleDateString()}</span>
            )}
            {task.tags.length > 0 && (
              <div className="flex gap-1">
                {task.tags.map((tag) => (
                  <span
                    key={tag.id}
                    className="px-2 py-1 rounded text-xs"
                    style={{ backgroundColor: tag.color + '20', color: tag.color }}
                  >
                    {tag.name}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
```

#### TaskForm (Client Component)

```typescript
// components/TaskForm.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Task, TaskCreateInput, TaskUpdateInput, Priority } from '@/lib/types';
import { taskApi } from '@/lib/api';
import TagInput from './TagInput';
import PrioritySelector from './PrioritySelector';
import DueDatePicker from './DueDatePicker';

interface TaskFormProps {
  task?: Task; // If editing
  onSuccess?: () => void;
}

export default function TaskForm({ task, onSuccess }: TaskFormProps) {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    title: task?.title || '',
    description: task?.description || '',
    priority: task?.priority || Priority.MEDIUM,
    due_date: task?.due_date || '',
    tags: task?.tags.map(t => t.name) || [],
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      if (task) {
        await taskApi.update(task.id, formData);
      } else {
        await taskApi.create(formData);
      }

      onSuccess?.();
      router.push('/');
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div>
        <label className="block text-sm font-medium mb-2">
          Title <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          required
          maxLength={200}
          className="w-full border rounded-lg px-3 py-2"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Description</label>
        <textarea
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          maxLength={1000}
          rows={4}
          className="w-full border rounded-lg px-3 py-2"
        />
      </div>

      <PrioritySelector
        value={formData.priority}
        onChange={(priority) => setFormData({ ...formData, priority })}
      />

      <TagInput
        value={formData.tags}
        onChange={(tags) => setFormData({ ...formData, tags })}
      />

      <DueDatePicker
        value={formData.due_date}
        onChange={(due_date) => setFormData({ ...formData, due_date })}
      />

      <div className="flex gap-3">
        <button
          type="button"
          onClick={() => router.back()}
          className="px-4 py-2 border rounded-lg hover:bg-gray-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={isSubmitting}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {isSubmitting ? 'Saving...' : task ? 'Update Task' : 'Create Task'}
        </button>
      </div>
    </form>
  );
}
```

---

## Feature Specifications

### Feature 1: Task Priorities

**Implementation:**

**Backend:**
- `PriorityEnum` in SQLModel and Pydantic
- Database column with check constraint
- Default to `medium` on creation
- Sortable by priority (high → medium → low)

**Frontend:**
- `PrioritySelector` component (radio buttons or dropdown)
- `PriorityBadge` component with color coding:
  - High: Red background (#FEE2E2), red text (#EF4444)
  - Medium: Yellow background (#FEF3C7), yellow text (#F59E0B)
  - Low: Blue background (#DBEAFE), blue text (#3B82F6)
- Filter by priority in FilterPanel

**Acceptance Criteria:**
- [ ] Can create task with priority (high/medium/low)
- [ ] Priority defaults to medium if not specified
- [ ] Can update task priority
- [ ] Can filter tasks by priority
- [ ] Can sort tasks by priority
- [ ] Priority badge displays correct color
- [ ] API validates priority enum values

---

### Feature 2: Task Tags

**Implementation:**

**Backend:**
- Many-to-many relationship (tasks ↔ tags via task_tags)
- Tag auto-creation when new tag name provided
- Tag reuse when existing tag name provided
- Case-insensitive tag matching
- Tag endpoint for listing/creating tags

**Frontend:**
- `TagInput` component with autocomplete
- Fetch existing tags on mount
- Allow creating new tags inline
- Display tags as colored chips
- Remove tag by clicking X on chip
- Filter by tags (multi-select)

**Acceptance Criteria:**
- [ ] Can add tags to task (new and existing)
- [ ] Tags autocomplete from existing tags
- [ ] Can create new tag on the fly
- [ ] Can remove tag from task
- [ ] Can filter tasks by tag (single or multiple)
- [ ] Tags display with colors
- [ ] Tag management page allows CRUD on tags

---

### Feature 3: Filtering & Sorting

**Implementation:**

**Backend:**
- Query builder in `task_service.list_tasks()`
- Support multiple filters simultaneously
- Sort options: created_desc, created_asc, priority_desc, due_asc, title_asc
- Efficient SQL queries with proper indexes

**Frontend:**
- `FilterPanel` component with:
  - Status buttons: All / Active / Completed
  - Priority dropdown: All / High / Medium / Low
  - Tag multi-select with autocomplete
  - Sort dropdown
- Update URL search params on filter change
- Display active filters as removable chips
- Server component re-renders with new params

**Acceptance Criteria:**
- [ ] Can filter by status (all/active/completed)
- [ ] Can filter by priority
- [ ] Can filter by multiple tags simultaneously
- [ ] Can sort by created date, priority, due date, title
- [ ] Filters persist in URL (shareable links)
- [ ] Active filters displayed as chips
- [ ] Can remove individual filters

---

### Feature 4: Due Dates

**Implementation:**

**Backend:**
- `due_date` column (datetime, nullable)
- Query support for overdue tasks (`WHERE due_date < NOW()`)
- Sort by due date (soonest first)

**Frontend:**
- `DueDatePicker` component (HTML date input or react-datepicker)
- Display due date in TaskCard
- "Overdue" badge for past due dates (red)
- "Due today" indicator
- Filter by due date ranges

**Acceptance Criteria:**
- [ ] Can set due date when creating task
- [ ] Can update due date on existing task
- [ ] Can clear due date
- [ ] Overdue tasks show red "Overdue" badge
- [ ] Can sort by due date (soonest first)
- [ ] Can filter by due date ranges (overdue, due today, due this week)

---

## Integration & Data Flow

### Complete Flow: Create Task

```
1. User fills TaskForm on /tasks/new
   ↓
2. Submit POST /api/v1/tasks with:
   {
     "title": "Buy groceries",
     "priority": "high",
     "tags": ["personal", "shopping"],
     "due_date": "2025-12-31T23:59:59Z"
   }
   ↓
3. FastAPI validates with TaskCreate Pydantic model
   ↓
4. TaskService.create_task() executes:
   - Create Task object
   - Find or create tags by name
   - Link tags to task (TaskTag records)
   - Commit transaction
   ↓
5. Return 201 Created with full task object
   ↓
6. Frontend redirects to / and shows success toast
   ↓
7. TaskList server component re-fetches and displays new task
```

### Complete Flow: Filter Tasks

```
1. User clicks "High Priority" filter button
   ↓
2. FilterPanel updates URL: /?priority=high
   ↓
3. Next.js App Router triggers re-render
   ↓
4. TaskList server component receives { priority: 'high' }
   ↓
5. Calls GET /api/v1/tasks?priority=high
   ↓
6. TaskService.list_tasks() builds SQL query:
   SELECT * FROM tasks WHERE priority = 'high' AND user_id = 1
   ↓
7. Returns filtered tasks
   ↓
8. TaskList renders filtered tasks
   ↓
9. FilterPanel shows "High Priority" as active filter chip
```

---

## Testing Requirements

### Backend Tests

#### Unit Tests (pytest)

```python
# tests/test_task_service.py

@pytest.mark.asyncio
async def test_create_task_with_tags(db_session):
    """Test creating task with tags."""
    task_data = TaskCreate(
        title="Buy groceries",
        priority=PriorityEnum.HIGH,
        tags=["personal", "shopping"]
    )

    task = await task_service.create_task(db_session, task_data)

    assert task.id is not None
    assert task.title == "Buy groceries"
    assert task.priority == PriorityEnum.HIGH
    assert len(task.tags) == 2
    assert {t.name for t in task.tags} == {"personal", "shopping"}

@pytest.mark.asyncio
async def test_filter_by_priority(db_session):
    """Test filtering tasks by priority."""
    # Create tasks with different priorities
    await task_service.create_task(db_session, TaskCreate(title="High", priority=PriorityEnum.HIGH))
    await task_service.create_task(db_session, TaskCreate(title="Med", priority=PriorityEnum.MEDIUM))

    # Filter by high priority
    tasks, total = await task_service.list_tasks(
        db_session, priority=PriorityEnum.HIGH, user_id=1
    )

    assert total == 1
    assert tasks[0].title == "High"
```

#### API Tests (pytest + httpx)

```python
# tests/test_api.py

@pytest.mark.asyncio
async def test_create_task_api(client):
    """Test POST /api/v1/tasks endpoint."""
    response = await client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "priority": "high",
            "tags": ["test"]
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["data"]["title"] == "Test Task"
    assert data["data"]["priority"] == "high"

@pytest.mark.asyncio
async def test_filter_tasks_api(client):
    """Test GET /api/v1/tasks with filters."""
    # Create test data
    await client.post("/api/v1/tasks", json={"title": "High", "priority": "high"})
    await client.post("/api/v1/tasks", json={"title": "Low", "priority": "low"})

    # Filter by high priority
    response = await client.get("/api/v1/tasks?priority=high")

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total"] == 1
    assert data["data"]["tasks"][0]["title"] == "High"
```

### Frontend Tests

#### Component Tests (Jest + RTL)

```typescript
// __tests__/TaskCard.test.tsx

import { render, screen, fireEvent } from '@testing-library/react';
import TaskCard from '@/components/TaskCard';
import { Task, Priority } from '@/lib/types';

const mockTask: Task = {
  id: 1,
  title: 'Test Task',
  description: 'Description',
  completed: false,
  priority: Priority.HIGH,
  tags: [],
  created_at: '2025-12-26T10:00:00Z',
  updated_at: '2025-12-26T10:00:00Z',
  user_id: 1,
};

test('renders task title and priority', () => {
  render(<TaskCard task={mockTask} />);

  expect(screen.getByText('Test Task')).toBeInTheDocument();
  expect(screen.getByText('HIGH')).toBeInTheDocument();
});

test('toggles completed status on checkbox click', async () => {
  render(<TaskCard task={mockTask} />);

  const checkbox = screen.getByRole('checkbox');
  expect(checkbox).not.toBeChecked();

  fireEvent.click(checkbox);

  // Should optimistically update
  expect(checkbox).toBeChecked();
});
```

### E2E Tests (Playwright)

```typescript
// e2e/tasks.spec.ts

import { test, expect } from '@playwright/test';

test('create task end-to-end', async ({ page }) => {
  await page.goto('/');

  // Click new task button
  await page.click('text=New Task');

  // Fill form
  await page.fill('input[name="title"]', 'E2E Test Task');
  await page.fill('textarea[name="description"]', 'Test description');
  await page.selectOption('select[name="priority"]', 'high');

  // Submit
  await page.click('button[type="submit"]');

  // Verify redirect and task appears
  await expect(page).toHaveURL('/');
  await expect(page.locator('text=E2E Test Task')).toBeVisible();
});

test('filter tasks by priority', async ({ page }) => {
  await page.goto('/');

  // Click high priority filter
  await page.click('text=High');

  // Verify URL updated
  await expect(page).toHaveURL('/?priority=high');

  // Verify only high priority tasks shown
  const tasks = page.locator('[data-testid="task-card"]');
  await expect(tasks).toHaveCount(/* expected count */);
});
```

---

## Deployment & Configuration

### Environment Variables

#### Backend (.env)

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/todo_db

# CORS
CORS_ORIGINS=http://localhost:3000,https://todo-app.vercel.app

# Logging
LOG_LEVEL=INFO

# Development
DEBUG=false
```

#### Frontend (.env.local)

```env
# API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Feature flags (optional)
NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

### Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: todo_user
      POSTGRES_PASSWORD: todo_pass
      POSTGRES_DB: todo_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    command: uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://todo_user:todo_pass@postgres:5432/todo_db
      CORS_ORIGINS: http://localhost:3000
    depends_on:
      - postgres
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    command: npm run dev
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules

volumes:
  postgres_data:
```

### Deployment Checklist

#### Backend
- [ ] Environment variables configured
- [ ] Database migrations run (`alembic upgrade head`)
- [ ] Seed data loaded (dev only)
- [ ] CORS origins configured for production
- [ ] Logging configured
- [ ] Health check endpoint (`GET /health`)

#### Frontend
- [ ] API URL configured for production
- [ ] Build succeeds (`npm run build`)
- [ ] Environment variables set in Vercel/hosting
- [ ] Static assets optimized

---

## Acceptance Criteria

### Phase II Complete When:

#### Backend API
- [ ] All 7 endpoints implemented and tested
- [ ] OpenAPI documentation accessible
- [ ] Database migrations work (up and down)
- [ ] Test coverage ≥80%
- [ ] All validation errors handled gracefully
- [ ] CORS configured correctly

#### Frontend UI
- [ ] Home page lists tasks with server components
- [ ] Create task form validates and submits
- [ ] Edit task pre-populates and updates
- [ ] Delete task shows confirmation modal
- [ ] Checkbox toggle updates optimistically
- [ ] Filters work and persist in URL
- [ ] Sorting works
- [ ] Mobile-responsive (tested on 375px, 768px, 1024px)

#### Features
- [ ] All Phase I features work via web
- [ ] Priorities implemented (high/medium/low)
- [ ] Tags implemented (create, assign, filter)
- [ ] Filters work (status, priority, tags)
- [ ] Sorting works (date, priority, title)
- [ ] Due dates work (set, display, overdue indicator)

#### Quality
- [ ] TypeScript strict mode passes
- [ ] Backend type hints complete
- [ ] Error messages user-friendly
- [ ] Loading states shown
- [ ] Success/error toasts work
- [ ] Keyboard navigation works
- [ ] No console errors in production build

#### Migration
- [ ] Phase I data can be imported
- [ ] Export functionality for backup
- [ ] Documentation for data migration

---

**Specification Version:** 1.0.0
**Created:** 2025-12-26
**Status:** READY FOR APPROVAL

**Next Step:** Review & Approve → Create Implementation Plan
