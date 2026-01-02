# Phase II Task List - Full-Stack Web Todo App

**Project:** Evolution of Todo
**Phase:** II - Web Application
**Task List Version:** 1.0.0
**Parent Documents:**
- [Global Constitution](../CONSTITUTION.md)
- [Phase II Constitution](./CONSTITUTION.md)
- [Phase II Specification](./SPECIFICATION.md)
- [Phase II Plan](./PLAN.md)

---

## Task Organization

This document breaks down the Phase II implementation plan into **atomic, executable tasks** for Claude Code. Each task:
- Has a unique ID
- Belongs to a step from PLAN.md
- Can be completed independently (or with minimal dependencies)
- Has clear acceptance criteria
- Can be validated programmatically

**Total Tasks:** 52
**Milestones:** 4
**Estimated Complexity:** High (Full-Stack Implementation)

---

## Milestone 1: Backend Foundation (Tasks 1-19)

**Goal:** RESTful API with database operational
**Steps Covered:** Steps 1-3 from PLAN.md

---

### Step 1: Backend Project Setup & Database Connection

#### Task 1.1: Create Backend Directory Structure
**ID:** `PHASE2-001`
**Type:** Setup
**Step:** 1.1

**Description:**
Create the complete backend directory structure for the FastAPI application.

**Actions:**
1. Create `phase2/backend/` directory
2. Create all subdirectories: `app/`, `app/models/`, `app/schemas/`, `app/api/v1/endpoints/`, `app/services/`, `alembic/versions/`, `tests/`
3. Create all `__init__.py` files in Python packages
4. Verify structure matches specification

**Expected Artifacts:**
```
phase2/backend/
├── app/
│   ├── __init__.py
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
└── tests/
    └── __init__.py
```

**Acceptance Criteria:**
- [ ] All directories created
- [ ] All `__init__.py` files present
- [ ] Directory structure matches specification
- [ ] `ls -R phase2/backend/` shows complete structure

**Validation:**
```bash
cd /mnt/d/Data/GIAIC/hackathon2
ls -R phase2/backend/
```

---

#### Task 1.2: Generate requirements.txt
**ID:** `PHASE2-002`
**Type:** Configuration
**Step:** 1.2

**Description:**
Create `requirements.txt` with all backend dependencies.

**Actions:**
1. Create `phase2/backend/requirements.txt`
2. Add FastAPI, uvicorn, SQLModel, asyncpg, Alembic, Pydantic, pytest, and dev tools
3. Pin versions per specification

**Expected Artifacts:**
- `phase2/backend/requirements.txt` with 14+ dependencies

**Content:**
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

**Acceptance Criteria:**
- [ ] File exists at `phase2/backend/requirements.txt`
- [ ] All required packages listed
- [ ] Version constraints specified
- [ ] File parseable by pip

**Validation:**
```bash
cd phase2/backend
pip install -r requirements.txt --dry-run
```

---

#### Task 1.3: Create app/config.py
**ID:** `PHASE2-003`
**Type:** Code
**Step:** 1.3

**Description:**
Create configuration module using Pydantic settings for environment variables.

**Actions:**
1. Create `phase2/backend/app/config.py`
2. Implement `Settings` class with BaseSettings
3. Define DATABASE_URL, CORS_ORIGINS, APP_NAME, APP_VERSION, DEBUG, LOG_LEVEL
4. Configure to load from `.env` file

**Expected Artifacts:**
- `phase2/backend/app/config.py` (~40 lines)

**Acceptance Criteria:**
- [ ] File imports from pydantic_settings
- [ ] Settings class defined with all fields
- [ ] Config.env_file = ".env"
- [ ] settings instance exported
- [ ] Type hints complete
- [ ] mypy passes

**Validation:**
```bash
cd phase2/backend
python -c "from app.config import settings; print(settings.APP_NAME)"
```

---

#### Task 1.4: Create app/database.py
**ID:** `PHASE2-004`
**Type:** Code
**Step:** 1.4

**Description:**
Create database connection module with async SQLModel engine.

**Actions:**
1. Create `phase2/backend/app/database.py`
2. Implement async engine creation
3. Implement async session factory
4. Create `get_session()` dependency
5. Create `init_db()` for table creation

**Expected Artifacts:**
- `phase2/backend/app/database.py` (~30 lines)

**Acceptance Criteria:**
- [ ] Async engine created from settings.DATABASE_URL
- [ ] Session factory configured
- [ ] get_session() yields AsyncSession
- [ ] init_db() creates all tables
- [ ] Type hints complete
- [ ] mypy passes

**Validation:**
```bash
cd phase2/backend
python -c "from app.database import get_session; print('DB module OK')"
```

---

#### Task 1.5: Create app/main.py
**ID:** `PHASE2-005`
**Type:** Code
**Step:** 1.5

**Description:**
Create FastAPI application entry point with CORS and health endpoints.

**Actions:**
1. Create `phase2/backend/app/main.py`
2. Initialize FastAPI app with title, version, description
3. Add CORS middleware
4. Create startup event to call init_db()
5. Add `/health` endpoint
6. Add root `/` endpoint

**Expected Artifacts:**
- `phase2/backend/app/main.py` (~50 lines)

**Acceptance Criteria:**
- [ ] FastAPI app instantiated
- [ ] CORS configured for localhost:3000
- [ ] Startup event calls init_db()
- [ ] /health returns {"status": "healthy", "version": "1.0.0"}
- [ ] / returns welcome message with links
- [ ] Type hints complete

**Validation:**
```bash
cd phase2/backend
# Manual test: uvicorn app.main:app --reload (in separate terminal)
# curl http://localhost:8000/health
```

---

#### Task 1.6: Create .env.example
**ID:** `PHASE2-006`
**Type:** Configuration
**Step:** 1.6

