# Phase I Constitution - Console Todo App

**Phase:** I - Console Foundation
**Version:** 1.0.0
**Status:** Draft
**Parent:** [Global Constitution](../CONSTITUTION.md)

---

## Phase Overview

### Purpose
Build a foundational, in-memory Todo application using Python console interface to establish core domain logic and business rules that will evolve through all subsequent phases.

### Strategic Goals
1. **Establish domain model**: Define the canonical Todo entity and operations
2. **Prove core workflows**: Validate CRUD operations and task management logic
3. **Set quality baseline**: Demonstrate test-driven development and clean architecture
4. **Create migration foundation**: Build data structures that can evolve into database schemas

### Technology Stack
- **Language**: Python 3.10+
- **Storage**: In-memory (Python lists and dictionaries)
- **Interface**: Command-line interface (CLI)
- **Testing**: pytest with ≥80% code coverage
- **Dependencies**: Python standard library only (no external packages except dev tools)

---

## Phase-Specific Principles

### 1. Simplicity First
- Use native Python data structures (no ORM, no database)
- Direct function calls (no web framework, no API layer)
- Clear, readable code over clever abstractions
- Minimal dependencies to reduce complexity

### 2. Domain-Driven Foundation
- **Task** is the core entity - design it carefully
- Business logic must be independent of I/O (console interface)
- Domain rules must be explicit and testable
- Data validation happens at domain layer, not UI layer

### 3. Evolution-Ready Design
- Use dictionaries/classes that map naturally to JSON and database schemas
- Separate concerns: UI (console) ↔ Business Logic ↔ Data Storage
- Write logic that can be extracted to services in Phase II
- Document assumptions for future migration

---

## Functional Requirements

### Basic Features (MUST HAVE)

#### F1: Add Task
- **User Story**: As a user, I can add a new task with a title so I can track things I need to do
- **Acceptance Criteria**:
  - Task must have a unique ID (auto-generated)
  - Task must have a non-empty title (max 200 characters)
  - Task defaults to incomplete status
  - Task creation timestamp is recorded
  - System confirms task creation with ID and title
- **Edge Cases**:
  - Empty title → reject with error message
  - Title exceeds 200 chars → reject with error message
  - Duplicate title → allow (different tasks can have same title)

#### F2: View All Tasks
- **User Story**: As a user, I can view all my tasks so I can see what needs to be done
- **Acceptance Criteria**:
  - Display all tasks with ID, title, status, created date
  - Show total count of tasks
  - Show count of complete vs incomplete tasks
  - If no tasks exist, show helpful message
- **Display Format**:
  ```
  ID | Status | Title                  | Created
  ---+--------+------------------------+-------------------
  1  | [ ]    | Buy groceries          | 2025-12-26 10:30
  2  | [✓]    | Finish report          | 2025-12-26 09:15

  Total: 2 tasks (1 complete, 1 incomplete)
  ```

#### F3: View Single Task
- **User Story**: As a user, I can view details of a specific task
- **Acceptance Criteria**:
  - User provides task ID
  - System displays all task attributes in detail
  - If task ID doesn't exist → clear error message
- **Edge Cases**:
  - Invalid ID format (non-numeric) → error message
  - ID not found → "Task #X not found"

#### F4: Update Task
- **User Story**: As a user, I can update a task's title so I can correct or clarify it
- **Acceptance Criteria**:
  - User provides task ID and new title
  - System validates new title (non-empty, ≤200 chars)
  - System updates task and records modification timestamp
  - System confirms update with new details
- **Edge Cases**:
  - Task ID not found → error message
  - Empty new title → reject
  - Title exceeds 200 chars → reject

#### F5: Delete Task
- **User Story**: As a user, I can delete a task I no longer need
- **Acceptance Criteria**:
  - User provides task ID
  - System confirms deletion intent
  - System removes task permanently
  - System confirms successful deletion
- **Edge Cases**:
  - Task ID not found → error message
  - User cancels confirmation → task not deleted

#### F6: Mark Task Complete/Incomplete
- **User Story**: As a user, I can mark tasks as complete or incomplete to track my progress
- **Acceptance Criteria**:
  - User provides task ID
  - System toggles status (incomplete ↔ complete)
  - System records completion timestamp
  - System confirms new status
- **Edge Cases**:
  - Task ID not found → error message
  - Marking complete task as complete again → idempotent (no error)

---

## Data Model

### Task Entity

```python
Task = {
    "id": int,              # Unique identifier, auto-increment
    "title": str,           # Task title (1-200 characters)
    "status": str,          # "incomplete" or "complete"
    "created_at": datetime, # ISO 8601 timestamp
    "updated_at": datetime, # ISO 8601 timestamp
    "completed_at": datetime | None  # ISO 8601 timestamp or None
}
```

