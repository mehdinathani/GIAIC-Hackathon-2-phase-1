# Data Model: Phase II - Interactive CLI

**Branch**: `002-interactive-cli` | **Date**: 2025-12-28

## Overview

This feature adds an interactive presentation layer. The core data model from Phase I (Task, TaskCreate, TaskUpdate) remains unchanged. This document defines the new UI-specific entities.

## Existing Entities (from Phase I - unchanged)

### Task
Core domain entity representing a todo item.
- `id`: int (auto-increment, >= 1)
- `title`: str (1-255 chars)
- `description`: str | None (max 1000 chars)
- `completed`: bool (default False)
- `created_at`: datetime

### TaskCreate / TaskUpdate
DTOs for creating and updating tasks (unchanged from Phase I).

---

## New Entities (Interactive UI)

### MenuItem

Represents a selectable option in the main menu.

| Field | Type | Description |
|-------|------|-------------|
| `label` | str | Display text shown to user |
| `value` | str | Internal identifier for action routing |
| `shortcut` | str | None | Optional keyboard shortcut (e.g., "a" for Add) |

**Enum Values**:
- ADD_TASK = "add_task"
- VIEW_LIST = "view_list"  
- MARK_COMPLETE = "mark_complete"
- UPDATE_TASK = "update_task"
- DELETE_TASK = "delete_task"
- EXIT = "exit"

### TaskAction

Represents an action available in the task context menu.

| Field | Type | Description |
|-------|------|-------------|
| `label` | str | Display text shown to user |
| `value` | str | Internal identifier for action |

**Enum Values**:
- COMPLETE = "complete"
- UPDATE = "update"
- DELETE = "delete"
- BACK = "back"

### PromptResult

Generic result wrapper for prompt operations.

| Field | Type | Description |
|-------|------|-------------|
| `cancelled` | bool | True if user pressed Escape/Ctrl+C |
| `value` | T | None | The result value if not cancelled |

---

## Screen States

The interactive app has the following screen states:

```
[MAIN_MENU] <──────────────────────────────────────┐
     │                                              │
     ├── Add Task ──► [ADD_PROMPT] ──► success ────┘
     │                     │
     │                     └── cancel ─────────────┘
     │
     ├── View List ──► [TASK_LIST] ──► Back ───────┘
     │                      │
     │                      └── Select Task ──► [TASK_ACTIONS]
     │                                               │
     │                      ┌────────────────────────┘
     │                      │
     │                      ├── Complete ──► success ──► [TASK_LIST]
     │                      ├── Update ──► [UPDATE_PROMPT] ──► [TASK_LIST]
     │                      ├── Delete ──► [CONFIRM] ──► [TASK_LIST]
     │                      └── Back ──► [TASK_LIST]
     │
     ├── Mark Complete ──► [TASK_LIST_SELECT] ──► success ──┘
     ├── Update Task ──► [TASK_LIST_SELECT] ──► [UPDATE_PROMPT] ──┘
     ├── Delete Task ──► [TASK_LIST_SELECT] ──► [CONFIRM] ──┘
     │
     └── Exit ──► [GOODBYE] ──► terminate
```

---

## Relationships

```
┌─────────────────┐     displays      ┌──────────────────┐
│  Interactive    │ ─────────────────► │   MenuItem[]     │
│     Menu        │                    │   (Main Menu)    │
└─────────────────┘                    └──────────────────┘
        │
        │ uses
        ▼
┌─────────────────┐     delegates     ┌──────────────────┐
│  TaskService    │ ◄──────────────── │  Phase I Service │
│  (from Phase I) │                    │  (unchanged)     │
└─────────────────┘                    └──────────────────┘
        │
        │ uses
        ▼
┌─────────────────┐
│ InMemoryTask    │
│ Repository      │
│ (from Phase I)  │
└─────────────────┘
```

---

## Style Configuration

### ColorScheme

Consistent colors across the interactive UI.

| Element | Color | Usage |
|---------|-------|-------|
| `highlight` | cyan | Selected menu item |
| `success` | green | Success messages, completed tasks |
| `error` | red | Error messages, delete confirmation |
| `info` | blue | Info panels, help text |
| `pending` | yellow | Pending task status |
| `muted` | dim/gray | Timestamps, secondary info |

---

## Notes

- All existing Phase I entities and behaviors are preserved
- Interactive mode is an additional presentation layer only
- No changes to repository or service layer required
- MenuItem and TaskAction are UI-only concepts (not persisted)