**Description:**
Create environment variable template file.

**Actions:**
1. Create `phase2/backend/.env.example`
2. Add DATABASE_URL with placeholder
3. Add CORS_ORIGINS, DEBUG, LOG_LEVEL

**Expected Artifacts:**
- `phase2/backend/.env.example` (~5 lines)

**Content:**
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/todo_db
CORS_ORIGINS=http://localhost:3000
DEBUG=True
LOG_LEVEL=INFO
```

**Acceptance Criteria:**
- [ ] File exists
- [ ] All required variables present
- [ ] Format valid (KEY=value)

**Validation:**
```bash
cat phase2/backend/.env.example
```

---

#### Task 1.7: Initialize Alembic
**ID:** `PHASE2-007`
**Type:** Setup
**Step:** 1.7

**Description:**
Initialize Alembic for database migrations and configure for SQLModel.

**Actions:**
1. Run `alembic init alembic` in backend directory
2. Edit `alembic.ini` to use settings.DATABASE_URL
3. Edit `alembic/env.py` to import SQLModel metadata
4. Configure for async engine

**Expected Artifacts:**
- `phase2/backend/alembic.ini`
- `phase2/backend/alembic/env.py` (configured)
- `phase2/backend/alembic/versions/` directory

**Acceptance Criteria:**
- [ ] Alembic initialized
- [ ] alembic.ini configured
- [ ] env.py imports from app.database
- [ ] env.py uses SQLModel.metadata
- [ ] Async configuration complete

**Validation:**
```bash
cd phase2/backend
alembic current  # Should show no migrations yet
```

---

#### Task 1.8: Create backend README.md (Initial)
**ID:** `PHASE2-008`
**Type:** Documentation
**Step:** 1

**Description:**
Create initial backend README with setup instructions.

**Actions:**
1. Create `phase2/backend/README.md`
2. Add setup instructions
3. Add running instructions
4. Add development dependencies

**Expected Artifacts:**
- `phase2/backend/README.md` (~50 lines initially)

**Acceptance Criteria:**
- [ ] File exists
- [ ] Setup instructions clear
- [ ] Running commands included
- [ ] Development workflow documented

**Validation:**
```bash
cat phase2/backend/README.md
```

---

### Step 2: Database Models & Migrations

#### Task 2.1: Create app/models/user.py
**ID:** `PHASE2-009`
**Type:** Code
**Step:** 2.1

**Description:**
Create User SQLModel with relationships.

**Actions:**
1. Create `phase2/backend/app/models/user.py`
2. Define User model with table=True
3. Add fields: id, username, email, created_at
4. Add relationships: tasks, tags

**Expected Artifacts:**
- `phase2/backend/app/models/user.py` (~25 lines)

**Acceptance Criteria:**
- [ ] User inherits from SQLModel
- [ ] __tablename__ = "users"
- [ ] All fields typed correctly
- [ ] Relationships defined
- [ ] TYPE_CHECKING used for imports
- [ ] mypy passes

**Validation:**
```bash
cd phase2/backend
python -c "from app.models.user import User; print(User.__tablename__)"
```

---

#### Task 2.2: Create app/models/tag.py
**ID:** `PHASE2-010`
**Type:** Code
**Step:** 2.2

**Description:**
Create Tag SQLModel with user relationship.

**Actions:**
1. Create `phase2/backend/app/models/tag.py`
2. Define Tag model with table=True
3. Add fields: id, name, color, user_id
4. Add relationships: user, tasks

**Expected Artifacts:**
- `phase2/backend/app/models/tag.py` (~20 lines)

**Acceptance Criteria:**
- [ ] Tag inherits from SQLModel
- [ ] __tablename__ = "tags"
- [ ] user_id foreign key to users.id
- [ ] Relationships defined
- [ ] mypy passes

**Validation:**
```bash
cd phase2/backend
python -c "from app.models.tag import Tag; print(Tag.__tablename__)"
```

---

#### Task 2.3: Create app/models/task.py
**ID:** `PHASE2-011`
**Type:** Code
**Step:** 2.3

**Description:**
Create Task and TaskTag SQLModels with PriorityEnum.

**Actions:**
1. Create `phase2/backend/app/models/task.py`
2. Define PriorityEnum: HIGH, MEDIUM, LOW
3. Define TaskTag join table model
4. Define Task model with all fields
5. Add relationships: user, tags

**Expected Artifacts:**
- `phase2/backend/app/models/task.py` (~60 lines)

**Acceptance Criteria:**
- [ ] PriorityEnum defined as str, Enum
- [ ] TaskTag has task_id, tag_id as primary keys
- [ ] Task has all specified fields
- [ ] priority field uses PriorityEnum
- [ ] Indexes on completed, priority, due_date, created_at
- [ ] Relationships defined with link_model=TaskTag
- [ ] mypy passes

**Validation:**
```bash
cd phase2/backend
python -c "from app.models.task import Task, PriorityEnum; print(PriorityEnum.MEDIUM)"
```

---

#### Task 2.4: Create app/models/__init__.py
**ID:** `PHASE2-012`
**Type:** Code
**Step:** 2.4

**Description:**
Create models package __init__.py with exports.

**Actions:**
1. Update `phase2/backend/app/models/__init__.py`
2. Import all models
3. Define __all__ list

**Expected Artifacts:**
- `phase2/backend/app/models/__init__.py` (~10 lines)

**Acceptance Criteria:**
- [ ] Imports User, Tag, Task, TaskTag, PriorityEnum
- [ ] __all__ defined
- [ ] No circular import errors
- [ ] All models accessible from app.models

**Validation:**
```bash
cd phase2/backend
python -c "from app.models import User, Tag, Task, TaskTag, PriorityEnum; print('All models OK')"
```

---

#### Task 2.5: Create Initial Migration
**ID:** `PHASE2-013`
**Type:** Database
**Step:** 2.5

**Description:**
Generate and customize initial Alembic migration.

**Actions:**
1. Run `alembic revision --autogenerate -m "Initial schema"`
2. Review generated migration
3. Add indexes manually if not auto-detected
4. Add default user insert (id=1)
5. Test upgrade and downgrade

**Expected Artifacts:**
- `phase2/backend/alembic/versions/001_initial_schema_*.py`

**Acceptance Criteria:**
- [ ] Migration file created
- [ ] Creates users, tasks, tags, task_tags tables
- [ ] Indexes created as specified
- [ ] Default user (id=1) inserted
- [ ] upgrade() works
- [ ] downgrade() works

**Validation:**
```bash
cd phase2/backend
# Requires DATABASE_URL to be set
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

