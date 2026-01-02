# Phase II Constitution - Full-Stack Web Todo App

**Phase:** II - Web Application
**Version:** 1.0.0
**Status:** Draft
**Parent:** [Global Constitution](../CONSTITUTION.md)
**Previous Phase:** [Phase I Constitution](../phase1/CONSTITUTION.md)

---

## Phase Overview

### Purpose
Transform the console Todo application into a modern, full-stack web application with persistent storage, RESTful API, and responsive web UI. This phase demonstrates the evolution of clean architecture from command-line to web while preserving core domain logic.

### Strategic Goals
1. **Web-First Experience**: Deliver intuitive, responsive web UI for all task operations
2. **Persistent Storage**: Migrate from in-memory to PostgreSQL database
3. **API-Driven Architecture**: Create RESTful API for frontend-backend separation
4. **Feature Expansion**: Add priorities, tags, and filtering capabilities
5. **Auth-Ready Foundation**: Design with future authentication in mind

### Technology Stack

#### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **UI Library**: React 18+ with Server Components
- **Styling**: Tailwind CSS
- **State Management**: React hooks + Server Actions
- **HTTP Client**: Fetch API (native)

#### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Async Runtime**: asyncio with async/await
- **API Documentation**: OpenAPI (Swagger) auto-generated
- **CORS**: Configured for Next.js frontend
- **Validation**: Pydantic v2 models

#### Database
- **Database**: PostgreSQL (Neon managed instance)
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Migrations**: Alembic
- **Connection**: Async driver (asyncpg)

#### Development Tools
- **API Testing**: pytest + httpx (async)
- **Frontend Testing**: Jest + React Testing Library
- **Type Checking**: mypy (backend), TypeScript compiler (frontend)
- **Linting**: ruff (backend), ESLint (frontend)

---

## Phase-Specific Principles

### 1. Domain Continuity
- **Preserve Phase I Logic**: Core task operations remain semantically identical
- **Evolutionary Refactoring**: Adapt, don't rewrite - maintain recognizable patterns
- **Migration Path**: Clear mapping from Phase I models to Phase II schemas
- **Backward Compatibility**: Phase I export can import into Phase II

### 2. API-First Design
- **Contract-Driven**: API contracts defined before implementation
- **RESTful Principles**: Resource-oriented URLs, HTTP verbs, status codes
- **Versioned**: API version in URL path (`/api/v1/`)
- **Self-Documenting**: OpenAPI schema accessible at `/docs`

### 3. Separation of Concerns
```
┌─────────────────────────────────────┐
│   Frontend (Next.js)                │
│   - Pages & Components              │
│   - Client & Server Components      │
└─────────────────────────────────────┘
            ↓ HTTP/JSON ↑
┌─────────────────────────────────────┐
│   Backend API (FastAPI)             │
│   - Route Handlers                  │
│   - Business Logic (from Phase I)   │
└─────────────────────────────────────┘
            ↓ SQL ↑
┌─────────────────────────────────────┐
│   Database (PostgreSQL)             │
│   - Tables, Indexes, Constraints    │
└─────────────────────────────────────┘
```

### 4. Progressive Enhancement
- **Start Simple**: Mock auth initially, real auth later
- **Feature Flags**: New features can be toggled off
- **Graceful Degradation**: UI works without JavaScript for core reading
- **Mobile-First**: Responsive design from day one

### 5. Developer Experience
- **Hot Reload**: Fast development iteration (Next.js dev server, FastAPI --reload)
- **Type Safety**: End-to-end types (TypeScript ↔ OpenAPI ↔ Pydantic)
- **Easy Setup**: Docker Compose for local database, simple .env config
- **Clear Errors**: Meaningful validation errors propagated to UI

---

## Functional Requirements

### Migration from Phase I

#### Preserved Features (Web-Enabled)
All Phase I features now accessible via web UI and API:

| Phase I Feature | Phase II Implementation |
|----------------|------------------------|
| Add Task | POST `/api/v1/tasks` + UI form |
| View All Tasks | GET `/api/v1/tasks` + List page |
| View Task Detail | GET `/api/v1/tasks/{id}` + Detail view |
| Update Task | PATCH `/api/v1/tasks/{id}` + Edit form |
| Delete Task | DELETE `/api/v1/tasks/{id}` + Delete button |
| Complete/Uncomplete | PATCH `/api/v1/tasks/{id}` + Checkbox toggle |

