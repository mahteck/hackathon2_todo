# Phase I Task List - In-Memory Python Console Todo App

**Project:** Evolution of Todo
**Phase:** I - Console Foundation
**Task List Version:** 1.0.0
**Status:** Ready for Execution
**Parent Documents:**
- [Global Constitution](../CONSTITUTION.md)
- [Phase I Constitution](./CONSTITUTION.md)
- [Phase I Specification](./SPECIFICATION.md)
- [Phase I Plan](./PLAN.md)

---

## Task Execution Instructions

### For Claude Code:
1. Execute tasks **in order** (dependencies are sequential)
2. Read the referenced spec section before implementing
3. Generate code with **full type hints** and **docstrings**
4. Run validation commands after each task
5. If validation fails → **STOP**, refine spec if needed, regenerate code
6. Mark task as ✅ complete only when all success criteria met

### For Human Reviewer:
- Review generated code against spec
- Run validation commands to verify
- Approve before proceeding to next task
- Request spec refinement if behavior doesn't match intent

---

## Task Status Legend
- ⬜ Not Started
- 🔄 In Progress
- ✅ Complete
- ❌ Blocked/Failed
- 🔁 Needs Regeneration

---

## Milestone 1: Foundation Setup

### Task 1.1: Create Project Directory Structure
**Status:** ⬜

**Description:**
Set up the basic Python project directory structure with proper organization for source code, tests, and configuration files.

**Files to Create:**
- `phase1/src/__init__.py`
- `phase1/tests/__init__.py`
- `phase1/.gitignore`
- `phase1/requirements.txt`
- `phase1/README.md` (stub only)