### Invariants
- `id` must be unique and positive
- `title` must not be empty and ≤200 characters
- `status` must be either "incomplete" or "complete"
- `created_at` is immutable after creation
- `updated_at` is set on any modification
- `completed_at` is set only when status becomes "complete"

### Storage Structure
```python
# In-memory storage
tasks: dict[int, Task] = {}  # Key: task ID, Value: Task dict
next_id: int = 1             # Counter for auto-increment IDs
```

---

## Architecture

### Layered Architecture

```
┌─────────────────────────────────┐
│   Presentation Layer (CLI)      │  ← User interaction
│   - main.py                      │
│   - display helpers              │
└─────────────────────────────────┘
            ↓ ↑
┌─────────────────────────────────┐
│   Business Logic Layer          │  ← Core domain logic
│   - task_service.py              │
│   - validation rules             │
└─────────────────────────────────┘
            ↓ ↑
┌─────────────────────────────────┐
│   Data Layer                     │  ← In-memory storage
│   - task_repository.py           │
│   - storage management           │
└─────────────────────────────────┘
```

### Module Breakdown

#### `main.py`
- CLI interface and user interaction loop
- Command parsing and routing
- Display formatting and output
- Input validation (format only, not business rules)

#### `task_service.py`
- Business logic for all task operations
- Domain validation rules
- Orchestrates repository calls
- Returns results or raises domain exceptions

#### `task_repository.py`
- In-memory storage management
- CRUD operations on storage dict
- ID generation
- Data retrieval and filtering

#### `models.py`
- Task data structure definition
- Type hints and constants
- Helper functions for task creation

#### `exceptions.py`
- Custom exception classes
- Domain-specific errors (TaskNotFoundError, InvalidTaskDataError)

---

## User Interface Specification

### CLI Commands

```
Available commands:
  add <title>              - Add a new task
  list                     - View all tasks
  view <id>                - View a specific task
  update <id> <new_title>  - Update task title
  delete <id>              - Delete a task
  complete <id>            - Mark task as complete
  incomplete <id>          - Mark task as incomplete
  help                     - Show this help message
  exit                     - Exit the application
```

### Interaction Flow

#### Starting the application
```
$ python main.py

╔════════════════════════════════════╗
║     Todo App - Phase I             ║
║     Type 'help' for commands       ║
╚════════════════════════════════════╝

> _
```

#### Example session
```
> add Buy groceries
✓ Task created: #1 - Buy groceries

> add Finish project report
✓ Task created: #2 - Finish project report

> list
ID | Status | Title                  | Created
---+--------+------------------------+-------------------
1  | [ ]    | Buy groceries          | 2025-12-26 10:30
2  | [ ]    | Finish project report  | 2025-12-26 10:31

Total: 2 tasks (0 complete, 2 incomplete)

> complete 1
✓ Task #1 marked as complete

> list
ID | Status | Title                  | Created
---+--------+------------------------+-------------------
1  | [✓]    | Buy groceries          | 2025-12-26 10:30
2  | [ ]    | Finish project report  | 2025-12-26 10:31

Total: 2 tasks (1 complete, 1 incomplete)

> delete 2
⚠ Are you sure you want to delete task #2 - "Finish project report"? (y/n): y
✓ Task #2 deleted

> exit
Goodbye!
```

### Error Handling Examples

```
> add
✗ Error: Task title cannot be empty

> add [201 character string]
✗ Error: Task title cannot exceed 200 characters

> view 999
✗ Error: Task #999 not found

> complete abc
✗ Error: Invalid task ID format
```

---

## Non-Functional Requirements

### Performance
- **Response Time**: All operations complete in <100ms for up to 1,000 tasks
- **Memory**: Application uses <50MB RAM for 1,000 tasks
- **Startup Time**: Application starts in <1 second

### Usability
- Clear command syntax (no learning curve)
- Helpful error messages (actionable feedback)
- Immediate visual confirmation of actions
- Graceful handling of invalid input

### Maintainability
- **Code Organization**: Maximum 200 lines per file
- **Function Complexity**: Maximum cyclomatic complexity of 5 per function
- **Documentation**: Docstrings for all public functions
- **Type Hints**: Full type annotations on all functions

### Testability
- **Unit Test Coverage**: ≥80% line coverage
- **Test Categories**:
  - Task creation, retrieval, update, deletion
  - Status transitions
  - Edge cases and error conditions
  - Validation rules
- **Test Framework**: pytest
- **Test Organization**: Mirror source structure in `tests/` directory

---

## Testing Strategy

### Test Structure
```
tests/
├── test_task_service.py      # Business logic tests
├── test_task_repository.py   # Storage layer tests
├── test_models.py             # Data model tests
└── test_integration.py        # End-to-end workflow tests
```

### Test Coverage Requirements