#### Enhanced Features (New Fields)
Extended task model with new capabilities:

| Field | Phase I | Phase II |
|-------|---------|----------|
| `priority` | N/A | `high`, `medium`, `low` |
| `tags` | N/A | Array of strings (e.g., `["work", "urgent"]`) |
| `due_date` | N/A | ISO 8601 date (nullable) |

### New Phase II Features

#### F1: Task Priorities
- **Description**: Assign priority level to tasks for better organization
- **Priority Levels**:
  - `high` (red indicator, top of sorted lists)
  - `medium` (yellow indicator, default)
  - `low` (blue indicator, bottom of sorted lists)
- **UI**: Dropdown selector in create/edit forms, colored badges in list view
- **API**: `priority` field in task schema (enum validation)

#### F2: Task Tags/Categories
- **Description**: Organize tasks with multiple tags
- **Implementation**: Many-to-many relationship (tasks ↔ tags)
- **Tag Features**:
  - Auto-suggest existing tags
  - Create new tags inline
  - Multiple tags per task
  - Tag-based filtering
- **UI**: Tag input with autocomplete, tag chips with remove option
- **API**: `tags` array in task schema

#### F3: Filtering & Sorting
- **Filter Options**:
  - By status: All / Active / Completed
  - By priority: All / High / Medium / Low
  - By tag: Select one or more tags
  - By due date: Overdue / Due today / Due this week / No due date
- **Sort Options**:
  - By created date (newest/oldest)
  - By priority (high to low / low to high)
  - By due date (soonest first)
  - By title (A-Z / Z-A)
- **UI**: Filter panel with chips showing active filters
- **API**: Query parameters on GET `/api/v1/tasks`

#### F4: Due Dates
- **Description**: Set optional deadlines for tasks
- **Features**:
  - Date picker in UI
  - Visual indicators for overdue tasks
  - Sortable by due date
- **UI**: Date input, "Overdue" badge for past dates
- **API**: `due_date` field (ISO 8601, nullable)

### Authentication (Simplified)

#### Mock Authentication (Phase II Initial)
- **User Identification**: Single hardcoded user (`user_id = 1`)
- **No Login UI**: All tasks belong to default user
- **Database**: Tasks table includes `user_id` foreign key (prepared for multi-user)
- **API**: No auth headers required

#### Auth-Ready Design
- **User Model**: Defined but not enforced
- **Isolation**: Each task linked to user_id
- **Future Path**: Add JWT authentication, login page (Phase III or later)

---

## Data Model

### Database Schema (SQLModel)

#### Task Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from enum import Enum

class PriorityEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(SQLModel, table=True):
    """
    Task entity with persistence.

    Extends Phase I Task with priority, tags, and due date.
    """
    __tablename__ = "tasks"

    # Core fields (from Phase I)
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, nullable=False)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # New Phase II fields
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
    due_date: Optional[datetime] = Field(default=None, nullable=True)

    # Auth-ready field
    user_id: int = Field(foreign_key="users.id", default=1)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tasks")
    tags: list["Tag"] = Relationship(back_populates="tasks", link_model="TaskTag")
```

#### Tag Model

```python
class Tag(SQLModel, table=True):
    """Tag for categorizing tasks."""
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True, nullable=False)
    color: Optional[str] = Field(default=None, max_length=7)  # Hex color code
    user_id: int = Field(foreign_key="users.id", default=1)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="tags", link_model="TaskTag")
    user: Optional["User"] = Relationship(back_populates="tags")
```

#### TaskTag (Join Table)

```python
class TaskTag(SQLModel, table=True):
    """Many-to-many relationship between tasks and tags."""
    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)
