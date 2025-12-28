# Quickstart: Phase I - CLI Basics

**Branch**: `001-cli-basics` | **Date**: 2025-12-28

## Prerequisites

- Python 3.13+
- `uv` package manager installed
- WSL 2 environment (Windows) or Linux

## Installation

```bash
# Clone repository and navigate to project
cd phase1

# Install dependencies with uv
uv sync

# Verify installation
uv run todo --help
```

## Basic Usage

### Add a Task

```bash
# Simple task
uv run todo add "Buy groceries"

# Task with description
uv run todo add "Call dentist" -d "Schedule annual checkup"
```

### View All Tasks

```bash
uv run todo list
```

### Complete a Task

```bash
# Complete task with ID 1
uv run todo complete 1
```

### Update a Task

```bash
# Update title only
uv run todo update 1 -t "Buy organic groceries"

# Update description only
uv run todo update 1 -d "From Whole Foods"

# Update both
uv run todo update 1 -t "Buy organic groceries" -d "From Whole Foods"
```

### Delete a Task

```bash
uv run todo delete 1
```

## Example Session

```bash
$ uv run todo add "Learn Python"
╭─ Task Created ─────────────────────────────╮
│ ID: 1                                      │
│ Title: Learn Python                        │
│ Status: Pending                            │
╰────────────────────────────────────────────╯

$ uv run todo add "Build CLI app" -d "Using Typer and Rich"
╭─ Task Created ─────────────────────────────╮
│ ID: 2                                      │
│ Title: Build CLI app                       │
│ Description: Using Typer and Rich          │
│ Status: Pending                            │
╰────────────────────────────────────────────╯

$ uv run todo list
┏━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Title          ┃ Status    ┃ Created             ┃
┡━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ Learn Python   │ Pending   │ 2025-12-28 10:30:00 │
│ 2  │ Build CLI app  │ Pending   │ 2025-12-28 10:31:00 │
└────┴────────────────┴───────────┴─────────────────────┘

$ uv run todo complete 1
╭─ Task Completed ───────────────────────────╮
│ Task 1 marked as completed                 │
│ Title: Learn Python                        │
╰────────────────────────────────────────────╯

$ uv run todo list
┏━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Title          ┃ Status    ┃ Created             ┃
┡━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ Learn Python   │ Completed │ 2025-12-28 10:30:00 │
│ 2  │ Build CLI app  │ Pending   │ 2025-12-28 10:31:00 │
└────┴────────────────┴───────────┴─────────────────────┘
```

## Project Structure

```
phase1/
├── pyproject.toml          # Project configuration
├── src/
│   └── todo/
│       ├── __init__.py
│       ├── models.py       # Pydantic Task model
│       ├── repository.py   # InMemoryTaskRepository
│       ├── service.py      # TaskService business logic
│       └── cli.py          # Typer CLI commands
└── tests/
    ├── unit/
    │   ├── test_models.py
    │   ├── test_repository.py
    │   └── test_service.py
    └── integration/
        └── test_cli.py
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/todo

# Run specific test file
uv run pytest tests/unit/test_service.py
```

## Linting

```bash
# Check code style
uv run ruff check src/

# Auto-fix issues
uv run ruff check --fix src/

# Format code
uv run ruff format src/
```

## Important Notes

1. **Data Persistence**: Tasks are stored in memory only. All tasks are lost when the process exits. This is by design for Phase I.

2. **Single User**: The application is designed for single-user operation. No concurrent access handling is implemented.

3. **ID Assignment**: Task IDs are sequential integers starting from 1. IDs are never reused, even after deletion.

## Next Steps

After completing Phase I, Phase II will add:
- PostgreSQL persistence via Neon
- The Service layer will remain unchanged (Repository pattern benefit!)