---

#### Task 2.6: Create Seed Data Script
**ID:** `PHASE2-014`
**Type:** Code
**Step:** 2.6

**Description:**
Create script to seed development data.

**Actions:**
1. Create `phase2/backend/scripts/seed_data.py`
2. Create default user (id=1)
3. Create sample tags (personal, work, urgent)
4. Make script executable

**Expected Artifacts:**
- `phase2/backend/scripts/seed_data.py` (~40 lines)

**Acceptance Criteria:**
- [ ] Script creates default user
- [ ] Script creates 3+ sample tags
- [ ] Uses async/await
- [ ] Runnable: `python scripts/seed_data.py`
- [ ] Idempotent (can run multiple times)

**Validation:**
```bash
cd phase2/backend
python scripts/seed_data.py
# Verify in database
```

---

### Step 3: Pydantic Schemas & Core API Endpoints

#### Task 3.1: Create app/schemas/task.py
**ID:** `PHASE2-015`
**Type:** Code
**Step:** 3.1

**Description:**
Create Pydantic schemas for task validation.

**Actions:**
1. Create `phase2/backend/app/schemas/task.py`
2. Define TaskBase with field validators
3. Define TaskCreate, TaskUpdate, TaskResponse
4. Define TagSchema
5. Implement title validator

**Expected Artifacts:**
- `phase2/backend/app/schemas/task.py` (~80 lines)

**Acceptance Criteria:**
- [ ] All schemas inherit from BaseModel
- [ ] TaskBase has title, description, priority, due_date
- [ ] title validator strips whitespace
- [ ] TaskCreate includes tags list
- [ ] TaskUpdate has all optional fields
- [ ] TaskResponse includes id, created_at, updated_at, tags
- [ ] from_attributes = True in Config
- [ ] mypy passes

**Validation:**
```bash
cd phase2/backend
python -c "from app.schemas.task import TaskCreate; t = TaskCreate(title='Test'); print(t.title)"
```

---

#### Task 3.2: Create app/schemas/common.py
**ID:** `PHASE2-016`
**Type:** Code
**Step:** 3.2

**Description:**
Create common response schemas.

**Actions:**
1. Create `phase2/backend/app/schemas/common.py`
2. Define SuccessResponse
3. Define ErrorResponse

**Expected Artifacts:**
- `phase2/backend/app/schemas/common.py` (~15 lines)

**Acceptance Criteria:**
- [ ] SuccessResponse has data: Any, message: Optional[str]
- [ ] ErrorResponse has error: dict
- [ ] Both inherit from BaseModel
- [ ] mypy passes

**Validation:**
```bash
cd phase2/backend
python -c "from app.schemas.common import SuccessResponse; print('OK')"
```

---

#### Task 3.3: Create app/services/task_service.py
**ID:** `PHASE2-017`
**Type:** Code
**Step:** 3.3

**Description:**
Create TaskService with business logic for CRUD operations.

**Actions:**
1. Create `phase2/backend/app/services/task_service.py`
2. Implement create_task() with tag handling
3. Implement list_tasks() with filters and sorting
4. Implement get_task()
5. Implement update_task() with tag updates
6. Implement delete_task()

**Expected Artifacts:**
- `phase2/backend/app/services/task_service.py` (~150 lines)

**Acceptance Criteria:**
- [ ] All methods are @staticmethod async
- [ ] create_task creates task and links tags
- [ ] list_tasks supports status, priority, tags, sort_by filters
- [ ] list_tasks returns (tasks, total) tuple
- [ ] get_task returns Optional[Task]
- [ ] update_task handles partial updates
- [ ] update_task updates tags if provided
- [ ] delete_task returns bool
- [ ] Type hints complete
- [ ] mypy passes

**Validation:**
```bash
cd phase2/backend
python -c "from app.services.task_service import TaskService; print('Service OK')"
```

---

#### Task 3.4: Create app/api/v1/endpoints/tasks.py
**ID:** `PHASE2-018`
**Type:** Code
**Step:** 3.4

**Description:**
Create task API endpoints router.

**Actions:**
1. Create `phase2/backend/app/api/v1/endpoints/tasks.py`
2. Create APIRouter with prefix="/tasks"
3. Implement POST /tasks (create)
4. Implement GET /tasks (list with filters)
5. Implement GET /tasks/{id} (retrieve)
6. Implement PATCH /tasks/{id} (update)
7. Implement DELETE /tasks/{id} (delete)

**Expected Artifacts:**
- `phase2/backend/app/api/v1/endpoints/tasks.py` (~120 lines)

**Acceptance Criteria:**
- [ ] All 5 endpoints defined
- [ ] Proper status codes (201 for create, 200 for others, 404 for not found)
- [ ] Depends(get_session) for database session
- [ ] HTTPException for errors
- [ ] Response models use SuccessResponse
- [ ] Query parameters for filters
- [ ] Type hints complete