```

#### User Model (Placeholder)

```python
class User(SQLModel, table=True):
    """User model for future authentication."""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, nullable=False)
    email: str = Field(max_length=100, unique=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user")
    tags: list["Tag"] = Relationship(back_populates="user")
```

### Field Migrations from Phase I

| Phase I Field | Phase II Mapping | Changes |
|--------------|-----------------|---------|
| `id: int` | `id: Optional[int]` | Now auto-generated by DB |
| `title: str` | `title: str` | Max length enforced at DB level |
| `description: str` | `description: str` | Max length enforced at DB level |
| `completed: bool` | `completed: bool` | No change |
| `created_at: str` | `created_at: datetime` | ISO string → datetime object |
| `updated_at: str` | `updated_at: datetime` | ISO string → datetime object |
| N/A | `priority: PriorityEnum` | New field (default: `medium`) |
| N/A | `due_date: Optional[datetime]` | New field (nullable) |
| N/A | `user_id: int` | New field (default: 1) |
| N/A | `tags: list[Tag]` | New relationship |

### Database Indexes

```sql
-- Performance indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

CREATE INDEX idx_tags_user_id ON tags(user_id);
CREATE INDEX idx_tags_name ON tags(name);
```

---

## API Specification

### Base URL
- **Development**: `http://localhost:8000`
- **Production**: TBD (e.g., `https://api.todo-app.com`)
- **API Prefix**: `/api/v1`

### Authentication
- **Phase II Initial**: No authentication required
- **Header (Future)**: `Authorization: Bearer <token>`

### Response Format

#### Success Response
```json
{
  "data": { /* resource or array */ },
  "message": "Success message (optional)"
}
```

#### Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable error",
    "details": [
      {
        "field": "title",
        "message": "Title cannot be empty"
      }
    ]
  }
}
```

### Endpoints

#### 1. List Tasks
```
GET /api/v1/tasks
```

**Query Parameters:**
- `status` (optional): `all` | `active` | `completed` (default: `all`)
- `priority` (optional): `high` | `medium` | `low`
- `tag` (optional): Tag name or ID (can be repeated for multiple tags)
- `sort` (optional): `created_desc` | `created_asc` | `priority_desc` | `due_asc` | `title_asc`
- `limit` (optional): Integer (default: 100, max: 1000)
- `offset` (optional): Integer (default: 0)

**Response:** `200 OK`
```json
{
  "data": {
    "tasks": [
      {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": false,
        "priority": "high",
        "due_date": "2025-12-31T00:00:00Z",
        "tags": [
          {"id": 1, "name": "personal", "color": "#3B82F6"}
        ],
        "created_at": "2025-12-26T10:00:00Z",
        "updated_at": "2025-12-26T10:00:00Z",
        "user_id": 1
      }
    ],
    "total": 1,
    "limit": 100,
    "offset": 0
  }
}
```

#### 2. Get Task by ID
```
GET /api/v1/tasks/{id}
```

**Response:** `200 OK`
```json
{
  "data": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "priority": "high",
    "due_date": "2025-12-31T00:00:00Z",
    "tags": [
      {"id": 1, "name": "personal", "color": "#3B82F6"}
    ],
    "created_at": "2025-12-26T10:00:00Z",
    "updated_at": "2025-12-26T10:00:00Z",
    "user_id": 1
  }
}
```

**Error:** `404 Not Found`
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Task with ID 1 not found"
  }
}
```

#### 3. Create Task
```
POST /api/v1/tasks
```

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "high",
  "due_date": "2025-12-31T00:00:00Z",
  "tags": ["personal", "shopping"]
}
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
    "due_date": "2025-12-31T00:00:00Z",
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

#### 4. Update Task
```
PATCH /api/v1/tasks/{id}
```

**Request Body** (all fields optional):
```json
{
  "title": "Buy groceries and snacks",
  "description": "Updated description",
  "priority": "medium",
  "completed": true,
  "due_date": "2025-12-31T00:00:00Z",
  "tags": ["personal"]
}
```

**Response:** `200 OK`
```json
{
  "data": { /* updated task */ },
  "message": "Task updated successfully"
}
```

#### 5. Delete Task
```
DELETE /api/v1/tasks/{id}
```

**Response:** `200 OK`
```json
{
  "message": "Task deleted successfully"
}
```

#### 6. List Tags
```
GET /api/v1/tags
```

**Response:** `200 OK`
```json
{
  "data": [
    {"id": 1, "name": "personal", "color": "#3B82F6"},
    {"id": 2, "name": "work", "color": "#EF4444"}
  ]
}
```

