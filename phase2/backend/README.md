# Todo API - Phase II Backend

RESTful API built with FastAPI, SQLModel, and PostgreSQL for the Evolution of Todo project.

## Features

- **7 RESTful API endpoints** (5 task endpoints + 2 tag endpoints)
- **Async/await** throughout with async SQLModel
- **Full CRUD** operations for tasks
- **Task priorities** (high, medium, low)
- **Tags** with many-to-many relationships
- **Filtering & sorting** (by status, priority, tags, date)
- **Due dates** with overdue detection
- **Auto-generated OpenAPI docs** at `/docs`
- **CORS** enabled for Next.js frontend
- **Database migrations** with Alembic

## Technology Stack

- **FastAPI** - Modern async Python web framework
- **SQLModel** - SQL databases using Python type annotations
- **Pydantic v2** - Data validation and serialization
- **PostgreSQL** - Production database (Neon managed)
- **SQLite** - Testing database (aiosqlite)
- **Alembic** - Database migration tool
- **pytest** - Testing framework

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Settings (Pydantic)
│   ├── database.py             # Async engine & sessions
│   ├── models/                 # SQLModel models
│   │   ├── user.py
│   │   ├── tag.py
│   │   └── task.py
│   ├── schemas/                # Pydantic request/response schemas
│   │   ├── common.py
│   │   └── task.py
│   ├── services/               # Business logic
│   │   └── task_service.py
│   └── api/v1/endpoints/       # API routes
│       ├── tasks.py
│       └── tags.py
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
├── scripts/
│   └── seed_data.py            # Seed development data
├── tests/                      # pytest tests
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_task_service.py
│   └── test_api_tasks.py
├── requirements.txt
├── alembic.ini
├── .env.example
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- PostgreSQL database (or use SQLite for testing)

### 1. Clone and Navigate

```bash
cd /mnt/d/Data/GIAIC/hackathon2/phase2/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file from template:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# For PostgreSQL (production)
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/todo_db

# For SQLite (testing)
DATABASE_URL=sqlite+aiosqlite:///./test.db

CORS_ORIGINS=http://localhost:3000
DEBUG=True
LOG_LEVEL=INFO
```

### 5. Run Database Migrations

**Note:** Alembic requires manual installation if running migrations. For SQLite testing, the app will auto-create tables on startup.

```bash
# Create initial migration (if not exists)
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

### 6. Seed Development Data (Optional)

```bash
python scripts/seed_data.py
```

This creates:
- Default user (id=1)
- Sample tags (personal, work, urgent, shopping)
- Sample tasks

## Running the Application

### Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

### Production Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/tasks` | Create new task |
| GET | `/api/v1/tasks` | List tasks (with filters) |
| GET | `/api/v1/tasks/{id}` | Get task by ID |
| PATCH | `/api/v1/tasks/{id}` | Update task |
| DELETE | `/api/v1/tasks/{id}` | Delete task |

### Tags

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/tags` | List all tags |
| POST | `/api/v1/tags` | Create new tag |

### Query Parameters (List Tasks)

- `status` - Filter by status: `all`, `active`, `completed` (default: `all`)
- `priority` - Filter by priority: `high`, `medium`, `low`
- `tag` - Filter by tag name (can specify multiple)
- `sort` - Sort order: `created_desc`, `created_asc`, `priority_desc`, `due_asc`, `title_asc` (default: `created_desc`)
- `limit` - Max results (default: 100, max: 1000)
- `offset` - Pagination offset (default: 0)

### Example Requests

**Create Task:**

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "high",
    "due_date": "2025-12-31T23:59:59Z",
    "tags": ["personal", "shopping"]
  }'
```

**List Active Tasks:**

```bash
curl "http://localhost:8000/api/v1/tasks?status=active&sort=priority_desc"
```

**Update Task:**

```bash
curl -X PATCH http://localhost:8000/api/v1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

## Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=term-missing --cov-report=html
```

Coverage report will be generated in `htmlcov/index.html`.

### Run Specific Test Files

```bash
pytest tests/test_models.py
pytest tests/test_task_service.py
pytest tests/test_api_tasks.py
```

## Database Schema

### Tables

- **users** - User accounts (placeholder for Phase II)
- **tasks** - Todo tasks with all fields
- **tags** - Tags for categorization
- **task_tags** - Join table for many-to-many relationship

### Relationships

- User → Tasks (one-to-many)
- User → Tags (one-to-many)
- Tasks ↔ Tags (many-to-many via task_tags)

## Development Workflow

1. Create feature branch
2. Make changes to models/services/endpoints
3. Generate migration: `alembic revision --autogenerate -m "description"`
4. Review and edit migration file
5. Apply migration: `alembic upgrade head`
6. Write tests
7. Run tests: `pytest`
8. Check coverage: `pytest --cov=app`
9. Commit and push

## Troubleshooting

### Database Connection Issues

If using SQLite for testing:
```env
DATABASE_URL=sqlite+aiosqlite:///./test.db
```

The app will auto-create tables on startup (no Alembic needed).

### CORS Errors

Ensure `.env` has correct frontend URL:
```env
CORS_ORIGINS=http://localhost:3000
```

### Import Errors

Ensure you're in the virtual environment:
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

## Next Steps

- Integrate with frontend (Next.js)
- Add user authentication (Phase III)
- Deploy to production
- Set up CI/CD pipeline

## API Documentation

Full interactive API documentation with examples is available at `/docs` when the server is running.

## License

Part of the Evolution of Todo hackathon project.
