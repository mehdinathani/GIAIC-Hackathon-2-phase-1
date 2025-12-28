# Interactive CLI Interface Contract: Phase II

**Branch**: `002-interactive-cli` | **Date**: 2025-12-28

## Overview

This document defines the interactive CLI interface contract. The application launches into an interactive menu when invoked without subcommands.

---

## Entry Point

### Launch Interactive Mode

**Command**:
```bash
uv run todo
```

**Behavior**: When `todo` is called without any subcommand, launch interactive mode.

**Existing Commands Preserved**: All Phase I commands remain functional:
- `uv run todo add <title>`
- `uv run todo list`
- `uv run todo complete <id>`
- `uv run todo update <id>`
- `uv run todo delete <id>`

---

## Screen Contracts

### Main Menu Screen

**Display**:
```
=====================================
       TODO - Task Manager
=====================================

? What would you like to do?
> Add Task
  View Task List
  Mark Task Complete
  Update Task
  Delete Task
  Exit

(Use arrow keys to navigate, Enter to select)
```

**Inputs**:
| Key | Action |
|-----|--------|
| Up/Down Arrow | Navigate between options |
| Enter | Select highlighted option |
| q / Escape | Exit application |

**Options**:
| Option | Navigates To |
|--------|--------------|
| Add Task | Add Task Prompt |
| View Task List | Task List Screen |
| Mark Task Complete | Task Selection (for complete) |
| Update Task | Task Selection (for update) |
| Delete Task | Task Selection (for delete) |
| Exit | Goodbye Screen |

---

### Add Task Prompt

**Display**:
```
=====================================
         Add New Task
=====================================

? Enter task title: _

(Press Escape to cancel)
```

**Flow**:
1. Prompt for title (required)
2. Prompt for description (optional, press Enter to skip)
3. Show success message
4. Return to Main Menu

**Success Output**:
```
+------------------------------- Task Created --------------------------------+
| ID: 1                                                                       |
| Title: Buy groceries                                                        |
| Status: Pending                                                             |
+-----------------------------------------------------------------------------+

Press Enter to continue...
```

**Cancel**: Press Escape at any prompt to return to Main Menu.

---

### Task List Screen

**Display (with tasks)**:
```
=====================================
         Your Tasks
=====================================

? Select a task (or press Escape to go back):
> [1] Buy groceries          Pending    2025-12-28
  [2] Call dentist           Completed  2025-12-28
  [3] Finish report          Pending    2025-12-28

(Use arrow keys to navigate, Enter to select)
```

**Display (empty)**:
```
=====================================
         Your Tasks
=====================================

+----------------------------------- Info ------------------------------------+
| No tasks found. Would you like to add one?                                  |
+-----------------------------------------------------------------------------+

? Add a task now?
> Yes
  No (return to menu)
```

**Inputs**:
| Key | Action |
|-----|--------|
| Up/Down Arrow | Navigate between tasks |
| Enter | Open Task Actions menu |
| Escape | Return to Main Menu |

---

### Task Actions Menu (Context Menu)

**Display**:
```
=====================================
    Task: Buy groceries
=====================================

? What would you like to do with this task?
> Mark Complete
  Update
  Delete
  Back to List

(Use arrow keys to navigate, Enter to select)
```

**Options**:
| Option | Action |
|--------|--------|
| Mark Complete | Set task.completed = True, show success, return to list |
| Update | Show Update Prompts |
| Delete | Show Delete Confirmation |
| Back to List | Return to Task List Screen |

---

### Update Task Prompts

**Display**:
```
=====================================
    Update Task: Buy groceries
=====================================

Current title: Buy groceries
? Enter new title (or press Enter to keep current): _

Current description: (none)
? Enter new description (or press Enter to keep current): _
```

**Flow**:
1. Show current title, prompt for new (Enter = keep current)
2. Show current description, prompt for new (Enter = keep current)
3. Show success message
4. Return to Task List

**Cancel**: Press Escape to return to Task Actions without saving.

---

### Delete Confirmation

**Display**:
```
=====================================
    Delete Task: Buy groceries
=====================================

+---------------------------------- Warning ----------------------------------+
| This action cannot be undone!                                               |
+-----------------------------------------------------------------------------+

? Are you sure you want to delete this task?
> No
  Yes, delete it
```

**Default**: No (prevent accidental deletion)

**Flow**:
- Yes: Delete task, show success, return to Task List
- No: Return to Task Actions

---

### Goodbye Screen

**Display**:
```
+--------------------------------- Goodbye -----------------------------------+
| Thanks for using TODO! Your tasks are waiting for you next time.            |
+-----------------------------------------------------------------------------+
```

**Behavior**: Display message and exit process with code 0.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Normal exit (user chose Exit or Ctrl+C handled gracefully) |
| 1 | Error (should not occur in interactive mode) |

---

## Keyboard Shortcuts Summary

| Key | Global Action |
|-----|---------------|
| Up Arrow | Previous option |
| Down Arrow | Next option |
| Enter | Select/Confirm |
| Escape | Cancel/Back/Exit |
| q | Exit (from main menu only) |
| Ctrl+C | Graceful exit |

---

## Visual Style

| Element | Style |
|---------|-------|
| Header | Bold, centered |
| Selected option | Cyan highlight with > pointer |
| Success messages | Green border panel |
| Error messages | Red border panel |
| Info messages | Blue border panel |
| Warning messages | Yellow border panel |
| Completed tasks | Green text |
| Pending tasks | Yellow text |