#### 7. Create Tag
```
POST /api/v1/tags
```

**Request Body:**
```json
{
  "name": "urgent",
  "color": "#F59E0B"
}
```

**Response:** `201 Created`

---

## Frontend Specification

### Pages & Routes

| Route | Page | Description |
|-------|------|-------------|
| `/` | Home/Dashboard | List all tasks with filters |
| `/tasks/new` | Create Task | Form to add new task |
| `/tasks/[id]` | Task Detail | View/edit single task |
| `/tags` | Manage Tags | Create/edit/delete tags |

### Component Hierarchy

```
app/
├── layout.tsx                 # Root layout with nav
├── page.tsx                   # Home page (task list)
├── tasks/
│   ├── new/
│   │   └── page.tsx          # Create task page
│   └── [id]/
│       └── page.tsx          # Task detail/edit page
├── tags/
│   └── page.tsx              # Tag management
└── components/
    ├── TaskList.tsx          # Server component: list of tasks
    ├── TaskCard.tsx          # Task item with checkbox, priority badge
    ├── TaskForm.tsx          # Client component: create/edit form
    ├── FilterPanel.tsx       # Client component: filter UI
    ├── TagInput.tsx          # Client component: tag autocomplete
    ├── PriorityBadge.tsx     # Priority indicator
    ├── DueDatePicker.tsx     # Date selector
    └── Navigation.tsx        # App nav bar
```

### UI Flows

#### Flow 1: View Tasks (Landing Page)
1. User navigates to `/`
2. Server component fetches tasks from API
3. TaskList renders with TaskCard components
4. Each TaskCard shows:
   - Checkbox (completed state)
   - Title (clickable to detail page)
   - Priority badge (colored: high=red, medium=yellow, low=blue)
   - Tags (as chips)
   - Due date (if set, with "Overdue" badge if past)
5. FilterPanel (client component) allows filtering without page reload
6. Clicking filter updates URL search params, triggers re-render

#### Flow 2: Create Task
1. User clicks "New Task" button
2. Navigate to `/tasks/new`
3. TaskForm renders with fields:
   - Title (required, text input)
   - Description (optional, textarea)
   - Priority (dropdown: high/medium/low)
   - Tags (multi-select with autocomplete)
   - Due date (date picker, optional)
4. User fills form, clicks "Create"
5. Client submits POST `/api/v1/tasks`
6. On success: redirect to `/` with success toast
7. On error: display validation errors inline

#### Flow 3: Edit Task
1. User clicks task title in list
2. Navigate to `/tasks/[id]`
3. Server component fetches task detail
4. TaskForm pre-populated with existing values
5. User modifies fields, clicks "Save"
6. Client submits PATCH `/api/v1/tasks/{id}`
7. On success: show success message, stay on page or redirect
8. User can also click "Delete" → confirmation modal → DELETE request

#### Flow 4: Toggle Complete
1. User clicks checkbox on TaskCard
2. Client submits PATCH `/api/v1/tasks/{id}` with `{"completed": true}`
3. Optimistic UI update (check immediately)
4. On API success: keep checked
5. On API error: revert checkbox, show error toast

#### Flow 5: Filter & Sort
1. User selects filter (e.g., "Show only High priority")
2. FilterPanel updates URL: `/?priority=high`
3. Server component re-renders with filtered tasks
4. User can combine filters: `/?priority=high&status=active&tag=work`
5. User can sort: `/?sort=due_asc`
6. Active filters shown as removable chips

### Wireframe Descriptions

#### Home Page (`/`)
```
┌────────────────────────────────────────────────┐
│  [Todo App]              [+ New Task] [Tags]   │
├────────────────────────────────────────────────┤
│  Filters: [All] [Active] [Completed]           │
│  Priority: [All] [High] [Medium] [Low]         │
│  Sort: [Newest First ▼]                        │
├────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────┐ │
│  │ ☐ Buy groceries              [HIGH]      │ │
│  │   Milk, eggs, bread                      │ │
│  │   📅 Due: Dec 31  🏷 personal, shopping  │ │
│  └──────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────┐ │
│  │ ☑ Finish report            [MEDIUM]      │ │
│  │   Q4 financial analysis                  │ │
│  │   🏷 work                                │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  Showing 2 of 2 tasks                         │
└────────────────────────────────────────────────┘
```

