# Data Model: Phase I - CLI Basics

**Branch**: `001-cli-basics` | **Date**: 2025-12-28

## Entities

### Task

The core entity representing a single todo item.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | `int` | Primary key, auto-increment, >= 1 | Unique identifier |
| `title` | `str` | Required, 1-255 chars, non-empty | Task title |
| `description` | `str \| None` | Optional, max 1000 chars | Detailed description |
| `completed` | `bool` | Default: `False` | Completion status |
| `created_at` | `datetime` | Auto-set on creation, immutable | Creation timestamp |

**Validation Rules**:
- `title` must be non-empty after stripping whitespace
- `title` length must be between 1 and 255 characters
- `description` length must not exceed 1000 characters (if provided)
- `id` is assigned by the repository, not user-provided

**State Transitions**:
```
[Created] --> completed=False (Pending)
         --> completed=True  (Completed)
         --> [Deleted]
```

---

### TaskCreate (Input DTO)

Data transfer object for creating new tasks.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `title` | `str` | Required, 1-255 chars | Task title |
| `description` | `str \| None` | Optional | Detailed description |

---

### TaskUpdate (Input DTO)

Data transfer object for updating existing tasks.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `title` | `str \| None` | Optional, 1-255 chars if provided | New title |
| `description` | `str \| None` | Optional | New description |

**Note**: At least one field must be provided for update.

---

## Repository Interface

The repository provides an abstraction over data storage.

### ITaskRepository (Protocol)

```
Interface: ITaskRepository

Methods:
- add(task: Task) -> Task
  Creates a new task, assigns ID, returns task with ID

- get(id: int) -> Task | None
  Retrieves task by ID, returns None if not found

- get_all() -> list[Task]
  Returns all tasks, ordered by created_at ascending

- update(id: int, data: TaskUpdate) -> Task | None
  Updates task fields, returns updated task or None if not found

- delete(id: int) -> bool
  Removes task by ID, returns True if deleted, False if not found

- exists(id: int) -> bool
  Checks if task with ID exists
```

### InMemoryTaskRepository

Phase I implementation using Python dictionary.

**Internal State**:
- `_tasks: dict[int, Task]` - Storage keyed by task ID
- `_next_id: int` - Counter for ID generation (starts at 1)

**Behavior**:
- IDs are assigned sequentially and never reused
- Tasks are stored by reference (no deep copy needed for Phase I)
- Thread-safety not required (single-user assumption)

---

## Service Layer

### TaskService

Business logic layer that uses repository.

**Dependencies**:
- `repository: ITaskRepository`

**Methods**:
```
- create_task(data: TaskCreate) -> Task
  Validates input, creates task via repository

- get_task(id: int) -> Task
  Retrieves task, raises TaskNotFoundError if not found

- list_tasks() -> list[Task]
  Returns all tasks from repository

- complete_task(id: int) -> Task
  Sets completed=True, raises TaskNotFoundError if not found

- update_task(id: int, data: TaskUpdate) -> Task
  Updates task fields, raises TaskNotFoundError if not found

- delete_task(id: int) -> None
  Deletes task, raises TaskNotFoundError if not found
```

**Exceptions**:
- `TaskNotFoundError(task_id: int)` - Raised when task ID doesn't exist
- `ValidationError` - Raised by Pydantic for invalid input

---

## Relationships

```
┌─────────────┐     uses      ┌──────────────────┐
│  CLI Layer  │ ───────────── │   TaskService    │
│  (Typer)    │               │ (Business Logic) │
└─────────────┘               └──────────────────┘
                                      │
                                      │ uses
                                      ▼
                              ┌──────────────────┐
                              │ ITaskRepository  │
                              │   (Protocol)     │
                              └──────────────────┘
                                      △
                                      │ implements
                                      │
                              ┌──────────────────┐
                              │ InMemoryTask     │
                              │ Repository       │
                              └──────────────────┘
```

---

## Data Flow Examples

### Add Task
1. CLI receives `add "Buy milk" --description "2% milk"`
2. CLI creates `TaskCreate(title="Buy milk", description="2% milk")`
3. Service validates input via Pydantic
4. Service calls `repository.add(task)`
5. Repository assigns ID, stores task, returns task
6. CLI displays success panel with task details

### Complete Task
1. CLI receives `complete 1`
2. CLI calls `service.complete_task(1)`
3. Service calls `repository.get(1)`
4. If found: Service updates task, calls `repository.update(1, ...)`
5. If not found: Service raises `TaskNotFoundError`
6. CLI displays result (success panel or error panel)

### List Tasks
1. CLI receives `list`
2. CLI calls `service.list_tasks()`
3. Service calls `repository.get_all()`
4. CLI formats tasks as Rich table
5. If empty: CLI displays "No tasks found" message