**Validation:**
```bash
cd phase2/backend
python -c "from app.api.v1.endpoints.tasks import router; print(f'{len(router.routes)} routes')"
```

---

#### Task 3.5: Update app/main.py to include tasks router
**ID:** `PHASE2-019`
**Type:** Code
**Step:** 3.5

**Description:**
Register tasks router in main FastAPI app.

**Actions:**
1. Update `phase2/backend/app/main.py`
2. Import tasks router
3. Include router with prefix="/api/v1"

**Expected Artifacts:**
- Updated `phase2/backend/app/main.py`

**Acceptance Criteria:**
- [ ] tasks router imported
- [ ] app.include_router() called
- [ ] Prefix is "/api/v1"
- [ ] App runs without errors

**Validation:**
```bash
cd phase2/backend
# Manual: uvicorn app.main:app --reload
# Visit http://localhost:8000/docs
# Verify 5 task endpoints under /api/v1/tasks
```

---

## Milestone 2: Frontend Foundation (Tasks 20-31)

**Goal:** Basic UI displaying tasks
**Steps Covered:** Steps 4-5 from PLAN.md

---

### Step 4: Frontend Project Setup & API Client

#### Task 4.1: Create Next.js Project
**ID:** `PHASE2-020`
**Type:** Setup
**Step:** 4.1

**Description:**
Initialize Next.js 14 project with TypeScript and Tailwind CSS.

**Actions:**
1. Run create-next-app in phase2 directory
2. Use options: --typescript, --tailwind, --app, --no-src-dir
3. Set import alias to "@/*"

**Expected Artifacts:**
- `phase2/frontend/` directory with Next.js project

**Acceptance Criteria:**
- [ ] Next.js project created
- [ ] TypeScript configured
- [ ] Tailwind CSS configured
- [ ] App Router enabled
- [ ] package.json has correct dependencies
- [ ] npm run dev works

**Validation:**
```bash
cd phase2/frontend
npm run dev
# Visit http://localhost:3000
```

---

#### Task 4.2: Install Additional Dependencies
**ID:** `PHASE2-021`
**Type:** Setup
**Step:** 4.2

**Description:**
Install additional npm packages for date handling.

**Actions:**
1. Install date-fns
2. Install @types/node dev dependency

**Expected Artifacts:**
- Updated `phase2/frontend/package.json`

**Acceptance Criteria:**
- [ ] date-fns in dependencies
- [ ] @types/node in devDependencies
- [ ] npm install succeeds

**Validation:**
```bash
cd phase2/frontend
npm list date-fns
```

---

#### Task 4.3: Create lib/types.ts
**ID:** `PHASE2-022`
**Type:** Code
**Step:** 4.3

**Description:**
Create TypeScript type definitions matching backend schemas.

**Actions:**
1. Create `phase2/frontend/lib/types.ts`
2. Define Priority enum
3. Define Tag, Task interfaces
4. Define TaskCreateInput, TaskUpdateInput
5. Define FilterParams, TaskListResponse, TaskResponse

**Expected Artifacts:**
- `phase2/frontend/lib/types.ts` (~70 lines)

**Acceptance Criteria:**
- [ ] Priority enum matches backend PriorityEnum
- [ ] Task interface matches TaskResponse schema
- [ ] All date fields are strings (ISO format)
- [ ] TaskCreateInput matches TaskCreate schema
- [ ] TaskUpdateInput matches TaskUpdate schema
- [ ] No TypeScript errors

**Validation:**
```bash
cd phase2/frontend
npx tsc --noEmit
```

---

#### Task 4.4: Create lib/api.ts
**ID:** `PHASE2-023`
**Type:** Code
**Step:** 4.4

**Description:**
Create type-safe API client for backend communication.

**Actions:**
1. Create `phase2/frontend/lib/api.ts`
2. Define ApiError class
3. Implement fetchAPI() helper
4. Implement taskApi.list(), get(), create(), update(), delete()
5. Implement tagApi.list(), create()

**Expected Artifacts:**
- `phase2/frontend/lib/api.ts` (~100 lines)

**Acceptance Criteria:**
- [ ] API_BASE_URL from environment variable
- [ ] ApiError captures status and details
- [ ] fetchAPI handles JSON and errors
- [ ] taskApi has 5 methods
- [ ] tagApi has 2 methods
- [ ] All methods return typed promises
- [ ] No TypeScript errors

**Validation:**
```bash
cd phase2/frontend
npx tsc --noEmit
```

---

#### Task 4.5: Create .env.local
**ID:** `PHASE2-024`
**Type:** Configuration
**Step:** 4.5

**Description:**
Create environment variable file for frontend.

**Actions:**
1. Create `phase2/frontend/.env.local`
2. Set NEXT_PUBLIC_API_URL=http://localhost:8000

**Expected Artifacts:**
- `phase2/frontend/.env.local` (~2 lines)

**Content:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Acceptance Criteria:**
- [ ] File exists
- [ ] Variable accessible in lib/api.ts
- [ ] Not committed to git (in .gitignore)

**Validation:**
```bash
cat phase2/frontend/.env.local
```

---

#### Task 4.6: Update tailwind.config.ts
**ID:** `PHASE2-025`
**Type:** Configuration
**Step:** 4.6

**Description:**
Add custom Tailwind colors for priority badges.

**Actions:**
1. Update `phase2/frontend/tailwind.config.ts`
2. Add priority.high, priority.medium, priority.low colors

**Expected Artifacts:**
- Updated `phase2/frontend/tailwind.config.ts`

**Acceptance Criteria:**
- [ ] priority.high = '#EF4444' (red)
- [ ] priority.medium = '#F59E0B' (amber)
- [ ] priority.low = '#3B82F6' (blue)
- [ ] Tailwind build succeeds

**Validation:**
```bash
cd phase2/frontend
npm run build
```

---