**Spec Reference:**
- [PLAN.md § Step 1: Project Structure Setup](./PLAN.md#step-1-project-structure-setup)
- [SPECIFICATION.md § File Structure](./SPECIFICATION.md#file-structure)

**Implementation Details:**

1. **Create `src/__init__.py`:**
   - Empty file (marks directory as Python package)

2. **Create `tests/__init__.py`:**
   - Empty file (marks directory as Python package)

3. **Create `.gitignore`:**
   ```gitignore
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python

   # Virtual environments
   venv/
   env/
   ENV/

   # Testing
   .pytest_cache/
   .coverage
   htmlcov/
   .tox/

   # Type checking
   .mypy_cache/
   .dmypy.json
   dmypy.json

   # Linting
   .ruff_cache/

   # IDEs
   .vscode/
   .idea/
   *.swp
   *.swo
   .DS_Store
   ```

4. **Create `requirements.txt`:**
   ```
   # Development dependencies only (no runtime dependencies)
   pytest>=7.4.0
   pytest-cov>=4.1.0
   mypy>=1.5.0
   ruff>=0.1.0
   ```

5. **Create `README.md` stub:**
   ```markdown
   # Todo App - Phase I (Console)

   In-memory Python console Todo application.

   ## Status
   🚧 Under Development

   ## Documentation
   Coming soon...
   ```

**Success Criteria:**
- [ ] All directories exist: `phase1/src/`, `phase1/tests/`
- [ ] All `__init__.py` files are present and valid
- [ ] `.gitignore` contains Python-specific ignores
- [ ] `requirements.txt` has 4 dev dependencies
- [ ] `README.md` stub exists

**Validation Commands:**
```bash
cd phase1
ls -la src/ tests/
cat requirements.txt
python -m pip install -r requirements.txt --dry-run
```

**Estimated Effort:** 5 minutes

---

### Task 1.2: Implement Task Data Model
**Status:** ⬜

**Description:**
Create the core `Task` data model using TypedDict with all required fields and constants for validation.

**Files to Create:**
- `phase1/src/models.py`

**Spec Reference:**
- [SPECIFICATION.md § Data Model](./SPECIFICATION.md#data-model)
- [PLAN.md § Step 2.1: Create src/models.py](./PLAN.md#step-2-domain-model--data-layer)

**Implementation Details:**

Create `src/models.py` with:

1. **Imports:**
   ```python
   from typing import TypedDict
   ```

2. **Constants:**
   ```python
   MAX_TITLE_LENGTH = 200
   MAX_DESCRIPTION_LENGTH = 1000
   ```

3. **Task TypedDict:**
   ```python
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
       created_at: str
       updated_at: str
   ```

4. **Module docstring:**
   ```python
   """
   Data models and type definitions for the Todo application.

   This module defines the core Task entity and validation constants.
   """
   ```

**Success Criteria:**
- [ ] `Task` TypedDict has all 6 required fields with correct types
- [ ] `MAX_TITLE_LENGTH` constant is 200
- [ ] `MAX_DESCRIPTION_LENGTH` constant is 1000
- [ ] Module has comprehensive docstring
- [ ] Task class has comprehensive docstring
- [ ] File passes type checking: `mypy src/models.py`
- [ ] File passes linting: `ruff check src/models.py`
- [ ] Can import Task: `python -c "from src.models import Task; print('OK')"`

**Validation Commands:**
```bash
cd phase1
mypy src/models.py
ruff check src/models.py
python -c "from src.models import Task, MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH; print(f'Task model: OK, Max title: {MAX_TITLE_LENGTH}, Max desc: {MAX_DESCRIPTION_LENGTH}')"
```

**Estimated Effort:** 10 minutes

---

### Task 1.3: Implement Custom Exceptions
**Status:** ⬜

**Description:**
Create custom exception classes for domain-specific errors with clear inheritance and error messages.

**Files to Create:**
- `phase1/src/exceptions.py`

**Spec Reference:**
- [SPECIFICATION.md § Error Handling § Exception Classes](./SPECIFICATION.md#error-handling)
- [PLAN.md § Step 2.2: Create src/exceptions.py](./PLAN.md#step-2-domain-model--data-layer)

**Implementation Details:**

Create `src/exceptions.py` with:

1. **Module docstring:**
   ```python
   """
   Custom exceptions for the Todo application.

   Defines domain-specific exception hierarchy for better error handling
   and user-friendly error messages.
   """
   ```

2. **Base exception:**
   ```python
   class TodoAppError(Exception):
       """Base exception for all Todo app errors."""
       pass
   ```

3. **Validation error:**
   ```python
   class ValidationError(TodoAppError):
       """
       Raised when input validation fails.

       Examples: empty title, title too long, description too long.
       """
       pass
   ```

4. **Task not found error:**
   ```python
   class TaskNotFoundError(TodoAppError):
       """
       Raised when a task ID doesn't exist in storage.

       Attributes:
           task_id: The ID that was not found
       """

       def __init__(self, task_id: int):
           self.task_id = task_id
           super().__init__(f"Task with ID {task_id} not found")
   ```

5. **Invalid task ID error:**
   ```python
   class InvalidTaskIdError(TodoAppError):
       """
       Raised when task ID format is invalid.

       Examples: non-numeric ID, negative ID, zero ID.

       Attributes:
           value: The invalid value provided
       """

       def __init__(self, value: str):
           self.value = value
           super().__init__("Invalid task ID: must be a positive integer")
   ```

**Success Criteria:**
- [ ] All 4 exception classes defined (TodoAppError, ValidationError, TaskNotFoundError, InvalidTaskIdError)
- [ ] Inheritance chain correct: ValidationError → TodoAppError → Exception
- [ ] TaskNotFoundError has `task_id` attribute and formatted message
- [ ] InvalidTaskIdError has `value` attribute and clear message
- [ ] All classes have docstrings
- [ ] File passes type checking: `mypy src/exceptions.py`
- [ ] File passes linting: `ruff check src/exceptions.py`
- [ ] Can raise and catch exceptions: test import works

**Validation Commands:**
```bash
cd phase1
mypy src/exceptions.py
ruff check src/exceptions.py
python -c "from src.exceptions import TodoAppError, ValidationError, TaskNotFoundError, InvalidTaskIdError; e = TaskNotFoundError(42); print(f'Exception test: {e}')"
```

**Estimated Effort:** 15 minutes

---

### Task 1.4: Implement Task Repository (Data Layer)
**Status:** ⬜

**Description:**
Create the in-memory data storage layer with CRUD operations for tasks. This is the only module that directly interacts with the storage dictionary.

**Files to Create:**
- `phase1/src/task_repository.py`

**Spec Reference:**
- [SPECIFICATION.md § Data Model § Storage Structure](./SPECIFICATION.md#data-model)
- [PLAN.md § Step 2.3: Create src/task_repository.py](./PLAN.md#step-2-domain-model--data-layer)

**Implementation Details:**

Create `src/task_repository.py` with:

1. **Module docstring and imports:**
   ```python
   """
   Data access layer for task storage.

   Manages in-memory storage of tasks using a dictionary.
   Provides CRUD operations without business logic.
   """
   from typing import Optional
   from src.models import Task
   ```

2. **TaskRepository class:**
   ```python
   class TaskRepository:
       """
       Manages in-memory storage and retrieval of tasks.

       Storage is a dictionary mapping task IDs to Task objects.
       IDs are auto-incremented starting from 1.
       """

       def __init__(self) -> None:
           """Initialize empty storage and ID counter."""
           self._storage: dict[int, Task] = {}
           self._next_id: int = 1

       def generate_id(self) -> int:
           """
           Generate unique sequential task ID.

           Returns:
               Next available task ID (auto-incremented)
           """
           current_id = self._next_id
           self._next_id += 1
           return current_id

       def create(self, task: Task) -> Task:
           """
           Store a new task in memory.

           Args:
               task: Task object to store (must have 'id' field)

           Returns:
               The stored task
           """
           self._storage[task["id"]] = task
           return task

       def find_by_id(self, task_id: int) -> Optional[Task]:
           """
           Retrieve task by ID.

           Args:
               task_id: ID of task to retrieve

           Returns:
               Task if found, None otherwise
           """
           return self._storage.get(task_id)

       def find_all(self) -> list[Task]:
           """
           Retrieve all tasks sorted by ID.

           Returns:
               List of all tasks, sorted by ID ascending
           """
           return [self._storage[task_id] for task_id in sorted(self._storage.keys())]

       def update(self, task_id: int, task: Task) -> Task:
           """
           Update existing task in storage.

           Args:
               task_id: ID of task to update
               task: Updated task object

           Returns:
               Updated task
           """
           self._storage[task_id] = task
           return task

       def delete(self, task_id: int) -> bool:
           """
           Delete task from storage.

           Args:
               task_id: ID of task to delete

           Returns:
               True if task existed and was deleted, False otherwise
           """
           if task_id in self._storage:
               del self._storage[task_id]
               return True
           return False

       def clear(self) -> None:
           """
           Clear all tasks from storage.

           Useful for testing. Resets ID counter to 1.
           """
           self._storage.clear()
           self._next_id = 1
   ```

**Success Criteria:**
- [ ] TaskRepository class with 8 methods implemented
- [ ] `_storage` is `dict[int, Task]` initialized empty
- [ ] `_next_id` starts at 1
- [ ] `generate_id()` returns sequential IDs (1, 2, 3...)
- [ ] `find_all()` returns empty list when storage empty
- [ ] `find_all()` returns tasks sorted by ID
- [ ] `delete()` returns False for non-existent ID
- [ ] All methods have type hints and docstrings
- [ ] File passes type checking: `mypy src/task_repository.py`
- [ ] File passes linting: `ruff check src/task_repository.py`

**Validation Commands:**
```bash
cd phase1
mypy src/task_repository.py
ruff check src/task_repository.py
python -c "
from src.task_repository import TaskRepository
repo = TaskRepository()
print(f'ID 1: {repo.generate_id()}')
print(f'ID 2: {repo.generate_id()}')
print(f'All tasks: {repo.find_all()}')
print('Repository: OK')
"
```

**Estimated Effort:** 30 minutes

---

## Milestone 2: Business Logic Implementation

### Task 2.1: Implement Task Service - Core Structure
**Status:** ⬜

**Description:**
Create the service layer skeleton with initialization and helper methods for validation and timestamp generation.

**Files to Create:**
- `phase1/src/task_service.py`

**Spec Reference:**
- [SPECIFICATION.md § Validation Rules](./SPECIFICATION.md#data-model)
- [PLAN.md § Step 3.1: Create src/task_service.py](./PLAN.md#step-3-business-logic-layer)

**Implementation Details:**

Create `src/task_service.py` with:

1. **Module docstring and imports:**
   ```python
   """
   Business logic layer for task operations.

   Contains all domain validation, business rules, and orchestration
   of repository calls. No direct storage access.
   """
   from datetime import datetime
   from typing import Optional

   from src.models import Task, MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH
   from src.task_repository import TaskRepository
   from src.exceptions import ValidationError, TaskNotFoundError
   ```

2. **TaskService class with initialization:**
   ```python
   class TaskService:
       """
       Service layer for task management operations.

       Handles business logic, validation, and coordinates repository calls.
       """

       def __init__(self, repository: TaskRepository) -> None:
           """
           Initialize service with repository.

           Args:
               repository: TaskRepository instance for data access
           """
           self.repository = repository
   ```

3. **Helper methods:**
   ```python
       def _validate_title(self, title: str) -> str:
           """
           Validate and normalize task title.

           Args:
               title: Raw title string

           Returns:
               Stripped title

           Raises:
               ValidationError: If title is empty or too long
           """
           stripped = title.strip()
           if not stripped:
               raise ValidationError("Task title cannot be empty")
           if len(stripped) > MAX_TITLE_LENGTH:
               raise ValidationError(
                   f"Task title cannot exceed {MAX_TITLE_LENGTH} characters "
                   f"(got {len(stripped)})"
               )
           return stripped

       def _validate_description(self, description: str) -> str:
           """
           Validate task description.

           Args:
               description: Description string

           Returns:
               Description (unchanged)

           Raises:
               ValidationError: If description is too long
           """
           if len(description) > MAX_DESCRIPTION_LENGTH:
               raise ValidationError(
                   f"Task description cannot exceed {MAX_DESCRIPTION_LENGTH} characters "
                   f"(got {len(description)})"
               )
           return description

       def _generate_timestamp(self) -> str:
           """
           Generate ISO 8601 timestamp for current time.

           Returns:
               Timestamp string in ISO 8601 format
           """
           return datetime.now().isoformat()
   ```

**Success Criteria:**
- [ ] TaskService class defined with `__init__`
- [ ] `_validate_title()` strips whitespace and validates length
- [ ] `_validate_title()` raises ValidationError for empty title
- [ ] `_validate_title()` raises ValidationError for title >200 chars
- [ ] `_validate_description()` validates length ≤1000 chars
- [ ] `_generate_timestamp()` returns ISO 8601 format string
- [ ] All helper methods have type hints and docstrings
- [ ] File passes type checking: `mypy src/task_service.py`
- [ ] File passes linting: `ruff check src/task_service.py`

**Validation Commands:**
```bash
cd phase1
mypy src/task_service.py
ruff check src/task_service.py
python -c "
from src.task_service import TaskService
from src.task_repository import TaskRepository
service = TaskService(TaskRepository())
print(f'Timestamp: {service._generate_timestamp()}')
print(f'Valid title: {service._validate_title(\"  Test  \")}')
print('Service core: OK')
"
```

**Estimated Effort:** 20 minutes

---

### Task 2.2: Implement Add Task Operation
**Status:** ⬜

**Description:**
Implement the `add_task()` method in TaskService with full validation, timestamp generation, and task creation.

**Files to Modify:**
- `phase1/src/task_service.py` (add method to TaskService class)

**Spec Reference:**
- [SPECIFICATION.md § Feature 1: Add Task](./SPECIFICATION.md#feature-1-add-task)
- [PLAN.md § Step 3.1: add_task method](./PLAN.md#step-3-business-logic-layer)

**Implementation Details:**

Add this method to the `TaskService` class in `src/task_service.py`:

```python
    def add_task(self, title: str, description: str = "") -> Task:
        """
        Create a new task with validation.

        Args:
            title: Task title (required, 1-200 characters)
            description: Task description (optional, 0-1000 characters)

        Returns:
            Created Task object

        Raises:
            ValidationError: If title or description validation fails

        Examples:
            >>> service.add_task("Buy groceries")
            >>> service.add_task("Finish report", "Q4 analysis")
        """
        # Validate inputs
        validated_title = self._validate_title(title)
        validated_description = self._validate_description(description)

        # Generate ID and timestamps
        task_id = self.repository.generate_id()
        timestamp = self._generate_timestamp()

        # Create task object
        task: Task = {
            "id": task_id,
            "title": validated_title,
            "description": validated_description,
            "completed": False,
            "created_at": timestamp,
            "updated_at": timestamp
        }

        # Store and return
        return self.repository.create(task)
```

**Success Criteria:**
- [ ] `add_task()` method added to TaskService class
- [ ] Method validates title using `_validate_title()`
- [ ] Method validates description using `_validate_description()`
- [ ] Method generates unique ID via repository
- [ ] Method sets `created_at` and `updated_at` to same timestamp
- [ ] Method sets `completed` to False
- [ ] Method returns created Task object
- [ ] Method has comprehensive docstring with examples
- [ ] File passes type checking: `mypy src/task_service.py`
- [ ] Can create task: manual test successful

**Validation Commands:**
```bash
cd phase1
mypy src/task_service.py
ruff check src/task_service.py
python -c "
from src.task_service import TaskService
from src.task_repository import TaskRepository
service = TaskService(TaskRepository())
task = service.add_task('Test Task', 'Test Description')
print(f'Created task: ID={task[\"id\"]}, Title={task[\"title\"]}, Completed={task[\"completed\"]}')
assert task['id'] == 1
assert task['title'] == 'Test Task'
assert task['completed'] == False
print('add_task: OK')
"
```

**Estimated Effort:** 15 minutes

---

### Task 2.3: Implement Get Tasks Operations
**Status:** ⬜

**Description:**
Implement `get_all_tasks()` and `get_task_by_id()` methods for task retrieval.

**Files to Modify:**
- `phase1/src/task_service.py` (add methods to TaskService class)

**Spec Reference:**
- [SPECIFICATION.md § Feature 2: View Task List](./SPECIFICATION.md#feature-2-view-task-list)
- [SPECIFICATION.md § Feature 3: View Single Task](./SPECIFICATION.md#feature-3-view-single-task-detail-view)

**Implementation Details:**

Add these methods to the `TaskService` class:

```python
    def get_all_tasks(self) -> list[Task]:
        """
        Retrieve all tasks sorted by ID.

        Returns:
            List of all tasks, sorted by ID ascending

        Examples:
            >>> tasks = service.get_all_tasks()
            >>> print(f"Total tasks: {len(tasks)}")
        """
        return self.repository.find_all()

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Retrieve a specific task by ID.

        Args:
            task_id: ID of task to retrieve

        Returns:
            Task object

        Raises:
            TaskNotFoundError: If task ID doesn't exist

        Examples:
            >>> task = service.get_task_by_id(1)
            >>> print(task["title"])
        """
        task = self.repository.find_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task
```

**Success Criteria:**
- [ ] `get_all_tasks()` returns list from repository
- [ ] `get_all_tasks()` returns empty list when no tasks
- [ ] `get_task_by_id()` returns task when ID exists
- [ ] `get_task_by_id()` raises TaskNotFoundError when ID doesn't exist
- [ ] Both methods have docstrings with examples
- [ ] File passes type checking
- [ ] Can retrieve tasks: manual test successful

**Validation Commands:**
```bash
cd phase1
mypy src/task_service.py
ruff check src/task_service.py
python -c "
from src.task_service import TaskService
from src.task_repository import TaskRepository
from src.exceptions import TaskNotFoundError

service = TaskService(TaskRepository())

# Test get_all_tasks (empty)
tasks = service.get_all_tasks()
assert tasks == []

# Add a task
task = service.add_task('Test Task')

# Test get_all_tasks (with task)
tasks = service.get_all_tasks()
assert len(tasks) == 1

# Test get_task_by_id (exists)
retrieved = service.get_task_by_id(1)
assert retrieved['id'] == 1

# Test get_task_by_id (not found)
try:
    service.get_task_by_id(999)
    assert False, 'Should raise TaskNotFoundError'
except TaskNotFoundError as e:
    assert e.task_id == 999

print('get tasks operations: OK')
"
```

**Estimated Effort:** 15 minutes

---

### Task 2.4: Implement Update Task Operation
**Status:** ⬜

**Description:**
Implement `update_task()` method to modify task title and/or description with validation.

**Files to Modify:**
- `phase1/src/task_service.py` (add method to TaskService class)

**Spec Reference:**
- [SPECIFICATION.md § Feature 4: Update Task](./SPECIFICATION.md#feature-4-update-task)

**Implementation Details:**

Add this method to the `TaskService` class:

```python
    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """
        Update task title and/or description.

        Args:
            task_id: ID of task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task ID doesn't exist
            ValidationError: If no fields provided or validation fails

        Examples:
            >>> service.update_task(1, title="New Title")
            >>> service.update_task(1, description="New Description")
            >>> service.update_task(1, title="Title", description="Desc")
        """
        # Validate at least one field provided
        if title is None and description is None:
            raise ValidationError(
                "Must provide at least one field to update (title or description)"
            )

        # Retrieve existing task
        task = self.get_task_by_id(task_id)  # Raises TaskNotFoundError if not found

        # Validate and update title if provided
        if title is not None:
            task["title"] = self._validate_title(title)

        # Validate and update description if provided
        if description is not None:
            task["description"] = self._validate_description(description)

        # Update timestamp
        task["updated_at"] = self._generate_timestamp()

        # Store and return
        return self.repository.update(task_id, task)
```

**Success Criteria:**
- [ ] `update_task()` can update title only
- [ ] `update_task()` can update description only
- [ ] `update_task()` can update both title and description
- [ ] `update_task()` raises ValidationError if no fields provided
- [ ] `update_task()` raises TaskNotFoundError for invalid ID
- [ ] `update_task()` updates `updated_at` timestamp
- [ ] `update_task()` preserves `created_at` timestamp
- [ ] `update_task()` preserves `id` and `completed` fields
- [ ] Method has comprehensive docstring
- [ ] File passes type checking

**Validation Commands:**
```bash
cd phase1
mypy src/task_service.py
ruff check src/task_service.py
python -c "
from src.task_service import TaskService
from src.task_repository import TaskRepository
from src.exceptions import ValidationError
import time

service = TaskService(TaskRepository())
task = service.add_task('Original Title', 'Original Desc')
original_created = task['created_at']

time.sleep(0.01)  # Ensure timestamp difference

# Update title only
updated = service.update_task(1, title='New Title')
assert updated['title'] == 'New Title'
assert updated['description'] == 'Original Desc'
assert updated['created_at'] == original_created
assert updated['updated_at'] != original_created

# Update description only
updated = service.update_task(1, description='New Desc')
assert updated['description'] == 'New Desc'

# Test error: no fields
try:
    service.update_task(1)
    assert False, 'Should raise ValidationError'
except ValidationError:
    pass

print('update_task: OK')
"
```

**Estimated Effort:** 20 minutes

---

### Task 2.5: Implement Delete Task Operation
**Status:** ⬜

**Description:**
Implement `delete_task()` method to permanently remove tasks.

**Files to Modify:**
- `phase1/src/task_service.py` (add method to TaskService class)

**Spec Reference:**
- [SPECIFICATION.md § Feature 5: Delete Task](./SPECIFICATION.md#feature-5-delete-task)

**Implementation Details:**

Add this method to the `TaskService` class:

```python
    def delete_task(self, task_id: int) -> Task:
        """
        Delete a task permanently.

        Args:
            task_id: ID of task to delete

        Returns:
            The deleted Task object (for confirmation message)

        Raises:
            TaskNotFoundError: If task ID doesn't exist

        Examples:
            >>> deleted = service.delete_task(1)
            >>> print(f"Deleted: {deleted['title']}")
        """
        # Retrieve task first (for return value and validation)
        task = self.get_task_by_id(task_id)  # Raises TaskNotFoundError if not found

        # Delete from repository
        self.repository.delete(task_id)

        return task
```

**Success Criteria:**
- [ ] `delete_task()` removes task from storage
- [ ] `delete_task()` returns deleted task object
- [ ] `delete_task()` raises TaskNotFoundError for invalid ID
- [ ] Deleted task ID is not reused for new tasks
- [ ] Other tasks remain unaffected
- [ ] Method has docstring with examples
- [ ] File passes type checking

**Validation Commands:**
```bash
cd phase1
mypy src/task_service.py
ruff check src/task_service.py
python -c "
from src.task_service import TaskService
from src.task_repository import TaskRepository
from src.exceptions import TaskNotFoundError

service = TaskService(TaskRepository())

# Add tasks
task1 = service.add_task('Task 1')
task2 = service.add_task('Task 2')
task3 = service.add_task('Task 3')

# Delete task 2
deleted = service.delete_task(2)
assert deleted['id'] == 2
assert deleted['title'] == 'Task 2'

# Verify task 2 is gone
try:
    service.get_task_by_id(2)
    assert False, 'Should raise TaskNotFoundError'
except TaskNotFoundError:
    pass

# Verify tasks 1 and 3 still exist
assert service.get_task_by_id(1)['title'] == 'Task 1'
assert service.get_task_by_id(3)['title'] == 'Task 3'

# Verify new tasks get new IDs (not reusing 2)
task4 = service.add_task('Task 4')
assert task4['id'] == 4

print('delete_task: OK')
"
```

**Estimated Effort:** 10 minutes

---

### Task 2.6: Implement Complete/Uncomplete Operations
**Status:** ⬜

**Description:**
Implement `complete_task()` and `uncomplete_task()` methods to toggle task completion status.

**Files to Modify:**
- `phase1/src/task_service.py` (add methods to TaskService class)

**Spec Reference:**
- [SPECIFICATION.md § Feature 6: Mark Task as Complete](./SPECIFICATION.md#feature-6-mark-task-as-complete)
- [SPECIFICATION.md § Feature 7: Mark Task as Incomplete](./SPECIFICATION.md#feature-7-mark-task-as-incomplete)

**Implementation Details:**

Add these methods to the `TaskService` class:

```python
    def complete_task(self, task_id: int) -> Task:
        """
        Mark a task as completed.

        Args:
            task_id: ID of task to complete

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task ID doesn't exist

        Note:
            Idempotent - marking an already-completed task as complete
            is allowed and updates the timestamp.

        Examples:
            >>> task = service.complete_task(1)
            >>> print(f"Status: {task['completed']}")  # True
        """
        # Retrieve task
        task = self.get_task_by_id(task_id)

        # Update completion status
        task["completed"] = True
        task["updated_at"] = self._generate_timestamp()

        # Store and return
        return self.repository.update(task_id, task)

    def uncomplete_task(self, task_id: int) -> Task:
        """
        Mark a task as incomplete.

        Args:
            task_id: ID of task to mark incomplete

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task ID doesn't exist

        Note:
            Idempotent - marking an already-incomplete task as incomplete
            is allowed and updates the timestamp.

        Examples:
            >>> task = service.uncomplete_task(1)
            >>> print(f"Status: {task['completed']}")  # False
        """
        # Retrieve task
        task = self.get_task_by_id(task_id)

        # Update completion status
        task["completed"] = False
        task["updated_at"] = self._generate_timestamp()

        # Store and return
        return self.repository.update(task_id, task)
```

**Success Criteria:**
- [ ] `complete_task()` sets `completed` to True
- [ ] `complete_task()` updates `updated_at` timestamp
- [ ] `complete_task()` is idempotent (can complete twice)
- [ ] `uncomplete_task()` sets `completed` to False
- [ ] `uncomplete_task()` updates `updated_at` timestamp
- [ ] `uncomplete_task()` is idempotent (can uncomplete twice)
- [ ] Both methods raise TaskNotFoundError for invalid IDs
- [ ] Both methods preserve all other fields
- [ ] File passes type checking

**Validation Commands:**
```bash
cd phase1
mypy src/task_service.py
ruff check src/task_service.py
python -c "
from src.task_service import TaskService
from src.task_repository import TaskRepository

service = TaskService(TaskRepository())
task = service.add_task('Test Task')

# Initially incomplete
assert task['completed'] == False

# Mark complete
completed = service.complete_task(1)
assert completed['completed'] == True

# Mark complete again (idempotent)
completed = service.complete_task(1)
assert completed['completed'] == True

# Mark incomplete
incompleted = service.uncomplete_task(1)
assert incompleted['completed'] == False

# Mark incomplete again (idempotent)
incompleted = service.uncomplete_task(1)
assert incompleted['completed'] == False

print('complete/uncomplete operations: OK')
"
```

**Estimated Effort:** 15 minutes

---

## Milestone 3: CLI Interface Implementation

### Task 3.1: Implement CLI Formatter
**Status:** ⬜

**Description:**
Create display helper functions for formatting task lists, task details, messages, and the help screen.

**Files to Create:**
- `phase1/src/cli_formatter.py`

**Spec Reference:**
- [SPECIFICATION.md § CLI Interface Specification](./SPECIFICATION.md#cli-interface-specification)
- [PLAN.md § Step 4.1: Create src/cli_formatter.py](./PLAN.md#step-4-cli-interface-layer)

**Implementation Details:**

Create `src/cli_formatter.py` with these functions:

1. **Module docstring:**
   ```python
   """
   CLI display formatting utilities.

   Functions for formatting task lists, details, messages, and help text.
   """
   ```

2. **Import statements:**
   ```python
   from src.models import Task
   from datetime import datetime
   ```

3. **Implement formatting functions:**
   - `format_welcome() -> str`: Welcome banner
   - `format_goodbye() -> str`: Exit message
   - `format_help() -> str`: Complete help text with all commands
   - `format_success(message: str) -> str`: Success message with ✓
   - `format_error(message: str) -> str`: Error message with ✗
   - `format_task_list(tasks: list[Task]) -> str`: Formatted table
   - `format_task_detail(task: Task) -> str`: Detailed view
   - `_format_timestamp(iso_timestamp: str) -> str`: ISO to readable format
   - `_truncate_title(title: str, max_length: int = 50) -> str`: Truncate with ...

See SPECIFICATION.md § Feature 2 and § CLI Interface for exact format.

**Success Criteria:**
- [ ] `format_welcome()` returns welcome banner
- [ ] `format_help()` returns comprehensive help text with all 9 commands
- [ ] `format_task_list([])` shows "No tasks found" message
- [ ] `format_task_list(tasks)` shows table with headers and summary
- [ ] `format_task_detail(task)` shows all task fields
- [ ] Task list truncates titles >50 chars with "..."
- [ ] Timestamps formatted as "YYYY-MM-DD HH:MM"
- [ ] Status shown as [ ] for incomplete, [✓] for complete
- [ ] All functions have type hints and docstrings
- [ ] File passes type checking

**Validation Commands:**
```bash
cd phase1
mypy src/cli_formatter.py
ruff check src/cli_formatter.py
python -c "
from src.cli_formatter import format_welcome, format_help, format_task_list, format_success
print(format_welcome())
print(format_success('Test message'))
print(format_task_list([]))
help_text = format_help()
assert 'add' in help_text
assert 'delete' in help_text
print('CLI formatter: OK')
"
```

**Estimated Effort:** 40 minutes

---

### Task 3.2: Implement Command Parser
**Status:** ⬜

**Description:**
Create command parsing logic to extract command names, arguments, and flags from user input.

**Files to Create:**
- `phase1/src/command_parser.py`

**Spec Reference:**
- [SPECIFICATION.md § CLI Interface Specification § Command Parsing Rules](./SPECIFICATION.md#cli-interface-specification)
- [PLAN.md § Step 4.2: Create src/command_parser.py](./PLAN.md#step-4-cli-interface-layer)

**Implementation Details:**

Create `src/command_parser.py` with:

1. **Module docstring:**
   ```python
   """
   Command-line input parsing utilities.

   Parses user input into command name, arguments, and flags.
   """
   ```

2. **Constants:**
   ```python
   VALID_COMMANDS = [
       "add", "list", "view", "update", "delete",
       "complete", "uncomplete", "help", "exit"
   ]
   ```

3. **Parse function:**
   ```python
   def parse_command(input_str: str) -> tuple[str, list[str], dict[str, str]]:
       """
       Parse command input into components.

       Args:
           input_str: Raw user input

       Returns:
           Tuple of (command_name, args, flags)
           - command_name: Lowercased command (e.g., "add")
           - args: Positional arguments (e.g., ["1", "Buy milk"])
           - flags: Flag dictionary (e.g., {"title": "New Title"})

       Examples:
           >>> parse_command("add Buy milk")
           ("add", ["Buy milk"], {})

           >>> parse_command('add "Buy milk" "From store"')
           ("add", ["Buy milk", "From store"], {})

           >>> parse_command("update 1 --title New Title")
           ("update", ["1"], {"title": "New Title"})
       """
       # Implementation:
       # 1. Strip and split by spaces (respecting quotes)
       # 2. First token is command (lowercase)
       # 3. Subsequent tokens are args or flags
       # 4. Flags start with -- and take next token as value
       # 5. Handle quoted strings as single arguments
   ```

4. **Validation function:**
   ```python
   def is_valid_command(command: str) -> bool:
       """
       Check if command name is valid.

       Args:
           command: Command name to validate

       Returns:
           True if valid, False otherwise
       """
       return command.lower() in VALID_COMMANDS
   ```

**Success Criteria:**
- [ ] `parse_command("add Task")` returns `("add", ["Task"], {})`
- [ ] `parse_command('add "Task with spaces"')` handles quotes
- [ ] `parse_command("update 1 --title New")` returns flags dict
- [ ] Commands are case-insensitive
- [ ] Leading/trailing whitespace ignored
- [ ] `is_valid_command("add")` returns True
- [ ] `is_valid_command("invalid")` returns False
- [ ] All functions have type hints and docstrings
- [ ] File passes type checking

**Validation Commands:**
```bash
cd phase1
mypy src/command_parser.py
ruff check src/command_parser.py
python -c "
from src.command_parser import parse_command, is_valid_command, VALID_COMMANDS

# Test simple command
cmd, args, flags = parse_command('add Test Task')
assert cmd == 'add'
assert args == ['Test', 'Task'] or args == ['Test Task']

# Test valid command check
assert is_valid_command('add') == True
assert is_valid_command('invalid') == False
assert len(VALID_COMMANDS) == 9

print('Command parser: OK')
"
```

**Estimated Effort:** 30 minutes

---

### Task 3.3: Implement Main CLI Application
**Status:** ⬜

**Description:**
Create the main application entry point with command loop, routing, and command handlers.

**Files to Create:**
- `phase1/src/main.py`

**Spec Reference:**
- [SPECIFICATION.md § CLI Interface Specification § Application Lifecycle](./SPECIFICATION.md#cli-interface-specification)
- [PLAN.md § Step 4.3: Create src/main.py](./PLAN.md#step-4-cli-interface-layer)

**Implementation Details:**

Create `src/main.py` with:

1. **Module docstring and imports:**
   ```python
   """
   Main CLI application entry point.

   Handles user interaction loop, command routing, and display.
   """
   from src.task_service import TaskService
   from src.task_repository import TaskRepository
   from src.command_parser import parse_command, is_valid_command
   from src.cli_formatter import (
       format_welcome, format_goodbye, format_help,
       format_success, format_error,
       format_task_list, format_task_detail
   )
   from src.exceptions import TodoAppError
   ```

2. **Command handler functions:**
   - `handle_add(args: list[str], service: TaskService) -> None`
   - `handle_list(service: TaskService) -> None`
   - `handle_view(args: list[str], service: TaskService) -> None`
   - `handle_update(args: list[str], flags: dict[str, str], service: TaskService) -> None`
   - `handle_delete(args: list[str], service: TaskService) -> None`
   - `handle_complete(args: list[str], service: TaskService) -> None`
   - `handle_uncomplete(args: list[str], service: TaskService) -> None`
   - `handle_help() -> None`

3. **Main loop:**
   ```python
   def main() -> None:
       """Main application loop."""
       repository = TaskRepository()
       service = TaskService(repository)

       print(format_welcome())

       while True:
           try:
               user_input = input("> ").strip()

               if not user_input:
                   continue

               command, args, flags = parse_command(user_input)

               if command == "exit":
                   print(format_goodbye())
                   break

               if not is_valid_command(command):
                   print(format_error(f"Unknown command '{command}'. Type 'help' for available commands."))
                   continue

               # Route to appropriate handler
               if command == "add":
                   handle_add(args, service)
               elif command == "list":
                   handle_list(service)
               elif command == "view":
                   handle_view(args, service)
               elif command == "update":
                   handle_update(args, flags, service)
               elif command == "delete":
                   handle_delete(args, service)
               elif command == "complete":
                   handle_complete(args, service)
               elif command == "uncomplete":
                   handle_uncomplete(args, service)
               elif command == "help":
                   handle_help()

           except TodoAppError as e:
               print(format_error(str(e)))
           except KeyboardInterrupt:
               print("\n" + format_goodbye())
               break
           except Exception as e:
               print(format_error(f"An unexpected error occurred: {e}"))

   if __name__ == "__main__":
       main()
   ```

**Success Criteria:**
- [ ] Application starts and shows welcome message
- [ ] `help` command displays help text
- [ ] `exit` command terminates gracefully
- [ ] Unknown commands show error message
- [ ] Empty input is ignored (no error)
- [ ] Ctrl+C exits gracefully
- [ ] Errors display with format_error()
- [ ] All command handlers implemented
- [ ] File passes type checking

**Validation Commands:**
```bash
cd phase1
mypy src/main.py
ruff check src/main.py
# Manual test:
python src/main.py
# Type: help
# Type: exit
```

**Estimated Effort:** 60 minutes

---

## Milestone 4: Testing & Quality Assurance

### Task 4.1: Create Test Fixtures
**Status:** ⬜

**Description:**
Set up pytest fixtures for consistent test setup across all test modules.

**Files to Create:**
- `phase1/tests/conftest.py`

**Spec Reference:**
- [SPECIFICATION.md § Testing Requirements § Test Fixtures](./SPECIFICATION.md#testing-requirements)

**Implementation Details:**

Create `tests/conftest.py` with:

```python
"""
Pytest configuration and shared fixtures.

Provides reusable test fixtures for repository and service instances.
"""
import pytest
from src.task_repository import TaskRepository
from src.task_service import TaskService

@pytest.fixture
def empty_repository():
    """Provide a fresh, empty repository for each test."""
    repo = TaskRepository()
    repo.clear()
    return repo

@pytest.fixture
def repository_with_tasks(empty_repository):
    """Provide a repository with 3 sample tasks."""
    repo = empty_repository

    # Create sample tasks directly in repository
    task1 = {
        "id": 1,
        "title": "Task 1",
        "description": "Description 1",
        "completed": False,
        "created_at": "2025-01-01T10:00:00",
        "updated_at": "2025-01-01T10:00:00"
    }
    task2 = {
        "id": 2,
        "title": "Task 2",
        "description": "",
        "completed": True,
        "created_at": "2025-01-01T11:00:00",
        "updated_at": "2025-01-01T11:00:00"
    }
    task3 = {
        "id": 3,
        "title": "Task 3",
        "description": "Description 3",
        "completed": False,
        "created_at": "2025-01-01T12:00:00",
        "updated_at": "2025-01-01T12:00:00"
    }

    repo.create(task1)
    repo.create(task2)
    repo.create(task3)
    repo._next_id = 4  # Set next ID to 4

    return repo

@pytest.fixture
def task_service(empty_repository):
    """Provide a TaskService with empty repository."""
    return TaskService(empty_repository)

@pytest.fixture
def task_service_with_data(repository_with_tasks):
    """Provide a TaskService with sample data."""
    return TaskService(repository_with_tasks)
```

**Success Criteria:**
- [ ] 4 fixtures defined
- [ ] `empty_repository` returns clean TaskRepository
- [ ] `repository_with_tasks` creates 3 tasks
- [ ] Fixtures properly isolated (no cross-test contamination)
- [ ] File passes type checking
- [ ] Fixtures can be imported by test files

**Validation Commands:**
```bash
cd phase1
mypy tests/conftest.py
pytest tests/conftest.py -v
```

**Estimated Effort:** 15 minutes

---

### Task 4.2: Implement Repository Tests
**Status:** ⬜

**Description:**
Create comprehensive unit tests for the TaskRepository data layer.

**Files to Create:**
- `phase1/tests/test_task_repository.py`

**Spec Reference:**
- [SPECIFICATION.md § Testing Requirements § test_task_repository.py](./SPECIFICATION.md#testing-requirements)

**Implementation Details:**

Create `tests/test_task_repository.py` with these test functions:

1. **Module docstring:**
   ```python
   """
   Unit tests for TaskRepository (data access layer).

   Tests CRUD operations and ID generation.
   """
   ```

2. **Test functions (9 total):**
   - `test_generate_unique_ids(empty_repository)`: IDs are 1, 2, 3...
   - `test_create_task(empty_repository)`: Task stored with correct ID
   - `test_find_by_id_existing(repository_with_tasks)`: Returns correct task
   - `test_find_by_id_not_found(empty_repository)`: Returns None
   - `test_find_all_empty(empty_repository)`: Returns empty list
   - `test_find_all_multiple(repository_with_tasks)`: Returns all tasks sorted
   - `test_update_task(repository_with_tasks)`: Updates task in storage
   - `test_delete_task_existing(repository_with_tasks)`: Removes task successfully
   - `test_delete_task_nonexistent(empty_repository)`: Returns False

Each test should:
- Use appropriate fixture
- Test one specific behavior
- Have clear assertions
- Include docstring explaining what it tests

**Success Criteria:**
- [ ] All 9 tests implemented
- [ ] All tests pass: `pytest tests/test_task_repository.py -v`
- [ ] Each test has descriptive docstring
- [ ] Tests use fixtures appropriately
- [ ] File passes type checking
- [ ] Tests cover happy paths and error cases

**Validation Commands:**
```bash
cd phase1
pytest tests/test_task_repository.py -v
pytest tests/test_task_repository.py --cov=src/task_repository --cov-report=term-missing
mypy tests/test_task_repository.py
```

**Estimated Effort:** 30 minutes

---

### Task 4.3: Implement Service Tests (Part 1: Add & Get)
**Status:** ⬜

**Description:**
Create unit tests for TaskService add and get operations.

**Files to Create:**
- `phase1/tests/test_task_service.py` (part 1)

**Spec Reference:**
- [SPECIFICATION.md § Testing Requirements § test_task_service.py](./SPECIFICATION.md#testing-requirements)

**Implementation Details:**

Create `tests/test_task_service.py` with:

1. **Module docstring:**
   ```python
   """
   Unit tests for TaskService (business logic layer).

   Tests validation, business rules, and service operations.
   """
   import pytest
   from src.exceptions import ValidationError, TaskNotFoundError
   ```

2. **Add Task Tests (6 tests):**
   - `test_add_task_with_title_and_description(task_service)`
   - `test_add_task_with_title_only(task_service)`
   - `test_add_task_strips_whitespace(task_service)`
   - `test_add_task_empty_title_raises_error(task_service)`
   - `test_add_task_title_too_long_raises_error(task_service)`
   - `test_add_task_description_too_long_raises_error(task_service)`

3. **Get Tasks Tests (4 tests):**
   - `test_get_all_tasks_empty(task_service)`
   - `test_get_all_tasks_multiple_sorted(task_service_with_data)`
   - `test_get_task_by_id_found(task_service_with_data)`
   - `test_get_task_by_id_not_found_raises_error(task_service)`

**Success Criteria:**
- [ ] 10 tests implemented and passing
- [ ] Tests verify validation rules
- [ ] Tests use pytest.raises for exception testing
- [ ] Each test has docstring
- [ ] File passes type checking

**Validation Commands:**
```bash
cd phase1
pytest tests/test_task_service.py::test_add_task_with_title_and_description -v
pytest tests/test_task_service.py -k "add or get" -v
mypy tests/test_task_service.py
```

**Estimated Effort:** 40 minutes

---

### Task 4.4: Implement Service Tests (Part 2: Update, Delete, Complete)
**Status:** ⬜

**Description:**
Complete TaskService tests with update, delete, and complete/uncomplete operations.

**Files to Modify:**
- `phase1/tests/test_task_service.py` (add more tests)

**Spec Reference:**
- [SPECIFICATION.md § Testing Requirements § test_task_service.py](./SPECIFICATION.md#testing-requirements)

**Implementation Details:**

Add these test functions to `tests/test_task_service.py`:

1. **Update Task Tests (7 tests):**
   - `test_update_task_title_only(task_service_with_data)`
   - `test_update_task_description_only(task_service_with_data)`
   - `test_update_task_both_fields(task_service_with_data)`
   - `test_update_task_preserves_other_fields(task_service_with_data)`
   - `test_update_task_not_found_raises_error(task_service)`
   - `test_update_task_invalid_title_raises_error(task_service_with_data)`
   - `test_update_task_no_fields_raises_error(task_service_with_data)`

2. **Delete Task Tests (2 tests):**
   - `test_delete_task_existing(task_service_with_data)`
   - `test_delete_task_not_found_raises_error(task_service)`

3. **Complete/Uncomplete Tests (4 tests):**
   - `test_complete_task(task_service_with_data)`
   - `test_complete_task_already_complete_idempotent(task_service_with_data)`
   - `test_uncomplete_task(task_service_with_data)`
   - `test_uncomplete_task_already_incomplete_idempotent(task_service_with_data)`

4. **Timestamp Tests (3 tests):**
   - `test_timestamps_set_on_create(task_service)`
   - `test_updated_at_changes_on_update(task_service)`
   - `test_created_at_immutable_on_update(task_service)`

**Success Criteria:**
- [ ] All 16 additional tests implemented
- [ ] Total test count for file: 26 tests
- [ ] All tests pass
- [ ] Timestamp tests verify immutability of created_at
- [ ] Idempotent tests verify repeated operations

**Validation Commands:**
```bash
cd phase1
pytest tests/test_task_service.py -v
pytest tests/test_task_service.py --cov=src/task_service --cov-report=term-missing
mypy tests/test_task_service.py
```

**Estimated Effort:** 50 minutes

---

### Task 4.5: Implement Model Tests
**Status:** ⬜

**Description:**
Create simple tests to validate Task model structure and constants.

**Files to Create:**
- `phase1/tests/test_models.py`

**Spec Reference:**
- [SPECIFICATION.md § Testing Requirements § test_models.py](./SPECIFICATION.md#testing-requirements)

**Implementation Details:**

Create `tests/test_models.py` with:

```python
"""
Unit tests for data models.

Tests Task TypedDict structure and validation constants.
"""
from src.models import Task, MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH

def test_task_has_all_required_fields():
    """Verify Task TypedDict has all 6 required fields."""
    # Create a valid task
    task: Task = {
        "id": 1,
        "title": "Test",
        "description": "Test description",
        "completed": False,
        "created_at": "2025-01-01T10:00:00",
        "updated_at": "2025-01-01T10:00:00"
    }

    assert "id" in task
    assert "title" in task
    assert "description" in task
    assert "completed" in task
    assert "created_at" in task
    assert "updated_at" in task

def test_task_field_types():
    """Verify Task field types are correct."""
    task: Task = {
        "id": 1,
        "title": "Test",
        "description": "Desc",
        "completed": True,
        "created_at": "2025-01-01T10:00:00",
        "updated_at": "2025-01-01T10:00:00"
    }

    assert isinstance(task["id"], int)
    assert isinstance(task["title"], str)
    assert isinstance(task["description"], str)
    assert isinstance(task["completed"], bool)
    assert isinstance(task["created_at"], str)
    assert isinstance(task["updated_at"], str)

def test_constants():
    """Verify validation constants have correct values."""
    assert MAX_TITLE_LENGTH == 200
    assert MAX_DESCRIPTION_LENGTH == 1000
```

**Success Criteria:**
- [ ] 3 tests implemented
- [ ] All tests pass
- [ ] Tests verify Task structure
- [ ] Tests verify constants
- [ ] File passes type checking

**Validation Commands:**
```bash
cd phase1
pytest tests/test_models.py -v
mypy tests/test_models.py
```

**Estimated Effort:** 15 minutes

---

### Task 4.6: Implement Integration Tests
**Status:** ⬜

**Description:**
Create end-to-end integration tests that simulate complete user workflows.

**Files to Create:**
- `phase1/tests/test_integration.py`

**Spec Reference:**
- [SPECIFICATION.md § Testing Requirements § test_integration.py](./SPECIFICATION.md#testing-requirements)
- [PLAN.md § Step 5: Integration Testing](./PLAN.md#step-5-integration-testing)

**Implementation Details:**

Create `tests/test_integration.py` with:

```python
"""
Integration tests for complete user workflows.

Tests end-to-end scenarios across all layers.
"""
import pytest
import time
from src.task_service import TaskService
from src.task_repository import TaskRepository

@pytest.fixture
def fresh_service():
    """Provide a fresh service for each integration test."""
    return TaskService(TaskRepository())

def test_complete_user_workflow(fresh_service):
    """
    Test complete user workflow: add → view → update → complete → delete.

    Simulates a user creating, managing, and deleting a task.
    """
    service = fresh_service

    # Add task
    task = service.add_task("Buy groceries", "Milk and eggs")
    assert task["id"] == 1
    assert task["title"] == "Buy groceries"
    assert task["completed"] == False

    # View all tasks
    tasks = service.get_all_tasks()
    assert len(tasks) == 1

    # View task detail
    retrieved = service.get_task_by_id(1)
    assert retrieved["title"] == "Buy groceries"

    # Update task
    updated = service.update_task(1, title="Buy groceries and snacks")
    assert updated["title"] == "Buy groceries and snacks"

    # Complete task
    completed = service.complete_task(1)
    assert completed["completed"] == True

    # Delete task
    deleted = service.delete_task(1)
    assert deleted["id"] == 1

    # Verify deletion
    tasks = service.get_all_tasks()
    assert len(tasks) == 0

def test_multiple_tasks_management(fresh_service):
    """
    Test managing multiple tasks simultaneously.

    Create 10 tasks, complete 5, delete 2, verify state.
    """
    service = fresh_service

    # Add 10 tasks
    for i in range(1, 11):
        service.add_task(f"Task {i}", f"Description {i}")

    # Verify all created
    tasks = service.get_all_tasks()
    assert len(tasks) == 10

    # Complete tasks 1, 3, 5, 7, 9
    for task_id in [1, 3, 5, 7, 9]:
        service.complete_task(task_id)

    # Delete tasks 2, 4
    service.delete_task(2)
    service.delete_task(4)

    # Verify final state
    tasks = service.get_all_tasks()
    assert len(tasks) == 8

    # Count completed tasks
    completed_count = sum(1 for task in tasks if task["completed"])
    assert completed_count == 5

def test_error_recovery(fresh_service):
    """
    Test that application continues after errors.

    Trigger validation error, then successfully add task.
    """
    service = fresh_service

    # Trigger validation error
    with pytest.raises(Exception):
        service.add_task("")  # Empty title

    # Application should still work
    task = service.add_task("Valid task")
    assert task["id"] == 1

def test_task_independence(fresh_service):
    """
    Test that modifying one task doesn't affect others.

    Create 3 tasks, update task 2, verify tasks 1 and 3 unchanged.
    """
    service = fresh_service

    # Create 3 tasks
    task1 = service.add_task("Task 1", "Desc 1")
    task2 = service.add_task("Task 2", "Desc 2")
    task3 = service.add_task("Task 3", "Desc 3")

    # Update task 2
    service.update_task(2, title="Updated Task 2")

    # Verify task 1 unchanged
    retrieved1 = service.get_task_by_id(1)
    assert retrieved1["title"] == "Task 1"
    assert retrieved1["description"] == "Desc 1"

    # Verify task 3 unchanged
    retrieved3 = service.get_task_by_id(3)
    assert retrieved3["title"] == "Task 3"
    assert retrieved3["description"] == "Desc 3"

    # Verify task 2 changed
    retrieved2 = service.get_task_by_id(2)
    assert retrieved2["title"] == "Updated Task 2"

def test_idempotent_operations(fresh_service):
    """
    Test that idempotent operations work correctly.

    Complete task twice, uncomplete task twice.
    """
    service = fresh_service

    task = service.add_task("Test Task")

    # Mark complete twice
    service.complete_task(1)
    service.complete_task(1)  # Should not error

    retrieved = service.get_task_by_id(1)
    assert retrieved["completed"] == True

    # Mark incomplete twice
    service.uncomplete_task(1)
    service.uncomplete_task(1)  # Should not error

    retrieved = service.get_task_by_id(1)
    assert retrieved["completed"] == False

def test_timestamp_behavior(fresh_service):
    """
    Test that timestamps behave correctly.

    Verify created_at is immutable, updated_at changes.
    """
    service = fresh_service

    task = service.add_task("Test Task")
    original_created = task["created_at"]
    original_updated = task["updated_at"]

    # Wait briefly to ensure timestamp difference
    time.sleep(0.01)

    # Update task
    updated = service.update_task(1, title="New Title")

    # created_at should be unchanged
    assert updated["created_at"] == original_created

    # updated_at should be different
    assert updated["updated_at"] != original_updated
```

**Success Criteria:**
- [ ] All 6 integration tests implemented
- [ ] All tests pass
- [ ] Tests cover complete workflows
- [ ] Tests verify data integrity
- [ ] Tests verify error recovery
- [ ] File passes type checking

**Validation Commands:**
```bash
cd phase1
pytest tests/test_integration.py -v
pytest tests/test_integration.py --cov=src --cov-report=term-missing
mypy tests/test_integration.py
```

**Estimated Effort:** 45 minutes

---

### Task 4.7: Verify Test Coverage and Quality Gates
**Status:** ⬜

**Description:**
Run complete test suite, verify ≥80% coverage, and ensure all quality checks pass.

**Files to Verify:**
- All source files in `src/`
- All test files in `tests/`

**Spec Reference:**
- [SPECIFICATION.md § Acceptance Criteria § NFR4: Testing](./SPECIFICATION.md#acceptance-criteria)
- [PLAN.md § Step 6: Unit Testing & Quality Assurance](./PLAN.md#step-6-unit-testing--quality-assurance)

**Implementation Details:**

No new files to create. Execute validation commands and fix any issues.

**Quality Checks:**

1. **Run all tests:**
   ```bash
   pytest tests/ -v
   ```

2. **Check coverage:**
   ```bash
   pytest --cov=src --cov-report=html --cov-report=term-missing
   ```
   - Verify overall coverage ≥80%
   - Check coverage by module:
     - models.py: 100%
     - exceptions.py: 100%
     - task_repository.py: ≥90%
     - task_service.py: ≥85%
     - cli_formatter.py: ≥70%
     - command_parser.py: ≥80%
     - main.py: ≥60%

3. **Type checking:**
   ```bash
   mypy src/ tests/
   ```

4. **Linting:**
   ```bash
   ruff check src/ tests/
   ```

5. **Count tests:**
   ```bash
   pytest --collect-only
   ```
   - Should show ~40+ tests total

**Success Criteria:**
- [ ] All tests pass (0 failures)
- [ ] Overall test coverage ≥80%
- [ ] No type errors from mypy
- [ ] No linting errors from ruff
- [ ] All modules have docstrings
- [ ] All public functions have docstrings
- [ ] Test count ≥40

**If Coverage < 80%:**
1. Identify uncovered lines: `pytest --cov=src --cov-report=term-missing`
2. Add tests for uncovered code paths
3. Re-run coverage check
4. **DO NOT** modify source code to inflate coverage

**Validation Commands:**
```bash
cd phase1
pytest tests/ -v --tb=short
pytest --cov=src --cov-report=html --cov-report=term-missing
mypy src/ tests/
ruff check src/ tests/
pytest --collect-only | grep "test session starts"
```

**Estimated Effort:** 30 minutes (including fixing issues)

---

## Milestone 5: Documentation & Polish

### Task 5.1: Write Comprehensive README
**Status:** ⬜

**Description:**
Create complete user-facing documentation with installation, usage, and examples.

**Files to Modify:**
- `phase1/README.md` (replace stub)

**Spec Reference:**
- [SPECIFICATION.md § CLI Interface Specification](./SPECIFICATION.md#cli-interface-specification)
- [PLAN.md § Step 7.1: Update README.md](./PLAN.md#step-7-documentation--user-onboarding)

**Implementation Details:**

Replace `README.md` stub with comprehensive documentation including:

1. **Project Overview**
   - What is Phase I
   - Evolution of Todo context
   - Key features

2. **Features List**
   - All 7 core features with brief descriptions

3. **Requirements**
   - Python 3.10+
   - No runtime dependencies

4. **Installation**
   ```bash
   # Clone/download
   cd phase1
   pip install -r requirements.txt
   ```

5. **Usage**
   - How to start: `python src/main.py`
   - Basic workflow example (add → list → complete)

6. **Command Reference**
   - Table of all 9 commands
   - Syntax for each command
   - Example for each command (copy from SPECIFICATION.md)

7. **Examples**
   - Complete walkthrough session (code block)
   - Multiple example scenarios

8. **Development**
   - Running tests: `pytest`
   - Coverage: `pytest --cov=src`
   - Type checking: `mypy src/`
   - Linting: `ruff check src/`

9. **Architecture**
   - Brief 3-layer overview
   - File structure

10. **Limitations**
    - In-memory only (no persistence)
    - Single-user
    - Data lost on exit

11. **Future (Phase II)**
    - Preview of web app evolution

**Success Criteria:**
- [ ] README has all 11 sections
- [ ] Installation instructions work on fresh environment
- [ ] All command examples are accurate
- [ ] Walkthrough example can be copy-pasted
- [ ] Markdown formatting is correct
- [ ] Links to other docs work
- [ ] README is 250-350 lines

**Validation Commands:**
```bash
cd phase1
cat README.md | head -20  # Check header
grep -i "installation" README.md
grep -i "usage" README.md
grep -i "command" README.md
```

**Estimated Effort:** 45 minutes

---

### Task 5.2: Write Architecture Documentation
**Status:** ⬜

**Description:**
Document system design, module descriptions, and design rationale.

**Files to Create:**
- `phase1/ARCHITECTURE.md`

**Spec Reference:**
- [PLAN.md § Step 7.2: Create ARCHITECTURE.md](./PLAN.md#step-7-documentation--user-onboarding)

**Implementation Details:**

Create `ARCHITECTURE.md` with:

1. **System Overview**
   - High-level architecture diagram (ASCII or Markdown)
   - 3-layer architecture description

2. **Layer Descriptions**
   - **Presentation Layer (CLI)**: main.py, cli_formatter.py, command_parser.py
   - **Business Logic Layer**: task_service.py
   - **Data Layer**: task_repository.py, models.py, exceptions.py

3. **Module Descriptions**
   - For each module: purpose, responsibilities, key functions

4. **Data Flow Example**
   - Trace "add task" command through all layers

5. **Design Decisions**
   - Why TypedDict instead of dataclass
   - Why repository pattern in Phase I
   - Why in-memory storage
   - Separation of concerns rationale

6. **Evolution to Phase II**
   - How architecture prepares for web app
   - What will change (storage → database, CLI → API)
   - What will remain (service layer logic)

7. **Testing Strategy**
   - Test pyramid overview
   - Unit vs integration tests

**Success Criteria:**
- [ ] All 7 sections present
- [ ] Architecture diagram clear
- [ ] Each module documented
- [ ] Design rationale explained
- [ ] Migration path to Phase II described
- [ ] Document is 150-250 lines

**Validation Commands:**
```bash
cd phase1
cat ARCHITECTURE.md | head -20
grep -i "layer" ARCHITECTURE.md
grep -i "phase ii" ARCHITECTURE.md
```

**Estimated Effort:** 30 minutes

---

### Task 5.3: Write Testing Documentation
**Status:** ⬜

**Description:**
Document testing approach, how to run tests, and how to interpret results.

**Files to Create:**
- `phase1/TESTING.md`

**Spec Reference:**
- [PLAN.md § Step 7.3: Create TESTING.md](./PLAN.md#step-7-documentation--user-onboarding)

**Implementation Details:**

Create `TESTING.md` with:

1. **Overview**
   - Testing philosophy
   - Coverage goals (≥80%)

2. **Test Structure**
   - Explain 4 test modules:
     - test_task_repository.py (data layer)
     - test_task_service.py (business logic)
     - test_models.py (data structures)
     - test_integration.py (end-to-end)

3. **Running Tests**
   ```bash
   # All tests
   pytest

   # Specific file
   pytest tests/test_task_service.py

   # Specific test
   pytest tests/test_task_service.py::test_add_task_with_title_and_description

   # With coverage
   pytest --cov=src --cov-report=html

   # Verbose output
   pytest -v
   ```

4. **Coverage Goals**
   - Overall: ≥80%
   - Per module breakdown

5. **Interpreting Results**
   - How to read pytest output
   - How to read coverage reports
   - What to do if tests fail

6. **Adding New Tests**
   - Guidelines for contributors
   - Using fixtures
   - Naming conventions

7. **Continuous Integration**
   - (Placeholder for future CI/CD)

**Success Criteria:**
- [ ] All 7 sections present
- [ ] All commands tested and accurate
- [ ] Coverage goals documented
- [ ] Examples of test execution provided
- [ ] Document is 80-120 lines

**Validation Commands:**
```bash
cd phase1
cat TESTING.md
grep -i "pytest" TESTING.md
grep -i "coverage" TESTING.md
```

**Estimated Effort:** 20 minutes

---

### Task 5.4: Final Integration Test - Complete User Session
**Status:** ⬜

**Description:**
Manually test the complete application by running it and executing a full user session to verify all features work correctly.

**Files to Test:**
- `phase1/src/main.py` (complete application)

**Spec Reference:**
- [SPECIFICATION.md § CLI Interface Specification](./SPECIFICATION.md#cli-interface-specification)
- All feature specifications

**Implementation Details:**

**Manual Test Script:**

```bash
cd phase1
python src/main.py
```

Execute this sequence of commands in the application:

```
> help
# Verify: Help text displays all commands

> add "Buy groceries" "Milk, eggs, bread"
# Verify: Task created with ID 1

> add "Finish report"
# Verify: Task created with ID 2

> list
# Verify: Shows 2 tasks, both incomplete

> view 1
# Verify: Shows all details for task 1

> complete 1
# Verify: Task 1 marked complete

> list
# Verify: Task 1 shows [✓], task 2 shows [ ]

> update 2 --title "Finish Q4 report"
# Verify: Task 2 title updated

> view 2
# Verify: Title changed, updated_at changed, created_at same

> uncomplete 1
# Verify: Task 1 marked incomplete

> delete 1
# Verify: Task 1 deleted

> list
# Verify: Only task 2 remains

> add ""
# Verify: Error message about empty title

> view 999
# Verify: Error message about task not found

> invalid_command
# Verify: Error message about unknown command

> exit
# Verify: Goodbye message, application exits
```

**Success Criteria:**
- [ ] Application starts with welcome message
- [ ] Help command shows all 9 commands
- [ ] Can add task with title and description
- [ ] Can add task with title only
- [ ] List shows all tasks in table format
- [ ] View shows complete task details
- [ ] Update changes title/description
- [ ] Complete/uncomplete toggle status correctly
- [ ] Delete removes task
- [ ] Empty title shows error
- [ ] Invalid task ID shows error
- [ ] Unknown command shows error
- [ ] Exit terminates gracefully
- [ ] No crashes or exceptions during session

**Validation Commands:**
```bash
cd phase1
python src/main.py
# Follow manual test script above
```

**Estimated Effort:** 20 minutes

---

## Phase I Completion Checklist

### All Tasks Complete
- [ ] Milestone 1: Foundation (Tasks 1.1-1.4) ✅
- [ ] Milestone 2: Business Logic (Tasks 2.1-2.6) ✅
- [ ] Milestone 3: CLI Interface (Tasks 3.1-3.3) ✅
- [ ] Milestone 4: Testing (Tasks 4.1-4.7) ✅
- [ ] Milestone 5: Documentation (Tasks 5.1-5.4) ✅

### Quality Gates
- [ ] Test coverage ≥80%
- [ ] All tests passing
- [ ] No type errors (mypy)
- [ ] No linting errors (ruff)
- [ ] All code has docstrings
- [ ] All functions have type hints

### Documentation Complete
- [ ] README.md comprehensive
- [ ] ARCHITECTURE.md complete
- [ ] TESTING.md complete
- [ ] Code comments for complex logic

### User Experience
- [ ] Application runs without errors
- [ ] All commands work as specified
- [ ] Error messages are clear
- [ ] Help text is comprehensive

### Specification Compliance
- [ ] All 7 features implemented per spec
- [ ] All acceptance criteria met
- [ ] All error cases handled
- [ ] All success messages formatted correctly

---

## Task Execution Summary

**Total Tasks:** 22
**Estimated Total Effort:** ~9-11 hours

**Breakdown by Milestone:**
- Milestone 1 (Foundation): 4 tasks, ~1.5 hours
- Milestone 2 (Business Logic): 6 tasks, ~2.5 hours
- Milestone 3 (CLI): 3 tasks, ~2.5 hours
- Milestone 4 (Testing): 7 tasks, ~3.5 hours
- Milestone 5 (Documentation): 4 tasks, ~2 hours

**Critical Path:**
Tasks must be executed in order within each milestone due to dependencies.
Milestones 4 and 5 can partially overlap (start docs while finalizing tests).

---

## Next Steps

**Status:** ✅ Task list ready for execution

**Begin Implementation:**
```
Start with Task 1.1: Create Project Directory Structure
```

**Execution Strategy:**
1. Execute tasks sequentially
2. Validate each task before proceeding
3. If validation fails, debug or refine spec
4. Mark task complete only when all criteria met
5. After all tasks: run final integration test (Task 5.4)

**Track Progress:**
Update task status (⬜ → 🔄 → ✅) as you complete each one.

---

**Task List Version:** 1.0.0
**Created:** 2025-12-26
**Status:** READY FOR EXECUTION
