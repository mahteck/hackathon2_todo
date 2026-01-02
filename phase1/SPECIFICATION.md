# Phase I Specification - In-Memory Python Console Todo App

**Project:** Evolution of Todo
**Phase:** I - Console Foundation
**Version:** 1.0.0
**Status:** Approved for Planning
**Parent Documents:**
- [Global Constitution](../CONSTITUTION.md)
- [Phase I Constitution](./CONSTITUTION.md)

---

## Table of Contents
1. [Phase I Constitution](#phase-i-constitution)
2. [System Overview](#system-overview)
3. [Data Model](#data-model)
4. [Phase I Feature Specifications](#phase-i-feature-specifications)
5. [CLI Interface Specification](#cli-interface-specification)
6. [Error Handling](#error-handling)
7. [Acceptance Criteria](#acceptance-criteria)
8. [Testing Requirements](#testing-requirements)

---

## Phase I Constitution

### Design Principles

#### 1. Simplicity Above All
- **Pure Python**: Use only Python 3.10+ standard library (no external runtime dependencies)
- **In-Memory Only**: Store all data in Python data structures (lists, dicts)
- **CLI-First**: Command-line interface is the only user interaction method
- **No Persistence**: Data lives only during application runtime (acceptable for Phase I)

#### 2. Clean Domain Model
- **Task is Sacred**: The Task entity must be well-defined and complete
- **Immutable IDs**: Once a task is created, its ID never changes
- **Temporal Tracking**: All tasks track creation and modification timestamps
- **Status Clarity**: Task completion is a boolean state, not a multi-valued status

#### 3. Separation of Concerns
```
CLI Layer (main.py)
    ↓ Commands
Business Logic Layer (task_service.py)
    ↓ Domain Operations
Data Layer (task_repository.py)
    ↓ CRUD Operations
In-Memory Storage (dict)
```

#### 4. Fail-Fast Validation
- **Validate Early**: Check input at the service layer before storage
- **Clear Errors**: Every error message tells the user exactly what went wrong
- **No Silent Failures**: Every operation returns success or raises an exception

#### 5. Evolution-Ready Code
- **Type Hints**: All functions fully annotated for future refactoring
- **Testable Design**: Business logic independent of I/O
- **Migration Path**: Data structures easily convertible to JSON/database schemas
- **Documented Contracts**: Function signatures and behaviors clearly documented

---

## System Overview

### Purpose
Phase I delivers a foundational console-based Todo application that:
- Validates core domain logic (what is a task? what operations make sense?)
- Provides immediate user value (functional task management)
- Establishes patterns for future phases (service layer, repository pattern)
- Serves as a reference implementation for data model evolution

### Architecture

```
┌──────────────────────────────────────────────────────┐
│                   main.py (CLI)                      │
│  - Parse commands                                    │
│  - Display output                                    │
│  - Handle user input loop                            │
└──────────────────────────────────────────────────────┘
                          ↓ ↑
┌──────────────────────────────────────────────────────┐
│              task_service.py (Business Logic)        │
│  - add_task(title, description)                      │
│  - update_task(id, title, description)               │
│  - delete_task(id)                                   │
│  - complete_task(id)                                 │
│  - uncomplete_task(id)                               │
│  - get_all_tasks()                                   │
│  - get_task_by_id(id)                                │
└──────────────────────────────────────────────────────┘
                          ↓ ↑
┌──────────────────────────────────────────────────────┐
│        task_repository.py (Data Access)              │
│  - create(task_data) -> Task                         │
│  - update(id, task_data) -> Task                     │
│  - delete(id) -> bool                                │
│  - find_by_id(id) -> Task | None                     │
│  - find_all() -> list[Task]                          │
│  - generate_id() -> int                              │
└──────────────────────────────────────────────────────┘
                          ↓ ↑
┌──────────────────────────────────────────────────────┐
│              In-Memory Storage                       │
│  tasks: dict[int, Task] = {}                         │
│  next_id: int = 1                                    │
└──────────────────────────────────────────────────────┘
```

### Technology Stack
- **Language**: Python 3.10+
- **CLI**: Built-in `input()` and `print()`
- **Storage**: Python `dict` and `list`
- **Date/Time**: `datetime` from standard library
- **Testing**: pytest (dev dependency only)

---

## Data Model

### Task Entity

```python
from datetime import datetime
from typing import TypedDict

class Task(TypedDict):
    """
    Represents a single Todo task.

    Attributes:
        id: Unique integer identifier (auto-generated, immutable)
        title: Short task title (required, 1-200 characters)
        description: Optional detailed description (0-1000 characters)
        completed: Boolean flag indicating completion status
        created_at: ISO 8601 timestamp of task creation (immutable)
        updated_at: ISO 8601 timestamp of last modification
    """
    id: int
    title: str
    description: str
    completed: bool
    created_at: str  # ISO 8601 format: "2025-12-26T10:30:00"
    updated_at: str  # ISO 8601 format: "2025-12-26T10:30:00"
```

### Field Specifications

| Field | Type | Required | Constraints | Default | Mutable |
|-------|------|----------|-------------|---------|---------|
| `id` | int | Yes | Positive integer, unique | Auto-generated | No |
| `title` | str | Yes | 1-200 characters, non-empty | - | Yes |
| `description` | str | No | 0-1000 characters | Empty string `""` | Yes |
| `completed` | bool | Yes | `True` or `False` | `False` | Yes |
| `created_at` | str | Yes | ISO 8601 datetime string | Current timestamp | No |
| `updated_at` | str | Yes | ISO 8601 datetime string | Current timestamp | Yes (on update) |

### Validation Rules

#### Title Validation
- **Must not be empty**: `title.strip() != ""`
- **Maximum length**: 200 characters after stripping whitespace
- **Error messages**:
  - Empty: `"Task title cannot be empty"`
  - Too long: `"Task title cannot exceed 200 characters (got {len})"`

#### Description Validation
- **Optional**: Can be empty string
- **Maximum length**: 1000 characters
- **Error message**:
  - Too long: `"Task description cannot exceed 1000 characters (got {len})"`

#### ID Validation
- **Must be positive integer**: `id > 0`
- **Must exist**: When querying, ID must be in storage
- **Error messages**:
  - Invalid format: `"Invalid task ID: must be a positive integer"`
  - Not found: `"Task with ID {id} not found"`

### Storage Structure

```python
# Global in-memory storage
_storage: dict[int, Task] = {}
_next_id: int = 1

# Example populated storage:
_storage = {
    1: {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": False,
        "created_at": "2025-12-26T10:30:00",
        "updated_at": "2025-12-26T10:30:00"
    },
    2: {
        "id": 2,
        "title": "Finish project report",
        "description": "",
        "completed": True,
        "created_at": "2025-12-26T09:15:00",
        "updated_at": "2025-12-26T11:45:00"
    }
}
```

---

## Phase I Feature Specifications

### Feature 1: Add Task

#### Description
Create a new task with a title and optional description. The system auto-generates a unique ID and timestamps.

#### Preconditions
- Application is running
- User has access to the CLI

#### Inputs
- `title` (required): String, 1-200 characters
- `description` (optional): String, 0-1000 characters, defaults to empty string

#### Behavior
1. Validate `title` is not empty and ≤200 characters
2. Validate `description` is ≤1000 characters (if provided)
3. Generate unique integer ID (auto-increment)
4. Generate current timestamp in ISO 8601 format
5. Create Task object with:
   - `id`: Generated ID
   - `title`: Provided title (stripped of leading/trailing whitespace)
   - `description`: Provided description or empty string
   - `completed`: `False`
   - `created_at`: Current timestamp
   - `updated_at`: Current timestamp (same as created_at initially)
6. Store task in in-memory storage
7. Return created task

#### Postconditions
- New task exists in storage with unique ID
- Task is marked as incomplete
- Task has creation and update timestamps

#### Success Response
```
✓ Task created successfully
  ID: 1
  Title: Buy groceries
  Description: Milk, eggs, bread
  Status: Incomplete
  Created: 2025-12-26 10:30:00
```

#### Error Cases
| Condition | Error Message |
|-----------|---------------|
| Empty title | `"Task title cannot be empty"` |
| Title too long (>200 chars) | `"Task title cannot exceed 200 characters"` |
| Description too long (>1000 chars) | `"Task description cannot exceed 1000 characters"` |

#### CLI Usage Examples

```bash
# Add task with title only
> add "Buy groceries"
✓ Task created successfully
  ID: 1
  Title: Buy groceries
  Status: Incomplete

# Add task with title and description
> add "Finish report" "Complete Q4 financial analysis"
✓ Task created successfully
  ID: 2
  Title: Finish report
  Description: Complete Q4 financial analysis
  Status: Incomplete

# Error: empty title
> add ""
✗ Error: Task title cannot be empty

# Error: title too long
> add "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat duis aute irure dolor"
✗ Error: Task title cannot exceed 200 characters
```

---

### Feature 2: View Task List

#### Description
Display all tasks in storage with their key attributes in a formatted table.

#### Preconditions
- Application is running

#### Inputs
None (operates on all stored tasks)

#### Behavior
1. Retrieve all tasks from storage
2. Sort tasks by ID (ascending)
3. Format each task as a table row showing:
   - ID
   - Status icon (`[ ]` for incomplete, `[✓]` for complete)
   - Title (truncated to 50 chars if longer, with `...`)
   - Created timestamp (formatted as `YYYY-MM-DD HH:MM`)
4. Display summary statistics:
   - Total task count
   - Number of completed tasks
   - Number of incomplete tasks

#### Postconditions
- No changes to storage
- User sees current state of all tasks

#### Success Response

**When tasks exist:**
```
ID | Status | Title                                      | Created
---+--------+--------------------------------------------+-------------------
1  | [ ]    | Buy groceries                              | 2025-12-26 10:30
2  | [✓]    | Finish project report                      | 2025-12-26 09:15
3  | [ ]    | Schedule dentist appointment               | 2025-12-26 11:00

Total: 3 tasks (1 completed, 2 incomplete)
```

**When no tasks exist:**
```
No tasks found. Use 'add' to create your first task.
```

#### Error Cases
None (always succeeds, even with empty storage)

#### CLI Usage Examples

```bash
# List all tasks
> list
ID | Status | Title                                      | Created
---+--------+--------------------------------------------+-------------------
1  | [ ]    | Buy groceries                              | 2025-12-26 10:30
2  | [✓]    | Finish project report                      | 2025-12-26 09:15

Total: 2 tasks (1 completed, 1 incomplete)

# List when no tasks exist
> list
No tasks found. Use 'add' to create your first task.

# Long title truncation
> list
ID | Status | Title                                      | Created
---+--------+--------------------------------------------+-------------------
1  | [ ]    | This is a very long task title that will b...| 2025-12-26 10:30
```

---

### Feature 3: View Single Task (Detail View)

#### Description
Display detailed information about a specific task identified by its ID.

#### Preconditions
- Application is running
- Task with specified ID exists

#### Inputs
- `id` (required): Positive integer representing task ID

#### Behavior
1. Validate `id` is a positive integer
2. Retrieve task from storage by ID
3. If task not found, raise error
4. Display all task fields:
   - ID
   - Title (full text, not truncated)
   - Description (full text, "None" if empty)
   - Status (Completed / Incomplete)
   - Created timestamp
   - Updated timestamp

#### Postconditions
- No changes to storage
- User sees all details of specified task

#### Success Response
```
Task Details
────────────────────────────────────────
ID:          1
Title:       Buy groceries
Description: Milk, eggs, bread, chicken
Status:      Incomplete
Created:     2025-12-26 10:30:00
Updated:     2025-12-26 10:30:00
```

#### Error Cases
| Condition | Error Message |
|-----------|---------------|
| Non-numeric ID | `"Invalid task ID: must be a positive integer"` |
| Negative or zero ID | `"Invalid task ID: must be a positive integer"` |
| Task not found | `"Task with ID {id} not found"` |

#### CLI Usage Examples

```bash
# View existing task
> view 1
Task Details
────────────────────────────────────────
ID:          1
Title:       Buy groceries
Description: Milk, eggs, bread
Status:      Incomplete
Created:     2025-12-26 10:30:00
Updated:     2025-12-26 10:30:00

# View task without description
> view 2
Task Details
────────────────────────────────────────
ID:          2
Title:       Quick task
Description: None
Status:      Completed
Created:     2025-12-26 09:00:00
Updated:     2025-12-26 09:15:00

# Error: task not found
> view 999
✗ Error: Task with ID 999 not found

# Error: invalid ID
> view abc
✗ Error: Invalid task ID: must be a positive integer
```

---

### Feature 4: Update Task

#### Description
Modify the title and/or description of an existing task. Updates the `updated_at` timestamp.

#### Preconditions
- Application is running
- Task with specified ID exists

#### Inputs
- `id` (required): Positive integer representing task ID
- `title` (optional): New title string, 1-200 characters
- `description` (optional): New description string, 0-1000 characters

**Note**: At least one of `title` or `description` must be provided.

#### Behavior
1. Validate `id` is positive integer and exists in storage
2. Validate provided fields:
   - If `title` provided: must be non-empty and ≤200 chars
   - If `description` provided: must be ≤1000 chars
3. Retrieve existing task from storage
4. Update only the provided fields (keep others unchanged)
5. Update `updated_at` timestamp to current time
6. Store modified task back in storage
7. Return updated task

#### Postconditions
- Task exists with updated field(s)
- `updated_at` timestamp is current
- `created_at` timestamp remains unchanged
- `id` remains unchanged
- `completed` status remains unchanged

#### Success Response
```
✓ Task updated successfully
  ID: 1
  Title: Buy groceries and household items
  Description: Milk, eggs, bread, cleaning supplies
  Status: Incomplete
  Updated: 2025-12-26 11:45:00
```

#### Error Cases
| Condition | Error Message |
|-----------|---------------|
| Task not found | `"Task with ID {id} not found"` |
| Invalid ID format | `"Invalid task ID: must be a positive integer"` |
| Empty title (when updating title) | `"Task title cannot be empty"` |
| Title too long | `"Task title cannot exceed 200 characters"` |
| Description too long | `"Task description cannot exceed 1000 characters"` |
| No fields provided | `"Must provide at least one field to update (title or description)"` |

#### CLI Usage Examples

```bash
# Update title only
> update 1 --title "Buy groceries and household items"
✓ Task updated successfully
  ID: 1
  Title: Buy groceries and household items

# Update description only
> update 1 --description "Milk, eggs, bread, cleaning supplies"
✓ Task updated successfully
  ID: 1
  Description: Milk, eggs, bread, cleaning supplies

# Update both title and description
> update 1 --title "Shopping list" --description "Weekly grocery shopping"
✓ Task updated successfully
  ID: 1
  Title: Shopping list
  Description: Weekly grocery shopping

# Error: task not found
> update 999 --title "New title"
✗ Error: Task with ID 999 not found

# Error: empty title
> update 1 --title ""
✗ Error: Task title cannot be empty

# Error: no fields provided
> update 1
✗ Error: Must provide at least one field to update (title or description)
```

---

### Feature 5: Delete Task

#### Description
Permanently remove a task from storage by its ID.

#### Preconditions
- Application is running
- Task with specified ID exists

#### Inputs
- `id` (required): Positive integer representing task ID

#### Behavior
1. Validate `id` is positive integer
2. Check if task exists in storage
3. If task not found, raise error
4. Remove task from storage
5. Return success confirmation

**Note**: Deletion is permanent and immediate (no confirmation prompt in this phase).

#### Postconditions
- Task no longer exists in storage
- Task ID is not reused for future tasks
- Other tasks remain unaffected

#### Success Response
```
✓ Task deleted successfully
  Deleted task #1: "Buy groceries"
```

#### Error Cases
| Condition | Error Message |
|-----------|---------------|
| Task not found | `"Task with ID {id} not found"` |
| Invalid ID format | `"Invalid task ID: must be a positive integer"` |

#### CLI Usage Examples

```bash
# Delete existing task
> delete 1
✓ Task deleted successfully
  Deleted task #1: "Buy groceries"

# Error: task not found
> delete 999
✗ Error: Task with ID 999 not found

# Error: invalid ID
> delete abc
✗ Error: Invalid task ID: must be a positive integer

# Verify deletion
> list
ID | Status | Title                                      | Created
---+--------+--------------------------------------------+-------------------
2  | [✓]    | Finish project report                      | 2025-12-26 09:15

Total: 1 task (1 completed, 0 incomplete)
```

---

### Feature 6: Mark Task as Complete

#### Description
Set a task's `completed` status to `True` and update the `updated_at` timestamp.

#### Preconditions
- Application is running
- Task with specified ID exists

#### Inputs
- `id` (required): Positive integer representing task ID

#### Behavior
1. Validate `id` is positive integer
2. Retrieve task from storage
3. If task not found, raise error
4. Set `completed` field to `True`
5. Update `updated_at` timestamp to current time
6. Store modified task back in storage
7. Return success confirmation

**Note**: Marking an already-completed task as complete is idempotent (no error, operation succeeds).

#### Postconditions
- Task `completed` field is `True`
- `updated_at` timestamp is current
- All other fields remain unchanged

#### Success Response
```
✓ Task marked as complete
  Task #1: "Buy groceries" ✓
```

#### Error Cases
| Condition | Error Message |
|-----------|---------------|
| Task not found | `"Task with ID {id} not found"` |
| Invalid ID format | `"Invalid task ID: must be a positive integer"` |

#### CLI Usage Examples

```bash
# Mark incomplete task as complete
> complete 1
✓ Task marked as complete
  Task #1: "Buy groceries" ✓

# Verify status change
> list
ID | Status | Title                                      | Created
---+--------+--------------------------------------------+-------------------
1  | [✓]    | Buy groceries                              | 2025-12-26 10:30
2  | [ ]    | Finish project report                      | 2025-12-26 09:15

# Mark already-complete task (idempotent)
> complete 1
✓ Task marked as complete
  Task #1: "Buy groceries" ✓

# Error: task not found
> complete 999
✗ Error: Task with ID 999 not found
```

---

### Feature 7: Mark Task as Incomplete

#### Description
Set a task's `completed` status to `False` and update the `updated_at` timestamp.

#### Preconditions
- Application is running
- Task with specified ID exists

#### Inputs
- `id` (required): Positive integer representing task ID

#### Behavior
1. Validate `id` is positive integer
2. Retrieve task from storage
3. If task not found, raise error
4. Set `completed` field to `False`
5. Update `updated_at` timestamp to current time
6. Store modified task back in storage
7. Return success confirmation

**Note**: Marking an already-incomplete task as incomplete is idempotent (no error, operation succeeds).

#### Postconditions
- Task `completed` field is `False`
- `updated_at` timestamp is current
- All other fields remain unchanged

#### Success Response
```
✓ Task marked as incomplete
  Task #1: "Buy groceries" [ ]
```

#### Error Cases
| Condition | Error Message |
|-----------|---------------|
| Task not found | `"Task with ID {id} not found"` |
| Invalid ID format | `"Invalid task ID: must be a positive integer"` |

#### CLI Usage Examples

```bash
# Mark complete task as incomplete
> uncomplete 1
✓ Task marked as incomplete
  Task #1: "Buy groceries" [ ]

# Verify status change
> list
ID | Status | Title                                      | Created
---+--------+--------------------------------------------+-------------------
1  | [ ]    | Buy groceries                              | 2025-12-26 10:30
2  | [✓]    | Finish project report                      | 2025-12-26 09:15

# Mark already-incomplete task (idempotent)
> uncomplete 1
✓ Task marked as incomplete
  Task #1: "Buy groceries" [ ]

# Error: task not found
> uncomplete 999
✗ Error: Task with ID 999 not found
```

---

## CLI Interface Specification

### Command Syntax

```
Available Commands:
  add <title> [description]          Add a new task
  list                               View all tasks
  view <id>                          View task details
  update <id> [--title <title>] [--description <desc>]
                                     Update task title/description
  delete <id>                        Delete a task
  complete <id>                      Mark task as complete
  uncomplete <id>                    Mark task as incomplete
  help                               Show this help message
  exit                               Exit the application
```

### Command Parsing Rules

1. **Case Insensitive**: Commands are case-insensitive (`add` = `ADD` = `Add`)
2. **Whitespace Tolerant**: Leading/trailing whitespace is ignored
3. **Quote Handling**: Strings with spaces must be in quotes
   - `add "Buy groceries"`
   - `add "Buy groceries" "Milk and eggs"`
4. **Flag Syntax**: Update uses `--flag value` syntax
   - `update 1 --title "New title"`
   - `update 1 --description "New description"`
   - `update 1 --title "Title" --description "Description"`

### Application Lifecycle

#### Startup
```
╔════════════════════════════════════════════════╗
║      Todo App - Phase I (Console)             ║
║      Evolution of Todo Project                ║
╚════════════════════════════════════════════════╝

Type 'help' for available commands.

> _
```

#### Interactive Loop
1. Display prompt: `> `
2. Read user input
3. Parse command and arguments
4. Execute command (call appropriate service function)
5. Display result or error
6. Repeat until `exit` command

#### Shutdown
```
> exit
Goodbye! Your tasks are not saved (in-memory only).
```

### Help Command Output

```
> help

Todo App - Available Commands
═══════════════════════════════════════════════════════════════

Task Management:
  add <title> [description]
      Create a new task with optional description
      Example: add "Buy groceries" "Milk, eggs, bread"

  list
      Display all tasks in a formatted table
      Example: list

  view <id>
      Show detailed information for a specific task
      Example: view 1

  update <id> [--title <title>] [--description <desc>]
      Update task title and/or description
      Example: update 1 --title "New title"
      Example: update 1 --description "New description"
      Example: update 1 --title "Title" --description "Desc"

  delete <id>
      Permanently delete a task
      Example: delete 1

  complete <id>
      Mark a task as completed
      Example: complete 1

  uncomplete <id>
      Mark a task as incomplete
      Example: uncomplete 1

General:
  help
      Show this help message

  exit
      Exit the application (all data will be lost)

═══════════════════════════════════════════════════════════════
```

---

## Error Handling

### Error Message Format

```
✗ Error: [Clear description of what went wrong]
```

### Error Categories

#### 1. Validation Errors
- **Empty title**: `"Task title cannot be empty"`
- **Title too long**: `"Task title cannot exceed 200 characters"`
- **Description too long**: `"Task description cannot exceed 1000 characters"`

#### 2. Not Found Errors
- **Task not found**: `"Task with ID {id} not found"`

#### 3. Input Format Errors
- **Invalid ID**: `"Invalid task ID: must be a positive integer"`
- **Unknown command**: `"Unknown command '{command}'. Type 'help' for available commands."`
- **Missing required argument**: `"Missing required argument: {argument}"`
- **Invalid flag**: `"Invalid flag '{flag}'. Use --title or --description"`

#### 4. System Errors
- **Unexpected error**: `"An unexpected error occurred: {error_message}"`

### Error Handling Strategy

1. **Catch at Service Layer**: All business logic errors caught in `task_service.py`
2. **Custom Exceptions**: Define domain-specific exceptions in `exceptions.py`
3. **Display in CLI**: `main.py` catches exceptions and displays formatted error messages
4. **No Stack Traces to User**: Internal errors logged, user sees friendly message
5. **Recover Gracefully**: After error, return to command prompt (don't exit)

### Exception Classes

```python
# exceptions.py

class TodoAppError(Exception):
    """Base exception for all Todo app errors."""
    pass

class ValidationError(TodoAppError):
    """Raised when input validation fails."""
    pass

class TaskNotFoundError(TodoAppError):
    """Raised when a task ID doesn't exist."""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")

class InvalidTaskIdError(TodoAppError):
    """Raised when task ID format is invalid."""
    def __init__(self, value: str):
        self.value = value
        super().__init__(f"Invalid task ID: must be a positive integer")
```

---

## Acceptance Criteria

### Functional Requirements

#### FR1: Add Task
- [ ] Can create task with title only
- [ ] Can create task with title and description
- [ ] Task receives unique auto-incremented ID
- [ ] Task has creation timestamp in ISO 8601 format
- [ ] Task defaults to incomplete status
- [ ] Rejects empty title with clear error message
- [ ] Rejects title >200 characters with clear error message
- [ ] Rejects description >1000 characters with clear error message
- [ ] Strips leading/trailing whitespace from title

#### FR2: View Task List
- [ ] Displays all tasks in ID-ascending order
- [ ] Shows ID, status icon, title, and creation time for each task
- [ ] Truncates titles >50 chars with ellipsis (...)
- [ ] Displays summary: total, completed, incomplete counts
- [ ] Shows helpful message when no tasks exist
- [ ] Table formatting is aligned and readable

#### FR3: View Single Task
- [ ] Displays all task fields (ID, title, description, status, timestamps)
- [ ] Shows full title and description (no truncation)
- [ ] Shows "None" for empty description
- [ ] Returns error for non-existent task ID
- [ ] Returns error for invalid ID format (non-numeric, negative)

#### FR4: Update Task
- [ ] Can update title only
- [ ] Can update description only
- [ ] Can update both title and description
- [ ] Updates `updated_at` timestamp
- [ ] Preserves `created_at` timestamp
- [ ] Preserves `id` and `completed` status
- [ ] Returns error if task not found
- [ ] Validates new title (non-empty, ≤200 chars)
- [ ] Validates new description (≤1000 chars)
- [ ] Returns error if no fields provided

#### FR5: Delete Task
- [ ] Removes task from storage permanently
- [ ] Returns success message with deleted task details
- [ ] Returns error if task not found
- [ ] Returns error for invalid ID format
- [ ] Does not affect other tasks
- [ ] Does not reuse deleted task IDs

#### FR6: Mark Complete
- [ ] Sets task `completed` to `True`
- [ ] Updates `updated_at` timestamp
- [ ] Returns success message
- [ ] Returns error if task not found
- [ ] Is idempotent (can mark completed task as complete)

#### FR7: Mark Incomplete
- [ ] Sets task `completed` to `False`
- [ ] Updates `updated_at` timestamp
- [ ] Returns success message
- [ ] Returns error if task not found
- [ ] Is idempotent (can mark incomplete task as incomplete)

### Non-Functional Requirements

#### NFR1: Usability
- [ ] CLI commands are intuitive and consistent
- [ ] Error messages are clear and actionable
- [ ] Help command shows all available commands with examples
- [ ] Application starts with welcome message
- [ ] Exit command shows goodbye message

#### NFR2: Performance
- [ ] All operations complete in <100ms for ≤1000 tasks
- [ ] Application uses <50MB memory with 1000 tasks
- [ ] Application starts in <1 second

#### NFR3: Code Quality
- [ ] All functions have type hints
- [ ] All public functions have docstrings
- [ ] Code follows PEP 8 style guide
- [ ] No function exceeds 50 lines
- [ ] Cyclomatic complexity ≤5 per function

#### NFR4: Testing
- [ ] Unit test coverage ≥80%
- [ ] All features have passing tests
- [ ] All error cases have tests
- [ ] Integration tests cover complete workflows
- [ ] Tests run successfully with `pytest`

#### NFR5: Documentation
- [ ] README.md with setup and usage instructions
- [ ] README includes examples of all commands
- [ ] Code has inline comments for complex logic
- [ ] All custom exceptions documented

---

## Testing Requirements

### Test Coverage Breakdown

```
tests/
├── test_task_repository.py      # Data layer tests (25% coverage target)
├── test_task_service.py          # Business logic tests (40% coverage target)
├── test_models.py                # Data model tests (10% coverage target)
├── test_integration.py           # End-to-end tests (15% coverage target)
└── conftest.py                   # Shared fixtures
```

### Test Cases by Feature

#### test_task_repository.py
- [ ] `test_generate_unique_ids()` - IDs are sequential and unique
- [ ] `test_create_task()` - Task stored in dict with correct ID
- [ ] `test_find_by_id_existing()` - Returns correct task
- [ ] `test_find_by_id_not_found()` - Returns None for missing ID
- [ ] `test_find_all_empty()` - Returns empty list when no tasks
- [ ] `test_find_all_multiple()` - Returns all tasks
- [ ] `test_update_task()` - Updates task in storage
- [ ] `test_delete_task()` - Removes task from storage
- [ ] `test_delete_nonexistent()` - Returns False for missing task

#### test_task_service.py
- [ ] `test_add_task_valid()` - Creates task with title and description
- [ ] `test_add_task_title_only()` - Creates task with title, empty description
- [ ] `test_add_task_empty_title()` - Raises ValidationError
- [ ] `test_add_task_title_too_long()` - Raises ValidationError
- [ ] `test_add_task_description_too_long()` - Raises ValidationError
- [ ] `test_get_all_tasks_empty()` - Returns empty list
- [ ] `test_get_all_tasks_multiple()` - Returns all tasks sorted by ID
- [ ] `test_get_task_by_id_found()` - Returns correct task
- [ ] `test_get_task_by_id_not_found()` - Raises TaskNotFoundError
- [ ] `test_update_task_title()` - Updates title, preserves other fields
- [ ] `test_update_task_description()` - Updates description only
- [ ] `test_update_task_both()` - Updates both fields
- [ ] `test_update_task_not_found()` - Raises TaskNotFoundError
- [ ] `test_update_task_invalid_title()` - Raises ValidationError
- [ ] `test_delete_task_existing()` - Deletes successfully
- [ ] `test_delete_task_not_found()` - Raises TaskNotFoundError
- [ ] `test_complete_task()` - Sets completed=True
- [ ] `test_complete_task_already_complete()` - Idempotent
- [ ] `test_uncomplete_task()` - Sets completed=False
- [ ] `test_uncomplete_task_already_incomplete()` - Idempotent
- [ ] `test_timestamps_on_create()` - created_at and updated_at set
- [ ] `test_timestamps_on_update()` - updated_at changes, created_at doesn't

#### test_models.py
- [ ] `test_task_structure()` - Task has all required fields
- [ ] `test_task_defaults()` - Completed defaults to False
- [ ] `test_iso_timestamp_format()` - Timestamps in correct format

#### test_integration.py
- [ ] `test_complete_workflow()` - Add → View → Update → Complete → Delete
- [ ] `test_multiple_tasks()` - Create and manage 10 tasks
- [ ] `test_error_recovery()` - Application continues after errors
- [ ] `test_task_independence()` - Modifying one task doesn't affect others

### Test Fixtures (conftest.py)

```python
import pytest
from task_repository import TaskRepository

@pytest.fixture
def empty_repository():
    """Provides a fresh, empty repository for each test."""
    repo = TaskRepository()
    repo.clear()  # Ensure clean state
    return repo

@pytest.fixture
def repository_with_tasks(empty_repository):
    """Provides a repository with 3 sample tasks."""
    repo = empty_repository
    repo.create({
        "title": "Task 1",
        "description": "Description 1",
        "completed": False
    })
    repo.create({
        "title": "Task 2",
        "description": "",
        "completed": True
    })
    repo.create({
        "title": "Task 3",
        "description": "Description 3",
        "completed": False
    })
    return repo
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_task_service.py

# Run specific test
pytest tests/test_task_service.py::test_add_task_valid
```

### Coverage Target
- **Minimum**: 80% line coverage
- **Ideal**: 90%+ line coverage
- **Critical Paths**: 100% coverage (add, update, delete, complete)

---

## Implementation Notes

### Module Structure

```python
# src/models.py
"""
Data models and type definitions.
"""
from typing import TypedDict

class Task(TypedDict):
    id: int
    title: str
    description: str
    completed: bool
    created_at: str
    updated_at: str


# src/exceptions.py
"""
Custom exceptions for the Todo application.
"""
class TodoAppError(Exception):
    """Base exception."""
    pass

class ValidationError(TodoAppError):
    """Input validation failed."""
    pass

class TaskNotFoundError(TodoAppError):
    """Task ID not found."""
    pass


# src/task_repository.py
"""
Data access layer for task storage.
"""
from typing import Optional
from models import Task

class TaskRepository:
    def __init__(self):
        self._storage: dict[int, Task] = {}
        self._next_id: int = 1

    def create(self, task_data: dict) -> Task:
        """Create and store a new task."""
        pass

    def find_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve task by ID."""
        pass

    def find_all(self) -> list[Task]:
        """Retrieve all tasks."""
        pass

    def update(self, task_id: int, task_data: dict) -> Task:
        """Update existing task."""
        pass

    def delete(self, task_id: int) -> bool:
        """Delete task by ID."""
        pass


# src/task_service.py
"""
Business logic layer for task operations.
"""
from datetime import datetime
from models import Task
from task_repository import TaskRepository
from exceptions import ValidationError, TaskNotFoundError

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task."""
        pass

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks."""
        pass

    def get_task_by_id(self, task_id: int) -> Task:
        """Get task by ID."""
        pass

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> Task:
        """Update task fields."""
        pass

    def delete_task(self, task_id: int) -> None:
        """Delete task."""
        pass

    def complete_task(self, task_id: int) -> Task:
        """Mark task as complete."""
        pass

    def uncomplete_task(self, task_id: int) -> Task:
        """Mark task as incomplete."""
        pass


# src/main.py
"""
CLI interface and application entry point.
"""
from task_service import TaskService
from task_repository import TaskRepository

def main():
    """Main application loop."""
    repository = TaskRepository()
    service = TaskService(repository)

    print_welcome()

    while True:
        command = input("> ").strip()

        if command.lower() == "exit":
            print_goodbye()
            break

        try:
            execute_command(command, service)
        except Exception as e:
            print_error(str(e))

if __name__ == "__main__":
    main()
```

---

## Migration Path to Phase II

### Data Export Function
To facilitate migration to Phase II (web app with database), implement:

```python
def export_tasks_to_json(filepath: str) -> None:
    """
    Export all tasks to JSON file for migration to Phase II.

    Args:
        filepath: Path to output JSON file
    """
    import json
    tasks = service.get_all_tasks()
    with open(filepath, 'w') as f:
        json.dump(tasks, f, indent=2)
```

### Field Mapping for Phase II
Phase I → Phase II field mapping:
- `id` → `id` (database primary key)
- `title` → `title` (VARCHAR(200))
- `description` → `description` (TEXT)
- `completed` → `completed` (BOOLEAN)
- `created_at` → `created_at` (TIMESTAMP)
- `updated_at` → `updated_at` (TIMESTAMP)

New fields in Phase II:
- `priority` (HIGH/MEDIUM/LOW) - default to MEDIUM
- `tags` (many-to-many) - default to empty array
- `due_date` (TIMESTAMP nullable) - default to NULL

---

## Specification Approval

### Approval Checklist
- [x] All features clearly specified with acceptance criteria
- [x] Data model complete and documented
- [x] CLI interface fully defined with examples
- [x] Error handling comprehensive
- [x] Testing strategy detailed
- [x] Implementation notes provided
- [x] Migration path to Phase II documented

### Status
**✅ APPROVED FOR PLANNING**

### Next Steps
1. Run `/sp.plan phase1` to generate implementation plan
2. Review plan milestones and dependencies
3. Run `/sp.tasks phase1` to create task breakdown
4. Execute implementation via `/sp.implement`

---

**Document Version:** 1.0.0
**Last Updated:** 2025-12-26
**Status:** Ready for Implementation Planning
