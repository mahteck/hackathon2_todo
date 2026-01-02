# Todo App - Phase I (Console)

**Evolution of Todo Project - Phase I**

A foundational, in-memory Todo application with a Python console interface. This phase establishes core domain logic and business rules that will evolve through subsequent phases.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Command Reference](#command-reference)
- [Examples](#examples)
- [Development](#development)
- [Architecture](#architecture)
- [Limitations](#limitations)
- [Next Phase](#next-phase)

---

## Features

✅ **Core Task Management**
- Add new tasks with title and optional description
- View all tasks in a formatted table
- View detailed information for specific tasks
- Update task title and/or description
- Delete tasks permanently
- Mark tasks as complete/incomplete

✅ **Data Validation**
- Title validation (1-200 characters, non-empty)
- Description validation (0-1000 characters)
- Clear, actionable error messages

✅ **Clean Architecture**
- 3-layer design (CLI → Service → Repository)
- Separation of concerns
- Comprehensive test coverage (≥80%)

---

## Requirements

- **Python**: 3.10 or higher
- **Runtime Dependencies**: None (Python standard library only)
- **Development Dependencies**: pytest, pytest-cov, mypy, ruff (see `requirements.txt`)

---

## Installation

### 1. Clone or Download

```bash
cd phase1
```

### 2. (Optional) Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Development Dependencies (Optional - for testing)

```bash
pip install -r requirements.txt
```

---

## Usage

### Starting the Application

```bash
python src/main.py
```

```wsl/linux/ubuntu
python src/main.py
```

You'll see:

```
╔════════════════════════════════════════════════╗
║      Todo App - Phase I (Console)             ║
║      Evolution of Todo Project                ║
╚════════════════════════════════════════════════╝

Type 'help' for available commands.

>
```

### Basic Workflow

```bash
# Add a task
> add "Buy groceries"

# List all tasks
> list

# Mark task as complete
> complete 1

# Exit the application
> exit
```

---

## Command Reference

| Command | Syntax | Description | Example |
|---------|--------|-------------|---------|
| `add` | `add <title> [description]` | Create a new task | `add "Buy milk" "2% milk"` |
| `list` | `list` | Display all tasks | `list` |
| `view` | `view <id>` | Show task details | `view 1` |
| `update` | `update <id> [--title <title>] [--description <desc>]` | Update task | `update 1 --title "New title"` |
| `delete` | `delete <id>` | Delete a task | `delete 1` |
| `complete` | `complete <id>` | Mark as complete | `complete 1` |
| `uncomplete` | `uncomplete <id>` | Mark as incomplete | `uncomplete 1` |
| `help` | `help` | Show help message | `help` |
| `exit` | `exit` | Exit application | `exit` |

### Command Details

#### add - Create Task
```bash
# With title only
> add "Buy groceries"

# With title and description
> add "Finish report" "Q4 financial analysis"
```

#### list - View All Tasks
```bash
> list

ID | Status | Title                                      | Created
---+--------+--------------------------------------------+-------------------
1  | [ ]    | Buy groceries                              | 2025-12-26 10:30
2  | [✓]    | Finish report                              | 2025-12-26 09:15

Total: 2 tasks (1 completed, 1 incomplete)
```

#### view - View Task Details
```bash
> view 1

Task Details
────────────────────────────────────────
ID:          1
Title:       Buy groceries
Description: Milk, eggs, bread
Status:      Incomplete
Created:     2025-12-26 10:30
Updated:     2025-12-26 10:30
```

#### update - Modify Task
```bash
# Update title only
> update 1 --title "Buy groceries and snacks"

# Update description only
> update 1 --description "Don't forget the milk"

# Update both
> update 1 --title "Shopping" --description "Weekly groceries"
```

#### delete - Remove Task
```bash
> delete 1
✓ Task deleted successfully
  Deleted task #1: "Buy groceries"
```

#### complete/uncomplete - Toggle Status
```bash
> complete 1
✓ Task marked as complete
  Task #1: "Buy groceries" ✓

> uncomplete 1
✓ Task marked as incomplete
  Task #1: "Buy groceries" [ ]
```

---

## Examples

### Example Session 1: Quick Task Management

```bash
> add "Call dentist"
✓ Task created successfully
  ID: 1
  Title: Call dentist
  Status: Incomplete

> add "Submit expense report" "Due by Friday"
✓ Task created successfully
  ID: 2
  Title: Submit expense report
  Description: Due by Friday
  Status: Incomplete

> list
ID | Status | Title                                      | Created
---+--------+--------------------------------------------+-------------------
1  | [ ]    | Call dentist                               | 2025-12-26 14:00
2  | [ ]    | Submit expense report                      | 2025-12-26 14:01

Total: 2 tasks (0 completed, 2 incomplete)

> complete 1
✓ Task marked as complete
  Task #1: "Call dentist" ✓

> list
ID | Status | Title                                      | Created
---+--------+--------------------------------------------+-------------------
1  | [✓]    | Call dentist                               | 2025-12-26 14:00
2  | [ ]    | Submit expense report                      | 2025-12-26 14:01

Total: 2 tasks (1 completed, 1 incomplete)

> delete 1
✓ Task deleted successfully
  Deleted task #1: "Call dentist"

> exit
Goodbye! Your tasks are not saved (in-memory only).
```

### Example Session 2: Task Updates

```bash
> add "Project deadline"
✓ Task created successfully
  ID: 1

> view 1
Task Details
────────────────────────────────────────
ID:          1
Title:       Project deadline
Description: None
Status:      Incomplete
Created:     2025-12-26 14:05
Updated:     2025-12-26 14:05

> update 1 --description "Presentation slides due Monday"
✓ Task updated successfully
  ID: 1
  Title: Project deadline
  Description: Presentation slides due Monday

> update 1 --title "Team presentation - Monday"
✓ Task updated successfully
  ID: 1
  Title: Team presentation - Monday

> view 1
Task Details
────────────────────────────────────────
ID:          1
Title:       Team presentation - Monday
Description: Presentation slides due Monday
Status:      Incomplete
Created:     2025-12-26 14:05
Updated:     2025-12-26 14:07
```

---

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_task_service.py

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=src --cov-report=html
```

### Type Checking

```bash
mypy src/
```

### Linting

```bash
ruff check src/ tests/
```

### Project Structure

```
phase1/
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── task_service.py      # Business logic
│   ├── task_repository.py   # Data access
│   ├── models.py            # Data structures
│   ├── exceptions.py        # Custom exceptions
│   ├── cli_formatter.py     # Display formatting
│   └── command_parser.py    # Input parsing
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures
│   ├── test_task_repository.py
│   ├── test_task_service.py
│   ├── test_models.py
│   └── test_integration.py
├── requirements.txt         # Dev dependencies
├── README.md               # This file
├── ARCHITECTURE.md         # Design documentation
└── TESTING.md             # Testing guide
```

---

## Architecture

### 3-Layer Design

```
┌──────────────────────────────────┐
│  Presentation Layer (CLI)        │
│  - main.py                       │
│  - cli_formatter.py              │
│  - command_parser.py             │
└──────────────────────────────────┘
            ↓ ↑
┌──────────────────────────────────┐
│  Business Logic Layer            │
│  - task_service.py               │
│  - Validation & orchestration    │
└──────────────────────────────────┘
            ↓ ↑
┌──────────────────────────────────┐
│  Data Layer                      │
│  - task_repository.py            │
│  - In-memory storage (dict)      │
└──────────────────────────────────┘
```

### Key Design Principles

- **Separation of Concerns**: Each layer has distinct responsibilities
- **Dependency Injection**: Service receives repository instance
- **Domain-Driven**: Task entity is well-defined with clear invariants
- **Fail-Fast Validation**: Input validation at service layer
- **Evolution-Ready**: Code structure prepares for Phase II migration

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed design documentation.

---

## Limitations

⚠️ **Important Constraints**

- **No Persistence**: All data is lost when the application exits
- **In-Memory Only**: No database or file storage
- **Single-User**: Not designed for concurrent access
- **Local Only**: No network or multi-machine support

These are intentional design choices for Phase I. Phase II will introduce:
- Persistent storage (PostgreSQL via Neon DB)
- Web UI (Next.js frontend)
- RESTful API (FastAPI backend)

---

## Next Phase

**Phase II: Full-Stack Web Application**

Phase II will transform this console app into a full-stack web application:

- **Frontend**: Next.js 14+ with TypeScript
- **Backend**: FastAPI with async/await
- **Database**: PostgreSQL (Neon DB) with SQLModel ORM
- **New Features**: Priorities, tags, search, filter, sort

The business logic from this phase will be adapted and extended, demonstrating the value of clean architecture.

---

## Testing Coverage

- **Unit Tests**: Repository, Service, Models
- **Integration Tests**: Complete user workflows
- **Coverage Target**: ≥80% line coverage
- **Total Tests**: 40+ test cases

See [TESTING.md](./TESTING.md) for testing strategy and guidelines.

---

## Contributing

This is a hackathon project following **Spec-Driven Development**:

1. All production code is generated by Claude Code
2. Modifications require spec refinement, not manual coding
3. Tests validate spec compliance

For Phase II+ contributions, please maintain this methodology.

---

## License

Part of the "Evolution of Todo" educational project.

---

## Support

For questions or issues:
- Review [ARCHITECTURE.md](./ARCHITECTURE.md) for design details
- Check [TESTING.md](./TESTING.md) for testing guidance
- Refer to [Global Constitution](../CONSTITUTION.md) for project principles

---

**Status**: ✅ Phase I Complete - Ready for Phase II Planning

**Version**: 1.0.0
**Last Updated**: 2025-12-26