#### Create Task Page (`/tasks/new`)
```
┌────────────────────────────────────────────────┐
│  [← Back]          Create New Task             │
├────────────────────────────────────────────────┤
│  Title *                                       │
│  ┌──────────────────────────────────────────┐ │
│  │ Buy groceries                            │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  Description                                   │
│  ┌──────────────────────────────────────────┐ │
│  │ Milk, eggs, bread                        │ │
│  │                                          │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  Priority                                      │
│  ○ High  ● Medium  ○ Low                      │
│                                                │
│  Tags                                          │
│  [personal] [shopping] [+ Add tag]            │
│                                                │
│  Due Date                                      │
│  [📅 Select date] (optional)                  │
│                                                │
│  [Cancel]                    [Create Task]    │
└────────────────────────────────────────────────┘
```

### Styling Guidelines

- **Colors**:
  - Primary: Blue (#3B82F6)
  - Success/Complete: Green (#10B981)
  - High Priority: Red (#EF4444)
  - Medium Priority: Yellow/Orange (#F59E0B)
  - Low Priority: Blue/Gray (#6B7280)
- **Typography**: Sans-serif (Inter or system font)
- **Spacing**: Consistent 4px grid (Tailwind default)
- **Responsive**: Mobile-first, breakpoints at 640px, 768px, 1024px
- **Accessibility**: WCAG AA compliant (contrast, focus states, ARIA labels)

---

## Non-Functional Requirements

### Performance
- **API Response Time**: <200ms for list queries, <100ms for CRUD operations
- **Database Queries**: Use indexes, avoid N+1 queries
- **Frontend Load Time**: <2s initial page load (LCP)
- **Concurrent Users**: Support 100+ simultaneous users

### Security
- **SQL Injection**: Prevented by SQLModel/SQLAlchemy
- **XSS**: Sanitized by React (auto-escaping)
- **CORS**: Configured for specific origins only
- **Input Validation**: Both client and server-side
- **HTTPS**: Required in production

### Scalability
- **Database**: Connection pooling, prepared statements
- **API**: Stateless design, horizontal scaling ready
- **Frontend**: Static generation where possible (Next.js SSG)

### Reliability
- **Error Handling**: Graceful degradation, user-friendly messages
- **Database Transactions**: ACID compliance for multi-step operations
- **Retry Logic**: Frontend retries failed API calls (idempotent operations)

### Observability
- **Logging**: Structured JSON logs (FastAPI middleware)
- **Error Tracking**: Console errors captured (can add Sentry later)
- **API Monitoring**: Request/response logging

---

## Acceptance Criteria

### Milestone 1: Backend API
- [ ] All 7 API endpoints implemented and documented
- [ ] OpenAPI schema accessible at `/docs`
- [ ] Database migrations created via Alembic
- [ ] All endpoints have ≥80% test coverage
- [ ] Validation errors return proper 422 responses
- [ ] CORS configured for Next.js dev server

### Milestone 2: Database & Models
- [ ] SQLModel models defined for Task, Tag, TaskTag, User
- [ ] Database indexes created for performance
- [ ] Migrations tested (up and down)
- [ ] Seed data script for development
- [ ] Connection pooling configured

### Milestone 3: Frontend UI
- [ ] Home page lists tasks with filters
- [ ] Create task form validates and submits
- [ ] Edit task form pre-populates and updates
- [ ] Delete task shows confirmation
- [ ] Checkbox toggle optimistically updates
- [ ] Mobile-responsive design

### Milestone 4: End-to-End Flows
- [ ] User can create task with all fields
- [ ] User can filter by status, priority, tags
- [ ] User can sort tasks
- [ ] User can mark task complete/incomplete
- [ ] User can edit task and see changes immediately
- [ ] User can delete task

### Milestone 5: Quality & Polish
- [ ] All frontend components have TypeScript types
- [ ] All backend routes have type hints
- [ ] Error messages are user-friendly
- [ ] Loading states shown during async operations
- [ ] Success/error toasts for user feedback
- [ ] Accessibility: keyboard navigation works

---

## Migration Strategy from Phase I

### Data Migration
1. Export Phase I tasks to JSON (if any exist)
2. Transform JSON to Phase II schema:
   - Add `priority: "medium"` (default)
   - Add `tags: []` (empty array)
   - Convert ISO strings to datetime
   - Add `user_id: 1`
3. Import via SQL INSERT or API bulk create endpoint

### Code Reuse
- **Phase I Service Logic**: Adapt to async/await
  - `add_task()` → `async def create_task()`
  - `get_all_tasks()` → `async def list_tasks()`
  - Validation rules → Pydantic models
- **Phase I Repository**: Replace with SQLModel queries
  - In-memory dict → Database table
  - CRUD operations → SQLAlchemy async session

### Testing Strategy
- **Unit Tests**: SQLModel models, Pydantic schemas
- **Integration Tests**: API endpoints (pytest + httpx)
- **E2E Tests**: Frontend flows (Playwright or Cypress)
- **Migration Tests**: Verify Phase I data imports correctly

---

## Development Workflow

### Local Setup
1. **Database**: Start Neon Postgres locally or use Docker
2. **Backend**:
   ```bash
   cd phase2/backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   alembic upgrade head
   uvicorn main:app --reload
   ```
3. **Frontend**:
   ```bash
   cd phase2/frontend
   npm install
   npm run dev
   ```

### Environment Variables
```env
# Backend (.env)
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/todo_db
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development Flow
1. **API-First**: Define OpenAPI schema → Implement backend → Test with Swagger
2. **Frontend Integration**: Generate TypeScript types from OpenAPI → Build UI
3. **Iterative**: Test each feature end-to-end before moving to next

---

## Success Metrics

### Functionality
- ✅ All Phase I features work via web UI
- ✅ All Phase II features (priority, tags, filters) implemented
- ✅ No data loss compared to Phase I

### Quality
- ✅ Backend test coverage ≥80%
- ✅ Frontend components have unit tests
- ✅ All API endpoints documented
- ✅ TypeScript strict mode passes

### User Experience
- ✅ Intuitive UI (user can complete task without documentation)
- ✅ Fast (<2s page loads)
- ✅ Mobile-friendly
- ✅ Accessible (keyboard navigation, screen reader friendly)

### Code Quality
- ✅ Follows Phase I architectural patterns
- ✅ Clean separation of concerns
- ✅ Comprehensive error handling
- ✅ Clear code comments where needed

---

## Risks & Mitigations

### Risk 1: Database Connection Issues
- **Risk**: Neon Postgres connection failures
- **Mitigation**: Connection pooling, retry logic, fallback to local Postgres

### Risk 2: API-Frontend Mismatch
- **Risk**: API changes break frontend
- **Mitigation**: OpenAPI contract testing, TypeScript type generation from schema

### Risk 3: Performance Degradation
- **Risk**: Slow queries with many tasks
- **Mitigation**: Database indexes, pagination, caching headers

### Risk 4: Scope Creep
- **Risk**: Adding features beyond Phase II spec
- **Mitigation**: Strict adherence to spec, defer extras to Phase III

---

## Future Phase III Preview

Phase III will add:
- **AI Chatbot**: OpenAI Agents SDK for natural language task management
- **MCP Integration**: Model Context Protocol for AI-assisted scheduling
- **Advanced Features**: Recurring tasks, smart reminders

Phase II must prepare for this by:
- Keeping API stateless and RESTful
- Maintaining clean separation of frontend/backend
- Designing extensible task schema

---

**Constitution Version:** 1.0.0
**Effective Date:** 2025-12-26
**Status:** Ready for Specification Approval

---

## Quick Reference

**Tech Stack:** Next.js + FastAPI + PostgreSQL (Neon)
**New Features:** Priorities, Tags, Filters, Due Dates
**Auth:** Mock (user_id=1), designed for future JWT
**API:** RESTful, versioned (`/api/v1`), documented (OpenAPI)
**UI:** Responsive, mobile-first, Tailwind CSS

**Next Step:** Approve this Constitution → Create SPECIFICATION.md → Plan Implementation
