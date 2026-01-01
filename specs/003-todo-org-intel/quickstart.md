# Quickstart: Todo Organization & Intelligence

## Test Scenarios

### 1. Basic Organization
```bash
todo add "Finish report" --priority high --tag work
todo list --filter-priority high
# EXPECTED: "Finish report" shown in Red with #work tag
```

### 2. Search & Filter
```bash
todo add "Buy milk" --tag home
todo add "Call vet" --tag home
todo list --filter-tag home
# EXPECTED: Both home tasks shown
```

### 3. Intelligence Engine (Recurrence)
```bash
todo add "Daily Standup" --recur daily --due 2025-12-31
todo complete <id>
todo list
# EXPECTED: "Daily Standup" (new instance) appears with due date 2026-01-01
```

### 4. Overdue Highlighting
```bash
# Given a task with due date in the past
todo list
# EXPECTED: Task title is BOLD RED
```