#### Business Logic Tests (test_task_service.py)
- ✅ Create task with valid title
- ✅ Reject task with empty title
- ✅ Reject task with title >200 chars
- ✅ Update task with valid new title
- ✅ Reject update with empty title
- ✅ Delete existing task
- ✅ Error on delete non-existent task
- ✅ Mark task as complete
- ✅ Mark task as incomplete
- ✅ Toggle status multiple times
- ✅ Retrieve all tasks (empty, single, multiple)
- ✅ Retrieve task by ID

#### Repository Tests (test_task_repository.py)
- ✅ Generate unique sequential IDs
- ✅ Store and retrieve tasks
- ✅ Update task data
- ✅ Delete task from storage
- ✅ Handle concurrent ID generation

#### Integration Tests (test_integration.py)
- ✅ Complete user workflow: add → view → complete → delete
- ✅ Multiple tasks management
- ✅ Error recovery scenarios

---

## File Structure

```
phase1/
├── CONSTITUTION.md          # This file
├── SPECIFICATION.md         # Detailed spec (generated next)
├── PLAN.md                  # Implementation plan (via /sp.plan)
├── TASKS.md                 # Task breakdown (via /sp.tasks)
├── README.md                # User documentation
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── task_service.py      # Business logic
│   ├── task_repository.py   # Data storage
│   ├── models.py            # Data structures
│   └── exceptions.py        # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── test_task_service.py
│   ├── test_task_repository.py
│   ├── test_models.py
│   └── test_integration.py
├── requirements.txt         # Python dependencies (pytest only)
└── .gitignore              # Ignore __pycache__, .pytest_cache
```

---

## Acceptance Criteria

### Functional Completeness
- [ ] All 6 basic features implemented (F1-F6)
- [ ] All user stories satisfied with acceptance criteria met
- [ ] All edge cases handled with appropriate error messages

### Quality Gates
- [ ] Test coverage ≥80%
- [ ] All tests passing
- [ ] No linting errors (pycodestyle or ruff)
- [ ] Type checking passes (mypy)

### Documentation
- [ ] README.md with setup and usage instructions
- [ ] All functions have docstrings
- [ ] Code comments for non-obvious logic
- [ ] Examples in README demonstrate all features

### User Experience
- [ ] CLI is intuitive and responsive
- [ ] Error messages are clear and actionable
- [ ] Application handles invalid input gracefully
- [ ] Help command shows comprehensive usage

### Evolution Readiness
- [ ] Domain model documented for Phase II migration
- [ ] Business logic separated from presentation
- [ ] Data structures ready for JSON/DB serialization
- [ ] No hardcoded assumptions about storage mechanism

---

## Migration Notes for Phase II

### Data Model Evolution
- Current `Task` dict → SQLModel Task class
- Add fields in Phase II: `priority`, `tags`, `due_date`
- `id` becomes database primary key (auto-increment)
- Timestamps remain ISO 8601 format (SQLModel handles conversion)

### Business Logic Reuse
- `task_service.py` logic can be adapted to async FastAPI handlers
- Validation rules remain identical
- Exception handling patterns carry forward

### Storage Migration
- In-memory dict → PostgreSQL via SQLModel
- Repository pattern directly maps to database operations
- Add export/import functions for data continuity

---

## Dependencies

### Runtime Dependencies
None (Python 3.10+ standard library only)

### Development Dependencies
```
pytest>=7.4.0
pytest-cov>=4.1.0
mypy>=1.5.0
ruff>=0.1.0  # or pycodestyle
```

---

## Success Metrics

### Quantitative
- ✅ 100% of features implemented per spec
- ✅ Test coverage ≥80%
- ✅ 0 critical bugs
- ✅ All operations <100ms for 1,000 tasks

### Qualitative
- ✅ Code is readable and well-organized
- ✅ User can complete workflows without documentation
- ✅ Team can explain domain model clearly
- ✅ Phase II team can understand and extend the code

---

## Risks and Mitigations

### Risk 1: Scope Creep
- **Risk**: Adding features beyond basic requirements
- **Mitigation**: Strict adherence to F1-F6 only; defer enhancements to Phase II

### Risk 2: Over-Engineering
- **Risk**: Building abstractions for future phases
- **Mitigation**: YAGNI principle; build only what Phase I needs

### Risk 3: Insufficient Testing
- **Risk**: Not reaching 80% coverage or missing edge cases
- **Mitigation**: TDD approach; write tests before implementation

---

## Changelog

- **v1.0.0** (2025-12-26): Initial Phase I Constitution
  - Defined functional requirements (F1-F6)
  - Established architecture and data model
  - Set acceptance criteria and success metrics

---

## Approval Checklist

Before proceeding to `/sp.plan`:
- [ ] All functional requirements clearly defined
- [ ] Data model is complete and documented
- [ ] Architecture aligns with Global Constitution principles
- [ ] Acceptance criteria are measurable
- [ ] Testing strategy is comprehensive
- [ ] Migration path to Phase II is clear

---

**Status**: Ready for `/sp.plan`
**Next Command**: `/sp.plan phase1`