### Step 5: Task List Page with Filters

#### Task 5.1: Create components/PriorityBadge.tsx
**ID:** `PHASE2-026`
**Type:** Code
**Step:** 5.2

**Description:**
Create reusable priority badge component.

**Actions:**
1. Create `phase2/frontend/components/PriorityBadge.tsx`
2. Accept priority prop
3. Display colored badge with icon
4. Use Tailwind priority colors

**Expected Artifacts:**
- `phase2/frontend/components/PriorityBadge.tsx` (~30 lines)

**Acceptance Criteria:**
- [ ] Accepts priority: Priority prop
- [ ] High = red badge
- [ ] Medium = amber badge
- [ ] Low = blue badge
- [ ] Displays priority text (capitalized)
- [ ] TypeScript types correct

**Validation:**
Manual inspection in browser

---

#### Task 5.2: Create components/TaskCard.tsx
**ID:** `PHASE2-027`
**Type:** Code
**Step:** 5.1

**Description:**
Create task card component with checkbox and details.

**Actions:**
1. Create `phase2/frontend/components/TaskCard.tsx`
2. Accept task prop
3. Render checkbox for completion
4. Show title, description, priority badge, tags
5. Handle checkbox toggle with API call
6. Use optimistic updates

**Expected Artifacts:**
- `phase2/frontend/components/TaskCard.tsx` (~80 lines)

**Acceptance Criteria:**
- [ ] Client component ('use client')
- [ ] Checkbox calls taskApi.update()
- [ ] Optimistic UI update
- [ ] Displays PriorityBadge
- [ ] Tags displayed as chips
- [ ] Click title navigates to /tasks/{id}
- [ ] TypeScript types correct

**Validation:**
Manual inspection in browser

---

#### Task 5.3: Create components/FilterPanel.tsx
**ID:** `PHASE2-028`
**Type:** Code
**Step:** 5.4

**Description:**
Create filter controls for task list.

**Actions:**
1. Create `phase2/frontend/components/FilterPanel.tsx`
2. Add status filter (all, active, completed)
3. Add priority filter dropdown
4. Add sort dropdown
5. Update URL search params on change

**Expected Artifacts:**
- `phase2/frontend/components/FilterPanel.tsx` (~70 lines)

**Acceptance Criteria:**
- [ ] Client component ('use client')
- [ ] Status buttons (All, Active, Completed)
- [ ] Priority dropdown
- [ ] Sort dropdown (Created, Priority, Due Date, Title)
- [ ] useRouter to update search params
- [ ] TypeScript types correct

**Validation:**
Manual inspection in browser

---

#### Task 5.4: Create components/TaskList.tsx
**ID:** `PHASE2-029`
**Type:** Code
**Step:** 5.3

**Description:**
Create server component that fetches and displays tasks.

**Actions:**
1. Create `phase2/frontend/components/TaskList.tsx`
2. Server component (no 'use client')
3. Accept searchParams prop
4. Call taskApi.list() with filters
5. Render TaskCard for each task
6. Handle empty state

**Expected Artifacts:**
- `phase2/frontend/components/TaskList.tsx` (~50 lines)

**Acceptance Criteria:**
- [ ] Server component (async function)
- [ ] Fetches tasks using searchParams
- [ ] Maps tasks to TaskCard components
- [ ] Empty state message
- [ ] TypeScript types correct

**Validation:**
Manual inspection in browser

---

#### Task 5.5: Create components/Navigation.tsx
**ID:** `PHASE2-030`
**Type:** Code
**Step:** 5.5

**Description:**
Create app navigation header.

**Actions:**
1. Create `phase2/frontend/components/Navigation.tsx`
2. Display app title
3. Add "New Task" button (links to /tasks/new)
4. Responsive design

**Expected Artifacts:**
- `phase2/frontend/components/Navigation.tsx` (~40 lines)

**Acceptance Criteria:**
- [ ] Header with "Todo App - Phase II"
- [ ] "New Task" button with + icon
- [ ] Links to /tasks/new
- [ ] Tailwind styling
- [ ] Mobile responsive

**Validation:**
Manual inspection in browser

---

#### Task 5.6: Create app/page.tsx
**ID:** `PHASE2-031`
**Type:** Code
**Step:** 5.7

**Description:**
Create home page with task list and filters.

**Actions:**
1. Update `phase2/frontend/app/page.tsx`
2. Server component that accepts searchParams
3. Render FilterPanel and TaskList
4. Handle loading state

**Expected Artifacts:**
- Updated `phase2/frontend/app/page.tsx` (~40 lines)

**Acceptance Criteria:**
- [ ] Server component
- [ ] Receives searchParams from Next.js
- [ ] Renders FilterPanel
- [ ] Renders TaskList with searchParams
- [ ] TypeScript types correct

**Validation:**
```bash
cd phase2/frontend
npm run dev
# Visit http://localhost:3000
# Verify task list displays
```

---

## Milestone 3: Full CRUD UI (Tasks 32-44)

**Goal:** Complete user workflows
**Steps Covered:** Steps 6-8 from PLAN.md

---

### Step 6: Create & Edit Task Forms

#### Task 6.1: Create components/PrioritySelector.tsx
**ID:** `PHASE2-032`
**Type:** Code
**Step:** 6.3

**Description:**
Create priority selection component.

**Actions:**
1. Create `phase2/frontend/components/PrioritySelector.tsx`
2. Radio buttons or dropdown for High, Medium, Low
3. Controlled component

**Expected Artifacts:**
- `phase2/frontend/components/PrioritySelector.tsx` (~40 lines)

**Acceptance Criteria:**
- [ ] Accepts value and onChange props
- [ ] Displays 3 priority options
- [ ] Highlights selected priority
- [ ] TypeScript types correct

**Validation:**
Manual inspection in form

