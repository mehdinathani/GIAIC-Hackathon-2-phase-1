# Quickstart: Todo Organization & Intelligence

## Test Scenarios

### 1. Basic Organization
```bash
uv run todo add "Critical Fix" --priority HIGH --tags "#work,#urgent"
uv run todo list
# EXPECTED: "Critical Fix" shown with [HIGH] in Red and both tags listed.
```

### 2. Search & Filter
```bash
uv run todo list --search "Fix"
# EXPECTED: Only "Critical Fix" visible.

uv run todo list --filter-priority MEDIUM
# EXPECTED: Only tasks with MEDIUM priority visible.
```

### 3. Intelligence Engine (Recurrence)
```bash
# Set a task for today
uv run todo add "Daily Exercise" --recurrence DAILY --due-date 2026-01-01
uv run todo list
# Locate the ID (e.g., 5)

uv run todo complete 5
# EXPECTED: A new "Daily Exercise" task appears with due_date 2026-01-02.
```

### 4. Overdue Highlighting
```bash
uv run todo add "Late Task" --due-date 2025-12-25
uv run todo list
# EXPECTED: "Late Task" title rendered in BOLD RED.
```

### 5. Validation Errors
```bash
uv run todo add "Bad Date" --due-date "not-a-date"
# EXPECTED: Re-prompting or clear error message prompting for YYYY-MM-DD.
```
