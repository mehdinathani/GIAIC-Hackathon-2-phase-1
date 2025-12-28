# CLI Interface Contract: Phase I - CLI Basics

**Branch**: `001-cli-basics` | **Date**: 2025-12-28

## Overview

This document defines the CLI interface contract for the Todo application.
All commands follow the pattern: `todo <command> [arguments] [options]`

---

## Commands

### `todo add`

Creates a new task.

**Signature**:
```
todo add <title> [--description, -d TEXT]
```

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `title` | `str` | Yes | Task title (1-255 chars) |

**Options**:
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--description`, `-d` | `str` | None | Optional description |

**Success Output** (exit code 0):
```
╭─ Task Created ─────────────────────────────╮
│ ID: 1                                      │
│ Title: Buy milk                            │
│ Description: 2% milk from grocery store    │
│ Status: Pending                            │
│ Created: 2025-12-28 10:30:00              │
╰────────────────────────────────────────────╯
```

**Error Output** (exit code 1):
```
╭─ Validation Error ─────────────────────────╮
│ Title cannot be empty                      │
╰────────────────────────────────────────────╯
```

---

### `todo list`

Displays all tasks in a formatted table.

**Signature**:
```
todo list
```

**Arguments**: None

**Options**: None

**Success Output** (with tasks, exit code 0):
```
┏━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Title          ┃ Status    ┃ Created             ┃
┡━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ Buy milk       │ Pending   │ 2025-12-28 10:30:00 │
│ 2  │ Call dentist   │ Completed │ 2025-12-28 10:31:00 │
│ 3  │ Write report   │ Pending   │ 2025-12-28 10:32:00 │
└────┴────────────────┴───────────┴─────────────────────┘
```

**Success Output** (no tasks, exit code 0):
```
╭─ Info ─────────────────────────────────────╮
│ No tasks found. Add one with: todo add     │
╰────────────────────────────────────────────╯
```

---

### `todo complete`

Marks a task as completed.

**Signature**:
```
todo complete <task_id>
```

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_id` | `int` | Yes | ID of task to complete |

**Options**: None

**Success Output** (exit code 0):
```
╭─ Task Completed ───────────────────────────╮
│ Task 1 marked as completed                 │
│ Title: Buy milk                            │
╰────────────────────────────────────────────╯
```

**Error Output** (exit code 1):
```
╭─ Error ────────────────────────────────────╮
│ Task with ID 99 not found                  │
╰────────────────────────────────────────────╯
```

---

### `todo update`

Updates an existing task's title and/or description.

**Signature**:
```
todo update <task_id> [--title, -t TEXT] [--description, -d TEXT]
```

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_id` | `int` | Yes | ID of task to update |

**Options**:
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--title`, `-t` | `str` | None | New title |
| `--description`, `-d` | `str` | None | New description |

**Note**: At least one option must be provided.

**Success Output** (exit code 0):
```
╭─ Task Updated ─────────────────────────────╮
│ ID: 1                                      │
│ Title: Buy 2% milk                         │
│ Description: From the grocery store        │
│ Status: Pending                            │
╰────────────────────────────────────────────╯
```

**Error Output** (exit code 1):
```
╭─ Error ────────────────────────────────────╮
│ Task with ID 99 not found                  │
╰────────────────────────────────────────────╯
```

---

### `todo delete`

Permanently removes a task.

**Signature**:
```
todo delete <task_id>
```

**Arguments**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `task_id` | `int` | Yes | ID of task to delete |

**Options**: None

**Success Output** (exit code 0):
```
╭─ Task Deleted ─────────────────────────────╮
│ Task 1 has been deleted                    │
╰────────────────────────────────────────────╯
```

**Error Output** (exit code 1):
```
╭─ Error ────────────────────────────────────╮
│ Task with ID 99 not found                  │
╰────────────────────────────────────────────╯
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (validation, not found, etc.) |
| 2 | Invalid usage (missing arguments) |

---

## Help Output

Each command supports `--help`:

```
$ todo add --help

 Usage: todo add [OPTIONS] TITLE

 Create a new task.

╭─ Arguments ────────────────────────────────────────────────────╮
│ *    title      TEXT  Task title [required]                    │
╰────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────╮
│ --description  -d      TEXT  Optional task description         │
│ --help                       Show this message and exit        │
╰────────────────────────────────────────────────────────────────╯
```

---

## Styling Guidelines

All output uses Rich library with consistent styling:

| Element | Style |
|---------|-------|
| Success panels | Green border |
| Error panels | Red border |
| Info panels | Blue border |
| Table headers | Bold |
| Pending status | Yellow |
| Completed status | Green with strikethrough |
| Task IDs | Cyan |