---

#### Task 6.2: Create components/DueDatePicker.tsx
**ID:** `PHASE2-033`
**Type:** Code
**Step:** 6.4

**Description:**
Create date picker component.

**Actions:**
1. Create `phase2/frontend/components/DueDatePicker.tsx`
2. Use HTML5 date input or date library
3. Optional field with clear button

**Expected Artifacts:**
- `phase2/frontend/components/DueDatePicker.tsx` (~30 lines)

**Acceptance Criteria:**
- [ ] Accepts value (string | undefined) and onChange
- [ ] Renders date input
- [ ] Clear button to set to undefined
- [ ] TypeScript types correct

**Validation:**
Manual inspection in form

---

#### Task 6.3: Create components/TagInput.tsx
**ID:** `PHASE2-034`
**Type:** Code
**Step:** 6.2

**Description:**
Create tag input with autocomplete.

**Actions:**
1. Create `phase2/frontend/components/TagInput.tsx`
2. Fetch existing tags from tagApi.list()
3. Autocomplete input
4. Display selected tags as chips
5. Allow adding new tags

**Expected Artifacts:**
- `phase2/frontend/components/TagInput.tsx` (~90 lines)

**Acceptance Criteria:**
- [ ] Client component
- [ ] Fetches tags on mount
- [ ] Autocomplete dropdown
- [ ] Selected tags displayed as removable chips
- [ ] Can add new tags
- [ ] TypeScript types correct

**Validation:**
Manual inspection in form

---

#### Task 6.4: Create components/TaskForm.tsx
**ID:** `PHASE2-035`
**Type:** Code
**Step:** 6.1

**Description:**
Create task creation/editing form component.

**Actions:**
1. Create `phase2/frontend/components/TaskForm.tsx`
2. Form fields: title, description, priority, due_date, tags
3. Validation (title required, max lengths)
4. Submit handler calling taskApi.create() or update()
5. Loading state during submission
6. Error handling

**Expected Artifacts:**
- `phase2/frontend/components/TaskForm.tsx` (~150 lines)

**Acceptance Criteria:**
- [ ] Client component
- [ ] Accepts task prop (optional, for edit mode)
- [ ] All form fields with validation
- [ ] Uses PrioritySelector, DueDatePicker, TagInput
- [ ] Submit button disabled while loading
- [ ] Displays validation errors
- [ ] Calls onSuccess callback
- [ ] TypeScript types correct

**Validation:**
Manual testing in browser

---

#### Task 6.5: Create app/tasks/new/page.tsx
**ID:** `PHASE2-036`
**Type:** Code
**Step:** 6.5

**Description:**
Create new task page.

**Actions:**
1. Create `phase2/frontend/app/tasks/new/page.tsx`
2. Render TaskForm without task prop
3. Handle success with redirect to home
4. Show toast on success

**Expected Artifacts:**
- `phase2/frontend/app/tasks/new/page.tsx` (~40 lines)

**Acceptance Criteria:**
- [ ] Client component (needs form interactivity)
- [ ] Renders TaskForm
- [ ] onSuccess redirects to /
- [ ] Shows success toast
- [ ] Cancel button goes back

**Validation:**
```bash
# Visit http://localhost:3000/tasks/new
# Fill form and submit
# Verify redirect and task created
```

---

#### Task 6.6: Create app/tasks/[id]/page.tsx
**ID:** `PHASE2-037`
**Type:** Code
**Step:** 6.6

**Description:**
Create edit task page with dynamic route.

**Actions:**
1. Create `phase2/frontend/app/tasks/[id]/page.tsx`
2. Fetch task by ID (server component wrapper)
3. Render TaskForm with task prop
4. Handle success with redirect

**Expected Artifacts:**
- `phase2/frontend/app/tasks/[id]/page.tsx` (~50 lines)

**Acceptance Criteria:**
- [ ] Server component fetches task
- [ ] Client TaskForm component rendered
- [ ] Form pre-filled with task data
- [ ] onSuccess redirects to /
- [ ] 404 if task not found

**Validation:**
```bash
# Visit http://localhost:3000/tasks/1
# Edit and submit
# Verify task updated
```

---

### Step 7: Tags API & Management

#### Task 7.1: Create app/api/v1/endpoints/tags.py
**ID:** `PHASE2-038`
**Type:** Code
**Step:** 7.1

**Description:**
Create tags API endpoints.

**Actions:**
1. Create `phase2/backend/app/api/v1/endpoints/tags.py`
2. Create APIRouter with prefix="/tags"
3. Implement GET /tags (list)
4. Implement POST /tags (create)

**Expected Artifacts:**
- `phase2/backend/app/api/v1/endpoints/tags.py` (~50 lines)

**Acceptance Criteria:**
- [ ] Router defined
- [ ] GET /tags returns all user's tags
- [ ] POST /tags creates new tag
- [ ] Response uses SuccessResponse
- [ ] Type hints complete

**Validation:**
```bash
curl http://localhost:8000/api/v1/tags
```

---

#### Task 7.2: Include tags router in main.py
**ID:** `PHASE2-039`
**Type:** Code
**Step:** 7.2

**Description:**
Register tags router in main app.

**Actions:**
1. Update `phase2/backend/app/main.py`
2. Import tags router
3. Include with prefix="/api/v1"

**Expected Artifacts:**
- Updated `phase2/backend/app/main.py`

**Acceptance Criteria:**
- [ ] tags router imported
- [ ] app.include_router() called
- [ ] /api/v1/tags endpoints visible in /docs

**Validation:**
```bash
# Visit http://localhost:8000/docs
# Verify tags endpoints present
```

---

#### Task 7.3: (Optional) Create app/tags/page.tsx
**ID:** `PHASE2-040`
**Type:** Code
**Step:** 7.3

