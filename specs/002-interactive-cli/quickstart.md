# Quickstart: Phase II - Interactive CLI

**Branch**: `002-interactive-cli` | **Date**: 2025-12-28

## Prerequisites

- Python 3.13+
- `uv` package manager installed
- Phase I implementation complete

## Installation

```bash
# Navigate to project
cd phase1

# Install new dependency
uv add questionary

# Verify installation
uv run todo --help
```

## Launch Interactive Mode

```bash
# Start interactive mode (no subcommand)
uv run todo
```

This launches the interactive menu interface.

## Quick Navigation Guide

### Main Menu
- Use **Up/Down arrows** to navigate
- Press **Enter** to select an option
- Press **q** or **Escape** to exit

### Task List
- Use **Up/Down arrows** to select a task
- Press **Enter** to open task actions
- Press **Escape** to go back

### Prompts
- Type your input and press **Enter**
- Press **Escape** to cancel

## Example Session

```
$ uv run todo

=====================================
       TODO - Task Manager
=====================================

? What would you like to do? (Use arrow keys)
> Add Task
  View Task List
  Mark Task Complete
  Update Task
  Delete Task
  Exit

[User selects "Add Task"]

=====================================
         Add New Task
=====================================

? Enter task title: Buy groceries
? Enter description (optional): Milk, bread, eggs

+------------------------------- Task Created --------------------------------+
| ID: 1                                                                       |
| Title: Buy groceries                                                        |
| Description: Milk, bread, eggs                                              |
| Status: Pending                                                             |
+-----------------------------------------------------------------------------+

Press Enter to continue...

[Returns to main menu]

? What would you like to do?
> View Task List

=====================================
         Your Tasks
=====================================

? Select a task:
> [1] Buy groceries          Pending    2025-12-28

[User selects task]

=====================================
    Task: Buy groceries
=====================================

? What would you like to do with this task?
> Mark Complete
  Update
  Delete
  Back to List

[User selects "Mark Complete"]

+------------------------------- Task Completed ------------------------------+
| Task 1 marked as completed                                                  |
+-----------------------------------------------------------------------------+

[Returns to task list with updated status]
```

## Existing CLI Commands (Still Available)

All Phase I commands continue to work:

```bash
# Quick add (non-interactive)
uv run todo add "Quick task"

# Quick list
uv run todo list

# Quick complete
uv run todo complete 1

# Quick update
uv run todo update 1 -t "New title"

# Quick delete
uv run todo delete 1
```

## Keyboard Reference

| Key | Action |
|-----|--------|
| Up Arrow | Move selection up |
| Down Arrow | Move selection down |
| Enter | Select / Confirm |
| Escape | Cancel / Go back |
| q | Exit (from main menu) |
| Ctrl+C | Graceful exit |

## Running Tests

```bash
# Run all tests
uv run pytest

# Run interactive module tests only
uv run pytest tests/unit/test_interactive.py

# Run integration tests
uv run pytest tests/integration/test_interactive_cli.py
```

## Important Notes

1. **In-Memory Storage**: Tasks are stored in memory only (Phase I behavior). All tasks are lost when the application exits.

2. **Single User**: The application is designed for single-user operation.

3. **Terminal Requirements**: Requires a terminal that supports ANSI color codes and raw input mode.

4. **Minimum Terminal Size**: 80x24 characters recommended.