**Description:**
Create optional tag management page.

**Actions:**
1. Create `phase2/frontend/app/tags/page.tsx`
2. List all tags
3. Add new tag form
4. Delete tag button

**Expected Artifacts:**
- `phase2/frontend/app/tags/page.tsx` (~80 lines)

**Acceptance Criteria:**
- [ ] Displays all tags
- [ ] Form to create new tag
- [ ] Delete button per tag
- [ ] TypeScript types correct

**Validation:**
Manual testing in browser

---

### Step 8: Error Handling & Loading States

#### Task 8.1: Create components/ui/Loader.tsx
**ID:** `PHASE2-041`
**Type:** Code
**Step:** 8.2

**Description:**
Create loading spinner component.

**Actions:**
1. Create `phase2/frontend/components/ui/Loader.tsx`
2. Animated spinner SVG or CSS
3. Accept size prop

**Expected Artifacts:**
- `phase2/frontend/components/ui/Loader.tsx` (~30 lines)

**Acceptance Criteria:**
- [ ] Displays spinner animation
- [ ] Accepts size prop (sm, md, lg)
- [ ] Tailwind styling

**Validation:**
Manual inspection

---

#### Task 8.2: Create components/ui/Toast.tsx
**ID:** `PHASE2-042`
**Type:** Code
**Step:** 8.1

**Description:**
Create toast notification component.

**Actions:**
1. Create `phase2/frontend/components/ui/Toast.tsx`
2. Support success, error, info types
3. Auto-dismiss after timeout
4. Position fixed bottom-right

**Expected Artifacts:**
- `phase2/frontend/components/ui/Toast.tsx` (~60 lines)

**Acceptance Criteria:**
- [ ] Client component
- [ ] Accepts message, type, onClose
- [ ] Auto-dismisses after 3 seconds
- [ ] Color-coded by type
- [ ] TypeScript types correct

**Validation:**
Manual testing

---

#### Task 8.3: Create lib/utils.ts
**ID:** `PHASE2-043`
**Type:** Code
**Step:** 8.3

**Description:**
Create utility functions for error formatting.

**Actions:**
1. Create `phase2/frontend/lib/utils.ts`
2. Add formatError() to extract user-friendly messages
3. Add other helper functions as needed

**Expected Artifacts:**
- `phase2/frontend/lib/utils.ts` (~30 lines)

**Acceptance Criteria:**
- [ ] formatError(error: unknown) => string
- [ ] Handles ApiError, Error, unknown
- [ ] TypeScript types correct

**Validation:**
```bash
cd phase2/frontend
npx tsc --noEmit
```

---

#### Task 8.4: Add loading and error states to TaskList
**ID:** `PHASE2-044`
**Type:** Code
**Step:** 8.4

**Description:**
Update TaskList to show loading spinner and error messages.

**Actions:**
1. Update `phase2/frontend/components/TaskList.tsx`
2. Add try-catch for API calls
3. Show Loader while fetching
4. Show error message on failure

**Expected Artifacts:**
- Updated `phase2/frontend/components/TaskList.tsx`

**Acceptance Criteria:**
- [ ] Loading state shows Loader
- [ ] Error caught and displayed
- [ ] Uses formatError() for messages

**Validation:**
Manual testing (disconnect backend to trigger error)

---

## Milestone 4: Testing & Quality (Tasks 45-52)

**Goal:** Production-ready application
**Steps Covered:** Steps 9-10 from PLAN.md

---

### Step 9: Backend Testing

#### Task 9.1: Create tests/conftest.py
**ID:** `PHASE2-045`
**Type:** Testing
**Step:** 9.1

**Description:**
Create pytest fixtures for testing.

**Actions:**
1. Create `phase2/backend/tests/conftest.py`
2. Create test database fixture
3. Create async client fixture
4. Create test session fixture

**Expected Artifacts:**
- `phase2/backend/tests/conftest.py` (~60 lines)

**Acceptance Criteria:**
- [ ] pytest fixtures defined
- [ ] test_db_session creates clean DB per test
- [ ] test_client provides httpx AsyncClient
- [ ] Uses in-memory SQLite or test database

**Validation:**
```bash
cd phase2/backend
pytest tests/conftest.py -v
```

---

#### Task 9.2: Create tests/test_models.py
**ID:** `PHASE2-046`
**Type:** Testing
**Step:** 9.4

**Description:**
Write tests for SQLModel models.

**Actions:**
1. Create `phase2/backend/tests/test_models.py`
2. Test Task model creation
3. Test relationships (task.tags, task.user)
4. Test PriorityEnum

**Expected Artifacts:**
- `phase2/backend/tests/test_models.py` (~50 lines, 5+ tests)

**Acceptance Criteria:**
- [ ] Tests create Task instances
- [ ] Tests verify relationships
- [ ] Tests check default values
- [ ] All tests pass

**Validation:**
```bash
cd phase2/backend
pytest tests/test_models.py -v
```

---

#### Task 9.3: Create tests/test_task_service.py
**ID:** `PHASE2-047`
**Type:** Testing
**Step:** 9.2

**Description:**
Write unit tests for TaskService.

**Actions:**
1. Create `phase2/backend/tests/test_task_service.py`
2. Test create_task()
3. Test list_tasks() with filters
4. Test get_task()
5. Test update_task()
6. Test delete_task()

**Expected Artifacts:**
- `phase2/backend/tests/test_task_service.py` (~100 lines, 10+ tests)

**Acceptance Criteria:**
- [ ] Each service method has 2+ tests
- [ ] Tests use fixtures
- [ ] Tests cover error cases
- [ ] All tests pass

**Validation:**
```bash
cd phase2/backend
pytest tests/test_task_service.py -v
```

---

#### Task 9.4: Create tests/test_api_tasks.py
**ID:** `PHASE2-048`
**Type:** Testing
**Step:** 9.3

**Description:**
Write integration tests for task API endpoints.

**Actions:**
1. Create `phase2/backend/tests/test_api_tasks.py`
2. Test POST /api/v1/tasks (201 Created)
3. Test GET /api/v1/tasks (200 OK, filtering)
4. Test GET /api/v1/tasks/{id} (200 OK, 404 Not Found)
5. Test PATCH /api/v1/tasks/{id} (200 OK, 404, 422)
6. Test DELETE /api/v1/tasks/{id} (200 OK, 404)

**Expected Artifacts:**
- `phase2/backend/tests/test_api_tasks.py` (~120 lines, 12+ tests)

**Acceptance Criteria:**
- [ ] Each endpoint has 2+ tests
- [ ] Tests verify status codes
- [ ] Tests verify response schemas
- [ ] Tests cover error cases (404, 422)
- [ ] All tests pass

**Validation:**
```bash
cd phase2/backend
pytest tests/test_api_tasks.py -v
```

---

#### Task 9.5: Run coverage report
**ID:** `PHASE2-049`
**Type:** Testing
**Step:** 9

**Description:**
Generate test coverage report and verify ≥80%.

**Actions:**
1. Run pytest with --cov flag
2. Generate HTML coverage report
3. Verify coverage ≥80%

**Expected Artifacts:**
- Coverage report (terminal and HTML)

**Acceptance Criteria:**
- [ ] pytest --cov=app runs successfully
- [ ] Coverage ≥80%
- [ ] HTML report generated

**Validation:**
```bash
cd phase2/backend
pytest --cov=app --cov-report=term-missing --cov-report=html tests/
# Check htmlcov/index.html
```

---

### Step 10: Documentation & Deployment Prep

#### Task 10.1: Update backend/README.md
**ID:** `PHASE2-050`
**Type:** Documentation
**Step:** 10.1

**Description:**
Complete backend README with full documentation.

**Actions:**
1. Update `phase2/backend/README.md`
2. Add complete setup instructions
3. Document all environment variables
4. Add API documentation link
5. Add testing instructions

**Expected Artifacts:**
- Updated `phase2/backend/README.md` (~150 lines)

**Acceptance Criteria:**
- [ ] Setup section complete
- [ ] Environment variables documented
- [ ] Running instructions clear
- [ ] Testing commands included
- [ ] API docs link (/docs)

**Validation:**
```bash
cat phase2/backend/README.md
```

---

#### Task 10.2: Create frontend/README.md
**ID:** `PHASE2-051`
**Type:** Documentation
**Step:** 10.2

**Description:**
Create frontend README with setup and development instructions.

**Actions:**
1. Create `phase2/frontend/README.md`
2. Add setup instructions
3. Document environment variables
4. Add development workflow
5. Add build instructions

**Expected Artifacts:**
- `phase2/frontend/README.md` (~100 lines)

**Acceptance Criteria:**
- [ ] Setup section complete
- [ ] Environment variables documented
- [ ] npm commands explained
- [ ] Development workflow clear

**Validation:**
```bash
cat phase2/frontend/README.md
```

---

#### Task 10.3: Create docker-compose.yml
**ID:** `PHASE2-052`
**Type:** Configuration
**Step:** 10.3

**Description:**
Create docker-compose for local development environment.

**Actions:**
1. Create `phase2/docker-compose.yml`
2. Define postgres service
3. Define backend service
4. Define frontend service
5. Configure networking and volumes

**Expected Artifacts:**
- `phase2/docker-compose.yml` (~60 lines)

**Acceptance Criteria:**
- [ ] PostgreSQL service configured
- [ ] Backend service configured
- [ ] Frontend service configured
- [ ] Networks and volumes defined
- [ ] docker-compose up works

**Validation:**
```bash
cd phase2
docker-compose up
# Verify all services start
```

---

## Task Summary

### By Milestone:
- **Milestone 1 (Backend):** 19 tasks
- **Milestone 2 (Frontend Setup):** 12 tasks
- **Milestone 3 (Full CRUD):** 13 tasks
- **Milestone 4 (Testing & Docs):** 8 tasks

**Total:** 52 tasks

### By Type:
- **Code:** 35 tasks
- **Configuration:** 8 tasks
- **Setup:** 4 tasks
- **Testing:** 5 tasks
- **Documentation:** 3 tasks
- **Database:** 1 task

### By Complexity:
- **Simple:** 15 tasks (setup, config, simple components)
- **Medium:** 25 tasks (components, services, tests)
- **Complex:** 12 tasks (forms, API integration, service logic)

---

## Execution Notes

### Prerequisites
1. Neon PostgreSQL database created and DATABASE_URL available
2. Node.js 18+ installed
3. Python 3.10+ installed
4. Git repository initialized

### Recommended Execution Order
1. Complete all Milestone 1 tasks (backend foundation)
2. Verify backend works via Swagger UI (/docs)
3. Complete Milestone 2 (frontend setup)
4. Verify frontend displays tasks
5. Complete Milestone 3 (full CRUD UI)
6. Complete Milestone 4 (testing and docs)

### Testing Strategy
- Test each task immediately after completion
- Run validation commands after each task
- Manual testing in browser for UI components
- Automated tests for backend logic

### Risk Mitigation
- **Database Connection:** Test early (Task PHASE2-005)
- **CORS Issues:** Verify in Task PHASE2-005
- **Type Mismatches:** Validate in Tasks PHASE2-022, PHASE2-023
- **API Integration:** Test end-to-end after Task PHASE2-031

---

**Status:** READY FOR EXECUTION
**Created:** 2025-12-26
**Version:** 1.0.0

**Next Action:** Begin execution with Task PHASE2-001 or request Claude Code to execute all tasks automatically.
